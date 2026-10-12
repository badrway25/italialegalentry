"""Unit tests — FAQ models and services (no HTTP)."""

import datetime as dt

import pytest
from django.core.exceptions import ValidationError

from cms import locked_content
from cms.models import PublicationStatus, TranslationStatus
from faq import registry, services
from faq.models import FAQCategory, FAQItem, FAQItemTranslation

pytestmark = pytest.mark.django_db


@pytest.fixture
def category():
    return FAQCategory.objects.create(slug="general", name_fr="Général", order=0)


def test_registry_exposes_nine_prescribed_entries_in_order():
    keys = registry.keys()
    assert len(keys) == 9
    assert keys[0] == "faq_visas"
    assert keys[-1] == "faq_guaranteed_visa_offer"
    # Compare with the registry itself: prescribed wording is never copied into code (gate G0).
    prescribed = locked_content.get("p3.faq.items", "fr")[0]
    assert registry.item("faq_visas") == prescribed[0]
    assert registry.items() == prescribed
    assert registry.item("unknown") is None


def test_locked_item_save_re_asserts_registry_text(category):
    item = FAQItem.objects.create(
        key="faq_visas", category=category, is_locked=True, question_fr="tampered", answer_fr="tampered"
    )
    item.refresh_from_db()
    assert item.question_fr == registry.item("faq_visas")["question"]
    assert item.answer_fr == registry.item("faq_visas")["answer"]
    item.answer_fr = "tampered again"
    item.save()
    item.refresh_from_db()
    assert item.answer_fr == registry.item("faq_visas")["answer"]


def test_unlocked_item_keeps_editorial_text(category):
    item = FAQItem.objects.create(
        key="horaires", category=category, question_fr="Question éditoriale ?", answer_fr="Réponse éditoriale."
    )
    item.refresh_from_db()
    assert item.is_locked is False
    assert item.question_fr == "Question éditoriale ?"


def test_clean_rejects_locking_a_key_outside_the_registry(category):
    item = FAQItem(key="not_in_registry", category=category, is_locked=True, question_fr="q", answer_fr="a")
    with pytest.raises(ValidationError) as exc:
        item.full_clean()
    assert "is_locked" in exc.value.message_dict


def test_translation_rejects_french_source_language(category):
    item = FAQItem.objects.create(key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="")
    row = FAQItemTranslation(master=item, language="fr", question="q", answer="a")
    with pytest.raises(ValidationError) as exc:
        row.full_clean()
    assert "language" in exc.value.message_dict


def test_published_translation_of_locked_item_requires_official_source(category):
    item = FAQItem.objects.create(key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="")
    row = FAQItemTranslation(master=item, language="it", question="q", answer="a", status=TranslationStatus.PUBLISHED)
    with pytest.raises(ValidationError) as exc:
        row.full_clean()
    assert "source" in exc.value.message_dict
    row.source = "testo ufficiale trasmesso il 2026-10-05"
    row.full_clean()  # no error


def test_live_queryset_respects_status_and_window(category):
    published = FAQItem.objects.create(
        key="a", category=category, question_fr="A ?", answer_fr="a", status=PublicationStatus.PUBLISHED
    )
    FAQItem.objects.create(key="b", category=category, question_fr="B ?", answer_fr="b")  # draft
    FAQItem.objects.create(
        key="c",
        category=category,
        question_fr="C ?",
        answer_fr="c",
        status=PublicationStatus.PUBLISHED,
        unpublish_at=dt.datetime(2020, 1, 1, tzinfo=dt.UTC),
    )
    assert list(services.live_items()) == [published]


def test_entry_for_locked_item_uses_registry_and_marks_fallback(category):
    item = FAQItem.objects.create(
        key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="", status="published"
    )
    FAQItem.objects.filter(pk=item.pk).update(answer_fr="db mirror tampered")  # bypasses save()
    item.refresh_from_db()
    entry_fr = services.entry_for(item, "fr")
    assert entry_fr.answer == registry.item("faq_visas")["answer"]
    assert entry_fr.lang == "fr" and entry_fr.is_fallback is False
    entry_ar = services.entry_for(item, "ar")
    assert entry_ar.lang == "fr" and entry_ar.is_fallback is True


def test_entry_for_uses_published_translation_only(category):
    item = FAQItem.objects.create(
        key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="", status="published"
    )
    FAQItemTranslation.objects.create(
        master=item, language="it", question="Domanda IT", answer="Risposta IT", status=TranslationStatus.DRAFT
    )
    assert services.entry_for(item, "it").is_fallback is True
    FAQItemTranslation.objects.filter(master=item, language="it").update(
        status=TranslationStatus.PUBLISHED, source="ufficiale"
    )
    item = FAQItem.objects.prefetch_related("translations").get(pk=item.pk)
    entry = services.entry_for(item, "it")
    assert entry.is_fallback is False and entry.lang == "it" and entry.question == "Domanda IT"


def test_group_entries_orders_by_category_and_translates_names(category):
    other = FAQCategory.objects.create(slug="demarches", name_fr="Démarches", order=5)
    FAQItem.objects.create(key="x", category=other, question_fr="X ?", answer_fr="x", status="published", order=1)
    FAQItem.objects.create(key="y", category=category, question_fr="Y ?", answer_fr="y", status="published", order=1)
    entries = services.entries_for(services.live_items(), "fr")
    groups = services.group_entries(entries, "fr")
    assert [g.category.slug for g in groups] == ["general", "demarches"]
    assert groups[1].name == "Démarches" and groups[1].is_fallback is False
    groups_it = services.group_entries(entries, "it")
    assert groups_it[0].is_fallback is True and groups_it[0].lang == "fr"


def test_search_matches_french_full_text_and_substrings(category):
    FAQItem.objects.create(
        key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="", status="published"
    )
    FAQItem.objects.create(
        key="faq_who", category=category, is_locked=True, question_fr="", answer_fr="", status="published"
    )
    assert [i.key for i in services.search_items("visas")] == ["faq_visas"]
    assert [i.key for i in services.search_items("AGAMI")] == ["faq_who"]
    assert list(services.search_items("zzzz-nothing")) == []
    assert services.normalise_query("  a   b  ") == "a b"
    assert len(services.normalise_query("x" * 500)) == services.MAX_QUERY_LENGTH


def test_jsonld_contains_only_live_items(category):
    live = FAQItem.objects.create(
        key="faq_visas", category=category, is_locked=True, question_fr="", answer_fr="", status="published"
    )
    draft = FAQItem.objects.create(key="draft", category=category, question_fr="Draft ?", answer_fr="d")
    data = services.faq_jsonld(services.entries_for([live, draft], "fr"), "fr")
    assert data["@type"] == "FAQPage"
    assert [q["name"] for q in data["mainEntity"]] == [registry.item("faq_visas")["question"]]
    rendered = str(services.render_jsonld({"x": "</script><b>&"}))
    assert "</script>" not in rendered and "<" not in rendered and "&" not in rendered
