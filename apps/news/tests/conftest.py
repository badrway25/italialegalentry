from __future__ import annotations

import time

import pytest
from django.contrib.auth.models import Permission

from accounts import roles
from cms.models import PublicationStatus
from core import clock
from news.models import Article, NewsCategory
from news.seeds import seed_categories

# Shared project fixtures (tests/conftest.py) re-exported for this app's test package.
from tests.conftest import (  # noqa: F401
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


@pytest.fixture
def categories(db):
    seed_categories()
    return list(NewsCategory.objects.all())


@pytest.fixture
def category(categories):
    return NewsCategory.objects.get(slug="normativa")


@pytest.fixture
def article_factory(db, category):
    counter = {"n": 0}

    def _make(
        title: str = "Titre de test",
        *,
        status: str = PublicationStatus.PUBLISHED,
        slug: str | None = None,
        body: str = "Premier paragraphe.\n\n## Intertitre\n\nSecond paragraphe.\n\n- point un\n- point deux",
        **extra,
    ) -> Article:
        counter["n"] += 1
        slug = slug or f"article-{counter['n']}"
        defaults = {
            "slug": slug,
            "category": extra.pop("category", category),
            "title_fr": title,
            "summary_fr": extra.pop("summary_fr", "Résumé de l’article de test."),
            "body_fr": body,
            "status": status,
        }
        if status == PublicationStatus.PUBLISHED and "published_at" not in extra:
            defaults["published_at"] = clock.now()
        defaults.update(extra)
        return Article.objects.create(**defaults)

    return _make


@pytest.fixture
def publisher_user(user_factory):  # noqa: F811
    user = user_factory("publisher@example.test", role=roles.STAFF, is_staff=True)
    perm = Permission.objects.get(content_type__app_label="news", codename="publish_article")
    user.user_permissions.add(perm)
    return user


@pytest.fixture
def newsletter_on(set_flag):  # noqa: F811
    return set_flag("newsletter", True)


@pytest.fixture
def honeypot_ok():
    """POST data that passes the honeypot / timing check."""
    return {"website_url": "", "form_started_at": str(int(time.time()) - 30)}
