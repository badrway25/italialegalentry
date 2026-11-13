"""
Pluggable delivery transports for outbound events.

``LoggingTransport`` (default) NEVER opens a network connection: it logs the event and, in DEBUG,
reports success so developers see the outbox drain. Outside DEBUG it reports *skipped*, leaving the
event queued for the pull API (GET /api/v1/events/ + ack).

``HttpTransport`` is the real push implementation; it refuses to run unless
``INTEGRATIONS_ALLOW_NETWORK=True`` *and* it is selected through ``INTEGRATIONS_TRANSPORT``.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from dataclasses import dataclass

from django.conf import settings
from django.utils.module_loading import import_string

from integrations import conf

log = logging.getLogger("ile.integrations")


@dataclass(frozen=True)
class DeliveryResult:
    ok: bool
    response_code: int | None = None
    error: str = ""
    skipped: bool = False


class BaseTransport:
    name = "base"

    def deliver(self, event, endpoints) -> DeliveryResult:  # pragma: no cover - interface
        raise NotImplementedError


class LoggingTransport(BaseTransport):
    """Log-only transport: no socket is ever opened."""

    name = "logging"

    def deliver(self, event, endpoints) -> DeliveryResult:
        log.info(
            "outbound event %s type=%s attempts=%s endpoints=%d (logging transport, no network)",
            event.uuid,
            event.event_type,
            event.attempts,
            len(list(endpoints)),
        )
        if settings.DEBUG:
            return DeliveryResult(ok=True, response_code=200)
        return DeliveryResult(ok=False, skipped=True, error="no push transport configured")


class HttpTransport(BaseTransport):
    """Signed HTTP POST to every active endpoint of the event's system. Opt-in only."""

    name = "http"

    def deliver(self, event, endpoints) -> DeliveryResult:
        if not conf.allow_network():
            return DeliveryResult(ok=False, skipped=True, error="INTEGRATIONS_ALLOW_NETWORK is false")
        endpoints = [e for e in endpoints if e.is_active and e.accepts(event.event_type)]
        if not endpoints:
            return DeliveryResult(ok=False, skipped=True, error="no active endpoint")
        from integrations.services import serialize_event

        body = json.dumps(serialize_event(event), separators=(",", ":"), ensure_ascii=True).encode()
        last_code: int | None = None
        for endpoint in endpoints:
            code, error = self._post(endpoint, body)
            last_code = code
            if error:
                return DeliveryResult(ok=False, response_code=code, error=error)
        return DeliveryResult(ok=True, response_code=last_code)

    @staticmethod
    def _sign(secret: bytes, timestamp: str, nonce: str, body: bytes) -> str:
        message = b".".join([timestamp.encode(), nonce.encode(), body])
        return "sha256=" + hmac.new(secret, message, hashlib.sha256).hexdigest()

    def _post(self, endpoint, body: bytes) -> tuple[int | None, str]:
        import urllib.error
        import urllib.request

        headers = {"Content-Type": "application/json", "User-Agent": "ItalyLegalEntry-Integrations/1"}
        secret = os.environ.get(endpoint.signing_secret_env, "") if endpoint.signing_secret_env else ""
        if secret:
            timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
            headers["X-Timestamp"], headers["X-Nonce"] = timestamp, nonce
            headers["X-Signature"] = self._sign(secret.encode(), timestamp, nonce, body)
        request = urllib.request.Request(endpoint.url, data=body, headers=headers, method="POST")  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=conf.http_timeout_seconds()) as response:  # noqa: S310
                return response.status, ""
        except urllib.error.HTTPError as exc:
            return exc.code, f"HTTP {exc.code}"
        except Exception as exc:  # noqa: BLE001 - any transport failure is recorded, never raised
            return None, str(exc)[:500]


def get_transport() -> BaseTransport:
    return import_string(conf.transport_path())()
