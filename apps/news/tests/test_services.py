import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied
from freezegun import freeze_time

from audit.models import AuditEvent
from cms.models import PublicationStatus
from news import services

pytestmark = pytest.mark.django_db


def test_workflow_draft_review_published_archived(article_factory, publisher_user):
    article = article_factory("W", slug="w", status=PublicationStatus.DRAFT)
    services.submit_for_review(article, publisher_user)
    assert article.status == PublicationStatus.REVIEW
    services.publish(article, publisher_user)
    assert article.status == PublicationStatus.PUBLISHED
    assert article.published_at is not None
    assert article.reviewer == publisher_user and article.last_reviewed_at is not None
    assert article.editor == publisher_user
    services.archive(article, publisher_user)
    assert article.status == PublicationStatus.ARCHIVED
    actions = list(AuditEvent.objects.filter(target_type="Article").values_list("action", flat=True))
    assert {"news.article.submitted_for_review", "news.article.published", "news.article.archived"} <= set(actions)


def test_publish_requires_permission(article_factory, staff_user, publisher_user, superuser):
    article = article_factory("P", slug="p", status=PublicationStatus.REVIEW)
    assert services.can_publish(staff_user) is False
    with pytest.raises(PermissionDenied):
        services.publish(article, staff_user)
    article.refresh_from_db()
    assert article.status == PublicationStatus.REVIEW, "nothing changed"
    assert services.can_publish(publisher_user) is True
    assert services.can_publish(superuser) is True
    services.publish(article, superuser)
    assert article.status == PublicationStatus.PUBLISHED


def test_publish_from_draft_is_not_allowed(article_factory, publisher_user):
    article = article_factory("D", slug="d", status=PublicationStatus.DRAFT)
    with pytest.raises(services.WorkflowError):
        services.publish(article, publisher_user)
    with pytest.raises(services.WorkflowError):
        services.archive(article, publisher_user)


def test_publish_with_future_date_schedules(article_factory, publisher_user):
    with freeze_time("2026-10-05 10:00:00"):
        future = dt.datetime(2026, 10, 9, 8, 0, tzinfo=dt.UTC)
        article = article_factory("F", slug="f", status=PublicationStatus.REVIEW, publish_at=future)
        services.publish(article, publisher_user)
        assert article.status == PublicationStatus.SCHEDULED
        assert not article.is_live()
    with freeze_time("2026-10-09 09:00:00"):
        assert article.is_live()


def test_back_to_draft_and_republish_archived(article_factory, publisher_user):
    article = article_factory("B", slug="b", status=PublicationStatus.REVIEW)
    services.back_to_draft(article, publisher_user)
    assert article.status == PublicationStatus.DRAFT
    article.status = PublicationStatus.ARCHIVED
    article.save()
    services.publish(article, publisher_user)
    assert article.status == PublicationStatus.PUBLISHED


def test_related_and_latest(article_factory):
    a = article_factory("A", slug="a")
    b = article_factory("B", slug="b")
    c = article_factory("C", slug="c", status=PublicationStatus.DRAFT)
    a.related.add(b, c)
    assert list(services.related_articles(a)) == [b], "draft related articles are hidden"
    assert set(services.latest_articles()) == {a, b}
    assert services.category_by_slug("does-not-exist") is None
    assert services.category_by_slug("") is None


def test_jsonld_structure(article_factory, rf):
    article = article_factory("Titre JSON", slug="json", last_updated=dt.datetime(2026, 10, 6, tzinfo=dt.UTC))
    request = rf.get("/fr/actualites/json/")
    data = services.article_jsonld(article, request)
    assert '"@type": "Article"' in data
    assert '"headline": "Titre JSON"' in data
    assert "datePublished" in data and "dateModified" in data
    assert "AGAMI" in data
    assert "GovernmentOrganization" not in data
    assert "<" not in data and ">" not in data, "escaped for safe inline embedding"
