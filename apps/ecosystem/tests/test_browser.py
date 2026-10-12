"""
Browser tests (Playwright, Chromium) of the four ecosystem spaces.

Checks that need a real layout engine: no horizontal overflow at 390/800/1440 in LTR and RTL, the
prescribed eight-step diagram laid out vertically on a phone and on one row on a desktop (mirrored
in RTL), labels never clipped, nothing left hidden by the entrance motion (with JavaScript, without
JavaScript and with a reduced-motion preference), no request outside the site and no CSP violation.
Skipped when Chromium is not installed.

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
STEP = ".pilot-diagram .timeline__item"
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
    # Measure once the entrance motion is over: a step that is still sliding in reports a moving box.
    page.locator(".pilot-diagram__figure").scroll_into_view_if_needed()
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
            # A photograph ships only with its whole caption apparatus — place, date, a factual
            # sentence, a credit — and no asset in the inherited library carries one. So these
            # pages carry themselves on type, which is the test art direction A set for itself.
            # See tests/compliance/test_figure_caption.py for the rule itself.
            figures = page.locator("figure").count()
            captions = page.locator("figcaption").count()
            assert figures == captions, (path, f"{figures} figure for {captions} figcaption")
            hidden = page.evaluate(
                "Array.from(document.querySelectorAll('.reveal'))"
                ".filter(e => getComputedStyle(e).opacity === '0').length"
            )
            assert hidden == 0, (lang, viewport, path)
            # No block of the main column is wider than the viewport (long prescribed button labels).
            too_wide = page.evaluate(
                "Array.from(document.querySelectorAll('main .btn, main .cta-panel, main .notice, main .timeline'))"
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
            "Array.from(document.querySelectorAll('.pilot-diagram .timeline__label'))"
            ".filter(e => e.scrollWidth > e.clientWidth + 1).length"
        )
        assert clipped == 0
        assert page.evaluate("getComputedStyle(document.querySelector('.pilot-diagram .timeline__label')).hyphens") in (
            "manual",
            "none",
        )
        numerals = page.evaluate(
            "Array.from(document.querySelectorAll('.pilot-diagram .timeline__marker'))"
            ".map(e => getComputedStyle(e, '::before').content)"
        )
        assert numerals[0] in ("counter(timeline, decimal-leading-zero)", '"01"'), numerals[0]
    finally:
        context.close()


def test_pilot_steps_settle_with_motion_and_are_never_left_hidden(browser, live_server, phase3_live):
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(f"{live_server.url}/fr/{PILOT}", wait_until="networkidle")
        page.locator(".pilot-diagram__figure").scroll_into_view_if_needed()
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
            "main .reveal, main .timeline__item, main .ecosystem-enum__item, main .cta-panel",
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
        assert any("/static/css/dist/ecosystem/ecosystem.css" in u for u in requests)
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
        for selector in (
            "h1.page-header__title[lang='fr']",
            "p.page-header__lead[lang='fr']",
            "blockquote[lang='fr']",
            "[data-block='recruitment-guarantee'] .notice[lang='fr']",
        ):
            assert _direction(page, selector) == "ltr", selector
        assert _direction(page, ".ecosystem-layout") == "rtl"
        assert _direction(page, ".local-nav") == "rtl"
        # The closing question mark of the prescribed title sits AFTER the last word, not before it.
        question_mark_follows = page.evaluate(
            """() => {
              const node = document.querySelector("h1.page-header__title").firstChild;
              const text = node.textContent;
              const at = text.lastIndexOf("?");
              const rect = (i) => { const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1);
                                    return r.getBoundingClientRect(); };
              let letter = at - 1;
              while (letter > 0 && !text[letter].trim()) letter -= 1;
              const mark = rect(at), last = rect(letter);
              return Math.abs(mark.top - last.top) > 4 || mark.left >= last.right - 1;
            }"""
        )
        assert question_mark_follows

        page.goto(f"{live_server.url}/ar/institutions/", wait_until="networkidle")
        assert _direction(page, ".page-header__lead span[lang='fr']") == "ltr"
        assert _direction(page, "h1.page-header__title") == "rtl", "the translated title follows the page"
        assert _direction(page, "ul.ecosystem-enum") == "rtl", "lists stay mirrored"

        page.goto(f"{live_server.url}/ar/{PILOT}", wait_until="networkidle")
        assert _direction(page, "h1.page-header__title[lang='fr']") == "ltr"
        assert _direction(page, ".pilot-diagram ol.timeline") == "rtl", "the diagram stays mirrored"
    finally:
        context.close()
