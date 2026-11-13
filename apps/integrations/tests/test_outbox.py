"""Outbound events: idempotency, minimal payload, transports (no network), retries, signals."""

import datetime as dt
import urllib.request

import pytest
from django.apps import apps
from django.test import override_settings

from community.models import Membership, ParticipantCategory
from integrations import signals
from integrations.models import ExternalReference, OutboundEvent, OutboundEventStatus, SyncStatus, WebhookEndpoint
from integrations.services import (
    PayloadRejected,
    backoff_seconds,
    deliver_pending,
    emit,
    external_id_of,
    link_external_id,
    sanitize_payload,
)
from integrations.transports import DeliveryResult, HttpTransport, LoggingTransport, get_transport

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    def _boom(*args, **kwargs):
        raise AssertionError("network call attempted")

    monkeypatch.setattr(urllib.request, "urlopen", _boom)


def test_emit_is_idempotent_per_object(person_user):
    e1 = emit("accounts.user.created", person_user, {"created_at": person_user.created_at})
    e2 = emit("accounts.user.created", person_user, {"created_at": person_user.created_at})
    assert e1 is not None and e2 is None
    assert OutboundEvent.objects.count() == 1
    assert e1.idempotency_key == f"accounts.user.created:accounts.user:{person_user.pk}"
    assert e1.object_type == "accounts.user" and e1.object_id == str(person_user.pk)
    assert e1.status == OutboundEventStatus.QUEUED and e1.next_attempt_at is not None


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "x@example.test"},
        {"full_name": "Someone"},
        {"notes": "free text"},
        {"code": "x" * 65},
        {"code": "line\nbreak"},
        {"code": "person@example.test"},
        {"nested": {"a": 1}},
        {"list": [1, 2]},
    ],
)
def test_payload_minimisation_rejects_personal_data_and_free_text(payload):
    with pytest.raises(PayloadRejected):
        sanitize_payload(payload)


def test_payload_accepts_ids_codes_and_timestamps():
    now = dt.datetime(2026, 9, 17, 12, 0, tzinfo=dt.UTC)
    assert sanitize_payload({"category": "company", "created_at": now, "id": 3, "ok": True, "none": None}) == {
        "category": "company",
        "created_at": "2026-09-17T12:00:00+00:00",
        "id": 3,
        "ok": True,
        "none": None,
    }


def test_default_transport_is_logging_and_never_calls_network():
    transport = get_transport()
    assert isinstance(transport, LoggingTransport)
    event = emit("t.created", None, {})
    result = transport.deliver(event, [])
    assert result.skipped is True and result.ok is False  # DEBUG=False in tests → stays queued for pull API
    with override_settings(DEBUG=True):
        assert transport.deliver(event, []).ok is True


def test_deliver_pending_keeps_events_queued_without_push_transport():
    emit("t.created", None, {})
    counters = deliver_pending()
    assert counters == {"delivered": 0, "retry": 0, "failed": 0, "skipped": 1}
    event = OutboundEvent.objects.get()
    assert event.status == OutboundEventStatus.QUEUED and event.attempts == 0


@override_settings(DEBUG=True)
def test_deliver_pending_marks_delivered_in_debug():
    emit("t.created", None, {})
    assert deliver_pending()["delivered"] == 1
    event = OutboundEvent.objects.get()
    assert event.status == OutboundEventStatus.DELIVERED and event.delivered_at and event.attempts == 1


def test_http_transport_refuses_without_explicit_opt_in(system):
    WebhookEndpoint.objects.create(system=system, url="https://crm.example.test/hook", is_active=True)
    event = emit("t.created", None, {}, system=system)
    result = HttpTransport().deliver(event, list(system.endpoints.all()))
    assert result.skipped is True and "INTEGRATIONS_ALLOW_NETWORK" in result.error


class FailingTransport:
    name = "failing"

    def deliver(self, event, endpoints):
        return DeliveryResult(ok=False, response_code=503, error="boom")


@override_settings(
    INTEGRATIONS_TRANSPORT="integrations.tests.test_outbox.FailingTransport", INTEGRATIONS_MAX_ATTEMPTS=2
)
def test_retry_with_backoff_then_failed():
    emit("t.created", None, {})
    assert deliver_pending()["retry"] == 1
    event = OutboundEvent.objects.get()
    assert event.status == OutboundEventStatus.QUEUED and event.attempts == 1 and event.response_code == 503
    assert event.next_attempt_at > event.created_at
    assert backoff_seconds(1) == 60 and backoff_seconds(2) == 120 and backoff_seconds(30) == 6 * 3600
    # not due yet → untouched
    assert deliver_pending()["retry"] == 0
    OutboundEvent.objects.update(next_attempt_at=dt.datetime(2020, 1, 1, tzinfo=dt.UTC))
    assert deliver_pending()["failed"] == 1
    event.refresh_from_db()
    assert event.status == OutboundEventStatus.FAILED and event.attempts == 2 and event.last_error == "boom"


def test_deliver_outbound_events_command(capsys):
    from django.core.management import call_command

    emit("t.created", None, {})
    call_command("deliver_outbound_events")
    assert "transport=logging" in capsys.readouterr().out


def test_signals_skip_models_that_do_not_exist_yet():
    connected = signals.connect_receivers()
    for label in connected:
        apps.get_model(label)  # every connected label must exist
    watched = {label for label, _ in signals.WATCHED_MODELS}
    assert set(connected) <= watched


def test_receiver_emits_minimal_event_for_a_watched_model_save(person_user, monkeypatch):
    """Simulate enquiries.CompanyNeedsRequest with a real model carrying a `category` field."""
    monkeypatch.setitem(signals._PREFIX_BY_MODEL, Membership, "enquiries.company_needs")
    person_user.full_name = "Personal Name"
    person_user.save()
    membership = Membership.objects.create(
        user=person_user, category=ParticipantCategory.COMPANY, organisation="ACME S.r.l."
    )
    signals.on_watched_post_save(sender=Membership, instance=membership, created=True)
    event = OutboundEvent.objects.get(event_type="enquiries.company_needs.created")
    assert event.payload["category"] == "company"
    assert event.payload["status"] == "pending"
    assert "created_at" in event.payload
    dump = str(event.payload)
    assert "ACME" not in dump and "Personal Name" not in dump and "@" not in dump
    # a second save (update) emits nothing; a duplicate create is ignored
    signals.on_watched_post_save(sender=Membership, instance=membership, created=False)
    signals.on_watched_post_save(sender=Membership, instance=membership, created=True)
    assert OutboundEvent.objects.count() == 1


def test_external_reference_mapping(system, person_user):
    ref = link_external_id(system, person_user, "CRM-42")
    assert ref.sync_status == SyncStatus.SYNCED and ref.last_synced_at
    assert external_id_of(system, person_user) == "CRM-42"
    link_external_id(system, person_user, "CRM-43", synced=False)
    assert ExternalReference.objects.count() == 1
    assert external_id_of(system, person_user) == "CRM-43"
