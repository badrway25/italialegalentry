# Lane AR — Arabic completeness — NOTES (label v524-ar-build)

Work order: FINAL_DELIVERY_V2.md §3.8 with the AMENDED SCOPE (V5.27, R7′); process V5.28 (RECOVER → COMPLETE → TARGETED
TEST → TARGETED REAL-CHROME CHECK). Branch `v524-ar`, worktree `C:/tmp/ile_wt/v524-ar`, base `4e882904` (design-v5 at the
lane's cut), recovery checkpoint `5438f4fb` («WIP recovery: Arabic V5.27 after credit interruption»).

## §R — Recovery inventory (6 Nov 2026, 08:05–08:30, from `git show --stat 5438f4fb` and `git diff 4e882904 5438f4fb`)

The previous build agent stopped on the account's credit outage; its whole tree was checkpointed as 5438f4fb (45 files,
+4 119 −76). Nothing was regenerated; the lane continues from that exact state.

### R.1 Files already changed (45)

- Policy and seam (R7′ b/c): NEW `apps/cms/locked_renderings.py` (four treatments, `TREATMENT` per key/pattern,
  `SOURCE_ROUTES`, `SOURCE_PAGE_NAME`, `DEFERRED_WHOLE`, the 139 provisional Arabic renderings `AR`, the caption and
  pointer msgids, the request-route context variable, `resolve_value`, `leaves`, `board_rows`, `counts`);
  `apps/cms/locked_content.py` (`split_key` / `_walk` and the `get()` seam only; `LOCKED_TEXTS` and the checksums
  untouched); `apps/cms/locked_split.py` (the Arabic separators «؛ » «، » for the cuts — NOT in §3.8's files: recorded);
  `apps/core/templatetags/ile_core.py` (`{% locked %}` caption / pointer / brand `bdi`, `locked_caption`,
  `locked_treatment`, `locked_is_hidden`).
- W1.1 / W5.2: `apps/cms/templatetags/cms_nav.py` (the reworded Entreprises description; the menu notice of a
  C-SUBST-FR block not said on /ar/).
- W1.4: `scripts/i18n_audit.py` (the KEEP_SOURCE row's reason re-pointed; the table is NOT empty — three rows whose
  sources are other lanes' templates).
- W2: NEW `apps/cms/team_translations.py`, NEW `apps/cms/management/commands/seed_team_translations.py`, the seed hook in
  `apps/cms/seeds.py`.
- W3.1 `apps/companies/models.py` (`TAXONOMY_LABELS`, guarded `pgettext`); W3.2 `apps/documents/services.py`
  (`REQUIREMENT_TEXTS`, `displayed_text`), `apps/documents/presenters.py`, `apps/cases/services.py` (the obligations'
  words); W3.3 `apps/academy/models.py` (`TrainingProvider.display_name`) + the four Academy templates.
- W5.3: `templates/account/login.html` («Privacy Policy» isolated `lang="en" dir="ltr"`).
- Catalogues: `locale/{ar,en,fr,it}/LC_MESSAGES/django.po|.mo` (+218 lines each).
- R7′ (f): `apps/designpreview/views.py` (two context entries), NEW `templates/dev/designpreview/_locked_keys.html`,
  `templates/dev/designpreview/index.html` (the include + the anchor).
- Readers outside §3.8's files (recorded, see R.6): `apps/orientation/templatetags/orientation_tags.py` and
  `templates/orientation/result.html` (the result's title and description by sub-key).
- Tests: NEW `tests/i18n/test_arabic_completeness.py`, NEW `tests/i18n/arabic_allowlist.py`, NEW
  `tests/i18n/test_locked_renderings_v524.py`, NEW `apps/documents/tests/test_displayed_text_v524.py`, NEW
  `apps/companies/tests/test_taxonomy_labels_v524.py`, NEW `apps/academy/tests/test_provider_display_name_v524.py`;
  changed under V5.20 (each citing V5.27 / R7′): `tests/i18n/test_locked_texts.py`,
  `tests/compliance/test_locked_content.py`, `apps/community/tests/test_virtual_forum_gate.py`,
  `apps/enquiries/tests/test_compliance.py`, `apps/pages/tests/test_services.py`.

### R.2 Implementation completed

The policy is total: 248 texts of the registry (+1 prescribed msgid), 0 unclassified, 0 stale rows; every C-UI text has
its rendering and nothing else has one — C-UI 139 · C-SUBST-FR 34 · C-SUBST-IT 59 (the six `legal.*` courtesy keys'
leaves) · C-OFFICIAL 17. The seam, the tag, the caption / pointer lines, the menu's suppression, the data seed, the
taxonomy / documents / academy readers, the login span, the dev board listing, the catalogue entries.

### R.3 Implementation incomplete

- `docs/I18N_RTL.md` §5 / §9 not updated; `LOCKED_BLOCKS_REGISTER.md` not written; these NOTES not written.
- `locked_content.split_key` handles `[n]` steps only: a dict-field sub-key of a plain key
  (`legal.cookies.fr_courtesy.title`) raises `LockedContentMissing`.
- The completeness crawl's detector flags proper names / endonyms written whole (the promoter's legal name as a
  `strong`, the language switcher's «Français» endonym).
- No build, no headed check, no measured budgets yet.

### R.4 Tests already written — see R.1 (six new modules, five changed under V5.20).

### R.5 Tests run now (targeted, `test_ile_v524_ar`, 08:06–08:26): 496 passed, 18 failed, 1 skipped

`tests/i18n` + `tests/compliance/test_locked_content.py` + the three new app modules + the five changed app modules.
The 18 reds, each a remaining defect:

| # | test | cause |
|---|---|---|
| D1 | documents ×3 | the new test calls `open_case()` without the required `purpose` (test helper) |
| D2 | `test_the_arabic_policy_never_changes_the_registry` | `split_key` does not resolve dotted sub-keys (R.3) |
| D3 | `test_the_counts_of_the_report` | the new test's guessed figures (C-SUBST-FR ≥ 40, C-SUBST-IT = 6) against the measured 34 / 59 |
| D4 | `test_every_substantive_french_text_has_its_source_route_and_its_page_name` | the page name read outside `translation.override("ar")` |
| D5 | `test_every_allowlist_entry_is_justified` | an acronym's reason under four characters («2FA») |
| D6 | reserved area ×4, case file | the detector: proper names / endonyms written whole (R.3) |
| D7 | public site, burn-down | the crawl's page floor (54 pages render 200, the test asks 60) — to verify |
| D8 | questionnaire walk | the walk reaches no result page — to diagnose |
| D9 | `test_arabic_companies_page_renders_the_title_and_keeps_the_consent_french` | the consent not found on /ar/entreprises/ — to diagnose |
| D10 | `test_rtl_browser_entrance` ×2 | the Arabic page's paragraph under the action — to diagnose |

### R.6 Remaining defects and scope notes

D1–D10 above; R.3's documentation. Two readers outside §3.8's files were changed by the previous agent
(`orientation_tags.py`, `orientation/result.html`, `locked_split.py`): they are kept (the seam's consumers; reverting
would leave French on /ar/'s result page) and are recorded as contract items for the steward's ownership manifest.

---

## §1 What the lane delivers (after the recovery)

The V5.27 hybrid policy applied in one seam, beside the registry — never in it:

- `apps/cms/locked_renderings.py` — every text of the registry classified (R7′ (a)): **C-UI 139** provisional
  professional Arabic renderings (internal status «PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW», shown only on the dev
  board); **C-SUBST-FR 34** (French source on its own page, `lang="fr"` + the Arabic caption; hidden elsewhere behind one
  Arabic pointer line naming the source page); **C-SUBST-IT 6 keys / 59 texts** (the legal courtesy translations: the
  Italian authoritative text shown by `apps/legal`); **C-OFFICIAL 17** (the trademark, the Forum's names, the address,
  the ten Italian terms, the prescribed Forum msgid).
- `locked_content.get()` asks the policy before the French fallback; sub-keys address one text of a compound value
  (`p3.faq.items[0].question`, `legal.cookies.fr_courtesy.title`). `LOCKED_TEXTS`, `locked_content.sha256.json`,
  `scripts/lock_content.py`: byte-identical (`test_checksum_file_matches_registry`,
  `test_the_arabic_policy_never_changes_the_registry`).
- `{% locked %}` (block form) adds the caption before a source-language block on its own page; `locked_caption`,
  `locked_treatment`, `locked_is_hidden`; the brand inside an Arabic rendering is one `bdi dir="ltr"` run (M1). The
  caption uses the existing label role (`t-label`): **0 CSS** (R7′ (e) not needed).
- Italian and English keep today's behaviour (the French source with `lang="fr"`): the decision is Arabic (R7′ (1)).
- W1.1 the mega-menu's Entreprises description reworded; W2 the team's data seed (116 rows per language, it/en/ar,
  idempotent, `status=PUBLISHED`, run by `seed_all` on every environment); W3.1 sectors and regions, W3.2 the requested
  pieces, W3.3 the Academy's project-team provider in the reader's language; W5.3 «Privacy Policy» isolated on the
  login; the dev board lists every key with class, treatment and status (`/__design-v5/#testi-bloccati`).

### §1.1 Fixed in this run (the remaining defects of §R)

| defect | fix |
|---|---|
| D1 | the new documents test's helpers: `open_case(…, purpose=CasePurpose.WORK)`, `declare_requirement(…, responsible_actor=…)` |
| D2 | `split_key` resolves the longest registry key followed by a step (`[n]` or `.field`): every one of the 248 texts reads back byte-identical through `get(subkey, "fr")` |
| D3 | the counts test asserts the register's exact figures (139 / 34 / 59 over 6 keys / 17) — stronger than the guessed floors |
| D4 | the page name read under the Arabic override, and asserted Arabic |
| D5 | the acronyms' reasons written out |
| D6 | the detector admits a run made only of allowlisted names; the language switcher's codes and endonyms computed from `settings.LANGUAGES` + Django's `LANG_INFO` (nothing typed; the three typed endonyms removed) |
| D7 | the public crawl's floor is the measured 54 (57 registered routes, three behind a flag that is off in tests) |
| D8 | the wizard keeps one session URL for every question: the walk replays answer sequences on fresh sessions — every choice of every question once, each branch to its result |
| D9 | the Arabic companies test opens gate G2 (`legal_published`), as its it/en twin's form does |
| D10 | **regression of the seam, fixed in AR's own template**: on /ar/ the FAQ compound resolved to Arabic (question + pointer line), so the login's assurance showed a pointer under the action; `templates/account/login.html` keeps the Privacy link alone where the answer is in its hidden form (`locked_is_hidden`) — the existing RTL test's invariant (review m3) unchanged |
| new | the crawl finds literals that TRUNCATE a prescribed text (a KEEP_SOURCE msgid, the consent acknowledgement) from the registry, and holds them in the burn-down equality |

## §2 Tool → decision → change

| tool (real, on disk) | decision | change |
|---|---|---|
| `scripts/i18n_audit.py` | the catalogues must stay 100 % with msgstr == msgid for KEEP_SOURCE | exit 0; it/en/ar/fr 3 746 msgids, 100 %, 0 fuzzy, 0 obsolete |
| the audit's detector → `tests/i18n/test_arabic_completeness.py` (`french_score`, the crawler) | detect French runs on rendered /ar/ surfaces, never «any Latin letter» (V5.27 §5) | D6–D8 and the truncation finder; 30 passed |
| native-reader second pass (the lane, in-process) | the three caption msgids, the reworded menu line and a sample of the 139 renderings read for register (formal, plural of courtesy), «، ؛ ؟», Western digits, LRM after Latin runs | no change needed; the renderings' automated guard (`test_the_renderings_are_professional_arabic_not_machine_shaped`) green |
| Playwright + chromium-1234, headed, slot CHROMIUM_LOCK_A (label v524-ar-eye, 09:01:27–09:02:47) | the V5.27 §4 rendered check at 1440 and 390 | 28 frames, 0 console errors, 0 horizontal overflow, the brand run unbroken everywhere, 0 Arabic-Indic digits, Readex Pro on every Arabic h1, «Privacy Policy» isolated (`lang="en" dir="ltr"`) |
| design tools (impeccable, taste-skill, ui-ux-pro-max, figma-*, the animation skills) | not used: no design defect was identified on the lane's surfaces (V5.28 §9: design tools only on an identified defect); design-critique and design-handoff are not installed (TOOLS_AVAILABILITY.md) and are not claimed | — |

## §3 Budgets (measured)

| item | before | after | rule |
|---|---|---|---|
| `static/css/dist/main.css` gzip -9 (Python `gzip.compress(…, 9, mtime=0)`) | 32 695 | 32 695 (byte-identical) | ≤ 32 716 |
| CSS / JS changed | — | 0 B / 0 B | 0 |
| dist after two `npm run build` | — | identical to each other and to the committed dist | — |
| catalogue msgids (each of it/en/ar/fr) | 3 702 | 3 746 (+44: 25 «companies taxonomy», 14 «document requirement», the reworded menu line, «Lire la %(policy)s», 3 «locked caption») | +42 (+3 reworded) for W1–W5; the 3 captions are R7′ (d) |
| coverage | 100 % | 100 %, 0 fuzzy | 100 % |
| data rows (team translations) | 0 | 116 per language × 3 (348) | the audit's 50 masters grew with the steps / choices / outcomes the crawl needed |
| migrations | — | none | none |

## §4 Contract items for other lanes (the burn-down equality in `tests/i18n/arabic_allowlist.py`)

`ARABIC_BURNDOWN` holds exactly what still reads French on /ar/ because another lane's file composes it; the test fails
when a row is no longer needed, so the table only shrinks; CLOSING asserts it empty. Per lane:

- **HOME** — `apps/pages/services.py` `build_pathways`: the eight titles / descriptions through
  `locked_content.get(f"p3.persons.pathways[{i}].title", lang)` and `….description` (2 rows); then `DEFERRED_WHOLE` in
  `locked_renderings.py` loses its row (AR or CLOSING).
- **PUB1** — `pathways.services.index_entries(lang)`, the sheets' h1 and the description's caption, the Parcours lead's
  caption, Universités' stations, Diplômes and Formation captions, the sheets' glossary notes hidden off their page
  (`{% locked_is_hidden %}`), `templates/ecosystem/companies.html` lines 40–43, 70 reworded as cms_nav's line (then the
  KEEP_SOURCE row goes).
- **PUB2** — the antifraud body's caption; the FAQ questions by sub-key and the answers' caption; the glossary
  definitions' caption and the related pathways' titles by sub-key; Vivre en Italie's definition hidden off its page;
  Le projet's trademark words through the seam (reader in `apps/pages/services.py`, HOME's file); the Forum's programme
  lines and speakers' roles by sub-key; `templates/forum/partials/hero.html` and `templates/living/topic.html` literals
  (KEEP_SOURCE); `apps/faq/services.py:47` and `templates/pages/contact.html:52` «Privacy Policy» isolated with the new
  msgid «Lire la %(policy)s».
- **CLOSING** — the companies' and the Forum's consent captions in the preserved forms; `apps/consents/services.py`
  `ACKNOWLEDGEMENT_TEXT` (a truncation of the prescribed consent, declared French on the contact, institutions and
  universities forms); `templates/components/formwork_side.html:12` «Privacy Policy» isolated; the burn-down empty.
- **Steward (ownership manifest)** — three readers outside §3.8's files were changed by the build and are kept (the
  seam's consumers; reverting would leave French on /ar/): `apps/cms/locked_split.py` (the Arabic separators for the
  cuts), `apps/orientation/templatetags/orientation_tags.py` and `templates/orientation/result.html` (the result's
  title / description by sub-key), plus `apps/designpreview/views.py` (two context entries for the listing). Five
  existing tests changed under V5.20, each docstring citing V5.27 / R7′ with the same or a stronger invariant:
  `tests/i18n/test_locked_texts.py`, `tests/compliance/test_locked_content.py`,
  `apps/community/tests/test_virtual_forum_gate.py`, `apps/enquiries/tests/test_compliance.py`,
  `apps/pages/tests/test_services.py` (it/en keep the French-with-lang assertions; ar asserts the rendering, or the
  French isolated for a substantive text); and in this run, on the same rule, `apps/enquiries/tests/test_company_form.py`
  (the labels: it/en unchanged, ar the rendering with the consent still `fr`), `apps/orientation/tests/test_wizard.py`
  (the Arabic result's route sentence in Arabic, never French) and AR's own `apps/companies/tests/test_models.py` (never
  an empty cell; the catalogue's Italian for a seeded sector). `taxonomy_label` now reads an editor's Italian label
  before the catalogue (a back-office edit is never overridden).

Contracts applied from other lanes: T's label role (`t-label`) for the caption; T's `bdi[dir="ltr"]` rule for the
brand run (M1); no BACKGROUND_MATERIAL attribute and no PX attribution concerns this lane's files.

## §5 New msgids (professional it / en / ar; the Arabic reviewed)

| msgid (fr) | it | en | ar |
|---|---|---|---|
| «Texte source en français — traduction arabe en cours de validation.» (locked caption) | Testo sorgente in francese — traduzione araba in corso di validazione. | Source text in French — Arabic translation pending validation. | النص المصدر بالفرنسية — الترجمة العربية قيد التحقق. |
| «Texte italien faisant foi — traduction arabe en cours de validation.» (locked caption) | Testo italiano facente fede — traduzione araba in corso di validazione. | Authoritative Italian text — Arabic translation pending validation. | النص الإيطالي المعتمد — الترجمة العربية قيد التحقق. |
| «Texte source en français sur la page « %(page)s » — …» (locked caption, the pointer line) | Testo sorgente in francese nella pagina «%(page)s» — traduzione araba in corso di validazione. | Source text in French on the page “%(page)s” — Arabic translation pending validation. | النص المصدر بالفرنسية على صفحة «%(page)s» — الترجمة العربية قيد التحقق. |
| «Faites connaître les métiers et les compétences dont votre entreprise a besoin.» | Fate conoscere i mestieri e le competenze di cui la vostra impresa ha bisogno. | Tell us which trades and skills your company needs. | أعلِمونا بالمهن والكفاءات التي تحتاجها شركتكم. |
| «Lire la %(policy)s» (the policy name a `lang="en"` span) | in the catalogue | in the catalogue | in the catalogue |
| 25 × «companies taxonomy», 14 × «document requirement» | the audit's `fragments/it.po`, compiled | `fragments/en.po` | `fragments/ar.po` (Arabic reviewed in the audit) |

## §6 The three counts (V5.27 §8)

- Unintended French fallback on /ar/: **0** outside the burn-down equality's rows, which are the page lanes' contract
  items (§4) and reach 0 when those lanes merge and CLOSING empties the table.
- Provisional non-legal Arabic: **139** texts (C-UI).
- Untranslated authoritative legal blocks: **34 C-SUBST-FR** texts (French source identified on its page, hidden
  elsewhere) + **6 C-SUBST-IT** keys / 59 texts (the Italian authoritative text shown by the legal pages).

The owner question of R7 is closed as answered by V5.27 (the hybrid policy); option B is superseded (R7′).

## §7 Tests run (targeted, `test_ile_v524_ar`, one pytest at a time)

- §R baseline: 496 passed, 18 failed, 1 skipped (08:06–08:26).
- Targeted re-runs after each fix: the completeness module 30 passed; the renderings, locked-content and documents
  modules 51 passed, 1 skipped (the dev board's index test skips where the preview app is off); the Arabic companies
  test, the questionnaire walk, `test_rtl_browser_entrance.py` (headless, no slot) 13 passed.
- Non-browser targeted run (tests/i18n, tests/compliance, apps/cms, core, companies, documents, academy, cases,
  orientation, enquiries, the virtual Forum gate, pages services, designpreview; `--create-db`, 09:23–09:58):
  **1 378 passed, 3 failed, 1 skipped** — the three reds were existing tests asserting the French on /ar/ or in Italian
  where W3.1 / R7′ now render the reader's language; amended under V5.20 (§4) → 131 passed on their modules.
- Browser (headless, no slot): `tests/i18n -m browser` **47 passed**.
- An earlier broad run (08:51) was stopped and its orphaned pytest processes killed when they were found sharing the
  test database with the next run (R12); the 09:23 run above is on a fresh test database.
- Checks: `manage.py check` 0 issues; `makemigrations --check` no changes; ruff check and format clean on the lane's
  29 Python files; `scripts/i18n_audit.py` exit 0.

Stills: `C:/tmp/ile_v5_council/evidence/v524/ar/shots/` (14 Arabic pages × 1440 / 390, viewport + full page,
`measures.json`). The lane server 8791 (ile_v5_l7, migrated, `seed_all` → 348 team rows) stopped after the check.

## §8 Fix round `v524-ar-fix` (6 Nov 2026, the targeted check's findings)

Blockers (both fixed):

- **B1 — `/__design-v5/index/` answered 500 on the lane server.** `{{ locked_counts.C-UI }}` does not parse (a Django
  template cannot read a hyphenated key). `cms.locked_renderings.template_counts()` gives the counts as `c_ui`,
  `c_subst_it`, `c_subst_fr`, `c_official`. The view passes that, and `_locked_keys.html` reads it. The index test now
  skips only on 404 and asserts 200 and the four counts otherwise. A new test renders the fragment directly, so the
  break is caught even where the preview's URLs are not mounted. It was red on the old template and is green now.
  Commit `14101cb9`.
- **B2 — the need form's options were in French (`Vénétie`, `Agroalimentaire et transformation`) on /it/, /en/ and
  /ar/.** A ModelChoiceField prints `__str__`, and `__str__` returned `label_fr`. `Sector.__str__` and
  `Territory.__str__` now return `taxonomy_label(self)`, so the profile form's sector select is fixed as well. New
  tests: the need and profile forms' options in it/en/ar, and the `nouveau/` page's `<option>` text in it/en/ar (6
  tests, red on the old `__str__`). The completeness crawler now flags an `<option>` that prints a taxonomy French
  source, whatever its length (one word such as «Vénétie» falls under the detector's three-word floor). A new crawl
  serves the need form to a company with its profile. The existing T3 company crawl has no profile, so the form never
  reached it, which is why B2 escaped. That crawl was red on the old `__str__` (25 option leaks) and is green now.
  Commit `2d384e6b`.
  - One side effect, recorded: the audit metadata `companies.need.created` → `territory` is `str(territory)`, so it now
    follows the reader's language. This matches the record's existing `note` (`str(_("Besoin créé."))`). It does not
    change the key (`territory_id` / the target).

Minors:

- `apps/orientation/tests/test_wizard.py`: the Arabic result now asserts the full C-UI rendering of
  `p3.persons.how_it_works` as the disclaimer's text, and that the disclaimer is in no `lang="fr"` run. The French
  sentence is still asserted absent. This is a stronger invariant (V5.20). Commit `6788fb0f`.
- The comments and docstrings the formatter broke were re-wrapped by hand in `apps/cms/locked_renderings.py` (module
  docstring, `DEFERRED_WHOLE`, the renderings header, `current_route`, `treatment`, `is_hidden`, `resolve_value`,
  `counts`), `apps/companies/models.py`, `apps/documents/services.py`, `apps/cms/locked_split.py`,
  `apps/orientation/templatetags/orientation_tags.py`, `apps/community/tests/test_virtual_forum_gate.py` and
  `apps/pages/tests/test_services.py`. Commit `fc8387a8`.
- The crawler reads option text: done with B2.
- For the steward, not fixed here: the files outside §3.8's list (already in §4) go into the v524-ar family's slices.
  `KEEP_SOURCE` (3 rows) and `ARABIC_BURNDOWN` (~70 rows, all other lanes' templates) are re-measured at merge, and
  CLOSING asserts them empty.

Tests run (`test_ile_v524_ar`, one at a time):

- Renderings module: 25 passed, 1 skip (the 404 skip).
- `apps/companies`: 111 passed.
- Completeness module: 31 passed.
- orientation + community gate + pages services + documents + cms + renderings + companies: **522 passed, 1 skipped**.
- `manage.py check` 0 issues; ruff check and format clean.

Headed check under the slot (CHROMIUM_LOCK_A, label v524-ar-fix):

- Script: `.work/v524-ar/tools/headed_fix.py`, on lane server 8791 (ile_v5_l7, `ILE_DESIGN_PREVIEW_PORT=8791`).
- At 1440 and 390: the index returns 200 with the four counts (C-UI 139 · C-SUBST-FR 34 · C-SUBST-IT 59 · C-OFFICIAL
  17), and there are 0 page errors.
- As qa-company, `mes-besoins/nouveau/` returns 200 in ar/it/en. It shows 13 sector and 14 territory options in the
  reader's language (ar «فينيتو», «الصناعات الغذائية والتحويل»; it «Veneto»; en «Lombardy»), with 0 French source
  options and 0 overflow.
- Stills and `measures.json`: `C:/tmp/ile_v5_council/evidence/v524/ar/shots-fix/`. The lane server was stopped after
  the check.

Found, not fixed (outside this round's list; for the steward / CLOSING; these are not caused by the round):

- Eight existing tests outside the lane's earlier targeted set still assert French on /ar/, where R7′ now renders the
  provisional Arabic or the reader's language:
  - `tests/frontend/test_dashboard_w3_b.py::test_a_french_record_keeps_its_language_and_direction_on_an_arabic_page`
    (W3.2 renders the seeded piece's title).
  - `tests/frontend/test_cms_nav.py::test_portico_glosses_and_second_lines_carry_their_language` and
    `::test_portico_notice_stands_in_every_language_and_one_item_is_current`.
  - `apps/ecosystem/tests/test_companies_page.py::test_page_is_online_in_every_language_with_both_gates_closed[ar]`
    and `::test_arabic_page_is_rtl`.
  - `apps/portal/tests/test_compliance.py::test_access_point_partial_renders_title_body_and_button_for_anonymous_visitors`.
  - `apps/portal/tests/test_platform_v515_d.py::test_the_organisations_presentation_is_folded_verbatim_under_its_word[ar]`.
  - `apps/portal/tests/test_views.py::test_four_languages_render_with_correct_direction[ar]`.

  Seven of them were re-run with the round's `__str__` change reverted (the `[ar]` parameter of the companies page
  was not), and all seven still failed. They need the V5.20 amendment (the approved
  decision R7′ cited, with the same or a stronger invariant asserting the Arabic rendering), as §4 did for the earlier
  three.
