"""
Dynamic orientation: telling the platform something new changes what it tells you.

Without this, "profilazione" is a form that stores answers nothing reads, and the orientation is a
photograph taken once. The requirement is that a person who reports a job offer, or uploads the
document a rule asked for, gets an outcome that reflects it — while the previous outcome survives,
because it is evidence of what they were told and acted on.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.utils import timezone

from accounts import roles
from cases import services
from cases.intake import reassess
from cases.models import AssessmentOutcome, CasePurpose, ResponsibleActor
from rules import services as rule_services
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect

pytestmark = pytest.mark.django_db


@pytest.fixture
def person(django_user_model):
    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="reassess@example.test", password="x")
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(email="rule-author@example.test", password="x")


@pytest.fixture
def reviewer(django_user_model):
    return django_user_model.objects.create_user(email="rule-reviewer@example.test", password="x")


@pytest.fixture
def source(db):
    """
    A source somebody has actually opened.

    The date, the name and the URL are not decoration: `SOURCE_VERIFIED` refuses a rule whose
    sources carry a reference and nothing else, and every seeded source was in exactly that state.
    Without them this fixture fails at the first step, for a reason that has nothing to do with
    reassessment.
    """
    return LegalSource.objects.create(
        key="tui-22",
        title_fr="Travail salarié",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )


def _active_rule(author, reviewer, source, *, rule_id="R-OFFER", valid_from=dt.date(2026, 1, 1)):
    """A rule that fires only while the person has NOT declared a job offer, walked to ACTIVE."""
    rule = LegalRule.objects.create(
        rule_id=rule_id,
        version=1,
        pathway="salaried_work",
        condition={"field": "has_job_offer", "op": "is_false"},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.work.offer",
        message_fr="La procédure suppose un employeur identifié en Italie.",
        requirement_fr="Proposition de contrat d’un employeur établi en Italie.",
        responsible_actor=ResponsibleActor.COMPANY,
        valid_from=valid_from,
        created_by=author,
    )
    rule.sources.add(source)
    # The whole chain, not a shortcut to it: DRAFT no longer leads straight to LEGAL_REVIEW.
    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        rule_services.transition(rule, target, actor=reviewer)
    return rule


@pytest.fixture
def rule_in_force(author, reviewer, source):
    """A rule that fires only while the person has NOT declared a job offer."""
    return _active_rule(author, reviewer, source)


@pytest.fixture
def case_with_assessment(person, rule_in_force):
    """A case whose first assessment was taken when the person said they had no job offer."""
    from accounts.services import get_or_create_profile

    profile = get_or_create_profile(person)
    profile.has_job_offer = False
    profile.save()

    case = services.open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    evaluation = rule_services.evaluate(
        {"has_job_offer": False, "pathway": "salaried_work"},
        pathway="salaried_work",
        on_date=timezone.localdate(case.created_at),  # the case's date in Rome, as intake reads it
    )
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.MISSING_REQUIREMENT,
        ruleset_version=1,
        ruleset_snapshot={"orientation": {"questions": [], "rules": [], "outcomes": []}, "legal": evaluation.snapshot},
        answers={"objective": "work"},
        applied_rules=[
            {"rule_id": f.rule_id, "version": f.version, "effect": f.effect, "message": f.message}
            for f in evaluation.findings
        ],
        missing_requirements=[
            {"rule_id": f.rule_id, "requirement": f.requirement, "responsible_actor": f.responsible_actor}
            for f in evaluation.missing
        ],
        sources=list(evaluation.sources),
        pathway_key="salaried_work",
    )
    return case


def test_the_first_assessment_found_the_requirement(case_with_assessment):
    assessment = case_with_assessment.assessments.latest("assessed_at")
    assert assessment.outcome == AssessmentOutcome.MISSING_REQUIREMENT
    assert [applied["rule_id"] for applied in assessment.applied_rules] == ["R-OFFER"]


def test_a_changed_fact_produces_a_new_assessment(case_with_assessment, person):
    person.person_profile.has_job_offer = True
    person.person_profile.save()

    new = reassess(case_with_assessment)
    assert new is not None
    assert new.applied_rules == [], "the rule no longer fires once the offer is declared"


def test_the_previous_assessment_survives(case_with_assessment, person):
    person.person_profile.has_job_offer = True
    person.person_profile.save()
    reassess(case_with_assessment)

    assessments = list(case_with_assessment.assessments.order_by("assessed_at"))
    assert len(assessments) == 2
    assert assessments[0].applied_rules, "the earlier finding is evidence and is kept"


def test_an_unchanged_situation_records_nothing(case_with_assessment):
    """Re-running the same rules against the same facts must not lengthen the record."""
    assert reassess(case_with_assessment) is None
    assert case_with_assessment.assessments.count() == 1


def test_a_reassessment_never_weakens_a_recorded_outcome(case_with_assessment, person):
    """
    An outcome once recorded is not withdrawn by a later run.

    A person told that something was missing has acted on that. If the rules change and the
    requirement disappears, the case must show the NEW finding without quietly rewriting the old
    one into "everything was always fine" — so the recorded outcome only ever moves up.
    """
    person.person_profile.has_job_offer = True
    person.person_profile.save()
    new = reassess(case_with_assessment)
    assert new.outcome == AssessmentOutcome.MISSING_REQUIREMENT
    assert new.applied_rules == []


def test_a_reassessment_reads_the_frozen_answers_not_the_session(case_with_assessment, person):
    """The session is purged on a retention schedule; the reassessment must survive that."""
    from orientation.models import OrientationSession

    OrientationSession.objects.all().delete()
    person.person_profile.has_job_offer = True
    person.person_profile.save()
    new = reassess(case_with_assessment)
    assert new is not None
    assert new.answers == {"objective": "work"}


def test_a_case_with_no_assessment_is_left_alone(person):
    case = services.open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    assert reassess(case) is None
    assert case.assessments.count() == 0


def test_a_new_finding_becomes_a_checklist_line_with_its_source(person, rule_in_force, source):
    from accounts.services import get_or_create_profile

    profile = get_or_create_profile(person)
    profile.has_job_offer = True
    profile.save()

    case = services.open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.POSSIBLE,
        ruleset_version=1,
        ruleset_snapshot={"orientation": {}, "legal": {"format": "ile.legal.ruleset/1", "rules": []}},
        answers={},
        pathway_key="salaried_work",
    )

    profile.has_job_offer = False
    profile.save()
    reassess(case)

    lines = {item.requirement: item for item in case.checklist.all()}
    assert "Proposition de contrat d’un employeur établi en Italie." in lines
    line = lines["Proposition de contrat d’un employeur établi en Italie."]
    assert line.responsible_actor == ResponsibleActor.COMPANY
    assert line.source_ref == source.reference


def test_the_rules_are_those_in_force_on_the_day_the_case_was_opened_in_rome(
    after_midnight_in_rome, person, author, reviewer, source
):
    """
    A case opened at 00:30 in Rome is opened on that day, not on the UTC day before.

    ``created_at`` is held in UTC — 22:30 on 4 October for a case opened at 00:30 on 5 October in
    Rome — and the legal rules applied are those in force on the case's date. Taking the date of the
    UTC value selected the rules of the day before for two hours every night (one in winter): a rule
    entering into force on 5 October did not apply to a case opened at half past midnight that day.
    """
    from accounts.services import get_or_create_profile

    _active_rule(author, reviewer, source, rule_id="R-FROM-5-OCT", valid_from=dt.date(2026, 10, 5))
    profile = get_or_create_profile(person)
    profile.has_job_offer = False
    profile.save()
    case = services.open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    assert case.created_at.date() == dt.date(2026, 10, 4), "held in UTC: the trap this test is about"
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.POSSIBLE,
        ruleset_version=1,
        ruleset_snapshot={"orientation": {}, "legal": {"format": "ile.legal.ruleset/1", "rules": []}},
        answers={},
        pathway_key="salaried_work",
    )

    new = reassess(case)

    assert new is not None, "the rule in force from 5 October applies to a case opened on 5 October"
    assert new.ruleset_snapshot["legal"]["evaluated_on"] == "2026-10-05"
    assert [applied["rule_id"] for applied in new.applied_rules] == ["R-FROM-5-OCT"]
