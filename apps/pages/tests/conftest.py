"""Fixtures of the pages test package (project-wide fixtures are re-exported from tests/conftest.py)."""

from __future__ import annotations

import re

import pytest

from cms import locked_content
from cms.models import PublicationStatus
from tests.conftest import *  # noqa: F401,F403
from tests.conftest import _clear_caches  # noqa: F401

LANGS = ("fr", "it", "en", "ar")

# Every string of the Phase 3 part of the registry that the homepage could render: none of them
# may appear while gate G3 is closed.
PHASE3_HOME_KEYS = (
    "p3.hero.subtitle",
    "p3.hero.body",
    "p3.entrances.person.title",
    "p3.entrances.person.text",
    "p3.entrances.person.button",
    "p3.entrances.company.title",
    "p3.entrances.company.text",
    "p3.entrances.institution.title",
    "p3.entrances.institution.text",
    "p3.entrances.university.title",
    "p3.entrances.university.text",
    "p3.entrances.university.button",
    "p3.persons.how_it_works",
    "p3.pilot.title",
    "p3.antifraud.title",
    "p3.antifraud.body",
    "p3.reserved.title",
    "p3.reserved.body",
)


def text_of(key: str) -> str:
    return locked_content.text(key, "fr")


@pytest.fixture
def page(client):
    """GET a path and return (response, decoded html)."""

    def _get(path: str, **extra):
        response = client.get(path, **extra)
        return response, response.content.decode("utf-8")

    return _get


def section_order(html: str) -> list[str]:
    return re.findall(r'data-section="([a-z]+)"', html)


def escaped(value: str) -> str:
    from django.utils.html import escape

    return str(escape(value))


@pytest.fixture
def article_factory(db):
    from news.models import Article, NewsCategory

    category, _created = NewsCategory.objects.get_or_create(slug="forum", defaults={"name_fr": "Forum", "order": 30})
    counter = {"n": 0}

    def _make(title: str, status: str = PublicationStatus.PUBLISHED, **extra):
        counter["n"] += 1
        defaults = {
            "slug": f"article-pages-{counter['n']}",
            "category": category,
            "title_fr": title,
            "summary_fr": f"Résumé de « {title} ».",
            "body_fr": "Premier paragraphe.",
            "status": status,
        }
        defaults.update(extra)
        return Article.objects.create(**defaults)

    return _make


@pytest.fixture
def partner_factory(db):
    from partners.models import Partner, PartnerKind

    def _make(name: str, authorized: bool = True, status: str = PublicationStatus.PUBLISHED):
        return Partner.objects.create(
            name=name,
            kind=PartnerKind.UNIVERSITY,
            authorized=authorized,
            authorization_reference="Autorisation écrite de test du 2026-09-01" if authorized else "",
            status=status,
        )

    return _make


@pytest.fixture
def curated_photo(db):
    """
    Give every seeded media asset its caption apparatus.

    ``pages.services.photo_from_asset`` refuses an asset that cannot fill place, date, a factual
    sentence and a credit (art direction A §6.2), so a test about the IMAGE PIPELINE or about SEO
    metadata has to start from a publishable library. The refusal itself is covered by
    tests/compliance/test_figure_caption.py.
    """
    import datetime as dt

    from cms.models import MediaAsset

    MediaAsset.objects.filter(is_decorative=False).update(
        caption_place="Rovigo",
        caption_date=dt.date(2026, 10, 2),
        caption_fr="Séance de travail.",
        credit="AGAMI",
    )
