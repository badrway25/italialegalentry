"""
V5.30 §7 (the owner, 7 Nov 2026: «Italy + Morocco: stronger presence on ~3–4 semantically relevant surfaces … ONE reusable
visual primitive with contextual variants … Flags NEVER geometrically mirrored (RTL may change layout order, crop
placement, balance — never the national symbols); reduced motion static; decorative (aria-hidden), contrast kept»; stream A,
label v530-art-build) — the generalised «intesa» (templates/ecosystem/partials/intesa.html, static/css/v5/_intesa.css) in
Chromium, headless (no lock slot), on the seeded site with the gate G3 open and the clock at 3 October 2026 through
`core.clock.now` (a frozen monotonic clock stalls Playwright):

* ONE primitive on its surfaces, each with its variant: the Institutions collaboration head and Réseau's «Pour aller plus
  loin» (campo) — every layer aria-hidden, without text, transparent to the pointer; the home's cooperation moment
  (atmosfera, FINAL MICRO-PASS §5 A3) and the Institutions «Pour aller plus loin» (campo, the micro-pass's review) left;
* in Arabic AND in French the flags are NEVER mirrored: no transform, scale, rotate or translate on either drawing or any
  ancestor, positive screen matrices, the Italian green at the hoist (left of the red), the pentagram upright and unflipped
  — while the PLACEMENT follows the reading edge (Italy at the band's start edge, Morocco's centre on the far half);
* under reduced motion the layer runs no animation (a still composition);
* the home's words keep their contrast ≥ 4.5 : 1 on the composed ground (the darkest pixel under each text box, the text
  made transparent), at 1440, on a tablet (768: below the split the field stands under the words) and at 390, in French
  and in Arabic.
"""

from __future__ import annotations

import datetime as dt
import os
from io import BytesIO

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: path → (the band that carries the layer, its variant). FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the home's
#: «atmosfera» left the home's cooperation band — its blurred fields, lines and pentagram were the band's geometry —, so
#: the home is held apart: no layer of the primitive anywhere in the band, the band's words still there. RESTATED under
#: V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 5: the pentagram's line crossed the closing list's
#: rows and chevrons): the Institutions «Pour aller plus loin» is held apart the same way — no layer in its band, its
#: links still there
# RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D; the
# brief's «no literal flag bands»): Réseau's «Pour aller plus loin» is held apart the same way — no layer in its band,
# its links still there — and a closing band's ground is read on AGAMI's, the closing band that carries the same
# primitive (its default «campo» variant): the same checks, another surface
SURFACES = {
    "collaboration/institutions/": (".intesa-campo", "campo"),
    "agami/": ("section.agami-approdo", "campo"),
}
HEIGHTS = {1440: 900, 1024: 768, 768: 1024, 390: 844}

PROBE = """(band) => {
  const layer = document.querySelector(band + ' > .intesa');
  if (!layer) return null;
  const vw = document.documentElement.clientWidth;
  const it = layer.querySelector('svg[data-flag="it"]'), ma = layer.querySelector('svg[data-flag="ma"]');
  const r = el => el.getBoundingClientRect();
  const screen = (el, x, y) => { const m = el.getScreenCTM(); return [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]; };
  const chain = [];
  for (const start of [it, ma]) {
    for (let el = start; el && el !== document.body; el = el.parentElement) {
      const cs = getComputedStyle(el);
      chain.push([cs.transform, cs.scale, cs.rotate, cs.translate]);
    }
  }
  const star = ma.querySelector('.intesa__stella');
  const pts = star.getAttribute('points').trim().split(/\\s+/).map(p => p.split(',').map(Number)).map(([x, y]) => screen(star, x, y));
  const green = r(it.querySelector('[data-band="verde"]')), red = r(it.querySelector('[data-band="rosso"]'));
  const host = r(layer.parentElement);
  return {
    hidden: layer.getAttribute('aria-hidden'), text: layer.textContent.trim(), pointer: getComputedStyle(layer).pointerEvents,
    cls: layer.className, chain, vw, host: [host.left, host.right],
    itScale: it.getScreenCTM().a, maScale: ma.getScreenCTM().a, starScale: [star.getScreenCTM().a, star.getScreenCTM().d],
    green: [green.left, green.right], red: [red.left, red.right],
    maCentre: (r(ma).left + r(ma).right) / 2, itBox: [r(it).left, r(it).right], pts,
    running: layer.getAnimations({subtree: true}).length,
  };
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


@pytest.fixture
def open_pages(seeded, set_flag, monkeypatch, legal_published):
    """Gate G3 open for the live server without freezegun (a frozen monotonic clock stalls Playwright)."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _assert_unmirrored(state, where, lang, variant):
    assert state is not None, (where, "the primitive stands on its surface")
    assert f"intesa--{variant}" in state["cls"].split(), (where, "its contextual variant", state["cls"])
    assert state["hidden"] == "true" and state["text"] == "" and state["pointer"] == "none", (where, "decorative")
    # THE FLAGS ARE NEVER MIRRORED (V5.29 6 Nov 13:12; V5.30 §7): no transform on the drawings or any ancestor, positive
    # screen matrices, the Italian green at the hoist, the pentagram upright (its first point on top) and unflipped
    assert all(t == ["none", "none", "none", "none"] for t in state["chain"]), (where, state["chain"])
    assert state["itScale"] > 0 and state["maScale"] > 0 and min(state["starScale"]) > 0, where
    assert state["green"][1] <= state["red"][0], (where, "the Italian green at the hoist", state["green"], state["red"])
    top, right_down, left, right, left_down = state["pts"]
    assert top[1] < min(p[1] for p in (right_down, left, right, left_down)), (where, "the pentagram upright")
    assert left[0] < top[0] < right[0] and left_down[0] < right_down[0], (
        where,
        "the pentagram unflipped",
        state["pts"],
    )
    # the PLACEMENT follows the reading edge: Italy at the band's start edge, Morocco's centre on the far half
    start, end = state["host"]
    middle = (start + end) / 2
    if lang == "ar":
        assert abs(state["itBox"][1] - min(end, state["vw"])) <= 1 and state["maCentre"] < middle, (where, state)
    else:
        assert abs(state["itBox"][0] - max(start, 0)) <= 1 and state["maCentre"] > middle, (where, state)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_one_primitive_on_its_surfaces_never_mirrored_and_still_under_reduced_motion(
    browser, live_server, open_pages, lang
):
    for width in (1440, 1024, 390):
        context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, reduced_motion="reduce")
        page = context.new_page()
        try:
            for path, (band, variant) in SURFACES.items():
                page.goto(f"{live_server.url}/{lang}/{path}", wait_until="networkidle")
                state = page.evaluate(PROBE, band)
                where = (lang, width, path or "home")
                _assert_unmirrored(state, where, lang, variant)
                assert state["running"] == 0, (where, "a still composition under reduced motion")
            page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
            home = page.evaluate(
                "() => [document.querySelectorAll('section.home-ecosystem .intesa').length,"
                " document.querySelector('section.home-ecosystem .eco-split__titolo').textContent.trim()]"
            )
            assert home[0] == 0 and home[1], (lang, width, "home", home)
            page.goto(f"{live_server.url}/{lang}/institutions/", wait_until="networkidle")
            band = page.evaluate(
                "() => [document.querySelectorAll('section.ecosistema-approdo .intesa').length,"
                " document.querySelectorAll('section.ecosistema-approdo a.approdo__link').length]"
            )
            assert band[0] == 0 and band[1] >= 2, (lang, width, "institutions/", band)
            # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
            # (lane D)
            page.goto(f"{live_server.url}/{lang}/reseau/", wait_until="networkidle")
            band = page.evaluate(
                "() => [document.querySelectorAll('section.rete-approdo .intesa, .intesa').length,"
                " document.querySelectorAll('section.rete-approdo a.mosaico__link').length]"
            )
            assert band[0] == 0 and band[1] >= 2, (lang, width, "reseau/", band)
        finally:
            context.close()


def _srgb(channel: float) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _relative(px) -> float:
    return 0.2126 * _srgb(px[0]) + 0.7152 * _srgb(px[1]) + 0.0722 * _srgb(px[2])


def _contrast(a, b) -> float:
    la, lb = _relative(a), _relative(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


RECT = (
    "s => { const r = document.querySelector(s).getBoundingClientRect();"
    " return {top: r.top, left: r.left, width: r.width, height: r.height}; }"
)
#: the home's cooperation moment: the head and the promoter's colophon, whose ground the field composes
# RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§24, lane A): the head is the
# media split's
TEXTS = (
    ".home-ecosystem .eco-split__titolo",
    ".home-ecosystem .eco-split__lead",
    ".home-ecosystem .colofone__nome",
    ".home-ecosystem .colofone__testo",
)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 768, 390])
def test_the_home_s_cooperation_moment_keeps_its_words_contrast_on_the_field(
    browser, live_server, open_pages, lang, width
):
    context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
        texts = [s for s in TEXTS if page.evaluate("s => !!document.querySelector(s)", s)]
        assert ".home-ecosystem .colofone__testo" in texts, "the promoter's colophon stands on the field"
        inks = page.evaluate(
            "ss => ss.map(s => getComputedStyle(document.querySelector(s)).color.match(/[\\d.]+/g).slice(0, 3).map(Number))",
            texts,
        )
        # (through the CSSOM: the CSP refuses an inline style sheet)
        page.evaluate(
            "ss => ss.forEach(s => document.querySelectorAll(s + ', ' + s + ' *')"
            ".forEach(el => el.style.setProperty('color', 'transparent', 'important')))",
            texts,
        )
        image_module = pytest.importorskip("PIL.Image")
        for selector, ink in zip(texts, inks, strict=True):
            page.evaluate(
                "s => document.querySelector(s).scrollIntoView({block: 'center', behavior: 'instant'})", selector
            )
            page.wait_for_timeout(60)
            box = page.evaluate(RECT, selector)
            clip = {
                "x": max(0, box["left"]),
                "y": max(0, box["top"]),
                "width": min(box["width"], width),
                "height": box["height"],
            }
            shot = image_module.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
            darkest = min(shot.getdata(), key=_relative)
            assert _contrast(ink, darkest) >= 4.5, (
                lang,
                width,
                selector,
                ink,
                darkest,
                round(_contrast(ink, darkest), 2),
            )
    finally:
        context.close()
