"""
Gate-aware internal links — one rule for the whole site: never link to a page that answers 404.

``public_url(name, **kwargs)`` reverses a URL name and returns ``""`` when

* the name does not resolve (a sibling app is absent), or
* the resulting path is registered in ``core.public_routes`` behind a gate that is currently closed
  (Phase 3 pages before 2 October 2026, the Virtual Forum before its launch, …).

Templates use it through ``{% safe_url %}``; Python code calls it directly. Found by browser QA: the
collaboration forms linked back to ``/institutions/`` while that Phase 3 page was still gated.
"""

from __future__ import annotations

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from core import flags, gates
from core.public_routes import all_routes

_GATES = {
    "phase3_public": gates.phase3_public,
    "virtual_forum": gates.virtual_forum_enabled,
    "forum_permanent_mode": gates.forum_permanent_mode,
    "forum_banner": gates.forum_banner_visible,
    "newsletter": gates.newsletter_enabled,
    "legal_pages": gates.legal_pages_available,
    "public_forms": lambda: gates.public_forms_enabled().open,
}


def gate_is_open(name: str) -> bool:
    """True for an empty name; named gates use core.gates; anything else is a feature-flag key."""
    if not name:
        return True
    func = _GATES.get(name)
    return bool(func()) if func else flags.is_enabled(name)


def _relative(path: str) -> str:
    """'/fr/parcours/x/' → 'parcours/x/' (language prefix removed); other paths unchanged."""
    parts = path.lstrip("/").split("/", 1)
    if parts and parts[0] in {code for code, _name in settings.LANGUAGES}:
        return parts[1] if len(parts) > 1 else ""
    return path.lstrip("/")


def path_is_open(path: str) -> bool:
    relative = _relative(path.split("?")[0].split("#")[0])
    for route in all_routes():
        if route.requires_gate and route.path == relative:
            return gate_is_open(route.requires_gate)
    return True


def public_url(name: str, *args, **kwargs) -> str:
    if not name:
        return ""
    try:
        url = reverse(name, args=args or None, kwargs=kwargs or None)
    except NoReverseMatch:
        return ""
    return url if path_is_open(url) else ""
