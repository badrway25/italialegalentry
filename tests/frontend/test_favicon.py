"""
Every page declares an icon Chrome will accept without going looking for another one.

A site that ships only an SVG icon still gets probed for `/favicon.ico` at the root, and that probe
404s on every page of every session. It is one red line in a console that is otherwise clean, which
is exactly the kind of noise that teaches people to stop reading the console.

Found by opening the site in a real Chrome window and looking at the network panel, not by any
test: the page was correct, the asset was correct, and the browser asked for a third thing.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from django.urls import reverse
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SVG = ROOT / "static" / "img" / "favicon.svg"
ICO = ROOT / "static" / "img" / "favicon.ico"

#: What `scripts/make_favicon_ico.py` writes, and what a browser picks between.
EXPECTED_SIZES = [(16, 16), (32, 32), (48, 48)]


def test_both_icon_files_exist():
    assert SVG.is_file(), "the SVG icon is gone"
    assert ICO.is_file(), "no .ico: Chrome will probe /favicon.ico and log a 404 on every page"


def test_the_ico_really_carries_every_size():
    """
    Pillow's ICO writer builds every frame from the ONE image it is given.

    Passing a list through `append_images` looks right and silently writes a single 16px frame.
    Reopening the file is the only way to notice, so the test reopens it.
    """
    with Image.open(ICO) as image:
        assert sorted(image.ico.sizes()) == sorted(EXPECTED_SIZES)


def test_the_ico_uses_the_same_palette_as_the_svg():
    """
    The geometry is duplicated between the SVG and the generator, so the colours must be checked.

    A mark that drifts in one file and not the other is worse than no mark: the tab and the
    bookmark bar would disagree about what this project looks like.
    """
    import re

    svg = SVG.read_text(encoding="utf-8")
    ground = re.search(r'fill="(#[0-9a-fA-F]{6})"', svg).group(1).lower()
    expected = tuple(int(ground[i : i + 2], 16) for i in (1, 3, 5))

    with Image.open(ICO) as image:
        image.size = (48, 48)
        pixels = image.convert("RGB")
    # The centre of an edge, inside the rounded corner and away from every stroke.
    assert pixels.getpixel((2, 24)) == expected, "the .ico ground colour is not the SVG's"


@pytest.mark.django_db
def test_the_home_page_declares_both(client):
    html = client.get(reverse("pages:home")).content.decode()
    assert 'type="image/svg+xml"' in html
    assert "favicon.ico" in html, "only the SVG is declared; the browser will look for an .ico"
    # SVG first: the browsers that understand it should not download a raster they will not use.
    assert html.index("favicon.svg") < html.index("favicon.ico")
