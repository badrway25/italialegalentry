"""
Espace réservé views — thin: authentication, HTTP method, rendering. Every rule about WHAT an
account may see lives in ``portal.services`` / ``portal.policies`` (deny by default).

All views are ``login_required`` (anonymous → login page, whatever the HTTP method), ``never_cache``
(personal pages must never be stored by a shared cache) and ``noindex``.
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from portal import services


def portal_view(active: str, methods: tuple[str, ...] = ("GET", "HEAD")):
    """
    login_required (outermost, so an anonymous request is always sent to the login page) →
    never_cache → allowed methods → back-office kill switch.
    """

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not services.reserved_area_enabled() and not request.user.is_staff:
                response = render(request, "portal/unavailable.html", {"noindex": True}, status=503)
                return _noindex(response)
            request.portal_active = active
            return _noindex(view(request, *args, **kwargs))

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _noindex(response):
    """
    Say "do not index" in the HEADER as well as in the page.

    ``base.html`` already emits the meta tag, and that is what a crawler parsing the body reads. The
    header covers what the meta tag cannot: a HEAD request, a redirect, a 503, a file download —
    every response from the reserved area that is not a rendered HTML body. Neither one is
    sufficient on its own, and a personal case file is not somewhere to rely on the sufficient case.
    """
    response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
    return response


CRUMB_MAX_CHARS = 60


def _crumb(label) -> dict:
    """Last breadcrumb of a detail page: free text (subject, company name…) is shortened — the full
    wording is the page's h1 — so a long, unbroken value can never stretch the page on a phone."""
    return {"label": Truncator(str(label)).chars(CRUMB_MAX_CHARS), "url": ""}


def _render(request, template: str, context: dict, *crumbs: dict):
    root = {"label": _("Espace réservé"), "url": reverse("portal:dashboard")}
    if root["url"] == request.path:
        root["url"] = ""  # never a link to the page one is on
    context.update(
        {
            "portal_nav": services.navigation(request.user, getattr(request, "portal_active", "")),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "noindex": True,
        }
    )
    return render(request, template, context)


@portal_view("dashboard")
def dashboard(request):
    # The space's first page ends its trail on itself, as every other page does — «Espace réservé › Tableau de
    # bord», the word the rail lights — and not on the space's name (the W3-A review's m3).
    return _render(
        request,
        "portal/dashboard.html",
        services.dashboard_context(request.user),
        {"label": _("Tableau de bord"), "url": ""},
    )


@portal_view("requests")
def requests_list(request):
    page_obj = services.paginate(services.requests_for(request.user), request.GET.get("page"))
    return _render(request, "portal/requests.html", {"page_obj": page_obj}, {"label": _("Mes demandes"), "url": ""})


@portal_view("requests")
def request_detail(request, kind: str, pk: int):
    context = services.get_own_request(request.user, kind, pk)
    return _render(
        request,
        "portal/request_detail.html",
        context,
        {"label": _("Mes demandes"), "url": reverse("portal:requests")},
        _crumb(context["item"].title),
    )


@portal_view("pathways")
def pathways(request):
    context = services.pathways_page(request.user, request.GET.get("page"))
    return _render(request, "portal/pathways.html", context, {"label": _("Mon parcours"), "url": ""})


@portal_view("documents")
def documents(request):
    context = services.documents_page(request.user)
    context["page_obj"] = services.paginate(context.pop("documents"), request.GET.get("page"), per_page=20)
    return _render(request, "portal/documents.html", context, {"label": _("Mes documents"), "url": ""})


@portal_view("deadlines")
def deadlines(request):
    context = services.deadlines_page(request.user)
    return _render(request, "portal/deadlines.html", context, {"label": _("Mes échéances"), "url": ""})


@portal_view("messages")
def messages_list(request):
    page_obj = services.paginate(services.inbox(request.user), request.GET.get("page"))
    context = {"page_obj": page_obj, "unread_count": services.unread_count(request.user)}
    return _render(request, "portal/messages.html", context, {"label": _("Communications"), "url": ""})


@portal_view("messages")
def message_detail(request, pk):
    message = services.get_own_message(request.user, pk)
    context = {"message": message, "related_link": services.related_link(request.user, message)}
    return _render(
        request,
        "portal/message_detail.html",
        context,
        {"label": _("Communications"), "url": reverse("portal:messages")},
        _crumb(message.subject),
    )


@portal_view("messages", methods=("POST",))
def message_read(request, pk):
    message = services.mark_message_read(request.user, pk, request=request)
    messages.success(request, _("Communication marquée comme lue."))
    if request.POST.get("next") == "list":  # enumerated value — never a free URL (no open redirect)
        return redirect("portal:messages")
    return redirect("portal:message_detail", pk=message.pk)


@portal_view("situation", methods=("GET", "HEAD", "POST"))
def situation(request):
    """
    What the person tells us about their circumstances — and what changes when they tell us.

    The page is not a settings form. Saving it re-runs the legal rules against the new facts, so a
    person who reports a job offer sees their orientation move on the same visit. That is the whole
    difference between a profile and a questionnaire nobody reads again.
    """
    from accounts import services as account_services
    from accounts.profile_forms import SituationForm

    user = account_services.concrete_user(request.user)
    profile = account_services.get_or_create_profile(user)

    if request.method == "POST":
        form = SituationForm(request.POST, profile=profile)
        if form.is_valid():
            _profile, changed = account_services.update_situation(request, user, form.to_profile_values())
            if changed:
                updated = services.reassess_person(user, request=request)
                if updated is not None:
                    messages.success(
                        request,
                        _("Vos informations ont été enregistrées et votre orientation a été recalculée."),
                    )
                else:
                    messages.success(request, _("Vos informations ont été enregistrées."))
            else:
                messages.info(request, _("Aucune modification à enregistrer."))
            return redirect("portal:situation")
    else:
        form = SituationForm(profile=profile)

    # Design V4 (§3.7): the Stepper fills a node per answered question — the profile's own ``answered()`` rule, plus the
    # one question the rules do not read yet. One total for the person (W3-D's m4, W3-E): the counter under the Stepper
    # counts the questions the page asks and the ones answered, as the Stepper's nodes and the foot's «1 / 8» do — it
    # said «sur 7» (the fields the rules read) under eight nodes.
    answered_fields = set(profile.answered()) | (
        {"has_qualification_recognition"} if profile.has_qualification_recognition is not None else set()
    )
    return _render(
        request,
        "portal/situation.html",
        {
            "form": form,
            "profile": profile,
            "answered": len(answered_fields),
            "total": len(form.visible_fields()),
            "answered_fields": answered_fields,
            "case": services.active_case(user),
        },
        _crumb(_("Ma situation")),
    )
