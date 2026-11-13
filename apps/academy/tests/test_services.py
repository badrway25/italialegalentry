"""
Domain services: enrolment, attendance, completion, interruption, plans.

What these tests protect, beyond "it works":

* a completion is DERIVED from attendance and can be produced no other way;
* progress is a count, never a percentage;
* every state change leaves an audit row, with no personal data in it;
* a draft course is not enrollable, and asking twice does not create two enrolments.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from academy import services
from academy.models import (
    CompetenceLevel,
    Enrolment,
    EnrolmentOrigin,
    EnrolmentStatus,
    ModuleAttendance,
    PlanOrigin,
    PlanStatus,
    TrainingPlan,
)
from audit.models import AuditEvent

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# Enrolment
# ---------------------------------------------------------------------------------------------
def test_enrolling_twice_returns_the_same_enrolment(person, course):
    first = services.enrol(person, course)
    second = services.enrol(person, course)
    assert first.pk == second.pk
    assert Enrolment.objects.filter(person=person, course=course).count() == 1


def test_a_draft_course_is_not_enrollable(person, draft_course):
    with pytest.raises(services.EnrolmentRefused):
        services.enrol(person, draft_course)


def test_a_plan_belonging_to_someone_else_cannot_be_attached(person, other_person, course):
    plan = services.create_plan(other_person, title="Parcours d’un tiers")
    with pytest.raises(PermissionDenied):
        services.enrol(person, course, plan=plan)


def test_an_enrolment_from_a_plan_records_where_it_came_from(person, course):
    plan = services.create_plan(person, title="Mon parcours")
    enrolment = services.enrol(person, course, plan=plan)
    assert enrolment.origin == EnrolmentOrigin.PLAN
    assert enrolment.plan_id == plan.pk


def test_enrolment_is_audited_without_personal_data(person, course):
    services.enrol(person, course)
    event = AuditEvent.objects.filter(action="academy.enrolled").latest("created_at")
    assert event.actor_id == person.id
    assert event.metadata["course"] == course.slug
    assert "email" not in event.metadata
    assert person.email not in str(event.metadata)


# ---------------------------------------------------------------------------------------------
# Attendance and completion
# ---------------------------------------------------------------------------------------------
def test_attending_a_module_moves_the_enrolment_to_in_progress(person, course):
    enrolment = services.enrol(person, course)
    module = course.modules.first()
    services.record_attendance(enrolment, module)
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.IN_PROGRESS
    assert enrolment.started_at is not None


def test_attending_the_same_module_twice_records_one_fact(person, course):
    enrolment = services.enrol(person, course)
    module = course.modules.first()
    services.record_attendance(enrolment, module)
    services.record_attendance(enrolment, module)
    assert ModuleAttendance.objects.filter(enrolment=enrolment, module=module).count() == 1


def test_a_module_of_another_course_is_refused(person, course, course_factory, provider):
    other = course_factory(provider, slug="autre-cours", title="Autre cours")
    enrolment = services.enrol(person, course)
    with pytest.raises(Exception) as excinfo:
        services.record_attendance(enrolment, other.modules.first())
    assert "module" in str(excinfo.value)


def test_completion_is_derived_from_attendance_and_carries_a_reference(person, course):
    enrolment = services.enrol(person, course)
    for module in course.modules.all():
        services.record_attendance(enrolment, module)
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.COMPLETED
    assert enrolment.completed_at is not None
    assert len(enrolment.attendance_reference) == 10
    assert AuditEvent.objects.filter(action="academy.completed").exists()


def test_progress_is_counted_never_measured(person, course):
    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    counts = services.progress(enrolment)
    assert counts == {"total": 3, "attended": 1, "remaining": 2, "minutes": 60}
    assert not any(key in counts for key in ("percent", "percentage", "ratio", "score", "rate"))


def test_next_module_is_the_first_one_not_attended(person, course):
    enrolment = services.enrol(person, course)
    modules = list(course.modules.all())
    assert services.next_module(enrolment).pk == modules[0].pk
    services.record_attendance(enrolment, modules[0])
    assert services.next_module(enrolment).pk == modules[1].pk


# ---------------------------------------------------------------------------------------------
# Interrupting and resuming
# ---------------------------------------------------------------------------------------------
def test_withdrawing_keeps_the_attendance_already_recorded(person, course):
    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    services.withdraw(enrolment)
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.WITHDRAWN
    assert enrolment.attendances.count() == 1

    services.resume(enrolment)
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.IN_PROGRESS
    assert enrolment.withdrawn_at is None


def test_a_completed_training_cannot_be_withdrawn(person, course):
    enrolment = services.enrol(person, course)
    for module in course.modules.all():
        services.record_attendance(enrolment, module)
    enrolment.refresh_from_db()
    with pytest.raises(services.EnrolmentRefused):
        services.withdraw(enrolment)


def test_enrolling_again_after_an_interruption_resumes_it(person, course):
    enrolment = services.enrol(person, course)
    services.withdraw(enrolment)
    again = services.enrol(person, course)
    assert again.pk == enrolment.pk
    assert again.status == EnrolmentStatus.ENROLLED


# ---------------------------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------------------------
def test_the_catalogue_hides_drafts_from_a_person_and_shows_them_to_administration(
    person, admin_user, course, draft_course
):
    visible = {row.slug for row in services.catalogue(person)}
    assert visible == {course.slug}
    assert draft_course.slug in {row.slug for row in services.catalogue(admin_user)}


def test_an_unknown_filter_value_is_ignored_rather_than_widening_the_result(person, course):
    rows = services.catalogue(person, course_type="n’importe quoi")
    assert list(rows) == [course]


def test_an_anonymous_caller_sees_nothing(course):
    from django.contrib.auth.models import AnonymousUser

    assert list(services.catalogue(AnonymousUser())) == []


# ---------------------------------------------------------------------------------------------
# Training plans
# ---------------------------------------------------------------------------------------------
def test_a_company_need_plan_must_cite_its_reference(person):
    from django.core.exceptions import ValidationError

    with pytest.raises(ValidationError):
        services.create_plan(person, title="Sans référence", origin=PlanOrigin.COMPANY_NEED)

    plan = services.create_plan(
        person,
        title="Avec référence",
        origin=PlanOrigin.COMPANY_NEED,
        origin_reference="FB-2026-014 (exemple)",
    )
    assert plan.status == PlanStatus.ACTIVE


def test_the_skill_gap_is_a_comparison_with_a_word_for_the_gap(person, course, competence):
    plan = services.create_plan(person, title="Parcours conseillé")
    services.add_plan_item(plan, course, rationale="Cœur du besoin", expected_outcome="Comprendre une consigne")
    missing = services.add_gap_line(
        plan,
        competence,
        required_level=CompetenceLevel.INTERMEDIATE,
        current_level=CompetenceLevel.NONE,
        course=course,
        expected_outcome="Comprendre une consigne simple.",
        source_note="Besoin territorial (exemple)",
    )
    assert missing.gap_key == "missing"

    rows = services.plan_rows(plan)
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == {
        "competence",
        "required",
        "current",
        "gap_key",
        "gap",
        "course",
        "module",
        "expected_outcome",
        "source_note",
    }
    assert "%" not in str(row["gap"])


def test_a_plan_item_is_a_recommendation_not_a_condition(person, course):
    """
    A course in a plan and a course in the catalogue are enrolled the same way.

    The plan is consulted nowhere in ``enrol``; this test enrols in a course the plan recommends
    WITHOUT naming the plan, and the enrolment succeeds exactly as any other.
    """
    plan = services.create_plan(person, title="Parcours conseillé")
    services.add_plan_item(plan, course)
    enrolment = services.enrol(person, course)
    assert enrolment.plan is None
    assert enrolment.origin == EnrolmentOrigin.CATALOGUE


def test_summary_counts_what_the_person_has(person, course, course_factory, provider):
    second = course_factory(provider, slug="second-cours", title="Second cours")
    first_enrolment = services.enrol(person, course)
    services.enrol(person, second)
    for module in course.modules.all():
        services.record_attendance(first_enrolment, module)
    services.create_plan(person, title="Un plan")

    summary = services.summary(person)
    assert summary == {"ongoing": 1, "completed": 1, "plans": 1}


def test_a_plan_can_be_attached_to_a_case_file_without_gating_anything(person, course):
    from cases import services as case_services
    from cases.models import CasePurpose

    case = case_services.open_case(person, purpose=CasePurpose.TRAINING)
    plan = services.create_plan(
        person,
        title="Parcours issu de l’orientation",
        origin=PlanOrigin.ORIENTATION,
        case=case,
    )
    assert plan.case_id == case.pk
    # And the enrolment still needs nothing from that case.
    assert services.enrol(person, course).pk is not None


def test_plan_readable_by_an_assigned_professional_only_while_the_mandate_lives(person, professional, course):
    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    case = case_services.open_case(person, purpose=CasePurpose.TRAINING)
    plan = services.create_plan(person, title="Parcours suivi par un professionnel", case=case)
    assignment = case_services.assign(
        case,
        professional,
        role=AssignmentRole.PROFESSIONAL,
        # A live mandate: a year from today in Rome, not a fixed date (2099 was a fuse: red from 2 Jan 2099).
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),
    )
    assert plan in TrainingPlan.objects.readable_by(professional)

    case_services.revoke_assignment(assignment)
    assert plan not in TrainingPlan.objects.readable_by(professional)


def test_a_professional_never_sees_the_attendance_of_the_person_they_follow(person, professional, course):
    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    case = case_services.open_case(person, purpose=CasePurpose.TRAINING)
    case_services.assign(case, professional, role=AssignmentRole.PROFESSIONAL)
    services.enrol(person, course)
    assert list(Enrolment.objects.readable_by(professional)) == []


def test_composing_a_plan_is_audited_without_personal_data(person, professional, course, competence):
    """
    A plan is usually written by somebody else. Every line added to it is a state change on a
    person's record and leaves a trace, naming the course and the competence by CODE only.
    """
    plan = services.create_plan(person, title="Parcours accompagné", created_by=professional)
    services.add_plan_item(plan, course, rationale="Cœur du besoin")
    services.add_gap_line(
        plan,
        competence,
        required_level=CompetenceLevel.INTERMEDIATE,
        current_level=CompetenceLevel.NONE,
        course=course,
    )

    added = AuditEvent.objects.filter(action="academy.plan.course_added").latest("created_at")
    gap = AuditEvent.objects.filter(action="academy.plan.gap_line_added").latest("created_at")
    assert added.actor_id == professional.id
    assert added.metadata["course"] == course.slug
    assert gap.metadata["competence"] == competence.code
    assert gap.metadata["gap"] == "missing"
    for event in (added, gap):
        assert person.email not in str(event.metadata)
        assert professional.email not in str(event.metadata)


def test_adding_the_same_course_twice_leaves_one_audit_row(person, course):
    plan = services.create_plan(person, title="Parcours")
    services.add_plan_item(plan, course)
    services.add_plan_item(plan, course)
    assert AuditEvent.objects.filter(action="academy.plan.course_added").count() == 1
