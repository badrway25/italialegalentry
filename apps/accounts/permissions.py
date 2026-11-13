"""
Object-level authorisation — DENY BY DEFAULT.

``can(user, action, obj)`` looks up a policy registered for ``type(obj)``; if none exists the
answer is False. Domain apps register their policies at import time::

    from accounts.permissions import policy

    @policy(CompanyNeedsRequest)
    def _company_needs(user, action, obj):
        return action == "view" and obj.owner_id == user.id

``require(user, action, obj)`` raises PermissionDenied so views stay thin.
"""

from __future__ import annotations

from collections.abc import Callable

from django.core.exceptions import PermissionDenied

from accounts import roles

Policy = Callable[[object, str, object], bool]
_POLICIES: dict[type, Policy] = {}


def policy(model: type):
    def decorator(func: Policy) -> Policy:
        _POLICIES[model] = func
        return func

    return decorator


def can(user, action: str, obj) -> bool:
    if user is None or not getattr(user, "is_authenticated", False) or not user.is_active:
        return False
    if roles.is_superadmin(user):
        return True
    for klass in type(obj).__mro__:
        func = _POLICIES.get(klass)
        if func is not None:
            return bool(func(user, action, obj))
    return False


def require(user, action: str, obj) -> None:
    if not can(user, action, obj):
        raise PermissionDenied


def owns(user, obj, attr: str = "owner_id") -> bool:
    return getattr(obj, attr, None) == getattr(user, "id", None)


def member_of(user, organisation_id) -> bool:
    if not organisation_id or not getattr(user, "is_authenticated", False):
        return False
    return user.memberships.filter(organisation_id=organisation_id).exists()
