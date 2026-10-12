"""Join flow: gated by G2, consent recorded (purpose COMMUNITY), pending membership, notification."""

import pytest

from audit.models import AuditEvent
from cms import locked_content
from community.models import Membership, MembershipStatus
from consents.models import ConsentPurpose, ConsentRecord
from integrations.models import OutboundEvent
from notifications.models import EmailOutbox

pytestmark = pytest.mark.django_db

JOIN = "/fr/forum-virtuel/rejoindre/"


def test_join_requires_login(client, seeded, flag_on):
    r = client.get(JOIN)
    assert r.status_code == 302 and "/compte/login/" in r["Location"]


def test_join_form_unavailable_while_forms_gated(client, seeded, flag_on, person_user):
    client.force_login(person_user)
    r = client.get(JOIN)
    assert r.status_code == 200
    html = r.content.decode()
    assert 'data-gate="forms-closed"' in html
    assert 'name="consent"' not in html
    r = client.post(JOIN, {"category": "company", "consent": "on"})
    assert Membership.objects.count() == 0


def test_join_form_uses_prescribed_labels_and_consent_text(client, seeded, flag_on, legal_published, person_user):
    from consents.services import consent_text_for

    client.force_login(person_user)
    html = client.get(JOIN).content.decode()
    assert locked_content.text("p2.forum.registration.category_label", "fr") in html
    for label in locked_content.get("p2.forum.registration.categories", "fr")[0]:
        assert label in html
    assert consent_text_for(ConsentPurpose.COMMUNITY).text in html
    assert 'name="consent"' in html and "checked" not in html.split('name="consent"')[1].split(">")[0]
    assert html.count("<h1") == 1


def test_join_creates_pending_membership_consent_audit_notification(
    client, seeded, flag_on, legal_published, person_user
):
    client.force_login(person_user)
    r = client.post(
        JOIN,
        {
            "category": "university_training",
            "organisation": "Université de Test",
            "consent": "on",
            "show_organisation": "on",
        },
    )
    assert r.status_code == 302 and r["Location"] == "/fr/forum-virtuel/"
    m = Membership.objects.get(user=person_user)
    assert m.status == MembershipStatus.PENDING
    assert m.category == "university_training" and m.organisation == "Université de Test"
    assert m.show_name is False and m.show_organisation is True
    assert m.accepted_terms_at is not None
    consent = ConsentRecord.objects.get(purpose=ConsentPurpose.COMMUNITY)
    assert m.consent == consent and consent.user == person_user and consent.email == person_user.email
    assert AuditEvent.objects.filter(action="community.membership.requested").exists()
    mail = EmailOutbox.objects.get(reference=f"community.Membership:{m.pk}")
    assert mail.to_email == "contact@agamieuromed.org"
    assert "Université de Test" in mail.body_text
    event = OutboundEvent.objects.get(event_type="community.membership.requested")
    assert event.payload["category"] == "university_training"
    assert "@" not in str(event.payload) and "Université" not in str(event.payload)
    html = client.get("/fr/forum-virtuel/").content.decode()
    assert "Demande d’accès en cours d’examen" in html


def test_join_requires_consent(client, seeded, flag_on, legal_published, person_user):
    client.force_login(person_user)
    r = client.post(JOIN, {"category": "company"})
    assert r.status_code == 200
    assert "Le consenso è obbligatorio" in r.content.decode() or 'role="alert"' in r.content.decode()
    assert Membership.objects.count() == 0
    assert ConsentRecord.objects.count() == 0


def test_join_rejects_unknown_category(client, seeded, flag_on, legal_published, person_user):
    client.force_login(person_user)
    r = client.post(JOIN, {"category": "hacker", "consent": "on"})
    assert r.status_code == 200 and Membership.objects.count() == 0


def test_existing_member_is_redirected(client, seeded, flag_on, legal_published, company_member):
    client.force_login(company_member.user)
    r = client.get(JOIN)
    assert r.status_code == 302 and r["Location"] == "/fr/forum-virtuel/"


def test_seeds_are_idempotent(seeded):
    from community.models import Room
    from community.seeds import seed_consent_text, seed_rooms

    first = Room.objects.count()
    assert first == 4
    Room.objects.filter(slug="entreprises").update(name_fr="Renommée")
    seed_rooms()
    seed_consent_text()
    assert Room.objects.count() == 4
    assert Room.objects.get(slug="entreprises").name_fr == "Renommée"
