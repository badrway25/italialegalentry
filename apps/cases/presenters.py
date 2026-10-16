"""
Presenters of the case file page (design V4, CREATIVE_DIRECTION.md §3.6): what the page shows
that the domain does not compute for it — the timeline of what happened, the date each step of
the journey was reached, the checklist's health strip. Pure reads over the audit trail and the
file; nothing here decides, counts a percentage, or names a person.
"""

from __future__ import annotations

from django.utils.translation import gettext_lazy as _

from audit.models import AuditEvent
from cases.models import (
    AssessmentOutcome,
    AssignmentRole,
    CaseFile,
    CaseStatus,
    ChecklistStatus,
    ResponsibleActor,
)
from core.chips import register_for

#: The audit actions a person sees on their file's timeline — the file's own events, never the
#: platform's (sign-ins, exports, consultations by a mandate are in the trail, not on the page).
TIMELINE_ACTIONS: tuple[str, ...] = (
    "case.opened",
    "case.transition",
    "case.assessment",
    "case.assigned",
    "case.assignment.revoked",
    "case.checklist.status",
)
#: The inspector shows the most recent events; the trail keeps all of them.
TIMELINE_LIMIT = 12

_TITLES = {
    "case.opened": _("Dossier ouvert"),
    "case.transition": _("Nouvel état"),
    "case.assessment": _("Pré-évaluation enregistrée"),
    "case.assigned": _("Intervenant assigné"),
    "case.assignment.revoked": _("Mandat révoqué"),
    "case.checklist.status": _("Ligne mise à jour"),
}


def _label(choices, value) -> str:
    """The translated label of an enum member, or the raw value when the trail predates the enum."""
    try:
        return str(choices(value).label)
    except ValueError:
        return str(value or "")


def events_for(case: CaseFile):
    return AuditEvent.objects.filter(
        target_type="CaseFile", target_id=str(case.pk), action__in=TIMELINE_ACTIONS
    ).order_by("created_at", "id")


def timeline(case: CaseFile, *, limit: int = TIMELINE_LIMIT) -> list[dict]:
    """
    The file's events, newest first, the latest ``limit`` of them: where the file stands now
    heads the list (the inspector that holds it scrolls inside itself, and its first row is the
    one in view).

    The actor is a TYPE, never a name: «Vous» for the person, the role held on the file for an
    assignee, the project team for anybody else. A person's file is not the place to print the
    name of the operator who touched it.
    """
    roles = {assignment.assignee_id: str(assignment.get_role_display()) for assignment in case.assignments.all()}
    rows: list[dict] = []
    for event in events_for(case).order_by("-created_at", "-id")[:limit]:
        meta = event.metadata or {}
        chip_label, chip_register, detail = "", "", ""
        if event.action == "case.transition":
            chip_label = _label(CaseStatus, meta.get("to"))
            chip_register = register_for("cases.CaseStatus", meta.get("to"))
        elif event.action == "case.checklist.status":
            chip_label = _label(ChecklistStatus, meta.get("to"))
            chip_register = register_for("cases.ChecklistStatus", meta.get("to"))
        elif event.action == "case.assessment":
            detail = _label(AssessmentOutcome, meta.get("outcome"))
        elif event.action == "case.assigned":
            detail = _label(AssignmentRole, meta.get("role"))
        if event.actor_id is None:
            actor = ""
        elif event.actor_id == case.person_id:
            actor = str(_("Vous"))
        else:
            actor = roles.get(event.actor_id) or str(ResponsibleActor.PROJECT_TEAM.label)
        rows.append(
            {
                "when": event.created_at,
                "title": str(_TITLES.get(event.action, event.action)),
                "detail": detail,
                "chip_label": chip_label,
                "chip_register": chip_register,
                "actor": actor,
            }
        )
    return rows


def journey_with_dates(case: CaseFile) -> list[dict]:
    """
    portal.services.journey_for(case), each step with the date it was reached when the trail
    knows it: the opening for the first step, the transition that produced the step's status for
    the others, the file's own ``status_since`` for the current one. A step not yet reached has
    no date — and no invented one. A file standing on a threshold (SELECTION, on threshold A)
    dates the threshold, not a step: the steps before it are reached, the step after it is not.

    A SUSPENDED or CLOSED file has no place on the line, so nothing on it is current (the header's
    chip says the state): the trail says how far it had come — the last place it held on the line,
    read from the transitions in their order — and every step up to there is behind it, dated
    where the trail knows the date. Where a suspended file waits (a held node) is the trail
    contract's (JOURNEY_SIGNATURE.md §7.3), not drawn yet.
    """
    from portal.services import JOURNEY_STEPS, journey_for, journey_place

    if case is None:
        return []
    reached: dict[str, object] = {}
    stopped_at = 0.0  # the opening: a file starts on the first step
    for event in events_for(case).filter(action__in=("case.opened", "case.transition")):
        if event.action == "case.opened":
            reached.setdefault(str(CaseStatus.DRAFT), event.created_at)
            continue
        meta = event.metadata or {}
        target = meta.get("to")
        if target:
            reached[str(target)] = event.created_at
        for status in (meta.get("from"), target):
            place = journey_place(status)
            if place is not None:
                stopped_at = place
    steps = journey_for(case, stopped_at=stopped_at)
    reached.setdefault(str(CaseStatus.DRAFT), case.created_at)
    reached.setdefault(str(case.status), case.status_since)
    for index, (status, _side, _label) in enumerate(JOURNEY_STEPS):
        step = steps[index]
        step["reached_at"] = reached.get(str(status)) if step["state"] != "upcoming" else None
        if step["threshold"] and step["threshold"]["is_current"]:
            step["threshold"]["reached_at"] = reached.get(str(case.status))
    return steps


def checklist_health(checklist: list) -> dict | None:
    """
    The checklist as the HealthStrip reads it: one segment per status that has lines, in the
    enum's order, with the status's register. ``None`` when there is nothing to draw.
    """
    rows = [item for item in checklist if item.status != ChecklistStatus.NOT_APPLICABLE]
    if not rows:
        return None
    filters = []
    for status in ChecklistStatus:
        if status == ChecklistStatus.NOT_APPLICABLE:
            continue
        count = sum(1 for item in rows if item.status == status)
        if count:
            filters.append(
                {
                    "value": status.value,
                    "label": str(status.label),
                    "count": count,
                    "register": register_for("cases.ChecklistStatus", status),
                }
            )
    return {"counts": {"total": len(rows)}, "filters": filters}
