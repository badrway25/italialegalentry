"""
The composition library V2 in Chromium (design V5.22, SECTION_SYSTEM_V2 §9.1 «Proof»; lane S): every pattern's fixture
(tests/frontend/sezioni_fixtures.py — fixtures, never a page of the site) at the eight widths of §9.9 in French and in
Arabic, under reduced motion, from the keyboard and without script.

* no width scrolls the page sideways, in either direction of reading — and no text is cut by a section's own clip
  (`.sez` clips its inline overflow: a too-wide row would otherwise vanish silently, as a fieldset's chips once did);
* a section below the fold waits, then plays its entrance once — and once finished nothing is held
  (`document.getAnimations()` empty: fill `backwards`, V5.20); under reduced motion no state is written and nothing
  animates: every section is its designed still;
* the tabs (L) and the map (H) are operated from the keyboard (Arrows, Home, End, Escape), their panels stacked in one
  cell (a selection never moves the page); without script every panel and every entry stands in reading order;
* a locked text cut into levels keeps its textContent (la protezione).

Round 1 (label v522-s-improve1, QA_ROUND1 M1, M2, m2, m8):
* a tablist owns its tabs and nothing else — its list items step out of the tree (role none) while it is a tablist and
  come back when it is a list again; a panel's heading holds a button only as a phone's disclosure (axe's
  aria-required-children, aria-required-parent and listitem, at 0 for indice, explorer and mappa);
* «la linea V2» stands drawn at rest — in view at load and from the keyboard, every connector (the carriage return's
  turns included) at its full scale, unclipped, with no animation driving it (never the V5.12 scroll-linked reveal);
* «il flusso»: one curve through every node, drawn in its wrapper (never inside the list), right to left in Arabic;
* «il passaggio»: the rail snaps and scrolls inside itself, a focused plate stands inside it, its position rule is bound
  to the rail's own scroll;
* a band that declares its light sweeps it once as it enters (K «lo strato», «l'approdo»).
"""

from __future__ import annotations

import os

import pytest

from cms import locked_content
from tests.frontend import sezioni_fixtures as fx

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser]

WIDTHS = {1440: 900, 1280: 800, 1024: 768, 768: 1024, 430: 932, 390: 844, 375: 812, 360: 800}
ROUTE = "**/__fixture__/**"
#: every element with its own text lies inside the viewport's inline extent, unless it sits in a scroller of its own
CUT = """() => {
  const W = document.documentElement.clientWidth, out = [];
  for (const sec of document.querySelectorAll('[data-sec]')) {
    for (const el of sec.querySelectorAll('*')) {
      if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
      let a = el.parentElement, scroller = false;
      while (a && a !== sec) { if (/auto|scroll/.test(getComputedStyle(a).overflowX)) { scroller = true; break; } a = a.parentElement; }
      const r = el.getBoundingClientRect();
      if (scroller || !r.width || getComputedStyle(el).visibility !== 'visible') continue;
      if (r.left < -0.5 || r.right > W + 0.5) out.push([el.className || el.tagName, Math.round(r.left), Math.round(r.right), W]);
    }
  }
  return out;
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


def _open(browser, live_server, pages: dict, width: int, **context):
    ctx = browser.new_context(viewport={"width": width, "height": WIDTHS.get(width, 900)}, **context)
    page = ctx.new_page()
    page.route(ROUTE, lambda route: route.fulfill(body=pages[route.request.url.rsplit("/", 1)[1]],
                                                 content_type="text/html; charset=utf-8"))
    return ctx, page


def _go(page, live_server, key: str):
    page.goto(f"{live_server.url}/__fixture__/{key}", wait_until="load")
    page.wait_for_timeout(250)


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_pattern_scrolls_the_page_sideways_at_any_width(browser, live_server, lang):
    pages = {f"{name}-{lang}": fx.page(name, lang) for name in fx.NAMES}
    for width in WIDTHS:
        ctx, page = _open(browser, live_server, pages, width)
        try:
            for key in pages:
                _go(page, live_server, key)
                page.evaluate("document.querySelector('[data-sec]:not([data-rhythm=strip])').scrollIntoView()")
                over = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                assert over <= 0, (key, width, over)
                assert page.evaluate(CUT) == [], (key, width, "text cut by the section's clip")
        finally:
            ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("name", ["linea", "protezione", "mosaico", "campata", "strato", "approdo"])
def test_a_section_below_the_fold_waits_plays_once_and_holds_nothing(browser, live_server, name):
    pages = {f"{name}-fr": fx.page(name, "fr", spacer=True)}
    sel = f'[data-sec="{name}"]'
    ctx, page = _open(browser, live_server, pages, 1440)
    try:
        _go(page, live_server, f"{name}-fr")
        state = page.evaluate("s => document.querySelector(s).dataset.secState", sel)
        assert state == "wait", (name, state)
        page.evaluate("s => document.querySelector(s).scrollIntoView({block: 'center'})", sel)
        page.wait_for_timeout(200)
        assert page.evaluate("s => document.querySelector(s).dataset.secState", sel) == "in"
        running = page.evaluate("s => document.querySelector(s).getAnimations({subtree: true}).length", sel)
        assert running > 0, (name, "the entrance plays")
        page.wait_for_timeout(3200)
        left = page.evaluate("""s => document.querySelector(s).getAnimations({subtree: true})
            .filter(a => !(a.timeline instanceof ScrollTimeline || a.timeline instanceof ViewTimeline)).length""", sel)
        assert left == 0, (name, "a finished entrance leaves getAnimations() (fill backwards)")
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", [1440, 390])
def test_under_reduced_motion_every_section_is_its_still(browser, live_server, width):
    pages = {f"{name}-fr": fx.page(name, "fr", spacer=True) for name in ("linea", "protezione", "campata", "mappa", "sigillo")}
    ctx, page = _open(browser, live_server, pages, width, reduced_motion="reduce")
    try:
        for key in pages:
            _go(page, live_server, key)
            page.evaluate("document.querySelector('[data-sec]:not([data-rhythm=strip])').scrollIntoView()")
            page.wait_for_timeout(150)
            states = page.evaluate("[...document.querySelectorAll('[data-sec-state]')].length")
            assert states == 0, (key, "no state is written under reduced motion")
            moving = page.evaluate("""document.getAnimations().filter(a => a.playState === 'running'
                && !(a.timeline instanceof ScrollTimeline || a.timeline instanceof ViewTimeline)).length""")
            assert moving == 0, (key, moving)
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_tabs_and_the_map_from_the_keyboard(browser, live_server, lang):
    pages = {f"indice-{lang}": fx.page("indice", lang), f"mappa-{lang}": fx.page("mappa", lang)}
    ctx, page = _open(browser, live_server, pages, 1440)
    try:
        _go(page, live_server, f"indice-{lang}")
        page.wait_for_selector(".indice[data-mode='tabs']")
        tabs = page.locator(".indice__voce")
        assert tabs.nth(0).get_attribute("aria-selected") == "true"
        assert page.locator(".indice__lista").get_attribute("role") == "tablist"
        tabs.nth(0).focus()
        page.keyboard.press("ArrowDown")
        assert tabs.nth(1).get_attribute("aria-selected") == "true"
        assert page.evaluate("document.activeElement.id") == tabs.nth(1).get_attribute("id")
        boxes = page.evaluate("[...document.querySelectorAll('.indice__pannello')].map(p => p.getBoundingClientRect().top)")
        assert len({round(b) for b in boxes}) == 1, "the panels stand in one cell: no selection moves the page"
        page.keyboard.press("End")
        assert tabs.nth(tabs.count() - 1).get_attribute("aria-selected") == "true"
        visible = page.evaluate("[...document.querySelectorAll('.indice__pannello')].filter(p => getComputedStyle(p).visibility === 'visible').length")
        assert visible == 1

        _go(page, live_server, f"mappa-{lang}")
        page.wait_for_selector(".mappa[data-sel]")
        nodes = page.locator(".mappa__tasto")
        assert page.locator(".mappa__nodi").get_attribute("role") == "tablist"
        assert nodes.nth(0).get_attribute("aria-selected") == "true", "the hub first"
        nodes.nth(0).focus()
        page.keyboard.press("ArrowDown")
        assert nodes.nth(1).get_attribute("aria-selected") == "true"
        assert page.evaluate("document.querySelector('.mappa__raggio[data-on]') !== null"), "its spoke drawn"
        page.keyboard.press("Escape")
        assert nodes.nth(0).get_attribute("aria-selected") == "true", "Escape returns to the hub"
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("name", ["indice", "mappa", "tracciato", "racconto", "filo"])
def test_without_script_every_panel_and_entry_stands_in_reading_order(browser, live_server, name):
    pages = {f"{name}-fr": fx.page(name, "fr")}
    ctx, page = _open(browser, live_server, pages, 1440, java_script_enabled=False)
    try:
        _go(page, live_server, f"{name}-fr")
        entries = ".indice__pannello, .mappa__pannello, .tracciato__carta, .racconto__passo, .filo__tappa"
        assert page.evaluate("s => document.querySelectorAll(s).length", entries) > 1, name
        hidden = page.evaluate("""s => [...document.querySelectorAll(s)].filter(el => getComputedStyle(el).visibility !== 'visible'
            || getComputedStyle(el).display === 'none').length""", entries)
        assert hidden == 0, name
        tops = page.evaluate("s => [...document.querySelectorAll(s)].map(el => el.getBoundingClientRect().top)",
                             ".indice__pannello, .mappa__pannello, .racconto__passo, .filo__tappa")
        assert tops == sorted(tops), (name, "reading order")
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_protection_keeps_its_locked_text_whole(browser, live_server, lang):
    pages = {f"protezione-{lang}": fx.page("protezione", lang)}
    ctx, page = _open(browser, live_server, pages, 390)
    try:
        _go(page, live_server, f"protezione-{lang}")
        text = page.evaluate("document.querySelector('.protezione__testo').textContent")
        assert text == locked_content.get("p3.antifraud.body", lang)[0]
        assert page.evaluate("document.querySelectorAll('.protezione__testo .ls').length") == 4
        assert page.evaluate("getComputedStyle(document.querySelector('.protezione__testo')).visibility") == "visible"
    finally:
        ctx.close()


# ---------------------------------------------------------------------------------------------- round 1 (v522-s-improve1)

#: what a list or a tablist owns, as an accessibility tree reads it: its children, through the elements that stepped out
#: of the tree (role none or presentation) and the plain wrappers, up to the first element with a role of its own
OWNED = """sel => [...document.querySelectorAll(sel)].map(list => {
  const owned = [];
  const implicit = el => el.tagName === 'LI' ? 'listitem' : el.tagName === 'A' && el.hasAttribute('href') ? 'link'
    : el.tagName === 'BUTTON' ? 'button' : '';
  const walk = el => { for (const c of el.children) {
    const r = c.getAttribute('role');
    if (r === 'none' || r === 'presentation') { walk(c); continue; }
    const role = r || implicit(c);
    if (role) owned.push(role); else walk(c);
  } };
  walk(list);
  const root = list.closest('[data-sec-js]');
  return {role: list.getAttribute('role'), owned: [...new Set(owned)],
          apri: root.querySelectorAll('.indice__apri').length,
          expanded: [...root.querySelectorAll('.indice__apri')].every(b => b.hasAttribute('aria-expanded'))};
})"""


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_tablist_owns_its_tabs_and_a_list_its_items(browser, live_server, lang):
    pages = {f"{name}-{lang}": fx.page(name, lang) for name in ("indice", "explorer", "mappa")}
    for width in (1440, 390):
        ctx, page = _open(browser, live_server, pages, width)
        try:
            for key in pages:
                _go(page, live_server, key)
                page.wait_for_timeout(300)
                for found in page.evaluate(OWNED, ".indice__lista, .mappa__nodi"):
                    if found["role"] == "tablist":
                        assert found["owned"] == ["tab"], (key, width, found)
                        assert found["apri"] == 0, (key, width, "a tab's panel heading is a heading, never a button")
                    else:
                        assert found["role"] == "list" and found["owned"] == ["listitem"], (key, width, found)
                        assert found["expanded"], (key, width, "a disclosure button says whether it is open")
        finally:
            ctx.close()


#: every connector of «la linea V2» that is drawn: its scale, its clip, the animations driving it — at rest all three
#: must be the drawn route's (scale 1, no clip, none)
CONNECTORS = """() => [...document.querySelectorAll('.linea--large > li')].flatMap((step, i) => [
    [step, '::before'], [step.querySelector('.linea__num'), '::after'], [step.querySelector('.linea__segno'), '::after']]
  .filter(([el, pseudo]) => el && !['none', 'normal'].includes(getComputedStyle(el, pseudo).content)
    && getComputedStyle(el, pseudo).display !== 'none')
  .map(([el, pseudo]) => { const cs = getComputedStyle(el, pseudo);
    return {i: i + 1, pseudo, scale: cs.scale, clip: cs.clipPath, w: parseFloat(cs.width) || 0, h: parseFloat(cs.height) || 0,
      driven: document.getAnimations().filter(a => a.effect && a.effect.target === el && a.effect.pseudoElement === pseudo).length}; }))"""


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_la_linea_stands_drawn_at_rest_in_view_at_load_and_from_the_keyboard(browser, live_server, lang):
    pages = {f"{name}-{lang}": fx.page(name, lang) for name in ("linea", "linea-how")}
    for width, keyboard in ((390, False), (768, False), (1024, False), (768, True), (1440, True)):
        ctx, page = _open(browser, live_server, pages, width)
        try:
            for key in pages:
                _go(page, live_server, key)
                if keyboard:
                    page.keyboard.press("Tab")
                page.wait_for_timeout(1200)
                assert page.evaluate("document.querySelector('[data-sec-state]') === null"), (key, "in view: never waits")
                parts = page.evaluate(CONNECTORS)
                steps = page.evaluate("document.querySelectorAll('.linea--large > li').length")
                assert len(parts) >= steps - 1, (key, width, "a connector between every two stations")
                for part in parts:
                    assert part["scale"] in ("none", "1") and part["clip"] == "none" and not part["driven"], (key, width, keyboard, part)
                    assert part["w"] > 0 and part["h"] > 0, (key, width, part)
        finally:
            ctx.close()


FLOW = """() => {
  const svg = document.querySelector('.flow__svg'), box = svg.getBoundingClientRect();
  const nodes = [...document.querySelectorAll('[data-flow-node]')].map(n => { const r = n.getBoundingClientRect();
    return [r.left + r.width / 2 - box.left, r.top + r.height / 2 - box.top]; });
  const path = svg.querySelector('.flow__path'), d = path.getAttribute('d') || '';
  const pts = (d.match(/-?[0-9.]+/g) || []).map(Number);
  return {inList: !!svg.closest('ol, ul'), wrapper: svg.parentElement.hasAttribute('data-flow'),
          curves: (d.match(/C/g) || []).length, first: pts.slice(0, 2), last: pts.slice(-2), nodes,
          length: path.getTotalLength()};
}"""


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_measured_flow_runs_one_curve_through_every_node(browser, live_server, lang):
    pages = {f"flusso-{lang}": fx.page("flusso", lang)}
    for width in (1440, 768, 390):
        ctx, page = _open(browser, live_server, pages, width)
        try:
            _go(page, live_server, f"flusso-{lang}")
            page.wait_for_selector(".flow__svg .flow__path[d]", state="attached")
            flow = page.evaluate(FLOW)
            assert flow["wrapper"] and not flow["inList"], (width, "the overlay stands in its wrapper, never in the list")
            assert flow["curves"] == len(flow["nodes"]) - 1 and flow["length"] > 0, (width, flow)
            for got, want in ((flow["first"], flow["nodes"][0]), (flow["last"], flow["nodes"][-1])):
                assert abs(got[0] - want[0]) <= 1.5 and abs(got[1] - want[1]) <= 1.5, (width, got, want)
            if width >= 768:
                first, last = flow["nodes"][0][0], flow["nodes"][-1][0]
                assert (first > last) if lang == "ar" else (first < last), (width, "the route runs in the reading direction")
        finally:
            ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_passage_snaps_inside_itself_and_brings_a_focused_plate_into_its_rail(browser, live_server, lang):
    pages = {f"passaggio-{lang}": fx.page("passaggio", lang)}
    ctx, page = _open(browser, live_server, pages, 390)
    try:
        _go(page, live_server, f"passaggio-{lang}")
        rail = page.evaluate("""() => { const r = document.querySelector('.passaggio'), cs = getComputedStyle(r);
            const plate = r.querySelector('.passaggio__lastra').getBoundingClientRect().width;
            const inner = r.clientWidth - parseFloat(cs.paddingInlineStart) - parseFloat(cs.paddingInlineEnd);
            return {snap: cs.scrollSnapType, over: cs.overflowX, share: plate / inner, scrolls: r.scrollWidth > r.clientWidth,
                    rule: getComputedStyle(document.querySelector('.passaggio-rail'), '::after').animationName}; }""")
        assert "x" in rail["snap"] and "mandatory" in rail["snap"] and rail["over"] == "auto" and rail["scrolls"], rail
        assert abs(rail["share"] - 0.78) < 0.02, rail
        assert rail["rule"] == "sez-rail", "the position rule follows the rail's own scroll"
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
        for _plate in range(4):
            page.keyboard.press("Tab")
            page.wait_for_timeout(450)
            inside = page.evaluate("""() => { const a = document.activeElement, r = document.querySelector('.passaggio').getBoundingClientRect();
                const p = a.closest('.passaggio__lastra').getBoundingClientRect(); return p.left >= r.left - 1 && p.right <= r.right + 1; }""")
            assert inside, (lang, "a focused plate stands inside its rail")
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("name", ["strato", "approdo"])
def test_a_band_that_declares_its_light_sweeps_it_once_as_it_enters(browser, live_server, name):
    pages = {f"{name}-fr": fx.page(name, "fr", spacer=True)}
    sel = f'[data-sec="{name}"]'
    ctx, page = _open(browser, live_server, pages, 1440)
    try:
        _go(page, live_server, f"{name}-fr")
        assert page.evaluate("s => document.querySelector(s).dataset.verb", sel) == "light"
        page.evaluate("s => document.querySelector(s).scrollIntoView({block: 'center'})", sel)
        page.wait_for_function("s => document.querySelector(s).dataset.secState === 'in'", arg=sel)
        sweeps = page.evaluate("""s => { const band = document.querySelector(s); return band.getAnimations({subtree: true})
            .filter(a => a.animationName === 'sez-sweep' && a.effect.target === band && a.effect.pseudoElement === '::before').length; }""", sel)
        assert sweeps == 1, (name, "one light sweeps the band as it enters")
        page.wait_for_timeout(2600)
        left = page.evaluate("""s => document.querySelector(s).getAnimations({subtree: true})
            .filter(a => a.animationName === 'sez-sweep').length""", sel)
        assert left == 0, (name, "once: a finished sweep leaves getAnimations()")
    finally:
        ctx.close()
