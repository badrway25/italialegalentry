"""
The one motion gate of script (V5.4 plan §1.5 «Reduced motion, built as a state»; RTE-M2 fixes 2 and 3; W1-D).

`static/js/src/motion.js`'s `reducedMotion()` is the only place a script asks whether it may move: the person's
setting (`prefers-reduced-motion: reduce`) or the preview's flag `html.rm`. The CSS rule zeroes the duration
tokens, but the Web Animations API and a frame loop ignore every stylesheet — so script motion is held here, on
the sources (fast, offline):

* the gate reads the setting and the flag, and no other module under static/js/src/ reads the media query;
* no module calls `element.animate(` or `requestAnimationFrame` outside motion.js, and inside it each call sits
  in an exported helper that asks `reducedMotion()` before it — `play`, `nextFrame`, `afterPaint`, `tween`;
* Motion (motion.dev) is imported through motion.js only, and a module that animates with it consults the gate;
* no product script waits on `transitionend` / `animationend`: a 0 s transition never fires its event, so the
  wait would hang exactly under reduced motion. motion.js's `settled()` waits on the animations really running,
  raced with a timeout.

The browser half — the computed state under the emulated setting, the helpers run in a page — is
tests/frontend/test_reduced_motion_w1_d.py.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "static" / "js" / "src"
MOTION = SRC / "motion.js"
#: The helpers through which the rest of the code moves; each asks the gate first.
GATED_HELPERS = ("play", "nextFrame", "afterPaint", "tween")
EVENT_WAITS = re.compile(r"\b(?:on)?(?:transitionend|animationend|transitioncancel|animationcancel)\b", re.I)


def _strip_comments(source: str) -> str:
    """The code without its comments: block and line comments go, strings and template literals stay."""
    out, i, n = [], 0, len(source)
    while i < n:
        c = source[i]
        if c in "\"'`":
            j = i + 1
            while j < n and source[j] != c:
                j += 2 if source[j] == "\\" else 1
            out.append(source[i : j + 1])
            i = j + 1
        elif source.startswith("/*", i):
            end = source.find("*/", i + 2)
            i = n if end < 0 else end + 2
        elif source.startswith("//", i):
            end = source.find("\n", i)
            i = n if end < 0 else end
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _code(path: Path) -> str:
    return _strip_comments(path.read_text(encoding="utf-8"))


def _modules() -> list[Path]:
    found = sorted(SRC.rglob("*.js"))
    assert MOTION in found and len(found) > 1, "the layout of static/js/src moved and this test did not"
    return found


def _product_scripts() -> list[Path]:
    """Every script the product serves from source: static/js (not the bundles) and the apps' static trees."""
    found = [p for p in (ROOT / "static" / "js").rglob("*.js") if "dist" not in p.relative_to(ROOT).parts]
    found += list((ROOT / "apps").glob("*/static/**/*.js"))
    return sorted(found)


def _exported_functions(code: str) -> dict[str, str]:
    """`export function name(…) { body }` → {name: body}, the body matched brace by brace."""
    bodies: dict[str, str] = {}
    for match in re.finditer(r"export function (\w+)\s*\([^)]*\)\s*\{", code):
        depth, i = 1, match.end()
        while depth and i < len(code):
            depth += {"{": 1, "}": -1}.get(code[i], 0)
            i += 1
        bodies[match.group(1)] = code[match.end() : i - 1]
    return bodies


def test_the_gate_reads_the_setting_and_the_preview_flag():
    code = _code(MOTION)
    assert 'const QUERY = "(prefers-reduced-motion: reduce)";' in code
    gate = _exported_functions(code)["reducedMotion"]
    assert "media.matches" in gate, "the gate reads the setting, live"
    assert 'classList.contains("rm")' in gate, "the gate reads the preview's flag html.rm"


def test_no_other_module_asks_the_media_query():
    for path in _modules():
        if path == MOTION:
            continue
        code = _code(path)
        assert "prefers-reduced-motion" not in code, f"{path.name}: ask reducedMotion() from motion.js — one gate"


def test_no_animate_or_frame_loop_outside_the_gate():
    for path in _modules():
        if path == MOTION:
            continue
        code = _code(path)
        for token in (".animate(", "requestAnimationFrame"):
            assert token not in code, f"{path.name}: {token} — use play() / nextFrame() / afterPaint() / tween()"


def test_inside_motion_js_every_animate_and_frame_call_asks_the_gate_first():
    code = _code(MOTION)
    bodies = _exported_functions(code)
    for name in GATED_HELPERS:
        assert name in bodies, f"motion.js no longer exports {name}()"
    covered = 0
    for name, body in bodies.items():
        hits = [i for i in (body.find(".animate("), body.find("requestAnimationFrame")) if i >= 0]
        if not hits:
            continue
        gate = body.find("reducedMotion()")
        assert 0 <= gate < min(hits), f"{name}(): ask reducedMotion() before it animates or waits on a frame"
        covered += body.count(".animate(") + body.count("requestAnimationFrame")
    total = code.count(".animate(") + code.count("requestAnimationFrame")
    assert covered == total, "an .animate( or a requestAnimationFrame sits outside an exported, gated helper"


def test_motion_is_imported_through_motion_js_and_its_animations_consult_the_gate():
    for path in _modules():
        code = _code(path)
        if path != MOTION:
            assert not re.search(r"""from\s+["']motion(?:/[^"']*)?["']""", code), (
                f"{path.name}: import Motion from ./motion.js"
            )
        imported = re.search(r"""import\s*\{([^}]*)\}\s*from\s*["']\./motion\.js["']""", code)
        if path == MOTION or not imported:
            continue
        names = {name.split(" as ")[0].strip() for name in imported.group(1).split(",")}
        if names & {"animate", "scroll", "inView"}:
            assert "withMotion(" in code or "reducedMotion()" in code, (
                f"{path.name} animates with Motion and never asks the gate"
            )


def test_no_script_waits_on_a_transition_or_animation_event():
    scripts = _product_scripts()
    assert any(p.name == "main.js" for p in scripts) and any(p.name == "head.js" for p in scripts)
    for path in scripts:
        found = EVENT_WAITS.search(_code(path))
        assert not found, (
            f"{path.relative_to(ROOT).as_posix()}: {found.group(0)} — wait with motion.js's settled(), which has a timeout"
        )
    settled = _exported_functions(_code(MOTION))["settled"]
    assert "getAnimations(" in settled and "setTimeout(" in settled and "allSettled(" in settled
