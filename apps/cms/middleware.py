"""
Legacy URL handling for the migration from the WordPress site (docs/URL_MIGRATION_MAP.md).

* ``/?lang=xx`` (old client-side language switch)      → 301 ``/xx/``
* WordPress sitemaps                                   → 301 ``/sitemap.xml``
* WordPress endpoints, default post, author page, feed → 410 Gone (never redirected: the author
  page and the API have no public equivalent)
* anything else that ends in a 404                     → ``cms.Redirect`` rows (back-office editable)

The middleware never touches a request that resolves normally, so it cannot shadow a real page.

And the requests no URL of the site can hold: a NUL byte in the path, the query string, a form field or the session
cookie is answered with the 400 page before anything reads it (``NulByteMiddleware``, listed near the top of the chain:
the redirect lookup below was the first place such a path broke).
"""

from __future__ import annotations

import re

from django.conf import settings
from django.core.exceptions import BadRequest, SuspiciousOperation
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, UnreadablePostError
from django.http.multipartparser import MultiPartParserError
from django.shortcuts import render
from django.urls import get_resolver, get_urlconf

NUL = "\x00"

#: What reading request.POST raises on a body Django will not parse: a client gone mid-upload (UnreadablePostError), a
#: malformed multipart body, the limits (TooManyFieldsSent, TooManyFilesSent, RequestDataTooBig: SuspiciousOperation),
#: an urlencoded body declared in another charset (BadRequest).
UNPARSABLE = (UnreadablePostError, MultiPartParserError, SuspiciousOperation, BadRequest)

GONE_PATTERNS = tuple(
    re.compile(p)
    for p in (
        r"^/wp-json(/|$)",
        r"^/wp-admin(/|$)",
        r"^/wp-content(/|$)",
        r"^/wp-includes(/|$)",
        r"^/wp-login\.php$",
        r"^/xmlrpc\.php$",
        r"^/readme\.html$",
        r"^/hello-world/?$",
        r"^/category(/|$)",
        r"^/author(/|$)",
        r"^/feed/?$",
        r"^/comments/feed/?$",
    )
)
WP_SITEMAP = re.compile(r"^/wp-sitemap[\w.-]*\.xml$")


class LegacyURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.languages = {code for code, _name in settings.LANGUAGES}

    def __call__(self, request):
        early = self.early_response(request)
        if early is not None:
            return early
        response = self.get_response(request)
        if response.status_code == 404:
            redirect = self.lookup_redirect(request.path)
            if redirect is not None:
                return redirect
        return response

    def early_response(self, request):
        path = request.path
        if path == "/":
            lang = (request.GET.get("lang") or "").lower()[:5]
            if lang in self.languages:
                return HttpResponsePermanentRedirect(f"/{lang}/")
            return None
        if WP_SITEMAP.match(path):
            return HttpResponsePermanentRedirect("/sitemap.xml")
        if any(p.match(path) for p in GONE_PATTERNS):
            return render(request, "errors/410.html", status=410)
        return None

    @staticmethod
    def lookup_redirect(path: str):
        from cms.models import Redirect

        if NUL in path:
            # PostgreSQL refuses a NUL in text (psycopg raises DataError): no row can hold one. NulByteMiddleware
            # answers such a request long before this; this line holds if the guard is ever moved or removed.
            return None
        candidates = {path, path.rstrip("/") or "/", path if path.endswith("/") else path + "/"}
        row = Redirect.objects.filter(old_path__in=candidates).first()
        if row is None or not row.new_path.startswith("/") or row.new_path.startswith("//"):
            return None  # only same-site targets: no open redirect through the back-office table
        cls = HttpResponsePermanentRedirect if row.permanent else HttpResponseRedirect
        return cls(row.new_path)


class NulByteMiddleware:
    """
    A NUL byte in the path, the query string, a form field or the session cookie: the project's own 400 page, before
    anything reads the value.

    PostgreSQL refuses a NUL in text — psycopg raises DataError before the query leaves; in a jsonb value, «unsupported
    Unicode escape sequence» — and no URL, search term, form field or session key of this site has a use for one. Until
    16 October 2026 each of these vectors ended in a 500 and an ERROR line with its traceback, one per request, for
    anyone (gate 2's N-4, carried by gates 3 and 4 as N-G; docs/design-v5/QA/v54/devops/NOTES.md, second pass):

    * the path — ``LegacyURLMiddleware.lookup_redirect``, after the page's 404;
    * the query string — the view (``news.services.category_by_slug``, for one);
    * a form field a view reads without a form (a case file's transition and its reason → ``audit.services.record``).
      Django's form fields refuse a NUL themselves (``ProhibitNullCharactersValidator``); not every value goes through
      one;
    * the session cookie — an octal escape (``"\\000…"``) that Python's cookie parser decodes, then the session lookup.

    Listed after RequestIDMiddleware and LocaleMiddleware — the page carries the request's id and speaks its language —
    and before everything that reads a value: the session (AuthenticationMiddleware), CSRF, the views, the redirect
    lookup. The middlewares that write the site's security headers stand above it (config/settings/base.py), so its
    page carries them as every page does. The answer is the URLconf's 400 handler (config.urls ``handler400``, drawn
    without the request), returned rather than raised: Django logs a raised SuspiciousOperation at ERROR with its
    traceback, and a returned 400 at WARNING, the path escaped.

    The path, the query string and the session cookie are looked at first, before anything reads them. A POST's form
    fields are looked at in ``process_view``, where CsrfViewMiddleware reads the same form a step later (this guard's
    ``process_view`` runs first), and only for the views it protects. A ``csrf_exempt`` view reads its body itself: the
    integrations API reads it raw, which Django refuses once it has parsed a multipart body from the request's
    stream — the public webhook answered 500 to any multipart POST while this guard read every form (the review of the
    second pass, REVIEW_2 M1). A body Django will not parse (``UNPARSABLE``) is not this guard's to answer either: it
    goes on to the next reader, which answers it as it did before the guard — CSRF refuses a request without its
    cookie (403) before it reads anything. A file's bytes are never read: an uploaded document holds NUL bytes by
    nature, and lives in ``request.FILES``. A body that is not a form (the integrations API's JSON) is never parsed as
    one.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.carries_nul(request):
            return self.bad_request(request)
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method != "POST" or getattr(view_func, "csrf_exempt", False):
            return None
        try:
            fields = request.POST  # cached on the request: CsrfViewMiddleware and the view read this same parse
        except UNPARSABLE:
            return None
        if any(NUL in name or any(NUL in value for value in values) for name, values in fields.lists()):
            return self.bad_request(request)
        return None

    @staticmethod
    def carries_nul(request) -> bool:
        """The path, the query string, the session cookie: what every request carries, whatever its view."""
        if NUL in request.path_info:
            return True
        # The raw query string: a NUL is `%00` there (or the byte itself). Parsing it would raise TooManyFieldsSent
        # beyond DATA_UPLOAD_MAX_NUMBER_FIELDS on a page that never reads its query.
        query = request.META.get("QUERY_STRING", "")
        if NUL in query or "%00" in query:
            return True
        return NUL in request.COOKIES.get(settings.SESSION_COOKIE_NAME, "")

    @staticmethod
    def bad_request(request):
        handler = get_resolver(get_urlconf()).resolve_error_handler(400)
        return handler(request, exception=BadRequest("a NUL byte in the request"))
