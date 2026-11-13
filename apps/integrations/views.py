"""
API v1 views — thin: validation + envelope; logic in services / webhooks.

Unexpected input meets a controlled answer, never a 500 (finding F-8's API probe): a parameter that is not a plain
number or a possible date is a 400; a webhook body that is not a JSON object this API accepts — invalid, nested deeper
than the decoder recurses, or carrying a NUL or a lone surrogate, which the log's text and jsonb cannot store (the
review of sec-f8, F8R-4) — is a 400 that consumes no nonce; the headers a refusal logs are written without either.
"""

from __future__ import annotations

import logging
import re

from django.db import IntegrityError, transaction
from django.http import Http404
from django.utils.dateparse import parse_datetime

from core import clock
from integrations import api, conf
from integrations.auth import ApiError
from integrations.models import ApiScope, InboundWebhookLog, OutboundEventStatus
from integrations.openapi import SCHEMA
from integrations.services import acknowledge, events_for_key, serialize_event
from integrations.webhooks import minimal_inbound_payload, verify

log = logging.getLogger("ile.integrations")


@api.api_endpoint(methods=("GET",), auth=False, action="health")
def health(request):
    return api.ok(request, {"status": "ok", "version": api.API_VERSION, "time": clock.now().isoformat()})


@api.api_endpoint(methods=("GET",), auth=False, action="schema")
def schema(request):
    return api.ok(request, SCHEMA)


#: An integer parameter as a client writes one: ASCII digits, an optional minus, a length ``int`` always reads
#: (``str.isdigit`` accepts «²», which ``int`` refuses, and Python refuses an integer string beyond 4 300 digits).
_INTEGER = re.compile(r"-?[0-9]{1,20}", re.ASCII)


def _logged(value: str, limit: int) -> str:
    """A header's value as a refusal's log row keeps it: without what the database cannot store (a NUL, a lone
    surrogate — ``api.storable``), bounded."""
    return api.storable(value)[:limit]


def _int_param(request, name: str, default: int, minimum: int, maximum: int) -> int:
    raw = request.GET.get(name)
    if raw is None or raw == "":
        return default
    if not _INTEGER.fullmatch(raw):
        raise ApiError(400, "invalid_parameter", f"Parameter {name!r} must be an integer.")
    return max(minimum, min(int(raw), maximum))


@api.api_endpoint(methods=("GET",), scopes=(ApiScope.EVENTS_READ,), action="events.list")
def events_list(request):
    qs = events_for_key(request.api_key)
    status = request.GET.get("status", "queued")
    if status not in ("queued", "delivered", "failed", "all"):
        raise ApiError(400, "invalid_parameter", "Parameter 'status' must be queued, delivered, failed or all.")
    if status != "all":
        qs = qs.filter(status=status)
    since = request.GET.get("since")
    if since:
        try:
            parsed = parse_datetime(since)
        except ValueError:  # well formed, impossible: «2026-02-30T10:00:00+01:00»
            parsed = None
        if parsed is None:
            raise ApiError(400, "invalid_parameter", "Parameter 'since' must be an ISO-8601 date-time.")
        if parsed.tzinfo is None:
            raise ApiError(400, "invalid_parameter", "Parameter 'since' must carry a timezone offset.")
        qs = qs.filter(created_at__gte=parsed)
    event_type = request.GET.get("event_type")
    if event_type:
        qs = qs.filter(event_type=event_type[:80])
    after = _int_param(request, "after", 0, 0, 2**53)
    limit = _int_param(request, "limit", 50, 1, conf.api_page_limit())
    rows = list(qs.filter(id__gt=after).select_related("content_type").order_by("id")[: limit + 1])
    has_more = len(rows) > limit
    rows = rows[:limit]
    return api.ok(
        request,
        [serialize_event(e) for e in rows],
        pagination={"limit": limit, "has_more": has_more, "next_after": rows[-1].id if has_more else None},
    )


@api.api_endpoint(methods=("POST",), scopes=(ApiScope.EVENTS_ACK,), action="events.ack")
def events_ack(request, uuid):
    event = events_for_key(request.api_key).filter(uuid=uuid).first()
    if event is None:
        raise Http404
    if event.status == OutboundEventStatus.CANCELLED:
        raise ApiError(409, "event_cancelled", "This event was cancelled and cannot be acknowledged.")
    event = acknowledge(event, request.api_key)
    return api.ok(request, serialize_event(event))


@api.api_endpoint(methods=("POST",), auth=False, action="webhooks.inbound")
def inbound_webhook(request, system):
    body = request.body
    if len(body) > conf.max_webhook_body_bytes():
        return api.error(request, 413, "payload_too_large", "Body exceeds the accepted size.")
    verification = verify(system, request.headers, body)
    log_row = InboundWebhookLog(
        system=verification.system,
        system_key=system[:40],
        nonce=_logged(verification.nonce, 64),
        timestamp=_logged(verification.timestamp, 32),
        signature_valid=verification.ok,
        request_id=getattr(request, "request_id", "")[:64],
    )
    if not verification.ok:
        log_row.status_code = 401
        log_row.error = verification.code
        log_row.save()
        _audit_webhook(request, "webhook.rejected", log_row)
        return api.error(request, 401, verification.code, "Webhook rejected.")
    payload = api.decode_json(body) if body else {}
    if payload is None or not isinstance(payload, dict):
        log_row.signature_valid = False  # do not consume the nonce for a malformed body
        log_row.status_code = 400
        log_row.error = "invalid_json"
        log_row.save()
        _audit_webhook(request, "webhook.rejected", log_row)
        return api.error(request, 400, "invalid_json", "Request body is not a JSON object.")
    log_row.payload = minimal_inbound_payload(payload)
    log_row.event_type = str(payload.get("event") or payload.get("event_type") or "")[:80]
    log_row.status_code = 202
    try:
        with transaction.atomic():
            log_row.save()
    except IntegrityError:
        log_row = InboundWebhookLog.objects.create(
            system=verification.system,
            system_key=system[:40],
            nonce=_logged(verification.nonce, 64),
            timestamp=_logged(verification.timestamp, 32),
            signature_valid=False,
            status_code=401,
            error="replay",
            request_id=getattr(request, "request_id", "")[:64],
        )
        _audit_webhook(request, "webhook.rejected", log_row)
        return api.error(request, 401, "replay", "Nonce already used.")
    _audit_webhook(request, "webhook.received", log_row)
    return api.ok(request, {"accepted": True, "log_id": log_row.pk}, status=202)


def _audit_webhook(request, action: str, log_row: InboundWebhookLog) -> None:
    try:
        from audit.services import record

        record(
            request,
            action=action,
            target=log_row,
            metadata={"system": log_row.system_key, "status": log_row.status_code, "error": log_row.error},
        )
    except Exception:  # noqa: BLE001
        log.exception("webhook audit failed")
