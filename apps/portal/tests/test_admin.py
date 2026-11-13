"""Back-office of the reserved area: role-scoped access, e-mail designation, audit, data minimisation."""

from __future__ import annotations

import pytest

from accounts import roles
from audit.models import AuditEvent
from portal.models import Deadline, Message, PortalNotice

pytestmark = pytest.mark.django_db

MESSAGES = "/backoffice/portal/message/"
DEADLINES = "/backoffice/portal/deadline/"
NOTICES = "/backoffice/portal/portalnotice/"


def _message_payload(email, **extra):
    data = {
        "account_email": email,
        "subject": "Votre dossier",
        "body": "Bonjour,\nmerci de compléter votre dossier.",
        "visible_from_0": "",
        "visible_from_1": "",
        "content_type": "",
        "object_id": "",
    }
    data.update(extra)
    return data


def test_staff_creates_a_message_for_a_recipient_designated_by_email(client, seeded, staff_user, alice):
    client.force_login(staff_user)
    form = client.get(f"{MESSAGES}add/")
    assert form.status_code == 200
    html = form.content.decode()
    assert 'name="account_email"' in html
    assert 'name="recipient"' not in html, "no browsable list of accounts (data minimisation)"
    assert "Minimisation des données" in html
    assert alice.email not in html

    response = client.post(f"{MESSAGES}add/", _message_payload(alice.email.upper()))
    assert response.status_code == 302, response.content.decode()[:2000]
    message = Message.objects.get()
    assert message.recipient == alice and message.sender == staff_user and message.is_read is False

    event = AuditEvent.objects.get(action="portal.message.created")
    assert event.actor == staff_user and event.target_id == str(message.pk)
    assert event.metadata["recipient_id"] == alice.pk
    dumped = f"{event.metadata}{event.target_repr}"
    assert alice.email not in dumped and "compléter" not in dumped and "Votre dossier" not in dumped


def test_unknown_or_inactive_recipient_is_refused(client, seeded, staff_user, alice):
    client.force_login(staff_user)
    response = client.post(f"{MESSAGES}add/", _message_payload("nobody@example.test"))
    assert response.status_code == 200 and Message.objects.count() == 0
    assert "Aucun compte actif" in response.content.decode()
    alice.is_active = False
    alice.save(update_fields=["is_active"])
    response = client.post(f"{MESSAGES}add/", _message_payload(alice.email))
    assert response.status_code == 200 and Message.objects.count() == 0


def test_created_message_reaches_the_recipient_portal(client, seeded, staff_user, alice):
    client.force_login(staff_user)
    client.post(f"{MESSAGES}add/", _message_payload(alice.email, subject="Convocation du 5 octobre"))
    client.force_login(alice)
    assert "Convocation du 5 octobre" in client.get("/fr/espace-reserve/communications/").content.decode()


def test_changelist_filters_and_search_by_recipient_email(client, seeded, superuser, alice, bob, make_message):
    make_message(alice, subject="Pour Alice")
    make_message(bob, subject="Pour Bob")
    client.force_login(superuser)
    html = client.get(MESSAGES, {"q": "alice.alpha"}).content.decode()
    assert "Pour Alice" in html and "Pour Bob" not in html
    html = client.get(MESSAGES, {"is_read__exact": "1"}).content.decode()
    assert "Pour Alice" not in html and "Pour Bob" not in html


def test_staff_role_cannot_change_or_delete_a_sent_message(client, seeded, staff_user, alice, make_message):
    message = make_message(alice, subject="Objet initial")
    client.force_login(staff_user)
    view = client.get(f"{MESSAGES}{message.pk}/change/")
    assert view.status_code == 200
    assert 'name="subject"' not in view.content.decode(), "read-only for the staff role"
    client.post(f"{MESSAGES}{message.pk}/change/", {"subject": "Objet modifié", "body": "x"})
    message.refresh_from_db()
    assert message.subject == "Objet initial"


def test_administrator_can_correct_an_unread_message_but_never_the_recipient(
    client, seeded, user_factory, alice, bob, make_message
):
    administrator = user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)
    message = make_message(alice, subject="Objet initial")
    client.force_login(administrator)
    html = client.get(f"{MESSAGES}{message.pk}/change/").content.decode()
    assert 'name="subject"' in html and 'name="recipient"' not in html and 'name="account_email"' not in html
    response = client.post(
        f"{MESSAGES}{message.pk}/change/",
        {
            "subject": "Objet corrigé",
            "body": message.body,
            "visible_from_0": "",
            "visible_from_1": "",
            "content_type": "",
            "object_id": "",
            "recipient": bob.pk,
            "account_email": bob.email,
        },
    )
    assert response.status_code == 302, response.content.decode()[:2000]
    message.refresh_from_db()
    assert message.subject == "Objet corrigé" and message.recipient == alice
    assert AuditEvent.objects.filter(action="portal.message.changed", target_id=str(message.pk)).exists()


def test_read_message_is_frozen_even_for_administrators(client, seeded, superuser, alice, make_message):
    from portal import services

    message = make_message(alice, subject="Objet lu")
    services.mark_message_read(alice, message.pk)
    client.force_login(superuser)
    html = client.get(f"{MESSAGES}{message.pk}/change/").content.decode()
    assert 'name="subject"' not in html and 'name="body"' not in html


def test_deadline_admin_create_is_audited(client, seeded, staff_user, alice):
    client.force_login(staff_user)
    response = client.post(
        f"{DEADLINES}add/",
        {
            "account_email": alice.email,
            "title": "Dépôt des pièces",
            "due_on": "2026-11-15",
            "kind": "document",
            "status": "open",
            "description": "",
            "source_note": "Courrier du 01.10.2026",
        },
    )
    assert response.status_code == 302, response.content.decode()[:2000]
    deadline = Deadline.objects.get()
    assert deadline.owner == alice
    assert AuditEvent.objects.filter(action="portal.deadline.created", target_id=str(deadline.pk)).exists()
    assert client.get(f"{DEADLINES}{deadline.pk}/delete/").status_code == 403


def test_notice_admin_sets_author_and_keeps_draft(client, seeded, staff_user):
    client.force_login(staff_user)
    response = client.post(
        f"{NOTICES}add/",
        {
            "audience": "company",
            "heading_fr": "Information aux entreprises",
            "body_fr": "Texte de l’avis.",
            "order": "1",
            "status": "draft",
            "publish_at_0": "",
            "publish_at_1": "",
            "unpublish_at_0": "",
            "unpublish_at_1": "",
            "last_reviewed_at_0": "",
            "last_reviewed_at_1": "",
            "reviewer": "",
            "editorial_note": "",
        },
    )
    assert response.status_code == 302, response.content.decode()[:2000]
    notice = PortalNotice.objects.get(heading_fr="Information aux entreprises")
    assert notice.author == staff_user and notice.status == "draft"
    assert client.get(NOTICES).status_code == 200


def test_admin_classes_inherit_the_project_base():
    from django.contrib import admin

    from core.admin_base import BaseModelAdmin

    for model in (Message, Deadline, PortalNotice):
        assert isinstance(admin.site._registry[model], BaseModelAdmin)
