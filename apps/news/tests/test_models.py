import datetime as dt

import pytest
from django.db import IntegrityError
from django.utils import translation
from freezegun import freeze_time

from cms.models import PublicationStatus, TranslationStatus
from news.models import Article, ArticleTranslation, NewsCategory

pytestmark = pytest.mark.django_db


def test_category_name_falls_back_to_french(categories):
    cat = NewsCategory.objects.get(slug="echeances")
    assert cat.name("it") == "Scadenze", "the seed provides the four editorial labels (I18N-03)"
    cat.name_it = ""  # an editor-created category without an Italian label…
    assert cat.name("it") == "Échéances"  # …falls back to French
    with translation.override("it"):
        assert cat.name_is_fallback is True, "the template then marks it lang=fr"
    cat.name_it = "Scadenze"
    with translation.override("it"):
        assert cat.name() == "Scadenze"
        assert cat.name_is_fallback is False
    with translation.override("fr"):
        assert cat.name_is_fallback is False
    assert cat.get_absolute_url().endswith("?categorie=echeances")


def test_live_queryset_respects_status_and_schedule(article_factory):
    with freeze_time("2026-10-05 10:00:00"):
        now = dt.datetime(2026, 10, 5, 10, 0, tzinfo=dt.UTC)
        published = article_factory("Publié", slug="pub")
        draft = article_factory("Brouillon", slug="draft", status=PublicationStatus.DRAFT)
        review = article_factory("Revue", slug="rev", status=PublicationStatus.REVIEW)
        archived = article_factory("Archivé", slug="arch", status=PublicationStatus.ARCHIVED)
        scheduled_future = article_factory(
            "Futur", slug="future", status=PublicationStatus.SCHEDULED, publish_at=now + dt.timedelta(days=2)
        )
        scheduled_past = article_factory(
            "Programmé passé", slug="past", status=PublicationStatus.SCHEDULED, publish_at=now - dt.timedelta(hours=1)
        )
        expired = article_factory("Expiré", slug="expired", unpublish_at=now - dt.timedelta(minutes=1))
        live = set(Article.objects.live().values_list("slug", flat=True))
        assert live == {"pub", "past"}
        assert published.is_live() and scheduled_past.is_live()
        assert not any(a.is_live() for a in (draft, review, archived, scheduled_future, expired))

    with freeze_time("2026-10-08 10:00:00"):
        assert Article.objects.live().filter(slug="future").exists(), "scheduled article goes live at publish_at"


def test_public_ordering_by_publication_date(article_factory):
    base = dt.datetime(2026, 10, 1, 12, 0, tzinfo=dt.UTC)
    older = article_factory("Ancien", slug="old", published_at=base)
    newer = article_factory("Récent", slug="new", published_at=base + dt.timedelta(days=1))
    scheduled = article_factory(
        "Programmé", slug="sched", status=PublicationStatus.SCHEDULED, publish_at=base + dt.timedelta(days=2)
    )
    with freeze_time("2026-10-10 10:00:00"):
        slugs = list(Article.objects.public().values_list("slug", flat=True))
    assert slugs == [scheduled.slug, newer.slug, older.slug]


def test_version_increments_and_published_at_is_set(article_factory):
    article = article_factory("V", slug="v", status=PublicationStatus.DRAFT)
    assert article.version == 1 and article.published_at is None
    article.status = PublicationStatus.PUBLISHED
    article.save()
    assert article.version == 2
    assert article.published_at is not None
    assert article.date_published == article.published_at
    assert article.date_modified == article.published_at
    article.last_updated = article.published_at + dt.timedelta(days=3)
    assert article.date_modified == article.last_updated


def test_texts_use_only_published_translations(article_factory):
    article = article_factory("Titre FR", slug="t")
    ArticleTranslation.objects.create(master=article, language="it", title="Titolo IT", status=TranslationStatus.DRAFT)
    it = article.texts("it")
    assert it.title == "Titre FR" and it.language == "fr" and it.is_fallback is True
    ArticleTranslation.objects.filter(master=article, language="it").update(status=TranslationStatus.PUBLISHED)
    article = Article.objects.get(pk=article.pk)
    it = article.texts("it")
    assert it.title == "Titolo IT" and it.language == "it" and it.is_fallback is False
    assert it.summary == article.summary_fr, "missing translated summary falls back to the French one"
    fr = article.texts("fr")
    assert fr.title == "Titre FR" and fr.is_fallback is False
    assert fr.seo_title == "Titre FR" and fr.seo_description == article.summary_fr


def test_translation_unique_per_language(article_factory):
    article = article_factory("U", slug="u")
    ArticleTranslation.objects.create(master=article, language="en", title="One")
    with pytest.raises(IntegrityError):
        ArticleTranslation.objects.create(master=article, language="en", title="Two")


def test_slug_unique(article_factory):
    article_factory("A", slug="same")
    with pytest.raises(IntegrityError):
        article_factory("B", slug="same")


def test_source_links_validator(article_factory):
    from django.core.exceptions import ValidationError

    article = article_factory(
        "S", slug="s", source_links=[{"label": "Normattiva", "url": "https://www.normattiva.it/"}]
    )
    article.full_clean()
    article.source_links = [{"label": "x", "url": "javascript:alert(1)"}]
    with pytest.raises(ValidationError):
        article.full_clean()
