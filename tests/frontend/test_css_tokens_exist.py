"""
Every CSS custom property referenced anywhere in the project must be defined.

Regression (browser QA 2026-09-20): the Forum stylesheet referenced token names that do not exist
(``--color-primary``, ``--color-text`` …). Each ``var()`` silently fell back to a hard-coded colour and
the page drifted from the design system; its hero title ended up dark on dark navy.

The sheets read are the SOURCES (design V5, W1-A; V5.4 plan §2.3, DL54-15): every sheet of static/css and
of the apps, a `_`-prefixed partial included wherever it is — a partial is never an entry and has no output
of its own, so it is checked here like any sheet — and never the bundles of static/css/dist/, which are
outputs: a name that only a stale bundle still declares is not defined
(tests/frontend/test_css_bundle_is_current.py holds the bundles to their sources).
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS_FILES = sorted(
    p
    for p in [*(ROOT / "static").rglob("*.css"), *(ROOT / "apps").rglob("static/**/*.css")]
    if "staticfiles" not in p.parts and "dist" not in p.relative_to(ROOT).parts
)
DECLARATION = re.compile(r"(--[a-zA-Z0-9-]+)\s*:")
REFERENCE = re.compile(r"var\(\s*(--[a-zA-Z0-9-]+)")
# Set at run time by JavaScript or by a component modifier, never declared in a stylesheet. (--reveal-index left with
# components.css §29 and main.js's initReveal: W4-B; --nav-drawer-top, read by nothing since W2-A's drawer, left the
# shim with its declaration: W4-D part 2.) v515-a: --rise-k is written by rise.js on each rising row (its 40 ms
# step), --portico-from by nav.js's open() on a door switch (the old panel's height the card morphs from).
# V5.22 (SECTION_SYSTEM_V2 §2 H and §2 L «the rail» — approved owner/product decisions; lane S): the map's ring is laid
# out by its module, so --n (the actors' count) and --sel (the selected actor) are written by sezioni/mappa.js; the
# rail's lit segment, --spia-y and --spia-h, by sezioni/spia.js. Each reference carries a fallback for the still without
# script. V5.20 strict rule: the same invariant — every name declared, or written at run time and named here with its
# writer.
# V5.30 Fast Visual Variety Correction §7 INSTITUTIONS (V5.20 strict rule: the same invariant): the hemicycle's arc was the
# one stylesheet that declared an --i, and it is gone; the map's ring reads the --i sezioni/mappa.js writes on each node.
RUNTIME_PROPERTIES: set[str] = {"--rise-k", "--portico-from", "--n", "--i", "--sel", "--spia-y", "--spia-h"}
# Written by the PAGE, in the style attribute of the element that reads it — a primitive's one parameter, never declared
# in a stylesheet. v524-lib (DL54-189; BACKGROUND_MATERIAL_V2 §3.5, FINAL_DELIVERY_V2 R3): «il raccordo» is placed on
# its section's route by `style="--raccordo-x: …"` on the .sez-raccordo span (v5/_materia.css). Every reference to one
# carries its fallback, so a page that sets none still draws the primitive (checked below).
PAGE_PARAMETERS: set[str] = {"--raccordo-x"}
# v524-cifix (V5.20 strict rule: the same invariant, read correctly): a comment is not CSS. The guard read names out of
# comments — `var(--track-*)` in a tokens.css comment was taken for a reference to «--track-» — and counted a name
# written in a comment as defined. Both sides now read the code only: no false red, and no definition by comment.
COMMENT = re.compile(r"/\*.*?\*/", re.S)


def _code(path: Path) -> str:
    return COMMENT.sub("", path.read_text(encoding="utf-8"))


def _defined_everywhere() -> set[str]:
    names: set[str] = set()
    for path in CSS_FILES:
        names.update(DECLARATION.findall(_code(path)))
    return names


def test_css_files_are_discovered():
    assert any(p.name == "tokens.css" for p in CSS_FILES)
    assert len(CSS_FILES) >= 5
    # the partials are sources and are checked; the bundles are outputs and are not
    assert ROOT / "static" / "css" / "_legacy-tokens.css" in CSS_FILES
    assert ROOT / "static" / "css" / "v5" / "tokens.css" in CSS_FILES
    assert not [p for p in CSS_FILES if "dist" in p.relative_to(ROOT).parts]


@pytest.mark.parametrize("path", CSS_FILES, ids=[str(p.relative_to(ROOT)) for p in CSS_FILES])
def test_every_referenced_custom_property_is_defined(path):
    defined = _defined_everywhere() | RUNTIME_PROPERTIES | PAGE_PARAMETERS
    css = _code(path)
    inline_declared = set(re.findall(r"(--[a-zA-Z0-9-]+)\s*:", css))
    missing = sorted({name for name in REFERENCE.findall(css) if name not in defined | inline_declared})
    assert not missing, f"{path.relative_to(ROOT)} references undefined custom properties: {missing}"


def test_a_page_parameter_is_read_with_its_fallback_and_never_declared_by_a_sheet():
    """v524-cifix: the names the page writes (PAGE_PARAMETERS) are read with a fallback everywhere, and no stylesheet
    declares one — a sheet's declaration would make it a token, and it belongs in the guard's first rule then."""
    read = dict.fromkeys(PAGE_PARAMETERS, 0)
    for path in CSS_FILES:
        css = _code(path)
        for name in PAGE_PARAMETERS:
            assert name not in DECLARATION.findall(css), f"{path.relative_to(ROOT)} declares the page parameter {name}"
            references = re.findall(r"var\(\s*" + re.escape(name) + r"\s*([,)])", css)
            assert all(sep == "," for sep in references), f"{path.relative_to(ROOT)}: var({name}) without its fallback"
            read[name] += len(references)
    assert all(read.values()), f"a page parameter no sheet reads any more — take it out of PAGE_PARAMETERS: {read}"
