"""
Tiny API toolkit (ADR-011: no DRF yet): JSON envelope, decorator with auth + throttle + audit.

Success:  {"data": ..., "request_id": "..."}  (+ "pagination" on lists)
Error:    {"error": {"code": "...", "message": "...", "request_id": "..."}}
"""

from __future__ import annotations

import json
import logging
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


def parse_json_body(request) -> dict:
    if not request.body:
        return {}
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ApiError(400, "invalid_json", "Request body is not valid JSON.") from exc
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
