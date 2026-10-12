"""
At 320px the header must fit, and the menu button must keep its name.

320 is the narrowest width this project claims to support, and until this test existed the browser
lane started at 360 — which is precisely why nobody saw that the toggle was pushed 21px past the
container's padding and clipped by the viewport edge. A width you never render is a width you never
tested.

The two assertions are a pair, and the pair is the point. Making the button fit is trivial: delete
the word. But `.nav-toggle` carries no `aria-label` — its accessible name comes entirely from that
`<span>`, so deleting the word would trade a visual defect for a button a screen reader announces
as nothing at all. The fix has to buy the space and keep the name, so the test demands both.

It measures the RENDERED result rather than the shape of the CSS. The current fix is a media query
that applies the `.visually-hidden` declarations to the span; a future one might restructure the
header entirely. Either passes here, and a fix that silently drops the accessible name does not.

Two things this file got wrong on the first attempt, both of which made it pass against the broken
CSS — a guard that cannot fail is worse than no guard, because it is also a claim:

**It compared against the wrong edge.** The button overran the container's inner edge by 21px but
the viewport's by only 1. Asserting against the viewport made a real 21px defect a 1px one, close
enough to subpixel noise to be argued away. The container's content edge is the edge the design
means by "fits".

**It measured before the fonts had loaded.** With a 300ms wait the word "Menu" was still being
drawn in the fallback face, which is narrower than Fira Sans, so the button fitted by accident.
`document.fonts.ready` is not politeness here; it is the difference between measuring the page and
measuring a stage it passes through.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: 320x568 is the original iPhone SE viewport and the floor of every responsive checklist this
#: project answers to. 305 is what is left of it once Chromium's scrollbar is subtracted, which is
#: the number the layout actually has to live inside.
NARROWEST = {"width": 320, "height": 568}

GEOMETRY_JS = """async () => {
  await document.fonts.ready;
  const button = document.querySelector('[data-nav-toggle]');
  if (!button) return null;
  const inner = button.closest('.site-header__inner') || button.parentElement;
  const innerBox = inner.getBoundingClientRect();
  const padding = parseFloat(getComputedStyle(inner).paddingInlineEnd) || 0;
  const box = button.getBoundingClientRect();
  return {
    // `textContent` is the accessible name here only because there is no aria-label; if one is
    // ever added this test keeps passing for the right reason, since it reads the label first.
    name: (button.getAttribute('aria-label') || button.textContent || '').trim(),
    right: box.right,
    width: box.width,
    height: box.height,
    viewport: document.documentElement.clientWidth,
    // The inner edge of the container's padding — the line the header is laid out against.
    contentEdge: innerBox.right - padding,
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


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_menu_button_fits_and_keeps_its_name_at_320(browser, live_server, seeded, lang):
    context = browser.new_context(viewport=NARROWEST, device_scale_factor=1)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        geometry = page.evaluate(GEOMETRY_JS)
        assert geometry, "no [data-nav-toggle] in the header"

        # Half a pixel of tolerance for subpixel layout, and not one pixel more: the defect this
        # guards was 21px, and rounding it up to a friendlier threshold would let it back in.
        assert geometry["right"] <= geometry["contentEdge"] + 0.5, (
            f"the menu button runs {geometry['right'] - geometry['contentEdge']:.0f}px past the "
            f"container's inner edge at 320 ({lang}); viewport {geometry['viewport']}px"
        )
        assert geometry["name"], (
            "the menu button has no accessible name at 320 — the word was removed rather than "
            "hidden, and a screen reader now announces an unnamed button"
        )
        # WCAG 2.2 §2.5.8: 24px is the floor. Hiding the word must not leave a sliver behind.
        assert geometry["width"] >= 24 and geometry["height"] >= 24, geometry
    finally:
        context.close()


PHONE_ROW_JS = """async () => {
  await document.fonts.ready;
  const rect = (e) => e.getBoundingClientRect();
  const button = document.querySelector('[data-nav-toggle]');
  const inner = button.closest('.site-header__inner');
  const cs = getComputedStyle(inner);
  const ib = rect(inner);
  const rtl = document.documentElement.dir === 'rtl';
  const colEnd = rtl ? ib.left + parseFloat(cs.paddingLeft) : ib.right - parseFloat(cs.paddingRight);
  const b = rect(button);
  const name = document.querySelector('.lock__text');
  const word = button.querySelector('span');
  return {
    past: +(rtl ? colEnd - b.left : b.right - colEnd).toFixed(1),
    nameShown: Boolean(name) && rect(name).width > 2,
    wordShown: Boolean(word) && rect(word).width > 2,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  };
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_name_and_the_menu_button_share_the_phone_row(browser, live_server, seeded, lang):
    """The review's M4, and the arithmetic behind it (chrome.css §1, §3, §7): the brand's name is on screen from
    329 px — 340, 360, 375 and 390 included — and the mark stands alone only at ≤ 20.5rem, where the name (227.5 px)
    and «Menu» (44 px) cannot share the 280 px of a 320 px screen; the button's word returns from 369 px; at every
    width the button ends on the column's edge, never past it, and nothing scrolls sideways."""
    context = browser.new_context(viewport={"width": 390, "height": 740}, device_scale_factor=1)
    try:
        page = context.new_page()
        for width in (320, 328, 329, 340, 360, 368, 369, 375, 390):
            page.set_viewport_size({"width": width, "height": 740})
            page.goto(f"{live_server.url}/{lang}/", wait_until="load")
            row = page.evaluate(PHONE_ROW_JS)
            assert row["past"] <= 0.5, f"«Menu» runs {row['past']} px past the column at {width} ({lang}): {row}"
            assert row["scrollWidth"] <= row["clientWidth"], (width, lang, row)
            assert row["nameShown"] is (width >= 329), (width, lang, row)
            assert row["wordShown"] is (width >= 369), (width, lang, row)
    finally:
        context.close()


def test_nothing_at_all_overflows_the_narrowest_viewport(browser, live_server, seeded):
    """
    The header was the one that showed, not necessarily the only one.

    `scrollWidth` is compared against `clientWidth` rather than asking whether the document
    scrolls, because at this width a single overflowing child is the finding whether or not the
    browser decided to offer a scrollbar for it.
    """
    context = browser.new_context(viewport=NARROWEST, device_scale_factor=1)
    try:
        page = context.new_page()
        for path in ("/fr/", "/fr/parcours/", "/fr/compte/login/", "/ar/"):
            page.goto(live_server.url + path, wait_until="load")
            page.evaluate("async () => { await document.fonts.ready }")
            scroll_w, client_w = page.evaluate(
                "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
            )
            assert scroll_w <= client_w, f"{path} overflows by {scroll_w - client_w}px at 320"
    finally:
        context.close()
