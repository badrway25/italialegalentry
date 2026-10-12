"""
The HTTP surface of the digital help desk.

These are the tests that make the difference between «the models exist» and «the feature works»:
they drive the same forms a person drives, through the whole flow — open, escalate, designate, take
in review, reply, read the reply, close — and they check what is NOT on the page as carefully as
what is.

They run against the project's real URLconf: the module is mounted at
``/espace-reserve/guichet/``, under the reserved area and before the portal's own routes.
"""

from __future__ import annotations

import pytest

from helpdesk import services
from helpdesk.models import HelpdeskTicket, TicketStatus

pytestmark = pytest.mark.django_db

PASSWORD = "Str0ng-Passw0rd-2026!"


def login(client, user):
    assert client.login(email=user.email, password=PASSWORD)
    return client


# ---------------------------------------------------------------------------------------------
# Access
# ---------------------------------------------------------------------------------------------
def test_every_page_requires_an_account(client, reserved_area_on):
    for path in ("/fr/espace-reserve/guichet/", "/fr/espace-reserve/guichet/nouvelle-demande/"):
        response = client.get(path)
        assert response.status_code == 302
        assert "/compte/" in response["Location"]


def test_the_register_is_never_indexed_and_never_cached(client, reserved_area_on, person_user):
    login(client, person_user)
    response = client.get("/fr/espace-reserve/guichet/")
    assert response.status_code == 200
    assert "noindex" in response.content.decode()
    assert "no-store" in response["Cache-Control"]


def test_a_person_cannot_open_another_persons_request(client, reserved_area_on, ticket, other_person):
    login(client, other_person)
    response = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/")
    assert response.status_code == 403


def test_the_dispatch_register_is_refused_to_a_person(client, reserved_area_on, person_user):
    login(client, person_user)
    assert client.get("/fr/espace-reserve/guichet/designation/").status_code == 403


def test_the_professional_queue_is_refused_to_a_person(client, reserved_area_on, person_user):
    login(client, person_user)
    assert client.get("/fr/espace-reserve/guichet/confiees/").status_code == 403


# ---------------------------------------------------------------------------------------------
# The whole flow, driven through the forms
# ---------------------------------------------------------------------------------------------
def test_the_full_escalation_flow(client, reserved_area_on, person_user, professional, operator):
    # 1. The person opens a request.
    login(client, person_user)
    response = client.post(
        "/fr/espace-reserve/guichet/nouvelle-demande/",
        {
            "subject": "Validité de mon attestation de langue",
            "question": "Mon attestation date de dix-huit mois : est-elle encore recevable ?",
        },
        follow=True,
    )
    assert response.status_code == 200
    ticket = HelpdeskTicket.objects.get(person=person_user)
    assert ticket.status == TicketStatus.INFORMATION_ONLY

    # 2. The person asks for a human.
    client.post(f"/fr/espace-reserve/guichet/{ticket.uuid}/verification-professionnelle/")
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.PROFESSIONAL_REVIEW_REQUIRED

    # 3. An operator designates a professional, with a mandate.
    client.logout()
    login(client, operator)
    listing = client.get("/fr/espace-reserve/guichet/designation/")
    assert listing.status_code == 200
    assert ticket.reference in listing.content.decode()
    # …and the operator's register does NOT carry the text of the question.
    assert "dix-huit mois" not in listing.content.decode()

    prefix = f"t{ticket.uuid.hex}"
    response = client.post(
        "/fr/espace-reserve/guichet/designation/",
        {
            "ticket": str(ticket.uuid),
            f"{prefix}-professional": professional.pk,
            f"{prefix}-role_label": "Avocat — droit de l’immigration",
            f"{prefix}-mandate_note": "Examiner la recevabilité de l’attestation de langue.",
        },
        follow=True,
    )
    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.ASSIGNED
    assert ticket.assignee_id == professional.pk

    # 4. The professional takes it in review and replies.
    client.logout()
    login(client, professional)
    queue = client.get("/fr/espace-reserve/guichet/confiees/")
    assert ticket.reference in queue.content.decode()

    client.post(f"/fr/espace-reserve/guichet/{ticket.uuid}/prise-en-charge/")
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.IN_REVIEW

    client.post(
        f"/fr/espace-reserve/guichet/{ticket.uuid}/reponse/",
        {"response-body": "Votre attestation reste recevable ; joignez le justificatif d’inscription."},
    )
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.RESPONSE_AVAILABLE

    # 5. The person reads the reply — with a FUNCTION and a date, never a name.
    client.logout()
    login(client, person_user)
    page = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode()
    assert "Votre attestation reste recevable" in page
    assert "Avocat" in page
    assert professional.email not in page
    assert str(professional.pk) not in page.split("csrfmiddlewaretoken")[0]


def test_the_person_never_reads_a_professional_note(client, reserved_area_on, assigned_ticket, professional):
    login(client, professional)
    client.post(
        f"/fr/espace-reserve/guichet/{assigned_ticket.uuid}/note/",
        {"note-body": "NOTE INTERNE: vérifier l’arrêté cité."},
    )
    client.logout()

    login(client, assigned_ticket.person)
    page = client.get(f"/fr/espace-reserve/guichet/{assigned_ticket.uuid}/").content.decode()
    assert "NOTE INTERNE" not in page


def test_a_professional_cannot_reply_to_a_request_that_is_not_theirs(
    client, reserved_area_on, assigned_ticket, other_professional
):
    login(client, other_professional)
    response = client.post(
        f"/fr/espace-reserve/guichet/{assigned_ticket.uuid}/reponse/",
        {"response-body": "Une réponse que je n’ai pas mandat d’écrire."},
    )
    assert response.status_code == 403
    assigned_ticket.refresh_from_db()
    assert assigned_ticket.status == TicketStatus.IN_REVIEW


def test_a_malformed_identifier_is_refused_and_never_crashes(client, reserved_area_on, operator):
    """
    A hand-typed probe gets the same refusal as a foreign identifier.

    ``filter(uuid=…)`` raises out of the field for anything that is not a UUID, which would reach the
    handler as a 500: a different answer for a malformed identifier than for a valid one that
    belongs to somebody else, and an invitation to keep probing.
    """
    login(client, operator)
    response = client.post("/fr/espace-reserve/guichet/designation/", {"ticket": "not-a-uuid"})
    assert response.status_code == 403


def test_an_account_with_the_right_but_without_the_mandate_cannot_file_a_note(
    client, reserved_area_on, assigned_ticket, superuser
):
    """
    ``accounts.permissions.can`` grants a superadmin every action, so the mandate check in the
    service is the one that refuses — and its refusal must read as a refusal, not as a server error.
    """
    superuser.set_password(PASSWORD)
    superuser.save(update_fields=["password"])
    login(client, superuser)
    response = client.post(
        f"/fr/espace-reserve/guichet/{assigned_ticket.uuid}/note/",
        {"note-body": "Une note que l’administration n’a pas mandat d’écrire."},
        follow=True,
    )
    assert response.status_code == 200
    assert assigned_ticket.messages.filter(visibility="internal").count() == 0
    assert "Seul le professionnel désigné" in response.content.decode()


def test_the_designation_register_renders_without_the_question(client, reserved_area_on, ticket, person_user, operator):
    """
    Asserted against the RENDERED PAGE, not against the queryset.

    The queryset defers ``question``, but a deferred field loads on access — so the deferral is
    minimisation and this assertion is the actual boundary.
    """
    services.request_professional_review(ticket, actor=person_user)
    login(client, operator)
    page = client.get("/fr/espace-reserve/guichet/designation/").content.decode()
    assert ticket.reference in page
    assert "dix-huit mois" not in page
    assert ticket.question[:30] not in page


def test_an_available_reply_does_not_also_say_the_step_is_out_of_the_persons_hands(
    client, reserved_area_on, assigned_ticket, professional
):
    """The page announced a reply and «cette étape ne dépend pas de vous» in the same breath."""
    services.publish_response(assigned_ticket, "Votre attestation reste recevable.", actor=professional)
    login(client, assigned_ticket.person)
    page = client.get(f"/fr/espace-reserve/guichet/{assigned_ticket.uuid}/").content.decode()
    assert "Réponse disponible" in page
    assert "ne dépend pas de vous" not in page


def test_a_request_waiting_for_a_professional_does_say_so(client, reserved_area_on, ticket, person_user):
    login(client, person_user)
    services.request_professional_review(ticket, actor=person_user)
    page = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode()
    assert "ne dépend pas de vous" in page


def test_a_get_never_changes_a_state(client, reserved_area_on, ticket, person_user):
    login(client, person_user)
    response = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/verification-professionnelle/")
    assert response.status_code == 405
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.INFORMATION_ONLY


def test_closing_is_final_and_the_page_says_so(client, reserved_area_on, ticket, person_user):
    login(client, person_user)
    client.post(
        f"/fr/espace-reserve/guichet/{ticket.uuid}/cloture/",
        {"close-reason": "J’ai trouvé la réponse dans la checklist."},
    )
    ticket.refresh_from_db()
    assert ticket.status == TicketStatus.CLOSED

    page = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode()
    assert "n’est pas rouverte" in page


# ---------------------------------------------------------------------------------------------
# The register renders the register, not cards
# ---------------------------------------------------------------------------------------------
def test_the_empty_register_is_a_hairline_and_a_sentence(client, reserved_area_on, person_user):
    login(client, person_user)
    page = client.get("/fr/espace-reserve/guichet/").content.decode()
    assert 'class="empty"' in page
    assert "empty-state__icon" not in page
    assert 'class="card' not in page


def test_the_register_lists_the_state_as_a_word(client, reserved_area_on, ticket, person_user):
    login(client, person_user)
    page = client.get("/fr/espace-reserve/guichet/").content.decode()
    assert 'class="register"' in page
    assert "Information seulement" in page
    assert ticket.reference in page


def test_the_page_shows_the_next_step_and_who_it_depends_on(client, reserved_area_on, ticket, person_user):
    services.request_professional_review(ticket, actor=person_user)
    login(client, person_user)
    page = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode()
    assert "Cette étape ne dépend pas de vous" in page
