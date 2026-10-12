"""
RTL implementation rules checked statically on every project stylesheet (docs/I18N_RTL.md §7) — no browser,
no database:

* logical properties only: no ``left`` / ``right`` offsets, margins, paddings, borders, floats or alignments;
* a horizontal ``translate`` is direction-dependent, so every rule that uses one needs its ``[dir="rtl"]`` twin;
* the bidi helpers keep Latin data (e-mail, telephone, URL, number, password, code, dates) left-to-right inside
  an Arabic page, and the semantic icon mirroring class exists.
"""

from __future__ import annotations

import re

import pytest

from .conftest import ROOT

pytestmark = pytest.mark.compliance

STYLESHEETS = sorted(
    [
        *(ROOT / "static" / "css").glob("*.css"),
        *(ROOT / "apps").glob("*/static/**/*.css"),
    ]
)

_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
_PHYSICAL = re.compile(
    r"(?<![\w-])(?:"
    r"(?:margin|padding|border|inset|scroll-margin|scroll-padding)-(?:left|right)(?:-[a-z]+)*"
    r"|border-(?:top|bottom)-(?:left|right)-radius"
    r"|left|right"
    r")\s*:"
    r"|(?<![\w-])(?:text-align|float|clear)\s*:\s*(?:left|right)\b"
)
#: A horizontal shift, written either as a transform function — translateX(3px), translate(-50%, 0) — or with
#: the individual ``translate`` property (``translate: 3px 0``), which the design system uses for hover nudges
#: because it composes with the ``scaleX(-1)`` of a mirrored icon instead of replacing it.
_HORIZONTAL_SHIFT = re.compile(
    r"translate(?:X|3d)?\(\s*(-?[\d.]+)(?:px|rem|em|%)"
    r"|(?<![\w-])translate\s*:\s*(-?[\d.]+)(?:px|rem|em|%)"
)
_RTL_SCOPE = re.compile(r'\[dir="rtl"\]|:dir\(rtl\)')


def _rules(css: str) -> list[tuple[str, str]]:
    """Innermost ``selector { declarations }`` blocks (the rules inside @media / @supports included)."""
    found = []
    for selector, body in _RULE.findall(_COMMENT.sub("", css)):
        selector = " ".join(selector.split())
        if selector and not selector.startswith(("@", "from", "to")) and not re.fullmatch(r"[\d.%, ]+", selector):
            found.append((selector, body))
    return found


def test_the_project_stylesheets_are_found():
    names = {path.name for path in STYLESHEETS}
    assert {"tokens.css", "base.css", "layout.css", "components.css"} <= names
    assert len(STYLESHEETS) >= 6


@pytest.mark.parametrize("path", STYLESHEETS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_stylesheet_uses_logical_properties_only(path):
    css = _COMMENT.sub("", path.read_text(encoding="utf-8"))
    physical = sorted({match.group(0).strip() for match in _PHYSICAL.finditer(css)})
    assert physical == [], f"{path.name}: use the logical equivalents (inline-start / inline-end): {physical}"


def test_physical_property_detector():
    assert _PHYSICAL.search("a { margin-left: 1rem }")
    assert _PHYSICAL.search("a { left: 0 }")
    assert _PHYSICAL.search("a { text-align: right }")
    assert _PHYSICAL.search("a { border-top-left-radius: 2px }")
    assert not _PHYSICAL.search("a { margin-inline-start: 1rem; inset-inline-end: 0; text-align: end }")
    assert not _PHYSICAL.search("a { border-start-start-radius: 2px; --shadow-left: 0 }")


def _unmirrored_shifts() -> list[str]:
    missing = []
    for path in STYLESHEETS:
        rules = _rules(path.read_text(encoding="utf-8"))
        rtl_selectors = {
            _RTL_SCOPE.sub("", part).strip()
            for selector, body in rules
            if _RTL_SCOPE.search(selector) and ("transform" in body or "translate" in body)
            for part in selector.split(",")
        }
        for selector, body in rules:
            if _RTL_SCOPE.search(selector):
                continue
            shifts = [float(function or prop) for function, prop in _HORIZONTAL_SHIFT.findall(body)]
            if not any(shifts):
                continue
            missing += [
                f"{path.name}: {part.strip()}" for part in selector.split(",") if part.strip() not in rtl_selectors
            ]
    return missing


def test_horizontal_shift_detector_reads_the_transform_function_and_the_translate_property():
    def shifts(body: str) -> list[float]:
        return [float(function or prop) for function, prop in _HORIZONTAL_SHIFT.findall(body)]

    assert shifts("transform: translateX(3px)") == [3.0]
    assert shifts("transform: translate(-50%, 0) scaleX(-1)") == [-50.0]
    assert shifts("translate: -4px 0") == [-4.0]
    assert shifts("transition: translate 200ms ease-out") == []
    assert not any(shifts("translate: 0 -2px")), "a vertical nudge is not direction-dependent"
    assert not any(shifts("transform: translateY(-2px)"))


def test_every_horizontal_shift_has_its_rtl_twin():
    """Also RTL-06 (fixed): the no-JS dialog fallback was centred with inset-inline-start: 50% + translateX(-50%)."""
    assert _unmirrored_shifts() == [], 'add a [dir="rtl"] rule that reverses the horizontal shift'


def test_bidi_helpers_keep_latin_data_left_to_right():
    rules = dict(_rules((ROOT / "static" / "css" / "base.css").read_text(encoding="utf-8")))
    isolated = next((s, b) for s, b in rules.items() if ".ltr" in s.split(", ") and "unicode-bidi" in b)
    selector, body = isolated
    for needed in (
        '[dir="rtl"] input[type="email"]',
        '[dir="rtl"] input[type="tel"]',
        '[dir="rtl"] input[type="url"]',
        '[dir="rtl"] input[type="number"]',
        '[dir="rtl"] input[type="password"]',
        '[dir="rtl"] code',
        '[dir="rtl"] time[datetime]',
    ):
        assert needed in selector, needed
    assert "direction: ltr" in body and "unicode-bidi: isolate" in body
    assert "scaleX(-1)" in rules['[dir="rtl"] .icon--flip-rtl']


def test_fallback_blocks_in_another_language_are_isolated_left_to_right():
    """
    RTL-01 / RTL-09 (fixed): inside an Arabic page a French, Italian or English text element keeps its own
    direction, otherwise the final punctuation of a prescribed sentence jumps to the start of its last line.
    ``label`` matters: the locked consent sentence of every public form is a ``<label lang="fr">``.
    """
    rules = _rules((ROOT / "static" / "css" / "base.css").read_text(encoding="utf-8"))
    selector, body = next((s, b) for s, b in rules if '[lang="fr"]' in s and "unicode-bidi" in b)
    assert selector.startswith('[dir="rtl"] :is(')
    elements = {name.strip() for name in selector.split(":is(", 1)[1].split(")", 1)[0].split(",")}
    assert {"p", "h1", "h2", "h3", "li", "dd", "blockquote", "label", "td", "th", "span"} <= elements
    assert not {"a", "button", "ul", "ol", "div", "nav", "section"} & elements, "containers and links stay mirrored"
    for lang in ("fr", "it", "en"):
        assert f'[lang="{lang}"]' in selector
    assert "direction: ltr" in body and "unicode-bidi: isolate" in body


def test_arabic_has_its_own_display_and_interface_pair():
    """
    Arabic is designed, not translated.

    The build this replaces had ONE Arabic face doing all six levels, so the Arabic edition had no
    display/text contrast at all while the Latin edition had a serif and a sans. Art direction A
    gives Arabic the same pair: a true Naskh for reading — the register Moroccan administrative
    documents use, and the correct counterpart to a Latin serif — and IBM Plex Sans Arabic for the
    interface, where its Kufi-influenced construction is right.
    """
    tokens = (ROOT / "static" / "css" / "tokens.css").read_text(encoding="utf-8")
    block = re.search(r":root:lang\(ar\),?[^{]*\{([^}]*)\}", tokens)
    assert block, "tokens.css declares no Arabic block"
    body = block.group(1)
    assert "--font-display: var(--font-display-ar)" in body
    assert "--font-ui: var(--font-ui-ar)" in body
    # Tracking breaks Arabic joining, so the tracked-caps register is neutralised.
    assert "--track-folio: 0" in body

    display = re.search(r"--font-display-ar:\s*([^;]+);", tokens)
    interface = re.search(r"--font-ui-ar:\s*([^;]+);", tokens)
    assert display and "Noto Naskh Arabic" in display.group(1)
    assert interface and "IBM Plex Sans Arabic" in interface.group(1)

    fonts = (ROOT / "static" / "css" / "fonts.css").read_text(encoding="utf-8")
    for family in ("Noto Naskh Arabic", "IBM Plex Sans Arabic"):
        assert family in fonts, family
    assert "http" not in fonts, "fonts are self-hosted (CSP self-only)"


def test_previous_page_icon_points_backwards_in_both_directions():
    """RTL-07 (fixed): the « previous » link used the forward arrow with a class no stylesheet defined."""
    template = (ROOT / "templates" / "components" / "pagination.html").read_text(encoding="utf-8")
    assert "pagination__icon-prev" in template
    rules = dict(_rules((ROOT / "static" / "css" / "components.css").read_text(encoding="utf-8")))
    assert "scaleX(-1)" in rules.get(".pagination__icon-prev", "") or "rotate(180deg)" in rules.get(
        ".pagination__icon-prev", ""
    )
    assert "transform" in rules.get('[dir="rtl"] .pagination__icon-prev', "")
