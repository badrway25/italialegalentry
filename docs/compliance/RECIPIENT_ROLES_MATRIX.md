# Recipient roles matrix (V5.16 §9)

- Written 28 October 2026 by lane P2 (label `v516-p2-build`), from the product's actual workflow
  (`apps/accounts/roles.py`, the policies of `cases`, `documents`, `academy`, `selection`, `portal`, `helpdesk`) and
  the runbook.
- Directive V5.16 §9: «Do not classify every external actor generically as "processor".» **A**: on documented
  instructions → candidate processor; **B**: independently determines purposes/means → candidate independent
  controller; **C**: jointly → possible joint controllers. «Create the matrix but do not invent the legal
  classification. Processors require the appropriate Article 28 contractual arrangement.»
- **Every classification below is to be confirmed by legal review.** It is a candidate, with the reason the code
  gives, never a decision.
- The candidate controller is AGAMI APS (OF-01, OWNER CONFIRMATION REQUIRED). «The controller» below means that
  candidate.
- Persons who act **under the controller's authority** (its staff, volunteers, members acting for it) are not
  recipients in the art. 4(9) sense of third parties. They are authorised persons (art. 29 GDPR; art. 2-quaterdecies
  Codice privacy) and need written instructions. They are listed as **I — internal**. If one of them is in fact an
  external organisation, it moves to A, B or C.

| # | Actor | What it receives in the workflow | Candidate class | Reason | Arrangement needed |
|---|---|---|---|---|---|
| R-01 | **Hosting provider** — DigitalOcean, the intended provider (V5.16 §10) | everything stored on the droplet, the database and the volumes | **A** — candidate processor | it hosts on the controller's behalf and does not use the data for its own purposes (ANX §5 «prestataires assurant … l'hébergement … actes de désignation au sens de l'art. 28») | **art. 28**: DigitalOcean's DPA accepted for the production account; sub-processor list; region and transfers → PRODUCTION CONFIGURATION REQUIRED (OF-02) |
| R-02 | **SMTP provider** (not chosen; `EMAIL_HOST=<smtp-host>`) | every outgoing e-mail: verification and reset links, notifications, form copies | **A** — candidate processor | it delivers mail on instructions | **art. 28** DPA; region/transfers → PRODUCTION CONFIGURATION REQUIRED (OF-03) |
| R-03 | **Mail host of contact@agamieuromed.org** | every form copy (IMPL p.2: all forms go to that address) | **A** — candidate processor of the controller | it hosts the controller's mailbox | **art. 28** (usually the provider's standard terms) → PRODUCTION CONFIGURATION REQUIRED (OF-03) |
| R-04 | **Off-server backup storage** (not decided) | the encrypted backups (gpg to the owner's key) | **A** — candidate processor | storage on instructions; the data are encrypted before they leave | **art. 28** → PRODUCTION CONFIGURATION REQUIRED (OF-04) |
| R-05 | **Controller's staff roles**: staff, administrator, superadmin, content editor, legal editor/approver, moderator (`apps/accounts/roles.py:12-38`) | within their role: back office, case views, consent records, audit (administrator) | **I** — internal, authorised persons | they act for the controller | written instructions and authorisation (art. 29; art. 2-quaterdecies); MFA already enforced |
| R-06 | **Operators** (`role:operator`, «handles case files and the help desk day to day») | the case files and helpdesk tickets assigned to them | **I** if the controller's people; **A** if an external organisation works on the controller's instructions | the code gives the operator the controller's operational tasks | instructions; **art. 28** if external |
| R-07 | **Professionals** (`role:professional`; assigned to a case; answer helpdesk requests that ask for professional review, `apps/helpdesk/forms.py` `professional_review`) | the case file and the documents of the persons assigned to them | **B** — candidate independent controller, or **A** | a lawyer or consultant giving professional advice usually decides the means of that advice under their own professional duties (→ B). If they only execute the controller's service under its instructions → A. The code records the reply «attributed to your function, never to your name» (`ResponseForm`), which suggests a service on the controller's behalf | **LEGAL REVIEW REQUIRED**: B → own notice and a data-sharing arrangement; A → **art. 28** |
| R-08 | **Authorised actors**: employment agencies, authorised intermediaries, public employment services, bilateral bodies, authorised professionals (`apps/selection/models.py:56-68`) | within a live mandate: the person's competences, evidence and process stages | **B** — candidate independent controller; **C** possible | they carry out a selection reserved to them by law, under their own authorisation; «Italy Legal Entry is NEVER the intermediary» (`apps/selection/models.py:4-6`) → own purposes and legal duties (B). The platform imposes the means of the chain (mandate → process → disclosure), which may make the platform's part joint (C) | **LEGAL REVIEW REQUIRED**: B → a sharing arrangement and their own notice; C → art. 26 arrangement, its essence made available to the persons |
| R-09 | **Training providers / universities as course providers** (`role:training_provider`; `apps/academy/policies.py` `_training_body_of`) | the enrolments and attendance of their own courses; the plan items where assigned (`PLAN_ASSIGNEE_ROLES`) | **B** — candidate independent controller, or **A** | a provider that delivers and certifies its own course keeps its own training records (B); a provider delivering a course on the controller's behalf only (A) | **LEGAL REVIEW REQUIRED** per provider |
| R-10 | **Companies** | their own account and needs; a **person's identity only** through an `IdentityDisclosure` the person consented to, for a named purpose, at most 180 days, every access logged (`apps/selection/models.py:711`, `:729`, `:858`) | **B** — candidate independent controller for the disclosed identity | the company uses the identity for its own recruitment purposes | **LEGAL REVIEW REQUIRED**: B → the person's consent (M-13) plus the company's own notice; no art. 28 |
| R-11 | **Institutions** (`role:institution`) and **universities** (`role:university`) as organisations | their own organisation workspace (`apps/portal/services.py` `ORGANISATION_ROLES`). No policy found by this lane gives them a person's case file | **B** for what they send or receive as organisations; **n/a** for persons' case data (not received) | public bodies act under their own legal tasks | **LEGAL REVIEW REQUIRED** if a workflow later shares a person's data with them |
| R-12 | **Organisation managers** (members of an organisation, `documents/policies.py`) | the organisation's documents | **I** for their own organisation's data | they are the organisation's own people | — |
| R-13 | **Other Virtual Forum members** (closed) | only what a member chose to show (`show_name`, `show_organisation` default False) and their posts | **B**? Not a recipient on the controller's behalf | users of the forum | **LEGAL REVIEW REQUIRED** before the Virtual Forum opens |
| R-14 | **CRM integration** (inactive: `LoggingTransport`) | ids and closed codes only | **A** if ever enabled | — | art. 28 before `INTEGRATIONS_ALLOW_NETWORK` is set |
| R-15 | **Public authorities on a legal request** (e.g. the Garante, courts) | what the request requires | **B** — independent controllers | own legal powers | none (art. 6(1)(c) for the disclosure: LEGAL REVIEW REQUIRED) |

## What the notice may say today

The notice lists recipient **categories** (lane P audit OF-12). Its marker **OF-12 — LEGAL REVIEW REQUIRED** stays
until the legal review fixes each category's role. Then:
- A-class providers are named with their art. 28 agreements (OF-02 to OF-04: PRODUCTION CONFIGURATION REQUIRED);
- B-class recipients are named as categories of independent controllers;
- a C-class arrangement is described in its essence (art. 26(2)).
