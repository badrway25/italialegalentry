"""
Object-level policies of the reserved area (deny by default — ``accounts.permissions``).

Superadmins pass through ``accounts.permissions.can`` before any policy is consulted.

Message      recipient: view + mark_read, only once the message is visible (``visible_from``)
             staff / administrator role: view (back-office); administrator: change, delete
Deadline     owner: view
             staff / administrator role: view, change; administrator: delete
PortalNotice any active account: view when the notice is live AND addressed to one of its audiences
             staff / administrator role: view, change; administrator: delete

The portal VIEWS are stricter than these policies on purpose: they are a *personal* space, so they
additionally require the row to belong to ``request.user`` (``portal.services.get_own_*``). A
back-office role therefore never reads somebody else's message through the portal (which would
also flip its read state); staff use the admin, where every access is role-checked and every
creation, change and deletion is audited (reading is not).
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from portal.models import Deadline, Message, PortalNotice

BACKOFFICE_VIEW_ROLES = (roles.STAFF, roles.ADMINISTRATOR)
BACKOFFICE_MANAGE_ROLES = (roles.ADMINISTRATOR,)

RECIPIENT_ACTIONS = frozenset({"view", "mark_read"})


def audiences_of(user) -> set[str]:
    """Notice audiences of an account: its account type plus every ``role:<audience>`` it holds."""
    from portal.models import NoticeAudience

    known = set(NoticeAudience.values) - {NoticeAudience.ALL}
    audiences = {NoticeAudience.ALL.value}
    account_type = getattr(user, "account_type", "")
    if account_type in known:
        audiences.add(account_type)
    for role in roles.roles_of(user):
        name = role.removeprefix("role:")
        if name in known:
            audiences.add(name)
    return audiences


@policy(Message)
def message_policy(user, action: str, obj: Message) -> bool:
    if obj.recipient_id == user.id and action in RECIPIENT_ACTIONS and obj.is_visible():
        return True
    if action == "view":
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(Deadline)
def deadline_policy(user, action: str, obj: Deadline) -> bool:
    if action == "view" and obj.owner_id == user.id:
        return True
    if action in {"view", "change"}:
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "delete":
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(PortalNotice)
def notice_policy(user, action: str, obj: PortalNotice) -> bool:
    if action == "view" and obj.is_live() and obj.audience in audiences_of(user):
        return True
    if action in {"view", "change"}:
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "delete":
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False
