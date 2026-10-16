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
