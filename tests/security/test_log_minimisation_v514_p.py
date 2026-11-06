"""
V5.14 §5 — the log stream carries no e-mail address, while every security and operations signal stays.

Finding LG-1 of the privacy audit: ``notifications.services.deliver`` logs the SMTP library's exception text, and
``SMTPRecipientsRefused`` puts the recipient's address in it. ``config/log_filters.py`` redacts addresses from the
message and the traceback on the ``console`` handler; the logger, level, request id, identifiers, exception class
and stack remain.
"""

from __future__ import annotations

import io
import json
import logging
import smtplib
import sys

import pytest
from django.conf import settings

from config.log_filters import (
    RedactingFormatter,
    RedactingStructuredFormatter,
    RedactPersonalDataFilter,
    redact,
)

ADDRESS = "persona.riservata@example.test"


def _record(msg, *args, exc_info=None, name="ile.notifications"):
    return logging.LogRecord(name, logging.WARNING, __file__, 1, msg, args or None, exc_info)


def test_redact_replaces_addresses_and_nothing_else():
    assert (
        redact(f"refused: {{'{ADDRESS}': (550, b'no')}} outbox 42") == "refused: {'[e-mail]': (550, b'no')} outbox 42"
    )
    assert redact("GET /fr/compte/ 404 from 127.0.0.1") == "GET /fr/compte/ 404 from 127.0.0.1"
    assert redact("") == ""


def test_the_filter_redacts_the_formatted_message_and_keeps_the_record():
    record = _record(
        "email delivery failed for outbox %s: %s", 42, smtplib.SMTPRecipientsRefused({ADDRESS: (550, b"no")})
    )
    assert RedactPersonalDataFilter().filter(record) is True
    message = record.getMessage()
    assert ADDRESS not in message and "outbox 42" in message and "[e-mail]" in message


def test_the_formatters_redact_the_traceback_but_keep_the_exception_class():
    try:
        raise smtplib.SMTPRecipientsRefused({ADDRESS: (550, b"no")})
    except smtplib.SMTPRecipientsRefused:
        record = _record("delivery failed", exc_info=sys.exc_info())
    RedactPersonalDataFilter().filter(record)
    payload = json.loads(RedactingStructuredFormatter().format(record))
    assert ADDRESS not in json.dumps(payload) and "SMTPRecipientsRefused" in payload["exception"]
    record.exc_text = None
    plain = RedactingFormatter("%(levelname)s %(name)s %(message)s").format(record)
    assert ADDRESS not in plain and "SMTPRecipientsRefused" in plain


def test_the_settings_put_the_filter_and_the_redacting_formatters_on_the_console_handler():
    logging_conf = settings.LOGGING
    assert "redact_personal_data" in logging_conf["handlers"]["console"]["filters"]
    assert "request_id" in logging_conf["handlers"]["console"]["filters"], "security correlation is kept"
    assert logging_conf["formatters"]["structured"]["()"] == "config.log_filters.RedactingStructuredFormatter"
    assert logging_conf["formatters"]["plain"]["class"] == "config.log_filters.RedactingFormatter"
    assert logging_conf["loggers"]["django.security"]["level"] == "WARNING"
    assert logging_conf["loggers"]["ile.security"]["level"] == "INFO"


@pytest.mark.django_db
def test_a_refused_recipient_never_reaches_the_log_stream(monkeypatch):
    from notifications.models import EmailOutbox, OutboxStatus
    from notifications.services import deliver

    handler = next(
        (h for h in logging.getLogger().handlers if any(isinstance(f, RedactPersonalDataFilter) for f in h.filters)),
        None,
    )
    assert handler is not None, "the configured console handler carries the redaction filter"
    stream = io.StringIO()
    previous = handler.setStream(stream)

    def refuse(self, fail_silently=False):
        raise smtplib.SMTPRecipientsRefused({ADDRESS: (550, b"5.1.1 user unknown")})

    monkeypatch.setattr("django.core.mail.EmailMultiAlternatives.send", refuse)
    item = EmailOutbox.objects.create(to_email=ADDRESS, subject="s", body_text="b")
    try:
        assert deliver(item) is False
    finally:
        handler.setStream(previous)
    written = stream.getvalue()
    assert f"outbox {item.pk}" in written, "the operations signal stays"
    assert ADDRESS not in written
    item.refresh_from_db()
    assert item.status == OutboxStatus.FAILED and ADDRESS in item.last_error, "the access-controlled copy stays"
