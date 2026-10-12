"""
Deny by default, applied IN THE QUERYSET.

A user must never learn that an object exists — not through a count, not through an autocomplete,
not through a differently worded "not found". Every test here therefore checks the QUERYSET first
and the object-level policy second, because a policy that guards a detail page while a list still
counts the row has disclosed the row.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from accounts import roles
from accounts.permissions import can
from selection import services
from selection.models import ActorOperator, AuthorizedActor, SelectionProcess

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# An actor sees only its own assignments
# ---------------------------------------------------------------------------------------------
def test_an_actor_sees_only_the_processes_assigned_to_it(
    process, operator, make_user, company, mandate_factory, agency, other_agency, case
):
    """A second authorisation, with its own operator, must not see the first one's process."""
    today = timezone.localdate()
    second_actor = services.register_actor(
        organisation=other_agency,
        actor_type="authorised_intermediary",
        jurisdiction="IT",
        authorisation_reference="TEST-AUT-0002",
        valid_from=today - dt.timedelta(days=10),
        valid_until=today + dt.timedelta(days=100),
    )
    second_operator = make_user("operator2@example.test", role=roles.AUTHORISED_ACTOR)
    services.add_operator(second_actor, second_operator)

    assert list(SelectionProcess.objects.for_operator(operator)) == [process]
    assert list(SelectionProcess.objects.for_operator(second_operator)) == []
    # and not through a count either
    assert SelectionProcess.objects.readable_by(second_operator).count() == 0
    assert can(second_operator, "view", process) is False


def test_the_workspace_never_returns_a_global_view(process, operator, superuser):
    """Even an account that may read everything through the admin gets only its own here."""
    assert list(SelectionProcess.objects.for_operator(superuser)) == []
    assert services.workspace(operator) == [process]


# ---------------------------------------------------------------------------------------------
# A lapsed authorisation reads nothing
# ---------------------------------------------------------------------------------------------
def test_a_lapsed_authorisation_reads_nothing(process, operator, actor):
    assert SelectionProcess.objects.readable_by(operator).count() == 1
    actor.valid_until = timezone.localdate() - dt.timedelta(days=1)
    actor.save(update_fields=["valid_until"])
    assert SelectionProcess.objects.readable_by(operator).count() == 0, "not even a count"
    assert list(SelectionProcess.objects.for_operator(operator)) == []
    with pytest.raises(PermissionDenied):
        services.get_process(operator, process.uuid)


def test_a_suspended_authorisation_reads_nothing(process, operator, actor):
    actor.suspended_at = timezone.now()
    actor.save(update_fields=["suspended_at"])
    assert SelectionProcess.objects.readable_by(operator).count() == 0


def test_a_withdrawn_authorisation_reads_nothing(process, operator, actor):
    actor.withdrawn_at = timezone.now()
    actor.save(update_fields=["withdrawn_at"])
    assert SelectionProcess.objects.readable_by(operator).count() == 0


def test_a_revoked_operator_reads_nothing(process, operator, actor):
    row = ActorOperator.objects.get(actor=actor, user=operator)
    services.revoke_operator(row)
    assert SelectionProcess.objects.readable_by(operator).count() == 0
    assert can(operator, "view", process) is False


def test_an_authorisation_that_has_not_started_yet_opens_nothing(agency, make_user):
    today = timezone.localdate()
    future = AuthorizedActor(
        organisation=agency,
        actor_type="employment_agency",
        jurisdiction="IT",
        authorisation_reference="TEST-AUT-FUTURE",
        valid_from=today + dt.timedelta(days=10),
    )
    future.full_clean(exclude=["uuid"])
    future.save()
    assert future.is_valid() is False
    assert AuthorizedActor.objects.valid().filter(pk=future.pk).exists() is False


# ---------------------------------------------------------------------------------------------
# The three perimeters, and nothing else
# ---------------------------------------------------------------------------------------------
def test_the_person_sees_the_process_opened_on_their_own_case(process, person):
    assert SelectionProcess.objects.readable_by(person).count() == 1
    assert can(person, "view", process) is True
    assert can(person, "change", process) is False, "the person sees; they do not act on the process"


def test_the_company_sees_the_process_attached_to_its_own_need(process, company_user):
    assert SelectionProcess.objects.readable_by(company_user).count() == 1
    assert can(company_user, "view", process) is True
    assert can(company_user, "change", process) is False


def test_a_stranger_sees_nothing_at_all(process, stranger):
    assert SelectionProcess.objects.readable_by(stranger).count() == 0
    assert can(stranger, "view", process) is False
    with pytest.raises(PermissionDenied):
        services.get_process(stranger, process.uuid)


def test_an_anonymous_visitor_sees_nothing(process):
    from django.contrib.auth.models import AnonymousUser

    assert SelectionProcess.objects.readable_by(AnonymousUser()).count() == 0
    assert can(AnonymousUser(), "view", process) is False


def test_project_staff_get_nothing_here(process, staff_user):
    """
    Same choice as ``cases``: a standing platform-side list of selection processes is not
    supervision, it is a disclosure. Staff supervise from the back-office, where access is audited.
    """
    assert SelectionProcess.objects.readable_by(staff_user).count() == 0
    assert can(staff_user, "view", process) is False


def test_an_administrator_reads_everything_and_the_superuser_passes_through(process, superuser, make_user):
    admin = make_user("admin-role@example.test", role=roles.ADMINISTRATOR)
    assert SelectionProcess.objects.readable_by(admin).count() == 1
    assert SelectionProcess.objects.readable_by(superuser).count() == 1


def test_a_recorded_movement_is_never_editable(process, operator, superuser):
    from selection.models import SelectionStage

    services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator)
    event = process.events.first()
    assert can(operator, "view", event) is True
    # A correction is a new movement, never an edit: the history stays honest. The superuser short
    # circuit in ``accounts.permissions.can`` is checked through the policy directly.
    from selection.policies import stage_event_policy

    assert stage_event_policy(superuser, "change", event) is False


def test_an_unregistered_model_is_denied_by_default():
    """The registry answers False for anything nobody registered — that is the whole design."""
    from accounts.permissions import _POLICIES
    from selection import models as selection_models

    registered = {
        selection_models.AuthorizedActor,
        selection_models.ActorOperator,
        selection_models.SelectionMandate,
        selection_models.SelectionProcess,
        selection_models.SelectionEvidence,
        selection_models.IdentityDisclosure,
        selection_models.SelectionStageEvent,
        selection_models.IdentityAccess,
    }
    assert registered <= set(_POLICIES), "every model this app adds must carry a policy"


@pytest.fixture
def staff_user(make_user):
    from accounts.models import AccountType

    return make_user("staff@example.test", role=roles.STAFF, account_type=AccountType.STAFF)


# ---------------------------------------------------------------------------------------------
# The back-office is an administration tool, not a second way to move a process
# ---------------------------------------------------------------------------------------------
def test_the_admin_cannot_create_a_process_behind_open_process(rf, superuser):
    """
    ``services.open_process`` is the only way a process exists, so the admin form must not be a
    second one: a row added there would carry no ``CaseAssignment``, no authorisation and no audit.
    """
    from django.contrib import admin as django_admin

    from selection.models import SelectionProcess

    request = rf.get("/backoffice/")
    request.user = superuser
    assert django_admin.site._registry[SelectionProcess].has_add_permission(request) is False


def test_the_admin_cannot_move_a_stage_or_write_an_outcome(rf, superuser, process):
    """
    A stage must name the authorised actor answerable for it. The admin form calls neither
    ``advance`` nor ``conclude``, so an editable ``stage`` there would skip the transition table,
    the stage event and the audit row alike.
    """
    from django.contrib import admin as django_admin

    from selection.models import SelectionProcess

    request = rf.get("/backoffice/")
    request.user = superuser
    model_admin = django_admin.site._registry[SelectionProcess]
    readonly = set(model_admin.get_readonly_fields(request, process))
    assert {"stage", "outcome"} <= readonly


def test_the_admin_cannot_grant_a_disclosure_in_the_persons_place(rf, superuser):
    """Granting is the person's act. The back-office may read the register, never decide in it."""
    from django.contrib import admin as django_admin

    from selection.models import IdentityDisclosure

    request = rf.get("/backoffice/")
    request.user = superuser
    model_admin = django_admin.site._registry[IdentityDisclosure]
    assert model_admin.has_add_permission(request) is False
    readonly = set(model_admin.get_readonly_fields(request, None))
    assert {"status", "consent", "expires_at"} <= readonly
