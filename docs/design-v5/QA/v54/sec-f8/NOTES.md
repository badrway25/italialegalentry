# sec-f8 — the back office as a second way into personal data (finding F-8) — notes

A security fix, not design work (V5.5 delivery mode; V5.9: nothing deployed, production untouched). Branch
`v54-sec-f8`, worktree `C:/tmp/ile_wt/v54-sec-f8`, from design-v5 at `5bf2f90`. Implementer `sec-f8-fix`,
16 October 2026. Lane 7: pytest on `test_ile_v5_l7`, one run at a time, `-p no:randomly`; no lane server was needed.
Personas only through minted sessions (`Client.force_login`), test users with test-only passwords. Scratch scripts and
logs outside every repository: `C:/tmp/ile_v5_council/.work/sec-f8/`.

**F-8** (sec-f7's review, «observation for the back-office hardening»; GitHub checkpoint #3's adversary on design-v5
`5bf2f90`): the back office (`/backoffice/`, unfold, `accounts.admin_site.BackofficeAdminSite` — staff reach it only
after their second factor since sec-f5) is a second way into personal data that the platform's object policies do not
govern. `CaseFileAdmin` has no queryset limit, so role:operator — which holds the «cases» view/change model permissions
(`accounts.roles.ROLE_PERMISSIONS`, seeded in production by `seed_all`) — lists and reads every case file there, while
`docs/security/PERMISSION_MODEL.md` §5.1 says «assigned (D)» and `cases.policies` / `CaseFileQuerySet.readable_by` give
an unassigned operator nothing on the platform side.

Also open, and in this brief: the case checklist inline stays editable on any file and a line's status changed there
writes no `case.checklist.status` event (sec-f7 NOTES «Review fixes» 2; DL54-132 item 11); the policies' administrator
branch ignores read-only (the checklist policy lets an administrator change a CLOSED file's lines; sec-f7 NOTES, «The
review's other observations stand»); the second-factor perimeter is defined by PATH, so privileged staff actions on
public paths are outside it (sec-f5 REVIEW, «Outside this fix»); NUL bytes inside JSON bodies sent to the integrations
API were never probed (DL54-152 item 8).

## 1. The audit — before any change

Every ModelAdmin and inline registered on the back office was listed mechanically (the registry of
`accounts.admin_site.BackofficeAdminSite`, crossed with `ROLE_PERMISSIONS` and with every policy registered in
`accounts.permissions`: 166 rows; script and output in `.work/sec-f8/inventory.py`, `inventory.txt`, `policies.py`), then
each screen that shows or changes personal or case data was read. Facts are as of design-v5 `5bf2f90`.

**How the back office decides today.** A screen opens to an active `is_staff` account that has passed the second factor
(sec-f5) and holds the model permission. `ROLE_PERMISSIONS` grants by APPLICATION (`"cases": ("view", "change")` covers
every model of `cases`), never by row. Django's `ModelAdmin.get_queryset` returns every row; `has_view_permission` /
`has_change_permission` ignore the object. The platform decides with the policies (`accounts.permissions.can`, deny by
default) and the `readable_by` querysets — per row, per role, per state. Nothing compared the two:
`tests/security/test_object_permissions.py::test_13_the_list_and_the_object_check_agree` compares the platform's list
with the platform's policy only. role:administrator holds no «cases», «helpdesk», «selection», «companies» or «academy»
model permission, so those screens are closed to it (it reads case files on the platform: `readable_by` gives it all);
a superuser holds every model permission and passes every policy (`can`: superadmin first) — the last resort by design
(PERMISSION_MODEL §3.4).

Legend — **Roles**: the roles whose model permissions open the screen (superuser always). **Rows**: what its queryset
returns to each of them. **Platform rule**: the app's policy / `readable_by`, and PERMISSION_MODEL where it has a row.

### 1.1 Case data

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `CaseFileAdmin` (`cases.CaseFile`) | operator (view, change): **every file** | `purpose`, `pathway_key` (owner, status, its trace and the suspension's reason read-only since sec-f7); no add; delete superuser only | `readable_by`: the owner, a live assignee, the administrator; `case_policy` change: the owner and a live professional/operator assignee while active, the administrator (ignoring CLOSED); §5.1 operator «assigned» | **MISMATCH — F-8.** The operator lists and opens every file and changes the purpose and the pathway of any file, CLOSED included (§4 rule 5). `purpose` and `pathway_key` are written by the domain from the orientation (`cases.intake`): the pathway is what the rule engine evaluates at the next reassessment, the purpose what keeps one active file per purpose (`case_for_purpose`) |
| ↳ `ChecklistInline` (`cases.ChecklistItem`) | operator (change; no add/delete perm): the lines of every file | `order`, `requirement`, **`status`**, **`responsible_actor`**, `responsible_note`, `due_date`, on any file, CLOSED included | `checklist_policy` change: a live professional/operator assignee while the file is active, the owner on PERSON lines only, the administrator (ignoring CLOSED); the platform changes a status only through `services.set_checklist_status` (event `case.checklist.status`); PERMISSION_MODEL §6 rule 5: `responsible_actor` is an authority field | **MISMATCH.** A status changed here writes no `case.checklist.status` (only the LogEntry mirror «admin.change»); `responsible_actor` decides who may tick the line (the person ticks PERSON lines only) — a capacity handed out with no domain event |
| ↳ `AssignmentInline` | read-only (sec-f7): every assignment of the file shown | none | `assignment_policy` view: the assignee, the file's owner, the administrator | follows the file — **MISMATCH with F-8** |
| ↳ `AssessmentInline` | read-only | none | follows the file | follows the file — **MISMATCH with F-8** |
| `CaseAssignmentAdmin` | operator (view; change refused by `assignment_policy`): **every assignment**; the add form's `case` autocomplete answers from `CaseFileAdmin`'s queryset | grant/revoke through the domain (sec-f7), superuser only | `assignment_policy` view: the assignee, the file's owner, the administrator | **MISMATCH.** The operator reads who holds which file under which authorisation; through `/backoffice/autocomplete/?app_label=cases&model_name=caseassignment&field_name=case` it enumerates every file's reference (Django checks the TARGET screen's view permission, which the operator holds) |
| `PathwayAssessmentAdmin` | operator (view): **every assessment** — the person's questionnaire answers, the rationale, the rules applied | read-only | `assessment_policy` view: the owner, a live assignee, the administrator | **MISMATCH** |

### 1.2 Documents and their files

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `PrivateDocumentAdmin` | administrator (view): every document, deleted ones included (metadata: owner, organisation, file name, size, hash, scan state) | read-only; `mark_clean`/`mark_infected` need «change» (superuser); `export_csv` (metadata, owner e-mails) on «view», **not audited** | `private_document_policy`: the administrator reads every alive document (case documents through `DocumentRequirement.readable_by`, loose ones as staff/administrator); download only of a clean file (`services.delivery_block`); §5.3 «Amministratore all (solo clean)» | consistent. **The back office cannot open or download a file another way**: the model has no FileField; the only link, for a superuser only, is `documents:download` → `documents.views._serve` (policy, `delivery_block`, throttle, audit event `documents.downloaded`); `DocumentVersionInline`'s `document` is a link to this metadata screen. Observations (§6): deleted rows' metadata listed; the export is not audited (AUDIT_MODEL's known gap) |
| `DocumentRequirementAdmin` (+ `DocumentVersionInline`, read-only) | administrator (view): every requirement | `refresh_states` needs «change» (superuser); state read-only | `requirement_policy`: view for the owner, a live assignee (non-restricted), the administrator; change/delete the administrator | consistent (the administrator holds view only) |

### 1.3 Help desk

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `HelpdeskTicketAdmin` | operator (view, change, add — every field read-only, no add, no delete): **every ticket** — reference, status, origin, its case (a link to the file's screen), assignee, mandate | none | `ticket_policy`: the operator **dispatches, never views**; `TicketQuerySet.readable_by` gives it nothing; its platform register is `dispatchable_by` (the requests waiting for a professional, the question deferred) | **MISMATCH.** The operator reads the shape of every request — live mandates and closed ones too — and reaches each request's file |

### 1.4 Requests, messages, enquiries

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `CompanyNeedsRequestAdmin`, `CollaborationProposalAdmin`, `ContactRequestAdmin` (`enquiries.PublicSubmission`) | staff (view, change), **operator (view, change)**, administrator (view, change, **delete**; add refused): every submission | workflow fields; `export_csv` (audited), `mark_handled`, `anonymise_selected` (irreversible), `export_json_single` (audited); `delete_selected` for the administrator | `submission_policy`: staff, administrator, superadmin view/change/export/anonymise; the owner views; **nobody deletes** (erasure is the anonymisation, which keeps the consent proof); §5.4 operator «scope (D)» | **MISMATCH.** (a) The operator reads, changes, exports and anonymises every public submission; (b) the administrator hard-deletes a submission and its consent proof with it |
| `MessageAdmin`, `DeadlineAdmin`, `PortalNoticeAdmin` (`RoleScopedAdmin`: `is_staff` + staff/administrator/superadmin, not model permissions) | staff: view, add, deadlines change; administrator: also change/delete messages | sent messages read-only once read; account by exact e-mail | `portal.policies`: Message view staff/administrator, change/delete administrator; Deadline view/change staff/administrator, delete administrator | consistent |

### 1.5 Accounts

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `UserAdmin` (+ `MembershipInline`) | administrator (view, change): every account | e-mail, password (change form), profile, `is_active`, **`is_staff`**, **`groups`** minus role:superadmin/role:administrator, memberships; `is_superuser` hidden and refused, superusers untouchable (L-01) | no policy for User; §5.10 administrator W «all **tranne** `is_superuser`, `is_staff`, `groups`» | departure from §5.10's matrix accepted by L-01's closure (it is how staff accounts are made) — **owner question Q-1**, not changed here |
| `OrganisationAdmin`, `PersonProfileAdmin` | administrator (view, change) | profile fields | §5.10 | consistent |
| allauth `EmailAddressAdmin`, `AuthenticatorAdmin`, `GroupAdmin`, `SiteAdmin` | nobody but a superuser (no role holds `account`, `mfa`, `auth`, `sites`) | — | — | consistent |

### 1.6 Audit events

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `AuditEventAdmin` | administrator (view), **legal_approver (view)**: every event — actors' e-mail addresses (`actor_label`), targets (case references, file names), metadata | read-only | AUDIT_MODEL §6.1: administrator and superadmin read everything, «tutti gli altri ruoli: nessun accesso — IMPLEMENTATO»; PERMISSION_MODEL §5.9 the same | **MISMATCH.** role:legal_approver reads the whole trail (`ROLE_PERMISSIONS`: «reads everything a reviewer needs») — every login, every file's events |

### 1.7 Notifications

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `EmailOutboxAdmin` | staff (view), **operator (view)**, administrator (view, change): every e-mail — recipient, subject, **bodies** (a portal message's text; a public submission's data for the forms inbox; a newsletter confirmation's links, **with their bearer tokens**), errors | `resend`, `cancel` declared **without permissions**: Django offers them to every account that opens the list | no policy; a body copies an object whose policy is `portal.policies` (Message: staff/administrator), `enquiries.policies` (staff/administrator), or a consent's token (nobody should hold it) | **MISMATCH.** The operator reads the content of every message to every person (the Message policy does not name it); view-only holders (staff, operator) requeue or cancel mail — a write on a view grant; whoever reads a confirmation can confirm a subscription in the subscriber's name |
| `NotificationAdmin` | staff, **operator** (view); administrator (view, delete): every notification — recipient, event, category, channel, its message | read-only | the record that a person was told something; its message is a portal Message | **MISMATCH for the operator** (the Message policy) |
| `NotificationPreferenceAdmin` | staff, **operator** (view); administrator (change): every person's e-mail switches | the administrator changes a person's choices | no policy | the operator: follows the row above. The administrator's change: observation (§6) |

### 1.8 Consents

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `ConsentRecordAdmin` | staff (view), administrator (view, change): every consent (e-mail, purpose, dates) | read-only fields; `withdraw_selected` declared **without permissions** | §5.11: the administrator records a withdrawal; staff not named | **MISMATCH.** role:staff, view-only, records the withdrawal of anyone's consent |
| `NewsletterSubscriptionAdmin` | staff (view), administrator (view, change): every subscription | **`confirm_token`, `unsubscribe_token` displayed**; the administrator edits the subscriber's `email` and `language` (the consent's subject) | the tokens are bearer secrets of the person (`consents.views.newsletter_confirm` / `newsletter_unsubscribe`) | **MISMATCH.** Whoever opens a subscription can confirm it in the subscriber's name — an opt-in nobody gave — or end it; the consent's evidence is editable |

### 1.9 Orientation

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `OrientationSessionAdmin`, `OrientationResultAdmin` | administrator (view, change, add refused): every session and result — `state` (the answers in progress), **`answers_snapshot`**, the account | read-only; `anonymise_action` (GDPR), `export_statistics_csv` (aggregates) | `orientation.policies`: a session and its result are its owner's, nobody else's — anonymous sessions nobody's | **MISMATCH.** The administrator reads every questionnaire's answers, anonymous ones included; the shape (reference, status, outcome, versions, dates) is what anonymisation on request and the statistics need |

### 1.10 Forum — the event, the governance module, the virtual forum

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| `ForumRegistrationAdmin` | staff (view, change), administrator (+ delete) | workflow; export, marks, anonymise | `forum.permissions`: administrator view/change/delete, staff view/change | consistent |
| Governance: `ForumEditionAdmin`, `CommissionAdmin` (+ commission, table and **mandate** inlines), `ForumProfileAdmin`, `CommissionMemberAdmin`, `TableAdmin`, `ForumProposalAdmin`, `ForumProjectAdmin` (+ milestone/monitoring inlines), `AnnualReportAdmin` | **staff (view, change, add)** — the «forum» grant covers the whole app; administrator (all) | everything but the states; mandates granted and revoked | `forum.governance_policies`: the whole module without a Forum profile is the **administrator's only** («`role:staff` is absent for the reason the case file records»); mandates «granted and revoked by the secretariat» | **MISMATCH.** role:staff reads every participation profile (its account), proposal and mandate, and grants mandates — a capacity on the platform (a live mandate reads a commission's proposals; a referent moderates its tables) |
| Virtual forum: `MembershipAdmin`, `RoomAdmin`, `DiscussionAdmin` (+ posts), `PostAdmin`, `PendingPostAdmin` (+ attachments), `ReportAdmin`, `ModerationActionAdmin`, `CalendarEntryAdmin`, `InitiativeAdmin` (+ collaborations) | moderator (view, change), **staff (view, change)**, administrator (all) | approve/suspend/trust members; approve/hide/unhide posts; close/reopen/hide discussions; handle reports | `community.policies`: moderators are role:moderator, role:administrator, role:superadmin; a membership is seen by its member or a moderator; hidden posts and reports by moderators only | **MISMATCH.** role:staff moderates and reads every membership — including the name and organisation a member chose not to show (`show_name`/`show_organisation`, REQ-FOR-06) — every hidden post and every report |

### 1.11 Selection, companies, Academy, integrations

| Screen | Roles · rows | Editable · actions | Platform rule | Verdict |
|---|---|---|---|---|
| every `selection`, `companies` and `academy` screen (processes, mandates, disclosures and accesses; needs, profiles, need assignments; enrolments, attendances, training plans) | nobody but a superuser: no role holds these apps' model permissions | (superuser) | their policies | consistent (superuser = last resort). Observation: `NeedAssignmentInline`, `ActorOperatorInline` and `TrainingPlanAdmin` edit outside the domain services — superuser only |
| `OutboundEventAdmin` | administrator (view): identifiers only | `requeue`, `cancel` declared **without permissions** | `ROLE_PERMISSIONS`: integrations «view» for the administrator | **MISMATCH** (a write on a view grant; no personal data) |
| `InboundWebhookLogAdmin`, `ApiKeyAdmin`, `ExternalSystemAdmin`, `ExternalReferenceAdmin`, `WebhookEndpointAdmin` | administrator (view) | read-only for it | identifiers, key hashes | consistent |

### 1.12 The second-factor perimeter and the API — what the audit found to probe

The middleware (`accounts.middleware.second_factor_response`) guards `/backoffice/`, the reserved area and
`/documents/` by PATH. Every privileged staff branch outside them, found by reading every `is_staff`, `has_perm`,
`has_role` and moderator test outside the admin and the policies:

| Path | Branch | Who |
|---|---|---|
| `/<lang>/forum-virtuel/…` | `community.views.member_required` and `index`: a moderator reads every room, hidden post and pending post, and moderates (`post_moderate`, `discussion_moderate`) | role:moderator, role:administrator, role:superadmin |
| `/<lang>/actualites/<slug>/` | `news.views.detail`: an unpublished article for `is_staff` + `news.view_article` | staff, content_editor, administrator |
| `/<lang>/vivre-en-italie/…?preview=1` | `living.views._check_gate`: `is_staff` + `living.view_livingtopic` | idem |
| `/<lang>/faq/`, `/<lang>/glossaire/…` | `faq.services.page_visible`, `glossary.services.page_visible`: any `is_staff` while Phase 3 is closed | every staff account |
| the ecosystem spaces, the pathways pages, the antifraud page, `?preview=1` | `ecosystem.services.can_preview`, `pathways.services.can_preview`, `pages.services.can_preview` | every staff account |

Not privileged, checked: the public forum event's views, partners, enquiries' forms, consents, orientation, the account's
own pages (`/compte/profil/…`: `request.user` only), `/api/` (an API key, never a session), the design preview and
`/_design/` (DEBUG only, absent under the test and production settings). Publishing news, «living» sheets and legal
texts happens in the back office's actions, inside the perimeter.

The integrations API (`/api/v1/…`): `inbound_webhook` parses its signed JSON body and writes `minimal_inbound_payload` (a
jsonb) and `event_type` (text) into `InboundWebhookLog`; on a refused signature it writes the `X-Nonce` and
`X-Timestamp` headers as received. `events_list` reads the query string (the NUL guard answers it); `events_ack` reads no
body; `authenticate` matches the key against a strict pattern before any query.

**Added 16 October, after the audit:** the owner's V5.10
(`C:/tmp/ile_v5_council/directives/V5_10_RELEASE_MAIN_D1_PREAPPROVED.md`, 08:15) makes F-8 a release blocker: the
audit's scope is not to be reduced, no access is to be widened, and every item of its list — case files, documents,
accounts and person data, requests / help desk / selection, admin, audit, 2FA, the integrations API — is verified with
DENY tests as strong as the ALLOW tests. §4 maps each item to its tests.

## 2. Root causes

1. **Two authorities, never compared.** The back office asked the model permission alone; the platform asks the
   object policy and the `readable_by` querysets. `ROLE_PERMISSIONS` grants by application — role:operator's
   «cases» meant every case file, role:staff's «community» every membership, its «forum» the whole governance
   module — while the policies judge per row, per role, per state. Django's `ModelAdmin.get_queryset` returns every
   row and its `has_*_permission` ignore the object, so nothing in the back office ever met a policy. No test
   compared the two: `test_13_the_list_and_the_object_check_agree` compares the platform's list with the platform's
   policy.
2. **Django offers an action declared without `permissions` to every account that opens the list**: a view grant
   resent mail, cancelled it, recorded the withdrawal of a consent, requeued an outbound event.
3. **A ModelAdmin shows and edits every field by default**: the purpose and pathway the orientation writes, a
   checklist line's status (written without the domain's event) and responsible actor, a subscription's bearer
   tokens and its evidence, a questionnaire's answers.
4. **The second-factor perimeter is a path rule**, and the public views decide inside themselves that an account acts
   as staff — no path tells the middleware.
5. **The API trusted** `str.isdigit` (it accepts «²»), `json.loads` (`RecursionError` is not a `ValueError`),
   `hmac.compare_digest` on a `str` (it raises on non-ASCII) and wrote header and payload values to PostgreSQL text
   and jsonb, which refuse a NUL.

## 3. The fix

### 3.1 The rule — the back office asks the platform; the grants are left as they are

**Decision.** A back-office screen needs the model permission AND the platform's own rule:
`core.admin_base.PolicyBoundAdminMixin` reads the rows through the domain's `readable_by` (lists, counts, searches,
filters, autocompletes, object pages, history and delete pages all read from the screen's queryset, so a row the
account may not read is answered as an id never issued), asks `can(user, action, obj)` on each object's page
(`object_policy`), and opens the screen only to the roles the policy names (`policy_roles`). Each condition is
necessary, so nobody gains anything; a superuser passes every gate, as it passes every policy (PERMISSION_MODEL §3.4).
Checked beside the screens: Django's autocomplete answers from the target screen's queryset (held by a test); unfold's
model search is off (`UNFOLD` declares no `COMMAND.search_models`) and would read the same querysets
(`UnfoldAdminSite._search_models` calls `get_queryset`), over the permission-filtered app list.

**Why the policies, not narrower grants** (the brief let me choose; sec-f7 declined the grants for the same reason).
(1) One answer by construction: when a policy changes — the owner deciding, for instance, that the operator handles
public submissions — the back office follows without a second edit. (2) Robust to a stale grant: a production group
keeps its permissions until the next `seed_all` re-runs `ensure_roles`. (3) `ROLE_PERMISSIONS` is sec-f5's area and
PERMISSION_MODEL §2.1's documented table; it is untouched. The grants that are now inert in the back office are listed
for the owner (Q-2): keep them for a future policy, or remove them in a later clean-up. Where no platform policy exists
(the outbox, consents, the audit trail), the rule is the document that governs the data (§3.2).

### 3.2 Screen by screen

| Screen | Before | After | Commit · tests |
|---|---|---|---|
| `CaseFileAdmin` | operator: every file; `purpose`, `pathway_key` editable on any file | `readable_by` (own, LIVE assignments, administration); `can` per object (a CLOSED file opens read-only); `purpose` and `pathway_key` read-only (`cases.intake` writes them) | `fe1e595` · `apps/cases/tests/test_backoffice_follows_the_policy.py` |
| ↳ `ChecklistInline` | lines of every file editable, CLOSED included; status without event; responsible actor rewritable | editable only where `can(user, "change", file)`, never on a CLOSED file (a superuser included), never by the file's own owner; status through `services.set_checklist_status` (one `case.checklist.status` per line that moved, each line judged by `checklist_policy` first; a new line made PENDING then moved by the domain); responsible actor disabled once the line exists | idem |
| ↳ `AssignmentInline`, `CaseAssignmentAdmin` | every assignment | `cases.policies.readable_assignments` (the assignee, the file's owner, the administration) — `assignment_policy`'s «view» as a queryset | idem; two sec-f7 tests retargeted (§9) |
| `PathwayAssessmentAdmin` (and the assessment inline, through its file) | every assessment, the answers with it | the assessments of a readable file; `can` per object | idem |
| `cases.policies` | the administrator changed a CLOSED file and its lines | «change» refused on a CLOSED file for the administrator too; «delete» kept (§3.6) | idem |
| `HelpdeskTicketAdmin` | operator: every request's shape and its file | `TicketQuerySet.readable_by` — the operator dispatches on the platform's register (`/espace-reserve/guichet/designation/`, the question deferred) | `6b62891` · `tests/backoffice/test_screens_follow_the_policies.py` |
| Public submissions (3 screens) | operator: read, change, export, anonymise; administrator: hard delete | `policy_roles` = `enquiries.policies.BACKOFFICE_VIEW_ROLES` (staff, administration); `can` per object; deletion refused but for a superuser; the writing actions need «change» | idem |
| Virtual forum (9 screens) | staff moderated and read every membership, hidden post, report | `policy_roles` = `community.policies.MODERATOR_ROLES`; trusting a member recorded (`community.membership.trusted`) | idem |
| Forum governance (8 screens and their inlines) | staff read profiles, proposals, mandates; granted mandates | `policy_roles` = `governance_policies.BACKOFFICE_VIEW_ROLES` (the administrator); staff keeps the public Forum's screens (registrations, programme, media…) | idem |
| Notifications (3 screens) | operator read every message; view grants read bodies (a newsletter's bearer link included) and resent/cancelled | `policy_roles` = `portal.policies.BACKOFFICE_VIEW_ROLES` (staff, administration); the bodies only with «change» (the administration); resend/cancel need «change» and are recorded (`notifications.outbox.resent` / `.cancelled`) | idem |
| `ConsentRecordAdmin`, `NewsletterSubscriptionAdmin` | staff (view) withdrew consents; tokens shown; the subscriber's e-mail and language editable | withdrawal needs «change», recorded (`consents.withdrawn`); the two tokens never displayed; the subscription read-only | idem |
| `AuditEventAdmin` | legal approver: every event | the administration reads all; any other account the rules' trail (`target_type` LegalRule / LegalSource, as `record` and the admin's log name them) | idem |
| Orientation sessions and results | the administrator read every questionnaire's answers | `state` and `answers_snapshot` shown to a superuser only; the shape, the anonymisation on request and the statistics stay | idem |
| `OutboundEventAdmin` | the administrator (view) requeued and cancelled | requeue/cancel need «change», recorded (`integrations.outbound.requeued` / `.cancelled`) | idem |
| `PrivateDocumentAdmin`, `DocumentRequirementAdmin` | the administrator listed deleted documents' metadata; the register's export unrecorded | the rows `documents.policies` lets the account read (no deleted document but for a superuser), `can` per object; the export recorded (`documents.exported`) | idem |

### 3.3 The second-factor perimeter (`3123b09`)

`accounts.middleware.require_second_factor(request)`: a branch of a public view that decides «this account acts as
staff» calls it before it acts; a session that owes the factor (`services.second_factor_due`: enrol when the
deployment requires it, present the device the account holds) leaves through `SecondFactorRequired`, which
`BackofficeMFAMiddleware.process_exception` answers with the perimeters' own redirects (the activation page, or
allauth's MFA re-authentication with `next` = the page asked for). sec-f5's two rules, its pages and its exemptions
are unchanged; the policy keys on the privilege exercised, not on the path. Applied where the privilege is decided:

- the virtual forum's moderators — `community.views.member_required` and `index` (every room, hidden and pending
  posts, the moderation POSTs);
- every staff preview of unpublished content — `ecosystem.services.can_preview`, `pathways.services.can_preview`,
  `pages.services.can_preview` (`?preview=1`), `faq.services.page_visible` and `glossary.services.page_visible` (any
  staff account while Phase 3 is closed), `living.views._check_gate` (`?preview=1` + `living.view_livingtopic`),
  `news.views.detail` (an unpublished article, `news.view_article`).

`test_every_staff_branch_of_a_public_view_asks_for_the_second_factor` reads every module of `apps/` holding an
`is_staff`, `has_perm(` or `is_moderator(` test outside the admin, the policies and the reserved area's modules (each
exemption named with its reason): a future preview or moderator branch that forgets the rule fails there, named.

### 3.4 The integrations API (`e1d01cc`)

`integrations.api.decode_json` — `None` for invalid UTF-8 or JSON, for `RecursionError`, and for a NUL anywhere
(`carries_nul`: strings and object keys, every depth) — feeds the webhook (the same 400 «invalid_json» as a malformed
body, which consumes no nonce) and `parse_json_body` (`ApiError` 400). The refusal's log row writes `X-Nonce` and
`X-Timestamp` without a NUL (`_logged`). `webhooks.verify`: the timestamp ASCII digits, at most 12; the nonce matched
whole, ASCII; the signature compared only when ASCII («invalid_signature» otherwise). `events_list`: integer
parameters ASCII and bounded (`-?[0-9]{1,20}`), an impossible date a 400. Raw NUL bytes were already refused by the
decoder (strict mode) — held by the tests.

### 3.5 What the domain writes, CLOSED, and the checklist's trail

Read-only in the back office because the domain writes them: a file's owner, status and its trace, the suspension's
reason (sec-f7), purpose and pathway (`cases.intake`), a checklist line's responsible actor once made, an assignment's
capacity (sec-f7), an assessment (frozen), a selection's stage and outcome, a need's status, a submission's data, a
consent and a subscription, the audit trail. A CLOSED file is read-only for everybody (§4 rule 5): the inline renders
read-only even for a superuser, and `case_policy` / `checklist_policy` refuse the administrator «change». A line's
status leaves a `case.checklist.status` event naming the account, the line, from and to — as the platform's own
`set_item_status` does.

### 3.6 Deliberate exceptions, and what did not change

- **Deleting a CLOSED file stays the administrator's** in the policy (a deletion is how retention ends a file, not a
  change of it). In the back office no role holds `cases.delete_*`: a superuser deletes.
- **A superuser stays the last resort**: every screen, the answers, deleted documents' metadata, a submission's hard
  delete. CLOSED is the one rule it meets in the back office too.
- **The administrator role gains no case screen**: it holds no «cases» model permission (unchanged); it reads case
  files on the platform. Nobody was widened anywhere.
- Not changed: the portal's message screens (`RoleScopedAdmin` already follows `portal.policies`), forum
  registrations (follow `forum.permissions`), the document requirements' rights (the administrator views), accounts
  (§6 Q-1), selection, companies and Academy (no role holds them: a superuser's), the rule editor, the editorial
  apps. No template, stylesheet or script changed (W4-A's and W4-B's files untouched); no migration.

## 4. Every path checked — the owner's V5.10 list

| Item | DENY (each failing before the fix where it reproduces one) | ALLOW (still possible) |
|---|---|---|
| CASE FILES — assigned/scoped access | an unassigned file not listed, not found by reference or owner's e-mail, not in the `case` autocomplete; a revoked or expired assignment reads nothing; every assignment and assessment of an unrelated file invisible | the operator lists, searches and opens its own file (a LIVE OPERATOR assignment) |
| CASE FILES — no enumeration | the change, history and delete pages of an unrelated file answer exactly as a never-issued id; the list's count holds the readable rows only | — |
| CASE FILES — view/change/delete | the operator deletes no file, its own included (403, no `delete_selected`); changes nothing on its file once CLOSED (403); purpose/pathway not rewritable (superuser included); a responsible actor not rewritable; an owner does not act on its own file there | the operator changes a line's status (recorded) and due date on its active file; a superuser reads every file |
| DOCUMENTS | operator, staff, moderator, content editor, legal editor, legal approver: 403 on both document screens and on a document's page; the administrator sees no file link and no deleted document; an unscanned file is refused even to a superuser by `_serve` (403) | the administrator reads metadata; a superuser's link (clean file only) is `documents:download` → `_serve`, served `private, no-store`, recorded `documents.downloaded` |
| ACCOUNTS / PERSON DATA | the six roles above: 403 on users, person profiles, organisations, e-mail addresses, authenticators, groups; the administrator: 403 on e-mail addresses, authenticators, groups; staff: no virtual-forum membership, no governance profile, no mail body, no subscription token; the operator: no notification, no public submission | the administrator reads and changes accounts (L-01's guards kept); staff keeps what its policies name (submissions, forum registrations, the team's messages, consents' view) |
| REQUESTS / HELPDESK / SELECTION | the operator: no request in the back office, no public submission (list, page, four actions); the administrator: no hard delete; every role but a superuser — the administrator included — 403 on selection processes, mandates, disclosures, authorised actors, company needs and profiles, enrolments, training plans | the operator designates on the platform's register (the question not shown); staff marks a submission handled; the administrator exports and anonymises; a superuser reaches the superuser-only screens |
| ADMIN — closed case, sensitive operations | lines of a CLOSED file read-only for a superuser; `can(administrator, "change", closed file / line)` False; view grants: no resend, cancel, withdrawal, requeue (not offered, not executed); staff grants itself no mandate; no submission hard-deleted; tokens never displayed; subscription evidence not rewritable; answers not shown to the administrator | the administrator changes an active file's lines (policy), deletes a closed file (policy), resends mail, records a withdrawal, anonymises a questionnaire on request; a superuser requeues |
| AUDIT | the legal approver reads no case or sign-in event (list, page, search); other roles 403 on the trail | `case.checklist.status` (who, line, from, to); `consents.withdrawn`, `notifications.outbox.resent`, `integrations.outbound.requeued`, `community.membership.trusted`, `documents.exported` written with the acting account; existing records (enquiries' exports, forum, orientation, scans, assignments, the admin's LogEntry mirror) kept; the administration reads the whole trail |
| 2FA | a staff session that owes the factor is sent to present it before six previews and an unpublished article; a moderator before the forum's index and a discussion, and its moderation POST is not executed; ENROL sends to the activation page; the source guard | a session that presented its factor previews and moderates; no device and no enforcement: nothing owed; a visitor and a member untouched; a published page owes nothing |
| INTEGRATIONS API | escaped NUL in four places of a signed body → 400, nothing stored, nonce not consumed; raw NUL in four places → 400; NUL in X-Nonce / X-Timestamp → 401, logged without it; five malformed timestamps → 401; three non-ASCII signatures → 401; a body nested 100 000 deep → 400; seven impossible parameters → 400; NUL in the query → the project's 400; NUL body on the acknowledgement → 404; `parse_json_body` refuses four bodies; no ERROR line, no traceback | a clean signed body accepted (202) and logged; plain parameters answered (200); `parse_json_body` reads an object |

## 5. Reproduced first

Each new test was written before the code it holds and run against the code before the fix; the logs are in
`.work/sec-f8/`: `repro_cases_before_fix.txt` (15 failed, 5 passed — the five are the legitimate-work tests),
`repro_screens_before_fix.txt` (23 failed, 35 passed — the passing ones are ALLOW tests and DENY tests of rules
that already held: documents, accounts, the superuser-only screens), and `before_fix_all_new_tests.txt`: every new
module, copied into a throwaway worktree of design-v5 `5bf2f90` (removed afterwards) — **73 failed, 59 passed of 132**.
Every failure is a reproduction — a DENY rule that did not hold, or an audit record that was not written; the 59 that
passed are the ALLOW tests and the DENY rules that already held (accounts, the documents' roles and the download, the
superuser-only screens, the audit trail's other roles, the operator's deletion, the raw NUL bytes). The API's answers on
that base (`before_fix_api_statuses.txt`): a 500 for every vector but two — a NUL in a key the log drops (accepted, 202)
and an Arabic-Indic timestamp (401 under another code).

## 6. Questions for the owner

- **Q-1 — the administrator and accounts (PERMISSION_MODEL §5.10).** The matrix says the administrator changes «all
  **tranne** `is_superuser`, `is_staff`, `groups`»; L-01's closure hides and refuses `is_superuser` and the protected
  groups only, so the administrator still makes staff accounts (the `is_staff` flag, every non-protected role) and
  sets the password of any non-superuser account. Confirm (and §5.10 says so) or narrow (only a superuser makes staff
  accounts). Unchanged here: it is how staff accounts are made, and sec-f5's area.
- **Q-2 — grants now inert in the back office.** role:operator's «enquiries», «notifications» and «helpdesk» (its
  help-desk list is empty: it dispatches on the platform); role:staff's «community» and the governance half of
  «forum». Either the policies gain these roles (should the operator handle public submissions, as L-03 planned? should
  staff moderate the virtual forum?), or `ROLE_PERMISSIONS` loses the grants in a later clean-up.
- **Q-3 — deleted documents.** Their metadata (owner, file name) is now a superuser's only (the policy refuses a
  deleted document to everybody). Should the administrator supervise retention there?
- **Q-4 — a line's responsible actor** is now set once. If the team must hand a line to another actor, a domain
  service with its audit event is the way; none exists.
- **Q-5 — the administrator role and the case screens.** It holds no «cases» model permission: it reads files on the
  platform, and only a superuser grants or ends an assignment in the back office (sec-f7's observation). Granting the
  administrator the case screens would be a widening of the back office within its policy — not done.
- **Q-6 — mail bodies** are hidden from role:staff (a view grant): staff reads the team's messages in their own
  screen; the bodies also carry a newsletter's bearer link. Confirm.
- **Q-7 — notification preferences**: the administrator may change a person's e-mail switches in the back office (no
  policy governs them). Keep, or make the screen read-only?
- **Q-8 — an assignment on a CLOSED file**: `services.assign` does not refuse one (unchanged). It changes who reads the
  file, not the file (§4 rule 5); confirm.
- **Q-9 — role:staff and consents**: it reads every consent record (e-mail, purpose, dates) — §5.11's status note
  names the grant, its matrix does not name staff. Confirm or remove.

## 7. Words — none invented

No msgid added, changed or removed in any catalogue (fr, ar, it, en). The second-factor redirects use sec-f5's existing
messages; the API's refusals reuse its existing English messages («Request body is not a JSON object.», «Request body
is not valid JSON.», «Parameter … must be an integer.», «Parameter 'since' must be an ISO-8601 date-time.», «Webhook
rejected.»); the new audit actions are identifiers, never shown. **Missing words for copy packet B1: none.**

## 8. Tests and runs

New: 132 tests in four modules — `apps/cases/tests/test_backoffice_follows_the_policy.py` (23),
`tests/backoffice/test_screens_follow_the_policies.py` (58),
`apps/accounts/tests/test_second_factor_wherever_the_privilege_lives.py` (16),
`apps/integrations/tests/test_unexpected_input.py` (35); two of sec-f7's tests retargeted (§9). One pytest at a time on
`test_ile_v5_l7`, `-p no:randomly` (logs in `.work/sec-f8/`):

| Run | Result |
|---|---|
| `apps/cases`, after the case screens' fix (`fe1e595`) | 203 passed, 3 skipped (5 min 22 s; `suite_cases_1.txt`); the three skips are `test_intake.py`'s cases that need a legal rule in force (none is) |
| `tests/security/test_object_permissions.py`, `tests/security/test_authorization_audit.py`, `tests/backoffice` | 88 passed (3 min 21 s) — `test_13`, the list and the object check agreeing, holds with the CLOSED branch |
| `tests/backoffice/test_screens_follow_the_policies.py`, after the screens' fix | 58 passed |
| `apps/{enquiries,community,forum,notifications,orientation,integrations,documents,helpdesk,audit,consents}`, `apps/portal/tests/{test_admin_cascade,test_security}.py`, `-m "not browser"` | 875 passed (5 min 35 s; `suite_apps_screens_1.txt`) |
| the perimeter's module, sec-f5's `test_backoffice_second_factor.py`, `test_mfa_middleware.py`, `test_identity_gaps.py`, `apps/{news,living,faq,glossary,ecosystem,pathways,pages,community}`, `-m "not browser"` | 955 passed, 47 deselected (19 min 17 s; `suite_perimeter_1.txt`) |
| `apps/integrations`, `tests/deployment/test_nul_bytes.py` | 103 passed |
| every new module on design-v5 `5bf2f90`, before the fix | 73 failed, 59 passed (§5; `before_fix_all_new_tests.txt`, `before_fix_api_statuses.txt`) |
| **Final**, on the branch's code (`e1d01cc`; `668ca70` after it changes documents only): `apps/{accounts,cases,documents,selection,audit,forum,integrations,news,living,faq,glossary,ecosystem,pathways,pages,community,helpdesk,enquiries,notifications,consents,orientation,portal}`, `tests/backoffice`, `tests/security`, `tests/deployment`, `tests/frontend/test_design_docs.py`, `tests/test_check_ownership.py`, `tests/test_migration_drift.py`, `tests/test_phase_console.py`, `-m "not browser"` — the brief's list and every app whose screens or views changed | **2 765 passed, 3 skipped, 55 deselected** (the browser tests) in 47 min 55 s (`final_regression.log`); the skips are `test_intake.py`'s, as above |
| `tests/frontend/test_content_pages_w3_f2.py` (it reads the virtual forum's public page), `-m "not browser"` | 50 passed |
| `manage.py check` · `makemigrations --check --dry-run` · `ruff check .` (on `ile_v5_l7`) | no issue · «No changes detected» · clean; `ruff format --check` clean on every file this lane formats (`apps/forum/governance_admin.py` was not formatted before and is left as it was, its imports sorted) |

Not run, on purpose: the full suite (the brief: never; the steward's merge regression and CI are the full runs) and
the browser suites — no template, stylesheet or script changed, and every behaviour changed is a server answer the
client tests above read.

## 9. Hand-over

- **Paths touched** (no template, stylesheet, script or migration; W4-A's and W4-B's files untouched):
  `apps/core/admin_base.py` (the mixin), `apps/cases/{admin,policies}.py`, `apps/{helpdesk,enquiries,community,
  notifications,consents,audit,orientation,integrations,documents}/admin.py`, `apps/forum/governance_admin.py`,
  `apps/accounts/middleware.py`, `apps/community/views.py`, `apps/{ecosystem,pathways,pages,faq,glossary}/services.py`,
  `apps/{living,news}/views.py`, `apps/integrations/{api,views,webhooks}.py`; tests:
  `apps/cases/tests/test_backoffice_follows_the_policy.py`, `tests/backoffice/test_screens_follow_the_policies.py`,
  `apps/accounts/tests/test_second_factor_wherever_the_privilege_lives.py`,
  `apps/integrations/tests/test_unexpected_input.py` (new), `apps/cases/tests/test_transition_actors.py` (two tests
  retargeted); docs: `docs/security/PERMISSION_MODEL.md` (§3.5, one paragraph), `docs/security/AUDIT_MODEL.md` (§6.1,
  one row: the legal approver), these notes.
- **For the steward (at the merge).** The family «sec-f8» goes in the manifest outside the waves, as sec-f5 and
  sec-f7 (`tests/test_check_ownership.py::OUTSIDE_THE_WAVES`). Read against `OWNERSHIP_V54.json` at `5bf2f90`, the
  paths other families hold, and what this lane wrote in each (every slice outside theirs):
  - `apps/accounts/middleware.py` (sec-f5's slice, its rules): a docstring paragraph, `SecondFactorRequired`,
    `require_second_factor`, `BackofficeMFAMiddleware.process_exception`;
  - `apps/accounts/tests/**` (W2-B's glob, «the allauth flows' tests»): the new
    `test_second_factor_wherever_the_privilege_lives.py`, to assign to sec-f8 whole;
  - `apps/cases/admin.py` (sec-f7's slice, the screens hand out no capacity): the module docstring's F-8 paragraph,
    `readable_files`, `ChecklistLineForm`, `ChecklistInline`'s rules, the mixin on the three screens, `readable`,
    `save_formset` / `save_checklist`, `purpose` / `pathway_key` read-only, `CaseAssignmentAdmin.readable` and its
    simplified `has_change_permission` (the same rule, the policy now asked by the mixin);
  - `apps/cases/tests/test_transition_actors.py` (sec-f7's, W3-E's slice untouched): the two retargeted tests of
    `TestTheBackOffice` (`test_the_operator_cannot_take_over_another_files_assignment_and_move_that_file`,
    `test_the_operator_ends_no_assignment_there`) — another file's assignment is not found there any more (302 to the
    index, as an id never issued) where it answered 403; the intent kept, and the second now also proves that the
    operator reads its OWN assignment's screen and still changes nothing on it;
  - `apps/pages/services.py` (W2-D's and W2-E's slices, the home page) and `apps/pathways/services.py` (W3-F1's slice,
    the presentation): `can_preview` only;
  - `docs/security/PERMISSION_MODEL.md` (sec-f5's slice, three passages): the new §3.5.
  No family holds the other paths (`apps/core/admin_base.py`, `apps/cases/policies.py`, the nine `admin.py`, the
  governance admin, the content apps' preview functions, `apps/community/views.py`, the API's three files,
  `docs/security/AUDIT_MODEL.md`, the three new test modules outside `apps/accounts/tests/`).
- **For the owner.** §6.

## 10. Review fixes (sec-f8-fix2, 16 October 2026)

The independent review (`REVIEW.md`, at `9c8dda4`: **SHIP_AFTER_FIXES**) found the headline defect fixed and holding,
and four MAJOR gaps inside the audit's own declared scope (V5.10: ACCOUNTS / PERSON DATA, ADMIN sensitive operations,
the INTEGRATIONS API). Each is fixed below with its tests; each DENY was run against the pre-fix code first and failed
there (`git stash` of the fix's source files, the new tests kept; logs in `.work/sec-f8/fix2/`). No access was widened,
no other security property weakened (sec-f5's second factor, sec-f7's «who may» table, `readable_by`, the audit events,
the rate limits, CSRF and CSP are untouched); no template, stylesheet, script or migration changed.

V5.10's list, completed by these fixes: **ADMIN — sensitive operations** (the legal rules' approval and entry into force:
F8R-1); **ACCOUNTS / PERSON DATA** (a hidden field read back through the list: F8R-2; other accounts' addresses on
editorial forms and filters: F8R-3); **INTEGRATIONS API** (unexpected input beyond the NUL: F8R-4). §4's other rows stand
as the review verified them.

| Finding | Root cause | Fix | Commit · tests (failing before / total) |
|---|---|---|---|
| **F8R-1** — a view-only administrator and a non-approver legal editor approved and put legal rules in force through the back office | the rule editor's workflow actions were declared without `permissions` (Django offers such an action to every account that opens the list) and called `rules.services.transition`, which checks only the four-eyes author rule — §3.6 had left `apps/rules/admin.py` out | each action is offered (Django's `permissions`) to an account that may change rules here AND holds the role its verb names in `rules.policies` (`submit`: a drafter; `approve`, `activate`, `retire`: role:legal_approver — `rules.policies.may_review`, a name for what the policy already said), and each selected rule is asked `can(user, verb, rule)` before the service, which keeps its own refusals; the rule and source screens are policy-bound (`PolicyBoundAdminMixin`, `object_policy`) | `3458d2b` · `apps/rules/tests/test_backoffice_follows_the_policy.py` (16 / 20) |
| **F8R-2** — fields the fix hid stayed readable through the changelist's query string | a changelist prints its count, and `ModelAdmin.lookup_allowed` allows any lookup over the model's own fields | `core.admin_base.BaseModelAdmin.hidden_fields(request)` names, per account, the fields a screen hides; a lookup over one is refused as Django refuses any lookup it does not allow (`DisallowedModelAdminLookup`: its 400, logged as a security event) and the search box never reads one — the subscription's two tokens (from everybody), the outbox's bodies (from a view grant), the questionnaire's answers (from all but a superuser) | `8bbaca1` · `tests/backoffice/test_a_hidden_field_is_no_filter.py` (8 / 14) |
| **F8R-3** — editorial forms listed every account's e-mail address to roles that may not read accounts | `User.__str__` is the address; a foreign key renders its choices from the whole user table; an autocomplete renders the label of whichever id its initial value names; Django's list filter over a foreign key lists every row of the related table | for an account that may not open the accounts screen (`core.admin_base.may_read_accounts` — the test Django's autocomplete asks of a target), every account field of a form or an inline is read-only (`frozen_account_fields`, in `BaseModelAdmin` and both inline bases): it shows the account the row already names and nothing else, and the workflow sets it; a list filter over an account lists only the accounts the screen's own rows name (`RelatedOnlyFieldListFilter`) | `d7ffd9e` · `tests/backoffice/test_forms_name_no_account.py` (27 / 35) |
| **F8R-4** — a signed webhook body with a lone UTF-16 surrogate was a 500 | `decode_json` refused a NUL only; the decoder keeps a lone surrogate, PostgreSQL refuses it in jsonb and psycopg cannot encode it for text | `integrations.api.UNSTORABLE` (the NUL and `\ud800`–`\udfff`): `carries_unstorable` refuses either anywhere in a body (the NUL's answer: a 400 «invalid_json» that consumes no nonce); a surrogate PAIR is one character and is accepted; a refusal's log row writes its headers through `api.storable` | `77a2876` · `apps/integrations/tests/test_unexpected_input.py` (9 / 11 new, 46 in the module) |

**Beyond the letter of the review — the same classes, found while fixing them, fixed and tested with them:**

- F8R-1's class. The legal approver could rewrite a rule's text, and a source's reference, in the back office before
  approving it (`rules.policies`: «change» is a drafter's) — the approver now reads the text it approves and changes
  none of it; the review state moves through the actions only. A view-only administrator could write a new version of
  any rule through the direct URL `…/legalrule/<pk>/new-version/` (the view asked the policy alone, which lets a
  drafter — the administrator is one — open a version): a new version is a new row and now needs «add» besides the
  policy. The diff and the preview pages asked the policy alone too (role:staff, a policy reader without the rule
  screens, reached them by URL): they now ask the screen's own view test.
- F8R-3's class. A moderator could hand a forum membership to another account (the membership form's `user`, an
  autocomplete that accepts any id on POST) — reproduced, now read-only; a crafted POST named any account as an
  editorial row's author or reviewer, and the page then printed its address — now impossible for these roles; the news
  list's «dernier éditeur» filter listed every account — now only the editors of the list's own rows. The review's
  inventory also showed `enquiries` `handled_by` (role:staff) and `cases.CaseAssignment` `assignee` (role:operator, an
  override that did not call `super()` — routed through `with_frozen_account_fields`): both read-only for them now (the
  first is set by «mark handled», the second only by a superuser granting an assignment). A registry-wide test holds
  that no add or change form, nor any inline, offers a role that may not read accounts a choice among accounts.
- F8R-2's class. `?password__startswith=` on the accounts list would be the same oracle over password hashes for the
  administrator — Django's own `UserAdmin.lookup_allowed` already refuses every `password` lookup; held by a test.
- F8R-4's class. A WSGI server hands headers over as Latin-1, so no surrogate reaches `X-Nonce` / `X-Timestamp` that
  way; the test client can, and the refusal's log row is written without it all the same.

**What the workflow does now (the team's decision, stated for the owner):** role:staff and role:content_editor no longer
pick an editorial row's author or reviewer by hand — the author is the account that creates the row
(`PublishableAdminMixin`, unchanged), the reviewer the account that runs the review action (a «Vivre en Italie» sheet:
«Marquer comme revue juridiquement (réviseur = vous, date = maintenant)»; a news article: its publication, whose
publisher is its reviewer, as before). A portal notice's reviewer — which no logic reads — is set by the administration
only; a translation's `reviewed_by` was already out of these roles' reach (the account autocomplete answers them 403).
The administration, which reads accounts, still chooses all of them. The legal approver changes no rule or source field
in the back office.

**Words.** No msgid added, changed or removed. The rule editor's refusals reuse two existing msgids: «Permesso negato.»
(`legal/admin.py`'s, translated in fr, ar, it, en) and «L'autore di una regola non può approvarla.» (the service's own).
**Missing words for copy packet B1: none.**

**Runs** (lane 7, `test_ile_v5_l7`, one pytest at a time, `-p no:randomly`; logs in `.work/sec-f8/fix2/`):

| Run | Result |
|---|---|
| each new module on the pre-fix code (`git stash` of the fix's source files, the tests kept) | F8R-1 16 failed of 20 · F8R-2 8 of 14 · F8R-3 27 of 35 · F8R-4 9 of the 11 new — every failure a reproduction; what passed is an ALLOW test or a rule that already held (Django's own `password` and cross-relation guards, the autocomplete add pages without an initial value, the legal roles' forms, the four-eyes refusal of the service) |
| `apps/rules`, after F8R-1 | 120 passed |
| `tests/backoffice`, `apps/{consents,notifications,orientation}`, after F8R-2 | 283 passed |
| `apps/{cms,news,living,faq,glossary,forum,partners,pathways,portal,community,enquiries,cases,rules}`, `tests/backoffice`, `tests/security`, `-m "not browser"`, after F8R-3 | 1 491 passed, 3 skipped, 8 deselected (23 min 13 s; `suite_f8r3_1.txt`); the skips are `test_intake.py`'s, as in §8 |
| `apps/integrations`, `tests/deployment/test_nul_bytes.py`, after F8R-4 | 114 passed |
| the review's own suite — a copy of the reviewer's modules in `.work/sec-f8/fix2/review_copy/` (its inventory test writes beside itself; the reviewer's folder is untouched) | **71 passed** (at `9c8dda4`: 49 passed, 22 failed — the four findings' DENY tests); the regenerated inventory lists an editable account field for no role but the administrator and the superuser (`review_suite_after_fix.txt`) |
| `apps/{accounts,documents,selection,audit,ecosystem,pages,helpdesk,companies,academy,legal,core}`, `tests/deployment`, `tests/frontend/test_design_docs.py`, `tests/test_check_ownership.py`, `tests/test_migration_drift.py`, `tests/test_phase_console.py`, `tests/compliance/test_public_pages.py`, `-m "not browser"` — the rest of §8's final list and every other app whose screens inherit the changed base class | 1 404 passed, 47 deselected (the browser tests) in 23 min 56 s (`suite_rest_1.txt`) |
| `manage.py check` · `makemigrations --check --dry-run` · `ruff check .` | no issue · «No changes detected» · clean (on `ile_v5_l7`) |

Not run, on purpose, as in §8: the full suite and the browser suites (no template, stylesheet or script changed).

**Hand-over additions for the steward.** Paths written by this pass: `apps/rules/{admin,policies}.py`,
`apps/core/admin_base.py`, `apps/{consents,notifications,orientation}/admin.py`, `apps/integrations/{api,views}.py`,
`apps/cases/admin.py` (sec-f7's slice: `CaseAssignmentAdmin.get_readonly_fields` routes its result through
`with_frozen_account_fields` — a few lines and an import), `docs/security/PERMISSION_MODEL.md` (§3.5, sec-f8's own: one
paragraph), these notes; new tests, to assign to the family «sec-f8» whole:
`apps/rules/tests/test_backoffice_follows_the_policy.py`, `tests/backoffice/test_a_hidden_field_is_no_filter.py`,
`tests/backoffice/test_forms_name_no_account.py`; `apps/integrations/tests/test_unexpected_input.py` (sec-f8's own)
extended. No family holds `apps/rules/**` or the other paths at `5bf2f90`. The owner's questions Q-1…Q-9 (§6) stand
unchanged; the four fixes apply the policies as written and raise no new question.

## 11. At the merge (the steward, 16 October 2026)

The steward's merge step (`sec-f8-merge`, under `C:/tmp/ile_locks/DESIGN_V5_MERGE_LOCK`, taken at 12:47:16) on lane 7:
`TEST_DATABASE_URL=…/ile_v5_l7`, one pytest at a time, `-p no:randomly`, every heavy step gated on
`PERFORMANCE_BENCHMARK_LOCK`; no server started, no persona used, no password typed. Nothing deployed, nothing pushed,
nothing on main, no production touched. Logs: `C:/tmp/ile_v5_council/evidence/v54/sec-f8/merge/`.

- **The sync** (`04a31b2`). design-v5 had moved from `5bf2f90` to `fad36e0`: 49 commits — the W4-B merge (the motion
  audit: the Motion library out of the product), its records DL54-153 and DL54-154, the changelog line and its note;
  the W4-D part 1 merge (CI on the production target, the release named in the deployment documents) and its record
  DL54-155. `git merge --no-ff design-v5`: no conflict and no path in common. The sync brought static sources and
  bundles (one sheet under `apps/portal/static`), `templates/base.html`, the build script and the package files,
  `tests/frontend` and one compliance test, CI, the deployment documents, `tests/deployment`, the README, the release
  notes and the decision log — and no Python module of `apps/`; this branch holds the back office's screens, the
  policies, the public staff branches, the API and their tests.
- **The bundles.** No static source, script, template or package file differs between the merged branch and
  design-v5. Both dist trees were deleted and rebuilt from clean all the same (`npm run build`, `node_modules` a
  junction to design-v5's, removed afterwards): the 39 files byte for byte the committed ones, the chunk names
  included. The merge brings no bundle; nothing is rebuilt on design-v5. **The weight (V5.8)**: the family changes no
  stylesheet — `main.css` 31 799 B on every page and the console page types 39 978 B, as DL54-154 left them.
- **Ownership** (`74bb365`). The family «sec-f8» is registered in `docs/design-v5/OWNERSHIP_V54.json` outside the waves
  (wave 0, as devops, sec-f5, intfix and sec-f7; DL54-01's branch and worktree; no merge tag): 38 entries, each with its
  reason — 8 whole (the seven test modules the fix and its review fixes created; these reports) and 30 slices: the 24
  files no family held, and six files of five families (sec-f5's middleware and PERMISSION_MODEL.md, sec-f7's case
  screens and its test module, W2-D's and W2-E's `pages/services.py`, W3-F1's `pathways/services.py`).
  `tests/test_check_ownership.py` names it among the families outside the waves (the checker has accepted `sec-f<n>`
  since the sec-f5 merge). `check_ownership.py sec-f8 design-v5` before that commit: **39 paths, 9 inside, 30 slice →
  PASS**; after it the steward's two paths join the list (the manifest, steward-only; the checker's test, the steward
  family's), as at the sec-f5 and sec-f7 merges. `--validate`: **30 families, 783 entries**.
- **The slices, read.** Each of the 30 was read in `git diff design-v5...HEAD` and stays inside what its entry names.
  In the other families' files: sec-f5's middleware gains an exception, its raiser and `process_exception` (the policy's
  two rules, its pages and its exemptions unchanged); sec-f7's case screens gain the policy-bound mixin, the checklist's
  domain save and the read-only purpose and pathway beside sec-f7's capacities, which stand; sec-f7's module has two
  tests retargeted, their intent kept; `pages/services.py` and `pathways/services.py` change `can_preview` only;
  PERMISSION_MODEL.md gains §3.5. No template, stylesheet, script, migration or catalogue word.
- **Scan** (`scan_added_lines.log`). The merge's 4 034 added lines in 41 files (the family's 39, the manifest and the
  checker's test): no IPv4 address, no server or droplet name, no live domain; e-mail addresses `example.test` only; two
  URLs, the test client's own host (`https://testserver/…`) and `https://www.normattiva.it/`, the public legislation
  site other tests already cite as a rule's source; the credential-like lines are the tests' test-only passwords
  (`Local-Only-F8…-2026!`), the webhook tests' shared secret and a made-up bearer token; no private key; no CR, no NUL;
  `git diff --check` clean.
- **Tests on the merged branch** (`74bb365`), one pytest at a time, each gated on the benchmark lock (run B waited
  505 s while W4-C measured):
  - **Run A — the merge brief's list: 2 243 passed, 3 skipped** in 39 min 48 s (`-m "not browser"`, 47 browser tests
    deselected; `run_A.log`): `apps/accounts` 205 (this family's second-factor module and sec-f5's among them),
    `apps/cases` 206 (F-8's 23 and sec-f7's two retargeted tests among them), `apps/documents` 147, `apps/selection`
    86, `apps/audit` 8, `apps/forum` 213, `apps/integrations` 91 (`test_unexpected_input.py`'s 46 among them), the
    content apps — `apps/cms` 45, `apps/news` 68, `apps/living` 33, `apps/faq` 41, `apps/glossary` 52,
    `apps/ecosystem` 159, `apps/pathways` 98, `apps/pages` 319 —, `tests/backoffice` 112, `tests/security` 157 (the
    confidential-material guard with its private table), `tests/deployment` 99, `tests/frontend/test_design_docs.py`
    40, `tests/test_check_ownership.py` 57 and both bundle-currency tests 10. The three skips are
    `apps/cases/tests/test_intake.py`'s cases that need a legal rule in force (none is).
  - **Run B — every other app the fix reached: 1 018 passed** in 12 min 7 s (`-m "not browser"`, 8 deselected;
    `run_B.log`): `apps/rules` 120 (F8R-1's 20 among them), `apps/community` 48, `apps/helpdesk` 94, `apps/enquiries`
    72, `apps/notifications` 95, `apps/orientation` 111, `apps/portal` 216, `apps/companies` 99, `apps/academy` 81 and
    `apps/partners` 13 (their screens inherit the changed base class), `tests/test_migration_drift.py` 2,
    `tests/test_phase_console.py` 8, `tests/compliance/test_public_pages.py` 9 and
    `tests/frontend/test_content_pages_w3_f2.py` 50 (the virtual forum's public page). `apps/consents`, `apps/core` and
    `apps/legal` hold no test module of their own; their back office is tested in `tests/backoffice`.
  - **In Chromium**, the 55 browser tests of these suites (the ecosystem's pages, the home page and the person's
    dashboard — W4-B's scripts and `base.html` beside this branch's server for the first time on a committed tree):
    **55 passed** in 6 min 51 s (`run_browser.log`).
- **Checks.** `manage.py check`: no issue; `makemigrations --check --dry-run`: «No changes detected» (both on
  `ile_v5_l7`); `ruff check .`: clean on the whole merged tree (CI's own lint); `ruff format --check` on the merge's 36
  Python files (the family's 35 and the checker's test): 34 formatted — `apps/forum/governance_admin.py` and
  `apps/rules/admin.py` were unformatted on design-v5 before the fix and are left as they were (CI lints, it does not
  format).

**V5.10's list, on the merged branch.** Every item has its DENY tests and its ALLOW tests on the merged tree, and every
one passed in the runs above. The seven modules the fix created hold 212 tests; §5 and §10 give how many failed on the
code before their fix — 73 of the first 132, 60 of the review fixes' 80 —, every failure a reproduction. The DENY
tests assert what was not disclosed and what did not change — a reference, an address or a synthetic answer absent from
the page, a row count of zero, a never-issued id's exact answer, the stored row unchanged, no audit event — not a status
code alone.

| V5.10 item | DENY | ALLOW |
|---|---|---|
| CASE FILES — assigned and scoped access | `test_an_unassigned_file_does_not_open`, `test_the_list_holds_its_assigned_file_and_not_another`, `test_an_assignment_that_has_ended_reads_nothing_there`, `test_an_expired_authorisation_reads_nothing_there`, `test_it_reads_its_own_assignment_and_no_other`, `test_it_reads_no_assessment_of_a_file_it_may_not_read`; sec-f7's two retargeted `TestTheBackOffice` tests | `test_the_operator_opens_and_works_on_its_assigned_file`, `test_a_superuser_reads_every_file`; `test_the_administrator_role_gains_no_case_screen` (nobody widened) |
| CASE FILES — no enumeration | `test_a_search_does_not_find_an_unassigned_file`, `test_the_autocomplete_enumerates_no_file`, `test_every_page_of_an_unassigned_file_answers_as_an_id_never_issued`, `test_the_lists_count_only_readable_rows` | the search still finds the operator's own file (in the first) |
| CASE FILES — view / change / delete | `test_the_operator_deletes_no_file_not_even_its_own`, `test_the_operator_changes_nothing_on_its_own_file_once_closed`, `test_the_purpose_and_the_pathway_are_the_domains`, `test_who_is_responsible_for_a_line_is_not_rewritten_there`, `test_an_operator_who_owns_a_file_does_not_act_on_it_there` | `test_a_lines_status_changed_there_is_recorded_by_the_domain`, `test_a_lines_other_fields_still_save_and_an_unchanged_status_records_nothing` |
| DOCUMENTS | `TestDocuments`: `test_no_role_but_the_administration_reaches_the_documents`, `test_a_deleted_document_is_nobodys_to_read_there_but_a_superusers`, `test_the_administrator_reads_metadata_and_no_file`; `tests/deployment/test_private_documents_are_never_served.py`; `apps/documents` (the download's policy, delivery rule, throttle and record) | `test_the_superusers_link_is_the_documents_own_checked_view`, `test_the_export_of_the_register_is_recorded` |
| ACCOUNTS / PERSON DATA | `TestAccounts::test_no_staff_role_reads_the_accounts`; `test_forms_name_no_account.py` (`test_no_form_of_the_registry_offers_a_choice_of_accounts`, `test_an_add_page_lists_no_other_account`, `test_an_initial_value_names_no_account`, `test_a_crafted_post_names_no_other_account_as_author_or_reviewer`, `test_a_moderator_moves_no_membership_to_another_account`, `test_the_news_editor_filter_lists_only_the_editors_of_the_list`); `test_a_hidden_field_is_no_filter.py` (the tokens, the mail bodies, the answers, the password hash); `test_staff_reaches_no_virtual_forum_screen`; `test_the_operator_reaches_no_notification_screen` | `test_the_administrator_reads_the_accounts_and_not_their_factors`, `test_an_account_that_reads_accounts_still_chooses_them`, `test_the_author_is_the_account_that_creates_the_row`, `test_the_review_action_records_the_reviewer`, `TestTheListsStillWork` |
| REQUESTS / HELPDESK / SELECTION | `test_the_operator_reads_no_request_in_the_back_office`, `test_the_operator_reaches_no_public_submission`, `test_the_administrator_hard_deletes_no_submission`, `TestSuperuserOnlyScreens::test_no_role_reaches_them` (selection, companies, Academy) | `test_the_operator_still_designates_a_professional_on_the_platform`, `test_staff_and_the_administrator_keep_their_work`, `test_a_superuser_reads_every_request`, `TestSuperuserOnlyScreens::test_the_superuser_does` |
| ADMIN — closed case, sensitive operations | `test_the_administrator_changes_neither_a_closed_file_nor_its_lines`, `test_a_closed_files_lines_are_read_only_for_everybody`; the view grants: `test_a_view_only_account_resends_and_cancels_nothing`, `test_staff_withdraws_no_consent`, `test_the_administrator_requeues_and_cancels_nothing`, `test_staff_grants_itself_no_mandate`, `test_staff_moderates_nothing`, `test_nobody_reads_a_subscribers_tokens_there`, `test_the_administrator_rewrites_no_subscription_evidence`, `test_the_administrator_reads_no_answer`; the legal rules: `test_the_view_only_administrator_moves_no_rule`, `test_the_view_only_administrator_is_offered_no_workflow_action`, `test_a_legal_editor_neither_approves_nor_puts_in_force_nor_retires`, `test_the_approver_never_approves_a_rule_it_wrote_and_is_told_why`, `test_the_legal_approver_reads_a_rule_and_cannot_rewrite_it`, `test_the_legal_approver_cannot_rewrite_a_source`, `test_the_view_only_administrator_writes_no_new_version`, `test_a_role_without_the_rules_screens_reads_neither_the_diff_nor_the_preview` | `test_the_administrator_still_changes_an_active_file_and_deletes_a_closed_one`, `test_the_administrator_reads_the_body_and_resends_with_a_record`, `test_the_administrator_records_a_withdrawal_in_the_audit_trail`, `test_a_superuser_requeues_with_a_record`, `test_moderators_and_the_administrator_keep_moderating`, `test_the_administrator_still_anonymises_on_request`, `test_the_legal_approver_approves_puts_in_force_and_retires`, `test_a_legal_editor_submits_for_review_edits_a_draft_and_opens_a_new_version`, `test_a_superuser_is_offered_every_action_and_the_service_keeps_its_refusals` |
| AUDIT | `test_the_legal_approver_reads_its_rules_trail_and_nothing_else`, `TestTheAuditTrail::test_no_other_role_reads_it`, `test_a_refused_action_records_no_transition`, no event for an unchanged status (above) | `test_a_lines_status_changed_there_is_recorded_by_the_domain` (`case.checklist.status`: who, line, from, to), `test_trusting_a_member_is_recorded`, `test_the_export_of_the_register_is_recorded`, the withdrawal, resend and requeue records above, `test_the_administration_reads_the_whole_trail` |
| 2FA | `TestAPrivilegeMeetsTheSecondFactor`: `test_a_staff_preview_asks_for_the_factor_first` (six previews), `test_an_unpublished_article_asks_for_the_factor_first`, `test_a_moderator_reads_the_forum_only_after_the_factor`, `test_a_moderator_moderates_nothing_before_the_factor`, `test_an_account_the_deployment_requires_to_enrol_is_sent_to_enrol`; the source guard `test_every_staff_branch_of_a_public_view_asks_for_the_second_factor`; sec-f5's `test_backoffice_second_factor.py` | `TestWhatStays`: a session that presented its factor previews and moderates, a published page owes nothing, a visitor and a member untouched, nothing owed without a device where the deployment does not require one |
| INTEGRATIONS API | `test_unexpected_input.py`: an escaped and a raw NUL in a signed body, a NUL and a lone surrogate in a header, a lone surrogate in a body, a signature that is not ASCII, a timestamp that is no plain number, a body nested deeper than the decoder recurses, an impossible parameter, a NUL in the query string, a NUL body on the acknowledgement, `parse_json_body` refusing what the database would; `tests/deployment/test_nul_bytes.py` | `test_a_clean_signed_body_is_still_accepted`, `test_a_surrogate_pair_is_one_character_and_is_accepted`, `test_plain_parameters_still_work`, `test_parse_json_body_still_reads_an_object`, `test_parse_json_body_reads_a_surrogate_pair_as_its_character` |

The merge itself, the audit's summary, the review and the owner's questions are recorded in
`docs/design-v5/DECISION_LOG_V54.md` (DL54-156). No tag, no push, nothing on main, no change to 8780 or to v5-live; no
line in `CHANGELOG_V54.md` or `live_status.json` (not a preview surface — DL54-77, DL54-121, DL54-130, DL54-132). The
release notes' F-8 paragraph («pending F-8's merge», `docs/RELEASE_NOTES_v2.0.0.md`) is w4-d's file: W4-D part 2
completes it. The owner's questions Q-1…Q-9 (§6) stand.
