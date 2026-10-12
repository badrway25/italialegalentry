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
        # No photograph is requested: the plate is typographic until a captioned image exists
        # (a <figure> without a <figcaption> is a defect — art direction A §6.2).
        assert [u for u in requests if "/static/img/photos/" in u] == []
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
        hero_bottom = page.evaluate("document.querySelector('.hero').getBoundingClientRect().bottom")
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
        assert page.locator(".register--entrances").is_visible()
    finally:
        context.close()


def test_the_four_entrances_are_a_quay_and_the_dark_chapters_are_deliberate(browser, live_server, seeded):
    """
    The four entrances are not four identical cards, and the dark grounds are not scattered.

    Both halves of this test outlive the art direction that first wrote them; only their shapes
    changed. The entrances were four columns side by side, each with its own line drawing — the
    banned pattern twice over, applied to the four most important links on the site. They became a
    stacked register, and on 24 September 2026 a QUAY OF FOUR PIERS (DESIGN_SYSTEM_V2.md §8.5): a
    zig-zag of two rows on the twelve-column grid, 7/5 then 5/7, each pier with its own index,
    landform glyph, tint and mooring line. What is still forbidden is what was always forbidden —
    four boxes of the same width, in the same row, telling the reader nothing about which door is
    theirs. On a phone they stack, because a list is what survives 320px.

    The ground change was "exactly one navy band per page". The V2 principle is the same rule with
    a number that fits an immersive page: at most two midnight chapters on HOME and FORUM, at most
    one anywhere else, and they begin and end at a section boundary. Two on the home, the hero and
    the pilot route, is the ceiling — not an invitation.
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
        assert len({p["top"] for p in piers}) == 2, "a quay is two rows of two"
        assert piers[0]["top"] == piers[1]["top"] and piers[2]["top"] == piers[3]["top"]
        # The zig-zag: within each row the widths differ, and the long one alternates sides.
        assert piers[0]["width"] > piers[1]["width"], "row 1 runs long then short"
        assert piers[2]["width"] < piers[3]["width"], "row 2 runs short then long"

        chapters = page.locator(".chapter--dark").count()
        assert chapters <= 2, f"at most two midnight chapters on an immersive page, found {chapters}"
        first = page.evaluate("document.querySelector('.chapter--dark')?.getAttribute('data-section')")
        assert first == "hero", "the first midnight chapter is the hero"
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
        # The prescribed eight-step sequence, now drawn as the route between two shores
        # (DESIGN_SYSTEM_V2.md §8.6) instead of a row of circles: still eight, still an ordered
        # list, still in the prescribed order. The class changed; the contract did not.
        assert page.locator("[data-section='pilot'] .voyage__step").count() == 8
    finally:
        context.close()
