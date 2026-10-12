"""
The structured log stream must carry no personal data.

``apps/core/logging.py`` claims "No personal data is logged by design". That claim was false:
``audit.services.record`` passed ``actor_label`` (the account's e-mail address) and ``target_repr``
(for a document, the uploaded file name) into ``extra``, and the JSON formatter copies both.

The distinction that matters: the DATABASE audit row keeps readable values, because it is access
controlled and an auditor needs them. The LOG STREAM is shipped, copied, retained elsewhere and read
by people with no business seeing personal data, so it gets identifiers only.
"""

from __future__ import annotations

import json
import logging

import pytest

from audit.services import record
from core.logging import StructuredFormatter

pytestmark = pytest.mark.django_db


class Capture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


@pytest.fixture
def captured():
    handler = Capture()
    logger = logging.getLogger("ile.audit")
    logger.addHandler(handler)
    previous = logger.level
    logger.setLevel(logging.INFO)
    yield handler
    logger.removeHandler(handler)
    logger.setLevel(previous)


@pytest.fixture
def person(django_user_model):
    return django_user_model.objects.create_user(email="riservata@example.test", password="x", full_name="Nome Cognome")


def formatted(handler: Capture) -> list[dict]:
    formatter = StructuredFormatter()
    return [json.loads(formatter.format(row)) for row in handler.records]


def test_the_log_stream_carries_no_e_mail_address(captured, person):
    record(action="test.event", actor=person)
    payloads = formatted(captured)
    assert payloads, "the audit call must emit a log record"
    blob = json.dumps(payloads, ensure_ascii=False)
    assert "riservata@example.test" not in blob
    assert "Nome Cognome" not in blob


def test_the_log_stream_identifies_the_actor_by_key(captured, person):
    record(action="test.event", actor=person)
    assert formatted(captured)[0]["actor"] == f"user:{person.pk}"


def test_an_anonymous_actor_is_labelled_anonymous(captured):
    record(action="test.event")
    assert formatted(captured)[0]["actor"] == "anonymous"


def test_the_log_stream_carries_no_target_representation(captured, person):
    """``str(target)`` is a file name for a document and an e-mail for a user: identifiers only."""
    record(action="test.event", target=person)
    payload = formatted(captured)[0]
    assert payload["target"] == f"User:{person.pk}"
    assert "riservata@example.test" not in json.dumps(payload, ensure_ascii=False)


def test_the_database_row_keeps_the_readable_values(person):
    """The audit trail itself is access controlled, so it may and must stay readable."""
    event = record(action="test.event", actor=person, target=person)
    assert "riservata@example.test" in event.actor_label
    assert "riservata@example.test" in event.target_repr


# ---------------------------------------------------------------------------------------------
# The label of a non-user object
# ---------------------------------------------------------------------------------------------
def test_a_consent_of_an_anonymised_person_is_not_labelled_as_a_user(db, django_user_model):
    """
    ``anonymise_user`` rewrites the anonymised address onto the person's CONSENTS as well. The label
    helper used to match on the address alone, so an audit row about a consent was written as
    ``user:<consent id> (anonymised)`` — a wrong user id inside an audit trail, which is worse than
    no label at all because it reads as a fact.
    """
    from accounts.services import ANONYMISED_DOMAIN
    from audit.services import _label

    class FakeConsent:
        pk = 4242
        email = f"anonymised-1@{ANONYMISED_DOMAIN}"

        def __str__(self) -> str:
            return "Consent 4242"

    assert _label(FakeConsent()) == "Consent 4242"


def test_a_model_whose_email_is_not_a_string_does_not_break_the_audit_trail(db):
    """A failure in ``record()`` takes down the operation it was meant to witness."""
    from audit.services import _label

    class FakeRow:
        pk = 7
        email = object()  # e.g. a foreign key to an outbox row

        def __str__(self) -> str:
            return "Row 7"

    assert _label(FakeRow()) == "Row 7"


def test_an_anonymised_user_is_still_pseudonymised(db, django_user_model):
    from accounts.services import ANONYMISED_DOMAIN, anonymised_label_for
    from audit.services import _label

    user = django_user_model.objects.create_user(email="before@example.test", password="x")
    user.email = f"anonymised-{user.pk}@{ANONYMISED_DOMAIN}"
    user.save(update_fields=["email"])
    assert _label(user) == anonymised_label_for(user.pk)
