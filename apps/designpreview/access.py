"""
Who the preview answers — the one gate shared by every preview route, the persona switch and the
frame middleware (V5.4 plan §4.4). DEVELOPMENT ONLY.

A request is the preview's only when all of these hold:

* ``settings.DEBUG`` and ``settings.ILE_DESIGN_PREVIEW`` (the flag ``config/settings/dev.py`` reads
  from the environment, ``ILE_DESIGN_PREVIEW=1``);
* the caller is the loopback interface (``REMOTE_ADDR``) **and no proxy header is present**. A local
  tunnel, a port-forward or a reverse proxy connects from loopback too: what gives it away is the
  header it adds — ``X-Forwarded-For``, ``Forwarded``, ``X-Real-IP``, ``X-Forwarded-Host``,
  ``CF-Connecting-IP`` (the plan's five) and the others tunnels are known to add. Present at all,
  even empty, it refuses the request;
* the ``Host`` header is ``127.0.0.1:<port>`` or ``localhost:<port>``, for this process's own port
  (``ILE_DESIGN_PREVIEW_PORT``: 8780 for the owner's server, the lane's for a lane). A page that
  rebinds its own name to 127.0.0.1, or a forward from another port, names another host.

Everything else is answered 404 by the views — the preview is not there — and is never relaxed by
the frame middleware. A 404, never a 403: a caller who may not see something is told nothing
(docs/SECURITY.md).
"""

from __future__ import annotations

from django.conf import settings

#: The loopback interface as ``REMOTE_ADDR`` names it.
LOOPBACK = frozenset({"127.0.0.1", "::1", "localhost"})

#: The headers a proxy, a tunnel or a port-forward adds, as WSGI names them. The first five are the
#: plan's (§4.4); the rest are what ngrok, Cloudflare Tunnel, VS Code's forwarded ports, Fastly,
#: Akamai and the common reverse proxies add as well. One of them, present at all, refuses.
PROXY_HEADERS = (
    "HTTP_X_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED_HOST",
    "HTTP_CF_CONNECTING_IP",
    "HTTP_X_FORWARDED_PROTO",
    "HTTP_X_FORWARDED_PORT",
    "HTTP_X_FORWARDED_SERVER",
    "HTTP_X_ORIGINAL_FORWARDED_FOR",
    "HTTP_VIA",
    "HTTP_TRUE_CLIENT_IP",
    "HTTP_X_CLIENT_IP",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FASTLY_CLIENT_IP",
    "HTTP_CF_RAY",
    "HTTP_CDN_LOOP",
)

#: The owner's preview server (plan §2.8). A lane sets its own in the environment.
DEFAULT_PORT = 8780


def enabled() -> bool:
    """DEBUG and the flag: the preview exists in this process."""
    return bool(settings.DEBUG and getattr(settings, "ILE_DESIGN_PREVIEW", False))


def own_port() -> int:
    return int(getattr(settings, "ILE_DESIGN_PREVIEW_PORT", DEFAULT_PORT))


def own_hosts() -> frozenset[str]:
    """The two ``Host`` values this process answers to."""
    port = own_port()
    return frozenset({f"127.0.0.1:{port}", f"localhost:{port}"})


def proxied(request) -> bool:
    return any(name in request.META for name in PROXY_HEADERS)


def loopback(request) -> bool:
    return request.META.get("REMOTE_ADDR", "") in LOOPBACK


def allowed(request) -> bool:
    """Every condition of the module docstring, in one place."""
    return enabled() and loopback(request) and not proxied(request) and request.META.get("HTTP_HOST", "") in own_hosts()


def loggable(value) -> str:
    """
    A value a request chose, fit for one log line: at most 200 characters, every control character
    escaped — a path holding ``%0a`` cannot write a second line that looks like the preview's own
    (Django escapes its request log the same way since CVE-2025-48432). Every line the preview logs
    passes what a request chose through here: the read-only refusal's (designpreview.personas) and
    the ceiling's 503 (designpreview.middleware) — review W1-P, security m2 and m7; CD condition C6.
    """
    return str(value)[:200].encode("unicode_escape").decode("ascii")
