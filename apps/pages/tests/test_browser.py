"""
Browser tests (Playwright, Chromium) of the homepage and institutional pages.

Checks that need a real layout engine: no horizontal overflow at 360/768/1440 in LTR and RTL,
content never hidden by the reveal motion, the Forum banner in the flow (never an overlay) and its
client-side-only dismissal, no request outside the site. Skipped when Chromium is not installed.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

VIEWPORTS = {"mobile": (360, 780), "tablet": (768, 1024), "desktop": (1440, 900)}
PATHS = ("/{lang}/", "/{lang}/le-projet/", "/{lang}/agami/", "/{lang}/reseau/", "/{lang}/contact/")


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
def before_the_forum_live(monkeypatch):
    """
    The run-up to the Forum for the live server — banner up — WITHOUT freezegun: a frozen
    ``time.monotonic`` stalls Playwright's event loop. The banner gate and the edition's mode are
    read through ``core.clock.now()``, so patching it is enough (as ``phase3_live`` does in
    tests/i18n/test_rtl_browser.py). On the real clock the banner expired on 2 Oct 2026: the two
    banner tests below were skipped instead of run, and the layout sweeps stopped laying it out.
    """
    from core import clock, flags
    from tests.conftest import BEFORE_THE_FORUM

    monkeypatch.setattr(clock, "now", lambda: BEFORE_THE_FORUM)
    flags.invalidate()
    yield BEFORE_THE_FORUM
    flags.invalidate()


def _page(browser, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    return context, context.new_page()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("viewport", list(VIEWPORTS))
def test_no_overflow_and_no_hidden_content(browser, live_server, seeded, lang, viewport):
    width, height = VIEWPORTS[viewport]
    context, page = _page(browser, width, height)
    try:
        for path in PATHS:
            page.goto(live_server.url + path.format(lang=lang), wait_until="networkidle")
            scroll_w, client_w = page.evaluate(
                "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
            )
            assert scroll_w <= client_w, (lang, viewport, path, scroll_w, client_w)
            assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
            hidden = page.evaluate(
                "Array.from(document.querySelectorAll('.reveal'))"
                ".filter(e => getComputedStyle(e).opacity === '0').length"
            )
            assert hidden == 0, (lang, viewport, path)
            assert page.locator("h1").count() == 1
    finally:
        context.close()


def test_homepage_loads_nothing_outside_the_site(browser, live_server, seeded):
    context, page = _page(browser, 1440, 900)
    requests: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        assert [u for u in requests if not u.startswith(live_server.url)] == []
        assert any("/static/css/dist/pages/css/pages.css" in u for u in requests)
        # The only photographs requested are the hero's own (design V5.4, W2-D): the door's photograph — the one
        # preloaded, high-priority image — and the four audience photographs of static/img/photos/hero/, decorative
        # (alt=""), never a <figure>, their provenance recorded. No other photograph: a <figure> without a
        # <figcaption> is still a defect (art direction A §6.2).
        photos = [u for u in requests if "/static/img/photos/" in u]
        assert photos and all("/static/img/photos/hero/he-" in u for u in photos), photos
        assert len([u for u in requests if "/static/brand/v5/doorway-arch-" in u]) == 1, "the door, once"
    finally:
        context.close()


def test_forum_banner_is_in_the_flow_and_dismissible_client_side_only(
    browser, live_server, seeded, before_the_forum_live
):
    context, page = _page(browser, 1280, 900)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        banner = page.locator("[data-dismissible='forum-banner']")
        assert banner.count() == 1, "the banner is up in the run-up to the Forum"
        assert banner.is_visible()
        # In the flow, and ATTACHED to the hero: the institution speaks, and this is what it is
        # announcing now. The hero drops its closing space when a banner follows it. (The selector
        # was `.home-plate` until design V2 replaced the navy plate with the midnight chapter.)
        assert page.evaluate("getComputedStyle(document.querySelector('.home-banner')).position") == "relative"
        hero_bottom = page.evaluate("document.querySelector('[data-section=\"hero\"]').getBoundingClientRect().bottom")
        banner_top = page.evaluate("document.querySelector('.home-banner').getBoundingClientRect().top")
        assert abs(banner_top - hero_bottom) < 2
        cookies_before = {c["name"] for c in context.cookies()}
        dismiss = page.locator("[data-dismiss]")
        assert dismiss.is_visible()  # enabled by the script (hidden without JS)
        box = dismiss.bounding_box()
        assert box["width"] >= 44 and box["height"] >= 44  # WCAG 2.5.8 target size
        dismiss.focus()
        page.keyboard.press("Enter")
        assert not banner.is_visible()
        assert page.evaluate("document.activeElement.id") == "main-content"
        # No cookie written, nothing sent: the choice lives in sessionStorage for this tab only.
        assert {c["name"] for c in context.cookies()} == cookies_before
        assert page.evaluate("sessionStorage.getItem('ile.dismissed.forum-banner')") == "1"
        page.reload(wait_until="networkidle")
        assert not page.locator("[data-dismissible='forum-banner']").is_visible()
    finally:
        context.close()


def test_forum_banner_stays_without_javascript(browser, live_server, seeded, before_the_forum_live):
    context = browser.new_context(viewport={"width": 1280, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/", wait_until="load")
        assert page.locator("[data-dismissible='forum-banner']").count() == 1, "the banner is up"
        assert page.locator("[data-banner='forum']").is_visible()
        assert not page.locator("[data-dismiss]").is_visible()
        assert page.locator(".register--entrances .entry").count() == 4
        # Without JavaScript the hero is its rested picture, and its four origins are the page's visible entrances at
        # 1280: the register under the hero is not drawn there (the hero's review fix, W2-D, 9 October 2026 —
        # hero.css), but its four piers stay in the document, the page's structure.
        assert page.locator(".he-origin__link").count() == 4
        assert page.locator(".he-origin__link").first.is_visible()
        assert not page.locator(".register--entrances").is_visible()
    finally:
        context.close()


def test_the_four_entrances_are_a_quay_and_the_dark_chapters_are_deliberate(browser, live_server, seeded):
    """
    The four entrances are not four identical cards, and the dark grounds are not scattered.

    Both halves of this test outlive the art directions that first wrote them; only their shapes
    changed. The entrances were four columns side by side, each with its own line drawing — the
    banned pattern twice over, applied to the four most important links on the site. They became a
    stacked register, on 24 September 2026 a quay of four piers (DESIGN_SYSTEM_V2.md §8.5: a zig-zag
    with an index, a landform glyph, a tint and a mooring line each), and with design V5.4 the hero
    itself carries the four — photograph, word, sentence, call. What is under the hero since W2-D
    step 3 is the register again, one frame of four rows without index or glyph (the four are never
    ranked), and it is drawn only where the hero's tiles carry words alone. What is still forbidden
    is what was always forbidden — four boxes of the same width, in the same row, telling the reader
    nothing about which door is theirs. On a phone they stack, because a list is what survives 320px.

    The ground change was "exactly one navy band per page". The V2 principle is the same rule with
    a number that fits an immersive page: at most two midnight chapters on HOME and FORUM, at most
    one anywhere else, and they begin and end at a section boundary. Two on the home — today the
    pilot's statement and the reserved row the footer continues — is the ceiling, not an invitation.
    """
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        piers = page.evaluate(
            """() => Array.from(document.querySelectorAll('.register--entrances .entry')).map(e => {
                 const r = e.getBoundingClientRect();
                 return {top: Math.round(r.top), width: Math.round(r.width), link: e.tagName === 'A'};
               })"""
        )
        assert len(piers) == 4
        assert all(p["link"] for p in piers), "every pier is a link: the whole panel is the target"
        # Since the hero's review fix (design V5.4, W2-D, 9 October 2026): on the desktop the hero's four origins carry
        # the word, the sentence and the call at rest, so the register under the hero — the same four, the same four
        # sentences, the same four links — is not drawn there (hero.css: UX-1, design M-6; RH-5 «the audiences once»,
        # RH-6 «each block raises a new question»). The piers stay in the DOM: the list is the page's structure, and
        # the phone below is where the register is the only copy of the sentences.
        hidden = page.evaluate("getComputedStyle(document.querySelector('.home-entrances')).display")
        assert hidden == "none", "under the hero at 1440 the register repeats the hero's four: not drawn"
        glosses = page.evaluate(
            "Array.from(document.querySelectorAll('.he-origin__gloss')).map(e => e.getBoundingClientRect().width)"
        )
        assert len(glosses) == 4 and all(w > 100 for w in glosses), "the hero's four sentences are drawn on the desktop"

        chapters = page.locator(".chapter--dark").count()
        assert chapters <= 2, f"at most two midnight chapters on an immersive page, found {chapters}"
        # Since design V5.4 (W2-D) the hero is not a midnight chapter: a light wall with ONE night niche, the door's,
        # at its end (HERO_FINAL.md §2); the midnight chapters of the page start under it.
        first = page.evaluate("document.querySelector('.chapter--dark')?.getAttribute('data-section')")
        assert first != "hero", "the hero is a light wall with a night niche, not a midnight chapter"
        assert page.locator("[data-section='hero'] .he-niche").count() == 1
    finally:
        context.close()

    context, page = _page(browser, 390, 844)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        tops = page.evaluate(
            "Array.from(document.querySelectorAll('.register--entrances .entry'))"
            ".map(e => Math.round(e.getBoundingClientRect().top))"
        )
        assert len(tops) == 4
        assert len(set(tops)) == 4, "on a phone the quay stacks: four piers, four tops"
        assert tops == sorted(tops)
        # On a phone the hero's tiles carry words only (the brief's composition), so the register under the hero is the
        # page's one copy of the four sentences, and it reads at 16 px (RE-4; the review's MOB-1).
        shown = page.evaluate("getComputedStyle(document.querySelector('.home-entrances')).display")
        assert shown != "none"
        gloss = page.evaluate("getComputedStyle(document.querySelector('.home-entrances .entry__gloss')).fontSize")
        assert gloss == "16px", gloss
        words = page.evaluate(
            "Array.from(document.querySelectorAll('.he-origin__word')).map(e => getComputedStyle(e).fontSize)"
        )
        assert words == ["16px"] * 4, words
    finally:
        context.close()


# ---- Reviewer additions: 390 px (common phone width), both gate states, anti-fraud page included ----
@pytest.fixture
def phase3_live(seeded):
    """Open gate G3 for the live server without freezing time (Playwright needs a real clock)."""
    from core import flags
    from core.models import FeatureFlag

    FeatureFlag.objects.update_or_create(
        key="phase3_public", defaults={"enabled": True, "enabled_from": None, "enabled_until": None}
    )
    flags.invalidate()
    yield
    flags.invalidate()


def _assert_fits(page, label):
    scroll_w, client_w = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    assert scroll_w <= client_w, (label, scroll_w, client_w)
    # No element of the main landmark may stick out of the viewport either (clipped overflow is still a defect).
    offenders = page.evaluate(
        """() => { const w = document.documentElement.clientWidth;
        // An element inside a box that CLIPS is not sticking out of the viewport: it is contained,
        // and the reader sees exactly the part the design meant them to see. The hero's territory
        // drawing is drawn with preserveAspectRatio="slice" precisely so it always covers, which
        // means its geometry always extends past the frame — inside `.hero { overflow: clip }`.
        // Without this exception the rule would forbid every full-bleed drawing on the site.
        const clipped = (el) => {
          for (let p = el.parentElement; p; p = p.parentElement) {
            const o = getComputedStyle(p).overflowX;
            if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return true;
          }
          return false;
        };
        return Array.from(document.querySelectorAll('main *')).filter(e => {
          const r = e.getBoundingClientRect();
          return r.width > 0 && (r.left < -1 || r.right > w + 1)
                 && !e.closest('.visually-hidden') && !clipped(e);
        }).slice(0, 5).map(e => e.tagName + '.' + e.className); }"""
    )
    assert offenders == [], (label, offenders)
    assert page.locator("h1").count() == 1, label


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_phone_390_gate_closed(browser, live_server, seeded, lang):
    context, page = _page(browser, 390, 844)
    try:
        for path in PATHS:
            page.goto(live_server.url + path.format(lang=lang), wait_until="networkidle")
            _assert_fits(page, (lang, path))
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("viewport", [*VIEWPORTS, "phone-390"])
def test_the_homepage_with_the_forum_banner_fits_every_width(
    browser, live_server, seeded, before_the_forum_live, lang, viewport
):
    """
    The homepage of the run-up to the Forum, banner up, at every width the layout sweeps use, LTR and RTL.

    Those sweeps (``test_no_overflow_and_no_hidden_content``, ``test_phone_390_gate_closed``,
    tests/frontend/test_browser.py) read the real clock: from 2 October 2026 they lay out a homepage
    without the banner, and still pass. The banner can be scheduled again from the back office, so its
    layout is checked here at a named moment, and its presence is asserted rather than assumed.
    """
    width, height = VIEWPORTS.get(viewport, (390, 844))
    context, page = _page(browser, width, height)
    try:
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        banner = page.locator("[data-banner='forum']")
        assert banner.count() == 1, "the page under test carries the banner"
        assert banner.is_visible()
        assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
        hidden = page.evaluate(
            "Array.from(document.querySelectorAll('.reveal')).filter(e => getComputedStyle(e).opacity === '0').length"
        )
        assert hidden == 0, (lang, viewport)
        _assert_fits(page, (lang, viewport))
    finally:
        context.close()


_HERO_GEOMETRY = """() => {
  const q = (s) => document.querySelector(s);
  const R = (el) => {
    const b = el.getBoundingClientRect();
    return {x: b.left, y: b.top, w: b.width, h: b.height, r: b.right, b: b.bottom};
  };
  const lines = (el) => Math.round(el.getBoundingClientRect().height / parseFloat(getComputedStyle(el).lineHeight));
  const door = R(q('.he-door')), niche = R(q('.he-niche')), hero = R(q('.he'));
  const pathWall = q('.he-path--wall') && R(q('.he-path--wall')), rail = q('.he-rail') && R(q('.he-rail'));
  const vw = document.documentElement.clientWidth, rtl = getComputedStyle(q('.he')).direction === 'rtl';
  // an element's distance from the window's reading-start edge: what «stands on one column» compares
  const start = (el) => (el ? (rtl ? vw - R(el).r : R(el).x) : null);
  const all = (s) => Array.from(document.querySelectorAll(s));
  return {
    vw, vh: innerHeight, rtl, variant: q('.he').dataset.heroVariant,
    hero, niche, door, pathWall, rail, promise: R(q('.he__promise')),
    plates: all('.he-plate').map(e => R(e).w),
    plateBoxes: all('.he-plate').map(R),
    columns: all('.he-origin').map(e => R(e).w),
    tiles: all('.he-origin__link').map(R),
    glossLines: all('.he-origin__gloss').map(lines),
    glossTops: all('.he-origin__gloss').map(e => R(e).y),
    nodes: all('.he-station__node').map(R),
    labels: all('.he-station__label').map(R),
    body: R(q('.he__body')),
    edges: {
      logo: start(q('.site-header .brand')), promise: start(q('.he__promise')), plate: start(q('.he-plate')),
      body: start(q('.he__body')), chapter: start(q('.chapter:not(.home-entrances) .section__title')),
    },
    lead: q('.he__lead') && {
      display: getComputedStyle(q('.he__lead')).display, size: getComputedStyle(q('.he__lead')).fontSize,
    },
    railStart: rail && getComputedStyle(q('.he-rail')).borderInlineStartWidth,
  };
}"""


def test_the_hero_holds_its_geometry(browser, live_server, phase3_live):
    """
    The hero's geometry, on the settled still (reduced motion: no movement to wait for), Phase 3 (the stations drawn).

    What the review fix of 9 October 2026 measured and closed (design V5.4, W2-D;
    docs/design-v5/QA/v54/w2-d/NOTES.md §7), held: the wall takes the page (it starts at the page's pad, whatever the
    chrome's column), the composition keeps the hero's height (the fold shows the description's first line, 48 px at
    1440 × 900), the door stands on the niche's floor with the path on its springing, the plates are 180 px or more
    and no sentence is over five lines at 1440. And two defects of the port that two smokes had not seen: the
    product's list reset took the stations' start padding, which left the phone rail's nodes off the rail and Maroc's
    disc off the compact desktop's path.
    """

    def still(width, height, lang="fr"):
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=1, reduced_motion="reduce"
        )
        page = context.new_page()
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        page.wait_for_selector(".he.is-ajar")
        try:
            return page.evaluate(_HERO_GEOMETRY)
        finally:
            context.close()

    g = still(1440, 900)
    assert abs(g["promise"]["x"] - 32) <= 1, "the wall starts at the page's pad"
    assert abs(g["niche"]["r"] - g["vw"]) <= 1, "the niche bleeds to the page's far edge"
    assert abs(g["niche"]["b"] - (g["vh"] - 48)) <= 1, "the composition keeps the hero's height: a 48 px peek"
    assert g["body"]["y"] >= g["niche"]["b"] - 1 and g["body"]["y"] < g["vh"], "the description opens at the fold"
    assert abs((g["niche"]["b"] - g["door"]["b"]) - 16) <= 1, "the door stands 16 px above the niche's floor"
    springing = g["door"]["y"] + g["door"]["h"] * 176 / 456
    assert abs((g["pathWall"]["y"] + g["pathWall"]["h"] / 2) - springing) <= 1, "the path is on the door's springing"
    assert all(w >= 180 for w in g["plates"]), g["plates"]
    assert max(g["glossLines"]) <= 5, g["glossLines"]

    g = still(1024, 768)
    maroc, path = g["nodes"][0], g["pathWall"]
    assert abs((maroc["x"] + maroc["w"] / 2) - path["x"]) <= 1.5, "Maroc's disc is centred on the path's start"
    assert abs((maroc["y"] + maroc["h"] / 2) - (path["y"] + path["h"] / 2)) <= 1.5

    for lang in ("fr", "ar"):
        g = still(390, 844, lang)
        # the rail is the start edge of an L-shaped box (the rail, its corner, the floor line to the door)
        rail_x = g["rail"]["r"] if g["rtl"] else g["rail"]["x"]
        assert len(g["nodes"]) == 6
        for node, label in zip(g["nodes"], g["labels"]):
            assert abs((node["x"] + node["w"] / 2) - rail_x) <= 1.5, (lang, "a station's node stands on the rail")
            gap = (node["x"] - label["r"]) if g["rtl"] else (label["x"] - node["r"])
            assert 6 <= gap <= 14, (lang, "the label stands beside its node, clear of the rail", gap)

    # The senior review's M1 (9 October 2026; NOTES.md «Review fixes»). Up to 1535 px the wall needs the page: its four
    # columns are 196 px at 1440 × 900 with the wall at the page's pad. From 1536 px four such columns fit between the
    # container's content edge and the niche, and the hero stands on the page's column: the promise, the first plate,
    # the description and the chapter under it start where the letterhead's logo starts (the promise stood 248 px left
    # of the logo at 1920 × 1080). There the plate is as wide as its column (no sentence runs past its photograph), the
    # row of four fits the hero's height with air under it, and no sentence is over five lines. 1536 × 960 is the cell
    # where the wall caps the niche: its columns are the minimum, 192 px — «Universités & Formation →» needs 187.5 px
    # of column to keep its arrow on its line, and a classic scrollbar (which this browser does not draw) takes 2 px of
    # each column, because the cap is read in vw and the grid in %: at 188 px the word took two lines under one.
    for lang in ("fr", "ar"):
        for width, height in ((1536, 864), (1536, 960), (1920, 1080)):
            g, cell = still(width, height, lang), (lang, width, height)
            edge = g["edges"]["logo"]
            assert edge > 100, cell
            for name in ("promise", "plate", "body", "chapter"):
                assert abs(g["edges"][name] - edge) <= 1.5, (cell, name, g["edges"])
            far = g["niche"]["x"] if g["rtl"] else g["vw"] - g["niche"]["r"]
            assert abs(far) <= 1, (cell, "the niche keeps the far edge of the window")
            for plate, column in zip(g["plateBoxes"], g["columns"]):
                assert abs(plate["w"] - column) <= 1, (cell, "a plate is as wide as its column", plate["w"], column)
                assert 2 / 3 - 0.01 <= plate["h"] / plate["w"] <= 5 / 4 + 0.01, (cell, "between 3 : 2 and 4 : 5")
            assert min(g["columns"]) >= 191.5 and max(g["glossLines"]) <= 5, (cell, g["columns"], g["glossLines"])
            assert max(g["glossTops"]) - min(g["glossTops"]) <= 1, (cell, "the four sentences share a line")
            assert max(tile["b"] for tile in g["tiles"]) <= g["niche"]["b"] - 8, (cell, "the row fits the composition")
            assert g["body"]["y"] >= g["niche"]["b"] - 1, (cell, "the niche stands on the composition's bottom edge")

    # …and at every desktop width the description stands on the page's column, under the composition (below 1536 px
    # the wall keeps the page's pad: the two edges differ there, by design); the four sentences share a line at 1440
    # and at 1280 too — the fourth word and its arrow took two lines (the review's m2).
    for width, height in ((1440, 900), (1280, 800)):
        g = still(width, height)
        assert abs(g["promise"]["x"] - 32) <= 1, (width, "the wall still takes the page")
        assert abs(g["edges"]["body"] - g["edges"]["logo"]) <= 1.5, (width, g["edges"])
        assert abs(g["edges"]["body"] - g["edges"]["chapter"]) <= 1.5, (width, g["edges"])
        assert max(g["glossTops"]) - min(g["glossTops"]) <= 1, (width, "the four sentences share a line")


def test_the_interim_hero_on_a_phone_keeps_its_four_tiles_in_the_first_screen(browser, live_server, seeded):
    """
    Gate G3 closed — what the site shows today: no station may be drawn (the senior review's M3).

    The phone band kept its rail, so half of the night was empty but for an L-shaped gold line, and the taller
    statement (eyebrow, title, lead) pushed the tiles out of the first screen: 2 / 4 at 360 × 800 and 390 × 664, none at
    360 × 640. No rail where there is no station: the door stands in the middle of the band, on the spine's axis, on a
    floor line that runs from pad to pad; the lead is not drawn (the description says it one swipe lower); the door is
    sized by the window's height. On the desktop the lead is read at the reading size.
    """

    def still(width, height, lang="fr"):
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=1, reduced_motion="reduce"
        )
        page = context.new_page()
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        page.wait_for_selector(".he.is-ajar")
        try:
            return page.evaluate(_HERO_GEOMETRY)
        finally:
            context.close()

    cells = ((360, 640, "fr"), (390, 664, "fr"), (360, 800, "fr"), (390, 844, "fr"), (390, 844, "ar"))
    for width, height, lang in cells:
        g, cell = still(width, height, lang), (width, height, lang)
        assert g["variant"] == "interim" and g["nodes"] == [], cell
        lowest = max(tile["b"] for tile in g["tiles"])
        assert len(g["tiles"]) == 4 and lowest <= g["vh"], (cell, "4 / 4 tiles in the first screen", lowest)
        assert abs((g["door"]["x"] + g["door"]["w"] / 2) - g["vw"] / 2) <= 1, (cell, "the door on the spine's axis")
        assert g["railStart"] == "0px", (cell, "no rail without a station: the floor line alone")
        assert abs(g["rail"]["x"] - 16) <= 1 and abs(g["rail"]["r"] - (g["vw"] - 16)) <= 1, (cell, "from pad to pad")
        assert g["lead"]["display"] == "none", (cell, "the lead is not drawn on a phone")
        assert g["hero"]["w"] <= g["vw"], cell

    g = still(1440, 900)
    assert g["lead"]["display"] != "none" and g["lead"]["size"] == "17px", g["lead"]


_PRESSED = "document.querySelector('.he-origin__link').classList.contains('is-pressed')"
_FLOWING = "document.querySelector('[data-he]').classList.contains('is-flowing')"
_PAST_THE_HERO = "window.scrollTo(0, document.querySelector('[data-he]').offsetHeight + 600)"
_FINGER_LOG = """() => {
  window.__log = [];
  const hero = document.querySelector('[data-he]'), tile = document.querySelector('.he-origin__link');
  const note = (what) => window.__log.push([performance.now(), what]);
  for (const type of ['pointerdown', 'pointerup', 'pointercancel']) tile.addEventListener(type, () => note(type), true);
  const watch = (el, name) => new MutationObserver(() => note(name + ':' + el.className))
    .observe(el, { attributes: true, attributeFilter: ['class'] });
  watch(hero, 'hero');
  watch(tile, 'tile');
  document.addEventListener('click', (event) => event.preventDefault(), true);
}"""


def test_a_finger_on_the_tiles_scrolls_without_a_press_and_taps_with_one(browser, live_server, phase3_live):
    """
    A finger on the hero's tiles (touch synthesised through the DevTools protocol; the senior review's M2 and M4).

    The four tiles are the bottom fifth of a phone's first screen, where a thumb starts the scroll: a flick that began
    on one flashed its pressed ground, its chip in colour and a bead on the spine, because the press was set at
    `pointerdown`. It is armed 100 ms after the finger lands — the browser cancels a scroll's pointer sooner — or at
    once when the finger lifts before that: a scroll shows nothing, a tap shows its press and sends its light. And
    where nothing hovers, the hand's short light runs once each time the hero comes back into view.
    """
    context = browser.new_context(
        viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True
    )
    try:
        page = context.new_page()
        # the settled hero of a later load of the session: the first movement is not this test's subject
        page.add_init_script("try { sessionStorage.setItem('ile.hero.discovered', '1'); } catch (e) {}")
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.wait_for_selector(".he.is-ajar.has-replay")
        assert page.evaluate("matchMedia('(hover: none)').matches")
        cdp = context.new_cdp_session(page)
        page.evaluate(_FINGER_LOG)
        box = page.locator(".he-origin__link").first.bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

        # 1 · a scroll that starts on the first tile. The moves follow the touch at once; an attempt counts when the
        # browser cancelled the pointer within 90 ms of its landing (a stalled machine can deliver them later, and
        # the press is then rightly armed: such an attempt proves nothing either way and is made again).
        counted = 0
        for _attempt in range(5):
            page.evaluate("window.__log.length = 0; window.scrollTo(0, 0)")
            page.wait_for_timeout(700)
            cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y, "id": 1}]})
            for step in range(1, 13):
                point = {"x": x, "y": y - 18 * step, "id": 1}
                cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [point]})
            cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
            page.wait_for_timeout(1200)
            log = page.evaluate("window.__log")
            times = {what: at for at, what in reversed(log)}
            if "pointercancel" not in times or times["pointercancel"] - times["pointerdown"] > 90:
                continue
            counted += 1
            assert page.evaluate("scrollY") > 100, "the gesture scrolled the page"
            shown = [what for _at, what in log if "is-pressed" in what or "is-flowing" in what]
            assert shown == [], ("a scroll that starts on a tile shows no press and sends no light", log)
            break
        assert counted, "no scroll gesture was delivered within 90 ms of its touch in five attempts"

        # 2 · a tap: the press and the light at the lift, held while the next page answers (the click is refused here)
        page.evaluate("window.__log.length = 0; window.scrollTo(0, 0)")
        page.wait_for_timeout(1500)
        page.locator(".he-origin__link").first.tap()
        # (a function, not an expression: the page's CSP has no 'unsafe-eval', and a polled expression is eval'd)
        page.wait_for_function(f"() => {_PRESSED} && {_FLOWING}", timeout=3000)
        page.wait_for_function(f"() => !{_PRESSED}", timeout=3000)
        page.wait_for_function(f"() => !{_FLOWING}", timeout=4000)
        assert page.evaluate("document.getAnimations().length") == 0, "the light ends by itself: nothing loops"

        # 3 · the hero leaves the view and comes back: the short light once more, without a touch (M4)
        page.evaluate(_PAST_THE_HERO)
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_function(f"() => {_FLOWING}", timeout=3000)
        page.wait_for_function(f"() => !{_FLOWING}", timeout=4000)
        halo = page.evaluate("getComputedStyle(document.querySelector('.he-key-halo')).opacity")
        assert 0.3 <= float(halo) <= 0.6, ("the key rests softly lit where nothing hovers", halo)
    finally:
        context.close()

    # with a mouse nothing runs when the hero comes back, and the key's halo waits for the hand
    context, page = _page(browser, 1440, 900)
    try:
        page.add_init_script("try { sessionStorage.setItem('ile.hero.discovered', '1'); } catch (e) {}")
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.wait_for_selector(".he.is-ajar.has-replay")
        assert page.evaluate("getComputedStyle(document.querySelector('.he-key-halo')).opacity") == "0"
        page.evaluate(_PAST_THE_HERO)
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(700)
        assert not page.evaluate(_FLOWING)
    finally:
        context.close()


_DOOR_LOADED = (
    "() => { const i = document.querySelector('[data-door-img]'); return i && i.complete && i.naturalWidth > 0; }"
)
_DOOR_FILE = """() => {
  const i = document.querySelector('[data-door-img]');
  return {
    file: Number((i.currentSrc.match(/doorway-arch-([0-9]+)[.]/) || [])[1]),
    told: i.naturalWidth,
    drawn: i.getBoundingClientRect().width,
  };
}"""


def test_the_door_photograph_is_told_its_width(browser, live_server, phase3_live):
    """
    The door's `sizes` say the widest the photograph is drawn, never less.

    The door is the hero's centre and the page's LCP image. Its `sizes` (pages/home/_hero.html, and the preload's
    `imagesizes` in pages/home.html, the same string) once told the width at the BOTTOM of each range of windows:
    the browser took a file too small and stretched it — the 400 px file 2 % at 1366 × 768, the 576 px file 15 % at
    1920 × 1200 and on a 2560 × 1440 screen (design V5.4, W2-D; docs/design-v5/QA/v54/w2-d/NOTES.md §7.9). They now
    follow hero.css rule for rule, and this test holds the two together: a change to the stage's size is a change to
    `sizes`.

    `naturalWidth` of an image chosen by a `w` descriptor is the width `sizes` resolved to (the file's width over its
    density, floored). At density 1 no file may be drawn wider than its own pixels; above it the browser's own rule
    may take a file slightly short of the device's pixels, which is not the page's to decide.
    """
    cells = [
        (1366, 768, 1),  # was told 400 px and drawn 409
        (1440, 799, 1),  # the top of a range: was told 400 px and drawn 425
        (1440, 900, 1),
        (1920, 1200, 1),  # the hero's 64 rem ceiling: was told 576 px and drawn 662
        (1536, 1000, 1),  # from 96 rem the wall caps the niche: the height's line told 545 px, the door is 470
        (1279, 900, 1),  # the compact band: the niche's 40vw decides
        (960, 600, 1.5),  # a small tablet lying down: the short-phone rule alone drew the door 374 px wide
        (844, 390, 3),  # the landscape plinth: 34vh told 133 px, the door is 144
        (390, 844, 3),
    ]
    for width, height, density in cells:
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=density, reduced_motion="reduce"
        )
        page = context.new_page()
        try:
            page.goto(live_server.url + "/fr/", wait_until="networkidle")
            page.wait_for_function(_DOOR_LOADED)
            door = page.evaluate(_DOOR_FILE)
        finally:
            context.close()
        cell = (width, height, density, door)
        assert door["told"] + 1.5 >= door["drawn"], ("the door is drawn wider than its sizes say", cell)
        assert door["told"] <= door["drawn"] * 1.05 + 1.5, ("the door's sizes say far more than it is drawn", cell)
        if density == 1:
            assert door["file"] + 1 >= door["drawn"], ("a file stretched at density 1", cell)
        if width < 1024:
            assert door["drawn"] <= 272.5, ("below the desktop the door keeps the tablets' 17 rem", cell)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_phone_390_phase3_open_including_antifraud(browser, live_server, phase3_live, lang):
    context, page = _page(browser, 390, 844)
    try:
        for path in (*PATHS, "/{lang}/attention-aux-fraudes/"):
            response = page.goto(live_server.url + path.format(lang=lang), wait_until="networkidle")
            assert response.status == 200, (lang, path)
            _assert_fits(page, (lang, path))
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        assert page.locator(".register--entrances .entry").count() == 4
        assert page.locator("[data-section='antifraud']").is_visible()
        # The Morocco → Italy model is said once (W2-D step 3): the hero's path carries six stations — the origin's
        # shore, five steps of the prescribed sequence, the door — and the pilot chapter, which drew the eight
        # steps again as a route between two shores, is a statement with one link (the whole sequence stands on
        # the pilot's own page).
        assert page.locator("[data-section='hero'] .he-station").count() == 6
        assert page.locator("[data-section='pilot']").is_visible()
        assert page.locator("[data-section='pilot'] :is(ol, ul, svg.voyage__svg, .voyage)").count() == 0
        assert page.locator("[data-section='pilot'] a").count() == 1
    finally:
        context.close()


_CHAPTERS = """() => {
  const main = document.querySelector('main');
  const px = (el, p) => parseFloat(getComputedStyle(el)[p]);
  const R = (el) => {
    const b = el.getBoundingClientRect();
    return {x: b.left, r: b.right, y: b.top + scrollY, w: b.width, h: b.height};
  };
  const shown = (el) => {
    const b = el.getBoundingClientRect();
    return b.width > 2 && b.height > 2 && getComputedStyle(el).visibility !== 'hidden';
  };
  const size = (selector) => {
    const el = main.querySelector(selector);
    return el && shown(el) ? px(el, 'fontSize') : null;
  };
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  const start = (el) => (rtl ? R(el).r : R(el).x);
  const chapters = Array.from(main.querySelectorAll(':scope > .chapter')).filter(shown);
  // labels, links and buttons are not what a person reads: they are set at the interface sizes
  const notReading = '.home-section__more, .home-ecosystem__label, .home-ecosystem__more, .gradino__actions, ' +
    '.home-orientation__actions, .card__eyebrow';
  return {
    rtl, vw: document.documentElement.clientWidth, vh: innerHeight, pageH: document.documentElement.scrollHeight,
    chapters: chapters.map((c) => {
      const title = c.querySelector('.section__title:not(.visually-hidden), .gradino__title');
      const head = c.querySelector('.chapter__head, .gradino__head');
      const body = c.querySelector('.chapter__body, .gradino__content');
      return {
        key: c.dataset.section,
        title: title ? px(title, 'fontSize') : null,
        weight: title ? getComputedStyle(title).fontWeight : null,
        head: head ? R(head) : null, body: body ? R(body) : null,
        headStart: head ? start(head) : null, bodyStart: body ? start(body) : null,
      };
    }),
    // a row's title is never smaller than what it titles
    pairs: [
      ['.home-pathways .pathway-list__title', '.home-pathways .pathway-list__desc'],
      ['.home-trust__question', '.home-trust__answer'],
      ['.home-entrances .entry__title', '.home-entrances .entry__gloss'],
      ['.home-entrances .entry__title', '.home-entrances .entry__cta'],
    ].map(([a, b]) => [a, size(a), size(b)]),
    // what a person reads in a chapter: the paragraphs and the glosses
    reading: Array.from(main.querySelectorAll('.chapter p, .chapter .entry__gloss, .home-reserved p'))
      .filter((e) => shown(e) && !e.closest('.he') && !e.matches(notReading))
      .map((e) => px(e, 'fontSize')),
    // black and white rests in the hero only (DL54-12)
    grey: Array.from(main.querySelectorAll('*'))
      .filter((e) => !e.closest('.he') && /grayscale/.test(getComputedStyle(e).filter)).length,
    picturesUnderTheHero: Array.from(main.querySelectorAll('img, picture, video'))
      .filter((e) => !e.closest('.he')).length,
    frenchRuns: Array.from(main.querySelectorAll('.chapter [lang="fr"]'))
      .filter((e) => shown(e) && e.matches('p, h2, h3'))
      .map((e) => getComputedStyle(e).direction),
  };
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_home_under_the_hero_is_one_system(browser, live_server, phase3_live, article_factory, lang):
    """
    The chapters under the hero (design V5.4, W2-D step 3; docs/design-v5/QA/v54/w2-d/NOTES.md §8), on the real page,
    Phase 3, every chapter published.

    One object repeated: a band on its ground, a head at the reading edge, a body. On a desktop every body starts on
    one line — the fifth column of twelve — the anti-fraud plate's paragraph included, and every head on the
    container's edge; the titles are one size (28 px at 600). A row's title is never smaller than what it titles
    (the pathways' titles were 13 px above 15 px descriptions, the questions 13 px above 17 px answers). On a phone
    nothing a person reads is under 16 px. Black and white rests in the hero only: no greyscale and no photograph
    under it. On the Arabic page the chapter mirrors, and a French run keeps its own direction. And the page is
    short: at most eight screens at 1440 × 900 (the home was 7.4 screens with the route and the bar; it is 6.1).
    """

    # the news chapter is on the home once an article is live (the review fix, m4): one is published for this page
    article_factory("Programme du Forum publié")

    def chapters(width, height):
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=1, reduced_motion="reduce"
        )
        page = context.new_page()
        try:
            page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
            fits = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            return page.evaluate(_CHAPTERS), fits
        finally:
            context.close()

    g, fits = chapters(1440, 900)
    assert fits[0] <= fits[1], fits
    keys = [c["key"] for c in g["chapters"]]
    assert keys == ["orientation", "pathways", "pilot", "trust", "antifraud", "news", "ecosystem"], keys
    assert g["rtl"] is (lang == "ar")
    starts = {round(c["bodyStart"]) for c in g["chapters"]}
    assert len(starts) == 1, (
        "every chapter's body starts on one line",
        [(c["key"], c["bodyStart"]) for c in g["chapters"]],
    )
    heads = {round(c["headStart"]) for c in g["chapters"] if c["key"] != "antifraud"}
    assert len(heads) == 1, ("every chapter's head stands on the container's edge", heads)
    assert {c["title"] for c in g["chapters"]} == {28.0} and {c["weight"] for c in g["chapters"]} == {"600"}
    for c in g["chapters"]:
        assert c["head"]["w"] < c["body"]["w"], (c["key"], "the head is the narrow column")
    for selector, title, text in g["pairs"]:
        if title is not None and text is not None:
            assert title >= text, (selector, title, text)
    assert g["grey"] == 0 and g["picturesUnderTheHero"] == 0
    assert g["pageH"] <= 8 * g["vh"], (g["pageH"], "a short home: at most eight screens at 1440 × 900")
    if lang == "ar":
        runs = g["frenchRuns"]
        assert runs and set(runs) == {"ltr"}, "a French run on the Arabic page reads left to right"

    g, fits = chapters(390, 844)
    assert fits[0] <= fits[1], fits
    assert [c["key"] for c in g["chapters"]][0] == "entrances", "on a phone the register opens the chapters"
    sizes = sorted(set(g["reading"]))
    assert sizes and sizes[0] >= 16, ("nothing a person reads on a phone is under 16 px", sizes)
    for selector, title, text in g["pairs"]:
        if title is not None and text is not None:
            assert title >= text, (selector, title, text)
    for c in g["chapters"]:
        if c["head"] and c["body"]:
            stacked = c["body"]["y"] >= c["head"]["y"] + c["head"]["h"] - 1
            assert stacked, (c["key"], "on a phone the head stands above its body")
    assert g["grey"] == 0 and g["picturesUnderTheHero"] == 0
