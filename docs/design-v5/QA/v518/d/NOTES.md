# Lane D (v518-d-fix) — V5.18 stabilisation pass

- 29 October 2026. Worktree `C:/tmp/ile_wt/v518-d`, branch `v518-d` from `design-v5` `238dc1c` (W3 merged: v515/a, c,
  b, d). Database lane l6 (`ile_v5_l6`, tests on `test_ile_v5_l6`); lane server 8786 (launcher outside the repo:
  `C:/tmp/ile_v5_council/.work/v518-d/srv/run_8786.py`; the v515-d server that still held the port since 14:57 was
  stopped first).
- Binding: V5.18 §2 «Do not use stabilisation as an excuse for another broad redesign» — every change below is a
  targeted fix of an audited item (`evidence/v518/AUDIT_quality.md`, `AUDIT_resp.md`, `workflows_v515/v518_findings.json`)
  or of lane D's merge carry-overs (DL54-174). No locked text reworded, no machine translation, no new msgid.

## Items

| Item | What changed | Where |
|---|---|---|
| **P-3 / m-5** — the locked French «ESPACE RÉSERVÉ» head on the it/en/ar no-case dashboards (fresh person, company) | S1 §3.10 («texte du point d’accès à l’espace réservé», `docs/REQUIREMENTS_MATRIX.md` R-P3-035, `CONTENT_SOURCE_MAP.md`) prescribes the access point's title, sentence and button **in French**, with no official it/en/ar version (`locked_content` falls back to French). The dashboard keeps the locked pair **only where it is written — French** (`locked_is_fallback`): `/fr/espace-reserve/` is unchanged and `test_compliance` still finds the locked title as the single h1. In it/en/ar the head is the console's own, as on every other dashboard: «Tableau de bord» (existing msgid: «Pannello di riepilogo», «Dashboard», «لوحة المتابعة») and, for a person, the page's own translated sentence (existing msgid «Votre espace personnel : parcours, documents, échéances et communications.»); the company's head has no lead (its identity sheet follows, as the organisations' heads). Nothing reworded, nothing translated. | `templates/portal/dashboard.html` |
| **M-2** — the company space (and the console's remaining static pages) had no atrium head and no motion | Every page of «Espace entreprise» now opens on lane D's atrium, as the person and organisation spaces do: `data-atrium="company"` (the blue wash), the **seal** figure with the audience's glyph (`atrium_seal = icons.AUDIENCE["company"]`, set once in `companies.views._render`), the eyebrow = the account's space name (`atrium_eyebrow.html`: «Espace Entreprises» / «Area Imprese» / «Enterprises Area» / «فضاء الشركات»; on the company dashboard it replaces the bare «Entreprise», the same rule lane D applied to every atrium page in round 2), the phone band. The main column gets `.db-main` beside `.reg-page` so lane A's existing `c-rise` applies (no new animation; the registers' sheet is linked after the console's, so `.reg-page`'s own gap still wins: no layout change). Pages: dashboard, «Mes besoins», a need, «Mon entreprise», the need and identity forms, the territorial analysis (staff). The person's remaining static pages got the same: «Déposer un fichier», «Dépôt indisponible» and a piece's page (the atrium head only: a piece's `<article>` is taken whole into the drawer, and on the upload page a rise under the depot's frame moved its measured box — see Tests), «Pré-évaluation» (head and `c-rise`). `platform.css` linked on each. Not touched: the forum governance and selection workspaces (other products, not in the audit). | `templates/companies/*.html` (7), `templates/documents/{upload,terms_required,requirement_detail}.html`, `templates/cases/assessment.html`, `apps/companies/views.py` |
| **m-6** — 11 gradients in `apps/portal/static/portal/v5/_platform.css` (`test_conforming_app_stylesheets_use_only_design_tokens` red) | The gradient declarations moved, unchanged, to a new design-system partial `static/css/v5/_platform-grounds.css`, imported by `apps/portal/static/portal/platform.css` right after `v5/_platform.css` (page-only, as before; never main.css/console.css). Why not `tokens.css`: these images read values that only exist on the drawing element (`--atrium-wash` per audience, `--spot-x/--spot-y` from the pointer, the console's `--surface-area`), which a `:root` token cannot hold, and `tokens.css` is in main.css, at 33 448 / 33 600 B gzip with «no further rise» (DL54-170). Same selectors, same order, one import later; the two planes `_platform.css` repaints for forced colours and print (atrium, calm panel) are wrapped in `@media screen and (forced-colors: none)` so that repaint still wins. Measured identical: computed `background-image`, `mask-image`, `background-color` of every moved rule on 8780 (base) vs 8786, qa-doc-person / qa-institution / qa-fresh-person, fr+ar, 1440+390 — 12/12 equal (`probe_m6.json`). No non-conforming row needed. | `static/css/v5/_platform-grounds.css` (new), `platform.css`, `_platform.css`, `static/css/dist/portal/platform.css` |
| **Bridge order (4)** and **c-rise (18)** in `test_dashboard_browser_w3_b` | See *Tests*. | `tests/frontend/test_dashboard_browser_w3_b.py` |
| **B-1** — «Démonstration : état positionné par la commande companies_demo.» in the need history | The seed now writes the sentence a project team would write at that step (`DEMO_TRANSITION_NOTES`: «Besoin transmis à l’équipe du projet.», «Besoin reçu par l’équipe du projet ; son examen est en cours.», «Besoin pris en charge par l’acteur autorisé.»), by the need's state. The preview's three existing rows: the script outside the repo (below). | `apps/companies/management/commands/companies_demo.py` |
| **P-8** — 7 hub research links answering 404 | Not in `apps/designpreview`: the links are inside the four uiux-platform proposal pages (`proof/research/uiux-platform/proto/{shell,docs}-{fr,ar}.html`), copies of gate-0 comps two folders deeper than their originals. Their build script now rewrites the page's own links (language switch → the proposal's own pair; the console's home → `shell-fr/ar.html`; the dépôt and the chips → `../../../documents/…`) and the pages were rebuilt: only `href`s changed (diffed). Crawl of the four pages on 8780: **0 broken** (was 14 references / 7 URLs). | outside the repo: `C:/tmp/ile_v5_council/proof/research/uiux-platform/proto/build.py` + the 4 pages (before: `.work/v518-d/proto_before/`) |
| **P-9** — «Diplome» on the private document's description | Same script as B-1 (below). | outside the repo |
| **T3** — stale tests of lane D's families | `tests/i18n/test_routing.py`: floor 23 ungated routes, plus the three substantive legal pages asserted gated by `legal_pages` (never dropped). `tests/frontend/test_nav_sheet_w2_c2.py`: the account popover's label read on an account with a name («Personne Essai — Mon compte», exact), plus a new nameless case («Mon compte» alone, no dash). `apps/portal/tests/test_views.py` (found red on the base, same family): the empty state is lane B's tile (`empty-state empty-state--tile`, exact), and the it/en/ar dashboard no longer shows the French fallback (P-3) but the translated «Tableau de bord» h1. | tests |


## Tests

Lane l6 (`TEST_DATABASE_URL=…/ile_v5_l6` → `test_ile_v5_l6`), one pytest at a time; browser runs under the Chromium
lock (17:30–17:39 and 18:23–18:40, label `v518-d-fix`).

- `apps/portal` + `apps/companies` (not browser): 405 passed, **5 failed → fixed**: `test_views.py` ×5 (the two
  empty states read lane B's tile class; the it/en/ar dashboard reads the translated head, P-3) → `test_views.py`
  **35 passed**.
- `tests/i18n/test_routing.py`, `tests/frontend/test_nav_sheet_w2_c2.py`, `apps/portal/tests/test_compliance.py`,
  `tests/frontend/test_design_docs.py`: **93 passed** (m-6: `test_conforming_app_stylesheets_use_only_design_tokens`
  green; the FR dashboard's locked h1 still checked by `test_compliance`).
- `apps/documents apps/cases apps/designpreview tests/i18n tests/compliance` + 25 frontend files touching the changed
  templates/sheets (bundle, pipeline, tokens, O14, RTL, terminology, documents, dashboard, console, chips…):
  **2381 passed, 3 skipped, 16 failed** — the **same 16 fail on `design-v5` 238dc1c** (run there on the same lane):
  `_fronte.css` ×3 (T1/T2 and its literal `#000`, lane C), `test_service_pages_w3_f2` ×10 (account frames, the
  situation's `country_of_residence`, the 400/500 pages), `test_journey_w3_d` (`_compose.css` passage), `test_mobile_rtl_w4_a`
  (500), `test_o14_lint` (`check` in `partials/header.html`, lane A). None is in a file this lane changed.
- Browser: `test_dashboard_browser_w3_b.py` **26 of 27** — the 18 `c-rise` and the 4 bridge-order failures are
  green:
  - **c-rise (T3):** `SETTLE_JS` now also waits out lane A's `c-rise` when it is finite (after the arrival's veil has
    lifted: `html.lume-in` moves the rise's delay), and the «moving» gates admit a `c-rise` **only once finished**
    (`RISEN`: `c-rise` fills `both`, so an ended rise stays in `getAnimations()`); anything still running, or any
    other animation, is still «moving»; under reduced motion the existing tests still require **no** animation.
  - **bridge order:** an institution now has its own dashboard (V5.12 Q7, V5.15 lane D), whose registers are drawn
    only with rows (D-20): the expected order is `deadlines, messages, organisation`; the rest of the gate (no
    NowPanel, no primary, no shadow, no overflow, nothing moving, rows on the reading edge) is unchanged.
  - still red, not in this lane's list and present before: `test_the_one_primary…[390x844-fr]` — a `12px` corner
    (the DRAFT chip at 390-fr, recorded in v515/d NOTES as pre-existing).
- `test_platform_browser_v515_d.py`, `test_documents_browser_w3_c.py`, `test_drawer_browser_w3_c.py`,
  `test_depot_browser_w3_c.py`: **84 + 1** → the one failure (`the zone keeps its size`, 76 vs 75.99997 on
  `/documents/upload/`, measured during the rise) came from this lane's `.db-main` on the upload page: removed there
  and on «Dépôt indisponible» (the atrium head stays) → depot **14 passed**.
- `ruff check` clean on the changed Python (one E501 in `test_views.py` predates this lane).

## Headed check

Headed Chromium 1234 on 8786 (this branch) and 8780 (design-v5, for m-6), probe `C:/tmp/ile_v5_council/.work/v518-d/probe.py`,
results and shots `C:/tmp/ile_v5_council/evidence/v518/d/` (`probe_p3.json`, `probe_m2.json`, `probe_m6.json`).

- **P-3**, qa-fresh-person and qa-company, fr/it/en/ar × 1440/390: fr keeps «ESPACE RÉSERVÉ» + the locked sentence
  (`lang` fr on a fr page); it «Pannello di riepilogo» / en «Dashboard» / ar «لوحة المتابعة», each `lang` = the page,
  under the translated eyebrow; the person's lead translated, the company without a lead; 0 px horizontal scroll;
  the company's seal glyph within 0.15 px of its ring (`p3_*.png`; `p3_qa-fresh-person_ar_390.png` is the audited
  screen).
- **M-2**, qa-company (dashboard, «Mes besoins», a need, «Mon entreprise») and qa-doc-person («Déposer un fichier»),
  1440/1024/768/390, fr+ar, motion and reduced motion: atrium on every page, the seal glyph within 0.3 px of its
  ring, the band on phones, 0 px horizontal scroll, 8–20 finite animations at load, **none running after 2.6 s,
  none infinite, 0 under reduced motion**; the first block stays 12–24 px under the head (no layout change). The
  territorial analysis answers «Accès non autorisé» to a company (staff page): head unchanged for it.
- **m-6**: 12/12 identical computed grounds base vs branch (above); forced colours/print repaint untouched by design.

## Outside the repository (for the merge steward)

- `C:/tmp/ile_v5_council/servers/acceptance/fix_preview_text_v518d.py` — **to be run by the merge steward**, on `ile_v5`
  only (`_env` refuses anything else before a query): dry run by default, `--apply` in one transaction, idempotent.
  It matches only the exact values: the 3 `companies.NeedEvent` rows with the demonstration note (pk 2, 4, 6 →
  the sentence of their `to_status`) and the 1 `documents.PrivateDocument` with «Diplome ou titre de formation»
  (→ «Diplôme …»). Dry run done by this lane (read-only): 3 + 1 rows found, nothing written.
- The P-8 rebuild (`proof/research/uiux-platform/proto/`), already live on 8780 (the hub serves the folder).
- Lane server 8786 still runs the v518-d tree (`.work/v518-d/srv/run_8786.py`); stop it after the merge.


## Not done / for others

- `test_dashboard_browser_w3_b::…[390x844-fr]` — the 12 px corner (DRAFT chip), pre-existing, not in this list.
- The bridge proper (`portal/dashboard.html` `db--bridge`, now drawn for a professional account only) has no browser
  test of its own since the institution moved to its dashboard; the institution test now guards the organisation
  dashboard. Worth a professional-account case in a later round.
- The w3-b test ownership crossing (DL54-174): this round edits `tests/frontend/test_dashboard_browser_w3_b.py`
  again (settle + RISEN + the institution's order) — please confirm at merge, as for v515-d.
- Not this lane's (seen while testing, same on design-v5): the 16 non-browser failures listed above (lanes A/B/C).
- Forum governance and selection workspaces keep their own heads (not console families in the audit).
- No new msgid: no catalogue pass needed for this lane.

## v518-d-refix (after the integrated review) — the case step chip on phones

- **Finding** (polish): «Étape 1 sur 7 — Votre situation et votre objectif» wrapped inside the chip at fr 390/360
  (qa-doc-person dashboard and «Mes dossiers», it 390): a two-line, 44 px plate with a 12 px corner — also the
  pre-existing `test_dashboard_browser_w3_b::…[390x844-fr]` corner failure listed above under «Not done».
- **Fix**: the step title moves out of the chip (the review's second option; chip.css says a chip's word wraps and is
  never cut, so no ellipsis). `CaseFile.get_person_status_parts()` gives the chip's word («Étape 1 sur 7», or the
  state's own label) and the step's title ("" for every other state); `get_person_status_display()` is composed from
  it and unchanged. Dashboard and file heads: the chip, then `<span class="ctx__step">` in `.ctx__meta` (its own
  flex item, the meta's ink-2). «Mes dossiers»: the chip says the rank in the state cell, the title is the first
  span of the row's meta line (`.reg-row__step`). No new msgid, no CSS, every language at every width.
- **Headed check** (8786 restarted on the branch, `probe_chip.py` → `evidence/v518/d/refix/`): qa-doc-person,
  fr/it/en/ar × 1440/390/360, dashboard and «Mes dossiers»: every case chip 24 px on one line, corner 12 px = full,
  title beside it, 0 px horizontal scroll; screenshots fr/ar 390/360. qa-waiting-person could not be entered on
  l6 (the strip redirects to login) — its file is not DRAFT, so its chip is the state's own label, unchanged.
  Process note: the first run started while another lane held CHROMIUM_LOCK (the noclobber write failed and the
  script was not gated on it); the lock was free when checked right after, then taken properly for the test run.
- **Tests** (l6): `test_terminology_v512_d` extended to the split (chip word, `ctx__step`, `reg-row__step`, another
  state's empty title); `test_terminology_v512_d` + `test_dashboard_browser_w3_b` + `test_dashboard_w3_b` +
  `test_platform_browser_v515_d`: 153 passed — the `[390x844-fr]` corner now passes.
- Wider non-browser sweep (l6): `test_case_file_w3_e`, `test_console_shell_w3_a`, `test_organisation_space_v512_d`,
  `test_overlays_console_w2_a`, `apps/portal/tests/test_held_file` + `test_navigation_reaches_every_surface`, and
  `tests/i18n`: 550 passed, 6 failed — all on the public pages/`static/css/v5/_fronte.css` (RTL viewport fit, the
  trademark sign, the architrave's entries, a physical `text-align: right` in `_fronte.css`), none touching a file of
  this refix (no CSS changed here): lane A's, reported, not fixed here. Process note: `tests/i18n` holds browser tests
  and ran outside CHROMIUM_LOCK (headless, by the pytest live server); flagged for the steward. The extended
  `test_terminology_v512_d`: 40 passed.
