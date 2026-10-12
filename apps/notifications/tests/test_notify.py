"""
The notification service, tested at the domain level rather than through a screen.

Everything here asserts behaviour that must hold however the notification arrives — a view, the
admin, a management command or a future API — because a rule that only lives in one call site is
not a rule.
"""

from __future__ import annotations

import pytest
from django.conf import settings
from django.core import mail

from audit.models import AuditEvent
from notifications import events
from notifications import services as notifications
from notifications.models import (
    EmailOutbox,
    EmailSuppression,
    Notification,
    NotificationChannel,
    NotificationPreference,
)
from portal.models import Message
from portal.services import unread_count

pytestmark = pytest.mark.django_db


def context_for(event) -> dict:
    return {name: f"valeur-{name}" for name in event.fields}


def notify(person, key, **kwargs):
    return notifications.notify(person, key, context=context_for(events.get(key)), **kwargs)


# ---------------------------------------------------------------------------------------------
# Every event reaches the person
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("key", sorted(events.EVENTS))
def test_every_event_produces_an_in_app_notification(person, key):
    notification = notify(person, key)

    assert notification.pk is not None
    assert notification.event == key
    assert notification.recipient_id == person.pk
    assert notification.category == events.get(key).category
    assert notification.subject == str(events.get(key).subject_fr)
    assert notification.body.strip()


def test_the_in_app_record_is_the_portal_inbox(person):
    """
    One inbox, not two. The reserved area's own counter must see the notification.

    This is the whole reason this app attaches to ``portal.Message`` instead of owning a table that
    looks like it: a second inbox would mean a second list to read and a badge that is wrong by
    construction.
    """
    notification = notify(person, events.CASE_TRANSITIONED)

    assert Message.objects.inbox(person).count() == 1
    assert unread_count(person) == 1
    assert notification.message in Message.objects.inbox(person)
    assert notification.is_read is False


def test_the_related_object_is_linked_not_copied(person, case):
    notification = notify(person, events.CASE_TRANSITIONED, related=case)

    assert notification.related_object == case
    assert notification.message.object_id == str(case.pk)


def test_an_unknown_event_is_refused(person):
    with pytest.raises(events.UnknownEvent):
        notifications.notify(person, "case.invented", context={})


def test_a_body_that_cannot_be_filled_is_refused(person):
    """No half-rendered notification: a blank where the reference belongs looks like a broken site."""
    with pytest.raises(events.MissingContext):
        notifications.notify(person, events.CHECKLIST_OVERDUE, context={"requirement": "Passeport"})
    assert Notification.objects.count() == 0
    assert Message.objects.count() == 0


def test_the_text_is_rendered_in_the_recipients_language(person):
    """A night-time command has no language; a member of staff has the wrong one. The account decides."""
    person.preferred_language = "fr"
    person.save(update_fields=["preferred_language"])

    notification = notify(person, events.CHECKLIST_OVERDUE)

    assert "Dossier :" in notification.body


# ---------------------------------------------------------------------------------------------
# The e-mail decision follows the registry
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("key", sorted(events.EVENTS))
def test_the_email_decision_follows_the_registry(person, key):
    notification = notify(person, key)
    declared = events.get(key)

    if declared.email:
        assert notification.channel == NotificationChannel.IN_APP_AND_EMAIL
        assert notification.outbox is not None
        assert notification.email_suppressed == ""
    else:
        assert notification.channel == NotificationChannel.IN_APP
        assert notification.outbox is None
        assert notification.email_suppressed == EmailSuppression.NOT_BY_EMAIL


def test_an_event_without_email_queues_nothing(person):
    notify(person, events.CASE_OPENED)

    assert EmailOutbox.objects.count() == 0
    assert mail.outbox == []


def test_an_event_with_email_goes_through_the_outbox(person):
    notification = notify(person, events.DOCUMENT_REJECTED)

    item = EmailOutbox.objects.get()
    assert notification.outbox_id == item.pk
    assert item.to_email == person.email
    assert item.reference == f"notifications.Notification:{notification.pk}"
    assert notification.body.split("\n")[0] in item.body_text


# ---------------------------------------------------------------------------------------------
# Preferences: e-mail only
# ---------------------------------------------------------------------------------------------
def test_preferences_switch_off_the_email(person):
    notifications.set_email_preference(person, events.CATEGORY_DOCUMENT, enabled=False)

    notification = notify(person, events.DOCUMENT_EXPIRED)

    assert notification.channel == NotificationChannel.IN_APP
    assert notification.email_suppressed == EmailSuppression.PREFERENCE
    assert EmailOutbox.objects.count() == 0
    assert mail.outbox == []


def test_preferences_never_switch_off_the_record(person):
    """The in-app notification is the record that somebody was told. It has no off switch."""
    for category in events.CATEGORIES:
        notifications.set_email_preference(person, category, enabled=False)

    for key in events.EVENTS:
        notify(person, key)

    assert Notification.objects.for_recipient(person).count() == len(events.EVENTS)
    assert unread_count(person) == len(events.EVENTS)
    assert EmailOutbox.objects.count() == 0


def test_a_preference_is_per_category(person):
    notifications.set_email_preference(person, events.CATEGORY_DEADLINE, enabled=False)

    silenced = notify(person, events.CHECKLIST_OVERDUE)
    still_sent = notify(person, events.ASSIGNMENT_GRANTED)

    assert silenced.outbox is None
    assert still_sent.outbox is not None


def test_an_account_with_no_preference_row_receives_email(person):
    """Never configured is not the same as refused: the defaults are on."""
    assert not NotificationPreference.objects.filter(user=person).exists()

    assert notify(person, events.TEAM_MESSAGE).outbox is not None


def test_switching_a_preference_is_audited(person):
    notifications.set_email_preference(person, events.CATEGORY_CASE, enabled=False)

    event = AuditEvent.objects.get(action="notifications.preference")
    assert event.metadata["category"] == events.CATEGORY_CASE
    assert event.metadata["email"] is False


def test_an_unknown_category_cannot_be_configured(person):
    with pytest.raises(events.UnknownEvent):
        notifications.set_email_preference(person, "invented", enabled=False)


# ---------------------------------------------------------------------------------------------
# Idempotence
# ---------------------------------------------------------------------------------------------
def test_the_same_key_never_notifies_twice(person):
    first = notify(person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-02")
    second = notify(person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-02")

    assert first.pk == second.pk
    assert Notification.objects.count() == 1
    assert EmailOutbox.objects.count() == 1


def test_a_different_key_notifies_again(person):
    notify(person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-02")
    notify(person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-20")

    assert Notification.objects.count() == 2


def test_two_people_may_share_a_key(person, other_person):
    """Deduplication is per account: one person's warning must not silence another's."""
    notify(person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-02")
    notify(other_person, events.CHECKLIST_OVERDUE, dedupe_key="checklist.overdue:1:2026-10-02")

    assert Notification.objects.count() == 2


def test_an_event_without_a_key_may_repeat(person):
    """The équipe may write twice. Only declared states are deduplicated."""
    notify(person, events.TEAM_MESSAGE)
    notify(person, events.TEAM_MESSAGE)

    assert Notification.objects.count() == 2


# ---------------------------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------------------------
def test_every_notification_is_audited_without_personal_data(person):
    notification = notify(person, events.DOCUMENT_REJECTED)

    event = AuditEvent.objects.get(action="notifications.sent")
    assert event.metadata["event"] == events.DOCUMENT_REJECTED
    assert event.metadata["recipient_id"] == person.pk
    serialised = str(event.metadata) + event.target_repr
    assert person.email not in serialised
    assert notification.subject not in serialised
    assert "valeur-reason" not in serialised


# ---------------------------------------------------------------------------------------------
# Failure isolation
# ---------------------------------------------------------------------------------------------
def test_notify_quietly_swallows_a_failure(person):
    """A case file transition must not be lost because a notification could not be written."""
    assert notifications.notify_quietly(person, "case.invented", context={}) is None
    assert Notification.objects.count() == 0


def test_notify_quietly_returns_the_notification_when_it_works(person):
    notification = notifications.notify_quietly(
        person, events.CASE_OPENED, context=context_for(events.get(events.CASE_OPENED))
    )
    assert notification is not None
    assert Notification.objects.count() == 1


# ---------------------------------------------------------------------------------------------
# A message somebody wrote
# ---------------------------------------------------------------------------------------------
def test_a_staff_message_is_announced_without_being_written_twice(person, superuser):
    """
    The équipe's own message keeps its subject in the reserved area, and borrows the constant for
    the mail header. One row, not two — the person must not read the same thing twice.
    """
    from portal.services import send_message

    message = send_message(
        recipient=person,
        subject="Votre dossier — pièce manquante",
        body="Bonjour, il manque une pièce à votre dossier.",
        sender=superuser,
    )

    notification = notifications.notify_for_message(message)

    assert Message.objects.inbox(person).count() == 1
    assert notification.message_id == message.pk
    assert notification.subject == "Votre dossier — pièce manquante"
    assert notification.outbox.subject == (
        f"{settings.ACCOUNT_EMAIL_SUBJECT_PREFIX}{events.get(events.TEAM_MESSAGE).subject_fr}"
    )
    assert "pièce manquante" not in notification.outbox.subject


def test_announcing_the_same_message_twice_changes_nothing(person, superuser):
    from portal.services import send_message

    message = send_message(recipient=person, subject="Objet", body="Texte.", sender=superuser)

    first = notifications.notify_for_message(message)
    second = notifications.notify_for_message(message)

    assert first.pk == second.pk
    assert Notification.objects.count() == 1
    assert EmailOutbox.objects.count() == 1


def test_a_scheduled_message_is_not_announced_before_its_date(person, superuser):
    """A message the team chose to hold until a date is not announced by e-mail today."""
    from datetime import timedelta

    from core import clock
    from portal.services import send_message

    message = send_message(
        recipient=person,
        subject="Objet",
        body="Texte.",
        sender=superuser,
        visible_from=clock.now() + timedelta(days=3),
    )

    assert notifications.notify_for_message(message) is None
    assert Notification.objects.count() == 0
    assert mail.outbox == []
