"""
Design-system asset compliance: tokens, WCAG contrast, icon sprite, forbidden strings,
no external hosts, no inline styles in owned templates.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from cms.forbidden import scan

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
OWNED_TEMPLATE_DIRS = ["partials", "components", "errors", "allauth", "account", "mfa"]

pytestmark = pytest.mark.compliance


def _tokens() -> dict[str, str]:
    css = (STATIC / "css" / "tokens.css").read_text(encoding="utf-8")
    root = css.split(":root {", 1)[1].split("\n}", 1)[0]
    return dict(re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", root))


def _hex(tokens: dict[str, str], name: str) -> str:
    value = tokens[name].strip()
    while value.startswith("var("):
        value = tokens[value[4:-1].strip()].strip()
    assert re.fullmatch(r"#[0-9a-f]{6}", value), (name, value)
    return value


def _luminance(hex_color: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(fg: str, bg: str) -> float:
    lf, lb = _luminance(fg), _luminance(bg)
    hi, lo = max(lf, lb), min(lf, lb)
    return (hi + 0.05) / (lo + 0.05)


REQUIRED_TOKEN_PREFIXES = [
    "--state-done-",
    "--state-info-",
    "--state-warn-",
    "--state-error-",
    "--state-pending-",
    "--paper",
    "--ink",
    "--navy",
    "--rubric",
    "--cooperation",
    "--rule-",
    "--font-",
    "--t-",
    "--track-",
    "--s-",
    "--rank-",
    "--grid-",
    "--measure-",
    "--radius-",
    "--shadow-",
    "--motion-",
    "--ease-",
    "--z-",
    "--chrome-",
    "--container",
]
#: The ten roles of the scale (AD-A §3.3). Eleven size tokens collapsed to ten roles, and the
#: fourth heading level became a folio label rather than a size smaller than the lead.
REQUIRED_TYPE_ROLES = [
    "plate",
    "title",
    "band",
    "entry",
    "lead",
    "prose",
    "gloss",
    "caption",
    "ui",
    "folio",
    "numeral",
]

# (label, foreground token, background token, minimum ratio).
# Re-verified against --paper #FAF7F0 on 21 September 2026: the ground moved when art direction A
# replaced the token set, and a contrast figure computed against the previous ground is not a
# contrast figure. Every value here is recomputed by the test itself, never trusted from a document.
CONTRAST_PAIRS = [
    # Text (WCAG 1.4.3 — 4.5:1)
    ("ink on paper", "--ink", "--paper", 4.5),
    ("ink on paper-deep", "--ink", "--paper-deep", 4.5),
    ("ink-secondary on paper", "--ink-secondary", "--paper", 4.5),
    ("ink-muted on paper", "--ink-muted", "--paper", 4.5),
    ("ink-muted on paper-deep", "--ink-muted", "--paper-deep", 4.5),
    ("ink on input", "--ink", "--surface-input", 4.5),
    ("navy on paper", "--navy", "--paper", 4.5),
    ("paper on navy", "--paper-on-navy", "--navy", 4.5),
    ("paper-muted on navy", "--paper-muted-on-navy", "--navy", 4.5),
    ("paper on navy-deep", "--paper-on-navy", "--navy-deep", 4.5),
    ("rubric on paper", "--rubric", "--paper", 4.5),
    ("rubric on paper-deep", "--rubric", "--paper-deep", 4.5),
    ("cooperation on paper", "--cooperation", "--paper", 4.5),
    ("state done fg on bg", "--state-done-fg", "--state-done-bg", 4.5),
    ("state info fg on bg", "--state-info-fg", "--state-info-bg", 4.5),
    ("state warn fg on bg", "--state-warn-fg", "--state-warn-bg", 4.5),
    ("state error fg on bg", "--state-error-fg", "--state-error-bg", 4.5),
    ("state error fg on paper", "--state-error-fg", "--paper", 4.5),
    ("state pending fg on bg", "--state-pending-fg", "--state-pending-bg", 4.5),
    # Non-text UI and rules (WCAG 1.4.11 — 3:1), measured against the surface they are DRAWN on
    ("rule-ink on paper", "--rule-ink", "--paper", 3.0),
    ("rule-ink on input", "--rule-ink", "--surface-input", 3.0),
    ("rubric rule on paper", "--rubric", "--paper", 3.0),
    ("rubric rule on navy", "--rubric-on-navy", "--navy", 3.0),
    ("navy rule on paper", "--navy", "--paper", 3.0),
    ("state done border on paper", "--state-done-br", "--paper", 3.0),
    ("state info border on paper", "--state-info-br", "--paper", 3.0),
    ("state warn border on paper", "--state-warn-br", "--paper", 3.0),
    ("state error border on paper", "--state-error-br", "--paper", 3.0),
    ("state pending border on paper", "--state-pending-br", "--paper", 3.0),
]


def test_tokens_file_is_complete():
    tokens = _tokens()
    for prefix in REQUIRED_TOKEN_PREFIXES:
        assert any(k.startswith(prefix) for k in tokens), prefix
    for role in REQUIRED_TYPE_ROLES:
        assert f"--t-{role}-size" in tokens, role
    for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32):
        assert f"--s-{n}" in tokens
    assert tokens["--s-1"].strip() == "4px"  # 4px rhythm, in px so the base unit is visible
    assert "--radius-control" in tokens and "--radius-marker" in tokens


def test_every_line_height_is_a_multiple_of_four():
    """AD-A §3.3 and §8: the vertical rhythm is 4px, so a line-height that is not is a defect."""
    tokens = _tokens()
    offenders = []
    for name, value in tokens.items():
        if name.endswith("-lh") and value.strip().endswith("px"):
            px = int(value.strip().removesuffix("px"))
            if px % 4:
                offenders.append(f"{name}: {px}px")
    assert offenders == [], offenders


def test_prose_size_never_changes_across_breakpoints():
    """
    Fluid interpolation is what flattened the previous hierarchy: the heading-to-prose ratio fell
    from 1.62 at 1920 to 1.35 at 390. Display sizes step at breakpoints; prose does not move at all.
    """
    css = (STATIC / "css" / "tokens.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # comments explain the rule; they are not the rule
    # Every redefinition of --t-prose-size outside the base :root block would break it.
    for block in code.split("@media")[1:]:
        assert "--t-prose-size" not in block, "prose size must not change at a breakpoint"
    assert "clamp(" not in code, "no clamp() on the type scale: sizes step so ratios are designed"


@pytest.mark.parametrize("label, fg, bg, minimum", CONTRAST_PAIRS, ids=[p[0] for p in CONTRAST_PAIRS])
def test_wcag_contrast(label, fg, bg, minimum):
    tokens = _tokens()
    ratio = contrast(_hex(tokens, fg), _hex(tokens, bg))
    assert ratio >= minimum, f"{label}: {ratio:.2f} < {minimum}"


def test_no_hardcoded_colours_outside_tokens_and_fonts():
    for name in ("base.css", "layout.css", "components.css"):
        css = (STATIC / "css" / name).read_text(encoding="utf-8")
        # data: URI icons (select chevron) are the only place a literal colour is allowed.
        stripped = re.sub(r"url\(\"data:[^\"]+\"\)", "", css)
        hexes = re.findall(r"#[0-9a-fA-F]{3,8}\b", stripped)
        assert hexes == [], (name, hexes)


def _owned_template_files() -> list[Path]:
    files = [TEMPLATES / "base.html"]
    for folder in OWNED_TEMPLATE_DIRS:
        path = TEMPLATES / folder
        if path.exists():
            files += sorted(path.rglob("*.html"))
    return files


def _static_files() -> list[Path]:
    return [p for p in STATIC.rglob("*") if p.suffix in {".css", ".js", ".svg"}]


def test_every_icon_used_in_templates_exists_in_sprite():
    sprite = (STATIC / "img" / "icons.svg").read_text(encoding="utf-8")
    ids = set(re.findall(r'<symbol id="icon-([a-z0-9-]+)"', sprite))
    used = set()
    for path in _owned_template_files():
        used |= set(re.findall(r'svg_icon "([a-z0-9-]+)"', path.read_text(encoding="utf-8")))
    missing = used - ids
    assert not missing, missing
    assert {
        "person",
        "building",
        "institution",
        "university",
        "arrow",
        "check",
        "warning",
        "shield",
        "calendar",
        "document",
        "globe",
        "menu",
        "close",
        "chevron",
        "search",
        "mail",
        "phone",
        "user",
        "lock",
    } <= ids


def test_static_assets_have_no_external_hosts_or_forbidden_strings():
    for path in _static_files():
        text = path.read_text(encoding="utf-8")
        urls = re.findall(r"https?://[^\s\"')]+", text)
        externals = [u for u in urls if not u.startswith("http://www.w3.org/")]
        assert externals == [], (path.name, externals)
        assert scan(text) == [], (path.name, scan(text))
        assert "®" not in text, path.name


def test_owned_templates_have_no_forbidden_strings_inline_styles_or_handlers():
    for path in _owned_template_files():
        text = path.read_text(encoding="utf-8")
        violations = scan(text)
        assert violations == [], (path, violations)
        assert not re.search(r"\sstyle=\"", text), path
        assert not re.search(r"\son[a-z]+=\"", text), path
        assert "®" not in text, path
        assert "fonts.googleapis" not in text and "unsplash" not in text.lower(), path


def test_illustrations_avoid_stereotyped_subjects():
    forbidden = (
        "porta",
        "door",
        "frontier",
        "frontière",
        "border",
        "passport",
        "passeport",
        "valigia",
        "suitcase",
        "airport",
        "aéroport",
        "grille",
        "queue",
    )
    for path in sorted((STATIC / "img" / "illustrations").glob("*.svg")):
        text = path.read_text(encoding="utf-8").lower()
        for word in forbidden:
            assert word not in text, (path.name, word)
        assert path.name.startswith(("entrance-", "pilot-", "orientation"))
    names = {p.name for p in (STATIC / "img").rglob("*")}
    for banned in ("veneto", "rovigo", "regione", "comune"):
        assert not any(banned in n.lower() for n in names), banned


def test_locked_texts_never_hand_copied_in_owned_templates():
    """Prescribed sentences must only enter templates through {% locked %}."""
    from cms import locked_content

    samples = [
        locked_content.text("p1.companies.title", "fr"),
        locked_content.text("p3.antifraud.title", "fr"),
        locked_content.text("p3.entrances.person.title", "fr"),
        locked_content.text("p2.home.banner.button", "fr"),
        locked_content.text("p3.reserved.title", "fr"),
    ]
    for path in _owned_template_files():
        text = path.read_text(encoding="utf-8")
        for sample in samples:
            assert sample not in text, (path, sample)


def test_main_js_is_an_es_module_without_external_dependencies():
    js = (STATIC / "js" / "main.js").read_text(encoding="utf-8")
    assert "export {" in js
    assert "import " not in js.replace("importNode", "")
    assert "prefers-reduced-motion" in js
    assert "IntersectionObserver" in js
    assert "showModal" in js
    assert "aria-expanded" in js
    assert "Escape" in js
