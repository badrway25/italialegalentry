"""
The forced-colors probe must be able to FAIL, or its "0 lost" means nothing.

`scripts/qa_chrome_media.py` reported zero lost indicators on every page it walked. That is either
a good result or a broken detector, and the two are indistinguishable from the outside. These tests
drive `lost_indicators` with synthetic readings, including the one that actually happens in a
browser, so that the zero is a measurement rather than an accident.

The case worth knowing: forced colors does NOT make a background transparent. It rewrites it to a
system colour. An indicator painted with `background: var(--accent)` comes back as `Canvas` — the
same colour as the surface it sits on, therefore invisible, yet not transparent by any test. The
first version of this detector only looked for transparency and would have reported that as fine.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from qa_chrome_media import lost_indicators, transparent  # noqa: E402

CANVAS = "rgb(255, 255, 255)"
INK = "rgb(0, 0, 0)"


def reading(**over):
    base = {
        "key": 0,
        "el": "li.stepper__item::before",
        "paints": True,
        "w": 8.0,
        "h": 8.0,
        "bg": "rgb(15, 106, 114)",
        "img": "none",
        "border": "none 0px",
        "outline": "0px",
        "behind": CANVAS,
    }
    base.update(over)
    return base


def test_an_indicator_repainted_as_its_own_ground_is_lost():
    """The real forced-colors failure: same colour as what it sits on, and no edge to fall back on."""
    normal = [reading()]
    forced = [reading(bg=CANVAS, behind=CANVAS)]
    lost = lost_indicators(normal, forced)
    assert len(lost) == 1
    assert lost[0]["el"] == "li.stepper__item::before"
    assert lost[0]["was"] == "rgb(15, 106, 114)"


def test_an_indicator_that_keeps_contrast_is_not_lost():
    normal = [reading()]
    forced = [reading(bg=INK, behind=CANVAS)]
    assert lost_indicators(normal, forced) == []


def test_a_border_saves_an_indicator_that_lost_its_fill():
    """A hairline survives high contrast; an indicator that has one is not lost even if its fill goes."""
    normal = [reading()]
    forced = [reading(bg=CANVAS, behind=CANVAS, border="solid 1px")]
    assert lost_indicators(normal, forced) == []


def test_an_outline_saves_it_too():
    normal = [reading()]
    forced = [reading(bg=CANVAS, behind=CANVAS, outline="1px")]
    assert lost_indicators(normal, forced) == []


def test_a_background_image_dropped_to_none_is_lost():
    """Forced colors drops background-image outright, which is how a CSS-drawn rule disappears."""
    normal = [reading(bg="rgba(0, 0, 0, 0)", img="linear-gradient(rgb(15, 106, 114), rgb(15, 106, 114))")]
    forced = [reading(bg="rgba(0, 0, 0, 0)", img="none")]
    lost = lost_indicators(normal, forced)
    assert len(lost) == 1
    assert lost[0]["was"].startswith("linear-gradient")


def test_an_element_that_painted_nothing_to_begin_with_is_ignored():
    normal = [reading(paints=False, bg="rgba(0, 0, 0, 0)")]
    forced = [reading(paints=False, bg="rgba(0, 0, 0, 0)")]
    assert lost_indicators(normal, forced) == []


def test_readings_that_drifted_are_not_compared():
    """
    Two reads of a page that changed between them cannot be diffed element by element.

    Saying nothing is the right answer: a mismatched pair would otherwise be reported as a defect
    in whichever element happened to land at that index.
    """
    normal = [reading(key=0, el="a.main-nav__link::after")]
    forced = [reading(key=0, el="li.timeline__item::before", bg=CANVAS)]
    assert lost_indicators(normal, forced) == []


def test_transparent_recognises_the_forms_chrome_emits():
    assert transparent("rgba(0, 0, 0, 0)")
    assert transparent("transparent")
    assert transparent("rgba(15, 106, 114, 0)")
    assert not transparent("rgb(255, 255, 255)")
    assert not transparent("rgba(15, 106, 114, 0.14)")
