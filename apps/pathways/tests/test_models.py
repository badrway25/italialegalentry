import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import translation
from freezegun import freeze_time

from cms import locked_content
from cms.models import PublicationStatus, TranslationStatus
from pathways.models import (
    GENERIC_AUTHORITY_NAMES,
    PATHWAY_KEYS,
    Pathway,
    PathwayStep,
    PathwayTranslation,
    locked_pathway_entries,
    validate_authorities,
    validate_pathway_key,
)

pytestmark = pytest.mark.django_db

EXPECTED_ORDER = (
    "salaried_work",
    "skilled_work_eu_blue_card",
    "training_in_origin_country",
    "study_and_training_in_italy",
    "family_reunification",
    "self_employment_entrepreneurship",
    "scientific_research",
    "other_regular_routes",
)


def test_registry_exposes_eight_keys_in_prescribed_order():
    assert PATHWAY_KEYS == EXPECTED_ORDER
    entries = locked_pathway_entries()
    assert [e["key"] for e in entries] == list(EXPECTED_ORDER)
    assert entries[0]["title"] == "Travail salarié"
    assert entries[-1]["title"] == "Autres voies régulières"


def test_title_and_description_come_from_registry_not_db():
    p = Pathway.objects.create(key="family_reunification", order=5)
    entry = locked_content.get("p3.persons.pathways", "fr")[0][4]
    assert p.title == entry["title"] == "Regroupement familial"
    assert p.description == entry["description"]
    assert str(p) == "Regroupement familial"
    assert p.locked is True
    assert p.reviewed_by is None


def test_key_must_be_one_of_the_locked_keys():
    with pytest.raises(ValidationError):
        validate_pathway_key("tourism")
    p = Pathway(key="tourism", order=99)
    with pytest.raises(ValidationError):
        p.full_clean()


def test_order_is_unique():
    Pathway.objects.create(key="salaried_work", order=1)
    with pytest.raises(IntegrityError), transaction.atomic():
        Pathway.objects.create(key="scientific_research", order=1)


def test_key_is_unique():
    Pathway.objects.create(key="salaried_work", order=1)
    with pytest.raises(IntegrityError), transaction.atomic():
        Pathway.objects.create(key="salaried_work", order=2)


def test_authorities_validation():
    validate_authorities([])
    validate_authorities([{"name": "Questura", "url": ""}])
    validate_authorities([{"name": "Prefettura", "url": "https://example.invalid/"}])
    with pytest.raises(ValidationError):
        validate_authorities({"name": "x"})
    with pytest.raises(ValidationError):
        validate_authorities([{"name": ""}])
    with pytest.raises(ValidationError):
        validate_authorities([{"name": "Questura", "url": "http://insecure.invalid/"}])


def test_generic_authority_names_are_in_locked_texts():
    corpus = locked_content.canonical(locked_content.LOCKED_TEXTS["fr"])
    for name in GENERIC_AUTHORITY_NAMES:
        assert name in corpus, name


def test_scheduled_pathway_is_live_only_after_publish_at():
    p = Pathway.objects.create(
        key="salaried_work",
        order=1,
        status=PublicationStatus.SCHEDULED,
        publish_at=dt.datetime(2026, 10, 2, tzinfo=dt.UTC),
    )
    with freeze_time("2026-09-30 12:00:00"):
        assert not p.is_live()
        assert not Pathway.objects.live().filter(pk=p.pk).exists()
    with freeze_time("2026-10-03 12:00:00"):
        assert p.is_live()
        assert Pathway.objects.live().filter(pk=p.pk).exists()


def test_draft_pathway_is_never_live():
    p = Pathway.objects.create(key="salaried_work", order=1, status=PublicationStatus.DRAFT)
    with freeze_time("2026-12-01 12:00:00"):
        assert not p.is_live()


def test_get_absolute_url_uses_key():
    p = Pathway.objects.create(key="scientific_research", order=7)
    with translation.override("fr"):
        assert p.get_absolute_url() == "/fr/parcours/scientific_research/"
    with translation.override("ar"):
        assert p.get_absolute_url() == "/ar/parcours/scientific_research/"


def test_translation_unique_per_language():
    p = Pathway.objects.create(key="salaried_work", order=1)
    PathwayTranslation.objects.create(master=p, language="it", eligibility_context="x", status=TranslationStatus.DRAFT)
    with pytest.raises(IntegrityError), transaction.atomic():
        PathwayTranslation.objects.create(master=p, language="it", eligibility_context="y")


def test_step_order_unique_per_pathway_and_pending_by_default():
    p = Pathway.objects.create(key="salaried_work", order=1)
    step = PathwayStep.objects.create(pathway=p, order=1, title_fr="S’orienter")
    assert step.pending_legal_review is True
    assert step.is_reviewed is False
    assert str(step) == "1. S’orienter"
    with pytest.raises(IntegrityError), transaction.atomic():
        PathwayStep.objects.create(pathway=p, order=1, title_fr="Doublon")


def test_pathway_version_increments_on_save():
    p = Pathway.objects.create(key="salaried_work", order=1)
    assert p.version == 1
    p.icon = "briefcase"
    p.save()
    assert p.version == 2
