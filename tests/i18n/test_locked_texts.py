"""
Prescribed texts and legal pages are NEVER translated by the team: in Italian and in English they render in the
official French wording with ``lang="fr"`` (legal pages: official Italian with ``lang="it"``), and no catalogue can
translate them (gate G10, docs/LEGAL_AND_PUBLICATION_GATES.md).

V5.27 «ARABIC OWNER DECISION — FINAL» (5 Nov 2026; FINAL_DELIVERY_V2.md R7′; lane AR, under V5.20's strict rule — the old
expectation conflicts with the owner's decision, the new behaviour is implemented on purpose, the invariant is the same or
stronger): on /ar/ a COMPOSITIONAL prescribed text (C-UI) renders in a provisional professional Arabic kept beside the
registry (``cms.locked_renderings``), without a language attribute; a SUBSTANTIVE text (C-SUBST-FR) stands in French,
isolated, on its own page; an official name (C-OFFICIAL) stays as written. The French of the registry is untouched
(``tests/compliance/test_locked_content.py``) and no catalogue ever carries a prescribed text.
"""

from __future__ import annotations

import html as html_module
import re

import pytest
from django.template import Context, Template
from django.utils import translation
from django.utils.translation import gettext

from cms import locked_content, locked_renderings

from .conftest import LANGS, TRANSLATED, region

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]


def _locked(key: str) -> str:
    return html_module.escape(locked_content.text(key, "fr"))


def _element_with_text(page: str, text: str) -> str:
    """Opening tag of the element whose text starts with ``text`` (the element that carries ``lang``)."""
    match = re.search(r"<([a-z0-9]+)\b([^>]*)>\s*" + re.escape(text), page)
    assert match, f"locked text not rendered: {text[:60]}"
    return match.group(0)


@pytest.mark.parametrize("lang", ["it", "en"])
def test_locked_tag_renders_french_with_a_lang_attribute(lang):
    with translation.override(lang):
        inline = Template('{% locked "p1.companies.title" %}').render(Context())
        block = Template('{% locked "p1.companies.title" "h1" "page-header__title" %}').render(Context())
    assert inline == f'<span lang="fr">{_locked("p1.companies.title")}</span>'
    assert block == f'<h1 class="page-header__title" lang="fr">{_locked("p1.companies.title")}</h1>'


def test_locked_tag_renders_the_arabic_policy():
    """V5.27 / R7′: a compositional text in its provisional Arabic without a language attribute; a substantive text in
    French with ``lang="fr"`` (outside a request, as on its own page); the French source byte-identical in both cases."""
    with translation.override("ar"):
        inline = Template('{% locked "p1.companies.title" %}').render(Context())
        consent = Template('{% locked "p1.companies.form.consent" %}').render(Context())
    assert inline == locked_renderings.AR["p1.companies.title"]
    assert consent == f'<span lang="fr">{_locked("p1.companies.form.consent")}</span>'
    assert locked_content.text("p1.companies.title", "fr") == locked_content.LOCKED_TEXTS["fr"]["p1.companies.title"]


def test_locked_tag_needs_no_lang_attribute_in_french():
    with translation.override("fr"):
        assert Template('{% locked "p1.companies.title" %}').render(Context()) == _locked("p1.companies.title")


def test_registry_falls_back_to_french_without_an_official_version():
    """A language table may only hold officially transmitted texts; every other key falls back to French — in Arabic
    through the rendering policy (V5.27 / R7′): a compositional key answers its provisional rendering, every other key the
    French (outside a request, as on a block's own page)."""
    french = locked_content.LOCKED_TEXTS["fr"]
    for lang in TRANSLATED:
        table = locked_content.LOCKED_TEXTS.get(lang, {})
        assert set(table) <= set(french), lang
        for key in locked_content.keys():
            value, effective = locked_content.get(key, lang)
            if (
                lang == "ar"
                and key not in table
                and locked_renderings.resolve_value(key, french[key], "ar") is not None
            ):
                assert effective == "ar" and value != french[key], key
                continue
            assert effective == (lang if key in table else "fr"), (lang, key)
            if key not in table:
                assert value == french[key]


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_catalogue_translates_a_locked_text(audit, lang):
    with translation.override(lang):
        for key, _normalised in audit.locked_strings():
            root = key.split("[", 1)[0]
            value = locked_content.LOCKED_TEXTS["fr"].get(root)
            if isinstance(value, str) and len(value) >= 25:
                assert gettext(value) == value, (lang, key)


@pytest.mark.parametrize("lang", ["it", "en"])
def test_companies_page_keeps_the_prescribed_french_wording(client, seeded, lang):
    page = client.get(f"/{lang}/entreprises/").content.decode()
    main = region(page, "main")
    title = _element_with_text(main, _locked("p1.companies.title"))
    assert title.startswith("<h1") and 'lang="fr"' in title
    assert len(re.findall(r"<h1\b", page)) == 1


def test_arabic_companies_page_renders_the_title_and_keeps_the_consent_french(client, seeded, legal_published):
    """V5.27 / R7′: the prescribed title (compositional) in provisional Arabic as the page's h1, without a language
    attribute; the consent sentence (substantive) on its own page in French, isolated."""
    page = client.get("/ar/entreprises/").content.decode()
    main = region(page, "main")
    title = _element_with_text(main, html_module.escape(locked_renderings.AR["p1.companies.title"]))
    assert title.startswith("<h1") and 'lang="fr"' not in title
    assert _locked("p1.companies.title") not in main
    consent = _element_with_text(main, _locked("p1.companies.form.consent"))
    assert 'lang="fr"' in consent
    assert len(re.findall(r"<h1\b", page)) == 1


def test_companies_page_in_french_carries_no_fallback_marker(client, seeded):
    main = region(client.get("/fr/entreprises/").content.decode(), "main")
    assert 'lang="fr"' not in _element_with_text(main, _locked("p1.companies.title"))


@pytest.mark.parametrize("lang", ["it", "en"])
def test_forum_page_keeps_the_prescribed_french_wording(client, seeded, lang):
    main = region(client.get(f"/{lang}/forum/").content.decode(), "main")
    # The breadcrumb repeats the event name (a proper noun); the prescribed header is what is checked here.
    main = re.sub(r'<nav class="breadcrumbs.*?</nav>', "", main, flags=re.S)
    for key in ("p2.forum.header.title", "p2.forum.header.subtitle", "p2.forum.header.meta"):
        assert 'lang="fr"' in _element_with_text(main, _locked(key)), (lang, key)


def test_arabic_forum_page_keeps_the_official_title_and_renders_the_subtitle(client, seeded):
    """V5.27 / R7′: the Forum's name (official, C-OFFICIAL) stays in French, isolated; its subtitle and its meta line
    (compositional) read in provisional Arabic."""
    main = region(client.get("/ar/forum/").content.decode(), "main")
    main = re.sub(r'<nav class="breadcrumbs.*?</nav>', "", main, flags=re.S)
    assert 'lang="fr"' in _element_with_text(main, _locked("p2.forum.header.title"))
    for key in ("p2.forum.header.subtitle", "p2.forum.header.meta"):
        assert _locked(key) not in main, key
        assert html_module.escape(locked_renderings.AR[key]) in main, key


@pytest.mark.parametrize("lang", ["it", "en"])
def test_phase3_hero_keeps_the_prescribed_french_wording(client, seeded, phase3_open, lang):
    page = client.get(f"/{lang}/").content.decode()
    assert 'lang="fr"' in _element_with_text(page, _locked("p3.hero.subtitle")), lang


def test_arabic_hero_renders_the_prescribed_subtitle(client, seeded, phase3_open):
    """V5.27 / R7′: the home's first screen reads Arabic — the hero's promise is a compositional text."""
    page = client.get("/ar/").content.decode()
    assert _locked("p3.hero.subtitle") not in page
    element = _element_with_text(page, html_module.escape(locked_renderings.AR["p3.hero.subtitle"]))
    assert 'lang="fr"' not in element


@pytest.mark.parametrize("lang", LANGS)
def test_official_legal_text_is_italian_in_every_language(client, seeded, legal_published, lang):
    page = client.get(f"/{lang}/privacy-policy/").content.decode()
    main = region(page, "main")
    assert re.search(r'<article class="container legal-page" lang="it">', main)
    assert "TESTO UFFICIALE DI PROVA" in main  # the official Italian body, verbatim, whatever the page language
    # The status line is interface text: it follows the page language.
    assert f'<p class="legal-page__meta" lang="{lang}">' in main
