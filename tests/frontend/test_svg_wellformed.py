"""
Every SVG served by the site must be well-formed XML.

Regression: the icon sprite once carried ``--`` inside an XML comment. HTML parsers tolerate that,
but an SVG referenced through ``<use href="icons.svg#…">`` is parsed as XML: the browser discarded the
whole sprite and no icon was drawn anywhere on the site. Only a real-browser check revealed it.
"""

from pathlib import Path
from xml.dom import minidom

import pytest

STATIC = Path(__file__).resolve().parents[2] / "static"
SVG_FILES = sorted(STATIC.rglob("*.svg"))


def test_there_are_svg_assets_to_check():
    assert SVG_FILES, "no SVG asset found under static/"


@pytest.mark.parametrize("path", SVG_FILES, ids=[str(p.relative_to(STATIC)) for p in SVG_FILES])
def test_svg_is_wellformed_xml(path):
    minidom.parse(str(path))  # raises ExpatError on malformed XML


def test_icon_sprite_symbols_have_a_viewbox_and_content():
    sprite = minidom.parse(str(STATIC / "img" / "icons.svg"))
    symbols = sprite.getElementsByTagName("symbol")
    assert len(symbols) >= 30
    for symbol in symbols:
        assert symbol.getAttribute("id").startswith("icon-")
        assert symbol.getAttribute("viewBox") == "0 0 24 24", symbol.getAttribute("id")
        drawable = [n for n in symbol.childNodes if n.nodeType == n.ELEMENT_NODE]
        assert drawable, f"{symbol.getAttribute('id')} is empty"
