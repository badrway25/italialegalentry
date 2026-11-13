"""
Read-only access to the prescribed glossary terms (locked registry key ``p3.glossary.terms``).

No ORM access here so that models, seeds, admin, services and template tags can import it freely.
"""

from __future__ import annotations

from cms import locked_content

REGISTRY_KEY = "p3.glossary.terms"


def terms(language: str = "fr") -> list[dict[str, str]]:
    """Prescribed terms in the prescribed order: ``[{key, term, definition}, ...]``."""
    value, _effective = locked_content.get(REGISTRY_KEY, language)
    return [dict(entry) for entry in value]


def keys() -> list[str]:
    return [entry["key"] for entry in terms()]


def term(key: str) -> dict[str, str] | None:
    for entry in terms():
        if entry["key"] == key:
            return entry
    return None
