"""
Forum template tags — thin wrappers around the core ``{% locked %}`` tag that compose the key
from the edition's ``locked_key_prefix`` (``p2.forum`` for Rovigo). Nothing is copied by hand.

{% event_text event "who.title" "h2" "section__title" %}   → locked text (lang attr on fallback)
{% event_text event "what.body" as paragraphs %}          → list value
{% event_lang event "what.body" %}                        → effective language of the locked text
"""

from __future__ import annotations

from django import template
from django.conf import settings
from django.utils import translation

from cms import locked_content
from core.templatetags.ile_core import locked

register = template.Library()


def _key(event, suffix: str) -> str:
    prefix = getattr(event, "locked_key_prefix", None) or "p2.forum"
    return f"{prefix}.{suffix}"


@register.simple_tag(takes_context=True)
def event_text(context, event, suffix: str, tag: str = "", css_class: str = ""):
    try:
        return locked(context, _key(event, suffix), tag, css_class)
    except locked_content.LockedContentMissing:
        return ""


@register.simple_tag
def event_lang(event, suffix: str) -> str:
    lang = translation.get_language() or settings.LANGUAGE_CODE
    try:
        _value, effective = locked_content.get(_key(event, suffix), lang)
    except locked_content.LockedContentMissing:
        return lang
    return effective


@register.simple_tag
def event_is_fallback(event, suffix: str) -> bool:
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    return event_lang(event, suffix) != lang
