"""
The integrations API answers NUL bytes and other unexpected input with a controlled response — never a 500, never a NUL
written to the database (finding F-8's fifth item; DL54-152 item 8: «JSON bodies with a NUL (the integrations API,
behind its key) are left to their view; not probed»).

``cms.middleware.NulByteMiddleware`` answers a NUL in the path, the query string, a form field or the session cookie;
it never parses a JSON body (the API reads its own raw body, ``csrf_exempt``). Probed on 16 October 2026, before the
fix:

* a signed webhook body whose JSON carries ``\\u0000`` in an identifier — PostgreSQL refuses it in the log's jsonb
  («unsupported Unicode escape sequence») and psycopg refuses it in ``event_type`` (text): a 500, for any holder of the
  system's shared secret;
* ``X-Nonce`` / ``X-Timestamp`` carrying a NUL, written as received into the refusal's log row: a 500 for anybody who
  knows an active system's key (a NUL never reaches here through nginx, which refuses it in a header; Django's own
  server and the test client let it through);
* ``X-Timestamp: ²`` — ``str.isdigit`` accepts a superscript, ``int`` refuses it — and a timestamp of 5 000 digits
  (beyond Python's integer-string limit): a 500 before any signature is checked;
* ``X-Signature`` carrying a non-ASCII character: ``hmac.compare_digest`` raises on a non-ASCII ``str``, a 500;
* a signed body nested deeper than the JSON decoder recurses: ``RecursionError``, not ``ValueError``, a 500;
* behind an API key, ``events_list``'s ``since`` with an impossible date (``ValueError`` from ``parse_datetime``) and
  ``after`` / ``limit`` as ``²``, ``--5`` or 5 000 digits: a 500.

Raw NUL bytes inside or outside a JSON string were already refused by the decoder (strict mode): a 400, held here.

The review of the fix (F8R-4) found the NUL's sibling: a lone UTF-16 surrogate escaped in a signed body (``\\ud800``
alone, half a pair) — the decoder keeps it, PostgreSQL refuses it in the log's jsonb («Unicode low surrogate must follow
a high surrogate») and psycopg cannot encode it for ``event_type`` («surrogates not allowed»): a 500 with a traceback.
It meets the NUL's answer now (a 400 that consumes no nonce); a surrogate PAIR is one character and is accepted.
"""

from __future__ import annotations

import json
import logging
import time

import pytest

from integrations import api
from integrations.auth import ApiError
from integrations.models import InboundWebhookLog
from integrations.webhooks import compute_signature

pytestmark = [pytest.mark.django_db, pytest.mark.security]

SECRET = "test-shared-secret-value"
URL = "/api/v1/webhooks/crm/"
EVENTS = "/api/v1/events/"


@pytest.fixture(autouse=True)
def _secret_env(monkeypatch):
    monkeypatch.setenv("ILE_TEST_WEBHOOK_SECRET", SECRET)


@pytest.fixture
def quiet(caplog):
    """No ERROR line and no traceback: a controlled answer is not an incident."""
    yield caplog
    loud = [(r.levelname, r.name, r.getMessage()) for r in caplog.records if r.levelno >= logging.ERROR or r.exc_info]
    assert not loud, f"an ERROR line or a traceback in the log: {loud}"


def _headers(body: bytes, *, nonce="nonce-f8-0001", timestamp=None, signature=None):
    ts = str(int(time.time())) if timestamp is None else timestamp
    sig = signature or compute_signature(SECRET.encode(), ts, nonce, body)
    return {"HTTP_X_SIGNATURE": sig, "HTTP_X_TIMESTAMP": ts, "HTTP_X_NONCE": nonce, "content_type": "application/json"}


def _no_nul_stored() -> None:
    for row in InboundWebhookLog.objects.all():
        stored = json.dumps(row.payload) + row.event_type + row.nonce + row.timestamp + row.error + row.system_key
        assert "\x00" not in stored and "\\u0000" not in stored, row.pk


def _nothing_unstorable_stored() -> None:
    for row in InboundWebhookLog.objects.all():
        stored = json.dumps(row.payload, ensure_ascii=False) + row.event_type + row.nonce + row.timestamp + row.error
        assert not api.UNSTORABLE.search(stored), row.pk


@pytest.fixture
def client_(client):
    client.raise_request_exception = False
    return client


# ---------------------------------------------------------------------------------------------
# The public webhook
# ---------------------------------------------------------------------------------------------
class TestTheWebhook:
    @pytest.mark.parametrize(
        "payload",
        [
            {"event": "crm.contact.updated\u0000", "external_id": "C-1"},
            {"event": "crm.contact.updated", "external_id": "C-\u00001"},
            {"event": "crm.contact.updated", "status": "\u0000"},
            {"event": "crm.contact.updated", "nested": {"note\u0000": ["\u0000"]}},
        ],
    )
    def test_an_escaped_nul_in_a_signed_body_is_a_400_and_nothing_with_it_is_stored(
        self, client_, system, quiet, payload
    ):
        body = json.dumps(payload).encode()
        assert b"\\u0000" in body
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 400, response.content
        assert response.json()["error"]["code"] == "invalid_json"
        _no_nul_stored()
        # the refusal consumed no nonce: the same nonce with a clean body is still accepted
        clean = json.dumps({"event": "crm.contact.updated", "external_id": "C-1"}).encode()
        assert client_.post(URL, data=clean, **_headers(clean)).status_code == 202

    @pytest.mark.parametrize(
        "body",
        [b'{"event": "a\x00b"}', b'{"event": "a"}\x00', b"\x00", b'{"\x00": 1}'],
        ids=["in-a-string", "after-the-object", "alone", "in-a-key"],
    )
    def test_a_raw_nul_byte_in_the_body_is_a_400(self, client_, system, quiet, body):
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 400 and response.json()["error"]["code"] == "invalid_json"
        _no_nul_stored()

    @pytest.mark.parametrize("header", ["HTTP_X_NONCE", "HTTP_X_TIMESTAMP"])
    def test_a_nul_in_a_header_is_refused_and_never_stored(self, client_, system, quiet, header):
        body = json.dumps({"event": "crm.contact.updated"}).encode()
        headers = _headers(body)
        headers[header] = headers[header] + "\x00"
        response = client_.post(URL, data=body, **headers)
        assert response.status_code == 401 and response.json()["error"]["code"] == "malformed_headers"
        assert InboundWebhookLog.objects.filter(status_code=401).count() == 1, "the refusal is still logged"
        _no_nul_stored()

    @pytest.mark.parametrize(
        "timestamp",
        ["²", "١٢٣", "9" * 5000, "+1700000000", " "],
        ids=["superscript", "arabic-indic", "5000-digits", "signed", "blank"],
    )
    def test_a_timestamp_that_is_no_plain_number_is_refused(self, client_, system, quiet, timestamp):
        body = json.dumps({"event": "crm.contact.updated"}).encode()
        response = client_.post(URL, data=body, **_headers(body, timestamp=timestamp, signature="sha256=00"))
        assert response.status_code == 401 and response.json()["error"]["code"] == "malformed_headers"

    @pytest.mark.parametrize(
        "signature",
        ["sha256=é", "sha256=☃", "sha256=" + "f" * 63 + "é"],
        ids=["accent", "snowman", "long-then-accent"],
    )
    def test_a_signature_that_is_not_ascii_is_refused(self, client_, system, quiet, signature):
        body = json.dumps({"event": "crm.contact.updated"}).encode()
        response = client_.post(URL, data=body, **_headers(body, signature=signature))
        assert response.status_code == 401 and response.json()["error"]["code"] == "invalid_signature"

    def test_a_body_nested_deeper_than_the_decoder_recurses_is_a_400(self, client_, system, quiet):
        body = b"[" * 100_000 + b"]" * 100_000
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 400 and response.json()["error"]["code"] == "invalid_json"

    def test_a_clean_signed_body_is_still_accepted(self, client_, system, quiet):
        body = json.dumps({"event": "crm.contact.updated", "external_id": "C-1"}).encode()
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 202
        assert InboundWebhookLog.objects.get(pk=response.json()["data"]["log_id"]).payload["external_id"] == "C-1"

    @pytest.mark.parametrize(
        "body",
        [
            b'{"event": "crm.contact.updated", "external_id": "\\ud800"}',
            b'{"event": "\\udfff"}',
            b'{"event": "crm.contact.updated", "status": "\\ud83d"}',
            b'{"event": "crm.contact.updated", "id": "C-\\ude00-1"}',
            b'{"event": "crm.contact.updated", "nested": {"\\udc00": ["x"]}}',
        ],
        ids=["high-alone-in-a-kept-id", "low-alone-in-the-event", "half-a-pair", "low-alone-mid-string", "in-a-key"],
    )
    def test_a_lone_surrogate_in_a_signed_body_is_a_400_and_nothing_with_it_is_stored(
        self, client_, system, quiet, body
    ):
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 400, response.content
        assert response.json()["error"]["code"] == "invalid_json"
        assert not InboundWebhookLog.objects.filter(status_code=202).exists()
        _nothing_unstorable_stored()
        # the refusal consumed no nonce: the same nonce with a clean body is still accepted
        clean = json.dumps({"event": "crm.contact.updated", "external_id": "C-1"}).encode()
        assert client_.post(URL, data=clean, **_headers(clean)).status_code == 202

    def test_a_surrogate_pair_is_one_character_and_is_accepted(self, client_, system, quiet):
        body = b'{"event": "crm.contact.updated", "external_id": "C-\\ud83d\\ude00"}'
        response = client_.post(URL, data=body, **_headers(body))
        assert response.status_code == 202
        row = InboundWebhookLog.objects.get(pk=response.json()["data"]["log_id"])
        assert row.payload["external_id"] == "C-\U0001f600"

    @pytest.mark.parametrize("header", ["HTTP_X_NONCE", "HTTP_X_TIMESTAMP"])
    def test_a_lone_surrogate_in_a_header_is_refused_and_never_stored(self, client_, system, quiet, header):
        """A WSGI server hands headers over as Latin-1, so no surrogate arrives that way; the test client can — the
        refusal's log row is written without it all the same."""
        body = json.dumps({"event": "crm.contact.updated"}).encode()
        headers = _headers(body)
        headers[header] = headers[header] + "\ud800"
        response = client_.post(URL, data=body, **headers)
        assert response.status_code == 401 and response.json()["error"]["code"] == "malformed_headers"
        assert InboundWebhookLog.objects.filter(status_code=401).count() == 1, "the refusal is still logged"
        _nothing_unstorable_stored()


# ---------------------------------------------------------------------------------------------
# Behind an API key
# ---------------------------------------------------------------------------------------------
class TestTheKeyedEndpoints:
    @pytest.mark.parametrize(
        "query",
        [
            {"since": "2026-13-45T00:00:00+00:00"},
            {"since": "2026-02-30T10:00:00+01:00"},
            {"after": "²"},
            {"after": "--5"},
            {"after": "9" * 5000},
            {"limit": "١٢٣٤٥٦٧٨٩٠" * 500},
            {"limit": "-"},
        ],
        ids=["month-13", "february-30", "after-superscript", "after-double-minus", "after-5000", "limit-5000", "dash"],
    )
    def test_an_impossible_parameter_is_a_400(self, client_, auth, quiet, query):
        response = client_.get(EVENTS, query, **auth)
        assert response.status_code == 400, response.content
        assert response.json()["error"]["code"] == "invalid_parameter"

    def test_a_nul_in_the_query_string_is_the_projects_400(self, client_, auth, quiet):
        assert client_.get(f"{EVENTS}?status=queued%00", **auth).status_code == 400

    def test_a_json_body_with_a_nul_on_the_acknowledgement_is_never_a_500(self, client_, auth, quiet):
        body = json.dumps({"note": "\u0000"}).encode()
        url = f"{EVENTS}00000000-0000-0000-0000-000000000000/ack/"
        response = client_.post(url, data=body, content_type="application/json", **auth)
        assert response.status_code == 404 and response.json()["error"]["code"] == "not_found"

    def test_plain_parameters_still_work(self, client_, auth, quiet):
        response = client_.get(EVENTS, {"after": "0", "limit": "10", "since": "2026-01-01T00:00:00+00:00"}, **auth)
        assert response.status_code == 200


# ---------------------------------------------------------------------------------------------
# The toolkit's own reader
# ---------------------------------------------------------------------------------------------
class TestTheBodyReader:
    @pytest.mark.parametrize(
        "body",
        [
            b'{"a": "\\u0000"}',
            b'{"\\u0000": 1}',
            b'{"a": ["x", {"b": "\\u0000"}]}',
            b"[" * 100_000,
            b'{"a": "\\ud800"}',
            b'{"\\udfff": 1}',
        ],
        ids=["in-a-value", "in-a-key", "nested", "too-deep", "lone-surrogate-value", "lone-surrogate-key"],
    )
    def test_parse_json_body_refuses_what_the_database_would(self, rf, body):
        request = rf.post("/api/v1/anything/", data=body, content_type="application/json")
        with pytest.raises(ApiError) as refused:
            api.parse_json_body(request)
        assert refused.value.status == 400 and refused.value.code == "invalid_json"

    def test_parse_json_body_still_reads_an_object(self, rf):
        request = rf.post("/api/v1/anything/", data=b'{"a": [1, "b"]}', content_type="application/json")
        assert api.parse_json_body(request) == {"a": [1, "b"]}

    def test_parse_json_body_reads_a_surrogate_pair_as_its_character(self, rf):
        request = rf.post("/api/v1/anything/", data=b'{"a": "\\ud83d\\ude00"}', content_type="application/json")
        assert api.parse_json_body(request) == {"a": "\U0001f600"}
