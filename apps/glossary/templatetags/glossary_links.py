"""
Contextual glossary links for other content (pathways, living, FAQ, …).

Usage::

    {% load glossary_links %}
    … le {% glossary_link "codice_fiscale" %} est nécessaire …
    … votre {% glossary_link "permesso_di_soggiorno" "titre de séjour" %} …

* First argument: the term ``key`` (slug of the permalink, e.g. ``codice_fiscale``; the ten
  prescribed keys are listed in ``glossary.registry.keys()``).
* Optional second argument: a custom label. Without it the Italian term is printed with
  ``lang="it"``; with it the label is printed in the page language (no ``lang`` attribute).
* Output: ``<a class="glossary-link" href="/<lang>/glossaire/<key>/" title="<short definition>"
  data-glossary-key="<key>">…</a>``. The ``title`` carries the short definition (abbr-like).
* Safety: while gate G3 (Phase 3) is closed, or when the term is not live, the tag prints the
  plain label (no dead link, no 404). Unknown keys print the label or the humanised key.
"""

from __future__ import annotations

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape, format_html

from glossary import services

register = template.Library()


@register.simple_tag
def glossary_link(key: str, label: str = ""):
    key = (key or "").strip()
    target = services.link_target(key) if key else None
    if target is None:
        return escape(label or key.replace("_", " "))
    try:
        url = reverse("glossary:term", kwargs={"slug": key})
    except NoReverseMatch:  # pragma: no cover - the glossary URLconf is always mounted
        return escape(label or target.term)
    if label:
        return format_html(
            '<a class="glossary-link" href="{}" title="{}" data-glossary-key="{}">{}</a>',
            url,
            target.short_definition,
            key,
            label,
        )
    return format_html(
        '<a class="glossary-link" href="{}" title="{}" data-glossary-key="{}" lang="it">{}</a>',
        url,
        target.short_definition,
        key,
        target.term,
    )


@register.simple_tag
def glossary_term_url(key: str) -> str:
    """Permalink of a live term, or "" when not publicly reachable (for custom markup)."""
    key = (key or "").strip()
    if not key or services.link_target(key) is None:
        return ""
    try:
        return reverse("glossary:term", kwargs={"slug": key})
    except NoReverseMatch:  # pragma: no cover
        return ""
