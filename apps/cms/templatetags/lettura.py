"""
The content pages' template tags (design V5.4, W3-F2 — «la lettura», static/css/v5/_lettura.css).

{% load lettura %}
{{ url|host }}                → the host an authority's link leads to, shown beside its name (plan §1.18 D26: «an
                                authority link's host made visible»): «https://www.salute.gov.it/…» → «salute.gov.it»;
                                "" for anything that is not an http(s) URL with a host, so a template shows nothing
                                rather than a guess.
{% locked_title "key" %}      → the page's h1 from a prescribed title of the registry, whole — `page-header__title`,
                                plus `page-header__title--caps` when the prescribed words are written in capitals (they
                                are tracked as every capital run is, TR rule 6). When the words are shown in another
                                language than the page's (the core `locked` tag's rule) they are a run of their own
                                inside the page's h1 — `<span dir lang>`: the run keeps its direction and its
                                punctuation (a French title on the Arabic page reads left to right), the h1 keeps the
                                page's, so the run starts on the page's reading edge (logical, nothing physical).
"""

from __future__ import annotations

from urllib.parse import urlsplit

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.html import format_html

from cms import locked_content

register = template.Library()


@register.filter
def host(url) -> str:
    try:
        parts = urlsplit(str(url or "").strip())
    except ValueError:
        return ""
    if parts.scheme not in ("http", "https") or not parts.hostname:
        return ""
    name = parts.hostname
    return name[4:] if name.startswith("www.") else name


@register.simple_tag
def locked_title(key: str, css_class: str = "page-header__title"):
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    value, effective = locked_content.get(key, lang)
    value = str(value)
    classes = css_class
    if value.upper() == value and any(ch.isalpha() and ch.upper() != ch.lower() for ch in value):
        classes += " page-header__title--caps"
    if effective != lang:
        direction = "rtl" if effective in settings.RTL_LANGUAGES else "ltr"
        run = format_html('<span dir="{}" lang="{}">{}</span>', direction, effective, value)
        return format_html('<h1 class="{}">{}</h1>', classes, run)
    return format_html('<h1 class="{}">{}</h1>', classes, value)
