"""
Design V5 core components, part 1 — buttons, fields «la lastra», notices, tabs and the disclosure (W1-C;
docs/design-v5/V5_4_EXECUTION_PLAN.md §3.3 item 7, §1.2, §1.4–§1.6, §1.8, §2.3).

The rules these four sheets hold, read from the sources — fast and offline, files on disk only:

* the sheets follow the foundation in main.css in the plan's order, and the legacy rules they replace are gone
  (the deletion map of §2.3): components.css §1, §4, §14, §15 and §20's field rules, v3/buttons.css and
  v4/buttons.css — its busy face went when the loader family's key took its place;
* buttons: every primary flat (SH-9), ONE press gesture, no dimming, the sizes on the control tokens, 44 px under a
  coarse pointer, and nothing drawn for a busy button;
* fields: a hairline plate with no shadow, 52 px on public pages, an invalid state that is never colour alone, the
  native checkbox / radio / switch drawn from tokens with a 44 px hit area under a coarse pointer;
* notices: the registers of §1.2 — a done thing in ink, never green; a warning's edge dashed, an error's double;
* tabs: one indicator moved with transform alone, the console on --ease-layout and the public pages on
  --spring-snappy; no keyframes, nothing that loops, every duration a token (so reduced motion zeroes them);
* behaviour: initTabs keeps the keyboard model, travels for a pointer only and remembers nothing.

What a browser must show (the focus ring, the travelling indicator in Arabic, the 2 px rule) is in
tests/frontend/test_browser_w1_c.py. Literal colours, logical properties and the tokens' existence are held for every
V5 sheet by test_v5_tokens.py, tests/i18n/test_rtl_static.py and test_css_tokens_exist.py.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
V5 = CSS / "v5"
SHEETS = ("buttons.css", "field.css", "notice.css", "tabs.css")
#: The contexts that are night for a button: the V3 list, kept (v5/buttons.css §5).
NIGHT = ":is(.hero, .chapter--dark, .on-inverse, .forum-cta, .forum-hero, .forum-banner)"

pytestmark = pytest.mark.compliance


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _css(name: str) -> str:
    """A V5 sheet without its comments."""
    return re.sub(r"/\*.*?\*/", "", _read(V5 / name), flags=re.S)


def _rules(css: str) -> list[tuple[str, str]]:
    """Innermost `selector { declarations }` blocks, the rules inside at-rules included."""
    return [(" ".join(s.split()), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if s.strip()]


def _parts(selector: str) -> list[str]:
    """A selector list split on its top-level commas (the commas inside :is(), :not() and :where() stay)."""
    parts, depth, start = [], 0, 0
    for i, char in enumerate(selector):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(selector[start:i].strip())
            start = i + 1
    parts.append(selector[start:].strip())
    return parts


def _block(css: str, selector: str) -> str:
    """The declarations of the FIRST rule whose selector is exactly `selector`."""
    for found, body in _rules(css):
        if found == selector:
            return body
    raise AssertionError(f"no rule for {selector!r}")


def _blocks(css: str, selector: str) -> str:
    """The declarations of every rule that names `selector` in its selector list, joined."""
    bodies = [body for found, body in _rules(css) if selector in _parts(found)]
    assert bodies, f"no rule names {selector!r}"
    return "\n".join(bodies)


def _imports() -> list[str]:
    return re.findall(r'@import url\("([^"]+)"\)', _read(CSS / "main.css"))


def _js_function(name: str) -> str:
    source = _read(ROOT / "static" / "js" / "main.js")
    start = source.index(f"function {name}(")
    end = source.index("\n}\n", start)
    return source[start:end]


# ---- the cascade and the deletion map ------------------------------------------------------------------


def test_the_sheets_follow_the_foundation_in_the_plans_order():
    imports = _imports()
    family = [f"v5/{name}" for name in SHEETS]
    positions = [imports.index(name) for name in family]
    assert positions == sorted(positions), "buttons → field → notice → tabs (plan §2.3)"
    assert positions[0] > imports.index("v5/base.css"), "after the foundation's base roles"
    if "v5/chrome.css" in imports:
        assert positions[-1] < imports.index("v5/chrome.css"), "before the public chrome"
    if "v5/loader.css" in imports:
        # the loader family's sheet (W1-D), once merged: `.btn[aria-busy="true"] { cursor: progress }` meets the
        # slab's disabled cursor at (0,2,0), and the later rule wins
        assert positions[-1] < imports.index("v5/loader.css"), "… tabs, overlays, loader, chrome (plan §2.3)"
    for name in SHEETS:
        assert (V5 / name).exists(), name


def test_the_legacy_rules_these_sheets_replace_are_gone():
    imports = _imports()
    assert "v3/buttons.css" not in imports and not (CSS / "v3" / "buttons.css").exists()
    legacy = re.sub(r"/\*.*?\*/", "", _read(CSS / "components.css"), flags=re.S)
    # a rule that STARTS with one of these blocks is the component's own; a page that places the component
    # (`.account-page .form-field`, the public interior's) is its family's and stays
    own = [part for selector, _ in _rules(legacy) for part in _parts(selector)]
    for gone in (
        ".btn",
        ".link-arrow",
        ".notice",
        ".alert",
        ".messages",
        ".tabs",
        ".accordion",
        ".form-field",
        ".form__",
        ".form-row",
        ".input",
    ):
        left = [part for part in own if re.match(re.escape(gone) + r"(?![a-z0-9])", part)]
        assert not left, f"components.css still styles {gone}: {left[:3]}"
    numbered = re.findall(r"^   (\d+)\. ", _read(CSS / "components.css"), flags=re.M)
    assert not {"1", "4", "14", "15"} & set(numbered), numbered
    # §3 (the badges' pointer) and §13 (the cards) went with part 2 of the family: the chip and the cards
    # (tests/frontend/test_chips_cards_w1_c.py holds that half of the deletion map)
    assert not {"3", "13"} & set(numbered), numbered
    shell = re.sub(r"/\*.*?\*/", "", _read(CSS / "v4" / "shell.css"), flags=re.S)
    assert ".notice" not in shell, "the notice's face is v5/notice.css's"


def test_what_is_left_of_the_v4_buttons_is_the_busy_face_and_nothing_else():
    """The busy face is the loader family's (v5/loader.css, W1-D). Since the two families are on one branch the V4
    meter is gone with its file — the first branch below. The second is the state before that merge, kept so the
    test reads true on an older tree: every rule left in the file is the busy face's."""
    path = CSS / "v4" / "buttons.css"
    if not path.exists():
        # after the loader family's merge the file goes with its import (W1-D's hand-over to this family): the busy
        # face is then v5/loader.css's alone, and a busy button keeps its own variant's surface
        assert "v4/buttons.css" not in _imports() and "v5/loader.css" in _imports()
        return
    v4 = re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)
    for selector, _body in _rules(v4):
        if selector in ("0%, 100%", "50%"):
            continue  # the meter's keyframes
        assert ".is-busy" in selector, f"v4/buttons.css keeps a rule that is not the busy face: {selector}"
    slab = _block(_css("buttons.css"), ".btn")
    for name in ("--btn-fill", "--btn-ink", "--btn-edge"):
        assert re.search(rf"var\({name}[,)]", slab) and re.search(rf"{name}\s*:", v4), name
    # the block paints its own background: the slab reads no V4 lighting, so the file can go and leave nothing
    assert "background-image: var(--grad-primary);" in v4 and "--btn-lighting" not in v4


# ---- buttons -----------------------------------------------------------------------------------------------


def test_every_primary_is_flat_and_no_button_carries_a_shadow():
    css = _css("buttons.css")
    assert "gradient(" not in css, "no gradient: a primary is one colour (SH-9, DL54-13)"
    assert "--shadow-" not in css and "filter" not in css
    shadows = set(re.findall(r"box-shadow\s*:\s*([^;]+);", css))
    assert shadows == {"none"}, shadows
    primary = _block(css, ".btn--primary")
    for token in ("--fill-primary)", "--fill-primary-hover)", "--fill-primary-press)", "--text-on-accent)"):
        assert token in primary, token
    night = _block(css, f"{NIGHT} .btn--primary, .btn--inverse.btn--primary")
    for token in ("--fill-primary-night)", "--fill-primary-night-hover)", "--fill-primary-night-press)"):
        assert token in night, "on night the primary is the paper plate"
    # the slab says so itself — a legacy sheet's gradient cannot show through — and reads no V4 lighting
    assert "background-image: none;" in _block(css, ".btn")
    assert "--btn-lighting" not in css and "background-image" not in css.replace("background-image: none;", "")


def test_one_press_gesture():
    css = _css("buttons.css")
    presses = [(s, b) for s, b in _rules(css) if re.search(r"(?<![\w-])translate\s*:\s*0 var\(--btn-press-shift\)", b)]
    assert len(presses) == 1, [s for s, _ in presses]
    selector, body = presses[0]
    assert selector.endswith(":active") and ".is-busy" in selector and ":disabled" in selector
    assert "transition-duration: 0ms" in body, "the press goes down at 0 ms"
    assert "scale(" not in css and "scale:" not in css, "never a scale"
    slab = _block(css, ".btn")
    assert "translate var(--spring-snappy-duration) var(--btn-release)" in slab, "released on the snappy spring"
    reduced = css.split("@media (prefers-reduced-motion: reduce)", 1)[1].split("@media", 1)[0]
    assert "translate: none" in reduced, "reduced motion: colour changes only"


def test_a_disabled_button_is_never_dimmed_and_a_busy_one_is_not_drawn_here():
    css = _css("buttons.css")
    assert not re.search(r"(?<![\w-])opacity\s*:", css), "disabled by colour and by cursor, never by opacity"
    assert "pointer-events" not in css.replace(".btn--icon::before", ""), "the pointer still reaches a disabled button"
    disabled = _block(css, '.btn:is(:disabled, [aria-disabled="true"], .is-disabled):where(:not(.is-busy))')
    assert "--btn-disabled-fill" in disabled and "--btn-disabled-ink" in disabled and "cursor: not-allowed" in disabled
    for selector, _body in _rules(css):
        for part in _parts(selector):
            if ".is-busy" in part:
                assert re.search(r":not\([^()]*\.is-busy[^()]*\)", part), f"the busy face is not drawn here: {part}"


def test_sizes_are_the_control_tokens_and_reach_44px_under_a_coarse_pointer():
    css = _css("buttons.css")
    tokens = _read(V5 / "tokens.css")
    for name, control in (
        ("--btn-h", "--control-md"),
        ("--btn-h-sm", "--control-sm"),
        ("--btn-h-lg", "--control-lg"),
        ("--btn-h-icon", "--control-icon"),
    ):
        assert re.search(rf"{name}: var\({control}\)", tokens), name
    assert "min-block-size: var(--btn-box-h, var(--btn-h))" in _block(css, ".btn")
    assert "--btn-box-h: var(--btn-h-sm)" in _block(css, ".btn--sm")
    assert "--btn-box-h: var(--btn-h-lg)" in _blocks(css, ".btn--lg")
    coarse = "\n".join(part.split("@media", 1)[0] for part in css.split("@media (pointer: coarse)")[1:])
    assert ".btn--sm" in coarse and ".btn--link" in coarse and "--btn-box-h: var(--hit-primary)" in coarse
    assert "--hit-min" not in css, "the V4 name with two meanings is not read here (v5/aliases.css)"
    assert "calc(50% - var(--hit-primary) / 2)" in _block(css, ".btn--icon::before"), "an icon button is hit in 44 px"
    # the text link with its arrow is hit in 44 px under a finger without a taller line (A11Y A3)
    assert "inset-block: min(0px, calc(50% - var(--hit-primary) / 2))" in coarse and ".link-arrow::after" in coarse
    # a public form's actions stand at 52 px, and on a phone its primary takes the column (review M3)
    public = _block(css, "body:not(.console) :is(.form__actions, .form-actions) > .btn:not(.btn--link, .btn--text, .btn--sm, .btn--icon)")
    assert "--btn-box-h: var(--control-lg)" in public and "--btn-pad: var(--btn-pad-lg)" in public
    assert "inline-size: 100%" in _block(css, "body:not(.console) :is(.form__actions, .form-actions) > .btn--primary")
    # a text action wraps in a panel head (A11Y A1)
    assert "white-space: normal" in _blocks(css, ".btn.btn--link")


def test_a_wrapped_latin_label_stays_centred_on_an_arabic_page():
    """base.css isolates a French, Italian or English span left to right on an Arabic page AND aligns it to its own
    start: a label that wraps on two lines hung on the left of a centred slab (the company form at 390 px)."""
    css = _css("buttons.css")
    assert "text-align: center" in _block(css, ".btn")
    rule = '[dir="rtl"] .btn:not(.btn--link, .btn--text) > :is([lang="fr"], [lang="it"], [lang="en"])'
    assert _block(css, rule).strip() == "text-align: center;", "the label of a slab, never of a link-style button"
    assert "text-align: start" in _blocks(css, ".btn--link"), "a link in the line of text reads from its start"


def test_the_slab_keeps_the_padding_api_the_busy_key_is_centred_in():
    """The loader family's busy key sits in the middle of the slab's inline-end padding and reads the slab's own
    expression (v5/loader.css; tests/frontend/test_loader_rules.py pins it from that side, and reads the padless
    variants off the sheets as the ones that write `--btn-pad: 0`). The arrow's optical margin is that end padding,
    4 px shorter, never a negative margin on the glyph: the key keeps its air beside the arrow."""
    css = _css("buttons.css")
    slab = _block(css, ".btn")
    assert "padding-block: var(--s-1);" in slab
    assert (
        "padding-inline: var(--btn-pad, var(--btn-pad-md)) var(--btn-pad-end, var(--btn-pad, var(--btn-pad-md)));"
        in slab
    )
    assert _block(css, ".btn--arrow").strip() == "--btn-pad-end: calc(var(--btn-pad, var(--btn-pad-md)) - 4px);"
    assert "margin" not in _blocks(css, ".btn--arrow .icon")
    padless = set()
    for selector, body in _rules(css):
        if re.search(r"--btn-pad\s*:\s*0\s*;", body):
            padless.update(re.findall(r"\.btn--[a-z-]+", selector))
    assert padless == {".btn--link", ".btn--text", ".btn--icon"}, padless
    link = _blocks(css, ".btn--link")
    assert "--btn-pad-end: 0;" in link, "after the arrow's rule: a link with an arrow has no padding at either end"
    assert css.index(".btn--arrow {") < css.index(".btn--link,"), "the in-line variants come after the sizes"


def test_hover_answers_only_where_a_pointer_hovers_and_never_on_a_disabled_or_busy_button():
    css = _css("buttons.css")
    hover_rules = [s for s, _ in _rules(css) if ":hover" in s]
    assert hover_rules
    guarded = css.split("@media (hover: hover)")
    in_media = "".join(part.split("\n}\n", 1)[0] for part in guarded[1:])
    slab_hover = '.btn:where(:not(:disabled, [aria-disabled="true"], .is-disabled, .is-busy)):hover'
    assert slab_hover in " ".join(in_media.split()), "the slab's hover sits behind (hover: hover)"
    lean = css.split("@media (hover: hover) and (pointer: fine)", 1)[1].split("\n}\n", 1)[0]
    assert "translate: 3px 0" in lean and '[dir="rtl"] .btn--arrow:hover .icon' in lean, (
        "the arrow leans for a fine pointer, mirrored"
    )


# ---- fields ------------------------------------------------------------------------------------------------


def test_la_lastra_is_a_hairline_plate_with_no_shadow_52px_on_public_pages():
    css = _css("field.css")
    plate = _blocks(css, ".input")
    for declaration in (
        "min-block-size: var(--field-h)",
        "border: 1px solid var(--field-edge)",
        "border-radius: var(--field-radius)",
        "background-color: var(--field-bg)",
        "box-shadow: none",
    ):
        assert declaration in plate, declaration
    assert "--field-h: var(--control-lg)" in _block(css, "body:not(.console)"), (
        "public form fields are 52 px (plan §1.8)"
    )
    assert re.search(r"--field-h: var\(--input-h\)", _read(V5 / "tokens.css")) and "--input-h: 44px" in _read(
        V5 / "tokens.css"
    )
    label = _block(css, ".form-field__label")
    assert (
        "font-size: var(--u-ui)" in label
        and "font-weight: var(--w-control)" in label
        and "margin-block-end: var(--s-2)" in label
    )
    assert "margin-block-end: var(--s-6)" in _block(css, ".form-field"), "24 px between two fields (SP-3)"
    # typed text: the 16 px rule is the foundation's, held against every sheet
    assert "font-size: var(--t-field) !important" in re.sub(r"/\*.*?\*/", "", _read(V5 / "base.css"), flags=re.S)
    assert not re.search(r"font-size\s*:", plate), "the plate does not size typed text: v5/base.css does"


def test_the_plate_stays_light_so_a_component_that_draws_its_own_control_keeps_it():
    """Specificity is the contract: the plate is (0,1,0) and the stray-control base is (0,0,0)."""
    css = _css("field.css")
    selectors = [s for s, _ in _rules(css)]
    base = [s for s in selectors if s.startswith(":where(input:not(")]
    assert base, "the zero-specificity base for a control no component has drawn"
    assert any(s.startswith(".form-field :where(input:not(") and s.endswith(".search-form__input") for s in selectors)
    assert "appearance: none" not in _blocks(css, base[0]), "a stray select keeps its native arrow"


def test_an_invalid_field_is_never_colour_alone():
    css = _css("field.css")
    invalid = next(
        b for s, b in _rules(css) if '[aria-invalid="true"]' in s and ":focus-visible" not in s and "border-color" in b
    )
    assert "border-color: var(--field-edge-invalid)" in invalid
    assert "box-shadow: inset 0 0 0 1px var(--field-edge-invalid)" in invalid, "the edge doubles: 2 px against 1"
    mark = _block(css, ".form-field__errors li::before")
    assert "border: 1.5px solid" in mark and "currentColor" in mark, "a drawn mark beside the words"
    focused = next(b for s, b in _rules(css) if '[aria-invalid="true"]:focus-visible' in s)
    assert "var(--focus-halo)" in focused and "inset" in focused, "focused and invalid keeps both"


def test_the_focus_rule_draws_with_transform_and_not_at_all_from_the_keyboard():
    css = _css("field.css")
    rule = _block(css, ".form-field::after")
    assert "transform: scaleX(0)" in rule and "transform-origin: 0 50%" in rule and "block-size: 2px" in rule
    assert "transform-origin: 100% 50%" in _block(css, '[dir="rtl"] .form-field::after'), (
        "from the reading edge in Arabic too"
    )
    drawn = next(b for s, b in _rules(css) if s.startswith(".form-field:has(") and s.endswith("::after"))
    assert "transform: scaleX(1)" in drawn and "transition: transform var(--field-draw) var(--ease-enter)" in drawn
    assert "--field-draw: var(--motion-standard)" in _block(css, ".form-field")
    assert "--field-draw: 0ms" in _block(css, 'html[data-input="key"] .form-field'), (
        "tier 0: a keyboard focus does not draw"
    )


def test_checkbox_radio_and_switch_are_the_native_controls_drawn_from_tokens():
    css = _css("field.css")
    box = _block(css, ':where(input[type="checkbox"], input[type="radio"])')
    for declaration in (
        "appearance: none",
        "inline-size: 1.5rem",
        "block-size: 1.5rem",
        "border: 1px solid var(--field-edge)",
    ):
        assert declaration in box, declaration
    checked = _block(css, ':where(input[type="checkbox"], input[type="radio"]):checked')
    assert "var(--fill-primary)" in checked
    assert "clip-path: polygon(" in _block(css, ':where(input[type="checkbox"], input[type="radio"])::before'), (
        "the mark is drawn"
    )
    assert "url(" not in css, "no image, no data URI: the marks are drawn from tokens"
    switch_on = ':where(input[type="checkbox"][role="switch"]):checked::before'
    assert "translateX(1.25rem)" in _block(css, switch_on) and "translateX(-1.25rem)" in _block(
        css, f'[dir="rtl"] {switch_on}'
    )
    forced = css.split("@media (forced-colors: active)", 1)[1]
    assert "appearance: auto" in forced, "the system's own controls come back in forced colours"


def test_form_controls_are_hit_in_44px_under_a_coarse_pointer():
    css = _css("field.css")
    coarse = "\n".join(part.split("\n}\n", 1)[0] for part in css.split("@media (pointer: coarse)")[1:])
    # a 24 px box: 22 px inside its 1 px edge, 11 px more on every side
    assert ':where(input[type="checkbox"], input[type="radio"])::after' in coarse and "inset: -11px" in coarse
    # the file control's own button: a small secondary (36 px) for a mouse, 44 px for a finger
    assert "min-block-size: var(--control-sm)" in _block(css, '.form-field input[type="file"]::file-selector-button')
    assert '.form-field input[type="file"]::file-selector-button { min-block-size: var(--hit-primary); }' in coarse
    toggle = _block(css, ".form-field__toggle")
    # the seat is the plate's height less 8 px — 44 public, 36 console — and is hit 4 px further (review M2)
    assert "inline-size: calc(var(--field-h) - 8px)" in toggle and "block-size: calc(var(--field-h) - 8px)" in toggle
    assert "inset: -4px" in _block(css, ".form-field__toggle::after"), "36 + 2 × 4 = 44 in the console"
    row = _block(css, ".form-field__check")
    assert "padding-block: calc((var(--hit-primary) - 1.5rem) / 2)" in row, "a one-line checkbox row is 44 px"
    tokens = _read(V5 / "tokens.css")
    assert "--control-sm: 36px" in tokens and "--hit-primary: 44px" in tokens


def test_a_password_keeps_its_room_for_the_control_on_an_arabic_page():
    css = _css("field.css")
    rtl = [
        (s, b) for s, b in _rules(css) if s.startswith('[dir="rtl"] .form-field .form-field__control--password > input')
    ]
    assert len(rtl) == 1, "one square at the plate's end, at every width (review M2)"
    assert "direction: ltr" in rtl[0][1] and "padding-inline: var(--field-h)" in rtl[0][1] and "text-align: end" in rtl[0][1]
    ltr = _block(css, ".form-field .form-field__control--password > input:not([type=\"checkbox\"], [type=\"radio\"], [type=\"file\"])")
    assert "padding-inline-end: var(--field-h)" in ltr
    # the entrance's sheet no longer draws a field of its own: the login's fields are the system's
    entrance = _read(ROOT / "apps" / "accounts" / "static" / "accounts" / "entrance.css")
    entrance = re.sub(r"/\*.*?\*/", "", entrance, flags=re.S)
    assert not re.search(r"\.form-field[^{]*(input|select|textarea)[^{]*\{", entrance), "entrance.css draws no control"


# ---- notices -----------------------------------------------------------------------------------------------


def test_the_required_mark_never_stands_alone_on_a_line():
    """A label that fills its line sent the asterisk to the next one, alone (the account pages at 1440 px, whose
    own template has the same space). In this family's template a no-break space ties the mark to the label's
    last word; the mark stays out of the accessible name (aria-hidden) and the control carries `required`."""
    template = _read(ROOT / "templates" / "components" / "form_field.html")
    tied = (
        '{% if field.field.required %}&nbsp;<span class="form-field__required" aria-hidden="true">*</span>{% endif %}'
    )
    assert template.count(tied) == 2, "the label above a control and the label beside a checkbox"
    assert '%} <span class="form-field__required"' not in template


def test_notices_speak_the_registers_and_never_by_colour_alone():
    css = _css("notice.css")
    done = _block(css, ".notice--success, .alert--success")
    assert "var(--tone-conforme-bg)" in done and "var(--tone-conforme-mark)" in done, "a done thing is ink (O14)"
    for banned in ("--ok-", "--brand-green", "--cooperation", "--color-success", "--state-done", "green"):
        assert banned not in css, f"no colour ever means «approved»: {banned}"
    assert "border-inline-start-style: dashed" in _block(css, ".notice--warning, .notice--warn, .alert--warning")
    assert "border-inline-start-style: double" in _block(css, ".notice--error, .alert--error")
    base = _block(css, ".notice, .alert")
    assert "border-inline-start: 3px solid var(--notice-rule)" in base and "var(--notice-info-bg)" in base
    assert "var(--notice-pending-bg)" in _block(css, ".notice--pending, .alert--pending"), "«en examen» is lapis"
    institutional = _block(css, ".notice--institutional")
    assert "var(--notice-institutional-rule)" in institutional and "var(--line-rhythm)" in institutional
    assert "box-shadow" not in css, "a sheet with a hairline, no shadow"
    forced = css.split("@media (forced-colors: active)", 1)[1]
    assert "dashed" in forced and "double" in forced, "the edge styles survive forced colours"


# ---- tabs and the disclosure ------------------------------------------------------------------------------


def test_one_indicator_moved_with_transform_alone():
    css = _css("tabs.css")
    indicator = _block(css, ".tabs__list::after")
    assert "transform: translate(var(--tabs-x), var(--tabs-y)) scaleX(var(--tabs-w))" in indicator
    assert "visibility: hidden" in indicator and "pointer-events: none" in indicator
    declared = _block(css, ".tabs")
    for name in ("--tabs-x: 0px", "--tabs-y: 0px", "--tabs-w: 0", "--tabs-dir: 1"):
        assert name in declared, f"{name}: a run-time property is declared with its no-script value"
    public = _block(css, ".tabs.is-travelling .tabs__list::after")
    console = _block(css, "body.console .tabs.is-travelling .tabs__list::after")
    assert public.strip() == "transition: transform var(--spring-snappy-duration) var(--spring-snappy);"
    assert console.strip() == "transition: transform var(--motion-standard) var(--ease-layout);"
    assert "display: none" in _block(css, "html.no-js .tabs__list"), (
        "without script the panels stand one under the other"
    )
    assert "display: block" in _block(css, "html.no-js .tabs .tabs__panel")


def test_the_disclosure_draws_its_own_mark_for_every_producer():
    css = _css("tabs.css")
    mark = _block(css, ".accordion__summary::after")
    assert "border-width: 0 1.5px 1.5px 0" in mark and "rotate(45deg)" in mark
    assert "rotate(-135deg)" in _block(css, ".accordion__item[open] > .accordion__summary::after")
    assert "display: none" in _block(css, ".accordion__summary > .icon"), "the legacy inline glyph gives way to it"
    assert "min-block-size: 3.5rem" in _block(css, ".accordion__summary")
    # the FAQ's markup names the answer `__panel` (G-19): both names are the same box
    assert "max-inline-size: var(--measure-body)" in _block(css, ".accordion__body, .accordion__panel")


@pytest.mark.parametrize("name", SHEETS)
def test_nothing_loops_and_every_duration_is_a_token(name):
    """No keyframes, no animation, nothing infinite; a transition's time is a motion token or 0 ms, so the
    reduced-motion block of v5/tokens.css lands every change at once."""
    css = _css(name)
    assert "@keyframes" not in css and "infinite" not in css and not re.search(r"(?<![\w-])animation\s*:", css)
    for value in re.findall(r"transition(?:-duration)?\s*:\s*([^;]+);", css):
        if value.strip() == "none":
            continue
        literal = re.findall(r"(?<![\w.-])\d*\.?\d+m?s\b", re.sub(r"var\([^()]*\)", "", value))
        assert all(t in ("0ms", "0s") for t in literal), (name, value)
        moved = [part.strip().split()[0] for part in value.split(",")]
        allowed = {"background-color", "border-color", "color", "translate", "transform", "opacity", "0ms"}
        assert set(moved) <= allowed, (name, value)
    assert "will-change" not in css


# ---- behaviour and markup -------------------------------------------------------------------------------------


def test_a_change_asked_from_the_keyboard_is_not_animated():
    """Tier 0 (plan §1.5, R-07): every family writes its rule for `html[data-input="key"]`, the input-modality flag
    of static/js/head.js (W1-D). This family's: the slab, the field's edge, rule, show / hide control and tick, the
    tab's label and the disclosure's mark. The indicator and the panel need none: only a pointer makes them travel."""
    key = 'html[data-input="key"] '
    zero = "transition-duration: 0ms;"
    assert _block(_css("buttons.css"), key + ".btn").strip() == zero

    field = _css("field.css")
    assert _block(field, key + ".form-field").strip() == "--field-draw: 0ms;", "the 2 px rule is there at once"
    rule = [(s, b) for s, b in _rules(field) if s.startswith(key + ":is(")]
    assert len(rule) == 1 and rule[0][1].strip() == zero
    controls, tick = _parts(rule[0][0])
    for name in (
        ".form-field :is(input, select, textarea)",
        ".input",
        ".search-form__input",
        ".form-field__toggle",
        'input[type="checkbox"]',
        'input[type="radio"]',
    ):
        assert name in controls, name
    assert tick == key + ':is(input[type="checkbox"], input[type="radio"])::before'

    tabs = _css("tabs.css")
    assert zero in _blocks(tabs, key + ".tabs__tab") and zero in _blocks(tabs, key + ".accordion__summary::after")
    travelling = [s for s, b in _rules(tabs) if "transition" in b and ("::after" in s or "__panel" in s)]
    assert all(".is-travelling" in s or ".accordion__summary" in s for s in travelling), travelling


def test_init_tabs_keeps_the_keyboard_model_travels_for_a_pointer_only_and_remembers_nothing():
    body = _js_function("initTabs")
    for key in ('"ArrowRight"', '"ArrowLeft"', '"Home"', '"End"'):
        assert key in body, key
    assert "event.altKey || event.ctrlKey || event.metaKey" in body, "Alt + arrow stays the browser's"
    assert 'direction === "rtl"' in body, "the arrows follow the reading direction"
    assert "travel: event.detail > 0" in body, "only a pointer's click travels"
    assert "select((target + tabs.length) % tabs.length, { focus: true })" in body, (
        "automatic activation, focus follows"
    )
    assert "localStorage" not in _read(ROOT / "static" / "js" / "main.js"), "the choice is not remembered (plan §1.15)"
    for name in ("--tabs-x", "--tabs-y", "--tabs-w", "--tabs-dir"):
        assert f'setProperty("{name}"' in body, name
    for banned in (".animate(", "requestAnimationFrame", "setTimeout", "transitionend"):
        assert banned not in body, f"the sheet moves the indicator, not the script: {banned}"
    assert "tab.tabIndex = selected ? 0 : -1" in body and "panels[i].hidden = !selected" in body


def test_init_accordions_opens_the_row_a_link_names():
    body = _js_function("initAccordions")
    assert 'target.matches("details.accordion__item")' in body and "target.open = true" in body
    assert '"hashchange"' in body and '[data-accordion="single"]' in body


def test_the_tabs_markup_is_the_aria_pattern_and_carries_no_memory():
    template = _read(ROOT / "templates" / "components" / "tabs.html")
    for fragment in (
        'role="tablist"',
        'role="tab"',
        'role="tabpanel"',
        "aria-controls=",
        "aria-labelledby=",
        "aria-selected=",
        "data-tabs",
    ):
        assert fragment in template, fragment
    assert "data-tabs-remember" not in template and "remember" not in template.split("{% endcomment %}", 1)[1]


def test_the_password_control_is_a_glyph_with_one_channel_and_the_help_can_hold_a_list():
    """Review M1, M2; A11Y A2, A10: the help is a <div> (Django's password rules are a list), the show / hide
    control is eye / eye-off under a constant name with aria-pressed, the field's errors keep their list."""
    from django import forms
    from django.template.loader import render_to_string
    from django.utils import translation
    from django.utils.safestring import mark_safe

    class DemoForm(forms.Form):
        password = forms.CharField(
            label="Mot de passe", widget=forms.PasswordInput, help_text=mark_safe("<ul><li>12 caractères</li><li>Pas commun</li></ul>")
        )

    form = DemoForm(data={"password": ""})
    assert not form.is_valid()
    with translation.override("fr"):
        html = render_to_string("components/form_field.html", {"field": form["password"]})
    assert '<div class="form-field__help" id="id_password_helptext"><ul><li>' in html
    assert '<div class="form-field__errors" id="id_password_error" role="alert"><ul class="form-field__error-list"><li>' in html
    toggle = re.search(r'<button class="form-field__toggle"[^>]*>(.*?)</button>', html, re.S)
    assert toggle and 'aria-pressed="false"' in toggle.group(0) and 'aria-controls="id_password"' in toggle.group(0)
    assert "data-label-hide" not in html, "one channel: the name does not flip"
    assert '<span class="visually-hidden">Afficher le mot de passe</span>' in toggle.group(1)
    assert "#icon-eye\"" in toggle.group(1) and "#icon-eye-off\"" in toggle.group(1)
    shell = _read(ROOT / "static" / "js" / "src" / "shell.js")
    assert "textContent" not in shell.split("/* 3.", 1)[1].split("/* 4.", 1)[0], "the script swaps the type only"
