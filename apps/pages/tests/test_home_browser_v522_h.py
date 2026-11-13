"""
V5.22 — HOMEPAGE COMPOSITION V2 in a real layout engine (SECTION_SYSTEM_V2 §2.0, §3.1, §5.3, §9.9; lane H).

* the hand-off (V5.30 Fast Visual Variety Correction §5; V5.20 strict rule): no line crosses from the hero into the
  orientation, the band follows the hero and its origin seal sits in its own cell, at the desktop and tablet widths;
* the trigger contract on the real page: a section below the fold waits, plays its verbs once and holds nothing
  (V5.20: a finished entrance leaves document.getAnimations()); under reduced motion nothing is written and the page
  is its designed still — every line drawn, every photograph in colour;
* the pathways' index from the keyboard: the ARIA tabs pattern, the stage changing in place (the section never moves);
* the pilot's panels draw what their `sizes` say (object-fit: cover: the drawn width is the box's or its height's 2:3);
* the reserved row's key turns on its own button, never under reduced motion;
* the phone's doors: one rail the keyboard crosses plate by plate, every focused plate whole in the rail;
* round 1 (QA_ROUND1, label v522-h-improve1): the hand-off without an empty run, the panel's tile at the route's origin,
  «la protezione» on the reading edge, the gold key beside its button, the arch's square foot and its drawn doorway, the
  Arabic page's French runs each on its own edge and its folio in its own face;
* round 2 (QA_ROUND2, label v522-h-improve2): on the Arabic page every French run hangs from one edge (the reserved
  row's title and sentence, the colophon's name and answer, the route's captions at a caption's measure) and a phone's
  disclosure row reads tile · title … chevron; the phone index inks in its order;
* final fix round (QA_ROUND3, label v522-h-fix): the doorway's sill and outline and the phone doors' lunettes are
  PAINTED as one line each, growing from their foot at the verb's pace, at 1× and 2× (round 2's model assertion read a
  dash the reviewer's 1.25× display did not paint; the class of that defect — a dash on a non-scaling stroke, laid in
  the screen's own pixels — is guarded structurally by test_home_v522_h.py, since the headless shell these tests run
  lays such a dash at 1× whatever the screen's factor); the Arabic index's eight French titles stand on one edge, the
  reading edge's, at the eight review widths; the colophon's connector ran on its folio's rule (V5.30: it stands
  down on the home, the band's one motif the Italy + Morocco field);
* after the final review (v522-h-final-qa1, label v522-h-final-improve): with the catalogue's entry for the pilot's
  lead, the pilot's statement — the French title, the lead in the page's language, the link — shares the seam's axis
  from 64 rem and one reading edge below, in the four languages at the eight review widths, and its lead never ends on
  one word (F-M1, F-m2).
"""

from __future__ import annotations

import os

import pytest

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


@pytest.fixture
def phase3_live(seeded):
    """Open gate G3 for the live server without freezing time (Playwright needs a real clock)."""
    from core import flags
    from core.models import FeatureFlag

    FeatureFlag.objects.update_or_create(
        key="phase3_public", defaults={"enabled": True, "enabled_from": None, "enabled_until": None}
    )
    flags.invalidate()
    yield
    flags.invalidate()


def _open(browser, live_server, path, width, height, motion="no-preference"):
    context = browser.new_context(
        viewport={"width": width, "height": height}, device_scale_factor=1, reduced_motion=motion
    )
    page = context.new_page()
    page.goto(live_server.url + path, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    return context, page


def _until_ready(page, selector):
    """home.js marks a tabs root `data-ready` once its tabs are wired (V5.31, lane B)."""
    for _ in range(40):
        if page.evaluate(f"!!document.querySelector('{selector}[data-ready]')"):
            return
        page.wait_for_timeout(50)
    raise AssertionError(("the tabs never became ready", selector))


def _scroll_through(page, step=0.5, pause=180):
    height = page.evaluate("innerHeight")
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.mouse.wheel(0, int(height * step))
        y += int(height * step)
        page.wait_for_timeout(pause)


_MEET = """() => {
  const sec = document.querySelector('.home-orientation').getBoundingClientRect();
  // RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B «il viaggio»): the
  // first station is the first moment's tab — its glyph tile where the marker stood, its keyword its words
  const first = document.querySelector('.home-orientation .viaggio__voce');
  const cell = first.getBoundingClientRect(), num = first.querySelector('.viaggio__glifo').getBoundingClientRect();
  const label = first.querySelector('.viaggio__nome'), words = label.getBoundingClientRect();
  // RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§8–§9, lane A):
  // the hero's statement is now followed by the ecosystem's introduction, part of the hero's group (no section key
  // of its own) — the band follows THAT, with no gap
  const group = document.querySelector('.he + .home-intro') || document.querySelector('.he');
  const heroBox = group.getBoundingClientRect();
  return {drawn: document.querySelectorAll('.he__soglia, .he__soglia-linea, .orienta__soglia').length,
          heroBottom: heroBox.bottom, top: sec.top,
          seals: document.querySelectorAll('.home-orientation .sigillo').length,
          num: [num.top, num.bottom], said: label.textContent.trim(),
          words: [words.left, words.right, words.top, words.bottom],
          cell: [cell.left, cell.right, cell.top, cell.bottom]};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_line_crosses_from_the_hero_and_the_origin_seal_sits_in_its_cell(browser, live_server, phase3_live, lang):
    """V5.30 Fast Visual Variety Correction §5, §7 HOME (V5.20 strict rule; this decision replaces H0 «la soglia»,
    §3.1, the line that ran from the statement down to the seal's sill): no line is drawn between the two bands; the
    band follows the hero with no gap, and the route's origin seal sits inside its own cell of the panel. Measured at
    rest (reduced motion). FINAL MICRO-PASS §5 A1 (V5.20 strict rule: the origin's seal left — the route opens on its
    quiet marker): no seal in the band; the first station's marker stands on its cell's rows and its words inside its
    cell, said."""
    for width, height in ((1440, 900), (1024, 768), (768, 1024)):
        context, page = _open(browser, live_server, f"/{lang}/", width, height, motion="reduce")
        try:
            m = page.evaluate(_MEET)
            where = (lang, width)
            assert m["drawn"] == 0, where
            assert abs(m["top"] - m["heroBottom"]) <= 1, (where, m)
            words, cell = m["words"], m["cell"]
            assert m["seals"] == 0 and m["said"], (where, m)
            assert cell[0] <= words[0] and words[1] <= cell[1], (where, m)
            assert cell[2] <= words[2] and words[3] <= cell[3], (where, m)
            assert cell[2] <= m["num"][0] and m["num"][1] <= cell[3], (where, m)
        finally:
            context.close()


_TIMED = """() => document.getAnimations().filter(a => {
  const t = a.timeline;
  const linked = ('ScrollTimeline' in window && t instanceof ScrollTimeline)
    || ('ViewTimeline' in window && t instanceof ViewTimeline);
  return !(t && linked);
}).map(a => a.animationName || a.constructor.name)"""


def test_each_section_waits_plays_once_and_holds_nothing(browser, live_server, phase3_live):
    context, page = _open(browser, live_server, "/fr/", 1440, 900)
    try:
        states = page.evaluate("() => [...document.querySelectorAll('[data-sec]')].map(s => s.dataset.secState || '')")
        assert "wait" in states, "the sections below the fold wait for the reader"
        _scroll_through(page)
        page.wait_for_timeout(3000)
        after = page.evaluate(
            "() => [...document.querySelectorAll('[data-sec]')].map(s => [s.dataset.sec, s.dataset.secState || ''])"
        )
        assert all(state in ("in", "") for _sec, state in after), after
        assert [sec for sec, state in after if state == "in"], "the sections played their verbs"
        # V5.20: a finished entrance leaves getAnimations() (fill backwards); only scroll-linked progress stays attached
        assert page.evaluate(_TIMED) == [], "a time-based animation is still held"
        # text never waits: no word of a section is transparent at any time after the scroll
        hidden = page.evaluate(
            "() => [...document.querySelectorAll('main .sez :is(h2,h3,p,li,a)')]"
            ".filter(e => getComputedStyle(e).opacity === '0').length"
        )
        assert hidden == 0
    finally:
        context.close()


def test_reduced_motion_writes_no_state_and_draws_the_still(browser, live_server, phase3_live):
    context, page = _open(browser, live_server, "/fr/", 1440, 900, motion="reduce")
    try:
        _scroll_through(page)
        still = page.evaluate(
            """() => ({
              states: [...document.querySelectorAll('[data-sec]')].filter(s => s.dataset.secState).length,
              lines: document.querySelectorAll('.he__soglia-linea, .orienta__soglia, .pilota__filo').length,
              grey: [...document.querySelectorAll('.pilota-scena img')].map(i => getComputedStyle(i).filter),
              running: document.getAnimations().length,
            })"""
        )
        assert still["states"] == 0, still
        assert still["lines"] == 0, ("V5.30 Fast Visual Variety Correction §5: no such line is left to draw", still)
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§18, lane A): the
        # diptych's two halves stand on the stage —
        # both read, both in colour (the list is never empty: stronger than a selector that could match nothing)
        assert len(still["grey"]) == 2 and all(f in ("none", "grayscale(0)") for f in still["grey"]), still
        assert still["running"] == 0, still
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_pathways_index_works_from_the_keyboard_and_the_stage_never_moves(browser, live_server, phase3_live, lang):
    context, page = _open(browser, live_server, f"/{lang}/", 1440, 900)
    try:
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B
        # «l'esploratore»): the explorer is home.js's tabs — ready when it marks its root; the CSP allows no
        # page-side polling, so the test polls
        _until_ready(page, ".home-pathways [data-tabs]")
        section = page.locator(".home-pathways")
        section.scroll_into_view_if_needed()
        before = page.evaluate("document.querySelector('.home-pathways').getBoundingClientRect().height")
        tabs = page.locator(".home-pathways [role='tab']")
        assert tabs.count() == 8
        assert page.locator(".home-pathways [role='tablist'][aria-orientation='vertical']").count() == 1
        tabs.first.focus()
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowDown")
        selected = page.evaluate(
            "() => [...document.querySelectorAll('.home-pathways [role=tab]')]"
            ".findIndex(t => t.getAttribute('aria-selected') === 'true')"
        )
        assert selected == 2
        shown = page.evaluate(
            "() => [...document.querySelectorAll('.home-pathways [role=tabpanel]')]"
            ".filter(p => getComputedStyle(p).visibility !== 'hidden').map(p => p.id)"
        )
        assert shown == ["parcours-training-in-origin-country"], shown
        page.keyboard.press("End")
        page.keyboard.press("Home")
        after = page.evaluate("document.querySelector('.home-pathways').getBoundingClientRect().height")
        assert abs(after - before) <= 1, ("a selection never moves the page (CLS 0)", before, after)
        focused = page.evaluate("document.activeElement.getAttribute('aria-selected')")
        assert focused == "true"
    finally:
        context.close()


_SIZES = """(slot) => {
  const img = document.querySelector(`figure[data-slot="${slot}"] img`);
  // split on the top-level commas only: a length may hold max(), clamp() and their own commas
  const parts = [];
  let depth = 0, from = 0;
  for (let i = 0; i < img.sizes.length; i++) {
    const c = img.sizes[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if (c === ',' && depth === 0) { parts.push(img.sizes.slice(from, i).trim()); from = i + 1; }
  }
  parts.push(img.sizes.slice(from).trim());
  let length = parts[parts.length - 1];
  for (const part of parts) {
    const m = part.match(/^(\\([^()]*\\))\\s+(\\S.*)$/);
    if (!m) { length = part; break; }
    if (matchMedia(m[1]).matches) { length = m[2]; break; }
  }
  const layout = document.documentElement.clientWidth;
  const probe = document.createElement('div');
  probe.style.position = 'absolute';
  probe.style.inlineSize = length.replace(/(\\d+(?:\\.\\d+)?)vw/g, (_, n) => `calc(${layout}px * ${n} / 100)`);
  document.body.append(probe);
  const sizes = probe.getBoundingClientRect().width;
  probe.remove();
  const box = img.getBoundingClientRect();
  const ratio = img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : 2 / 3;
  const fit = getComputedStyle(img).objectFit;
  const drawn = fit === 'cover' ? Math.max(box.width, box.height * ratio) : box.width;
  return {sizes, drawn, box: [box.width, box.height], fit, current: img.currentSrc.split('/').pop()};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_pilot_panels_and_the_ecosystem_frame_draw_what_their_sizes_say(browser, live_server, phase3_live, lang):
    """Lane M's request (QA/v522/m/NOTES.md §9.10): drawn = `sizes`. A panel is drawn by `cover`, so the width the
    photograph is drawn at is the box's, or its height's 2:3 when the panel is taller than wide; the ecosystem's frame
    under the arch is drawn at its box. Within 1.5 px, no under-fetch, every width."""
    for width, height, dpr_note in (
        (1440, 900, "desktop"),
        (1280, 800, "laptop"),
        (1024, 768, "64rem"),
        (768, 1024, "tablet"),
        (390, 844, "phone"),
    ):
        context, page = _open(browser, live_server, f"/{lang}/", width, height, motion="reduce")
        try:
            for slot in ("home.pilot.cedar", "home.pilot.marble", "home.ecosystem"):
                page.locator(f'figure[data-slot="{slot}"]').scroll_into_view_if_needed()
                page.wait_for_timeout(150)
                m = page.evaluate(_SIZES, slot)
                assert abs(m["sizes"] - m["drawn"]) <= 1.5 or m["sizes"] > m["drawn"], (lang, dpr_note, slot, m)
                assert m["sizes"] - m["drawn"] <= max(24, 0.06 * m["drawn"]), (lang, dpr_note, slot, "over-fetch", m)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_phone_doors_are_one_rail_the_keyboard_crosses_plate_by_plate(browser, live_server, phase3_live, lang):
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (agent B, point 5): the phone's rail
    # of doors is not drawn any more (it repeated the hero's four doors) — the keyboard crosses the four doors where
    # the hero draws them: four links in order, each focused whole inside the page, and the page never scrolls sideways
    context, page = _open(browser, live_server, f"/{lang}/", 390, 844)
    try:
        assert page.evaluate("getComputedStyle(document.querySelector('.home-entrances')).display") == "none"
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE PRECISION PASS of 11 Nov 2026 (§3: on a phone the four
        # descriptions were lost — «restore them with an accessible progressive pattern on the hero's own doors»).
        # Old invariant: Tab crosses four links in order. New, stronger: Tab crosses door by door — the door's link,
        # then its own disclosure (a real button, a 44 px target) — each focused whole inside the page; the keyboard
        # opens a door's sentence (Enter), one at a time, the sentence is then drawn inside the page and is the one the
        # link is described by; the page never scrolls sideways, closed or open
        page.locator(".he-origin__link").first.focus()
        seen = []
        for n in range(4):
            box = page.evaluate(
                """() => { const a = document.activeElement, r = a.getBoundingClientRect();
                   return {cls: a.className, href: a.getAttribute('href'), left: r.left, right: r.right,
                           vw: document.documentElement.clientWidth}; }"""
            )
            assert "he-origin__link" in box["cls"], box
            assert box["left"] >= -1 and box["right"] <= box["vw"] + 1, (lang, "a focused door stands whole", box)
            seen.append(box["href"])
            page.keyboard.press("Tab")
            page.wait_for_timeout(350)
            more = page.evaluate(
                """() => { const b = document.activeElement, t = getComputedStyle(b, '::before');
                   const r = b.getBoundingClientRect(), link = b.closest('.he-origin').querySelector('a');
                   return {tag: b.tagName, cls: b.className, expanded: b.getAttribute('aria-expanded'),
                           controls: b.getAttribute('aria-controls'), described: link.getAttribute('aria-describedby'),
                           named: !!b.getAttribute('aria-label'), left: r.left, right: r.right,
                           target: r.width - 2 * parseFloat(t.insetInlineStart),
                           vw: document.documentElement.clientWidth}; }"""
            )
            assert more["tag"] == "BUTTON" and "he-origin__more" in more["cls"] and more["named"], (lang, n, more)
            assert more["expanded"] == "false" and more["controls"] in more["described"].split(), (lang, n, more)
            assert more["target"] >= 44 and more["left"] >= -11 and more["right"] <= more["vw"] + 1, (lang, n, more)
            page.keyboard.press("Enter")
            page.wait_for_timeout(350)
            opened = page.evaluate(
                """() => { const g = document.getElementById(document.activeElement.getAttribute('aria-controls'));
                   const r = g.getBoundingClientRect();
                   return {open: [...document.querySelectorAll('[data-origin-more]')]
                             .map(b => b.getAttribute('aria-expanded')),
                           w: r.width, h: r.height, left: r.left, right: r.right, text: g.textContent.trim().length,
                           vw: document.documentElement.clientWidth,
                           page: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
            )
            assert opened["open"] == ["true" if k == n else "false" for k in range(4)], (lang, "one at a time", opened)
            assert opened["w"] > 250 and opened["h"] > 20 and opened["text"] > 20, (
                lang,
                "the sentence is drawn",
                opened,
            )
            assert opened["left"] >= -1 and opened["right"] <= opened["vw"] + 1 and opened["page"] <= 0, (lang, opened)
            page.keyboard.press("Tab")
            page.wait_for_timeout(350)
        assert len(set(seen)) == 4, (lang, "four doors, each its own way", seen)
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
    finally:
        context.close()


# ---------------------------------------------------------------------------------------------- round 1 (QA_ROUND1)

_ROUND1 = """() => {
  const box = (b) => ({left: b.left, right: b.right, top: b.top, bottom: b.bottom, width: b.width, height: b.height});
  const R = (sel) => { const e = document.querySelector(sel); return e ? box(e.getBoundingClientRect()) : null; };
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  const probe = document.createElement('span');
  probe.style.color = 'var(--identity-key)';
  document.body.append(probe);
  const gold = getComputedStyle(probe).color;
  probe.remove();
  const pic = document.querySelector('.home-ecosystem .eco-split__media picture');
  const label = document.querySelector('.colofone__label');
  // RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B): the stage is the
  // explorer's, the route the journey's moments, the tablet the FAQ preview's grid, the plate the fraud band's
  const panel = document.querySelector('.home-pathways .esplora__pannello[data-on]');
  const edge = (r) => (rtl ? r.right : r.left);
  return {
    rtl, air: parseFloat(getComputedStyle(document.querySelector('.home-orientation')).paddingBlockStart),
    statement: R('.home-intro') || R('.he__body'), head: R('.home-orientation .testa'),
    seal: R('.home-orientation .viaggio__voce .sigillo'),
    tablet: R('.home-faq .domande__griglia'), plate: R('.home-antifraud .allerta'),
    // RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): no reserved row, no key
    reserved: document.querySelectorAll('.home-reserved, main .sg-g--key').length, gold,
    access: (() => { const a = [...document.querySelectorAll('header a.targa')]
                       .find((e) => e.getBoundingClientRect().width > 0);
                     return a ? a.getAttribute('href') : null; })(),
    corners: (() => { const s = getComputedStyle(pic.querySelector('img'));
                      return [s.borderTopLeftRadius, s.borderTopRightRadius,
                              s.borderBottomRightRadius, s.borderBottomLeftRadius]; })(),
    drawing: document.querySelectorAll('.home-ecosystem :is(.casa-arco, .casa-arco__disegno)').length,
    // a moment's station words hang from its keyword's edge (the tab's text column), as a label from its station
    labels: [...document.querySelectorAll('.home-orientation .viaggio__parole')].map((l) => {
      const s = getComputedStyle(l), box = l.getBoundingClientRect();
      const name = l.closest('.viaggio__voce').querySelector('.viaggio__nome').getBoundingClientRect();
      return {dir: s.direction, align: s.textAlign, gap: rtl ? name.right - box.right : box.left - name.left};
    }),
    stage: panel ? [edge(panel.querySelector('.esplora__titolo').getBoundingClientRect()),
                    edge(panel.querySelector('.parcours__descrizione').getBoundingClientRect()),
                    panel.querySelector('.esplora__titolo').getBoundingClientRect().left,
                    panel.querySelector('.parcours__descrizione').getBoundingClientRect().left] : null,
    folio: [getComputedStyle(label).fontFamily, getComputedStyle(label).letterSpacing],
  };
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_round_1_the_home_holds_its_hand_off_its_edges_its_gold_and_its_arabic_runs(
    browser, live_server, phase3_live, lang
):
    """QA_ROUND1 M1 and M2, measured at rest at 1440 × 900 (reduced motion: the designed still):
    * M1 a — the orientation's head follows the statement at the foot's own distance: no empty run of wash between them;
    * M1 b — the route's origin was the body's seal, 72 × 88; RESTATED under V5.20 for V5.30 Fast Visual Variety
      Correction §7 HOME: it is one of the panel's tiles, 48 × 48;
    * M1 c — «la protezione» hangs from the reading edge, the tablet's own edge above it, never centred;
    * M1 d, m10 — the key is drawn in the identity's gold, beside its button;
    * M1 e — the arch's foot stood square on its sill, the doorway drawn 12 px around the frame; RESTATED under V5.20
      for the owner's V5.30 (7 Nov 2026, «geometry saturation» and §4 «reduce cumulative arches/lines/outlined
      geometry»; stream A): the frame is plain — one corner, the card's, on its four corners — and NO doorway is drawn
      around it;
    * M2 a — on the Arabic page each French station label is its own left-to-right box, on its station's edge;
    * M2 b — the stage's French title and description start on one edge;
    * M2 c — the Arabic folio is never set in a Latin monospace nor tracked."""
    context, page = _open(browser, live_server, f"/{lang}/", 1440, 900, motion="reduce")
    try:
        _until_ready(page, ".home-pathways [data-tabs]")  # RESTATED under V5.20 (FINAL HOMEPAGE REBUILD, lane B)
        m = page.evaluate(_ROUND1)
        gap = m["head"]["top"] - m["statement"]["bottom"]
        # FINAL MICRO-PASS §5 A1 (C, «the head with air»; V5.20 strict rule): M1 a's foot distance (≤ 40 px) gave way to
        # the band's own air — the head stands exactly the band's top padding under the statement, never more than
        # --s-20 (80 px), nothing else between them
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§8–§9, lane A): the
        # hero's statement is followed by the
        # ecosystem's introduction (the actors), so the orientation's head is measured under THAT band's foot — the
        # same invariant: exactly the band's own air, never more than 80 px, nothing else between them
        assert abs(gap - m["air"]) <= 1 and 0 <= gap <= 80, (lang, "the head at the band's air", gap, m["air"])
        # FINAL MICRO-PASS §5 A1 (V5.20 strict rule): M1 b's origin tile left with the seal — the route opens on its
        # quiet marker, its four stations still said
        assert m["seal"] is None and len(m["labels"]) == 4, (lang, m["seal"], m["labels"])
        side = "right" if m["rtl"] else "left"
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B): the fraud
        # band's plate hangs from the reading edge the FAQ preview's grid stands on, never centred off it
        assert abs(m["plate"][side] - m["tablet"][side]) <= 1, (lang, "on the reading edge", m["plate"], m["tablet"])
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2; M1 d and m10 held a
        # row the home no longer draws): no reserved row and no key under the hero — its access stays in the header
        assert m["reserved"] == 0, (lang, "no reserved row on the home", m["reserved"])
        assert m["access"] == f"/{lang}/compte/login/", (lang, "the access stays in the header", m["access"])
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§24, lane A): the
        # frame bleeds to the viewport's reading
        # edge, so its two corners there are square and its two inner corners the card's — mirrored in Arabic
        tl, tr, br, bl = m["corners"]
        start, end = ((tr, br), (tl, bl)) if m["rtl"] else ((tl, bl), (tr, br))
        assert set(start) == {"0px"} and len(set(end)) == 1 and end[0] != "0px", (
            lang,
            "square at the bleed, the card's corner inside",
            m["corners"],
        )
        assert m["drawing"] == 0, (lang, "no doorway drawn around the frame (V5.30)", m["drawing"])
        if lang == "ar":
            # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the station labels are
            # the pilot sequence's provisional Arabic — right to left, on their start edge, hanging from their station
            # (V5.30 Fast Visual Variety Correction §7 HOME, V5.20 strict rule: a station is now a cell of the panel, so
            # the same exact invariant is read on the cell's content edge, its padding apart)
            for label in m["labels"]:
                assert label["dir"] == "rtl" and label["align"] in ("start", "right"), label
                assert abs(label["gap"]) <= 1, ("a label hangs from its station's edge", label)
            # RESTATED under V5.20 (FINAL HOMEPAGE REBUILD, lane B): since V5.27 / R7′ the stage's title and
            # description read Arabic — their one start edge is the reading edge (the right), held the same 1 px
            assert abs(m["stage"][0] - m["stage"][1]) <= 1, ("one start edge for the stage's texts", m["stage"])
            assert "mono" not in m["folio"][0].lower() and m["folio"][1] in ("0px", "normal"), m["folio"]
    finally:
        context.close()


# ---------------------------------------------------------------------------------------------- round 2 (QA_ROUND2)

_ROUND2_AR = """() => {
  const ink = (e) => { const g = document.createRange(); g.selectNodeContents(e);
                       const rs = [...g.getClientRects()].filter((q) => q.width > 0);
                       return {left: Math.min(...rs.map((q) => q.left)), right: Math.max(...rs.map((q) => q.right))}; };
  const col = document.querySelector('.colofone');
  // RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B «il viaggio»): a
  // station's words are drawn in its moment's tab, under its keyword — shown on the rail from 64 rem (the phone's
  // strip of chips names the moment only); each hangs from its keyword's edge
  const shownWords = [...document.querySelectorAll('.home-orientation .viaggio__parole')]
    .filter((l) => l.getBoundingClientRect().width > 0);
  return {
    // RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): no reserved row
    reserved: document.querySelectorAll('.home-reserved').length,
    colophon: [ink(col.querySelector('.fronte__name')), ink(col.querySelector('.fronte__name-rest')),
               ink(col.querySelector('.colofone__testo'))],
    answer: {lang: col.querySelector('.colofone__testo').getAttribute('lang') || '',
             dir: getComputedStyle(col.querySelector('.colofone__testo')).direction},
    across: shownWords.length === 4,
    labels: shownWords.map((l) => {
      const s = l.closest('.viaggio__voce').querySelector('.viaggio__nome').getBoundingClientRect();
      const box = l.getBoundingClientRect();
      return {gap: s.right - box.right, width: box.width, em: parseFloat(getComputedStyle(l).fontSize),
              lang: l.closest('[lang]').getAttribute('lang')};
    }),
  };
}"""


@pytest.mark.parametrize("width,height", [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (390, 844), (360, 780)])
def test_round_2_the_arabic_page_hangs_each_french_run_from_one_edge(browser, live_server, phase3_live, width, height):
    """QA_ROUND2 M1 a, m3, m4 on the Arabic page, at rest (SECTION_SYSTEM_V2 §1 rule 6: a French run stands in its own
    box, aligned to its own start, hanging from the page's reading edge):
    * M1 a — the reserved row's French title and its sentence start on one edge, one quotation (from 64 rem the title
      stood 430–540 px from its sentence);
    * m3 — the colophon's name, in its two parts, and the French answer start on one edge, one left-to-right box (since
      V5.27 / R7′ the answer, off its page, is the Arabic pointer line: the name keeps its one box, the line reads RTL);
    * m4 — a station's French caption stands at a caption's measure (12.5 em), never its column's; across the route it
      hangs from its own station's edge."""
    context, page = _open(browser, live_server, "/ar/", width, height, motion="reduce")
    try:
        m = page.evaluate(_ROUND2_AR)
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): M1 a held the reserved
        # row's two runs on one edge — the row is not drawn on the Arabic home either, so no run of it can hang wrong
        assert m["reserved"] == 0, (width, "no reserved row on the Arabic home", m["reserved"])
        name, rest, answer = m["colophon"]
        assert abs(name["left"] - rest["left"]) <= 1, (width, "the name in one left-to-right box", m["colophon"])
        if m["answer"]["lang"] == "fr":
            for part in (name, rest):
                assert abs(part["left"] - answer["left"]) <= 1, (width, "one left-to-right box", m["colophon"])
        else:
            # V5.27 / R7′ (V5.20, an approved decision): the quoted FAQ answer is a substantive text off its own page —
            # on /ar/ it stands in its hidden form, the Arabic pointer line, right to left and with no French `lang`
            assert m["answer"] == {"lang": "", "dir": "rtl"}, (width, m["answer"])
        for label in m["labels"]:
            # a FRENCH caption at a caption's measure (m4); since V5.27 / R7′ the labels are the pilot sequence's
            # provisional Arabic (V5.20, an approved decision): the measure is the French run's rule, the edge stays
            if label["lang"] == "fr":
                assert label["width"] <= 12.5 * label["em"] + 0.5, (width, "a caption's measure", label)
            if m["across"]:
                assert abs(label["gap"]) <= 1, (width, "on its station's edge", label)
    finally:
        context.close()


# RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§14, lane B «l'esploratore»):
# on a phone the pathways are no longer a disclosure list — the explorer's rail becomes a horizontal strip of chips
# (real tabs) above the one stage; each chip reads from its reading edge tile · title, and the chips ink in order
_ROWS = """() => [...document.querySelectorAll('.home-pathways .esplora__voce')].map((v) => {
  const tile = v.querySelector('.esplora__tessera').getBoundingClientRect();
  const g = document.createRange(); g.selectNodeContents(v.querySelector('.esplora__nome'));
  const rs = [...g.getClientRects()].filter((q) => q.width > 0);
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  return {rtl, dir: getComputedStyle(v).direction, role: v.getAttribute('role'),
          ink: [Math.min(...rs.map((q) => q.left)), Math.max(...rs.map((q) => q.right))],
          tile: [tile.left, tile.right]};
})"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_round_2_a_phone_s_disclosure_row_reads_tile_title_chevron_and_inks_in_order(
    browser, live_server, phase3_live, lang
):
    """QA_ROUND2 M1 b and m2 on a phone (390 × 844):
    * the row reads from its reading edge tile · title … chevron — on the Arabic page the French heading no longer turns
      the inserted button left to right, which put the chevron between the title and the tile;
    * the rows' titles take their rank (0 … 5, the library's six steps), so they ink in the index's order, 60 ms apart —
      an unregistered sibling-index() resolved on the title's own span and every row inked at once."""
    context, page = _open(browser, live_server, f"/{lang}/", 390, 844)
    try:
        _until_ready(page, ".home-pathways [data-tabs]")
        assert page.locator(".home-pathways [role='tablist'][aria-orientation='horizontal']").count() == 1
        rows = page.evaluate(_ROWS)
        assert len(rows) == 8, rows
        for row in rows:
            assert row["dir"] == ("rtl" if lang == "ar" else "ltr") and row["role"] == "tab", row
            if row["rtl"]:
                assert row["tile"][0] >= row["ink"][1] - 0.5, (lang, "tile · title from the reading edge", row)
            else:
                assert row["tile"][1] <= row["ink"][0] + 0.5, (lang, "tile · title from the reading edge", row)
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
        page.locator(".home-pathways").scroll_into_view_if_needed()
        for _ in range(40):  # the section's trigger (rise.js); no page-side polling: the CSP allows no eval
            if page.evaluate("document.querySelector('.home-pathways').dataset.secState") == "in":
                break
            page.wait_for_timeout(100)
        delays = page.evaluate(
            "[...document.querySelectorAll('.home-pathways .esplora__riga')]"
            ".map((s) => [getComputedStyle(s).animationName, getComputedStyle(s).animationDelay])"
        )
        assert [name for name, _delay in delays] == ["hb-rise"] * 8, delays
        assert [d for _n, d in delays] == ["0s", "0.06s", "0.12s", "0.18s", "0.24s", "0.24s", "0.24s", "0.24s"], delays
    finally:
        context.close()


# ------------------------------------------------------------------------------------------ final fix round (QA_ROUND3)


# the page scrolls smoothly for a pointer: the measured section is brought in at once, so its lines stay where measured
_CENTRE = "(sel) => document.querySelector(sel).scrollIntoView({block: 'center', behavior: 'instant'})"


@pytest.mark.parametrize("dsf", [1, 2])
def test_final_the_doorway_is_painted_as_one_line_from_its_foot(browser, live_server, phase3_live, dsf):
    """QA_ROUND3 m1 asked the ecosystem's doorway — the sill and the arch's outline drawn around the frame — to paint as
    ONE line from its foot at every pixel ratio. RESTATED under V5.20 (the strict test-update rule) for the owner's
    V5.30 (7 Nov 2026, «geometry saturation»: «arches, lines, geometric frames … repeated door forms — keep them as
    BRAND SIGNATURES, stop using them as the default»; §4 «Homepage: rebalance — reduce cumulative
    arches/lines/outlined geometry, alternate with premium photography»; stream A): the arch, its sill and its drawn
    outline left the frame, so the invariant held is the approved composition's and it is stronger than the old one's
    letter — at the reviewer's widths, a phone's and the Arabic page's, at 1× and 2×, NO line is painted around the
    frame at any time (no doorway drawing, no mask of one, no sill), the photograph opens and settles in its plain
    frame on the card's corner, and the band's ground is the Italy + Morocco field (the primitive's own guards:
    tests/frontend/test_intesa_browser_v530.py).
    The old doorway cannot silently return."""
    for width, height, lang in ((1023, 768, "fr"), (1920, 1080, "fr"), (390, 844, "fr"), (1440, 900, "ar")):
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=dsf, reduced_motion="no-preference"
        )
        page = context.new_page()
        try:
            page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            cell = (dsf, width, lang)
            assert page.evaluate("document.querySelector('.home-ecosystem').dataset.secState") == "wait", cell
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§24, lane A): the
            # frame is the media split's
            page.evaluate(_CENTRE, ".home-ecosystem .eco-split__media")
            for _ in range(60):  # the section's trigger (rise.js)
                if page.evaluate("document.querySelector('.home-ecosystem').dataset.secState") == "in":
                    break
                page.wait_for_timeout(50)
            page.wait_for_timeout(2500)
            frame = page.evaluate(
                """() => {
                  const media = document.querySelector('.home-ecosystem .eco-split__media');
                  const img = media.querySelector('img'), s = getComputedStyle(img);
                  const box = media.getBoundingClientRect(), vw = document.documentElement.clientWidth;
                  return {doorway: document.querySelectorAll(
                            '.home-ecosystem :is(.casa-arco, .casa-arco__disegno, mask)').length,
                          arch: !!media.closest('.campata'),
                          rtl: getComputedStyle(document.documentElement).direction === 'rtl',
                          edges: [box.left, vw - box.right],
                          painted: img.complete && img.naturalWidth > 0,
                          corners: [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomRightRadius,
                                    s.borderBottomLeftRadius],
                          field: !!document.querySelector('.home-ecosystem .intesa'),
                          running: media.getAnimations({subtree: true}).length};
                }"""
            )
            assert frame["doorway"] == 0 and not frame["arch"], (cell, "no doorway drawn around the frame", frame)
            assert frame["painted"], (cell, "the photograph stands in its plain frame", frame)
            # the plain frame's corners: the card's below 64 rem from 48 rem; on a phone the photograph runs to the
            # page's edges, square; from 64 rem square at the viewport's reading edge, the card's inside
            tl, tr, br, bl = frame["corners"]
            start, end = ((tr, br), (tl, bl)) if frame["rtl"] else ((tl, bl), (tr, br))
            if width < 768:
                edge_to_edge = max(map(abs, frame["edges"])) <= 1
                assert set(frame["corners"]) == {"0px"} and edge_to_edge, (cell, "edge to edge", frame)
            elif width < 1024:
                card = len(set(frame["corners"])) == 1 and frame["corners"][0] != "0px"
                assert card, (cell, "the card's corner", frame)
            else:
                assert set(start) == {"0px"} and len(set(end)) == 1 and end[0] != "0px", (cell, "the bleed", frame)
                bleed = frame["edges"][1] if frame["rtl"] else frame["edges"][0]
                assert abs(bleed) <= 1, (cell, "the frame meets the viewport's reading edge", frame)
            # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the band's Italy + Morocco field left the home — no layer of
            # it anywhere in the band; the photograph and its plain frame above still stand
            assert not frame["field"], (cell, "no field drawn under the band", frame)
            assert frame["running"] == 0, (cell, "the frame's entrance has ended and left nothing applied", frame)
        finally:
            context.close()


# 1x only: nothing of the phone's door register is drawn, so no cell depends on the pixel ratio any more
@pytest.mark.parametrize("dsf", [1])
def test_final_a_phone_door_s_lunette_is_painted_as_one_line_from_its_foot(browser, live_server, phase3_live, dsf):
    """The same cause in the phone's doors (components/entrances.html; found with QA_ROUND3 m1's): on a 2× phone the
    lunette's far half was painted before its line began, on a 3× phone it drew as dashes. Drawn through its own mask,
    it is bare before its line begins, one run from its foot on its way and whole after (390 fr, 360 ar).
    RESTATED under V5.20 (the strict test-update rule) for the FINAL MICRO-PASS's review (10 Nov 2026, defect 1: on a
    phone the four lunettes and their discs were the page's arches after the hero's door): the doors carry no seat, so
    at either pixel ratio no lunette is painted — no arch, no seat, no disc, no drawing but the calls' arrows in the
    rail — and once the band has entered, the first plate's words stand inside it in order, the question first with
    the plate's own air above it (390 fr, 360 ar)."""
    for width, height, lang in ((390, 844, "fr"), (360, 780, "ar")):
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=dsf,
            has_touch=True,
            reduced_motion="no-preference",
        )
        page = context.new_page()
        try:
            page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (agent B, point 5): the
            # phone's register of doors is not drawn at all — so, stronger than «no lunette», nothing of it is
            # painted at either pixel ratio: no box, no seat, no arch, no disc; the doors are the hero's
            m = page.evaluate(
                """() => { const band = document.querySelector('.home-entrances');
                  return {boxes: band.getClientRects().length,
                          drawn: band.querySelectorAll('.passaggio__seggio, .passaggio__arco, .sez-disc, mask').length,
                          doors: [...document.querySelectorAll('.he-origin__link')]
                            .filter((a) => a.getBoundingClientRect().width > 0).length}; }"""
            )
            cell = (dsf, width, lang)
            assert m["boxes"] == 0 and m["drawn"] == 0, (cell, "no door plate, no lunette is painted", m)
            assert m["doors"] == 4, (cell, "the four doors are the hero's", m)
        finally:
            context.close()


_INDEX = """() => {
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  const ink = (e) => { const g = document.createRange(); g.selectNodeContents(e);
    const rs = [...g.getClientRects()].filter((q) => q.width > 0);
    return {left: Math.min(...rs.map((q) => q.left)), right: Math.max(...rs.map((q) => q.right)),
            lines: new Set(rs.map((q) => Math.round(q.top))).size}; };
  // RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B «l'esploratore»):
  // the index is the explorer's rail — vertical from 64 rem, a horizontal strip of chips below; each row its tile
  // and its title, the row's own gap between them
  const ix = document.querySelector('.home-pathways [data-tabs]');
  const list = ix.querySelector('[role="tablist"]');
  const rows = [...ix.querySelectorAll('.esplora__voce')].map((r) => {
    const g = r.querySelector('.esplora__tessera').getBoundingClientRect();
    const t = ink(r.querySelector('.esplora__nome'));
    return {edge: rtl ? t.right : t.left, gap: rtl ? g.left - t.right : t.left - g.right, glyph: g.width,
            lines: t.lines, own: parseFloat(getComputedStyle(r).columnGap)};
  });
  const label = document.querySelector('.colofone__label').getBoundingClientRect();
  return {mode: list ? list.getAttribute('aria-orientation') : '', rows,
          ponte: {drawn: document.querySelectorAll('.campata__ponte, .colofone__label .testa__rule').length,
                  label: label.width > 0 && label.height > 0}};
}"""


@pytest.mark.parametrize(
    "width,height",
    [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (430, 932), (390, 844), (375, 812), (360, 780)],
)
def test_final_the_arabic_index_s_titles_stand_on_one_edge_and_the_connector_on_its_rule(
    browser, live_server, phase3_live, width, height
):
    """QA_ROUND3 M1 and m2, at rest:
    * M1 — on the Arabic page the index's eight French titles stand on ONE edge, the reading edge's, within 1 px (a
      title that wrapped filled its row and started at the far edge, beside the chevron: the list zig-zagged at
      1024–1280 and on every phone); each title 12 px from its own glyph or tile, the glyphs one size — the RTL
      label exception of SECTION_SYSTEM_V2 §2 F; the widths where a title wraps hold the case M1 is about;
    * m2 — from 64 rem the colophon's connector ran on its folio's rule (centre lines within 0.5 px, ending where the
      rule begins); below 64 rem it was not drawn. RESTATED under V5.20 (the strict test-update rule) for the owner's
      V5.30 (7 Nov 2026, the RULE «a section should not stack arch + route line + geometric plate + outlined circle +
      connector»; stream A): the band's one motif is the Italy + Morocco field, so no connector is drawn on the home
      at ANY of the eight widths, in both languages (the old «below 64 rem» case, now everywhere), and the folio's
      own rule — the label role's — still stands."""
    for lang in ("ar", "fr"):
        context, page = _open(browser, live_server, f"/{lang}/", width, height, motion="reduce")
        try:
            _until_ready(page, ".home-pathways [data-tabs]")
            m = page.evaluate(_INDEX)
            rows, cell = m["rows"], (lang, width, m["mode"])
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (lane B
            # «l'esploratore»): the rail is vertical from 64 rem and a horizontal strip of chips below it (never a
            # disclosure list). On the vertical rail the eight titles stand on ONE edge (a wrapped title included);
            # on the strip each chip's title stays on one line. On both, in both languages, each title sits the row's
            # own gap from its tile (the gap the sheet sets, never a drift), the tiles one size
            vertical = width >= 1024
            assert m["mode"] == ("vertical" if vertical else "horizontal") and len(rows) == 8, (cell, rows)
            assert all(abs(row["gap"] - row["own"]) <= 1 for row in rows), (cell, "each beside its tile", rows)
            glyphs = [row["glyph"] for row in rows]
            assert max(glyphs) - min(glyphs) <= 0.5, (cell, "the tiles one size", glyphs)
            if vertical:
                edges = [row["edge"] for row in rows]
                assert max(edges) - min(edges) <= 1, (cell, "one edge for the eight titles", edges)
            else:
                assert all(row["lines"] == 1 for row in rows), (cell, "a chip's title on one line", rows)
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§25, lane A): the
            # campata and its connector left the
            # home with the folio's rule they ran on — none of them is in the page at any width, in both languages
            # (stronger than «stands down»); the promoter's label still stands
            ponte = m["ponte"]
            assert ponte["drawn"] == 0, (cell, "no connector, no rule for it", ponte)
            assert ponte["label"], (cell, "the promoter's label stands", ponte)
        finally:
            context.close()


# ------------------------------------------------------------------- after the final review (v522-h-final-qa1)

_PILOT = """() => {
  const lines = (e) => { if (!e) return []; const g = document.createRange(); g.selectNodeContents(e);
    const out = [];
    for (const q of [...g.getClientRects()].filter((r) => r.width > 1)) {
      const l = out.find((x) => Math.abs(x.top - q.top) < 6);
      if (l) { l.left = Math.min(l.left, q.left); l.right = Math.max(l.right, q.right); }
      else out.push({top: q.top, left: q.left, right: q.right}); }
    return out.sort((a, b) => a.top - b.top).map((l) => [l.left, l.right]); };
  const words = (e) => { const res = []; const walk = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n;
    while ((n = walk.nextNode())) { const re = /\\S+/g; let m;
      while ((m = re.exec(n.data))) {
        const g = document.createRange(); g.setStart(n, m.index); g.setEnd(n, m.index + m[0].length);
        const r = g.getClientRects()[0]; if (r) res.push(Math.round(r.top)); } }
    return res; };
  const q = (s) => document.querySelector(s);
  const title = q('.pilota__titolo'), lead = q('.pilota__lead');
  const link = q('.pilota__azione a');
  const a = link.getBoundingClientRect();
  const tops = words(lead), last = tops[tops.length - 1];
  return {rtl: getComputedStyle(document.documentElement).direction === 'rtl', title: lines(title), lead: lines(lead),
          link: [a.left, a.right],
          titleLang: title.getAttribute('lang'), leadLang: lead.getAttribute('lang'), leadText: lead.textContent,
          lastLineWords: tops.filter((top) => Math.abs(top - last) < 6).length};
}"""


@pytest.mark.parametrize(
    "width,height",
    [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (430, 932), (390, 844), (375, 812), (360, 780)],
)
def test_final_review_the_pilot_statement_stands_on_its_panel_axis_or_its_reading_edge(
    browser, live_server, phase3_live, width, height
):
    """The final review's F-M1 and F-m2 (v522-h-final-qa1; label v522-h-final-improve), at rest, at the eight review
    widths, with the catalogue's entry for the pilot's lead present (the lead in the page's own language — Arabic on the
    Arabic page —, no `lang` on it; the title the locked French, `lang="fr"`, on it, en and ar):
    * F-M1 — the page's one moment says one statement on one alignment: from 64 rem the title's lines, the lead's lines
      and the link share the panel's axis within 2 px (V5.30 Fast Visual Variety Correction §5, V5.20 strict rule:
      the gold thread that marked it is gone, the same axis is read on the panel's own centre); below 64 rem they hang
      from the reading edge — the right on the Arabic page, the left on the others — within 1 px. On the Arabic page
      the French title stood on its own left, 13–50 px off the axis and on the far edge from its lead, while the lead
      and link followed the seam;
    * F-m2 — the lead's last line is never one word («واحد.» alone at 768 on the Arabic page)."""
    for lang in ("ar", "fr", "it", "en"):
        context, page = _open(browser, live_server, f"/{lang}/", width, height, motion="reduce")
        try:
            page.evaluate("document.querySelector('.pilota-testa').scrollIntoView({block: 'center'})")
            m = page.evaluate(_PILOT)
            cell = (lang, width)
            assert m["leadLang"] is None, (
                cell,
                "the lead in the page's language: the catalogue carries it",
                m["leadText"],
            )
            # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): on /ar/ the title is
            # its provisional Arabic rendering (C-UI), in the page's language; it and en keep the locked French
            assert m["titleLang"] == (None if lang in ("fr", "ar") else "fr"), (cell, "the title's language")
            if lang == "ar":
                assert any("؀" <= ch <= "ۿ" for ch in m["leadText"]), (cell, "an Arabic lead", m["leadText"])
            assert len(m["title"]) == 2 and len(m["lead"]) >= 2, (cell, m["title"], m["lead"])
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§17, lane A): the
            # head no longer stands in a
            # centred seam panel — it is a head on the page's grid. From 64 rem the title's lines hang from the
            # reading edge and the lead's lines and the call from ONE edge of their own column beside it, never
            # overlapping the title; below 64 rem the title, the lead and the call hang from one reading edge — the
            # right on the Arabic page, the left on the others — within 1 px
            side = 1 if m["rtl"] else 0
            assert m["rtl"] == (lang == "ar"), cell
            if width >= 1024:
                title_edges = [box[side] for box in m["title"]]
                aside_edges = [box[side] for box in m["lead"] + [m["link"]]]
                assert max(title_edges) - min(title_edges) <= 1, (cell, "the title on the reading edge", title_edges)
                assert max(aside_edges) - min(aside_edges) <= 1, (cell, "the lead and call on one edge", aside_edges)
                if m["rtl"]:
                    assert max(box[1] for box in m["lead"]) < min(box[0] for box in m["title"]), (cell, m)
                else:
                    assert min(box[0] for box in m["lead"]) > max(box[1] for box in m["title"]), (cell, m)
            else:
                edges = [box[side] for box in m["title"] + m["lead"] + [m["link"]]]
                assert max(edges) - min(edges) <= 1, (cell, "one reading edge", edges)
            assert m["lastLineWords"] >= 2, (cell, "the lead never ends on one word", m["leadText"])
        finally:
            context.close()
