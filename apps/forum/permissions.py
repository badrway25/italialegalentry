"""Object-level policies (deny by default) for Forum records."""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from forum.models import ForumRegistration


@policy(ForumRegistration)
def _registration_policy(user, action: str, obj: ForumRegistration) -> bool:
    if roles.has_role(user, roles.ADMINISTRATOR):
        return action in {"view", "change", "delete"}
    if roles.has_role(user, roles.STAFF):
        return action in {"view", "change"}
    # A registrant sees only their own registration (linked account or same verified e-mail).
    if action != "view":
        return False
    if obj.user_id and obj.user_id == user.id:
        return True
    return bool(obj.email) and obj.email.lower() == (user.email or "").lower() and not obj.is_anonymised
