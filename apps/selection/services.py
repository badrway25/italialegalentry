"""
Domain services of authorised selection.

Every state change goes through this module. The views, the admin, the seeds and any future API
call the same functions, so the chain cannot be short-circuited by choosing a different entry point:

    CompanyNeed → AuthorizedActor → SelectionMandate → SelectionProcess → CaseFile/Person → AuditEvent

Refusals are exceptions, never a silently ignored no-op: a refused selection that the interface
renders as if it had happened is worse than an error message.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from audit.services import record
from cases import services as case_services
from cases.models import AssignmentRole, CaseFile, CaseStatus, ResponsibleActor
from core import clock
from core.privacy import hashed_client_ip, truncated_user_agent
from selection.models import (
    MAX_DISCLOSURE_DAYS,
    ActorOperator,
    AuthorizedActor,
    DisclosureStatus,
    EvidenceStatus,
    IdentityAccess,
    IdentityDisclosure,
    IdentityField,
    SelectionEvidence,
    SelectionMandate,
    SelectionOutcome,
    SelectionProcess,
    SelectionStage,
    SelectionStageEvent,
    stages_from,
)


class SelectionRefused(ValidationError):
    """An act the domain does not allow. Never downgrade this to a silent no-op."""


# ---------------------------------------------------------------------------------------------
# The actor
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def register_actor(
    *,
    organisation,
    actor_type: str,
    jurisdiction: str,
    authorisation_reference: str,
    valid_from: dt.date,
    valid_until: dt.date | None = None,
    authorisation_register: str = "",
    scope_note: str = "",
    by=None,
    request=None,
) -> AuthorizedActor:
    """Record an authorisation. ``full_clean`` refuses one without a reference or a jurisdiction."""
    actor = AuthorizedActor(
        organisation=organisation,
        actor_type=actor_type,
        jurisdiction=jurisdiction,
        authorisation_reference=authorisation_reference,
        authorisation_register=authorisation_register,
        valid_from=valid_from,
        valid_until=valid_until,
        scope_note=scope_note,
    )
    actor.full_clean(exclude=["uuid"])
    actor.save()
    record(
        request,
        actor=by,
        action="selection.actor.registered",
        target=actor,
        metadata={
            "organisation": organisation.pk,
            "actor_type": actor_type,
            "jurisdiction": jurisdiction,
            "valid_until": valid_until.isoformat() if valid_until else "",
        },
    )
    return actor


@transaction.atomic
def add_operator(actor: AuthorizedActor, user, *, function_note: str = "", by=None, request=None) -> ActorOperator:
    """Entitle an account to work under an authorisation, and grant it the matching role."""
    from accounts import roles

    row, created = ActorOperator.objects.get_or_create(
        actor=actor, user=user, defaults={"function_note": function_note}
    )
    if not created and row.revoked_at is not None:
        row.revoked_at = None
        row.save(update_fields=["revoked_at", "updated_at"])
    roles.assign_role(user, roles.AUTHORISED_ACTOR)
    record(
        request,
        actor=by,
        action="selection.actor.operator_added",
        target=actor,
        metadata={"operator": user.pk, "function": function_note[:120]},
    )
    return row


@transaction.atomic
def revoke_operator(row: ActorOperator, *, by=None, request=None) -> ActorOperator:
    row.revoked_at = timezone.now()
    row.save(update_fields=["revoked_at", "updated_at"])
    record(
        request,
        actor=by,
        action="selection.actor.operator_revoked",
        target=row.actor,
        metadata={"operator": row.user_id},
    )
    return row


def operator_link(user, actor: AuthorizedActor) -> ActorOperator | None:
    """The live link between ``user`` and ``actor``, or None. A lapsed authorisation returns None."""
    if not getattr(user, "is_authenticated", False):
        return None
    for row in actor.operators.all():
        if row.user_id == user.id and row.is_live:
            return row
    return None


def is_operator(user, actor: AuthorizedActor) -> bool:
    return operator_link(user, actor) is not None


def actors_of(user) -> list[AuthorizedActor]:
    """The authorisations the account may work under, today. Empty for everybody else."""
    return list(AuthorizedActor.objects.valid().filter(operators__user=user, operators__revoked_at__isnull=True))


# ---------------------------------------------------------------------------------------------
# The mandate
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def issue_mandate(
    *,
    actor: AuthorizedActor,
    company,
    need_profile: str,
    need_source: str = "companies.CompanyNeed",
    need_id: str = "",
    need_reference: str = "",
    need_sector: str = "",
    need_territory: str = "",
    need_headcount: int = 1,
    need_competences: list | None = None,
    need_language_requirement: str = "",
    need_timeframe: str = "",
    need_snapshot: dict | None = None,
    valid_until: dt.date | None = None,
    scope_note: str = "",
    by=None,
    request=None,
) -> SelectionMandate:
    """
    Entrust one company need to one authorised actor.

    An actor whose authorisation is not in force is refused HERE, not at the process: a mandate
    issued to a lapsed authorisation would be a piece of paper claiming something untrue.
    """
    if not actor.is_valid():
        raise SelectionRefused(
            _("L’autorisation de cet acteur n’est pas en vigueur : aucun mandat ne peut lui être confié.")
        )
    mandate = SelectionMandate(
        actor=actor,
        company=company,
        need_source=need_source,
        need_id=str(need_id or ""),
        need_reference=need_reference,
        need_profile=need_profile,
        need_sector=need_sector,
        need_territory=need_territory,
        need_headcount=need_headcount,
        need_competences=need_competences or [],
        need_language_requirement=need_language_requirement,
        need_timeframe=need_timeframe,
        need_snapshot=need_snapshot or {},
        valid_until=valid_until,
        scope_note=scope_note,
        issued_by=by if getattr(by, "is_authenticated", False) else None,
    )
    mandate.full_clean(exclude=["uuid", "reference"])
    mandate.save()
    record(
        request,
        actor=by,
        action="selection.mandate.issued",
        target=mandate,
        metadata={
            "actor": actor.pk,
            "company": company.pk,
            "authorisation": actor.authorisation_reference[:120],
            "need_source": need_source,
            "need_id": str(need_id or ""),
        },
    )
    return mandate


@transaction.atomic
def revoke_mandate(mandate: SelectionMandate, *, by=None, request=None) -> SelectionMandate:
    mandate.revoked_at = timezone.now()
    mandate.save(update_fields=["revoked_at", "updated_at"])
    record(request, actor=by, action="selection.mandate.revoked", target=mandate, metadata={})
    return mandate


# ---------------------------------------------------------------------------------------------
# The process
# ---------------------------------------------------------------------------------------------

#: The case states from which a selection process may be opened. ``cases.ALLOWED_TRANSITIONS``
#: declares TRAINING → SELECTION; nothing else reaches SELECTION, and this module does not invent a
#: second answer to the same question.
CASE_STATES_OPENING_SELECTION: frozenset[str] = frozenset({CaseStatus.TRAINING, CaseStatus.SELECTION})

#: The evidence every process starts with. Each line names WHO must produce it — the rule that
#: ``cases.ChecklistItem`` enforces, applied here for the same reason.
#: These three lines are written into ``SelectionEvidence`` and read on screen, so they go through
#: ``gettext`` like every other user-visible string — the same treatment ``cases.services`` gives the
#: labels it persists on a ``ChecklistItem``. ``_`` is lazy here, and ``CharField.to_python``
#: resolves the proxy at save time, so the row stores the wording in the language the process was
#: opened in rather than a hard-coded French literal that ``makemessages`` never sees.
DEFAULT_EVIDENCE: tuple[tuple[str, str, str], ...] = (
    (
        _("Attestation des compétences exigées par le besoin"),
        ResponsibleActor.AUTHORISED_ACTOR,
        _("Vérification conduite par l’acteur autorisé, sous sa responsabilité."),
    ),
    (
        _("Justificatifs de formation ou de qualification"),
        ResponsibleActor.PERSON,
        _("Documents déposés par la personne dans son dossier."),
    ),
    (
        _("Conditions du besoin confirmées par l’entreprise"),
        ResponsibleActor.COMPANY,
        _("Conditions de travail, lieu et calendrier, confirmés par écrit."),
    ),
)


@transaction.atomic
def open_process(
    *,
    mandate: SelectionMandate,
    case: CaseFile,
    operator,
    request=None,
    with_default_evidence: bool = True,
) -> SelectionProcess:
    """
    Open a selection process — the only way one comes into existence.

    Three refusals, in the domain and not in a form:

    1. no live mandate (which means no valid, unexpired authorised actor) → refused;
    2. an account that is not a live operator of that actor → refused;
    3. a case file that is not in a state from which ``cases`` declares SELECTION reachable →
       refused, with the case's own vocabulary.

    On success the actor is assigned to the case with ITS OWN authorisation reference and validity,
    and the case is moved to SELECTION through ``cases.services.transition`` — which re-checks the
    assignment. The two rules therefore cannot drift apart: there is only one of them, applied twice.
    """
    actor = mandate.actor
    if not mandate.is_live:
        raise SelectionRefused(
            _("Ce mandat n’est pas en vigueur : un processus de sélection exige un acteur autorisé valide.")
        )
    if not is_operator(operator, actor):
        raise PermissionDenied
    if case.status not in CASE_STATES_OPENING_SELECTION:
        raise SelectionRefused(
            _("Un processus de sélection s’ouvre depuis un dossier en parcours de formation (état actuel : %(state)s).")
            % {"state": case.get_status_display()}
        )
    if SelectionProcess.objects.filter(mandate=mandate, case=case).exists():
        raise SelectionRefused(_("Un processus existe déjà pour ce mandat et ce dossier."))

    process = SelectionProcess(
        mandate=mandate,
        actor=actor,
        case=case,
        stage=SelectionStage.MANDATE_CONFIRMED,
        opened_by=operator if getattr(operator, "is_authenticated", False) else None,
    )
    process.full_clean(exclude=["uuid", "reference"])
    process.save()

    # The assignment carries the actor's OWN authorisation: cases.CaseFile.has_valid_authorised_actor
    # then answers True for the same reason the process was allowed, not for a different one.
    case_services.assign(
        case,
        operator,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference=actor.authorisation_reference,
        authorisation_jurisdiction=actor.jurisdiction[:8],
        authorisation_valid_until=actor.valid_until,
        organisation=actor.organisation,
        mandate_note=_("Mandat %(ref)s — %(profile)s")
        % {"ref": mandate.reference, "profile": mandate.need_profile[:120]},
        actor=operator,
        request=request,
    )
    if case.status != CaseStatus.SELECTION:
        case_services.transition(case, CaseStatus.SELECTION, actor=operator, request=request)

    if with_default_evidence:
        for order, (requirement, responsible, detail) in enumerate(DEFAULT_EVIDENCE):
            add_evidence(
                process,
                requirement=requirement,
                responsible_actor=responsible,
                detail=detail,
                order=order,
            )

    SelectionStageEvent.objects.create(
        process=process,
        from_stage="",
        to_stage=SelectionStage.MANDATE_CONFIRMED,
        actor=actor,
        performed_by=operator if getattr(operator, "is_authenticated", False) else None,
        note=str(_("Ouverture du processus sous mandat %(ref)s.")) % {"ref": mandate.reference},
    )
    record(
        request,
        actor=operator,
        action="selection.process.opened",
        target=process,
        metadata={
            "mandate": mandate.reference,
            "case": case.reference,
            "responsible_actor": process.responsible_label[:180],
            "authorisation": actor.authorisation_reference[:120],
        },
    )
    return process


@transaction.atomic
def advance(
    process: SelectionProcess,
    target: str,
    *,
    operator,
    note: str = "",
    request=None,
) -> SelectionProcess:
    """Move the process to ``target``, or refuse. Every move writes an event AND an audit row."""
    if target not in SelectionStage.values:
        raise SelectionRefused(_("Phase inconnue."))
    if target == SelectionStage.CONCLUDED:
        raise SelectionRefused(_("La clôture passe par la fonction de clôture, qui exige une issue."))
    if not is_operator(operator, process.actor):
        raise PermissionDenied
    if not process.mandate.is_live:
        raise SelectionRefused(_("Le mandat n’est plus en vigueur : le processus ne peut plus avancer."))
    if process.is_closed:
        raise SelectionRefused(_("Un processus clos ne se rouvre pas."))
    if target == process.stage:
        return process
    if target not in stages_from(process.stage):
        raise SelectionRefused(
            _("Passage non prévu de « %(from)s » à « %(to)s ».")
            % {"from": process.get_stage_display(), "to": dict(SelectionStage.choices)[target]}
        )
    if target == SelectionStage.SUSPENDED and not note.strip():
        raise SelectionRefused(_("Une suspension se motive."))

    previous = process.stage
    process.previous_stage = previous
    process.stage = target
    process.stage_since = timezone.now()
    process.suspension_reason = note.strip()[:300] if target == SelectionStage.SUSPENDED else ""
    process.save(update_fields=["previous_stage", "stage", "stage_since", "suspension_reason", "updated_at"])

    SelectionStageEvent.objects.create(
        process=process,
        from_stage=previous,
        to_stage=target,
        actor=process.actor,
        performed_by=operator,
        note=note[:300],
    )
    record(
        request,
        actor=operator,
        action="selection.stage",
        target=process,
        metadata={
            "from": previous,
            "to": target,
            "responsible_actor": process.responsible_label[:180],
            "note": note[:300],
        },
    )
    return process


@transaction.atomic
def conclude(
    process: SelectionProcess,
    outcome: str,
    *,
    operator,
    note: str = "",
    request=None,
) -> SelectionProcess:
    """
    Close the process with an issue that describes WHAT HAPPENED, never a judgement on the person.

    The case file follows: a file referred to the authorised administrative procedure moves to
    ADMIN_PROCESS; anything else returns to TRAINING, because a person whose selection ended is
    still on their pathway. The actor's assignment is revoked and any standing identity disclosure
    ends with the process — a purpose that no longer exists cannot keep justifying an access.
    """
    if outcome not in SelectionOutcome.values:
        raise SelectionRefused(_("Issue inconnue."))
    if not is_operator(operator, process.actor):
        raise PermissionDenied
    if process.is_closed:
        raise SelectionRefused(_("Ce processus est déjà clos."))

    previous = process.stage
    process.previous_stage = previous
    process.stage = SelectionStage.CONCLUDED
    process.stage_since = timezone.now()
    process.outcome = outcome
    process.closed_at = timezone.now()
    process.closing_note = note[:300]
    process.suspension_reason = ""
    process.save(
        update_fields=[
            "previous_stage",
            "stage",
            "stage_since",
            "outcome",
            "closed_at",
            "closing_note",
            "suspension_reason",
            "updated_at",
        ]
    )
    SelectionStageEvent.objects.create(
        process=process,
        from_stage=previous,
        to_stage=SelectionStage.CONCLUDED,
        actor=process.actor,
        performed_by=operator,
        note=note[:300],
    )

    for disclosure in process.disclosures.filter(status=DisclosureStatus.GRANTED, withdrawn_at__isnull=True):
        _end_disclosure(disclosure, reason="process_concluded", by=operator, request=request)

    case = process.case
    for assignment in case.assignments.filter(
        assignee=operator, role=AssignmentRole.AUTHORISED_ACTOR, revoked_at__isnull=True
    ):
        case_services.revoke_assignment(assignment, actor=operator, request=request)

    if case.status == CaseStatus.SELECTION:
        target = CaseStatus.ADMIN_PROCESS if outcome == SelectionOutcome.REFERRED_TO_PROCEDURE else CaseStatus.TRAINING
        case_services.transition(case, target, actor=operator, request=request)

    record(
        request,
        actor=operator,
        action="selection.process.concluded",
        target=process,
        metadata={
            "outcome": outcome,
            "responsible_actor": process.responsible_label[:180],
            "case": case.reference,
        },
    )
    return process


# ---------------------------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def add_evidence(
    process: SelectionProcess,
    *,
    requirement: str,
    responsible_actor: str,
    detail: str = "",
    responsible_note: str = "",
    due_date: dt.date | None = None,
    order: int | None = None,
) -> SelectionEvidence:
    row = SelectionEvidence(
        process=process,
        requirement=requirement,
        detail=detail,
        responsible_actor=responsible_actor,
        responsible_note=responsible_note,
        due_date=due_date,
        order=order if order is not None else process.evidence.count(),
    )
    row.full_clean()
    row.save()
    return row


@transaction.atomic
def set_evidence_status(
    row: SelectionEvidence, status: str, *, operator, note: str = "", request=None
) -> SelectionEvidence:
    if status not in EvidenceStatus.values:
        raise SelectionRefused(_("État inconnu."))
    if not is_operator(operator, row.process.actor):
        raise PermissionDenied
    if row.process.is_closed:
        raise SelectionRefused(_("Un processus clos ne se modifie plus."))
    previous, row.status = row.status, status
    if note:
        row.note = note[:300]
    row.save(update_fields=["status", "note", "updated_at"])
    record(
        request,
        actor=operator,
        action="selection.evidence.status",
        target=row.process,
        metadata={
            "evidence": row.pk,
            "from": previous,
            "to": status,
            "responsible_actor": row.process.responsible_label[:180],
        },
    )
    return row


def evidence_summary(process: SelectionProcess) -> dict:
    """Counts, never an invented percentage: a meter that cannot be verified is decoration."""
    rows = list(process.evidence.all())
    applicable = [row for row in rows if row.status != EvidenceStatus.NOT_APPLICABLE]
    provided = [row for row in applicable if row.status == EvidenceStatus.PROVIDED]
    return {
        "total": len(applicable),
        "provided": len(provided),
        "open": len(applicable) - len(provided),
        "overdue": len([row for row in applicable if row.is_overdue]),
    }


# ---------------------------------------------------------------------------------------------
# Progressive disclosure of identity
# ---------------------------------------------------------------------------------------------
def _consent_text():
    """
    The exact wording the person is shown, versioned, so the record points at what they read.

    ``consents.ConsentPurpose`` does not yet carry ``identity_disclosure`` (the app is another
    lane — see the shared-file request), so the row is created with the purpose key declared in
    ``selection.models`` and its label is rendered from ``IDENTITY_CONSENT_LABEL``.
    """
    from consents.models import ConsentText
    from selection.models import IDENTITY_CONSENT_PURPOSE

    wording = (
        "J’autorise la communication de mon identité à l’entreprise nommée ci-dessus, "
        "pour la finalité indiquée et pour la durée indiquée. "
        "Je peux retirer cette autorisation à tout moment, sans avoir à me justifier."
    )
    row, _created = ConsentText.objects.get_or_create(
        purpose=IDENTITY_CONSENT_PURPOSE,
        language="fr",
        version=1,
        defaults={
            "text": wording,
            "source": "selection.services (RGPD art. 6§1 a — consentement spécifique)",
            "effective_from": clock.now(),
        },
    )
    return row


@transaction.atomic
def request_identity_disclosure(
    process: SelectionProcess,
    *,
    operator,
    purpose: str,
    fields: list[str],
    duration_days: int,
    request=None,
) -> IdentityDisclosure:
    """
    The authorised actor asks; it does NOT decide. The person decides.

    The recipient is always the company that expressed the need — a disclosure to anybody else
    would be a purpose nobody stated.
    """
    if not is_operator(operator, process.actor):
        raise PermissionDenied
    if not process.mandate.is_live:
        raise SelectionRefused(_("Le mandat n’est plus en vigueur."))
    if process.is_closed:
        raise SelectionRefused(_("Un processus clos ne demande plus rien."))
    if process.disclosures.filter(status=DisclosureStatus.REQUESTED).exists():
        raise SelectionRefused(_("Une demande est déjà en attente de la décision de la personne."))
    if process.live_disclosure() is not None:
        raise SelectionRefused(_("Une autorisation est déjà en vigueur pour ce processus."))

    disclosure = IdentityDisclosure(
        process=process,
        recipient_organisation=process.mandate.company,
        purpose=purpose,
        fields_disclosed=[key for key in fields if key in IdentityField.values],
        duration_days=duration_days,
        requested_by=operator if getattr(operator, "is_authenticated", False) else None,
    )
    disclosure.full_clean(exclude=["uuid"])
    disclosure.save()
    record(
        request,
        actor=operator,
        action="selection.identity.requested",
        target=process,
        metadata={
            "disclosure": disclosure.pk,
            "recipient": disclosure.recipient_organisation_id,
            "fields": disclosure.fields_disclosed,
            "duration_days": duration_days,
            "purpose": purpose[:200],
            "responsible_actor": process.responsible_label[:180],
        },
    )
    return disclosure


@transaction.atomic
def grant_identity_disclosure(disclosure: IdentityDisclosure, *, person, note: str = "", request=None):
    """
    The person authorises. A ``consents.ConsentRecord`` is written pointing at the exact wording
    shown, and the authorisation is given an END: ``expires_at`` is computed from the duration the
    request had to state. Nothing here is open-ended.
    """
    from consents.models import ConsentRecord
    from selection.models import IDENTITY_CONSENT_PURPOSE

    if disclosure.process.case.person_id != getattr(person, "id", None):
        raise PermissionDenied
    if disclosure.status != DisclosureStatus.REQUESTED:
        raise SelectionRefused(_("Cette demande a déjà été tranchée."))
    if not disclosure.process.mandate.is_live:
        raise SelectionRefused(_("Le mandat n’est plus en vigueur : la demande est caduque."))

    now = timezone.now()
    consent = ConsentRecord.objects.create(
        purpose=IDENTITY_CONSENT_PURPOSE,
        consent_text=_consent_text(),
        email=person.email,
        user=person,
        given_at=now,
        ip_hash=hashed_client_ip(request) if request is not None else "",
        user_agent=truncated_user_agent(request) if request is not None else "",
        language=(getattr(person, "preferred_language", "fr") or "fr").split("-")[0],
    )
    disclosure.consent = consent
    disclosure.status = DisclosureStatus.GRANTED
    disclosure.decided_at = now
    disclosure.expires_at = now + dt.timedelta(days=disclosure.duration_days)
    disclosure.decision_note = note[:300]
    disclosure.save(update_fields=["consent", "status", "decided_at", "expires_at", "decision_note", "updated_at"])
    record(
        request,
        actor=person,
        action="selection.identity.granted",
        target=disclosure.process,
        metadata={
            "disclosure": disclosure.pk,
            "recipient": disclosure.recipient_organisation_id,
            "consent": consent.pk,
            "expires_at": disclosure.expires_at.isoformat(),
            "fields": disclosure.fields_disclosed,
        },
    )
    return disclosure


@transaction.atomic
def refuse_identity_disclosure(disclosure: IdentityDisclosure, *, person, note: str = "", request=None):
    """A refusal is a decision like any other: recorded, dated, and never held against the person."""
    if disclosure.process.case.person_id != getattr(person, "id", None):
        raise PermissionDenied
    if disclosure.status != DisclosureStatus.REQUESTED:
        raise SelectionRefused(_("Cette demande a déjà été tranchée."))
    disclosure.status = DisclosureStatus.REFUSED
    disclosure.decided_at = timezone.now()
    disclosure.decision_note = note[:300]
    disclosure.save(update_fields=["status", "decided_at", "decision_note", "updated_at"])
    record(
        request,
        actor=person,
        action="selection.identity.refused",
        target=disclosure.process,
        metadata={"disclosure": disclosure.pk, "recipient": disclosure.recipient_organisation_id},
    )
    return disclosure


@transaction.atomic
def withdraw_identity_disclosure(disclosure: IdentityDisclosure, *, person, note: str = "", request=None):
    """Withdrawal is immediate and needs no justification. The consent record is withdrawn with it."""
    if disclosure.process.case.person_id != getattr(person, "id", None):
        raise PermissionDenied
    if disclosure.status != DisclosureStatus.GRANTED:
        raise SelectionRefused(_("Seule une autorisation en vigueur peut être retirée."))
    return _end_disclosure(disclosure, reason="withdrawn_by_person", by=person, note=note, request=request)


def _end_disclosure(disclosure: IdentityDisclosure, *, reason: str, by=None, note: str = "", request=None):
    from consents.services import withdraw as withdraw_consent

    now = timezone.now()
    disclosure.status = DisclosureStatus.WITHDRAWN
    disclosure.withdrawn_at = now
    disclosure.expires_at = now
    if note:
        disclosure.decision_note = note[:300]
    disclosure.save(update_fields=["status", "withdrawn_at", "expires_at", "decision_note", "updated_at"])
    if disclosure.consent is not None and disclosure.consent.is_active:
        withdraw_consent(disclosure.consent, note=reason)
    record(
        request,
        actor=by,
        action="selection.identity.withdrawn",
        target=disclosure.process,
        metadata={"disclosure": disclosure.pk, "reason": reason},
    )
    return disclosure


def read_identity(disclosure: IdentityDisclosure, *, user, request=None) -> dict[str, str] | None:
    """
    The ONE place a person's identity leaves the case file towards a company.

    Returns ``None`` — not a partial answer, not an empty dict — whenever the disclosure is not in
    force, so a caller that forgets to check still discloses nothing. When it does return, the
    access is written to ``IdentityAccess`` and to the audit trail BEFORE the caller can use it.
    """
    if not disclosure.is_active():
        return None
    organisation = disclosure.recipient_organisation
    is_recipient = organisation.memberships.filter(user=user).exists()
    is_subject = disclosure.process.case.person_id == getattr(user, "id", None)
    if not (is_recipient or is_subject):
        raise PermissionDenied

    person = disclosure.process.case.person
    available = {
        IdentityField.FULL_NAME: person.get_full_name(),
        IdentityField.CONTACT_EMAIL: person.email,
        IdentityField.PREFERRED_LANGUAGE: person.get_preferred_language_display(),
    }
    labels = dict(IdentityField.choices)
    disclosed = {str(labels[key]): available[key] for key in disclosure.fields_disclosed if key in available}

    IdentityAccess.objects.create(
        disclosure=disclosure,
        accessed_by=user if getattr(user, "is_authenticated", False) else None,
        accessed_by_organisation=organisation if is_recipient else None,
        fields_read=list(disclosure.fields_disclosed),
        purpose_at_access=disclosure.purpose[:300],
        ip_hash=hashed_client_ip(request) if request is not None else "",
    )
    record(
        request,
        actor=user,
        action="selection.identity.accessed",
        target=disclosure.process,
        metadata={
            "disclosure": disclosure.pk,
            "recipient": organisation.pk if is_recipient else None,
            "fields": list(disclosure.fields_disclosed),
        },
    )
    return disclosed


# ---------------------------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------------------------
def get_process(user, uuid_value) -> SelectionProcess:
    """Fetch a process the user may read, or raise. Authorisation is applied in the queryset."""
    process = (
        SelectionProcess.objects.readable_by(user)
        .select_related("mandate", "mandate__company", "actor", "actor__organisation", "case", "case__person")
        .filter(uuid=uuid_value)
        .first()
    )
    if process is None:
        # Deliberately indistinguishable from "does not exist": an unauthorised user must not learn
        # that the object is there.
        raise PermissionDenied
    return process


def workspace(user) -> list[SelectionProcess]:
    """The actor's workspace: ONLY the processes assigned to them, newest first."""
    return list(
        SelectionProcess.objects.for_operator(user)
        .select_related("mandate", "mandate__company", "actor", "actor__organisation", "case")
        .order_by("-opened_at")
        .distinct()
    )


@dataclass(frozen=True)
class Viewpoint:
    """What THIS account may see and do on THIS process. Deny by default: every flag starts False."""

    is_operator: bool = False
    is_subject: bool = False
    is_recipient: bool = False
    is_administrator: bool = False
    can_advance: bool = False
    can_request_identity: bool = False
    can_decide_identity: bool = False
    can_read_identity: bool = False
    next_stages: tuple = ()
    reason: str = ""


def viewpoint(user, process: SelectionProcess) -> Viewpoint:
    from accounts import roles

    operator = is_operator(user, process.actor)
    subject = process.case.person_id == getattr(user, "id", None)
    recipient = process.mandate.company.memberships.filter(user=user).exists()
    administrator = roles.has_role(user, roles.ADMINISTRATOR)
    live_mandate = process.mandate.is_live
    live_disclosure = process.live_disclosure()

    reason = ""
    if not live_mandate:
        reason = str(_("Le mandat n’est plus en vigueur : le processus est en lecture seule."))
    elif process.is_closed:
        reason = str(_("Processus clos : plus aucune action n’est possible."))

    return Viewpoint(
        is_operator=operator,
        is_subject=subject,
        is_recipient=recipient,
        is_administrator=administrator,
        can_advance=operator and live_mandate and not process.is_closed,
        can_request_identity=(
            operator
            and live_mandate
            and not process.is_closed
            and live_disclosure is None
            and not process.disclosures.filter(status=DisclosureStatus.REQUESTED).exists()
        ),
        can_decide_identity=subject,
        can_read_identity=bool(live_disclosure) and (recipient or subject),
        next_stages=(
            tuple(
                {"key": key, "label": str(dict(SelectionStage.choices)[key])}
                for key in STAGE_ORDER + (SelectionStage.SUSPENDED,)
                if key in stages_from(process.stage) and key != SelectionStage.CONCLUDED
            )
            if operator and live_mandate and not process.is_closed
            else ()
        ),
        reason=reason,
    )


@dataclass
class ProcessPage:
    """Everything one process screen needs, assembled once, in the service and not in a template."""

    process: SelectionProcess
    view: Viewpoint
    evidence: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    disclosures: list = field(default_factory=list)
    live_disclosure: object = None
    pending_disclosure: object = None
    stage_sequence: list = field(default_factory=list)


#: The stages in reading order, for the ``.sequence`` device. SUSPENDED is not a step of the path;
#: it is an interruption of it, and is shown as such.
STAGE_ORDER: tuple[str, ...] = (
    SelectionStage.MANDATE_CONFIRMED,
    SelectionStage.COMPETENCE_REVIEW,
    SelectionStage.EVIDENCE_REVIEW,
    SelectionStage.COMPANY_REVIEW,
    SelectionStage.CONCLUDED,
)


def stage_sequence(process: SelectionProcess) -> list[dict]:
    """The path, with the step reached marked by a WORD, never by a colour alone."""
    reached = {event.to_stage for event in process.events.all()}
    labels = dict(SelectionStage.choices)
    rows = []
    for key in STAGE_ORDER:
        rows.append(
            {
                "key": key,
                "label": str(labels[key]),
                "is_current": process.stage == key,
                "is_done": key in reached and process.stage != key,
                "responsible": process.responsible_label,
            }
        )
    return rows


def process_page(user, process: SelectionProcess) -> ProcessPage:
    view = viewpoint(user, process)
    disclosures = list(
        process.disclosures.select_related("recipient_organisation", "consent").order_by("-requested_at")
    )
    return ProcessPage(
        process=process,
        view=view,
        evidence=list(process.evidence.all()),
        summary=evidence_summary(process),
        events=list(process.events.select_related("actor", "actor__organisation")),
        disclosures=disclosures,
        live_disclosure=process.live_disclosure(),
        pending_disclosure=next((row for row in disclosures if row.status == DisclosureStatus.REQUESTED), None),
        stage_sequence=stage_sequence(process),
    )


def _own_disclosures(user):
    """A person's own rows — the ONE filter of the panel and of the rail's entry to it."""
    return IdentityDisclosure.objects.filter(process__case__person=user)


def has_disclosures(user) -> bool:
    """
    Whether anybody ever asked to know this person's identity. The console's rail offers «Communications
    d’identité» to those accounts only (portal.services.shell_navigation): the panel is theirs, and its history
    stays — a consent can be withdrawn at any moment.
    """
    return _own_disclosures(user).exists()


def disclosures_for_person(user) -> list[IdentityDisclosure]:
    """What a person is being asked, and what they have already authorised. Their own, only."""
    return list(
        _own_disclosures(user)
        .select_related(
            "process",
            "process__actor",
            "process__actor__organisation",
            "process__mandate",
            "recipient_organisation",
            "consent",
        )
        .order_by("-requested_at")
    )


def accesses_for(disclosure: IdentityDisclosure) -> list[IdentityAccess]:
    """Who consulted the identity, and when. The person can always read this."""
    return list(disclosure.accesses.select_related("accessed_by_organisation").order_by("-accessed_at"))


def navigation(user, active: str = "") -> list[dict]:
    """
    The console's rail on the module's pages: the one every page of «Espace réservé» draws
    (``portal.services.shell_navigation``; design V5, V5.4 plan §1.18 D06; W3-A), with «Processus
    assignés» marked. The module used to draw a rail of its own here — three rows without a glyph —
    so the navigation changed when one entered it.

    An account that is not an authorised actor is never offered the workspace: a menu item that
    answers 403 is a way of telling someone that something exists. The panel of identity disclosures
    is a person's own: the rail lists it for the account somebody has asked (``has_disclosures``) and
    marks it there; for any other account the panel's place is the module's — «Processus assignés»
    for an actor, and no row at all for an account that is none.
    """
    from portal import services as portal_services

    key = active
    if active == "workspace" or (active == "disclosures" and not has_disclosures(user)):
        key = "selection"
    return portal_services.shell_navigation(user, active=key)


def max_disclosure_days() -> int:
    return MAX_DISCLOSURE_DAYS
