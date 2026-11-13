"""
{% load locked_split %} — locked copy re-composed at render (design V5.22, SECTION_SYSTEM_V2 §2.0 «Data»; lane S).

{{ text|locked_spans:"sentence" }}   the text cut on its own separators (``sentence``, ``clause``, ``:``, ``;``, ``→``,
                                     ``,``) into numbered spans ``ls ls-1`` …; the text whole and escaped when the cut
                                     does not rebuild it character for character (cms.locked_split)
{{ text|emphasize:"a|b" }}           each exact substring wrapped in ``<span class="em-keyword">``; emphasis only — a
                                     substring that is absent is ignored, the textContent stays the source
{{ text|isolate_ltr:"a|b" }}         the same, as ``<bdi class="em-keyword" dir="ltr">``: a French name in an
                                     Arabic text, one left-to-right unit
{% locked_text "key" as text %}      the registry's plain text in the page's language (or its French source): the raw
                                     string the two filters cut — ``{% locked %}`` returns it rendered (escaped, and
                                     wrapped in its lang span on a fallback), which a cut must never slice
"""

from __future__ import annotations

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.html import escape
from django.utils.safestring import SafeString

from cms import locked_content, locked_split

register = template.Library()


@register.filter
def locked_spans(text, mode: str = "sentence") -> SafeString:
    parts = locked_split.cut(str(text or ""), str(mode))
    return locked_split.spans(parts) if parts else escape(str(text or ""))


@register.filter
def emphasize(text, needles: str = "") -> SafeString:
    return locked_split.emphasize(str(text or ""), [n for n in str(needles or "").split("|") if n])


@register.filter
def isolate_ltr(text, needles: str = "") -> SafeString:
    """``emphasize``'s spans as ``<bdi dir="ltr">``: a French proper name inside a right-to-left text kept as one
    left-to-right unit (the owner's FINAL CLOSURE PASS of 12 Nov 2026); the textContent stays the source."""
    return locked_split.emphasize(str(text or ""), [n for n in str(needles or "").split("|") if n], ltr=True)


@register.simple_tag
def locked_text(key: str) -> str:
    """The locked text itself, unrendered: the caller sets its ``lang`` with ``{% locked_lang %}`` /
    ``{% locked_is_fallback %}`` and cuts it with ``locked_spans`` (which escapes every part)."""
    value, _effective = locked_content.get(key, translation.get_language() or settings.LANGUAGE_CODE)
    return value if isinstance(value, str) else ""
