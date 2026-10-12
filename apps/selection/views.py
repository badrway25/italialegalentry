"""
Authorised-selection views — thin: authentication, HTTP method, rendering.

Every rule about WHAT an account may see lives in ``selection.services`` and
``selection.policies`` (deny by default). Every rule about what it may DO lives in the services,
which raise rather than return, so a view cannot forget a check by forgetting an ``if``.

All views are ``login_required`` (an anonymous request goes to the login page whatever its method),
``never_cache`` (these pages carry personal data and must never sit in a shared cache) and
``noindex``. There is NO public entry point to this module, in any language: CR-03.
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from selection import services
from selection.models import (
    DisclosureStatus,
    EvidenceStatus,
    IdentityDisclosure,
    IdentityField,
    SelectionEvidence,
    SelectionOutcome,
    SelectionStage,
)


def selection_view(active: str, methods: tuple[str, ...] = ("GET", "HEAD")):
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            request.selection_active = active
            return view(request, *args, **kwargs)

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _render(request, template: str, context: dict, *crumbs: dict):
    root = {"label": _("Espace réservé"), "url": reverse("portal:dashboard")}
    here = {"label": _("Sélection autorisée"), "url": reverse("selection:workspace")}
    context.update(
        {
            "portal_nav": services.navigation(request.user, getattr(request, "selection_active", "")),
            "breadcrumbs": [root, here, *crumbs] if crumbs else [root, {**here, "url": ""}],
            "noindex": True,
        }
    )
    return render(request, template, context)


def _refused(request, exc: ValidationError, fallback_url: str):
    """A refusal is shown, never swallowed: the user must know the act did not happen."""
    for text in exc.messages:
        messages.error(request, text)
    return redirect(fallback_url)


# ---------------------------------------------------------------------------------------------
# The actor's workspace
# ---------------------------------------------------------------------------------------------
@selection_view("workspace")
def workspace(request):
    """
    ONLY the processes assigned to this account, under an authorisation in force.

    Never a global view, and never a searchable list of people: there is no search box on this page
    because there is nothing to search — the workspace holds the mandates entrusted to this actor.
    """
    processes = services.workspace(request.user)
    return _render(
        request,
        "selection/workspace.html",
        {
            "processes": processes,
            "actors": services.actors_of(request.user),
            "open_count": len([row for row in processes if row.is_open]),
        },
    )


@selection_view("workspace")
def process_detail(request, uuid):
    process = services.get_process(request.user, uuid)
    page = services.process_page(request.user, process)
    return _render(
        request,
        "selection/process.html",
        {
            "page": page,
            "process": process,
            "view": page.view,
            "stages": SelectionStage,
            "outcomes": SelectionOutcome.choices,
            "evidence_statuses": EvidenceStatus.choices,
            "identity_fields": IdentityField.choices,
            "max_disclosure_days": services.max_disclosure_days(),
        },
        {"label": process.reference, "url": ""},
    )


@selection_view("workspace", methods=("POST",))
def advance_stage(request, uuid):
    process = services.get_process(request.user, uuid)
    back = reverse("selection:process", args=[process.uuid])
    target = request.POST.get("stage", "")
    note = request.POST.get("note", "")[:300]
    try:
        services.advance(process, target, operator=request.user, note=note, request=request)
    except ValidationError as exc:
        return _refused(request, exc, back)
    messages.success(request, _("Phase enregistrée."))
    return redirect(back)


@selection_view("workspace", methods=("POST",))
def conclude_process(request, uuid):
    process = services.get_process(request.user, uuid)
    back = reverse("selection:process", args=[process.uuid])
    try:
        services.conclude(
            process,
            request.POST.get("outcome", ""),
            operator=request.user,
            note=request.POST.get("note", "")[:300],
            request=request,
        )
    except ValidationError as exc:
        return _refused(request, exc, back)
    messages.success(request, _("Processus clos et dossier mis à jour."))
    return redirect(back)


@selection_view("workspace", methods=("POST",))
def evidence_status(request, uuid, pk: int):
    process = services.get_process(request.user, uuid)
    back = reverse("selection:process", args=[process.uuid])
    row = SelectionEvidence.objects.filter(pk=pk, process=process).first()
    if row is None:
        raise PermissionDenied
    try:
        services.set_evidence_status(
            row,
            request.POST.get("status", ""),
            operator=request.user,
            note=request.POST.get("note", "")[:300],
            request=request,
        )
    except ValidationError as exc:
        return _refused(request, exc, back)
    messages.success(request, _("Justificatif mis à jour."))
    return redirect(back)


# ---------------------------------------------------------------------------------------------
# Progressive disclosure of identity
# ---------------------------------------------------------------------------------------------
@selection_view("workspace", methods=("POST",))
def request_identity(request, uuid):
    """The actor asks. The person decides — this view records a request, never an access."""
    process = services.get_process(request.user, uuid)
    back = reverse("selection:process", args=[process.uuid])
    try:
        duration = int(request.POST.get("duration_days", "0") or 0)
    except ValueError:
        duration = 0
    try:
        services.request_identity_disclosure(
            process,
            operator=request.user,
            purpose=request.POST.get("purpose", "")[:300],
            fields=request.POST.getlist("fields"),
            duration_days=duration,
            request=request,
        )
    except ValidationError as exc:
        return _refused(request, exc, back)
    messages.success(request, _("Demande transmise à la personne concernée. Elle seule décide."))
    return redirect(back)


@selection_view("disclosures")
def disclosures(request):
    """The person's own panel: what is asked of them, what they authorised, and who looked."""
    rows = services.disclosures_for_person(request.user)
    return _render(
        request,
        "selection/disclosures.html",
        {
            "disclosures": rows,
            "pending": [row for row in rows if row.status == DisclosureStatus.REQUESTED],
            "accesses": {row.pk: services.accesses_for(row) for row in rows},
        },
        {"label": _("Communications d’identité"), "url": ""},
    )


@selection_view("disclosures", methods=("POST",))
def decide_disclosure(request, uuid):
    disclosure = IdentityDisclosure.objects.filter(uuid=uuid, process__case__person=request.user).first()
    if disclosure is None:
        raise PermissionDenied
    back = reverse("selection:disclosures")
    decision = request.POST.get("decision", "")
    note = request.POST.get("note", "")[:300]
    try:
        if decision == "grant":
            services.grant_identity_disclosure(disclosure, person=request.user, note=note, request=request)
            messages.success(request, _("Autorisation enregistrée. Vous pouvez la retirer à tout moment."))
        elif decision == "refuse":
            services.refuse_identity_disclosure(disclosure, person=request.user, note=note, request=request)
            messages.success(request, _("Refus enregistré."))
        elif decision == "withdraw":
            services.withdraw_identity_disclosure(disclosure, person=request.user, note=note, request=request)
            messages.success(request, _("Autorisation retirée. L’entreprise ne voit plus votre identité."))
        else:
            messages.error(request, _("Décision inconnue."))
    except ValidationError as exc:
        return _refused(request, exc, back)
    return redirect(back)


@selection_view("workspace", methods=("POST",))
def identity(request, uuid):
    """
    Read an identity that a person has authorised — POST only, deliberately.

    A GET would be followed by a crawler, a prefetch or a back button, and each of those would be a
    real access to real personal data. Here one deliberate act produces exactly one recorded access:
    ``services.read_identity`` writes the ``IdentityAccess`` row and the audit event before the
    template ever sees a value.
    """
    process = services.get_process(request.user, uuid)
    disclosure = process.live_disclosure()
    if disclosure is None:
        messages.error(request, _("Aucune autorisation n’est en vigueur pour ce processus."))
        return redirect("selection:process", uuid=process.uuid)
    disclosed = services.read_identity(disclosure, user=request.user, request=request)
    if disclosed is None:
        messages.error(request, _("Aucune autorisation n’est en vigueur pour ce processus."))
        return redirect("selection:process", uuid=process.uuid)
    return _render(
        request,
        "selection/identity.html",
        {
            "process": process,
            "disclosure": disclosure,
            "disclosed": disclosed,
            "access_count": disclosure.accesses.count(),
        },
        {"label": process.reference, "url": reverse("selection:process", args=[process.uuid])},
        {"label": _("Identité communiquée"), "url": ""},
    )
