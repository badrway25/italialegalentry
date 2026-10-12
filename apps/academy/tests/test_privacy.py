"""
The two duties an app holding personal data owes the person it belongs to.

A training record says what a named individual is learning and when they attended. That makes the
Academy answerable for GDPR art. 15 (the record appears in the person's data export) and art. 17
(it disappears when the account is anonymised). Both are wired from ``AcademyConfig.ready`` by
calling the accounts API, and both are tested here rather than assumed.
"""

from __future__ import annotations

import pytest

from academy import services
from academy.models import Enrolment, ModuleAttendance, TrainingPlan

pytestmark = pytest.mark.django_db


def test_the_training_record_is_in_the_personal_data_export(person, course, competence):
    from accounts.services import export_user_data

    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    plan = services.create_plan(person, title="Parcours conseillé")
    services.add_plan_item(plan, course)
    services.add_gap_line(plan, competence, required_level=2, current_level=0, course=course)

    export = export_user_data(person)
    section = export["academy"]

    assert section["enrolments"][0]["course"] == course.title
    assert section["enrolments"][0]["modules_attended"][0]["module"] == course.modules.first().title
    assert section["training_plans"][0]["title"] == "Parcours conseillé"
    assert section["training_plans"][0]["competence_comparison"][0]["gap"] == "Compétence à acquérir"
    # The export states the record, it does not grade it.
    assert "score" not in str(section)


def test_anonymising_an_account_erases_its_training_record(person, course):
    from accounts.services import anonymise_user

    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    services.create_plan(person, title="Parcours conseillé")

    anonymise_user(person)

    assert Enrolment.objects.filter(person_id=person.pk).count() == 0
    assert ModuleAttendance.objects.filter(enrolment_id=enrolment.pk).count() == 0
    assert TrainingPlan.objects.filter(person_id=person.pk).count() == 0


def test_the_erasure_receiver_is_idempotent(person, course):
    from academy.receivers import on_user_anonymised

    services.enrol(person, course)
    on_user_anonymised(None, user_id=person.pk)
    on_user_anonymised(None, user_id=person.pk)  # must not raise, must not re-create anything
    assert Enrolment.objects.filter(person_id=person.pk).count() == 0


def test_the_audit_trail_of_a_training_never_carries_the_course_content_or_an_email(person, course):
    from audit.models import AuditEvent

    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    for event in AuditEvent.objects.filter(action__startswith="academy."):
        blob = str(event.metadata)
        assert person.email not in blob
        assert course.description not in blob
