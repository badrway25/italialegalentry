# W4-C — Performance + accessibility consolidation: notes (w4-c-impl-1, 16 October 2026)

Plan §3.6 item 3 (W4-C), §2.6 (the budgets and their protocol on 8782), §1.6, §2.5, WCAG 2.2 AA; the owner's V5.5
(delivery mode), V5.8 (no shared CSS ceiling raised), V5.9 §15 («accessibility critical checks», «performance sanity
check») and V5.10 (the release gates). Worktree `C:/tmp/ile_wt/v54-w4-c`, branch `v54-w4-c` from design-v5 `5bf2f90`,
then design-v5 merged at `v54/w4-b` (`dd61b21`) before any measure, and again at the end (`fad36e0`: W4-D's part 1 —
documents, CI and deployment tests only). Lane 4: dev server 8784 on `ile_v5_l4`
(`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); pytest on
`TEST_DATABASE_URL=…/test_ile_v5_l4`. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/`; scratch:
`C:/tmp/ile_v5_council/.work/w4-c/w4-c-impl-1/`. Reports: `A11Y_SWEEP.md` and `PERF.md` (this folder).

## 1. What changed

| # | What | Where (owner) | Commit |
|---|---|---|---|
| F1 | **The questionnaire's resume form says its errors as every other form does**: the shared summary (`components/form_errors.html`: `role="alert"`, a link to the field, focused by `main.js`'s `initFormErrorFocus` after the round trip) in place of the bare non-field line — the sweep found it the one main form whose invalid answer left the focus on `<body>` | `templates/orientation/resume.html` (W3-F1's slice `templates/{ecosystem,orientation,pathways}/**`) | `8239d71` |
| P1 | **The Dépôt's zone drawn at its final size from the first frame** — its enhanced drawing (the input covering the frame, «Déposer un fichier», one row) keyed on `html.js`, which `head.js` sets in `<head>` before the first paint, instead of the `[data-enhanced]` that `depot.js` writes once its dynamically imported module has arrived: the zone no longer shrinks under the fields that follow it. Measured on the twin: **CLS 0.042–0.071 on every load of the upload page** (a flagship page of W3-C: budget 0.05 — 3 of 4 cells over) and 0.034 on a piece's page in Arabic → re-measured on the twin at n = 9 per cell: **0.000** on all eight cells (PERF.md). The sending frame keyed on the attribute only the script writes (`data-sending`); no JS change, no dist rebuild but the CSS | `apps/portal/static/portal/v5/_depot.css` (W3-C), `static/css/dist/documents/documents.css` (generated), `tests/frontend/test_depot_w3_c.py` (W3-C: the static assertion follows the two selectors) | `3ca0b0c` |
| — | The two reports | `docs/design-v5/QA/v54/w4-c/A11Y_SWEEP.md`, `PERF.md` (this folder) | `53404d0`, `b514012` |
| — | The record | `DECISION_LOG_V54.md`: DL54-159 (append-only, this area's own entry; written as DL54-156 after design-v5's DL54-155, renumbered at the merge — the sec-f8 merge's record took DL54-156, W4-A's entry and its merge's record DL54-157 and DL54-158) | `60fb0c6` |

**Weights** (gzip −9 from the files, `.work/w2-a/w2-a-merge/weigh_pages.py` and the same reading for the page sheet):
`dist/main.css` 31 799 → **31 799 B** (untouched), the console page types (main + console + portal) 39 978 → **39 978 B**
(untouched), `dist/documents/documents.css` 5 497 → **5 494 B** (−3; raw −114 B) — «Mes pièces» 45 475 → 45 472 B. No
shared ceiling raised, no page type's total grown. No JS changed (`static/js/dist` untouched).

## 2. The lane, the data and the cleanup

- Worktree created as briefed (`git worktree add … -b v54-w4-c design-v5` at `5bf2f90`; `.env` copied and pinned to
  lane 4 — `DATABASE_URL` → `ile_v5_l4`, `TEST_DATABASE_URL` → `test_ile_v5_l4`; `node_modules` a junction to
  design-v5's). **v54/w4-b merged before any measure** (a fast-forward to `dd61b21` at 08:30; the accessibility pass
  begun on the pre-W4-B tree was discarded and run again on the merged one).
- Lane server 8784 from this worktree (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview
  flag; `PGAPPNAME=ile-lane-4-w4c`); restarted once to load F1's template (Django's cached loader under `--noreload`).
  Sessions minted with `Client.force_login` on `ile_v5_l4` (11 personas) and on `ile_v5_perf` (9) by scratch scripts
  outside every repository; no password used, typed or stored; the cookie values only under
  `C:/tmp/ile_v5_council/.profiles/w4-c-impl-1/`. Revoked at the end: 11 session rows on `ile_v5_l4`, 9 on `ile_v5_perf`, both secrets files removed.
- Lane-only data, for the bridges' drawing: an institution and a university account (`w4c-institution@example.test`,
  `w4c-university@example.test`, unusable passwords, one organisation each), on `ile_v5_l4` only — deleted at the end with their memberships and organisations (checked: 0 left). One
  anonymous orientation session per language (the questionnaire's step, reached by «Commencer»), on the lane.
- One headless Chromium of this role at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w4-c-impl-1/`); one
  pytest at a time; every browser series and every build after `lock_gate.py`; this role's browser re-runs and builds
  during the perf series held the benchmark lock themselves (`held.py`), so they never ran beside a perf window.
  **No run ended on a crash.** Never 8780, Chrome 9222 / 9223, `ile_v5` or the V4 control.
- The twin 8782: switched to this worktree under the lock (09:28, `twin.py switch`: collectstatic 617 files / 1 455
  post-processed), switched again for P1's measure (12:16, the tree at `3ca0b0c`: the series' one gap refilled, P1's cells at n = 9), returned to design-v5's tree at the end (12:25, `twin.py restore`: collectstatic from `C:/tmp/ile_wt/design-v5`, 8782 started from it).

## 3. The measures, in short (the two reports hold the rest)

**Accessibility — `A11Y_SWEEP.md`.** 101 pages (every surface key of `live_status.json`, the four organisation bridges,
the staff's pages, the error pages, the open menu, a questionnaire step) × fr, ar × 1440, 390 = 404 page views per
pass; passes: the AX tree + axe-core 4.13.0 (from disk) + the keyboard walk + pixel and non-text contrast + 1.4.12 (desk,
phone), forced colours at both widths, 400 % (320 × 256), every overlay opener, the tooltips under the keyboard, the
forms' errors, Arabic's language of parts. **0 axe violation nodes on 404 views (WCAG and best-practice tags); every
one of 11 444 Tab stops indicated; none entirely under a fixed or sticky layer (2.4.11); the lowest focus ring 3.44 : 1
on its ground; the lowest text 5.19 : 1 on the pixels; 0 px of overflow at 400 %; every state distinguishable under
forced colours; 19 openers: focus in, Esc, focus back, axe inside the open panel 0.** The one failing pattern: F1
(fixed). The by-design patterns the probes flag (the register row's clipped separator point, the rail's and the phone
bar's ellipses with their words whole elsewhere, the architrave marking the current door under forced colours, the
stacked skip links, the self-sufficient 400 / 500) are listed with their counts, not counted.

**Performance — `PERF.md`.** The twin 8782 serving this worktree; 78 page types × fr, ar × 1440 @1, 390 @2; profile A
+ CPU × 4; n = 5 cold loads per cell, interleaved: 1 560 loads in nine windows. **LCP: slowest median 1 508 ms (PASS
on 312 cells). CLS: PASS but the upload page (0.042–0.071 on every load, a flagship page: 0.05) → P1 → 0.000 at n = 9.
INP: seven overlays cold, p90 ≤ 120 ms, 0 of 154 over 200 ms. Long tasks after the first paint: the rest of the
first layout (style + layout, Arabic text shaping), lighter than V4's single first-render task. Requests over W1-0's
count only by V5.8's page sheets and the 394 B helpers chunk, no measured cost, HTTP/2 measured (+8 ms median, noise).
Fonts, JS (the home 24 138 B), CSS (shared bundles unchanged), sprite and images within their figures.**

## 4. The hand-offs to W4-C / Wave 4, answered

Found with `grep -n "W4-C\|Wave 4\|W4 perf\|W4 sweep\|performance sweep"` over `QA/v54/*/NOTES.md`, `*/SHIPPED.md`,
`*/A11Y_PERF.md` and `DECISION_LOG_V54.md` (design-v5 at `dd61b21`); the accessibility and performance items only.

| From | Item | Answer |
|---|---|---|
| W2-A REVIEW m1 · DL54-93 item 7 · W2-A SHIPPED | the console drawer's cold open on the INP edge (p90 168 ms on the lane, a busy machine) — «Wave 4's measure on a quiet machine decides» | **Answered — no change needed**: on the quiet twin (profile A, CPU × 4, cold, n = 11) the drawer opens at **p90 112 ms** on the Arabic «Mes documents» at 390 and **112 ms on W2-A's own cell** (412 @1.75), closes at p90 88 / 96 ms; 0 of 154 cold interactions over 200 ms (PERF.md, INP). Plan §1.14's INP item 1 (the closed drawer laid out at idle) is not needed |
| W2-A REVIEW m2 (O10) · W3-C NOTES «Wave 4» · W3-D m6 · W3-D SHIPPED · DL54-154 item 9 | the drawer and the sheet, `::details-content`, «the motion seen at speed», in WebKit and Firefox | **Not run, and said**: no Playwright WebKit or Firefox binary on this machine (only Chromium builds under `%LOCALAPPDATA%/ms-playwright`), none downloaded (standing rule). Open for a machine that has them; no Safari, no real device, no screen reader run by a person (A11Y_SWEEP.md «Cross-engine») |
| W3-D A11Y_PERF O2 (W3-A / W4-B) | under forced colours the rail's current entry drew the focus ring's outline at rest — no focus visible on it | **Verified fixed** (W4-B `55efe3e`): on the 202 console views of the forced pass (1440 and 390, fr and ar) every Tab stop shows an indicator; the current entry is the underlined word and the Highlight disc, outline none at rest (A11Y_SWEEP.md, forced) |
| W3-D A11Y_PERF O3 (W3-A / the W4 performance sweep) | `html:has(.console-drawer[open])` re-styled the whole document on every `[open]` toggle | **Gone**: no `html:has(…[open])` rule is left (W2-A's step 2 moved the drawer onto the overlay system); the console's one document-wide `:has()` left is `.console:has(:is([data-console-action], [data-file-action-bar]))`, on body. The cold opens measured: p90 ≤ 120 ms on every overlay (PERF.md) |
| W3-D A11Y_PERF O1 | the case file's inspector scrolled inside itself with nothing focusable (axe `scrollable-region-focusable`) | **Gone**: no `scrollable-region-focusable` on either person's case file, fr and ar, 1440 and 390 (W3-E redrew the case file) |
| W3-E NOTES item 6 · W3-E SHIPPED · DL54-151 | budget letter: the case file links seven stylesheets (the one-sheet variant: one request less, 2.6 KB not reused from cache) | **Answered — keep the seven sheets**: the case file loads 7 CSS + 8 JS before `load` (W1-0: 3 + 8) and its LCP medians are 1 108–1 408 ms on the four cells, CLS 0.000 (max 0.0003), no task of its own beyond the first layout (the longest after the first paint 219 ms at CPU × 4, the per-cell TBT after FCP ≤ 50 ms); over HTTP/2 the extra requests cost nothing measurable either (HTTP/2 − HTTP/1.1 LCP on its four cells −60 to +68 ms, n = 3 each, within the spread). The one-sheet variant would save one request and lose 2.6 KB of cross-page cache reuse: no measured reason to take it |
| W3-F2 A11Y_PERF O1 (W2-C1 / the W4 performance sweep) | the signed-in letterhead shifted at 1440 (CLS up to 0.1125 in some loads) | **Confirmed, and wider — for W4-D** (corrected by the review fixes: W2-C1 is a closed family, REVIEW m1): not only signed in: 11 of 860 public loads on the twin show a shift through `nav.main-nav` (and the content below it) above 0.03, one over 0.10 (`training`, ar 1440: 0.109); every median ≤ 0.02, so no page is over its budget. Diagnosed by the fix pass: the menu's block size never changes (64 px); its inline place does, when the faces swap in (FCP + 10–95 ms, before `nav.js` runs) — «Review fixes», m1 |
| W3-F2 A11Y_PERF O2 · W4-B A11Y_PERF O1 («for W4-A / W4-C») | a focused link flush with the viewport's bottom edge loses the bottom of its ring (`scroll-padding-block-end` ≥ 6 px on the root) | **Not changed here**: not a 2.4.7 / 2.4.11 failure (three sides and the halo stay; W3-F2 and W4-B both say so), and the one declaration goes into `main.css` (every page), whose ceiling no merge may raise (V5.8): it has to be paid by a deletion in the shared bundle. The candidates W4-B listed for W4-D's legacy sweep (`--duration-reveal`, `--reveal-distance`, `--reveal-index` in `_legacy-tokens.css`, with DS 2026 §17's rows) pay it several times over — **for W4-D**, in the same commit as that sweep |
| W3-F2 A11Y_PERF A4 | «Privacy Policy» in English without `lang="en"` | **Fixed by the review fixes** (`8bd1f1c`; this row first read «already fixed», true only of the error pages' way-on list and the legal page's h1 — REVIEW m2): `lang="en"` on every standalone policy name — the public and console footers, the Forum's join form and privacy note; inside a translated sentence the name is the document's proper name (docs/ACCESSIBILITY.md, 3.1.2 and G-08) |
| W4-B A11Y_PERF O3 («a build question for the steward / W4-C») | esbuild's 672 B runtime-helpers chunk (`chunks/chunk-MVEBZ5U4.js`) is a request of its own on every page; the login stays one script request above W1-0's count | **Measured, not changed**: the entrance pages load 2 + 7 requests before `load` against W1-0's 2 + 6 — the 394 B chunk; no LCP cost (the login's medians 1 136–1 356 ms) and over HTTP/2 none (the same loads behind a local TLS proxy move LCP by a median +8 ms, −104 to +160 ms over 24 cells, n = 3 each: noise). Inlining it is a build change in `scripts/build_frontend.mjs` (W4-B's `INLINED` slice / the steward's build), with the JS dist rebuilt from clean in design-v5 only — **for the steward**, if the request ratchet is to be met to the letter |
| W1-C A11Y_PERF R1 / SHIPPED | the 2.59 : 1 ring beside its halo on public text fields; laguna-600 «optional, through the steward» | **Not changed**: ruled not a failure (1.4.11 measures the indicator against its neighbours: 3.70 / 3.94 against the ground); this sweep's ring check finds no stop under 3 : 1 against its ground on any page type |
| W2-C2 SHIPPED · W2-A · DL54-101 | the home's JS over §2.6's 45 KB until W4-B removed the Motion library | **Holds**: the home 24 138 B gzip on the wire (W4-B's figure), every public page ≤ 24 138 B, the heaviest console page 27 510 B (PERF.md) |
| W2-C1 A11Y_PERF item 5 | +1 script request per public page (the `nav.js` chunk) | **Holds**: W4-B inlined `nav.js` into `shell.js` (`INLINED`, `ec7b935`); a door page now loads 2 + 6 (W1-0: 1 + 6 — the +1 is its own page sheet, V5.8) |

## 5. Tests (V5.5: targeted; the integration checkpoints run the suite)

Lane test database `test_ile_v5_l4` (`TEST_DATABASE_URL=…/test_ile_v5_l4`), one pytest at a time, each run after the
lock gate (or holding the lock, between this role's own perf windows):

- **Non-browser, targeted** — `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline`,
  `test_design_docs`, `test_o14_lint`, `test_script_motion_gate`, `test_case_file_w3_e` (W3-E's family file),
  `test_layout`, `test_orientation_w3_f1`, `apps/orientation/tests`: **308 passed** (after F1); then, after P1,
  `test_depot_w3_c` (the updated static assertion), `test_documents_w3_c`, `test_css_bundle_is_current`,
  `test_design_docs`, `test_static_pipeline`: **117 passed**.
- **Browser, targeted** — `tests/i18n/test_rtl_browser.py`, `test_console_shell_browser_w3_a`,
  `test_console_phone_browser_w3_a`, the overlay browser tests (`test_overlays_browser_w2_a`,
  `test_overlays_console_browser_w2_a`, `tests/i18n/test_rtl_browser_overlays.py`), `test_dashboard_browser_w3_b`, the
  W3-C documents browser tests (`test_documents_browser_w3_c`, `test_drawer_browser_w3_c`, `test_depot_browser_w3_c`),
  `test_journey_browser_w3_d`, `apps/portal/tests/test_browser.py`, `apps/pages/tests/test_browser.py`,
  `test_orientation_browser_w3_f1` (F1's page): **275 passed**, 51 deselected (the non-browser tests of those files), 0 failed, 0 skipped (`-rs`), 25 min, one Chromium at a time.
- `scripts/check_ownership.py w4-c design-v5`: **PASS** — 3 inside (this folder's three reports), 1 slice (the decision log, append-only), 1 generated
  (`static/css/dist/documents/documents.css`), 3 delegated (`templates/orientation/resume.html` → W3-F1,
  `apps/portal/static/portal/v5/_depot.css` and `tests/frontend/test_depot_w3_c.py` → W3-C), merge base `fad36e0`.

## 6. What is left, and for whom

- **W4-D** (was «W2-C1», a closed family — REVIEW m1) — the letterhead's intermittent shift on public pages (W3-F2's O1,
  confirmed wider: 11 of 860 public loads above 0.03, one over 0.10; medians ≤ 0.02), diagnosed in «Review fixes» m1;
  and `card.css`'s French colon in every language (REVIEW m3, docs/ACCESSIBILITY.md G-14). Both are `main.css`
  rules, paid by a deletion in the same bundle (V5.8) — W4-D's legacy sweep.
- **W4-D** — the ring cut at the viewport's bottom edge (W3-F2 O2, W4-B O1): `scroll-padding-block-end` on the root,
  paid in `main.css` by its legacy sweep's dead tokens (`--duration-reveal`, `--reveal-distance`, `--reveal-index`, with
  DS 2026 §17's rows); and the lead the traces give (not a defect): the overlay core wires its panels at load (up to
  174 ms at CPU × 4 on a console phone page) — wiring them on first use would take it out of the load.
- **The steward** — esbuild's runtime-helpers chunk, one script request on every page above W1-0's count on the
  entrance pages (W4-B's O3): a build change in `scripts/build_frontend.mjs`, the JS dist rebuilt from clean in
  design-v5 only; no measured cost, so only if the request ratchet is to be met to the letter.
- **W3-C / W3-E** — records whose language is known (the ruleset's notes, written in French) could carry `lang="fr"`
  on the Arabic pages, when the content plumbing carries a language (3.1.2: not a failure today).
- **W2-C1 / the steward** — «Formation» marks two doors `aria-current`; the architrave sits under one (under forced
  colours the other shows no mark).
- **Not run, for a machine that has them**: Playwright WebKit and Firefox (W2-A's O10, W3-C's and W3-D's m6, W4-B's
  «at speed»); a real phone; a screen reader by a person.

## 7. For the merge step (the steward)

- **Paths** (`check_ownership.py w4-c design-v5`): this area's own `docs/design-v5/QA/v54/w4-c/**` and its
  `DECISION_LOG_V54.md` entry; delegated, each in its owner's slice and to be written into the manifest:
  `templates/orientation/resume.html` (W3-F1 — F1), `apps/portal/static/portal/v5/_depot.css` (W3-C — P1),
  `tests/frontend/test_depot_w3_c.py` (W3-C — the static assertion that follows P1's two selectors),
  `static/css/dist/documents/documents.css` (generated: rebuild from clean as usual — `npm run build:css` gives the same
  bytes; no JS was built).
- **Decision log**: DL54-159 (written here as DL54-156 after design-v5's DL54-155, W4-D part 1; renumbered at the merge, design-v5 having given DL54-156 to the sec-f8 merge's record, DL54-157 and DL54-158 to W4-A's entry and its merge's record).
- **Weights**: `dist/main.css` 31 799 B, the console page types 39 978 B — unchanged; «Mes pièces» 45 475 → 45 472 B
  (documents.css 5 497 → 5 494 B). No ceiling to move.
- **The twin 8782** is back on design-v5's tree (12:25, from `C:/tmp/ile_wt/design-v5`); its sessions revoked.

## Review fixes (w4-c-fix, 16 October 2026)

The fix pass for `REVIEW.md` (SHIP_AFTER_FIXES: M1, M2, m1–m4) and `A11Y_PERF.md` (SHIP_AFTER_FIXES: A1 = M2, A2 = M1,
a1, a2 = m1). Every major fixed; the minors fixed where cheap and safe, the rest handed by name. Lane 4 as before:
the dev server 8784 from this worktree on `ile_v5_l4` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`, no preview flag), then a compressed instance of the branch on the same port for the measures (the twin's
settings module with its own `STATIC_ROOT` and `ile_v5_l4`, as the review's 8884; the twin 8782 never touched);
two sessions minted with `Client.force_login` (no password used, typed or stored) and revoked at the end (2 rows, the
secrets file removed); one headless Chromium and one pytest at a time, every browser series and build after the lock
gate, the two measuring series holding `PERFORMANCE_BENCHMARK_LOCK` themselves (M2's measure 15:04–15:09, then the
letterhead's diagnosis); no run crashed. Scratch: `C:/tmp/ile_v5_council/.work/w4-c/w4-c-fix/`; evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/fix/`.

| Finding | Fix | Commit | Proof |
|---|---|---|---|
| **M1** (REVIEW) = **A2** (A11Y_PERF) — «Ma situation» declares no input purpose (WCAG 1.3.5) | `SituationForm` (`apps/accounts/profile_forms.py`): the date of birth `DateInput(attrs={"type": "date", "autocomplete": "bday"})`, the country of residence `TextInput(attrs={"autocomplete": "country-name"})`; the nationality has no HTML token and is left. A delegated path (W3-F2's slice there is the profile form's widgets) | `0858927` | the test beside W3-F2's profile test (`tests/frontend/test_service_pages_w3_f2.py`), `/fr/` and `/ar/espace-reserve/ma-situation/`, red before; 211 passed (with `apps/portal/tests/test_situation.py`, `apps/accounts/tests`); the smoke at 1440 and 390, fr and ar: `bday` and `country-name` on the inputs, axe 0 |
| **M2** (REVIEW) = **A1** (A11Y_PERF) — P1's lost-module path: a silent picker | **The CSS fallback A11Y_PERF measured, not the review's `.catch`** — one direction, the one that covers every way the module can fail to arrive (a lost `depot.js`, a lost `console.js`, a stalled import, a browser without modules), needs no state from the script and never touches the normal path: until `depot.js` has written `[data-enhanced]`, a chosen file (`:valid` — the zone's one control, `required`) shows the browser's own control in the frame, its name with it, set in by the frame's own padding, the frame's words unpainted in their box (`_depot.css` §2 bis). And the late module: a file chosen while `depot.js` is on its way is taken up when it arrives (`depot.js`: `wire()` dispatches the input's `change` once its listeners are on), so the name is never lost. **Paid in the page sheet** (V5.8: «a family that adds to documents.css first deletes»): the Dépôt's four `[hidden]` rules are one scoped `.doc-depot [hidden]` — which also covers the formats' note after the gate, hidden until now only by V1 `base.css`'s global rule, on W4-D's deletion map —, and the four rules that restated the one focus system on the filed answer and the state's heading are deleted (the ring read identical with and without them, fr and ar, keyboard and pointer: `fix/focus/focus.json`). The comments of `_depot.css` §2 bis, `console.js` 2d and `depot.js`'s header say it; the JS dist rebuilt from clean (the Dépôt's chunk renamed, `console.js` byte-identical) | `a3613b3` | four browser tests in W3-C's `test_depot_browser_w3_c.py` — the module's request aborted (fr 1440, ar 390: the control painted on top, the file's name in it, the zone's height kept, no overflow, no CSP report), the module held then released (the row takes the file up), a1's regions — each red before the fix, all 14 of the file green; W3-C's static pin of the rules; the lane, 20 cells (both pages × fr, ar × 1440, 390 + forced colours, blocked and normal): blocked — the control shown, the zone 76 → 76 / 96 → 96 px; normal — the fallback never matches, the row as before (`fix/fallback/`); **CLS re-measured on the compressed build: 0.000 on every cell, max 0.0005** (below) |
| **a1** (A11Y_PERF) — the polite region kept the previous file's sentence beside a refusal | `depot.js`: a new choice or a send empties both live regions first (`hush`, called by `clear()`), so neither keeps a sentence that no longer holds — fixed here rather than handed to W3-C, a closed family: one line in the module M2 rebuilt anyway | `a3613b3` | `test_a_refused_choice_leaves_no_sentence_of_the_file_before_it`, red before |
| **m1** (REVIEW) = **a2** (A11Y_PERF) — the letterhead's shift handed to a closed family | **Handed to W4-D by name** (§4, §6): the fix is a rule of W2-C1's `chrome.css`, inside `main.css`, which no merge may raise (V5.8) — it has to be paid by a deletion in that bundle, W4-D's legacy sweep. **Diagnosed** on the compressed build (12 desktop loads of «Formation» fr / ar, the login and «Parcours», under the lock; `fix/letterhead/letterhead.json`): the menu's block size never changes (64 px before and after); its inline place does — it moves 56 px toward the start at fr 1440, widens 437 → 715 px in Arabic and 558 → 829 px on the login — at FCP + 10–95 ms, before `nav.js` marks it (≈ FCP + 400 ms): the row re-distributes when the faces swap in (the wordmark's and Host Grotesk's matched fallbacks match a mean advance, not these strings). The rule for W4-D: hold the letterhead row's parts at their final inline sizes from the first frame (the lock-up's and the menu's boxes reserved, `flex: none` with a set inline size), or tighten the fallback metrics for the strings the row draws — measured with the fonts, paid in `main.css` | — | — |
| **m2** (REVIEW) — «Privacy Policy» and «Cookie Policy» unmarked | `lang="en"` on every standalone policy name: the public footer (W2-C1), the console footer (W3-A; «Privacy Policy» in all four catalogues), the virtual Forum's join form (W3-F2), the Forum's privacy note (W3-F1); the embedded runs («Lire la Privacy Policy», «قراءة Privacy Policy», the consent) read as the document's proper name, written in docs/ACCESSIBILITY.md (the 3.1.2 row, §10.1, G-08 — whose recorded residue, the footer's two titles, is done); §4's A4 answer corrected | `8bd1f1c` | the smoke, 24 views (fr, ar × 1440, 390): every standalone name `lang="en"`, axe 0, overflow 0, CSP 0; the footer test (`tests/i18n/test_ui_translations.py`), the Forum's and the community's tests, the content and service pages, `test_design_docs`: 268 + 242 passed; the console shell's and the RTL browser tests: 58 passed |
| **m3** (REVIEW) — `card.css`'s French colon in every language | **Not changed here; handed to W4-D** (§6): `card.css` is in `main.css`, and a `:lang(fr)` rule (+≈ 20 B) needs a paying deletion in that bundle (V5.8). The gap is already docs/ACCESSIBILITY.md's G-14 | — | — |
| **m4** (REVIEW) — four budget letters recorded as PASS | Written as **accepted exceptions** (no code): the overlay core 6 523 B against §2.6's 4 KB per module; the Arabic console pages with ILE Mono 63 144 B of fonts against 56 KB; the entrance pages' one script request over W1-0's count (the 394 B helpers chunk); the tasks after the first paint read as the rest of the first render (D27's letter) — none with a measured cost (LCP ≤ 1.6 s, INP ≤ 152 ms) — in PERF.md, in DL54-159 and in the release notes' known limits (which also receive W4-C's performance figures and its Chromium-only limit, in the two places the draft kept for them) | this commit | — |
| The sweep's verdict | `A11Y_SWEEP.md`: «no WCAG 2.2 AA failure» holds **after the review fixes**, and says the sweep missed 1.3.5 (its probes do not test it; the review's read of the input purposes on its 396 views found no other form); M1, M2 (with a1) and m2 in its fixed table | this commit | — |

**M2's measure** (the compressed build of `a3613b3`: `collectstatic` 617 files, 1 455 post-processed — the twin's own
figures; `documents.css` served gzip at 5 496 B, `immutable`; profile A + CPU × 4, cold, a fresh context per load,
interleaved, under the lock; `fix/perf/m2.jsonl`):

| Cell | n | LCP median (min–max) | CLS median / max | The review on `5ea1ce2` (n = 5) |
|---|---|---|---|---|
| upload fr 1440 | 9 | 1 048 (996–1 076) | 0.000 / 0.001 | 1 068 · 0.000 |
| upload ar 1440 | 9 | 1 244 (1 220–1 304) | 0.000 / 0.001 | 1 276 · 0.000 |
| upload fr 390 | 9 | 1 040 (964–1 076) | 0.000 / 0.000 | 1 076 · 0.000 |
| upload ar 390 | 9 | 1 228 (1 132–1 268) | 0.000 / 0.000 | 1 224 · 0.000 |
| a piece fr 1440 · ar 1440 | 5 · 5 | 1 136 · 1 308 | 0.000 · 0.000 | — · 1 432 |
| a piece fr 390 · ar 390 | 5 · 5 | 1 032 · 1 308 | 0.000 · 0.000 | 1 176 · — |

Requests unchanged (4 CSS + 9 JS before `load`); the page's JS 24 491 → 24 540 B (the Dépôt's chunk 3 702 → 3 751 B);
no long task after FCP over 116 ms. **Weights** (gzip −9 of the rebuilt bundles): `main.css` 31 799, `console.css`
7 134, `portal.css` 1 045 B — unchanged; `documents.css` 5 494 → **5 496 B** (design-v5: 5 497; the fallback +42 B, its
payment −40 B), so the piece, the loose upload and the gate weigh **45 474 B** against their 45 475 B ceiling and the
documents' registers with their panels 47 534 B against 47 535 B. No ceiling moves.

**Tests** (targeted, V5.5; `test_ile_v5_l4`, one pytest at a time): M1 — 211 passed; M2 — non-browser
`test_depot_w3_c`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_documents_w3_c`,
`test_static_pipeline`, `test_design_docs`: 122 passed; browser `test_depot_browser_w3_c` 14 passed (the four new ones
red without the fix), `test_drawer_browser_w3_c` + `test_documents_browser_w3_c` 45 passed; m2 — 268 + 242 passed, the
console shell's and the RTL browser tests 58 passed; after the records, `test_design_docs`, the inventory, the
confidential-material guard and the checker's tests 120 passed. A last round on the final HEAD did not run: the
shared PostgreSQL container (127.0.0.1:5439) stopped accepting connections (connection timeouts, eight probes over
1.5 min; another lane's run waits on it too) — left alone, it is not this lane's to restart. Nothing but these records
changed after the runs above. `ruff check` and `ruff format --check` clean on the changed Python. Every changed
file is LF.

**For the merge step (the steward).** `check_ownership.py w4-c design-v5` at `310971d`: **PASS — 5 inside, 1 slice,
5 generated, 14 delegated** (merge base `fad36e0`). The new delegated paths,
each in its owner's file, to be written into the manifest: `apps/accounts/profile_forms.py` (outside W3-F2's slice:
`SituationForm`'s two widgets), `tests/frontend/test_service_pages_w3_f2.py` (W3-F2), `static/js/src/depot.js`,
`static/js/src/console.js` (§2d's comment, W3-C's slice), `tests/frontend/test_depot_browser_w3_c.py` (W3-C),
`templates/partials/footer.html` (W2-C1), `templates/portal/base_portal.html` (W3-A), `templates/community/join.html`
(W3-F2), `templates/forum/partials/privacy_note.html` (W3-F1), `docs/ACCESSIBILITY.md` (the 3.1.2 row, §10.1, G-08),
`docs/RELEASE_NOTES_v2.0.0.md` (W4-D's: §6's performance and browsers lines); generated: `static/css/dist/documents/
documents.css` and `static/js/dist/**` (rebuild from clean). design-v5 moved on after this branch's base (the sec-f8
merge took the number DL54-156): this area's entry is renumbered at the merge, as §7 says.
