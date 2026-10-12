"""
Object-level policies of the digital help desk (deny by default — ``accounts.permissions``).

The querysets in ``helpdesk.models`` are the primary defence: they keep unauthorised rows out of
lists, counts and detail lookups, so nobody learns that a request exists. These policies are the
second defence, for one object already in hand.

HelpdeskTicket   person:          view; change while the request is open
                 live assignee:   view; change while the request is open
                 operator:        dispatch only — NOT view, NOT read
                 administrator:   view and dispatch; never ``respond``
TicketMessage    person:          view when the message is shared
                 live assignee:   view, shared and internal alike
                 nobody else

Two refusals are deliberate and are the substance of the module:

* An **operator** may assign a request to a professional and may not read it. Choosing who should
  look at a legal question does not require reading the question, and the narrower right is the one
  the task actually needs.
* An **administrator** may never ``respond``. Answering is a professional act performed under a
  mandate; an account whose power comes from configuring the platform has no mandate, and the
  platform must not be able to speak in a professional's place. ``accounts.permissions.can`` grants
  a superadmin everything by construction, which is why the response path is guarded a second time
  in ``services.publish_response`` by the live-mandate check — a right is not a mandate.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from helpdesk.models import HelpdeskTicket, MessageVisibility, TicketMessage

DISPATCH_ROLES = (roles.OPERATOR, roles.ADMINISTRATOR)


@policy(HelpdeskTicket)
def ticket_policy(user, action: str, obj: HelpdeskTicket) -> bool:
    if obj.person_id == user.id:
        if action == "view":
            return True
        if action == "change":
            # Writing a message, or asking for a human.
            return not obj.is_read_only
        return False

    if obj.assignee_id == user.id and obj.mandate_is_live:
        if action in {"view", "read_internal"}:
            return True
        if action in {"change", "respond"}:
            return not obj.is_read_only
        return False

    if action == "dispatch":
        return roles.has_role(user, *DISPATCH_ROLES) and not obj.is_read_only
    if action == "view":
        return roles.has_role(user, roles.ADMINISTRATOR)
    return False


@policy(TicketMessage)
def message_policy(user, action: str, obj: TicketMessage) -> bool:
    # A message is written evidence of an exchange: nobody edits or deletes one. A correction is a
    # further message, so the record of what was actually said on a given date stays intact.
    if action != "view":
        return False
    ticket = obj.ticket
    if ticket.person_id == user.id:
        return obj.visibility == MessageVisibility.SHARED
    return ticket.assignee_id == user.id and ticket.mandate_is_live
