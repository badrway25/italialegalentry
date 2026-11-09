"""
V5.29 §10–§13 — the FAQ as a product experience, lane PUB2 (FINAL_DELIVERY_V2 §3.6; built on stream SYS's icon primitive,
v5/_sezioni.css `.sez-tile--sm`; label v524-pub2-build): what the server renders and what the route sheet draws.

  * one semantic glyph per prescribed question (faq.views.GLYPHS), every one a registry symbol, never one twice and never
    two look-alikes of the registry's TWINS together (the list is one list);
  * the glyph in the library's small tile on every index row and every panel heading (the phone's question row), and
    before a search's answers;
  * a search with no answer: the empty state beside the whole register, each question one link to its permalink;
  * the sheet: the rows' ink by state, a visible focus, the open choreography never from the keyboard and never under
    reduced motion, the stage's heading without a tile beside the seal from 64 rem.
The browser half (the open state, RTL, reduced motion) is tests/frontend/test_pages_browser_v524_pub2.py.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from core import icons
from faq import registry
from faq.views import FRAUD_KEY, GLYPHS

ROOT = Path(__file__).resolve().parents[2]
SHEET = ROOT / "apps" / "cms" / "static" / "cms" / "_faq-v2.css"

pytestmark = pytest.mark.compliance


@pytest.fixture
def get(client, seeded, phase3_open, legal_published):
    def fetch(path: str) -> BeautifulSoup:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        html = response.content.decode("utf-8")
        return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")

    return fetch


def _symbol(svg) -> str:
    return svg.select_one("use")["href"].rsplit("#icon-", 1)[1]


def test_every_prescribed_question_has_its_own_glyph():
    assert set(GLYPHS) == set(registry.keys()), "one glyph per prescribed question, none for a key outside the register"
    symbols = list(GLYPHS.values())
    assert len(set(symbols)) == len(symbols), "never one icon twice"
    for symbol in symbols:
        assert icons.resolve(symbol) == symbol, symbol
    for twins in icons.TWINS:
        assert len(twins & set(symbols)) <= 1, twins
    assert GLYPHS[FRAUD_KEY] == "ile-scudo", "the fraud question keeps the protection's own mark"
    assert not {"shield", "shield-alert", "shield-check"} & set(symbols), "no second shield beside the fraud mark"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_index_rows_and_the_question_headings_carry_the_tile(get, lang):
    main = get(f"/{lang}/faq/")
    rows = main.select(".faq-esploratore .indice__voce")
    assert len(rows) == len(GLYPHS)
    seen = []
    for row in rows:
        tile = row.select_one(":scope > .indice__glifo.sez-tile.sez-tile--sm[aria-hidden='true']")
        assert tile is not None, row["href"]
        key = row["href"].lstrip("#")
        assert _symbol(tile.svg) == GLYPHS[key], key
        seen.append(key)
        heading = main.select_one(f"#{key}-title")
        head_tile = heading.select_one(":scope > .sez-tile.sez-tile--sm[aria-hidden='true']")
        assert head_tile is not None and _symbol(head_tile.svg) == GLYPHS[key], key
        assert heading.get_text(strip=True), "the heading's words stay its name (the tile is aria-hidden)"
    assert seen == registry.keys(), "the prescribed order, never a ranking"
    # the fraud question keeps its ink rule
    assert "indice__voce--marcata" in main.select_one(f'.indice__voce[href="#{FRAUD_KEY}"]')["class"]


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_search_without_answer_keeps_every_question_one_step_away(get, lang):
    main = get(f"/{lang}/faq/?q=zzzz-aucun")
    band = main.select_one('section.faq-risultati[data-ground="stone"]')
    assert band is not None
    empty = band.select_one(".faq-vuoto > .empty-state[role='status']")
    assert empty is not None
    nav = band.select_one(".faq-vuoto > nav.faq-vuoto__indice[aria-labelledby='faq-index-title']")
    assert nav is not None and nav.select_one("h3#faq-index-title.t-label") is not None
    links = nav.select("a.faq-vuoto__voce")
    assert [a["href"].split("#", 1)[1] for a in links] == registry.keys()
    for link in links:
        assert link["href"].startswith(f"/{lang}/faq/#")
        assert _symbol(link.select_one(".sez-tile.sez-tile--sm svg")) == GLYPHS[link["href"].split("#", 1)[1]]


@pytest.mark.django_db
def test_a_search_s_answers_carry_their_glyph(get):
    main = get("/fr/faq/?q=visa")
    items = main.select(".faq-risultati details.faq-item[open]")
    assert items
    for item in items:
        tile = item.select_one("summary > .faq-item__glifo.sez-tile.sez-tile--sm[aria-hidden='true']")
        assert tile is not None and _symbol(tile.svg) == GLYPHS[item["id"]]
    assert main.select_one(".faq-vuoto") is None


def _css() -> str:
    return re.sub(r"/\*.*?\*/", "", SHEET.read_text(encoding="utf-8"), flags=re.S)


def test_the_sheet_draws_the_states_and_never_animates_from_the_keyboard():
    css = _css()
    assert re.search(
        r"\.faq-esploratore \.indice__voce\[aria-selected=\"true\"\]\s*\{[^}]*color:\s*var\(--accent-text\)", css
    )
    assert re.search(
        r"\.faq-esploratore \.indice__voce:focus-visible\s*\{[^}]*outline:\s*var\(--focus-ring-width\) solid var\(--focus-ring\)",
        css,
    )
    assert re.search(r'html\[data-input="key"\] \.faq-esploratore \.indice__voce\s*\{\s*transition:\s*none;', css)
    # the answer's entrance only under no-preference, never from the keyboard or under the site's reduced-motion class
    block = css.split("@media (prefers-reduced-motion: no-preference)", 1)[1]
    assert re.match(
        r'\s*\{\s*:root:not\(\.rm\):not\(\[data-input="key"\]\) \.faq-esploratore[^{]*\{\s*animation:\s*faq-svela',
        block,
    )
    assert css.count("faq-svela") == 2, "one use, one keyframe"
    # the stage's heading draws no tile beside the seal from 64 rem
    assert re.search(
        r"@media \(min-width: 64rem\)\s*\{\s*\.faq-esploratore \.indice__titolo > \.sez-tile\s*\{\s*display:\s*none;",
        css,
    )
    # no literal weight, no literal colour
    assert not re.search(r"font-weight:\s*\d", css)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css)
