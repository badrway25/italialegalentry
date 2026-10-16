"""
The overlay system's contract, on the sources (design V5, family W2-A; docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14;
the primitive contract docs/design-v5/QA/v54/w2-a/CONTRACT.md) — fast, offline, no browser:

* one sheet every page loads, static/css/v5/overlays.css, in main.css's V5 order (… tabs, overlays, loader, chrome —
  plan §2.3), and components.css §21 (the V2 dialog) gone with it; and its page-only part, static/css/v5/
  _overlay-panels.css (the panels with a head, a native modal's backdrop, the control's own CSS tooltip), out of
  main.css, built as css/dist/core/overlay-panels.css and linked only by the pages that draw it (the owner's V5.8 CSS
  budget: the shared ceilings are hard) — the checks below read the two as the one system they are;
* the anatomy's tokens: a paper sheet with a hairline edge; shadow 3 for a popover, 4 for the modal kinds; the scrim
  --scrim-modal, opacity only, never a blur; corners 4 · 8 · 12, a sheet's top ones and a drawer's free edge's;
  «Fermer» 44 px for every pointer; a menu's rows 44 px under a coarse pointer;
* the motion: transitions both ways (@starting-style in, `allow-discrete` on display and overlay out), no keyframes,
  every time a token or 0 ms, nothing that shapes a panel under [open] / :popover-open (B1); the clocks of §1.14 per
  family; tier 0 from the keyboard, last in the sheet; under reduced motion one --motion-reduced opacity and no
  transform; the drawer's travel through one --dir; the tooltip's wait, its warm group and its bridge;
* the module: the API the contract publishes, the hooks it names, the platform's own mechanisms (showModal, the
  popover API), CSSOM writes only, nothing that waits on a transition;
* the components: each template draws the contract's markup, in French and in Arabic;
* the propagation (step 2): every overlay of a console page is the system's — the drawer, the account popover, the
  row menu, the rail's disclosures and its word —, console.js imports the module and keeps no overlay of its own,
  main.js keeps no dialog and a dropdown fallback that steps aside, and the deletion map's W2-A rows are gone;
* the review's fixes (QA/v54/w2-a/REVIEW.md, A11Y_PERF.md): a menu shown as a phone sheet stands over the one scrim,
  which holds the whole press, and is headed by its name; the trapped panel takes the page out of the accessibility
  tree by aria-hidden — which no rule of the project selects —, brings its focus into its own view, and the layer tip
  follows a scroll; the rarer parts (the grip, Back, the placement without anchor positioning, a dialog's scrolling
  body made a stop, a native modal's backdrop press) live in overlay/extras.js behind a dynamic import, which no
  console page fetches; the account trigger is named by its words and what it opens.

The behaviour in a browser is tests/frontend/test_overlays_browser_w2_a.py (the board) and
tests/frontend/test_overlays_console_browser_w2_a.py (the console's pages); the Arabic geometry is
tests/i18n/test_rtl_browser_overlays.py; the rendered console is tests/frontend/test_overlays_console_w2_a.py.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

import pytest
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.safestring import mark_safe

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
SHEET = CSS / "v5" / "overlays.css"
PANELS = CSS / "v5" / "_overlay-panels.css"
PANELS_ENTRY = ROOT / "apps" / "core" / "static" / "core" / "overlay-panels.css"
PANELS_LINK = "{% static 'css/dist/core/overlay-panels.css' %}"
MODULE = ROOT / "static" / "js" / "src" / "overlay.js"
EXTRAS = ROOT / "static" / "js" / "src" / "overlay" / "extras.js"
CONTRACT = ROOT / "docs" / "design-v5" / "QA" / "v54" / "w2-a" / "CONTRACT.md"
COMPONENTS = ROOT / "templates" / "components"
FAMILIES = ("dialog", "drawer", "popover", "tooltip", "sheet")


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


SHARED_TEXT = _strip_comments(_read(SHEET))
PANELS_TEXT = _strip_comments(_read(PANELS))
#: the system's CSS: what every page loads, then its page-only part (the order of a page that links both)
CSS_TEXT = SHARED_TEXT + "\n" + PANELS_TEXT


def _rules(css: str = CSS_TEXT) -> list[tuple[str, str]]:
    """Innermost `selector { declarations }` blocks, those inside @media / @supports / @starting-style included."""
    return [(" ".join(s.split()), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if s.strip()]


def _block(selector: str, css: str = CSS_TEXT) -> str:
    """The declarations of every rule whose selector list names `selector` exactly, joined."""
    found = [body for sel, body in _rules(css) if selector in [part.strip() for part in _split(sel)]]
    assert found, f"no rule for {selector!r}"
    return "\n".join(found)


def _split(selector: str) -> list[str]:
    parts, depth, start = [], 0, 0
    for i, char in enumerate(selector):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(selector[start:i])
            start = i + 1
    parts.append(selector[start:])
    return parts


def _medias(query: str, css: str = CSS_TEXT) -> list[str]:
    """The bodies of every @media block whose condition is exactly `query` (brace-matched)."""
    bodies = []
    for match in re.finditer(r"@media\s*" + re.escape(query) + r"\s*\{", css):
        depth, i = 1, match.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        bodies.append(css[match.end() : i - 1])
    assert bodies, f"no @media {query}"
    return bodies


def _collected(sheet: Path, target: str) -> Path:
    """The source an @import of `sheet` draws, read in the COLLECTED tree as collectstatic and build_css.mjs read it
    (static/<p> → <p>, apps/<app>/static/<p> → <p>; DS 2026 §2)."""
    roots = [ROOT / "static", *sorted((ROOT / "apps").glob("*/static"))]
    here = next(sheet.relative_to(root).as_posix() for root in roots if sheet.is_relative_to(root))
    collected = posixpath.normpath(posixpath.join(posixpath.dirname(here), target))
    return next(root / collected for root in roots if (root / collected).is_file())


def _media(query: str, css: str = CSS_TEXT) -> str:
    """The bodies of the @media blocks whose condition is exactly `query`, joined."""
    return " ".join(_medias(query, css))


# ---- the cascade ------------------------------------------------------------------------------------------------


def test_the_sheet_is_a_layer_of_main_css_in_the_plans_order():
    imports = re.findall(r'@import url\("([^"]+)"\)', _read(CSS / "main.css"))
    assert "v5/overlays.css" in imports
    at = imports.index("v5/overlays.css")
    assert imports.index("v5/tabs.css") < at < imports.index("v5/loader.css") < imports.index("v5/chrome.css"), (
        "… tabs, overlays, loader, chrome (plan §2.3)"
    )


def test_the_panels_are_page_only_and_linked_by_the_pages_that_draw_them():
    """The owner's V5.8 budget (DL54-94): what no product page draws — the dialog and the alert, the bottom sheet and its
    grip, the head / body / foot of dialog.html, sheet.html and drawer.html, a native modal's ::backdrop, the
    control's own CSS tooltip — is a page-only partial, carried by its own css/dist entry and linked only where it is
    drawn; the shared sheet keeps the panel, the drawer, the popover, the top-layer tip and the scrim."""
    assert PANELS.name.startswith("_"), "a partial: never an entry of its own, never in main.css"
    assert "_overlay-panels.css" not in _read(CSS / "main.css")
    assert re.findall(r'@import url\("([^"]+)"\)', _read(PANELS_ENTRY)) == ["../css/v5/_overlay-panels.css"], (
        "the entry imports the partial as it resolves in the collected tree (DS 2026 §2)"
    )
    assert (CSS / "dist" / "core" / "overlay-panels.css").is_file()
    for absent in (
        ".overlay--dialog",
        ".overlay--sheet",
        ".overlay__head",
        ".overlay__foot",
        ".overlay__grip",
        "::backdrop",
        "@property --tip-warm",
        '[data-tip]:not([data-tip="layer"])::after',
    ):
        assert absent not in SHARED_TEXT, f"{absent}: page-only, never in the shared sheet"
    for present in (".overlay--drawer", ".overlay--popover", ".overlay-scrim", ".tooltip", ".overlay__item"):
        assert present in SHARED_TEXT, f"{present}: product pages draw it — the shared sheet keeps it"
    # who links it: every template that draws a page-only part, and none that does not
    draws = re.compile(
        r"overlay--dialog|overlay--sheet|overlay__head|overlay__grip|data-overlay-modal=\"native\""
        r'|components/(?:dialog|sheet|drawer)\.html|data-tip(?![-=])|data-tip="(?!layer)'
        # the tooltip component without `layer` draws the control's own CSS tip
        r'|\{%\s*include\s+"components/tooltip\.html"(?![^%]*\blayer=True)[^%]*%\}'
    )
    # a partial drawn inside pages (W3-C's preview drawer and filter sheet, templates/documents/partials/) is linked
    # when every template that includes it is — the link stays in the page's head, never in a fragment
    templates = {path.relative_to(ROOT / "templates").as_posix(): path for path in (ROOT / "templates").rglob("*.html")}
    texts = {name: _read(path) for name, path in templates.items()}
    includers: dict[str, set[str]] = {}
    for name, text in texts.items():
        for included in re.findall(r'{%\s*include\s+"([^"]+)"', text):
            includers.setdefault(included, set()).add(name)

    def linked(name: str, seen: frozenset = frozenset()) -> bool:
        if PANELS_LINK in texts[name]:
            return True
        parents = includers.get(name, set()) - seen
        return bool(parents) and all(linked(parent, seen | {name}) for parent in parents)

    linking = set()
    for name, template in templates.items():
        if template.parent == COMPONENTS:
            continue
        text = texts[name]
        if PANELS_LINK in text:
            linking.add(template.relative_to(ROOT).as_posix())
        elif draws.search(text) and not linked(name):
            raise AssertionError(f"{template}: draws a page-only overlay part without linking {PANELS_LINK}")
    # today the board and the showcase; a family that adopts a panel adds its page (CONTRACT §1)
    assert {"templates/dev/designpreview/specimens/overlays.html", "templates/dev/showcase.html"} <= linking, linking
    for template in (CHROME, COMPONENTS / "document_row.html", COMPONENTS / "account_menu.html"):
        assert PANELS_LINK not in _read(template), "a console page fetches none of it"


def test_the_v2_dialog_of_components_css_left_with_its_template():
    """The deletion map (plan §2.3): components.css §21 is W2-A's — the dialog is the overlay system's now."""
    legacy = _read(CSS / "components.css")
    assert "21. Dialog" not in legacy and ".dialog__" not in legacy and "dialog-in" not in legacy
    assert ".dialog[open]" not in legacy, "the reduced-motion block's guard left with the dialog (REVIEW m4)"
    for path in (ROOT / "templates").rglob("*.html"):
        assert 'class="dialog' not in _read(path), f"{path}: the V2 dialog's classes are gone"


# ---- the anatomy ------------------------------------------------------------------------------------------------


def test_one_paper_sheet_one_shadow_per_family_and_the_corners_of_lo_spigolo():
    panel = _block(".overlay")
    assert "background: var(--surface-raised)" in panel and "border: 1px solid var(--line-rhythm)" in panel
    assert "box-shadow: var(--shadow-3)" in _block(".overlay--popover")
    for family in (".overlay--dialog", ".overlay--drawer", ".overlay--sheet"):
        assert "box-shadow: var(--shadow-4)" in _block(family), family
    assert "border-radius: var(--radius-lg)" in _block(".overlay--popover"), "a popover's corners: 8"
    assert "border-radius: var(--radius-xl)" in _block(".overlay--dialog"), "a dialog's: 12"
    sheet = _block(".overlay--sheet")
    assert "border-radius: var(--radius-xl) var(--radius-xl) 0 0" in sheet, "a sheet's top corners only"
    drawer = _block(".overlay--drawer")
    assert (
        "border-start-start-radius: var(--radius-xl)" in drawer
        and "border-end-start-radius: var(--radius-xl)" in drawer
    )
    start = _block('.overlay--drawer[data-overlay-edge="start"]')
    assert "border-start-end-radius: var(--radius-xl)" in start and "border-end-end-radius: var(--radius-xl)" in start
    tip = _block('[data-tip]:not([data-tip="layer"])::after')
    assert "border-radius: var(--radius-sm)" in tip, "a tooltip's: 4"
    # nothing lit, nothing blurred, no colour of its own: tokens only
    assert "backdrop-filter" not in CSS_TEXT and "blur(" not in CSS_TEXT
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(", CSS_TEXT)


def test_the_scrim_is_the_panels_backdrop_opacity_only():
    scrim = _block(".overlay::backdrop")
    assert "background: var(--scrim-modal)" in scrim and "opacity: 0" in scrim
    assert "opacity: calc(1 - var(--overlay-drag))" in _block(".overlay:is([open], :popover-open)::backdrop")
    assert "background: none" in _block(".overlay--popover::backdrop"), "a menu dims nothing"
    for selector, body in _rules():
        if "::backdrop" in selector:
            assert not re.search(r"(?<![\w-])(transform|translate|scale|filter)\s*:", body), selector


def test_fermer_is_44px_for_every_pointer_and_a_menus_rows_44_under_a_coarse_one():
    close = _block(".overlay__close")
    assert "inline-size: var(--hit-primary)" in close and "block-size: var(--hit-primary)" in close
    assert "min-block-size: var(--menu-row-h)" in _block(".overlay__item")
    assert "min-block-size: var(--hit-primary)" in _media("(pointer: coarse)")


def test_the_body_scrolls_on_its_own_and_the_foot_is_pinned():
    body = _block(".overlay__body")
    assert "overflow-y: auto" in body and "overscroll-behavior: contain" in body and "min-block-size: 0" in body
    assert "flex: none" in _block(".overlay__foot") and "flex: none" in _block(".overlay__head")


# ---- the motion ------------------------------------------------------------------------------------------------


def test_transitions_both_ways_never_keyframes_every_time_a_token():
    assert "@keyframes" not in CSS_TEXT and not re.search(r"(?<![\w-])animation\s*:", CSS_TEXT)
    assert "will-change" not in CSS_TEXT and "infinite" not in CSS_TEXT
    base = _block(".overlay")
    assert "display var(--overlay-out) allow-discrete" in base and "overlay var(--overlay-out) allow-discrete" in base
    assert "@starting-style" in CSS_TEXT
    for value in re.findall(r"transition(?:-duration|-delay)?\s*:\s*([^;]+);", CSS_TEXT):
        bare = re.sub(r"var\([^()]*\)", "", value)
        literal = re.findall(r"(?<![\w.-])\d*\.?\d+m?s\b", bare)
        assert all(t in ("0ms", "0s") for t in literal), value


def test_nothing_that_shapes_a_panel_sits_under_open():
    """B1: the open state carries only what moves and its clock; the panel's layout is the base rule's, so its rows
    do not jump while it leaves (EMIL §8.6)."""
    allowed = {"opacity", "translate", "scale", "transition-duration", "transition-timing-function", "transition"}
    for selector, body in _rules():
        if (
            ("[open]" in selector or ":popover-open" in selector)
            and "::backdrop" not in selector
            and "tooltip" not in selector
        ):
            if selector.startswith(".overlay:not("):
                continue  # the closed state: display none
            props = set(re.findall(r"(?:^|;)\s*([a-z-]+)\s*:", body))
            assert props <= allowed, (selector, props - allowed)


def test_the_clocks_of_the_plan_per_family():
    panel = _block(".overlay")
    assert "--overlay-in: var(--motion-standard)" in panel and "--overlay-out: var(--motion-fast)" in panel
    assert "--overlay-in: var(--motion-emphasized)" in _block(".overlay--dialog")
    dialog = PANELS_TEXT.split(".overlay--dialog {", 1)[1].split("}", 1)[0]
    assert "--overlay-out" not in dialog, "out in 120 ms: the panel's own way out, not a copy of it"
    assert "--overlay-closed-scale: 0.96" in _block(".overlay--dialog"), "only a modal scales, from .96 (MS-O6)"
    drawer = _block(".overlay--drawer")
    for token in (
        "--overlay-in: var(--motion-emphasized)",
        "--overlay-out: var(--motion-standard)",
        "--overlay-out-ease: var(--ease-layout)",
        "--overlay-scrim-in: var(--motion-emphasized)",
    ):
        assert token in drawer, token
    assert "--overlay-closed-translate: calc(100% * var(--overlay-edge) * var(--dir)) 0" in drawer, "one --dir"
    sheet = _block(".overlay--sheet")
    for token in (
        "--overlay-in: var(--spring-sheet-duration)",
        "--overlay-in-ease: var(--spring-sheet)",
        "--overlay-out: var(--motion-standard)",
        "--overlay-out-ease: var(--ease-layout)",
        "--overlay-closed-translate: 0 100%",
        "--overlay-bleed: var(--s-12)",
    ):
        assert token in sheet, token
    assert "env(safe-area-inset-bottom" in sheet
    popover = SHARED_TEXT.split(".overlay--popover {", 1)[1].split("}", 1)[0]
    assert "--overlay-in" not in popover and "--overlay-out" not in popover, "in 200, out 120: the panel's own clocks"
    assert "--overlay-closed-translate: 0 calc(-4px * var(--overlay-side))" in popover, "the 4 px drop (MS-O6)"
    assert "--overlay-side: -1" in _block('.overlay--popover[data-overlay-side="above"]'), "away from the trigger"
    assert "--overlay-out-ease: var(--ease-enter)" in _block(".overlay"), "a small surface leaves on the entrance curve"


def test_the_keyboard_is_tier_0_and_has_the_last_word():
    key = 'html[data-input="key"] .overlay'
    assert "transition-duration: 0ms" in _block(key) and "transition-duration: 0ms" in _block(
        ".overlay.overlay[data-instant]"
    )
    assert SHARED_TEXT.rindex(key) > SHARED_TEXT.rindex("prefers-reduced-motion"), "after the reduced-motion block"
    # the page-only part comes after main.css: it says reduced motion and the keyboard again, after its families
    assert PANELS_TEXT.rindex('html[data-input="key"] .overlay::backdrop') > PANELS_TEXT.rindex(
        "prefers-reduced-motion"
    )
    assert PANELS_TEXT.index("prefers-reduced-motion") > PANELS_TEXT.index(".overlay--sheet,"), "after the families"
    assert "--overlay-closed-scale: none" in PANELS_TEXT.split("prefers-reduced-motion", 1)[1], "no .96 at any frame"


def test_reduced_motion_is_one_opacity_and_no_transform():
    body = _media("(prefers-reduced-motion: reduce)")
    assert "--overlay-closed-translate: none" in body and "--overlay-closed-scale: none" in body
    assert body.count("opacity var(--motion-reduced) linear") >= 2
    for value in re.findall(r"transition\s*:\s*([^;]+);", body):
        for part in value.split(","):
            part = part.strip()
            assert part.startswith("opacity ") or re.fullmatch(
                r"(display|overlay) var\(--motion-reduced\) allow-discrete", part
            ), part
    phone = _media("(prefers-reduced-motion: reduce) and (max-width: 40rem)")
    assert "--overlay-closed-translate: none" in phone


def test_the_rtl_variable_is_declared_once_and_mirrors():
    assert re.search(r"\[dir=\"rtl\"\]\s*\{\s*--dir:\s*-1;\s*\}", CSS_TEXT)
    assert re.search(r":root\s*\{\s*--dir:\s*1;\s*\}", CSS_TEXT)
    assert "--overlay-edge: -1" in _block('.overlay--drawer[data-overlay-edge="start"]')
    assert "self-block-end span-self-inline-start" in CSS_TEXT, (
        "a menu aligns on its trigger's inline end, in its own direction"
    )


def test_the_tooltip_mirrors_the_name_waits_warms_bridges_and_leaves_at_once():
    tip = _block('[data-tip]:not([data-tip="layer"])::after')
    assert "content: attr(aria-label)" in tip
    assert "border-block-end: 6px solid transparent" in tip and "background-clip: padding-box" in tip, "the bridge"
    assert "transition: opacity 0ms, visibility 0ms" in tip, "it leaves at 0 ms"
    hover = next(body for body in _medias("(hover: hover) and (pointer: fine)") if ":hover::after" in body)
    assert "var(--tooltip-delay)" in hover and "var(--tip-warm)" in hover and "var(--motion-fast)" in hover
    assert "@property --tip-warm" in CSS_TEXT and "--tip-warm: 1" in CSS_TEXT
    assert "transition: none" in _block('[data-tip]:not([data-tip="layer"]):focus-visible::after'), (
        "instant from the keyboard"
    )
    assert "display: none" in _block('[data-tip][aria-expanded="true"]::after')
    assert "[data-tip]::after" in _media("(max-width: 40rem)"), "none on a phone"


def test_forced_colours_keep_an_edge_and_paper_prints_none():
    forced = _media("(forced-colors: active)")
    assert "border: 1px solid CanvasText" in forced
    assert "display: none !important" in _media("print")


def test_the_traps_scrim_is_drawn_like_a_backdrop_on_the_familys_clocks():
    scrim = _block(".overlay-scrim")
    assert "background: var(--scrim-modal)" in scrim and "opacity: 0" in scrim and "pointer-events: none" in scrim
    assert "z-index: calc(var(--z-modal) - 1)" in scrim
    assert "pointer-events: auto" in _block(".overlay-scrim[data-open]")
    assert "--overlay-in: var(--motion-emphasized)" in _block('.overlay-scrim[data-kind="drawer"]'), "with the panel"
    assert "transition: opacity var(--motion-reduced) linear" in _media("(prefers-reduced-motion: reduce)")
    assert "transition-duration: 0ms" in _block(".overlay-scrim.overlay-scrim[data-instant]")
    # the whole press is the scrim's, pointerdown to click: a menu sheet is light-dismissed on the way up (REVIEW M1)
    assert "pointer-events: auto" in _block(".overlay-scrim[data-held]")


def test_a_menu_shown_as_a_phone_sheet_is_headed_by_its_name_and_stands_over_the_scrim():
    """REVIEW M1: ≤ 40rem a menu sheet draws the one scrim (no trap, no lock) and its name heads its rows — the group's
    aria-label, in the small secondary ink, hidden from assistive technology (the group's name already says it)."""
    assert "display: none" in _block(".overlay__caption"), "anchored, a menu stands beside the trigger that names it"
    phone = _media("(max-width: 40rem)")
    head = '.overlay--popover:not([data-overlay-phone="none"]) .overlay__caption {'
    caption = phone.split(head, 1)[1].split("}", 1)[0]
    for declaration in (
        "display: block",
        "color: var(--text-2)",
        "font-size: var(--u-small)",
        "padding-inline: var(--s-3)",
    ):
        assert declaration in caption, declaration
    named = _render("popover", id="m", body=mark_safe('<ul class="overlay__list"></ul>'), label="Mon compte")
    assert '<p class="overlay__caption" aria-hidden="true">Mon compte</p>' in named
    assert named.index("overlay__caption") < named.index("overlay__body"), "above the rows"
    anchored = _render("popover", id="m", body=mark_safe("<ul></ul>"), label="Mon compte", anchored=True)
    unnamed = _render("popover", id="m", body=mark_safe("<ul></ul>"))
    assert "overlay__caption" not in anchored and "overlay__caption" not in unnamed
    # the module: a popover shown as a sheet is what the scrim stands under, and the scrim holds the press to its click
    assert '(kindOf(panel) === "popover" && asSheet(panel))' in JS
    assert 'scrim.setAttribute("data-held", "")' in JS and 'scrim.addEventListener("click"' in JS
    assert 'if (kindOf(panel) === "popover") close(panel, { reason: "light" });' in JS


def test_no_document_wide_has_is_re_evaluated_by_a_focus_or_an_opening():
    """The INP rule (plan §1.14; NOTES «INP»): `html:has(:focus-visible)` re-styled the whole document on every focus
    change — every press of a link or a button, every overlay's focus move (3 500 elements on the Arabic «Mes documents»
    at CPU × 4). No sheet of main.css's cascade may put a :has() over the whole document that a focus or an [open]
    re-evaluates; the keyboard's own state is head.js's html[data-input]."""
    sheets = [CSS / name for name in re.findall(r'@import url\("([^"]+)"\)', _read(CSS / "main.css"))]
    # and the console's entry (W3-A's html:has(.console-drawer[open]) lived there: ≈ 700 elements at every [open])
    console = ROOT / "apps" / "portal" / "static" / "portal" / "console.css"
    sheets += [_collected(console, name) for name in re.findall(r'@import url\("([^"]+)"\)', _read(console))]
    for path in sheets:
        name = path.name
        css = _strip_comments(_read(path))
        for selector, _body in _rules(css):
            for part in _split(selector):
                part = part.strip()
                if re.match(r"(html|body|:root)\b[^ ]*:has\(", part) and re.search(
                    r":focus|\[open\]|:popover-open|:modal", part
                ):
                    raise AssertionError(f"{name}: {part} — a document-wide :has() on the focus or an opening")
    assert 'html[data-input="key"] { scroll-behavior: auto; }' in _read(CSS / "v5" / "chrome.css")


def test_the_scroll_lock_keeps_the_gutter():
    assert "overflow: hidden" in _block("html[data-overlay-lock]")
    assert "scrollbar-gutter: stable" in _block('html[data-overlay-lock="gutter"]')


# ---- the module -------------------------------------------------------------------------------------------------

JS = _read(MODULE)
EXTRAS_JS = _read(EXTRAS)
#: what the browser may receive of the system: the core and its rarer parts
SYSTEM_JS = JS + EXTRAS_JS


def test_the_module_publishes_the_contracts_api():
    for name in ("open", "close", "toggle", "isOpen", "initOverlays"):
        assert re.search(rf"^export function {name}\(", JS, flags=re.M), name
    contract = _read(CONTRACT)
    for name in ("open(panel", "close(panel", "toggle(panel", "isOpen(panel", "initOverlays(root"):
        assert name in contract, name
    for event in ("overlay:open", "overlay:close"):
        assert event in JS and event in contract, event


def test_every_hook_the_contract_names_is_read_by_the_module_or_the_sheet():
    contract = _read(CONTRACT)
    hooks = set(re.findall(r"`(data-(?:overlay|tip)[a-z-]*)", contract))
    assert {"data-overlay-open", "data-overlay-close", "data-overlay-safe", "data-overlay-grip", "data-tip"} <= hooks
    for hook in hooks:
        assert hook in SYSTEM_JS or f"[{hook}" in CSS_TEXT, (
            f"{hook}: in the contract, read by neither overlay.js nor overlays.css"
        )


def test_the_module_rests_on_the_platform_and_writes_no_style_attribute():
    for native in ("showModal()", "show()", "showPopover(", "hidePopover()", ".close()", '"cancel"', '"beforetoggle"'):
        assert native in JS, native
    # the INP rule (plan §1.14): a modal kind opens with show(), aria-modal and one scrim; showModal() is the opt-in
    assert 'setAttribute("aria-modal", "true")' in JS and 'getAttribute("data-overlay-modal") === "native"' in JS
    assert 'setAttribute("closedby", "closerequest")' in JS, "close requests reach a dialog not opened by showModal()"
    for source in (JS, EXTRAS_JS):  # the core and its rarer parts: CSSOM writes only, which the CSP allows
        assert "innerHTML" not in source and 'setAttribute("style"' not in source and "cssText" not in source
        writes = set(re.findall(r"\.style\.(?:setProperty|removeProperty)\(\"([a-z-]+)\"", source))
        writes |= set(re.findall(r"\.style\.([a-zA-Z]+)\s*=", source))
        assert writes <= {"left", "top", "translate", "anchor-name", "position-anchor", "--overlay-drag", "z-index"}, (
            writes
        )
        assert not re.search(r"transitionend|animationend", source), "nothing waits on a transition"


def test_the_rarer_parts_wait_behind_a_dynamic_import_that_no_console_page_makes():
    """A11Y_PERF M4 (plan §2.6's module budget): the grip, Back, the placement without anchor positioning, a dialog's
    scrolling body made a stop and a native modal's backdrop press are overlay/extras.js's, imported on demand; the core
    asks for them only where a page draws one (or where the engine has no anchor positioning) — never on a console page,
    whose overlays are the drawer, the popovers, the disclosures and the tips."""
    assert 'import("./overlay/extras.js")' in JS and "import(" not in JS.replace('import("./overlay/extras.js")', "")
    assert re.search(r"^export function install\(", EXTRAS_JS, flags=re.M) and not re.search(
        r"^import ", EXTRAS_JS, re.M
    )
    for part in (
        "function wireGrip(",
        "function remember(",
        "function place(",
        "function follow(",
        "function reachable(",
        "function wireBackdrop(",
        '"popstate"',
        "pushState(",
        "setPointerCapture(",
    ):
        assert part in EXTRAS_JS, part
    for gone in ("function wireGrip(", "pushState(", "setPointerCapture(", '"popstate"', "function reachable("):
        assert gone not in JS, f"the core still carries {gone}"
    # where the core asks for them: at idle where a page draws one, at once without anchor positioning
    preload = JS.split("whenIdle(() => {\n    measure(", 1)[1].split("});", 1)[0]
    assert (
        "[data-overlay-history], [data-overlay-grip], [data-overlay-modal='native'], dialog[data-overlay] .overlay__body"
        in preload
    )
    assert "if (!ANCHORED && scope.querySelector(\"[data-overlay='popover']\")) loadExtras();" in JS
    chrome, row = _read(CHROME), _read(COMPONENTS / "document_row.html")
    for markup in (chrome, row, _read(COMPONENTS / "account_menu.html")):
        assert "data-overlay-history" not in markup and "data-overlay-grip" not in markup
        assert 'data-overlay-modal="native"' not in markup
    assert "overlay__body" not in chrome, "the console's drawer is no dialog with a body that could scroll alone"


def test_the_trapped_panel_takes_the_page_out_of_the_tree_and_its_focus_into_its_view():
    """A11Y_PERF M2: while a trapped panel is open the rest of the page is aria-hidden — set once the focus is in,
    taken back before it comes out, never inert — and no rule of the project selects aria-hidden, so nothing is
    re-styled. A11Y_PERF M1: a focus moved by the module stays off the page's scroll and comes into its panel's view.
    A11Y_PERF M3: a scroll re-places the layer tip while its control keeps the focus or the pointer."""
    assert 'element.setAttribute("aria-hidden", "true")' in JS and 'element.removeAttribute("aria-hidden")' in JS
    opening = JS.split("export function open(", 1)[1].split("\n}\n", 1)[0]
    assert opening.index("focus(focusTarget(panel, options.focus));") < opening.index("syncHidden();")
    settling = JS.split("function settle(", 1)[1].split("\n}\n", 1)[0]
    assert settling.index("syncHidden();") < settling.index("focus(target);")
    assert ".inert = true" not in JS.split("function syncHidden(", 1)[1].split("\n}\n", 1)[0]
    sheets = [path for path in (ROOT / "static" / "css").rglob("*.css") if "dist" not in path.parts]
    sheets += list((ROOT / "apps").rglob("static/**/*.css"))
    for path in sheets:
        for selector, _body in _rules(_strip_comments(_read(path))):
            assert "aria-hidden" not in selector, f"{path.name}: {selector} — a rule selects aria-hidden"
    focusing = JS.split("function focus(element) {", 1)[1].split("\n}\n", 1)[0]
    assert "element.focus({ preventScroll: true });" in focusing
    assert 'element.scrollIntoView({ block: "nearest", inline: "nearest" })' in focusing
    assert "isOpen(panel)" in focusing, "only inside an open panel: the page behind never scrolls"
    assert 'if (tipFor.matches(":focus-visible, :hover") && inView(tipFor)) placeTip(tipFor);' in JS


# ---- the components ---------------------------------------------------------------------------------------------


def test_every_family_has_its_component():
    for family in FAMILIES:
        assert (COMPONENTS / f"{family}.html").exists(), family


def _render(name: str, lang: str = "fr", **context) -> str:
    with translation.override(lang):
        return render_to_string(f"components/{name}.html", context)


def test_the_dialog_draws_the_contract_in_french_and_arabic():
    html = _render(
        "dialog", id="d", title="Titre", body=mark_safe("<p>Texte</p>"), actions=mark_safe("<button>OK</button>")
    )
    assert re.search(
        r'<dialog class="overlay overlay--dialog" id="d" data-overlay="dialog" aria-labelledby="d-title">', html
    )
    assert '<h2 class="overlay__title" id="d-title">Titre</h2>' in html
    assert '<a class="overlay__close" href="#main-content" data-overlay-close aria-label="Fermer">' in html
    assert (
        '<div class="overlay__body"><p>Texte</p></div>' in html
        and '<div class="overlay__foot"><button>OK</button></div>' in html
    )
    alert = _render("dialog", id="a", title="T", kind="alert", glyph="trash-2", describedby="a-text", return_id="top")
    assert 'data-overlay="alert" role="alertdialog"' in alert and "overlay--alert" in alert
    assert 'aria-describedby="a-text"' in alert and 'class="overlay__glyph" aria-hidden="true"' in alert
    assert 'href="#top" data-overlay-close' in alert and "overlay__foot" not in alert
    assert 'aria-label="إغلاق"' in _render("dialog", lang="ar", id="d", title="T"), "«Fermer» from the catalogue"


def test_the_drawer_the_sheet_and_the_popover_draw_their_options():
    drawer = _render("drawer", id="n", title="Menu", edge="start")
    assert 'data-overlay="drawer" data-overlay-edge="start" aria-labelledby="n-title"' in drawer
    beside = _render("drawer", id="p", title="P", modal=False, history=True)
    assert 'data-overlay-modal="none" data-overlay-history' in beside and "data-overlay-edge" not in beside
    assert "data-overlay-modal" not in _render("drawer", id="m", title="M"), "modal by default"
    sheet = _render("sheet", id="s", title="Langue")
    assert '<span class="overlay__grip" data-overlay-grip aria-hidden="true"></span>' in sheet
    assert 'class="overlay__close"' in sheet, "the grip is never the only way out (WCAG 2.5.7)"
    popover = _render(
        "popover", id="m", body=mark_safe('<ul class="overlay__list"></ul>'), label="Mon compte", anchored=True
    )
    assert re.search(
        r'<div class="overlay overlay--popover" id="m" data-overlay="popover" popover data-overlay-phone="none" role="group" aria-label="Mon compte">',
        popover,
    )


def test_the_tooltip_is_an_icon_control_named_by_its_tip():
    button = _render("tooltip", label="Rechercher", icon="search")
    assert re.search(
        r'<button class="btn btn--icon btn--ghost" type="button" aria-label="Rechercher" data-tip>', button
    )
    link = _render("tooltip", label="Télécharger", icon="download", href="/x/", layer=True, side="inline-end")
    assert 'href="/x/" aria-label="Télécharger" data-tip="layer" data-tip-side="inline-end"' in link
    trigger = _render("tooltip", label="Menu", icon="ellipsis-vertical", popovertarget="row")
    assert 'popovertarget="row"' in trigger


@pytest.mark.parametrize("family", ["dialog", "drawer", "sheet"])
def test_a_body_and_a_foot_may_come_from_a_template(family):
    """`body_template` / `actions_template`: what a template-side caller needs, since an include wraps nothing."""
    html = _render(
        family,
        id="x",
        title="T",
        body_template="components/glyph.html",
        actions_template="components/glyph.html",
        glyph="",
    )
    assert html.count('class="glyph glyph--md glyph--none"') == 2


# ---- the propagation (step 2): every overlay of a console page is the system's -----------------------------------

CHROME = ROOT / "templates" / "partials" / "portal_chrome.html"
CONSOLE_JS = ROOT / "static" / "js" / "src" / "console.js"
MAIN_JS = ROOT / "static" / "js" / "main.js"
SHELL_CSS = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_shell.css"


def test_the_console_loads_the_system_and_keeps_no_overlay_of_its_own():
    script = _read(CONSOLE_JS)
    assert 'import { close, isOpen } from "./overlay.js";' in script, (
        "console.js imports the overlay system (CONTRACT §6)"
    )
    for own in ("showModal", "rail__tip", "doc-menu", 'createElement("span")', ".animate("):
        assert own not in script, f"console.js draws an overlay of its own: {own}"
    # the rail says which controls have a word and when; the system draws it
    assert 'item.setAttribute("data-tip", "layer");' in script and '"overlay:tip"' in script
    assert 'item.setAttribute("data-tip-beyond", "nav[data-rail]");' in script
    shell = _strip_comments(_read(SHELL_CSS))
    assert ".rail__tip" not in shell and "@keyframes" not in shell and "::backdrop" not in shell
    assert not re.search(r"\.console-drawer\[open\]", shell), "nothing that shapes the drawer sits under [open] (B1)"
    assert "html:has(.console-drawer" not in shell, "the drawer's lock is html[data-overlay-lock]"


def test_the_console_drawer_is_a_modal_drawer_of_the_system_and_menu_its_link_opener():
    chrome = _read(CHROME)
    assert re.search(
        r'<dialog class="console-drawer overlay overlay--drawer" id="console-drawer" data-overlay="drawer" '
        r'data-overlay-edge="start" data-console-drawer',
        chrome,
    ), "from the reading edge (navigation), modal (the default): the system's trap, scrim, Esc and focus"
    assert re.search(
        r'<a class="console-bottom__item console-bottom__menu" id="console-menu" href="#console-drawer" '
        r"data-console-menu data-overlay-open",
        chrome,
    ), "«Menu» is a link: it works without script"
    assert '<a class="console-drawer__close" href="#main-content" data-console-close data-overlay-close>' in chrome
    shape = _strip_comments(_read(SHELL_CSS)).split(".console-drawer.overlay--drawer {", 1)[1].split("}", 1)[0]
    for declaration in (
        "inline-size: min(calc(320px + var(--safe-start)), 88vw);",
        "background-color: var(--rail-bg);",
        "border-start-end-radius: var(--drawer-radius);",
        "box-shadow: var(--shadow-4-dark);",
    ):
        assert declaration in shape, f"the console's drawer keeps its own measures and night: {declaration}"


def test_the_account_menu_is_the_systems_popover_in_the_console_and_in_the_letterhead():
    menu = _read(COMPONENTS / "account_menu.html")
    assert (
        '<button class="account-menu__summary" type="button" popovertarget="{{ panel_id }}" '
        'aria-label="{{ user.get_short_name }} — {{ account_label }}">' in menu
    ), "named by the words it shows, then what it opens (REVIEW m3, WCAG 2.5.3)"
    assert (
        '{% include "components/popover.html" with id=panel_id label=account_label '
        'body_template="components/account_menu.html" %}' in menu
    )
    assert menu.count('class="overlay__item"') == 4 and '<button class="overlay__item" type="submit">' in menu
    # one face: the letterhead's seat and the phone sheet's foot moved onto the popover too (W2-C2), and design V4's
    # <details> face left with v4/shell.css, the file
    assert '<details class="account-menu"' not in menu and "<summary" not in menu
    assert '{% include "components/account_menu.html" with popover=True menu_id="console-account" %}' in _read(CHROME)
    header = _read(ROOT / "templates" / "partials" / "header.html")
    assert '{% include "components/account_menu.html" with popover=True menu_id="account-menu" %}' in header
    assert 'with popover=True menu_id="account-menu-sheet"' in _read(ROOT / "templates" / "partials" / "main_nav.html")
    # the deletion map's rows: components.css §8 left, then v4/shell.css (W2-C2)
    components = _read(CSS / "components.css")
    assert "8. Account menu" not in components and ".account-menu" not in components
    assert not (CSS / "v4" / "shell.css").exists()
    # the trigger's base serves both faces: a button or a summary, the name cut by an ellipsis
    assert "font: inherit" in _block(".account-menu__summary") and "border: 0" in _block(".account-menu__summary")
    assert "text-overflow: ellipsis" in _block(".account-menu__name")


def test_the_register_row_opens_its_piece_in_the_systems_drawer():
    """W2-A drew the row menu on the system's popover; «Mes pièces» V5.2 (W3-C) removed the row menu — the row is the
    link, «Télécharger» and the deposits are the piece's (DOCUMENT_WORKSPACE D2) — and opens the piece in the system's
    drawer, non-modal beside the list (retargeted by W3-C, intent kept: the register's overlay is the system's)."""
    row = _read(COMPONENTS / "document_row.html")
    assert "doc-row__more" not in row and "popovertarget" not in row and "components/popover.html" not in row
    drawer = _read(ROOT / "templates" / "documents" / "partials" / "piece_drawer.html")
    assert 'class="overlay overlay--drawer doc-drawer"' in drawer
    assert 'data-overlay="drawer" data-overlay-modal="none"' in drawer and "data-overlay-close" in drawer
    workspace = _read(CSS / "v4" / "workspace.css")
    assert ".doc-menu" not in workspace, "the deletion map's row: v4/workspace.css's row popover"


def test_main_js_keeps_no_dialog_and_a_dropdown_fallback_that_steps_aside():
    main = _read(MAIN_JS)
    assert "function initDialogs" not in main and "initDialogs()" not in main and "showModal" not in main
    assert "data-dialog" not in main
    # the fallback served the letterhead's <details> account menu until shell.js imported overlay.js (W2-C2, as this
    # family's hand-over asked): every page now loads the system, which owns every disclosure, so it left main.js
    assert "function initDropdowns" not in main and "data-dropdown" not in main
    assert 'details.setAttribute("data-dropdown", "overlay");' in JS
    assert 'const DISCLOSURE = "details[data-dropdown]";' in JS
    # the open disclosure takes the Esc before the panel it stands in (DL54-69)
    esc = JS.split('if (event.key !== "Escape") return;', 1)[1]
    assert esc.index("DISCLOSURE") < esc.index("escapePanel(top)")


def test_no_page_opens_a_dialog_outside_the_system():
    for template in (ROOT / "templates").rglob("*.html"):
        text = _read(template)
        assert "data-dialog-open" not in text and "data-dialog-close" not in text, template
    showcase = _read(ROOT / "templates" / "dev" / "showcase.html")
    assert showcase.count("data-overlay-open>") == 2 and "js/dist/overlay.js" in showcase
    assert "data-dialog-close" not in _read(ROOT / "apps" / "core" / "dev.py")


def test_the_layer_tip_takes_its_words_its_place_and_a_veto_from_the_page():
    assert 'control.getAttribute("data-tip-label") || control.getAttribute("aria-label")' in JS
    assert 'control.getAttribute("data-tip-beyond")' in JS
    assert 'new CustomEvent("overlay:tip", { bubbles: true, cancelable: true })' in JS
    # a control names nothing while the OVERLAY it opens is open — the rail's control (aria-expanded = the rail) does
    assert "panelOpenFor(control)" in JS and 'control.getAttribute("aria-expanded") === "true"' not in JS
