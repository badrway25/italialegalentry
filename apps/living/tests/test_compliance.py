"""Compliance: « Vivre en Italie » pages render the locked texts verbatim and nothing forbidden."""

import re

import pytest
from django.conf import settings

from cms import locked_content
from cms.forbidden import scan
from living.catalogue import TOPIC_SLUGS

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

LANGS = [code for code, _ in settings.LANGUAGES]


@pytest.fixture
def own_seeds(db):
    from django.core.management import call_command

    for prefix in ("accounts.", "legal.", "consents.", "living."):
        call_command("seed_all", only=prefix, verbosity=0)


@pytest.fixture
def living_pages(client, own_seeds, phase3_open, sheet_factory):
    sheet = sheet_factory(
        "Fiche de conformité",
        slug="conformite",
        sources=[{"label": "Source officielle", "url": "https://www.salute.gov.it/"}],
    )
    paths = ["vivre-en-italie/"] + [f"vivre-en-italie/{slug}/" for slug in TOPIC_SLUGS]
    paths.append(sheet.get_absolute_url().split("/", 2)[2])
    pages = []
    for lang in LANGS:
        for path in paths:
            r = client.get(f"/{lang}/{path}")
            assert r.status_code == 200, (lang, path)
            pages.append((lang, path, r.content.decode()))
    return pages


def test_locked_living_texts_rendered_verbatim(living_pages):
    for lang, path, html in living_pages:
        if path == "vivre-en-italie/":
            assert locked_content.text("p3.living.title", "fr") in html, (lang, path)
            assert locked_content.text("p3.living.body", "fr") in html, (lang, path)
            if lang != "fr":
                assert 'lang="fr"' in html


def test_no_forbidden_formulations_or_markers(living_pages):
    for lang, path, html in living_pages:
        assert not scan(html), (lang, path, scan(html))
        assert "®" not in html and "Italy Legal Entry™" in html
        for marker in ("CONTENT_PENDING_LEGAL_REVIEW", "lorem ipsum", "TODO"):
            assert marker not in html, (lang, path, marker)


def test_no_external_resources(living_pages):
    for lang, path, html in living_pages:
        srcs = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
        externals = [s for s in srcs if "testserver" not in s and "localhost" not in s]
        assert externals in ([], ["https://www.salute.gov.it/"]), (lang, path, externals)
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}, (lang, path, emails)


def test_gated_pages_404_before_phase3_in_every_language(client, own_seeds, before_phase3):
    for lang in LANGS:
        assert client.get(f"/{lang}/vivre-en-italie/").status_code == 404
        assert client.get(f"/{lang}/vivre-en-italie/logement/").status_code == 404
