"""
The section library's follow-up in Chromium (design V5.22, SECTION_SYSTEM_V2 §2, §4, §5.3; lane S's follow-up, label
v522-s2-build). Fixtures, never a page of the site (tests/frontend/sezioni_fixtures.py's machinery, served by
Playwright's route), for what this follow-up changed in the library:

* lane P2's merge conditions on lane S's modules (QA_ROUND3 MC-1…MC-3), proved on the library's own fixtures:
  - «l'indice» (explorer): a permalink on a phone lands on its OPEN answer, and a hash changed within the page — a link
    to another answer, the address bar — selects (≥ 64 rem) or opens (< 64 rem) the answer it names (W1-C's
    same-document step, restored here for the library);
  - «la spia» over parts laid out as a grid: a followed letter lights itself, and a read through lights every row;
  - «la mappa»: a chosen actor's entry that stands below the screen comes into view;
* the red guards' product fixes: the route board's light waits beyond the rail's start and runs to its end in Arabic
  (the RTL twin); the hemicycle pairs its seats and phrases through its own attribute, never Lume's L3 seat;
* lane H's requests: an index glyph is never squeezed below its 20 px; «la protezione»'s French title is one
  left-to-right box on an Arabic page, on the body's edge; the curated plate's byline sets its space before the colon
  in French only (V5.24 §2: the stock frame's credit no longer exists; the byline renders only for a licence that
  demands it — a CC BY asset here); the keyboard's tier 0 is filed under the library's own classes (the tile's glyph
  and rule, the disc, the key,
  the mosaic's rule and doors) and the stroke verb's carriers pass the draw to their shapes by inheritance;
* the disclosure's height (static/css/v5/motion.css, the one INP rule): from the keyboard it opens and closes at once,
  for a pointer it still interpolates.
"""

from __future__ import annotations

import os

import pytest
from django.template import engines
from django.templatetags.static import static
from django.utils import translation

from tests.frontend import sezioni_fixtures as fx

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser]

ROUTE = "**/__fixture__/**"
LETTERS = ("A", "C", "D", "L", "N", "P", "R", "V")

#: a scroll-spy over parts laid out three to a row, as the glossary's register is (lane P2's QA_ROUND2 M3)
SPIA_GRIGLIA = """<div class="fx-spia" data-sec-js="spia">
  <nav class="filo__rail" aria-label="Lettres"><ol class="filo__indice">{% for l in letters %}<li><a class="filo__voce" href="#fx-l-{{ l }}">{{ l }}</a></li>{% endfor %}</ol></nav>
  <div class="fx-spia__griglia" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px">{% for l in letters %}<section id="fx-l-{{ l }}" style="min-block-size:{% cycle 420 300 360 %}px;border:1px solid"><h3>{{ l }}</h3></section>{% endfor %}</div>
  <div class="fx-spia__seguito" style="min-block-size:100vh"></div>
</div>"""
#: a stroke verb on its CARRIER (an svg, a g, a span round a mark): the shapes inside draw with it (lane P2's drawings)
TRATTO = """<svg class="fx-tratto" viewBox="0 0 120 40" width="240" height="80" data-verb="stroke" aria-hidden="true" focusable="false" fill="none" stroke="currentColor">
  <g><path pathLength="1" d="M4 36C30 4 90 4 116 36"/><circle pathLength="1" cx="60" cy="20" r="8"/></g></svg>"""
#: the console's and the reading pages' disclosure (main.css: tabs.css + motion.css's height)
ACCORDION = """<div class="accordion">{% for q in questions %}<details class="accordion__item" id="fx-acc-{{ forloop.counter }}"><summary class="accordion__summary">{{ q }}</summary><div class="accordion__panel"><p>{{ q }} — une réponse de plusieurs lignes, pour que la hauteur se voie : la plateforme oriente, elle ne décide pas ; les autorités compétentes décident.</p><p><a href="#">Un lien dans la réponse</a></p></div></details>{% endfor %}</div>"""
EXTRA = {
    "spia-griglia": (SPIA_GRIGLIA, "Lettres"),
    "tratto": (TRATTO, "Un tracé"),
    "accordion": (ACCORDION, "Questions"),
    "emiciclo-frase": (
        '{% include "components/sezioni/mappa.html" with layout="arc" nodes=seats sentence=frase sentence_lang=frase_lang %}',
        "Destinataires",
    ),
}


def _extra(name: str, lang: str, spacer: bool = False) -> str:
    """A fixture of this module, in the library's bare page (sezioni_fixtures' head and foot, its section wrapper)."""
    from ecosystem import services

    with translation.override(lang):
        ctx = {"letters": LETTERS, "questions": ("Qui décide ?", "Combien de temps ?", "Est-ce garanti ?")}
        if name == "emiciclo-frase":
            recipients = services.enumeration("p3.institutions.recipients", lang)
            ctx.update(
                seats=services.recipient_seats(recipients),
                frase=services.recipients_sentence(recipients),
                frase_lang=recipients.source.lang_attr,
            )
        source, title = EXTRA[name]
        body = engines["django"].from_string(source).render(ctx)
        section = fx._section(name, body, "night" if name == "emiciclo-frase" else "paper", title, lang=lang)
        head = fx.HEAD.format(
            lang=lang,
            dir="rtl" if lang == "ar" else "ltr",
            name=name,
            main=static("css/dist/main.css"),
            reveal=static("css/dist/core/reveal.css"),
            fronte=static("css/dist/pages/css/fronte.css"),
            partials=f'<link rel="stylesheet" href="{static("css/dist/core/sezioni.css")}">',
            head_js=static("js/head.js"),
            rtl="is-rtl" if lang == "ar" else "",
            gap="Une première bande, pour que la section commence sous la ligne de flottaison." * (60 if spacer else 6),
        )
        return head + section + fx.FOOT.format(rise=static("js/dist/rise.js"))


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


def _open(browser, pages: dict, width: int, height: int = 900, **context):
    ctx = browser.new_context(viewport={"width": width, "height": height}, **context)
    page = ctx.new_page()
    page.route(
        ROUTE,
        lambda route: route.fulfill(
            body=pages[route.request.url.rsplit("/", 1)[1].split("#", 1)[0]], content_type="text/html; charset=utf-8"
        ),
    )
    return ctx, page


def _go(page, live_server, key: str, hash_: str = ""):
    page.goto(f"{live_server.url}/__fixture__/{key}{hash_}", wait_until="load")
    page.wait_for_timeout(300)


# ---------------------------------------------------------------------------------------------- MC-1 · «l'indice»

EXPLORER = """() => ({
  mode: document.querySelector('.indice').dataset.mode,
  selected: [...document.querySelectorAll('.indice__voce[aria-selected="true"]')].map((a) => a.hash),
  expanded: [...document.querySelectorAll('.indice__apri')].map((b) => b.getAttribute('aria-expanded')),
  shown: [...document.querySelectorAll('.indice__pannello')].filter((p) => getComputedStyle(p).visibility !== 'hidden'
    && p.querySelector('.indice__corpo').getBoundingClientRect().height > 0).map((p) => '#' + p.id),
})"""


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_an_explorer_permalink_lands_on_its_open_answer_and_follows_the_address(browser, live_server, lang):
    """MC-1 (lane P2's QA_ROUND3; indice.js.patch): on a phone the answer the address names is open at arrival — the
    others folded —, and a hash changed within the page selects (≥ 64 rem) or opens (< 64 rem) its answer, its heading
    brought into view on a phone; W1-C's same-document step, for the library."""
    key = f"explorer-{lang}"
    pages = {key: fx.page("explorer", lang)}
    ids = [item["id"] for item in fx._context(lang)["faq_items"]]
    for width, height in ((390, 844), (1440, 900)):
        ctx, page = _open(browser, pages, width, height)
        try:
            _go(page, live_server, key, f"#{ids[2]}")
            page.wait_for_selector(".indice[data-mode]")
            state = page.evaluate(EXPLORER)
            if width < 1024:
                assert state["mode"] == "disclosure", state
                assert state["shown"] == [f"#{ids[2]}"] and state["expanded"].count("true") == 1, (lang, width, state)
            else:
                assert state["mode"] == "tabs" and state["selected"] == [f"#{ids[2]}"], (lang, width, state)
                assert state["shown"] == [f"#{ids[2]}"], (lang, width, state)
            # the same document: a link to another answer, the address bar (a fresh `hashchange`, no new load)
            page.evaluate("(id) => { location.hash = '#' + id; }", ids[4])
            page.wait_for_function("(id) => document.getElementById(id).hasAttribute('data-on')", arg=ids[4])
            page.wait_for_timeout(700)
            state = page.evaluate(EXPLORER)
            assert state["shown"] == [f"#{ids[4]}"], (lang, width, "the explorer follows the address", state)
            if width >= 1024:
                assert state["selected"] == [f"#{ids[4]}"], (lang, width, state)
            else:
                box = page.evaluate(
                    "(id) => { const r = document.getElementById(id + '-title').getBoundingClientRect(); return [r.top, r.bottom]; }",
                    ids[4],
                )
                assert 0 <= box[0] and box[1] <= height, (lang, width, "its heading in view", box)
            page.goto(f"{live_server.url}/__fixture__/{key}#{ids[1]}", wait_until="load")
            page.wait_for_function("(id) => document.getElementById(id).hasAttribute('data-on')", arg=ids[1])
            assert page.evaluate(EXPLORER)["shown"] == [f"#{ids[1]}"], (lang, width, "W1-C's same-document step")
        finally:
            ctx.close()


# ---------------------------------------------------------------------------------------------- MC-2 · «la spia»


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_spy_over_a_grid_lights_the_letter_followed_and_every_row_read(browser, live_server, lang):
    """MC-2 (lane P2's QA_ROUND3; spia.js.patch): parts that share a row cross the band together — one stop, marked from
    its first (aria-current), the row's others flagged; a followed link is current at once and stays so through the
    scroll it started; a read through the page lights every row."""
    key = f"spia-griglia-{lang}"
    pages = {key: _extra("spia-griglia", lang)}
    lit = """() => [...document.querySelectorAll('.filo__voce')].filter((a) => a.hasAttribute('aria-current')
        || a.hasAttribute('data-spia-con')).map((a) => a.hash)"""
    for width, height in ((1440, 900), (1024, 768)):
        ctx, page = _open(browser, pages, width, height)
        try:
            _go(page, live_server, key)
            links = page.locator(".filo__voce")
            for i in range(links.count()):
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(250)
                href = links.nth(i).get_attribute("href")
                links.nth(i).click()
                page.wait_for_timeout(1200)
                current = page.evaluate("() => document.querySelector('.filo__voce[aria-current]')?.hash")
                assert current == href, (lang, width, href, current)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            seen = set()
            for _ in range(40):
                page.mouse.wheel(0, 120)
                page.wait_for_timeout(80)
                seen |= set(page.evaluate(lit))
            assert seen == {f"#fx-l-{letter}" for letter in LETTERS}, (lang, width, sorted(seen))
        finally:
            ctx.close()


# ---------------------------------------------------------------------------------------------- MC-3 · «la mappa»


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_chosen_actor_s_entry_below_the_screen_comes_into_view(browser, live_server, lang):
    """MC-3 (lane P2's QA_ROUND3 m1; mappa.js.patch): below 64 rem the entries stand under the ring; a node chosen while
    its entry is below the screen brings the entry into view (at once from the keyboard and under reduced motion)."""
    key = f"mappa-{lang}"
    pages = {key: fx.page("mappa", lang)}
    ctx, page = _open(browser, pages, 768, 560)
    try:
        _go(page, live_server, key)
        page.wait_for_selector(".mappa[data-sel]")
        page.evaluate("document.querySelector('.mappa__anello').scrollIntoView({block: 'start'})")
        page.wait_for_timeout(300)
        node = page.locator(".mappa__tasto").nth(3)
        target = node.get_attribute("href")
        below = page.evaluate("(sel) => document.querySelector(sel).getBoundingClientRect().top > innerHeight", target)
        node.click()
        page.wait_for_timeout(900)
        box = page.evaluate(
            "(sel) => { const r = document.querySelector(sel).getBoundingClientRect(); return [r.top, r.bottom]; }",
            target,
        )
        assert below, (lang, "the case: the entry stood below the screen")
        assert box[0] < 560 and box[1] > 0, (lang, "the chosen entry is in view", box)
    finally:
        ctx.close()


# ---------------------------------------------------------------------------------------------- the red guards' fixes


@pytest.mark.django_db(transaction=True)
def test_the_route_board_s_light_waits_beyond_the_rail_s_start_and_runs_in_the_page_s_direction(browser, live_server):
    """DL54-182 item 10 a (tests/i18n/test_rtl_static.py's twin): right to left, the light's box stands at the rail's
    start, its right end — it waits beyond it (never a glow inside the rail at rest) and runs to the rail's end."""
    pages = {f"tracciato-{lang}": fx.page("tracciato", lang) for lang in ("fr", "ar")}
    ctx, page = _open(browser, pages, 1440)
    try:
        for lang, rest, run in (("fr", "-110%", "sez-run"), ("ar", "110%", "sez-run-rtl")):
            _go(page, live_server, f"tracciato-{lang}")
            light = page.evaluate("""() => { const rail = document.querySelector('.tracciato__linea');
                const cs = getComputedStyle(rail, '::after'); const r = rail.getBoundingClientRect();
                const w = parseFloat(cs.width), tx = parseFloat(cs.translate) / 100 * w;
                const start = getComputedStyle(rail).direction === 'rtl' ? r.width - w : 0;
                return {translate: cs.translate, from: start + tx, to: start + tx + w, rail: r.width}; }""")
            assert light["translate"].startswith(rest), (lang, light)
            assert light["to"] <= 0.5 or light["from"] >= light["rail"] - 0.5, (lang, "outside the rail at rest", light)
            page.locator(".tracciato__chip").nth(1).click()
            page.wait_for_timeout(60)
            names = page.evaluate("""() => document.getAnimations().filter((a) => a.effect && a.effect.pseudoElement === '::after'
                && a.effect.target.classList.contains('tracciato__linea')).map((a) => a.animationName)""")
            assert names and set(names) == {run}, (lang, names)
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_hemicycle_pairs_its_seats_and_phrases_through_its_own_attribute(browser, live_server, lang):
    """DL54-182 item 10 b (tests/frontend/test_loader_rules.py's L3 guard): the locked sentence's items carry `data-seggio`,
    the pattern's own — nothing of the section carries Lume's L3 `data-seat`. FINAL MICRO-PASS §6 B4 (V5.20; was «a
    phrase under the hand lights its seat, a seat its phrase»): the six seat tiles left, so no seat is drawn and nothing
    lights; the sentence is one typographic annotation — its six recipients in the primary ink, one ink for all six,
    its joins and its head apart."""
    key = f"emiciclo-frase-{lang}"
    pages = {key: _extra("emiciclo-frase", lang)}
    ctx, page = _open(browser, pages, 1440)
    try:
        _go(page, live_server, key)
        counts = page.evaluate("""() => ({seat: document.querySelectorAll('[data-seat]').length,
            seats: document.querySelectorAll('.emiciclo__seggio, .emiciclo__seggi, .emiciclo .sez-disc').length,
            phrases: document.querySelectorAll('.emiciclo__voce[data-seggio]').length})""")
        assert counts == {"seat": 0, "seats": 0, "phrases": 6}, (lang, counts)
        ink = "(sel) => getComputedStyle(document.querySelector(sel)).color"
        inks = {page.evaluate(ink, f'.emiciclo__voce[data-seggio="{n}"]') for n in range(1, 7)}
        assert len(inks) == 1, (lang, "one ink for the six recipients", inks)
        assert inks != {page.evaluate(ink, ".emiciclo__frase")}, (lang, "the joins apart from the recipients")
        rest = page.evaluate(ink, '.emiciclo__voce[data-seggio="3"]')
        page.hover('.emiciclo__voce[data-seggio="3"]')
        page.wait_for_timeout(100)
        assert page.evaluate(ink, '.emiciclo__voce[data-seggio="3"]') == rest, (lang, "a phrase under the hand stays")
    finally:
        ctx.close()


# ---------------------------------------------------------------------------------------------- lane H's requests


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_an_index_glyph_keeps_its_twenty_pixels_whatever_its_title_wraps_to(browser, live_server, lang):
    """Lane H's QA_ROUND3 m3: in the tab rows (1024–1280) a title that wraps once squeezed its glyph to 15.5 px; the
    glyph is never a flex item that shrinks (§4.2: 20 px in an index row)."""
    pages = {f"indice-{lang}": fx.page("indice", lang)}
    for width in (1024, 1280, 1440):
        ctx, page = _open(browser, pages, width)
        try:
            _go(page, live_server, f"indice-{lang}")
            page.wait_for_selector(".indice[data-mode='tabs']")
            rows = page.evaluate("""() => [...document.querySelectorAll('.indice__voce')].map((a) => {
                const g = a.querySelector('.indice__glifo').getBoundingClientRect(), n = a.querySelector('.indice__nome');
                return {w: g.width, lines: Math.round(n.getBoundingClientRect().height / parseFloat(getComputedStyle(n).lineHeight))}; })""")
            assert all(abs(row["w"] - 20) < 0.5 for row in rows), (lang, width, rows)
            if width == 1024:
                assert any(row["lines"] > 1 for row in rows), (lang, "the case: a title that wraps", rows)
        finally:
            ctx.close()


@pytest.mark.django_db(transaction=True)
def test_the_protection_s_french_title_is_one_left_to_right_box_on_the_body_s_edge(browser, live_server):
    """Lane H's QA_ROUND3 m5 (NOTES §12.5 item 5): on an Arabic page the French title stood at the right while its French
    body ran flush left in its box; the title now carries its language, so the two share one start."""
    pages = {"protezione-ar": fx.page("protezione", "ar"), "protezione-fr": fx.page("protezione", "fr")}
    for width in (1440, 390):
        ctx, page = _open(browser, pages, width)
        try:
            for key in pages:
                _go(page, live_server, key)
                edges = page.evaluate("""() => { const range = (el) => { const r = document.createRange(); r.selectNodeContents(el);
                    return r.getClientRects()[0]; };
                    const t = document.querySelector('.protezione__titolo'), b = document.querySelector('.protezione__testo .ls-1');
                    return {dir: getComputedStyle(t).direction, title: range(t).left, body: range(b).left,
                            titleEnd: range(t).right,
                            bodyEnd: document.querySelector('.protezione__testo').getBoundingClientRect().right}; }""")
                if key == "protezione-ar":
                    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): on /ar/ the
                    # title is its provisional Arabic rendering, right to left, and starts on the body's own edge (the
                    # right one); the body is the Arabic pointer line on a product page, the source French here
                    assert edges["dir"] == "rtl", (key, width, edges)
                    assert abs(edges["titleEnd"] - edges["bodyEnd"]) <= 1, (key, width, "one start", edges)
                    continue
                assert edges["dir"] == "ltr", (key, width, edges)
                assert abs(edges["title"] - edges["body"]) <= 1, (key, width, "one start", edges)
        finally:
            ctx.close()


def _plate_page(lang: str) -> str:
    """The frontispiece's curated plate (pages/partials/_ingresso.html) in the library's bare page, drawn from a CC BY
    asset — the one licence whose byline renders (V5.24 §2, cms.MediaAsset.attribution_required) — built as
    tests/frontend/test_frontispiece_v515_c.py builds its curated photograph, through pages.services."""
    import datetime as dt

    from cms.models import MediaAsset, MediaLicense
    from pages import services

    asset = MediaAsset(
        title="Tavola",
        file="media/2026/09/tavola.jpg",
        alt_fr="Une table de travail",
        caption_fr="Une séance de travail.",
        caption_place="Rovigo",
        caption_date=dt.date(2026, 10, 2),
        credit="Archive",
        license=MediaLicense.CC_BY,
    )
    photo = services.photo_from_asset(asset, lang)
    assert photo is not None and photo.attribution_required
    with translation.override(lang):
        body = (
            engines["django"]
            .from_string(
                '{% include "pages/partials/_ingresso.html" with title=title photo=photo fronte_linked=True only %}'
            )
            .render({"title": "Un titre", "photo": photo})
        )
        head = fx.HEAD.format(
            lang=lang,
            dir="rtl" if lang == "ar" else "ltr",
            name="plate",
            main=static("css/dist/main.css"),
            reveal=static("css/dist/core/reveal.css"),
            fronte=static("css/dist/pages/css/fronte.css"),
            partials=f'<link rel="stylesheet" href="{static("css/dist/core/sezioni.css")}">',
            head_js=static("js/head.js"),
            rtl="is-rtl" if lang == "ar" else "",
            gap="Une première bande." * 6,
        )
        return head + body + fx.FOOT.format(rise=static("js/dist/rise.js"))


@pytest.mark.django_db(transaction=True)
def test_the_plate_s_byline_sets_its_space_before_the_colon_in_french_only(browser, live_server):
    """Lane H's QA_ROUND3 m7 (an observation for S): «Foto : …», «Photo : …» on it/en; the colon takes its space in
    French only — there a no-break one, never at the start of a line. V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6; V5.20):
    the stock frame's credit no longer exists, so the same invariant is held on the markup that still prints a byline
    — the frontispiece's curated plate, for an asset whose licence demands the credit (CC BY)."""
    pages = {f"plate-{lang}": _plate_page(lang) for lang in ("fr", "it", "en", "ar")}
    ctx, page = _open(browser, pages, 1440)
    try:
        for lang, word in (("fr", "Photo : "), ("it", "Foto: "), ("en", "Photo: "), ("ar", ": ")):
            _go(page, live_server, f"plate-{lang}")
            assert page.evaluate("document.querySelectorAll('figure[data-slot] figcaption, .foto__credit').length") == 0
            caption = page.evaluate("document.querySelector('.ingresso__aside.figura figcaption').textContent")
            credit = caption.split(" — ", 1)[1]
            assert word in credit and " :" not in credit.replace(" :", ""), (lang, credit)
            if lang != "fr":
                assert " " not in credit.split(":", 1)[0], (lang, credit)
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
def test_the_keyboard_s_tier_zero_is_filed_under_the_library_s_own_classes(browser, live_server):
    """Lane H's INP requests 1–2 (NOTES §12.5): the keyboard's final state at once — the tile's glyph and its rule, the
    disc, the mosaic's rule and its doors — through the library's classes (the tile carries --sez-t, which its glyph
    and rule read), never a rule whose subject is every icon or every element of a section."""
    pages = {"mosaico-fr": fx.page("mosaico", "fr"), "porte-fr": fx.page("porte", "fr")}
    read = """() => { const d = (el, pseudo) => el ? Math.max(...getComputedStyle(el, pseudo).transitionDuration.split(',').map(parseFloat)) : -1;
        const q = (s) => document.querySelector(s);
        return {glyph: d(q('.sez-tile .icon')), rule: d(q('.sez-tile'), '::after'), disc: d(q('.sez-disc')),
                soglia: d(q('.mosaico__soglia')), door: d(q('.mosaico--porte .mosaico__tessera'))}; }"""
    ctx, page = _open(browser, pages, 1440)
    try:
        for key, names in (("mosaico-fr", ("glyph", "soglia")), ("porte-fr", ("disc", "soglia", "door"))):
            _go(page, live_server, key)
            pointer = page.evaluate(read)
            assert all(pointer[name] > 0 for name in names), (key, "a pointer gets its feedback", pointer)
            if key == "mosaico-fr":
                # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the bare tile draws no rule, so it has nothing to transition
                rule = page.evaluate("getComputedStyle(document.querySelector('.sez-tile'), '::after').content")
                assert pointer["rule"] == 0 and rule == "none", (key, pointer, rule)
            page.keyboard.press("Tab")
            keyboard = page.evaluate(read)
            assert page.evaluate("document.documentElement.dataset.input") == "key"
            assert all(keyboard[name] == 0 for name in names), (key, keyboard)
    finally:
        ctx.close()


@pytest.mark.django_db(transaction=True)
def test_a_stroke_carrier_passes_its_draw_to_the_shapes_inside(browser, live_server):
    """Lane H's INP request 1: the stroke verb has no tag-name branch any more — a carrier (an svg, a g, a span round a
    mark: lane P2's drawings) holds the dash and runs the draw, and its shapes inherit it: held while the section waits,
    drawing as it enters, at rest after (nothing left running, no dash)."""
    pages = {"tratto-fr": _extra("tratto", "fr", spacer=True)}
    ctx, page = _open(browser, pages, 1440)
    try:
        _go(page, live_server, "tratto-fr")
        shape = "(sel) => { const cs = getComputedStyle(document.querySelector(sel)); return [cs.strokeDasharray, cs.strokeDashoffset]; }"
        assert page.evaluate("document.querySelector('[data-sec]').dataset.secState") == "wait"
        for sel in (".fx-tratto path", ".fx-tratto circle"):
            assert page.evaluate(shape, sel) == ["1px", "1px"], (sel, page.evaluate(shape, sel))
        page.evaluate("document.querySelector('[data-sec]').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(450)
        drawing = page.evaluate(shape, ".fx-tratto path")
        assert drawing[0] == "1px" and 0 <= float(drawing[1].rstrip("px")) < 1, ("drawing", drawing)
        page.wait_for_timeout(1600)
        assert page.evaluate(shape, ".fx-tratto path") == ["none", "0px"], "at rest"
        assert page.evaluate("document.querySelector('[data-sec]').getAnimations({subtree: true}).length") == 0
    finally:
        ctx.close()


HEIGHT = "(sel) => document.querySelector(sel).getBoundingClientRect().height"


@pytest.mark.django_db(transaction=True)
def test_from_the_keyboard_a_disclosure_opens_and_closes_at_once_and_a_pointer_still_sees_it_move(browser, live_server):
    """static/css/v5/motion.css's one INP rule (lane H's QA_ROUND3 M2): the keyboard's condition stands on the accordion
    — a class Blink scopes —, never on a rule that ends on ::details-content; from the keyboard the height is not
    interpolable (it opens and closes at once), and a pointer still sees it open and close (V5.12 M6)."""
    pages = {"accordion-fr": _extra("accordion", "fr")}
    ctx, page = _open(browser, pages, 1440)
    try:
        _go(page, live_server, "accordion-fr")
        assert page.evaluate("CSS.supports('selector(::details-content)')"), (
            "the pinned Chromium draws ::details-content"
        )
        closed = page.evaluate(HEIGHT, "#fx-acc-1")
        page.click("#fx-acc-1 > summary")  # a pointer: the height interpolates
        page.wait_for_timeout(40)
        mid = page.evaluate(HEIGHT, "#fx-acc-1")
        page.wait_for_timeout(700)
        opened = page.evaluate(HEIGHT, "#fx-acc-1")
        assert closed < mid < opened, ("a pointer sees it open", closed, mid, opened)
        page.focus("#fx-acc-2 > summary")
        page.keyboard.press("Enter")  # the keyboard: at once
        page.wait_for_timeout(40)
        at_once = page.evaluate(HEIGHT, "#fx-acc-2")
        page.wait_for_timeout(700)
        assert page.evaluate("document.documentElement.dataset.input") == "key"
        assert abs(at_once - page.evaluate(HEIGHT, "#fx-acc-2")) < 0.5 and at_once > closed + 20, (
            "opened at once",
            at_once,
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(40)
        assert abs(page.evaluate(HEIGHT, "#fx-acc-2") - closed) < 0.5, "closed at once"
    finally:
        ctx.close()
