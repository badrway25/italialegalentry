"""
V5.32 GLOBAL SITE + PLATFORM DESIGN COMPLETION (lane A, 12 Nov 2026) — the legal reader «il documento».

* a published legal text carries its own index: every h2 of the text has an anchor, the «Sommaire de la page» lists the
  same headings, verbatim and in order, each link reaching its heading; the index is the library's scroll-spy
  (data-sec-js="spia") inside one native disclosure;
* the text itself is unchanged by the index: the blocks rendered are the blocks of the body, the h2s only gain an id;
* a text still awaited keeps its notice and lists the legal texts already published — never itself, never an unpublished
  one (the footer's own rule, legal_links);
* the reader's sheet is the legal pages' own route sheet (legal/legale.css), linked after the content sheet, inside its
  measured ceiling (gzip -9 of the built dist).
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest

from legal import drafts
from legal.models import LegalDocument, LegalKind
from legal.services import invalidate, publish

ROOT = Path(__file__).resolve().parents[3]
LANGS = ("fr", "it", "en", "ar")
#: the legal reader's route sheet, at its measure (gzip -9 of static/css/dist/legal/legale.css: 1 272 B on 12 Nov 2026,
#: ceiling = measure + 3 %)
LEGALE_CSS_CEILING = 1_311


def _main(html: str) -> str:
    match = re.search(r"<main\b.*?</main>", html, flags=re.S)
    return match.group(0) if match else html


@pytest.fixture
def drafted(db):
    from legal.services import ensure_documents

    ensure_documents()
    drafts.load_drafts()
    invalidate()
    return {kind: LegalDocument.objects.get(kind=kind) for kind in (LegalKind.PRIVACY, LegalKind.COOKIES)}


@pytest.fixture
def open_fields_allowed(settings):
    # the privacy notice still holds open fields: a preview publishes it (production never does)
    settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED = True
    invalidate()
    yield
    invalidate()


@pytest.mark.parametrize("lang", LANGS)
def test_a_published_text_carries_its_own_index_of_its_headings(client, drafted, superuser, open_fields_allowed, lang):
    publish(drafted[LegalKind.PRIVACY], superuser)
    invalidate()
    main = _main(client.get(f"/{lang}/privacy-policy/").content.decode())
    headings = re.findall(r'<h2 id="(sezione-\d+)">(.*?)</h2>', main)
    nav = re.search(
        r'<nav class="legale__indice" aria-labelledby="legale-indice-title" data-sec-js="spia">(.*?)</nav>', main, re.S
    )
    assert nav is not None and len(headings) >= 5
    assert "<details" in nav.group(1) and 'id="legale-indice-title"' in nav.group(1)
    entries = re.findall(r'<a class="legale__voce" href="#(sezione-\d+)">(.*?)</a>', nav.group(1))
    assert entries == headings, "the index lists the text's own headings, verbatim, in order, each to its anchor"
    assert [anchor for anchor, _words in headings] == [f"sezione-{n}" for n in range(1, len(headings) + 1)]
    # the body has no h2 without its anchor: nothing in the text is left out of the index
    body = re.search(r'<div class="legal-page__body prose">(.*?)</div>', main, re.S).group(1)
    assert body.count("<h2") == len(headings)


def test_the_index_changes_nothing_in_the_text(client, drafted, superuser):
    from legal.rendering import blocks

    publish(drafted[LegalKind.COOKIES], superuser)
    invalidate()
    main = _main(client.get("/it/cookie-policy/").content.decode())
    rendered = re.sub(r'<h2 id="sezione-\d+">', "<h2>", main)
    for block in blocks(LegalDocument.objects.get(kind=LegalKind.COOKIES).body_it):
        if block["kind"] in ("h2", "h3", "p"):
            assert str(block["html"]) in rendered


@pytest.mark.parametrize("lang", LANGS)
def test_a_text_still_awaited_lists_only_the_published_texts(client, drafted, superuser, open_fields_allowed, lang):
    publish(drafted[LegalKind.PRIVACY], superuser)
    invalidate()
    main = _main(client.get(f"/{lang}/cookie-policy/").content.decode())
    assert 'data-gate="legal-blocked"' in main
    others = re.search(r'<nav class="legale-altri" aria-labelledby="legale-altri-title">(.*?)</nav>', main, re.S)
    assert others is not None
    hrefs = re.findall(r'<a class="legale-altri__link" href="([^"]+)"', others.group(1))
    # the published privacy notice only: never the page itself, never a gated one
    assert hrefs == [f"/{lang}/privacy-policy/"]


def test_with_nothing_published_the_awaited_page_lists_nothing(client, drafted):
    main = _main(client.get("/fr/cookie-policy/").content.decode())
    assert 'data-gate="legal-blocked"' in main and "legale-altri" not in main


def test_the_reader_links_its_own_route_sheet_after_the_content_sheet():
    source = (ROOT / "templates" / "legal" / "document.html").read_text(encoding="utf-8")
    content = source.index("{% static 'css/dist/cms/lettura.css' %}")
    assert source.index("{% static 'css/dist/legal/legale.css' %}") > content
    sheet = (ROOT / "apps" / "legal" / "static" / "legal" / "legale.css").read_text(encoding="utf-8")
    assert "@import" not in sheet, "a route sheet of its own rules: no shared partial carried twice"
    assert "legale" not in (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")


def test_the_reader_sheet_is_inside_its_ceiling():
    built = (ROOT / "static" / "css" / "dist" / "legal" / "legale.css").read_bytes()
    assert len(gzip.compress(built, 9)) <= LEGALE_CSS_CEILING, len(gzip.compress(built, 9))
