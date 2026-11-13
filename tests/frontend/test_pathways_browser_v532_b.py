"""
V5.32 lane B — the Espace Personnes in a browser (the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION, 12 Nov 2026).

Chromium, gate G3 open through the clock: «l'esploratore» previews the pathway a row points at or is focused on, from
64 rem (and never moves the focus or the page); below 64 rem, and without script, there is no preview and every row
shows its line; no page of the space is wider than its viewport (1440, 1024, 768, 390; French and Arabic); the sheet's
local navigation stays in reach while the chapters scroll and marks the chapter in view, and below 64 rem its sticky
bar never hides the control the keyboard focuses, nor the chapter an anchor brings in (WCAG 2.4.11).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PAGES = ("/{lang}/parcours/", "/{lang}/parcours/salaried_work/", "/{lang}/diplomes-et-titres/", "/{lang}/formation/")


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
def phase3(set_flag, monkeypatch):
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_page_of_the_space_is_wider_than_its_viewport(browser, live_server, seeded, phase3, lang):
    for width in (1440, 1024, 768, 390):
        context = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        try:
            for path in PAGES:
                page.goto(live_server.url + path.format(lang=lang), wait_until="load")
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                assert overflow <= 0, (path, lang, width, overflow)
            assert errors == [], (lang, width, errors)
        finally:
            context.close()


def test_the_explorer_previews_the_row_pointed_at_or_focused(browser, live_server, seeded, phase3):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/parcours/", wait_until="load")
        page.wait_for_selector("[data-esplora][data-esplora-pronto]")
        shown = "() => [...document.querySelectorAll('[data-esplora-anteprima]')].filter((c) => !c.hidden).map((c) => c.dataset.esploraAnteprima)"
        assert page.evaluate(shown) == ["salaried_work"]
        assert page.locator(".esplora__anteprime").is_visible()
        page.hover("[data-esplora-voce='scientific_research']")
        page.wait_for_timeout(250)
        assert page.evaluate(shown) == ["scientific_research"]
        page.focus("[data-esplora-voce='family_reunification']")
        assert page.evaluate(shown) == ["family_reunification"]
        assert page.evaluate("document.activeElement.dataset.esploraVoce") == "family_reunification"
        assert page.locator("[data-esplora-voce='family_reunification']").get_attribute("data-attiva") == ""
        # the row's line is kept for a screen reader, not drawn
        assert page.evaluate("getComputedStyle(document.querySelector('.esplora__riga')).clipPath") != "none"
    finally:
        context.close()


@pytest.mark.parametrize(("width", "script"), [(390, True), (1440, False)])
def test_without_the_preview_every_row_shows_its_line(browser, live_server, seeded, phase3, width, script):
    context = browser.new_context(
        viewport={"width": width, "height": 900}, device_scale_factor=1, java_script_enabled=script
    )
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/parcours/", wait_until="load")
        assert not page.locator(".esplora__anteprime").is_visible()
        lines = page.locator(".esplora__riga")
        assert lines.count() == 8
        for i in range(8):
            assert lines.nth(i).is_visible()
            assert lines.nth(i).bounding_box()["width"] > 40
    finally:
        context.close()


def test_the_sheet_s_navigation_stays_in_reach_and_marks_the_chapter_in_view(browser, live_server, seeded, phase3):
    for width in (1440, 390):
        context = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        try:
            page.goto(live_server.url + "/fr/parcours/salaried_work/", wait_until="load")
            page.evaluate("document.getElementById('ressources').scrollIntoView()")
            page.wait_for_timeout(600)
            box = page.locator("nav.scheda-nav").bounding_box()
            assert 0 <= box["y"] < 900, (width, box)
            page.locator("a.scheda-nav__voce[href='#autorites']").click()
            page.wait_for_timeout(800)
            assert page.locator("a.scheda-nav__voce[href='#autorites']").get_attribute("aria-current") == "location"
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_sheet_s_sticky_bar_never_hides_the_focus_or_an_anchor_s_chapter(
    browser, live_server, seeded, phase3, lang
):
    """WCAG 2.4.11 Focus Not Obscured (Minimum): Shift+Tab walks back through the chapters' controls at a phone's
    width — each focused control lands wholly below the letterhead and the sticky bar of anchors (measured before the
    fix: «Tous les parcours réguliers» at 72–100 px, under the bar's 56–111 px); an anchor's chapter starts below the
    bar too, and close under it (never a screen's third away)."""
    context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    page = context.new_page()
    probe = """() => {
      const r = document.activeElement.getBoundingClientRect();
      const bar = document.querySelector('nav.scheda-nav').getBoundingClientRect();
      return {tag: document.activeElement.tagName, top: r.top, bottom: r.bottom, bar: bar.bottom,
              inside: Boolean(document.activeElement.closest('.scheda-capitoli'))};
    }"""
    try:
        page.goto(live_server.url + f"/{lang}/parcours/salaried_work/", wait_until="load")
        page.evaluate(
            "() => { const c = document.querySelectorAll('.scheda-capitoli :is(a[href], summary)'); c[c.length - 1].focus(); }"
        )
        seen = 0
        for _ in range(14):
            page.keyboard.press("Shift+Tab")
            info = page.evaluate(probe)
            if not info["inside"] or info["tag"] not in ("A", "SUMMARY", "BUTTON"):
                continue
            seen += 1
            assert info["top"] >= info["bar"], (lang, info)
        assert seen >= 8, seen
        page.goto(live_server.url + f"/{lang}/parcours/salaried_work/#ressources", wait_until="load")
        page.wait_for_timeout(400)
        top = page.evaluate("document.getElementById('ressources').getBoundingClientRect().top")
        bar = page.evaluate("document.querySelector('nav.scheda-nav').getBoundingClientRect().bottom")
        assert bar <= top <= bar + 48, (lang, top, bar)
    finally:
        context.close()
