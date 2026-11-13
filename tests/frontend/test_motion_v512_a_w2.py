"""
The motion system across the product — V5.12 §5, the Director's DECISIONS §2 M1–M9, M11–M13 and §1 T4 (lane A, wave W2).

Fast, offline (the sources):
* the reading of a public page is a PAGE-ONLY sheet (core/reveal.css from v5/_reveal.css), linked by base.html on the
  public pages and emptied by the console's base; main.css carries none of it and stays under its ceiling;
* every scroll reveal is pure CSS (`animation-timeline: view()`) inside `@supports` and `prefers-reduced-motion:
  no-preference`, never under html.rm; the keyframes that start from opacity 0 act on marks and rules only, never on a
  word (§2 rule 1); the page head's hairline is drawn OVER the rule, which never leaves;
* M5: the journey's light (public and console) on a page's first view in a session only (html.is-seen-passage / html.is-seen-journey, head.js; surface tokens, never a path);
* M6: the disclosure's height (`interpolate-size`, `::details-content`), its open plate, plus / minus drawn;
* M7: the tabs' height morph; M8: the scrim's 4 px blur on its own clocks; M11, M13 in the console's partial;
* M9: the session's notices — two regions, a success in the toast region with its own clock, an error never timed;
  notices.js fetched only by a page that carries one; «Fermer» hidden without script;
* T4: lume/region.js — nothing for 400 ms, then aria-busy and the host's key, the word at 1 s, everything removed on
  arrival; wired to the drawer's reading and the Dépôt's page refresh.

With Django's client: the session's messages land in their regions with their kind's mark.

In Chromium (``-m browser``): the head's hairline draws at load (not under reduced motion); a disclosure opens its
height; a success leaves after 6 s, held while the pointer is on it, a warning stays; the drawer's slow reading shows
its key, its shapes and its word, then nothing; a filing marks the row whose state changed.
"""

from __future__ import annotations

import gzip
import os
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.messages import constants
from django.contrib.messages.storage.session import SessionStorage
from django.http import HttpRequest, HttpResponse
from django.test import Client

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
REVEAL = CSS / "v5" / "_reveal.css"
REVEAL_ENTRY = ROOT / "apps" / "core" / "static" / "core" / "reveal.css"
MOTION_CSS = CSS / "v5" / "motion.css"
TABS_CSS = CSS / "v5" / "tabs.css"
NOTICE_CSS = CSS / "v5" / "notice.css"
OVERLAYS_CSS = CSS / "v5" / "overlays.css"
CONSOLE_MOTION = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_motion.css"
JOURNEY_RAIL = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_journey-rail.css"
HEAD_JS = ROOT / "static" / "js" / "src" / "head" / "head.js"
SHELL_JS = ROOT / "static" / "js" / "src" / "shell.js"
NOTICES_JS = ROOT / "static" / "js" / "src" / "notices.js"
REGION_JS = ROOT / "static" / "js" / "src" / "lume" / "region.js"
DRAWER_JS = ROOT / "static" / "js" / "src" / "piece-drawer.js"
DEPOT_JS = ROOT / "static" / "js" / "src" / "depot.js"
MAIN_JS = ROOT / "static" / "js" / "main.js"
BASE = ROOT / "templates" / "base.html"
BASE_PORTAL = ROOT / "templates" / "portal" / "base_portal.html"
NOTICE_TEMPLATE = ROOT / "templates" / "components" / "session_notice.html"
DRAWER_TEMPLATE = ROOT / "templates" / "documents" / "partials" / "piece_drawer.html"
DIST = ROOT / "static" / "css" / "dist"
JS_DIST = ROOT / "static" / "js" / "dist"


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _gz(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), compresslevel=9))


def _keyframes(css: str, name: str) -> str:
    match = re.search(rf"@keyframes {re.escape(name)} \{{(.*?)\n\}}", css, flags=re.S)
    assert match, name
    return match.group(1)


def _blocks_with(css: str, needle: str) -> list[tuple[str, str]]:
    """(selector, body) of every innermost rule whose body holds `needle`."""
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css) if needle in m.group(2)]


# ---------------------------------------------------------------------------------------------- the page-only sheet


def test_the_reading_is_a_page_only_sheet_linked_on_public_pages_only():
    assert '@import url("../css/v5/_reveal.css");' in _read(REVEAL_ENTRY)
    base = _read(BASE)
    # V5.15 round 1 (DL54-170): the public block also links the desktop's mega panel, with media="(min-width: 64rem)"
    assert "{% block reveal_sheet %}<link rel=\"stylesheet\" href=\"{% static 'css/dist/core/reveal.css' %}\"><link rel=\"stylesheet\" href=\"{% static 'css/dist/core/portico.css' %}\" media=\"(min-width: 64rem)\"><script type=\"module\" src=\"{% static 'js/dist/rise.js' %}\" fetchpriority=\"low\"></script>{% endblock %}" in base
    assert base.index("css/dist/main.css") < base.index("css/dist/core/reveal.css"), "after main.css"
    assert "{% block reveal_sheet %}{% endblock %}" in _read(BASE_PORTAL), "the console's motion is its own partial"
    imports = " ".join(re.findall(r'@import url\("([^"]+)"\)', _css(CSS / "main.css")))
    assert "reveal" not in imports, "main.css carries none of the reading's motion"


@pytest.mark.django_db
def test_a_public_page_links_the_sheet_and_a_console_page_does_not(client, seeded, person_user):
    assert "css/dist/core/reveal.css" in client.get("/fr/faq/").content.decode()
    client.force_login(person_user)
    assert "core/reveal.css" not in client.get("/fr/espace-reserve/").content.decode()


def test_the_budgets_hold():
    # V5.15: the central veil is global brand infrastructure, in the shared sheet — the Director's measured exception
    # (DL54-170, docs/design-v5/QA/v515/a/NOTES.md): 31 414 → 33 600 B gzip at most, no further rise
    # V5.20: ratchet restored by dead-rule removal (v520-css, 30 October 2026: the declarations a later layer of the
    # same context re-declares and the custom properties nothing reads left the token layers; the shim shrank) — 33 530
    # → 32 657 B → 32 105 B (CLOSING, V5.29 09:41 item 2: the headroom under the hard 32 716), the measure; the veil stays in the shared sheet
    assert _gz(DIST / "main.css") <= 32_105, "main.css gzip ≤ 32 105 B (V5.20: ratchet restored by dead-rule removal)"
    assert _gz(DIST / "core" / "reveal.css") <= 6 * 1024, "a page-only sheet ≤ 6 KB gzip"
    # V5.29 («layout & brand refinement» §3, the owner's 6 Nov 2026): the lock-up's key turns once at the brand's reveal
    # and on its hover or focus. The brand steward re-recorded shell.js at 4 866 B for its WAAPI turn; the owner's
    # CLOSING gate (V5.29 09:41 item 1) did not accept it: «restore the test ceiling to 4 700 … never raise the
    # budget». CLOSING moved the turn to the stylesheet (motion.css §6, CSS only) and took the dead shell code out
    # (the layout flag nothing read, the nav's unread class, a spotlight selector no template draws): 4 866 → 4 648 B,
    # under the ceiling restored to 4 700 B
    assert _gz(JS_DIST / "shell.js") <= 4_700, "shell.js gzip ≤ 4 700 B (V5.29 09:41 item 1)"
    assert _gz(JS_DIST / "notices.js") <= 1_536, "the notices' module ≤ 1.5 KB gzip (LANE_A §3, Toast 24297)"


# ---------------------------------------------------------------------------------------------- the scroll reveals


def test_every_scroll_reveal_is_gated_and_nothing_hides_a_word():
    css = _css(REVEAL)
    # each view() timeline sits inside @supports (animation-timeline: view()) and a no-preference block, under :root:not(.rm)
    for selector, body in _blocks_with(css, "animation-timeline: view()"):
        assert ":root:not(.rm)" in selector, selector
        before = css[: css.index(body)]
        assert before.rfind("@supports (animation-timeline: view())") > before.rfind("@keyframes"), selector
        assert "prefers-reduced-motion: no-preference" in before[before.rfind("@supports") :], selector
    # the keyframes that start from opacity 0 are drawn on marks, rings and rules — never on words
    hiding = [name for name in re.findall(r"@keyframes ([\w-]+)", css) if "opacity: 0" in _keyframes(css, name).split("}")[0]]
    # V5.15 §6 (DL54-170, DECISIONS §2 rule 1 amended): `rise-in` may carry words, in two bounded places only — the
    # page head's sequence at load and a section's heading as it enters (at rest whenever already in view)
    # V5.22 (SECTION_SYSTEM_V2 §5.1 DEPTH and LIGHT — an approved owner/product decision; lane S): two keyframes of the
    # motion vocabulary V2 start from opacity 0, and they act on LAYERS only — a plate's pre-painted shadow layer (SH-4: a
    # shadow never animates, its layer's opacity does) and a band's light — asserted below on every rule that runs them
    # (V5.20 strict rule: the set is still exact, each new name is bounded to pseudo-element layers)
    layers = {"sez-layer", "sez-sweep"}
    assert set(hiding) == {"reveal-mark", "reveal-ring", "rise-in", "sez-tone"} | layers, hiding
    for name in layers:
        for selector, _body in _blocks_with(css, f"animation: {name}"):
            assert re.search(r"::(?:after|before)\s*$", selector), (name, selector)
        hiding.remove(name)
    # and the seal's tone (§4.7: «the mark's 12–18 % tone fades in last»): a fill-opacity on the drawing's .sg-t shapes
    for selector, _body in _blocks_with(css, "animation: sez-tone"):
        assert selector.endswith(".sg-t"), selector
    hiding.remove("sez-tone")
    for selector, _body in _blocks_with(css, "animation: rise-in"):
        # V5.15 round 1 (DL54-170): a list's rows rise as the list enters — bounded to the lists the pages draw
        assert re.search(r"page-header|ingresso|data-stagger|\.chapter|data-motion|\.register, \.registro:not\(\.spazi\), \.home-trust__list, \.forum-programme, \.page-links", selector), selector
    hiding.remove("rise-in")
    for name in hiding:
        for selector, _body in _blocks_with(css, f"animation: {name}"):
            assert not re.search(r"__(title|lead|text|label|body)|\bh[1-6]\b|\bp\b", selector), selector


def test_the_head_s_hairline_is_drawn_over_the_rule_which_never_leaves():
    css = _css(REVEAL)
    rest = re.search(r":is\(\.ingresso, \.page-header, \.fronte-wrap\):has\(\+ \.chapter\)::after \{([^}]*)\}", css).group(1)
    assert "opacity: 0;" in rest and "var(--line-structure)" in rest, "at rest the stroke is not drawn at all"
    assert not [sel for sel, body in _blocks_with(css, "border") if ".chapter" in sel], "the chapter's rule is untouched"
    frames = _keyframes(css, "reveal-rule")
    assert "scaleX(0)" in frames and frames.rstrip().endswith("}") and "opacity: 0;" in frames.split("100%")[1]
    assert re.search(r"\[dir=\"rtl\"\] :is\(\.ingresso, \.page-header, \.fronte-wrap\):has\(\+ \.chapter\)::after \{\s*transform-origin: 100% 50%;", css)
    gated = re.search(r"@media \(prefers-reduced-motion: no-preference\) \{\s*:root:not\(\.rm\) :is\(\.ingresso, \.page-header, \.fronte-wrap\)", css)
    assert gated, "the draw is declared under no-preference only, never under html.rm"


def test_the_photograph_s_mask_mirrors_and_black_and_white_is_never_autoplayed_but_by_scroll():
    css = _css(REVEAL)
    assert "--reveal-from: inset(0 100% 0 0);" in css and re.search(r'\[dir="rtl"\] \{\s*--reveal-from: inset\(0 0 0 100%\);', css)
    assert "scale: var(--reveal-zoom);" in _keyframes(css, "reveal-zoom")
    hover = re.search(r"@media \(hover: hover\) and \(pointer: fine\) \{\s*\[data-grade=\"bw\"\]:hover img \{\s*filter: none;", css)
    assert hover and '[data-grade="bw"]:focus-within img' in css
    reduced = re.search(r"@media \(prefers-reduced-motion: reduce\) \{\s*\[data-grade\|=\"bw\"\] img \{\s*filter: none;", css)
    assert reduced, "under reduced motion the photographs are in colour, still"
    assert css.count("reveal-colour") == 2, "only bw-scroll colours by itself"


def test_the_passage_lights_on_the_first_view_only():
    head = _read(HEAD_JS)
    assert 'sessionStorage.getItem("ile.seen")' in head and 'root.classList.add("is-seen-" + token)' in head
    assert head.index('"ile.seen"') < head.index('addEventListener("pagereveal"'), "set before the first paint"
    # v512-a-fix-w2: the key holds fixed surface tokens, never a path (a case file's path carries its reference, and
    # the published technical-storage information says the values hold no identifier)
    seen_block = head[head.index("var SURFACES"):head.index("handed = sessionStorage")]
    assert "pathname" not in seen_block and '"ile.seen", shown.join(" ")' in seen_block
    assert 'passage: ".linea__step--current, .linea__step--done"' in head
    assert 'journey: ".journey:not(.journey--descriptive)"' in head
    assert "SURFACES.hasOwnProperty(token)" in head, "an old value (paths) is dropped on read"
    built = _read(ROOT / "static" / "js" / "head.js")
    assert "ile.seen" in built and "is-seen-" in built and "pathname" not in built.split("ile.seen")[1][:400], (
        "the minified head carries it (npm run build:js)")
    public = _css(REVEAL)
    assert ".is-seen)" not in public and ".is-seen)" not in _css(JOURNEY_RAIL)
    assert ":root:not(.rm):not(.is-seen-passage) .linea__step--current .linea__num::after" in public
    assert "calc(var(--reveal-i, 0) * 120ms)" in public
    console = _css(JOURNEY_RAIL)
    assert ".journey" not in _css(CONSOLE_MOTION), "the journey's light is the journey's page sheet, not the console's"
    assert ":root:not(.rm):not(.is-seen-journey) .journey:not(.journey--descriptive)" in console
    assert "animation-delay: calc(var(--m5-i, 0) * var(--motion-fast));" in console, "120 ms a stretch"
    assert "m5-settle var(--motion-standard) var(--spring-soft)" in console


# ---------------------------------------------------------------------------------------------- M6, M7, M8, M11, M13


def test_the_disclosure_opens_its_height_on_its_open_plate_with_a_drawn_minus():
    motion = _css(MOTION_CSS)
    block = motion.split("@supports selector(::details-content)", 1)[1]
    assert motion.rfind("@media (prefers-reduced-motion: no-preference)", 0, motion.index("@supports selector(::details-content)")) > 0
    assert "interpolate-size: allow-keywords;" in block
    assert "transition: block-size var(--motion-fast) var(--ease-layout), content-visibility var(--motion-fast) allow-discrete;" in block
    assert re.search(r"\.accordion__item\[open\]::details-content \{\s*block-size: auto;\s*transition-duration: var\(--motion-standard\);", block)
    # V5.20 strict rule, cited — SECTION_SYSTEM_V2 §5.3 and §9.9 item 6 (INP within its target, an approved acceptance
    # criterion; lane H's QA_ROUND3 M2, NOTES §12.5: a [data-input] rule ending on ::details-content is not scoped by
    # Blink, and the first key of every page restyled the whole document): «from the keyboard at once» is held by the
    # keyboard's condition on the accordion itself — its height interpolates for a pointer only — and no rule under
    # html[data-input] ends on the pseudo-element (stronger: the browser test of v522-s2 opens and closes it from the
    # keyboard at once, and sees a pointer's still move)
    assert 'html:not([data-input="key"]) .accordion {\n      interpolate-size: allow-keywords;' in block
    assert not re.search(r"data-input[^{}]*::details-content", block), "the keyboard's rule never ends on the pseudo-element"
    tabs = _css(TABS_CSS)
    assert "body:not(.console) .accordion__item[open] { background-color: var(--surface-hover); }" in tabs
    assert "background-size: 100% 1.5px, 1.5px 0;" in tabs, "the upright bar folds away: plus → minus"
    assert "rotate(45deg)" not in tabs, "the chevron gave way to the drawn plus"


def test_the_tabs_morph_their_height_for_a_pointer_only():
    tabs = _css(TABS_CSS)
    assert "block-size var(--motion-standard) var(--ease-layout)" in tabs and "@keyframes" not in tabs
    assert "block-size: var(--tabs-from-h); }" in tabs.split("@starting-style", 1)[1], "from the panel left"
    assert "--tabs-from-h: auto;" in tabs
    assert "if (travel && index !== current && panels[current]) widget.style.setProperty(\"--tabs-from-h\"" in _read(MAIN_JS)


def test_the_scrim_blurs_on_its_own_clocks():
    css = _css(OVERLAYS_CSS)
    rest = re.search(r"\.overlay-scrim \{([^}]*)\}", css).group(1)
    assert "backdrop-filter" not in rest.split("transition")[0], "no blur at rest"
    assert "backdrop-filter var(--overlay-out) var(--overlay-out-ease)" in rest
    shown = re.search(r"\.overlay-scrim\[data-open\] \{([^}]*)\}", css).group(1)
    assert "backdrop-filter: blur(4px);" in shown
    assert css.count("blur(") == 1, "one blur, the scrim's (DECISIONS §2 M8)"
    reduced = css.split("@media (prefers-reduced-motion: reduce) {", 1)[1]
    assert ".overlay-scrim[data-open] { transition: opacity var(--motion-reduced) linear; }" in reduced


def test_the_console_s_rail_plate_and_a_changed_document_state():
    css = _css(CONSOLE_MOTION)
    assert re.search(r"@media \(min-width: 64rem\) \{\s*\.rail__item\[aria-current=\"page\"\] \{\s*view-transition-name: rail-current;", css)
    assert re.search(r"@media \(max-width: 63\.999rem\) \{\s*\.console-bottom__item\[aria-current=\"page\"\] \{\s*view-transition-name: rail-current;", css)
    assert ".vt-lang :is(.rail__item, .console-bottom__item)[aria-current=\"page\"]" in css
    assert ".doc-row[data-changed] .doc-row__state {\n  animation: m11-chip calc(var(--motion-fast) * 2)" in css
    assert "animation: m11-rule calc(var(--motion-standard) * 5) linear calc(var(--motion-fast) * 2) 1 backwards;" in css
    drawer = _read(DRAWER_JS)
    assert 'row.setAttribute("data-changed", "")' in drawer and "before.get(row.dataset.piece) !== row.dataset.state" in drawer


# ---------------------------------------------------------------------------------------------- M9, the notices


def test_the_notices_module_times_a_success_only_and_holds_it():
    js = _read(NOTICES_JS)
    assert "export const AUTO_AFTER = 6000;" in js
    for why in ('hold("pointer")', 'hold("focus")', 'hold("hidden")'):
        assert why in js
    assert 'notice.hasAttribute("data-notice-auto")' in js
    assert ".animate(" not in js and "requestAnimationFrame" not in js, "motion is CSS (motion.css §4)"
    assert 'if (document.querySelector("[data-notices]")) import("./notices.js");' in _read(SHELL_JS)
    template = _read(NOTICE_TEMPLATE)
    assert 'data-notice-close hidden aria-label="{% translate \'Fermer\' %}"' in template, "no control without script"
    assert "{% if message.level_tag == 'error' %} role=\"alert\"{% endif %}" in template
    assert '|concept:"notice"' in template, "the kind's mark from the registry"
    base = _read(BASE)
    assert "{% if message.level_tag == 'success' %}{% include \"components/session_notice.html\" with auto=True %}" in base
    assert "{% if message.level_tag != 'success' %}{% include \"components/session_notice.html\" %}" in base


def test_the_toast_region_is_placed_by_script_only_and_stands_above_the_console_bar():
    css = _css(NOTICE_CSS)
    assert re.search(r"html\.js \.messages--toast \{\s*position: fixed;", css), "without script it is a notice in the flow"
    assert "z-index: var(--z-toast);" in css
    assert "html.js body.console .messages--toast { inset-block-end: calc(var(--bottom-bar-h)" in css
    motion = _css(MOTION_CSS)
    start = motion.split("@starting-style {", 1)[1].split("\n}\n", 1)[0]
    flow = start.split(".messages--toast .alert", 1)[0]
    assert "translate: 0 calc(-1 * var(--reveal-shift));" in flow and "opacity" not in flow, "an in-page notice's words are read at once"
    assert "opacity: 0;" in start.split(".messages--toast .alert", 1)[1], "the toast, an overlay, fades in"
    assert "@keyframes notice" not in motion


def _with_messages(client, items):
    session = client.session
    request = HttpRequest()
    request.session = session
    storage = SessionStorage(request)
    for level, text in items:
        storage.add(level, text)
    storage.update(HttpResponse())
    session.save()


@pytest.mark.django_db
def test_the_session_s_messages_land_in_their_regions(client, seeded, person_user):
    client.force_login(person_user)
    _with_messages(client, [(constants.SUCCESS, "Fait."), (constants.ERROR, "Refusé."), (constants.WARNING, "Attention.")])
    html = client.get("/fr/espace-reserve/").content.decode()
    flow = html.split('class="container messages" role="status" aria-live="polite" data-notices>', 1)[1].split("messages--toast", 1)[0]
    toast = html.split('class="container messages messages--toast" role="status" aria-live="polite" data-notices>', 1)[1].split("</main>", 1)[0]
    assert "Refusé." in flow and "Attention." in flow and "Fait." not in flow
    assert "Fait." in toast and "data-notice-auto" in toast and "data-notice-auto" not in flow
    assert re.search(r'<div class="alert alert--error" role="alert">', flow), "an error is an alert"
    assert "#icon-circle-alert" in flow and "#icon-warning" in flow and "#icon-circle-check" in toast, "each kind's mark"
    assert flow.count("data-notice-close hidden") == 2


# ---------------------------------------------------------------------------------------------- T4, the region


def test_the_region_waits_before_it_says_anything_and_leaves_nothing():
    js = _read(REGION_JS)
    assert "const WAIT = 400;" in js and "const WORD_AFTER = 1000;" in js
    assert 'container.setAttribute("aria-busy", "true");' in js and 'host.classList.add("is-busy");' in js
    end = js.split("const end = () => {", 1)[1].split("};", 1)[0]
    assert 'container.removeAttribute("aria-busy")' in end and 'host.classList.remove("is-busy")' in end and 'status.textContent = ""' in end
    assert ".animate(" not in js and "requestAnimationFrame" not in js
    assert 'export { region } from "./lume/region.js";' in _read(ROOT / "static" / "js" / "src" / "loader.js")
    assert "await region(body, readArticle(url, signal), { host: drawer, status: word })" in _read(DRAWER_JS)
    assert "await region(article, read, { host: submit })" in _read(DEPOT_JS)
    assert 'class="doc-drawer__word" role="status" data-region-word="{% translate \'Chargement…\' %}"' in _read(DRAWER_TEMPLATE)
    console = _css(CONSOLE_MOTION)
    shapes = console.split(".doc-drawer.is-busy .doc-drawer__body:empty::before,", 1)[1].split("@media", 1)[0]
    assert "background: var(--skeleton-bg);" in shapes and "animation" not in shapes, "still shapes: nothing pulses"


# ---------------------------------------------------------------------------------------------- in Chromium


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


def _context(browser, live_server, motion="no-preference", client=None, width=1440):
    context = browser.new_context(viewport={"width": width, "height": 900 if width > 600 else 844}, reduced_motion=motion)
    if client is not None:
        context.add_cookies(
            [{"name": settings.SESSION_COOKIE_NAME, "value": client.cookies[settings.SESSION_COOKIE_NAME].value, "url": live_server.url}]
        )
    return context


@pytest.fixture
def phase3_live(set_flag, monkeypatch):
    """Gate G3 open for the live server without freezegun (test_browser_w1_c's fixture: core.clock.now() patched)."""
    import datetime as dt

    from core import clock, flags

    monkeypatch.setattr(clock, "now", lambda: dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC))
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


HAIRLINE = """() => { const h = document.querySelector(':is(.ingresso, .page-header, .fronte-wrap):has(+ .chapter)');
  const a = getComputedStyle(h, '::after'); return {anim: a.animationName, transform: a.transform, opacity: a.opacity}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("motion", ["no-preference", "reduce"])
def test_the_head_s_hairline_draws_at_load_and_a_question_opens_its_height(
    browser, live_server, seeded, legal_published, phase3_live, motion
):
    """V5.22 (SECTION_SYSTEM_V2 §3.13 Q1 and §3.17 AG-2, lane P2; V5.20 strict rule; QA_ROUND2 M4): the FAQ no longer
    meets its head with a chapter (its body is the L explorer, «l'indice», since the composition remediation) nor
    unfolds its answers as accordion rows (the explorer's tabs, a phone's disclosure buttons — W3-F2's keyboard test
    holds them). The same two invariants, measured where they still stand: the head's hairline on a head that meets
    its first chapter (/fr/orientation/, a page V5.22 does not recompose) draws once at load and stands still under
    reduced motion; the system's disclosure (the promoter's question on /fr/agami/, inside its `.accordion`) opens its
    height on its tinted plate, at once under reduced motion."""
    context = _context(browser, live_server, motion=motion)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/fr/orientation/", wait_until="commit")
        page.wait_for_selector(":is(.ingresso, .page-header, .fronte-wrap) + .chapter", state="attached")
        page.wait_for_timeout(300)
        early = page.evaluate(HAIRLINE)
        page.wait_for_timeout(1500)
        late = page.evaluate(HAIRLINE)
        if motion == "reduce":
            assert early["anim"] == "none" and early["opacity"] == "0", "reduced motion: the rule alone, still"
        else:
            assert early["anim"] == "reveal-rule" and early["opacity"] == "1"
            assert 0 < float(early["transform"].split("(")[1].split(",")[0]) < 1, early
            assert late["opacity"] == "0", "the stroke has settled into the hairline"
        page.goto(f"{live_server.url}/fr/agami/", wait_until="networkidle")
        summary = page.locator(".accordion__summary").first
        closed = page.evaluate("() => document.querySelector('.accordion__item').getBoundingClientRect().height")
        summary.click()
        page.wait_for_timeout(40)
        mid = page.evaluate("() => document.querySelector('.accordion__item').getBoundingClientRect().height")
        page.wait_for_timeout(500)
        final = page.evaluate("() => document.querySelector('.accordion__item').getBoundingClientRect().height")
        assert final > closed
        if motion == "reduce":
            assert mid == final, "reduced motion: open at once"
        else:
            assert closed < mid < final, (closed, mid, final)
        plate = page.evaluate("() => getComputedStyle(document.querySelector('.accordion__item[open]')).backgroundColor")
        assert plate not in ("rgba(0, 0, 0, 0)", "transparent")
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_success_leaves_after_six_seconds_held_by_the_pointer_and_a_warning_stays(browser, live_server, seeded, person_user):
    client = Client()
    client.force_login(person_user)
    _with_messages(client, [(constants.SUCCESS, "Fait."), (constants.WARNING, "Attention.")])
    context = _context(browser, live_server, client=client)
    try:
        page = context.new_page()
        page.clock.install()
        page.goto(f"{live_server.url}/fr/espace-reserve/", wait_until="networkidle")
        page.wait_for_function("() => document.querySelector('.messages--toast .alert[data-notice-wired]')")
        state = page.evaluate(
            """() => { const t = document.querySelector('.messages--toast'); const r = t.querySelector('.alert').getBoundingClientRect();
              return {position: getComputedStyle(t).position, bottom: innerHeight - r.bottom, close: !t.querySelector('[data-notice-close]').hidden}; }"""
        )
        assert state["position"] == "fixed" and state["bottom"] >= 16 and state["close"], state
        page.locator(".messages--toast .alert").hover()
        page.clock.run_for(8000)
        assert page.locator(".messages--toast .alert").count() == 1, "held while the pointer is on it"
        page.mouse.move(2, 2)
        page.clock.run_for(6500)
        assert page.locator(".messages--toast .alert").count() == 0, "gone after its 6 s"
        assert page.locator(".alert--warning").count() == 1, "a warning is never timed away"
        page.locator(".alert--warning [data-notice-close]").click()
        page.clock.run_for(500)
        assert page.locator(".alert--warning").count() == 0
    finally:
        context.close()


try:  # the drawer's register (a file with pieces of every state): its fixture and helpers, W3-C's
    from tests.frontend.test_drawer_browser_w3_c import MINIMAL_PDF, _loaded, _open, register  # noqa: F401
except Exception:  # pragma: no cover - the module moved
    register = None


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_slow_reading_shows_the_drawer_s_key_shapes_and_word_and_a_filing_marks_the_changed_row(browser, live_server, register):
    context, page, errors = _open(browser, live_server, register)
    try:
        page.evaluate("() => { const f = window.fetch; window.fetch = (...a) => new Promise((r) => setTimeout(() => r(f(...a)), 1500)); }")
        page.locator(".doc-row__link").first.click()
        page.wait_for_timeout(200)
        quiet = page.evaluate("() => ({busy: document.querySelector('[data-piece-drawer]').classList.contains('is-busy'), word: document.querySelector('.doc-drawer__word').textContent})")
        assert quiet == {"busy": False, "word": ""}, "nothing in the first 400 ms"
        page.wait_for_timeout(1000)
        waiting = page.evaluate(
            """() => { const d = document.querySelector('[data-piece-drawer]'); const b = d.querySelector('[data-drawer-body]');
              return {busy: d.classList.contains('is-busy'), aria: b.getAttribute('aria-busy'), word: d.querySelector('.doc-drawer__word').textContent,
                shapes: getComputedStyle(b, '::before').content, anim: getComputedStyle(b, '::before').animationName}; }"""
        )
        assert waiting["busy"] and waiting["aria"] == "true" and waiting["word"] == "Chargement…", waiting
        assert waiting["shapes"] == '""' and waiting["anim"] == "none", "still shapes"
        _loaded(page)
        done = page.evaluate("() => ({busy: document.querySelector('[data-piece-drawer]').classList.contains('is-busy'), aria: document.querySelector('[data-drawer-body]').getAttribute('aria-busy'), word: document.querySelector('.doc-drawer__word').textContent})")
        assert done == {"busy": False, "aria": None, "word": ""}, done
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        page.reload(wait_until="networkidle")
        page.locator(".doc-row__act a").first.click()
        _loaded(page)
        page.set_input_files(
            "[data-piece-drawer] [data-depot] input[type=file]",
            {"name": "piece.pdf", "mimeType": "application/pdf", "buffer": MINIMAL_PDF},
        )
        page.click("[data-piece-drawer] [data-depot-submit]")
        page.wait_for_function("() => document.querySelector('.doc-row[data-changed]')", timeout=20000)
        changed = page.evaluate(
            """() => [...document.querySelectorAll('.doc-row[data-changed]')].map((r) => ({state: r.dataset.state,
              chip: getComputedStyle(r.querySelector('.doc-row__state')).animationName, row: getComputedStyle(r).animationName}))"""
        )
        assert len(changed) == 1 and changed[0]["chip"] == "m11-chip" and changed[0]["row"] == "m11-rule", changed
        assert not errors, errors
    finally:
        context.close()


def test_the_console_footer_is_lane_ds_console_foot():
    # v512-a-fix-w2 (review, integration major): the shell's footer is lane D's partial — the promoter, the locked «not
    # an authority» sentence, the published legal pages only — never the inline footer that linked the unpublished
    # terms and disclaimer (V5.12 Q2, V5.14 §13)
    shell = _read(ROOT / "templates" / "portal" / "base_portal.html")
    block = shell.split("{% block site_footer %}", 1)[1].split("{% endblock %}", 1)[0]
    assert block == '{% include "portal/partials/console_foot.html" %}'
    assert "legal:terms" not in shell and "legal:disclaimer" not in shell
