"""
Read-only access to the prescribed FAQ entries (locked registry key ``p3.faq.items``).

This module never touches the ORM so that models, seeds, admin and services can all import it
without cycles. The nine entries are the *only* source of truth for locked FAQ texts (gate G0).
"""

from __future__ import annotations

from cms import locked_content

REGISTRY_KEY = "p3.faq.items"


def items(language: str = "fr") -> list[dict[str, str]]:
    """Prescribed entries in the prescribed order: ``[{key, question, answer}, ...]``."""
    value, _effective = locked_content.get(REGISTRY_KEY, language)
    return [dict(entry) for entry in value]


def keys() -> list[str]:
    return [entry["key"] for entry in items()]


def item(key: str) -> dict[str, str] | None:
    for entry in items():
        if entry["key"] == key:
            return entry
    return None
