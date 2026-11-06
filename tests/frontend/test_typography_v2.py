"""
Typography V2 — the guards of the type system (v524-t; V5.24 §11–§14; TYPOGRAPHY_V2 §4–§6; FINAL_DELIVERY_V2 R1, §3.1).

Static, offline, on the sources: the twelve steps declared once in static/css/v5/tokens.css; the weight map
(--w-display 600); the phone step-up and the Arabic block; the label and the numeral roles; the primary call at
16/24 600; the Arabic rules of base.css in the SUBJECT form; the three RTL minors (M1, M3, C-1); and four sheet
disciplines with a BURN-DOWN table — every `font-size` written with clamp()/min()/max() outside tokens.css, every
`font-size` that is neither a token nor a value of the scale, every `var(--f-mono)` outside the reference classes,
every «:lang(ar) descendant» / «[dir="rtl"] descendant» rule that writes a type property, and every
`text-transform: uppercase` outside the label role and the locked-caps classes — counted per sheet. The table holds
the counts measured on the tree at the lane's merge: a lane that converts its sheet LOWERS its row (to nothing, then
deletes it); a sheet that is clean may not be listed; a sheet may never rise. CLOSING asserts the table empty and
deletes it (FINAL_DELIVERY_V2 §3.9 c).

The browser twins (marked `browser`) read the Arabic product: no Arabic letters under 14 px, no multi-line Arabic
element under 1.3 em of leading, every lang="fr" element of 20 px or more on an Arabic page at its Latin leading,
no Arabic letters in an element whose first family is ILE Mono (TYPOGRAPHY_V2 §6 «Arabic guards»).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
V5 = STATIC / "css" / "v5"
TOKENS = V5 / "tokens.css"
BASE = V5 / "base.css"
BUTTONS = V5 / "buttons.css"

pytestmark = pytest.mark.compliance

# ---- the sheets the disciplines read ------------------------------------------------------------------------------


def _strip(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _sheets() -> list[Path]:
    """Every source sheet of the V5 system and of the apps: static/css/v5/** and apps/*/static/**; never dist/, never
    the preview's own dev sheets (static/css/dev/**, the design board), never the legacy layers CLOSING retires."""
    found = [*V5.glob("**/*.css"), *(ROOT / "apps").glob("*/static/**/*.css")]
    return sorted(p for p in found if "dist" not in p.parts)


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _rules(css: str) -> list[tuple[str, str]]:
    """(selector, body) of every rule of a sheet, media blocks flattened (a nested block's own braces unwrapped)."""
    css = _strip(css)
    css = re.sub(r"@(media|supports|container|layer)[^{]*\{", "", css)  # open the at-rule; its closing brace below
    return [(sel.strip(), body) for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if sel.strip()]


#: The twelve steps (TYPOGRAPHY_V2 §4.2) and the rem values a font-size may be written as when it is not a token:
#: the steps' own values, the phone step-up's and the primary call's. Everything else is a literal to burn down.
SCALE_REM = {
    "4rem",
    "3.5rem",
    "2.75rem",
    "2.25rem",
    "2.125rem",
    "1.75rem",
    "1.5rem",
    "1.375rem",
    "1.25rem",
    "1.0625rem",
    "1rem",
    "0.9375rem",
    "0.875rem",
    "0.8125rem",
    "0.75rem",
}
TOKEN_FONT_SIZE = re.compile(r"var\(--(t|u)-[a-z0-9-]+(?:-size)?\)")
#: The reference classes ILE Mono draws (TYPOGRAPHY_V2 F-3): a `var(--f-mono)` rule whose selector names only these
#: (or the elements code/kbd/pre/samp) is the mono's one seat; any other is a folio to burn down.
MONO_SEAT = re.compile(
    r"^(?:\s*(?:code|kbd|pre|samp|\.t-ref|\.ctx__ref|\.doc-workspace__ref|\.error-page__ref|\.db-ref|\.reg-ref)"
    r"(?:\s*[:>\s][^,]*)?\s*,?)+$"
)
TYPE_PROPERTY = re.compile(r"(?<![\w-])(line-height|letter-spacing|font-size)\s*:")
#: A descendant-form Arabic rule: «:lang(ar) X» or «[dir="rtl"] X» with a descendant/child after the language test
#: (the SUBJECT form `.x:lang(ar)` has nothing after it but a pseudo-class or another compound part).
ARABIC_DESCENDANT = re.compile(
    r'(?::lang\(ar\)|\[dir="rtl"\])\)?(?::not\([^)]*\))?(?:\s+[>~+]?\s*|\s*[>~+]\s*)[.\[a-z:#*]'
)
#: `text-transform: uppercase` is the label role's (and the wordmark's, and the locked capital strings'): a rule whose
#: selector names one of these is allowed; any other is an eyebrow/kicker/folio to burn down into the role.
UPPERCASE_ALLOWED = (
    ".t-label",
    ".eyebrow",
    ".t-folio",
    "h4",
    ".lock__wm",
    ".brand__wordmark",
    ".home__wordmark",
    ".page-header__wordmark",
    ".site-footer__wordmark-inline",
    ".rail__wm",
    ".rail__wordmark",
    ".hero__title",
    ".btn--upper",
)


def measure(path: Path) -> dict[str, int]:
    """The five counts of one sheet: clamp · literal · mono · ar_descendant · uppercase."""
    css = path.read_text(encoding="utf-8")
    rules = _rules(css)
    counts = {"clamp": 0, "literal": 0, "mono": 0, "ar_descendant": 0, "uppercase": 0}
    for selector, body in rules:
        for value in re.findall(r"(?<![\w-])font-size\s*:\s*([^;}]+)", body):
            value = " ".join(value.replace("!important", "").split())
            if re.search(r"\b(clamp|min|max)\(", value):
                counts["clamp"] += 1
            elif not TOKEN_FONT_SIZE.search(value) and value not in SCALE_REM and value != "inherit":
                counts["literal"] += 1
        if "var(--f-mono)" in body and not MONO_SEAT.match(" ".join(selector.split())):
            counts["mono"] += body.count("var(--f-mono)")
        if TYPE_PROPERTY.search(body):
            for part in selector.split(","):
                if ARABIC_DESCENDANT.search(part.strip()):
                    counts["ar_descendant"] += 1
                    break
        if re.search(r"text-transform\s*:\s*uppercase", body) and not any(a in selector for a in UPPERCASE_ALLOWED):
            counts["uppercase"] += 1
    return counts


#: The burn-down table — measured on the tree at v524-t's merge (FINAL_DELIVERY_V2 §3.1: «which every other lane
#: empties for its own sheets and CLOSING asserts empty»). Keys are the sheets' repository paths; a count that is not
#: listed is 0. tokens.css is never listed (its clamps ARE the scale); static/css/v5/base.css, buttons.css and
#: fonts.css are clean by construction (lane T's).
TYPOGRAPHY_BURNDOWN: dict[str, dict[str, int]] = {  # measured 5 Nov 2026 on 4bafcfa0 + T (NOTES.md §5)
    "apps/academy/static/academy/academy.css": {"mono": 1},
    "apps/accounts/static/accounts/entrance.css": {"ar_descendant": 2},
    "apps/cms/static/cms/_faq-v2.css": {"mono": 1, "uppercase": 1},
    "apps/cms/static/cms/_lessico-v2.css": {"clamp": 2, "ar_descendant": 1},
    "apps/ecosystem/static/ecosystem/_companies.css": {"clamp": 1, "mono": 1},
    "apps/ecosystem/static/ecosystem/_spazi-v2.css": {"ar_descendant": 1},
    "apps/ecosystem/static/ecosystem/_universities.css": {"mono": 1},
    "apps/forum/static/forum/_forum.css": {"clamp": 1},
    "apps/orientation/static/orientation/wizard.css": {"ar_descendant": 1, "uppercase": 1},
    "apps/pages/static/pages/css/_agami.css": {"clamp": 2, "mono": 2, "ar_descendant": 1, "uppercase": 2},
    "apps/pages/static/pages/css/_canali.css": {"clamp": 1, "ar_descendant": 1, "uppercase": 1},
    "apps/pages/static/pages/css/_contatto.css": {"clamp": 1},
    "apps/pages/static/pages/css/_frodi.css": {"clamp": 2},
    "apps/pages/static/pages/css/_rete.css": {"mono": 1, "uppercase": 1},
    "apps/pages/static/pages/css/hero.css": {"clamp": 3, "literal": 3, "uppercase": 4},
    "apps/pages/static/pages/css/pages.css": {"clamp": 2, "mono": 1, "uppercase": 1},
    "apps/pathways/static/pathways/_diplomas.css": {"mono": 1, "ar_descendant": 1},
    "apps/pathways/static/pathways/_index.css": {"mono": 1, "ar_descendant": 1, "uppercase": 1},
    "apps/pathways/static/pathways/_persone-v2.css": {"ar_descendant": 1, "uppercase": 1},
    "apps/pathways/static/pathways/_sheet.css": {"mono": 1, "ar_descendant": 1, "uppercase": 1},
    "apps/pathways/static/pathways/_training.css": {"mono": 1, "ar_descendant": 1},
    "apps/portal/static/portal/portal.css": {"literal": 1},
    "apps/portal/static/portal/v5/_dashboard.css": {"ar_descendant": 1},
    "apps/portal/static/portal/v5/_depot.css": {"ar_descendant": 1},
    "apps/portal/static/portal/v5/_frame.css": {"uppercase": 1},
    "apps/portal/static/portal/v5/_journey-rail.css": {"ar_descendant": 1},
    "apps/portal/static/portal/v5/_platform.css": {"clamp": 1, "literal": 2, "mono": 5, "uppercase": 3},
    "apps/portal/static/portal/v5/_registers.css": {"mono": 1, "ar_descendant": 1},
    "apps/portal/static/portal/v5/_shell.css": {"literal": 1, "ar_descendant": 3},
    "apps/portal/static/portal/v5/_table.css": {"ar_descendant": 1},
    "apps/portal/static/portal/v5/_workspace.css": {"mono": 1, "ar_descendant": 2},
    "static/css/v5/_formwork.css": {"literal": 1, "ar_descendant": 4, "uppercase": 1},
    # v524-lib (FINAL_DELIVERY_V2 §3.3, gate 4; TYPOGRAPHY_V2 §6): the frontispiece converted — what stays is the AGAMI name
    # device's two clamps (R3.3 «.fronte__name takes --track-display and nothing else») and the folio label's uppercase,
    # restated through the role's tokens until pages/partials/_ingresso.html (lane PX's file) carries `t-label` (LIB NOTES §4)
    "static/css/v5/_fronte.css": {"clamp": 2, "uppercase": 1},
    "static/css/v5/_glyph.css": {"ar_descendant": 1},
    "static/css/v5/_portico.css": {"ar_descendant": 3, "uppercase": 2},
    "static/css/v5/_receipt.css": {"literal": 1, "ar_descendant": 1},
    "static/css/v5/_steps.css": {"ar_descendant": 1},
    "static/css/v5/aliases.css": {"mono": 2},
    "static/css/v5/chrome.css": {"literal": 6, "ar_descendant": 5, "uppercase": 3},
    "static/css/v5/field.css": {"ar_descendant": 1},
    "static/css/v5/lume.css": {"ar_descendant": 1, "uppercase": 1},
}


def test_tokens_css_is_never_in_the_burn_down_table_and_the_table_names_real_sheets():
    assert "static/css/v5/tokens.css" not in TYPOGRAPHY_BURNDOWN
    for sheet in TYPOGRAPHY_BURNDOWN:
        assert (ROOT / sheet).exists(), sheet
        assert all(v > 0 for v in TYPOGRAPHY_BURNDOWN[sheet].values()), (sheet, "a zero is deleted, not listed")


@pytest.mark.parametrize("path", _sheets(), ids=_rel)
def test_the_burn_down_table_equals_the_measured_counts(path: Path):
    """Equality, not a ceiling: a lane that cleans a sheet lowers its row — the table is the work list, and it only
    goes down (FINAL_DELIVERY_V2 §3.1, §3.3 gate 4, §3.5–§3.7 «T's burn-down emptied for these sheets»)."""
    if path == TOKENS:
        return
    measured = {k: v for k, v in measure(path).items() if v}
    recorded = TYPOGRAPHY_BURNDOWN.get(_rel(path), {})
    assert measured == recorded, (
        f"{_rel(path)}: measured {measured}, recorded {recorded} — a sheet converted to the twelve steps lowers its row "
        f"(V5.20: cite TYPOGRAPHY_V2 §4.2 / F-3 / F-4 / F-7); a sheet may never rise"
    )


def test_the_shared_layer_is_clean():
    """T's own sheets carry no clamp, no literal, no folio, no descendant-form Arabic rule, no eyebrow (R4 c)."""
    for sheet in (BASE, BUTTONS, V5 / "fonts.css"):
        assert not {k: v for k, v in measure(sheet).items() if v}, _rel(sheet)


# ---- the tokens ------------------------------------------------------------------------------------------------------


def _root_blocks(css: str) -> list[str]:
    """The bodies of the TOP-LEVEL `:root {}` blocks of a sheet (not those inside a media or language block)."""
    css = _strip(css)
    bodies, depth, i, n = [], 0, 0, len(css)
    while i < n:
        m = re.compile(r":root\s*\{").match(css, i) if depth == 0 else None
        if m:
            j = css.index("}", m.end())
            bodies.append(css[m.end() : j])
            i = j + 1
            continue
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
        i += 1
    return bodies


def _declarations(body: str) -> dict[str, str]:
    return {name: " ".join(value.split()) for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", body)}


def _clamp_px(value: str, viewport: int) -> float:
    """A `clamp(Arem, Brem + Cvw, Drem)` at a viewport width, in px (16 px rem)."""
    m = re.fullmatch(r"clamp\(([0-9.]+)rem,\s*([0-9.]+)rem\s*\+\s*([0-9.]+)vw,\s*([0-9.]+)rem\)", value)
    assert m, value
    lo, a, b, hi = (float(x) for x in m.groups())
    return round(min(max(lo * 16, a * 16 + b * viewport / 100), hi * 16), 2)


TWELVE = {
    "--t-display": ("clamp", 44, 64, "1"),
    "--t-title-1": ("clamp", 34, 56, "1.08"),
    "--t-title-2": ("clamp", 28, 36, "1.15"),
    "--t-band": ("clamp", 24, 28, "1.25"),
    "--t-entry": ("fixed", 20, 20, "1.75rem"),
    "--t-lead": ("fixed", 20, 20, "1.75rem"),
    "--t-body": ("fixed", 17, 17, "1.75rem"),
    "--t-ui": ("fixed", 15, 15, "1.25rem"),
    "--t-small": ("fixed", 13, 13, "1.25rem"),
    "--t-caption": ("fixed", 12, 12, "1rem"),
    "--t-label": ("fixed", 13, 13, "1rem"),
    "--t-numeral": ("fixed", 28, 28, "2rem"),
}


def test_the_twelve_steps_are_declared_once_in_tokens_css_with_their_leadings():
    """TYPOGRAPHY_V2 §4.2 (V5.24 §12): four fluid steps from 390 to 1440, eight fixed, the leadings as decided; each
    declared exactly once at the top level of tokens.css (the phone and Arabic blocks re-point, never re-declare)."""
    css = TOKENS.read_text(encoding="utf-8")
    roots = _root_blocks(css)
    declared: dict[str, str] = {}
    for body in roots:
        for name, value in _declarations(body).items():
            assert name not in declared or not name.startswith("--t-"), f"{name} declared twice at the top level"
            declared[name] = value
    for name, (kind, at_390, at_1440, lh) in TWELVE.items():
        value = declared[name]
        if kind == "clamp":
            assert _clamp_px(value, 390) == at_390 and _clamp_px(value, 1440) == at_1440, (name, value)
        else:
            assert float(value.removesuffix("rem")) * 16 == at_390, (name, value)
        assert declared[name + "-lh"] == lh, (name, declared[name + "-lh"])
    assert declared["--t-numeral-lg"] == "2.25rem" and declared["--t-numeral-lg-lh"] == "2.5rem"
    assert declared["--t-field"] == "1rem"
    # the lead at 22/32 from 64 rem, for the Latin run on an Arabic page too (F-9)
    assert re.search(
        r"@media \(min-width: 64rem\)\s*\{\s*:root, :where\(:root:lang\(ar\)\) :where\(\[lang=\"fr\"\], \[lang=\"it\"\], "
        r"\[lang=\"en\"\]\)\s*\{\s*--t-lead: 1\.375rem; --t-lead-lh: 2rem;\s*\}",
        _strip(css),
    )
    # no font-size clamp anywhere else: tokens.css is the one place a fluid size is written
    assert len(re.findall(r"clamp\(", _strip(css))) >= 5  # the four steps and the console workspace title


def test_the_weight_map_tracking_and_measures():
    """400 reads · 500 acts · 600 intitles · 700 emphasis; the display line is 600 (F-1: the hero's statement was the
    lightest text on the page); tracking by size, −0.03 em at display; measures in rem."""
    declared: dict[str, str] = {}
    for body in _root_blocks(TOKENS.read_text(encoding="utf-8")):
        declared.update(_declarations(body))
    assert declared["--w-body"] == "400" and declared["--w-control"] == "500"
    assert declared["--w-title"] == "600" and declared["--w-display"] == "600"
    assert declared["--w-label"] == "600" and declared["--w-strong"] == "700"
    assert declared["--track-display"] == "-0.03em" and declared["--track-title"] == "-0.028em"
    assert declared["--track-title-2"] == "-0.02em" and declared["--track-band"] == "-0.016em"
    assert declared["--track-entry"] == "-0.012em" and declared["--track-label"] == "0.08em"
    assert declared["--measure-body"] == "36rem" and declared["--measure-lead"] == "36rem"
    assert declared["--measure-small"] == "29rem"
    # the legacy names are aliases of the twelve, never a thirteenth value (the lanes burn them down)
    assert declared["--t-plate"] == "var(--t-display)" and declared["--t-folio"] == "var(--t-label)"
    assert declared["--track-eyebrow"] == "var(--track-label)" and declared["--track-folio"] == "var(--track-label)"
    assert "--ar-console-lh" not in declared, "the Vazirmatn trio's console leading left with the face"


def test_the_public_roles_step_up_on_phones_and_under_a_coarse_pointer():
    """TYPOGRAPHY_V2 F-5 (V5.24 §13): below 48 rem or under a coarse pointer the public ui is 16/24, small, caption and
    label 14/20 — nothing under 14 px on a phone, as the Arabic floor already was; the console keeps its own step
    (TR F2), with the eyebrow at 13/20 (the label role)."""
    css = _strip(TOKENS.read_text(encoding="utf-8"))
    block = re.search(r"@media \(max-width: 47\.999rem\), \(pointer: coarse\)\s*\{(.*?)\n\}", css, flags=re.S)
    assert block, "no step-up block"
    public = re.search(r":root\s*\{([^}]*)\}", block.group(1))
    console = re.search(r"body\.console\s*\{([^}]*)\}", block.group(1))
    assert public and console
    p, c = _declarations(public.group(1)), _declarations(console.group(1))
    assert p == {
        "--t-ui": "1rem",
        "--t-ui-lh": "1.5rem",
        "--t-small": "0.875rem",
        "--t-small-lh": "1.25rem",
        "--t-caption": "0.875rem",
        "--t-caption-lh": "1.25rem",
        "--t-label": "0.875rem",
        "--t-label-lh": "1.25rem",
    }, p
    for name, value in p.items():
        if not name.endswith("-lh"):
            assert float(value.removesuffix("rem")) * 16 >= 14, name
    assert c["--u-body"] == "1rem" and c["--u-ui"] == "0.9375rem" and c["--u-small"] == "0.875rem"
    assert c["--u-caption"] == "0.8125rem" and c["--u-eyebrow"] == "0.8125rem" and c["--u-eyebrow-lh"] == "1.25rem"
    assert c["--u-ref"] == "0.875rem"


def test_the_arabic_block_and_the_latin_boundary():
    """TYPOGRAPHY_V2 §4.5, F-6, F-7: Readex Pro at ratio 1.0; the floor 14 px; titles +0.1 of leading, entry and lead
    20/32, body 17/28 as Latin (V1's Naskh leadings closed at (0,2,0)); no tracking in Arabic; and every re-pointed
    value restated at the boundary of a French, Italian or English run, so a lang="fr" element on an Arabic page keeps
    its Latin leading and tracking."""
    css = _strip(TOKENS.read_text(encoding="utf-8"))
    arabic = re.search(r"(?m)^:root:lang\(ar\), :lang\(ar\)\s*\{([^}]*)\}", css)
    assert arabic, "no Arabic block"
    a = _declarations(arabic.group(1))
    assert a["--f-sans"] == "var(--f-sans-ar)" and a["--f-serif"] == "var(--f-sans-ar)"
    assert a["--ar-lh-plus"] == "0.1"
    assert (a["--t-display-lh"], a["--t-title-1-lh"], a["--t-title-2-lh"], a["--t-band-lh"]) == (
        "1.1",
        "1.18",
        "1.25",
        "1.35",
    )
    assert a["--t-entry-lh"] == "2rem" and a["--t-lead-lh"] == "2rem"
    assert a["--t-prose-lh"] == "var(--t-body-lh)", "V1's 32 px Naskh body leading is closed on the Latin 17/28"
    for name in ("--t-small", "--t-caption", "--t-label", "--u-small", "--u-caption", "--u-eyebrow"):
        assert float(a[name].removesuffix("rem")) * 16 >= 14, name
    tracks = ("--track-display", "--track-title", "--track-title-2", "--track-band", "--track-entry", "--track-label")
    assert all(a[t] == "0" for t in tracks), {t: a.get(t) for t in tracks}
    boundary = re.search(
        r':where\(:root:lang\(ar\)\) :where\(\[lang="fr"\], \[lang="it"\], \[lang="en"\]\)\s*\{([^}]*)\}', css
    )
    assert boundary, "no Latin boundary block"
    b = _declarations(boundary.group(1))
    roots: dict[str, str] = {}
    for body in _root_blocks(TOKENS.read_text(encoding="utf-8")):
        roots.update(_declarations(body))
    # what the boundary restates: the Latin leadings of the roles Arabic opens, every track, the plus — the 14 px
    # floor of the small roles is NOT restated (a French caption inside an Arabic page keeps the Arabic floor)
    restated = [n for n in a if n.startswith("--track-")] + [
        "--t-display-lh",
        "--t-title-1-lh",
        "--t-title-2-lh",
        "--t-band-lh",
        "--t-entry-lh",
        "--t-lead-lh",
        "--ar-lh-plus",
    ]
    for name in restated:
        assert b.get(name) == roots[name], (name, b.get(name), roots[name])
    for name in ("--t-small", "--t-caption", "--t-label", "--t-caption-lh", "--t-label-lh"):
        assert name not in b, f"{name}: the floor is not undone inside a Latin run"
    assert b["--f-sans"] == "var(--f-sans-lat)" and b["--f-serif"] == "var(--f-sans-lat)"
    # the Arabic block comes after the step-up, so the 14 px floor wins on an Arabic phone
    assert css.index("@media (max-width: 47.999rem), (pointer: coarse)") < css.index(":root:lang(ar), :lang(ar)")


# ---- base.css and buttons.css ------------------------------------------------------------------------------------------


def test_the_label_and_numeral_roles_in_base_css():
    """TYPOGRAPHY_V2 F-3, F-4: the label is Host Grotesk 13/16 600 +0.08 em uppercase through the tokens, never the
    mono; the numeral is the sans at 600, tabular."""
    base = _strip(BASE.read_text(encoding="utf-8"))
    label = re.search(r"\.t-label, \.eyebrow\s*\{([^}]*)\}", base)
    assert label, "no label role"
    body = label.group(1)
    for declaration in (
        "font-family: var(--f-sans)",
        "font-size: var(--t-label)",
        "line-height: var(--t-label-lh)",
        "font-weight: var(--w-label)",
        "letter-spacing: var(--track-label)",
        "text-transform: uppercase",
    ):
        assert declaration in body, declaration
    numeral = re.search(r"\.t-numeral\s*\{([^}]*)\}", base)
    assert numeral
    for declaration in (
        "font-family: var(--f-sans)",
        "font-size: var(--t-numeral)",
        "line-height: var(--t-numeral-lh)",
        "font-weight: var(--w-title)",
        "font-variant-numeric: var(--numeric-data)",
    ):
        assert declaration in numeral.group(1), declaration
    assert "var(--f-mono)" not in base, "base.css never seats the mono: the reference classes do, in their sheets"


def test_base_css_arabic_rules_are_in_the_subject_form_and_the_rtl_minors_are_present():
    """TYPOGRAPHY_V2 F-7 (`.x:lang(ar)`, never `:lang(ar) .x`, for a type property) and the Arabic audit's M1, M3, C-1
    (FINAL_DELIVERY_V2 R7: the brand isolate unbreakable, inline Latin links isolated, a wholly-French heading on the
    French paragraph's edge)."""
    base = _strip(BASE.read_text(encoding="utf-8"))
    for selector, body in _rules(base):
        if TYPE_PROPERTY.search(body):
            for part in selector.split(","):
                assert not ARABIC_DESCENDANT.search(part.strip()), (selector, body)
    assert re.search(
        r":is\(h1, h2, h3, h4, h5, h6, \.t-band, \.t-label, \.t-folio, \.eyebrow\):lang\(ar\):not\(\[translate=\"no\"\]\)\s*\{\s*"
        r"letter-spacing: 0; text-transform: none;\s*\}",
        base,
    )
    assert re.search(r":is\(em, i\):lang\(ar\)\s*\{\s*font-style: normal; font-weight: var\(--w-control\);\s*\}", base)
    assert 'bdi[dir="ltr"]:not(.phone, .email) { white-space: nowrap; }' in base, "M1"
    assert '[dir="rtl"] :is(a, button):is([lang="fr"], [lang="it"], [lang="en"]) { unicode-bidi: isolate; }' in base, (
        "M3"
    )
    assert (
        '[dir="rtl"] :is(h1, h2, h3, h4):has(> [lang="fr"]:only-child) { direction: ltr; text-align: start; }' in base
    ), "C-1"


def test_the_primary_call_is_16_24_600_and_17_on_phones():
    """TYPOGRAPHY_V2 §4.2, §5: «primary calls 16/24 600; secondary 15/20 500»; 17/24 under the phone step-up."""
    buttons = _strip(BUTTONS.read_text(encoding="utf-8"))
    primary = re.search(r"\.btn--primary\s*\{([^}]*)\}", buttons)
    assert primary
    for declaration in ("font-size: 1rem", "line-height: 1.5rem", "font-weight: var(--w-title)"):
        assert declaration in primary.group(1), declaration
    assert re.search(
        r"@media \(max-width: 47\.999rem\), \(pointer: coarse\)\s*\{\s*\.btn--primary\s*\{\s*font-size: 1\.0625rem;\s*\}\s*\}",
        buttons,
    )
    slab = re.search(r"\.btn\s*\{([^}]*)\}", buttons)
    assert slab and "font-size: var(--t-ui)" in slab.group(1) and "font-weight: var(--w-control)" in slab.group(1)
    assert ".btn--upper:lang(ar)" in buttons and ":lang(ar) .btn--upper" not in buttons, "the subject form (F-7)"


# ---- the Arabic product, in a browser ----------------------------------------------------------------------------------

ARABIC_LETTERS = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")

_ARABIC_GUARDS_JS = r"""
() => {
  const AR = /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/;
  const out = {small: [], tight: [], frenchLeading: [], mono: []};
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const text = node.nodeValue;
    if (!text || !text.trim()) continue;
    const el = node.parentElement;
    if (!el || seen.has(el)) continue;
    seen.add(el);
    if (el.closest('script, style, noscript, template, [hidden], [aria-hidden="true"]')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const fs = parseFloat(cs.fontSize), lh = cs.lineHeight === 'normal' ? NaN : parseFloat(cs.lineHeight);
    const tag = el.tagName.toLowerCase();
    const lang = el.closest('[lang]') ? el.closest('[lang]').getAttribute('lang') : '';
    const sel = tag + (el.className ? '.' + String(el.className).trim().split(/\s+/).slice(0, 2).join('.') : '');
    const block = !/^inline(?!-block|-flex|-grid)/.test(cs.display);
    if (AR.test(text)) {
      if (fs < 14) out.small.push({sel, fs, text: text.trim().slice(0, 30)});
      if (block && !isNaN(lh) && r.height > lh * 1.5 && lh / fs < 1.3) out.tight.push({sel, fs, lh});
      if (/^"?ILE Mono/.test(cs.fontFamily)) out.mono.push({sel, family: cs.fontFamily.slice(0, 40)});
    } else if (block && lang && lang !== 'ar' && fs >= 20 && !isNaN(lh)) {
      // a French block on an Arabic page keeps its Latin leading: a title of 24 px or more at most 1.3 (title-2 1.15,
      // band 1.25; the Arabic band is 1.35), an entry, a lead or a statement at most 1.5 (entry 1.4, lead 1.455; Arabic 1.6)
      const ratio = lh / fs;
      const title = fs >= 24 && (/^h[1-6]$/.test(tag) || /^h[1-6]$/.test(el.parentElement ? el.parentElement.tagName.toLowerCase() : ''));
      const limit = title ? 1.3 : 1.5;
      if (ratio > limit + 0.005) out.frenchLeading.push({sel, lang, fs, lh, ratio: Math.round(ratio * 1000) / 1000, title});
    }
  }
  return out;
}
"""

#: The Arabic pages the guard reads now — the ones whose sheets are already in the subject form and off the mono.
ARABIC_PAGES = (
    "/ar/parcours/",
    "/ar/faq/",
    "/ar/glossaire/",
    "/ar/contact/",
    "/ar/compte/login/",
    "/ar/forum/",
    "/ar/attention-aux-fraudes/",
    "/ar/parcours/salaried_work/",  # v524-lib: the frontispiece on the steps (the French h1 at 1.08, the lead 22/32), the numerals in the sans
)
#: Pages whose findings belong to another lane's burn-down (measured 5 Nov 2026 on 4bafcfa0 + T, lane server 8785; the
#: full crawl is docs/design-v5/QA/v524/t/NOTES.md §6): the lane that converts the sheet moves its page into ARABIC_PAGES.
ARABIC_PAGES_BURNDOWN = {
    "/ar/": "HOME — hero.css: .he-origin__call 12 px literal (Arabic calls under the 14 px floor on the seeded home), .he-origin__word 16/19.2 on two lines",
    "/ar/le-projet/": "PUB2 — _projet.css:172 .racconto__titolo[id=project-why-title] (a French h2 of 24 px at 32 px; the library's title reads --t-band-lh)",
    "/ar/entreprises/": "PUB1 — _companies.css: the companies' statement at 44 px (24/44 at 390); the library's .testa__title reads --t-title-2-lh since v524-lib",
    "/ar/agami/": "PUB2 — _agami.css: .agami-id__etichetta(-voce) and dt in ILE Mono (F-3: Arabic in a system fallback)",
}


@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", (1440, 390))
def test_arabic_product_sizes_leadings_and_faces(browser, live_server, seeded, width):
    """TYPOGRAPHY_V2 §6 «Arabic guards» (V5.24 §13–§14): on /ar/ no Arabic letters under 14 px; no multi-line Arabic
    element whose leading is under 1.3 em; every French run of 20 px or more at its Latin leading (titles ≤ 1.2 em,
    leads and statements ≤ 1.5 em — the lead's own 22/32 is 1.455); no Arabic letters drawn by an element whose first
    family is ILE Mono (the registers of AGAMI and Réseau fell to a system face)."""
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    context = browser.new_context(viewport={"width": width, "height": 900 if width > 400 else 844})
    page = context.new_page()
    try:
        for path in ARABIC_PAGES:
            page.goto(live_server.url + path, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            found = page.evaluate(_ARABIC_GUARDS_JS)
            assert found["small"] == [], (path, width, found["small"][:8])
            assert found["tight"] == [], (path, width, found["tight"][:8])
            assert found["frenchLeading"] == [], (path, width, found["frenchLeading"][:8])
            assert found["mono"] == [], (path, width, found["mono"][:8])
            families = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
            assert "Readex Pro" in families and "Vazirmatn" not in families, (path, families)
        for path in ARABIC_PAGES_BURNDOWN:
            # the face holds on every page now; the floor, the leading and the mono seats are the lanes' rows
            page.goto(live_server.url + path, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            families = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
            assert "Readex Pro" in families and "Vazirmatn" not in families, (path, families)
    finally:
        context.close()
