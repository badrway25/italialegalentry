"""
Measure the button system the way its reviewer did: computed styles AND pixels, at rest and
under the pointer, on the page where every variant is on one screen.

    python scripts/qa_chrome_buttons.py                       # /_design/ on 8770
    python scripts/qa_chrome_buttons.py http://127.0.0.1:8770/fr/forum/ .forum-hero

Why pixels and not only computed styles: the defect this exists to catch — a hover layer that
paints over the button's own border — is invisible to getComputedStyle, which reports the border
colour the stylesheet asked for, not the colour the screen shows. So for each measured button the
script screenshots it at rest and on hover and reads the top edge row and two interior rows.

The pointer is moved with `Input.dispatchMouseEvent`, which is a real pointer as far as the page
is concerned: `:hover` matches and `(hover: hover)` media applies, as it does for a mouse.
"""

from __future__ import annotations

import base64
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cdp import CDPError, Page  # noqa: E402

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

DEFAULT_URL = "http://127.0.0.1:8770/_design/"

#: One representative of each variant, as the showcase renders them.
TARGETS = [
    ("primary", "#boutons .ds__row .btn--primary"),
    ("secondary", "#boutons .ds__row .btn--secondary"),
    ("ghost", "#boutons .ds__row .btn--ghost"),
    ("link", "#boutons .ds__row .btn--link"),
    ("danger", "#boutons .ds__row .btn--danger"),
    ("primary sm", "#boutons .btn--sm"),
    ("primary lg", "#boutons .btn--lg"),
    ("primary disabled", "#boutons .btn--primary[disabled]"),
    ("dark primary", ".ds__dark .btn--primary"),
    ("dark secondary", ".ds__dark .btn--secondary"),
    ("dark ghost", ".ds__dark .btn--ghost"),
]

STYLE_JS = """
((selector) => {
  const el = document.querySelector(selector);
  if (!el) return null;
  const s = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  return {
    x: r.x, y: r.y, w: r.width, h: r.height, sx: window.scrollX, sy: window.scrollY,
    bg: s.backgroundColor, fg: s.color, edge: s.borderTopColor, edgeW: s.borderTopWidth,
    img: s.backgroundImage === 'none' ? 'none' : 'gradient',
    shadow: s.boxShadow, radius: s.borderTopLeftRadius, fs: s.fontSize, pad: s.paddingLeft,
    translate: s.translate, opacity: s.opacity, cursor: s.cursor,
  };
})(%s)
"""


def sample(page: Page, rect: dict) -> dict:
    """
    Top edge row, and two interior rows a quarter and three quarters of the way down.

    A CLIPPED capture, not a viewport capture with arithmetic on top: the clip is the element's
    own box at scale 1, so the image is exactly w x h CSS pixels and the sample coordinates are
    local. The first version captured the viewport and multiplied by devicePixelRatio, and the
    first button it measured fell outside the image.
    """
    if Image is None:
        return {}
    clip = {
        "x": rect["x"] + rect["sx"],
        "y": rect["y"] + rect["sy"],
        "width": rect["w"],
        "height": rect["h"],
        "scale": 1,
    }
    data = page.send("Page.captureScreenshot", {"format": "png", "clip": clip, "captureBeyondViewport": True})["data"]
    img = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
    cx = max(0, min(img.width - 1, int(rect["w"] / 2)))

    def px(py: float) -> str:
        r, g, b = img.getpixel((cx, max(0, min(img.height - 1, int(py)))))
        return f"#{r:02x}{g:02x}{b:02x}"

    return {
        "edge": px(0),
        "upper": px(rect["h"] * 0.25),
        "lower": px(rect["h"] * 0.75),
        "img": f"{img.width}x{img.height}",
    }


def measure(page: Page, label: str, selector: str) -> dict | None:
    page.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 2, "y": 2})
    page.send("Runtime.evaluate", {"expression": "document.activeElement && document.activeElement.blur()"})
    rest = page.evaluate(STYLE_JS % json.dumps(selector))
    if not rest:
        return None
    # `behavior: 'instant'`, and it is not optional. The site scrolls smoothly, so a plain
    # scrollIntoView starts a 300ms glide; the rectangle read straight after it is a frame of that
    # glide, and the pointer lands where the button WAS. Measured: the `:hover` chain stopped two
    # elements short of the button on three of eleven targets — the ones that needed a scroll.
    page.evaluate(
        f"(document.querySelector({json.dumps(selector)})).scrollIntoView({{block: 'center', behavior: 'instant'}})",
        await_promise=False,
    )
    page.send(
        "Runtime.evaluate", {"expression": "new Promise(r => requestAnimationFrame(() => r()))", "awaitPromise": True}
    )
    rest = page.evaluate(STYLE_JS % json.dumps(selector))
    rest_px = sample(page, rest)

    page.send(
        "Input.dispatchMouseEvent",
        {"type": "mouseMoved", "x": rest["x"] + rest["w"] / 2, "y": rest["y"] + rest["h"] / 2},
    )
    page.send("Runtime.evaluate", {"expression": "new Promise(r => setTimeout(r, 500))", "awaitPromise": True})
    hovering = page.evaluate("document.querySelectorAll(':hover').length")
    hover = page.evaluate(STYLE_JS % json.dumps(selector))
    hover_px = sample(page, hover)
    page.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 2, "y": 2})

    return {
        "label": label,
        "rest": rest,
        "rest_px": rest_px,
        "hover": hover,
        "hover_px": hover_px,
        "hovering": hovering,
    }


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    url = argv[0] if argv else DEFAULT_URL
    targets = (
        TARGETS if len(argv) < 2 else [(argv[1], argv[1] + " .btn--primary"), (argv[1], argv[1] + " .btn--secondary")]
    )
    try:
        # Any tab on a local dev server, whichever port it is on right now: the tab is navigated
        # to the URL asked for, so what matters is only that it is ours and not the user's.
        with Page.attach(url_contains="127.0.0.1:") as page:
            page.navigate(url, settle=0.4)
            # `Page.navigate` honours the cache, and the dev server sends Last-Modified without
            # Cache-Control, so Chrome keeps a stylesheet heuristically. A reload with
            # ignoreCache is the only way to be sure the sheet on screen is the sheet on disk.
            page.reload(settle=0.8)
            rows = [r for r in (measure(page, label, sel) for label, sel in targets) if r]
    except CDPError as exc:
        print(f"# CDP: {exc}", file=sys.stderr)
        return 2

    print(
        f"{'variant':<18} {'h':>4} {'fill rest→hover (css)':<40} {'edge px':<18} "
        f"{'body px':<18} {'light':<6} {':hover'}"
    )
    problems = 0
    for r in rows:
        a, b = r["rest"], r["hover"]
        # «Boundary lost» is the edge row matching the body row UNDER THE POINTER — the defect the
        # reviewer measured. A translucent edge (the dark secondary's rgba) legitimately shifts a
        # few units when the fill beneath it changes; that is not the boundary going away.
        edge_kept = r["hover_px"].get("edge") != r["hover_px"].get("upper")
        lit = r["hover_px"].get("upper") != r["hover_px"].get("lower")
        print(
            f"{r['label']:<18} {a['h']:>4.0f} {a['bg']:<19}→{b['bg']:<19} "
            f"{r['rest_px'].get('edge', '?')}→{r['hover_px'].get('edge', '?'):<9} "
            f"{r['rest_px'].get('upper', '?')}→{r['hover_px'].get('upper', '?'):<9} "
            f"{'yes' if lit else 'flat':<6} {r['hovering']:>3}  "
            f"{'' if edge_kept or a['edge'] in ('rgba(0, 0, 0, 0)',) else 'EDGE CHANGED'}"
        )
        if a["img"] == "gradient" and not lit and "disabled" not in r["label"]:
            problems += 1
        if a["edgeW"] != "0px" and a["edge"] != "rgba(0, 0, 0, 0)" and not edge_kept:
            problems += 1
    print(f"\n# {problems} rilievi", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
