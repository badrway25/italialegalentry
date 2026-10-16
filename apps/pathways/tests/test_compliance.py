"""
Compliance for the Espace Personnes: forbidden formulations, no invented legal claims, no visible
internal markers, self-only resources, single public e-mail — in every language, gate closed and open.
"""

import re
from pathlib import Path

import pytest
from django.conf import settings

from cms.forbidden import scan
from core.public_routes import all_routes
from pathways.models import PATHWAY_KEYS

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

LANGS = [code for code, _ in settings.LANGUAGES]
ROOT = Path(__file__).resolve().parents[3]
OWNED_TEMPLATES = ROOT / "templates" / "pathways"
OWNED_PY = ROOT / "apps" / "pathways"

RECOGNITION_TOKENS = (
    "reconnaît",
    "reconnaissons",
    "riconosce",
    "riconosciamo",
    "recognises",
    "recognizes",
    "omologa",
    "equivalenze",
)
PROMISE_TOKENS = (
    "visa garanti",
    "visto garantito",
    "guaranteed",
    "entrée assurée",
    "canal actif",
    "corridoio operativo",
    "ingressi garantiti",
)
APPROVAL_TOKENS = ("approbation ministérielle", "approvazione ministeriale", "attestation ministérielle")
INTERNAL_MARKERS = ("CONTENT_PENDING_LEGAL_REVIEW", "lorem ipsum", "TODO", "[ ]", "PENDING_CLIENT")


def _pages(gate_open: bool) -> list[str]:
    pages = ["parcours/"]
    if gate_open:
        pages += [f"parcours/{key}/" for key in PATHWAY_KEYS] + ["diplomes-et-titres/", "formation/"]
    return pages


def _iter_html(client, gate_open: bool):
    for lang in LANGS:
        for path in _pages(gate_open):
            r = client.get(f"/{lang}/{path}")
            assert r.status_code == 200, (lang, path, r.status_code)
            yield lang, path, r.content.decode("utf-8")


class TestRenderedPagesClosed:
    def test_no_forbidden_formulations(self, client, pathways_seeded, before_phase3):
        for lang, path, html in _iter_html(client, False):
            assert not scan(html), (lang, path, scan(html))

    def test_no_internal_markers_visible(self, client, pathways_seeded, before_phase3, visible_text_fn):
        for lang, path, html in _iter_html(client, False):
            text = visible_text_fn(html)
            for marker in INTERNAL_MARKERS:
                assert marker not in text, (lang, path, marker)


class TestRenderedPagesOpen:
    def test_no_forbidden_formulations(self, client, pathways_seeded, phase3_open):
        for lang, path, html in _iter_html(client, True):
            assert not scan(html), (lang, path, scan(html))

    def test_trademark_tm_and_no_registered(self, client, pathways_seeded, phase3_open):
        for lang, path, html in _iter_html(client, True):
            assert "Italy Legal Entry™" in html, (lang, path)
            assert "®" not in html and "&reg;" not in html and "&#174;" not in html, (lang, path)

    def test_only_public_email(self, client, pathways_seeded, phase3_open):
        for lang, path, html in _iter_html(client, True):
            emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
            assert emails <= {"contact@agamieuromed.org"}, (lang, path, emails)

    def test_no_external_resources(self, client, pathways_seeded, phase3_open):
        for lang, path, html in _iter_html(client, True):
            urls = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
            externals = [u for u in urls if "testserver" not in u and "localhost" not in u]
            assert not externals, (lang, path, externals)

    def test_no_internal_markers_visible(self, client, pathways_seeded, phase3_open, visible_text_fn):
        for lang, path, html in _iter_html(client, True):
            text = visible_text_fn(html)
            for marker in INTERNAL_MARKERS:
                assert marker not in text, (lang, path, marker)

    def test_no_recognition_promise_or_approval_claims_outside_locked_texts(
        self, client, pathways_seeded, phase3_open, strip_locked_fn, visible_text_fn
    ):
        for lang, path, html in _iter_html(client, True):
            remaining = visible_text_fn(strip_locked_fn(html)).lower()
            for token in RECOGNITION_TOKENS + PROMISE_TOKENS + APPROVAL_TOKENS:
                assert token not in remaining, (lang, path, token)

    def test_locked_texts_rendered_where_placed(self, client, pathways_seeded, phase3_open):
        from django.utils.html import escape

        from cms import locked_content

        placements = {
            "parcours/": (
                "p3.persons.title",
                "p3.persons.intro",
                "p3.persons.how_it_works",
                "p3.antifraud.title",
                "p3.antifraud.body",
            ),
            "parcours/salaried_work/": ("p3.antifraud.title", "p3.antifraud.body"),
            "diplomes-et-titres/": ("p3.diplomas.title", "p3.diplomas.body", "p3.antifraud.title"),
            "formation/": ("p3.training_after.title", "p3.training_after.body", "p3.antifraud.title"),
        }
        #: a locked text the page cuts on its own separators for layout (CREATIVE_DIRECTION_V5 law 8): it is read whole
        #: in its element's text, never retyped
        cut = {"p3.persons.how_it_works"}
        for path, keys in placements.items():
            html = client.get(f"/fr/{path}").content.decode()
            for key in keys:
                if key in cut:
                    from bs4 import BeautifulSoup

                    block = BeautifulSoup(html, "html.parser").select_one(f'[data-locked="{key}"]')
                    text = " ".join(block.get_text(" ").split()) if block else ""
                    assert text == locked_content.text(key, "fr"), (path, key)
                    continue
                assert escape(locked_content.text(key, "fr")) in html, (path, key)

    def test_fallback_language_marked_for_non_french(self, client, pathways_seeded, phase3_open):
        html = client.get("/it/parcours/").content.decode()
        assert 'lang="fr"' in html
        html = client.get("/ar/parcours/salaried_work/").content.decode()
        assert 'lang="fr"' in html


class TestSources:
    """Team-written sources never contain prescribed texts copied by hand nor forbidden claims."""

    def _owned_files(self):
        files = list(OWNED_TEMPLATES.rglob("*.html"))
        files += [p for p in OWNED_PY.rglob("*.py") if "tests" not in p.parts and "migrations" not in p.parts]
        return files

    def test_no_hand_copied_locked_text_in_templates_or_code(self):
        from cms import locked_content

        sentences = []
        for key, value in locked_content.LOCKED_TEXTS["fr"].items():
            if key.startswith("legal."):
                continue
            if isinstance(value, str) and len(value) > 40:
                sentences.append((key, value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for v in item.values():
                            if isinstance(v, str) and len(v) > 40:
                                sentences.append((key, v))
        for path in self._owned_files():
            source = path.read_text(encoding="utf-8")
            for key, sentence in sentences:
                assert sentence not in source, f"{path.name} hand-copies locked text {key}"

    def test_no_recognition_or_promise_wording_in_sources(self):
        for path in self._owned_files():
            source = path.read_text(encoding="utf-8").lower()
            for token in RECOGNITION_TOKENS + PROMISE_TOKENS + APPROVAL_TOKENS:
                assert token not in source, (path.name, token)

    def test_no_forbidden_phrases_in_sources(self):
        for path in self._owned_files():
            source = path.read_text(encoding="utf-8")
            violations = [v for v in scan(source) if v.label != "MATCHING" or "matching" in source.lower()]
            assert not violations, (path.name, violations)

    def test_no_external_urls_in_templates(self):
        for path in OWNED_TEMPLATES.rglob("*.html"):
            source = path.read_text(encoding="utf-8")
            assert not re.search(r"https?://", source), path.name

    def test_ui_strings_are_translated(self):
        """Every template renders UI copy through translate/blocktranslate or locked tags (spot check)."""
        for path in OWNED_TEMPLATES.rglob("*.html"):
            source = path.read_text(encoding="utf-8")
            assert "{% load i18n" in source, path.name


class TestRouteRegistry:
    def test_routes_registered_with_gates(self):
        routes = {(r.path, r.requires_gate) for r in all_routes() if r.app == "pathways"}
        assert ("parcours/", "") in routes
        for key in PATHWAY_KEYS:
            assert (f"parcours/{key}/", "phase3_public") in routes
        assert ("diplomes-et-titres/", "phase3_public") in routes
        assert ("formation/", "phase3_public") in routes
