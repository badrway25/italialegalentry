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

import io
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
  const first = document.querySelector('.home-orientation .linea__step');
  const cell = first.getBoundingClientRect(), num = first.querySelector('.linea__num').getBoundingClientRect();
  const label = first.querySelector('.linea__label'), words = label.getBoundingClientRect();
  const heroBox = document.querySelector('.he').getBoundingClientRect();
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
              grey: [...document.querySelectorAll('.pilota__quadro img')].map(i => getComputedStyle(i).filter),
              running: document.getAnimations().length,
            })"""
        )
        assert still["states"] == 0, still
        assert still["lines"] == 0, ("V5.30 Fast Visual Variety Correction §5: no such line is left to draw", still)
        assert all(f in ("none", "grayscale(0)") for f in still["grey"]), still
        assert still["running"] == 0, still
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_pathways_index_works_from_the_keyboard_and_the_stage_never_moves(browser, live_server, phase3_live, lang):
    context, page = _open(browser, live_server, f"/{lang}/", 1440, 900)
    try:
        page.wait_for_function("document.querySelector('.home-pathways .indice')?.dataset.mode === 'tabs'")
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


def test_the_reserved_key_turns_on_its_button_and_never_under_reduced_motion(browser, live_server, phase3_live):
    for motion, turned in (("no-preference", True), ("reduce", False)):
        context, page = _open(browser, live_server, "/fr/", 1440, 900, motion=motion)
        try:
            button = page.locator(".home-reserved__button")
            button.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
            rest = page.evaluate("getComputedStyle(document.querySelector('.home-reserved .sg-g--key')).rotate")
            button.hover()
            page.wait_for_timeout(600)
            lit = page.evaluate("getComputedStyle(document.querySelector('.home-reserved .sg-g--key')).rotate")
            assert rest in ("none", "0deg"), (motion, rest)
            assert (lit == "-90deg") is turned, (motion, lit)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_phone_doors_are_one_rail_the_keyboard_crosses_plate_by_plate(browser, live_server, phase3_live, lang):
    context, page = _open(browser, live_server, f"/{lang}/", 390, 844)
    try:
        page.locator(".home-entrances").scroll_into_view_if_needed()
        page.locator(".passaggio__porta").first.focus()
        seen = []
        for _ in range(4):
            box = page.evaluate(
                """() => { const a = document.activeElement, r = a.getBoundingClientRect(),
                     rail = a.closest('.passaggio').getBoundingClientRect();
                   return {cls: a.className, left: r.left, right: r.right, railL: rail.left, railR: rail.right}; }"""
            )
            assert box["cls"] == "passaggio__porta", box
            assert box["left"] >= box["railL"] - 1 and box["right"] <= box["railR"] + 1, (
                lang,
                "a focused door stands whole",
                box,
            )
            seen.append(box)
            page.keyboard.press("Tab")
            page.wait_for_timeout(350)
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
  const pic = document.querySelector('.home-ecosystem .campata__media picture');
  const label = document.querySelector('.colofone__label');
  const panel = document.querySelector('.home-pathways .indice__pannello[data-on]');
  const edge = (r) => (rtl ? r.right : r.left);
  return {
    rtl, air: parseFloat(getComputedStyle(document.querySelector('.home-orientation')).paddingBlockStart),
    statement: R('.he__body'), head: R('.home-orientation .testa'),
    seal: R('.home-orientation .linea__step .sigillo'),
    tablet: R('.integrita__tavola'), plate: R('.home-antifraud .protezione'),
    key: getComputedStyle(document.querySelector('.home-reserved .sg-g--key')).color, gold,
    keyToButton: (() => {
      const k = R('.home-reserved .sigillo'), b = R('.home-reserved__button');
      return rtl ? k.left - b.right : b.left - k.right;
    })(),
    corners: (() => { const s = getComputedStyle(pic.querySelector('img'));
                      return [s.borderTopLeftRadius, s.borderTopRightRadius,
                              s.borderBottomRightRadius, s.borderBottomLeftRadius]; })(),
    drawing: document.querySelectorAll('.home-ecosystem :is(.casa-arco, .casa-arco__disegno)').length,
    labels: [...document.querySelectorAll('.home-orientation .linea__label')].map((l) => {
      const s = getComputedStyle(l), box = l.getBoundingClientRect();
      const cell = l.closest('.linea__step'), step = cell.getBoundingClientRect();
      const pad = parseFloat(getComputedStyle(cell).paddingInlineStart);
      return {dir: s.direction, align: s.textAlign, gap: (rtl ? step.right - box.right : box.left - step.left) - pad};
    }),
    stage: panel ? [edge(panel.querySelector('.indice__titolo').getBoundingClientRect()),
                    edge(panel.querySelector('.parcours__descrizione').getBoundingClientRect()),
                    panel.querySelector('.indice__titolo').getBoundingClientRect().left,
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
        page.wait_for_function("document.querySelector('.home-pathways .indice')?.dataset.mode === 'tabs'")
        m = page.evaluate(_ROUND1)
        gap = m["head"]["top"] - m["statement"]["bottom"]
        # FINAL MICRO-PASS §5 A1 (C, «the head with air»; V5.20 strict rule): M1 a's foot distance (≤ 40 px) gave way to
        # the band's own air — the head stands exactly the band's top padding under the statement, never more than
        # --s-20 (80 px), nothing else between them
        assert abs(gap - m["air"]) <= 1 and 0 <= gap <= 80, (lang, "the head at the band's air", gap, m["air"])
        # FINAL MICRO-PASS §5 A1 (V5.20 strict rule): M1 b's origin tile left with the seal — the route opens on its
        # quiet marker, its four stations still said
        assert m["seal"] is None and len(m["labels"]) == 4, (lang, m["seal"], m["labels"])
        side = "right" if m["rtl"] else "left"
        assert abs(m["plate"][side] - m["tablet"][side]) <= 1, (lang, "on the reading edge", m["plate"], m["tablet"])
        assert m["key"] == m["gold"], (lang, "the key in the identity's gold", m["key"], m["gold"])
        assert 0 <= m["keyToButton"] <= 32, (lang, "the seat beside its button", m["keyToButton"])
        assert len(set(m["corners"])) == 1 and m["corners"][0] != "0px", (
            lang,
            "the frame on the card's corner",
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
            assert abs(m["stage"][2] - m["stage"][3]) <= 1, ("one start edge for the stage's French", m["stage"])
            assert "mono" not in m["folio"][0].lower() and m["folio"][1] in ("0px", "normal"), m["folio"]
    finally:
        context.close()


# ---------------------------------------------------------------------------------------------- round 2 (QA_ROUND2)

_ROUND2_AR = """() => {
  const ink = (e) => { const g = document.createRange(); g.selectNodeContents(e);
                       const rs = [...g.getClientRects()].filter((q) => q.width > 0);
                       return {left: Math.min(...rs.map((q) => q.left)), right: Math.max(...rs.map((q) => q.right))}; };
  const col = document.querySelector('.colofone');
  const step = document.querySelector('.home-orientation .linea__step');
  return {
    reserved: [ink(document.querySelector('.home-reserved__title')),
               ink(document.querySelector('.home-reserved__body'))],
    colophon: [ink(col.querySelector('.fronte__name')), ink(col.querySelector('.fronte__name-rest')),
               ink(col.querySelector('.colofone__testo'))],
    answer: {lang: col.querySelector('.colofone__testo').getAttribute('lang') || '',
             dir: getComputedStyle(col.querySelector('.colofone__testo')).direction},
    across: getComputedStyle(step).gridTemplateColumns.trim().split(/\\s+/).length === 1,
    labels: [...document.querySelectorAll('.home-orientation .linea__label')].map((l) => {
      const s = l.closest('.linea__step').getBoundingClientRect(), box = l.getBoundingClientRect();
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
        title, body = m["reserved"]
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the reserved row's title
        # and sentence are their provisional Arabic renderings (C-UI) — one start edge, the right one
        assert abs(title["right"] - body["right"]) <= 1, (width, "one start edge for the reserved row", m["reserved"])
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


_ROWS = """() => [...document.querySelectorAll('.home-pathways .indice[data-mode="disclosure"] .indice__pannello')]
.map((p) => {
  const button = p.querySelector('.indice__apri'), b = button.getBoundingClientRect();
  const tile = p.querySelector('.indice__tessera').getBoundingClientRect();
  const g = document.createRange(); g.selectNodeContents(p.querySelector('.indice__parola'));
  const rs = [...g.getClientRects()].filter((q) => q.width > 0);
  const after = getComputedStyle(button, '::after');
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  // the chevron is the button's last flex item, 6 px off the row's end: its inner edge, the one facing the title
  const chevron = rtl ? b.left + parseFloat(after.marginLeft) + parseFloat(after.width)
                      : b.right - parseFloat(after.marginRight) - parseFloat(after.width);
  return {rtl, dir: getComputedStyle(button).direction, end: rtl ? after.marginLeft : after.marginRight, chevron,
          ink: [Math.min(...rs.map((q) => q.left)), Math.max(...rs.map((q) => q.right))], tile: [tile.left, tile.right],
          sezI: getComputedStyle(p.querySelector('.indice__parola')).getPropertyValue('--sez-i').trim()};
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
        page.wait_for_function("document.querySelector('.home-pathways .indice')?.dataset.mode === 'disclosure'")
        rows = page.evaluate(_ROWS)
        assert len(rows) == 8, rows
        for row in rows:
            assert row["dir"] == ("rtl" if lang == "ar" else "ltr"), row
            assert row["end"] == "6px", (lang, "the chevron at the row's end", row)
            if row["rtl"]:
                assert row["tile"][0] >= row["ink"][1] - 0.5 and row["ink"][0] >= row["chevron"] - 0.5, (lang, row)
            else:
                assert row["tile"][1] <= row["ink"][0] + 0.5 and row["ink"][1] <= row["chevron"] + 0.5, (lang, row)
        assert [row["sezI"] for row in rows] == ["", "1", "2", "3", "4", "5", "5", "5"], [row["sezI"] for row in rows]
        page.locator(".home-pathways").scroll_into_view_if_needed()
        for _ in range(40):  # the section's trigger (rise.js); no page-side polling: the CSP allows no eval
            if page.evaluate("document.querySelector('.home-pathways').dataset.secState") == "in":
                break
            page.wait_for_timeout(100)
        delays = page.evaluate(
            "[...document.querySelectorAll('.home-pathways .indice__pannello .indice__parola')]"
            ".map((s) => getComputedStyle(s).animationDelay)"
        )
        assert delays == ["0s", "0.06s", "0.12s", "0.18s", "0.24s", "0.3s", "0.3s", "0.3s"], delays
    finally:
        context.close()


# ------------------------------------------------------------------------------------------ final fix round (QA_ROUND3)

_LINE_POINTS = """(sel) => [...document.querySelectorAll(sel)].filter((p) => !p.closest('mask')).map((p) => {
  const m = p.getScreenCTM(), length = p.getTotalLength(), pts = [];
  for (let i = 0; i <= 240; i++) {
    const q = p.getPointAtLength(length * i / 240);
    pts.push([m.a * q.x + m.c * q.y + m.e, m.b * q.x + m.d * q.y + m.f]);
  }
  return pts;
})"""

_PAUSE = """(sel) => {
  const sec = document.querySelector(sel);
  window.__drawn = document.getAnimations().filter((a) => a.timeline === document.timeline && a.effect
    && a.effect.target && sec.contains(a.effect.target));
  window.__drawn.forEach((a) => a.pause());
  return window.__drawn.length;
}"""

# the page scrolls smoothly for a pointer: the measured section is brought in at once, so its lines stay where measured
_CENTRE = "(sel) => document.querySelector(sel).scrollIntoView({block: 'center', behavior: 'instant'})"

_COLOUR = """(lines) => lines.forEach(([sel, colour]) => document.querySelectorAll(sel).forEach((p) => {
  if (!p.closest('mask')) p.style.stroke = colour;
}))"""


def _ink(png, dsf, clip, pts, hue):
    """Along a line's own screen points: whether the pixel under each (or one of its eight neighbours, at the device's
    resolution) carries the line's measuring ink — pure red or pure blue, set on the VISIBLE line only through the CSSOM
    (a measuring aid: the dash, the mask and the timing are the page's own)."""
    from PIL import Image

    img = Image.open(io.BytesIO(png)).convert("RGB")
    width, height = img.size
    flags = []
    for x, y in pts:
        cx, cy = round((x - clip["x"]) * dsf), round((y - clip["y"]) * dsf)
        hit = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if 0 <= cx + dx < width and 0 <= cy + dy < height:
                    r, g, b = img.getpixel((cx + dx, cy + dy))
                    hit = hit or ((r > g + 60 and r > b + 60) if hue == "red" else (b > r + 60 and b > g + 60))
        flags.append(hit)
    return flags


def _runs(flags):
    """The painted runs along a line, as (first, last) sample indices; one bare sample is antialiasing, not a gap."""
    runs, start, last, gap = [], None, None, 0
    for i, flag in enumerate(flags):
        if flag:
            start = i if start is None else start
            last, gap = i, 0
        elif start is not None:
            gap += 1
            if gap > 1:
                runs.append((start, last))
                start, gap = None, 0
    if start is not None:
        runs.append((start, last))
    return runs


def _seek_and_shoot(page, section, lines, times, dsf):
    """Once the section plays, pause its own time-based animations, ink the measured lines, then seek and photograph:
    {time: {line: painted runs}} along each line's 241 samples, from its own start."""
    for _ in range(60):  # the section's trigger (rise.js); the CSP allows no page-side polling
        if page.evaluate(f"document.querySelector('{section}').dataset.secState") == "in":
            break
        page.wait_for_timeout(50)
    assert page.evaluate(f"document.querySelector('{section}').dataset.secState") == "in", section
    page.wait_for_timeout(50)
    assert page.evaluate(_PAUSE, section) > 0, (section, "its verbs run")
    page.evaluate(_COLOUR, [[sel, "rgb(255, 0, 0)" if hue == "red" else "rgb(0, 0, 255)"] for sel, hue in lines])
    points = {}
    for sel, _hue in lines:
        drawn = page.evaluate(_LINE_POINTS, sel)
        assert drawn, (sel, "the visible line, drawn through its own mask")
        points[sel] = drawn[0]
    xs = [x for pts in points.values() for x, _y in pts]
    ys = [y for pts in points.values() for _x, y in pts]
    clip = {"x": max(0, min(xs) - 8), "y": max(0, min(ys) - 8)}
    clip["width"], clip["height"] = max(xs) + 8 - clip["x"], max(ys) + 8 - clip["y"]
    shots = {}
    for t in times:
        page.evaluate(f"window.__drawn.forEach((a) => {{ a.currentTime = {t}; }})")
        page.wait_for_timeout(60)
        png = page.screenshot(clip=clip)
        shots[t] = {sel: _runs(_ink(png, dsf, clip, points[sel], hue)) for sel, hue in lines}
    return shots


def _whole(runs):
    return len(runs) == 1 and runs[0][1] - runs[0][0] >= 234


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
            page.evaluate(_CENTRE, ".home-ecosystem .campata__media")
            for _ in range(60):  # the section's trigger (rise.js)
                if page.evaluate("document.querySelector('.home-ecosystem').dataset.secState") == "in":
                    break
                page.wait_for_timeout(50)
            page.wait_for_timeout(2500)
            frame = page.evaluate(
                """() => {
                  const media = document.querySelector('.home-ecosystem .campata__media');
                  const img = media.querySelector('img'), s = getComputedStyle(img);
                  return {doorway: document.querySelectorAll(
                            '.home-ecosystem :is(.casa-arco, .casa-arco__disegno, mask)').length,
                          arch: media.closest('.campata').classList.contains('campata--arch'),
                          painted: img.complete && img.naturalWidth > 0,
                          corners: [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomRightRadius,
                                    s.borderBottomLeftRadius],
                          field: !!document.querySelector('.home-ecosystem .intesa'),
                          running: media.getAnimations({subtree: true}).length};
                }"""
            )
            assert frame["doorway"] == 0 and not frame["arch"], (cell, "no doorway drawn around the frame", frame)
            assert frame["painted"], (cell, "the photograph stands in its plain frame", frame)
            assert len(set(frame["corners"])) == 1 and frame["corners"][0] != "0px", (cell, "the card's corner", frame)
            # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the band's Italy + Morocco field left the home — no layer of
            # it anywhere in the band; the photograph and its plain frame above still stand
            assert not frame["field"], (cell, "no field drawn under the band", frame)
            assert frame["running"] == 0, (cell, "the frame's entrance has ended and left nothing applied", frame)
        finally:
            context.close()


#: the first door's plate (FINAL MICRO-PASS, the review's defect 1): what the rail draws besides the calls' arrows, and
#: the places of the plate's three words inside it
_DOOR = """() => {
  const rail = document.querySelector('.home-entrances .passaggio');
  const plate = rail.querySelector('.passaggio__porta'), box = plate.getBoundingClientRect();
  const parts = ['.passaggio__titolo', '.passaggio__testo', '.passaggio__cta'].map((s) => {
    const r = plate.querySelector(s).getBoundingClientRect();
    return {top: Math.round(r.top - box.top), height: r.height,
            inside: r.left >= box.left - 1 && r.right <= box.right + 1};
  });
  const drawn = rail.querySelectorAll('.passaggio__seggio, .passaggio__arco, .sez-disc, mask, svg:not(.icon)');
  return {drawn: drawn.length, parts};
}"""


@pytest.mark.parametrize("dsf", [1, 2])
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
            state = page.evaluate("document.querySelector('.home-entrances').dataset.secState")
            assert state == "wait", (width, lang, "the doors' band starts below the fold", state)
            page.evaluate(_CENTRE, ".home-entrances .passaggio")
            page.wait_for_function("() => document.querySelector('.home-entrances').dataset.secState === 'in'")
            plate = page.evaluate(_DOOR)
            cell = (dsf, width, lang)
            assert plate["drawn"] == 0, (cell, "no seat, no arch, no disc on a door", plate)
            tops = [part["top"] for part in plate["parts"]]
            assert all(part["height"] > 0 and part["inside"] for part in plate["parts"]), (cell, plate)
            assert tops == sorted(tops) and tops[0] >= 16, (cell, "the question first, with the plate's air", plate)
        finally:
            context.close()


_INDEX = """() => {
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  const ink = (e) => { const g = document.createRange(); g.selectNodeContents(e);
    const rs = [...g.getClientRects()].filter((q) => q.width > 0);
    return {left: Math.min(...rs.map((q) => q.left)), right: Math.max(...rs.map((q) => q.right)),
            lines: new Set(rs.map((q) => Math.round(q.top))).size}; };
  const ix = document.querySelector('.home-pathways .indice');
  const tabs = ix.dataset.mode === 'tabs';
  const rows = [...ix.querySelectorAll(tabs ? '.indice__voce' : '.indice__pannello')].map((r) => {
    const g = r.querySelector(tabs ? '.indice__glifo' : '.indice__tessera').getBoundingClientRect();
    const t = ink(r.querySelector(tabs ? '.indice__nome' : '.indice__parola'));
    return {edge: rtl ? t.right : t.left, gap: rtl ? g.left - t.right : t.left - g.right, glyph: g.width,
            lines: t.lines};
  });
  const ponte = document.querySelector('.campata__ponte');
  const rule = document.querySelector('.colofone__label .testa__rule');
  const p = ponte.getBoundingClientRect(), q = rule.getBoundingClientRect();
  return {mode: ix.dataset.mode || '', rows,
          ponte: {shown: getComputedStyle(ponte).display !== 'none' && p.width > 0, rule: q.width > 0}};
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
            for _ in range(40):  # indice.js sets the index's mode; the CSP allows no page-side polling
                if page.evaluate("document.querySelector('.home-pathways .indice').dataset.mode || ''"):
                    break
                page.wait_for_timeout(50)
            m = page.evaluate(_INDEX)
            rows, cell = m["rows"], (lang, width, m["mode"])
            assert m["mode"] == ("tabs" if width >= 1024 else "disclosure") and len(rows) == 8, (cell, rows)
            if lang == "ar":
                edges = [row["edge"] for row in rows]
                assert max(edges) - min(edges) <= 1, (cell, "one edge for the eight titles", edges)
                assert all(abs(row["gap"] - 12) <= 1 for row in rows), (cell, "each beside its glyph", rows)
                glyphs = [row["glyph"] for row in rows]
                assert max(glyphs) - min(glyphs) <= 0.5, (cell, "the glyphs one size", glyphs)
                if width not in (1440, 768):
                    assert any(row["lines"] > 1 for row in rows), (cell, "a title wraps: the case under test", rows)
            ponte = m["ponte"]
            assert not ponte["shown"], (cell, "the connector stands down on the home (V5.30)", ponte)
            assert ponte["rule"], (cell, "the folio keeps its rule", ponte)
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
  const link = q('.pilota__azione a'), panel = q('.pilota__testo');
  const t = panel.getBoundingClientRect(), a = link.getBoundingClientRect();
  const tops = words(lead), last = tops[tops.length - 1];
  return {rtl: getComputedStyle(document.documentElement).direction === 'rtl',
          axis: t.width > 0 ? (t.left + t.right) / 2 : null, title: lines(title), lead: lines(lead),
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
            page.evaluate("document.querySelector('.pilota__testo').scrollIntoView({block: 'center'})")
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
            if width >= 1024:
                assert m["axis"] is not None, cell
                centres = [(left + right) / 2 for left, right in m["title"] + m["lead"] + [m["link"]]]
                assert max(abs(c - m["axis"]) for c in centres) <= 2, (cell, "one axis, the panel's", m["axis"],
                centres)
            else:
                side = 1 if m["rtl"] else 0
                edges = [box[side] for box in m["title"] + m["lead"] + [m["link"]]]
                assert m["rtl"] == (lang == "ar") and max(edges) - min(edges) <= 1, (cell, "one reading edge", edges)
            assert m["lastLineWords"] >= 2, (cell, "the lead never ends on one word", m["leadText"])
        finally:
            context.close()
