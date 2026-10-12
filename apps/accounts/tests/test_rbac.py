"""RBAC: role groups, has_role, deny-by-default object policies, membership helpers."""

from __future__ import annotations

import pytest
from django.contrib.auth.models import AnonymousUser, Group, Permission

from accounts import permissions, roles
from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind

pytestmark = [pytest.mark.django_db, pytest.mark.security]


class _Widget:
    def __init__(self, owner_id):
        self.owner_id = owner_id


class _Unregistered:
    pass


def test_ensure_roles_creates_every_group_idempotently():
    created = roles.ensure_roles()
    assert created == len(roles.ALL_ROLES)
    assert set(Group.objects.values_list("name", flat=True)) >= set(roles.ALL_ROLES)
    assert roles.ensure_roles() == 0


def test_role_permissions_follow_the_catalogue_and_deny_by_default():
    roles.ensure_roles()
    person = Group.objects.get(name=roles.PERSON)
    assert person.permissions.count() == 0, "public roles get no model permission"
    admin_group = Group.objects.get(name=roles.ADMINISTRATOR)
    codenames = set(admin_group.permissions.values_list("codename", flat=True))
    assert "view_privatedocument" in codenames
    assert "delete_privatedocument" not in codenames
    assert "change_privatedocument" not in codenames
    staff_group = Group.objects.get(name=roles.STAFF)
    staff_codenames = set(staff_group.permissions.values_list("codename", flat=True))
    assert not any(c.endswith("_privatedocument") for c in staff_codenames)
    assert not any(c.endswith("_user") for c in staff_codenames)
    for group in Group.objects.filter(name__in=roles.ALL_ROLES):
        for perm in group.permissions.all():
            assert Permission.objects.filter(pk=perm.pk).exists()


def test_has_role_and_roles_of(user_factory, superuser):
    user = user_factory("u@example.test", role=roles.COMPANY)
    assert roles.has_role(user, roles.COMPANY)
    assert not roles.has_role(user, roles.STAFF)
    assert roles.has_role(user, roles.STAFF, roles.COMPANY)
    assert roles.roles_of(user) == {roles.COMPANY}
    assert roles.has_role(superuser, roles.MODERATOR), "superuser satisfies every role check"
    assert not roles.has_role(AnonymousUser(), roles.PERSON)
    assert roles.roles_of(AnonymousUser()) == set()
    assert not roles.is_backoffice(user)
    roles.assign_role(user, roles.STAFF)
    assert roles.is_backoffice(user)
    roles.revoke_role(user, roles.STAFF)
    assert not roles.is_backoffice(user)
    assert roles.is_superadmin(superuser)
    assert not roles.is_superadmin(user)


def test_policy_deny_by_default(user_factory, superuser):
    user = user_factory("p@example.test", role=roles.PERSON)
    assert permissions.can(user, "view", _Unregistered()) is False
    assert permissions.can(AnonymousUser(), "view", _Unregistered()) is False
    assert permissions.can(None, "view", _Unregistered()) is False
    assert permissions.can(superuser, "view", _Unregistered()) is True
    with pytest.raises(permissions.PermissionDenied):
        permissions.require(user, "view", _Unregistered())


def test_registered_policy_and_inactive_user(user_factory):
    @permissions.policy(_Widget)
    def _widget_policy(user, action, obj):
        return action == "view" and permissions.owns(user, obj)

    owner = user_factory("owner@example.test")
    other = user_factory("other@example.test")
    widget = _Widget(owner.pk)
    assert permissions.can(owner, "view", widget)
    assert not permissions.can(owner, "delete", widget)
    assert not permissions.can(other, "view", widget)
    owner.is_active = False
    assert not permissions.can(owner, "view", widget), "inactive accounts are denied everything"


def test_membership_helpers(user_factory):
    a = user_factory("a@example.test")
    b = user_factory("b@example.test")
    org = Organisation.objects.create(name="Org", kind=OrganisationKind.INSTITUTION)
    Membership.objects.create(user=a, organisation=org, role=MembershipRole.MEMBER)
    assert permissions.member_of(a, org.pk)
    assert not permissions.member_of(b, org.pk)
    assert not permissions.member_of(a, None)
    assert not permissions.member_of(AnonymousUser(), org.pk)
    assert list(a.organisations) == [org]
    assert list(b.organisations) == []


def test_company_cannot_see_persons_by_default(user_factory):
    """Annexe §1.5 — no automatic relation between companies and persons; deny by default."""
    company = user_factory("c@example.test", role=roles.COMPANY)
    person = user_factory("person2@example.test", role=roles.PERSON)
    assert permissions.can(company, "view", person) is False
    assert permissions.can(person, "view", company) is False
