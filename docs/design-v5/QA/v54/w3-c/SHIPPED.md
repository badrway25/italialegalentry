# W3-C shipped — 12 October 2026

**Document workspace and status — «Mes pièces», upload, requirement detail, the deadline registers.** Tag
**`v54/w3-c`** (design-v5 `e39bc32`, the status commit, as for the earlier families); merge commit `92cdddb`. The owner's
preview on http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 08:00 and verified.
Steward's merge, label `w3-c-merge`, under `DESIGN_V5_MERGE_LOCK` from 07:22 (after W2-C2's and W3-F1's merges, which
held the lock before it). Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` are both SHIP_AFTER_FIXES with
no P0; the fix pass (`NOTES.md`, «Review fixes») closed the three majors, the seven minors of the review and the three
minors of the check. No reviewer has read the fix pass again.

## What shipped

- **«Mes pièces» — «il registro»** (`templates/portal/documents.html`, `templates/documents/index.html`,
  `templates/documents/partials/register.html`, `apps/documents/presenters.py`): one raised strip, the page's one primary
  plane — whose move it is, in three runs («À faire», «En cours», «Valide») whose marks are the pieces themselves (the
  colour is the group, the shape is the state; the marks drawn by the dashboard's ledger rules), then the next piece with
  its date and the page's ONE primary («Déposer la pièce», «Remplacer la pièce», or «Consulter» with the Conditions
  gate's line while G1 holds); none when nothing is asked (the sentence). Below, one partition in the same three groups,
  one piece per row, **the row itself the link**: the state always a word and its mark («Valide» in ink, never a check;
  «En examen» in lapis; «Manquant» and «À remplacer» each their own mark), the date always with its glyph, the act only
  where the reader acts. The state filter is also the key to the marks; on a phone it is the overlay system's sheet.
  The account's files below, one item each on a phone.
- **The preview drawer** (`templates/documents/partials/piece_drawer.html`, `static/js/src/piece-drawer.js`): a piece
  opens beside the list on desktop — non-modal, the list usable, another row swaps it —, as a modal sheet on a phone;
  the head filled from the row at once, the body read under the loader; the piece's URL pushed, a swap replaces it;
  Esc, «Fermer» and Back bring the register back with its `?état=`, at its place, the focus on the shown piece's row; the
  open row marked (`aria-current`, a 2 px accent rule; Highlight under forced colours). Open median 72–80 ms, close
  ≤ 128 ms at CPU × 4 (the lane's smoke).
- **The Dépôt** (`templates/documents/partials/depot.html`, `static/js/src/depot.js`, `apps/documents/views.py`'s JSON
  answers): one markup on the piece's page, in the drawer and for a loose file; every answer composed in place — a
  format refused, an empty file, a size over 10 Mo (said as «10,1 Mo», never contradicting the refusal), the server's
  content check, a past validity date, the antivirus refusal, the throttle, the Conditions gate, the filing with its new
  state; a refused file marks its field. The same validation chain, limits, scans, throttle and permissions run on both
  roads (the review read them line by line). A loose file's «Supprimer» asks first, in the system's alert dialog.
- **The piece, the loose upload and the Conditions gate** (`requirement_detail.html`, `upload.html`,
  `terms_required.html`) in the same grammar, from the documents pages' own sheet.
- **F13 on the deadline registers**: «En retard» is azione (terracotta, the disc with clock hands, the alarm-clock glyph),
  «Bientôt» attesa — on the deadlines page's dates, the case file's checklist, dates and next step, the console's next
  action and the portal tables' late rows: red never means lateness. **One clock decides one deadline**:
  `DocumentRequirement.is_overdue` and `ChecklistItem.is_overdue` read the project's clock, as the register, the
  deadlines page and T1 already did (on a lane or the preview a piece due tomorrow reads «Bientôt», never «En retard»).
- **Everywhere**: Arabic mirrored with the French record titles isolated; reduced motion (opacity only) and forced
  colours drawn; no new word — every word is a catalogue string. **CSS**: the documents' V4 rules and the current
  entry's rules left the shared sheet — `dist/main.css` 38 683 → **37 324 B on every page** (−1 359), the console page
  types 48 556 → **47 200 B** —; the pages' own CSS is their page-only sheet `documents.css` (5 497 B gzip), the two
  register pages also linking W2-A's `overlay-panels.css` for the drawer and the sheet.

## The merge

- **The pre-merge sync** (`351b078`): design-v5 was 126 commits ahead (W3-F2's, W2-C2's and W3-F1's merges with their
  stewards' commits, the confidential-material docs commit). Conflicts, both areas kept: the decision log (design-v5's
  entries, then the family's, renumbered **DL54-110 … DL54-119**, add 14 — checked byte for byte both ways; the notes'
  closing section maps the old numbers, `3863fad`); DS 2026 §2's table (design-v5's rows, the family's one prose change on
  the `v4/workspace.css` row, the figures regenerated, `ca6e0e7`); the bundles, deleted and rebuilt from the merged
  sources. Every other file merged on its own.
- **Ownership** (`96e8b3d`): the 18 paths outside the slice the family declared, each read in the diff, assigned to w3-c
  (6 whole files in two globs, 12 slices) and four slices named as written; after it 26 inside, 19 slice, 21 generated
  and the manifest itself; `--validate` coherent (25 families, 611 entries).
- **The shared CSS gate (V5.8) passed** and every ceiling lowered to the merged weight; the documents pages' two page
  types recorded through their own sheet — the piece, the loose upload and the gate **52 697 B**, the two register pages
  **54 768 B** (+2 969 and +5 040 B on their own pages only; the family's performance check on the twin is the sanity
  check). The record: **DL54-120** (`884d873`).
- **Bundles** rebuilt from a clean dist in the branch (the sync) and in design-v5 after the merge (`fa3697a`: the CSS byte
  for byte the tested branch's, the JS up to the chunks' names). `scripts/regen_design_inventory.py`: current on
  design-v5. The capture report is unchanged (it captures the home, privacy, login and 404, none of which the family
  changes). `ruff check .` clean; `makemigrations --check`: no changes.
- **Tests** (lane `test_ile_v5_l9`, one pytest and one browser at a time, no run crashed; V5.5: targeted, not the full
  suite; `evidence/v54/w3-c/merge/tests_*.log`): non-browser — `apps/documents`, `apps/portal`, `apps/cases`,
  `tests/test_phase_console.py`, `tests/security` (with the object-permission and authorisation audits and the
  confidential-material sentinel test), the chips registry and registers, the O14 lint, the overlay tests, the design
  docs, both bundle-current tests, the static pipeline, the family's own and what the merge touched — **1 817 passed**,
  3 skipped (the intake suite's own); browser — the family's three files with `apps/portal/tests/test_browser.py`
  **63 passed**, the overlay browser tests with `tests/i18n/test_rtl_browser.py` and `test_rtl_browser_overlays.py`
  **67 passed**, 0 skipped; on design-v5 after the merge and the rebuild **327 passed** (the bundle, docs, pipeline,
  ownership and inventory tests and the family's own), the preview's own tests with the new status files **297 passed**.
- `live_status.json`: the family row w3-c — state v5, its review as the decision, the tag — and the five surfaces the
  census names for the area marked v5: `documents-portal`, `documents`, `document-requirement`, `document-upload`,
  `document-upload-terms-required`. `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all checked by request after the restart: 200, no traceback)

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w3-c`; the index http://127.0.0.1:8780/__design-v5/index/
  lists the family as passed with its review (http://127.0.0.1:8780/__design-v5/decisioni/w3-c/REVIEW.md) and the five
  documents surfaces as «V5 — council-passed». http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/ answer 200.
- Through the preview's persona switch («Personas» → «Entrer», no password), then:
  - «Personne avec dossier» (qa-doc-person): «Mes pièces» http://127.0.0.1:8780/fr/espace-reserve/mes-documents/ and
    http://127.0.0.1:8780/ar/espace-reserve/mes-documents/ — the strip and its one primary «Remplacer la pièce», three
    rows; press a row to open the piece in the drawer, another row to swap it, Esc / «Fermer» / Back to come back; the
    full register http://127.0.0.1:8780/documents/; the piece
    http://127.0.0.1:8780/documents/requirements/70d79bd5-9917-468f-abaf-6ec44669abb4/ and the loose upload
    http://127.0.0.1:8780/documents/upload/, each with its Dépôt (choose a .txt file, an empty file or one over 10 Mo to
    see the refusals composed in place, nothing sent).
  - «Personne, conditions non acceptées» (qa-person): http://127.0.0.1:8780/fr/espace-reserve/mes-documents/ — seven
    pieces in seven states, the strip's «Consulter» with the gate's line; http://127.0.0.1:8780/documents/upload/ — the
    Conditions gate (403, as the census says).
  - «Personne sans dossier» (qa-fresh-person): http://127.0.0.1:8780/fr/espace-reserve/mes-documents/ — the register's
    one sentence, no primary.
  - The phone: the strip's phone frame (390 px) — the strip composed, one filter control opening the system's sheet, the
    drawer as a sheet. Reduced motion and forced colours: the system's settings.

## Not done

- **«Mes échéances» stays «V4 + fondazione»** in the preview (`deadlines` not marked): its dates carry F13 from this merge,
  but its page — the template, its eyebrow — is W3-E's to redraw. On the preview database none of the personas has a
  date, so the page shows its empty state («Aucune échéance»); F13 on that page is held by the area's tests and was seen
  on the lane (the implementer's `w3c-depot` persona, three dates).
- **Writes in the preview**: a persona's session is read-only — a deposit or a deletion is refused before any view (the
  page reloads, nothing filed). The client guards answer in place; the filing and the server's answers are held by the
  area's tests (real filings and a real deletion) and were seen on the lane.
- **Words waiting for the owner (B1 item 3, O43)**: the copy packet in `NOTES.md` — the group words «À vous · En cours ·
  Réglées», «Prochaine pièce à fournir», a deadline's distance in words, «Sans échéance», «Pièce» for «Pièce demandée»,
  the caption's clause, the Dépôt's words, a question form for the deletion. Nothing of it is shipped.
- **Measures not made**: the Performance Lead's on 8782 (the container query's layout cost, the drawer's INP on a real
  mid-range Android — the lane's figures are a smoke); the drawer and the sheet in WebKit and Firefox (Wave 4, O10);
  Safari, a real phone and a screen reader were never run; no browser on 8780 (by rule).
- **Handed to other families** (`NOTES.md` «For other families», «Carry-overs»): W2-A — `settle()` should read whether
  the focus was inside the panel before `panel.close()` (the drawer does it for itself); W1-C — the
  `.form-field:has(… :focus-visible …)` rules re-style ≈ 800 elements on a phone (the remedy every page at once:
  `html[data-input="key"] .form-field:focus-within`); W3-A — the rail's 200 ms width transition when a window crosses
  80rem; W3-E — the deadlines page's template, the case file's band, the HealthStrip's last consumer (T1 and the
  checklist read the fixed `is_overdue`: nothing to change); W3-B — keep the ledger rules' class names, which now draw
  the documents strip's marks too.
- **Documentation**: DS 2026 §2.1 has no row for `documents/documents.css` (it never had one) and the
  `core/overlay-panels.css` row does not yet name the two register pages among its consumers — family prose (W3-C's,
  W2-A's) for a later pass. `ruff format --check` flags two lines that are design-v5's own (not changed here).
- **design-v5's own failing test**, unchanged by this merge: `test_script_motion_gate.py` on W2-A's `overlay/extras.js`
  (`requestAnimationFrame`; DL54-102 item 10) — the family's modules pass the gate.
- **The full suite** was not run (V5.5: the integration checkpoint runs it). Nothing was pushed to GitHub.
