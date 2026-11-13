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
    """
    The family's prescribed title and description for the result page, each with the language it is shown in: V5.27
    (FINAL_DELIVERY_V2 R7′; lane AR) renders the title in provisional Arabic on /ar/ and keeps the description as the
    French source — hidden here, off its own sheet, behind the pointer line the registry's seam gives — so the two parts
    are read by their sub-keys (``p3.persons.pathways[<n>].title`` …), each carrying its own ``lang`` / ``fallback``.
    """
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    entries, _effective = locked_content.get("p3.persons.pathways", "fr")
    for index, entry in enumerate(entries):
        if entry.get("key") == key:
            title, title_lang = locked_content.get(f"p3.persons.pathways[{index}].title", lang)
            description, description_lang = locked_content.get(f"p3.persons.pathways[{index}].description", lang)
            return {
                "key": key,
                "title": title,
                "description": description,
                "lang": title_lang,
                "fallback": title_lang != lang,
                "description_lang": description_lang,
                "description_fallback": description_lang != lang,
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
