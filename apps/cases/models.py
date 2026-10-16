"""
Digital case file (``fascicolo digitale``) — the object the whole platform turns around.

A ``CaseFile`` represents ONE pathway of ONE person towards ONE lawful purpose (work, study,
training, family, other). A person may hold several case files, for different purposes or at
different times. See docs/platform/CASE_LIFECYCLE.md for the model and its eleven states, and
docs/source-of-truth/PLATFORM_REQUIREMENTS_V2.md §6 for the requirements it satisfies.

Three invariants are enforced here rather than in the interface, because an interface can be
bypassed and a requirement that is only drawn on a screen is not a requirement:

1. A transition that is not declared in ``ALLOWED_TRANSITIONS`` is refused by the domain — and so is a declared one
   made by somebody ``TRANSITION_ACTORS`` (the lifecycle's «Chi può» column) does not name.
2. ``SELECTION`` is unreachable without a valid, unexpired authorised actor assigned to the case
   (Master Dossier §4: reserved activities belong to authorised parties; CR-03).
3. A checklist item cannot be saved without a responsible actor. "Who is responsible" is the
   question the client made an acceptance criterion, so an item that cannot answer it is invalid.

The case file NEVER decides anything. It records what was assessed, with which rules, what is
missing, who is responsible for each step, and what happened when.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core import clock
from core.models import TimeStampedModel


class CaseStatus(models.TextChoices):
    """The eleven states of Technical Blueprint v1.0 §8."""

    DRAFT = "draft", _("Bozza")
    ORIENTED = "oriented", _("Orientamento completato")
    REVIEW_REQUIRED = "review_required", _("Verifica professionale necessaria")
    TRAINING = "training", _("Percorso formativo attivo")
    SELECTION = "selection", _("Fase gestita da soggetto autorizzato")
    ADMIN_PROCESS = "admin_process", _("Procedura amministrativa in corso")
    PRE_DEPARTURE = "pre_departure", _("Preparazione alla partenza")
    ENTERED = "entered", _("Ingresso registrato")
    POST_ENTRY = "post_entry", _("Accompagnamento e inclusione")
    CLOSED = "closed", _("Percorso concluso")
    SUSPENDED = "suspended", _("Sospeso")


#: States from which a case is still being worked on. SUSPENDED is reachable from any of them.
ACTIVE_STATUSES: frozenset[str] = frozenset(
    {
        CaseStatus.DRAFT,
        CaseStatus.ORIENTED,
        CaseStatus.REVIEW_REQUIRED,
        CaseStatus.TRAINING,
        CaseStatus.SELECTION,
        CaseStatus.ADMIN_PROCESS,
        CaseStatus.PRE_DEPARTURE,
        CaseStatus.ENTERED,
        CaseStatus.POST_ENTRY,
    }
)

#: Declared transitions (docs/platform/CASE_LIFECYCLE.md §4). Anything absent here is refused.
#: SUSPENDED and CLOSED are added programmatically below: they are reachable from every active state.
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    CaseStatus.DRAFT: frozenset({CaseStatus.ORIENTED}),
    CaseStatus.ORIENTED: frozenset({CaseStatus.REVIEW_REQUIRED, CaseStatus.TRAINING, CaseStatus.ADMIN_PROCESS}),
    CaseStatus.REVIEW_REQUIRED: frozenset({CaseStatus.ORIENTED, CaseStatus.TRAINING, CaseStatus.ADMIN_PROCESS}),
    CaseStatus.TRAINING: frozenset({CaseStatus.SELECTION, CaseStatus.ADMIN_PROCESS, CaseStatus.ORIENTED}),
    CaseStatus.SELECTION: frozenset({CaseStatus.ADMIN_PROCESS, CaseStatus.TRAINING}),
    CaseStatus.ADMIN_PROCESS: frozenset({CaseStatus.PRE_DEPARTURE, CaseStatus.REVIEW_REQUIRED}),
    CaseStatus.PRE_DEPARTURE: frozenset({CaseStatus.ENTERED, CaseStatus.ADMIN_PROCESS}),
    CaseStatus.ENTERED: frozenset({CaseStatus.POST_ENTRY}),
    CaseStatus.POST_ENTRY: frozenset(set()),
    CaseStatus.CLOSED: frozenset(set()),
    CaseStatus.SUSPENDED: frozenset(set()),  # resolved at runtime: back to the previous state, or CLOSED
}

#: States whose entry requires an assigned, valid authorised actor (CR-03).
REQUIRES_AUTHORISED_ACTOR: frozenset[str] = frozenset({CaseStatus.SELECTION})


def transitions_from(status: str) -> frozenset[str]:
    """Every state reachable from ``status``, including the universal SUSPENDED / CLOSED exits."""
    declared = ALLOWED_TRANSITIONS.get(status, frozenset())
    if status in ACTIVE_STATUSES:
        return declared | {CaseStatus.SUSPENDED, CaseStatus.CLOSED}
    if status == CaseStatus.SUSPENDED:
        return frozenset(ACTIVE_STATUSES) | {CaseStatus.CLOSED}
    return declared


class TransitionActor:
    """
    The capacities the «Chi può» column of docs/platform/CASE_LIFECYCLE.md §4 names — identifiers, never shown.

    An assignee acts in the capacity of its ``AssignmentRole`` (the same four strings); the owner of the file as PERSON;
    an administrator as ADMINISTRATOR; the platform itself as SYSTEM — ``services.transition`` called without an actor:
    the orientation service's DRAFT → ORIENTED and ORIENTED → REVIEW_REQUIRED, the seeds.
    """

    PERSON = "person"
    PROFESSIONAL = "professional"
    AUTHORISED_ACTOR = "authorised_actor"
    TRAINING_BODY = "training_body"
    OPERATOR = "operator"
    ADMINISTRATOR = "administrator"
    SYSTEM = "system"


_WHO = TransitionActor

#: WHO may perform each transition ``ALLOWED_TRANSITIONS`` declares — the «Chi può» column of CASE_LIFECYCLE.md §4, as
#: data (finding F-7). ``services.transition`` enforces it whenever it is given an actor, and
#: ``services.transitions_available`` is computed from it, so the case page never offers a move the domain refuses.
#: A row names EVERY capacity that may make the move, the administrator included — which §4 names on none of these
#: rows, only on the three below the table (suspend, close, and lift a suspension as «superiore»): an administrator
#: neither opens nor concludes a selection (CR-03: a reserved activity), nor claims an orientation or a professional
#: review nobody ran (sec-f7 REVIEW, finding 1). The rows the graph declares and §4's table does not («not in §4»)
#: are nobody's (rule 2), the platform's own path aside. ``BEYOND_SECTION_4`` lists, each with its reason, the
#: capacities this data holds that §4 does not name — the owner's to confirm or remove (sec-f7 NOTES, Q1 and Q5).
TRANSITION_ACTORS: dict[tuple[str, str], frozenset[str]] = {
    (CaseStatus.DRAFT, CaseStatus.ORIENTED): frozenset({_WHO.SYSTEM}),
    (CaseStatus.ORIENTED, CaseStatus.REVIEW_REQUIRED): frozenset({_WHO.SYSTEM, _WHO.OPERATOR}),
    (CaseStatus.ORIENTED, CaseStatus.TRAINING): frozenset({_WHO.OPERATOR, _WHO.TRAINING_BODY}),
    (CaseStatus.ORIENTED, CaseStatus.ADMIN_PROCESS): frozenset({_WHO.OPERATOR}),
    (CaseStatus.REVIEW_REQUIRED, CaseStatus.ORIENTED): frozenset({_WHO.PROFESSIONAL}),
    (CaseStatus.REVIEW_REQUIRED, CaseStatus.TRAINING): frozenset({_WHO.PROFESSIONAL}),
    (CaseStatus.REVIEW_REQUIRED, CaseStatus.ADMIN_PROCESS): frozenset(),  # not in §4
    (CaseStatus.TRAINING, CaseStatus.SELECTION): frozenset({_WHO.AUTHORISED_ACTOR}),
    (CaseStatus.TRAINING, CaseStatus.ADMIN_PROCESS): frozenset(),  # not in §4
    (CaseStatus.TRAINING, CaseStatus.ORIENTED): frozenset(),  # not in §4
    (CaseStatus.SELECTION, CaseStatus.ADMIN_PROCESS): frozenset({_WHO.AUTHORISED_ACTOR}),
    (CaseStatus.SELECTION, CaseStatus.TRAINING): frozenset({_WHO.AUTHORISED_ACTOR, _WHO.ADMINISTRATOR}),  # not in §4
    (CaseStatus.ADMIN_PROCESS, CaseStatus.PRE_DEPARTURE): frozenset({_WHO.OPERATOR}),
    (CaseStatus.ADMIN_PROCESS, CaseStatus.REVIEW_REQUIRED): frozenset(),  # not in §4
    (CaseStatus.PRE_DEPARTURE, CaseStatus.ENTERED): frozenset({_WHO.OPERATOR}),
    (CaseStatus.PRE_DEPARTURE, CaseStatus.ADMIN_PROCESS): frozenset(),  # not in §4
    (CaseStatus.ENTERED, CaseStatus.POST_ENTRY): frozenset({_WHO.SYSTEM, _WHO.ADMINISTRATOR}),
}

#: «qualunque attivo → SUSPENDED: persona, operatore, amministratore». DRAFT → SUSPENDED («persona, operatore») is one
#: of those moves: a move is open to every capacity that a row of §4 matching it names.
SUSPEND_ACTORS: frozenset[str] = frozenset({_WHO.PERSON, _WHO.OPERATOR, _WHO.ADMINISTRATOR})
#: «qualunque → CLOSED: persona, amministratore» — and «POST_ENTRY → CLOSED: operatore, persona».
CLOSE_ACTORS: frozenset[str] = frozenset({_WHO.PERSON, _WHO.ADMINISTRATOR})
CLOSE_ACTORS_FROM: dict[str, frozenset[str]] = {CaseStatus.POST_ENTRY: CLOSE_ACTORS | {_WHO.OPERATOR}}
#: «SUSPENDED → stato precedente: chi ha sospeso, o superiore» — the superior is the administrator (sec-f7 NOTES, Q4);
#: whoever suspended the file is a fact of its history this table cannot hold (``services.suspended_by``). §4 declares
#: no other way out of SUSPENDED but CLOSED.
RESUME_ACTORS: frozenset[str] = frozenset({_WHO.ADMINISTRATOR})

#: Every capacity the data above holds that §4 does not name, with its reason — the only departures from the table.
#: ``apps/cases/tests/test_transition_actors.py`` reads §4 from the document and checks that the data is the table plus
#: exactly these. Each is the owner's to confirm (and §4 to gain) or to remove (sec-f7 NOTES, Q1 and Q5).
BEYOND_SECTION_4: dict[tuple[str, str], tuple[frozenset[str], str]] = {
    (CaseStatus.SELECTION, CaseStatus.TRAINING): (
        frozenset({_WHO.AUTHORISED_ACTOR, _WHO.ADMINISTRATOR}),
        "Not in §4. A selection that ends without a referral returns the file to its training pathway "
        "(selection.services.conclude); and the administrator's way out of a selection that can no longer be "
        "concluded (sec-f7 REVIEW, finding 4). The move asserts no outcome.",
    ),
    (CaseStatus.ENTERED, CaseStatus.POST_ENTRY): (
        frozenset({_WHO.ADMINISTRATOR}),
        "§4 names «sistema — automatica», and nothing performs the move: the administrator stands in for the missing "
        "automation, so that a file whose entry is recorded can reach its accompaniment (sec-f7 NOTES, Q5).",
    ),
}


def transition_actors(status: str, target: str, *, previous: str = "") -> frozenset[str]:
    """
    The capacities that may move a file from ``status`` to ``target`` — empty when the move is not declared at all,
    and for a declared move nobody may make (a row §4 does not have).

    Out of SUSPENDED, ``previous`` is the state the file was suspended from: the way back to it is the superior's
    (``RESUME_ACTORS``) and, at runtime, whoever suspended the file — ``services.permitted_transitions`` reads that
    from the audit trail («chi ha sospeso, o superiore»). Every other way out of SUSPENDED but CLOSED is nobody's:
    §4 declares the way back to the previous state only.
    """
    if target not in transitions_from(status):
        return frozenset()
    if target == CaseStatus.CLOSED:
        return CLOSE_ACTORS_FROM.get(status, CLOSE_ACTORS)
    if target == CaseStatus.SUSPENDED:
        return SUSPEND_ACTORS
    if status == CaseStatus.SUSPENDED:
        return RESUME_ACTORS if previous and target == previous else frozenset()
    return TRANSITION_ACTORS.get((status, target), frozenset())


class CasePurpose(models.TextChoices):
    """The lawful purposes of Technical Blueprint v1.0 §5.3. Never a promise of outcome."""

    WORK = "work", _("Lavoro")
    STUDY = "study", _("Studio")
    TRAINING = "training", _("Formazione")
    FAMILY = "family", _("Famiglia")
    OTHER = "other", _("Altra finalità lecita")


class CaseFileQuerySet(models.QuerySet):
    def readable_by(self, user) -> CaseFileQuerySet:
        """
        Authorisation applied AT QUERY TIME, never after the fact.

        A user must not be able to learn that an object exists through a count, an autocomplete or a
        differently worded "not found": the filter therefore belongs to the queryset.

        Two deliberate strictnesses, both tightened on 20 September 2026 after a security review:

        * An assignment grants access only while it is LIVE. Checking ``revoked_at`` alone let an
          expired mandate keep listing case files, which is precisely the boundary a dated
          authorisation exists to draw (Technical Blueprint §4).
        * ``role:staff`` gets nothing here. Project staff supervise through the back-office, where
          every access is role-checked and auditable; a platform-side list of every case file in the
          system is not supervision, it is a standing disclosure of personal data. Same reasoning as
          the reserved area, which is stricter than its own policies on purpose.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        today = timezone.localdate()
        assigned = models.Q(
            assignments__assignee=user,
            assignments__revoked_at__isnull=True,
        ) & (
            models.Q(assignments__authorisation_valid_until__isnull=True)
            | models.Q(assignments__authorisation_valid_until__gte=today)
        )
        return self.filter(models.Q(person=user) | assigned).distinct()

    def active(self) -> CaseFileQuerySet:
        return self.filter(status__in=ACTIVE_STATUSES)


class CaseFile(TimeStampedModel):
    """One pathway of one person towards one lawful purpose."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(
        _("riferimento"),
        max_length=16,
        unique=True,
        editable=False,
        help_text=_("Riferimento breve mostrato alla persona e citato nelle comunicazioni."),
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="case_files",
        verbose_name=_("persona"),
    )
    purpose = models.CharField(_("finalità"), max_length=16, choices=CasePurpose.choices)
    pathway_key = models.CharField(
        _("percorso"),
        max_length=64,
        blank=True,
        help_text=_("Chiave della famiglia di percorsi individuata dall'orientamento."),
    )
    status = models.CharField(
        _("stato"), max_length=20, choices=CaseStatus.choices, default=CaseStatus.DRAFT, db_index=True
    )
    status_since = models.DateTimeField(_("in questo stato dal"), default=timezone.now, editable=False)
    previous_status = models.CharField(
        _("stato precedente"), max_length=20, choices=CaseStatus.choices, blank=True, editable=False
    )
    suspension_reason = models.TextField(_("motivo della sospensione"), blank=True)
    closed_at = models.DateTimeField(_("chiuso il"), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _("fascicolo digitale")
        verbose_name_plural = _("fascicoli digitali")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["person", "status"]),
            models.Index(fields=["status", "status_since"]),
        ]

    objects = CaseFileQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.reference} · {self.get_purpose_display()}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._new_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _new_reference() -> str:
        """A short, non-sequential reference: sequential ones leak how many cases exist."""
        for _attempt in range(12):
            candidate = uuid.uuid4().hex[:10].upper()
            if not CaseFile.objects.filter(reference=candidate).exists():
                return candidate
        raise RuntimeError("could not allocate a unique case reference")

    # -- lifecycle ---------------------------------------------------------------------------
    @property
    def is_active(self) -> bool:
        return self.status in ACTIVE_STATUSES

    @property
    def is_read_only(self) -> bool:
        """A closed case is never reopened: a new case is opened instead (CASE_LIFECYCLE §4)."""
        return self.status == CaseStatus.CLOSED

    def allowed_transitions(self) -> frozenset[str]:
        return transitions_from(self.status)

    def can_transition_to(self, target: str) -> bool:
        return target in self.allowed_transitions()

    def has_valid_authorised_actor(self) -> bool:
        """
        True when a non-revoked AUTHORISED_ACTOR assignment carries an authorisation valid today (CR-03, §4 rule 1).

        The role is part of it: an operator's or a professional's assignment that happens to carry a reference is not
        an authorised actor (sec-f7 REVIEW, the CR-03 observation).
        """
        today = timezone.localdate()
        return (
            self.assignments.filter(
                role=AssignmentRole.AUTHORISED_ACTOR,
                revoked_at__isnull=True,
                authorisation_reference__gt="",
            )
            .filter(models.Q(authorisation_valid_until__isnull=True) | models.Q(authorisation_valid_until__gte=today))
            .exists()
        )

    def clean(self) -> None:
        if self.status == CaseStatus.SUSPENDED and not self.suspension_reason.strip():
            raise ValidationError({"suspension_reason": _("La sospensione richiede una motivazione.")})


class ChecklistStatus(models.TextChoices):
    PENDING = "pending", _("Da fare")
    IN_PROGRESS = "in_progress", _("In corso")
    DONE = "done", _("Completato")
    NOT_APPLICABLE = "not_applicable", _("Non applicabile")
    BLOCKED = "blocked", _("Bloccato")


class ResponsibleActor(models.TextChoices):
    """
    WHO must act. Deliberately explicit, and deliberately never "Italy Legal Entry": the platform
    coordinates, it does not perform acts reserved to authorities or to authorised parties.
    """

    PERSON = "person", _("La persona")
    COMPANY = "company", _("L'impresa")
    AUTHORITY = "authority", _("L'autorità competente")
    PROFESSIONAL = "professional", _("Il professionista incaricato")
    TRAINING_BODY = "training_body", _("L'ente di formazione")
    AUTHORISED_ACTOR = "authorised_actor", _("Il soggetto autorizzato")
    PROJECT_TEAM = "project_team", _("L'équipe del progetto")


class ChecklistItem(TimeStampedModel):
    """A requirement of the case, with the actor responsible for it. Never anonymous."""

    case = models.ForeignKey(CaseFile, on_delete=models.CASCADE, related_name="checklist", verbose_name=_("fascicolo"))
    order = models.PositiveIntegerField(_("ordine"), default=0)
    requirement = models.CharField(_("requisito"), max_length=300)
    detail = models.TextField(_("dettaglio"), blank=True)
    status = models.CharField(
        _("stato"), max_length=16, choices=ChecklistStatus.choices, default=ChecklistStatus.PENDING, db_index=True
    )
    responsible_actor = models.CharField(_("responsabile"), max_length=20, choices=ResponsibleActor.choices)
    responsible_note = models.CharField(
        _("precisazione sul responsabile"),
        max_length=200,
        blank=True,
        help_text=_("Es. il nome dell'autorità competente, senza nominare persone fisiche."),
    )
    due_date = models.DateField(_("scadenza"), null=True, blank=True)
    source_title = models.CharField(_("fonte"), max_length=200, blank=True)
    source_ref = models.CharField(_("riferimento della fonte"), max_length=300, blank=True)
    language = models.CharField(_("lingua del testo"), max_length=8, default="fr", editable=False)

    class Meta:
        verbose_name = _("voce di checklist")
        verbose_name_plural = _("checklist")
        ordering = ["case", "order", "id"]
        indexes = [models.Index(fields=["case", "status"])]

    def __str__(self) -> str:
        return self.requirement[:80]

    def clean(self) -> None:
        # "Who is responsible" is an acceptance criterion: an item that cannot answer it is invalid.
        if not self.responsible_actor:
            raise ValidationError({"responsible_actor": _("Ogni voce deve indicare un responsabile.")})

    @property
    def is_open(self) -> bool:
        return self.status in {ChecklistStatus.PENDING, ChecklistStatus.IN_PROGRESS, ChecklistStatus.BLOCKED}

    @property
    def is_overdue(self) -> bool:
        # the project's clock, as every deadline of the interface (T1, the documents' register, the deadlines page):
        # on a lane or the preview a reference date stands in for today (W3-C REVIEW M3)
        return bool(self.due_date and self.is_open and self.due_date < clock.today())


class AssignmentRole(models.TextChoices):
    PROFESSIONAL = "professional", _("Professionista")
    AUTHORISED_ACTOR = "authorised_actor", _("Soggetto autorizzato")
    TRAINING_BODY = "training_body", _("Ente di formazione")
    OPERATOR = "operator", _("Operatore")


class CaseAssignment(TimeStampedModel):
    """
    Who is working on this case, in which capacity, under which mandate, from when to when.

    ``authorisation_reference`` is what makes a SELECTION lawful: an assignment as authorised actor
    without a reference and a validity is not an authorisation, it is a claim.
    """

    case = models.ForeignKey(
        CaseFile, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("fascicolo")
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="case_assignments",
        verbose_name=_("assegnatario"),
    )
    role = models.CharField(_("ruolo nell'incarico"), max_length=20, choices=AssignmentRole.choices)
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="case_assignments",
        verbose_name=_("organizzazione"),
    )
    authorisation_reference = models.CharField(
        _("riferimento dell'autorizzazione"),
        max_length=200,
        blank=True,
        help_text=_("Obbligatorio per il ruolo «soggetto autorizzato»: estremi dell'abilitazione."),
    )
    authorisation_jurisdiction = models.CharField(_("giurisdizione"), max_length=8, blank=True)
    authorisation_valid_until = models.DateField(_("autorizzazione valida fino al"), null=True, blank=True)
    mandate_note = models.CharField(_("nota sul mandato"), max_length=300, blank=True)
    assigned_at = models.DateTimeField(_("assegnato il"), default=timezone.now)
    revoked_at = models.DateTimeField(_("revocato il"), null=True, blank=True)

    class Meta:
        verbose_name = _("assegnazione")
        verbose_name_plural = _("assegnazioni")
        ordering = ["-assigned_at"]
        indexes = [models.Index(fields=["case", "revoked_at"])]

    def __str__(self) -> str:
        return f"{self.get_role_display()} · {self.case.reference}"

    @property
    def is_live(self) -> bool:
        if self.revoked_at is not None:
            return False
        return not (self.authorisation_valid_until and self.authorisation_valid_until < timezone.localdate())

    def clean(self) -> None:
        if self.role == AssignmentRole.AUTHORISED_ACTOR and not self.authorisation_reference.strip():
            raise ValidationError(
                {
                    "authorisation_reference": _(
                        "Il ruolo «soggetto autorizzato» richiede gli estremi dell'autorizzazione."
                    )
                }
            )


class AssessmentOutcome(models.TextChoices):
    """
    The five admissible outcomes. ``eligible`` from the Blueprint deliberately does NOT exist: a user
    reads it as "I am entitled to enter". See CONFLICT_REGISTER CR-11.
    """

    POSSIBLE = "possible", _("Percorso pertinente")
    MISSING_REQUIREMENT = "missing_requirement", _("Requisito mancante")
    WARNING = "warning", _("Avvertenza")
    STOP = "stop", _("Elemento ostativo")
    REVIEW_REQUIRED = "review_required", _("Verifica professionale necessaria")


class PathwayAssessment(TimeStampedModel):
    """
    One execution of the rule engine, frozen.

    ``ruleset_snapshot`` holds the WHOLE ruleset used, not a version number: the acceptance criterion
    is that an outcome can be reproduced from the snapshot even after the rules have changed
    (Technical Blueprint §17.2). Keeping only a pointer would make the outcome unreproducible the day
    it matters — which is the day someone disputes it.
    """

    case = models.ForeignKey(
        CaseFile, on_delete=models.CASCADE, related_name="assessments", verbose_name=_("fascicolo")
    )
    assessed_at = models.DateTimeField(_("valutato il"), default=timezone.now, editable=False, db_index=True)
    purpose = models.CharField(_("finalità"), max_length=16, choices=CasePurpose.choices)
    outcome = models.CharField(_("esito"), max_length=24, choices=AssessmentOutcome.choices, db_index=True)
    pathway_key = models.CharField(_("percorso"), max_length=64, blank=True)
    ruleset_version = models.PositiveIntegerField(_("versione del ruleset"))
    ruleset_snapshot = models.JSONField(_("snapshot del ruleset"), default=dict)
    answers = models.JSONField(_("risposte"), default=dict)
    applied_rules = models.JSONField(
        _("regole applicate"),
        default=list,
        help_text=_("Elenco di {rule_id, version, effect} nell'ordine di applicazione."),
    )
    missing_requirements = models.JSONField(_("requisiti mancanti"), default=list)
    sources = models.JSONField(_("fonti"), default=list)
    rationale = models.TextField(_("motivazione"), blank=True)

    class Meta:
        verbose_name = _("pre-valutazione")
        verbose_name_plural = _("pre-valutazioni")
        ordering = ["-assessed_at"]

    def __str__(self) -> str:
        return f"{self.case.reference} · {self.get_outcome_display()} · {self.assessed_at:%d/%m/%Y}"

    @property
    def is_blocking(self) -> bool:
        return self.outcome == AssessmentOutcome.STOP

    @property
    def needs_human_review(self) -> bool:
        return self.outcome == AssessmentOutcome.REVIEW_REQUIRED
