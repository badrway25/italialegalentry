"""Back-office tests — locked glossary texts are read-only and undeletable; unlocked terms are editable."""

import re

import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.urls import reverse

from glossary import registry
from glossary.admin import TermAdmin
from glossary.models import Term
from glossary.seeds import seed_locked_terms

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]


@pytest.fixture
def locked_term():
    seed_locked_terms()
    return Term.objects.get(key="codice_fiscale")


@pytest.fixture
def admin_client(client, superuser):
    client.force_login(superuser)
    return client


def _request(user):
    request = RequestFactory().get("/backoffice/")
    request.user = user
    return request


def test_locked_fields_are_readonly_for_locked_terms(locked_term, superuser):
    model_admin = TermAdmin(Term, AdminSite())
    readonly = model_admin.get_readonly_fields(_request(superuser), locked_term)
    for name in ("term", "definition_fr", "key", "is_locked"):
        assert name in readonly
    assert model_admin.has_delete_permission(_request(superuser), locked_term) is False
    assert model_admin.get_prepopulated_fields(_request(superuser), locked_term) == {}


def test_unlocked_terms_remain_editable(superuser):
    term = Term.objects.create(key="isee", term="ISEE", definition_fr="indicateur…")
    model_admin = TermAdmin(Term, AdminSite())
    readonly = model_admin.get_readonly_fields(_request(superuser), term)
    assert "term" not in readonly and "definition_fr" not in readonly
    assert "is_locked" in readonly
    assert model_admin.has_delete_permission(_request(superuser), term) is True


def test_change_view_renders_locked_text_readonly(admin_client, locked_term):
    response = admin_client.get(reverse("admin:glossary_term_change", args=[locked_term.pk]))
    assert response.status_code == 200
    html = response.content.decode()
    assert registry.term("codice_fiscale")["definition"] in html
    assert not re.search(r'<(input|textarea)[^>]*\sname="definition_fr"', html)
    assert not re.search(r'<(input|textarea)[^>]*\sname="term"', html)
    assert not re.search(r'<(input|textarea)[^>]*\sname="key"', html)
    assert re.search(r'<input[^>]*\sname="source"', html)  # editorial metadata still editable


def test_posting_the_change_form_cannot_alter_locked_text(admin_client, locked_term):
    url = reverse("admin:glossary_term_change", args=[locked_term.pk])
    data = {
        "status": "published",
        "source": "Source mise à jour",
        "editorial_note": "",
        "term": "HACKED",
        "definition_fr": "HACKED",
        "key": "hacked",
        "translations-TOTAL_FORMS": "0",
        "translations-INITIAL_FORMS": "0",
        "translations-MIN_NUM_FORMS": "0",
        "translations-MAX_NUM_FORMS": "1000",
    }
    response = admin_client.post(url, data)
    assert response.status_code in (200, 302), response.content[:500]
    locked_term.refresh_from_db()
    assert locked_term.key == "codice_fiscale"
    assert locked_term.term == "Codice fiscale"
    assert locked_term.definition_fr == registry.term("codice_fiscale")["definition"]
    assert locked_term.source == "Source mise à jour"


def test_changelist_add_and_autocomplete_render(admin_client, locked_term):
    assert admin_client.get(reverse("admin:glossary_term_changelist")).status_code == 200
    assert admin_client.get(reverse("admin:glossary_term_add")).status_code == 200
    response = admin_client.get(
        reverse("admin:autocomplete"),
        {"term": "codice", "app_label": "glossary", "model_name": "term", "field_name": "related"},
    )
    assert response.status_code == 200
    assert "Codice fiscale" in response.content.decode()


def test_delete_view_refused_for_locked_term(admin_client, locked_term):
    response = admin_client.post(reverse("admin:glossary_term_delete", args=[locked_term.pk]), {"post": "yes"})
    assert response.status_code == 403
    assert Term.objects.filter(pk=locked_term.pk).exists()


def test_csv_export_action(admin_client, locked_term):
    response = admin_client.post(
        reverse("admin:glossary_term_changelist"), {"action": "export_csv", "_selected_action": [locked_term.pk]}
    )
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert "codice_fiscale" in response.content.decode("utf-8")
