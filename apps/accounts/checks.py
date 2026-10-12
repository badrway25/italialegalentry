"""
Deployment checks (``manage.py check --deploy``) for the second-factor policy.

The name of the setting is historical. The policy is no longer about the back-office: it is about
RESPONSIBILITY. ``accounts.services.MFA_REQUIRED_ROLES`` covers everyone who can read another
person's case file — a professional, an authorised actor, an operator, the legal roles, editorial
and administration — and a professional holds no ``is_staff`` flag at all. Tying the second factor to
the admin URL protected the wrong door.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register

MIDDLEWARE_PATH = "accounts.middleware.BackofficeMFAMiddleware"
AUTH_MIDDLEWARE = "django.contrib.auth.middleware.AuthenticationMiddleware"


@register(Tags.security, deploy=True)
def check_backoffice_mfa(app_configs, **kwargs):
    problems = []
    enforced = bool(getattr(settings, "BACKOFFICE_MFA_ENFORCED", False))
    middleware = list(getattr(settings, "MIDDLEWARE", []))
    if not enforced:
        problems.append(
            Warning(
                "BACKOFFICE_MFA_ENFORCED is not true: accounts that can read another person's "
                "case file — professional, authorised actor, operator, legal, editorial, "
                "administration — can sign in with a password alone.",
                hint="Set BACKOFFICE_MFA_ENFORCED=1 in production, once staff have enrolled a TOTP device.",
                id="accounts.W001",
            )
        )
    if MIDDLEWARE_PATH not in middleware:
        problems.append(
            Error(
                "accounts.middleware.BackofficeMFAMiddleware is not installed.",
                hint=f"Add '{MIDDLEWARE_PATH}' after '{AUTH_MIDDLEWARE}' in MIDDLEWARE.",
                id="accounts.E001",
            )
        )
    elif AUTH_MIDDLEWARE in middleware and middleware.index(MIDDLEWARE_PATH) < middleware.index(AUTH_MIDDLEWARE):
        problems.append(
            Error(
                "BackofficeMFAMiddleware must come after AuthenticationMiddleware.",
                id="accounts.E002",
            )
        )
    return problems
