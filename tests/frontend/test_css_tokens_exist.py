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
# Set at run time by JavaScript or by a component modifier, never declared in a stylesheet.
RUNTIME_PROPERTIES = {"--nav-drawer-top", "--reveal-index"}  # both set by static/js/main.js


def _defined_everywhere() -> set[str]:
    names: set[str] = set()
    for path in CSS_FILES:
        names.update(DECLARATION.findall(path.read_text(encoding="utf-8")))
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
    defined = _defined_everywhere() | RUNTIME_PROPERTIES
    css = path.read_text(encoding="utf-8")
    inline_declared = set(re.findall(r"(--[a-zA-Z0-9-]+)\s*:", css))
    missing = sorted({name for name in REFERENCE.findall(css) if name not in defined | inline_declared})
    assert not missing, f"{path.relative_to(ROOT)} references undefined custom properties: {missing}"
