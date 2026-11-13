"""
Model invariants — the rules that must hold whatever calls the ORM.

A service can be bypassed by a management command, a data migration or a future API. What is
enforced here is enforced by the database or by ``full_clean``, so it holds anyway.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from academy.models import (
    CompetenceLevel,
    Course,
    CourseModule,
    Enrolment,
    ModuleAttendance,
    PlanOrigin,
    SkillGapLine,
    TrainingPlan,
)

pytestmark = pytest.mark.django_db


def test_one_enrolment_per_person_and_course(person, course):
    Enrolment.objects.create(person=person, course=course)
    with pytest.raises(IntegrityError), transaction.atomic():
        Enrolment.objects.create(person=person, course=course)


def test_one_attendance_per_module(person, course):
    enrolment = Enrolment.objects.create(person=person, course=course)
    module = course.modules.first()
    ModuleAttendance.objects.create(enrolment=enrolment, module=module)
    with pytest.raises(IntegrityError), transaction.atomic():
        ModuleAttendance.objects.create(enrolment=enrolment, module=module)


def test_module_order_is_unique_inside_a_course(course):
    with pytest.raises(IntegrityError), transaction.atomic():
        CourseModule.objects.create(course=course, order=1, title="Doublon")


def test_attendance_refuses_a_module_from_another_course(person, course, course_factory, provider):
    other = course_factory(provider, slug="autre", title="Autre")
    enrolment = Enrolment.objects.create(person=person, course=course)
    attendance = ModuleAttendance(enrolment=enrolment, module=other.modules.first())
    with pytest.raises(ValidationError):
        attendance.full_clean()


def test_a_company_need_plan_without_a_reference_is_invalid(person):
    plan = TrainingPlan(person=person, title="Sans référence", origin=PlanOrigin.COMPANY_NEED)
    with pytest.raises(ValidationError) as excinfo:
        plan.full_clean()
    assert "origin_reference" in excinfo.value.message_dict


@pytest.mark.parametrize(
    ("required", "current", "expected"),
    [
        (CompetenceLevel.INTERMEDIATE, CompetenceLevel.NONE, "missing"),
        (CompetenceLevel.INTERMEDIATE, CompetenceLevel.BASIC, "partial"),
        (CompetenceLevel.BASIC, CompetenceLevel.BASIC, "covered"),
        (CompetenceLevel.BASIC, CompetenceLevel.ADVANCED, "covered"),
    ],
)
def test_the_gap_is_derived_and_named(person, competence, required, current, expected):
    plan = TrainingPlan.objects.create(person=person, title="Plan")
    line = SkillGapLine(plan=plan, competence=competence, required_level=required, current_level=current)
    assert line.gap_key == expected
    assert "%" not in str(line.gap_label)


def test_a_gap_line_refuses_a_module_outside_its_course(person, competence, course, course_factory, provider):
    other = course_factory(provider, slug="ailleurs", title="Ailleurs")
    plan = TrainingPlan.objects.create(person=person, title="Plan")
    line = SkillGapLine(
        plan=plan,
        competence=competence,
        required_level=CompetenceLevel.BASIC,
        course=course,
        module=other.modules.first(),
    )
    with pytest.raises(ValidationError):
        line.full_clean()


def test_a_course_reference_is_never_sequential(person, course, course_factory, provider):
    """
    Two completions, two unrelated references.

    A sequential reference would tell anybody holding one how many people had attended — the same
    reasoning the case file applies to its own reference.
    """
    from academy import services

    second = course_factory(provider, slug="second", title="Second")
    references = []
    for target in (course, second):
        enrolment = services.enrol(person, target)
        for module in target.modules.all():
            services.record_attendance(enrolment, module)
        enrolment.refresh_from_db()
        references.append(enrolment.attendance_reference)
    assert len(set(references)) == 2
    assert not references[1].startswith(references[0][:6])


def test_the_enrolment_freezes_the_course_version(person, course):
    from academy import services

    course.version = 3
    course.save(update_fields=["version"])
    enrolment = services.enrol(person, course)
    Course.objects.filter(pk=course.pk).update(version=4)
    enrolment.refresh_from_db()
    assert enrolment.course_version == 3
