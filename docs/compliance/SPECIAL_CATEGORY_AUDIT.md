# Special-category (art. 9 GDPR) audit of uploads and free-text fields (V5.16 §5–§6)

- Written 28 October 2026 by lane P2 (label `v516-p2-build`). Read from the code on branch `v516-p2`.
- Directive V5.16 §5: «If yes: Article 6 alone is NOT sufficient … If no valid Article 9 condition has yet been
  approved: do not open that production processing flow. Mark: SPECIAL CATEGORY LEGAL BASIS REQUIRED. Do not simply
  add an "explicit consent" checkbox as a universal solution without legal review.» §6: «tell users not to provide
  it and technically minimise collection where practical. Do not collect broad documents "just in case".»
- **Approved material holds no art. 9 condition.** ANX §2 only says: «L'utilisateur est invité à ne pas insérer dans
  les champs libres des catégories particulières de données au sens de l'art. 9 du RGPD, non requises pour les
  finalités du service.» The Master Dossier and IMPL name none either (lane P audit, §1 and OF-10). So every «yes»
  below is **SPECIAL CATEGORY LEGAL BASIS REQUIRED**. No explicit-consent box was added.
- **Art. 9 categories**: racial or ethnic origin, political opinions, religious or philosophical beliefs, trade-union
  membership, genetic data, biometric data processed to uniquely identify a person, health, sex life or sexual
  orientation. A passport photograph is not biometric data unless it is processed through specific technical means
  that identify a person (recital 51). Nothing in the code does that: no face matching, no OCR, no antivirus
  (`DOCUMENT_SCANNER` empty).
- **Who the data subjects are**: mostly third-country nationals preparing a regular entry to Italy (work, study,
  family reunification, research, other routes; `apps/orientation/seeds.py`). In that context, people realistically
  describe illness, pregnancy, disability, religion, persecution or sexual orientation when they explain their
  situation. Some documents of the pathways carry such data as a side effect: marriage certificates, payslips with
  union dues, medical certificates.

## 1. The inventory

«Live in production?» describes what the code allows once deployed. Public sign-up is closed by G2
(`apps/accounts/adapters.py:10-11`, `apps/core/gates.py` `public_forms_enabled`). But an account that staff create
in the back office reaches the reserved area, so **no gate closes the reserved-area flows today**. See §3.

| # | Field / flow | Who writes it | Realistic art. 9 content? | Why | Closed in production by | Status |
|---|---|---|---|---|---|---|
| S-01 | **Loose document upload** (`DocumentUploadForm`, `apps/documents/forms.py`; kinds `identity`, `diploma`, `contract`, `other`, default `other`, `apps/documents/models.py:23-27`) | the person, an organisation member | **yes** | «other» admits any file: medical certificates, religious marriage certificates, payslips showing union dues. Identity documents are not art. 9 by themselves (no biometric processing) | **nothing** (staff-created accounts) | **SPECIAL CATEGORY LEGAL BASIS REQUIRED — MUST stay closed — not enforced in code until R-SC-1; manual gate A-31** |
| S-02 | **Upload against a named requirement** (`RequirementUploadForm`) | the person | **yes, depending on the requirement** | the requirement names the piece. A family-reunification marriage certificate can reveal sex life or orientation (same-sex spouse) or religion (religious celebration) | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED — MUST stay closed — not enforced in code until R-SC-1; manual gate A-31**; requirement review R-SC-3 |
| S-03 | **Helpdesk question and messages** (`OpenRequestForm.question`, `MessageForm.body`, `apps/helpdesk/forms.py`; `TicketMessage.body`) | the person; operators; professionals | **yes** | a person explains a situation in their own words. The form already says «N'indiquez pas de données de santé, de religion ou d'opinion» | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED — MUST stay closed — not enforced in code until R-SC-1; manual gate A-31** |
| S-04 | **Portal messages and deadline descriptions** (`apps/portal/models.py:82`, `:187`) | staff, assignees | **yes** | written about the person's file; the help text asks for minimisation (`DATA_MINIMISATION_HELP`, `apps/portal/models.py:34`) | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED** (R-SC-1) |
| S-05 | **Case-file free texts**: suspension reason, checklist detail, assessment rationale (`apps/cases/models.py:276`, `:394`, `:552`); `reason` in `cases/views.py:218` | assignees, staff | **yes** | a suspension «for health reasons», a pregnancy, a detention | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED** (R-SC-1) |
| S-06 | **Academy notes and attendance** (`apps/academy/models.py:425`, `:674`) | the training provider, assignees | possible | an absence explained by illness | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED** (R-SC-1) |
| S-07 | **Selection notes and evidence detail** (300 characters, `apps/selection/views.py:119-217`; `SelectionEvidence.detail`/`note`) | the authorised actor, operators | possible | fitness for a job, a union | nothing | **SPECIAL CATEGORY LEGAL BASIS REQUIRED** (R-SC-1). The module already refuses health, religion and union **fields** (`apps/selection/models.py:31-35`) |
| S-08 | **Company need texts**: duties, motivation, training needs (`apps/companies/models.py:499-545`) | the company | not about a natural person by design | they describe a role, not a person. The help text asks for no third-party or sensitive data (`apps/companies/forms.py:28`) | — | **no**: guidance kept |
| S-09 | **Public forms' free texts**: notes, proposal, message (`apps/enquiries/models.py:193-276`) | the visitor | **yes** (contact message) | free text from anyone | **G2** (`apps/core/gates.py` `public_forms_enabled`, closed while the Allegato 1 pages are unpublished) | **SPECIAL CATEGORY LEGAL BASIS REQUIRED — closed by G2**; guidance present (`SENSITIVE_DATA_HELP`, `apps/enquiries/forms.py:23`) |
| S-10 | **Virtual Forum posts, replies, reports, attachments** (`apps/community`) | members | **yes** | a public-to-members discussion | flag `virtual_forum` **and** G1 (`apps/core/gates.py` `virtual_forum_enabled`) | **SPECIAL CATEGORY LEGAL BASIS REQUIRED — closed by its flag and G1**; guidance applied (§4) |
| S-11 | **Orientation answers** (`AnswerForm`, choice keys only) | the visitor | **no** | every option is a situational choice: objective, work profile, study type, family member status, training interest (`apps/orientation/seeds.py`). No free text | — | **no** |
| S-12 | **Profile and account** (name, e-mail, phone, country, language, account type) | the person | **no** | no art. 9 field | — | **no** |
| S-13 | **Account verification notes** (`AccountVerification.evidence_note`, `decision_note`, `apps/accounts/models.py:133-138`) | the applicant, staff | unlikely | about an organisation's credentials | — | **no**: minimisation note R-SC-4 |
| S-14 | **Forum registration** (`sector_of_interest`, free text) | the registrant | unlikely | a sector name | G2 + `forum_public` | **no** |
| S-15 | **Staff notes on submissions** (`admin_notes`, `apps/enquiries/models.py:74`, `apps/forum/models.py:294`) | staff | possible | free text about a submitter | back office only | **SPECIAL CATEGORY LEGAL BASIS REQUIRED** for the content; guidance request R-SC-4 |

## 2. Data minimisation — what the platform already does

- A document is downloaded only through a 10-minute signed link, and is stored outside every served directory
  (lane P audit P11).
- The selection domain refuses age, nationality, gender, health, religion and union fields (`apps/selection/models.py:31-35`).
- A person's identity reaches a company only through a disclosure with a purpose, a duration of at most 180 days and
  every access recorded (`apps/selection/models.py:711`, `:729`).
- The helpdesk question, the public forms, the company needs and the portal already carry a «no sensitive data» help
  text (`apps/helpdesk/forms.py`, `apps/enquiries/forms.py:23`, `apps/companies/forms.py:28`, `apps/portal/models.py:34`).

## 3. The production gate

No art. 9 condition is approved. So the flows S-01 to S-07 and S-15 must not be opened to real data subjects in
production. Today nothing in the code closes them: a staff-created account reaches them.

**R-SC-1 — request to lane C (`apps/core/gates.py`), with the owners of `documents`, `helpdesk`, `portal`, `cases`,
`academy` and `selection`:**
- add a gate (for example `special_category_basis_approved()`, backed by a feature flag `special_category_basis`,
  default **False**, whose `note` must cite the legal review's written approval, as `forms_override_without_legal`
  does);
- while it is False, refuse the uploads S-01/S-02 and the free-text posts S-03 to S-07 with the platform's closed
  state (`data-gate`), or keep the reserved area closed to data subjects altogether.

Until that gate exists, the production checklist carries the condition as a release item: **A-31 SPECIAL CATEGORY
LEGAL BASIS** (`docs/deployment/PRODUCTION_CHECKLIST.md`). The owner does not create accounts for real data subjects
in production before A-31 is closed.

### 3.1 R-SC-1 as built (V5.17 §4–§5, lane P3, 28 October 2026)

The «not enforced in code until R-SC-1» of §1 is superseded: R-SC-1 is a real production control. It is a setting
read by a guard module of its own, not a feature flag of `apps/core/gates.py` (lane C's file): a setting, so that no
back-office toggle can open it in production:

- `ILE_SPECIAL_CATEGORY_FLOWS_ENABLED` — off in `base.py` and `prod.py`; prod.py refuses it on without
  `ILE_SPECIAL_CATEGORY_BASIS_REFERENCE` (the written approval of the art. 9 condition, checklist A-31); on in the
  preview (`dev.py`, DEBUG) and the test suite.
- `apps/core/special_category.py` — the guard every flow asks.

| Row | Production (switch off) | Preview (switch on) |
|---|---|---|
| S-02 a piece that names a special-category document (medical certificate, disability, religious certificate, union card, fingerprints… — `SPECIAL_CATEGORY_TERMS`) | **not offered**: no Dépôt, no act on the register, a calm sentence on the piece's page; refused by `documents.services.file_version` whatever the road | offered |
| S-01 the loose upload | the named kinds only (identity, diploma, contract); «Autre document» not offered, refused if posted; G-UPLOAD beside the kind | every kind; G-UPLOAD |
| S-02 any other piece (passport, diploma, civil record…) | open; the depot note stays | open |
| S-03 helpdesk messages | open, with G-FREE | open, with G-FREE |
| S-05 the case file's reason | open, with G-FREE | open, with G-FREE |

S-04, S-06, S-07 and S-15 are staff/assignee texts about the person, not flows that solicit data from the person;
they keep their minimisation help texts (R-SC-4 stays a request). Nothing was deleted from the local product and no
«explicit consent» box was added. Tests: `apps/documents/tests/test_special_category_v517.py` (DENY and ALLOW, and
prod.py loaded in a subprocess). The feature table is [`PREVIEW_VS_PRODUCTION.md`](PREVIEW_VS_PRODUCTION.md).

How the guard recognises a piece, and what it does not cover (review of lane P3):

- It reads the requirement's **code and title only**, never its detail: a detail often says what NOT to send («sans
  mention religieuse», «no health data»), and reading it would close an ordinary piece.
- Biometric data is matched by name («données biométriques», «dati biometrici», «biometric data», fingerprints),
  never by the bare stem: «Passeport biométrique» and «Photo d'identité biométrique» stay open, since a photograph is
  biometric data only when processed to uniquely identify a person (recital 51).
- **Residual risk.** The control works from the piece's NAME. A staff member can still declare
  (`documents.services.declare_requirement`) a piece that solicits art. 9 data under a neutral title, and the guard
  will not see it. Until a check at declaration time exists (follow-up R-P3-6: with the switch off, warn or refuse
  there), this is held by the declaring staff's instruction and the legal review of the requirement catalogue
  (checklist A-31). Recorded in the DPIA as part of RK-2.

## 4. User-facing guidance (UI guidance, not legal content)

Two sentences. The French text is the catalogue source; the Italian, English and Arabic texts are for the catalogue
owner (lane D, `locale/*/LC_MESSAGES/django.po`), to be reviewed with the other translations.

**G-FREE — free-text fields**
- fr (msgid): «N’indiquez pas de données sur la santé, l’origine ethnique, les convictions religieuses ou
  philosophiques, les opinions politiques, l’appartenance syndicale, la vie sexuelle ou l’orientation sexuelle :
  elles ne sont pas nécessaires ici.»
- it: «Non indicate dati sulla salute, sull’origine etnica, sulle convinzioni religiose o filosofiche, sulle opinioni
  politiche, sull’appartenenza sindacale, sulla vita sessuale o sull’orientamento sessuale: qui non sono necessari.»
- en: «Do not include information about health, ethnic origin, religious or philosophical beliefs, political
  opinions, trade-union membership, sex life or sexual orientation: it is not needed here.»
- ar: «لا تذكروا هنا بيانات عن الصحة أو الأصل العرقي أو المعتقدات الدينية أو الفلسفية أو الآراء السياسية أو الانتماء
  النقابي أو الحياة الجنسية أو التوجه الجنسي: فهي غير ضرورية.»

**G-UPLOAD — uploads**
- fr (msgid): «Ne déposez que les pièces nécessaires à votre démarche : aucun document médical ni aucun document qui
  révèle la santé, l’origine ethnique, les convictions, les opinions, l’appartenance syndicale, la vie sexuelle ou
  l’orientation sexuelle.»
- it: «Caricate solo i documenti necessari alla vostra pratica: nessun documento medico né alcun documento che riveli
  la salute, l’origine etnica, le convinzioni, le opinioni, l’appartenenza sindacale, la vita sessuale o
  l’orientamento sessuale.»
- en: «Upload only the documents your application needs: no medical document, and no document that reveals health,
  ethnic origin, beliefs, opinions, trade-union membership, sex life or sexual orientation.»
- ar: «لا تحمِّلوا إلا الوثائق اللازمة لملفكم: لا وثائق طبية، ولا أي وثيقة تكشف عن الصحة أو الأصل العرقي أو المعتقدات أو
  الآراء أو الانتماء النقابي أو الحياة الجنسية أو التوجه الجنسي.»

**Applied by this lane** (form slices). This lane adds **no new catalogue message**: lane D owns `locale/`, and
`tests/i18n/test_catalogues.py` requires every source message translated. The public forms' existing message
«Merci de ne pas indiquer de données sensibles (santé, origine, opinions, etc.) dans ce champ.» is already translated
in it/en/ar. As `apps/core/forms.py` `SPECIAL_CATEGORY_GUIDANCE` it is now applied to:
- the help text of the helpdesk message (`apps/helpdesk/forms.py` `MessageForm.body`, S-03), which had none;
- the Virtual Forum's discussions and replies, after «Texte simple ; aucune donnée personnelle de tiers.»
  (`apps/community/forms.py`, S-10; `core.forms.with_guidance`).

The upload already carries guidance: the description's «N’indiquez aucune donnée sensible.» and the depot note
«Ne déposez aucune donnée sensible qui ne vous est pas demandée.». G-FREE and G-UPLOAD are the fuller wording,
**requested** from lane D (R-SC-5): add both messages with the it/en/ar texts above. Then:
- G-UPLOAD becomes the help text of the loose upload's «Type de document» (`apps/documents/forms.py`);
- G-FREE replaces `SPECIAL_CATEGORY_GUIDANCE`'s message.

Both are one-line changes, which the documents owner or this lane makes after D's pass.

**Requested** (templates and models of other lanes):
- R-SC-2 (lane A, `templates/documents/partials/depot.html`): the depot note under a **requirement's** upload keeps
  «Ne déposez que la pièce demandée ici.». The loose upload's note «Ne déposez aucune donnée sensible qui ne vous est
  pas demandée.» could become G-UPLOAD, the same words as the form.
- R-SC-4 (portal/cases/enquiries owners): G-FREE as the help text of the staff free texts S-04, S-05, S-15 (model
  `help_text`, beside `DATA_MINIMISATION_HELP`).

## 5. Technical minimisation — concrete changes (requests; none is this lane's code)

| # | Change | Where | Why |
|---|---|---|---|
| T-1 | The loose upload's `kind` has **no default** (today `initial=DocumentKind.OTHER`). The person must say what the piece is | `apps/documents/forms.py` (documents owner) | a default «Autre document» invites the «just in case» upload (§6) |
| T-2 | In production, the loose upload (no requirement) is **off**, or limited to the kinds a pathway needs; a piece is filed only against a named requirement | `documents` views and policy | V5.16 §6: «Do not collect broad documents "just in case"» |
| T-3 | Every requirement that asks for a document says **which** document, and none asks for a medical or religious document until an art. 9 condition is approved | the requirement seeds/checklists (`documents_refresh_requirements`, `pathways`) | S-02 |
| T-4 | `retention_until` is set by code from a policy, not by hand (TG-2) | `apps/documents/models.py:94` | minimisation by time; OF-07 |
| T-5 | The e-mail outbox drops the body after a successful send (TG-3; DC Q-04) | `apps/notifications` | form copies are kept with no purge |
| T-6 | The R-SC-1 gate (§3) | `apps/core/gates.py` | the production flow stays closed |
| T-7 | No «explicit consent» box is added as a universal fix (§5) | — | a consent cannot be required for the service it conditions; the legal review chooses the art. 9 condition, if any |
