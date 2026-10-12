"""
Design V5 core components, part 2 — the status chip «i cerchi», the tag and the cards by purpose (W1-C;
docs/design-v5/V5_4_EXECUTION_PLAN.md §3.3 item 7, §1.2–§1.4, §1.8, §1.15, §2.3).

The rules the two sheets hold, read from the sources — fast and offline, files on disk only:

* the sheets take their place in main.css in the plan's order, and what they replace has left the cascade (the
  deletion map of §2.3): static/css/v3/chip.css, components.css §3 and §13, the V4 pill of v4/workspace.css, the
  pastille's last comments in register.css;
* the chip: a mark, a word and an edge, painted by the five names v5/tokens.css re-points on `data-register` — the
  sheet names no register and no colour of its own; three exact heights, 20 / 24 / 28 px; it wraps, except in a
  table cell; it is not a control — no hover, no focus, no motion; an unknown value is dotted;
* never colour alone: the eight registers keep their marks apart and the two «open» ones their edge style;
  «conforme» is ink, «esame» is the register's lapis;
* the tag is a term: no register, no mark, and a 44 px target under a coarse pointer when it is a link;
* cards by purpose: the record (level 1), the action card (level 2, the raised panel) and the summary strip; the
  five shadow levels and nothing else, one radius, no shadow that moves; no stat card, nothing to drag;
* no stat-card grid on a person's or a company's screen.

What a browser must show (the exact heights in French and in Arabic, the contrast on paper and on night, the mark
on the reading side, forced colours, the 44 px target) is in tests/frontend/test_browser_chips_w1_c.py. The call
sites are held by test_state_chips_carry_a_register.py, the registry by test_chips_registry.py, O14 by
test_o14_lint.py; literal colours, logical properties and the tokens' existence by test_v5_tokens.py,
tests/i18n/test_rtl_static.py and test_css_tokens_exist.py.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
V5 = CSS / "v5"

pytestmark = pytest.mark.compliance


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _css(name: str) -> str:
    return _strip(_read(V5 / name))


def _rules(css: str) -> list[tuple[str, str]]:
    """Innermost `selector { declarations }` blocks, the rules inside at-rules included."""
    return [(" ".join(s.split()), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if s.strip()]


def _block(css: str, selector: str) -> str:
    for found, body in _rules(css):
        if found == selector:
            return body
    raise AssertionError(f"no rule for {selector!r}")


def _imports() -> list[str]:
    return re.findall(r'@import url\("([^"]+)"\)', _read(CSS / "main.css"))


def _px(value: str) -> float:
    value = value.strip()
    if value.endswith("rem"):
        return float(value[:-3]) * 16
    assert value.endswith("px"), value
    return float(value[:-2])


def _token(name: str) -> str:
    match = re.search(rf"(?<![\w-]){re.escape(name)}\s*:\s*([^;]+);", _css("tokens.css"))
    assert match, name
    return match.group(1).strip()


# ---- the cascade and the deletion map ------------------------------------------------------------------


def test_the_two_sheets_take_their_place_in_the_plans_order():
    imports = _imports()
    family = [f"v5/{name}.css" for name in ("buttons", "field", "chip", "card", "notice", "tabs")]
    positions = [imports.index(name) for name in family]
    assert positions == list(range(positions[0], positions[0] + 6)), "buttons, field, chip, card, notice, tabs (plan §2.3)"
    assert imports.index("v5/base.css") < positions[0]
    assert not [name for name in imports if name.startswith("v3/")], "V3 has left the cascade"
    assert not (CSS / "v3").exists() or not list((CSS / "v3").glob("*.css"))


def test_what_the_chip_and_the_cards_replace_is_gone():
    legacy = _read(CSS / "components.css")
    numbered = set(re.findall(r"^   (\d+)\. ", legacy, flags=re.M))
    assert not {"1", "3", "4", "13", "14", "15"} & numbered, sorted(numbered, key=int)
    own = [selector for selector, _ in _rules(_strip(legacy))]
    for gone in (".card", ".meta-row", ".badge", ".chip", ".state"):
        left = [s for s in own if re.search(re.escape(gone) + r"(?![\w-])", s)]
        assert not left, f"components.css still styles {gone}: {left[:3]}"
    assert "STATE CHIP" not in _read(CSS / "register.css") and "chip.css" not in _read(CSS / "register.css")


def test_the_chip_is_drawn_by_one_sheet():
    """Outside v5/chip.css a sheet may PLACE a chip in its page — a column, a margin, a line that must not break —
    and the filter's legend sizes the mark it borrows. Nothing else paints `.chip`, and the two classes it replaced
    are styled nowhere."""
    placed = {
        "static/css/v4/workspace.css": {".doc-row__state, .doc-row__state .chip", ".seg__dot .chip__g", ".seg__link--empty .chip__g"},
        "apps/documents/static/documents/documents.css": {".doc-register__table td .chip + .t-caption", ".doc-version .entry__title .chip"},
    }
    sheets = [p for p in CSS.rglob("*.css") if not {"dist", "dev"} & set(p.relative_to(CSS).parts)]
    sheets += list((ROOT / "apps").glob("*/static/**/*.css"))
    for path in sheets:
        rel = path.relative_to(ROOT).as_posix()
        if rel in ("static/css/v5/chip.css", "static/css/v5/tokens.css"):
            continue
        for selector, _ in _rules(_strip(_read(path))):
            if re.search(r"\.(?:chip|tag)(?:__[\w-]+|--[\w-]+)?(?![\w-])", selector):
                assert selector in placed.get(rel, set()), f"{rel} styles the chip: {selector}"
            assert not re.search(r"\.(?:state|badge)(?:--[\w-]+)?(?![\w-])", selector), f"{rel}: {selector}"


# ---- the chip -------------------------------------------------------------------------------------------------


def test_the_chip_is_painted_by_the_tokens_of_its_register_and_names_none():
    css = _css("chip.css")
    chip = _block(css, ".chip")
    for declaration in (
        "border: var(--chip-edge-width) var(--chip-edge-style) var(--chip-edge)",
        "border-radius: calc(var(--chip-box, var(--chip-h)) / 2)",
        "inline-size: fit-content",
        "background-color: var(--chip-bg)",
        "color: var(--chip-text)",
    ):
        assert declaration in chip, declaration
    assert "color: var(--chip-mark)" in _block(css, ".chip__g"), "the mark is the register's, never a template's"
    assert not re.search(r"data-register=", css), "no register is named here: v5/tokens.css §4.1 re-points the five names"
    assert "border-style: dotted" in _block(css, ".chip:not([data-register])"), "an unknown value is seen"
    tokens = _css("tokens.css")
    for register in chips.REGISTERS:
        body = _block(tokens, f'[data-register="{register}"]')
        for name in ("--chip-bg", "--chip-edge", "--chip-mark", "--chip-text"):
            assert f"{name}: var(--tone-{register}-" in body, (register, name)
        night = _block(tokens, f':is(.on-inverse, .rail, .tooltip, .site-footer) [data-register="{register}"]')
        assert f"--chip-text: var(--tone-{register}-night-text)" in night, register


def test_never_colour_alone_and_never_a_verdict():
    """The two registers that are «open» keep a broken edge — dashed for a thing due, dotted for one that carries
    nothing — and the six others a solid one; «conforme» is ink, with no chroma to mean approval; «En examen» is the
    register's lapis, and the violet it replaced is not in the sheet (plan §1.2)."""
    tokens = _css("tokens.css")
    styles = {}
    for register in chips.REGISTERS:
        match = re.search(r"--chip-edge-style:\s*(\w+)", _block(tokens, f'[data-register="{register}"]'))
        styles[register] = match.group(1) if match else "solid"
    assert styles == {**dict.fromkeys(chips.REGISTERS, "solid"), "attesa": "dashed", "nullo": "dotted"}, styles
    assert _token("--chip-edge-style") == "solid"
    for part in ("bg", "edge", "mark", "text"):
        assert re.fullmatch(r"var\(--p-(?:inchiostro|carta)-\d+\)", _token(f"--tone-conforme-{part}")), part
    assert _token("--tone-esame-mark") == "var(--p-registro-500)" and _token("--tone-esame-text") == "var(--p-registro-800)"
    assert not re.search(r"--tone-esame-[\w-]+:\s*var\(--p-(?!registro-)", tokens), "esame reads the lapis and nothing else"
    for banned in ("--ok-", "--brand-green", "--cooperation", "--color-success"):
        assert banned not in _css("chip.css") and banned not in _css("card.css"), banned


def test_three_exact_heights_20_24_28():
    """Height = the line + the block padding + the 1 px edge, twice: exact in every script, whatever the type step."""
    css = _css("chip.css")
    assert (_px(_token("--chip-h")), _px(_token("--chip-h-s")), _px(_token("--chip-h-l"))) == (24, 20, 28)
    chip, small, large = _block(css, ".chip"), _block(css, ".chip--s"), _block(css, ".chip--l")
    assert "min-block-size: var(--chip-box, var(--chip-h))" in chip and "box-sizing: border-box" in chip
    assert "line-height: var(--chip-line, 1.25rem)" in chip and "padding-block: var(--chip-pad-block, 1px)" in chip
    edge = _px(_token("--chip-edge-width"))

    def value(body: str, name: str, default: str) -> float:
        match = re.search(rf"{name}:\s*([^;]+);", body)
        return _px(match.group(1) if match else default)

    for body, height in ((chip, 24), (small, 20), (large, 28)):
        line = value(body, "--chip-line", "1.25rem")
        pad = value(body, "--chip-pad-block", "1px")
        assert line + 2 * pad + 2 * edge == height, (height, line, pad, edge)
    assert "--chip-box: var(--chip-h-s)" in small and "--chip-box: var(--chip-h-l)" in large
    assert _px(_token("--chip-mark-size")) == 16 and "--chip-mark-size: 14px" in small
    assert "font-size: var(--u-small)" in chip and "font-size: var(--u-caption)" in small, "the type roles: 14 px in Arabic"


def test_a_long_word_wraps_except_in_a_table_cell():
    css = _css("chip.css")
    chip = _block(css, ".chip")
    assert "white-space: normal" in chip and "max-inline-size: 100%" in chip and "align-items: flex-start" in chip
    assert "overflow" not in chip and "text-overflow" not in css, "never cut"
    cell = _block(css, ":is(td, th) .chip")
    assert "white-space: nowrap" in cell and "max-inline-size: none" in cell, "one line, and the body holds its word"
    assert "margin-block: 2px" in _block(css, ".chip__g"), "the mark stays centred on the first line"


def test_a_status_is_not_a_control():
    css = _css("chip.css")
    for selector, body in _rules(css):
        if not re.search(r"\.chip(?![\w-])|\.chip__|\.chip--", selector):
            continue
        assert not re.search(r":hover|:focus|:active", selector), selector
        assert not re.search(r"(?<![\w-])(?:cursor|transition|animation|outline)\s*:", body), (selector, body)
    assert not re.search(r"(?:^|[\s,])(?:a|button)\.chip", css), "a filter is a control of its own family"
    assert "@keyframes" not in css and "will-change" not in css


def test_the_gauge_is_three_notches_in_the_registers_mark():
    css = _css("chip.css")
    notch = _block(css, ".chip__meter > span")
    assert "border: 1px solid var(--chip-mark)" in notch and "border-radius: var(--radius-full)" in notch
    assert "background-color: var(--chip-mark)" in _block(css, ".chip__meter > .is-on")
    partial = _read(ROOT / "templates" / "components" / "chip.html")
    assert '<span class="chip__meter" aria-hidden="true">' in partial, "decoration: the word names the stage"


def test_the_tag_is_a_term_with_no_register_and_a_44px_target_when_it_is_a_link():
    css = _css("chip.css")
    tag = _block(css, ".tag")
    assert "--chip-" not in tag.replace("var(--chip-h)", "").replace("var(--chip-pad-inline)", ""), "no register paints it"
    assert "border: 1px solid var(--line-structure)" in tag and "min-block-size: var(--chip-h)" in tag
    assert "position: relative" in tag and "text-decoration: none" in tag
    hover = css.split("@media (hover: hover)", 1)[1].split("@media", 1)[0]
    assert "a.tag:hover" in hover, "it answers where a pointer hovers, and only as a link"
    coarse = css.split("@media (pointer: coarse)", 1)[1].split("@media", 1)[0]
    # centred on the padding box: half the box less half the target — 44 px whatever the edge and the height
    assert "a.tag::after" in coarse and "inset: calc(50% - var(--chip-hit) / 2) calc(50% - max(50%, var(--chip-hit) / 2))" in coarse
    assert _px(_token("--chip-hit")) == 44
    assert not [s for s, _ in _rules(css) if ".tag" in s and ("focus" in s or "outline" in s)], "the one ring is the foundation's"


# ---- the cards ----------------------------------------------------------------------------------------------


def test_cards_by_purpose_on_the_five_levels():
    """A record is a sheet (level 1), the action card the raised panel (level 2: one a screen), an entry of a list has
    no plane at all. No other shadow, and none that moves: contact strengthens the hairline (plan §1.4 SH-1, SH-2,
    SH-4, SH-8)."""
    css = _css("card.css")
    assert "box-shadow: var(--card-shadow)" in _block(css, ".card")
    action = _block(css, ".card--action")
    assert "box-shadow: var(--panel-raised-shadow)" in action and "background-color: var(--surface-raised)" in action
    assert "box-shadow: none" in _block(css, ".card--flat")
    assert set(re.findall(r"box-shadow\s*:\s*([^;]+);", css)) == {"var(--card-shadow)", "var(--panel-raised-shadow)", "none"}
    assert _token("--card-shadow") == "var(--shadow-1)" and _token("--panel-raised-shadow") == "var(--shadow-2)"
    assert "gradient(" not in css and "filter" not in css and "backdrop" not in css, "no glow, no glass, no lit edge"
    transitions = re.findall(r"transition\s*:\s*([^;]+);", css)
    assert transitions == ["border-color var(--motion-fast) var(--ease-enter)"], transitions
    hover = css.split("@media (hover: hover)", 1)[1]
    assert "border-color: var(--line-structure)" in _block(hover, ".card--link:hover")
    assert not [s for s, _ in _rules(css.split("@media (hover: hover)", 1)[0]) if ":hover" in s], "hover only where a pointer hovers"
    assert "@keyframes" not in css and "will-change" not in css and "transform" not in css


def test_one_radius_for_the_cards():
    css = _css("card.css")
    radii = set(re.findall(r"border-radius\s*:\s*([^;]+);", css))
    assert radii == {"var(--card-radius)", "0"}, radii
    assert _token("--card-radius") == "var(--radius-lg)" and _token("--radius-lg") == "8px"
    assert "padding: var(--card-pad)" in _block(css, ".card") and _token("--card-pad") == "var(--s-6)"
    phone = css.split("@media (max-width: 47.999rem)", 1)[1].split("}\n}", 1)[0]
    assert ".card {" in phone and "padding: var(--s-4)" in phone, "a phone is recomposed: 16 px (SP-7)"
    assert css.index("@media (max-width: 47.999rem)") < css.index(".card--flat {"), "the entry has no side padding to give up"


def test_an_entry_keeps_its_room_a_second_action_its_target_and_a_wrapped_card_its_flow():
    """Three things the final sweep found on the five pages that draw a card. An entry of a list has the same room
    under its last line as over its first — the related lists keep an 8 px row gap, and the next hairline sat on the
    text. The meta line can hold the card's second action: a link alone there is 24 px, the floor of every target
    (SP-8), on a 13/20 line. And a card whose content is wrapped in one labelled section keeps the card's flow —
    the gap between its parts, the meta line at the foot."""
    css = _css("card.css")
    assert "padding: var(--s-5) 0;" in _block(css, ".card--flat")
    link = _block(css, ".card__meta > :any-link")
    assert "min-block-size: 1.5rem" in link and "display: inline-flex" in link and "align-items: center" in link
    assert "line-height: var(--t-small-lh)" in _block(css, ".card__meta")
    wrapper = _block(css, ".card > :where(section, div):only-child")
    for declaration in ("display: flex", "flex-direction: column", "flex: 1 1 auto", "gap: inherit"):
        assert declaration in wrapper, declaration
    # the children are named: no universal subject after a structural pseudo-class (A11Y P1)
    named = ".card > :where(section, div):only-child > :where(.card__eyebrow, .card__title, .card__text, .card__meta, .notice)"
    assert "margin-block: 0" in _block(css, named)
    for sheet in sorted(V5.glob("*.css")):
        source = re.sub(r"/\*.*?\*/", "", _read(sheet), flags=re.S)
        for selector in re.findall(r"([^{}]+)\{", source):
            assert not re.search(r":(?:only|first|last|nth)-[\w-]+(?:\([^)]*\))?\s*>?\s*\*", selector), (sheet.name, selector)
    assert "margin-block-start: auto" in _block(css, ".card > :where(section, div):only-child > .card__meta")
    # the two cards of «Formation» are written that way, and the showcase draws the case
    training = _read(ROOT / "templates" / "pathways" / "training.html")
    assert training.count('<li class="card training-phase"') == 2 and training.count('<p class="card__meta"><a class="link-arrow"') == 2
    assert 'data-sample="wrapped"' in _read(ROOT / "templates" / "dev" / "showcase.html")


def test_the_three_purposes_and_no_other():
    css = _css("card.css")
    selectors = {s for s, _ in _rules(css)}
    for needed in (".card", ".card--flat", ".card--action", ".card__action", ".summary", ".summary__item", ".summary__item > dd"):
        assert needed in selectors, needed
    modifiers = set(re.findall(r"\.card--([a-z-]+)", css))
    assert modifiers == {"flat", "link", "action"}, modifiers
    # no stat card: nothing in the sheet is set at the numeral's size, and a summary's value is the card title's
    assert "--u-numeral" not in css and "numeral" not in css and "stat" not in css
    assert "font-size: var(--u-card)" in _block(css, ".summary__item > dd")
    sizes = set(re.findall(r"font-size\s*:\s*([^;]+);", css))
    assert sizes <= {"var(--t-small)", "var(--t-entry)", "var(--t-ui)", "var(--u-small)", "var(--u-card)"}, sizes
    # one destination, one tab stop
    assert "inset: 0" in _block(css, ".card--link .card__title a::after")


def test_nothing_is_dragged_resized_or_hidden_by_the_person():
    """Plan §1.15: no card board. The system orders a screen by priority; what is secondary folds with a native
    disclosure. Neither sheet, no script and no template offers to move, resize or hide a card."""
    for name in ("card.css", "chip.css"):
        css = _css(name)
        assert not re.search(r"cursor\s*:\s*(?:grab|grabbing|move|[a-z-]*resize)|(?<![\w-])resize\s*:|user-drag|touch-action", css), name
    scripts = [p for p in (ROOT / "static" / "js").rglob("*.js") if not {"dist", "dev", "vendor"} & set(p.relative_to(ROOT).parts)]
    assert scripts
    for path in scripts:
        source = _read(path)
        for banned in ("dragstart", "draggable", "sortable", "dropzone", "ondrop"):
            assert banned not in source.lower(), f"{path.name}: {banned}"
    for path in (ROOT / "templates").rglob("*.html"):
        assert "draggable=" not in _read(path), path


def test_no_stat_card_grid_on_a_persons_or_a_companys_screen():
    """The person's dashboard and the company's are panels of different rank, not a grid of equal counted boxes. The
    bridge — the accounts that have no workspace yet — no longer draws the six counted cards either: since W3-B's second
    step its registers are flat sections in the dashboard's grammar (templates/portal/partials/card.html), behind the
    branch that keeps them from a person."""
    person = _read(ROOT / "templates" / "portal" / "dashboard.html")
    before_bridge = person[: person.index('<div class="db-main">')]
    assert before_bridge.rfind("{% else %}") > before_bridge.rfind("{% if is_person %}") >= 0, "never for a person"
    company = _read(ROOT / "templates" / "companies" / "dashboard.html")
    bridge = _read(ROOT / "templates" / "portal" / "partials" / "card.html")
    for source in (person, company, bridge):
        body = source.split("{% endcomment %}", 1)[1]
        for banned in ("portal-card", "card--stat", "__figure", "data-count"):
            assert banned not in body, banned
    for path in (ROOT / "templates").rglob("*.html"):
        assert "card--stat" not in _read(path), path


def test_the_metadata_row_came_over_value_for_value():
    css = _css("card.css")
    row = _block(css, ".meta-row")
    assert "gap: var(--s-2) var(--s-6)" in row and "font-size: var(--t-ui)" in row and "color: var(--text-2)" in row
    assert "color: var(--text-3)" in _block(css, ".meta-row__item dt")
    icon = _block(css, ".meta-row .icon")
    assert "inline-size: var(--icon-sm)" in icon and "color: var(--icon-muted)" in icon
