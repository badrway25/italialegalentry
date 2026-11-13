from __future__ import annotations

import datetime as dt
import json
import logging

from core.middleware import current_request_id


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = current_request_id()
        return True


class StructuredFormatter(logging.Formatter):
    """
    One JSON object per line; safe for log shippers.

    No personal data reaches this stream by design: callers pass identifiers, not labels. The claim
    is enforced by ``tests/security/test_log_privacy.py`` rather than trusted — it was false until
    20 September 2026, when ``audit.services.record`` still passed the account's e-mail address as
    ``actor`` and, for a document, the uploaded file name as ``target``.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": dt.datetime.now(dt.UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, "request_id", "-"),
            "message": record.getMessage(),
        }
        for key in ("event", "actor", "target", "status"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)
