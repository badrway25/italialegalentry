"""
Authorised selection — the most legally sensitive module of the product.

Italy Legal Entry is NEVER the intermediary. Search and selection are activities reserved, under
the applicable law, to authorised parties (Master Dossier §4; CONFLICT_REGISTER CR-03). What the
platform does is keep the chain traceable and refuse to let it be short-circuited:

    CompanyNeed → AuthorizedActor → SelectionMandate → SelectionProcess → CaseFile/Person → AuditEvent

Four invariants are enforced HERE, in the domain, rather than in a form — a form is one entry point
among several, and a rule that only exists in a form is a rule that the admin, a management command
or a future API does not have:

1. An authorisation that has lapsed, been suspended or been withdrawn grants NOTHING. This is the
   rule ``cases.models.CaseAssignment.is_live`` already applies to a case assignment; the same rule
   is applied here to the actor itself, and the querysets filter on it so that a lapsed authorisation
   does not even read a list.
2. A ``SelectionProcess`` cannot exist without a live mandate held by a valid authorised actor.
   ``cases.services.transition`` already refuses ``CaseStatus.SELECTION`` without a valid assigned
   actor; ``selection.services.open_process`` creates that assignment from the actor's own
   authorisation, so the two statements can never disagree.
3. A person's identity reaches a company ONLY through an ``IdentityDisclosure`` that names a
   purpose, carries a recorded consent OF THE PERSON, and expires. The previous platform let its own
   staff decide this, with no consent from the subject, no purpose and no duration
   (previous-platform audit, part 2 §5, private register). Every single access is recorded, one row
   per access.
4. No outcome of a selection process is a judgement on a person. There is no "approved", no
   "selected", no "rejected": the outcomes describe what happened to the PROCESS. For the same
   reason as CR-11 removed ``eligible`` from the rule engine.

What is deliberately NOT here, and must never be added: any age, age band, nationality, gender,
health, religion or union field on a need, a mandate or a process. The previous platform carried an
age band on every job opening, which is direct age discrimination under Directive 2000/78/EC and
D.lgs. 216/2003 (previous-platform audit, part 2 §3, private register). ``tests/test_models.py``
asserts the absence.
"""

from __future__ import annotations

import datetime as dt
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

# ---------------------------------------------------------------------------------------------
# The authorised actor
# ---------------------------------------------------------------------------------------------


class ActorType(models.TextChoices):
    """
    What kind of authorisation the actor holds. The type is descriptive; what makes the actor
    lawful is the reference and the validity window, never the label.
    """

    EMPLOYMENT_AGENCY = "employment_agency", _("Agence pour l’emploi autorisée")
    AUTHORISED_INTERMEDIARY = "authorised_intermediary", _("Sujet autorisé à l’intermédiation")
    PUBLIC_EMPLOYMENT_SERVICE = "public_service", _("Service public de l’emploi")
    BILATERAL_BODY = "bilateral_body", _("Organisme bilatéral habilité")
    AUTHORISED_PROFESSIONAL = "authorised_professional", _("Professionnel habilité")


class AuthorizedActorQuerySet(models.QuerySet):
    def valid(self, on: dt.date | None = None) -> AuthorizedActorQuerySet:
        """Actors whose authorisation is in force. The filter lives in the QUERYSET on purpose."""
        day = on or timezone.localdate()
        return self.filter(
            withdrawn_at__isnull=True,
            suspended_at__isnull=True,
            valid_from__lte=day,
            authorisation_reference__gt="",
        ).filter(models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=day))

    def readable_by(self, user) -> AuthorizedActorQuerySet:
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        return self.filter(operators__user=user, operators__revoked_at__isnull=True).distinct()


class AuthorizedActor(TimeStampedModel):
    """
    An authorisation held by an organisation, with the reference that proves it and the window in
    which it is in force.

    ``authorisation_reference`` is not decoration: an actor without it is a claim, not an
    authorisation, and the domain refuses to build anything on a claim.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.PROTECT,
        related_name="authorisations",
        verbose_name=_("organisation titulaire"),
    )
    actor_type = models.CharField(_("type d’acteur"), max_length=32, choices=ActorType.choices)
    jurisdiction = models.CharField(
        _("juridiction"),
        max_length=16,
        help_text=_("Territoire où l’autorisation produit ses effets (ex. IT, IT-VEN, MA)."),
    )
    authorisation_reference = models.CharField(
        _("référence de l’autorisation"),
        max_length=200,
        help_text=_("Les références de l’acte qui habilite l’organisation. Obligatoire."),
    )
    authorisation_register = models.CharField(
        _("registre ou albo"),
        max_length=200,
        blank=True,
        help_text=_("Registre public où l’autorisation est inscrite, s’il existe."),
    )
    valid_from = models.DateField(_("valable à partir du"))
    valid_until = models.DateField(
        _("valable jusqu’au"),
        null=True,
        blank=True,
        help_text=_("Vide = sans échéance inscrite. Une échéance passée n’ouvre plus rien."),
    )
    suspended_at = models.DateTimeField(_("suspendue le"), null=True, blank=True)
    withdrawn_at = models.DateTimeField(_("retirée le"), null=True, blank=True)
    scope_note = models.CharField(
        _("portée"),
        max_length=300,
        blank=True,
        help_text=_("Ce que l’autorisation couvre, dans les termes de l’acte."),
    )

    objects = AuthorizedActorQuerySet.as_manager()

    class Meta:
        verbose_name = _("acteur autorisé")
        verbose_name_plural = _("acteurs autorisés")
        ordering = ["organisation__name", "-valid_from"]
        constraints = [
            models.UniqueConstraint(
                fields=["organisation", "authorisation_reference"],
                name="uniq_actor_authorisation",
            ),
        ]
        indexes = [models.Index(fields=["valid_until", "withdrawn_at"])]

    def __str__(self) -> str:
        return f"{self.organisation.name} · {self.authorisation_reference}"

    def clean(self) -> None:
        errors = {}
        if not (self.authorisation_reference or "").strip():
            errors["authorisation_reference"] = _("Un acteur autorisé sans référence d’autorisation n’existe pas.")
        if not (self.jurisdiction or "").strip():
            errors["jurisdiction"] = _("La juridiction de l’autorisation est obligatoire.")
        if self.valid_until and self.valid_from and self.valid_until < self.valid_from:
            errors["valid_until"] = _("L’échéance précède la prise d’effet.")
        if errors:
            raise ValidationError(errors)

    def is_valid(self, on: dt.date | None = None) -> bool:
        """The single definition of "this authorisation is in force today"."""
        day = on or timezone.localdate()
        if self.withdrawn_at is not None or self.suspended_at is not None:
            return False
        if not (self.authorisation_reference or "").strip():
            return False
        if self.valid_from > day:
            return False
        return not (self.valid_until and self.valid_until < day)

    @property
    def is_live(self) -> bool:
        return self.is_valid()

    @property
    def status_word(self) -> str:
        """A WORD for the state — never a colour on its own (design system: ``.state``)."""
        if self.withdrawn_at is not None:
            return "withdrawn"
        if self.suspended_at is not None:
            return "suspended"
        if not self.is_valid():
            return "expired"
        return "valid"

    def live_operator_ids(self) -> set[int]:
        return {row.user_id for row in self.operators.all() if row.is_live}


class ActorOperator(TimeStampedModel):
    """
    An account entitled to work UNDER an authorisation. Not a role a user grants themselves: the
    link is created by the administration and is what the workspace queryset filters on.

    ``function_note`` names a FUNCTION ("responsable du processus"), never a natural person: the
    platform names the organisation and the function that answer for an act.
    """

    actor = models.ForeignKey(
        AuthorizedActor, on_delete=models.CASCADE, related_name="operators", verbose_name=_("acteur autorisé")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="actor_authorisations",
        verbose_name=_("compte"),
    )
    function_note = models.CharField(_("fonction"), max_length=200, blank=True)
    added_at = models.DateTimeField(_("habilité le"), default=timezone.now)
    revoked_at = models.DateTimeField(_("révoqué le"), null=True, blank=True)

    class Meta:
        verbose_name = _("intervenant habilité")
        verbose_name_plural = _("intervenants habilités")
        ordering = ["-added_at"]
        constraints = [models.UniqueConstraint(fields=["actor", "user"], name="uniq_actor_operator")]

    def __str__(self) -> str:
        return f"{self.actor.organisation.name} · {self.function_note or self.user_id}"

    @property
    def is_live(self) -> bool:
        return self.revoked_at is None and self.actor.is_valid()


# ---------------------------------------------------------------------------------------------
# The mandate: the CompanyNeed → AuthorizedActor edge
# ---------------------------------------------------------------------------------------------


class SelectionMandate(TimeStampedModel):
    """
    One company need entrusted to one authorised actor, for a period.

    The need itself belongs to ``companies``. It is referenced here by a SOFT reference plus a
    FROZEN snapshot of the facts the actor is mandated to work on, for two reasons:

    * the mandate must stay readable and auditable exactly as it was issued, even if the company
      later edits or deletes its need — the same reasoning that makes ``PathwayAssessment`` freeze
      the whole ruleset rather than a version number;
    * the need fields the actor may see are enumerated here, which is what keeps data minimisation
      a property of the code rather than a promise.

    The snapshot carries COMPETENCES and CONDITIONS. It carries no age, no nationality and no other
    protected characteristic, and it never will.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(_("référence"), max_length=16, unique=True, editable=False)
    actor = models.ForeignKey(
        AuthorizedActor, on_delete=models.PROTECT, related_name="mandates", verbose_name=_("acteur autorisé")
    )
    company = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.PROTECT,
        related_name="selection_mandates",
        verbose_name=_("entreprise à l’origine du besoin"),
    )

    # -- the soft reference to the need (apps.companies owns the need itself) --------------------
    need_source = models.CharField(
        _("origine du besoin"),
        max_length=64,
        default="companies.CompanyNeed",
        help_text=_("Modèle d’origine du besoin, référencé sans couplage dur."),
    )
    need_id = models.CharField(_("identifiant du besoin"), max_length=64, blank=True)
    need_reference = models.CharField(_("référence du besoin"), max_length=64, blank=True)

    # -- the frozen facts of the need ------------------------------------------------------------
    need_profile = models.CharField(_("profil professionnel"), max_length=200)
    need_sector = models.CharField(_("secteur"), max_length=120, blank=True)
    need_territory = models.CharField(_("territoire"), max_length=120, blank=True)
    need_headcount = models.PositiveSmallIntegerField(_("nombre de postes"), default=1)
    need_competences = models.JSONField(
        _("compétences attendues"),
        default=list,
        blank=True,
        help_text=_("Liste de {label, level}. Compétences et conditions uniquement."),
    )
    need_language_requirement = models.CharField(_("exigence linguistique"), max_length=120, blank=True)
    need_timeframe = models.CharField(_("échéance du besoin"), max_length=120, blank=True)
    need_snapshot = models.JSONField(_("instantané du besoin"), default=dict, blank=True)

    issued_at = models.DateTimeField(_("délivré le"), default=timezone.now)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("délivré par"),
    )
    valid_until = models.DateField(_("valable jusqu’au"), null=True, blank=True)
    revoked_at = models.DateTimeField(_("révoqué le"), null=True, blank=True)
    scope_note = models.CharField(_("portée du mandat"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("mandat de sélection")
        verbose_name_plural = _("mandats de sélection")
        ordering = ["-issued_at"]
        indexes = [models.Index(fields=["actor", "revoked_at"])]

    def __str__(self) -> str:
        return f"{self.reference} · {self.need_profile}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = _new_reference(SelectionMandate)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        errors = {}
        if not (self.need_profile or "").strip():
            errors["need_profile"] = _("Un mandat porte sur un profil professionnel identifié.")
        if self.valid_until and self.valid_until < timezone.localdate() and self.pk is None:
            errors["valid_until"] = _("Un mandat ne peut pas être délivré déjà échu.")
        if not isinstance(self.need_competences, list):
            errors["need_competences"] = _("Les compétences attendues sont une liste.")
        if errors:
            raise ValidationError(errors)

    @property
    def is_live(self) -> bool:
        """A mandate is only as live as the authorisation behind it."""
        if self.revoked_at is not None:
            return False
        if self.valid_until and self.valid_until < timezone.localdate():
            return False
        return self.actor.is_valid()

    @property
    def status_word(self) -> str:
        if self.revoked_at is not None:
            return "withdrawn"
        if not self.actor.is_valid():
            return "expired"
        if self.valid_until and self.valid_until < timezone.localdate():
            return "expired"
        return "valid"

    @property
    def competences(self) -> list[dict]:
        rows = self.need_competences if isinstance(self.need_competences, list) else []
        return [row for row in rows if isinstance(row, dict)]


# ---------------------------------------------------------------------------------------------
# The selection process
# ---------------------------------------------------------------------------------------------


class SelectionStage(models.TextChoices):
    """
    Where the process stands. Each stage names an ACT of the authorised actor, never a verdict on a
    person.
    """

    MANDATE_CONFIRMED = "mandate_confirmed", _("Mandat confirmé")
    COMPETENCE_REVIEW = "competence_review", _("Examen des compétences")
    EVIDENCE_REVIEW = "evidence_review", _("Vérification des justificatifs")
    COMPANY_REVIEW = "company_review", _("Examen par l’entreprise")
    CONCLUDED = "concluded", _("Processus clos")
    SUSPENDED = "suspended", _("Processus suspendu")


#: Stages in which the process is still being worked on.
OPEN_STAGES: frozenset[str] = frozenset(
    {
        SelectionStage.MANDATE_CONFIRMED,
        SelectionStage.COMPETENCE_REVIEW,
        SelectionStage.EVIDENCE_REVIEW,
        SelectionStage.COMPANY_REVIEW,
    }
)

#: The declared transition table. Anything absent is refused by the domain, exactly as in
#: ``cases.models.ALLOWED_TRANSITIONS`` — a stage reached by a path nobody declared is a stage
#: nobody can account for.
ALLOWED_STAGE_TRANSITIONS: dict[str, frozenset[str]] = {
    SelectionStage.MANDATE_CONFIRMED: frozenset({SelectionStage.COMPETENCE_REVIEW}),
    SelectionStage.COMPETENCE_REVIEW: frozenset({SelectionStage.EVIDENCE_REVIEW}),
    SelectionStage.EVIDENCE_REVIEW: frozenset({SelectionStage.COMPANY_REVIEW, SelectionStage.COMPETENCE_REVIEW}),
    SelectionStage.COMPANY_REVIEW: frozenset({SelectionStage.EVIDENCE_REVIEW}),
    SelectionStage.CONCLUDED: frozenset(),
    SelectionStage.SUSPENDED: frozenset(),
}


def stages_from(stage: str) -> frozenset[str]:
    """Every stage reachable from ``stage``, including the universal exits."""
    declared = ALLOWED_STAGE_TRANSITIONS.get(stage, frozenset())
    if stage in OPEN_STAGES:
        return declared | {SelectionStage.SUSPENDED, SelectionStage.CONCLUDED}
    if stage == SelectionStage.SUSPENDED:
        return frozenset(OPEN_STAGES) | {SelectionStage.CONCLUDED}
    return declared


class SelectionOutcome(models.TextChoices):
    """
    How the process ENDED. Read the list twice: not one of these says anything about the worth of a
    person, and none of them can be read as an administrative decision.

    There is deliberately no "retenu", no "approuvé", no "refusé". A platform that cannot approve
    anybody must not own a vocabulary that looks as if it could (CR-11, and CR-03 for the reason the
    decision belongs to the authorised actor and to the competent authority, never here).
    """

    REFERRED_TO_PROCEDURE = "referred_to_procedure", _("Transmis à la procédure autorisée")
    CLOSED_NO_FOLLOW_UP = "closed_no_follow_up", _("Clos sans suite")
    # Reworded: « Clos à la demande de la personne » repeats a phrase of the prescribed privacy
    # notice, and a prescribed text retyped here would enter the translation catalogues.
    WITHDRAWN_BY_PERSON = "withdrawn_by_person", _("Interrompu par la personne concernée")
    WITHDRAWN_BY_COMPANY = "withdrawn_by_company", _("Besoin retiré par l’entreprise")
    MANDATE_LAPSED = "mandate_lapsed", _("Mandat échu")


class SelectionProcessQuerySet(models.QuerySet):
    def readable_by(self, user) -> SelectionProcessQuerySet:
        """
        Authorisation applied AT QUERY TIME.

        Three perimeters, and nothing else:

        * the PERSON whose case file it is — they always see who is working on their file and at
          which stage; a selection conducted on someone without their knowledge is not traceability;
        * a LIVE OPERATOR of the authorised actor — and only while the authorisation is in force, so
          a lapsed authorisation reads nothing, not even a count;
        * a member of the COMPANY that expressed the need — the process attached to its own need,
          never a list of people, and never an identity without a disclosure.

        ``role:staff`` gets nothing, as in ``cases.models.CaseFileQuerySet.readable_by``: project
        staff supervise from the back-office where every access is role-checked and audited. A
        standing platform-side list of selection processes is not supervision, it is a disclosure.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        today = timezone.localdate()
        operator = (
            models.Q(actor__operators__user=user, actor__operators__revoked_at__isnull=True)
            & models.Q(
                actor__withdrawn_at__isnull=True,
                actor__suspended_at__isnull=True,
                actor__valid_from__lte=today,
            )
            & (models.Q(actor__valid_until__isnull=True) | models.Q(actor__valid_until__gte=today))
        )
        company = models.Q(mandate__company__memberships__user=user)
        return self.filter(models.Q(case__person=user) | operator | company).distinct()

    def for_operator(self, user) -> SelectionProcessQuerySet:
        """The actor's workspace: ONLY the processes assigned to them. Never a global view."""
        if not getattr(user, "is_authenticated", False):
            return self.none()
        today = timezone.localdate()
        return self.filter(
            actor__operators__user=user,
            actor__operators__revoked_at__isnull=True,
            actor__withdrawn_at__isnull=True,
            actor__suspended_at__isnull=True,
            actor__valid_from__lte=today,
        ).filter(models.Q(actor__valid_until__isnull=True) | models.Q(actor__valid_until__gte=today))

    def open(self) -> SelectionProcessQuerySet:
        return self.filter(stage__in=OPEN_STAGES)


class SelectionProcess(TimeStampedModel):
    """
    One need, one authorised actor, one case file, one stage.

    It cannot be created without a live mandate held by a valid actor: see
    ``selection.services.open_process``, which is the only way in, and which also creates the
    ``cases.CaseAssignment`` that lets ``cases.services.transition`` accept ``SELECTION``. The two
    statements cannot disagree because there is only one of them.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(_("référence"), max_length=16, unique=True, editable=False)
    mandate = models.ForeignKey(
        SelectionMandate, on_delete=models.PROTECT, related_name="processes", verbose_name=_("mandat")
    )
    actor = models.ForeignKey(
        AuthorizedActor, on_delete=models.PROTECT, related_name="processes", verbose_name=_("acteur responsable")
    )
    case = models.ForeignKey(
        "cases.CaseFile", on_delete=models.CASCADE, related_name="selection_processes", verbose_name=_("dossier")
    )
    stage = models.CharField(
        _("phase"),
        max_length=24,
        choices=SelectionStage.choices,
        default=SelectionStage.MANDATE_CONFIRMED,
        db_index=True,
    )
    stage_since = models.DateTimeField(_("dans cette phase depuis"), default=timezone.now, editable=False)
    previous_stage = models.CharField(_("phase précédente"), max_length=24, blank=True, editable=False)
    outcome = models.CharField(_("issue"), max_length=32, choices=SelectionOutcome.choices, blank=True, db_index=True)
    opened_at = models.DateTimeField(_("ouvert le"), default=timezone.now, editable=False)
    opened_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    closed_at = models.DateTimeField(_("clos le"), null=True, blank=True, editable=False)
    closing_note = models.CharField(_("note de clôture"), max_length=300, blank=True)
    suspension_reason = models.CharField(_("motif de la suspension"), max_length=300, blank=True)

    objects = SelectionProcessQuerySet.as_manager()

    class Meta:
        verbose_name = _("processus de sélection")
        verbose_name_plural = _("processus de sélection")
        ordering = ["-opened_at"]
        constraints = [
            models.UniqueConstraint(fields=["mandate", "case"], name="uniq_process_per_mandate_and_case"),
        ]
        indexes = [
            models.Index(fields=["actor", "stage"]),
            models.Index(fields=["case", "stage"]),
        ]

    def __str__(self) -> str:
        return f"{self.reference} · {self.get_stage_display()}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = _new_reference(SelectionProcess)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        errors = {}
        if self.mandate_id and self.actor_id and self.mandate.actor_id != self.actor_id:
            errors["actor"] = _("L’acteur responsable doit être celui du mandat.")
        if self.stage == SelectionStage.SUSPENDED and not (self.suspension_reason or "").strip():
            errors["suspension_reason"] = _("Une suspension se motive.")
        if errors:
            raise ValidationError(errors)

    # -- lifecycle ----------------------------------------------------------------------------
    @property
    def is_open(self) -> bool:
        return self.stage in OPEN_STAGES

    @property
    def is_closed(self) -> bool:
        return self.stage == SelectionStage.CONCLUDED

    def allowed_stages(self) -> frozenset[str]:
        return stages_from(self.stage)

    def can_move_to(self, target: str) -> bool:
        return target in self.allowed_stages()

    @property
    def person(self):
        return self.case.person

    @property
    def responsible_label(self) -> str:
        """
        WHO answers for this process. Named on every screen where a stage is visible, because Italy
        Legal Entry is never the intermediary and a screen that does not say so implies otherwise.
        """
        return f"{self.actor.organisation.name} — {self.actor.authorisation_reference}"

    def live_disclosure(self, now=None):
        """The disclosure currently in force, if any. Never trust a stored 'granted' alone."""
        moment = now or timezone.now()
        for row in self.disclosures.all():
            if row.is_active(moment):
                return row
        return None


class SelectionStageEvent(TimeStampedModel):
    """
    One stage change, with the authorised actor that is answerable for it.

    An ``AuditEvent`` is written as well (``selection.stage``): the audit trail is the institution's
    record, this row is the one the person and the company read on the process page. Both name the
    actor; neither names a natural person.
    """

    process = models.ForeignKey(
        SelectionProcess, on_delete=models.CASCADE, related_name="events", verbose_name=_("processus")
    )
    from_stage = models.CharField(_("de la phase"), max_length=24, choices=SelectionStage.choices, blank=True)
    to_stage = models.CharField(_("vers la phase"), max_length=24, choices=SelectionStage.choices)
    actor = models.ForeignKey(
        AuthorizedActor, on_delete=models.PROTECT, related_name="+", verbose_name=_("acteur responsable")
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    note = models.CharField(_("note"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("mouvement de phase")
        verbose_name_plural = _("mouvements de phase")
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"{self.process_id} · {self.to_stage}"

    @property
    def responsible_label(self) -> str:
        return f"{self.actor.organisation.name} — {self.actor.authorisation_reference}"


class EvidenceStatus(models.TextChoices):
    REQUESTED = "requested", _("Demandé")
    PROVIDED = "provided", _("Fourni")
    NOT_APPLICABLE = "not_applicable", _("Sans objet")
    BLOCKED = "blocked", _("Bloqué")


class SelectionEvidence(TimeStampedModel):
    """
    What the actor requires, and WHO must produce it. Never anonymous — the same rule as
    ``cases.ChecklistItem``: an item that cannot say who is responsible is invalid.
    """

    process = models.ForeignKey(
        SelectionProcess, on_delete=models.CASCADE, related_name="evidence", verbose_name=_("processus")
    )
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    requirement = models.CharField(_("justificatif attendu"), max_length=300)
    detail = models.CharField(_("précision"), max_length=300, blank=True)
    responsible_actor = models.CharField(_("responsable"), max_length=20)
    responsible_note = models.CharField(_("précision sur le responsable"), max_length=200, blank=True)
    status = models.CharField(
        _("état"), max_length=16, choices=EvidenceStatus.choices, default=EvidenceStatus.REQUESTED, db_index=True
    )
    due_date = models.DateField(_("échéance"), null=True, blank=True)
    note = models.CharField(_("note"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("justificatif requis")
        verbose_name_plural = _("justificatifs requis")
        ordering = ["process", "order", "id"]
        indexes = [models.Index(fields=["process", "status"])]

    def __str__(self) -> str:
        return self.requirement[:80]

    def clean(self) -> None:
        from cases.models import ResponsibleActor

        if self.responsible_actor not in ResponsibleActor.values:
            raise ValidationError({"responsible_actor": _("Chaque justificatif indique un responsable.")})

    def get_responsible_actor_display(self) -> str:
        from cases.models import ResponsibleActor

        return str(dict(ResponsibleActor.choices).get(self.responsible_actor, self.responsible_actor))

    @property
    def is_open(self) -> bool:
        return self.status in {EvidenceStatus.REQUESTED, EvidenceStatus.BLOCKED}

    @property
    def is_overdue(self) -> bool:
        return bool(self.due_date and self.is_open and self.due_date < timezone.localdate())


# ---------------------------------------------------------------------------------------------
# Progressive disclosure of identity
# ---------------------------------------------------------------------------------------------


class IdentityField(models.TextChoices):
    """
    The ONLY fields a disclosure can ever carry. An enumeration, not a free list, because "which
    fields exactly" is the whole question — and because a free list would drift.

    No special-category data can appear here (GDPR art. 9), and no protected characteristic.
    """

    FULL_NAME = "full_name", _("Nom et prénom")
    CONTACT_EMAIL = "contact_email", _("Adresse de contact")
    PREFERRED_LANGUAGE = "preferred_language", _("Langue de contact")


class DisclosureStatus(models.TextChoices):
    REQUESTED = "requested", _("Demandée — en attente de la décision de la personne")
    GRANTED = "granted", _("Autorisée par la personne")
    REFUSED = "refused", _("Refusée par la personne")
    WITHDRAWN = "withdrawn", _("Retirée par la personne")


#: The consent purpose used for an identity disclosure. ``consents.ConsentPurpose`` does not carry
#: it yet (the app belongs to another lane — see the shared-file request), so the key is declared
#: here and the label is rendered from ``IDENTITY_CONSENT_LABEL`` rather than from
#: ``get_purpose_display()``, which would print the raw key.
IDENTITY_CONSENT_PURPOSE = "identity_disclosure"
IDENTITY_CONSENT_LABEL = _("Communication de l’identité à une entreprise nommée")

#: Longest disclosure a request may ask for. A disclosure without an end is the defect the previous
#: platform had: once communicated, the identity appeared to be communicated for ever.
MAX_DISCLOSURE_DAYS = 180


class IdentityDisclosureQuerySet(models.QuerySet):
    def readable_by(self, user) -> IdentityDisclosureQuerySet:
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        readable_processes = SelectionProcess.objects.readable_by(user)
        return self.filter(process__in=readable_processes).distinct()

    def awaiting_decision_of(self, user) -> IdentityDisclosureQuerySet:
        return self.filter(process__case__person=user, status=DisclosureStatus.REQUESTED)


class IdentityDisclosure(TimeStampedModel):
    """
    The good idea of the previous platform, with the three defects removed.

    The previous platform let its own staff decide that a company could see a person's identity:
    no consent from the subject, no purpose recorded, no duration, no legal basis
    (previous-platform audit, part 2 §5, private register). Here:

    * the AUTHORISED ACTOR requests, naming the company, the purpose and the fields;
    * the PERSON decides, and their decision is recorded as a ``consents.ConsentRecord`` pointing at
      the exact wording they were shown;
    * the disclosure EXPIRES — ``expires_at`` is computed from a duration the request had to state;
    * the person can withdraw it at any moment, which withdraws the consent record too;
    * every single access is written to ``IdentityAccess`` and to the audit trail.

    Until all of that holds, ``is_active()`` is False and ``services.read_identity`` returns nothing
    — the company sees competences and a stage, which is what the process is about.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    process = models.ForeignKey(
        SelectionProcess, on_delete=models.CASCADE, related_name="disclosures", verbose_name=_("processus")
    )
    recipient_organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.PROTECT,
        related_name="identity_disclosures",
        verbose_name=_("entreprise destinataire"),
    )
    purpose = models.CharField(
        _("finalité déclarée"),
        max_length=300,
        help_text=_("Ce à quoi l’identité va servir, en une phrase vérifiable."),
    )
    fields_disclosed = models.JSONField(_("champs communiqués"), default=list, blank=True)
    duration_days = models.PositiveSmallIntegerField(
        _("durée (jours)"), help_text=_("Durée au-delà de laquelle l’autorisation cesse d’elle-même.")
    )
    legal_basis = models.CharField(
        _("base juridique"),
        max_length=64,
        default="gdpr_6_1_a_consent",
        help_text=_("Consentement de la personne concernée — RGPD art. 6§1 a)."),
    )
    status = models.CharField(
        _("état"), max_length=16, choices=DisclosureStatus.choices, default=DisclosureStatus.REQUESTED, db_index=True
    )
    requested_at = models.DateTimeField(_("demandée le"), default=timezone.now, editable=False)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    consent = models.ForeignKey(
        "consents.ConsentRecord",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="identity_disclosures",
        verbose_name=_("consentement enregistré"),
    )
    decided_at = models.DateTimeField(_("décidée le"), null=True, blank=True)
    expires_at = models.DateTimeField(_("expire le"), null=True, blank=True)
    withdrawn_at = models.DateTimeField(_("retirée le"), null=True, blank=True)
    decision_note = models.CharField(_("note de la personne"), max_length=300, blank=True)

    objects = IdentityDisclosureQuerySet.as_manager()

    class Meta:
        verbose_name = _("communication d’identité")
        verbose_name_plural = _("communications d’identité")
        ordering = ["-requested_at"]
        indexes = [models.Index(fields=["process", "status"])]

    def __str__(self) -> str:
        return f"{self.process_id} → {self.recipient_organisation_id} ({self.status})"

    def clean(self) -> None:
        errors = {}
        if not (self.purpose or "").strip():
            errors["purpose"] = _("Une communication d’identité sans finalité déclarée n’est pas licite.")
        rows = self.fields_disclosed if isinstance(self.fields_disclosed, list) else None
        if not rows:
            errors["fields_disclosed"] = _("Indiquez les champs précis qui seront communiqués.")
        elif set(rows) - set(IdentityField.values):
            errors["fields_disclosed"] = _("Champ non prévu par le registre des champs communicables.")
        if not self.duration_days or self.duration_days > MAX_DISCLOSURE_DAYS:
            errors["duration_days"] = _("La durée est obligatoire et ne dépasse pas %(max)d jours.") % {
                "max": MAX_DISCLOSURE_DAYS
            }
        if errors:
            raise ValidationError(errors)

    def is_active(self, now=None) -> bool:
        """
        The single test the whole module relies on. Four conditions, all necessary:
        granted, not withdrawn, not expired, and the consent record still standing.
        """
        moment = now or timezone.now()
        if self.status != DisclosureStatus.GRANTED or self.withdrawn_at is not None:
            return False
        if self.expires_at is None or self.expires_at <= moment:
            return False
        return not (self.consent is None or not self.consent.is_active)

    @property
    def is_expired(self) -> bool:
        return (
            self.status == DisclosureStatus.GRANTED
            and self.withdrawn_at is None
            and self.expires_at is not None
            and self.expires_at <= timezone.now()
        )

    @property
    def status_word(self) -> str:
        if self.is_active():
            return "valid"
        if self.is_expired:
            return "expired"
        if self.status == DisclosureStatus.REQUESTED:
            return "missing"
        return "invalid"

    @property
    def field_labels(self) -> list[str]:
        table = dict(IdentityField.choices)
        rows = self.fields_disclosed if isinstance(self.fields_disclosed, list) else []
        return [str(table[key]) for key in rows if key in table]


class IdentityAccess(models.Model):
    """
    One row per access to a disclosed identity. Append-only, never edited, never deleted from a UI.

    Written by ``selection.services.read_identity`` and nowhere else, so "every access is audited"
    is a property of the only code path that can read the data, not a promise attached to a screen.
    """

    disclosure = models.ForeignKey(
        IdentityDisclosure, on_delete=models.CASCADE, related_name="accesses", verbose_name=_("communication")
    )
    accessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+", verbose_name=_("consulté par")
    )
    accessed_by_organisation = models.ForeignKey(
        "accounts.Organisation", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    accessed_at = models.DateTimeField(_("consulté le"), auto_now_add=True, db_index=True)
    fields_read = models.JSONField(_("champs consultés"), default=list, blank=True)
    purpose_at_access = models.CharField(_("finalité au moment de l’accès"), max_length=300, blank=True)
    ip_hash = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = _("accès à une identité communiquée")
        verbose_name_plural = _("accès aux identités communiquées")
        ordering = ["-accessed_at"]
        indexes = [models.Index(fields=["disclosure", "accessed_at"])]

    def __str__(self) -> str:
        return f"{self.disclosure_id} · {self.accessed_at:%Y-%m-%d %H:%M}"


# ---------------------------------------------------------------------------------------------


def _new_reference(model: type[models.Model]) -> str:
    """A short, NON-SEQUENTIAL reference: a sequential one leaks how many processes exist."""
    for _attempt in range(12):
        candidate = uuid.uuid4().hex[:10].upper()
        if not model.objects.filter(reference=candidate).exists():
            return candidate
    raise RuntimeError("could not allocate a unique reference")
