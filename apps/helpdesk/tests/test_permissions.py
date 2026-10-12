"""
Object-level authorisation of the digital help desk.

The rule the whole platform is built on: a user must never learn that an object exists — not through
a list, not through a count, not through a differently worded «not found». These tests check the
QUERYSET, not just the policy, because the queryset is what keeps a row out of a count.

Rebase directive §61 asks explicitly for: person A cannot reach person B, the professional sees only
what is assigned, and a hand-discovered identifier never bypasses a permission. All three are here.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from accounts.permissions import can
from helpdesk import services
from helpdesk.models import HelpdeskTicket, MessageVisibility, TicketMessage

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# The queryset is the authorisation
# ---------------------------------------------------------------------------------------------
def test_a_person_sees_only_their_own_requests(ticket, other_person):
    assert HelpdeskTicket.objects.readable_by(ticket.person).count() == 1
    assert HelpdeskTicket.objects.readable_by(other_person).count() == 0


def test_an_anonymous_user_sees_nothing(ticket):
    from django.contrib.auth.models import AnonymousUser

    assert HelpdeskTicket.objects.readable_by(AnonymousUser()).count() == 0


def test_a_hand_discovered_identifier_does_not_bypass_the_permission(ticket, other_person):
    """The refusal is indistinguishable from «does not exist»: no existence is disclosed."""
    with pytest.raises(PermissionDenied):
        services.ticket_detail(other_person, ticket.uuid)


def test_project_staff_see_nothing(ticket, staff_user):
    """Reading somebody's question to a lawyer is not supervision."""
    assert HelpdeskTicket.objects.readable_by(staff_user).count() == 0
    assert can(staff_user, "view", ticket) is False


def test_an_operator_may_dispatch_but_may_not_read(ticket, operator):
    services.request_professional_review(ticket, actor=ticket.person)
    ticket.refresh_from_db()

    assert HelpdeskTicket.objects.readable_by(operator).count() == 0
    assert can(operator, "view", ticket) is False
    assert can(operator, "dispatch", ticket) is True

    # The dispatch register lists the row and defers the question: the text is not fetched at all.
    row = HelpdeskTicket.objects.dispatchable_by(operator).get(pk=ticket.pk)
    assert row.reference == ticket.reference
    assert "question" in row.get_deferred_fields()


def test_a_professional_sees_only_what_is_confided_to_them(assigned_ticket, professional, other_professional):
    assert HelpdeskTicket.objects.readable_by(professional).count() == 1
    assert HelpdeskTicket.objects.readable_by(other_professional).count() == 0
    with pytest.raises(PermissionDenied):
        services.ticket_detail(other_professional, assigned_ticket.uuid)


def test_a_revoked_mandate_stops_granting_access(assigned_ticket, professional):
    services.revoke_mandate(assigned_ticket, actor=assigned_ticket.person)
    assert HelpdeskTicket.objects.readable_by(professional).count() == 0
    with pytest.raises(PermissionDenied):
        services.ticket_detail(professional, assigned_ticket.uuid)


# ---------------------------------------------------------------------------------------------
# The professional note is not part of the exchange the person reads
# ---------------------------------------------------------------------------------------------
def test_an_internal_note_is_invisible_to_the_person(assigned_ticket, professional):
    services.add_internal_note(assigned_ticket, "Vérifier l’arrêté cité par la personne.", actor=professional)

    person_view = services.exchange_for(assigned_ticket.person, assigned_ticket)
    assert all(message.visibility == MessageVisibility.SHARED for message in person_view)

    professional_view = services.exchange_for(professional, assigned_ticket)
    assert any(message.is_internal for message in professional_view)


def test_the_message_policy_refuses_every_action_but_view(assigned_ticket, professional):
    message = services.add_internal_note(assigned_ticket, "Note.", actor=professional)
    assert can(professional, "view", message) is True
    assert can(professional, "change", message) is False
    assert can(professional, "delete", message) is False
    assert can(assigned_ticket.person, "view", message) is False


def test_message_queryset_hides_other_peoples_exchanges(assigned_ticket, other_person, other_professional):
    assert TicketMessage.objects.readable_by(other_person).count() == 0
    assert TicketMessage.objects.readable_by(other_professional).count() == 0


def test_an_administrator_reads_the_exchange_but_never_a_professional_note(
    assigned_ticket, professional, administrator
):
    """
    The two defences must agree.

    ``policies.message_policy`` says an internal note is for the live assignee and nobody else. The
    QUERYSET is what the detail page renders, so if it were wider than the policy the policy would be
    decoration: an administrator would read privileged working material written under a mandate they
    do not hold, and the narrower rule would only ever have been a comment.
    """
    services.add_internal_note(assigned_ticket, "Vérifier l’arrêté cité par la personne.", actor=professional)

    visible = services.exchange_for(administrator, assigned_ticket)
    assert visible.count() > 0, "an administrator must still be able to read the shared exchange"
    assert all(message.visibility == MessageVisibility.SHARED for message in visible)

    note = TicketMessage.objects.get(visibility=MessageVisibility.INTERNAL)
    assert can(administrator, "view", note) is False
    assert TicketMessage.objects.readable_by(administrator).filter(pk=note.pk).exists() is False


def test_a_superuser_reads_the_exchange_but_never_a_professional_note(assigned_ticket, professional, superuser):
    """A right is not a mandate — and ``can()`` grants a superadmin every right by construction."""
    services.add_internal_note(assigned_ticket, "Note de travail.", actor=professional)
    visible = services.exchange_for(superuser, assigned_ticket)
    assert visible.count() > 0
    assert all(message.visibility == MessageVisibility.SHARED for message in visible)


def test_an_administrator_who_holds_the_mandate_reads_their_own_notes(assigned_ticket, administrator, professional):
    """The exception is the mandate itself, never the role."""
    from accounts import roles

    roles.assign_role(administrator, roles.PROFESSIONAL)
    services.add_internal_note(assigned_ticket, "Note du professionnel en place.", actor=professional)
    services.assign(
        assigned_ticket,
        administrator,
        mandate_note="Reprendre l’examen de la recevabilité de l’attestation.",
        actor=administrator,
    )
    assert any(message.is_internal for message in services.exchange_for(administrator, assigned_ticket))


# ---------------------------------------------------------------------------------------------
# A request never points at somebody else's file
# ---------------------------------------------------------------------------------------------
def test_a_request_cannot_be_attached_to_another_persons_case(person_user, other_person):
    from cases import services as case_services

    foreign_case = case_services.open_case(other_person, purpose="work")
    with pytest.raises(PermissionDenied):
        services.open_ticket(
            person_user,
            subject="Tentative",
            question="Une question qui vise le dossier de quelqu’un d’autre.",
            case=foreign_case,
        )


def test_the_open_form_only_offers_the_signed_in_persons_own_cases(person_user, other_person):
    from cases import services as case_services
    from helpdesk.forms import OpenRequestForm

    mine = case_services.open_case(person_user, purpose="work")
    case_services.open_case(other_person, purpose="study")

    form = OpenRequestForm(person=person_user)
    assert list(form.fields["case"].queryset) == [mine]


# ---------------------------------------------------------------------------------------------
# Expiry, again, at the message level
# ---------------------------------------------------------------------------------------------
def test_an_expired_mandate_hides_the_exchange_too(assigned_ticket, professional):
    HelpdeskTicket.objects.filter(pk=assigned_ticket.pk).update(
        mandate_valid_until=timezone.localdate() - dt.timedelta(days=1)
    )
    assert TicketMessage.objects.readable_by(professional).count() == 0
