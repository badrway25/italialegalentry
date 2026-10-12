"""
Every CSS custom property referenced anywhere in the project must be defined.

Regression (browser QA 2026-09-20): the Forum stylesheet referenced token names that do not exist
(``--color-primary``, ``--color-text`` …). Each ``var()`` silently fell back to a hard-coded colour and
the page drifted from the design system; its hero title ended up dark on dark navy.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CSS_FILES = sorted(
    p
    for p in [*(ROOT / "static").rglob("*.css"), *(ROOT / "apps").rglob("static/**/*.css")]
    if "staticfiles" not in p.parts
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


@pytest.mark.parametrize("path", CSS_FILES, ids=[str(p.relative_to(ROOT)) for p in CSS_FILES])
def test_every_referenced_custom_property_is_defined(path):
    defined = _defined_everywhere() | RUNTIME_PROPERTIES
    css = path.read_text(encoding="utf-8")
    inline_declared = set(re.findall(r"(--[a-zA-Z0-9-]+)\s*:", css))
    missing = sorted({name for name in REFERENCE.findall(css) if name not in defined | inline_declared})
    assert not missing, f"{path.relative_to(ROOT)} references undefined custom properties: {missing}"
