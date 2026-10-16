"""
F-5 — the back office must open only to a session that presented its second factor.

Found by the DevOps lane (docs/design-v5/QA/v54/devops/NOTES.md, F-5; checklist A-13): with
``BACKOFFICE_MFA_ENFORCED=True``, an account WITH a TOTP authenticator reached ``/backoffice/`` on its
password alone, through Django's own admin sign-in form (``/backoffice/login/``, the unfold site's login
view). That form is not allauth's: it has no MFA stage. And ``BackofficeMFAMiddleware`` asked whether a
device was *enrolled*, never whether *this session* had used it.

The fix, in depth (docs/design-v5/QA/v54/sec-f5/NOTES.md):

* the back office's own sign-in authenticates no one — it sends the visitor to allauth's page, whose sign-in
  runs the MFA stage (``accounts.admin_site``);
* an account the policy covers that HOLDS a second factor is let in only if THIS session presented it —
  allauth's MFA step with one of the account's own authenticators, at sign-in or at re-authentication, or the
  activation of a device the session enrolled — at the middleware (``/backoffice/``, the reserved area and the
  ``/documents/`` endpoints that serve its pieces), at the admin site itself, and on allauth's pages that manage
  the factor (``accounts.services.second_factor_due``);
* enrolment stays what it was: required when the deployment enforces it, for the accounts that hold nothing;
* allauth's resumption of a request it suspended — it calls the view itself, past every middleware — runs nothing
  after a password re-authentication for a session that owes the factor (the sec-f5 review, finding 1).

Every test creates its own accounts with the test-only password of ``user_factory``; no real page is ever
driven and no password is stored anywhere but the test database. TOTP codes are real (allauth's own HOTP over
the secret) on a pinned time step, so a code never expires between its computation and its check.
"""

from __future__ import annotations

import importlib
import re
import time
import uuid
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from allauth.account.internal.flows.login import AUTHENTICATION_METHODS_SESSION_KEY
from allauth.account.internal.flows.reauthentication import STATE_SESSION_KEY as SUSPENDED_REQUEST_KEY
from allauth.account.models import EmailAddress
from allauth.mfa.models import Authenticator
from allauth.mfa.recovery_codes.internal.auth import RecoveryCodes
from allauth.mfa.totp.internal import auth as totp_auth
from django.conf import settings as django_settings
from django.test import RequestFactory, override_settings

from accounts import roles
from accounts.middleware import (
    PASSWORD_REAUTHENTICATION,
    BackofficeMFAMiddleware,
    forget_what_a_password_step_must_not_resume,
    manages_second_factor,
    second_factor_response,
)

pytestmark = [pytest.mark.django_db, pytest.mark.security]

#: ``user_factory``'s test-only default password (tests/conftest.py).
PASSWORD = "Str0ng-Passw0rd-2026!"
BACKOFFICE = "/backoffice/"
ADMIN_LOGIN = "/backoffice/login/"
SIGN_IN = "/fr/compte/login/"
MFA_STAGE = "/fr/compte/2fa/authenticate/"
MFA_REAUTH = "/fr/compte/2fa/reauthenticate/"
PASSWORD_REAUTH = "/fr/compte/reauthenticate/"
TOTP_ACTIVATE = "/fr/compte/2fa/totp/activate/"
RECOVERY_CODES = "/fr/compte/2fa/recovery-codes/"
RECOVERY_CODES_GENERATE = "/fr/compte/2fa/recovery-codes/generate/"
RESERVED = "/fr/espace-reserve/"
MFA_MIDDLEWARE = "accounts.middleware.BackofficeMFAMiddleware"


# ---------------------------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------------------------
class PinnedTotpClock:
    """allauth's TOTP check on one fixed time step: real codes, never a period boundary in the middle of a test."""

    def __init__(self, monkeypatch):
        self.step = 59_000_000
        monkeypatch.setattr(totp_auth, "yield_hotp_counters_from_time", lambda: iter([self.step]))

    def code(self, secret: str) -> str:
        return totp_auth.format_hotp_value(totp_auth.hotp_value(secret, self.step))


@pytest.fixture
def clock(monkeypatch):
    return PinnedTotpClock(monkeypatch)


def _enrol_totp(user) -> str:
    """Give ``user`` a real TOTP authenticator, as allauth's activation does; return its secret."""
    secret = totp_auth.generate_totp_secret()
    totp_auth.TOTP.activate(user, secret)
    return secret


def _verified(user):
    """allauth's sign-in requires a verified address (ACCOUNT_EMAIL_VERIFICATION = "mandatory")."""
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    return user


def _path(response) -> str:
    return urlsplit(response["Location"]).path


def _next_in(url: str) -> str:
    return parse_qs(urlsplit(url).query).get("next", [""])[0]


def _next(response) -> str:
    return _next_in(response["Location"])


def _signed_in(client) -> bool:
    return "_auth_user_id" in client.session


def _record_mfa_step(client, authenticator) -> None:
    """Write the record allauth's MFA step writes (``record_authentication``), for tests about what it proves."""
    session = client.session
    records = list(session.get(AUTHENTICATION_METHODS_SESSION_KEY, []))
    records.append({"method": "mfa", "at": time.time(), "id": authenticator.pk, "type": authenticator.type})
    session[AUTHENTICATION_METHODS_SESSION_KEY] = records
    session.save()


def _allauth_sign_in(client, user, password=PASSWORD, next_url=BACKOFFICE):
    return client.post(SIGN_IN, {"login": user.email, "password": password, "next": next_url})


def _age_the_steps(client, seconds: int = 3600) -> None:
    """Make every authentication step of the session older than ``ACCOUNT_REAUTHENTICATION_TIMEOUT`` (300 s)."""
    session = client.session
    session[AUTHENTICATION_METHODS_SESSION_KEY] = [
        {**step, "at": step["at"] - seconds} for step in session[AUTHENTICATION_METHODS_SESSION_KEY]
    ]
    session.save()


def _backoffice_status(client) -> int:
    return client.get(BACKOFFICE).status_code


@pytest.fixture
def enforced(settings):
    settings.BACKOFFICE_MFA_ENFORCED = True
    return settings


@pytest.fixture(params=[True, False], ids=["enforced", "not-enforced"])
def either_setting(request, settings):
    """The Present rule holds whatever BACKOFFICE_MFA_ENFORCED says: it is about a factor the account HOLDS."""
    settings.BACKOFFICE_MFA_ENFORCED = request.param
    return request.param


# ---------------------------------------------------------------------------------------------------------------
# (a) The back office's own sign-in form authenticates no one
# ---------------------------------------------------------------------------------------------------------------
class TestTheBackofficeSignInFormIsClosed:
    def test_f5_the_backoffice_sign_in_form_never_opens_the_backoffice_on_a_password_alone(
        self, client, staff_user, either_setting
    ):
        """The DevOps lane's reproduction: POST the password to the back office's own form, then open it."""
        _enrol_totp(staff_user)

        response = client.post(
            f"{ADMIN_LOGIN}?next={BACKOFFICE}",
            {"username": staff_user.email, "password": PASSWORD, "next": BACKOFFICE},
        )

        assert not _signed_in(client), "the back office's own form signed the account in"
        assert _path(response) == SIGN_IN and _next(response) == BACKOFFICE
        assert _backoffice_status(client) != 200, "the back office opened without the second factor"

    def test_it_authenticates_no_one_whatever_it_is_sent(self, client, staff_user, superuser, person_user):
        """No session, no attempt either: the audit trail records neither a sign-in nor a failed one."""
        from audit.models import AuditEvent

        for email, password in (
            (staff_user.email, PASSWORD),  # a staff account without a device
            (superuser.email, PASSWORD),
            (person_user.email, PASSWORD),
            (staff_user.email, "not-the-password"),
        ):
            response = client.post(ADMIN_LOGIN, {"username": email, "password": password})
            assert response.status_code == 302 and _path(response) == SIGN_IN, email
            assert not _signed_in(client), email
        assert not AuditEvent.objects.filter(action__in=("auth.login", "auth.login_failed")).exists()

    def test_it_renders_no_password_field(self, client):
        response = client.get(ADMIN_LOGIN)
        assert response.status_code == 302
        assert b'type="password"' not in response.content
        assert "no-store" in response["Cache-Control"] or "max-age=0" in response["Cache-Control"]

    def test_a_signed_out_visitor_is_sent_to_allauth_with_the_page_asked_for(self, client):
        response = client.get(f"{ADMIN_LOGIN}?next=/backoffice/cms/page/")
        assert response.status_code == 302
        assert _path(response) == SIGN_IN
        assert _next(response) == "/backoffice/cms/page/"

    @pytest.mark.parametrize(
        "hostile",
        [
            "https://evil.example/backoffice/",
            "http://testserver/backoffice/",  # this host, but an absolute address: still not a back-office path
            "//evil.example/backoffice/",
            "///evil.example/backoffice/",
            "///backoffice/",
            "/\\evil.example/backoffice/",
            "\\\\evil.example\\backoffice\\",
            "javascript:alert(1)//backoffice/",
            "/fr/espace-reserve/",  # this site, but not the back office
            "/backofficeX/",
            "",
        ],
    )
    def test_a_next_that_is_not_a_backoffice_page_of_this_site_becomes_the_index(self, client, hostile):
        response = client.get(ADMIN_LOGIN, {"next": hostile})
        assert response.status_code == 302 and _path(response) == SIGN_IN
        assert _next(response) == BACKOFFICE, hostile

    def test_an_anonymous_visit_to_any_backoffice_page_ends_at_allauth_sign_in(self, client, seeded):
        response = client.get("/backoffice/accounts/user/", follow=True)
        assert response.status_code == 200
        assert response.request["PATH_INFO"] == SIGN_IN
        hops = [urlsplit(url).path for url, _status in response.redirect_chain]
        assert hops == [ADMIN_LOGIN, SIGN_IN], response.redirect_chain
        assert _next_in(response.redirect_chain[-1][0]) == "/backoffice/accounts/user/"

    def test_a_signed_in_account_without_the_backoffice_meets_a_refusal_not_a_form(self, client, seeded, person_user):
        """Django's form offered «sign in as another account»; a redirect back to the index would loop."""
        client.force_login(person_user)
        assert client.get(ADMIN_LOGIN).status_code == 403
        response = client.get(BACKOFFICE, follow=True)
        assert response.status_code == 403
        assert len(response.redirect_chain) == 1, response.redirect_chain

    def test_a_staff_session_that_presented_its_factor_is_sent_on(self, client, staff_user):
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        _record_mfa_step(client, Authenticator.objects.get(user=staff_user))
        response = client.get(ADMIN_LOGIN, {"next": "/backoffice/accounts/user/"})
        assert response.status_code == 302 and response["Location"] == "/backoffice/accounts/user/"

    def test_a_staff_session_that_did_not_is_sent_to_present_it(self, client, staff_user):
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        with override_settings(MIDDLEWARE=[m for m in django_settings.MIDDLEWARE if m != MFA_MIDDLEWARE]):
            response = client.get(ADMIN_LOGIN, {"next": "/backoffice/accounts/user/"})
        assert _path(response) == MFA_REAUTH and _next(response) == "/backoffice/accounts/user/"


# ---------------------------------------------------------------------------------------------------------------
# (b) Present: an account that holds a second factor reaches the back office only after presenting it
# ---------------------------------------------------------------------------------------------------------------
class TestEnrolledStaffMustPresentTheirSecondFactor:
    def test_through_allauth_the_code_is_asked_before_the_backoffice_opens(
        self, client, seeded, staff_user, clock, either_setting
    ):
        secret = _enrol_totp(_verified(staff_user))

        response = _allauth_sign_in(client, staff_user)
        assert _path(response) == MFA_STAGE, "allauth's sign-in must stop at its MFA stage"
        assert not _signed_in(client), "the password alone signed the account in"
        assert _backoffice_status(client) != 200

        response = client.post(MFA_STAGE, {"code": clock.code(secret)})
        assert response.status_code == 302 and response["Location"] == BACKOFFICE
        assert _signed_in(client)
        assert _backoffice_status(client) == 200

    def test_a_wrong_code_never_opens_it(self, client, seeded, staff_user, clock):
        secret = _enrol_totp(_verified(staff_user))
        _allauth_sign_in(client, staff_user)
        wrong = f"{(int(clock.code(secret)) + 1) % 1_000_000:06d}"
        assert client.post(MFA_STAGE, {"code": wrong}).status_code == 200
        assert not _signed_in(client)
        assert _backoffice_status(client) != 200

    def test_a_recovery_code_is_a_second_factor_too(self, client, seeded, staff_user):
        _enrol_totp(_verified(staff_user))
        recovery = RecoveryCodes.activate(staff_user).generate_codes()[0]
        _allauth_sign_in(client, staff_user)
        response = client.post(MFA_STAGE, {"code": recovery})
        assert response.status_code == 302 and response["Location"] == BACKOFFICE
        assert _backoffice_status(client) == 200

    def test_a_session_opened_by_another_door_is_sent_to_present_the_factor(self, client, staff_user, either_setting):
        """``force_login`` stands for every door that is not allauth's sign-in — the admin form among them."""
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        response = client.get(BACKOFFICE)
        assert response.status_code == 302
        assert _path(response) == MFA_REAUTH and _next(response) == BACKOFFICE

    def test_an_admin_page_reads_the_accounts_authenticators_once(self, client, seeded, superuser, clock, enforced):
        """One admin page asked the policy four times — eight reads of the authenticators (the review, finding 3)."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        secret = _enrol_totp(_verified(superuser))
        _allauth_sign_in(client, superuser)
        client.post(MFA_STAGE, {"code": clock.code(secret)})
        with CaptureQueriesContext(connection) as captured:
            assert client.get("/backoffice/accounts/user/").status_code == 200
        reads = [query["sql"] for query in captured.captured_queries if "mfa_authenticator" in query["sql"]]
        assert len(reads) <= 2, reads  # whether it holds a TOTP device (Enrol), and which authenticators (Present)

    def test_the_answer_is_kept_for_the_request_but_follows_what_it_was_computed_from(
        self, staff_user, user_factory, settings, django_assert_num_queries
    ):
        """Kept on the request, never across a change the request itself makes: the account, the setting, a step."""
        from accounts import services

        settings.BACKOFFICE_MFA_ENFORCED = True
        newcomer = user_factory("newcomer@example.test", role=roles.STAFF, is_staff=True)  # no device yet
        _enrol_totp(staff_user)
        device = Authenticator.objects.get(user=staff_user)
        request = RequestFactory().get(BACKOFFICE)
        request.session, request.user = {}, staff_user

        # Each step below changes exactly one of the three inputs, right after an answer kept for the other two.
        assert services.second_factor_due(request, staff_user) == services.PRESENT
        with django_assert_num_queries(0):
            assert services.second_factor_due(request, staff_user) == services.PRESENT
        request.session[AUTHENTICATION_METHODS_SESSION_KEY] = [
            {"method": "mfa", "at": time.time(), "id": device.pk, "type": device.type}
        ]
        assert services.second_factor_due(request, staff_user) is None, "a factor presented during the request counts"
        assert services.second_factor_due(request, newcomer) == services.ENROL, "each account answered for itself"
        settings.BACKOFFICE_MFA_ENFORCED = False
        assert services.second_factor_due(request, newcomer) is None, "the setting is part of the answer"

    def test_presenting_the_code_at_reauthentication_opens_it(self, client, seeded, staff_user, clock):
        secret = _enrol_totp(staff_user)
        client.force_login(staff_user)
        reauth = client.get(BACKOFFICE)["Location"]

        response = client.post(reauth, {"code": clock.code(secret)})
        assert response.status_code == 302 and response["Location"] == BACKOFFICE
        assert _backoffice_status(client) == 200

    def test_failed_codes_at_reauthentication_are_rate_limited(self, client, seeded, staff_user, clock):
        """allauth's limit on failed codes (``login_failed``, per account) holds on the new door."""
        secret = _enrol_totp(staff_user)
        client.force_login(staff_user)
        wrong = f"{(int(clock.code(secret)) + 1) % 1_000_000:06d}"
        attempts = int(django_settings.ACCOUNT_RATE_LIMITS["login_failed"].split(",")[-1].split("/")[0])
        for _ in range(attempts):
            assert client.post(MFA_REAUTH, {"code": wrong, "next": BACKOFFICE}).status_code in (200, 429)
        client.post(MFA_REAUTH, {"code": clock.code(secret), "next": BACKOFFICE})
        assert _backoffice_status(client) == 302, "the right code after the limit must not open the back office"

    def test_a_password_reauthentication_is_not_a_second_factor(self, client, seeded, staff_user):
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        client.post("/fr/compte/reauthenticate/", {"password": PASSWORD, "next": BACKOFFICE})
        steps = client.session.get(AUTHENTICATION_METHODS_SESSION_KEY, [])
        assert any(s["method"] == "password" and s.get("reauthenticated") for s in steps), "accepted by allauth"
        response = client.get(BACKOFFICE)
        assert _path(response) == MFA_REAUTH

    def test_a_step_proved_with_another_accounts_device_does_not_count(self, client, user_factory, staff_user):
        """A sign-in begun as A and abandoned leaves A's step in the session; B's session inherits it on login."""
        other = user_factory("other@example.test")
        _enrol_totp(other)
        _enrol_totp(staff_user)
        _record_mfa_step(client, Authenticator.objects.get(user=other))
        client.force_login(staff_user)  # no user in the session yet: Django rotates the key and keeps the data
        assert client.session.get(AUTHENTICATION_METHODS_SESSION_KEY), "the inherited step is there"
        assert _path(client.get(BACKOFFICE)) == MFA_REAUTH

    def test_a_step_whose_authenticator_is_gone_does_not_count(self, client, staff_user):
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        old = Authenticator.objects.get(user=staff_user)
        _record_mfa_step(client, old)
        assert _backoffice_status(client) == 200
        old.delete()
        _enrol_totp(staff_user)  # a new device, never presented in this session
        assert _path(client.get(BACKOFFICE)) == MFA_REAUTH

    def test_a_device_added_behind_an_open_session_is_not_a_proof(self, client, staff_user, enforced):
        """An administrator may add an authenticator to an account; the session that is already open proved nothing."""
        client.force_login(staff_user)
        assert _path(client.get(BACKOFFICE)) == TOTP_ACTIVATE
        _enrol_totp(staff_user)
        assert _path(client.get(BACKOFFICE)) == MFA_REAUTH

    def test_a_person_promoted_to_staff_while_signed_in(self, client, seeded, user_factory, clock, enforced):
        """Signed in with a password (no device, no MFA stage), then promoted: enrol, then present, then enter."""
        person = _verified(user_factory("promoted@example.test", role=roles.PERSON))
        response = _allauth_sign_in(client, person, next_url=RESERVED)
        assert response.status_code == 302 and _signed_in(client)

        person.is_staff = True
        person.save(update_fields=["is_staff"])
        roles.assign_role(person, roles.STAFF)
        assert _path(client.get(BACKOFFICE)) == TOTP_ACTIVATE

        secret = _enrol_totp(person)
        reauth = client.get(BACKOFFICE)
        assert _path(reauth) == MFA_REAUTH
        client.post(reauth["Location"], {"code": clock.code(secret)})
        assert _backoffice_status(client) == 200


# ---------------------------------------------------------------------------------------------------------------
# Enrol, and who the rules do not concern
# ---------------------------------------------------------------------------------------------------------------
class TestEnrolmentAndTheAccountsOutsideThePolicy:
    def test_unenrolled_staff_signed_in_through_allauth_are_sent_to_enrol_when_enforced(
        self, client, seeded, staff_user, enforced
    ):
        _allauth_sign_in(client, _verified(staff_user))
        assert _signed_in(client)
        assert _path(client.get(BACKOFFICE)) == TOTP_ACTIVATE

    def test_unenrolled_staff_reach_the_backoffice_when_not_enforced(self, client, staff_user, settings):
        settings.BACKOFFICE_MFA_ENFORCED = False
        client.force_login(staff_user)
        assert _backoffice_status(client) == 200

    def test_an_unenrolled_account_can_still_enrol(self, client, staff_user, enforced):
        """allauth asks for the password before a device is added — never for a factor the account does not hold."""
        client.force_login(staff_user)
        response = client.get(TOTP_ACTIVATE)
        assert response.status_code in (200, 302)
        if response.status_code == 302:
            assert _path(response) not in (MFA_REAUTH, TOTP_ACTIVATE)

    @pytest.mark.django_db(transaction=True)
    def test_enrolling_through_allauth_counts_as_presenting_the_new_device(
        self, client, seeded, staff_user, clock, enforced
    ):
        """
        allauth's activation takes a right code of the new device: the next page does not ask for another.

        A transactional test, because allauth sends ``authenticator_added`` on commit: under ATOMIC_REQUESTS the
        request's transaction commits when the view returns, before the session is saved — only a real commit
        reproduces that order (captured callbacks would run after the response, on a session already saved).
        """
        _allauth_sign_in(client, _verified(staff_user))  # a password, no device: no MFA stage
        assert _path(client.get(BACKOFFICE)) == TOTP_ACTIVATE
        assert client.get(TOTP_ACTIVATE).status_code == 200  # just signed in: no re-authentication asked
        secret = client.session[totp_auth.SECRET_SESSION_KEY]
        response = client.post(TOTP_ACTIVATE, {"code": clock.code(secret)})
        assert _path(response) == "/fr/compte/2fa/recovery-codes/", "allauth shows the new recovery codes next"
        assert client.get(response["Location"]).status_code == 200, "the codes, not a second request for the code"
        assert _backoffice_status(client) == 200

    @pytest.mark.django_db(transaction=True)
    def test_a_device_enrolled_in_one_session_is_presented_in_that_one_only(
        self, client, seeded, staff_user, clock, enforced
    ):
        from django.test import Client

        _allauth_sign_in(client, _verified(staff_user))
        client.get(TOTP_ACTIVATE)
        client.post(TOTP_ACTIVATE, {"code": clock.code(client.session[totp_auth.SECRET_SESSION_KEY])})
        assert _backoffice_status(client) == 200

        elsewhere = Client()
        elsewhere.force_login(staff_user)
        assert _path(elsewhere.get(BACKOFFICE)) == MFA_REAUTH

    def test_only_the_sessions_own_new_device_is_remembered(self, staff_user, user_factory):
        """Asserted through the policy's own entry point, ``second_factor_due`` (the sec-f5 review, finding 4)."""
        from accounts import services

        other = user_factory("someone-else@example.test", role=roles.STAFF, is_staff=True)
        request = RequestFactory().get(TOTP_ACTIVATE)
        request.session, request.user = {}, staff_user
        _enrol_totp(other)
        services.remember_enrolment(None, request, other, Authenticator.objects.get(user=other))
        recovery = RecoveryCodes.activate(staff_user).instance
        services.remember_enrolment(None, request, staff_user, recovery)
        assert request.session == {}, "another account's device, or recovery codes, are never remembered"
        _enrol_totp(staff_user)
        own = Authenticator.objects.get(user=staff_user, type=Authenticator.Type.TOTP)
        services.remember_enrolment(None, request, staff_user, own)
        assert services.second_factor_due(request, staff_user) is None, "the session's own new device counts"
        assert services.second_factor_due(request, other) == services.PRESENT, "never for another account's device"

    def test_the_policy_runs_the_binding_rule_it_documents(self, staff_user, monkeypatch):
        """``session_presented_second_factor`` decides on the production path; it is not a helper beside it."""
        from accounts import services

        def unproven_request():
            request = RequestFactory().get(BACKOFFICE)
            request.session, request.user = {}, staff_user
            return request

        _enrol_totp(staff_user)
        assert services.second_factor_due(unproven_request(), staff_user) == services.PRESENT
        monkeypatch.setattr(services, "session_presented_second_factor", lambda *args, **kwargs: True)
        assert services.second_factor_due(unproven_request(), staff_user) is None, "decided without the binding rule"

    def test_a_person_with_a_device_is_not_concerned(self, client, user_factory, either_setting):
        person = user_factory("person-with-totp@example.test", role=roles.PERSON)
        _enrol_totp(person)
        client.force_login(person)
        assert client.get(RESERVED).status_code == 200
        assert client.get(BACKOFFICE, follow=True).status_code == 403


# ---------------------------------------------------------------------------------------------------------------
# The reserved area: the same rule, for every account that reads another person's file
# ---------------------------------------------------------------------------------------------------------------
class TestTheReservedArea:
    def test_an_enrolled_professional_presents_the_factor_before_any_case_file(
        self, client, user_factory, either_setting
    ):
        professional = user_factory("pro@example.test", role=roles.PROFESSIONAL)
        _enrol_totp(professional)
        client.force_login(professional)
        for path in (RESERVED, "/fr/espace-reserve/dossiers/", "/it/espace-reserve/", "/ar/espace-reserve/guichet/"):
            response = client.get(path)
            assert response.status_code == 302 and _path(response).endswith("/compte/2fa/reauthenticate/"), path
        _record_mfa_step(client, Authenticator.objects.get(user=professional))
        assert client.get(RESERVED).status_code == 200

    def test_an_enrolled_professional_signed_in_through_allauth_enters(self, client, seeded, user_factory, clock):
        professional = _verified(user_factory("pro-real@example.test", role=roles.PROFESSIONAL))
        secret = _enrol_totp(professional)
        assert _path(_allauth_sign_in(client, professional, next_url=RESERVED)) == MFA_STAGE
        client.post(MFA_STAGE, {"code": clock.code(secret)})
        assert client.get(RESERVED).status_code == 200

    def test_the_documents_endpoints_belong_to_the_perimeter(self, client, user_factory, either_setting):
        """
        ``/documents/`` is language-neutral, mounted outside the reserved area, and serves its pieces: a reviewer
        downloads another person's documents there. The middleware's own docstring said a document was read inside
        the perimeter; the path was not in it.
        """
        professional = user_factory("pro-docs@example.test", role=roles.PROFESSIONAL)
        _enrol_totp(professional)
        client.force_login(professional)
        for path in (
            "/documents/",
            f"/documents/{uuid.uuid4()}/",
            f"/documents/requirements/{uuid.uuid4()}/",
            f"/documents/requirements/{uuid.uuid4()}/review/",
            "/documents/link/some-token/",
        ):
            response = client.get(path)
            assert response.status_code == 302 and _path(response) == MFA_REAUTH, path
        _record_mfa_step(client, Authenticator.objects.get(user=professional))
        assert client.get(f"/documents/{uuid.uuid4()}/").status_code == 404, "presented: the view answers itself"

    def test_an_unenrolled_reviewer_enrols_before_any_document_when_enforced(self, client, user_factory, enforced):
        operator = user_factory("operator-docs@example.test", role=roles.OPERATOR)
        client.force_login(operator)
        assert _path(client.get(f"/documents/{uuid.uuid4()}/")) == TOTP_ACTIVATE

    def test_a_persons_documents_are_not_concerned(self, client, seeded, user_factory, either_setting):
        person = user_factory("person-docs@example.test", role=roles.PERSON)
        _enrol_totp(person)
        client.force_login(person)
        response = client.get("/documents/")
        assert response.status_code == 200 or _path(response) not in (MFA_REAUTH, TOTP_ACTIVATE)


# ---------------------------------------------------------------------------------------------------------------
# (c) Every other way in
# ---------------------------------------------------------------------------------------------------------------
class TestTheOtherDoors:
    @pytest.fixture
    def unproven(self, client, staff_user):
        """A signed-in staff session of an account WITH a device that it never presented."""
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        return client

    def test_the_backoffice_sign_out_stays_open_and_ends_the_session(self, unproven):
        unproven.post("/backoffice/logout/")
        assert not _signed_in(unproven)

    def test_allauths_sign_out_stays_open(self, unproven):
        unproven.post("/fr/compte/logout/")
        assert not _signed_in(unproven)

    def test_the_backoffice_password_change_needs_the_factor(self, unproven):
        response = unproven.get("/backoffice/password_change/")
        assert _path(response) == MFA_REAUTH and _next(response) == "/backoffice/password_change/"

    @pytest.mark.parametrize(
        "page",
        [
            "/fr/compte/2fa/",
            "/fr/compte/2fa/totp/deactivate/",
            "/fr/compte/2fa/recovery-codes/",
            "/fr/compte/2fa/recovery-codes/generate/",
            "/fr/compte/2fa/recovery-codes/download/",
            "/en/compte/2fa/totp/deactivate/",
        ],
    )
    def test_the_pages_that_manage_the_factor_need_it_presented(self, unproven, page, either_setting):
        """allauth lets a session re-authenticate there by password: turn the device off, enrol another, walk in."""
        response = unproven.get(page)
        assert response.status_code == 302 and _path(response).endswith("/compte/2fa/reauthenticate/"), page

    def test_the_page_where_the_factor_is_presented_stays_open(self, unproven, seeded):
        assert unproven.get(f"{MFA_REAUTH}?next={BACKOFFICE}").status_code == 200

    @pytest.mark.parametrize(
        "crafted",
        [
            "/backoffice/accounts/user/1/2fa/change/",
            "/backoffice/accounts/user/1/logout/",
            "/backoffice/accounts/user/1/compte/logout/",
            "/fr/espace-reserve/2fa/",
            "/fr/espace-reserve/logout/",
        ],
    )
    def test_a_crafted_path_borrows_no_exemption(self, staff_user, crafted):
        """The exemptions are routes, not fragments: a back-office object id is a path and can hold «/2fa/»."""
        _enrol_totp(staff_user)
        request = RequestFactory().get(crafted)
        request.session = {}
        request.user = staff_user
        response = second_factor_response(request)
        assert response is not None and urlsplit(response["Location"]).path == MFA_REAUTH, crafted
        assert BackofficeMFAMiddleware.must_redirect(request)

    def test_the_exemptions_are_exactly_signing_out_and_presenting(self):
        assert manages_second_factor("/fr/compte/2fa/totp/deactivate/")
        assert manages_second_factor("/ar/compte/2fa/recovery-codes/")
        assert not manages_second_factor(MFA_REAUTH)
        assert not manages_second_factor(MFA_STAGE)
        assert not manages_second_factor("/backoffice/2fa/")

    def test_the_admin_site_keeps_the_policy_without_the_middleware(self, client, staff_user):
        """The middleware knows the back office by its path; the site itself must not depend on that."""
        _enrol_totp(staff_user)
        client.force_login(staff_user)
        with override_settings(MIDDLEWARE=[m for m in django_settings.MIDDLEWARE if m != MFA_MIDDLEWARE]):
            to_sign_in = client.get(BACKOFFICE)  # admin_view: no permission without the factor
            assert _path(to_sign_in) == ADMIN_LOGIN and _next(to_sign_in) == BACKOFFICE
            to_present = client.get(to_sign_in["Location"])  # the site's login: present it, then come back
            assert _path(to_present) == MFA_REAUTH and _next(to_present) == BACKOFFICE
            client.post("/backoffice/logout/")
            assert not _signed_in(client), "signing out stays open at the site too"

    def test_a_password_reset_signs_no_one_in_and_the_next_sign_in_asks_the_code(self, client, seeded, staff_user):
        """The link allauth e-mails (its own token generator and encoding), followed to the new password."""
        from allauth.account.forms import default_token_generator
        from allauth.account.utils import user_pk_to_url_str

        _enrol_totp(_verified(staff_user))
        key = f"{user_pk_to_url_str(staff_user)}-{default_token_generator.make_token(staff_user)}"
        set_password = client.get(f"/fr/compte/password/reset/key/{key}/")["Location"]
        assert set_password.endswith("-set-password/"), set_password
        new_password = "Nuovo-Segreto-di-Prova-2026!"  # test-only
        response = client.post(set_password, {"password1": new_password, "password2": new_password})
        assert response.status_code == 302
        assert not _signed_in(client), "a password reset must never sign the account in"

        assert _path(_allauth_sign_in(client, staff_user, password=new_password)) == MFA_STAGE
        assert not _signed_in(client)

    def test_no_setting_opens_a_door_around_the_mfa_stage(self):
        """Remember-me, trusted browsers, passkey or code sign-in, sign-in on reset: none is on."""
        from allauth.account import app_settings as account_settings
        from allauth.mfa import app_settings as mfa_settings

        assert account_settings.LOGIN_ON_PASSWORD_RESET is False
        assert account_settings.SESSION_REMEMBER is False, "the session ends with the browser, after 8 h at most"
        assert account_settings.LOGIN_BY_CODE_ENABLED is False
        assert mfa_settings.TRUST_ENABLED is False, "a trusted browser skips the MFA stage"
        assert mfa_settings.PASSKEY_LOGIN_ENABLED is False
        assert mfa_settings.TOTP_INSECURE_BYPASS_CODE is None
        assert django_settings.SESSION_COOKIE_AGE <= 8 * 60 * 60


# ---------------------------------------------------------------------------------------------------------------
# allauth's resumption of a suspended request (the sec-f5 review, finding 1)
# ---------------------------------------------------------------------------------------------------------------
class TestAllauthsResumptionOfASuspendedRequest:
    """
    When a page asks for a recent sign-in, allauth keeps the POST it interrupted and, after the re-authentication,
    resumes it by calling the view function itself — no middleware runs on that call. A password step never presents
    the factor: for a session that owes it, nothing is resumed.
    """

    @staticmethod
    def _suspend_a_regeneration(client) -> None:
        """A POST to a page that asks for a recent sign-in, from a session whose last step is old: allauth keeps it."""
        _age_the_steps(client)
        response = client.post(RECOVERY_CODES_GENERATE, {})
        assert response.status_code == 302 and _path(response) == PASSWORD_REAUTH, response
        assert SUSPENDED_REQUEST_KEY in client.session, "allauth kept the POST"

    def test_a_request_suspended_before_enrolment_is_not_resumed_by_a_password_step(
        self, client, staff_user, either_setting
    ):
        """
        The reviewer's chain: a session opened while the account held nothing keeps a POST that regenerates the
        recovery codes; the owner enrols in another session; this session, which never presented the factor,
        re-authenticates with the password and names the kept page.
        """
        _allauth_sign_in(client, _verified(staff_user))
        assert _signed_in(client), "no device yet: no MFA stage"
        self._suspend_a_regeneration(client)

        _enrol_totp(staff_user)  # the owner, elsewhere
        owners_codes = RecoveryCodes.activate(staff_user).instance

        response = client.post(PASSWORD_REAUTH, {"password": PASSWORD, "next": RECOVERY_CODES_GENERATE})
        steps = client.session.get(AUTHENTICATION_METHODS_SESSION_KEY, [])
        assert any(s["method"] == "password" and s.get("reauthenticated") for s in steps), "accepted by allauth"
        assert Authenticator.objects.filter(pk=owners_codes.pk).exists(), "the owner's recovery codes were regenerated"
        assert SUSPENDED_REQUEST_KEY not in client.session
        assert response.status_code == 302 and _path(response) == RECOVERY_CODES_GENERATE, "sent on to next …"
        assert _path(client.get(response["Location"])) == MFA_REAUTH, "… where the rule holds it"
        assert _path(client.get(RECOVERY_CODES)) == MFA_REAUTH, "the codes are never shown"
        assert _backoffice_status(client) != 200

    def test_a_session_that_presented_the_factor_still_resumes_its_request(self, client, seeded, staff_user, clock):
        """allauth's resumption is unchanged for a session that owes nothing: the owner's own regeneration runs."""
        secret = _enrol_totp(_verified(staff_user))
        owners_codes = RecoveryCodes.activate(staff_user).instance
        _allauth_sign_in(client, staff_user)
        client.post(MFA_STAGE, {"code": clock.code(secret)})
        self._suspend_a_regeneration(client)

        client.post(PASSWORD_REAUTH, {"password": PASSWORD, "next": RECOVERY_CODES_GENERATE})
        assert not Authenticator.objects.filter(pk=owners_codes.pk).exists(), "the owner's request was not resumed"
        assert Authenticator.objects.filter(user=staff_user, type=Authenticator.Type.RECOVERY_CODES).exists()

    def test_presenting_the_factor_at_reauthentication_resumes_the_request(
        self, client, staff_user, clock, either_setting
    ):
        """The MFA re-authentication records the code first: what it resumes runs for a session that presented it."""
        _allauth_sign_in(client, _verified(staff_user))
        self._suspend_a_regeneration(client)
        secret = _enrol_totp(staff_user)
        owners_codes = RecoveryCodes.activate(staff_user).instance

        client.post(MFA_REAUTH, {"code": clock.code(secret), "next": RECOVERY_CODES_GENERATE})
        assert not Authenticator.objects.filter(pk=owners_codes.pk).exists(), "presented: the kept request runs"

    @pytest.mark.parametrize(
        ("path", "presented", "dropped"),
        [
            (PASSWORD_REAUTH, False, True),
            ("/ar/compte/reauthenticate/", False, True),
            (PASSWORD_REAUTH, True, False),  # a session that owes nothing keeps allauth's resumption
            (MFA_REAUTH, False, False),  # the code is presented there before anything resumes
            ("/fr/compte/email/", False, False),  # resuming happens on a re-authentication page only
        ],
    )
    def test_only_a_password_step_of_a_session_that_owes_the_factor_loses_it(
        self, staff_user, path, presented, dropped
    ):
        _enrol_totp(staff_user)
        request = RequestFactory().post(path)
        request.user = staff_user
        request.session = {SUSPENDED_REQUEST_KEY: {"request": "{}"}}
        if presented:
            device = Authenticator.objects.get(user=staff_user)
            request.session[AUTHENTICATION_METHODS_SESSION_KEY] = [
                {"method": "mfa", "at": time.time(), "id": device.pk, "type": device.type}
            ]
        forget_what_a_password_step_must_not_resume(request)
        assert (SUSPENDED_REQUEST_KEY not in request.session) is dropped

    def test_the_middleware_knows_allauths_reauthentication_pages_in_every_language(self):
        """The routes are matched by pattern; a change of allauth's mount point must fail here, not in silence."""
        from django.urls import reverse
        from django.utils import translation

        for language, _name in django_settings.LANGUAGES:
            with translation.override(language):
                assert PASSWORD_REAUTHENTICATION.match(reverse("account_reauthenticate")), language
                assert not manages_second_factor(reverse("mfa_reauthenticate")), language


# ---------------------------------------------------------------------------------------------------------------
# What the documents say (the sec-f5 review, finding 2)
# ---------------------------------------------------------------------------------------------------------------
class TestWhatTheDocumentsSay:
    #: The settings and the operator's documents. docs/design-v5/ holds the lanes' notes, which quote removed names
    #: as history.
    SOURCES = (
        "config/settings/*.py",
        "README.md",
        ".env.example",
        "docs/*.md",
        "docs/deployment/*",
        "docs/security/*.md",
    )

    def test_every_name_of_the_accounts_code_they_cite_exists(self):
        """``prod.py`` still cited ``accounts.middleware.EXEMPT_FRAGMENTS``, a name the fix had removed."""
        root = Path(django_settings.BASE_DIR)
        modules = sorted(path.stem for path in (root / "apps" / "accounts").glob("*.py") if path.stem != "__init__")
        citation = re.compile(rf"\baccounts\.({'|'.join(modules)})\.([A-Za-z_][A-Za-z0-9_]*)")
        cited: dict[str, str] = {}
        for pattern in self.SOURCES:
            for path in sorted(root.glob(pattern)):
                for module, name in citation.findall(path.read_text(encoding="utf-8")):
                    cited.setdefault(f"accounts.{module}.{name}", path.relative_to(root).as_posix())
        assert "accounts.middleware.BackofficeMFAMiddleware" in cited, "the sources were read"
        missing = {
            dotted: where
            for dotted, where in cited.items()
            if not hasattr(importlib.import_module(dotted.rsplit(".", 1)[0]), dotted.rsplit(".", 1)[1])
        }
        assert missing == {}, missing

    def test_what_the_flag_does_when_it_is_off(self, client, seeded, staff_user, clock, settings):
        """
        The documented sentence: the flag makes enrolment mandatory; a device the account holds is asked for in every
        session whatever it says. Off, the device is still asked for; an account that holds nothing enters on its
        password — even one whose device was deleted while the session was open: optional enrolment is what off means.
        """
        settings.BACKOFFICE_MFA_ENFORCED = False
        secret = _enrol_totp(_verified(staff_user))
        assert _path(_allauth_sign_in(client, staff_user)) == MFA_STAGE
        client.post(MFA_STAGE, {"code": clock.code(secret)})
        assert _backoffice_status(client) == 200
        Authenticator.objects.filter(user=staff_user).delete()
        assert _backoffice_status(client) == 200
