# W3-B shipped — 11 October 2026

**Dashboard and cards — the person, company and institution dashboards.** Tag **`v54/w3-b`** (design-v5 `0a8299d`,
the status commit, as for the earlier families); merge commit `d92fe07`. The owner's preview on http://127.0.0.1:8780
serves it: v5-live checked out at the tag, 8780 restarted at 19:27 and verified. Steward's merge, label `w3-b-merge`,
under `DESIGN_V5_MERGE_LOCK` from 18:38. Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` are both
SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md`, «Review fixes») closed the three majors, every minor of W3-B's
but one optional part, and the check's findings 1–4 and 6; finding 7 — the console's CSS weight — was handed to the
merge and is recorded here (DL54-87 item 3). No reviewer has read the fix pass again.

## What shipped

- **The person's dashboard** (`templates/portal/dashboard.html`, `templates/portal/partials/now_panel.html`,
  `apps/portal/static/portal/v5/_dashboard.css` — a console partial imported by `console.css` after the shell): the
  DOM's order is h1 → NowPanel → journey. **The NowPanel** is the page's one raised plane (W1-C's action card) with its
  ONE primary — what to do now: the obligation, its state, its date, who answers for it, and the act in the register's
  words («Déposer la pièce», «Remplacer la pièce»; while the Conditions gate blocks the filing, «Consulter» on the
  piece's own page with the register's «Acceptation des Conditions d'utilisation requise.» — the terms page has nothing
  to accept yet). Four variants chosen by the system, never arranged by the account: «à vous», «en attente d'un
  tiers», «rien à faire» (naming the file's live assignment), «pas encore de dossier» with the owner's door — the
  console's one empty state that shows it; an overdue date takes the panel over. Then the journey (W3-D's, still at
  load), the file's facts in W1-C's summary strip beside the NowPanel from 64rem, «il registro» of the pieces by who
  holds them (the person's own first with their act, then the pieces in somebody else's hands with who holds them;
  each piece once), the dates and the communications as flat lists, the secondary in native disclosures, the account
  in one quiet line.
- **T1 — one next action** (`apps/cases/services.py`, a presenter change): over every open obligation of the file —
  its checklist items and the pieces it still waits for — on the precedence the function had, a piece read through the
  documents app's own authorisation (`reader`); the case pages pass the reader, so the dashboard and the case name the
  same piece. Before it, `qa-person`'s dashboard named an authority's undated item while three of the person's pieces
  were due.
- **F9** (`apps/portal/services.py`): a person's dashboard builds no card grid — six presenters and their queries no
  longer run for a grid nobody saw.
- **The company's dashboard** (`templates/companies/dashboard.html`): the person's grammar, not a second system — the
  legal name as the h1 with its verification, the NowPanel with the company's one next action and its one primary
  («Transmettre au projet», the need page's own form, for a complete draft when the account may submit; «Déclarer mon
  entreprise», «Compléter le besoin», «Créer un besoin»), «Mon entreprise» beside it, «il registro» of the needs by who
  holds them, «Communications», flat.
- **The bridge** (the accounts that are not a person — institutions, universities, authorised actors, a company-typed
  account; `templates/portal/partials/card.html`): no NowPanel — the system knows no next action of theirs —, its
  registers as flat sections: first what is due and what came in (an overdue date in terracotta, never the red of a
  refusal), then what was sent and filed, the organisation beside; an empty region is one line; for a company account
  or an authorised actor, one quiet link to where its work lives.
- **What left the cascade** (the bust rule's first remedy): the dashboards' V4 rules, the facts, the 12-column
  workspace grid, the lone next step, the bridge's assessment panel and every rule of the needs table in
  `v4/workspace.css`; the bridge's card grid and the old account panel in `portal.css`; two dashboard-only variants
  nothing called any more.
- **Everywhere**: no stat card, no grid of equal cards, no board, nothing dragged, resized or hidden — the system orders
  priority (the value matrix in `NOTES.md`); nothing animates at load; in Arabic the page mirrors and a record's own
  words keep their direction (`dir="auto"`); the keyboard goes skip link → the NowPanel's primary → …, every stop with
  the 2 px ring; reduced motion and forced colours drawn. No new copy: every word is a catalogue string (tested).

## The merge

- **The pre-merge sync.** The branch took design-v5 first (`3c24d67`; design-v5 was `38f78d4`, 50 commits ahead: W2-B's
  login «Il varco», its steward's merge and shipped note, the static pipeline). Four conflicts, both areas kept: the
  decision log (below); DS 2026 §2.1 (the family's console row, which now names the dashboards' partial, beside W2-B's
  entrance row) and §10 `doorway.html` («Usato in»: the NowPanel partial is the one template that includes the
  component; the home and the entrance draw the stage with their own markup); W3-A's import-list test (the family's
  check of the partials after the shell, with the static pipeline's collected-tree import of the light sheet). The
  dist files were not resolved by hand: `static/css/dist` and `static/js/dist` deleted and rebuilt (`npm run build`)
  on the merged sources. `console.css` merged clean and was read: the collected-tree convention, the light sheet, the
  shell, then `v5/_dashboard.css` — a path that resolves the same in the source and the collected tree.
- **Numbering.** W2-B's entries, the record of their merge and the static pipeline hold DL54-74 … DL54-77 on design-v5,
  so the family's nine entries are **DL54-78 … DL54-86** — add 4 —, content unchanged but for their cross-references;
  the index gained the fix pass's row (DL54-86). The code and DS 2026 cite none of the moved numbers; `NOTES.md`'s
  closing section says how to read the old numbers in the notes, the review and the accessibility report (`6bcb460`).
  The steward's record of the merge is **DL54-87** (`54d3572`).
- **Ownership.** `scripts/check_ownership.py w3-b design-v5` listed the nine paths the family declares (DL54-82,
  DL54-85); each was read in the diff and written under w3-b (`046879f`): `templates/portal/partials/now_panel.html` and
  `card.html` whole; `apps/cases/views.py`, `apps/companies/views.py` (the file stays W3-A's), the three
  `apps/portal/tests` files, one test each of `test_chips_cards_w1_c.py` and `test_console_shell_w3_a.py` as slices;
  the slices of `v4/workspace.css`, `portal.css` and DS 2026 named as written. After it: 10 inside, 14 slice, 18
  generated, and the manifest itself, the one steward-only path (before: 9 outside). `--validate`: coherent.
- **Bundles** rebuilt from a clean `static/js/dist` and `static/css/dist` in the branch (in the sync commit) and in
  design-v5 after the merge (`b94de50`: every CSS bundle byte for byte the tested branch's; the JS byte for byte
  design-v5's before the merge — the family changed no script — with this worktree's chunk names).
  `scripts/regen_design_inventory.py` finds the inventory current on the branch and on design-v5 (nothing written). The
  capture report is unchanged: `capture.py` captures the home, the privacy page, the login and the 404, none of which
  the merge changes (DL54-87 item 5).
- **Bytes** (gzip −9; DL54-87 item 3): `dist/main.css` 41 880 B (−651: the legacy rules deleted),
  `dist/portal/console.css` 7 072 B (+1 780: the dashboards' partial), `dist/portal/portal.css` 1 975 B (−288) —
  **50 927 B in the three sheets every console page loads**, 841 B over the ceiling of 50 086 B. §2.6 item 5 applied
  and said: the legacy rules were deleted first, the page-partial move weighed and refused (every session opens on a
  dashboard), and LCP and the first render measured no worse on the area's twin (W1-0's protocol, n = 9: LCP 252–300 ms
  earlier than V4, the first-render task 39–57 ms where V4's was 370–500, CLS 0) — not by the Performance Lead on 8782.
  The console page types' ceiling is **50 927 B** from here; the once-only raise is spent. The company's dashboard
  51 800 B, «Mes pièces» 52 099 B. `main.css`'s −651 B reaches every page type (the login 46 741 B, the home 56 531 B):
  no ceiling is lowered (none lands more than 1 KB under). `main.css` stands 4 200 B under its 45 KB ceiling. JS
  unchanged.
- **Lint and migrations.** `ruff check .` (CI's Lint step): all checks passed on the merged tree;
  `makemigrations --check --dry-run`: no changes.
- **Tests** (lane `test_ile_v5_l6`, one pytest and one browser at a time; V5.5: targeted, not the full suite). On the
  branch after the sync and the steward's commits, non-browser — `apps/portal`, `apps/companies`, `apps/cases`,
  `tests/test_phase_console.py`, `tests/security`, `test_dashboard_w3_b.py`, W3-A's `test_console_shell_w3_a.py` and
  `test_console_shell_stylesheets.py`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
  `test_design_docs`, `test_static_pipeline` (a real `collectstatic` under the manifest storage), W1-C's
  `test_chips_cards_w1_c.py`, `test_o14_lint.py`, `test_state_chips_carry_a_register.py`, `test_icons.py`,
  `tests/test_regen_design_inventory.py`, `tests/test_check_ownership.py`: **957 passed**, 3 skipped (the intake suite's
  own: no legal rule in force), 0 failed (15 min 56 s). Browser (headless Chromium) — `apps/portal/tests/test_browser.py`,
  `test_dashboard_browser_w3_b.py`, `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`,
  `tests/i18n/test_rtl_browser.py`: **122 passed**, 0 skipped, 0 failed, no run crashed (13 min 21 s). On design-v5
  after the merge and the rebuild: the two bundle tests, `test_design_docs`, the ownership and inventory tests, the
  static pipeline, the shell's two files and `test_dashboard_w3_b.py` — **219 passed** (1 min 47 s). Logs:
  `C:/tmp/ile_v5_council/evidence/v54/w3-b/merge/`.
- `live_status.json`: the family row w3-b — state v5, its review as the decision, the tag — and the five surfaces the
  census names for the area (`dashboard-person`, `dashboard-person-terms-pending`, `dashboard-person-empty`,
  `company-dashboard`, `org-bridge`) marked v5 with the tag. `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w3-b`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w3-b/REVIEW.md), and the five dashboard surfaces as «V5 — council-passed».
- **The person's dashboard** — `/__design-v5/` → «Personas» → «Entrer» (no password; the preview's sessions are
  read-only), then http://127.0.0.1:8780/fr/espace-reserve/ and http://127.0.0.1:8780/ar/espace-reserve/:
  - «Personne avec dossier» (qa-doc-person): the NowPanel «Votre prochaine action» — «Diplôme ou titre de formation»,
    its state, and the one primary «Remplacer la pièce» on the piece's page; the journey; the file's facts beside;
    «il registro»; the lists; what folds.
  - «Personne, conditions non acceptées» (qa-person): «Acte d'état civil légalisé» with «Consulter» on the piece's page
    and the register's «Acceptation des Conditions d'utilisation requise.»; the pieces due with their dates.
  - «Personne sans dossier» (qa-fresh-person): «pas encore de dossier» with the owner's door and «Commencer le
    questionnaire» as the primary.
- **The company's dashboard** — «Entreprise — Cantiere Adriatico» (qa-company):
  http://127.0.0.1:8780/fr/espace-reserve/entreprise/ and http://127.0.0.1:8780/ar/espace-reserve/entreprise/ — the
  NowPanel «Transmettez le besoin «Soudure d'assemblage sur charpente métallique» au projet» with the need page's own
  «Transmettre au projet» (pressing it in the preview is refused: a persona's session is read-only, 403; the area's test
  posts it and the need is «Transmis»), «Mon entreprise», the needs by who holds them, «Communications».
- **The phone**: the strip's phone frame, or a window under 1024 px — the NowPanel's facts two by two, the primary
  across. **Reduced motion** and **forced colours**: the system's settings.
- **The bridge** has no persona in the preview (it is for the accounts that are not a person; see «Not done»): it is
  held by the area's tests at 1440 and 390, fr and ar.

Checked after the restart, by request only (no browser on the owner's server;
`C:/tmp/ile_v5_council/evidence/v54/w3-b/merge/verify_8780.log`): `/fr/`, `/ar/`, `/it/`, `/en/`, `/__design-v5/`, the
index, the review and the login answer 200, the strip names `v54/w3-b` and the index the family. Through the preview's
own persona switch (no password; «Sortir» after each): qa-doc-person's dashboard in fr, ar, it and en, qa-person's and
qa-fresh-person's in fr and ar, qa-company's company dashboard in fr and ar — each 200 with the shell and the NowPanel
in the markup (the variant expected: «yours», or «no-case» with the door) and one primary; the bundles answer 200, the
console's with the dashboards' partial; no traceback in the server's log (`.work/servers/srv8780.log`).

## Not done

- **The bridge in the preview.** The census gives qa-company's «Espace réservé» the key `org-bridge` («il ponte delle
  organizzazioni»), but on the preview's database that persona is typed `person` (`account_type`), so
  `portal.services.is_person_account` is true — before this merge as after it — and the address draws the person's
  dashboard without a file («pas encore de dossier»), as it drew the person's V4 dashboard before (both V5 now). No
  preview persona is an account that is not a person (an institution, a university, an authorised actor, a
  company-typed account): the bridge is seen in the area's evidence and held by its tests. The census note is W1-P's
  to correct (`apps/designpreview/live.py`).
- **The console page types' CSS** stands at its raised ceiling (DL54-87 item 3): the once-only raise is spent. The
  rows the family measured by deletion and left with their consumers — Panel, ContextHeader and the workspace head,
  HealthStrip, the meter (624 B) — and the case file's own V4 section (866 B) leave with W3-C's and W3-E's redraws.
  The Performance Lead's measure on 8782 was not made.
- **The door's paint** on the dashboard is still `v4/hero.css` in `main.css` (DL54-87 item 4): the pass that retires
  `v4/hero.css` (DL54-76 item 7 (b)) first gives the console `_door.css`, through the steward, and measures the person's
  dashboard without a file as its third page.
- **The family's own leftovers** (`NOTES.md`, «Not done, and why»): the person's register keeps `auto` end columns (a
  fixed track would narrow the titles at 1024–1440 for one shift in seven cold loads on the dev server, none on the
  twin); a case's suspension reason in its notice stays unisolated (W1-C's notice has no direction parameter);
  multi-line French on an Arabic page at 320 px wraps in its own direction.
- **Handed to other families** (`NOTES.md`, «Handed over» and «What is left, and whose»): W3-A — in forced colours the
  current rail entry draws the focus ring's outline at rest (the check's finding 5); W3-C — the register row's
  «Accepter les Conditions» (the same resolution as M1), the documents page's primary through
  `next_action(case, reader=user)`, the deadline kinds (F13), the `compact` branches left in `document_row.html` and
  `health_strip.html`; W3-D — the journey rail's redraw and the `SELECTION` mapping (`seed-person`'s file still sits on
  step 1); W2-A — the account popover, then the account's line leaves both dashboards; W3-E — Panel, ContextHeader and
  HealthStrip with their last consumers, and `companies/partials/need_table.html`, drawn by no page now.
- **Words waiting for the owner (B1)** — the copy packets in `NOTES.md` (steps 1 and 2): the ledger's group words, «Sans
  échéance», whose hands a file is in, «En attente d'un tiers», a deadline's distance in words, a total for the needs'
  ledger, «et {n} autres besoins», the bridge's sentence for an empty space. Nothing of it is shipped: every word on
  the dashboards is a catalogue string.
- **Not checked at the merge:** no browser on 8780 (by rule) — the dashboards were checked there by request only;
  Safari, Firefox, a real phone and a screen reader were never run (the area's notes).
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
