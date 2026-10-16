"""
The public interior of design V5.4 in a browser — W3-F1, step 1: the doors and the project pages (plan §3.5 item 1;
§1.3 three corners a screen; §2.5 RTL; Q8 the steps never mirror; BI04 the disc moves with the inline start).

Chromium, gate G3 open through the clock (a frozen `time.monotonic` stalls Playwright, so `core.clock.now` is
patched as the navigation family does), at 1440 × 900 and 390 × 844, in French and in Arabic: no page wider than its
viewport; at most three distinct corner radii painted in the first screen, the chrome included; the door card carries
the door's way in, its disc at the inline start and clear of the words, its control inside the first screen (the fix
pass, M1); the chapter's head stands at the reading edge; the trail's and the forward links' targets stand on 24 px,
44 px under a finger (SP-8); the pilot's stations never break a word.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PAGES = ("/{lang}/parcours/", "/{lang}/entreprises/", "/{lang}/projet-pilote/", "/{lang}/forum/")

#: the distinct radii of what is painted and on screen in the first viewport (an element with a ground, an edge, a
#: shadow or an image); the skip link and other off-screen boxes do not count
RADII_JS = """() => {
  const seen = new Set();
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1 || r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
    const painted = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.borderTopWidth !== '0px' || cs.boxShadow !== 'none' || el.tagName === 'IMG';
    const rad = cs.borderTopLeftRadius;
    if (painted && rad && rad !== '0px') seen.add(rad.includes('%') ? rad : String(Math.min(999, Math.round(parseFloat(rad)))));
  }
  return [...seen].sort();
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
def phase3(set_flag, monkeypatch):
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (390, 844)])
def test_no_overflow_and_three_corners_a_screen(browser, live_server, seeded, phase3, lang, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    page = context.new_page()
    try:
        for path in PAGES:
            page.goto(live_server.url + path.format(lang=lang), wait_until="load")
            page.evaluate("document.fonts.ready")
            sizes = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            assert sizes[0] <= sizes[1], (path, lang, width, sizes)
            radii = page.evaluate(RADII_JS)
            assert len(radii) <= 3, (path, lang, width, radii)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (390, 844)])
def test_the_door_card_carries_its_way_in_the_first_screen_its_disc_at_the_inline_start(
    browser, live_server, seeded, phase3, lang, width, height
):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    page = context.new_page()
    try:
        for path in (
            "/{lang}/parcours/",
            "/{lang}/institutions/",
            "/{lang}/universites-et-formation/",
            "/{lang}/entreprises/",
        ):
            page.goto(live_server.url + path.format(lang=lang), wait_until="load")
            page.evaluate("document.fonts.ready")
            geometry = page.evaluate("""() => {
              const box = (el) => el.getBoundingClientRect();
              const card = box(document.querySelector('.ingresso__aside.porta'));
              const disc = box(document.querySelector('.porta__disc'));
              const words = box(document.querySelector('.porta .porta__disc + *'));
              const control = box(document.querySelector('.porta .via__action .btn'));
              const head = box(document.querySelector('.chapter__head'));
              const body = box(document.querySelector('.chapter__body'));
              return {discLeft: disc.left - card.left, discRight: card.right - disc.right,
                      overlap: !(words.right <= disc.left || words.left >= disc.right),
                      controlTop: control.top, controlInside: control.left >= card.left && control.right <= card.right,
                      headLeft: head.left, bodyLeft: body.left, vh: innerHeight};
            }""")
            where = (path, lang, width)
            assert not geometry["overlap"], ("the disc and the way's words never meet", where)
            assert geometry["controlInside"], where
            if width == 1440:
                assert geometry["controlTop"] < geometry["vh"], ("the door's control in the first screen", where)
            else:
                assert geometry["controlTop"] < 1.25 * geometry["vh"], (
                    "the door's control at the first screen's foot",
                    where,
                )
            if lang == "ar":
                assert geometry["discRight"] < geometry["discLeft"], (
                    "the disc stands at the inline start (BI04)",
                    where,
                )
                if width == 1440:
                    assert geometry["headLeft"] > geometry["bodyLeft"], (
                        "the chapter's head at the reading edge, on the right"
                    )
            else:
                assert geometry["discLeft"] < geometry["discRight"], where
                if width == 1440:
                    assert geometry["headLeft"] < geometry["bodyLeft"]
    finally:
        context.close()


#: a link answers on `floor` px when a point (floor / 2 - 1) px above and below its middle still lands on it — the box
#: or the target it carries (the trail's ::after under a finger, the shared page's drawing since the budget pass)
TARGET_JS = """(floor) => [...document.querySelectorAll('.breadcrumbs__item a, .chapter__more > a, .chapter__links > a')]
  .filter((a) => a.getClientRects().length)
  .map((a) => {
    a.scrollIntoView({block: 'center', behavior: 'instant'});
    const r = a.getBoundingClientRect();
    const x = r.left + Math.min(r.width / 2, 20), mid = r.top + r.height / 2, reach = floor / 2 - 1;
    const hits = [mid - reach, mid + reach].map((y) => {
      const el = document.elementFromPoint(x, y);
      return !!el && (el === a || a.contains(el));
    });
    return [a.textContent.trim().slice(0, 30), Math.round(r.height), hits[0] && hits[1]];
  })"""


@pytest.mark.parametrize("coarse", [False, True])
def test_the_trail_and_the_forward_links_stand_on_the_target_floor(browser, live_server, seeded, phase3, coarse):
    """SP-8 (plan §1.4; the fix pass, A11Y_PERF finding 1): 24 px is the floor of every target, 44 px under a finger —
    the box, or the target a link carries without a taller line (the trail: v5/_pagina.css §1, the budget pass)."""
    options = (
        {"viewport": {"width": 390, "height": 844}, "has_touch": True, "is_mobile": True}
        if coarse
        else {"viewport": {"width": 1440, "height": 900}}
    )
    context = browser.new_context(device_scale_factor=1, **options)
    page = context.new_page()
    floor = 44 if coarse else 24
    try:
        for path in ("/fr/le-projet/", "/fr/agami/", "/fr/parcours/salaried_work/", "/fr/entreprises/"):
            page.goto(live_server.url + path, wait_until="load")
            targets = page.evaluate(TARGET_JS, floor)
            assert targets, path
            assert any(text == "Accueil" for text, *_ in targets), (path, "the trail is measured")
            short = [target for target in targets if not target[2]]
            assert not short, (path, coarse, short)
            if not coarse:
                assert all(height >= 24 for _, height, _ in targets), (path, targets)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_pilot_s_stations_never_break_a_word(browser, live_server, seeded, phase3, lang):
    """The fix pass (M5): eight stations a row only from 90rem — below it «ACCOMPAGNEMENT» broke at 1280 and 1366."""
    context = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    page = context.new_page()
    try:
        for width in (1280, 1366, 1440):
            page.set_viewport_size({"width": width, "height": 800})
            page.goto(live_server.url + f"/{lang}/projet-pilote/", wait_until="load")
            page.evaluate("document.fonts.ready")
            broken = page.evaluate("""() => [...document.querySelectorAll('.pilot-diagram .linea__label')].filter((label) => {
              const node = label.firstChild; if (!node) return false;
              const text = node.textContent; let found = false;
              for (const m of text.matchAll(/[^\\s]+/g)) {
                const r = document.createRange(); r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length);
                const tops = new Set([...r.getClientRects()].filter((x) => x.width > 0.5).map((x) => Math.round(x.top)));
                if (tops.size > 1) found = true;
              }
              return found;
            }).map((label) => label.textContent)""")
            assert not broken, (lang, width, broken)
            columns = page.evaluate(
                "getComputedStyle(document.querySelector('.pilot-diagram .linea--across')).gridTemplateColumns.split(' ').length"
            )
            assert columns == (8 if width >= 1440 else 4), (lang, width, columns)
    finally:
        context.close()
