"""
RTL check of the navbar, part 2 (design V5, V5.4 plan §1.12 item 8, acceptance N19 and O5; W2-C2).

What no static guard can see (plan §2.5): the sheet is the overlay system's modal drawer, and a drawer mirrors — from
48rem the side sheet slides in from the inline end, the LEFT in Arabic, and leaves by it; on a phone the sheet's
«Quiet» rise is vertical and does not mirror (O5: «drawers mirror; sheets do not»); its rows read from the right —
the disc at the inline start, the chevron at the inline end; and the signed-in targa's account popover hangs on the
trigger's inline end, its left edge on the trigger's left edge (N19: «menus aligned on the inline end»).
Chromium on the Arabic home, gate G3 open.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

MENU = "[data-nav-toggle]"


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
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _open(browser, width, height, **kwargs):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **kwargs)
    return context, context.new_page()


def test_in_arabic_the_side_sheet_comes_and_goes_by_the_left(browser, live_server, seeded, four_doors):
    context, page = _open(browser, 768, 1024, has_touch=True)
    try:
        page.goto(f"{live_server.url}/ar/", wait_until="load")
        assert page.evaluate("document.documentElement.dir") == "rtl"
        page.tap(MENU)
        rights = page.evaluate(
            """async () => { const s = document.getElementById('nav-sheet'), out = [];
              for (let i = 0; i < 6; i++) { await new Promise((r) => setTimeout(r, 40)); out.push(Math.round(s.getBoundingClientRect().right)); }
              return out; }"""
        )
        page.wait_for_timeout(300)
        box = page.evaluate(
            "(() => { const b = document.getElementById('nav-sheet').getBoundingClientRect(); return [b.left, b.right].map(Math.round); })()"
        )
        assert box[0] == 0 and 416 <= box[1] <= 428, box
        assert rights[0] < rights[-1] <= box[1] + 2 and rights == sorted(rights), f"in from the left: {rights}"
        page.mouse.click(700, 600)  # the scrim, on the right of the sheet
        out = page.evaluate(
            """async () => { const s = document.getElementById('nav-sheet'), out = [];
              for (let i = 0; i < 4; i++) { await new Promise((r) => setTimeout(r, 35)); const b = s.getBoundingClientRect(); out.push(b.width ? Math.round(b.right) : null); }
              return out; }"""
        )
        moving = [right for right in out if right is not None]
        assert moving and moving == sorted(moving, reverse=True) and moving[-1] < box[1], f"out by the left: {out}"
        page.wait_for_timeout(300)
        assert not page.evaluate("document.getElementById('nav-sheet').open")
    finally:
        context.close()


def test_in_arabic_the_phone_sheet_rises_without_travelling_sideways(browser, live_server, seeded, four_doors):
    context, page = _open(browser, 390, 844, has_touch=True)
    try:
        page.goto(f"{live_server.url}/ar/", wait_until="load")
        page.tap(MENU)
        frames = page.evaluate(
            """async () => { const s = document.getElementById('nav-sheet'), b = s.querySelector('.nav-sheet__body'), out = [];
              for (let i = 0; i < 6; i++) { out.push([Math.round(s.getBoundingClientRect().left), getComputedStyle(b).translate]); await new Promise((r) => setTimeout(r, 40)); }
              return out; }"""
        )
        assert {left for left, _ in frames} == {0}, frames
        for _, translate in frames:
            assert translate == "none" or translate.startswith("0px "), frames
        page.wait_for_timeout(400)
        # the rows read from the right: the disc at the inline start, the chevron at the inline end
        row = page.evaluate(
            """() => { const s = document.querySelector('#nav-sheet .nav-sheet__item--door summary'), r = (q) => s.querySelector(q).getBoundingClientRect();
              const word = s.children[1].getBoundingClientRect();
              return {disc: [r('.portico__disc').left, r('.portico__disc').right], word: [word.left, word.right], chevron: [r('.nav-sheet__chevron').left, r('.nav-sheet__chevron').right]}; }"""
        )
        assert row["disc"][0] >= row["word"][1] - 0.5 and row["chevron"][1] <= row["word"][0] + 0.5, row
        assert row["disc"][1] <= 390 - 16 + 0.5, row
    finally:
        context.close()


def test_in_arabic_the_account_popover_hangs_on_the_inline_end(browser, live_server, seeded, four_doors, person_user):
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(person_user)  # nothing typed, no password used
    context, page = _open(browser, 1440, 900)
    try:
        context.add_cookies(
            [
                {
                    "name": settings.SESSION_COOKIE_NAME,
                    "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
                    "url": live_server.url,
                }
            ]
        )
        page.goto(f"{live_server.url}/ar/", wait_until="load")
        # the trigger sits on the row's middle: its wrapper is a flex box, not a block that takes Vazirmatn's 32 px
        # strut and set it 2 px high (REVIEW m6)
        middles = page.evaluate(
            """() => { const m = (e) => { const b = e.getBoundingClientRect(); return (b.top + b.bottom) / 2; };
              return [m(document.querySelector('.site-header__end .account-menu__summary')), m(document.querySelector('.site-header__inner'))]; }"""
        )
        assert abs(middles[0] - middles[1]) <= 0.5, middles
        page.locator(".site-header__end .account-menu__summary").click()
        page.wait_for_timeout(350)
        edges = page.evaluate(
            """() => { const t = document.querySelector('.site-header__end .account-menu__summary').getBoundingClientRect();
              const p = document.getElementById('account-menu').getBoundingClientRect();
              return {trigger: [t.left, t.right], panel: [p.left, p.right], dir: getComputedStyle(document.getElementById('account-menu')).direction}; }"""
        )
        assert abs(edges["panel"][0] - edges["trigger"][0]) <= 1 and edges["panel"][1] > edges["trigger"][1], edges
        assert edges["dir"] == "rtl", edges
    finally:
        context.close()
