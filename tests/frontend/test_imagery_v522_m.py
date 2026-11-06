"""
V5.22 lane M (labels v522-m-build, v522-m-improve1; SECTION_SYSTEM_V2 §8, §9.9) in the browser.

1. The REAL page (QA round 1, m2). Universités is the one page that already draws a lane-M rendering
   (`universities.exchange`, re-cut). On /fr/ and /ar/universites-et-formation/, at 1600, 1440, 1199 and 1024 (1x),
   768 and 390 (2x), the width the frame is drawn at is the width its `sizes` states. The sizes are evaluated by the test the way the
   browser evaluates them, with each `vw` read against the layout viewport — the classic scrollbar is the only
   difference a `vw` length cannot know, and it is measured, not tolerated (|drawn − sizes| ≤ 1.5 px). The raw
   evaluation never states LESS than what is drawn, so the browser never under-fetches. Its choice of file is sound for
   the density, the art-directed ratio is taken, and the frame is lazy, async and boxed.
   When lanes H, P1 and P2 place a V5.22 slot or variant on their pages, they assert the same there (NOTES §7).

2. The test bench (templates/dev/designpreview/specimens/imagery.html), where every new rendering is drawn alone by
   the product's own {% photo %} tag. The bench lays its frames out in its own boxes, so it is NOT used to compare the
   drawn width with `sizes` (round 1, m2: that comparison was circular there). It checks what does not depend on the
   bench's layout: the ratio each band takes (art direction) and the box keeping it, the browser's choice of file for
   the sizes it is given at each density, the lazy, async, boxed markup, and no horizontal overflow (m3).
Chromium only.
"""

from __future__ import annotations

import datetime as dt
import os
import re

import pytest
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path
from django.utils import translation

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

BOARD = "dev/designpreview/specimens/imagery.html"


def _board(request):
    with translation.override("it"):
        return HttpResponse(render_to_string(BOARD, {"board": "imagery"}))


urlpatterns = [path("imagery-board/", _board)]

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: (slot, variant) -> the ratio drawn from 64 rem, from 48 rem, below 48 rem
RATIOS = {
    ("home.integrity.stone", ""): ("21x9", "4x5", "4x5"),
    ("home.pilot.cedar", "pannello"): ("2x3", "3x2", "3x2"),
    ("home.pilot.marble", "pannello"): ("2x3", "3x2", "3x2"),
    ("home.ecosystem", "campata"): ("4x3", "3x2", "3x2"),
    ("project.volumes", ""): ("21x9", "16x9", "4x5"),
    ("pathways.family.work", ""): ("3x2", "21x9", "21x9"),
    ("pathways.family.study", ""): ("3x2", "21x9", "21x9"),
    ("pathways.family.family", ""): ("3x2", "21x9", "21x9"),
    ("pathways.family.other", ""): ("3x2", "21x9", "21x9"),
    ("training.before", ""): ("4x5", "3x2", "3x2"),
    ("universities.exchange", ""): ("3x2", "3x2", "3x2"),
}
NUM = {"21x9": 21 / 9, "16x9": 16 / 9, "4x5": 4 / 5, "3x2": 3 / 2, "2x3": 2 / 3, "4x3": 4 / 3}

PROBE = r"""(slot) => {
  const fig = document.querySelector(`figure[data-slot="${slot}"]`);
  const img = fig.querySelector('img');
  // the sizes the browser was given, evaluated at this viewport: the first entry whose media matches
  const parts = img.sizes.split(/,(?![^(]*\))/).map(s => s.trim());
  let length = parts[parts.length - 1];
  for (const part of parts) {
    const m = part.match(/^(\(.+\))\s+(\S.*)$/);
    if (!m) { length = part; break; }
    if (matchMedia(m[1]).matches) { length = m[2]; break; }
  }
  const measure = (value) => {
    const probe = document.createElement('div');
    probe.style.position = 'absolute';
    probe.style.inlineSize = value;
    document.body.append(probe);
    const w = probe.getBoundingClientRect().width;
    probe.remove();
    return w;
  };
  // as the browser reads it (a vw is 1 % of the window, scrollbar included) ...
  const sizesRaw = measure(length);
  // ... and with each vw read against the layout viewport (the classic scrollbar taken out)
  const layout = document.documentElement.clientWidth;
  const sizesLayout = measure(length.replace(/(\d+(?:\.\d+)?)vw/g, (_, n) => `calc(${layout}px * ${n} / 100)`));
  const box = img.getBoundingClientRect();
  const source = [...fig.querySelectorAll('source')].find(s => s.type === 'image/avif' && (!s.media || matchMedia(s.media).matches));
  return {
    length, sizesRaw, sizesLayout, scrollbar: innerWidth - layout, drawn: box.width, drawnH: box.height,
    current: img.currentSrc, natural: [img.naturalWidth, img.naturalHeight], srcset: source.srcset,
    loading: img.loading, decoding: img.decoding, fetchpriority: img.getAttribute('fetchpriority'),
    imgBox: [img.getAttribute('width'), img.getAttribute('height')],
    sourcesBoxed: [...fig.querySelectorAll('source')].every(s => s.getAttribute('width') && s.getAttribute('height')),
    dpr: devicePixelRatio,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
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


def _band(width: int) -> int:
    return 0 if width >= 1024 else (1 if width >= 768 else 2)


def _probe(page, slot: str) -> dict:
    page.evaluate(
        """(slot) => document.querySelector(`figure[data-slot="${slot}"]`).scrollIntoView({block: 'center'})""", slot
    )
    page.wait_for_function(
        """(slot) => { const i = document.querySelector(`figure[data-slot="${slot}"] img`);
                       return i.complete && i.naturalWidth > 0; }""",
        arg=slot,
        timeout=15000,
    )
    page.wait_for_timeout(250)
    return page.evaluate(PROBE, slot)


def _check_markup_ratio_and_pick(state: dict, expected: str, dpr: int, where: tuple) -> None:
    # explicit boxes, lazy, async, never a priority
    assert state["loading"] == "lazy" and state["decoding"] == "async", where
    assert state["fetchpriority"] is None and all(state["imgBox"]) and state["sourcesBoxed"], where
    # the art direction: the file taken has the ratio drawn at this width, and the box keeps it
    assert f"-{expected}-" in state["current"], (where, expected, state["current"])
    nw, nh = state["natural"]
    assert abs(nw / nh - NUM[expected]) < 0.02, (where, state["natural"])
    assert abs(state["drawn"] / state["drawnH"] - NUM[expected]) < 0.03, (where, state)
    # the browser's choice is sound for the sizes it was given at this density
    ladder = sorted(int(w) for w in re.findall(r" (\d+)w", state["srcset"]))
    taken = int(re.search(r"-(\d+)\.(?:avif|webp)", state["current"]).group(1))
    need = state["sizesRaw"] * dpr
    above = [w for w in ladder if w >= need]
    assert taken in ladder, (where, taken, ladder)
    if above:
        # Blink may take the step below when the density sits under the two steps' geometric mean
        below = [w for w in ladder if w < need]
        assert taken in {above[0], *(below[-1:])}, (where, taken, need, ladder)
    else:
        assert taken == ladder[-1], (where, taken, need, ladder)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(
    "width, height, dpr",
    # the four widths of QA round 1 (m2), plus 1 600 (the 1 440 container) and 1 199 (the top of the 64–75 rem step,
    # where a 45vw approximation was 8 px short)
    [(1600, 900, 1), (1440, 900, 1), (1199, 800, 1), (1024, 768, 1), (768, 1024, 2), (390, 844, 2)],
)
def test_the_live_campus_frame_is_drawn_at_the_width_its_sizes_states(
    browser, live_server, open_pages, lang, width, height, dpr
):
    """QA round 1, m2: drawn width = evaluated `sizes` on the real Universités page, not on a fixture laid out with the
    sizes' own lengths."""
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/universites-et-formation/", wait_until="networkidle")
        state = _probe(page, "universities.exchange")
        where = ("universities.exchange", lang, width, dpr)
        # the width the frame is drawn at is the width its sizes states, the scrollbar measured (± rounding)
        assert abs(state["drawn"] - state["sizesLayout"]) <= 1.5, (where, state)
        # and the raw evaluation (a vw counts the scrollbar) never under-states it: the browser never under-fetches
        assert state["sizesRaw"] >= state["drawn"] - 0.5, (where, state)
        _check_markup_ratio_and_pick(state, "3x2", dpr, where)
        assert state["overflow"] <= 0, (where, state["overflow"])
    finally:
        context.close()


@pytest.mark.urls(__name__)
@pytest.mark.parametrize(
    "width, height, dpr",
    [(1440, 900, 1), (1440, 900, 2), (768, 1024, 2), (390, 844, 2), (390, 844, 3)],
)
def test_every_v522_rendering_takes_its_ratio_and_a_sound_file_on_the_bench(browser, live_server, width, height, dpr):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/imagery-board/", wait_until="networkidle")
        for (slot, _variant), ratios in RATIOS.items():
            state = _probe(page, slot)
            _check_markup_ratio_and_pick(state, ratios[_band(width)], dpr, (slot, width, dpr))
        # the bench never overflows the layout viewport (m3: its frames are sized in % of the container, never in vw)
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
    finally:
        context.close()
