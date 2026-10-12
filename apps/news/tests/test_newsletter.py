"""Newsletter « Restez informés » — separate, explicit, never pre-ticked, revocable consent with double opt-in."""

import re

import pytest
from django.core import mail

from audit.models import AuditEvent
from cms import locked_content
from consents.models import ConsentPurpose, ConsentRecord, NewsletterSubscription
from news.forms import NewsletterForm
from notifications.models import EmailOutbox

pytestmark = pytest.mark.django_db

INDEX = "/fr/actualites/"
SUBSCRIBE = "/fr/actualites/lettre-d-information/"
CONSENT_TEXT = locked_content.text("p3.news.newsletter_consent", "fr")
LABEL_TEXT = locked_content.text("p3.news.newsletter_label", "fr")


def test_block_hidden_when_flag_off(client, legal_published):
    html = client.get(INDEX).content.decode()
    assert LABEL_TEXT not in html
    assert 'id="newsletter"' not in html


def test_block_shows_unavailable_notice_when_forms_gate_closed(client, newsletter_on):
    html = client.get(INDEX).content.decode()
    assert LABEL_TEXT in html
    assert 'data-gate="forms-closed"' in html
    assert 'action="/fr/actualites/lettre-d-information/"' not in html


def test_form_label_and_separate_consent_not_prechecked(client, newsletter_on, legal_published):
    html = client.get(INDEX).content.decode()
    assert LABEL_TEXT in html
    assert CONSENT_TEXT in html
    assert 'action="/fr/actualites/lettre-d-information/"' in html
    checkbox = re.search(r'<input[^>]*name="consent"[^>]*>', html).group(0)
    assert "checked" not in checkbox
    assert 'type="checkbox"' in checkbox
    assert "required" in checkbox
    form = NewsletterForm()
    assert form.fields["consent"].initial is False
    assert form.fields["consent"].required is True
    assert str(form.fields["consent"].label) == CONSENT_TEXT


def test_consent_is_mandatory(client, newsletter_on, legal_published, honeypot_ok):
    r = client.post(SUBSCRIBE, {"email": "person@example.test", **honeypot_ok})
    assert r.status_code == 200
    html = r.content.decode()
    assert "Le consenso è obbligatorio" in html or "consenso" in html.lower() or "form-field--error" in html
    assert 'aria-invalid="true"' in html
    assert 'aria-describedby="id_consent_error"' in html
    assert 'id="id_consent_error"' in html
    assert NewsletterSubscription.objects.count() == 0
    assert ConsentRecord.objects.count() == 0
    assert EmailOutbox.objects.count() == 0


def test_invalid_email_rejected(client, newsletter_on, legal_published, honeypot_ok):
    r = client.post(SUBSCRIBE, {"email": "not-an-email", "consent": "on", **honeypot_ok})
    assert r.status_code == 200
    assert NewsletterSubscription.objects.count() == 0


def test_subscribe_confirm_unsubscribe_flow(client, newsletter_on, legal_published, honeypot_ok):
    r = client.post(SUBSCRIBE, {"email": "Person@Example.test", "consent": "on", **honeypot_ok}, follow=True)
    assert r.status_code == 200
    assert "e-mail de confirmation" in r.content.decode()
    sub = NewsletterSubscription.objects.get()
    assert sub.email == "person@example.test"
    assert sub.confirmed_at is None and sub.unsubscribed_at is None and not sub.is_active
    consent = sub.consent
    assert consent.purpose == ConsentPurpose.NEWSLETTER
    assert consent.consent_text.locked_key == "p3.news.newsletter_consent"
    assert consent.consent_text.text == CONSENT_TEXT
    assert consent.ip_hash and len(consent.ip_hash) == 32
    assert ConsentRecord.objects.exclude(purpose=ConsentPurpose.NEWSLETTER).count() == 0, (
        "never linked to other consents"
    )
    # double opt-in e-mail queued in the outbox and delivered to the test mailbox
    outbox = EmailOutbox.objects.get(to_email="person@example.test")
    assert sub.confirm_token in outbox.body_text
    assert sub.unsubscribe_token in outbox.body_text
    assert "legalitalentry.it" not in outbox.body_text
    assert len(mail.outbox) >= 1
    delivered = [m for m in mail.outbox if m.to == ["person@example.test"]]
    assert delivered and sub.confirm_token in delivered[0].body
    # staff inbox notice contains no personal data
    notice = EmailOutbox.objects.get(to_email="contact@agamieuromed.org")
    assert "person@example.test" not in notice.body_text
    assert AuditEvent.objects.filter(action="newsletter.created").exists()

    confirm_url = f"/fr/consentements/newsletter/confirmer/{sub.confirm_token}/"
    assert client.get(confirm_url).status_code == 200
    client.post(confirm_url)
    sub.refresh_from_db()
    assert sub.confirmed_at is not None and sub.is_active

    unsub_url = f"/fr/consentements/newsletter/desinscription/{sub.unsubscribe_token}/"
    client.post(unsub_url)
    sub.refresh_from_db()
    consent.refresh_from_db()
    assert sub.unsubscribed_at is not None and not sub.is_active
    assert consent.withdrawn_at is not None, "revocation is recorded on the consent"


def test_resubscribe_after_unsubscribe_creates_new_consent_and_tokens(
    client, newsletter_on, legal_published, honeypot_ok
):
    client.post(SUBSCRIBE, {"email": "again@example.test", "consent": "on", **honeypot_ok})
    sub = NewsletterSubscription.objects.get()
    old_consent, old_token = sub.consent_id, sub.confirm_token
    client.post(f"/fr/consentements/newsletter/confirmer/{sub.confirm_token}/")
    client.post(f"/fr/consentements/newsletter/desinscription/{sub.unsubscribe_token}/")
    client.post(SUBSCRIBE, {"email": "again@example.test", "consent": "on", **honeypot_ok})
    sub.refresh_from_db()
    assert sub.consent_id != old_consent and sub.confirm_token != old_token
    assert sub.unsubscribed_at is None and sub.confirmed_at is None
    assert ConsentRecord.objects.filter(email="again@example.test").count() == 2
    assert EmailOutbox.objects.filter(to_email="again@example.test").count() == 2


def test_pending_request_resends_without_new_consent(client, newsletter_on, legal_published, honeypot_ok):
    client.post(SUBSCRIBE, {"email": "twice@example.test", "consent": "on", **honeypot_ok})
    client.post(SUBSCRIBE, {"email": "twice@example.test", "consent": "on", **honeypot_ok})
    assert NewsletterSubscription.objects.count() == 1
    assert ConsentRecord.objects.count() == 1
    assert EmailOutbox.objects.filter(to_email="twice@example.test").count() == 2


def test_active_subscriber_is_not_mailed_again(client, newsletter_on, legal_published, honeypot_ok):
    client.post(SUBSCRIBE, {"email": "active@example.test", "consent": "on", **honeypot_ok})
    sub = NewsletterSubscription.objects.get()
    client.post(f"/fr/consentements/newsletter/confirmer/{sub.confirm_token}/")
    r = client.post(SUBSCRIBE, {"email": "active@example.test", "consent": "on", **honeypot_ok}, follow=True)
    assert r.status_code == 200
    assert "e-mail de confirmation" in r.content.decode(), "same generic message (no enumeration)"
    assert EmailOutbox.objects.filter(to_email="active@example.test").count() == 1
    assert ConsentRecord.objects.count() == 1


def test_no_subscription_when_forms_gate_closed(client, newsletter_on, honeypot_ok):
    r = client.post(SUBSCRIBE, {"email": "gated@example.test", "consent": "on", **honeypot_ok})
    assert r.status_code == 403
    assert 'data-gate="forms-closed"' in r.content.decode()
    assert NewsletterSubscription.objects.count() == 0
    assert ConsentRecord.objects.count() == 0
    assert EmailOutbox.objects.count() == 0
    assert mail.outbox == []


def test_no_subscription_when_newsletter_flag_off(client, legal_published, honeypot_ok):
    r = client.post(SUBSCRIBE, {"email": "off@example.test", "consent": "on", **honeypot_ok})
    assert r.status_code == 404
    assert NewsletterSubscription.objects.count() == 0
    assert EmailOutbox.objects.count() == 0


def test_honeypot_spam_gets_success_without_saving(client, newsletter_on, legal_published, honeypot_ok):
    data = {"email": "bot@example.test", "consent": "on", **honeypot_ok, "website_url": "http://spam.example"}
    r = client.post(SUBSCRIBE, data, follow=True)
    assert r.status_code == 200
    assert "e-mail de confirmation" in r.content.decode()
    assert NewsletterSubscription.objects.count() == 0
    assert EmailOutbox.objects.count() == 0
    # too fast (timing check)
    r = client.post(
        SUBSCRIBE, {"email": "fast@example.test", "consent": "on", "website_url": "", "form_started_at": "0"}
    )
    assert r.status_code == 302
    assert NewsletterSubscription.objects.count() == 0


def test_throttle_returns_429(client, newsletter_on, legal_published, honeypot_ok, settings):
    limit = settings.PUBLIC_FORM_THROTTLE["limit"]
    for i in range(limit):
        r = client.post(SUBSCRIBE, {"email": f"t{i}@example.test", "consent": "on", **honeypot_ok})
        assert r.status_code == 302
    r = client.post(SUBSCRIBE, {"email": "over@example.test", "consent": "on", **honeypot_ok})
    assert r.status_code == 429
    assert NewsletterSubscription.objects.filter(email="over@example.test").count() == 0


def test_get_not_allowed_on_subscribe_endpoint(client, newsletter_on, legal_published):
    assert client.get(SUBSCRIBE).status_code == 405


def test_consent_label_uses_locked_text_in_other_languages(client, newsletter_on, legal_published):
    html = client.get("/en/actualites/").content.decode()
    assert CONSENT_TEXT in html
    assert 'lang="fr"' in html
    with __import__("django").utils.translation.override("ar"):
        form = NewsletterForm()
        assert str(form.fields["consent"].label) == CONSENT_TEXT
        assert form.consent_is_fallback is True and form.consent_language == "fr"
