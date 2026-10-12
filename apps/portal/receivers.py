"""
Signal receivers and personal-data hooks of the reserved area.

* ``on_user_anonymised`` — GDPR art. 17: when an account is anonymised, the messages addressed to it
  and its deadlines are deleted (they are free text written about that person). Idempotent.
* ``portal_export_section`` — GDPR art. 15/20: the account's own messages and deadlines are added to
  the personal-data export of ``accounts.services.export_user_data``. The export is COMPLETE: it
  also contains the communications scheduled for later (``visible_from`` in the future). They are
  hidden from the portal pages until their date, but they are personal data already held about the
  person, so a right-of-access copy that left them out would be incomplete.
"""

from __future__ import annotations

import logging

from audit.services import record as audit_record
from portal.models import Deadline, Message

log = logging.getLogger("ile.portal")


def on_user_anonymised(sender, *, user_id, **kwargs) -> None:
    messages, _ = Message.objects.filter(recipient_id=user_id).delete()
    deadlines, _ = Deadline.objects.filter(owner_id=user_id).delete()
    # Staff accounts: keep the messages they wrote, drop the link to the scrubbed account.
    Message.objects.filter(sender_id=user_id).update(sender=None)
    if messages or deadlines:
        audit_record(
            None,
            action="portal.account_data_erased",
            metadata={"user_id": user_id, "messages": messages, "deadlines": deadlines},
        )


def portal_export_section(user) -> dict:
    return {
        "messages": [
            {
                "id": str(m.pk),
                "subject": m.subject,
                "body": m.body,
                "received_at": m.created_at,
                "visible_from": m.visible_from,
                "is_read": m.is_read,
                "read_at": m.read_at,
            }
            # for_recipient — NOT inbox(): the inbox hides scheduled messages, the export must not.
            for m in Message.objects.for_recipient(user).order_by("-created_at")
        ],
        "deadlines": [
            {
                "title": d.title,
                "due_on": d.due_on,
                "kind": d.kind,
                "status": d.status,
                "description": d.description,
                "source_note": d.source_note,
            }
            for d in Deadline.objects.for_owner(user)
        ],
    }
