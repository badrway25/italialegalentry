"""
Views of the Forum Permanent governance module — thin: the gate, authentication, the HTTP method,
rendering. Nothing here decides WHO may see WHAT and nothing here writes a state.

Three things every route obeys, in this order:

1. **The gate first, before authentication.** ``virtual_forum`` is closed (G11). While it is closed
   the module answers « momentanément indisponible » with HTTP 503 to EVERYONE — anonymous, person,
   staff, secretariat alike — exactly as the reserved area answers when its own kill switch is off.
   The flag is checked outside ``login_required`` on purpose: sending someone to a login page for a
   module that does not open afterwards is a lie told in the form of a redirect.

2. **Authorisation in the query.** Every list comes from a ``readable_by`` queryset and every detail
   page from a ``governance_services.get_*`` helper, which raises ``Http404`` for a row the caller
   may not see. A list and a detail page therefore always agree: a row you can see, you can open,
   and a row you cannot see does not exist as far as this module is concerned.

3. **No ``save()``.** A state change calls a service, which validates the declared transition,
   refuses out loud and writes the audit row.

Every view is ``never_cache`` (a member's workspace must never sit in a shared cache) and
``noindex``, in the header as well as in the page, because a 503 and a redirect carry no meta tag.
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from accounts.permissions import can
from forum import governance_services as services
from forum.governance import DECISION_PROPOSAL_STATUSES, MilestoneStatus, ProposalStatus
from forum.governance_forms import ProposalForm, ProposalTransitionForm

CRUMB_MAX_CHARS = 60


def _noindex(response):
    """Say « do not index » in the header too: a 503, a redirect and a HEAD carry no meta tag."""
    response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
    return response


def _unavailable(request, template: str = "forum/governance/unavailable.html"):
    return _noindex(render(request, template, {"noindex": True}, status=503))


def governance_view(active: str, methods: tuple[str, ...] = ("GET", "HEAD")):
    """
    gate (outermost) → login_required → never_cache → allowed methods → back-office kill switch.

    The gate sits outside ``login_required``, which is the one deviation from the reserved area's
    own decorator, and it is deliberate: ``portal`` puts ``login_required`` first so that an
    anonymous request always reaches the login page whatever the method. Here there is nothing
    behind the login while the flag is shut, so the honest answer to everyone is the same one.
    """

    def decorator(view):
        @wraps(view)
        def inner(request, *args, **kwargs):
            from portal import services as portal_services

            if not portal_services.reserved_area_enabled() and not request.user.is_staff:
                return _unavailable(request, "portal/unavailable.html")
            request.forum_governance_active = active
            return _noindex(view(request, *args, **kwargs))

        guarded = login_required(never_cache(require_http_methods(list(methods))(inner)))

        @wraps(view)
        def gated(request, *args, **kwargs):
            if not services.governance_enabled():
                return _unavailable(request)
            return guarded(request, *args, **kwargs)

        return gated

    return decorator


def _crumb(label) -> dict:
    return {"label": Truncator(str(label)).chars(CRUMB_MAX_CHARS), "url": ""}


def _render(request, template: str, context: dict, *crumbs: dict):
    root = {"label": _("Forum permanent"), "url": reverse("forum_governance:participation")}
    context.update(
        {
            "portal_nav": services.navigation(request.user, getattr(request, "forum_governance_active", "")),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "portal_context": _("Forum permanent"),
            "noindex": True,
        }
    )
    return render(request, template, context)


# =================================================================================================
# Ma participation
# =================================================================================================
@governance_view("forum_participation")
def participation(request):
    context = services.participation(request.user)
    context["open_proposals"] = list(context["open_proposals"][:10])
    return _render(request, "forum/governance/participation.html", context)


# =================================================================================================
# Commissions, tables
# =================================================================================================
@governance_view("forum_commissions")
def commissions(request):
    context = {"commissions": list(services.commissions_for(request.user))}
    return _render(request, "forum/governance/commissions.html", context, {"label": _("Commissions"), "url": ""})


@governance_view("forum_commissions")
def commission_detail(request, key: str):
    commission = services.get_commission(request.user, key)
    proposals = services.proposals_for(request.user).filter(commission=commission)
    context = {
        "commission": commission,
        "members": services.commission_members(request.user, commission),
        "tables": list(commission.tables.select_related("referent", "referent__profile")),
        "proposals": list(proposals[:50]),
        "projects": list(services.projects_for(request.user).filter(commission=commission)),
        "may_propose": bool(
            services.capacities(request.user, commission) & {"member", "referent", "secretariat"}
        ),
    }
    return _render(
        request,
        "forum/governance/commission_detail.html",
        context,
        {"label": _("Commissions"), "url": reverse("forum_governance:commissions")},
        _crumb(commission.name_fr),
    )


@governance_view("forum_commissions")
def table_detail(request, key: str, table_key: str):
    table = services.get_table(request.user, key, table_key)
    proposals = services.proposals_for(request.user).filter(table=table)
    context = {
        "table": table,
        "commission": table.commission,
        "referent": table.live_referent,
        "proposals": list(proposals[:50]),
    }
    return _render(
        request,
        "forum/governance/table_detail.html",
        context,
        {"label": _("Commissions"), "url": reverse("forum_governance:commissions")},
        {
            "label": Truncator(table.commission.name_fr).chars(CRUMB_MAX_CHARS),
            "url": reverse("forum_governance:commission_detail", args=[table.commission.key]),
        },
        _crumb(table.title_fr),
    )


# =================================================================================================
# Propositions
# =================================================================================================
@governance_view("forum_proposals")
def proposals(request):
    rows = list(services.proposals_for(request.user)[:100])
    context = {
        "proposals": rows,
        "mine": [row for row in rows if row.proposer.user_id == request.user.id],
        "decided_statuses": DECISION_PROPOSAL_STATUSES,
    }
    return _render(request, "forum/governance/proposals.html", context, {"label": _("Propositions"), "url": ""})


@governance_view("forum_proposals", methods=("GET", "HEAD", "POST"))
def proposal_create(request, key: str):
    commission = services.get_commission(request.user, key)
    if not services.capacities(request.user, commission) & {"member", "referent", "secretariat"}:
        # An observer consults, it does not table proposals (FORUM_GOVERNANCE §5). The caller can
        # already see this commission, so refusing out loud discloses nothing new.
        raise PermissionDenied
    form = ProposalForm(request.POST or None, commission=commission)
    if request.method == "POST" and form.is_valid():
        proposal = services.open_proposal(
            request.user,
            commission,
            title_fr=form.cleaned_data["title_fr"],
            body_fr=form.cleaned_data["body_fr"],
            table=form.cleaned_data.get("table"),
            request=request,
        )
        messages.success(request, _("Votre proposition est enregistrée comme brouillon."))
        return redirect("forum_governance:proposal_detail", uuid=proposal.uuid)
    context = {"form": form, "commission": commission}
    return _render(
        request,
        "forum/governance/proposal_form.html",
        context,
        {"label": _("Commissions"), "url": reverse("forum_governance:commissions")},
        {
            "label": Truncator(commission.name_fr).chars(CRUMB_MAX_CHARS),
            "url": reverse("forum_governance:commission_detail", args=[commission.key]),
        },
        {"label": _("Nouvelle proposition"), "url": ""},
    )


@governance_view("forum_proposals")
def proposal_detail(request, uuid):
    proposal = services.get_proposal(request.user, uuid)
    transitions = services.available_transitions(request.user, proposal)
    context = {
        "proposal": proposal,
        "proposer": services.public_profile(proposal.proposer),
        "transitions": transitions,
        "transition_form": ProposalTransitionForm(transitions=transitions) if transitions else None,
        "project": getattr(proposal, "project", None),
        "may_change": can(request.user, "change", proposal),
    }
    return _render(
        request,
        "forum/governance/proposal_detail.html",
        context,
        {"label": _("Propositions"), "url": reverse("forum_governance:proposals")},
        _crumb(proposal.title_fr),
    )


@governance_view("forum_proposals", methods=("POST",))
def proposal_transition(request, uuid):
    """
    The single door through which a proposal changes state from the interface.

    The view does not decide anything: it revalidates the choices against the service, calls the
    service and reports what the service said. A refusal is shown as a message, never swallowed.
    """
    proposal = services.get_proposal(request.user, uuid)
    transitions = services.available_transitions(request.user, proposal)
    form = ProposalTransitionForm(request.POST, transitions=transitions)
    if not form.is_valid():
        for error in form.errors.values():
            messages.error(request, error[0])
        return redirect("forum_governance:proposal_detail", uuid=proposal.uuid)
    try:
        services.transition_proposal(
            proposal,
            form.cleaned_data["target"],
            actor=request.user,
            note=form.cleaned_data["note"],
            request=request,
        )
    except services.TransitionRefused as refusal:
        messages.error(request, "; ".join(refusal.messages))
    else:
        messages.success(request, _("L’état de la proposition a été mis à jour."))
    return redirect("forum_governance:proposal_detail", uuid=proposal.uuid)


# =================================================================================================
# Projets
# =================================================================================================
@governance_view("forum_projects")
def projects(request):
    context = {"projects": list(services.projects_for(request.user)[:100])}
    return _render(request, "forum/governance/projects.html", context, {"label": _("Projets"), "url": ""})


@governance_view("forum_projects")
def project_detail(request, uuid):
    project = services.get_project(request.user, uuid)
    milestones = list(project.milestones.select_related("responsible", "responsible__organisation"))
    context = {
        "project": project,
        "counts": project.milestone_counts(),
        "milestones": milestones,
        "monitoring": list(project.monitoring.select_related("recorded_by")),
        "origin": project.origin,
        "lead": services.public_profile(project.lead),
        "open_milestone_status": MilestoneStatus.PENDING,
    }
    return _render(
        request,
        "forum/governance/project_detail.html",
        context,
        {"label": _("Projets"), "url": reverse("forum_governance:projects")},
        _crumb(project.title_fr),
    )


# =================================================================================================
# Relation annuelle
# =================================================================================================
@governance_view("forum_report")
def annual_report(request, year: int | None = None):
    report = services.get_annual_report(request.user, year)
    context = {
        "report": report,
        "sections": report.sections or [],
        "edition": report.edition,
        "is_draft": not report.is_published,
    }
    return _render(
        request,
        "forum/governance/annual_report.html",
        context,
        {"label": _("Relation annuelle"), "url": ""},
    )


#: Exported so a template or a test can name the statuses that close a proposal without importing
#: the model layer. Kept next to the views because that is where the templates read from.
DECIDED_PROPOSAL_STATUSES = DECISION_PROPOSAL_STATUSES
PROPOSAL_DRAFT = ProposalStatus.DRAFT
