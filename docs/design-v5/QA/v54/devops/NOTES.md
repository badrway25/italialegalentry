# DevOps readiness (directive V5.9) — lane notes

Lane `devops-impl`, branch `v54-devops` (worktree `C:/tmp/ile_wt/v54-devops`, created from `design-v5` at `1c03e3b`),
12 October 2026. Brief: the owner's directive V5.9 (`C:/tmp/ile_v5_council/directives/V5_9_DELIVERY_AND_PRODUCTION_READINESS.md`),
read in full, with V5.8 (the legacy host is LEGACY_REFERENCE_ONLY).

**Hard limits kept.** No deployment. No connection to, resolution of or contact with any production host. No DNS
change, no domain operation, no certificate. No package installed, nothing downloaded. No secret in the repository —
the only values are placeholders, and the generated values used for the local verification lived in a scratch
directory outside it and were never committed. No production server address, host name or droplet name in any file
(a test now refuses a non-loopback, non-documentation IPv4 address in `docs/deployment/`). No future domain: the new
documents use `example.com` / `<your-domain>`. No template, CSS or JS file and no other family's QA folder touched.

## Delivered

| File | What |
|---|---|
| `docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md` | the runbook: exact commands for Ubuntu 24.04 LTS on DigitalOcean from a release tag, steps 1–15, and the sections the owner asked for (static vs public media vs private documents, TLS/HTTPS, registrar transfer vs DNS cutover, the cutover sequence step by step, legacy, release tags, the three states, known limits) |
| `docs/deployment/PRODUCTION_CHECKLIST.md` | §A the owner's release gate (V5.9 §15), 22 items each with how to verify it and what evidence to keep, plus the go-live blockers and decisions (A-23…A-27); §B before deployment; §C backup before cutover with a restore check («do not claim a backup exists unless verified»); §D smoke test |
| `docs/deployment/ROLLBACK.md` | previous tag; forward-only migrations and the verified dump; storage restored with its database; DNS rollback in the TTL window; safe vs unsafe |
| `docs/deployment/production.env.example` | the template of the server's environment file (systemd `EnvironmentFile=`): production values and `<...>` placeholders |
| `.env.example` | every variable the application reads — settings, code, scripts, tests — grouped, one comment each; optional variables commented out (see F-3) |
| `config/settings/prod.py` | see «Production settings» below |
| `config/settings/base.py` | one line: an empty `PRIVATE_MEDIA_ROOT` means the default directory |
| `apps/core/checks.py` (+ one import in `apps/core/apps.py`) | `core.E001`, `core.W001`, `core.W002`, `core.W003` |
| `docker-compose.staging.yml` | passes `IP_HASH_SALT` (now mandatory under the production settings) |
| `tests/deployment/` | `test_production_checks.py`, `test_private_documents_are_never_served.py`, `test_error_pages_with_debug_off.py` (+ `error_urls.py`), `test_runbook_matches_the_code.py` |
| `tests/security/test_production_settings_refuse_to_start.py`, `tests/test_env_example_is_complete.py` | extended / made stricter |
| `docs/DEPLOYMENT.md`, `docs/DEPLOYMENT_READINESS.md`, `README.md` | superseded pointers (history kept); README environment and deployment sections point to `docs/deployment/` |

Commits on `v54-devops`: `6484968` settings + checks + tests · `298664e` environment files + test · `8a69674` error
pages through the handlers · `49cbe06` runbook, checklist, rollback + runbook test · `18ac6d0` superseded pointers +
README · this notes commit.

## The architecture summary of the brief, checked point by point

| Claim | Verdict | Evidence |
|---|---|---|
| Django 5.2 LTS | ✓ 5.2.17 | `requirements/base.txt` |
| PostgreSQL via psycopg 3 and `DATABASE_URL` | ✓ binary wheel, no `libpq-dev` | `requirements/base.txt`, `base.py` |
| WhiteNoise, `CompressedManifestStaticFilesStorage` | ✓ served through Gunicorn; bundles and `.mo` catalogues committed — no Node, no gettext on the server | `base.py`, `git ls-files static/*/dist locale` |
| Gunicorn | ✓ 26.2.0; supports systemd socket activation and `sd_notify` (read in its source) | `requirements/base.txt`, `gunicorn/arbiter.py` |
| «optional Redis cache (`REDIS_URL`)» | **✗ corrected** — not usable: Django's `RedisCache` needs the `redis` client library, which is not in the requirements. With `REDIS_URL` set, every cache access raises `ModuleNotFoundError` (run: dev settings, `REDIS_URL=redis://127.0.0.1:1/0`) — allauth's rate limits run on the cache, so sign-in would fail. Now `core.E001`; the templates keep it empty | F-2 |
| SMTP e-mail | ✓; allauth's e-mails are sent during the request, notifications are queued in `EmailOutbox` | `notifications/services.py` |
| Private documents outside `MEDIA_ROOT`, authorised views only | ✓ `documents.views._serve` is the only exit (policy + `delivery_block`, attachment, `no-store`, CSP sandbox, audited); `open_for_download` has no other caller | `documents/views.py`, `services.py`, `storage.py` |
| `prod.py` already hardened | ✓, and extended (below) | |
| Queued notifications need a scheduled sender | ✓ `send_queued_emails`; the full job list has seven entries | runbook step 10 |
| `ILE_VERSION_LABEL` | ✓ default `v2.0.0 — Fase 1`, but **only a fallback**: the footer reads `SiteSettings.version_label` (same default, editable in the back-office) | `core/context_processors.py`, `core/models.py` |
| Forms go only to contact@agamieuromed.org | ✓ default of `FORMS_DESTINATION_EMAIL`, kept in both templates | `base.py` |
| `/media/` | **public media exists**: `seed_all` copies the library's photographs into `MEDIA_ROOT` (15 files, verified), the Forum's public photos/videos/PDFs and the logo are uploaded there. Django serves `/media/` only with DEBUG on, so nginx must serve it | `cms/seeds_media.py`, `forum/models.py`, `config/urls.py` |
| Health endpoint | ✓ `/healthz/` (`SELECT 1`); covers the database only | `core/views.py` |

## Findings — each found by running something

- **F-1 — allauth behind a reverse proxy (fixed).** allauth trusts no proxy by default (`ALLAUTH_TRUSTED_PROXY_COUNT=0`):
  behind nginx on TCP every visitor is `127.0.0.1` — one rate-limit bucket for the world (five failed sign-ins by
  anyone lock everyone out for five minutes; ten sign-ups an hour site-wide); on a unix socket `REMOTE_ADDR` is empty
  and allauth's adapter raises `PermissionDenied("Unable to determine client IP address")` on every rate-limited
  action, sign-in included. Probe output: `TCP bind, default: 127.0.0.1` · `UNIX socket, default: PermissionDenied` ·
  with one trusted proxy `203.0.113.7` in all three cases, a client-forged left-most entry included. Fix:
  `ALLAUTH_TRUSTED_PROXY_COUNT = env.int(..., default=1)` in `prod.py`; nginx overwrites `X-Forwarded-For` with
  `$remote_addr` (also required by `core.privacy.client_ip`, which reads the **first** entry); `core.W001` reports a
  proxy trusted by Django and not by allauth.
- **F-2 — `REDIS_URL` unusable** (above). `core.E001`; documented in both templates and the runbook.
- **F-3 — the development template's empty values (fixed).** With django-environ 0.14 an empty variable is a value:
  `bool` → False, `int` → ValueError, `str` → `''`. Copying the old `.env.example` (README: `cp .env.example .env`)
  gave `PRIVATE_MEDIA_ROOT=` → `Path("")` → `.` → **identity documents written in the root of the checkout**
  (`private_root()` resolved to `C:\tmp\ile_wt\v54-devops`; numbered directories are not git-ignored);
  `ILE_SEED_DEMONSTRATION_DATA=` → False although its comment said «default DJANGO_DEBUG»; `ILE_VERSION_LABEL=` → `''`;
  `SECURE_HSTS_SECONDS=` → a parse error under the production settings. Fixed: optional variables are commented out,
  `base.py` treats an empty `PRIVATE_MEDIA_ROOT` as unset (and `prod.py` an empty `MEDIA_ROOT`), and the test refuses
  an empty declaration whose default is not empty.
- **F-4 — the sitemap prints `http://example.com/...`** until the `django_site` row is set (`django.contrib.sites` +
  `SITE_ID=1`; the initial migration creates `example.com`). Runbook step 8 sets it; the smoke test checks it.
- **F-5 — the back-office sign-in path does not ask for the second factor — GO-LIVE BLOCKER, fixed** (lane
  `sec-f5-fix`, branch `v54-sec-f5`, 15 October 2026 — `docs/design-v5/QA/v54/sec-f5/NOTES.md`). As found: a superuser
  WITH a TOTP device, `BACKOFFICE_MFA_ENFORCED=True`: `POST /backoffice/login/` with the password alone → 302 →
  `GET /backoffice/` → 200. Django's admin sign-in form is not allauth's (no MFA stage), and
  `accounts.services.needs_backoffice_mfa` asks whether a device is *enrolled*, not whether *this session* used it.
  Not fixed here: it is the accounts lane and it changes the staff sign-in flow. Recommended: send
  `/backoffice/login/` to allauth's sign-in (keeping `next`), and have `BackofficeMFAMiddleware` require, for an
  enrolled account, that the session's authentication records include the MFA step. Checklist A-13; the runbook tells
  the operator to sign in through `/fr/compte/login/` only.
  **Fixed by** the recommended change, in depth: `/backoffice/login/` signs no one in and sends the visitor to
  allauth's sign-in with a safe `next` (`accounts/admin_site.py`, the default admin site); an account that holds a
  second factor reaches the back office, the reserved area or a private document only if allauth's log of THIS
  session's authentication steps shows its MFA step with one of the account's own authenticators — whatever
  `BACKOFFICE_MFA_ENFORCED` says — enforced by `BackofficeMFAMiddleware`, by the admin site itself and on allauth's
  pages that manage the factor (`accounts.services.second_factor_due`). Tests:
  `apps/accounts/tests/test_backoffice_second_factor.py` — the reproduction is
  `test_f5_the_backoffice_sign_in_form_never_opens_the_backoffice_on_a_password_alone`; also
  `test_through_allauth_the_code_is_asked_before_the_backoffice_opens`,
  `test_a_session_opened_by_another_door_is_sent_to_present_the_factor`,
  `test_the_pages_that_manage_the_factor_need_it_presented`,
  `test_the_admin_site_keeps_the_policy_without_the_middleware` — and `test_mfa_middleware.py`. The nginx redirect
  stays as a second layer.
- **F-6 — a request for an unknown Host gets no error page.** `templates/partials/seo_head.html` computes
  `request.get_host` on every page, the 400 page included: `DisallowedHost` again in the 400 handler, again in the
  500 handler, then the WSGI server's bare 500. Recorded as a strict xfail (`raises=DisallowedHost`) in
  `tests/deployment/test_error_pages_with_debug_off.py`; production is protected by nginx's catch-all server (runbook
  step 11). The template fix belongs to its owner (checklist A-21).
- **F-7 — `DATABASE_URL` had a development fallback in production** (127.0.0.1:5439, the development password): a
  process missing the variable would have failed at its first request, not at boot. Now mandatory in `prod.py`.
- **F-8 — `IP_HASH_SALT` had a published fallback in production** (`dev-salt-change-me`): every stored IP hash
  (audit, consents, forms, uploads, throttle keys) reversible by hashing the IPv4 space. Now mandatory, refused when
  published or shorter than 32 characters.
- **F-9 — Python 3.12 vs 3.13.** Ubuntu 24.04 LTS ships 3.12; CI and the Dockerfile run 3.13. All 766 project sources
  compile under a local CPython 3.12.10 (`compile()` in memory, 0 syntax errors) and no 3.13-only library call is
  used (searched). The test suite itself was not run on 3.12: it would need packages installed into a 3.12
  environment, which this lane may not do.
- **F-10 — the first deployment does not need `ILE_ALLOW_INSECURE_PROD`.** `prod.py`'s docstring said it might,
  «before staff have enrolled a TOTP device». Under the production settings with enforcement on, an allauth sign-in
  of a fresh superuser is accepted and the back-office redirects to `/fr/compte/2fa/totp/activate/` (smoke test);
  the docstring now says so.
- **F-11 — the scheduled jobs.** The older documents missed `documents_refresh_requirements` («run it daily») and
  `clearsessions` (database sessions), and listed `deliver_outbound_events`, which does nothing useful until a push
  transport is approved (`INTEGRATIONS_ALLOW_NETWORK` is a setting, not a variable). `documents_purge_expired` and
  `purge_expired_submissions` dry-run by default: their timers pass `--apply` (held by the runbook test).

## Production settings — what changed and why

`config/settings/prod.py`:

- mandatory: `DATABASE_URL` (F-7) and `IP_HASH_SALT` (F-8), beside the three that already were;
- `SECURE_HSTS_INCLUDE_SUBDOMAINS` / `SECURE_HSTS_PRELOAD` read from the environment **with the current values as
  defaults (on)** — the defaults are not weakened. Turning either off is an operator's explicit statement about the
  domain's other hosts, and `check --deploy` reports it (`security.W005` / `W021`). The production *template* sets
  both to `0` for the cutover, because no inventory of the domain's subdomains exists and includeSubDomains on the
  apex breaks any subdomain that is not on valid HTTPS for a year; the runbook's TLS section says when to turn them on.
  They are not in the refusal list: they concern the domain's other hosts, not this application's security;
- `ALLAUTH_TRUSTED_PROXY_COUNT` (F-1); `MEDIA_ROOT` from the environment; `CONN_HEALTH_CHECKS = True` (connections are
  reused 60 s by a fixed set of workers: after a PostgreSQL restart each worker would otherwise answer one 500);
- refused unless `ILE_ALLOW_INSECURE_PROD=1`: `*` in `DJANGO_ALLOWED_HOSTS` (Host-header poisoning of the e-mailed
  links), a published or short salt, a mail backend that does not deliver (`console` would write password-reset links
  into journald), an unfilled `<...>` placeholder of the production template;
- refused **even through the hatch**: `PRIVATE_MEDIA_ROOT` overlapping `MEDIA_ROOT`, `STATIC_ROOT` or
  `STATICFILES_DIRS` — WhiteNoise indexes `STATIC_ROOT` at start-up, so a private file there would become public after
  a restart; `documents.storage.private_root()` only checked `MEDIA_ROOT`, and only at the first upload.

Verified unchanged and correct: `DEBUG = False` forced; `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` without default;
`SECURE_PROXY_SSL_HEADER`; session, CSRF and language cookies `Secure`; `USE_X_FORWARDED_HOST`; structured JSON logging
to the console; error handlers for 400/403/404/500 (+ `error_429`); no development assumption left in `prod.py`
(the Windows path `C:/tmp/ile_v5_council/proof` and the ports 8770/8771/8780 live in `dev.py`'s preview block, which
`prod.py` never reads — listed in the NOT FOR PRODUCTION section of `.env.example`).

## Commands run and their results

All on this workstation; the database is the local development PostgreSQL (docker, 127.0.0.1:5439). Placeholder
production values were generated at run time (`secrets.token_urlsafe`) in a scratch script outside the repository.

| Command | Result |
|---|---|
| baseline `pytest tests/test_env_example_is_complete.py tests/security/test_production_settings_refuse_to_start.py` | 14 passed |
| `manage.py check --deploy` under `config.settings.prod`, before any change | «System check identified no issues» |
| same, after: placeholder mail values (no `EMAIL_HOST`, sender `@example.com`) | `core.W002`, `core.W003` — as designed |
| same, with `EMAIL_HOST` and a real-domain sender | **0 issues** (exit 0 with `--fail-level WARNING`) |
| same, with `SECURE_HSTS_INCLUDE_SUBDOMAINS=0 SECURE_HSTS_PRELOAD=0` | `security.W005`, `security.W021` — the expected cutover warnings |
| `collectstatic --noinput`, production storage, temporary `STATIC_ROOT` (scratch settings module) | 571 files copied, 1317 post-processed; manifest 571 entries; 746 `.gz`; `main.css`, `portal/console.css`, `shell.js` hashed |
| `makemigrations --check --dry-run` under the production settings | «No changes detected», exit 0 |
| `CREATE DATABASE ile_devops_scratch`; `migrate --noinput` under the production settings | every migration applied |
| `migrate --check` · `showmigrations` | exit 0 · 71 `[X]`, 0 `[ ]` |
| `seed_all` (production settings) | 30 seeds; the three demonstration seeds «skipped»; 15 library photographs copied to `MEDIA_ROOT` |
| `createsuperuser --noinput` (smoke only), then the runbook's `EmailAddress` and `Site` one-liners | both one-liners work as written |
| in-process smoke through the full production middleware stack (Django test client, scratch settings) | **17/17 pass**: healthz, HTTP→HTTPS 301, home 200, HSTS / CSP / X-Frame-Options, secure cookies, hashed bundle served by WhiteNoise `immutable`, product 404 without debug output, sitemap and robots on `https://example.com`, no `/media/` from Django, login 200, **allauth sign-in accepted behind the proxy**, **back-office redirects to TOTP enrolment**; plus F-6 |
| the scheduled commands under the production settings | `send_queued_emails` sent=0 failed=0 · `clearsessions` exit 0 · `documents_refresh_requirements` · `notifications_scan_deadlines --dry-run` · the three purge dry runs · `rules_pending_review --strict` exit 0 · the runbook's mail-queue one-liner prints `{}` |
| `pg_dump -Fc` → `pg_restore` from stdin into a restore database (inside the database container) | dump 1.7 MB; `django_migrations` / `accounts_user` / `documents_privatedocument` counts identical (71 / 1 / 0) — the checklist's C-6 procedure works |
| targeted suites (deployment, security, env, back-office, documents, accounts, static pipeline, …) | 460 passed |
| `pytest tests/deployment` | 34 passed, 1 xfailed (F-6) |
| `ruff check .` | All checks passed |
| full suite `pytest -m "not browser" -p no:randomly` | **stopped at 1 %** — see «Full suite» at the end |
| the remaining areas the changes touch, on the final files: `tests/compliance`, `tests/security/test_confidential_material.py`, `tests/i18n/test_documentation.py`, `apps/core`, `tests/test_migration_drift.py`, `tests/test_check_ownership.py`, `tests/deployment`, the env and refusal tests | 204 passed, 1 xfailed, **1 failed → fixed** (below), then `tests/deployment` with a browser module collected: 34 passed, 1 xfailed |

Scratch databases `ile_devops_scratch` and `ile_devops_restore_test` were dropped afterwards; `test_ile_devops`
(pytest's `--reuse-db` database of this lane) remains.

Not run, by necessity: Gunicorn (it does not run on Windows), nginx, systemd, certbot — the configuration they read
was reviewed, not executed; the runbook validates each on the server (`systemd-analyze verify`, `nginx -t`,
`certbot renew --dry-run`, the smoke test) and says what to relax if the sandbox refuses something.

## Open questions for the owner

1. **F-5, the back-office sign-in path** — answered: fixed by the sec-f5 lane with the recommended change (staff sign
   in through allauth's page; the middleware — and the admin site — check that the session used the second factor).
   What remains is D-12 on the server.
2. **Release tag**: `v2.0.0` (the version the platform already displays) or `v1.0.0` (the directive's example)?
   Release candidate: `v5-release-candidate` (then `-2`, never a moved tag).
3. **Host names**: apex, `www`, or both — and which is canonical? Is a temporary validation host (a new subdomain
   pointing at the droplet, option A of cutover step 3) acceptable?
4. **HSTS**: who inventories the domain's subdomains, and when may `includeSubDomains` be turned on? Submitting to the
   preload list is a separate decision.
5. **Database**: PostgreSQL 16 on the droplet (the runbook's default) or a DigitalOcean Managed PostgreSQL cluster in
   an EU region? Development and CI run 17.
6. **Python**: run the suite once on 3.12 before the release (a CI job — `.github/workflows/ci.yml` is the steward's
   file), or install 3.13 on the server?
7. **SMTP**: provider, sender domain (SPF/DKIM), and is outbound SMTP open from the droplet (DigitalOcean restricts it
   on many accounts; 2525 is a common alternative)?
8. **Redis**: accept rate limits counted per Gunicorn worker (up to three times the configured figure), or add the
   Redis client library to the requirements (a new dependency) and run Redis?
9. **Backups**: off-server EU location, who holds the encryption passphrase, retention aligned with the privacy
   retention terms, DigitalOcean droplet backups or snapshots (region)?
10. **Access logs**: the runbook masks the client address (consistent with the application, which never stores a raw
    IP); is a raw-IP log with a short retention wanted for incident response?
11. **Health**: an endpoint that also checks the private storage and the mail queue — wanted? (Not invented here.)
12. **F-6**: the template fix of `partials/seo_head.html` — which family schedules it?
13. **Which server**: the runbook's firewall and catch-all steps are for a fresh droplet; if the designated server
    already hosts other sites, who owns its nginx `default_server` and its firewall?
14. **EU hosting (CR-08)**: written confirmation of the region of the droplet, the database and the backups.

## Not done

- No deployment and no action on any server, DNS record, domain or certificate (forbidden by the directive).
- Gunicorn, nginx, systemd and certbot not executed (Windows workstation, no server): reviewed, not run.
- The test suite on Python 3.12 (needs packages installed in a 3.12 environment).
- F-5 not fixed here (accounts lane; it changes the staff sign-in flow) — fixed since by the sec-f5 lane; F-6 not
  fixed (a template).
- No CI change (the workflow is the steward's file); no release tag (tags are milestone decisions, after final QA).

## Full suite

Started on the lane's own database (`test_ile_devops`) and **stopped at 1 % after about fifteen minutes**: three
other lanes' suites were running on the same machine and the same PostgreSQL server, the pace projected to many
hours, and the V5 families' runs come first (directive V5.9 §18). The lane's processes were stopped and their
connections checked gone. In its place, every area the changes can reach ran on the final files (table above);
the steward's full regression at the merge and CI on the published commit (`.github/workflows/ci.yml`, about
57 minutes) remain the full runs.

That targeted run found one defect of this lane, now fixed: `test_check_deploy_reports_no_issue_under_the_runbook_configuration`
inherited `DJANGO_ALLOW_ASYNC_UNSAFE=true` — which the browser test modules set in `os.environ` when they are
imported, deselected or not — and the child `check --deploy` reported `async.E001`. In CI, which collects every
module, it would have failed. The helper now drops the variable (a server never has it), and the fix was
verified by collecting `tests/frontend/test_browser.py` in the same run. The development-settings probe of
`test_private_documents_are_never_served.py` now also pins `ILE_DESIGN_PREVIEW=0`, so a developer's `.env` cannot
change what it sees.

## Review fixes

Lane `devops-fix`, 12 October 2026, on `663539a`. Brief: `REVIEW.md` (nine major, ten minor, six nits) and
`VERIFY.md` (three major, thirteen minor), both SHIP_AFTER_FIXES. **Every major and every minor finding is fixed;
five of the six nits too.** Each fix is held by a test where a test can hold it, and exercised where this
workstation can run it.

**Hard limits kept.** No deployment. No connection to, resolution of or contact with any production host. No DNS,
domain or certificate operation. Nothing installed, nothing downloaded: Gunicorn ran in the project's own staging
image, already on this machine, offline (`--network none`); gpg is Git for Windows'. No secret in the repository:
the generated values and the throwaway gpg key lived in scratch directories outside it, now deleted. The diff of
this pass adds no IPv4 address but loopback and the two public resolvers, no production host name, no secret-like
token (scanned by pattern, nothing typed). No template, CSS or JS file and no other family's folder touched. The code
changes stay in two management-side files (`apps/companies/management/commands/companies_demo.py`,
`apps/rules/seeds.py`); no in-flight branch modifies either (checked on every local branch).

| Finding | Change | Evidence |
|---|---|---|
| **M1** password in sudo's log | Runbook step 6: the password goes to psql on stdin (`printf '\\set pw %s\n'`, a builtin). CREATE ROLE / CREATE DATABASE run only when missing (`\gexec`); `ALTER ROLE … PASSWORD :'pw'` sets the password on each run. Managed path: the backup reads `/etc/italylegalentry/pgpass` (0600); `<connection string>` in argv is gone | `test_no_password_reaches_a_command_line`. **Exercised** on the local PostgreSQL 17 with probe names: two runs, both exit 0; the file's password opened the database over scram-sha-256 and a wrong one was refused; 0 server-log lines held the password |
| **M2** no backup after go-live | Runbook step 10, «The nightly backup»: `/usr/local/sbin/ile-backup` and `italylegalentry-backup.{service,timer}` (01:30 Rome). It runs `pg_dump -Fc` first, then the private, media and configuration archives, each streamed through gpg `--recipient-file` (the owner's **public** key). It writes `SHA256SUMS` by relative name, keeps 7 days locally and prunes forgotten rollback dumps. The off-server copy goes through an owner-written hook (rsync-over-SSH example); the run exits 2 until the hook exists. Checklist A-28 (go-live gate) and §B | `test_a_backup_runs_every_night_encrypted_and_leaves_the_server`. **Exercised** (Git Bash, the real script with paths re-rooted, `runuser` shimmed to the PostgreSQL container, throwaway key): the set was written and copied to a local stand-in; `sha256sum -c` passed there; C-6 restored it and every document row's file matched its sha256. A damaged copy failed, a missing file failed, a failing `pg_dump` failed with nothing left behind, and pruning removed an 8-day-old dump and a 13-hour-old partial folder |
| **M3** / verify 3 / m8 — empty manifest, archives off the server in clear | Checklist §C is now the backup's first run with the application stopped, the manifest checked inside the directory, C-5 the off-server copy, and C-6 a restore elsewhere with the private key: counts, row-to-file sha256 check, media count, config listing. The config archive includes `/etc/letsencrypt` and the catch-all server | `test_the_backup_before_the_cutover_is_the_nightly_backup_and_leaves_nothing_in_clear`; the drill exercised as above |
| **M4** Gunicorn control socket | `--no-control-socket` in `ExecStart` | **Reproduced** in `italylegalentry-staging-web` (Gunicorn 26.2.0), user 65534, `HOME=/nonexistent`, read-only root, `--max-requests 2`: four `[ERROR] Control server error: [Errno 30] Read-only file system` lines (start plus three recycles); with the flag, 0. `test_gunicorn_runs_without_its_control_socket` reads the pinned source |
| **M5** vacuous `-p err` | The error check counts `"level": "(ERROR\|CRITICAL)"\|[(ERROR\|CRITICAL)]` in the journal's content, with `sudo` (a non-adm account counts nothing). It is written once in step 13 and used in cutover step 2 and D-20 | `test_the_no_error_checks_read_the_content`, `test_the_checklist_error_checks_read_the_content`; the pattern counts the real `StructuredFormatter` output (1 error, 1 warning of 3 lines) and Gunicorn's lines (above) |
| **M6** / verify 2 / m10 — code switched under a live service | §15 stops the service, its socket, the timers and any running job before the checkout. It takes a rollback dump of the stopped database, checked by a restore, and starts everything after `collectstatic`. ROLLBACK §1 does the same. nginx serves a static maintenance page with a 503 meanwhile, through a URI `error_page`: a named location would answer a POST with 405. Per-release directories are written down as the later improvement | `test_an_update_stops_the_application_before_the_code_changes`, `test_a_code_rollback_stops_the_application…`, `test_a_maintenance_page_answers_while_the_application_is_stopped`. Not run: nginx (no image here, no download) |
| **M7** AddField misread | ROLLBACK §1 and §2: code-rollback-safe means `CreateModel`, a nullable `AddField`, an `AddField` with `db_default`, or a non-unique `AddIndex`. A NOT NULL `AddField` with only a Python default, and any unique constraint, go to §2/§3 under the two-release rule | Django 5.2.17 `base/schema.py` `add_field` (the default is dropped unless `has_db_default()`); test above |
| **M8** back-office MFA bypass | nginx: `location = /backoffice/login/ { return 302 /fr/compte/login/$is_args$args; }`. Step 0 is qualified; step 8 explains; A-13 gives the `curl` check and stays a go-live blocker for the accounts fix (since fixed by the sec-f5 lane; the redirect stays as a second layer) | `test_the_password_only_backoffice_sign_in_is_closed_at_the_edge` (`reverse("admin:login")`, `reverse("account_login")` under `fr`) |
| **M9** seed_all reverts the jurist | `rules.legal_ruleset`: `get_or_create`; an existing source is only completed where a field is empty; `jurisdiction` stays build-owned (not in the admin, corrected by the seed before). The runbook keeps `seed_all` at every release, with `--only` for a seed a handoff flags | `apps/rules/tests/test_seed_keeps_editorial_changes.py` (5 tests): **fails on the previous code** (checked), passes now |
| **Verify 1** `companies_demo` without a guard | `demonstration_data_allowed()` guard with a `CommandError`, as `rules_activate_demonstration` has; the runbook row now says so | `apps/companies/tests/test_demo_command.py`. **Re-run** under `config.settings.prod` on a scratch database: exit 1, 0 company profiles (was: exit 0, company and four needs) |
| **m1** HSTS on by default | `prod.py` reads both directives with no default; the staging stack, `.env.example` and the three test environments declare them | Refusal tests (both names); end to end: with the line deleted, «Set the SECURE_HSTS_INCLUDE_SUBDOMAINS environment variable» |
| **m2** / verify 9 — A-5 vs the template | A-5 says which configuration gives which result. The two tests are named for the HSTS values they run, and one is tied to the template's lines | **End to end**: template values → exactly `security.W005` and `security.W021`, exit 1; both directives on → «no issues», exit 0 |
| **m3** env file wider than needed | `/etc/italylegalentry` 0700 root:root; the env file 0600 root:root (systemd reads it as root) | `test_the_environment_file_is_root_only` |
| **m4** managed PostgreSQL | `sslmode=verify-full` with the cluster's CA; `GRANT CREATE, USAGE ON SCHEMA public` as the admin user | **Reproduced** on PostgreSQL 17 with a non-superuser CREATEDB/CREATEROLE admin: «permission denied for schema public». The review's `ALTER DATABASE … OWNER TO` fails («must be able to SET ROLE») for a user that admin did not create; the GRANT works. django-environ passes `sslmode` / `sslrootcert` to `OPTIONS` (checked) |
| **m5** / verify 7 step numbers | Environment file = step 5, database = step 6, in both templates | read |
| **m6** / verify 4 rename/drop case | Lower-case timestamps everywhere (`%Y%m%dt%H%Mz`) | **Checked** on PostgreSQL 17: rename, then `dropdb "…_failed_$TS"`, exit 0; `test_git_runs_as_root_and_timestamps_stay_lower_case` |
| **m7** / verify 10 certbot names | TLS step 3 and cutover step 7: `-d "$ILE_DOMAIN" ${ILE_STAGING_HOST:+-d "$ILE_STAGING_HOST"}` (+ www when served); step 8's reissue unchanged | the idiom tested in bash: two names when set, one when empty |
| **m9** DNS-to-certificate window | Documented under cutover step 6 (HSTS visitors cannot click through; DNS-01 as the owner's option) | read |
| **Verify 5** ROLLBACK §3 «code steps» | «only the checkout, the SHA test, the two `pip` lines and `collectstatic`» | test above |
| **Verify 6** `git describe` without sudo | `sudo git -C …` | every `git -C` of the three documents is held to `sudo` |
| **Verify 8** annotated tag SHA | A-2 compares `refs/tags/<tag>^{}` | **Exercised** on a local annotated tag: the plain line is the tag object, `^{}` is the commit; a lightweight tag has only the plain line |
| **Verify 11** AAAA / CAA | Cutover 5 records A, AAAA and CAA; step 6 points or removes AAAA and checks CAA; ROLLBACK §5 restores AAAA | read |
| **Verify 12** `POSTGRES_PASSWORD` | Documented in NOT FOR PRODUCTION; the completeness test reads `docker-compose*.yml` in both directions | `test_every_variable_the_compose_files_interpolate_is_documented` |
| **Verify 13** unpinned closure | `requirements/constraints.txt`: all 19 distributions for Linux/CPython 3.12, at the versions the project's tests run on, each accepting 3.12. `-c` in runbook steps 4 and 15 and ROLLBACK §1 | `tests/deployment/test_requirements_constraints.py`: direct pins equal base.txt's; the closure walked under the server's markers equals the pinned names; the set satisfies its own requirements; every install line uses it |
| **Verify 14** memory figure | Labelled an estimate, with how to read the real one | read |
| **Verify 15** «characters» vs bytes | «64 / 48 random bytes, URL-safe»; the generator replaces exactly those strings | `test_step_5_fills_the_templates_placeholders`; end to end: 86 and 64 characters, 43 for the database password |
| **Verify 16** token paths | Three kinds, with lifetimes read in the code: 10 min (`DOWNLOAD_LINK_TTL = 600`), 3 days (`PASSWORD_RESET_TIMEOUT`, not overridden), 3 days (`ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS`) | read |
| Nits | `server_tokens off` on port 80; `proxy_ignore_headers X-Accel-Redirect`; `smtp.example.net` in the tests; D-20's 5xx count anchored on the request's closing quote (`grep -cE '" 5[0-9]{2} '`); the 86-character secret (verify 15). **Not done:** a `prod.py` placeholder refusal for `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — an SMTP password may legitimately hold `<` or `>`, `EMAIL_HOST`'s placeholder is already refused, and step 5's `grep` lists all four | — |

Commits of this pass: `7274549` HSTS without a default, deploy checks named (m1, m2) · `cb684ca` `companies_demo`
guard (verify 1) · `9baadc0` legal sources keep the jurist's corrections (M9) · `80e9e84` constraints file
(verify 13) · `88a6108` environment templates (m5, verify 7, 12, 15) · `119f655` runbook procedures (M1, M2, M4, M5,
M6, M8; m3, m4, m7, m9, m10; verify 10, 11, 14, 16) · `ab3ddb9` checklist §C and rollback (M3, M5, M6, M7; m6, m8;
verify 3–6, 8) · this commit (reserved SMTP test host, these notes).

**Commands run on the final files**

| Command | Result |
|---|---|
| `pytest tests/deployment tests/test_env_example_is_complete.py tests/security tests/compliance tests/i18n/test_documentation.py tests/test_check_ownership.py tests/test_migration_drift.py tests/test_demonstration_data_switch.py apps/rules apps/companies apps/core apps/cms/tests/test_media_assets.py -m "not browser" -p no:randomly` (`…/ile_devops`; the confidential-material test with its sentinels) | **561 passed, 1 xfailed** (F-6), 0 skipped — 6 min 15 s |
| After the last change (the reserved SMTP host): `pytest tests/deployment tests/test_env_example_is_complete.py tests/security/test_production_settings_refuse_to_start.py apps/rules/tests/test_seed_keeps_editorial_changes.py apps/companies/tests/test_demo_command.py` | **104 passed, 1 xfailed** |
| `ruff check` / `ruff format --check` on the 11 Python files this pass changed | clean |
| `bash -n` on every ```bash block of the three documents | 43 blocks, 0 errors |
| Runbook step 5 (its generator, extracted verbatim) on a copy of the template → domain `sed` → placeholder `grep` → SMTP fill → step 6's extraction → `check --deploy` under `config.settings.prod` with that file's variables only | `grep`: exactly the four SMTP lines, then none; password 43 characters, URL-safe; key 86, salt 64; `security.W005` + `security.W021` (exit 1); both HSTS on: no issues (exit 0); an HSTS line deleted: refused |
| The embedded `ile-backup` and `backup-offsite` against the files exercised | byte-identical |

Scratch objects removed: the probe roles and databases, `ile_devops_bkp`, the restore database, the scratch storage,
the key ring. `test_ile_devops` (this lane's pytest database) remains.

**Not exercised here (Windows, no server, no download):** systemd (`systemd-analyze verify` of the backup units),
nginx (`nginx -t`, the maintenance page, the `/backoffice/login/` redirect), certbot, `runuser`, rsync over SSH, a
3.12 interpreter. The runbook says how to check each on the server.

**Still open — not this lane's to close**
- A-13's code fix (accounts): the nginx redirect is a mitigation, not the fix.
- F-6's template fix; the suite on Python 3.12 (A-26); the owner's decisions of the list above, now with the backup's
  destination, key holder and retention made concrete (runbook step 10, A-28).
- CI installs `requirements/dev.txt` without the constraints, so CI may run newer transitive versions than the server
  will. Installing with `-c requirements/constraints.txt` there would close that (the steward's file).
- Optional: a `<3>`/`<4>` prefix on the structured formatter's error lines would make `journalctl -p` meaningful too;
  the content checks do not need it.

## At the merge (the steward, 12 October 2026)

The steward's merge step (`devops-merge`) synced design-v5 into this branch (`e3291a8`: W2-A, W3-F2, W2-C2 and the
documentation commit `3780a7c` came in, without a conflict). Two consequences, both resolved on this branch:

- **F-6 is closed — by W3-F2, not by a template fix.** W3-F2 draws the 400 and 500 pages without the request
  (`core.views._self_sufficient`, merged in `9af0e1a`), so the 400 page no longer asks for the host.
  `test_a_request_for_an_unknown_host_gets_the_400_page` turned XPASS(strict) on the synced branch and passed with
  `--runxfail`; the marker is gone and the test now also checks that the page leaks nothing. Checklist A-21, the
  runbook's catch-all paragraph (step 11) and its «Known limits» say so; the catch-all server stays (scanners' noise,
  one `DisallowedHost` line each). Open question 12 above is moot.
- **The completeness rule caught the V5 families' new test variables**: `W3F2_SHOTS` (W3-F2's browser tests),
  `ILE_OVERLAY_SMOKE_ENGINES` and `PLAYWRIGHT_BROWSERS_PATH` (W2-A's overlay smoke test) are documented in the
  NOT FOR PRODUCTION section of `.env.example`; `LOCALAPPDATA`, Windows' own (read by the same test), joins
  `SELF_SET`.

After both: `pytest tests/deployment tests/test_env_example_is_complete.py
tests/security/test_production_settings_refuse_to_start.py` — 98 passed (before the sync: 97 passed, 1 xfailed).
The merge, this family's entry in the ownership manifest and the steward's tests are recorded in
`docs/design-v5/DECISION_LOG_V54.md` (the devops merge's entry).

## Second pass (16 Oct)

Lane `devops2-fix`, branch `v54-devops-2` (worktree `C:/tmp/ile_wt/v54-devops-2`, created from `design-v5` at
`8ab5b89`), 16 October 2026. Brief: four items handed on by integration checkpoint 3's review
(`QA/v54/intfix/REVIEW.md`, «outside this branch») and by gates 2–4 (N-4, then N-G), each reproduced first — a failing
test or a measured probe — then fixed, then proved.

**Hard limits kept.** Nothing deployed; no server, DNS record, domain or certificate touched or contacted; no
production host named. No package installed, nothing downloaded. No secret in any file: the «production» values of the
probes are the throwaway placeholders `tests/deployment` already uses, and the probes, settings and captures lived in a
scratch directory outside the repository. One pytest at a time, on `ile_v5_l9` (its test database `test_ile_v5_l9`),
`-p no:randomly`, never the full suite. The lane server ran on 127.0.0.1:8789 against `ile_v5_l9` only — never 8780,
never `ile_v5` — and is stopped; the five sessions the browser proof opened for `qa-doc-person` (forced, no password
typed) were ended by its sign-out, the first deleted (none left: checked). Other teams' files untouched: W3-E (the console's templates and CSS), W4-B
(`static/js/src/**`, the JS dist), sec-f7 (`apps/cases`). The ownership manifest is the steward's: the paths this pass
adds to the family are listed at the end.

### 1. Stale scripts after a release — fixed

**Root cause.** `config/settings/base.py` set `WHITENOISE_MAX_AGE = 31536000` at the bootstrap (17 September). WhiteNoise
serves a name it recognises as hashed (through the manifest) `max-age=315360000, public, immutable` whatever that says,
and every other name `max-age=<WHITENOISE_MAX_AGE>, public`. The templates link hashed names, but the bundles of
`static/js/dist` are ES modules that import one another by relative specifiers, and the manifest storage rewrites a
stylesheet's `url()` and `@import`, never a script's import: from a hashed entry the browser went on to request the
chunks and the on-demand entries under their plain names — a year of cache on a URL whose content changes at the next
release.

**The facts, measured** on a real `collectstatic` under `config.settings.prod` (the runbook's environment, DEBUG off)
into an empty temporary `STATIC_ROOT`: exit 0, 615 files copied, 1 449 post-processed — DL54-44's failure of 10 October
(W1-D's console entry) is gone (DL54-77). Then the import graph followed from the templates' 31 entries (their hashed
copies, as the browser receives them), each URL asked of WhiteNoise under the production settings: **48 files, 10 of
them plain names served `max-age=31536000, public`** — the seven esbuild chunks (`chunk-ESWNIYP5`, `-MFQVK52T`,
`-MVEBZ5U4`, `-OAT2KRBG`, `-OYVDETPU`, `-T6TU3QHP`, `extras-MMO4GKTU`) and the three entries imported on demand,
`loader.js` (from `shell.js`, `piece-drawer.js` and `chunk-T6TU3QHP`), `depot.js` and `piece-drawer.js` (from
`console.js`). The same in Chromium, on the lane server with the production settings (only what plain HTTP on loopback
needs relaxed), home → console → `/documents/` → `/documents/upload/` → sign-out: 41 `/static/` requests, the same 10
plain — the home's five chunks, `chunk-T6TU3QHP`, `extras-…` and `piece-drawer.js` on `/documents/`, `depot.js` and
`loader.js` on the depot page.

**Fix.** `apps/core/storage.py` — `CompressedManifestModulesStorage`, WhiteNoise's `CompressedManifestStaticFilesStorage`
with Django's `support_js_module_import_aggregation`: `import … from "…"`, `export … from "…"`, `import "…"` and
`import("…")` rewritten to the hashed names, as `url()` is — `base.py`'s `STORAGES` names it. And `WHITENOISE_MAX_AGE =
60`: a plain name — the original copy collectstatic keeps beside each hashed one, linked by no page now — is revalidated
after a minute. Why this one, of the brief's three:

- a short max-age alone leaves the module names plain: a minute of staleness instead of a year, but a page opened before
  a release still imports the next release's `loader.js` into its old shell, and every chunk is revalidated on every
  visit;
- content-hashed entry names belong to the build (`scripts/build_frontend.mjs`, `package.json`: W4-B's and the
  steward's files) and to the templates, and Django would hash those names again;
- the rewriting makes every file a page loads a hashed, immutable name, and one page load one release (the files of the
  previous release stay collected: never `--clear`). The short max-age stays behind it, for whatever would escape it.

What it asks, written in `core/storage.py` and the runbook's known limits: literal specifiers (a computed `import(x)`
cannot be rewritten — the test refuses one in a module a page loads) and an acyclic module graph (a cycle has no hash
fixed point: collectstatic stops with «Max post-process passes exceeded», at build time, in CI). Today's dist needed
3 of the 5 extra passes Django allows. nginx serves no `/static/` (runbook step 11, held by a test): WhiteNoise makes the
distinction; the runbook says what an nginx `location /static/` would have to do to keep it.

**Proof.**

| Check | Before | After |
|---|---|---|
| `tests/deployment/test_static_caching.py` — collectstatic under the production settings from an empty root; the graph walked from every `{% static %}` of every template (71 files with the design pages); every import of the 19 modules of `static/js/dist` (50 specifiers, 6 of them dynamic) the hashed name it resolves to; plain names ≤ 300 s | 3 of 4 fail: «10 of the 71 files … a plain name, «max-age=31536000, public»»; every specifier «served as './chunks/chunk-….js', not as the hashed …»; «31536000 > 300» | 4 passed |
| The probe (48 files from the 31 non-design entries) | 10 plain, `max-age=31536000, public` | 48 hashed, `max-age=315360000, public, immutable` |
| Chromium on the lane server, the same walk | 41 requests, 10 plain, a year | 41 requests, 0 plain, 0 not 200, 0 not immutable, 0 JS errors; the depot page itself requested `depot.c34d82a16457.js` and `loader.0b99e21f3c13.js`; `import()` of the rewritten loader specifier from the page: its 14 exports |
| The rewritten text | — | only `}from"` → `} from "` (Django's template) and the URL; nothing else of the minified code changes (diffed on five modules) |
| `tests/frontend/test_static_pipeline.py`, `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py` | — | 11 passed (the steward's collectstatic runs base.py's storage, now this one) |

`support_js_module_import_aggregation` reaches every `.js` collected, not only the dist: on the full tree it changed
exactly 18 of the 19 modules of `static/js/dist` (the nineteenth imports nothing) and 11 sources of `static/js/src`,
collected as they always were (their relative imports; a bare `"motion"` is left alone) — no third-party file: the
admin's and Unfold's scripts hash as before. A future dependency whose script names a module that does
not exist would stop collectstatic loudly — never a silent change: a match is rewritten only to the hashed copy of the
file it names.

### 2. The NUL-byte 500 — fixed

**Where it first broke** (probe through the test client, DEBUG off, 16 October): PostgreSQL refuses a NUL in text and
psycopg raises `DataError` before the query leaves; in a jsonb value, «unsupported Unicode escape sequence».

| Vector | Before | After |
|---|---|---|
| path `/fr/nothing%00here/` (also `/fr/%00/`, `/%00`, `/fr/glossaire/a%00b/`, `/static/js/dist/loader.js%00`) | 500, ERROR + traceback: the 404 rendered, then `cms/middleware.py:52` → `:75` `lookup_redirect` | 400, one WARNING «Bad Request: /fr/nothing\x00here/» |
| query string `/fr/actualites/?categorie=%00` | 500: the view, `news/views.py:62` → `news/services.py:51 category_by_slug` | 400 |
| query string read by no view (`/fr/?x=%00`, `/?lang=%00`) | 200 / 302 | 400 |
| form field read without a form: a case file's transition, NUL in its reason | 500: `cases/views.py:211` → `cases/services.py:155` → `audit/services.py:47 record` (jsonb) | 400 |
| form field through a Django form (the sign-in) | 200, the form's message (`ProhibitNullCharactersValidator`) | 400 |
| session cookie `sessionid="\000abcdefgh"` — found on the way: Python's cookie parser decodes the octal escape | 500: the session lookup | 400 |
| CSRF or language cookie with a NUL | 200 (sanitised, ignored) | 200, untouched |

**Fix.** `cms.middleware.NulByteMiddleware`, listed after `RequestIDMiddleware` and `LocaleMiddleware` (the page carries
the request id and the visitor's language: `/ar/…%00` answers in Arabic, `dir="rtl"`), before CommonMiddleware, CSRF,
the session's readers, the views and the redirect lookup. It looks at the decoded path, the raw query string (`%00` or
the byte: parsing it would raise TooManyFieldsSent on a page that never reads its query), the session cookie, and a
POST's form fields through `request.POST` (CsrfViewMiddleware parses it a few steps on anyway; an unreadable body is left
to CSRF, which answers it as before). It never reads a file's bytes — a document holds NUL by nature and lives in
`request.FILES` — nor a body that is not a form (the integrations API's JSON, behind its key: its view's). It returns the
URLconf's `handler400` (W3-F2's self-sufficient page) instead of raising a SuspiciousOperation, which Django logs at
ERROR with its traceback: a returned 400 is one WARNING line, the path escaped. `lookup_redirect` skips a NUL path as a
second layer. In `cms/middleware.py`, the file the brief named; `core.middleware` would be the other natural home, should
the steward prefer it.

**Proof.** `tests/deployment/test_nul_bytes.py`: 15 of 17 failed before (every vector a 500 with an ERROR record), 17
passed after — the path (5), the query string (4), a form field (urlencoded, a NUL in a field's name, multipart beside a
file) through the stand-in view of `tests/deployment/nul_urls.py` (it looks the field up, as the views that store a
posted value do — independent of sec-f7's in-flight `apps/cases`), the public sign-in form, the session cookie, the
page's language, a file holding NUL bytes never refused (200), requests without NUL untouched (`%2500` is three
characters), the lookup's second layer (0 queries), the guard's place in the chain. The probe's eighteen vectors after:
every NUL vector 400 with one WARNING and no traceback.

### 3. collectstatic and the deploy checks — no new warning since DL54-121

`collectstatic --noinput` under `config.settings.prod`, empty `STATIC_ROOT`, the final code: exit 0, «615 static files
copied …, 1449 post-processed», manifest 615 entries (the 19 modules of `static/js/dist` hashed), 834 `.gz`.

`check --deploy --fail-level WARNING` under `config.settings.prod` with the runbook's environment (the placeholders of
`tests/deployment/test_production_checks.py`, `DATABASE_URL` on `ile_v5_l9`):

```
=== template HSTS (0/0)
SystemCheckError: System check identified some issues:

WARNINGS:
?: (security.W005) You have not set the SECURE_HSTS_INCLUDE_SUBDOMAINS setting to True. […]
?: (security.W021) You have not set the SECURE_HSTS_PRELOAD setting to True. […]

System check identified 2 issues (0 silenced).
exit 1

=== HSTS fully on (1/1)
System check identified no issues (0 silenced).
exit 0
```

Exactly DL54-121's: W005 and W021 while the template keeps both HSTS directives off, nothing with both on; the new
storage and middleware add none. `manage.py check`: no issues; `makemigrations --check --dry-run`: «No changes
detected».

### 4. The browser suite's port flake — fixed

**Root cause, measured.** pytest-django's `live_server` binds port 0: the operating system chooses. This workstation's
dynamic range is 1024 + 64 511 (`netsh int ipv4 show dynamicport tcp`), and Windows hands those ports out in sequence
(2 000 binds to port 0 on 127.0.0.1: 46 145 … 48 148, consecutive), so when the sequence passes the low thousands a live
server lands wherever it is. Asked of the installed Chromium (Playwright's, 153) for every port from 1024 to 32767 but
the 23 where something listened: it refuses **17** before connecting (`net::ERR_UNSAFE_PORT`) — 1719, 1720, 1723, 2049,
3659, 4045, 5060, 5061, 6000, 6566, 6665–6669, 6697, 10080 — and none above 10080 (4190 and 6679, on some published lists,
it opens). Reproduced: `--liveserver localhost:4045` → «Page.goto: net::ERR_UNSAFE_PORT at
http://localhost:4045/fr/espace-reserve/mes-demandes/».

**Fix.** `tests/live_server.py`, imported by the root `conftest.py` (so it holds for `tests/` and every `apps/*/tests`):
a `live_server` fixture that is pytest-django's — the same `LiveServer` object, the same settings handling — whose
thread draws the port with `SystemRandom` from 20000–32767 (above every refusal, below the default dynamic ranges of
Linux, 32768–60999, and Windows, 49152–65535; this machine's Hyper-V exclusions include 29992–30091, inside it — a bind
there fails with WSAEACCES and the next port is drawn: corrected after REVIEW_2 n3) and binds it: the bind is
the test of freedom, so there is no window between choosing and using, and a port that is taken — another lane, an
outgoing connection, a reservation — is skipped for the next draw (50 at most, then the error). Nothing is fixed, so two
lanes never share a port. A `--liveserver` address or `DJANGO_LIVE_TEST_SERVER_ADDRESS` that names a port is honoured
exactly (now documented in `.env.example`). A summary line names the port a run used — and says so when a given port is
one Chromium refuses.

**Proof.** `tests/test_live_server.py`, 7 passed: 500 draws all in range and clear of the 17; a taken port skipped for the
next; every draw taken → an `OSError`, never a shared port; a named port honoured; the summary line; the fixture on a
drawn port answering `/healthz/`; Chromium opening that port and refusing 4045 (marker `browser`). The browser files the
brief named, `tests/frontend/test_overlays_console_browser_w2_a.py` + `apps/portal/tests/test_browser.py`: **23 passed**
(3 min 15 s), «live server: http://localhost:27844 (a port drawn …)». Chromium answered no refusal on any of the
12 765 ports of the range it was asked (three were listening).

### Commands run on the final files

| Command | Result |
|---|---|
| `pytest tests/deployment apps/cms tests/frontend/test_static_pipeline.py tests/frontend/test_css_bundle_is_current.py tests/frontend/test_frontend_bundle_is_current.py tests/test_env_example_is_complete.py tests/test_live_server.py -p no:randomly` | **153 passed** — `tests/deployment` 76 (22 new: 4 + 17 + 1), `apps/cms` 45, the static pipeline and bundles 11, the environment template 14, the live server 7 |
| `pytest tests/security -p no:randomly -rs` (the confidential-material test with its sentinels, from the local environment) | **157 passed**, 0 skipped |
| `pytest tests/frontend/test_design_docs.py` | 40 passed |
| `pytest tests/test_env_example_is_complete.py`, before `DJANGO_LIVE_TEST_SERVER_ADDRESS` was documented | 1 failed («read by the code but absent from .env.example»), then 14 passed |
| `pytest tests/frontend/test_overlays_console_browser_w2_a.py apps/portal/tests/test_browser.py` | 23 passed |
| `manage.py check` · `makemigrations --check --dry-run` | no issues · «No changes detected» |
| `ruff check .` · `ruff format --check` on the changed Python files | clean |
| `bash -n` on every ```bash block of the three documents | 43 blocks, 0 errors |
| `git merge-tree --write-tree design-v5 HEAD` (design-v5 at `11070b5`, after the sec-f7 merge) | no conflict |

Commits of this pass, on `v54-devops-2`: `d62d256` item 1 (storage, max-age, test) · `fabc2d9` item 2 (guard, tests) ·
`7785a2b` runbook, checklist and their test · `06397fb` item 4 (live server, tests) · `bfde9e2` `.env.example` ·
`2c08123` the static probe never reads a database (`DATABASE_URL` at a dead address; 4 passed again) · `b3eac59` and
this commit, these notes.

### For the steward

`scripts/check_ownership.py devops design-v5`: 13 paths — 6 inside, 2 slice, **5 outside** → FAIL until the manifest
assigns them (the manifest is the steward's file; 14 paths and 7 inside once `REVIEW_2.md` was committed — REVIEW_2 n4;
16 after the review fixes, «Second pass — review fixes» below). Proposed entries for the family «devops»:

| Path | Whole or slice | Source |
|---|---|---|
| `apps/core/storage.py` | whole | second pass, item 1 |
| `config/settings/base.py` | slice, extended: `STORAGES["staticfiles"]` and its comment, `WHITENOISE_MAX_AGE` and its comment, the `cms.middleware.NulByteMiddleware` entry of `MIDDLEWARE` and its comment | items 1 and 2 |
| `apps/cms/middleware.py` | slice: the module docstring's last paragraph, `NUL`, `NulByteMiddleware`, `lookup_redirect`'s NUL lines, their imports | item 2 |
| `conftest.py` (root) | slice: the docstring's live-server paragraph and the import of `tests.live_server` | item 4 |
| `tests/live_server.py`, `tests/test_live_server.py` | whole | item 4 |

Already the family's: `docs/deployment/**`, `tests/deployment/**` (two new tests and `nul_urls.py`), `.env.example`'s
NOT FOR PRODUCTION section.

### Open, not this lane's to close

- **W4-B's dist** (Motion removed) is not on design-v5 yet: `tests/deployment/test_static_caching.py` walks whatever
  dist is collected, so the merge that brings it runs the proof again — a cycle or a computed import there fails it, with
  the file named.
- **JSON bodies** with a NUL (the integrations API, behind its key) are left to their view; a probe there was not run.
- Not exercised: nginx, Gunicorn, a server (Windows workstation); the browser suite as a whole (the brief: never the full
  suite) — the two files above and the new browser test ran.

## Second pass — review fixes

Lane `devops2-fix2`, branch `v54-devops-2` (worktree `C:/tmp/ile_wt/v54-devops-2`), 16 October 2026, on `4849b06`.
Brief: `REVIEW_2.md` — SHIP_AFTER_FIXES, one major, six minors, four nits. **The major and the six minors are fixed,
each held by a test that fails before the fix; the four nits too.** m4's last step — the design preview's `_runserver`
calling the new helper — is one line in W1-P's file, left to the steward (below). One more red, found on the way, is
fixed: the design preview's landing test, broken by the guard since `fabc2d9`.

**Hard limits kept.** Nothing deployed; no server, DNS record, domain or certificate touched or contacted; no production
host named — the added lines hold no IPv4 address but 127.0.0.1, no host name, no secret-like token (scanned). No
package installed, nothing downloaded. One pytest at a time on `test_ile_v5_l9`, `-p no:randomly`, never the full suite;
no lane server was needed. Scratch probes and settings lived in the session's scratch directory, outside the repository.
Other teams' files untouched: `git diff --stat design-v5...HEAD -- static/ templates/ apps/cases apps/portal` is empty.
One file outside the family's paths changed, for the red above: `tests/frontend/test_design_preview.py` (W1-P's).

| Finding | Change | Evidence |
|---|---|---|
| **M1** the guard read every POST's form: a multipart POST to the public webhook was a 500 | `cms.middleware.NulByteMiddleware`: the path, the query string and the session cookie stay in `__call__`, before every reader; a POST's form moves to `process_view` — the chain's first `process_view`, one step before `CsrfViewMiddleware.process_view` reads the same form — and is never read for a `csrf_exempt` view (the integrations API and the public webhook read their raw body; no such view stores a posted field). The review's prototype, plus the next row | `test_the_public_webhook_still_reads_its_body_after_a_multipart_post` (500 before, 401 after, no ERROR record); `test_a_csrf_exempt_view_keeps_its_raw_body_nul_or_not` (a csrf_exempt stand-in in `nul_urls.py`: 400 before, 200 after). The review's 34-vector probe (`review/test_nul_review.py`) run against this tree: 34 passed, every status equal to the review's «proposed» column, no ERROR record, CSP, X-Frame-Options and Permissions-Policy on every 400 |
| **m1** TooManyFieldsSent on the webhook — and, found here, on every protected form | The same move frees the webhook. Beyond the prototype: a body Django will not parse (`UNPARSABLE`: `UnreadablePostError`, `MultiPartParserError`, `SuspiciousOperation` — TooManyFieldsSent, TooManyFilesSent, RequestDataTooBig —, `BadRequest`) is not the guard's to answer: `process_view` returns `None` and the next reader answers as without the guard. With the prototype alone, the sign-in form still answered a 250-field POST 400 with TooManyFieldsSent's ERROR line, for anyone without a CSRF cookie — CSRF answers 403 without reading the body | `test_a_webhook_body_of_more_fields_than_django_parses_is_still_the_webhook_s` (400 + ERROR before, 401 after); `test_a_body_django_will_not_parse_is_answered_as_without_the_guard[urlencoded, multipart]` (the sign-in with CSRF enforced: 400 + ERROR before, 403 after) |
| **m2** the guard's 400 had no CSP, X-Frame-Options or Permissions-Policy | `config/settings/base.py`: `XFrameOptionsMiddleware`, `CSPMiddleware`, `BackofficeCSPMiddleware` and `ExtraSecurityHeadersMiddleware` right after `TextGZipMiddleware`, their order kept (django-csp below the gzip layer; the back office's relaxation after django-csp, so it runs first on the way out). Response hooks only; no template or code reads `request.csp_nonce`; more responses carry the headers, none fewer (the legacy 410s and the redirects now too) | `test_the_400_carries_the_security_headers_of_every_page`: the 400 answering a NUL in the path, the query string, the session cookie and a form carries the eight security headers of `/fr/`, with the same values (before: CSP, X-Frame-Options, Permissions-Policy, CORP and X-Permitted-Cross-Domain-Policies absent); the order test extended. The design preview's chain test (its frame exception listed after django-csp and X-Frame-Options) passes |
| **m3** «Max post-process passes exceeded» is not only a cycle, and the passes follow the directory order | `core.storage`: Django's four module patterns on `static/js/dist` only — `MODULES = r"js[/\]dist[/\]*.js"`, because collectstatic's paths are `os.path.join`'s, a backslash on Windows — and `support_js_module_import_aggregation` off. The worst chain was `js/src/console.js → piece-drawer → depot → loader`, sources no page loads: worst case 3 → 2 of the 4 passes a name may take. The three sentences corrected (`core/storage.py`, runbook step 8, Known limits) | `test_no_directory_order_asks_django_for_more_passes_than_it_runs` computes the worst case over every directory order from the finders' files and the storage's own patterns, no collectstatic, in milliseconds: 2 (3 under the second pass's storage; W4-B's dist alone, by the review's script: 2). The model checked against the review's real collectstatic: `test_the_model_of_the_passes_agrees_with_django_on_a_chain_of_modules` — seven modules in one directory 5 > 4 (the review's run failed), six 4, down the directories 0, a cycle never |
| **m4** the design preview's `dev_server` binds port 0 | `tests/live_server.py`: `bind_a_port_chromium_accepts(bind)` — draw, bind, the next draw on a taken or reserved port, the last error rather than a shared port — now used by the live server's thread, ready for `_runserver`. Measured on the way: two of Django's `WSGIServer`s with their default `allow_reuse_address=True` bind one port on Windows, so the caller passes `False`, as Django's live server does. Not done: the call in `_runserver` | `test_a_server_built_outside_live_server_binds_a_port_chromium_accepts`, `test_the_helper_skips_a_taken_port_and_never_shares_one`; the seven earlier live-server tests; 23 browser tests in Chromium on a drawn port (27680) |
| **m5** no test collected twice into one root | `test_a_release_collected_over_the_previous_one_renames_what_changed_and_keeps_the_previous`: the bundles of `static/js/dist` alone (a copy), the production settings, a collect; `loader.js` changed in place with a later mtime; a second collect into the same root, no `--clear` | renamed: exactly `loader.js` and its five importers (`chunk-T6TU3QHP`, `depot`, `piece-drawer`, `shell`, `console`); every file of release N and its `.gz`, byte for byte; each release's graph holds its own hashed names only. Under the merge base's storage it fails: `loader.js` alone renamed |
| **m6** the rewriting read every collected script | The restriction of m3. And a fast check of everything the storage rewrites | `test_the_module_patterns_read_the_bundles_of_static_js_dist_only` (the 19 bundles and nothing else, both separators); `test_no_script_outside_static_js_dist_is_rewritten_by_the_module_patterns` (the real collect: the 11 sources of `js/src` rewritten before, none after, no third-party script); `test_every_reference_the_storage_rewrites_names_a_collected_file` (none unresolved). The dist itself is unchanged: both storages collected and compared, the 19 bundles have the same names and the same bytes as under the second pass's storage, which Chromium imported in the review |
| **n1** behind nginx a NUL in the path never reaches Django | Checklist D-10: the path line says the 400 is nginx's own; the query line greps the project's page (`class="container error-page"` → 1). A-21 and the runbook's Known limits say which layer answers which | `test_the_smoke_test_proves_the_nul_guard_where_nginx_lets_a_nul_through` (fails on the previous checklist) |
| **n2** a previous release's hashed names are served `max-age=60` | Step 11 and the static table: `immutable` for a name of the current release; a plain name, or a previous release's hashed name, 60 s — its content never changes | read |
| **n3** «outside this machine's Hyper-V exclusions» | §4 corrected: 29992–30091 lies inside the range (`netsh int ipv4 show excludedportrange protocol=tcp`, read again); a bind there fails with WSAEACCES and the next port is drawn — the helper's docstring says so | read |
| **n4** the steward's counts | corrected in place; the final counts below | `check_ownership.py` |

**Found on the way — fixed.** `test_the_landing_never_frames_what_is_not_a_page_of_this_site[/fr/\x00]`
(`tests/frontend/test_design_preview.py`) had failed on this branch since the guard (`fabc2d9`): the landing's
`?page=/fr/%00` is the product's 400 before the landing reads it, not the preview's own sealed page. Neither the second
pass nor its review ran the design preview's tests. Checked on `4849b06` (fails), then fixed in the test: the NUL case
is now `test_a_nul_byte_never_reaches_the_landing` (400, the project's page, nothing framed, nothing of the preview
named); the preview's validator keeps its control-character case (`"/fr/ x"`). Every test was searched for `\x00`,
`%00`, `\0` and `\u0000`: no other request carries a NUL (the rest are file bytes and unit tests of sanitisers).

**A body Django will not parse, probed** (scratch harness, test client, DEBUG off): a NUL form posted to an unknown
URL → 404 (nothing reads the form); a malformed multipart body, or 120 files, to the sign-in → 403 with CSRF enforced,
200 without (the view finds no field); an urlencoded body declared latin-1 → 403 enforced, 400 and a WARNING without
(the view's own parse, as before the guard); a PUT with a NUL → 200 (never parsed). No ERROR record in any. One
difference with `design-v5` stays, by design: a multipart body Django refuses, from a client holding a CSRF cookie, now
meets CSRF with the fields the failed parse left empty — 403 «CSRF token missing» instead of the 400 it had (with an
ERROR line for the limits). The failed parse consumed the stream; the site's upload forms send one file each, and its
text fields stay far below the 5 MB of `DATA_UPLOAD_MAX_MEMORY_SIZE`.

**Commands run on the final files**

| Command | Result |
|---|---|
| `pytest tests/deployment apps/cms tests/frontend/test_static_pipeline.py tests/frontend/test_css_bundle_is_current.py tests/frontend/test_frontend_bundle_is_current.py tests/test_env_example_is_complete.py tests/test_live_server.py -p no:randomly` | **168 passed** — the NOTES' set, 153 + 15 new (NUL bytes 6, static caching 6, runbook 1, live server 2) |
| `pytest tests/security -p no:randomly -rs` (the confidential-material test with its sentinels) | **157 passed**, 0 skipped |
| `pytest apps/integrations apps/core tests/backoffice/test_backoffice.py tests/compliance/test_public_pages.py apps/documents/tests/test_download.py apps/accounts tests/frontend/test_layout.py tests/frontend/test_429_w2_b.py tests/i18n/test_routing.py tests/frontend/test_design_docs.py -m "not browser" -p no:randomly` | **366 passed** — what the new middleware order reaches: MFA, layout, 429, routing, public pages, downloads, the API |
| `pytest tests/frontend/test_design_preview.py -m "not browser" -p no:randomly` | **297 passed** (1 failed before the landing test's fix) |
| `pytest tests/frontend/test_overlays_console_browser_w2_a.py apps/portal/tests/test_browser.py -p no:randomly` | **23 passed** in Chromium, the live server on a drawn port |
| The review's NUL probe (34 vectors) against this tree | 34 passed; every status the review's «proposed» one |
| collectstatic under the production settings with each storage, compared | 615 files copied, 1 449 post-processed, both; 11 names differ, all in `js/src`; `js/dist`: same names, same bytes |
| `check --deploy --fail-level WARNING` under `config.settings.prod`, the runbook's placeholders, `DATABASE_URL` on `ile_v5_l9` | template HSTS: W005 and W021, exit 1; both on: «no issues», exit 0 — unchanged |
| `manage.py check` · `makemigrations --check --dry-run` | no issues · «No changes detected» |
| `ruff check .` · `ruff format --check` on the branch's changed Python files | clean |
| `bash -n` on every ```bash block of the three documents | 43 blocks, 0 errors |

Commits of this pass: `0596d94` the preview's landing test · `056bacc` the guard (M1, m1) and the header writers (m2) ·
`36b65ea` the storage and its tests (m3, m5, m6) · `926be59` the port helper (m4) · `12fa21c` runbook and checklist
(m3, m6, n1, n2, M1, m2) · this commit (n3, n4, this section). The message of `36b65ea` says «each new test failing on
the storage it replaces»: true of the m5 and m6 tests; the worst-case and unresolved-reference checks pass under both
storages — they hold what comes next.

### For the steward (review fixes)

`scripts/check_ownership.py devops design-v5`: **16 paths — 8 inside, 2 slice, 6 outside** → FAIL until the manifest
assigns them: the five of the second pass («For the steward» above) and the design preview's test.

| Path | Whole or slice | Source |
|---|---|---|
| `config/settings/base.py` | slice, extended again: the four header middlewares' place right after `TextGZipMiddleware` and their comment — besides `STORAGES["staticfiles"]`, `WHITENOISE_MAX_AGE` and the guard's entry (above) | m2 |
| `apps/cms/middleware.py` | slice (above), now with `UNPARSABLE`, `process_view` and the docstring's paragraphs on them | M1, m1 |
| `apps/core/storage.py`, `tests/live_server.py`, `tests/test_live_server.py` | whole (above) — now with `MODULES` and `bind_a_port_chromium_accepts` | m3, m4, m6 |
| `tests/frontend/test_design_preview.py` | slice: `test_a_nul_byte_never_reaches_the_landing` and the `"/fr/\x00"` case it replaces in `test_the_landing_never_frames_what_is_not_a_page_of_this_site`; the file stays W1-P's | the guard's red, found here |

m4, for W1-P or the steward: in `_runserver` (`tests/frontend/test_design_preview.py`), build the server through
`tests.live_server.bind_a_port_chromium_accepts(lambda port: server_class(("127.0.0.1", port), WSGIRequestHandler,
allow_reuse_address=False))`, `server_class` being the `type("WSGIServer", (socketserver.ThreadingMixIn, WSGIServer),
{})` it builds today, instead of binding `("127.0.0.1", 0)`.

### Open, not this lane's to close

- m4's call in `_runserver` (above).
- The full suite and the browser suite as a whole (the brief: never the full suite): the steward's checkpoint.
- nginx, Gunicorn, a server: not run here (Windows workstation); the review measured nginx 1.24 in WSL.

## At the merge (the steward, 16 October 2026) — second pass

The steward's merge step (`devops2-merge`) on lane 9, under `C:/tmp/ile_locks/DESIGN_V5_MERGE_LOCK` — held by the W3-E
merge when the step began (06:12), taken at 06:42:48 once that merge had released it:
`TEST_DATABASE_URL=…/test_ile_v5_l9`, one pytest at a time, `-p no:randomly`; no lane server started, no persona used.
Nothing deployed, nothing pushed; no server, DNS record, domain or certificate touched or contacted. Logs:
`C:/tmp/ile_v5_council/evidence/v54/devops/merge-2/`.

- **The sync** (`53b9695`). design-v5 had moved from `8ab5b89` to `a833403`: 69 commits — the sec-f7 merge and its
  record DL54-132; `11070b5`, this family's `tests/deployment/test_private_documents_are_never_served.py`, fixed by the
  orchestrator between the passes (GitHub's Linux runner could not create the runbook's private root, so the probe now
  asks the same storage class at the same root whether it hands out a URL); the W3-E merge, its rebuild, DL54-151 and
  its changelog line. `git merge --no-ff design-v5`: no conflict, and no path in common with this branch.
- **The bundles.** The merge brought stylesheet sources (W3-E's sheets) and `static/js/src/console.js`, so both dist
  trees were deleted and rebuilt from clean (`npm run build`; `node_modules` a junction to design-v5's):
  `static/css/dist` byte for byte the committed tree; `static/js/dist` identical once esbuild's chunk names are read as
  one (12 entries, 7 chunks; the names follow the worktree). design-v5's committed tree kept (`git checkout`), so the
  merge brings no bundle. This family changes no stylesheet and no script: V5.8's shared CSS payload is not concerned.
- **REVIEW_2 m4's last step** (`4b56576`, the lane's hand-over to the steward): the design preview's `_runserver` builds
  its server through `tests.live_server.bind_a_port_chromium_accepts`, with `allow_reuse_address=False`, where it bound
  `("127.0.0.1", 0)` — one helper call and its comment in W1-P's file, the recipe of the lane's notes and the review.
  The dev-server outage, slot and SO_LINGER tests build their server there: `test_design_preview.py -m "not browser"`,
  297 passed before and after the sync; its 17 browser tests below.
- **Ownership** (`5a8415a`). The family keeps its id and DL54-01's branch name in the manifest; its note names the
  second branch. `base.py`'s slice extended (`STORAGES["staticfiles"]`, `WHITENOISE_MAX_AGE`, the four security-header
  middlewares' place right after `TextGZipMiddleware`, the guard's entry) and six entries added — whole:
  `apps/core/storage.py`, `tests/live_server.py`, `tests/test_live_server.py`; slices: the guard in
  `apps/cms/middleware.py` (`LegacyURLMiddleware` stays as it was, a file no family held), the root `conftest.py`'s
  docstring paragraph and import, the design preview's NUL test and `_runserver`'s port (the file stays W1-P's). Each
  slice read in the diff and staying inside it. `check_ownership.py devops design-v5`: 16 paths, 8 inside, 2 slice, 6
  outside → FAIL before; **16 paths, 11 inside, 5 slice → PASS** with the extended manifest, before its commit (after it
  the manifest joins the diff as the steward's own, steward-only path, as at the sec-f5 and sec-f7 merges);
  `--validate`: **29 families, 736 entries**.
- **Tests on the merged branch**:
  - the brief's list, with the live-server tests and the design preview's file (`-m "not browser"`): **719 passed** in 5
    min 56 s, no skip — `tests/deployment` 90, `tests/security` 157 (the confidential-material guard with its
    sentinels), `apps/cms` 45, `test_static_pipeline.py` 3, both bundle-currency tests 8, `test_design_docs.py` 40,
    `test_env_example_is_complete.py` 14, `tests/test_check_ownership.py` 57, `tests/test_live_server.py` 8,
    `test_design_preview.py` 297;
  - what the new middleware order reaches, with W3-E's pages, which meet it for the first time on this tree (`-m "not
    browser"`): **401 passed** in 8 min 03 s — `apps/integrations` 45, `apps/accounts` 189,
    `tests/backoffice/test_backoffice.py` 5, `tests/compliance/test_public_pages.py` 9,
    `apps/documents/tests/test_download.py` 12, `tests/frontend/test_layout.py` 29, `test_429_w2_b.py` 7,
    `tests/i18n/test_routing.py` 30, W3-E's `test_case_file_w3_e.py` 22, `apps/portal/tests/test_views.py` 35,
    `apps/helpdesk/tests/test_views.py` 18;
  - in Chromium, through the new live-server plumbing: **41 passed** in 3 min 40 s —
    `tests/frontend/test_overlays_console_browser_w2_a.py` 15 and `apps/portal/tests/test_browser.py` 8, on
    pytest-django's `live_server` through `tests/live_server.py` («live server: http://localhost:23662 (a port drawn by
    tests/live_server.py, which Chromium accepts)»); `tests/test_live_server.py`'s Chromium test 1 (a drawn port opened,
    4045 refused); the design preview's 17 (`dev_server` through `_runserver` and m4's helper, the archive's pages
    through `live_server`) — with another lane's browser suite running beside it;
  - `manage.py check`: no issue; `makemigrations --check --dry-run`: «No changes detected»; `ruff check .`: clean; `ruff
    format --check` on the family's 11 Python files: clean; `bash -n` on the three documents' 46 ```bash blocks: 0
    errors.
- **Scan.** The family's 2 189 added lines (`design-v5...HEAD` before this section: 17 paths, the manifest among them):
  no IPv4 address but 127.0.0.1, URLs on `localhost` only and one `https://<host…>` placeholder, `example.com` /
  `example.test` addresses only, no credential, secret-like assignment or high-entropy token, no production host,
  droplet name or live domain.

The merge itself is recorded in `docs/design-v5/DECISION_LOG_V54.md` (DL54-152). No tag, no restart of 8780, no change
to v5-live, no line in `CHANGELOG_V54.md` or `live_status.json` (devops is not a preview surface: DL54-77, DL54-121).
