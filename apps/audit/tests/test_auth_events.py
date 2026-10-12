"""
Authentication and role events reach the audit trail.

REQ-SEC-06 lists "eventi di sicurezza dell'accesso" first, and the coverage was zero until
20 September 2026: the trail knew what people did with objects and nothing about who signed in.
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Group

from accounts import roles
from audit.models import AuditEvent

pytestmark = pytest.mark.django_db

PASSWORD = "Audit-Passw0rd-2026!"


@pytest.fixture
def person(django_user_model):
    roles.ensure_roles()
    return django_user_model.objects.create_user(email="accesso@example.test", password=PASSWORD)


def actions_for(target=None) -> set[str]:
    rows = AuditEvent.objects.all()
    if target is not None:
        rows = rows.filter(target_type=type(target).__name__, target_id=str(target.pk))
    return set(rows.values_list("action", flat=True))


def test_a_successful_login_is_audited(client, person):
    assert client.login(email="accesso@example.test", password=PASSWORD)
    assert "auth.login" in actions_for(person)


def test_a_logout_is_audited(client, person):
    client.login(email="accesso@example.test", password=PASSWORD)
    client.logout()
    assert "auth.logout" in actions_for(person)


def test_a_failed_login_is_audited(client, person):
    assert not client.login(email="accesso@example.test", password="wrong-password")
    assert "auth.login_failed" in actions_for()


def test_a_failed_login_stores_no_identifier(client, person):
    """
    The submitted address is often a real person's e-mail typed by someone else, and sometimes a
    password typed into the wrong field. What detects an attack is the rate and the origin.
    """
    client.login(email="vittima@example.test", password="Segreta-Passw0rd!")
    event = AuditEvent.objects.filter(action="auth.login_failed").latest("created_at")
    blob = f"{event.actor_label} {event.target_repr} {event.metadata}"
    assert "vittima@example.test" not in blob
    assert "Segreta-Passw0rd!" not in blob
    assert event.actor_id is None


def test_granting_a_role_is_audited(person):
    roles.assign_role(person, roles.PERSON)
    event = AuditEvent.objects.filter(action="auth.role_granted").latest("created_at")
    assert event.metadata["roles"] == ["role:person"]
    assert event.target_id == str(person.pk)


def test_revoking_a_role_is_audited(person):
    roles.assign_role(person, roles.PERSON)
    roles.revoke_role(person, roles.PERSON)
    event = AuditEvent.objects.filter(action="auth.role_revoked").latest("created_at")
    assert event.metadata["roles"] == ["role:person"]


def test_clearing_every_role_is_audited(person):
    roles.assign_role(person, roles.PERSON)
    person.groups.clear()
    event = AuditEvent.objects.filter(action="auth.role_revoked").latest("created_at")
    assert event.metadata["roles"] == ["<all>"]


def test_granting_from_the_group_side_is_audited(person):
    group = Group.objects.get(name="role:company")
    group.user_set.add(person)
    event = AuditEvent.objects.filter(action="auth.role_granted").latest("created_at")
    assert event.metadata["roles"] == ["role:company"]
    assert event.target_id == str(person.pk)
