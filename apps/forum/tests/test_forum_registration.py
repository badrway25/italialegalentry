"""Registration form: prescribed order/labels, consent, gate G2, honeypot, duplicates, throttle, e-mails."""

from __future__ import annotations

import re

import pytest
from django.conf import settings
from django.core import mail
from django.utils.html import escape

from audit.models import AuditEvent
from cms import locked_content
from cms.forbidden import scan
from consents.models import ConsentPurpose, ConsentRecord
from core.forms import HONEYPOT_FIELD
from forum.forms import PUBLIC_FIELD_ORDER, ForumRegistrationForm
from forum.models import ForumRegistration, RegistrationCategory

# Registration is open until the event ends (2 Oct 2026, 18:00 Rome): the whole module runs at a
# moment before the Forum, never on the real date, on which every test here expired with the event.
pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("before_the_forum")]

REGISTER = "/fr/forum/inscription/"
DONE = "/fr/forum/inscription/confirmation/"


def test_title_and_intro(client, event, forms_open):
    html = client.get(REGISTER).content.decode()
    assert escape(locked_content.text("p2.forum.registration.title", "fr")) in html
    assert escape(locked_content.text("p2.forum.registration.intro", "fr")) in html
    assert html.count("<h1") == 1


def test_field_order_and_labels(event, forms_open):
    form = ForumRegistrationForm()
    public = [f.name for f in form.public_fields()]
    assert tuple(public) == PUBLIC_FIELD_ORDER
    labels = [str(form.fields[name].label) for name in public[:7]]
    assert labels == locked_content.get("p2.forum.registration.fields", "fr")[0]
    assert str(form.fields["category"].label) == "Catégorie"
    assert str(form.fields["sector_of_interest"].label) == "Secteur d’intérêt"
    # the rendered order matches too (honeypot last, hidden from humans)
    visible = [f.name for f in form.visible_fields()]
    assert visible[: len(PUBLIC_FIELD_ORDER)] == list(PUBLIC_FIELD_ORDER)
    assert visible[-1] == HONEYPOT_FIELD


def test_rendered_field_order(client, event, forms_open):
    html = client.get(REGISTER).content.decode()
    names = re.findall(r'<(?:input|select)[^>]*name="([a-z_]+)"', html)
    names = [n for n in names if n in PUBLIC_FIELD_ORDER]
    assert names == list(PUBLIC_FIELD_ORDER)


def test_category_choices_exact(event, forms_open):
    form = ForumRegistrationForm()
    labels = [str(label) for value, label in form.fields["category"].choices if value]
    assert labels == locked_content.get("p2.forum.registration.categories", "fr")[0]
    assert [value for value, _l in form.fields["category"].choices][0] == ""


def test_consent_required_and_text(client, event, forms_open, registration_payload):
    form = ForumRegistrationForm()
    assert form.fields["consent"].required is True
    assert form.fields["consent"].initial is False
    assert str(form.fields["consent"].label) == locked_content.text("p2.forum.registration.consent", "fr")
    html = client.get(REGISTER).content.decode()
    assert escape(locked_content.text("p2.forum.registration.consent", "fr")) in html
    assert 'name="consent"' in html and "checked" not in html.split('name="consent"')[1].split(">")[0]
    response = client.post(REGISTER, registration_payload(consent=""))
    assert response.status_code == 400
    assert ForumRegistration.objects.count() == 0
    assert 'aria-invalid="true"' in response.content.decode()


def test_buttons(client, event, forms_open):
    html = client.get(REGISTER).content.decode()
    label = escape(locked_content.text("p2.forum.registration.button_primary", "fr"))
    assert f'<button type="submit" class="btn btn--primary btn--lg">{label}</button>' in html


def test_privacy_link_target_it(client, event, forms_open):
    html = client.get(REGISTER).content.decode()
    assert 'href="/it/privacy-policy/" hreflang="it" data-privacy-link' in html


def test_gate_closed_get_shows_unavailable_and_post_refused(client, event, registration_payload):
    html = client.get(REGISTER).content.decode()
    assert 'data-gate="forms-closed"' in html
    assert 'id="forum-registration-form"' not in html
    response = client.post(REGISTER, registration_payload())
    assert response.status_code == 403
    assert ForumRegistration.objects.count() == 0
    assert ConsentRecord.objects.count() == 0
    assert mail.outbox == []


def test_successful_registration(client, event, forms_open, registration_payload):
    response = client.post(REGISTER, registration_payload())
    assert response.status_code == 302 and response["Location"].endswith(DONE)
    reg = ForumRegistration.objects.get()
    assert reg.email == "amina@example.test"
    assert reg.category == RegistrationCategory.INSTITUTION
    assert reg.status == "pending"
    assert reg.ip_hash and len(reg.ip_hash) == 32
    consent = reg.consent
    assert consent.purpose == ConsentPurpose.FORUM_REGISTRATION
    assert consent.consent_text.locked_key == "p2.forum.registration.consent"
    assert consent.email == reg.email
    assert AuditEvent.objects.filter(action="forum.registration.created", target_id=str(reg.pk)).exists()
    done = client.get(DONE)
    assert done.status_code == 200
    assert 'data-registration="done"' in done.content.decode()


def test_emails_to_forms_inbox_and_registrant_only(client, event, forms_open, registration_payload):
    client.post(REGISTER, registration_payload())
    assert len(mail.outbox) == 2
    recipients = {addr for m in mail.outbox for addr in m.to}
    assert recipients == {"contact@agamieuromed.org", "amina@example.test"}
    inbox = next(m for m in mail.outbox if m.to == ["contact@agamieuromed.org"])
    assert settings.ILE["FORMS_DESTINATION_EMAIL"] == "contact@agamieuromed.org"
    assert "Amina" in inbox.body and "p2.forum.registration.consent@v1" in inbox.body
    assert "Institution" in inbox.body
    ack = next(m for m in mail.outbox if m.to == ["amina@example.test"])
    assert "réception" in ack.body
    assert ack.reply_to == ["contact@agamieuromed.org"]
    for m in mail.outbox:
        assert "legalitalentry.it" not in m.body and "legalitalentry.it" not in m.subject
        assert not scan(m.body), m.body
        for word in ("garanti", "visa", "visto"):
            assert word not in m.body.lower()


def test_duplicate_email_gives_success_without_second_row(client, event, forms_open, registration_payload):
    client.post(REGISTER, registration_payload())
    mail.outbox.clear()
    response = client.post(REGISTER, registration_payload(email="AMINA@example.test", first_name="Other"))
    assert response.status_code == 302 and response["Location"].endswith(DONE)
    assert ForumRegistration.objects.count() == 1
    assert ForumRegistration.objects.get().first_name == "Amina"
    assert mail.outbox == [], "no duplicate notification"
    assert AuditEvent.objects.filter(action="forum.registration.duplicate").exists()


def test_honeypot_spam_is_swallowed(client, event, forms_open, registration_payload):
    response = client.post(REGISTER, registration_payload(**{HONEYPOT_FIELD: "http://spam.example"}))
    assert response.status_code == 302 and response["Location"].endswith(DONE)
    assert ForumRegistration.objects.count() == 0
    assert mail.outbox == []
    assert AuditEvent.objects.filter(action="forum.registration.spam_rejected").exists()


def test_too_fast_submission_is_spam(client, event, forms_open, registration_payload):
    import time

    from core.forms import TIMESTAMP_FIELD

    response = client.post(REGISTER, registration_payload(**{TIMESTAMP_FIELD: str(int(time.time()))}))
    assert response.status_code == 302
    assert ForumRegistration.objects.count() == 0


def test_throttle(client, event, forms_open, registration_payload):
    limit = settings.PUBLIC_FORM_THROTTLE["limit"]
    for i in range(limit):
        response = client.post(REGISTER, registration_payload(email=f"p{i}@example.test"))
        assert response.status_code == 302, i
    response = client.post(REGISTER, registration_payload(email="over@example.test"))
    assert response.status_code == 429
    assert ForumRegistration.objects.count() == limit
    assert AuditEvent.objects.filter(action="forum.registration.throttled").exists()


def test_validation_errors_are_accessible(client, event, forms_open, registration_payload):
    response = client.post(REGISTER, registration_payload(email="not-an-email", category=""))
    assert response.status_code == 400
    html = response.content.decode()
    assert 'role="alert"' in html
    assert 'aria-describedby="id_forum_email_errors"' in html
    assert ForumRegistration.objects.count() == 0


def test_invalid_category_rejected(client, event, forms_open, registration_payload):
    response = client.post(REGISTER, registration_payload(category="hacker"))
    assert response.status_code == 400
    assert ForumRegistration.objects.count() == 0


def test_registration_page_without_event(client, db):
    response = client.get(REGISTER)
    assert response.status_code == 200
    assert 'class="empty-state"' in response.content.decode()


def test_registration_pages_compliance(client, event, forms_open):
    for path in (REGISTER, DONE):
        for lang in ("fr", "it", "en", "ar"):
            html = client.get(path.replace("/fr/", f"/{lang}/")).content.decode()
            assert not scan(html), (path, lang)
            assert "Italy Legal Entry™" in html
