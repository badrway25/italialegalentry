"""
The preview's reduced-motion flag is the reduced-motion state (MOTION_SYSTEM MS7 / RM-2; V5.4 plan §1.5; W1-D).

`html.rm`, in static/css/v5/tokens.css, stands in for `prefers-reduced-motion: reduce` when a review cannot change
the setting: a review made with it must see what a person with the setting gets. Gate 0's flag stopped a loader
and a drawer and left every duration token running (`--motion-fast` still 120 ms), so a «still» reviewed with it
showed more motion than the setting allows. Here the flag is the media block's token list, written as a twin, and
this file holds it on the effective cascade — static/css/main.css in order, then the apps' sheets (fast, offline):

* every custom property resolves to the same value under the flag as under the setting, whichever layer declared
  it — the durations at 0 ms, the thresholds and `--motion-reduced` kept;
* the twin declares exactly what the media block declares, and nothing else;
* motion.js's gate reads the flag beside the setting (tests/frontend/test_script_motion_gate.py holds the rest).

The flag is not evidence: reduced-motion evidence is taken with the setting emulated
(tests/frontend/test_reduced_motion_w1_d.py). When the twin drifts, the failure prints the block to paste.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
TOKENS = CSS / "v5" / "tokens.css"
REDUCE = "prefers-reduced-motion: reduce"


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _rules(css: str) -> list[tuple[tuple[str, ...], str, str]]:
    """Every style rule as (enclosing at-rule preludes, selector, body), brace by brace."""
    rules, stack, start = [], [], 0
    for i, c in enumerate(css):
        if c == "{":
            stack.append((" ".join(css[start:i].split()), i))
            start = i + 1
        elif c == "}":
            if stack:
                prelude, opened = stack.pop()
                if not prelude.startswith("@"):
                    rules.append((tuple(p for p, _ in stack), prelude, css[opened + 1 : i]))
            start = i + 1
        elif c == ";" and (not stack or stack[-1][0].startswith("@")):
            start = i + 1
    return rules


def _declarations(body: str) -> dict[str, str]:
    return {name: " ".join(value.split()) for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", body)}


def _sheets() -> list[Path]:
    main = [CSS / name for name in re.findall(r'@import url\("([^"]+)"\)', (CSS / "main.css").read_text("utf-8"))]
    apps = sorted(ROOT.glob("apps/*/static/**/*.css"))
    assert TOKENS in main and apps, "the cascade moved and this test did not"
    return main + apps


def _states() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """The custom properties of the root element: at rest, under the setting, under the flag (unresolved).

    Under the setting a `:root` inside the reduced-motion media query competes with the top-level `:root`
    blocks by order (the same specificity). Under the flag `html.rm` (0,1,1) beats every `:root` (0,1,0),
    whatever the order. Roots inside other media queries (the viewport) are the same in every state: left out.
    """
    rest: dict[str, str] = {}
    setting: dict[str, str] = {}
    flag: dict[str, str] = {}
    for sheet in _sheets():
        for context, selector, body in _rules(_strip_comments(sheet.read_text("utf-8"))):
            declared = _declarations(body)
            if selector == ":root" and not context:
                rest.update(declared)
                setting.update(declared)
            elif selector == ":root" and context and all(REDUCE in prelude for prelude in context):
                setting.update(declared)
            elif selector == "html.rm":
                assert not context, f"{sheet.name}: the flag's twin is a top-level rule"
                flag.update(declared)
    return rest, setting, {**rest, **flag}


def _resolve(value: str, table: dict[str, str], depth: int = 0) -> str:
    assert depth < 16, value
    return re.sub(
        r"var\((--[a-z0-9-]+)\)",
        lambda m: _resolve(table.get(m.group(1), f"<{m.group(1)} unset>"), table, depth + 1),
        value,
    )


def _media_block() -> dict[str, str]:
    css = _strip_comments(TOKENS.read_text("utf-8"))
    blocks = [
        body for context, selector, body in _rules(css) if selector == ":root" and context == (f"@media ({REDUCE})",)
    ]
    assert len(blocks) == 1, "v5/tokens.css carries one reduced-motion block"
    return _declarations(blocks[0])


def _twin_to_paste(block: dict[str, str]) -> str:
    return "html.rm {\n" + "".join(f"  {name}: {value};\n" for name, value in block.items()) + "}"


def test_under_the_flag_every_custom_property_resolves_as_under_the_setting():
    rest, setting, flag = _states()
    parted = {
        name: (_resolve(setting[name], setting), _resolve(flag.get(name, "<unset>"), flag))
        for name in setting
        if _resolve(setting[name], setting) != _resolve(flag.get(name, "<unset>"), flag)
    }
    assert not parted, (
        f"the flag parts from the setting on {parted}; the twin should read:\n{_twin_to_paste(_media_block())}"
    )
    changed = [name for name in setting if _resolve(setting[name], setting) != _resolve(rest[name], rest)]
    assert len(changed) >= 14, f"the setting changes too little to be the state: {changed}"
    for name in changed:
        assert _resolve(flag[name], flag) in {"0ms", "0s", "0"}, (name, flag[name])


def test_the_twin_is_the_media_block_and_nothing_else():
    css = _strip_comments(TOKENS.read_text("utf-8"))
    twins = [body for context, selector, body in _rules(css) if selector == "html.rm" and not context]
    assert len(twins) == 1, (
        f"v5/tokens.css carries one html.rm block; it should read:\n{_twin_to_paste(_media_block())}"
    )
    assert _declarations(twins[0]) == _media_block(), (
        f"the twin drifted; it should read:\n{_twin_to_paste(_media_block())}"
    )
    for sheet in _sheets():
        if sheet != TOKENS:
            text = _strip_comments(sheet.read_text("utf-8"))
            assert not any(sel == "html.rm" for _, sel, _ in _rules(text)), (
                f"{sheet.name}: the token twin lives beside its media block"
            )


def test_the_gate_reads_the_flag():
    gate = (ROOT / "static" / "js" / "src" / "motion.js").read_text("utf-8")
    assert 'classList.contains("rm")' in gate and "(prefers-reduced-motion: reduce)" in gate
