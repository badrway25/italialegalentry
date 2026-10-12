"""
Prescribed texts and legal pages are NEVER translated by the team: in every language they render in the
official French wording with ``lang="fr"`` (legal pages: official Italian with ``lang="it"``), and no
catalogue can translate them (gate G10, docs/LEGAL_AND_PUBLICATION_GATES.md).
"""

from __future__ import annotations

import html as html_module
import re

import pytest
from django.template import Context, Template
from django.utils import translation
from django.utils.translation import gettext

from cms import locked_content

from .conftest import LANGS, TRANSLATED, region

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]


def _locked(key: str) -> str:
    return html_module.escape(locked_content.text(key, "fr"))


def _element_with_text(page: str, text: str) -> str:
    """Opening tag of the element whose text starts with ``text`` (the element that carries ``lang``)."""
    match = re.search(r"<([a-z0-9]+)\b([^>]*)>\s*" + re.escape(text), page)
    assert match, f"locked text not rendered: {text[:60]}"
    return match.group(0)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_locked_tag_renders_french_with_a_lang_attribute(lang):
    with translation.override(lang):
        inline = Template('{% locked "p1.companies.title" %}').render(Context())
        block = Template('{% locked "p1.companies.title" "h1" "page-header__title" %}').render(Context())
    assert inline == f'<span lang="fr">{_locked("p1.companies.title")}</span>'
    assert block == f'<h1 class="page-header__title" lang="fr">{_locked("p1.companies.title")}</h1>'


def test_locked_tag_needs_no_lang_attribute_in_french():
    with translation.override("fr"):
        assert Template('{% locked "p1.companies.title" %}').render(Context()) == _locked("p1.companies.title")


def test_registry_falls_back_to_french_without_an_official_version():
    """A language table may only hold officially transmitted texts; every other key falls back to French."""
    french = locked_content.LOCKED_TEXTS["fr"]
    for lang in TRANSLATED:
        table = locked_content.LOCKED_TEXTS.get(lang, {})
        assert set(table) <= set(french), lang
        for key in locked_content.keys():
            value, effective = locked_content.get(key, lang)
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


@pytest.mark.parametrize("lang", TRANSLATED)
def test_companies_page_keeps_the_prescribed_french_wording(client, seeded, lang):
    page = client.get(f"/{lang}/entreprises/").content.decode()
    main = region(page, "main")
    title = _element_with_text(main, _locked("p1.companies.title"))
    assert title.startswith("<h1") and 'lang="fr"' in title
    assert len(re.findall(r"<h1\b", page)) == 1


def test_companies_page_in_french_carries_no_fallback_marker(client, seeded):
    main = region(client.get("/fr/entreprises/").content.decode(), "main")
    assert 'lang="fr"' not in _element_with_text(main, _locked("p1.companies.title"))


@pytest.mark.parametrize("lang", TRANSLATED)
def test_forum_page_keeps_the_prescribed_french_wording(client, seeded, lang):
    main = region(client.get(f"/{lang}/forum/").content.decode(), "main")
    # The breadcrumb repeats the event name (a proper noun); the prescribed header is what is checked here.
    main = re.sub(r'<nav class="breadcrumbs.*?</nav>', "", main, flags=re.S)
    for key in ("p2.forum.header.title", "p2.forum.header.subtitle", "p2.forum.header.meta"):
        assert 'lang="fr"' in _element_with_text(main, _locked(key)), (lang, key)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_phase3_hero_keeps_the_prescribed_french_wording(client, seeded, phase3_open, lang):
    page = client.get(f"/{lang}/").content.decode()
    assert 'lang="fr"' in _element_with_text(page, _locked("p3.hero.subtitle")), lang


@pytest.mark.parametrize("lang", LANGS)
def test_official_legal_text_is_italian_in_every_language(client, seeded, legal_published, lang):
    page = client.get(f"/{lang}/privacy-policy/").content.decode()
    main = region(page, "main")
    assert re.search(r'<article class="container legal-page" lang="it">', main)
    assert "TESTO UFFICIALE DI PROVA" in main  # the official Italian body, verbatim, whatever the page language
    # The status line is interface text: it follows the page language.
    assert f'<p class="legal-page__meta" lang="{lang}">' in main
