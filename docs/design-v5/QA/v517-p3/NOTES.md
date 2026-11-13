# Lane P3 (v517-p3-build) — V5.17 privacy governance correction

- 28 October 2026. Worktree `C:/tmp/ile_wt/v517-p3`, branch `v517-p3` from `design-v5` `e580b41`.
- Directive V5.17 (`C:/tmp/ile_v5_council/directives/V5_17_PRIVACY_GOVERNANCE_CORRECTION.md`), with V5.14 and V5.16.
- A small, low-load lane beside Wave 3. No visual lane's file was edited: no `base.html`, header, footer, `gates.py`,
  portal template or static CSS/JS. One recorded slice in a platform template (below).

## 1. Status model (V5.17 §2)

PRODUCT_COMPLETE / **COMPLIANCE_REVIEW_COMPLETE** / PRODUCTION_CONFIG_COMPLETE / PRODUCTION_READY, with the owner's
definitions verbatim. V5.16's PRIVACY_CONTENT_COMPLETE is replaced everywhere it was a state:

- runbook *States* (the quotation, the rows, the paragraph «do **not** block PRODUCT_COMPLETE», the §10 sentence: the
  infrastructure values are not questions for the owner now; they are verified when the server is prepared);
- checklist §A (intro: «None of A-29 … A-33 blocks PRODUCT_COMPLETE»; the «State it completes» column; A-30 «verified
  when the production server is prepared, not asked beforehand»; A-31 names R-SC-1; A-32 points at `DPIA.md`);
- release notes §5, `apps/legal/models.py` (comment), `docs/compliance/PRIVACY_PROCESSING_AUDIT.md` §6;
- `tests/deployment/test_privacy_states_v516.py` reads the V5.17 model, and a new test fails if a living document
  keeps PRIVACY_CONTENT_COMPLETE other than as «the name it replaced».

The historical records (DECISION_LOG_V54, OWNERSHIP_V54.json's v516-p2 title, lane P2's notes) are left as written.

## 2. DPIA (V5.17 §3)

- `docs/compliance/DPIA.md` — IN PREPARATION: context, art. 35(7)(a) description (nature, scope, context, purposes,
  recipients, retention), (b) necessity and proportionality per principle, sources of risk, (c) eight risks with a
  preliminary technical rating, (d) fourteen measures with their evidence, residual risk, consultation, the open facts
  D-1 … D-10 (only what is genuinely unknown, each with its class), sign-off.
- `DPIA_NECESSITY.md` §4: «DPIA to be prepared (in progress: DPIA.md) unless legal review documents a reasoned
  conclusion that it is not required. DPIA = PRODUCTION GATE».

## 3. R-SC-1 (V5.17 §4–§5)

- Setting `ILE_SPECIAL_CATEGORY_FLOWS_ENABLED`: base False; prod.py False and **refuses True without
  `ILE_SPECIAL_CATEGORY_BASIS_REFERENCE`**; dev.py = DEBUG (the preview); test.py True (the local product; the DENY
  tests switch it off). Declared in `.env.example` and `docs/deployment/production.env.example` (`=0`).
- Guard `apps/core/special_category.py`: `flows_enabled`, `solicits_special_category(requirement)` (terms that name a
  special-category DOCUMENT, accent- and case-insensitive; «Assurance médicale de voyage» stays open), `piece_closed`,
  `loose_upload_kinds`, the sentences G-FREE, G-UPLOAD and the closed-piece notice in it/fr/en/ar.
- Used by: `documents.presenters.present_requirement` (`may_file` false, `special_category_closed`),
  `documents.views.requirement_detail` (the calm sentence as an info message), `documents.services.file_version`
  (`RequirementRefused`, code `special_category`: the form post, the Dépôt's JSON and any other road),
  `documents.forms.DocumentUploadForm` (named kinds, no pre-selection, G-UPLOAD), `helpdesk.forms.MessageForm`
  (G-FREE), `cases.views.detail` (`free_text_guidance` → the reason field).
- Nothing deleted; no consent box. Tests `apps/documents/tests/test_special_category_v517.py` (34): classification,
  DENY by page, register, form post, Dépôt JSON and service; ALLOW in the preview; the guidance in four languages;
  prod.py in a subprocess (off; refuses on without the reference; on with it). Mutation check: with the guard
  neutralised, the three DENY tests fail.
- `docs/compliance/PREVIEW_VS_PRODUCTION.md` (feature | preview | production | gate);
  `SPECIAL_CATEGORY_AUDIT.md` §3.1 «R-SC-1 as built».
- G-UPLOAD stands beside the **loose upload** only. The requirement's Dépôt (`templates/documents/partials/depot.html`,
  a visual lane's file) keeps its own depot note; it does not show G-UPLOAD (audit §3.1 table: «the depot note
  stays»). R-P3-2 below is the request.
- Review fixes (steward, v517-p3-merge): the bare stem «biometri» replaced by «données biométriques», «dati
  biometrici», «biometric data» («Passeport biométrique» and «Photo d'identité biométrique» stay open); the guard
  reads code and title, never the detail (tests for both); the closed sentence is said once after a refused post;
  the production privacy test's docstring says «the production switches», not prod.py.

### Recorded slice in another family's file

- `templates/cases/partials/state_dialog.html` (w3-e's): `{% if free_text_guidance %} {{ free_text_guidance }}{% endif %}`
  appended inside the reason field's help paragraph. One line, no markup change.

### For the catalogue pass (lane D) — msgids to add, then switch the guard to `gettext_lazy`

The texts are served from `core.special_category` dictionaries meanwhile, so `tests/i18n` stays whole.

1. G-FREE — msgid «N’indiquez pas de données sur la santé, l’origine ethnique, les convictions religieuses ou
   philosophiques, les opinions politiques, l’appartenance syndicale, la vie sexuelle ou l’orientation sexuelle : elles
   ne sont pas nécessaires ici.» (it/en/ar: `G_FREE`)
2. G-UPLOAD — msgid «Ne déposez que les pièces nécessaires à votre démarche : aucun document médical ni aucun document
   qui révèle la santé, l’origine ethnique, les convictions, les opinions, l’appartenance syndicale, la vie sexuelle ou
   l’orientation sexuelle.» (`G_UPLOAD`)
3. Closed piece — msgid «Cette pièce ne se dépose pas sur la plateforme : elle relève des catégories particulières de
   données, que la plateforme ne reçoit pas. Pour savoir comment la transmettre, écrivez au Guichet numérique.»
   (`CLOSED_PIECE`; «Guichet numérique» in the catalogue's renderings: Sportello digitale, Digital helpdesk, الشباك الرقمي)

### Requests

- R-P3-1 (lane D / w3-e, the case file): if the reason field moves, keep `free_text_guidance` under it.
- R-P3-2 (documents owner): the depot note of the loose upload (R-SC-2) may become G-UPLOAD once it is a catalogue
  message; today G-UPLOAD stands as the kind's help text.
- R-P3-3 (legal review): the criminal-record extract (`documents/seeds.py` `criminal_record`) is art. 10 data, not
  art. 9; R-SC-1 does not close it. Whether art. 10 needs its own gate is for the legal review — not decided here.
- R-P3-5 (documents owner, product decision): in production a closed special-category piece still counts as missing
  on the case checklist and offers no action; the piece's page says why, but the row may read as blocking. A neutral
  «outside the platform» state is the documents owner's call — not changed here.
- R-P3-6 (documents owner, follow-up): with the switch off, warn or refuse at `documents.services.declare_requirement`
  for a piece that solicits art. 9 data; the residual risk of a neutral title is recorded in the audit §3.1 and DPIA
  RK-2.
- R-P3-4 (steward): ownership of the new files — `apps/core/special_category.py`,
  `apps/documents/tests/test_special_category_v517.py`, `apps/legal/tests/test_production_privacy_page_v517.py`,
  `docs/compliance/{DPIA,PREVIEW_VS_PRODUCTION,OF11_ANNEXE_DEVIATIONS}.md`, these notes — and slices in
  `apps/documents/{forms,presenters,services,views}.py`, `apps/helpdesk/forms.py`, `apps/cases/views.py`,
  `templates/cases/partials/state_dialog.html`, `config/settings/{base,dev,prod,test}.py`, `.env.example`,
  `docs/deployment/{production.env.example,PRODUCTION_CHECKLIST.md,PRODUCTION_DEPLOYMENT_RUNBOOK.md}`,
  `docs/RELEASE_NOTES_v2.0.0.md`, `docs/compliance/{DPIA_NECESSITY,SPECIAL_CATEGORY_AUDIT,PRIVACY_PROCESSING_AUDIT}.md`,
  `apps/legal/models.py`, `tests/deployment/test_privacy_states_v516.py`.

## 4. OF-11 (V5.17 §7)

Not closed. `docs/compliance/OF11_ANNEXE_DEVIATIONS.md` lists both deviations (ANNEXE 1 SAYS → VERIFIED PRODUCT
REALITY → PROPOSED NOTICE) with an empty acceptance row; `PRIVACY_PROCESSING_AUDIT.md` no longer says that publishing
is the acceptance.

## 5. Production privacy page (V5.17 §9)

`apps/legal/tests/test_production_privacy_page_v517.py` (9): under the production switches, in it/fr/en/ar, on the
whole page — a published row with open fields renders the pending notice and none of: the marker, an OF id, a class
name («legal review required» …), the highlight (`mark`, `data-open-field`), the preview's list of fields, the
pending-translation note; the same text with every marker filled renders its body and still none of them.

## 6. Not done

- No browser run (not indispensable: the changes are server-side; the info message uses the existing notice).
- Tests run (lane l9): apps/documents, apps/helpdesk, apps/cases, apps/legal, tests/i18n — 799 passed, 3 skipped;
  tests/deployment, tests/compliance, tests/security, tests/test_env_example_is_complete.py, apps/portal — 593 passed,
  1 failed: `apps/portal/tests/test_views.py::test_dashboard_for_a_fresh_account_shows_empty_states_not_numbers`, which
  fails identically on `design-v5` `e580b41` (stale since the empty-wall collapse; DECISIONS §16 assigns it to lane D).
- Catalogue messages (lane D), ownership entries (steward).
