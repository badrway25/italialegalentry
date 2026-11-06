"""
V5.15 lane A — the central loader «Lume», the one-row letterhead, the motion language (DECISIONS §15 lane A).

Fast, offline (the sources) and with Django's client:
* the veil is global brand infrastructure: base.html includes it once on every page — public and console — right after
  the skip link; the picture is aria-hidden with no focusable element, and the page has ONE status line of a wait (the
  veil's), written by the template in the page's language;
* lume.css: never in the way (pointer-events none at every moment, a fixed layer above the overlays), one 700 ms clock
  shared by the two pages (the arrival's delay is -(--lume-t)), the key turns 0 → 360° (it never ends mirrored),
  the sill holds at .85 on a wait (no fake completion), nothing loops; under reduced motion the still — no rotation,
  no scale — and the preview's html.rm zeroes it; never on the hub's chrome, an error page, in forced colours or print;
* threshold.js begins the veil on a pointer's navigation only (never from the keyboard), AFTER its own `quiet()`;
  Esc stops a pending navigation and puts the veil away; head.js hands the click's time to the next page, clamps it to
  the turn (400 ms), skips the View Transition when the veil is the page change, and plays the first page of a session;
* the letterhead is one row: no institutional bar is drawn, the end zone holds the language switch (a popover of the
  four languages, the current one marked), the access, and the primary action; every item is in the bar from 64rem.

In Chromium (``-m browser``): a pointer's navigation whose answer comes late (a 204 after 1.4 s, so the page stays to
be read) draws the veil — visible, the doorway at full opacity, the sill held at .85, «Chargement…» once — and Esc
puts it away; from the keyboard the still appears only after the wait; reduced motion shows the still with no turn;
an arrival continues the clock and the veil is gone by the end of it, never taking a click; the letterhead holds its
items on ONE row at 1024, 1280 and 1440 in French and Arabic, and the sheet takes over below 64rem.
"""

from __future__ import annotations

import gzip
import os
import re
import time
from pathlib import Path

import pytest
from django.test import Client

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
LUME_CSS = ROOT / "static" / "css" / "v5" / "lume.css"
MAIN_CSS = ROOT / "static" / "css" / "main.css"
CHROME_CSS = ROOT / "static" / "css" / "v5" / "chrome.css"
VEIL = ROOT / "templates" / "components" / "lume_veil.html"
BASE = ROOT / "templates" / "base.html"
HEADER = ROOT / "templates" / "partials" / "header.html"
THRESHOLD_JS = ROOT / "static" / "js" / "src" / "lume" / "threshold.js"
HEAD_JS = ROOT / "static" / "js" / "src" / "head" / "head.js"
HEAD_BUILT = ROOT / "static" / "js" / "head.js"
DIST_MAIN = ROOT / "static" / "css" / "dist" / "main.css"


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _strip(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


# ---------------------------------------------------------------------------------------------- the sources


def test_the_veil_is_included_once_by_the_base_template_after_the_skip_link():
    base = _read(BASE)
    assert base.count('{% include "components/lume_veil.html" %}') == 1
    assert base.index("skip-link") < base.index("components/lume_veil.html") < base.index("{% block chrome %}")
    veil = _read(VEIL)
    picture = veil.split('<div class="lume-veil" aria-hidden="true" data-lume-veil>', 1)[1].rsplit("</div>", 1)[0]
    for focusable in ("<a ", "<button", "<input", "tabindex", "href="):
        assert focusable not in picture, f"the veil holds nothing focusable: {focusable}"
    assert '{% include "components/loader.html" with css_class="lume-veil__sig" %}' in veil, "the verbatim mark in layers"
    assert """<p class="lume-veil__word" role="status" data-lume-word="{% translate 'Chargement…' %}"></p>""" in veil
    assert veil.index("lume-veil__word") > veil.index("</div>\n</div>"), "the status line lives outside the hidden picture"
    imports = re.findall(r'@import url\("([^"]+)"\)', _strip(_read(MAIN_CSS)))
    assert imports[-1] == "v5/lume.css", "global brand infrastructure: in the one shared sheet, after motion.css"


def test_the_veil_never_takes_a_click_and_shares_one_clock():
    css = _strip(_read(LUME_CSS))
    veil = re.search(r"\n\.lume-veil \{([^}]*)\}", css).group(1)
    assert "position: fixed;" in veil and "pointer-events: none;" in veil and "visibility: hidden;" in veil
    assert "z-index: calc(var(--z-tooltip) + 10);" in veil
    assert "pointer-events: auto" not in css, "never in the way, at any moment"
    for layer in ("lume-veil", "lume-veil__ground", "lume-veil__stage", "lume-veil__halo::after", "lume-veil__spill", "lume-veil__sill"):
        rule = re.search(r":is\(\.lume-in, \.lume-first\) \." + re.escape(layer) + r" \{([^}]*)\}", css)
        assert rule and "700ms linear calc(-1 * var(--lume-t, 0ms)) both" in rule.group(1), f"{layer}: the arrival continues the clock"
    life = re.search(r"@keyframes lume-veil-life \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "100% { visibility: hidden; }" in life, "the arrival fills to hidden by itself: a page whose script fails is never covered"
    clock = re.search(r"@keyframes lume-key-clock \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "0%, 12.86% { transform: rotateY(0deg)" in clock and "65.71%, 100% { transform: rotateY(360deg)" in clock, (
        "the key turns once on its shaft (90 → 400 ms of the clock) and ends verbatim"
    )
    # review round 1, M-3: a turn the eye reads at 390 — the key lifts and HOLDS forward while it turns (never a pulse),
    # a specular light sweeps its face, its shadow swings with it; the leaving page plays the same keyframes
    forward = re.search(r"@keyframes lume-key-forward \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "17.14% { transform: translateY(-3%) scale(1.45); }" in forward and "57.14% { transform: translateY(-3%) scale(1.45);" in forward
    # review round 2, M-1: compositor-only — the shadow is a pre-drawn layer and the glint a still light, both by
    # opacity alone; no filter, no background-position is animated (they repainted the key on every frame)
    assert "filter" not in clock and "drop-shadow" not in css
    assert ".lume-veil__sig .sig__turn::before {" in css and re.search(r"@keyframes lume-shade \{", css)
    glint = re.search(r"@keyframes lume-glint \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "background-position" not in glint and "mask: var(--lume-key-mask)" in css
    # the leaving page follows the clock to 150 ms, then only crawls; a wait completes the turn and holds it
    assert ".lume-go .lume-veil__sig .sig__turn {\n  animation: lume-key-leave 1000ms linear both;" in css
    leave = re.search(r"@keyframes lume-key-leave \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "15% { transform: rotateY(10deg); }" in leave and "100% { transform: rotateY(40deg); }" in leave
    assert "html:not(.rm).lume-go.is-departing .lume-veil__sig .sig__turn {\n    animation: lume-key-finish 260ms" in css, (
        "under no-preference only: reduced motion keeps the still"
    )
    # pre-warmed once the page is idle: the click's first frame changes opacities only; no full-viewport blur
    assert "html.lume-warm .lume-veil {\n  visibility: visible;" in css
    assert "html.lume-warm .lume-veil__stage {\n  opacity: 0.002;\n  will-change: opacity, transform;" in css
    assert "backdrop-filter: blur" not in css, "the full-viewport blur cost every frame of the turn (review round 2)"
    assert "0 0 96px" not in css and "0 0 48px" not in css, "the halo's glow is pre-drawn, never a blurred shadow"
    assert ":root {\n  --lume-w: min(24rem, 80vw, 52vh);" in css, "the stage's width on the root: the word's calc() can read it"
    # finishing round F1, M-1: the arrival's turn runs up to 120 ms behind the clock (its long first frame lands on the
    # resting key), and not at all from a wait's 480 ms (the key is turned already)
    assert re.search(
        r"\.lume-in \.lume-veil__sig \.sig__turn,\s*\.lume-in \.lume-veil__sig \.sig__turn::before,\s*\.lume-in \.lume-veil__sig \.sig__turn::after \{\s*"
        r"animation-delay: calc\(min\(120ms, 480ms - var\(--lume-t, 0ms\)\) - var\(--lume-t, 0ms\)\);",
        css,
    )
    hold = re.search(r"@keyframes lume-sill-hold \{(.*?)\n\}", css, flags=re.S).group(1)
    assert "scaleX(0.85)" in hold and "scaleX(1)" not in hold, "a wait never pretends to finish"
    assert "infinite" not in css and "alternate" not in css, "nothing loops"


def test_reduced_motion_shows_the_branded_still_and_the_hub_never_the_veil():
    css = _strip(_read(LUME_CSS))
    reduced = css.split("@media (prefers-reduced-motion: reduce) {", 1)[1].split("\nhtml.rm", 1)[0]
    assert re.search(r"\.lume-go \.lume-veil__sig :is\(\.sig__turn, \.sig__key\),\s*:is\(\.lume-in, \.lume-first\) \.lume-veil__sig :is\(\.sig__turn, \.sig__key\),\s*\.lume-veil__sig \.sig__turn::after,\s*\.lume-veil__sig \.sig__turn::before \{\s*animation: none;", reduced), (
        "no rotation, no depth, no glint and no swinging shadow under reduced motion"
    )
    assert "html.rm .lume-veil .sig__turn::before,\nhtml.rm .lume-veil .sig__turn::after {\n  animation: none;" in css
    assert "transform: scaleX(0.85);" in reduced and "opacity: 1;" in reduced, "the sill held and the room lit: a clear loading indication"
    assert "lume-ground-in 80ms linear both" in reduced, "one 80 ms fade"
    assert "html.rm:is(.lume-go, .is-departing, .lume-in, .lume-first) .lume-veil," in css, "the preview's flag: the still"
    assert "!important" not in css.split("@media print", 1)[0], "nothing forced but print's hiding"
    assert re.search(r"\.dp-page \.lume-veil,\s*\.dp-page \.lume-veil__word,\s*\.page-error \.lume-veil \{\s*display: none;", css)
    assert re.search(r"@media \(forced-colors: active\) \{\s*\.lume-veil \{\s*display: none;", css)


def test_the_threshold_begins_the_veil_for_the_pointer_and_esc_stops_it():
    js = _strip(_read(THRESHOLD_JS))
    after = js.split("export function after(event)", 1)[1].split("\n}\n", 1)[0]
    assert after.index("depart();") < after.index('if (root.dataset.input !== "key") go();'), (
        "depart() begins with quiet(): the veil is drawn after it, never put away by it"
    )
    go = js.split("export function go()", 1)[1].split("\n}\n", 1)[0]
    assert 'root.classList.add("lume-go")' in go and "root.dataset.lumeAt = String(at);" in go
    # review round 2, M-1: the last frame PAINTED is counted, for head.js's hand-off — as a phase of the clock
    # (finishing round F1, M-1): at most 150 ms before a wait, TURNED_AT once a wait has begun (this page turned the key)
    assert 'const shown = root.classList.contains("is-departing") ? TURNED_AT : Math.min(150, Date.now() - at);' in go
    assert "root.dataset.lumePainted = String(shown);" in go and "nextFrame().then(painted);" in go
    assert "export const TURNED_AT = 480;" in js
    warm = js.split("export function initThreshold()", 1)[1]
    assert 'root.classList.toggle("lume-warm", !document.hidden);' in warm and "requestIdleCallback(warm" in warm, "the veil pre-warmed once idle"
    assert 'document.addEventListener("visibilitychange"' in warm, "a hidden tab keeps no warm layer (finishing round F1)"
    quiet = js.split("export function quiet()", 1)[1].split("\n}\n", 1)[0]
    assert 'root.classList.remove("is-departing", "lume-go", "lume-pane")' in quiet
    assert 'root.classList.toggle("lume-pane", document.body.classList.contains("console"));' in go, (
        "between two console pages the veil covers the work pane only (review round 1)"
    )
    init = js.split("export function initThreshold()", 1)[1]
    assert 'event.key !== "Escape"' in init and "window.stop();" in init and "quiet();" in init, "Esc always works"
    for forbidden in ("preventDefault", "setTimeout(() => location", "MIN_SHOWN", "minDisplay"):
        assert forbidden not in js, f"{forbidden}: the veil never holds or delays a navigation"


def test_head_js_hands_the_clock_over_and_dissolves_the_held_frame_under_the_veil():
    js = _strip(_read(HEAD_JS))
    # review round 2, M-1: the arrival continues from the last frame the leaving page PAINTED (handed on in
    # `pagehide`); threshold.js hands it on as a phase — ≤ 150 ms before a wait, 480 ms after one (finishing round F1)
    assert 'root.classList.add("lume-in");' in js
    assert 'Math.min(480, age, parts[2] | 0) + "ms"' in js
    assert "age < 15000" in js, "a fresh hand-off only"
    assert 'root.classList.add("lume-first")' in js and 'sessionStorage.setItem("ile.lume1", "1")' in js
    assert "html.lume-first {\n  --lume-t: 460ms;" in _strip(_read(LUME_CSS)), "the first page of a session: the resolve alone"
    swap = js.split('addEventListener("pageswap"', 1)[1].split("});", 1)[0]
    assert "lume-go" not in swap and "transition.skipTransition();" in swap, "under the veil the View Transition is kept"
    reveal = js.split('addEventListener("pagereveal"', 1)[1].split("});", 1)[0]
    assert "lume-in" not in reveal
    motion = _strip(_read(ROOT / "static" / "css" / "v5" / "motion.css"))
    assert "html.lume-in::view-transition-old(root) {\n  animation: lume-out var(--motion-fast) var(--ease-enter) 1 both;" in motion, "a short dissolve of the held frame"
    assert "html.lume-in::view-transition-new(root) {\n  animation: none;" in motion
    assert ":is(.vt-lang, .lume-go, .lume-in) :is(.lock-sig, #varco-door) {\n  view-transition-name: none;" in motion, "no mark travels under the veil"
    hide = js.split('addEventListener("pagehide"', 1)[1].split("});", 1)[0]
    assert '"go"' in hide and 'getAttribute("data-lume-at")' in hide
    assert 'getAttribute("data-lume-painted")' in hide
    assert 'mark + "|" + at + "|" + (shown === null ? Date.now() - at : shown) + pane' in hide, "what was painted, and the console's pane"
    assert "try { sessionStorage.setItem(KEY" in hide, "storage refused: nothing handed on, nothing breaks"
    built = _read(HEAD_BUILT)
    # the Director's measured exception (docs/design-v5/QA/v515/a/NOTES.md): the veil's hand-off must run before the
    # first paint, so it is in the render-blocking script; the ceiling moves from 1 000 to 1 250 B gzip, no further
    assert len(gzip.compress(built.encode("utf-8"), 9)) <= 1250


@pytest.mark.django_db
def test_every_page_has_one_veil_and_one_status_line_of_a_wait(client, seeded, person_user):
    for lang in ("fr", "ar"):
        html = client.get(f"/{lang}/").content.decode()
        assert html.count("data-lume-veil") == 1 and html.count("data-lume-word") == 1, lang
        word = {"fr": "Chargement…", "ar": "جارٍ التحميل…"}[lang]
        assert f'data-lume-word="{word}"' in html
    signed = Client()
    signed.force_login(person_user)
    console = signed.get("/fr/espace-reserve/").content.decode()
    assert console.count("data-lume-veil") == 1 and console.count("data-lume-word") == 1, "the platform has the same loader"


@pytest.mark.django_db
def test_the_letterhead_is_one_row_with_language_access_and_action(client, seeded):
    html = client.get("/fr/").content.decode()
    assert "utility-bar" not in html, "no institutional bar above the letterhead: one row"
    header = html.split('<header class="site-header"', 1)[1].split("</header>", 1)[0]
    end = header.split('<div class="site-header__end', 1)[1]
    assert 'class="lang-switch" type="button" popovertarget="lang-menu"' in end and 'aria-label="Français — Choisir la langue"' in end
    menu = end.split('id="lang-menu"', 1)[1].split("</ul>", 1)[0]
    assert menu.count('class="overlay__item lang-menu__item"') == 4 and menu.count('aria-current="true"') == 1
    for name, code in (("Italiano", "it"), ("Français", "fr"), ("English", "en"), ("العربية", "ar")):
        assert f'hreflang="{code}"' in menu and name in menu
    assert "targa" in end or "targa-seat" in end
    assert "Commencer l’orientation" not in end, "measured: a third control never fits the row (the panel carries it)"
    nav = _read(ROOT / "templates" / "partials" / "main_nav.html")
    assert '{% if item.audience == "person" and orientation_url %}<a class="portico__feature portico__lunetta" href="{{ orientation_url }}">' in nav, (
        "the highlighted destination: the person door's plate, only while the questionnaire is public"
    )
    assert '{% elif item.url %}<a class="portico__feature portico__lunetta" href="{{ item.url }}"' in nav, "the other doors': their space"
    assert "{% if item.photo.menu_only %}" in nav and nav.count("item.photo.srcset") == 2, (
        "V5.15 §2 «Do NOT repeat the same image»: a photograph only from a frame of the menu's own (lane C)"
    )
    css = _strip(_read(CHROME_CSS))
    assert ".utility-bar" not in css
    assert "@media (min-width: 64rem) and (max-width: 79.999rem) {\n  .main-nav[data-portico] .main-nav__item:not(.main-nav__item--door) { display: none; }" not in css, (
        "every item is in the bar from 64rem"
    )
    assert re.search(r"@media \(max-width: 63\.999rem\) \{\s*\.nav-toggle \{ display: inline-flex; \}", css), "«Menu» below 64rem only"


def test_the_shared_sheet_s_measured_exception():
    """The veil is global brand infrastructure (V5.15 §10): main.css carries it. The Director's measured exception
    (docs/design-v5/QA/v515/a/NOTES.md): 31 414 → 33 600 B gzip at most, paid in part by W1's band line, the band's
    word, the arrival's light and the institutional bar, which left. V5.20: ratchet restored by dead-rule removal
    (v520-css, 30 October 2026: the declarations a later layer of the same context re-declares and the custom properties
    nothing reads left the token layers; the shim shrank) — 33 530 → 32 718 B, the measure: the veil
    stays in the shared sheet, under the restored ratchet."""
    assert len(gzip.compress(DIST_MAIN.read_bytes(), 9)) <= 32_718
    # review round 1: the desktop's mega panel left main.css for a sheet a phone never waits for (33 565 → 33 152 B)
    base = _read(BASE)
    assert """<link rel="stylesheet" href="{% static 'css/dist/core/portico.css' %}" media="(min-width: 64rem)">""" in base
    portico = ROOT / "static" / "css" / "dist" / "core" / "portico.css"
    assert len(gzip.compress(portico.read_bytes(), 9)) <= 3_000
    assert "@import url(\"v5/_portico.css\")" not in _read(MAIN_CSS)


# ---------------------------------------------------------------------------------------------- in Chromium

STATE = """() => { const h = document.documentElement; const v = document.querySelector('.lume-veil');
  const w = document.querySelector('.lume-veil__word'); const turn = v.querySelector('.sig__turn');
  return {go: h.classList.contains('lume-go'), departing: h.classList.contains('is-departing'),
    visible: getComputedStyle(v).visibility, pe: getComputedStyle(v).pointerEvents,
    ground: getComputedStyle(v.querySelector('.lume-veil__ground')).opacity, stage: getComputedStyle(v.querySelector('.lume-veil__stage')).opacity,
    turn: getComputedStyle(turn).animationName, sill: getComputedStyle(v.querySelector('.lume-veil__sill')).transform,
    word: w.textContent, words: document.querySelectorAll('[data-lume-word]').length}; }"""


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


GONE = """() => { const v = document.querySelector('.lume-veil');
  const o = (s) => v && getComputedStyle(v).visibility === 'visible' ? +getComputedStyle(document.querySelector(s)).opacity : 0;
  return {go: document.documentElement.classList.contains('lume-go'), ground: o('.lume-veil__ground'), stage: o('.lume-veil__stage')}; }"""


def _context(browser, width=1440, motion="no-preference"):
    context = browser.new_context(viewport={"width": width, "height": 900 if width > 600 else 844}, reduced_motion=motion)
    context.add_init_script("try { sessionStorage.setItem('ile.lume1', '1'); } catch (e) {}")
    return context


def _late_link(page, seconds):
    def answer(route):
        time.sleep(seconds)
        route.fulfill(status=204, body="")

    page.route("**/__lume-late/**", answer)
    page.evaluate(
        """() => { const a = document.createElement('a'); a.href = '/fr/__lume-late/'; a.id = 'lume-late'; a.textContent = 'late';
        a.style.cssText = 'position:fixed;bottom:120px;left:160px;z-index:9999;background:#fff;padding:12px'; document.body.append(a); }"""
    )
    return page.locator("#lume-late")


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(("lang", "width"), [("fr", 1440), ("ar", 390)])
def test_a_pointer_navigation_draws_the_veil_and_esc_puts_it_away(browser, live_server, seeded, lang, width):
    context = _context(browser, width)
    page = context.new_page()
    page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
    _late_link(page, 1.4).click(no_wait_after=True)
    page.wait_for_timeout(200)
    # the sill's draw to its hold is 900 ms from the wait's start; on a loaded machine the read may come first: wait for
    # the hold itself (it must get there and stay — never further, asserted below)
    page.wait_for_function(
        "() => getComputedStyle(document.querySelector('.lume-veil__sill')).transform === 'matrix(0.85, 0, 0, 1, 0, 0)'", timeout=3000
    )
    state = page.evaluate(STATE)
    assert state["go"] and state["departing"] and state["visible"] == "visible" and state["pe"] == "none", state
    assert state["ground"] == "1" and state["stage"] == "1" and state["turn"] == "lume-key-finish", state
    assert state["sill"] == "matrix(0.85, 0, 0, 1, 0, 0)", "the sill held on the wait"
    word = {"fr": "Chargement…", "ar": "جارٍ التحميل…"}[lang]
    assert state["word"] == word and state["words"] == 1, "said once"
    # review round 1: the word stands UNDER the stage and inside the viewport (it rendered at y ≈ 12 px over the
    # letterhead while --lume-w was declared on the veil, of which the word is a sibling)
    page.wait_for_timeout(1100)
    geo = page.evaluate(
        """() => { const s = document.querySelector('.lume-veil__stage').getBoundingClientRect(), w = document.querySelector('.lume-veil__word').getBoundingClientRect();
          return {stage: s.bottom, top: w.top, bottom: w.bottom, vh: innerHeight}; }"""
    )
    assert geo["top"] >= geo["stage"] and geo["bottom"] <= geo["vh"], geo
    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    # put away: no lume-go, and the veil back at rest — hidden, or pre-warmed at an imperceptible opacity (round 2)
    gone = page.evaluate(GONE)
    assert gone["go"] is False and gone["ground"] <= 0.01 and gone["stage"] <= 0.01, gone
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_keyboard_and_reduced_motion_see_the_still(browser, live_server, seeded):
    context = _context(browser, motion="reduce")
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    _late_link(page, 1.4).click(no_wait_after=True)
    page.wait_for_timeout(200)
    state = page.evaluate(STATE)
    assert state["go"] and state["visible"] == "visible" and state["turn"] == "none", "the still: no rotation"
    assert state["sill"] == "matrix(0.85, 0, 0, 1, 0, 0)"
    context.close()
    context = _context(browser)
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    link = _late_link(page, 1.4)
    link.focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(200)
    state = page.evaluate(STATE)
    assert not state["go"] and state["departing"] and state["visible"] == "visible", "the keyboard: no veil before the wait, the still after"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_an_arrival_continues_the_clock_and_never_covers_the_page_after_it(browser, live_server, seeded):
    context = _context(browser)
    # the arriving page's first frame, read in its first animation frame
    context.add_init_script(
        """requestAnimationFrame(() => { const g = document.querySelector('.lume-veil__ground');
          window.__first = g ? +getComputedStyle(g).opacity : -1; });"""
    )
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    # a click 400 ms ago whose page painted its last frame of the veil 40 ms after the click (a fast server's paint hold)
    page.evaluate("sessionStorage.setItem('ile.lume', 'go|' + (Date.now() - 400) + '|40')")
    page.goto(f"{live_server.url}/fr/faq/", wait_until="commit")
    page.wait_for_load_state("domcontentloaded")
    early = page.evaluate(
        """() => [document.documentElement.classList.contains('lume-in'), document.documentElement.style.getPropertyValue('--lume-t'), window.__first]"""
    )
    assert early[0] and early[1] == "40ms", early
    # review round 1, M-2: the arrival never starts at the turned key with the ground already at 1 — the veil is still
    # coming in on the arriving page's first frame (the held old frame dissolves into it, motion.css)
    assert 0 < early[2] < 1, early
    page.wait_for_timeout(1000)
    late = page.evaluate(GONE)
    assert late["ground"] <= 0.01 and late["stage"] <= 0.01, late
    assert not page.evaluate("document.documentElement.classList.contains('lume-in')"), "the veil is gone with its clock, and its class with it"
    hit = page.evaluate("() => document.elementFromPoint(innerWidth / 2, innerHeight / 2).closest('.lume-veil')")
    assert hit is None
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(("lang", "width"), [("fr", 1440), ("ar", 390)])
def test_a_real_click_hands_on_what_was_painted_and_leaves_the_turn_to_the_arrival(browser, live_server, seeded, lang, width):
    """Review round 2, M-1: nothing asserted what a REAL click hands on (measured 265 / 290 ms: the time to pagehide,
    leaving 110-135 ms of the turn). The leaving page counts the frames it painted; the arrival starts at most 150 ms
    into the clock, so at least 250 ms of the turn play on the arriving page."""
    context = _context(browser, width)
    page = context.new_page()
    page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
    page.wait_for_function("() => document.documentElement.classList.contains('lume-warm')", timeout=3000)  # pre-warmed once idle
    link = page.locator(".main-nav__link[href]" if width >= 1024 else f"main a[href^='/{lang}/']:not([href='/{lang}/'])").first
    with page.expect_navigation():
        link.click()
    page.wait_for_load_state("domcontentloaded")
    handed = page.evaluate("document.documentElement.style.getPropertyValue('--lume-t')")
    assert handed.endswith("ms") and 0 <= int(handed[:-2]) <= 150, handed
    context.close()



@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_slow_navigation_s_arrival_never_turns_the_key_a_second_time(browser, live_server, seeded):
    """Finishing round F1, M-1: on a slow navigation (1.5 s of latency) the leaving page completes the turn and holds
    the key turned, the room half-lit; the arrival continues from the turned key (--lume-t ≥ 400 ms) — round 3 filmed
    the arrival clamped to 150 ms, the key turning a second time and the lit room going dark. Its first frame's key is
    turned (≥ 300°) or at identity."""
    context = _context(browser, 1440)
    context.add_init_script(
        """requestAnimationFrame(() => { const k = document.querySelector('.lume-veil .sig__turn');
          window.__key = k ? getComputedStyle(k).transform : ''; });"""
    )
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    page.wait_for_function("() => document.documentElement.classList.contains('lume-warm')", timeout=3000)
    cdp = context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 1500, "downloadThroughput": -1, "uploadThroughput": -1})
    with page.expect_navigation(timeout=15000):
        page.locator(".main-nav__link[href]").first.click()
    page.wait_for_load_state("domcontentloaded")
    handed = page.evaluate("document.documentElement.style.getPropertyValue('--lume-t')")
    assert handed.endswith("ms") and int(handed[:-2]) >= 400, handed
    key = page.evaluate("window.__key")
    match = re.match(r"matrix3d\(([^)]*)\)", key)
    if match:  # rotateY(a): m11 = cos(a); turned ≥ 300° → cos ≥ 0.5 (none: identity)
        assert float(match.group(1).split(",")[0]) >= 0.5, key
    context.close()

ROW = """() => { const items = [...document.querySelectorAll('.site-header__inner > .brand, .main-nav__link, .site-header__end > :not([popover])')]
  .filter(e => e.getClientRects().length && getComputedStyle(e).display !== 'none');
  return {rows: new Set(items.map(e => { const r = e.getBoundingClientRect(); return Math.round(r.top + r.height / 2); })).size,
    links: document.querySelectorAll('.main-nav__link').length, shown: items.filter(e => e.matches('.main-nav__link')).length,
    toggle: getComputedStyle(document.querySelector('.site-header .nav-toggle')).display,
    overflow: document.documentElement.scrollWidth - innerWidth}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_letterhead_holds_one_row_at_every_desktop_width(browser, live_server, seeded, lang):
    for width in (1024, 1280, 1440):
        context = _context(browser, width)
        page = context.new_page()
        page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
        row = page.evaluate(ROW)
        assert row["rows"] == 1 and row["shown"] == row["links"] and row["toggle"] == "none" and row["overflow"] <= 0, (width, row)
        context.close()
    context = _context(browser, 390)
    page = context.new_page()
    page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
    row = page.evaluate(ROW)
    assert row["shown"] == 0 and row["toggle"] != "none", "below 64rem the sheet carries the navigation"
    context.close()
