"""Integration points offered to sibling apps: sitemap, reusable form partial / template tag, portal hook."""

import pytest
from django.template import Context, Template
from django.test import RequestFactory

from cms import locked_content
from core.sitemaps import SITEMAPS
from enquiries.forms import CompanyNeedsForm

pytestmark = pytest.mark.django_db


def test_sitemap_registered_and_lists_form_pages(client, seeded):
    assert "enquiries" in SITEMAPS
    xml = client.get("/sitemap.xml").content.decode()
    for path in ("entreprises/recueil-des-besoins/", "collaboration/institutions/", "contact/formulaire/"):
        assert f"/fr/{path}" in xml
        assert f"/ar/{path}" in xml
    assert "demande-transmise" not in xml  # confirmation page is noindex, never listed


def _render_tag(request):
    template = Template("{% load enquiries_tags %}{% company_needs_form %}")
    return template.render(Context({"request": request, "site": {"contact_email": "contact@agamieuromed.org"}}))


def test_company_needs_form_tag_renders_unavailable_when_gate_closed(seeded):
    request = RequestFactory().get("/fr/entreprises/")
    html = _render_tag(request)
    assert 'data-gate="forms-closed"' in html
    assert "<form" not in html


def test_company_needs_form_tag_renders_form_posting_to_enquiries(seeded, legal_published):
    request = RequestFactory().get("/fr/entreprises/")
    html = _render_tag(request)
    assert 'action="/fr/entreprises/recueil-des-besoins/"' in html
    assert locked_content.text("p1.companies.form.button", "fr") in html
    assert locked_content.text("p1.companies.form.consent", "fr") in html
    for label in locked_content.get("p1.companies.form.fields", "fr")[0]:
        assert label in html


def test_company_needs_form_tag_accepts_bound_form(seeded, legal_published):
    request = RequestFactory().get("/fr/entreprises/")
    bound = CompanyNeedsForm({"company_name": ""})
    bound.is_valid()
    template = Template("{% load enquiries_tags %}{% company_needs_form form=bound %}")
    html = template.render(Context({"request": request, "bound": bound}))
    assert 'aria-invalid="true"' in html
