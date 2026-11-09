"""
V5.24 — the homepage's professional pass, the browser half (FINAL_DELIVERY_V2 §3.4 gate 2; lane HOME, label v524-home).
On the real page, Phase 3, through Playwright's Chromium (headless; no lock slot: the lane's gate takes one for the
eye):

* the seams stand where the Director placed them, fr and ar — the wash's foot a 6 rem fade into the index band's stone;
  the pilot's gold seam beginning 32 px above the night on the panel's centre line, its node on the seam's axis, hidden
  where the halves stack (390); the night's velatura at the top of the masonry (12 rem; 8 on phones) as a still
  gradient; the pietra's grid on «la protezione», one compact band (V5.29 §4: no sill, no bookend); the light at
  the arch's sill;
* the raccordo plays once — it waits below the fold, draws after the panel's own thread (the primitive's delay) and
  leaves getAnimations(); under reduced motion and from the keyboard it stands drawn and nothing runs;
* the masonry band's head keeps its contrast under the night: the paper behind the title, sampled from the rendered
  frame, against the ink at ≥ 7 : 1 (the head's words stand on the stone, not in the night).
"""

from __future__ import annotations

import io
import os

import pytest

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

RECT = """(s) => { const el = document.querySelector(s); if (!el) return null;
  const b = el.getBoundingClientRect();
  return {top: b.top + scrollY, bottom: b.bottom + scrollY, left: b.left, right: b.right, w: b.width, h: b.height};
}"""
PSEUDO = """([s, p, pseudo]) => { const el = document.querySelector(s);
  return el ? getComputedStyle(el, pseudo)[p] : null; }"""
RUNNING = """(s) => document.getAnimations()
  .filter(a => a.effect && a.effect.target === document.querySelector(s) && a.playState === 'running')
  .map(a => a.animationName)"""
GOLD = """() => { const p = document.createElement('span'); p.style.color = 'var(--identity-light)';
  document.body.append(p);
  const c = getComputedStyle(p).color; p.remove(); return c; }"""
NIGHT = """() => { const p = document.createElement('span'); p.style.color = 'var(--surface-night)';
  document.body.append(p);
  const c = getComputedStyle(p).color; p.remove(); return c; }"""
INK = """() => getComputedStyle(document.querySelector('.home-trust .testa__title')).color"""


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
    """Open gate G3 for the live server without freezing time (Playwright needs a real clock), as the V2 module does."""
    from core import flags
    from core.models import FeatureFlag

    FeatureFlag.objects.update_or_create(
        key="phase3_public", defaults={"enabled": True, "enabled_from": None, "enabled_until": None}
    )
    flags.invalidate()
    yield
    flags.invalidate()


def _context(browser, width, height, **kw):
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    # bypass_csp: wait_for_function evaluates its predicate as a string, which the site's CSP (no unsafe-eval) refuses
    viewport = {"width": width, "height": height}
    return browser.new_context(viewport=viewport, device_scale_factor=1, bypass_csp=True, **kw)


def _rgb(text: str) -> tuple[int, int, int]:
    nums = [float(x) for x in text.replace("rgba", "rgb").strip("rgb() ").split(",")[:3]]
    return tuple(round(n) for n in nums)


def _luminance(rgb) -> float:
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a, b) -> float:
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_seams_stand_where_the_director_placed_them(browser, live_server, phase3_live, lang):
    """FINAL_DELIVERY_V2 §3.4 gate 2 at 1440 and 390: the S2 → S3 fade over 6 rem; no seam into the pilot's night
    (V5.30 Fast Visual Variety Correction §5, V5.20 strict rule: the gold line and its thread are gone); the night
    veiling the masonry's first 12 rem (8 on phones) with no animation on the gradient; the protection's grid on the
    pietra and one compact band (V5.29 §4: no sill, no bookend, ≤ 240 px at 1440 fr); the ecosystem's frame plain
    (V5.30 §2: no arch, no light)."""
    context = _context(browser, 1440, 900, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        night = page.evaluate(NIGHT)
        # S2 → S3: the sfumatura, 6 rem of the velatura into the stone, on the wash's foot
        assert page.evaluate(PSEUDO, [".home-orientation", "height", "::after"]) == "96px"
        fade = page.evaluate(PSEUDO, [".home-orientation", "backgroundImage", "::after"])
        assert fade.startswith("linear-gradient(rgba(0, 0, 0, 0)") and fade.endswith(")"), fade
        assert page.evaluate("document.querySelector('.home-pathways').dataset.ground") == "stone"
        # S3 → S4: the panel opens on its photographs, no raccordo, no thread (V5.30 VARIETY §5)
        assert (
            page.evaluate("document.querySelector('.home-pilot').firstElementChild.className")
            == "panorama panorama--coppia pilota"
        )
        drawn = page.evaluate("document.querySelectorAll('.sez-raccordo, .pilota__filo, .panorama__cucitura').length")
        assert drawn == 0
        # S4 → S5: the velatura — the night first, over the stone veil, a still
        veil = page.evaluate(PSEUDO, [".home-trust .strato--foto", "backgroundImage", "::before"])
        assert veil.startswith(f"linear-gradient({night}, ") and veil.count("linear-gradient(") == 2, veil
        assert "192px" in veil, ("12 rem", veil)
        assert page.evaluate(PSEUDO, [".home-trust .strato--foto", "animationName", "::before"]) == "none"
        # S6: pietra — the grid masked toward the plate. Amended under V5.20 citing V5.29 §4 (the owner, 6 Nov 2026:
        # «protezione__campo too dominant … one global refined compact treatment»): V5.24's bookend and sill are
        # retired, so the seam is now the compact band on the same ground — no sill, no bookend, the pietra and its
        # grid's mask direction kept, the band ≤ 240 px at 1440 in fr (a stronger bound on the band's weight).
        assert page.evaluate("document.querySelector('.home-antifraud').dataset.ground") == "pietra"
        grid = page.evaluate(PSEUDO, [".home-antifraud", "maskImage", "::before"])
        assert grid.startswith("linear-gradient(to " + ("right" if lang == "ar" else "left")), grid
        assert page.evaluate("document.querySelector('.home-antifraud .sez-fondale')") is None, "no bookend"
        assert page.evaluate("document.querySelector('.protezione__davanzale')") is None, "no sill"
        band = page.evaluate(RECT, ".home-antifraud .protezione")
        assert band is not None and band["w"] > 0, band
        if lang == "fr":
            assert band["h"] <= 240, ("one compact band at 1440", band)
        # S7: carta viva. Amended under V5.20 citing V5.30 §2 (the owner, 7 Nov 2026: one dominant motif per section;
        # the home's arch and its sill's light are retired, docs/design-v5/QA/v530/art/NOTES.md §6–§7): the frame stands
        # plain, with nothing painted behind it, and the section still carries no light of its own.
        assert page.evaluate(PSEUDO, [".home-ecosystem .campata__media", "content", "::before"]) == "none"
        assert "data-luce" not in page.evaluate("document.querySelector('.home-ecosystem').outerHTML.split('>')[0]")
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") == 0
    finally:
        context.close()

    context = _context(browser, 390, 844, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        assert page.evaluate(PSEUDO, [".home-orientation", "height", "::after"]) == "96px", "6 rem at every width"
        assert page.evaluate("document.querySelectorAll('.sez-raccordo, .pilota__filo').length") == 0
        veil = page.evaluate(PSEUDO, [".home-trust .strato--foto", "backgroundImage", "::before"])
        assert "128px" in veil and veil.count("linear-gradient(") == 2, ("8 rem on phones", veil)
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") == 0
    finally:
        context.close()


def test_the_pilot_band_waits_and_enters_with_no_raccordo_and_stands_still_for_reduced_motion_and_the_keyboard(
    browser, live_server, phase3_live
):
    """V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule; this decision replaces the raccordo's draw on this
    band, BACKGROUND_MATERIAL_V2 §3.4): no line is left to draw; the band keeps its contract: it waits and enters on
    the panel's trigger (that a finished entrance leaves getAnimations() is held for every section by the V5.22 test);
    under reduced motion no state is written and nothing runs; from the keyboard nothing runs on it."""
    context = _context(browser, 1440, 900)
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.wait_for_function("document.querySelector('.home-pilot').dataset.secState === 'wait'")
        assert page.evaluate("document.querySelector('.home-pilot .sez-raccordo') === null")
        page.evaluate("document.querySelector('.home-pilot').scrollIntoView({block: 'start'})")
        page.wait_for_function("document.querySelector('.home-pilot').dataset.secState === 'in'")
    finally:
        context.close()

    context = _context(browser, 1440, 900, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.evaluate("document.querySelector('.home-pilot').scrollIntoView({block: 'start'})")
        page.wait_for_timeout(400)
        assert page.evaluate("document.querySelector('.home-pilot').hasAttribute('data-sec-state')") is False
        assert page.evaluate("document.getAnimations().filter(a => a.playState === 'running').length") == 0
    finally:
        context.close()

    context = _context(browser, 1440, 900)
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.keyboard.press("Tab")
        page.wait_for_function("document.documentElement.dataset.input === 'key'")
        page.evaluate("document.querySelector('.home-pilot').scrollIntoView({block: 'start'})")
        page.wait_for_function("document.querySelector('.home-pilot').dataset.secState === 'in'")
        page.wait_for_timeout(200)
        assert page.evaluate(RUNNING, ".home-pilot") == []
    finally:
        context.close()


@pytest.mark.parametrize(
    "width,height,lang", [(1440, 900, "fr"), (1440, 900, "ar"), (1024, 768, "fr"), (390, 844, "fr"), (390, 844, "ar")]
)
def test_the_masonry_band_s_head_keeps_its_contrast_under_the_night(
    browser, live_server, phase3_live, width, height, lang
):
    """The velatura's night stop is front-loaded so the head's words stand on the stone (BACKGROUND_MATERIAL_V2 §6.1's
    legibility; the lane's decision, NOTES §3): the frame's colour beside the title's first line, sampled from the
    rendered page, against the title's ink at ≥ 7 : 1 — and the band's top edge is the night's (the seam dissolved, not
    cut)."""
    from PIL import Image

    context = _context(browser, width, height, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.evaluate("document.querySelector('.home-trust').scrollIntoView({block: 'start'})")
        page.wait_for_timeout(500)
        band = page.evaluate("document.querySelector('.home-trust').getBoundingClientRect().toJSON()")
        title = page.evaluate("document.querySelector('.home-trust .testa__title').getBoundingClientRect().toJSON()")
        ink = _rgb(page.evaluate(INK))
        shot = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
        # the paper beside the title's first line: 6 px outside its box on the band's far side of the reading edge
        x = int(title["x"] - 12) if lang != "ar" else int(title["x"] + title["width"] + 12)
        x = min(max(x, 2), width - 3)
        y = int(title["y"] + 8)
        samples = [shot.getpixel((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (0, 4, 8)]
        paper = tuple(round(sum(s[i] for s in samples) / len(samples)) for i in range(3))
        ratio = _contrast(paper, ink)
        assert ratio >= 7, (width, lang, "the head on the stone", paper, ink, round(ratio, 2))
        # the band's first row reads as the night above it: within 1.3 : 1 of --surface-night (the night stop is
        # front-loaded, so a few pixels down the photograph already lifts it)
        top = shot.getpixel((width // 2, int(band["y"]) + 1))
        night = _rgb(page.evaluate(NIGHT))
        assert _contrast(top, night) <= 1.3, (width, lang, "the band begins in the night", top, night)
    finally:
        context.close()
