"""
Service layer of the integration boundary. Views, signals, commands and admin call ONLY these.

Data-minimisation rule (contract §6): an outbound payload carries identifiers, timestamps and
closed-vocabulary codes (category, kind, status). Free text and personal data are rejected at
emission time; the CRM fetches details through a future authenticated endpoint.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import logging
import secrets
import uuid as uuid_lib
from collections.abc import Iterable

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.db.models import Q, QuerySet

from core import clock
from integrations import conf
from integrations.models import (
    ApiKey,
    ExternalReference,
    ExternalSystem,
    OutboundEvent,
    OutboundEventStatus,
    SyncStatus,
    WebhookEndpoint,
)
from integrations.transports import DeliveryResult, get_transport

log = logging.getLogger("ile.integrations")

# Keys that must never travel in an outbound payload (personal data / free text).
FORBIDDEN_PAYLOAD_KEYS = frozenset(
    {
        "email",
        "e_mail",
        "phone",
        "telephone",
        "name",
        "first_name",
        "last_name",
        "full_name",
        "contact",
        "contact_name",
        "referent",
        "address",
        "body",
        "notes",
        "note",
        "message",
        "description",
        "text",
        "ip",
        "ip_hash",
        "user_agent",
    }
)
MAX_PAYLOAD_STRING_LENGTH = 64
MAX_PAYLOAD_KEYS = 20


class PayloadRejected(ValueError):
    """Raised when a payload violates the data-minimisation rule."""


# --------------------------------------------------------------------------------------------
# Outbound events
# --------------------------------------------------------------------------------------------
def _scalar(value):
    if isinstance(value, dt.datetime | dt.date):
        return value.isoformat()
    if isinstance(value, uuid_lib.UUID):
        return str(value)
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        if len(value) > MAX_PAYLOAD_STRING_LENGTH or "\n" in value or "@" in value:
            raise PayloadRejected("string values must be short codes without newlines or e-mail addresses")
        return value
    raise PayloadRejected(f"unsupported payload value type {type(value).__name__}")


def sanitize_payload(payload: dict | None) -> dict:
    """Enforce the minimal-payload rule; raise PayloadRejected on personal data or free text."""
    if not payload:
        return {}
    if not isinstance(payload, dict):
        raise PayloadRejected("payload must be a mapping")
    if len(payload) > MAX_PAYLOAD_KEYS:
        raise PayloadRejected("too many payload keys")
    cleaned = {}
    for key, value in payload.items():
        if not isinstance(key, str) or not key:
            raise PayloadRejected("payload keys must be non-empty strings")
        if key.lower() in FORBIDDEN_PAYLOAD_KEYS:
            raise PayloadRejected(f"payload key {key!r} is not allowed (personal data / free text)")
        cleaned[key] = _scalar(value)
    return cleaned


def default_idempotency_key(event_type: str, obj) -> str:
    if obj is None:
        return f"{event_type}:{uuid_lib.uuid4()}"
    label = f"{obj._meta.app_label}.{obj._meta.model_name}"
    return f"{event_type}:{label}:{obj.pk}"[:160]


def emit(
    event_type: str,
    obj=None,
    payload: dict | None = None,
    *,
    system: ExternalSystem | None = None,
    idempotency_key: str | None = None,
    occurred_at: dt.datetime | None = None,
) -> OutboundEvent | None:
    """
    Queue an outbound event. Returns ``None`` when the idempotency key already exists (duplicate).
    Never raises for a duplicate; raises PayloadRejected for a payload that breaks minimisation.
    """
    data = sanitize_payload(payload)
    key = idempotency_key or default_idempotency_key(event_type, obj)
    content_type = ContentType.objects.get_for_model(obj) if obj is not None else None
    try:
        with transaction.atomic():
            event = OutboundEvent.objects.create(
                event_type=event_type,
                system=system,
                content_type=content_type,
                object_id=str(obj.pk) if obj is not None else "",
                occurred_at=occurred_at or clock.now(),
                payload=data,
                idempotency_key=key,
                next_attempt_at=clock.now(),
            )
    except IntegrityError:
        log.info("outbound event duplicate ignored key=%s", key)
        return None
    log.info("outbound event queued type=%s uuid=%s", event_type, event.uuid)
    return event


def serialize_event(event: OutboundEvent) -> dict:
    return {
        "uuid": str(event.uuid),
        "event_type": event.event_type,
        "occurred_at": event.occurred_at.isoformat(),
        "status": event.status,
        "attempts": event.attempts,
        "object": {"type": event.object_type, "id": event.object_id} if event.object_id else None,
        "data": event.payload,
        "created_at": event.created_at.isoformat(),
        "delivered_at": event.delivered_at.isoformat() if event.delivered_at else None,
        "acknowledged_at": event.acknowledged_at.isoformat() if event.acknowledged_at else None,
    }


def backoff_seconds(attempts: int) -> int:
    return min(60 * (2 ** max(attempts - 1, 0)), conf.max_backoff_seconds())


def _endpoints_for(event: OutboundEvent) -> Iterable[WebhookEndpoint]:
    qs = WebhookEndpoint.objects.filter(is_active=True, system__is_active=True).select_related("system")
    if event.system_id:
        qs = qs.filter(system_id=event.system_id)
    return list(qs)


def _apply_result(event: OutboundEvent, result: DeliveryResult, now: dt.datetime) -> None:
    if result.skipped:
        event.last_error = result.error
        event.save(update_fields=["last_error", "updated_at"])
        return
    event.attempts += 1
    event.response_code = result.response_code
    if result.ok:
        event.status = OutboundEventStatus.DELIVERED
        event.delivered_at = now
        event.next_attempt_at = None
        event.last_error = ""
    else:
        event.last_error = result.error[:2000]
        if event.attempts >= conf.max_attempts():
            event.status = OutboundEventStatus.FAILED
            event.next_attempt_at = None
        else:
            event.status = OutboundEventStatus.QUEUED
            event.next_attempt_at = now + dt.timedelta(seconds=backoff_seconds(event.attempts))
    event.save(
        update_fields=[
            "attempts",
            "response_code",
            "status",
            "delivered_at",
            "next_attempt_at",
            "last_error",
            "updated_at",
        ]
    )


def deliver_pending(limit: int = 100) -> dict[str, int]:
    """Push queued events through the configured transport (cron / management command)."""
    now = clock.now()
    transport = get_transport()
    qs = (
        OutboundEvent.objects.filter(status=OutboundEventStatus.QUEUED, acknowledged_at__isnull=True)
        .filter(Q(next_attempt_at__isnull=True) | Q(next_attempt_at__lte=now))
        .order_by("created_at")[:limit]
    )
    counters = {"delivered": 0, "retry": 0, "failed": 0, "skipped": 0}
    for event in qs:
        try:
            result = transport.deliver(event, _endpoints_for(event))
        except Exception as exc:  # noqa: BLE001 - a transport bug must not stop the loop
            result = DeliveryResult(ok=False, error=f"transport error: {exc}"[:500])
        _apply_result(event, result, now)
        if result.skipped:
            counters["skipped"] += 1
        elif result.ok:
            counters["delivered"] += 1
        elif event.status == OutboundEventStatus.FAILED:
            counters["failed"] += 1
        else:
            counters["retry"] += 1
    return counters


def cancel_event(event: OutboundEvent, reason: str = "") -> None:
    if event.status in (OutboundEventStatus.QUEUED, OutboundEventStatus.FAILED):
        event.status = OutboundEventStatus.CANCELLED
        event.next_attempt_at = None
        event.last_error = reason[:2000]
        event.save(update_fields=["status", "next_attempt_at", "last_error", "updated_at"])


def requeue_event(event: OutboundEvent) -> None:
    if event.status in (OutboundEventStatus.FAILED, OutboundEventStatus.CANCELLED):
        event.status = OutboundEventStatus.QUEUED
        event.attempts = 0
        event.next_attempt_at = clock.now()
        event.last_error = ""
        event.save(update_fields=["status", "attempts", "next_attempt_at", "last_error", "updated_at"])


# --------------------------------------------------------------------------------------------
# Pull API helpers
# --------------------------------------------------------------------------------------------
def events_for_key(key: ApiKey) -> QuerySet[OutboundEvent]:
    """Events visible to a key: broadcast events plus those addressed to the key's system."""
    qs = OutboundEvent.objects.exclude(status=OutboundEventStatus.CANCELLED)
    if key.system_id:
        return qs.filter(Q(system__isnull=True) | Q(system_id=key.system_id))
    return qs.filter(system__isnull=True)


def acknowledge(event: OutboundEvent, key: ApiKey) -> OutboundEvent:
    """Idempotent: a second ack returns the same, unchanged event."""
    if event.acknowledged_at:
        return event
    now = clock.now()
    event.acknowledged_at = now
    event.acknowledged_by = key
    event.status = OutboundEventStatus.DELIVERED
    event.delivered_at = event.delivered_at or now
    event.next_attempt_at = None
    event.save(
        update_fields=["acknowledged_at", "acknowledged_by", "status", "delivered_at", "next_attempt_at", "updated_at"]
    )
    return event


# --------------------------------------------------------------------------------------------
# API keys
# --------------------------------------------------------------------------------------------
def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def create_api_key(
    name: str, scopes: Iterable[str], *, system: ExternalSystem | None = None, created_by=None, expires_at=None
) -> tuple[ApiKey, str]:
    """Create a key; the raw value is returned ONCE and never stored."""
    prefix = secrets.token_hex(4)
    raw = f"ile_{prefix}_{secrets.token_urlsafe(32)}"
    key = ApiKey.objects.create(
        name=name,
        prefix=prefix,
        key_hash=hash_key(raw),
        scopes=sorted(set(scopes)),
        system=system,
        created_by=created_by,
        expires_at=expires_at,
    )
    return key, raw


def touch_key(key: ApiKey) -> None:
    now = clock.now()
    if not key.last_used_at or (now - key.last_used_at).total_seconds() > 60:
        ApiKey.objects.filter(pk=key.pk).update(last_used_at=now)


# --------------------------------------------------------------------------------------------
# External references
# --------------------------------------------------------------------------------------------
def link_external_id(system: ExternalSystem, obj, external_id: str, *, synced: bool = True) -> ExternalReference:
    content_type = ContentType.objects.get_for_model(obj)
    ref, _created = ExternalReference.objects.update_or_create(
        system=system,
        content_type=content_type,
        object_id=str(obj.pk),
        defaults={
            "external_id": external_id,
            "sync_status": SyncStatus.SYNCED if synced else SyncStatus.PENDING,
            "last_synced_at": clock.now() if synced else None,
            "last_error": "",
        },
    )
    return ref


def external_id_of(system: ExternalSystem, obj) -> str | None:
    content_type = ContentType.objects.get_for_model(obj)
    ref = ExternalReference.objects.filter(system=system, content_type=content_type, object_id=str(obj.pk)).first()
    return ref.external_id if ref else None


def mark_sync_error(ref: ExternalReference, error: str) -> None:
    ref.sync_status = SyncStatus.ERROR
    ref.last_error = error[:2000]
    ref.save(update_fields=["sync_status", "last_error", "updated_at"])
