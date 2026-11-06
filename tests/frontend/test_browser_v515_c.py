"""
V5.15 W3, lane C, round 2 (label v515-c-improve2) in the browser: the black-and-white frames DEVELOP.

The quality round's MJ-1: a body frame carries both lane A's mask (the zoom on its img) and the develop grade
(bw-scroll: the colour on the same img); two animation shorthands on one img let the zoom win, so the assembly hall,
the microscopes and the home diptych stayed grey at mid-viewport. The markup tests asserted the attributes only; this
one asserts the outcome: scrolled to the middle of the viewport, the frame's img is in full colour.
Chromium only (scroll-driven animations); under reduced motion the frame is in colour, still.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

FRAMES = {"/fr/formation/": "training.after", "/fr/institutions/": "institutions.chamber"}

PROBE = """slot => {
  const fig = document.querySelector(`figure[data-slot="${slot}"]`);
  const img = fig.querySelector('img');
  return { filter: getComputedStyle(img).filter, grade: fig.dataset.grade, reveal: fig.dataset.reveal || '' };
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


@pytest.fixture
def open_pages(seeded, set_flag, monkeypatch, legal_published):
    """Gate G3 open for the live server without freezegun (a frozen monotonic clock stalls Playwright)."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _mid(page, slot: str) -> dict:
    # V5.22 (lane P1, round 1; V5.20 strict rule — the expectation unchanged): the page's `scroll-behavior: smooth`
    # turns a plain scrollBy into a scroll still moving when the frame is read — on SECTION_SYSTEM_V2's Formation
    # (§3.9) at 390 the 600 ms wait read the second time's frame short of the middle (grayscale 0.03; brought there at
    # once it is grayscale(0), measured). The frame is brought to the middle at once, then read: the same outcome.
    page.evaluate(
        """slot => { const f = document.querySelector(`figure[data-slot="${slot}"]`); const r = f.getBoundingClientRect();
                     scrollBy({top: r.top + r.height / 2 - innerHeight / 2, behavior: 'instant'}); }""",
        slot,
    )
    page.wait_for_timeout(600)
    return page.evaluate(PROBE, slot)


@pytest.mark.parametrize("path", list(FRAMES))
@pytest.mark.parametrize("width, height", [(1440, 900), (390, 844)])
def test_a_developing_frame_is_in_colour_at_mid_viewport(browser, live_server, open_pages, path, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}{path}", wait_until="networkidle")
        state = _mid(page, FRAMES[path])
        assert state["grade"] == "bw-scroll" and state["reveal"] == "mask", state
        # a finished colour keyframe computes as «grayscale(0)», the still state as «none»: both are full colour
        assert state["filter"] in ("none", "grayscale(0)"), (path, width, state)
    finally:
        context.close()


def test_a_developing_frame_is_grey_before_it_enters(browser, live_server, open_pages):
    # the treatment exists: far below the fold the frame is still black and white
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/institutions/", wait_until="networkidle")
        assert "grayscale(1)" in page.evaluate(PROBE, "institutions.chamber")["filter"]
    finally:
        context.close()
