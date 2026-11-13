# W3-D · The journey «La soglia» — senior review (one pass)

Reviewer label `w3-d-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-d`
at `5860677` (the passage and the rail, the fixes, the notes), from design-v5 `d40f209`. Looked at on the reviewer's own
server from this worktree (127.0.0.1:8886, `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03` — `2026-10-01` for the home's
passage only, gate G3 closed by its own date, no data changed — `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag),
headless Chromium with its own profile and the cache disabled, one browser and one pytest at a time, sessions minted
with `Client.force_login` (no password used, typed or stored) and revoked at the end; the server stopped. No run ended
on a crash. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-d/review/` (`r1` … `r6`, each with its `report.json`;
`perf/`; `aria.json`). Scratch scripts: `C:/tmp/ile_v5_council/.work/w3-d/w3-d-review/`.

**Looked at.** The dashboard's «Mon parcours» for `seed-person` (a file in SELECTION — on threshold A), `qa-person`
(step 2), `qa-doc-person` (step 1) and `qa-fresh-person` (no file); the case file's journey and timeline (`0FEEBAE3A9`,
`E46E03B461`); «Ma situation»'s Stepper; the «Mon parcours» page; the home's passage — × fr / ar × 1440 × 900,
1366 × 768, 1280 × 800, 390 × 844, 360 × 800 (phones emulated), plus 1024 and 834 for the level line's floor, the opened
disclosure, the keyboard, reduced motion and forced colours on the flagship screens, 2× crops for the glyphs. The
statuses the lane's data lacks (training, admin_process, pre_departure, entered, post_entry, suspended, closed) were
drawn by the real presenter and the real component, spliced into a real dashboard page (a scratch file served
same-origin to the browser only). **112 captured loads: 0 horizontal overflow, 0 console errors, 0 CSP reports (the
dev server sends the CSP), 0 responses ≥ 400.** The presenter and the four components read line by line;
`tests/frontend/test_journey_w3_d.py` (29) and `tests/frontend/test_journey_browser_w3_d.py` (10) re-run on
`test_ile_v5_l6`: **39 passed**.

## Verdict: **SHIP_AFTER_FIXES**

The drawing is at the bar. On the console the journey is now one thing: the dashboard's level line, the phone's card,
the case file's dated spine, the timeline and «Ma situation»'s Stepper speak one vocabulary from one sheet — an ink dot
behind, the laguna ring on its wash where the file stands, an open ring ahead, a 2 px line in laguna where the file has
been — and it tells a person where they stand in one look. The level line between «Maroc» and «Italie», crossed by the
stamp and the arch with their jurisdiction captions, passes the swap test without the logo; nothing in it is a stepper
kit (no numbered circles, no ticks, no percentage). SELECTION finally stands on threshold A: the dashboard, the phone
card and the case file agree with the header's chip. The phone's card + «Où j'en suis» is the right answer (what is
true now first, the list one tap away, closed and out of the accessibility tree). Nothing moves at load, reduced
motion is the same still, and Arabic is a true mirror with the dates and the numerals left alone. The public passage
«la linea» is quiet and correct on the home.

No P0: no broken page, no wrong direction, no data or permission change introduced. **Four majors before the merge:**
the shared console CSS passes its hard ceiling (V5.8 sends that merge back); «Mon parcours» — a page on the family's
own list — still draws no journey; a suspended or closed file is told «Vous êtes ici» on step 1; and the consolidation
with W3-F1 (the plan's merge order) is what makes «never a third» true in the product. The rest is polish.

## The gate, checked on the real pages

| Gate item | Result |
|---|---|
| One passage and one rail drawing, never a third | **Console: yes** — `_journey-rail.css` draws `.journey`, `.tl`, `.wstep`; nothing else draws a journey on the dashboard, the case file or «Ma situation». **Product: not yet** — `components.css` §17 `.timeline` (pathways, diplomas, interim index, ecosystem companies, pilot) and `register.css` `.sequence` (Academy, a need, the help desk, the selection) still draw sequences; W3-F1's branch carries its own «la linea» and Stepper (M4) |
| The phone journey as a card + a disclosure | yes at 390 / 360 (and 834 — up to a 56rem component), fr and ar: the current item's glyph and words, «Étape n sur 7» on a step (none on a threshold), «Vous êtes ici», then «Où j'en suis» closed — summary 44 px, a 2 px laguna ring by keyboard, Enter opens it onto the spine; closed, the list is absent from the accessibility tree; at 1440 the closed `<details>` is laid out and its list exposed (`aria.json`) |
| Still at load | yes — 0 animations or transitions from the journey on the dashboard, the case file and «Ma situation». The only movement on these pages is someone else's: L1, the loader's entrance release (once per sign-in, W1-D), and the HealthStrip's `strip-fill` on `qa-person`'s case file (W3-C / W3-E) |
| Reduced motion a true still | yes — `emulateMedia({reducedMotion: "reduce"})` on the three pages: the same stills, 0 animations |
| The numeral / glyph / holder rule | yes — the rail: one phase glyph a column, from the registry; no numeral; no tick (a step behind is a filled dot); no holder (A′). The passage: CSS-counter numerals over open rings |
| SELECTION on threshold A | yes — `seed-person`: eight items, steps 1–3 travelled, the threshold the current item («Phase gérée par un acteur autorisé», «Vous êtes ici»), step 4 ahead; the case file dates the threshold and not step 4, though the trail once reached it |
| No long task | at load the journey runs no script, no observer, no animation (its style and layout ride in the first render — the implementer's traces, not re-traced here); the phone's tap on «Où j'en suis» costs a 63–96 ms task at CPU ×4 (m2) |
| RTL | mirrored: «المغرب» at the reading start, the line from right to left, the thresholds' hairlines and captions on the mirrored side, the spine on the right, the Stepper's phone row from the right. Not mirrored, as they must not be: the glyphs, the dates (21.09.2026), the passage's 01–04, the (symmetric) chevron |
| Level geometry | nodes on one level (spread 0 px) at 1024–1440, fr and ar; no word collides with another; at exactly 56rem (1024, fr) «Accompagnement» runs 3 px into the gutter — invisible |
| §3.1 item 7 — identity carriers | the dashboard and the case file: «La soglia» (the shores, the stamp and the arch, the travelled laguna line); «Ma situation»: the shared vocabulary only — enough for a form |
| Shared CSS (V5.8: before → after, gzip -9 of the committed bundles) | `main.css` 41 880 → 40 599 (−1 281 on every page) · `portal/console.css` 7 072 → 8 956 (+1 884) · `portal/portal.css` 1 975 (=) · `pages/css/pages.css` 4 083 → 4 497 (+414). **Console page types 50 927 → 51 530 B: +603 over the hard ceiling (M1)**; the home 45 963 → 45 096 (−867) |
| Tests · ownership | 29 + 10 passed (re-run here); `check_ownership.py w3-d design-v5`: 9 inside, 8 slice, 18 generated, 7 outside — each justified in DL54-92 for the merge step |

## Major — fix before the merge

**M1 · The shared console CSS passes its hard ceiling.** The console page types (main + console + portal) go from
50 927 to 51 530 B gzip, 603 B over the ceiling recorded at the w3-b merge (DL54-87; the notes measure 598). Under the
owner's V5.8 (appended to V5_5_DELIVERY_MODE.md on 11 October, 19:40) the shared ceilings are hard and a merge that grows
them is sent back — the notes' «for the merge step to record» is no longer on offer. *Fix:* the rail is the journey's
own CSS and three console pages use it. Take `v5/_journey-rail.css` out of `console.css` into a page-only entry (for
instance `apps/portal/static/portal/journey.css` → `css/dist/portal/journey.css`), linked with
`{% block extra_head %}{{ block.super }}…{% endblock %}` on the dashboard, «Ma situation», the case file — and «Mon
parcours» with M2 — as documents, companies, academy and the help desk already load theirs; the console page types
then fall below design-v5's. Report the payload before → after at the merge.

**M2 · «Mon parcours» draws no journey.** The console's «Parcours» group reads «Tableau de bord», «Ma situation»,
«Mon parcours»; the last wears the journey's own glyph (`ile-steps`, the same as the dashboard's «Mon parcours»
section) and opens a page of saved pre-assessments with no journey at all (fr / ar, 1440 / 390). A person who taps «Mon
parcours» to see where they stand does not find it there. The plan lists «Mon parcours» among W3-D's pages (§3.5 item
6); the notes leave it as a proposal to W3-E. *Fix:* draw the component at the page's head when the person has an
active file — `components/journey_rail.html` with `steps = journey_for(active_case(user))` and the label «Où j'en suis»
(the dashboard's component and words: no new copy) — the pre-assessments under it; record `templates/portal/pathways.html`
(W3-E's slice) as a justified path for the manifest — or have the orchestrator write it into W3-E's acceptance list,
not leave it as a proposal.

**M3 · A suspended or closed file is told «Vous êtes ici» on step 1.** DL54-88 keeps V4's mapping for SUSPENDED and
CLOSED. Drawn through the real presenter, both put the ring and «Vous êtes ici» on «Votre situation et votre objectif»
and leave every later step undated (`r2/states-*-c8`, `-c9`). The dashboard never shows these files, but the case file
does — from «Mes dossiers», for the person and for the assignees — with «Suspendu» or «Parcours clôturé» in the
header's chip over a journey that says the file is at its first step. That is the one thing the component exists to
say, said wrong. *Fix (no new copy):* a status with no place on the line gets no current item and no «Vous êtes ici»
(the chip says the state); on the case file the steps the trail reached are done and dated (`journey_with_dates`
already reads them); guard the card in `journey_rail.html`, which prints «Vous êtes ici» even when no item is current;
one test per status. Where a suspended file stopped (a held ring) can wait for the trail contract (JS §7.3).

**M4 · The consolidation with W3-F1 is part of the merge.** «One passage and one rail drawing, never a third» holds on
the pages W3-D draws, not yet in the product: on this branch the pathway pages, the diplomas, the interim index, the
ecosystem's companies page and the pilot still draw `components.css` §17's `.timeline` — broken at 1440 on design-v5
today (below) — and W3-F1's branch carries its own copy of «la linea» (`_interior.css` §5) and of the Stepper
(`v5/_wizard.css`). *Fix:* as planned — when `v54/w3-f1` is on design-v5, merge it and do the notes' «For W3-F1» items
1–5 in one commit (one home for «la linea», the import lines, `_linea.html` → `components/stepper.html`, §17 and
`timeline.html` retired, the Stepper's rules out of `_wizard.css`); re-shoot the door pages and «Ma situation» (fr / ar,
1440 / 390) and re-measure the shared payload (M1). `register.css`'s `.sequence` stays W3-E's to retire.

## Minor — polish

- **m1 · The timeline hides its «now».** The case file's timeline is oldest first inside the inspector, which is sticky
  with its own scroll (756 px tall at 1440 for 1 771 px of content; 656 / 1 839 at 1280): the lit latest event — where
  the file stands — ends about 440 px below the scroller's visible end, and each «Intervenant assigné» says «Acteur
  autorisé» twice (the role as detail, the actor as the same role). Newest first with the first row lit, and the actor
  line skipped when it repeats the detail (the component and the presenter's order; the inspector is W3-E's).
- **m2 · The disclosure's tap is heavier than the notes say.** CPU ×4 on the dev server: the tap that opens «Où j'en
  suis» makes a 63–96 ms task and an 88–128 ms interaction over five runs (a tap on plain text: 40 ms, no task); closing
  it, 78–86 ms (`perf/`). Still a good INP and no regression (V4 laid the list out at every load), but the notes' «≈ 27
  ms at ×4» should say what was measured, and the a11y/perf check confirms it on 8782.
- **m3 · The shores disagree between densities.** On the level line «Italie» stands at the rail's far end, about
  115 px past node 7 where the line stops, while «Maroc» stands over node 1 — and the spine carries the line on to
  «Italie». Draw the last stretch to the rail's end, as the spine does, or set «Italie» over node 7. «Vous êtes ici» on
  its own fourth row floats 110–125 px under its node at 1440 (at step 7 it is pushed to the far end): acceptable, but
  closer reads faster.
- **m4 · «Ma situation» counts three ways.** The Stepper draws 8 questions and the foot says «1 / 8»; the line under the
  Stepper says «0 question(s) renseignée(s) sur 7» (`total = len(PROFILE_FIELDS)`, without the recognition question the
  Stepper counts). One number for one person — W3-E's view and template.
- **m5 · On a threshold the phone card says the phase, not the place.** For SELECTION the card reads «Phase gérée par
  un acteur autorisé · Vous êtes ici» with no rank (rightly). The threshold's caption — «Autorités compétentes :
  décisions administratives», a catalogue string already in the spine — at the card's head would say where that is
  without opening the list.
- **m6 · The wide density leans on one browser behaviour.** From 56rem the closed `<details>` is shown by
  `::details-content { content-visibility: visible }`; that works where the user agent hides a closed details with
  `content-visibility: hidden` (the current HTML spec; Chromium 131+). A browser that supports the selector but hides
  another way would show nothing at the wide width — the card and the summary leave under the same `@supports`. Not
  exercised in WebKit or Firefox (not installed here): check once on Safari 18.4+ and Firefox before the owner's report.

## Seen on the way — outside this area (for the orchestrator; not counted in the verdict)

- **The pathway pages' V1 timeline renders broken on design-v5 today.** `/fr/parcours/salaried_work/`, «Étapes», at
  1440: five numbered circles over columns about 50 px wide, every label split letter by letter («S'ORIE NTER»,
  «PRÉPA RER LA DOCU…»; `r5/`, `r6/`). The same with design-v5's own `main.css` swapped in — pre-existing, not this
  branch. W3-F1 replaces it with «la linea»: check it at W3-F1's merge and in M4's re-shoot.
- **A suspended or closed person's dashboard says there is no file.** `active_case` keeps the active statuses only, so
  the NowPanel falls to «Vous n'avez pas encore de dossier… Commencer le questionnaire» (read in `now_panel`, not drawn
  — no such file in the lane's data). W3-B's; the same truth as M3.
- **The person is offered state changes on their own file.** On `seed-person`'s case file «Faire évoluer l'état du
  dossier» offers «Suspendu», «Procédure administrative en cours», «Parcours de formation en cours» and «Parcours
  clôturé», as `cases/policies.py` says («person (owner): view, and change while the case is active»; main `b3ac2b7`).
  Not exercised. Whether a person may self-declare the administrative procedure — which the journey then draws as a
  fact — is a product-policy question (class C) for the owner.
- **The home shows the passage only while gate G3 is closed.** At the preview's date (3 October) the home carries the
  prescribed sentence and no passage; the owner sees «la linea» at 1 October and, after W3-F1, on the door pages — the
  report should say so.

## Not checked

WebKit and Firefox (m6); a screen reader (the tree read is Chromium's); a real phone; the performance PASS on 8782 (the
tap was timed on the dev server at CPU ×4, with the benchmark lock absent); the consolidated tree (M4 does not exist
yet); text spacing and 400 % reflow (the accessibility check's).

## The lane, cleaned

The four minted sessions revoked on `ile_v5_l6`; the server on 8886 stopped; no browser left running; scratch and
evidence outside every repository.
