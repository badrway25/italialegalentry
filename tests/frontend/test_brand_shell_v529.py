"""
V5.29 «SMALL LAYOUT & BRAND REFINEMENT» (the owner, 6 Nov 2026 21:49; directives/V5_29_FINAL_PREMIUM_VISUAL_REMEDIATION.md,
last section) — held on the sources, where a refactor would undo it. The browser evidence is the lane's targeted review
(evidence/v529/brand/review.json): the shell, the forms, the key.

1. ONE horizontal system of related widths (v5/tokens.css): the content's column (--content-wide, the container,
   unchanged — every composition and image `sizes` is measured on it), the letterhead's shell (the column + 10rem,
   capped by the viewport less the gutters) and the premium form's band, which stands on the shell (--form-wide).
2. The lock-up one step up from 80rem, the same at rest and scrolled — 36/19 under V5.29, 40/21 since V5.30 §5 (the
   verbatim 38/20 ratio either way; restated under V5.20 below).
3. The key alone turns, once, through the motion gate (never under reduced motion), and never loops — since CLOSING
   (V5.29 09:41 item 1, «CSS-only where possible»; V5.20) in the stylesheet (v5/chrome.css §1), shell.js none of it.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_the_shell_is_one_system_of_related_widths():
    v5 = _read(CSS / "v5" / "tokens.css")
    assert (
        "--content-wide: var(--container); --site-shell-max: calc(var(--content-wide) + 10rem);"
        " --form-wide: var(--site-shell-max);" in v5
    ), "three related widths, one source"
    legacy = _read(CSS / "tokens.css")
    assert {int(px) for px in re.findall(r"--container: (\d+)px;", legacy)} == {1176, 1320, 1440}, "the column unchanged"
    chrome = _read(CSS / "v5" / "chrome.css")
    inner = chrome[chrome.index(".site-header__inner {") :]
    assert "max-inline-size: var(--site-shell-max);" in inner[: inner.index("}")], "the letterhead is the shell"
    formwork = _read(CSS / "v5" / "_formwork.css")
    assert "max-inline-size: var(--form-wide);" in formwork
    assert ":is(.formwork-section, .chapter):has(.formwork) > .container { max-inline-size: var(--form-wide); }" in formwork
    header = _read(ROOT / "templates" / "partials" / "header.html")
    assert '<div class="container site-header__inner">' in header, "the gutters stay the container's"


def test_the_lockup_is_one_step_up_from_80rem_in_both_states():
    """V5.29 §3 asked 36/19, V5.30 §5 40/21 from 80rem. RESTATED under V5.20 for the owner's FINAL HOMEPAGE PRECISION PASS
    of 11 Nov 2026: «brand lockup too small, weak presence, not legible — optical sizing: mark size, wordmark size,
    baseline, gap … the navbar must not become oversized»: the lock-up is sized band by band through ONE custom property,
    --sig-size (the mark and the layers over it), and the wordmark's size beside it — 48rem 42/18 · 64rem the mark alone
    44 · 76rem 40/16 · 80rem 42/20 · 85rem 46/22. The same invariants, and stronger: every desktop step from 80rem is at
    least the approved 40/21's mark and never smaller than the band before it, one brand at rest and scrolled, the layers
    over the mark follow it by construction (no size of their own left in motion.css), and the letterhead's height is
    held (64 px, 56 px scrolled) with the mark inside the scrolled row."""
    chrome = _read(CSS / "v5" / "chrome.css")
    assert ".site-header { --sig-size: 38px; }" in chrome
    assert ".site-header .lock__mark { inline-size: var(--sig-size); block-size: var(--sig-size); }" in chrome
    bands = {
        int(rem): (int(mark), int(words))
        for rem, mark, words in re.findall(
            r"@media \(min-width: (\d+)rem\) \{\n  \.site-header \{ --sig-size: (\d+)px; \}\n"
            r"  \.site-header \.lock__wm \{ font-size: (\d+)px; \}\n\}",
            chrome,
        )
    }
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026 (A4): «the FULL
    # lockup must be visible and readable across the whole desktop/tablet header range INCLUDING 1024–1215 px — today
    # that band shows the mark alone». Was: 64rem the mark alone (44) · 76rem 40/16 · 80rem 42/20. Now: the whole
    # lock-up at every desktop width — 48rem's 42/18 holds through 64rem (no mark-alone step), 72rem (1152 px) 42/20,
    # 85rem 46/22 — every desktop step is at least the approved 40/21's mark, the name never under 18 from 48rem
    # (stronger than the old 16), never smaller than the band before it, and no band from 20.5rem hides the name
    assert bands == {48: (42, 18), 72: (42, 20), 85: (46, 22)}, bands
    assert "--sig-size: 44px" not in chrome and "@media (min-width: 64rem) { .site-header { --sig-size" not in chrome, (
        "the mark-alone step is gone")
    steps = [bands[rem] for rem in sorted(bands)]
    assert all(b[0] >= a[0] and b[1] >= a[1] for a, b in zip(steps, steps[1:])), steps
    assert bands[72][0] >= 40 and bands[85][0] >= bands[72][0] and bands[85][1] >= 21, "never under the approved 40/21"
    assert ".lock__text { display: none; }" not in re.sub(r"@media \(max-width: 20\.5rem\)[^}]*\}[^}]*\}", "", chrome), (
        "no band from 20.5rem up hides the name")
    assert max(mark for mark, _ in bands.values()) <= 56 - 8, "the mark inside the scrolled row (56 px) with air"
    assert ".site-header.is-scrolled .lock__mark" not in chrome and ".site-header.is-scrolled .lock__wm" not in chrome, (
        "one brand at rest and scrolled")
    assert ".is-scrolled { --sig-size" not in chrome and ".is-scrolled .lock" not in chrome
    motion = _read(CSS / "v5" / "motion.css")
    assert "--sig-size:" not in motion, "the layers over the mark follow it: their size is the letterhead's --sig-size"
    tokens = _read(CSS / "v5" / "tokens.css")
    assert "--header-h: 64px; --header-h-scrolled: 56px;" in tokens, "the letterhead's height unchanged (V5.30 §5)"


def test_the_key_alone_turns_once_through_the_gate():
    """V5.29 09:41 item 1 (the owner's CLOSING gate: «keep the accepted key interaction — one initial unlock gesture,
    hover/focus replay, idle static, reduced-motion static: make it CSS-only where possible, … share the existing
    reduced-motion handling, delete dead shell code»; V5.20, restated by lane CLOSING): the turn is the stylesheet's
    (v5/chrome.css §1, the lock-up's own section) and the same invariants are held where it lives — the key's layer alone, the preparation, the
    turn and the settle on the verbatim mark, the ILE tokens, one turn at a time (the latch: on at once, off
    --motion-key after the pointer or the focus left), never a loop, never under reduced motion — and no script turns
    it any more (shell.js ≤ 4 700 B, test_motion_v512_a_w2.py)."""
    nav = _read(ROOT / "static" / "js" / "src" / "nav.js")
    assert "initBrandKey" not in nav and "rotateY" not in nav and "sig__turn" not in nav, "no script turns the key"
    chrome = re.sub(r"/\*.*?\*/", "", _read(CSS / "v5" / "chrome.css"), flags=re.S)
    turn = re.search(r"@keyframes brand-key \{(.*?)\n\}", chrome, flags=re.S).group(1)
    assert "14% { transform: rotateY(-16deg); animation-timing-function: cubic-bezier(0.77, 0, 0.175, 1); }" in turn, (
        "a 16° counter-turn, then the turn on --ease-turn")
    assert "80% { transform: rotateY(364deg); animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }" in turn, (
        "4° past, then the settle on --ease-enter")
    assert "to { transform: rotateY(360deg); }" in turn and "var(" not in turn, "it settles on the verbatim mark"
    latch = chrome[chrome.index("@property --lock-turn {") :]
    assert latch.startswith('@property --lock-turn {\n  syntax: "<number>";\n  inherits: true;\n  initial-value: 0;\n}')
    gate = latch[latch.index("@media (prefers-reduced-motion: no-preference) {") :]
    gate = gate[: gate.index("\n}\n")]
    # the latch is held by the key's layered mark, never by the link: the link's own colour transition stays (the A/B)
    assert ":root:not(.rm) .site-header .lock-sig { transition-property: --lock-turn; transition-delay: var(--motion-key); }" in gate, (
        "off --motion-key after the pointer or the focus has left: a turn begun is a turn finished")
    assert "@starting-style { :root:not(.rm) .site-header .lock-sig { --lock-turn: 1; } }" in gate, "the brand's reveal"
    assert ":root:not(.rm) .site-header .brand:is(:hover, :focus-visible) .lock-sig { --lock-turn: 1; transition-delay: 0ms; }" in gate, (
        "on at once, on its hover or focus; a second pass during the turn does not restart it")
    assert not re.search(r"\.brand(?::is\([^)]*\))?\s*\{[^}]*transition", gate), "no transition is declared on the link itself"
    assert "@container style(--lock-turn: 1) {\n    .site-header .lock-sig .sig__turn { animation: brand-key var(--motion-key) var(--ease-enter) 1 backwards; }" in gate, (
        "the key's layer, never the wordmark or the base; one iteration; the ILE tokens; nothing applied after its end")
    assert chrome.count("brand-key") == 2 and "infinite" not in chrome, "one turn, played from one rule, never a loop"
    motion = _read(CSS / "v5" / "motion.css")
    assert "brand-key" not in motion and "--lock-turn" not in motion, "one home: the lock-up's section"
