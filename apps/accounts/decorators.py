"""
View decorators for the MFA policy. ``mfa_required_for_backoffice`` protects back-office-like views
that live outside ``/backoffice/`` (exports, moderation tools) with the same rules as the middleware:
enrol when the deployment requires a device, and present the second factor when the account holds one
that this session never presented (F-5).
"""

from __future__ import annotations

from functools import wraps

from accounts import services
from accounts.middleware import mfa_redirect, second_factor_redirect


def mfa_required_for_backoffice(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        due = services.second_factor_due(request, getattr(request, "user", None))
        if due == services.ENROL:
            return mfa_redirect(request)
        if due == services.PRESENT:
            return second_factor_redirect(request)
        return view_func(request, *args, **kwargs)

    return _wrapped
