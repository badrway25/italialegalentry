# sec-f8 — independent security review (label sec-f8-review)

Reviewer built nothing. Branch `v54-sec-f8` at `9c8dda4`, from design-v5 `5bf2f90`
(`git -C C:/tmp/ile_wt/v54-sec-f8 diff design-v5...HEAD`). Lane 7 (`ile_v5_l7`), one pytest at a time, `-p no:randomly`,
personas only through `force_login`, test-only passwords. Review tests live outside the repository
(`C:/tmp/ile_v5_council/.work/sec-f8/review/`); none was added to the tree.

## Verdict: SHIP_AFTER_FIXES

The headline F-8 defect is **fixed and holds** under adversarial testing: role:operator (and every other role) now reads
and changes in the back office no more than the platform's own policies allow, across the case file, documents, the help
desk, public submissions, the virtual forum, forum governance, notifications, consents, the audit trail, orientation and
the integrations outbound events. `core.admin_base.PolicyBoundAdminMixin` is a sound construction (model permission AND
policy role AND `readable_by` queryset AND per-object `can`, each necessary), and the querysets close lists, searches,
autocompletes, object pages, history and delete pages together — I could not read or enumerate a case file, a document,
an assignment, an assessment, a help-desk request or a public submission that the platform forbids.

But four residual gaps fall inside the audit's own declared scope (the reviewer's charge — "change through the back
office what the platform policies forbid", "can a filter leak a field the role may not read?" — and the owner's V5.10
mandatory list: ACCOUNTS/PERSON DATA, ADMIN sensitive operations, INTEGRATIONS API unexpected input). Each is verified
with a test. None re-opens the case-file disclosure; all should be fixed (or explicitly accepted by the owner) before
design-v5 is promoted, because V5.10 says the audit scope is not to be reduced and names these categories.

---

## What holds (verified, ALLOW and DENY)

- **Case files** — `test_10_case_files.py`, 27 checks. Ten roles without the "cases" model permission reach no case
  screen (403/redirect, no reference leaked). An operator lists and opens only a LIVE assignment; an unassigned, revoked
  or expired operator gets nothing — list, change, history, delete, search by reference and by owner e-mail, and FIVE
  autocomplete source fields and unfold's sidebar search all answer an unrelated file as an id never issued. A foreign
  checklist line cannot be injected into the formset; the responsible actor is not rewritten; a CLOSED file changes for
  nobody, a superuser included; a line status change writes `case.checklist.status`. A superuser reads every file.
- **Documents** — `test_50_documents.py`, 11 checks. Six roles reach neither document screen nor a document page; an
  unrelated document is not delivered by `/documents/<uuid>/` to a moderator, an operator or a content editor; the
  administrator reads metadata with no file link. The model has no FileField.
- **Help desk, public submissions, selection/companies/academy** — the operator lists no request (0 rows) and still
  designates on the platform register; the superuser-only screens stay the superuser's (inventory probe
  `test_00_inventory.py`, and the implementer's `tests/backoffice/test_screens_follow_the_policies.py`).
- **Accounts screens** — every staff role is 403 on users, person profiles, organisations, e-mail addresses,
  authenticators and groups (inventory + implementer tests); L-01's superuser/-staff/-group guards kept.
- **Second-factor perimeter** — every preview and moderator branch on a public path calls `require_second_factor`
  before it acts; the source guard `test_every_staff_branch_of_a_public_view_asks_for_the_second_factor` keeps future
  ones named. No public visitor path is touched.
- **Integrations API — NUL** — escaped and raw NUL in a signed body, in the headers and in the query string meet a
  controlled 4xx; a clean body is still accepted (implementer's `test_unexpected_input.py`; my `test_70` NUL siblings).

---

## Findings

### F8R-1 (MAJOR) — a view-only administrator and a non-approver legal editor approve and put legal rules in force through the back office

`apps/rules/admin.py` was left untouched by the fix (NOTES §3.6, "the rule editor" under "what did not change"), and its
workflow actions (`action_approve`, `action_activate`, `action_retire`, `action_submit_for_review`) carry no
`permissions=` and call `rules.services.transition`, which checks only the four-eyes author rule — never the role.
`rules.policies` says "approve" is role:legal_approver and not the author, "activate"/"retire" is role:legal_approver;
PERMISSION_MODEL §2.1 gives the administrator "rules: view" only and the legal editor "Redige, non approva". The back
office ignores all of it — exactly F-8's root cause (model permission alone, the object policy never asked; an action
declared without permissions offered to every account that opens the list), on a sensitive operation (a rule in force is
what the engine tells every applicant).

Verified (`test_40_rule_workflow_actions.py`): `can(legal_editor, "approve", rule)` and `can(administrator, "approve",
rule)` are both False, yet through `/backoffice/rules/legalrule/` the legal editor approved another editor's rule, and
the **view-only administrator approved and then activated** a rule (`review_status` -> `approved` -> `active`). The
four-eyes / separation-of-duties control (Technical Blueprint §4) is defeated from the back office; the transition is
audited, but the authorisation is not enforced.

Failure scenario: a single administrator holding `rules: view` opens the rule list, selects a drafted rule, runs
"Approva" then "Metti in vigore"; a wrong or unreviewed legal rule binds every person's assessment with no approver and
no second pair of eyes.

Fix: build `LegalRuleAdmin` on `PolicyBoundAdminMixin` (or give each action `permissions=[...]` and gate the body on
`can(request.user, "approve"|"activate"|"retire", rule)`), so the admin asks the same policy the platform asks.

### F8R-2 (MAJOR) — fields the fix hides from a role stay readable through the changelist query string

The fix removes bearer tokens and sensitive content from the rendered pages (`NewsletterSubscription` tokens,
`EmailOutbox` bodies for a view grant, orientation `answers_snapshot`/`state`), but leaves them as **local-field
filters**. Django's `ModelAdmin.lookup_allowed` returns True for any lookup on a local field, and the changelist prints
the result count, so a value hidden from display is still an oracle one predicate at a time.

Verified (`test_20_hidden_fields_filterable.py`): for role:staff and role:administrator,
`?confirm_token__startswith=<prefix>` on `/backoffice/consents/newslettersubscription/` returns 1 vs 0 (a brute-force
oracle: a base64url token is recoverable in ~64×len requests, no changelist rate limit); for a view-only staff account
`?body_text__contains=<marker>` on the outbox returns 1 vs 0 while the body is absent from the change page; for the
administrator `?answers_snapshot__family=<value>` on the orientation results returns 1 vs 0 while the answers are absent
from the page. `state` on `OrientationSession` is the same class.

This re-opens, by brute force, the exact harm the fix identified for the tokens (NOTES §1.8: "whoever opens a
subscription can confirm it in the subscriber's name … or end it"): the tokens are the subscriber's bearer secrets.

Fix: override `lookup_allowed` (or filter the changelist params) on these admins to refuse lookups over the hidden
fields — an allowlist of the fields a role may filter on — so a hidden field is hidden from the query string too.

### F8R-3 (MAJOR) — editorial forms list every account's e-mail address to roles that may not read accounts

The accounts screens are correctly 403 for role:staff and role:content_editor, but the editorial models whose
`author`/`reviewer` foreign keys render with a plain select (`UnfoldAdminSelectWidget`) list **every** account —
18/18, applicants and persons included — with `User.__str__` being the e-mail address. `portal.PortalNotice` already
limits its `reviewer` to `is_staff` (15/18), so the pattern to follow exists.

Verified (`test_30_person_data_in_form_widgets.py`): on the ADD form, role:staff reads the e-mail of a person, another
person, an operator and the administrator on `cms/sitebanner`, `forum/forumevent`, `living/livingtopic`, `news/article`,
`partners/partner`; role:content_editor on `cms/homehero`, `living/livingsheet`, `news/article`, `partners/partner`. An
autocomplete-backed field (`faq/faqitem?author=<pk>`) renders the selected account's e-mail from its id for both roles.
"No broad staff visibility of person data without authorisation" (V5.10) is not met for these forms.

Fix: give these FKs `autocomplete_fields` (the User autocomplete already checks the target's view permission, which
these roles lack -> 403, no leak) or `limit_choices_to={"is_staff": True}`, as `PortalNotice` does.

### F8R-4 (MAJOR) — a signed webhook body with a lone UTF-16 surrogate crashes the integrations API (500)

The fix guards NUL in the JSON body (`carries_nul`) but not lone surrogates, which `json.loads` accepts into a Python
`str`. Such a value is kept by `minimal_inbound_payload` / `event_type` and written to PostgreSQL jsonb/text, which
refuses it — the same database refusal the NUL guard exists to prevent, and the same "signed body" trust level the fix
already chose to harden (NOTES §3.4; the implementer's own test asserts "never a 500", "no ERROR line, no traceback").

Verified (`test_70_api_unexpected_input.py`): a signed body `{"event":"…","external_id":"\ud800"}` (and `\udfff` in
`event`, `\ud83d` in `status`) returns **500** — `DataError: invalid input syntax for type json` /
`UnicodeEncodeError: surrogates not allowed` with a traceback logged. Needs the system's shared secret, so a trusted
integration partner (not the public), and the transaction rolls back (availability, not disclosure) — hence MAJOR, not
blocking. Non-finite numbers (`NaN`, `Infinity`, `1e999`) are handled; a clean body is still accepted (202).

Fix: in `decode_json`, reject a value that will not round-trip to the database (refuse a string carrying a lone
surrogate, or catch the write and answer 400), so "unexpected input -> a controlled response" holds for surrogates as it
does for NUL.

---

## No regression, and legitimate work

- My ALLOW tests pass throughout: the assigned operator changes and records a line status; a superuser reads every file;
  the administration reads the documents register, the message/notification channel, the audit trail; the legal_approver
  still approves and activates; a clean webhook is accepted.
- sec-f5 (the second factor) and sec-f7 (the "who may" table, read-only fields, the assignment capacity) are not
  weakened: the mixin adds conditions, removes none; the second-factor policy now also reaches public-path privileges.
- No new user-visible string (fr/ar/it/en); the findings' fixes above need none either. Missing words for copy packet
  B1: none.
- CSRF, CSP, rate limits, `readable_by`, audit events: untouched by the branch and by the suggested fixes.

Regression (lane 7, `-m "not browser"`, one run): the implementer's four new modules + sec-f5's `test_backoffice_second_factor` / `test_mfa_middleware` / `test_identity_gaps` + sec-f7's `test_transition_actors` + `tests/security/{test_object_permissions,test_authorization_audit,test_privilege_escalation}` + `tests/deployment/{test_nul_bytes,test_private_documents_are_never_served}` + `tests/compliance/test_public_pages` = **474 passed, exit 0** (668 s). The review's own suite = **49 passed, 22 failed** (187 s): the 22 failures are the four findings' DENY tests (F8R-1 rule actions, F8R-2 filter oracles, F8R-3 editorial e-mail, F8R-4 API surrogate); every ALLOW / positive-control test — the case-file matrix (27), documents (11), the operator's removal from notifications (3), the inventory, the rule policy's own refusals and the legal_approver's success, the clean webhook and non-finite numbers — passed.

## Owner's open questions
NOTES §6 (Q-1 … Q-9) remain for the owner; F8R-1 and F8R-3 are new to this review and are not among them.
