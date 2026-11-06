"""
The folio's T1 seal on the approved heads, in Chromium (design V5.22, SECTION_SYSTEM_V2 §0.1 «Folio seals in the
heads», §4.2; lane S, round 1 — label v522-s-improve1, QA_ROUND1 M3). The seat is 32 px taller than the 36 px disc it
replaced; the head is refined, never recomposed, and the head's call stays in the first screen (V5.18 §2/§3):

* the call stands inside the first screen at the sizes that were short of room — 1024 × 768, 1280 × 720 and 1366 × 768
  on a desktop, 390 × 844, 375 × 812, 360 × 800 and 375 × 667 on a phone — in French and in Arabic;
* from 48 rem, and on every head whose band keeps its 40 px, the seat rises into the band's top padding: the title
  stands at most 4 px lower in its column than with the disc (60 px from the column's top instead of 56); on a phone's
  door head (a band held to 24 px, V5.18 B2) at most 12 px lower; on a short phone's door head (16 px) the folio stays
  typographic, in the disc's 36 px;
* the seat never touches the trail (8 px of the band above it at least) and never crowds the title (12 px under its
  sill at least);
* on Parcours (the route head, from 48 rem) the seal, the line that leaves its sill and the stations' rings share one
  axis (round 1: the seal's 56 px moved the line to its centre, the rings had stayed on the disc's).

Chromium on the seeded site, the gate G3 open, the clock at 3 October 2026 through `core.clock.now` (a frozen monotonic
clock stalls Playwright).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: the seven heads that draw a seal (FOLIO), the four door heads first (their call is the head's way in)
PAGES = ("parcours/", "entreprises/", "institutions/", "universites-et-formation/", "parcours/salaried_work/",
         "formation/", "attention-aux-fraudes/")
SIZES = ((1024, 768), (1280, 720), (1366, 768), (390, 844), (375, 812), (360, 800), (375, 667))
#: the title's distance from its column's top (the folio's row and its margin): the disc's folio was 36 px + its 20 px
#: margin (16 on a phone's door head, 12 on a short phone's); the seat adds at most 4 px, 12 on a phone's door head
ROOM = {"head": 60.5, "door-phone": 64.5, "door-short": 48.5}

PROBE = """() => {
  const head = document.querySelector('header.ingresso'), label = head.querySelector('.ingresso__label');
  const column = head.querySelector('.ingresso__text');
  const seal = label.querySelector('.sigillo'), h1 = document.querySelector('h1');
  const call = head.querySelector('.ingresso__way .btn, .ingresso__aside .btn, .via .btn');
  const r = el => el.getBoundingClientRect();
  return {vh: innerHeight, door: !!head.querySelector('.ingresso__way'), pad: parseFloat(getComputedStyle(head).paddingTop),
          band: r(head).top, column: r(column).top, label: r(label).bottom, title: r(h1).top,
          seal: seal && getComputedStyle(seal).display !== 'none' ? r(seal).top : null, call: call ? r(call).bottom : null};
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


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_seal_folio_keeps_the_head_and_its_call_in_the_first_screen(browser, live_server, open_pages, lang):
    for width, height in SIZES:
        ctx = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = ctx.new_page()
        try:
            for path in PAGES:
                page.goto(f"{live_server.url}/{lang}/{path}", wait_until="load")
                head = page.evaluate(PROBE)
                where = (lang, path, f"{width}x{height}")
                if head["call"] is not None:
                    assert head["call"] <= head["vh"], (*where, "the head's call in the first screen", head)
                phone_door = width < 768 and head["door"]
                room = "door-short" if phone_door and height <= 760 else "door-phone" if phone_door else "head"
                assert head["title"] - head["column"] <= ROOM[room], (*where, room, head)
                if room == "door-short":
                    assert head["seal"] is None, (*where, "a short phone's door head keeps a typographic folio")
                    continue
                assert head["seal"] is not None, (*where, "the page's T1 seal stands in its folio")
                assert head["seal"] - head["band"] >= 8, (*where, "the seat never touches the trail", head)
                assert head["title"] - head["label"] >= 12, (*where, "the sill never crowds the title", head)
        finally:
            ctx.close()


AXIS = """() => {
  const text = document.querySelector('[data-compose="route"] .ingresso__text');
  const seal = text.querySelector('.ingresso__label > .sigillo').getBoundingClientRect();
  const x = (el, pseudo) => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el, pseudo);
    return r.left + parseFloat(cs.left) + parseFloat(cs.width) / 2; };
  return {seal: seal.left + seal.width / 2, line: x(text, '::before'),
          rings: [...text.querySelectorAll('.ingresso__title, .ingresso__lead, .via__title')].map(el => x(el, '::before'))};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_route_head_s_seal_line_and_stations_share_one_axis(browser, live_server, open_pages, lang):
    for width in (1440, 1024, 768):
        ctx = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        try:
            page.goto(f"{live_server.url}/{lang}/parcours/", wait_until="load")
            axis = page.evaluate(AXIS)
            assert abs(axis["line"] - axis["seal"]) <= 1, (lang, width, axis)
            assert axis["rings"] and all(abs(ring - axis["line"]) <= 1 for ring in axis["rings"]), (lang, width, axis)
        finally:
            ctx.close()
