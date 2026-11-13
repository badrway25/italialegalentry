# DevOps readiness (directive V5.9) — runbook verification

Lane `devops-verify` (verifier: built nothing in the runbook), branch `v54-devops`, worktree `C:/tmp/ile_wt/v54-devops`,
verified at **`3de8c57`**, 12 October 2026. Brief: the owner's directive V5.9, read in full, with V5.8 (the legacy host
is LEGACY_REFERENCE_ONLY). Documents walked line by line: `docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md`,
`PRODUCTION_CHECKLIST.md`, `ROLLBACK.md`, and the two templates they rest on (`docs/deployment/production.env.example`,
`.env.example`).

**Hard limits kept.** No deployment; no connection to, resolution of or contact with any production host; no DNS, domain
or certificate operation; nothing installed or downloaded. The production server's address and droplet name appear in
no file of the worktree and in no commit of the branch (checked with the patterns piped from outside the repository,
never written down). Placeholder production values were generated at run time inside a scratch directory outside the
repository and deleted afterwards. SMTP pointed at a closed loopback port: nothing could leave the machine. Scratch
databases were created and dropped; no template, CSS, JS or other family's file was touched.

## Verdict: SHIP_AFTER_FIXES

The first-deployment path (runbook steps 1–14) holds on an empty server as far as it can be exercised without one:
every file, command, setting, variable, URL and test it cites exists under that exact name; nothing is used before the
step that creates it; every command that can run locally ran and behaved as written (`check --deploy`, `migrate` →
verify on an empty database, `collectstatic`, `seed_all`, the Site and EmailAddress one-liners, all seven timer
commands, the error pages with DEBUG off, the TOTP-enrolment redirect, the C-6 restore check). No P0: nothing exposes
private documents, carries a secret or names a production machine.

Three **major** findings, to fix before the owner relies on the procedures they sit in — none blocks the first
deployment itself — and thirteen **minor** ones.

| # | Sev. | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | major | runbook l. 496 | The "not scheduled" table says `companies_demo` and `rules_activate_demonstration` «refuse under the production settings». **`companies_demo` does not**: run under `config.settings.prod` on the scratch database it answered rc 0, «demonstration company created; 4 need(s) created», and its `--verified` flag (default **True**) marks the account's verification APPROVED. The command has no `demonstration_data_allowed()` guard (`apps/companies/management/commands/companies_demo.py` l. 155–160); `rules_activate_demonstration` does refuse (rc 1, CommandError). A false safety statement about invented records in production (V5.8). | Add the guard to `companies_demo` (companies lane), with the same refusal as `rules_activate_demonstration`. Until then the runbook row must say it has no guard and must never be run on the server. |
| 2 | major | runbook §15 l. 691–696 · ROLLBACK §1 l. 33–42 | **In-place update under a running service.** The tag is checked out and `pip install` runs while Gunicorn keeps serving (only the timers are stopped). Gunicorn loads the app in each worker after fork unless `--preload` (gunicorn 26.2 `workers/base.py` l. 137, `arbiter.py` l. 163–164) and the unit recycles workers (`--max-requests 1000`); Django's cached template loader reads any template a worker has not used yet from disk; each process keeps the static manifest it loaded. Until the restart, the site can render new templates with old code, look up new static names in the old manifest (ValueError → 500) or run new code against the old schema. The rollback path has the same shape. Derived from the code; not runnable here (no Gunicorn on Windows). | Stop `italylegalentry.socket italylegalentry.service` (and the timers) before the checkout and start them after `migrate`/`collectstatic` — a short maintenance window — or check each tag out into its own directory and switch a symlink, then restart. Same in ROLLBACK §1. |
| 3 | major | checklist §C l. 78–101 | **Personal data leaves the server unencrypted.** Only C-2 (configuration) is `gpg`-encrypted; C-1 (database dump) and C-3 (the identity-documents archive) are copied off-server by C-5 as plain files, against §B («encrypted») and C-3's own «same protection as the database». The first pre-cutover backup holds no real person yet; every later one does. | Encrypt `db-*.dump`, `private-*.tar.gz` (and `media-*`) before C-5, as C-2 does, passphrase kept off the server; run C-6 from the decrypted copy. |
| 4 | minor | ROLLBACK §3 l. 78, 92 | `ALTER DATABASE italylegalentry RENAME TO italylegalentry_failed_$TS` uses an unquoted identifier, so PostgreSQL folds `$TS` (`…T0300Z`) to lowercase; the later `dropdb "italylegalentry_failed_$TS"` quotes it and fails. **Exercised** on the local PostgreSQL 17: rename OK, then `dropdb: error: … database "…_20261012T0300Z" does not exist` (exit 1); the copy (personal data) stays. | Lowercase the timestamp (`date -u +%Y%m%dt%H%Mz`) or quote the identifier in both commands. |
| 5 | minor | ROLLBACK §3 l. 83 | «Then section 1's code steps» — section 1's block also restarts the service and starts the timers, before §3's own `migrate --check` and start. | Say «section 1's checkout, SHA test, `pip` and `collectstatic` lines only». |
| 6 | minor | ROLLBACK l. 17 | `git -C /srv/italylegalentry/app describe --tags` without `sudo`: the checkout belongs to root, and git ≥ 2.35.2 (Ubuntu 24.04 ships 2.43) refuses another user's repository («detected dubious ownership»). Every other git command of the three documents has `sudo`. Not exercised (no Linux host). | `sudo git -C … describe --tags`. |
| 7 | minor | `production.env.example` l. 1, 22 · `.env.example` l. 6 | Wrong step numbers: the environment file is runbook **step 5** (both templates say step 6); the database is created in **step 6** (the production template says step 5). Every other step/cutover/checklist reference of the documents, templates, settings and tests is right (checked one by one). | Correct the three numbers. |
| 8 | minor | checklist A-2 l. 25 | `git ls-remote … "refs/tags/<tag>"` prints the **tag object's** SHA for an annotated tag, not the commit of A-1 (13 of the project's 15 tags are annotated). **Exercised** on a local annotated tag: the pattern gave the tag object, `refs/tags/<tag>^{}` gave the commit. | Compare with `refs/tags/<tag>^{}` (or decide release tags are lightweight and say so). |
| 9 | minor | checklist A-5 l. 28 | «`check --deploy --fail-level WARNING` … (runbook values) → no issue». With the production template's values (`SECURE_HSTS_INCLUDE_SUBDOMAINS=0`, `SECURE_HSTS_PRELOAD=0`) it reports `security.W005` + `security.W021` and exits non-zero at that fail level (**exercised**); runbook step 7 says this correctly. | Align A-5 with step 7 (no issue other than W005/W021 while the HSTS inventory is pending), or name the variables the test overrides. |
| 10 | minor | runbook cutover step 7 l. 881–885 vs TLS l. 753–754 | The literal command (`-d "$ILE_DOMAIN"` only) drops the temporary host from the certificate while it is still in `server_name` and `DJANGO_ALLOWED_HOSTS` until step 8 — the TLS section says to keep it — and omits `www` when it is served. | Write the full name list in step 7: `-d "$ILE_DOMAIN"` [`-d "www.$ILE_DOMAIN"`] `-d "$ILE_STAGING_HOST"`. |
| 11 | minor | runbook cutover steps 5–6 l. 863–879 | Only `A` and `MX` are written down and checked. An existing `AAAA` (and `CAA`) on the apex or `www` is neither recorded for the rollback nor handled: if the old site has an `AAAA` and the droplet has no IPv6, IPv6 visitors stay on the old site and Let's Encrypt, which prefers IPv6, validates against the old host — step 7 fails. The TLS section's «A (and AAAA) records point at this droplet» is not carried into the steps. | Step 5: record `AAAA` and `CAA` too. Step 6: point `AAAA` at the droplet or remove it; check `CAA` allows `letsencrypt.org`. |
| 12 | minor | `.env.example` · `docker-compose.staging.yml` l. 5–6, 23, 46 | `POSTGRES_PASSWORD` is required by the staging stack the runbook names as the hatch's only user (`${POSTGRES_PASSWORD:?…}`, «from the git-ignored `.env`») and is absent from `.env.example`, which says it lists every variable read. `tests/test_env_example_is_complete.py` scans Python only. | Document it in the NOT FOR PRODUCTION section (commented out), or have the test read the compose files too. |
| 13 | minor | runbook l. 156, 692 · ROLLBACK l. 37 | `requirements/base.txt` pins the 9 direct packages (and `psycopg-binary` through psycopg's extra); the other 9 distributions of the 19-name closure (asgiref, sqlparse, cryptography, cffi, pycparser, fido2, qrcode, packaging, typing-extensions) resolve at install time against lower bounds only, so the server can get versions CI never ran, and a rollback's `pip install -r` does not restore the previous set. | A constraints file frozen from the CI environment, installed with `-c` in steps 4/15 and ROLLBACK §1 (a file, not a new package). |
| 14 | minor | runbook l. 388–389 | «about 100–150 MB each» is attributed to the staging measurement, but `docs/STAGING_PERFORMANCE.md` has no memory figure (only «gunicorn, 3 worker»). | Label it an estimate, or read it on the server (`systemctl status italylegalentry`). |
| 15 | minor | `production.env.example` l. 15–16, 25–26 · runbook l. 174–175 | The placeholders say «64 / 48 URL-safe random characters», but `secrets.token_urlsafe(n)` takes **bytes**: the runbook's generator produced 86 and 64 characters (**exercised**). Harmless (longer than required). | «64 / 48 random bytes, URL-safe». |
| 16 | minor | runbook l. 669–671 | «two kinds of path hold a short-lived token»: password-reset links are valid three days (Django's default `PASSWORD_RESET_TIMEOUT`, not overridden), and allauth's e-mail-confirmation keys (three days, `ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS`) are a third kind in the access log. The retention advice stands. | Name the three kinds and their lifetimes. |

## What was exercised, and what it returned

Production settings throughout (`config.settings.prod`; for `collectstatic` and the page probe a scratch module that
imports it and only moves `STATIC_ROOT` to a temporary folder — its name contains «prod», so `.env` stays ignored).
The environment was built **exactly as runbook step 5 builds it**: the template copied, the runbook's own Python
heredoc run on it, its `sed`, the SMTP placeholders filled as `sudoedit` would, then parsed the way systemd's
`EnvironmentFile=` reads those lines; only `DATABASE_URL`, `MEDIA_ROOT`, `PRIVATE_MEDIA_ROOT` pointed at scratch targets.

| Runbook / checklist | Command, as written | Result |
|---|---|---|
| all three documents | `bash -n` on every ```bash block | 37 blocks, 0 syntax errors |
| step 5 | the secret-generation heredoc · `sed s/<your-domain>/…/g` | both work; secrets 86 and 64 characters, ≥ 44 distinct |
| step 5 | the placeholder `grep` before / after the SMTP edit | lists exactly `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` / «no placeholder left» |
| step 6 | the `DB_PASSWORD` `sed` | extracts the 43-character generated password |
| prod.py refusal | the template installed and never filled | ImproperlyConfigured naming `DJANGO_SECRET_KEY, IP_HASH_SALT, DJANGO_ALLOWED_HOSTS, DJANGO_CSRF_TRUSTED_ORIGINS, EMAIL_HOST` |
| step 7 | `check --deploy` (template values) | exactly `security.W005` + `security.W021`, as the runbook says |
| A-5 | `check --deploy --fail-level WARNING`, HSTS directives at 1 | «System check identified no issues», exit 0 |
| A-5 | same with an `example.com` sender | `core.W003` added, as the step-7 table says |
| step 7 | `makemigrations --check --dry-run` (before and after migrate) | «No changes detected», exit 0 |
| step 6/7 | scratch database created `TEMPLATE template0`; `migrate --plan`; `migrate --check` | full plan printed; `--check` exit 1 before |
| step 7 | `migrate --noinput` · `migrate --check` · `showmigrations` | 21 s; exit 0; **71 applied, 0 pending** |
| step 8 | `collectstatic --noinput` (temporary `STATIC_ROOT`) | 571 copied, 1317 post-processed, manifest 571 entries, 746 `.gz`, `main.css` / `shell.js` hashed; three «duplicate destination» notices for `admin/js` (unfold over admin — harmless) |
| step 8 | `seed_all` | 30 seeds; `academy.demo_plan`, `helpdesk.demo`, `selection.chain` skipped; 15 photographs in `media/library/photos`; nothing in the private root |
| step 8 | the Site one-liner · `createsuperuser` · the EmailAddress one-liner, as written | all rc 0; EmailAddress `verified=True, primary=True` |
| step 10 | the seven timer commands, from the runbook's own JOBS block | all rc 0 (`sent=0 failed=0`, purges with `--apply` «APPLIED … 0», …) |
| step 10 | the dry runs; `rules_pending_review --strict`; `documents_scan_pending`; `deliver_outbound_events` | rc 0; 16 rules, **0 in force**; «DOCUMENT_SCANNER is not configured»; `transport=logging` |
| step 10 | `companies_demo --account <superuser>` · `rules_activate_demonstration` | **rc 0, company and 4 needs created** (finding 1) · rc 1, refused |
| step 12 | the mail-queue one-liner | `{}` |
| WSGI | `import config.wsgi` with the filled environment file (template paths) | `WSGIHandler`, `config.settings.prod`, DEBUG False, `.env` of the checkout ignored; WhiteNoise warns «No directory at …/staticfiles» until `collectstatic` — the reason step 8 precedes step 9 |
| pages (D, A-8, A-21) | full middleware stack, the headers nginx sends | `/healthz/` 200 `{"status": "ok", "database": true}`; plain HTTP → 301 `https://example.com/fr/`; `/it/ /fr/ /en/ /ar/` 200; `<html lang="ar" dir="rtl">`; HSTS, CSP, X-Frame-Options DENY, nosniff, Referrer-Policy, COOP, CORP, Permissions-Policy, X-Request-ID present; hashed CSS `immutable` and gzip; `/media/` 404 from Django; `/_design/` and `/__design-v5/` 404; sitemap `<loc>https://example.com/…`; robots `Sitemap: https://example.com/sitemap.xml`; `/wp-json/` 410; 404 without traceback; cookies Secure + HttpOnly + Lax |
| A-8 / A-21 | error pages through the real handlers, DEBUG off | 400, 403, 404, 429, 500: the product's page, one `h1`, no leak; the 500 page shows the request id |
| A-21 (carried) | a request for an unknown Host | `DisallowedHost` escapes the handlers — the recorded defect, mitigated by the catch-all server |
| step 8 / F-10 | allauth sign-in as the device-less superuser, then `/backoffice/` | 302 → `/fr/compte/2fa/totp/activate/` → 200: the first deployment needs no escape hatch |
| C-6 | `pg_dump -Fc` → `pg_restore` (container) → the checklist's three counts | `71|2|0` on both databases |
| tests | `pytest tests/test_env_example_is_complete.py tests/security tests/deployment -p no:randomly -m "not browser"` (lane database `…/ile_devops`) | **202 passed, 1 xfailed** (the unknown-Host xfail), 0 skipped — the confidential-material test ran with its sentinels |
| Known limits | every project source compiled by CPython 3.12.10 | 773 files, 0 syntax errors |
| step 4 | third-party imports of every non-test module of `apps/` and `config/` vs the dependency closure of `requirements/base.txt` | all inside the closure (19 distributions); every one accepts Python 3.12 (`django-unfold` requires ≥ 3.12) |

Scratch databases `ile_verify_scratch`, `ile_verify_restore` and the case-folding probe were dropped; the lane's pytest
database `test_ile_devops` (pre-existing, `--reuse-db`) remains. The scratch environment file and collected tree were
deleted.

## The walk, document by document

**Every citation exists.** Every path and test file (bare names resolved in their cell: `test_authorization_audit.py`,
`test_privilege_escalation.py` in `tests/security/`, `test_console_phone_browser_w3_a.py` in `tests/frontend/`) and all
six named test functions;
every management command and every flag the documents pass (`--limit`, `--apply`, `--dry-run`, `--strict`); every
ALL-CAPS setting, variable and constant (the remainder are shell variables, file names and psql options); every system
check id with the meaning given (`core.E001`, `core.W001–W003`, `accounts.W001`); every URL (`/healthz/`,
`/fr/compte/login/`, `/backoffice/`, `/backoffice/login/`, `/documents/<uuid>/`, `/documents/link/<token>/`,
`/sitemap.xml`, `/robots.txt`, `/wp-json/`); every cited document section (PREPROD §5, §10bis, §15 — six blockers, one
decided; DEPLOYMENT_READINESS §3 — twelve points, §4.3, §5.2; `docs/DEPLOYMENT.md` `v2.0.0-phase1`); every intra-document
link and anchor (0 broken). Ports agree: 5432 (production template), 587/2525/465 (SMTP), 80/443, 65 s nginx vs 60 s
Gunicorn timeouts; body limits 12 m ≥ 10 MiB × 1.05 and 64 m ≥ 60 MiB × 1.05.

**Runbook.** §0 matches the code (Django 5.2.17, psycopg binary, WhiteNoise manifest storage, 14 + 12 committed bundles
and 4 `.mo` catalogues, local-memory cache, no Celery, seven timers). The refusal list matches `prod.py` line for line.
Steps 1–14 — see the order below. §15 — finding 2. The static / public media / private table is right in every cell
(private files `{owner pk}/{uuid4}{ext}` at mode 0600, `PrivateFileSystemStorage.url` raises, no `FileField` on the
model, `_serve` re-runs the policy and `delivery_block`, attachment, `no-store`, sandbox CSP, audited); the five «why a
private document can never be reached» statements hold. TLS, registrar vs DNS, legacy, release tags (the local
`v54/*` / `checkpoint/*` tags exist, 13 of 15 annotated), states and known limits are consistent with the code; the cutover
sequence is the owner's, in his order (held by a test) — findings 10 and 11.

**Checklist.** A-1…A-22 cover the owner's §15 list item by item; every file, script and test they cite exists. A-2,
A-5 — findings 8, 9. §C — finding 3; the C-6 query is right (exercised). §D's expectations match what the page probe
returned (healthz body, 301, the header list, four 200s, `dir="rtl"`, `immutable`, sitemap/robots, 404 without
traceback, 410); D-20's `awk '$6 ~ /^5/'` reads the status field of the runbook's log format.

**Rollback.** §1–§6 are coherent with the runbook and the backup procedure; findings 2, 4, 5, 6.

## Environment variables, both directions

- Everything the code reads is in `.env.example`: settings (`base`, `prod`, `dev`, `test`), application code, scripts
  and tests, including the names held in constants (`ILE_QA_PASSWORD`, `ILE_CONFIDENTIAL_SENTINELS`,
  `ILE_REDACTION_TABLE`, `PEXELS_API_KEY`) and the run-time names of integration secrets (explained in the file). Checked
  by the test and by an independent scan of every tracked file in every language (`os.environ`, `getenv`, `env.*(`,
  `process.env`, `${…}`). One exception outside Python: `POSTGRES_PASSWORD` (finding 12). Self-set ones
  (`DJANGO_ALLOW_ASYNC_UNSAFE`, `PYTHONPATH`) are rightly excluded.
- Everything in `.env.example` is read somewhere; the development-only ones sit commented in NOT FOR PRODUCTION.
- `production.env.example` declares every variable the production settings read, and nothing they ignore; every boolean
  and integer parses (the settings loaded with it); `REDIS_URL` and `DOCUMENT_SCANNER` are empty, which is their default.

## Order of the steps on an empty server

Nothing is used before it exists: packages (1) → user, media, private, ACME and backup directories (2) → checkout and
`staticfiles/` (3) → venv (4) → environment file and `ile-manage` (5; the template comes from the checkout) → role and
database (6; the password from step 5's file) → checks, migrations (7) → collected static, seeds, Site, administrator
(8; directories from 2–3, database from 6) → socket and service (9; the venv, the env file, the collected tree) →
timers (10) → nginx (11; the snake-oil pair from `ssl-cert`, the ACME webroot, the socket) → health (12). `check --deploy`
runs before the database exists without touching it (exercised). TLS and the cutover come after, in the owner's
sequence. `openssl` arrives with `ssl-cert`; `dig` is not in step 1's list but is present on standard Ubuntu server
images and can be run from any workstation.

## Not exercisable here — reviewed only

systemd units and timers (`systemd-analyze verify`), the `ile-manage` wrapper (`systemd-run`), Gunicorn (does not run
on Windows; socket activation and `sd_notify` read in its 26.2 source), nginx (`nginx -t`), certbot, ufw, apt, `dig`,
journald and logrotate. The runbook already says so and gives the on-server checks for each.

## Carried go-live blockers (not new; status)

- **A-13 / F-5** — the back-office sign-in form does not ask for the second factor. Not re-verified (needs an enrolled
  TOTP device). Observed: an anonymous `/backoffice/` is redirected to `/backoffice/login/?next=/backoffice/` — the
  application itself sends staff to that form, so the runbook's «sign in through `/fr/compte/login/`» protects only the
  operator who reads it.
- **A-21 / F-6** — re-verified under the production settings (`DisallowedHost` escapes); mitigated by the catch-all
  server on a fresh server.
- A-23…A-27 — owner, jurist, provider decisions; unchanged.
