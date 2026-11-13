"""
Domain services of the digital help desk.

Every state change goes through this module — views, admin, management commands and the orientation
receiver all call the same functions — so the invariants and the audit trail cannot be bypassed by
choosing a different entry point. Naming follows ``cases.services`` (``transition``, ``assign``,
``close``) because a reader who has understood the case file should not have to learn a second
vocabulary for the same idea.

What is NOT here, and never will be: any code path that composes an answer. ``publish_response``
stores text somebody typed. There is no model, no completion, no key, no prompt (see the module
docstring of ``helpdesk.models``).

Audit metadata carries identifiers, states and lengths — never the text of a question or a reply.
The audit trail records that an exchange happened; the exchange itself stays in the exchange.
"""

from __future__ import annotations

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from audit.services import record
from helpdesk.models import (
    REQUIRES_LIVE_MANDATE,
    REQUIRES_SHARED_RESPONSE,
    STRANDED_WITHOUT_MANDATE,
    HelpdeskTicket,
    MessageKind,
    MessageVisibility,
    ResponderRole,
    TicketMessage,
    TicketOrigin,
    TicketStatus,
    transitions_from,
)


class TransitionRefused(ValidationError):
    """A state change the domain does not allow. Never downgraded to a silent no-op."""


# ---------------------------------------------------------------------------------------------
# Opening
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def open_ticket(
    person,
    *,
    subject: str,
    question: str,
    case=None,
    assessment=None,
    origin: str = TicketOrigin.PERSON,
    language: str = "fr",
    status: str = TicketStatus.INFORMATION_ONLY,
    request=None,
) -> HelpdeskTicket:
    """
    Record a request at the help desk.

    A request opens as ``INFORMATION_ONLY``: most questions are answered by what is already
    published, and starting every request at "a professional is needed" would both devalue the state
    and queue work that nobody asked for. Escalation is an explicit act — the person's
    (``request_professional_review``) or the rule engine's (``open_from_assessment``).
    """
    if status not in {TicketStatus.INFORMATION_ONLY, TicketStatus.PROFESSIONAL_REVIEW_REQUIRED}:
        raise ValidationError(
            {"status": _("Une demande s’ouvre comme information ou comme vérification professionnelle.")}
        )
    if case is not None and case.person_id != person.pk:
        # Belt and braces: a ticket must never be able to point at somebody else's case file.
        raise PermissionDenied
    ticket = HelpdeskTicket(
        person=person,
        case=case,
        assessment=assessment,
        origin=origin,
        subject=subject.strip(),
        question=question.strip(),
        language=language,
        status=status,
    )
    ticket.full_clean(exclude=["reference"])
    ticket.save()

    _write_message(
        ticket,
        author=person,
        author_role=ResponderRole.PERSON,
        kind=MessageKind.QUESTION,
        body=ticket.question,
        visibility=MessageVisibility.SHARED,
        language=language,
    )
    record(
        request,
        actor=person,
        action="helpdesk.opened",
        target=ticket,
        metadata={
            "origin": origin,
            "status": status,
            "case": ticket.case.reference if ticket.case_id else "",
            "language": language,
        },
    )
    return ticket


@transaction.atomic
def open_from_assessment(assessment, *, request=None) -> HelpdeskTicket | None:
    """
    The escalation seam: a frozen ``REVIEW_REQUIRED`` outcome becomes a request for a human.

    This is the whole point of the module. The rule engine is allowed to say «this situation needs
    someone qualified to look at it» and refuse to answer; without this function that sentence would
    be a dead end on a result page, which is exactly what the previous platform's chat box existed
    to paper over.

    Idempotent: one escalation per frozen outcome (the model's unique constraint says the same
    thing, so a race cannot produce two).
    """
    from cases.models import AssessmentOutcome

    if assessment.outcome != AssessmentOutcome.REVIEW_REQUIRED:
        return None
    existing = HelpdeskTicket.objects.filter(assessment=assessment).first()
    if existing is not None:
        return existing

    case = assessment.case
    person = case.person
    subject = _("Vérification professionnelle — dossier %(reference)s") % {"reference": case.reference}
    question = _(
        "Cette demande a été ouverte automatiquement parce que l’orientation du %(date)s a conclu "
        "qu’une vérification professionnelle est nécessaire pour ce dossier. Aucune réponse n’a été "
        "produite automatiquement. Vous pouvez ajouter ci-dessous tout élément utile à l’examen."
    ) % {"date": timezone.localtime(assessment.assessed_at).strftime("%d.%m.%Y")}

    ticket = HelpdeskTicket(
        person=person,
        case=case,
        assessment=assessment,
        origin=TicketOrigin.ASSESSMENT,
        subject=str(subject)[:200],
        question=str(question),
        language=getattr(person, "preferred_language", "fr") or "fr",
        status=TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
    )
    ticket.full_clean(exclude=["reference"])
    ticket.save()
    _write_message(
        ticket,
        author=None,
        author_role=ResponderRole.PROJECT_TEAM,
        kind=MessageKind.QUESTION,
        body=ticket.question,
        visibility=MessageVisibility.SHARED,
        language=ticket.language,
    )
    record(
        request,
        actor=None,
        action="helpdesk.opened",
        target=ticket,
        metadata={
            "origin": TicketOrigin.ASSESSMENT.value,
            "status": ticket.status,
            "case": case.reference,
            "ruleset_version": assessment.ruleset_version,
            "assessment_id": assessment.pk,
        },
    )
    return ticket


# ---------------------------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def transition(ticket: HelpdeskTicket, target: str, *, actor=None, reason: str = "", request=None) -> HelpdeskTicket:
    """Move ``ticket`` to ``target``, or refuse. Refusals are exceptions, never silent no-ops."""
    if target not in TicketStatus.values:
        raise TransitionRefused(_("État non reconnu."))
    if ticket.is_read_only:
        raise TransitionRefused(_("Une demande close n’est pas rouverte : une nouvelle demande est ouverte."))
    if target == ticket.status:
        return ticket
    if target not in transitions_from(ticket.status):
        raise TransitionRefused(
            _("Transition non autorisée de « %(from)s » à « %(to)s ».")
            % {"from": ticket.get_status_display(), "to": dict(TicketStatus.choices)[target]}
        )
    if target in REQUIRES_LIVE_MANDATE and not ticket.mandate_is_live:
        raise TransitionRefused(_("Cet état exige un professionnel désigné dont le mandat est valable."))
    if target in REQUIRES_SHARED_RESPONSE and not ticket.has_shared_response():
        # «Risposta disponibile» must mean a reply the person can read actually exists.
        raise TransitionRefused(_("On n’annonce pas une réponse qui n’a pas été écrite."))

    previous = ticket.status
    ticket.previous_status = previous
    ticket.status = target
    ticket.status_since = timezone.now()
    if target == TicketStatus.CLOSED:
        ticket.closed_at = timezone.now()
        if reason.strip():
            ticket.closure_note = reason.strip()[:300]
    ticket.save(update_fields=["previous_status", "status", "status_since", "closed_at", "closure_note", "updated_at"])
    record(
        request,
        actor=actor,
        action="helpdesk.transition",
        target=ticket,
        metadata={"from": previous, "to": target},
    )
    return ticket


def request_professional_review(ticket: HelpdeskTicket, *, actor=None, request=None) -> HelpdeskTicket:
    """The person (or the team) asks for a human. The one escalation the platform promises."""
    return transition(ticket, TicketStatus.PROFESSIONAL_REVIEW_REQUIRED, actor=actor, request=request)


@transaction.atomic
def close(ticket: HelpdeskTicket, *, actor=None, reason: str = "", request=None) -> HelpdeskTicket:
    if ticket.status == TicketStatus.CLOSED:
        return ticket
    if reason.strip():
        _write_message(
            ticket,
            author=actor,
            author_role=_role_of(actor, ticket),
            kind=MessageKind.CLOSURE,
            body=reason,
            visibility=MessageVisibility.SHARED,
            language=ticket.language,
        )
    ticket = transition(ticket, TicketStatus.CLOSED, actor=actor, reason=reason, request=request)
    record(
        request,
        actor=actor,
        action="helpdesk.closed",
        target=ticket,
        metadata={"reference": ticket.reference, "had_response": ticket.has_shared_response()},
    )
    return ticket


# ---------------------------------------------------------------------------------------------
# Mandate
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def assign(
    ticket: HelpdeskTicket,
    professional,
    *,
    mandate_note: str,
    role_label: str = "",
    valid_until=None,
    actor=None,
    request=None,
) -> HelpdeskTicket:
    """
    Put the request in the hands of a named professional, under a stated mandate.

    ``mandate_note`` is mandatory. An assignment without a mandate is a routing decision dressed up
    as an authorisation, and the whole difference between this module and a support inbox is that
    the person on the other end is answerable for something specific.
    """
    from accounts import roles

    if ticket.is_read_only:
        raise TransitionRefused(_("Une demande close ne se confie pas."))
    if not roles.has_role(professional, roles.PROFESSIONAL):
        raise ValidationError({"assignee": _("Seul un compte portant le rôle « Professionnel » peut être désigné.")})
    if not mandate_note.strip():
        raise ValidationError({"mandate_note": _("Une désignation sans contexte de mandat n’est pas un mandat.")})
    if valid_until is not None and valid_until < timezone.localdate():
        # A mandate that has already expired grants nothing, so recording one would create a state
        # the domain immediately refuses — a row that looks like an authorisation and is not.
        raise ValidationError({"valid_until": _("Un mandat ne se donne pas avec une échéance déjà passée.")})

    # Confiding a request that is already in somebody's hands ENDS that mandate, and a mandate that
    # simply ran out on its date ended without anybody acting. Both are recorded the same way, as
    # what actually happened: the request returns to «waiting for a professional» and is then
    # confided again. A trail in which one name silently replaces another has lost the fact that a
    # mandate ended, which is the only fact that matters afterwards.
    previous_assignee_id = ticket.assignee_id
    handing_over = previous_assignee_id is not None and previous_assignee_id != professional.pk
    if ticket.status in STRANDED_WITHOUT_MANDATE and (handing_over or not ticket.mandate_is_live):
        transition(ticket, TicketStatus.PROFESSIONAL_REVIEW_REQUIRED, actor=actor, request=request)

    ticket.assignee = professional
    ticket.mandate_note = mandate_note.strip()[:300]
    ticket.assignee_role_label = (role_label or str(_("Professionnel désigné")))[:120]
    ticket.mandate_valid_until = valid_until
    ticket.assigned_at = timezone.now()
    ticket.assignment_revoked_at = None
    ticket.full_clean(exclude=["reference"])
    ticket.save(
        update_fields=[
            "assignee",
            "mandate_note",
            "assignee_role_label",
            "mandate_valid_until",
            "assigned_at",
            "assignment_revoked_at",
            "updated_at",
        ]
    )
    record(
        request,
        actor=actor,
        action="helpdesk.assigned",
        target=ticket,
        metadata={
            "assignee": professional.pk,
            # Identifiers only, never names: an auditor who needs the account goes through the
            # audit trail and is authorised for it.
            "previous_assignee": previous_assignee_id or "",
            "valid_until": valid_until.isoformat() if valid_until else "",
            "mandate_stated": True,
        },
    )
    if ticket.status != TicketStatus.ASSIGNED:
        transition(ticket, TicketStatus.ASSIGNED, actor=actor, request=request)
    return ticket


@transaction.atomic
def revoke_mandate(ticket: HelpdeskTicket, *, actor=None, request=None) -> HelpdeskTicket:
    """
    End the mandate. The professional stops seeing the request the moment this is recorded.

    And the request goes BACK to waiting for a professional. Ending a mandate without moving the
    state left the request stranded: nobody could open it, nobody could find it on the designation
    register, and the person's page went on saying that the professional was examining it. Taking a
    right away has to be as complete an act as granting one.
    """
    ticket.assignment_revoked_at = timezone.now()
    ticket.save(update_fields=["assignment_revoked_at", "updated_at"])
    record(
        request,
        actor=actor,
        action="helpdesk.assignment.revoked",
        target=ticket,
        metadata={"assignee": ticket.assignee_id},
    )
    return _return_to_the_designation_register(ticket, actor=actor, request=request)


def _return_to_the_designation_register(ticket: HelpdeskTicket, *, actor=None, request=None) -> HelpdeskTicket:
    """A state that needs a live mandate, and has none, is a request waiting for a professional."""
    if ticket.status in STRANDED_WITHOUT_MANDATE and not ticket.mandate_is_live:
        return transition(ticket, TicketStatus.PROFESSIONAL_REVIEW_REQUIRED, actor=actor, request=request)
    return ticket


def require_assignee(ticket: HelpdeskTicket, actor) -> None:
    """
    Only the mandated professional acts on the professional side of the exchange.

    A right is not a mandate. ``accounts.permissions.can`` grants a superadmin every action by
    construction, so without this check the platform's own administrator could file a reply that the
    person would read as coming from «il professionista incaricato». The domain refuses it, whatever
    the screen and whatever the role.
    """
    if actor is None or ticket.assignee_id != getattr(actor, "pk", None) or not ticket.mandate_is_live:
        raise TransitionRefused(_("Seul le professionnel désigné, dont le mandat est valable, peut agir ici."))


def take_in_review(ticket: HelpdeskTicket, *, actor=None, request=None) -> HelpdeskTicket:
    """The assignee opens the file. A visible state, so the person is not left guessing."""
    require_assignee(ticket, actor)
    return transition(ticket, TicketStatus.IN_REVIEW, actor=actor, request=request)


# ---------------------------------------------------------------------------------------------
# The exchange
# ---------------------------------------------------------------------------------------------
def _role_of(actor, ticket: HelpdeskTicket) -> str:
    if actor is not None and ticket.person_id == getattr(actor, "pk", None):
        return ResponderRole.PERSON
    if actor is not None and ticket.assignee_id == getattr(actor, "pk", None):
        return ResponderRole.PROFESSIONAL
    return ResponderRole.PROJECT_TEAM


def _write_message(
    ticket: HelpdeskTicket,
    *,
    author,
    author_role: str,
    kind: str,
    body: str,
    visibility: str,
    language: str = "fr",
) -> TicketMessage:
    message = TicketMessage(
        ticket=ticket,
        author=author,
        author_role=author_role,
        kind=kind,
        visibility=visibility,
        body=body.strip(),
        language=language,
    )
    message.full_clean()
    message.save()
    return message


@transaction.atomic
def add_person_message(ticket: HelpdeskTicket, body: str, *, actor, request=None) -> TicketMessage:
    """
    The person writes. Answering a clarification hands the request back to the professional.

    The state moves with the message rather than waiting for somebody to notice it: a question that
    sits in «chiarimento necessario» after the clarification was given is a queue that lies.
    """
    if ticket.is_read_only:
        raise TransitionRefused(_("Une demande close n’accepte plus de message."))
    kind = MessageKind.CLARIFICATION if ticket.status == TicketStatus.NEEDS_CLARIFICATION else MessageKind.QUESTION
    message = _write_message(
        ticket,
        author=actor,
        author_role=ResponderRole.PERSON,
        kind=kind,
        body=body,
        visibility=MessageVisibility.SHARED,
        language=ticket.language,
    )
    record(
        request,
        actor=actor,
        action="helpdesk.message",
        target=ticket,
        metadata={"role": ResponderRole.PERSON.value, "kind": kind, "chars": len(body.strip())},
    )
    if ticket.status == TicketStatus.NEEDS_CLARIFICATION:
        target = TicketStatus.IN_REVIEW if ticket.mandate_is_live else TicketStatus.INFORMATION_ONLY
        transition(ticket, target, actor=actor, request=request)
    return message


@transaction.atomic
def ask_clarification(ticket: HelpdeskTicket, body: str, *, actor, request=None) -> TicketMessage:
    """The professional asks the person for a missing element, in writing and on the record."""
    require_assignee(ticket, actor)
    message = _write_message(
        ticket,
        author=actor,
        author_role=ResponderRole.PROFESSIONAL,
        kind=MessageKind.CLARIFICATION_REQUEST,
        body=body,
        visibility=MessageVisibility.SHARED,
        language=ticket.language,
    )
    record(
        request,
        actor=actor,
        action="helpdesk.message",
        target=ticket,
        metadata={
            "role": ResponderRole.PROFESSIONAL.value,
            "kind": MessageKind.CLARIFICATION_REQUEST.value,
            "chars": len(body.strip()),
        },
    )
    transition(ticket, TicketStatus.NEEDS_CLARIFICATION, actor=actor, request=request)
    return message


@transaction.atomic
def add_internal_note(ticket: HelpdeskTicket, body: str, *, actor, request=None) -> TicketMessage:
    """A professional note. Not visible to the person unless it is deliberately shared as a reply."""
    require_assignee(ticket, actor)
    message = _write_message(
        ticket,
        author=actor,
        author_role=ResponderRole.PROFESSIONAL,
        kind=MessageKind.NOTE,
        body=body,
        visibility=MessageVisibility.INTERNAL,
        language=ticket.language,
    )
    record(
        request,
        actor=actor,
        action="helpdesk.note",
        target=ticket,
        metadata={"kind": MessageKind.NOTE.value, "chars": len(body.strip())},
    )
    return message


@transaction.atomic
def publish_response(ticket: HelpdeskTicket, body: str, *, actor, request=None) -> TicketMessage:
    """
    The reply the person reads, with its date and the responder's ROLE.

    Nothing in this function composes anything: ``body`` is what a professional typed. The state
    only moves afterwards, so ``RESPONSE_AVAILABLE`` can never be announced before the reply exists.
    """
    if ticket.is_read_only:
        raise TransitionRefused(_("Une demande close n’accepte pas de réponse."))
    require_assignee(ticket, actor)
    message = _write_message(
        ticket,
        author=actor,
        author_role=ResponderRole.PROFESSIONAL,
        kind=MessageKind.RESPONSE,
        body=body,
        visibility=MessageVisibility.SHARED,
        language=ticket.language,
    )
    record(
        request,
        actor=actor,
        action="helpdesk.response",
        target=ticket,
        metadata={
            "role": ResponderRole.PROFESSIONAL.value,
            "chars": len(body.strip()),
            "role_label_shown": ticket.assignee_role_label,
        },
    )
    transition(ticket, TicketStatus.RESPONSE_AVAILABLE, actor=actor, request=request)
    return message


# ---------------------------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------------------------
def tickets_for(user):
    """The person's own requests, newest first."""
    return HelpdeskTicket.objects.filter(person=user).select_related("case").order_by("-created_at")


def queue_for(professional):
    """
    The professional's register: the requests mandated to them, open ones first.

    Built on ``readable_by`` rather than on a plain ``filter(assignee=…)`` so the live-mandate rule
    is applied once, in the place that also guards the detail page.
    """
    return (
        HelpdeskTicket.objects.readable_by(professional)
        .filter(assignee=professional)
        .select_related("case")
        .order_by("status_since")
    )


def dispatch_queue(user):
    """Requests waiting for a professional, for an operator or an administrator."""
    return HelpdeskTicket.objects.dispatchable_by(user).select_related("case").order_by("status_since")


def ticket_detail(user, uuid_value) -> HelpdeskTicket:
    """Fetch a request the user may read, or raise. Authorisation is applied in the queryset."""
    ticket = HelpdeskTicket.objects.readable_by(user).filter(uuid=uuid_value).first()
    if ticket is None:
        # Deliberately indistinguishable from «does not exist».
        raise PermissionDenied
    return ticket


def exchange_for(user, ticket: HelpdeskTicket):
    """The messages this user may read on this ticket, oldest first."""
    return TicketMessage.objects.readable_by(user).filter(ticket=ticket).order_by("created_at", "id")


#: What happens next, per state, said plainly and without a promise. Keyed by state so the sentence
#: is data the interface reads, not a chain of ``{% if %}`` in a template.
NEXT_STEP: dict[str, str] = {
    TicketStatus.INFORMATION_ONLY: _(
        "Votre demande est enregistrée. Si elle dépasse ce que l’orientation peut établir, "
        "vous pouvez demander une vérification professionnelle."
    ),
    TicketStatus.NEEDS_CLARIFICATION: _(
        "Un élément manque pour examiner votre demande. Répondez ci-dessous : "
        "l’examen reprend dès que votre précision est enregistrée."
    ),
    TicketStatus.PROFESSIONAL_REVIEW_REQUIRED: _(
        "Votre demande attend qu’un professionnel soit désigné. Cette étape ne dépend pas de vous."
    ),
    TicketStatus.ASSIGNED: _(
        "Un professionnel a été désigné et le mandat est enregistré. Cette étape ne dépend pas de vous."
    ),
    TicketStatus.IN_REVIEW: _("Le professionnel désigné examine votre demande. Cette étape ne dépend pas de vous."),
    TicketStatus.RESPONSE_AVAILABLE: _(
        "Une réponse écrite est disponible ci-dessous. Elle est datée et signée par une fonction, "
        "et elle n’est ni une décision ni une garantie de résultat."
    ),
    TicketStatus.CLOSED: _(
        "Cette demande est close. Elle n’est pas rouverte : une nouvelle demande peut être ouverte "
        "si votre situation évolue."
    ),
}


def next_step_for(ticket: HelpdeskTicket) -> str:
    """Keyed on the EFFECTIVE state: a sentence about work nobody is doing is worse than none."""
    return str(NEXT_STEP.get(ticket.effective_status, ""))


def waits_on_person(ticket: HelpdeskTicket) -> bool:
    """
    True when the person is the one who has to act. Used to avoid implying they are late.

    ``RESPONSE_AVAILABLE`` belongs here: once a reply is on the page, nobody else is working on the
    request — the person reads it, asks again, or closes. Without it the page announced a reply and
    said «cette étape ne dépend pas de vous» in the same breath, which is the interface contradicting
    itself about the one thing the state exists to say.
    """
    return ticket.effective_status in {
        TicketStatus.NEEDS_CLARIFICATION,
        TicketStatus.INFORMATION_ONLY,
        TicketStatus.RESPONSE_AVAILABLE,
    }
