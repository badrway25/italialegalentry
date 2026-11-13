"""
Log minimisation (owner directive V5.14 §5; privacy audit finding LG-1).

The application's log stream carries identifiers, not personal data (``core.logging``; enforced by
``tests/security/test_log_privacy.py``). One path still let an e-mail address through: a failed delivery logs the
SMTP library's exception text, and ``SMTPRecipientsRefused`` puts the recipient's address in it
(``notifications.services.deliver``). A third-party library or an unexpected traceback can do the same.

The filter and the two formatters below remove e-mail addresses from every line the ``console`` handler writes —
the message and the traceback alike — and keep everything else: the logger, the level, the request id, the
identifiers, the exception class and its stack. Security and operations lose nothing they need: the address of a
failed delivery stays in ``EmailOutbox.last_error``, in the access-controlled database.

Raw IP addresses are not touched here because the application never logs one (``core.privacy`` hashes them);
the reverse proxy's logs are configured in the runbook, not in Django.
"""

from __future__ import annotations

import logging
import re

from core.logging import StructuredFormatter

#: The shape of an address, the one ``tests/compliance/test_no_personal_data_in_repository.py`` uses.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
REPLACEMENT = "[e-mail]"


def redact(text: str) -> str:
    return EMAIL.sub(REPLACEMENT, text) if text and "@" in text else text


class RedactPersonalDataFilter(logging.Filter):
    """Rewrite the record's message with its e-mail addresses replaced; never drops a record."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:  # noqa: BLE001 - a malformed record is the logging module's to report, not ours
            return True
        cleaned = redact(message)
        if cleaned != message:
            record.msg = cleaned
            record.args = None
        if record.exc_text:
            record.exc_text = redact(record.exc_text)
        return True


class RedactingFormatter(logging.Formatter):
    """The plain (development) format, with the traceback redacted too."""

    def formatException(self, ei) -> str:  # noqa: N802 - logging's API
        return redact(super().formatException(ei))


class RedactingStructuredFormatter(StructuredFormatter):
    """The JSON lines of production, with the traceback redacted too."""

    def formatException(self, ei) -> str:  # noqa: N802 - logging's API
        return redact(super().formatException(ei))
