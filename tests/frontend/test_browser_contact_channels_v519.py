"""
V5.19 (lane v519-k) in the browser: the owner's telephone channels under a finger.

The contact page's two plates, the footer's two links and the phone sheet's two plates: each a link of at least
44 × 44 CSS px at 390 and 360 px, its number on one line (no wrap inside the digit groups), and — on the Arabic
page — the groups in the owner's order, left to right (the isolate's computed direction is ltr and the first group is
drawn left of the last).

V5.20 (option B): the owner-confirmed WhatsApp number is configured outside the repository (V5.19/V5.20); the channel
is drawn here with Ofcom's fictional +44 7700 900123 (tests/conftest.py, ``whatsapp_channel``), whose label has the
owner's number's length (16 characters), so the plates, the footer's links and the sheet's plates are measured as
they are drawn for the real one. Test-update note: the hrefs the test expects come from the configured channel
instead of a written number; every measure is unchanged.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PROBE = """sel => [...document.querySelectorAll(sel)].map(a => {
  const r = a.getBoundingClientRect();
  const num = a.querySelector('bdi.phone');
  let order = null, lines = null, dir = null;
  if (num) {
    const range = document.createRange();
    range.selectNodeContents(num);
    const rects = [...range.getClientRects()].filter(x => x.width > 0);
    lines = new Set(rects.map(x => Math.round(x.top))).size;
    dir = getComputedStyle(num).direction;
    const text = num.firstChild;
    const first = document.createRange(); first.setStart(text, 0); first.setEnd(text, 1);
    const last = document.createRange(); last.setStart(text, text.length - 1); last.setEnd(text, text.length);
    order = first.getBoundingClientRect().left < last.getBoundingClientRect().left;
  }
  return { href: a.getAttribute('href'), w: r.width, h: r.height, lines, dir, order, text: num ? num.textContent : null };
})"""


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


def _check(rows, expected_hrefs):
    assert {row["href"] for row in rows} == expected_hrefs, rows
    for row in rows:
        assert row["w"] >= 44 and row["h"] >= 44, row
        if row["text"] is not None:
            assert row["lines"] == 1, row
            assert row["dir"] == "ltr" and row["order"] is True, row


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [390, 360])
def test_the_channels_are_tappable_and_read_in_order(browser, live_server, seeded, whatsapp_channel, lang, width):
    hrefs = {"tel:800642015", whatsapp_channel.url}
    context = browser.new_context(viewport={"width": width, "height": 800}, device_scale_factor=1, has_touch=True, is_mobile=True)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/contact/", wait_until="networkidle")
        _check(page.evaluate(PROBE, ".canale__link"), hrefs)
        _check(page.evaluate(PROBE, ".site-footer__channel"), hrefs)
        page.click("[data-nav-toggle]")
        page.wait_for_selector("#nav-sheet[open]")
        page.wait_for_timeout(500)
        _check(page.evaluate(PROBE, ".nav-sheet__channel"), hrefs)
    finally:
        context.close()
