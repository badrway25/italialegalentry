"""
Legacy URL handling for the migration from the WordPress site (docs/URL_MIGRATION_MAP.md).

* ``/?lang=xx`` (old client-side language switch)      → 301 ``/xx/``
* WordPress sitemaps                                   → 301 ``/sitemap.xml``
* WordPress endpoints, default post, author page, feed → 410 Gone (never redirected: the author
  page and the API have no public equivalent)
* anything else that ends in a 404                     → ``cms.Redirect`` rows (back-office editable)

The middleware never touches a request that resolves normally, so it cannot shadow a real page.
"""

from __future__ import annotations

import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render

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

        candidates = {path, path.rstrip("/") or "/", path if path.endswith("/") else path + "/"}
        row = Redirect.objects.filter(old_path__in=candidates).first()
        if row is None or not row.new_path.startswith("/") or row.new_path.startswith("//"):
            return None  # only same-site targets: no open redirect through the back-office table
        cls = HttpResponsePermanentRedirect if row.permanent else HttpResponseRedirect
        return cls(row.new_path)
