"""
Authorisation: deny by default, applied in the queryset.

The rule this suite holds is not "an unauthorised user gets an error" but "an unauthorised user
learns nothing": no count, no autocomplete, no differently worded refusal may reveal that an
object exists. ``enrolment_for`` and ``plan_for`` therefore raise the SAME PermissionDenied for an
object that is not there and for an object that is there but not theirs.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from academy import services
from academy.models import Course, Enrolment, TrainingPlan
from accounts.permissions import can

pytestmark = pytest.mark.django_db


def test_nothing_is_readable_without_a_policy_for_an_anonymous_user(course):
    from django.contrib.auth.models import AnonymousUser

    anonymous = AnonymousUser()
    assert can(anonymous, "view", course) is False
    assert list(Course.objects.visible_to(anonymous)) == []


def test_a_published_course_is_viewable_by_any_authenticated_account(person, course):
    assert can(person, "view", course) is True
    assert can(person, "enrol", course) is True


def test_a_draft_course_is_neither_viewable_nor_enrollable_by_a_person(person, draft_course):
    assert can(person, "view", draft_course) is False
    assert can(person, "enrol", draft_course) is False
    with pytest.raises(PermissionDenied):
        services.course_for(person, draft_course.slug)


def test_nobody_changes_the_catalogue_but_administration(person, professional, admin_user, course):
    assert can(person, "change", course) is False
    assert can(professional, "change", course) is False
    assert can(admin_user, "change", course) is True


def test_an_enrolment_is_invisible_to_everyone_but_its_person(person, other_person, course):
    enrolment = services.enrol(person, course)

    assert can(person, "view", enrolment) is True
    assert can(other_person, "view", enrolment) is False
    assert list(Enrolment.objects.readable_by(other_person)) == []
    with pytest.raises(PermissionDenied):
        services.enrolment_for(other_person, enrolment.uuid)


def test_the_refusal_is_the_same_whether_the_object_exists_or_not(person, other_person, course):
    """An identical exception for both cases: the wording must not leak existence."""
    import uuid as uuid_module

    enrolment = services.enrol(person, course)
    with pytest.raises(PermissionDenied) as existing:
        services.enrolment_for(other_person, enrolment.uuid)
    with pytest.raises(PermissionDenied) as absent:
        services.enrolment_for(other_person, uuid_module.uuid4())
    assert type(existing.value) is type(absent.value)
    assert str(existing.value) == str(absent.value)


def test_staff_gets_no_platform_side_list_of_who_is_learning_what(staff_user, person, course):
    """
    Deliberately stricter than the catalogue, and the same decision ``CaseFileQuerySet`` takes:
    supervision happens in the back-office, which is role-checked and audited. A standing list of
    everyone's training in the platform is a disclosure of personal data, not supervision.
    """
    services.enrol(person, course)
    assert list(Enrolment.objects.readable_by(staff_user)) == []


def test_an_attendance_fact_can_never_be_changed_by_anyone(person, admin_user, course):
    enrolment = services.enrol(person, course)
    attendance = services.record_attendance(enrolment, course.modules.first())
    assert can(person, "change", attendance) is False
    assert can(admin_user, "change", attendance) is False
    assert can(person, "view", attendance) is True


def test_a_person_may_interrupt_their_own_training_but_not_delete_the_record(person, course):
    enrolment = services.enrol(person, course)
    assert can(person, "change", enrolment) is True
    assert can(person, "delete", enrolment) is False


def test_a_plan_is_invisible_to_another_person(person, other_person):
    plan = services.create_plan(person, title="Mon parcours")
    assert can(other_person, "view", plan) is False
    assert list(TrainingPlan.objects.readable_by(other_person)) == []
    with pytest.raises(PermissionDenied):
        services.plan_for(other_person, plan.uuid)


def test_an_expired_authorisation_stops_reading_the_plan(person, professional):
    import datetime as dt

    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    case = case_services.open_case(person, purpose=CasePurpose.TRAINING)
    plan = services.create_plan(person, title="Parcours accompagné", case=case)
    case_services.assign(
        case,
        professional,
        role=AssignmentRole.PROFESSIONAL,
        authorisation_valid_until=dt.date(2020, 1, 1),  # lapsed
    )
    assert list(TrainingPlan.objects.readable_by(professional)) == []
    assert can(professional, "view", plan) is False


def test_an_authorised_actor_assignment_does_not_open_the_training_record(person, user_factory):
    """
    CR-03 reserves certain activities to an authorised actor; it does not hand them the person's
    training file. Their mandate concerns the phase reserved to them, and nothing else.
    """
    import datetime as dt

    from accounts import roles
    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    actor = user_factory("acteur@example.test", role=roles.PROFESSIONAL)
    case = case_services.open_case(person, purpose=CasePurpose.WORK)
    plan = services.create_plan(person, title="Parcours", case=case)
    case_services.assign(
        case,
        actor,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="AUT-2026-001",
        # In force: a year from today in Rome. A fixed 2099 would lapse, and the test pass for nothing.
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),
    )
    assert can(actor, "view", plan) is False
    # And the row never enters the queryset either. Until 21 September 2026 it did: the policy
    # refused the detail page while "my trainings" still listed the plan's title, its origin and
    # its origin reference. Deny by default is a property of the QUERY, not of the last check.
    assert list(TrainingPlan.objects.readable_by(actor)) == []
    assert list(services.plans_for(actor)) == []


def test_the_plan_queryset_and_the_plan_policy_agree_for_every_assignment_role(person, user_factory):
    """
    The list and the object check must never disagree.

    A row the policy would refuse must not be listed, and a row the policy allows must be listed —
    otherwise one of the two is the real authorisation and the other is decoration.
    """
    import datetime as dt

    from accounts import roles
    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    for index, role in enumerate(AssignmentRole.values):
        reader = user_factory(f"assigne-{index}@example.test", role=roles.PROFESSIONAL)
        case = case_services.open_case(person, purpose=CasePurpose.WORK)
        plan = services.create_plan(person, title=f"Parcours {role}", case=case)
        case_services.assign(
            case,
            reader,
            role=role,
            authorisation_reference="AUT-2026-00X",
            authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),  # in force, a year on
        )
        listed = plan in TrainingPlan.objects.readable_by(reader)
        allowed = can(reader, "view", plan)
        assert listed == allowed, f"{role}: listed={listed} but policy says {allowed}"
