"""
V5.32 lane C (the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026), in Chrome.

P2-2 of the integration review — RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION
directive of 12 Nov 2026: the university proposal's head draws no photograph (round 2 seated the campus frame of
/universites-et-formation/ there, the page one click before). What the round-2 test held and still holds: the head's
compact contract — the formwork starts in the first screen at 1440, in either reading direction — and, stronger, the
campus frame is neither drawn nor fetched on the form at any width.

P2-6 of the integration review: the rows of the register of actors on /institutions/ open on a capital at display
only — the computed ::first-letter — and Arabic, which has no case, is left alone.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

# Playwright's sync API runs an event loop in this thread; the live server's seeding is synchronous Django
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]


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


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_university_proposal_head_draws_no_frame_and_the_form_starts_in_the_first_screen(
    browser, live_server, seeded, legal_published, lang
):
    # gate G2 open (the legal pages published): the page draws its formwork, not the «forms closed» notice
    url = f"{live_server.url}/{lang}/collaboration/universites-formation/"
    for width, height in ((1440, 900), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        fetched: list[str] = []
        page.on("request", lambda request: fetched.append(request.url) if "echange-campus" in request.url else None)
        try:
            page.goto(url, wait_until="load")
            page.wait_for_timeout(400)
            state = page.evaluate("""() => ({
              frames: document.querySelectorAll('header.ingresso :is(figure, picture, img)').length,
              form: document.querySelector('.formwork').getBoundingClientRect().top, h: innerHeight})""")
            assert state["frames"] == 0 and not fetched, (width, state, fetched)
            if width == 1440:
                assert state["form"] < state["h"], (state, "the formwork starts in the first screen")
        finally:
            context.close()


@pytest.fixture
def phase3_live(set_flag, monkeypatch):
    """Gate G3 open for the live server without freezegun (a frozen monotonic clock stalls Playwright)."""
    from core import clock, flags

    monkeypatch.setattr(clock, "now", lambda: dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC))
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_register_rows_open_on_a_capital_and_arabic_is_left_alone(browser, live_server, seeded, phase3_live, lang):
    """P2-6 of the integration review: on /institutions/ each row of the register of actors opens on a capital in
    French (the computed ::first-letter), its words untouched («organismes publics» stays as written in the text);
    in Arabic no row carries the transform."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/institutions/", wait_until="load")
        rows = page.evaluate("""() => [...document.querySelectorAll('.istituzioni-aula .emiciclo__voce')].map(r => ({
          text: r.textContent, display: getComputedStyle(r).display,
          first: getComputedStyle(r, '::first-letter').textTransform}))""")
        assert len(rows) == 6 and all(row["display"] == "block" for row in rows), rows
        if lang == "ar":
            assert all(row["first"] == "none" for row in rows), rows
        else:
            assert all(row["first"] == "capitalize" for row in rows), rows
            assert "organismes publics" in [row["text"] for row in rows], "the text itself is never edited"
    finally:
        context.close()
