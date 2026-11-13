"""
V5.29 §10–§13 — the FAQ as a product experience, lane PUB2 (FINAL_DELIVERY_V2 §3.6; label v524-pub2-build), restated under
the V5.20 strict rule for the FINAL MICRO-PASS §6 B1 (9 Nov 2026; the owner's representative test: «if the FAQ still looks
like geometric cards with repeated icons, the pass has failed»): what the server renders and what the route sheet draws.

  * no question carries a glyph any more (V5.29's faq.views.GLYPHS left): the list draws ONE mark — the fraud question's
    protection, bare, at the question's size (BRIEF §2.1) — and no tile anywhere;
  * the questions are one list of the system's disclosures, in the prescribed order, each its permalink's row; a theme
    is a presentation group of prescribed keys (faq.views.THEMES), every key in exactly one, named by catalogue strings;
  * a search with no answer: the empty state beside the whole register, each question one link to its permalink — words
    only; a search's answers are the open rows, without a glyph;
  * the sheet: the pills' and the rows' states, a visible focus, the answer's entrance never from the keyboard and never
    under reduced motion, the mark that turns; tokens only.
The browser half (the opening, the filter, RTL) is tests/frontend/test_pages_browser_v524_pub2.py and
tests/frontend/test_browser_w1_c.py.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.utils import translation

from faq import registry, views
from faq.views import FRAUD_KEY, THEMES

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


def test_no_question_carries_a_glyph_and_every_prescribed_question_has_one_theme():
    """FINAL MICRO-PASS §6 B1 (V5.20; replaces «every prescribed question has its own glyph»): the per-question glyph map
    is gone; the themes group the register's keys, each key once, every theme named by a translated catalogue string."""
    assert not hasattr(views, "GLYPHS") and not hasattr(views, "glyph")
    keys = [key for _name, _label, members in THEMES for key in members]
    assert sorted(keys) == sorted(registry.keys()) and len(set(keys)) == len(keys), "each prescribed key in one theme"
    assert FRAUD_KEY in keys
    for _name, label, _members in THEMES:
        with translation.override("fr"):
            french = str(label)
        for lang in ("it", "en", "ar"):
            with translation.override(lang):
                assert str(label) and str(label) != french, (lang, french)


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_questions_are_one_list_in_order_and_only_the_fraud_question_keeps_its_mark(get, lang):
    """FINAL MICRO-PASS §6 B1 (V5.20; replaces «the index rows and the question headings carry the tile»): the rows in the
    prescribed order, each heading its words; no tile in the list; the fraud row its ONE mark, bare, inside its heading."""
    main = get(f"/{lang}/faq/")
    rows = main.select(".faq-lista > details.faq-item")
    assert [row["id"] for row in rows] == registry.keys(), "the prescribed order, never a ranking"
    assert not main.select(".faq-lista .sez-tile, .faq-lista .sigillo, .faq-item__glifo, .faq-esploratore")
    for row in rows:
        heading = row.select_one(":scope > summary > h3.faq-item__question")
        assert heading.get_text(strip=True), "the heading's words stay its name"
        marks = row.select("summary svg")
        if row["id"] == FRAUD_KEY:
            assert "faq-item--marcata" in row["class"]
            assert len(marks) == 1 and _symbol(marks[0]) == "ile-scudo" and marks[0].get("aria-hidden") == "true"
            assert marks[0].parent is heading and "faq-item__segno" in marks[0]["class"], "bare, at the question's size"
        else:
            assert marks == [], row["id"]
    assert len(main.select(".faq-lista svg")) == 1, "one mark in the whole list"


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
        # FINAL MICRO-PASS §6 B1 (V5.20): words only — the link carries no tile and no glyph (it carried its question's)
        assert link.get_text(strip=True) and not link.select("svg, .sez-tile"), link["href"]


@pytest.mark.django_db
def test_a_search_s_answers_are_the_open_rows_without_a_glyph(get):
    """FINAL MICRO-PASS §6 B1 (V5.20; replaces «a search's answers carry their glyph»): the answers are the list's own rows,
    open, no tile before the question; the fraud answer keeps its one mark."""
    main = get("/fr/faq/?q=visa")
    items = main.select(".faq-risultati .faq-lista > details.faq-item[open]")
    assert items and FRAUD_KEY in [item["id"] for item in items]
    for item in items:
        assert item.select_one("summary > h3.faq-item__question") is not None
        assert not item.select(".sez-tile, .faq-item__glifo")
        assert len(item.select("summary svg")) == (1 if item["id"] == FRAUD_KEY else 0), item["id"]
    assert main.select_one(".faq-vuoto") is None


def _css() -> str:
    return re.sub(r"/\*.*?\*/", "", SHEET.read_text(encoding="utf-8"), flags=re.S)


def test_the_sheet_draws_the_states_and_never_animates_from_the_keyboard():
    css = _css()
    # FINAL MICRO-PASS §6 B1 (V5.20): the chosen theme filled with the ink (it was the index row in the accent), a visible
    # focus on the pills and the rows, no transition from the keyboard, the mark that turns once open
    assert re.search(r'\.faq-tema\[aria-pressed="true"\]\s*\{[^}]*background-color:\s*var\(--text-1\)', css)
    assert re.search(
        r":is\(\.faq-tema, \.faq-item > \.accordion__summary\):focus-visible\s*\{[^}]*outline:\s*var\(--focus-ring-width\) solid var\(--focus-ring\)",
        css,
    )
    assert re.search(r'html\[data-input="key"\] :is\(\.faq-tema, \.faq-item > \.accordion__summary,[^)]*\)\s*\{\s*transition:\s*none;', css)
    assert re.search(r"\.faq-item\[open\] > \.accordion__summary::after\s*\{[^}]*rotate:\s*180deg", css)
    # the answer's entrance only under no-preference, never from the keyboard or under the site's reduced-motion class
    block = css.split("@media (prefers-reduced-motion: no-preference)", 1)[1]
    assert re.match(
        r'\s*\{\s*:root:not\(\.rm\):not\(\[data-input="key"\]\) \.faq-domande \.faq-item\[open\] > \.faq-item__answer\s*\{\s*animation:\s*faq-svela',
        block,
    )
    assert css.count("faq-svela") == 2, "one use, one keyframe"
    # the explorer's compositions left with it, and no plate opens under an answer
    assert not re.search(r"faq-esploratore|\.indice|sez-tile|sigillo", css)
    assert re.search(
        r"\.lettura \.faq-lista \.accordion__item,\s*\.lettura \.faq-lista \.accordion__item\[open\]\s*\{[^}]*"
        r"background-color:\s*transparent",
        css,
    ), "no plate under a row, open or closed (v5/tabs.css paints an open row at (0,3,1))"
    # the question at the body's size and weight (BRIEF §6 B1: 400–450, 17–19 px)
    assert re.search(r"\.faq-item > \.accordion__summary\s*\{[^}]*font-size:\s*var\(--t-body\);[^}]*font-weight:\s*var\(--w-body\)", css)
    # no literal weight, no literal colour
    assert not re.search(r"font-weight:\s*\d", css)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css)
