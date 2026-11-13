"""
System checks for a production configuration that loads but would still fail, quietly, in production.

``config/settings/prod.py`` refuses to start on a WEAKENED configuration. What follows is not a
weakening, and the settings module cannot see it all: a cache that breaks at its first use, rate limits
keyed on the wrong address, mail that cannot leave. ``manage.py check --deploy`` is a step of
docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md, so it says these things before the first visitor does.
Each was found by running the configuration, not by reading it (12 October 2026):

* core.E001 — a Redis cache is configured and the Redis client library is not installed. Django's
  RedisCache imports it at the first cache access, so every access fails; allauth's rate limits run on
  the cache, and signing in fails with them. requirements/base.txt does not pin the library. Checked on
  every run, not only ``--deploy``: it breaks a development server the same way.
* core.W001 — the application trusts a reverse proxy (SECURE_PROXY_SSL_HEADER) but allauth trusts none:
  behind nginx its rate limits are keyed on the proxy's address (one bucket for every visitor) or, on a
  unix socket, the request is refused for want of an address.
* core.W002 — the SMTP backend with no EMAIL_HOST: every message fails, and allauth sends the
  verification and password-reset e-mails during the request, so signing up fails with it.
* core.W003 — DEFAULT_FROM_EMAIL on a reserved placeholder domain (RFC 2606 / RFC 6761): receiving
  servers reject or bin it.
"""

from __future__ import annotations

import importlib.util
import re
from email.utils import parseaddr

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register

REDIS_CACHE_BACKEND = "django.core.cache.backends.redis.RedisCache"
SMTP_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#: Reserved for documentation and testing (RFC 2606, RFC 6761): nothing sent from them arrives as intended.
PLACEHOLDER_DOMAINS = frozenset({"example.com", "example.net", "example.org"})
PLACEHOLDER_SUFFIXES = (".invalid", ".test", ".example", ".localhost")
#: A registrable host name: labels of letters, digits and hyphens, at least one dot.
HOSTNAME = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}")


@register(Tags.caches)
def check_redis_client_library(app_configs, **kwargs):
    caches = getattr(settings, "CACHES", {}) or {}
    uses_redis = any(conf.get("BACKEND") == REDIS_CACHE_BACKEND for conf in caches.values())
    if not uses_redis or importlib.util.find_spec("redis") is not None:
        return []
    return [
        Error(
            "A Redis cache is configured (REDIS_URL) but the Redis client library is not installed: every "
            "cache access fails, and allauth's rate limits on signing in run on the cache.",
            hint="Leave REDIS_URL empty (local-memory cache), or add the client library to "
            "requirements/base.txt first — an owner's decision, since it is a new dependency.",
            id="core.E001",
        )
    ]


@register(Tags.security, deploy=True)
def check_reverse_proxy_client_address(app_configs, **kwargs):
    if not getattr(settings, "SECURE_PROXY_SSL_HEADER", None):
        return []
    trusted_count = getattr(settings, "ALLAUTH_TRUSTED_PROXY_COUNT", 0)
    if trusted_count or getattr(settings, "ALLAUTH_TRUSTED_CLIENT_IP_HEADER", None):
        return []
    return [
        Warning(
            "The application trusts a reverse proxy (SECURE_PROXY_SSL_HEADER) but allauth trusts none "
            "(ALLAUTH_TRUSTED_PROXY_COUNT is 0): its rate limits on sign-in, sign-up and password reset are "
            "keyed on the proxy's address, one bucket for every visitor — or the request is refused when "
            "the application listens on a unix socket.",
            hint="Set ALLAUTH_TRUSTED_PROXY_COUNT=1 (the production default) with nginx writing "
            "X-Forwarded-For $remote_addr.",
            id="core.W001",
        )
    ]


@register("email", deploy=True)
def check_outbound_email(app_configs, **kwargs):
    problems = []
    if getattr(settings, "EMAIL_BACKEND", "") == SMTP_BACKEND and not getattr(settings, "EMAIL_HOST", ""):
        problems.append(
            Warning(
                "EMAIL_BACKEND is SMTP but EMAIL_HOST is empty: every message fails, and the account "
                "verification and password-reset e-mails are sent during the request.",
                hint="Set EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and EMAIL_USE_TLS, then "
                "run `manage.py sendtestemail <address>`.",
                id="core.W002",
            )
        )
    raw = getattr(settings, "DEFAULT_FROM_EMAIL", "") or ""
    address = parseaddr(raw)[1]
    domain = address.rpartition("@")[2].lower().rstrip(".")
    if (
        not HOSTNAME.fullmatch(domain)
        or raw.count("<") > 1  # an unfilled «Name <noreply@<sender-domain>>» from the production template
        or domain in PLACEHOLDER_DOMAINS
        or domain.endswith(PLACEHOLDER_SUFFIXES + tuple(f".{reserved}" for reserved in PLACEHOLDER_DOMAINS))
    ):
        problems.append(
            Warning(
                f"DEFAULT_FROM_EMAIL ({address or 'empty'}) is not on a real domain: receiving servers reject "
                "or bin what it sends.",
                hint="Set DEFAULT_FROM_EMAIL to a sender address your SMTP provider is authorised to send for.",
                id="core.W003",
            )
        )
    return problems
