# W2-A · Accessibility + performance check — A11Y_PERF

Label `w2-a-a11y-perf`, 11 October 2026, one pass (V5.5: implement → review once → fix → ship). Built nothing, changed
nothing in the family's code. Reviewed branch `v54-w2-a` at `4743c88` (code as of `d544ff5`; `5192f46` adds only the
senior review, read after this check's measures and cross-referenced below). Merge base with `design-v5`: `1c001e6`;
design-v5 is 50 commits further on (`38f78d4`: W2-B's merge, the steward's static pipeline), so the merged weights below
are computed from design-v5's recorded figures, not measured on a merged tree.

**Lane and tools.** Lane 3 from `C:/tmp/ile_wt/v54-w2-a` on `ile_v5_l3`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`: the dev server on 8783 with `ILE_DESIGN_PREVIEW=1` (the overlay board) for
accessibility; the lane's compressed twin on 8783 for performance (8782's shape: DEBUG off,
`CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire, `collectstatic` into a scratch root with
`--ignore "portal?console.css"` — DL54-44 item 4's raw entry; settings outside every repository). For the A/B, the branch
base `1c001e6` was extracted with `git archive` into a scratch folder outside every repository and served the same way,
same port, same clone. Signed-in pages through sessions minted with `Client.force_login` on `ile_v5_l3` (`qa-doc-person`,
`qa-person`, `qa-company`, `qa-admin`, `demo-operateur`; no password used, typed or stored; every row revoked at the end;
288 traces and 48 result files scanned: no cookie or session value in the evidence). Headless Playwright Chromium (the
venv's 1.63, HeadlessChrome 153.0.8010.12), one fresh profile per context under
`C:/tmp/ile_v5_council/.profiles/w2-a-a11y-perf/`, removed at close; reduced motion and forced colours by Playwright's
emulation; axe-core 4.13.0. One browser and no pytest at a time; every series waited on `PERFORMANCE_BENCHMARK_LOCK`
(never present; this role never created it). No run crashed. Never 8780, 8782, 9222 or 9223. **The machine was shared
and loaded** (CPU 44–86 %, 0.7–1.1 GB free during the timing series): the before-set comparison is a lane screen, the
attribution to this area is the round-interleaved A/B against the branch base. Scratch static roots and the base tree
deleted at the end; the lane server stopped.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w2-a/a11y-perf/` — `s1/` (keyboard, semantics, axe, contrast, targets;
13 cells, JSON + PNGs), `s2/` (reduced motion, forced colours, reflow, text spacing), `probe1.json`, `probe2.json`,
`probe3-head.json`, `probe4.json`, `probe5.json`, `ab/head.json` + `ab/base.json` (the regressions on both trees),
`probe_fix.json` (two fixes tried in the page), `perf/head/` (144 traced loads), `perf/ab-head/` + `perf/ab-base/`
(144 more, interleaved), `perf/interact-{head,base}.jsonl`, `perf/summary-head.json`, `perf/summary-ab.json`. Probes:
`C:/tmp/ile_v5_council/.work/w2-a/w2-a-a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 4 major · 1 minor. The system holds on the board and on the console pages, fr and ar: every family is a
named dialog, alertdialog or group; the focus goes in where the contract says, wraps, and comes back on Esc and on
«Fermer»; menus answer the arrows and close when the focus leaves; tooltips appear at once under the keyboard and go on
Esc; reduced motion is a true still (one 80 ms opacity, no transform at any frame); forced colours draw every panel;
320 px and 400 % reflow; no target under 24 px, none under 44 under a finger. The console's overlays open and close two
to three times faster than W3-A's (the drawer's cold open p90 504 → 144 ms), and nothing loops at rest. Against the
branch base three behaviours regressed, all in `overlay.js` and each a few lines (two of the fixes were tried in the
page); and the module and the sheets are over their §2.6 budgets, with a small measured cost.

## Findings

| # | Severity | What | Where | Fix |
|---|---|---|---|---|
| M1 | **major** | **The focus lands off-screen when the console drawer opens on a page whose entry sits low in the drawer, and after Shift+Tab across the wrap where the drawer's foot scrolls.** `qa-admin` at 390 × 844 (a phone held upright): on «Communications», «Guichet numérique» and «Academy» the focused current row lies wholly outside the drawer's visible list (visible share 0; «Mes échéances» 0.89), fr and ar; `qa-doc-person`'s and `qa-admin`'s «Academy» at 320 × 568 and on a phone on its side (844 × 390) — every persona's rail ends on it. At 844 × 390 (the foot not pinned under 30rem of height), Shift+Tab from the drawer's first stop wraps to «Site public» at y 771 in a 390 px viewport, fr and ar. A keyboard user sees no focus until the next Tab (WCAG 2.4.7 in practice). **Regression:** on the base (W3-A's `showModal()` + `focus()`) the row was scrolled into view in every one of these cells and Shift+Tab rested on the dialog (`ab/base.json` vs `ab/head.json`). The board's panels are not affected: their lists fit (`probe4.json`). | `static/js/src/overlay.js` `focus()`: `element.focus({ preventScroll: true })`, used by `open()`, the trap's wrap and the `focusin` guard | Keep `preventScroll` for the page, and bring the target into view inside its panel: after the focus, `element.scrollIntoView({ block: "nearest", inline: "nearest" })` when it stands in an open overlay (a fixed panel over a locked page: the page cannot move). Tried in the page on the twin: «Academy» fully visible at 390 × 844, 844 × 390 and in Arabic at 320 × 568, `scrollY` 0 → 0 (`probe_fix.json`). Test: `qa-admin`'s «Academy» at 390 × 844 and 844 × 390, the focused row's box inside the drawer's visible list; Shift+Tab across the wrap at 844 × 390. |
| M2 | **major** | **With the trapped modal (`show()` + `aria-modal`), the page behind stays in the accessibility tree.** Chromium's tree (the lanes' engine, Windows) with the console drawer open exposes the banner, «Navigation rapide», `main`, `contentinfo` and «Mon compte» — 357 nodes kept; with W3-A's `showModal()` drawer only the dialog and its «Menu» remained (107 kept, 43 ignored as `activeModalDialog`). The board shows the same: the trapped alert keeps 229 nodes, the native opt-in 23. The keyboard trap holds; a screen reader's virtual cursor leaves the drawer unless the screen reader applies `aria-modal` itself. DL54-75 says «Assistive technology reads `aria-modal`»: this engine does not prune for it. **Regression** for the console drawer. | `overlay.js` `open()` (trap mode) and `settle()` | While a trapped panel is open, `aria-hidden="true"` on the body's other element children (and back on close) — not `inert`: no rule of the project selects `aria-hidden`, so nothing is re-styled, which keeps the INP rule's gain. Tried in the page on the twin at CPU × 4: the tree pruned as `showModal()`'s (357 → 107 nodes: the dialog and its menu), at 0–1 style recalculation (≤ 0.7 ms) and no layout, against the opening's own 7 recalculations and ≈ 47 ms of style; trap and `aria-modal` unchanged (`probe_fix.json`). Alternative: `data-overlay-modal="native"` on the console drawer, if its cold open stays under 200 ms p90 — the INP rule fired on a `showModal()` p90 of 200 ms (the rule says «> 200»), measured while W3-A's `:has()` rule was still there. |
| M3 | **major** | **The rail's word (O11) does not appear under the keyboard's focus when focusing an item scrolls the compact rail.** The module puts the top-layer tip away on every scroll event (a capture listener on `window`), including the scroll the focus itself causes in the rail's list. Real Tab presses, rail compact: `qa-admin` at 1366 × 657 (a short laptop), fr and ar: 16 of 18 words shown — not «Mes échéances», «Communications»; `qa-doc-person` at 1100 × 600: 14 of 16 — not «Academy», nor «Tableau de bord» on the way back up. **Regression:** W3-A's tip showed 18 of 18 and 16 of 16 (`ab/`). Not a WCAG failure — each item keeps its accessible name — but O11 for the keyboard. REVIEW's O11 row reports the word at once on keyboard focus; the miss needs a focus that scrolls the rail's list. | `overlay.js` `wireDocument()`: `window.addEventListener("scroll", () => tipFor && hideTip(), { capture: true, passive: true })` | On a scroll, re-place the tip while its control is still `:focus-visible` or `:hover` (`placeTip(tipFor)`); hide it otherwise. Test: Tab through the compact rail at 1366 × 657 with `qa-admin`, a word for every item. |
| M4 | **major** | **The weight is over §2.6.** **JS:** the overlay chunk is 6 472 B gzip (+ the 142 B entry; 18.5 KB minified) for a module budget of 4 KB (+62 %; +29 % against the module and the tooltip helpers' 5 KB together). Console pages fetch 5 916 B more script on the wire and two more module requests (the overlay chunk and esbuild's runtime-helper chunk, 394 B): CSS + JS requests before `load` 3 + 9 on the dashboard and 4 + 9 on «Mes pièces», one over the before set's 3 + 8 / 4 + 8. Every public page gains the runtime chunk (+394 B, one request) through `shell.js`; the home's script stays under 45 KB (45 484 B on the wire). **CSS** (gzip −9): `main.css` +2 080 B (`v5/overlays.css` +3.1 KB less `components.css` §21 and §8), `portal/console.css` −231 B. On design-v5's recorded figures (DL54-73, DL54-76): the console page types ≈ 51 935 B for their ceiling of 50 086 B (+1 849 B), the login ≈ 49 472 B for 47 392 B (+2 080 B), the home ≈ 59 262 B for 59 137 B (+125 B), an interior page 44 611 B for 44 486 B (+125 B); `main.css` stays 1 469 B under its 46 080 B. **Measured cost** (the A/B, n = 9 per cell and arm): LCP +34 ms pooled over the eight console cells (+4 … +52 ms on seven, +140 ms on the dashboard ar 412, spreads overlapping), first-render task +3 ms, longest load task +7 ms, TBT +40 ms; in the same window every console cell stays within the before set's LCP resolution (seven under it, the dashboard ar 412 at +20 ms). | `static/js/dist/chunks/` (the overlay chunk and the runtime chunk), `static/css/dist/main.css` (`v5/overlays.css`) | Move what no console page draws behind a dynamic `import()` (the sheet's grip and the history are used by no page yet; the scripted placement only where anchor positioning is missing), and keep esbuild's helpers in the shared chunk (the steward's build). Then the merge step records the page types' ceilings and the module's budget in DL54, as DL54-44, -73 and -76 did, with these timings. |
| m1 | minor | **At 400 % (320 × 256) the alert's body is a 24 px scroll region with nothing focusable** — axe `scrollable-region-focusable` (serious, 2.1.1). Chromium ≥ 130 and Firefox make such a scroller focusable themselves (the Tab walk reached it), Safari does not. | `overlay.js` / `.overlay__body` | `tabindex="0"` on `.overlay__body` while it overflows (set at open and on resize), and let the trap's list count it. |

**Observations (not counted):**

- **INP — the console's overlays, A/B** (the Arabic «Mes documents», 412 × 823 @1.75, touch, CPU × 4, a fresh browser per
  load, n = 9 per arm, interleaved; Event Timing): the drawer opens at median 128 / p90 144 / max 160 ms (the base, W3-A's
  drawer: 432 / 504 / 528 — over the 200 ms budget) and closes at 120 / 152 / 168 (base 280 / 344 / 432); the account
  popover opens at 48 / 64 / 64 (base, V4's `<details>`: 128 / 144 / 208) and closes at 40 / 48 / 48. Each drawer opening
  still holds one long task (median 102, max 130 ms), as REVIEW m1 traced; REVIEW measured p90 215–232 ms (n = 18,
  the dev server, another window of the shared machine). The budget's edge depends on the machine; the area removed
  W3-A's 400–500 ms opening.
- **Nothing loops.** 3 s at rest after the drawer and the account popover opened and closed: 0 style recalculations,
  0 layouts, 0 animation frames, ≈ 2 ms of tasks; `document.getAnimations()` holds only the page's own finished
  `strip-fill` (W3-B's health strip) and, after a fresh sign-in, the entrance release — the same before and after the
  overlays (`probe5.json`).
- **Forced colours:** the CSS tip's 6 px transparent bridge (`border-block-end`) is painted CanvasText — a black bar
  under the box (`s2/forced-board-1440-tip-fr.png`). Cosmetic; `border-block-end-color: Canvas` under forced colours
  would remove it.
- axe's incompletes are benign: `aria-controls` naming a closed dialog (184 nodes), the night drawer's gradient (87,
  measured on pixels instead).
- The account trigger is named by the person's short name only — REVIEW m3, not repeated here.
- O10 (the WebKit / Firefox smoke) did not run here either: no binaries, none downloaded (REVIEW m2).
- The board's two popovers carry no group name (a dev board; the product's are named).

## Accessibility — what was measured

**Semantics and keyboard (s1: 13 cells, 51 overlay scenarios, ≈ 490 keyboard stops).** The board at 1440, at 390 under
a finger and at 400 % (320 × 256 @4); the console's drawer, account popover and row menu at 390 and 820 under a finger;
the row menu and the rail's language at 1440; the compact rail's words at 1100; `qa-admin`'s drawer at 390 and 844 × 390;
fr and ar. Every modal kind is a `dialog` (the alert an `alertdialog`) named by its title — the console drawer by its
label, «Navigation de l'espace réservé» — with `aria-modal="true"`. Its opener is a button: a link opener gets
`role="button"` and answers Space; `aria-haspopup="dialog"`, `aria-controls`, and an `aria-expanded` that follows the
panel. The product's popovers are groups named «Mon compte» and by the piece's title; their triggers are real buttons whose
`aria-expanded` follows. The focus goes in where the contract says: the alert's safe «Annuler», the dialog's field, the
drawer's current page, the sheet's current language, the menu's first row, the non-modal drawer's title. Tab wraps inside
every modal and Shift+Tab across the wrap lands on the last stop. A menu answers ArrowDown, ArrowUp, Home and End, and
closes when Tab takes the focus out. Esc closes every panel and puts the focus back on its opener, ringed, with
`aria-expanded` false; Space opens; «Fermer» by Enter closes and returns. In the drawer the rail's language list takes the
first Esc (focus on its summary, the drawer stays) and the second closes the drawer (focus on «Menu»). Every stop inside a
panel is `:focus-visible`, ringed on pixels and uncovered (5 × 3 points, `elementFromPoint`), but for M1's. axe-core in 33
open states: 0 violations but m1's. 0 CSP violations and 0 console errors in every cell.

**Tooltips.** Under the keyboard both tips (the control's `::after` and the top-layer one) are there at once, never over
their control; Esc puts them away and the focus stays. Under the pointer the tip is absent at 200 ms and present at
650 ms; it stays while the pointer rests on it, and Esc puts it away while the pointer stays (1.4.13). The rail's word
stands beyond the rail's edge (on its left in Arabic), inside the viewport, never over its item; «⋮» has its word and says
nothing while its menu is open. The rail's word under a scrolling rail is M3.

**Contrast on pixels (115 texts; the glyph method: the text shot as drawn and with its glyphs made transparent, p5 of the
footprint).**
- Titles 16.23 : 1 (20 px); body 16.0–16.2 (15 px); rows 16.23 (14 px).
- Buttons: the destructive action 9.85, the secondary 13.5–15.6, the primary 5.24–5.29 (15 px, W1-C's button).
- Tips 10.6–11.8 on night (13–14 px); the drawer's words 6.06–6.13 (W3-A's section titles).
- «Fermer»'s cross 7.17 on paper and 9.94 on night (≥ 3 : 1 for a glyph).
- Every text ≥ 4.5 : 1. DS 2026 and the colour council ask 7 : 1 only of the status register's words, and no overlay
  draws one.
- Rings on pixels (319 stops): `#1d8a93` 4.11 on white and 3.94 on `#fbfaf8`; the night ring 7.65. All ≥ 3 : 1.

**Reduced motion is a real still.** Every frame was sampled while each family opened and closed by the pointer: 19
scenarios (the board's alert, drawers, sheet and menu at 1440 in fr and ar; the dialog and the menu as sheets at 390; the
console drawer and account popover at 390 in fr and ar). Each held one pose and one position at every frame, with only
`opacity` (and the discrete `display` / `overlay`) running, 80 ms, panel and scrim. Without the setting the same
openings move (13–29 poses: the .96 scale, the «Slide», the sheet's spring, the 4 px drop). From the keyboard nothing
animates (tier 0).

**Forced colours (25 states, looked at).** Every panel is framed in CanvasText over a dimmed page, the focus ring drawn,
the destructive action outlined. The drawer and the sheets read in Arabic, the current page framed, the tips framed
boxes. The CSS tip's bridge is an observation above.

**Targets.** «Fermer» 44 × 44 on every panel; rows 36 px under a fine pointer and 44 under a coarse one. Under a finger
no control of any panel is under 44; nowhere under 24.

**Reflow and spacing.** At 320 × 568 every panel lies within the viewport (the console drawer 282 px wide, the others
full-width sheets), and the document never scrolls sideways. At 400 % (320 × 256) every family stays usable from the
keyboard with every stop visible; the alert's body then scrolls (m1). With WCAG 1.4.12's spacing no text is clipped and no
control overlaps in any panel (22 states).

## Performance — against `w1-0/before/MANIFEST.json`, then the A/B

**The before set** — its own `trace.py` `measure()` and `analyse.py` (byte-identical copies). Profile A (150 ms RTT,
1.6 / 0.75 Mbps), CPU × 4, cache off, a fresh profile per load, n = 9 per cell interleaved, medians (spread), on the
lane's compressed twin under the loaded machine; «before» = the W1-0 set on 8782 at `v54/base`.

| cell | LCP before → after | first-render task | longest load task | CLS max | LCP element |
|---|---|---|---|---|---|
| home fr 1440 | 2 064 → 1 792 (1 416–1 992) | 710 → 41 | 710 → 188 | 0.0252 | the stage's photograph (W2-D's) |
| home fr 412 | 2 100 → 1 768 (1 628–1 968) | 746 → 38 | 746 → 166 | 0 | the photograph (W2-D's) |
| home ar 1440 | 2 356 → 2 084 (1 828–2 540) | 938 → 39 | 938 → 198 | 0.0183 | the photograph (W2-D's) |
| home ar 412 | 2 328 → 2 008 (1 756–2 592) | 914 → 42 | 914 → 236 | 0 | the photograph (W2-D's) |
| login fr 1440 | 1 720 → 1 508 (1 316–1 676) | 397 → 134 | 397 → 171 | 0.0455 | = |
| login fr 412 | 1 708 → 1 536 (1 424–1 688) | 384 → 61 | 384 → 104 | 0 | = |
| login ar 1440 | 1 872 → 1 752 (1 524–1 896) | 485 → 124 | 485 → 192 | 0.0325 | = |
| login ar 412 | 1 872 → 1 784 (1 584–1 876) | 483 → 72 | 483 → 125 | 0 | = |
| dashboard fr 1440 | 1 604 → 1 768 (1 596–1 952) | 405 → 57 | 405 → 210 | 0.0005 | `p.empty` = |
| dashboard fr 412 | 1 584 → 1 608 (1 308–1 824) | 370 → 53 | 370 → 231 | 0 | `p.panel__title` = |
| dashboard ar 1440 | 1 792 → 1 876 (1 624–2 100) | 500 → 70 | 500 → 246 | 0.0149 | `h1.ctx__title` = |
| dashboard ar 412 | 1 740 → 1 788 (1 584–2 020) | 449 → 58 | 449 → 237 | 0 | `p.panel__title` = |
| documents fr 1440 | 1 552 → 1 484 (1 272–1 664) | 354 → 57 | 354 → 142 | 0.0010 | `p.doc-page__lead` = |
| documents fr 412 | 1 564 → 1 428 (1 128–1 576) | 324 → 55 | 324 → 159 | 0 | `p.doc-page__lead` = |
| documents ar 1440 | 1 692 → 1 584 (1 364–2 008) | 435 → 59 | 435 → 149 | 0.0050 | `p.doc-page__lead` = |
| documents ar 412 | 1 672 → 1 632 (1 372–1 920) | 399 → 50 | 399 → 176 | 0 | `p.doc-page__lead` = |

- Fourteen of sixteen cells inside §2.6. Every first-render task is far under the before set's. Every LCP is ≤ 2.5 s.
  CLS ≤ 0.05 on every flagship (the login's 0.0455 is W2-B's page).
- No console cell's LCP element changed. The home's moved to the hero's photograph with W2-D, earlier than before.
- Two dashboard cells sit over the +50 ms resolution in this series (fr 1440 +164, ar 1440 +84 ms). The series ran with
  the machine at 44–86 % CPU, and the A/B below, run in a quieter window, puts both cells under the before set (1 564 and
  1 672 ms).
- TBT is higher than the before set's everywhere (W3-A's check explained why: the page now paints in a 40–70 ms first
  task and finishes after FCP). The A/B gives this area's share.

**The A/B** — the head and the branch base on the same twin, interleaved by round (each round one tree serves every cell
once, then the other; the order alternates), n = 9 per cell and arm, machine at 39–50 % CPU:

| cell | LCP base → head (Δ) | first-render task | longest load task | TBT | CSS + JS req. |
|---|---|---|---|---|---|
| dashboard fr 1440 | 1 516 → 1 564 (+48) | 52 → 56 | 132 → 167 | 85 → 171 | 3 + 7 → 3 + 9 |
| dashboard fr 412 | 1 384 → 1 428 (+44) | 41 → 47 | 208 → 209 | 200 → 289 | 3 + 7 → 3 + 9 |
| dashboard ar 1440 | 1 632 → 1 672 (+40) | 58 → 60 | 216 → 215 | 208 → 200 | 3 + 7 → 3 + 9 |
| dashboard ar 412 | 1 620 → 1 760 (+140) | 49 → 47 | 250 → 278 | 294 → 329 | 3 + 7 → 3 + 9 |
| documents fr 1440 | 1 300 → 1 336 (+36) | 47 → 51 | 100 → 110 | 73 → 109 | 4 + 7 → 4 + 9 |
| documents fr 412 | 1 284 → 1 300 (+16) | 42 → 44 | 154 → 129 | 173 → 210 | 4 + 7 → 4 + 9 |
| documents ar 1440 | 1 512 → 1 516 (+4) | 52 → 56 | 121 → 156 | 133 → 185 | 4 + 7 → 4 + 9 |
| documents ar 412 | 1 436 → 1 488 (+52) | 45 → 52 | 155 → 155 | 211 → 237 | 4 + 7 → 4 + 9 |

- Pooled: LCP 1 460 → 1 494 ms, first-render task 48 → 51, longest load task 160 → 167, TBT 165 → 205; CLS 0 in both
  arms. The LCP element is unchanged in every cell.
- On the wire: script 40 578 → 46 494 B; the dashboard's sheets 50 071 → 51 913 B, «Mes pièces»' 51 243 → 53 085 B.
- The traces put the LCP behind the second webfont's swap in both arms, and the module chunks are fetched after it
  (≈ 1.5–1.7 s), so the weight's cost is small and within the spreads (LCP spreads overlap by 200–400 ms). It is real on
  the Arabic phone cells: M4.
- The interactions and the rest are in the observations above.

## What this role did not do

- No code, no test run, and no change to the worktree but this file.
- Two fixes were tried in a page by `page.evaluate` (`probe_fix.json`), never written.
- Scratch folders (the twin's two static roots, the base tree) were deleted after the series. The lane's server is
  stopped and every minted session revoked.
- No Safari or Firefox; no real device. Phones are emulated.
