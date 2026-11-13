"""
Thin views: gate check (G2), throttle, form validation, delegation to ``services.submit``.

Every public form follows the same contract (docs/AGENT_CONVENTIONS.md §2):
* gate closed → GET renders the "form unavailable" component, POST is rejected (403, nothing stored);
* throttle exceeded → the same form page with status 429: the form bound to what the person typed and a calm notice
  (V5.32, P2-10 of the integration review — the throttle itself is unchanged: every POST counts); nothing is sent;
* honeypot spam and 24 h duplicates → same success redirect, nothing stored.
"""

from __future__ import annotations

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_http_methods

from cms import locked_content
from core import gates, throttle
from enquiries import services
from enquiries.forms import CollaborationProposalForm, CompanyNeedsForm, ContactForm
from enquiries.services import FormSpec

#: V5.32 (lane C): a request of a family's space returns to that space BY NAME — its crumb in the trail (as on its form)
#: and its return action («Retour à l’espace …»); the contact keeps «Retour à la page précédente» and its plain trail
DONE_KINDS = {
    "company_needs": {
        "back_url_name": "ecosystem:companies",
        "space": gettext_lazy("Espace Entreprises"),
        "back_label": gettext_lazy("Retour à l’espace Entreprises"),
    },
    "institution_proposal": {
        "back_url_name": "ecosystem:institutions",
        "space": gettext_lazy("Espace Institutions"),
        "back_label": gettext_lazy("Retour à l’espace Institutions"),
    },
    "university_proposal": {
        "back_url_name": "ecosystem:universities",
        "space": gettext_lazy("Espace Universités et Formation"),
        "back_label": gettext_lazy("Retour à l’espace Universités et Formation"),
    },
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
            # V5.32 (lane C; P2-10 of the integration review): the refusal no longer loses what the person typed —
            # the same page, the form bound to their data, and the 429 page's own words as a calm notice (base.html's
            # session notices). Nothing is submitted, stored or e-mailed; the status stays 429; the throttle is as it
            # was (every POST counts).
            messages.info(
                request,
                _(
                    "Vous avez atteint la limite d’envois autorisée. Merci de réessayer dans quelques minutes ; rien "
                    "n’a été perdu de votre côté."
                ),
            )
            form = form_class(request.POST, **form_kwargs)
            return render(request, template, {**context, "form": form, "forms_open": True}, status=429)
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
    space = info.get("space") if back_url else None
    return render(
        request,
        "enquiries/done.html",
        {
            "page_title": _("Demande transmise"),
            "back_url": back_url,
            "back_label": info.get("back_label", "") if back_url else "",
            "noindex": True,
            "kind": kind if info else "",
            "breadcrumbs": [
                *([{"label": space, "url": back_url}] if space else []),
                {"label": _("Demande transmise"), "url": ""},
            ],
        },
    )


def _safe_reverse(name: str) -> str:
    """Gate-aware reverse: "" when the route is missing or still behind a closed gate."""
    from core.links import public_url

    return public_url(name)
