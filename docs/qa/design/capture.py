"""
Design QA screenshots — Italy Legal Entry™ (docs/DESIGN_SYSTEM.md, docs/ACCESSIBILITY.md).

Captures the pages that exist from the foundation at the three reference widths (390 / 768 / 1440)
in French (LTR) and Arabic (RTL), plus the interaction states the documentation refers to
(skip link focused, drawer open, mega-menu open, focus ring, reduced motion, 200 % / 400 % zoom
equivalents, JavaScript disabled).

The PNG files are QA artefacts: ``docs/qa/**/*.png`` is git-ignored, so regenerate them locally.

Usage (from the project root, with a local server running — never a remote host). Use a DEDICATED
database: the shared dev database must not be migrated or seeded by whoever captures, and when it
lags behind the working tree the homepage answers 500::

    set DJANGO_DEBUG=False
    set DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_<your_key>_capture
    .venv/Scripts/python manage.py migrate
    .venv/Scripts/python manage.py seed_all
    .venv/Scripts/python manage.py runserver 127.0.0.1:8793 --noreload --insecure
    .venv/Scripts/python docs/qa/design/capture.py --base-url http://127.0.0.1:8793

``DJANGO_DEBUG=False`` matters: with DEBUG on, Django renders its technical 404 page instead of
``templates/errors/404.html``. The script writes ``capture-report.json`` next to the screenshots
(HTTP status, horizontal overflow, <h1> count, dir attribute, external requests per page) and exits
with code 1 when a page answers with an unexpected status, overflows horizontally, loads an external
resource, does not have exactly one <h1>, still hides a ``.reveal`` block after the safety net, or lays
out an icon that draws nothing (``emptyIcons``: regression guard for gap G-01). The drawer-open captures
also record the drawer and overlay geometry (``drawer``), the JavaScript-disabled captures the sticky
header geometry (``header``) and the form-error captures the element that holds the focus after an
invalid submit (``focus``): evidence for gaps G-02, G-23, G-04 and G-05, never a failure condition.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

OUT = Path(__file__).resolve().parent
WIDTHS = {390: 844, 768: 1024, 1440: 900}
PAGES = {
    "home": "/{lang}/",
    "privacy": "/{lang}/privacy-policy/",
    "login": "/{lang}/compte/login/",
    "404": "/{lang}/page-inexistante/",
}
LANGS = ("fr", "ar")
NOT_FOUND_SUFFIX = PAGES["404"].replace("/{lang}", "")  # the only page expected to answer 404


def _allowed_host(base_url: str) -> None:
    host = urlparse(base_url).hostname or ""
    if host not in {"127.0.0.1", "localhost"}:
        raise SystemExit(f"Refusing to capture a non-local host: {host!r} (local work only).")


def _metrics(page) -> dict:
    return page.evaluate(
        """() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            h1: document.querySelectorAll('h1').length,
            dir: document.documentElement.dir,
            lang: document.documentElement.lang,
            js: document.documentElement.classList.contains('js'),
            hiddenReveal: Array.from(document.querySelectorAll('.reveal'))
                .filter(e => getComputedStyle(e).opacity === '0').length,
            // Regression guard for gap G-01 (closed): an icon whose box is laid out but whose <use>
            // has no geometry means the sprite did not load or did not parse. Icons inside hidden
            // containers have no box and are not counted.
            icons: Array.from(document.querySelectorAll('svg.icon')).filter(s => {
                const r = s.getBoundingClientRect(); return r.width > 0 && r.height > 0;
            }).length,
            emptyIcons: Array.from(document.querySelectorAll('svg.icon')).filter(s => {
                const r = s.getBoundingClientRect();
                if (!(r.width > 0 && r.height > 0)) return false;
                const use = s.querySelector('use');
                try { const b = use.getBBox(); return !(b.width > 0 && b.height > 0); } catch (e) { return true; }
            }).length,
        })"""
    )


def _drawer_geometry(page) -> dict:
    """Evidence for gaps G-02 (drawer height) and G-23 (overlay painted over the header): never a failure."""
    return page.evaluate(
        """() => {
            const drawer = document.querySelector('#nav-drawer');
            const overlay = document.querySelector('[data-nav-overlay]');
            const header = document.querySelector('.site-header');
            return {
                height: Math.round(drawer.getBoundingClientRect().height),
                contentHeight: drawer.scrollHeight,
                overlayHeight: overlay ? Math.round(overlay.getBoundingClientRect().height) : null,
                expectedHeight: Math.round(window.innerHeight - drawer.getBoundingClientRect().top),
                overlayTop: overlay ? Math.round(overlay.getBoundingClientRect().top) : null,
                headerBottom: Math.round(header.getBoundingClientRect().bottom),
            };
        }"""
    )


def _header_geometry(page) -> dict:
    """Evidence for gap G-04 (open): without JavaScript the sticky header holds the whole menu."""
    return page.evaluate(
        """() => {
            const header = document.querySelector('.site-header');
            return {
                height: Math.round(header.getBoundingClientRect().height),
                viewportHeight: window.innerHeight,
                position: getComputedStyle(header).position,
            };
        }"""
    )


def capture(base_url: str) -> int:
    from playwright.sync_api import sync_playwright

    _allowed_host(base_url)
    report: dict[str, dict] = {}
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()

        def shot(name: str, url: str, width: int, height: int, *, full_page=True, before=None, **ctx):
            nonlocal failures
            context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **ctx)
            page = context.new_page()
            external: list[str] = []
            page.on("request", lambda r: external.append(r.url) if not r.url.startswith(base_url) else None)
            response = page.goto(base_url + url, wait_until="networkidle")
            if before:
                before(page)
            data = _metrics(page)
            if data["hiddenReveal"]:
                # Below-the-fold .reveal blocks stay at opacity 0 until they intersect the viewport or
                # the 2.5 s safety net of main.js fires: wait for it so full-page captures are complete.
                page.wait_for_timeout(2700)
                data["hiddenRevealAfterSafetyNet"] = _metrics(page)["hiddenReveal"]
            data["status"] = response.status if response else None
            data["expectedStatus"] = 404 if url.endswith(NOT_FOUND_SUFFIX) else 200
            data["external"] = [u for u in external if not u.startswith("data:")]
            data["overflow"] = data["scrollWidth"] > data["clientWidth"]
            if name.startswith("state-drawer-open"):
                data["drawer"] = _drawer_geometry(page)
            if name.startswith("a11y-nojs"):
                data["header"] = _header_geometry(page)
            if name.startswith("state-form-errors"):
                # Evidence for gap G-05: after an invalid submit the focus belongs on the error summary.
                data["focus"] = page.evaluate("() => document.activeElement.id || document.activeElement.tagName")
            if (
                data["status"] != data["expectedStatus"]  # e.g. a 500 page must never pass as a valid capture
                or data["overflow"]
                or data["external"]
                or data["h1"] != 1
                or data.get("hiddenRevealAfterSafetyNet")
                or data["emptyIcons"]  # G-01 regression: a laid-out icon that draws nothing
            ):
                failures += 1
            page.screenshot(path=str(OUT / f"{name}.png"), full_page=full_page)
            report[name] = data
            context.close()

        # 1. Reference pages × widths × languages
        for lang in LANGS:
            for key, path in PAGES.items():
                for width, height in WIDTHS.items():
                    shot(f"{key}-{lang}-{width}", path.format(lang=lang), width, height)

        # 2. Interaction states
        def focus_skip_link(page):
            page.keyboard.press("Tab")

        def open_drawer(page):
            page.click("[data-nav-toggle]")
            page.wait_for_timeout(350)

        def open_mega_menu(page):
            # «Il portico» (design V5, W2-C1): a door is a disclosure button; Enter opens, the focus stays on it
            door = page.locator("[data-portico-door]").first
            if door.count():
                door.focus()
                page.keyboard.press("Enter")
                page.wait_for_timeout(300)

        def focus_first_field(page):
            page.focus("#id_login")

        def submit_empty_login(page):
            page.click("form.form button[type=submit]")
            page.wait_for_load_state("networkidle")

        for lang in LANGS:
            shot(f"state-skiplink-{lang}-390", f"/{lang}/", 390, 844, full_page=False, before=focus_skip_link)
            shot(f"state-drawer-open-{lang}-390", f"/{lang}/", 390, 844, full_page=False, before=open_drawer)
            # The navigation breakpoint is 80rem: a 1024 px laptop or a landscape tablet gets the drawer too.
            shot(f"state-drawer-open-{lang}-1024", f"/{lang}/", 1024, 768, full_page=False, before=open_drawer)
            shot(f"state-megamenu-open-{lang}-1440", f"/{lang}/", 1440, 900, full_page=False, before=open_mega_menu)
            shot(f"state-focus-field-{lang}-1440", f"/{lang}/compte/login/", 1440, 900, before=focus_first_field)
            shot(f"state-form-errors-{lang}-390", f"/{lang}/compte/login/", 390, 844, before=submit_empty_login)

        # 3. Accessibility variants (French): reduced motion, zoom equivalents, JavaScript disabled.
        #    200 % zoom of a 1280 px window = 640 CSS px; 400 % = 320 CSS px (WCAG 1.4.4 / 1.4.10).
        shot("a11y-reduced-motion-fr-1440", "/fr/", 1440, 900, reduced_motion="reduce")
        shot("a11y-zoom200-fr-640", "/fr/compte/login/", 640, 450)
        shot("a11y-zoom400-fr-320", "/fr/compte/login/", 320, 256)
        shot("a11y-zoom400-ar-320", "/ar/compte/login/", 320, 256)
        shot("a11y-nojs-fr-390", "/fr/", 390, 844, java_script_enabled=False)
        shot("a11y-nojs-fr-1024", "/fr/", 1024, 768, java_script_enabled=False)
        shot("a11y-nojs-fr-1440", "/fr/", 1440, 900, java_script_enabled=False)

        browser.close()

    (OUT / "capture-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(report)} screenshots written to {OUT}")
    for name, data in report.items():
        flag = "OVERFLOW" if data["overflow"] else "ok"
        print(f"  {name:<36} {data['status']} {data['dir']:<3} h1={data['h1']} {flag} ext={len(data['external'])}")
    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8793")
    args = parser.parse_args()
    sys.exit(1 if capture(args.base_url.rstrip("/")) else 0)
