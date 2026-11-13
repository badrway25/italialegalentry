# F-5 — the back office's second factor — lane notes

Lane `sec-f5-fix` (security implementer), branch `v54-sec-f5` (worktree `C:/tmp/ile_wt/v54-sec-f5`, created from
`design-v5` at `3d5351b`), 15 October 2026. Brief: the DevOps lane's finding F-5
(`docs/design-v5/QA/v54/devops/NOTES.md`; checklist A-13), under directive V5.9 (never deploy, never touch
production). A security fix, not design work.

**Hard limits kept.** No deployment, no server, no DNS, no certificate. No package added (allauth 65.19.4, Django
5.2.17, django-unfold 0.107.0 as installed). No password typed into a real page or stored: every test creates its own
accounts with the test-only password of `user_factory`, and its TOTP secrets with allauth's own generator. One pytest
at a time, on this lane's database (`ile_v5_l4`). No other security property weakened — rate limits, CSRF, no user
enumeration, session rotation and the audit trail are each covered below.

## The finding, reproduced first

A staff account WITH a TOTP authenticator, `BACKOFFICE_MFA_ENFORCED=True`:
`POST /backoffice/login/?next=/backoffice/` with the password alone → **302 `/backoffice/`** → `GET /backoffice/` →
**200** (and the audit trail logs `auth.login`). Committed first as a strict xfail
(`9eef573`, `test_f5_the_backoffice_sign_in_form_never_opens_the_backoffice_on_a_password_alone`), so the fix had to
remove the marker.

## Root cause

Two facts, each sufficient on its own:

1. **The back office had a second sign-in door.** `/backoffice/login/` is Django's `AdminSite.login`: a `LoginView`
   with the admin's authentication form (unfold's `AuthenticationForm` subclasses `AdminAuthenticationForm`), which
   calls `authenticate()` and `login()` with the password. allauth's MFA stage is one of allauth's *login stages*: only
   allauth's own flows run it. Django's form knows nothing of it — and has no rate limit either (allauth's
   `login_failed` limits apply to allauth's form only).
2. **The policy asked a question about the account, never about the session.** `BackofficeMFAMiddleware` asked
   `needs_backoffice_mfa(user)` → `has_active_totp(user)`: *is a device enrolled?* Enrolment is a property of the
   account; *presenting* the device is a property of the session. A session opened by any door that skips allauth's
   stage — the admin form, `Client.force_login`, a shortcut written later — passed as long as the account owned a
   device.

allauth's own `secure_admin_login` decorator would not have been enough: for a signed-in staff session it still
hands a POST to Django's form, which signs in **another** account on its password alone.

## How allauth records the methods of a login (read in the installed source)

`allauth.account.internal.flows.login.record_authentication` appends to the session key
`account_authentication_methods` (constant `AUTHENTICATION_METHODS_SESSION_KEY`); the public reader is
`allauth.account.authentication.get_authentication_records(request)`. A password sign-in writes
`{"method": "password", "at": …, "email": …}`; the MFA stage, when it accepts a code
(`allauth.mfa.base.internal.flows.post_authentication`), writes `{"method": "mfa", "at": …, "id": <authenticator pk>,
"type": "totp" | "recovery_codes" | "webauthn"}`, and `mfa_reauthenticate` the same with `"reauthenticated": True`.
A sign-in's two records are written **before** allauth calls Django's `login()`, whose key rotation (`cycle_key`)
keeps the session data — that is how they reach the signed-in session; a re-authentication writes into the
signed-in session itself. Django flushes the session, and the log with it, on `logout()` and on a `login()` as a
different account. A device's **activation** writes no record.

## The fix

| Commit | What |
|---|---|
| `9eef573` | the reproduction, as a strict xfail |
| `1dd3185` | **(a)** the back office's own sign-in signs no one in |
| `a340bff` | **(b)** an account that holds a second factor gets in only after presenting it in this session |
| `e6170d6` | a device this session enrols through allauth counts as presented (no second code right after enrolment) |
| `812e8ef` | `/documents/` joins the reserved area's perimeter (the middleware's own docstring already said it was in it) |
| `17c9dd9` | test polish: the password re-authentication test first proves allauth accepted the step |
| the commit adding this file | these notes and the DevOps documents' F-5 entries |

**(a) `accounts/admin_site.py` — `BackofficeAdminSite`**, unfold's site with `login()` replaced. It never reads the
request body, never calls `authenticate` or `login`:

- signed out → 302 to allauth's sign-in (`settings.LOGIN_URL`), `next` = the back-office page asked for **if** it is
  one of this site (`backoffice_next`: Django's `url_has_allowed_host_and_scheme`, then a path under the admin index
  with neither scheme nor host), else the index — no open redirect (eleven hostile values tested);
- signed in, an active staff account → that page, or first the second factor (enrol / present);
- signed in, anything else → **403** — no form to sign in as another account, no redirect that could loop.

Installed the documented way: `unfold.apps.BasicAppConfig` (leaves the default site alone) and
`accounts.admin_apps.BackofficeAdminConfig` (an `AdminConfig` whose `default_site` names the class) in place of
`django.contrib.admin`. Checked by diff: the registry (107 models, each with its `ModelAdmin` class) and the 118 admin
URL patterns are identical before and after.

**(b) The rule — `accounts.services.second_factor_due(request, user)`**, for an account the policy covers
(`reads_other_peoples_data`):

- **Enrol** (unchanged): it holds no TOTP device and `BACKOFFICE_MFA_ENFORCED` → the activation page.
- **Present** (new): it HOLDS a second factor (TOTP or WebAuthn — what allauth's MFA stage asks for) and THIS session
  has not presented one of the account's **own** authenticators (`session_presented_second_factor`) → allauth's MFA
  re-authentication (`mfa_reauthenticate?next=<the page>`), then back. A password step never counts, nor a step proved
  with another account's device (a sign-in begun as A and abandoned leaves A's step in a session that B's later
  `login()` keeps), nor a step whose authenticator has been deleted since.
- **Independent of `BACKOFFICE_MFA_ENFORCED`.** The setting decides whether enrolment is *mandatory*; allauth asks an
  enrolled account for its code at every sign-in whatever it says, so a signed-in session of such an account that
  never presented it was opened by another door. (This also closes F-5 on a deployment run with
  `ILE_ALLOW_INSECURE_PROD`.)

Enforced at three points, each tested on its own:

1. `BackofficeMFAMiddleware` on the guarded perimeters: `/backoffice/`, the reserved area (MFA by responsibility, not
   by URL — PERMISSION_MODEL L-10) together with the private documents' endpoints that serve it (`/documents/`,
   language-neutral, mounted outside the reserved area — `812e8ef`; before, an operator who had not enrolled was sent
   to enrol on `/fr/espace-reserve/…` and could still open `/documents/<uuid>/` directly). And on **allauth's pages
   that manage the factor** (`/<lang>/compte/2fa/…`: index, deactivate, recovery codes view/generate/download):
   allauth lets a signed-in session re-authenticate there **with the password**, which for a session that never
   presented the factor is the way round it — turn the device off, enrol another, walk in. The two pages where the
   factor is presented (`reauthenticate/`, `authenticate/`) stay open, and so does enrolling for an account that holds
   nothing.
   **Exemptions are now the exact routes** (allauth's and the admin's sign-out), never a fragment anywhere in a path:
   a back-office object id is `<path:object_id>`, so `/backoffice/accounts/user/1/2fa/change/` used to borrow the
   «/2fa/» exemption and skip the middleware.
2. `BackofficeAdminSite.has_permission` (and its login view): the middleware knows the back office by its path; the
   site keeps the policy without it and wherever it is mounted. The admin's sign-out stays open.
3. `mfa_required_for_backoffice`, the decorator for back-office-like views outside `/backoffice/`.

**`e6170d6` — enrolling counts as presenting.** allauth's activation takes a right code of the new device but records no
`mfa` step; without this, an account that has just enrolled — the enrolment the policy demanded — was stopped on the
very next page allauth shows it (its recovery codes) and asked for a second code. `services.remember_enrolment`,
connected to allauth's public `authenticator_added` signal, remembers in the session (`ile.second_factor_enrolled`) a
TOTP/WebAuthn device that allauth's own flow has just added **for the session's own account**. It changes nothing for
a device that existed before the session: allauth adds a TOTP device only to an account that holds none, and the pages
that add one are behind the Present rule for an account that holds a factor. An authenticator saved any other way (the
admin, a script) sends no signal and proves nothing. allauth sends the signal on commit: the tests that drive the
activation are transactional, the only way to reproduce production's order (under `ATOMIC_REQUESTS` the commit happens
when the view returns, before the session is saved).

**No new user-visible string.** The re-authentication page is allauth's, translated by allauth; the i18n catalogue
gate (`tests/i18n/test_catalogues.py`) is untouched.

## Every way into the back office, checked

| Path | Before | Now | Held by |
|---|---|---|---|
| `POST /backoffice/login/` with a password (F-5) | signed in; `/backoffice/` 200 | 302 to allauth's sign-in; no session; no `auth.login` nor `auth.login_failed` audited | `test_f5_…_on_a_password_alone` (both settings), `test_it_authenticates_no_one_whatever_it_is_sent` |
| `GET /backoffice/login/` signed out | Django's form | 302 to allauth's sign-in, safe `next`; no password field; `no-store` | `test_a_signed_out_visitor_is_sent_to_allauth_…`, `test_a_next_that_is_not_a_backoffice_page_…` (11 values), `test_it_renders_no_password_field` |
| any back-office page signed out | → Django's form | → `/backoffice/login/` → allauth's sign-in | `test_an_anonymous_visit_to_any_backoffice_page_ends_at_allauth_sign_in` |
| `/backoffice/login/` signed in without the back office | «sign in as another account» form | 403, no loop | `test_a_signed_in_account_without_the_backoffice_meets_a_refusal_not_a_form` |
| allauth's sign-in, enrolled account | MFA stage, then in | MFA stage; the back office checks the session's MFA step; a wrong code never opens it; a recovery code does | `test_through_allauth_the_code_is_asked_before_the_backoffice_opens` (both settings), `test_a_wrong_code_never_opens_it`, `test_a_recovery_code_is_a_second_factor_too` |
| any other door (`force_login`, a future shortcut, a session left by the old form) | in, the device being enrolled | → MFA re-authentication, then in | `test_a_session_opened_by_another_door_is_sent_to_present_the_factor` (both settings), `test_presenting_the_code_at_reauthentication_opens_it` |
| allauth's MFA re-authentication | — | counts; rate-limited by allauth (failed codes `login_failed` per account; `reauthenticate` per user) | `test_failed_codes_at_reauthentication_are_rate_limited` |
| allauth's password re-authentication | — | never a second factor | `test_a_password_reauthentication_is_not_a_second_factor` |
| a step from another account's device / a deleted authenticator | — | never counts | `test_a_step_proved_with_another_accounts_device_does_not_count`, `test_a_step_whose_authenticator_is_gone_does_not_count` |
| a device added behind an open session (an administrator adds one) | in | Present | `test_a_device_added_behind_an_open_session_is_not_a_proof` |
| staff created or promoted while signed in | enrol, then in | enrol (allauth's activation counts as presenting); a device added otherwise → Present | `test_a_person_promoted_to_staff_while_signed_in`, `test_enrolling_through_allauth_counts_as_presenting_the_new_device`, `test_a_device_enrolled_in_one_session_is_presented_in_that_one_only` |
| the admin's password change | staff only | + the policy | `test_the_backoffice_password_change_needs_the_factor` |
| the admin's and allauth's sign-out | open | open — exact routes, at the middleware and at the site | `test_the_backoffice_sign_out_stays_open_and_ends_the_session`, `test_allauths_sign_out_stays_open`, `test_the_admin_site_keeps_the_policy_without_the_middleware` |
| allauth's 2fa management pages | exempt for everyone | Present for an account that holds a factor; presenting pages and enrolling stay open | `test_the_pages_that_manage_the_factor_need_it_presented` (6 pages), `test_the_page_where_the_factor_is_presented_stays_open`, `test_an_unenrolled_account_can_still_enrol` |
| crafted paths holding «/2fa/» or «/logout/» | exempt | not exempt | `test_a_crafted_path_borrows_no_exemption` (5 paths), `test_the_exemptions_are_exactly_signing_out_and_presenting` |
| password reset → sign-in | no sign-in (`ACCOUNT_LOGIN_ON_PASSWORD_RESET` off) | the same; the next sign-in asks the code | `test_a_password_reset_signs_no_one_in_and_the_next_sign_in_asks_the_code` |
| «remember me», long sessions, trusted browser, passkey, login by code, bypass code | — | none enabled — pinned by a test | `test_no_setting_opens_a_door_around_the_mfa_stage` |
| the back office remounted / the middleware missing | middleware only, by path | the site keeps the policy | `test_the_admin_site_keeps_the_policy_without_the_middleware`, `test_a_staff_session_that_did_not_is_sent_to_present_it` |
| the reserved area | enrolment only | + Present, every language and module | `test_an_enrolled_professional_presents_the_factor_before_any_case_file`, `test_an_enrolled_professional_signed_in_through_allauth_enters` |
| `/documents/` (downloads, requirement review, signed links) | **outside both perimeters** | guarded with the reserved area | `test_the_documents_endpoints_belong_to_the_perimeter` (5 endpoints, both settings), `test_an_unenrolled_reviewer_enrols_before_any_document_when_enforced`, `test_a_persons_documents_are_not_concerned` |
| accounts outside the policy (a person, even with a device) | unaffected | unaffected | `test_a_person_with_a_device_is_not_concerned` |
| design preview persona switch | dev only, never staff or privileged | unchanged (outside the policy) | the preview's own tests |
| sign-up / e-mail confirmation | no sign-in before verification; no sign-in on confirmation | unchanged | `test_real_login.py` |
| an account created in the back office or by `createsuperuser` | no verified address: allauth mails the confirmation at its first sign-in | unchanged; then enrolment when enforced | `test_unverified_email_cannot_enter_the_reserved_area` |
| QA scripts that mint a session (`scripts/qa_*.py`, `capture_baseline.py`) | the session, as `force_login` | the same, unless the account holds a device (no seed gives one): then the Present rule | — |

**The other security properties.** *Rate limits*: the admin form had none; every sign-in now meets allauth's, and
the new door (MFA re-authentication) is allauth's, limited. *CSRF*: `CsrfViewMiddleware` is global and untouched; the
closed view changes no state. *No user enumeration*: the closed view answers every POST identically, whatever the
account. *Session rotation*: unchanged — every sign-in is allauth's, through Django's `login()`. *Audit*: every
sign-in and failed sign-in is still audited by the existing receivers; the closed view performs no authentication to
audit.

## Tests

- `apps/accounts/tests/test_backoffice_second_factor.py` — 68 tests; `test_mfa_middleware.py` updated: an
  enrolled device is no longer enough on its own (the two assertions that encoded the old rule now require the
  session's step, and the decorator's test gains the Present case).
- The design preview's browser test «a page the frame cannot hold» linked `/backoffice/login/`; signed out, every
  back-office address now ends at allauth's sign-in, which that frame may hold. It now links the preview's own index
  (run in Chromium: the old version times out against the fix, the new one passes).
- **Mutation check** — each layer broken on purpose, the F-5 tests run, the file restored:

  | Layer broken on purpose | Tests failing (of 75) |
  |---|---|
  | (a) the admin login uses Django's form again | 23 |
  | (a) `next` not validated | 10 |
  | the middleware never asks to present | 27 |
  | the admin site's `has_permission` ignores the policy | 1 |
  | any `mfa` record counts (no binding to the account) | 2 |
  | Present only when `BACKOFFICE_MFA_ENFORCED` | 22 |
  | exemptions back to fragments | 11 |
  | 2fa management pages not guarded | 7 |
  | reserved area not guarded by Present | 7 |
  | `/documents/` not guarded | 3 |
  | enrolment in this session not remembered | 3 |
  | the enrolment receiver remembers another account's device | 1 |
  | the enrolment receiver remembers recovery codes | 1 |

  Run on the final code (`812e8ef` plus the test polish), the F-5 module with `test_mfa_middleware.py`; every file
  restored after each run (`git diff` empty).

- **Suites**, on the final code, one at a time on `ile_v5_l4` with `-p no:randomly` (all green):

  | Run | Result |
  |---|---|
  | `apps/accounts` `tests/backoffice` `tests/security` (`test_production_settings_refuse_to_start` included) | 329 passed |
  | `tests/deployment` `tests/compliance` `tests/i18n` `apps/audit` `apps/documents` (`-m "not browser"`; the edited runbook and checklist included) | 523 passed |
  | every test file that drives the admin — `community`, `companies`, `ecosystem`, `enquiries`, `faq`, `forum` (×2), `glossary`, `living`, `news`, `orientation`, `pages` (×2), `partners`, `pathways`, `selection`, all of `apps/portal` and `apps/rules`, `tests/compliance/test_gates.py` | 513 passed |
  | the documents' and depot's pages (`tests/frontend/test_documents_w3_c.py`, `test_depot_w3_c.py`) and `test_private_documents_are_never_served.py`, with the F-5 module | green (193 and 127 in two runs) |
  | the design preview's two framing tests, one of them in Chromium | 2 passed |
  | `manage.py check`; `makemigrations --check --dry-run` | no issues; no changes |

  The admin registry (107 models with their `ModelAdmin` classes) and the 118 admin URL patterns were diffed against
  `design-v5`: identical.

## For the owner (observations, nothing changed)

1. **How long the proof lasts.** As long as the session: 8 hours after its last write (`SESSION_COOKIE_AGE`;
   `SESSION_SAVE_EVERY_REQUEST` off) and the cookie ends with the browser (`ACCOUNT_SESSION_REMEMBER = False`). A
   shorter life for back-office sessions — asking the code again every few hours — is a policy decision.
2. **The admin's own password change** stays (now behind the policy) but does not apply allauth's `change_password`
   rate limit nor `ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE`; sending staff to allauth's page would make one path of the two.
3. **Rate limits per Gunicorn worker** (local-memory cache, runbook *Known limits*) apply to the MFA re-authentication
   as to every allauth limit.
4. **The nginx redirect** of `/backoffice/login/` (runbook step 11) is kept as a second layer; it can stay.
5. `docs/SECURITY.md` and `docs/security/PERMISSION_MODEL.md` (Italian) could gain a line stating the session rule;
   left to the steward with the merge.
6. **QA scripts that mint a session** (`scripts/qa_*.py`, `capture_baseline.py`, «what `force_login` does, written
   out») now meet the Present rule for an account that holds a device; no seed gives a QA account one.
7. **WebAuthn** is not enabled. If it were, the Present rule already counts it, while the Enrol rule — unchanged —
   would still ask a WebAuthn-only account to add a TOTP device.

## Not done

- No push, no merge, no tag (the steward's).
- **The full suite was not run here.** Three other lanes' suites (two of them browser suites) were running on this
  machine and its PostgreSQL server; a full non-browser run would have taken hours and slowed the V5 families, which
  come first (directive V5.9 §18) — the DevOps lane's precedent. In its place: every area the change can reach, above
  (about 1 400 distinct tests). The steward's regression at the merge and CI (`-m "not browser"`) remain the full runs.
- The two observations of `For the owner` that would change behaviour (a maximum age for back-office sessions; one
  password-change path) are decisions, not fixes, and were left alone.

## Review fixes

Lane `sec-f5-fix2` (security implementer), 15 October 2026, on top of `8d98992`. The independent review
(`REVIEW.md`, lane `sec-f5-review`, committed with this section) found F-5 closed, nothing blocking, and four minor
findings — verdict SHIP_AFTER_FIXES. All four are fixed, each with its tests. The hard limits above held: nothing
deployed, no server touched, no package added, no password typed into a real page, one pytest at a time on
`ile_v5_l4`.

| # | Finding | Commit | Fix | Tests |
|---|---|---|---|---|
| 1 | security — after a **password** re-authentication, allauth resumed a suspended POST past `BackofficeMFAMiddleware`: a session that never presented the factor regenerated the owner's recovery codes | `98b0067` | `accounts.middleware.forget_what_a_password_step_must_not_resume`, called first by the middleware: on allauth's password re-authentication page (`PASSWORD_REAUTHENTICATION`), a session that owes the factor (`services.needs_second_factor_in_session`) loses allauth's suspended request (`account_reauthentication_state`, the constant imported from allauth) before the page reads it | `TestAllauthsResumptionOfASuspendedRequest` (11) |
| 4 | tests — `session_presented_second_factor` was called by no production code; `needs_second_factor_in_session` carried its own copy of the binding | `a29e3cd` | the policy decides through `session_presented_second_factor`, handing it the authenticators it has already read (`_authenticators_of`): one binding rule, no extra query | `test_only_the_sessions_own_new_device_is_remembered` (now through `second_factor_due`, with a covered account on the other side), `test_the_policy_runs_the_binding_rule_it_documents` |
| 3 | efficiency — the policy ran on every `has_permission` call: 8 of the 27 queries of `GET /backoffice/accounts/user/` read `mfa_authenticator` | `035da86` | `second_factor_due` keeps its answer on the request, keyed by what the request itself can change: the account, `BACKOFFICE_MFA_ENFORCED` and the steps the session presented. Now 2 of 21 | `test_an_admin_page_reads_the_accounts_authenticators_once`, `test_the_answer_is_kept_for_the_request_but_follows_what_it_was_computed_from` |
| 2 | documents — `prod.py` cited the removed `accounts.middleware.EXEMPT_FRAGMENTS`; several places described the flag as switching the second factor on or off | `96ba940` | in each place, the sentence «the flag makes enrolment mandatory; a device the account holds is asked for in every session, whatever the flag says» (list below) | `test_every_name_of_the_accounts_code_they_cite_exists` (fails on the old `prod.py`), `test_what_the_flag_does_when_it_is_off`; `test_the_pages_that_manage_the_factor_need_it_presented` now runs under both settings |

**1 — allauth's resumption.** When a page asks for a recent sign-in, allauth keeps the POST it interrupted in the
session and, after the re-authentication (by password or by code), calls that view itself (`resume_request`): no
middleware runs on the call. A password step never presents the factor, so a session that owes it has nothing to
resume there. allauth still records the step and sends the session to `next`, where the middleware holds the page
and asks for the code. Three things stay as they were, on purpose, each pinned by a test:

- the MFA re-authentication page's resumption: allauth checks and records the code first, so what it resumes runs
  for a session that has just presented the factor (`test_presenting_the_factor_at_reauthentication_resumes_the_request`,
  both settings);
- the password page's resumption for a session that owes nothing: the owner's own regeneration still runs after a
  password step (`test_a_session_that_presented_the_factor_still_resumes_its_request`);
- the boundary, request by request (`test_only_a_password_step_of_a_session_that_owes_the_factor_loses_it`, 5
  cases). The route patterns are checked against `reverse("account_reauthenticate")` and
  `reverse("mfa_reauthenticate")` in the four languages, so a change of allauth's mount point fails a test.

The reviewer's chain is `test_a_request_suspended_before_enrolment_is_not_resumed_by_a_password_step` (both
settings); with the drop removed, it fails under both. The reviewer's whole attack suite (outside the repository)
gives 144 passed on the fixed branch. On `8d98992` the review reports 1 failed, 143 passed; the failing test was
reproduced here before the fix.

- **Placement.** In `BackofficeMFAMiddleware.__call__`, not in `second_factor_response`: that function answers
  what the policy owes a request (`must_redirect` with it) and keeps no side effect.
- **The reviewer's alternative**, holding the password page under the Present rule, was not taken. The drop is the
  smaller change, the one the reviewer proved, and it leaves allauth's page to what it re-authenticates outside the
  policy.
- **Scope** (read in the installed source, allauth 65.19.4). A request is suspended only by a view that raises
  `ReauthenticationRequired`. Here those are allauth's own 2fa pages (its e-mail management would too, but
  `ACCOUNT_REAUTHENTICATION_REQUIRED` is off); no project view raises it (grep). The admin site keeps the policy at the view, so a resumed admin view would still meet it. The
  reserved area relies on the middleware alone: were a view there ever to ask allauth for a recent sign-in, its
  resumption after a password step by an account that must enrol would skip the Enrol rule. None does today; noted,
  not built.

**3 — the answer kept for the request.** Reading the account's authenticators and roles once per request is safe
because only a request's first answer admits anything. An admin page is one view, admitted by its first check, and
its later checks (`each_context`, the index) ask the same question. allauth's resumption happens on the
re-authentication pages, where the middleware asks nothing (they are neither guarded nor managing), so a resumed
view computes its own answer. Each of the key's three parts, removed by mutation, fails the test.

**2 — the documents changed.**

- `config/settings/prod.py`: the docstring's list of refusals, the comment above the flag, and the refusal's
  comment (no `EXEMPT_FRAGMENTS` any more). Its message now names the accounts «that have not enrolled a second
  factor»; the test pins only its first words.
- `config/settings/base.py`: the comment above the flag.
- `.env.example` and `README.md`: the flag's line.
- `docs/SECURITY.md`: A07, and the 12.2 row, which said that switching the flag on in production waited for staff
  onboarding (`prod.py` has refused it off since 21 September 2026, `156e41a`).
- `docs/security/PERMISSION_MODEL.md`: a paragraph «Attivare e presentare sono due regole», the L-10 row, and the
  stale line reference `middleware.py:37-53`. This does the builder's *For the owner* 5.
- The runbook's `accounts.W001` row, and the W001 check's message and hint. The hint said «once staff have enrolled
  a TOTP device», which contradicted F-10.

**Runs**, one at a time on `ile_v5_l4` with `-p no:randomly` (all green):

| Run | Result |
|---|---|
| `apps/accounts` `tests/security` `tests/backoffice` (`-m "not browser"`) | 351 passed: the builder's 329 and the 22 new |
| `tests/deployment` `tests/compliance` `tests/i18n` `apps/audit` `apps/documents` `tests/test_env_example_is_complete.py` (`-m "not browser"`) | 537 passed: the builder's 523 and the `.env.example` file's 14 |
| every test file that drives the admin (the builder's list; all of `apps/forum`, `apps/portal`, `apps/rules`) and `tests/frontend/test_design_preview.py` (`-m "not browser"`) | 948 passed |
| the documents' and depot's pages (`tests/frontend/test_documents_w3_c.py`, `test_depot_w3_c.py`, `-m "not browser"`) | 69 passed |
| the reviewer's attack suite | 144 passed |
| `manage.py check`; `check --deploy` (W001 shows the new text); `makemigrations --check --dry-run` | no issues; as expected; no changes |

The F-5 module now holds 90 tests (68 before).

**Not done.**

- The full suite was not run, for the reason given above; the steward's merge regression and CI remain the full
  runs.
- No push, merge or tag.
- One side effect outside the repository: a run of the reviewer's suite rewrote their measurement file
  (`measure_queries.txt`) with the fixed branch's figure. It was put back to the figure `REVIEW.md` records.

## At the merge (the steward, 15 October 2026)

The steward's merge step (`sec-f5-merge`, under the merge lock) synced design-v5 into this branch (`ddd468d`: W3-D's
merge, its steward's record DL54-129 and its shipped note). No conflict, and no path in common: W3-D's templates,
CSS, JS and presenters on one side, this branch's accounts, settings and documents on the other. No test outside
`apps/accounts` creates an authenticator, so the Present rule meets no other family's tests. Then:

- **Ownership.** The family «sec-f5» is registered in `docs/design-v5/OWNERSHIP_V54.json` outside the waves — 21
  entries, 4 whole and 17 slices, each with its reason (`93eff12`) — and `scripts/check_ownership.py` accepts the id
  `sec-f<n>` (`814e005`). `check_ownership.py sec-f5 design-v5`: 22 paths, 5 inside, 17 slice → PASS, each slice read
  in the diff; `--validate`: 27 families, 672 entries.
- **Tests on the merged branch** (`ile_v5_l4`, one pytest at a time, `-p no:randomly`):
  the merge brief's list — `tests/backoffice`, `apps/accounts`, `tests/security` (the production settings' refusals among
  them), `tests/deployment` (`test_production_checks.py` among them), `tests/compliance`,
  `tests/frontend/test_design_docs.py` — with `tests/test_check_ownership.py`, `tests/test_env_example_is_complete.py`
  and `tests/test_migration_drift.py`: **574 passed** in 12 min 12 s, no skip, no xfail. Then
  `tests/frontend/test_design_preview.py` and `tests/i18n/test_documentation.py` (`-m "not browser"`; W3-D's merge
  changed the preview's `apps/core/dev.py`): 307 passed; the framing test this branch changed, in Chromium: 1 passed.
  `manage.py check`: no issue; `makemigrations --check`: no changes; `ruff check` and `ruff format --check`: clean on
  the 15 Python files.
- **Scan.** The family's 1 989 added lines: no IPv4 address but loopback, no production host or droplet name, no live
  domain, only `example.test` addresses, no credential but the test-only passwords of the existing auth tests.

The merge itself, the review and what is left are recorded in `docs/design-v5/DECISION_LOG_V54.md` (DL54-130).
