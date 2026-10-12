"""Local fixtures for the Espace Personnes test-suite (shared ones live in tests/conftest.py)."""

from __future__ import annotations

import re
from html import unescape

import pytest
from django.utils.html import escape

from cms import locked_content
from pathways.models import Pathway
from pathways.seeds import seed_pathways
from tests.conftest import (  # noqa: F401 — shared fixtures made visible to this app's tests
    _clear_caches,
    before_phase3,
    client_ar,
    client_fr,
    legal_published,
    person_user,
    phase3_open,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)

PATHWAY_URL = "/fr/parcours/"
DIPLOMAS_URL = "/fr/diplomes-et-titres/"
TRAINING_URL = "/fr/formation/"


@pytest.fixture
def pathways_seeded(db):
    """Run only the pathways seed (faster than the full ``seeded`` fixture)."""
    seed_pathways()
    return list(Pathway.objects.ordered())


def _iter_locked_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _iter_locked_strings(v)
    elif isinstance(value, list | tuple):
        for v in value:
            yield from _iter_locked_strings(v)


def strip_locked(html: str) -> str:
    """Remove every locked (prescribed) text from rendered HTML so only team-written text remains."""
    out = html
    for value in locked_content.LOCKED_TEXTS["fr"].values():
        for text in _iter_locked_strings(value):
            if len(text) < 12:
                continue
            out = out.replace(escape(text), " ").replace(text, " ")
    return out


def visible_text(html: str) -> str:
    """Rough text extraction (tags removed, entities decoded) for wording assertions."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return unescape(text)


@pytest.fixture
def strip_locked_fn():
    return strip_locked


@pytest.fixture
def visible_text_fn():
    return visible_text
