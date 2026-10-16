# W3-C — Document workspace and status — notes

Family W3-C of the V5.4 plan (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 5, §1.2, §1.14, §1.15; the platform
map `C:/tmp/ile_v5_council/.work/v54-plan/platform.md` §3, §6 item 0), worked in the owner's delivery mode (V5.5:
implement → review once → fix → ship). Branch `v54-w3-c`, worktree `C:/tmp/ile_wt/v54-w3-c`, started from **W3-B's
branch** `v54-w3-b` (`41a725a`) while W3-B is in review. Evidence outside every repository:
`C:/tmp/ile_v5_council/evidence/v54/w3-c/` (E/ below). Decision log: DL54-82 … DL54-85 (numbered after this branch's
DL54-81; renumbered after design-v5's own at the sync merge).

## Step 1/2 — «Mes pièces» V5.2: the register, the row, the status (implementer w3-c-impl-1, 11 October 2026)

**Lane.** Lane 9: dev server 8789 from this worktree on `ile_v5_l9` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), pytest on `test_ile_v5_l9`, one pytest and one headless Chromium of
mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-c-impl-1/`). Signed-in pages through sessions
minted with `Client.force_login` by a scratch script outside the repository (no password used, typed or stored),
revoked at the end. Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a crash. NB: with `--noreload` the
cached template loader keeps the first template it read — the server is restarted after every template change.

**The static pipeline came first.** The brief asks for the page partials' imports «in the COLLECTED tree per DS 2026 §2,
guard tests/frontend/test_static_pipeline.py» — both exist on design-v5 (the steward's static fix) and not on W3-B's
branch. The three commits were cherry-picked with `-x` (`2a94951` → `546a51e`, `822c82d` → `a2da180`, `6705f21` →
`070c5c1`); one conflict in `tests/frontend/test_console_shell_w3_a.py`, resolved by keeping W3-B's form (the light sheet,
the shell, then each family's partial) with the collected path. They are design-v5's own changes: they merge cleanly
at the sync, and they show as «outside» in an ownership check against `41a725a` until then.

**Personas** (the lane's clone of the QA data): the person with a case — `qa-person` (`E46E03B461`: seven pieces in the
seven states, dates on all, the Conditions NOT accepted, so every open piece's act is the gate's) and `qa-doc-person`
(`EE167596D4`: a piece to replace, two filed, no dates, the Conditions accepted); the company account —
`seed-company` (and `qa-company`): no file, the register's empty sentence.

### What was built

- **The presenters** (`apps/documents/presenters.py`; DL54-82, DL54-83):
  - **F8** — `urgency` runs only while the piece is OPEN; a filed, in-review or valid piece's date is drawn calm (no
    word, the calendar). On the QA data the valid passport (due 21.10.2026) lost its «upcoming» mark.
  - `register_groups` — the three groups by whose move it is: to act (an open piece the person answers for) · in hand
    (everything else not settled) · settled (valid). The strip's runs and the collection's groups are the same sets;
    the dashboard's ledger follows the same rule (W3-B). Words: «À faire», «En cours», «Valide» (catalogue).
  - `next_piece` — the page's one act: T1's piece (`cases.services.next_action(case, reader=user)`) when the reader can
    act on it, otherwise T1's precedence over the open pieces the reader acts on (overdue, nearest date, register's
    order). On `qa-person` it is «Acte d’état civil légalisé», 05.11.2026 — the dashboard's NowPanel names the same.
  - `row_act` — one act per row, only on an OPEN piece the reader may file: «Déposer la pièce» / «Remplacer la
    pièce» (with their glyphs); None elsewhere — no «Consulter». `next_act` — the strip's act: the row's own, or, where
    the Conditions gate blocks the filing, «Consulter» on the piece's page with «Acceptation des Conditions
    d’utilisation requise.» under the date (W3-B's review M1, carried over: «Accepter les Conditions» led to a page
    with nothing to accept — the acceptance flow waits on G1; the rows say «Bloqué»). `state_filters` in
    `STATE_ORDER`. `record_language` isolates a French title on an Arabic page. `can(user, "file", …)` asked once per
    row instead of three times.
- **F13** (`apps/portal/services.py`, `present_deadline` only): «En retard» → `overdue` (azione, terracotta, the disc
  with clock hands), «Bientôt» → `soon` (attesa, amber, the dashed ring). Before: `error` / `warning`, a refusal's
  garnet for lateness. The deadlines page's template (W3-E's) draws the chip through `badge.html` → the registry.
- **The register** (`templates/documents/partials/register.html`, for `/fr/espace-reserve/mes-documents/` and
  `/documents/`): the file's head (title, reference in ILE Mono, search at the inline end — in the card layout from
  thirteen pieces on); **«il registro»**, the screen's one raised plane: three runs (20/28 count, one 16 px mark per
  piece, a link to the group), «Votre prochaine action» with the piece, its date and **the page's one primary**, the
  locked count sentence; the **state filter** in `STATE_ORDER` (a state with no piece is a word) and, below 52rem of
  register, **one 44 px control + a bottom sheet** (native `popover`, «Fermer», 320 / 200 ms, still under reduced
  motion); the **collection** in the strip's three groups — six columns on a subgrid, five with the actor under the
  title from 52rem, cards below, by the register's own width (container query `wscase`); the register's caveat 16 px
  under it.
- **The row** (`templates/components/document_row.html`): six zones and the note as the footer; the title's link
  stretched over the row (z 1), the act above it (z 2) and described by the piece's title (W-3); no row menu, no
  «Consulter»; «Bloqué» beside the chip where the Conditions gate blocks, and no act there (no button that promises an
  acceptance nobody can make yet); the date's glyph in a 20 px seat (`alarm-clock` drawn at 20 px, its floor — W1-B's
  item).
- **The files**, named for what they are (`_table.css`): «Tous les fichiers de votre compte», «Documents de mon
  organisation», «Autres fichiers déposés» — real tables, the whole file name the download link, stacked under 40rem of
  their region; each «Supprimer» described by its file (W-3).
- **The piece** (`templates/documents/requirement_detail.html`, `templates/documents/partials/depot.html` — new, one
  markup drawn in two places; DL54-84): the order of need — the state, its rule and this piece's reason; the deposit
  while the piece is open (after the deposits otherwise); what is asked; the source; the deposits («Télécharger»
  described by its version). The head names the file by its reference; V4's case band is not drawn there (200 px on a
  phone before the state). The upload page and the gate page on the console's header (the upload page keeps its line
  on a phone: it says what the page is for).
- **The sheets** (DL54-84): `apps/portal/static/portal/v5/_workspace.css`, `_table.css`, `_depot.css`, imported by
  `apps/documents/static/documents/documents.css` (the five documents pages) as `../portal/v5/_x.css` — never by
  `main.css` or `console.css`. Tokens only, logical properties only, no animation; one shadow value at rest; corners
  4 · 8 · full (the sheet's 12 only while it is open).
- **Legacy rules deleted** (`static/css/v4/workspace.css`, in main.css): the SegmentedControl, the search,
  DocumentCollection / Row / Card with the row menu, their forced-colour and touch lines, the portal page's files
  table rules (−12.9 KB raw). `register.css`'s register and entry stay (eight other page families draw them).
- **console.js**: the register's search hides a group whose rows it hides (four lines in the search block).
- **Docs**: DS 2026 §11.8 «Mes pièces», the §10 entries of `document_row.html` and `health_strip.html`, §2's row of
  `v4/workspace.css` (weight regenerated by `scripts/regen_design_inventory.py --write`, 45.7 → 33.2 KB); DL54-82 … 85.

### The gate (plan §3.5 item 5 and the brief), measured

Lane 8789, `qa-person` / `qa-doc-person` / `seed-company`, fr and ar (E/r3, E/r4, E/r5, E/final; the probe:
`.work/w3-c/w3-c-impl-1/probe.js`).

| Item | Result |
|---|---|
| the first card's title at ≤ 700 px at 390 × 844 | **692 px** (fr), 660 px (ar) on `qa-person`, whose strip carries the Conditions gate's line; 624 / 628 px on `qa-doc-person`; 650 px before the gate's line was added |
| the first object in the first viewport at 390 and 360 | yes — the first piece's title above the bottom bar at 390 × 844 and 360 × 800, fr and ar (the strip's primary at 395–439 px at 390) — browser test |
| ledger counts = group counts | equal on every page (presenter and rendered HTML; the dossier fixture: 4 · 3 · 1 = 8) — test |
| entries follow `STATE_ORDER` | expired, invalid, missing, to replace, in review, filed, valid — the marks in that order — test |
| a filed piece due tomorrow reads calm | no urgency, no word, the calendar — test |
| no `badge--*` on the console pages owned | 0 on the register, `/documents/`, a piece, the upload page and the deadlines page — test |
| edges and hatch ≥ 3 : 1 | the broken (dashed, attesa) chip edge **3.96 : 1** against the sheet, 3.42 against the chip; the ledger marks 5.98 · 7.17 · 16.23; the 3 px rule terracotta. No hatch is drawn on these pages any more (the HealthStrip left the register; it stays on the case file, W3-E) |
| a colour-vision check | deuteranopia, protanopia, tritanopia, achromatopsia (CDP emulation, E/r5/cvd-*.png, `cvd-board.png`): every state stays distinct by its mark (clock hands · cross · arrows · dashed ring · half disc · ring and dot · plain disc) and by its edge style; amber / terracotta and terracotta / garnet pairs are told apart by shape |
| the whole row as the target | **0 dead probe points of 42** at 1440, 1280, 1100, 390, 360, fr and ar (0 / 16 on `qa-doc-person`) — browser test |
| the register at 6 / 5 columns, then cards, by its own width | 1440 → six (register 70.5rem), 1280 and 1100 → five (60.5rem), 768 / 390 / 360 → cards — browser test |
| controls named by their piece (W-3) | every act `aria-describedby` its piece's title; no two controls of the collection share a name and a description — test |
| 16 px fields under a coarse pointer (W-4) | every typed field 16 px (the foundation's rule, W1-A); the file control is the browser's own button (13 px, takes no typed text) — browser test |
| the files table below, named for what it is | yes, three real tables |
| the one primary, with its piece and its date | one `btn--primary` per page, in the strip, `aria-describedby` the piece, its date and «En retard» / «Bientôt» beside — test |
| nothing moves at load · overflow · errors · CSP | 0 animations; 0 px overflow from 320 to 1440 (fr, ar); 0 console errors; 0 CSP reports on every capture (the final set: 40 captures — the register, the company's register, `/documents/`, a piece, the upload page, the deadlines page — fr and ar, 1440 · 1280 · 1100 · 390 · 360; E/final/report.json) |
| reduced motion · forced colours | the page still under reduced motion (nothing moves at rest anyway; the sheet appears and leaves at once); under forced colours every edge is drawn — the strip (its transparent edge turns CanvasText), the collection, the rows, the group's 3 px rule — and the chosen filter entry is outlined in Highlight (E/r5/fc-*.png) |
| text under 14 px at 390 | 2 % of the characters (fr), 0 % (ar) |

### §3.1 item 7 — the screen's identity carriers

- **«Il registro»** — the strip's runs and their marks: the colour is the group, the shape is the state.
- **«I cerchi»** — every state a chip with its mark; «En examen» in lapis; «Valide» in ink, no check (O14).
- **«Il lume»** in the rail (W3-A); the page's one raised plane carrying the one act (as the dashboard's NowPanel).
- **ILE Mono** — the file's reference in the file's head and in the piece's head.
- The swap test: with the logo removed, the night rail with its lit disc, the three-run ledger of state marks and the
  terracotta rule of the group that asks something of the person still say ILE; the silhouette is not «table + pill
  badges»: one raised strip, everything else flat under hairlines, rows that open as a whole.

### The CSS weight

gzip −9 (Python's `gzip.compress(…, 9)`, DL54-73): `dist/main.css` 41 802 → **40 470 B** (−1 332, every page);
`dist/portal/console.css` 7 012 and `dist/portal/portal.css` 1 954 unchanged. **The console page types' three sheets
50 768 → 49 436 B — 571 B under the ceiling of DL54-73 (50 007 B)**, which W3-B left 761 B over. The documents pages'
own sheet `dist/documents/documents.css` 1 172 → **4 623 B** (the three page partials, one bundle for the five pages);
the documents page type 51 940 → 54 059 B in all (+2 119). DL54-85 reports it for the merge step.

### Performance (a smoke on the lane, not a benchmark)

The lane's dev server (uncompressed, DEBUG), headless Chromium, `qa-person`, five cold loads after a warm one, the
machine shared with other lanes' test runs (`.work/w3-c/w3-c-impl-1/perf.py`; E/perf/perf.jsonl):

| Page | CPU | LCP median (range) | CLS | Longest task median (max) | TBT median |
|---|---|---|---|---|---|
| «Mes pièces» fr 1440 | × 1 | 364 ms (316–424) | 0 | none | 0 |
| «Mes pièces» ar 1440 | × 1 | 388 ms (316–432) | 0 | none | 0 |
| «Mes pièces» fr 390 | × 1 | 376 ms (344–400) | 0 | none | 0 |
| «Mes pièces» ar 390 | × 1 | 416 ms (372–428) | 0 | none | 0 |
| «Mes pièces» fr 390 | × 4 | 872 ms (648–2 084) | 0 | 142 ms (247) | 147 ms |
| «Mes pièces» ar 390 | × 4 | 1 100 ms (952–1 252) | 0 | 197 ms (278) | 240 ms |
| the dashboard fr 390 (reference, same lane) | × 4 | 1 040 ms (768–1 792) | 0 | 134 ms (183) | 147 ms |
| the dashboard ar 390 (reference, same lane) | × 4 | 1 016 ms (856–3 032) | 0 | 144 ms (236) | 152 ms |

No layout shift, nothing over 50 ms unthrottled; at CPU × 4 the French register costs what the dashboard costs and the
Arabic one about 50 ms more in its longest task — the first render's style and layout of the whole document (the
container query and the three subgrids, DOCUMENT_WORKSPACE §16.6 measured the same order on the comp). Not a
regression the smoke can show against V4 (V4 is not served on this lane); the formal measure on 8782 is the
Performance Lead's.

### Tests run (targeted, V5.5 — not the full suite)

One pytest and one browser of mine at a time, on `test_ile_v5_l9`; no run ended on a crash.

- **The family's own** — `tests/frontend/test_documents_w3_c.py` **26 passed**; `tests/frontend/test_documents_browser_w3_c.py`
  **19 passed** (browser, `-rs`, 0 skipped), on the final tree.
- **Guards and the documents app** — `apps/documents`, `test_documents_w3_c.py`, `test_state_chips_carry_a_register.py`,
  `test_o14_lint.py`, `test_chips_registry.py`, `test_chips_cards_w1_c.py`, `test_design_docs.py`,
  `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_static_pipeline.py`,
  `test_css_tokens_exist.py`, `tests/i18n/test_rtl_static.py`, `test_v4_tokens.py`, `test_v5_tokens.py`,
  `tests/test_regen_design_inventory.py`: **1 090 passed, 0 failed** (after the retargets below); after the Conditions
  gate's change, `apps/documents` with the guards again: **511 passed**.
- **The console around it** (`-m "not browser"`) — `apps/portal`, `apps/cases`, `apps/companies`,
  `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits included),
  `tests/frontend/test_dashboard_w3_b.py`, `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`,
  `test_layout.py`, `test_icons.py`, `tests/i18n`: **922 passed, 3 skipped** (the intake suite's own: no rule in
  force), 0 failed, in 34 min.
- **Browser** (`-m browser`, `-rs`) — `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`,
  `tests/frontend/test_browser_chips_w1_c.py` (the showcase's filter legend: the documents sheet now draws it),
  `test_console_shell_browser_w3_a.py` (the documents pages' title on the frame's edge), `test_console_phone_browser_w3_a.py`,
  `test_dashboard_browser_w3_b.py`, `test_documents_browser_w3_c.py`: **152 passed, 0 skipped**, 0 failed, in 20 min.
- Not on this branch, so not run: `tests/frontend/test_overlays.py` and the overlay browser tests (W2-A's, unmerged).
- **Retargeted, intent kept**: `apps/documents/tests/test_requirement_views.py` (the register is a collection of rows
  and the row is the link; one blocked row, counted on the rows; the Conditions gate said on the row and in the
  strip), W1-A's console partials guard in `tests/frontend/test_v5_tokens.py` (DL54-84). Ruff clean on every changed
  Python file; every changed file LF.

## Items handed to W3-C — answered

- **W1-B — `.doc-row__due-icon` is 16 px and `alarm-clock`'s floor is 20.** Done: every date's glyph stands in a 20 px
  seat; `alarm-clock` (overdue) is drawn at 20 px, `calendar` and `clock` at 16 in the same seat, so a column's dates
  share one edge (`_workspace.css` §4). **«the identity `document` disc on every row (Q1 / Q4, the owner's)»**: the V5.2
  row has no identity disc — `document` is «Mes pièces»' own glyph (DL54-33); the row's first zone is the piece's title.
- **W1-C — «En retard» drawn as a refusal.** Done: F13 (`present_deadline` → `overdue`, azione), tested on the
  deadlines page. **`SCAN_BADGES` beside the registry**: the documents pages draw no scan state from it — the files
  tables show none, and the piece's versions say the antivirus in words (`antivirus_state`); the one consumer left is
  the bridge's documents card (`portal.services._documents_card`, W3-B's) → «For W3-B». **«the third row's chip off its
  column»**: gone — one subgrid, one x per zone on every row (state, actor, date measured on one x at 1440).
  **The deadline's text styles of DS V5 §10.2**: drawn (`.doc-due` on the deadline tokens). **The count pill**: the
  group heads carry their count as text after the word, no pill (a pill would be a fourth form for a figure the strip
  already gives).
- **W3-A — the documents pages' search field corner (6 px).** Done: the search is W1-C's `.input` (4 px); the documents
  pages draw 4 · 8 · full (the probe: three radii on every capture at rest).
- **W3-B — the documents page's primary through `next_action(case, reader=user)` when it is a piece (T1's third
  screen).** Done: `next_piece` (DL54-82); the NowPanel and the strip name the same piece on the QA data. **The deadline
  kinds (F13)**: done. **The `compact` branches left in `document_row.html` and `health_strip.html`**: the row has none
  any more; `health_strip.html` is drawn by the case file only now (`bare`), its `compact` documented as uncalled —
  it goes with W3-E's redraw of the case file (not this slice). **Panel, ContextHeader and HealthStrip leave
  `v4/workspace.css` with their last consumers**: «Mes pièces» and the register no longer draw Panel or HealthStrip;
  they keep the workspace head (`ws-head`), as the dashboard does.

## For W3-B (not edited here — W3-B's files)

- `portal.services._deadlines_card` maps `error` → `overdue` itself; `present_deadline` now emits `overdue`: the mapping
  is a no-op — harmless, removable.
- `portal.services._documents_card` (the bridge) still draws the scan state through `SCAN_BADGES` (`error` → `warning`
  → attesa, `clean` → `success` → conforme) where the registry says azione and neutro (`documents.ScanStatus`,
  DL54-52): pass the registry's producer and value to the card item instead, then `SCAN_BADGES` leaves.
- `_dashboard_pieces` could read `documents.presenters.register_groups` (the same partition, one function) instead of
  its own three comprehensions; the rule is identical today.
- F8 reaches the dashboard's list through `register_for_case`: a filed piece due soon no longer says «Bientôt» there
  either — consistent with the register.

## For the merge step

- **Paths outside the slice** (DL54-85): `templates/documents/partials/depot.html` (new),
  `apps/documents/tests/test_requirement_views.py` (two pins retargeted), `tests/frontend/test_v5_tokens.py` (the
  partials' guard), `templates/dev/showcase.html` (loads the documents sheet), `static/js/src/console.js` (the search
  block). Against `41a725a` the check also lists the cherry-picked static pipeline's files (design-v5's own).
- **Conflicts to expect with W2-A** (the overlay system, not merged yet): `templates/components/document_row.html` —
  W2-A put the row menu on its popover; W3-C removes the row menu (D2): keep W3-C's file. `static/css/v4/workspace.css`
  — W2-A deleted the row popover's rules, W3-C deleted the whole section: keep the deletion. `static/js/src/console.js`
  — W2-A deletes the row menu's placement block (2b), W3-C touches only the search block above it.
- The documents page type's CSS ceiling, as measured (DL54-85); DL54-82 … 85 renumbered after design-v5's own.

## Copy packet for the owner (B1 item 3 — listed, never written)

No new microcopy: every word on the documents pages is a catalogue string (tested). The V5.2 comp's proposals, for the
copy review (O43) — French drafts only; the team never translates Arabic:

1. The group words and their glosses: «À vous · En cours · Réglées» — «à fournir ou à remplacer · chez un tiers ou en
   examen · rien à faire» (D3; the build uses «À faire · En cours · Valide»).
2. «Prochaine pièce à fournir» for the strip's next act (the build uses «Votre prochaine action», the NowPanel's).
3. «Rien à fournir pour l’instant.» (the build uses «Aucune action ne vous est demandée pour l’instant.»).
4. A deadline's distance in words: «dans %(n)d jours», «demain», «aujourd’hui», «en retard de %(n)d jours» (D11; the
   build uses «Bientôt» / «En retard»), and «Sans échéance» for a piece with no date (the build draws nothing).
5. The column header «Pièce» (the build uses «Pièce demandée»); «Autres états» for the states with no piece (the
   build draws them as words).
6. The caption's third clause (D4): «4 en attente» counts the open pieces, a set no run shows — end the caption at
   «1 sur 7 validées», or let its third clause name a run.
7. «La personne» or «Vous» in one's own register (D5); two durations on one row — the piece's validity and the
   deadline's distance (D6).
8. The Dépôt's words: «Choisir un fichier», «Choisir un autre fichier», one vocabulary for the two routes (D12); the
   throttle's sentence and its «quelques minutes» against a fixed hour (D10).

## What is left, and whose

- **W3-C step 2**: the preview drawer (a non-modal panel beside the list on desktop, a sheet on a phone; the head
  filled at 0 ms from the row, the body an asynchronous fragment under L3; `?état=` kept, `replaceState` on swaps) and
  the filter sheet on `overlay.js` once W2-A has merged; the Dépôt's eleven answers composed in place (the JSON answers
  of `views.py`, IP S7) with the ready, refused-by-the-server and throttled states.
- **W3-E**: the case file's band (`portal/partials/case_header.html`, V4's uppercase labels) and the HealthStrip's last
  consumer; the deadlines page's template (`templates/portal/deadlines.html` draws the F13 chips already).
- **The Performance Lead**: the documents pages on 8782 under the lock (the container query's layout cost, DOCUMENT_WORKSPACE
  §16.6, measured here only as a smoke).


## Step 2/2 — the Dépôt, the piece, the deadline registers, the preview drawer and the filter sheet (implementer w3-c-impl-2, 11–12 October 2026)

**Two sessions, one label.** The first session (11 Oct, 19:00–22:06) built the Dépôt, F13 and the deletions, synced
with design-v5 and rehearsed the drawer and the sheet on a scratch merge of W2-A (a worktree outside the repository's
own, `.work/w3-c/w3-c-impl-2/wt`, scratch branches `w3c-impl2-scratch` and `w3c-impl2-trial2` — never pushed, never
merged); it stopped at the session limit before its measures and these notes. The second (11 Oct 23:20 → 12 Oct
03:00) checked that work and fixed what it had missed, waited for W2-A's tag (`v54/w2-a`, on design-v5 at 01:39),
merged design-v5, carried the drawer and the sheet, measured the whole area and wrote this section. DL54 numbers: W3-C's
six entries are **DL54-96 … DL54-101** after this sync (written DL54-82 … 87, then 94 … 99 on the branch); this step adds
DL54-102 … DL54-104.

**Lane.** Lane 9 as in step 1: dev server 8789 from this worktree on `ile_v5_l9` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); pytest with `TEST_DATABASE_URL=…/test_ile_v5_l9`; one pytest and
one headless Chromium of mine at a time, profile `C:/tmp/ile_v5_council/.profiles/w3-c-impl-2/`; sessions minted with
`Client.force_login` (`.work/w3-c/w3-c-impl-2/sessions.py`; no password used, typed or stored), revoked at the end. A
persona of the step's own on the lane clone, `w3c-depot@example.test` (an unusable password; three pieces, three
deadlines), so the live deposits never moved the QA personas' data. Never 8780, Chrome 9222 / 9223. No browser run
ended on a crash. Scratch: `.work/w3-c/w3-c-impl-2/` (and `carry2/`); evidence: `evidence/v54/w3-c/s2/` (E2/ below).

### What was built

- **The Dépôt's JSON answers** (`apps/documents/views.py`, the slice «the Dépôt's JSON answers, if needed», IP S7;
  DL54-100): the same form to the same two endpoints with `X-ILE-Depot: 1`; each of the eleven answers of
  DOCUMENT_WORKSPACE §11.1 goes out as `{answer, message, …}`, always a 200 (Chrome logs every 4xx of an XHR as a console
  error), never cached. The road without script is untouched (redirect and message, the 429 page, the Conditions page at
  403); the validation chain, the size limit, the MIME and antivirus checks, the storage, the throttle and the
  permissions run the same lines on both roads (tests: an intruder meets the same 404, a third party the same 403).
- **The Dépôt** (`templates/documents/partials/depot.html`, one markup for the piece's road and the loose road;
  `static/js/src/depot.js`, imported by `console.js` where a Dépôt is drawn; `_depot.css`): the native field (the whole
  Dépôt without script), the zone that keeps the real input inside it, the client guards read from the server's own
  limits (`presenters.deposit_rules`), the transfer with a real `<progress>` and «Annuler», and **the eleven answers
  composed in place** — a refusal on the file's row (the double rule of «rifiuto», the server's sentence), a date already
  past under its field, the throttle as a notice with «Déposer» kept as the retry, the Conditions gate in place of the
  form, a filing as the piece read again with its answer under the new state (the filed state's mark drawing itself, no
  check), the network or the server in error. Two live regions outside what a refresh replaces.
- **The piece and the gate page on the same grammar**: `requirement_detail.html` in the order of need with the answer
  slot under the state, «Télécharger» keeping the drawer open (`data-overlay-keep`), and a record's own words (the
  detail, the source, the responsible's note) isolated with `dir="auto"` on the reading edge — French data on an Arabic
  page had drawn its final period at the wrong end (seen in the drawer's body); `terms_required.html` the Dépôt's gate (the
  sentence and its link in the dashed frame of a shut door); `upload.html` the loose road on the console's header.
- **F13 on every page that draws a deadline register** (DL54-101): the case file's checklist, dates and next step
  (`v4/workspace.css`), the console's next action and the portal tables' late rows (`portal.css`) take the deadline tokens
  («soon» attesa, «overdue» azione) instead of a refusal's garnet; the deadlines page's dates carry the glyph of their
  register in the dashboard's grammar (`.db-due`, no new shared CSS).
- **The preview drawer** (`templates/documents/partials/piece_drawer.html`, `static/js/src/piece-drawer.js`; DL54-102)
  on W2-A's overlay system — never a second mechanism: `data-overlay-modal="none"`, **beside the list on desktop** (no
  scrim, the page usable, another row swaps the content, the slide never replays; the workspace makes room once the
  drawer's first frame is painted and the register lays itself out by the width it is left — cards at 1440), **a modal
  sheet on a phone** (≤ 40rem: the scrim, `aria-modal`, the trap). The head at 0 ms from the row (the reference, the title
  in its language, the chip · actor · date, written into slots), the busy key after 400 ms; the body is the piece's own
  `<article>`, fetched, **seated by L3** on a first arrival (the loader asked for at the opening; a fragment that arrives
  first simply stands). **History**: the opening pushes the piece's URL, Esc / «Fermer» / Back bring the register's URL
  back **with its `?état=`**, a swap **replaces the entry**; the focus on the title, back on the row's title; a row's act
  sends it to the Dépôt's field, and a filing inside reads the piece and the register again. **RTL** (O5): it stands on
  the left in Arabic; reduced motion: one 80 ms opacity, no transform.
- **The filter's sheet**: the card layout's one 44 px control is a link to the system's bottom sheet
  (`components/sheet.html`: the scrim, the grip, «Fermer», Esc; the focus on the current entry and back on the control);
  the entries are one partial drawn twice (`state_filter.html`). The register pages link W2-A's page-only
  `css/dist/core/overlay-panels.css` before the documents sheet (CONTRACT §1); the native popover sheet left
  `_workspace.css`.
- **The deletion map** (plan §2.3): `v4/workspace.css`'s DocumentCollection / Row / Card, SegmentedControl and search left
  in step 1; `register.css`'s register and entry stay — eight page families still draw them — but the current entry's
  rules, which no page marks any more, left; the native sheet's rules (step 1's own) left `_workspace.css`.

### Found and fixed in this session

- **Two of the project's script rules were broken** by the first session's Dépôt (W1-D): a static import of `loader.js`
  and a bare `requestAnimationFrame` — `test_loader_rules.py` and `test_script_motion_gate.py` failed (neither was in its
  targeted runs). Fixed (`de935b8`): the loader on demand, the live region's words by a timer.
- **A focus in a row re-styled the whole page on a phone**: ≈ 650 elements a time on «Mes pièces» at 390 (Blink's
  `:has()` invalidation from `<body>`, `allDescendantsMightBeInvalid`, through W3-C's own
  `.doc-row:has(.doc-row__link:focus-visible)`; 276 for the Dépôt's field through `.doc-depot__zone:has(> input:focus-visible)`),
  paid twice by the drawer's open. Fixed (`1774840`, DL54-103): the keyboard read from the input's modality
  (`html[data-input="key"] … :focus-within`), the zone's wait from `[data-sending]`; a source guard; a keyboard browser test.
  The same focus now re-styles 4 elements.
- **The drawer's INP** (O7: p90 ≤ 200 ms at CPU × 4): 232–296 ms open as rehearsed — now 96–136 ms (below).
- **W1-C's chip guard** refused the drawer's placeholder chip (a literal member) and pinned the filter's legend in
  `register.html`: the slot is a register chip, the pins follow the legend into `state_filter.html`.
- **A flaky sweep**: `test_nothing_overflows_from_320_to_1440` read the page in the middle of the console shell's own
  transitions (the rail's width and the frame's padding after the 80rem crossing, W3-A's) and saw 20–60 px for a moment
  (reproduced on the branch before the merge: a resize's transient; with script off, or the transitions waited out, 0 px).
  The sweep now waits them out.

### The gate, measured (the merged branch `8b8e186`, lane 8789; E2/final, E2/final-drawer, E2/sweep-final.json)

| Item | Result |
|---|---|
| corners ≤ 3 a screen | at rest **4 · 8 · full** at most on every one of 72 captures (the register, the company's register, `/documents/`, a piece open and gated, the upload page, the gate page, the deadlines page; fr and ar; 1440 · 1280 · 390 · 360); with the drawer or the sheet open, the overlay's own 12 (plan §1.3: an open overlay may add its one) |
| ≤ 1 raised panel, ≤ 2 shadow values | at rest **1** raised plane (the strip) and **1** elevation value on the register pages, 0 elsewhere; with an overlay open, 2 values (the strip's and the overlay's level 4); the inset rules (the group's 3 px rule, the segmented edge) are edges, not shadows |
| CSP · console errors | **0 CSP reports, 0 script errors** on 86 captures; the gate page answers its document with the 403 the road without script has always had (IP S7: unchanged) and Chrome logs that status line — not a script error |
| no overflow 320–430 | **0 px** at 320 · 340 · 360 · 375 · 390 · 400 · 414 · 430 on every page of the area, fr and ar, at rest and with the drawer and the filter's sheet open (E2/sweep-final.json); 0 px at 1440 · 1280 on the captures |
| the drawer does not block the page on desktop | non-modal: no scrim, `aria-modal` absent, the register usable beside it (a second row swaps it) — E2/final-drawer d02–d04 |
| its history | the opening pushes the piece's URL (history length +1), a swap keeps the length (`replaceState`), Esc and Back bring the register's URL back; `?état=invalid` kept on closing (e02) |
| L3 on the fragment | the article's rows rise on the first arrival (`is-seating`, six animations at the first frame), none under reduced motion |
| Esc · focus · the trap where the contract says modal | Esc, «Fermer», Back close it; the focus on its title, back on the row's title; on a phone the sheet holds the focus (three Tabs stay in it); desktop: no trap |
| reduced motion · RTL | translate none, one 80 ms opacity; in Arabic the drawer stands on the left (x 0, 420 px), the sheets do not mirror |
| the first object in a phone's first viewport | the first piece's title at 692 px (fr) / 660 px (ar) at 390 × 844, 692 / 680 at 360 × 800 |
| the whole row as the target | 0 dead points of 42 (`qa-person`) and of 16 (`qa-doc-person`), fr and ar, 1440 → 360 |
| no `badge--*` | 0 on every capture |
| INP, CPU × 4, n = 9 cold loads a cell (E2/inp9-final.json) | the drawer opens p90 **136 / 128 ms** (ar / fr, 1440, beside the list) and **96 / 136 ms** (fr / ar, 390, as a sheet), closes p90 184 / 128 / 72 / 72 ms; the filter's sheet opens p90 120 / 104 ms, closes 80 / 64 ms. Before (E2/inp9-rehearsal-base.json): opens 232–296 ms |
| the audits | `tests/security` (the object-permission and authorisation audits) green, untouched |

### The CSS weight (gzip −9, `gzip.compress(data, 9)`, bundles rebuilt from a clean dist)

| | design-v5 `361b03d` (with W2-A) | this branch | change |
|---|---|---|---|
| `dist/main.css` (every page) | 42 152 | **40 876** | −1 276 |
| `dist/portal/console.css` | 6 809 | 6 809 | 0 |
| `dist/portal/portal.css` | 1 932 | 1 935 | +3 |
| **the console page types (the three shared sheets)** | 50 893 | **49 620** | **−1 273** (ceiling 50 927: 1 307 B under) |
| `dist/documents/documents.css` (page-only: the five documents pages and the showcase) | 1 172 | 5 418 | +4 246 |
| `dist/core/overlay-panels.css` (W2-A's page-only sheet, now linked by the two register pages) | 2 071 | 2 071 | — |
| «Mes pièces» in all | 52 065 | 57 109 | +5 044 |

The shared payload goes down (the owner's V5.8: the hard ceilings are the shared bundles'); everything the step added
lives in page-only sheets (DL54-104). For the merge step: the steward's per-page-type table records «Mes pièces» with
its own sheet «as it weighs at this merge» (DL54-87 item 3) — it weighs 5 418 B (and 2 071 B of W2-A's panels) because
the register, the piece, the Dépôt and the drawer's own rules live there and nowhere else (V5.8: «route/surface-specific
CSS loading where justified»).

### Tests (targeted, V5.5)

One pytest and one browser of mine at a time, on `test_ile_v5_l9` (Django's test database of
`TEST_DATABASE_URL=…/test_ile_v5_l9`); no run ended on a crash. On the merged branch (`8b8e186`):

- **Without a browser** — `apps/documents`, `apps/portal`, `tests/test_phase_console.py`, `tests/security` (the
  object-permission and authorisation audits among them), `test_chips_registry.py`, `test_state_chips_carry_a_register.py`,
  `test_o14_lint.py`, W2-A's `test_overlays.py` and `test_overlays_console_w2_a.py`, `test_design_docs.py`,
  `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_static_pipeline.py`,
  `test_documents_w3_c.py`, `test_depot_w3_c.py`, `test_script_motion_gate.py`, `test_loader_rules.py`,
  `test_console_shell_stylesheets.py`, `test_console_shell_w3_a.py`, `test_v5_tokens.py`, `test_dashboard_w3_b.py`,
  `test_chips_cards_w1_c.py`, `test_icons.py`, `tests/i18n/test_rtl_static.py`, `tests/test_regen_design_inventory.py`,
  `tests/test_check_ownership.py`: **1 664 passed, 1 skipped** (the confidential sentinels' table is not configured on
  the lane), **1 failed — `test_script_motion_gate`, on W2-A's `overlay/extras.js`** (design-v5's own since its merge;
  see «For the merge step»; W3-C's scripts pass it).
- **In the browser** (`-m browser -rs`, 0 skipped) — W3-C's `test_drawer_browser_w3_c.py`,
  `test_documents_browser_w3_c.py`, `test_depot_browser_w3_c.py`, W2-A's `test_overlays_console_browser_w2_a.py`,
  `test_overlays_browser_w2_a.py`, `tests/i18n/test_rtl_browser_overlays.py`, `tests/i18n/test_rtl_browser.py`,
  `apps/portal/tests/test_browser.py`: **114 passed**; W3-A's `test_console_shell_browser_w3_a.py` and
  `test_console_phone_browser_w3_a.py`, W3-B's `test_dashboard_browser_w3_b.py`, W1-C's `test_browser_chips_w1_c.py`:
  **104 passed**.
- Before the merge, on the branch as the first session left it: 840 + 50 + 8 passed (the same suites less W2-A's); the
  two script guards above failed on `depot.js` and were fixed first.
- New tests: the source guard of the documents sheets' `:has()`, the zone's keyboard ring, a row's keyboard light, the
  page-only sheet's link and its order on the register pages, a record's own words isolated on the piece's page;
  retargeted with their intent: the filing tests wait for the announcement, the overflow sweep waits out the shell's
  transitions. `ruff check` and `ruff format --check` clean on every changed Python file; every changed file LF.

### For the merge step

- **Paths outside the slice** (each justified in the decision log; `scripts/check_ownership.py w3-c design-v5`: 18
  inside, 7 slice, 21 generated, 15 outside): DL54-99 — `templates/documents/partials/depot.html`,
  `apps/documents/tests/test_requirement_views.py`, `tests/frontend/test_v5_tokens.py`, `templates/dev/showcase.html`;
  DL54-101 — `apps/portal/static/portal/portal.css`, `templates/portal/partials/deadline_item.html`,
  `apps/documents/templatetags/documents_register.py`, `static/js/src/depot.js`; DL54-104 — `static/js/src/piece-drawer.js`,
  `templates/documents/partials/piece_drawer.html`, `state_filter.html`, `tests/frontend/test_overlays.py`,
  `test_overlays_console_w2_a.py`, `test_overlays_console_browser_w2_a.py`, `tests/frontend/test_state_chips_carry_a_register.py`.
- **W2-A's `static/js/src/overlay/extras.js` fails `tests/frontend/test_script_motion_gate.py`** (a bare
  `requestAnimationFrame` outside `motion.js`) — on W2-A's own branch and on design-v5 since its merge; not W3-C's file,
  so not changed here (the gate's rule: `afterPaint()` / `nextFrame()` from motion.js). The steward's batches did not run
  that test.
- Numbering: DL54-96 … DL54-104 follow design-v5's DL54-95.

### For other families (not edited here)

- **W1-C**: `.form-field:has(… :focus-visible …)::after` and `.opt:has(input:focus-visible)` (`main.css`) re-style
  ≈ 800 elements when the Dépôt's date field takes the focus on a phone (the same Blink invalidation as above): the
  remedy that W2-C1 used and W3-C now uses — `html[data-input="key"] .form-field:focus-within` — is W1-C's, every page at
  once.
- **W3-A**: after a window crosses 80rem the rail's width and the frame's inline padding transition for 200 ms (a resize,
  not the person's act); read in the middle, the page's inline end is out of the viewport for a moment. Harmless at rest.
- **W3-E**: the deadlines page's template (its eyebrow «Espace réservé»), the case file's band and the HealthStrip's last
  consumer, as step 1 said.
- **W3-B**: unchanged from step 1's list (`_deadlines_card`'s no-op mapping, the bridge's `SCAN_BADGES`).

### Copy packet

No new word in step 2: every word of the Dépôt, the drawer and the sheet is a catalogue string (the drawer's head
repeats the row's; «Pièce demandée», «État», «Responsable», «Échéance», «Fermer», «Filtrer par état»). Step 1's packet
stands (B1 item 3).

### What is left, and whose

- **The Performance Lead**: the documents pages on 8782 under the lock (the container query's layout cost, the drawer's
  INP on a real mid-range Android: the lane's figures are a smoke).
- **Wave 4**: the drawer and the sheet in WebKit and Firefox (O10 — W2-A's gate ran the system's own; the register's are
  Chromium-measured here).
- The owner's copy review (B1): the packet of step 1.

## Review fixes (implementer w3-c-fix, 12 October 2026)

The fix pass of V5.5 (implement → review once → fix → ship) on the senior review (`REVIEW.md`, SHIP_AFTER_FIXES: three
majors, seven minors) and the accessibility/performance check (`A11Y_PERF.md`, SHIP_AFTER_FIXES: its finding 1 is the
review's M1, three minors). **Every item is fixed**: the three majors, the seven minors of the review and the three
minors of the check — nothing listed for later but the carry-overs that are other families' files. Decision log:
DL54-105. Evidence outside every repository: `C:/tmp/ile_v5_council/evidence/v54/w3-c/fix/` (`m1/`, `m2/`, `strip/`,
`files/`, `delete/`, `ring/`, `depot/`, `loose/`, `band/`, `inp/`).

**Lane.** Lane 9 as before: dev server 8789 from this worktree on `ile_v5_l9` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), pytest on `test_ile_v5_l9`; one pytest and one headless Chromium of
mine at a time, the profile `C:/tmp/ile_v5_council/.profiles/w3-c-fix/` (emptied before each run, so no bundle comes
from a cache); sessions minted with `Client.force_login` for `qa-person`, `qa-doc-person` and `w3c-depot` (no password
used, typed or stored), revoked at the end; the server stopped while the browser suites ran and at the end. **No piece
or file of the lane was written**: the loose deposit's answer was fulfilled inside the browser (Playwright's route) and
the deletion's dialog was answered «Annuler» (the real filings and the real deletion ran in the tests); the only writes
on the clone are the three minted sessions (deleted), the accounts' `last_login` and one `auth.login` audit event each.
Never 8780, 8782, Chrome 9222 / 9223; no browser run crashed; the benchmark lock was never present.

### What was fixed, and how

| Item | The fix | Where |
|---|---|---|
| **M1** (and A11Y_PERF 1) — after a swap the close threw the page to the scroll of the first opening and the focus to the first row opened (or left it 1 060 px below the fold) | Two causes, two remedies. **The scroll**: the register's history entry keeps no scroll to restore while the drawer owns the next one — `history.scrollRestoration = "manual"` set before the first push (the drawer's entry inherits it) and given back once the traversal back to the register has landed, after its frame (`settleScroll`). **The focus**: on `overlay:close` the focus goes to the event's opener — the title of the row of the piece SHOWN, which the swap moved — when it was inside the drawer or nowhere, never for a link that leaves; whether it was inside is tracked by `focusin` / `focusout` (the native close's own focusout comes with the drawer shut: the `<dialog>`, shown once, hands the focus to the row focused at its `show()` before `overlay.js` looks). Then the focus is brought into view if it is not | `static/js/src/piece-drawer.js` |
| **M2** — opening re-laid out the register under the pointer, and nothing said which piece was open | **Marked**: the open piece's title `aria-current="true"`, its row `data-drawer-open` — the hover's surface and a 2 px `--accent-mark` rule on the reading edge (the portico's current-link rule), an outline in Highlight under forced colours —, written after the drawer's first frame with the re-layout, moved on a swap, cleared on closing. **Kept in place**: the element the person is on — what was pressed on opening (the row's title, the row's act, the strip's act), the focus on closing — is measured before the `data-drawer-beside` toggle and put back by an instant scroll after it. DL54-102's decision (cards beside the drawer) is kept | `piece-drawer.js` (`mark`, `beside`); `_workspace.css` §10, §9 |
| **M3** — two clocks: an open piece due tomorrow read «En retard» on a lane or the preview | `DocumentRequirement.is_overdue` and `ChecklistItem.is_overdue` read `core.clock.today()` (one line each — two justified paths outside the slice); T1 (`_open_obligations`) and the case's progress read those properties; the presenter keeps `overdue=` (both clocks are one now) | `apps/documents/models.py`, `apps/cases/models.py` |
| **m1** — the caption counted a set no run shows | The caption ends at «… sur … validées» (one clause dropped, no new word; the copy packet's item 6) | `templates/documents/partials/register.html` |
| **m2** — two primaries for one act when the drawer showed the strip's piece | While the drawer shows the strip's piece, the strip's next piece takes the open row's state and its act steps down to a secondary (`data-drawer-stepped` restores it); the drawer's «Déposer» is the one primary in view | `piece-drawer.js` (`mark`); `_workspace.css` §10 |
| **m3** — on a phone the files tables stacked into label blocks (≈ 1 300 px at 390) | Below 40rem of their region one item a file: the name (the link) and its glosses on their line, then «type · taille · date» on one muted line, the act at its inline end, the register's hairline between files, no label. No cell carries `data-label` any more, so portal.css's labelled pop-in (`table:has(tbody [data-label])`, 0-1-4: the uppercase labels and 2 px navy rules came from there) never reaches them. «Tous les fichiers de votre compte» on `qa-person` at 390: 635 px | `_table.css`; `templates/portal/documents.html`, `templates/documents/index.html` |
| **m4** — «Supprimer» deleted a loose file at once | The row's «Supprimer» opens the overlay system's alert dialog — the declarative opener (`data-overlay-open`: without script the button posts its form, as it always has). The dialog: the trash disc, «Supprimer», the file's name then «Cette action est définitive.» (the account deletion's sentence) as its description, «Annuler» the safe answer (the focus, Esc), «Supprimer» the garnet outline — a submit button `console.js` points at the row's form (`form=`), the same POST. On a phone the system's bottom sheet | `templates/documents/partials/delete_confirm.html` (new), `index.html`, `static/js/src/console.js` §2e |
| **m5** — the loose deposit's answer emptied the page | The answer names the file before the server's sentence («copie.pdf» / «Document téléversé.» / «Retour au registre des pièces»), the form is set back and the zone stays for another file; the polite region says «copie.pdf — Document téléversé.» | `depot.js`; `depot.html` (the name's slot); `_depot.css` |
| **m6** — the size shown contradicted the refusal | `sizeOf(bytes, max)`: an empty file «0 ko»; from a megabyte one decimal rounded away from the limit — «10,1 Mo» for a file just over it, «10 Mo» at it | `depot.js` |
| **m7** — «il registro» drawn twice | The strip's marks carry the dashboard's ledger classes (`db-ledger__marks`, the run `db-ledger__group--*`: their size and their group's colour, on every console page through console.css); the copies left `_workspace.css`, which keeps only their place (their band under the count, 6 px between marks) | `register.html`; `_workspace.css` §3 |
| **A11Y_PERF 2** — the runs lost most of their ring to the strip's clip | `.reg a.reg-run:focus-visible { outline-offset: -4px; box-shadow: none }` — the step-1 rule (`a.reg-run`, −3 px) lost to v4/workspace.css's `.console__workspace :is(a, …):focus-visible` (0-3-0), which set the 2 px offset back. Ring fill on the pixels 1.01 on all three runs (was 0.27–0.68) | `_workspace.css` §3 |
| **A11Y_PERF 3** — «Télécharger» under 44 px for a finger | Under a coarse pointer the foot links' invisible band: 44 px tall, and 44 px wide where the word is shorter (`inset-inline: min(0px, calc(50% - var(--hit-primary) / 2))`). Measured at 390 touch: 76 × 44 (fr), 44 × 44 (ar). The gate's link keeps WCAG 2.5.8's inline exception (it stands in its sentence) | `_depot.css` (the coarse block) |
| **A11Y_PERF 4** — a refused file was not tied to its field | `refuseFile()` (one function for the Dépôt and the fresh one after an antivirus refusal) sets `aria-invalid="true"` and adds the refusal's id (`{{ field.auto_id }}_refusal`) to the field's description; `clear()` — run first by every new choice — takes both back | `depot.js`; `depot.html` |

### As measured (lane 8789, `qa-person` · `qa-doc-person` · `w3c-depot`, fr and ar)

- **M1** (`fix/m1/final-fr-1440.json`, `after1-*.json`): open «Extrait de casier judiciaire», scroll, swap to
  «Proposition de contrat de travail» (scrollY 1 028), then «Fermer», Esc in the drawer, Esc in the list, Back — in all
  four the focus lands on «Proposition…», its title where it stood (500 px from the top of a 900 px viewport, 500
  after), the page at 560 once the table is back (it was 92 or 0, the focus on «Extrait…» or 1 060 px below the fold);
  before the last anchor change (the row's top kept rather than its title's) ar 1440 gave 1 423 → 940 with the row at
  120 → 120 and fr 1100 1 074 → 712 with 500 → 499; the browser tests hold it to 2 px in fr and ar.
  `history.scrollRestoration` reads `manual` while the drawer is open and `auto` 50 ms after the close.
- **M2** (`fix/m2/`): at 1440, 1280 and 1100 the row pressed is still the row under the pointer once the register is
  cards (it was another piece's); `aria-current` on its title, `data-drawer-open` on the row; the first opening at
  scrollY 0 scrolls 62 px at 1440 so the pressed title stays put. Under forced colours the open row's edge is a 2 px
  Highlight outline; under reduced motion nothing runs; on a phone (the modal sheet) the marks are set under it and
  cleared with it, the focus back on the row in view (`fix/final/`).
- **m2** (`fix/strip/`, `qa-doc-person` 1280): the strip's act `btn--primary` → `btn--secondary` while the drawer shows
  «Diplôme…» (one visible primary: the drawer's «Déposer»), back to primary on Esc, the focus on the row's title.
- **m3** (`fix/files/`): at 390 «Tous les fichiers de votre compte» is 635 px (six files, each a name, its gloss and
  one line «Contrat · 298 octets · 21.09.2026»); «Autres fichiers déposés» 186 px for one file, «Supprimer» at the
  inline end; 0 px overflow.
- **m4** (`fix/delete/`, `w3c-depot`, 1440 and 390): role `alertdialog`, `aria-modal`, its description
  «diplome-scan-2026.pdf Cette action est définitive.», the focus on «Annuler», the dialog's «Supprimer» owned by the
  row's form (`loose-delete-<pk>`), Esc closes it and the focus is back on the row's «Supprimer»; nothing posted.
- **m5 / m6 / A11Y 4** (`fix/loose/`, `fix/depot/`, routed): «PDF · 0 ko» beside «Le fichier est vide.»; «PDF · 10,1 Mo»
  beside «… taille maximale de 10 Mo.»; a file of exactly 10 Mo «PDF · 10 Mo», accepted; the refused field
  `aria-invalid="true"`, described by `id_file_helptext id_file_refusal`, both gone on the next choice.
- **Health**: 0 console errors and 0 CSP reports on every page of these runs.
- **INP smoke** (`fix/inp/inp_smoke.json`, CPU × 4, n = 5 cold loads a cell — a smoke, not a benchmark): the drawer's
  open, median 72–80 ms (max 88–96), and its close by Esc, median 40–96 ms (max 112–128), in ar 1440 · fr 1440 · fr 390
  — under the 200 ms of O7. The press's task gained one `history.scrollRestoration` write; the marks and the kept
  place are written after the drawer's first frame, with the re-layout that was already there.
- **Weight** (gzip −9, bundles rebuilt from a clean dist): the shared bundles unchanged — `dist/main.css` 40 876,
  `dist/portal/console.css` 6 809, `dist/portal/portal.css` 1 935, **the console page types 49 620 B** (ceiling 50 927);
  the page-only `dist/documents/documents.css` 5 418 → **5 497 B** (+79: the files' list, the selected state, the
  download's band, the loose answer's name, less the ledger marks' copy); «Mes pièces» in all 57 109 → 57 188 B. JS:
  `dist/piece-drawer.js` 2 358 → 3 044 B (under §2.6's 4 KB module row), `dist/console.js` 1 647 → 1 754 B, the Dépôt's
  chunk 3 577 → 3 702 B (renamed `chunk-VNVIHY5J.js`; the old `chunk-OSH5OWDU.js` deleted).

### Tests (targeted, V5.5 — not the full suite)

One pytest and one browser of mine at a time, on `test_ile_v5_l9`; no run crashed. On the final tree:

- **The family's own and the guards around it** (`-m "not browser"`): `test_documents_w3_c.py`, `test_depot_w3_c.py`,
  W2-A's `test_overlays.py` and `test_overlays_console_w2_a.py`, `test_dashboard_w3_b.py`, `test_console_shell_w3_a.py`,
  `test_console_shell_stylesheets.py`, `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`,
  `test_static_pipeline.py`, `test_chips_registry.py`, `test_state_chips_carry_a_register.py`, `test_o14_lint.py`,
  `test_design_docs.py`, `test_script_motion_gate.py`, `test_loader_rules.py`, `test_v5_tokens.py`,
  `test_css_tokens_exist.py`, `tests/i18n/test_rtl_static.py`, `tests/test_regen_design_inventory.py`,
  `tests/test_check_ownership.py` and `tests/security`: **1 337 passed, 1 skipped** (the confidential sentinels' table
  is not configured on the lane), **1 failed — `test_script_motion_gate` on W2-A's `overlay/extras.js`**, as before
  (W3-C's scripts pass it: no `requestAnimationFrame`, no `.animate(`).
- **The models' change** (`-m "not browser"`): `apps/documents`, `apps/cases`, `apps/portal`, `test_dashboard_w3_b.py`,
  `tests/test_phase_console.py`: **515 passed, 3 skipped** (the intake suite's own: no rule in force), 0 failed.
- **In the browser** (`-m browser -rs`, 0 skipped): W3-C's `test_drawer_browser_w3_c.py`,
  `test_documents_browser_w3_c.py`, `test_depot_browser_w3_c.py` — **55 passed**; W2-A's `test_overlays_console_browser_w2_a.py`,
  `test_overlays_browser_w2_a.py`, `tests/i18n/test_rtl_browser_overlays.py`, `apps/portal/tests/test_browser.py` —
  **52 passed**.
- **New tests**: the drawer — after a swap «Fermer», Esc in the drawer, Esc in the list and Back keep the place and
  give the focus to the shown piece's row, inside the viewport (fr ×4, ar); the open row marked and kept under the
  pointer, moved on a swap, cleared on closing (fr, ar); the strip's act stepping down; the documents — the runs' and
  the rows' rings uncut by any clipping ancestor and a run's ring whole on the pixels (fr, ar); the files one item each
  on a phone (fr, ar); a loose file's deletion behind the alert dialog (Esc sends nothing, «Supprimer» deletes);
  «Télécharger» 44 × 44 under a finger (fr, ar); the Dépôt — a refused field `aria-invalid` and described, taken back
  by the next choice; the sizes «0 ko» / «10,1 Mo» / «10 Mo»; the loose road's answer with the file's name and the zone
  back (retargeted from «starts with Document téléversé.», intent kept); without a browser — one clock under a
  reference date (the reference a month before and a month after the real date: pieces, checklist items, the
  presenter's urgency, T1's obligations), the models on `clock.today()`, the caption, the ledger marks drawn once,
  the runs' inset ring rule, the files without `data-label`, the deletion's markup and its road without script, the
  refusal's id and `refuseFile`, the download's band, `sizeOf`. The count-reading pin of
  `test_the_rendered_counts_equal_the_rendered_groups` reads a run's class with the ledger's modifier after it.
- **They catch the defects**: on the review's tree the three clock tests fail (both directions, and the source pin), and
  the eight new drawer tests fail with the review's own symptoms — the focus on «Diplôme…» (the first row opened), the
  row 822 px down a 560 px viewport with scrollY 0, another piece under the pointer, no mark.
- `ruff check` and `ruff format --check` clean on every changed Python file; every changed file LF.

### For the merge step

- **Paths outside the slice** (DL54-105): `apps/documents/models.py`, `apps/cases/models.py` (M3, one line each),
  `templates/documents/partials/delete_confirm.html` (new). `static/js/src/piece-drawer.js`, `depot.js` and
  `templates/documents/partials/depot.html` were justified by DL54-99 / DL54-104; the tests are the slice's
  (`tests/**/test_*_w3_c.py`). `scripts/check_ownership.py w3-c design-v5`: 20 inside, 7 slice, 21 generated,
  **18 outside** — step 2's fifteen (DL54-99, DL54-101, DL54-104) and these three.
- **The weight to record**: the register page type (`«Mes pièces»`, `/documents/`) **57 188 B** with its page-only
  sheets (the shared 49 620 + documents.css 5 497 + overlay-panels.css 2 071); the piece / upload / gate type
  55 117 B. The shared bundles did not move in this pass.
- **The decision log**: DL54-105 is written after this branch's DL54-104; design-v5 holds DL54-96 … DL54-99 of its own
  (W3-F2's and the steward's) — renumber W3-C's from DL54-100 as the review said.
- **W2-A's `overlay/extras.js` still fails `tests/frontend/test_script_motion_gate.py`** (a bare
  `requestAnimationFrame`, W2-A's file, on design-v5 since its merge) — not changed here.

### Carry-overs (not W3-C's files)

- **W2-A**: `settle()` decides «was the focus inside the panel» after `panel.close()`, when a native dialog shown once
  has already restored the focus to the element focused at its `show()` — read it before closing (M1's system half;
  the drawer now does it for itself).
- **W3-B / W3-E**: T1 and the case file's checklist read the fixed `is_overdue` — nothing for them to change; the
  dashboard's `_dashboard.css` ledger rules now draw the documents strip's marks too (keep the class names, or move
  both together).
- **The copy review (O43)**: a question form for the deletion («Supprimer « %(name)s » ?») would read better than
  «Supprimer» + the name + «Cette action est définitive.» — no such string exists in the catalogue, so the dialog
  composes the existing ones; the review's one page under three names stands.

---

## Merge step — the steward's note on numbering (12 October 2026; label w3-c-merge)

W3-F2's three entries and the record of their merge, W2-C2's two and theirs, and W3-F1's six and theirs reached
design-v5 first (DL54-96 … DL54-109), so at the family's merge its ten entries became **DL54-110 … DL54-119** — the same
order, add 14 —, their content unchanged but for the cross-references between the ten, which moved with them (the
pre-merge sync, `351b078`). The steward's own record of the merge is **DL54-120**. The code and DS 2026 cite none of the
moved numbers.

How to read the numbers written before the merge — in this file, `REVIEW.md` and `A11Y_PERF.md` alike:

| Written in step 1 | Written in step 2, the review, the check and the fix pass | Read | The entry |
|---|---|---|---|
| DL54-82 | DL54-96 | **DL54-110** | «Mes pièces» V5.2 — the strip, one partition, the row as the link |
| DL54-83 | DL54-97 | **DL54-111** | F8 and F13 — the ladder stops once a piece is filed; lateness speaks azione |
| DL54-84 | DL54-98 | **DL54-112** | page partials imported by the page sheet; the piece in the order of need |
| DL54-85 | DL54-99 | **DL54-113** | paths outside the slice, the legacy rules deleted, the CSS weight |
| — | DL54-100 | **DL54-114** | step 2: the Dépôt — the eleven answers composed in place, on a JSON road that changes no rule |
| — | DL54-101 | **DL54-115** | step 2: F13 on every page that draws a deadline register; the register and the entry |
| — | DL54-102 | **DL54-116** | step 2: the preview drawer and the filter's sheet, on the overlay system |
| — | DL54-103 | **DL54-117** | step 2: no state read through `:has()` — the drawer's open and close under 200 ms |
| — | DL54-104 | **DL54-118** | step 2: paths outside the slice; the CSS as measured |
| — | DL54-105 | **DL54-119** | the fix pass: the person's place after a swap; the open piece marked; one clock decides one deadline |

The exceptions are design-v5's own numbers, unchanged: every DL54-33, DL54-52, DL54-73 and DL54-87; step 1's «this
branch's DL54-81» (W3-B's entry, the same number on design-v5); «design-v5's DL54-95» in step 2; and the fix pass's and
the review's notes for the merge step, «design-v5 holds DL54-96 … DL54-99 of its own (W3-F2's and the steward's)» and
«renumber from DL54-100» — which the merge read as above, after every entry that reached design-v5 since.
