"""
The loader «Lume» across the product — V5.12 §4, the Director's DECISIONS §1 T1–T3 (lane A, wave W1).

Fast, offline (the sources):
* T1 — the cross-document View Transition is declared under `prefers-reduced-motion: no-preference` only; the page
  cross-fades on opacity alone; `ile-mark` is the one name that travels — the letterhead's mark, the sign-in's door, the
  console's tile (the rail's from 64rem, the top bar's below) — with one name per page (the entrance's letterhead gives
  it up) and none across a language switch; head.js skips the transition from the keyboard, on the preview hub and
  under html.rm, and hands «slow» / «lang» to the next page through sessionStorage, read once within five seconds;
* T2 — «la soglia»: lume/threshold.js arms on a same-origin link or a submit that nothing cancelled, never on a new
  tab, a download, a same-page anchor, an opted-out form, a form with its own host, an OUTCOME_BEARING form (the same
  four as loader.js), the preview hub or an error page; --motion-wait before anything shows, the word at 1 s, a lease
  of 10 s; no animation in the script; the line scales to .85 and holds (never to 1), from the inline-start edge;
  tier 0 from the keyboard; the still under reduced motion; the band's one `role="status"` line;
* T3 — the release once per space per session (accounts.signals.consume_space_release), the plate that takes the
  light, the reduced-motion lit still.

With Django's client: the letterhead carries the mark in layers over the lock-up's <img> and the status line; the
console carries the release on the first page of each space of the session, and the mark at rest after.

In Chromium (``-m browser``): a link whose answer comes late — a 204 after 1.4 s, so the page stays and can be read —
shows the line, the turned key and «Chargement…»; a fast one shows nothing; reduced motion shows the lit still; the
keyboard shows it at once; Arabic draws the line from the right; a pointer navigation runs a View Transition, the
keyboard and reduced motion do not, a language switch runs one without the mark's name.
"""

from __future__ import annotations

import gzip
import os
import re
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from django.conf import settings
from django.test import Client

from accounts.signals import ENTRANCE_RELEASE_KEY, LUME_SPACES_KEY, consume_space_release

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
MOTION_CSS = CSS / "v5" / "motion.css"
CONSOLE_MOTION = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_motion.css"
CONSOLE_ENTRY = ROOT / "apps" / "portal" / "static" / "portal" / "console.css"
TOKENS = CSS / "v5" / "tokens.css"
HEAD_JS = ROOT / "static" / "js" / "src" / "head" / "head.js"  # the commented source; static/js/head.js is its build
HEAD_BUILT = ROOT / "static" / "js" / "head.js"
SHELL_JS = ROOT / "static" / "js" / "src" / "shell.js"
THRESHOLD_JS = ROOT / "static" / "js" / "src" / "lume" / "threshold.js"
LOADER_JS = ROOT / "static" / "js" / "src" / "loader.js"
HEADER = ROOT / "templates" / "partials" / "header.html"
CHROME = ROOT / "templates" / "partials" / "portal_chrome.html"
RELEASE = 'data-lume="release"'


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _js(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _rule(css: str, selector: str) -> str:
    match = re.search(re.escape(selector) + r"\s*\{([^{}]*)\}", css)
    assert match, selector
    return match.group(1)


# ---------------------------------------------------------------------------------------------- T1, the sources


def test_the_view_transition_is_declared_under_no_preference_only_and_the_page_only_fades():
    css = _css(MOTION_CSS)
    assert re.search(
        r"@media \(prefers-reduced-motion: no-preference\) \{\s*@view-transition \{\s*navigation: auto;\s*\}\s*\}", css
    ), "the opt-in lives under no-preference: reduced motion has no View Transition"
    assert css.count("@view-transition") == 1
    assert "animation: lume-out var(--motion-fast) var(--ease-enter) 1 both;" in _rule(css, "::view-transition-old(root)")
    assert "animation: lume-in var(--motion-standard) var(--ease-enter) 1 both;" in _rule(css, "::view-transition-new(root)")
    for name in ("lume-out", "lume-in"):
        body = re.search(rf"@keyframes {name} \{{(.*?)\n\}}", css, flags=re.S).group(1)
        assert set(re.findall(r"([a-z-]+)\s*:", body)) == {"opacity"}, f"{name}: the page fades, it never travels (MS-O3)"
    group = _rule(css, "::view-transition-group(ile-mark)")
    assert "var(--motion-emphasized)" in group and "var(--ease-layout)" in group


def test_one_mark_travels_and_each_page_names_it_once():
    css = _css(MOTION_CSS)
    assert "view-transition-name: ile-mark;" in _rule(css, ".site-header .lock-sig,\n#varco-door")
    assert re.search(r"\.page-entrance \.site-header \.lock-sig,\s*:is\(\.vt-lang, \.lume-go, \.lume-in\) :is\(\.lock-sig, #varco-door\) \{\s*view-transition-name: none;", css), (
        "the sign-in's letterhead gives the name up to the door; a language switch takes it from both"
    )
    console = _css(CONSOLE_MOTION)
    assert re.search(r"@media \(min-width: 64rem\) \{\s*\.rail__tile \{\s*view-transition-name: ile-mark;", console)
    assert re.search(r"@media \(max-width: 63\.999rem\) \{\s*\.console-bar__tile \{\s*view-transition-name: ile-mark;", console)
    assert re.search(r"\.vt-lang :is\(\.rail__tile, \.console-bar__tile\) \{\s*view-transition-name: none;", console)
    assert _read(CONSOLE_ENTRY).rstrip().endswith('@import url("v5/_motion.css");'), "the console's half is the console's"
    imports = re.findall(r'@import url\("([^"]+)"\)', _css(CSS / "main.css"))
    # V5.15: the central veil (v5/lume.css) closes the cascade, right after motion.css
    assert imports[-2:] == ["v5/motion.css", "v5/lume.css"] and imports.index("v5/motion.css") > imports.index("v5/loader.css")
    assert "_motion" not in " ".join(imports), "a public page never downloads the console's half"


def test_head_js_skips_hands_over_and_reads_once():
    js = _js(HEAD_JS)
    assert 'addEventListener("pagereveal"' in js and 'addEventListener("pageswap"' in js
    swap = js.split('addEventListener("pageswap"', 1)[1].split("});", 1)[0]
    assert 'root.getAttribute("data-input") === "key"' in swap and 'classList.contains("rm")' in swap and "hub()" in swap
    assert "transition.skipTransition();" in swap, "keyboard (tier 0), the preview hub and the preview's flag: no transition"
    assert "langOf(new URL(entry.url)) !== langOf(location)" in swap and 'root.classList.add("vt-lang")' in swap
    reveal = js.split('addEventListener("pagereveal"', 1)[1].split("});", 1)[0]
    assert "transition.finished.then(done, done)" in reveal, "the language's class leaves with the transition"
    hide = js.split('addEventListener("pagehide"', 1)[1].split("});", 1)[0]
    # V5.15: the hand-off is the veil's («go» and the click's time) or the language's; W1's «slow» arrival light left
    # with the band's line (tests/frontend/test_lume_v515_a.py holds the veil's hand-off)
    assert '"go"' in hide and '"lang"' in hide
    assert "try { sessionStorage.setItem(KEY" in hide, "storage refused: nothing handed on, nothing breaks"
    assert "sessionStorage.removeItem(KEY)" in js and "age < 15000" in js and "age < 5000" in js, "read once, while fresh"
    assert 'root.classList.add("vt-lang")' in js and "lume-arrive" not in js
    assert "prefers-reduced-motion" not in js, "the setting turns the transition off in the sheet"


# ---------------------------------------------------------------------------------------------- T2, the sources


def test_the_threshold_decides_when_and_draws_nothing():
    js = _js(THRESHOLD_JS)
    assert "export const WORD_AFTER = 1000;" in js and "export const SLOW_AFTER = 10000;" in js
    assert 'durationToken("--motion-wait", 400)' in js, "nothing before the threshold token"
    loader = re.search(r"OUTCOME_BEARING = new Set\(\[([^\]]*)\]\)", _read(LOADER_JS)).group(1)
    mine = re.search(r"OUTCOME_BEARING = new Set\(\[([^\]]*)\]\)", js).group(1)
    assert set(re.findall(r'"([a-z-]+)"', mine)) == set(re.findall(r'"([a-z-]+)"', loader)), "the two lists are one"
    leaves = js.split("export function leaves(event)", 1)[1].split("\n}\n", 1)[0]
    for exclusion in (
        "event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey",
        'link.hasAttribute("download") || optedOut(link)',
        '["", "_self"].includes(link.getAttribute("target") || "")',
        "url.origin !== location.origin",
        "return !(here && url.hash);",
    ):
        assert exclusion in leaves, exclusion
    submits = js.split("export function submits(form, staysOnPage)", 1)[1].split("\n}\n", 1)[0]
    # V5.18 §4 (P12): the sign-in's form (`data-loader-host`) is a navigation like any other — login → platform is the
    # central veil's — so it is no longer excluded here; loader.js then leaves its door at rest (test_loader_rules.py)
    assert "if (staysOnPage || optedOut(form)) return false;" in submits and "loaderHost" not in submits
    assert 'OUTCOME_BEARING.has(form.dataset.loaderAction || "")' in submits
    assert 'document.body.matches(".dp-page, .page-error")' in js, "never on the preview hub, never on an error page"
    after = js.split("export function after(event)", 1)[1].split("\n}\n", 1)[0]
    assert "if (still()) return false;" in after and after.rstrip().endswith("return true;"), "it says whether it took the page"
    assert "if (event.defaultPrevented) return;" in after and "depart();" in after and "}, 0);" in after, (
        "armed once nothing cancelled it"
    )
    depart = js.split("export function depart()", 1)[1].split("\n}\n", 1)[0]
    assert 'root.classList.add("is-departing"), wait)' in depart and "setTimeout(quiet, SLOW_AFTER)" in depart
    assert "Math.max(WORD_AFTER, wait)" in depart
    init = js.split("export function initThreshold()", 1)[1]
    assert '"click"' in init and "true," in init, "a capture-phase click"
    assert "event.persisted) quiet()" in init and '"navigateerror", quiet' in init
    for forbidden in (".animate(", "requestAnimationFrame", "prefers-reduced-motion", "minDisplay", "MIN_SHOWN"):
        assert forbidden not in js, f"{forbidden}: the threshold draws nothing and holds nothing"
    shell = _js(SHELL_JS)
    assert 'import { after, initThreshold, submits } from "./lume/threshold.js";' in shell and "initThreshold();" in shell


def test_the_band_line_left_for_the_central_veil():
    """V5.15 §8: «a gold line under the header is NOT the primary branded loader». W1's band line, the band's turning
    key and the console bar's line are gone; the wait's held, never-finished drawing is the veil's sill
    (test_lume_v515_a.py: scaleX .85, held). The tokens of the line stay for any later consumer."""
    css = _css(MOTION_CSS)
    assert ".site-header::after" not in css and "@keyframes lume-line" not in css
    assert ".is-departing .site-header" not in css
    console = _css(CONSOLE_MOTION)
    assert ":is(.console-bar, .console-bar__inner)::after" not in console and ".is-departing" not in console
    tokens = _css(TOKENS)
    assert '[dir="rtl"] { --lume-line-to: 270deg; }' in tokens and "--lume-line-to: 90deg;" in tokens

def test_the_page_says_it_once_in_words_written_by_the_template():
    """V5.15: the one status line of a wait is the central veil's (components/lume_veil.html), on every page; the
    letterhead and the console bar carry none any more. The letterhead keeps its mark in layers over the <img>."""
    for path in (HEADER, CHROME):
        assert "data-lume-word" not in _read(path), path.name
    veil = _read(ROOT / "templates" / "components" / "lume_veil.html")
    assert veil.count("data-lume-word") == 1
    assert """<p class="lume-veil__word" role="status" data-lume-word="{% translate 'Chargement…' %}"></p>""" in veil
    header = _read(HEADER)
    assert '{% include "components/loader.html" with css_class="lock-sig" %}{% brand_lockup %}' in header
    css = _css(MOTION_CSS)
    assert "visibility: hidden;" in _rule(css, ".site-header .lock-sig + .lock .lock__mark"), "one mark is seen, not two"
    lume = _css(ROOT / "static" / "css" / "v5" / "lume.css")
    assert "display: none;" in _rule(lume, ".lume-veil__word:empty")
    # Typography V2 (FINAL_DELIVERY_V2 R1, TYPOGRAPHY_V2: every Arabic type rule in the subject form ``.x:lang(ar)``;
    # V5.20, lane CLOSING §3.9 c): the veil's word is read in the subject form, the same invariant (no tracking in
    # Arabic) — tools/probe_subject.py proved both selectors match the same elements on every Arabic page at 1440 and
    # 390 (CLOSING NOTES §3); the descendant form is gone, so it cannot return beside it
    assert "letter-spacing: 0;" in _rule(lume, ".lume-veil__word:lang(ar)")
    assert not re.search(r":lang\(ar\)\s+\.lume-veil__word", lume), "the Arabic rule is written once, in the subject form"

def test_head_js_is_served_minified_from_its_source():
    """Review v512-a-fix-w1: the render-blocking head script is the build of its commented source."""
    built = _read(HEAD_BUILT)
    assert built.startswith("/* built from static/js/src/head/head.js"), "static/js/head.js is written by npm run build:js"
    banner, code = built.split("\n", 1)
    assert banner.endswith("*/") and code.count("\n") <= 1 and "/*" not in code, "minified: no comment but the banner"
    assert "pagereveal" in built and "pageswap" in built and "ile.lume" in built and 'replace("no-js","js")' in built
    assert "import " not in built and "export" not in built, "a classic script, not a module"
    assert HEAD_BUILT.stat().st_mtime >= HEAD_JS.stat().st_mtime - 1, "head.js is older than its source: npm run build:js"
    # V5.15: the veil's hand-off must run before the first paint — the Director's measured exception (QA/v515/a/NOTES.md)
    assert len(gzip.compress(built.encode("utf-8"), 9)) <= 1250, "the critical path's script stays under 1.25 KB gzip"


@pytest.mark.django_db
def test_every_page_names_its_release_in_the_head(client, seeded):
    html = client.get("/fr/").content.decode()
    head = html.split("</head>", 1)[0]
    assert re.search(r'<meta name="generator" content="Italy Legal Entry™ [^"]+">', head), "the release number, in the head"


def test_a_download_link_opts_out():
    detail = _read(ROOT / "templates" / "documents" / "requirement_detail.html")
    assert re.search(r'<a href="\{\{ version\.download_url \}\}"[^>]*data-loader="none"', detail), (
        "a file is not a page: no threshold would ever end"
    )


# ---------------------------------------------------------------------------------------------- T3, the flags


def _request(session=None):
    return SimpleNamespace(session={} if session is None else session)


def test_the_release_plays_once_per_space_per_session():
    request = _request({ENTRANCE_RELEASE_KEY: True})
    assert consume_space_release(request, "person") is True, "the sign-in's first console page"
    assert ENTRANCE_RELEASE_KEY not in request.session and request.session[LUME_SPACES_KEY] == ["person"]
    assert consume_space_release(request, "person") is False, "never twice in a space"
    assert consume_space_release(request, "company") is True, "the first page of a further space"
    assert consume_space_release(request, "company") is False
    assert request.session[LUME_SPACES_KEY] == ["person", "company"]
    request.session[ENTRANCE_RELEASE_KEY] = True
    assert consume_space_release(request, "company") is True, "a new sign-in starts the list again"
    assert request.session[LUME_SPACES_KEY] == ["company"]
    assert consume_space_release(_request(), "") is False, "no space, no sign-in: nothing"
    assert consume_space_release(_request({ENTRANCE_RELEASE_KEY: True}), "") is True, "no space: the sign-in alone"
    assert consume_space_release(SimpleNamespace(), "person") is False, "no session at all"


def test_the_plate_takes_the_light_on_the_release_s_phase_and_its_still():
    light = _css(CSS / "v5" / "_loader-light.css")
    plate = ':is(.rail__tile, .console-bar__tile):has(> [data-lume="release"])'
    assert f"{plate}::before {{ animation: lume-plate-o var(--motion-door) linear 1 both; }}" in light
    assert re.search(re.escape(plate) + r"::before \{[^}]*opacity: 0;", light), "at rest it is not there"
    reduced = light.split("@media (prefers-reduced-motion: reduce)", 1)[1].split("\n}", 1)[0]
    assert "animation: lume-still var(--motion-reduced) linear var(--lume-still) 1 both;" in reduced
    assert '[data-lume="release"] .sig__lume { transform: none; }' in reduced, "the still does not grow"
    keyframes = _css(MOTION_CSS)
    still = re.search(r"@keyframes lume-still \{(.*?)\n\}", keyframes, flags=re.S).group(1)
    assert set(re.findall(r"([a-z-]+)\s*:", still)) == {"opacity"}


# ---------------------------------------------------------------------------------------------- with Django's client


@pytest.mark.django_db
def test_the_letterhead_lays_the_mark_in_layers_over_the_lock_up(client, seeded):
    for lang in ("fr", "ar"):
        html = client.get(f"/{lang}/").content.decode()
        assert html.count('<span class="sig lock-sig"') == 1, lang
        assert html.index('class="sig lock-sig"') < html.index('class="lock__mark"'), "the layers come first, the <img> under"
        assert html.count('role="status" data-lume-word=') == 1, lang  # the veil's (V5.15)
        assert RELEASE not in html, "the console's release stays the console's"


@pytest.mark.django_db
def test_the_console_releases_once_per_space_and_keeps_the_mark_at_rest(client, seeded, person_user):
    """The person's space: the release on the first page, the mark at rest in layers after. The company space's first
    page is the same flag (test_the_release_plays_once_per_space_per_session; measured on the lane server with
    qa-company, docs/design-v5/QA/v512/a-w1/NOTES.md)."""
    client.force_login(person_user)
    first = client.get("/fr/espace-reserve/").content.decode()
    assert first.count(RELEASE) == 2, "the rail's mark and the top bar's mark"
    assert client.session[LUME_SPACES_KEY] == ["person"] and ENTRANCE_RELEASE_KEY not in client.session
    again = client.get("/fr/espace-reserve/").content.decode()
    assert RELEASE not in again and again.count('<span class="sig"') == 2, "at rest, in layers"
    assert again.count('role="status" data-lume-word=') == 1, "the page's one status line: the veil's (V5.15)"


# ---------------------------------------------------------------------------------------------- in Chromium

STATE = r"""() => {
  const h = document.documentElement;
  const band = [...document.querySelectorAll('.site-header, .console-bar')].find((e) => e.getClientRects().length);
  const line = getComputedStyle(band, '::after');
  const word = document.querySelector('[data-lume-word]');
  const turn = [...document.querySelectorAll('.lock-sig .sig__turn, .rail__tile > .sig .sig__turn, .console-bar__tile > .sig .sig__turn')].find((e) => e.getClientRects().length);
  const sig = turn.closest('.sig');
  return {departing: h.classList.contains('is-departing'), lineOpacity: line.opacity, lineTransform: line.transform,
    lineOrigin: line.transformOrigin, lineAnim: line.animationName, lineDuration: line.animationDuration,
    word: word.textContent, wordShown: getComputedStyle(word).display !== 'none',
    wordTop: word.getBoundingClientRect().top, wordStart: word.getBoundingClientRect().left,
    wordEnd: word.getBoundingClientRect().right, bandBottom: band.getBoundingClientRect().bottom,
    turn: getComputedStyle(turn).animationName, turnDuration: getComputedStyle(turn).animationDuration,
    light: getComputedStyle(sig.querySelector('.sig__lume')).opacity, width: innerWidth};
}"""


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


def _context(browser, live_server, motion="no-preference", user=None, width=1440):
    context = browser.new_context(viewport={"width": width, "height": 900 if width > 600 else 844}, reduced_motion=motion)
    if user is not None:
        client = Client()
        client.force_login(user)
        context.add_cookies(
            [{"name": settings.SESSION_COOKIE_NAME, "value": client.cookies[settings.SESSION_COOKIE_NAME].value, "url": live_server.url}]
        )
    return context


def _late_link(page, seconds):
    """A link of this site whose answer comes `seconds` late and is a 204: the navigation never commits, so the page
    that waited stays to be read. The handler holds the answer; the page's own clock runs meanwhile."""

    def answer(route):
        time.sleep(seconds)
        route.fulfill(status=204, body="")

    page.route("**/__lume-late/**", answer)
    page.evaluate(
        """() => { const a = document.createElement('a'); a.href = '/fr/__lume-late/'; a.id = 'lume-late'; a.textContent = 'late';
        a.style.cssText = 'position:fixed;bottom:120px;left:160px;z-index:9999;background:#fff;padding:12px'; document.body.append(a); }"""
    )
    return page.locator("#lume-late")


# V5.15 (DECISIONS §15 lane A): the threshold's picture is the central veil now — its departure, its hold, its still,
# Esc — measured by tests/frontend/test_lume_v515_a.py on the public pages; here, the console takes the same veil, and
# the View Transition steps aside whenever the veil is the page change.

VEIL = """() => { const h = document.documentElement; const v = document.querySelector('.lume-veil');
  return {go: h.classList.contains('lume-go'), departing: h.classList.contains('is-departing'),
    visible: getComputedStyle(v).visibility, turn: getComputedStyle(v.querySelector('.sig__turn')).animationName,
    word: document.querySelector('[data-lume-word]').textContent, words: document.querySelectorAll('[data-lume-word]').length}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_console_takes_the_central_veil(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, user=person_user, width=390)
    context.add_init_script("try { sessionStorage.setItem('ile.lume1', '1'); } catch (e) {}")
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/espace-reserve/", wait_until="networkidle")
    _late_link(page, 1.4).click(no_wait_after=True)
    page.wait_for_timeout(200)
    state = page.evaluate(VEIL)
    assert state["go"] and state["departing"] and state["visible"] == "visible" and state["turn"] == "lume-key-finish", state
    assert state["word"] == "Chargement…" and state["words"] == 1, "the platform's one status line"
    context.close()


VT = "window.__vt = 'unset'; addEventListener('pagereveal', (e) => { window.__vt = e.viewTransition ? 'vt' : 'none'; window.__lume = document.documentElement.classList.contains('lume-in'); });"


def _go(page, href, key=False):
    page.evaluate(
        f"""() => {{ const a = document.createElement('a'); a.href = '{href}'; a.id = 'lume-go'; a.textContent = 'go';
        a.style.cssText = 'position:fixed;bottom:120px;left:160px;z-index:9999;background:#fff;padding:12px'; document.body.append(a); }}"""
    )
    link = page.locator("#lume-go")
    with page.expect_navigation(wait_until="networkidle"):
        if key:
            link.focus()
            page.keyboard.press("Enter")
        else:
            link.click()
    page.wait_for_timeout(900)  # the veil's clock is over before the next departure
    return page.evaluate("() => [window.__vt, window.__lume]")


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("motion", ["no-preference", "reduce"])
def test_the_veil_is_the_page_change_and_the_view_transition_steps_aside(browser, live_server, seeded, motion):
    """A pointer's navigation: the veil arrives (lume-in); under it the View Transition is only a short dissolve of the
    held old frame (V5.15 review round 1, DL54-170 — the cut from the paint-held frame to the full veil), where the
    setting allows a View Transition at all; the keyboard: neither (tier 0). No mark travels under the veil
    (motion.css: `:is(.vt-lang, .lume-go, .lume-in)` takes the name away); the mark in layers keeps its name for the
    navigations the veil does not take."""
    context = _context(browser, live_server, motion=motion)
    context.add_init_script(VT)
    context.add_init_script("try { sessionStorage.setItem('ile.lume1', '1'); } catch (e) {}")
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    names = page.evaluate("() => getComputedStyle(document.querySelector('.lock-sig')).viewTransitionName")
    assert names == "ile-mark"
    dissolve = "vt" if motion == "no-preference" else "none"
    assert _go(page, "/fr/faq/") == [dissolve, True], "the veil, over a short dissolve of the held frame"
    assert _go(page, "/fr/glossaire/", key=True) == ["none", False], "tier 0 from the keyboard"
    # from a page of the site that is not an error page (the test database answers 404 for the FAQ and the glossary,
    # and an error page never begins the veil: its door stays still)
    page.goto(f"{live_server.url}/fr/", wait_until="networkidle")
    page.mouse.move(5, 300)
    assert _go(page, "/ar/") == [dissolve, True], "a language switch: the veil too"
    context.close()


#: The forms whose answer is a legal outcome, each with its name in threshold.js's OUTCOME_BEARING (DL54-09): the
#: threshold and the arrival light skip them, the button keeps its busy key. Tagged at the v512 W1 merge (the review's
#: M5; DL54-164). «eligibility» has no form in the product today: the name stays reserved in both lists.
OUTCOME_FORMS = {
    "templates/portal/situation.html": "recalculate-situation",
    "templates/orientation/_step.html": "pre-assessment",
    "templates/documents/requirement_detail.html": "scan-verification",
}


def test_an_outcome_bearing_form_names_its_action_and_a_download_link_opts_out():
    listed = re.search(r"OUTCOME_BEARING = new Set\(\[([^\]]*)\]\)", _read(THRESHOLD_JS)).group(1)
    names = set(re.findall(r'"([a-z-]+)"', listed))
    for template, action in OUTCOME_FORMS.items():
        assert action in names, action
        assert f'data-loader-action="{action}"' in _read(ROOT / template), template
    # an attachment's download answers a file: no page would end the wait (DECISIONS §1, «never shown on downloads»)
    discussion = _read(ROOT / "templates" / "community" / "discussion.html")
    links = re.findall(r'<a href="\{\{ download_url \}\}"[^>]*>', discussion)
    assert links and all('data-loader="none"' in link for link in links), links
