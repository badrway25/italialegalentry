"""
V5.24 lane PUB1 — the material pass in Chromium (FINAL_DELIVERY_V2 §3.5 gate 2, R3, R5; BACKGROUND_MATERIAL_V2 §3.2, §3.4,
§4.2; label v524-pub1-build). Headless: no Chromium lock slot (R12). The seeded site, gate G3 open, the clock at 3 October
2026 through `core.clock.now` (as test_pages_browser_v522_p1.py — a frozen monotonic clock stalls Playwright).

* the three raccordi (v5/_materia.css, R3's name) each the FIRST CHILD of the band it enters (LIB NOTES §4 c): held below
  the fold it waits (scale 1 0), draws once on that band's trigger after the band's own line (the draw-y verb, --sez-d =
  --motion-draw: a 0.9 s delay), leaves document.getAnimations() when done, and its node lands within 2 px of the line it
  was placed on — the board's trunk rising 48 px (32 on phones) into the head's foot (Parcours), the filo's line into the
  night band down to its head rule (a sheet: the band's own padding), the dossier's route into the protection down to the
  plate's 3 px rule (Diplômes) — on the route's own x, in French and in Arabic, at 1440 and 390; and it is PAINTED (the
  line's column against the ground beside it — LIB's proof, B2);
* the velatura at the chamber's foot is a still ground (12 rem; 8 on phones) and the band's words stand above it;
* the «Comment ça marche» plates' tiles ink and light their floor and never settle (§3.4 PA-2); the grids are «carta viva»;
* Formation's order (R5) and the pilot's route on the wash with its status plate standing on it; the filiera's sfumatura;
* reduced motion: no state written, the raccordi stand drawn, nothing runs; the keyboard: nothing animates;
* the eight pages hold their width at 1024 and 360 — the two widths the v522 twin does not read —, fr and ar, 0 console errors;
* V5.29 §15–§17 «l'intesa» (the Italy + Morocco ground of the collaboration proposal's head and the landing's approdo;
  since the FINAL MICRO-PASS's review the landing's approdo draws none, and a closing band's ground is read on Réseau's):
  aria-hidden, no text, the flags NEVER mirrored (no transform, the Italian green at the hoist, the pentagram upright and
  unflipped) while the placement follows the reading edge, the words' contrast ≥ 4.5 on the composed ground (1440 and 390, fr
  and ar), one slow reveal from each outer edge that leaves getAnimations(), a still under reduced motion.
"""

from __future__ import annotations

import datetime as dt
import os
from io import BytesIO

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PAGES = (
    "parcours/",
    "parcours/salaried_work/",
    "projet-pilote/",
    "entreprises/",
    "institutions/",
    "universites-et-formation/",
    "formation/",
    "diplomes-et-titres/",
)
HEIGHTS = {1440: 900, 1024: 768, 390: 844, 360: 740}
#: path → (the band the raccordo enters, the line its node lands on — None: the head's foot —, the modifier, the route the
#: line continues and the x on it (fr; mirrored in Arabic), its length at 1440 and at 390)
#: FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the board's trunk left with the head's spine and its arrival disc, so
#: «Parcours» keeps no raccordo either — no page draws one (the filo's and the dossier's: below and test_pages_v522_p1);
#: the band it entered and the route it continued still stand. path → (the band, the route)
#: RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the band
#: the trunk entered is lane B's explorer strip, and the route it continued the explorer's families (`esplora__indice`)
FORMER_RACCORDI = {"parcours/": ("section.esplora-sez", ".esplora__indice")}

RECT = "s => { const r = document.querySelector(s).getBoundingClientRect(); return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height}; }"
RUNNING = """s => document.querySelector(s).getAnimations({subtree: true})
    .filter(a => !(a.timeline instanceof ScrollTimeline || a.timeline instanceof ViewTimeline))
    .map(a => [a.animationName || a.constructor.name, a.effect && a.effect.pseudoElement || '', a.playState])"""
STATE = "s => document.querySelector(s).dataset.secState"
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


def _luminance(page, x: float, y: float, width: float, height: float) -> float:
    """The mean luminance of a clip of the viewport (0 black … 255 white): the paint, not the box model."""
    image = pytest.importorskip("PIL.Image").open(
        BytesIO(page.screenshot(clip={"x": x, "y": y, "width": width, "height": height}))
    )
    data = image.convert("L").tobytes()
    return sum(data) / len(data)


def _bring(page, selector: str, offset: int = 300) -> None:
    """Scroll so the band's top edge stands `offset` px under the viewport's top — the seam and the raccordo in view — and a
    quarter of the band shows (the runtime's trigger, rise.js): a band taller than that lowers the offset, never under the
    scrolled letterhead's 56 px plus the primitive's 48 px."""
    page.evaluate(
        """([s, o]) => {
          const r = document.querySelector(s).getBoundingClientRect();
          const room = Math.max(104, Math.min(o, innerHeight - Math.ceil(r.height / 4) - 20));
          // instant: the shell scrolls smoothly (chrome.css), and a box read mid-scroll is read against a moving page
          scrollTo({top: scrollY + r.top - room, behavior: "instant"});
        }""",
        [selector, offset],
    )
    page.wait_for_timeout(120)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 390])
def test_each_raccordo_waits_draws_once_after_its_band_s_line_lands_on_its_line_and_is_painted(
    browser, live_server, open_pages, lang, width
):
    context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]})
    page = context.new_page()
    try:
        # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the raccordo is absent from the page it served; the band it entered
        # and the route it continued still stand, in French and in Arabic, at 1440 and 390
        for path, (band, route) in FORMER_RACCORDI.items():
            where = (lang, width, path)
            page.goto(f"{live_server.url}/{lang}/{path}", wait_until="networkidle")
            assert page.evaluate("() => document.querySelectorAll('.sez-raccordo').length") == 0, where
            _bring(page, band)
            assert page.evaluate(RECT, band)["height"] > 0 and page.evaluate(RECT, route)["height"] > 0, where
    finally:
        context.close()


@pytest.mark.parametrize("width", [1440, 390])
def test_no_fade_at_the_chamber_s_foot_and_its_words_stand_on_the_plate(browser, live_server, open_pages, width):
    """V5.30 Fast Visual Variety Correction §7 INSTITUTIONS, «premium split» (V5.20 strict rule; this decision replaces «la
    velatura» at the chamber's foot): the night plate ends on its own edge, nothing is painted or runs on its ::after, and
    the words stand inside it."""
    context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/institutions/", wait_until="networkidle")
        band = "section#destinataires"
        after = "s => getComputedStyle(document.querySelector(s), '::after')"
        assert page.evaluate(after + ".backgroundImage", band) == "none"
        _bring(page, band, 120)
        page.wait_for_function("s => document.querySelector(s).dataset.secState !== 'wait'", arg=band)
        page.wait_for_timeout(600)
        assert not [a for a in page.evaluate(RUNNING, band) if a[1] == "::after"], "a fade is a ground, never a verb"
        box, words = page.evaluate(RECT, band), page.evaluate(RECT, f"{band} .istituzioni-aula__piede")
        assert box["top"] <= words["top"] and words["bottom"] <= box["bottom"], (box, words, "on the night's own ground")
    finally:
        context.close()


def test_the_come_plates_tiles_ink_and_light_and_never_settle_and_the_grids_are_carta_viva(
    browser, live_server, open_pages
):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/", wait_until="networkidle")
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026:
        # «Comment ça marche» is lane B's band (`esplora-come`)
        band = "section.esplora-come"
        assert page.evaluate(STATE, band) == "wait"
        # FINAL MICRO-PASS §5 A2 (V5.20 strict rule: the plates' tiles, their ink and their lit floor left — a station is
        # the quiet sequence marker): no tile; four markers, each its figure; the band enters, then nothing runs —
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no numbering»):
        # the four markers are four empty rings on one rail, hidden from assistive technology, no figure drawn in any
        assert page.evaluate("document.querySelectorAll('.come .sez-tile').length") == 0
        rings = page.evaluate(
            "[...document.querySelectorAll('.come .come__punto')]"
            ".map(n => [n.textContent, getComputedStyle(n, '::before').content, n.getAttribute('aria-hidden')])"
        )
        assert len(rings) == 4 and all(ring == ["", "none", "true"] for ring in rings), rings
        _bring(page, band, 120)
        page.wait_for_function("s => document.querySelector(s).dataset.secState === 'in'", arg=band)
        names = {a[0] for a in page.evaluate(RUNNING, band)}
        assert not names & {"sez-node", "sez-ink", "sez-layer"}, names
        page.wait_for_timeout(3200)
        assert page.evaluate(RUNNING, band) == []
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
        # correction round of the senior integration review (P2-3, lane B) — the space's register of links stands once,
        # on /parcours/, still on «carta viva»; Formation and Diplômes close on ONE band on «pietra» and draw no grid
        for path, grids in (("parcours/", 1), ("formation/", 0), ("diplomes-et-titres/", 0)):
            page.goto(f"{live_server.url}/fr/{path}", wait_until="load")
            assert page.evaluate("document.querySelectorAll('[data-luce=\"origine\"]').length") == grids, path
            if not grids:
                continue
            image = page.evaluate("getComputedStyle(document.querySelector('[data-luce=\"origine\"]')).backgroundImage")
            assert image.startswith("radial-gradient(") and ("at 0% 0%" in image or "at 0px 0px" in image), (
                path,
                image,
            )
    finally:
        context.close()


def test_formation_s_order_the_pilot_s_route_on_the_wash_and_the_filiera_s_sfumatura(browser, live_server, open_pages):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/formation/", wait_until="load")
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the grid of
        # the space's pages is lane B's «spazio» (`section.spazio`) — the same order
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
        # correction round of the senior integration review (P2-3, lane B) — the protection, the grid and the boussole
        # are ONE closing band («la chiusura»): the traversata, then that band, the last of the page's bands
        tops = page.evaluate("""() => ['.formazione-traversata', '.persone-protezione[data-action="orientation"]']
            .map(s => document.querySelector(s).getBoundingClientRect().top)""")
        assert tops == sorted(tops), ("R5: la traversata → la chiusura", tops)
        assert page.evaluate("[...document.querySelectorAll('main .sez')].at(-1).dataset.action") == "orientation"
        page.goto(f"{live_server.url}/fr/projet-pilote/", wait_until="load")
        state = page.evaluate("""() => {
          const band = document.querySelector('#sequence'), plate = document.querySelector('[data-notice="pilot-not-authorised"] .notice');
          const b = band.getBoundingClientRect(), p = plate.getBoundingClientRect();
          return {wash: getComputedStyle(band).backgroundImage, plateBg: getComputedStyle(plate).backgroundColor,
                  inside: p.top >= b.top && p.bottom <= b.bottom, rhythm: band.dataset.rhythm};
        }""")
        assert "gradient(" in state["wash"] and state["rhythm"] == "band", state
        assert state["plateBg"] not in ("rgba(0, 0, 0, 0)", "transparent") and state["inside"], state
        page.goto(f"{live_server.url}/fr/universites-et-formation/", wait_until="load")
        band = "section#filiere"
        before = page.evaluate("s => getComputedStyle(document.querySelector(s), '::before')", band)
        assert "inset" in before["boxShadow"] and "gradient(" in page.evaluate(
            "s => getComputedStyle(document.querySelector(s)).backgroundImage", band
        ), before["boxShadow"]
        assert not [a for a in page.evaluate(RUNNING, band) if a[1] == "::before"], "the sfumatura never moves"
    finally:
        context.close()


def test_under_reduced_motion_and_from_the_keyboard_the_seams_stand_drawn_and_nothing_runs(
    browser, live_server, open_pages
):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    try:
        for path, (band, _route) in FORMER_RACCORDI.items():
            page.goto(f"{live_server.url}/fr/{path}", wait_until="networkidle")
            _bring(page, band)
            page.wait_for_timeout(300)
            assert page.evaluate("document.querySelectorAll('[data-sec-state]').length") == 0, path
            assert page.evaluate("document.getAnimations().filter(a => a.playState === 'running').length") == 0, path
            # FINAL MICRO-PASS §5 A3: the seam's raccordo left — nothing to stand drawn, nothing to run
            assert page.evaluate("s => document.querySelector(s + ' > .sez-raccordo')", band) is None, path
        page.goto(f"{live_server.url}/fr/institutions/", wait_until="networkidle")
        page.mouse.wheel(0, 1600)
        page.wait_for_timeout(400)
        assert page.evaluate("document.getAnimations().filter(a => a.playState === 'running').length") == 0
    finally:
        context.close()
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/parcours/salaried_work/", wait_until="networkidle")
        page.keyboard.press("Tab")
        page.wait_for_timeout(100)
        assert page.evaluate("document.documentElement.dataset.input") == "key"
        _bring(page, "section#autorites")
        page.wait_for_timeout(300)
        # the band's own animations (the frontispiece keeps its halo loop outside reduced motion: the head's, not this lane's);
        # the states written at load stay — the keyboard tier stills the verbs through :root:not([data-input="key"])
        assert page.evaluate(RUNNING, "section#autorites") == [], "the keyboard sees the still"
        assert page.evaluate("document.querySelector('section#autorites .sez-raccordo') === null"), "V5.30 VARIETY §5"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_pages_hold_their_width_at_1024_and_360_with_no_console_error(browser, live_server, open_pages, lang):
    for width in (1024, 360):
        context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, reduced_motion="reduce")
        page = context.new_page()
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text[:160]) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)[:160]))
        try:
            for path in PAGES:
                page.goto(f"{live_server.url}/{lang}/{path}", wait_until="load")
                state = page.evaluate(OVERFLOW)
                assert state["over"] <= 0 and not state["outside"], (lang, width, path, state)
            assert errors == [], (lang, width, errors)
        finally:
            context.close()


# ---- V5.29 §15–§17: «l'intesa», the Italy + Morocco ground of the Espace Institutions -------------------------------

INTESA = """() => {
  const layer = document.querySelector('.intesa');
  if (!layer) return null;
  const vw = document.documentElement.clientWidth;
  const it = layer.querySelector('svg[data-flag="it"]'), ma = layer.querySelector('svg[data-flag="ma"]');
  const r = el => el.getBoundingClientRect();
  const screen = (el, x, y) => { const m = el.getScreenCTM(); return [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]; };
  const chain = [];
  for (const start of [it, ma]) {
    for (let el = start; el && el !== document.body; el = el.parentElement) {
      const cs = getComputedStyle(el);
      chain.push([cs.transform, cs.scale, cs.rotate, cs.translate]);
    }
  }
  const star = ma.querySelector('.intesa__stella');
  const pts = star.getAttribute('points').trim().split(/\\s+/).map(p => p.split(',').map(Number)).map(([x, y]) => screen(star, x, y));
  const green = r(it.querySelector('[data-band="verde"]')), red = r(it.querySelector('[data-band="rosso"]'));
  return {
    hidden: layer.getAttribute('aria-hidden'), text: layer.textContent.trim(), pointer: getComputedStyle(layer).pointerEvents,
    blend: getComputedStyle(layer).mixBlendMode, z: getComputedStyle(layer).zIndex, chain,
    itScale: it.getScreenCTM().a, maScale: ma.getScreenCTM().a, starScale: [star.getScreenCTM().a, star.getScreenCTM().d],
    green: [green.left, green.right], red: [red.left, red.right], vw,
    maCentre: (r(ma).left + r(ma).right) / 2, itBox: [r(it).left, r(it).right], pts,
    parentFirst: layer.parentElement.firstElementChild === layer, parent: layer.parentElement.className,
  };
}"""


def _srgb(channel: float) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _relative(px) -> float:
    return 0.2126 * _srgb(px[0]) + 0.7152 * _srgb(px[1]) + 0.0722 * _srgb(px[2])


def _contrast(a, b) -> float:
    la, lb = _relative(a), _relative(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _assert_flags_unmirrored(state, where, lang):
    assert state is not None, (where, "the ground is drawn")
    assert state["hidden"] == "true" and state["text"] == "" and state["pointer"] == "none", (where, state["hidden"])
    # THE FLAGS ARE NEVER MIRRORED (V5.29, the owner's correction of 6 Nov 13:12): no transform on the drawings or any
    # ancestor, the drawings' screen matrices positive, the Italian green at the hoist (left of the red) in either
    # language, the pentagram upright and unflipped (its first point on top, its left arm on the left)
    assert all(t == ["none", "none", "none", "none"] for t in state["chain"]), (where, state["chain"])
    assert state["itScale"] > 0 and state["maScale"] > 0 and min(state["starScale"]) > 0, where
    assert state["green"][1] <= state["red"][0], (where, "the Italian green at the hoist", state["green"], state["red"])
    top, right_down, left, right, left_down = state["pts"]
    assert top[1] < min(p[1] for p in (right_down, left, right, left_down)), (where, "the pentagram upright")
    assert left[0] < top[0] < right[0] and left_down[0] < right_down[0], (
        where,
        "the pentagram unflipped",
        state["pts"],
    )
    # the PLACEMENT follows the reading edge: Italy at the start edge, Morocco at the far edge
    vw = state["vw"]
    if lang == "ar":
        assert abs(state["itBox"][1] - vw) <= 1 and state["maCentre"] < vw / 2, (
            where,
            state["itBox"],
            state["maCentre"],
        )
    else:
        assert abs(state["itBox"][0]) <= 1 and state["maCentre"] > vw / 2, (where, state["itBox"], state["maCentre"])


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 390])
def test_the_institutions_collaboration_head_stands_on_l_intesa_unmirrored_and_the_words_keep_their_contrast(
    browser, live_server, open_pages, lang, width
):
    context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, reduced_motion="reduce")
    page = context.new_page()
    try:
        where = (lang, width, "collaboration/institutions/")
        page.goto(f"{live_server.url}/{lang}/collaboration/institutions/", wait_until="networkidle")
        state = page.evaluate(INTESA)
        _assert_flags_unmirrored(state, where, lang)
        assert state["parentFirst"] and state["parent"] == "intesa-campo", where
        assert state["blend"] == "multiply" and state["z"] == "1", (where, "multiplied into the ground")
        assert page.evaluate("document.querySelector('.intesa').getAnimations({subtree: true}).length") == 0, (
            where,
            "a still composition under reduced motion",
        )
        # the words' contrast on the composed ground: the text made transparent, the ground read under each text box
        # (its darkest pixel, the worst case) against the text's own ink
        texts = [
            ".intesa-campo .ingresso__title",
            ".intesa-campo .ingresso__text .ingresso__lead",
            ".emiciclo-nota__frase",
        ]
        inks = page.evaluate(
            "ss => ss.map(s => getComputedStyle(document.querySelector(s)).color.match(/[\\d.]+/g).slice(0, 3).map(Number))",
            texts,
        )
        # (through the CSSOM: the CSP refuses an inline style sheet)
        page.evaluate(
            "() => document.querySelectorAll('.intesa-campo, .intesa-campo *')"
            ".forEach(el => el.style.setProperty('color', 'transparent', 'important'))"
        )
        image_module = pytest.importorskip("PIL.Image")
        for selector, ink in zip(texts, inks, strict=True):
            box = page.evaluate(RECT, selector)
            clip = {
                "x": max(0, box["left"]),
                "y": box["top"],
                "width": min(box["width"], width),
                "height": box["height"],
            }
            shot = image_module.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
            darkest = min(shot.getdata(), key=_relative)
            assert _contrast(ink, darkest) >= 4.5, (where, selector, ink, darkest, round(_contrast(ink, darkest), 2))
    finally:
        context.close()


def test_l_intesa_reveals_once_from_each_outer_edge_and_leaves_and_the_landing_s_approdo_carries_it(
    browser, live_server, open_pages
):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/collaboration/institutions/", wait_until="load")
        svgs = "[...document.querySelectorAll('.intesa svg')]"
        names = page.evaluate(
            f"{svgs}.map(s => getComputedStyle(s).animationName + ' ' + getComputedStyle(s).animationDuration)"
        )
        assert names == ["reveal-mask 2.2s", "reveal-mask 2.2s"], names
        froms = page.evaluate(f"{svgs}.map(s => getComputedStyle(s).getPropertyValue('--reveal-from').trim())")
        assert froms == ["inset(0 100% 0 0)", "inset(0 0 0 100%)"], ("each from its outer edge inward", froms)
        page.wait_for_timeout(3000)
        assert page.evaluate("document.querySelector('.intesa').getAnimations({subtree: true}).length") == 0
        # RESTATED under V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 5: the pentagram's line crossed the
        # closing list's rows and chevrons): the Institutions landing's «Pour aller plus loin» draws no ground, its links
        # still there; a closing band's ground — unmirrored, the band's first child, under its words, revealed on the
        # band's own trigger — is read on Réseau's, the closing band that carries it: the same checks, another surface
        for lang in ("fr", "ar"):
            page.goto(f"{live_server.url}/{lang}/institutions/", wait_until="load")
            landing = page.evaluate(
                "() => [document.querySelectorAll('.intesa').length,"
                " document.querySelectorAll('section.ecosistema-approdo a.approdo__link').length]"
            )
            assert landing[0] == 0 and landing[1] >= 2, (lang, "institutions/", landing)
            # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
            # (lane D; the brief's «no literal flag bands»): Réseau's closing band is held apart the same way — no
            # ground, its links still there —, and the closing band that carries the primitive is AGAMI's: the same
            # checks, another surface
            page.goto(f"{live_server.url}/{lang}/reseau/", wait_until="load")
            network = page.evaluate(
                "() => [document.querySelectorAll('.intesa').length,"
                " document.querySelectorAll('section.rete-approdo a.mosaico__link').length]"
            )
            assert network[0] == 0 and network[1] >= 2, (lang, "reseau/", network)
            page.goto(f"{live_server.url}/{lang}/agami/", wait_until="load")
            state = page.evaluate(INTESA)
            _assert_flags_unmirrored(state, (lang, 1440, "agami/"), lang)
            assert state["parentFirst"] and "agami-approdo" in state["parent"] and state["z"] == "-1", state
        # on AGAMI the band reveals on its own trigger (rise.js's wait / in), not at load below the fold
        band = "section.agami-approdo"
        if page.evaluate(STATE, band) == "wait":
            assert page.evaluate(f"getComputedStyle(document.querySelector('{band} > .intesa svg')).clipPath") != "none"
            _bring(page, band, 120)
            page.wait_for_function("s => document.querySelector(s).dataset.secState === 'in'", arg=band)
            assert "reveal-mask" in page.evaluate(
                f"getComputedStyle(document.querySelector('{band} > .intesa svg')).animationName"
            )
            page.wait_for_timeout(3000)
            assert (
                page.evaluate(f"document.querySelector('{band} > .intesa').getAnimations({{subtree: true}}).length")
                == 0
            )
        page.goto(f"{live_server.url}/fr/collaboration/universites-formation/", wait_until="load")
        assert page.evaluate("document.querySelector('.intesa')") is None, "a university's page draws none"
    finally:
        context.close()
