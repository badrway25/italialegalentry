# Italy Legal Entry™ — production deployment runbook

> **Documentation only. Nothing in this file has been executed against any server.** It was written on
> 12 October 2026 from the repository itself — settings, views, management commands, tests — for the owner, who
> performs the deployment and the domain cutover himself (directive V5.9). No server was contacted, no DNS record
> changed, no certificate issued. Where a statement depends on the code, the file is named.
>
> Updated on 16 October 2026 by the DevOps lane's second pass, from the repository again: what a browser caches
> (step 8, step 11, the static section), the NUL-byte 400, and the known limits that follow from both; the same day,
> by its review fixes: what «Max post-process passes exceeded» means, the previous release's names, what nginx answers
> itself, which forms the NUL guard reads.
>
> Companions: [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) (release gate, backup before cutover, smoke test) ·
> [`ROLLBACK.md`](ROLLBACK.md) · [`production.env.example`](production.env.example) (the server's environment file).
> They supersede `docs/DEPLOYMENT.md` and `docs/DEPLOYMENT_READINESS.md`, which stay as history.

## Contents

0. [What is deployed, verified in the code](#0-what-is-deployed-verified-in-the-code)
1. [System packages](#1-system-packages) · 2. [User and directories](#2-user-and-directories) ·
   3. [Code at the release tag](#3-code-at-the-release-tag) · 4. [Virtual environment](#4-virtual-environment) ·
   5. [Environment file](#5-environment-file) · 6. [PostgreSQL](#6-postgresql) ·
   7. [Checks and migrations](#7-checks-and-migrations) ·
   8. [Static files, seeds, site, first administrator](#8-static-files-seeds-site-first-administrator) ·
   9. [Gunicorn under systemd](#9-gunicorn-under-systemd) · 10. [Scheduled jobs](#10-scheduled-jobs) ·
   11. [nginx](#11-nginx) · 12. [Health checks](#12-health-checks) · 13. [Logs](#13-logs) ·
   14. [Restart, reload, stop](#14-restart-reload-stop) · 15. [Updating to a new release](#15-updating-to-a-new-release)
- [STATIC ASSETS vs PUBLIC MEDIA vs PRIVATE USER DOCUMENTS](#static-assets-vs-public-media-vs-private-user-documents)
- [TLS / HTTPS](#tls--https)
- [DOMAIN: REGISTRAR TRANSFER vs DNS CUTOVER](#domain-registrar-transfer-vs-dns-cutover)
- [DOMAIN CUTOVER SEQUENCE](#domain-cutover-sequence)
- [LEGACY](#legacy)
- [RELEASE TAGS](#release-tags) · [States: DEVELOPMENT_COMPLETE / RELEASE_CANDIDATE / PRODUCTION_READY](#states)
- [Known limits and external dependencies](#known-limits-and-external-dependencies)

---

## 0. What is deployed, verified in the code

| Component | What the repository actually uses | Where |
|---|---|---|
| Application | Django 5.2.17 LTS, modular monolith, server-rendered; WSGI entry `config.wsgi:application`, which defaults to `config.settings.prod` | `requirements/base.txt`, `config/wsgi.py` |
| Python | `requires-python >= 3.12`; Ubuntu **24.04 LTS** ships 3.12 (22.04's 3.10 is too old). CI and the Dockerfile run 3.13 — see [Known limits](#known-limits-and-external-dependencies) | `pyproject.toml`, `.github/workflows/ci.yml` |
| Database | PostgreSQL only, psycopg 3 binary wheel (no `libpq-dev`, no compiler), `DATABASE_URL`, `ATOMIC_REQUESTS`, connections reused 60 s with health checks | `config/settings/base.py`, `prod.py` |
| Application server | Gunicorn 26.2 (sync workers), behind one reverse proxy | `requirements/base.txt` |
| Static files | WhiteNoise middleware, `core.storage.CompressedManifestModulesStorage` — WhiteNoise's `CompressedManifestStaticFilesStorage` (hashed names, `.gz` siblings) with the ES modules' imports rewritten to the hashed names too: every file a page loads is a hashed name, cached `immutable`; a plain name is revalidated after 60 s ([step 8](#8-static-files-seeds-site-first-administrator)) — served **through Gunicorn**. The bundles (`static/css/dist`, `static/js/dist`) and the compiled catalogues (`locale/*/LC_MESSAGES/*.mo`) are committed: **no Node, no gettext on the server** | `base.py` `STORAGES`, `core/storage.py`, `tests/frontend/test_static_pipeline.py`, `tests/deployment/test_static_caching.py` |
| Public media | `MEDIA_ROOT` at `/media/`, served by **nginx** (Django serves it only with DEBUG on) | `config/urls.py`, `prod.py` |
| Private documents | `PRIVATE_MEDIA_ROOT`, outside every served directory, delivered only by `documents.views._serve` after authorisation | `apps/documents/storage.py`, `views.py` |
| Cache | Local memory. `REDIS_URL` must stay empty: the Redis client library is not in the requirements (check `core.E001`) | `base.py`, `apps/core/checks.py` |
| E-mail | SMTP (`EMAIL_*`); account e-mails are sent during the request, notifications are queued in `EmailOutbox` and sent by a timer | `apps/notifications/services.py` |
| Background work | **No Celery, no worker.** Seven management commands on systemd timers, and a nightly encrypted backup | [step 10](#10-scheduled-jobs) |
| Second factor | TOTP enrolment enforced in production for every account that reads other people's data, and an account that holds a device asked for its code in every session before the back office, the reserved area or a private document opens. `/backoffice/login/`, Django's own sign-in form, is closed: it signs no one in and sends the visitor to allauth's sign-in, which asks the code (F-5, fixed — checklist A-13); nginx's redirect of that path stays as a second layer ([step 11](#11-nginx)) | `accounts/middleware.py`, `accounts/admin_site.py`, `prod.py` |

Production settings refuse to start on a weakened configuration (`config/settings/prod.py`): missing
`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DATABASE_URL` or `IP_HASH_SALT`, or no
explicit `0`/`1` for `SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD`; HTTPS redirect off; HSTS under a
year; a short key; the second factor off; `*` in the host list; a published or short salt; a mail backend that
writes to the logs; an unfilled `<...>` placeholder. `ILE_ALLOW_INSECURE_PROD=1` is the
single escape hatch — **never on this host** (it exists for the TLS-less staging-like stack,
`docker-compose.staging.yml`). One thing is refused even through the hatch: `PRIVATE_MEDIA_ROOT` inside a served
directory.

### Names used throughout

| What | Value |
|---|---|
| System user and group | `italylegalentry` (no login shell, no home) |
| Code (git checkout, owned by root) | `/srv/italylegalentry/app` |
| Virtual environment (owned by root) | `/srv/italylegalentry/venv` |
| Collected static files (`STATIC_ROOT`) | `/srv/italylegalentry/app/staticfiles` (owned by `italylegalentry`) |
| Environment file | `/etc/italylegalentry/italylegalentry.env` (root:root, 0600 — systemd reads it as root) |
| Public media (`MEDIA_ROOT`) | `/var/lib/italylegalentry/media` (italylegalentry:www-data, 2750) |
| Private documents (`PRIVATE_MEDIA_ROOT`) | `/var/lib/italylegalentry/private` (italylegalentry:italylegalentry, 0700) |
| Gunicorn socket | `/run/italylegalentry.sock` (owned by www-data, 0600 — only nginx connects) |
| Management command wrapper | `/usr/local/sbin/ile-manage` |
| Backup script | `/usr/local/sbin/ile-backup` (root, 0700), run nightly by `italylegalentry-backup.timer` |
| Backups | `/var/backups/italylegalentry` (root, 0700): encrypted sets, kept 7 days; the off-server copy keeps the retention |
| ACME webroot | `/var/www/letsencrypt` |
| Maintenance page | `/var/www/italylegalentry-maintenance` (nginx serves it while the application is stopped) |

### Shell variables for the session

Set these once in the SSH session; every command below reads them. **Replace the values.**

```bash
export ILE_DOMAIN=example.com              # the production host name, no scheme
export ILE_TAG=v5-release-candidate        # the validated release tag from the handoff
export ILE_SHA=0000000000000000000000000000000000000000   # the commit SHA the handoff gives for that tag
export ILE_STAGING_HOST=                   # optional: temporary host name for validation before the cutover
sudo -v                                    # cache sudo credentials before the multi-line blocks
```

Before you start: an Ubuntu 24.04 LTS droplet in an **EU region** (CR-08: the region of the server, the database and
the backups must be confirmed in writing), SSH access as a sudo user, the credentials of an SMTP provider, and the
handoff block (tag, SHA, test results). **Do not change any DNS record until the [cutover sequence](#domain-cutover-sequence).**

---

## 1. System packages

Only what the architecture needs: git, Python with `venv`, PostgreSQL, nginx, certbot, `ssl-cert` for the
temporary self-signed certificate, and `gnupg` and `rsync` for the backups (step 10; both usually present already).

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-venv postgresql postgresql-client nginx ssl-cert certbot curl gnupg rsync
python3 --version        # must print Python 3.12 or later
psql --version           # Ubuntu 24.04: PostgreSQL 16 (Django 5.2 supports 14 and later)
nginx -v                 # Ubuntu 24.04: nginx 1.24
```

**Firewall.** On a *fresh* droplet with nothing else on it:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

On an *existing* server, do **not** enable ufw blindly: list what already listens (`sudo ss -ltnp`) and what the
DigitalOcean cloud firewall allows, then open only 80 and 443 in addition. PostgreSQL listens on localhost only
(Ubuntu's default) and must stay that way.

## 2. User and directories

```bash
sudo useradd --system --user-group --no-create-home --home-dir /nonexistent --shell /usr/sbin/nologin italylegalentry
sudo install -d -o root -g root -m 0755 /srv/italylegalentry /var/lib/italylegalentry /var/www/letsencrypt \
     /var/www/italylegalentry-maintenance
sudo install -d -o italylegalentry -g www-data -m 2750 /var/lib/italylegalentry/media
sudo install -d -o italylegalentry -g italylegalentry -m 0700 /var/lib/italylegalentry/private
sudo install -d -o root -g root -m 0700 /etc/italylegalentry
sudo install -d -o root -g root -m 0700 /var/backups/italylegalentry
```

Why these modes: nginx (user `www-data`) reads public media through the group, and the set-group-ID bit (`2750`)
makes every directory the application creates there inherit that group. The private directory is `0700`: nginx has
no permission on it at all, and the application writes its files `0600` (`documents/storage.py`). The code and the
virtual environment belong to root: the running service cannot modify its own code. `/etc/italylegalentry` (the
environment file, later the backup key and the off-server copy's credentials) is root's alone: systemd reads the
environment file as root before it starts the service, a timer or `ile-manage`, so the application's user never
needs to.

## 3. Code at the release tag

The server always runs a **tag**, never a branch. The public repository's history is a sequence of clean snapshot
commits (one per publication): the SHA to check is the one the handoff gives for the tag.

```bash
sudo git clone https://github.com/badrway25/italialegalentry.git /srv/italylegalentry/app
sudo git -C /srv/italylegalentry/app fetch --tags
sudo git -C /srv/italylegalentry/app checkout --detach "refs/tags/$ILE_TAG"
test "$(sudo git -C /srv/italylegalentry/app rev-parse HEAD)" = "$ILE_SHA" && echo "SHA OK" || echo "SHA MISMATCH — STOP"
sudo git -C /srv/italylegalentry/app status --porcelain      # must print nothing
sudo install -d -o italylegalentry -g italylegalentry -m 0755 /srv/italylegalentry/app/staticfiles
```

`staticfiles/`, `media/` and `private_media/` are ignored by git (`.gitignore`), so checking out another tag never
touches them.

## 4. Virtual environment

Production dependencies only — `requirements/base.txt`, **never** `requirements/dev.txt` (test runners, Playwright,
linters) — with `requirements/constraints.txt`, which pins the exact version of every package they pull in (base.txt
pins only the nine it names): the server gets the set the tests ran, and a rollback restores the previous tag's set.
Every package installs from a wheel: no compiler is needed.

```bash
sudo python3 -m venv /srv/italylegalentry/venv
sudo /srv/italylegalentry/venv/bin/python -m pip install --no-cache-dir -r /srv/italylegalentry/app/requirements/base.txt -c /srv/italylegalentry/app/requirements/constraints.txt
sudo /srv/italylegalentry/venv/bin/python -m pip check       # "No broken requirements found."
```

## 5. Environment file

`config/settings/prod.py` ignores any `.env` file — a development file copied onto a server would *satisfy* the
mandatory variables with development values. The variables come from the process environment, which systemd builds
from this file (`EnvironmentFile=`) for the application, its timers and `ile-manage` — reading it as root, so the file
is root's alone (0600).

```bash
sudo install -o root -g root -m 0600 /srv/italylegalentry/app/docs/deployment/production.env.example /etc/italylegalentry/italylegalentry.env
# The three secrets, generated on the server and written straight into the file (never on a command line):
sudo python3 - /etc/italylegalentry/italylegalentry.env <<'PY'
import pathlib, secrets, sys
path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
for placeholder, nbytes in (
    ("<generate a secret: 64 random bytes, URL-safe>", 64),   # DJANGO_SECRET_KEY (86 characters)
    ("<generate a secret: 48 random bytes, URL-safe>", 48),   # IP_HASH_SALT (64 characters)
    ("<database-password>", 32),                              # the database role's password, step 6 (43 characters)
):
    text = text.replace(placeholder, secrets.token_urlsafe(nbytes), 1)
path.write_text(text, encoding="utf-8")
PY
sudo sed -i "s/<your-domain>/$ILE_DOMAIN/g" /etc/italylegalentry/italylegalentry.env
sudoedit /etc/italylegalentry/italylegalentry.env    # fill <smtp-host>, <smtp-user>, <smtp-password>, <sender-domain>
sudo grep -nE '^[^#].*<[^@>]*>' /etc/italylegalentry/italylegalentry.env || echo "no placeholder left"
```

What each variable does, and why the template sets it so, is written beside it in
[`production.env.example`](production.env.example); the complete list of everything the code reads is
[`.env.example`](../../.env.example). Three switches deserve their own line here:

- **`ILE_READ_ENV_FILE`** — never set it on this host. It makes the production settings read a `.env` file in the
  checkout again; its only use is a local production-like experiment.
- **`ILE_ALLOW_INSECURE_PROD`** — never set it on this host. It disables every refusal of `prod.py` at once. **The
  first deployment does not need it**: with the second factor enforced, an account without a device is redirected to
  the enrolment page, which stays reachable (`accounts/middleware.py`: the page is under no guarded perimeter, and
  the rule on allauth's second-factor pages concerns only an account that already holds a device) — verified locally
  with the production settings on 12 October 2026, and through allauth's own activation since F-5's fix
  (`test_an_unenrolled_account_can_still_enrol`,
  `test_enrolling_through_allauth_counts_as_presenting_the_new_device`). If it is ever used: write down why and until
  when, and remove it.
- **`SECURE_HSTS_INCLUDE_SUBDOMAINS` / `SECURE_HSTS_PRELOAD`** — the template sets both to `0` until every host of the
  domain is known to serve valid HTTPS; see [TLS / HTTPS](#tls--https). Neither has a default in `prod.py`: keep
  both lines — without one, the application refuses to start.

Then the wrapper that runs a management command as the application user with exactly that environment (systemd
parses the file, as it does for the service — no shell quoting surprises). It also names the settings module,
like every unit below: `manage.py` on its own defaults to the **development** settings (`manage.py`), and the
environment file, which sets the same value, wins whenever it says otherwise:

```bash
sudo tee /usr/local/sbin/ile-manage >/dev/null <<'EOF'
#!/bin/sh
# ile-manage <command> [arguments] — a Django management command of Italy Legal Entry, run as the application
# user with the environment of the service (systemd reads /etc/italylegalentry/italylegalentry.env).
set -eu
if [ -t 0 ] && [ -t 1 ]; then stdio=--pty; else stdio=--pipe; fi
exec systemd-run --quiet --wait --collect --service-type=exec "$stdio" \
    --uid=italylegalentry --gid=italylegalentry \
    --working-directory=/srv/italylegalentry/app \
    --property=EnvironmentFile=/etc/italylegalentry/italylegalentry.env \
    --setenv=DJANGO_SETTINGS_MODULE=config.settings.prod --setenv=PYTHONDONTWRITEBYTECODE=1 \
    /srv/italylegalentry/venv/bin/python manage.py "$@"
EOF
sudo chmod 0755 /usr/local/sbin/ile-manage
```

## 6. PostgreSQL

The production database starts from the **current schema of this project, empty**. Never restore, attach or import
the legacy database (see [LEGACY](#legacy)).

Local PostgreSQL on the droplet — the role's password is the one step 5 generated into `DATABASE_URL`. It reaches
`psql` on its **standard input**, never on a command line: `sudo` writes every command line to its log
(`/var/log/auth.log`) and `/proc` shows it while the command runs, but `printf` is a shell builtin, so the password
appears in neither. And no statement below can fail on a re-run — a failing statement is what PostgreSQL writes to
its own log, password included:

```bash
DB_PASSWORD="$(sudo sed -n 's|^DATABASE_URL=postgres://italylegalentry:\([^@]*\)@.*|\1|p' /etc/italylegalentry/italylegalentry.env)"
printf '%s' "$DB_PASSWORD" | grep -qxE '[A-Za-z0-9_-]{32,}' && echo "password read" || echo "STOP: no URL-safe password in DATABASE_URL"
{ printf '\\set pw %s\n' "$DB_PASSWORD"; cat <<'SQL'; } | sudo -u postgres psql -v ON_ERROR_STOP=1 --quiet
SELECT 'CREATE ROLE italylegalentry LOGIN' WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'italylegalentry') \gexec
ALTER ROLE italylegalentry WITH LOGIN PASSWORD :'pw';
SELECT 'CREATE DATABASE italylegalentry OWNER italylegalentry ENCODING ''UTF8'' TEMPLATE template0'
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'italylegalentry') \gexec
SQL
unset DB_PASSWORD
```

Safe to run again: the role and the database are created only when missing, and the role's password is set from the
file each time — after changing it in `DATABASE_URL`, run the block again, then restart the service. The password
stays URL-safe (letters, digits, `-`, `_`), as generated: it is read back from the URL. Exercised on a local
PostgreSQL 17 on 12 October 2026: twice in a row; the file's password then opened the database over scram-sha-256,
and the server log never held it.

A **DigitalOcean Managed PostgreSQL** cluster instead (EU region, CR-08): skip the block above. In the control panel,
create the user `italylegalentry` and the database `italylegalentry`, and download the cluster's CA certificate. Then:

```bash
sudo install -o root -g root -m 0644 ca-certificate.crt /srv/italylegalentry/db-ca.crt   # public; the service reads it
sudoedit /etc/italylegalentry/italylegalentry.env
#   DATABASE_URL=postgres://italylegalentry:<password>@<cluster-host>:<port>/italylegalentry?sslmode=verify-full&sslrootcert=/srv/italylegalentry/db-ca.crt
#   verify-full checks the server's certificate and its name; sslmode=require only encrypts, and would talk to any
#   server. Percent-encode the password if it holds anything but letters, digits, - and _.
# PostgreSQL 15 and later: the database the panel creates belongs to the admin user, and the new user may not create
# tables in its schema public (migrate: «permission denied for schema public»). Grant it, as the admin user,
# connected to that database — psql asks for the admin password, so nothing secret is on the command line:
psql "host=<cluster-host> port=<port> dbname=italylegalentry user=<admin-user> sslmode=verify-full sslrootcert=/srv/italylegalentry/db-ca.crt" \
     -c 'GRANT CREATE, USAGE ON SCHEMA public TO italylegalentry;'
# The nightly backup (step 10) reads the password from a root-only file — libpq ignores it unless it is 0600:
sudo install -o root -g root -m 0600 /dev/null /etc/italylegalentry/pgpass
sudoedit /etc/italylegalentry/pgpass      # one line: <cluster-host>:<port>:italylegalentry:italylegalentry:<password>
```

`ALTER DATABASE italylegalentry OWNER TO italylegalentry` would also do, but from PostgreSQL 16 the admin user may run
it only if it can `SET ROLE italylegalentry`, which a user created by the panel does not grant (reproduced on a local
PostgreSQL 17 with a non-superuser admin: «must be able to SET ROLE»; the `GRANT` above worked). In
`/usr/local/sbin/ile-backup` (step 10), replace the `pg()` line with the managed one written above it.

## 7. Checks and migrations

```bash
sudo ile-manage check --deploy
```

Expected: **no issue**, except `security.W005` and `security.W021` while the environment file keeps
`SECURE_HSTS_INCLUDE_SUBDOMAINS=0` / `SECURE_HSTS_PRELOAD=0` — expected and justified until the domain's hosts are
inventoried. Anything else is a configuration to fix before going further:

| Id | Meaning | Fix |
|---|---|---|
| `core.E001` | `REDIS_URL` set, Redis client library absent: every cache access fails, sign-in included | empty `REDIS_URL` |
| `core.W001` | Django trusts the proxy, allauth does not: one rate-limit bucket for everyone, or 403 | `ALLAUTH_TRUSTED_PROXY_COUNT=1` |
| `core.W002` | SMTP backend without `EMAIL_HOST` | fill the `EMAIL_*` variables |
| `core.W003` | `DEFAULT_FROM_EMAIL` on a placeholder domain | a sender your SMTP provider is authorised for |
| `accounts.W001` | second-factor enrolment not mandatory: an account that reads others' data and holds no device signs in with a password alone (a device an account holds is asked for in every session whatever the flag says) | `BACKOFFICE_MFA_ENFORCED=1` |

**Migrate → verify → rollback strategy.**

```bash
sudo ile-manage migrate --plan | tail -n 5          # what will run (the first time: every migration)
sudo ile-manage migrate --noinput
sudo ile-manage migrate --check && echo "no unapplied migration"
sudo ile-manage makemigrations --check --dry-run     # "No changes detected": the tag has no model change without migration
sudo ile-manage showmigrations | grep -c '\[ \]'     # 0
```

Rollback strategy (details in [`ROLLBACK.md`](ROLLBACK.md)): migrations are treated as **forward-only**. On the first
deployment the database is new and empty, so a failed migration is undone by dropping and re-creating it. From the
second release on, a dump of the stopped database is taken and checked by a restore **before** every `migrate`
([step 15](#15-updating-to-a-new-release)), and the way back from a migration that removed or rewrote data is a
restore of that dump — never a hand-made reverse migration in production.

## 8. Static files, seeds, site, first administrator

```bash
sudo ile-manage collectstatic --noinput              # into /srv/italylegalentry/app/staticfiles; no Node needed
sudo ile-manage seed_all                             # creates what is missing, never rewrites what staff edited
sudo ls /var/lib/italylegalentry/media/library/photos | head -n 3   # seed_all copies the library's photographs here
sudo ile-manage shell -c "from django.contrib.sites.models import Site; Site.objects.update_or_create(id=1, defaults={'domain': '$ILE_DOMAIN', 'name': 'Italy Legal Entry'})"
```

- `seed_all` never invents people here: the production settings pin `ILE_SEED_DEMONSTRATION_DATA` off, and the
  demonstration seeds report «skipped». It writes **no rule in force**: the legal rules are candidates awaiting a
  jurist (`docs/PREPROD_REPORT.md` §5).
- `seed_all` is safe at every release: each seed creates what is missing — locked content, flags, menus, rule
  candidates, the media library — and never rewrites what staff edited (the contract of `apps/core/seeds.py`). The
  legal sources broke it until 12 October 2026 (a jurist's corrected citation returned to the build's text at each
  deployment); `apps/rules/tests/test_seed_keeps_editorial_changes.py` now holds them to it.
- **The Site row matters.** The sitemap builds its URLs from it (`django.contrib.sites`); until it is set, every
  `<loc>` of `/sitemap.xml` reads `http://example.com/…` (verified locally). Set it again if the domain changes.
- Keep the old static files: never `collectstatic --clear` — a rollback, and pages still open in browsers, reference
  the previous release's hashed names.
- **What a browser keeps, and for how long.** Every file a page loads is a hashed name — the scripts and stylesheets
  the templates link, the fonts and images the stylesheets name, and the ES modules each script imports (the shared
  chunks, and the entries loaded on demand: `loader.js`, `depot.js`, `piece-drawer.js`), whose import specifiers
  collectstatic rewrites to the hashed names (`core/storage.py`). WhiteNoise serves a hashed name
  `max-age=315360000, public, immutable`: a release changes the names, so a returning browser never runs a previous
  release's module, and a page opened before the release keeps importing its own release's files, which stay
  collected. A plain name — the original copy collectstatic keeps beside each hashed one, linked by no page — is
  `max-age=60, public` (`WHITENOISE_MAX_AGE`). Until 16 October 2026 the modules imported one another by plain names,
  cached a year (`tests/deployment/test_static_caching.py` runs a real collectstatic under the production settings
  and holds it). Only the bundles of `static/js/dist` are rewritten so; the sources of `static/js/src` are collected
  as written, and no page loads them. If this collectstatic ever stops on «Max post-process passes exceeded», a chain
  of imports in the dist is longer than Django's post-processing settles in this server's directory order (ext4 lists
  a directory in hash order, a workstation's NTFS sorted), or two bundles import each other. The same test computes
  the worst case over every order, so CI refuses such a dist first; the fix is in the build (`static/js/src`), never on
  the server, and the failed run leaves the previous manifest and every file it names in place (Known limits).

**First administrator.**

```bash
sudo ile-manage createsuperuser          # asks for the e-mail and the password — the user model has no username
ADMIN_EMAIL=you@example.org              # the address just entered
sudo ile-manage shell -c "from allauth.account.models import EmailAddress; from django.contrib.auth import get_user_model; u = get_user_model().objects.get(email='$ADMIN_EMAIL'); EmailAddress.objects.update_or_create(user=u, email=u.email, defaults={'verified': True, 'primary': True})"
```

E-mail verification is mandatory (`ACCOUNT_EMAIL_VERIFICATION`); an account made by `createsuperuser` has no verified
address, so allauth would mail a confirmation link at its first sign-in. Marking the operator's own address verified
is that click, done before SMTP is proven. Then — on the temporary host of cutover step 3, or on the domain after
the cutover — sign in at `/fr/compte/login/` (allauth): the second factor is enforced, so you land on the TOTP
enrolment page — scan, confirm, **store the recovery codes offline** — and only then reach `/backoffice/`. From then
on every sign-in asks the TOTP code before the back office opens. `/backoffice/login/` leads to the same page: since
F-5's fix the back office's own sign-in signs no one in and sends the visitor to allauth's (checklist A-13), and
nginx redirects that path to allauth's sign-in as well ([step 11](#11-nginx)).

## 9. Gunicorn under systemd

systemd owns the socket and hands it to Gunicorn (socket activation): only nginx can connect to it, and requests that
arrive during a restart wait instead of failing.

```bash
sudo tee /etc/systemd/system/italylegalentry.socket >/dev/null <<'EOF'
[Unit]
Description=Italy Legal Entry - gunicorn socket

[Socket]
ListenStream=/run/italylegalentry.sock
# Only nginx (www-data) may connect. The service inherits the open socket from systemd.
SocketUser=www-data
SocketGroup=www-data
SocketMode=0600

[Install]
WantedBy=sockets.target
EOF

sudo tee /etc/systemd/system/italylegalentry.service >/dev/null <<'EOF'
[Unit]
Description=Italy Legal Entry - gunicorn (config.wsgi)
Requires=italylegalentry.socket
After=network.target postgresql.service

[Service]
Type=notify
NotifyAccess=main
User=italylegalentry
Group=italylegalentry
WorkingDirectory=/srv/italylegalentry/app
EnvironmentFile=/etc/italylegalentry/italylegalentry.env
Environment=DJANGO_SETTINGS_MODULE=config.settings.prod PYTHONDONTWRITEBYTECODE=1
ExecStart=/srv/italylegalentry/venv/bin/gunicorn config.wsgi:application \
    --workers 3 --timeout 60 --graceful-timeout 30 \
    --max-requests 1000 --max-requests-jitter 100 \
    --no-control-socket --error-logfile - --log-level info
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=40
Restart=on-failure
RestartSec=5
UMask=0027

# Sandbox. The application writes only the two media directories, and its upload temporary files in /tmp
# (private to the service). Nothing under /srv is writable by the running process.
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ReadWritePaths=/var/lib/italylegalentry/media /var/lib/italylegalentry/private
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictSUIDSGID=yes
RestrictRealtime=yes
RestrictNamespaces=yes
LockPersonality=yes
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
CapabilityBoundingSet=
SystemCallArchitectures=native

[Install]
WantedBy=multi-user.target
EOF

sudo systemd-analyze verify /etc/systemd/system/italylegalentry.socket /etc/systemd/system/italylegalentry.service
sudo systemctl daemon-reload
sudo systemctl enable --now italylegalentry.socket
sudo systemctl enable --now italylegalentry.service
systemctl status italylegalentry.service --no-pager
sudo systemd-analyze security italylegalentry.service | tail -n 1
```

Choices, and where they come from:

- **3 sync workers** — the configuration measured on the staging-like stack (`docs/STAGING_PERFORMANCE.md`). Memory:
  about 100–150 MB each is an **estimate**, not a measurement (that document records the worker count, not their
  memory) — read the real figure on the server after the smoke test (`systemctl status italylegalentry`, line
  `Memory:`); 2 GB of RAM leaves room on that estimate. nginx buffers request bodies before passing them on, so a slow
  upload never holds a sync worker. **Timeout 60 s** with nginx's read timeout at 65 s.
- **`--no-control-socket`** — since 25.1 Gunicorn opens a control socket by default, under `$XDG_RUNTIME_DIR` or
  `$HOME/.gunicorn/`. This unit has neither (the user's home is `/nonexistent`, the filesystem read-only), and
  Gunicorn 26.2 then logs `[ERROR] Control server error: [Errno 30] Read-only file system` at start and again after
  every worker recycle — reproduced in a Linux container with the same user, home and read-only root on
  12 October 2026; none with the flag. `systemctl` is the control interface here; `gunicornc` is not used.
- **No access log in Gunicorn** — nginx keeps it ([step 13](#13-logs)); Gunicorn's errors and Django's structured
  JSON lines go to journald.
- **Sandbox** — `ReadWritePaths` lists exactly what the code writes (a search of the application for file writes
  finds only the two storages and Django's upload temporary files). `MemoryDenyWriteExecute` and
  `SystemCallFilter` are deliberately absent: they were not exercised on a Linux host while this runbook was
  written. **These directives have not been run on a server yet**: after enabling, run the smoke test of the
  checklist (§D) — sign-in, an upload, a download — and if something is refused, `sudo journalctl -u italylegalentry`
  names the directive to relax.

## 10. Scheduled jobs

There is no Celery and no queue worker: the platform's background work is seven management commands, each a systemd
timer, plus the nightly backup ([below](#the-nightly-backup)). Their sources and why each must run:

| Timer `italylegalentry-…` | When | Command | Source | If it does not run |
|---|---|---|---|---|
| `send-queued-emails` | every 2 min | `send_queued_emails --limit 100` | `apps/notifications/management/commands/send_queued_emails.py` | `NOTIFICATIONS_SEND_IMMEDIATELY=0` queues every notification and every form e-mail in `EmailOutbox`; nothing leaves. Failed sends are retried up to 5 times (`notifications/services.py`, `send_pending`) |
| `notifications-scan-deadlines` | daily 06:15 Rome | `notifications_scan_deadlines` | `apps/notifications/management/commands/notifications_scan_deadlines.py` | no warning of a due or overdue requirement; idempotent per state, safe to re-run |
| `documents-refresh-requirements` | daily 02:40 Rome | `documents_refresh_requirements` | `apps/documents/management/commands/documents_refresh_requirements.py` | stored requirement states drift from the derived ones (dashboards, counts); idempotent |
| `documents-purge-expired` | daily 03:10 Rome | `documents_purge_expired --apply` | `apps/documents/management/commands/documents_purge_expired.py` | **retention breach**: private files past `retention_until` stay on disk. Dry-run without `--apply` |
| `purge-expired-submissions` | daily 03:20 Rome | `purge_expired_submissions --apply` | `apps/enquiries/management/commands/purge_expired_submissions.py` | **retention breach**: form submissions older than 24 months (`ILE["RETENTION_MONTHS_FORMS"]`) stay. Dry-run without `--apply` |
| `purge-orientation-sessions` | daily 03:30 Rome | `purge_orientation_sessions` | `apps/orientation/management/commands/purge_orientation_sessions.py` | **retention breach**: anonymous orientation sessions older than 30 days stay. Applies by default (`--dry-run` previews) |
| `clearsessions` | daily 03:40 Rome | `clearsessions` | Django (`django.contrib.sessions`, database sessions: no `SESSION_ENGINE` is set) | expired sessions accumulate in the database |

Look before the purges run for the first time — the dry runs change nothing:

```bash
sudo ile-manage documents_purge_expired
sudo ile-manage purge_expired_submissions
sudo ile-manage purge_orientation_sessions --dry-run
systemd-analyze calendar '*-*-* 06:15:00 Europe/Rome'   # must print the next run; if it errors, drop " Europe/Rome" below (times are then UTC)
```

Install the fourteen units (one service and one timer per job):

```bash
while IFS='|' read -r name schedule command; do
  [ -n "$name" ] || continue
  sudo tee "/etc/systemd/system/italylegalentry-$name.service" >/dev/null <<EOF
[Unit]
Description=Italy Legal Entry job - $command
After=network.target postgresql.service

[Service]
Type=oneshot
User=italylegalentry
Group=italylegalentry
WorkingDirectory=/srv/italylegalentry/app
EnvironmentFile=/etc/italylegalentry/italylegalentry.env
Environment=DJANGO_SETTINGS_MODULE=config.settings.prod PYTHONDONTWRITEBYTECODE=1
ExecStart=/srv/italylegalentry/venv/bin/python manage.py $command
Nice=10
TimeoutStartSec=30min
UMask=0027
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=strict
ReadWritePaths=/var/lib/italylegalentry/media /var/lib/italylegalentry/private
ProtectHome=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
LockPersonality=yes
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
EOF
  sudo tee "/etc/systemd/system/italylegalentry-$name.timer" >/dev/null <<EOF
[Unit]
Description=Schedule of italylegalentry-$name

[Timer]
OnCalendar=$schedule
Persistent=true
RandomizedDelaySec=60

[Install]
WantedBy=timers.target
EOF
done <<'JOBS'
send-queued-emails|*:0/2|send_queued_emails --limit 100
notifications-scan-deadlines|*-*-* 06:15:00 Europe/Rome|notifications_scan_deadlines
documents-refresh-requirements|*-*-* 02:40:00 Europe/Rome|documents_refresh_requirements
documents-purge-expired|*-*-* 03:10:00 Europe/Rome|documents_purge_expired --apply
purge-expired-submissions|*-*-* 03:20:00 Europe/Rome|purge_expired_submissions --apply
purge-orientation-sessions|*-*-* 03:30:00 Europe/Rome|purge_orientation_sessions
clearsessions|*-*-* 03:40:00 Europe/Rome|clearsessions
JOBS
sudo systemd-analyze verify /etc/systemd/system/italylegalentry-*.service /etc/systemd/system/italylegalentry-*.timer
sudo systemctl daemon-reload
for job in send-queued-emails notifications-scan-deadlines documents-refresh-requirements documents-purge-expired \
           purge-expired-submissions purge-orientation-sessions clearsessions; do
  sudo systemctl enable --now "italylegalentry-$job.timer"
done
systemctl list-timers 'italylegalentry-*' --no-pager
```

**Not scheduled, on purpose:**

| Command | Why not now | When to add a timer |
|---|---|---|
| `documents_scan_pending` | no antivirus exists (`DOCUMENT_SCANNER` empty); the command says «not configured» and exits | when a scanner is configured: every 15 min |
| `deliver_outbound_events` | the default transport only logs, and outside DEBUG leaves events queued for the pull API; the push transport also needs `INTEGRATIONS_ALLOW_NETWORK`, which is a setting, not a variable | when a CRM push integration is approved |
| `rules_pending_review --strict` | a check, not a job: exit 1 means a rule is in force without an approver or on an unverified source. Today it exits 0 — no rule is in force | run it by hand after every rule activation, or as a monitored check |
| `seed_all`, `seed_legal_rules`, `create_api_key`, `activate_ruleset` / `import_ruleset` / `export_ruleset` / `validate_ruleset` | deployment or administration commands, run by a person | never on a timer |
| `companies_demo`, `rules_activate_demonstration` | demonstration only: both refuse (exit 1) wherever demonstration data is not allowed, and the production settings pin that switch off — `companies_demo` since 12 October 2026 (`apps/companies/tests/test_demo_command.py`); before, it invented a company and approved an account's verification | never in production |

### The nightly backup

`italylegalentry-backup.timer` runs `/usr/local/sbin/ile-backup` every night. It takes an online `pg_dump -Fc` first
(one consistent snapshot while the site runs), then the private documents, the public media and the configuration —
the environment file, nginx, the TLS keys, the units — each streamed through `gpg` to the **owner's public key**:
nothing readable is written to disk or leaves the server, and the server cannot decrypt its own backups, because the
private key never comes here. `SHA256SUMS-<TS>` lists the encrypted files by relative name, so `sha256sum -c` works
wherever the set is copied. The set is then copied off the server; the local copies are kept 7 days.

**The owner decides** (checklist §B and A-28): where the off-server copy lives (EU, CR-08) and who can read and delete
there; who holds the private key and its passphrase (two offline copies: losing the key loses every backup); the
retention. Proposal (`docs/DEPLOYMENT_READINESS.md` §4.2): 30 daily sets, monthly sets only by decision with the legal
referent — an erased person stays in every set until it expires, so a backup that outlives a retention term breaches
it. Pruning at the destination follows that decision.

**1. The owner's key** — made once, **on the owner's machine**; only its public part goes to the server:

```bash
gpg --quick-generate-key "Italy Legal Entry backups" default default never   # asks for the passphrase
gpg --export --armor "Italy Legal Entry backups" > backup-recipient.asc
gpg --show-keys backup-recipient.asc            # note the fingerprint; compare it after the copy
# copy backup-recipient.asc to the server (scp), then, on the server:
sudo install -o root -g root -m 0644 backup-recipient.asc /etc/italylegalentry/backup-recipient.asc
```

**2. The script and its two units:**

```bash
sudo tee /usr/local/sbin/ile-backup >/dev/null <<'EOF'
#!/bin/bash
# ile-backup - one backup set of Italy Legal Entry, encrypted to the owner's public key (runbook, step 10).
# Run as root: every night by italylegalentry-backup.timer, and by hand before the cutover (checklist, section C)
# and before every update (runbook, step 15). Writes {db,private,media,config}-<TS>.*.gpg and SHA256SUMS-<TS>
# (relative names) into /var/backups/italylegalentry, prunes the local copies, then copies the set off the server.
set -euo pipefail
umask 077
cd /

BACKUPS=/var/backups/italylegalentry
RECIPIENT=/etc/italylegalentry/backup-recipient.asc  # the owner's PUBLIC key; the private key never comes here
OFFSITE=/etc/italylegalentry/backup-offsite          # the owner's copy command (runbook, step 10); until then, exit 2
KEEP_LOCAL_DAYS=7                                    # local copies only: the off-server location keeps the retention

# The database, through the local socket as the postgres superuser. A managed cluster instead (runbook, step 6):
# pg() { PGPASSFILE=/etc/italylegalentry/pgpass "$@" "host=<cluster-host> port=<port> dbname=italylegalentry user=italylegalentry sslmode=verify-full sslrootcert=/srv/italylegalentry/db-ca.crt"; }
pg() { runuser -u postgres -- "$@" -d italylegalentry; }

[ -s "$RECIPIENT" ] || { echo "ile-backup: no public key at $RECIPIENT" >&2; exit 1; }
TS=$(date -u +%Y%m%dt%H%M%Sz)
WORK=$(mktemp -d "$BACKUPS/.partial-$TS.XXXXXX")
GNUPGHOME=$(mktemp -d)
export GNUPGHOME
trap 'rm -rf "$WORK" "$GNUPGHOME"' EXIT
encrypt() { gpg --batch --no-tty --quiet --recipient-file "$RECIPIENT" --output "$WORK/$1.gpg" --encrypt; }
# tar exits 1 when a file changes while it is read (an upload at that instant): tolerated. 2 is a failure.
archive() { tar "$@" || [ $? -eq 1 ]; }

# 1. The database first: pg_dump reads one consistent snapshot while the site keeps running.
pg pg_dump -Fc | encrypt "db-$TS.dump"
pg psql -tAc "select 'ile-backup: $TS rows: migrations=' || (select count(*) from django_migrations) || ' users=' || (select count(*) from accounts_user) || ' documents=' || (select count(*) from documents_privatedocument)"
# 2. Then the files, so that every document row of the dump has its file.
archive -C /var/lib/italylegalentry -czf - private | encrypt "private-$TS.tar.gz"
archive -C /var/lib/italylegalentry -czf - media | encrypt "media-$TS.tar.gz"
# 3. The configuration: the environment file (secrets), nginx, the TLS private keys, the units, the two scripts.
config=()
for path in etc/italylegalentry etc/letsencrypt etc/nginx/sites-available/italylegalentry \
            etc/nginx/sites-available/00-catch-all etc/nginx/snippets/italylegalentry-proxy.conf \
            etc/systemd/system/italylegalentry* usr/local/sbin/ile-manage usr/local/sbin/ile-backup; do
  if [ -e "$path" ]; then config+=("$path"); fi
done
tar -czf - "${config[@]}" | encrypt "config-$TS.tar.gz"
# 4. Checksums of the encrypted files, by relative name: `sha256sum -c` works wherever the set is copied.
(cd "$WORK" && sha256sum -- *.gpg > "SHA256SUMS-$TS")
mv -- "$WORK"/* "$BACKUPS"/
echo "ile-backup: $TS written: $(cd "$BACKUPS" && echo *-"$TS".*.gpg "SHA256SUMS-$TS")"
# 5. Local retention - the sets, a forgotten rollback dump of runbook step 15, the remains of an interrupted run -
#    then the copy off the server.
find "$BACKUPS" -maxdepth 1 -type f \( -name '*.gpg' -o -name 'SHA256SUMS-*' -o -name 'pre-update-*.dump' \) \
     -mtime +"$KEEP_LOCAL_DAYS" -delete
find "$BACKUPS" -maxdepth 1 -type d -name '.partial-*' -mmin +720 -exec rm -rf {} +
[ -x "$OFFSITE" ] || { echo "ile-backup: $TS NOT COPIED OFF THE SERVER - install $OFFSITE (runbook, step 10)" >&2; exit 2; }
"$OFFSITE" "$BACKUPS" "$TS"
echo "ile-backup: $TS copied off the server"
EOF
sudo chmod 0700 /usr/local/sbin/ile-backup
sudo tee /etc/systemd/system/italylegalentry-backup.service >/dev/null <<'EOF'
[Unit]
Description=Italy Legal Entry - encrypted backup (/usr/local/sbin/ile-backup)
After=postgresql.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/ile-backup
Nice=10
IOSchedulingClass=idle
TimeoutStartSec=3h
PrivateTmp=yes
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=/var/backups/italylegalentry
EOF
sudo tee /etc/systemd/system/italylegalentry-backup.timer >/dev/null <<'EOF'
[Unit]
Description=Schedule of italylegalentry-backup

[Timer]
OnCalendar=*-*-* 01:30:00 Europe/Rome
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
EOF
sudo systemd-analyze verify /etc/systemd/system/italylegalentry-backup.service /etc/systemd/system/italylegalentry-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable --now italylegalentry-backup.timer
```

**3. The copy off the server.** `ile-backup` calls `/etc/italylegalentry/backup-offsite <directory> <timestamp>`. An
example to adapt: rsync over SSH to a machine the owner controls, with a key that serves for nothing else.
Prefer a destination where that key may add files but not delete them (an append-only account, or object storage
with versioning and its own lifecycle rule): a compromised server must not be able to erase its own backups.

```bash
sudo ssh-keygen -t ed25519 -N '' -C italylegalentry-backup -f /etc/italylegalentry/backup-ssh-key
#   authorise /etc/italylegalentry/backup-ssh-key.pub at the destination, for that one account
sudo ssh-keyscan -t ed25519 "<backup-host>" | sudo tee /etc/italylegalentry/backup-known-hosts
#   compare that key's fingerprint with the one the destination shows itself
sudo tee /etc/italylegalentry/backup-offsite >/dev/null <<'EOF'
#!/bin/sh
# Copies one backup set off the server: $1 = the backup directory, $2 = the set's timestamp (called by ile-backup).
# AN EXAMPLE TO ADAPT - the destination is the owner's decision (EU location, CR-08; who can read and delete there).
# Here: rsync over SSH to a machine the owner controls, with a key that serves for nothing else.
set -eu
DEST="<backup-user>@<backup-host>:<backup-path>/"
case "$DEST" in *"<"*) echo "backup-offsite: set DEST in $0 first" >&2; exit 1 ;; esac
cd "$1"
exec rsync -a --chmod=F0600 \
  -e "ssh -i /etc/italylegalentry/backup-ssh-key -o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/etc/italylegalentry/backup-known-hosts" \
  -- *-"$2".*.gpg "SHA256SUMS-$2" "$DEST"
EOF
sudo chmod 0700 /etc/italylegalentry/backup-offsite
sudoedit /etc/italylegalentry/backup-offsite      # set DEST
```

**4. The first run**, by hand, and what it must say:

```bash
sudo systemctl start italylegalentry-backup.service    # returns when the set is written and copied
sudo journalctl -u italylegalentry-backup -n 20 --no-pager   # "rows: …", "written: …", "copied off the server"
sudo ls -l /var/backups/italylegalentry | tail -n 6
systemctl list-timers italylegalentry-backup.timer --no-pager
```

Until the off-server copy is configured, each run writes its set, then fails with «NOT COPIED OFF THE SERVER» — on
purpose: `systemctl --failed` shows it every morning. A failure of the dump or of an archive fails the run and leaves
nothing behind. A set counts as a backup only once it has been restored elsewhere: the restore drill is checklist
C-6 — at go-live, then quarterly (`docs/DEPLOYMENT_READINESS.md` §4.3). Exercised on 12 October 2026 against a local
PostgreSQL 17 and a throwaway key: the set, its off-server copy, `sha256sum -c` there, then C-6's restore and its
file check — and both checks fail as they must on a damaged copy or a missing file. Not exercised: systemd, `runuser`,
rsync over SSH.

## 11. nginx

nginx terminates TLS, redirects HTTP to HTTPS, serves **public media** under `/media/`, and passes everything else —
static files included, which WhiteNoise serves — to Gunicorn. WhiteNoise also decides how long a browser keeps each
static file — a hashed name of the current release ten years, `immutable`; any other name 60 s: a plain name, or a
previous release's hashed name, kept for the pages still open, whose content never changes ([step 8](#8-static-files-seeds-site-first-administrator))
— so there is deliberately **no `location /static/`** here: one `expires` would give both kinds of name one rule, and a
long one on a plain name brings back the stale module. Should `/static/` ever be served by nginx itself (an `alias` of
the collected directory), it must keep the distinction: `expires max` with `immutable` only for a name that carries
Django's twelve-hex-digit hash (`~ "\.[0-9a-f]{12}\.[A-Za-z0-9]+$"`), `expires 60s` for every other. **There is no location, alias or root for the private
documents directory, and there must never be one** (not even an `internal` location for `X-Accel-Redirect`: the
application streams private files itself, after authorisation). While the application is stopped — an update, a
restore — nginx answers a static maintenance page with a 503 instead of its bare 502.

```bash
sudo tee /etc/nginx/snippets/italylegalentry-proxy.conf >/dev/null <<'EOF'
# Italy Legal Entry - headers the production settings rely on (config/settings/prod.py, apps/core/privacy.py).
proxy_pass http://italylegalentry_app;
proxy_set_header Host $host;
# USE_X_FORWARDED_HOST: Django reads the host from here; overwrite whatever the client sent.
proxy_set_header X-Forwarded-Host $host;
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https").
proxy_set_header X-Forwarded-Proto $scheme;
# OVERWRITE, never append: core.privacy reads the first entry, allauth the last (ALLAUTH_TRUSTED_PROXY_COUNT=1).
proxy_set_header X-Forwarded-For $remote_addr;
# core.middleware.RequestIDMiddleware keeps an alphanumeric id: one id in nginx's log and Django's.
proxy_set_header X-Request-ID $request_id;
proxy_redirect off;
# Defence in depth: the application never sends X-Accel-Redirect, and nginx would not follow one if it did.
proxy_ignore_headers X-Accel-Redirect;
proxy_connect_timeout 5s;
proxy_send_timeout 65s;
proxy_read_timeout 65s;
EOF

sudo tee /etc/nginx/sites-available/italylegalentry >/dev/null <<'EOF'
# Italy Legal Entry - reverse proxy (docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md, step 11).
upstream italylegalentry_app {
    server unix:/run/italylegalentry.sock fail_timeout=0;
}

# The access log keeps the client address with its last part zeroed: the application itself never stores a raw IP
# (apps/core/privacy.py). Switch to the "combined" format only by decision, with a short retention.
map $remote_addr $italylegalentry_client {
    ~^(?<prefix>\d+\.\d+\.\d+)\.\d+$                      $prefix.0;
    ~^(?<prefix>[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+):  $prefix::;
    default                                               -;
}
log_format italylegalentry '$italylegalentry_client [$time_iso8601] "$request_method $uri $server_protocol" '
                           '$status $body_bytes_sent $request_time "$host" $request_id';

server {
    listen 80;
    listen [::]:80;
    server_name __DOMAIN__;
    server_tokens off;
    access_log /var/log/nginx/italylegalentry.access.log italylegalentry;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
        default_type "text/plain";
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name __DOMAIN__;

    # Until the Let's Encrypt certificate exists: the self-signed pair of package ssl-cert (TLS section).
    ssl_certificate     /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_session_timeout 1d;
    ssl_session_cache shared:italylegalentry_tls:10m;
    ssl_session_tickets off;
    server_tokens off;

    # documents.services.MAX_UPLOAD_BYTES = 10 MiB per file, plus the multipart envelope.
    client_max_body_size 12m;
    access_log /var/log/nginx/italylegalentry.access.log italylegalentry;
    error_log  /var/log/nginx/italylegalentry.error.log warn;

    # The application stopped (an update, a restore) or unreachable: a static page and a 503, never nginx's bare 502.
    # Errors the application itself returns (a 503 of /healthz/, say) pass through untouched. A URI, not a named
    # location: nginx then serves the page to a POST too (as a GET), where a named location would answer 405.
    error_page 502 503 504 =503 /maintenance.html;
    location = /maintenance.html {
        root /var/www/italylegalentry-maintenance;
        add_header Cache-Control "no-store" always;
        add_header Retry-After "300" always;
    }

    # A second layer (checklist A-13, F-5): the application's own /backoffice/login/ signs no one in and sends the
    # visitor to allauth's sign-in, which runs the TOTP stage; nginx does the same here, with the same ?next=.
    location = /backoffice/login/ {
        return 302 /fr/compte/login/$is_args$args;
    }

    # PUBLIC media only: the media library's photographs, the Forum's public photos, videos and PDFs, the logo.
    location /media/ {
        alias /var/lib/italylegalentry/media/;
        limit_except GET HEAD { deny all; }
        expires 7d;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Cross-Origin-Resource-Policy "same-origin" always;
    }

    # Back-office uploads: the Forum's photos and videos reach 60 MiB (forum.validators.MEDIA_MAX_BYTES).
    location /backoffice/ {
        client_max_body_size 64m;
        include snippets/italylegalentry-proxy.conf;
    }

    location / {
        include snippets/italylegalentry-proxy.conf;
    }
}
EOF
sudo sed -i "s/__DOMAIN__/$ILE_DOMAIN/g" /etc/nginx/sites-available/italylegalentry
sudo ln -sf /etc/nginx/sites-available/italylegalentry /etc/nginx/sites-enabled/italylegalentry
sudo tee /var/www/italylegalentry-maintenance/maintenance.html >/dev/null <<'HTML'
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Italy Legal Entry</title>
</head>
<body style="font-family: system-ui, sans-serif; max-width: 36rem; margin: 4rem auto; padding: 0 1rem; line-height: 1.5">
<h1>Italy Legal Entry</h1>
<p lang="fr">Le site est momentanément indisponible. Merci de réessayer dans quelques minutes.</p>
<p lang="it">Il sito è momentaneamente non disponibile. Riprovi tra qualche minuto.</p>
<p lang="en">The site is temporarily unavailable. Please try again in a few minutes.</p>
<p lang="ar" dir="rtl">الموقع غير متاح مؤقتًا. يُرجى المحاولة مرة أخرى بعد بضع دقائق.</p>
</body>
</html>
HTML
```

**Catch-all server — fresh server only.** Requests whose `Host` is not the domain must never reach Django: they are
scanners' noise, each one a `DisallowedHost` line in the journal (Django answers them with its 400 page, checklist
A-21). On a server where no other site declares `default_server` (`grep -R default_server /etc/nginx/sites-enabled/`
prints nothing once nginx's placeholder site is removed):

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/00-catch-all >/dev/null <<'EOF'
# Answers nothing to a request for a host this server does not serve.
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;
    ssl_reject_handshake on;
    return 444;
}
EOF
sudo ln -sf /etc/nginx/sites-available/00-catch-all /etc/nginx/sites-enabled/00-catch-all
```

On an *existing* server that already has a `default_server`, leave it: unknown hosts go to that site, not here.

```bash
sudo nginx -t && sudo systemctl reload nginx
```

**`www`.** Serve one canonical host. If `www.<your-domain>` must answer, include it in the certificate (TLS section)
and add a server block that only redirects:
`server { listen 443 ssl http2; server_name www.<your-domain>; ssl_certificate …; ssl_certificate_key …; return 301 https://<your-domain>$request_uri; }`
— and add `www.<your-domain>` to the port-80 `server_name`.

## 12. Health checks

`GET /healthz/` (`apps/core/views.py`) runs `SELECT 1` and answers `{"status": "ok", "database": true}` with 200,
or 503 with `"degraded"`. It needs a `Host` from `DJANGO_ALLOWED_HOSTS` and, behind the HTTPS redirect,
`X-Forwarded-Proto: https`.

```bash
# On the server, through the socket (root may connect to it):
sudo curl -fsS --unix-socket /run/italylegalentry.sock -H "Host: $ILE_DOMAIN" -H "X-Forwarded-Proto: https" http://localhost/healthz/
# Through nginx, before DNS points here (self-signed certificate, hence -k):
curl -fsSk --resolve "$ILE_DOMAIN:443:127.0.0.1" "https://$ILE_DOMAIN/healthz/"
# From anywhere, after the cutover — the URL for an external uptime monitor:
curl -fsS "https://$ILE_DOMAIN/healthz/"
```

What it does **not** cover, and how to look at it instead:

| Concern | Check |
|---|---|
| timers ran and did not fail | `systemctl list-timers 'italylegalentry-*' --no-pager` · `systemctl --failed` |
| mail is leaving | `sudo ile-manage shell -c "from django.db.models import Count; from notifications.models import EmailOutbox; print(dict(EmailOutbox.objects.values_list('status').annotate(n=Count('id'))))"` — a growing `queued` or `failed` count is the alarm |
| private storage writable and not full | `sudo df -h /var/lib/italylegalentry` · an upload in the smoke test |
| no rule in force without approval | `sudo ile-manage rules_pending_review --strict` (exit 0) |
| certificate validity | `sudo certbot certificates` |
| the backup ran and left the server | `systemctl status italylegalentry-backup.service --no-pager` (the last run succeeded) · `sudo journalctl -u italylegalentry-backup -n 5 --no-pager` («copied off the server») · the newest set at the destination |

An endpoint covering storage and the mail queue does not exist; adding one is an open question for the owner, not
something this runbook invents.

## 13. Logs

| Source | Where | Read it |
|---|---|---|
| Gunicorn and Django (one JSON object per line from Django, with `request_id`) | journald, unit `italylegalentry` | below |
| Scheduled jobs and the backup | journald, units `italylegalentry-*` | `sudo journalctl -u 'italylegalentry-*' --since yesterday` · `sudo journalctl -u italylegalentry-documents-purge-expired -n 20` |
| nginx | `/var/log/nginx/italylegalentry.access.log` (client address masked), `…error.log` | `sudo tail -f /var/log/nginx/italylegalentry.access.log` · rotated daily, 14 days (`/etc/logrotate.d/nginx`) |

**Look for errors in the content, never with `journalctl -p`.** journald files every line a service writes at the
unit's level (info) unless the line starts with a `<N>` priority prefix — and neither Django's JSON lines nor
Gunicorn's `[ERROR]` lines carry one. `journalctl -u italylegalentry -p err` therefore stays empty while the
application answers 500s. The error check of this runbook — cutover step 2, smoke test D-20, after every update — is:

```bash
# Errors and critical lines of the last hour: must print 0.
sudo journalctl -u italylegalentry --since -1h -o cat --no-pager | grep -cE '"level": "(ERROR|CRITICAL)"|\[(ERROR|CRITICAL)\]'
# Warnings, to read rather than to hold to 0 (Django logs every 404 as one):
sudo journalctl -u italylegalentry --since today -o cat --no-pager | grep -E '"level": "WARNING"|\[WARNING\]' | tail -n 20
sudo journalctl -u italylegalentry -f                        # follow; `-o cat | grep '^{'` keeps Django's lines only
```

`sudo`, because an account outside the `adm` and `systemd-journal` groups sees no system unit's lines at all — and a
count of nothing is 0 as well.

- One request, one id: the `X-Request-ID` response header, the last field of the nginx line and the `request_id` of
  Django's line are the same value.
- The application logs identifiers, never personal data (`tests/security/test_log_privacy.py`). The nginx log does
  carry paths, and three kinds of path hold a token: `/documents/link/<token>/` (bound to one account, valid
  10 minutes: `documents.services.DOWNLOAD_LINK_TTL`), the password-reset links
  `/<lang>/compte/password/reset/key/<uid>-<key>/` (valid 3 days: Django's `PASSWORD_RESET_TIMEOUT`, not overridden)
  and the e-mail confirmation links `/<lang>/compte/confirm-email/<key>/` (3 days:
  `ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS`). Keep the logs readable by root and `adm` only (the default) and the
  retention short.
- journald's retention is the owner's policy: `SystemMaxUse=` / `MaxRetentionSec=` in `/etc/systemd/journald.conf`.

## 14. Restart, reload, stop

| Situation | Command |
|---|---|
| changed environment file | `sudo systemctl restart italylegalentry.service` — the socket stays open, requests wait |
| new release | [step 15](#15-updating-to-a-new-release): stop everything, update, start again |
| graceful worker recycle only | `sudo systemctl reload italylegalentry.service` (HUP: new workers, fresh imports) |
| nginx configuration | `sudo nginx -t && sudo systemctl reload nginx` |
| **stop everything** (update, restore, maintenance) — the service and its socket, the timers, and any job or backup running | `sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service` |
| start again | `sudo systemctl start italylegalentry.socket italylegalentry.service && sudo systemctl start $(systemctl list-unit-files 'italylegalentry-*.timer' --no-legend \| cut -d' ' -f1)` |

Stopping only `italylegalentry.service` is not a stop: the socket stays open and the next request starts the service
again. Stop the socket too. While both are stopped, nginx answers the maintenance page with a 503 (step 11).

## 15. Updating to a new release

The application is **stopped while its code changes.** Gunicorn loads the application in each worker as the worker
starts, and recycles one every ~1000 requests or after a timeout: a worker started between the checkout and the
restart would run the new code against the old schema and the old static manifest (500s for real visitors), and a
half-replaced package can keep a worker from booting at all. Meanwhile nginx answers the maintenance page with a 503
(step 11). The window lasts from step 3 to step 9 — time it at the first update.

1. Read the new handoff: tag, SHA, migration notes, anything flagged as destructive, the seeds that changed.
2. Before the window, while the site runs — fetch the tag, look at what changes, and take a backup set off the
   server:

```bash
sudo git -C /srv/italylegalentry/app fetch --tags
sudo git -C /srv/italylegalentry/app diff --stat HEAD "refs/tags/$ILE_TAG" -- requirements/ 'apps/*/migrations/'
sudo /usr/local/sbin/ile-backup                     # encrypted, copied off the server (step 10)
```

3. **The window opens** — stop the service, its socket, the timers, and any job or backup running:

```bash
sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service
curl -sk -o /dev/null -w '%{http_code}\n' --resolve "$ILE_DOMAIN:443:127.0.0.1" "https://$ILE_DOMAIN/fr/"   # 503: the maintenance page
```

4. **The rollback point** — a dump of the stopped database, checked by a restore. It stays on the server, readable by
   root alone — the same protection as the database it copies — until the release is accepted; `ile-backup` deletes
   any one left after 7 days:

```bash
TS=$(date -u +%Y%m%dt%H%Mz)
sudo sh -c 'runuser -u postgres -- pg_dump -Fc -d italylegalentry > "/var/backups/italylegalentry/pre-update-$1.dump"' sh "$TS"
sudo -u postgres createdb -O italylegalentry italylegalentry_restore_test
sudo cat "/var/backups/italylegalentry/pre-update-$TS.dump" | sudo -u postgres pg_restore --no-owner --role=italylegalentry -d italylegalentry_restore_test
for db in italylegalentry italylegalentry_restore_test; do
  sudo -u postgres psql -d "$db" -tAc "select '$db', (select count(*) from django_migrations), (select count(*) from accounts_user), (select count(*) from documents_privatedocument)"
done                                    # the two lines must match
sudo -u postgres dropdb italylegalentry_restore_test
```

5. Code: `sudo git -C /srv/italylegalentry/app checkout --detach "refs/tags/$ILE_TAG"`, then the SHA test of step 3.
6. Dependencies: `sudo /srv/italylegalentry/venv/bin/python -m pip install --no-cache-dir -r /srv/italylegalentry/app/requirements/base.txt -c /srv/italylegalentry/app/requirements/constraints.txt && sudo /srv/italylegalentry/venv/bin/python -m pip check`.
7. `sudo ile-manage check --deploy`; `sudo ile-manage migrate --plan` — read it; then
   `sudo ile-manage migrate --noinput && sudo ile-manage migrate --check`.
8. `sudo ile-manage collectstatic --noinput` (never `--clear`) and `sudo ile-manage seed_all` — safe at every release:
   every seed creates what is missing and none rewrites what staff edited (step 8). If the handoff flags a seed as
   rewriting, run only the new ones: `sudo ile-manage seed_all --only <name prefix>`.
9. **The window closes** — start everything again (step 14, «start again»), then the error check of step 13: 0.
10. Smoke test — checklist §D. Write down: tag, SHA, time, the backup set's timestamp, the rollback dump's name.
11. Anything wrong: [`ROLLBACK.md`](ROLLBACK.md). The release accepted (72 hours without a rollback), delete the
    rollback dump — it holds personal data in clear: `sudo rm /var/backups/italylegalentry/pre-update-<TS>.dump`.

Better, later: one directory and one virtual environment per release (`/srv/italylegalentry/releases/<tag>`), migrated
and collected from there, a `current` symlink switched, then a restart; a rollback switches the symlink back. It keeps
the window to the migration alone. Not done here: the paths above are a single checkout.

---

## STATIC ASSETS vs PUBLIC MEDIA vs PRIVATE USER DOCUMENTS

Verified against the code on 12 October 2026.

| | STATIC ASSETS | PUBLIC MEDIA | PRIVATE USER DOCUMENTS |
|---|---|---|---|
| What | the design's CSS and JS bundles, fonts, icons, images; the back-office's assets | the media library's photographs (`seed_all` copies them from `static/img/photos`), the Forum's public photos, videos and PDFs, the optional logo — uploaded by staff in the back-office, public by nature (`forum/validators.py`: «only public, non-personal material») | identity documents, contracts, diplomas a person files into their case (`documents` app) |
| Where | sources `static/` and `apps/*/static/`; collected into `STATIC_ROOT` = `<checkout>/staticfiles` | `MEDIA_ROOT` = `/var/lib/italylegalentry/media` (`prod.py`, environment) | `PRIVATE_MEDIA_ROOT` = `/var/lib/italylegalentry/private`, one directory per owner, a `uuid4` name per file, mode `0600` (`documents/storage.py`, `services.py`) |
| Served by | **Gunicorn through WhiteNoise** (`base.py` middleware and `STORAGES`, `core/storage.py`): every file a page loads is a hashed name — the ES modules' imports included — with a `.gz` sibling, `Cache-Control: max-age=315360000, public, immutable` for a name of the current release; a plain name, or a previous release's hashed name, `max-age=60, public` (step 8) | **nginx**, `location /media/` with `alias` — Django serves `/media/` only when DEBUG is on (`config/urls.py`) | **only** `documents.views._serve`, after login, `documents.policies.require(user, "download", doc)` and `services.delivery_block`; as an attachment, `Cache-Control: private, no-store`, `Content-Security-Policy: default-src 'none'; sandbox`; every delivery audited (`documents.downloaded`) |
| URL | `/static/<path>.<hash>.<ext>` | `/media/<path>` | `/documents/<uuid>/` and `/documents/link/<signed, time-limited, account-bound token>/` — no file path appears in any URL |
| Backup | no: rebuilt from the tag by `collectstatic` | **yes**: back-office uploads exist only here (the library photographs can be re-seeded) — nightly, encrypted (step 10) | **yes**: nightly with the database, encrypted to the owner's key before anything is written (step 10) |

**Why a private document can never be reached through a web-server alias:**

1. The runbook's nginx has no location, alias or root for the private directory — and nginx could not read it if it
   had: the directory is `0700`, owned by `italylegalentry`; nginx runs as `www-data`.
2. The private root overlaps no served directory. `config/settings/prod.py` refuses to start — even through
   `ILE_ALLOW_INSECURE_PROD` — when `PRIVATE_MEDIA_ROOT` overlaps `MEDIA_ROOT`, `STATIC_ROOT` or `STATICFILES_DIRS`
   (WhiteNoise indexes `STATIC_ROOT` at start-up, so a file there would be public after a restart);
   `documents.storage.private_root()` refuses `MEDIA_ROOT` again at the first upload.
3. The private storage has no URL (`PrivateFileSystemStorage.url` raises) and the document model has no `FileField`
   (`documents/models.py`): no template can print a file's address.
4. In production no URL pattern serves files from disk at all.
5. Every delivery runs the object-level policy again, signed link or not.

Tests that prove it: `apps/documents/tests/test_download.py` (anonymous → login, another account → 403 even with the
UUID, staff roles, infected files never, soft-deleted files hidden, both routes rate-bounded) ·
`apps/documents/tests/test_signed_links.py` (a link is inert in another account, forged or expired tokens refused,
the policy still runs on a valid link) · `tests/security/test_authorization_audit.py`
(`test_a_known_document_url_serves_nobody_but_its_owner`, `test_the_private_media_root_is_not_served_by_the_web_server`) ·
`apps/documents/tests/test_upload.py` (`test_private_storage_refuses_media_root`, `test_private_file_is_not_served_under_media`) ·
`tests/deployment/test_private_documents_are_never_served.py` (no URL pattern and no setting exposes the private root,
under the production settings) · `tests/security/test_production_settings_refuse_to_start.py` (the boot refusal) ·
`tests/deployment/test_runbook_matches_the_code.py` (this runbook's nginx never names the private directory).

## TLS / HTTPS

The order matters, and **nothing here is to be done before the [cutover sequence](#domain-cutover-sequence) says so**:

1. **DNS resolution first.** Let's Encrypt's HTTP challenge reaches the host the domain resolves to. A certificate
   for the domain can be issued only once its A (and AAAA) records point at this droplet — or, for the temporary
   host, once that host's record does.
2. **Reverse proxy ready.** nginx answers on port 80 with the ACME location of step 11 and serves HTTPS with the
   self-signed pair meanwhile (enough for `curl -k`, not for browsers).
3. **Issue** — webroot method, which leaves the nginx configuration as written, under one stable certificate name
   (`italylegalentry`), so the paths in nginx never change when the list of names does:

   ```bash
   # Cutover step 3, option A — the temporary host only (the domain cannot validate before its DNS moves):
   sudo certbot certonly --webroot -w /var/www/letsencrypt --cert-name italylegalentry \
        -d "$ILE_STAGING_HOST" --deploy-hook "systemctl reload nginx"
   # Cutover step 7 — the domain, with every name nginx still serves: the temporary host stays in the certificate
   # until cutover step 8 retires it (${ILE_STAGING_HOST:+…} adds it only when the variable is set), and add
   # -d "www.$ILE_DOMAIN" if www is served. certbot asks to confirm the new list of names:
   sudo certbot certonly --webroot -w /var/www/letsencrypt --cert-name italylegalentry \
        -d "$ILE_DOMAIN" ${ILE_STAGING_HOST:+-d "$ILE_STAGING_HOST"} --deploy-hook "systemctl reload nginx"
   # The first time a Let's Encrypt certificate exists, point nginx at it instead of the self-signed pair:
   sudo sed -i -e 's|/etc/ssl/certs/ssl-cert-snakeoil.pem|/etc/letsencrypt/live/italylegalentry/fullchain.pem|' \
               -e 's|/etc/ssl/private/ssl-cert-snakeoil.key|/etc/letsencrypt/live/italylegalentry/privkey.pem|' \
               /etc/nginx/sites-available/italylegalentry
   sudo nginx -t && sudo systemctl reload nginx
   echo | openssl s_client -connect "$ILE_DOMAIN:443" -servername "$ILE_DOMAIN" 2>/dev/null | openssl x509 -noout -issuer -subject -dates
   ```

4. **Automated renewal.** The Ubuntu package installs `certbot.timer` (twice a day); the deploy hook given at issuance
   is kept in `/etc/letsencrypt/renewal/italylegalentry.conf` and reloads nginx after each renewal.

   ```bash
   systemctl list-timers certbot.timer --no-pager
   sudo certbot renew --dry-run
   ```

5. **HTTP → HTTPS.** nginx's port-80 server answers every path but the ACME one with a 301 to HTTPS; Django's
   `SECURE_SSL_REDIRECT` (on, refused off) redirects again whatever reaches it as plain HTTP.
6. **Django's secure headers** (`config/settings/prod.py`, `base.py`, `core.middleware`): HSTS
   (`SECURE_HSTS_SECONDS` = one year, refused lower), `Secure` + `HttpOnly` + `SameSite=Lax` cookies (session, CSRF,
   language), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy:
   strict-origin-when-cross-origin`, `Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Resource-Policy`,
   `Permissions-Policy`, and a self-only Content-Security-Policy. nginx adds none of them to proxied responses (no
   duplicates); it adds `nosniff` and CORP to the media it serves itself.

**HSTS — read before turning anything on.** The application sends `Strict-Transport-Security` from its first HTTPS
response, and a browser that has seen it refuses plain HTTP to that host for the max-age — a year.

- `includeSubDomains` extends that refusal to **every subdomain** of the host it is sent from. On the apex domain, a
  subdomain that still serves HTTP only, or a certificate that does not match (a parked CNAME, an old service, a
  mail web interface), becomes unreachable for every visitor of the site. The template therefore starts with
  `SECURE_HSTS_INCLUDE_SUBDOMAINS=0`: inventory the domain's DNS records first, confirm each answering host serves
  valid HTTPS, then set it to `1` and restart.
- `preload` is a request to be hard-coded into browsers. Sending the directive is harmless on its own; **submitting
  the domain to the preload list is a separate, near-permanent decision** — removal takes months — and must not be
  made during the cutover. The template starts with `SECURE_HSTS_PRELOAD=0`.
- While either is `0`, `check --deploy` reports `security.W005` / `security.W021`: expected, and justified by the
  pending inventory. `prod.py` has no default for either: the environment file states `0` or `1`, and a missing
  line stops the application, so the decision is always made for this domain, never inherited.
- Optional, at the DNS host, later: a `CAA` record allowing `letsencrypt.org` only.

## DOMAIN: REGISTRAR TRANSFER vs DNS CUTOVER

Two different operations. **The deployment depends only on the second.**

| | REGISTRAR TRANSFER | DNS CUTOVER |
|---|---|---|
| What changes | which company the domain is registered with (ownership record, renewal, billing) | where the domain's **web records** point: the `A` (and `AAAA`) records of the apex and of `www` |
| Where it is done | between the current registrar and a new one (authorisation code, unlock, confirmation; a 60-day transfer lock follows) | in the DNS zone, wherever it is hosted today — usually the current registrar's DNS panel |
| What it touches | nothing visible if done right — and a lot if the nameservers change with it | only the records changed; MX (mail), TXT (SPF, DKIM, verification) and every other record stay as they are |
| Needed for this deployment | **no** | **yes** — that is the cutover |

A third operation exists and is **not needed either**: moving the zone's hosting to DigitalOcean DNS (changing the
nameservers at the registrar). It would require re-creating every record — mail first — before the switch, and it
multiplies the risk of the cutover window. If the owner ever wants it, or a registrar transfer, it is a separate
change in a separate window, after the new site is stable. The domain stays with its registrar; the droplet only
needs its public address in two records.

## DOMAIN CUTOVER SEQUENCE

The owner's sequence, with what to check at each step. **Do not start a step before the previous one is checked.**
Nothing here is done before the owner decides to cut over.

**1. NEW SERVER READY.** Steps 1–14 done.

```bash
systemctl is-active italylegalentry.socket italylegalentry.service nginx postgresql   # four lines: active
systemctl list-timers 'italylegalentry-*' --no-pager                                    # eight: seven jobs, the backup
sudo grep -nE '^[^#].*<[^@>]*>' /etc/italylegalentry/italylegalentry.env || echo "no placeholder left"
sudo ile-manage check --deploy          # only security.W005 / W021 while the HSTS inventory is pending
```

Write down the release tag and its SHA.

**2. APPLICATION HEALTHY.**

```bash
sudo curl -fsS --unix-socket /run/italylegalentry.sock -H "Host: $ILE_DOMAIN" -H "X-Forwarded-Proto: https" http://localhost/healthz/
sudo journalctl -u italylegalentry --since -1h -o cat --no-pager | grep -cE '"level": "(ERROR|CRITICAL)"|\[(ERROR|CRITICAL)\]'   # 0 (step 13)
sudo ile-manage migrate --check && echo "migrations applied"
```

**3. TEMPORARY/STAGING HOST VALIDATED.** Validate the real stack before the real domain moves.

- **Option A (recommended): a temporary host name** — for example a new subdomain — whose **new** `A` record points
  at the droplet. Creating a new record does not touch the live site's records.

  ```bash
  export ILE_STAGING_HOST=new.example.com    # replace
  sudoedit /etc/italylegalentry/italylegalentry.env   # DJANGO_ALLOWED_HOSTS: add the temporary host; CSRF: its https:// origin
  sudo sed -i "s/server_name $ILE_DOMAIN;/server_name $ILE_DOMAIN $ILE_STAGING_HOST;/" /etc/nginx/sites-available/italylegalentry
  sudo nginx -t && sudo systemctl reload nginx
  sudo certbot certonly --webroot -w /var/www/letsencrypt --cert-name italylegalentry -d "$ILE_STAGING_HOST" --deploy-hook "systemctl reload nginx"
  # then the sed of TLS step 3 (self-signed -> Let's Encrypt paths), and:
  sudo systemctl restart italylegalentry.service
  ```

  Run the whole smoke test (checklist §D) on `https://$ILE_STAGING_HOST`: the four languages, Arabic in RTL, sign-in
  with TOTP enrolment, an upload and a download of a private document, `sendtestemail`, the back-office.
- **Option B: no DNS at all** — from your workstation, `curl -k --resolve "<domain>:443:<droplet address>" https://<domain>/healthz/`
  and the same for the pages. A browser cannot replace curl here if the current site already sends HSTS for the
  domain: browsers then refuse to bypass the self-signed certificate's warning.

**4. BACKUP CONFIRMED.** Checklist §C done **and verified**: the first backup set of the new server written,
copied off the server, and restored elsewhere (C-6) — database, private documents, public media, configuration. The current site's own backup is confirmed by whoever operates it: the
current site is the DNS rollback target and stays running, untouched.

**5. DNS TTL PREPARED.** At least 24–48 hours before the change, at the current DNS host: the TTL of the apex and
`www` records — `A` **and** `AAAA` — lowered to 300 seconds.

```bash
for name in "$ILE_DOMAIN" "www.$ILE_DOMAIN"; do
  for type in A AAAA CAA; do dig +noall +answer "$name" "$type"; done
done                                                                        # TTL column reads 300 once the old TTL expired
dig +noall +answer "$ILE_DOMAIN" MX                                         # written down; never changed by the cutover
```

Write down the current values of every record shown: they are the rollback. An `AAAA` record matters as much as the
`A`: IPv6 visitors follow it, and so does Let's Encrypt, which prefers IPv6.

**6. DOMAIN DNS POINTED TO DIGITALOCEAN.** At the current DNS host, change only the web records of the apex and `www`:

- `A` → the droplet's public address;
- `AAAA` → the droplet's IPv6 address if it has one (nginx listens on `[::]`), otherwise **remove** the old `AAAA`
  records — left in place they keep IPv6 visitors on the old site and make step 7 fail, Let's Encrypt validating
  against the old host;
- a `CAA` record, if one exists, must allow `letsencrypt.org`.

No registrar transfer, no nameserver change, no MX or TXT change.

```bash
dig @1.1.1.1 +short "$ILE_DOMAIN" A ; dig @8.8.8.8 +short "$ILE_DOMAIN" A         # the droplet's address, from both
dig @1.1.1.1 +short "$ILE_DOMAIN" AAAA ; dig @8.8.8.8 +short "$ILE_DOMAIN" AAAA   # the droplet's IPv6, or nothing
dig +short "$ILE_DOMAIN" CAA                                                      # nothing, or letsencrypt.org allowed
```

**Between steps 6 and 7 visitors see a certificate warning.** Until the certificate exists, a visitor whom DNS
already sends here gets the temporary certificate — the temporary host's, or the self-signed pair — and a browser
that already holds HSTS for the domain offers no way past it. Keep the window short: change the records at a quiet
hour and run step 7 as soon as both resolvers return the droplet's address. If the DNS host has an API that a certbot
DNS plugin supports, the certificate can instead be issued before the switch with the DNS-01 challenge — a plugin
package and an API token: the owner's decision.

**7. HTTPS CERTIFICATE.** TLS step 3 for the domain — every name nginx serves, the temporary host included until
step 8 — then TLS step 4. Without a temporary host (option B), nginx still points at the self-signed pair: run the
`sed` of TLS step 3 after this certificate.

```bash
sudo certbot certonly --webroot -w /var/www/letsencrypt --cert-name italylegalentry \
     -d "$ILE_DOMAIN" ${ILE_STAGING_HOST:+-d "$ILE_STAGING_HOST"} --deploy-hook "systemctl reload nginx"   # add -d "www.$ILE_DOMAIN" if www is served
sudo certbot renew --dry-run
curl -sI "https://$ILE_DOMAIN/fr/" | grep -i strict-transport-security
```

**8. ALLOWED_HOSTS / CSRF verification.** `DJANGO_ALLOWED_HOSTS` holds exactly the host names served,
`DJANGO_CSRF_TRUSTED_ORIGINS` their `https://` origins; restart after any change.

```bash
sudo grep -E '^(DJANGO_ALLOWED_HOSTS|DJANGO_CSRF_TRUSTED_ORIGINS)=' /etc/italylegalentry/italylegalentry.env
sudo systemctl restart italylegalentry.service
sudo journalctl -u italylegalentry --since -1h --no-pager | grep -c DisallowedHost    # 0
curl -s "https://$ILE_DOMAIN/sitemap.xml" | grep -m1 -o "<loc>[^<]*"                # https://<domain>/...
```

A sign-in (a POST) must succeed: a CSRF failure here means an origin is missing. When the temporary host is no longer
needed, remove it from both variables, from the `server_name` lines and from the certificate
(`sudo certbot certonly --webroot -w /var/www/letsencrypt --cert-name italylegalentry -d "$ILE_DOMAIN"`, with
`-d "www.$ILE_DOMAIN"` if www is served), then restart and reload.

**9. PRODUCTION SMOKE TEST.** Checklist §D on the real domain, every line.

**10. MONITOR.** For 72 hours: an external check of `https://<domain>/healthz/`, the error count of step 13 (0), 5xx
in the nginx log, the timers and the mail queue, the disk. Then weekly: the certificate (`sudo certbot certificates`),
the backup (the last run of `italylegalentry-backup.service` succeeded and was copied off the server; the newest set
is at the destination — step 12), the purge timers. Quarterly: a restore drill (checklist C-6).
Keep the current site intact until the TTL window **and** 72 hours have passed without a rollback; its
decommissioning is a separate decision.

## LEGACY

The legacy environment is **LEGACY_REFERENCE_ONLY** (owner's decisions V5.8, 11 October 2026, and V5.9). The
production deployment is a **clean deployment of the new application**:

- no automatic migration of legacy **users**, **documents**, **personal data**, **database**, **recruitment
  records**, **age criteria** or **secrets** — nothing from the legacy host is imported, attached, restored or
  copied into `MEDIA_ROOT`, `PRIVATE_MEDIA_ROOT` or the database;
- no legacy password, key or credential is reused: every secret of this deployment is generated in step 5;
- the legacy host is not infrastructure of the new platform and not a dependency of it;
- the old public URLs are handled by `cms.middleware.LegacyURLMiddleware` (redirects and 410s,
  `docs/URL_MIGRATION_MAP.md`) — URL compatibility, not data migration.

Any future data migration is a **separate project**, explicitly approved by the owner, with its own legal basis,
mapping, minimisation and verification. This runbook contains none.

## RELEASE TAGS

What the repository establishes: the platform labels itself with a semantic version — `v2.0.0 — Fase 1` is the
default of both `ILE_VERSION_LABEL` (`config/settings/base.py`) and `SiteSettings.version_label`
(`apps/core/models.py`, the value the footer shows), and `docs/DEPLOYMENT.md` gave `v2.0.0-phase1` as a tag example.
No release tag exists yet; the local `v54/*` and `checkpoint/*` tags are internal milestones and are never published.

Recommendation:

1. **Release candidate**: `v5-release-candidate` (the name of the owner's directive), created on the published
   commit once the release gate passes on it. A second candidate is `v5-release-candidate-2` — a tag is **never moved
   and never force-pushed**.
2. **Release**: a semantic version on the validated candidate's commit. The platform already declares `v2.0.0`, so
   `v2.0.0` keeps the tag, the footer label and the handoff saying the same thing; `v1.0.0` (the directive's example)
   is the alternative if the owner prefers to count the new platform from one. The owner chooses — once.
3. The server checks out the tag (`refs/tags/…`), never a branch, and compares `HEAD` with the SHA of the handoff
   (step 3). Tags are created on the **published** snapshot commit, so that SHA is GitHub's.
4. After deploying a release, set the label the footer shows: back-office → Site settings → version label.

## States

| State | Applies when | What it does not mean |
|---|---|---|
| **DEVELOPMENT_COMPLETE** | every V5 family is merged, nothing is left to build, the full suite is green on the integration branch | not tagged, not validated, not deployable |
| **RELEASE_CANDIDATE** | one commit, published to GitHub and tagged `v5-release-candidate`, on which the release gate's automated part passed (clean tree, synchronised, full suite, migrations clean, `check --deploy`, secret and personal-data scans) and final QA runs | not production-ready: the manual items and the go-live blockers may still be open |
| **PRODUCTION_READY** | the candidate passed **every** item of the release gate (checklist §A) with evidence, the go-live blockers are closed or accepted by the owner in writing, the release tag exists, and the final handoff is written | not deployed: the owner deploys and cuts over |

«GitHub pushed» is none of these.

## Known limits and external dependencies

- **Back-office sign-in path** — closed (F-5, checklist A-13), fixed by the sec-f5 lane: the back office's own
  sign-in signs no one in, and an account that holds a second factor presents it in every session before the back
  office, the reserved area or a private document opens (`apps/accounts/tests/test_backoffice_second_factor.py`,
  `docs/design-v5/QA/v54/sec-f5/NOTES.md`). The proof lasts as long as the session — 8 hours after its last write,
  the cookie ending with the browser; asking the code again within a session is a policy decision, not made.
- **Static modules** — every file a page loads is cached by its hashed name (step 8). That needs the import
  specifiers of `static/js/dist` to be string literals and its chains of imports to stay short (`core/storage.py`):
  each pass of Django's post-processing settles one more link of a chain it meets in the wrong order, that order
  follows the directory listing — hash order on the server's ext4 — and a name that needs more than four passes, or a
  cycle, stops `collectstatic` with «Max post-process passes exceeded». `tests/deployment/test_static_caching.py`
  computes the worst case over every directory order (2 of the 4 today) and refuses a computed `import(x)`: with
  `tests/frontend/test_static_pipeline.py`, at build time, in CI, never in front of a visitor. Only the dist is
  rewritten — no third-party script is read for imports. Django calls its rewriting of module imports experimental
  (4.2); the test reads the real minified dist.
- **NUL bytes** — a NUL in the query string, the session cookie or a form posted to a page that CSRF protects is
  answered with the project's 400 page, with the security headers of every page and one WARNING line
  (`cms.middleware.NulByteMiddleware`, `tests/deployment/test_nul_bytes.py`); until 16 October 2026 it was a 500 and an
  ERROR line with its traceback, one per request, for anyone (gate 2's N-4). Behind nginx a `%00` in the path never
  reaches Django: nginx answers its own bare 400. The body of a `csrf_exempt` view — the integrations API, the public
  webhook among them, which read their raw body — and a body that is not a form are left to their view; none stores a
  posted field. A body Django will not parse (too many fields, too large, malformed) is answered as without the guard:
  without its CSRF cookie, a 403.
- **SMTP** — a provider is required; account e-mails are sent during the request. Outbound SMTP is restricted on
  many DigitalOcean accounts: confirm the provider's port is open from the droplet (`sendtestemail`) before the
  cutover; 2525 is a common alternative to 587. Implicit TLS (465) is not configurable.
- **EU hosting (CR-08)** — region of the droplet, of the database and **of the backups**, the provider's
  sub-processors and the processing agreement, confirmed in writing (`docs/DEPLOYMENT_READINESS.md` §3 keeps the
  twelve-point list).
- **No antivirus** — uploads stay «not analysed», which the delivery rule states.
- **Backups** — where the off-server copy lives, who holds the private key, and the retention are the owner's
  decisions (step 10, checklist A-28). Until the copy is configured, the nightly backup writes its set and then fails,
  on purpose.
- **Rate limits per worker** — with the local-memory cache, allauth's and the forms' limits are counted per Gunicorn
  worker: up to three times the configured figure. Shared counting needs Redis and its client library — a new
  dependency, the owner's decision.
- **Python 3.12** — Ubuntu 24.04's interpreter; every source compiles under 3.12.10 and no 3.13-only library call is
  used, but the test suite runs on 3.13 in CI. Run it once on 3.12 before the release, or install 3.13.
- **PostgreSQL 16** on Ubuntu 24.04, 17 in development and CI; Django 5.2 supports both and the migrations contain
  no raw SQL.
- **The go-live blockers of `docs/PREPROD_REPORT.md` §15** — official Italian legal texts, jurist review of the rules,
  EU hosting confirmation, human review of the translations, a real screen-reader pass. None of them is code.
