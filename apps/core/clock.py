"""
Project clock.

All date gates (Phase 3, Forum transitions, banner expiry) call ``core.clock.now()`` instead of
``timezone.now()`` directly, so that a developer can preview a future state locally by setting
``ILE_REFERENCE_DATE=2026-10-03`` (only honoured when DEBUG is true) and tests can freeze time.
"""

from __future__ import annotations

import datetime as dt

from django.conf import settings
from django.utils import timezone


def now() -> dt.datetime:
    override = settings.ILE.get("REFERENCE_DATE_OVERRIDE")
    if override and settings.DEBUG:
        try:
            date = dt.date.fromisoformat(override)
        except ValueError:
            return timezone.now()
        return dt.datetime.combine(date, dt.time(12, 0), tzinfo=settings.ROME)
    return timezone.now()


def today() -> dt.date:
    return timezone.localtime(now(), settings.ROME).date()
