"""
Thin views: gate check (G2), throttle, form validation, delegation to ``services.submit``.

Every public form follows the same contract (docs/AGENT_CONVENTIONS.md §2):
* gate closed → GET renders the "form unavailable" component, POST is rejected (403, nothing stored);
* throttle exceeded → ``errors/429.html`` with status 429;
* honeypot spam and 24 h duplicates → same success redirect, nothing stored.
"""

from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from cms import locked_content
from core import gates, throttle
from enquiries import services
from enquiries.forms import CollaborationProposalForm, CompanyNeedsForm, ContactForm
from enquiries.services import FormSpec

DONE_KINDS = {
    "company_needs": {"back_url_name": "ecosystem:companies"},
    "institution_proposal": {"back_url_name": "ecosystem:institutions"},
    "university_proposal": {"back_url_name": "ecosystem:universities"},
    "contact": {"back_url_name": "pages:contact"},
}


def _forms_open() -> bool:
    return gates.public_forms_enabled().open


def _handle(request, *, form_class, spec: FormSpec, template: str, context: dict, form_kwargs=None):
    forms_open = _forms_open()
    form_kwargs = form_kwargs or {}
    if request.method == "POST":
        if not forms_open:
            # G2 closed: nothing is validated, persisted or e-mailed.
            return render(request, template, {**context, "form": None, "forms_open": False}, status=403)
        if not throttle.allow(request, spec.throttle_scope):
            return render(request, "errors/429.html", status=429)
        form = form_class(request.POST, **form_kwargs)
        if form.is_valid():
            services.submit(request, form, spec)
            return redirect(f"{reverse('enquiries:done')}?k={spec.key}")
    else:
        form = form_class(**form_kwargs) if forms_open else None
    return render(request, template, {**context, "form": form, "forms_open": forms_open})


@require_http_methods(["GET", "POST"])
def company_needs(request):
    lang = request.LANGUAGE_CODE
    context = {
        "page_title": locked_content.text("p1.companies.title", lang),
        "meta_description": locked_content.text("p1.companies.intro", lang),
        "breadcrumbs": [
            {"label": _("Espace Entreprises"), "url": _safe_reverse("ecosystem:companies")},
            {"label": _("Recueil des besoins"), "url": ""},
        ],
        "form_action": reverse("enquiries:company_needs"),
    }
    return _handle(
        request,
        form_class=CompanyNeedsForm,
        spec=services.COMPANY_NEEDS,
        template="enquiries/company_needs.html",
        context=context,
    )


def _collaboration(request, spec: FormSpec, *, title: str, phase3_button_key: str, parent_url_name: str, parent_label):
    phase3 = gates.phase3_public()
    lang = request.LANGUAGE_CODE
    # Submit label: Phase 3 prescribed button once G3 is open, else the generic Phase 2 label.
    button_key = phase3_button_key if phase3 else "p2.forum.registration.button_secondary_collab"
    context = {
        "page_title": title,
        "meta_description": title,
        "kind": spec.extra.get("kind"),
        "phase3_public": phase3,
        "button_key": button_key,
        "submit_label": locked_content.text(button_key, lang),
        "breadcrumbs": [
            {"label": parent_label, "url": _safe_reverse(parent_url_name)},
            {"label": title, "url": ""},
        ],
    }
    return _handle(
        request,
        form_class=CollaborationProposalForm,
        spec=spec,
        template="enquiries/collaboration_proposal.html",
        context=context,
        form_kwargs={"purpose": spec.purpose},
    )


@require_http_methods(["GET", "POST"])
def institution_proposal(request):
    return _collaboration(
        request,
        services.INSTITUTION_PROPOSAL,
        title=_("Proposer une collaboration institutionnelle"),
        phase3_button_key="p3.institutions.button",
        parent_url_name="ecosystem:institutions",
        parent_label=_("Espace Institutions"),
    )


@require_http_methods(["GET", "POST"])
def university_proposal(request):
    return _collaboration(
        request,
        services.UNIVERSITY_PROPOSAL,
        title=_("Proposer un partenariat — universités et organismes de formation"),
        phase3_button_key="p3.universities.button",
        parent_url_name="ecosystem:universities",
        parent_label=_("Espace Universités et Formation"),
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    title = _("Nous écrire")
    context = {
        "page_title": title,
        "meta_description": _("Formulaire de contact d’Italy Legal Entry™ — une seule adresse de réponse."),
        "breadcrumbs": [
            {"label": _("Contact"), "url": _safe_reverse("pages:contact")},
            {"label": title, "url": ""},
        ],
    }
    return _handle(
        request,
        form_class=ContactForm,
        spec=services.CONTACT,
        template="enquiries/contact.html",
        context=context,
    )


@require_http_methods(["GET"])
def done(request) -> HttpResponse:
    kind = request.GET.get("k", "")
    info = DONE_KINDS.get(kind, {})
    back_url = _safe_reverse(info.get("back_url_name", "")) if info else ""
    return render(
        request,
        "enquiries/done.html",
        {
            "page_title": _("Demande transmise"),
            "back_url": back_url,
            "noindex": True,
            "kind": kind if info else "",
            "breadcrumbs": [{"label": _("Demande transmise"), "url": ""}],
        },
    )


def _safe_reverse(name: str) -> str:
    """Gate-aware reverse: "" when the route is missing or still behind a closed gate."""
    from core.links import public_url

    return public_url(name)
