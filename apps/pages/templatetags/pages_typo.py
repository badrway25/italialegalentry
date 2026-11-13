"""
French spacing for TEAM-AUTHORED strings — ``{{ text|typo }}`` (design V5.4, plan §1.1 «French spacing — never
inside locked copy»; W2-D step 3 «the home around the hero»).

French sets a space beside its high punctuation: before ``: ; ! ? »`` and after ``«``. Written as an ordinary
space it is a place to break, and a line starts with « : la séquence… » or ends on an opening guillemet — both were
on the home at phone widths. The filter writes that space as a NO-BREAK SPACE, U+00A0 (Host Grotesk carries no
U+202F), and changes nothing else: no word, no other space, no hyphen.

It is OPT-IN and for team-authored strings only — the catalogue's interface strings and the editorial columns of
the back office (``pages.services.editorial``). A prescribed text never passes through it: a no-break space changes
the characters of a locked string, which tests/i18n/test_locked_texts.py compares exactly, and drawing locked
French with no-break spaces is the owner's and counsel's decision (plan §1.19, B1 item 8). The rule is held twice:
the templates apply the filter to editorial variables only, and the filter itself returns untouched any string
that is a prescribed text or carries a six-word run of one (``pages.prescribed``) — a locked value handed to it
by mistake stays byte for byte what the registry holds.

The other languages are safe to pass through: Italian and English set no space before their punctuation, and
Arabic's own marks («؟», «؛») are not matched.
"""

from __future__ import annotations

import re
from functools import lru_cache

from django import template
from django.utils.safestring import SafeData, mark_safe

from cms import locked_content
from pages import prescribed

register = template.Library()

NBSP = "\u00a0"  # written as an escape: a literal no-break space is invisible in a source file
_BEFORE_HIGH_PUNCTUATION = re.compile(r" (?=[:;!?»])")
_AFTER_OPENING_GUILLEMET = re.compile(r"(?<=«) ")


@lru_cache(maxsize=1)
def _locked_strings() -> frozenset[str]:
    """Every string of the registry, whatever its length — the short labels included, which carry no six-word run."""
    found: set[str] = set()

    def walk(value) -> None:
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    for table in locked_content.LOCKED_TEXTS.values():
        walk(table)
    return frozenset(found)


def is_prescribed(text: str) -> bool:
    return text in _locked_strings() or prescribed.any_phase(text)


@register.filter(name="typo")
def typo(value) -> str:
    """The value as a string, with no-break spaces beside French high punctuation; a prescribed text is returned
    as it is. A plain string stays plain (the template escapes it as it would have escaped the value), a safe one
    stays safe."""
    text = "" if value is None else str(value)
    if " " not in text or is_prescribed(text):
        return value if isinstance(value, SafeData) else text
    spaced = _AFTER_OPENING_GUILLEMET.sub(NBSP, _BEFORE_HIGH_PUNCTUATION.sub(NBSP, text))
    return mark_safe(spaced) if isinstance(value, SafeData) else spaced  # noqa: S308 - safe in, safe out: no markup added
