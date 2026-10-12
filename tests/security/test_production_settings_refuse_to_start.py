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

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

#: 64 URL-safe characters, well past the 50-character and 5-distinct-characters floor.
GOOD_KEY = "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s"

SOUND = {
    "DJANGO_SETTINGS_MODULE": "config.settings.prod",
    "DJANGO_SECRET_KEY": GOOD_KEY,
    "DJANGO_ALLOWED_HOSTS": "example.com",
    "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
    "DATABASE_URL": "postgres://ile:ile-dev-password@127.0.0.1:5439/ile",
    "BACKOFFICE_MFA_ENFORCED": "1",
    "SECURE_SSL_REDIRECT": "true",
    "SECURE_HSTS_SECONDS": "31536000",
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
    ],
    ids=["mfa-off", "no-https-redirect", "weak-hsts", "short-key", "unvaried-key"],
)
def test_production_refuses_a_weakened_configuration(overrides, expected):
    result = _load(**overrides)
    assert "LOADED" not in result.stdout, f"production started with {overrides}"
    assert "ImproperlyConfigured" in result.stderr, result.stderr[-1000:]
    assert expected in result.stderr, result.stderr[-1000:]


@pytest.mark.parametrize(
    "missing",
    ["DJANGO_SECRET_KEY", "DJANGO_ALLOWED_HOSTS", "DJANGO_CSRF_TRUSTED_ORIGINS"],
)
def test_the_three_variables_without_a_default_stop_the_boot(missing):
    """These are the three `.env.example` marks OBBLIGATORIA. This is why."""
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
