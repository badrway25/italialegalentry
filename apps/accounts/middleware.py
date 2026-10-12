"""
The second-factor policy, enforced (REQUIREMENTS_MATRIX R-SEC-005, PERMISSION_MODEL L-10).

The class name is historical and the setting's name with it. The policy is no longer about the
back-office: it is about RESPONSIBILITY. ``accounts.services.MFA_REQUIRED_ROLES`` names everyone who
can read another person's case file — a professional, an authorised actor, an operator, the legal
roles, editorial and administration — and a professional holds no ``is_staff`` flag at all and never
opens ``/backoffice/``.

Widening the policy without widening the enforcement would have been worse than leaving both narrow:
``needs_backoffice_mfa`` would have answered "yes, this account must enrol" and nothing would have
asked. A policy with no enforcement point is a comment.

So two perimeters are guarded, and they are guarded for different reasons:

* ``/backoffice/`` — the administration surface. Anyone who reaches it can change configuration.
* the reserved area (``/espace-reserve/`` and the platform modules mounted under it) — where a
  case file, a document and a person's legal situation are read. This is the perimeter the previous
  version left open.

Must be listed AFTER ``AuthenticationMiddleware`` (and allauth's ``AccountMiddleware``). Anonymous
visitors are left alone — they meet the login page first. Logout always stays reachable, and so does
the TOTP activation page itself: an account that cannot leave and cannot enrol is an account that is
locked out by the very rule meant to protect it.
"""

from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts import services

BACKOFFICE_PREFIX = "/backoffice/"

#: Path fragments that mark the authenticated platform, whatever the language prefix. Matched as a
#: fragment rather than a prefix because every reserved URL carries `/fr/`, `/it/`, `/en/` or `/ar/`
#: in front of it, and a rule that only knew one language would guard one quarter of the surface.
RESERVED_FRAGMENTS = ("/espace-reserve/",)

#: Reachable without a second factor, always. Leaving and enrolling must never sit behind the rule
#: they exist to satisfy.
#:
#: The enrolment page itself (``/<lang>/compte/2fa/totp/activate/``) is not under either guarded
#: perimeter, so it is already reachable; it is named here anyway, because a redirect target that is
#: safe only by accident of where it happens to be mounted is one move away from a redirect loop.
EXEMPT_FRAGMENTS = ("/logout/", "/2fa/", "/compte/logout/")


def is_backoffice_path(path: str) -> bool:
    return path.startswith(BACKOFFICE_PREFIX)


def is_reserved_path(path: str) -> bool:
    return any(fragment in path for fragment in RESERVED_FRAGMENTS)


def is_exempt(path: str) -> bool:
    return any(fragment in path for fragment in EXEMPT_FRAGMENTS)


def mfa_redirect(request):
    messages.warning(
        request,
        _(
            "Votre rôle donne accès au dossier d’autres personnes : l’authentification à deux "
            "facteurs (TOTP) doit être activée avant de continuer."
        ),
        fail_silently=True,  # ordering relative to MessageMiddleware must never break the redirect
    )
    return redirect(reverse("mfa_activate_totp"))


class BackofficeMFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.must_redirect(request):
            return mfa_redirect(request)
        return self.get_response(request)

    @staticmethod
    def must_redirect(request) -> bool:
        path = request.path
        if is_exempt(path):
            return False
        if not (is_backoffice_path(path) or is_reserved_path(path)):
            return False
        return services.needs_backoffice_mfa(getattr(request, "user", None))
