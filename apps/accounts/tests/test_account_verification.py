"""
A declared account type does not grant its role.

Anyone can tick "Institution" on a public signup form. Until 20 September 2026 that declaration was
enough to be granted ``role:institution`` immediately. The roles carried no model permissions yet, so
nothing was exposed — but from phase P1 each of those roles opens a workspace with a real perimeter,
and a self-declared role would then be an escalation that needs no exploit, only a dropdown.
"""

from __future__ import annotations

import time

import pytest
from django.core.exceptions import PermissionDenied

from accounts import roles, services
from accounts.models import AccountType, AccountVerification, VerificationStatus
from audit.models import AuditEvent

pytestmark = pytest.mark.django_db

PASSWORD = "Signup-Passw0rd-2026!"


@pytest.fixture(autouse=True)
def _roles():
    roles.ensure_roles()


@pytest.fixture(autouse=True)
def _signup_open(legal_published, settings):
    """Signup is closed by gate G2 while the legal pages are missing: open it for these tests."""
    settings.ACCOUNT_USER_MODEL_USERNAME_FIELD = None


@pytest.fixture
def approver(django_user_model):
    user = django_user_model.objects.create_user(email="staff@example.test", password="x", is_staff=True)
    roles.assign_role(user, roles.ADMINISTRATOR)
    return user


def signup(client, email: str, account_type: str):
    return client.post(
        "/fr/compte/signup/",
        {
            "full_name": "Test Utente",
            "email": email,
            "account_type": account_type,
            "password1": PASSWORD,
            "password2": PASSWORD,
            "accept_terms": "on",
            "form_started_at": str(int(time.time()) - 30),
            "website_url": "",
        },
        follow=True,
    )


# ---------------------------------------------------------------------------------------------
# Signup
# ---------------------------------------------------------------------------------------------
def test_a_person_gets_the_person_role_immediately(client, django_user_model):
    """Claiming to be a person claims nothing, and the role only reaches one's own data."""
    signup(client, "persona@example.test", AccountType.PERSON)
    user = django_user_model.objects.get(email="persona@example.test")
    assert roles.has_role(user, roles.PERSON)
    assert not AccountVerification.objects.filter(user=user).exists()


@pytest.mark.parametrize(
    "account_type,role",
    [
        (AccountType.COMPANY, roles.COMPANY),
        (AccountType.INSTITUTION, roles.INSTITUTION),
        (AccountType.UNIVERSITY, roles.UNIVERSITY),
        (AccountType.PROFESSIONAL, roles.PROFESSIONAL),
    ],
)
def test_a_declared_type_grants_no_role_before_verification(client, django_user_model, account_type, role):
    signup(client, f"{account_type}@example.test", account_type)
    user = django_user_model.objects.get(email=f"{account_type}@example.test")
    assert roles.has_role(user, role) is False, "a declaration must not grant a role"
    assert user.groups.count() == 0


@pytest.mark.parametrize(
    "account_type",
    [AccountType.COMPANY, AccountType.INSTITUTION, AccountType.UNIVERSITY, AccountType.PROFESSIONAL],
)
def test_a_declared_type_opens_a_pending_verification(client, django_user_model, account_type):
    signup(client, f"{account_type}@example.test", account_type)
    user = django_user_model.objects.get(email=f"{account_type}@example.test")
    verification = AccountVerification.objects.get(user=user)
    assert verification.status == VerificationStatus.PENDING
    assert verification.declared_type == account_type
    assert verification.is_pending


def test_the_declaration_is_audited(client, django_user_model):
    signup(client, "impresa@example.test", AccountType.COMPANY)
    user = django_user_model.objects.get(email="impresa@example.test")
    event = AuditEvent.objects.filter(action="account.verification_requested", target_id=str(user.pk)).first()
    assert event is not None
    assert event.metadata["declared_type"] == AccountType.COMPANY


def test_a_staff_account_type_cannot_be_declared(client):
    """``staff`` is not among the public choices, and a crafted POST must not slip it through."""
    response = signup(client, "intruso@example.test", AccountType.STAFF)
    assert b"account_type" in response.content or response.status_code == 200
    from accounts.models import User

    user = User.objects.filter(email="intruso@example.test").first()
    assert user is None or user.groups.count() == 0


# ---------------------------------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------------------------------
def test_approval_grants_the_role(client, django_user_model, approver):
    signup(client, "impresa@example.test", AccountType.COMPANY)
    user = django_user_model.objects.get(email="impresa@example.test")
    verification = AccountVerification.objects.get(user=user)
    services.approve_account_verification(verification, decided_by=approver, note="verificata la visura")
    assert roles.has_role(user, roles.COMPANY)
    verification.refresh_from_db()
    assert verification.status == VerificationStatus.APPROVED
    assert verification.decided_by == approver
    assert verification.decided_at is not None


def test_an_account_cannot_verify_itself(client, django_user_model):
    """Four eyes: the decision is somebody else's, or it is not a verification."""
    signup(client, "impresa@example.test", AccountType.COMPANY)
    user = django_user_model.objects.get(email="impresa@example.test")
    verification = AccountVerification.objects.get(user=user)
    with pytest.raises(PermissionDenied):
        services.approve_account_verification(verification, decided_by=user)
    assert roles.has_role(user, roles.COMPANY) is False


def test_rejection_withdraws_the_role(client, django_user_model, approver):
    signup(client, "impresa@example.test", AccountType.COMPANY)
    user = django_user_model.objects.get(email="impresa@example.test")
    verification = AccountVerification.objects.get(user=user)
    services.approve_account_verification(verification, decided_by=approver)
    services.reject_account_verification(verification, decided_by=approver, note="documenti non conformi")
    assert roles.has_role(user, roles.COMPANY) is False
    verification.refresh_from_db()
    assert verification.status == VerificationStatus.REJECTED


def test_decisions_are_audited(client, django_user_model, approver):
    signup(client, "impresa@example.test", AccountType.COMPANY)
    user = django_user_model.objects.get(email="impresa@example.test")
    verification = AccountVerification.objects.get(user=user)
    services.approve_account_verification(verification, decided_by=approver)
    services.reject_account_verification(verification, decided_by=approver)
    actions = set(
        AuditEvent.objects.filter(target_id=str(user.pk), target_type="User").values_list("action", flat=True)
    )
    assert {"account.verification_approved", "account.verification_rejected"} <= actions
