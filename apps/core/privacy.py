"""Privacy-by-design helpers: IP addresses are hashed with a server-side salt, never stored raw."""

from __future__ import annotations

import hashlib

from django.conf import settings


def client_ip(request) -> str:
    """Return the client IP. X-Forwarded-For is honoured only when USE_X_FORWARDED_HOST is set (proxy)."""
    if getattr(settings, "USE_X_FORWARDED_HOST", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def hash_ip(ip: str) -> str:
    if not ip:
        return ""
    digest = hashlib.sha256(f"{settings.IP_HASH_SALT}:{ip}".encode()).hexdigest()
    return digest[:32]


def hashed_client_ip(request) -> str:
    return hash_ip(client_ip(request))


def truncated_user_agent(request, limit: int = 160) -> str:
    return (request.META.get("HTTP_USER_AGENT", "") or "")[:limit]
