from __future__ import annotations

import threading
import uuid

from django.conf import settings
from django.middleware.gzip import GZipMiddleware

_local = threading.local()


def current_request_id() -> str:
    return getattr(_local, "request_id", "-")


class RequestIDMiddleware:
    """Attach a correlation id to every request (header X-Request-ID) and to log records."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming = request.headers.get("X-Request-ID", "")
        request_id = incoming[:64] if incoming and incoming.isalnum() else uuid.uuid4().hex
        request.request_id = request_id
        _local.request_id = request_id
        try:
            response = self.get_response(request)
        finally:
            _local.request_id = "-"
        response["X-Request-ID"] = request_id
        return response


class ExtraSecurityHeadersMiddleware:
    """Headers not covered by Django's SecurityMiddleware / django-csp."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Permissions-Policy", settings.PERMISSIONS_POLICY)
        response.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        response.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        return response


class BackofficeCSPMiddleware:
    """
    The back-office theme (django-unfold) is driven by Alpine.js, which evaluates expressions from
    HTML attributes and writes inline styles: under the public policy (``script-src 'self'``) every
    panel, modal and dropdown renders at once and the admin is unusable (browser QA 2026-09-20).

    The public site keeps the strict policy. ONLY responses under ``/backoffice/`` — reachable by
    authenticated staff, behind MFA in production — get ``'unsafe-inline'``/``'unsafe-eval'`` for
    scripts and ``'unsafe-inline'`` for styles, still limited to same-origin sources.

    django-csp applies ``response._csp_replace`` when it builds the header, so this middleware must
    be listed AFTER ``csp.middleware.CSPMiddleware`` (it then runs before it on the way out).
    """

    PREFIX = "/backoffice/"
    REPLACE = {
        "script-src": ("'self'", "'unsafe-inline'", "'unsafe-eval'"),
        "style-src": ("'self'", "'unsafe-inline'"),
        "img-src": ("'self'", "data:", "blob:"),
        "font-src": ("'self'", "data:"),
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(self.PREFIX):
            response._csp_replace = dict(self.REPLACE)
        return response


class LanguageCookieMiddleware:
    """
    Remember the language the visitor is reading.

    The language switcher is a list of plain links (``/ar/…``), so Django never wrote its language
    cookie: pages outside ``i18n_patterns`` (private documents, error pages) fell back to the browser
    language — an Arabic reader with a French browser got ``/documents/`` in French (I18N-05).

    Whenever a language-prefixed page is served successfully, the technical cookie
    ``settings.LANGUAGE_COOKIE_NAME`` is aligned with that prefix. It stores a two-letter code only —
    exactly the « mémorisation de la langue sélectionnée » purpose described by the Cookie Policy.
    Must be listed AFTER ``LocaleMiddleware`` (it then sees the final response).
    """

    MAX_AGE = 60 * 60 * 24 * 365

    def __init__(self, get_response):
        self.get_response = get_response
        self.languages = {code for code, _name in settings.LANGUAGES}

    def __call__(self, request):
        response = self.get_response(request)
        prefix = request.path_info.lstrip("/").split("/", 1)[0]
        if prefix in self.languages and response.status_code < 400:
            name = settings.LANGUAGE_COOKIE_NAME
            if request.COOKIES.get(name) != prefix:
                response.set_cookie(
                    name,
                    prefix,
                    max_age=self.MAX_AGE,
                    samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                    secure=settings.LANGUAGE_COOKIE_SECURE,
                    httponly=True,
                )
        return response


# Content types worth compressing: text the application renders. Anything else — a private PDF or
# a scanned identity document streamed by documents.views, an image — is either already compressed
# or large and binary, and gzipping it on the fly costs CPU for nothing (and drops Content-Length).
_COMPRESSIBLE = (
    "text/html",
    "text/plain",
    "text/csv",
    "application/json",
    "application/ld+json",
    "application/xml",
    "text/xml",
)


class TextGZipMiddleware(GZipMiddleware):
    """HTML compression in the application stack (Gate A, 26/09/2026 — approved by the product owner).

    Why here: the repository ships gunicorn + WhiteNoise and no reverse proxy (Dockerfile,
    docker-compose.staging.yml), so the application is the one layer that exists everywhere. If a
    proxy that compresses is added in front, it sees `Content-Encoding` and leaves the body alone:
    no double compression either way.

    Why it is safe: Django's GZipMiddleware (≥ 4.2) pads every gzip body with up to 100 random bytes
    against BREACH, and the CSRF token in a form is masked per response. Static files never reach
    it: settings put it BELOW WhiteNoiseMiddleware, which answers them first, already compressed.
    """

    def process_response(self, request, response):
        content_type = response.get("Content-Type", "").split(";")[0].strip().lower()
        if content_type not in _COMPRESSIBLE:
            return response
        return super().process_response(request, response)
