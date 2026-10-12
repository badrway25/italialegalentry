"""
The icon system in the browser — what the review's fix pass changed, held where a static test cannot see it
(design V5, V5.4 plan §1.7; W1-B; docs/design-v5/QA/v54/w1-b/NOTES.md «Review fixes»).

* Review M1 — the console rail, its bottom bar and its drawer draw the registry's symbol for every entry, at or above
  the symbol's floor.
* Review M2 and M3 — an empty state draws the glyph of its space, or the neutral mark `empty` when it has none
  (never `document` by default), with the one hand's 1.5 px stroke.
* The a11y check of «Il portico» (finding 7, handed to the icon system) — under forced colours every icon is the ink
  of the text beside it, whatever rule coloured it, and paints no ground of its own.

Chromium on the seeded site, gate G3 open (the live server without freezegun, as tests/i18n/test_rtl_browser.py).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

from core import icons

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: Every visible sprite icon of the page: its symbol, the size the glyph is DRAWN at (the svg's content box: the
#: empty state pads its glyph into a disc), its stroke, its own ground, the colour of the element that holds it (the
#: text beside it), the link it sits in and which part of the console's shell holds it.
ICONS_JS = """() => {
  const shown = (el) => { for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = getComputedStyle(n); if (s.display === 'none' || s.visibility === 'hidden') return false; } return true; };
  const px = (v) => parseFloat(v) || 0;
  return [...document.querySelectorAll('svg.icon')].filter((svg) => svg.querySelector('use') && shown(svg)
      && svg.getBoundingClientRect().width > 0).map((svg) => {
    const cs = getComputedStyle(svg); const box = svg.getBoundingClientRect();
    const w = box.width - px(cs.paddingLeft) - px(cs.paddingRight) - px(cs.borderLeftWidth) - px(cs.borderRightWidth);
    const h = box.height - px(cs.paddingTop) - px(cs.paddingBottom) - px(cs.borderTopWidth) - px(cs.borderBottomWidth);
    const link = svg.closest('a[href]');
    return {id: svg.querySelector('use').getAttribute('href').split('#icon-')[1], cls: svg.getAttribute('class'),
            size: Math.min(w, h), stroke: cs.stroke, strokeWidth: cs.strokeWidth, ground: cs.backgroundColor,
            text: getComputedStyle(svg.parentElement).color, href: link ? link.getAttribute('href') : '',
            where: svg.closest('dialog.console-drawer') ? 'drawer' : svg.closest('nav.console-bottom') ? 'bottom'
                 : svg.closest('nav.rail [data-rail-item]') ? 'rail' : ''};
  });
}"""
TRANSPARENT = ("rgba(0, 0, 0, 0)", "transparent")


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
def site(live_server, seeded, legal_published, set_flag, monkeypatch):
    """The seeded site with gate G3 open, WITHOUT freezegun (a frozen ``time.monotonic`` stalls Playwright): every
    publication decision goes through ``core.clock.now()``, so patching it is enough."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield live_server.url
    flags.invalidate()


def _session(user, site: str) -> dict:
    """A session minted with ``Client.force_login``: nothing typed, no password used."""
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(user)
    return {"name": settings.SESSION_COOKIE_NAME, "value": client.cookies[settings.SESSION_COOKIE_NAME].value, "url": site}


def _at_its_floor(icon: dict) -> bool:
    return icon["size"] + 0.01 >= icons.MIN_SIZE[icon["id"]]


def test_the_rail_the_bottom_bar_and_the_drawer_draw_the_registrys_symbols(browser, site, person_user):
    from portal import services as portal_services

    entries = portal_services.navigation(person_user)
    expected = {entry["url"]: icons.NAV[entry["key"]] for entry in entries}
    assert set(expected.values()) >= {"ile-steps", "folder", "document", "concierge-bell", "book-open"}
    on_the_bar = {entry["url"] for entry in entries if entry["bottom"]}

    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        context.add_cookies([_session(person_user, site)])
        page = context.new_page()
        page.goto(site + "/fr/espace-reserve/", wait_until="networkidle")
        rail = [icon for icon in page.evaluate(ICONS_JS) if icon["where"] == "rail"]
        assert {icon["href"]: icon["id"] for icon in rail} == expected, "the rail, entry by entry"
        for icon in rail:
            assert _at_its_floor(icon) and icon["strokeWidth"] == "1.5px", icon

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(site + "/fr/espace-reserve/", wait_until="networkidle")
        # «Menu» is a link too since W3-A's phone chrome (`#console-drawer`: it leads to the drawer without
        # script): the bar's ENTRIES are the links to a page
        bar = [
            icon
            for icon in page.evaluate(ICONS_JS)
            if icon["where"] == "bottom" and icon["href"] and not icon["href"].startswith("#")
        ]
        assert {icon["href"] for icon in bar} == on_the_bar, "the bottom bar's four entries"
        for icon in bar:
            assert icon["id"] == expected[icon["href"]] and _at_its_floor(icon), icon

        page.click("nav.console-bottom [data-console-menu]")
        page.wait_for_selector("dialog.console-drawer[open]")
        drawer = [icon for icon in page.evaluate(ICONS_JS) if icon["where"] == "drawer" and icon["href"] in expected]
        assert {icon["href"]: icon["id"] for icon in drawer} == expected, "the drawer, entry by entry"
        assert all(_at_its_floor(icon) for icon in drawer), drawer
    finally:
        context.close()


def test_an_empty_state_draws_its_space_or_the_neutral_mark_with_the_one_hand(browser, site):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page = context.new_page()
        for path, symbol in (("/fr/partenaires/", icons.EMPTY_STATE), ("/fr/actualites/", "newspaper")):
            page.goto(site + path, wait_until="networkidle")
            marks = [icon for icon in page.evaluate(ICONS_JS) if "empty-state__icon" in icon["cls"]]
            assert [icon["id"] for icon in marks] == [symbol], (path, marks)
            assert marks[0]["strokeWidth"] == "1.5px", "the empty state's glyph is drawn by the .icon rule, like every other"
            assert marks[0]["size"] >= 24 and _at_its_floor(marks[0]), (path, marks[0])
        assert icons.EMPTY_STATE != "document"
    finally:
        context.close()


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_under_forced_colours_every_icon_is_the_ink_of_its_text(browser, site, scheme):
    """A browser gives <svg> ``forced-color-adjust: preserve-parent-color``: an icon whose component colours it
    kept its authored hex under forced colours (the home's navy arrows at 1.4 : 1 on a dark canvas, the footer's
    night ink at 1.8 : 1 on a light one). The .icon rule inherits again there, and drops any ground of its own."""
    plain = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, color_scheme=scheme)
    try:
        page = plain.new_page()
        page.goto(site + "/fr/", wait_until="networkidle")
        drawn = page.evaluate(ICONS_JS)
        assert [icon for icon in drawn if icon["stroke"] != icon["text"]], (
            "the home has icons coloured by their own component: the check below has something to hold"
        )
        # the disc: an empty state's glyph on its own ground. The home drew one while it announced an empty news
        # chapter; it draws that chapter only once an article is live (W2-D review fix, m4), so the disc is read
        # where it stands — on the news' own page.
        page.goto(site + "/fr/actualites/", wait_until="networkidle")
        assert [icon for icon in page.evaluate(ICONS_JS) if icon["ground"] not in TRANSPARENT], (
            "and one that paints its own disc (the news' empty state)"
        )
    finally:
        plain.close()
    forced = browser.new_context(
        viewport={"width": 1440, "height": 900}, device_scale_factor=1, forced_colors="active", color_scheme=scheme
    )
    try:
        page = forced.new_page()
        page.goto(site + "/fr/", wait_until="networkidle")
        assert page.evaluate("matchMedia('(forced-colors: active)').matches")
        drawn = page.evaluate(ICONS_JS)
        assert len(drawn) >= 20, len(drawn)
        off = [icon for icon in drawn if icon["stroke"] != icon["text"]]
        assert off == [], f"{len(off)} icon(s) keep an authored colour under forced colours: {off[:3]}"
        grounds = [icon for icon in drawn if icon["ground"] not in TRANSPARENT]
        assert grounds == [], f"an icon paints a ground of its own under forced colours: {grounds[:3]}"
        page.goto(site + "/fr/actualites/", wait_until="networkidle")
        discs = [icon for icon in page.evaluate(ICONS_JS) if "empty-state__icon" in icon["cls"]]
        assert len(discs) == 1, "the news' empty state is on the page"
        assert discs[0]["ground"] in TRANSPARENT and discs[0]["stroke"] == discs[0]["text"], discs[0]
    finally:
        forced.close()
