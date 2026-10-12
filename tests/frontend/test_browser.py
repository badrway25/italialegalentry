"""
Browser tests (Playwright, Chromium) for the design system shell.

Run with: pytest tests/frontend/test_browser.py -m browser
Screenshots land in docs/qa/design/ (ignored by git except the golden set).
Checks: no horizontal overflow at 360/768/1440 in LTR and RTL, the keyboard model of «Il portico» (design V5,
V5.4 plan §1.12; the full behaviour checks are in test_browser_w2_c1.py), mobile drawer, reveal never hides content,
dialogs restore focus.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
QA_DIR = ROOT / "docs" / "qa" / "design"

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

VIEWPORTS = {"mobile": (360, 780), "tablet": (768, 1024), "desktop": (1440, 900)}
PAGES = {
    "home": "/{lang}/",
    "login": "/{lang}/compte/login/",
    "privacy": "/{lang}/privacy-policy/",
    "404": "/{lang}/page-inesistente/",
}


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
def menu_rows(db):
    """CMS menu rows with children so the mega-menu is exercised whatever sibling apps exist."""
    from cms.models import MenuItem, MenuLocation

    for order, (label, url) in enumerate([("Personnes", "/fr/"), ("Entreprises", "/fr/privacy-policy/")], start=1):
        parent = MenuItem.objects.create(
            location=MenuLocation.MAIN,
            order=order,
            label_fr=label,
            label_it=label,
            label_en=label,
            label_ar=label,
            url=url,
            description_fr="Section description",
        )
        for sub, (child, curl) in enumerate(
            [
                ("Privacy Policy", "/fr/privacy-policy/"),
                ("Cookie Policy", "/fr/cookie-policy/"),
                ("Mentions", "/fr/note-legali/"),
            ],
            start=1,
        ):
            MenuItem.objects.create(
                location=MenuLocation.MAIN,
                parent=parent,
                order=sub,
                label_fr=child,
                label_it=child,
                label_en=child,
                label_ar=child,
                url=curl,
            )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        order=3,
        label_fr="Forum",
        label_it="Forum",
        label_en="Forum",
        label_ar="Forum",
        url="/fr/avvertenze/",
    )


def _page(browser, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    return context, context.new_page()


def _overflow(page) -> tuple[int, int]:
    return page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("viewport", list(VIEWPORTS))
def test_no_horizontal_overflow_and_screenshots(browser, live_server, seeded, menu_rows, lang, viewport):
    QA_DIR.mkdir(parents=True, exist_ok=True)
    width, height = VIEWPORTS[viewport]
    context, page = _page(browser, width, height)
    try:
        for name, path in PAGES.items():
            page.goto(live_server.url + path.format(lang=lang), wait_until="networkidle")
            scroll_w, client_w = _overflow(page)
            assert scroll_w <= client_w, (lang, viewport, name, scroll_w, client_w)
            assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
            assert page.evaluate("document.documentElement.classList.contains('js')")
            # Reveal never hides content: every .reveal is visible after load
            hidden = page.evaluate(
                "Array.from(document.querySelectorAll('.reveal')).filter(e => getComputedStyle(e).opacity === '0').length"
            )
            assert hidden == 0
            page.screenshot(path=str(QA_DIR / f"{name}-{lang}-{viewport}.png"), full_page=True)
        # Open the mobile drawer / desktop panel for a screenshot of the navigation state
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        if width < 1024:
            page.click("[data-nav-toggle]")
            page.wait_for_timeout(300)
        else:
            page.click("[data-portico-door]")
            page.wait_for_timeout(300)
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
        page.screenshot(path=str(QA_DIR / f"nav-open-{lang}-{viewport}.png"), full_page=False)
    finally:
        context.close()


def test_mega_menu_is_keyboard_operable(browser, live_server, seeded, menu_rows):
    """«Il portico» (design V5, plan §1.12) is a disclosure navigation: Enter toggles a panel and leaves the focus on
    its door, ↓ enters the panel, Esc closes it and returns the focus, ← → walk the bar — with a panel open the
    open panel follows them — and focus leaving the navigation closes it (WCAG 1.4.13)."""
    context, page = _page(browser, 1440, 900)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        door = page.locator("[data-portico-door]").first
        panel_id = door.get_attribute("aria-controls")
        panel = page.locator(f"#{panel_id}")
        door.focus()
        page.keyboard.press("Enter")
        assert door.get_attribute("aria-expanded") == "true"
        assert panel.is_visible()
        # a disclosure, not a menu: the focus stays on the door; ↓ enters the panel
        assert page.evaluate("document.activeElement.hasAttribute('data-portico-door')")
        page.keyboard.press("ArrowDown")
        assert page.evaluate(f"document.getElementById('{panel_id}').contains(document.activeElement)")
        # Escape closes it and returns the focus to the door
        page.keyboard.press("Escape")
        assert door.get_attribute("aria-expanded") == "false"
        assert not panel.is_visible()
        assert page.evaluate("document.activeElement.hasAttribute('data-portico-door')")
        # ← → move between the top-level items without opening anything
        page.keyboard.press("ArrowRight")
        assert page.evaluate("document.activeElement.textContent.trim()") == "Entreprises"
        assert page.locator("[data-portico-door][aria-expanded='true']").count() == 0
        # with a panel open, the arrows move the open panel with the focus (never a closed bar)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowLeft")
        assert page.evaluate("document.activeElement.textContent.trim()") == "Personnes"
        assert door.get_attribute("aria-expanded") == "true"
        # Tab past the navigation closes the panel (focusout)
        for _ in range(30):
            page.keyboard.press("Tab")
            if not page.evaluate("document.querySelector('[data-portico]').contains(document.activeElement)"):
                break
        assert page.locator("[data-portico-door][aria-expanded='true']").count() == 0
    finally:
        context.close()


def test_mobile_drawer_and_language_switcher(browser, live_server, seeded, menu_rows):
    context, page = _page(browser, 360, 780)
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        assert not page.locator("#nav-drawer").is_visible()
        page.click("[data-nav-toggle]")
        page.wait_for_timeout(300)
        assert page.locator("#nav-drawer").is_visible()
        assert page.get_attribute("[data-nav-toggle]", "aria-expanded") == "true"
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        assert page.get_attribute("[data-nav-toggle]", "aria-expanded") == "false"

        # Language switcher: details opens, Escape closes, link goes to /ar/.
        #
        # Below 48rem the institutional bar is not drawn — the letterhead is 56px in total on a
        # phone (docs/design-v2/DESIGN_SYSTEM_V2.md §4, §8.2) — and its contents, the promoter line,
        # the reserved-area link and this switcher, are rendered at the top of the drawer instead.
        # So on a phone the language is reached through the menu, which is where IND and
        # Migrationsverket put it too. The drawer is opened first, and the switcher is addressed
        # inside it: the one in the bar is still in the DOM at this width, and still display:none.
        #
        # That move is what exposed the Escape bug the assertion below now guards: one key press
        # used to close the language list AND the menu around it, because the dropdown's handler
        # did not stop the event reaching the drawer's handler on `document`.
        drawer = page.locator("#nav-drawer")
        page.click("[data-nav-toggle]")
        page.wait_for_timeout(300)
        # Design V4: the drawer carries the segmented language control — four links, no dropdown,
        # so Escape has one thing to close: the drawer itself.
        assert drawer.locator(".lang-seg__link").count() == 4
        page.keyboard.press("Escape")
        assert page.get_attribute("[data-nav-toggle]", "aria-expanded") == "false"
        page.click("[data-nav-toggle]")
        page.wait_for_timeout(300)
        drawer.locator(".lang-seg__link[hreflang='ar']").click()
        page.wait_for_load_state("networkidle")
        assert page.url.endswith("/ar/")
        assert page.evaluate("document.documentElement.dir") == "rtl"
        scroll_w, client_w = _overflow(page)
        assert scroll_w <= client_w
    finally:
        context.close()


def test_fonts_are_self_hosted_and_loaded(browser, live_server, seeded):
    context, page = _page(browser, 1280, 800)
    requests: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        externals = [u for u in requests if not u.startswith(live_server.url)]
        assert externals == [], externals
        # Design V5, type «Una voce» (V5.4 plan §1.1): Host Grotesk draws every Latin role and «ILE Wordmark»
        # the name in the letterhead — both preloaded, both loaded; no V4 face is requested.
        assert page.evaluate("document.fonts.ready.then(() => document.fonts.check('16px \"Host Grotesk\"'))")
        loaded = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
        assert "Host Grotesk" in loaded and "ILE Wordmark" in loaded, loaded
        assert page.evaluate("getComputedStyle(document.body).fontFamily").startswith('"Host Grotesk"')
        assert page.evaluate("getComputedStyle(document.querySelector('.lock__wm')).fontFamily").startswith(
            '"ILE Wordmark"'
        )
        fonts = [u.rsplit("/", 1)[-1] for u in requests if u.endswith(".woff2")]
        assert fonts and all(name.startswith("v5-") for name in fonts), fonts
        assert not any("vazirmatn" in name for name in fonts), "a Latin page never downloads the Arabic face"
    finally:
        context.close()
