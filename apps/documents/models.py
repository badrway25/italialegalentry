"""
Private documents (reserved area). Files live under ``settings.PRIVATE_MEDIA_ROOT`` — never under
``MEDIA_ROOT`` — and are only ever served by ``documents.views.download`` after an object-level
permission check (``accounts.permissions``). The model deliberately has NO FileField so that no
template can ever print a public URL for a private file.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cases.models import ResponsibleActor
from core import clock
from core.models import TimeStampedModel


class DocumentKind(models.TextChoices):
    IDENTITY = "identity", _("Pièce d’identité")
    DIPLOMA = "diploma", _("Diplôme ou titre")
    CONTRACT = "contract", _("Contrat")
    OTHER = "other", _("Autre document")


class ScanStatus(models.TextChoices):
    """
    What the ANTIVIRUS says about a file. Four honest values and no fifth (REQ-DOC-03).

    ``NOT_CONFIGURED`` exists because the previous value was a lie: with no scanner deployed, every
    upload sat at "En attente d’analyse" — which tells a reader that an analysis is coming. None was.
    A security control that reports a queue it does not have is worse than one that reports nothing,
    because it buys trust it has not earned. The word for "no scanner is deployed here" is now in the
    vocabulary, and ``documents.services.scan_file`` returns it.
    """

    NOT_CONFIGURED = "not_configured", _("Aucune analyse antivirus n’est configurée")
    PENDING = "pending", _("En attente d’analyse")
    CLEAN = "clean", _("Analysé — sain")
    INFECTED = "infected", _("Infecté — bloqué")
    ERROR = "error", _("Erreur d’analyse")


class PrivateDocumentQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)

    def for_owner(self, user):
        return self.alive().filter(owner=user)

    def pending_scan(self):
        """Files a scanner should look at once one is deployed — NOT_CONFIGURED files included."""
        return self.alive().filter(scan_status__in=[ScanStatus.NOT_CONFIGURED, ScanStatus.PENDING, ScanStatus.ERROR])


class PrivateDocument(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="private_documents",
        verbose_name=_("propriétaire"),
    )
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="private_documents",
        verbose_name=_("organisation"),
    )
    kind = models.CharField(_("type"), max_length=10, choices=DocumentKind.choices, default=DocumentKind.OTHER)
    original_name = models.CharField(_("nom d’origine (assaini)"), max_length=255)
    stored_name = models.CharField(_("nom de stockage"), max_length=80, unique=True, editable=False)
    content_type = models.CharField(_("type MIME"), max_length=100)
    size = models.PositiveBigIntegerField(_("taille (octets)"))
    sha256 = models.CharField("SHA-256", max_length=64, db_index=True)
    description = models.CharField(_("description"), max_length=200, blank=True)
    scan_status = models.CharField(
        _("analyse antivirus"),
        max_length=16,
        choices=ScanStatus.choices,
        default=ScanStatus.NOT_CONFIGURED,
        db_index=True,
    )
    scanned_at = models.DateTimeField(_("analysé le"), null=True, blank=True)
    retention_until = models.DateField(
        _("conservation jusqu’au"),
        null=True,
        blank=True,
        help_text=_("Date au-delà de laquelle le fichier est purgé (commande documents_purge_expired)."),
    )
    uploaded_ip_hash = models.CharField(_("empreinte IP (hachée)"), max_length=32, blank=True, editable=False)
    deleted_at = models.DateTimeField(_("supprimé le"), null=True, blank=True, db_index=True)
    file_removed_at = models.DateTimeField(_("fichier purgé le"), null=True, blank=True, editable=False)

    objects = PrivateDocumentQuerySet.as_manager()

    class Meta:
        verbose_name = _("document privé")
        verbose_name_plural = _("documents privés")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "deleted_at"], name="privdoc_owner_alive_idx")]
        constraints = [models.CheckConstraint(condition=models.Q(size__gt=0), name="privdoc_size_positive")]

    def __str__(self) -> str:
        return f"{self.original_name} ({self.get_kind_display()})"

    @property
    def relative_path(self) -> str:
        """Storage path relative to PRIVATE_MEDIA_ROOT: one directory per owner."""
        return f"{self.owner_id}/{self.stored_name}"

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @property
    def is_infected(self) -> bool:
        return self.scan_status == ScanStatus.INFECTED

    @property
    def is_clean(self) -> bool:
        return self.scan_status == ScanStatus.CLEAN

    @property
    def has_file(self) -> bool:
        return self.file_removed_at is None


# =================================================================================================
# A DOCUMENT AS A REQUIREMENT OF A CASE (REQ-DOC-01, REQ-DOC-04, REQ-DOC-05)
#
# ``PrivateDocument`` above answers "what file is stored, and is it safe". That is a question about
# a FILE. It is not the question a person has. A person asks: *what is still missing from my file,
# who is waiting for it, and what happens next*. Those are two different questions, and conflating
# them is the defect this section exists to remove — the reserved area used to show an antivirus
# verdict ("En attente d'analyse") in the column where a person looked for their own status.
#
# So the requirement is the ROW and the files are VERSIONS INSIDE it (art direction A §13.3):
# re-uploading replaces the version in force and keeps the history, instead of adding another
# free-floating object the person has to reconcile by hand.
# =================================================================================================


class RequirementState(models.TextChoices):
    """
    The seven states visible to a person (PLATFORM_REQUIREMENTS_V2 §7, art direction A §13.3).

    Each is a WORD carrying a rule (``documents.requirements.STATE_RULES``), never a colour alone,
    and none of them means "approved": VALIDE says the piece received is the piece asked for, not
    that anything has been granted. This platform approves nobody (CONFLICT_REGISTER CR-11).
    """

    MISSING = "missing", _("Manquant")
    FILED = "filed", _("Déposé")
    IN_REVIEW = "in_review", _("En examen")
    VALID = "valid", _("Valide")
    INVALID = "invalid", _("Non valide")
    EXPIRED = "expired", _("Expiré")
    TO_REPLACE = "to_replace", _("À remplacer")


#: States that still need something from somebody. Used for ordering and for counts.
OPEN_STATES: frozenset[str] = frozenset(
    {
        RequirementState.MISSING,
        RequirementState.INVALID,
        RequirementState.EXPIRED,
        RequirementState.TO_REPLACE,
    }
)


class AccessClass(models.TextChoices):
    """
    Who, beyond the person, may read the file (REQ-DOC-01, « classe di accesso »).

    CASE is the default: the people actually working on the case file, and only while their mandate
    is live. RESTRICTED keeps a piece to the person and the administration — a family record naming
    children has no business being readable by a training body that needs a language certificate.
    """

    CASE = "case", _("Intervenants du dossier")
    RESTRICTED = "restricted", _("Personne concernée et administration seulement")


class DocumentRequirementQuerySet(models.QuerySet):
    def readable_by(self, user):
        """
        Authorisation applied AT QUERY TIME, never after the fact, and derived from the case file.

        Readable by the person whose case it is, by a live assignee of that case when the access
        class allows it, and by the administration. ``role:staff`` gets nothing here, for the same
        reason ``cases.CaseFileQuerySet.readable_by`` gives it nothing: supervision happens in the
        back-office where every access is role-checked, not through a standing list of everybody's
        identity papers.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False) or not user.is_active:
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        today = timezone.localdate()
        assigned = (
            models.Q(case__assignments__assignee=user, case__assignments__revoked_at__isnull=True)
            & (
                models.Q(case__assignments__authorisation_valid_until__isnull=True)
                | models.Q(case__assignments__authorisation_valid_until__gte=today)
            )
            & models.Q(access_class=AccessClass.CASE)
        )
        return self.filter(models.Q(case__person=user) | assigned).distinct()

    def open(self):
        return self.filter(state__in=OPEN_STATES)


class DocumentRequirement(TimeStampedModel):
    """
    One piece a case file needs, the actor answerable for it, and where the obligation comes from.

    Deliberately NOT a field bolted onto ``cases.ChecklistItem``: a checklist item is a STEP
    ("obtain the declaration of value"), a requirement is an ARTEFACT with versions, an expiry and
    an access class. ``checklist_item`` links the two where they coincide, so the checklist keeps
    its single answer to "who is responsible" and this table keeps the file's life-cycle.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(
        "cases.CaseFile",
        on_delete=models.CASCADE,
        related_name="document_requirements",
        verbose_name=_("dossier"),
    )
    checklist_item = models.ForeignKey(
        "cases.ChecklistItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_requirements",
        verbose_name=_("élément de checklist"),
        help_text=_("L’étape de la checklist que cette pièce satisfait, lorsqu’elle en satisfait une."),
    )
    code = models.SlugField(
        _("clé"),
        max_length=64,
        help_text=_("Clé stable de l’exigence dans ce dossier."),
    )
    order = models.PositiveIntegerField(_("ordre"), default=0)
    title = models.CharField(_("pièce demandée"), max_length=300)
    detail = models.TextField(_("précisions"), blank=True)
    kind = models.CharField(_("type"), max_length=10, choices=DocumentKind.choices, default=DocumentKind.OTHER)
    responsible_actor = models.CharField(
        _("responsable"),
        max_length=20,
        choices=ResponsibleActor.choices,
        help_text=_("Qui doit fournir la pièce. Une exigence anonyme n’est pas une exigence."),
    )
    responsible_note = models.CharField(_("précision sur le responsable"), max_length=200, blank=True)
    mandatory = models.BooleanField(_("obligatoire"), default=True)
    due_date = models.DateField(_("échéance"), null=True, blank=True)
    access_class = models.CharField(
        _("classe d’accès"), max_length=12, choices=AccessClass.choices, default=AccessClass.CASE
    )
    source_title = models.CharField(_("source"), max_length=200, blank=True)
    source_ref = models.CharField(_("référence de la source"), max_length=300, blank=True)
    source_url = models.URLField(_("lien de la source"), max_length=500, blank=True)
    #: Cached copy of ``documents.requirements.derive_state``. The interface reads the DERIVED
    #: value, so an expiry is honest the second it happens; this column exists so a queryset can
    #: count and filter without loading every row, and ``documents_refresh_requirements``
    #: reconciles it and audits every change it makes.
    state = models.CharField(
        _("état"), max_length=12, choices=RequirementState.choices, default=RequirementState.MISSING, db_index=True
    )
    state_note = models.CharField(_("motif de l’état"), max_length=300, blank=True)
    replacement_requested_at = models.DateTimeField(_("remplacement demandé le"), null=True, blank=True)
    replacement_reason = models.CharField(_("motif du remplacement"), max_length=300, blank=True)
    language = models.CharField(_("langue du texte"), max_length=8, default="fr", editable=False)

    objects = DocumentRequirementQuerySet.as_manager()

    class Meta:
        verbose_name = _("pièce exigée")
        verbose_name_plural = _("pièces exigées")
        ordering = ["case", "order", "title"]
        constraints = [models.UniqueConstraint(fields=["case", "code"], name="docreq_unique_code_per_case")]
        indexes = [
            models.Index(fields=["case", "state"], name="docreq_case_state_idx"),
            models.Index(fields=["state", "due_date"], name="docreq_state_due_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.title[:60]}"

    def clean(self) -> None:
        # Same acceptance criterion as the checklist: a requirement that cannot say who must act on
        # it is not a requirement, it is a worry.
        if not self.responsible_actor:
            raise ValidationError({"responsible_actor": _("Chaque pièce doit indiquer un responsable.")})

    # -- versions ------------------------------------------------------------------------------
    @property
    def current_version(self):
        """The version in force. Versions live inside the row; exactly one is current at a time."""
        for version in self.versions.all():  # prefetch-friendly: no extra query once prefetched
            if version.is_current:
                return version
        return None

    # -- state ---------------------------------------------------------------------------------
    def derived_state(self, *, today=None) -> str:
        from documents.requirements import derive_state

        return derive_state(self, self.current_version, today=today)

    @property
    def display_state(self) -> str:
        return self.derived_state()

    @property
    def is_open(self) -> bool:
        return self.display_state in OPEN_STATES

    @property
    def is_overdue(self) -> bool:
        # the project's clock, as every deadline of the interface (requirements.due_urgency, the deadlines page): on a
        # lane or the preview a reference date stands in for today, and one clock decides one deadline (REVIEW M3)
        return bool(self.due_date and self.is_open and self.due_date < clock.today())


class VersionDecision(models.TextChoices):
    """What a HUMAN reviewer concluded about this version. Never what a scanner concluded."""

    PENDING = "pending", _("En attente d’examen")
    IN_REVIEW = "in_review", _("En examen")
    ACCEPTED = "accepted", _("Pièce acceptée")
    REFUSED = "refused", _("Pièce refusée")


class DocumentVersionQuerySet(models.QuerySet):
    def current(self):
        return self.filter(is_current=True)

    def readable_by(self, user):
        return self.filter(requirement__in=DocumentRequirement.objects.readable_by(user))


class DocumentVersion(TimeStampedModel):
    """
    One deposit against a requirement. Re-uploading supersedes the previous version and keeps it.

    The file itself stays a ``PrivateDocument``: one storage path, one validation chain, one
    download view, one audit trail. This row adds only what a version needs — its rank, when it
    stopped being the one in force, when the piece it carries expires, and what a reviewer said.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requirement = models.ForeignKey(
        DocumentRequirement, on_delete=models.CASCADE, related_name="versions", verbose_name=_("pièce exigée")
    )
    number = models.PositiveIntegerField(_("version"))
    document = models.ForeignKey(
        PrivateDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requirement_versions",
        verbose_name=_("fichier"),
        help_text=_("Vide lorsque le fichier a été purgé : la version demeure comme trace."),
    )
    filed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_versions_filed",
        verbose_name=_("déposé par"),
    )
    is_current = models.BooleanField(_("version en vigueur"), default=True)
    superseded_at = models.DateTimeField(_("remplacée le"), null=True, blank=True)
    expires_on = models.DateField(
        _("la pièce expire le"),
        null=True,
        blank=True,
        help_text=_("Date de validité de la pièce elle-même (passeport, titre, certificat)."),
    )
    decision = models.CharField(
        _("examen"), max_length=12, choices=VersionDecision.choices, default=VersionDecision.PENDING
    )
    decision_note = models.CharField(_("motif de l’examen"), max_length=300, blank=True)
    decided_at = models.DateTimeField(_("examiné le"), null=True, blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="document_versions_reviewed",
        verbose_name=_("examiné par"),
    )

    objects = DocumentVersionQuerySet.as_manager()

    class Meta:
        verbose_name = _("version de pièce")
        verbose_name_plural = _("versions de pièce")
        ordering = ["requirement", "-number"]
        constraints = [
            models.UniqueConstraint(fields=["requirement", "number"], name="docver_unique_number"),
            models.UniqueConstraint(
                fields=["requirement"], condition=models.Q(is_current=True), name="docver_one_current"
            ),
        ]

    def __str__(self) -> str:
        return f"v{self.number}"

    @property
    def has_file(self) -> bool:
        doc = self.document
        return bool(doc and doc.deleted_at is None and doc.has_file and not doc.is_infected)
