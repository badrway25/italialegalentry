"""
An administrator must not be able to become a superadmin.

``role:administrator`` legitimately holds ``accounts: change`` so that it can manage ordinary
accounts. Django's stock ``UserAdmin`` exposes ``is_superuser`` and ``groups`` to anyone with that
permission, which turns a legitimate delegation into a one-click privilege escalation: tick
"superuser", or grant yourself ``role:superadmin`` — which ``accounts.permissions.can`` short-circuits
past every object-level policy — and the least-privilege model is gone.

These tests exercise the real admin over HTTP, not the guard functions, because the guard is only
worth what the request path actually enforces.
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse

from accounts import roles

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _roles():
    roles.ensure_roles()


@pytest.fixture
def administrator(django_user_model):
    user = django_user_model.objects.create_user(
        email="amministratore@example.test", password="Admin-Passw0rd-2026!", is_staff=True
    )
    roles.assign_role(user, roles.ADMINISTRATOR)
    return user


@pytest.fixture
def victim(django_user_model):
    return django_user_model.objects.create_user(email="persona@example.test", password="x")


@pytest.fixture
def superadmin(django_user_model):
    return django_user_model.objects.create_superuser(email="super@example.test", password="Super-Passw0rd-2026!")


@pytest.fixture
def as_administrator(client, administrator, settings):
    settings.BACKOFFICE_MFA_ENFORCED = False
    client.force_login(administrator)
    return client


def change_url(user) -> str:
    return reverse("admin:accounts_user_change", args=[user.pk])


def post_change(client, user, **overrides) -> None:
    payload = {
        "email": user.email,
        "full_name": user.full_name or "",
        "preferred_language": user.preferred_language or "fr",
        "account_type": user.account_type or "person",
        "is_active": "on",
        "memberships-TOTAL_FORMS": "0",
        "memberships-INITIAL_FORMS": "0",
        "memberships-MIN_NUM_FORMS": "0",
        "memberships-MAX_NUM_FORMS": "1000",
        **overrides,
    }
    client.post(change_url(user), payload, follow=True)


# ---------------------------------------------------------------------------------------------
# is_superuser
# ---------------------------------------------------------------------------------------------
def test_the_superuser_field_is_not_offered_to_an_administrator(as_administrator, victim):
    response = as_administrator.get(change_url(victim))
    assert response.status_code == 200
    assert b'name="is_superuser"' not in response.content


def test_an_administrator_cannot_grant_superuser_to_another_account(as_administrator, victim):
    post_change(as_administrator, victim, is_superuser="on")
    victim.refresh_from_db()
    assert victim.is_superuser is False


def test_an_administrator_cannot_grant_superuser_to_themselves(as_administrator, administrator):
    post_change(as_administrator, administrator, is_superuser="on")
    administrator.refresh_from_db()
    assert administrator.is_superuser is False


def test_an_administrator_cannot_strip_superuser_from_a_superadmin(as_administrator, superadmin):
    post_change(as_administrator, superadmin, is_superuser="")
    superadmin.refresh_from_db()
    assert superadmin.is_superuser is True


# ---------------------------------------------------------------------------------------------
# Protected groups
# ---------------------------------------------------------------------------------------------
def test_an_administrator_cannot_grant_the_superadmin_group(as_administrator, victim):
    group = Group.objects.get(name="role:superadmin")
    post_change(as_administrator, victim, groups=[str(group.pk)])
    assert victim.groups.filter(name="role:superadmin").exists() is False


def test_an_administrator_cannot_grant_the_administrator_group(as_administrator, victim):
    group = Group.objects.get(name="role:administrator")
    post_change(as_administrator, victim, groups=[str(group.pk)])
    assert victim.groups.filter(name="role:administrator").exists() is False


def test_protected_groups_are_absent_from_the_choices(as_administrator, victim):
    response = as_administrator.get(change_url(victim))
    body = response.content.decode()
    assert "role:superadmin" not in body
    assert "role:administrator" not in body


def test_an_administrator_may_still_grant_an_ordinary_role(as_administrator, victim):
    group = Group.objects.get(name="role:person")
    post_change(as_administrator, victim, groups=[str(group.pk)])
    assert victim.groups.filter(name="role:person").exists() is True


def test_an_existing_protected_group_is_not_stripped_by_an_ordinary_edit(as_administrator, victim):
    roles.assign_role(victim, roles.ADMINISTRATOR)
    person = Group.objects.get(name="role:person")
    post_change(as_administrator, victim, groups=[str(person.pk)])
    victim.refresh_from_db()
    assert victim.groups.filter(name="role:administrator").exists() is True
    assert victim.groups.filter(name="role:person").exists() is True


# ---------------------------------------------------------------------------------------------
# Superuser accounts are off limits
# ---------------------------------------------------------------------------------------------
def test_an_administrator_sees_a_superuser_account_read_only(as_administrator, superadmin):
    """
    Django renders the change view read-only when change permission is denied but view is allowed.
    That is acceptable — supervision without power — as long as nothing is submittable.
    """
    response = as_administrator.get(change_url(superadmin))
    assert response.status_code == 200
    body = response.content.decode()
    assert 'name="email"' not in body, "the form must be read-only, not editable"
    assert "_save" not in body, "no save button on an account the editor may not change"


def test_an_administrator_cannot_change_a_superuser_password(as_administrator, superadmin):
    """
    Resetting the password would let the administrator sign in as the superuser: the same
    escalation by a longer road.
    """
    url = reverse("admin:auth_user_password_change", args=[superadmin.pk])
    response = as_administrator.post(
        url, {"password1": "Owned-Passw0rd-2026!", "password2": "Owned-Passw0rd-2026!"}, follow=False
    )
    assert response.status_code in (302, 403, 404)
    superadmin.refresh_from_db()
    assert superadmin.check_password("Super-Passw0rd-2026!") is True


def test_an_administrator_cannot_delete_a_superuser(as_administrator, superadmin, django_user_model):
    response = as_administrator.post(
        reverse("admin:accounts_user_delete", args=[superadmin.pk]), {"post": "yes"}, follow=False
    )
    assert response.status_code in (302, 403)
    assert django_user_model.objects.filter(pk=superadmin.pk).exists()


def test_a_superadmin_still_sees_and_sets_everything(client, superadmin, victim, settings):
    settings.BACKOFFICE_MFA_ENFORCED = False
    client.force_login(superadmin)
    response = client.get(change_url(victim))
    assert b'name="is_superuser"' in response.content
    post_change(client, victim, is_superuser="on")
    victim.refresh_from_db()
    assert victim.is_superuser is True
