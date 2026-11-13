"""
Tiny API toolkit (ADR-011: no DRF yet): JSON envelope, decorator with auth + throttle + audit.

Success:  {"data": ..., "request_id": "..."}  (+ "pagination" on lists)
Error:    {"error": {"code": "...", "message": "...", "request_id": "..."}}
"""

from __future__ import annotations

import json
import logging
import re
from functools import wraps

from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core import throttle
from integrations import conf
from integrations.auth import ApiError, authenticate

log = logging.getLogger("ile.integrations")
API_VERSION = "v1"


def _request_id(request) -> str:
    return getattr(request, "request_id", "") or ""


def ok(request, data, status: int = 200, **extra) -> JsonResponse:
    body = {"data": data, "request_id": _request_id(request)}
    body.update(extra)
    response = JsonResponse(body, status=status)
    response["Cache-Control"] = "no-store"
    return response


def error(request, status: int, code: str, message: str) -> JsonResponse:
    response = JsonResponse(
        {"error": {"code": code, "message": message, "request_id": _request_id(request)}}, status=status
    )
    response["Cache-Control"] = "no-store"
    if status == 401:
        response["WWW-Authenticate"] = 'Bearer realm="italylegalentry-api"'
    return response


#: A JSON document's NUL: the decoder turns ``\u0000`` into one (a raw NUL byte it refuses itself, strict mode).
NUL = "\x00"

#: What a JSON string can carry and the database cannot store: the NUL, and a lone UTF-16 surrogate — ``\ud800`` …
#: ``\udfff`` escaped alone, which the decoder keeps as it is (a pair it joins into one character: «\ud83d\ude00» is
#: «😀»). PostgreSQL refuses the first in text and in jsonb; the second cannot even be encoded to UTF-8 for the query.
UNSTORABLE = re.compile("[\x00\ud800-\udfff]")


def carries_unstorable(value) -> bool:
    """
    Whether a decoded JSON value holds a NUL or a lone surrogate anywhere — in a string or in an object's key, at any
    depth.

    Either became a 500 at the first write — the NUL (finding F-8's API probe), the lone surrogate («Unicode low
    surrogate must follow a high surrogate», «surrogates not allowed»: the review of sec-f8, F8R-4) — and no identifier
    this API reads has a use for either. ``cms.middleware.NulByteMiddleware`` answers the path, the query string and
    the forms (whose decoding replaces a surrogate); a JSON body is this module's to answer.
    """
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, str):
            if UNSTORABLE.search(item):
                return True
        elif isinstance(item, dict):
            pending.extend(item.keys())
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    return False


def storable(value: str) -> str:
    """``value`` without what the database cannot store (``UNSTORABLE``) — for a header a refusal's log row keeps."""
    return UNSTORABLE.sub("", value)


def decode_json(body: bytes):
    """
    The body's JSON value — or ``None`` for a body that is not one this API accepts: invalid UTF-8 or JSON, nested
    deeper than the decoder recurses (``RecursionError``, not a ``ValueError``), or carrying a NUL or a lone surrogate
    (``carries_unstorable``).
    """
    try:
        value = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, RecursionError):
        return None
    return None if carries_unstorable(value) else value


def parse_json_body(request) -> dict:
    if not request.body:
        return {}
    data = decode_json(request.body)
    if data is None:
        raise ApiError(400, "invalid_json", "Request body is not valid JSON.")
    if not isinstance(data, dict):
        raise ApiError(400, "invalid_json", "Request body must be a JSON object.")
    return data


def api_endpoint(*, methods=("GET",), scopes=(), auth: bool = True, action: str):
    """Wrap a view: method check → auth → throttle → scopes → view; audit every call."""

    def decorator(view):
        @csrf_exempt
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            request.api_key = None
            try:
                if request.method not in methods:
                    raise ApiError(405, "method_not_allowed", f"Allowed methods: {', '.join(methods)}.")
                if auth:
                    key = authenticate(request)
                    limits = conf.api_throttle()
                    if not throttle.allow(request, f"api:{key.prefix}", limits["limit"], limits["window_seconds"]):
                        raise ApiError(429, "rate_limited", "Too many requests for this API key.")
                    for scope in scopes:
                        if not key.has_scope(scope):
                            raise ApiError(403, "insufficient_scope", f"Scope {scope!r} is required.")
                    request.api_key = key
                response = view(request, *args, **kwargs)
            except ApiError as exc:
                response = error(request, exc.status, exc.code, exc.message)
            except Http404:
                response = error(request, 404, "not_found", "Resource not found.")
            _audit(request, action, response.status_code)
            if request.method not in methods:
                response["Allow"] = ", ".join(methods)
            return response

        return wrapper

    return decorator


def _audit(request, action: str, status_code: int) -> None:
    try:
        from audit.services import record

        key = getattr(request, "api_key", None)
        record(
            request,
            action=f"api.{action}",
            metadata={
                "status": status_code,
                "key_prefix": key.prefix if key else "",
                "path": request.path[:200],
                "method": request.method,
            },
        )
    except Exception:  # noqa: BLE001 - auditing must never break the API response
        log.exception("api audit failed for %s", action)
