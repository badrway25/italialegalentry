"""
Domain services of the digital case file.

Every state change goes through this module: the views, the admin, the management commands and any
future API all call the same functions, so the invariants and the audit trail cannot be bypassed by
choosing a different entry point.

Naming follows Technical Blueprint v1.0 §11 (``open_case``, ``case_detail``, ``transition``) so that
the mapping between the document's operations and the code is obvious — see CONFLICT_REGISTER CR-02.
"""

from __future__ import annotations

import datetime as dt
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
    """The single thing the person should do next. One priority, never a list of five.

    Design V5.4, T1 (W3-B): the action also says WHAT obligation it is about, so the dashboard, the case and the
    documents can draw the same thing — ``kind`` ("item": a checklist item · "piece": a required piece ·
    "outcome": the pre-assessment's · "orientation": the questionnaire), the obligation's ``due_date`` and
    ``state`` (the piece's ``RequirementState`` or the item's ``ChecklistStatus``), the piece's ``piece_id`` and the
    ``lang`` the obligation's own words are written in ("" when the words are the interface's).
    """

    label: str
    url_name: str = ""
    url_args: tuple = ()
    detail: str = ""
    urgency: str = "normal"  # normal | soon | overdue | blocked
    responsible_actor: str = ""
    cta_label: str = ""
    kind: str = ""
    due_date: dt.date | None = None
    state: str = ""
    piece_id: str = ""
    lang: str = ""

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


@dataclass(frozen=True)
class _Obligation:
    """One open obligation of a case file: a checklist item, or a piece the file is still waiting for (T1)."""

    kind: str  # "item" | "piece"
    label: str
    detail: str
    due_date: dt.date | None
    overdue: bool
    responsible_actor: str
    state: str
    pk: object
    lang: str

    def action(self, urgency: str) -> NextAction:
        piece = self.kind == "piece"
        return NextAction(
            label=self.label,
            detail=self.detail,
            urgency=urgency,
            responsible_actor=self.responsible_actor,
            # A piece has its own page — where it is filed, replaced or read; a checklist item has none.
            url_name="documents:requirement" if piece else "",
            url_args=(self.pk,) if piece else (),
            kind=self.kind,
            due_date=self.due_date,
            state=self.state,
            piece_id=str(self.pk) if piece else "",
            lang=self.lang,
        )

    @property
    def is_the_persons(self) -> bool:
        return self.responsible_actor == "person"


def _open_pieces(case: CaseFile, reader=None) -> list:
    """
    The pieces this file is still waiting for (``documents.models.OPEN_STATES``), in their declared order.

    Read through the documents app's own authorisation, AT QUERY TIME: with a ``reader``, the pieces that account may
    read (``DocumentRequirement.objects.readable_by``); without one, only the pieces every reader of the case may read
    — the access class CASE — so a caller that does not say who is looking never learns the title of a piece kept to
    the person and the administration. Imported late, like every other reference to a sibling app: the case file
    does not depend on the documents app at module level.
    """
    try:
        from documents.models import OPEN_STATES, AccessClass, DocumentRequirement
    except (ImportError, LookupError):  # pragma: no cover - the documents app ships with every deployment today
        return []
    pieces = DocumentRequirement.objects.filter(case=case)
    if reader is not None:
        pieces = DocumentRequirement.objects.readable_by(reader).filter(case=case)
    else:
        pieces = pieces.filter(access_class=AccessClass.CASE)
    pieces = pieces.prefetch_related("versions__document").order_by("order", "title", "pk")
    return [piece for piece in pieces if piece.derived_state() in OPEN_STATES]


def _open_obligations(case: CaseFile, reader=None) -> list[_Obligation]:
    """
    Every open obligation of the file: its open checklist items, then the pieces it is still waiting for.

    A piece that satisfies a checklist item (``DocumentRequirement.checklist_item``) stands for that item while it is
    open: the same obligation is counted — and drawn — once, as the piece, which has a page and an act.
    """
    pieces = _open_pieces(case, reader)
    met_by_a_piece = {piece.checklist_item_id for piece in pieces if piece.checklist_item_id}
    obligations = [
        _Obligation(
            kind="item",
            label=item.requirement,
            detail=item.detail,
            due_date=item.due_date,
            overdue=item.is_overdue,
            responsible_actor=item.responsible_actor,
            state=item.status,
            pk=item.pk,
            lang=item.language,
        )
        for item in open_items(case)
        if item.pk not in met_by_a_piece
    ]
    obligations += [
        _Obligation(
            kind="piece",
            label=piece.title,
            detail=piece.detail,
            due_date=piece.due_date,
            overdue=piece.is_overdue,
            responsible_actor=piece.responsible_actor,
            state=piece.derived_state(),
            pk=piece.pk,
            lang=piece.language,
        )
        for piece in pieces
    ]
    return obligations


def next_action(case: CaseFile, *, reader=None) -> NextAction | None:
    """
    The one thing to do next.

    Order of precedence: a blocking outcome, then an overdue requirement, then the nearest due
    requirement, then the first open one, then the state itself.

    Design V5.4, T1 (W3-B): ONE next action over every open obligation of the file — its checklist items AND the
    pieces it is still waiting for — on that same precedence, so the dashboard, the case and the documents name the
    same thing. A presenter change only: no rung moves and no rule, permission or state changes. Inside a rung an
    item comes before a piece on the same date, as before T1; among the obligations with no date, the first one the
    person must act on comes first («open item the person must act on», IMPLEMENTATION_PLAN.md §2 T1), and when none
    is theirs the first of anybody's, so the page can say whose hands it is in. ``reader`` is the account the action
    is shown to: the pieces it may read are the ones considered (see ``_open_pieces``).
    """
    assessment = latest_assessment(case)
    if assessment and assessment.is_blocking:
        return NextAction(
            label=_("Consultare l'esito e le fonti"),
            detail=_("Un elemento impedisce di proseguire su questo percorso."),
            urgency="blocked",
            responsible_actor="person",
            # the outcome and its sources have a page of their own: the action leads to it
            url_name="cases:assessment",
            url_args=(case.reference, assessment.pk),
            kind="outcome",
        )
    if assessment and assessment.needs_human_review and case.status == CaseStatus.REVIEW_REQUIRED:
        return NextAction(
            label=_("Richiedere una verifica professionale"),
            detail=_("La situazione richiede una valutazione da parte di un professionista."),
            urgency="soon",
            responsible_actor="person",
            kind="outcome",
        )
    obligations = _open_obligations(case, reader)
    overdue = sorted((row for row in obligations if row.overdue), key=_by_date)
    if overdue:
        return overdue[0].action("overdue")
    dated = sorted((row for row in obligations if row.due_date), key=_by_date)
    if dated:
        return dated[0].action("soon")
    if obligations:
        theirs = [row for row in obligations if row.is_the_persons]
        return (theirs or obligations)[0].action("normal")
    if case.status == CaseStatus.DRAFT:
        return NextAction(
            label=_("Completare il questionario di orientamento"),
            url_name="orientation:start",
            urgency="normal",
            responsible_actor="person",
            kind="orientation",
        )
    return None


def _by_date(row: _Obligation) -> tuple:
    """The nearest date first; on the same date a checklist item before a piece (the order before T1)."""
    return (row.due_date, 0 if row.kind == "item" else 1)


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
