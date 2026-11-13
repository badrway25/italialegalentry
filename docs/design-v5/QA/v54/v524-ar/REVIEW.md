# Lane AR — the reviewer's targeted gate (label v524-ar-qa) — 6 Nov 2026

Branch `v524-ar`, head `737c4552` (base design-v5 `f8b8ed4a`). Gate: FINAL_DELIVERY_V2.md §3.8 items (1)–(6) plus the
amended items (V5.27, R7′); targeted (V5.25 §2), no full matrix, no six-dimension re-scoring (no composition change).

**Verdict: FAIL — 2 blockers.** Everything else holds.

## Blockers

| # | where | what was found | fix |
|---|---|---|---|
| B1 | `templates/dev/designpreview/_locked_keys.html` (R7′ (f)) + `tests/i18n/test_locked_renderings_v524.py:402` | `/__design-v5/index/` returns **500** on the lane server: `TemplateSyntaxError: Could not parse the remainder: '-UI' from 'locked_counts.C-UI'`. A Django template cannot read a dict key with a hyphen in it. The base (8780) returns 200, so the owner's preview index breaks at merge. The test that should catch this skips on **any** non-200 status, so it skipped the 500 as well (the «1 skipped» in the run). | Give the counts keys a template can read (e.g. `{"c_ui": …, "c_subst_fr": …, "c_subst_it": …, "c_official": …}`), or pass a list of (class, count) pairs. Make the test skip only on 404 and assert 200 otherwise. |
| B2 | `apps/companies/models.py` `Sector.__str__` / `Territory.__str__` (W3.1; gate (3) «needs list **and form** (sectors, regions)», gate (4)) | On `/ar/espace-reserve/entreprise/mes-besoins/nouveau/` (persona qa-company) the `territory` and `sector` select options read French: «Vénétie», «Lombardie», «Agroalimentaire et transformation»… The same French shows on /it/ and /en/. The form's ModelChoiceField prints `__str__`, which is `label_fr`, and `taxonomy_label` is never called. The options carry no language marker, so this is visible unintended French on /ar/. The list page (`mes-besoins/`) is correct in all three languages (لومبارديا / Lombardia; الصناعات المعدنية والميكانيكية). The completeness crawler does not read `<option>` text, which is why it stayed green. | Make the options read the label: have `__str__` return `taxonomy_label(self)` (a file AR owns), or set the form fields' `label_from_instance`. Add a test that the need form's options read the catalogue's rendering in it/en/ar, and have the crawler read option text. |

## Gate items

1. **Catalogues and tests: HOLDS.**
   - `scripts/i18n_audit.py` exits 0.
   - The targeted non-browser run on `test_ile_v524_ar` (`--create-db`, 17 min 32 s) gave **778 passed, 1 skipped**. It covered tests/i18n, tests/compliance/test_locked_content.py, the three new app modules, apps/companies/tests, apps/documents/tests and the six changed app modules. That includes T1–T5, `test_locked_renderings_v524.py`, `test_locked_derived_msgids_are_never_translated`, `test_no_unreviewed_locked_fragment_in_the_catalogue` and `test_checksum_file_matches_registry`. The one skip is B1's masked 500.
   - `KNOWN_FRENCH = {}`. Every allowlist entry has a reason (`test_every_allowlist_entry_is_justified`).
2. **Rendered crawl of /ar/: HOLDS, with contracts.**
   - Every French run left on the 19 Arabic surfaces is marked `lang="fr"`. Each is one of these:
     - a C-SUBST block on its own page with its caption (home 6, pathway sheet 7, antifraud 1, AGAMI 1, diplomas 4, the questionnaire result 1);
     - a C-OFFICIAL name (the Forum's title);
     - an `ARABIC_BURNDOWN` / `KEEP_SOURCE` row owned by HOME, PUB1, PUB2 or CLOSING (the home's pathway index, the sheets' h1, the FAQ questions and the answers' caption, the glossary definitions' caption, «Signalez les besoins…», the Forum's eyebrow);
     - D-demo content (the Academy's course data, the persona's own document note).
   - The register's counts are tested exactly: C-UI 139, C-SUBST-FR 34, C-SUBST-IT 59 over 6 keys, C-OFFICIAL 17.
   - **Exception: B2.** The need form's options are unmarked French.
3. **Headed check: HOLDS, except B2.**
   - Run under CHROMIUM_LOCK_A (label v524-ar-qa, 10:27–10:28, chromium-1234), /ar/ at 1440 and 390: **38 frames** across 19 surfaces.
   - Surfaces: home, the `salaried_work` sheet, Entreprises and its form, FAQ, glossary, Attention aux fraudes, Forum, AGAMI, Diplômes, login, contact, questionnaire step 1, a questionnaire result (walked), the person's dashboard («now» card), the case file, the Academy catalogue, the company's needs list and new-need form.
   - Every frame: 200, `dir="rtl"`, 0 console errors, 0 horizontal overflow, 0 Arabic-Indic digits, the brand run on one line at every width, Readex Pro 600 on every Arabic h1.
   - axe-core on 22 frames: 0 serious/critical violations.
   - «Privacy Policy» on the login is isolated (`lang="en" dir="ltr"`). The unisolated one on the contact page (`contact.html:52`) is PUB2's contract.
   - The provider shows as «فريق المشروع Italy Legal Entry™». The requested documents read Arabic (شهادة أو مؤهل تكويني; تصريح «Nulla osta» للعمل).
   - Reduced motion: 0 animations still running after settle on home, login and needs form. Keyboard: the first Tab lands on the skip link with a visible 1.6 px outline, and 6 of the next 12 stops show an outline.
4. **it/en twins: HOLDS, except B2.**
   - Run headless, no slot: 72 frames.
   - The provider shows as «Team del progetto» / «Project team».
   - The needs list's sectors and regions read Italian (Lombardia, Metallurgia e meccanica) and English.
   - The case file's documents read Italian / English («Diploma o titolo di formazione», «Work nulla osta»).
   - The persona's passport row stays French together with its note («Pages d'identité uniquement.»), because the note is the persona's own text with no rendering. That is the designed isolation, not a defect.
   - The form's options are French (B2).
5. **Locked copy: HOLDS.**
   - `apps/cms/locked_content.sha256.json` and `scripts/lock_content.py` are unchanged. `LOCKED_TEXTS` is untouched; the diff is the `get()` / `split_key` seam only.
   - Every one of the 248 texts reads back byte-identical through `get(subkey, "fr")`.
   - No catalogue translates a locked text (tests green).
6. **Owner question: HOLDS.** It is closed as answered by V5.27. The three counts are in NOTES §6; the DL entry is the steward's.

## Other checks

- **Contact channels:** tel, WhatsApp and mailto on /fr/ /it/ /en/ /ar/contact/ are identical between lane 8791 and base 8780 (sha-256 compared in process; no value printed).
- **Budgets:**
  - main.css is 32 695 B gzip -9, within the ceiling of 32 716.
  - 0 CSS and 0 JS changed. Two `npm run build` runs came out identical to each other and to the committed dist (tree clean).
  - No migration.
  - The catalogue is +44 msgids per language, 100 %, 0 fuzzy.
- **Tests changed under V5.20:**
  - Eight existing tests changed: `test_locked_texts`, `test_locked_content`, `test_virtual_forum_gate`, `test_compliance`, `test_company_form`, `test_services`, `test_wizard` and `companies/test_models`.
  - Each cites V5.27 / R7′. Each keeps the it/en French-with-lang invariant and asserts the Arabic rendering, or the isolated French, on /ar/. None is loosened in substance.
  - `test_wizard` drops `'lang="fr"' in html` for the Arabic result and checks only the route sentence's first clause (m3).
- **Preserved families:** untouched beyond the login span (W5.3, owned). No CSS, so no family's styling moved.
- **Contract items for the other lanes:** all written in NOTES §4 (HOME, PUB1, PUB2, CLOSING, steward).

## Minors (recorded)

- m1 — There are readers outside §3.8's file list: `apps/cms/locked_split.py`, `apps/orientation/templatetags/orientation_tags.py`, `templates/orientation/result.html`, `apps/designpreview/views.py`, and the app tests of enquiries, pages, community and orientation. All are recorded in NOTES §4 for the steward's manifest.
- m2 — `KEEP_SOURCE` is not empty (3 rows) and `ARABIC_BURNDOWN` holds about 70 rows. All of them are other lanes' templates and are carried as contracts. Under the merge order these lanes go before AR, so a steward must re-measure the burn-down at merge (the equality test fails on a stale row).
- m3 — In `apps/orientation/tests/test_wizard.py` the Arabic assertion is a prefix (`split(":")[0]`), and the earlier `lang="fr"` check was dropped. The full rendering would be the stronger check.
- m4 — Docstrings and comments in several files were broken mid-sentence by a formatter (e.g. `apps/companies/models.py` TAXONOMY_LABELS comment, `test_virtual_forum_gate.py`, `test_services.py`, `documents/services.py`, `locked_renderings.counts`). This is cosmetic; re-wrap them.
- m5 — The completeness crawler does not read `<option>` text or `<select>` contents (the root of B2's escape).
- m6 — The questionnaire walk in my it/en probe reached no result, because of the probe's button choice. The Arabic walk reached one; the it/en result pages are covered by the in-process test (post-acceptance: none).
- Post-acceptance candidate (not fixed, R14): the Academy's course titles and descriptions are French in it/en/ar (D-demo, ARABIC_AUDIT R2).

## Stills and measures

`C:/tmp/ile_v5_council/evidence/v524/ar/qa/` contains:
- `<page>_<1440|390>_ar.png` plus `_390_ar_full.png` (57 files);
- `<page>_<1440|390>_<it|en>.png` (72 files);
- `measures_ar.json` and `measures_it_en.json`.

The pytest log is `~/AppData/Local/Temp/claude/<session>/scratchpad/ar_qa_pytest.log`.

## Housekeeping

- The lane server 8791 (ile_v5_l7, `seed_all` re-run) is stopped. The temporary `.env` copy (gitignored) is removed and the worktree is clean.
- CHROMIUM_LOCK_A is released. No pytest is running on `test_ile_v524_ar`.
- Nothing was pushed, tagged or merged.

## After the one fix round (`v524-ar-fix`) — the verdict as the workflow returned it, verbatim

```json
{"review": [{"page":"/ar/ gate surfaces (19 surfaces x 1440/390, headed)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"Not re-scored: the lane changes no composition and no CSS; 4 where not applicable."}],
 "minors": [{"severity":"minor","where":"templates/dev/designpreview/_locked_keys.html + tests/i18n/test_locked_renderings_v524.py","detail":"FIXED in the one fix round: the dev index returned 500 (TemplateSyntaxError on locked_counts.C-UI).","fix":"template_counts() keys"},{"severity":"minor","where":"apps/companies/models.py Sector.__str__ / Territory.__str__","detail":"FIXED in the one fix round: French sector/territory options on /ar/ need form.","fix":"taxonomy_label(self)"},{"severity":"minor","where":"files outside §3.8's list","detail":"apps/cms/locked_split.py, apps/orientation/templatetags/orientation_tags.py, templates/orientation/result.html, apps/designpreview/views.py and app tests changed; recorded in NOTES §4.","fix":"The steward adds them to the v524-ar family's slices."},{"severity":"minor","where":"scripts/i18n_audit.py KEEP_SOURCE; tests/i18n/arabic_allowlist.py ARABIC_BURNDOWN","detail":"KEEP_SOURCE 3 rows and ARABIC_BURNDOWN ~70 rows, all other lanes' templates (HOME, PUB1, PUB2, CLOSING); remaining French on /ar/ is lang-marked.","fix":"The steward re-measures at merge; CLOSING asserts it empty."},{"severity":"minor","where":"apps/orientation/tests/test_wizard.py","detail":"Fixed in the fix round: the Arabic result asserts the full C-UI rendering.","fix":"done"},{"severity":"minor","where":"several comments/docstrings","detail":"Fixed in the fix round: formatter-broken comments re-wrapped.","fix":"done"}],
 "new_strings": [],
 "not_done": []}
```
