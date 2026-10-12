"""
{% load enquiries_tags %}
{% company_needs_form %}   → renders the reusable « Recueil des besoins » form partial (gate-aware),
                             posting to enquiries:company_needs. Intended for ecosystem:companies.
"""

from __future__ import annotations

from django import template
from django.urls import reverse

from core import gates
from enquiries.forms import CompanyNeedsForm

register = template.Library()


@register.inclusion_tag("enquiries/partials/company_needs_form.html", takes_context=True)
def company_needs_form(context, form=None):
    forms_open = gates.public_forms_enabled().open
    if form is None and forms_open:
        form = CompanyNeedsForm()
    return {
        "form": form,
        "forms_open": forms_open,
        "form_action": reverse("enquiries:company_needs"),
        "site": context.get("site"),
        "csrf_token": context.get("csrf_token"),
        "request": context.get("request"),
    }
