# W4-B · The motion audit — accessibility + performance check (one pass)

Label `w4-b-a11y-perf`, 16 October 2026 — the area's one accessibility/performance check (V5.5: implement → review once
→ fix → ship). Built nothing, changed nothing in the area's code. Checked branch `v54-w4-b` at `d63bab3` — its code as
of `286da57`; `d63bab3` adds the notes only — against the branch point, design-v5 at `8ab5b89` (integration
checkpoint 3). design-v5's tip during the check, `11070b5`, differs from `8ab5b89` by one line of
`templates/portal/dashboard.html` (sec-f7) and by no stylesheet or script.

**Lane.** Lane 8, port 8788: the dev server from `C:/tmp/ile_wt/v54-w4-b` on `ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; the branch point served on the same port from an export of
`8ab5b89` in this role's scratch folder for every before/after. Signed-in pages through sessions minted with
`Client.force_login` on `ile_v5_l8` (no password used, typed or stored), revoked at the end. Headless Playwright
Chromium (the venv's), its own profile under `C:/tmp/ile_v5_council/.profiles/w4-b-a11y-perf/`; one browser and no pytest
at a time; every series waited on `PERFORMANCE_BENCHMARK_LOCK` (never present, never created). **No run crashed.** Never
8780, 8782, 9222 or 9223.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-b/a11y-perf/` — `desk/`, `phone/` (keyboard walk with each ring read on
pixels, pixel contrast, hit areas, Chromium's accessibility tree, axe — one JSON and one capture per page), `forced/`,
`reduce/`, `reflow/`, `probes/` (the skip link, the portico, the rail, «Ma situation» with and without motion, the hero
with and without motion, the console's entrance release, the overlays from the keyboard, the console at load, the
review's cross-checks `review-crosscheck.json` and `race-*.png`),
`probes-base/` (the branch point's question change), `perf/` (`runs.jsonl`, `interact.jsonl`, `weigh.json`,
`perf_summary.json`, `interact_summary.json`, `traces/`). Probes: `C:/tmp/ile_v5_council/.work/w4-b/w4-b-a11y-perf/`
(W3-B / W3-D's probes; this check's own `motionlog.js`, injected before the page's scripts, logs every transition that
runs, every CSS animation that starts and every `element.animate()` call, phase by phase, with its timing).

## Verdict — SHIP_AFTER_FIXES

**0 blocking · 1 major · 2 minor** in the area. **No WCAG 2.2 AA failure in normal use** on the pages W4-B touched —
fr and ar; 1440, 390 touch, 320 × 640, 320 × 256; keyboard, focus visible and never covered, names and roles, contrast
on pixels, targets, reduced motion as a real still, forced colours. What W4-B fixed holds in the browser: no text waits
for a reveal (K17); the Motion library is in no bundle; the rail folds in the next frame (R10); the portico and the
skip link do not move from the keyboard (F4, F5); the current entry keeps its own marker under forced colours and the
focus adds its ring on it (O2); the console moves nothing at load but the entrance release. **The major is the plan's
own motion rule:** «Ma situation»'s question change — the one script animation W4-B rewrote — still plays its 120 +
200 ms when a key asks for it (Enter on «Continuer» or «Précédent»); tier 0 (R-07) wants it at once, as every other
state change a key asks for in the product already is (the hero's decorative light apart, by decision: O4). One
condition in `situation.js` and one browser case (finding 1). The two minors are the senior review's m2 and m3,
confirmed here on their accessibility side: a return within the question's 120 ms fade leaves no question drawn and
the focus on `body` (finding 2, a race inside that window), and the console bar's trail links fade 120 ms when the
keyboard focuses them (finding 3).
**No performance regression:** every page type's script is 26.9 KB gzip lighter with one request fewer (the home 27.1 KB
and two requests: 51 249 → 24 138 B, under §2.6's 45 KB by 21.9 KB), the shared CSS 92 B lighter on every page and
144 B on the console page types; TBT lower and the load's tasks over 50 ms fewer or as many in every cell, the
first-render task no worse (−6.0 … +1.2 ms), the LCP element unchanged everywhere, CLS ≤ 0.0035, nothing loops.

## What was checked

| Key | Account | Page | What W4-B changed there |
|---|---|---|---|
| H | — | `/fr/`, `/ar/` | the home: `home.js` with `hero.js` inlined (the hero's discovery and replay on `play()`), no Motion chunk |
| P | — | `/fr/parcours/`, `/ar/parcours/` | a door page: the portico at tier 0 from the keyboard (F4), the skip link without its slide (F5), `shell.js` with `nav.js` inlined |
| L | — | `/fr/compte/login/`, `/ar/…` | the entrance «Il varco»: the same shell |
| D | `qa-doc-person` | `/fr/espace-reserve/`, `/ar/…` | the console: the rail's fold instant (R10, F3), the forced-colours current entry (O2), the entrance release |
| S | `qa-doc-person` | `/fr/espace-reserve/ma-situation/`, `/ar/…` | the question change on `play()` (F2) |
| M | `qa-doc-person` | `/documents/` | «Mes pièces»: the console shell, the drawer's modules (French only: the app has no language prefix and the persona's language is French, as in W1-0's set) |

Passes: 1440 × 900 (fine pointer) and 390 × 844 (phone emulation, touch) — keyboard walk, pixel contrast, hit areas,
Chromium's accessibility tree, axe-core 4.13.0 (W1-0's copy) on `wcag2a/2aa/21a/21aa/22aa` and `best-practice`, W1-0's
`health.js`; 320 × 640 and 320 × 256 (400 % of 1280 × 1024); reduced motion (`reducedMotion: "reduce"`, never the
preview's flag) and forced colours (Chromium's emulation) at 1440 and 390; the interaction probes with the motion
instrument. **89 accessibility loads and 63 probe cases: 0 CSP reports, 0 console errors, every response 200.**

## Accessibility

| Check | Result |
|---|---|
| Keyboard, fr and ar | **735 stops over 22 walks** (1440 and 390), and 731 more under forced colours: every one `:focus-visible`, every one named; the order follows the page; the first stop on every page is the skip link |
| Focus visible on pixels | each stop shot focused and unfocused at the same scroll: the ring whole on every side (fill ≥ 0.98 at p5; median change contrast 9.93); the two partial rings are links cut by the phone's bottom edge (O1). The low change contrasts are the ones earlier checks measured and ruled: the login's field halo (1.44; W1-C R1) and the hero's CTA-B and replay (2.04 / 1.32 as a whole change; W2-D measured their rings against the outside, 4.1–7.6) |
| Focus not obscured (2.4.11) | 0 of 1 466 stops covered by a fixed or sticky layer; the skip link's target (`main#main-content`) lands at or under the bar's edge (57 / 57 px on the public phone, 57 / 57 on the console at 1440, 48 / 48 at 390) |
| Names, roles, structure | 0 nameless control; one h1 per page; the rail's control «Navigation» keeps its name while `aria-expanded` turns true ↔ false; the portico's doors `aria-expanded`; the arriving question named by its title («Question 2 Nationalité …», `aria-labelledby`); the replay button «Rejouer l’animation de la porte». axe: **0 violations, 0 best-practice**; its «incomplete» are colour pairs (settled on pixels below) and `aria-controls` on the closed overlays' triggers (W2-A's pattern, not W4-B's) |
| Contrast on pixels | **1 090 text runs, 0 below AA** (each run's colour with its opacity chain against the pixels under it, the page redrawn with every glyph transparent); lowest 4.99 : 1 (white at 0.96 on the teal primary, «Continuer» at 390); the state words 7.23–7.25 (COLOUR's ≥ 7 : 1 for state words holds); no notice title on these pages; the skip link 13.48 : 1 (public) and ≥ 8.73 (console). W4-B changed no colour |
| Targets (2.5.8; 44 under a finger) | **727 targets, 0 under 24 px** without the spacing exception; the controls W4-B touched: the skip link 229 × 52, the replay 44 × 71 on the phone, the rail's control 36 × 36 (fine pointer only; O2) |
| Arabic | the portico's arrows follow the reading direction (← is «next»), the rail and the phone bar mirrored, the question arrives from the left (−16 px); no Arabic text under 14 px |
| Reduced motion — a real still | **22 loads:** 0 transitions, CSS animations or `animate()` calls during the load; 0 running at load, at + 1 s and after the gestures; 0 `will-change`. The phone's sheet and the console drawer: one 80 ms opacity, sheet and scrim (MS-O4); the door panel, the rail's fold, «Continuer», Tab and every Esc: nothing. The hero: 0 `animate()` calls, its still, no replay button. The entrance release: its three animations at 0 ms (the still) |
| Forced colours | every focus changes pixels (0 stops without a change). **The current entry (O2):** the lit Highlight disc and, in the rail, the word underlined; focusing it now changes 1 060 px in the rail (fill 0.99, 15.13 : 1) and 508–620 px in the phone bar (11.31 : 1), fr and ar. Usable at 1440 and 390, fr and ar (`forced/*.png`, looked at) |
| Reflow (1.4.10) | 320 × 640 and 320 × 256, 22 loads: 0 horizontal overflow, 0 clipped text |
| K17 — text never waits for a reveal | no `[data-reveal]`, `.reveal`, `[data-counter]` on any page; 0 laid-out text at opacity 0 or hidden at rest but the hero's four «call» lines — the hand's state of an origin, shown (opacity 1) on a key focus too and part of each origin's description |

## Motion — what the instrument saw

| Where | With motion | Asked from the keyboard | Under reduced motion |
|---|---|---|---|
| The skip link (H, P, D; 1440, 390; fr, ar — 12 cases) | — | on the first Tab, at + 30 ms, already at `transform: none`, whole in the viewport, 0 transitions (F5 holds); Enter moves the focus to `main#main-content` | — |
| The portico (P, 1440, fr and ar) | a pointer's opening: the panel's 200 ms opacity and transform, its entries, the chevron, the architrave's 470 ms spring — the control | Enter opens, the arrows go door to door, ArrowDown enters the panel, Esc closes and gives the focus back, Esc after a pointer's opening: **0 transitions in every phase** (F4 holds); the focus visible, never covered | the panel at once |
| The rail's fold (D, 1440, fr and ar) | a click: 248 → 64 px and the page's padding with it **within 16 ms**, no width or padding transition (only the control's 120 ms hover colours) | Enter and Space: the same, 0 transitions; the focus stays on «Navigation», its laguna-400 ring drawn | nothing |
| The rail's stored choice | reloaded folded: 64 px from the first frame, **0 layout shifts** (`rail-pref.js`) | — | — |
| «Ma situation»'s question (S; 1440, 390; fr, ar) | the leaving question 1 → 0 in 120 ms, then the arriving one 0 → 1 and `translateX(16px)` → 0 in 200 ms (−16 px in Arabic, reversed for «Précédent»), both on `cubic-bezier(0.25, 1, 0.5, 1)` (`--ease-enter`), 123 ms apart; afterwards one question, opacity 1, no `style`, no animation; two presses of «Continuer» 40 ms apart land on one whole question, two further on; **a return within the fade** («Continuer» then «Précédent», or the Stepper's Q3 then Q1, 40 ms apart) **leaves no question drawn and the focus on `body`** (finding 2) | **the same 120 + 200 ms** (finding 1); the focus on the arriving question, its ring drawn once the question has faded in | nothing: swapped at once, the focus on it |
| The hero (H; 1440, 390; fr, ar) | the discovery: 35 `animate()` calls over 3 564–3 573 ms at 1440, 29 over 2 758–2 763 ms at 390 (≤ 5 s); the replay 3 865–3 873 / 3 044–3 045 ms; at rest 0 running, 0 `will-change`, no endless animation | the replay reached by Tab, named, ring drawn (laguna-400 at 3 px); a focused origin runs its light (W2-D's documented choice, O4) | the still: 0 `animate()` calls, no replay button |
| The overlays (the phone sheet, the console drawer, the filter's bottom sheet; fr, ar) | a tap: 320 ms (the sheet, the drawer), the bottom sheet's 550 ms spring twin — the control | Enter opens and Esc closes with **0 transitions** | one 80 ms opacity (the sheet and the drawer, measured) |
| The console at load (D, S, M; 1440, 390; fr, ar) | a fresh session: only the entrance release — `lume-light-o`, `lume-light-t`, `lume-ink-o`, 1 600 ms, on the mark; the next load and every other console load: **nothing** in the first 2.5 s | — | the release's three at 0 ms |

## Performance

**Script and style before `load`**, per page type — the files each page requested (Resource Timing in the loads below),
weighed as gzip −9 of the tree's own files; W1-0's «before» set is V4 on 8782 (`MANIFEST.json`):

| Page type | W1-0 (V4): JS req · gz — CSS req · gz | design-v5 `8ab5b89`: JS | `v54-w4-b`: JS | CSS `8ab5b89` → `v54-w4-b` |
|---|---|---|---|---|
| the home | 8 · 36 892 — 2 · 39 114 | 9 · 51 249 | **7 · 24 138** | 3 · 49 844 → 49 752 |
| a door page | 6 · 34 488 — 1 · 36 294 | 7 · 43 674 | **6 · 16 781** | 2 · 39 068 → 38 976 |
| the login | 6 · 34 488 — 2 · 37 502 | 8 · 45 351 | **7 · 18 462** | 2 · 40 344 → 40 252 |
| the dashboard | 8 · 36 706 — 3 · 41 668 | 9 · 46 070 | **8 · 19 178** | 4 · 46 617 → 46 473 |
| «Ma situation» | 9 · 37 902 — 3 · 41 668 | 10 · 47 292 | **9 · 20 415** | 4 · 46 398 → 46 254 |
| «Mes pièces» | 8 · 36 706 — 4 · 42 839 | 10 · 49 113 | **9 · 22 221** | 5 · 51 764 → 51 620 |

The shared bundles: `dist/main.css` 35 483 → **35 391 B** (−92, every page), the console page types (main + console +
portal) 44 196 → **44 052 B** (−144); the JS dist 60 726 → 33 806 B gzip in all (the Motion chunk's 26 611 B gone; its
identifiers in 0 bundles, `motion` in neither package file). §2.6's «a public page ≤ 45 KB» (46 080 B) holds on every
page type, and every page type's script is now 12.8–17.7 KB under V4's. Requests: one script fewer on every page type
(two on the home), no stylesheet added; the home is back at W1-0's count (3 + 7 = 2 + 8), the scripts of the door page,
the dashboard and «Ma situation» at it; the login keeps one script above V4's 6 (O3) and «Mes pièces» one above with
`piece-drawer.js` (W3-C); the extra stylesheets are the page-only sheets V5.8's ruling allows. The notes' figures are
confirmed byte for byte (theirs for «Mes pièces» count the drawer's two modules fetched after `load`).

**Cold loads before / after** (W1-0's `trace.py` protocol on the lane: CPU × 4, no network throttling, the dev server's
uncompressed static files, a fresh profile and the cache disabled per load, one discarded warm-up per cell after each
server start, interleaved in two blocks — BASE then HEAD, HEAD then BASE —; medians; the LCP column gives HEAD − BASE
inside each block):

| Cell | n | first-render task ms | longest load task ms | TBT ms | load tasks > 50 ms | LCP ms (blocks) | LCP element | CLS max |
|---|---|---|---|---|---|---|---|---|
| the home — fr 1440 | 5 / 5 | 20.0 → 17.2 | 120 → 125 | 136 → 102 | 7 → 5 | 660 → 648 (−124, +32) | the door's image, both | 0.0099 → 0.0013 |
| the home — fr 412 | 5 / 5 | 40.6 → 40.7 | 121 → 130 | 118 → 102 | 5 → 4 | 680 → 588 (−148, −12) | the door's image, both | 0 → 0 |
| the home — ar 1440 | 5 / 5 | 24.4 → 18.7 | 150 → 150 | 186 → 121 | 7 → 5 | 640 → 620 (−164, +38) | the door's image, both | 0.0088 → 0 |
| a door page — fr 1440 | 5 / 5 | 75.0 → 76.2 | 137 → 115 | 78 → 58 | 3 → 3 | 452 → 452 (−24, +44) | `p.ingresso__lead`, both | 0.0099 → 0 |
| the login — fr 1440 | 5 / 5 | 20.7 → 16.5 | 96 → 89 | 53 → 28 | 4 → 2 | 576 → 504 (−80, +14) | the door's image, both | 0.0017 → 0.0035 |
| the dashboard — fr 1440 | 5 / 5 | 24.8 → 18.8 | 110 → 127 | 70 → 56 | 4 → 3 | 656 → 640 (−180, +104) | `p.db-empty`, both | 0 → 0.0001 |
| the dashboard — fr 412 | 5 / 5 | 31.2 → 28.9 | 99 → 97 | 95 → 64 | 4 → 3 | 576 → 568 (−12, −24) | `h2#db-now-title`, both | 0 → 0 |
| «Ma situation» — fr 1440 | 5 / 5 | 19.2 → 17.9 | 69 → 68 | 10 → 0 | 3 → 2 | 484 → 396 (−132, −30) | `p.ws-head__lead`, both | 0.0005 → 0.0005 |
| «Mes pièces» — fr 1440 | 5 / 5 | 23.4 → 18.9 | 93 → 79 | 50 → 34 | 4 → 3 | 560 → 496 (−108, −68) | `p.ws-head__lead`, both | 0.0018 → 0 |

- **No long task introduced at load.** The count of load tasks over 50 ms is lower or equal in every cell and TBT lower in
  every cell. The longest load task is a rendering task — style, layout and paint, no script — on both trees (traced);
  it moves by −22 … +17 ms, and in the three cells where it grows the same rendering work lands in fewer, larger tasks:
  the dashboard's base did a forced 84 ms layout, then a 96 ms frame at 790 ms; the branch one 129 ms frame at 371 ms.
  In the kept traces (one a tree) the main thread is busy 830 → 491 ms over the dashboard's first 4.5 s and 1 204 → 833
  ms over the home's, script 82 → 27 and 164 → 116 ms.
- **LCP** no worse in any cell — the medians fall or hold; the block differences change sign in five cells (the
  machine's noise; other lanes share it) — and **the LCP element is the same** on both trees in every cell (the door's
  photograph on the home and the login, as in W1-0's set at 1440; W3-B's and W3-C's heads on the console pages). **CLS** ≤ 0.0035 everywhere, far under
  0.05 on the flagships. At the end of every load: 0 running animations, 0 `will-change`.
- The absolute figures are the lane's dev server, not W1-0's protocol on the compressed twin: the claim is the relative
  before/after on one server, same data, same sessions.

**Interactions before / after** (CPU × 4, a fresh context per sample, n = 5 + 5 in two interleaved blocks, medians):

| Interaction | Event Timing ms | long tasks | frames in 800 ms · worst gap | done at |
|---|---|---|---|---|
| the rail's fold by a click (the dashboard, 1440) | 72 → 88 | one per press on both: 51–66 → 67–71 ms | 47 → 47 · 50 → 67 ms | 311 → 100 ms |
| «Continuer» on «Ma situation» (1440) | 64 → 48 (48–80) | 0 → one 56 ms in 1 of 5 | 47 → 48 · 50 → 34 ms | — |
| Enter on a portico door (a door page, 1440) | 48 → 56 (one 8 ms step of Event Timing) | none on either | 49 → 49 · 33 → 33 ms | — |

The rail's press is R10's trade, measured: the whole relayout now happens once, in the press's own frame (+16 ms of
event time at × 4, ≈ 4 ms at × 1), instead of a 200 ms transition that re-laid the workspace on every frame for 300 ms;
INP far under 200 ms. Not a regression to fix. The question change is lighter (WAAPI on the compositor where Motion ran
a frame loop for `x`).

**At rest — nothing loops.** 0 running animations and 0 `will-change` after every load, every probe and every gesture,
with and without motion; the entrance release's three animations `finished`.

## Findings

1. **Major — «Ma situation»'s question change animates when a key asks for it.** Enter on «Continuer» or «Précédent»
   (Space, and Enter on a Stepper link, reach the same `show()`) runs the leaving fade (120 ms) and the arriving slide
   (200 ms from 16 px) exactly as a click does: the instrument logs both `animate()` calls in the key's phase, with
   `html[data-input="key"]` set (`probes/wizard-fr.json`, `wizard-ar.json`; 1440 and 390). Plan §1.5's tier 0 —
   «every keyboard-initiated change (T-7, R-07): 0 ms» — and `head.js`: «a change asked from the keyboard is tier 0,
   there in the next frame». Everywhere else a key asks for a change it is there at once — measured here for the
   overlays (the phone sheet, the console drawer and the filter's sheet open and close from the keyboard with 0
   transitions), the portico and the skip link (this area's own F4 / F5) and the rail; written as one
   `html[data-input="key"]` rule for the buttons, the fields, the tabs and «Ma situation»'s own options (`_wizard.css`
   §4: «tier 0 … asked from the keyboard, the change is there in the next frame»). `situation.js` asks
   only `reducedMotion()`. Not introduced by W4-B — the branch point animated the same way through Motion
   (`probes-base/wizard-fr.json`) — but the area rewrote this very animation (F2) and AUDIT.md §6 lists it for «click /
   tap» only, while §10 and DL54-153 state that everything else meets its tier. Not a WCAG 2.2 AA failure (2.3.3 is
   AAA; under the setting the change is still). Meanwhile the focus lands on the arriving question while it is at
   opacity 0, so a keyboard user sees its ring only once it has faded in, ≈ 320 ms after the key. *Fix:* in
   `static/js/src/situation.js`, `const animated = Boolean(travel) && !reducedMotion() &&
   document.documentElement.getAttribute("data-input") !== "key";` — the question then swaps at once, as under the
   setting — and one browser case in `tests/frontend/test_motion_browser_w4_b.py` beside the reduced-motion ones (focus
   «Continuer», Enter: no animation created, the arriving question whole at once with the focus on it); the JS dist
   rebuilt; AUDIT.md §6's row and DL54-153 say «from the keyboard at once».

2. **Minor — «Ma situation»: a return within the leaving fade leaves no question on the page and the focus on `body`**
   (the review's m2, cross-checked). «Continuer» then «Précédent» 40 ms later, or a Stepper jump to Q3 then back to Q1
   40 ms later (pointer), end with the Stepper on Q1, «1 / 8», no question card drawn — and `document.activeElement` is
   `body`: the question the second change focused was hidden under the focus by the first change's late `enter()`, so a
   keyboard or screen-reader user is put back at the top of the document with nothing to read (fr and ar, 1440 and 390;
   `probes/review-crosscheck.json`, `race-*.png`). Rare by hand (the window is the 120 ms fade), and finding 1's fix
   closes it for the keyboard; the pointer keeps it. *Fix:* the review's — a generation token in `show()` that a late
   `enter()` checks before it hides anything, and a change asked in flight first lands the old one (cancel the steps'
   animations, clear their inline opacity); the test asserts exactly the current question drawn at opacity 1, no
   `style`, and the focus on it.
3. **Minor — the console bar's trail links fade when the keyboard focuses them** (the review's m3, cross-checked):
   «Accueil» / «الرئيسية», reached by Tab with `html[data-input="key"]`, run a 120 ms colour transition in and out (fr
   and ar, 1440). Tier 0, as finding 1; plain links have no keyboard rule (W1-C's cover buttons, fields, tabs).
   *Fix:* the review's one rule, `html[data-input="key"] a { transition-duration: 0ms; }` in `v5/base.css` (through
   the steward, as F4 and F5).

## Seen on the way — outside this area (for the orchestrator; not counted in the verdict)

- **O1 · the home at 390 — a focused link at the screen's bottom edge loses the bottom of its ring** («Autres voies
  régulières», «Découvrir le projet pilote»: fill 0.59, fr and ar, forced colours too). Chromium scrolls the link's box
  into view, not its outline; partly visible, not a 2.4.11 failure. A `scroll-padding-block-end` of ≥ 6 px on the root
  would keep it whole — for W4-A / W4-C.
- **O2 · SP-8's 44 px.** Under a finger: the public footer's links (24–25 px to the finger on the login page at 390) and
  the dashboard's «Profil» in «Mon compte» (32 × 44 at 390, fr). On a fine pointer: the rail's foot tools (the fold
  control, «Se déconnecter», the language and «Site public» rows) are 36 px tall, where SP-8 lists the rail. WCAG
  2.5.8's 24 px holds everywhere; pre-existing (the foot, W3-B, W3-A) — for W4-A's target sweep.
- **O3 · every page loads esbuild's 672 B runtime-helpers chunk as a request of its own** (`chunks/chunk-MVEBZ5U4.js`,
  imported by `shell.js` and every entry): with it the login stays one script request above W1-0's count. A build
  question for the steward / W4-C, not W4-B's.
- **O4 · the hero's origins run their light on a keyboard focus** — W2-D's documented review fix (the states instant,
  nothing under the setting or in forced colours): with finding 1 fixed, the one place a key starts motion, by
  decision. Recorded for the CD; nothing to fix here.

## Not checked

WebKit and Firefox (only Chromium is installed); a screen reader (the tree read is Chromium's); a real phone; the
compressed twin 8782 (the before/after is relative, on the lane's dev server); «Mes pièces» in Arabic (no language
prefix; the persona's language is French); the loose piece's alert dialog (no loose piece in the lane's data; the
overlay system is not W4-B's code and m4's test covers its resize path); the rail's account popover from the keyboard
(the probe's selector found no trigger — the other three overlays stand for the system); the login's L1 / L2 key
mid-flight; the case file (W3-E's, merging into design-v5 during this check); 1.4.12 text spacing (W4-B changed no
layout rule but the rail's transitions).

## The lane, cleaned

The seven minted sessions revoked on `ile_v5_l8` (`sessions.py revoke`: 6 + 1 rows deleted, the cookie file removed); the
server on 8788 stopped; this role's Chromium profile deleted and no browser of it left running; the `.env` copy removed from the
base export; the benchmark lock never created; scratch and evidence outside every repository. This report is the only
file this role wrote in the worktree.
