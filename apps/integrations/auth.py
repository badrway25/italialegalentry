"""
API key authentication (``Authorization: Bearer ile_<prefix>_<secret>``).

Keys are looked up by prefix and compared in constant time against the stored SHA-256 hash.
Every failure maps to a stable error code used by the JSON envelope.
"""

from __future__ import annotations

import hmac
import re

from integrations.models import ApiKey
from integrations.services import hash_key, touch_key

_KEY_RE = re.compile(r"^ile_(?P<prefix>[0-9a-f]{8})_[A-Za-z0-9_\-]{20,}$")


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def extract_bearer(request) -> str:
    header = request.headers.get("Authorization", "")
    scheme, _, value = header.partition(" ")
    if scheme.lower() != "bearer" or not value.strip():
        raise ApiError(401, "unauthorized", "Missing or malformed Authorization header.")
    return value.strip()


def authenticate(request) -> ApiKey:
    raw = extract_bearer(request)
    match = _KEY_RE.match(raw)
    if not match:
        raise ApiError(401, "unauthorized", "Invalid API key.")
    candidates = ApiKey.objects.filter(prefix=match.group("prefix")).select_related("system")
    digest = hash_key(raw)
    for key in candidates:
        if hmac.compare_digest(key.key_hash, digest):
            if not key.is_valid:
                raise ApiError(401, "unauthorized", "API key inactive or expired.")
            touch_key(key)
            return key
    raise ApiError(401, "unauthorized", "Invalid API key.")
