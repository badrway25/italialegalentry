"""
Cache-based rate limiting for public forms and sensitive endpoints.

``allow(request, scope)`` returns True when the request is within the limit for the scope.
Keys are derived from the hashed client IP so raw addresses never reach the cache.
"""

from __future__ import annotations

from django.conf import settings
from django.core.cache import cache

from core.privacy import hashed_client_ip


def _key(scope: str, ident: str) -> str:
    return f"throttle:{scope}:{ident}"


def allow(request, scope: str, limit: int | None = None, window_seconds: int | None = None) -> bool:
    conf = settings.PUBLIC_FORM_THROTTLE
    limit = limit or conf["limit"]
    window = window_seconds or conf["window_seconds"]
    ident = hashed_client_ip(request) or "anonymous"
    key = _key(scope, ident)
    added = cache.add(key, 0, timeout=window)
    try:
        count = cache.incr(key)
    except ValueError:  # key expired between add and incr
        cache.add(key, 1, timeout=window)
        count = 1
    if added and count == 1:
        return True
    return count <= limit


def remaining(request, scope: str, limit: int | None = None) -> int:
    conf = settings.PUBLIC_FORM_THROTTLE
    limit = limit or conf["limit"]
    ident = hashed_client_ip(request) or "anonymous"
    count = cache.get(_key(scope, ident), 0)
    return max(0, limit - int(count))


def reset(request, scope: str) -> None:
    ident = hashed_client_ip(request) or "anonymous"
    cache.delete(_key(scope, ident))
