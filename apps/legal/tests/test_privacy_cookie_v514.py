"""
V5.14 — the privacy notice (A) and the cookie / technical-storage information (B) do not depend on Allegato 1.

What this file pins:

* the drafts load, in Italian (the master) and in French, English and Arabic (courtesy translations that say the
  Italian prevails), with the same sections and the same open fields in every language;
* the seed writes them as DRAFTS, never publishes them, never overwrites an editor's change or a published text;
* production refuses to publish — or to show — a document that still carries an open field «[DA COMPLETARE …]»;
  the preview shows it highlighted;
* A and B are public and reachable on their own while C and D stay unpublished, and the forms, sign-up, newsletter
  and Virtual Forum that depend on Allegato 1 stay closed (gate G1 asks for all five documents);
* the cookie register in the text matches the configuration it describes, so neither can drift unnoticed.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError

from core import gates
from legal import drafts
from legal.models import (
    OPEN_FIELD_ID_RE,
    OPEN_FIELD_PREFIX,
    TRANSLATION_LANGUAGES,
    VERIFIED_PROCESSING_KINDS,
    LegalDocument,
    LegalKind,
    LegalStatus,
    TranslationStatus,
)
from legal.services import all_official_pages_published, document_available, invalidate, publish

ROOT = Path(__file__).resolve().parents[3]
LANGS = ("it", *TRANSLATION_LANGUAGES)
SLUGS = {LegalKind.PRIVACY: "privacy-policy", LegalKind.COOKIES: "cookie-policy"}
C_AND_D = (LegalKind.NOTICES, LegalKind.TERMS, LegalKind.DISCLAIMER)


def _main(html: str) -> str:
    match = re.search(r"<main\b.*?</main>", html, flags=re.S)
    return match.group(0) if match else html


@pytest.fixture
def drafted(db):
    from legal.services import ensure_documents

    ensure_documents()
    drafts.load_drafts()
    invalidate()
    return {kind: LegalDocument.objects.get(kind=kind) for kind in VERIFIED_PROCESSING_KINDS}


@pytest.fixture
def open_fields_allowed(settings):
    settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED = True
    invalidate()
    yield
    invalidate()


# ------------------------------------------------------------------------------------------------- the texts


@pytest.mark.parametrize("kind", VERIFIED_PROCESSING_KINDS)
def test_every_language_loads_with_the_same_sections_and_open_fields(kind):
    master = drafts.read(kind, "it")
    sections = [line for line in master["body"].splitlines() if line.startswith(("## ", "### "))]
    ids = set(OPEN_FIELD_ID_RE.findall(" ".join(re.findall(r"\[DA COMPLETARE[^\]]*\]", master["body"]))))
    assert master["title"] and len(sections) >= 5
    for lang in TRANSLATION_LANGUAGES:
        entry = drafts.read(kind, lang)
        assert entry["title"] and entry["notice"] and entry["italian_link"] and entry["pending"], lang
        translated = [line for line in entry["body"].splitlines() if line.startswith(("## ", "### "))]
        assert len(translated) == len(sections), f"{kind}/{lang}: the translation must follow the master's sections"
        markers = re.findall(r"\[DA COMPLETARE[^\]]*\]", entry["body"])
        assert set(OPEN_FIELD_ID_RE.findall(" ".join(markers))) == ids, f"{kind}/{lang}: the same open fields"
        assert entry["body"].count("contact@agamieuromed.org") == master["body"].count("contact@agamieuromed.org")


@pytest.mark.parametrize(
    ("lang", "words"),
    [("fr", "la version italienne fait foi"), ("en", "the Italian version prevails"), ("ar", "النص الإيطالي")],
)
def test_each_translation_says_the_italian_prevails(lang, words):
    for kind in VERIFIED_PROCESSING_KINDS:
        assert words in drafts.read(kind, lang)["notice"]


def test_the_arabic_trademark_keeps_its_left_to_right_mark():
    for kind in VERIFIED_PROCESSING_KINDS:
        body = drafts.read(kind, "ar")["body"]
        assert "™" in body and re.search("™(?!‎)", body) is None
        assert not re.search("[٠-٩]", body), "Western digits, as in the rest of the Arabic interface"


def test_the_privacy_notice_states_only_the_verified_facts_and_leaves_the_rest_open():
    body = drafts.read(LegalKind.PRIVACY, "it")["body"]
    # verified: the controller (Annexe 1 §1.1), the Garante (Annexe 1 §8), the configured durations
    for fact in ("AGAMI — Dialogo Giuridico Interculturale APS", "contact@agamieuromed.org", "art. 77", "14 giorni"):
        assert fact in body
    # never invented: DPO, hosting region, transfers, providers are open fields, not statements
    assert "OF-08" in body and "OF-02" in body and "OF-03" in body and "OF-04" in body
    # V5.16 §10: DigitalOcean may be named as the INTENDED hosting provider; its region, DPA and transfers may not
    assert "fornitore previsto: DigitalOcean" in body
    for invented in ("Unione europea e non sono trasferiti", "Frankfurt", "Amsterdam", "FRA1", "AMS3", "DPO:"):
        assert invented not in body
    assert "fornitori esterni" not in body, "the Annexe's «external providers» sentence is false for this software"


def test_the_cookie_register_matches_the_configuration():
    from core.middleware import LanguageCookieMiddleware

    body = drafts.read(LegalKind.COOKIES, "it")["body"]
    assert settings.SESSION_COOKIE_NAME == "sessionid" and "### sessionid" in body
    assert settings.CSRF_COOKIE_NAME == "csrftoken" and "### csrftoken" in body
    assert settings.LANGUAGE_COOKIE_NAME == "ile_language" and "### ile_language" in body
    assert settings.SESSION_COOKIE_AGE == 8 * 3600 and "fino a 8 ore" in body
    assert settings.ACCOUNT_SESSION_REMEMBER is False and "fino alla chiusura del browser" in body
    assert settings.CSRF_COOKIE_AGE == 52 * 7 * 24 * 3600 and "52 settimane" in body
    assert LanguageCookieMiddleware.MAX_AGE == 365 * 24 * 3600 and "365 giorni" in body
    assert not getattr(settings, "MFA_TRUST_ENABLED", False), "allauth's «trust this browser» cookie is not listed"
    assert drafts.read(LegalKind.COOKIES, "it")["body"].count(OPEN_FIELD_PREFIX) == 0


def test_every_storage_key_named_in_the_notice_exists_in_the_front_end():
    sources = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for folder in (ROOT / "static" / "js" / "src", ROOT / "static" / "js")
        for path in folder.glob("**/*.js")
        if "dist" not in path.parts and "vendor" not in path.parts
    )
    for key in ("ile.rail", "ile.lume", "ile.hero.discovered", "ile.dismissed."):
        assert key in sources, key


def test_every_back_office_storage_key_of_the_installed_unfold_is_named_in_the_notice():
    """The back office's keys are read from the installed django-unfold, so an upgrade that adds one fails here."""
    import unfold

    app_js = (Path(unfold.__file__).resolve().parent / "static" / "unfold" / "js" / "app.js").read_text(
        encoding="utf-8"
    )
    keys = set(re.findall(r"""(?:local|session)Storage\.(?:getItem|setItem)\(\s*["']([^"']+)["']""", app_js))
    keys |= set(re.findall(r"""\$persist\([^)]*\)\.as\(\s*["']([^"']+)["']""", app_js))
    assert {"sidebarOpen", "sidebarWidth", "commandHistory", "adminTheme"} <= keys, keys
    for lang in LANGS:
        body = drafts.read(LegalKind.COOKIES, lang)["body"]
        for key in keys:
            assert key in body, f"{lang}: unfold stores «{key}» and the notice does not name it"


# ------------------------------------------------------------------------------------------------- the seed


def test_the_seed_writes_drafts_and_publishes_nothing(drafted):
    for kind, doc in drafted.items():
        assert doc.status == LegalStatus.DRAFT and doc.body_it.strip() and doc.title_it
        assert set(doc.translations) == set(TRANSLATION_LANGUAGES)
        assert doc.translation_status == TranslationStatus.PENDING
        assert doc.source_reference and "V5.14" in doc.source_reference
    for kind in C_AND_D:
        doc = LegalDocument.objects.get(kind=kind)
        assert doc.status == LegalStatus.BLOCKED and not doc.body_it.strip(), "C/D are never drafted by the team"
    assert drafts.load_drafts() == 0, "idempotent"


def test_the_seed_never_overwrites_an_editors_change_or_a_published_text(drafted, superuser):
    privacy = drafted[LegalKind.PRIVACY]
    privacy.body_it += "\nModifica del redattore.\n"
    privacy.save()
    assert drafts.apply_draft(privacy) is False
    assert "Modifica del redattore." in LegalDocument.objects.get(kind=LegalKind.PRIVACY).body_it

    cookies = drafted[LegalKind.COOKIES]
    publish(cookies, superuser)
    cookies.refresh_from_db()
    cookies.status = LegalStatus.PUBLISHED
    assert drafts.apply_draft(cookies) is False


# ------------------------------------------------------------------------------------------------- publication


def test_production_refuses_to_publish_a_document_with_an_open_field(drafted, superuser):
    assert settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED is False
    privacy = drafted[LegalKind.PRIVACY]
    assert privacy.open_fields()
    with pytest.raises(ValidationError) as exc:
        publish(privacy, superuser)
    assert "OF-01" in str(exc.value) and "OF-08" in str(exc.value)
    privacy.refresh_from_db()
    assert privacy.status == LegalStatus.DRAFT


def test_production_never_shows_a_document_with_an_open_field_even_if_its_row_says_published(drafted):
    privacy = drafted[LegalKind.PRIVACY]
    LegalDocument.objects.filter(pk=privacy.pk).update(status=LegalStatus.PUBLISHED)
    invalidate()
    privacy.refresh_from_db()
    assert privacy.is_available is False
    assert document_available(LegalKind.PRIVACY) is False


def test_an_open_field_in_a_translation_also_blocks_publication(drafted, superuser):
    cookies = drafted[LegalKind.COOKIES]
    cookies.translations["en"]["body"] += "\n[DA COMPLETARE — OF-99: test]\n"
    cookies.save()
    with pytest.raises(ValidationError):
        publish(cookies, superuser)


def test_production_settings_force_open_fields_off(tmp_path):
    env = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "config.settings.prod",
        "DJANGO_SECRET_KEY": "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s",
        "DJANGO_ALLOWED_HOSTS": "example.com",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
        "IP_HASH_SALT": "Zq3vN8rT1yW6uI0oP5aS9dF2gH7jK4lX-cV_bN1mQ8wE3rT6",
        "BACKOFFICE_MFA_ENFORCED": "1",
        "SECURE_SSL_REDIRECT": "true",
        "SECURE_HSTS_SECONDS": "31536000",
        "SECURE_HSTS_INCLUDE_SUBDOMAINS": "0",
        "SECURE_HSTS_PRELOAD": "0",
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST": "smtp.example.com",
        # No settings module reads an ILE_LEGAL_OPEN_FIELDS_ALLOWED variable; DJANGO_DEBUG is the one that matters:
        # dev.py derives the switch from DEBUG, and production must hold it False even when DEBUG is asked for.
        "DJANGO_DEBUG": "1",
    }
    code = (
        "import django, json; django.setup(); from django.conf import settings; "
        "print(json.dumps([settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED, settings.DEBUG]))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120, check=False
    )
    assert result.returncode == 0, f"prod settings did not load: {result.stderr[-800:]}"
    assert json.loads(result.stdout.strip().splitlines()[-1]) == [False, False]


@pytest.mark.parametrize("lang", ["it", "ar"])
def test_production_serves_the_blocked_notice_for_a_published_row_with_open_fields(client, drafted, lang):
    """The HTTP-level DENY: a row marked PUBLISHED that still carries an open field renders the pending notice only."""
    assert settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED is False
    privacy = drafted[LegalKind.PRIVACY]
    LegalDocument.objects.filter(pk=privacy.pk).update(status=LegalStatus.PUBLISHED)
    invalidate()
    response = client.get(f"/{lang}/privacy-policy/")
    assert response.status_code == 200
    html = _main(response.content.decode())
    assert 'data-gate="legal-blocked"' in html
    assert "DA COMPLETARE" not in html and "OF-01" not in html and "data-open-field" not in html
    body = drafts.read(LegalKind.PRIVACY, lang)["body"]
    headings = [line.lstrip("#").strip() for line in body.splitlines() if line.startswith(("## ", "### "))]
    assert len(headings) >= 5
    for heading in headings:
        assert heading not in html, f"{lang}: the body's «{heading}» reached the page"


def test_editing_a_published_text_returns_it_to_draft_until_it_is_published_again(drafted, superuser):
    """Only publish() puts a text online (permission, source, open fields, snapshot): an edit takes it offline."""
    cookies = publish(drafted[LegalKind.COOKIES], superuser)
    assert cookies.versions.count() == 1 and cookies.is_available

    cookies.save()  # a save that keeps the text keeps the publication
    cookies.refresh_from_db()
    assert cookies.status == LegalStatus.PUBLISHED

    cookies.body_it += "\nModifica non pubblicata.\n"
    cookies.save()
    cookies.refresh_from_db()
    invalidate()
    assert cookies.status == LegalStatus.DRAFT and document_available(LegalKind.COOKIES) is False

    republished = publish(cookies, superuser)
    assert republished.status == LegalStatus.PUBLISHED and republished.versions.count() == 2
    republished.translations["en"]["body"] += "\nEdited translation.\n"
    republished.save()
    republished.refresh_from_db()
    assert republished.status == LegalStatus.DRAFT, "a translation edit is a change of text too"
    latest = republished.versions.order_by("-version").first()
    assert "Modifica non pubblicata." in latest.body_it
    assert "Edited translation." not in json.dumps(latest.translations, ensure_ascii=False)


def test_the_back_office_change_form_cannot_change_a_live_text(drafted, superuser):
    from django.contrib.admin.sites import AdminSite
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.test import RequestFactory

    from legal.admin import LegalDocumentAdmin

    cookies = publish(drafted[LegalKind.COOKIES], superuser)
    request = RequestFactory().post("/backoffice/")
    request.user = superuser
    request.session = {}
    request._messages = FallbackStorage(request)
    cookies.body_it += "\nRitocco dal back office.\n"
    LegalDocumentAdmin(LegalDocument, AdminSite()).save_model(request, cookies, form=None, change=True)
    cookies.refresh_from_db()
    assert cookies.status == LegalStatus.DRAFT and cookies.versions.count() == 1
    assert any("non è più visibile online" in str(message) for message in request._messages)


def test_the_cookie_information_is_publishable_now_and_public_in_every_language(client, drafted, superuser):
    publish(drafted[LegalKind.COOKIES], superuser)
    invalidate()
    for lang in LANGS:
        html = _main(client.get(f"/{lang}/cookie-policy/").content.decode())
        assert 'data-gate="legal-blocked"' not in html
        assert "### " not in html and "<h3>sessionid</h3>" in html and "<h3>ile.rail (localStorage)</h3>" in html
        if lang == "it":
            assert 'lang="it"' in html and "data-courtesy-translation" not in html
        else:
            assert f'lang="{lang}" data-courtesy-translation' in html
            assert 'href="/it/cookie-policy/" hreflang="it" data-italian-version' in html
            assert drafts.read(LegalKind.COOKIES, lang)["notice"] in html
            assert "data-translation-pending" not in html, "the review flag is metadata in production"
    assert document_available(LegalKind.COOKIES) is True


def test_the_preview_shows_the_privacy_notice_with_its_open_fields_highlighted(
    client, drafted, superuser, open_fields_allowed
):
    publish(drafted[LegalKind.PRIVACY], superuser)
    invalidate()
    for lang in LANGS:
        html = _main(client.get(f"/{lang}/privacy-policy/").content.decode())
        assert (
            '<mark class="legal-open-field" data-open-field data-open-field-class="owner-confirmation">'
            "[DA COMPLETARE — OF-01 — OWNER CONFIRMATION REQUIRED"
        ) in html
        assert 'data-open-fields="11"' in html and "OF-12" in html and "OF-13" in html
    assert "data-translation-pending" in _main(client.get("/fr/privacy-policy/").content.decode())


# ------------------------------------------------------------------------------------------------- logging


def test_a_django_request_line_reaches_no_output_unredacted_under_debug(settings):
    """Django's DEFAULT_LOGGING handlers are detached: every django.* line goes through the redacting root handler."""
    import io
    import logging

    settings.DEBUG = True  # Django's own console handler printed only under DEBUG (RequireDebugTrue)
    assert logging.getLogger("django").handlers == []
    logger = logging.getLogger("django.request")
    handlers, node = [], logger
    while node is not None:
        handlers.extend(h for h in node.handlers if not type(h).__module__.startswith("_pytest"))
        node = node.parent if node.propagate else None
    assert handlers, "the root console handler"
    swapped = []
    for handler in handlers:
        assert type(handler) is logging.StreamHandler, f"an unexpected handler: {handler!r}"
        swapped.append((handler, handler.setStream(io.StringIO())))
    try:
        logger.error("Not Found: /it/conto/?email=%s", "mario.rossi@example.com")
        output = "".join(handler.stream.getvalue() for handler, _ in swapped)
    finally:
        for handler, stream in swapped:
            handler.setStream(stream)
    assert "Not Found" in output and "[e-mail]" in output
    assert "mario.rossi@example.com" not in output


# ------------------------------------------------------------------------------------------------- gate G1


def test_privacy_and_cookies_public_keep_every_allegato_1_flow_closed(
    client, seeded, superuser, set_flag, open_fields_allowed
):
    drafts.load_drafts()
    for kind in VERIFIED_PROCESSING_KINDS:
        publish(LegalDocument.objects.get(kind=kind), superuser)
    invalidate()
    set_flag("newsletter", True)
    set_flag("virtual_forum", True)

    assert document_available(LegalKind.PRIVACY) and document_available(LegalKind.COOKIES)
    for kind in C_AND_D:
        assert not document_available(kind)
        slug = LegalDocument.objects.get(kind=kind).slug
        assert 'data-gate="legal-blocked"' in client.get(f"/fr/{slug}/").content.decode()
    assert all_official_pages_published() is False
    assert gates.legal_pages_available() is False
    assert gates.public_forms_enabled().open is False
    assert gates.newsletter_enabled() is False
    assert gates.virtual_forum_enabled() is False
    assert "Inscriptions ferm" in client.get("/fr/compte/signup/").content.decode()
    for slug in SLUGS.values():
        assert client.get(f"/fr/{slug}/").status_code == 200
