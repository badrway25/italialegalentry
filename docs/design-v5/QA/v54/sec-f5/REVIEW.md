# F-5 — the back office's second factor — independent security review

Lane `sec-f5-review` (independent security reviewer; built nothing), 15 October 2026. Reviewed: branch `v54-sec-f5`
at `8d98992` — `git diff design-v5...HEAD`, 7 commits, 15 files (`accounts/admin_site.py`, `admin_apps.py`,
`middleware.py`, `services.py`, `decorators.py`, `apps.py`, `config/settings/base.py`, the tests and the documents).
Directive V5.9 kept: nothing deployed, no server, DNS or certificate touched, no package added. No password typed into
a real page: every account below is created by the tests with `user_factory`'s test-only password; TOTP codes are
allauth's own HOTP on a pinned time step. My tests live outside the repository
(`C:/tmp/ile_v5_council/.work/sec-f5/review/test_sec_f5_bypass.py`); a passing test means the attack failed.

## Verdict — SHIP_AFTER_FIXES (nothing blocking)

**F-5 is closed.** I found no way to open `/backoffice/` on a password alone, nor any admin view, the reserved area
or `/documents/`, nor with a session that never presented the factor. 143 of my 144 attack tests hold, among them a
sweep of all 657 admin URL patterns (GET, POST and HEAD; with the middleware and with the admin site alone; both
values of `BACKOFFICE_MFA_ENFORCED`). The same attacks run against `design-v5` reproduce F-5 (the control: the
password-only sign-in, the old form and the unpresented sessions all get in there). Rate limits, CSRF, no user
enumeration, session rotation and the audit trail did not regress.

**One narrow bypass of a property the fix itself adds** (finding 1). After a successful re-authentication, allauth
*replays* a POST it had suspended by calling the view directly, so no middleware runs. A session that never presented
the factor can use this to regenerate the owner's recovery codes. It opens nothing: no back office, no reserved area,
and the new codes stay hidden. It needs the password plus a session opened before the owner enrolled. Those pages
were open to everyone before the fix, so this is not a regression. A small remedy is proven below. With it, and the
document corrections of finding 2, the branch can merge.

## Findings

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | minor — security | allauth's resume-after-reauthentication replays a suspended POST past `BackofficeMFAMiddleware`: a session that never presented the factor regenerates the owner's recovery codes (`test_a_post_stashed_before_enrolment_is_not_replayed_on_a_managed_page` **fails** on the branch) | drop allauth's suspended request on the password re-authentication page when the session owes the factor (below); keep the reviewer's test as the regression test |
| 2 | minor — documents | `prod.py:128` cites `accounts.middleware.EXEMPT_FRAGMENTS`, which the fix removed. Several documents still describe `BACKOFFICE_MFA_ENFORCED` as switching the second factor itself on or off. Since the fix, a device the account holds is asked for in every session whatever the flag says | one sentence in each place (below) |
| 3 | minor — efficiency | the policy runs once per `has_permission` call: on `GET /backoffice/accounts/user/`, 8 of the 27 queries read `mfa_authenticator` | memoise `second_factor_due` per request |
| 4 | minor — tests | `services.session_presented_second_factor` is called by no production code. The middleware docstring names it as the rule, and a test asserts through it | call it from `needs_second_factor_in_session`, or delete it and point the test at `second_factor_due` |

### 1. The replay of a suspended POST

`allauth.account.internal.flows.reauthentication.resume_request` runs after a successful re-authentication, by
password or by code. If the session holds a suspended POST (`account_reauthentication_state`) whose path equals
`next`, allauth resolves that path and calls the view function itself (`resolved.func(suspended_request, …)`). No
middleware runs on that call. Yet the Present rule on allauth's pages that manage the factor lives only in the
middleware (`second_factor_response`, `accounts/middleware.py:130`).

The chain, reproduced end to end by the test:

1. The account holds no device. A session S signs in through allauth with the password; there is no MFA stage,
   because nothing is enrolled.
2. S waits until its last authentication step is older than `ACCOUNT_REAUTHENTICATION_TIMEOUT` (300 s). Then it
   POSTs `/fr/compte/2fa/recovery-codes/generate/`. The policy lets the POST through, since the account holds
   nothing. allauth's `reauthentication_required` stores the POST in S and redirects to `/fr/compte/reauthenticate/`.
3. The owner enrols a TOTP device and recovery codes in their own session.
4. From now on the Present rule holds S on `/backoffice/` and on the generate page (both checked). But S POSTs
   `/fr/compte/reauthenticate/` with the password and `next=/fr/compte/2fa/recovery-codes/generate/`. allauth replays
   the stored POST, and the owner's recovery codes are deleted and regenerated. With `ACCOUNT_EMAIL_NOTIFICATIONS`
   off, nobody is told.

What it does **not** do (checked):

- S cannot see the new codes: `/fr/compte/2fa/recovery-codes/` sends it to the MFA re-authentication.
- S still cannot open the back office.
- The device cannot be removed this way. allauth's deactivation answers 404 while there is no device, so nothing is
  stored then. Once there is a device, S is held before the view runs.

Why fix it anyway:

- The owner's offline codes become void without anyone knowing. If the owner then loses the phone, an administrator
  has to reset the authenticators. That reset opens a new window in which the password alone enrols a device.
- The notes say «allauth's 2fa management pages — Present for an account that holds a factor» and «a device added
  behind an open session — Present». Neither holds on this path.

**Remedy.** Proven by monkeypatch in
`test_proposed_remedy_drop_allauths_suspended_request_when_the_factor_is_owed`. The owner's own resume still works:
`test_proposed_remedy_keeps_the_legitimate_replay_after_presenting_the_factor`.

- In `second_factor_response`, on allauth's password re-authentication page (`^/<lang>/compte/reauthenticate/$`),
  when `services.needs_second_factor_in_session(request, user)` is true, run
  `request.session.pop("account_reauthentication_state", None)` before allauth reads it. A password step never
  counts for such a session, so it must not resume anything.
- An equivalent alternative: hold that page under the Present rule for such a session.
- Either way, add the reviewer's replay test to `test_backoffice_second_factor.py`.

### 2. The documents

- `config/settings/prod.py:128` still says the enrolment page «is exempt from the rule
  (accounts.middleware.EXEMPT_FRAGMENTS)». The fix removed that name. The runbook's twin sentence was updated; this
  one was not.
- **What the flag does, as documented.** These places still describe the flag as it was before the Present rule:
  - `.env.example:38` — «TOTP second factor for every account that reads others' data»;
  - `README.md:178` — «spento in locale»;
  - the comment above `config/settings/base.py:390` — «TOTP mandatory for every staff account entering
    /backoffice/ … Off by default so a fresh local install can reach the back-office»;
  - `docs/SECURITY.md` (A07, and the table at line 184) and `docs/security/PERMISSION_MODEL.md` (L-10). The builder
    left these two to the steward (NOTES, *For the owner* 5).
- **What the flag does since the fix, when it is off** (each point tested):
  - (a) `/backoffice/login/` signs no one in all the same;
  - (b) an account that holds a device must present it in each session before the back office, the reserved area,
    `/documents/` and the 2fa management pages;
  - (c) an account that holds nothing enters on its password. That includes an account whose device was deleted
    mid-session: being optional is what «off» means for enrolment.
- **Suggested sentence:** «the flag makes enrolment mandatory; a device the account holds is asked for in every
  session, whatever the flag says».
- `accounts/checks.py:31` hints «once staff have enrolled a TOTP device». That predates this branch and contradicts
  F-10 (no first-deployment window needs enforcement off).

### 3. The policy's cost per admin page

`BackofficeAdminSite.has_permission` evaluates `second_factor_due` every time it is called: from `admin_view`, from
`each_context`, from the index and app index, on top of the middleware's own call. Measured on
`GET /backoffice/accounts/user/` for a presented superuser: 8 of 27 queries read `mfa_authenticator`. Caching the
answer on the request (keyed by the user's pk) removes the repeats. This has no security effect.

### 4. A helper the policy does not use

`session_presented_second_factor` (`services.py:394`) and `needs_second_factor_in_session` (`services.py:410`) each
implement the binding to the account's own authenticators. Only the second is on the production path.
`test_only_the_sessions_own_new_device_is_remembered` asserts through the first, so it proves something the policy
does not run.

## Every vector of the brief

| Vector | What was tried | Result | Tests |
|---|---|---|---|
| The back office's login URL | `/backoffice/login/` with GET, HEAD, POST, PUT, PATCH, DELETE and OPTIONS × both settings. Fields sent: Django's own (`username`, `password`, `this_is_the_login_form`, `next`) and allauth's (`login`) | never signed in; a 302 to allauth's sign-in; `/backoffice/` stays closed | `test_the_admin_login_signs_no_one_in_whatever_the_method` (14) |
| Every admin auth view, every admin view | the resolver's 657 admin URL patterns (index, password change and done, autocomplete, jsi18n, view on site, unfold's search, every ModelAdmin view including another user's password form), GET, POST and HEAD, from an enrolled superuser's unpresented session. Run with the middleware and with the site alone, × both settings; data compared before and after | no 200, no 5xx, every redirect to a holding page (re-authentication or the admin login); no data changed. Control: a presented session gets 200 | `test_no_admin_view_opens_to_a_staff_session_that_never_presented_its_factor` (4), `test_control_the_sweep_would_see_a_leak`, `test_the_sweep_sees_the_whole_admin` |
| Admin sign-out | GET and POST from an unpresented session | GET 405, nothing shown; POST signs out | `test_signing_out_of_the_admin_stays_open_but_shows_nothing` |
| Direct POSTs, with and without CSRF | the admin login without a token, with a valid token, and from a signed-in person carrying the superuser's credentials | 403 without a token; with one, nobody signed in; the person stays the person (403) | `test_a_post_without_csrf_token_…`, `test_a_post_with_a_valid_csrf_token_…`, `test_a_signed_in_person_cannot_use_the_admin_login_…` |
| Only the password step recorded | the allauth password step, then nine guarded and allauth pages, then the code given to the re-authentication page instead of the stage | nothing opens; still not signed in | `test_a_session_with_only_the_password_step_opens_nothing` |
| Session fixation | a session key planted before allauth's sign-in; a colleague's presented session then used to sign in another account on the same browser | the key rotates and the planted one is dead; no step carries over (Present) | `test_a_planted_session_key_dies_…`, `test_a_colleagues_presented_step_never_carries_over_…`, `test_the_session_key_rotates_at_allauths_sign_in` |
| A session predating the fix, records missing or malformed | 14 log shapes × both settings: absent, empty, password only, a password re-authentication, the id as a string, a bool or a float, the id missing, `MFA` in capitals, an unknown id, non-dict entries, a dict instead of a list, the enrolment key as a string, the enrolment key naming another account's device | always held at the MFA re-authentication; the reserved area stays closed | `test_a_session_predating_the_fix_or_with_a_malformed_log_never_opens` (28) |
| `next=` open redirects | 24 hostile values, signed out and as a presented session: absolute, `HTTPS://`, `user@host`, `//`, `///`, `////`, `/\`, `\/`, `\\`, leading space, tab or NUL, `%2F%2F`, `https:host`, `https:/host`, `javascript:`, `data:`, dot segments, backslash dot segments, `/backoffice@host`, raw and encoded CRLF. Also 5 hostile raw request paths for the redirect that carries `next` (`//evil/espace-reserve/` …), and an absolute `next` at allauth's re-authentication | every Location stays on this site (judged as a browser would: `/\` counted as `//`, leading control characters dropped); no header injected, no 500 | `test_signed_out_the_next_…` (24), `test_signed_in_and_presented_the_redirect_…` (24), `test_the_present_redirect_built_from_the_request_path_…` (5), `test_allauths_reauthentication_refuses_an_absolute_next` |
| Staff promoted mid-session | a person who presented a device; a person with no device (enforced, then off); a person whose device was added behind the session | enters; enrols; enters (the documented «off»); held (both settings) | `test_a_person_who_presented_a_device_then_promoted_enters`, `test_a_person_without_a_device_promoted_mid_session_is_sent_to_enrol_when_enforced`, `test_documented_off_behaviour_a_person_without_a_device_promoted_mid_session_enters`, `test_a_person_promoted_after_a_device_was_added_…` (2) |
| Authenticator deleted mid-session | deleted (enforced, then off); deleted and replaced elsewhere | enrol; enters (the documented «off»); held (both settings) | `test_device_deleted_mid_session_then_enrolment_is_asked_when_enforced`, `test_documented_off_behaviour_device_deleted_mid_session_then_the_session_enters`, `test_device_replaced_behind_the_session_…` (2) |
| allauth's re-authentication | by password; failed codes; an absolute `next`; the replay of a suspended POST | a password step never counts; 429 after the per-user limit and the right code refused; `next` refused; **the replay goes through: finding 1** | `test_a_password_reauthentication_never_counts`, `test_the_mfa_reauthentication_page_is_rate_limited_per_user`, `test_a_post_stashed_before_enrolment_…` |
| The API or any other namespace serving admin views | a walk of the whole URL tree (i18n patterns, `/api/`, `/documents/` …) for any admin-site or ModelAdmin view outside the `admin` namespace; the admin sites alive in memory; how `/api/` authenticates | none outside `/backoffice/`; one admin site object, of the closed class; `/api/` takes Bearer keys only, never a session | `test_no_admin_view_is_mounted_outside_the_backoffice_namespace`, `test_there_is_one_admin_site_and_it_is_the_closed_one` |
| The reserved area's spellings (it relies on the middleware alone) | 12 paths: four languages, three modules, `//`, `%2D`, `/./`, no trailing slash, `/documents/<uuid>/` | none opens to an unpresented professional | `test_no_spelling_of_a_reserved_path_opens_…` (12) |
| `BACKOFFICE_MFA_ENFORCED` off | the paths above with the flag off | the behaviour (a)–(c) of finding 2; the documents need that sentence | the `not-enforced` cases above |

## The other security properties — no regression

- **Rate limits.**
  - allauth's sign-in: after five failures, the right password does not reach the MFA stage.
  - The MFA stage: after five wrong codes, the right one does not sign in.
  - The MFA re-authentication: 429.
  - The admin form had no limit at all; it now authenticates nothing.
- **CSRF.**
  - The admin login without a token gets 403.
  - allauth's sign-in, MFA re-authentication and password re-authentication each refuse a POST without a token.
- **No user enumeration.** The closed form answers byte-identically (status, Location, body, cookies) for the right
  password, a wrong password and an unknown account. allauth's sign-in form and adapter are untouched by the diff.
- **Session rotation.** allauth's sign-in deletes the pre-sign-in key.
- **Audit trail.**
  - allauth's sign-in is recorded as `auth.login`, a wrong password as `auth.login_failed`.
  - The closed form records nothing, because it authenticates nothing.
- **The builder's suites, re-run here** on `ile_v5_l4` with `-p no:randomly`:
  `apps/accounts tests/security tests/backoffice -m "not browser"` gives 329 passed, as in the notes.

## Outside this fix — observations, not findings

- **Enrolment is trust-on-first-use** (by design, pre-existing). Whoever holds the password of an account with no
  device can sign in and enrol a device of their own. Runbook step 8 has the operator enrol at the first sign-in;
  initial passwords must stay private and enrolment be immediate.
- **The perimeter is defined by path.** Privileged actions on public paths are outside both rules, as before the
  fix: moderation in the virtual forum (`/<lang>/forum-virtuel/…/moderation/`) and staff previews of unpublished
  news and «living» pages.
- **The proof lasts as long as the session:** 8 hours after its last write, so a session that keeps writing stays
  alive (the builder's observation 1).

## Reproduce

```
cd C:/tmp/ile_wt/v54-sec-f5
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_v5_l4 PYTHONIOENCODING=utf-8 \
  C:/tmp/italylegalentry/.venv/Scripts/python.exe -m pytest -c pyproject.toml --rootdir . \
  -p no:randomly -p no:cacheprovider C:/tmp/ile_v5_council/.work/sec-f5/review/test_sec_f5_bypass.py
```

Expected on `8d98992`: 1 failed (finding 1), 143 passed.

## Not done

- No change to the branch's code or tests: I review, I do not build. This file is the only one added, and it is not
  committed.
- The full suite was not run here. The areas the change reaches were: my 144 tests and the builder's 329.
