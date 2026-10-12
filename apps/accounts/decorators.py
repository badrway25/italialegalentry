"""
View decorators for the MFA policy. ``mfa_required_for_backoffice`` protects back-office-like views
that live outside ``/backoffice/`` (exports, moderation tools) with the same rule as the middleware.
"""

from __future__ import annotations

from functools import wraps

from accounts import services
from accounts.middleware import mfa_redirect


def mfa_required_for_backoffice(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if services.needs_backoffice_mfa(getattr(request, "user", None)):
            return mfa_redirect(request)
        return view_func(request, *args, **kwargs)

    return _wrapped
