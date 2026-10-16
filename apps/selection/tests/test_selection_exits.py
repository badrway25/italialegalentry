"""
A selection whose authorised actor's assignment on the file ended while the process was open (sec-f7 REVIEW, finding 4).

The case domain moves a file for an authorised actor only on the selection service's path
(``cases.services.transition(..., as_authorised_actor=True)``, the lifecycle's «Chi può» column). The reserved act —
into SELECTION, and out of it with a referral to the administrative procedure — needs the actor's assignment standing
on the file. The way back to the training pathway asserts no outcome and stays open: a revoked assignment must never
leave the file in SELECTION with nobody answerable for it (CASE_LIFECYCLE.md §4, rule 1) and a process nobody can
conclude.
"""

from __future__ import annotations

import pytest

from accounts import roles
from audit.models import AuditEvent
from cases import services as case_services
from cases.models import AssignmentRole, CaseStatus
from selection import services
from selection.models import SelectionOutcome

pytestmark = pytest.mark.django_db


def _end_the_actors_assignment(case):
    for row in case.assignments.filter(role=AssignmentRole.AUTHORISED_ACTOR, revoked_at__isnull=True):
        case_services.revoke_assignment(row)


def _last_move(case):
    return (
        AuditEvent.objects.filter(action="case.transition", target_type="CaseFile", target_id=str(case.pk))
        .order_by("-created_at", "-id")
        .first()
    )


def test_a_selection_whose_assignment_ended_still_concludes_without_a_referral(process, case, operator):
    _end_the_actors_assignment(case)
    services.conclude(process, SelectionOutcome.CLOSED_NO_FOLLOW_UP, operator=operator)
    process.refresh_from_db()
    case.refresh_from_db()
    assert process.is_closed and case.status == CaseStatus.TRAINING
    move = _last_move(case)
    assert move.actor_id == operator.pk
    assert (move.metadata["from"], move.metadata["to"]) == (CaseStatus.SELECTION, CaseStatus.TRAINING)


def test_but_refers_nobody_to_the_procedure_once_its_assignment_ended(process, case, operator):
    _end_the_actors_assignment(case)
    with pytest.raises(case_services.TransitionNotPermitted):
        services.conclude(process, SelectionOutcome.REFERRED_TO_PROCEDURE, operator=operator)
    process.refresh_from_db()
    case.refresh_from_db()
    assert not process.is_closed and case.status == CaseStatus.SELECTION, "refused whole: nothing half-done"


def test_the_way_back_is_the_selection_services_alone(process, case, operator, person, stranger):
    """Not a door for anybody else: the flag is the selection service's and the domain still asks for the role; without
    the flag the authorised actor has no hand on the file at all (the case policy gives it no «change»)."""
    _end_the_actors_assignment(case)
    for user in (person, stranger, None):
        with pytest.raises(case_services.TransitionNotPermitted):
            case_services.transition(case, CaseStatus.TRAINING, actor=user, as_authorised_actor=True)
    with pytest.raises(case_services.TransitionNotPermitted):
        case_services.transition(case, CaseStatus.TRAINING, actor=operator)
    case.refresh_from_db()
    assert case.status == CaseStatus.SELECTION


def test_the_administrator_returns_a_stuck_file_to_its_pathway_and_the_process_then_concludes(
    process, case, operator, make_user
):
    """The administrator's way out (``cases.models.BEYOND_SECTION_4``): SELECTION → TRAINING, which asserts no outcome —
    never SELECTION → ADMIN_PROCESS, the authorised actor's referral. The process is then concluded by its operator;
    the file, no longer in SELECTION, stays where the administrator put it."""
    administrator = make_user("administrator@example.test", role=roles.ADMINISTRATOR)
    _end_the_actors_assignment(case)
    with pytest.raises(case_services.TransitionNotPermitted):
        case_services.transition(case, CaseStatus.ADMIN_PROCESS, actor=administrator)
    case_services.transition(case, CaseStatus.TRAINING, actor=administrator)
    services.conclude(process, SelectionOutcome.CLOSED_NO_FOLLOW_UP, operator=operator)
    process.refresh_from_db()
    case.refresh_from_db()
    assert process.is_closed and case.status == CaseStatus.TRAINING
    assert _last_move(case).actor_id == administrator.pk
