"""
The material, the seams and the tile's verbs in Chromium — V5.24, lane LIB (FINAL_DELIVERY_V2 §3.3 gate 2;
BACKGROUND_MATERIAL_V2 §3.1, §3.2, §3.4, §4.2). Fixture pages built here from the library's partials (the fixtures'
bundle static/css/dist/core/sezioni.css carries v5/_materia.css after the shell), served through Playwright's route —
never a page of the site (§5, §29: the library is no catalogue). Headless: no Chromium lock slot (R12).

* pietra: the drafting grid stands on the far side and fades toward the plate — mirrored in Arabic; the protection's
  shield bookend low on the far side at 30 % of the structure's ink, its sill from the plate's far edge to the
  container's (nothing over the plate; the bookend stands down where the field is under 68 rem);
* carta viva: the light at the origin corner, mirrored; the velatura: 12 rem (8 on phones) in the next ground's colour,
  and it never animates; the incastro: the doors' band begins 64 px up with no top padding, its ground painted from
  64 px down — the first door the whole 64 px over the band above;
* the raccordo — the first child of the band it ENTERS (every .sez isolates: hung under the leaving band it was painted
  over, the gate's B2): waits (scale 1 0), draws once on that band's trigger after its own line (the draw-y verb, a
  900 ms delay), leaves document.getAnimations() when done (fill backwards), its node lands within 2 px of the band's
  head rule at 1440 and 390, in French and in Arabic — and it is PAINTED: the line's column is darker than the ground
  beside it (a clip screenshot, the reviewer's proof);
* the mosaico: its tiles ink and light their floor, no settle (sez-node) plays on a tile, the card's rule draws;
* reduced motion: no data-sec-state written, the raccordo stands drawn, nothing runs; the keyboard: nothing animates.

Improve round (label v524-lib-improve; V5.20: the same invariants or stronger, cited to FINAL_DELIVERY_V2 §3.3 and the
reviewer's QA.md B2, B4, B5): the entered band is addressed by its own attributes, the phone trigger is waited for
(wait_for_function on data-sec-state, no timeout raised), the reduced-motion check of the raccordo reads the raccordo
page, and one pixel assertion proves the paint.
"""

from __future__ import annotations

import os
from io import BytesIO

import pytest
from django.template import engines
from django.templatetags.static import static
from django.utils import translation

from tests.frontend import sezioni_fixtures as fx

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

ROUTE = "**/__fixture__/**"
HEIGHTS = {1440: 900, 1024: 768, 390: 844}

#: the fixtures: a list of sections per page — (pattern, ground, rhythm, extra attributes, body template, the section's
#: own children before its container: the raccordo's span, a child of the band it enters)
PROTEZIONE = '{% include "components/sezioni/protezione.html" with url="#" %}'
#: the entered band's head: a process head — its first line stands at the strip's content edge, where the raccordo's node
#: lands (V5.30 Fast Visual Variety Correction §5: only a panel head draws a rule, in its label's line: a page lane that lands
#: on one sets --sez-raccordo on its placement, NOTES §4)
STRIP_HEAD = ('{% include "components/sezioni/_testa.html" with role="process" title_id="t-next" title="La bande suivante"'
              ' title_lang=fr %}')
RACCORDO = '<span class="sez-raccordo" data-verb="draw-y" aria-hidden="true" style="--raccordo-x: 23px"></span>'
LEAVING = '<p{% if fr %} lang="fr"{% endif %}>La route de cette bande quitte son pied et entre dans la suivante.</p>'
FIXTURES = {
    "pietra": [("strato", "pietra", "band", "", PROTEZIONE, ""), ("strato", "paper", "strip", "", STRIP_HEAD, "")],
    "luce": [("mosaico", "paper", "band", ' data-luce="origine"', '{% include "components/sezioni/mosaico.html" with variant="grid" tiles=tiles_ampio %}', "")],
    "sfuma": [("strato", "night", "band", ' data-sfuma="stone"', '<p>Une bande de nuit dont le pied se dissout dans la pierre.</p>', ""),
              ("strato", "stone", "band", "", PROTEZIONE, "")],
    "raccordo": [("strato", "paper", "band", "", LEAVING, ""), ("strato", "stone", "strip", "", STRIP_HEAD, RACCORDO)],
    "incastro": [("strato", "paper", "band", "", '<p>La bande au-dessus des portes.</p>', ""),
                 ("mosaico", "stone", "band", " data-incastro", '{% include "components/sezioni/mosaico.html" with variant="porte" tiles=doors %}', "")],
}
ENTERED = '[data-sec="strato"][data-ground="stone"][data-rhythm="strip"]'


def page(name: str, lang: str = "fr", spacer: bool = False) -> str:
    """One fixture's document: the sections of FIXTURES[name] after the fixtures' own first strip (fx.HEAD)."""
    with translation.override(lang):
        fr = fx._fr(lang)
        ctx = fx._context(lang)
        fx._tiles_lang(ctx, fr)
        ctx["tiles_ampio"] = [{k: v for k, v in tile.items() if k != "frame_slot"} for tile in ctx["tiles"]]
        ctx.update(fr=fr, label="Repère", site={"lang": lang, "dir": "rtl" if lang == "ar" else "ltr"})
        sections = []
        for pattern, ground, rhythm, extra, body, own in FIXTURES[name]:
            html = engines["django"].from_string(body).render(ctx)
            sections.append(
                f'<section class="sez sez--{pattern}" data-sec="{pattern}" data-ground="{ground}" data-rhythm="{rhythm}"{extra}'
                f' aria-label="{pattern}">{own}<div class="container">{html}</div></section>'
            )
        head = fx.HEAD.format(
            lang=lang, dir="rtl" if lang == "ar" else "ltr", name=name, main=static("css/dist/main.css"),
            reveal=static("css/dist/core/reveal.css"), fronte=static("css/dist/pages/css/fronte.css"),
            partials=f'<link rel="stylesheet" href="{static("css/dist/core/sezioni.css")}">',
            head_js=static("js/head.js"), rtl="is-rtl" if lang == "ar" else "",
            gap="Une première bande, pour que la section commence sous la ligne de flottaison." * (60 if spacer else 6),
        )
        return head + "".join(sections) + fx.FOOT.format(rise=static("js/dist/rise.js"))


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


def _open(browser, pages: dict, width: int, **context):
    ctx = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, **context)
    pg = ctx.new_page()
    pg.route(ROUTE, lambda route: route.fulfill(body=pages[route.request.url.rsplit("/", 1)[1]],
                                               content_type="text/html; charset=utf-8"))
    return ctx, pg


def _go(pg, live_server, key: str):
    pg.goto(f"{live_server.url}/__fixture__/{key}", wait_until="load")
    pg.wait_for_timeout(250)


RECT = "s => { const r = document.querySelector(s).getBoundingClientRect(); return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height}; }"
RUNNING = """s => document.querySelector(s).getAnimations({subtree: true})
    .filter(a => !(a.timeline instanceof ScrollTimeline || a.timeline instanceof ViewTimeline))
    .map(a => [a.animationName || a.constructor.name, a.effect && a.effect.pseudoElement || '', a.playState])"""
STATE = "s => document.querySelector(s).dataset.secState"


def _luminance(pg, x: float, y: float, width: float, height: float) -> float:
    """The mean luminance of a clip of the viewport (0 black … 255 white): the paint, not the box model."""
    image = pytest.importorskip("PIL.Image").open(BytesIO(pg.screenshot(clip={"x": x, "y": y, "width": width, "height": height})))
    data = image.convert("L").tobytes()
    return sum(data) / len(data)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 1024, 390])
def test_pietra_draws_its_grid_on_the_far_side_and_the_protection_is_one_compact_band(browser, live_server, lang, width):
    """V5.29 (owner, 6 Nov 2026: «protezione__campo too dominant … one global refined compact treatment»; stream SYS;
    V5.20: the grid's letter kept, the band's held by stronger measures — it spans its field, the seal stands inside it
    at the reading edge, it stays compact, the call at the far end on a desktop, the locked text whole and visible)."""
    pages = {f"pietra-{lang}": page("pietra", lang)}
    ctx, pg = _open(browser, pages, width)
    try:
        _go(pg, live_server, f"pietra-{lang}")
        band = '[data-ground="pietra"]'
        mask = pg.evaluate("s => getComputedStyle(document.querySelector(s), '::before').maskImage", band)
        assert "linear-gradient(" in mask and ("to right" if lang == "ar" else "to left") in mask, (lang, mask)
        assert "48px" in pg.evaluate("s => getComputedStyle(document.querySelector(s), '::before').backgroundSize", band)
        plate, field = pg.evaluate(RECT, ".protezione"), pg.evaluate(RECT, ".protezione__campo")
        seal, title = pg.evaluate(RECT, ".protezione__sigillo"), pg.evaluate(RECT, ".protezione__titolo")
        assert abs(plate["width"] - field["width"]) <= 1, "the band spans its field"
        assert plate["top"] - 1 <= seal["top"] and seal["top"] + seal["height"] <= plate["top"] + plate["height"] + 1, "the seal inside"
        if width == 390:  # a phone: the seal above the title, both on the band's one start (lane H's m5)
            assert seal["bottom"] <= title["top"] + 1, (seal, title)
            if lang == "ar":
                assert plate["right"] - seal["right"] <= 40, (seal, plate)
            else:
                assert abs(seal["left"] - title["left"]) <= 1 and seal["left"] - plate["left"] <= 40, (seal, title)
        elif lang == "ar":
            assert plate["right"] - seal["right"] <= 40 and seal["left"] > title["left"], (seal, plate)
        else:
            assert seal["left"] - plate["left"] <= 40 and seal["left"] < title["left"], (seal, plate)
        assert plate["height"] <= {1440: 260, 1024: 300, 390: 600}[width], ("compact", plate["height"])
        assert pg.evaluate("document.querySelectorAll('.protezione__davanzale, .sez-fondale').length") == 0
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (the
        # senior review's P2-5): two columns from 80 rem, one measure below, and at every width no sentence of the
        # locked text is read in two pieces (none of its lines climbs back to a column's top) - a stronger invariant
        columns = pg.evaluate("getComputedStyle(document.querySelector('.protezione__testo')).columnCount")
        assert columns == ("2" if width >= 1280 else "auto"), (width, columns)
        climbs = pg.evaluate("""() => [...document.querySelectorAll('.protezione__testo .ls')].map(s => {
            const r = [...s.getClientRects()]; return r.some((x, i) => i > 0 && x.top < r[i - 1].top - 2); })""")
        assert not any(climbs), ("a sentence split between the columns", width, climbs)
        if width >= 1024:
            action = pg.evaluate(RECT, ".protezione__azione")
            if lang == "ar":
                assert action["left"] < title["left"], "the call at the band's far end"
            else:
                assert action["left"] > title["left"] + title["width"] / 2, "the call at the band's far end"
        assert pg.evaluate("document.querySelector('.protezione__testo').textContent").strip(), "the locked text stands"
        assert pg.evaluate("getComputedStyle(document.querySelector('.protezione__testo')).visibility") == "visible"
    finally:
        ctx.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_carta_viva_lights_the_origin_corner_and_the_velatura_is_a_still_ground(browser, live_server, lang):
    pages = {f"luce-{lang}": page("luce", lang), f"sfuma-{lang}": page("sfuma", lang)}
    for width in (1440, 390):
        ctx, pg = _open(browser, pages, width)
        try:
            _go(pg, live_server, f"luce-{lang}")
            image = pg.evaluate("getComputedStyle(document.querySelector('[data-luce=\"origine\"]')).backgroundImage")
            assert image.startswith("radial-gradient(") and ("at 100% 0" in image if lang == "ar" else "at 0% 0%" in image or "at 0px 0px" in image), image
            _go(pg, live_server, f"sfuma-{lang}")
            after = "s => getComputedStyle(document.querySelector(s), '::after')"
            style = pg.evaluate(after + ".height", '[data-sfuma="stone"]')
            assert style == ("128px" if width == 390 else "192px"), (width, style)
            assert "linear-gradient(" in pg.evaluate(after + ".backgroundImage", '[data-sfuma="stone"]')
            pg.evaluate("document.querySelector('[data-sfuma]').scrollIntoView({block: 'center'})")
            pg.wait_for_timeout(400)
            assert not [a for a in pg.evaluate(RUNNING, "[data-sfuma]") if a[1] == "::after"], "a fade is a ground, never a verb"
        finally:
            ctx.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 390])
def test_the_raccordo_waits_draws_once_after_the_band_s_line_lands_on_its_head_and_is_painted(browser, live_server, lang, width):
    pages = {f"raccordo-{lang}": page("raccordo", lang, spacer=True)}
    ctx, pg = _open(browser, pages, width)
    try:
        _go(pg, live_server, f"raccordo-{lang}")
        assert pg.evaluate("s => document.querySelector('.sez-raccordo').parentElement.matches(s)", ENTERED), \
            "the span is the first child of the band it enters"
        assert pg.evaluate(STATE, ENTERED) == "wait"
        assert pg.evaluate("getComputedStyle(document.querySelector('.sez-raccordo')).scale") == "1 0", "the first frame: the line not yet drawn"
        pg.evaluate("s => document.querySelector(s).scrollIntoView({block: 'start'})", ENTERED)
        pg.wait_for_function("s => document.querySelector(s).dataset.secState === 'in'", arg=ENTERED)
        running = pg.evaluate(RUNNING, ".sez-raccordo")
        names = {a[0] for a in running}
        assert "sez-draw-y" in names, running
        delay = pg.evaluate("getComputedStyle(document.querySelector('.sez-raccordo')).animationDelay")
        assert delay == "0.9s", ("after the band's own line: --sez-d = --motion-draw", delay)
        pg.wait_for_timeout(3200)
        assert pg.evaluate(RUNNING, ".sez-raccordo") == [], "a finished entrance leaves getAnimations()"
        line = pg.evaluate(RECT, ".sez-raccordo")
        # V5.20 strict rule, V5.30 Fast Visual Variety Correction §5: the head draws no rule, the same place is the head's top
        rule = pg.evaluate(RECT, ENTERED + " .testa")
        assert pg.evaluate("s => document.querySelector(s).querySelectorAll('.testa__rule').length", ENTERED) == 0
        band = pg.evaluate(RECT, ENTERED)
        assert round(line["height"]) == (32 if width == 390 else 48), line
        assert abs(line["top"] - band["top"]) <= 1, "it crosses the seam: from the band's top edge"
        assert abs(line["bottom"] - rule["top"]) <= 2, ("the node on the band's head", line["bottom"], rule["top"])
        node = pg.evaluate("s => { const cs = getComputedStyle(document.querySelector(s), '::after'); return [cs.width, cs.height, cs.backgroundColor]; }", ".sez-raccordo")
        assert node[0] == "6px" and node[1] == "6px", node
        x = pg.evaluate("getComputedStyle(document.querySelector('.sez-raccordo')).insetInlineStart")
        assert x == "23px", "placed on the route by --raccordo-x"
        # the paint (B2): the line's 2 px column, from the seam to the node, is darker than the ground 12 px beside it
        x0, y0, h = line["left"] - 1, max(line["top"], 0) + 2, line["height"] - 10
        ink = _luminance(pg, x0, y0, 4, h)
        ground = _luminance(pg, x0 + (-12 if lang == "ar" else 12), y0, 4, h)
        assert ground - ink >= 20, ("not one pixel of the line is painted", ink, ground)
    finally:
        ctx.close()


def test_the_incastro_begins_sixty_four_pixels_up_and_the_doors_stand_over_the_band_above(browser, live_server):
    pages = {"incastro-fr": page("incastro", "fr")}
    ctx, pg = _open(browser, pages, 1440)
    try:
        _go(pg, live_server, "incastro-fr")
        above = pg.evaluate(RECT, '[data-ground="paper"][data-sec="strato"]')
        doors = pg.evaluate(RECT, "[data-incastro]")
        assert round(above["bottom"] - doors["top"]) == 64, (above, doors)
        image = pg.evaluate("getComputedStyle(document.querySelector('[data-incastro]')).backgroundImage")
        assert image.startswith("linear-gradient(") and "64px" in image, image
        first_door = pg.evaluate(RECT, "[data-incastro] .mosaico__tessera")
        # B4: the band's own top padding sank the first door 32 px under the seam; with none, its arched top stands the
        # whole 64 px over the band above (the overlap the audit drew)
        assert above["bottom"] - first_door["top"] >= 63, ("the doors' arched tops rise into the band above", above["bottom"], first_door["top"])
        assert pg.evaluate("getComputedStyle(document.querySelector('[data-incastro] > .container')).zIndex") == "1"
    finally:
        ctx.close()


def test_the_mosaico_s_tiles_ink_and_light_and_never_settle(browser, live_server):
    """RESTATED under V5.20 for FINAL MICRO-PASS §5 A3 (the tile is bare: no vault, no lit floor, no foot rule): as
    the section enters the glyph still inks in and the row's threshold still draws, but no layer of the tile runs and
    nothing settles after it — the tile bare before and after."""
    pages = {"mosaico-fr": fx.page("mosaico", "fr", spacer=True)}
    ctx, pg = _open(browser, pages, 1440)
    bare = (
        "() => { const t = document.querySelector('.mosaico .sez-tile'), cs = getComputedStyle(t);"
        " return [getComputedStyle(t, '::before').content, getComputedStyle(t, '::after').content,"
        " cs.backgroundImage, cs.boxShadow, !!t.querySelector('svg.icon')]; }"
    )
    try:
        _go(pg, live_server, "mosaico-fr")
        sec = '[data-sec="mosaico"]'
        assert pg.evaluate(STATE, sec) == "wait"
        assert pg.evaluate(bare) == ["none", "none", "none", "none", True]
        pg.evaluate("s => document.querySelector(s).scrollIntoView({block: 'center'})", sec)
        pg.wait_for_function("s => document.querySelector(s).dataset.secState === 'in'", arg=sec)
        running = pg.evaluate(RUNNING, sec)
        names = {a[0] for a in running}
        assert not names & {"sez-node", "sez-layer"} and {"sez-ink", "sez-draw"} <= names, running
        pg.wait_for_timeout(3200)
        assert pg.evaluate(RUNNING, sec) == []
        assert pg.evaluate(bare) == ["none", "none", "none", "none", True]
    finally:
        ctx.close()


def test_under_reduced_motion_and_from_the_keyboard_the_raccordo_stands_drawn_and_nothing_runs(browser, live_server):
    pages = {"mosaico-fr": fx.page("mosaico", "fr", spacer=True), "raccordo-fr": page("raccordo", "fr", spacer=True)}
    ctx, pg = _open(browser, pages, 1440, reduced_motion="reduce")
    try:
        for key in pages:  # the raccordo page last: its line is read where it stands
            _go(pg, live_server, key)
            pg.evaluate("document.querySelector('[data-sec]:not([data-rhythm=strip])').scrollIntoView()")
            pg.wait_for_timeout(200)
            assert pg.evaluate("document.querySelectorAll('[data-sec-state]').length") == 0, key
            assert pg.evaluate("document.getAnimations().filter(a => a.playState === 'running').length") == 0, key
        assert pg.evaluate("getComputedStyle(document.querySelector('.sez-raccordo')).scale") == "none", "drawn at rest under reduced motion"
    finally:
        ctx.close()
    ctx, pg = _open(browser, pages, 1440)
    try:
        _go(pg, live_server, "raccordo-fr")
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(100)
        assert pg.evaluate("document.documentElement.dataset.input") == "key"
        pg.evaluate("s => document.querySelector(s).scrollIntoView({block: 'start'})", ENTERED)
        pg.wait_for_timeout(300)
        assert pg.evaluate("document.getAnimations().filter(a => a.playState === 'running').length") == 0, "the keyboard sees the still"
        assert pg.evaluate("getComputedStyle(document.querySelector('.sez-raccordo')).scale") == "none"
    finally:
        ctx.close()
