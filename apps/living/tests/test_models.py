import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import translation
from freezegun import freeze_time

from cms.models import PublicationStatus, TranslationStatus
from living.catalogue import INITIAL_TOPICS, TOPIC_SLUGS
from living.models import LegalReviewStatus, LivingSheet, LivingSheetTranslation, LivingTopic, LivingTopicTranslation
from living.seeds import seed_topics

pytestmark = pytest.mark.django_db


def test_seed_creates_ten_published_topics_idempotently(db):
    seed_topics()
    seed_topics()
    assert LivingTopic.objects.count() == 10
    assert list(LivingTopic.objects.values_list("slug", flat=True)) == list(TOPIC_SLUGS)
    assert LivingTopic.objects.filter(status=PublicationStatus.PUBLISHED).count() == 10
    assert LivingSheet.objects.count() == 0, "no sheet is seeded (CONTENT_PENDING_LEGAL_REVIEW)"
    names = {spec.name_fr for spec in INITIAL_TOPICS}
    assert {"Langue italienne", "Logement", "Santé", "Service sanitaire national (SSN)", "École"} <= names
    assert {
        "Éducation civique",
        "Droits et devoirs",
        "Sécurité au travail",
        "Fiscalité de base",
        "Services publics",
    } <= names


def test_seed_never_overwrites_editorial_changes(topics):
    topic = LivingTopic.objects.get(slug="sante")
    topic.name_fr = "Santé et bien-être"
    topic.order = 5
    topic.save()
    seed_topics()
    topic.refresh_from_db()
    assert topic.name_fr == "Santé et bien-être" and topic.order == 5


def test_topic_texts_translations(topic):
    fr = topic.texts("fr")
    assert fr.title == "Logement" and fr.is_fallback is False
    it = topic.texts("it")
    assert it.title == "Logement" and it.is_fallback is False, "seeded label is a UI string (gettext)"
    LivingTopicTranslation.objects.create(master=topic, language="it", name="Alloggio", status=TranslationStatus.DRAFT)
    assert topic.texts("it").title == "Logement", "draft translation never rendered"
    LivingTopicTranslation.objects.filter(master=topic).update(status=TranslationStatus.PUBLISHED)
    topic = LivingTopic.objects.get(pk=topic.pk)
    assert topic.texts("it").title == "Alloggio"
    topic.name_fr = "Habitat"
    assert topic.texts("en").title == "Habitat" and topic.texts("en").is_fallback is True
    with translation.override("ar"):
        assert topic.texts().language == "fr"


def test_sheet_cannot_be_published_without_legal_review_db_constraint(topic):
    with pytest.raises(IntegrityError), transaction.atomic():
        LivingSheet.objects.create(
            topic=topic,
            slug="x",
            title_fr="X",
            status=PublicationStatus.PUBLISHED,
            legal_review=LegalReviewStatus.PENDING,
        )
    with pytest.raises(IntegrityError), transaction.atomic():
        LivingSheet.objects.create(
            topic=topic,
            slug="y",
            title_fr="Y",
            status=PublicationStatus.SCHEDULED,
            publish_at=dt.datetime(2026, 11, 1, tzinfo=dt.UTC),
            legal_review=LegalReviewStatus.PENDING,
        )
    assert LivingSheet.objects.count() == 0


def test_sheet_clean_requires_review_metadata(topic, reviewer):
    sheet = LivingSheet(topic=topic, slug="c", title_fr="C", status=PublicationStatus.PUBLISHED)
    with pytest.raises(ValidationError) as exc:
        sheet.full_clean()
    assert "status" in exc.value.error_dict
    sheet.legal_review = LegalReviewStatus.REVIEWED
    with pytest.raises(ValidationError) as exc:
        sheet.full_clean()
    assert "last_reviewed_at" in exc.value.error_dict
    sheet.last_reviewed_at = dt.datetime(2026, 10, 1, tzinfo=dt.UTC)
    with pytest.raises(ValidationError) as exc:
        sheet.full_clean()
    assert "reviewer" in exc.value.error_dict
    sheet.reviewer = reviewer
    sheet.full_clean()


def test_sheet_slug_unique_per_topic(sheet_factory, topics):
    other = LivingTopic.objects.get(slug="sante")
    sheet_factory("A", slug="same")
    sheet_factory("B", slug="same", topic=other)
    with pytest.raises(IntegrityError):
        sheet_factory("C", slug="same")


def test_sheet_public_queryset_and_scheduling(sheet_factory):
    with freeze_time("2026-10-05 10:00:00"):
        now = dt.datetime(2026, 10, 5, 10, 0, tzinfo=dt.UTC)
        live = sheet_factory("Live", slug="live")
        sheet_factory("Draft", slug="draft", status=PublicationStatus.DRAFT)
        sheet_factory("Unreviewed", slug="unrev", status=PublicationStatus.DRAFT, reviewed=False)
        sheet_factory(
            "Future", slug="future", status=PublicationStatus.SCHEDULED, publish_at=now + dt.timedelta(days=1)
        )
        assert list(LivingSheet.objects.public()) == [live]
    with freeze_time("2026-10-07 10:00:00"):
        assert set(LivingSheet.objects.public().values_list("slug", flat=True)) == {"live", "future"}


def test_sheet_texts_and_urls(sheet_factory):
    sheet = sheet_factory("Titre fiche", slug="titre-fiche", summary_fr="")
    with translation.override("fr"):
        assert sheet.get_absolute_url() == "/fr/vivre-en-italie/logement/titre-fiche/"
    with translation.override("ar"):
        assert sheet.get_absolute_url() == "/ar/vivre-en-italie/logement/titre-fiche/"
    fr = sheet.texts("fr")
    assert fr.title == "Titre fiche" and fr.summary.startswith("Paragraphe.")
    LivingSheetTranslation.objects.create(
        master=sheet, language="en", title="Sheet title", status=TranslationStatus.PUBLISHED
    )
    sheet = LivingSheet.objects.get(pk=sheet.pk)
    en = sheet.texts("en")
    assert en.title == "Sheet title" and en.body == sheet.body_fr and en.is_fallback is False
    assert sheet.texts("ar").is_fallback is True
