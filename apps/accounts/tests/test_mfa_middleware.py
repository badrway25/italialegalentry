"""Back-office MFA policy: staff/superusers without TOTP are redirected to the activation page."""

from __future__ import annotations

import pytest
from allauth.mfa.models import Authenticator
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory, override_settings

from accounts import checks, services
from accounts.decorators import mfa_required_for_backoffice
from accounts.middleware import BackofficeMFAMiddleware

pytestmark = [pytest.mark.django_db, pytest.mark.security]

MFA_MIDDLEWARE = "accounts.middleware.BackofficeMFAMiddleware"
# The project settings install the middleware; the tests build both variants explicitly so they
# stay valid whatever the project configuration is.
MIDDLEWARE_WITHOUT_MFA = [m for m in settings.MIDDLEWARE if m != MFA_MIDDLEWARE]
MIDDLEWARE_WITH_MFA = [*MIDDLEWARE_WITHOUT_MFA]
MIDDLEWARE_WITH_MFA.insert(
    MIDDLEWARE_WITH_MFA.index("django.contrib.messages.middleware.MessageMiddleware") + 1,
    MFA_MIDDLEWARE,
)
TOTP_ACTIVATE = "/fr/compte/2fa/totp/activate/"


def _totp(user):
    return Authenticator.objects.create(user=user, type=Authenticator.Type.TOTP, data={"secret": "test"})


def _request(path, user):
    request = RequestFactory().get(path)
    SessionMiddleware(lambda r: HttpResponse()).process_request(request)
    request._messages = FallbackStorage(request)
    request.user = user
    return request


@override_settings(BACKOFFICE_MFA_ENFORCED=True)
def test_needs_backoffice_mfa(staff_user, superuser, person_user):
    assert services.needs_backoffice_mfa(staff_user)
    assert services.needs_backoffice_mfa(superuser)
    assert not services.needs_backoffice_mfa(person_user)
    assert not services.needs_backoffice_mfa(AnonymousUser())
    _totp(staff_user)
    assert not services.needs_backoffice_mfa(staff_user)
    assert services.has_active_totp(staff_user)


def test_not_enforced_by_default(staff_user):
    assert not services.backoffice_mfa_enforced()
    assert not services.needs_backoffice_mfa(staff_user)


@override_settings(BACKOFFICE_MFA_ENFORCED=True)
def test_middleware_redirects_staff_without_totp(staff_user, person_user):
    middleware = BackofficeMFAMiddleware(lambda r: HttpResponse("ok"))
    r = middleware(_request("/backoffice/", staff_user))
    assert r.status_code == 302 and r["Location"] == TOTP_ACTIVATE
    assert middleware(_request("/backoffice/logout/", staff_user)).status_code == 200
    assert middleware(_request("/fr/", staff_user)).status_code == 200
    assert middleware(_request("/backoffice/", person_user)).status_code == 200
    assert middleware(_request("/backoffice/", AnonymousUser())).status_code == 200
    _totp(staff_user)
    assert middleware(_request("/backoffice/", staff_user)).status_code == 200


@override_settings(BACKOFFICE_MFA_ENFORCED=True, MIDDLEWARE=MIDDLEWARE_WITH_MFA)
def test_middleware_integration_with_admin(client, staff_user):
    client.force_login(staff_user)
    r = client.get("/backoffice/")
    assert r.status_code == 302 and r["Location"] == TOTP_ACTIVATE
    r = client.get("/backoffice/logout/")
    assert r.status_code != 302 or r["Location"] != TOTP_ACTIVATE, "logout stays reachable"
    client.force_login(staff_user)
    _totp(staff_user)
    r = client.get("/backoffice/")
    assert r.status_code == 200


@override_settings(BACKOFFICE_MFA_ENFORCED=True)
def test_decorator(staff_user, person_user):
    view = mfa_required_for_backoffice(lambda request: HttpResponse("ok"))
    assert view(_request("/fr/export/", staff_user)).status_code == 302
    assert view(_request("/fr/export/", person_user)).status_code == 200


def test_deploy_checks():
    with override_settings(BACKOFFICE_MFA_ENFORCED=False, MIDDLEWARE=MIDDLEWARE_WITHOUT_MFA):
        ids = {p.id for p in checks.check_backoffice_mfa(None)}
        assert ids == {"accounts.W001", "accounts.E001"}
    with override_settings(BACKOFFICE_MFA_ENFORCED=True, MIDDLEWARE=MIDDLEWARE_WITH_MFA):
        assert checks.check_backoffice_mfa(None) == []
    with override_settings(BACKOFFICE_MFA_ENFORCED=True, MIDDLEWARE=[MFA_MIDDLEWARE, *MIDDLEWARE_WITHOUT_MFA]):
        assert {p.id for p in checks.check_backoffice_mfa(None)} == {"accounts.E002"}


def test_project_settings_install_the_middleware_in_the_right_place():
    middleware = list(settings.MIDDLEWARE)
    assert MFA_MIDDLEWARE in middleware
    assert middleware.index(MFA_MIDDLEWARE) > middleware.index(
        "django.contrib.auth.middleware.AuthenticationMiddleware"
    )
    assert middleware.index(MFA_MIDDLEWARE) > middleware.index("django.contrib.messages.middleware.MessageMiddleware")
