"""Signup: gated by G2, mandatory consent, consent record + role assignment on success."""

from __future__ import annotations

import time

import pytest
from django.contrib.auth import get_user_model

from accounts import roles
from accounts.forms import SignupForm
from consents.models import ConsentPurpose, ConsentRecord

pytestmark = [pytest.mark.django_db]

SIGNUP_URL = "/fr/compte/signup/"


@pytest.fixture(autouse=True)
def _email_only_user_model(settings):
    """The project user model has no username: allauth must be told (settings change requested)."""
    settings.ACCOUNT_USER_MODEL_USERNAME_FIELD = None


def _payload(**overrides):
    data = {
        "full_name": "Nouvelle Personne",
        "email": "new.person@example.test",
        "account_type": "person",
        "password1": "Very-Str0ng-Passphrase-2026",
        "password2": "Very-Str0ng-Passphrase-2026",
        "accept_terms": "on",
        "form_started_at": str(int(time.time()) - 30),
        "website_url": "",
    }
    data.update(overrides)
    return data


def test_signup_closed_while_forms_gated(client):
    r = client.post(SIGNUP_URL, _payload())
    assert not get_user_model().objects.filter(email="new.person@example.test").exists()
    assert r.status_code in (200, 302)
    page = client.get(SIGNUP_URL)
    assert "Inscriptions ferm" in page.content.decode()


def test_signup_requires_consent(rf, legal_published):
    """Form-level: the consent checkbox is mandatory; nothing is created without it."""
    form = SignupForm(data=_payload(accept_terms=""))
    assert not form.is_valid()
    assert "accept_terms" in form.errors
    assert not get_user_model().objects.filter(email="new.person@example.test").exists()
    assert ConsentRecord.objects.filter(purpose=ConsentPurpose.ACCOUNT_TERMS).count() == 0


def test_signup_form_consent_never_prechecked():
    form = SignupForm()
    assert form.fields["accept_terms"].initial is False
    assert form.fields["accept_terms"].required is True
    assert form.field_order[-1] == "accept_terms"


def test_signup_creates_consent_record_and_role(client, legal_published):
    """
    A "company" signup records the declaration and the consent, and grants NO role.

    Changed deliberately on 20 September 2026: the declared account type used to grant its role on
    the spot, which was harmless only while those roles carried no permissions. The declaration is
    now queued for human verification (``accounts.services.register_declared_account_type``); see
    ``test_account_verification.py`` for the whole contract.
    """
    r = client.post(SIGNUP_URL, _payload(account_type="company"))
    assert r.status_code == 302, r.content.decode()[:500]
    user = get_user_model().objects.get(email="new.person@example.test")
    assert user.full_name == "Nouvelle Personne"
    assert user.account_type == "company"
    assert not roles.has_role(user, roles.COMPANY), "a declaration must not grant a role"
    assert user.verification.is_pending
    assert not user.is_staff
    consent = ConsentRecord.objects.get(purpose=ConsentPurpose.ACCOUNT_TERMS, user=user)
    assert consent.email == user.email
    assert consent.consent_text.version == 1
    assert user.terms_consent_id == consent.pk
    assert user.terms_accepted_at is not None


def test_signup_honeypot_spam_creates_nothing(legal_published):
    """Form-level: honeypot filled or instant submission → invalid, no user, no consent row."""
    for payload in (_payload(website_url="http://spam.example"), _payload(form_started_at=str(int(time.time())))):
        form = SignupForm(data=payload)
        assert not form.is_valid()
    assert not get_user_model().objects.filter(email="new.person@example.test").exists()
    assert ConsentRecord.objects.count() == 0
