"""
docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md holds the configuration the owner will type on the server: the nginx
site, the systemd units, the timers. Every value in it that the code decides is held to the code here, so that a
change on one side cannot leave the other wrong:

* nginx's body limits cover the largest upload the code accepts (documents, the Forum's back-office media);
* nginx sends exactly the proxy headers the production settings trust, and OVERWRITES X-Forwarded-For — core.privacy
  reads its first entry, allauth its last (ALLAUTH_TRUSTED_PROXY_COUNT=1);
* no alias, root or internal location of nginx reaches the private documents directory; the only alias is public
  media, at the MEDIA_ROOT of the production template;
* the service may write exactly where the application writes;
* every retention purge and delivery command of the code is on a timer — with --apply where the command dry-runs by
  default — and the commands deliberately left off are named;
* production installs requirements/base.txt only; the runbook names no real server address;
* the cutover sequence is the owner's, in the owner's order.

And what the DevOps review and verification found in the procedures themselves (12 October 2026):

* no password reaches a command line — sudo logs them, /proc shows them — and step 6 cannot fail on a re-run (M1);
* a backup runs every night, encrypted to the owner's key before anything is written, and leaves the server (M2, M3);
* Gunicorn runs without its control socket, which this sandbox cannot host (M4);
* every "no error" check reads the journal's content: journald files the service's lines at info (M5);
* an update or a rollback stops the application before the code changes; nginx answers a maintenance page (M6);
* the password-only back-office sign-in form is closed at the edge until the accounts fix (M8);
* the environment file and its directory are root's alone (m3); git runs as root on root's checkout; timestamps
  stay lower-case, so a database renamed with one can be dropped by the same name (m6).
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = (ROOT / "docs" / "deployment" / "PRODUCTION_DEPLOYMENT_RUNBOOK.md").read_text(encoding="utf-8")
CHECKLIST = (ROOT / "docs" / "deployment" / "PRODUCTION_CHECKLIST.md").read_text(encoding="utf-8")
ROLLBACK = (ROOT / "docs" / "deployment" / "ROLLBACK.md").read_text(encoding="utf-8")
TEMPLATE = (ROOT / "docs" / "deployment" / "production.env.example").read_text(encoding="utf-8")
DOCUMENTS = {"runbook": RUNBOOK, "checklist": CHECKLIST, "rollback": ROLLBACK}

#: The journal's error check (runbook step 13): Django's JSON lines and Gunicorn's bracketed levels.
ERROR_COUNT = r"""grep -cE '"level": "(ERROR|CRITICAL)"|\[(ERROR|CRITICAL)\]'"""


def _bash_blocks(text: str) -> str:
    """Every ```bash block of a document, joined: the commands, not the prose that explains them."""
    return "\n".join(re.findall(r"^```bash\n(.*?)^```$", text, flags=re.MULTILINE | re.DOTALL))


def _section(text: str, heading: str) -> str:
    """From ``heading`` to the next heading of level 1 or 2 — outside code blocks, where `# ` opens a shell comment."""
    lines = text[text.index(heading) :].splitlines(keepends=True)
    kept, fenced = [lines[0]], False
    for line in lines[1:]:
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,2} ", line):
            break
        kept.append(line)
    return "".join(kept)


def _heredoc(opener: str) -> str:
    """The body of the heredoc that starts on the line holding ``opener`` and ends at the next ``EOF`` line."""
    start = RUNBOOK.index(opener)
    body = RUNBOOK.index("\n", start) + 1
    return RUNBOOK[body : RUNBOOK.index("\nEOF\n", body)]


NGINX_SITE = _heredoc("sudo tee /etc/nginx/sites-available/italylegalentry >/dev/null <<'EOF'")
NGINX_CATCH_ALL = _heredoc("sudo tee /etc/nginx/sites-available/00-catch-all >/dev/null <<'EOF'")
PROXY_SNIPPET = _heredoc("sudo tee /etc/nginx/snippets/italylegalentry-proxy.conf >/dev/null <<'EOF'")
SERVICE = _heredoc("sudo tee /etc/systemd/system/italylegalentry.service >/dev/null <<'EOF'")
JOB_SERVICE = _heredoc('sudo tee "/etc/systemd/system/italylegalentry-$name.service" >/dev/null <<EOF')
JOBS = RUNBOOK[RUNBOOK.index("done <<'JOBS'\n") + len("done <<'JOBS'\n") : RUNBOOK.index("\nJOBS\n")]
BACKUP_SCRIPT = _heredoc("sudo tee /usr/local/sbin/ile-backup >/dev/null <<'EOF'")
BACKUP_SERVICE = _heredoc("sudo tee /etc/systemd/system/italylegalentry-backup.service >/dev/null <<'EOF'")
BACKUP_TIMER = _heredoc("sudo tee /etc/systemd/system/italylegalentry-backup.timer >/dev/null <<'EOF'")
HTTPS_SERVER = NGINX_SITE[NGINX_SITE.index("listen 443") :]


def _template_value(name: str) -> str:
    match = re.search(rf"^{name}=(.*)$", TEMPLATE, flags=re.MULTILINE)
    assert match, f"{name} is not declared in production.env.example"
    return match.group(1).strip()


def _size(value: str) -> int:
    number, unit = re.fullmatch(r"(\d+)([kmg]?)", value.lower()).groups()
    return int(number) * {"": 1, "k": 1024, "m": 1024**2, "g": 1024**3}[unit]


def _location(block: str, prefix: str) -> str:
    start = block.index(f"location {prefix} {{")
    return block[start : block.index("\n    }", start)]


def test_the_body_limits_cover_what_the_code_accepts():
    from documents.services import MAX_UPLOAD_BYTES
    from forum.validators import MEDIA_MAX_BYTES, PDF_MAX_BYTES

    https_server = NGINX_SITE[NGINX_SITE.index("listen 443") :]
    server_limit = _size(re.search(r"^    client_max_body_size (\w+);", https_server, flags=re.MULTILINE).group(1))
    backoffice = _location(https_server, "/backoffice/")
    backoffice_limit = _size(re.search(r"client_max_body_size (\w+);", backoffice).group(1))
    # A multipart body is the file plus its envelope: at least 5 % on top.
    assert server_limit >= MAX_UPLOAD_BYTES * 1.05, (server_limit, MAX_UPLOAD_BYTES)
    assert backoffice_limit >= max(MEDIA_MAX_BYTES, PDF_MAX_BYTES) * 1.05, (backoffice_limit, MEDIA_MAX_BYTES)


def test_the_only_public_upload_form_is_the_documents_one():
    """If another public form accepts files, the server-wide body limit above must be re-read against it."""
    with_files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "apps").glob("*/forms.py")
        if re.search(r"forms\.(?:File|Image)Field\(", p.read_text(encoding="utf-8"))
    )
    assert with_files == ["apps/documents/forms.py"], with_files


def test_nginx_sends_the_proxy_headers_the_production_settings_trust():
    prod = (ROOT / "config" / "settings" / "prod.py").read_text(encoding="utf-8")
    assert 'SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")' in prod
    assert "USE_X_FORWARDED_HOST = True" in prod
    assert 'env.int("ALLAUTH_TRUSTED_PROXY_COUNT", default=1)' in prod
    assert _template_value("ALLAUTH_TRUSTED_PROXY_COUNT") == "1"
    for line in (
        "proxy_pass http://italylegalentry_app;",
        "proxy_set_header Host $host;",
        "proxy_set_header X-Forwarded-Host $host;",
        "proxy_set_header X-Forwarded-Proto $scheme;",
        "proxy_set_header X-Forwarded-For $remote_addr;",
        "proxy_set_header X-Request-ID $request_id;",
    ):
        assert line in PROXY_SNIPPET, f"the proxy snippet lacks: {line}"
    assert "$proxy_add_x_forwarded_for" not in RUNBOOK, "X-Forwarded-For must be overwritten, never appended"
    # Both locations that reach the application use the snippet.
    https_server = NGINX_SITE[NGINX_SITE.index("listen 443") :]
    for prefix in ("/backoffice/", "/"):
        assert "include snippets/italylegalentry-proxy.conf;" in _location(https_server, prefix), prefix


def test_no_web_server_alias_reaches_the_private_documents():
    private = _template_value("PRIVATE_MEDIA_ROOT")
    media = _template_value("MEDIA_ROOT")
    nginx = NGINX_SITE + NGINX_CATCH_ALL + PROXY_SNIPPET
    aliases = re.findall(r"^\s*alias\s+([^;]+);", nginx, flags=re.MULTILINE)
    roots = re.findall(r"^\s*root\s+([^;]+);", nginx, flags=re.MULTILINE)
    assert aliases == [media.rstrip("/") + "/"], aliases
    assert "alias " + media.rstrip("/") + "/" in _location(NGINX_SITE, "/media/")
    # The ACME challenges and the maintenance page: two static directories of their own, under /var/www.
    assert sorted(roots) == ["/var/www/italylegalentry-maintenance", "/var/www/letsencrypt"], roots
    for root in roots:
        assert not Path(root).is_relative_to(Path(private)) and not Path(root).is_relative_to(Path(media)), root
    assert private not in nginx, "nginx names the private documents directory"
    assert not re.search(r"^\s*(?:alias|root)\s+[^;]*private", RUNBOOK, flags=re.MULTILINE)
    assert not re.search(r"^\s*internal\s*;", RUNBOOK, flags=re.MULTILINE), "no internal location (X-Accel-Redirect)"
    assert not Path(private).is_relative_to(Path(media)) and not Path(media).is_relative_to(Path(private))


def test_static_files_are_left_to_whitenoise_which_tells_a_hashed_name_from_a_plain_one():
    """
    nginx serves no /static/: WhiteNoise does, and decides each file's cache — a hashed name immutable for ten years, a
    plain name WHITENOISE_MAX_AGE seconds (tests/deployment/test_static_caching.py runs it). One nginx `expires` on
    /static/ would give both names one rule, and a long one on a plain name is the stale module the DevOps lane's second
    pass removed. The runbook states both answers as the settings give them, and the gate runs the two tests.
    """
    base = (ROOT / "config" / "settings" / "base.py").read_text(encoding="utf-8")
    assert '"staticfiles": {"BACKEND": "core.storage.CompressedManifestModulesStorage"}' in base
    assert '"whitenoise.middleware.WhiteNoiseMiddleware"' in base
    max_age = int(re.search(r"^WHITENOISE_MAX_AGE = (\d+)$", base, flags=re.MULTILINE).group(1))
    assert max_age <= 300, max_age
    assert not re.search(r"location\s+(?:[~^=*]+\s*)?/static", NGINX_SITE), "nginx must leave /static/ to WhiteNoise"
    assert "max-age=315360000, public, immutable" in RUNBOOK
    assert f"max-age={max_age}, public" in RUNBOOK and f"max-age={max_age}, public" in CHECKLIST
    for test in ("tests/deployment/test_static_caching.py", "tests/deployment/test_nul_bytes.py"):
        assert test in CHECKLIST, f"the release gate does not name {test}"


def test_the_smoke_test_proves_the_nul_guard_where_nginx_lets_a_nul_through():
    """
    Behind nginx a `%00` in the path is nginx's own bare 400 and never reaches Django; a `%00` in the query string does
    (measured with Ubuntu 24.04's nginx 1.24, REVIEW_2 n1). D-10 proves the guard on the query string — the project's
    page, not only a status nginx can answer itself — and the runbook says which layer answers which.
    """
    d10 = [line for line in _bash_blocks(CHECKLIST).splitlines() if "# D-10" in line]
    assert any("?q=%00" in line and "grep -c 'class=\"container error-page\"'" in line for line in d10), d10
    assert any("%00/" in line and "nginx's own" in line for line in d10), d10
    assert "nginx answers its own bare 400" in RUNBOOK


def test_the_service_may_write_where_the_application_writes():
    paths = {_template_value("MEDIA_ROOT"), _template_value("PRIVATE_MEDIA_ROOT")}
    for unit in (SERVICE, JOB_SERVICE):
        writable = set(re.search(r"^ReadWritePaths=(.*)$", unit, flags=re.MULTILINE).group(1).split())
        assert writable == paths, writable
        assert "EnvironmentFile=/etc/italylegalentry/italylegalentry.env" in unit
        assert "ProtectSystem=strict" in unit and "PrivateTmp=yes" in unit
    assert "config.wsgi:application" in SERVICE


def _management_commands() -> dict[str, str]:
    return {
        p.stem: p.read_text(encoding="utf-8")
        for p in (ROOT / "apps").glob("*/management/commands/*.py")
        if p.stem != "__init__"
    }


def test_every_retention_and_delivery_command_is_on_a_timer():
    commands = _management_commands()
    scheduled = {}
    for line in JOBS.strip().splitlines():
        name, schedule, command = line.split("|")
        scheduled[command.split()[0]] = command
        assert command.split()[0] in commands or command.split()[0] == "clearsessions", f"{command}: no such command"
    must_run = {name for name in commands if re.search(r"purge|send_queued|refresh_requirements|scan_deadlines", name)}
    assert must_run <= set(scheduled), f"not on a timer: {sorted(must_run - set(scheduled))}"
    assert "clearsessions" in scheduled, "database sessions accumulate without clearsessions"
    for name in must_run:
        if re.search(r"add_argument\(\s*[\"']--apply[\"']", commands[name]):
            assert "--apply" in scheduled[name].split(), f"{name} dry-runs by default: its timer must pass --apply"
    for deliberately_off in ("documents_scan_pending", "deliver_outbound_events", "rules_pending_review"):
        assert deliberately_off in RUNBOOK, f"say why {deliberately_off} is not on a timer"


def test_step_5_fills_the_templates_placeholders():
    """Step 5 generates three secrets into the template by replacing its placeholders, then the domain by sed: what is
    left must be exactly the four SMTP values the operator types — the strings must match the template's, byte for
    byte (a renamed placeholder would silently stay unfilled, and prod.py would refuse to start on it)."""
    start = RUNBOOK.index("sudo python3 - /etc/italylegalentry/italylegalentry.env <<'PY'")
    generator = RUNBOOK[start : RUNBOOK.index("\nPY\n", start)]
    generated = re.findall(r'\("(<[^"]+>)", \d+\)', generator)
    assert generated == [
        "<generate a secret: 64 random bytes, URL-safe>",
        "<generate a secret: 48 random bytes, URL-safe>",
        "<database-password>",
    ], generated
    lines = [line for line in TEMPLATE.splitlines() if line and not line.startswith("#")]
    filled = "\n".join(lines)
    for placeholder in generated:
        assert filled.count(placeholder) == 1, placeholder
        filled = filled.replace(placeholder, "generated")
    filled = filled.replace("<your-domain>", "example.com")
    assert set(re.findall(r"<[^<>@]*>", filled)) == {"<smtp-host>", "<smtp-user>", "<smtp-password>", "<sender-domain>"}


def test_the_runbook_installs_production_requirements_only():
    installs = [line for line in RUNBOOK.splitlines() if "pip install" in line]
    assert installs, "the runbook installs nothing"
    for line in installs:
        if "-r " in line:
            assert "requirements/base.txt" in line and "dev.txt" not in line, line


def test_the_runbook_names_no_real_server_address():
    """Loopback, the documentation ranges (RFC 5737) and the two public resolvers the `dig` checks query: the
    repository is public, and no address of the project's own machines may appear in it."""
    allowed = ("127.", "0.0.0.0", "192.0.2.", "198.51.100.", "203.0.113.")
    public_resolvers = {"1.1.1.1", "8.8.8.8"}
    for path in sorted((ROOT / "docs" / "deployment").glob("*")):
        for address in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", path.read_text(encoding="utf-8")):
            assert address.startswith(allowed) or address in public_resolvers, f"{path.name} names {address}"


def test_the_cutover_sequence_is_the_owners():
    section = RUNBOOK[RUNBOOK.index("## DOMAIN CUTOVER SEQUENCE") : RUNBOOK.index("## LEGACY")]
    steps = [
        "NEW SERVER READY",
        "APPLICATION HEALTHY",
        "TEMPORARY/STAGING HOST VALIDATED",
        "BACKUP CONFIRMED",
        "DNS TTL PREPARED",
        "DOMAIN DNS POINTED TO DIGITALOCEAN",
        "HTTPS CERTIFICATE",
        "ALLOWED_HOSTS / CSRF verification",
        "PRODUCTION SMOKE TEST",
        "MONITOR",
    ]
    positions = [section.index(f"**{number}. {step}") for number, step in enumerate(steps, start=1)]
    assert positions == sorted(positions)


def test_the_sections_the_owner_asked_for_exist():
    for heading in (
        "## STATIC ASSETS vs PUBLIC MEDIA vs PRIVATE USER DOCUMENTS",
        "## TLS / HTTPS",
        "## DOMAIN: REGISTRAR TRANSFER vs DNS CUTOVER",
        "## DOMAIN CUTOVER SEQUENCE",
        "## LEGACY",
        "## RELEASE TAGS",
        "## States",
    ):
        assert f"\n{heading}\n" in RUNBOOK, heading
    for state in ("DEVELOPMENT_COMPLETE", "RELEASE_CANDIDATE", "PRODUCTION_READY", "LEGACY_REFERENCE_ONLY"):
        assert state in RUNBOOK, state


def test_the_health_endpoint_and_the_python_floor_are_the_codes():
    from django.urls import reverse

    assert reverse("healthz") == "/healthz/" and "/healthz/" in RUNBOOK
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    floor = re.search(r'requires-python = ">=(\d+\.\d+)"', pyproject).group(1)
    assert f"Python {floor} or later" in RUNBOOK, floor


# ---------------------------------------------------------------------------------------------------------------
# The review's findings (docs/design-v5/QA/v54/devops/REVIEW.md, VERIFY.md), held
# ---------------------------------------------------------------------------------------------------------------
def test_no_password_reaches_a_command_line():
    """M1. sudo writes every command line to its log and /proc shows it while it runs: the database password reaches
    psql on its standard input (printf is a shell builtin), and no statement of step 6 can fail on a re-run — a failing
    statement lands in PostgreSQL's log, password included. A managed database's password stays in a 0600 file."""
    step_6 = _bash_blocks(_section(RUNBOOK, "## 6. PostgreSQL"))
    assert "-v pw=" not in RUNBOOK
    assert r"""{ printf '\\set pw %s\n' "$DB_PASSWORD"; cat <<'SQL'; } | sudo -u postgres psql""" in step_6
    assert "ALTER ROLE italylegalentry WITH LOGIN PASSWORD :'pw';" in step_6
    for created in ("pg_roles WHERE rolname = 'italylegalentry'", "pg_database WHERE datname = 'italylegalentry'"):
        assert f"WHERE NOT EXISTS (SELECT FROM {created}) \\gexec" in step_6, created
    assert "PASSWORD :'pw'" not in step_6.split("ALTER ROLE", 1)[0], "CREATE ROLE must carry no password"
    assert "sudo install -o root -g root -m 0600 /dev/null /etc/italylegalentry/pgpass" in RUNBOOK
    assert "PGPASSFILE=/etc/italylegalentry/pgpass" in BACKUP_SCRIPT
    for name, text in DOCUMENTS.items():
        # A connection URL with a password in it is never an argument: the template's placeholders hold a "<", and
        # step 6's sed reads the password out of the URL with a group, "\(...\)".
        assert not re.search(r"postgres(?:ql)?://[^\s:/@]+:[^\s@<\\]+@", _bash_blocks(text)), name
        assert "<connection string>" not in text, name


def test_gunicorn_runs_without_its_control_socket():
    """M4. Gunicorn 25.1+ opens a control socket under $XDG_RUNTIME_DIR or $HOME by default; under this unit (HOME
    /nonexistent, read-only filesystem) 26.2 logged «Control server error» at start and at every worker recycle.
    The pinned source is read rather than imported: gunicorn.config imports `grp`, which Windows lacks."""
    config = Path(importlib.util.find_spec("gunicorn").origin).with_name("config.py").read_text(encoding="utf-8")
    assert 'cli = ["--no-control-socket"]' in config
    exec_start = re.search(r"^ExecStart=.*?(?=^\w)", SERVICE, flags=re.MULTILINE | re.DOTALL).group(0)
    assert "--no-control-socket" in exec_start


def test_a_backup_runs_every_night_encrypted_and_leaves_the_server():
    """M2 and M3: a timer, the database first and the files after it, everything encrypted to the owner's public key
    before it touches the disk, checksums by relative name, the configuration with the TLS keys and the catch-all
    server (m8), a copy off the server, a local retention."""
    assert "ExecStart=/usr/local/sbin/ile-backup" in BACKUP_SERVICE
    assert "ReadWritePaths=/var/backups/italylegalentry" in BACKUP_SERVICE
    assert re.search(r"^OnCalendar=\*-\*-\* \d\d:\d\d:\d\d Europe/Rome$", BACKUP_TIMER, flags=re.MULTILINE)
    assert "Persistent=true" in BACKUP_TIMER
    assert "sudo systemctl enable --now italylegalentry-backup.timer" in RUNBOOK
    assert BACKUP_SCRIPT.startswith("#!/bin/bash\n") and "set -euo pipefail" in BACKUP_SCRIPT
    assert "--recipient-file" in BACKUP_SCRIPT and "--symmetric" not in BACKUP_SCRIPT
    commands = [line for line in BACKUP_SCRIPT.splitlines() if line and not line.lstrip().startswith("#")]
    writes = [line for line in commands if "pg_dump" in line or re.search(r"-czf -", line)]
    assert len(writes) == 4, writes  # database, private, media, configuration
    for line in writes:
        assert re.search(r'\| encrypt "[a-z]+-\$TS\.[a-z.]+"$', line), f"written without encryption: {line}"
    script = "\n".join(commands)
    assert script.index("pg_dump") < script.index("private |") < script.index("media |"), "the database comes first"
    assert '(cd "$WORK" && sha256sum -- *.gpg > "SHA256SUMS-$TS")' in BACKUP_SCRIPT
    for path in ("etc/italylegalentry", "etc/letsencrypt", "etc/nginx/sites-available/00-catch-all"):
        assert path in BACKUP_SCRIPT, path
    assert '"$OFFSITE" "$BACKUPS" "$TS"' in BACKUP_SCRIPT and '-mtime +"$KEEP_LOCAL_DAYS" -delete' in BACKUP_SCRIPT


def test_the_no_error_checks_read_the_content():
    """M5. journald files the service's lines at the unit's level (info) — Django's JSON lines and Gunicorn's [ERROR]
    lines carry no priority prefix — so `journalctl -p err` stays empty while the application answers 500s."""
    commands = _bash_blocks(RUNBOOK)
    assert not re.search(r"journalctl[^\n|]*\s-p\s", commands), "a journalctl -p check cannot see an error"
    assert ERROR_COUNT in commands
    cutover_2 = RUNBOOK[RUNBOOK.index("**2. APPLICATION HEALTHY.**") : RUNBOOK.index("**3. TEMPORARY/STAGING")]
    assert ERROR_COUNT in cutover_2
    for line in commands.splitlines():
        if "journalctl" in line and "--no-pager" in line and "|" in line:
            assert line.lstrip().startswith("sudo "), f"without sudo, a non-adm account counts nothing: {line}"


def test_an_update_stops_the_application_before_the_code_changes():
    """M6 / verification 2. A worker started between the checkout and the restart would run the new code against the
    old schema and the old static manifest; the update holds the application from before the checkout until after
    collectstatic."""
    update = _section(RUNBOOK, "## 15. Updating to a new release")
    order = [
        "sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service",
        "pre-update-$1.dump",
        'checkout --detach "refs/tags/$ILE_TAG"',
        "pip install",
        "migrate --noinput",
        "collectstatic --noinput",
        "start everything again",
    ]
    positions = [update.index(marker) for marker in order]
    assert positions == sorted(positions), list(zip(order, positions))


def test_a_maintenance_page_answers_while_the_application_is_stopped():
    assert "error_page 502 503 504 =503 /maintenance.html;" in HTTPS_SERVER
    location = HTTPS_SERVER[HTTPS_SERVER.index("location = /maintenance.html {") :]
    location = location[: location.index("}")]
    assert "root /var/www/italylegalentry-maintenance;" in location
    assert "sudo tee /var/www/italylegalentry-maintenance/maintenance.html >/dev/null <<'HTML'" in RUNBOOK
    assert "install -d -o root -g root -m 0755" in RUNBOOK and "/var/www/italylegalentry-maintenance" in RUNBOOK


def test_the_password_only_backoffice_sign_in_is_closed_at_the_edge():
    """M8. /backoffice/login/ was Django's admin form, which took a password alone even from an account with a TOTP
    device (F-5, checklist A-13). The application now closes it itself (accounts.admin_site: the site's login signs no
    one in and sends the visitor to allauth's sign-in, which runs the TOTP stage — test_backoffice_second_factor.py);
    nginx's redirect of the same path stays as a second layer at the edge."""
    from django.urls import reverse
    from django.utils import translation

    with translation.override("fr"):
        allauth_login = reverse("account_login")
    assert reverse("admin:login") == "/backoffice/login/"
    location = HTTPS_SERVER[HTTPS_SERVER.index("location = /backoffice/login/ {") :]
    location = location[: location.index("}")]
    assert f"return 302 {allauth_login}$is_args$args;" in location, location
    assert "TOTP enrolment enforced" in RUNBOOK and "TOTP mandatory in production" not in RUNBOOK


def test_the_environment_file_is_root_only():
    """m3. systemd reads EnvironmentFile= as root for the service, the timers and ile-manage."""
    assert "sudo install -d -o root -g root -m 0700 /etc/italylegalentry" in RUNBOOK
    assert re.search(
        r"sudo install -o root -g root -m 0600 \S+/production\.env\.example /etc/italylegalentry/italylegalentry\.env",
        RUNBOOK,
    )
    assert "0640" not in RUNBOOK and "0750 /etc/italylegalentry" not in RUNBOOK
    assert "owner root, group root, mode 0600" in TEMPLATE


def test_the_backup_before_the_cutover_is_the_nightly_backup_and_leaves_nothing_in_clear():
    """M3. The former section C globbed a root-only directory from the operator's shell (an empty manifest), wrote
    absolute paths into it (`sha256sum -c` failed anywhere else), and copied the database dump and the identity
    documents off the server unencrypted. Now it is a run of ile-backup, checked inside the directory, restored
    elsewhere (C-6); and the go-live gate asks for a running backup and one drill (A-28)."""
    section_c = _section(CHECKLIST, "## C. Backup before the cutover")
    commands = _bash_blocks(section_c)
    assert "sudo /usr/local/sbin/ile-backup" in commands
    assert (
        """sudo sh -c 'cd /var/backups/italylegalentry && ls -l -- *-"$1".*.gpg "SHA256SUMS-$1" && sha256sum -c"""
        in commands
    )
    assert '"$B"/' not in CHECKLIST, "a glob expanded by the operator's shell in a root-only directory"
    assert not re.search(r"tar -c\S*f \S+\.tar\.gz\b", commands), "an archive written in clear"
    for archive in ("db-$TS.dump.gpg", "private-$TS.tar.gz.gpg", "media-$TS.tar.gz.gpg", "config-$TS.tar.gz.gpg"):
        assert archive in section_c, archive
    assert "pg_restore --no-owner --no-acl --exit-on-error" in commands
    assert "sha256sum -c --quiet ../documents.sha256" in commands, "the drill checks every document row's file"
    assert re.search(
        r"^\| A-28 \| \*\*Backups running and restorable\*\*.*restore drill passed", CHECKLIST, re.MULTILINE
    )


def test_the_checklist_error_checks_read_the_content():
    """M5 in the smoke test (D-20), and the 5xx count anchored on the request's closing quote."""
    assert ERROR_COUNT in CHECKLIST
    assert "-p err` is empty" not in CHECKLIST
    assert """sudo grep -cE '" 5[0-9]{2} ' /var/log/nginx/italylegalentry.access.log""" in CHECKLIST


def test_a_code_rollback_stops_the_application_and_knows_which_migrations_allow_it():
    """M6 and M7 in ROLLBACK.md: the code switch happens with the application stopped, and «code-rollback-safe» is
    what Django's schema editor makes it — a NOT NULL AddField with only a Python default is not (the temporary
    database default is dropped), nor is a unique constraint."""
    section_1 = _section(ROLLBACK, "## 1. Application rollback to the previous tag")
    order = [
        "sudo systemctl stop 'italylegalentry-*.timer' 'italylegalentry-*.service' italylegalentry.socket italylegalentry.service",
        'checkout --detach "refs/tags/$PREVIOUS_TAG"',
        "pip install",
        "collectstatic --noinput",
        "sudo systemctl start italylegalentry.socket italylegalentry.service",
    ]
    positions = [section_1.index(marker) for marker in order]
    assert positions == sorted(positions), list(zip(order, positions))
    assert "systemctl restart italylegalentry.service" not in section_1
    for text in (section_1, _section(ROLLBACK, "## 2. Database: forward-only")):
        assert "db_default" in text and "NOT NULL" in text and "unique" in text
    assert "AddField` with a null or a default" not in ROLLBACK
    section_3 = _section(ROLLBACK, "## 3. Restore the database from the verified dump")
    assert "**only** the checkout, the SHA test, the two `pip` lines and `collectstatic`" in section_3


def test_git_runs_as_root_and_timestamps_stay_lower_case():
    """Verification 6: the checkout belongs to root, and git refuses another user's repository («dubious ownership»).
    m6: PostgreSQL folds an unquoted database name to lower case; `dropdb "…_$TS"` quotes it — so the timestamp of the
    rename is lower case, and the same name drops it."""
    for name, text in DOCUMENTS.items():
        for match in re.finditer(r"(\S+) git -C /srv/italylegalentry/app", text):
            assert re.search(r"(?:^|[(`\"])sudo$", match.group(1)), f"{name}: {match.group(0)}"
        assert "%Y%m%dT%H%MZ" not in text, name
    assert "TS=$(date -u +%Y%m%dt%H%Mz)" in ROLLBACK
    assert "RENAME TO italylegalentry_failed_$TS;" in ROLLBACK and 'dropdb "italylegalentry_failed_$TS"' in ROLLBACK


def test_the_release_gate_compares_the_tags_commit():
    """Verification 8: for an annotated tag, `refs/tags/<tag>` is the tag object's SHA; `^{}` is the commit."""
    assert '"refs/tags/<tag>^{}"' in CHECKLIST
