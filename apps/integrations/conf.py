"""
Settings of the integration layer, read lazily so that tests can ``override_settings``.

Every value has a safe default; nothing here enables network traffic. The recommended entries
for ``config/settings/base.py`` are documented in docs/CRM_INTEGRATION_CONTRACT.md §11.
"""

from __future__ import annotations

from django.conf import settings

DEFAULT_TRANSPORT = "integrations.transports.LoggingTransport"


def transport_path() -> str:
    return getattr(settings, "INTEGRATIONS_TRANSPORT", DEFAULT_TRANSPORT)


def allow_network() -> bool:
    """Real HTTP delivery is opt-in; the default transport never opens a socket."""
    return bool(getattr(settings, "INTEGRATIONS_ALLOW_NETWORK", False))


def api_throttle() -> dict:
    return getattr(settings, "INTEGRATIONS_API_THROTTLE", {"limit": 120, "window_seconds": 60})


def webhook_tolerance_seconds() -> int:
    return int(getattr(settings, "INTEGRATIONS_WEBHOOK_TOLERANCE_SECONDS", 300))


def max_attempts() -> int:
    return int(getattr(settings, "INTEGRATIONS_MAX_ATTEMPTS", 8))


def max_backoff_seconds() -> int:
    return int(getattr(settings, "INTEGRATIONS_MAX_BACKOFF_SECONDS", 6 * 3600))


def http_timeout_seconds() -> int:
    return int(getattr(settings, "INTEGRATIONS_HTTP_TIMEOUT_SECONDS", 10))


def max_webhook_body_bytes() -> int:
    return int(getattr(settings, "INTEGRATIONS_MAX_WEBHOOK_BODY_BYTES", 256 * 1024))


def api_page_limit() -> int:
    return int(getattr(settings, "INTEGRATIONS_API_PAGE_LIMIT", 200))
