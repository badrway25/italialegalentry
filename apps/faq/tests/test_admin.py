"""Back-office tests — locked FAQ texts are read-only and undeletable; unlocked entries are editable."""

import re

import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.urls import reverse

from faq import registry
from faq.admin import FAQItemAdmin
from faq.models import FAQCategory, FAQItem
from faq.seeds import seed_locked_faq_items

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]


@pytest.fixture
def seeded_faq():
    seed_locked_faq_items()
    return FAQItem.objects.get(key="faq_visas")


@pytest.fixture
def admin_client(client, superuser):
    client.force_login(superuser)
    return client


def _request(user):
    request = RequestFactory().get("/backoffice/")
    request.user = user
    return request


def test_locked_fields_are_readonly_for_locked_items(seeded_faq, superuser):
    model_admin = FAQItemAdmin(FAQItem, AdminSite())
    readonly = model_admin.get_readonly_fields(_request(superuser), seeded_faq)
    for name in ("question_fr", "answer_fr", "key", "is_locked"):
        assert name in readonly
    assert model_admin.has_delete_permission(_request(superuser), seeded_faq) is False
    assert model_admin.get_prepopulated_fields(_request(superuser), seeded_faq) == {}


def test_unlocked_items_remain_editable(superuser):
    category = FAQCategory.objects.create(slug="general", name_fr="Général")
    item = FAQItem.objects.create(key="horaires", category=category, question_fr="Q ?", answer_fr="A.")
    model_admin = FAQItemAdmin(FAQItem, AdminSite())
    readonly = model_admin.get_readonly_fields(_request(superuser), item)
    assert "question_fr" not in readonly and "answer_fr" not in readonly
    assert "is_locked" in readonly  # only the seed may lock rows
    assert model_admin.has_delete_permission(_request(superuser), item) is True
    assert model_admin.get_prepopulated_fields(_request(superuser), None) == {"key": ("question_fr",)}


def test_change_view_renders_locked_text_readonly(admin_client, seeded_faq):
    url = reverse("admin:faq_faqitem_change", args=[seeded_faq.pk])
    response = admin_client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert registry.item("faq_visas")["answer"] in html
    assert not re.search(r'<(input|textarea)[^>]*\sname="answer_fr"', html)
    assert not re.search(r'<(input|textarea)[^>]*\sname="question_fr"', html)
    assert not re.search(r'<(input|textarea)[^>]*\sname="key"', html)
    assert re.search(r'<input[^>]*\sname="order"', html)  # editorial field still editable


def test_posting_the_change_form_cannot_alter_locked_text(admin_client, seeded_faq):
    url = reverse("admin:faq_faqitem_change", args=[seeded_faq.pk])
    data = {
        "category": seeded_faq.category_id,
        "order": 5,
        "status": "published",
        "last_updated": "2026-09-14",
        "editorial_note": "",
        "question_fr": "HACKED QUESTION",
        "answer_fr": "HACKED ANSWER",
        "key": "hacked_key",
        "translations-TOTAL_FORMS": "0",
        "translations-INITIAL_FORMS": "0",
        "translations-MIN_NUM_FORMS": "0",
        "translations-MAX_NUM_FORMS": "1000",
    }
    response = admin_client.post(url, data)
    assert response.status_code in (200, 302), response.content[:500]
    seeded_faq.refresh_from_db()
    assert seeded_faq.key == "faq_visas"
    assert seeded_faq.question_fr == registry.item("faq_visas")["question"]
    assert seeded_faq.answer_fr == registry.item("faq_visas")["answer"]
    assert seeded_faq.order == 5, "editorial reorder must still be applied"


def test_changelist_and_category_admin_render(admin_client, seeded_faq):
    assert admin_client.get(reverse("admin:faq_faqitem_changelist")).status_code == 200
    assert admin_client.get(reverse("admin:faq_faqcategory_changelist")).status_code == 200
    assert admin_client.get(reverse("admin:faq_faqitem_add")).status_code == 200


def test_delete_view_refused_for_locked_item(admin_client, seeded_faq):
    url = reverse("admin:faq_faqitem_delete", args=[seeded_faq.pk])
    response = admin_client.post(url, {"post": "yes"})
    assert response.status_code == 403
    assert FAQItem.objects.filter(pk=seeded_faq.pk).exists()


def test_csv_export_action(admin_client, seeded_faq):
    url = reverse("admin:faq_faqitem_changelist")
    response = admin_client.post(url, {"action": "export_csv", "_selected_action": [seeded_faq.pk]})
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert "faq_visas" in response.content.decode("utf-8")
