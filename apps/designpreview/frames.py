"""
The one exception to «nothing frames a real page» — for the preview's own frames. DEVELOPMENT ONLY.

Real pages say ``X-Frame-Options: DENY`` and ``frame-ancestors 'none'`` (config/settings/base.py),
and that stays true for every top-level navigation. The live V5 product at ``/__design-v5/`` is
the real home in one same-origin frame, and the index opens real pages in frames on demand: those
requests, and only those, may be framed by this origin (V5.4 plan §4.4, «Frames»).

``PreviewFrameMiddleware`` is installed by the preview block of ``config/settings/dev.py`` alone,
listed **after** ``csp.middleware.CSPMiddleware`` and
``django.middleware.clickjacking.XFrameOptionsMiddleware`` — so its response hook runs before
theirs. It uses the codebase's own pattern (``core.middleware.BackofficeCSPMiddleware``): it puts
``frame-ancestors 'self'`` in ``response._csp_replace``, which django-csp applies when it writes
the header, and sets ``X-Frame-Options: SAMEORIGIN``, which ``XFrameOptionsMiddleware`` keeps
because the header is already there. It adds ``Vary: Sec-Fetch-Dest, Sec-Fetch-Site`` to every
response whose policy those two headers decide.

It relaxes a response only when **all** hold:

* DEBUG and the flag; a loopback caller with no proxy header; this process's own ``Host``
  (``designpreview.access.allowed``);
* the method is one a frame navigates with: GET or HEAD for a link, POST for a form submitted
  inside the frame. The plan said «GET or HEAD»; DL54-17 (the council's security reviewer, review
  W1-P M1) relaxes a POST answer under exactly the same condition — without it every form of the
  product, the sign-in's error and the product's own sign-out left the owner a blank frame. The
  read-only rule of a persona session still refuses a persona's write before any view
  (designpreview.personas), and its refusal is what the frame then shows;
* ``Sec-Fetch-Dest: iframe`` and ``Sec-Fetch-Site: same-origin`` — the browser says the page is
  being loaded into a frame of a page of this very origin (web content cannot forge either);
* the path is not the back-office's and not the preview's own: ``/__design-v5/`` pages decide their
  own policy (the proof files say ``frame-ancestors 'self'`` themselves; the landing, the index and
  the archive are never framed).

A relaxed response also loses ``upgrade-insecure-requests``, and nothing else changes in its
policy. The preview is plain http on loopback: under that directive Chromium upgrades the frame's
redirect hops to https — the sign-in a reserved page sends a visitor to, the page a form answers
with — and then refuses them as another origin, so the frame stays blank (review W1-P B1). A frame
also inherits its parent's insecure-requests policy, so the landing and the index drop the
directive too (designpreview.views). Production never sees any of it: this module exists only
under DEBUG and the flag, and the global policy keeps the directive.

A top-level navigation, a cross-site or same-site frame, a PUT, a request through a tunnel: the
normal policy, unchanged.
"""

from __future__ import annotations

from django.utils.cache import patch_vary_headers

from designpreview import access

#: What the browser sends that this middleware reads — and so what every response it judges varies on.
VARY = ("Sec-Fetch-Dest", "Sec-Fetch-Site")
#: Paths this middleware never touches: the staff back-office, and the preview, whose views decide.
EXCLUDED_PREFIXES = ("/backoffice/", "/__design-v5/")
#: The methods a frame navigates with: a link (GET, HEAD), a form submitted inside it (POST, DL54-17).
FRAMED_METHODS = frozenset({"GET", "HEAD", "POST"})
#: Everything a relaxed policy changes, and nothing else: the tests compare the rest of it, byte for byte.
RELAXED = {"frame-ancestors": ("'self'",), "upgrade-insecure-requests": None}


def framed_by_this_origin(request) -> bool:
    """
    The browser loads this response into a frame of a page of this origin, for the preview's own
    caller, by a method a frame navigates with. The one predicate: the middleware relaxes on it and
    on nothing else, and so does the read-only refusal (designpreview.personas) — a persona's framed
    PUT, PATCH or DELETE keeps the normal policy (review W1-P, security m6; CD condition C5).
    """
    return (
        request.method in FRAMED_METHODS
        and access.allowed(request)
        and request.META.get("HTTP_SEC_FETCH_DEST") == "iframe"
        and request.META.get("HTTP_SEC_FETCH_SITE") == "same-origin"
    )


def relax(response) -> None:
    """
    ``frame-ancestors 'self'`` and no ``upgrade-insecure-requests`` (merged into whatever
    ``_csp_replace`` the view set — django-csp omits a directive replaced by ``None``), and
    ``X-Frame-Options: SAMEORIGIN``.
    """
    replace = dict(getattr(response, "_csp_replace", None) or {})
    replace.update(RELAXED)
    response._csp_replace = replace
    response["X-Frame-Options"] = "SAMEORIGIN"


class PreviewFrameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if access.enabled() and not request.path_info.startswith(EXCLUDED_PREFIXES):
            patch_vary_headers(response, VARY)
            if framed_by_this_origin(request):
                relax(response)
        return response
