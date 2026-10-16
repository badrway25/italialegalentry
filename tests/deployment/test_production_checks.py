"""
The production configuration checks (apps/core/checks.py) and `manage.py check --deploy` as the runbook runs it.

Each check stands for a failure found by running a production-like configuration on 12 October 2026, not by
reading it: a Redis cache configured without its client library (every cache access fails, sign-in with it),
allauth trusting no proxy behind nginx (one rate-limit bucket for every visitor, or a 403 on a unix socket),
an SMTP backend with no host, a sender on a placeholder domain. The last two tests run the real command under
the production settings with the values the runbook tells the operator to provide — the runbook's gate
(docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md, step 7; checklist A-5) — once with the production template's
HSTS lines (exactly security.W005 and security.W021, nothing else) and once with both directives on (no issue).
"""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from django.test import override_settings

from core import checks

ROOT = Path(__file__).resolve().parents[2]

REDIS = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": "redis://127.0.0.1:1/0"}}
LOCMEM = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "probe"}}
SMTP = "django.core.mail.backends.smtp.EmailBackend"


def _ids(messages) -> list[str]:
    return [message.id for message in messages]


# ---------------------------------------------------------------------------------------------------------------
# core.E001 — a Redis cache without the client library
# ---------------------------------------------------------------------------------------------------------------
def test_a_redis_cache_without_its_client_library_is_an_error(monkeypatch):
    real_find_spec = importlib.util.find_spec
    monkeypatch.setattr(
        checks.importlib.util, "find_spec", lambda name, *a: None if name == "redis" else real_find_spec(name, *a)
    )
    with override_settings(CACHES=REDIS):
        assert _ids(checks.check_redis_client_library(None)) == ["core.E001"]
    with override_settings(CACHES=LOCMEM):
        assert checks.check_redis_client_library(None) == []


def test_a_redis_cache_with_its_client_library_passes(monkeypatch):
    monkeypatch.setattr(checks.importlib.util, "find_spec", lambda name, *a: object())
    with override_settings(CACHES=REDIS):
        assert checks.check_redis_client_library(None) == []


def test_the_pinned_requirements_do_not_carry_the_redis_client():
    """The fact core.E001 rests on. When the owner adds the library, this test is the one to update — with REDIS_URL."""
    requirements = (ROOT / "requirements" / "base.txt").read_text(encoding="utf-8").lower()
    assert not any(line.split("==")[0].strip().startswith("redis") for line in requirements.splitlines())


# ---------------------------------------------------------------------------------------------------------------
# core.W001 — a proxy the application trusts and allauth does not
# ---------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        (
            {"SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"), "ALLAUTH_TRUSTED_PROXY_COUNT": 0},
            ["core.W001"],
        ),
        ({"SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"), "ALLAUTH_TRUSTED_PROXY_COUNT": 1}, []),
        (
            {
                "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
                "ALLAUTH_TRUSTED_PROXY_COUNT": 0,
                "ALLAUTH_TRUSTED_CLIENT_IP_HEADER": "X-Real-IP",
            },
            [],
        ),
        ({"SECURE_PROXY_SSL_HEADER": None, "ALLAUTH_TRUSTED_PROXY_COUNT": 0}, []),
    ],
    ids=["proxy-trusted-by-django-only", "one-trusted-proxy", "trusted-client-ip-header", "no-proxy"],
)
def test_the_proxy_the_application_trusts_is_trusted_by_allauth_too(overrides, expected):
    with override_settings(**overrides):
        assert _ids(checks.check_reverse_proxy_client_address(None)) == expected


# ---------------------------------------------------------------------------------------------------------------
# core.W002 / core.W003 — outbound e-mail
# ---------------------------------------------------------------------------------------------------------------
REAL_SENDER = "Italy Legal Entry <noreply@agamieuromed.org>"


def test_smtp_without_a_host_is_reported():
    with override_settings(EMAIL_BACKEND=SMTP, EMAIL_HOST="", DEFAULT_FROM_EMAIL=REAL_SENDER):
        assert _ids(checks.check_outbound_email(None)) == ["core.W002"]
    with override_settings(EMAIL_BACKEND=SMTP, EMAIL_HOST="smtp.example.net", DEFAULT_FROM_EMAIL=REAL_SENDER):
        assert checks.check_outbound_email(None) == []


@pytest.mark.parametrize(
    "sender",
    [
        "Italy Legal Entry <noreply@example.invalid>",  # base.py's default
        "noreply@example.com",
        "Italy Legal Entry <noreply@mail.example.org>",
        "noreply@staging.test",
        "Italy Legal Entry <noreply@<sender-domain>>",  # the production template, unfilled
        "",
    ],
    ids=["base-default", "example-com", "example-org-subdomain", "dot-test", "template-placeholder", "empty"],
)
def test_a_sender_on_a_placeholder_domain_is_reported(sender):
    with override_settings(EMAIL_BACKEND=SMTP, EMAIL_HOST="smtp.example.net", DEFAULT_FROM_EMAIL=sender):
        assert _ids(checks.check_outbound_email(None)) == ["core.W003"]


def test_a_sender_on_a_real_domain_passes():
    with override_settings(EMAIL_BACKEND=SMTP, EMAIL_HOST="smtp.example.net", DEFAULT_FROM_EMAIL=REAL_SENDER):
        assert checks.check_outbound_email(None) == []


# ---------------------------------------------------------------------------------------------------------------
# The runbook's gate: `check --deploy` under the production settings, with the values the runbook prescribes
# ---------------------------------------------------------------------------------------------------------------
RUNBOOK_ENVIRONMENT = {
    "DJANGO_SETTINGS_MODULE": "config.settings.prod",
    "DJANGO_SECRET_KEY": "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s",
    "DJANGO_ALLOWED_HOSTS": "example.com",
    "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
    "DATABASE_URL": "postgres://ile:ile-dev-password@127.0.0.1:5439/ile",
    "IP_HASH_SALT": "Zq3vN8rT1yW6uI0oP5aS9dF2gH7jK4lX-cV_bN1mQ8wE3rT6",
    "BACKOFFICE_MFA_ENFORCED": "1",
    "EMAIL_BACKEND": SMTP,
    "EMAIL_HOST": "smtp.example.net",
    "DEFAULT_FROM_EMAIL": REAL_SENDER,
    "REDIS_URL": "",
}

#: The two HSTS lines of docs/deployment/production.env.example: both off until every host of the domain is known to
#: serve valid HTTPS. prod.py has no default for either, so every run below names one of these two configurations.
TEMPLATE_HSTS = {"SECURE_HSTS_INCLUDE_SUBDOMAINS": "0", "SECURE_HSTS_PRELOAD": "0"}
HSTS_FULLY_ON = {"SECURE_HSTS_INCLUDE_SUBDOMAINS": "1", "SECURE_HSTS_PRELOAD": "1"}

#: `?: (security.W005) You have not set …` — one id per reported issue.
ISSUE_ID = re.compile(r"\(([a-z_]+\.[CEWID]\d{3})\)")


def _check_deploy(**overrides) -> subprocess.CompletedProcess:
    env = {**os.environ, **RUNBOOK_ENVIRONMENT, **overrides}
    for name in (
        "ILE_ALLOW_INSECURE_PROD",
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        "SECURE_HSTS_PRELOAD",
        "SECURE_SSL_REDIRECT",
        # Set by the browser test modules at import time (os.environ.setdefault), so present in this process
        # whenever the suite collects them — deselected or not. A server never has it; check --deploy would
        # report async.E001 for it.
        "DJANGO_ALLOW_ASYNC_UNSAFE",
    ):
        if name not in overrides:
            env.pop(name, None)
    return subprocess.run(
        [sys.executable, str(ROOT / "manage.py"), "check", "--deploy", "--fail-level", "WARNING"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        check=False,
    )


def test_the_template_hsts_values_are_the_ones_these_tests_run():
    template = (ROOT / "docs" / "deployment" / "production.env.example").read_text(encoding="utf-8")
    for name, value in TEMPLATE_HSTS.items():
        assert re.search(rf"^{name}={value}$", template, flags=re.MULTILINE), f"production.env.example: {name}"


def test_check_deploy_reports_only_w005_and_w021_with_the_template_hsts_values():
    """The configuration the runbook installs (step 5) and checks (step 7, checklist A-5) until the domain's other hosts
    are inventoried: exactly two warnings, expected and named in the runbook — and so a non-zero exit at
    --fail-level WARNING."""
    run = _check_deploy(**TEMPLATE_HSTS)
    output = run.stdout + run.stderr
    assert run.returncode != 0, output[-2000:]
    assert set(ISSUE_ID.findall(output)) == {"security.W005", "security.W021"}, output[-2000:]


def test_check_deploy_reports_no_issue_with_hsts_fully_on():
    """Both directives on — the configuration once every host of the domain serves valid HTTPS: no issue at all."""
    run = _check_deploy(**HSTS_FULLY_ON)
    assert run.returncode == 0, (run.stdout + run.stderr)[-3000:]
    assert "System check identified no issues" in run.stdout, run.stdout[-2000:]
