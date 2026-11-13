"""Shared helpers for the ecosystem test-suite (fixtures from tests/conftest.py are reused)."""

from __future__ import annotations

import pytest
from django.conf import settings
from django.utils import translation

from tests.conftest import (  # noqa: F401 — shared project fixtures (tests/conftest.py)
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

LANGS = [code for code, _name in settings.LANGUAGES]

COMPANIES_PATH = "entreprises/"
GATED_PATHS = {
    "institutions": "institutions/",
    "universities": "universites-et-formation/",
    "pilot": "projet-pilote/",
}


@pytest.fixture(autouse=True)
def _french_by_default():
    """A request to /ar/ leaves Arabic active in the thread: every test starts from the source language."""
    with translation.override("fr"):
        yield


@pytest.fixture
def get_html(client):
    def _get(lang: str, path: str, expected: int = 200, **params) -> str:
        response = client.get(f"/{lang}/{path}", params or None)
        assert response.status_code == expected, (lang, path, response.status_code)
        return response.content.decode("utf-8")

    return _get


@pytest.fixture
def curated_photo(db):
    """
    Give every seeded media asset its caption apparatus.

    ``ecosystem.services.photo_for`` refuses an asset that cannot fill place, date, a factual
    sentence and a credit (art direction A §6.2), so a test about anything OTHER than that refusal
    — SEO metadata, a preview, a layout — has to start from a publishable library. The rule itself
    is covered by tests/compliance/test_figure_caption.py.
    """
    import datetime as dt

    from cms.models import MediaAsset

    MediaAsset.objects.filter(is_decorative=False).update(
        caption_place="Rovigo",
        caption_date=dt.date(2026, 10, 2),
        caption_fr="Séance de travail.",
        credit="AGAMI",
    )
