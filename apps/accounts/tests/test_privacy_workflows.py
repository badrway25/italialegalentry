"""GDPR workflows: export of own data, deletion request → anonymisation + consent withdrawal + audit."""

from __future__ import annotations

import json

import pytest
from allauth.account.models import EmailAddress
from allauth.mfa.models import Authenticator
from django.test import RequestFactory

from accounts import roles, services
from accounts.models import Membership, PersonProfile
from audit.models import AuditEvent
from consents.models import ConsentPurpose
from consents.services import record_consent

pytestmark = [pytest.mark.django_db, pytest.mark.security]

EXPORT_URL = "/fr/compte/profil/export/"
DELETE_URL = "/fr/compte/profil/suppression/"
PASSWORD = "Str0ng-Passw0rd-2026!"


def _consent_for(user):
    request = RequestFactory().post("/")
    request.user = user
    return record_consent(request, ConsentPurpose.ACCOUNT_TERMS, email=user.email, user=user)


def test_export_requires_post_and_login(client, terms_user):
    assert client.get(EXPORT_URL).status_code == 302
    client.force_login(terms_user)
    assert client.get(EXPORT_URL).status_code == 405


def test_export_contains_own_data_only(client, terms_user, other_user, organisation):
    consent = _consent_for(terms_user)
    _consent_for(other_user)
    PersonProfile.objects.create(user=terms_user, phone="+212600000000", country_of_residence="Maroc")
    client.force_login(terms_user)
    r = client.post(EXPORT_URL)
    assert r.status_code == 200
    assert r["Content-Type"].startswith("application/json")
    assert 'attachment; filename="italy-legal-entry-donnees-' in r["Content-Disposition"]
    assert {"private", "no-store"} <= {token.strip() for token in r["Cache-Control"].split(",")}
    data = json.loads(r.content.decode("utf-8"))
    assert data["account"]["email"] == "alice@example.test"
    assert data["account"]["roles"] == [roles.PERSON]
    assert data["profile"]["phone"] == "+212600000000"
    assert data["profile"]["country_of_residence"] == "Maroc"
    assert data["memberships"][0]["organisation"] == "Acme Formazione"
    assert data["memberships"][0]["role"] == "owner"
    assert len(data["consents"]) == 1
    assert data["consents"][0]["text_version"] == f"account_terms@v{consent.consent_text.version}"
    assert data["documents"] == []
    assert data["contact"] == "contact@agamieuromed.org"
    dump = json.dumps(data)
    assert "bob@example.test" not in dump
    assert "Bob Durand" not in dump
    assert AuditEvent.objects.filter(action="account.export", actor=terms_user).exists()


def test_the_export_carries_every_personal_field_the_profile_holds(client, terms_user):
    """
    Derived from the model, never from a literal.

    This assertion used to be an exact dict of two keys. An exact dict fails loudly when a field is
    ADDED — which is only noise — and stays silent when a field is FORGOTTEN, which is the failure
    that matters: a personal column the platform stores and the export omits is an incomplete
    subject access request. Seven profile fields were added during the platform build and the
    literal had to be rewritten; this version would not have needed touching, and would have caught
    the opposite mistake.
    """
    PersonProfile.objects.create(user=terms_user, phone="+212600000000", country_of_residence="Maroc")
    client.force_login(terms_user)
    exported = json.loads(client.post(EXPORT_URL).content.decode("utf-8"))["profile"]

    technical = {"id", "created_at", "updated_at", "user"}
    personal = {
        f.name for f in PersonProfile._meta.get_fields() if getattr(f, "concrete", False)
    } - technical
    missing = sorted(personal - set(exported))
    assert not missing, f"stored but never exported: {missing}"
    assert set(PersonProfile.PROFILE_FIELDS) <= set(exported)


def test_deletion_requires_password(client, terms_user):
    client.force_login(terms_user)
    assert client.get(DELETE_URL).status_code == 200
    r = client.post(DELETE_URL, {"password": "wrong-password", "confirm": "on"})
    assert r.status_code == 200
    terms_user.refresh_from_db()
    assert terms_user.is_active
    assert terms_user.email == "alice@example.test"
    r = client.post(DELETE_URL, {"password": PASSWORD})
    assert r.status_code == 200, "confirmation checkbox is mandatory"
    terms_user.refresh_from_db()
    assert terms_user.is_active


def test_deletion_anonymises_and_withdraws_consents(client, terms_user, other_user, organisation):
    consent = _consent_for(terms_user)
    terms_user.terms_consent = consent
    terms_user.save()
    other_consent = _consent_for(other_user)
    PersonProfile.objects.create(user=terms_user, phone="+212600000000")
    EmailAddress.objects.create(user=terms_user, email=terms_user.email, verified=True, primary=True)
    Authenticator.objects.create(user=terms_user, type=Authenticator.Type.TOTP, data={"secret": "x"})
    user_id = terms_user.pk

    client.force_login(terms_user)
    r = client.post(DELETE_URL, {"password": PASSWORD, "confirm": "on"})
    assert r.status_code == 302
    assert r["Location"].endswith("/fr/compte/profil/suppression/confirmee/")

    terms_user.refresh_from_db()
    assert terms_user.is_active is False
    assert terms_user.email == f"anonymised-{user_id}@anonymised.invalid"
    assert terms_user.full_name == ""
    assert not terms_user.has_usable_password()
    assert terms_user.groups.count() == 0
    assert not Membership.objects.filter(user_id=user_id).exists()
    assert not PersonProfile.objects.filter(user_id=user_id).exists()
    assert not EmailAddress.objects.filter(user_id=user_id).exists()
    assert not Authenticator.objects.filter(user_id=user_id).exists()
    consent.refresh_from_db()
    assert consent.withdrawn_at is not None
    assert consent.email == terms_user.email
    other_consent.refresh_from_db()
    assert other_consent.withdrawn_at is None, "other people's consents are untouched"
    other_user.refresh_from_db()
    assert other_user.is_active and other_user.email == "bob@example.test"

    actions = set(AuditEvent.objects.filter(actor_id=user_id).values_list("action", flat=True))
    assert {"account.deletion_requested", "account.anonymised"} <= actions
    for event in AuditEvent.objects.filter(actor_id=user_id):
        assert "alice@example.test" not in event.actor_label
        assert "alice@example.test" not in event.target_repr
        assert event.actor_label == f"user:{user_id} (anonymised)"
    # session is gone: profile now redirects to login
    assert client.get("/fr/compte/profil/").status_code == 302
    assert not client.login(email="alice@example.test", password=PASSWORD)


def test_anonymise_user_is_idempotent(terms_user):
    services.anonymise_user(terms_user, reason="test")
    services.anonymise_user(terms_user, reason="test")
    terms_user.refresh_from_db()
    assert terms_user.email.startswith("anonymised-")


def test_superuser_cannot_self_delete(client, superuser):
    client.force_login(superuser)
    assert client.get(DELETE_URL).status_code == 403
    assert client.post(DELETE_URL, {"password": PASSWORD, "confirm": "on"}).status_code == 403
    superuser.refresh_from_db()
    assert superuser.is_active


def test_deletion_only_targets_request_user(client, terms_user, other_user):
    client.force_login(terms_user)
    client.post(DELETE_URL, {"password": PASSWORD, "confirm": "on", "user": other_user.pk, "email": other_user.email})
    other_user.refresh_from_db()
    assert other_user.is_active and other_user.email == "bob@example.test"
    terms_user.refresh_from_db()
    assert not terms_user.is_active
