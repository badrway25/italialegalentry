"""
The public interior of design V5.4 — W3-F1, step 1: the doors and the project pages (plan §3.5 item 1; §1.18 D26;
§1.4 RH-5; §1.7 the six-icon ceiling; §1.16; §2.3).

What the grammar promises on every page it draws, read in the rendered HTML: one entrance and one h1; on a door, the
door card for its own audience, carrying the door's way in (the fix pass, M1: the page's one action, or on the
companies' page the way to its form, in the first screen); one primary action at most; at most six icons in the
editorial body (the section device's identity mark apart); a curated plate never without its caption and a stock frame
never with one (V5.24 §2); the live «who can help
me» line where the page offers an action; no block waiting for a scroll; the page sheets written as plain import lists
in the collected tree; an authority's host beside its link; a locked sentence cut for layout reads back whole (law 8);
French on an Arabic page says so.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.conf import settings

from core import icons

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
PAGE = ROOT / "static" / "css" / "v5" / "_pagina.css"
DOORS = {
    "/fr/parcours/": "person",
    "/fr/entreprises/": "company",
    "/fr/institutions/": "institution",
    "/fr/universites-et-formation/": "university",
}
INTERIOR = [
    *DOORS,
    "/fr/projet-pilote/",
    "/fr/forum/",
    "/fr/forum/inscription/",
    "/fr/le-projet/",
    "/fr/agami/",
    "/fr/reseau/",
    "/fr/contact/",
    "/fr/attention-aux-fraudes/",
]
#: pages whose body offers an action, and so says who can help (D26: «who can help me», live text only)
WITH_HELP = ["/fr/parcours/", "/fr/institutions/", "/fr/universites-et-formation/", "/fr/projet-pilote/", "/fr/forum/"]
ICON = re.compile(r'<use href="[^"#]*#icon-([a-z0-9-]+)"')


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


@pytest.fixture
def interior(client, seeded, phase3_open, legal_published):
    def get(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return get


@pytest.mark.parametrize("path", INTERIOR)
def test_one_entrance_one_h1_and_no_side_column(interior, path):
    main = _main(interior(path))
    assert main.count('<header class="ingresso') == 1, path
    assert main.count("<h1") == 1, path
    assert '<nav class="local-nav"' not in main and "layout-sidebar" not in main, path


#: each door's way in: the control's destination, and whether it is the page's one primary (the companies' card leads
#: to the form further down, whose submit stays the one action)
WAYS = {
    "/fr/parcours/": ("/fr/orientation/", True),
    "/fr/entreprises/": ("#formulaire", False),
    "/fr/institutions/": ("/fr/collaboration/institutions/", True),
    "/fr/universites-et-formation/": ("/fr/collaboration/universites-formation/", True),
}


SLOTS = {
    "/fr/parcours/": "pathways.hero",
    "/fr/entreprises/": "companies.hero",
    "/fr/institutions/": "institutions.hero",
    "/fr/universites-et-formation/": "universities.hero",
}


@pytest.mark.parametrize(("path", "audience"), DOORS.items())
def test_a_door_s_entrance_carries_its_photograph_and_its_way_in(interior, path, audience):
    """
    V5.12 (DECISIONS §6/§7, W2-C) supersedes the night door card of W3-F1's fix pass on the four landings: the end
    seat holds the space's photograph (the page's one LCP image, from the slot registry), and the door's way in — its
    sentence and its one control — stands under the lead, on the paper (.ingresso__way, the design _porta.css keeps for
    a photographed entrance). What W3-F1's review M1 asked still holds: the way is in the first screen, it says what it
    gives, and the page's one primary is its control (the companies' way leads to the form, a secondary).
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(_main(interior(path)), "html.parser")
    entrance = soup.select_one("header.ingresso")
    assert entrance["data-audience"] == audience
    photo = entrance.select_one("figure.ingresso__aside.ingresso__photo")
    assert photo["data-slot"] == SLOTS[path]
    img = photo.select_one("img")
    assert img["alt"] and img["fetchpriority"] == "high" and img.get("width") and img.get("height")
    # V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6; V5.20): the stock frame carries no caption and no stock label
    assert photo.select_one("figcaption") is None and "Pexels" not in str(photo)
    assert not entrance.select(".porta"), "one way in: under the lead, not a second card"
    way = entrance.select_one(".ingresso__text > .ingresso__way.via")
    assert way.select_one(".via__text").get_text(strip=True), "the way says what it gives"
    url, primary = WAYS[path]
    control = way.select_one(".via__action a.btn")
    assert control["href"] == url
    assert ("btn--primary" in control["class"]) is primary
    primaries = soup.select(".btn--primary")
    if primary:
        assert primaries == [control], "the page's one action is the way's"
    else:
        assert "btn--secondary" in control["class"] and not way.select(".btn--primary")


def test_the_person_door_s_way_is_the_questionnaire_s_action(interior):
    from bs4 import BeautifulSoup

    way = BeautifulSoup(_main(interior("/fr/parcours/")), "html.parser").select_one(".ingresso__way")
    assert (
        way.select_one("h2.via__title#orientation-title").get_text(strip=True)
        == "Identifiez la voie régulière à explorer"
    )
    assert way.select_one(".via__action a").get_text(" ", strip=True) == "Commencer le questionnaire d’orientation"


def test_how_it_works_stands_on_the_line_and_reads_back_whole(interior):
    """
    The fix pass (W3-F1's review M2; CREATIVE_DIRECTION_V5 law 8, D-U4): the locked «Comment ça marche» sentence is cut
    on its own arrows into four stations of «la linea», its caveat under them; joined back — the hidden opening words
    and arrows included — it is the registry's sentence, character for character.
    """
    from bs4 import BeautifulSoup

    from cms import locked_content

    text = locked_content.text("p3.persons.how_it_works", "fr")
    soup = BeautifulSoup(_main(interior("/fr/parcours/")), "html.parser")
    block = soup.select_one('[data-locked="p3.persons.how_it_works"]')
    assert " ".join(block.get_text(" ").split()) == text
    # V5.22 (SECTION_SYSTEM_V2 §3.4 PA-2 — an approved owner/product decision; lane P1; V5.20 strict rule): the four
    # stations are four plates on the brand ground (lane S's «il tracciato» band), each its registry glyph
    # (icons.HOW_STEP) — the same cut on the sentence's own arrows, the arrows kept as text, the caveat under them
    stations = block.select("ol.come__tappe > li.come__tappa")
    assert len(stations) == 4 and block.select_one("ol")["data-steps"] == "4"
    labels = [li.select_one(".come__testo").get_text(" ", strip=True) for li in stations]
    assert labels[0].startswith("répondez aux questions") and labels[-1].endswith("acteurs compétents.")
    assert all(li.select_one(".come__testo .visually-hidden") for li in stations[:-1]), "the arrows kept as text"
    assert block.select_one(".come__avvertenza").get_text(strip=True) == text.rsplit(". ", 1)[1]


def test_the_cut_never_retypes_the_sentence():
    from cms import locked_content
    from pathways import services

    for lang in ("fr", "it", "en", "ar"):
        cut = services.how_it_works(lang)
        assert cut is not None and cut.text == locked_content.get("p3.persons.how_it_works", lang)[0]
        assert len(cut.steps) == 4 and cut.lead.endswith(": ")
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the Arabic is the provisional rendering, in the page's language
        assert cut.lang == ("" if lang in ("fr", "ar") else "fr")


def test_the_programme_numbers_its_rows_when_not_every_row_has_a_time(interior):
    """CREATIVE_DIRECTION_V5 §20 (the fix pass, m1): a time column only when every row has a time."""
    from bs4 import BeautifulSoup

    from cms import locked_content

    programme = BeautifulSoup(_main(interior("/fr/forum/")), "html.parser").select_one("ol.forum-programme")
    assert "forum-programme--timed" not in programme["class"]
    rows = programme.select(":scope > li")
    assert len(rows) == 8 and all(row.select_one(".forum-programme__num") for row in rows)
    first = rows[0].select_one(".forum-programme__title").get_text()
    assert first == locked_content.get("p2.forum.programme.items", "fr")[0][0], "the first row's words whole"


def test_a_programme_with_every_row_timed_keeps_its_time_column(client, seeded, phase3_open, legal_published):
    from bs4 import BeautifulSoup

    from forum.services import current_event

    event = current_event()
    for index, item in enumerate(event.programme_items.all(), start=1):
        item.time_label = f"{14 + index}h00"
        item.save()
    html = client.get("/fr/forum/").content.decode("utf-8")
    programme = BeautifulSoup(_main(html), "html.parser").select_one("ol.forum-programme")
    assert "forum-programme--timed" in programme["class"]
    assert [t.get_text() for t in programme.select(".forum-programme__time")][:2] == ["15h00", "16h00"]
    assert not programme.select(".forum-programme__num")


def test_french_on_an_arabic_page_says_so(client, seeded, phase3_open, legal_published):
    """WCAG 3.1.2 (the fix pass, m6): the Forum's untranslated eyebrow and name, the trail's link to it, the FAQ's
    question and answer on /ar/agami/ — each carries its language on its own element."""
    from bs4 import BeautifulSoup

    from forum.models import ModeOverride
    from forum.services import current_event

    event = current_event()
    event.mode_override = ModeOverride.PERMANENT
    event.save()
    forum = BeautifulSoup(client.get("/ar/forum/").content, "html.parser")
    # FINAL_DELIVERY_V2 §3.6 / ARABIC_AUDIT W1.2 (V5.20, the steward's amendment at the v524-pub2 merge): the eyebrow is
    # a team string of its own, translated (the catalogue's Arabic) — it reads Arabic with no lang of its own, where it
    # was the locked paragraph's French clause marked lang="fr" (stronger: no French at all)
    eyebrow = forum.select_one(".forum-hero__eyebrow")
    assert not eyebrow.get("lang") and re.search(r"[\u0600-\u06ff]", eyebrow.get_text())
    assert forum.select_one("h1.forum-hero__title").get("lang") == "fr"
    register = BeautifulSoup(client.get("/ar/forum/inscription/").content, "html.parser")
    assert register.select_one('.breadcrumbs a[href="/ar/forum/"] span[lang="fr"]')
    french = BeautifulSoup(client.get("/fr/forum/").content, "html.parser")
    assert not french.select_one(".forum-hero__eyebrow").get("lang") and not french.select_one("h1").get("lang")
    agami = BeautifulSoup(client.get("/ar/agami/").content, "html.parser")
    # V5.22 (SECTION_SYSTEM_V2 §3.17 AG-2; strict rule V5.20): the FAQ's near-identical answer is a disclosure row under
    # the promoter's text, no longer a chapter — its question the disclosure's summary, still carrying its language
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the FAQ's question is
    # compositional (C-UI) and reads Arabic; its answer is substantive (C-SUBST-FR) and this is not its page — the
    # Arabic pointer line in its place; neither says French
    from django.utils import translation

    from cms import locked_content, locked_renderings

    arabic = re.compile(r"[\u0600-\u06ff]")
    question = agami.select_one("details summary #agami-faq-title")
    assert not question.get("lang") and arabic.search(question.get_text())
    answer = agami.select_one("p[data-faq]")
    entries = locked_content.LOCKED_TEXTS["fr"]["p3.faq.items"]
    index = next(i for i, item in enumerate(entries) if item["key"] == answer["data-faq"])
    subkey = f"p3.faq.items[{index}].answer"
    assert locked_renderings.treatment(subkey) == "C-SUBST-FR"
    with translation.override("ar"):
        pointer = str(locked_renderings.pointer_line(subkey))
    assert not answer.get("lang") and answer.get_text().strip() == pointer


#: the area's template folders (plan §3.5 item 1, «Owns»)
AREA_TEMPLATES = ("pages", "ecosystem", "orientation", "pathways", "forum")


def test_no_template_comment_spans_two_lines():
    """
    The fix pass: Django's `{# … #}` holds on one line only — written over two, it is text, and on /agami/ its words
    stood on the page in both languages. A comment that needs two lines is a {% comment %} block.
    """
    found = []
    for folder in AREA_TEMPLATES:
        for path in sorted((ROOT / "templates" / folder).rglob("*.html")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                opened = line.rfind("{#")
                if opened >= 0 and "#}" not in line[opened:]:
                    found.append(f"{path.relative_to(ROOT).as_posix()}:{number}")
    assert not found, found


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("path", INTERIOR)
def test_no_template_syntax_reaches_the_page(interior, path, lang):
    main = _main(interior(path.replace("/fr/", f"/{lang}/", 1)))
    for token in ("{#", "#}", "{%", "%}", "{{", "}}"):
        assert token not in main, (path, lang, token)


def test_the_index_and_the_targets_and_the_pilot_s_row_in_the_sheet():
    """
    The fix pass: the entrance's index is one link a row at every width (m3); the forward links' boxes stand on SP-8's
    floor and on 44 px under a finger (A11Y_PERF finding 1); the pilot's eight stations stand in one row only from
    90rem (M5: «ACCOMPAGNEMENT» broke in its middle at 1280 and 1366). The budget pass: the trail is the shared page's
    (v5/_pagina.css §1, W3-F2's drawing) — a 24 px box at rest, its target 44 px under a finger without a taller line.
    """
    css = (ROOT / "static" / "css" / "v5" / "_interior.css").read_text(encoding="utf-8")
    assert "porta__stair" not in css
    assert not re.search(r"\.sommaire__list\s*\{[^}]*flex-wrap", css), "no row of wrapped links"
    floor = re.search(r"\.chapter__more > a,\s*\.chapter__links > a \{([^}]*)\}", css)
    assert floor and "min-block-size: var(--hit-min)" in floor.group(1)
    coarse = css.split("@media (pointer: coarse)", 1)[1].split("}\n}", 1)[0]
    for target in (".chapter__more > a", ".chapter__links > a"):
        assert target in coarse
    assert "min-block-size: var(--hit-primary)" in coarse
    assert ".breadcrumbs" not in re.sub(r"/\*.*?\*/", "", css, flags=re.S), (
        "the trail is drawn once, in the shared page"
    )
    page = re.sub(r"/\*.*?\*/", "", PAGE.read_text(encoding="utf-8"), flags=re.S)
    trail = re.search(r"(?<![\w-])\.breadcrumbs__item a \{([^}]*)\}", page).group(1)
    assert "display: inline-block;" in trail and "padding-block: 2px;" in trail, "a 24 px box, its line 20 px"
    finger = page.split("@media (pointer: coarse)", 1)[1].split("}\n}", 1)[0]
    assert re.search(r"\.breadcrumbs__item a::after \{[^}]*inset-block: -10px;", finger), "44 px under a finger"
    assert re.search(r"\.breadcrumbs__list \{\s*row-gap: var\(--s-5\);", finger), "two rows never overlap"
    # (merge of design-v5 into v522-p2, V5.20 strict rule: the coarse-pointer rows of this loop both left with their
    # markup — the contact address is the head's action, the pathway terms are disclosures —, each replaced below by
    # a 44 px floor under every pointer, a stronger invariant; the loop with no row left goes)
    # V5.22 (SECTION_SYSTEM_V2 §3.12 C0 + C1; strict rule V5.20): the contact page's «Par e-mail» chapter left — its
    # address is the head's action, said once. That link stands on 44 px at every pointer, not only under a finger: a
    # row centred on its 48 px disc (v5/_fronte.css «the address, the head's action»)
    fronte = re.sub(r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v5" / "_fronte.css").read_text(encoding="utf-8"), flags=re.S)
    link = re.search(r"\.fronte-azione__link \{([^}]*)\}", fronte).group(1)
    disc = re.search(r"\.fronte-azione__disc \{([^}]*)\}", fronte).group(1)
    assert "display: inline-flex;" in link and "align-items: center;" in link
    assert "inline-size: 48px;" in disc and "block-size: 48px;" in disc and "flex: none;" in disc
    # V5.22 (SECTION_SYSTEM_V2 §3.5 PS-4, §3.10 D1 — approved owner/product decisions; lane P1; V5.20 strict rule):
    # a pathway's Italian terms are disclosures that open their definitions in place; each term's summary — the
    # target — stands on 44 px under every pointer, not only a finger (a stronger floor than the chip's coarse band)
    for sheet, target in (
        ("static/css/v5/_sec-indice.css", ".indice__sommario"),
        ("apps/pathways/static/pathways/_diplomas.css", ".dossier__voce"),
    ):
        text = re.sub(r"/\*.*?\*/", "", (ROOT / sheet).read_text(encoding="utf-8"), flags=re.S)
        assert re.search(r"(?m)^" + re.escape(target) + r" \{[^}]*min-block-size: var\(--hit-primary", text), target
    # V5.22 (SECTION_SYSTEM_V2 §3.3 PP-1: «≥ 80 rem: one gently stepped row» on lane S's «la linea V2»; V5.20 strict
    # rule): M5's invariant — no locked capital broken inside a word, no two labels meeting, at 1280 and 1366 — is the
    # pilot's caps rule and its stepped row in the family's one modifier sheet of the passage: from 80 rem the even
    # stations' capitals stand below the route (row 5), the odd ones' above it (row 1), each with two columns' room less
    # 16 px (QA_ROUND1 M1, m12); measured in the browser at 1280, 1366, 1440 and 1920 in four languages
    # (tests/frontend/test_pages_browser_v522_p1.py::test_the_pilot_s_capitals_never_break_inside_a_word)
    spaces = (ROOT / "apps" / "ecosystem" / "static" / "ecosystem" / "_spaces.css").read_text(encoding="utf-8")
    spaces = re.sub(r"/\*.*?\*/", "", spaces, flags=re.S)
    caps = r"\.pilota-rotta \.linea--large \.linea__label--caps \{\s*overflow-wrap: normal;\s*hyphens: manual;"
    assert re.search(caps, spaces)
    # FINAL MICRO-PASS §5 A2 (V5.20 strict rule: the 80 rem stepped row — capitals · numeral · tile · numeral ·
    # capitals — left with the stations' tiles and numerals): the eight stations stand on the route's own composition,
    # four to a row from 48 rem (v5/_linea-v2.css), each label in its own column under its quiet marker, so no two labels
    # can meet; the caps rule above still keeps every locked capital whole
    assert "@media (min-width: 80rem)" not in spaces and "linea__segno" not in spaces
    linea = re.sub(
        r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v5" / "_linea-v2.css").read_text(encoding="utf-8"), flags=re.S
    )
    assert "grid-template-columns: repeat(var(--lv-n, 4), minmax(0, 1fr));" in linea
    assert ".pilot-diagram" not in spaces, "the V5.4 rule left with its markup"


@pytest.mark.parametrize("path", INTERIOR)
def test_one_primary_action_and_at_most_six_icons_in_the_body(interior, path):
    main = _main(interior(path))
    assert len(re.findall(r'class="btn btn--primary\b', main)) <= 1, path
    # the chapter heads' concept marks apart (V5.12 §7: they replaced the one stair; each is one head's, at most
    # once per concept on a page — tests/frontend/test_icons.py)
    # the glyph tiles of a form's steps and side (V5.15 W3, lane B: the icon system's concept tiles, like the heads'
    # marks) are the form's structure, not body icons
    main = re.sub(r'<span class="glyph-tile[^"]*"[^>]*>.*?</span>', "", main, flags=re.S)
    # and so are a field's own glyphs inside its control (the e-mail's at-sign, the telephone's handset: the v515-b
    # merge, where lane C's composed /entreprises/ and lane B's public form first met on one page)
    main = re.sub(r'<svg class="icon form-field__glyph"[^>]*>.*?</svg>', "", main, flags=re.S)
    heads = re.findall(r'<svg class="icon chapter__mark[^"]*"[^>]*><use href="[^"#]*#icon-([a-z0-9-]+)"', main)
    body_icons = ICON.findall(main)
    # V5.15 W3: the frontispiece's folio glyph is the head's concept mark, as a chapter head's is — not the body's
    heads += re.findall(r'<span class="fronte__glyph" aria-hidden="true"><svg class="icon"[^>]*><use href="[^"#]*#icon-([a-z0-9-]+)"', main)
    # V5.15 W3 round 1 (v515-c-improve1): the network head's diagram (aria-hidden) draws the five actors' glyphs on its
    # ring — the head's drawing, as the folio glyph is; the register below keeps its own glyphs under the ceiling
    heads += re.findall(r'<span class="fronte-rete__disc"><svg class="icon"[^>]*><use href="[^"#]*#icon-([a-z0-9-]+)"', main)
    heads += re.findall(r'<span class="fronte-azione__disc" aria-hidden="true"><svg class="icon"[^>]*><use href="[^"#]*#icon-([a-z0-9-]+)"', main)
    for name in heads:
        body_icons.remove(name)
    assert "ile-steps" not in body_icons, (path, "the journey's stair in a public body")
    # V5.22 (SECTION_SYSTEM_V2 §4.10 — an approved owner/product decision; lane S): a register of named entities — the
    # PATHWAY index, the pilot's eight stations, the Forum's nine actors — draws its glyphs all or none and counts as ONE
    # register ([data-registro], the library's own marker since v522-s2 — the chip's data-register stays the chip
    # partial's, DL54-182 item 10 c — and a chip's register mark read as before); every body icon is a registered symbol,
    # one concept once a section (DS V5 §14.2; V5.20 strict rule: the cap of six holds for loose icons, the registers
    # gain an all-or-none rule they lacked)
    registers = re.findall(r'<(\w+)[^>]*\bdata-registr(?:o|er)\b[^>]*>(.*?)</\1>', main, flags=re.S)
    for _tag, register in registers:
        rows = re.findall(r"<li\b([^>]*)>(.*?)</li>", register, flags=re.S)
        # V5.22 (SECTION_SYSTEM_V2 §2 K «l'approdo»: «the Forum tile is typographic on a night face (Q4); the others are
        # raised paper with a T2 or T2a glyph»; lane P2, strict rule V5.20): the closing band's Forum tile never draws
        # a glyph — it stands outside the all-or-none, and it must stay bare; every other tile is held to the rule
        forum = [row for attrs, row in rows if "approdo__tessera--forum" in attrs]
        assert all("#icon-" not in row for row in forum), (path, "the Forum's tile is typographic (Q4)")
        items = [row for attrs, row in rows if "approdo__tessera--forum" not in attrs]
        with_glyph = [item for item in items if "#icon-" in item]
        assert not with_glyph or len(with_glyph) == len(items), (path, "a register's glyphs: all or none")
        for name in ICON.findall(register):
            body_icons.remove(name)
    assert set(body_icons) <= set(icons.SYMBOLS) | set(icons.LEGACY), (path, "a registered symbol")
    assert len(body_icons) <= 6, (path, body_icons)


@pytest.mark.parametrize("path", INTERIOR)
def test_a_plate_is_captioned_a_stock_frame_is_not_and_nothing_waits_for_a_scroll(interior, path):
    """V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6; strict rule V5.20): the count «a figure per figcaption» becomes two
    invariants — every curated plate (`figure.figura`) keeps its caption apparatus, and no stock frame
    (`figure[data-slot]`, the slot registry) carries a caption: the first is the rule as it was, the second is new.
    v524-px-improve (the reviewer's m1; V5.20, stronger): the first is held on every figure that is NOT a stock frame —
    the exact complement of the second — so the two cover every figure as the old count did."""
    main = _main(interior(path))
    # a page without a photograph (the Forum, AGAMI — Q4, Q5 —, the fraud page) has nothing to check here
    for attrs, body in re.findall(r"<figure\b([^>]*)>(.*?)</figure>", main, flags=re.S):
        if "data-slot=" not in attrs:
            assert "<figcaption" in body, (path, "a curated plate ships with its caption")
        if "data-slot=" in attrs:
            assert "<figcaption" not in body and "Pexels" not in body, (path, "a stock frame carries no credit")
    assert not re.search(r'class="[^"]*\breveal\b', main), path


@pytest.mark.parametrize("path", WITH_HELP)
def test_who_can_help_me_is_the_live_line_with_the_public_address(interior, path):
    main = _main(interior(path))
    line = main.split('class="aiuto', 1)[1].split("</p>", 1)[0]
    assert 'href="mailto:contact@agamieuromed.org"' in line, path


def test_the_universities_sentence_is_said_once(interior):
    from cms import locked_content

    main = _main(interior("/fr/universites-et-formation/"))
    assert main.count(locked_content.text("p3.universities.intro", "fr")) == 1


def test_the_pilot_sequence_stands_on_the_line(interior):
    from cms import locked_content

    main = _main(interior("/fr/projet-pilote/"))
    figure = main.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    # V5.22 (SECTION_SYSTEM_V2 §3.3 PP-1 «il tracciato pilota», lane S's «la linea V2»; V5.20 strict rule): the labels
    # are the large passage's locked capitals (their own class, the INK verb) — still the eight, whole, in order
    labels = re.findall(r'<p class="linea__label(?: linea__label--caps)?"[^>]*>(.*?)</p>', figure)
    assert labels == locked_content.get("p3.pilot.sequence", "fr")[0]
    assert "pilot-flow.svg" not in main


def test_an_authority_link_shows_its_host(client, seeded, phase3_open):
    from pathways.models import Pathway

    pathway = Pathway.objects.get(key="salaried_work")
    pathway.authorities = [
        {"name": "Sportello Unico per l'Immigrazione", "url": "https://www.interno.gov.it/", "lang": "it"}
    ]
    pathway.save()
    html = client.get("/fr/parcours/salaried_work/").content.decode("utf-8")
    # V5.22 (SECTION_SYSTEM_V2 §3.5 PS-2 «chi decide», the arc of seats on the night; V5.20 strict rule): the same
    # authority list (its class kept), an ordered arc of seats; each link still shows its host
    row = _main(html).split('authority-list"', 1)[1].split("</ol>", 1)[0]
    assert 'href="https://www.interno.gov.it/"' in row
    assert '<span class="autorita__host">interno.gov.it</span>' in row


def test_the_pathway_sheet_has_its_index_in_the_entrance_and_no_sticky_bar(client, seeded, phase3_open):
    html = client.get("/fr/parcours/salaried_work/").content.decode("utf-8")
    main = _main(html)
    entrance = main.split('<header class="ingresso', 1)[1].split("</header>", 1)[0]
    # a chapter lane C's gates hide when it is empty (V5.12 §13: «Aperçu» without an eligibility text, «Documentation»
    # without a document) has no entry in the index either (the v512 W1 merge, the review's M1)
    anchors = ("apercu", "etapes", "documentation", "autorites", "avertissements", "ressources", "orientation")
    drawn = [anchor for anchor in anchors if f'<section id="{anchor}"' in main]
    assert {"etapes", "orientation"} <= set(drawn), drawn
    for anchor in anchors:
        assert (f'href="#{anchor}"' in entrance) is (anchor in drawn), anchor
    assert "section-nav" not in html


@pytest.mark.parametrize(
    ("sheet", "imports"),
    [
        (
            "apps/ecosystem/static/ecosystem/ecosystem.css",
            [
                "../css/v5/_pagina.css",
                "../css/v5/_interior.css",
                "../css/v5/_journey-passage.css",
                "../css/v5/_porta.css",
                "../css/v5/_photo.css",
                "../css/v5/_compose.css",
                "_spaces.css",
            ],
        ),
        # V5.22 (SECTION_SYSTEM_V2 §3.16, lane S's request §8; lane P2, strict rule V5.20): the library's shell and the
        # seat a page imports before its partial — still nothing but imports
        (
            "apps/forum/static/forum/forum.css",
            [
                "../css/v5/_pagina.css",
                "../css/v5/_interior.css",
                "../css/v5/_sezioni.css",
                "../css/v5/_sigillo.css",
                # FINAL_DELIVERY_V2 §3.6, R3 (lane PUB2; V5.20, the steward's amendment at the v524-pub2 merge): the
                # library's material partial for the Forum raccordo — still nothing but imports
                "../css/v5/_materia.css",
                "_forum.css",
            ],
        ),
        (
            "apps/pages/static/pages/css/interior.css",
            [
                "../../css/v5/_pagina.css",
                "../../css/v5/_interior.css",
                "../../css/v5/_photo.css",
                "../../css/v5/_compose.css",
                # V5.22 (SECTION_SYSTEM_V2 §3.2, §3.11, §3.12, §3.17, §3.18; lane P2, strict rule V5.20): the library's
                # shell and the three patterns the pages compose (C, E, K), then each page's V2 partial
                "../../css/v5/_sezioni.css",
                "../../css/v5/_sec-racconto.css",
                "../../css/v5/_sec-mosaico.css",
                "../../css/v5/_sec-strato.css",
                "_institutional.css",
                "_canali.css",  # V5.19 (lane v519-k): the contact page's telephone channels
                # FINAL_DELIVERY_V2 §3.6, R4 a (lane PUB2; V5.20, the steward's amendment at the v524-pub2 merge): Le
                # projet's partial on its own route sheet (below) with the material partial, linked by that page only
                "_contatto.css",
                # V5.22 lane P2 round 2 (QA_ROUND2 m5; the owner's V5.22 «route-specific bundles with their own recorded
                # budgets»; strict rule V5.20): Réseau's, AGAMI's and the fraud page's partials are their route sheets'
                # (below), linked by those pages only — still nothing but imports
            ],
        ),
        # V5.20, citing V5.30 §7: the Italy + Morocco primitive under Réseau's closing band joins its sheet, once
        ("apps/pages/static/pages/css/rete.css", ["../../css/v5/_intesa.css", "_rete.css"]),
        ("apps/pages/static/pages/css/agami.css", ["_agami.css"]),
        ("apps/pages/static/pages/css/frodi.css", ["_frodi.css"]),
        ("apps/pages/static/pages/css/projet.css", ["../../css/v5/_materia.css", "_projet.css"]),
        # FINAL MICRO-PASS §6 B1 (V5.20): the explorer's pattern partial left the FAQ's route sheet with the explorer
        ("apps/cms/static/cms/faq.css", ["_faq-v2.css"]),
        ("apps/cms/static/cms/lessico.css", ["_lessico-v2.css"]),
        (
            "apps/pathways/static/pathways/pathways.css",
            [
                "../css/v5/_pagina.css",
                "../css/v5/_interior.css",
                "../css/v5/_journey-passage.css",
                "../css/v5/_porta.css",
                "../css/v5/_photo.css",
                "../css/v5/_compose.css",
                "_pathways.css",
            ],
        ),
    ],
)
def test_page_sheets_are_plain_import_lists_in_the_collected_tree(sheet, imports):
    """Each page sheet is a list of imports a later family extends with one line (W3-D's passage; DS 2026 §2)."""
    text = (ROOT / sheet).read_text(encoding="utf-8")
    without_comments = re.sub(r"/\*.*?\*/", "", text, flags=re.S).strip()
    assert re.findall(r'@import url\("([^"]+)"\);', without_comments) == imports
    assert re.sub(r'@import url\("[^"]+"\);', "", without_comments).strip() == "", "nothing but imports"


def test_the_interior_grammar_never_enters_main_css():
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "_interior.css" not in main and "_porta.css" not in main and "_pagina.css" not in main


#: the components every page of the public interior draws — one drawing each, in the shared page (the owner's V5.8:
#: no duplicated component families; W3-F2's review m11), never again in a surface's own partial
SHARED_RULES = (
    ".breadcrumbs__item a {",
    ".breadcrumbs__item[aria-current] {",
    ".ingresso,\n.page-header {",
    ".ingresso__title,\n.page-header__title {",
    ".ingresso__lead,\n.page-header__lead {",
    ".chapter__inner {",
    ".chapter__mark {",
    ".chapter__title,\n.chapter__head > h2:not([class]) {",
    ".chapter__label {",
    ".registro {",
    ".registro__row {",
    ".registro__text {",
    ".autorita__host {",
    ".figura img {",
    ".aiuto {",
)


def test_one_page_partial_draws_the_interior_s_shared_components_for_both_families():
    """The budget pass: W3-F1's _interior.css and W3-F2's _lettura.css drew the trail, the head, the chapters, the
    register and D26's shared slots value for value; they are drawn once, in static/css/v5/_pagina.css, the first
    import of both families' page sheets, and neither partial draws them again."""
    page = re.sub(r"/\*.*?\*/", "", PAGE.read_text(encoding="utf-8"), flags=re.S)
    own = {
        name: re.sub(r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v5" / name).read_text(encoding="utf-8"), flags=re.S)
        for name in ("_interior.css", "_lettura.css")
    }
    for rule in SHARED_RULES:
        assert len(re.findall(r"(?m)^" + re.escape(rule), page)) == 1, rule
        for name, css in own.items():
            head = rule.split(",")[0].split(" {")[0]
            assert not re.search(r"(?m)^\s*" + re.escape(head) + r"\s*[,{]", css), (name, head)
    importers = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "apps").glob("*/static/**/*.css")
        if "_pagina.css" in path.read_text(encoding="utf-8")
    )
    assert importers == [
        "apps/cms/static/cms/lettura.css",
        "apps/ecosystem/static/ecosystem/ecosystem.css",
        "apps/forum/static/forum/forum.css",
        "apps/orientation/static/orientation/wizard.css",
        "apps/pages/static/pages/css/interior.css",
        "apps/pathways/static/pathways/pathways.css",
    ]
    for path in importers:
        imports = re.findall(r'@import url\("([^"]+)"\);', (ROOT / path).read_text(encoding="utf-8"))
        assert imports[0].endswith("css/v5/_pagina.css"), (path, "the shared page first, then the surface's own")
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|gradient\(", page), "tokens only"
    assert not re.search(r"(?<![\w-])(margin|padding|border)-(left|right|top|bottom)\s*:", page), "logical only"
    tokens = (ROOT / "static" / "css" / "v5" / "tokens.css").read_text(encoding="utf-8")
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", tokens + page))
    assert set(re.findall(r"var\((--[a-z0-9-]+)", page)) <= declared


def test_the_door_card_loads_only_where_a_door_is_drawn():
    """
    The fix pass (V5.8: a surface's own CSS loads only where it is drawn): the door card and its way in are the doors'
    own — static/css/v5/_porta.css, imported by the two door sheets alone; the interior's grammar, which the Forum,
    the project's pages and the questionnaire load too, carries none of it.
    """
    source = (ROOT / "static" / "css" / "v5" / "_interior.css").read_text(encoding="utf-8")
    interior = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    assert not re.search(r"\.porta\b|\.via__|\.ingresso__way", interior)
    importers = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "apps").glob("*/static/**/*.css")
        if "_porta.css" in path.read_text(encoding="utf-8")
    )
    assert importers == ["apps/ecosystem/static/ecosystem/ecosystem.css", "apps/pathways/static/pathways/pathways.css"]
