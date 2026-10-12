"""
Inbound webhook verification: HMAC-SHA256 over ``timestamp.nonce.body`` with the per-system secret.

* the secret lives ONLY in the environment variable named by ``ExternalSystem.inbound_secret_env``;
  the database stores its SHA-256 fingerprint to detect a misconfigured environment;
* ``X-Timestamp`` must be within ±tolerance of the server clock;
* ``X-Nonce`` must be unique per system (partial unique index on valid receptions) → replay ⇒ 401.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import time
from dataclasses import dataclass

from integrations import conf
from integrations.models import ExternalSystem

_NONCE_RE = re.compile(r"^[A-Za-z0-9_\-]{8,64}$")


@dataclass(frozen=True)
class Verification:
    ok: bool
    code: str = ""
    system: ExternalSystem | None = None
    timestamp: str = ""
    nonce: str = ""


def compute_signature(secret: bytes, timestamp: str, nonce: str, body: bytes) -> str:
    message = b".".join([timestamp.encode(), nonce.encode(), body])
    return "sha256=" + hmac.new(secret, message, hashlib.sha256).hexdigest()


def secret_for(system: ExternalSystem) -> bytes | None:
    if not system.inbound_secret_env:
        return None
    raw = os.environ.get(system.inbound_secret_env, "")
    if not raw:
        return None
    if system.inbound_secret_hash and hashlib.sha256(raw.encode()).hexdigest() != system.inbound_secret_hash:
        return None  # environment does not match the registered fingerprint
    return raw.encode()


def verify(system_key: str, headers, body: bytes, *, now: float | None = None) -> Verification:
    system = ExternalSystem.objects.filter(key=system_key, is_active=True).first()
    if system is None:
        return Verification(False, "unknown_system")
    timestamp = (headers.get("X-Timestamp") or "").strip()
    nonce = (headers.get("X-Nonce") or "").strip()
    signature = (headers.get("X-Signature") or "").strip()
    if not timestamp.isdigit() or not _NONCE_RE.match(nonce) or not signature.startswith("sha256="):
        return Verification(False, "malformed_headers", system, timestamp, nonce)
    current = now if now is not None else time.time()
    if abs(current - int(timestamp)) > conf.webhook_tolerance_seconds():
        return Verification(False, "timestamp_out_of_range", system, timestamp, nonce)
    secret = secret_for(system)
    if secret is None:
        return Verification(False, "secret_not_configured", system, timestamp, nonce)
    expected = compute_signature(secret, timestamp, nonce, body)
    if not hmac.compare_digest(expected, signature):
        return Verification(False, "invalid_signature", system, timestamp, nonce)
    return Verification(True, "", system, timestamp, nonce)


def minimal_inbound_payload(payload) -> dict:
    """Keep only identifiers from an inbound payload (never store free text or personal data)."""
    if not isinstance(payload, dict):
        return {}
    keep = {}
    for key in ("event", "event_type", "id", "external_id", "object_type", "object_id", "status"):
        value = payload.get(key)
        if isinstance(value, str | int | bool) and (not isinstance(value, str) or len(value) <= 120):
            keep[key] = value
    return keep
