"""
Design V4 tokens — the sheet says what docs/design-v4/DESIGN_SYSTEM_V4.md says, and the values hold.

`static/css/v4/tokens.css` is loaded last and keeps the V2 names, so a value it declares is the
value every earlier layer ends up with. These tests read the cascade the way the browser does
(in `main.css` order, last `:root` declaration wins) and compare it with the code blocks of the
design system, recompute the contrast ratios the sheet claims in its comments, and hold the two
cascade facts the file header explains: the narrow-viewport override V2 relied on is restated,
and reduced motion zeroes every duration.

Fast and offline: files on disk only.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
V4 = STATIC / "css" / "v4" / "tokens.css"
DESIGN = ROOT / "docs" / "design-v4" / "DESIGN_SYSTEM_V4.md"

pytestmark = pytest.mark.compliance


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _cascade() -> list[str]:
    return re.findall(r'@import url\("([^"]+)"\)', _read(STATIC / "css" / "main.css"))


def _root_declarations(css: str) -> dict[str, str]:
    """The `--name: value` pairs of the TOP-LEVEL :root blocks (a :root nested in a media query is
    indented, and is not the one that wins across the cascade)."""
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


def _norm(value: str) -> str:
    """Whitespace and number spelling are not differences: `rgba(7,18,38,.50)` is `rgba(7, 18, 38, 0.5)`."""
    compact = re.sub(r"\s+", "", value.lower())
    compact = re.sub(r"(?<![0-9])\.(\d)", r"0.\1", compact)  # .45 → 0.45
    compact = re.sub(r"(\d\.\d*?)0+(?=[^0-9.]|$)", r"\1", compact)  # 0.50 → 0.5
    return re.sub(r"(\d)\.(?=[^0-9]|$)", r"\1", compact)  # 1. → 1


def _resolve(tokens: dict[str, str], value: str, depth: int = 0) -> str:
    assert depth < 8, value
    m = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value.strip())
    return _resolve(tokens, tokens[m.group(1)], depth + 1) if m else value.strip()


def _rgb(value: str) -> tuple[float, float, float, float]:
    value = value.strip()
    if value.startswith("#"):
        h = value[1:]
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([0-9.]+))?\s*\)", value)
    assert m, value
    return int(m[1]), int(m[2]), int(m[3]), float(m[4] or 1)


def _over(fg: str, bg: str) -> tuple[float, float, float]:
    r, g, b, a = _rgb(fg)
    br, bg_, bb, _ = _rgb(bg)
    return (r * a + br * (1 - a), g * a + bg_ * (1 - a), b * a + bb * (1 - a))


def _luminance(rgb: tuple[float, float, float]) -> float:
    def channel(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast(fg: str, bg: str) -> float:
    """fg may carry alpha: it is composited over bg first (that is what the eye meets)."""
    l1 = _luminance(_over(fg, bg))
    l2 = _luminance(_over(bg, "#000000"))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------------------------------------


def test_v4_tokens_open_the_last_block_of_the_cascade_and_are_in_the_bundle():
    """The V4 layers close the cascade, and the tokens open them: every V4 sheet reads values the
    tokens sheet has already set, and no non-V4 sheet may come after them. They reach the browser in
    static/css/dist/main.css (npm run build:css), which base.html applies — no longer preloaded one
    by one."""
    imports = _cascade()
    first = imports.index("v4/tokens.css")
    assert all(name.startswith("v4/") for name in imports[first:]), imports[first:]
    assert not any(name.startswith("v4/") for name in imports[:first]), imports[:first]
    shell = _read(ROOT / "templates" / "base.html")
    assert "{% static 'css/dist/main.css' %}" in shell


def test_every_value_in_the_design_system_code_blocks_is_the_cascade_value():
    """The ```css blocks of DESIGN_SYSTEM_V4.md are the contract; the cascade is the fact."""
    tokens = _effective()
    blocks = re.findall(r"```css\n(.*?)```", _read(DESIGN), flags=re.S)
    assert blocks, "DESIGN_SYSTEM_V4.md has no css code block"
    documented: dict[str, str] = {}
    for block in blocks:
        for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", _strip_comments(block)):
            if "…" in value:  # an abbreviated range («--s-1: 4px … --s-32: 128px»), not a value
                continue
            documented[name] = " ".join(value.split())
    assert len(documented) >= 90, len(documented)
    missing = sorted(name for name in documented if name not in tokens)
    assert not missing, f"documented in DESIGN_SYSTEM_V4.md, declared nowhere in the cascade: {missing}"
    wrong = {name: (documented[name], tokens[name]) for name in documented if _norm(documented[name]) != _norm(tokens[name])}
    assert not wrong, wrong


@pytest.mark.parametrize(
    "label, fg, bg, minimum",
    [
        # text (1.4.3 — 4.5:1)
        ("white on the primary gradient, top stop", "#ffffff", "#12777f", 4.5),
        ("white on the primary gradient, bottom stop", "#ffffff", "#0f6a72", 4.5),
        ("white on the hover gradient, top stop", "#ffffff", "#15808a", 4.5),
        ("accent-2 on min-0", "--accent-2", "--min-0", 4.5),
        ("accent on min-1", "--accent", "--min-1", 4.5),
        ("accent-hover on accent-wash", "--accent-hover", "--accent-wash", 4.5),
        ("accent-hover on accent-wash-2", "--accent-hover", "--accent-wash-2", 4.5),
        ("on-dark on mid-1", "--on-dark", "--mid-1", 4.5),
        ("on-dark on mid-4", "--on-dark", "--mid-4", 4.5),
        ("on-dark-2 on mid-3", "--on-dark-2", "--mid-3", 4.5),
        ("on-dark-3 on mid-2", "--on-dark-3", "--mid-2", 4.5),
        ("accent-dark on mid-1", "--accent-dark", "--mid-1", 4.5),
        ("accent-dark on mid-3", "--accent-dark", "--mid-3", 4.5),
        ("mid-1 on accent-dark-2", "--mid-1", "--accent-dark-2", 4.5),
        ("mid-1 on accent-dark-hover", "--mid-1", "--accent-dark-hover", 4.5),
        ("route-1-dark on mid-1", "--route-1-dark", "--mid-1", 4.5),
        ("route-2-dark on mid-1", "--route-2-dark", "--mid-1", 4.5),
        ("route-3-dark on mid-1", "--route-3-dark", "--mid-1", 4.5),
        ("route-4-dark on mid-1", "--route-4-dark", "--mid-1", 4.5),
        ("pending-300 on mid-1", "--pending-300", "--mid-1", 4.5),
        ("err-300 on mid-1", "--err-300", "--mid-1", 4.5),
        ("ink-3 on surface-disabled", "--ink-3", "--surface-disabled", 4.5),
        ("brand-gold on mid-1", "--brand-gold", "--mid-1", 4.5),
        ("ink on the brand gradient, top stop", "--ink", "#d9eef0", 4.5),
        ("accent on the brand gradient, top stop", "--accent", "#d9eef0", 4.5),
        ("on-dark on the dark brand gradient, top stop", "--on-dark", "#1b344e", 4.5),
        ("ink over light glass on paper", "--ink", "rgba(251, 250, 248, 0.85)|#faf9f7", 4.5),
        ("accent over light glass on paper", "--accent", "rgba(251, 250, 248, 0.85)|#faf9f7", 4.5),
        ("on-dark over dark glass on mid-1", "--on-dark", "rgba(11, 26, 51, 0.55)|#0b1a33", 4.5),
        # non-text (1.4.11 — 3:1)
        ("accent-ring on min-0", "--accent-ring", "--min-0", 3.0),
        ("accent-ring on min-2", "--accent-ring", "--min-2", 3.0),
        ("accent-ring on accent-wash", "--accent-ring", "--accent-wash", 3.0),
        ("accent-ring on accent-wash-2", "--accent-ring", "--accent-wash-2", 3.0),
        ("edge-dark on mid-1", "--edge-dark", "--mid-1", 3.0),
        ("hairline-strong on accent-wash", "--hairline-strong", "--accent-wash", 3.0),
        ("routes on navy dimmed to 50 %, weakest", "rgba(170, 183, 204, 0.5)", "--mid-1", 3.0),
    ],
)
def test_the_contrast_the_comments_claim_holds(label, fg, bg, minimum):
    tokens = _effective()

    def colour(spec: str) -> str:
        if "|" in spec:  # «layer|ground»: a translucent layer composited on a ground
            layer, ground = spec.split("|")
            r, g, b = _over(layer, ground)
            return f"rgb({round(r)}, {round(g)}, {round(b)})"
        return _resolve(tokens, tokens[spec]) if spec.startswith("--") else spec

    ratio = _contrast(colour(fg), colour(bg))
    assert ratio >= minimum, f"{label}: {ratio:.2f} < {minimum}"


def test_the_interface_is_the_plex_superfamily_and_the_files_are_self_hosted():
    tokens = _effective()
    assert tokens["--f-sans"].startswith('"IBM Plex Sans", "IBM Plex Sans Arabic"'), tokens["--f-sans"]
    assert tokens["--f-mono"].startswith('"IBM Plex Mono"'), tokens["--f-mono"]
    # the names of tokens.css and of the shim are re-pointed, so layers 1–7 change face at once
    assert tokens["--font-ui"] == "var(--f-sans)"
    assert tokens["--font-ref"] == "var(--f-mono)"
    assert tokens["--font-mono"] == "var(--f-mono)"
    assert tokens["--f-serif"].startswith('"Newsreader"'), "the public display face is kept"
    fonts = _read(STATIC / "css" / "fonts.css")
    for family in ("IBM Plex Sans", "IBM Plex Mono", "IBM Plex Sans Arabic", "Newsreader", "Noto Naskh Arabic"):
        assert f'font-family: "{family}";' in fonts, family
    assert 'font-family: "Fira' not in fonts
    on_disk = {p.name for p in (STATIC / "fonts").glob("*.woff2")}
    assert not [name for name in on_disk if name.startswith("fira-")], "the Fira files retired with V4"
    for weight, style in (("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal")):
        for subset in ("latin", "latin-ext"):
            assert f"ibm-plex-sans-{weight}-{style}-{subset}.woff2" in on_disk, (weight, style, subset)
    assert "ibm-plex-mono-400-normal-latin.woff2" in on_disk
    shell = _read(ROOT / "templates" / "base.html")
    assert "fonts/ibm-plex-sans-400-normal-latin.woff2" in shell, "the LTR page preloads the reading sans"
    assert "fira-" not in shell


def test_the_narrow_override_v2_relied_on_is_restated():
    """v2/tokens.css zeroes the utility bar and lowers the header below md inside a media query;
    a later top-level :root wins over that whatever the viewport, so V4 restates it."""
    narrow = re.search(r"@media \(max-width: 47\.999rem\)\s*\{\s*:root\s*\{(.*?)\}", _strip_comments(_read(V4)), flags=re.S)
    assert narrow, "no narrow-viewport override in v4/tokens.css"
    body = " ".join(narrow.group(1).split())
    assert "--utility-h: 0px;" in body and "--header-h: 56px;" in body and "--page-pad: 16px;" in body, body
    tokens = _effective()
    assert tokens["--utility-height"] == "var(--utility-h)" and tokens["--header-height"] == "var(--header-h)"


def test_reduced_motion_zeroes_every_duration_but_the_ambient_loop():
    reduced = re.search(
        r"@media \(prefers-reduced-motion: reduce\)\s*\{\s*:root\s*\{(.*?)\}", _strip_comments(_read(V4)), flags=re.S
    )
    assert reduced, "no reduced-motion block in v4/tokens.css"
    zeroed = dict(re.findall(r"(--motion-[a-z]+)\s*:\s*([^;]+);", reduced.group(1)))
    for name in ("--motion-fast", "--motion-standard", "--motion-emphasized", "--motion-slow", "--motion-draw"):
        assert zeroed.get(name) == "0ms", (name, zeroed.get(name))
    assert "--motion-ambient" not in zeroed, "an infinite animation with no duration spins: the sheet removes the object"
    tokens = _effective()
    assert tokens["--motion-instant"] == "var(--motion-fast)" and tokens["--motion-base"] == "var(--motion-standard)"


def test_motion_slow_changed_meaning_so_no_v2_sheet_still_uses_it():
    """V2's --motion-slow was 320 ms; V4 gives the name 480 ms and the old sites --motion-emphasized."""
    for sheet in (STATIC / "css" / "v2").glob("*.css"):
        assert "var(--motion-slow)" not in _read(sheet), sheet.name
    for sheet in (STATIC / "css" / "v3").glob("*.css"):
        assert "var(--motion-slow)" not in _read(sheet), sheet.name


def test_six_shadow_roles_and_their_dark_twins():
    v4 = _root_declarations(_read(V4))
    for role in ("--shadow-1", "--shadow-2", "--shadow-3", "--shadow-4", "--shadow-glow", "--shadow-door"):
        assert role in v4, role
    for level in ("1", "2", "3", "4"):
        light, dark = v4[f"--shadow-{level}"], v4[f"--shadow-{level}-dark"]
        alphas_light = [float(a) for a in re.findall(r"rgba\([^)]*,\s*([0-9.]+)\)", light)]
        alphas_dark = [float(a) for a in re.findall(r"rgba\([^)]*,\s*([0-9.]+)\)", dark)]
        assert [round(a * 2, 2) for a in alphas_light] == alphas_dark, (level, light, dark)
        assert re.sub(r"rgba\([^)]*\)", "", light) == re.sub(r"rgba\([^)]*\)", "", dark), "same offsets"
    assert v4["--shadow-5"] == "var(--shadow-4)", "the V2 name survives as an alias"


def test_the_brand_colours_are_not_touched_and_the_shim_colour_names_are_not_reused():
    v4 = _root_declarations(_read(V4))
    assert not [name for name in v4 if name.startswith("--brand-")], "the official brand is declared once, in v2"
    # --border-strong and --border-accent are COLOURS in _legacy-tokens.css; a shorthand under the
    # same name would turn every `border: 1px solid var(--border-strong)` of layers 1–7 invalid.
    assert "--border-strong" not in v4 and "--border-accent" not in v4
    for line in ("--line-hair", "--line-strong", "--line-accent", "--line-dash"):
        assert line in v4, line


def test_the_v4_component_sheets_carry_no_literal_colour():
    """Every colour, shadow and gradient of the V4 sheets is a token: the literals live in
    v4/tokens.css and nowhere else (gate A review, binary check 3). The one exception is the
    forced-colours layer, whose system colours are keywords, not literals."""
    app_sheets = [
        ROOT / "apps" / "accounts" / "static" / "accounts" / "entrance.css",
        ROOT / "apps" / "portal" / "static" / "portal" / "console.css",
    ]
    for sheet in [*sorted((STATIC / "css" / "v4").glob("*.css")), *app_sheets]:
        if sheet.name == "tokens.css":
            continue
        css = _strip_comments(_read(sheet))
        literals = re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\blinear-gradient\(|\bradial-gradient\(|\bdrop-shadow\(", css)
        assert literals == [], (sheet.name, literals)


def test_no_register_is_painted_with_the_verdict_green_or_the_accent():
    """«No colour ever means approved»: a `[data-register]` surface of the V4 sheets is painted with
    the chips' marks (ink, pending, err, hairline), never with `--ok-*` nor with the accent (gate C
    review, correction 1)."""
    for sheet in sorted((STATIC / "css" / "v4").glob("*.css")):
        css = _strip_comments(_read(sheet))
        for match in re.finditer(r"\[data-register=\"[a-z]+\"\][^{]*\{([^}]*)\}", css):
            body = match.group(1)
            assert "--ok-" not in body and "var(--accent)" not in body, (sheet.name, body.strip())


def test_the_z_order_of_the_old_names_follows_the_new_scale():
    tokens = _effective()
    order = ["--z-base", "--z-raised", "--z-sticky", "--z-rail", "--z-header", "--z-popover", "--z-drawer", "--z-modal", "--z-toast", "--z-tooltip"]
    values = [int(tokens[name]) for name in order]
    assert values == sorted(values) and len(set(values)) == len(values), values
    assert tokens["--z-dropdown"] == "var(--z-popover)" and tokens["--z-dialog"] == "var(--z-modal)"
    assert tokens["--z-skiplink"] == "calc(var(--z-tooltip) + 1)"
