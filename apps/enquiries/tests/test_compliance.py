"""Content compliance of the enquiries pages and e-mails: locked texts, forbidden wording, e-mail domain."""

import re

import pytest
from django.conf import settings
from django.core import mail

from cms import locked_content
from cms.forbidden import scan
from enquiries.tests.conftest import (
    COMPANY_URL,
    CONTACT_URL,
    DONE_URL,
    INSTITUTION_URL,
    UNIVERSITY_URL,
    company_payload,
    honeypot,
)

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

LANGS = [code for code, _ in settings.LANGUAGES]
PATHS = [
    "entreprises/recueil-des-besoins/",
    "collaboration/institutions/",
    "collaboration/universites-formation/",
    "contact/formulaire/",
    "demande-transmise/",
]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")


def _pages(client):
    for lang in LANGS:
        for path in PATHS:
            r = client.get(f"/{lang}/{path}")
            assert r.status_code == 200, (lang, path)
            yield lang, path, r.content.decode()


def test_no_forbidden_formulations_gate_closed(client, seeded):
    for lang, path, html in _pages(client):
        assert scan(html) == [], (lang, path)
        assert "®" not in html
        assert set(EMAIL_RE.findall(html)) <= {"contact@agamieuromed.org"}, (lang, path)
        assert "CONTENT_PENDING_LEGAL_REVIEW" not in html


def test_no_forbidden_formulations_gate_open(client, seeded, legal_published):
    for lang, path, html in _pages(client):
        assert scan(html) == [], (lang, path)
        assert "®" not in html
        assert set(EMAIL_RE.findall(html)) <= {"contact@agamieuromed.org"}, (lang, path)
        assert not re.search(r'(?:src|href)="https?://(?!testserver)', html), (lang, path)


def test_company_page_renders_every_locked_key_exactly(client, seeded, legal_published):
    html = client.get(COMPANY_URL).content.decode()
    for key in (
        "p1.companies.title",
        "p1.companies.intro",
        "p1.companies.quote",
        "p1.companies.form.consent",
        "p1.companies.form.button",
    ):
        assert locked_content.text(key, "fr") in html, key
    for label in locked_content.get("p1.companies.form.fields", "fr")[0]:
        assert label in html, label
    assert html.count("<h1") == 1


@pytest.mark.parametrize("lang", ["it", "en", "ar"])
def test_fallback_french_marked_with_lang_attribute(client, seeded, legal_published, lang):
    html = client.get(f"/{lang}/entreprises/recueil-des-besoins/").content.decode()
    title = locked_content.text("p1.companies.title", "fr")
    assert f'lang="fr">{title}' in html
    first_label = locked_content.get("p1.companies.form.fields", "fr")[0][0]
    assert f'<span lang="fr">{first_label}</span>' in html
    assert html.count("<h1") == 1


def test_accessibility_landmarks_and_labels(client, seeded, legal_published):
    for url in (COMPANY_URL, INSTITUTION_URL, UNIVERSITY_URL, CONTACT_URL, DONE_URL):
        html = client.get(url).content.decode()
        assert '<main id="main-content"' in html
        assert html.count("<h1") == 1, url
        assert 'aria-label="' in html  # breadcrumbs / navigation landmarks
        if url != DONE_URL:
            inputs = re.findall(r'<(?:input|textarea)[^>]*\sid="(id_[a-z_]+)"', html)
            visible = [i for i in inputs if i not in ("id_website_url", "id_form_started_at")]
            for input_id in visible:
                assert f'for="{input_id}"' in html, (url, input_id)
            assert 'type="submit"' in html
            assert "<noscript" not in html  # works without JavaScript: nothing depends on scripts


def test_notification_email_is_plain_text_and_compliant(client, seeded, legal_published):
    client.post(COMPANY_URL, honeypot(company_payload()))
    msg = mail.outbox[0]
    assert msg.to == ["contact@agamieuromed.org"]
    assert not msg.alternatives
    assert scan(msg.body) == []
    assert set(EMAIL_RE.findall(msg.body)) <= {"contact@agamieuromed.org", "maria.rossi@example.test"}
    assert "legalitalentry.it" not in msg.body
    assert "Italy Legal Entry™" in msg.body
