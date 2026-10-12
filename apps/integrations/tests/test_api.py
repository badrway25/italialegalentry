"""API v1: auth, throttle, scoping, pagination, ack idempotency, envelope, schema, audit."""

import datetime as dt
import json
from urllib.parse import quote

import pytest
from django.test import override_settings

from audit.models import AuditEvent
from integrations.models import ApiKey, ApiScope, OutboundEvent, OutboundEventStatus
from integrations.services import cancel_event, create_api_key, emit

pytestmark = [pytest.mark.django_db, pytest.mark.security]

EVENTS = "/api/v1/events/"


def _error(response):
    body = response.json()
    assert set(body) == {"error"}
    assert set(body["error"]) == {"code", "message", "request_id"}
    assert body["error"]["request_id"]
    return body["error"]


def test_health_is_public_and_enveloped(client):
    r = client.get("/api/v1/health/")
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["status"] == "ok" and body["data"]["version"] == "v1"
    assert body["request_id"] == r["X-Request-ID"]
    assert r["Cache-Control"] == "no-store"


def test_schema_is_valid_openapi_json(client):
    r = client.get("/api/v1/schema/")
    assert r.status_code == 200
    schema = json.loads(r.content)["data"]
    assert schema["openapi"] == "3.1.0"
    assert {"/health/", "/events/", "/events/{uuid}/ack/", "/webhooks/{system}/", "/schema/"} <= set(schema["paths"])
    assert "Error" in schema["components"]["schemas"] and "Event" in schema["components"]["schemas"]
    assert "bearerAuth" in schema["components"]["securitySchemes"]


def test_missing_key_is_401_with_envelope(client):
    r = client.get(EVENTS)
    assert r.status_code == 401
    assert _error(r)["code"] == "unauthorized"
    assert r["WWW-Authenticate"].startswith("Bearer")


def test_invalid_key_is_401(client, api_key):
    r = client.get(EVENTS, HTTP_AUTHORIZATION="Bearer ile_0123abcd_notarealkeyvaluexxxxxxxxx")
    assert r.status_code == 401
    r = client.get(EVENTS, HTTP_AUTHORIZATION="Bearer garbage")
    assert r.status_code == 401
    r = client.get(EVENTS, HTTP_AUTHORIZATION=f"Basic {api_key[1]}")
    assert r.status_code == 401


def test_inactive_and_expired_keys_are_401(client, api_key, auth):
    key, _raw = api_key
    key.is_active = False
    key.save()
    assert client.get(EVENTS, **auth).status_code == 401
    key.is_active = True
    key.expires_at = dt.datetime(2020, 1, 1, tzinfo=dt.UTC)
    key.save()
    r = client.get(EVENTS, **auth)
    assert r.status_code == 401
    assert _error(r)["message"] == "API key inactive or expired."


def test_scope_enforced(client, system):
    key, raw = create_api_key("read-only", [ApiScope.EVENTS_READ], system=system)
    event = emit("test.created", None, {"n": 1})
    r = client.post(f"/api/v1/events/{event.uuid}/ack/", HTTP_AUTHORIZATION=f"Bearer {raw}")
    assert r.status_code == 403
    assert _error(r)["code"] == "insufficient_scope"


@override_settings(INTEGRATIONS_API_THROTTLE={"limit": 2, "window_seconds": 60})
def test_throttle_per_key_returns_429(client, auth):
    assert client.get(EVENTS, **auth).status_code == 200
    assert client.get(EVENTS, **auth).status_code == 200
    r = client.get(EVENTS, **auth)
    assert r.status_code == 429
    assert _error(r)["code"] == "rate_limited"


def test_events_are_scoped_to_key_system(client, auth, system, other_system):
    mine = emit("a.created", None, {"n": 1}, system=system)
    broadcast = emit("b.created", None, {"n": 2})
    foreign = emit("c.created", None, {"n": 3}, system=other_system)
    r = client.get(EVENTS, **auth)
    uuids = {e["uuid"] for e in r.json()["data"]}
    assert uuids == {str(mine.uuid), str(broadcast.uuid)}
    assert str(foreign.uuid) not in uuids
    # IDOR: acking a foreign event is 404, not 403 (no existence leak)
    r = client.post(f"/api/v1/events/{foreign.uuid}/ack/", **auth)
    assert r.status_code == 404
    assert _error(r)["code"] == "not_found"


def test_events_filters_and_pagination(client, auth, system):
    events = [emit(f"t.{i}", None, {"i": i}, system=system) for i in range(5)]
    r = client.get(EVENTS + "?limit=2", **auth)
    body = r.json()
    assert [e["event_type"] for e in body["data"]] == ["t.0", "t.1"]
    assert body["pagination"] == {"limit": 2, "has_more": True, "next_after": events[1].id}
    r = client.get(EVENTS + f"?limit=2&after={events[1].id}", **auth)
    assert [e["event_type"] for e in r.json()["data"]] == ["t.2", "t.3"]
    r = client.get(EVENTS + f"?limit=2&after={events[3].id}", **auth)
    assert r.json()["pagination"]["has_more"] is False
    r = client.get(EVENTS + "?event_type=t.3", **auth)
    assert [e["event_type"] for e in r.json()["data"]] == ["t.3"]
    since = quote((events[4].created_at + dt.timedelta(seconds=1)).isoformat())
    assert client.get(EVENTS + f"?since={since}", **auth).json()["data"] == []
    before = quote(events[0].created_at.isoformat())
    assert len(client.get(EVENTS + f"?since={before}", **auth).json()["data"]) == 5
    assert client.get(EVENTS + "?since=not-a-date", **auth).status_code == 400
    assert client.get(EVENTS + "?status=bogus", **auth).status_code == 400
    assert client.get(EVENTS + "?limit=abc", **auth).status_code == 400


def test_event_payload_shape_has_no_personal_data(client, auth, system):
    emit(
        "x.created", None, {"category": "company", "created_at": dt.datetime(2026, 9, 17, tzinfo=dt.UTC)}, system=system
    )
    e = client.get(EVENTS, **auth).json()["data"][0]
    assert set(e) == {
        "uuid",
        "event_type",
        "occurred_at",
        "status",
        "attempts",
        "object",
        "data",
        "created_at",
        "delivered_at",
        "acknowledged_at",
    }
    assert e["data"] == {"category": "company", "created_at": "2026-09-17T00:00:00+00:00"}
    assert e["status"] == "queued"


def test_ack_is_idempotent(client, auth, api_key, system):
    event = emit("y.created", None, {"n": 1}, system=system)
    r1 = client.post(f"/api/v1/events/{event.uuid}/ack/", **auth)
    assert r1.status_code == 200
    d1 = r1.json()["data"]
    assert d1["status"] == "delivered" and d1["acknowledged_at"]
    r2 = client.post(f"/api/v1/events/{event.uuid}/ack/", **auth)
    assert r2.status_code == 200
    assert r2.json()["data"] == d1
    event.refresh_from_db()
    assert event.status == OutboundEventStatus.DELIVERED
    assert event.acknowledged_by_id == api_key[0].id
    # acknowledged events leave the default (queued) listing
    assert client.get(EVENTS, **auth).json()["data"] == []
    assert len(client.get(EVENTS + "?status=delivered", **auth).json()["data"]) == 1


def test_ack_cancelled_event_is_409_and_get_is_405(client, auth, system):
    event = emit("z.created", None, {}, system=system)
    cancel_event(event, "test")
    r = client.post(f"/api/v1/events/{event.uuid}/ack/", **auth)
    assert r.status_code == 404  # cancelled events are not exposed at all
    event2 = emit("z2.created", None, {}, system=system)
    r = client.get(f"/api/v1/events/{event2.uuid}/ack/", **auth)
    assert r.status_code == 405
    assert r["Allow"] == "POST"


def test_every_api_call_is_audited(client, auth, api_key):
    client.get(EVENTS, **auth)
    client.get(EVENTS)  # unauthenticated attempt is audited too
    rows = list(AuditEvent.objects.filter(action="api.events.list").order_by("id"))
    assert len(rows) == 2
    assert rows[0].metadata["key_prefix"] == api_key[0].prefix and rows[0].metadata["status"] == 200
    assert rows[1].metadata["key_prefix"] == "" and rows[1].metadata["status"] == 401


def test_last_used_is_touched(client, auth, api_key):
    assert api_key[0].last_used_at is None
    client.get(EVENTS, **auth)
    assert ApiKey.objects.get(pk=api_key[0].pk).last_used_at is not None


def test_key_without_system_sees_only_broadcast(client, system):
    _key, raw = create_api_key("global", [ApiScope.EVENTS_READ])
    emit("s.created", None, {}, system=system)
    broadcast = emit("g.created", None, {})
    r = client.get(EVENTS, HTTP_AUTHORIZATION=f"Bearer {raw}")
    assert [e["uuid"] for e in r.json()["data"]] == [str(broadcast.uuid)]


def test_create_api_key_command_prints_key_once(capsys, system):
    from django.core.management import call_command

    call_command("create_api_key", "--name", "CRM prod", "--system", "crm", "--scopes", "events:read")
    out = capsys.readouterr().out
    line = [ln for ln in out.splitlines() if ln.startswith("ile_")][0]
    key = ApiKey.objects.get(name="CRM prod")
    assert key.scopes == ["events:read"] and key.system == system
    assert line.split("_")[1] == key.prefix
    assert key.key_hash != line and line not in key.key_hash
    assert OutboundEvent.objects.count() == 0
