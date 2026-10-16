"""
RTL visual check (Playwright, Chromium) — Arabic pages against their LTR (French) equivalents.

Run with:  pytest tests/i18n/test_rtl_browser.py
Screenshots land in docs/qa/rtl/<page>-<lang>-<width>.png (reviewed in docs/I18N_RTL.md §8).

Checked at 390 px and 1440 px on the homepage, a public form (gate G2 opened with TEST-ONLY legal text),
the FAQ (Phase 3 opened) and the login page: no horizontal overflow, the drawer / mega-menu opens and stays
inside the viewport, and the layout is mirrored SEMANTICALLY — brand at the inline start, breadcrumbs
running right-to-left, forward arrows flipped, accordions and form labels aligned to the right, while
e-mail / password inputs and Latin data keep ``direction: ltr``.
"""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
QA_DIR = ROOT / "docs" / "qa" / "rtl"

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

WIDTHS = {390: 844, 1440: 900}
PAGES = {
    "home": "/{lang}/",
    "form": "/{lang}/entreprises/recueil-des-besoins/",
    "faq": "/{lang}/faq/",
    "login": "/{lang}/compte/login/",
}
#: Open defects of other owners ((lang, page, width)), kept visible by an xfail test instead of hiding the check.
KNOWN_OVERFLOW: set[tuple[str, str, int]] = set()


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
def phase3_live(set_flag, monkeypatch):
    """
    Open gate G3 for the live server WITHOUT freezegun: a frozen ``time.monotonic`` stalls Playwright's
    event loop. Every publication decision goes through ``core.clock.now()``, so patching it is enough.
    """
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.fixture
def site(live_server, seeded, legal_published, phase3_live):
    return live_server.url


def _open(browser, width: int):
    context = browser.new_context(viewport={"width": width, "height": WIDTHS[width]}, device_scale_factor=1)
    return context, context.new_page()


def _overflow(page) -> tuple[int, int]:
    return tuple(page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]"))


def _box(page, selector: str) -> dict:
    box = page.locator(selector).first.bounding_box()
    assert box, f"{selector} is not rendered"
    return box


@pytest.mark.parametrize("width", list(WIDTHS))
def test_arabic_pages_do_not_overflow_and_are_captured_with_their_ltr_twin(browser, site, width):
    QA_DIR.mkdir(parents=True, exist_ok=True)
    context, page = _open(browser, width)
    try:
        for lang in ("ar", "fr"):
            for name, path in PAGES.items():
                response = page.goto(site + path.format(lang=lang), wait_until="networkidle")
                assert response.status == 200, (lang, name, response.status)
                assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
                assert page.evaluate("document.documentElement.lang") == lang
                page.screenshot(path=str(QA_DIR / f"{name}-{lang}-{width}.png"), full_page=True)
                assert page.locator("h1").count() == 1, (lang, name)
                if (lang, name, width) not in KNOWN_OVERFLOW:
                    scroll_w, client_w = _overflow(page)
                    assert scroll_w <= client_w, (lang, name, width, scroll_w, client_w)
    finally:
        context.close()


@pytest.mark.parametrize("width", list(WIDTHS))
def test_every_arabic_public_page_fits_the_viewport(browser, site, width):
    """Whole-site sweep (every registered public route, gates open): no horizontal overflow, exactly one h1."""
    from core.public_routes import all_routes

    context, page = _open(browser, width)
    try:
        served, problems = 0, []
        for route in all_routes():
            response = page.goto(site + f"/ar/{route.path}", wait_until="domcontentloaded")
            served += response.status == 200
            scroll_w, client_w = _overflow(page)
            if scroll_w > client_w or page.locator("h1").count() != 1:
                problems.append((route.path, response.status, scroll_w, client_w, page.locator("h1").count()))
        assert served >= 55, served
        assert problems == []
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["ar", "fr"])
def test_mobile_drawer_opens_inside_the_viewport(browser, site, lang):
    """Below 80rem «Menu» opens the sheet (design V5, plan §1.12 item 8; W2-C2): inside the viewport, in both
    directions; the full measures in Arabic are tests/i18n/test_rtl_browser_w2_c2.py's."""
    context, page = _open(browser, 390)
    try:
        page.goto(site + f"/{lang}/", wait_until="networkidle")
        toggle = page.locator("[data-nav-toggle]")
        assert toggle.get_attribute("aria-expanded") == "false"
        toggle.click()
        page.wait_for_timeout(450)
        assert toggle.get_attribute("aria-expanded") == "true"
        drawer = page.locator("#nav-sheet")
        assert drawer.is_visible()
        first_link = drawer.locator("a").first
        assert first_link.is_visible()
        box = first_link.bounding_box()
        assert 0 <= box["x"] and box["x"] + box["width"] <= 390, box
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
        page.screenshot(path=str(QA_DIR / f"nav-open-{lang}-390.png"), full_page=False)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        assert toggle.get_attribute("aria-expanded") == "false"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["ar", "fr"])
def test_desktop_mega_menu_opens_inside_the_viewport(browser, site, lang):
    context, page = _open(browser, 1440)
    try:
        page.goto(site + f"/{lang}/", wait_until="networkidle")
        # «Il portico» (design V5, W2-C1): a door is a disclosure button; its panel hangs from the content width
        door = page.locator("[data-portico-door]").first
        door.click()
        page.wait_for_timeout(350)
        assert door.get_attribute("aria-expanded") == "true"
        panel = page.locator("#" + door.get_attribute("aria-controls"))
        assert panel.is_visible()
        box = panel.bounding_box()
        assert 0 <= box["x"] and box["x"] + box["width"] <= 1440, box
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
        page.screenshot(path=str(QA_DIR / f"nav-open-{lang}-1440.png"), full_page=False)
    finally:
        context.close()


def test_header_breadcrumbs_and_arrows_are_mirrored_semantically(browser, site):
    """Same page in French and Arabic: what is at the inline start in LTR is at the inline start in RTL."""
    context, page = _open(browser, 1440)
    try:
        measures = {}
        for lang in ("fr", "ar"):
            page.goto(site + f"/{lang}/entreprises/recueil-des-besoins/", wait_until="networkidle")
            brand, nav = _box(page, ".brand"), _box(page, ".main-nav__list")
            crumbs = page.locator(".breadcrumbs__item")
            first, last = crumbs.first.bounding_box(), crumbs.last.bounding_box()
            measures[lang] = {
                "brand_before_nav": brand["x"] + brand["width"] <= nav["x"] + 1,
                "nav_before_brand": nav["x"] + nav["width"] <= brand["x"] + 1,
                "crumbs_left_to_right": first["x"] < last["x"],
                "h1_align": page.evaluate("getComputedStyle(document.querySelector('h1')).textAlign"),
                "body_direction": page.evaluate("getComputedStyle(document.body).direction"),
            }
        assert measures["fr"]["brand_before_nav"] and measures["ar"]["nav_before_brand"], measures
        assert measures["fr"]["crumbs_left_to_right"] and not measures["ar"]["crumbs_left_to_right"], measures
        assert measures["fr"]["body_direction"] == "ltr" and measures["ar"]["body_direction"] == "rtl"
        assert measures["ar"]["h1_align"] in ("start", "right", "center")

        # Forward arrows (.icon--flip-rtl) are flipped in Arabic only.
        for lang, expected in (("fr", "none"), ("ar", "matrix(-1, 0, 0, 1, 0, 0)")):
            page.goto(site + f"/{lang}/page-inexistante/", wait_until="networkidle")
            transform = page.evaluate("getComputedStyle(document.querySelector('main .icon--flip-rtl')).transform")
            assert transform == expected, (lang, transform)
        # Direction mirrors, meaning does not (design V5, the closed flip list of core.icons): on the Arabic page the
        # key of «Espace réservé» — the identity tier, on the letterhead's plate since «Il portico» (W2-C1) — keeps
        # its drawing, and the tag gave it no flip class.
        page.goto(site + "/ar/", wait_until="networkidle")
        key = page.evaluate(
            "(() => { const s = document.querySelector('.site-header__end .targa svg.icon');"
            " return s && [getComputedStyle(s).transform, s.getAttribute('class'), s.querySelector('use').getAttribute('href')]; })()"
        )
        assert key and key[0] == "none" and "icon--flip-rtl" not in key[1] and key[2].endswith("#icon-ile-key"), key
    finally:
        context.close()


def test_arabic_typefaces_are_applied_and_loaded(browser, site):
    """Design V5, type «Una voce» (V5.4 plan §1.1): Vazirmatn draws every Arabic role — the interface on a
    nav link and the reading text of the body — with Host Grotesk right behind it in the stack for the Latin
    runs and the digits; both are preloaded on an Arabic page, and loaded."""
    context, page = _open(browser, 1440)
    try:
        page.goto(site + "/ar/", wait_until="networkidle")

        def stack(css: str) -> list[str]:  # a one-word family is serialised without quotes
            return [family.strip().strip('"') for family in css.split(",")]

        nav = page.evaluate("getComputedStyle(document.querySelector('.main-nav__link')).fontFamily")
        assert stack(nav)[:2] == ["Vazirmatn", "Host Grotesk"], nav
        body = page.evaluate("getComputedStyle(document.body).fontFamily")
        assert stack(body)[:2] == ["Vazirmatn", "Host Grotesk"], body
        assert page.evaluate("document.fonts.ready.then(() => document.fonts.check('16px \"Vazirmatn\"', 'الرئيسية'))")
        loaded = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
        assert "Vazirmatn" in loaded and "Host Grotesk" in loaded, loaded
        for retired in ("Noto Naskh Arabic", "IBM Plex Sans Arabic"):
            assert retired not in loaded, retired
        # Naskh needs room for its diacritics: the leading opens, the size does not shrink.
        assert page.evaluate("getComputedStyle(document.body).lineHeight") == "32px"
    finally:
        context.close()


def test_arabic_form_is_right_aligned_and_latin_inputs_stay_ltr(browser, site):
    context, page = _open(browser, 390)
    try:
        page.goto(site + "/ar/entreprises/recueil-des-besoins/", wait_until="networkidle")
        assert page.locator("form[method='post'] input[name='csrfmiddlewaretoken']").count() == 1
        label = page.locator(".form-field__label").first
        field_id = label.get_attribute("for")
        label_box, input_box = label.bounding_box(), page.locator(f"#{field_id}").bounding_box()
        # Label and control share their inline-start (right) edge.
        assert abs((label_box["x"] + label_box["width"]) - (input_box["x"] + input_box["width"])) <= 2
        assert page.evaluate(f"getComputedStyle(document.getElementById('{field_id}')).direction") == "rtl"
        for selector in ("input[type='email']", "input[type='tel']"):
            if page.locator(selector).count():
                style = page.evaluate(
                    f'(() => {{ const s = getComputedStyle(document.querySelector("{selector}"));'
                    " return [s.direction, s.textAlign]; })()"
                )
                assert style[0] == "ltr", (selector, style)
                assert style[1] in ("end", "right"), (selector, style)
        # Submitting the empty form shows the errors, translated, without breaking the layout.
        page.locator("form[method='post'] [type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
        page.screenshot(path=str(QA_DIR / "form-errors-ar-390.png"), full_page=True)

        page.goto(site + "/ar/compte/login/", wait_until="networkidle")
        for selector in ("input[type='email']", "input[type='password']"):
            assert page.evaluate(f'getComputedStyle(document.querySelector("{selector}")).direction') == "ltr"
    finally:
        context.close()


def test_arabic_accordion_opens_with_its_question_at_the_inline_start(browser, site):
    context, page = _open(browser, 1440)
    try:
        page.goto(site + "/ar/faq/", wait_until="networkidle")
        item = page.locator("details.accordion__item").first
        summary = item.locator("summary")
        assert item.evaluate("el => el.open") is False
        summary.click()
        page.wait_for_timeout(250)
        assert item.evaluate("el => el.open") is True
        assert item.locator(".accordion__panel").is_visible()
        summary_box, question_box = summary.bounding_box(), summary.locator("h3").bounding_box()
        gap_right = (summary_box["x"] + summary_box["width"]) - (question_box["x"] + question_box["width"])
        gap_left = question_box["x"] - summary_box["x"]
        assert gap_right <= 8 and gap_right <= gap_left, "in RTL the question starts at the right edge"
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
        page.screenshot(path=str(QA_DIR / "faq-open-ar-1440.png"), full_page=False)
    finally:
        context.close()


@pytest.mark.parametrize("path", ["faq/", "glossaire/"])
def test_arabic_search_pages_do_not_overflow_on_a_phone(browser, site, path):
    """RTL-03 (fixed 2026-09-20 by the design system): the search form wraps instead of overflowing at 390 px."""
    context, page = _open(browser, 390)
    try:
        page.goto(site + f"/ar/{path}", wait_until="networkidle")
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w, (path, scroll_w, client_w)
    finally:
        context.close()


#: Text-bearing fallback elements (``lang`` = fr / it / en, with a text node of their own) that are still laid out
#: right-to-left on an Arabic page. Containers (lists, grids, the diagram) keep the page direction on purpose and
#: carry no text of their own; links and buttons follow the page so that their arrows stay mirrored.
_FALLBACK_PROBE = """
Array.from(document.querySelectorAll('main [lang="fr"], main [lang="it"], main [lang="en"]'))
  .filter(el => !el.closest('a, button'))
  .filter(el => Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 1))
  .map(el => ({tag: el.tagName.toLowerCase(), direction: getComputedStyle(el).direction,
               text: el.textContent.trim().slice(0, 60)}))
"""
_FALLBACK_PAGES = ("/ar/", "/ar/entreprises/", "/ar/entreprises/recueil-des-besoins/", "/ar/forum/", "/ar/faq/")


def _fallback_elements(browser, site) -> list[dict]:
    context, page = _open(browser, 1440)
    try:
        found = []
        for path in _FALLBACK_PAGES:
            page.goto(site + path, wait_until="networkidle")
            found += [{**item, "path": path} for item in page.evaluate(_FALLBACK_PROBE)]
        return found
    finally:
        context.close()


def test_french_fallback_blocks_are_isolated_left_to_right_on_arabic_pages(browser, site):
    """
    RTL-01 and RTL-09 (fixed 20/09/2026 in static/css/base.css): every [lang] fallback TEXT element — the
    ``<label lang="fr">`` of the locked consent sentence included — is isolated left-to-right, so the final
    full stop of a prescribed sentence stays at its end.
    """
    found = _fallback_elements(browser, site)
    assert len(found) >= 20, "the pages render prescribed French texts"
    assert {item["path"] for item in found} == set(_FALLBACK_PAGES)
    assert [item for item in found if item["tag"] == "label"], "the Arabic forms render the locked consent sentence"
    assert [item for item in found if item["direction"] != "ltr"] == []


def _icon_matrix(page, selector: str) -> list[float]:
    value = page.evaluate(f'getComputedStyle(document.querySelector("{selector}")).transform')
    assert value.startswith("matrix("), value
    return [float(part) for part in value[7:-1].split(",")]


def test_mirrored_arrow_stays_mirrored_while_hovered(browser, site):
    """RTL-05 (fixed by the design system): the hover nudge uses the ``translate`` property, which composes with the scaleX(-1) of .icon--flip-rtl instead of replacing it."""
    context, page = _open(browser, 1440)
    try:
        page.goto(site + "/ar/page-inexistante/", wait_until="networkidle")
        selector = "main .btn--arrow .icon--flip-rtl"
        assert _icon_matrix(page, selector)[0] == -1
        page.hover("main .btn--arrow")
        page.wait_for_timeout(400)
        assert _icon_matrix(page, selector)[0] == -1, "the hover transform dropped the RTL mirroring"
    finally:
        context.close()


_TRADEMARK_PROBE = """
(() => {
  const name = "Italy Legal Entry";
  const found = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const at = node.data.indexOf(name + "\\u2122");
    const element = node.parentElement;
    if (at < 0 || !element || element.closest("script, style, svg, title")) continue;
    const first = document.createRange();
    first.setStart(node, at);
    first.setEnd(node, at + 1);
    const sign = document.createRange();
    sign.setStart(node, at + name.length);
    sign.setEnd(node, at + name.length + 1);
    const a = first.getBoundingClientRect();
    const b = sign.getBoundingClientRect();
    if (!a.width || !b.width || Math.abs(a.y - b.y) > a.height) continue;  // hidden, or wrapped on two lines
    const scope = element.closest("[lang]");
    found.push({
      lang: scope ? scope.lang : "",
      wordmark: !!element.closest('[translate="no"]'),
      ok: b.x > a.x,
      where: element.tagName.toLowerCase() + "." + element.className,
      text: node.data.trim().slice(0, 70),
    });
  }
  // The V2 lock-up (cms_nav.brand_lockup, 24 September 2026) sets the three words and the sign
  // in four spans of their own — «Italy» green, «Legal» navy, «Entry» red — so no single text
  // node holds «Italy Legal Entry™» any more and the walk above cannot see the header or the
  // footer wordmark. The property under test is the same: the sign paints to the RIGHT of the
  // first letter, inside a left-to-right isolate. It is measured on the spans instead.
  for (const wm of document.querySelectorAll(".lock__wm")) {
    const first = wm.querySelector(".lock__w1");
    const sign = wm.querySelector(".lock__tm");
    if (!first || !sign) continue;
    const a = first.getBoundingClientRect();
    const b = sign.getBoundingClientRect();
    if (!a.width || !b.width) continue;
    const lock = wm.closest(".lock");
    const scope = wm.closest("[lang]");
    found.push({
      lang: scope ? scope.lang : "",
      wordmark: !!(lock && lock.getAttribute("translate") === "no" && lock.getAttribute("dir") === "ltr"),
      ok: b.x > a.x,
      where: "span." + lock.className,
      text: wm.textContent.trim().slice(0, 70),
    });
  }
  return found;
})()
"""


def _trademark_occurrences(browser, site, paths) -> list[dict]:
    context, page = _open(browser, 1440)
    try:
        found = []
        for path in paths:
            page.goto(site + path, wait_until="networkidle")
            found += [{**item, "path": path} for item in page.evaluate(_TRADEMARK_PROBE)]
        return found
    finally:
        context.close()


_TRADEMARK_PAGES = ("/ar/", "/ar/le-projet/", "/ar/entreprises/", "/ar/contact/", "/ar/compte/login/")


def test_trademark_sign_stays_on_the_right_of_the_name_in_arabic_sentences(browser, site):
    """
    « ™ » is a bidi-neutral character: without the LEFT-TO-RIGHT MARK that the Arabic catalogue puts after it,
    a right-to-left sentence paints it on the LEFT of the name (« ™Italy Legal Entry »).
    """
    found = _trademark_occurrences(browser, site, _TRADEMARK_PAGES)
    translated = [item for item in found if item["lang"] == "ar" and not item["wordmark"]]
    assert len(translated) >= 3, found
    assert [item for item in translated if not item["ok"]] == []


def test_trademark_sign_stays_on_the_right_of_the_name_in_every_wordmark(browser, site):
    """I18N-06 (fixed): every {% brand %} wordmark — header and footer — is isolated left-to-right."""
    found = _trademark_occurrences(browser, site, _TRADEMARK_PAGES[:1])
    wordmarks = [item for item in found if item["wordmark"]]
    assert len(wordmarks) >= 2, found
    assert [item for item in wordmarks if not item["ok"]] == []


def test_arabic_orientation_wizard_is_mirrored_on_a_phone(browser, site):
    """Multi-step flow in RTL: progress bar filled from the right, choices read right-to-left, no overflow."""
    context, page = _open(browser, 390)
    try:
        page.goto(site + "/ar/orientation/", wait_until="networkidle")
        page.locator("form.wizard-intro__start [type='submit']").click()
        page.wait_for_load_state("networkidle")
        assert "/ar/orientation/session/" in page.url
        assert page.evaluate("document.documentElement.dir") == "rtl"
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w, (scroll_w, client_w)
        bar, fill = _box(page, ".wizard__progress-bar"), _box(page, ".wizard__progress-fill")
        assert abs((bar["x"] + bar["width"]) - (fill["x"] + fill["width"])) <= 1, "the progress grows from the right"
        choice = page.locator(".wizard__choice").first
        choice_box, label_box = choice.bounding_box(), choice.locator("label").bounding_box()
        gap_right = (choice_box["x"] + choice_box["width"]) - (label_box["x"] + label_box["width"])
        gap_left = label_box["x"] - choice_box["x"]
        assert gap_right >= 0 and gap_left >= 0
        assert page.evaluate("getComputedStyle(document.querySelector('.wizard__label')).direction") in ("rtl", "ltr")
        actions = page.locator(".wizard__actions .btn")
        assert actions.first.is_visible()
        page.screenshot(path=str(QA_DIR / "wizard-ar-390.png"), full_page=True)
        # Answer the first question: the second step offers « previous », laid out after « continue » (to its left).
        choice.locator("label").click()
        actions.first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w, (scroll_w, client_w)
        buttons = page.locator(".wizard__actions .btn")
        if buttons.count() == 2:
            first, second = buttons.nth(0).bounding_box(), buttons.nth(1).bounding_box()
            same_row = abs(first["y"] - second["y"]) < first["height"] / 2
            assert not same_row or second["x"] < first["x"], "in RTL the second action sits on the left of the first"
    finally:
        context.close()


_SEPARATOR_PROBE = """
(() => {
  const item = document.querySelector(".breadcrumbs__item + .breadcrumbs__item");
  const style = getComputedStyle(item, "::before");
  const matrix = style.transform.slice(7, -1).split(",").map(Number);
  // The chevron is the corner between the two painted borders: it points along their diagonal.
  const x = parseFloat(style.borderRightWidth) > 0 ? 1 : -1;
  const y = parseFloat(style.borderBottomWidth) > 0 ? 1 : -1;
  return [matrix[0] * x + matrix[2] * y, matrix[1] * x + matrix[3] * y];
})()
"""


def _separator_direction(browser, site, lang: str) -> tuple[float, float]:
    context, page = _open(browser, 1440)
    try:
        page.goto(site + f"/{lang}/entreprises/recueil-des-besoins/", wait_until="networkidle")
        x, y = page.evaluate(_SEPARATOR_PROBE)
        return round(x, 2), round(y, 2)
    finally:
        context.close()


def test_breadcrumb_separator_points_forward_in_french(browser, site):
    x, y = _separator_direction(browser, site, "fr")
    assert x > 1 and abs(y) < 0.1, (x, y)


def test_breadcrumb_separator_points_forward_in_arabic(browser, site):
    """RTL-08 (fixed by the design system): the chevron drawn with logical borders is no longer rotated twice."""
    x, y = _separator_direction(browser, site, "ar")
    assert x < -1 and abs(y) < 0.1, (x, y)


# ---------------------------------------------------------------------------------------------
# Reserved area (signed-in person) in Arabic on a phone
# ---------------------------------------------------------------------------------------------
def _signed_in_page(browser, site, user, width: int):
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(user)
    context = browser.new_context(viewport={"width": width, "height": WIDTHS[width]}, device_scale_factor=1)
    session = client.cookies[settings.SESSION_COOKIE_NAME].value
    context.add_cookies([{"name": settings.SESSION_COOKIE_NAME, "value": session, "url": site}])
    return context, context.new_page()


def _reserved_area_overflow(browser, site, user, paths) -> list[tuple]:
    context, page = _signed_in_page(browser, site, user, 390)
    try:
        problems = []
        for path in paths:
            response = page.goto(site + f"/ar/{path}", wait_until="networkidle")
            assert response.status == 200, (path, response.status)
            assert page.evaluate("document.documentElement.dir") == "rtl"
            scroll_w, client_w = _overflow(page)
            if scroll_w > client_w or page.locator("h1").count() != 1:
                problems.append((path, scroll_w, client_w, page.locator("h1").count()))
        return problems
    finally:
        context.close()


def test_arabic_reserved_area_fits_a_phone(browser, site, person_user):
    from .test_page_integrity import RESERVED_AREA

    assert _reserved_area_overflow(browser, site, person_user, RESERVED_AREA) == []


def test_arabic_saved_pre_assessment_fits_a_phone(browser, site, person_user):
    """
    RTL-10, closed on 20 September 2026.

    A left-to-right item inside a mirrored list hung its bullet outside the item's inline-start
    edge — on the left, where a mirrored list has no padding — giving 3 px of horizontal scroll at
    390 px and bullets on the wrong side. Fixed with list-style-position: inside for exactly those
    items (base.css), so the marker stays inside the item box.
    """
    from orientation.models import OrientationResult, OrientationSession, Outcome, SessionStatus
    from orientation.services import active_ruleset

    ruleset = active_ruleset()
    outcome = Outcome.objects.filter(ruleset=ruleset).order_by("id").first()
    session = OrientationSession.objects.create(ruleset=ruleset, user=person_user, status=SessionStatus.COMPLETED)
    OrientationResult.objects.create(
        session=session, outcome=outcome, ruleset_version=ruleset.version, result_text_fr=outcome.explanation_fr
    )
    assert _reserved_area_overflow(browser, site, person_user, ("espace-reserve/mon-parcours/",)) == []
