"""
{% locked_pathway "salaried_work" as pw %} → {"key", "title", "description", "lang", "fallback"} from the
locked registry (``p3.persons.pathways``), or None for ``needs_individual_analysis``. The texts are
read from the registry at render time — never copied into the database.
"""

from __future__ import annotations

from django import template
from django.conf import settings
from django.utils import translation

from cms import locked_content

register = template.Library()


@register.simple_tag
def locked_pathway(key: str):
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    entries, effective = locked_content.get("p3.persons.pathways", lang)
    for entry in entries:
        if entry.get("key") == key:
            return {
                "key": key,
                "title": entry.get("title", ""),
                "description": entry.get("description", ""),
                "lang": effective,
                "fallback": effective != lang,
            }
    return None


@register.filter
def progress_class(value) -> str:
    """CSP-safe width class for the progress bar (multiples of 5)."""
    try:
        pct = int(value)
    except (TypeError, ValueError):
        pct = 0
    pct = max(0, min(100, int(round(pct / 5.0) * 5)))
    return f"wizard__progress-fill--{pct}"
