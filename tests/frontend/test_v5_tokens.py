"""
Design V5 tokens — the foundation W1-A wires (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.1–§1.6, §1.8, §2.3).

`static/css/v5/` closes the cascade of `static/css/main.css`: a value declared there is the value every
earlier layer ends up with, and `static/css/v5/aliases.css` gives the V1 / V2 / V4 names their V5 values
(architecture A, «in place, alias-first», plan §2.1). These tests read the cascade the way the browser does
— in main.css order, the last top-level `:root` declaration wins — and hold:

* the order (v5 closes the cascade) and the five self-hosted faces of type «Una voce» (§1.1);
* the type system: one family, the wordmark, ILE Mono, Vazirmatn; eight public sizes; line-heights on the
  4 px line; nothing under 12 px Latin or 14 px Arabic; typed text 16 px; measures in rem; the console one
  step up on phones;
* colour (§1.2): «En examen» in lapis and no violet left; the broken edges and the hatch at 3 : 1; the night
  marks re-solved (0 of 28 pairs under 0.05 in any of four visions); the glass at α 0.94; ≥ 400 contrast
  pairs recomputed from the effective cascade, 0 below their minimum;
* PLATFORM_COLORS D-doc-6 (night separation; edges and patterns at 3 : 1; plates and glass over night; the tones on
  the selected and disabled surfaces) and PC §6.3's 23 pairs below their minimum, each answered by a token or kept
  off every page by a rule written in DESIGN_SYSTEM_2026.md §5;
* corners «Lo spigolo» (§1.3), five shadow levels in the night's own colour (SH-1), flat primaries (§1.4);
* the brand colours declared once (in v2/tokens.css), no literal colour outside the token sheets and no register
  painted green or with the accent — in every V5 sheet: main.css's four, the page partials, the console partials;
  and the console partials close the console entry as v5/* closes main.css (plan §2.3, §2.7);
* the documents: the css blocks and the contrast tables of DESIGN_SYSTEM_2026.md (§5, §6, §7), and the bytes and
  hashes of docs/design-v5/FONTS_V5.md, are the files' and the cascade's.

Retired into this file from tests/frontend/test_v4_tokens.py (the cascade order, the Plex faces, the V4 pairs, the
six shadow roles) and tests/frontend/test_static_assets.py (the V1 contrast pairs: values no page renders any more).
Fast and offline: files on disk only.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import posixpath
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
V5 = STATIC / "css" / "v5"
#: Console-only V5 CSS: `_`-prefixed partials imported by the console entry, never by main.css (plan §2.3).
PORTAL_V5 = ROOT / "apps" / "portal" / "static" / "portal" / "v5"
CONSOLE_ENTRY = ROOT / "apps" / "portal" / "static" / "portal" / "console.css"
DS2026 = ROOT / "docs" / "design" / "DESIGN_SYSTEM_2026.md"
FONTS_DOC = ROOT / "docs" / "design-v5" / "FONTS_V5.md"

pytestmark = pytest.mark.compliance


# ---- the effective cascade ------------------------------------------------------------------------


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _cascade() -> list[str]:
    return re.findall(r'@import url\("([^"]+)"\)', _read(STATIC / "css" / "main.css"))


def _root_declarations(css: str) -> dict[str, str]:
    """The `--name: value` pairs of the TOP-LEVEL :root blocks (a :root inside a media query is indented)."""
    found: dict[str, str] = {}
    for block in re.findall(r"^:root\s*\{(.*?)^\}", _strip_comments(css), flags=re.M | re.S):
        for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", block):
            found[name] = " ".join(value.split())
    return found


def _effective() -> dict[str, str]:
    tokens: dict[str, str] = {}
    for sheet in _cascade():
        tokens.update(_root_declarations(_read(STATIC / "css" / sheet)))
    return tokens


TOKENS = _effective()


def _resolve(value: str, depth: int = 0) -> str:
    assert depth < 12, value
    value = value.strip()
    m = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value)
    return _resolve(TOKENS[m.group(1)], depth + 1) if m else value


def _token(name: str) -> str:
    return _resolve(TOKENS[name])


# ---- colour arithmetic (WCAG 2.x; OKLab and Machado 2009 for the separation) ------------------------


def _rgba(value: str) -> tuple[float, float, float, float]:
    value = value.strip()
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([0-9.]+))?\s*\)", value)
    assert m, value
    return int(m[1]), int(m[2]), int(m[3]), float(m[4] or 1)


def _over(fg: str, bg: str) -> str:
    r, g, b, a = _rgba(fg)
    br, bg_, bb, _ = _rgba(bg)
    return "#{:02x}{:02x}{:02x}".format(*(round(c * a + d * (1 - a)) for c, d in ((r, br), (g, bg_), (b, bb))))


def _luminance(colour: str) -> float:
    def channel(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b, _ = _rgba(colour)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast(fg: str, bg: str) -> float:
    """fg may carry alpha: it is composited over bg first (what the eye meets)."""
    l1, l2 = _luminance(_over(fg, bg)), _luminance(_over(bg, "#000000"))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _colour(spec: str) -> str:
    """A token, a literal, or «layer|ground»: a translucent layer composited on a ground."""
    if "|" in spec:
        layer, ground = spec.split("|")
        return _over(_colour(layer), _colour(ground))
    return _token(spec) if spec.startswith("--") else spec


#: Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB — the model PLATFORM_COLORS used
#: (its rendered and computed figures agree within ΔE 0.004).
_MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def _oklab(colour: str, vision: str = "normal") -> tuple[float, float, float]:
    def lin(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b, _ = _rgba(colour)
    rgb = (lin(r), lin(g), lin(b))
    if vision != "normal":
        m = _MACHADO[vision]
        rgb = tuple(min(1.0, max(0.0, sum(m[i][j] * rgb[j] for j in range(3)))) for i in range(3))
    r, g, b = rgb
    lms = (
        0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
        0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
        0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b,
    )
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in lms)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _weak_pairs(colours: dict[str, str], threshold: float = 0.05) -> set[tuple[str, str, str]]:
    weak = set()
    for (na, a), (nb, b) in itertools.combinations(colours.items(), 2):
        for vision in ("normal", "protan", "deutan", "tritan"):
            if math.dist(_oklab(a, vision), _oklab(b, vision)) < threshold:
                weak.add((na, nb, vision))
    return weak


REGISTERS = ("conforme", "esame", "neutro", "attesa", "azione", "rifiuto", "blocco", "nullo")


# ---- the order and the faces ------------------------------------------------------------------------


def test_v5_closes_the_cascade_and_reaches_the_browser_in_the_bundle():
    imports = _cascade()
    first = imports.index("v5/fonts.css")
    v5 = imports[first:]
    # the foundation's four sheets first; after them only V5 sheets, the families' (chrome.css, W2-C1 …), plan §2.3
    assert v5[:4] == ["v5/fonts.css", "v5/tokens.css", "v5/aliases.css", "v5/base.css"], v5
    assert all(name.startswith("v5/") for name in v5), v5
    assert not any(name.startswith("v5/") for name in imports[:first])
    assert imports[first - 1].startswith("v4/"), "the V5 block follows the V4 layers it re-values"
    assert "fonts.css" not in imports
    bundle = _read(STATIC / "css" / "dist" / "main.css")
    for family in ("Host Grotesk", "ILE Wordmark", "ILE Mono", "Vazirmatn"):
        # esbuild drops the quotes of a family name it can leave bare
        assert re.search(r'@font-face\{font-family:"?' + re.escape(family) + r'"?;', bundle), family
    assert "{% static 'css/dist/main.css' %}" in _read(ROOT / "templates" / "base.html")


def test_the_five_faces_are_self_hosted_with_their_licences():
    fonts = _strip_comments(_read(V5 / "fonts.css"))
    faces = re.findall(r"@font-face\s*\{([^}]*)\}", fonts)
    web = [f for f in faces if "url(" in f]
    assert len(web) == 6, "five faces, six files: ILE Mono's reference core and the rest"
    declared = {}
    for face in web:
        family = re.search(r'font-family:\s*"([^"]+)"', face).group(1)
        url = re.search(r'url\("\.\./\.\./fonts/([a-z0-9-]+\.woff2)"\)', face).group(1)
        assert (STATIC / "fonts" / url).exists(), url
        assert "font-display: swap" in face and "unicode-range" in face, family
        declared.setdefault(family, []).append(url)
    assert sorted(declared) == ["Host Grotesk", "ILE Mono", "ILE Wordmark", "Vazirmatn"]
    assert len(declared["Host Grotesk"]) == 2, "roman variable 400–700 and italic 400"
    assert sorted(declared["ILE Mono"]) == ["v5-ile-mono-400-ext.woff2", "v5-ile-mono-400.woff2"]
    assert {p.name for p in (STATIC / "fonts").glob("*.woff2")} == {u for urls in declared.values() for u in urls}
    assert not list((STATIC / "fonts").glob("ibm-plex-*")) and not list((STATIC / "fonts").glob("newsreader-*"))
    assert not (STATIC / "css" / "fonts.css").exists()
    # every fallback face is local(): nothing is fetched from another host
    for face in faces:
        if "url(" not in face:
            assert "local(" in face and "size-adjust" in face and "ascent-override" in face, face
    licences = {p.name for p in (STATIC / "fonts" / "licenses").glob("*.txt")}
    assert licences == {"OFL-HostGrotesk.txt", "OFL-Newsreader.txt", "OFL-IBMPlexMono.txt", "OFL-Vazirmatn.txt"}
    assert 'Reserved Font Name "Plex"' in _read(STATIC / "fonts" / "licenses" / "OFL-IBMPlexMono.txt")
    assert (ROOT / "docs" / "design-v5" / "FONTS_V5.md").exists()


def test_the_matched_fallbacks_cover_windows_apple_through_arial_and_android():
    fonts = _strip_comments(_read(V5 / "fonts.css"))
    for family, source in (
        ("ILE Sans Fallback", 'local("Segoe UI")'),
        ("ILE Sans Fallback Arial", 'local("Arial")'),
        ("ILE Sans Fallback Android", 'local("Roboto")'),
        ("ILE Arabic Fallback", 'local("Segoe UI")'),
        ("ILE Wordmark Fallback", 'local("Georgia")'),
        ("ILE Mono Fallback", 'local("Consolas")'),
    ):
        face = re.search(r'@font-face\s*\{[^}]*font-family:\s*"' + re.escape(family) + r'";[^}]*\}', fonts)
        assert face and source in face.group(0), family
    sans = _token("--f-sans-lat")
    assert (
        sans.index('"ILE Sans Fallback"')
        < sans.index('"ILE Sans Fallback Arial"')
        < sans.index('"ILE Sans Fallback Android"')
    )


# ---- the type system «Una voce» ---------------------------------------------------------------------


def test_one_family_the_wordmark_ile_mono_and_vazirmatn():
    assert _token("--f-sans").startswith('"Host Grotesk", "ILE Sans Fallback"')
    assert _token("--f-serif") == _token("--f-sans"), "every serif role takes the sans (DL54-10)"
    assert _token("--f-mono").startswith('"ILE Mono", "ILE Mono Fallback"')
    assert _token("--f-wordmark").startswith('"ILE Wordmark", "ILE Wordmark Fallback"')
    assert _token("--f-sans-ar").startswith('"Vazirmatn", "Host Grotesk", "ILE Arabic Fallback"')
    # the legacy names follow (static/css/v5/aliases.css)
    for legacy in ("--font-display", "--font-ui"):
        assert _token(legacy) == _token("--f-sans-lat"), legacy
    for legacy in ("--font-ref", "--font-mono"):
        assert _token(legacy) == _token("--f-mono"), legacy
    for legacy in ("--font-display-ar", "--font-ui-ar"):
        assert _token(legacy) == _token("--f-sans-ar"), legacy
    stacks = " ".join(_token(n) for n in ("--f-sans", "--f-serif", "--f-mono", "--f-wordmark", "--f-sans-ar"))
    for retired in ("Plex", "Newsreader", "Naskh", "Fira", "Source Serif", "Markazi"):
        assert retired not in stacks, retired


def test_every_rendering_of_the_name_is_the_wordmark_and_ile_mono_has_one_seat():
    base = _strip_comments(_read(V5 / "base.css"))
    name = re.search(r":root :is\(([^)]*\[translate=\"no\"\])\)\s*\{([^}]*)\}", base)
    assert name, "no rule for the name"
    for cls in (
        ".lock__wm",
        ".brand__wordmark",
        ".home__wordmark",
        ".page-header__wordmark",
        ".site-footer__wordmark-inline",
        ".rail__wm",
        ".rail__wordmark",
    ):
        assert cls in name.group(1), cls
    assert "font-family: var(--f-wordmark)" in name.group(2) and "text-transform: uppercase" in name.group(2)
    seat = re.search(r":root :is\((\.site-footer__heading[^)]*)\)\s*\{([^}]*)\}", base)
    assert seat and "font-family: var(--f-sans)" in seat.group(2), "the legacy mono labels take the sans"


def test_the_public_scale_has_eight_sizes():
    def px(name: str) -> float:
        value = _token(name)
        m = re.fullmatch(r"([0-9.]+)rem", value)
        assert m, (name, value)
        return float(m[1]) * 16

    display = _token("--t-display")
    m = re.fullmatch(r"clamp\(([0-9.]+)rem, [^,]+, ([0-9.]+)rem\)", display)
    assert m and float(m[1]) * 16 == 40 and float(m[2]) * 16 == 64, display
    sizes = {64.0, 40.0} | {
        px(n)
        for n in (
            "--t-title",
            "--t-band",
            "--t-entry",
            "--t-lead",
            "--t-body",
            "--t-ui",
            "--t-small",
            "--t-caption",
            "--t-folio",
        )
    }
    assert sizes - {40.0} == {64.0, 36.0, 28.0, 20.0, 17.0, 15.0, 13.0, 12.0}, sorted(sizes)
    assert _token("--t-plate") == display, "no ninth size: the plate is the display"
    # V1's ten roles land on the same eight
    v1 = {
        "--t-title-size": 36,
        "--t-band-size": 28,
        "--t-entry-size": 20,
        "--t-lead-size": 20,
        "--t-prose-size": 17,
        "--t-gloss-size": 15,
        "--t-caption-size": 13,
        "--t-ui-size": 15,
        "--t-folio-size": 13,
    }
    for name, size in v1.items():
        assert px(name) == size, name
    assert _token("--t-plate-size") == display


def test_line_heights_sit_on_the_4px_line():
    offenders = []
    for name, value in TOKENS.items():
        if not name.endswith("-lh"):
            continue
        resolved = _resolve(value)
        m = re.fullmatch(r"([0-9.]+)(rem|px)", resolved)
        if not m:
            continue  # unitless ratios (the display line) are checked by eye on stills
        px = float(m[1]) * (16 if m[2] == "rem" else 1)
        if abs(px / 4 - round(px / 4)) > 0.01:
            offenders.append(f"{name}: {px}px")
    assert offenders == [], offenders


def test_nothing_under_12px_latin_14px_arabic_and_typed_text_16px():
    for name in ("--t-caption", "--t-small", "--t-folio", "--u-caption", "--u-small", "--u-eyebrow", "--u-ref"):
        assert float(_token(name).removesuffix("rem")) * 16 >= 12, name
    assert _token("--u-eyebrow") == "0.75rem", "the eyebrow rises from 11 to 12 px (TR C5)"
    v5 = _strip_comments(_read(V5 / "tokens.css"))
    arabic = re.search(r"(?m)^:lang\(ar\)\s*\{([^}]*)\}", v5).group(1)
    for name in ("--t-small", "--t-caption", "--t-folio", "--u-small", "--u-caption", "--u-eyebrow"):
        value = re.search(re.escape(name) + r":\s*([0-9.]+)rem", arabic)
        assert value and float(value[1]) * 16 >= 14, name
    assert _token("--t-field") == "1rem"
    base = _strip_comments(_read(V5 / "base.css"))
    assert re.search(r"textarea, select\)\s*\{\s*font-size: var\(--t-field\) !important;", base)


def test_the_console_steps_up_below_48rem_and_under_a_coarse_pointer():
    v5 = _strip_comments(_read(V5 / "tokens.css"))
    block = re.search(r"@media \(max-width: 47\.999rem\), \(pointer: coarse\)\s*\{\s*body\.console\s*\{([^}]*)\}", v5)
    assert block, "no console step-up"
    steps = dict(re.findall(r"(--u-[a-z]+)\s*:\s*([^;]+);", block.group(1)))
    assert steps["--u-body"] == "1rem" and steps["--u-ui"] == "0.9375rem" and steps["--u-small"] == "0.875rem"
    assert steps["--u-caption"] == "0.8125rem" and steps["--u-eyebrow"] == "0.75rem"


def test_measures_are_in_rem():
    assert _token("--measure-body") == "36rem" and _token("--measure-small") == "29rem"
    assert _token("--measure-prose") == "36rem" and _token("--measure-gloss") == "29rem"
    assert "ch" not in _token("--measure-lead")


def test_the_narrow_overrides_of_the_names_v5_declares_are_restated():
    """A top-level :root here beats an earlier :root inside a media query: v4's narrow block is restated."""
    v5 = _strip_comments(_read(V5 / "tokens.css"))
    narrow = re.search(r"@media \(max-width: 47\.999rem\)\s*\{\s*:root\s*\{(.*?)\}", v5, flags=re.S)
    assert narrow
    body = " ".join(narrow.group(1).split())
    for declaration in ("--page-pad: 16px;", "--utility-h: 0px;", "--header-h: 56px;", "--u-title: 1.5rem;"):
        assert declaration in body, declaration
    # The reduced-motion block is restated here too: test_reduced_motion_is_a_state_every_duration_lands_at_zero.
    assert _token("--ease-turn") == "cubic-bezier(0.77, 0, 0.175, 1)"
    assert "--ease-turn-in" not in TOKENS or "--ease-turn-in" not in _root_declarations(_read(V5 / "tokens.css"))


# ---- reduced motion, a state (plan §1.5, W1-D; retired here from test_v4_tokens.py) --------------------

#: Time-valued names that keep their value under reduced motion. Thresholds are not motion (RM-4): the tooltip
#: still waits, a menu keeps its intent and its grace, a toast its time. --motion-reduced is the one 80 ms
#: opacity an overlay may keep (MS-O4, RM-1). --motion-ambient is V4's loop: it plays only under no-preference
#: (v4/hero.css) and leaves with that sheet (W2-D).
REDUCED_MOTION_KEEPS = (
    "--motion-wait",
    "--tooltip-delay",
    "--panel-hover-intent",
    "--panel-grace",
    "--toast-timeout",
    "--motion-reduced",
    "--motion-ambient",
)
_REDUCED_BLOCK = r"@media \(prefers-reduced-motion: reduce\)\s*\{"


def _effective_under_reduced_motion() -> dict[str, str]:
    """The cascade as the setting sees it: in each sheet its top-level :root blocks and the :root of its
    reduced-motion media query, in source order — one specificity, so the later wins."""
    tokens: dict[str, str] = {}
    for sheet in _cascade():
        css = _strip_comments(_read(STATIC / "css" / sheet))
        blocks = [(m.start(), m.group(1)) for m in re.finditer(r"^:root\s*\{(.*?)^\}", css, flags=re.M | re.S)]
        blocks += [(m.start(), m.group(1)) for m in re.finditer(_REDUCED_BLOCK + r"\s*:root\s*\{([^}]*)\}", css)]
        for _, body in sorted(blocks):
            for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", body):
                tokens[name] = " ".join(value.split())
    return tokens


def _resolved(name: str, table: dict[str, str], depth: int = 0) -> str:
    assert depth < 12, name
    value = table[name].strip()
    m = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value)
    return _resolved(m.group(1), table, depth + 1) if m else value


def _delivered_sheets() -> list[Path]:
    return [STATIC / "css" / sheet for sheet in _cascade()] + sorted(ROOT.glob("apps/*/static/**/*.css"))


def _reduced_motion_blocks(css: str) -> tuple[list[str], str]:
    """The bodies of the reduced-motion media blocks (brace-matched) and the sheet without them."""
    bodies, rest, cursor = [], [], 0
    for m in re.finditer(_REDUCED_BLOCK, css):
        if m.start() < cursor:
            continue
        depth, i = 1, m.end()
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        rest.append(css[cursor : m.start()])
        bodies.append(css[m.end() : i - 1])
        cursor = i
    rest.append(css[cursor:])
    return bodies, "".join(rest)


def test_reduced_motion_is_a_state_every_duration_lands_at_zero():
    """V1's universal `0.01ms !important` switch is gone (components.css, W1-D): under the setting every duration
    token resolves to 0 ms — the key, the door, the light and the staggers included, since nothing in V5 loops — so
    each transition and animation written on a token lands at once. Thresholds and --motion-reduced keep theirs."""
    rest, reduced = TOKENS, _effective_under_reduced_motion()
    timed = [
        name
        for name in rest
        if re.fullmatch(r"\d*\.?\d+m?s", _resolved(name, rest)) and float(re.sub("m?s", "", _resolved(name, rest))) > 0
    ]
    assert {"--motion-fast", "--motion-key", "--motion-luce", "--motion-stagger", "--spring-sheet-duration"} <= set(
        timed
    )
    for name in timed:
        if name in REDUCED_MOTION_KEEPS:
            assert _resolved(name, reduced) == _resolved(name, rest), f"{name} is a threshold: it keeps its value"
        else:
            assert _resolved(name, reduced) == "0ms", (
                f"{name} still moves under reduced motion: zero it in v5/tokens.css"
            )
    assert _resolved("--motion-reduced", reduced) == "80ms"
    # The legacy names reach the zero through their aliases (they were V4's pin, test_v4_tokens.py:90).
    assert rest["--motion-instant"] == "var(--motion-fast)" and rest["--motion-base"] == "var(--motion-standard)"
    for legacy in ("--duration-fast", "--duration-base", "--duration-slow", "--motion-instant", "--motion-base"):
        assert _resolved(legacy, reduced) == "0ms", legacy


def test_no_sheet_forces_a_duration_and_motion_reduced_only_fades():
    """The switch does not come back in another form: no `!important` on a transition or an animation, no
    universal selector in a reduced-motion block; and --motion-reduced is read inside a reduced-motion block
    only, by an opacity transition only (MS-O4, RM-1: «an 80 ms opacity ramp contains no movement»). The fade of a
    surface that leaves the display may carry its discrete companion — `display` or `overlay` with
    `allow-discrete`, for the same 80 ms (the portico, v5/chrome.css §9): a property that does not interpolate
    keeps the surface in place while its opacity goes, and draws nothing of its own."""
    for sheet in _delivered_sheets():
        css = _strip_comments(_read(sheet))
        name = sheet.relative_to(ROOT).as_posix()
        assert not re.search(r"(?:transition|animation)[a-z-]*\s*:[^;{}]*!important", css), f"{name} forces a duration"
        blocks, outside = _reduced_motion_blocks(css)
        assert "var(--motion-reduced)" not in outside, f"{name} reads --motion-reduced outside a reduced-motion block"
        for body in blocks:
            assert not re.search(r"(?:^|[,{}])\s*\*(?:::?[a-z-]+)?\s*[,{]", body), (
                f"{name}: a universal rule in a reduced-motion block"
            )
            for rule in re.findall(r"\{([^{}]*var\(--motion-reduced\)[^{}]*)\}", body):
                for prop, value in re.findall(r"([a-z-]+)\s*:\s*([^;]+)", rule):
                    if "var(--motion-reduced)" not in value:
                        continue
                    if prop in ("transition", "animation"):
                        parts = [part.strip() for part in value.split(",") if "var(--motion-reduced)" in part]
                        discrete = re.compile(r"(?:display|overlay) var\(--motion-reduced\)(?: [a-z-]+)* allow-discrete$")
                        fades = [part for part in parts if part.startswith("opacity ")]
                        rest = [part for part in parts if part not in fades]
                        assert fades, f"{name}: {prop}: {value}"
                        assert all(prop == "transition" and discrete.match(part) for part in rest), f"{name}: {prop}: {value}"
                    else:
                        assert re.search(r"transition-property\s*:\s*opacity\s*(;|$)", rule), f"{name}: {prop}: {value}"


# ---- colour ------------------------------------------------------------------------------------------


def test_en_examen_is_lapis_and_no_violet_is_left():
    v5 = _root_declarations(_read(V5 / "tokens.css"))
    assert not [name for name in v5 if name.startswith("--p-esame-")], "the nine wisteria primitives are retired"
    assert _token("--tone-esame-mark") == "#5278c1"
    assert _token("--notice-pending-edge") == _token("--p-registro-600")
    wisteria = {"#f2eaff", "#e9defb", "#cebde9", "#8b67bc", "#5e3d87", "#362c45", "#cab4ec", "#a481d8", "#f7f3fb"}
    assert not wisteria & {_resolve(v).lower() for v in v5.values()}
    # no primitive of the palette is a violet (OKLCH hue 280–330 with chroma)
    for name, value in v5.items():
        if name.startswith("--p-") and value.startswith("#"):
            _, a, b = _oklab(value)
            hue = math.degrees(math.atan2(b, a)) % 360
            assert not (280 <= hue <= 330 and math.hypot(a, b) > 0.04), (name, value, round(hue))


def test_the_information_notice_is_on_the_slate_wash_and_deadlines_never_mean_red():
    assert _token("--notice-info-bg") == "#f3f5f8"
    assert _token("--deadline-soon-mark") == _token("--tone-attesa-mark")
    assert _token("--deadline-overdue-mark") == _token("--tone-azione-mark")
    assert _token("--tone-conforme-mark") == _token("--p-inchiostro-900"), "VALIDE in ink (O14)"


def test_the_broken_edges_and_the_hatch_reach_3_to_1():
    for register in ("attesa", "nullo"):
        edge = _token(f"--tone-{register}-edge")
        for ground in (f"--tone-{register}-bg", "--p-carta-0", "--p-carta-25", "--p-carta-50", "--p-carta-100"):
            assert _contrast(edge, _colour(ground)) >= 3.0, (register, ground)
    hatch = re.search(r"rgba\(255, 255, 255, ([0-9.]+)\)", _token("--pattern-hatch"))
    assert hatch and float(hatch[1]) == 0.78
    stripe = _over("rgba(255, 255, 255, 0.78)", _token("--tone-attesa-mark"))
    assert _contrast(stripe, _token("--tone-attesa-mark")) >= 3.0


def test_the_night_marks_separate_in_four_visions():
    night = {r: _token(f"--tone-{r}-night-mark") for r in REGISTERS}
    assert _weak_pairs(night) == set(), "PC C5: 0 of 28 night mark pairs under 0.05"
    paper = {r: _token(f"--tone-{r}-mark") for r in REGISTERS}
    assert _weak_pairs(paper) == {("rifiuto", "blocco", "protan")}, (
        "the one paper pair, carried by × / lock and dots / cross"
    )
    audiences = {a: _token(f"--aud-{a}") for a in ("persona", "impresa", "istituzione", "universita")}
    assert _weak_pairs(audiences) <= {("persona", "universita", "protan")}, "never alone: index, glyph and word"
    assert math.dist(_oklab(audiences["impresa"]), _oklab(audiences["istituzione"])) > 0.1, "PC C8: 0.047 → 0.131"


def test_the_glass_of_the_pinned_bars_is_094():
    glass = _token("--glass-light")
    assert _rgba(glass)[3] == 0.94
    over_night = _over(glass, _token("--p-notte-900"))
    assert _contrast(_token("--brand-green"), over_night) >= 4.5, "«Italy» over the night hero (PC C7: 4.61)"
    assert _token("--blur-panel") == "0px" and _token("--blur-scrim") == "0px", "glass on the two sticky bars only"


#: (label, foreground, background, minimum). Built from the token families, recomputed from the effective cascade.
PAIRS: list[tuple[str, str, str, float]] = []
_PAPER = ("--p-carta-0", "--p-carta-25", "--p-carta-50", "--p-carta-100", "--surface-hover", "--surface-selected")
_NIGHT = ("--p-notte-950", "--p-notte-900", "--p-notte-850", "--p-notte-800")
_TEXT = (
    "--text-1",
    "--text-2",
    "--text-3",
    "--accent-text",
    "--accent-text-hover",
    *(f"--tone-{r}-text" for r in REGISTERS),
    "--notice-info-text",
    "--notice-pending-text",
    "--notice-warning-text",
    "--notice-error-text",
    "--deadline-normal-text",
    "--deadline-upcoming-text",
    "--deadline-soon-text",
    "--deadline-overdue-text",
    "--ink",
    "--ink-2",
    "--ink-3",
    "--accent",
    "--accent-hover",
    "--err-700",
    "--pending-700",
)
_NIGHT_TEXT = (
    "--text-on-night-1",
    "--text-on-night-2",
    "--accent-night",
    "--identity-key-night-text",
    *(f"--tone-{r}-night-text" for r in REGISTERS),
    "--aud-persona",
    "--aud-impresa",
    "--aud-istituzione",
    "--aud-universita",
    "--on-dark",
    "--on-dark-2",
    "--err-300",
    "--pending-300",
)
for fg in _TEXT:
    for bg in _PAPER:
        PAIRS.append((f"{fg} on {bg}", fg, bg, 4.5))
for r in REGISTERS:
    PAIRS += [
        (f"{r} word on its body", f"--tone-{r}-text", f"--tone-{r}-bg", 4.5),
        (f"{r} word on its hover body", f"--tone-{r}-text", f"--tone-{r}-bg-hover", 4.5),
        (f"ink on the {r} body", "--text-1", f"--tone-{r}-bg", 4.5),
        (f"{r} night word on its night body", f"--tone-{r}-night-text", f"--tone-{r}-night-bg", 4.5),
        (f"{r} mark on its body", f"--tone-{r}-mark", f"--tone-{r}-bg", 3.0),
        (f"{r} mark on its hover body", f"--tone-{r}-mark", f"--tone-{r}-bg-hover", 3.0),
        (f"focus ring on the {r} body", "--focus-ring", f"--tone-{r}-bg", 3.0),
    ]
    for ground in ("--p-carta-0", "--p-carta-25", "--p-carta-50", "--p-carta-100"):
        PAIRS.append((f"{r} mark on {ground}", f"--tone-{r}-mark", ground, 3.0))
    for ground in ("--p-notte-900", "--p-notte-800", "--p-notte-700"):
        PAIRS.append((f"{r} night mark on {ground}", f"--tone-{r}-night-mark", ground, 3.0))
#: PC C3: the broken edge is the meaning of attesa (dashed) and nullo (dotted), drawn at step 600: 3 : 1 on its body and
#: on every paper (3.13 – 3.96).
for r in ("attesa", "nullo"):
    for ground in (f"--tone-{r}-bg", "--p-carta-0", "--p-carta-25", "--p-carta-50", "--p-carta-100"):
        PAIRS.append((f"{r} broken edge on {ground}", f"--tone-{r}-edge", ground, 3.0))
#: PC D-doc-6, «tones on the selected and disabled surfaces»: a selected row and a disabled control are grounds a state
#: may meet. The word holds 4.5 on both (on the selected wash it is among the text × paper pairs above); the mark, and
#: the broken edge of attesa and nullo, hold 3 : 1 — except nullo's on the disabled surface (2.89), which no page
#: composes: the disabled surface is the fill of a disabled control, and a disabled control carries no state
#: (DESIGN_SYSTEM_2026.md §5; PC §6.3, held by test_the_23_pairs_of_pc_6_3_are_answered).
_NO_STATE_ON_DISABLED = {("--tone-nullo-mark", "--surface-disabled"), ("--tone-nullo-edge", "--surface-disabled")}
for r in REGISTERS:
    PAIRS.append((f"{r} word on the disabled surface", f"--tone-{r}-text", "--surface-disabled", 4.5))
    for ground in ("--surface-selected", "--surface-disabled"):
        for kind, part in (("mark", "mark"), ("broken edge", "edge")):
            if part == "edge" and r not in ("attesa", "nullo"):
                continue
            if (f"--tone-{r}-{part}", ground) not in _NO_STATE_ON_DISABLED:
                PAIRS.append((f"{r} {kind} on {ground}", f"--tone-{r}-{part}", ground, 3.0))
for fg in _NIGHT_TEXT:
    for bg in _NIGHT:
        PAIRS.append((f"{fg} on {bg}", fg, bg, 4.5))
for bg in _NIGHT:  # --text-on-night-3 never on notte-700 (4.03; D-doc-2)
    PAIRS.append((f"--text-on-night-3 on {bg}", "--text-on-night-3", bg, 4.5))
for kind in ("info", "pending", "warning", "error", "institutional"):
    PAIRS += [
        (f"{kind} notice: its word on its wash", f"--notice-{kind}-text", f"--notice-{kind}-bg", 4.5),
        (f"{kind} notice: body ink", "--text-1", f"--notice-{kind}-bg", 4.5),
        (f"{kind} notice: a link", "--accent-text", f"--notice-{kind}-bg", 4.5),
        (f"{kind} notice: the focus ring", "--focus-ring", f"--notice-{kind}-bg", 3.0),
        (f"{kind} notice: its rule on its wash", f"--notice-{kind}-edge", f"--notice-{kind}-bg", 3.0),
        (f"{kind} notice: its rule on the page", f"--notice-{kind}-edge", "--p-carta-50", 3.0),
    ]
for bg in _PAPER:
    PAIRS += [
        (f"focus ring on {bg}", "--focus-ring", bg, 3.0),
        (f"structure line on {bg}", "--line-structure", bg, 3.0),
    ]
for bg in (*_NIGHT, "--p-notte-700"):
    PAIRS += [
        (f"night focus ring on {bg}", "--focus-ring-night", bg, 3.0),
        (f"night edge on {bg}", f"--line-night|{bg}", bg, 3.0),
    ]
PAIRS += [
    ("white on the flat primary", "#ffffff", "--fill-primary", 4.5),
    ("white on the primary in hover", "#ffffff", "--fill-primary-hover", 4.5),
    ("white on the primary pressed", "#ffffff", "--fill-primary-press", 4.5),
    ("ink on the paper plate", "--text-1", "--fill-primary-night", 4.5),
    ("ink on the paper plate in hover", "--text-1", "--fill-primary-night-hover", 4.5),
    ("ink on the paper plate pressed", "--text-1", "--fill-primary-night-press", 4.5),
    ("the paper plate on night", "--fill-primary-night", "--p-notte-900", 3.0),
    ("the primary on the page", "--fill-primary", "--p-carta-50", 3.0),
    ("ink over the glass on paper", "--text-1", "--glass-light|--p-carta-50", 4.5),
    ("a link over the glass on paper", "--accent-text", "--glass-light|--p-carta-50", 4.5),
    ("«Italy» over the glass on night", "--brand-green", "--glass-light|--p-notte-900", 4.5),
    ("«Legal» over the glass on night", "--brand-navy", "--glass-light|--p-notte-900", 4.5),
    ("«Entry» over the glass on night", "--brand-red", "--glass-light|--p-notte-900", 4.5),
    ("text-2 over the glass on night", "--text-2", "--glass-light|--p-notte-900", 4.5),
    ("text-3 over the glass on night", "--text-3", "--glass-light|--p-notte-900", 4.5),
    ("a link over the glass on night", "--accent-text", "--glass-light|--p-notte-900", 4.5),
    ("the nav indicator over the glass on night", "--nav-indicator", "--glass-light|--p-notte-900", 3.0),
    ("night text on the night plate", "--text-on-night-1", "--plate-night|--p-notte-900", 4.5),
    ("night text-2 on the night plate", "--text-on-night-2", "--plate-night|--p-notte-900", 4.5),
    ("laguna on the night plate", "--accent-night", "--plate-night|--p-notte-900", 4.5),
    ("gold on the night plate", "--identity-key-night-text", "--plate-night|--p-notte-900", 4.5),
    # PC C6, kept as a rule: what holds over a WHITE pixel of a photograph
    ("C6: night text on the AA scrim over white", "--text-on-night-1", "--scrim-photo-aa|#ffffff", 4.5),
    ("C6: night text on the photo plate over white", "--text-on-night-1", "--plate-night-photo|#ffffff", 4.5),
    ("C6: night text-2 on the photo plate over white", "--text-on-night-2", "--plate-night-photo|#ffffff", 4.5),
    ("C6: laguna on the photo plate over white", "--accent-night", "--plate-night-photo|#ffffff", 4.5),
    ("C6: gold on the photo plate over white", "--identity-key-night-text", "--plate-night-photo|#ffffff", 4.5),
    ("C6: Persona on the photo plate over white", "--aud-persona", "--plate-night-photo|#ffffff", 4.5),
    ("C6: Impresa on the photo plate over white", "--aud-impresa", "--plate-night-photo|#ffffff", 4.5),
    ("C6: Istituzione on the photo plate over white", "--aud-istituzione", "--plate-night-photo|#ffffff", 4.5),
    ("C6: Università on the photo plate over white", "--aud-universita", "--plate-night-photo|#ffffff", 4.5),
    ("the dots on the rifiuto mark", "rgba(255, 255, 255, 0.6)|--tone-rifiuto-mark", "--tone-rifiuto-mark", 3.0),
    ("the cross-hatch on the blocco mark", "rgba(255, 255, 255, 0.45)|--tone-blocco-mark", "--tone-blocco-mark", 3.0),
    ("the hatch on the attesa mark", "rgba(255, 255, 255, 0.78)|--tone-attesa-mark", "--tone-attesa-mark", 3.0),
    ("the gold key on the navy seal", "--seal-glyph", "--seal-disc", 3.0),
    ("ledger: to act", "--ledger-to-act", "--p-carta-0", 4.5),
    ("ledger: in hand", "--ledger-in-hand", "--p-carta-0", 4.5),
    ("ledger: settled", "--ledger-settled", "--p-carta-0", 4.5),
    ("journey: the passed station on night", "--journey-station-done", "--p-notte-900", 3.0),
]
for ground in ("--p-carta-0", "--p-carta-50"):
    PAIRS += [
        (f"node: current ring on {ground}", "--node-current-ring", ground, 3.0),
        (f"node: done disc on {ground}", "--node-done-fill", ground, 3.0),
        (f"node: next ring on {ground}", "--node-next-edge", ground, 3.0),
        (f"node: blocked disc on {ground}", "--node-blocked-fill", ground, 3.0),
        (f"deadline: soon mark on {ground}", "--deadline-soon-mark", ground, 3.0),
        (f"deadline: overdue mark on {ground}", "--deadline-overdue-mark", ground, 3.0),
    ]


def test_at_least_four_hundred_pairs_are_held():
    assert len(PAIRS) >= 400, len(PAIRS)
    assert len({label for label, *_ in PAIRS}) == len(PAIRS), "a pair is listed twice"


@pytest.mark.parametrize("label, fg, bg, minimum", PAIRS, ids=[p[0] for p in PAIRS])
def test_contrast_on_the_effective_cascade(label, fg, bg, minimum):
    ratio = _contrast(_colour(fg), _colour(bg))
    assert ratio >= minimum, f"{label}: {ratio:.2f} < {minimum}"


#: PC §6.3, «the 23 token pairs below their minimum», each with its answer: a token the plan changed — C7 the glass at
#: 0.94, C8 «argento», O19 Persona on sand: the pair holds now — or a rule that keeps the pair off every page. C6: over a
#: photograph the night plate is --plate-night-photo (α 0.80) or a scrim, --plate-night (α 0.72) sits on the night mesh
#: only, the AA scrim carries --text-on-night-1 alone, and --text-on-night-3 never meets a photograph. D-doc-2:
#: --text-on-night-3 never on notte-700. The disabled surface carries no state. DESIGN_SYSTEM_2026.md §5 lists each one.
_WHITE, _MID_GREY = "#ffffff", "#808080"
_ON_WHITE = f"--plate-night|{_WHITE}"
PC_6_3: list[tuple[str, str, str, float, str]] = [
    ("night text-2 on the night plate over a white pixel", "--text-on-night-2", _ON_WHITE, 4.5, "C6"),
    ("laguna on the night plate over a white pixel", "--accent-night", _ON_WHITE, 4.5, "C6"),
    ("gold text on the night plate over a white pixel", "--identity-key-night-text", _ON_WHITE, 4.5, "C6"),
    ("Persona on the night plate over a white pixel", "--aud-persona", _ON_WHITE, 4.5, "O19"),
    ("Impresa on the night plate over a white pixel", "--aud-impresa", _ON_WHITE, 4.5, "C6"),
    ("Istituzione on the night plate over a white pixel", "--aud-istituzione", _ON_WHITE, 4.5, "C8"),
    ("Università on the night plate over a white pixel", "--aud-universita", _ON_WHITE, 4.5, "C6"),
    ("night text-3 on the night plate over a white pixel", "--text-on-night-3", _ON_WHITE, 4.5, "C6"),
    (
        "night text-3 on the night plate over a mid-grey pixel",
        "--text-on-night-3",
        f"--plate-night|{_MID_GREY}",
        4.5,
        "C6",
    ),
    ("the gold glyph on the night plate over a white pixel", "--brand-gold", _ON_WHITE, 3.0, "C6"),
    *(
        (f"{r} night word on the night plate over a white pixel", f"--tone-{r}-night-text", _ON_WHITE, 4.5, "C6")
        for r in REGISTERS
        if r != "conforme"
    ),
    ("night text-2 on the AA scrim over a white pixel", "--text-on-night-2", f"--scrim-photo-aa|{_WHITE}", 4.5, "C6"),
    ("laguna on the AA scrim over a white pixel", "--accent-night", f"--scrim-photo-aa|{_WHITE}", 4.5, "C6"),
    (
        "gold text on the AA scrim over a white pixel",
        "--identity-key-night-text",
        f"--scrim-photo-aa|{_WHITE}",
        4.5,
        "C6",
    ),
    ("a link over the glass on night (0.85 → 0.94)", "--accent-text", "--glass-light|--p-notte-900", 4.5, "C7"),
    ("night text-3 on notte-700", "--text-on-night-3", "--p-notte-700", 4.5, "D-doc-2"),
    ("the nullo mark on the disabled surface", "--tone-nullo-mark", "--surface-disabled", 3.0, "disabled"),
]
#: Answers that are tokens (the pair holds now) — every other answer is a rule, named in the §5 table by these words.
_TOKEN_ANSWERS = {"C7", "C8", "O19"}
_RULE_WORDS = {"C6": "C6", "D-doc-2": "D-doc-2", "disabled": "superficie disabilitata"}
#: Ruled out with them, from D-doc-6: the dotted edge is the same colour as the nullo mark.
_RULED_OUT_TOO = [
    ("the nullo dotted edge on the disabled surface", "--tone-nullo-edge", "--surface-disabled", 3.0, "disabled")
]


def _ds_table(marker: str) -> list[list[str]]:
    """The rows of a DESIGN_SYSTEM_2026.md table fenced by `<!-- marker:start -->` and `<!-- marker:end -->`."""
    block = re.search(rf"<!-- {marker}:start -->(.*?)<!-- {marker}:end -->", _read(DS2026), flags=re.S)
    assert block, f"DESIGN_SYSTEM_2026.md has no {marker} table"
    rows = []
    for line in block.group(1).splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[1].startswith("`"):
            rows.append(cells)
    return rows


def _cell(text: str) -> tuple[str, str | None]:
    """«`--a` su `--b` #hex» → ("--a|--b", "#hex"): a layer on its ground, as PAIRS writes it; the hex is optional."""
    m = re.fullmatch(r"`([^`]+)`(?: su `([^`]+)`)?(?: (#[0-9a-f]{6}))?", text)
    assert m, text
    return (f"{m[1]}|{m[2]}" if m[2] else m[1]), m[3]


def test_the_23_pairs_of_pc_6_3_are_answered():
    """PC §6.3's 23 pairs: each one now holds (its token changed), or is kept off every page by a rule that
    DESIGN_SYSTEM_2026.md §5 lists with its measured ratio — and a ruled-out pair that has come to hold is moved, not
    left ruled out."""
    assert len(PC_6_3) == 23 and len({row[0] for row in PC_6_3}) == 23
    documented = {}
    for _label, fg_cell, bg_cell, ratio, rule in _ds_table("contrast-v5-ruled-out"):
        documented[(_cell(fg_cell)[0], _cell(bg_cell)[0])] = (float(ratio.removesuffix(":1")), rule)
    expected = set()
    for label, fg, bg, minimum, answer in [*PC_6_3, *_RULED_OUT_TOO]:
        ratio = _contrast(_colour(fg), _colour(bg))
        if answer in _TOKEN_ANSWERS:
            assert ratio >= minimum, f"{label}: {ratio:.2f} < {minimum} although {answer} answers it"
            continue
        assert ratio < minimum, f"{label}: {ratio:.2f} holds now — move it to PAIRS and off the ruled-out table"
        expected.add((fg, bg))
        assert (fg, bg) in documented, f"{label} is not in the ruled-out table of DS 2026 §5"
        printed, rule = documented[(fg, bg)]
        assert abs(printed - ratio) <= 0.01, (label, printed, round(ratio, 2))
        assert _RULE_WORDS[answer] in rule, (label, rule)
    assert set(documented) == expected, sorted(set(documented) - expected)


def test_the_design_system_2026_contrast_table_is_the_effective_cascade():
    """DS 2026 §5's V5 table: each row is a pair this file holds, with the hex the cascade resolves (a layer composited
    on its ground) and the ratio recomputed — the document cannot drift from the values a page renders."""
    rows = _ds_table("contrast-v5")
    assert len(rows) >= 50, len(rows)
    assert f"**{len(PAIRS)} coppie**" in _read(DS2026), f"DS 2026 §5 must state the {len(PAIRS)} pairs this file holds"
    held = {(fg, bg, minimum) for _label, fg, bg, minimum in PAIRS}
    for label, fg_cell, bg_cell, ratio_cell, requirement in rows:
        (fg, fg_hex), (bg, bg_hex) = _cell(fg_cell), _cell(bg_cell)
        minimum = float(requirement)
        assert (fg, bg, minimum) in held, f"DS 2026 §5 documents a pair this file does not hold: {label}"
        assert fg_hex in (None, _colour(fg).lower()), (label, fg_hex, _colour(fg))
        assert bg_hex == _colour(bg).lower(), (label, bg_hex, _colour(bg))
        ratio = _contrast(_colour(fg), _colour(bg))
        assert abs(ratio - float(ratio_cell.removesuffix(":1"))) <= 0.01, (label, round(ratio, 2), ratio_cell)
        assert ratio >= minimum, (label, ratio)


# ---- corners, shadows, materials -------------------------------------------------------------------


def test_the_corner_scale_is_lo_spigolo():
    scale = {name: _token(f"--radius-{name}") for name in ("xs", "sm", "md", "lg", "xl", "full")}
    assert scale == {"xs": "2px", "sm": "4px", "md": "6px", "lg": "8px", "xl": "12px", "full": "999px"}
    assert _token("--radius-control") == "4px", "buttons and fields on sm"
    assert _token("--radius-tile") == "6px" and _token("--radius-pill") == "999px"
    assert (
        _token("--card-radius") == "8px" and _token("--dialog-radius") == "12px" and _token("--field-radius") == "4px"
    )


def test_five_shadow_levels_in_the_nights_own_colour():
    """SH-1: five levels, each with a meaning — 0 the canvas (no shadow), 1 sheet, 2 raised, 3 popover / menu / panel,
    4 modal / drawer with a scrim — each with its twin for night grounds (same offsets, twice the alpha), and the door's
    own; V5 declares no other shadow (V4's six roles, retired from test_v4_tokens.py: the glow is gone)."""
    declared = {name for name in _root_declarations(_read(V5 / "tokens.css")) if name.startswith("--shadow-")}
    assert declared == {*(f"--shadow-{n}" for n in "1234"), *(f"--shadow-{n}-dark" for n in "1234"), "--shadow-door"}
    for level in ("1", "2", "3", "4"):
        light, dark = _token(f"--shadow-{level}"), _token(f"--shadow-{level}-dark")
        for shadow in (light, dark):
            colours = re.findall(r"rgba\([^)]*\)", shadow)
            assert colours and all(c.startswith("rgba(7, 18, 38,") for c in colours), shadow
        alphas_light = [float(a) for a in re.findall(r"rgba\([^)]*,\s*([0-9.]+)\)", light)]
        alphas_dark = [float(a) for a in re.findall(r"rgba\([^)]*,\s*([0-9.]+)\)", dark)]
        assert [round(a * 2, 2) for a in alphas_light] == alphas_dark, level
        assert re.sub(r"rgba\([^)]*\)", "", light) == re.sub(r"rgba\([^)]*\)", "", dark), "same offsets"
    assert _token("--shadow-surface") == _token("--shadow-4"), "V1's one shadow is the modal / drawer level"
    assert _token("--shadow-5") == _token("--shadow-4"), "the V2 name is the modal / drawer level"
    for glow in ("--shadow-glow", "--shadow-glow-dark"):
        assert _token(glow) == "0 0 0 0 transparent", "the glow is retired (SH-3, SH-9)"


def test_every_primary_is_flat():
    for name, fill in (
        ("--grad-primary", "--fill-primary"),
        ("--grad-primary-hover", "--fill-primary-hover"),
        ("--grad-primary-press", "--fill-primary-press"),
        ("--grad-primary-dark", "--fill-primary-night"),
        ("--grad-primary-dark-hover", "--fill-primary-night-hover"),
        ("--grad-primary-dark-press", "--fill-primary-night-press"),
    ):
        assert TOKENS[name] == f"linear-gradient(var({fill}), var({fill}))", name


#: Generated, not written by hand: the frames of the L1 light are computed (scripts/gen_loader_light.py, W1-D; plan §2.4).
GENERATED_SHEETS = {"_loader-light.css"}


def _v5_sheets() -> list[Path]:
    """Every V5 sheet: static/css/v5/ — main.css's four and the page partials (`_*.css`) — and the console partials."""
    return sorted([*V5.glob("*.css"), *PORTAL_V5.glob("*.css")])


def test_the_brand_colours_are_declared_once_and_no_literal_colour_leaves_the_token_sheets():
    """Kept from test_v4_tokens.py and extended to every V5 sheet (plan §2.7): the brand colours are declared in
    v2/tokens.css only; a literal colour lives in v5/tokens.css, never in the aliases, the base, a page partial or a
    console partial (the generated loader light excepted); no register is painted with the verdict green, the accent
    or the brand green — «no colour ever means approved» (O14)."""
    sheets = _v5_sheets()
    assert {"fonts.css", "tokens.css", "aliases.css", "base.css"} <= {sheet.name for sheet in sheets}
    for sheet in sheets:
        css = _strip_comments(_read(sheet))
        assert not re.search(r"--brand-[a-z]+\s*:", css), f"{sheet.name} re-declares a brand colour"
        for match in re.finditer(r"\[data-register=\"[a-z]+\"\][^{]*\{([^}]*)\}", css):
            body = match.group(1)
            assert not re.search(r"--ok-|--accent|--brand-green", body), (sheet.name, body.strip())
        if sheet.name in ("tokens.css", "fonts.css") or sheet.name in GENERATED_SHEETS:
            continue
        literals = re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\blinear-gradient\(\s*#", css)
        assert literals == [], (sheet.name, literals)


def _product_template_chains() -> dict[str, str]:
    """Every product template (templates/dev/ is served under DEBUG only) with the text of its chain of
    {% extends %}: what a page drawn from it can link. The project's templates before the apps' (Django's DIRS)."""
    sources: dict[str, str] = {}
    for root in (ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))):
        for path in sorted(root.rglob("*.html")):
            sources.setdefault(path.relative_to(root).as_posix(), _read(path))

    def chain(name: str, seen: tuple[str, ...] = ()) -> str:
        text = sources.get(name, "")
        parent = re.search(r"""\{%\s*extends\s+["']([^"']+)["']""", text)
        if parent and parent.group(1) not in seen:
            text += chain(parent.group(1), (*seen, name))
        return text

    return {name: chain(name) for name in sources if not name.startswith("dev/")}


def test_the_console_partials_close_the_console_entry():
    """Plan §2.3 and §2.7: console-only V5 CSS lives in `_`-prefixed partials in apps/portal/static/portal/v5/, which
    the console entry imports and main.css never does; they close the entry as v5/* closes main.css — every one of them
    imported, after every other import, and, once there is one, no rule of the entry's own (CSS puts every @import
    before the rules, so a rule left in the entry would beat the V5 partials). Today the entry imports none."""
    assert CONSOLE_ENTRY.exists()
    assert "css/dist/portal/console.css" in _read(ROOT / "templates" / "portal" / "base_portal.html")
    css = _strip_comments(_read(CONSOLE_ENTRY))
    imports = re.findall(r'@import url\("([^"]+)"\)', css)
    partials = sorted(f"v5/{path.name}" for path in PORTAL_V5.glob("_*.css"))
    v5_imports = [name for name in imports if name.startswith("v5/")]
    # A console partial drawn by a few pages only is imported by THEIR page sheet, never by the console entry
    # every page loads (W3-C, plan §3.5 item 5: «Mes pièces»' three, by apps/documents/static/documents/documents.css;
    # DS 2026 §2). An import is read where the collected tree resolves it: ../portal/v5/_x.css from another app's
    # sheet, v5/_x.css from the portal's own page sheets (W3-D: portal/journey.css, portal/situation.css).
    page_imports: dict[str, list[str]] = {}
    for sheet in sorted((ROOT / "apps").glob("*/static/**/*.css")):
        if sheet.name.startswith("_") or "dist" in sheet.parts or sheet == CONSOLE_ENTRY:
            continue
        collected = "/".join(sheet.relative_to(ROOT / "apps").parts[2:])  # apps/<app>/static/<path> -> <path>
        for target in re.findall(r'@import url\("([^"]+)"\)', _strip_comments(_read(sheet))):
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(collected), target))
            if re.fullmatch(r"portal/v5/_[a-z-]+\.css", resolved):
                page_imports.setdefault(f"v5/{posixpath.basename(resolved)}", []).append(collected)
    assert not set(v5_imports) & set(page_imports), "a partial is the console entry's or page sheets', never both"
    assert len(set(v5_imports)) == len(v5_imports), "the console entry imports a partial once"
    assert sorted(set(v5_imports) | set(page_imports)) == partials, (
        "every console partial is imported by the console entry, or by the page sheets of the pages that draw it"
    )
    # DL54-112 gave each partial ONE importer; W3-D's journey composes one vocabulary, written once, into two page
    # sheets — the rail's nodes, v5/_journey-nodes.css, in portal/journey.css and portal/situation.css (DL54-128 item
    # 4). What «one importer» protected stays the rule: a page loads a partial once — no product template, its chain
    # of {% extends %} included, links two sheets that import the same partial.
    chains = _product_template_chains()
    assert len(chains) > 50, len(chains)
    for name, sheets in page_imports.items():
        for template, text in chains.items():
            together = [sheet for sheet in sheets if f"css/dist/{sheet}" in text]
            assert len(together) <= 1, f"{template} loads {name} twice, through {together}"
    assert not any(name.startswith("v5/_") or "portal/v5/" in name for name in _cascade()), "never by main.css"
    if v5_imports:
        assert imports[-len(v5_imports) :] == v5_imports, "the V5 partials are the entry's last imports"
        own = re.sub(r'@import url\("[^"]+"\)[^;]*;', "", css).strip()
        assert own == "", "the console entry keeps rules of its own after its V5 partials: move them into partials"


def test_the_design_system_2026_css_blocks_are_the_cascade_values():
    """The ```css blocks of DESIGN_SYSTEM_2026.md (§6, §7) are the contract; the cascade is the fact."""
    blocks = re.findall(r"```css\n(.*?)```", _read(DS2026), flags=re.S)
    assert blocks, "DESIGN_SYSTEM_2026.md has no css code block"
    documented: dict[str, str] = {}
    for block in blocks:
        for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", _strip_comments(block)):
            documented[name] = " ".join(value.split())
    assert len(documented) >= 60, len(documented)
    missing = sorted(name for name in documented if name not in TOKENS)
    assert not missing, f"documented in DESIGN_SYSTEM_2026.md, declared nowhere in the cascade: {missing}"
    wrong = {n: (documented[n], TOKENS[n]) for n in documented if " ".join(TOKENS[n].split()) != documented[n]}
    assert not wrong, wrong


def test_fonts_v5_md_records_every_shipped_face_with_its_bytes_and_hash():
    """docs/design-v5/FONTS_V5.md is the provenance record (plan §2.3): every woff2 the product ships is in its table,
    with the size and the SHA-256 of the file on disk, and each licence text with the opening of its hash."""
    doc = _read(FONTS_DOC)
    rows = re.findall(
        r"^\| `(v5-[a-z0-9-]+\.woff2)` \|[^|]*\|[^|]*\| ([0-9 ]+) \| `([0-9a-f]{64})` \|$", doc, flags=re.M
    )
    on_disk = {path.name: path.read_bytes() for path in (STATIC / "fonts").glob("*.woff2")}
    assert sorted(name for name, *_ in rows) == sorted(on_disk), "FONTS_V5.md and static/fonts/ list different faces"
    for name, size, digest in rows:
        assert len(on_disk[name]) == int(size.replace(" ", "")), name
        assert hashlib.sha256(on_disk[name]).hexdigest() == digest, name
    for family, text in (
        ("Host Grotesk", "OFL-HostGrotesk.txt"),
        ("IBM Plex Mono", "OFL-IBMPlexMono.txt"),
        ("Newsreader", "OFL-Newsreader.txt"),
        ("Vazirmatn", "OFL-Vazirmatn.txt"),
    ):
        prefix = re.search(re.escape(family) + r"\s+`([0-9a-f]{8})…`", doc)
        digest = hashlib.sha256((STATIC / "fonts" / "licenses" / text).read_bytes()).hexdigest()
        assert prefix and digest.startswith(prefix[1]), text
