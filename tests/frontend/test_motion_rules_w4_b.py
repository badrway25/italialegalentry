"""
Two motion rules of the V5.4 plan §1.5 held on the stylesheets — design V5, family W4-B (its review's m3 and m4,
docs/design-v5/QA/v54/w4-b/REVIEW.md; the browser side is tests/frontend/test_motion_browser_w4_b.py):

* tier 0 (R-07): a change the keyboard asks for is not animated, and each family writes its one
  `html[data-input="key"]` rule (static/js/head.js). Plain links had none: the console bar's trail ran the 120 ms
  colour fade of every link (`a { transition: color … }`, static/css/v5/base.css) when Tab focused it. The links' rule
  stands next to the links' transition;
* the curves (MS-O1, MS-O2): every arrival and the way into a hover on `--ease-enter`; a small surface leaves on
  `--ease-enter` at 120 ms, a long travel on `--ease-layout`; `--ease-exit` keeps one role only — an object that crosses
  the view. Ten declarations had kept the superseded council table's exit curve (the portico's pointer exit, menu-item
  hovers, the rail's rows, tools and foot, the phone bar). No object crosses the view today, so no stylesheet names
  `--ease-exit` but the token files; one that does is added below with its reason.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_V5 = ROOT / "static" / "css" / "v5" / "base.css"
#: The token files that define the curve (V5's, and V4's until it leaves).
TOKEN_FILES = {Path("static/css/v5/tokens.css"), Path("static/css/v4/tokens.css")}
#: Declarations that may name --ease-exit: objects that cross the view (path → why). None today.
CROSSES_THE_VIEW: dict[Path, str] = {}
COMMENT = re.compile(r"/\*.*?\*/", re.S)


def _sheets() -> list[Path]:
    roots = [ROOT / "static" / "css", *sorted((ROOT / "apps").glob("*/static"))]
    sheets = []
    for root in roots:
        for path in root.rglob("*.css"):
            relative = path.relative_to(ROOT)
            if "dist" in relative.parts:
                continue
            sheets.append(relative)
    return sorted(sheets)


def test_a_link_the_keyboard_focuses_takes_its_colour_at_once():
    css = COMMENT.sub("", BASE_V5.read_text(encoding="utf-8"))
    links = re.search(r"(?m)^a \{([^}]*)\}", css)
    assert links and "transition: color var(--motion-fast) var(--ease-enter)" in links.group(1), "the links' fade moved"
    rule = re.search(r'(?m)^html\[data-input="key"\] a \{([^}]*)\}', css)
    assert rule and rule.group(1).strip() == "transition-duration: 0ms;", "tier 0: the links' keyboard rule"
    assert rule.start() > links.start(), "the keyboard's rule follows the transition it silences"


def test_ease_exit_keeps_its_one_role():
    sheets = _sheets()
    assert Path("static/css/v5/base.css") in sheets and Path("apps/portal/static/portal/v5/_shell.css") in sheets
    named = {}
    for relative in sheets:
        if relative in TOKEN_FILES:
            continue
        css = COMMENT.sub("", (ROOT / relative).read_text(encoding="utf-8"))
        hits = [line.strip() for line in css.splitlines() if "--ease-exit" in line]
        if hits and relative not in CROSSES_THE_VIEW:
            named[str(relative)] = hits
    assert named == {}, (
        "--ease-exit is for an object that crosses the view only (plan §1.5 MS-O2): a small surface leaves on "
        f"--ease-enter at 120 ms, a long travel on --ease-layout; the way into a hover is --ease-enter — {named}"
    )
