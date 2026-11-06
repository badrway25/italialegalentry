"""
The console foot's words (templates/portal/partials/console_foot.html; V5.12 §16, D-16): the promoter line every public
page carries, and the locked statement that Italy Legal Entry is not an authority.

That statement is the FIRST SENTENCE of the locked presentation of «Espace Personnes» (S1 §3.3, ``p3.persons.intro``):
«Italy Legal Entry ne délivre pas de visas, de permis de séjour ni d’autorisations : ces décisions relèvent
exclusivement des autorités compétentes.» It is cut from the locked text at its first full stop, never retyped and
never translated here: a language without an official locked version shows the French, marked ``lang="fr"``
(the locked-content fallback rule, apps/cms/locked_content.get).
"""

from __future__ import annotations

import re

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.html import format_html

from cms import locked_content

register = template.Library()

#: The end of a sentence: a full stop followed by a space and the next sentence's capital (or the end of the text).
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Þ؀-ۿ])")


def first_sentence(text: str) -> str:
    """The first sentence of ``text``, its words and its full stop unchanged."""
    return _SENTENCE_END.split(str(text).strip(), maxsplit=1)[0]


@register.simple_tag
def locked_sentence(key: str):
    """The first sentence of the locked text ``key``, in the page's language when the text has an official version,
    else in French inside ``<span lang="fr">``."""
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    value, effective = locked_content.get(key, lang)
    sentence = first_sentence(value)
    if effective != lang:
        return format_html('<span lang="{}" dir="ltr">{}</span>', effective, sentence)
    return sentence
