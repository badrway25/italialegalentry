"""
Views of the company workspace — thin: authentication, HTTP method, rendering.

Every rule about WHAT an account may see lives in ``companies.services`` and ``companies.policies``
(deny by default). Every view is ``login_required``, ``never_cache`` (a company's needs must never
be stored by a shared cache) and ``noindex``.

There is NO view here that lists, searches, counts or displays a person. There is no route that
takes a person identifier. ``apps/companies/tests/test_no_people.py`` proves it by walking every
route this module declares.
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from accounts.permissions import can
from companies import services
from companies.forms import CompanyNeedForm, CompanyProfileForm, WithdrawForm
from companies.models import NeedStatus

CRUMB_MAX_CHARS = 60


def company_view(active: str, methods: tuple[str, ...] = ("GET", "HEAD")):
    """login_required (outermost) → never_cache → allowed methods → back-office kill switch."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            from portal import services as portal_services

            if not portal_services.reserved_area_enabled() and not request.user.is_staff:
                return render(request, "portal/unavailable.html", {"noindex": True}, status=503)
            request.companies_active = active
            return view(request, *args, **kwargs)

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _crumb(label) -> dict:
    return {"label": Truncator(str(label)).chars(CRUMB_MAX_CHARS), "url": ""}


def _render(request, template: str, context: dict, *crumbs: dict):
    from portal import services as portal_services

    root = {"label": _("Espace entreprise"), "url": reverse("companies:dashboard")}
    if root["url"] == request.path:
        root["url"] = ""  # never a link to the page one is on
    # Every view that has a company puts it under « company »; the navigation uses it to hide the
    # entries that only mean something to an account that HAS one. The rail is the console shell's
    # (design V5, V5.4 plan §1.18 D06; W3-A): «Espace entreprise» — this module's own entries
    # (services.navigation), then the way back to «Espace réservé».
    context.update(
        {
            "portal_nav": portal_services.shell_navigation(
                request.user,
                portal_services.SPACE_COMPANY,
                getattr(request, "companies_active", ""),
                company=context.get("company"),
            ),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "noindex": True,
        }
    )
    return render(request, template, context)


def _require_company(request):
    """The company this account is responsible for, or a redirect to the declaration form."""
    company = services.company_for(request.user)
    if company is None:
        messages.info(request, _("Déclarez votre entreprise pour ouvrir votre espace."))
        return None
    return company


# ---------------------------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------------------------
@company_view("dashboard")
def dashboard(request):
    company = services.company_for(request.user)
    needs = list(services.needs_of(company)) if company is not None else []
    context = {
        "company": company,
        "needs": needs,
        "open_needs": [need for need in needs if need.is_open],
        "next_action": services.next_action(company, needs),
        "communications": services.communications(request.user),
        "portal_context": company.legal_name if company else "",
        "can_manage": bool(company and can(request.user, "change", company)),
        "needs_url": services.safe_reverse("companies:needs"),
        "create_url": services.safe_reverse("companies:need_create"),
        "profile_url": services.safe_reverse("companies:profile"),
        "declare_url": services.safe_reverse("companies:profile_create"),
    }
    # The dashboard's composition — the NowPanel, the needs by who holds them — is the console's dashboard presenter
    # (design V5, W3-B): the same raised plane and the same ledger as the person's, over this app's own answers.
    from portal import services as portal_services

    context.update(portal_services.company_dashboard(company, needs, context["next_action"], user=request.user))
    # The space's first page ends its trail on itself — «Espace entreprise › Tableau de bord», the word the rail
    # lights — as every other page does (the W3-A review's m3).
    return _render(request, "companies/dashboard.html", context, {"label": _("Tableau de bord"), "url": ""})


# ---------------------------------------------------------------------------------------------
# The company identity
# ---------------------------------------------------------------------------------------------
@company_view("profile")
def profile(request):
    company = _require_company(request)
    if company is None:
        return redirect("companies:profile_create")
    context = {
        "company": company,
        "can_manage": can(request.user, "change", company),
        "portal_context": company.legal_name,
        "edit_url": services.safe_reverse("companies:profile_edit"),
    }
    return _render(request, "companies/profile.html", context, {"label": _("Mon entreprise"), "url": ""})


@company_view("profile", methods=("GET", "HEAD", "POST"))
def profile_create(request):
    if services.company_for(request.user) is not None:
        return redirect("companies:profile")
    form = CompanyProfileForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = {name: form.cleaned_data[name] for name in form.Meta.fields}
        try:
            services.declare_company(request.user, data=data, request=request)
        except ValidationError as exc:
            form.add_error(None, exc)
        else:
            messages.success(
                request,
                _("Entreprise déclarée. L’équipe du projet procède à la vérification avant toute transmission."),
            )
            return redirect("companies:dashboard")
    context = {"form": form, "is_creation": True}
    return _render(request, "companies/profile_form.html", context, {"label": _("Déclarer mon entreprise"), "url": ""})


@company_view("profile", methods=("GET", "HEAD", "POST"))
def profile_edit(request):
    company = _require_company(request)
    if company is None:
        return redirect("companies:profile_create")
    if not can(request.user, "change", company):
        raise PermissionDenied
    form = CompanyProfileForm(request.POST or None, instance=company)
    if request.method == "POST" and form.is_valid():
        data = {name: form.cleaned_data[name] for name in form.Meta.fields}
        services.update_company(company, data=data, actor=request.user, request=request)
        messages.success(request, _("Identité de l’entreprise mise à jour."))
        return redirect("companies:profile")
    context = {"form": form, "company": company, "is_creation": False, "portal_context": company.legal_name}
    return _render(
        request,
        "companies/profile_form.html",
        context,
        {"label": _("Mon entreprise"), "url": reverse("companies:profile")},
        {"label": _("Modifier"), "url": ""},
    )


# ---------------------------------------------------------------------------------------------
# Needs
# ---------------------------------------------------------------------------------------------
@company_view("needs")
def needs(request):
    company = _require_company(request)
    if company is None:
        return redirect("companies:profile_create")
    rows = list(services.needs_of(company))
    context = {
        "company": company,
        "needs": rows,
        "can_manage": can(request.user, "change", company),
        "portal_context": company.legal_name,
        "create_url": services.safe_reverse("companies:need_create"),
    }
    # the register's counts are its filter, by who holds each need (design V5, W3-E: platform.md E-3)
    from portal import services as portal_services

    context.update(portal_services.needs_register(rows, request.GET.get("état", "")))
    return _render(request, "companies/needs.html", context, {"label": _("Mes besoins"), "url": ""})


@company_view("needs")
def need_detail(request, reference: str):
    need = services.get_own_need(request.user, reference)
    context = {
        "need": need,
        "company": need.company,
        "responsible": services.responsible_for(need),
        "events": list(need.events.all()),
        "mandatory_skills": list(need.mandatory_skills()),
        "preferred_skills": list(need.preferred_skills()),
        "missing": need.missing_for_submission(),
        "can_change": can(request.user, "change", need),
        "can_submit": can(request.user, "submit", need),
        "can_withdraw": can(request.user, "withdraw", need),
        "portal_context": need.reference,
    }
    return _render(
        request,
        "companies/need_detail.html",
        context,
        {"label": _("Mes besoins"), "url": reverse("companies:needs")},
        _crumb(need.title),
    )


@company_view("needs", methods=("GET", "HEAD", "POST"))
def need_create(request):
    company = _require_company(request)
    if company is None:
        return redirect("companies:profile_create")
    if not can(request.user, "change", company):
        raise PermissionDenied
    form = CompanyNeedForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        need = services.create_need(company, data=form.model_data(), actor=request.user, request=request)
        services.set_skills(
            need,
            mandatory=form.cleaned_mandatory(),
            preferred=form.cleaned_preferred(),
            actor=request.user,
            request=request,
        )
        messages.success(request, _("Besoin créé. Il reste un brouillon tant qu’il n’est pas transmis."))
        return redirect("companies:need_detail", reference=need.reference)
    context = {"form": form, "company": company, "is_creation": True, "portal_context": company.legal_name}
    return _render(
        request,
        "companies/need_form.html",
        context,
        {"label": _("Mes besoins"), "url": reverse("companies:needs")},
        {"label": _("Nouveau besoin"), "url": ""},
    )


@company_view("needs", methods=("GET", "HEAD", "POST"))
def need_edit(request, reference: str):
    need = services.get_own_need(request.user, reference)
    if not can(request.user, "change", need):
        raise PermissionDenied
    form = CompanyNeedForm(request.POST or None, instance=need)
    if request.method == "POST" and form.is_valid():
        services.update_need(need, data=form.model_data(), actor=request.user, request=request)
        services.set_skills(
            need,
            mandatory=form.cleaned_mandatory(),
            preferred=form.cleaned_preferred(),
            actor=request.user,
            request=request,
        )
        messages.success(request, _("Besoin mis à jour."))
        return redirect("companies:need_detail", reference=need.reference)
    context = {
        "form": form,
        "need": need,
        "company": need.company,
        "is_creation": False,
        "portal_context": need.reference,
    }
    return _render(
        request,
        "companies/need_form.html",
        context,
        {"label": _("Mes besoins"), "url": reverse("companies:needs")},
        _crumb(need.title),
        {"label": _("Modifier"), "url": ""},
    )


@company_view("needs", methods=("POST",))
def need_submit(request, reference: str):
    need = services.get_own_need(request.user, reference)
    try:
        services.submit(need, actor=request.user, request=request)
    except ValidationError as exc:
        messages.error(request, " ".join(exc.messages))
    else:
        messages.success(request, _("Besoin transmis au projet pour examen."))
    return redirect("companies:need_detail", reference=need.reference)


@company_view("needs", methods=("POST",))
def need_withdraw(request, reference: str):
    need = services.get_own_need(request.user, reference)
    form = WithdrawForm(request.POST)
    reason = form.cleaned_data["reason"] if form.is_valid() else ""
    try:
        services.withdraw(need, actor=request.user, reason=reason, request=request)
    except ValidationError as exc:
        messages.error(request, " ".join(exc.messages))
    else:
        messages.success(request, _("Besoin retiré."))
    return redirect("companies:need_detail", reference=need.reference)


# ---------------------------------------------------------------------------------------------
# Territorial and sectoral analysis — COUNTS ONLY (REQ-B2B-05)
# ---------------------------------------------------------------------------------------------
@company_view("analysis")
def analysis(request):
    """
    Aggregated needs, for the project team only.

    A company must never see this page: it aggregates every company's needs. ``needs_aggregate``
    raises PermissionDenied for anyone outside the project roles, and it returns counts — never a
    company name, a need title or an identifier.
    """
    data = services.needs_aggregate(request.user)
    context = {"aggregate": data, "statuses": NeedStatus.choices}
    return _render(request, "companies/analysis.html", context, {"label": _("Analyse territoriale"), "url": ""})
