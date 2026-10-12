"""Seed tests — the nine prescribed FAQ entries are created exactly once, verbatim, and never drift."""

import pytest
from django.core.management import call_command

from cms import locked_content
from cms.models import PublicationStatus
from faq import registry
from faq.models import FAQCategory, FAQItem
from faq.seeds import LOCKED_SOURCE_DATE, seed_locked_faq_items

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]


def test_seed_creates_nine_locked_published_items_in_prescribed_order():
    seed_locked_faq_items()
    items = list(FAQItem.objects.filter(is_locked=True).order_by("order"))
    assert len(items) == 9
    prescribed = locked_content.get("p3.faq.items", "fr")[0]
    assert [i.key for i in items] == [p["key"] for p in prescribed]
    for item, entry in zip(items, prescribed, strict=True):
        assert item.question_fr == entry["question"]
        assert item.answer_fr == entry["answer"]
        assert item.status == PublicationStatus.PUBLISHED
        assert item.category.slug == "general"
        assert item.last_updated == LOCKED_SOURCE_DATE
    assert FAQCategory.objects.count() == 1


def test_seed_is_idempotent_and_does_not_bump_versions():
    seed_locked_faq_items()
    versions = dict(FAQItem.objects.values_list("key", "version"))
    result = seed_locked_faq_items()
    assert FAQItem.objects.count() == 9
    assert FAQCategory.objects.count() == 1
    assert dict(FAQItem.objects.values_list("key", "version")) == versions
    assert result.startswith("0 locked FAQ item(s) created, 0 re-synchronised")


def test_seed_all_command_runs_the_faq_seed():
    call_command("seed_all", "--only", "faq", verbosity=0)
    assert FAQItem.objects.filter(is_locked=True).count() == 9
    call_command("seed_all", "--only", "faq", verbosity=0)
    assert FAQItem.objects.count() == 9


def test_seed_preserves_editorial_fields_but_restores_locked_text():
    seed_locked_faq_items()
    other = FAQCategory.objects.create(slug="demarches", name_fr="Démarches", order=3)
    item = FAQItem.objects.get(key="faq_visas")
    item.order = 999
    item.category = other
    item.status = PublicationStatus.DRAFT
    item.save()
    # Bypass save() to simulate a drift of the mirrored text in the database.
    FAQItem.objects.filter(key="faq_visas").update(answer_fr="drifted", is_locked=False)
    seed_locked_faq_items()
    item.refresh_from_db()
    assert item.order == 999
    assert item.category == other
    assert item.status == PublicationStatus.DRAFT
    assert item.is_locked is True
    assert item.answer_fr == registry.item("faq_visas")["answer"]
