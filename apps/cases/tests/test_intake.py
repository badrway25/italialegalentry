"""
Completing the orientation questionnaire opens a real case file.

This is the seam that makes the platform a product rather than a questionnaire: Technical Blueprint
§5 puts «Creazione del fascicolo e checklist» in the sequence, and REQ-PER-07 is the requirement.
Everything here exercises the REAL path — the service the wizard calls on completion — not a
hand-built fixture.
"""

from __future__ import annotations

import pytest
from django.contrib.sessions.backends.db import SessionStore

from cases.models import AssessmentOutcome, CaseFile, CasePurpose, CaseStatus, ChecklistStatus, ResponsibleActor
from orientation import services as orientation_services
from orientation.models import Outcome, SessionStatus

pytestmark = pytest.mark.django_db


@pytest.fixture
def person(django_user_model):
    from accounts import roles

    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="intake@example.test", password="x")
    roles.assign_role(user, roles.PERSON)
    return user


def run_questionnaire(person, rf=None):
    """Answer the seeded questionnaire to the end, through the real service."""
    from django.test import RequestFactory

    request = (rf or RequestFactory()).get("/")
    request.user = person
    # A real session object: the orientation service stores a one-time reveal token on it and sets
    # ``modified``, which a plain dict cannot carry.
    request.session = SessionStore()

    session = orientation_services.start_session(request)
    guard = 0
    while session.status != SessionStatus.COMPLETED and guard < 30:
        guard += 1
        step = orientation_services.current_step(session)
        question = getattr(step, "question", None)
        if question is None:
            break
        # ``question`` is an engine QuestionSpec: its choices are a tuple, not a queryset.
        choices = list(question.choices)
        if question.type == "multiple":
            value = [choices[0].key] if choices else []
        elif question.type == "boolean":
            value = True
        else:
            value = choices[0].key if choices else True
        orientation_services.submit_answer(request, session, question.key, value)
        session.refresh_from_db()
    session.refresh_from_db()
    return session


# ---------------------------------------------------------------------------------------------
# The seam
# ---------------------------------------------------------------------------------------------
def test_completing_the_questionnaire_opens_a_case_file(person, seeded):
    session = run_questionnaire(person)
    assert session.status == SessionStatus.COMPLETED

    case = CaseFile.objects.filter(person=person).first()
    assert case is not None, "a completed questionnaire must produce a case file"
    assert case.status == CaseStatus.ORIENTED
    assert case.reference


def test_the_case_carries_the_pathway_the_outcome_names(person, seeded):
    session = run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assert case.pathway_key == session.result.outcome.pathway_key


def test_the_purpose_is_derived_from_the_pathway_never_guessed(person, seeded):
    from cases.intake import purpose_for

    assert purpose_for("work.salaried", "work") == CasePurpose.WORK
    assert purpose_for("study", "study") == CasePurpose.STUDY
    assert purpose_for("family.reunification", "family") == CasePurpose.FAMILY
    # An unknown pathway is OTHER, not a guess at the closest match.
    assert purpose_for("something.new", "unknown") == CasePurpose.OTHER


# ---------------------------------------------------------------------------------------------
# The assessment
# ---------------------------------------------------------------------------------------------
def test_the_assessment_freezes_both_rulesets(person, seeded):
    """
    An outcome now rests on two rulesets, so reproducing it needs both.

    The questionnaire's ruleset says which pathway the answers point to; the legal rules in force on
    the day say what that pathway requires. Freezing only one would leave an assessment that can be
    replayed but not explained, which is the worse half.
    """
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assessment = case.assessments.latest("assessed_at")
    snapshot = assessment.ruleset_snapshot

    orientation = snapshot.get("orientation") or {}
    assert orientation.get("questions"), "the snapshot must carry the questions"
    assert orientation.get("rules"), "the snapshot must carry the rules themselves, not a version"
    assert orientation.get("outcomes")

    legal = snapshot.get("legal") or {}
    assert legal.get("format") == "ile.legal.ruleset/1"
    assert legal.get("evaluated_on"), "a legal snapshot without its date cannot be checked"
    for rule in legal.get("rules", []):
        assert "condition" in rule, "the condition is frozen, not referenced"
        assert rule.get("sources"), "a rule in force carries at least one source"


def test_the_legal_layer_supplies_the_sources_the_questionnaire_cannot(person, seeded):
    """
    The numbered source list is what turns a questionnaire result into an institutional finding.

    Before the rule engine it was empty, honestly so: the orientation ruleset has no citations. Now
    every source comes from a rule in force, and every one names a precise provision rather than the
    name of a law.
    """
    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    if not assessment.applied_rules:
        pytest.skip("no legal rule in force applies to the pathway this questionnaire run reached")
    assert assessment.sources, "an outcome produced by rules in force must show its sources"
    for source in assessment.sources:
        assert source.get("reference"), "a citation without a precise reference cannot be checked"


def test_every_applied_rule_names_its_identifier_and_version(person, seeded):
    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    for applied in assessment.applied_rules:
        assert applied["rule_id"]
        assert applied["version"] >= 1
        assert applied["effect"]


def test_the_outcome_is_reproducible_from_its_snapshot(person, seeded):
    """
    Replaying is only evidence if the replay is compared with what was recorded.

    A reproduction that silently differs is worse than none, because it looks like verification — so
    the assertion is on ``matches``, not on the replay merely returning something.
    """
    from cases.services import reproduce

    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    replayed = reproduce(assessment)
    assert replayed.orientation is not None
    assert replayed.matches, f"replay gave {replayed.outcome}, the case recorded {replayed.recorded}"


def test_the_replay_reads_the_snapshot_and_not_the_database(person, seeded):
    """The rules can all be retired and the assessment still explains itself."""
    from cases.services import reproduce
    from rules.models import LegalRule, LegalSource

    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    before = reproduce(assessment).outcome

    LegalRule.objects.all().delete()
    LegalSource.objects.all().delete()

    assert reproduce(assessment).outcome == before


def test_the_assessment_records_the_answers_and_the_rationale(person, seeded):
    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    assert assessment.answers, "the answers are part of what makes the outcome reproducible"
    assert assessment.rationale, "an outcome without a rationale is an oracle"


def test_the_questionnaire_alone_never_claims_more_than_possible(person, seeded):
    """
    The questionnaire has no sources and no validity dates, so it cannot justify a STOP or a
    WARNING on its own. Those belong to the legal rule engine, which has both.

    This is asserted against the questionnaire's OWN contribution rather than against the recorded
    outcome, because the recorded outcome is now the stronger of two answers — and the assertion
    that matters is that the strength came from somewhere that can cite a provision.
    """
    from cases.intake import outcome_for

    session = run_questionnaire(person)
    assert outcome_for(session.result.outcome.key) in {
        AssessmentOutcome.POSSIBLE,
        AssessmentOutcome.REVIEW_REQUIRED,
    }


def test_an_outcome_stronger_than_possible_can_say_which_rule_made_it_so(person, seeded):
    """No finding, no escalation. An outcome nobody can trace back to a rule is an oracle."""
    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    if assessment.outcome in {AssessmentOutcome.POSSIBLE, AssessmentOutcome.REVIEW_REQUIRED}:
        pytest.skip("this run did not reach an outcome stronger than the questionnaire's own")
    assert assessment.applied_rules, "a stronger outcome must name the rules that produced it"
    assert assessment.sources, "and those rules must carry their sources"


def test_the_recorded_outcome_is_the_stronger_of_the_two_layers(person, seeded):
    from cases.intake import EFFECT_TO_OUTCOME, OUTCOME_RANK, outcome_for

    session = run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")
    from_questionnaire = outcome_for(session.result.outcome.key)
    strongest_rule = max(
        (EFFECT_TO_OUTCOME[applied["effect"]] for applied in assessment.applied_rules),
        key=lambda value: OUTCOME_RANK[value],
        default=AssessmentOutcome.POSSIBLE,
    )
    expected = max((from_questionnaire, strongest_rule), key=lambda value: OUTCOME_RANK[value])
    assert assessment.outcome == expected


def test_a_legal_requirement_becomes_a_checklist_line_carrying_its_source(person, seeded):
    """
    A requirement a rule found missing must reach the person as something they can act on, with the
    provision behind it — not as an instruction with no author.
    """
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assessment = case.assessments.latest("assessed_at")
    if not assessment.missing_requirements:
        pytest.skip("no rule in force found a missing requirement for this pathway")
    requirements = {item.requirement for item in case.checklist.all()}
    for missing in assessment.missing_requirements:
        assert missing["requirement"] in requirements
    cited = [item for item in case.checklist.all() if item.source_ref]
    assert cited, "at least one checklist line must carry the reference of the rule behind it"


# ---------------------------------------------------------------------------------------------
# The checklist
# ---------------------------------------------------------------------------------------------
def test_the_outcome_checklist_becomes_the_case_checklist(person, seeded):
    session = run_questionnaire(person)
    outcome = session.result.outcome
    expected = {item.text_fr.strip() for item in outcome.checklist_items.all() if item.text_fr.strip()}
    if not expected:
        pytest.skip("the seeded outcome carries no checklist items")
    case = CaseFile.objects.get(person=person)
    assert {item.requirement for item in case.checklist.all()} >= expected


def test_every_checklist_item_names_a_responsible_actor(person, seeded):
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    items = list(case.checklist.all())
    if not items:
        pytest.skip("the seeded outcome carries no checklist items")
    assert all(item.responsible_actor for item in items)


def test_an_authority_step_is_not_shown_as_the_person_s_task(person, seeded):
    """
    A document the consulate must issue is not a task the applicant can perform, and showing it as
    one would waste their time and misplace the responsibility.
    """
    from cases.intake import RESPONSIBLE_BY_CATEGORY

    assert RESPONSIBLE_BY_CATEGORY["authorities"] == ResponsibleActor.AUTHORITY
    assert RESPONSIBLE_BY_CATEGORY["documents"] == ResponsibleActor.PERSON


# ---------------------------------------------------------------------------------------------
# Retaking the questionnaire
# ---------------------------------------------------------------------------------------------
def test_retaking_the_questionnaire_updates_the_case_rather_than_opening_a_second(person, seeded):
    run_questionnaire(person)
    run_questionnaire(person)
    assert CaseFile.objects.filter(person=person).count() == 1, "two open files for one objective is ambiguous"


def test_retaking_the_questionnaire_records_a_second_assessment(person, seeded):
    run_questionnaire(person)
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assert case.assessments.count() == 2, "each evaluation is kept: the history is the evidence"


def test_completed_work_survives_retaking_the_questionnaire(person, seeded):
    from cases import services

    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    item = case.checklist.first()
    if item is None:
        pytest.skip("the seeded outcome carries no checklist items")
    services.set_checklist_status(item, ChecklistStatus.DONE)

    run_questionnaire(person)
    item.refresh_from_db()
    assert item.status == ChecklistStatus.DONE, "a person must not find their completed work undone"


# ---------------------------------------------------------------------------------------------
# Anonymous sessions
# ---------------------------------------------------------------------------------------------
def test_an_anonymous_session_opens_no_case(seeded):
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore()
    session = orientation_services.start_session(request)
    guard = 0
    while session.status != SessionStatus.COMPLETED and guard < 30:
        guard += 1
        step = orientation_services.current_step(session)
        question = getattr(step, "question", None)
        if question is None:
            break
        # ``question`` is an engine QuestionSpec: its choices are a tuple, not a queryset.
        choices = list(question.choices)
        if question.type == "multiple":
            value = [choices[0].key] if choices else []
        elif question.type == "boolean":
            value = True
        else:
            value = choices[0].key if choices else True
        orientation_services.submit_answer(request, session, question.key, value)
        session.refresh_from_db()
    assert CaseFile.objects.count() == 0


# ---------------------------------------------------------------------------------------------
# Resilience
# ---------------------------------------------------------------------------------------------
def test_a_failure_opening_the_case_never_loses_the_result(person, seeded, monkeypatch, caplog):
    """
    The session and its result are saved before the case is opened. A downstream failure is an
    incident to investigate, never a reason to throw away the answer a person just earned.
    """
    import cases.intake as intake

    monkeypatch.setattr(intake, "open_case_from_session", lambda *a, **k: 1 / 0)
    session = run_questionnaire(person)
    session.refresh_from_db()
    assert session.status == SessionStatus.COMPLETED
    assert session.result is not None
    assert CaseFile.objects.count() == 0
    assert person.email not in caplog.text, "no personal data in the log"


def test_the_outcome_model_is_unchanged_by_intake(person, seeded):
    """Intake reads the orientation ruleset; it must never write to it."""
    before = list(Outcome.objects.values_list("key", "pathway_key").order_by("key"))
    run_questionnaire(person)
    assert list(Outcome.objects.values_list("key", "pathway_key").order_by("key")) == before
