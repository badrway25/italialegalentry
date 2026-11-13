"""
Write `static/img/favicon.ico` from the same geometry as `static/img/favicon.svg`.

Chrome asks for `/favicon.ico` whatever else a page declares, so a site that ships only an SVG icon
logs a 404 in the console of **every page, in every session**. The pre-production directive forbids
exactly that: «nei principali flussi non devono restare 404 asset».

A redirect from `/favicon.ico` to the SVG would silence it too, and it would be worse: an extra
round trip on every first page load, and a file type the probe did not ask for. This writes the
real thing.

The geometry is duplicated here from the SVG rather than rasterised from it, because rasterising
SVG needs a renderer this project does not depend on, and the shape is four primitives:

    a rounded navy square, a cream rule near the foot, three white uprights.

If the mark changes, change both — and the test in `tests/frontend/test_favicon.py` fails until the
two agree on size and palette.

    python scripts/make_favicon_ico.py
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "static" / "img" / "favicon.svg"
ICO = ROOT / "static" / "img" / "favicon.ico"

#: Rendered at 4x and downsampled, so the 1.5px rule and the rounded corner survive at 16px.
SCALE = 8
SIZES = [(16, 16), (32, 32), (48, 48)]


def palette() -> dict[str, str]:
    """Read the colours out of the SVG, so the two cannot drift apart silently."""
    svg = SVG.read_text(encoding="utf-8")
    fills = re.findall(r'fill="(#[0-9a-fA-F]{6})"', svg)
    strokes = re.findall(r'stroke="(#[0-9a-fA-F]{6})"', svg)
    return {"ground": fills[0], "rule": strokes[0], "uprights": strokes[1]}


def draw(size: int, colours: dict[str, str]) -> Image.Image:
    s = size * SCALE
    unit = s / 32  # the SVG's own 32-unit viewBox
    image = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    pen = ImageDraw.Draw(image)

    pen.rounded_rectangle([0, 0, s - 1, s - 1], radius=4 * unit, fill=colours["ground"])
    pen.line(
        [(8 * unit, 22.5 * unit), (24 * unit, 22.5 * unit)],
        fill=colours["rule"],
        width=max(1, round(1.5 * unit)),
    )
    for x in (11, 16, 21):
        pen.line(
            [(x * unit, 9 * unit), (x * unit, 19 * unit)],
            fill=colours["uprights"],
            width=max(1, round(2 * unit)),
        )
    return image.resize((size, size), Image.LANCZOS)


def main() -> int:
    colours = palette()
    # Pillow's ICO writer builds every entry from the ONE image it is given, resizing it to each
    # entry in `sizes`. Passing a list through `append_images` looks right and silently produces a
    # single 16px frame — verified by reopening the file, which is the only way to notice.
    largest = draw(max(w for w, _ in SIZES), colours)
    largest.save(ICO, format="ICO", sizes=SIZES)

    written = sorted(Image.open(ICO).ico.sizes())
    if written != sorted(SIZES):
        raise SystemExit(f"expected {sorted(SIZES)} in the .ico, found {written}")
    print(f"{ICO.relative_to(ROOT).as_posix()}  {ICO.stat().st_size} B  sizes={[s[0] for s in written]}")
    print(f"palette from the SVG: {colours}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
