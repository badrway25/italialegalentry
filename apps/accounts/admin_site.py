"""
The back office's admin site: django-unfold's, with Django's own sign-in form closed (F-5).

``/backoffice/login/`` was Django's admin sign-in — ``LoginView`` with the admin's authentication form. It
signs an account in on its password alone: no MFA stage, and no rate limit either (allauth's ``login_failed``
limits apply to allauth's form only). With ``BACKOFFICE_MFA_ENFORCED=True``, an account that HAD a TOTP device
reached the back office through it with the password alone (the DevOps lane's F-5, checklist A-13).

Staff sign in where everyone signs in: allauth's page, whose sign-in runs the MFA stage for every account that
holds a second factor, with allauth's rate limits and the audit trail of every sign-in. This site's ``login``
authenticates no one any more, whatever it is sent: it never reads the request body, never calls
``authenticate`` and never calls ``login``.

* signed out → allauth's sign-in, ``next`` = the back-office page asked for, if it is one (``backoffice_next``);
* signed in, an active staff account → the page asked for, or first the second factor
  (``services.second_factor_due``: enrol, or present the one the account holds);
* signed in, anything else → 403: neither a sign-in form for another account nor a redirect that could loop.

And the site keeps the policy itself (``has_permission``), not only the middleware in front of it: the
middleware recognises the back office by its path, and a site remounted under another path would have taken
its doors with it. Signing out stays open whatever the policy asks.

Installed as the default admin site by ``accounts.admin_apps.BackofficeAdminConfig`` (INSTALLED_APPS, in place of
``django.contrib.admin``, with unfold's ``BasicAppConfig``, which leaves the default site alone).
"""

from __future__ import annotations

from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlencode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from unfold.sites import UnfoldAdminSite

from accounts import services
from accounts.middleware import mfa_redirect, second_factor_redirect


def backoffice_next(request, index: str) -> str:
    """
    Where the visitor was going, when that is a page of this back office on this site; ``index`` otherwise.

    Never an open redirect: Django's own test of the address first (``url_has_allowed_host_and_scheme``, which
    refuses another host, another scheme, ``//host``, ``///host``, ``\\host`` and control characters), then a
    path under the back office's own index, with neither scheme nor host. Read from the query string only — the
    form this view replaced put its ``next`` there too — so this view never reads a request body.
    """
    candidate = request.GET.get(REDIRECT_FIELD_NAME, "")
    if not candidate or not url_has_allowed_host_and_scheme(
        candidate, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return index
    parts = urlsplit(candidate)
    if parts.scheme or parts.netloc or not parts.path.startswith(index):
        return index
    return candidate


class BackofficeAdminSite(UnfoldAdminSite):
    """django-unfold's admin site, signing no one in and keeping the second-factor policy itself (F-5)."""

    def has_permission(self, request) -> bool:
        if not super().has_permission(request):
            return False
        if request.path == reverse("admin:logout", current_app=self.name):
            return True  # leaving never sits behind the rule it escapes
        return services.second_factor_due(request, request.user) is None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        index = reverse("admin:index", current_app=self.name)
        target = backoffice_next(request, index)
        user = request.user
        if not user.is_authenticated:
            sign_in = resolve_url(settings.LOGIN_URL)
            return HttpResponseRedirect(f"{sign_in}?{urlencode({REDIRECT_FIELD_NAME: target})}")
        if not super().has_permission(request):
            raise PermissionDenied
        due = services.second_factor_due(request, user)
        if due == services.ENROL:
            return mfa_redirect(request)
        if due == services.PRESENT:
            return second_factor_redirect(request, target)
        return HttpResponseRedirect(target)
