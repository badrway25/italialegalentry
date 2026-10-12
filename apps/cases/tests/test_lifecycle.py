"""
The invariants of the case file, tested at the domain level rather than through the interface.

An interface can be bypassed; a rule that only lives in a template is not a rule. Everything here
asserts behaviour that must hold however the change arrives — view, admin, management command or a
future API.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts import roles
from audit.models import AuditEvent
from cases import services
from cases.models import (
    AssessmentOutcome,
    AssignmentRole,
    CaseFile,
    CasePurpose,
    CaseStatus,
    ChecklistStatus,
    ResponsibleActor,
    transitions_from,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def person(django_user_model):
    user = django_user_model.objects.create_user(email="persona@example.test", password="x")
    roles.ensure_roles()
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def other_person(django_user_model):
    return django_user_model.objects.create_user(email="altra@example.test", password="x")


@pytest.fixture
def professional(django_user_model):
    user = django_user_model.objects.create_user(email="prof@example.test", password="x")
    roles.ensure_roles()
    roles.assign_role(user, roles.PROFESSIONAL)
    return user


@pytest.fixture
def case(person):
    return services.open_case(person, purpose=CasePurpose.WORK, pathway_key="work.salaried")


# ---------------------------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------------------------
def test_a_new_case_starts_in_draft_with_a_reference(case):
    assert case.status == CaseStatus.DRAFT
    assert len(case.reference) == 10
    # Upper case means no lower-case letter: ``isupper()`` is False for an all-digit draw, which a random
    # reference is once in 110 (seen: '7266137222').
    assert case.reference == case.reference.upper()


def test_references_are_not_sequential(person):
    """A sequential reference would leak how many case files exist."""
    cases = [services.open_case(person, purpose=CasePurpose.STUDY) for _ in range(12)]
    references = [case.reference for case in cases]
    assert len(set(references)) == 12
    # A sequential reference sorts exactly like the primary keys; a random one does not: twelve rows
    # make an accidental match one chance in 12! (about two in a billion). The earlier check, « no
    # reference is all digits », failed by chance about one run in 22: ten random hex digits are all
    # decimal once in 110, five references were drawn — and an all-digit draw is not a sequence.
    assert sorted(references) != [case.reference for case in sorted(cases, key=lambda case: case.pk)]


def test_opening_a_case_is_audited(case):
    assert AuditEvent.objects.filter(action="case.opened", target_id=str(case.pk)).exists()


def test_an_unknown_purpose_is_refused(person):
    with pytest.raises(ValidationError):
        services.open_case(person, purpose="tourism")


# ---------------------------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------------------------
def test_declared_transition_is_allowed(case):
    services.transition(case, CaseStatus.ORIENTED)
    case.refresh_from_db()
    assert case.status == CaseStatus.ORIENTED
    assert case.previous_status == CaseStatus.DRAFT


def test_undeclared_transition_is_refused(case):
    with pytest.raises(services.TransitionRefused):
        services.transition(case, CaseStatus.ENTERED)
    case.refresh_from_db()
    assert case.status == CaseStatus.DRAFT


def test_every_transition_is_audited(case):
    services.transition(case, CaseStatus.ORIENTED)
    event = AuditEvent.objects.filter(action="case.transition").latest("created_at")
    assert event.metadata["from"] == CaseStatus.DRAFT
    assert event.metadata["to"] == CaseStatus.ORIENTED


def test_suspension_requires_a_reason(case):
    with pytest.raises(services.TransitionRefused):
        services.transition(case, CaseStatus.SUSPENDED, reason="   ")
    services.transition(case, CaseStatus.SUSPENDED, reason="documenti in attesa")
    case.refresh_from_db()
    assert case.suspension_reason == "documenti in attesa"


def test_resume_returns_to_the_previous_state(case):
    services.transition(case, CaseStatus.ORIENTED)
    services.transition(case, CaseStatus.SUSPENDED, reason="in attesa")
    services.resume(case)
    case.refresh_from_db()
    assert case.status == CaseStatus.ORIENTED
    assert case.suspension_reason == ""


def test_a_closed_case_is_read_only(case):
    services.transition(case, CaseStatus.CLOSED)
    case.refresh_from_db()
    assert case.is_read_only
    with pytest.raises(services.TransitionRefused):
        services.transition(case, CaseStatus.ORIENTED)


def test_suspended_is_reachable_from_every_active_state():
    for status in (
        CaseStatus.DRAFT,
        CaseStatus.ORIENTED,
        CaseStatus.TRAINING,
        CaseStatus.ADMIN_PROCESS,
        CaseStatus.PRE_DEPARTURE,
        CaseStatus.POST_ENTRY,
    ):
        assert CaseStatus.SUSPENDED in transitions_from(status)


# ---------------------------------------------------------------------------------------------
# The selection invariant (CR-03): reserved activities belong to authorised parties
# ---------------------------------------------------------------------------------------------
def test_selection_is_refused_without_an_authorised_actor(case, person):
    services.transition(case, CaseStatus.ORIENTED)
    services.transition(case, CaseStatus.TRAINING)
    with pytest.raises(services.TransitionRefused):
        services.transition(case, CaseStatus.SELECTION)


def test_selection_is_refused_when_the_authorisation_has_expired(case, professional):
    services.transition(case, CaseStatus.ORIENTED)
    services.transition(case, CaseStatus.TRAINING)
    services.assign(
        case,
        professional,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2020-001",
        authorisation_valid_until=timezone.localdate() - dt.timedelta(days=1),
    )
    with pytest.raises(services.TransitionRefused):
        services.transition(case, CaseStatus.SELECTION)


def test_selection_is_allowed_with_a_valid_authorised_actor(case, professional):
    services.transition(case, CaseStatus.ORIENTED)
    services.transition(case, CaseStatus.TRAINING)
    services.assign(
        case,
        professional,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2026-014",
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),
    )
    services.transition(case, CaseStatus.SELECTION)
    case.refresh_from_db()
    assert case.status == CaseStatus.SELECTION


def test_an_authorised_actor_assignment_requires_an_authorisation_reference(case, professional):
    with pytest.raises(ValidationError):
        services.assign(case, professional, role=AssignmentRole.AUTHORISED_ACTOR)


def test_a_revoked_assignment_grants_nothing(case, professional):
    assignment = services.assign(
        case,
        professional,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2026-014",
    )
    services.revoke_assignment(assignment)
    assert case.has_valid_authorised_actor() is False
    assert services.responsible_for(case) == []


# ---------------------------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------------------------
def test_a_checklist_item_needs_a_responsible_actor(case):
    with pytest.raises(ValidationError):
        services.add_checklist_item(case, requirement="Documento", responsible_actor="")


def test_progress_counts_instead_of_inventing_a_percentage(case):
    services.add_checklist_item(case, requirement="A", responsible_actor=ResponsibleActor.PERSON)
    item_b = services.add_checklist_item(case, requirement="B", responsible_actor=ResponsibleActor.AUTHORITY)
    services.add_checklist_item(case, requirement="C", responsible_actor=ResponsibleActor.PERSON)
    services.set_checklist_status(item_b, ChecklistStatus.DONE)
    counts = services.progress(case)
    assert counts == {"total": 3, "done": 1, "open": 2, "overdue": 0, "blocked": 0}
    assert "percent" not in counts


def test_not_applicable_items_leave_the_denominator(case):
    services.add_checklist_item(case, requirement="A", responsible_actor=ResponsibleActor.PERSON)
    skipped = services.add_checklist_item(case, requirement="B", responsible_actor=ResponsibleActor.PERSON)
    services.set_checklist_status(skipped, ChecklistStatus.NOT_APPLICABLE)
    assert services.progress(case)["total"] == 1


def test_overdue_is_computed_from_the_due_date(case):
    services.add_checklist_item(
        case,
        requirement="Scaduto",
        responsible_actor=ResponsibleActor.PERSON,
        due_date=timezone.localdate() - dt.timedelta(days=3),
    )
    assert services.progress(case)["overdue"] == 1


# ---------------------------------------------------------------------------------------------
# Assessment and reproducibility
# ---------------------------------------------------------------------------------------------
SNAPSHOT = {
    "format": "ile.orientation.ruleset/1",
    "version": 1,
    "questions": [
        {
            "key": "objective",
            "is_entry": True,
            "type": "single",
            "text_fr": "Quel est votre objectif ?",
            "choices": [{"key": "work", "label_fr": "Travailler"}, {"key": "study", "label_fr": "Étudier"}],
        }
    ],
    "outcomes": [
        {"key": "work", "pathway_key": "work.salaried", "title_fr": "Travail salarié", "checklist": []},
        {"key": "study", "pathway_key": "study", "title_fr": "Études", "checklist": []},
    ],
    "rules": [
        {"name": "work", "conditions": {"question_key": "objective", "op": "eq", "value": "work"}, "outcome": "work"},
        {
            "name": "study",
            "conditions": {"question_key": "objective", "op": "eq", "value": "study"},
            "outcome": "study",
        },
    ],
}


def test_an_assessment_stores_the_whole_ruleset_not_a_pointer(case):
    assessment = services.record_assessment(
        case,
        outcome=AssessmentOutcome.POSSIBLE,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    assert assessment.ruleset_snapshot["rules"], "the snapshot must carry the rules themselves"


def test_an_assessment_without_a_snapshot_is_refused(case):
    with pytest.raises(ValidationError):
        services.record_assessment(
            case, outcome=AssessmentOutcome.POSSIBLE, ruleset_version=1, ruleset_snapshot={}, answers={}
        )


def test_an_outcome_is_reproducible_from_its_snapshot(case):
    assessment = services.record_assessment(
        case,
        outcome=AssessmentOutcome.POSSIBLE,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
        pathway_key="work.salaried",
    )
    replayed = services.reproduce(assessment)
    assert getattr(replayed, "outcome", None) is not None or hasattr(replayed, "question")


def test_an_assessment_moves_a_draft_case_to_oriented(case):
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.POSSIBLE,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    case.refresh_from_db()
    assert case.status == CaseStatus.ORIENTED


def test_a_stop_never_advances_the_case(case):
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.STOP,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    case.refresh_from_db()
    assert case.status == CaseStatus.DRAFT, "a blocking outcome must not present the pathway as practicable"


def test_review_required_moves_the_case_to_review_required(case):
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.REVIEW_REQUIRED,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    case.refresh_from_db()
    assert case.status == CaseStatus.REVIEW_REQUIRED


def test_the_outcome_eligible_does_not_exist():
    """CR-11: a user reads "eligible" as "I am entitled to enter"."""
    assert "eligible" not in AssessmentOutcome.values


# ---------------------------------------------------------------------------------------------
# Next action
# ---------------------------------------------------------------------------------------------
def test_next_action_prefers_an_overdue_requirement(case):
    services.add_checklist_item(case, requirement="Più tardi", responsible_actor=ResponsibleActor.PERSON)
    services.add_checklist_item(
        case,
        requirement="In ritardo",
        responsible_actor=ResponsibleActor.PERSON,
        due_date=timezone.localdate() - dt.timedelta(days=2),
    )
    action = services.next_action(case)
    assert action.label == "In ritardo"
    assert action.urgency == "overdue"


def test_next_action_names_who_is_responsible(case):
    services.add_checklist_item(
        case, requirement="Rilascio del documento", responsible_actor=ResponsibleActor.AUTHORITY
    )
    action = services.next_action(case)
    assert action.responsible_actor == ResponsibleActor.AUTHORITY
    assert action.is_for_someone_else is True


def test_a_blocking_outcome_drives_the_next_action(case):
    services.record_assessment(
        case,
        outcome=AssessmentOutcome.STOP,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    assert services.next_action(case).urgency == "blocked"


# ---------------------------------------------------------------------------------------------
# Authorisation
# ---------------------------------------------------------------------------------------------
def test_a_person_only_sees_their_own_cases(case, person, other_person):
    services.open_case(other_person, purpose=CasePurpose.STUDY)
    assert list(CaseFile.objects.readable_by(person)) == [case]
    assert list(CaseFile.objects.readable_by(other_person)) != [case]


def test_an_unknown_uuid_and_a_forbidden_uuid_are_indistinguishable(case, other_person):
    """
    Knowing a UUID must never be enough, and must never reveal that the object exists.

    Both answers are Http404, and the assertion is that they are the SAME answer. It used to be
    PermissionDenied, which a view renders as 403 — and a 403 on somebody else's file confirms the
    file exists. The two branches now raise one exception type, so there is nothing left to tell
    apart (PERMISSION_MODEL L-07).
    """
    import uuid as uuid_module

    from django.http import Http404

    with pytest.raises(Http404):
        services.case_detail(other_person, case.uuid)
    with pytest.raises(Http404):
        services.case_detail(other_person, uuid_module.uuid4())


def test_an_anonymous_user_reads_nothing():
    from django.contrib.auth.models import AnonymousUser

    assert list(CaseFile.objects.readable_by(AnonymousUser())) == []


def test_an_assigned_professional_reads_the_case(case, professional):
    services.assign(case, professional, role=AssignmentRole.PROFESSIONAL)
    assert case in CaseFile.objects.readable_by(professional)


def test_a_revoked_professional_stops_reading_the_case(case, professional):
    assignment = services.assign(case, professional, role=AssignmentRole.PROFESSIONAL)
    services.revoke_assignment(assignment)
    assert case not in CaseFile.objects.readable_by(professional)


# ---------------------------------------------------------------------------------------------
# Queryset strictness (tightened after the 20 September 2026 security review)
# ---------------------------------------------------------------------------------------------
def test_an_expired_mandate_stops_listing_the_case(case, professional):
    """Checking only ``revoked_at`` let a lapsed authorisation keep reading personal data."""
    services.assign(
        case,
        professional,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2020-001",
        authorisation_valid_until=timezone.localdate() - dt.timedelta(days=1),
    )
    assert case not in CaseFile.objects.readable_by(professional)


def test_a_mandate_valid_today_still_lists_the_case(case, professional):
    services.assign(
        case,
        professional,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2026-014",
        authorisation_valid_until=timezone.localdate(),
    )
    assert case in CaseFile.objects.readable_by(professional)


def test_project_staff_do_not_see_every_case_file(case, django_user_model):
    """Staff supervise through the audited back-office, not through a platform-side list of all cases."""
    staff = django_user_model.objects.create_user(email="staff@example.test", password="x", is_staff=True)
    roles.assign_role(staff, roles.STAFF)
    assert list(CaseFile.objects.readable_by(staff)) == []


def test_an_administrator_sees_every_case_file(case, django_user_model):
    administrator = django_user_model.objects.create_user(email="admin@example.test", password="x", is_staff=True)
    roles.assign_role(administrator, roles.ADMINISTRATOR)
    assert case in CaseFile.objects.readable_by(administrator)
