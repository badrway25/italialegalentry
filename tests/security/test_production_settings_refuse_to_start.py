"""
`config/settings/prod.py` must refuse to start on a weakened configuration.

The guard rail exists because `base.py` reads a local `.env` whatever the settings module, so a
development file copied onto a server silently weakens the deployment. It covered TLS and the
secret key. It did **not** cover the second factor: the same stray `.env` turned
`BACKOFFICE_MFA_ENFORCED` off, and that opens the case files of real people to a password alone.

It was a `check --deploy` warning, which is a thing you read if you happen to run the command. Now
it stops the process, with the same explicit escape hatch as everything else here — because there
is a legitimate window with the second factor off, the first deployment before staff have enrolled
a device, and the right way to have that window is to ask for it on the record.

Each case runs in a child process. Importing a settings module twice in one interpreter does not
re-run it, so asserting on `ImproperlyConfigured` requires a fresh one.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

#: 64 URL-safe characters, well past the 50-character and 5-distinct-characters floor.
GOOD_KEY = "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s"

#: 48 URL-safe characters: past the 32-character floor, and not one of the published placeholders.
GOOD_SALT = "Zq3vN8rT1yW6uI0oP5aS9dF2gH7jK4lX-cV_bN1mQ8wE3rT6"

SOUND = {
    "DJANGO_SETTINGS_MODULE": "config.settings.prod",
    "DJANGO_SECRET_KEY": GOOD_KEY,
    "DJANGO_ALLOWED_HOSTS": "example.com",
    "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
    "DATABASE_URL": "postgres://ile:ile-dev-password@127.0.0.1:5439/ile",
    "IP_HASH_SALT": GOOD_SALT,
    "BACKOFFICE_MFA_ENFORCED": "1",
    "SECURE_SSL_REDIRECT": "true",
    "SECURE_HSTS_SECONDS": "31536000",
    # No default since 12 October 2026: the production template's values, until the domain's hosts are inventoried.
    "SECURE_HSTS_INCLUDE_SUBDOMAINS": "0",
    "SECURE_HSTS_PRELOAD": "0",
    # Explicit, because the local `.env` that the pytest process itself has read (the test settings
    # read it) names the console backend, and the child inherits the parent's environment.
    "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
}


def _load(**overrides) -> subprocess.CompletedProcess:
    """Import the production settings in a child process and report what happened."""
    env = {**os.environ, **SOUND, **{k: str(v) for k, v in overrides.items()}}
    env.pop("ILE_ALLOW_INSECURE_PROD", None)
    for key, value in overrides.items():
        if value is None:
            env.pop(key, None)
    return subprocess.run(
        [sys.executable, "-c", "import django; django.setup(); print('LOADED')"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_a_sound_production_configuration_loads():
    """The control case. Without it, every assertion below could be passing for the wrong reason."""
    result = _load()
    assert "LOADED" in result.stdout, result.stderr[-1500:]


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"BACKOFFICE_MFA_ENFORCED": "0"}, "BACKOFFICE_MFA_ENFORCED is false"),
        ({"SECURE_SSL_REDIRECT": "false"}, "SECURE_SSL_REDIRECT is false"),
        ({"SECURE_HSTS_SECONDS": "3600"}, "SECURE_HSTS_SECONDS is 3600"),
        ({"DJANGO_SECRET_KEY": "short"}, "too short or not random enough"),
        ({"DJANGO_SECRET_KEY": "a" * 60}, "too short or not random enough"),
        ({"DJANGO_ALLOWED_HOSTS": "example.com,*"}, "DJANGO_ALLOWED_HOSTS contains '*'"),
        ({"IP_HASH_SALT": "dev-salt-change-me"}, "IP_HASH_SALT is a published placeholder"),
        ({"IP_HASH_SALT": "change-me-dev-only-not-for-production"}, "IP_HASH_SALT is a published placeholder"),
        ({"IP_HASH_SALT": "s" * 31}, "IP_HASH_SALT is a published placeholder or shorter than 32"),
        ({"EMAIL_BACKEND": "django.core.mail.backends.console.EmailBackend"}, "would be written to the logs"),
        ({"EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend"}, "would be written to the logs"),
        (
            {"IP_HASH_SALT": "<generate: python3 -c 'import secrets; print(secrets.token_urlsafe(48))'>"},
            "still holding a placeholder of the template (<...>): IP_HASH_SALT",
        ),
        (
            {"DJANGO_ALLOWED_HOSTS": "<your-domain>", "DJANGO_CSRF_TRUSTED_ORIGINS": "https://<your-domain>"},
            "still holding a placeholder of the template (<...>): DJANGO_ALLOWED_HOSTS, DJANGO_CSRF_TRUSTED_ORIGINS",
        ),
        (
            {"DATABASE_URL": "postgres://italylegalentry:<database-password>@127.0.0.1:5432/italylegalentry"},
            "still holding a placeholder of the template (<...>): DATABASE_URL",
        ),
    ],
    ids=[
        "mfa-off",
        "no-https-redirect",
        "weak-hsts",
        "short-key",
        "unvaried-key",
        "wildcard-host",
        "salt-base-default",
        "salt-example-placeholder",
        "short-salt",
        "console-mail",
        "locmem-mail",
        "unfilled-salt",
        "unfilled-hosts",
        "unfilled-database",
    ],
)
def test_production_refuses_a_weakened_configuration(overrides, expected):
    result = _load(**overrides)
    assert "LOADED" not in result.stdout, f"production started with {overrides}"
    assert "ImproperlyConfigured" in result.stderr, result.stderr[-1000:]
    assert expected in result.stderr, result.stderr[-1000:]


@pytest.mark.parametrize(
    "missing",
    [
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "DATABASE_URL",
        "IP_HASH_SALT",
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        "SECURE_HSTS_PRELOAD",
    ],
)
def test_the_variables_without_a_default_stop_the_boot(missing):
    """
    These are the variables `.env.example` marks REQUIRED IN PRODUCTION. This is why.

    DATABASE_URL joined them because base.py's fallback is the local development server, which a
    production process would have reached for at its first request instead of at boot; IP_HASH_SALT
    because base.py's fallback is published in this repository; the two HSTS directives because a
    default of "on" sent includeSubDomains from the apex of a domain nobody had inventoried whenever
    the environment file lost its line.
    """
    result = _load(**{missing: None})
    assert "LOADED" not in result.stdout, f"production started without {missing}"
    assert missing in result.stderr, result.stderr[-800:]


def test_the_escape_hatch_works_and_is_the_only_one():
    """
    A deliberate, recorded exception is allowed. An accidental one is not.

    If this ever fails, the guard rail has become something an operator cannot get past even when
    they have a real reason, and the next person will disable the whole block instead.
    """
    env = {**os.environ, **SOUND, "BACKOFFICE_MFA_ENFORCED": "0", "ILE_ALLOW_INSECURE_PROD": "1"}
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup(); print('LOADED')"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert "LOADED" in result.stdout, result.stderr[-1000:]


def _probe(code: str, **overrides) -> object:
    """Run ``code`` after ``django.setup()`` under the production settings; return its last printed line, as JSON."""
    env = {**os.environ, **SOUND, **{k: str(v) for k, v in overrides.items() if v is not None}}
    env.pop("ILE_ALLOW_INSECURE_PROD", None)
    for key, value in overrides.items():
        if value is None:
            env.pop(key, None)
    result = subprocess.run(
        [sys.executable, "-c", "import json, django; django.setup()\n" + code],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert result.returncode == 0, result.stderr[-1500:]
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_hsts_subdomains_and_preload_are_what_the_environment_decides():
    """
    No default either way: each directive is an operator's statement about the domain's other hosts, made in the
    environment (the refusal when one is missing is tested above). Off, `check --deploy` reports it
    (security.W005 / W021).
    """
    code = (
        "from django.conf import settings as s\n"
        "print(json.dumps([s.SECURE_HSTS_SECONDS, s.SECURE_HSTS_INCLUDE_SUBDOMAINS, s.SECURE_HSTS_PRELOAD]))"
    )
    assert _probe(code, SECURE_HSTS_INCLUDE_SUBDOMAINS="1", SECURE_HSTS_PRELOAD="1") == [31536000, True, True]
    assert _probe(code, SECURE_HSTS_INCLUDE_SUBDOMAINS="0", SECURE_HSTS_PRELOAD="0") == [31536000, False, False]
    assert _probe(code, SECURE_HSTS_INCLUDE_SUBDOMAINS="1", SECURE_HSTS_PRELOAD="0") == [31536000, True, False]


def test_allauth_reads_the_client_address_the_reverse_proxy_appends():
    """
    Behind nginx, allauth's default (no trusted proxy) keys every rate limit on 127.0.0.1 — one bucket
    for the whole world — or, on a unix socket, finds no address and answers 403 to every sign-in.
    Under the production settings it reads the right-most X-Forwarded-For entry, the one nginx wrote,
    so a client that sends its own header cannot choose its bucket.
    """
    code = (
        "from django.test import RequestFactory\n"
        "from allauth.account.adapter import get_adapter\n"
        "rf = RequestFactory()\n"
        "unix = rf.get('/', REMOTE_ADDR='', HTTP_X_FORWARDED_FOR='203.0.113.7')\n"
        "tcp = rf.get('/', REMOTE_ADDR='127.0.0.1', HTTP_X_FORWARDED_FOR='203.0.113.7')\n"
        "forged = rf.get('/', REMOTE_ADDR='', HTTP_X_FORWARDED_FOR='198.51.100.9, 203.0.113.7')\n"
        "print(json.dumps([get_adapter().get_client_ip(r) for r in (unix, tcp, forged)]))"
    )
    assert _probe(code) == ["203.0.113.7", "203.0.113.7", "203.0.113.7"]


def test_the_database_connection_is_checked_before_reuse_and_requests_stay_atomic():
    code = (
        "from django.conf import settings as s\n"
        "d = s.DATABASES['default']\n"
        "print(json.dumps([d['CONN_HEALTH_CHECKS'], d['ATOMIC_REQUESTS'], d['CONN_MAX_AGE'], d['HOST'], d['NAME']]))"
    )
    # DB_CONN_MAX_AGE removed: the local `.env` read by the parent process sets it to 0 for runserver.
    assert _probe(code, DB_CONN_MAX_AGE=None) == [True, True, 60, "127.0.0.1", "ile"]


def test_public_media_can_live_outside_the_checkout(tmp_path):
    code = "from django.conf import settings as s\nprint(json.dumps(str(s.MEDIA_ROOT)))"
    assert _probe(code, MEDIA_ROOT=str(tmp_path / "public-media")) == str(tmp_path / "public-media")
    assert _probe(code, MEDIA_ROOT=None) == str(ROOT / "media")


@pytest.mark.parametrize(
    ("relative", "label"),
    [("media/private", "MEDIA_ROOT"), ("staticfiles/private", "STATIC_ROOT"), ("static/private", "STATICFILES_DIRS")],
    ids=["inside-media", "inside-static-root", "inside-static-source"],
)
def test_private_documents_inside_a_served_directory_stop_the_boot_even_through_the_hatch(relative, label):
    """
    An exposure, not a weakening: no escape hatch reaches it. WhiteNoise indexes STATIC_ROOT at start-up,
    so a private file there would be public after the next restart; nginx serves MEDIA_ROOT.
    """
    env = {
        **os.environ,
        **SOUND,
        "PRIVATE_MEDIA_ROOT": str(ROOT / relative),
        "MEDIA_ROOT": str(ROOT / "media"),
        "ILE_ALLOW_INSECURE_PROD": "1",
    }
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup(); print('LOADED')"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert "LOADED" not in result.stdout, f"production started with private documents inside {label}"
    assert "PRIVATE_MEDIA_ROOT" in result.stderr and label in result.stderr, result.stderr[-1000:]
