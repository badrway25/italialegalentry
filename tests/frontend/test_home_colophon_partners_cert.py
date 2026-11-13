"""
The owner's final certification of 13 Nov 2026 (label v532-cert; «If a test exposes a genuine P0/P1 defect: fix only that
defect, rerun the affected gate»): the home's promoter band stands on AGAMI's night plate since V5.31 and, once a partner
is live AND authorised in writing (G6, ``core.gates.partners_public``), its colophon draws the partners' block — the
«Partenaires» label, each partner's name and «Voir les partenaires» (templates/pages/home/_ecosystem_colophon.html).
axe-core 4.10.2 measured that link at 2.38 : 1 on the band (#0f6a72, the light ground's link colour, on #0e2840):
WCAG 1.4.3 asks 4.5 : 1 of its 15–16 px text. In Chromium, headless (no lock slot), on the seeded site with gate G3 open,
the clock at 3 October 2026 through ``core.clock.now`` (a frozen monotonic clock stalls Playwright) and ONE partner live
and authorised:

* the block is drawn with its link to the partners' index, in French and in Arabic, at 1440, 768 and 390;
* every word of it keeps ≥ 4.5 : 1 against the ground under its box, the text made transparent — held against the pixel
  that gives the LEAST contrast with its ink (the lightest one for a light ink, the darkest one for a dark ink).
"""

from __future__ import annotations

import datetime as dt
import os
from io import BytesIO

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

HEIGHTS = {1440: 900, 768: 1024, 390: 844}
BLOCK = ".home-ecosystem .colofone__partner"
LINK = f"{BLOCK} .colofone__altro a.link-arrow"
#: the partners' block on the band: its label, the partner's name, the link to the index
TEXTS = (f"{BLOCK} .colofone__label", f"{BLOCK} .home-ecosystem__partner-name", LINK)
RECT = (
    "s => { const r = document.querySelector(s).getBoundingClientRect();"
    " return {top: r.top, left: r.left, width: r.width, height: r.height}; }"
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
def partner_live(seeded, set_flag, monkeypatch, legal_published):
    """Gate G3 open and one partner live AND authorised in writing, for the live server, without freezegun."""
    from cms.models import PublicationStatus
    from core import clock, flags
    from partners.models import Partner, PartnerKind

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    Partner.objects.create(
        name="Université de test v532-cert",
        kind=PartnerKind.UNIVERSITY,
        city="Rovigo",
        country="Italie",
        description_fr="Description de test.",
        authorized=True,
        authorization_reference="TEST-ONLY",
        authorized_at=fixed,
        status=PublicationStatus.PUBLISHED,
        published_at=fixed - dt.timedelta(days=1),
    )
    flags.invalidate()
    yield
    flags.invalidate()


def _srgb(channel: float) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _relative(px) -> float:
    return 0.2126 * _srgb(px[0]) + 0.7152 * _srgb(px[1]) + 0.0722 * _srgb(px[2])


def _contrast(a, b) -> float:
    la, lb = _relative(a), _relative(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [1440, 768, 390])
def test_the_home_s_partners_block_keeps_its_words_contrast_on_the_night_band(
    browser, live_server, partner_live, lang, width
):
    context = browser.new_context(viewport={"width": width, "height": HEIGHTS[width]}, reduced_motion="reduce")
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="networkidle")
        drawn = page.evaluate(
            "([block, link]) => [!!document.querySelector(block),"
            " (document.querySelector(link) || {pathname: ''}).pathname,"
            " !!document.querySelector(block) && !!document.querySelector(block).closest('.agami-banda')]",
            [BLOCK, LINK],
        )
        assert drawn[0] and drawn[1] == f"/{lang}/partenaires/" and drawn[2], (
            lang,
            width,
            "the block on the band",
            drawn,
        )
        inks = page.evaluate(
            "ss => ss.map(s => getComputedStyle(document.querySelector(s)).color.match(/[\\d.]+/g).slice(0, 3).map(Number))",
            list(TEXTS),
        )
        # (through the CSSOM: the CSP refuses an inline style sheet)
        page.evaluate(
            "ss => ss.forEach(s => document.querySelectorAll(s + ', ' + s + ' *')"
            ".forEach(el => el.style.setProperty('color', 'transparent', 'important')))",
            list(TEXTS),
        )
        image_module = pytest.importorskip("PIL.Image")
        for selector, ink in zip(TEXTS, inks, strict=True):
            page.evaluate(
                "s => document.querySelector(s).scrollIntoView({block: 'center', behavior: 'instant'})", selector
            )
            page.wait_for_timeout(60)
            box = page.evaluate(RECT, selector)
            assert box["width"] > 0 and box["height"] > 0, (lang, width, selector, box)
            clip = {
                "x": max(0, box["left"]),
                "y": max(0, box["top"]),
                "width": min(box["width"], width),
                "height": box["height"],
            }
            shot = image_module.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")
            worst = min(shot.getdata(), key=lambda pixel, ink=ink: _contrast(ink, pixel))
            assert _contrast(ink, worst) >= 4.5, (lang, width, selector, ink, worst, round(_contrast(ink, worst), 2))
    finally:
        context.close()
