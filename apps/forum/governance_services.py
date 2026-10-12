"""
Domain services of the Forum Permanent governance module.

Every state change of the cooperation cycle goes through this module. The views, the back-office,
a management command and any future API call the same functions, so an invariant cannot be dodged
by choosing a different door. Two consequences that are not negotiable in this codebase:

* **A view never calls ``save()`` to change a state.** It calls ``transition_proposal`` or
  ``transition_project``, which validate against the declared transition table, refuse OUT LOUD
  (an exception, never a silent no-op) and write an ``AuditEvent``.

* **A refusal is an exception, not a return value.** A transition that quietly did nothing would
  leave the screen showing a state the domain never reached — which looks like success and is
  therefore worse than an error.

Reading is symmetrical: every ``get_*`` helper goes through ``readable_by`` and raises ``Http404``
for a row the caller may not see. Not ``PermissionDenied``: a 403 on somebody else's proposal says
« this proposal exists and is not yours », which is a disclosure in itself. The reserved area
settled this question first (``portal.services.get_own_message``); the Forum follows it.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from audit.services import record
from core import gates
from forum.governance import (
    DECISION_PROPOSAL_STATUSES,
    PUBLIC_PROFILE_KEYS,
    AnnualReport,
    Commission,
    CommissionMember,
    ForumEdition,
    ForumProfile,
    ForumProject,
    ForumProposal,
    ForumRole,
    MandateRole,
    MilestoneStatus,
    MonitoringEntry,
    ProjectMilestone,
    ProjectStatus,
    ProposalStatus,
    ReportStatus,
    Table,
    _is_unrestricted,
    project_transitions_from,
    proposal_transitions_from,
)

#: The gate the whole module lives behind (G11). Closed until after the Morocco forum.
GOVERNANCE_FLAG = "virtual_forum"


def governance_enabled() -> bool:
    """
    The single read of the gate.

    Everything else in the module asks this function rather than the flag, so the day the gate gains
    a second condition — the G1 legal-pages gate that FORUM_GOVERNANCE §7 already subordinates it to
    — there is one line to change and no route that was forgotten.
    """
    return gates.virtual_forum_enabled()


class TransitionRefused(ValidationError):
    """A state change the domain does not allow. Never downgrade this to a silent no-op."""


class GovernanceRefused(ValidationError):
    """An operation the cycle does not allow (a project without an accepted proposal, …)."""


# =================================================================================================
# Capacities — WHO may ask for a transition
# =================================================================================================
#: The lifecycle table says what is possible; this one says who may ask for it. Both are declared,
#: both are read by the service, and neither is duplicated in a view or a template.
#:
#: « proposer »    the profile that wrote the proposal
#: « referent »    a live mandate of role REFERENT on the proposal's commission
#: « secretariat » a live participation profile of role SECRETARIAT on the edition
PROPOSAL_TRANSITION_CAPACITIES: dict[str, frozenset[str]] = {
    ProposalStatus.SUBMITTED: frozenset({"proposer", "secretariat"}),
    ProposalStatus.UNDER_REVIEW: frozenset({"referent", "secretariat"}),
    ProposalStatus.ACCEPTED: frozenset({"referent", "secretariat"}),
    ProposalStatus.REJECTED: frozenset({"referent", "secretariat"}),
    ProposalStatus.WITHDRAWN: frozenset({"proposer", "secretariat"}),
}

#: Mandate roles that may elaborate a proposal. An observer consults «secondo il perimetro
#: dell'accordo» (FORUM_GOVERNANCE §5) and does not table proposals: an observer who could propose
#: would be a member, and the agreement would say so.
PROPOSING_MANDATE_ROLES: frozenset[str] = frozenset({MandateRole.MEMBER, MandateRole.REFERENT})


def capacities(user, commission: Commission, proposal: ForumProposal | None = None) -> set[str]:
    """Every capacity ``user`` holds on ``commission`` right now. Empty set = no capacity at all."""
    held: set[str] = set()
    if not getattr(user, "is_authenticated", False):
        return held
    profiles = list(ForumProfile.objects.active().filter(user=user, edition_id=commission.edition_id))
    if any(profile.role == ForumRole.SECRETARIAT for profile in profiles):
        held.add("secretariat")
    if profiles:
        mandates = CommissionMember.objects.live().filter(commission=commission, profile__in=profiles)
        for mandate in mandates:
            if mandate.role == MandateRole.REFERENT:
                held.add("referent")
            if mandate.role in PROPOSING_MANDATE_ROLES:
                held.add("member")
            if mandate.role == MandateRole.OBSERVER:
                held.add("observer")
    if proposal is not None and proposal.proposer.user_id == getattr(user, "id", None):
        held.add("proposer")
    return held


def acting_profile(user, edition: ForumEdition) -> ForumProfile:
    """The caller's active profile on ``edition``, or a refusal. A lapsed profile is not a profile."""
    profile = ForumProfile.objects.active().filter(user=user, edition=edition).first()
    if profile is None:
        raise PermissionDenied
    return profile


# =================================================================================================
# Reading — authorisation is in the query, and a row you cannot see is a 404
# =================================================================================================
def participation(user) -> dict:
    """« Ma participation »: the caller's own profiles, their live mandates and nothing else."""
    profiles = list(
        ForumProfile.objects.filter(user=user).select_related("edition", "organisation").order_by("-edition__year")
    )
    rows = []
    for profile in profiles:
        rows.append(
            {
                "profile": profile,
                "edition": profile.edition,
                "mandates": list(profile.live_mandates()),
                "lapsed_mandates": [row for row in profile.mandates.all() if not row.is_live],
            }
        )
    return {
        "profiles": rows,
        "commissions": list(Commission.objects.readable_by(user).select_related("edition")),
        "open_proposals": ForumProposal.objects.readable_by(user).exclude(status__in=DECISION_PROPOSAL_STATUSES),
    }


def commissions_for(user):
    return Commission.objects.readable_by(user).select_related("edition").order_by("edition__year", "order", "key")


def get_commission(user, key: str) -> Commission:
    # A commission key is unique within an edition, not across them, so the most recent readable
    # edition wins. Deterministic beats « whichever row the database returned first ».
    commission = (
        Commission.objects.readable_by(user)
        .filter(key=key)
        .select_related("edition")
        .order_by("-edition__year")
        .first()
    )
    if commission is None:
        raise Http404
    return commission


def get_table(user, commission_key: str, table_key: str) -> Table:
    table = (
        Table.objects.readable_by(user)
        .filter(commission__key=commission_key, key=table_key)
        .select_related("commission", "commission__edition", "referent", "referent__profile")
        .order_by("-commission__edition__year")
        .first()
    )
    if table is None:
        raise Http404
    return table


def proposals_for(user):
    return ForumProposal.objects.readable_by(user).select_related("commission", "table", "proposer")


def get_proposal(user, uuid_value) -> ForumProposal:
    proposal = (
        ForumProposal.objects.readable_by(user)
        .filter(uuid=uuid_value)
        .select_related("commission", "commission__edition", "table", "proposer", "proposer__organisation")
        .first()
    )
    if proposal is None:
        raise Http404
    return proposal


def projects_for(user):
    return ForumProject.objects.readable_by(user).select_related("commission", "lead", "origin")


def get_project(user, uuid_value) -> ForumProject:
    project = (
        ForumProject.objects.readable_by(user)
        .filter(uuid=uuid_value)
        .select_related("commission", "commission__edition", "lead", "origin")
        .first()
    )
    if project is None:
        raise Http404
    return project


def get_annual_report(user, year: int | None = None) -> AnnualReport:
    reports = AnnualReport.objects.readable_by(user).select_related("edition")
    report = reports.filter(edition__year=year).first() if year else reports.first()
    if report is None:
        raise Http404
    return report


def public_profile(profile: ForumProfile) -> dict:
    """
    Everything one participant may learn about another — and the ONLY shape the templates render.

    FORUM_GOVERNANCE §5: «I profili mostrano organizzazione, categoria e interessi dichiarati, non
    dati personali». The model holds nothing else, so this function cannot leak anything else; it
    exists so that the rule is visible in the code a reviewer reads, not only in the schema.
    """
    return {
        "organisation": profile.display_label,
        "category": profile.get_category_display(),
        "interests": profile.declared_interests,
    }


def commission_members(user, commission: Commission) -> list[dict]:
    """The membership list of a commission: live mandates only, public fields only."""
    rows = []
    for mandate in (
        CommissionMember.objects.readable_by(user)
        .live()
        .filter(commission=commission)
        .select_related("profile", "profile__organisation")
    ):
        rows.append(
            {
                "role": mandate.get_role_display(),
                "valid_from": mandate.valid_from,
                "valid_until": mandate.valid_until,
                **public_profile(mandate.profile),
            }
        )
    return sorted(rows, key=lambda row: row["organisation"])


# =================================================================================================
# Mandates
# =================================================================================================
@transaction.atomic
def grant_mandate(
    commission: Commission,
    profile: ForumProfile,
    *,
    role: str = MandateRole.MEMBER,
    valid_from=None,
    valid_until=None,
    mandate_reference: str = "",
    actor=None,
    request=None,
) -> CommissionMember:
    """Seat a profile on a commission for a bounded period. The window is never implicit."""
    mandate = CommissionMember(
        commission=commission,
        profile=profile,
        role=role,
        valid_from=valid_from or timezone.localdate(),
        valid_until=valid_until,
        mandate_reference=mandate_reference,
    )
    mandate.full_clean()
    mandate.save()
    record(
        request,
        actor=actor,
        action="forum.mandate.granted",
        target=mandate,
        metadata={
            "commission": commission.key,
            "role": role,
            "from": str(mandate.valid_from),
            "until": str(mandate.valid_until or ""),
        },
    )
    return mandate


@transaction.atomic
def revoke_mandate(mandate: CommissionMember, *, actor=None, request=None) -> CommissionMember:
    mandate.revoked_at = timezone.now()
    mandate.save(update_fields=["revoked_at", "updated_at"])
    record(
        request,
        actor=actor,
        action="forum.mandate.revoked",
        target=mandate,
        metadata={"commission": mandate.commission.key, "role": mandate.role},
    )
    return mandate


# =================================================================================================
# Proposals
# =================================================================================================
@transaction.atomic
def open_proposal(
    user,
    commission: Commission,
    *,
    title_fr: str,
    body_fr: str,
    table: Table | None = None,
    request=None,
) -> ForumProposal:
    """Create a DRAFT proposal for ``commission``. Only a live member or referent may table one."""
    held = capacities(user, commission)
    if not (_is_unrestricted(user) or held & {"member", "referent", "secretariat"}):
        raise PermissionDenied
    profile = acting_profile(user, commission.edition)
    proposal = ForumProposal(
        proposer=profile,
        commission=commission,
        table=table,
        title_fr=title_fr,
        body_fr=body_fr,
        status=ProposalStatus.DRAFT,
    )
    proposal.full_clean(exclude=["reference"])
    proposal.save()
    record(
        request,
        actor=user,
        action="forum.proposal.created",
        target=proposal,
        metadata={"commission": commission.key, "table": table.key if table else ""},
    )
    return proposal


@transaction.atomic
def transition_proposal(
    proposal: ForumProposal,
    target: str,
    *,
    actor=None,
    note: str = "",
    request=None,
) -> ForumProposal:
    """
    Move ``proposal`` to ``target``, or refuse.

    The order of the checks is itself a rule: the target must exist, the edge must be declared, the
    caller must hold a capacity for it, and a decision must carry its motivation. Each refusal names
    which of the four failed, because « transition refusée » with no reason is how a workflow
    becomes folklore.
    """
    if target not in ProposalStatus.values:
        raise TransitionRefused(_("État inconnu."))
    if target == proposal.status:
        return proposal
    if target not in proposal_transitions_from(proposal.status):
        raise TransitionRefused(
            _("Transition non autorisée de « %(from)s » vers « %(to)s ».")
            % {"from": proposal.get_status_display(), "to": dict(ProposalStatus.choices)[target]}
        )
    required = PROPOSAL_TRANSITION_CAPACITIES.get(target, frozenset())
    held = capacities(actor, proposal.commission, proposal) if actor is not None else set()
    if not (_is_unrestricted(actor) or held & required):
        raise PermissionDenied
    note = note.strip()
    if target in DECISION_PROPOSAL_STATUSES and not note:
        raise TransitionRefused(_("Une décision doit être motivée : indiquez le motif de la commission."))

    previous = proposal.status
    proposal.previous_status = previous
    proposal.status = target
    proposal.status_since = timezone.now()
    if note:
        proposal.decision_note_fr = note
    if target in DECISION_PROPOSAL_STATUSES:
        proposal.decided_at = timezone.now()
    proposal.save(
        update_fields=[
            "previous_status",
            "status",
            "status_since",
            "decision_note_fr",
            "decided_at",
            "updated_at",
        ]
    )
    record(
        request,
        actor=actor,
        action="forum.proposal.transition",
        target=proposal,
        metadata={"from": previous, "to": target, "commission": proposal.commission.key, "motivated": bool(note)},
    )
    return proposal


def available_transitions(user, proposal: ForumProposal) -> list[dict]:
    """The transitions this caller may actually ask for — so a screen never offers a refusal."""
    held = capacities(user, proposal.commission, proposal)
    unrestricted = _is_unrestricted(user)
    labels = dict(ProposalStatus.choices)
    rows = []
    for target in sorted(proposal_transitions_from(proposal.status)):
        required = PROPOSAL_TRANSITION_CAPACITIES.get(target, frozenset())
        if unrestricted or held & required:
            rows.append(
                {
                    "value": target,
                    "label": labels[target],
                    "needs_note": target in DECISION_PROPOSAL_STATUSES,
                }
            )
    return rows


# =================================================================================================
# Projects
# =================================================================================================
@transaction.atomic
def promote_to_project(
    proposal: ForumProposal,
    *,
    lead: ForumProfile,
    title_fr: str = "",
    summary_fr: str = "",
    partners_fr: str = "",
    actor=None,
    request=None,
) -> ForumProject:
    """
    Turn an ACCEPTED proposal into a project.

    A proposal that has not been accepted cannot become one — FORUM_GOVERNANCE §2 makes the edge
    « una proposta accolta diventa progetto » the hinge of the whole cycle — and a project always
    names the organisation answerable for it.
    """
    if proposal.status != ProposalStatus.ACCEPTED:
        raise GovernanceRefused(_("Seule une proposition retenue peut devenir un projet."))
    if hasattr(proposal, "project"):
        raise GovernanceRefused(_("Cette proposition a déjà donné lieu à un projet."))
    project = ForumProject(
        origin=proposal,
        commission=proposal.commission,
        title_fr=title_fr or proposal.title_fr,
        summary_fr=summary_fr,
        lead=lead,
        partners_fr=partners_fr,
        status=ProjectStatus.PREPARATION,
    )
    project.full_clean()
    project.save()
    record(
        request,
        actor=actor,
        action="forum.project.created",
        target=project,
        metadata={"proposal": proposal.reference, "commission": proposal.commission.key},
    )
    return project


@transaction.atomic
def transition_project(project: ForumProject, target: str, *, actor=None, request=None) -> ForumProject:
    if target not in ProjectStatus.values:
        raise TransitionRefused(_("État inconnu."))
    if target == project.status:
        return project
    if target not in project_transitions_from(project.status):
        raise TransitionRefused(
            _("Transition non autorisée de « %(from)s » vers « %(to)s ».")
            % {"from": project.get_status_display(), "to": dict(ProjectStatus.choices)[target]}
        )
    held = capacities(actor, project.commission) if actor is not None else set()
    if not (_is_unrestricted(actor) or held & {"referent", "secretariat"}):
        raise PermissionDenied
    previous = project.status
    project.previous_status = previous
    project.status = target
    project.status_since = timezone.now()
    project.save(update_fields=["previous_status", "status", "status_since", "updated_at"])
    record(
        request,
        actor=actor,
        action="forum.project.transition",
        target=project,
        metadata={"from": previous, "to": target},
    )
    return project


@transaction.atomic
def add_milestone(
    project: ForumProject,
    *,
    title_fr: str,
    responsible: ForumProfile,
    detail_fr: str = "",
    due_on=None,
    responsible_note: str = "",
    order: int | None = None,
) -> ProjectMilestone:
    """A milestone always names who is answerable for it; the model refuses one that does not."""
    milestone = ProjectMilestone(
        project=project,
        title_fr=title_fr,
        detail_fr=detail_fr,
        due_on=due_on,
        responsible=responsible,
        responsible_note=responsible_note,
        order=order if order is not None else project.milestones.count(),
    )
    milestone.full_clean()
    milestone.save()
    return milestone


@transaction.atomic
def set_milestone_status(milestone: ProjectMilestone, status: str, *, actor=None, request=None) -> ProjectMilestone:
    if status not in MilestoneStatus.values:
        raise ValidationError({"status": _("État inconnu.")})
    previous, milestone.status = milestone.status, status
    milestone.save(update_fields=["status", "updated_at"])
    record(
        request,
        actor=actor,
        action="forum.milestone.status",
        target=milestone,
        metadata={"project": str(milestone.project.uuid), "from": previous, "to": status},
    )
    return milestone


@transaction.atomic
def record_monitoring(
    project: ForumProject,
    *,
    period_start,
    period_end,
    indicators: dict | None = None,
    note_fr: str = "",
    recorded_by: ForumProfile | None = None,
    actor=None,
    request=None,
) -> MonitoringEntry:
    entry = MonitoringEntry(
        project=project,
        period_start=period_start,
        period_end=period_end,
        indicators=indicators or {},
        note_fr=note_fr,
        recorded_by=recorded_by,
    )
    entry.full_clean()
    entry.save()
    record(
        request,
        actor=actor,
        action="forum.monitoring.recorded",
        target=entry,
        metadata={"project": str(project.uuid), "period": f"{period_start}/{period_end}"},
    )
    return entry


# =================================================================================================
# The annual report — ASSEMBLED from the data
# =================================================================================================
@dataclass(frozen=True)
class ReportSection:
    """One block of the relation. ``rows`` is always a list of flat, JSON-safe mappings."""

    key: str
    title: str
    rows: list[dict]
    summary: dict

    def as_dict(self) -> dict:
        return {"key": self.key, "title": str(self.title), "rows": self.rows, "summary": self.summary}


def _numeric_indicator_totals(entries) -> dict[str, float]:
    """
    Add up the indicators the commissions actually declared — and nothing else.

    No index, no weighting, no score. A number in this report is a sum of numbers somebody entered,
    which is the only kind of figure a governance report can defend six months later.
    """
    totals: dict[str, float] = {}
    for entry in entries:
        for key, value in (entry.indicators or {}).items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                continue
            totals[key] = totals.get(key, 0) + value
    return totals


def build_report_sections(edition: ForumEdition) -> list[dict]:
    """
    Assemble the annual relation from the edition's own data. Pure: no request, no user, no writes.

    The sections follow the cycle of FORUM_GOVERNANCE §2 in order — edition, commissions, accepted
    proposals, projects, monitoring — because the report's job is to show that the cycle turned, and
    a reader who cannot see the sequence cannot see whether it did.
    """
    commissions = list(edition.commissions.order_by("order", "key"))
    commission_ids = [commission.pk for commission in commissions]
    proposals = list(
        ForumProposal.objects.filter(commission_id__in=commission_ids).select_related("commission", "proposer")
    )
    projects = list(
        ForumProject.objects.filter(commission_id__in=commission_ids)
        .select_related("commission", "lead", "origin")
        .prefetch_related("milestones", "monitoring")
    )
    profiles = list(edition.profiles.filter(is_active=True))
    today = timezone.localdate()
    live_mandates = list(
        CommissionMember.objects.live(today).filter(commission_id__in=commission_ids).select_related("profile")
    )

    sections: list[ReportSection] = []

    sections.append(
        ReportSection(
            key="edition",
            title=_("L’édition"),
            rows=[
                {
                    "key": edition.key,
                    "year": edition.year,
                    "title": edition.title_fr,
                    "city": edition.city,
                    "status": str(edition.get_status_display()),
                    "starts_on": edition.starts_on.isoformat() if edition.starts_on else "",
                    "ends_on": edition.ends_on.isoformat() if edition.ends_on else "",
                }
            ],
            summary={
                "participants": len(profiles),
                "commissions": len(commissions),
                "mandates_live": len(live_mandates),
            },
        )
    )

    commission_rows = []
    for commission in commissions:
        own = [row for row in proposals if row.commission_id == commission.pk]
        commission_rows.append(
            {
                "key": commission.key,
                "name": commission.name_fr,
                "status": str(commission.get_status_display()),
                "members_live": len([row for row in live_mandates if row.commission_id == commission.pk]),
                "tables": commission.tables.count(),
                "proposals": len(own),
                "accepted": len([row for row in own if row.status == ProposalStatus.ACCEPTED]),
                "rejected": len([row for row in own if row.status == ProposalStatus.REJECTED]),
                "under_review": len([row for row in own if row.status == ProposalStatus.UNDER_REVIEW]),
            }
        )
    sections.append(
        ReportSection(
            key="commissions",
            title=_("Les commissions"),
            rows=commission_rows,
            summary={"total": len(commission_rows)},
        )
    )

    accepted = [row for row in proposals if row.status == ProposalStatus.ACCEPTED]
    sections.append(
        ReportSection(
            key="proposals",
            title=_("Les propositions retenues"),
            rows=[
                {
                    "reference": row.reference,
                    "title": row.title_fr,
                    "commission": row.commission.name_fr,
                    "proposer": row.proposer.display_label,
                    # Rome's date: ``decided_at`` is UTC, whose date is the day before from 00:00 to 02:00.
                    "decided_on": timezone.localdate(row.decided_at).isoformat() if row.decided_at else "",
                }
                for row in accepted
            ],
            summary={
                "submitted": len([row for row in proposals if row.status != ProposalStatus.DRAFT]),
                "accepted": len(accepted),
                "rejected": len([row for row in proposals if row.status == ProposalStatus.REJECTED]),
                "withdrawn": len([row for row in proposals if row.status == ProposalStatus.WITHDRAWN]),
            },
        )
    )

    project_rows = []
    for project in projects:
        counts = project.milestone_counts()
        project_rows.append(
            {
                "title": project.title_fr,
                "commission": project.commission.name_fr,
                "status": str(project.get_status_display()),
                "lead": project.lead.display_label,
                "partners": project.partner_lines,
                "origin": project.origin.reference,
                "milestones_done": counts["done"],
                "milestones_total": counts["total"],
                "milestones_overdue": counts["overdue"],
            }
        )
    sections.append(
        ReportSection(
            key="projects",
            title=_("Les projets"),
            rows=project_rows,
            summary={
                "total": len(project_rows),
                "running": len(
                    [row for row in projects if row.status in {ProjectStatus.PREPARATION, ProjectStatus.ACTIVE}]
                ),
                "completed": len([row for row in projects if row.status == ProjectStatus.COMPLETED]),
            },
        )
    )

    monitoring_rows = []
    all_entries = []
    for project in projects:
        entries = list(project.monitoring.all())
        all_entries.extend(entries)
        if not entries:
            continue
        latest = max(entries, key=lambda row: row.period_end)
        monitoring_rows.append(
            {
                "project": project.title_fr,
                "entries": len(entries),
                "latest_period": f"{latest.period_start.isoformat()}/{latest.period_end.isoformat()}",
                "indicators": _numeric_indicator_totals(entries),
            }
        )
    sections.append(
        ReportSection(
            key="monitoring",
            title=_("Le suivi"),
            rows=monitoring_rows,
            summary={
                "entries": len(all_entries),
                "projects_monitored": len(monitoring_rows),
                "projects_without_monitoring": len(projects) - len(monitoring_rows),
                "indicators": _numeric_indicator_totals(all_entries),
            },
        )
    )

    return [section.as_dict() for section in sections]


@transaction.atomic
def generate_annual_report(edition: ForumEdition, *, actor=None, request=None) -> AnnualReport:
    """
    Assemble (or re-assemble) the relation of ``edition``.

    A PUBLISHED relation is never regenerated. It is the record of what the Forum reported on the
    day it reported it, and a document that silently rewrites itself as the data moves is not a
    record — the same reasoning that freezes a ruleset snapshot onto a case assessment.
    """
    report, created = AnnualReport.objects.get_or_create(edition=edition)
    if report.is_published:
        raise GovernanceRefused(_("Une relation annuelle publiée ne se régénère pas : ouvrez l’édition suivante."))
    report.sections = build_report_sections(edition)
    report.generated_at = timezone.now()
    report.generated_by = (
        ForumProfile.objects.active().filter(user=actor, edition=edition).first() if actor is not None else None
    )
    report.save(update_fields=["sections", "generated_at", "generated_by", "updated_at"])
    record(
        request,
        actor=actor,
        action="forum.report.generated",
        target=report,
        metadata={"edition": edition.key, "created": created, "sections": len(report.sections)},
    )
    return report


@transaction.atomic
def publish_annual_report(report: AnnualReport, *, actor=None, request=None) -> AnnualReport:
    if report.is_published:
        return report
    if not report.sections:
        raise GovernanceRefused(_("Une relation vide ne se publie pas : assemblez-la d’abord."))
    report.status = ReportStatus.PUBLISHED
    report.published_at = timezone.now()
    report.save(update_fields=["status", "published_at", "updated_at"])
    record(
        request,
        actor=actor,
        action="forum.report.published",
        target=report,
        metadata={"edition": report.edition.key},
    )
    return report


# =================================================================================================
# Navigation of the module (§7)
# =================================================================================================
def navigation(user, active: str = "") -> list[dict]:
    """
    The platform navigation with the Forum entries appended.

    ``portal.services.navigation`` belongs to another lane and does not know about this module; its
    result is extended here rather than edited there, and an entry whose route does not resolve is
    dropped instead of rendered as a dead link.
    """
    from core.links import public_url
    from portal import services as portal_services

    items = [dict(item) for item in portal_services.navigation(user, "")]
    known = {item.get("key") for item in items}
    extra = (
        ("forum_participation", _("Forum — ma participation"), public_url("forum_governance:participation")),
        ("forum_commissions", _("Commissions"), public_url("forum_governance:commissions")),
        ("forum_proposals", _("Propositions"), public_url("forum_governance:proposals")),
        ("forum_projects", _("Projets"), public_url("forum_governance:projects")),
        ("forum_report", _("Relation annuelle"), public_url("forum_governance:annual_report")),
    )
    for key, label, url in extra:
        if key not in known and url:
            items.append({"key": key, "label": label, "url": url})
    for item in items:
        item["current"] = item.get("key") == active
    return items


def period_label(start: dt.date, end: dt.date) -> str:
    return f"{start:%d.%m.%Y} — {end:%d.%m.%Y}"


#: Re-exported so that callers do not have to reach into ``forum.governance`` for the privacy
#: contract: the keys of ``public_profile`` are the whole of what a participant may learn.
PUBLIC_PROFILE_FIELDS = PUBLIC_PROFILE_KEYS
