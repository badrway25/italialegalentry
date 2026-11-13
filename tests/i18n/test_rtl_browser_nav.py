"""
RTL check of «Il portico» (design V5, V5.4 plan §1.12 acceptance N19; W2-C1).

Placed by script, so no static guard can see it (plan §2.5): in Arabic as in French, «l'architrave» — the one
indicator — sits under the open door; a door's panel floats on the letterhead's content box and holds its three zones
in the reading direction — the lede, the entries, «la lunetta» (V5.15 lane A, DL54-170: this replaced W2-C1's N2,
«the entries column starts at the first door's inline start»); and the plain panel («Projet») hangs from the bar's
inline end. Chromium at 1440 × 900 on the home, with the static
fallback menu (two doors before gate G3, four after it).
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DOOR = "[data-portico-door]"


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


def _content_edges(page) -> dict:
    """The letterhead's content box: the lock-up's start and the end zone's end, which the panels hang from."""
    return page.evaluate(
        """() => {
            const inner = document.querySelector('.site-header__inner');
            const r = inner.getBoundingClientRect();
            const cs = getComputedStyle(inner);
            return {left: r.left + parseFloat(cs.paddingLeft), right: r.right - parseFloat(cs.paddingRight)};
        }"""
    )


@pytest.mark.parametrize("lang", ["ar", "fr"])
def test_the_architrave_and_the_entries_follow_the_doors_in_both_directions(browser, live_server, seeded, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
        doors = page.locator(DOOR)
        assert doors.count() >= 2
        door = doors.nth(1)
        door.click()
        page.wait_for_timeout(400)
        assert door.get_attribute("aria-expanded") == "true"

        # N19: the architrave sits under the open door — inside its box, as wide as its words
        box = door.bounding_box()
        pad = page.evaluate("parseFloat(getComputedStyle(document.querySelectorAll('[data-portico-door]')[1]).paddingLeft)")
        arch = page.locator("[data-portico-architrave]").bounding_box()
        assert arch, "no architrave rendered"
        assert abs(arch["x"] - (box["x"] + pad)) <= 1.5, (lang, box, arch)
        assert abs(arch["width"] - (box["width"] - 2 * pad)) <= 1.5, (lang, box, arch)
        assert abs(arch["y"] - (box["y"] + box["height"])) <= 2, (lang, box, arch)

        # the floating mega panel (V5.15 lane A, DL54-170, cb252091/b9098210; static/css/v5/_portico.css) in place of
        # W2-C1's N2: three zones in the reading direction — the lede (eyebrow, gloss) on the panel's inline start, the
        # entries a 32 px column gap after it, «la lunetta» flush on the inline end — mirrored, not re-ordered, in Arabic
        zones = page.evaluate(
            """(id) => { const p = document.getElementById(id); const R = (s) => { const b = p.querySelector(s).getBoundingClientRect();
                 return {start: b.left, end: b.right}; };
               const panel = p.getBoundingClientRect(); const rtl = document.documentElement.dir === 'rtl';
               const flip = (z) => rtl ? {start: panel.right - z.end, end: panel.right - z.start} : {start: z.start - panel.left, end: z.end - panel.left};
               return Object.fromEntries(['.portico__sheet', '.portico__eyebrow', '.portico__gloss', '.portico__entries', '.portico__lunetta']
                 .map((s) => [s.slice(10), flip(R(s))]).concat([['width', panel.width]])); }""",
            door.get_attribute("aria-controls"),
        )
        width = zones["width"]
        assert abs(zones["sheet"]["start"] - 1) <= 1 and abs(zones["lunetta"]["end"] - (width - 1)) <= 1, (lang, zones)
        assert abs(zones["sheet"]["end"] - zones["lunetta"]["start"]) <= 1, (lang, zones)
        for lede in ("eyebrow", "gloss"):
            assert abs(zones[lede]["start"] - zones["sheet"]["start"]) <= 1, (lang, lede, zones)
        assert abs(zones["entries"]["start"] - (zones["gloss"]["end"] + 32)) <= 1.5, (lang, zones)
        assert zones["entries"]["end"] <= zones["lunetta"]["start"] + 1, (lang, zones)
        panel = page.locator(f"#{door.get_attribute('aria-controls')}").bounding_box()
        edges = _content_edges(page)
        assert abs(panel["x"] - edges["left"]) <= 1 and abs(panel["x"] + panel["width"] - edges["right"]) <= 1, (panel, edges)
        page.keyboard.press("Escape")

        # the plain panel («Projet») hangs from the bar's inline end
        last = doors.nth(doors.count() - 1)
        last.click()
        page.wait_for_timeout(400)
        plain = page.locator(f"#{last.get_attribute('aria-controls')}")
        assert plain.is_visible() and "portico--plain" in (plain.get_attribute("class") or "")
        box = plain.bounding_box()
        if lang == "ar":
            assert abs(box["x"] - edges["left"]) <= 1, (box, edges)
        else:
            assert abs(box["x"] + box["width"] - edges["right"]) <= 1, (box, edges)
        page.screenshot(path=str(os.path.join(os.path.dirname(__file__), "..", "..", "docs", "qa", "rtl", f"portico-{lang}-1440.png")), full_page=False)
    finally:
        context.close()


# French: tests/frontend/test_browser_w2_c1.py::test_the_keyboard_model_of_the_portico runs the same keys, left to right
@pytest.mark.parametrize("lang", ["ar"])
def test_the_arrows_follow_the_eye(browser, live_server, seeded, lang):
    """In Arabic ← is «next»: from the first door the key that points along the reading direction reaches the second
    door, and its panel follows an open one (NAVIGATION §4.8; plan §1.12 item 6)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
        doors = page.locator(DOOR)
        first, second = doors.nth(0), doors.nth(1)
        first.focus()
        page.keyboard.press("ArrowDown")
        assert first.get_attribute("aria-expanded") == "true"
        page.keyboard.press("ArrowLeft")
        assert page.evaluate("document.activeElement.textContent.trim()") == second.text_content().strip()
        assert second.get_attribute("aria-expanded") == "true" and first.get_attribute("aria-expanded") == "false"
        page.keyboard.press("Escape")
        assert page.evaluate("document.activeElement.textContent.trim()") == second.text_content().strip()
        assert page.locator(f"{DOOR}[aria-expanded='true']").count() == 0
    finally:
        context.close()
