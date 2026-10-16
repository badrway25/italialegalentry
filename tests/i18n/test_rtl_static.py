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

#: Every project stylesheet, recursively (design V5, V5.4 plan §2.5: a top-level glob would let
#: static/css/v5/ and every later layer escape the guard) — the bundles in dist/ and the DEBUG-only
#: sheets in dev/ excepted.
STYLESHEETS = sorted(
    [
        *(
            path
            for path in (ROOT / "static" / "css").rglob("*.css")
            if not {"dist", "dev"} & set(path.relative_to(ROOT / "static" / "css").parts)
        ),
        *(ROOT / "apps").glob("*/static/**/*.css"),
    ]
)
#: LTR stage geometry that is drawn, not laid out, and never mirrors (the door stage, the loader light:
#: plan §2.5, DL54-08): a physical property is allowed in these selectors only. Empty until W1-D and
#: W2-B bring those sheets; each entry names its sheet and its selector.
LTR_STAGE_ALLOW_LIST: dict[str, set[str]] = {}

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
#: A box placed at the physical centre (`inset: 50% auto auto 50%`, or `inset: 50%`) and pulled back by half its
#: own size is centred whatever the direction (the hit extensions of the chips and the busy button, seen since
#: the guard became recursive): its -50 % shift needs no [dir="rtl"] twin. `inset-inline-start: 50%` is NOT
#: centred — in RTL it anchors the right edge, which is RTL-06's case — and stays checked.
_CENTRED = re.compile(r"(?<![\w-])inset\s*:\s*50%(?:\s+auto\s+auto\s+50%)?\s*(?:;|$)")


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
    relative = {path.relative_to(ROOT).as_posix() for path in STYLESHEETS}
    assert {"static/css/v5/tokens.css", "static/css/v5/base.css", "static/css/v4/workspace.css"} <= relative
    assert not [name for name in relative if "/dist/" in name or "/dev/" in name]
    assert len(STYLESHEETS) >= 30


@pytest.mark.parametrize("path", STYLESHEETS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_stylesheet_uses_logical_properties_only(path):
    allowed = LTR_STAGE_ALLOW_LIST.get(path.relative_to(ROOT).as_posix(), set())
    physical = sorted(
        {
            match.group(0).strip()
            for selector, body in _rules(path.read_text(encoding="utf-8"))
            if selector not in allowed
            for match in _PHYSICAL.finditer(body)
        }
    )
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
            if _CENTRED.search(body) and set(shifts) == {-50.0}:
                continue  # centred on both axes from the physical centre: the same in both directions
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


#: Shifts the recursive guard found in the legacy layers when design V5 made it recursive (W1-A), each with the
#: family whose merge removes it. A known debt, not an exemption: a new entry needs an owner, and the test fails
#: when an entry is fixed and not taken off the list.
#: Empty since 9 October 2026: the one entry was V4's busy notches (`v4/buttons.css`, `.btn.is-busy::after`),
#: gone with the sheet when the L2 key of `v5/loader.css` took its place (W1-D, then W1-C's deletion).
KNOWN_UNMIRRORED: dict[str, str] = {}


def test_every_horizontal_shift_has_its_rtl_twin():
    """Also RTL-06 (fixed): the no-JS dialog fallback was centred with inset-inline-start: 50% + translateX(-50%)."""
    found = _unmirrored_shifts()
    assert [m for m in found if m not in KNOWN_UNMIRRORED] == [], (
        'add a [dir="rtl"] rule that reverses the horizontal shift'
    )
    assert sorted(set(KNOWN_UNMIRRORED) - set(found)) == [], "a known shift is fixed: take it off KNOWN_UNMIRRORED"


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

    Design V5, type «Una voce» (V5.4 plan §1.1): Vazirmatn carries every Arabic role — titles at 600 with
    no ×1.15, reading text, the console — the most coherent Arabic of the four systems measured (one
    family, no Naskh beside a sans; TYPOGRAPHY_REVIEW §3.B). The Arabic stack holds the Latin pair right
    after the Arabic face, so the digits and the Latin runs of an Arabic page are Host Grotesk's; and V1's
    two family names, which tokens.css re-points on :root:lang(ar), follow the same stack through
    static/css/v5/aliases.css. Provisional until the Moroccan reader's review (owner item B2).
    """
    tokens = (ROOT / "static" / "css" / "tokens.css").read_text(encoding="utf-8")
    block = re.search(r":root:lang\(ar\),?[^{]*\{([^}]*)\}", tokens)
    assert block, "tokens.css declares no Arabic block"
    body = block.group(1)
    assert "--font-display: var(--font-display-ar)" in body
    assert "--font-ui: var(--font-ui-ar)" in body
    # Tracking breaks Arabic joining, so the tracked-caps register is neutralised.
    assert "--track-folio: 0" in body

    v5 = _COMMENT.sub("", (ROOT / "static" / "css" / "v5" / "tokens.css").read_text(encoding="utf-8"))
    stack = re.search(r"--f-sans-ar:\s*([^;]+);", v5)
    assert stack and stack.group(1).startswith('"Vazirmatn", "Host Grotesk"'), stack
    arabic = re.search(r"(?m)^:lang\(ar\)\s*\{([^}]*)\}", v5)
    assert (
        arabic and "--f-sans: var(--f-sans-ar)" in arabic.group(1) and "--f-serif: var(--f-sans-ar)" in arabic.group(1)
    )
    aliases = _COMMENT.sub("", (ROOT / "static" / "css" / "v5" / "aliases.css").read_text(encoding="utf-8"))
    assert "--font-display-ar: var(--f-sans-ar)" in aliases and "--font-ui-ar: var(--f-sans-ar)" in aliases

    fonts = (ROOT / "static" / "css" / "v5" / "fonts.css").read_text(encoding="utf-8")
    assert 'font-family: "Vazirmatn"' in fonts
    for retired in ("Noto Naskh Arabic", "IBM Plex Sans Arabic", "Markazi Text"):
        assert f'font-family: "{retired}"' not in fonts, retired
    assert "http" not in fonts, "fonts are self-hosted (CSP self-only)"


def test_previous_page_icon_points_backwards_in_both_directions():
    """RTL-07 (fixed): the « previous » link used the forward arrow with a class no stylesheet defined.

    Design V5 (the icon system, V5.4 plan §1.7 «RTL»): «Précédent» draws a back arrow of its own, `arrow-start`,
    and «Suivant» the forward `arrow`; both are on the closed flip list, so the svg_icon tag gives each
    `icon--flip-rtl` and base.css mirrors it under [dir="rtl"] — each points the way its word says in French and
    in Arabic. The V4 mechanism (the forward arrow turned by `.pagination__icon-prev`) is no longer drawn."""
    from django.template import Context, Template

    from core import icons

    template = (ROOT / "templates" / "components" / "pagination.html").read_text(encoding="utf-8")
    previous = template[template.index('rel="prev"') : template.index("</a>", template.index('rel="prev"'))]
    following = template[template.index('rel="next"') : template.index("</a>", template.index('rel="next"'))]
    assert 'svg_icon "arrow-start"' in previous and "pagination__icon-prev" not in template
    assert 'svg_icon "arrow"' in following
    assert {"arrow-start", "arrow"} <= icons.FLIP_RTL
    drawn = Template('{% svg_icon "arrow-start" "icon icon--sm" %}').render(Context({}))
    assert 'class="icon icon--sm icon--flip-rtl"' in drawn and "#icon-arrow-start" in drawn
    rules = dict(_rules((ROOT / "static" / "css" / "base.css").read_text(encoding="utf-8")))
    assert "scaleX(-1)" in rules.get('[dir="rtl"] .icon--flip-rtl', "")
