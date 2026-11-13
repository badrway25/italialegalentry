"""Service-level tests: activation, import/export, anonymisation, purge, statistics."""

import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from freezegun import freeze_time

from audit.models import AuditEvent
from orientation import constants, engine, services
from orientation.models import OrientationResult, OrientationSession, Rule, Ruleset, RulesetStatus, SessionStatus

pytestmark = pytest.mark.django_db


def _request(user=None):
    request = RequestFactory().get("/fr/orientation/")
    from django.contrib.auth.models import AnonymousUser

    request.user = user or AnonymousUser()
    return request


def _run(request, session, answers):
    step = None
    for key, value in answers:
        step = services.submit_answer(request, session, key, value)
    return step


def test_spec_round_trip_through_database(active_ruleset):
    from orientation.seeds import build_v1_spec

    assert services.spec_for(active_ruleset) == build_v1_spec()


def test_activate_swaps_active_ruleset_atomically(active_ruleset, superuser):
    v2 = services.import_ruleset(services.export_ruleset(active_ruleset), version=2, user=superuser, notes="v2")
    assert v2.status == RulesetStatus.DRAFT and v2.questions.count() == 5
    services.activate_ruleset(v2, user=superuser)
    active_ruleset.refresh_from_db()
    assert active_ruleset.status == RulesetStatus.RETIRED
    assert services.active_ruleset() == v2 and v2.activated_at is not None
    assert AuditEvent.objects.filter(action="orientation.ruleset.activated", target_id=str(v2.pk)).exists()


def test_activate_refuses_invalid_ruleset(active_ruleset):
    broken = Ruleset.objects.create(version=3)
    with pytest.raises(services.RulesetInvalid) as exc:
        services.activate_ruleset(broken)
    assert exc.value.report.errors
    assert services.active_ruleset() == active_ruleset


def test_import_refuses_existing_version(active_ruleset):
    with pytest.raises(ValidationError):
        services.import_ruleset(services.export_ruleset(active_ruleset), version=1)
    imported = services.import_ruleset(services.export_ruleset(active_ruleset))
    assert imported.version == 2


def test_rule_clean_validates_conditions(active_ruleset):
    rule = Rule(ruleset=active_ruleset, name="bad", conditions={"question_key": "nope", "op": "eq", "value": "x"})
    with pytest.raises(ValidationError) as exc:
        rule.full_clean()
    assert "conditions" in exc.value.message_dict
    assert "next_question" in exc.value.message_dict  # no target at all
    q = active_ruleset.questions.get(key="objective")
    o = active_ruleset.outcomes.first()
    both = Rule(ruleset=active_ruleset, name="both", conditions={}, next_question=q, outcome=o)
    with pytest.raises(ValidationError):
        both.full_clean()
    ok = Rule(
        ruleset=active_ruleset,
        name="ok",
        conditions={"question_key": "objective", "op": "eq", "value": "work"},
        outcome=o,
    )
    ok.full_clean()


def test_db_constraints_one_active_and_one_entry(active_ruleset):
    from django.db import IntegrityError, transaction

    with pytest.raises(IntegrityError), transaction.atomic():
        Ruleset.objects.create(version=9, status=RulesetStatus.ACTIVE)
    from orientation.models import Question

    with pytest.raises(IntegrityError), transaction.atomic():
        Question.objects.create(ruleset=active_ruleset, key="second_entry", text_fr="x", is_entry=True)


def test_session_lifecycle_and_result(active_ruleset):
    request = _request()
    session = services.start_session(request)
    assert session.current_question.key == "objective"
    step = services.current_step(session)
    assert step.question.key == "objective" and step.progress == 0 and step.can_go_back is False
    step = _run(request, session, [("objective", "work"), ("work_profile", "highly_qualified")])
    assert step.question.key == "training_interest" and step.can_go_back
    step = services.go_back(session)
    assert step.question.key == "work_profile"
    step = _run(request, session, [("work_profile", "highly_qualified"), ("training_interest", "true")])
    assert step.result is not None and step.progress == 100
    session.refresh_from_db()
    result = OrientationResult.objects.get(session=session)
    assert result.outcome.pathway_key == "skilled_work_eu_blue_card"
    assert result.ruleset_version == 1 and result.disclaimer_version == constants.DISCLAIMER_VERSION
    assert result.result_text_fr.startswith("D’après vos réponses")
    assert session.status == SessionStatus.COMPLETED and session.current_question is None
    assert AuditEvent.objects.filter(action="orientation.session.completed").exists()
    event = AuditEvent.objects.get(action="orientation.session.completed")
    assert "answers" not in event.metadata and event.metadata["pathway_key"] == "skilled_work_eu_blue_card"


def test_submit_answer_rejects_stale_question(active_ruleset):
    request = _request()
    session = services.start_session(request)
    with pytest.raises(engine.InvalidAnswer):
        services.submit_answer(request, session, "work_profile", "salaried")
    with pytest.raises(engine.InvalidAnswer):
        services.submit_answer(request, session, "objective", "nope")


def test_start_session_requires_active_ruleset(db):
    with pytest.raises(services.NoActiveRuleset):
        services.start_session(_request())


def test_anonymise_session_strips_everything(active_ruleset, person_user):
    request = _request(person_user)
    session = services.start_session(request)
    _run(request, session, [("objective", "research")])
    session.refresh_from_db()
    assert session.user == person_user and session.resume_token_hash
    services.anonymise_session(session)
    session.refresh_from_db()
    assert session.user is None and session.ip_hash == "" and session.resume_token_hash == ""
    assert session.answers == {} and session.history == []
    assert session.result.answers_snapshot == {} and session.result.result_text_fr == ""
    assert session.result.outcome.pathway_key == "scientific_research"  # statistics kept
    assert AuditEvent.objects.filter(action="orientation.session.anonymised").exists()


def test_anonymise_user_sessions_and_delete(active_ruleset, person_user):
    request = _request(person_user)
    s1 = services.start_session(request)
    s2 = services.start_session(request)
    assert services.anonymise_user_sessions(person_user) == 2
    assert OrientationSession.objects.filter(user=person_user).count() == 0
    services.delete_session(s1)
    assert not OrientationSession.objects.filter(pk=s1.pk).exists()
    assert OrientationSession.objects.filter(pk=s2.pk).exists()


def test_purge_expired_sessions(active_ruleset, person_user):
    with freeze_time("2026-09-01 10:00:00"):
        anon_done = services.start_session(_request())
        _run(_request(), anon_done, [("objective", "research")])
        anon_open = services.start_session(_request())
        owned = services.start_session(_request(person_user))
    with freeze_time("2026-09-20 10:00:00"):
        fresh = services.start_session(_request())
    with freeze_time("2026-10-05 10:00:00"):
        report = services.purge_expired_sessions(dry_run=True)
        assert (report.deleted, report.anonymised, report.dry_run) == (1, 1, True)
        assert OrientationSession.objects.count() == 4
        report = services.purge_expired_sessions()
        assert (report.deleted, report.anonymised) == (1, 1)
        assert not OrientationSession.objects.filter(pk=anon_open.pk).exists()
        anon_done.refresh_from_db()
        assert anon_done.answers == {} and anon_done.resume_token_hash == ""
        assert OrientationSession.objects.filter(pk=owned.pk, user=person_user).exists()
        assert OrientationSession.objects.filter(pk=fresh.pk).exists()
        # second run is a no-op
        report = services.purge_expired_sessions()
        assert (report.deleted, report.anonymised) == (0, 0)


def test_expiry_is_refreshed_on_activity(active_ruleset):
    request = _request()
    with freeze_time("2026-09-17 10:00:00"):
        session = services.start_session(request)
        assert session.expires_at == session.created_at + dt.timedelta(days=constants.ANONYMOUS_SESSION_TTL_DAYS)
    with freeze_time("2026-09-27 10:00:00"):
        services.submit_answer(request, session, "objective", "work")
        session.refresh_from_db()
        assert session.expires_at.date() == dt.date(2026, 10, 27)
        assert session.is_expired() is False
    with freeze_time("2026-10-28 10:00:00"):
        assert session.is_expired() is True


def test_sessions_for_user_orders_recent_first(active_ruleset, person_user):
    request = _request(person_user)
    first = services.start_session(request)
    second = services.start_session(request)
    assert list(services.sessions_for_user(person_user)) == [second, first]
    from django.contrib.auth.models import AnonymousUser

    assert services.sessions_for_user(AnonymousUser()).count() == 0


def test_statistics_are_anonymised(active_ruleset):
    for objective in ("research", "research", "self_employment"):
        session = services.start_session(_request())
        _run(_request(), session, [("objective", objective)])
    csv_text = services.statistics_csv(OrientationResult.objects.all())
    lines = csv_text.strip().splitlines()
    assert lines[0] == "ruleset_version;outcome;pathway_key;language;disclaimer_version;total"
    assert "1;research;scientific_research;fr;2026-09-17.1;2" in lines
    assert "1;self_employment;self_employment_entrepreneurship;fr;2026-09-17.1;1" in lines
    for session in OrientationSession.objects.all():
        assert str(session.id) not in csv_text
    assert "objective" not in csv_text


def test_present_result_groups_checklist(active_ruleset):
    session = services.start_session(_request())
    _run(_request(), session, [("objective", "work"), ("work_profile", "salaried"), ("training_interest", "true")])
    session.refresh_from_db()
    presentation = services.present_result(session.result, "fr")
    assert presentation["pathway_key"] == "salaried_work"
    assert presentation["training_interest"] is True
    assert [g["key"] for g in presentation["checklist_groups"]] == ["documents", "steps", "authorities", "warnings"]
    assert presentation["disclaimer_locked_key"] == "p3.persons.how_it_works"
    assert presentation["kind"] == "INFORMATIVE_PREASSESSMENT"


def test_present_question_uses_published_translation_only(active_ruleset):
    from cms.models import TranslationStatus
    from orientation.models import ChoiceTranslation, Question, QuestionTranslation

    question = Question.objects.get(ruleset=active_ruleset, key="objective")
    spec_q = services.spec_for(active_ruleset).question_map["objective"]
    QuestionTranslation.objects.create(master=question, language="ar", text="سؤال", status=TranslationStatus.DRAFT)
    shown = services.present_question(active_ruleset, spec_q, "ar")
    assert shown["text"] == question.text_fr and shown["lang"] == "fr" and shown["fallback"] is True
    QuestionTranslation.objects.filter(master=question).update(status=TranslationStatus.PUBLISHED)
    choice = question.choices.get(key="work")
    ChoiceTranslation.objects.create(master=choice, language="ar", label="عمل", status=TranslationStatus.PUBLISHED)
    shown = services.present_question(active_ruleset, spec_q, "ar")
    assert shown["text"] == "سؤال" and shown["lang"] == "ar" and shown["fallback"] is False
    labels = {c["key"]: (c["label"], c["lang"]) for c in shown["choices"]}
    assert labels["work"] == ("عمل", "ar") and labels["study"][1] == "fr"
