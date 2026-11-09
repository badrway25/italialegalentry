"""Compliance: « Vivre en Italie » pages render the locked texts verbatim and nothing forbidden."""

import re

import pytest
from django.conf import settings

from cms import locked_content
from cms.forbidden import scan
from living.catalogue import TOPIC_SLUGS
from tests.conftest import whatsapp_link_set_aside

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
    # V5.12 §8: a theme has a page only with a live, reviewed sheet — the sheet's own theme is the one rendered
    paths = ["vivre-en-italie/", f"vivre-en-italie/{sheet.topic.slug}/", sheet.get_absolute_url().split("/", 2)[2]]
    pages = []
    for lang in LANGS:
        for path in paths:
            r = client.get(f"/{lang}/{path}")
            assert r.status_code == 200, (lang, path)
            pages.append((lang, path, r.content.decode()))
        for slug in TOPIC_SLUGS:  # every other theme has no page at all
            if slug != sheet.topic.slug:
                assert client.get(f"/{lang}/vivre-en-italie/{slug}/").status_code == 404, (lang, slug)
    return pages


def test_locked_living_texts_rendered_verbatim(living_pages):
    for lang, path, html in living_pages:
        if path == "vivre-en-italie/" and lang == "ar":
            # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the title and the
            # body are compositional (C-UI) — their provisional Arabic renderings, never the French
            from cms import locked_renderings

            for key in ("p3.living.title", "p3.living.body"):
                assert locked_renderings.treatment(key) == "C-UI", key
                assert locked_renderings.rendering(key) in html, (lang, path, key)
                assert locked_content.text(key, "fr") not in html, (lang, path, key)
        elif path == "vivre-en-italie/":
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
        checked = whatsapp_link_set_aside(html)  # V5.19 §7: the owner's WhatsApp link only, as a link
        srcs = re.findall(r'(?:src|href)="(https?://[^"]+)"', checked)
        externals = [s for s in srcs if "testserver" not in s and "localhost" not in s]
        assert externals in ([], ["https://www.salute.gov.it/"]), (lang, path, externals)
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}, (lang, path, emails)


def test_gated_pages_404_before_phase3_in_every_language(client, own_seeds, before_phase3):
    for lang in LANGS:
        assert client.get(f"/{lang}/vivre-en-italie/").status_code == 404
        assert client.get(f"/{lang}/vivre-en-italie/logement/").status_code == 404
