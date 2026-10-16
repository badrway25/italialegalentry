"""
Truthfulness tests for docs/design/DESIGN_SYSTEM_2026.md and docs/ACCESSIBILITY.md.

The two documents describe what exists in the code. These tests fail as soon as the code and the
documents drift apart: a token added, renamed or re-valued; a legacy-shim entry added without its
replacement being written down; a component, icon, font file, JS module, breakpoint or keyframe
added or removed; a contrast ratio that no longer matches; a cited template, test or screenshot
that does not exist; a WCAG criterion missing from the checklist; an app-level stylesheet
(apps/*/static) that stops using the design tokens.

DESIGN_SYSTEM_2026.md replaced docs/DESIGN_SYSTEM.md when art direction A («Le Registre») replaced
the token set; the retired document is kept only as a superseded stub and is no longer checked.

Fast and offline: no database, no browser, no network — only files on disk plus one in-memory
render of ``components/form_field.html``.
"""

from __future__ import annotations

import importlib.util
import posixpath
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
STATIC = ROOT / "static"
COMPONENTS = ROOT / "templates" / "components"
DESIGN_DOC = DOCS / "design" / "DESIGN_SYSTEM_2026.md"
A11Y_DOC = DOCS / "ACCESSIBILITY.md"
CAPTURE_SCRIPT = DOCS / "qa" / "design" / "capture.py"
#: The demolition scaffold: part of static/css and of the cascade, but not of the design system.
#: It is documented on its own in §17 and it must only ever shrink.
LEGACY_SHIM = STATIC / "css" / "_legacy-tokens.css"

pytestmark = pytest.mark.compliance

#: Prefixes of every token family, old and new. A backticked span starting with one of these is
#: checked against the real token set: the art direction A families first, then the legacy names
#: that still live in the shim and are still cited by ACCESSIBILITY.md.
TOKEN_FAMILY_PREFIXES = (
    # art direction A
    "--paper",
    "--ink",
    "--navy",
    "--rubric",
    "--cooperation",
    "--rule-",
    "--state-",
    "--t-",
    "--track-",
    "--s-",
    "--rank-",
    "--grid-",
    "--chrome-",
    "--motion-",
    "--width-",
    # kept from the retired system, now declared by the shim
    "--color-",
    "--surface-",
    "--text-",
    "--border-",
    "--focus-ring",
    "--font-",
    "--leading-",
    "--tracking-",
    "--weight-",
    "--measure-",
    "--space-",
    "--section-gap",
    "--stack-gap",
    "--gutter",
    "--radius-",
    "--shadow-",
    "--duration-",
    "--ease-",
    "--reveal-",
    "--z-",
    "--container",
    "--control-height",
    "--icon-size",
    "--header-height",
    "--utility-height",
)

# WCAG 2.2 success criteria at levels A and AA (4.1.1 Parsing is obsolete and removed in 2.2).
WCAG_22_A_AA = {
    "1.1.1": "A",
    "1.2.1": "A",
    "1.2.2": "A",
    "1.2.3": "A",
    "1.2.4": "AA",
    "1.2.5": "AA",
    "1.3.1": "A",
    "1.3.2": "A",
    "1.3.3": "A",
    "1.3.4": "AA",
    "1.3.5": "AA",
    "1.4.1": "A",
    "1.4.2": "A",
    "1.4.3": "AA",
    "1.4.4": "AA",
    "1.4.5": "AA",
    "1.4.10": "AA",
    "1.4.11": "AA",
    "1.4.12": "AA",
    "1.4.13": "AA",
    "2.1.1": "A",
    "2.1.2": "A",
    "2.1.4": "A",
    "2.2.1": "A",
    "2.2.2": "A",
    "2.3.1": "A",
    "2.4.1": "A",
    "2.4.2": "A",
    "2.4.3": "A",
    "2.4.4": "A",
    "2.4.5": "AA",
    "2.4.6": "AA",
    "2.4.7": "AA",
    "2.4.11": "AA",
    "2.5.1": "A",
    "2.5.2": "A",
    "2.5.3": "A",
    "2.5.4": "A",
    "2.5.7": "AA",
    "2.5.8": "AA",
    "3.1.1": "A",
    "3.1.2": "AA",
    "3.2.1": "A",
    "3.2.2": "A",
    "3.2.3": "AA",
    "3.2.4": "AA",
    "3.2.6": "A",
    "3.3.1": "A",
    "3.3.2": "A",
    "3.3.3": "AA",
    "3.3.4": "AA",
    "3.3.7": "A",
    "3.3.8": "AA",
    "4.1.2": "A",
    "4.1.3": "AA",
}
CHECKLIST_STATUSES = ("Conforme", "Da confermare in QA", "Parziale", "Non applicabile")
COMPONENT_BULLETS = ("Scopo", "Blocco CSS", "Contratto", "Varianti", "Accessibilità", "Usato in")


# ---------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _design() -> str:
    return _read(DESIGN_DOC)


def _a11y() -> str:
    return _read(A11Y_DOC)


def _tokens() -> dict[str, str]:
    css = _read(STATIC / "css" / "tokens.css")
    root = css.split(":root {", 1)[1].split("\n}", 1)[0]
    return {name: " ".join(value.split()) for name, value in re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", root)}


def _shim_tokens() -> dict[str, str]:
    """Every legacy name the demolition scaffold still declares, with the value it resolves to."""
    names: dict[str, str] = {}
    for block in re.findall(r":root \{(.*?)\n\}", _read(LEGACY_SHIM), flags=re.S):
        names.update(
            {name: " ".join(value.split()) for name, value in re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", block)}
        )
    return names


def _cascade() -> list[str]:
    """The stylesheet layers, in the order main.css imports them.

    Derived, never hard-coded: art direction A adds layers as the graphic language is built
    (register.css), and a layer that exists but is not imported — or is imported but missing — is
    itself a defect, which is what test_breakpoints_keyframes_and_stylesheets_are_documented checks.
    """
    return re.findall(r'@import url\("([^"]+)"\)', _read(STATIC / "css" / "main.css"))


def _is_partial(path: Path) -> bool:
    """A `_`-prefixed sheet is a partial wherever it is: never a build entry, bundled by the sheets that import it
    (design V5, V5.4 plan §2.3, DL54-15)."""
    return path.name.startswith("_")


def _design_system_partials() -> list[Path]:
    """The design system's partials that main.css does not carry: page-only CSS in static/css (outside dist/ and dev/)
    and console-only CSS in apps/portal/static/portal/v5/ (plan §2.3). None exists before the families that draw them."""
    css = STATIC / "css"
    found = [p for p in css.rglob("_*.css") if not {"dist", "dev"} & set(p.relative_to(css).parts)]
    found += (ROOT / "apps" / "portal" / "static" / "portal" / "v5").glob("_*.css")
    in_cascade = {(css / name).resolve() for name in _cascade()}
    return sorted(p for p in found if p.resolve() not in in_cascade)


def _page_sheets() -> list[Path]:
    """The app entries — the page sheets and the console entry, loaded in extra_head (plan §2.3): every sheet under
    apps/*/static that is not a partial."""
    return sorted(p for p in ROOT.glob("apps/*/static/**/*.css") if not _is_partial(p))


def _imported_sheet(sheet: Path, target: str) -> Path | None:
    """The file an @import of `sheet` draws, read as collectstatic and scripts/build_css.mjs read it: from the sheet's
    place in the COLLECTED tree (static/<p> → <p>, apps/<app>/static/<p> → <p>; DS 2026 §2), never through the source
    tree. None when nothing is collected there: tests/frontend/test_static_pipeline.py names that reference."""
    roots = [STATIC, *sorted((ROOT / "apps").glob("*/static"))]
    here = next(sheet.relative_to(root).as_posix() for root in roots if sheet.is_relative_to(root))
    collected = posixpath.normpath(posixpath.join(posixpath.dirname(here), target))
    return next(((root / collected).resolve() for root in roots if (root / collected).is_file()), None)


def _component_custom_properties() -> set[str]:
    names: set[str] = set()
    for sheet in _cascade():
        names |= set(re.findall(r"(?<![\w-])(--[a-z0-9-]+)\s*:", _read(STATIC / "css" / sheet)))
    return names


def _resolve(tokens: dict[str, str], name: str) -> str:
    value = tokens[name]
    while value.startswith("var("):
        value = tokens[value[4:-1].strip()]
    return value


def _luminance(hex_color: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast(fg: str, bg: str) -> float:
    lf, lb = _luminance(fg), _luminance(bg)
    hi, lo = max(lf, lb), min(lf, lb)
    return (hi + 0.05) / (lo + 0.05)


def _between(text: str, start: str, end: str) -> str:
    assert start in text and end in text, (start, end)
    return text.split(start, 1)[1].split(end, 1)[0]


def _code_spans(text: str) -> list[str]:
    without_fences = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.findall(r"`([^`\n]+)`", without_fences)


def _component_sections() -> dict[str, str]:
    doc = _design()
    catalogue = _between(doc, "## 10. Catalogo componenti", "### 10.1 ")
    parts = re.split(r"^#### `([a-z_]+\.html)`\s*$", catalogue, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def _bullet(section: str, label: str) -> str:
    match = re.search(rf"^- \*\*{re.escape(label)}\*\*: (.*?)(?=^- \*\*|\n```|\Z)", section, flags=re.M | re.S)
    assert match, label
    return match.group(1)


def _gap_rows(text: str, heading: str) -> dict[str, str]:
    """The numbered-gap table of a document, keyed by gap id."""
    table = text.split(heading, 1)[1]
    return {m.group(1): m.group(0) for m in re.finditer(r"^\| (G-\d\d) \|.*$", table, flags=re.M)}


def _capture_module():
    spec = importlib.util.spec_from_file_location("ile_design_capture", CAPTURE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # imports Playwright lazily inside capture(): safe offline
    return module


# ---------------------------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------------------------
def test_both_documents_exist_and_reference_each_other():
    design, a11y = _design(), _a11y()
    assert "docs/ACCESSIBILITY.md" in design
    assert "docs/design/DESIGN_SYSTEM_2026.md" in a11y
    for doc in (design, a11y):
        assert "Italy Legal Entry™" in doc
        assert "®" not in doc
        assert "tests/frontend/test_design_docs.py" in doc
    # The design document names the art direction it documents, and the decision that binds it.
    for source in ("docs/design/ART_DIRECTION_A.md", "docs/design/ART_DIRECTION_DECISION.md"):
        assert source in design, source
    for heading in (
        "## 1. Principi e anti-pattern",
        "## 2. Architettura CSS",
        "## 3. Token",
        "## 4. Colore",
        "## 5. Contrasto WCAG misurato",
        "## 6. Tipografia",
        "## 7. Griglia, breakpoint e layout",
        "## 8. Il linguaggio grafico proprio",
        "## 9. Superfici, bordi, elevazione",
        "## 10. Catalogo componenti",
        "## 11. Pattern di navigazione",
        "## 12. Motion",
        "## 13. Iconografia",
        "## 14. Illustrazioni e fotografia",
        "## 15. RTL e arabo",
        "## 16. Moduli JS e progressive enhancement",
        "## 17. Lo shim legacy",
        "## 18. Come estendere il sistema",
        "## 19. Screenshot QA",
        "## 20. Controlli automatici",
        "## 21. Difetti noti",
    ):
        assert heading in design, heading
    for heading in (
        "## 2. Checklist WCAG 2.2",
        "## 3. Modello tastiera",
        "## 4. Gestione del focus",
        "## 5. Semantica per screen reader",
        "## 6. Contratto di accessibilità dei form",
        "## 7. Movimento ridotto",
        "## 8. Zoom, reflow",
        "## 9. Dimensione dei bersagli",
        "## 10. Lingua, RTL e bidi",
        "## 11. Controlli automatici esistenti",
        "## 12. Procedura di test manuale",
        "## 13. Lacune note",
    ):
        assert heading in a11y, heading


# ---------------------------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------------------------
def test_every_token_is_documented_with_its_literal_value():
    tokens = _tokens()
    reference = _between(_design(), "## 3. Token", "### 3.19 ")
    rows = dict(re.findall(r"^\| `(--[a-z0-9-]+)` \| `([^`]+)` \|", reference, flags=re.M))
    missing = sorted(set(tokens) - set(rows))
    assert not missing, f"tokens.css tokens without a row in DESIGN_SYSTEM_2026.md §3: {missing}"
    stale = sorted(set(rows) - set(tokens))
    assert not stale, f"DESIGN_SYSTEM_2026.md §3 documents tokens that no longer exist: {stale}"
    for name, documented in rows.items():
        assert " ".join(documented.split()) == tokens[name], (name, documented, tokens[name])


def test_every_legacy_shim_token_is_documented_with_its_replacement():
    """§17: the demolition scaffold is a countdown, so every entry must be visible with its target.

    A name added to _legacy-tokens.css without a row in §17 turns the suite red; so does a row in
    §17 for a name the file no longer declares. That is what makes the shim shrink instead of
    quietly becoming a second design system.
    """
    shim = _shim_tokens()
    assert shim, "_legacy-tokens.css declares nothing: the shim is gone, update §17 and this test"
    section = _between(_design(), "## 17. Lo shim legacy", "## 18. ")
    rows = dict(re.findall(r"^\| `(--[a-z0-9-]+)` \| `([^`]+)` \|", section, flags=re.M))
    missing = sorted(set(shim) - set(rows))
    assert not missing, f"legacy names without a row in DESIGN_SYSTEM_2026.md §17: {missing}"
    stale = sorted(set(rows) - set(shim))
    assert not stale, f"§17 documents legacy names the shim no longer declares: {stale}"
    for name, documented in rows.items():
        assert " ".join(documented.split()) == shim[name], (name, documented, shim[name])
    counted = re.search(r"\*\*(\d+) nomi\*\*", section)
    assert counted, "§17 must state how many names are left in the shim"
    assert int(counted.group(1)) == len(shim), (counted.group(1), len(shim))
    # §17 must point at the file that actually enforces the countdown, and that file must hold a
    # ceiling equal to the census the document publishes. A pointer with no ceiling behind it is
    # how the previous version of this section came to cite a test that did not exist.
    enforcer = ROOT / "tests" / "frontend" / "test_legacy_token_shim.py"
    assert enforcer.exists(), "the file §17 relies on for the countdown is missing"
    assert "tests/frontend/test_legacy_token_shim.py" in section, (
        "§17 must name the test file that holds the shim's ceilings"
    )
    ceiling = re.search(r"MAX_SHIM_TOKENS = (\d+)", _read(enforcer))
    assert ceiling and int(ceiling.group(1)) == len(shim), (
        "the ceiling in test_legacy_token_shim.py and the real shim disagree: lower the ceiling in "
        "the commit that removes entries"
    )
    # Every replacement that is itself a token must be a token that exists.
    real = set(_tokens())
    for name, documented in rows.items():
        for referenced in re.findall(r"var\((--[a-z0-9-]+)\)", documented):
            assert referenced in real, f"{name} in §17 resolves to a token that does not exist: {referenced}"


def test_token_family_headings_match_tokens_css():
    tokens = _tokens()
    reference = _between(_design(), "## 3. Token", "### 3.19 ")
    headings = re.findall(r"^### 3\.\d+ .*$", reference, flags=re.M)
    assert len(headings) == 18, headings
    patterns: list[str] = []
    exact: set[str] = set()
    for heading in headings:
        for span in re.findall(r"`(--[a-z0-9*-]+)`", heading):
            if "*" in span:
                patterns.append(span.split("*", 1)[0])
            else:
                exact.add(span)
    assert patterns, "no token family pattern found in the §3 headings"
    for prefix in patterns:
        assert any(name.startswith(prefix) for name in tokens), f"documented family {prefix}* has no token"
    for name in exact:
        assert name in tokens, name
    orphans = [n for n in tokens if n not in exact and not any(n.startswith(p) for p in patterns)]
    assert not orphans, f"tokens that belong to no documented family: {orphans}"


def test_tokens_named_in_the_documents_exist():
    known = set(_tokens()) | _shim_tokens().keys() | _component_custom_properties()
    for path, text in ((DESIGN_DOC, _design()), (A11Y_DOC, _a11y())):
        for span in _code_spans(text):
            if not span.startswith(TOKEN_FAMILY_PREFIXES):
                continue
            match = re.match(r"--[a-z0-9-]+", span)
            name = match.group(0)
            rest = span[len(name) :]
            if rest.startswith("*") or name.endswith("-"):
                continue  # family pattern such as --color-primary-* or --color-*-border
            assert name in known, f"{path.name} names an unknown token: {span}"


def test_documented_contextual_overrides_exist_in_tokens_css():
    css = _read(STATIC / "css" / "tokens.css")
    arabic = _between(css, ':root:lang(ar),\n:root[dir="rtl"] {', "\n}")
    for name in (
        "--font-display",
        "--font-ui",
        "--t-prose-lh",
        "--t-gloss-lh",
        "--t-entry-lh",
        "--track-folio",
        "--track-caps-display",
    ):
        assert name in arabic, name
    reduced = css.split("@media (prefers-reduced-motion: reduce)", 1)[1]
    for name in ("--motion-fast", "--motion-base", "--motion-slow"):
        assert name in reduced, name
    overrides = _between(_design(), "### 3.19 ", "## 4. ")
    assert ":lang(ar)" in overrides and "prefers-reduced-motion" in overrides
    # The reduced-motion zeroing must reach the legacy duration names too, or a template that has
    # not been migrated keeps animating while the documents claim nothing does.
    shim = _shim_tokens()
    for legacy, target in (
        ("--duration-fast", "--motion-fast"),
        ("--duration-base", "--motion-base"),
        ("--duration-slow", "--motion-slow"),
    ):
        assert shim[legacy] == f"var({target})", (legacy, shim[legacy])


# ---------------------------------------------------------------------------------------------
# Contrast
# ---------------------------------------------------------------------------------------------
def _contrast_rows() -> list[tuple[str, str, str, float, str]]:
    table = _between(_design(), "<!-- contrast-table:start -->", "<!-- contrast-table:end -->")
    rows = []
    for line in table.splitlines():
        match = re.match(
            r"^\| (?P<label>[^|]+) \| `(?P<fg>--[a-z0-9-]+)` (?P<fg_hex>#[0-9a-f]{6}) \| "
            r"`(?P<bg>--[a-z0-9-]+)` (?P<bg_hex>#[0-9a-f]{6}) \| (?P<ratio>[0-9.]+):1 \| (?P<req>[^|]+) \|",
            line,
        )
        if match:
            rows.append(match)
    return rows


def test_contrast_table_matches_recomputed_ratios():
    tokens = _tokens()
    rows = _contrast_rows()
    assert len(rows) >= 30, len(rows)
    for row in rows:
        fg, bg = _resolve(tokens, row["fg"]), _resolve(tokens, row["bg"])
        assert fg == row["fg_hex"], (row["fg"], fg, row["fg_hex"])
        assert bg == row["bg_hex"], (row["bg"], bg, row["bg_hex"])
        ratio = _contrast(fg, bg)
        assert abs(ratio - float(row["ratio"])) <= 0.05, (row["label"].strip(), ratio, row["ratio"])
        requirement = row["req"].strip()
        if requirement != "—":
            assert ratio >= float(requirement), (row["label"].strip(), ratio, requirement)


def test_contrast_table_covers_every_pair_locked_by_the_asset_tests():
    source = _read(ROOT / "tests" / "frontend" / "test_static_assets.py")
    block = _between(source, "CONTRAST_PAIRS = [", "\n]\n")
    locked = re.findall(r'\("[^"]+",\s*"(--[a-z0-9-]+)",\s*"(--[a-z0-9-]+)",\s*([0-9.]+)\)', block)
    assert len(locked) >= 29, len(locked)
    # A pair can be locked twice with two thresholds — --navy and --rubric are both text colours
    # (4.5) and rule colours (3.0) — so the document must carry a row for each threshold, not one
    # row that happens to satisfy the looser of the two.
    documented: dict[tuple[str, str], set[float]] = {}
    for row in _contrast_rows():
        requirement = row["req"].strip()
        if requirement != "—":
            documented.setdefault((row["fg"], row["bg"]), set()).add(float(requirement))
    for fg, bg, minimum in locked:
        assert (fg, bg) in documented, f"contrast pair missing from DESIGN_SYSTEM_2026.md §5: {fg} on {bg}"
        assert float(minimum) in documented[(fg, bg)], (fg, bg, sorted(documented[(fg, bg)]), minimum)


# ---------------------------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------------------------
def test_every_component_file_has_a_section_and_vice_versa():
    files = {p.name for p in COMPONENTS.glob("*.html")}
    sections = _component_sections()
    assert files, "templates/components/ is empty"
    assert not files - set(sections), (
        f"components without a section in DESIGN_SYSTEM_2026.md §10: {sorted(files - set(sections))}"
    )
    assert not set(sections) - files, f"documented components that do not exist: {sorted(set(sections) - files)}"
    assert f"{len(files)} file" in _between(_design(), "## 10. Catalogo componenti", "#### ")
    for name, body in sections.items():
        for label in COMPONENT_BULLETS:
            assert f"- **{label}**:" in body, (name, label)
        assert "- **Esempio" in body and "```django" in body, name
        assert f"components/{name}" in body or name in ("account_menu.html", "language_switcher.html"), name


def test_component_css_blocks_and_consumers_are_real():
    """A component's CSS block is defined somewhere a page loads it: the main.css cascade, the design system's page
    and console partials, or the app entries that import them — the console entry and the page sheets (design V5
    moves page-only and console-only CSS out of main.css, V5.4 plan §2.3)."""
    sources = [*(STATIC / "css" / name for name in _cascade()), *_design_system_partials(), *_page_sheets()]
    css = "".join(_read(path) for path in sources)
    for name, body in _component_sections().items():
        block = re.search(r"`(\.[a-z][a-z0-9_-]*)`", _bullet(body, "Blocco CSS"))
        assert block, name
        selector = block.group(1)
        assert re.search(re.escape(selector) + r"(?![a-z0-9])", css), f"{name}: {selector} is not defined in the CSS"
        class_name = selector.lstrip(".")
        for path in re.findall(r"`(templates/[^`\s]+\.html)`", _bullet(body, "Usato in")):
            source = ROOT / path
            assert source.exists(), f"{name}: cited consumer does not exist: {path}"
            text = _read(source)
            assert f"components/{name}" in text or class_name.split("__")[0] in text, (name, path)


def test_documented_contract_variables_are_used_by_the_component_template():
    """Every context variable named in a «Contratto» bullet must appear in the component source."""
    ignore = {"True", "False", "user", "site"}
    for name, body in _component_sections().items():
        source = _read(COMPONENTS / name)
        contract = _bullet(body, "Contratto")
        lead_names = re.findall(r"(?:^|; |, | \+ )`([a-z_]+)`", contract)
        assert lead_names or "nessuna variabile" in contract, name
        for variable in lead_names:
            if variable in ignore:
                continue
            assert re.search(rf"\b{variable}\b", source), (
                f"{name}: documented variable `{variable}` is not in the template"
            )


# ---------------------------------------------------------------------------------------------
# Icons, fonts, JS, CSS structure
# ---------------------------------------------------------------------------------------------
def test_no_icon_svg_bakes_a_literal_colour_without_it_being_recorded():
    """AD-A §7.7: icons are drawn in ``currentColor``; a literal hex inside static/img is a defect.

    The sprite itself must be clean. The illustrations still bake the retired palette, which is why
    §14.1 marks all six for retirement or redrawing — the document has to say so, per file.
    """
    sprite = _read(STATIC / "img" / "icons.svg")
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b", sprite), "icons.svg bakes a literal colour"
    section = _between(_design(), "### 14.1 ", "### 14.2 ")
    for path in sorted((STATIC / "img" / "illustrations").glob("*.svg")):
        if re.findall(r"#[0-9a-fA-F]{3,8}\b", _read(path)):
            assert f"`{path.name}`" in section, f"{path.name} bakes a literal colour and §14.1 does not list it"


def test_every_icon_id_is_listed_and_no_listed_icon_is_missing():
    sprite = _read(STATIC / "img" / "icons.svg")
    ids = set(re.findall(r'<symbol id="icon-([a-z0-9-]+)"', sprite))
    listing = _between(_design(), "<!-- icon-list:start -->", "<!-- icon-list:end -->")
    listed = re.findall(r"`([a-z0-9-]+)`", listing)
    assert not [name for name, count in Counter(listed).items() if count > 1], "icon listed twice"
    assert set(listed) == ids, (sorted(ids - set(listed)), sorted(set(listed) - ids))
    assert f"{len(ids)} icone" in listing


def test_listed_font_files_exist_and_every_font_file_is_listed():
    on_disk = {p.name for p in (STATIC / "fonts").glob("*.woff2")}
    section = _between(_design(), "### 6.2 ", "### 6.3 ")
    listed = set(re.findall(r"`([a-z0-9-]+\.woff2)`", section))
    assert listed == on_disk, (sorted(on_disk - listed), sorted(listed - on_disk))
    assert f"{len(on_disk)} file woff2" in section
    # Design V5, type «Una voce» (V5.4 plan §1.1, §2.3): the faces are declared in static/css/v5/fonts.css;
    # the V4 fonts.css left with its 26 files.
    in_css = {
        url.rsplit("/", 1)[-1]
        for url in re.findall(r'url\("([^"]+\.woff2)"\)', _read(STATIC / "css" / "v5" / "fonts.css"))
    }
    assert in_css == on_disk, (sorted(on_disk - in_css), sorted(in_css - on_disk))
    typography = _between(_design(), "## 6. Tipografia", "## 7. ")
    for phrase in (
        "SIL Open Font License 1.1",
        "font-display: swap",
        "Host Grotesk",
        "ILE Wordmark",
        "ILE Mono",
        "Vazirmatn",
        "unicode-range",
        "static/fonts/licenses/",
        "docs/design-v5/FONTS_V5.md",
    ):
        assert phrase in typography, phrase
    # Every font base.html preloads must be named in §6, and a preload of a file that is not on
    # disk is a defect the documents have to carry by number (gap G-24), not a silent 404.
    preloads = set(re.findall(r"fonts/([a-z0-9-]+\.woff2)", _read(ROOT / "templates" / "base.html")))
    assert preloads, "base.html no longer preloads any font"
    for preload in preloads:
        assert preload in typography, f"base.html preloads {preload} and §6 does not mention it"
    stale = sorted(preload for preload in preloads if preload not in on_disk)
    gap_row = _gap_rows(_a11y(), "## 13. Lacune note")["G-24"]
    if "chiusa" in gap_row:
        assert not stale, f"G-24 is documented as closed but base.html still preloads {stale}"
    else:
        assert stale, "G-24 looks fixed: close it in both documents"
        for name in stale:
            assert name in gap_row, f"G-24 must name the stale preload {name}"
            assert name in typography, name


def test_js_module_inventory_matches_the_source():
    inventory = _between(_design(), "## 16. Moduli JS", "## 17. ")
    for path in (STATIC / "js").glob("*.js"):
        assert f"static/js/{path.name}" in inventory, path.name
    main_js = _read(STATIC / "js" / "main.js")
    functions = set(re.findall(r"^function (init[A-Za-z]+)\(", main_js, flags=re.M))
    documented = set(re.findall(r"^\| `(init[A-Za-z]+)` \|", inventory, flags=re.M))
    assert functions == documented, (sorted(functions - documented), sorted(documented - functions))
    hooks = set(re.findall(r"`(data-[a-z-]+)", inventory))
    assert hooks, "no data-* hook documented"
    # a hook lives in main.js or in a bundled module of static/js/src/ (design V5: the navigation in nav.js)
    sources = main_js + "".join(_read(path) for path in sorted((STATIC / "js" / "src").glob("*.js")))
    for hook in hooks:
        camel = re.sub(r"-([a-z])", lambda m: m.group(1).upper(), hook[5:])
        assert hook in sources or f"dataset.{camel}" in sources, f"documented hook not in main.js or static/js/src: {hook}"


def test_breakpoints_keyframes_and_stylesheets_are_documented():
    design = _design()
    # Every layer is scanned, tokens.css included: it carries the six named tiers of the grid, and
    # a tier that changes the container or the scale is as much a breakpoint as one that moves a
    # component.
    sheets = {name: _read(STATIC / "css" / name) for name in _cascade()}
    widths = set()
    for css in sheets.values():
        widths |= set(re.findall(r"@media \((?:min|max)-width: ([0-9.]+rem)\)", css))
    assert widths
    layout = _between(design, "## 7. Griglia, breakpoint e layout", "## 8. ")
    for width in widths:
        assert f"`{width}`" in layout or f"`max-width: {width}`" in layout, (
            f"breakpoint {width} is not documented in §7"
        )
    motion = _between(design, "## 12. Motion", "## 13. ")
    # `[a-z0-9-]+`: the V2 tide keyframes are numbered (`tide-1`, `tide-2`), and the old pattern
    # matched «tide-» — a name that exists nowhere, so the guard asked the document for the wrong
    # string and would have gone on asking for it forever.
    keyframes = {name for css in sheets.values() for name in re.findall(r"@keyframes ([a-z0-9-]+)", css)}
    assert keyframes, "no keyframe left in the cascade: update §12 and this test"
    for keyframe in keyframes:
        assert f"`{keyframe}`" in motion, keyframe
    architecture = _between(design, "## 2. Architettura CSS", "## 3. ")
    imports = _cascade()
    # rglob and a relative path: the cascade moved into static/css/v2/ with design V2, and a glob
    # that only sees the top level would report every V2 layer as "imported but missing".
    #
    # `dev/` is excluded, and the exclusion is the point rather than a hole: a stylesheet under
    # static/css/dev/ serves a page that only exists when DEBUG is on, and putting it in main.css
    # would make every production visitor download it. `test_the_dev_stylesheet_stays_out_of_the
    # _production_cascade` below holds the other end of that bargain. `dist/` is excluded too: it is
    # the OUTPUT of `npm run build:css` (the bundle and the minified app sheets), not a layer;
    # tests/frontend/test_css_bundle_is_current.py holds it to its sources.
    #
    # Design V5 (V5.4 plan §2.3, DL54-15): a `_`-prefixed sheet is a partial. Every NON-partial sheet of static/css is
    # a layer of main.css; a partial is imported by at least one entry — main.css (the legacy shim is one) or an app
    # entry (the page sheets, the console entry) — directly or through the sheets those import.
    on_disk = sorted(
        p.relative_to(STATIC / "css").as_posix()
        for p in (STATIC / "css").rglob("*.css")
        if p.name != "main.css" and p.parent.name != "dev" and "dist" not in p.relative_to(STATIC / "css").parts
    )
    layers = [name for name in on_disk if not name.rsplit("/", 1)[-1].startswith("_")]
    assert not set(layers) - set(imports) and not set(imports) - set(on_disk), (
        f"main.css and static/css disagree: not imported {sorted(set(layers) - set(imports))}, "
        f"imported but missing {sorted(set(imports) - set(on_disk))}"
    )
    reached: set[Path] = set()
    todo = [(STATIC / "css" / "main.css").resolve(), *(p.resolve() for p in _page_sheets())]
    while todo:
        sheet = todo.pop()
        for target in re.findall(r'@import url\("([^"]+)"\)', re.sub(r"/\*.*?\*/", "", _read(sheet), flags=re.S)):
            path = _imported_sheet(sheet, target)
            if path is not None and path not in reached:
                reached.add(path)
                todo.append(path)
    partials = [STATIC / "css" / name for name in on_disk if name.rsplit("/", 1)[-1].startswith("_")]
    partials += _design_system_partials()
    orphans = sorted({p.relative_to(ROOT).as_posix() for p in partials if p.resolve() not in reached})
    assert not orphans, f"partials that no entry imports: {orphans}"
    # V1's tokens open the cascade; design V5 closes it (V5.4 plan §2.3): the faces, the tokens, the aliases
    # that give the V1 / V2 / V4 names their V5 values, and the base roles, after every V4 layer.
    assert imports[0] == "tokens.css", imports
    # the foundation's four sheets first, then the families' sheets (chrome.css, W2-C1 …) in plan §2.3's order
    v5 = [name for name in imports if name.startswith("v5/")]
    assert imports[-len(v5) :] == v5, imports
    assert v5[:4] == ["v5/fonts.css", "v5/tokens.css", "v5/aliases.css", "v5/base.css"], imports
    assert "fonts.css" not in imports, "the V4 fonts.css left the cascade with its faces"
    positions = [architecture.index(f"| `{name}` |") for name in imports]
    assert positions == sorted(positions), "the cascade order in §2 differs from main.css"
    sections = re.findall(r"^   (\d+)\. ", sheets["components.css"], flags=re.M)
    assert f"{len(sections)} sezioni numerate" in architecture


def test_the_dev_stylesheet_stays_out_of_the_production_cascade():
    """
    A stylesheet under static/css/dev/ is loaded by a DEBUG-only template and by nothing else.

    The cascade test above stops asking whether these files are imported. This one asks the
    opposite question, so that the exemption cannot quietly become a way of smuggling a layer into
    the site: nothing under dev/ may appear in main.css, and every one of those files must be
    referenced by a template under templates/dev/ — the directory whose pages are unreachable
    without DEBUG.
    """
    dev_sheets = sorted((STATIC / "css" / "dev").glob("*.css"))
    if not dev_sheets:
        pytest.skip("no development stylesheet")
    main_css = _read(STATIC / "css" / "main.css")
    dev_templates = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "templates" / "dev").rglob("*.html"))
    for sheet in dev_sheets:
        assert f"dev/{sheet.name}" not in main_css, f"{sheet.name} is in the production cascade"
        assert f"css/dev/{sheet.name}" in dev_templates, f"{sheet.name} is loaded by no development template"


def test_documented_illustrations_exist():
    on_disk = {p.name for p in (STATIC / "img" / "illustrations").glob("*.svg")}
    section = _between(_design(), "### 14.1 ", "### 14.2 ")
    listed = set(re.findall(r"^\| `([a-z-]+\.svg)` \|", section, flags=re.M))
    assert listed == on_disk, (sorted(on_disk - listed), sorted(listed - on_disk))


# ---------------------------------------------------------------------------------------------
# Citations: paths, tests, screenshots
# ---------------------------------------------------------------------------------------------
def test_cited_paths_exist():
    # G-16 is closed: docs/I18N_RTL.md was written, so there is no exemption left.
    pattern = re.compile(r"^(?:templates|static|apps|tests|scripts|docs|config)/[^\s*{}<>]*$")
    for path, text in ((DESIGN_DOC, _design()), (A11Y_DOC, _a11y())):
        for span in _code_spans(text):
            target = span.split("::", 1)[0]
            if not pattern.match(target) or target.endswith(".png"):
                continue
            assert (ROOT / target).exists(), f"{path.name} cites a path that does not exist: {target}"


def test_cited_tests_exist():
    cited = 0
    for path, text in ((DESIGN_DOC, _design()), (A11Y_DOC, _a11y())):
        for file_name, test_name in re.findall(r"`(tests/[a-z_/]+\.py)::(test_[a-z0-9_]+)`", text):
            source = ROOT / file_name
            assert source.exists(), f"{path.name}: {file_name}"
            assert re.search(rf"^def {test_name}\(", _read(source), flags=re.M), (
                f"{path.name}: {file_name}::{test_name}"
            )
            cited += 1
    assert cited >= 25, cited


def test_referenced_screenshots_can_be_produced_by_the_capture_script():
    module = _capture_module()
    expected = {f"{page}-{lang}-{width}" for page in module.PAGES for lang in module.LANGS for width in module.WIDTHS}
    for template in re.findall(r'shot\(\s*f?"([^"]+)"', _read(CAPTURE_SCRIPT)):
        if "{key}" in template:
            continue
        expected |= {template.replace("{lang}", lang) for lang in module.LANGS}
    assert set(module.WIDTHS) == {390, 768, 1440}
    assert set(module.LANGS) == {"fr", "ar"}
    assert {"home", "privacy", "login", "404"} <= set(module.PAGES)
    referenced = set()
    for text in (_design(), _a11y()):
        referenced |= set(re.findall(r"`docs/qa/design/([a-z0-9-]+)\.png`", text))
    assert len(referenced) >= 30, len(referenced)
    unknown = sorted(referenced - expected)
    assert not unknown, f"screenshots cited in the docs that capture.py never writes: {unknown}"
    for page in ("home", "privacy", "login", "404"):
        for width in (390, 768, 1440):
            assert f"{page}-fr-{width}" in referenced, (page, width)
    assert any(name.endswith(("-ar-390", "-ar-768", "-ar-1440")) for name in referenced)


# ---------------------------------------------------------------------------------------------
# Accessibility document
# ---------------------------------------------------------------------------------------------
def _checklist_rows() -> list[list[str]]:
    table = _between(_a11y(), "<!-- wcag-checklist:start -->", "<!-- wcag-checklist:end -->")
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table.splitlines()
        if re.match(r"^\| \d", line)
    ]


def test_wcag_checklist_lists_every_a_and_aa_criterion():
    rows = _checklist_rows()
    numbers = [row[0] for row in rows]
    assert len(numbers) == len(set(numbers)), "duplicated success criterion"
    assert set(numbers) == set(WCAG_22_A_AA), (
        sorted(set(WCAG_22_A_AA) - set(numbers)),
        sorted(set(numbers) - set(WCAG_22_A_AA)),
    )
    tally: Counter[str] = Counter()
    for number, _name, level, status, implementation in (row[:5] for row in rows):
        assert level == WCAG_22_A_AA[number], (number, level)
        matched = [s for s in CHECKLIST_STATUSES if status.startswith(s)]
        assert matched, (number, status)
        tally[matched[0]] += 1
        assert len(implementation) > 15, number
        if matched[0] == "Parziale":
            assert re.search(r"G-\d\d", status), f"{number}: a partial criterion must name its gap"
    summary = re.search(
        r"Riepilogo: (\d+) criteri — (\d+) conformi, (\d+) parziali, (\d+) da confermare in QA, (\d+) non applicabili",
        _a11y(),
    )
    assert summary, "summary line missing under the checklist"
    total, ok, partial, todo, na = (int(g) for g in summary.groups())
    assert total == len(rows) == 55
    assert (ok, partial, todo, na) == (
        tally["Conforme"],
        tally["Parziale"],
        tally["Da confermare in QA"],
        tally["Non applicabile"],
    )


def test_known_gaps_are_numbered_consistently_across_both_documents():
    a11y = _a11y()
    gaps_table = a11y.split("## 13. Lacune note", 1)[1]
    ids = re.findall(r"^\| (G-\d\d) \|", gaps_table, flags=re.M)
    assert ids == [f"G-{n:02d}" for n in range(1, len(ids) + 1)], ids
    assert len(ids) >= 18
    assert f"G-01 … {ids[-1]}" in a11y and f"G-01 … {ids[-1]}" in _design()
    for text in (_design(), a11y):
        for ref in set(re.findall(r"G-\d\d", text)):
            assert ref in ids, f"reference to an undefined gap: {ref}"
    design_gaps = re.findall(r"^\| (G-\d\d) \|", _design().split("## 21. Difetti noti", 1)[1], flags=re.M)
    assert design_gaps and set(design_gaps) <= set(ids)


def test_keyboard_model_covers_every_interactive_component():
    keyboard = _between(_a11y(), "## 3. Modello tastiera", "## 4. ")
    for needle in (
        "Skip link",
        "details[data-dropdown]",
        "«Il portico»",
        "Drawer",
        "templates/components/tabs.html",
        "templates/components/accordion.html",
        "templates/components/dialog.html",
        "templates/components/form_field.html",
        "templates/components/account_menu.html",
        "[data-stepper]",
        "Paginazione",
        "stretched link",
    ):
        assert needle in keyboard, needle


def _v5(name: str) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(STATIC / "css" / "v5" / name), flags=re.S)


def test_focus_and_motion_claims_match_the_stylesheets():
    base = _read(STATIC / "css" / "base.css")
    # The one focus system of design V5 (V5.4 plan §1.6), in static/css/v5/base.css — V1's navy two-tone
    # ring left base.css in W1-A's deletion step: `:focus-visible` only, a 2 px ring at a 2 px offset on the
    # element's own radius, no halo but on text fields, Highlight in forced colours, laguna-400 inside a night
    # context (the token is re-pointed there, so no selector has to repeat the ring).
    v5_base = _v5("base.css")
    focus = _between(v5_base, "\n:focus-visible {", "}")
    for declaration in (
        "outline: var(--focus-ring-width) solid var(--focus-ring)",
        "outline-offset: var(--focus-ring-offset)",
        "box-shadow: none",
    ):
        assert declaration in focus, declaration
    assert "border-radius" not in focus, "the ring follows the element's own radius"
    assert "box-shadow: 0 0 0 5px var(--focus-halo)" in v5_base, "the halo belongs to text fields"
    assert "outline: 2px solid Highlight" in _between(v5_base, "@media (forced-colors: active) {", "}\n}")
    assert ":focus-visible" not in re.sub(r"/\*.*?\*/", "", base, flags=re.S).replace(".skip-link:focus-visible", "")
    v5_tokens = _v5("tokens.css")
    night = re.search(r":is\(\.on-inverse, \.rail, [^)]*\) \{([^}]*)\}", v5_tokens)
    assert night and "--focus-ring: var(--focus-ring-night)" in night.group(1), "the night contexts re-point the ring"
    assert "--focus-ring: var(--p-laguna-550)" in v5_tokens and "--focus-ring-night: var(--p-laguna-400)" in v5_tokens
    assert "--focus-ring-width: 2px" in v5_tokens and "--focus-ring-offset: 2px" in v5_tokens
    assert "scroll-padding-block-start: calc(var(--chrome-block-size) + var(--s-4))" in base
    assert "transform: translateY(-200%)" in _between(base, ".skip-link {", "}")
    # The control height is one value; its legacy name follows the V5 token (static/css/v5/aliases.css).
    assert "--control-height: var(--control-md)" in _v5("aliases.css") and "--control-md: 44px" in v5_tokens
    # Reduced motion is a state, not a switch (V5.4 plan §1.5, W1-D; ACCESSIBILITY.md §7, DS 2026 §12): V1's
    # universal `0.01ms !important` rule left components.css; static/css/v5/tokens.css zeroes the duration tokens
    # every transition and animation is written with, and its twin html.rm is the preview's flag
    # (test_rm_flag_parity.py); the smooth scroll of base.css yields to the setting on its own. The block's last
    # guard, `.reveal`'s, left with §29 (W4-B, K17): no reduced-motion block is left in components.css, and none may
    # force a duration back.
    components = re.sub(r"/\*.*?\*/", "", _read(STATIC / "css" / "components.css"), flags=re.S)
    assert "0.01ms" not in components
    for block in components.split("@media (prefers-reduced-motion: reduce)")[1:]:
        assert "!important" not in block, "no reduced-motion rule of components.css forces a duration"
    assert ".reveal" not in components, "text never waits for a reveal (K17): §29 left with W4-B"
    reduced = _between(v5_tokens, "@media (prefers-reduced-motion: reduce) {", "\n}")
    for declaration in (
        "--motion-fast: 0ms",
        "--motion-standard: 0ms",
        "--motion-key: 0ms",
        "--spring-snappy-duration: 0ms",
    ):
        assert declaration in reduced and declaration in _between(v5_tokens, "\nhtml.rm {", "}"), declaration
    assert "--motion-reduced" not in reduced and "--motion-wait" not in reduced, "a threshold and the one fade stay"
    assert "scroll-behavior: auto" in _between(base, "@media (prefers-reduced-motion: reduce) {", "}")
    shell = _read(ROOT / "templates" / "base.html")
    assert '<a class="skip-link" href="#main-content">' in shell
    assert '<main id="main-content" tabindex="-1">' in shell
    assert 'role="status" aria-live="polite"' in shell


def test_form_field_contract_matches_accessibility_doc():
    """The aria wiring published in ACCESSIBILITY.md §6 is what the component really renders."""
    from django import forms
    from django.template.loader import render_to_string
    from django.utils import translation

    class DemoForm(forms.Form):
        email = forms.EmailField(label="Adresse e-mail", help_text="Aide")
        consent = forms.BooleanField(label="Consentement", required=True)

    form = DemoForm(data={"email": "invalide"})
    assert not form.is_valid()
    with translation.override("fr"):
        field = render_to_string("components/form_field.html", {"field": form["email"]})
        checkbox = render_to_string("components/form_field.html", {"field": form["consent"]})
        pristine = render_to_string("components/form_field.html", {"field": DemoForm()["email"]})
    assert '<label class="form-field__label" for="id_email">' in field
    assert 'aria-invalid="true"' in field
    assert 'aria-describedby="id_email_helptext id_email_error"' in field
    assert 'id="id_email_helptext"' in field
    assert '<div class="form-field__errors" id="id_email_error" role="alert"><ul class="form-field__error-list">' in field
    assert '<div class="form-field__help" id="id_email_helptext">' in field
    assert '<span class="form-field__required" aria-hidden="true">*</span>' in field
    ids = set(re.findall(r'\sid="([^"]+)"', field))
    for described in re.findall(r'aria-describedby="([^"]+)"', field):
        assert set(described.split()) <= ids, described
    assert 'class="form-field__check"' in checkbox and 'aria-describedby="id_consent_error"' in checkbox
    assert checkbox.index("<input") < checkbox.index("<label")
    assert "aria-invalid" not in pristine and 'aria-describedby="id_email_helptext"' in pristine
    documented = _between(_a11y(), "## 6. Contratto di accessibilità dei form", "## 7. ")
    for fragment in (
        'aria-describedby="id_email_helptext id_email_error"',
        'id="id_email_error" role="alert"',
        'aria-invalid="true"',
        'aria-hidden="true">*</span>',
    ):
        assert fragment in documented, fragment


# ---------------------------------------------------------------------------------------------
# App-level stylesheets and scripts (DESIGN_SYSTEM.md §2.1)
# ---------------------------------------------------------------------------------------------
# Stylesheets documented as outside the design system, with the gap that owns the defect. Empty
# again since G-25 was closed on 2026-09-21 (the shim now declares the six custom properties that
# ecosystem.css and pages.css were calling into the void); G-22 (forum.css, wizard.css) closed on
# 2026-09-20. Every app stylesheet is therefore checked strictly. The mechanism stays for the next
# one: an entry here must be marked «non conforme» in §2.1 and must name NON_CONFORMING_GAP, and
# test_stage1_app_stylesheets_use_only_design_tokens must carry an xfail for that gap.
NON_CONFORMING_GAP = "G-25"
KNOWN_NON_CONFORMING_APP_STYLESHEETS: set[str] = set()


def _app_stylesheets() -> list[Path]:
    return sorted((ROOT / "apps").glob("*/static/**/*.css"))


def _declared(path: Path) -> set[str]:
    return set(re.findall(r"(?<![\w-])(--[a-z0-9-]+)\s*:", re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)))


def _vocabulary_before(path: Path) -> set[str]:
    """The custom properties a partial may read from the partials an entry imports BEFORE it: it composes their
    vocabulary (the w3-d merge: the journey's v5/_journey-rail.css and v5/_journey-stepper.css on
    v5/_journey-nodes.css — one line, three nodes, written once). Only sibling imports (resolved next to the entry, as
    in the collected tree, DS 2026 §2) are read; an import of static/css/v5/ is a partial of its own grammar."""
    names: set[str] = set()
    if not path.name.startswith("_"):
        return names
    for entry in _app_stylesheets():
        if entry.name.startswith("_"):
            continue
        refs = re.findall(r'@import url\("([^"]+)"\);', _read(entry))
        sources = [(entry.parent / ref).resolve() for ref in refs if not ref.startswith("../")]
        if path.resolve() in sources:
            for earlier in sources[: sources.index(path.resolve())]:
                names |= _declared(earlier)
    return names


def _stylesheet_violations(path: Path) -> list[str]:
    """Design-system rules for a stylesheet outside static/css: real tokens only, no literal colour."""
    css = re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)
    css = re.sub(r"url\(\"data:[^\"]+\"\)", "", css)
    known = set(_tokens()) | _component_custom_properties() | set(re.findall(r"(?<![\w-])(--[a-z0-9-]+)\s*:", css))
    known |= _vocabulary_before(path)
    violations = [f"unknown token {name}" for name in sorted(set(re.findall(r"var\((--[a-z0-9-]+)", css)) - known)]
    for value in re.findall(r":\s*([^;{}]+);", css):
        violations += [f"literal colour {colour}" for colour in re.findall(r"#[0-9a-fA-F]{3,8}\b", value)]
        violations += [f"literal colour {match}" for match in re.findall(r"\brgba?\([^)]*\)", value)]
        if "gradient(" in value:
            violations.append("gradient")
    return violations


def test_app_asset_inventory_is_truthful():
    """§2.1: every listed file exists, is loaded by the templates it names, and is classified."""
    section = _between(_design(), "### 2.1 ", "## 3. Token")
    rows = re.findall(r"^\| `(apps/[^`]+)`[^|]*\| ([^|]+) \| ([^|]+) \|$", section, flags=re.M)
    assert len(rows) >= 5, rows
    for asset, loaders, verdict in rows:
        assert (ROOT / asset).exists(), asset
        static_name = asset.split("/static/", 1)[1]
        cited = re.findall(r"`(templates/[^`]+\.html)`", loaders)
        assert cited, asset
        for template in cited:
            assert static_name in _read(ROOT / template), f"{template} does not load {static_name}"
        if asset.endswith(".css"):
            conforming = asset not in KNOWN_NON_CONFORMING_APP_STYLESHEETS
            assert ("non conforme" in verdict) is not conforming, (asset, verdict)
            if not conforming:
                assert NON_CONFORMING_GAP in verdict, asset
    documented = {asset for asset, _loaders, _verdict in rows}
    assert KNOWN_NON_CONFORMING_APP_STYLESHEETS <= documented


def test_conforming_app_stylesheets_use_only_design_tokens():
    """AGENT_CONVENTIONS §3: tokens through var(--…), no hard-coded colour — also outside static/css."""
    checked = 0
    for path in _app_stylesheets():
        relative = path.relative_to(ROOT).as_posix()
        if relative in KNOWN_NON_CONFORMING_APP_STYLESHEETS:
            continue
        assert _stylesheet_violations(path) == [], relative
        checked += 1
    assert checked >= 1


def test_capture_script_never_accepts_an_error_page_as_a_valid_capture():
    module = _capture_module()
    assert module.NOT_FOUND_SUFFIX == "/page-inexistante/"
    source = _read(CAPTURE_SCRIPT)
    assert 'data["status"] != data["expectedStatus"]' in source
    assert "DATABASE_URL" in source, "the usage notes must tell the reader to use a dedicated database"


# ---------------------------------------------------------------------------------------------
# Open defects kept visible. None today: G-01, G-02 and G-22 were fixed by their owners on
# 2026-09-20 and G-24, G-25 and G-27 on 2026-09-21, so their tests are plain regression tests. An
# open defect is xfail, not skipped: once the owning
# agent fixes the file the test reports XPASS and the gap can be closed in the documents. The marker is
# deliberately NOT strict: a strict xfail would turn the suite red for the agent who fixes the defect,
# and that agent cannot edit this file. The price is that an XPASS is silent, which is how G-01 and then
# G-02 went stale in the documents for a while; test_gap_status_and_xfail_markers_stay_in_lockstep keeps
# documents and markers consistent once somebody closes a gap, and
# test_capture_report_is_current_and_backs_the_documented_figures compares each gap's status with what
# the browser measured (G-02 drawer geometry, G-04 header geometry without JavaScript).
# ---------------------------------------------------------------------------------------------
def test_stage1_app_stylesheets_use_only_design_tokens():
    """The app stylesheets §2.1 declares non conforming, kept in view until their gap closes.

    G-25 closed on 2026-09-21: the shim declares the six orphaned custom properties, so the set is
    empty and every app stylesheet is checked strictly by
    test_conforming_app_stylesheets_use_only_design_tokens instead.
    """
    for relative in sorted(KNOWN_NON_CONFORMING_APP_STYLESHEETS):
        assert _stylesheet_violations(ROOT / relative) == [], relative


def test_icon_sprite_is_well_formed_xml():
    """Regression test for gap G-01 (closed on 2026-09-20): the sprite must survive a strict XML parser.

    A double hyphen inside an XML comment made browsers draw no icon at all. The icon listing test reads
    the ids with a regular expression, so this one also checks that a real parser sees the same symbols.
    """
    sprite = STATIC / "img" / "icons.svg"
    namespace = "{http://www.w3.org/2000/svg}"
    symbols = list(ET.parse(sprite).getroot().iter(f"{namespace}symbol"))
    parsed = {el.get("id") for el in symbols}
    by_regex = {f"icon-{name}" for name in re.findall(r'<symbol id="icon-([a-z0-9-]+)"', _read(sprite))}
    assert parsed and parsed == by_regex, sorted(parsed ^ by_regex)
    for el in symbols:
        assert el.get("viewBox") == "0 0 24 24", el.get("id")


def test_sticky_header_does_not_trap_fixed_drawer():
    """Regression test for gap G-02 (closed on 2026-09-20).

    A backdrop-filter (or filter, transform, perspective, contain) on .site-header makes the header the
    containing block of the position: fixed drawer it contains: the drawer collapsed to 65 px. The veil
    now lives on .site-header::before, which has no fixed descendant. Design V5 (W2-C1): the chrome moved to
    static/css/v5/chrome.css, where the same rule holds (the glass is painted by the pseudo-element). W2-C2: the
    menu below 80rem is the sheet, a trapped panel of the overlay system, which stands at the body's level, after
    the header — never inside it, whatever the header declares (docs/design-v5/QA/v54/w2-a/CONTRACT.md).
    """
    chrome = _read(STATIC / "css" / "v5" / "chrome.css")
    header_rule = _between(chrome, "\n.site-header {", "}")
    header_html = _read(ROOT / "templates" / "partials" / "header.html")
    inside = _between(header_html, "<header", "</header>")
    trapped = 'nav_variant="sheet"' in inside or "<dialog" in inside or "nav-drawer" in inside
    assert not trapped, "a menu panel sits inside the sticky header"
    assert 'nav_variant="sheet"' in header_html.split("</header>", 1)[1], "the sheet follows the header"
    for prop in ("backdrop-filter", "filter:", "transform:", "perspective:", "contain:"):
        assert not (trapped and prop in header_rule), f".site-header declares {prop} around a fixed menu panel"


def test_open_defects_are_described_where_the_reader_will_look():
    design, a11y = _design(), _a11y()
    iconography = _between(design, "## 13. Iconografia", "## 14. ")
    assert "G-01" in iconography and "chiusa" in iconography, "§13 must record G-01 and its closure"
    drawer_section = _between(design, "### 11.2 ", "### 11.3 ")
    assert "G-02" in drawer_section and "chiusa" in drawer_section, "§11.2 must record G-02 and its closure"
    assert "G-04" in drawer_section, "§11.2 describes the no-JS menu: it must name the open defect G-04"
    assert "G-23" in drawer_section, "§11.2 describes the overlay: it must name the open defect G-23"
    assert NON_CONFORMING_GAP in _between(design, "### 2.1 ", "## 3. Token")
    # The font-preload defect belongs where a reader looks for the loading strategy, not only in
    # the gap table.
    assert "G-24" in _between(design, "### 6.4 ", "### 6.5 ")
    for test_name in (
        "test_icon_sprite_is_well_formed_xml",
        "test_sticky_header_does_not_trap_fixed_drawer",
        "test_stage1_app_stylesheets_use_only_design_tokens",
    ):
        assert test_name in a11y, test_name


# ---------------------------------------------------------------------------------------------
# Claims that used to be unguarded (found stale by the second independent review)
# ---------------------------------------------------------------------------------------------
def _design_system_css() -> str:
    """Every sheet of the design system, the demolition scaffold included.

    The scaffold is part of the cascade and it consumes real tokens (that is its whole job), so a
    token it uses is genuinely consumed and is not a reserve. Design V5 (V5.4 plan §2.3) moves page-only
    and console-only CSS out of main.css into partials, which the page sheets and the console entry import:
    those partials are the design system's wherever they live, and are read too. The app sheets' own rules
    — the page sheets', the console entry's — stay out of scope on purpose (see the test): an app
    stylesheet may consume a reserve token, which is what a reserve is for.
    """
    sources = [*(STATIC / "css" / name for name in _cascade()), *_design_system_partials()]
    return "".join(_read(path) for path in sources)


def test_reserve_labels_match_the_design_system_stylesheets():
    """§3: «riserva» means no rule of static/css consumes the token, and the label is true both ways.

    Scoped to static/css deliberately: an app stylesheet may consume a reserve token (that is what a
    reserve is for), and such a legitimate change must not turn the suite red for an agent who cannot
    edit the document.
    """
    css = _design_system_css()
    reference = _between(_design(), "## 3. Token", "### 3.19 ")
    assert "nessun foglio di `static/css/`" in reference, "§3 must define «riserva» with its real scope"
    rows = re.findall(r"^\| `(--[a-z0-9-]+)` \| `[^`]+` \| [^|]* \| ([^|]*) \|$", reference, flags=re.M)
    assert len(rows) == len(_tokens())
    for name, use in rows:
        consumers = len(re.findall(rf"var\({re.escape(name)}\s*[,)]", css))
        if use.strip().startswith("riserva"):
            assert not consumers, f"{name} is labelled «riserva» but static/css consumes it {consumers}x"
        else:
            assert consumers, f"{name} is documented as used but nothing in static/css consumes it"


def _templates_including(component: str) -> set[str]:
    found = set()
    for root in (ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))):
        for path in root.rglob("*.html"):
            relative = path.relative_to(ROOT).as_posix()
            if not relative.startswith("templates/components/") and f"components/{component}" in _read(path):
                found.add(relative)
    return found


def test_usato_in_minimum_counts_are_true():
    """«e almeno altri N» is a floor, not an exact count: templates added by other agents keep it true."""
    checked = 0
    for name, body in _component_sections().items():
        used_in = _bullet(body, "Usato in")
        assert not re.search(r"\be\s+altri\s+\d+", used_in), (
            f"{name}: an exact «e altri N» count goes stale within hours; write «e almeno altri N»"
        )
        match = re.search(r"e\s+almeno\s+altri\s+(\d+)", used_in)
        if not match:
            continue
        cited = set(re.findall(r"`(templates/[^`\s]+\.html)`", used_in))
        others = _templates_including(name) - cited
        assert len(others) >= int(match.group(1)), (name, len(others), match.group(1))
        checked += 1
    assert checked >= 5, checked


def test_capture_report_is_current_and_backs_the_documented_figures():
    """§10, §15, G-01 and G-02 quote capture-report.json: it must come from the current capture.py."""
    import json

    module = _capture_module()
    report = json.loads(_read(CAPTURE_SCRIPT.parent / "capture-report.json"))
    expected = {f"{page}-{lang}-{width}" for page in module.PAGES for lang in module.LANGS for width in module.WIDTHS}
    for template in re.findall(r'shot\(\s*f?"([^"]+)"', _read(CAPTURE_SCRIPT)):
        if "{key}" not in template:
            expected |= {template.replace("{lang}", lang) for lang in module.LANGS}
    assert set(report) == expected, sorted(set(report) ^ expected)
    required = ("status", "expectedStatus", "overflow", "external", "h1", "hiddenReveal", "icons", "emptyIcons")
    for name, data in report.items():
        for key in required:
            assert key in data, f"{name}: no «{key}»: the report predates the current capture.py, regenerate it"
        assert data["status"] == data["expectedStatus"], name
        assert not data["overflow"] and not data["external"] and data["h1"] == 1, name
        assert not data["hiddenReveal"] and not data.get("hiddenRevealAfterSafetyNet"), name
        assert data["emptyIcons"] == 0 and data["icons"] > 0, f"{name}: icons are not drawn (G-01 regression)"
    design, a11y = _design(), _a11y()
    assert f"**{len(report)} catture" in _between(design, "## 19. Screenshot QA", "## 20. ")
    laid_out = sum(data["icons"] for data in report.values())
    assert f"{laid_out} icone disposte" in _between(design, "## 13. Iconografia", "## 14. ")
    gap_rows = _gap_rows(a11y, "## 13. Lacune note")
    drawer_section = _between(design, "### 11.2 ", "### 11.3 ")
    # G-02: the status written in the documents must be the one the browser measured, and the figures
    # quoted next to it must be the measured ones (phone and 1024 px: the drawer applies below 80rem).
    for name in ("state-drawer-open-fr-390", "state-drawer-open-fr-1024"):
        drawer = report[name]["drawer"]
        assert set(drawer) == {
            "height",
            "contentHeight",
            "overlayHeight",
            "expectedHeight",
            "overlayTop",
            "headerBottom",
            "top",
        }, f"{name}: the report predates the current capture.py, regenerate it"
        fills_the_screen = drawer["height"] >= drawer["expectedHeight"] - 2
        if "chiusa" in gap_rows["G-02"]:
            assert fills_the_screen, f"{name}: G-02 is documented as closed but the drawer is collapsed again"
            assert drawer["overlayHeight"] >= drawer["expectedHeight"], f"{name}: the overlay does not cover the page"
        else:
            assert not fills_the_screen, "G-02 looks fixed: close it in both documents"
        for text in (gap_rows["G-02"], drawer_section):
            assert f"{drawer['height']} px" in text and f"{drawer['expectedHeight']} px" in text, (name, drawer)
        # G-23: the veil never lies over the header's controls while the menu is open — the V4 drawer's scrim started
        # where the header ends; the V5 sheet (W2-C2) owns its head line from the top, «Fermer» where «Menu» was, so a
        # scrim over the rest of the letterhead is the modal's own
        veils_the_header = drawer["overlayTop"] < drawer["headerBottom"] - 1 and drawer["top"] > 0
        if "chiusa" in gap_rows["G-23"]:
            assert not veils_the_header, f"{name}: G-23 is documented as closed but the overlay still covers the header"
        else:
            assert veils_the_header, "G-23 looks fixed: close it in both documents"
            for text in (gap_rows["G-23"], drawer_section):
                assert f"{drawer['overlayTop']} px" in text and f"{drawer['headerBottom']} px" in text, (name, drawer)
    # G-04: without JavaScript the sticky header must not hold a menu that hides the page.
    for name in ("a11y-nojs-fr-390", "a11y-nojs-fr-1024"):
        header = report[name]["header"]
        assert set(header) == {"height", "viewportHeight", "position"}, name
        hides_the_page = header["position"] == "sticky" and header["height"] > header["viewportHeight"] / 2
        if "chiusa" in gap_rows["G-04"]:
            assert not hides_the_page, f"{name}: G-04 is documented as closed but the header still hides the page"
        else:
            assert hides_the_page, "G-04 looks fixed: close it in both documents"
            for text in (gap_rows["G-04"], drawer_section):
                assert f"{header['height']} px" in text, (name, header)
    # G-05: after an invalid submit the focus belongs on the error summary (#form-errors).
    for name in ("state-form-errors-fr-390", "state-form-errors-ar-390"):
        assert "focus" in report[name], f"{name}: no «focus»: the report predates the current capture.py"
        on_summary = report[name]["focus"] == "form-errors"
        if "chiusa" in gap_rows["G-05"]:
            assert on_summary, f"{name}: G-05 is documented as closed but the focus lands on {report[name]['focus']}"
        else:
            assert not on_summary, "G-05 looks fixed: close it in both documents"


def test_gap_status_and_xfail_markers_stay_in_lockstep():
    """A gap marked «chiusa» keeps no xfail marker, an xfail'ed gap is not marked closed, and the two
    documents agree on which gaps are closed."""
    # Every gap found so far is closed, so no xfail marker is left; the set stays computed so that a
    # future open defect (new xfail) is again checked against the two documents.
    still_xfail = set(re.findall(r'@pytest\.mark\.xfail\(\s*reason="(G-\d\d)', _read(Path(__file__))))

    a11y_rows = _gap_rows(_a11y(), "## 13. Lacune note")
    design_rows = _gap_rows(_design(), "## 21. Difetti noti")
    closed = {gap for gap, row in a11y_rows.items() if "chiusa" in row}
    assert {"G-01", "G-02", "G-22"} <= closed, "G-01, G-02 and G-22 were fixed by their owners and verified"
    assert not closed & still_xfail, f"closed in the documents but still xfail here: {sorted(closed & still_xfail)}"
    for gap, row in design_rows.items():
        assert ("chiusa" in row) is (gap in closed), f"{gap}: the two documents disagree on whether it is closed"
    for gap in still_xfail:
        assert gap in a11y_rows, gap


def test_navigation_breakpoint_is_consistent_and_documented():
    """The navigation's thresholds live in chrome.css and in nav.js: both must agree with the documents.

    Design V5 «Il portico» (W2-C1): the four doors enter the letterhead at `BAR` (64rem) and the full bar with the
    panels' photographs at `DESKTOP` (80rem), below which «Menu» and the sheet apply (the overlay system's modal
    drawer, W2-C2). Every «≥ 64rem» in the two documents went stale once already, when the threshold moved: the
    documents quote the code's numbers.
    """
    chrome = _read(STATIC / "css" / "v5" / "chrome.css")
    nav_js = _read(STATIC / "js" / "src" / "nav.js")
    desktop = re.search(r'const DESKTOP = window\.matchMedia\("\(min-width: ([0-9.]+)rem\)"\)', nav_js)
    bar = re.search(r'const BAR = window\.matchMedia\("\(min-width: ([0-9.]+)rem\)"\)', nav_js)
    assert desktop and bar, "nav.js no longer declares the DESKTOP and BAR media queries"
    threshold, doors = desktop.group(1), bar.group(1)
    drawer_block = re.search(
        r"@media \(max-width: ([0-9.]+)rem\) \{(?:(?!@media).)*?\n  \.nav-toggle \{ display: inline-flex; \}",
        chrome,
        flags=re.S,
    )
    assert drawer_block, "chrome.css no longer shows .nav-toggle in a max-width block"
    assert 0 < float(threshold) - float(drawer_block.group(1)) < 0.01, (drawer_block.group(1), threshold)
    # the sheet (W2-C2): the overlay system's modal drawer, which «Menu» opens
    assert 'href="#nav-sheet" data-overlay-open' in _read(ROOT / "templates" / "partials" / "header.html")
    assert 'data-overlay="drawer"' in _read(ROOT / "templates" / "partials" / "main_nav.html")
    assert f"@media (min-width: {doors}rem)" in chrome and f"@media (min-width: {threshold}rem)" in chrome
    assert "function initNavigation" not in _read(STATIC / "js" / "main.js"), "initNavigation moved into nav.js"

    design, a11y = _design(), _a11y()
    assert f"### 11.1 «Il portico» (≥ {doors}rem; con la fotografia da {threshold}rem)" in design
    assert f"### 11.2 Drawer (< {threshold}rem" in design
    breakpoints = _between(design, "### 7.2 ", "### 7.3 ")
    rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| `([0-9.]+)rem` \|.*$", breakpoints, flags=re.M)}
    assert threshold in rows and doors in rows, f"§7.2 has no row for {threshold}rem or {doors}rem"
    for width, row in rows.items():
        assert ("navigazione desktop" in row) is (width == threshold), (
            f"§7.2: wrong row claims the desktop navigation ({width}rem)"
        )
    assert "le quattro porte entrano nella testata" in rows[doors]
    assert f'matchMedia("(min-width: {threshold}rem)")' in breakpoints
    assert f'matchMedia("(min-width: {doors}rem)")' in breakpoints
    assert f"`max-width: {drawer_block.group(1)}rem` (drawer)" in breakpoints
    keyboard = _between(a11y, "## 3. Modello tastiera", "## 4. ")
    assert f"| «Il portico» (≥ {doors}rem" in keyboard
    assert f"| Drawer (< {threshold}rem" in keyboard


def test_documented_file_weights_are_roughly_true():
    """§2, §6.2 and §16 quote file weights: indicative figures, but they must stay within 10 % of the truth."""
    design = _design()
    architecture = _between(design, "## 2. Architettura CSS", "### 2.1 ")
    # `\d+` and a path, not `\d` and a bare file name: the cascade passed ten layers and moved into
    # a subdirectory when design V2 landed (static/css/v2/…), and a guard that cannot read the
    # table it checks silently stops checking it.
    rows = re.findall(r"^\| \d+ \| `([a-z0-9_/-]+\.css)` \| (?:≈ )?([0-9.]+) KB \|", architecture, flags=re.M)
    assert [name for name, _ in rows] == _cascade(), rows
    for name, documented in rows:
        actual = (STATIC / "css" / name).stat().st_size / 1024
        assert abs(actual - float(documented)) / actual <= 0.10, (name, documented, round(actual, 1))
    scripts = re.search(r"≈ ([0-9.]+) KB non compressi in totale", _between(design, "## 16. Moduli JS", "## 17. "))
    assert scripts, "§16 no longer states the total weight of static/js"
    actual = sum(p.stat().st_size for p in (STATIC / "js").glob("*.js")) / 1024
    assert abs(actual - float(scripts.group(1))) / actual <= 0.10, (scripts.group(1), round(actual, 1))
    fonts = re.search(r"≈ ([0-9]+) KB in totale", _between(design, "### 6.2 ", "### 6.3 "))
    assert fonts, "§6.2 no longer states the total weight of static/fonts"
    actual = sum(p.stat().st_size for p in (STATIC / "fonts").glob("*.woff2")) / 1024
    assert abs(actual - float(fonts.group(1))) / actual <= 0.10, (fonts.group(1), round(actual))


def test_base_template_stylesheet_links_match_the_documented_architecture():
    """§2: the bundle built from main.css is the only stylesheet applied, and no layer is preloaded
    — they are IN the bundle (Gate A, 26/09/2026: 21 requests held the connections for 1.3 s)."""
    shell = _read(ROOT / "templates" / "base.html")
    applied = re.findall(r"<link rel=\"stylesheet\" href=\"\{% static '([^']+)' %\}\">", shell)
    assert applied == ["css/dist/main.css"], applied
    preloaded = re.findall(r"<link rel=\"preload\" href=\"\{% static 'css/([^']+)' %\}\" as=\"style\">", shell)
    assert preloaded == [], preloaded
    architecture = _between(_design(), "## 2. Architettura CSS", "### 2.1 ")
    assert "npm run build:css" in architecture and "css/dist/main.css" in architecture, (
        "§2 must say that base.html applies the bundle and how it is built"
    )
