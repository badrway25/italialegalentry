# V5.16 privacy lane P2 — build notes (label v516-p2-build)

- Branch `v516-p2`, from `design-v5` at `4d9ada5` (lane P merged: tag `v514/privacy`, DL54-165).
- Directive: V5.16 «Privacy open fields: classify, do not block visual delivery» (28 Oct 2026, 18:21), with V5.14.
- Rules held: no legal fact invented (controller, bases, art. 9 conditions, DPO, DPIA conclusion, roles, retention,
  region, DPA, transfers are classified, never filled); locked copy never reworded; no secret, no real personal data,
  no server identity; production never touched; LF everywhere (bytes in, bytes out).

## What was delivered

1. **`docs/compliance/PROCESSING_PURPOSE_MATRIX.md`** — 21 purposes (M-01 … M-21). Each row gives PURPOSE, DATA,
   NECESSITY, ART. 6, ART. 9, RETENTION (CONFIGURED with `file:line` / APPROVED POLICY / PROPOSED / UNRESOLVED) and
   RECIPIENTS. A basis is given only where ANX states it; everywhere else the cell says LEGAL REVIEW REQUIRED.
   - Assessed separately: security logs, fraud/abuse prevention, the audit trail, legal compliance, the helpdesk
     (request vs internal notes), the Academy and the selection.
   - None of them gets 6(1)(b) by default.
2. **`docs/compliance/SPECIAL_CATEGORY_AUDIT.md`** — 15 upload and free-text flows (S-01 … S-15).
   - **«Yes» flows**: documents (loose and per requirement), helpdesk, portal messages, case texts, Academy notes,
     selection notes, staff notes, public-form texts and Virtual Forum posts. All of them are marked SPECIAL CATEGORY
     LEGAL BASIS REQUIRED, because no art. 9 condition exists in approved material.
   - **Closed today**: the public forms are closed by G2; the Virtual Forum by its flag and G1.
   - **Not closed**: the reserved-area flows. No gate closes them, because an account staff create reaches them.
     Hence request R-SC-1 for a gate, and checklist A-31 until the gate exists.
   - **Guidance**: G-FREE and G-UPLOAD, written in it/fr/en/ar.
   - **Technical minimisation**: T-1 … T-7.
3. **`docs/compliance/DPO_ASSESSMENT.md`** — the art. 37(1)(a)/(b)/(c) and (4) triggers, applied to the processing.
   - Conclusion: **DPO STATUS = TO BE CONFIRMED**.
   - The four facts that decide it: scale, core activity, whether art. 9 flows open, and duration.
   - No DPO is invented. AGAMI APS is not a public body.
4. **`docs/compliance/DPIA_NECESSITY.md`** — art. 35, the Garante's list (provv. 467/2018) and the nine WP248
   criteria, applied to identity documents, case files, possible art. 9 data, pre-assessments and multiple actors.
   - Four criteria are likely met: evaluation, highly personal data, matching, vulnerable subjects.
   - Conclusion: **DPIA LIKELY REQUIRED → DPIA = PRODUCTION GATE** (checklist A-32). It is stated as an assessment,
     with the facts that could reverse it.
5. **`docs/compliance/RECIPIENT_ROLES_MATRIX.md`** — R-01 … R-15. Each row gives A (candidate processor), B
   (candidate independent controller), C (possible joint controller) or I (internal, authorised persons), with the
   workflow's reason. Every row is «to be confirmed by legal review», and the art. 28 need is stated for every A.
6. **Forms' legal-basis UX** — `docs/compliance/FORMS_LEGAL_BASIS_UX.md` (inventory F-01 … F-13) and code (below).
   Tests are in `tests/compliance/test_forms_legal_basis_v516.py`:
   - no pre-ticked box;
   - every required box in the team's wording is an acknowledgement, and neither its label nor its error says
     «consent»;
   - the only consent sentences are the three prescribed ones, each classified;
   - optional choices are separate;
   - no bundled consent;
   - the old reused text is versioned.
7. **Open-field markers reclassified** (apps/legal):
   - **Classes.** Every marker in A, in all four languages, is now `[DA COMPLETARE — OF-nn — <CLASS>: …]`:
     - PRODUCTION CONFIGURATION REQUIRED: OF-02, OF-03, OF-04, OF-05;
     - OWNER CONFIRMATION REQUIRED: OF-01, with AGAMI APS as the candidate (Italy Legal Entry is not
       substituted as controller unless the owner confirms it is a separate legal entity);
     - LEGAL REVIEW REQUIRED: OF-06, OF-07, OF-08 (DPO STATUS = TO BE CONFIRMED), OF-10, OF-12 (processor /
       independent / joint), and the new **OF-13** (SPECIAL CATEGORY LEGAL BASIS REQUIRED, §3.5).
   - **DigitalOcean** is named once in §5 as «fornitore previsto» (intended provider). Its DPA, sub-processors,
     region and transfers stay in OF-02 markers.
   - **Code.**
     - `legal.models.OPEN_FIELD_CLASSES`, `open_field_class()` and `LegalDocument.open_field_classes()`;
     - the rendering marks `data-open-field-class`;
     - the preview notice lists the fields by class;
     - the back office lists them by class;
     - the publication refusal names the classes.
   - **The production guard is unchanged**: it refuses a marker of any class (tested per class).
   - **Tests**: `apps/legal/tests/test_open_field_classes_v516.py`.
8. **Status model** (V5.16 §14):
   - **Runbook *States***: PRODUCT_COMPLETE, PRIVACY_CONTENT_COMPLETE and PRODUCTION_CONFIG_COMPLETE rows are added.
     PRODUCTION_READY now needs all three plus the gate «PRIVACY NOTICE = VERIFIED AND PUBLIC». The V5.9/V5.10 rows
     and the one bar are kept.
   - **Checklist §A**: A-29 … A-33 are added, closed and never accepted as open:
     - A-29: privacy notice verified and public;
     - A-30: the production configuration, including the nginx/Gunicorn/application logging verification of §12;
     - A-31: art. 9;
     - A-32: DPIA;
     - A-33: governance facts, the controller, bases, DPO, roles and art. 28 included.
   - **Release notes §5**: a paragraph says what «production-ready» now means. Nothing in the notes conflicted.
   - **Tests**: `tests/deployment/test_privacy_states_v516.py`. The W4-D tests (`test_release_tags_w4_d.py`,
     `test_runbook_matches_the_code.py`) pass unchanged.

## Code changes outside apps/legal (slices; minimal)

- `apps/core/forms.py`:
  - `AcknowledgementBooleanField` (required, never pre-ticked, Django's own required message, CSS hook
    `consent-checkbox` kept);
  - `SPECIAL_CATEGORY_GUIDANCE` (reuses the translated enquiries message) and `with_guidance()`.
- `apps/consents/services.py`:
  - `REUSED_CONSENT_KEYS` emptied;
  - `ACKNOWLEDGEMENT_TEXT` / `ACKNOWLEDGEMENT_PURPOSES` added;
  - `ensure_consent_text` versions the old reuse (v1 → v2, records keep v1);
  - `LOCKED_COPY_LEGAL_REVIEW_REQUIRED` marks the company-needs and Forum-registration sentences.
- `apps/enquiries/forms.py`: the label and the field type follow the purpose.
- `apps/accounts/forms.py` (`SignupForm.accept_terms` only) and `apps/community/forms.py` (`JoinForm.consent`, the
  body help texts): the acknowledgement field and the guidance.
- `apps/helpdesk/forms.py`: `MessageForm.body` help text (guidance).
- `apps/enquiries/tests/test_views.py`: one assertion, the institution proposal records the acknowledgement.
- `templates/legal/document.html`: the preview notice only (the list by class).

**Not touched**: footer, base, header, `gates.py`, static CSS/JS, portal templates and `locale/` (lane D's).

## No new catalogue message

`tests/i18n/test_catalogues.py` requires every source message to be translated and forbids unreviewed
locked fragments. This lane therefore adds no msgid:
- the acknowledgement is French-only, with `lang="fr"`, like the prescribed sentences;
- the guidance reuses an existing translated message.

The fuller wording (G-FREE, G-UPLOAD, the acknowledgement) is requested from lane D.

## LOCKED COPY — LEGAL REVIEW REQUIRED (for the owner and the legal lead)

- `p1.companies.form.consent` (company needs) and `p2.forum.registration.consent` (Forum registration) ask for a
  «consent» for processing that ANX §3 founds on 6(1)(b).
  - They are kept verbatim in the code and marked.
  - Proposals P-1/P-2 (acknowledgement «J’ai lu l’information sur le traitement des données personnelles (Privacy
    Policy).», with a separate optional consent only if a real optional purpose exists) are in
    `FORMS_LEGAL_BASIS_UX.md` §3.
  - Both forms depend on Allegato 1 and stay closed (G2).
- The newsletter's prescribed consent is a real optional consent (B) and is compliant.

## Requests to other lanes

- **R-SC-1, lane C (`apps/core/gates.py`) with the documents / helpdesk / portal / cases / academy / selection
  owners**:
  - a gate, flag `special_category_basis` default False, whose note cites the legal approval;
  - while it is closed, it closes the uploads and the person-facing free texts in production (or the reserved
    area to data subjects).
  - Until then, checklist A-31 says that no account is created for a real data subject.
- **R-SC-2, lane A (`templates/documents/partials/depot.html`)**: the loose upload's note → G-UPLOAD once D has it.
- **R-SC-4, portal / cases / enquiries owners**: G-FREE as model help text on the staff free texts (portal
  messages, case reasons, `admin_notes`).
- **R-SC-5, lane D (`locale/`)**: add G-FREE, G-UPLOAD (it/en/ar in SPECIAL_CATEGORY_AUDIT §4), and, after the
  legal lead's P-1/P-2 decision, the acknowledgement with an overlap decision. Then one-line follow-ups:
  - the `kind` help text of the loose upload;
  - `SPECIAL_CATEGORY_GUIDANCE` → G-FREE.
- **Documents owner**: the technical minimisation T-1 … T-4 (SPECIAL_CATEGORY_AUDIT §5):
  - T-1: no default kind;
  - T-2: no loose upload in production;
  - T-3: requirements name their piece;
  - T-4: `retention_until` set by policy.
- **Notifications owner**: T-5, drop the outbox body after delivery (TG-3).
- **Owner of `templates/pages/contact.html`**: a stale comment («prescribed wording») for the contact box.
- **Steward**: assign this lane's files in `docs/design-v5/OWNERSHIP_V54.json`, family `v516-p2`:
  - **whole files**:
    - `docs/compliance/{PROCESSING_PURPOSE_MATRIX,SPECIAL_CATEGORY_AUDIT,DPO_ASSESSMENT,DPIA_NECESSITY,RECIPIENT_ROLES_MATRIX,FORMS_LEGAL_BASIS_UX}.md`;
    - `apps/legal/tests/test_open_field_classes_v516.py`;
    - `tests/compliance/test_forms_legal_basis_v516.py`;
    - `tests/deployment/test_privacy_states_v516.py`;
    - this file;
  - **slices**: the files listed under «Code changes»; the checklist header note + A-29 … A-33 + the bar's V5.16
    sentence; the runbook header note + *States*' intro and its three new rows plus PRODUCTION_READY's V5.16
    phrases; the release notes' «Privacy and the states» paragraph.
  - `check_ownership.py v514-p … --working-tree` lists them as outside v514-p today (expected).

## Owner input (classified; nothing filled by the team)

- **OWNER CONFIRMATION REQUIRED**: OF-01, the controller (AGAMI APS as the candidate); OF-11.
- **PRODUCTION CONFIGURATION REQUIRED (A-30)**: OF-02, DigitalOcean region, DB/storage region, DPA, sub-processors,
  transfers; OF-03, SMTP provider and mailbox host; OF-04, off-server backups and their retention; OF-05, journald
  and nginx rotation; plus the §12 logging verification.
- **LEGAL REVIEW REQUIRED (A-31 … A-33)**: OF-06/07, retention policies; OF-08, DPO status; OF-10, bases; OF-12,
  roles; OF-13, art. 9; OF-09, the locked sentences P-1/P-2; the DPIA (A-32); the LIAs for 6(1)(f) (matrix M-01 …
  M-03).

## Verification (lane l9: `DATABASE_URL …/ile_v5_l9`, `TEST_DATABASE_URL …/test_ile_v5_l9`)

- `apps/legal` passes 41 of 41, including the 17 new class tests and the updated v514 tests (11 open-field ids, OF-13,
  the `data-open-field-class` mark, DigitalOcean only as the intended provider).
- These pass 569 of 569: `apps/legal`, `tests/compliance` (with the 6 new forms tests), `tests/i18n/test_catalogues.py`,
  `test_page_integrity.py`, `tests/frontend/test_documents_w3_c.py`, `apps/documents`, `apps/helpdesk`,
  `apps/consents`, `tests/security/test_log_privacy.py`, `tests/test_check_ownership.py` and
  `tests/deployment/test_privacy_states_v516.py`.
- These pass 302, with 1 skipped (the confidential-sentinel test, which needs its private environment):
  `apps/enquiries`, `apps/community`, `tests/i18n/test_documentation.py` and `tests/security`.
- The deployment documents' tests pass 64 of 64: `test_release_tags_w4_d.py`, `test_runbook_matches_the_code.py`,
  `test_production_checks.py`, `test_rule_counts_in_documents_w4_d.py` and the new states test.
- A first run of `apps/accounts`, `apps/forum` and `apps/news` (with enquiries, community and consents) passed 611.
  The one failure was the institution assertion, since updated.
- ruff check + format: clean on every touched Python file.
- No browser run. The changes are a help line under two existing form fields (helpdesk message, Virtual Forum) and
  the preview-only notice of the legal page; HTTP tests render the preview in four languages. The help line uses the
  shared form-field component and needs no new CSS. A visual check belongs to the next lane that measures those
  pages.

## Review fix (v516-p2-fix, 28 Oct 2026)

One major and four minors from the lane's review.

- **Major: the entity's legal status was stated as a fact.** `DPO_ASSESSMENT.md`, the OF-01 row of
  `PRIVACY_PROCESSING_AUDIT.md`, checklist A-33 and the docstring and test name of
  `apps/legal/tests/test_open_field_classes_v516.py` said, in one form or another, that Italy Legal Entry «is not a
  legal entity» or is «never» the controller. No approved material says this. V5.16 §2 is conditional.
  - Each place now says: Italy Legal Entry is not substituted as controller unless the owner confirms it is a separate
    legal entity (OF-01).
  - `tests/deployment/test_privacy_states_v516.py` pins the new A-33 wording.
- **Minor: consent_text_for could return the old reused consent row.** On a database that still has the v1 row reusing
  `p1.companies.form.consent` (dev or preview, or between `migrate` and `seed_all`), `record_consent` recorded the old
  consent sentence while the form showed the acknowledgement.
  - `consent_text_for` now sends an acknowledgement purpose whose current row carries `RETIRED_REUSE_KEY` to
    `ensure_consent_text`, which creates v2.
  - New test: `test_a_submission_on_a_database_that_still_holds_the_reused_consent_records_the_acknowledgement` goes
    through `record_consent` with the v1 row present.
  - **Release handoff**: the first `seed_all`, or the first submission, on a database seeded before V5.16 creates v2
    of the `fr` text of the institution, university, contact and orientation purposes. The v1 rows stay, and so do the
    records that point at them.
- **Minor: SPECIAL_CATEGORY_AUDIT §1 overstated the enforcement.** S-01 … S-03 now read «MUST stay closed — not
  enforced in code until R-SC-1; manual gate A-31». Today nothing closes those flows in code. The director or steward
  tracks **R-SC-1 as a PRODUCTION_READY blocker**.
- **Minor: the back office's withdrawal action** (`ConsentRecordAdmin.withdraw_selected`, «Registra la revoca del
  consenso») also applies to acknowledgement records. To staff, an acknowledgement then looks like a consent that can
  be revoked.
  - `apps/consents/admin.py` belongs to the sec-f8 slice assigned by the steward (OWNERSHIP_V54), so it is not edited
    here.
  - `apps/consents/services.py` now exports `CONSENT_PURPOSES = (ConsentPurpose.NEWSLETTER,)`: the category-B
    purposes recorded as `ConsentRecord`. The selection's identity disclosure is not a `ConsentPurpose` today.
  - **Request R-ADM-1, to the owner of `apps/consents/admin.py` (sec-f8 slice, via the steward)**: in
    `withdraw_selected`, act only on `queryset.filter(purpose__in=CONSENT_PURPOSES, withdrawn_at__isnull=True)`.
    Report the records left out with `self.message_user(..., level=messages.WARNING)` («una presa visione
    dell'informativa non è un consenso revocabile»). The withdrawal action stays tied to «change» and stays audited.
- **Minor: DPIA_NECESSITY §4** said «three» WP248 criteria but lists four (1, 4, 6, 7). It now says «four».

Verification (lane l9): `tests/compliance/test_forms_legal_basis_v516.py`, `tests/deployment/` (including
`test_privacy_states_v516.py`), `apps/legal/tests/test_open_field_classes_v516.py` and
`apps/enquiries/tests/test_views.py` give 155 passed. `apps/community/tests/test_join.py`, `apps/legal` and
`apps/accounts/tests` give 254 passed. The test files touched are clean under ruff check and ruff format.
