"""Community settings read lazily (safe defaults; override in config/settings if needed)."""

from __future__ import annotations

from django.conf import settings


def post_throttle() -> dict:
    return getattr(settings, "COMMUNITY_POST_THROTTLE", {"limit": 10, "window_seconds": 600})


def report_throttle() -> dict:
    return getattr(settings, "COMMUNITY_REPORT_THROTTLE", {"limit": 5, "window_seconds": 600})


def join_throttle() -> dict:
    return getattr(settings, "COMMUNITY_JOIN_THROTTLE", {"limit": 3, "window_seconds": 600})


def trusted_post_threshold() -> int:
    """Members with fewer visible posts than this are 'new': their posts queue for moderation."""
    return int(getattr(settings, "COMMUNITY_TRUSTED_POST_THRESHOLD", 3))


def max_post_length() -> int:
    return int(getattr(settings, "COMMUNITY_MAX_POST_LENGTH", 8000))
