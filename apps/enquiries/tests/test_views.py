"""Integration tests for the public form views: gate G2, throttle, spam, duplicates, e-mail, audit."""

import pytest
from django.conf import settings
from django.core import mail
from django.test import Client
from freezegun import freeze_time

from audit.models import AuditEvent
from cms import locked_content
from consents.models import ConsentRecord
from core import flags
from core.public_routes import all_routes
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest, ProposalKind
from enquiries.tests.conftest import (
    COMPANY_URL,
    CONTACT_URL,
    DONE_URL,
    INBOX,
    INSTITUTION_URL,
    UNIVERSITY_URL,
    collaboration_payload,
    company_payload,
    contact_payload,
    honeypot,
)

pytestmark = pytest.mark.django_db

LANGS = [code for code, _ in settings.LANGUAGES]
ALL_PATHS = [
    "entreprises/recueil-des-besoins/",
    "collaboration/institutions/",
    "collaboration/universites-formation/",
    "contact/formulaire/",
    "demande-transmise/",
]


def test_all_routes_registered_without_gate():
    registered = {r.path: r for r in all_routes() if r.app == "enquiries"}
    for path in ALL_PATHS:
        assert path in registered, path
        assert registered[path].requires_gate == ""


@pytest.mark.parametrize("lang", LANGS)
def test_routes_render_200_in_every_language(client, seeded, lang):
    for path in ALL_PATHS:
        r = client.get(f"/{lang}/{path}")
        assert r.status_code == 200, (lang, path)
        html = r.content.decode()
        assert "Italy Legal Entry™" in html
        assert f'<html lang="{lang}"' in html


# ---- gate G2 ------------------------------------------------------------------------------------


def test_gate_closed_get_shows_unavailable_and_post_rejected(client, seeded):
    r = client.get(COMPANY_URL)
    html = r.content.decode()
    assert r.status_code == 200
    assert 'data-gate="forms-closed"' in html
    assert '<form method="post"' not in html
    assert INBOX in html
    r = client.post(COMPANY_URL, honeypot(company_payload()))
    assert r.status_code == 403
    assert CompanyNeedsRequest.objects.count() == 0
    assert ConsentRecord.objects.count() == 0
    assert mail.outbox == []


@pytest.mark.parametrize("url", [INSTITUTION_URL, UNIVERSITY_URL, CONTACT_URL])
def test_gate_closed_for_every_form(client, seeded, url):
    assert 'data-gate="forms-closed"' in client.get(url).content.decode()
    r = client.post(url, honeypot(collaboration_payload()))
    assert r.status_code == 403
    assert CollaborationProposal.objects.count() == 0
    assert ContactRequest.objects.count() == 0


def test_gate_open_renders_form_with_locked_texts(client, seeded, legal_published):
    html = client.get(COMPANY_URL).content.decode()
    assert '<form method="post"' in html
    assert 'data-gate="forms-closed"' not in html
    for key in ("p1.companies.title", "p1.companies.intro", "p1.companies.quote", "p1.companies.form.button"):
        assert locked_content.text(key, "fr") in html, key
    assert locked_content.text("p1.companies.form.consent", "fr") in html
    labels = locked_content.get("p1.companies.form.fields", "fr")[0]
    positions = [html.index(label) for label in labels]
    assert positions == sorted(positions), "labels must appear in the prescribed order"
    assert 'name="consent"' in html and "checked" not in html.split('name="consent"')[1].split(">")[0]


# ---- successful submission ------------------------------------------------------------------------


def test_company_submission_creates_row_consent_email_and_audit(client, seeded, legal_published):
    r = client.post(COMPANY_URL, honeypot(company_payload()), HTTP_USER_AGENT="pytest/1.0")
    assert r.status_code == 302
    assert r["Location"].startswith(DONE_URL)
    obj = CompanyNeedsRequest.objects.get()
    assert obj.company_name == "Officine Meccaniche Rossi S.r.l."
    assert obj.email == "maria.rossi@example.test"  # normalised
    assert obj.language == "fr"
    assert obj.source_path == COMPANY_URL
    assert obj.owner is None
    assert obj.ip_hash and len(obj.ip_hash) == 32 and "127.0.0.1" not in obj.ip_hash
    assert obj.user_agent == "pytest/1.0"
    assert obj.duplicate_hash and len(obj.duplicate_hash) == 64
    assert obj.last_contact_at is not None
    consent = obj.consent
    assert consent.purpose == "company_needs"
    assert consent.email == obj.email
    assert consent.consent_text.locked_key == "p1.companies.form.consent"
    assert consent.consent_text.version == 1
    assert consent.consent_text.text == locked_content.text("p1.companies.form.consent", "fr")
    assert consent.given_at is not None
    # single notification, to the configured inbox only, plain text listing the fields
    assert len(mail.outbox) == 1
    msg = mail.outbox[0]
    assert msg.to == [INBOX]
    assert not msg.alternatives
    assert "Officine Meccaniche Rossi" in msg.body
    assert "Soudeurs, opérateurs CNC" in msg.body
    assert locked_content.get("p1.companies.form.fields", "fr")[0][0] in msg.body
    assert "p1.companies.form.consent" in msg.body
    assert "&#" not in msg.body and "&amp;" not in msg.body
    assert AuditEvent.objects.filter(action="enquiries.submitted", target_id=str(obj.pk)).exists()
    # follow the redirect: sober confirmation, no promise, not indexed
    done = client.get(r["Location"])
    assert done.status_code == 200
    html = done.content.decode()
    assert 'name="robots" content="noindex' in html
    assert "garanti" in html  # « ni une garantie de résultat »


def test_authenticated_submitter_becomes_owner(client, seeded, legal_published, person_user):
    client.force_login(person_user)
    client.post(COMPANY_URL, honeypot(company_payload(email="other@example.test")))
    obj = CompanyNeedsRequest.objects.get()
    assert obj.owner == person_user
    assert obj.consent.user == person_user


def test_invalid_payload_rerenders_with_errors_and_stores_nothing(client, seeded, legal_published):
    r = client.post(COMPANY_URL, honeypot(company_payload(email="not-an-email", consent="")))
    assert r.status_code == 200
    html = r.content.decode()
    assert 'aria-invalid="true"' in html
    assert "_error" in html
    assert CompanyNeedsRequest.objects.count() == 0
    assert mail.outbox == []


def test_csrf_enforced(seeded, legal_published):
    csrf_client = Client(enforce_csrf_checks=True)
    r = csrf_client.post(COMPANY_URL, honeypot(company_payload()))
    assert r.status_code == 403
    assert CompanyNeedsRequest.objects.count() == 0


# ---- anti-spam ----------------------------------------------------------------------------------


def test_honeypot_spam_gets_success_but_nothing_is_stored(client, seeded, legal_published):
    r = client.post(COMPANY_URL, honeypot(company_payload(), website_url="http://spam.example"))
    assert r.status_code == 302 and r["Location"].startswith(DONE_URL)
    assert CompanyNeedsRequest.objects.count() == 0
    assert ConsentRecord.objects.count() == 0
    assert mail.outbox == []
    assert AuditEvent.objects.filter(action="enquiries.spam_dropped").exists()


def test_time_trap_spam_dropped(client, seeded, legal_published):
    r = client.post(COMPANY_URL, honeypot(company_payload(), started_seconds_ago=0))
    assert r.status_code == 302
    assert CompanyNeedsRequest.objects.count() == 0


def test_throttle_returns_429_after_limit(client, seeded, legal_published):
    limit = settings.PUBLIC_FORM_THROTTLE["limit"]
    payload = honeypot(company_payload(consent=""))  # invalid on purpose: nothing is stored
    for _ in range(limit):
        assert client.post(COMPANY_URL, payload).status_code == 200
    r = client.post(COMPANY_URL, payload)
    assert r.status_code == 429
    assert "errors/429.html" in [t.name for t in r.templates]
    assert client.get(COMPANY_URL).status_code == 200  # GET is never throttled


def test_duplicate_within_24h_is_suppressed(client, seeded, legal_published):
    with freeze_time("2026-09-17 10:00:00"):
        flags.invalidate()
        assert client.post(COMPANY_URL, honeypot(company_payload())).status_code == 302
        r = client.post(COMPANY_URL, honeypot(company_payload(email="MARIA.ROSSI@example.test")))
        assert r.status_code == 302 and r["Location"].startswith(DONE_URL)
    assert CompanyNeedsRequest.objects.count() == 1
    assert len(mail.outbox) == 1
    assert AuditEvent.objects.filter(action="enquiries.duplicate").count() == 1
    with freeze_time("2026-09-18 11:00:00"):
        flags.invalidate()
        assert client.post(COMPANY_URL, honeypot(company_payload())).status_code == 302
    assert CompanyNeedsRequest.objects.count() == 2


def test_different_content_is_not_a_duplicate(client, seeded, legal_published):
    client.post(COMPANY_URL, honeypot(company_payload()))
    client.post(COMPANY_URL, honeypot(company_payload(profiles_needed="Électriciens")))
    assert CompanyNeedsRequest.objects.count() == 2


# ---- collaboration & contact --------------------------------------------------------------------


def test_institution_proposal_sets_kind_and_purpose(client, seeded, legal_published):
    r = client.post(INSTITUTION_URL, honeypot(collaboration_payload()))
    assert r.status_code == 302
    obj = CollaborationProposal.objects.get()
    assert obj.kind == ProposalKind.INSTITUTION
    assert obj.consent.purpose == "institution_proposal"
    assert obj.consent.consent_text.locked_key == "p1.companies.form.consent"
    assert mail.outbox[0].to == [INBOX]
    assert "Université de Casablanca" in mail.outbox[0].body


def test_university_proposal_sets_kind_and_purpose(client, seeded, legal_published):
    client.post(UNIVERSITY_URL, honeypot(collaboration_payload()))
    obj = CollaborationProposal.objects.get()
    assert obj.kind == ProposalKind.UNIVERSITY
    assert obj.consent.purpose == "university_proposal"


def test_collaboration_button_generic_before_phase3(client, seeded, legal_published, before_phase3):
    generic = locked_content.text("p2.forum.registration.button_secondary_collab", "fr")
    html = client.get(INSTITUTION_URL).content.decode()
    assert generic in html
    assert locked_content.text("p3.institutions.button", "fr") not in html
    assert locked_content.text("p3.institutions.intro", "fr") not in html
    html = client.get(UNIVERSITY_URL).content.decode()
    assert generic in html
    assert locked_content.text("p3.universities.button", "fr") not in html


def test_collaboration_button_prescribed_after_phase3(client, seeded, legal_published, phase3_open):
    html = client.get(INSTITUTION_URL).content.decode()
    assert locked_content.text("p3.institutions.button", "fr") in html
    assert locked_content.text("p3.institutions.intro", "fr") in html
    assert locked_content.text("p3.institutions.recipients", "fr") in html
    html = client.get(UNIVERSITY_URL).content.decode()
    assert locked_content.text("p3.universities.button", "fr") in html
    assert locked_content.text("p3.universities.intro", "fr") in html


def test_contact_submission(client, seeded, legal_published):
    r = client.post(CONTACT_URL, honeypot(contact_payload()))
    assert r.status_code == 302
    obj = ContactRequest.objects.get()
    assert obj.subject == "Question sur le projet"
    assert obj.consent.purpose == "contact"
    assert len(mail.outbox) == 1 and mail.outbox[0].to == [INBOX]
    assert "Question sur le projet" in mail.outbox[0].body


def test_done_page_ignores_unknown_kind(client, seeded):
    r = client.get(DONE_URL + "?k=<script>")
    assert r.status_code == 200
    html = r.content.decode()
    assert "<script>" not in html.split("<main")[1].split("</main>")[0]
    assert 'data-enquiry-done=""' in html


def test_acknowledgement_is_optional_and_neutral(client, seeded, legal_published, settings):
    settings.ENQUIRIES_ACKNOWLEDGE_SUBMITTER = True
    client.post(COMPANY_URL, honeypot(company_payload()))
    recipients = sorted(m.to[0] for m in mail.outbox)
    assert recipients == [INBOX, "maria.rossi@example.test"]
    ack = next(m for m in mail.outbox if m.to == ["maria.rossi@example.test"])
    assert "Officine Meccaniche Rossi" not in ack.body
    assert "Soudeurs" not in ack.body
    assert "garantie" in ack.body
