from __future__ import annotations

import pytest
from django.contrib.auth.models import Permission

from accounts import roles
from cms.models import PublicationStatus
from core import clock
from living.models import LegalReviewStatus, LivingSheet, LivingTopic
from living.seeds import seed_topics

# Shared project fixtures (tests/conftest.py is not an ancestor of this directory, so re-export them).
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
def topics(db):
    seed_topics()
    return list(LivingTopic.objects.all())


@pytest.fixture
def topic(topics):
    return LivingTopic.objects.get(slug="logement")


@pytest.fixture
def reviewer(user_factory):  # noqa: F811
    return user_factory("reviewer@example.test", role=roles.STAFF, is_staff=True)


@pytest.fixture
def sheet_factory(db, topic, reviewer):
    counter = {"n": 0}

    def _make(
        title: str = "Fiche de test",
        *,
        status: str = PublicationStatus.PUBLISHED,
        reviewed: bool = True,
        slug: str | None = None,
        **extra,
    ) -> LivingSheet:
        counter["n"] += 1
        defaults = {
            "topic": extra.pop("topic", topic),
            "slug": slug or f"fiche-{counter['n']}",
            "title_fr": title,
            "summary_fr": extra.pop("summary_fr", "Résumé de la fiche."),
            "body_fr": extra.pop("body_fr", "Paragraphe.\n\n## Section\n\n- a\n- b"),
            "status": status,
        }
        if reviewed:
            defaults.update(legal_review=LegalReviewStatus.REVIEWED, reviewer=reviewer, last_reviewed_at=clock.now())
        if status == PublicationStatus.PUBLISHED:
            defaults.setdefault("published_at", clock.now())
        defaults.update(extra)
        return LivingSheet.objects.create(**defaults)

    return _make


@pytest.fixture
def publisher_user(user_factory):  # noqa: F811
    user = user_factory("living-publisher@example.test", role=roles.STAFF, is_staff=True)
    perm = Permission.objects.get(content_type__app_label="living", codename="publish_livingsheet")
    user.user_permissions.add(perm)
    return user
