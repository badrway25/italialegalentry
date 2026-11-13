# W3-E shipped — 16 October 2026

**The case file and the secondary console pages — requests, messages, deadlines, the company, Academy, help desk,
selection.** Tag **`v54/w3-e`** (design-v5 `ab67efe`, the status commit, as for the earlier families); merge commit
`16a8cfd`. The owner's preview on http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at
06:37 and verified by request at 06:38 (`verify_8780.log`: 59 requests, every one as expected; no traceback in the
server log). Steward's merge, label `w3-e-merge`, under `DESIGN_V5_MERGE_LOCK` from 05:41:42, after W3-D's tag (the
plan's order, §3.5 item 7). Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` were both SHIP_AFTER_FIXES
with no P0; the fix pass (`NOTES.md` «Review fixes») closed the review's four majors and the check's one major, and
fixed or handed on every minor. No reviewer has read the fix pass again; the steward's targeted run and the requests on
8780 checked it on the merged tree (`NOTES.md` «At the merge»).

## What shipped

- **The person's registers on one grammar** — «Mes demandes» and a request, «Communications» and «la lettera», «Mes
  échéances», «Mes dossiers», the case's pre-assessment, «Mon parcours» (the journey at its head when there is a file,
  the saved pre-assessments as records under it), «Ma situation»: W3-A's workspace head with no eyebrow repeating the
  level, the band (the register's count on the dashboard's ledger line, each event counted once), one row a record on
  hairlines with the whole row the way to it, the state always a chip through its producer (three new producers:
  `enquiries.SubmissionStatus`, `forum.RegistrationStatus`, `portal.DeadlineStatus`; «En retard» azione, never a
  refusal's red), the date with its register's glyph, «Non lue» a word with its ink dot; a communication drawn as the
  letter it is, the team's mark its seal; the empty state is design V5's component; the reserved area's 503 a page of
  service in the error pages' grammar (the door at rest, the key out of the lock).
- **«Ma situation»** counts one total («0 question(s) renseignée(s) sur 8» under the Stepper's eight nodes and «1 / 8»)
  and on a phone its one act is the shell's action bar («Continuer», the submit on the last question; «Menu» kept).
- **The organisations' and the other spaces' pages in the same grammar**: the company beyond its dashboard («Mes
  besoins» with the register's counts as its filter — «Tous», «À faire», «En cours», «Clos», `?état=`, no tile, no chart
  —, a need with its acts and history, «Mon entreprise», the forms; the V1 company band gone from every page); the
  Academy (the catalogue with its domains as the filter, «Mes formations», a course, a follow-up, the plan with its state
  as a chip — `academy.PlanStatus`'s producer); the help desk (the person's requests and the professional's queue, a
  request with the appointed professional as the answerable party and the exchange headed by function, opening one;
  the dispatch desk's chrome); the selection (the authorised actor as the answerable party wherever a stage is visible,
  the process's phases as the registers' sequence, the person's panel, the disclosures); the Forum's governance
  («Ma participation», the commissions, the proposals, the projects, the annual report) and its closed page; the
  bridge's states through their producers (`badge.html` retired on console pages), «Mon organisation» with the account's
  audience glyph.
- **The case file in design V5 — the five questions in order, in the first screen**: the head (reference in ILE Mono,
  the state's chip, since when); the journey in W3-D's compact forms (the level line where its column holds 56rem, else
  the card and «Où j'en suis»); the NowPanel with the page's one primary — the next checklist line drawn once, its act
  its own alert dialog («Nouvel état de cette ligne»), a mandated reader told the next step in nobody's voice;
  «Exigences» as register rows (who answers, the team's note, the source in ILE Mono, the chip, the date) and «Pièces du
  dossier» with «il registro»; the answerable parties; the feed beside it from 80rem (newest first, «Vous» for the person
  only, «La personne» for anybody else, a line's change naming its line). A held file (sec-f7) says its state and its
  reason once, in the NowPanel. On a phone the act is the shell's action bar.
- **State changes on the overlay system** (C-5, C-6): a line's «⋮» menu and the alert dialog — the consequence said
  before the act, «Annuler» the safe default with the focus on it, the trap, Esc, the scrim that never closes it, the
  focus back on «⋮», the POST returning to the row with «La ligne a été mise à jour.»; the file's own state in the same
  dialog (the moves the domain permits this reader, radios with none chosen in advance, the closure's consequence, the
  suspension's rule); the irreversible closures of the help desk («Clore la demande») and of the selection («Clore le
  processus») open the same alert dialog. Without script each dialog shows in place.
- **CSS (V5.8)**: `v4/workspace.css` left the cascade with its last named consumer (what other console pages still
  drew of it moved unchanged to the console partial `v5/_frame.css`), and the V1 devices these pages were the last to
  draw left `main.css` (the folio, the entry's ordinal and responsible actor, the night verso) — `dist/main.css` 35 483 →
  **31 906 B on every page** (−3 577), the console page types 44 196 → **40 140 B** (−4 056). The registers' CSS is one
  page-only sheet (`portal/registers.css`, 2 875 B) linked by the pages that draw a register, the case file's another
  (`portal/case.css`, 955 B); W2-A's overlay panels (2 071 B) only where a dialog is drawn. Nothing moves at load;
  reduced motion the same still; forced colours drawn; Arabic mirrored, French data isolated in its direction.

## The merge

- **The order and the sync**: `v54/w3-d` has stood on design-v5 since 15 October (the plan's order: W3-E after W3-C
  and W3-D). design-v5 had moved from the branch's merge base `fec37d3` to `11070b5` (the sec-f5 merge, integration
  checkpoint 3, the sec-f7 merge, the private-root probe's test: 63 commits); the steward's sync (`dcf11a2`) resolved
  the decision log — the family's eighteen entries are **DL54-133 … DL54-150** on design-v5 (add 3; the notes and the
  review keep the numbers they were written with, and their closing section gives the mapping) — and rebuilt the JS
  bundles (`merge=binary`). Where sec-f7 meets the case file the steward wrote two lines (`398590e`) and retargeted
  sec-f7's page test, whose V4 select options the case file draws as its state dialog's radios (`ab0a79a`); one
  end-to-end test of the held file's page added to the family's file.
- **Ownership** (`c8859fc`, `6518c78`, on the branch): the 33 paths outside the slice the family declares, each read in
  the diff and assigned with its reason and its owner (four whole-file entries, 27 slices), the merge's retargeted test
  as a slice of sec-f7's file, two slices named as written. After it: 69 inside, 41 slice, 32 generated, and the
  manifest itself, the one steward-only path; `--validate`: coherent, 29 families, 730 entries.
- **The shared CSS gate (V5.8) passed**: both shared bundles fall — `main.css` 35 483 → 31 906 B on every page, the
  console page types 44 196 → 40 140 B —; the page types that draw a dialog grow by W2-A's panels only where they draw
  one; every ceiling lowered to the merged weight; the area's page types recorded through their own sheets. The
  record: **DL54-151** (`9eb32da`), with the table of every page type before → after.
- **Bundles** rebuilt from a clean dist in the branch (byte for byte the committed ones) and in design-v5 after the
  merge (`3667aba`: the CSS byte for byte the branch's; the JS the same code, the chunks' names following this
  worktree). `scripts/regen_design_inventory.py`: current on both. The capture report is unchanged (the home, the
  privacy page, the login and the 404: no icon, h1, overflow or direction changes). `ruff check .` clean;
  `makemigrations --check`: no changes; `manage.py check`: no issue.
- **Tests** (lane `test_ile_v5_l5`, one pytest and one browser of the steward's at a time, no run crashed; V5.5:
  targeted, not the full suite; `C:/tmp/ile_v5_council/evidence/v54/w3-e/merge/tests_*.log`): non-browser — the merge
  brief's list (`apps/cases`, `apps/portal`, `apps/companies`, `apps/academy`, `apps/helpdesk`, `apps/selection`,
  `apps/forum`, `apps/notifications`, `tests/test_phase_console.py`, `tests/security` with the object-permission and
  authorisation audits, the chip registry and the state chips' register, the O14 lint, the design docs, both
  bundle-current tests, the static pipeline) with the family's own file and the files it retargeted or reads, the
  checker's and the inventory's — **2 000 passed**, 3 skipped (the intake suite's own: no legal rule in force), 1
  xfailed (the showcase's captions), **10 failed: the one semantic conflict with sec-f7** (above), fixed — the three
  files concerned re-run: **162 passed**; browser — `apps/portal/tests/test_browser.py`,
  `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_overlays.py` and the console's browser files the family touches or
  reads (W3-D's journey, W3-A's phone and shell, W3-B's dashboard, W2-A's console overlays, W3-C's documents and drawer)
  — **199 passed**, 0 skipped; on design-v5 after the merge and the rebuild **232 passed**, 1 xfailed; the preview's own
  tests and the checker's with the new status files **354 passed**.
- `live_status.json`: the family row w3-e — state v5, its review as the decision, the tag — and nineteen surface keys
  v5 at `v54/w3-e`. `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all checked by request after the restart: 200, one h1 on every console page, no traceback, the expected sheets)

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w3-e`; the index http://127.0.0.1:8780/__design-v5/index/
  lists the family with its review (http://127.0.0.1:8780/__design-v5/decisioni/w3-e/REVIEW.md) and marks its
  nineteen surfaces V5. http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/ answer 200.
- Through the preview's persona switch («Personas» → «Entrer», no password), then:
  - «Personne avec dossier» (qa-doc-person): «Mes dossiers» http://127.0.0.1:8780/fr/espace-reserve/dossiers/, the
    case file http://127.0.0.1:8780/fr/espace-reserve/dossiers/EE167596D4/ (the compact journey, the NowPanel, the
    pieces, the file's state dialog), «Ma situation» http://127.0.0.1:8780/fr/espace-reserve/ma-situation/, «Mes
    demandes» http://127.0.0.1:8780/fr/espace-reserve/mes-demandes/, «Mon parcours»
    http://127.0.0.1:8780/fr/espace-reserve/mon-parcours/ (the journey at its head), «Mes échéances»
    http://127.0.0.1:8780/fr/espace-reserve/mes-echeances/ (its empty state: this persona has no date),
    «Communications» http://127.0.0.1:8780/fr/espace-reserve/communications/, the Academy
    http://127.0.0.1:8780/fr/espace-reserve/formation/ and a course
    http://127.0.0.1:8780/fr/espace-reserve/formation/cours/italien-a1/; the mirror under `/ar/`.
  - «Personne, conditions non acceptées» (qa-person): the case file with its lines, their «⋮» menus and dialogs
    http://127.0.0.1:8780/fr/espace-reserve/dossiers/E46E03B461/, a request
    http://127.0.0.1:8780/fr/espace-reserve/mes-demandes/contact/1/, «Mon parcours» with its saved pre-assessment, the
    help desk http://127.0.0.1:8780/fr/espace-reserve/guichet/, a request and its closure dialog
    http://127.0.0.1:8780/fr/espace-reserve/guichet/4262f0d4-1396-4f63-a690-a2b8e9c27ad4/, opening one
    http://127.0.0.1:8780/fr/espace-reserve/guichet/nouvelle-demande/, «Mes formations»
    http://127.0.0.1:8780/fr/espace-reserve/formation/mes-formations/ and a follow-up
    http://127.0.0.1:8780/fr/espace-reserve/formation/mes-formations/32589170-cc35-4fda-984f-edabf4d3f30f/; the mirror
    under `/ar/`.
  - «Entreprise — Cantiere Adriatico» (qa-company): the dashboard (no module sheet any more)
    http://127.0.0.1:8780/fr/espace-reserve/entreprise/, «Mon entreprise»
    http://127.0.0.1:8780/fr/espace-reserve/entreprise/mon-entreprise/, «Mes besoins» and its filter
    http://127.0.0.1:8780/fr/espace-reserve/entreprise/mes-besoins/, «Nouveau besoin»
    http://127.0.0.1:8780/fr/espace-reserve/entreprise/mes-besoins/nouveau/.
  - Reduced motion and forced colours: the system's settings (nothing moves at load on these pages).

## Not done

- **Not reachable through the preview's personas**: the selection (an authorised actor's workspace and process, the
  person's panel), the Forum's governance (the module is shut — G11 — and its closed page is the 503 of a page of
  service), the bridge's institution and university, the dispatch desk and the territorial analysis (staff), a
  mandated reader's case file (the professional, the administrator), a held file's page (a suspended or closed file:
  the family's tests and the end-to-end test added at the merge hold it). The family's review and its fix pass drew
  them on lane 5 with lane-only data (`REVIEW.md`, `NOTES.md`).
- **No surface key** for the selection and the Forum's governance: the preview's census has no id for them.
- **Measures not made at the merge**: no browser on 8780 (by rule); the steward measured no page by hand — the family's
  accessibility + performance check stands for the page types (`A11Y_PERF.md`); a real phone and a screen reader were
  never run.
- **Handed on** (`NOTES.md` «Handed on», DL54-151 item 11): **B1** — the copy packet (a deadline's distance; a heading
  over the pre-assessments; the case file's words on a mandated reader's screen; «au titre d'un mandat daté» shown to
  an administrator; the guichet's band without its figure); **W3-A** — the rail's «Communications (n)» beside the band,
  the organisations' accounts offered the person's file entries, the Forum governance's rail; **W1-C** — the register
  per state, not per audience; **W3-D / W4-D** — the journey's `descriptive` variant without a consumer, and
  `.section--verso` / `.plate--verso` still named in `v5/tokens.css`'s night-grounds selector lists (W1-A's serialized
  file; dead selectors there); **the staff's design debt** — the selection's evidence table, the dispatch desk, the
  territorial analysis, the Django admin; **the showcase's owner** — the V4 samples left unstyled and
  `companies/partials/need_table.html`; **the companies module** — `companies/services.py`'s docstring naming the deleted
  `next_action.html`; **W4-C** — the case file's seven stylesheets; **W4-B** (in flight) — it meets this merge in the
  decision log, DS 2026, `base.css`, `components.css` and W3-A's two console test files at its sync.
- **The full suite** was not run (V5.5: the integration checkpoint runs it). Nothing was pushed to GitHub; nothing was
  deployed.
