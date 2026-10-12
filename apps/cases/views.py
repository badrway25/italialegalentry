"""
The case file's own pages — the workspace the platform was missing.

Until now a case file existed as a model, a service layer and a band at the top of the person's
dashboard. Nobody could open one. That mattered twice over: a person could not see their own file in
full, and a professional or an operator assigned to somebody else's file had no page at all, which
made their role a row in a table rather than a job.

Four principles, each of which the code enforces rather than assumes:

1. **One queryset decides who sees what.** ``CaseFile.objects.readable_by`` answers for the list and
   for the detail, so there is no way for the two to disagree — the disagreement between a queryset
   and a policy is exactly the defect assertion §61.13 exists to catch, and it found one.

2. **A reference that is not yours answers 404**, identically to a reference nobody ever issued. A
   403 would confirm that the file exists, and the reference is ten characters long.

3. **Every change goes through a service.** No view calls ``save()`` on a state: the services hold
   the declared transition table and write the audit trail, and a view that bypassed them would
   bypass both.

4. **Who may do what depends on the object, not only on the role.** A person may tick off a
   requirement that is THEIRS to perform; the same person may not tick off "the consulate has issued
   the document", because they cannot attest it. That distinction lives in ``cases.policies``.
"""

from __future__ import annotations

import logging
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from accounts.permissions import can, require
from cases import services
from cases.models import CaseFile, ChecklistItem, ChecklistStatus

logger = logging.getLogger("ile.cases")


def case_view(methods: tuple[str, ...] = ("GET", "HEAD")):
    """login_required → never_cache → allowed methods, and the reserved area's own kill switch."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            from portal import services as portal_services

            if not portal_services.reserved_area_enabled() and not request.user.is_staff:
                return render(request, "portal/unavailable.html", {"noindex": True}, status=503)
            response = view(request, *args, **kwargs)
            response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
            return response

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _case_or_404(user, reference: str) -> CaseFile:
    """
    The case, read through the authorisation queryset.

    ``get_object_or_404`` on the filtered queryset is the whole of the access control: a reference
    belonging to somebody else never matches, so it produces the same 404 as a reference that does
    not exist. There is no branch here that could be forgotten.
    """
    return get_object_or_404(
        CaseFile.objects.readable_by(user)
        .select_related("person")
        .prefetch_related("assignments__assignee", "assignments__organisation", "checklist"),
        reference=reference.upper(),
    )


def _render(request, template: str, context: dict, *crumbs: dict):
    from portal import services as portal_services

    root = {"label": _("Espace réservé"), "url": reverse("portal:dashboard")}
    context.update(
        {
            "portal_nav": portal_services.navigation(request.user, "cases"),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "noindex": True,
        }
    )
    return render(request, template, context)


@case_view()
def index(request):
    """
    Every case file the caller may read — their own, and the ones assigned to them.

    A person normally sees one row. A professional sees the files they hold a live mandate for. The
    page is the same page, because the answer comes from the same queryset; building a separate
    "professional view" would be building a second authorisation rule.
    """
    cases = (
        CaseFile.objects.readable_by(request.user)
        .select_related("person")
        .prefetch_related("assignments__assignee")
        .order_by("-status_since", "-created_at")
    )
    rows = []
    for case in cases:
        rows.append(
            {
                "case": case,
                "is_own": case.person_id == request.user.id,
                "progress": services.progress(case),
                "next_action": services.next_action(case),
                "responsible": services.responsible_for(case),
            }
        )
    return _render(
        request,
        "cases/index.html",
        {"rows": rows, "has_foreign": any(not row["is_own"] for row in rows)},
        {"label": _("Dossiers"), "url": ""},
    )


@case_view()
def detail(request, reference: str):
    case = _case_or_404(request.user, reference)
    assessment = services.latest_assessment(case)
    # Annotate each row with what THIS caller may do to it. The template hides a control the policy
    # would refuse, and the POST view asks the policy again — a hidden control is not a closed door,
    # and a visible one that fails teaches the reader that the interface does not know the rules.
    checklist = list(case.checklist.all().order_by("order", "id"))
    for item in checklist:
        item.can_change = can(request.user, "change", item)
    # Design V4 (CREATIVE_DIRECTION.md §3.6): the page also reads the file's timeline from the audit
    # trail, dates the journey's steps from it, and carries the person's communications and dates
    # in its inspector — the same rows the dashboard shows, from the same helpers.
    from cases import presenters
    from portal import services as portal_services

    return _render(
        request,
        "cases/detail.html",
        {
            "case": case,
            "is_own": case.person_id == request.user.id,
            "progress": portal_services._with_meter(services.progress(case)),
            "next_action": services.next_action(case),
            "responsible": services.responsible_for(case),
            "checklist": checklist,
            "checklist_health": presenters.checklist_health(checklist),
            # A column of dashes says nothing: the table shows a column only when a line fills it.
            "checklist_columns": {
                "source": any(item.source_ref or item.source_title for item in checklist),
                "due": any(item.due_date for item in checklist),
            },
            "assessment": assessment,
            "assessments": case.assessments.order_by("-assessed_at")[:10],
            "can_change": can(request.user, "change", case),
            "transitions": services.transitions_available(case, request.user),
            "journey": presenters.journey_with_dates(case),
            "timeline": presenters.timeline(case),
            "messages_list": portal_services._safe_rows("messages", portal_services._dashboard_messages, request.user),
            "deadlines": portal_services._safe_rows("deadlines", portal_services._dashboard_deadlines, request.user),
            "statuses": ChecklistStatus.choices,
        },
        {"label": _("Dossiers"), "url": reverse("cases:index")},
        {"label": case.reference, "url": ""},
    )


@case_view(methods=("POST",))
def set_item_status(request, reference: str, pk: int):
    """
    Advance one requirement.

    The policy decides, not the form: a person may move an item that is theirs to perform and no
    other, because marking "the authority has issued the document" is not something an applicant can
    attest. A form that offered the choice and then refused it would be worse than one that never
    offered it, so the template hides what the policy would refuse — and the policy refuses it again
    here, because a hidden control is not a closed door.
    """
    case = _case_or_404(request.user, reference)
    item = get_object_or_404(ChecklistItem, pk=pk, case=case)
    require(request.user, "change", item)

    status = request.POST.get("status", "")
    try:
        services.set_checklist_status(item, status, actor=request.user, request=request)
    except ValidationError as exc:
        messages.error(request, _message_of(exc))
    else:
        messages.success(request, _("La ligne a été mise à jour."))
    return redirect("cases:detail", reference=case.reference)


@case_view(methods=("POST",))
def transition(request, reference: str):
    case = _case_or_404(request.user, reference)
    require(request.user, "change", case)
    target = request.POST.get("status", "")
    reason = (request.POST.get("reason") or "").strip()
    try:
        services.transition(case, target, actor=request.user, reason=reason, request=request)
    except (ValidationError, PermissionDenied) as exc:
        messages.error(request, _message_of(exc))
    else:
        messages.success(request, _("L’état du dossier a été mis à jour."))
    return redirect("cases:detail", reference=case.reference)


def _is_demonstration(assessment) -> bool:
    """
    Whether this assessment rests on rules nobody really approved.

    Read from ``ruleset_snapshot``, not from ``applied_rules`` and not from the rules as they stand
    today. ``applied_rules`` is a reduced shape — id, version, effect, message — and carries no
    approver; the whole ruleset is in the snapshot, which is also the thing that must keep telling
    the truth about THIS result after a real ruleset has replaced the demonstration one. The
    reader's question is «was this result trustworthy», not «is the engine trustworthy now».
    """
    from rules.models import is_demonstration_approval

    legal = (assessment.ruleset_snapshot or {}).get("legal") or {}
    return any(
        is_demonstration_approval(rule.get("approved_by", "")) for rule in legal.get("rules") or []
    )


@case_view()
def assessment_detail(request, reference: str, pk: int):
    """
    One frozen assessment, with the rules that produced it and the provisions behind them.

    This is the page that answers "why was I told this". It reads the SNAPSHOT, not the current
    rules: an outcome given in October must still explain itself in March, when the rules have moved
    on without it.
    """
    case = _case_or_404(request.user, reference)
    assessment = get_object_or_404(case.assessments, pk=pk)
    if not can(request.user, "view", assessment):
        raise Http404
    reproduction = None
    try:
        reproduction = services.reproduce(assessment)
    except Exception:  # noqa: BLE001 - an unreplayable snapshot must not hide the assessment itself
        logger.exception("assessment %s could not be replayed", assessment.pk)

    applied = assessment.applied_rules or []
    return _render(
        request,
        "cases/assessment.html",
        {
            "case": case,
            "assessment": assessment,
            "reproduction": reproduction,
            "applied_rules": applied,
            "sources": assessment.sources or [],
            "missing": assessment.missing_requirements or [],
            # A result page carries numbered sources, consultation dates and a reproducible replay.
            # It reads as authoritative whether or not a jurist ever saw the rules behind it, and
            # that difference has to be ON THE PAGE — not only in the database and the reports.
            "demonstration_ruleset": _is_demonstration(assessment),
        },
        {"label": _("Dossiers"), "url": reverse("cases:index")},
        {"label": case.reference, "url": reverse("cases:detail", args=[case.reference])},
        {"label": _("Pré-évaluation"), "url": ""},
    )


def _message_of(exc) -> str:
    listed = getattr(exc, "messages", None)
    return " ".join(str(m) for m in listed) if listed else str(exc)


def _journey(case: CaseFile) -> list[dict]:
    from portal import services as portal_services

    return portal_services.journey_for(case)
