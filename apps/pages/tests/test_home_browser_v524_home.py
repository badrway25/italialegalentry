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
# RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 5): the trust band opens on its
# statement (its title stays in the outline) — the head whose contrast is held is that statement
INK = """() => getComputedStyle(document.querySelector('.home-trust .chiaro__enunciato')).color"""


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
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§10, lane B «il
        # viaggio»): the wash became the deep ink band — no sfumatura is drawn over its action panel; the night ends
        # on its own edge right above the explorer's stone
        assert page.evaluate(PSEUDO, [".home-orientation", "content", "::after"]) == "none"
        assert page.evaluate("document.querySelector('.home-orientation').dataset.ground") == "night"
        assert page.evaluate("document.querySelector('.home-orientation').dataset.sfuma") is None
        assert page.evaluate("document.querySelector('.home-pathways').dataset.ground") == "stone"
        # S3 → S4: no raccordo, no thread (V5.30 VARIETY §5). RESTATED under V5.20 for the owner's FINAL HOMEPAGE
        # REBUILD directive of 10 Nov 2026 (§17,
        # lane A): the night opens on its two national fields (aria-hidden), the head and the photographs' stage follow
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 6: photography first):
        # the head is the band's first child in the document, the stage is DRAWN first, and each national field is
        # inside its photograph's half (aria-hidden) — Morocco's at the left, Italy's at the right in both languages
        assert page.evaluate("document.querySelector('.home-pilot').firstElementChild.className") == (
            "container pilota-testa"
        )
        fields = page.evaluate(
            """() => [...document.querySelectorAll('.home-pilot .pilota-scena .pilota-campo')].map((e) => {
                 const r = e.getBoundingClientRect(), s = e.closest('.pilota-scena').getBoundingClientRect();
                 return [e.className.split('--')[1], e.getAttribute('aria-hidden'),
                         Math.round(r.left - s.left) === 0, Math.round(s.right - r.right) === 0]; })"""
        )
        assert fields == [["ma", "true", True, False], ["it", "true", False, True]], (lang, "never mirrored", fields)
        stage_top = page.evaluate("document.querySelector('.pilota-scena').getBoundingClientRect().top")
        head_top = page.evaluate("document.querySelector('.pilota-testa').getBoundingClientRect().top")
        assert stage_top < head_top, "the photographs open the band"
        assert page.evaluate("document.querySelectorAll('.home-pilot .pilota-scena .foto[data-slot]').length") == 2
        drawn = page.evaluate("document.querySelectorAll('.sez-raccordo, .pilota__filo, .panorama__cucitura').length")
        assert drawn == 0
        # S4 → S5 — RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§19, lane B
        # «la chiarezza»): the masonry photograph and its night veil left the trust band — it stands on paper, its two
        # surfaces the material; no veil, no frame behind it, nothing animated on its ground
        assert page.evaluate("document.querySelector('.home-trust .strato--foto')") is None, "no masonry, no veil"
        assert page.evaluate("document.querySelector('.home-trust').dataset.ground") == "paper"
        assert page.evaluate(PSEUDO, [".home-trust", "animationName", "::before"]) == "none"
        # S6 — RESTATED under V5.20 (FINAL HOMEPAGE REBUILD §22, lane B «l'allerta»): the warning is one ochre plate
        # (never red) on the paper that follows the FAQ preview's stone; the pietra's grid is not drawn behind it, no
        # bookend, no sill. The V5.29 bound (≤ 240 px) held a body-only band; the directive's section carries the
        # locked body whole, five red flags and one call. Re-recorded DOWN in the correction round (senior review,
        # 10 Nov 2026: 476 px was too tall): the red flags beside the reading column, the call beside the title — the
        # plate's measure at 1440 in fr was 438 px. RESTATED again under V5.20 for the owner's directive of 10 Nov 2026
        # (FINAL HOMEPAGE REBUILD §22 «short primary warning; progressive disclosure for details», and the owner's
        # correction note «restore a justified compact ceiling»): with the script the body's two middle sentences wait
        # behind «Lire le détail», the lead and the platform's promise in sight, the <p data-locked> still holding the
        # WHOLE body (asserted below, with the opening); the plate measures 345 px, so never more than 350 px
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (points 1 and 4): the warning is
        # the LAST section, a dark warm plate (never ochre, never red) on the light ground that follows the FAQ
        # preview's paper; the same compact ceiling
        assert page.evaluate("document.querySelector('.home-antifraud').dataset.ground") == "stone"
        assert page.evaluate("[...document.querySelectorAll('main > .sez')].pop().dataset.section") == "antifraud"
        assert page.evaluate(PSEUDO, [".home-antifraud", "content", "::before"]) == "none"
        assert page.evaluate("document.querySelector('.home-antifraud .sez-fondale')") is None, "no bookend"
        assert page.evaluate("document.querySelector('.protezione__davanzale')") is None, "no sill"
        band = page.evaluate(RECT, ".home-antifraud .allerta")
        assert band is not None and band["w"] > 0, band
        if lang == "fr":
            assert band["h"] <= 350, ("one plate, never the screen at 1440", band)
            detail = page.evaluate(
                """() => {
                  const p = document.querySelector('.allerta__testo');
                  const b = document.querySelector('[data-allerta-apri]');
                  const seen = () => [...p.querySelectorAll('.ls')].map((e) => e.getClientRects().length > 0);
                  const closed = seen(); b.click();
                  const open = seen(), state = b.getAttribute('aria-expanded'); b.click();
                  const whole = p.textContent === [...p.querySelectorAll('.ls')].map((e) => e.textContent).join('');
                  return {closed, open, state, again: seen(), whole,
                          shown: !b.hidden && b.getClientRects().length > 0}; }"""
            )
            assert detail["closed"] == [True, False, False, True], ("the lead and the promise in sight", detail)
            assert detail["open"] == [True] * 4 and detail["state"] == "true", ("the whole body on demand", detail)
            assert detail["again"] == detail["closed"] and detail["shown"] and detail["whole"], detail
        # S7: carta viva. Amended under V5.20 citing V5.30 §2 (the owner, 7 Nov 2026: one dominant motif per section;
        # the home's arch and its sill's light are retired, docs/design-v5/QA/v530/art/NOTES.md §6–§7): the frame stands
        # plain, with nothing painted behind it, and the section still carries no light of its own.
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§24, lane A): the
        # frame is the media split's
        assert page.evaluate(PSEUDO, [".home-ecosystem .eco-split__media", "content", "::before"]) == "none"
        assert "data-luce" not in page.evaluate("document.querySelector('.home-ecosystem').outerHTML.split('>')[0]")
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") == 0
    finally:
        context.close()

    context = _context(browser, 390, 844, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(live_server.url + f"/{lang}/", wait_until="networkidle")
        # RESTATED under V5.20 (FINAL HOMEPAGE REBUILD, lane B): no sfumatura and no veil at any width
        assert page.evaluate(PSEUDO, [".home-orientation", "content", "::after"]) == "none", "no fade at any width"
        assert page.evaluate("document.querySelectorAll('.sez-raccordo, .pilota__filo').length") == 0
        assert page.evaluate("document.querySelector('.home-trust .strato--foto')") is None, "no veil on phones"
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
        head = "document.querySelector('.home-trust .chiaro__enunciato').getBoundingClientRect().toJSON()"
        title = page.evaluate(head)
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
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§19, lane B «la
        # chiarezza»): the masonry and its night veil left — the band begins on its own paper, the pilot's night ending
        # at the seam: its first row within 1.1 : 1 of the paper the head stands on (no veil, no dissolve left)
        top = shot.getpixel((width // 2, int(band["y"]) + 2))
        assert _contrast(top, paper) <= 1.1, (width, lang, "the band begins on its own paper", top, paper)
        assert page.evaluate("document.querySelector('.home-trust').dataset.ground") == "paper"
    finally:
        context.close()
