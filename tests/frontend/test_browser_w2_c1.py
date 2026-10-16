"""
«Il portico» — the behaviour checks of NAVIGATION.md §9.3 ported to the product (design V5, V5.4 plan §1.12; W2-C1).

The keyboard model, hover intent and the pin, the safe triangle (doors 2–4: the open panel holds along the straight
path from the door to its first entry, the travel reported in px), the photographs' loading policy (nothing before
`load`, four at idle from 80rem, never on a phone), the no-script fallback (a door opens on hover; below 80rem the
sheet shows in place: G-04), and WCAG 2.4.11 under the sticky letterhead. Chromium on the French home with the static fallback
menu, gate G3 open so that the four doors are in the bar.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DOOR = "[data-portico-door]"
OPEN = f"{DOOR}[aria-expanded='true']"

#: The letterhead's fit, read from the rendered boxes (the review's M1 and M2 measured document overflow only, which
#: stays 0 while the viewport has room; the finding was the end zone past the CONTENT COLUMN).
FIT_JS = """async () => {
  await document.fonts.ready;
  const rect = (e) => e.getBoundingClientRect();
  const inner = document.querySelector('.site-header__inner');
  const cs = getComputedStyle(inner);
  const ib = rect(inner);
  const rtl = document.documentElement.dir === 'rtl';
  const colEnd = rtl ? ib.left + parseFloat(cs.paddingLeft) : ib.right - parseFloat(cs.paddingRight);
  const end = rect(document.querySelector('.site-header__end'));
  const tops = [...document.querySelectorAll('.main-nav[data-portico] .main-nav__link')].filter((e) => e.getClientRects().length).map(rect);
  const label = document.querySelector('.site-header__end .targa__label');
  const name = document.querySelector('.targa-seat .account-menu__name');
  const chrome = [...document.querySelectorAll('.site-header__inner > a, .main-nav[data-portico] .main-nav__link, .site-header__end > *')].filter((e) => e.getClientRects().length).map(rect);
  return {
    // + = the end zone sticks out past the column's inline-end edge; 0 = it sits on it
    past: +(rtl ? colEnd - end.left : end.right - colEnd).toFixed(1),
    rows: new Set(tops.map((r) => Math.round(r.top))).size,
    items: tops.length,
    headerH: rect(document.querySelector('.site-header')).height,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    outOfViewport: chrome.filter((r) => r.right > innerWidth + 0.5 || r.left < -0.5).length,
    label: Boolean(label) && rect(label).width > 2,
    seat: Boolean(document.querySelector('.targa-seat .account-menu__summary')),
    nameShown: Boolean(name) && rect(name).width > 2,
  };
}"""
TEXT_SPACING = (
    "* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }"
    " p { margin-block-end: 2em !important; }"
)


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
def four_doors(set_flag, monkeypatch, legal_published):
    """Gate G3 open for the live server WITHOUT freezegun (a frozen ``time.monotonic`` stalls Playwright): every
    publication decision goes through ``core.clock.now()``, so patching it is enough. The task links of the
    Institutions and Universités doors are public forms, open once the legal pages are published."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _open(browser, width=1440, height=900, **kwargs):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **kwargs)
    return context, context.new_page()


def _active(page) -> str:
    return page.evaluate("(document.activeElement.textContent || '').trim()")


def _open_door(page):
    return page.evaluate("(document.querySelector('[data-portico-door][aria-expanded=\"true\"]') || {textContent: ''}).textContent.trim()")


def _scrim_shown(page) -> bool:
    return page.evaluate("!document.querySelector('[data-portico-scrim]').hidden")


def test_the_keyboard_model_of_the_portico(browser, live_server, seeded, four_doors):
    context, page = _open(browser)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        doors = page.locator(DOOR)
        assert doors.count() == 5, "four doors and «Projet» as sections"
        history = page.evaluate("history.length")
        labels = [doors.nth(i).text_content().strip() for i in range(doors.count())]
        # ← → move without opening; Home / End reach the ends of the bar
        doors.nth(0).focus()
        page.keyboard.press("ArrowRight")
        assert _active(page) == labels[1] and not _open_door(page)
        page.keyboard.press("End")
        assert _active(page) == "Projet"
        page.keyboard.press("Home")
        assert _active(page) == labels[0]
        # ↓ opens and enters, instantly, with the scrim (a keyboard open)
        page.keyboard.press("ArrowDown")
        assert _open_door(page) == labels[0] and _scrim_shown(page)
        assert page.evaluate("document.activeElement.classList.contains('portico__link')")
        first_entry = _active(page)
        # ↓ ↑ walk the entries; ↑ on the first returns to the door and leaves the panel open
        page.keyboard.press("ArrowDown")
        assert _active(page) != first_entry
        page.keyboard.press("ArrowUp")
        page.keyboard.press("ArrowUp")
        assert _active(page) == labels[0] and _open_door(page) == labels[0]
        # End / Home inside the panel: last / first link
        page.keyboard.press("ArrowDown")
        page.keyboard.press("End")
        assert page.evaluate("document.activeElement.closest('[data-portico-panel]') !== null")
        assert _active(page) != first_entry
        page.keyboard.press("Home")
        assert _active(page) == first_entry
        # → with a panel open switches the door — from inside the panel too
        page.keyboard.press("ArrowRight")
        assert _active(page) == labels[1] and _open_door(page) == labels[1]
        # Esc closes, returns the focus to the door, removes the scrim
        page.keyboard.press("Escape")
        assert not _open_door(page) and _active(page) == labels[1] and not _scrim_shown(page)
        # Enter toggles the disclosure and keeps the focus on the door; Tab walks into the open panel
        page.keyboard.press("Enter")
        assert _open_door(page) == labels[1] and _active(page) == labels[1]
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.closest('[data-portico-panel]') !== null")
        page.keyboard.press("Enter") if False else None
        # focus leaving the navigation closes the panel (WCAG 1.4.13); nothing was pushed on the history
        for _ in range(40):
            page.keyboard.press("Tab")
            if not page.evaluate("document.querySelector('[data-portico]').contains(document.activeElement)"):
                break
        assert not _open_door(page)
        assert page.evaluate("history.length") == history
        # ↑ on a door never scrolls the page
        page.evaluate("window.scrollTo(0, 300)")
        doors.nth(0).focus()
        page.keyboard.press("ArrowUp")
        assert page.evaluate("window.scrollY") >= 300 - 1
    finally:
        context.close()


def test_hover_intent_and_the_pin(browser, live_server, seeded, four_doors):
    """Open after 120 ms of intent, no scrim on a hover, a click pins what the hover opened, closed after a grace
    once the pointer has left (plan §1.12 item 6)."""
    context, page = _open(browser)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        door = page.locator(DOOR).first
        box = door.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(40)
        assert not _open_door(page), "nothing opens before the intent delay"
        page.wait_for_timeout(300)
        assert _open_door(page) == door.text_content().strip()
        assert not _scrim_shown(page), "a hover never shows the scrim"
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(100)
        assert _open_door(page) and _scrim_shown(page), "a click pins a hover-opened panel and gives it its scrim"
        page.mouse.move(720, 860)
        page.wait_for_timeout(500)
        assert _open_door(page), "a pinned panel stays open when the pointer leaves"
        page.keyboard.press("Escape")
        assert not _open_door(page)
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(350)
        assert _open_door(page)
        page.mouse.move(720, 860)
        page.wait_for_timeout(100)
        assert _open_door(page), "still open inside the grace"
        page.wait_for_timeout(400)
        assert not _open_door(page), "closed after the grace"
    finally:
        context.close()


def test_the_safe_triangle_holds_for_doors_two_to_four(browser, live_server, seeded, four_doors):
    """Doors 2–4 sit away from their entries (the column starts at the first door): along the straight path from the
    door to its first entry the pointer crosses other doors, and the open panel must hold (plan §1.12 change 1).
    The travel is reported in px in the assertion."""
    context, page = _open(browser)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        doors = page.locator(DOOR)
        travels = {}
        for index in (1, 2, 3):
            door = doors.nth(index)
            label = door.text_content().strip()
            box = door.bounding_box()
            sx, sy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            page.mouse.move(sx, sy)
            page.wait_for_timeout(350)
            assert _open_door(page) == label
            entry = page.locator(f"#{door.get_attribute('aria-controls')} .portico__link").first.bounding_box()
            ex, ey = entry["x"] + 24, entry["y"] + entry["height"] / 2
            steps = 14
            for step in range(1, steps + 1):
                page.mouse.move(sx + (ex - sx) * step / steps, sy + (ey - sy) * step / steps)
                page.wait_for_timeout(16)
            page.wait_for_timeout(300)
            travels[label] = round(((ex - sx) ** 2 + (ey - sy) ** 2) ** 0.5)
            assert _open_door(page) == label, f"the panel switched on the way to its first entry ({label}, travel {travels[label]} px)"
            assert page.evaluate("document.activeElement.tagName") != "A"
            page.mouse.move(720, 860)
            page.wait_for_timeout(450)
            assert not _open_door(page)
        assert all(travel > 48 for travel in travels.values()), travels  # doors 2–4 need the triangle, door 1 does not
        print(f"\nsafe-triangle travel (px): {travels}")
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_the_letterhead_holds_its_column_at_every_desktop_width(
    browser, live_server, seeded, four_doors, person_user, lang
):
    """The review's M1: the end zone's inline-end edge sits on the content column's edge — never past it — at 1280,
    1366, 1440, 1512, 1600 and 1920, the six items on one row, signed out and signed in; the plate's label and the
    signed-in name appear only from 100rem, where the measured room allows them (chrome.css §4, §6). The signed-in
    pages use a session minted with ``Client.force_login`` for the fixture's person: nothing typed, no password used."""
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(person_user)
    session = {
        "name": settings.SESSION_COOKIE_NAME,
        "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
        "url": live_server.url,
    }
    for signed_in, widths in ((False, (1280, 1366, 1440, 1512, 1600, 1920)), (True, (1280, 1440, 1600))):
        context, page = _open(browser, 1440, 900)
        try:
            if signed_in:
                context.add_cookies([session])
            for width in widths:
                page.set_viewport_size({"width": width, "height": 900})
                page.goto(live_server.url + f"/{lang}/", wait_until="load")
                fit = page.evaluate(FIT_JS)
                where = f"{lang} {width}px {'signed in' if signed_in else 'signed out'}"
                assert fit["items"] == 6 and fit["rows"] == 1, (where, fit)
                assert fit["past"] <= 0.5, f"the end zone runs {fit['past']} px past the content column ({where})"
                assert fit["scrollWidth"] == fit["clientWidth"] and fit["outOfViewport"] == 0, (where, fit)
                assert fit["seat"] is signed_in, (where, fit)
                shown = fit["nameShown"] if signed_in else fit["label"]
                assert shown is (width >= 1600), f"the label / the name is shown exactly from 100rem ({where}: {fit})"
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_bar_wraps_under_text_spacing_and_never_clips(browser, live_server, seeded, four_doors, lang):
    """WCAG 1.4.12 (plan §1.12 item 9): under the standard text-spacing sheet the bar wraps — the letterhead grows by
    one row — or holds; nothing of the chrome leaves the viewport and the page never scrolls sideways (the review's
    M2 and the a11y/perf check's finding 1: 1 600 px of scrollWidth at 1440 in French)."""
    for width in (1024, 1280, 1440):
        context, page = _open(browser, width, 800, bypass_csp=True)
        try:
            page.goto(live_server.url + f"/{lang}/", wait_until="load")
            page.add_style_tag(content=TEXT_SPACING)
            page.wait_for_timeout(250)
            fit = page.evaluate(FIT_JS)
            where = f"{lang} {width}px under text spacing"
            assert fit["scrollWidth"] == fit["clientWidth"], f"the page scrolls sideways ({where}: {fit})"
            assert fit["outOfViewport"] == 0 and fit["past"] <= 0.5, (where, fit)
            assert fit["rows"] in (1, 2), (where, fit)
            assert fit["headerH"] >= 64, (where, fit)
        finally:
            context.close()


def test_the_photographs_follow_the_loading_policy(browser, live_server, seeded, four_doors):
    """Nothing before `load`; the four at idle after it, from 80rem only; never on a phone (plan §1.12 item 4)."""
    for width, height, expected_after_idle in ((1440, 900, 4), (1024, 768, 0), (390, 844, 0)):
        context, page = _open(browser, width, height)
        try:
            requests: list[str] = []
            page.on("request", lambda r: requests.append(r.url))
            # the load event goes into the same ordered stream: goto() returns a moment after it, and the idle
            # callback may already have asked for the photographs in between (regression-1, 10 Oct, at 1440)
            page.on("load", lambda: requests.append("LOAD"))
            page.goto(live_server.url + "/fr/", wait_until="load")
            before = [u for u in requests[: requests.index("LOAD")] if "/img/portico/" in u]
            assert before == [], (width, before)
            page.wait_for_timeout(3500)
            after = [u for u in requests if "/img/portico/" in u]
            assert len(after) == expected_after_idle, (width, after)
            if expected_after_idle:
                assert all(u.endswith("-640.webp") for u in after), after
        finally:
            context.close()


def test_without_script_a_door_opens_on_hover_and_the_sheet_opens_in_place(browser, live_server, seeded, four_doors):
    """The CSS fallback (NAVIGATION §4.8, four checks): a panel opens on :hover and :focus-within, its entries are
    reachable links. Below 80rem «Menu» is a link to the sheet, which shows in place (:target) over a letterhead that
    holds nothing but its row — so a sticky header never hides the page (G-04 closed) — and «Fermer» is a link back
    (W2-C2, the overlay system's no-script path)."""
    context, page = _open(browser, java_script_enabled=False)
    try:
        page.goto(live_server.url + "/fr/", wait_until="load")
        assert page.evaluate("document.documentElement.classList.contains('no-js')")
        door = page.locator(DOOR).first
        panel = page.locator(f"#{door.get_attribute('aria-controls')}")
        assert not panel.is_visible()
        door.hover()
        page.wait_for_timeout(100)
        assert panel.is_visible(), "without the module a door still opens on hover"
        assert panel.locator("a[href]").count() >= 2
        page.mouse.move(720, 860)
        page.wait_for_timeout(400)  # the panel leaves through its 120 ms display transition (allow-discrete)
        assert not panel.is_visible()
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(live_server.url + "/fr/", wait_until="load")
        header = page.evaluate(
            "(() => { const h = document.querySelector('.site-header'); return {position: getComputedStyle(h).position, height: h.getBoundingClientRect().height}; })()"
        )
        assert header["height"] < 844 / 2, header
        sheet = page.locator("#nav-sheet")
        assert not sheet.is_visible()
        page.locator("[data-nav-toggle]").click()
        page.wait_for_timeout(200)
        assert page.evaluate("location.hash") == "#nav-sheet" and sheet.is_visible(), "the sheet shows in place"
        assert sheet.locator("a[href]").first.is_visible()
        sheet.locator("summary").first.click()
        assert page.evaluate("document.querySelector('#nav-sheet details').open"), "a door unfolds without script"
        sheet.locator(".nav-sheet__head .nav-toggle").click()
        page.wait_for_timeout(200)
        assert not sheet.is_visible(), "«Fermer» is a link back"
    finally:
        context.close()


def test_focus_is_not_obscured_by_the_sticky_letterhead(browser, live_server, seeded, four_doors):
    """WCAG 2.4.11 under the V5 bars (plan §1.6): a link focused from below the fold scrolls into view under the
    letterhead, not beneath it — the CSS-native scroll padding is measured, so focus-clear.js stays unwritten."""
    context, page = _open(browser)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(200)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(200)
        result = page.evaluate(
            """() => {
                const links = [...document.querySelectorAll('main a[href]')].filter(a => a.getClientRects().length);
                const target = links.find(a => a.getBoundingClientRect().top > innerHeight + 200);
                if (!target) return null;
                target.focus();
                const r = target.getBoundingClientRect();
                const header = document.querySelector('.site-header').getBoundingClientRect();
                return {top: r.top, headerBottom: header.bottom, text: target.textContent.trim().slice(0, 40)};
            }"""
        )
        assert result, "no link below the fold to focus"
        assert result["top"] >= result["headerBottom"], result
    finally:
        context.close()
