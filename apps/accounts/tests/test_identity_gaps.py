"""
The identity gaps of PERMISSION_MODEL §7, closed and kept closed.

Three of them, each a way an account could hold access it should not:

* **L-08** a revoked role kept working until the session cookie expired;
* **L-09** every account landed on the person's dashboard, whatever it was;
* **L-10** the second factor was required of ``is_staff``, which describes who reaches the Django
  admin rather than who reaches somebody else's case file.
"""

from __future__ import annotations

import pytest
from django.contrib.sessions.models import Session

from accounts import roles, services

pytestmark = pytest.mark.django_db


@pytest.fixture
def account(django_user_model):
    roles.ensure_roles()
    return django_user_model.objects.create_user(email="iam@example.test", password="Local-Only-2026!")


class TestSessionRevocation:
    def test_revoking_a_role_ends_the_open_sessions(self, client, account):
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        assert Session.objects.count() >= 1

        roles.revoke_role(account, roles.PROFESSIONAL)
        assert services.revoke_sessions(account) == 0, "the revocation already ended them"
        assert client.get("/fr/espace-reserve/").status_code == 302

    def test_another_accounts_session_is_untouched(self, client, django_user_model, account):
        other = django_user_model.objects.create_user(email="other@example.test", password="x")
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(other)
        before = Session.objects.count()

        roles.revoke_role(account, roles.PROFESSIONAL)
        assert Session.objects.count() == before

    def test_the_revocation_is_audited_without_naming_the_account(self, client, account):
        from audit.models import AuditEvent

        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        roles.revoke_role(account, roles.PROFESSIONAL)

        event = AuditEvent.objects.filter(action="account.sessions_revoked").latest("created_at")
        assert event.metadata["user_id"] == account.pk
        assert account.email not in str(event.metadata)

    def test_revoking_a_role_nobody_holds_is_harmless(self, account):
        roles.revoke_role(account, roles.PROFESSIONAL)
        roles.revoke_role(account, "role:does_not_exist")


class TestSecondFactor:
    def test_a_professional_needs_one_even_without_the_staff_flag(self, settings, account):
        settings.BACKOFFICE_MFA_ENFORCED = True
        roles.assign_role(account, roles.PROFESSIONAL)
        assert account.is_staff is False
        assert services.needs_backoffice_mfa(account) is True

    def test_an_authorised_actor_needs_one(self, settings, account):
        settings.BACKOFFICE_MFA_ENFORCED = True
        roles.assign_role(account, roles.AUTHORISED_ACTOR)
        assert services.needs_backoffice_mfa(account) is True

    def test_a_person_reading_only_their_own_file_does_not(self, settings, account):
        settings.BACKOFFICE_MFA_ENFORCED = True
        roles.assign_role(account, roles.PERSON)
        assert services.needs_backoffice_mfa(account) is False

    def test_the_requirement_is_off_when_the_deployment_says_so(self, settings, account):
        settings.BACKOFFICE_MFA_ENFORCED = False
        roles.assign_role(account, roles.ADMINISTRATOR)
        assert services.needs_backoffice_mfa(account) is False


class TestPostLoginRouting:
    def _redirect_for(self, rf, account):
        from accounts.adapters import AccountAdapter

        request = rf.get("/")
        request.user = account
        return AccountAdapter().get_login_redirect_url(request)

    def test_a_person_lands_on_their_dashboard(self, rf, account):
        roles.assign_role(account, roles.PERSON)
        assert self._redirect_for(rf, account).endswith("/espace-reserve/")

    def test_a_company_lands_in_the_company_workspace(self, rf, account):
        roles.assign_role(account, roles.COMPANY)
        assert "entreprise" in self._redirect_for(rf, account)

    def test_an_authorised_actor_lands_in_the_selection_workspace(self, rf, account):
        roles.assign_role(account, roles.AUTHORISED_ACTOR)
        assert "selection" in self._redirect_for(rf, account)

    def test_an_account_with_no_role_still_gets_a_usable_page(self, rf, account):
        assert self._redirect_for(rf, account).endswith("/espace-reserve/")


class TestSeparationOfDuties:
    def test_one_account_cannot_be_both_legal_editor_and_legal_approver(self, account):
        roles.assign_role(account, roles.LEGAL_EDITOR)
        with pytest.raises(roles.IncompatibleRoles):
            roles.assign_role(account, roles.LEGAL_APPROVER)

    def test_the_refusal_holds_in_the_other_order(self, account):
        roles.assign_role(account, roles.LEGAL_APPROVER)
        with pytest.raises(roles.IncompatibleRoles):
            roles.assign_role(account, roles.LEGAL_EDITOR)

    def test_the_pair_is_refused_when_groups_are_set_directly(self, account):
        from django.contrib.auth.models import Group

        names = [roles.LEGAL_EDITOR, roles.LEGAL_APPROVER]
        with pytest.raises(roles.IncompatibleRoles):
            roles.check_role_set(group.name for group in Group.objects.filter(name__in=names))

    def test_an_unrelated_pair_of_roles_is_allowed(self, account):
        roles.assign_role(account, roles.LEGAL_EDITOR)
        roles.assign_role(account, roles.CONTENT_EDITOR)
        assert {roles.LEGAL_EDITOR, roles.CONTENT_EDITOR} <= roles.roles_of(account)


class TestTheSecondFactorIsEnforcedWhereItIsRequired:
    """
    Widening WHO needs a second factor is only half the fix.

    `needs_backoffice_mfa` covers anyone who can read another person's case file, but the middleware
    used to guard `/backoffice/` alone — so a professional, who never goes there, was told by a
    function nothing consulted. A policy with no enforcement point is a comment.
    """

    @pytest.fixture
    def enforced(self, settings):
        settings.BACKOFFICE_MFA_ENFORCED = True
        return settings

    def test_a_professional_without_totp_is_sent_to_enrol(self, client, account, enforced):
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        response = client.get("/fr/espace-reserve/")
        assert response.status_code == 302
        assert "mfa" in response["Location"] or "totp" in response["Location"].lower()

    def test_a_person_reading_only_their_own_file_is_not(self, client, account, enforced):
        roles.assign_role(account, roles.PERSON)
        client.force_login(account)
        assert client.get("/fr/espace-reserve/").status_code == 200

    def test_the_platform_modules_are_guarded_too(self, client, account, enforced):
        """Every module mounts under the reserved area; none of them is a way round the rule."""
        roles.assign_role(account, roles.OPERATOR)
        client.force_login(account)
        for path in (
            "/fr/espace-reserve/dossiers/",
            "/fr/espace-reserve/entreprise/",
            "/fr/espace-reserve/guichet/",
            "/fr/espace-reserve/formation/",
        ):
            assert client.get(path).status_code == 302, path

    def test_every_language_is_guarded(self, client, account, enforced):
        """A rule that knew one language prefix would guard a quarter of the surface."""
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        for lang in ("fr", "it", "en", "ar"):
            assert client.get(f"/{lang}/espace-reserve/").status_code == 302, lang

    def test_leaving_is_never_blocked(self, client, account, enforced):
        """An account that can neither leave nor enrol is locked out by the rule that protects it."""
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        response = client.get("/fr/compte/logout/")
        assert response.status_code in (200, 302)
        if response.status_code == 302:
            assert "mfa" not in response["Location"].lower()

    def test_nothing_changes_when_the_deployment_has_not_enabled_it(self, client, account, settings):
        settings.BACKOFFICE_MFA_ENFORCED = False
        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        assert client.get("/fr/espace-reserve/").status_code == 200

    def test_the_enrolment_page_does_not_redirect_to_itself(self, client, account, enforced):
        """
        A redirect target that sits behind the rule it satisfies is a loop.

        allauth sends an enrolling account to its re-authentication page first — confirm your
        password before adding a second factor — which is correct and is NOT a loop. The assertion is
        therefore on the destination PATH, not on the whole Location: the `next` parameter carries
        the enrolment URL back, and a substring test would read that as the loop it is not.
        """
        from urllib.parse import urlparse

        from django.urls import reverse

        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        enrol = reverse("mfa_activate_totp")
        response = client.get(enrol)
        assert response.status_code in (200, 302)
        if response.status_code == 302:
            assert urlparse(response["Location"]).path != enrol

    def test_the_reserved_area_sends_the_account_to_enrol(self, client, account, enforced):
        from urllib.parse import urlparse

        from django.urls import reverse

        roles.assign_role(account, roles.PROFESSIONAL)
        client.force_login(account)
        response = client.get("/fr/espace-reserve/")
        assert urlparse(response["Location"]).path == reverse("mfa_activate_totp")
