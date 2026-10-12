"""
Public-page compliance: forbidden formulations, legal routes, trademark, e-mail domain, headers.

Routes come from ``core.public_routes`` (each app registers its public paths in AppConfig.ready).
"""

import re

import pytest
from django.conf import settings

from cms.forbidden import scan

pytestmark = pytest.mark.compliance

LANGS = [code for code, _ in settings.LANGUAGES]


def _iter_pages(client):
    from core.public_routes import ungated_paths

    for lang in LANGS:
        for path in ungated_paths():
            response = client.get(f"/{lang}/{path}")
            assert response.status_code == 200, (lang, path, response.status_code)
            yield lang, path, response.content.decode("utf-8")


@pytest.mark.django_db
def test_no_forbidden_formulations_on_public_pages(client, seeded):
    for lang, path, html in _iter_pages(client):
        violations = scan(html)
        assert not violations, f"/{lang}/{path}: {violations}"


@pytest.mark.django_db
def test_trademark_uses_tm_never_registered(client, seeded):
    for lang, path, html in _iter_pages(client):
        assert "®" not in html, (lang, path)
        assert "Italy Legal Entry™" in html, (lang, path)


@pytest.mark.django_db
def test_public_email_is_only_agami_address(client, seeded):
    for lang, path, html in _iter_pages(client):
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}, (lang, path, emails)


@pytest.mark.django_db
def test_five_legal_routes_are_distinct_pages(client, seeded):
    paths = ["privacy-policy/", "cookie-policy/", "note-legali/", "condizioni-di-utilizzo/", "avvertenze/"]
    bodies = []
    for path in paths:
        r = client.get(f"/fr/{path}")
        assert r.status_code == 200
        bodies.append(r.content)
    assert len({hash(b) for b in bodies}) == 5, "legal pages must not be aliases of one page"
    home = client.get("/fr/").content.decode()
    for path in paths:
        assert f'href="/fr/{path}"' in home
    assert 'href="#apropos"' not in home


@pytest.mark.django_db
def test_legal_pages_blocked_until_official_text(client, seeded):
    r = client.get("/fr/privacy-policy/")
    html = r.content.decode()
    assert 'data-gate="legal-blocked"' in html
    assert 'name="robots" content="noindex' in html


@pytest.mark.django_db
def test_no_external_scripts_fonts_or_images(client, seeded):
    for lang, path, html in _iter_pages(client):
        srcs = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
        externals = [s for s in srcs if "testserver" not in s and "localhost" not in s]
        # mailto/hreflang absolute URLs point to testserver; anything else is forbidden.
        assert not externals, (lang, path, externals)


@pytest.mark.django_db
def test_security_headers_present(client, seeded):
    r = client.get("/fr/")
    assert r["X-Frame-Options"] == "DENY"
    assert r["X-Content-Type-Options"] == "nosniff"
    assert "Referrer-Policy" in r
    assert "Permissions-Policy" in r
    csp = r["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "X-Request-ID" in r


@pytest.mark.django_db
def test_arabic_is_rtl_and_others_ltr(client, seeded):
    assert '<html lang="ar" dir="rtl"' in client.get("/ar/").content.decode()
    for lang in ("it", "fr", "en"):
        assert f'<html lang="{lang}" dir="ltr"' in client.get(f"/{lang}/").content.decode()


@pytest.mark.django_db
def test_hreflang_alternates_present(client, seeded):
    html = client.get("/fr/").content.decode()
    for lang in LANGS:
        assert f'hreflang="{lang}"' in html
    assert 'hreflang="x-default"' in html
    assert '<link rel="canonical"' in html
