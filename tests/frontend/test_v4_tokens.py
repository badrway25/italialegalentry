"""
Design V4 tokens — what static/css/v4/tokens.css still holds once design V5 closes the cascade.

`static/css/v4/tokens.css` keeps the V2 names and gives them the V4 values; since W1-A (V5.4 plan §2.3)
`static/css/v5/` is imported after it and re-values the same names (static/css/v5/aliases.css). What V4
alone answered for — the cascade order, the DS V4 code blocks, the contrast of the V4 values, the Plex
faces, the six shadow roles (SH-1 keeps five levels, the glow is gone) — is retired into
tests/frontend/test_v5_tokens.py, which reads the effective cascade. What stays here is true of the V4
sheets themselves, as long as they hold it: the narrow-viewport override the file header explains, the brand
colours left to v2, no literal colour in the V4 component sheets, no register painted green, the z-order of
the old names. Reduced motion — V4 zeroed its six durations but the loop — is retired into
tests/frontend/test_v5_tokens.py (W1-D): v5/tokens.css zeroes every duration, and the legacy names follow.

Fast and offline: files on disk only.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
V4 = STATIC / "css" / "v4" / "tokens.css"

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


# ---------------------------------------------------------------------------------------------


def test_v4_layers_form_one_block_before_the_v5_block_that_closes_the_cascade():
    """The V4 layers stay one block, opened by their tokens; design V5 follows them and closes the cascade
    (tests/frontend/test_v5_tokens.py holds the V5 end). They reach the browser in static/css/dist/main.css
    (npm run build:css), which base.html applies — no longer preloaded one by one."""
    imports = _cascade()
    first = imports.index("v4/tokens.css")
    v5 = imports.index("v5/fonts.css")
    assert all(name.startswith("v4/") for name in imports[first:v5]), imports[first:v5]
    assert all(name.startswith("v5/") for name in imports[v5:]), imports[v5:]
    assert not any(name.startswith("v4/") for name in imports[:first]), imports[:first]
    shell = _read(ROOT / "templates" / "base.html")
    assert "{% static 'css/dist/main.css' %}" in shell


def test_the_narrow_override_v2_relied_on_is_restated():
    """v2/tokens.css zeroes the utility bar and lowers the header below md inside a media query;
    a later top-level :root wins over that whatever the viewport, so V4 restates it."""
    narrow = re.search(
        r"@media \(max-width: 47\.999rem\)\s*\{\s*:root\s*\{(.*?)\}", _strip_comments(_read(V4)), flags=re.S
    )
    assert narrow, "no narrow-viewport override in v4/tokens.css"
    body = " ".join(narrow.group(1).split())
    assert "--utility-h: 0px;" in body and "--header-h: 56px;" in body and "--page-pad: 16px;" in body, body
    tokens = _effective()
    assert tokens["--utility-height"] == "var(--utility-h)" and tokens["--header-height"] == "var(--header-h)"


def test_motion_slow_changed_meaning_so_no_v2_sheet_still_uses_it():
    """V2's --motion-slow was 320 ms; V4 gives the name 480 ms and the old sites --motion-emphasized."""
    for sheet in (STATIC / "css" / "v2").glob("*.css"):
        assert "var(--motion-slow)" not in _read(sheet), sheet.name
    for sheet in (STATIC / "css" / "v3").glob("*.css"):
        assert "var(--motion-slow)" not in _read(sheet), sheet.name


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
        literals = re.findall(
            r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\blinear-gradient\(|\bradial-gradient\(|\bdrop-shadow\(", css
        )
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
    order = [
        "--z-base",
        "--z-raised",
        "--z-sticky",
        "--z-rail",
        "--z-header",
        "--z-popover",
        "--z-drawer",
        "--z-modal",
        "--z-toast",
        "--z-tooltip",
    ]
    values = [int(tokens[name]) for name in order]
    assert values == sorted(values) and len(set(values)) == len(values), values
    assert tokens["--z-dropdown"] == "var(--z-popover)" and tokens["--z-dialog"] == "var(--z-modal)"
    assert tokens["--z-skiplink"] == "calc(var(--z-tooltip) + 1)"
