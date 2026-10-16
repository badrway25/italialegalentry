# W2-C2 · The navbar, part 2 — the phone sheet, the targa's account popover, the panel on `overlay.js`

Implementer `w2-c2-impl-1`, 11–12 October 2026 (V5.5 delivery mode; plan §3.4 item 5, §1.12 items 6–8, §1.11, §1.14;
surfaces.md §1.3 items 7–8, §1.4 N8 N9 N13 N14 N19, §4.4 O2–O8). Branch `v54-w2-c2`, worktree
`C:/tmp/ile_wt/v54-w2-c2`, lane 8788 (`ile_v5_l8`; tests on `test_ile_v5_l8`). Scratch:
`C:/tmp/ile_v5_council/.work/w2-c2/w2-c2-impl-1/` (the step's second session: `resume/`); evidence:
`C:/tmp/ile_v5_council/evidence/v54/w2-c2/`. Decisions: DL54-96.

**Status: built and checked, ready for the review — one item not done: the desktop panel's switch to `overlay.js`
(item 3), which the contract cannot carry yet («For W2-A» below).** The branch started from `v54-w2-a`, merged its
budget fix as it landed (`64558c8`, `a4bd279`, `1fbb8f9`), then design-v5 once `v54/w2-a` was tagged (`46360c6`, at
`361b03d`): design-v5 is an ancestor of the branch, its content was already here, the bundles were rebuilt from a clean
dist (nothing changed). The family's decision entry is DL54-96, after the steward's DL54-95.

## What is built

- **The sheet below 80rem** (`templates/partials/main_nav.html`, «sheet»; `static/css/v5/chrome.css` §7;
  `static/js/src/nav.js` `initSheet`): the overlay system's modal drawer (`data-overlay="drawer"`, CONTRACT §1), at the
  body's level after the letterhead, opened by «Menu» (a link to it: the no-script path shows it in place). Its own head
  line — the lock-up and «Fermer» (`data-overlay-focus`: the first focus) on the letterhead's row and measure, so the
  bar becomes the sheet's head without a jump. Then the Fase 3 order: the languages by their own names → the four doors
  as 64 px rows on night glyph discs, each unfolding in place (an exclusive `<details name>`; the locked gloss, the
  entries with their live second lines, «Voir l'espace»; the current section's door open; no height animation) →
  Forum · Projet → the FAQ's search (only when that page is public) → the primary → the anti-fraud line → the foot
  pinned on night («la targa» at 44 px, or signed in the account popover's trigger; the promoter). Below 48rem it takes
  the screen «Quiet» (opacity; the body and the foot rise 12 px; the drawer's clocks 320 / 200 ms); from 48rem the
  side sheet slides in from the inline end (the letterhead keeps its lock-up, «la targa», the promoter); from 64rem it
  carries Forum · Projet · the languages · the search (the band as W2-C1 built it). The overlay system holds the trap,
  the one scrim, Esc, «Fermer», a link, the focus back on «Menu», the scroll lock without a shift and the page out of
  the accessibility tree; `nav.js` only puts the sheet away when the window is widened past 80rem.
- **The signed-in targa's account popover** (`templates/partials/header.html`): `components/account_menu.html` with
  `popover` in the targa's seat (the person glyph alone below 100rem, the name beside it from there) and in the sheet's
  foot — the system's popover: hung on the trigger's inline end, the focus on its first row, ↓ ↑ Home End, Esc and the
  focus back, closed when the focus leaves or a row is chosen; a bottom sheet over the one scrim at ≤ 40rem.
- **The key alone** is named by the system's shared top-layer tip (`data-tip="layer"`), refused through the cancelable
  `overlay:tip` from 100rem where the plate says its word (`nav.js` `initTarga`): the control's own CSS tip became
  page-only in W2-A's budget fix.
- **No hole when the flags are off**: signed out with nothing to seat, the end zone is marked
  `site-header__end--bare` and, from 80rem (no «Menu» either), not drawn — it took the row's gap and left the bar 16 px
  short of the column's edge (measured at 1280, fr and ar).
- **`overlay.js` on every public page**: `static/js/src/shell.js` imports it (one chunk with the console's).
- **The drawer's last legacy rules deleted**: the V4 drawer's markup (`header.html`) and script (`nav.js` `initDrawer`;
  `initTarga`'s CSS-tip handling), `v4/shell.css` (the file and its import in `main.css`), `components.css`'s V4 drawer
  panel guard in the reduced-motion block (`components.css` keeps its 17 sections: §7 itself had left with W2-C1), the
  account menu's `<details>` face, `main.js`'s `initDropdowns` fallback, V4's segmented language track. As W2-A's own
  comments asked once `shell.js` imports the system.

## Not done — item 3, the desktop panel on `overlay.js`

Plan §1.12 item 6 and RTD-m8: the portico panel's scrim, dismissal and focus from `overlay.js`, the panel still a
disclosure navigation. The contract's API opens kinds (dialog, alert, drawer, sheet, popover); it has no primitive for
a disclosure region, and the popover family cannot carry the panel without breaking what W2-C1 shipped:
- without anchor positioning (Firefox; Safari before 26) the module writes `left` / `top` on every popover it opens
  (`placeByScript` → `extras.place`), and the panel hangs from the content width (N1);
- its keydown model moves ↓ ↑ Home End among the panel's stops and wraps; the portico's ↑ from the first entry returns
  to the door and ← → change door (NAVIGATION §4.8, 22 keyboard checks);
- a shown popover is in the top layer with the UA popover rules: the panel's geometry would need script, and the
  no-script hover / focus-within path fights `[popover]:not(:popover-open)`;
- the photographs' cross-fade on a door change needs the leaving panel ABOVE the arriving one (its photograph fades out
  over the new panel, `.is-leaving`): two auto popovers stack in the order they were shown, so the arriving panel's
  opaque paper would cover the leaving one — the cross-fade the step must keep unchanged would be lost;
- the system's scrim is for trapped panels and phone menu sheets (full viewport); the portico's stands below the
  letterhead, never over the utility bar (A11Y M3), at `--scrim-overlay`, not `--scrim-modal`.
So `nav.js` keeps W2-C1's adapter (its header says so), the motion tokens are already the system's, and the request
is below. The switch lands when the primitive exists (W2-C2's follow-up, a small change in `initPortico`).

## For W2-A

1. **A disclosure primitive for the portico** (plan §1.12 item 6, RTD-m8), in whichever shape the contract prefers —
   e.g. a `data-overlay="disclosure"` kind, a region that stays in place (no top layer, no placement), opened by
   `open(panel, {opener, focus: false, instant})` from intent, a click or a key; dismissed by Esc wherever the focus is,
   a press outside a named scope (`data-overlay-scope`: the `nav`, so a press on another door is a switch, not a light
   dismiss) and the focus leaving that scope; the focus back on the opener after Esc; `aria-expanded` on the opener; no
   key model of its own (the portico keeps ← → ↓ ↑ Home End); optionally the scrim below an edge (the letterhead's foot)
   at `--scrim-overlay`. Or two opt-outs on the popover family: `data-overlay-place="none"` (no anchor binding, no
   script placement) and `data-overlay-keys="none"`, plus the in-place rendering.
2. **The letterhead's fallback is gone, so its traces can go** (W2-A's files, not touched here): CONTRACT §6's
   «W2-C2 adds it to `shell.js` … until then `main.js` keeps a fallback for the letterhead's `<details>` account menu»
   (now done); `wireDisclosure`'s `data-dropdown="overlay"` marking and its comment, written for `main.js`'s fallback,
   which no page loads any more (test_overlays pins the marking); `overlays.css` §9's «on design V4's summary (the
   letterhead's, until W2-C2)» with the summary-only declarations (`list-style: none`,
   `.account-menu__summary::-webkit-details-marker`): a few dozen bytes of `main.css`.
3. **The core chunk on public pages.** It is now on every public page (6 466 B gzip; plan §2.6's module budget 4 KB,
   the figure DL54-94 recorded). The home's JS is 51 136 B gzip in all against §2.6's «a public page ≤ 45 KB» (45 584 B
   before this step: the Motion library's 26.6 KB chunk is most of it, W4-B's). Whatever of the core is console-only
   and could load on demand would come off every public page.

## Measures

**CSS — the shared payload** (gzip −9 as the stewards weigh it, `gzip.compress(data, 9)`, bundles rebuilt from a clean
dist; before = design-v5 at `v54/w2-a` (`361b03d`, the steward's figures); after = this branch's HEAD;
`evidence/v54/w2-c2/weight-before-design-v5-361b03d.json`, `weight-final.json`):

| Page type | before | after | change |
|---|---|---|---|
| an interior page (`main.css`) | 42 152 | 41 565 | −587 |
| the home (+ `hero.css`, `pages.css`) | 56 803 | 56 216 | −587 |
| the login (+ `entrance.css`) | 47 013 | 46 426 | −587 |
| the console page types (`main` + `console` + `portal`) | 50 893 | 50 306 | −587 |
| «Mes pièces» (+ `documents.css`) | 52 065 | 51 478 | −587 |
| the company's dashboard (+ `companies.css`) | 51 766 | 51 179 | −587 |

The shared payload does not grow: every page type is 587 B lighter. Nothing of this step is page-only and nothing
links `css/dist/core/overlay-panels.css`: the sheet is the drawer family with its own head, the popover and the layer
tip are the shared part. Where the bytes went: `v4/shell.css` and the drawer's rules out, the V4 language track out,
the sheet's rules on the shared `.portico__*` drawing (one drawing of the entries, «Voir l'espace», the foot and the
disc for the bar's panel and the sheet).

**JS** (gzip −9; the static module closure of the page's entries, plus `main.js` and `head.js`): an interior page
38 007 → 43 559 B, the home 45 584 → 51 136 B (+5 552: the overlay core 6 466, the nav chunk −397, `main.js` −536).
Script requests before `load` on the home: 8 → 9 (the overlay chunk, shared with the console's cache).

**N9 / O7 — the sheet's cold open** (lane 8788, dev server, Chromium headless, 390 × 844 @2, touch, CPU × 4 by CDP, a
fresh context per load, tap «Menu» 2.5 s after `load`, then «Fermer»; Event Timing, the longest event of each
interaction; n = 9 per cell; `evidence/v54/w2-c2/inp-*.json`, script `.work/…/inp.py`):

| Run | machine | fr open p90 (median) | ar open p90 (median) | close p90 fr / ar |
|---|---|---|---|---|
| `inp-4` | CPU 21 % | 168 (152) | 192 (136) | 120 / 168 |
| `inp-5` | CPU 23 % | 144 (136) | 192 (152) | 120 / 168 |
| `inp-3` | CPU 85 % (other lanes' browsers) | 200 (152) | 224 (200) | 160 / 216 |

N9 holds (p90 ≤ 200 ms) wherever the machine is not saturated; the Arabic margin is thin (192). The open's own cost is
the sheet's first style and layout (187 layout objects, inside the tap's task because the focus moves in — O3); no
rule restyles the page (no selector reads `aria-hidden`; the rise is named by class, never `*`).

**N8** — 0 photographs on a phone, sheet open, every door unfolded, fr and ar (smoke probe `photos: 0` on every phone
capture), and none with Save-Data from 80rem (`test_no_photograph_on_a_phone_nor_with_save_data`); from 80rem without
Save-Data the four arrive at idle after `load` (W2-C1's rule, unchanged).

**N13** — «la targa» seated in both states: signed out the plate (32 × 32 key alone below 100rem, the word from 100rem),
signed in the popover's trigger on the same plate; 32 px on a fine pointer, 44 under a coarse one; the key alone named
(`aria-label` + the layer tip); no hole when the flags are off (above; `test_the_flag_off_leaves_no_hole_in_the_letterhead`,
1280 / 1440 / 1920, fr and ar; the sheet's foot keeps the promoter: `test_the_flag_off_leaves_no_targa_in_the_sheet_and_no_hole`).

**N14** — no target under 44 px in the sheet under a coarse pointer at 360 / 390 / 412 / 768, fr and ar (smoke probe:
`small: []`; `test_every_target_of_the_sheet_holds_44_px_under_a_finger`); on a fine pointer the languages keep 24 px
(§1.11). «Italiano»'s ring whole in the viewport (probe and test). An unfolded door adds no glyph; the desktop panel
keeps W2-C1's two.

**N19 / O5** — Arabic: the architrave under the active door and the panels' entries following the doors
(`test_rtl_browser_nav.py`, W2-C1's, green); the account popover hung on the trigger's inline end (its left edge on the
trigger's, measured at 1440); the side sheet comes and goes by the left — a drawer mirrors (CONTRACT §5) — and the
phone's rise is vertical, no sideways travel in either language (`tests/i18n/test_rtl_browser_w2_c2.py`).

**O2–O8 for the sheet and the popover** — exit by the entry edge with the leaving panel `inert` (no click, no Tab);
`open`, `aria-expanded`, `aria-modal` and the focus set in the tap's task (keyboard opens: tier 0, no animation on the
first frame); reduced motion one 80 ms opacity, no transform; the focus back on «Menu» / the targa, Esc everywhere, the
popover closed when the focus leaves; the page held with `html[data-overlay-lock]` (the gutter kept where a scrollbar
exists), no horizontal scroll at any width (`scrollWidth = clientWidth` on every capture); 0 console errors.

**Seen** (`evidence/v54/w2-c2/smoke3/`, probes `probe-0.json` … `probe-2.json`): forced colours (the sheet with a door
open at 390 — its pinned foot, whose night the mode removes, now keeps a `CanvasText` line; the popover at 1440) and
reduced motion (the Arabic sheet at 390, settled); the sheet open at 360 / 390 / 412,
each of the four doors unfolded, fr and ar; the keyboard open and «Italiano»'s ring; the signed-in foot's popover as a
bottom sheet over the scrim; the side sheet at 768 (fr, ar with a door open); the 1024 and 1279 bands (fr, ar, the
keyboard's ring on «إغلاق»); the account popover at 1279 and 1440 (fr, ar); the desktop panel at 1440 (W2-C1's look,
unchanged); the sheet over a door page (`/fr/parcours/`), the FAQ (fr 390, ar 412) and the login (W2-B's page).

## Tests (lane 8 databases; one pytest and one browser at a time)

- Non-browser: `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline`,
  `test_nav_sheet_w2_c2`, `test_cms_nav`, `test_overlays`, `test_overlays_console_w2_a`, `test_layout`,
  `test_css_tokens_exist`, `test_rtl_static`, `test_loader_rules`, `test_v5_tokens`, `test_template_comments_do_not_leak`,
  `tests/compliance`, `apps/cms` — green. `test_design_docs`: green but
  `test_capture_report_is_current_and_backs_the_documented_figures`, which reads the steward-only
  `docs/qa/design/capture-report.json`: `capture.py` now records the sheet's `top`, so the report must be regenerated
  at the merge (plan §2.2 step 3); the documents already carry the sheet's figures (844 / 844 px at 390 × 844, 768 /
  768 px at 1024 × 768; G-02, G-04, G-23 closed).
- Browser (Chromium headless): `test_browser_w2_c2` (12, incl. the new flag-off test), `test_rtl_browser_w2_c2` (3),
  `test_browser_w2_c1` + `test_header_fits_the_narrowest_viewport` (17), `test_browser` + `test_rtl_browser_nav`
  (13), `test_rtl_browser` nav slice (9), `test_overlays_browser_w2_a` +
  `test_rtl_browser_overlays` (30), `test_overlays_console_browser_w2_a` (14) — all green, 0 skipped, no crashed run.
- Not run: WebKit and Firefox (not installed on this machine; installing browsers is outside the step's rules); the
  full suite (an integration checkpoint's).

## Ownership

`scripts/check_ownership.py w2-c2 v54-w2-a`: 4 inside, 8 slice, 5 generated, 16 outside. The 16, each the consequence
of the sheet replacing the drawer or of W2-A's hand-over (for the merge step to write into the manifest):
- `docs/ACCESSIBILITY.md` — the sheet's and the popover's rows (§3, 1.4.13, 2.1.2, 2.4.3, §9.1 targets, §11, §12.1;
  G-02, G-04, G-11, G-23), W2-C1's precedent;
- `docs/qa/design/capture.py` — W2-C1's «drawer selectors and figures»: the selectors follow the sheet (`#nav-sheet`,
  the system's scrim, the sheet's `top`);
- `static/css/main.css` (the `v4/shell.css` import line) and `static/css/v4/shell.css` (deleted) — the deletion map's
  «W2-C1 (W2-C2 for the drawer's last rules)»; the file held only the account menu's `<details>` face;
- `static/js/main.js` (`initDropdowns` deleted) and `templates/components/account_menu.html` (the `<details>` face
  deleted) — W2-A's files, deleted as W2-A's comments asked once `shell.js` imports the system;
- `templates/components/language_segmented.html` — V4's segmented track, drawn for the drawer and the console bar,
  whose families redrew them: no caller left;
- `templates/dev/showcase.html` — its account-menu demo shows the popover face, its language demo on the bar's night;
- tests that pinned the drawer or the hand-over: `tests/frontend/test_browser.py`, `test_browser_w2_c1.py`,
  `test_cms_nav.py`, `test_layout.py`, `test_overlays.py`, `test_overlays_console_w2_a.py`,
  `tests/i18n/test_rtl_browser.py`, `test_rtl_static.py` — each assertion follows the sheet or the popover, none
  weakened.
Slices: `test_design_docs.py` also carries W2-C1's assertions on the sheet (at the body's level, the G-23 rule with the
sheet's own head, «Menu» opens the sheet); DS 2026 besides §11's prose: §10 / §16 / §21's sentences on the account
menu, the language control and the sheet, and §2's figures regenerated by `scripts/regen_design_inventory.py --write`.

## What is left

- **Item 3** (above): the portico panel's switch to `overlay.js`, after W2-A's primitive.
- **The steward**: `capture-report.json` regenerated by `capture.py`; DL54-96 renumbered if another merge lands first.
- **For W4-D**: `_legacy-tokens.css`'s `--nav-drawer-top` has no consumer since the drawer left (with DS 2026 §3.18 and
  §17's rows, and `test_css_tokens_exist.py`'s `RUNTIME_PROPERTIES`, whose comment still says `main.js` sets it).
- **The home's JS over plan §2.6's 45 KB** (51 136 B) — the overlay core and the Motion library (For W2-A item 3; W4-B).
- **N18** («richer than Fase 3»: the comp beside the build) stays the navbar review's, for W2-C1 and W2-C2 together.

## Review fixes

Implementer `w2-c2-fix`, 12 October 2026, 03:10 → 04:20 (V5.5: implement → review once → fix → ship). The items of
`REVIEW.md` (the senior review, `15d2a12`) and `A11Y_PERF.md` (the accessibility + performance check, `1821e36`),
every major fixed, every minor fixed or routed; no new package, CSP-clean, LF bytes. Lane 8 (8788, `ile_v5_l8`;
tests on `test_ile_v5_l8`), headless Chromium, one browser and one pytest at a time, no crashed run, the
`PERFORMANCE_BENCHMARK_LOCK` checked before every series (never present). The signed-in header through one session
minted with `Client.force_login` (`qa-person`; no password used, typed or stored), revoked at the end. Scripts:
`C:/tmp/ile_v5_council/.work/w2-c2/w2-c2-fix/`; evidence: `C:/tmp/ile_v5_council/evidence/v54/w2-c2/fix/` (E/ below).
Commits: `52c7929` (the JS), `b7e2bbe` (the CSS and the templates), `527ac45` (the tests), `9f43030` (DS 2026 §11,
ACCESSIBILITY), and this record with DL54-97.

### What was fixed, and how it measures now

| Item | Fix | Measured after (before) |
|---|---|---|
| REVIEW **M1** — the French letterhead on two rows at 1024 (iPad in landscape, a Windows window) | `chrome.css` §4: the letterhead is compact from 64 to 90rem — the lock-up at 32/17 (the scrolled state's size; 303.5 → 259.5 px), one block with the laptop band's, the 64–80rem block keeping only the doors | at 1024, spare under a finger / beside Chromium's 15 px scrollbar: **fr 42.8 / 39.8** (−1.2 / −4.2: two rows, a 129 px letterhead), en 52.2 / 49.2 (8.2 / 5.2), it 89.3 / 86.3, ar 160.3 / 157.3 — signed out and in identical; a 17 px gutter leaves fr 37.8 (fine) and 25.8 (coarse and gutter together); one row and a 65 px letterhead everywhere (E/probe-band-after.json, probe-band-after-in.json, probe-band-before.json; shots/after-1024-fr-*.png, gutter-1024-fr-0-closed.png) |
| REVIEW **M2** — the tablet sheet without its pinned foot | `chrome.css` §7: from 48rem only the head's lock-up is hidden; the night foot stays at 48–80rem | every sheet ends on «la targa» (44 px, the column's width) or, signed in, the account trigger, and the promoter: at 768 touch and at 1024 fine and touch, fr and ar, signed out and in; the trap's cycle **16 stops at 768, 10 at 1024** (15 / 9), the foot's targa among them, wrapping to «Fermer»; no target under 44 px under a finger, none under 24 on a fine pointer; no sideways scroll; 0 console errors, 0 CSP reports (E/smoke-side.json; shots/side-*.png) |
| A11Y **M1** — a tap on the menu sheet's scrim reached the phone sheet's rows | `overlay.js` (W2-A's module, a justified path outside the slice): `syncScrim()` leaves the scrim's z-index alone while a press holds it (`data-held`); `release()` re-syncs it | signed in, 390 × 844 touch, `page.touchscreen.tap` over a door, Forum and «English», fr and ar: pointerdown → touchstart → (the light dismiss; the focus back on the foot's trigger) → pointerup → touchend → **mousedown / mouseup / click on the scrim** (before: on the row); the menu closed, no door unfolded, the URL and the language unchanged, the focus on the trigger, the sheet open and `aria-modal`; the scrim back at z 49 after the click (E/smoke-scrimtap.json) |
| A11Y **M2** — the foot's account menu drew the night's ring on white (1.75 : 1) | `main_nav.html`: the foot is no longer `on-inverse`; `chrome.css`: the night's ring and halo only on the foot's own controls (`.nav-sheet__foot :is(.targa, .account-menu__summary)`) — no literal colour, tokens only | each focused row **#1d8a93** (4.11 : 1 on white), its glyph **#4a5a62**, at 390 (the bottom sheet) and 768 (anchored above the trigger, on its inline end), fr and ar; the trigger keeps #7fd1d8 on night (E/smoke-ring.json; shots/ring-*.png) |
| A11Y **M3** — the public pages' script beyond plan §2.6 | **recorded, not deferred** — DL54-97 item 4 names the figures and the A/B: a dynamic import of the overlay core would make the first press on «Menu» and on the account trigger race the chunk's fetch (a click shim and its replay, «Menu» upgraded to a button late, the keyboard's first tip missed, the scrim made in the tap) for no measured cost | home 51 136 → **51 156 B** gzip (+20: the held scrim, the `overlay:open` listener), an interior page 43 559 → 43 579; requests before `load` unchanged by the fix pass — the same modules, the import graph untouched (home 3 + 9, a door page 1 + 7) |
| REVIEW **m2** — a pinned door panel left open under the sheet or the popover in WebKit | `nav.js`: any `overlay:open` of the system closes the door's panel | a door and «Menu» (1024), a door and the account trigger (1440 signed in) pressed by dispatched clicks that move no focus (WebKit's press): the panel and its scrim gone, fr and ar (E/smoke-portico.json). The panel's switch to `overlay.js` still waits for W2-A's disclosure primitive — tracked below |
| REVIEW **m3** — the side sheet on the page's 40 px margin | `chrome.css` §7: `--grid-margin` re-pointed to 24 px in the sheet from 48rem (head, body and foot alike) | a **371 px** column at 768 (339); the primary «Découvrir le questionnaire d'orientation» on one line in fr and ar (two in French with the old 40 px, checked by the same line count: E/probe-misc.json) |
| REVIEW **m4** — the unfolded door's gloss read as one more grey second line | `.nav-sheet__gloss`: `--t-ui` on a 24 px line, `--text-1` | the gloss 15/24 in ink (400), the entries' titles 17/24 (500), their second lines 13/20 in `text-2` (14 in Arabic) (E/smoke-gloss.json; shots/gloss-390-*.png) |
| REVIEW **m5** — «Menu» and «Fermer» of different widths | both buttons hold both words in one grid cell, centred, the other hidden (`.nav-toggle__alt`, `aria-hidden`; named by a class: no rule may select `[aria-hidden]`, W2-A's guard); below 48rem 6 px inside (8) so the phone row's arithmetic holds; from 48rem the alternate word is not drawn | one width per language — fr **88.6**, it 82.6, en 78, ar 80.8 — with both edges equal (fr 84 → 95 and its leading edge 11 px before); spare at 369: fr 0.9, it 6.9, en 11.5, ar 8.7 (and «Fermer» no longer runs 5 px past the column at fr 369); one outline in the 60 ms frame (E/probe-toggle-final.json, probe-toggle-before.json, m5-frames.json; shots/m5-390-*-opening-60ms.png) |
| REVIEW **m6** — the signed-in trigger 2 px high in Arabic | `:is(.targa-seat, .nav-sheet__foot) .account-menu { display: flex; }` | the trigger's middle on the row's at 768, 1024, 1440, fr and ar (64 / 76 against 64 / 76; the wrapper 32 or 44 px, was 36) (E/smoke-seat.json) |
| REVIEW **m7** — Android's tap tint on the chrome | `:is(.site-header, .utility-bar, .nav-sheet) :is(a, button, summary) { -webkit-tap-highlight-color: transparent; }` | the rule on every link, button and summary of the public chrome; `.btn` already had it |
| A11Y **m1** — at 320 × 256 the head and the pinned foot left the list one row | `chrome.css` §7, `@media (max-height: 30rem)`: the sheet scrolls as one (`display: block`), the head sticky on paper, the body unclipped, `scroll-padding-block-start: var(--header-h)` | at 320 × 256 the list takes **78 %** of the viewport (31 %), fr and ar; 844 × 390 84 %; the keyboard reaches «la targa» at the end, no stop under the head or off screen; 390 × 844 keeps the pinned foot (E/smoke-short.json; shots/short-*.png) |
| REVIEW **m1** — the scrim and an inline-end drawer stop at a classic scrollbar's gutter | **routed to W2-A** (the scrim and the scroll lock are its): «For W2-A» item 4 below | unchanged: the 15 px strip at 1024 with scrollbars shown, fr and ar (E/shots/gutter-1024-*-1-open.png, re-captured on the final tree) |

Also seen on the final tree: forced colours at 768 (the side sheet's foot keeps its `CanvasText` line, the plates
their borders: E/shots/fc-768-fr-sheet.png); no script at 768 (the `:target` sheet shows in place with its foot at
the bottom: E/probe-misc.json, shots/nojs-768-fr-sheet.png); reduced motion and the side sheet's slide by the inline
end (the family's tests, below).

### Measures

**CSS — the shared payload** (gzip −9 of the committed bundles, rebuilt from a clean JS dist and by `build:css`):

| Page type | base `361b03d` | before the fix pass `1821e36` | after `b7e2bbe` |
|---|---|---|---|
| an interior page (`main.css`) | 42 152 | 41 565 | **41 697** |
| the home (+ `hero.css`, `pages.css`) | 56 803 | 56 216 | 56 348 |
| the login (+ `entrance.css`) | 47 013 | 46 426 | 46 558 |
| the console page types (`main` + `console` + `portal`) | 50 893 | 50 306 | 50 438 |
| «Mes pièces» (+ `documents.css`) | 52 065 | 51 478 | 51 610 |
| the company's dashboard (+ `companies.css`) | 51 766 | 51 179 | 51 311 |

The fix pass adds 132 B to every page type (the band's merged block, the toggle's cell, the foot's ring, the side
sheet's margin, the short viewport, the tap tint); the family stays 455 B under the base on every page type. No page
sheet changed. design-v5 has moved since (`v54/w3-f2`: `main.css` 41 464 B, DL54-99): the merge step weighs the merged
tree against that ceiling.

**JS** (the static closure of the page's entries + `main.js` + `head.js`, gzip −9): the home 51 156 B, an interior
page 43 579 B (+20 each); the overlay chunk 6 476 B, the nav chunk 3 143 B.

### Tests (lane 8; one pytest and one browser at a time; no crashed run)

- Non-browser: `test_nav_sheet_w2_c2` (11, the new `test_the_review_fixes_hold_in_the_sources` among them),
  `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_overlays`, `test_v5_tokens`,
  `test_template_comments_do_not_leak` — **589 passed**; `test_design_docs` 39 passed and the known steward-only
  `test_capture_report_is_current_and_backs_the_documented_figures` (the capture report is regenerated at the merge,
  as recorded above); `scripts/regen_design_inventory.py`: current (DS 2026 §2's chrome.css 47.4 → 50.5 KB written).
- Browser (Chromium headless): `test_browser_w2_c2` **25 passed** — six new tests (the band at 1024 in four
  languages × signed out / in × fine / coarse × with / without a 17 px gutter; the side sheet's foot, margin, one-line
  primary and trap, fr + ar; the menu sheet's scrim tap over a door, Forum and a language, fr + ar; the foot's menu's
  paper ring at 390 and 768, fr + ar; the portico closed by an opening that moves no focus; the short viewport,
  fr + ar) and two extended (one toggle width; the band's foot); `test_rtl_browser_w2_c2` +
  `test_header_fits_the_narrowest_viewport` **8 passed** (the Arabic trigger on the row's middle; the phone row at
  320–390 with the new toggle widths); `test_overlays_browser_w2_a` + `test_rtl_browser_overlays` **30 passed**;
  `test_overlays_console_browser_w2_a` + `test_browser_w2_c1` **26 passed**; `test_browser` +
  `test_rtl_browser_nav` **13 passed**.
- Not run: WebKit and Firefox (no engine on this machine; m2's WebKit press is reproduced by dispatched clicks); the
  full suite (an integration checkpoint's).

### Ownership

`scripts/check_ownership.py w2-c2 361b03d`: 6 inside, 9 slice, 19 generated, **17 outside** — the 16 of «Ownership»
above and one new: **`static/js/src/overlay.js`** (W2-A's module), the four-line fix of A11Y_PERF M1 that the check
itself placed there (plan §2.2: a justified extra path; W2-A's REVIEW M1 promised that a menu sheet's scrim takes the
whole press, and only this family's composition — a menu sheet over a trapped drawer — reached the case). The merge
step writes it into the manifest with the 16. `docs/ACCESSIBILITY.md` (already among the 16) received four clauses.

### For W2-A (added by the fix pass)

4. **The scrim and an inline-end drawer beside a classic scrollbar** (REVIEW m1): with `html[data-overlay-lock=
   "gutter"]` the gutter is kept, so nothing moves sideways, but neither the scrim (`inset: 0`) nor a drawer at the
   inline end reaches it — a 15–17 px undimmed strip runs down the window's edge whenever a trapped modal opens
   (glaring in Arabic beside the dimmed page; E/shots/gutter-1024-ar-1-open.png). Every trapped modal shows it.
   Suggested: the scrim's inline size `100vw` (or an inset that reaches into the gutter) and an inline-end drawer that
   meets the window's edge; re-capture at 1024 with Chromium's scrollbars shown (`ignore_default_args=
   ["--hide-scrollbars"]`), fr and ar.
5. **The held scrim** (A11Y_PERF M1, written here in `overlay.js`): `syncScrim()` keeps the scrim's z-index while a
   press holds it and `release()` re-syncs — W2-A to own it from the merge; `test_overlays.py`'s guards are untouched.

### What is left (after the fix pass)

- **The portico panel on `overlay.js`** (plan §1.12 item 6, §3.4 item 5's gate): waits for W2-A's disclosure
  primitive (For W2-A item 1). Until then `nav.js` closes the panel on any `overlay:open` (REVIEW m2). This gate item
  stays open for W2-C2's follow-up — the switch is a small change in `initPortico` once the primitive lands.
- **The public pages' JS over plan §2.6** (the home 51 156 B, +1 request): recorded in DL54-97 with the A/B; the
  Motion library (26 611 B, W4-B's) is the largest share and leaves with W4-B.
- **The steward**: `capture-report.json` regenerated by `capture.py`; DL54-96 and DL54-97 renumbered after
  design-v5's DL54-96 … DL54-99 (W3-F2's merge).
- WebKit and Firefox at the integration checkpoint: the sheet's `<summary>` rows drawn as grids, `<details name>`,
  `closedby`, the press without focus (m2), the held scrim on a real touch screen.

---

## Merge step — the steward's note on numbering (12 October 2026; label w2-c2-merge)

W3-F2's three entries and its merge's record (DL54-96 … DL54-99) reached design-v5 first, so at the family's merge
its two entries became **DL54-100** and **DL54-101** — the same order, add 4 — in the sync with design-v5 (`63b5860`).
Their content is unchanged but for their citations of each other: the second cited the first five times («amends
DL54-96 item 1», «DL54-96 item 5», its sources), which the log now writes DL54-100; the sentence that called each
number provisional now says what it was written as. The steward's own record of the merge is **DL54-102**. The code,
the tests, DS 2026 and ACCESSIBILITY.md cite none of the moved numbers.

How to read the numbers written before the merge — in this file and in `REVIEW.md` alike (`A11Y_PERF.md` cites none):

| Written | Read | The entry |
|---|---|---|
| DL54-96 | **DL54-100** | the sheet is the system's drawer with its own head; the targa's popover; the portico panel keeps its adapter |
| DL54-97 | **DL54-101** | the fix pass: the letterhead compact from 64rem; every sheet ends on its night foot; the held scrim; the script |

The exceptions are design-v5's own numbers, unchanged: «design-v5's DL54-96 … DL54-99 (W3-F2's merge)» («What is left
(after the fix pass)») names W3-F2's entries and its merge's record, and every other DL54 number in these files
(DL54-88 … DL54-95) is design-v5's.
