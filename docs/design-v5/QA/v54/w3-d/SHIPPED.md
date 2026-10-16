# W3-D shipped — 15 October 2026

**The journey «La soglia» — one passage and one rail drawing across the product.** Tag **`v54/w3-d`** (design-v5
`17b65bf`, the status commit, as for the earlier families); merge commit `e35714c`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 22:14 and verified by request at
22:15. Steward's merge, label `w3-d-merge`, under `DESIGN_V5_MERGE_LOCK` from 21:14:58, after W3-F1's tag (the plan's
order, §3.5 item 6). Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` were both SHIP_AFTER_FIXES with no
P0; the fix pass and the integration pass (`NOTES.md`) closed the four majors and the minors of the review and the
check's three findings, and `P0_RECHECK.md` closed the check's one blocking item (SHIP). No reviewer has read the
integration pass again; the family verified it end to end on the merged tree (`NOTES.md`, «Integration pass —
resumed»).

## What shipped

- **One rail drawing for the console** (`apps/portal/static/portal/v5/_journey-nodes.css`, `_journey-rail.css`,
  `_journey-stepper.css`; `templates/components/{journey_rail,case_timeline,wizard_stepper}.html`). One vocabulary on
  every journey of the console: behind the file a 10 px ink dot (never a check), where it stands an 18 px laguna ring
  on its flat wash, ahead a 12 px open ring; the line 2 px, laguna where the file has been. One marker a column, the
  phase's glyph: no numeral, no holder.
  - **The dashboard's «Mon parcours»**: from 56rem of the component's own width, the level line — «Maroc» at the reading
    start, «Italie» at the end, the seven steps on one level with their glyphs and words, the two thresholds crossing
    it (the competent authorities' stamp before the first Italian step, the Italian territory's arch before the
    arrival) with the site's own jurisdiction captions, «Vous êtes ici» under the item where the file stands. Below
    it — the phone, the tablet, a narrow column — **a card and its disclosure**: what is true now (the item's glyph and
    words, «Étape n sur 7», «Vous êtes ici»), then the list behind the native «Où j'en suis», closed, as a spine.
  - **A threshold is a place**: a file in SELECTION stands on threshold A, not on a step — the dashboard, the phone's
    card and the case file agree with the header's chip (`portal.services.journey_for`).
  - **A file off the line** (SUSPENDED, CLOSED) has no current item: nothing says «Vous êtes ici»; the case file reads
    its trail for how far it had come and marks the stop (`cases.presenters.journey_with_dates`).
  - **The case file**: the same component as a dated spine at every width, every reached step with its date; the
    timeline on the same spine, newest first, the latest event lit, an actor line never repeated.
  - **«Ma situation»**: the Stepper on the same nodes — answered the ink dot, the question shown the ring, the others
    open; the line a hairline (answered in any order, never «travelled»); on a phone a level row of nodes. The page
    moves nothing at load (the submit takes its role without a transition, `static/js/src/situation.js`).
  - **«Mon parcours»** draws the journey at its head when the person has a file (the dashboard's component and label),
    the saved pre-assessments under it.
- **One passage drawing for the public pages** — «la linea» (`static/css/v5/_journey-passage.css`,
  `templates/components/stepper.html`): the numerals over open stations, the words under them, down the reading edge
  on a phone, across from 48rem. W3-F1's «la linea» folded into it (V5.8 rule 3: the family that merges second
  consolidates): the doors, the pilot, the pathway sheets, «Diplômes et titres», «Formation» and the questionnaire draw
  from this one partial — measured identical but for their rings' rim antialias —, and the home's orientation steps
  are drawn by it while gate G3 is closed. An explanation is never a progress: no current station on these pages.
- **Still at load** everywhere: no animation, transition or keyframe in the journey; reduced motion the same still;
  forced colours drawn; Arabic mirrored, the dates and the numerals left alone; no new word — every word a catalogue
  string.
- **CSS** (V5.8): the journey's CSS left the shared bundles for the page-only sheets of the pages that draw it —
  `dist/main.css` 37 324 → **35 483 B on every page** (−1 841), the console page types 47 200 → **44 196 B** (−3 004);
  `portal/journey.css` (2 421 B) on the dashboard with a person's file, «Mon parcours» with a file and the case file
  (**46 617 B**), `portal/situation.css` (2 202 B: W3-F1's guided form, then the Stepper) on «Ma situation» alone of
  the product's pages (**46 398 B**); every page type lighter. Retired with their last consumers: `components.css` §16
  (the V1 stepper, the progress bar) and §17 (the timeline) with `components/timeline.html`, `v4/workspace.css`'s
  JourneyRail and Timeline with their three keyframes, `register.css`'s shore crossing, the home's V4 sequence rules,
  `v5/_wizard.css`'s Stepper rules, `v5/_interior.css` §5.

## The merge

- **The order and the sync**: `v54/w3-f1` has stood on design-v5 since 12 October. design-v5 at `3d5351b` (the devops
  record) was the branch's merge base — the family's third sync had merged it —, so `git merge design-v5` in the
  branch said «Already up to date», the family's seven decision-log entries stand as **DL54-122 … DL54-128** (additive
  only, checked), and the merge into design-v5 wrote no conflict (`git diff v54-w3-d e35714c` is empty).
- **Ownership** (`9b1fc84`, on the branch): the 19 paths outside the slice the family declares (DL54-126 item 1,
  DL54-127 item 6, DL54-128 item 6), each read in the diff and assigned to w3-d — one whole file
  (`templates/components/timeline.html`, retired) and 18 slices —; the four new sheets as whole files; seven slices
  named as written and a note on `apps/cases/services.py` (the plan's slice names it; `journey_for` lives in
  `apps/portal/services.py`). After it: 17 inside, 31 slice, 29 generated and the manifest itself, the one
  steward-only path; `--validate`: coherent, 26 families, 651 entries.
- **The shared CSS gate (V5.8) passed**: both shared bundles fall and no page type grows; every ceiling lowered to the
  merged weight; the journey's two page types recorded through their own sheet (V5.8 rule 2: each lighter than the
  console page type it was, so the performance check is not triggered; the family's check and its P0 re-check stand).
  The record: **DL54-129** (`7295882`), with the table of every page type before → after.
- **Bundles** rebuilt from a clean dist in the branch (byte for byte the committed ones) and in design-v5 after the
  merge (`cec9425`: the CSS byte for byte the tested branch's; the JS design-v5's own but `situation.js`, the chunks'
  names following this worktree). `scripts/regen_design_inventory.py`: current on both. The capture report is
  unchanged (the home, the privacy page, the login and the 404: no icon, h1, overflow or direction changes).
  `ruff check .` clean; `makemigrations --check`: no changes; `manage.py check`: no issue.
- **Tests** (lane `test_ile_v5_l6`, one pytest and one browser of the steward's at a time, no run crashed; V5.5:
  targeted, not the full suite; `C:/tmp/ile_v5_council/evidence/v54/w3-d/merge/tests_*.log`): non-browser —
  `apps/cases`, `apps/portal`, `tests/test_phase_console.py`, `tests/security` (with the object-permission and
  authorisation audits), `apps/orientation`, the home's tests, `apps/ecosystem`, `apps/pathways`, the family's own,
  W3-F1's, the chips, the motion gate, the design docs, both bundle-current tests, the static pipeline, the showcase,
  the console shell's and the dashboards' — **1 404 passed**, 3 skipped (the intake suite's own), 1 xfailed, **1
  failed: design-v5's own motion gate** (below); browser — the family's, W3-F1's two, `apps/portal/tests/test_browser.py`,
  `tests/i18n/test_rtl_browser.py`, the ecosystem's and the pages' — **113 passed**, 0 skipped; on design-v5 after the
  merge and the rebuild **297 passed** (bundles, docs, pipeline, ownership, inventory, the family's own, the showcase,
  the chips, W3-F1's import lists), the preview's own tests with the new status files **297 passed**.
- `live_status.json`: the family row w3-d — state v5, its review as the decision, the tag — and **no surface key**
  (below). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all checked by request after the restart: 200, no traceback, 0 errors in the server log)

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w3-d`; the index http://127.0.0.1:8780/__design-v5/index/
  lists the family with its review (http://127.0.0.1:8780/__design-v5/decisioni/w3-d/REVIEW.md).
  http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/ answer 200.
- **The public passage «la linea»**: http://127.0.0.1:8780/fr/projet-pilote/ · http://127.0.0.1:8780/fr/entreprises/ ·
  http://127.0.0.1:8780/fr/parcours/ · http://127.0.0.1:8780/fr/parcours/salaried_work/ ·
  http://127.0.0.1:8780/fr/diplomes-et-titres/ · http://127.0.0.1:8780/fr/formation/ ·
  http://127.0.0.1:8780/fr/orientation/ — and the same under `/ar/`.
- Through the preview's persona switch («Personas» → «Entrer», no password), then:
  - «Personne avec dossier» (qa-doc-person, a file at step 1): the dashboard http://127.0.0.1:8780/fr/espace-reserve/
    (the level line at desktop width; the card and «Où j'en suis» in the phone frame), the case file
    http://127.0.0.1:8780/fr/espace-reserve/dossiers/EE167596D4/ (the dated spine and its timeline), «Ma situation»
    http://127.0.0.1:8780/fr/espace-reserve/ma-situation/ (the Stepper's eight questions), «Mon parcours»
    http://127.0.0.1:8780/fr/espace-reserve/mon-parcours/ (the journey at its head); the mirror under `/ar/`.
  - «Personne, conditions non acceptées» (qa-person, a file at step 2): the dashboard, the case file
    http://127.0.0.1:8780/fr/espace-reserve/dossiers/E46E03B461/ (three events, newest first), «Ma situation», «Mon
    parcours» with its saved pre-assessment.
  - «Personne sans dossier» (qa-fresh-person): the dashboard draws no journey and loads no journey sheet; «Ma
    situation».
  - Reduced motion and forced colours: the system's settings.

## Not done

- **No surface key in `live_status.json`.** The journey is drawn inside other families' page types: the dashboards (v5
  since W3-B), the home and the doors (v5 since W2-D and W3-F1), and «Ma situation», «Mon parcours» and the case file,
  whose pages W3-E completes — «Ma situation» still draws V4's Panel and workspace head, «Mon parcours» its V4 results
  and empty state, the case file is W3-E's page. No page type's composition is completed by this merge alone (as W3-A's
  and W2-A's merges said of their systems): those three stay «V4 + fondation» in the index, with the V5 journey inside
  them, until W3-E's merge marks them (DL54-129 item 11).
- **Not reachable through the preview's personas**: a file in SELECTION standing on threshold A, and a suspended or a
  closed file — none of the qa personas' files is in those states (the lanes' `seed-person` stands on threshold A; the
  states off the line are held by the family's tests, one per status, and were seen in the review's spliced captures).
  At the preview's date (3 October, gate G3 open) the home carries the prescribed sentence and no passage.
- **Measures not made**: the wide density's `::details-content` in Safari 18.4+ and Firefox (review m6; neither
  installed — W4-C); a real phone and a screen reader were never run; the Performance Lead's measures on 8782; no
  browser on 8780 (by rule).
- **Handed to other families** (`NOTES.md` «Handed to»): **W3-E** — «Ma situation»'s one count (m4: «0 question(s)
  renseignée(s) sur 7» under eight questions), the case file inspector's focusable scroller (O1), and the three links
  this family wrote into W3-E's templates (`portal/journey.css` in `cases/detail.html` and `portal/pathways.html`,
  `portal/situation.css` in `portal/situation.html`) — the only way those pages get their drawing: keep them;
  **W3-A / W4-B** — the forced-colours current entry drawn with the focus ring's outline at rest (O2), and
  `html:has(.console-drawer[open])` recalculating the whole document on every toggle (O3); **W3-F1 / W4-A** — the door
  pages' station text stays 15 px on phones (RE-4 would be one line in `_journey-passage.css`); **the showcase's
  owner** — its 78 px overflow at 390, design-v5's too; **the owner (B1)** — no word was added: OJ5, OJ6, the timeline's
  title and the deadline-distance words wait; **the orchestrator** — W3-B's dashboard tells a suspended or closed
  person there is no file; a person is offered state changes on their own file (a class C question).
- **design-v5's own failing test**, unchanged by this merge: `test_script_motion_gate.py` on W2-A's
  `static/js/src/overlay/extras.js` (`requestAnimationFrame`) — identical on design-v5 before the merge; its fix is
  `v54-intfix`'s (`822b3ae`), not yet on design-v5. The gate's check run over every module finds that line and no
  other: the family's modules pass it. `ruff format --check` flags two lines of `tests/frontend/test_design_docs.py`
  that are design-v5's own (not changed here).
- **The full suite** was not run (V5.5: the integration checkpoint runs it). Nothing was pushed to GitHub.
