# V5.12 lane D, wave W1 (label `v512-d-w1`): notes

- **Branch:** `v512-d-w1`, built on `design-v5` at `e047fae`.
- **Worktree:** `C:/tmp/ile_wt/v512-d`.
- **Database lane:** l6.
- **Lane server:** 8786 (stopped at the end).
- **Scope:** the lane D items of the W1 row in DECISIONS.md: D-01, D-02, D-03, D-07, D-14, D-17, D-18, the Academy seed gate (D-06), the preview data cleanup and the preview hub labels.
- **Owner questions:** Q1–Q8 are not answered. Each one uses the Director's default. Every EN/AR label added here is **PROVISIONAL** (Q3) and is flagged in `docs/I18N_RTL.md` §5.

## What changed, and what the owner sees

### D-01 · The person's word is the space's name, never the role word

**Code**
- `accounts.roles.AUDIENCE_SPACE_LABELS` holds the visitor's labels:
  - person: «Espace Personnes / Area Persone / Individuals Area / فضاء الأفراد»
  - company: «Entreprise»
  - institution, university, training provider, authorised actor, professional: their glossary labels
  - staff: «Équipe du projet»
- `ROLE_LABELS` stays for the back office.
- New helpers: `audience_role()`, `space_label()` and `is_project_team()`. They follow the same order that `portal.services._audience` used before: team first, then roles, then type.
- `_audience` now reads from these helpers. Its concept table (`_AUDIENCE_CONCEPTS`) is unchanged.

**Where the owner sees it**
- **Rail foot:** «Samira El Amrani / Espace Personnes» (it: Area Persone, en: Individuals Area, ar: فضاء الأفراد).
- **Dashboard account strip:** shows the space name instead of `get_account_type_display`. This removes «Entreprise» on a person (D-09).
- **Account button:** shows the full name, never its first word. The CSS already truncates it.
- **Profile:** the «Rôles» row now appears for the back office only. The view passes `space_label` (see the request to B below).

### D-07 · The documents section has one name

- The H1, the `<title>` and the breadcrumb of `/espace-reserve/mes-documents/` and `/documents/` say «Mes documents / I miei documenti / My documents / وثائقي».
- The preview hub also says «Mes documents».

### D-14 · The person's own words

| What | Before | After |
|---|---|---|
| Responsible actor on the NowPanel, the case lines and the documents register | «La personne» | «Vous» (it: «Lei», as in DECISIONS; was «Voi») when the reader is the file's person; «La personne concernée» for third parties (`cases.presenters.responsible_label`) |
| Draft file chip (dashboard, Mes dossiers, case file) | «Brouillon» | «Étape 1 sur 7 — Votre situation et votre objectif» (`CaseFile.get_person_status_display`, built from the journey's catalogue entries) |
| Antivirus scan on the person's surfaces | always shown | hidden; only «Fichier bloqué» when the file is infected (`_person_scan_word`) |

### D-17 · The footer says the phase

- The footer says «Phase 3 / Fase 3 / Phase 3 / المرحلة 3», taken from the phase gate. Phase 2 and Phase 1 show before that gate opens.
- No release number appears in the public footer.
- `SiteSettings.version_label` now defaults to "". Migration `core/0002` empties the field where it still holds the old default.
- `site.version_label` still gives the release from `settings.ILE["VERSION_LABEL"]`, for a `<meta name="generator">`. Adding that tag is a request to A below.

### D-18 · No Italian in the French catalogue

- 72 Italian msgstr in `fr.po` are now in French, for example «Aucun titre déclaré», «Enseignement secondaire», «Post-universitaire», «date de naissance» and the rules back-office labels.
- The audit's Italian-copy check (`scripts/i18n_audit.py::unnormalised_source_msgids`) no longer has a four-word floor. Its exceptions are now listed explicitly in `SAME_IN_FRENCH` (Menu, Academy, Audit …).
- The existing catalogue tests and a new test both enforce this.

### D-06 · Academy seed gate

- `academy.catalogue` now runs only where `demonstration_data_allowed()` is true. In production, `seed_all` skips it.
- The data step `academy/0002_unpublish_demonstration_catalogue` moves the 8 seeded slugs from published to draft where demonstration data is off. Nothing is deleted. Where demonstration data is allowed (dev and preview) it does nothing.
- The providers have realistic fictional names: «Centro linguistico Valfiorita», «Institut des métiers Oued Lakhdar», «Università Collina Verde». The «(exemple)» markers are gone.
- The test fixture `academy_seeded` turns the switch on explicitly, so the compliance tests read the real seed and never an empty one.

### D-02 · Hub labels

| Element | Before | After |
|---|---|---|
| Page state | «V5 — council-passed / V4 + fondation» | «Approvata in revisione / Da rifinire» (Italian, no `lang="fr"`) |
| Strip name | «V5, la migliore di oggi» | «Italy Legal Entry™ — Anteprima di accettazione» |
| Personas menu | «Personas» | «Accessi di prova (sola lettura)» |
| Access names | French fixture names | Italian acceptance labels for all 9 keys (`personas.ACCEPTANCE`, which also covers the launcher's 5 whatever the launcher calls them) |
| Key, case reference, «dati fittizi» | shown as the name | one small grey metadata line |
| «Superfici V5» | «Superfici V5» | «Pagine approvate» |
| Build | tag shown | «Versione del 28 ottobre 2026»; tag and commit in grey |
| «Novità» | several lines per entry | one sentence per entry; details behind «I dettagli»; date and tag in grey |
| Index headings | «Stati senza credenziali», «Stato delle famiglie» … | «Da verificare senza accesso», «Avanzamento dei lavori», «Tavole del sistema visivo», «Confronto con la versione precedente», «Archivio delle proposte» |
| Page titles | «L’accesso «Il varco»», «Mes pièces — /documents/» | product titles only («L’accesso», «Mes documents»). `live.TITLES` overrides a row declared by the launcher, which still says «Mes pièces». |

### D-03 / D-19 · Preview data

New command: `manage.py preview_data_clean [--apply]`. It is defined in `apps/designpreview/preview_data.py` and is dev-only.
- It refuses any database that is not a preview database.
- Without `--apply` it is a dry run.
- It is idempotent: a second run changes 0 values.

What it does:
- Gives realistic fictional names to the 9 acceptance accounts and the demo and seed role accounts, for example «Samira El Amrani» and «Ufficio Relazioni internazionali — Comune di Valfiorita».
- Retypes `qa-doc-person` to person (D-09).
- Strips «(prova) / (fictive) / (exemple) / (données de test) / Demo —» from organisations, providers, plans, deadlines and verifications.
- Puts references into a plausible format: «RO-187264», «PRO-2026-0412», «AUT-2026-0148», «prot. 0012874/2026».
- Fixes the help-desk accents. One duplicate becomes a distinct request; the other duplicate is deleted. The census ticket is kept.
- Rewrites red-team contact request #1 as an ordinary request, because the census page `request-detail` needs pk 1. Request #2 is deleted.
- Puts a sample PDF back wherever a live document's file is missing, with its size and sha256. This is done in `--apply` only.
- Measured on `ile_v5_l6`: 80 values changed, then 0 on the second run.

## Checked on 8786

The lane server ran on `ile_v5_l6`, cleaned, with `ILE_DESIGN_PREVIEW_PORT=8786`.

- **HTTP crawl:** 4 personas × 4 languages × 6 pages: dashboard, Mes documents, dossiers, demandes, formation, profil.
  - Rail role: fr «Espace Personnes», it «Area Persone», en «Individuals Area», ar «فضاء الأفراد». The company gets «Entreprise / Impresa / Enterprise / شركة».
  - No «Personne» role word.
  - No fixture names, except the `qa-…@example.test` e-mail addresses (see «Not done»).
- **Footer:** «Phase 3 / Fase 3 / Phase 3 / المرحلة 3», with no «v2.0.0».
- **Chromium** (lock taken and released). Screenshots are in `C:/tmp/ile_v5_council/.work/v512-d-w1/shots/`:
  - hub index and «Accessi di prova» at 1440;
  - dashboard fr/it at 1440 and ar at 390 with reduced motion: «Étape 1 sur 7», «Responsable : Vous / أنتم», «Samira El Amrani»;
  - documents fr 1440 and ar 390;
  - footer fr and ar.
  - AR at 390 has no horizontal overflow (0 px).

## Budgets

- No shared CSS or JS changed. `main.css` and `shell.js` are untouched.
- The only CSS added is about 0.5 KB in `static/css/dev/designpreview.css`, which is dev-only and not in any bundle.
- No npm or dist rebuild was needed.

## Tests (targeted, `TEST_DATABASE_URL=…/test_ile_v5_l6`)

- **New:** `tests/frontend/test_terminology_v512_d.py`, 35 tests, all pass.
- **Stale tests updated, same intent:**
  - `test_console_shell_w3_a` («Espace Personnes»)
  - `test_overlays`, `test_overlays_console_w2_a` (full name)
  - `test_page_integrity` (no «Rôles» row for a person)
  - `test_release_tags_w4_d` (empty model default; the settings label still equals the tag)
  - `apps/cases/tests/test_views.py` and `apps/documents/tests/test_requirement_views.py` («Vous»)
  - `test_design_preview` (the acceptance labels, including its browser tests' strings; the footprint is now 29 files)
  - academy `conftest` (the demonstration switch)
- **Runs:**
  - Group 1: `test_console_shell_w3_a`, `test_overlays*`, `tests/i18n`, `test_release_tags_w4_d`, `test_layout`, `apps/academy`, `test_dashboard_w3_b`, `test_case_file_w3_e`, `test_documents_w3_c`. Result: **612 passed**.
  - Group 2: `test_design_preview` and the new file. Result: **332 passed**, 17 browser tests deselected and not run; their strings were updated statically.
  - Group 3: `apps/{portal,cases,documents,accounts,core,helpdesk,designpreview}` + `test_mobile_rtl_w4_a` + `tests/deployment` + env/demonstration tests. Result: **1005 passed, 3 skipped, 2 failed**. The two failures were stale «La personne» assertions in `apps/cases/tests/test_views.py` and `apps/documents/tests/test_requirement_views.py`. They now assert «Vous», and «La personne» is absent.
  - Rerun of those two files + the new file: **99 passed**.
  - Final rerun of `test_design_preview` + `tests/i18n/test_documentation.py` + `test_catalogues.py`: **360 passed**.
- **Other checks:**
  - `scripts/i18n_audit.py`: OK in all 4 languages, 100%.
  - `ruff check`: clean.
  - `makemigrations --check`: no changes.

## New msgids (catalogue pass, lane D)

| msgid | it | en | ar |
|---|---|---|---|
| «La personne concernée» | La persona interessata | The individual concerned | الشخص المعني |
| «Fichier bloqué» | File bloccato | File blocked | ملف محظور |
| «Phase 1/2/3» | Fase n | Phase n | المرحلة n |

- The Italian msgstr of «Vous» changed from «Voi» to «Lei» (DECISIONS §9).
- The entries were added by hand, with no `--sync`, to keep the diff small. `--sync` would also drop 71 stale msgids. That is for the post-wave catalogue pass.

## Requests to other lanes and the orchestrator

- **B** (`templates/accounts/profile.html`): replace the row `«Type de compte» {{ request.user.get_account_type_display }}` with `{% translate "Votre espace" %}` → `{{ space_label }}`. The view already passes `space_label`, and `roles` is empty for non-back-office accounts. «Votre espace» is a new msgid for D's pass: it Il suo spazio · en Your area · ar فضاؤكم (PROVISIONAL). Until then, the profile still shows «Type de compte : Personne/Persona».
- **A** (`templates/base.html`): add `<meta name="generator" content="Italy Legal Entry™ {{ site.version_label }}">` in the head, because the release number has left the footer.
- **Orchestrator:**
  1. After merging, run on `ile_v5`: `manage.py preview_data_clean` (a dry run), then `--apply`, from `v5-live` with the 8780 environment.
  2. Restart 8780.
  3. Optionally, in `run_8780.py`, rename the launcher's «Mes pièces» page rows to «Mes documents». The hub already overrides them.
  4. Note that `migrate` brings `core/0002` (the version label) and `academy/0002`. `academy/0002` does nothing on dev because demonstration data is allowed there.

## Not done in W1, or left for later waves

- **Academy rail entry hidden while 0 courses are published.** Moved to W2 together with `_person_rail`'s organisation branch. Hiding it changes the TEN-entry rail that dozens of tests pin.
- **The `qa-…@example.test` e-mail addresses** remain visible on the dashboard account strip and the profile. They are the switch's allow-list (dev.py and the launcher's settings). Renaming them is an orchestrator and settings decision.
- **D-19 in code:** «a document whose file is missing renders without a link» was not changed. The preview's files are restored by the command instead.
- **Other D items:** D-24 (the footer's fraud-link label) and D-22 (rail grouping) are W2/W3 items.

## Fixes after review (label `v512-d-fix-w1`)

| Finding | Severity | Fix |
|---|---|---|
| The threshold's `role="status"` word read «Chargement…» in it/en/ar (bidi-reversed in Arabic) | major | msgid «Chargement…» added to the four catalogues: it «Caricamento…», en «Loading…», ar «جارٍ التحميل…», fr itself (DECISIONS §1 T2); `.mo` recompiled, `i18n_audit.py` OK. The msgid lives in A's `header.html` / `portal_chrome.html`, so on this branch alone the audit lists it as stale (harmless); after A's merge it is in the sources. |
| The hub links `/vivre-en-italie/logement/`, `/actualites/`, `/partenaires/`, which answer 404 after C's gates | major | The three rows stay (they are census page types; `CENSUS_TYPES` and W1-0's census file are unchanged at 79) and carry a note, as the virtual Forum does: «404 finché il tema non ha una scheda pubblicata (i temi restano nascosti: Q8)», «404 finché nessuna notizia è pubblicata e la newsletter è chiusa», «404 finché nessun partner è pubblicato con l’autorizzazione scritta (G6)». |
| `specimens/icons.html:58` drew `wrench`, which left the sprite | minor | `briefcase-business`. It draws once B's W1 is merged (the symbol is B's); merge order A → B → C → D makes that so. |
| The dry run counted 69 changes and `--apply` made 80 | minor | `_sample_files` runs in the dry run too and reports each restoration without writing a file, so both counts agree. Test: `test_the_dry_run_counts_the_sample_file_restorations_it_does_not_write`. |
| `get_full_name` falls back to the e-mail address | minor | The account button (`components/account_menu.html`) and the rail's account row (`portal/partials/rail_nav.html`) show `full_name`, or «Mon compte» when there is none (existing msgid). The aria-label begins with the visible words (WCAG 2.5.3). Test: `test_an_account_without_a_name_is_my_account_never_its_e_mail_address`; `test_overlays` brought to the new markup. |
| `AUDIENCE_SPACE_LABELS` mixes a space name with identity words | minor | **Not in W1:** harmonised in W2 with Q7 (the minimal organisation space), as the review says. The dashboard strip's own e-mail address (`db-account__who`) stays: it is the account's own address, and the `qa-…` addresses are the launcher's allow-list (see above). |

- **Tests (lane l6):** `test_terminology_v512_d` (37), `tests/i18n`, `test_design_preview`, `test_icons`, `test_overlays*`, `test_console_shell_w3_a`, `apps/designpreview`, `apps/portal/tests`, browser tests deselected (72, not run; no browser was opened). Result: **941 passed**. Then `test_terminology_v512_d` + `test_overlays` + `test_catalogues` after `ruff format`: **131 passed**. `i18n_audit.py`: OK, 100 % in the four languages. `ruff check` / `ruff format --check`: clean on the touched files.
- **Orchestrator:** the dry run of `preview_data_clean` now announces the same number of changes as `--apply`.
