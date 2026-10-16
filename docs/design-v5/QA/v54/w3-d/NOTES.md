# W3-D — The journey «La soglia» — notes

Family W3-D of the V5.4 plan (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 6, §1.18 D16, §1.5, §3.1 item 7),
worked in the owner's delivery mode (V5.5: implement → review once → fix → ship). Branch `v54-w3-d`, worktree
`C:/tmp/ile_wt/v54-w3-d`, from design-v5 at `d40f209` (W3-B merged). Evidence outside every repository:
`C:/tmp/ile_v5_council/evidence/v54/w3-d/` (E/ below).

## Step 1/1 — the passage and the rail (implementer w3-d-impl-1, 11 October 2026)

**Lane.** Lane 6: dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; for the home's passage only, the same server restarted for a few
minutes at `ILE_REFERENCE_DATE=2026-10-01` — gate G3 closed by the flag's own date, no data changed — then back);
pytest on `test_ile_v5_l6`; one pytest and one headless Chromium of mine at a time, with its own profile
(`C:/tmp/ile_v5_council/.profiles/w3-d-impl-1/`) and the browser cache disabled (a module of the first runs came from
the profile's cache: those runs were thrown away and shot again). Signed-in pages through sessions minted with
`Client.force_login` by a scratch script outside the repository — no password used, typed or stored — revoked at the
end. Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a crash.

**Personas** (the lane's clone of the QA data): `qa-doc-person` (`EE167596D4`, draft — step 1), `qa-person`
(`E46E03B461`, oriented — step 2, the conditions not accepted), `seed-person` (`0FEEBAE3A9`, «Phase gérée par un
acteur autorisé» — the file on threshold A), `qa-fresh-person` (no file: no journey, «Ma situation» with no answer),
`qa-company` (the company: no journey on its dashboard; «Ma situation» through its person's rail).

### What was built

- **SELECTION on threshold A** (`portal.services.journey_for`, a presenter change only; DL54-88). A threshold is a
  place: each step now carries its `status` (its glyph, through the registry's `JOURNEY` map), its `state` (done ·
  current · upcoming) and, on the step a threshold opens, that `threshold` — its key, its caption (the site's own
  jurisdiction labels, the same catalogue entries), its state and, when the file stands on it, the file's state in
  its own words. A file in SELECTION is on no step: steps 1–3 behind it, threshold A current, step 4 ahead.
  `cases.presenters.journey_with_dates` follows the presenter's states and dates the threshold — never a step the file
  left (the seed's trail once reached the administrative procedure, then came back). SUSPENDED and CLOSED keep V4's
  first step: where a suspended file stopped and the record a closed one became are read from the trail, not from the
  status (left, below). `journey_for` lives in `apps/portal/services.py`: the plan's slice names
  `apps/cases/services.py` (a path outside the slice, justified below).
- **One rail drawing** — `apps/portal/static/portal/v5/_journey-rail.css` (a console partial, imported by
  `console.css` after the dashboards; DL54-89), for the console's three journey components:
  - `components/journey_rail.html` — the dashboard's «Mon parcours»: ONE list, one DOM. From **56rem of the
    component's own width** (a container query) the level line: «Maroc» at the reading start, «Italie» at the end,
    the seven steps' nodes on one level, each step's glyph and words under its node at the reading start, the two
    thresholds as narrow columns (2rem; the whole column when the file stands on it) with their hairline across the
    line and their captions over the heads of the steps they open, «Vous êtes ici» on the row that is the current
    item's alone. Under 56rem (the phone, the tablet, a narrow column) **the card and its disclosure**: what is true
    now — the current item's glyph and words, «Étape n sur 7» (on a step), «Vous êtes ici» — then the list behind the
    native `<details>` «Où j’en suis», closed, as a spine; `::details-content` lays the list out at the wide width
    and drops the card and the summary; where a browser lacks it, the card and its disclosure stay at every width. The
    case file draws the same component `descriptive`: the spine at every width, every reached step with its date.
  - `components/case_timeline.html` — the case file's timeline on the same spine: every event a filled ink dot, the
    latest the laguna ring on its wash.
  - `components/wizard_stepper.html` — «Ma situation»'s Stepper on the same nodes: answered = the ink dot, the
    question shown = the ring, the others an open ring; the line a hairline (answered in any order, never
    «travelled»); under 64rem a level row of nodes with the line between them (W3-F1's phone row kept, now drawn).
  The vocabulary everywhere: behind the file a 10 px ink dot (never a check, O14), where it stands an 18 px laguna
  ring on a flat wash — a disc behind it, not a shadow (the dashboard's second shadow value is gone: one, the
  NowPanel's) —, ahead a 12 px open ring; the line 2 px, laguna where the file has been, the decorative hairline
  ahead; every item draws the stretch from its node to the next item's (no gradient, no measure, no script; the grid
  mirrors it in Arabic). One marker a column (D16): the phase glyph — no numeral, no holder (A′: `actor` stays empty
  until the actors' mapping D9 is signed), no beads (OJ3: on the dashboard the pieces are «il registro», W3-B's, once).
- **One passage drawing** — `static/css/v5/_journey-passage.css` (a page-only partial) and `components/stepper.html`
  (DL54-90): «la linea», the numerals over open stations, the words under them — down the reading edge on a phone,
  across from 48rem as many columns as stations; a flow (`current`) fills the steps behind in ink and thickens its
  own ring in the primary, with its rank under the passage; 16 px text below 64rem (RE-4). W3-F1 drew «la linea»
  first for the door pages and wrote «the public passage, when W3-D draws it, is the same line»: this partial is
  that drawing's home. **On the home** the orientation's four neutral steps (gate G3 closed) are drawn by it
  (`templates/pages/home/_orientation.html` includes the component; `pages.css` imports the partial, written in the
  collected tree: `../../css/v5/_journey-passage.css`). **The door pages are untouched**: their import lines and the
  consolidation with W3-F1's own «la linea» wait for W3-F1's tag `v54/w3-f1` on design-v5 (below).
- **Still at load.** No animation, no transition, no keyframes, no `will-change` in either partial (tested). V4's
  JourneyRail and Timeline left `v4/workspace.css` with `rail-draw`, `rail-draw-y` and `tl-light`; W3-B's one
  dashboard rule that stopped the line drawing itself left `_dashboard.css`. **«Ma situation»** played six colour
  transitions at load (the submit taking its secondary role from `situation.js` after the first paint): the script
  now applies that role under `transition: none` in one style pass and restores it once painted
  (`static/js/src/situation.js`, taken from W1-D's note «until W3-D's journey work takes the file»).
- **Deleted with their consumers** (plan §2.3, W3-D's row): `components.css` §16 (the V1 stepper and the progress
  bar; the section count 19 → 18), `v4/workspace.css`'s JourneyRail and Timeline (and their forced-colours lines),
  `register.css`'s shore crossing (`.sequence__crossing`, `.sequence__step--italy`), the home's `.home-orientation
  .sequence*` rules in `pages.css`. `v2/voyage.css` was already gone (W2-D). Kept, because pages still draw them:
  `register.css`'s `.sequence` (the Academy's modules, a need's history, the help desk's turns, the selection's
  stages — W3-E's pages) and `components.css` §17 (`.timeline`: the pathway pages, the pilot and the companies' page
  on design-v5 today — W3-F1 moves them to «la linea»).
- **Docs.** `DESIGN_SYSTEM_2026.md`: §10's four entries (journey_rail, case_timeline, stepper, wizard_stepper), a new
  §11.8 «Il viaggio — La soglia», the sentences of §2 / §2.1 / §11.7 / §12 my deletions made untrue; §2's weights
  and section count by `scripts/regen_design_inventory.py --write` (not by hand). DL54-88 … DL54-92 (the steward
  renumbers at the merge).
- **Tests.** `tests/frontend/test_journey_w3_d.py` (29 — the mapping status by status, the threshold's date, the
  list's items and its one current, the glyphs from the registry, no numeral, no check, no holder, the card and its
  disclosure, the timeline, the Stepper's contract with `situation.js`, the pages that draw it, the home's passage,
  the two partials still and on tokens, the imports, «one rail drawing and one passage drawing, never a third», V4's
  drawing gone, no new copy) and `tests/frontend/test_journey_browser_w3_d.py` (10, browser — the level line on one
  level on threshold A, mirrored in Arabic; the phone's card and disclosure opening onto the spine; nothing moving at
  load on the three pages, with and without reduced motion; the case file's spine and its lit event; «Ma
  situation»'s spine and phone row with the line whole from node to node; forced colours). `apps/pages/tests/test_home.py`'s two orientation tests follow
  the markup (`.linea__step`), their intent kept.

### The items handed to W3-D, answered

`grep -n "W3-D" docs/design-v5/QA/v54/*/NOTES.md docs/design-v5/QA/v54/*/SHIPPED.md` on design-v5 at `d40f209`, plus
W3-F1's notes on its branch (not merged yet):

| From | The item | Answer |
|---|---|---|
| W1-C NOTES (seen on the way) | «the wizard's sticky action bar covers the first question at 390 px until the page scrolls (W3-D)» | **W3-F1's**, done on its branch: `v4/wizard.css` retired for `v5/_wizard.css`, the foot part of the page at every width (lands with its merge). Not W3-D's file |
| W1-C NOTES | the stepper's check removed from `components.css` §16 (W3-D's) | **done further**: §16 deleted whole — no page drew `.stepper` once `components/stepper.html` became the passage |
| W1-C NOTES | the wizard's own input (6 px) and question panel (12 px); «the journey family draws the done step when it redraws the journey» | the radii: **W3-F1's** (`_wizard.css`: 4 and 8, on its branch). The done step: **drawn** — on the rail a filled ink dot, on the passage the station filled in ink with its numeral above (`.linea__step--done`); never a check (O14) |
| W1-C NOTES | O3 (the wizard's sticky foot, its 20 px radios), O6 (`role="alert"` on a list in `components/option_cards.html`, `portal/situation.html`) | O3: **W3-F1's** (the foot and the OptionCards are `_wizard.css`'s). O6: neither file is W3-D's — `option_cards.html` is in no family's slice, `situation.html` is W3-E's: **handed to W3-E** (below) |
| W1-D NOTES | `situation.js`: «proposed: W1-D, the motion gate and frame wait, until W3-D's journey work takes the file» | **taken**: one change (the submit's role at load without its transition, DL54-91); proposed manifest slice for W3-D: «the guided form's first frame» |
| W1-D NOTES / SHIPPED (W3-B / W3-D) | the dashboard animates at load: `rail-draw` (900 ms) and `strip-fill` (320 ms) | `rail-draw`, `rail-draw-y` and `tl-light`: **gone** with V4's JourneyRail and Timeline — 0 animations at load on the dashboard, the case file's journey and timeline, «Ma situation» (measured, and tested in the browser with and without reduced motion). `strip-fill` is the HealthStrip's: no longer on the dashboard (W3-B), still on the case file — **handed to W3-C / W3-E** (below) |
| W2-D NOTES | `v2/voyage.css` (W3-D's row of the deletion map) deleted by W2-D with its last consumer | **nothing left**: absent from the tree and from `main.css` |
| W3-A NOTES | «animations at load inside the shell: 0 (the pages' own draw patterns — `rail-draw`, `strip-fill` — are W3-B's and W3-D's)» | `rail-draw`: **gone** (above) |
| W3-B NOTES (the gate table) | two shadow values on the dashboard: the NowPanel's and «the journey node's halo (W3-D's component)» | **one now**: the current node's wash is a disc behind the ring, not a `box-shadow` (tested: no shadow inside the rail) |
| W3-B NOTES / SHIPPED | «the journey rail's redraw (still at load — the dashboard's scoped rule then becomes redundant) and the `SELECTION` mapping (`seed-person`'s advanced file still sits on step 1)» | **both done**: the rail still by itself and W3-B's rule removed from `_dashboard.css`; `seed-person`'s file stands on threshold A (DL54-88) |
| W3-B NOTES (handed over) | «`seed-person`'s file reads «Phase gérée par un acteur autorisé» while the journey says «Vous êtes ici · 1» … and one fixed place for «Vous êtes ici»» | **done**: the file on threshold A, the list's current item; «Vous êtes ici» has one place — the row that is the current item's alone (the level line's fourth row; under the current item's words on the spine; after them in the card) |
| W3-A SHIPPED | the journey's composition complete only when W3-D ships | this family |
| W3-F1 NOTES (its branch) | «W3-D may draw the public passage on these pages: one import line in a page sheet; the pilot's sequence on «la linea» is the same diagram language» | **the passage is «la linea»** (DL54-90); its import lines in the door pages' sheets wait for W3-F1's merge, with the consolidation written below («For W3-F1») |
| W3-F1 NOTES (its branch) | «the Stepper of «Ma situation» stands in `v5/_wizard.css` until the journey family redraws it» | **redrawn** in `_journey-rail.css` §7; `_wizard.css`'s Stepper rules leave at the consolidation (below) |

### For W3-F1 (and the merge step, if W3-F1 merges after this branch is done)

The plan's order is W3-F1, then W3-D. When `v54/w3-f1` is on design-v5, this branch runs `git merge design-v5` and, in
one commit, does what this family could not do before:
1. **«la linea» has one home.** The `.linea` rules of `static/css/v5/_interior.css` §5 (`.linea`, `__step`, `__num`,
   `__label`, `__text`, `--pending`, `--across`) leave for `static/css/v5/_journey-passage.css`, which already holds
   them, written from the same grammar (plus a flow's place, the 16 px text below 64rem — RE-4 — and a ring open
   through to its ground). `_interior.css` keeps its page modifiers (`linea--phases`, `__kicker`, `diploma-steps` …)
   or they move into the page partials that use them.
2. **The import line** `@import url("../css/v5/_journey-passage.css");` in each page sheet that draws «la linea»,
   after `_interior.css`: `pages/css/interior.css`, `pathways/pathways.css`, `ecosystem/ecosystem.css`,
   `orientation/wizard.css` — whichever draw it on the merged tree (a grep for `class="linea` in `templates/`).
3. **One component.** `templates/pages/partials/_linea.html` includes `components/stepper.html` with the same
   arguments (`steps`, `label`, `lang`, `across`, `cols`), or its callers call the component.
4. **`components.css` §17 and `components/timeline.html`** retire: on W3-F1's branch the showcase is their last
   caller (the section count 18 → 17; DS 2026 §10's `timeline.html` entry with it).
5. **The Stepper's rules leave `v5/_wizard.css`** (§2 `.wstep*`, the phone row and the forced-colours `.wstep` lines):
   `_journey-rail.css` §7 draws it, at the guided form's own 64rem break.
6. **A proposal, W3-F1's call:** the questionnaire's progress (`templates/orientation/_step.html`, a progress bar — the
   review's FM12 «the questionnaire's percentage») could be the passage with `current` (`components/stepper.html`:
   numerals over stations, the steps behind filled, its rank in words, no percentage).

### For W3-E · W3-C · the owner

- **W3-E** — `register.css`'s `.sequence` stays for the console's secondary pages that draw it (the Academy's modules
  and an enrolment's, a need's history, the help desk's turns, the selection's stages); an event history can take the
  rail's timeline (`components/case_timeline.html`'s `.tl`) when W3-E redraws them, and the last consumer deletes
  `.sequence`. **O6** (W1-C): `role="alert"` on a list in `components/option_cards.html` and `portal/situation.html`.
  **«Mon parcours»** (`portal/pathways.html`): the rail's `ile-steps` entry leads to the saved pre-assessments, and no
  journey is drawn there — a proposal: «Où j’en suis» (the component, not descriptive) at the page's head (a template
  and a view change, W3-E / W3-A); **done by the fix pass** (the review's M2: «Review fixes»).
- **W3-C / W3-E** — the case file's HealthStrip still plays `strip-fill` at load (`v4/workspace.css`, the HealthStrip's
  last consumers).
- **The owner (B1)** — no word was added: every string on the four components is the catalogue's (tested). Waiting on
  B1: OJ5 («Cette étape ne dépend pas de vous» under a holder — not drawn), OJ6 (short phase words — not drawn), the
  timeline's title and the deadline-distance words (item 4 — untouched).

### The gate (plan §3.5 item 6), measured

Lane 8786; the five personas; fr and ar; 1440 · 1280 · 1024 · 1000 · 900 · 834 · 768 · 390 · 360 (the phone
widths emulated, and said so), plus the opened disclosure, reduced motion and forced colours on the flagship screen:
**100 drawings in the final set** (`E/final/report.json`, `E/final/*.png`) after the working sets (`E/a1` … `E/w1`), all
looked at — the level line, the card, the spine, the thresholds, the mirror, the forced colours.

| Item | Result |
|---|---|
| one passage and one rail drawing, never a third | the rail: `_journey-rail.css` draws `.journey`, `.tl`, `.wstep`; the passage: `_journey-passage.css` draws `.linea` — tested: no other sheet of the product draws the journey's classes, but the four legacy seats that leave with W3-F1's merge (`v4/wizard.css` / `v5/_wizard.css`'s Stepper, `components.css` §17 and the ecosystem's pilot diagram, `_interior.css` §5) — the consolidation is written above |
| the phone journey as a card and a disclosure | at 390 and 360 (and up to a 56rem component: 768–900 px tablets), fr and ar: the card — the current item's glyph and words, «Étape n sur 7», «Vous êtes ici» — and «Où j’en suis» closed, its summary 44 px (`--hit-primary`); opened, the spine (the nodes on one column, in the list's order); closed, the list neither laid out nor exposed to assistive technology (the accessibility tree empty), opened by the keyboard (Enter), its ring 2 px |
| still at load | 0 animations at load in the rail, the timeline and the Stepper on the 100 drawings (the only movement left on the journey's pages is the case file's HealthStrip `strip-fill`, W3-C / W3-E's); a true still under reduced motion (tested in the browser on the three pages); V4's `rail-draw`, `rail-draw-y` and `tl-light` out of the cascade; «Ma situation» 6 → 0 transitions at load |
| the numeral / glyph / holder rule | the rail: one glyph a step, from the registry; no numeral; no holder (A′) — tested on the markup; the passage: the numeral (a CSS counter, decorative) |
| `SELECTION` on threshold A | `seed-person`'s `0FEEBAE3A9`: the list's current item is threshold A — eight items exposed, steps 1–3 travelled, step 4 ahead (the accessibility tree: the threshold's item says the caption, «Phase gérée par un acteur autorisé», «Vous êtes ici»); the case file dates it, step 4 undated though the trail once reached it |
| no task above 12 ms | the journey runs **no task of its own**: no script (no `journey-rail.js`), no animation, no observer — at load or after it. Its style and layout ride in the page's first layout: the dashboard's «Mon parcours» re-laid in place costs **2.6–4.5 ms at 1×, 18.6–33 ms at CPU ×4** at 1440 (two probes: the A/B's median of ten, the trace run's median of eight) (the research's rail: about 2 ms, 16–24 ms at ×4); the case file's journey 2.3–3.0 ms (18 ms at ×4; the research's case file 4–5 ms, 32–42 ms); «Ma situation»'s Stepper 1.4 ms at 1440 and 2.4–2.7 ms at 390 (12 and 18 ms at ×4). The one task the journey causes is the person's own tap on «Où j’en suis» on a phone. *Corrected by the fix pass (the review's m2, the accessibility check's finding 2; «Review fixes» below):* opening it at CPU ×4 makes a **63–153 ms task and an 88–128 ms interaction** (the review: 63–96 ms and 88–128 ms over five runs; the accessibility check: 64–153 ms and 96–128 ms, medians of five per persona), closing it 40–86 ms; **the journey's own share is 23–42 ms at ×4 (≈ 6–10 ms at ×1)** — the list's style and layout, the figure first written here as «4.5 ms at 1×, ≈ 27 ms at ×4» —, the rest the shell's `html:has(.console-drawer[open])`, which recalculates the whole document on every `[open]` toggle (390 elements; 112 without it) — W3-A / W4-B's. Under INP's 200 ms either way; no variant moved the journey's share (no glyph, rows not grids, layout containment: 26–31 ms at ×4). What it replaces: V4's phone list was laid out at every load. Traces at CPU ×4 under the performance lock (`E/perf/perf_trace.json`, 3 loads a case after a warm-up; `E/perf` and the A/B in this file's runs) |
| §3.1 item 7 — the identity carriers | below |

**The screens' identity carriers (§3.1 item 7).** The dashboard: «La soglia» — the two shores, the two thresholds
with their glyphs (`stamp`, the journey's one arch `ile-arch`) and their captions, the line travelled in laguna to
where the file stands — with «il lume» in the rail, «I cerchi» and «il registro» (W3-B's). The case file: the same
journey as a dated spine, and the timeline on the same nodes, its latest event lit. «Ma situation»: the Stepper on the
rail's nodes and line. The swap test: with the logo off, the level line between «Maroc» and «Italie» crossed by a stamp
and an arch says this product and no other; the silhouette is not a stepper of numbered circles and ticks.

**Accessibility** (`E/a11y/a11y.json`): axe (WCAG 2.0 / 2.1 / 2.2 A and AA) on the journey's regions — the dashboard
at 1440 (fr, ar) and 390 (fr, ar), the case file at 1440 and 390, «Ma situation» at 1440 and 390: **0 violations**.
The accessibility tree at the wide width: the list «Où j’en suis» exposed though its `<details>` is closed (laid out by
`::details-content`), its items as listed above, the hidden threshold's caption said in the step it opens. Contrast,
by the tokens: the labels 6.46 : 1 (behind) and 5.48 : 1 (ahead), «Vous êtes ici» laguna-700 on laguna-50 above
4.5 : 1, the nodes' edges 3.37 : 1 and more; the untravelled line and the threshold's hairline stay decorative, as the
research and the foundation have them (the nodes, the glyphs and the words carry the information). Forced colours:
the lines in `GrayText` / `CanvasText`, the nodes in `CanvasText`, the current ring in `Highlight`, the wash dropped
(captured, and tested).

### The weight

`gzip -9` of the committed bundles against design-v5 at `d40f209` (rebuilt here; the steward rebuilds from clean at
the merge):

| Bundle | design-v5 | w3-d | Δ |
|---|---|---|---|
| `dist/main.css` (every page) | 41 826 | 40 571 | **−1 255** |
| `dist/portal/console.css` | 7 084 | 8 968 | +1 884 |
| `dist/portal/portal.css` | 1 986 | 1 986 | 0 |
| `dist/pages/css/pages.css` (the home; the institutional pages until W3-F1) | 4 093 | 4 507 | +414 |
| `dist/situation.js` | 1 150 | 1 219 | +69 |

Page types: **every public page −1 255 B**; the home 56 496 → 55 655 B (−841); **the console page types 50 896 →
51 525 B (+629) — 598 B over the ceiling recorded at the w3-b merge (50 927 B, DL54-87)**, which spent §2.6 item 5's
once-only raise. The family deleted every legacy rule its components supersede that no page still draws (§2.3);
the rest is the drawing itself (the rail partial is 2.7 KB gzip alone, against the research's 5.7 KB; the passage 1.0 KB). **What brings
it back under:** the consolidation after W3-F1's merge — `v5/_wizard.css`'s Stepper rules out of the console entry and
`components.css` §17 out of `main.css` (estimated −0.8 KB on the console page types, to be measured then) — and
W3-C / W3-E's planned deletions (624 B + 866 B, W3-B's notes). For the merge step to record, under V5.5's performance
rule (no real regression: the journey adds 2.6 ms of style and layout at 1× to the dashboard's first layout and no
task; the phone's load is lighter by the list it no longer lays out).

### Tests run (targeted, V5.5 — not the full suite)

One pytest and one browser of mine at a time, on `test_ile_v5_l6`; no run ended on a crash.

| Run | Result |
|---|---|
| `apps/cases`, `apps/portal` (non-browser), `tests/test_phase_console.py`, `tests/security/test_authorization_audit.py`, `tests/security/test_object_permissions.py`, `apps/orientation`, `apps/pages/tests/test_home.py`, `tests/frontend/test_design_docs.py`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline` (a real `collectstatic` under the manifest storage), `test_journey_w3_d`, `test_dashboard_w3_b`, `test_o14_lint`, `test_icons`, `test_console_shell_w3_a`, `test_design_showcase`, `test_chips_cards_w1_c`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py` (`-m "not browser"`) | **924 passed**, 3 skipped (the intake's rule-dependent cases), 1 xfailed (the showcase's captions, an older marker), **1 failed → fixed**: `test_design_showcase`'s marker for the stepper (`stepper__item`) follows the passage's markup (`linea__step`); then the showcase, the bundles, the journey and the design docs: 85 passed |
| browser: `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`, `tests/frontend/test_dashboard_browser_w3_b.py`, `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`, `apps/pages/tests/test_browser.py` | **150 passed**, 0 skipped |
| browser: `tests/frontend/test_journey_browser_w3_d.py` (after the last CSS change, with the line-continuity checks) | **10 passed**, 0 skipped |
| `scripts/regen_design_inventory.py` (check) · `scripts/check_ownership.py w3-d design-v5` | current · 9 inside, 8 slice, 18 generated, **7 outside** (DL54-92: each justified for the manifest — `apps/portal/services.py`, `apps/cases/presenters.py`, `apps/core/dev.py`, `static/js/src/situation.js`, `templates/pages/home/_orientation.html`, `apps/pages/tests/test_home.py`, `tests/frontend/test_design_showcase.py`) |

The journey's own tests: `test_journey_w3_d.py` (non-browser) and `test_journey_browser_w3_d.py` (browser).

### Not done, and why

- **The door pages** (W3-F1's, in progress): not touched, by the plan's order — the passage's import lines in their
  sheets and the one-home consolidation of «la linea» wait for `v54/w3-f1` on design-v5 (written above, «For
  W3-F1»). `v54/w3-f1` was not on design-v5 when this step ended (W3-F1 was in its review: SHIP_AFTER_FIXES).
- **SUSPENDED and CLOSED** (*fixed by the fix pass*: no current item, «Vous êtes ici» nowhere, the case file dates what
  the trail reached — «Review fixes», DL54-93; the held node still waits for §7.3) keep V4's first step (DL54-88): where a suspended file stopped and the record a closed one
  became need the trail read into the journey (a held node, a record with no current) — the research's §7.3, beyond
  the gate's threshold A.
- **«Le relais»** (the light from where the file was last seen): not built — it needs a stored last-seen position,
  a policy (class C, plan §7.2); so no `journey-rail.js`. **The holder** of each stretch (A) waits for D9; **the
  beads** (OJ3) are «il registro» on the dashboard.
- **«Mon parcours»** (`portal/pathways.html`) draws no journey (a proposal to W3-E above) — *drawn by the fix pass*.
- **The console page types' CSS** (*fixed by the fix pass*: 49 614 B, 1 313 B under design-v5's ceiling — the rail in a
  page-only sheet, «Review fixes») stands 598 B over its ceiling until the consolidation and W3-C / W3-E's deletions
  (above, «The weight»).
- **Not run:** Firefox and WebKit (the `::details-content` fallback — the card and its disclosure at every width —
  was written, not exercised); a screen reader (the accessibility tree is Chromium's); a real phone; the performance
  PASS on the compressed twin 8782 (the traces ran on the lane's dev server at CPU ×4, under the lock); a person
  watching the pages (nothing moves: there is no motion to judge).

### The lane, cleaned

The five minted sessions revoked on `ile_v5_l6` (`sessions.py revoke`); the lane server on 8786 stopped; the
performance lock released by the script that held it (`C:/tmp/ile_locks/` empty); scratch scripts and evidence
outside every repository (`C:/tmp/ile_v5_council/.work/w3-d/w3-d-impl-1/`, `E/`).

## Review fixes (implementer w3-d-fix, 12 October 2026)

The fix pass after the senior review (`REVIEW.md`, SHIP_AFTER_FIXES: four majors, six minors) and the accessibility +
performance check (`A11Y_PERF.md`, SHIP_AFTER_FIXES: one blocking, two minors in W3-D's files), in the owner's delivery
mode (V5.5) under V5.8's hard CSS ceilings. Branch `v54-w3-d` from `be2fb31`.

**Lane.** Lane 6: dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`, no preview flag); pytest on `test_ile_v5_l6`; one pytest and one headless Chromium of mine at a time,
its own profile (`C:/tmp/ile_v5_council/.profiles/w3-d-fix/`), the cache disabled; sessions for `seed-person`,
`qa-person`, `qa-fresh-person` and `qa-doc-person` minted with `Client.force_login` by a scratch script outside the
repository (no password used, typed or stored), revoked at the end. Never 8780, 8782, Chrome 9222 / 9223; the benchmark
lock was absent at every series and build. **No browser run crashed.** The statuses the lane's data lacks
(SUSPENDED, CLOSED, a file at the last step) were drawn by the real presenter and the real component, spliced into the
real case file and dashboard pages in the browser only (a route on the same origin; no data changed). **36 probe
loads: 0 horizontal overflow, 0 console errors, 0 CSP reports, 0 responses ≥ 400** (`E/fix/report-*.json`, 37
captures; `report-states-unspliced-probe-bug.json` is a first run whose splice missed — the probe's bug, kept and
named, not evidence).

### What was fixed

| Item | The fix | Seen on the lane / tested |
|---|---|---|
| **M1** · A11Y blocking — the shared console CSS over its hard ceiling | `v5/_journey-rail.css` leaves `console.css` for a page-only entry, `apps/portal/static/portal/journey.css` → `css/dist/portal/journey.css` (an import list, like the console's entry), linked after the shell's two sheets with `{% block extra_head %}{{ block.super }}<link …>{% endblock %}` — the place in the cascade the rail held as `console.css`'s last import — by the dashboard and «Mon parcours» (only when the person has a file), the case file and «Ma situation» | **the console page types 51 530 → 49 614 B, 1 313 B under design-v5's 50 927** (below); `journey.css` on the four pages, absent from «Communications», «Mes documents» and the dashboard of a person without a file; the browser tests and the dashboard's, the portal's and the RTL browser tests pass with the new order |
| **M2** · «Mon parcours» draws no journey | `templates/portal/pathways.html` draws `components/journey_rail.html` at the page's head — `journey_for(active_case(user))` from `portal.services.pathways_page`, the dashboard's label «Où j’en suis», no new copy — the pre-assessments under it (`.journey-page`, 32 px); no file, no journey and no sheet | the level line at 1440 and the card at 390, fr and ar, the file on threshold A (`E/fix/parcours-*.png`); `qa-fresh-person`: the pre-assessments alone; tested in the page and the browser |
| **M3** · a suspended or closed file told «Vous êtes ici» on step 1 | a status with no place on the line has **no current item**: `journey_for` marks nothing current, nothing says «Vous êtes ici» (the header's chip says the state), and the card's «Vous êtes ici» belongs to the current item's branch — a list with none says it nowhere; the case file reads the trail (`journey_with_dates`): the last place the file held on the line, from its transitions in order, puts every step up to there behind it, dated where the trail knows the date, the item there marked `stop` (no travelled line past it); `portal.services.journey_place` names a status's place (DL54-88's «V4's first step» superseded: DL54-93) | spliced: SUSPENDED on threshold A — three steps dated, the line travelled to the threshold and no further; CLOSED at the administrative procedure — four steps dated, the line to step 4; fr / ar, 1440 / 390; 0 «Vous êtes ici», 0 `aria-current` (`E/fix/states-*.png`); one test per status in the presenter, the component and the page, the stop on a threshold, a resumed then closed file |
| **m1** · the timeline hides its «now» | newest first (`cases.presenters.timeline`: the latest `limit` events, `-created_at, -id`), the first row lit (`tl__row--last` → `tl__row--latest`); the actor line skipped when it repeats the detail | `seed-person`'s case file at 1440: the lit event the first row, 69 px into the inspector's 756 px (it ended ≈ 440 px below the scroller's end); «Intervenant assigné» says «Acteur autorisé» once (0 repeats, five rows); tested |
| **m3** · the shores drawn differently in the two densities | the level line's last stretch runs from step 7 to the rail's far end, under «Italie», as the spine carries it to its last row; «Vous êtes ici» under node 7 too (the push to the far end removed: at 56rem a column is 108 px, the pill 94 px in French, 69 in Arabic) | the line's end and «Italie»'s end on the rail's end (0 px), fr and ar, 1440 and 1024; spliced at step 7: the pill under its node, 24–83 px inside the rail; tested in the browser. The pill keeps its row of its own (the drawing's one place for it, W3-B's ask): it still stands under the tallest label |
| **m5** · on a threshold the card names the phase, not where it sits | the threshold's caption («Autorités compétentes : décisions administratives», the spine's own catalogue string) heads the card | fr and ar at 390 (`E/fix/dash-seed-*-390.png`); tested |
| **m6** · the wide density on one browser behaviour | the second condition: `::details-content` gets `display: block` with `content-visibility: visible`, so that a browser that knows the selector and hides a closed details through the slot's `display` shows the list too; Chromium computes `block / visible` (unchanged layout) | **not run in Safari 18.4+ or Firefox** — neither is installed here, and installing one is a new download: to check before the owner's report (the card and its disclosure remain the fallback where the selector is unknown) |
| A11Y 3 · the Stepper's line takes the pointer | `pointer-events: none` on `.journey > li::before, .tl__row::before, .wstep__item::before` | a point on the line just past each node lands on its question's link: 7 / 7 at 1440 and 390, fr and ar (it landed on the `li`); tested in the browser |
| m2 · A11Y 2 · the disclosure's tap | the notes' figure corrected in place (the gate table above): a 63–153 ms task and an 88–128 ms interaction at ×4, the journey's own share 23–42 ms (≈ 6–10 ms at ×1), the rest the shell's `html:has()` | nothing changed in W3-D's files (the accessibility check: «nothing needs to change»); the confirmation on 8782 is the integration checkpoint's (this role does not use the twin) |

### The shared payload, before → after (V5.8)

`gzip -9` (mtime 0) of the committed bundles; design-v5 at `1c03e3b` (the same CSS as the merge base `d40f209`):

| Bundle | design-v5 | before the fix (`b9907ab`) | after (`HEAD`) |
|---|---|---|---|
| `dist/main.css` (every page) | 41 880 | 40 599 | 40 599 |
| `dist/portal/console.css` | 7 072 | 8 956 | **7 040** |
| `dist/portal/portal.css` | 1 975 | 1 975 | 1 975 |
| `dist/portal/journey.css` (the four journey pages only) | — | — | 2 688 |
| `dist/pages/css/pages.css` (the home) | 4 083 | 4 497 | 4 497 |

| Page type | design-v5 | before | after | Ceiling |
|---|---|---|---|---|
| **console pages (main + console + portal)** | 50 927 | 51 530 | **49 614** | 50 927 — **1 313 under** |
| a journey page (+ `journey.css`) | — | — | 52 302 | «plus a page's own sheet» (DL54-87), as documents, companies, the Academy and the help desk load theirs |
| a public interior page (main) | 41 880 | 40 599 | 40 599 | 42 531 |
| the home (main + pages + hero) | 56 531 | 55 664 | 55 664 | 57 191 |

Requests: one stylesheet more on the four journey pages only (4 CSS + 7 JS on the dashboard and the case file, 4 + 8
on «Ma situation», against W1-0's «before» 3 + 8 and 3 + 9), none elsewhere; JS unchanged.

### Not done, and why

- **M4 · the consolidation with W3-F1.** `v54/w3-f1` is not on design-v5 (no tag; design-v5 at `1c03e3b`; W3-F1's
  branch at `b8def65`, after its own fix pass). The plan's order (W3-F1 merges, then W3-D) and the review's fix make it
  the first step after W3-F1's merge: `git merge design-v5`, then in one commit the five steps of «For W3-F1» above —
  one home for «la linea» in `_journey-passage.css`, the import lines in the door pages' sheets, `_linea.html` calling
  `components/stepper.html`, `components.css` §17 and `timeline.html` retired, `_wizard.css`'s Stepper rules out —, the
  door pages and «Ma situation» re-shot (fr / ar, 1440 / 390) and the shared payload re-measured. `register.css`'s
  `.sequence` stays W3-E's.
- **m4 · «Ma situation» counts three ways** — W3-E's view and template (handed over below).
- **m6 · Safari and Firefox** — not installed (above).
- **A file off the line, read without sight**: its steps behind are told by their dates (no item carries
  `aria-current`); an undated step behind it (a step the file skipped) reads like the others — the held node, and any
  words for it, wait for the trail contract (JS §7.3) and B1.

### Handed over

- **W3-E** — m4: one total for the person — the counter under the Stepper says «0 question(s) renseignée(s) sur 7»
  (`total = len(PROFILE_FIELDS)`, without the recognition question) while the Stepper draws 8 and the foot says «1 / 8».
  The accessibility check's O1: the inspector `aside.file-grid__inspector` scrolls inside itself from 80rem with nothing
  focusable in it (`tabindex="0"` on the labelled aside, or no inner scroll) — the newest-first timeline now puts the
  latest event in view, the focusability stays the inspector's. «Mon parcours»'s header lead («Les pré-évaluations
  d’orientation enregistrées dans votre compte.») now heads the journey too: new words would be B1's.
- **W3-A / W4-B** — O2: under forced colours the current entry of the rail and of the phone bar draws the same outline as
  the focus ring (WCAG 2.4.7); another current marker (a `border-inline-start` in Highlight). O3:
  `html:has(.console-drawer[open])` recalculates the whole document on every `[open]` toggle — a class set by the
  drawer's own script.
- **The merge step** — the paths outside the slice: DL54-92's seven and DL54-93's — `templates/portal/dashboard.html`
  (W3-B's, the sheet's link), `templates/cases/detail.html`, `templates/portal/situation.html` (W3-E's, the link),
  `templates/portal/pathways.html` (W3-E's, the link and the journey at the head); `apps/portal/static/portal/journey.css`
  is the journey's entry (the slice names its partial and an import line: a W3-D whole file); `pathways_page`'s
  `journey` joins W3-D's `journey_for` in `apps/portal/services.py`. The shared payload is 1 313 B under the ceiling.

### Tests run (targeted, V5.5)

| Run | Result |
|---|---|
| `apps/cases`, `apps/portal`, `tests/test_phase_console.py`, `tests/security/test_authorization_audit.py`, `tests/security/test_object_permissions.py`, `apps/pages/tests/test_home.py`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline` (a real `collectstatic`), `test_journey_w3_d`, `test_dashboard_w3_b`, `test_o14_lint`, `test_icons`, `test_console_shell_w3_a`, `test_console_shell_stylesheets`, `test_design_showcase`, `test_chips_cards_w1_c`, `test_state_chips_carry_a_register`, `tests/i18n/test_rtl_static.py`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py` (`-m "not browser"`) | **999 passed**, 3 skipped (the intake's rule-dependent cases), 1 xfailed (the showcase's captions, an older marker) |
| after the last CSS change and the docs: `test_design_docs`, `test_css_bundle_is_current`, `test_journey_w3_d`, `test_console_shell_stylesheets`, `test_regen_design_inventory` | **91 passed** |
| browser: `tests/frontend/test_journey_browser_w3_d.py` (the level line's last stretch, the timeline's first row, the Stepper's line under the pointer, «Mon parcours» at 1440 and 390 added) | **12 passed** |
| browser: `test_dashboard_browser_w3_b.py`, `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py` | **58 passed** |
| `scripts/regen_design_inventory.py` (check) · `scripts/check_ownership.py w3-d design-v5` | current · 11 inside, 9 slice, 19 generated, **11 outside** — each justified (DL54-92, DL54-93) |

The journey's own tests: `test_journey_w3_d.py` 38 (29 → 38: one test per off-line status in the presenter, the
component and the case file page, the stop on a threshold, the timeline's order, «Mon parcours» with and without a
file, the page-only sheet, the pointer) and `test_journey_browser_w3_d.py` 12.

### The lane, cleaned

The four minted sessions revoked on `ile_v5_l6`; the lane server on 8786 stopped; no browser of mine left running; the
benchmark lock never created; scratch scripts and evidence outside every repository
(`C:/tmp/ile_v5_council/.work/w3-d/w3-d-fix/`, `E/fix/`).

## Steward — the merge waited for W3-F1 and did not start (12 October 2026, 01:30–05:30)

The steward (label `w3-d-merge`). **Nothing was merged**: design-v5, v5-live and 8780 untouched, no `v54/w3-d` tag, no
`live_status.json` change, the merge lock never taken, no lane server, browser or session used. The plan's order (§3.5
item 6: W3-D merges after W3-F1) needs `v54/w3-f1` on design-v5; it did not appear in the four hours the role waits
(checked every 60 s from 01:30:13 to 05:30:51). Meanwhile W3-F1's first merge stopped at the shared-CSS gate (its
NOTES «Steward», 02:10) and its budget and consolidation pass committed 03:30–05:09 (`7cdaba8` … `cfe0167`); the lock
went to W2-A's merge (00:39–01:50), W3-F2's (01:50–02:44), a cherry-pick of main's gate-3 fix (02:44–02:59), then
W2-C2's (from 04:11, still held at 05:30).

**What the next attempt does — prepared** in `C:/tmp/ile_v5_council/.work/w3-d/w3-d-merge/` (scratch, outside the
repository; each script checks every anchor before it writes and refuses on a mismatch):
- **The consolidation (the review's M4) is part of the merge**, and the orchestrator's definitive ruling of 12 October
  02:15 (V5.8, rule 3: the family that merges second consolidates a duplicated component family before its merge)
  makes it a condition of the merge. Without it «Ma situation» draws two Steppers at once: W3-F1's `v5/_wizard.css`
  box on `.wstep__node` (its (0,3,0) inset shadow, its phone `::before { display: none }`) under `portal/journey.css`.
  `m4_apply.py` does «For W3-F1» items 1–5 in one pass — `_interior.css` §5 with its Arabic and forced-colours lines
  into `_journey-passage.css`; the passage's import line after `_interior.css` in `pathways.css`, `ecosystem.css` and
  `orientation/wizard.css`; `_linea.html` an include of `components/stepper.html` `with current=None` (a caller's
  `current` never makes an explanation a progress); `components.css` §17, `timeline.html` and the showcase's demo
  retired; `_wizard.css`'s Stepper rules out — and `m4_tests.py` the tests that follow (this family's «never a third»
  narrowed to the two partials plus the page modifiers, which qualify the drawing and never redraw it; W3-F1's two
  import-list tests receive the line they were written for). Anchors checked against W3-F1 at `76429f2`; its budget
  pass puts `_pagina.css` first in those page sheets, so the header anchors are re-checked on the merged tree.
- **The decision log**: `dl_merge.py` — this family's changes to it are additive only (six rows, six entries),
  renumbered after design-v5's last entry with their cross-references; the notes keep the numbers they were written
  with.
- **The gate under the ruling**: rule 1, `main.css` and main + console + portal no heavier than design-v5's at the merge
  (`weigh.py`, the figures of `.work/w2-a/w2-a-merge/weigh_pages.py`); rule 2, the four journey pages get their first
  page-only sheet (`portal/journey.css`, 2 688 B), so their total is recorded as measured after a performance sanity
  check on the lane's compressed twin — `twin_ctl.py` and `perf_twin.py` (BASE design-v5, HEAD the merged branch;
  W1-0's `measure()`, profile A, CPU ×4, interleaved blocks). `A11Y_PERF.md` preceded the fix pass that made the sheet.
- **The re-shoot M4 asks** (the pages that draw «la linea» and «Ma situation», fr / ar, 1440 / 390, before / after):
  `shoot_m4.py`, `compare_m4.py`. **Ownership**: `ownership.py` (DL54-92's and DL54-93's eleven paths and M4's seven,
  three slices named as written).
- This worktree's `.env` now matches design-v5's (`ILE_CONFIDENTIAL_SENTINELS`, read by `tests/security` after the sync).

## Integration pass (implementer w3-d-fix, 12 October 2026)

The orchestrator's integration task of 12 October: wait for `v54/w3-f1`, merge design-v5, then — under the
DEFINITIVE CSS RULING (the last section of `directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`) — one passage drawing
for the home and the door pages, and the shared console payload paid for. The review's and the accessibility check's
findings stand fixed as «Review fixes» records (not redone); this pass closes the review's M4, the one major that
waited for W3-F1's merge. Decision log: **DL54-128** (written DL54-116 at the first sync, DL54-127 at the second).
Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-d/integration/`
(E/ below); scripts: `C:/tmp/ile_v5_council/.work/w3-d/w3-d-fix/` (each edit anchored on exact text, every anchor
checked before anything is written).

**Lane.** Lane 6 as before: the dev server on 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`
— `2026-10-01` for the home's passage only, gate G3 closed by the flag's own date, no data changed —,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); pytest on `test_ile_v5_l6`; one pytest and one headless Chromium
of mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-d-fix/`), the cache off; sessions for
`seed-person`, `qa-person`, `qa-fresh-person` and `qa-doc-person` minted with `Client.force_login` (no password used,
typed or stored), revoked at the end. Never 8780, 8782, Chrome 9222 / 9223. The benchmark lock was absent at every
series and build. **No browser run crashed.**

**The wait, and a rehearsal.** `v54/w3-f1` was checked every 2 minutes from 05:35; it appeared at 07:01 (design-v5
`a2644b0`, the W3-F1 steward's merge). Meanwhile the whole pass was rehearsed in a scratch worktree (detached, never a
branch; removed at the end) on the W3-F1 steward's trial sync `993bae3`: the resolution, the consolidation, the
captures, the tests (there: 1 312 non-browser and 113 browser tests passed; the failures seen there were the run's own
mid-run edits, two trial-only reds and the motion gate's red, which design-v5 has too — below). On the real tree the merged pages were
pixel-identical to the rehearsal's (64 public, 84 console and 8 home captures), and the scripts ran unchanged.

**The merge** (`b379eec`): design-v5 at `v54/w3-f1`, 174 commits (W2-A's overlay system, W3-F2's content, legal,
error and account pages, W2-C2's phone sheet and the targa's popover, W3-F1's doors, project pages and orientation,
their stewards' merges). Conflicts, both areas kept: `pages.css`'s header (the institutional pages left it — W3-F1;
the passage's partial imported first — W3-D); DS 2026 — §2's generated rows design-v5's, then
`scripts/regen_design_inventory.py --write`, with this family's one prose change (the JourneyRail left
`v4/workspace.css`), §2.1's `pages.css` row (design-v5's, with the passage's sentence), the console rows (design-v5's
`console.css` row, this family's `journey.css` row, W2-A's `overlay-panels.css` row), §10's `wizard_stepper.html`
(the rail's); the decision log (design-v5's numbering, this family's six entries after it); `static/css/dist` and
`static/js/dist` deleted and rebuilt (`npm run build`). `manage.py check`: no issue.

**The second sync** (`69cdbe8`). design-v5 moved after the tag: W3-C's merge (the documents — «Mes pièces», the
preview drawer, F13 —, its steward's record DL54-110 … DL54-120 and shipped note; design-v5 `4ff9056`). This branch
merged it again before asking for its own merge. Conflicts, both areas kept: `v4/workspace.css` (this family's
JourneyRail and Timeline out, W3-C's DocumentCollection / Row / Card, SegmentedControl and search out — this family's
hunks applied on design-v5's file by exact text, the header naming both), the decision log (below), DS 2026 (§2's rows
design-v5's, regenerated; W3-C's «Mes pièces» keeps §11.8 and the journey «La soglia» becomes **§11.9**, this family's
references following — W3-C's one reference to its own §11.8 untouched); the bundles rebuilt from a clean dist.
`manage.py check`: no issue. The other files both families changed merged cleanly (`apps/portal/services.py`: W3-C's
`present_deadline`, this family's `pathways_page`; `register.css`; the showcase).

**How to read the decision-log numbers written before this pass:** the table in «Integration pass — resumed» below
(design-v5 ended at DL54-109 at the tag; W3-C's merge took DL54-110 … DL54-120 and the devops merge DL54-121, so this
family's seven entries are now **DL54-122 … DL54-128**). DS 2026's journey section, «§11.8» in this file's earlier
sections, is §11.9.

### One passage drawing (the review's M4; the ruling's rule 3: the family that merges second consolidates)

| Item | The change | Seen on the lane / proved |
|---|---|---|
| «la linea» has one home | W3-F1's rules (`static/css/v5/_interior.css` §5, its Arabic line in §7, its forced colours) fold into `static/css/v5/_journey-passage.css`, which already drew the same grammar; `_interior.css` §5 is a pointer. Where the two hands differed the door pages decide: W3-F1's Arabic rule for a French station is homed; the passage's «16 px below 64rem» line (RE-4) is dropped — the home's four stations carry no text, so it never applied there, and the door pages keep W3-F1's 15 px station text; the ring stays open to its ground (no `--surface-page` fill: on the home the stations sit on the BRAND gradient) | the home, the Forum and the institutional pages pixel-identical; the door pages identical but for their rings' rims (below) |
| the import line | `@import url("../css/v5/_journey-passage.css");` after `_interior.css` in `pathways/pathways.css`, `ecosystem/ecosystem.css` and `orientation/wizard.css` (the pages that draw «la linea»: a grep of `class="linea` and `_linea.html` in `templates/`); the Forum's and the institutional pages' sheets shed the drawing (Forum 3 494 → 3 021 B, institutional 2 797 → 2 266 B gzip) | W3-F1's import-list tests receive the line they were written for |
| one component | `templates/pages/partials/_linea.html` includes `components/stepper.html` `with current=None` — W3-F1's callers (`ecosystem/companies.html`, `ecosystem/partials/pilot_flow.html`, `pathways/detail.html`) and contract kept; an explanation never becomes a progress. The pages that write the markup by hand with their modifiers (`pathways/index.html`, `index_interim.html`, `diplomas.html`, `training.html`, `orientation/start.html`) keep it; their modifiers (`_pathways.css`, `_spaces.css`, `orientation/wizard.css`) qualify the drawing, never redraw it (tested) | the markup identical (the pages render the same `<ol class="linea">`) |
| before → after | `shoot.py` + `compare.py`: 156 captures — the door pages (`/projet-pilote/`, `/entreprises/`, `/parcours/salaried_work/`, `/parcours/`, `/diplomes-et-titres/`, `/formation/`, `/orientation/`), `/forum/`, `/le-projet/`, the home's orientation chapter, the console's journey pages and «Ma situation»; fr and ar, 1440 and 390, forced colours at 1440 for the console pages; the noise floor measured in the rehearsal (two identical runs: 64 / 64 and 56 / 56 captures identical) | **128 identical; 28 changed — all the door pages' rings' rims** (40–124 pixels a page, at most 4 / 255 a channel, 0 pixels above 24: the border's antialias over the page ground instead of over the ring's own paper fill; `E/int-after/zoom-ring-sheet-fr-1440.png` at 16×); the home 8 / 8, the Forum, the institutional pages and every console page identical (`E/int-after/compare-summary.txt`) |
| retired, with their proof | `components.css` §17 (the V1 timeline; 11 → 10 sections) and `components/timeline.html`, with the design showcase's demo and `DEMO_TIMELINE`; the Stepper's rules of `apps/portal/static/portal/v5/_wizard.css` (§2 but the count, the phone row, the forced-colours line — the rail draws the Stepper); DS 2026 §10.1's «Avanzamento» row (`progress.progress`, gone with §16 in this family's first step) | `proof.py` (`E/proof/proof-before.txt`): every template, Python, JS and JSON file of design-v5 at `a2644b0`, of this tree, and of the files each in-flight worktree changed against its merge base (`v54-w3-c` and its trial worktree, `v54-devops`; `v54-w3-e` absent) — the timeline's last caller is the showcase's demo; the Stepper is drawn only where `portal/situation.css` is linked; W3-C's change to the showcase touches neither (its head links and its documents sample). Again after the second sync (`E/proof/proof-after-resync.txt`: design-v5 at `1a61a7c`, with W3-C and devops; in flight `v54-w3-e`, `v54-intfix`): no new user |

### The shared payload paid for (rules 1 and 2)

- **«Ma situation»'s guided form leaves the shared bundle.** W3-F1's merge had put `v5/_wizard.css` in `console.css`, on
  every console page. It is that page's alone: it moves to a page-only sheet, `apps/portal/static/portal/situation.css`
  → `css/dist/portal/situation.css`, which only `templates/portal/situation.html` links, after the shell's two sheets —
  the place in the cascade it held as `console.css`'s last import.
- **Each journey page loads only what it draws.** With the form out, «Ma situation» would have loaded two page sheets,
  one of them the whole rail (the level line, the card, the timeline) for its Stepper. The console's one rail drawing is
  now a vocabulary and two components, three partials of one drawing: `v5/_journey-nodes.css` (one line, three nodes,
  written once), `v5/_journey-rail.css` (the journey and the timeline) and `v5/_journey-stepper.css` (the Stepper).
  `portal/journey.css` = nodes + rail (the dashboard, «Mon parcours», the case file); `portal/situation.css` = the form +
  nodes + Stepper. The cascade inside each page is the one it had; each forced-colour rule kept its selector's
  specificity. Seen on the lane: every console page identical before and after, normal and forced (84 captures).
- **The token check follows the composition.** `tests/frontend/test_design_docs.py` reads, for a partial, the custom
  properties of the partials its entry imports before it (sibling imports only), as the build composes them: the
  rail and the Stepper read `--node`, `--nc`, `--node-y`, `--rail-ground` from the vocabulary.

gzip −9 (mtime 0) of bundles rebuilt from a clean dist — `.work/w2-a/w2-a-merge/weigh_pages.py`'s figures and
`weigh_all.py`'s for the page sheets (`E/weigh_pages.txt`, `E/weigh_all.txt`):

| Page type | design-v5 `a2644b0` | the merge `b379eec` | **after** | after − design-v5 |
|---|---|---|---|---|
| `main.css` — every page (SHARED) | 38 683 | 37 355 | **37 030** | **−1 653** |
| the console page types: main + console + portal (SHARED) | 48 556 | 47 198 | **45 740** | **−2 816** |
| a journey page — the dashboard, «Mon parcours», the case file (+ `journey.css`) | 48 556 | 49 886 | **48 161** | −395 |
| «Ma situation» (+ `situation.css`: its form and its Stepper) | 48 556 | 49 886 | **47 942** | −614 |
| «Mes pièces» (+ documents) · the company's dashboard (+ companies) | 49 728 · 49 429 | 48 370 · 48 071 | 46 912 · 46 613 | −2 816 |
| the help desk (+ helpdesk) · the selection (+ selection) | 49 431 · 49 641 | 48 073 · 48 283 | 46 615 · 46 825 | −2 816 |
| the login (+ entrance) | 43 544 | 42 216 | 41 891 | −1 653 |
| the home (+ hero + pages) | 52 621 | 51 713 | 51 391 | −1 230 |
| the persons pages (+ pathways) · the ecosystem doors (+ ecosystem) | 42 177 · 42 018 | 40 849 · 40 690 | 40 615 · 40 457 | −1 562 · −1 561 |
| the Forum (+ forum) · the institutional pages (+ interior) | 42 177 · 41 480 | 40 849 · 40 152 | 40 051 · 39 296 | −2 126 · −2 184 |
| orientation (+ orientation/wizard) | 42 722 | 41 394 | 41 144 | −1 578 |
| the content · account · error pages (+ cms sheets) | 42 784 · 41 109 · 42 312 | 41 456 · 39 781 · 40 984 | 41 131 · 39 456 · 40 659 | −1 653 |

Sheets: `portal/console.css` 7 941 → 6 778 B; `portal/journey.css` 2 421 B; `portal/situation.css` 2 202 B.

**After the second sync** — the same instruments against design-v5 as it stands with W3-C (`4ff9056`; this branch at
`69cdbe8`; `E/weigh_pages_resync.txt`, `E/weigh_all_resync.txt`):

| Page type | design-v5 `4ff9056` | **this branch** | Δ |
|---|---|---|---|
| `main.css` — every page (SHARED) | 37 324 | **35 483** | **−1 841** |
| the console page types: main + console + portal (SHARED) | 47 200 | **44 196** | **−3 004** |
| a journey page (+ `journey.css`) | 47 200 | 46 617 | −583 |
| «Ma situation» (+ `situation.css`) | 47 200 | 46 398 | −802 |
| «Mes pièces» (+ documents) · the company's dashboard · the help desk · the selection | 52 697 · 48 073 · 48 075 · 48 285 | 49 693 · 45 069 · 45 071 · 45 281 | −3 004 |
| the login · the home | 42 185 · 51 262 | 40 344 · 49 844 | −1 841 · −1 418 |
| the persons pages · the ecosystem doors · the Forum · the institutional pages | 40 818 · 40 659 · 40 818 · 40 121 | 39 068 · 38 910 · 38 504 · 37 749 | −1 750 · −1 749 · −2 314 · −2 372 |
| orientation · the content · account · error pages | 41 363 · 41 425 · 39 750 · 40 953 | 39 597 · 39 584 · 37 909 · 39 112 | −1 766 · −1 841 · −1 841 · −1 841 |

**Both shared bundles fall; no page type grows** — rule 2's performance check is not triggered. Requests: four stylesheets on
the journey pages and on «Ma situation» (the shell's three and the page's one), three on every other console page —
as after the fix pass for the journey pages, one fewer on «Ma situation» than two page sheets would have made.

### Smoke on the lane — every capture looked at

`E/int-after/` (and `E/int-before/`, the merged tree before the consolidation): the dashboard's «Mon parcours» (the
level line at 1440 with the file on threshold A or at step 2, the card and «Où j’en suis» at 390), the case file's
dated spine and its timeline (newest first, the first row lit), «Mon parcours» at its head, «Ma situation» (W3-F1's
form with the Stepper's spine at 1440 and its row of nodes at 390), «Mes documents», the home's passage (1 October),
the door pages and the advice pages; fr and ar; 1440 and 390; forced colours at 1440 on the console pages. **0 console
errors, 0 CSP reports, 0 responses ≥ 400, 0 horizontal overflow** on every load. Looked at whole through contact
sheets (`E/int-after/sheet-*.png`, every capture labelled): nothing out of place — the full-page captures paint the
console's fixed bars where the viewport stood (Playwright's full-page capture), on both sets alike. **After the second
sync** the same 156 captures again (`E/int2/`): 138 identical to `E/int-after/`; the changes are the dashboards' «Mon
compte» line (the last sign-in time of the freshly minted sessions) and «Mes documents» (W3-C's own page, now merged)
— the journey's pages, the door pages, the home, the Forum, the institutional pages and «Ma situation» identical.

### Tests (targeted, V5.5 — one pytest and one browser at a time, `test_ile_v5_l6`)

On the tree of the first sync and the consolidation (`800525a`). After the second sync the non-browser run was cut by
the machine (below, «Integration pass — resumed»): its figures are not reported here.

| Run | Result |
|---|---|
| non-browser (`-m "not browser"`): `apps/cases`, `apps/portal`, `tests/test_phase_console.py`, `tests/security/test_authorization_audit.py`, `tests/security/test_object_permissions.py`, `apps/orientation`, `apps/pages/tests/test_home.py`, `apps/ecosystem`, `apps/pathways`, `test_journey_w3_d`, W3-F1's `test_interior_w3_f1` and `test_orientation_w3_f1`, `test_chips_cards_w1_c`, `test_script_motion_gate`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline` (a real `collectstatic`), `test_design_showcase`, `test_console_shell_stylesheets`, `test_console_shell_w3_a`, `test_dashboard_w3_b`, `test_o14_lint`, `test_icons`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py` | **1 323 passed**, 3 skipped (the intake's rule-dependent cases), 1 xfailed (the showcase's captions, an older marker), **1 failed — not this branch's**: `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` reds on W2-A's `static/js/src/overlay/extras.js` (a `window.requestAnimationFrame` for a resize, since `7f6ea2f`) — the same file and the same test on design-v5 at `a2644b0`; handed to W2-A (below) |
| browser (`-m browser`): `test_journey_browser_w3_d`, W3-F1's `test_browser_w3_f1` and `test_orientation_browser_w3_f1`, `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`, `apps/ecosystem/tests/test_browser.py`, `apps/pages/tests/test_browser.py` (the home among them) | **113 passed**, 0 skipped |
| `ruff check` on the touched Python; `ruff format` on this family's test file (`test_design_docs.py` keeps its own pre-existing format: two long lines outside this pass's helper); `git diff --check` | passed |
| `scripts/regen_design_inventory.py` (check) · `scripts/check_ownership.py w3-d design-v5` | current · 12 inside, 17 slice, 29 generated, 19 outside — each justified below |

The journey's own tests: `test_journey_w3_d.py` 41 (38 → 41: «Ma situation»'s one page-only sheet; the still-at-load
and tokens test over the rail's three partials and the passage; the «never a third» test reads the rail's three
partials, the passage's one home and the page modifiers that never redraw it; the retirements; the journey's sheet
without the Stepper) and `test_journey_browser_w3_d.py` 12.

### Paths outside the slice (for the merge step to write into the manifest)

`scripts/check_ownership.py w3-d design-v5` (after the second sync, and the same after the third): 12 inside, 17 slice,
29 generated, **19 outside**. DL54-126's and DL54-127's eleven stand
(`apps/portal/services.py`, `apps/cases/presenters.py`, `apps/core/dev.py`,
`static/js/src/situation.js`, `templates/pages/home/_orientation.html`, `apps/pages/tests/test_home.py`,
`tests/frontend/test_design_showcase.py`, `templates/portal/dashboard.html`, `templates/cases/detail.html`,
`templates/portal/situation.html`, `templates/portal/pathways.html`); this pass adds, each the consolidation's or the
budget's:
- `static/css/v5/_interior.css` (W3-F1's: §5 and its two lines in §7 leave for the passage);
- `templates/pages/partials/_linea.html` (W3-F1's: an include of the one component) and
  `templates/ecosystem/partials/pilot_flow.html` (W3-F1's: one comment names the drawing's home);
- `templates/components/timeline.html` (deleted with §17, its last caller the showcase's demo);
- `apps/core/dev.py` and `templates/dev/showcase.html` (the showcase's timeline demo out);
- `tests/frontend/test_interior_w3_f1.py`, `tests/frontend/test_orientation_w3_f1.py`,
  `apps/ecosystem/tests/test_compliance.py` (W3-F1's: the import lists receive the passage's line, the form's sheet
  is «Ma situation»'s, the partials read together include the passage), `tests/frontend/test_design_showcase.py`
  (the timeline's marker out);
- in files the checker passes as slices, beyond the slice's words: `apps/portal/static/portal/v5/_wizard.css`
  (W3-F1's: the Stepper's rules out, its header names its new sheet), `apps/portal/static/portal/console.css` (W3-F1's
  import line out), `tests/frontend/test_design_docs.py` (the token check's composition helper, beside this family's
  section-count slice);
- new, W3-D's whole files: `apps/portal/static/portal/situation.css` (the page-only sheet of «Ma situation»: the form,
  then the Stepper), `apps/portal/static/portal/v5/_journey-nodes.css` and `apps/portal/static/portal/v5/_journey-stepper.css`
  (the slice names `_journey-rail.css`; the drawing is now three partials), and `apps/portal/static/portal/journey.css`
  (DL54-127). Generated: `static/css/dist/portal/situation.css`.

### Not done, and handed to

- **W2-A (or the steward)** — the motion gate (W1-D's `tests/frontend/test_script_motion_gate.py`) is red on
  design-v5 at `a2644b0` and here alike: `static/js/src/overlay/extras.js` waits a frame with
  `window.requestAnimationFrame` (the resize's coalescing, `7f6ea2f`) where the gate asks `nextFrame()` from
  `motion.js`. W2-A's file: not touched.
- **W3-F1 / W4 (mobile)** — the door pages' station text stays 15 px on phones, as W3-F1 drew it (the passage dropped its
  RE-4 line to keep the door pages identical); if RE-4 should cover the door pages' stations too, it is one line in
  `_journey-passage.css` for every page that draws «la linea» — a design change, not this pass's.
- **The third sync** — design-v5 moved again while this pass closed: the devops merge (`1a61a7c`, production readiness:
  the deployment docs, settings and tests; its record DL54-121 shares the decision log with this branch) — merged by
  the resumed pass (below). The rehearsal worktree is removed.
- Still as «Review fixes» says: Safari and Firefox not run (m6); «Ma situation»'s count (m4, W3-E's); the items handed to
  W3-E, W3-A / W4-B.
- The rehearsal's two trial-only reds, `apps/ecosystem/tests/test_gated_pages.py`'s (the W3-F1 steward's `78cb0de`
  reads the gated doors' button in the page's content), pass on the real tree; the motion gate's red is design-v5's
  own (above).

### The lane, cleaned

The four minted sessions revoked on `ile_v5_l6` (`sessions.py revoke`); the lane server on 8786 stopped; no browser
of mine left running and the pass's Chromium profile deleted; the rehearsal worktree removed (its `node_modules`
junction unlinked first, then `git worktree remove`); the benchmark lock never created; scratch scripts and
evidence outside every repository (`C:/tmp/ile_v5_council/.work/w3-d/w3-d-fix/`, `E/`).

## Integration pass — resumed (implementer w3-d-fix, 15 October 2026)

The integration pass above was cut on 12 October by the previous account's weekly limit, after its commits and before
its notes. This sitting resumed it: what the branch held was read first, design-v5 was merged once more (the DevOps
readiness merge), and the pass was verified end to end on the merged tree instead of being redone. No product page
changed in this sitting: the decision log, one merge, the design showcase's links (§4 below, development only), these
notes. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-d/integration/` — `r3-base/` (design-v5), `r3-head/` (this branch),
`resumed/` (the weights, the proof, the comparisons); scripts: `C:/tmp/ile_v5_council/.work/w3-d/w3-d-fix/resumed/`.

**Lane.** Lane 6 on 8786: this worktree (HEAD) and, for every «before», an export of design-v5 at `3d5351b` in the
scratch folder (BASE: the tree 8780 would serve, on the lane's data), both on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`
— `2026-10-01` for the home's passage, gate G3 closed by the flag's own date, no data changed —, `DB_CONN_MAX_AGE=0`,
`--noreload`, no preview flag); pytest on `test_ile_v5_l6`; one headless Chromium of mine at a time (its own profile,
`C:/tmp/ile_v5_council/.profiles/w3-d-fix/`, the cache off) and one pytest of mine at a time — the non-browser run
first waited behind another session's full suite (on its own database, about 1 GB free beside it), then ran beside
the other sessions' runs once 1.8 GB were free.
Sessions for `seed-person`, `qa-person`, `qa-fresh-person` and `qa-doc-person` minted with `Client.force_login` (no
password used, typed or stored), revoked at the end. The benchmark lock was absent at every series and build. **No
browser run crashed.** Never 8780, 8782, Chrome 9222 / 9223.

### What the resume found, and what was kept

- **The branch** at `69cdbe8` (the second sync), with one uncommitted edit of `DECISION_LOG_V54.md` — the cut attempt's
  update of its integration entry: the second sync, and the weights against design-v5 after W3-C. Re-weighed on the
  committed bundles before anything else: every figure true (`main.css` 37 324 → 35 483 B, the console page types
  47 200 → 44 196 B, the journey pages 46 617 B, «Ma situation» 46 398 B, «Mes pièces» 52 697 → 49 693 B) — **kept**,
  committed `dca50a1`.
- **The notes' «Integration pass» section** — drafted by the cut attempt in its scratch folder at 08:17 on 12 October,
  never appended, though DL54-128 cites it: **appended above**, corrected only where the third sync made it untrue (the
  decision-log numbers, the devops merge, its last test run).
- **That attempt's last non-browser run** (after the second sync, 12 October 08:41) had ended on the machine, not the
  code: 3 failed and 4 errors, each a subprocess that could not start (`0xC0000142` — `collectstatic`, the icons'
  check, the ownership checker's runs). It was not reported then and is not now: the targeted runs below replace it.

### The third sync (`9237de4`)

design-v5 moved after W3-C's merge: the devops merge (production readiness, V5.9 — the runbook, the checklist, the
rollback, `.env.example`, the production settings and their tests; `1a61a7c`) and its record DL54-121 (`3d5351b`): 26
commits, documents, settings and tests only — no stylesheet, template or script. One conflict, the decision log:
design-v5's text kept whole, this family's seven rows and entries after its last, renumbered with their own
cross-references (`dl_resync.py`: 128 entries numbered 1 … 128 in order, the index the same); DL54-128 says the third
sync. `static/css/dist` and `static/js/dist` deleted and rebuilt (`npm run build`): **byte-identical to the committed
bundles**. `manage.py check`: no issue. `scripts/regen_design_inventory.py`: current.

**The decision-log numbers — a mapping for the steward.** design-v5 ends at DL54-121, so this family's entries are
**DL54-122 … DL54-128**. The numbers written earlier — in this file, `REVIEW.md`, `A11Y_PERF.md`, `P0_RECHECK.md` and the
commit messages — read as follows (only the numbers moved; the steward renumbers again if design-v5 moves first — the
family's changes to the log are additive: seven rows, seven entries):

| Written as (step 1, fix pass) | After the first sync (`b379eec`, `d7b7e69`) | After the second (`69cdbe8`) | **Now** (`9237de4`) | The entry |
|---|---|---|---|---|
| DL54-88 | DL54-110 | DL54-121 | **DL54-122** | a threshold is a place — SELECTION on threshold A |
| DL54-89 | DL54-111 | DL54-122 | **DL54-123** | one rail drawing for the console |
| DL54-90 | DL54-112 | DL54-123 | **DL54-124** | one passage drawing for the public pages |
| DL54-91 | DL54-113 | DL54-124 | **DL54-125** | a date on the rail in the sans; «Ma situation» still at load |
| DL54-92 | DL54-114 | DL54-125 | **DL54-126** | the paths outside the slice; the deletions; the CSS as measured |
| DL54-93 | DL54-115 | DL54-126 | **DL54-127** | the fix pass |
| — | DL54-116 | DL54-127 | **DL54-128** | the integration pass |

### Verified end to end on the merged tree

**1 · One passage drawing.** Before = design-v5 at `3d5351b` (BASE), after = this branch (HEAD), the same data and
dates; `shoot.py` + `compare.py` (`E/r3-base/`, `E/r3-head/`, `E/resumed/compare-base-head.txt`): `/projet-pilote/`,
`/entreprises/`, a pathway sheet (`/parcours/salaried_work/`), `/parcours/`, `/diplomes-et-titres/`, `/formation/`,
`/orientation/`, `/forum/` and `/le-projet/` (the two that shed the drawing), and the home's orientation chapter; fr and
ar; 1440 × 900 and 390 × 844 (phone emulated). **68 captures: 36 identical; 28 changed — every one the door pages' ring
rims**, 40–124 pixels a page, none above 24 / 255 (the open ring's border antialiased over the page's ground instead of
over a paper fill: the integration pass's figures, unchanged); **the home's chapter changes, as designed** (4 captures,
a new height — 454 → 440 px at 1440; 733 → 778 px fr and 644 → 699 px ar at 390): design-v5 draws its four neutral steps
with V4's `.sequence`, this branch with «la linea» (DL54-124). Looked at, and measured: the home's passage computes what
the door pages compute — the ring 12 px, a 1 px ink border, no fill; the numeral a CSS counter, 13 px (14 px in Arabic)
in text-2; the line 1 px `rgb(122, 134, 139)`; the label 17 px at 600 (`report-home.json`, `report-public.json`) — four
stations across from 48rem, down the reading edge on a phone, mirrored in Arabic with its numerals left alone. 80 loads:
0 console errors, 0 CSP reports, 0 responses ≥ 400, 0 horizontal overflow.
- **The import lines.** `@import url("../css/v5/_journey-passage.css");` after `_interior.css` in
  `pathways/pathways.css`, `ecosystem/ecosystem.css` and `orientation/wizard.css`; the home's `pages/css/pages.css`
  imports it first; the Forum's and the institutional pages' sheets do not (they draw no passage). Every template that
  draws «la linea» (`class="linea`, `_linea.html`, `components/stepper.html`) is served by one of those four sheets — the
  dev showcase too, since §4.
- **Retired only where proved unused** (`proof.py`, `E/resumed/proof-third-sync.txt`: every template, Python, JS and
  JSON file of design-v5 at `3d5351b`, of this tree, and of the worktrees in flight — `v54-w3-e` (at design-v5, nothing
  changed yet), `v54-intfix` (28 files: the overlay, shell and loader scripts and their tests), `v54-sec-f5` (nothing
  changed)). `components.css` §17 and `components/timeline.html`: on design-v5 their last caller is the showcase's demo,
  retired with them; nothing in flight uses them; the four tests that name the timeline assert its absence or feed a
  probe synthetic readings. `v5/_wizard.css`'s Stepper rules: the Stepper (`components/wizard_stepper.html`, `wstep`) is
  drawn by «Ma situation», which links `portal/situation.css` (the form, then the Stepper), and by the dev showcase;
  nothing in flight draws it elsewhere. Built: `main.css`, `console.css` and `portal.css` carry no `.wstep`, `.linea` or
  `.timeline` rule and no rule of the guided form (`.wiz*`, `.opt*`) — `main.css` keeps base.css's one font line for
  `.wiz__foot-count`, `.journey__when` and `.tl__when`.

**2 · The shared CSS under the definitive ruling.** gzip −9 (mtime 0) of the bundles rebuilt from a clean dist,
`.work/w2-a/w2-a-merge/weigh_pages.py` and `weigh_all.py` (`E/resumed/weigh_pages_3rd.txt`, `weigh_all_3rd.txt`;
`weigh_every_sheet.txt` for every `css/dist` entry):

| Page type | design-v5 `3d5351b` | this branch `9237de4` | Δ |
|---|---|---|---|
| `main.css` — every page (SHARED) | 37 324 | **35 483** | **−1 841** |
| the console page types: main + console + portal (SHARED) | 47 200 | **44 196** | **−3 004** |
| a journey page — the dashboard, «Mon parcours», the case file (+ `journey.css`, 2 421) | 47 200 | 46 617 | −583 |
| «Ma situation» (+ `situation.css`, 2 202: its form and its Stepper) | 47 200 | 46 398 | −802 |
| «Mes pièces» (+ documents) | 52 697 | 49 693 | −3 004 |
| the company's dashboard · the help desk · the selection · the Academy (+ their sheets) | 48 073 · 48 075 · 48 285 · 47 818 | 45 069 · 45 071 · 45 281 · 44 814 | −3 004 |
| the login (+ entrance) | 42 185 | 40 344 | −1 841 |
| the home (+ hero + pages) | 51 262 | 49 844 | −1 418 |
| the persons pages (+ pathways) · the ecosystem doors (+ ecosystem) | 40 818 · 40 659 | 39 068 · 38 910 | −1 750 · −1 749 |
| the Forum (+ forum) · the institutional pages (+ interior) | 40 818 · 40 121 | 38 504 · 37 749 | −2 314 · −2 372 |
| orientation (+ orientation/wizard) | 41 363 | 39 597 | −1 766 |
| the content · account · error pages (+ cms sheets) | 41 425 · 39 750 · 40 953 | 39 584 · 37 909 · 39 112 | −1 841 |

Both shared bundles fall (rule 1; their ceilings ratchet down at the merge) and no page type grows (rule 2's
performance check is not triggered); a page that also links W2-A's `core/overlay-panels.css` moves with its base. The
sheets that changed: `main.css` −1 841, `console.css` −1 163, `forum.css` −473, `interior.css` −531 (they shed the
passage); `pathways.css` +91, `ecosystem.css` +92, `orientation/wizard.css` +75 (the passage's one home), `pages.css`
+423 (the home: the passage for V4's sequence rules); new, page-only: `journey.css` 2 421, `situation.css` 2 202.
**«Ma situation»'s form CSS** lives in `apps/portal/static/portal/situation.css` → `css/dist/portal/situation.css`,
linked, of the product's templates, by `templates/portal/situation.html` alone, after the shell's two sheets (W3-E keeps
that link on its branch; the dev showcase links it for its specimens, §4).

**3 · Smoke on the lane — every capture looked at** (`E/r3-head/`, through labelled contact sheets `sheet-*.png` and the
journey's crops at full size): the dashboard's «Mon parcours» (the level line at 1440 — `seed-person`'s file on
threshold A, `qa-person`'s at step 2; the card and «Où j’en suis» at 390, the threshold's caption heading it), «Mon
parcours» at its head, the case file's dated spine and its timeline (newest first, the latest lit), «Ma situation»
(the form with the Stepper's spine at 1440 and its row of nodes at 390), «Mes documents», the home's passage, the door
pages; fr and ar; 1440 and 390; forced colours at 1440 on the console pages. **82 loads, 156 captures: 0 console
errors, 0 CSP reports, 0 responses ≥ 400, 0 horizontal overflow**; the journey's sheet on the dashboard, «Mon parcours» and the case
file, `situation.css` on «Ma situation», neither on «Mes documents». Against the second sync's set (`E/int2/`,
`E/resumed/compare-int2-head.txt`): **144 of 156 identical**; the 12 others are the dashboards' «Dernière connexion»
line, the minted sessions' sign-in time (`E/resumed/signin-diff-dash-seed-fr-1440.png`).

**4 · One thing the verification found, fixed: the design showcase** (`/_design/`, development only; `5a898f5`,
`5672576`, `002fd24`). Since the journey's CSS left `main.css` (V4's JourneyRail and Timeline, the V1 stepper — step 1)
and the rail left `console.css` (the fix pass), the showcase drew its rail, timeline and passage demos bare, and its
Stepper and OptionCards as on design-v5 (bare: their rules were never in `main.css`): it links `main.css` and the page
sheets of the families that drew into one (W2-A's `core/overlay-panels.css`, W3-C's `documents/documents.css`), not this
family's. It now links `portal/journey.css`, `portal/situation.css` and, for the passage, `pages/css/pages.css` (a
partial is never an output of its own; the home's sheet is the passage's one importer with no page grammar of its own —
none of its home rules finds an element on the showcase). A first try without `situation.css`, to keep «Ma situation»'s
sheet with one linker, left the Stepper half drawn by the journey sheet's vocabulary (nodes and line, no layout:
`E/r3-head-old-showcase/`) — so the sheet is linked, and the rule is stated where it holds: **of the product's
templates, `templates/portal/situation.html` alone links `portal/situation.css`** (`templates/dev/` is never served
without DEBUG; `test_journey_w3_d` checks it so). DS 2026 §2.1 names the showcase among the three sheets' loaders;
DL54-128 item 7. Seen on the lane (`E/r3-base/showcase-*`, `E/r3-head/showcase-*`, 1440 and 390): design-v5's showcase
drew V4's numbered rail and the V1 stepper and left the Stepper as bare links; this branch's draws «La soglia» (the
spine and the level line, the card at 390), the timeline on the spine, the Stepper and «la linea» as the product does.
0 console errors, 0 CSP reports; the showcase's 78 px overflow at 390 is design-v5's too (handed to, below).

**5 · Tests** (targeted, V5.5 — one pytest at a time, `test_ile_v5_l6`):

| Run | Result |
|---|---|
| non-browser (`-m "not browser"`, 35 min): `apps/cases`, `apps/portal`, `tests/test_phase_console.py`, `tests/security/test_authorization_audit.py`, `tests/security/test_object_permissions.py`, `apps/orientation`, `apps/pages/tests/test_home.py`, `apps/ecosystem`, `apps/pathways`, `test_journey_w3_d`, W3-F1's `test_interior_w3_f1` and `test_orientation_w3_f1`, `test_chips_cards_w1_c`, `test_script_motion_gate`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline` (a real `collectstatic` under the manifest storage), `test_design_showcase`, `test_console_shell_stylesheets`, `test_console_shell_w3_a`, `test_dashboard_w3_b`, `test_o14_lint`, `test_icons`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py` | **1 330 passed**, 3 skipped (the intake's rule-dependent cases), 1 xfailed (the showcase's captions, an older marker), **1 failed — not this branch's**: `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` on W2-A's `static/js/src/overlay/extras.js` (`window.requestAnimationFrame`), red on design-v5 too and fixed on `v54-intfix` (`822b3ae`); `test_chips_cards_w1_c` green (`E/resumed/targeted-nonbrowser.log`) |
| browser (`-m browser`, 12 min): `test_journey_browser_w3_d`, W3-F1's `test_browser_w3_f1` and `test_orientation_browser_w3_f1`, `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`, `apps/ecosystem/tests/test_browser.py`, `apps/pages/tests/test_browser.py` (the home among them) | **113 passed**, 0 skipped, no crash (`E/resumed/targeted-browser.log`) |
| `ruff check` and `ruff format --check` on the one Python file this sitting changed (`test_journey_w3_d.py`); `git diff --check`; no CR byte in any text file the branch changes | passed |

The journey's own tests: `test_journey_w3_d.py` 41 (its «Ma situation» test now says «of the product's templates»: the
DEBUG-only showcase links the sheet too, §4) and `test_journey_browser_w3_d.py` 12.

**6 · Ownership.** `scripts/check_ownership.py w3-d design-v5`: 12 inside, 17 slice, 29 generated, **19 outside** —
the same 19 as the second sync, each justified in «Integration pass» above (DL54-126's and DL54-127's eleven, the
consolidation's and the budget's eight) for the merge step to write into the manifest; the showcase's three links sit in
`templates/dev/showcase.html`, already among them (the timeline's demo out), as W2-A's and W3-C's links were assigned
to theirs.

## Review fixes — re-verified on the merged tree (implementer w3-d-fix, 15 October 2026)

Finding → change → evidence. The review (`REVIEW.md`: four majors, six minors) and the accessibility check
(`A11Y_PERF.md`: one blocking, two minors) were fixed by the fix pass («Review fixes», 12 October) and the integration
pass (M4); `P0_RECHECK.md` closed the blocking item. Here, each one where it stands after the third sync — nothing of
the review is left open in this family's slice but m6's two browsers.

| Finding | The change | Evidence on the merged tree |
|---|---|---|
| **M1** · A11Y **1** (blocking) — the console page types over the hard CSS ceiling | the rail in the page-only `portal/journey.css` (fix pass); «Ma situation»'s form and Stepper in `portal/situation.css`, the rail a vocabulary and two components (integration pass) | the console page types **44 196 B against design-v5's 47 200** (−3 004), `main.css` −1 841 (table above); `journey.css` linked by the three journey pages, `situation.css` by «Ma situation» alone of the product's pages (the 42 console loads) |
| **M2** — «Mon parcours» draws no journey | `templates/portal/pathways.html` draws `components/journey_rail.html` at its head when the person has a file (`pathways_page`), the dashboard's label, no new copy | `parcours-seed-*`: the level line at 1440, the card at 390, fr and ar; `test_journey_w3_d` («Mon parcours» with and without a file), `test_journey_browser_w3_d` |
| **M3** — a suspended or closed file told «Vous êtes ici» on step 1 | no current item for a status off the line, «Vous êtes ici» nowhere; the case file dates what the trail reached (`journey_place`, `journey_with_dates`) | `test_journey_w3_d`: one test per status in the presenter, the component and the case file, the stop on a threshold, a resumed then closed file (no such file in the lane's data; the fix pass's spliced captures stand) |
| **M4** — «never a third» true in the product | the integration pass: one passage drawing, `components.css` §17, `timeline.html` and `_wizard.css`'s Stepper retired | §1 above: the door pages identical to design-v5's but for the rings' rims, the home's passage the door pages' drawing, the retirements proved on design-v5 and in flight |
| **m1** — the timeline hides its «now» | newest first, the first row lit; the actor line skipped when it repeats the detail | `file-seed-*-timeline`: the lit ring on the first row, «Acteur autorisé» once a row, fr and ar |
| **m2** · A11Y **2** — the disclosure's tap | the notes say what was measured (a 63–153 ms task at ×4, the journey's share 23–42 ms; the shell's `html:has()` the rest) | no code; O3 handed to W3-A / W4-B |
| **m3** — the shores disagree between densities | the level line's last stretch to the rail's end under «Italie»; «Vous êtes ici» under its node | `dash-*-1440-rail`: the line ends under «Italie» / «إيطاليا», fr and ar |
| **m4** — «Ma situation» counts three ways | — (W3-E's view and template) | still true: «0 question(s) renseignée(s) sur 7» under an eight-node Stepper (`situation-*-390-page`) — handed to W3-E |
| **m5** — on a threshold the card names the phase, not the place | the threshold's caption heads the card | `dash-seed-*-390-rail`: «Autorités compétentes : décisions administratives» / «السلطات المختصة: القرارات الإدارية» over the phase |
| **m6** — the wide density leans on one browser behaviour | `::details-content` gets `display: block` with `content-visibility: visible` | Chromium only (as computed at the fix pass); Safari 18.4+ and Firefox not installed — handed to the W4 sweep |
| A11Y **3** — the Stepper's line takes the pointer | `pointer-events: none` on the lines | `test_journey_browser_w3_d` (a point on the line lands on its question's link) |

### Handed to

- **W3-E** (the console's secondary pages and the case file; on its own branch since 15 October): **m4** — one total for
  the person («0 question(s) renseignée(s) sur 7» while the Stepper draws eight questions and the foot counts «1 / 8»;
  `total = len(PROFILE_FIELDS)` without the recognition question); **O1** — the case file's inspector
  (`aside.file-grid__inspector`) scrolls inside itself from 80rem with nothing focusable in it (`tabindex="0"` on the
  labelled aside, or no inner scroll); «Mon parcours»'s lead now heads the journey too (new words would be B1's); and
  the three links this family wrote into W3-E's templates — `portal/situation.css` in `portal/situation.html`,
  `portal/journey.css` in `cases/detail.html` and `portal/pathways.html` — are the only way those pages get their
  drawing: keep them.
- **W3-A / W4-B** — **O2**: under forced colours the current entry of the rail and of the phone bar draws the focus
  ring's outline at rest (WCAG 2.4.7); another current marker. **O3**: `html:has(.console-drawer[open])` recalculates
  the whole document on every `[open]` toggle (the journey's disclosure pays 390 elements for its 112).
- **W2-A / the integration checkpoint** (`v54-intfix`) — the motion gate (`tests/frontend/test_script_motion_gate.py`)
  reds on design-v5 and here alike on `static/js/src/overlay/extras.js`'s `window.requestAnimationFrame`; fixed on
  `v54-intfix` (`822b3ae`), not yet on design-v5. Not this family's file.
- **The integration checkpoint** — `test_chips_cards_w1_c` (design-v5's second CI red on 12 October: W3-F2's
  `.registro__row > .chip` placement) passes on this merged tree: nothing to hand over there; the motion gate above
  is the one red, and it is `v54-intfix`'s to land.
- **The steward / the showcase's owner** (`templates/dev/showcase.html`, `apps/core/dev.py`, `static/css/dev/showcase.css`
  — the showcase test's xfail says they have no owner) — at 390 the showcase overflows by 78 px, on design-v5 as here
  (another demo, not the journey's: its demos are drawn now, §4).
- **W3-F1 / W4-A (mobile)** — the door pages' station text stays 15 px on phones as W3-F1 drew it (the passage dropped
  its RE-4 line to keep them identical); RE-4 for the door pages would be one line in `_journey-passage.css`.
- **W4-C (accessibility + performance sweep) or the owner's report** — m6: the wide density in Safari 18.4+ and Firefox
  (neither installed here).
- **The owner (B1)** — unchanged: no word was added; OJ5, OJ6, the timeline's title and the deadline-distance words wait.
- **From the review's «Seen on the way», still true, for the orchestrator:** W3-B's dashboard (shipped) tells a
  suspended or closed person that there is no file (`active_case` keeps the active statuses only; the NowPanel falls to
  «Vous n'avez pas encore de dossier…»); the owner (a class C question) — a person is offered state changes on their own
  file (`cases/policies.py`: «Suspendu», «Procédure administrative en cours», «Parcours clôturé»…), which the journey
  then draws as a fact; the report — at the preview's date (3 October, gate G3 open) the home carries the prescribed
  sentence and no passage: «la linea» shows on the door pages, and on the home only while G3 is closed. The review's
  first item (the pathway pages' V1 timeline broken at 1440) is gone: those pages draw «la linea» (§1).

### The lane, cleaned

The four minted sessions revoked on `ile_v5_l6` (`sessions.py revoke`: 4 rows deleted, the cookie file removed; 0
live sessions left on the lane's database); the lane server on 8786 stopped (`lane2.py stop`: the port free); no
browser of mine left running and this sitting's Chromium profile deleted; the first, queued test run's waiter shell
stopped with its task before it ran a test (it waited on another session's suite; the run then started on its own);
the benchmark lock never created; design-v5's export (`base-3d5351b`) kept in the scratch folder for a re-shoot,
outside every repository, like every script and capture (`C:/tmp/ile_v5_council/.work/w3-d/w3-d-fix/resumed/`, `E/`).
