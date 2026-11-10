"""
V5.22 lane P1 — Page Composition V2 in Chromium (SECTION_SYSTEM_V2 §3.3–§3.10, §9.9; label v522-p1-build).

* the eight recomposed pages and the two form pages hold their width — no sideways scroll, no text outside the viewport
  unless it is in a scroller of its own — at 1440, 768 and 390, in French and in Arabic;
* the section runtime (§2.0): a section below the fold waits, plays once when it enters and holds nothing after (no
  time-based animation left running); under reduced motion no state is ever written and nothing runs;
* every frame a composition draws is drawn at the width its `sizes` states (lane M's probe, the `vw` read against the
  layout viewport): the four family frames of the route board, the two times' frames, the campus destination;
* the route board's choice keeps every station in the layout, dims the other lanes to the quiet ink, never an
  opacity, and its polite line says the chosen family's count;
* the diplomas' definitions open from the keyboard, one at a time;
* without script every station, milestone and term stands, in reading order;
* round 1 (QA_ROUND1, label v522-p1-improve1): the pilot's locked capitals keep whole words AND their own room — no two
  labels' boxes meet, every two at least 16 px apart, at 1280, 1366, 1440 and 1920 in four languages (M1); the pilot's
  route is its own trigger, so a desktop's first screen still sees it drawn, and its status plate ends it across its
  width (M2); on a phone the family choice is one bar with its own ground and its count, and a choice brings its lane
  under the bar (M3); the sheets' rail is in reach from every part of the page and marks the part in view (M4); the
  Formation notice keeps a reading measure and whole words (M5); the campus frame develops as the route arrives (m2);
  in Arabic a card's French title and line share one edge (m1);
* round 2 (QA_ROUND2, label v522-p1-improve2): a family chosen anywhere in the board — at its top, 900 px and 1 500 px
  into it, after a wheel scroll, by a tap — lands its lane right under the bar, the bar in view, nothing leaving the
  layout (M1, m6), on a desktop too; a French run in an Arabic card keeps the Latin leading (m2).

Chromium on the seeded site, gate G3 open, the clock at 3 October 2026 through `core.clock.now` (a frozen monotonic
clock stalls Playwright).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PAGES = (
    "projet-pilote/",
    "entreprises/",
    "institutions/",
    "universites-et-formation/",
    "parcours/",
    "parcours/salaried_work/",
    "formation/",
    "diplomes-et-titres/",
    "entreprises/recueil-des-besoins/",
    "collaboration/institutions/",
)
SIZES = ((1440, 900), (768, 1024), (390, 844))

OVERFLOW = """() => {
  const doc = document.documentElement, width = doc.clientWidth, out = [];
  for (const el of document.querySelectorAll('main *')) {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || (r.right <= width + 1 && r.left >= -1)) continue;
    let s = el, scroller = false, hidden = false;
    while (s && s !== document.body) {
      const cs = getComputedStyle(s);
      if (/(auto|scroll)/.test(cs.overflowX) && s.scrollWidth > s.clientWidth) { scroller = true; break; }
      if (cs.position === 'absolute' && (cs.clip !== 'auto' || cs.clipPath !== 'none')) hidden = true;
      s = s.parentElement;
    }
    if (!scroller && !hidden && !el.closest('.visually-hidden, [hidden], .honeypot, [aria-hidden="true"]') && getComputedStyle(el).visibility !== 'hidden') {
      out.push((el.className || el.tagName) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
    }
  }
  return {over: doc.scrollWidth - width, outside: out.slice(0, 5)};
}"""

#: lane M's probe (tests/frontend/test_imagery_v522_m.py), reduced to what P1 asserts: the media query the `sizes` list
#: picks, its length with every `vw` read against the layout viewport, and the width the frame is drawn at
DRAWN = """(selector) => {
  const img = document.querySelector(selector);
  const vw = document.documentElement.clientWidth / 100;
  const parts = img.getAttribute('sizes').split(/,(?![^(]*\\))/).map(s => s.trim());
  let length = parts[parts.length - 1];
  for (const part of parts) {
    const m = part.match(/^(\\(.*\\))\\s+(.+)$/);
    if (m && matchMedia(m[1]).matches) { length = m[2]; break; }
    if (!m) { length = part; break; }
  }
  const probe = document.createElement('div');
  probe.style.position = 'absolute'; probe.style.visibility = 'hidden';
  probe.style.width = length.replace(/(-?[\\d.]+)vw/g, (_, n) => `${parseFloat(n) * vw}px`);
  document.body.append(probe);
  const stated = probe.getBoundingClientRect().width;
  probe.remove();
  return {stated, drawn: img.getBoundingClientRect().width, length};
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
def test_the_pages_hold_their_width_at_every_size(browser, live_server, open_pages, lang):
    for width, height in SIZES:
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        try:
            for path in PAGES:
                page.goto(f"{live_server.url}/{lang}/{path}", wait_until="load")
                state = page.evaluate(OVERFLOW)
                assert state["over"] <= 0 and not state["outside"], (lang, width, path, state)
        finally:
            context.close()


def test_a_section_below_the_fold_waits_plays_once_and_holds_nothing(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        for path, selector, height in (
            ("parcours/", ".percorsi-come", 900),
            ("projet-pilote/", ".pilota-porte", 900),
            # QA_ROUND1 M2 f: the pilot's section starts in a desktop's first screen, its route is its own trigger —
            # the line is held and draws when the route itself is seen. FINAL MICRO-PASS §5 A3 (V5.20 strict rule):
            # the heads lost their drawings, so at 1440 × 900 the route starts 11 px inside the first screen and
            # stands at once; it is read on a 1440 × 800 desktop, where it starts under its fold — same invariant
            ("projet-pilote/", ".pilota-rotta__percorso", 800),
            ("universites-et-formation/", ".universita-filiera", 900),
            ("diplomes-et-titres/", ".persone-protezione", 900),
        ):
            page.set_viewport_size({"width": 1440, "height": height})
            page.goto(f"{live_server.url}/fr/{path}", wait_until="networkidle")
            assert page.eval_on_selector(selector, "s => s.dataset.secState") == "wait", path
            if selector == ".universita-filiera":
                # m2: the destination frame waits in black and white and develops as the route arrives
                held = page.eval_on_selector(f"{selector} .filiera__meta img", "i => getComputedStyle(i).filter")
                assert held == "grayscale(1)", held
            page.eval_on_selector(selector, "s => s.scrollIntoView({block: 'center'})")
            page.wait_for_function(
                "s => document.querySelector(s).dataset.secState === 'in'", arg=selector, timeout=4000
            )
            page.wait_for_timeout(2600)
            # the section's own: the head's one load sequence (lane S's frontispiece halo, 1.75 s + 2.2 s) is not it
            running = page.evaluate(
                "s => document.getAnimations().filter(a => a.playState === 'running' && "
                "(!a.timeline || a.timeline instanceof DocumentTimeline) && "
                "a.effect && a.effect.target && document.querySelector(s).contains(a.effect.target)).length",
                selector,
            )
            assert running == 0, (path, running)
            if selector == ".universita-filiera":
                developed = page.eval_on_selector(f"{selector} .filiera__meta img", "i => getComputedStyle(i).filter")
                assert developed == "none", developed
    finally:
        context.close()


def test_under_reduced_motion_no_state_is_written_and_nothing_runs(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        for path in ("parcours/", "projet-pilote/", "formation/", "institutions/"):
            page.goto(f"{live_server.url}/fr/{path}", wait_until="networkidle")
            page.mouse.wheel(0, 2400)
            page.wait_for_timeout(600)
            assert page.evaluate("document.querySelectorAll('[data-sec-state]').length") == 0, path
            running = page.evaluate("document.getAnimations().filter(a => a.playState === 'running').length")
            assert running == 0, path
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_every_composed_frame_is_drawn_at_the_width_its_sizes_states(browser, live_server, open_pages, lang):
    frames = {
        "parcours/": [
            f'.tracciato__corsia[data-lane="{k}"] .tracciato__testa img' for k in ("work", "study", "family", "other")
        ],
        "formation/": ['figure[data-slot="training.before"] img', 'figure[data-slot="training.after"] img'],
        "universites-et-formation/": ['figure[data-slot="universities.exchange"] img'],
    }
    for width, height in ((1600, 900), (1440, 900), (1199, 800), (1024, 768), (768, 1024), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        try:
            for path, selectors in frames.items():
                page.goto(f"{live_server.url}/{lang}/{path}", wait_until="load")
                for selector in selectors:
                    state = page.evaluate(DRAWN, selector)
                    assert abs(state["drawn"] - state["stated"]) <= 1.5, (lang, width, path, selector, state)
        finally:
            context.close()


#: the route board after a choice: the bar and the chosen lane's boxes, the board's height, the stations still drawn,
#: the count line and where it stands, the inks and opacities of the lanes, the checked radio
CHOSEN = """(key) => {
  const box = el => el.getBoundingClientRect();
  const bar = box(document.querySelector('.percorsi-scelta'));
  const lanes = [...document.querySelectorAll('.tracciato__corsia')];
  const lane = box(document.querySelector(`.tracciato__corsia[data-lane="${key}"]`));
  const count = [...document.querySelectorAll('.percorsi-conto__riga')].filter(s => getComputedStyle(s).display !== 'none');
  return {
    barTop: bar.top, barBottom: bar.bottom, laneTop: lane.top, laneBottom: lane.bottom, vh: innerHeight,
    board: Math.round(box(document.querySelector('.percorsi-tracciato')).height),
    shown: [...document.querySelectorAll('.tracciato__stazione')].filter(s => box(s).height > 0).length,
    line: count.map(c => c.textContent.trim()),
    count: count.map(c => c.dataset.count),
    inBar: count.length === 1 && count.every(c => { const r = box(c); return bar.top <= r.top && r.bottom <= bar.bottom; }),
    inks: Object.fromEntries(lanes.map(l => [l.dataset.lane, getComputedStyle(l).color])),
    opacity: lanes.map(l => getComputedStyle(l).opacity),
    checked: document.querySelector('input[name="pathway-family"]:checked').value,
  };
}"""


def test_choosing_a_family_keeps_every_station_and_lights_its_lane(browser, live_server, open_pages):
    """A family chosen keeps every station in the layout, lights its lane and turns the others to the quiet ink (never an
    opacity), and its polite line says its count. Round 2 (QA_ROUND2 M1; SECTION_SYSTEM_V2 §2 B, V5.20 strict rule: the
    chip is now its radio's label, the radio at its lane's head — the old selector named a radio inside the chip): the
    choice also brings its lane under the bar, which stays in view, on a desktop as on a phone."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/", wait_until="load")
        height = page.evaluate(
            "Math.round(document.querySelector('.percorsi-tracciato').getBoundingClientRect().height)"
        )
        page.click('.tracciato__chip[for="family-work"]')
        state = page.evaluate(CHOSEN, "work")
        assert state["checked"] == "work" and state["shown"] == 8 and state["board"] == height, state
        assert all(ink != state["inks"]["work"] for lane, ink in state["inks"].items() if lane != "work"), state
        assert set(state["opacity"]) == {"1"}, "the other lanes go to the quiet ink, never to an opacity"
        assert state["line"] == ["3 parcours affichés"] and state["inBar"], state
        assert 0 <= state["barTop"] and state["barBottom"] <= state["laneTop"] <= state["barBottom"] + 40, state
        # the board's far end: «Autres voies», chosen from the board's top, comes under the bar
        page.evaluate(
            "scrollTo(0, document.querySelector('.percorsi-tracciato').getBoundingClientRect().top + scrollY - 64)"
        )
        page.click('.tracciato__chip[for="family-other"]')
        state = page.evaluate(CHOSEN, "other")
        assert state["checked"] == "other" and state["shown"] == 8 and state["board"] == height, state
        assert state["barBottom"] <= state["laneTop"] <= state["barBottom"] + 40, state
        assert state["line"] == ["1 parcours affiché"] and state["inBar"], state
    finally:
        context.close()


def test_the_diplomas_definitions_open_from_the_keyboard_one_at_a_time(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/diplomes-et-titres/", wait_until="load")
        assert page.evaluate("[...document.querySelectorAll('details[name=dossier]')].filter(d => d.open).length") == 1
        page.focus("#etape-declaration summary")
        page.keyboard.press("Enter")
        opened = page.evaluate(
            "[...document.querySelectorAll('details[name=dossier]')].filter(d => d.open).map(d => d.closest('li').id)"
        )
        assert opened == ["etape-declaration"], opened
        outline = page.evaluate("getComputedStyle(document.activeElement).outlineStyle")
        assert outline != "none", "the focus stays visible"
    finally:
        context.close()


def test_without_script_every_station_milestone_and_term_stands(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/", wait_until="load")
        assert page.locator(".tracciato__stazione:visible").count() == 8
        page.goto(f"{live_server.url}/fr/parcours/salaried_work/", wait_until="load")
        assert page.locator(".filo__tappa:visible").count() == 5
        assert page.locator("details[name='termini'] summary:visible").count() >= 3
        page.goto(f"{live_server.url}/fr/projet-pilote/", wait_until="load")
        assert page.locator("[data-diagram='pilot-sequence'] .linea__step:visible").count() == 8
        assert page.locator("[data-notice='pilot-not-authorised'] .notice:visible").count() == 1
    finally:
        context.close()


#: every word of a label on ONE line (a word's range never spans two lines), and every label's box (the union of its
#: lines) at least 16 px from every other label's — horizontally or vertically
LABELS = """() => {
  const labels = [...document.querySelectorAll('[data-diagram="pilot-sequence"] .linea__label')];
  const broken = [];
  const boxes = labels.map(p => {
    const node = p.firstChild, text = node.textContent;
    let at = 0;
    for (const word of text.split(/(\\s+)/)) {
      if (word.trim()) {
        const range = document.createRange(); range.setStart(node, at); range.setEnd(node, at + word.length);
        if (new Set([...range.getClientRects()].map(r => Math.round(r.top))).size > 1) broken.push(word);
      }
      at += word.length;
    }
    const range = document.createRange(); range.selectNodeContents(p);
    const rects = [...range.getClientRects()];
    return {text: text.trim(), hyphens: getComputedStyle(p).hyphens,
      left: Math.min(...rects.map(r => r.left)), right: Math.max(...rects.map(r => r.right)),
      top: Math.min(...rects.map(r => r.top)), bottom: Math.max(...rects.map(r => r.bottom))};
  });
  let gap = Infinity, pair = null;
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    const apart = Math.max(b.left - a.right, a.left - b.right, b.top - a.bottom, a.top - b.bottom);
    if (apart < gap) { gap = apart; pair = [a.text, b.text]; }
  }
  return {count: boxes.length, broken, gap: Math.round(gap), pair, hyphens: [...new Set(boxes.map(b => b.hyphens))]};
}"""


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_the_pilot_s_capitals_never_break_inside_a_word(browser, live_server, open_pages, lang):
    """Lane S's review, n4 («ACCOMPAGNE-» / «MENT» at eight a row), and QA_ROUND1 M1: the pilot's eight locked labels
    keep whole words AND their own room at the laptop widths — no two labels' boxes meet, every two at least 16 px apart
    (at 1280 and 1366 «ACCOMPAGNEMENT» ran 7–8 px into «SUIVI» on one line; §3.3's «gently stepped» row sets neighbours
    on the two sides of the route). V5.20 strict rule: the predicate `lines <= words` let an overlap through — this one
    measures every word and every box, a stronger invariant than fdd6e34's «eight a row only from 90 rem»."""
    for width in (1280, 1366, 1440, 1920):
        context = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce")
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/{lang}/projet-pilote/", wait_until="load")
            state = page.evaluate(LABELS)
            assert state["count"] == 8, (lang, width, state)
            assert state["hyphens"] == ["manual"], (lang, width, state)
            assert not state["broken"], (lang, width, state["broken"], "a word broken across lines")
            assert state["gap"] >= 16, (lang, width, state["pair"], state["gap"])
        finally:
            context.close()


def test_the_pilot_s_status_plate_ends_the_route_across_its_width(browser, live_server, open_pages):
    """QA_ROUND1 M2 e: the mandatory notice is the route's terminal plate, under it and across the route's width — no
    empty half beside it; from 80 rem the route runs on past station 8 and turns down into it, dashed; station 6 is the
    page's one gold arrival (its node edged in the identity gold, §3.3)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/projet-pilote/", wait_until="load")
        state = page.evaluate("""() => {
          const ol = document.querySelector('[data-diagram="pilot-sequence"] ol').getBoundingClientRect();
          const plate = document.querySelector('[data-notice="pilot-not-authorised"] .notice').getBoundingClientRect();
          const steps = document.querySelectorAll('[data-diagram="pilot-sequence"] .linea__step');
          const turn = getComputedStyle(steps[7], '::before'), arrival = steps[5].querySelector('p');
          return {olLeft: ol.left, olRight: ol.right, olBottom: ol.bottom, left: plate.left, right: plate.right,
                  top: plate.top, turn: turn.content, arrival: getComputedStyle(arrival).fontWeight,
                  said: arrival.textContent.trim().length,
                  tiles: document.querySelectorAll('[data-diagram="pilot-sequence"] .sez-tile').length};
        }""")
        assert abs(state["left"] - state["olLeft"]) <= 1 and abs(state["right"] - state["olRight"]) <= 1, state
        assert state["top"] > state["olBottom"], state
        # FINAL MICRO-PASS §5 A2, A3 (V5.20 strict rule: the route's dashed turn into the plate and station 6's gold
        # node and light left with the stations' tiles): no turn, no tile; the arrival is its words, at the title's weight
        assert state["turn"] in ("none", "normal") and state["tiles"] == 0, state
        assert state["arrival"] == "500" and state["said"], state
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_on_a_phone_the_family_choice_is_one_bar_and_brings_its_lane_under_it(browser, live_server, open_pages, lang):
    """QA_ROUND1 M3: on a phone the choice and its count are one sticky bar with its own ground — the legend kept for
    assistive technology, never printed over the board —, and a choice shows its result where the hand is.
    QA_ROUND2 M1 (V5.20 strict rule; SECTION_SYSTEM_V2 §0.1 and §2 B «nothing leaves the layout»): round 1 folded the
    other lanes, which stranded a reader who chose deeper than about one screen into the board — the old assertion
    («only the chosen family's stations are drawn») was that fold, and it chose only at the board's top. Now a family
    is chosen by a tap on its chip after a wheel scroll to the board's top, 900 px and 1 500 px into it: the chosen lane
    lands right under the bar, the bar stays in view, nothing leaves the layout (the board's height and its eight
    stations unchanged) and the count is read in the bar. «Tous» lights every lane again."""
    context = browser.new_context(
        viewport={"width": 390, "height": 844}, reduced_motion="reduce", has_touch=True, is_mobile=True
    )
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/parcours/", wait_until="load")
        bar = page.evaluate("""() => {
          const bar = document.querySelector('.percorsi-scelta');
          const board = bar.closest('fieldset');
          const legend = board.querySelector(':scope > legend');
          const box = legend.getBoundingClientRect();
          return {sticky: getComputedStyle(bar).position, ground: getComputedStyle(bar).backgroundColor,
                  holds: !!bar.querySelector('label.tracciato__chip') && !!bar.querySelector('[aria-live="polite"]'),
                  radios: board.querySelectorAll('input[type="radio"][name="pathway-family"]').length,
                  legend: [box.width, box.height], name: legend.textContent.trim()};
        }""")
        assert bar["sticky"] == "sticky" and bar["holds"] and bar["radios"] == 5, bar
        assert bar["ground"] not in ("rgba(0, 0, 0, 0)", "transparent"), bar
        assert bar["legend"][0] <= 1 and bar["legend"][1] <= 1 and bar["name"], bar
        top = page.evaluate("document.querySelector('.percorsi-tracciato').getBoundingClientRect().top + scrollY")
        height = page.evaluate(
            "Math.round(document.querySelector('.percorsi-tracciato').getBoundingClientRect().height)"
        )
        page.mouse.move(195, 600)
        for depth, key in ((0, "other"), (900, "other"), (1500, "work"), (900, "family"), (1500, "study")):
            target = int(top) - 64 + depth
            for _ in range(40):
                gap = target - page.evaluate("scrollY")
                if abs(gap) < 8:
                    break
                page.mouse.wheel(0, max(-400, min(400, gap)))
                page.wait_for_timeout(60)
            page.tap(f'.tracciato__chip[for="family-{key}"]')
            page.wait_for_timeout(150)
            state = page.evaluate(CHOSEN, key)
            where = (lang, depth, key, state)
            assert state["checked"] == key, where
            assert 0 <= state["barTop"] and state["barBottom"] <= 160, where  # the bar in view, under the letterhead
            assert state["barBottom"] <= state["laneTop"] <= state["barBottom"] + 40, where  # the lane under the bar
            assert state["board"] == height and state["shown"] == 8, where  # nothing leaves the layout
            assert state["count"] == [key] and state["inBar"], where  # the chosen family's count, read in the bar
        page.tap('.tracciato__chip:has(input[value="all"])')
        state = page.evaluate(CHOSEN, "work")
        assert state["checked"] == "all" and len(set(state["inks"].values())) == 1 and state["shown"] == 8, state
    finally:
        context.close()


def test_the_sheet_s_rail_is_in_reach_from_every_part(browser, live_server, open_pages):
    """QA_ROUND1 M4, §3.5 PS-1: from 64 rem the page's index is ONE sticky rail beside every part — Étapes, Autorités,
    Avertissements, Ressources, Orientation —, in the viewport wherever the reader is, the part in view marked
    (aria-current="location"); below 64 rem the head's «Sommaire» is the index."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/salaried_work/", wait_until="networkidle")
        for part, label in (
            ("#etapes", "Étapes"),
            ("#autorites", "Autorités"),
            ("#avertissements", "Avertissements"),
            ("#ressources", "Ressources"),
            ("#orientation", "Orientation"),
        ):
            page.eval_on_selector(part, "e => e.scrollIntoView({block: 'start'})")
            page.mouse.wheel(0, 40)
            page.wait_for_function(
                "label => [...document.querySelectorAll('.scheda-rail a[aria-current]')]"
                ".map(a => a.textContent.trim()).includes(label)",
                arg=label,
                timeout=4000,
            )
            box = page.eval_on_selector(
                ".scheda-rail__lastra", "e => { const r = e.getBoundingClientRect(); return [r.top, r.bottom]; }"
            )
            assert box[0] >= 56 and box[1] <= 900, (part, box)
        assert page.locator(".pathway-entrance .sommaire").is_hidden()
    finally:
        context.close()
    context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/salaried_work/", wait_until="load")
        assert page.locator(".scheda-rail").is_hidden() and page.locator(".pathway-entrance .sommaire").is_visible()
    finally:
        context.close()


#: the Formation notice: its words' width in rem, its box against its frame's, and any word broken across lines
NOTICE = """() => {
  const note = document.querySelector('[data-notice="training-before"]');
  const p = note.querySelector('p'), node = p.firstChild, text = node.textContent;
  const broken = []; let at = 0;
  for (const word of text.split(/(\\s+)/)) {
    if (word.trim()) {
      const range = document.createRange(); range.setStart(node, at); range.setEnd(node, at + word.length);
      if (new Set([...range.getClientRects()].map(r => Math.round(r.top))).size > 1) broken.push(word);
    }
    at += word.length;
  }
  const frame = document.querySelector('figure[data-slot="training.before"] picture').getBoundingClientRect();
  const box = note.getBoundingClientRect();
  return {words: p.getBoundingClientRect().width / parseFloat(getComputedStyle(document.documentElement).fontSize),
          note: [box.left, box.right, box.top], frame: [frame.left, frame.right, frame.bottom], broken};
}"""


def test_the_formation_notice_keeps_a_reading_measure_under_its_frame(browser, live_server, open_pages):
    """QA_ROUND1 M5: the legally required notice («… aucune attestation n’a valeur d’approbation administrative.») is
    docked under its frame at the frame's width — at least 16 rem of words from 80 rem, never a word broken (it was an
    83–135 px column beside the frame, «d’approbati|on»)."""
    for width, height in ((1024, 768), (1280, 800), (1440, 900)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/fr/formation/", wait_until="load")
            state = page.evaluate(NOTICE)
            assert not state["broken"], (width, state)
            note, frame = state["note"], state["frame"]
            assert abs(note[0] - frame[0]) <= 1 and abs(note[1] - frame[1]) <= 1, (width, state)
            assert note[2] >= frame[2], (width, state)
            if width >= 1280:
                assert state["words"] >= 16, (width, state)
        finally:
            context.close()


def test_an_arabic_page_keeps_its_french_titles_on_their_marker_s_edge(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/ar/parcours/salaried_work/", wait_until="load")
        gaps = page.evaluate("""() => [...document.querySelectorAll('.filo__tappa')].map(li => {
          const node = li.querySelector('.filo__num').getBoundingClientRect();
          const title = li.querySelector('.filo__titolo');
          const range = document.createRange(); range.selectNodeContents(title);
          const text = range.getBoundingClientRect();
          return Math.round(node.left - text.right);
        })""")
        # FINAL MICRO-PASS §5 A2 (V5.20 strict rule): the node gave way to the quiet marker; the title hangs from it
        assert len(gaps) == 5 and all(0 <= gap <= 120 for gap in gaps), gaps
        # an Arabic lane name is never tracked (a tracked Arabic word breaks apart)
        page.goto(f"{live_server.url}/ar/parcours/", wait_until="load")
        labels = page.evaluate(
            "[...document.querySelectorAll('.tracciato__nome')].map(el => getComputedStyle(el).letterSpacing)"
        )
        assert len(labels) == 4 and all(value in ("normal", "0px") for value in labels), labels
        # V5.20, FINAL_DELIVERY_V2 R7′ / V5.27 cited (the v524-pub1 steward): the Arabic board reads each pathway's title
        # in its provisional Arabic and, the description hidden off its sheet, draws no line on a station that links the
        # sheet — so no French run is left in a card (stronger than QA_ROUND2 m2's 28 px French leading, which had none
        # left to read), and QA_ROUND1 m1's «one edge» reads across the eight cards: every title starts at the same
        # distance from its card's reading (right) edge, beside its numeral
        cards = page.evaluate(
            "[...document.querySelectorAll('.tracciato__carta')].map(card => {"
            " const r = document.createRange(); r.selectNodeContents(card.querySelector('.tracciato__titolo'));"
            " const right = Math.max(...[...r.getClientRects()].map(x => x.right));"
            " return {inset: Math.round(card.getBoundingClientRect().right - right), link: card.tagName === 'A',"
            " french: card.querySelectorAll('[lang=\"fr\"]').length, lines: card.querySelectorAll('.tracciato__riga').length};"
            " })"
        )
        insets = [card["inset"] for card in cards]
        assert len(cards) == 8 and max(insets) - min(insets) <= 2, cards
        assert all(card["french"] == 0 for card in cards), cards
        assert all(card["lines"] == 0 for card in cards if card["link"]), cards
        # the pilot's route runs with the page, station 1 on the reading edge, though its list carries the labels'
        # lang="fr" (the library's French-run rule would turn the list itself left-to-right)
        page.goto(f"{live_server.url}/ar/projet-pilote/", wait_until="load")
        # FINAL MICRO-PASS §5 A2 (V5.20 strict rule: the stations' tiles left — each is its quiet marker, four to a row
        # from 48 rem): each row of four runs right to left, station 1 and station 5 on the reading edge
        xs = page.evaluate(
            "[...document.querySelectorAll('[data-diagram=\"pilot-sequence\"] .linea__num')]"
            ".map(s => Math.round(s.getBoundingClientRect().right))"
        )
        assert len(xs) == 8 and xs[:4] == sorted(xs[:4], reverse=True) and xs[4:] == sorted(xs[4:], reverse=True), xs
        assert xs[0] == xs[4] == max(xs), xs
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_institutions_head_sets_its_recipients_as_one_annotation(browser, live_server, open_pages, lang):
    """QA_ROUND2 M2 (SECTION_SYSTEM_V2 §3.7 IN-H «the locked recipients sentence becomes a side annotation»; §1 rule 6),
    restated under V5.20 for V5.30 Fast Visual Variety Correction §7 INSTITUTIONS («Do not make every institutional
    relationship an arc»): the small six-seat hemicycle is gone; at 1440 and 390 the sentence is an annotation (15 px), not
    a second lead; in Arabic the lead and the note hang from the same reading edge — since V5.27 / FINAL_DELIVERY_V2 R7′
    (V5.20, the v524-pub1 steward) both in the page's Arabic (the C-UI renderings), right to left, where they were French
    boxes."""
    for width, height in ((1440, 900), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/{lang}/collaboration/institutions/", wait_until="load")
            state = page.evaluate("""() => {
              const box = el => el.getBoundingClientRect();
              const p = document.querySelector('.emiciclo-nota__frase');
              const lead = document.querySelector('header.ingresso .ingresso__lead');
              return {drawing: document.querySelectorAll('.emiciclo-nota__disegno, .emiciclo-nota svg').length,
                      font: parseFloat(getComputedStyle(p).fontSize), leadFont: parseFloat(getComputedStyle(lead).fontSize),
                      leadBox: [box(lead).left, box(lead).right], noteBox: [box(p.closest('.emiciclo-nota')).left, box(p.closest('.emiciclo-nota')).right],
                      dirs: [getComputedStyle(lead).direction, getComputedStyle(p).direction], form: box(document.querySelector('#formulaire')).top};
            }""")
            where = (lang, width, state)
            assert state["drawing"] == 0, where
            # an annotation, not a second lead — V5.24 (TYPOGRAPHY_V2 §4.2: the ui step 15, 16 under 48 rem by the phone
            # step-up; FINAL_DELIVERY_V2 §3.5; V5.20 strict rule): the same invariant, exact — the annotation IS the ui step,
            # and under the lead (the 15.5 cap predates T's step-up and read a phone's 16 px as a second lead)
            assert state["font"] == (16 if width == 390 else 15) < state["leadFont"], where
            if lang == "ar":
                assert state["dirs"] == ["rtl", "rtl"], where  # the page's Arabic (R7′ C-UI), never a French box
                assert abs(state["leadBox"][1] - state["noteBox"][1]) <= 2, where  # hanging from one reading edge
            if width == 1440:
                assert state["form"] < height, where  # the formwork still starts in the first screen
        finally:
            context.close()


def test_the_pilot_doors_calls_start_on_one_line_and_the_sill_is_their_only_rule(browser, live_server, open_pages):
    """QA_ROUND2 m4: the two doors' calls start on one line from 48 rem (at 768 the institutions' call ran to three lines
    and started 17 px higher); m5: the help line stands on the doors' sill, its own hairline gone (a double rule)."""
    for lang, width in (("fr", 768), ("ar", 768), ("it", 1024), ("fr", 1440)):
        context = browser.new_context(viewport={"width": width, "height": 1000}, reduced_motion="reduce")
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/{lang}/projet-pilote/", wait_until="load")
            state = page.evaluate("""() => ({
              calls: [...document.querySelectorAll('.porta-pilota__azione')].map(a => Math.round(a.getBoundingClientRect().top)),
              rule: getComputedStyle(document.querySelector('.pilota-porte__aiuto')).borderTopStyle,
            })""")
            assert len(state["calls"]) == 2 and abs(state["calls"][0] - state["calls"][1]) <= 1, (lang, width, state)
            assert state["rule"] == "none", (lang, width, state)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_campus_frame_and_the_note_stand_beside_the_three_cards(browser, live_server, open_pages, lang):
    """V5.30 Fast Visual Variety Correction §7 UNIVERSITÉS, «campus imagery, stations/cards» (V5.20 strict rule; this decision
    replaces QA_ROUND2 m1, the last plate laid over the frame's edge): at 1440 and 1024 the frame stands at the reading edge
    with the band's note under it, its top on the first card's, and each card stands wholly beside it, none over it."""
    for width, height in ((1440, 900), (1024, 768)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/{lang}/universites-et-formation/", wait_until="load")
            state = page.evaluate("""() => {
              const box = (e) => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
              return {frame: box(document.querySelector('.filiera__meta')), note: box(document.querySelector('.filiera__nota')),
                      plates: [...document.querySelectorAll('.filiera__lastra')].map(box), rtl: document.dir === 'rtl'};
            }""")
            frame, note, plates = state["frame"], state["note"], state["plates"]
            assert len(plates) == 3, state
            assert abs(frame[1] - plates[0][1]) <= 2, state  # the first card's top
            assert note[1] >= frame[3] and abs(note[0] - frame[0]) <= 1 and abs(note[2] - frame[2]) <= 1, state
            for plate in plates:
                assert plate[2] <= frame[0] + 0.5 if state["rtl"] else plate[0] >= frame[2] - 0.5, state  # never over it
        finally:
            context.close()


def test_the_companies_three_moments_open_on_their_numerals(browser, live_server, open_pages):
    """Round 2 (SECTION_SYSTEM_V2 §2 F; §3.6 EN-1): each of the three moments opens on its numeral, the moments' own order.
    V5.30 Fast Visual Variety Correction §7 ENTREPRISES (V5.20 strict rule): the process's title stands under the
    quotation, on its panel. FINAL MICRO-PASS §6 B3 (V5.20; was «a station's ILE Mono numeral at 36 px»): the numeral is
    the quiet sequence marker (BRIEF §2.2) — the counter at the caption's size, tabular, «1» not «01», the first in the
    accent and the others in one quieter ink — the three on one line, each joined to the next by a 1 px hairline; they
    stand in their own band after the démarche's opening (the quotation beside the territory), the title under it."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/entreprises/", wait_until="load")
        state = page.evaluate("""() => {
          const cells = [...document.querySelectorAll('.imprese-tempi .flusso__tappa')];
          const marks = cells.map(c => { const cs = getComputedStyle(c, '::before');
            return [cs.content, cs.fontSize, cs.fontVariantNumeric, cs.color, Math.round(c.getBoundingClientRect().top)]; });
          const lines = cells.map(c => getComputedStyle(c, '::after').height);
          const caption = (() => { const p = document.createElement('i'); p.style.fontSize = 'var(--t-caption)';
            document.body.append(p); const v = getComputedStyle(p).fontSize; p.remove(); return v; })();
          const quote = document.querySelector('.imprese-citazione').getBoundingClientRect();
          const head = document.querySelector('.imprese-tempi .testa').getBoundingClientRect();
          const panel = document.querySelector('.imprese-tempi .flusso').getBoundingClientRect();
          return {marks, lines, caption, under: head.top >= quote.bottom - 1 && panel.top >= head.bottom - 1};
        }""")
        marks = state["marks"]
        assert len(marks) == 3 and all(m[0] == "counter(flusso)" and m[2] == "tabular-nums" for m in marks), state
        assert all(m[1] == state["caption"] for m in marks) and float(state["caption"][:-2]) <= 14, state
        assert marks[0][3] != marks[1][3] == marks[2][3], (state, "the first in the accent")
        assert len({m[4] for m in marks}) == 1 and state["lines"] == ["1px"] * 3, state
        assert state["under"], state
    finally:
        context.close()
