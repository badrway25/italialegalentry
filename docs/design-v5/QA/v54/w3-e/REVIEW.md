# W3-E — senior review (w3-e-review)

Reviewer **w3-e-review** (built nothing), 16 October 2026. Branch `v54-w3-e` at `dd0eba7` (base design-v5 `fec37d3`;
design-v5 is now `2ebfed1`). One pass — design, UX and taste together — against the owner's bar («credible alongside
excellent international digital products», V5.1 §96) and the settled direction (plan §3.5 item 7, §3.1 item 7, §1.2,
§1.14; platform.md §3; DL54-130 … 146). V5.5: implement → review once → fix → ship.

**Verdict: SHIP_AFTER_FIXES.** No P0. The family finishes the person's and the organisations' secondary pages as one
workspace with the dashboard, «Mes pièces» and the journey: registers on hairlines, chips through their producers, the
workspace head without eyebrows, the answerable party, the clause, the overlay system's menu and alert dialog. Nothing
falls back to V4's panels, tables of selects or badges. Four majors hold the merge — three on the case file (its first
screen, the next line drawn twice, the history's «Vous» on a mandated reader's screen) and one across the module pages
(irreversible closures without the alert dialog the case file uses). Each is a small change.

## How it was looked at

- Own server 127.0.0.1:8885 from the worktree on `ile_v5_l5` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
  `--noreload`, no preview flag); sessions minted by `Client.force_login` (no password), revoked at the end; one headless
  Chromium at a time, its own profile; the benchmark lock checked before every series (never present).
- 236 captured page loads, plus the interaction, POST, swap, focus, forced-colours and reduced-motion runs: the case file
  as the person, the assigned professional, the administrator and a file on threshold A; «Mes dossiers», the
  pre-assessment; «Mes demandes», a request; «Communications», a letter; «Mes échéances»; the empty states; «Mon
  parcours», «Ma situation»; the company's needs and filter, a need, «Mon entreprise», the forms; the Academy
  (catalogue, mine, course, follow-up, plan); the guichet (person, professional, opening, dispatch); the selection
  (workspace, process, panel, disclosures); the Forum's closed page; the dashboard and «Mes pièces» beside them. fr and
  ar at 1440 × 900, 1366 × 768, 390 × 844 and 360 × 800 for the ten core pages, 1440 and 390 for the rest; 1280 × 800,
  1100 and 1920 on the case file.
- Lane data: the case file's checklist drawn with w3-e-impl-3's seed under the reviewer's own tag «[w3er]» (five lines,
  a linked piece, a message, two dates); one line's state changed through its dialog and put back. All of it removed at
  the end with its audit events (EE167596D4 back to three pieces, no line, «Brouillon»).
- Not drawn live: the bridge's institution and university (their lane accounts were removed by step 2) and the open
  Forum governance (flag closed, G11; its closed page was drawn).
- Evidence (outside the repository): `C:/tmp/ile_v5_council/evidence/v54/w3-e/review/` — `b/` the core pages at four
  sizes, `c/` the rest, `d/` breakpoints, forced colours and reduced motion, `i/` the menu and dialogs, `p/` the POST
  round-trip and the whole-row links, `swap/`, `f/` focus.

## What holds

- **Health.** Every capture 200 (the Forum's closed page 503 by design), 0 CSP report, 0 console error (the 503's own
  status line apart), 0 horizontal overflow, one h1, no eyebrow repeating a level, no badge, no tracked capitals, no
  duplicate id, ≤ 3 corners in every first viewport, one raised plane (the NowPanel) with its one shadow. Text under
  14 px at 390: 0 % on the registers, 6–7 % on the case file, 17 % on «Ma situation».
- **The case file in the settled order**: the head (reference in ILE Mono, chip, since when) → the journey → the
  NowPanel → «Exigences» as register rows (who answers, the source in ILE Mono, the chip, the date in its register) →
  «Pièces du dossier» with «il registro» → the answerable parties → the feed beside it from 80rem. V4's five panels,
  inspector scroll, eyebrow and table of selects are gone.
- **C-5 / C-6 are well built.** «⋮» is named «Actions» and described by its line. The menu opens on Enter. The
  alertdialog is `aria-modal`, described by the line and its consequence, and opens with «Annuler» focused. Tab stays
  inside (10 of 10). A press on the scrim never closes it; Esc does, and the focus goes back to «⋮». The phone sheets
  work in ar and fr. Without script the popover opens natively and the dialog shows in place. The POST returns to
  `#line-<pk>` with a ring on the row and «La ligne a été mise à jour.». The file's dialog states the closure's
  consequence and the suspension's rule. Permissions, the state machine and the audit trail are untouched (diff read:
  `can()` / `require()` unchanged, the service records the event).
- **Requests, messages, deadlines.** The head; the band, one count per event (a late date is not also «à venir»); rows
  whose whole surface leads to the record (a press on the date or the seal opens it); chips through producers (late
  azione, soon attesa, cancelled nullo — red never means late); «Non lue» as a word with the ink dot and the weight.
  «la lettera» is a quiet, credible page.
- **The company.** The register's counts are its filter (Tous · À faire · En cours · Clos, `?état=`, an unknown value
  filters nothing), one space rail, no chart, no V1 band.
- **RTL.** Correct mirroring everywhere looked at (rails, rows, chips, primaries at the inline end, flipped arrows,
  the dialogs' foot); French data isolated in its own direction.
- **CSS (gzip -9).** `main.css` 35 483 → 31 906 B on every page; main + console + portal 44 196 → 40 140 B on every
  console page (design-v5 `2ebfed1` → `dd0eba7`). The case file is 45 968 B, or 48 039 B with the overlay panels where
  a dialog is drawn. The V5.8 ratchet holds.
- **Targeted tests** on `test_ile_v5_l5`: `apps/cases` plus the frontend gates (bundles current, template comments,
  chip registry, state chips, O14, overlays, static pipeline) — 378 passed, 3 skipped (no rule in force).

## Blocking

None.

## Major

### M1 · The case file's first screen holds no act at 1280–1440 and hides «what next» on a phone (LA-9)

Measured in fr for `qa-doc-person` and `qa-person`: the descriptive spine is 460 px tall and opens the main column. The
NowPanel's title lands at y 762–790 and its primary at y 895 (987 for `qa-person`).
- 1366 × 768: the title is cut by the fold and the primary is 127 px below it. The first screen is the head and the
  journey.
- 1280 × 800 and 1440 × 900: the primary is below the fold, or on it with 5 px showing.
- 390 × 844 and 360 × 800: the spine takes 481–521 px and the NowPanel's title sits behind the action bar. The bar's
  «Continuer» does not say what it continues.

On the dashboard the same NowPanel's primary sits at y 423. LA-9 names the case file: the first viewport answers
where / what next / what is missing / who / what changed, and holds the one primary, at 1440, 1366 × 768 and 390.

**Fix.** Keep the order (journey → NowPanel) but draw the journey compact. Above 56rem use the console's level line;
below it use the card with the «Où j'en suis» disclosure. These are W3-D's own two forms, the ones the dashboard and
«Mon parcours» draw (`descriptive` off), and the dated history stays in «Où en est votre demande» beside it.
Alternatively, move the dated spine to the side column above the timeline from 80rem and fold it under the card on a
phone. Re-measure: the NowPanel's title and primary within 768 px at 1366, and the title clear of the bar at 360 × 800.

### M2 · The next line is drawn twice, and the page's one primary scrolls to the copy

When the next action is a checklist line (the usual case, since lines are the file's backbone), the NowPanel draws it
with its chip, date and holder, and «Exigences» draws the same row again under the next heading. «Continuer»
(`#line-<pk>`) only scrolls to that copy, whose act hides behind «⋮»: three more presses after a search for the
trigger, and after a pointer press no ring shows which row it landed on. The same presenter already draws a piece once
(`case_pieces(skip=…)`, W3-B's rule); `case_lines` has no skip.

**Fix.** Draw the line once. Skip the NowPanel's line in «Exigences» as the pieces do (the count «1 sur 4» unchanged).
Where the reader may move the line, make the NowPanel's primary open that line's alert dialog directly
(`href="#line-<pk>-state" data-overlay-open`, its dialog still laid out). Otherwise draw no primary, as for a mandated
reader.

### M3 · The history says «Vous» to a mandated reader for what the person did

`presenters.timeline(case)` labels the person's acts «Vous» whoever reads the page. The assigned professional sees
«Ligne mise à jour · En cours — Vous» for the person's change; the administrator sees «Vous» on the person's three
events. On a feed read from the audit trail this names the wrong author, on the page whose own rule is «a mandated
reader is told … in nobody's voice» (DL54-142). The defect is pre-existing in V4, but the redraw kept it.

**Fix.** Pass the reader (`timeline(case, reader=request.user)` — W3-D's presenter slice, a justified extra path).
Label the person's acts «Vous» only for the person, and «La personne» (`ResponsibleActor.PERSON`, already in the
catalogue) for everyone else. Add a test that a professional's view carries no «Vous».

### M4 · Irreversible closures skip the alert dialog the case file uses

Closing a case file goes through the overlay system's alert dialog with its consequence («Un dossier clôturé ne se
rouvre pas…»). The three other irreversible acts this family draws are one-press submits:
- the selection's «Clore le processus» (the authorised actor; «Un processus clos ne se rouvre pas»);
- the guichet's «Clore définitivement» for the professional;
- the same button for the person («Une demande close n'est pas rouverte»).

That is one family with two grammars for the same consequence. Plan §3.5 item 7's gate is «staff consequence dialogs
on the modal», not the case file's alone. The selection's evidence table also still updates each row with a select
and «Mettre à jour» — the V4 pattern C-5 retired on the case file.

**Fix.** The three closures open `components/dialog.html` with `kind="alert"`: the panels' page-only sheet linked where
drawn, «Annuler» marked `data-overlay-safe`, the consequence sentence (already in the catalogue) as the dialog's
description, and the reason field inside. Move the evidence rows to the row menu and dialog when the staff surface is
next touched, or record them as design debt beside the dispatch desk.

## Minor

1. Wrapped fact lines leave a «·» at the end of a line (the needs register, the Academy, «Mes dossiers», the queue):
   use a separator that wraps with the next item, or a gap without dots.
2. On a phone the case rows' «⋮» floats beside the words, because the words' column is sized by its content. It jumps
   from x 185 to x 333 between rows at 360 instead of keeping a stable column at the inline end.
3. The Academy's domain filter wraps to five rows at 390 (F19's symptom). Below 52rem use the platform's one-control
   filter (W3-C's sheet) or a single scrolling row.
4. On the pre-assessment, «Ce qui a produit ce résultat» and «Les textes…» run at the full 1 130 px (about 160
   characters a line) where the rest holds 36rem.
5. The feed shows «Ligne mise à jour» four times without saying which line. The audit metadata holds the item, so its
   own words could say it with no new copy. Long chips also wrap to two lines in the 1/3 column at 1280–1440 («Phase
   gérée par un acteur autorisé»).
6. RTL: the note's «—» sits inside the `dir="auto"` isolate and lands on the far side of «Sportello Unico…» on Arabic
   pages; put it outside the span. A wrapped French h1 on an Arabic guichet page aligns left while the deadlines'
   titles align right; pick one rule.
7. Voice on a mandated reader's screen beyond M3: «Vous êtes ici», «Où en est votre demande», «Ce qui vous a été
   indiqué», the assessment's empty sentence, and «au titre d'un mandat daté» for an administrator. These belong to the
   B1 copy packet.
8. One counter per event: the rail's «Communications (2)» sits beside the band's «2 communications non lues» (D17 says
   «a dot on the rail»; W3-A's rail, a hand-off). The guichet's band is a sentence («5 demandes en cours.») where the
   other registers draw the figure.
9. States off the chip grammar: an Academy plan's state is plain words (no producer for `academy.PlanStatus`). The
   professional's queue paints «Réponse disponible» in azione for a reader with nothing to do; the registry is per
   state, so this is a note for W1-C.
10. Swap test (TS §19.3 B, with the lock-up covered): «la lettera» rests on the team's mark, which is the brand's own
    glyph. The guichet's opening form and the pre-assessment carry nothing at rest (the notes call them «weak»). Name
    one carrier for each.
11. At the merge: design-v5 `2ebfed1` (sec-f7) draws a held file's reason in the NowPanel, so the case file's
    suspension notice would repeat it. Keep one (DS 2026 §11.7: «the reason drawn once»).

## For the merge step

- `check_ownership.py w3-e design-v5`: 58 inside, 12 slice, 29 generated, 30 outside → FAIL until the manifest names the
  justified paths (the notes list them for steps 1–3).
- design-v5 has moved to `2ebfed1` (sec-f5, intfix, sec-f7). They meet this branch in `apps/portal/services.py`,
  `apps/cases/*`, DS 2026 and the decision log.
- The lane at the end of the review: the «[w3er]» data removed, 10 sessions revoked, 8885 stopped, no browser left.
