"""
{% load forum_v2 %} — the Forum page's V2 compositions of its prescribed texts (design V5.22, SECTION_SYSTEM_V2 §3.16;
lane P2). Every text is the edition's locked one (``p2.forum.*``, the key composed as forum_tags does); it is cut at
render on its OWN separators and the parts rebuild it character for character, or the cut does not happen and the
caller renders it whole (cms.locked_split's rule). Nothing is retyped here.

{% forum_raw event "objectives.body" as text %}     the plain locked text and {% forum_raw_lang … %} its language
{{ text|forum_clauses }}                             the objectives: the clauses cut on the sentence's own « ; »
{{ text|forum_actors }}                              the audience: the actors of the enumeration cut on its own « , »
                                                     and on the last item's conjunction, each with its punctuation
"""

from __future__ import annotations

import re

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.html import conditional_escape, format_html

from cms import locked_content, locked_split
from core import icons

register = template.Library()

#: the conjunction that closes an enumeration, as the locked texts write it (French; the other languages' if they exist)
CONJUNCTIONS = (" et ", " e ", " and ")

#: FO2b: the actors of the prescribed audience sentence that name an ILE audience, by their place in the sentence — the
#: institutions, the companies, the universities, the training bodies — and the registry's concept of each (its T2a
#: disc's glyph is the registry's, apps/core/icons.py: AUDIENCE «institution», «company», «university»; ACTOR
#: «training_body» — never a literal in a register, the O14 lint)
AUDIENCE_CONCEPTS = {
    1: ("audience", "institution"),
    2: ("audience", "company"),
    5: ("audience", "university"),
    6: ("actor", "training_body"),
}
#: … and the audience whose accent rings each disc on the night (v5/_sezioni.css --aud)
AUDIENCE_OF = {1: "institution", 2: "company", 5: "university", 6: "university"}


def _key(event, suffix: str) -> str:
    prefix = getattr(event, "locked_key_prefix", None) or "p2.forum"
    return f"{prefix}.{suffix}"


def _lang() -> str:
    return translation.get_language() or settings.LANGUAGE_CODE


@register.simple_tag
def forum_raw(event, suffix: str) -> str:
    """The locked text itself (a plain string), unrendered — the filters below cut it."""
    try:
        value, _effective = locked_content.get(_key(event, suffix), _lang())
    except locked_content.LockedContentMissing:
        return ""
    return value if isinstance(value, str) else ""


@register.simple_tag
def forum_raw_lang(event, suffix: str) -> str:
    """The ``lang`` attribute the text needs on this page: its effective language when it is not the page's."""
    try:
        _value, effective = locked_content.get(_key(event, suffix), _lang())
    except locked_content.LockedContentMissing:
        return ""
    return effective if effective != _lang().split("-")[0] else ""


@register.simple_tag
def forum_mark() -> str:
    """The Forum's ILE mark (icons.MARKS["forum"]): the objectives' arrival carries it, the ring's hub its seal."""
    return icons.MARKS["forum"].id


@register.filter
def forum_clauses(text) -> list[str]:
    """The sentence's clauses, each with its own « ; » (and the final full stop with the last), or [] (render whole)."""
    parts = locked_split.split(str(text or ""), ";")
    return list(parts) if parts else []


#: a clause's last word with what follows it (its spaces and its punctuation): they never part at a line's end
_TAIL = re.compile(r"(?s)^(.*?)(\S+\s*[;:!?.,]?\s*)$")


@register.filter
def forum_coda(clause) -> str:
    """A clause with its last word and its punctuation held together (round 1, QA_ROUND1 m12: the first clause's « ; »
    wrapped alone onto a line at 1024): markup only — the text is the clause itself, character for character."""
    clause = str(clause or "")
    found = _TAIL.match(clause)
    if not found or not found.group(1):
        return conditional_escape(clause)
    head, tail = found.groups()
    return format_html('{}<span class="forum-obiettivi__coda">{}</span>', head, tail)


def actors(text: str) -> list[tuple[str, str]] | None:
    """An enumeration's actors as (words, punctuation) pairs — «, » after each, the closing conjunction and the final
    full stop kept — whose concatenation is the text itself; None when the cut does not rebuild it."""
    text = str(text or "")
    parts = locked_split.split(text, ",")
    if not parts:
        return None
    pieces: list[str] = list(parts[:-1])
    last = parts[-1]
    for conjunction in CONJUNCTIONS:
        head, found, tail = last.partition(conjunction)
        if found and head and tail:
            pieces += [head + conjunction, tail]
            break
    else:
        pieces.append(last)
    out: list[tuple[str, str]] = []
    for piece in pieces:
        words = piece.rstrip(" ,.;")
        for conjunction in CONJUNCTIONS:
            if piece.endswith(conjunction):
                words = piece[: -len(conjunction)]
                break
        out.append((words, piece[len(words) :]))
    if "".join(w + p for w, p in out) != text:
        return None
    return out


@register.filter
def forum_actors(text) -> list[dict]:
    """The audience's actors for the ring: [{"words", "punct", "n"}], or [] (render whole)."""
    found = actors(str(text or "")) or []
    return [
        {
            "words": w,
            "punct": p,
            "n": i,
            "glyph": icons.concept(*AUDIENCE_CONCEPTS[i]) if len(found) == 9 and i in AUDIENCE_CONCEPTS else "",
            "audience": AUDIENCE_OF.get(i, "") if len(found) == 9 else "",
        }
        for i, (w, p) in enumerate(found or [], 1)
    ]
