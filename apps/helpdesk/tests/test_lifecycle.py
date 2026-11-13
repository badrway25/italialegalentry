"""
The state machine of the digital help desk.

These tests exist because the seven states of Technical Blueprint §13 are a promise to a person
about what is happening to their question. A state that can be reached without the thing it
announces, or that can be reached from anywhere, is decoration.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from audit.models import AuditEvent
from helpdesk import services
from helpdesk.models import (
    ALLOWED_TRANSITIONS,
    HelpdeskTicket,
    MessageKind,
    MessageVisibility,
    ResponderRole,
    TicketOrigin,
    TicketStatus,
)

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# The declared table
# ---------------------------------------------------------------------------------------------
def test_every_state_is_declared_in_the_transition_table():
    assert set(ALLOWED_TRANSITIONS) == set(TicketStatus.values)


def test_closed_is_terminal():
    assert ALLOWED_TRANSITIONS[TicketStatus.CLOSED] == frozenset()


def test_an_undeclared_transition_is_refused(ticket):
    # INFORMATION_ONLY → IN_REVIEW is not in the table: there is nobody to review it.
    with pytest.raises(ValidationError):
        services.transition(ticket, TicketStatus.IN_REVIEW)
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.INFORMATION_ONLY


def test_an_unknown_state_is_refused(ticket):
    with pytest.raises(ValidationError):
        services.transition(ticket, "approved")


def test_a_closed_request_is_never_reopened(ticket):
    services.close(ticket, actor=ticket.person, reason="Question résolue.")
    with pytest.raises(ValidationError):
        services.transition(ticket, TicketStatus.INFORMATION_ONLY)


# ---------------------------------------------------------------------------------------------
# The mandate invariant
# ---------------------------------------------------------------------------------------------
def test_assignment_without_a_mandate_note_is_refused(ticket, professional, operator):
    services.request_professional_review(ticket, actor=ticket.person)
    with pytest.raises(ValidationError):
        services.assign(ticket, professional, mandate_note="   ", actor=operator)


def test_only_an_account_with_the_professional_role_can_be_designated(ticket, person_user, operator, other_person):
    services.request_professional_review(ticket, actor=ticket.person)
    with pytest.raises(ValidationError):
        services.assign(ticket, other_person, mandate_note="Examiner le dossier.", actor=operator)


def test_a_mandate_cannot_be_given_with_an_expired_date(ticket, professional, operator):
    services.request_professional_review(ticket, actor=ticket.person)
    with pytest.raises(ValidationError):
        services.assign(
            ticket,
            professional,
            mandate_note="Examiner la recevabilité de l’attestation.",
            valid_until=dt.date(2020, 1, 1),
            actor=operator,
        )


def test_an_expired_mandate_stops_granting_anything(assigned_ticket, professional):
    """
    The passage of time, not a revocation.

    A dated authorisation that keeps working after its date is not an authorisation, so the day the
    mandate lapses the professional stops seeing the request and stops being able to act on it —
    with nobody having to remember to switch anything off.
    """
    HelpdeskTicket.objects.filter(pk=assigned_ticket.pk).update(
        mandate_valid_until=timezone.localdate() - dt.timedelta(days=1)
    )
    assigned_ticket.refresh_from_db()

    assert assigned_ticket.mandate_is_live is False
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0
    with pytest.raises(ValidationError):
        services.publish_response(assigned_ticket, "Voici la réponse.", actor=professional)


def test_a_lapsed_mandate_returns_the_request_to_the_designation_register(
    assigned_ticket, professional, operator, other_professional
):
    """
    A request must never be stranded.

    Before this was fixed, a mandate that ran out on its date left the request in IN_REVIEW: the
    professional could no longer open it, the designation register only looked at
    PROFESSIONAL_REVIEW_REQUIRED so nobody could find it, no second professional could be designated
    — and the person's page went on saying « Le professionnel désigné examine votre demande » about
    an account that could not read a word of it. The state outlived the thing it announced.
    """
    HelpdeskTicket.objects.filter(pk=assigned_ticket.pk).update(
        mandate_valid_until=timezone.localdate() - dt.timedelta(days=1)
    )
    assigned_ticket.refresh_from_db()
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0

    # The register finds it again, still without the text of the question.
    waiting = HelpdeskTicket.objects.dispatchable_by(operator)
    assert list(waiting.values_list("pk", flat=True)) == [assigned_ticket.pk]
    assert "question" in waiting.get(pk=assigned_ticket.pk).get_deferred_fields()

    # And a second professional can be designated, which is the point of finding it.
    services.assign(
        assigned_ticket,
        other_professional,
        mandate_note="Reprendre l’examen de la recevabilité de l’attestation.",
        actor=operator,
    )
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.ASSIGNED
    assert assigned_ticket.assignee_id == other_professional.pk
    assert HelpdeskTicket.objects.readable_by(other_professional).count() == 1
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0


def test_an_answered_request_is_not_re_queued_when_its_mandate_lapses(assigned_ticket, professional, operator):
    """A reply that exists goes on existing. Re-queueing it would invent work that is already done."""
    services.publish_response(assigned_ticket, "Votre attestation reste recevable.", actor=professional)
    HelpdeskTicket.objects.filter(pk=assigned_ticket.pk).update(
        mandate_valid_until=timezone.localdate() - dt.timedelta(days=1)
    )
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.RESPONSE_AVAILABLE
    assert HelpdeskTicket.objects.dispatchable_by(operator).count() == 0
    # …and the person can still read the reply that was written for them.
    assert services.exchange_for(assigned_ticket.person, assigned_ticket).count() == 2


def test_the_state_shown_never_survives_the_mandate_it_depends_on(assigned_ticket, professional):
    """
    Expiry is nobody's action, so nothing writes a transition on the day it happens.

    The stored value stays IN_REVIEW — it is the record of what was decided — but what the page says
    is read through ``effective_status``, so it never announces an examination that no account in the
    platform can carry out.
    """
    HelpdeskTicket.objects.filter(pk=assigned_ticket.pk).update(
        mandate_valid_until=timezone.localdate() - dt.timedelta(days=1)
    )
    assigned_ticket.refresh_from_db()

    assert assigned_ticket.status == TicketStatus.IN_REVIEW
    assert assigned_ticket.effective_status == TicketStatus.PROFESSIONAL_REVIEW_REQUIRED
    assert "attend qu’un professionnel soit désigné" in services.next_step_for(assigned_ticket)
    assert "examine votre demande" not in services.next_step_for(assigned_ticket)


def test_revoking_a_mandate_puts_the_request_back_in_the_queue(assigned_ticket, professional, operator):
    services.revoke_mandate(assigned_ticket, actor=operator)
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.PROFESSIONAL_REVIEW_REQUIRED
    assert "Cette étape ne dépend pas de vous" in services.next_step_for(assigned_ticket)
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0
    assert HelpdeskTicket.objects.dispatchable_by(operator).count() == 1


def test_returning_to_the_queue_is_audited_as_a_transition(assigned_ticket, operator):
    services.revoke_mandate(assigned_ticket, actor=operator)
    events = AuditEvent.objects.filter(target_type="HelpdeskTicket").values_list("action", flat=True)
    assert "helpdesk.assignment.revoked" in set(events)
    last = AuditEvent.objects.filter(action="helpdesk.transition").order_by("-id").first()
    assert last.metadata == {
        "from": TicketStatus.IN_REVIEW.value,
        "to": TicketStatus.PROFESSIONAL_REVIEW_REQUIRED.value,
    }


def test_a_handover_ends_one_mandate_before_it_begins_another(
    assigned_ticket, professional, other_professional, operator
):
    """
    Confiding a request that is already in somebody's hands is two facts, not one.

    The state returns to «waiting for a professional» and then to ASSIGNED — not straight to the new
    name while the page still says IN_REVIEW, which would claim that the new professional had
    already begun reading. The trail names the account that lost the mandate.
    """
    services.assign(
        assigned_ticket,
        other_professional,
        mandate_note="Reprendre l’examen de la recevabilité de l’attestation.",
        actor=operator,
    )
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.assignee_id == other_professional.pk
    assert assigned_ticket.status == TicketStatus.ASSIGNED
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0

    event = AuditEvent.objects.filter(action="helpdesk.assigned").order_by("-id").first()
    assert event.metadata["previous_assignee"] == professional.pk
    assert event.metadata["assignee"] == other_professional.pk


def test_a_professional_who_is_not_the_assignee_cannot_act(assigned_ticket, other_professional):
    with pytest.raises(ValidationError):
        services.publish_response(assigned_ticket, "Voici ma réponse.", actor=other_professional)


def test_an_administrator_cannot_answer_in_a_professionals_place(assigned_ticket, superuser):
    """A right is not a mandate: the platform must not be able to speak as the professional."""
    with pytest.raises(ValidationError):
        services.publish_response(assigned_ticket, "Réponse de l’administration.", actor=superuser)


# ---------------------------------------------------------------------------------------------
# «Réponse disponible» means a reply exists
# ---------------------------------------------------------------------------------------------
def test_response_available_is_unreachable_without_a_shared_reply(assigned_ticket):
    assert assigned_ticket.has_shared_response() is False
    with pytest.raises(ValidationError):
        services.transition(assigned_ticket, TicketStatus.RESPONSE_AVAILABLE)


def test_publishing_a_response_moves_the_state_and_records_the_role(assigned_ticket, professional):
    message = services.publish_response(assigned_ticket, "Votre attestation reste recevable.", actor=professional)
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.RESPONSE_AVAILABLE
    assert message.author_role == ResponderRole.PROFESSIONAL
    assert message.visibility == MessageVisibility.SHARED
    assert message.kind == MessageKind.RESPONSE


# ---------------------------------------------------------------------------------------------
# Clarification round trip
# ---------------------------------------------------------------------------------------------
def test_clarification_returns_the_request_to_the_professional(assigned_ticket, professional):
    services.ask_clarification(assigned_ticket, "Pouvez-vous préciser la date d’obtention ?", actor=professional)
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.NEEDS_CLARIFICATION

    services.add_person_message(assigned_ticket, "Elle date du 4 mars 2025.", actor=assigned_ticket.person)
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.IN_REVIEW


def test_clarification_without_a_mandate_returns_to_information_only(ticket, person_user):
    services.transition(ticket, TicketStatus.NEEDS_CLARIFICATION)
    services.add_person_message(ticket, "Voici la précision demandée.", actor=person_user)
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.INFORMATION_ONLY


# ---------------------------------------------------------------------------------------------
# Escalation from the rule engine
# ---------------------------------------------------------------------------------------------
def _assessment(case, outcome):
    from cases import services as case_services

    return case_services.record_assessment(
        case,
        outcome=outcome,
        ruleset_version=1,
        ruleset_snapshot={"version": 1, "rules": []},
        answers={"q": "a"},
    )


@pytest.fixture
def case(db, person_user):
    from cases import services as case_services

    return case_services.open_case(person_user, purpose="work")


def test_a_review_required_outcome_opens_a_request_automatically(case):
    from cases.models import AssessmentOutcome

    assessment = _assessment(case, AssessmentOutcome.REVIEW_REQUIRED)
    ticket = HelpdeskTicket.objects.get(assessment=assessment)
    assert ticket.status == TicketStatus.PROFESSIONAL_REVIEW_REQUIRED
    assert ticket.origin == TicketOrigin.ASSESSMENT
    assert ticket.person_id == case.person_id
    assert ticket.case_id == case.pk


def test_a_possible_outcome_opens_nothing(case):
    from cases.models import AssessmentOutcome

    _assessment(case, AssessmentOutcome.POSSIBLE)
    assert HelpdeskTicket.objects.count() == 0


def test_the_escalation_is_idempotent(case):
    from cases.models import AssessmentOutcome

    assessment = _assessment(case, AssessmentOutcome.REVIEW_REQUIRED)
    again = services.open_from_assessment(assessment)
    assert HelpdeskTicket.objects.filter(assessment=assessment).count() == 1
    assert again.pk == HelpdeskTicket.objects.get(assessment=assessment).pk


# ---------------------------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------------------------
def test_open_assign_reply_and_close_are_all_audited(ticket, professional, operator):
    services.request_professional_review(ticket, actor=ticket.person)
    services.assign(ticket, professional, mandate_note="Examiner l’attestation.", actor=operator)
    services.take_in_review(ticket, actor=professional)
    services.publish_response(ticket, "Voici la réponse.", actor=professional)
    services.close(ticket, actor=ticket.person, reason="Merci.")

    actions = set(AuditEvent.objects.filter(target_type="HelpdeskTicket").values_list("action", flat=True))
    assert {"helpdesk.opened", "helpdesk.assigned", "helpdesk.response", "helpdesk.closed"} <= actions


def test_the_audit_trail_never_carries_the_text_of_the_exchange(assigned_ticket, professional):
    secret = "Ceci est le texte confidentiel de la réponse."
    services.publish_response(assigned_ticket, secret, actor=professional)
    for event in AuditEvent.objects.filter(target_type="HelpdeskTicket"):
        assert secret not in str(event.metadata)
        assert secret not in event.target_repr
