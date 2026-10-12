"""
A communication that was notified must still be deletable in the back office.

`notifications.Notification` hangs off `portal.Message` by a `OneToOneField` with `CASCADE`, so
every message the platform announces acquires a companion row. Django's admin refuses a deletion
whose cascade reaches a registered model the account may not delete — and it refuses it with a bare
403, no missing button, no message. The effect was that an administrator could delete a message
nobody had been notified about, and nothing else.

Found by `test_audit_rows_never_contain_the_subject_title_or_body`, which asserts the deletion
succeeds; it began failing when the notifications app attached itself to the inbox.
"""

from __future__ import annotations

import pytest

from accounts import roles
from audit.models import AuditEvent
from notifications.models import Notification
from portal import services
from portal.models import Message
from portal.tests.conftest import *  # noqa: F401,F403 — seeded, alice, private media root

ADMIN_MESSAGES = "/backoffice/portal/message/"
ADMIN_NOTIFICATIONS = "/backoffice/notifications/notification/"


@pytest.fixture
def administrator(user_factory):
    return user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)


def _notified_message(alice, staff_user):
    """An ordinary staff communication. The companion row is not arranged here: sending makes it."""
    message = services.send_message(recipient=alice, sender=staff_user, subject="Objet", body="Corps")
    assert Notification.objects.filter(message=message).exists(), "send_message no longer notifies"
    return message


def test_an_administrator_can_delete_a_message_that_carries_a_notification(
    client, seeded, alice, staff_user, administrator
):
    message = _notified_message(alice, staff_user)
    client.force_login(administrator)
    response = client.post(f"{ADMIN_MESSAGES}{message.pk}/delete/", {"post": "yes"})
    assert response.status_code == 302, "403 here means the cascade needs a permission nobody holds"
    assert not Message.objects.filter(pk=message.pk).exists()
    assert not Notification.objects.filter(message_id=message.pk).exists()


def test_the_delete_page_of_a_notified_message_is_reachable(client, seeded, alice, staff_user, administrator):
    """The confirmation page raises the same 403 as the POST, so it is worth asserting separately."""
    message = _notified_message(alice, staff_user)
    client.force_login(administrator)
    assert client.get(f"{ADMIN_MESSAGES}{message.pk}/delete/").status_code == 200


def test_staff_still_cannot_delete_a_message(client, seeded, alice, staff_user):
    """The grant went to administrators. It must not have widened the role below them."""
    message = _notified_message(alice, staff_user)
    client.force_login(staff_user)
    assert client.post(f"{ADMIN_MESSAGES}{message.pk}/delete/", {"post": "yes"}).status_code == 403
    assert Message.objects.filter(pk=message.pk).exists()


def test_deleting_a_notification_on_its_own_page_is_audited(client, seeded, alice, staff_user, administrator):
    """Erasing the record that somebody was told something leaves a record of the erasure."""
    message = _notified_message(alice, staff_user)
    notification = Notification.objects.get(message=message)
    client.force_login(administrator)
    assert client.post(f"{ADMIN_NOTIFICATIONS}{notification.pk}/delete/", {"post": "yes"}).status_code == 302
    assert not Notification.objects.filter(pk=notification.pk).exists()
    assert Message.objects.filter(pk=message.pk).exists(), "the companion goes, the communication stays"
    events = AuditEvent.objects.filter(action="notifications.notification.deleted")
    assert events.count() == 1
    dumped = f"{events.get().target_repr} {events.get().metadata}"
    assert alice.email not in dumped


def test_no_role_may_delete_an_outbox_row(client, seeded, administrator):
    """The outbox is the record of what was actually sent. The grant stopped short of it."""
    assert not administrator.has_perm("notifications.delete_emailoutbox")
    assert administrator.has_perm("notifications.delete_notification")
