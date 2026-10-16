# Italy Legal Entry™ — production checklist

> Companion of [`PRODUCTION_DEPLOYMENT_RUNBOOK.md`](PRODUCTION_DEPLOYMENT_RUNBOOK.md) and [`ROLLBACK.md`](ROLLBACK.md).
> A box is ticked only with its evidence written beside it — a command's output, a test count, a file name and its
> checksum. «Should be fine» is not evidence. Written 12 October 2026; nothing in it has been run on a server.
> Updated 16 October 2026 (the DevOps lane's second pass): A-21 and D-10 (the NUL-byte 400), A-22 and D-7 (every
> static file a page loads cached by its hashed name); the same day, by its review fixes: A-21 and D-10 (what nginx
> answers itself, the security headers of the 400).

- [A. Release gate](#a-release-gate) — the owner's list (directive V5.9 §15), item by item, with how to verify it
- [B. Before the deployment](#b-before-the-deployment)
- [C. Backup before the cutover](#c-backup-before-the-cutover)
- [D. Smoke test after the cutover](#d-smoke-test-after-the-cutover)

Commands written `python …` run in a development checkout with the project's virtual environment; commands written
`sudo ile-manage …` run on the server (runbook, step 5). `TEST_DATABASE_URL` gives every test run its own database.

---

## A. Release gate

On **one commit** — the one that will be tagged — and nothing else. The project is called ready for server deployment
only when every line is ticked (see *States* in the runbook).

| # | Item | How to verify | Evidence to write down |
|---|---|---|---|
| A-1 | **Clean Git status** | `git status --porcelain` prints nothing, in the integration checkout and in the publication repository; `git log -1` is the commit to tag | the SHA |
| A-2 | **GitHub synchronised** | `git ls-remote https://github.com/badrway25/italialegalentry.git refs/heads/main "refs/tags/<tag>" "refs/tags/<tag>^{}"`: the `refs/heads/main` line and the `refs/tags/<tag>^{}` line show the SHA of A-1 — for an annotated tag the plain `refs/tags/<tag>` line is the tag object's own SHA, not the commit's; a lightweight tag has only the plain line, which is then the commit (checked on a local annotated tag, 12 October 2026). The CI run of that SHA is green on GitHub | the `ls-remote` output, the CI run's link |
| A-3 | **Full test suite** | `TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_t_release python -m pytest -m "not browser" -p no:randomly`, then the browser suite `python -m pytest -m browser` with the QA servers up | passed / failed / skipped / xfailed counts of both runs: **0 failed** |
| A-4 | **Migrations clean** | `python manage.py makemigrations --check --dry-run` → «No changes detected» (also under `config.settings.prod`); `tests/test_migration_drift.py`; `migrate` on an **empty** scratch database under the production settings, then `migrate --check` exits 0 | the three outputs |
| A-5 | **Django deploy checks** | `check --deploy --fail-level WARNING` under `config.settings.prod`, with generated placeholder values for the secrets and the rest as the production template sets it: with the template's `SECURE_HSTS_INCLUDE_SUBDOMAINS=0` / `SECURE_HSTS_PRELOAD=0`, **exactly** `security.W005` and `security.W021` and nothing else (exit 1 at that fail level — runbook step 7); with both set to `1`, no issue (exit 0). Held by `tests/deployment/test_production_checks.py::test_check_deploy_reports_only_w005_and_w021_with_the_template_hsts_values` and `::test_check_deploy_reports_no_issue_with_hsts_fully_on` | both outputs |
| A-6 | **No secrets** | `python scripts/history_secret_scan.py` over what will be published; the fixed-string scan for the known local secrets (QA password, API keys) on the snapshot tree → 0 hits; `git ls-files \| grep -E '(^\|/)\.env$'` prints nothing; both templates hold placeholders only (`tests/test_env_example_is_complete.py`) | scan reports |
| A-7 | **No personal-data artifacts** | `tests/compliance/test_no_personal_data_in_repository.py`; `tests/security/test_confidential_material.py` **with** `ILE_CONFIDENTIAL_SENTINELS` set (a skipped test is not a pass); every new image, capture, PDF or JSON of the release reviewed by name (`git diff --name-only <previous tag>..HEAD`) | test output, the reviewed list |
| A-8 | **No DEBUG production leak** | `prod.py` forces `DEBUG = False`; `tests/deployment/test_error_pages_with_debug_off.py` (no traceback, no request dump, no settings on 400/403/404/429/500); on the server: `sudo ile-manage shell -c "from django.conf import settings; print(settings.DEBUG)"` → `False`; `/_design/` and `/__design-v5/` answer 404 | outputs |
| A-9 | **Accessibility, critical checks** | the automated checks of the browser suite (A-3) and `docs/ACCESSIBILITY.md`; by hand on the release: keyboard only through sign-in, a form and the case file; visible focus; the skip link; one `h1` per page; contrast of the error and notice states. **A real screen-reader pass** (`docs/HUMAN_QA_CHECKLIST.md`) is a go-live blocker in its own right (A-23) | the pages walked, the findings |
| A-10 | **Mobile** | the phone-width browser tests (`tests/frontend/test_header_fits_the_narrowest_viewport.py`, `test_console_phone_browser_w3_a.py`); by hand on a real phone on the temporary host: home, a pathway, sign-in, «Mes pièces», the case file, the phone menu | device, pages, findings |
| A-11 | **RTL** | `tests/i18n/test_rtl_browser*.py`, `scripts/qa_rtl_check.py`; `curl -s https://<host>/ar/ \| grep -o '<html[^>]*>'` shows `dir="rtl"`; by hand: Arabic home, a form, the console | outputs |
| A-12 | **Core workflows** | `scripts/qa_person_journey.py`, `scripts/qa_company_journey.py`, `scripts/qa_journey_tail.py` on the QA server; the chains of `docs/PREPROD_REPORT.md` §10bis (visitor → account → profiling → orientation → rule engine → result → case file → checklist → documents; company → verification → need → competences → authorised actors) | the scripts' reports |
| A-13 | **Authentication** | `apps/accounts/tests`; sign-up (when G2 is open) → verification e-mail → sign-in → sign-out; password reset by e-mail; rate limits keyed on the real client behind the proxy (`tests/security/test_production_settings_refuse_to_start.py::test_allauth_reads_the_client_address_the_reverse_proxy_appends`); TOTP enrolment enforced for every role that reads others' data. **And: with an account that HAS a TOTP device, `/backoffice/login/` must not open `/backoffice/` on the password alone** (the DevOps lane's F-5, found on 12 October 2026: Django's own admin sign-in form did not ask for the second factor, and the second-factor middleware checked that a device was enrolled, not that this session used it). **Fixed by the sec-f5 lane** (`docs/design-v5/QA/v54/sec-f5/NOTES.md`): the back office's own sign-in signs no one in and sends the visitor to allauth's sign-in, whose MFA stage asks the code (`accounts/admin_site.py`); an account that holds a second factor reaches the back office, the reserved area or a private document only after presenting it in that session (`accounts.services.second_factor_due`, enforced by the middleware, by the admin site itself and on allauth's pages that manage the factor). Held by `apps/accounts/tests/test_backoffice_second_factor.py` — among its tests `test_f5_the_backoffice_sign_in_form_never_opens_the_backoffice_on_a_password_alone`, `test_through_allauth_the_code_is_asked_before_the_backoffice_opens`, `test_a_session_opened_by_another_door_is_sent_to_present_the_factor`, `test_the_pages_that_manage_the_factor_need_it_presented`, `test_the_admin_site_keeps_the_policy_without_the_middleware` — and `apps/accounts/tests/test_mfa_middleware.py`. The runbook's nginx redirect of that path (step 11) stays as a second layer — on the server, `curl -sI "https://<host>/backoffice/login/?next=/backoffice/" \| grep -i '^location'` shows `/fr/compte/login/?next=/backoffice/`; D-12 is the sign-in by hand | the `curl` line; D-12 (the TOTP code asked before the back office opens) |
| A-14 | **Permissions** | `tests/security/test_object_permissions.py`, `test_authorization_audit.py`, `test_privilege_escalation.py`; by hand with two person accounts and a company account on the temporary host: nobody reaches another's case file, documents or company (404, never 403 for what one may not see) | test counts, the manual matrix |
| A-15 | **Documents** | `apps/documents/tests` (upload, download, signed links, lifecycle), `tests/deployment/test_private_documents_are_never_served.py`; on the server: an upload lands in `/var/lib/italylegalentry/private/<id>/` with mode `0600`; another account gets 403/404; `curl -sI https://<host>/media/` does not list anything; the purge dry-runs (runbook step 10) report sane counts | outputs |
| A-16 | **Rule Engine** | `apps/rules/tests`; `sudo ile-manage rules_pending_review --strict` exits 0 (no rule in force without an approver or on an unverified source); no rule is activated in production before the jurist's review (go-live blocker A-23) | output |
| A-17 | **Case File** | `apps/cases/tests`, `apps/portal/tests`; by hand: open, read and update a case file as its person and as its assigned professional; the timeline and the checklist agree | test counts, the walk |
| A-18 | **Company** | `apps/companies/tests`, `apps/selection/tests`, `scripts/qa_company_journey.py` | outputs |
| A-19 | **Academy** | `apps/academy/tests`; the catalogue and a training plan render for the right roles only | outputs |
| A-20 | **Forum** | `apps/forum/tests`, `apps/community/tests`; the feature flags agree with the date (`phase3_public`, `forum_permanent_mode`, `virtual_forum` — back-office, phase console) | outputs, the flags' states |
| A-21 | **Error pages** | `tests/deployment/test_error_pages_with_debug_off.py` (through the real handlers), `tests/frontend/test_layout.py`, `tests/frontend/test_429_w2_b.py`. A request whose `Host` is not allowed gets the 400 page: since W3-F2 the 400 and 500 pages are drawn without the request (`core.views._self_sufficient`), and `test_error_pages_with_debug_off.py` asserts it (the DevOps lane's F-6, a strict xfail until the devops merge, closed by W3-F2's merge `9af0e1a`). nginx's catch-all server (runbook step 11) still keeps such requests away from Django. A NUL byte in the query string, the session cookie or a form field gets the 400 page too, with the security headers of every page and no ERROR line — it was a 500 with a traceback until 16 October 2026 (gate 2's N-4): `tests/deployment/test_nul_bytes.py` (`cms.middleware.NulByteMiddleware`); behind nginx a NUL in the path gets nginx's own 400 and never reaches Django; on the server, D-10 | outputs |
| A-22 | **Performance sanity check** | on the temporary host, the method of `docs/STAGING_PERFORMANCE.md`: server time of `/fr/` and `/ar/` (`curl -o /dev/null -s -w '%{time_starttransfer}\n'`, median of 5), LCP and CLS of the home and the console on a phone profile, every static file a page loads `immutable` — the ES modules its scripts import included (`tests/deployment/test_static_caching.py`, D-7) — and gzip; the shared CSS within its recorded ceilings (directive V5.8) | the figures |

Go-live blockers that are **not code** (`docs/PREPROD_REPORT.md` §15) and decisions found by the DevOps pass:

| # | Item | Whose |
|---|---|---|
| A-23 | Official Italian legal texts (the legal pages and the public forms stay closed until then); jurist review of the rules and verification of the fifteen sources; human review of the translations; a real screen-reader pass | owner, jurist, translators |
| A-24 | EU hosting confirmed in writing: region of the droplet, of the database, **of the backups**; sub-processors; processing agreement (CR-08, `docs/DEPLOYMENT_READINESS.md` §3) | owner + provider |
| A-25 | SMTP provider chosen, sender domain authorised (SPF, DKIM), outbound port open from the droplet (`sudo ile-manage sendtestemail <address>` arrives) | owner |
| A-26 | The test suite run once on Python 3.12 (Ubuntu 24.04's interpreter) — or Python 3.13 installed on the server | team / owner |
| A-27 | The release tag's name: `v2.0.0` (the version the platform already declares) or `v1.0.0` (runbook, *Release tags*) | owner |
| A-28 | **Backups running and restorable** (runbook step 10): the owner's backup key pair made, the private key and its passphrase stored offline twice; the off-server destination decided and configured; `italylegalentry-backup.timer` active and its last run «copied off the server»; **one off-server restore drill passed** (C-6) | owner |

## B. Before the deployment

- [ ] The final handoff block is in hand: repository, tag, **SHA**, test results, migration state, open issues.
- [ ] The release gate (A) is fully ticked on that SHA, or every open line is accepted by the owner in writing.
- [ ] Ubuntu 24.04 LTS droplet in an **EU region**; SSH by key; a sudo user; nothing else listening on 80/443 — or,
      on an existing server, the other sites' nginx configuration and firewall reviewed (runbook steps 1 and 11).
- [ ] SMTP credentials and the sender address ready (A-25).
- [ ] Access to the domain's DNS zone confirmed — **and no record changed yet**.
- [ ] The backups decided (runbook step 10, A-28): the off-server destination (EU location; who may read and delete
      there), the owner's backup key pair made — private key and passphrase stored offline, twice — and the retention.
- [ ] The current site's operator informed of the cutover window; its own backup confirmed by them.

## C. Backup before the cutover

**Do not claim a backup exists unless it has been verified.** A backup is verified when it has been restored
somewhere else and the restored copy has been checked. Until then it is a file.

It is the **first run of the nightly backup** (runbook step 10) — the same script, the same encrypted set — taken
with the application stopped, so that the database and the files are of one instant and the counts compare exactly.
Nothing readable leaves the server: the four archives are encrypted to the owner's public key before anything is
written, the manifest holds the checksums of the encrypted files by relative name, and the server cannot decrypt
any of it.

```bash
sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service
sudo /usr/local/sbin/ile-backup        # prints "rows: …", "written: …", then "copied off the server" (C-1…C-5)
sudo systemctl start italylegalentry.socket italylegalentry.service
sudo systemctl start $(systemctl list-unit-files 'italylegalentry-*.timer' --no-legend | cut -d' ' -f1)
TS=20261020t013000z                    # replace: the timestamp ile-backup printed
sudo sh -c 'cd /var/backups/italylegalentry && ls -l -- *-"$1".*.gpg "SHA256SUMS-$1" && sha256sum -c "SHA256SUMS-$1"' sh "$TS"
sudo find /var/lib/italylegalentry/media -type f | wc -l     # for C-4
```

A managed database: `ile-backup`'s `pg()` line reads the password from `/etc/italylegalentry/pgpass` (runbook step 6)
— never a connection string on a command line — and `pg_dump`'s major version must be at least the cluster's
(Ubuntu 24.04's is 16). The provider's own backups do not replace C-6.

| # | Item | How | Evidence |
|---|---|---|---|
| C-1 | PostgreSQL dump | `db-$TS.dump.gpg`: `pg_dump -Fc`, encrypted to the owner's key | file, size, its `SHA256SUMS` line, the «rows:» line `ile-backup` printed |
| C-2 | Application configuration | `config-$TS.tar.gz.gpg`: the environment file (the secrets), nginx's site, proxy snippet and catch-all server, `/etc/letsencrypt` (certificates and the ACME account key: private keys), the systemd units, `ile-manage`, `ile-backup` | C-6's listing |
| C-3 | Private storage | `private-$TS.tar.gz.gpg`: personal data, encrypted before it touches the disk | C-6: every document row has its file |
| C-4 | Public media | `media-$TS.tar.gz.gpg` — the back-office uploads exist only here | C-6's file count = the `find` count above |
| C-5 | Off-server copy | `ile-backup` copies the four `.gpg` files and `SHA256SUMS-$TS` through `/etc/italylegalentry/backup-offsite` (runbook step 10); until that exists, it ends with «NOT COPIED OFF THE SERVER» and those five files are copied by hand. `sha256sum -c "SHA256SUMS-$TS"` at the destination | location, `sha256sum -c` output |
| C-6 | **Restore verification, elsewhere** | below — on a machine that is not the server and holds the private key | the «rows:» line, the file check, the two listings |
| C-7 | Rollback point recorded | the running tag and SHA, the previous tag (none at the first deployment: the rollback is then DNS — `ROLLBACK.md` §5), the DNS records' current values (cutover step 5) | the three |

C-6, on a machine that is not the server, holding the private key, with `gpg` and PostgreSQL 16 or later (a local or
throwaway instance, as its superuser), in the directory the set was copied to:

```bash
TS=20261020t013000z                                    # replace: the set's timestamp
sha256sum -c "SHA256SUMS-$TS"                          # four lines: OK (macOS: shasum -a 256 -c)
gpg --decrypt --output "db-$TS.dump" "db-$TS.dump.gpg" # asks for the key's passphrase
createdb ile_restore_test
pg_restore --no-owner --no-acl --exit-on-error -d ile_restore_test "db-$TS.dump" && echo "database restored"
psql -d ile_restore_test -tAc "select 'rows: migrations=' || (select count(*) from django_migrations) || ' users=' || (select count(*) from accounts_user) || ' documents=' || (select count(*) from documents_privatedocument)"
mkdir restore && gpg --decrypt "private-$TS.tar.gz.gpg" | tar -C restore -xzf -
psql -d ile_restore_test -tAc "select sha256 || '  private/' || owner_id || '/' || stored_name from documents_privatedocument where file_removed_at is null" > documents.sha256
if [ -s documents.sha256 ]; then (cd restore && sha256sum -c --quiet ../documents.sha256) && echo "every document row has its file, byte for byte"; else echo "no document yet"; fi
gpg --decrypt "media-$TS.tar.gz.gpg" | tar -tzf - | grep -vc '/$'                                      # the public media files (C-4)
gpg --decrypt "config-$TS.tar.gz.gpg" | tar -tzf - | grep -x 'etc/italylegalentry/italylegalentry.env'  # the environment file is in it
dropdb ile_restore_test && rm -rf restore "db-$TS.dump" documents.sha256      # the restored copy holds personal data
```

The «rows:» line must equal the one `ile-backup` printed for that set (for a nightly set, taken while the site runs:
equal or lower). Exercised on 12 October 2026 with a throwaway key and a local PostgreSQL 17, line by line as above;
a document file missing from the archive and a damaged copy each made the drill fail, as they must.

Once real people's data exists, the full drill of `docs/DEPLOYMENT_READINESS.md` §4.3 replaces this check, every
quarter: restore database **and** private documents on a clean machine, start the application on them, open a case
file, download a document, time it.

## D. Smoke test after the cutover

Run on the real domain (cutover step 9), and on the temporary host before it (cutover step 3). `H` is the host
under test.

```bash
H=https://example.com     # replace
curl -fsS "$H/healthz/"                                                                  # D-1  {"status": "ok", "database": true}
curl -sI "http://${H#https://}/" | sed -n '1p;/^[Ll]ocation/p'                            # D-2  301 to https://
echo | openssl s_client -connect "${H#https://}:443" -servername "${H#https://}" 2>/dev/null | openssl x509 -noout -issuer -dates   # D-3
curl -sI "$H/fr/" | grep -iE 'strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy|cross-origin|x-request-id'   # D-4
for l in it fr en ar; do curl -s -o /dev/null -w "$l %{http_code}\n" "$H/$l/"; done      # D-5  four times 200
curl -s "$H/ar/" | grep -o '<html[^>]*>'                                                 # D-6  dir="rtl"
css=$(curl -s "$H/fr/" | grep -o '/static/css/dist/main\.[0-9a-f]*\.css' | head -n1); curl -sI "$H$css" | grep -i cache-control   # D-7  immutable
js=$(curl -s "$H/fr/" | grep -o '/static/js/dist/shell\.[0-9a-f]*\.js' | head -n1); curl -s "$H$js" | grep -oE '(from|import) ?\(?"[^"]+"' | sort -u   # D-7  every import names a hashed file (.<12 hex digits>.js)
curl -sI "$H/static/js/dist/shell.js" | grep -i cache-control                              # D-7  a plain name: max-age=60, public
curl -s -o /dev/null -w '%{http_code}\n' "$H/media/"                                     # D-8  403 or 404: no listing
curl -s "$H/sitemap.xml" | grep -m1 -o '<loc>[^<]*'; curl -s "$H/robots.txt" | tail -n 1   # D-9  the domain, https
curl -s -o /dev/null -w '%{http_code}\n' "$H/fr/no-such-page/"; curl -s "$H/fr/no-such-page/" | grep -c Traceback   # D-10 404, then 0
curl -s -o /dev/null -w '%{http_code}\n' "$H/fr/no-such-page%00/"                         # D-10 400, nginx's own: a NUL in the path never reaches Django
curl -s -o /dev/null -w '%{http_code}\n' "$H/fr/?q=%00"; curl -s "$H/fr/?q=%00" | grep -c 'class="container error-page"'   # D-10 400, then 1: the project's page, never a 500
curl -s -o /dev/null -w '%{http_code}\n' "$H/wp-json/"                                   # D-11 410 (legacy WordPress endpoint)
```

By hand, in a browser:

- [ ] D-12 Sign in as the administrator through `/fr/compte/login/`: the TOTP code is asked; the back-office loads
      with its styles; sign out.
- [ ] D-13 `sudo ile-manage sendtestemail <your address>` arrives (inbox, not spam); a password reset requested for
      the administrator arrives and its link works.
- [ ] D-14 Two minutes later the mail queue is empty: the `EmailOutbox` counts of runbook step 12 show no growing
      `queued` or `failed`.
- [ ] D-15 With a test person account: upload a document, download it, check
      `sudo ls -l /var/lib/italylegalentry/private/<account id>/` (mode `-rw-------`); a second account gets 403/404 on
      the same URL. Delete the test accounts afterwards.
- [ ] D-16 A public photograph loads (`/media/library/photos/…`), a Forum public document opens.
- [ ] D-17 Public forms and sign-up show the state the gates decide (closed until the legal texts are published).
- [ ] D-18 The flags agree with the date (phase console in the back-office); the footer's version label is the release.
- [ ] D-19 `systemctl list-timers 'italylegalentry-*'` shows the next runs (eight: seven jobs and the backup);
      `systemctl --failed` is empty.
- [ ] D-20 Since the cutover (after an update: since the window closed — the maintenance page answers 503 by design):
      the error check of runbook step 13 prints 0 —
      `sudo journalctl -u italylegalentry --since -1h -o cat --no-pager | grep -cE '"level": "(ERROR|CRITICAL)"|\[(ERROR|CRITICAL)\]'`
      (`journalctl -p err` would stay empty: journald files the service's lines at info);
      `sudo grep -cE '" 5[0-9]{2} ' /var/log/nginx/italylegalentry.access.log` is 0 (the status follows the request's
      closing quote, whatever spaces the path holds);
      `sudo journalctl -u italylegalentry --since -1h --no-pager | grep -c DisallowedHost` is 0.
