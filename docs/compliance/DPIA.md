# Data protection impact assessment (art. 35 GDPR) — IN PREPARATION

- Prepared 28 October 2026 by the privacy lane P3 (label `v517-p3-build`), on branch `v517-p3` from `design-v5`
  `e580b41`. Owner directive V5.17 §3: «proceed on the assumption that a DPIA should be prepared unless the
  legal/privacy review produces a documented reasoned conclusion that it is not required … Prepare the assessment
  structure and evidence now from known facts. Leave only genuinely unknown production/governance facts open.»
- **Status: IN PREPARATION. Not signed, not a legal determination.** It becomes the DPIA when the controller signs it
  with the legal review (and the DPO's advice, art. 35(2), if one is designated). Production gate: checklist **A-32**.
  It blocks PRODUCTION_READY, **not** PRODUCT_COMPLETE (runbook *States*, V5.17 §2).
- Structure: art. 35(7) GDPR — (a) the description of the processing and its purposes, (b) necessity and
  proportionality, (c) the risks to the rights and freedoms of data subjects, (d) the measures — plus the residual
  risk, the consultation (art. 35(2), 35(9), 36) and the sign-off. The WP248 rev.01 guidelines (endorsed by the EDPB)
  and the Garante's list (provv. n. 467 of 11 October 2018) are the references; why a DPIA is prepared is in
  [`DPIA_NECESSITY.md`](DPIA_NECESSITY.md).
- Every fact below is read from the code, the settings, the runbook or the compliance matrices of this folder; each
  cites its evidence. What nobody knows yet is marked **OPEN** with its class, as the privacy notice's open fields are:
  **PRODUCTION CONFIGURATION REQUIRED** (known when the server is prepared, checklist A-30 — never a question to the
  owner now, V5.17 §10), **OWNER CONFIRMATION REQUIRED**, **LEGAL REVIEW REQUIRED**. §9 lists them all.
- The team's risk ratings in §5 are a **preliminary technical rating** to be validated by the controller; they are
  not a legal conclusion. Nothing here invents a legal basis, a retention period, a recipient or a controller.
- Repository-safe: no secret, no personal data of a real person, no server identity.

## 1. Context and responsibilities

| Item | Known fact | Evidence | Open |
|---|---|---|---|
| Controller | AGAMI — Dialogo Giuridico Interculturale APS is the **candidate** controller (ANX §1.1) | [`PRIVACY_PROCESSING_AUDIT.md`](PRIVACY_PROCESSING_AUDIT.md) §1; `config/settings/base.py` `ILE["PROMOTER"]` | **OPEN — OWNER CONFIRMATION REQUIRED** (OF-01, V5.17 §6) |
| DPO | none named in any approved document | [`DPO_ASSESSMENT.md`](DPO_ASSESSMENT.md) | **OPEN — DPO STATUS = TO BE CONFIRMED** (OF-08, V5.17 §11) |
| Processors and other controllers | the candidates and their roles | [`RECIPIENT_ROLES_MATRIX.md`](RECIPIENT_ROLES_MATRIX.md) R-01 … | **OPEN — LEGAL REVIEW REQUIRED** (OF-12; art. 28 arrangements) |
| Hosting | DigitalOcean is the intended provider | RECIPIENT_ROLES_MATRIX R-01; runbook | **OPEN — PRODUCTION CONFIGURATION REQUIRED** (OF-02: region, DPA, sub-processors, transfers) |
| Who carried out the assessment | the privacy lane, from the repository | this file | the controller's signatory, §10 |

## 2. Systematic description of the processing — art. 35(7)(a)

### 2.1 Nature

A web platform (Django 5.2, PostgreSQL, behind nginx and Gunicorn; runbook) with a public site and a reserved area.
The reserved area is open only to accounts that staff create while public sign-up is closed by gate G2
(`apps/accounts/adapters.py`, `apps/core/gates.py`). No AI, no profiling for marketing, no biometric processing, no
automated decision with legal effect (ANX §4; `DPIA_NECESSITY.md` §2 criteria 2 and 8). No analytics, no third-party
cookie, no external request from the public pages (measured 28 Oct 2026; CSP `'self'`, `config/settings/base.py`;
audit §0).

### 2.2 Scope — the processing operations

The matrix rows are [`PROCESSING_PURPOSE_MATRIX.md`](PROCESSING_PURPOSE_MATRIX.md) M-01 … M-21. The DPIA covers the
ones that make the processing high-risk (DPIA_NECESSITY §1):

| Operation | Data | Matrix | State today |
|---|---|---|---|
| Orientation and pathway pre-assessment | situational choice keys, `ip_hash`, result and rule versions; `PathwayAssessment` rationale | M-06, M-07 | live; anonymous answers purged after 30 days (`apps/orientation/constants.py`) |
| Private documents | identity documents, diplomas, contracts, civil records; name, kind, size, sha256, `uploaded_ip_hash` | M-08 | live for staff-created accounts; special-category pieces closed in production (R-SC-1, §6) |
| Case files | status history, checklists, deadlines, portal messages, suspension reasons | M-09 | live |
| Helpdesk | the person's question, messages, internal notes, dispatch to a professional | M-10 | live |
| Academy | enrolments, plans, competence levels, attendance | M-11 | live |
| Authorised selection and identity disclosure | competences and evidence; identity fields disclosed to a company on the person's consent, with purpose and ≤ 180 days | M-12, M-13 | live for staff-created accounts |
| Accounts, MFA, sessions, audit trail, logs, outbox, backups | as the matrix | M-01 … M-05, M-19, M-20 | live |

### 2.3 Context — the data subjects

Mostly third-country nationals preparing a regular entry to Italy (work, study, family reunification, research;
`apps/orientation/seeds.py`), plus the staff of companies, institutions, universities and training bodies, and
professionals, operators and authorised actors acting on files (`accounts/roles.py`). The persons depend on documents
and on the actors around them: WP248 criterion 7 (vulnerable data subjects) is **likely met** (DPIA_NECESSITY §2).

### 2.4 Purposes

As the matrix's «Purpose» and «Necessity» columns state them, row by row. The legal basis of the authenticated
platform is **OPEN — LEGAL REVIEW REQUIRED** (OF-10); no basis is assumed here.

### 2.5 Recipients and flows

The person; the assignees of the person's file (professional, operator, training provider, authorised actor) through
an assignment with a validity date (`apps/documents/models.py` `readable_by`); a company only through an identity
disclosure the person grants (`apps/selection/models.py`); staff; the candidate processors (hosting, SMTP, forms
mailbox host, off-server backups — RECIPIENT_ROLES_MATRIX R-01 … R-04). The CRM integration sends nothing
(`INTEGRATIONS_TRANSPORT=LoggingTransport`). Transfers outside the EU/EEA: none performed by the code; the providers'
locations are **OPEN — PRODUCTION CONFIGURATION REQUIRED** (OF-02 … OF-04).

### 2.6 Retention

Configured: sessions 8 h (`config/settings/base.py` `SESSION_COOKIE_AGE`), anonymous orientation 30 days, public
forms 24 months (ANX §7; enforced for enquiries only), nginx logs 14 days and local backups 7 days (runbook).
Everything else — accounts' inactivity, documents (`retention_until` NULL by default), case files, helpdesk, Academy,
selection, the audit trail, the outbox, off-server backups — is **OPEN — LEGAL REVIEW REQUIRED** (OF-06, OF-07) or
**PRODUCTION CONFIGURATION REQUIRED** (OF-04, OF-05) (matrix «Retention»).

## 3. Necessity and proportionality — art. 35(7)(b)

| Principle | What the platform does | Evidence | Open |
|---|---|---|---|
| Lawfulness (art. 6, 9) | the bases are candidates per purpose, never 6(1)(b) by default; no art. 9 condition exists, so no flow that intentionally solicits art. 9 data is offered in production | PROCESSING_PURPOSE_MATRIX; [`SPECIAL_CATEGORY_AUDIT.md`](SPECIAL_CATEGORY_AUDIT.md); `apps/core/special_category.py` | **LEGAL REVIEW REQUIRED** (OF-10, the LIAs of M-01 … M-03, the art. 9 position) |
| Purpose limitation | each module has its own data; the selection domain refuses age, nationality, gender, health, religion and union fields | `apps/selection/models.py` | — |
| Data minimisation | situational choice keys, no free text in orientation; the loose upload offers named kinds only in production; minimisation guidance under free texts and uploads (it/fr/en/ar); IP stored only as a salted hash | `apps/orientation/seeds.py`; `apps/core/special_category.py`; `apps/core/privacy.py` | — |
| Accuracy | the person files new versions; history kept; validity dates per piece | `documents.services.file_version` | — |
| Storage limitation | see §2.6 | matrix | **OPEN** (OF-04 … OF-07) |
| Integrity and confidentiality | see §6 | — | — |
| Transparency | the privacy notice is written from the real processing, its open fields classified; production refuses it while one remains | `apps/legal/content/privacy/*`; `legal.services.publish`; `apps/legal/tests/test_production_privacy_page_v517.py` | the notice's open fields (A-29) |
| Data subjects' rights | self-service account deletion/anonymisation | `apps/accounts/urls.py`, `accounts.services` | the procedure for the other rights: **LEGAL REVIEW REQUIRED** |
| Processors | candidates named, roles classified | RECIPIENT_ROLES_MATRIX | **OPEN** art. 28 contracts (OF-12, OF-02, OF-03) |
| Transfers | none by the code | audit §2 | **OPEN — PRODUCTION CONFIGURATION REQUIRED** (OF-02 … OF-04) |

## 4. Sources of risk

- an unauthorised reader inside the platform (an expired or wrong assignment, a guessed identifier);
- an account takeover (credentials, phishing);
- the leakage of a stored file (misconfigured web server, backup copy);
- over-collection: a «just in case» upload, special-category content in free text;
- retention without an end (documents, outbox, audit trail);
- a processor or a transfer that is not under contract;
- an informational pre-assessment read as a decision on the person's entry.

## 5. Risks to the rights and freedoms of data subjects — art. 35(7)(c)

Preliminary technical rating (likelihood × severity, low / medium / high), **before** the measures of §6 and after
them (residual). The controller validates or changes each one.

| # | Risk | Impact on the person | Before | Measures (§6) | Residual |
|---|---|---|---|---|---|
| RK-1 | Illegitimate access to identity and pathway documents | identity fraud, exposure of the migration situation | high | T-1, T-2, T-3, T-4, T-5 | medium (OPEN: antivirus, retention) |
| RK-2 | Special-category data received without an art. 9 condition | unlawful processing of health, religion, sex life… | high | T-6, T-7 | low in production (closed flows, recognised by the piece's code and title); medium for free text (guidance only) and for a piece declared by staff under a neutral title, which the guard does not see (SPECIAL_CATEGORY_AUDIT §3.1, follow-up R-P3-6) |
| RK-3 | An account takeover of a role that reads others' files | access to many files | medium | T-2, T-8 | low |
| RK-4 | A pre-assessment taken as a decision | wrong decisions by the person; loss of a chance | medium | T-9 | low |
| RK-5 | Storage without an end | exposure grows with time | high | T-10 (partial) | **OPEN** until OF-06/OF-07 are set |
| RK-6 | Disclosure to a company beyond the person's will | discrimination in recruitment | medium | T-11 | low |
| RK-7 | Processors or transfers without a contract | loss of control, third-country access | medium | — | **OPEN — PRODUCTION CONFIGURATION REQUIRED** (A-30) |
| RK-8 | Logs that hold more than needed | tracking of a person's requests | low | T-12 | low (OPEN: journald retention OF-05; catch-all log R-4) |

## 6. Measures envisaged — art. 35(7)(d)

| # | Measure | Evidence | State |
|---|---|---|---|
| T-1 | authorisation in the queryset: a reader who may not see a row cannot tell it from one that does not exist; assignments carry a validity date; revoked mandates grant nothing | `apps/documents/models.py` `readable_by`; `apps/documents/tests/test_requirement_views.py` | in code |
| T-2 | MFA for every role that can read another person's data, enforced in the reserved area and the back office | `apps/accounts/services.py` `MFA_REQUIRED_ROLES`; `apps/accounts/middleware.py`; checklist A-13 | in code |
| T-3 | private storage outside every served directory; download only by a signed link valid 10 minutes; settings refuse an overlap | `apps/documents/services.py` `DOWNLOAD_LINK_MINUTES`; `config/settings/prod.py` | in code |
| T-4 | uploads: allow-list PDF/JPEG/PNG, 10 MB, magic-byte check, active PDF content refused, random storage name | `apps/documents/services.py` `validate_upload`; `apps/documents/tests/test_upload.py` | in code |
| T-5 | antivirus scan | `DOCUMENT_SCANNER` empty: uploads stay «not analysed», which the page states | **OPEN — PRODUCTION CONFIGURATION REQUIRED** |
| T-6 | **R-SC-1**: no flow that intentionally solicits special-category data is offered in production — such a piece is not offered for filing and is refused by the service; the loose upload's open «Autre document» is not offered | `apps/core/special_category.py`; `config/settings/prod.py`; [`PREVIEW_VS_PRODUCTION.md`](PREVIEW_VS_PRODUCTION.md); `apps/documents/tests/test_special_category_v517.py` | in code |
| T-7 | minimisation guidance under the free texts and the uploads (G-FREE, G-UPLOAD, four languages); no universal «explicit consent» box | `apps/core/special_category.py`; `apps/helpdesk/forms.py`; `templates/cases/partials/state_dialog.html` | in code |
| T-8 | sessions 8 h; sign-in throttles; failed sign-ins audited without the submitted address | `config/settings/base.py`; `apps/audit/receivers.py` | in code |
| T-9 | the orientation and assessments are informational and say so; no automated decision | ANX §4; orientation result pages | in code |
| T-10 | retention: orientation 30 days and enquiries 24 months purged daily; sessions cleared daily | `apps/orientation`; `apps/enquiries/services.py`; runbook §10 | partial: **OPEN** OF-06/OF-07 (documents, outbox, audit trail; TG-1 … TG-3) |
| T-11 | identity disclosure only on the person's specific consent, with a purpose, ≤ 180 days and every access recorded | `apps/selection/models.py`, `apps/selection/services.py` | in code |
| T-12 | logs: no raw IP or e-mail in the application log; redaction filter; nginx access log masked, without query string | `config/log_filters.py`; `tests/security/test_log_privacy.py`; runbook §11 | in code; nginx error/catch-all as audit LG-2/LG-3 |
| T-13 | an audit trail of sign-ins, role grants, downloads and case views | `apps/audit/` | in code (retention OPEN, OF-06) |
| T-14 | backups encrypted to the owner's key | runbook §10 | in code; off-server location **OPEN — PRODUCTION CONFIGURATION REQUIRED** (OF-04) |

## 7. Residual risk and conclusion

With the measures of §6 in place, the team's preliminary view is that **no residual risk is rated high**, provided
that the OPEN items of §9 marked as blocking are closed: retention (RK-5) and the processors and transfers (RK-7)
stay unrated until then. If the controller rates a residual risk high after the measures, the prior consultation of
the Garante (art. 36) applies. **OPEN — LEGAL REVIEW REQUIRED** (the controller's own conclusion).

## 8. Consultation

| Who | Rule | State |
|---|---|---|
| DPO | art. 35(2): the controller seeks the DPO's advice, where designated | **OPEN** — DPO STATUS = TO BE CONFIRMED (OF-08) |
| Data subjects or their representatives | art. 35(9): «where appropriate» | **OPEN — LEGAL REVIEW REQUIRED** (whether and how) |
| Processors | art. 28(3)(f): assistance | **OPEN** with the art. 28 contracts (OF-12) |
| Supervisory authority | art. 36: only if a high residual risk remains | §7 |

## 9. Open facts (only what is genuinely unknown)

| # | Fact | Class | Where it closes |
|---|---|---|---|
| D-1 | the controller (AGAMI APS, the candidate) | OWNER CONFIRMATION REQUIRED | OF-01, checklist A-33 |
| D-2 | DPO status | TO BE CONFIRMED (LEGAL REVIEW REQUIRED) | OF-08, A-33 |
| D-3 | the legal basis of the authenticated platform; the LIAs of M-01 … M-03 | LEGAL REVIEW REQUIRED | OF-10, A-33 |
| D-4 | an art. 9 condition, if any flow is ever to be opened | LEGAL REVIEW REQUIRED | A-31 |
| D-5 | retention per purpose (documents, case files, helpdesk, Academy, selection, audit trail, outbox, accounts) | LEGAL REVIEW REQUIRED | OF-06, OF-07, A-33 |
| D-6 | recipients' roles and the art. 28 contracts | LEGAL REVIEW REQUIRED | OF-12, A-33 |
| D-7 | hosting region, DPA and sub-processors; SMTP provider; mailbox host; off-server backups; journald retention | PRODUCTION CONFIGURATION REQUIRED | OF-02 … OF-05, A-30 (verified when the server is prepared) |
| D-8 | the antivirus scanner | PRODUCTION CONFIGURATION REQUIRED | `DOCUMENT_SCANNER`, A-30 |
| D-9 | the expected scale (number of persons, files, organisations) | OWNER CONFIRMATION REQUIRED | DPO_ASSESSMENT facts 1, 2, 4 |
| D-10 | the residual-risk conclusion and the consultation (§7, §8) | LEGAL REVIEW REQUIRED | §10 |

## 10. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Controller | — | — | — |
| Legal review | — | — | — |
| DPO (if designated) | — | — | — |

The DPIA is reviewed when a flow closed by R-SC-1 opens, when a new processor is added, when the scale changes, and
at least before each release that adds a processing operation.
