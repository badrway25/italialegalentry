"""
V5.22 — HOMEPAGE COMPOSITION V2 in a real layout engine (SECTION_SYSTEM_V2 §2.0, §3.1, §5.3, §9.9; lane H).

* the hand-off: the line beside the hero's statement and its continuation meet the orientation seal's sill — one route,
  on the reading edge, in both directions, at the desktop and tablet widths;
* the trigger contract on the real page: a section below the fold waits, plays its verbs once and holds nothing
  (V5.20: a finished entrance leaves document.getAnimations()); under reduced motion nothing is written and the page
  is its designed still — every line drawn, every photograph in colour;
* the pathways' index from the keyboard: the ARIA tabs pattern, the stage changing in place (the section never moves);
* the pilot's panels draw what their `sizes` say (object-fit: cover: the drawn width is the box's or its height's 2:3);
* the reserved row's key turns on its own button, never under reduced motion;
* the phone's doors: one rail the keyboard crosses plate by plate, every focused plate whole in the rail;
* round 1 (QA_ROUND1, label v522-h-improve1): the hand-off without an empty run, the body seal at the route's origin,
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
  reading edge's, at the eight review widths; the colophon's connector runs on its folio's rule;
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
  const hero = document.querySelector('.he__soglia').getBoundingClientRect();
  const line = document.querySelector('.orienta__soglia').getBoundingClientRect();
  const seal = document.querySelector('.home-orientation .linea__step .sigillo').getBoundingClientRect();
  const heroBox = document.querySelector('.he').getBoundingClientRect();
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  return {rtl, hero: [hero.left, hero.right, hero.bottom], heroBottom: heroBox.bottom, top: sec.top,
          line: [line.left, line.right, line.top, line.bottom], seal: [seal.left, seal.right, seal.bottom],
          display: getComputedStyle(document.querySelector('.orienta__soglia')).display};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_hero_line_runs_down_into_the_orientation_seal_sill(browser, live_server, phase3_live, lang):
    """H0 «la soglia» (§3.1): the 2 px line beside the statement, 12 px off the reading edge, reaches the hero's foot;
    in the orientation's band it goes on from the band's top on the same axis and ends on the seal's sill, where the
    route begins — so the hero's route and the orientation's are one line. Measured at rest (reduced motion)."""
    for width, height in ((1440, 900), (1024, 768), (768, 1024)):
        context, page = _open(browser, live_server, f"/{lang}/", width, height, motion="reduce")
        try:
            m = page.evaluate(_MEET)
            cell = (lang, width)
            assert m["display"] == "block", cell
            assert abs(m["hero"][0] - m["line"][0]) <= 0.5, (cell, "one axis", m)
            assert abs(m["hero"][2] - m["heroBottom"]) <= 1 and abs(m["top"] - m["heroBottom"]) <= 1, (cell, m)
            assert abs(m["line"][2] - m["top"]) <= 1, (cell, "from the band's top", m)
            assert abs(m["line"][3] - m["seal"][2]) <= 1, (cell, "to the sill", m)
            # the sill runs 12 px past the seal's side: the line stands at its outer end, on the reading edge
            sill_end = m["seal"][1] + 12 if m["rtl"] else m["seal"][0] - 12
            line_edge = m["line"][1] if m["rtl"] else m["line"][0]
            assert abs(line_edge - sill_end) <= 1.5, (cell, m)
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
              lines: [...document.querySelectorAll('.he__soglia-linea, .orienta__soglia, .pilota__filo')]
                .map(e => getComputedStyle(e).scale),
              grey: [...document.querySelectorAll('.pilota__quadro img')].map(i => getComputedStyle(i).filter),
              running: document.getAnimations().length,
            })"""
        )
        assert still["states"] == 0, still
        assert all(scale in ("none", "1") for scale in still["lines"]), still
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
    rtl,
    statement: R('.he__body'), head: R('.home-orientation .testa'),
    seal: R('.home-orientation .linea__step .sigillo'),
    tablet: R('.integrita__tavola'), plate: R('.home-antifraud .protezione'),
    key: getComputedStyle(document.querySelector('.home-reserved .sg-g--key')).color, gold,
    keyToButton: (() => {
      const k = R('.home-reserved .sigillo'), b = R('.home-reserved__button');
      return rtl ? k.left - b.right : b.left - k.right;
    })(),
    corners: [getComputedStyle(pic).borderBottomLeftRadius, getComputedStyle(pic).borderBottomRightRadius],
    drawing: [R('.casa-arco__disegno').width, pic.getBoundingClientRect().width],
    labels: [...document.querySelectorAll('.home-orientation .linea__label')].map((l) => {
      const s = getComputedStyle(l), box = l.getBoundingClientRect();
      const step = l.closest('.linea__step').getBoundingClientRect();
      return {dir: s.direction, align: s.textAlign, gap: rtl ? step.right - box.right : box.left - step.left};
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
    * M1 b — the route's origin is the body's seal, 72 × 88;
    * M1 c — «la protezione» hangs from the reading edge, the tablet's own edge above it, never centred;
    * M1 d, m10 — the key is drawn in the identity's gold, beside its button;
    * M1 e — the arch's foot stands square on its sill, the doorway drawn 12 px around the frame;
    * M2 a — on the Arabic page each French station label is its own left-to-right box, on its station's edge;
    * M2 b — the stage's French title and description start on one edge;
    * M2 c — the Arabic folio is never set in a Latin monospace nor tracked."""
    context, page = _open(browser, live_server, f"/{lang}/", 1440, 900, motion="reduce")
    try:
        page.wait_for_function("document.querySelector('.home-pathways .indice')?.dataset.mode === 'tabs'")
        m = page.evaluate(_ROUND1)
        gap = m["head"]["top"] - m["statement"]["bottom"]
        assert 0 <= gap <= 40, (lang, "the head follows the statement", gap)
        assert (round(m["seal"]["width"]), round(m["seal"]["height"])) == (72, 88), (lang, m["seal"])
        side = "right" if m["rtl"] else "left"
        assert abs(m["plate"][side] - m["tablet"][side]) <= 1, (lang, "on the reading edge", m["plate"], m["tablet"])
        assert m["key"] == m["gold"], (lang, "the key in the identity's gold", m["key"], m["gold"])
        assert 0 <= m["keyToButton"] <= 32, (lang, "the seat beside its button", m["keyToButton"])
        assert m["corners"] == ["0px", "0px"], (lang, "the arch's foot is square on its sill", m["corners"])
        assert abs(m["drawing"][0] - (m["drawing"][1] + 24)) <= 1, (lang, "the doorway 12 px around the frame", m)
        if lang == "ar":
            for label in m["labels"]:
                assert label["dir"] == "ltr" and label["align"] in ("start", "left"), label
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
    across: getComputedStyle(step).gridTemplateColumns.trim().split(/\\s+/).length === 1,
    labels: [...document.querySelectorAll('.home-orientation .linea__label')].map((l) => {
      const s = l.closest('.linea__step').getBoundingClientRect(), box = l.getBoundingClientRect();
      return {gap: s.right - box.right, width: box.width, em: parseFloat(getComputedStyle(l).fontSize)};
    }),
  };
}"""


@pytest.mark.parametrize("width,height", [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (390, 844), (360, 780)])
def test_round_2_the_arabic_page_hangs_each_french_run_from_one_edge(browser, live_server, phase3_live, width, height):
    """QA_ROUND2 M1 a, m3, m4 on the Arabic page, at rest (SECTION_SYSTEM_V2 §1 rule 6: a French run stands in its own
    box, aligned to its own start, hanging from the page's reading edge):
    * M1 a — the reserved row's French title and its sentence start on one edge, one quotation (from 64 rem the title
      stood 430–540 px from its sentence);
    * m3 — the colophon's name, in its two parts, and the French answer start on one edge, one left-to-right box;
    * m4 — a station's French caption stands at a caption's measure (12.5 em), never its column's; across the route it
      hangs from its own station's edge."""
    context, page = _open(browser, live_server, "/ar/", width, height, motion="reduce")
    try:
        m = page.evaluate(_ROUND2_AR)
        title, body = m["reserved"]
        assert abs(title["left"] - body["left"]) <= 1, (width, "one start edge for the reserved row", m["reserved"])
        name, rest, answer = m["colophon"]
        for part in (name, rest):
            assert abs(part["left"] - answer["left"]) <= 1, (width, "one left-to-right box", m["colophon"])
        for label in m["labels"]:
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


_OUTLINE = ".casa-arco__disegno > path.casa-arco__profilo"
_SILL = ".casa-arco__disegno > path:not(.casa-arco__profilo)"


@pytest.mark.parametrize("dsf", [1, 2])
def test_final_the_doorway_is_painted_as_one_line_from_its_foot(browser, live_server, phase3_live, dsf):
    """QA_ROUND3 m1 — the PAINTED assertion that replaces round 2's model of the dash (V5.20 strict rule;
    SECTION_SYSTEM_V2 §3.1 S7 «the arch outline draws», §5.1 LINE DRAW: one line, never segments). Round 2's dash was
    laid in DEVICE pixels: the far leg showed first on the reviewer's 1.25× display (1023, 1920), and on a 2× or 3×
    screen the outline and the sill drew as pieces (measured with the full Chromium build at a forced factor). Each
    line now draws through its own mask, a dash in the drawing's user space. Painted, sought frame by frame, at the
    reviewer's widths, a phone's and the Arabic page's: while the outline waits (300 ms) nothing of it — its far leg
    included — is painted and the sill grows from its end; on its way (1 000 ms) the outline is ONE run from its foot
    at the verb's pace, its far leg still bare (round 2's line was already whole there at 390); after (1 650 ms) both
    are whole."""
    for width, height, lang in ((1023, 768, "fr"), (1920, 1080, "fr"), (390, 844, "fr"), (1440, 900, "ar")):
        context = browser.new_context(
            viewport={"width": width, "height": height}, device_scale_factor=dsf, reduced_motion="no-preference"
        )
        page = context.new_page()
        try:
            page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            assert page.evaluate("document.querySelector('.home-ecosystem').dataset.secState") == "wait"
            page.evaluate(_CENTRE, ".home-ecosystem .campata__media")
            shots = _seek_and_shoot(
                page, ".home-ecosystem", [(_OUTLINE, "red"), (_SILL, "blue")], (300, 1000, 1650), dsf
            )
            cell = (dsf, width, lang)
            waiting, drawing, after = shots[300], shots[1000], shots[1650]
            assert waiting[_OUTLINE] == [], (cell, "the outline waits: nothing of it painted", waiting)
            assert len(waiting[_SILL]) == 1, (cell, "the sill: one line", waiting)
            assert waiting[_SILL][0][0] <= 2 and waiting[_SILL][0][1] < 216, (cell, "from its end", waiting)
            assert len(drawing[_OUTLINE]) == 1, (cell, "one line, never segments", drawing)
            first, last = drawing[_OUTLINE][0]
            assert first <= 2 and 24 <= last < 180, (cell, "from its foot, its far leg still bare", drawing)
            assert _whole(after[_OUTLINE]) and _whole(after[_SILL]), (cell, "both lines whole", after)
        finally:
            context.close()


@pytest.mark.parametrize("dsf", [1, 2])
def test_final_a_phone_door_s_lunette_is_painted_as_one_line_from_its_foot(browser, live_server, phase3_live, dsf):
    """The same cause in the phone's doors (components/entrances.html; found with QA_ROUND3 m1's): on a 2× phone the
    lunette's far half was painted before its line began, on a 3× phone it drew as dashes. Drawn through its own mask,
    it is bare before its line begins, one run from its foot on its way and whole after (390 fr, 360 ar)."""
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
            arch = ".passaggio__lastra:first-child .passaggio__arco > path[mask]"
            shots = _seek_and_shoot(page, ".home-entrances", [(arch, "red")], (0, 450, 1300), dsf)
            cell = (dsf, width, lang)
            assert shots[0][arch] == [], (cell, "nothing before the line begins", shots)
            assert len(shots[450][arch]) == 1, (cell, "one line, never segments", shots)
            assert shots[450][arch][0][0] <= 2 and shots[450][arch][0][1] < 180, (cell, "from its foot", shots)
            assert _whole(shots[1300][arch]), (cell, "whole", shots)
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
          ponte: {shown: getComputedStyle(ponte).display !== 'none',
                  centre: p.top + p.height / 2 - (q.top + q.height / 2),
                  meet: rtl ? p.left - q.right : q.left - p.right}};
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
    * m2 — from 64 rem the colophon's connector runs on its folio's rule (fr and ar): centre lines within 0.5 px, the
      connector ending where the rule begins (it stood 6 px above it); below 64 rem it is not drawn."""
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
            if width >= 1024:
                assert ponte["shown"] and abs(ponte["centre"]) <= 0.5, (cell, "the connector on its rule", ponte)
                assert abs(ponte["meet"]) <= 1, (cell, "it ends where the rule begins", ponte)
            else:
                assert not ponte["shown"], (cell, ponte)
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
  const link = q('.pilota__azione a'), thread = q('.pilota__filo');
  const t = thread.getBoundingClientRect(), a = link.getBoundingClientRect();
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
def test_final_review_the_pilot_statement_stands_on_its_seam_axis_or_its_reading_edge(
    browser, live_server, phase3_live, width, height
):
    """The final review's F-M1 and F-m2 (v522-h-final-qa1; label v522-h-final-improve), at rest, at the eight review
    widths, with the catalogue's entry for the pilot's lead present (the lead in the page's own language — Arabic on the
    Arabic page —, no `lang` on it; the title the locked French, `lang="fr"`, on it, en and ar):
    * F-M1 — the page's one moment says one statement on one alignment: from 64 rem the title's lines, the lead's lines
      and the link share the seam's axis (the gold thread's centre) within 2 px; below 64 rem they hang from the reading
      edge — the right on the Arabic page, the left on the others — within 1 px. On the Arabic page the French title
      stood on its own left, 13–50 px off the axis and on the far edge from its lead, while the lead and link followed
      the seam;
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
            assert m["titleLang"] == (None if lang == "fr" else "fr"), (cell, "the title is the locked French")
            if lang == "ar":
                assert any("؀" <= ch <= "ۿ" for ch in m["leadText"]), (cell, "an Arabic lead", m["leadText"])
            assert len(m["title"]) == 2 and len(m["lead"]) >= 2, (cell, m["title"], m["lead"])
            if width >= 1024:
                assert m["axis"] is not None, cell
                centres = [(left + right) / 2 for left, right in m["title"] + m["lead"] + [m["link"]]]
                assert max(abs(c - m["axis"]) for c in centres) <= 2, (cell, "one axis, the seam's", m["axis"], centres)
            else:
                side = 1 if m["rtl"] else 0
                edges = [box[side] for box in m["title"] + m["lead"] + [m["link"]]]
                assert m["rtl"] == (lang == "ar") and max(edges) - min(edges) <= 1, (cell, "one reading edge", edges)
            assert m["lastLineWords"] >= 2, (cell, "the lead never ends on one word", m["leadText"])
        finally:
            context.close()
