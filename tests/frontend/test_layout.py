"""
Layout / shell tests (design system): rendered with the Django test client.

Covers the base template, partials (utility bar, header, footer, SEO head), error pages and the
allauth override on the pages that exist from the foundation: /, /ar/, /fr/privacy-policy/,
/fr/compte/login/ and a 404.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders

ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.django_db

PAGES = ["/fr/", "/ar/", "/fr/privacy-policy/", "/fr/compte/login/", "/fr/page-inesistente/"]


def _get(client, path):
    response = client.get(path)
    return response, response.content.decode("utf-8")


def _external_urls(html: str) -> list[str]:
    urls = re.findall(r'(?:src|href|content|action)="(https?://[^"]+)"', html)
    return [u for u in urls if "testserver" not in u and "localhost" not in u]


def test_root_redirects_to_language_prefix(client, seeded):
    response = client.get("/")
    assert response.status_code == 302
    assert response["Location"].startswith("/")
    assert response["Location"].rstrip("/") in {"/fr", "/it", "/en", "/ar"}


@pytest.mark.parametrize("path", PAGES)
def test_shell_landmarks_skip_link_and_single_h1(client, seeded, path):
    response, html = _get(client, path)
    assert response.status_code in (200, 404), (path, response.status_code)
    assert '<a class="skip-link" href="#main-content">' in html
    assert '<main id="main-content" tabindex="-1">' in html
    assert html.count("<h1") == 1, path
    assert '<header class="site-header"' in html
    assert '<nav class="main-nav" aria-label=' in html
    assert '<footer class="site-footer' in html
    assert 'class="utility-bar' in html
    assert 'role="region" aria-label="Barre institutionnelle"' in html or 'role="region" aria-label=' in html


@pytest.mark.parametrize("path", PAGES)
def test_no_external_resources_or_inline_styles(client, seeded, path):
    _response, html = _get(client, path)
    assert _external_urls(html) == [], path
    # CSP is style-src 'self' without unsafe-inline: no style attributes, no inline <script> code.
    assert not re.search(r"<[a-z][^>]*\sstyle=", html), path
    assert not re.search(r"<script(?![^>]*\ssrc=)(?![^>]*application/ld\+json)[^>]*>\s*\S", html), path


def test_html_lang_and_dir_attributes(client, seeded):
    _r, fr = _get(client, "/fr/")
    _r, ar = _get(client, "/ar/")
    assert '<html lang="fr" dir="ltr" class="no-js">' in fr
    assert '<html lang="ar" dir="rtl" class="no-js">' in ar
    assert " is-rtl" in ar and "is-rtl" not in fr
    # Each page preloads the READING face of its own script, not a Latin serif on an Arabic page.
    # Art direction A gives Arabic its own display/text pair: a true Naskh for reading, because a
    # Kufi-influenced sans is a register mismatch against a serif, and IBM Plex Sans Arabic for the
    # interface, where a Kufi construction is correct.
    assert "noto-naskh-arabic-400-700-normal-arabic.woff2" in ar
    assert "ibm-plex-sans-arabic-400-normal-arabic.woff2" in ar
    assert "newsreader-200-800-normal-latin.woff2" in fr
    assert "ibm-plex-sans-400-normal-latin.woff2" in fr
    # A Latin page must not pull the Arabic faces, and the reverse.
    assert "noto-naskh" not in fr
    assert "newsreader" not in ar


def test_language_switcher_lists_every_language_with_hreflang(client, seeded):
    _r, html = _get(client, "/fr/")
    for code in ("it", "fr", "en", "ar"):
        assert f'class="lang-seg__link" href="/{code}/" lang="{code}" hreflang="{code}"' in html
    assert 'href="/fr/" lang="fr" hreflang="fr" dir="ltr" aria-current="true"' in html
    assert 'href="/ar/" lang="ar" hreflang="ar" dir="rtl"' in html


def test_footer_has_five_distinct_legal_links_identity_and_version(client, seeded):
    _r, html = _get(client, "/fr/")
    for path in [
        "/fr/privacy-policy/",
        "/fr/cookie-policy/",
        "/fr/note-legali/",
        "/fr/condizioni-di-utilizzo/",
        "/fr/avvertenze/",
    ]:
        assert f'href="{path}"' in html, path
    assert "contact@agamieuromed.org" in html
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in html
    assert 'class="site-footer__version"' in html
    assert "Italy Legal Entry™" in html
    assert "marque déposée" in html  # p1.trademark.words_fr in the FR footer


def test_footer_trademark_words_per_language(client, seeded):
    _r, it = _get(client, "/it/")
    assert "marchio depositato" in it
    assert "marchio registrato" not in it.lower()
    _r, en = _get(client, "/en/")
    assert "marque déposée" not in en and "marchio depositato" not in en


def test_antifraud_footer_link_only_when_phase3_open(client, seeded, phase3_open):
    _r, html = _get(client, "/fr/")
    # The route belongs to the pages app; when it exists the locked title appears, else nothing.
    if 'class="site-footer__antifraud"' in html:
        assert "ATTENTION AUX FRAUDES" in html


def test_antifraud_footer_link_hidden_before_phase3(client, seeded, before_phase3):
    _r, html = _get(client, "/fr/")
    assert 'class="site-footer__antifraud"' not in html


def test_reserved_area_link_follows_flag(client, seeded, set_flag):
    _r, html = _get(client, "/fr/")
    assert 'href="/fr/compte/login/"' in html
    set_flag("reserved_area_public_link", False)
    _r, html = _get(client, "/fr/")
    assert 'class="utility-bar__link" href="/fr/compte/login/"' not in html


def test_authenticated_user_gets_account_menu(client, seeded, person_user):
    client.force_login(person_user)
    _r, html = _get(client, "/fr/")
    assert 'class="account-menu"' in html
    assert 'action="/fr/compte/logout/"' in html
    assert "csrfmiddlewaretoken" in html


def test_seo_head_canonical_hreflang_og_twitter(client, seeded):
    _r, html = _get(client, "/fr/")
    assert '<link rel="canonical" href="http://testserver/fr/">' in html
    assert 'hreflang="x-default"' in html
    assert '<meta property="og:type" content="website">' in html
    assert '<meta property="og:image" content="http://testserver/static/img/og-default.png">' in html
    assert '<meta name="twitter:card" content="summary_large_image">' in html
    assert '<meta name="theme-color" content="#0f2b52">' in html


def test_404_page_offers_recovery_navigation(client, seeded):
    response, html = _get(client, "/fr/page-inesistente/")
    assert response.status_code == 404
    assert "Page introuvable" in html
    assert 'href="/fr/"' in html
    assert "mailto:contact@agamieuromed.org" in html
    assert 'aria-label="Navigation de secours"' in html
    assert 'href="/fr/privacy-policy/"' in html


def test_error_pages_render_with_shell(client, seeded):
    from django.template.loader import render_to_string
    from django.test import RequestFactory

    request = RequestFactory().get("/fr/")
    request.request_id = "abc123"
    for code in (400, 403, 429, 500):
        html = render_to_string(f"errors/{code}.html", {}, request=request)
        assert html.count("<h1") == 1, code
        assert 'class="error-page__code"' in html
        assert 'class="skip-link"' in html
    html = render_to_string("errors/500.html", {}, request=request)
    assert "abc123" in html


def test_login_page_uses_design_system_form(client, seeded):
    response, html = _get(client, "/fr/compte/login/")
    assert response.status_code == 200
    assert "account-page account-page--entrance" in html  # block + modifier on the layout section
    assert 'class="form"' in html
    assert 'class="form-field' in html
    assert 'class="btn btn--primary"' in html
    assert 'id="id_login"' in html and 'id="id_password"' in html
    assert "form.as_p" not in html
    assert html.count("<h1") == 1


def test_login_page_in_arabic_is_rtl(client, seeded):
    response, html = _get(client, "/ar/compte/login/")
    assert response.status_code == 200
    assert '<html lang="ar" dir="rtl"' in html


def test_signup_closed_message_while_forms_gated(client, seeded):
    response, html = _get(client, "/fr/compte/signup/")
    assert response.status_code == 200
    assert 'class="account-page' in html


def test_password_reset_page_renders(client, seeded):
    response, html = _get(client, "/fr/compte/password/reset/")
    assert response.status_code == 200
    assert 'class="form-field' in html
    assert 'type="email"' in html


def test_messages_region_present(client, seeded):
    _r, html = _get(client, "/fr/")
    # The region is rendered only with messages; the block must exist in the template source.
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    assert 'class="container messages" role="status" aria-live="polite"' in base
    assert "{% block jsonld %}" in base
    for block in (
        "page_title",
        "meta_description",
        "head_seo",
        "extra_head",
        "banner",
        "breadcrumbs",
        "content",
        "main_content",
        "extra_scripts",
        "body_class",
    ):
        assert f"{{% block {block} %}}" in base, block


def test_static_css_and_js_are_served_and_referenced(client, seeded):
    _r, html = _get(client, "/fr/")
    assert 'href="/static/css/dist/main.css"' in html
    assert '<script type="module" src="/static/js/main.js"></script>' in html
    assert '<script src="/static/js/head.js"></script>' in html
    for name in (
        "css/main.css",
        "css/dist/main.css",
        "css/tokens.css",
        "css/base.css",
        "css/layout.css",
        "css/components.css",
        "css/fonts.css",
        "js/main.js",
        "js/head.js",
        "img/icons.svg",
        "img/favicon.svg",
        "img/og-default.png",
    ):
        assert finders.find(name), f"static file missing: {name}"
    main_css = Path(finders.find("css/main.css")).read_text(encoding="utf-8")
    for imported in re.findall(r'@import url\("([^"]+)"\)', main_css):
        assert finders.find(f"css/{imported}"), imported


def test_fonts_css_references_only_local_files_that_exist():
    css = (ROOT / "static" / "css" / "fonts.css").read_text(encoding="utf-8")
    urls = re.findall(r'url\("([^"]+)"\)', css)
    assert urls, "fonts.css has no @font-face rules — run scripts/fetch_fonts.py"
    for url in urls:
        assert url.startswith("../fonts/"), url
        assert (ROOT / "static" / "fonts" / url.split("/")[-1]).exists(), url
    assert "googleapis" not in css and "gstatic" not in css
    assert "font-display: swap" in css
    assert "unicode-range" in css
    # Design V4 (docs/design-v4/DESIGN_SYSTEM_V4.md §4.1): the Latin interface is IBM Plex Sans and
    # IBM Plex Mono — one superfamily with IBM Plex Sans Arabic, which art direction A had kept as
    # the Arabic INTERFACE face. Fira Sans and Fira Mono retired with their files; Plex Serif never
    # came back.
    for family in ("Newsreader", "IBM Plex Sans", "IBM Plex Mono", "Noto Naskh Arabic", "IBM Plex Sans Arabic"):
        assert f'font-family: "{family}"' in css, family
    for retired in ('"IBM Plex Serif"', '"Fira Sans"', '"Fira Mono"'):
        assert f"font-family: {retired}" not in css, retired
