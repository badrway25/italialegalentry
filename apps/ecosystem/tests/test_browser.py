"""
Browser tests (Playwright, Chromium) of the four ecosystem spaces.

Checks that need a real layout engine: no horizontal overflow at 390/800/1440 in LTR and RTL, the
prescribed eight-step sequence laid out vertically on a phone and on one row on a desktop (mirrored
in RTL), labels never clipped, nothing left hidden (with JavaScript, without JavaScript and with a
reduced-motion preference), no request outside the site and no CSP violation. Skipped when Chromium is
not installed. Design V5.4 (W3-F1): the sequence stands on «la linea», still at load (no entrance motion).

V5.22 (SECTION_SYSTEM_V2 §3.3, §3.6–§3.8 — an approved owner/product decision; lane P1; V5.20 strict rule): the
spaces' bodies are V2 sections. The sequence is «la linea V2» in PP-1 (`[data-diagram="pilot-sequence"]`, the route its
own trigger: it may wait below the fold and draw once — its stations' boxes never move, only their lines and marks),
from 80 rem one stepped row; the recruitment answer is EN-4's split paragraph, the recipients' sentence IN-1's plate,
«Pour aller plus loin» «l'approdo»'s list, and each page links its own page sheet from the family's folder (the
family's sheet bundled in it, §7.1). Every check keeps its invariant on that markup.

Gate G3 is opened through its flag only (no frozen clock: Playwright's event loop needs a running
monotonic clock), so the live server answers the Phase 3 routes at the real current date.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

VIEWPORTS = {"phone": (390, 844), "tablet": (800, 1024), "desktop": (1440, 900)}
PATHS = ("entreprises/", "institutions/", "universites-et-formation/", "projet-pilote/")
PILOT = "projet-pilote/"
STEP = '[data-diagram="pilot-sequence"] .linea__step'
ALL_STEPS_OPAQUE = (
    "() => { const items = Array.from(document.querySelectorAll('" + STEP + "'));"
    " return items.length >= 8 && items.every(e => getComputedStyle(e).opacity === '1'); }"
)
ALL_STEPS_SETTLED = (
    "() => { const items = Array.from(document.querySelectorAll('" + STEP + "'));"
    " return items.length >= 8 && items.every(e => { const s = getComputedStyle(e);"
    " return s.opacity === '1' && (s.transform === 'none' || s.transform === 'matrix(1, 0, 0, 1, 0, 0)'); }); }"
)


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
def phase3_live(seeded, set_flag):
    """Gate G3 open at the real current date, editorial rows (photographs) online."""
    from cms.models import PublicationStatus
    from ecosystem.models import EcosystemSpace

    set_flag("phase3_public", True)
    EcosystemSpace.objects.update(status=PublicationStatus.PUBLISHED, publish_at=None)


def _page(browser, width, height, **options):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **options)
    return context, context.new_page()


def _boxes(page) -> list[dict]:
    # Measure once every station is laid out (the line is still at load: nothing slides in).
    page.locator('[data-diagram="pilot-sequence"]').scroll_into_view_if_needed()
    page.wait_for_function(ALL_STEPS_SETTLED, timeout=8000)
    return page.evaluate(
        "Array.from(document.querySelectorAll('" + STEP + "')).map(e => {"
        " const r = e.getBoundingClientRect();"
        " return {left: Math.round(r.left), right: Math.round(r.right), top: Math.round(r.top)}; })"
    )


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("viewport", list(VIEWPORTS))
def test_no_horizontal_overflow_and_nothing_left_hidden(browser, live_server, phase3_live, lang, viewport):
    width, height = VIEWPORTS[viewport]
    context, page = _page(browser, width, height)
    try:
        for path in PATHS:
            page.goto(f"{live_server.url}/{lang}/{path}", wait_until="networkidle")
            scroll_w, client_w = page.evaluate(
                "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
            )
            assert scroll_w <= client_w, (lang, viewport, path, scroll_w, client_w)
            assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
            assert page.evaluate("document.documentElement.classList.contains('js')")
            assert page.locator("h1").count() == 1
            # A curated photograph ships only with its whole caption apparatus — place, date, a factual
            # sentence, a credit — and no asset in the inherited library carries one. So these
            # pages carry themselves on type, which is the test art direction A set for itself.
            # See tests/compliance/test_figure_caption.py for the rule itself. V5.24 §2 (FINAL_DELIVERY_V2.md
            # §3.2 D6; V5.20): the slot registry's stock frames carry NO caption — a plate is captioned, a frame
            # is not (the first rule as it was, the second new).
            plates = page.locator("figure.figura").count()
            plate_captions = page.locator("figure.figura figcaption").count()
            assert plates == plate_captions, (path, f"{plates} plate for {plate_captions} figcaption")
            assert page.locator("figure[data-slot] figcaption").count() == 0, (path, "a stock frame's credit")
            hidden = page.evaluate(
                "Array.from(document.querySelectorAll('.reveal'))"
                ".filter(e => getComputedStyle(e).opacity === '0').length"
            )
            assert hidden == 0, (lang, viewport, path)
            # No block of the main column is wider than the viewport (long prescribed button labels).
            too_wide = page.evaluate(
                "Array.from(document.querySelectorAll('main .btn, main .card--action, main .notice, main .linea'))"
                ".filter(e => e.getBoundingClientRect().width > document.documentElement.clientWidth).length"
            )
            assert too_wide == 0, (lang, viewport, path)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_pilot_diagram_is_vertical_on_a_phone(browser, live_server, phase3_live, lang):
    context, page = _page(browser, 390, 844)
    try:
        page.goto(f"{live_server.url}/{lang}/{PILOT}", wait_until="networkidle")
        boxes = _boxes(page)
        assert len(boxes) == 8
        tops = [b["top"] for b in boxes]
        assert tops == sorted(tops) and len(set(tops)) == 8, "one step per row, in the prescribed order"
        edge = "right" if lang == "ar" else "left"
        assert len({b[edge] for b in boxes}) == 1, "steps share the same inline start edge"
        assert all(b["left"] >= 0 and b["right"] <= 390 for b in boxes)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_pilot_diagram_is_one_mirrored_row_on_a_desktop(browser, live_server, phase3_live, lang):
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(f"{live_server.url}/{lang}/{PILOT}", wait_until="networkidle")
        boxes = _boxes(page)
        assert len(boxes) == 8
        assert len({b["top"] for b in boxes}) == 1, "eight steps on one row"
        lefts = [b["left"] for b in boxes]
        assert lefts == sorted(lefts, reverse=(lang == "ar")), "reading order follows the writing direction"
        # Prescribed labels are never clipped nor hyphenated by the layout.
        clipped = page.evaluate(
            "Array.from(document.querySelectorAll('[data-diagram=\"pilot-sequence\"] .linea__label'))"
            ".filter(e => e.scrollWidth > e.clientWidth + 1).length"
        )
        assert clipped == 0
        hyphens = page.evaluate(
            "getComputedStyle(document.querySelector('[data-diagram=\"pilot-sequence\"] .linea__label')).hyphens"
        )
        assert hyphens in ("manual", "none")
        numerals = page.evaluate(
            "Array.from(document.querySelectorAll('[data-diagram=\"pilot-sequence\"] .linea__num'))"
            ".map(e => getComputedStyle(e, '::before').content)"
        )
        assert numerals[0] in ("counter(linea, decimal-leading-zero)", '"01"'), numerals[0]
    finally:
        context.close()


def test_pilot_steps_are_visible_at_once_and_never_left_hidden(browser, live_server, phase3_live):
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(f"{live_server.url}/fr/{PILOT}", wait_until="networkidle")
        page.locator('[data-diagram="pilot-sequence"]').scroll_into_view_if_needed()
        page.wait_for_function(ALL_STEPS_OPAQUE, timeout=6000)
        # The mandatory notice right after the diagram is visible as well.
        assert page.locator("[data-notice='pilot-not-authorised'] .notice").is_visible()
    finally:
        context.close()


def test_pilot_diagram_is_static_with_reduced_motion(browser, live_server, phase3_live):
    context, page = _page(browser, 1440, 900, reduced_motion="reduce")
    try:
        page.goto(f"{live_server.url}/fr/{PILOT}", wait_until="domcontentloaded")
        assert page.evaluate(ALL_STEPS_OPAQUE), "no entrance effect when the visitor prefers reduced motion"
        durations = page.evaluate(
            "Array.from(document.querySelectorAll('" + STEP + "')).map(e => getComputedStyle(e).transitionDuration)"
        )
        assert all(d in ("0s", "0.00001s", "1e-05s") for d in durations), durations
    finally:
        context.close()


@pytest.mark.parametrize("path", PATHS)
def test_pages_work_without_javascript(browser, live_server, phase3_live, path):
    context, page = _page(browser, 390, 844, java_script_enabled=False)
    try:
        page.goto(f"{live_server.url}/fr/{path}", wait_until="load")
        assert page.locator("h1").is_visible()
        invisible = page.eval_on_selector_all(
            "main .reveal, main .linea__step, main .porta, main .card--action",
            "els => els.filter(e => getComputedStyle(e).opacity === '0' || getComputedStyle(e).visibility === 'hidden')"
            ".length",
        )
        assert invisible == 0, path
        # Every call to action is a plain link: usable without any script.
        assert page.locator("main a.btn").count() >= (0 if path == "entreprises/" else 1)
    finally:
        context.close()


def test_pages_load_nothing_outside_the_site_and_raise_no_csp_violation(browser, live_server, phase3_live):
    context, page = _page(browser, 1440, 900)
    requests: list[str] = []
    console: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
    try:
        for path in PATHS:
            page.goto(f"{live_server.url}/fr/{path}", wait_until="networkidle")
        externals = [u for u in requests if not u.startswith(live_server.url) and not u.startswith("data:")]
        assert externals == [], externals
        # each page its own page sheet from the family's folder, the family's sheet bundled in it (V5.22 §7.1)
        for sheet in ("companies", "institutions", "universities", "pilot"):
            assert any(f"/static/css/dist/ecosystem/{sheet}.css" in u for u in requests), sheet
        # No photograph is requested: an uncaptioned asset never becomes a Photo, so it reaches no
        # template. When a curated, captioned image ships, this assertion flips back to requiring
        # the responsive WebP derivative — and tests/compliance/test_figure_caption.py will say so.
        assert [u for u in requests if "/static/img/photos/" in u] == []
        violations = [m for m in console if "Content Security Policy" in m or m.startswith("pageerror")]
        assert violations == [], violations
    finally:
        context.close()


def test_companies_page_is_online_in_a_browser_with_every_gate_closed(browser, live_server, seeded):
    """Phase 1: the page renders (form replaced by the unavailable notice) and links no Phase 3 page."""
    context, page = _page(browser, 390, 844)
    try:
        response = page.goto(f"{live_server.url}/fr/entreprises/", wait_until="networkidle")
        assert response.status == 200
        assert page.locator("[data-gate='forms-closed']").count() == 1
        assert page.locator("main form").count() == 0
        assert page.locator("a[href*='projet-pilote']").count() == 0
        scroll_w, client_w = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        assert scroll_w <= client_w
        assert page.goto(f"{live_server.url}/fr/{PILOT}").status == 404
    finally:
        context.close()


def _direction(page, selector: str) -> str:
    return page.evaluate("s => getComputedStyle(document.querySelector(s)).direction", selector)


def test_french_fallback_keeps_its_punctuation_in_place_on_the_arabic_pages(browser, live_server, phase3_live):
    """
    Without an official Arabic version the prescribed texts are printed in French. In a right-to-left
    page their punctuation would be moved to the wrong end of the line ("? A-T-ELLE BESOIN"): text
    blocks keep their own writing direction while the layout, the lists and the diagram stay mirrored.
    """
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(f"{live_server.url}/ar/entreprises/", wait_until="networkidle")
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the title, the intro and
        # the quotation are compositional (C-UI) and the FAQ's answer is substantive off its page (the Arabic pointer
        # line) — every block reads Arabic, right to left, inside no French run
        for selector in (
            "h1.ingresso__title",
            "p.ingresso__lead",
            "blockquote",
            "p[data-faq]",  # the pointer line stands whole (imprese-confine__intera): it has no question to answer
        ):
            assert _direction(page, selector) == "rtl", selector
            assert page.eval_on_selector(selector, "e => e.closest('[lang=\"fr\"]') === null"), selector
        assert _direction(page, "main .chapter__inner") == "rtl", "the layout stays mirrored"
        assert page.locator("main .local-nav").count() == 0, "no side column (the doors are the chrome's)"
        # The closing question mark of the title sits AFTER the last word in reading order — on /ar/ the Arabic «؟», at
        # the left of the last letter (V5.27 R7′, the steward's amendment at the v524-ar merge)
        question_mark_follows = page.evaluate(
            """() => {
              const node = document.querySelector("h1.ingresso__title").firstChild;
              const text = node.textContent;
              const at = text.lastIndexOf("؟");
              const rect = (i) => { const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1);
                                    return r.getBoundingClientRect(); };
              let letter = at - 1;
              while (letter > 0 && !text[letter].trim()) letter -= 1;
              const mark = rect(at), last = rect(letter);
              return at > 0 && (Math.abs(mark.top - last.top) > 4 || mark.right <= last.left + 1);
            }"""
        )
        assert question_mark_follows

        page.goto(f"{live_server.url}/ar/institutions/", wait_until="networkidle")
        # V5.27 R7′ (the steward's amendment): the intro and the recipients are their provisional Arabic (C-UI)
        assert _direction(page, ".ingresso__lead") == "rtl"
        assert _direction(page, "h1.ingresso__title") == "rtl", "the translated title follows the page"
        assert _direction(page, "p.emiciclo__frase") == "rtl", "the recipients' sentence in the page's language"
        # V5.22 §3.7 IN-2: «Pour aller plus loin» is «l'approdo», a list of tiles, `ul.approdo__tessere`
        assert _direction(page, "ul.approdo__tessere") == "rtl", "lists stay mirrored"

        page.goto(f"{live_server.url}/ar/{PILOT}", wait_until="networkidle")
        # V5.27 R7′ (the steward's amendment): the pilot's title is its provisional Arabic (C-UI)
        assert _direction(page, "h1.ingresso__title") == "rtl"
        assert _direction(page, '[data-diagram="pilot-sequence"] ol.linea') == "rtl", "the sequence stays mirrored"
    finally:
        context.close()
