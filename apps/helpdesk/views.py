"""
Views of the digital help desk — thin: authentication, HTTP method, rendering.

Every rule about WHAT an account may see or do lives in ``helpdesk.services`` (state machine and
audit) and ``helpdesk.policies`` (object level, deny by default). A view never filters after the
fact: it asks a service for a queryset that is already authorised.

All views are ``login_required`` (an anonymous request goes to the login page whatever the method),
``never_cache`` (a legal question must never sit in a shared cache) and ``noindex``. Every mutating
view is POST-only and redirects afterwards, so a refresh cannot replay an act.
"""

from __future__ import annotations

import uuid as uuid_lib
from functools import wraps

from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from accounts import roles
from accounts.permissions import require
from helpdesk import forms, services
from helpdesk.models import HelpdeskTicket, MessageVisibility, TicketOrigin, TicketStatus

CRUMB_MAX_CHARS = 60


def helpdesk_view(active: str = "helpdesk", methods: tuple[str, ...] = ("GET", "HEAD")):
    """login_required (outermost) → never_cache → allowed methods → reserved-area kill switch."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not _reserved_area_enabled() and not request.user.is_staff:
                return render(request, "portal/unavailable.html", {"noindex": True}, status=503)
            request.portal_active = active
            return view(request, *args, **kwargs)

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _reserved_area_enabled() -> bool:
    """The back-office kill switch of the reserved area, honoured here as in ``portal.views``."""
    try:
        from portal.services import reserved_area_enabled
    except ImportError:  # pragma: no cover - the sibling app is always installed
        return True
    return reserved_area_enabled()


def _navigation(user, active: str) -> list[dict]:
    """
    The platform navigation, with the help desk appended.

    ``portal.services.navigation`` owns the reserved area's entries and is read, never edited; the
    help desk adds its own row so the module is reachable from every authenticated page. When the
    signed-in account is a professional or dispatches requests, its working register is listed too —
    « la navigation s'adapte aux permissions : un module non disponible ne se montre pas ».
    """
    items: list[dict] = []
    try:
        from portal.services import navigation

        items = list(navigation(user, ""))
    except Exception:  # noqa: BLE001 - a sibling app being changed must not break this page
        items = []
    known = {item.get("key") for item in items}
    if "helpdesk" not in known:
        # `portal.services.navigation` lists the help desk now, so this is the fallback for the
        # case where it does not — a sibling app being changed must not make the module
        # unreachable from its own pages.
        items.append(
            {
                "key": "helpdesk",
                "label": _("Guichet numérique"),
                "url": reverse("helpdesk:requests"),
            }
        )
    for item in items:
        item["current"] = item.get("key") == active
    if roles.has_role(user, roles.PROFESSIONAL):
        items.append(
            {
                "key": "helpdesk-queue",
                "label": _("Demandes qui me sont confiées"),
                "url": reverse("helpdesk:queue"),
                "current": active == "helpdesk-queue",
            }
        )
    if roles.has_role(user, roles.OPERATOR, roles.ADMINISTRATOR):
        items.append(
            {
                "key": "helpdesk-dispatch",
                "label": _("Désignation des professionnels"),
                "url": reverse("helpdesk:dispatch"),
                "current": active == "helpdesk-dispatch",
            }
        )
    return items


def _render(request, template: str, context: dict, *crumbs: dict):
    root = {"label": _("Espace réservé"), "url": reverse("portal:dashboard")}
    context.update(
        {
            "portal_nav": _navigation(request.user, getattr(request, "portal_active", "")),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "noindex": True,
        }
    )
    return render(request, template, context)


def _crumb(label) -> dict:
    return {"label": Truncator(str(label)).chars(CRUMB_MAX_CHARS), "url": ""}


def _desk_crumb() -> dict:
    return {"label": _("Guichet numérique"), "url": reverse("helpdesk:requests")}


def _get(request, uuid_value) -> HelpdeskTicket:
    return services.ticket_detail(request.user, uuid_value)


def _back(ticket: HelpdeskTicket):
    return redirect("helpdesk:detail", uuid=ticket.uuid)


# ---------------------------------------------------------------------------------------------
# The person
# ---------------------------------------------------------------------------------------------
@helpdesk_view()
def requests_list(request):
    tickets = services.tickets_for(request.user)
    context = {
        "tickets": tickets,
        "open_count": sum(1 for row in tickets if row.is_open),
    }
    return _render(request, "helpdesk/requests.html", context, {**_desk_crumb(), "url": ""})


@helpdesk_view(methods=("GET", "HEAD", "POST"))
def open_request(request):
    form = forms.OpenRequestForm(request.POST or None, person=request.user)
    if request.method == "POST" and form.is_valid():
        wants_review = form.cleaned_data.get("professional_review")
        ticket = services.open_ticket(
            request.user,
            subject=form.cleaned_data["subject"],
            question=form.cleaned_data["question"],
            case=form.cleaned_data.get("case"),
            origin=TicketOrigin.PERSON,
            language=get_language() or "fr",
            status=(TicketStatus.PROFESSIONAL_REVIEW_REQUIRED if wants_review else TicketStatus.INFORMATION_ONLY),
            request=request,
        )
        django_messages.success(
            request,
            _("Votre demande est enregistrée sous la référence %(reference)s.") % {"reference": ticket.reference},
        )
        return _back(ticket)
    return _render(
        request,
        "helpdesk/open_request.html",
        {"form": form},
        _desk_crumb(),
        {"label": _("Nouvelle demande"), "url": ""},
    )


@helpdesk_view()
def detail(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "view", ticket)
    is_person = ticket.person_id == request.user.id
    is_assignee = ticket.assignee_id == request.user.id and ticket.mandate_is_live
    context = {
        "ticket": ticket,
        "exchange": services.exchange_for(request.user, ticket),
        "next_step": services.next_step_for(ticket),
        "waits_on_person": services.waits_on_person(ticket),
        "is_person": is_person,
        "is_assignee": is_assignee,
        "may_write": (is_person or is_assignee) and ticket.is_open,
        "may_escalate": is_person and ticket.can_transition_to(TicketStatus.PROFESSIONAL_REVIEW_REQUIRED),
        "may_take": is_assignee and ticket.can_transition_to(TicketStatus.IN_REVIEW),
        "may_respond": is_assignee and ticket.status == TicketStatus.IN_REVIEW,
        # Distinct prefixes: three textareas on one page must not share an id, or the label of
        # the second one points at the first and a screen reader reads the wrong field.
        "message_form": forms.MessageForm(prefix="message"),
        "note_form": forms.MessageForm(prefix="note"),
        "response_form": forms.ResponseForm(prefix="response"),
        "close_form": forms.CloseForm(prefix="close"),
        "internal_visibility": MessageVisibility.INTERNAL,
    }
    return _render(
        request,
        "helpdesk/detail.html",
        context,
        _desk_crumb(),
        _crumb(ticket.reference),
    )


@helpdesk_view(methods=("POST",))
def add_message(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "change", ticket)
    form = forms.MessageForm(request.POST, prefix="message")
    if not form.is_valid():
        django_messages.error(request, _("Votre message n’a pas pu être enregistré : il est vide."))
        return _back(ticket)
    if ticket.person_id == request.user.id:
        services.add_person_message(ticket, form.cleaned_data["body"], actor=request.user, request=request)
    elif ticket.assignee_id == request.user.id and ticket.mandate_is_live:
        services.ask_clarification(ticket, form.cleaned_data["body"], actor=request.user, request=request)
    else:
        raise PermissionDenied
    django_messages.success(request, _("Votre message est enregistré."))
    return _back(ticket)


@helpdesk_view(methods=("POST",))
def escalate(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "change", ticket)
    if ticket.person_id != request.user.id:
        raise PermissionDenied
    try:
        services.request_professional_review(ticket, actor=request.user, request=request)
    except ValidationError as exc:
        django_messages.error(request, "; ".join(exc.messages))
        return _back(ticket)
    django_messages.success(
        request, _("Votre demande attend la désignation d’un professionnel. Cette étape ne dépend pas de vous.")
    )
    return _back(ticket)


# ---------------------------------------------------------------------------------------------
# The professional
# ---------------------------------------------------------------------------------------------
@helpdesk_view(active="helpdesk-queue")
def queue(request):
    if not roles.has_role(request.user, roles.PROFESSIONAL):
        raise PermissionDenied
    tickets = services.queue_for(request.user)
    context = {"tickets": tickets, "open_count": sum(1 for row in tickets if row.is_open)}
    return _render(
        request,
        "helpdesk/queue.html",
        context,
        {"label": _("Demandes qui me sont confiées"), "url": ""},
    )


@helpdesk_view(methods=("POST",))
def take(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "respond", ticket)
    try:
        services.take_in_review(ticket, actor=request.user, request=request)
    except ValidationError as exc:
        django_messages.error(request, "; ".join(exc.messages))
        return _back(ticket)
    django_messages.success(request, _("La demande est marquée « en cours d’examen »."))
    return _back(ticket)


@helpdesk_view(methods=("POST",))
def respond(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "respond", ticket)
    form = forms.ResponseForm(request.POST, prefix="response")
    if not form.is_valid():
        django_messages.error(request, _("La réponse n’a pas pu être enregistrée : elle est vide."))
        return _back(ticket)
    try:
        services.publish_response(ticket, form.cleaned_data["body"], actor=request.user, request=request)
    except ValidationError as exc:
        django_messages.error(request, "; ".join(exc.messages))
        return _back(ticket)
    django_messages.success(request, _("La réponse est transmise à la personne."))
    return _back(ticket)


@helpdesk_view(methods=("POST",))
def add_note(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "respond", ticket)
    form = forms.MessageForm(request.POST, prefix="note")
    if not form.is_valid():
        django_messages.error(request, _("La note n’a pas pu être enregistrée : elle est vide."))
        return _back(ticket)
    try:
        # ``require`` above answers «has this account the right», and grants a superadmin
        # everything by construction; ``add_internal_note`` answers «has this account the mandate»,
        # and refuses. The refusal is a domain answer and must read as one, not as a server error.
        services.add_internal_note(ticket, form.cleaned_data["body"], actor=request.user, request=request)
    except ValidationError as exc:
        django_messages.error(request, "; ".join(exc.messages))
        return _back(ticket)
    django_messages.success(request, _("Note enregistrée. Elle n’est pas visible par la personne."))
    return _back(ticket)


@helpdesk_view(methods=("POST",))
def close_request(request, uuid):
    ticket = _get(request, uuid)
    require(request.user, "change", ticket)
    form = forms.CloseForm(request.POST, prefix="close")
    reason = form.cleaned_data.get("reason", "") if form.is_valid() else ""
    try:
        services.close(ticket, actor=request.user, reason=reason, request=request)
    except ValidationError as exc:
        django_messages.error(request, "; ".join(exc.messages))
        return _back(ticket)
    django_messages.success(request, _("La demande est close."))
    return _back(ticket)


# ---------------------------------------------------------------------------------------------
# Dispatch (operator / administrator)
# ---------------------------------------------------------------------------------------------
@helpdesk_view(active="helpdesk-dispatch", methods=("GET", "HEAD", "POST"))
def dispatch(request):
    """
    The register of requests waiting for a professional.

    The rows come from ``dispatchable_by``, which defers the question: designating who should look
    at a request does not require reading it. Each row carries its own mandate form under its own
    prefix, so the page can hold twenty of them without two fields ever sharing an id.
    """
    if not roles.has_role(request.user, roles.OPERATOR, roles.ADMINISTRATOR):
        raise PermissionDenied

    bound_uuid, bound_form = None, None
    if request.method == "POST":
        ticket = _dispatch_target(request.user, request.POST.get("ticket", ""))
        require(request.user, "dispatch", ticket)
        form = forms.AssignForm(request.POST, prefix=_prefix(ticket))
        if form.is_valid():
            try:
                services.assign(
                    ticket,
                    form.cleaned_data["professional"],
                    mandate_note=form.cleaned_data["mandate_note"],
                    role_label=form.cleaned_data["role_label"],
                    valid_until=form.cleaned_data.get("valid_until"),
                    actor=request.user,
                    request=request,
                )
            except ValidationError as exc:
                django_messages.error(request, "; ".join(exc.messages))
            else:
                django_messages.success(
                    request,
                    _("La demande %(reference)s est confiée, avec son mandat.") % {"reference": ticket.reference},
                )
                return redirect("helpdesk:dispatch")
        else:
            django_messages.error(request, _("Le mandat est incomplet : la demande n’a pas été confiée."))
        bound_uuid, bound_form = ticket.uuid, form

    rows = [
        {
            "ticket": ticket,
            "form": bound_form if ticket.uuid == bound_uuid else forms.AssignForm(prefix=_prefix(ticket)),
        }
        for ticket in services.dispatch_queue(request.user)
    ]
    return _render(
        request,
        "helpdesk/dispatch.html",
        {"rows": rows},
        {"label": _("Désignation des professionnels"), "url": ""},
    )


def _dispatch_target(user, raw: str) -> HelpdeskTicket:
    """
    The posted identifier, resolved through ``dispatchable_by`` or refused.

    The parse comes first because ``filter(uuid=…)`` on a value that is not a UUID raises
    ``ValidationError`` out of the field itself, which reaches the handler as a server error: a
    hand-typed probe would learn that it had made the platform fall over, and the refusal would be
    worded differently from the one a valid-but-foreign identifier gets. Both cases raise the same
    PermissionDenied, so neither discloses anything.
    """
    try:
        wanted = uuid_lib.UUID(str(raw))
    except (AttributeError, TypeError, ValueError):
        raise PermissionDenied from None
    ticket = HelpdeskTicket.objects.dispatchable_by(user).filter(uuid=wanted).first()
    if ticket is None:
        raise PermissionDenied
    return ticket


def _prefix(ticket: HelpdeskTicket) -> str:
    """One form prefix per row, so no two fields on the page share an id."""
    return f"t{ticket.uuid.hex}"
