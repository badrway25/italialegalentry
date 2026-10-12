"""
Design V5 core components, part 2, in a browser (W1-C; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.3 item 7) — what the
sources cannot show (tests/frontend/test_chips_cards_w1_c.py holds the rules):

* the eight registers are drawn with their marks from the sprite, each chip exactly 24 px, never by colour alone: the
  mark's drawing and the edge's style differ where the colours are close; the word holds 4.5 : 1 on its body and
  the mark 3 : 1, on paper and on night; «conforme» is ink, «En examen» is lapis;
* 20 / 24 / 28 px exactly, in French and in Arabic — where the mark sits on the reading side and the text is not
  under 14 px;
* a long word wraps with its mark on the first line and never widens the page; in a table cell it does not wrap;
* the gauge of a case status and the dotted edge of a value the registry does not know;
* under forced colours the edge style, the mark and the word remain;
* a chip is not a control; a tag that is a link is hit in 44 px under a coarse pointer;
* the filter's legend draws the chip's mark at 14 px, as wide as the dot it replaced;
* the cards sit on their levels with one radius, a hovered record strengthens its hairline and moves no shadow, and
  the summary strip fills its rows.

Chromium on the live server, on the development showcase (/_design/, DEBUG only), which draws every one of them
through the product's own tag and sheets.
"""

from __future__ import annotations

import importlib
import os

import pytest
from django.test import override_settings
from django.urls import clear_url_caches

from core import chips, icons

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: Every chip and tag of a container: its box, its paint, its mark, its word.
CHIPS_JS = """(selector) => {
  const rgb = (v) => { const m = /rgba?\\(([^)]+)\\)/.exec(v); const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
                       return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lum = (c) => { const f = (x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); };
                       return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  return [...document.querySelectorAll(selector + ' :is(.chip, .tag)')].map((el) => {
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    const mark = el.querySelector(':scope > svg.chip__g'); const word = el.querySelector(':scope > .chip__w');
    const mr = mark ? mark.getBoundingClientRect() : null; const wr = word ? word.getBoundingClientRect() : null;
    const body = rgb(cs.backgroundColor); const ink = rgb(cs.color);
    const markInk = mark ? rgb(getComputedStyle(mark).color) : null;
    const meter = el.querySelector(':scope > .chip__meter');
    return {
      tag: el.tagName.toLowerCase(), cls: el.className, register: el.getAttribute('data-register'),
      text: (word || el).textContent.trim(), tabIndex: el.tabIndex, cursor: cs.cursor,
      width: r.width, height: r.height, top: r.top, left: r.left, right: r.right,
      radius: parseFloat(cs.borderTopLeftRadius), edge: cs.borderTopStyle, edgeWidth: cs.borderTopWidth,
      colour: cs.color, body: cs.backgroundColor, edgeColour: cs.borderTopColor, fontSize: parseFloat(cs.fontSize),
      symbol: mark ? mark.querySelector('use').getAttribute('href').split('#icon-')[1] : null,
      mark: mr ? { width: mr.width, height: mr.height, left: mr.left, right: mr.right, top: mr.top, colour: getComputedStyle(mark).color } : null,
      word: wr ? { left: wr.left, right: wr.right, height: wr.height } : null,
      wordOnBody: body.a ? ratio(ink, body) : null, markOnBody: markInk && body.a ? ratio(markInk, body) : null,
      notches: meter ? [...meter.children].map((n) => getComputedStyle(n).backgroundColor !== 'rgba(0, 0, 0, 0)') : null,
      meterLeft: meter ? meter.getBoundingClientRect().left : null,
    };
  });
}"""
#: The resolved value of a shadow token, as the browser writes a computed box-shadow.
SHADOW_JS = """(name) => { const probe = document.createElement('i'); probe.style.boxShadow = `var(${name})`;
  document.body.appendChild(probe); const value = getComputedStyle(probe).boxShadow; probe.remove(); return value; }"""
#: The resolved value of a colour token.
COLOUR_JS = """(name) => { const probe = document.createElement('i'); probe.style.backgroundColor = `var(${name})`;
  document.body.appendChild(probe); const value = getComputedStyle(probe).backgroundColor; probe.remove(); return value; }"""
EXPECTED = [  # the first row of the showcase's «Pastilles»: register, mark
    ("conforme", "st-conforme"),
    ("esame", "st-esame"),
    ("neutro", "st-neutro"),
    ("attesa", "st-attesa"),
    ("attesa", "st-attesa-replace"),
    ("azione", "st-azione"),
    ("rifiuto", "st-rifiuto"),
    ("blocco", "lock"),
    ("nullo", "st-nullo"),
]


@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


@pytest.fixture
def showcase(live_server, seeded):
    """The development showcase on the live server: ``config/urls.py`` registers /_design/ at import time, with DEBUG
    on only, so the URLconf is rebuilt for the test and put back after it (tests/frontend/test_browser_w1_c.py)."""
    import config.urls

    with override_settings(DEBUG=True):
        clear_url_caches()
        importlib.reload(config.urls)
        yield live_server.url + "/_design/"
    clear_url_caches()
    importlib.reload(config.urls)


def _open(browser, width=1440, height=900, **kwargs):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **kwargs)
    return context, context.new_page()


def _rows(page) -> list[str]:
    """The three rows of chips of the showcase's «États», as selectors (they are the first three `.ds__row` there)."""
    return page.evaluate(
        """() => [...document.querySelectorAll('#etats .ds__row')].slice(0, 3).map((row, i) => {
             row.setAttribute('data-chip-row', i); return `#etats [data-chip-row="${i}"]`; })"""
    )


# ---- the registers ----------------------------------------------------------------------------------------------


def test_the_eight_registers_are_drawn_with_their_marks_at_24px_and_never_by_colour_alone(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        registers, _kinds, _sizes = _rows(page)
        drawn = page.evaluate(CHIPS_JS, registers)
        assert [(c["register"], c["symbol"]) for c in drawn] == EXPECTED
        assert {c["register"] for c in drawn} == set(chips.REGISTERS), "the eight, all of them"
        for chip in drawn:
            name = f"{chip['register']} «{chip['text']}»"
            assert chip["height"] == 24, f"{name}: {chip['height']} px"
            assert chip["radius"] >= 12, f"{name}: a pill"
            assert chip["edgeWidth"] == "1px"
            assert (chip["mark"]["width"], chip["mark"]["height"]) == (16, 16), name
            assert chip["mark"]["left"] - chip["left"] == 4, f"{name}: 1 px of edge and 3 px — concentric with the cap"
            assert chip["word"]["left"] - chip["mark"]["right"] == 6, name
            assert chip["wordOnBody"] >= 4.5, f"{name}: word {chip['wordOnBody']:.2f} : 1"
            assert chip["markOnBody"] >= 3, f"{name}: mark {chip['markOnBody']:.2f} : 1"
            assert chip["fontSize"] == 13
        by_register = {c["register"]: c for c in drawn}
        styles = {register: chip["edge"] for register, chip in by_register.items()}
        assert styles == {**dict.fromkeys(chips.REGISTERS, "solid"), "attesa": "dashed", "nullo": "dotted"}, styles
        assert len({c["symbol"] for c in drawn}) == 9, "nine drawings for nine chips: the mark tells them apart"
        # conforme is ink — the same ink for the word and the disc, no chroma to mean approval; «En examen» is lapis
        assert by_register["conforme"]["colour"] == by_register["conforme"]["mark"]["colour"] == "rgb(21, 34, 42)"
        assert by_register["esame"]["mark"]["colour"] == "rgb(82, 120, 193)", "the register's lapis, #5278c1"
        assert by_register["esame"]["symbol"] not in icons.CHECK_BEARING and by_register["conforme"]["symbol"] == "st-conforme"
    finally:
        context.close()


def test_on_night_the_same_registers_keep_their_contrast(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        registers, _kinds, _sizes = _rows(page)
        paper = page.evaluate(CHIPS_JS, registers)
        page.evaluate("(s) => document.querySelector(s).classList.add('on-inverse')", registers)
        night = page.evaluate(CHIPS_JS, registers)
        for before, after in zip(paper, night, strict=True):
            name = f"{after['register']} «{after['text']}»"
            assert after["body"] != before["body"] and after["colour"] != before["colour"], f"{name}: re-pointed on night"
            assert after["wordOnBody"] >= 4.5, f"{name}: word {after['wordOnBody']:.2f} : 1 on night"
            assert after["markOnBody"] >= 3, f"{name}: mark {after['markOnBody']:.2f} : 1 on night"
            assert (after["height"], after["edge"], after["symbol"]) == (before["height"], before["edge"], before["symbol"])
    finally:
        context.close()


def test_twenty_twenty_four_and_twenty_eight_px_in_french_and_in_arabic(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        _registers, _kinds, sizes = _rows(page)
        french = page.evaluate(CHIPS_JS, sizes)[:3]
        assert [c["height"] for c in french] == [20, 24, 28]
        assert [c["mark"]["width"] for c in french] == [14, 16, 16]
        assert [c["fontSize"] for c in french] == [12, 13, 13]
        assert all(c["mark"]["left"] < c["word"]["left"] for c in french), "the mark leads, on the reading side"

        # the same three chips set in Arabic: the catalogue's «قيد الفحص» stands in for the sample words
        page.evaluate(
            """(s) => { const row = document.querySelector(s); row.lang = 'ar'; row.dir = 'rtl';
                 row.querySelectorAll('.chip__w').forEach((w) => { w.textContent = 'قيد الفحص'; }); }""",
            sizes,
        )
        page.evaluate("document.fonts.ready.then(() => 1)")
        arabic = page.evaluate(CHIPS_JS, sizes)[:3]
        assert [c["height"] for c in arabic] == [20, 24, 28], "exact in every script"
        assert [c["mark"]["width"] for c in arabic] == [14, 16, 16]
        assert all(c["fontSize"] >= 14 for c in arabic), "never under 14 px in Arabic"
        for chip in arabic:
            assert chip["mark"]["right"] > chip["word"]["right"], "the mark is on the reading side: the right"
            assert chip["right"] - chip["mark"]["right"] in (3, 4, 6), chip
        scroll_w, client_w = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        assert scroll_w <= client_w
    finally:
        context.close()


def test_a_long_word_wraps_with_its_mark_on_the_first_line_and_not_in_a_table_cell(browser, showcase):
    context, page = _open(browser, 390, 844)
    try:
        page.goto(showcase, wait_until="networkidle")
        registers, _kinds, _sizes = _rows(page)
        state = page.evaluate(
            """(s) => {
              const chip = document.querySelector(s + ' .chip');
              chip.querySelector('.chip__w').textContent = 'Vérification professionnelle nécessaire';
              const column = document.createElement('div'); column.style.inlineSize = '180px';
              const wrapped = chip.cloneNode(true); column.appendChild(wrapped);
              const table = document.createElement('table'); table.style.inlineSize = '90px';
              table.innerHTML = '<tbody><tr><td></td></tr></tbody>';
              const cell = chip.cloneNode(true); table.querySelector('td').appendChild(cell);
              chip.parentElement.append(column, table);
              const box = (e) => e.getBoundingClientRect();
              return { width: box(wrapped).width, height: box(wrapped).height, markTop: box(wrapped.querySelector('svg')).top - box(wrapped).top,
                       wordHeight: box(wrapped.querySelector('.chip__w')).height,
                       columnScroll: column.scrollWidth, columnClient: column.clientWidth,
                       cellHeight: box(cell).height, cellWidth: box(cell).width, cellWrap: getComputedStyle(cell).whiteSpace,
                       columnOfTheTable: box(table.querySelector('td')).width };
            }""",
            registers,
        )
        assert state["width"] <= 180 and state["wordHeight"] >= 40, "the word goes to a second line; it is never cut"
        assert state["height"] == state["wordHeight"] + 4, "the line, the block padding and the edge"
        assert state["markTop"] == 4, "the mark stays centred on the first line"
        assert state["columnScroll"] <= state["columnClient"], "a chip never widens what holds it"
        assert state["cellWrap"] == "nowrap" and state["cellHeight"] == 24 and state["cellWidth"] > 90, "one line in a cell"
        assert state["columnOfTheTable"] >= state["cellWidth"], "and the column takes the chip's width — nothing overflows it"
    finally:
        context.close()


def test_the_gauge_of_a_case_status_and_the_dotted_edge_of_an_unknown_value(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        _registers, _kinds, sizes = _rows(page)
        drawn = page.evaluate(CHIPS_JS, sizes)
        training = next(c for c in drawn if c["notches"])
        assert training["register"] == "neutro" and training["notches"] == [True, True, False], "under way: two of three"
        assert training["meterLeft"] > training["word"]["right"], "after the word"
        assert training["height"] == 24
        unknown = next(c for c in drawn if "chip" in c["cls"].split() and c["register"] is None)
        assert unknown["edge"] == "dotted" and unknown["symbol"] == "st-neutro", "seen, and still a chip with its mark"
        tags = [c for c in drawn if "tag" in c["cls"].split()]
        assert [c["tag"] for c in tags] == ["a", "span"]
        for tag in tags:
            assert tag["register"] is None and tag["symbol"] is None and tag["height"] == 24, "a term: no register, no mark"
    finally:
        context.close()


def test_under_forced_colours_the_edge_the_mark_and_the_word_remain(browser, showcase):
    context, page = _open(browser, forced_colors="active")
    try:
        page.goto(showcase, wait_until="networkidle")
        assert page.evaluate("matchMedia('(forced-colors: active)').matches")
        registers, _kinds, _sizes = _rows(page)
        drawn = page.evaluate(CHIPS_JS, registers)
        assert [(c["register"], c["symbol"]) for c in drawn] == EXPECTED
        styles = {c["register"]: c["edge"] for c in drawn}
        assert styles["attesa"] == "dashed" and styles["nullo"] == "dotted" and styles["conforme"] == "solid"
        for chip in drawn:
            assert chip["mark"]["colour"] == chip["colour"], "the mark is the ink of its word (components.css §2)"
            assert chip["body"] != chip["colour"] and chip["edgeColour"] != chip["body"], chip["register"]
            assert chip["height"] == 24
        solid_ink = next(c for c in drawn if c["register"] == "conforme")
        assert solid_ink["edgeColour"] == solid_ink["colour"], "the edge is the system's text colour"
        ink = {c["register"]: c["colour"] for c in drawn}
        assert len({ink[r] for r in chips.REGISTERS if r != "nullo"}) == 1, "one system ink for seven registers"
        assert ink["nullo"] != ink["conforme"], "what carries nothing is the system's grey text"
    finally:
        context.close()


def test_a_chip_is_not_a_control_and_a_link_tag_is_hit_in_44px(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        registers, _kinds, sizes = _rows(page)
        before = page.evaluate(CHIPS_JS, registers)
        assert all(c["tag"] == "span" and c["tabIndex"] == -1 and c["cursor"] == "auto" for c in before)
        page.hover(f"{registers} .chip")
        page.wait_for_timeout(250)
        after = page.evaluate(CHIPS_JS, registers)
        assert [(c["body"], c["colour"], c["edgeColour"], c["height"], c["mark"]["colour"]) for c in after] == [
            (c["body"], c["colour"], c["edgeColour"], c["height"], c["mark"]["colour"]) for c in before
        ], "a status does not answer the pointer"
        link = page.evaluate(
            """(s) => { const a = document.querySelector(s + ' a.tag'); const cs = getComputedStyle(a);
                 return { edge: cs.borderTopColor, body: cs.backgroundColor, underline: cs.textDecorationLine }; }""",
            sizes,
        )
        page.hover(f"{sizes} a.tag")
        page.wait_for_timeout(250)
        hovered = page.evaluate(
            "(s) => { const cs = getComputedStyle(document.querySelector(s + ' a.tag')); return { edge: cs.borderTopColor, body: cs.backgroundColor }; }",
            sizes,
        )
        assert link["underline"] == "none" and hovered != {"edge": link["edge"], "body": link["body"]}, "a link answers"
    finally:
        context.close()

    context, page = _open(browser, 390, 844, is_mobile=True, has_touch=True)
    try:
        page.goto(showcase, wait_until="networkidle")
        assert page.evaluate("matchMedia('(pointer: coarse)').matches")
        _registers, _kinds, sizes = _rows(page)
        hit = page.evaluate(
            """(s) => { const a = document.querySelector(s + ' a.tag'); const after = getComputedStyle(a, '::after');
                 const span = getComputedStyle(document.querySelector(s + ' span.tag'), '::after');
                 return { visual: a.getBoundingClientRect().height, hit: parseFloat(after.height), top: after.top, plain: span.content }; }""",
            sizes,
        )
        assert hit["visual"] == 24 and hit["hit"] == 44 and hit["top"] == "-11px", f"22 px of padding box and 11 on each side: {hit}"
        assert hit["plain"] == "none", "a tag that is not a link has no target to extend"
    finally:
        context.close()


def test_the_filters_legend_draws_the_chips_mark_at_14px_as_wide_as_the_dot_was(browser, showcase):
    """The entry was a 10 px dot and 8 px of air; it is the state's own mark at 14 px and 4 px — the same 18 px, so
    the eight entries and the search of «Mes pièces» still share one row at 1440."""
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        entries = page.evaluate(
            """() => [...document.querySelectorAll('#console .seg .seg__link')].filter((a) => a.querySelector('.seg__dot')).map((a) => {
                 const dot = a.querySelector('.seg__dot'); const mark = dot.querySelector('svg.chip__g');
                 const text = [...a.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim());
                 const range = document.createRange(); range.selectNodeContents(text);
                 const first = [...range.getClientRects()][0]; const box = mark.getBoundingClientRect();
                 const lead = text.textContent.length - text.textContent.trimStart().length;
                 const word = document.createRange(); word.setStart(text, lead); word.setEnd(text, lead + 1);
                 return { register: dot.getAttribute('data-register'), symbol: mark.querySelector('use').getAttribute('href').split('#icon-')[1],
                          size: [box.width, box.height], gap: word.getBoundingClientRect().left - box.right,
                          colour: getComputedStyle(mark).color, dotBox: dot.getClientRects().length, lines: first ? 1 : 0 }; })"""
        )
        assert len(entries) == 7, "the seven states of a piece"
        assert [e["symbol"] for e in entries] == [
            "st-attesa", "st-neutro", "st-esame", "st-conforme", "st-rifiuto", "st-azione", "st-attesa-replace",
        ], "each state its own mark: «Manquant» and «À remplacer» no longer share one"
        for entry in entries:
            assert entry["size"] == [14, 14] and abs(entry["gap"] - 4) <= 0.5, entry
            assert entry["dotBox"] == 0, "the element that carries the register draws no box of its own"
        assert len({e["colour"] for e in entries}) == 6, "painted by the register: six registers among the seven states"
    finally:
        context.close()


# ---- the cards ----------------------------------------------------------------------------------------------------


def test_the_cards_sit_on_their_levels_with_one_radius(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        level1, level2 = page.evaluate(SHADOW_JS, "--shadow-1"), page.evaluate(SHADOW_JS, "--shadow-2")
        cards = page.evaluate(
            """() => [...document.querySelectorAll('#conteneurs .card')].map((c) => { const cs = getComputedStyle(c);
                 return { cls: c.className, radius: cs.borderTopLeftRadius, shadow: cs.boxShadow, edge: cs.borderTopColor,
                          edgeWidth: cs.borderTopWidth, sides: cs.borderLeftWidth, body: cs.backgroundColor, pad: cs.paddingTop,
                          title: getComputedStyle(c.querySelector('.card__title')).fontSize }; })"""
        )
        record = next(c for c in cards if c["cls"] == "card")
        opened = next(c for c in cards if "card--link" in c["cls"] and "card--flat" not in c["cls"])
        entry = next(c for c in cards if "card--flat" in c["cls"])
        action = next(c for c in cards if "card--action" in c["cls"])
        for card in (record, opened):
            assert card["radius"] == "8px" and card["shadow"] == level1 and card["edgeWidth"] == "1px" and card["pad"] == "24px", card
        assert action["radius"] == "8px" and action["shadow"] == level2, "the raised panel: level 2"
        assert action["edge"] in ("rgba(0, 0, 0, 0)", "transparent"), "the plane is its edge"
        assert action["body"] == page.evaluate(COLOUR_JS, "--surface-raised") != record["body"]
        assert record["body"] == page.evaluate(COLOUR_JS, "--surface-sheet")
        assert entry["radius"] == "0px" and entry["shadow"] == "none" and entry["sides"] == "0px" and entry["edgeWidth"] == "1px"
        assert {c["title"] for c in cards} == {"20px"}
        assert level1 != level2 and "rgba(7, 18, 38" in level1 and "rgba(7, 18, 38" in level2, "the night's own colour"

        # contact: the hairline strengthens and the title is underlined; the plane does not change
        link = "#conteneurs .card--link:not(.card--flat)"
        page.hover(link)
        page.wait_for_timeout(300)
        hovered = page.evaluate(
            "(s) => { const c = document.querySelector(s); const cs = getComputedStyle(c);"
            " return { edge: cs.borderTopColor, shadow: cs.boxShadow, line: getComputedStyle(c.querySelector('.card__title a')).textDecorationLine,"
            " target: getComputedStyle(c.querySelector('.card__title a'), '::after').position }; }",
            link,
        )
        assert hovered["edge"] != opened["edge"] and hovered["line"] == "underline"
        assert hovered["shadow"] == level1, "no shadow moves (SH-4)"
        assert hovered["target"] == "absolute", "one destination, one tab stop: the title's link covers the card"
    finally:
        context.close()


def test_a_wrapped_card_keeps_the_cards_flow_and_its_second_action_is_a_24px_target(browser, showcase):
    """The two phases of «Formation» wrap a card's content in one labelled section and put its second action in the
    meta line. The parts keep the card's 12 px, the action stands at the foot of the card — so two cards in a row
    hold it on one line — and it is 24 px tall on its 13/20 line."""
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        card = page.evaluate(
            """() => { const c = document.querySelector('#conteneurs .card[data-sample="wrapped"]'); const s = c.firstElementChild;
                 const box = (e) => e.getBoundingClientRect(); const parts = [...s.children].map(box); const cs = getComputedStyle(c);
                 const link = s.querySelector('.card__meta > a');
                 return { gaps: parts.slice(1).map((p, i) => Math.round((p.top - parts[i].bottom) * 10) / 10),
                          inner: box(c).bottom - parseFloat(cs.paddingBottom) - parseFloat(cs.borderBottomWidth),
                          last: parts[parts.length - 1].bottom, wrapper: box(s).bottom,
                          link: box(link).height, line: getComputedStyle(link.parentElement).lineHeight,
                          size: getComputedStyle(link.parentElement).fontSize, neighbour: box(c.previousElementSibling).height,
                          own: box(c).height }; }"""
        )
        assert card["gaps"][:2] == [12, 12], "eyebrow, title, text: the card's gap, not the wrapper's"
        assert card["gaps"][2] >= 12, "and at least that before the meta line, which takes the free room"
        assert abs(card["wrapper"] - card["inner"]) <= 0.5 and abs(card["last"] - card["inner"]) <= 0.5, "the action at the foot"
        assert card["link"] >= 24 and card["line"] == "20px" and card["size"] == "13px", card
    finally:
        context.close()


def test_an_entry_of_a_list_has_the_same_room_under_as_over(browser, showcase):
    context, page = _open(browser, 390, 844)
    try:
        page.goto(showcase, wait_until="networkidle")
        entry = page.evaluate(
            """() => { const c = document.querySelector('#conteneurs .card--flat'); const cs = getComputedStyle(c);
                 return { top: cs.paddingTop, bottom: cs.paddingBottom, start: cs.paddingInlineStart, end: cs.paddingInlineEnd }; }"""
        )
        assert entry == {"top": "20px", "bottom": "20px", "start": "0px", "end": "0px"}, entry
    finally:
        context.close()


@pytest.mark.parametrize(("width", "height", "rows"), [(1440, 900, 1), (390, 844, 2)])
def test_the_summary_strip_fills_its_rows_and_sets_no_numeral(browser, showcase, width, height, rows):
    context, page = _open(browser, width, height)
    try:
        page.goto(showcase, wait_until="networkidle")
        strip = page.evaluate(
            """() => { const dl = document.querySelector('#conteneurs dl.summary'); const box = dl.getBoundingClientRect();
                 const cells = [...dl.querySelectorAll('.summary__item')].map((c) => { const r = c.getBoundingClientRect();
                   return { top: Math.round(r.top), left: r.left, right: r.right, value: getComputedStyle(c.querySelector('dd')).fontSize }; });
                 return { left: box.left, right: box.right, radius: getComputedStyle(dl).borderTopLeftRadius, cells,
                          scroll: dl.scrollWidth, client: dl.clientWidth, viewport: document.documentElement.clientWidth }; }"""
        )
        tops = sorted({cell["top"] for cell in strip["cells"]})
        assert len(strip["cells"]) == 4 and len(tops) == rows, (tops, strip["cells"])
        for top in tops:
            line = [c for c in strip["cells"] if c["top"] == top]
            assert max(c["right"] for c in line) - min(c["left"] for c in line) >= strip["right"] - strip["left"] - 2.5, "every row is full"
        assert strip["radius"] == "8px" and {c["value"] for c in strip["cells"]} == {"17px"}, "words and figures at text size"
        # the strip's own box: the development showcase scrolls sideways at 390 by its console samples, not by this
        assert strip["scroll"] <= strip["client"] and strip["left"] >= 0 and strip["right"] <= strip["viewport"]
    finally:
        context.close()
