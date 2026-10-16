# DevOps + security review — branch `v54-devops` (directive V5.9)

Reviewer `devops-review`, 12 October 2026. I built nothing on this branch.

Reviewed: `design-v5...v54-devops`, six commits `6484968` … `3de8c57` on base `1c03e3b`, 22 files, +3 057 / −166.
Read in full: the owner's directives V5.9 and V5.8; `PRODUCTION_DEPLOYMENT_RUNBOOK.md`, `PRODUCTION_CHECKLIST.md`,
`ROLLBACK.md`, `production.env.example`, `.env.example`, `NOTES.md`; the diffs of `config/settings/{prod,base}.py`,
`apps/core/{checks,apps}.py`, `docker-compose.staging.yml`, `README.md` and the two superseded documents; the four new
and two extended test modules. Read in the pinned sources: Gunicorn 26.2.0 (`arbiter.py`, `sock.py`, `systemd.py`,
`ctl/server.py`, `config.py`, `http/message.py`), allauth 65.19.4 (`core/internal/httpkit.py`, `account/adapter.py`),
Django 5.2.17 (`db/backends/base/schema.py`).

## Verdict: SHIP_AFTER_FIXES

**No P0.** No path serves a private document except `documents.views._serve`. No secret is in the repository. No hard
limit of the owner is crossed and nothing names the production server. The first deployment, typed as written, comes
up.

**Nine majors** in commands and procedures the owner will type, each of which bites later:

- the database password lands in sudo's log;
- no backup is taken after go-live, and the pre-cutover backup's checksum manifest comes out empty while its
  archives are copied off the server unencrypted;
- updates switch the code under a live service;
- the rollback rule misreads Django's `AddField`;
- the "no error" checks cannot see an error;
- Gunicorn 26 logs an error at every worker fork under this sandbox;
- the back-office MFA bypass is left open, though nginx could close it today;
- `seed_all` reverts the jurist's corrections at every release.

All are fixable in the documents, plus one seed, one test name and one optional line of `prod.py`. None needs a new
package.

## What I ran

| | Result |
|---|---|
| `pytest tests/deployment tests/test_env_example_is_complete.py tests/security/test_production_settings_refuse_to_start.py -m "not browser" -p no:randomly` (`TEST_DATABASE_URL` …`/ile_devops`) | **75 passed, 1 xfailed** (F-6, strict) |
| `pytest apps/core apps/documents apps/accounts tests/security tests/compliance -m "not browser" -p no:randomly` | **460 passed** (8 min 11 s) |
| `ruff check` and `ruff format --check` on the 12 changed Python files | clean |
| Line endings and trailers of the six commits | LF only; every message ends with the Co-Authored-By line |
| **End-to-end check of the documented path** (in a scratch directory, deleted afterwards): runbook step 5's Python run verbatim on a copy of `production.env.example`; the domain `sed`; the SMTP fill; step 6's `sed` extraction; step 5's placeholder `grep`; the file parsed the way systemd's `EnvironmentFile=` parses it; `manage.py check --deploy` under `config.settings.prod` with that file's variables only | The `grep` names exactly the four SMTP lines before the fill and nothing after. Step 6 extracts the 43-character password. Key 86 characters, salt 64. `DEFAULT_FROM_EMAIL` reaches Django unquoted. `check --deploy` reports exactly `security.W005` and `security.W021`, as the runbook says |
| Hard-limit scan of the branch's tree and diff for the production server's address, its name and the host names associated with it | **0 hits** |
| IP addresses the branch adds | Loopback, `0.0.0.0`, the RFC 5737 documentation ranges, and the two public resolvers in the `dig` examples |
| Real domains the branch adds | The configured contact domain, GitHub, Let's Encrypt (CAA advice), and one domain already in `base.py` as `ILE["FORBIDDEN_EMAIL_DOMAIN"]` — nothing new |
| Every repository path and test name the three documents cite | all exist |

Not run (Windows workstation, and the owner's limits): Gunicorn, nginx, systemd, certbot. I checked their configuration
against the pinned sources and the documented behaviour of the Ubuntu 24.04 packages. The full suite remains the
steward's run at the merge (NOTES, «Full suite»).

## The brief's questions, answered

1. **Are the commands correct for Ubuntu 24.04, systemd, nginx, Gunicorn, PostgreSQL and certbot?** Mostly:
   - The socket and service pair is Gunicorn's documented pattern. The pinned 26.2.0 uses the systemd socket
     (`arbiter.py:191–197`; no bind, no unlink under systemd, `:445–451`) and sends `READY=1` (`:211`).
   - `ile-manage`'s `systemd-run` flags all exist in systemd 255, and with `--wait` it returns the service's exit
     status.
   - The nginx files read as valid for 1.24 (`ssl_reject_handshake`, `listen … http2`); I did not run nginx.
   - The timers' calendar specs with `Europe/Rome` are valid.
   - `After=postgresql.service` orders the service correctly, because Ubuntu's `postgresql@.service` declares
     `Before=postgresql.service`.

   Exceptions: M1, M3, M4, m4, m6, m7.
2. **Can a private document be served without the authorisation view?** **No.**
   - nginx has no alias, root or internal location for the private directory, and could not read it if it had one:
     the directory is 0700, owned by `italylegalentry`, and nginx runs as `www-data`.
   - `prod.py` refuses at boot any overlap with `MEDIA_ROOT`, `STATIC_ROOT` or `STATICFILES_DIRS`, even through the
     escape hatch.
   - Production mounts no `django.views.static.serve`.
   - The model has no `FileField`, and the private storage's `url()` raises.
   - Nothing emits `X-Accel-Redirect` or `X-Sendfile`.
   - `request.FILES` is read only by the two documents views.
   - The four public file fields (media library, logo, Forum media, Forum PDF) accept only Pillow-verified images or
     allow-listed extensions with magic-byte checks, so no SVG or HTML is ever served inline from the site's origin.

   Two notes for the privacy record, not defects:
   - While a request lasts, nginx buffers upload bodies and large download responses in `/var/lib/nginx/{body,proxy}`
     (same disk, deleted afterwards).
   - The backup copies are where documents do leave the server unprotected (M3).
3. **Are secrets only in a root-owned file?**
   - Repository: placeholders only; the completeness test holds both templates.
   - Unit files: none.
   - Command lines and logs: none for the application, but yes for runbook step 6 and for the managed-database dump
     (M1).
   - Backup copies: yes (M3).
   - The file itself is root-owned, but group-readable by the service account, which nothing needs (m3).
4. **Does the systemd sandbox break anything?** One thing: Gunicorn 26's control socket (M4). The rest holds:
   - `ReadWritePaths` is exactly what the application writes. I searched: the two storages, plus Django's upload
     temporary files under the private `/tmp`.
   - The socket is inherited from systemd, so `ProtectSystem=strict` costs nothing there.
   - `RestrictSUIDSGID` does not stop the kernel's set-group-ID inheritance in the media tree: the filter sees the
     `mkdir` mode argument, not the inherited bit.
   - `UMask=0027` is overridden for media files by `FILE_UPLOAD_PERMISSIONS` (0644). It still leaves nginx group
     traversal through the set-group-ID directories.
5. **Is the proxy header chain consistent, and can it be spoofed?** It is consistent and cannot be spoofed:
   - nginx overwrites `Host`, `X-Forwarded-Host`, `X-Forwarded-Proto` and `X-Forwarded-For`. The last is set to
     `$remote_addr`, never appended to.
   - Only the HTTPS server proxies to the application.
   - The socket admits only `www-data` and root.
   - nginx drops headers containing underscores, so a client cannot smuggle Django's `HTTP_X_FORWARDED_PROTO` or
     Gunicorn's `SCRIPT_NAME`.
   - Gunicorn trusts unix-socket peers for forwarded headers (`http/message.py:202`).
   - allauth, with one trusted proxy, reads `xff[-1]` (`httpkit.py:198–209`); `core.privacy` reads `xff[0]`. With
     an overwritten header these are the same single value. F-1's fix is right.
6. **Are upload limits consistent end to end?** Yes:
   - 12 MiB server-wide covers the 10 MiB documents form. It is the only public form with a file field, and the
     runbook test holds that.
   - 64 MiB under `/backoffice/` covers the 60 MiB Forum media.
   - nginx buffers request bodies, so a slow upload never holds a sync worker.
   - Django spills anything over 5 MiB to the private `/tmp`.
7. **Is the HSTS advice safe when the other subdomains are unknown?** The advice is: the template sets
   `includeSubDomains=0` and `preload=0`, the subdomains are inventoried first, and preload submission is a separate
   decision. When a line is missing, the code default is the opposite (m1).
8. **Are backups real and restore-tested?** The pre-cutover snapshot is real, and C-6 restores it — good. But nothing
   repeats it after go-live (M2), and the procedure's checksum manifest and encryption are broken (M3).
9. **Is rollback safe with forward-only migrations?** The principles are right: a dump before every migration, a
   restore rather than a reverse migration, removals spread over two releases, and storage restored with its database.
   Two defects: the "additive" rule misreads Django (M7), and the code is switched under a live service (M6).
10. **Does anything cross a hard limit or name the production server?** No. Nothing names the server, and the runbook
    test refuses any non-documentation IPv4 address in `docs/deployment/`.
11. **Does `.env.example` hold only placeholders and every variable?** Yes:
    - The test holds it in both directions.
    - Development-only variables sit commented out in their own section.
    - An empty value is declared only where empty is the default, which closes F-3's trap.

    One defect: the step cross-references are wrong (m5).

## Major findings — fix before the handoff

### M1 — The database password goes through sudo's log and the process list

**Where.** `PRODUCTION_DEPLOYMENT_RUNBOOK.md:229–234` passes the password as `psql -v pw="$DB_PASSWORD"`. Step 5 had
just promised «never on a command line».

**What happens.**
- `sudo` logs every command line in full, to `/var/log/auth.log` and `journalctl _COMM=sudo`.
- While psql runs, the argument is readable in `/proc/<pid>/cmdline`.
- If the block is re-run after the role exists, PostgreSQL also logs the failing statement, password included, under
  its default `log_min_error_statement`.
- The managed-database variant does the same with a whole connection string: `PRODUCTION_CHECKLIST.md:92`,
  `pg_dump -Fc "<connection string>"`.

**Fix.**
- Feed the password on stdin: `{ printf '\\set pw %s\n' "$DB_PASSWORD"; cat <<'SQL' … SQL; } | sudo -u postgres psql
  -v ON_ERROR_STOP=1`. `printf` is a shell builtin: no argv, and nothing for sudo to log.
- Guard `CREATE ROLE` with an existence check, or use `ALTER ROLE … PASSWORD` on a re-run.
- For a managed database, use the libpq variables or a root-only `PGPASSFILE`, never the URL in argv.

### M2 — No backup is taken after go-live

**Where.** Checklist §C is a one-time snapshot before the cutover. No timer, script, retention or off-server schedule
exists for afterwards.

**What happens.**
- The cutover's MONITOR step checks «the backups» weekly (`RUNBOOK:907`), and ROLLBACK §3 and §4 assume a recent
  verified dump. Nothing creates either.
- The superseded readiness document's proposal (nightly dump, RPO 24 h with a 1 h target, 30 daily and 12 monthly
  copies aligned with the privacy retention; `DEPLOYMENT_READINESS.md` §4.2) is cited as «still valid» and is
  implemented nowhere.
- A disk or droplet loss in week two loses every identity document filed since the cutover.

**Fix.**
- Add an `italylegalentry-backup` service and timer to step 10. Run it online: `pg_dump -Fc` first, then the private
  and media archives, so every database row has its file. Encrypt, checksum, copy off the server, and prune local
  copies by the retention.
- The destination and the key holder are the owner's decisions (NOTES question 9).
- Add a go-live line to checklist §A or §B: «recurring backup running, one off-server restore drill passed».

### M3 — The §C manifest comes out empty, and the archives leave the server unencrypted

**Where.** `PRODUCTION_CHECKLIST.md:89` (manifest), `:98` (C-2), `:101` (C-5); `ROLLBACK.md:103`.

**What happens.**
- `sudo sha256sum "$B"/*-"$TS".*` — the glob is expanded by the operator's non-root shell inside
  `/var/backups/italylegalentry`, which step 2 makes root-owned and 0700. The shell cannot list the directory, the
  pattern stays literal, `sha256sum` fails, and `SHA256SUMS-$TS` is empty.
- Even when run as root, the manifest holds absolute paths. C-5's `sha256sum -c` at the off-server location fails, and
  so does ROLLBACK §4's (`ROLLBACK.md:103`) — in the middle of an incident.
- C-5 copies «the files»:
  - the database dump and the identity documents were never encrypted;
  - C-2 encrypts the config tarball with `gpg`, but its plaintext is never removed;
  - the manifest lists the plaintext tarball, not the `.gpg`.

**Fix.**
- Run the block as root inside the directory (`sudo sh -c 'cd /var/backups/italylegalentry && …'`) and checksum
  relative names.
- Encrypt all four archives: to the owner's public key, so the server never holds the decryption key, or
  `--symmetric` for every one of them.
- Checksum the encrypted files.
- Remove the plaintext once C-6 has restored from it.
- Copy only `*.gpg` and the manifest.

### M4 — Gunicorn 26 logs an error at every start and every worker fork

**Where.** The service unit's `ExecStart`, `RUNBOOK:341–344`.

**What happens.**
- Since 25.1, Gunicorn opens a control socket by default, at `$XDG_RUNTIME_DIR/gunicorn.ctl` or
  `$HOME/.gunicorn/gunicorn.ctl` (`config.py:3229–3253`).
- For this unit, `XDG_RUNTIME_DIR` is unset, `HOME` is `/nonexistent`, and the filesystem is read-only.
  `ctl/server.py:213` (`os.makedirs`) fails, and `_run_loop` logs
  `Control server error: [Errno 30] Read-only file system: '/nonexistent'`.
- `os.register_at_fork` restarts the thread after each worker fork (`ctl/server.py:37–59`), so the line comes back at
  every `--max-requests` recycle.
- It is not fatal. But it is noise in the very log the runbook tells the operator to read, and `gunicornc` cannot
  work.
- NOTES says Gunicorn's source was read for its systemd support; this new default was missed.

**Fix.**
- Add `--no-control-socket` to `ExecStart`; the operator uses `systemctl`.
- Or set `RuntimeDirectory=italylegalentry` and pass `--control-socket /run/italylegalentry/gunicorn.ctl`.
- Either way, have `tests/deployment/test_runbook_matches_the_code.py` assert it.

### M5 — The «no error» checks cannot see an error

**Where.** Cutover step 2 (`RUNBOOK:834`, «# empty»), smoke test D-20 (`CHECKLIST:156`), and step 13's `-p warning`
(`RUNBOOK:663`).

**What happens.**
- journald stores every stdout and stderr line at the unit's `SyslogLevel=` (info by default), unless the line starts
  with a `<N>` priority prefix.
- Neither Django's JSON lines (`core/logging.py`, `"level": "ERROR"`) nor Gunicorn's `[ERROR]` lines carry one.
- So `journalctl -u italylegalentry -p err` stays empty while the application answers 500s, and all three checks pass
  vacuously. Only PID 1's own start and stop failures show up.

**Fix.**
- Test the content instead, in all three places:
  `journalctl -u italylegalentry --since -1h -o cat | grep -cE '"level": "(ERROR|CRITICAL)"|\[(ERROR|CRITICAL)\]'`
  must print 0.
- Later, a code change could prefix the formatter's lines with `<3>` or `<4>`; `SyslogLevelPrefix=` is on by default.

### M6 — Updates switch the code under a live service

**Where.** §15 (`RUNBOOK:687–698`); ROLLBACK §1 does the same in reverse (`ROLLBACK.md:33–43`).

**What happens.**
- §15 checks out the new tag (step 3) and replaces packages (step 4) while Gunicorn keeps running. It migrates at
  step 6, collects static files at step 7, and restarts only at step 8.
- In between, any worker that is recycled (`--max-requests 1000` with jitter, a timeout, a crash) imports the new code
  against the old schema and the old `staticfiles.json`.
- A template naming a new bundle raises `ValueError: Missing staticfiles manifest entry` (the manifest is strict), and
  a query on a new column fails. Real visitors get 500s until step 8.
- A worker that imports a half-replaced package can fail to boot, which stops the arbiter until `Restart=` brings it
  back.

**Fix.**
- **Minimal:** hold the application for steps 3–8. Stop the socket and the service, let nginx serve a static
  maintenance page on 502/503/504, run the steps through `ile-manage`, then start again.
- **Better, later:** one directory and one virtual environment per release (`/srv/italylegalentry/releases/<tag>`).
  Migrate and collect static from it, switch a `current` symlink, restart. A rollback switches the symlink back.

### M7 — The rollback rule misreads Django's `AddField`

**Where.** `ROLLBACK.md:29` and `:53–54` treat «`AddField` with a null or a default» as safe for a code-only rollback.

**What happens.**
- Django 5.2 adds the column with a temporary database default, then drops that default unless the field has
  `db_default` (`django/db/backends/base/schema.py`, `add_field`, «Drop the default if we need to»).
- The previous code's `INSERT`s do not name the new column, so they hit a NOT NULL violation. After a «safe» rollback,
  sign-ups, uploads and forms fail with 500.
- A new unique constraint or unique index can reject the old code's writes the same way.

**Fix.**
- Code-rollback-safe means: `CreateModel`, a nullable `AddField`, an `AddField` with `db_default`, or a non-unique
  `AddIndex`.
- A NOT NULL `AddField` with only a Python default, or any unique constraint, belongs in §2 and §3, and under the
  two-release rule.

### M8 — The MFA bypass is left to the operator's habits, though nginx can close it now

**Where.** `RUNBOOK:47` (step 0's table), `RUNBOOK:302–304` (step 8); checklist A-13.

**What happens.**
- F-5 / A-13 is confirmed in the code. `/backoffice/login/` is Django's password-only form, and
  `accounts.services.needs_backoffice_mfa` (`apps/accounts/services.py:319–333`) asks whether a device is enrolled,
  not whether this session used it.
- The runbook's only measure is «sign in through `/fr/compte/login/`». That stops nobody who holds a staff password.
- Step 0's table states «TOTP mandatory in production» without the caveat.

**Fix.**
- Until the accounts fix lands, add to the 443 server:
  `location = /backoffice/login/ { return 302 /fr/compte/login/$is_args$args; }`
  - allauth runs its MFA stage on that page;
  - the admin's `?next=` is the same parameter as allauth's `next`;
  - no other password-only login view is mounted — I checked `config/urls.py` and the `accounts` app.
- Qualify step 0's line.
- Keep A-13 a go-live blocker for the code fix.

### M9 — `seed_all` at every release reverts the jurist's corrections to the legal sources

**Where.** The runbook runs `seed_all` at every update (`RUNBOOK:695`) and as a repair (`ROLLBACK.md:116`). It relies
on the seeds' contract: «safe to run on every deploy … never overwrite editorial changes» (`apps/core/seeds.py:4–5`).

**What happens.**
- `rules.legal_ruleset` breaks that contract: it calls
  `LegalSource.objects.update_or_create(key=…, defaults={title_fr, title_it, reference, authority, jurisdiction…,
  "note": SEED_NOTE})` (`apps/rules/seeds.py:469`).
- The verification fields (`consulted_on`, `consulted_by`, `url`) survive.
- But staff can edit the other fields in the back-office (`apps/rules/admin.py:61–70`). A reference, title or
  authority the jurist corrects there, and the jurist's note, silently return to the seed's values at the next
  deployment. A corrected citation regresses in production.

**Fix.**
- Rules owner: `get_or_create`, then fill blank fields only, as the other seeds do.
- Until then, the runbook says so and runs `seed_all` only at the first deployment. Later releases use `--only` for
  the seeds they add.

## Minor findings

- **m1 — HSTS defaults to on when a line is missing.**
  - `prod.py:58–59` default both directives to True, so the safe cutover state exists only in the template's two
    lines.
  - An env file built from `.env.example` (whose comments say «production default on», `:44–47`), or one with those
    lines deleted, sends `includeSubDomains` from the apex with no warning.
  - Fix: make both variables mandatory in production — no default, refused when absent. Nothing is weakened, and the
    decision is forced.
- **m2 — The release gate says «no issue» where the runbook expects two warnings.**
  - Checklist A-5 (`CHECKLIST:28`) promises `check --deploy --fail-level WARNING` → no issue «with the runbook
    values». The runbook's own template yields W005 and W021, so the command exits 1.
  - The test it cites, `test_check_deploy_reports_no_issue_under_the_runbook_configuration`
    (`test_production_checks.py:170`), actually runs with both HSTS directives on.
  - Fix: say which configuration A-5 means, and rename the test.
- **m3 — The env file is wider than needed.**
  - It is `0640 root:italylegalentry` (`RUNBOOK:167`), in a directory step 2 makes 0750.
  - systemd (PID 1) reads `EnvironmentFile=` for the service, the timers and `ile-manage`, so the service account
    never reads it.
  - Fix: `0600 root:root`, and 0700 for the directory.
- **m4 — The managed-PostgreSQL path has two gaps** (`RUNBOOK:237–239`; template `:23`).
  - On PostgreSQL 15+, a database created in the provider's panel belongs to its admin user, and the new user has no
    CREATE right on schema `public`, so `migrate` fails with «permission denied for schema public». Fix: add
    `ALTER DATABASE italylegalentry OWNER TO italylegalentry`, run as the admin user.
  - `sslmode=require` does not verify the server. Fix: `verify-full` with the cluster's CA certificate.
- **m5 — Step cross-references are swapped.** `production.env.example:1` says the env file is runbook «step 6», and
  `:22` says the database is «step 5»; `.env.example:6` also says «step 6». They are steps 5 and 6.
- **m6 — The failed database cannot be dropped as written.**
  - `ROLLBACK.md:78` renames the database to an unquoted `italylegalentry_failed_$TS`; PostgreSQL lower-cases the
    `T` and `Z` of the timestamp.
  - `:92` then runs `dropdb "italylegalentry_failed_$TS"`, which quotes the original case, so the database «does not
    exist».
  - Fix: lower-case the timestamp, or quote both commands.
- **m7 — The staging host loses its certificate.**
  - The comment says to keep `-d "$ILE_STAGING_HOST"` while that host is in use, but the commands at `RUNBOOK:755–756`
    and `:884` omit it.
  - certbot then replaces the name list while nginx and `DJANGO_ALLOWED_HOSTS` still serve that host.
  - Fix: show the two-name form.
- **m8 — C-2 misses two files** (`CHECKLIST:81–82`): `/etc/letsencrypt` (the certificates and the ACME account key —
  private keys, so encrypt them) and `/etc/nginx/sites-available/00-catch-all`.
- **m9 — Cutover steps 6→7 show a certificate error.**
  - Between the DNS switch and issuance, visitors reaching the droplet get the staging or self-signed certificate.
  - Visitors who already carry HSTS for the domain cannot click through.
  - Fix: say so; issue as soon as both resolvers return the new address, or issue with DNS-01 before the switch if
    the DNS host offers an API.
- **m10 — Stopping the timers does not stop a running job.**
  - §15 step 6 (`RUNBOOK:694`) stops only `italylegalentry-*.timer`.
  - A `send_queued_emails` run or a purge that has already started keeps running during `migrate`.
  - Fix: stop `italylegalentry-*.service` (the job units) too.

**Nits** (none is needed to ship):
- `server_tokens off` is set only in the 443 server, so the port-80 redirects still show nginx's version.
- `token_urlsafe(64)` produces 86 characters, while the placeholder says 64.
- `prod.py`'s placeholder refusal does not cover `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD`; step 5's `grep` does.
- `proxy_ignore_headers X-Accel-Redirect;` in the proxy snippet would be cheap defence in depth. Nothing emits that
  header today, and nginx could not read the private directory anyway.
- The tests use `smtp.provider.eu`, a registrable domain (never contacted); `smtp.example.net` is reserved for this.
- D-20's `awk '$6'` miscounts any line whose decoded `$uri` contains a space.

## Verified correct — leave as is

- **`prod.py`:**
  - `DATABASE_URL` and `IP_HASH_SALT` are mandatory (F-7, F-8);
  - it refuses a published or short salt, a `*` host, a mail backend that does not deliver, and an unfilled
    placeholder;
  - it refuses a private root overlapping a served directory, even through the escape hatch;
  - `CONN_HEALTH_CHECKS` is on;
  - `ALLAUTH_TRUSTED_PROXY_COUNT=1` (F-1);
  - `MEDIA_ROOT` comes from the environment.
- **`base.py`:** an empty `PRIVATE_MEDIA_ROOT` means the default directory (F-3).
- **The checks:** `core.E001`, `W001`, `W002`, `W003` and their registration. The Redis finding (F-2) is right:
  `redis` is not in `requirements/base.txt`.
- **The nginx site:**
  - only the HTTPS server proxies, and it overwrites the forwarded headers;
  - the media alias has matching trailing slashes and a `limit_except`;
  - media responses carry `nosniff` and CORP;
  - the access log masks the client address;
  - the catch-all server rejects unknown hosts with `ssl_reject_handshake`.
- **systemd and the server procedure:**
  - the socket and service units;
  - the timers, with `--apply` where the commands dry-run by default;
  - the `ile-manage` wrapper;
  - the release tag with its SHA check.
- **The cutover and release sections:**
  - the cutover order;
  - registrar transfer vs DNS cutover;
  - the three states;
  - legacy as LEGACY_REFERENCE_ONLY;
  - the static / public / private table.
- **The tests:** the four new test modules and the two extended ones; the error pages exercised through the real
  handlers; F-6 recorded as a strict xfail.

## Outside this branch — still go-live blockers

- F-5's code fix (accounts).
- F-6's template fix (`partials/seo_head.html`).
- The test suite run on Python 3.12 (A-26).
- The owner's decisions listed in NOTES:
  - the tag name and the host names;
  - the HSTS inventory;
  - the database host and the SMTP provider;
  - Redis;
  - the backup destination and who holds its key;
  - the access-log policy;
  - who owns an existing server's `default_server`;
  - CR-08 confirmed in writing.
- The blockers in `docs/PREPROD_REPORT.md` §15.

Under V5.9 §16, this branch moves nothing to RELEASE_CANDIDATE or PRODUCTION_READY.
