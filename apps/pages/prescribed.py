"""
Detection of prescribed wording inside *editorial* strings (back-office columns, translation rows).

Prescribed texts reach a page only through ``cms.locked_content``. An editorial column is free
text, so two risks remain and are closed here:

* a Phase 3 sentence pasted into a heading / intro / hero field would be public while gate G3 is
  closed — ``pages.services`` drops such a value at render time (``phase3_only``);
* any prescribed sentence hand-copied into a column escapes the checksum of the registry —
  ``HomeSection.clean()`` / ``HomeSectionTranslation.clean()`` refuse it (``any_phase``).

A "fragment" is a run of six consecutive words of a prescribed text: the same rule as the review
suite (``pages/tests/test_prescribed_fragments.py``). Shorter prescribed strings are plain labels
("Vivre en Italie", "Besoins des entreprises"…) and are deliberately not matched: refusing them
would only produce false positives. Import-only module: no ORM access.
"""

from __future__ import annotations

import re
from functools import lru_cache

from cms import locked_content

RUN = 6
_WORD = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*")

ALL_PREFIXES: tuple[str, ...] = ("p1.", "p2.", "p3.", "legal.")
PHASE3_PREFIXES: tuple[str, ...] = ("p3.",)
ALREADY_PUBLIC_PREFIXES: tuple[str, ...] = ("p1.", "p2.")


def words(text: str) -> tuple[str, ...]:
    return tuple(_WORD.findall((text or "").lower().replace("’", "'")))


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for name, item in value.items():
            if name != "key":  # technical identifiers are not prescribed wording
                yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _runs(prefixes: tuple[str, ...]) -> frozenset[tuple[str, ...]]:
    """Six-word runs of every prescribed text stored under ``prefixes``, in every registry language."""
    runs: set[tuple[str, ...]] = set()
    for table in locked_content.LOCKED_TEXTS.values():
        for key, value in table.items():
            if key.startswith(prefixes):
                for text in _strings(value):
                    tokens = words(text)
                    runs.update(tokens[i : i + RUN] for i in range(len(tokens) - RUN + 1))
    return frozenset(runs)


@lru_cache(maxsize=1)
def _any_phase_runs() -> frozenset[tuple[str, ...]]:
    return _runs(ALL_PREFIXES)


@lru_cache(maxsize=1)
def _phase3_only_runs() -> frozenset[tuple[str, ...]]:
    return _runs(PHASE3_PREFIXES) - _runs(ALREADY_PUBLIC_PREFIXES)


def _contains(value: str, runs: frozenset[tuple[str, ...]]) -> bool:
    tokens = words(value)
    return any(tokens[i : i + RUN] in runs for i in range(len(tokens) - RUN + 1))


def any_phase(value: str) -> bool:
    """True when ``value`` carries a fragment of any prescribed text (Phases 1–3 or legal)."""
    return _contains(value, _any_phase_runs())


def phase3_only(value: str) -> bool:
    """True when ``value`` carries a fragment that belongs to Phase 3 texts only (gate G3)."""
    return _contains(value, _phase3_only_runs())
