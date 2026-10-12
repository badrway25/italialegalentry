"""Inbound webhooks: HMAC-SHA256 signature, timestamp window, nonce replay protection, audit."""

import hashlib
import json
import time

import pytest

from audit.models import AuditEvent
from integrations.models import InboundWebhookLog
from integrations.webhooks import compute_signature

pytestmark = [pytest.mark.django_db, pytest.mark.security]

SECRET = "test-shared-secret-value"
URL = "/api/v1/webhooks/crm/"


@pytest.fixture(autouse=True)
def _secret_env(monkeypatch):
    monkeypatch.setenv("ILE_TEST_WEBHOOK_SECRET", SECRET)


def _headers(body: bytes, *, timestamp=None, nonce="nonce-0001", secret=SECRET, signature=None):
    ts = str(int(timestamp if timestamp is not None else time.time()))
    sig = signature or compute_signature(secret.encode(), ts, nonce, body)
    return {"HTTP_X_SIGNATURE": sig, "HTTP_X_TIMESTAMP": ts, "HTTP_X_NONCE": nonce, "content_type": "application/json"}


def _body(**extra) -> bytes:
    payload = {"event": "crm.contact.updated", "external_id": "C-1", "email": "person@example.test", **extra}
    return json.dumps(payload).encode()


def test_valid_signature_is_accepted_logged_and_audited(client, system):
    body = _body()
    r = client.post(URL, data=body, **_headers(body))
    assert r.status_code == 202, r.content
    assert r.json()["data"]["accepted"] is True
    log = InboundWebhookLog.objects.get()
    assert log.signature_valid and log.status_code == 202 and log.system == system
    assert log.event_type == "crm.contact.updated"
    assert log.payload == {"event": "crm.contact.updated", "external_id": "C-1"}  # e-mail never stored
    assert AuditEvent.objects.filter(action="webhook.received").exists()


def test_invalid_signature_is_401(client, system):
    body = _body()
    r = client.post(URL, data=body, **_headers(body, secret="wrong-secret"))
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "invalid_signature"
    log = InboundWebhookLog.objects.get()
    assert log.signature_valid is False and log.error == "invalid_signature"
    assert AuditEvent.objects.filter(action="webhook.rejected").exists()


def test_tampered_body_is_rejected(client, system):
    body = _body()
    headers = _headers(body)
    r = client.post(URL, data=_body(external_id="C-2"), **headers)
    assert r.status_code == 401


def test_replay_of_same_nonce_is_401(client, system):
    body = _body()
    headers = _headers(body, nonce="replay-nonce-1")
    assert client.post(URL, data=body, **headers).status_code == 202
    r = client.post(URL, data=body, **headers)
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "replay"
    assert InboundWebhookLog.objects.filter(nonce="replay-nonce-1", signature_valid=True).count() == 1
    # a fresh nonce works again
    body2 = _body()
    assert client.post(URL, data=body2, **_headers(body2, nonce="replay-nonce-2")).status_code == 202


def test_stale_timestamp_is_401(client, system):
    body = _body()
    r = client.post(URL, data=body, **_headers(body, timestamp=time.time() - 3600))
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "timestamp_out_of_range"


def test_unknown_or_inactive_system_is_401(client, system):
    body = _body()
    r = client.post("/api/v1/webhooks/nope/", data=body, **_headers(body))
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unknown_system"
    system.is_active = False
    system.save()
    assert client.post(URL, data=body, **_headers(body)).status_code == 401


def test_missing_secret_env_is_401(client, system, monkeypatch):
    monkeypatch.delenv("ILE_TEST_WEBHOOK_SECRET")
    body = _body()
    r = client.post(URL, data=body, **_headers(body))
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "secret_not_configured"


def test_secret_fingerprint_mismatch_is_401(client, system):
    system.inbound_secret_hash = hashlib.sha256(b"another").hexdigest()
    system.save()
    body = _body()
    assert client.post(URL, data=body, **_headers(body)).status_code == 401
    system.inbound_secret_hash = hashlib.sha256(SECRET.encode()).hexdigest()
    system.save()
    assert client.post(URL, data=body, **_headers(body, nonce="fingerprint-ok-1")).status_code == 202


def test_malformed_headers_and_body(client, system):
    body = _body()
    r = client.post(URL, data=body, **{**_headers(body), "HTTP_X_NONCE": "x"})
    assert r.status_code == 401 and r.json()["error"]["code"] == "malformed_headers"
    bad = b"not json"
    r = client.post(URL, data=bad, **_headers(bad, nonce="bad-json-1"))
    assert r.status_code == 400 and r.json()["error"]["code"] == "invalid_json"
    # the nonce was not consumed by the malformed request
    good = _body()
    assert client.post(URL, data=good, **_headers(good, nonce="bad-json-1")).status_code == 202


def test_get_is_not_allowed(client, system):
    r = client.get(URL)
    assert r.status_code == 405
    assert r.json()["error"]["code"] == "method_not_allowed"
