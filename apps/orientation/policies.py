"""Object-level policies (deny by default) — imported from ``OrientationConfig.ready``."""

from __future__ import annotations

from accounts.permissions import policy
from orientation.models import OrientationResult, OrientationSession


@policy(OrientationSession)
def _session_policy(user, action: str, obj: OrientationSession) -> bool:
    if action in {"view", "change", "delete", "save"}:
        return bool(obj.user_id) and obj.user_id == user.id
    return False


@policy(OrientationResult)
def _result_policy(user, action: str, obj: OrientationResult) -> bool:
    return action == "view" and bool(obj.session.user_id) and obj.session.user_id == user.id
