"""
Feature flags / publication gates.

Resolution order: database row (FeatureFlag) → settings.FEATURE_FLAG_DEFAULTS → False.
Rows are cached briefly to keep templates cheap. ``is_enabled`` is the only public API.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache
from django.db.utils import DatabaseError, ProgrammingError

from core import clock

CACHE_KEY = "core.flags.snapshot"
CACHE_TTL = 30


@dataclass(frozen=True)
class FlagState:
    key: str
    enabled: bool
    enabled_from: dt.datetime | None
    enabled_until: dt.datetime | None
    source: str  # "db" | "default" | "missing"

    def active(self, at: dt.datetime | None = None) -> bool:
        if not self.enabled:
            return False
        at = at or clock.now()
        if self.enabled_from and at < self.enabled_from:
            return False
        return not (self.enabled_until and at >= self.enabled_until)


def _snapshot() -> dict[str, FlagState]:
    snap = cache.get(CACHE_KEY)
    if snap is not None:
        return snap
    from core.models import FeatureFlag

    snap = {}
    try:
        for row in FeatureFlag.objects.all():
            snap[row.key] = FlagState(row.key, row.enabled, row.enabled_from, row.enabled_until, "db")
    except (DatabaseError, ProgrammingError):  # pragma: no cover - before migrations
        pass
    cache.set(CACHE_KEY, snap, CACHE_TTL)
    return snap


def invalidate() -> None:
    cache.delete(CACHE_KEY)


def get_state(key: str) -> FlagState:
    state = _snapshot().get(key)
    if state:
        return state
    default = settings.FEATURE_FLAG_DEFAULTS.get(key)
    if default:
        return FlagState(
            key,
            bool(default.get("enabled", False)),
            default.get("enabled_from"),
            default.get("enabled_until"),
            "default",
        )
    return FlagState(key, False, None, None, "missing")


def is_enabled(key: str, at: dt.datetime | None = None) -> bool:
    return get_state(key).active(at)


def all_states() -> dict[str, FlagState]:
    keys = set(settings.FEATURE_FLAG_DEFAULTS) | set(_snapshot())
    return {k: get_state(k) for k in sorted(keys)}
