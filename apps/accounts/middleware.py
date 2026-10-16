"""
The second-factor policy, enforced (REQUIREMENTS_MATRIX R-SEC-005, PERMISSION_MODEL L-10, F-5).

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
  version left open. Its documents are served by ``/documents/`` — language-neutral, mounted outside
  ``i18n_patterns`` (config/urls.py), where a reviewer reads and downloads another person's pieces — and that
  path belongs to the perimeter. It did not, although this paragraph already said a document was read here.

On both, an account the policy covers meets two rules (``services.second_factor_due``):

* **Enrol** — it holds no TOTP device and the deployment enforces the policy (``BACKOFFICE_MFA_ENFORCED``):
  it is sent to the activation page.
* **Present** (F-5) — it HOLDS a second factor, and THIS session never presented it: it is sent to allauth's
  MFA re-authentication, whatever the setting says. Asking only whether a device was enrolled let Django's own
  admin sign-in form — no MFA stage — open the back office on a password alone: enrolment proves that a device
  exists, not that the person at the keyboard has it. A session presented the factor when allauth's log of its
  authentication steps holds an ``mfa`` step completed with one of the account's own authenticators
  (``services.session_presented_second_factor``). allauth's sign-in writes that step for every enrolled
  account; a session without it was opened by another door.

The Present rule also covers allauth's pages that MANAGE the second factor (``/<lang>/compte/2fa/…``): turning
the device off, seeing or regenerating the recovery codes. allauth lets a signed-in session re-authenticate there
with the password alone — sound for a session that presented the factor at sign-in, and a way round it for one
that did not: turn the device off with the password, enrol another, walk in. The two pages where the factor is
PRESENTED (``reauthenticate/``, and ``authenticate/``, the sign-in stage) stay open, and enrolling stays open to
an account that holds nothing yet.

And allauth's own way round a middleware is closed (``forget_what_a_password_step_must_not_resume``): after a
re-authentication allauth RESUMES the POST it interrupted by calling the view itself, so no middleware runs on it.
A session that owes the factor resumes nothing on a password step.

Must be listed AFTER ``AuthenticationMiddleware`` (and allauth's ``AccountMiddleware``). Anonymous
visitors are left alone — they meet the login page first. Signing out always stays reachable, and so
does the TOTP activation page itself: an account that cannot leave and cannot enrol is an account that
is locked out by the very rule meant to protect it. The exemptions are the exact routes, never a fragment
found anywhere in a path: a back-office object id is a path, and ``/backoffice/<app>/<model>/1/2fa/change/``
must meet the rule like any other back-office address.
"""

from __future__ import annotations

import re

from allauth.account.internal.flows.reauthentication import STATE_SESSION_KEY as SUSPENDED_REQUEST_KEY
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext as _

from accounts import services

BACKOFFICE_PREFIX = "/backoffice/"

#: Path fragments that mark the authenticated platform, whatever the language prefix. Matched as a
#: fragment rather than a prefix because every reserved URL carries `/fr/`, `/it/`, `/en/` or `/ar/`
#: in front of it, and a rule that only knew one language would guard one quarter of the surface.
RESERVED_FRAGMENTS = ("/espace-reserve/",)

#: The reserved area's documents: their endpoints (upload, review, download, signed link) are language-neutral and
#: mounted outside it (config/urls.py), but what they serve is a person's pieces — the same perimeter.
DOCUMENTS_PREFIX = "/documents/"

#: The language prefix of a public route (``/fr``, ``/ar`` …; ``i18n_patterns``).
_LANGUAGE = r"/[a-z]{2}(?:-[a-z]+)?"

#: Signing out — allauth's page in every language, and the back office's own. Reachable always: leaving must
#: never sit behind the rule it escapes.
LEAVING = re.compile(rf"^(?:{_LANGUAGE}/compte/logout/|{re.escape(BACKOFFICE_PREFIX)}logout/)$")

#: allauth's second-factor pages. The activation page is one of them, and it is not under either guarded
#: perimeter, so the Enrol rule never meets it; it is named here anyway, because a redirect target that is safe
#: only by accident of where it happens to be mounted is one move away from a redirect loop.
SECOND_FACTOR_PAGES = re.compile(rf"^{_LANGUAGE}/compte/2fa/")

#: Among them, the two where the factor is PRESENTED: re-authentication inside a session, and the sign-in stage.
PRESENTING_PAGES = re.compile(rf"^{_LANGUAGE}/compte/2fa/(?:reauthenticate|authenticate)/$")

#: allauth's re-authentication by PASSWORD (``account_reauthenticate``): the step it records never presents the factor.
PASSWORD_REAUTHENTICATION = re.compile(rf"^{_LANGUAGE}/compte/reauthenticate/$")


def is_backoffice_path(path: str) -> bool:
    return path.startswith(BACKOFFICE_PREFIX)


def is_reserved_path(path: str) -> bool:
    return path.startswith(DOCUMENTS_PREFIX) or any(fragment in path for fragment in RESERVED_FRAGMENTS)


def is_leaving(path: str) -> bool:
    return bool(LEAVING.match(path))


def manages_second_factor(path: str) -> bool:
    """allauth's pages that change the second factor or reveal its fallbacks (not the two that ask for it)."""
    return bool(SECOND_FACTOR_PAGES.match(path)) and not PRESENTING_PAGES.match(path)


def mfa_redirect(request):
    """Enrol: the account holds no TOTP device and the deployment requires one."""
    messages.warning(
        request,
        _(
            "Votre rôle donne accès au dossier d’autres personnes : l’authentification à deux "
            "facteurs (TOTP) doit être activée avant de continuer."
        ),
        fail_silently=True,  # ordering relative to MessageMiddleware must never break the redirect
    )
    return redirect(reverse("mfa_activate_totp"))


def second_factor_redirect(request, next_url: str | None = None):
    """
    Present: the account holds a second factor this session never presented — allauth's MFA re-authentication,
    then back. ``next`` is this site's own path (allauth checks it again before following it); allauth's page
    rate-limits the attempts (``reauthenticate`` per account, and the failed codes on the account's key).
    """
    target = next_url or request.get_full_path()
    return redirect(f"{reverse('mfa_reauthenticate')}?{urlencode({REDIRECT_FIELD_NAME: target})}")


def second_factor_response(request):
    """The redirect the policy owes this request, or ``None`` to let it through."""
    path = request.path
    if is_leaving(path):
        return None
    guarded = is_backoffice_path(path) or is_reserved_path(path)
    if not (guarded or manages_second_factor(path)):
        return None
    user = getattr(request, "user", None)
    due = services.second_factor_due(request, user) if guarded else None
    if due == services.ENROL:
        return mfa_redirect(request)
    if due == services.PRESENT or (not guarded and services.needs_second_factor_in_session(request, user)):
        return second_factor_redirect(request)
    return None


def forget_what_a_password_step_must_not_resume(request) -> None:
    """
    On allauth's password re-authentication, drop the request allauth suspended if this session owes the factor.

    When a page asks for a recent sign-in, allauth keeps the POST it interrupted in the session
    (``account_reauthentication_state``) and, once the session has re-authenticated, RESUMES it by calling the view
    function itself (``resume_request``): no middleware runs on that call, this one included. A POST kept while the
    account held nothing would then run after a mere password on a page the Present rule holds since — the session of
    somebody who knows the password, opened before the owner enrolled, regenerated the owner's recovery codes (the
    sec-f5 review, finding 1). A password step never presents the factor, so a session that owes it has nothing to
    resume there: the suspended request is dropped before allauth reads it. allauth still records the step and sends
    the session on to ``next``, where the rule meets it like any other request. The MFA re-authentication page checks
    and records the code before it resumes anything: what it resumes runs for a session that has just presented the
    factor. A session that owes nothing keeps allauth's resumption, unchanged.
    """
    if not PASSWORD_REAUTHENTICATION.match(request.path):
        return
    session = getattr(request, "session", None)
    if session is None or SUSPENDED_REQUEST_KEY not in session:
        return
    if services.needs_second_factor_in_session(request, getattr(request, "user", None)):
        del session[SUSPENDED_REQUEST_KEY]


class BackofficeMFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forget_what_a_password_step_must_not_resume(request)
        response = second_factor_response(request)
        if response is not None:
            return response
        return self.get_response(request)

    @staticmethod
    def must_redirect(request) -> bool:
        return second_factor_response(request) is not None
