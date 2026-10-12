"""
Domain services of the digital case file.

Every state change goes through this module: the views, the admin, the management commands and any
future API all call the same functions, so the invariants and the audit trail cannot be bypassed by
choosing a different entry point.

Naming follows Technical Blueprint v1.0 §11 (``open_case``, ``case_detail``, ``transition``) so that
the mapping between the document's operations and the code is obvious — see CONFLICT_REGISTER CR-02.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from audit.services import record
from cases.models import (
    ACTIVE_STATUSES,
    REQUIRES_AUTHORISED_ACTOR,
    AssessmentOutcome,
    AssignmentRole,
    CaseAssignment,
    CaseFile,
    CasePurpose,
    CaseStatus,
    ChecklistItem,
    ChecklistStatus,
    PathwayAssessment,
    transitions_from,
)

logger = logging.getLogger("ile.cases")


class TransitionRefused(ValidationError):
    """A state change the domain does not allow. Never downgrade this to a silent no-op."""


@dataclass(frozen=True)
class NextAction:
    """The single thing the person should do next. One priority, never a list of five."""

    label: str
    url_name: str = ""
    url_args: tuple = ()
    detail: str = ""
    urgency: str = "normal"  # normal | soon | overdue | blocked
    responsible_actor: str = ""
    cta_label: str = ""

    @property
    def is_for_someone_else(self) -> bool:
        return self.responsible_actor not in ("", "person")

    @property
    def url(self) -> str:
        """Resolved through core.links, so the action never points at a page a gate has closed."""
        from core.links import public_url

        return public_url(self.url_name, *self.url_args) if self.url_name else ""

    def get_responsible_display(self) -> str:
        from cases.models import ResponsibleActor

        return dict(ResponsibleActor.choices).get(self.responsible_actor, self.responsible_actor)


# ---------------------------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def open_case(person, *, purpose: str, pathway_key: str = "", request=None) -> CaseFile:
    """Create a case file in DRAFT for ``person``."""
    if purpose not in CasePurpose.values:
        raise ValidationError({"purpose": _("Finalità non riconosciuta.")})
    case = CaseFile(person=person, purpose=purpose, pathway_key=pathway_key, status=CaseStatus.DRAFT)
    case.full_clean(exclude=["reference"])
    case.save()
    record(request, action="case.opened", target=case, metadata={"purpose": purpose, "pathway": pathway_key})
    _announce(
        person,
        "CASE_OPENED",
        context={"case_reference": case.reference, "purpose": dict(CasePurpose.choices)[purpose]},
        related=case,
        dedupe_key=f"case.opened:{case.pk}",
        request=request,
    )
    return case


# ---------------------------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def transition(case: CaseFile, target: str, *, actor=None, reason: str = "", request=None) -> CaseFile:
    """
    Move ``case`` to ``target``, or refuse.

    Refusals are explicit exceptions rather than a return value, because a silently ignored
    transition would leave the interface showing a state the domain never reached.
    """
    if target not in CaseStatus.values:
        raise TransitionRefused(_("Stato non riconosciuto."))
    if case.is_read_only:
        raise TransitionRefused(_("Un fascicolo concluso non si riapre: se ne apre uno nuovo."))
    if target == case.status:
        return case
    if target not in transitions_from(case.status):
        raise TransitionRefused(
            _("Transizione non consentita da «%(from)s» a «%(to)s».")
            % {"from": case.get_status_display(), "to": dict(CaseStatus.choices)[target]}
        )
    if target in REQUIRES_AUTHORISED_ACTOR and not case.has_valid_authorised_actor():
        # CR-03: reserved activities belong to authorised parties. No actor, no selection.
        raise TransitionRefused(
            _("La fase di selezione richiede un soggetto autorizzato assegnato e con autorizzazione valida.")
        )
    if target == CaseStatus.SUSPENDED and not reason.strip():
        raise TransitionRefused(_("La sospensione richiede una motivazione."))

    previous = case.status
    case.previous_status = previous
    case.status = target
    case.status_since = timezone.now()
    if target == CaseStatus.SUSPENDED:
        case.suspension_reason = reason.strip()
    elif previous == CaseStatus.SUSPENDED:
        case.suspension_reason = ""
    if target == CaseStatus.CLOSED:
        case.closed_at = timezone.now()
    case.save(
        update_fields=["previous_status", "status", "status_since", "suspension_reason", "closed_at", "updated_at"]
    )

    record(
        request,
        actor=actor,
        action="case.transition",
        target=case,
        metadata={"from": previous, "to": target, "reason": reason[:500]},
    )
    _announce(
        case.person,
        "CASE_TRANSITIONED",
        context={
            "case_reference": case.reference,
            "status": dict(CaseStatus.choices)[target],
            "previous_status": dict(CaseStatus.choices).get(previous, previous),
        },
        related=case,
        # Keyed on the transition AND its timestamp: the same move made twice is two events, and a
        # person who watched their file go back and forth is entitled to be told both times.
        dedupe_key=f"case.transitioned:{case.pk}:{previous}->{target}:{case.status_since.isoformat()}",
        request=request,
    )
    return case


def resume(case: CaseFile, *, actor=None, request=None) -> CaseFile:
    """Leave SUSPENDED for the state the case was in before, or ORIENTED if that is unknown."""
    if case.status != CaseStatus.SUSPENDED:
        return case
    target = case.previous_status if case.previous_status in ACTIVE_STATUSES else CaseStatus.ORIENTED
    return transition(case, target, actor=actor, reason="", request=request)


# ---------------------------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def record_assessment(
    case: CaseFile,
    *,
    outcome: str,
    ruleset_version: int,
    ruleset_snapshot: dict,
    answers: dict,
    applied_rules: list | None = None,
    missing_requirements: list | None = None,
    sources: list | None = None,
    rationale: str = "",
    pathway_key: str = "",
    request=None,
) -> PathwayAssessment:
    """
    Freeze one rule-engine execution onto the case.

    ``ruleset_snapshot`` must be the whole ruleset, not a reference: reproducibility is an acceptance
    criterion and a pointer stops being reproducible the moment the rules change.
    """
    if outcome not in AssessmentOutcome.values:
        raise ValidationError({"outcome": _("Esito non riconosciuto.")})
    if not ruleset_snapshot:
        raise ValidationError({"ruleset_snapshot": _("Lo snapshot del ruleset è obbligatorio.")})

    assessment = PathwayAssessment.objects.create(
        case=case,
        purpose=case.purpose,
        outcome=outcome,
        pathway_key=pathway_key or case.pathway_key,
        ruleset_version=ruleset_version,
        ruleset_snapshot=ruleset_snapshot,
        answers=answers,
        applied_rules=applied_rules or [],
        missing_requirements=missing_requirements or [],
        sources=sources or [],
        rationale=rationale,
    )
    record(
        request,
        action="case.assessment",
        target=case,
        metadata={"outcome": outcome, "ruleset_version": ruleset_version, "assessment_id": assessment.pk},
    )
    _announce(
        case.person,
        "CASE_ASSESSED",
        context={
            "case_reference": case.reference,
            "outcome": dict(AssessmentOutcome.choices)[outcome],
            "ruleset_version": ruleset_version,
        },
        related=case,
        dedupe_key=f"case.assessed:{assessment.pk}",
        request=request,
    )

    # A STOP never advances the case: the pathway must not be presented as practicable.
    if outcome == AssessmentOutcome.STOP:
        return assessment
    if case.status == CaseStatus.DRAFT:
        transition(case, CaseStatus.ORIENTED, reason="", request=request)
    if outcome == AssessmentOutcome.REVIEW_REQUIRED and case.status == CaseStatus.ORIENTED:
        transition(case, CaseStatus.REVIEW_REQUIRED, reason="", request=request)
    return assessment


def latest_assessment(case: CaseFile) -> PathwayAssessment | None:
    return case.assessments.order_by("-assessed_at").first()


@dataclass(frozen=True)
class Reproduction:
    """
    The result of replaying a frozen assessment.

    ``matches`` is the part that makes the claim testable: replaying an outcome is only evidence if
    the replay is compared with what was recorded. A reproduction that silently differs is worse
    than none, because it looks like verification.
    """

    orientation: object
    legal_outcome: str
    outcome: str
    recorded: str

    @property
    def matches(self) -> bool:
        return self.outcome == self.recorded


def reproduce(assessment: PathwayAssessment) -> Reproduction:
    """
    Re-run the frozen snapshots against the frozen answers and return the recomputed outcome.

    This is what makes "every outcome is reproducible using the ruleset snapshot" a testable claim
    rather than a sentence in a document. Both layers are replayed from the snapshot and from nothing
    else: the questionnaire's ruleset and the legal rules that were in force on the day, neither of
    which is read back from the database, so a replay is unaffected by everything that changed since.

    Snapshots written before the legal layer existed carry the orientation spec at the top level.
    They are still replayable, and that is the point of holding the whole ruleset rather than a
    version number — so the old shape is read where it is found rather than migrated.
    """
    from orientation.engine import evaluate, spec_from_dict

    snapshot = assessment.ruleset_snapshot or {}
    orientation_snapshot = snapshot.get("orientation", snapshot)
    orientation_result = evaluate(spec_from_dict(orientation_snapshot), assessment.answers)

    legal_outcome = ""
    legal_snapshot = snapshot.get("legal")
    if legal_snapshot:
        from rules.services import replay

        legal_outcome = replay(legal_snapshot, assessment.answers)

    outcome = _stronger(_orientation_outcome(orientation_result), legal_outcome)
    return Reproduction(
        orientation=orientation_result,
        legal_outcome=legal_outcome,
        outcome=outcome,
        recorded=assessment.outcome,
    )


#: Replaying has to rank outcomes the same way recording did, or a reproduction would "fail" for a
#: reason that has nothing to do with the rules. The order is the one in ``cases.intake``.
_OUTCOME_RANK = {
    AssessmentOutcome.POSSIBLE: 0,
    AssessmentOutcome.WARNING: 1,
    AssessmentOutcome.MISSING_REQUIREMENT: 2,
    AssessmentOutcome.REVIEW_REQUIRED: 3,
    AssessmentOutcome.STOP: 4,
}


def _orientation_outcome(result) -> str:
    from cases.intake import outcome_for

    key = getattr(getattr(result, "outcome", None), "key", "")
    return outcome_for(key)


def _stronger(first: str, second: str) -> str:
    candidates = [value for value in (first, second) if value in _OUTCOME_RANK]
    if not candidates:
        return AssessmentOutcome.POSSIBLE
    return max(candidates, key=lambda value: _OUTCOME_RANK[value])


# ---------------------------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def add_checklist_item(
    case: CaseFile,
    *,
    requirement: str,
    responsible_actor: str,
    detail: str = "",
    responsible_note: str = "",
    due_date=None,
    source_title: str = "",
    source_ref: str = "",
    language: str = "fr",
    order: int | None = None,
) -> ChecklistItem:
    item = ChecklistItem(
        case=case,
        requirement=requirement,
        detail=detail,
        responsible_actor=responsible_actor,
        responsible_note=responsible_note,
        due_date=due_date,
        source_title=source_title,
        source_ref=source_ref,
        language=language,
        order=order if order is not None else case.checklist.count(),
    )
    item.full_clean()
    item.save()
    return item


@transaction.atomic
def set_checklist_status(item: ChecklistItem, status: str, *, actor=None, request=None) -> ChecklistItem:
    if status not in ChecklistStatus.values:
        raise ValidationError({"status": _("Stato non riconosciuto.")})
    previous, item.status = item.status, status
    item.save(update_fields=["status", "updated_at"])
    record(
        request,
        actor=actor,
        action="case.checklist.status",
        target=item.case,
        metadata={"item": item.pk, "from": previous, "to": status},
    )
    return item


def open_items(case: CaseFile):
    return case.checklist.filter(
        status__in=[ChecklistStatus.PENDING, ChecklistStatus.IN_PROGRESS, ChecklistStatus.BLOCKED]
    ).order_by("due_date", "order", "id")


def progress(case: CaseFile) -> dict:
    """
    Honest progress: counts, not an invented percentage.

    The client forbade meaningless meters; "4 of 11 requirements completed" is verifiable, a
    "62% complete" bar is not.
    """
    rows = list(case.checklist.all())
    applicable = [row for row in rows if row.status != ChecklistStatus.NOT_APPLICABLE]
    done = [row for row in applicable if row.status == ChecklistStatus.DONE]
    return {
        "total": len(applicable),
        "done": len(done),
        "open": len(applicable) - len(done),
        "overdue": len([row for row in applicable if row.is_overdue]),
        "blocked": len([row for row in applicable if row.status == ChecklistStatus.BLOCKED]),
    }


# ---------------------------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def assign(
    case: CaseFile,
    assignee,
    *,
    role: str,
    authorisation_reference: str = "",
    authorisation_jurisdiction: str = "",
    authorisation_valid_until=None,
    organisation=None,
    mandate_note: str = "",
    actor=None,
    request=None,
) -> CaseAssignment:
    assignment = CaseAssignment(
        case=case,
        assignee=assignee,
        role=role,
        organisation=organisation,
        authorisation_reference=authorisation_reference,
        authorisation_jurisdiction=authorisation_jurisdiction,
        authorisation_valid_until=authorisation_valid_until,
        mandate_note=mandate_note,
    )
    assignment.full_clean()
    assignment.save()
    record(
        request,
        actor=actor,
        action="case.assigned",
        target=case,
        metadata={"assignee": assignee.pk, "role": role, "authorisation": bool(authorisation_reference)},
    )
    _announce(
        assignee,
        "ASSIGNMENT_GRANTED",
        context={
            "case_reference": case.reference,
            "role": dict(AssignmentRole.choices)[role],
            "valid_until": (
                f"{authorisation_valid_until:%d/%m/%Y}" if authorisation_valid_until else str(_("sans date de fin"))
            ),
        },
        related=case,
        dedupe_key=f"assignment.granted:{assignment.pk}",
        request=request,
    )
    return assignment


@transaction.atomic
def revoke_assignment(assignment: CaseAssignment, *, actor=None, request=None) -> CaseAssignment:
    assignment.revoked_at = timezone.now()
    assignment.save(update_fields=["revoked_at", "updated_at"])
    record(
        request,
        actor=actor,
        action="case.assignment.revoked",
        target=assignment.case,
        metadata={"assignment": assignment.pk},
    )
    # The person losing the access is told. An authorisation that ends silently leaves somebody
    # believing they still hold it, which is the failure a dated mandate exists to prevent.
    _announce(
        assignment.assignee,
        "ASSIGNMENT_REVOKED",
        context={
            "case_reference": assignment.case.reference,
            "role": dict(AssignmentRole.choices)[assignment.role],
        },
        related=assignment.case,
        dedupe_key=f"assignment.revoked:{assignment.pk}",
        request=request,
    )
    return assignment


def responsible_for(case: CaseFile) -> list[CaseAssignment]:
    """Live assignments, so the interface can always name who is responsible."""
    return [row for row in case.assignments.select_related("assignee", "organisation") if row.is_live]


# ---------------------------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------------------------
def case_detail(user, uuid_value) -> CaseFile:
    """Fetch a case the user may read, or raise. Authorisation is applied in the queryset."""
    case = CaseFile.objects.readable_by(user).filter(uuid=uuid_value).first()
    if case is None:
        # Deliberately indistinguishable from "does not exist": an unauthorised user must not learn
        # that the object is there. Http404, not PermissionDenied, because a 403 page says "you may
        # not see this", which is the disclosure the whole arrangement exists to avoid.
        raise Http404
    return case


def next_action(case: CaseFile) -> NextAction | None:
    """
    The one thing to do next.

    Order of precedence: a blocking outcome, then an overdue requirement, then the nearest due
    requirement, then the first open one, then the state itself.
    """
    assessment = latest_assessment(case)
    if assessment and assessment.is_blocking:
        return NextAction(
            label=_("Consultare l'esito e le fonti"),
            detail=_("Un elemento impedisce di proseguire su questo percorso."),
            urgency="blocked",
            responsible_actor="person",
        )
    if assessment and assessment.needs_human_review and case.status == CaseStatus.REVIEW_REQUIRED:
        return NextAction(
            label=_("Richiedere una verifica professionale"),
            detail=_("La situazione richiede una valutazione da parte di un professionista."),
            urgency="soon",
            responsible_actor="person",
        )
    items = list(open_items(case))
    overdue = [row for row in items if row.is_overdue]
    if overdue:
        item = overdue[0]
        return NextAction(
            label=item.requirement,
            detail=item.detail,
            urgency="overdue",
            responsible_actor=item.responsible_actor,
        )
    dated = [row for row in items if row.due_date]
    if dated:
        item = dated[0]
        return NextAction(
            label=item.requirement, detail=item.detail, urgency="soon", responsible_actor=item.responsible_actor
        )
    if items:
        item = items[0]
        return NextAction(
            label=item.requirement, detail=item.detail, urgency="normal", responsible_actor=item.responsible_actor
        )
    if case.status == CaseStatus.DRAFT:
        return NextAction(
            label=_("Completare il questionario di orientamento"),
            url_name="orientation:start",
            urgency="normal",
            responsible_actor="person",
        )
    return None


def transitions_available(case: CaseFile, user) -> list[tuple[str, str]]:
    """
    The state changes THIS caller may actually perform on THIS case, with their labels.

    Offering a control the domain will refuse is worse than offering none: the person clicks, is
    told no, and learns that the interface does not know what the system permits. So the list is
    computed from the declared transition table and filtered by the object policy, and the same two
    checks run again inside ``transition`` — a hidden control is not a closed door.
    """
    from accounts.permissions import can

    if case.is_read_only or not can(user, "change", case):
        return []
    labels = dict(CaseStatus.choices)
    available = []
    for target in transitions_from(case.status):
        if target in REQUIRES_AUTHORISED_ACTOR and not case.has_valid_authorised_actor():
            continue
        available.append((target, str(labels[target])))
    return available


# ---------------------------------------------------------------------------------------------
# Telling the person
# ---------------------------------------------------------------------------------------------
def _announce(recipient, event_name: str, **kwargs) -> None:
    """
    Send one declared notification, and never let it break what has already happened.

    Two things are deliberate. The import is local, so ``cases`` does not depend on
    ``notifications`` at module level and either app can be read on its own. And the LABEL is passed
    rather than ``get_..._display()``: the display method is evaluated in the CALLER's language,
    which would send a French-speaking person the state of their file in Italian because an Italian
    operator moved it.

    ``notify_quietly`` isolates the write in its own savepoint. A case transition that succeeded and
    was audited must not be rolled back because an e-mail template had a typo.
    """
    try:
        from notifications import events
        from notifications.services import notify_quietly

        notify_quietly(recipient, getattr(events, event_name), **kwargs)
    except Exception:  # noqa: BLE001 - the domain change is done and audited; this is an extra
        logger.exception("notification %s could not be sent", event_name)
