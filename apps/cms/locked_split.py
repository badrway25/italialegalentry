"""
Locked copy, re-composed at render — never reworded (design V5.22, SECTION_SYSTEM_V2 §1 rule 6, §2.0 «Data»; lane S).

A V2 section may set a prescribed text in several typographic levels — a sentence larger, a keyword at display size, the
items of an enumeration on their seats — but the text itself never changes: the parts are cut on the text's OWN
separators and rebuild it character for character, or the cut does not happen and the caller renders the text whole.

    sentences(text)          after each «. », «? », «! » (the full stop stays with its sentence)
    split(text, on)          on «:» (the head keeps its colon), «;», «→» or «,» (the separator stays with the part
                             before)
    first_clause(text)       the text up to and including its first comma, then the rest
    spans(parts, …)          the parts as <span>s, escaped — nothing added between them, so textContent == the source

The filters of ``cms.templatetags.locked_split`` (``locked_spans``, ``emphasize``) call these; every cut used by a page
carries an equality test (apps/cms/tests/test_locked_split.py). A cut never retypes six words of a locked text: it only
slices the string the registry (cms.locked_content) returns.
"""

from __future__ import annotations

import re

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

#: the separators a cut may use, each kept with the part it closes
SEPARATORS = {":": ": ", ";": "; ", "→": "→", ",": ", "}
#: the same separators as Arabic writes them (V5.27, lane AR): a provisional Arabic rendering of a prescribed
#: enumeration carries «؛ » and «، », and the Forum's stations and ring cut it as they cut the French — a cut by ";" or
#: "," tries the Latin mark first, then the Arabic one; the part keeps whichever mark it closes with
ARABIC_SEPARATORS = {";": "؛ ", ",": "، "}
_SENTENCE_END = re.compile(r"(?<=[.?!…])(?: ?[»”])?\s+(?=\S)")


def _checked(text: str, parts: list[str]) -> tuple[str, ...] | None:
    parts = [p for p in parts if p]
    if len(parts) < 2 or "".join(parts) != text:
        return None
    return tuple(parts)


def sentences(text: str) -> tuple[str, ...] | None:
    """The text's sentences, each with its own closing punctuation and the space after it; None for one sentence."""
    text = str(text or "")
    parts: list[str] = []
    start = 0
    for match in _SENTENCE_END.finditer(text):
        parts.append(text[start : match.end()])
        start = match.end()
    parts.append(text[start:])
    return _checked(text, parts)


def split(text: str, on: str) -> tuple[str, ...] | None:
    """The text cut after each ``on`` separator («:», «;», «→», «,»), the separator kept with the part before it."""
    text = str(text or "")
    if on not in SEPARATORS:
        raise ValueError(f"no separator {on!r}: one of {sorted(SEPARATORS)}")
    mark = SEPARATORS[on]
    if mark not in text and on in ARABIC_SEPARATORS and ARABIC_SEPARATORS[on] in text:
        mark = ARABIC_SEPARATORS[on]
    pieces = text.split(mark)
    parts = [piece + mark for piece in pieces[:-1]] + [pieces[-1]]
    return _checked(text, parts)


def first_clause(text: str) -> tuple[str, str] | None:
    """The text up to and including its first «, », then the rest; None without a comma."""
    text = str(text or "")
    head, comma, rest = text.partition(", ")
    if not comma or not rest:
        return None
    parts = _checked(text, [head + comma, rest])
    return (parts[0], parts[1]) if parts else None


def keyword(text: str, most: int = 3) -> tuple[str, str] | None:
    """The text's first sentence when it is a keyword (at most ``most`` words — the answer's «Non.»), then the rest;
    None otherwise: a long first sentence is never set at the keyword's size."""
    parts = sentences(text)
    if not parts or len(parts[0].split()) > most:
        return None
    return (parts[0], "".join(parts[1:]))


def cut(text: str, mode: str) -> tuple[str, ...] | None:
    """One of the cuts by name: ``sentence``, ``keyword``, ``clause``, or a separator (``:``, ``;``, ``→``, ``,``)."""
    if mode == "keyword":
        return keyword(text)
    if mode == "sentence":
        return sentences(text)
    if mode == "clause":
        return first_clause(text)
    return split(text, mode)


def spans(parts: tuple[str, ...], css: str = "ls") -> SafeString:
    """The parts as numbered spans (``ls ls-1`` …), escaped; nothing between them, so the textContent is the source."""
    return mark_safe(  # noqa: S308 — every part is escaped here
        "".join(f'<span class="{css} {css}-{i}">{escape(part)}</span>' for i, part in enumerate(parts, 1))
    )


def emphasize(text: str, needles: list[str], css: str = "em-keyword", *, ltr: bool = False) -> SafeString:
    """The text with each exact substring of ``needles`` (first occurrence) wrapped in a span — emphasis only, never a
    change of words: a needle that is not in the text is ignored, and the textContent stays the source.

    ``ltr`` (the owner's FINAL CLOSURE PASS of 12 Nov 2026): the wrapper is ``<bdi dir="ltr">`` instead — a Latin
    proper name inside a right-to-left text («المشروع التجريبي Vénétie–Maroc») isolated as ONE left-to-right unit, so
    its dash is never reordered and the Arabic around it keeps its own direction; the bytes are the text's. No
    ``lang`` on it: a heading whose only element child carries a Latin ``lang`` turns left to right as a whole
    (v5/base.css's prescribed-French rule), and the name is a name — Readex Pro draws no Latin, so its letters are
    Host Grotesk's either way."""
    text = str(text or "")
    opening, closing = (f'<bdi class="{css}" dir="ltr">', "</bdi>") if ltr else (f'<span class="{css}">', "</span>")
    spots: list[tuple[int, int]] = []
    for needle in needles:
        if not needle:
            continue
        at = text.find(needle)
        if at < 0 or any(not (at + len(needle) <= s or at >= e) for s, e in spots):
            continue
        spots.append((at, at + len(needle)))
    out, last = [], 0
    for start, end in sorted(spots):
        out.append(escape(text[last:start]))
        out.append(f"{opening}{escape(text[start:end])}{closing}")
        last = end
    out.append(escape(text[last:]))
    return mark_safe("".join(out))  # noqa: S308 — every slice is escaped here
