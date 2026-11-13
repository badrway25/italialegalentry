"""
The safety properties of outgoing notification mail.

Three of them, and none is theoretical: subjects that carry personal data end up in mail server
logs and on lock screens; an address taken from a caller ends up delivering somebody's file to a
third party; and a test suite that can reach a real SMTP server eventually does, usually on the day
someone copies a production ``.env`` into a local shell.
"""

from __future__ import annotations

import inspect

import pytest
from django.conf import settings
from django.core import mail

from notifications import events
from notifications import services as notifications
from notifications.models import EmailOutbox, EmailSuppression

pytestmark = pytest.mark.django_db

#: Strings a notification must never put in a subject, in the shape they actually arrive in.
PERSONAL = {
    "name": "Amina Bensalah",
    "document": "passeport_amina_bensalah_2024.pdf",
    "passport": "AB1234567",
}


# ---------------------------------------------------------------------------------------------
# Nothing leaves through a real mail server under test
# ---------------------------------------------------------------------------------------------
def test_the_test_settings_use_an_in_memory_backend():
    assert settings.EMAIL_BACKEND == "django.core.mail.backends.locmem.EmailBackend"
    assert mail.get_connection().__class__.__module__.endswith("locmem")


def test_deliver_never_reaches_a_live_smtp_backend(person, monkeypatch):
    """
    Wire the SMTP backend to explode, then exercise the whole path that sends mail.

    Asserting that the setting says "locmem" only proves what the file says. Making the real backend
    fatal proves that nothing in this app opens one — neither ``notify``, nor ``queue_email``'s
    immediate delivery, nor ``send_pending``.
    """
    from django.core.mail.backends import smtp

    def explode(*args, **kwargs):  # pragma: no cover - the point is that it is never called
        raise AssertionError("a live SMTP backend was opened under test settings")

    monkeypatch.setattr(smtp.EmailBackend, "open", explode)
    monkeypatch.setattr(smtp.EmailBackend, "send_messages", explode)

    notifications.notify(
        person,
        events.DOCUMENT_REJECTED,
        context={"case_reference": "AB12CD34EF", "requirement": "Passeport", "reason": "illisible"},
    )
    notifications.send_pending()

    assert len(mail.outbox) == 1
    assert EmailOutbox.objects.get().status == "sent"


# ---------------------------------------------------------------------------------------------
# One address: the account's own
# ---------------------------------------------------------------------------------------------
def test_notify_cannot_be_given_an_address():
    """
    There is no address parameter, so no caller can redirect a person's mail to a third party.

    The address is resolved from the account inside the service. A signature is a cheap thing to
    assert and an expensive thing to get wrong.
    """
    parameters = set(inspect.signature(notifications.notify).parameters)
    assert not parameters & {"to_email", "to", "email", "address", "recipients"}


def test_mail_goes_to_the_account_and_nowhere_else(person, other_person):
    notification = notifications.notify(
        person,
        events.TEAM_MESSAGE,
        context={"body": "Votre dossier a été mis à jour."},
    )

    assert notification.outbox.to_email == person.email
    assert mail.outbox[0].to == [person.email]
    assert other_person.email not in mail.outbox[0].to
    assert mail.outbox[0].cc == []
    assert mail.outbox[0].bcc == []


def test_an_anonymised_account_is_never_written_to(person):
    """
    ``anonymise_user`` rewrites the address to a domain that does not exist.

    Mail to it bounces out of the platform carrying the subject of a notification about somebody who
    asked to be erased. The in-app record is still written: it is the record.
    """
    from accounts.services import ANONYMISED_DOMAIN

    person.email = f"anonymised-{person.pk}@{ANONYMISED_DOMAIN}"
    person.save(update_fields=["email"])

    notification = notifications.notify(person, events.TEAM_MESSAGE, context={"body": "Bonjour."})

    assert notification.outbox is None
    assert notification.email_suppressed == EmailSuppression.ANONYMISED
    assert mail.outbox == []


def test_a_deactivated_account_is_never_written_to(person):
    person.is_active = False
    person.save(update_fields=["is_active"])

    notification = notifications.notify(person, events.TEAM_MESSAGE, context={"body": "Bonjour."})

    assert notification.email_suppressed == EmailSuppression.INACTIVE
    assert mail.outbox == []


def test_the_look_alike_domain_is_never_written_to(person):
    """``ILE["FORBIDDEN_EMAIL_DOMAIN"]`` is not operated by the project. Nothing is sent to it."""
    person.email = f"personne@{settings.ILE['FORBIDDEN_EMAIL_DOMAIN']}"
    person.save(update_fields=["email"])

    notification = notifications.notify(person, events.TEAM_MESSAGE, context={"body": "Bonjour."})

    assert notification.outbox is None
    assert notification.email_suppressed == EmailSuppression.FORBIDDEN_DOMAIN
    assert mail.outbox == []


def test_a_notification_is_never_dressed_up_as_a_person_who_wrote(person, professional, superuser):
    """
    ``Message.sender`` means « l'équipe ». A mandated professional is not the équipe, and a scan is
    nobody: both are recorded as system-generated rather than signed with somebody's account.
    """
    from_professional = notifications.notify(
        person, events.TEAM_MESSAGE, context={"body": "Bonjour."}, sender=professional
    )
    from_staff = notifications.notify(person, events.TEAM_MESSAGE, context={"body": "Bonjour."}, sender=superuser)

    assert from_professional.message.sender is None
    assert from_staff.message.sender == superuser


# ---------------------------------------------------------------------------------------------
# Subjects
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("key", sorted(events.EVENTS))
def test_no_personal_data_reaches_a_subject(person, key):
    """
    Feed every declared event a context full of the worst possible strings, end to end.

    Subjects travel between servers in the clear and land on lock screens. The body may name the
    requirement — it reaches the account's own inbox and the reserved area — but the subject says
    only what kind of thing happened.
    """
    declared = events.get(key)
    context = dict.fromkeys(declared.fields, PERSONAL["document"])

    notification = notifications.notify(person, key, context=context)

    subjects = [notification.subject]
    if notification.outbox:
        subjects.append(notification.outbox.subject)
    subjects.extend(message.subject for message in mail.outbox)
    for subject in subjects:
        for value in (*PERSONAL.values(), person.email, str(person.pk)):
            assert value not in subject, f"{key}: {value!r} leaked into {subject!r}"


def test_the_subject_is_the_registry_constant_prefixed_by_the_project(person):
    notification = notifications.notify(person, events.TEAM_MESSAGE, context={"body": PERSONAL["name"]})

    declared = events.get(events.TEAM_MESSAGE)
    assert notification.subject == str(declared.subject_fr)
    assert notification.outbox.subject == f"{settings.ACCOUNT_EMAIL_SUBJECT_PREFIX}{declared.subject_fr}"
    # The detail is in the body, where it belongs — not lost, just not in a header.
    assert PERSONAL["name"] in notification.body
