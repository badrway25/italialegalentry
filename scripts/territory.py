"""
Draw the territory: two shores as contour clusters, a fine graticule, a route between them.

    python scripts/territory.py

Writes SVG *inner* markup (no <svg> root — the template supplies it, with the viewBox and the
accessibility attributes) as Django includes:

    templates/pages/home/partials/territory_hero_base.svg      graticule, ticks, route, stations
    templates/pages/home/partials/territory_hero_layer-1.svg   contour layer 1 (masked)
    templates/pages/home/partials/territory_hero_layer-2.svg   contour layer 2 (masked)
    templates/portal/partials/territory_band_base.svg
    templates/portal/partials/territory_band_layer-1.svg

Versioned, because the drawing is part of the design and a reviewer must be able to diff it.

One file per contour layer is not tidiness. The layers are what drifts (the "tide"), and a `<g>`
moved inside one big SVG — by CSS or by JavaScript — repaints the whole SVG on every frame: the
Council measured 162 paints in three seconds and 27 fps on the prototype that did exactly that. A
separate `<svg>` element per layer, positioned absolutely and moved with a CSS transform, is a
compositor layer, and the tide then costs no paint at all.

Deterministic on purpose: a fixed seed and a tiny generator rather than `random`, so the same
script on any machine produces byte-identical output and the lines are the ones the Council saw.
Never a literal map — no coastlines, no borders, no flags. The two ridges sit north-east and
south-west because that is where Veneto and Morocco are relative to each other, and the route
between them is the only line with a direction. Ported from the direction-C prototype.
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERO_DIR = ROOT / "templates" / "pages" / "home" / "partials"
BAND_DIR = ROOT / "templates" / "portal" / "partials"


def rng(seed: int):
    """mulberry32 — small, deterministic, and the same sequence the prototype used."""
    a = seed & 0xFFFFFFFF

    def nxt() -> float:
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = (a ^ (a >> 15)) * (1 | a) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296

    return nxt


def r1(n: float) -> str:
    return f"{n:.1f}".rstrip("0").rstrip(".")


def to_path(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom through the points, emitted as cubic Béziers — smooth without overshoot."""
    d = f"M{r1(pts[0][0])} {r1(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{r1(c1[0])} {r1(c1[1])} {r1(c2[0])} {r1(c2[1])} {r1(p2[0])} {r1(p2[1])}"
    return d


def contours(width, height, focals, seed, *, layers=2, count=14, step=48, margin=80):
    """Contour lines displaced by Gaussian ridges plus three low harmonics, one list per layer."""
    out = []
    for li in range(layers):
        g = rng(seed * 2654435761 + li * 40503 + 17)
        harmonics = [
            (0.0028 + g() * 0.0046, (5 + g() * 8) * (1 - li * 0.12), g() * math.tau, (g() - 0.5) * 0.01)
            for _ in range(3)
        ]
        n = max(5, round(count * (1 - li * 0.08)))
        spacing = (height + margin * 2) / n
        paths = []
        for k in range(n):
            base_y = -margin + spacing * (k + 0.5) + (g() - 0.5) * 6
            pts = []
            x = -margin
            while x <= width + margin:
                dsp = 0.0
                for fx, fy, amp, sx, sy in focals:
                    dx = x - fx
                    dy = base_y - fy
                    ex = math.exp(-(dx * dx) / (2 * sx * sx))
                    vy = math.exp(-(dy * dy) / (2 * sy * sy))
                    direction = 1 if dy >= 0 else -1
                    dsp += amp * ex * (0.52 + 0.48 * vy * direction) * (1 - li * 0.14)
                for f, a, p, gg in harmonics:
                    dsp += a * math.sin(x * f + p + base_y * gg)
                pts.append((x, base_y - dsp))
                x += step
            paths.append(to_path(pts))
        out.append(paths)
    return out


def mask_defs(width, height, safe, name) -> str:
    """The "safe area": contour lines fade under the text column so type never fights the map."""
    sx, sy, sw, sh = safe
    return (
        "<defs>"
        f'<radialGradient id="{name}-safe" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#2a2a2a"/><stop offset="60%" stop-color="#8a8a8a"/>'
        '<stop offset="100%" stop-color="#fff"/></radialGradient>'
        f'<mask id="{name}-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="{width}" height="{height}">'
        f'<rect width="{width}" height="{height}" fill="#fff"/>'
        f'<ellipse cx="{r1((sx + sw / 2) * width)}" cy="{r1((sy + sh / 2) * height)}" '
        f'rx="{r1(sw / 2 * width * 1.15)}" ry="{r1(sh / 2 * height * 1.15)}" fill="url(#{name}-safe)"/>'
        "</mask></defs>\n"
    )


def build(width, height, focals, seed, route, stations, safe, name, *, graticule=160, count=14, layers=2):
    """{"base": …, "layer-1": …, "layer-2": …} — see the module docstring for why they are apart."""
    base = ['<g class="terr__grid">']
    x = graticule
    while x < width:
        base.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}"/>')
        x += graticule
    y = graticule
    while y < height:
        base.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}"/>')
        y += graticule
    base.append("</g>")
    base.append('<g class="terr__ticks">')
    x = graticule
    while x < width:
        y = graticule
        while y < height:
            base.append(f'<path d="M{x - 4} {y}h8M{x} {y - 4}v8"/>')
            y += graticule
        x += graticule
    base.append("</g>")
    if route:
        base.append(f'<path class="terr__route" pathLength="1" d="{route}"/>')
        base.append('<g class="terr__stations">')
        for cx, cy in stations:
            base.append(
                f'<g class="terr__station"><circle cx="{cx}" cy="{cy}" r="10" class="terr__halo"/>'
                f'<circle cx="{cx}" cy="{cy}" r="3.5" class="terr__dot"/></g>'
            )
        base.append("</g>")
    out = {"base": "\n".join(base) + "\n"}

    for li, paths in enumerate(contours(width, height, focals, seed, count=count, layers=layers), start=1):
        # ids must be unique per document and every layer file carries its own mask.
        layer = [mask_defs(width, height, safe, f"{name}-{li}")]
        layer.append(f'<g class="terr__layer terr__layer--{li}" mask="url(#{name}-{li}-mask)">')
        layer.extend(f'<path d="{d}"/>' for d in paths)
        layer.append("</g>")
        out[f"layer-{li}"] = "\n".join(layer) + "\n"
    return out


def write(parts: dict[str, str], directory: Path, stem: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for key, markup in parts.items():
        path = directory / f"{stem}_{key}.svg"
        path.write_text(markup, encoding="utf-8")
        print(f"{path.relative_to(ROOT).as_posix()}  {path.stat().st_size / 1024:.1f} KB")


def main() -> int:
    # HERO 1440 × 820 — south shore bottom-left, north shore top-right; the route enters behind the
    # doorway (station 4 sits at its left shoulder) and re-emerges past the crown (stations 5–6).
    w, h = 1440, 820
    focals = [(w * 0.86, h * 0.16, 84, 250, 160), (w * 0.10, h * 0.94, 76, 270, 170)]
    stations = [(150, 760), (430, 735), (680, 660), (900, 585), (1270, 215), (1370, 110)]
    route = to_path([(-40, 766)] + stations[:4] + [(1100, 470)] + stations[4:] + [(1440, 60)])
    write(build(w, h, focals, 7, route, stations, safe=(0.03, 0.14, 0.54, 0.74), name="hero"),
          HERO_DIR, "territory_hero")

    # PLATFORM BAND 1440 × 260 — quieter: one ridge on the end side, no route, one still layer.
    w, h = 1440, 260
    write(build(w, h, [(w * 0.88, h * 0.35, 40, 260, 90)], 11, None, None,
                safe=(0.0, 0.0, 0.62, 1.0), name="band", graticule=120, count=9, layers=1),
          BAND_DIR, "territory_band")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
