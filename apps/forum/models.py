"""
Forum Vénétie–Maroc (Phase 2) → Forum Permanent Vénétie–Maroc (after 2 Oct 2026).

Prescribed texts (``p2.forum.*``) are NEVER stored here: the page reads them from the locked
registry through ``ForumEvent.locked_key_prefix``. The database holds only what the document
says is editable from the back-office (programme, speaker functions, partners, registrations,
and the permanent-mode collections: media, documents, interventions, agreements, outcomes,
next events).

Gates implemented as data + code (docs/LEGAL_AND_PUBLICATION_GATES.md):
* G4 — event/permanent mode: ``FeatureFlag forum_permanent_mode`` OR ``mode_override``.
* G5 — speaker names: ``SpeakerRole.names_authorized`` AND flag ``forum_speaker_names_authorized``.
* G6 — partner logos: ``ForumPartner.authorized`` AND a logo file.
"""

from __future__ import annotations

import datetime as dt

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.models import PublishableModel
from core import clock
from core.models import TimeStampedModel
from forum.validators import validate_media_file, validate_pdf

DEFAULT_LOCKED_PREFIX = "p2.forum"
SPEAKER_NAMES_FLAG = "forum_speaker_names_authorized"
PERMANENT_MODE_FLAG = "forum_permanent_mode"

# The prescribed category labels (document §2.1) — order is binding; values are technical keys.
_CATEGORY_LABELS: list[str] = list(locked_content.get("p2.forum.registration.categories", "fr")[0])


class ForumMode(models.TextChoices):
    EVENT = "event", _("Événement (page d’inscription)")
    PERMANENT = "permanent", _("Forum permanent (archives, résultats, suites)")


class ModeOverride(models.TextChoices):
    AUTO = "auto", _("Automatique (drapeau forum_permanent_mode)")
    EVENT = "event", _("Forcer le mode événement")
    PERMANENT = "permanent", _("Forcer le mode Forum permanent")


class ForumEvent(PublishableModel):
    """One edition of the Forum. The Rovigo edition (2 Oct 2026) is seeded and marked primary."""

    slug = models.SlugField(_("slug"), max_length=80, unique=True)
    locked_key_prefix = models.CharField(
        _("préfixe des textes prescrits"),
        max_length=40,
        default=DEFAULT_LOCKED_PREFIX,
        help_text=_("Préfixe du registre des textes bloqués (ex. p2.forum). Les textes ne sont pas modifiables ici."),
    )
    is_primary = models.BooleanField(
        _("édition affichée sur la page Forum"),
        default=False,
        help_text=_("Une seule édition peut être affichée à la fois sur /forum/."),
    )
    mode_override = models.CharField(
        _("mode de la page"),
        max_length=10,
        choices=ModeOverride.choices,
        default=ModeOverride.AUTO,
        help_text=_(
            "Automatique : la page passe en « Forum permanent » lorsque le drapeau forum_permanent_mode est actif "
            "(par défaut après le 2 octobre 2026, 18h00 Europe/Rome)."
        ),
    )
    date = models.DateField(_("date"), default=dt.date(2026, 10, 2))
    start_time = models.TimeField(_("début"), default=dt.time(15, 0))
    end_time = models.TimeField(_("fin"), default=dt.time(18, 0))
    venue = models.CharField(_("lieu"), max_length=160, default="Sala della Gran Guardia")
    city = models.CharField(_("ville"), max_length=120, default="Rovigo")
    country_code = models.CharField(_("pays (ISO)"), max_length=2, default="IT")
    registration_open = models.BooleanField(_("inscriptions ouvertes"), default=True)
    registration_deadline = models.DateTimeField(_("clôture des inscriptions"), null=True, blank=True)
    capacity = models.PositiveIntegerField(
        _("capacité (optionnelle)"),
        null=True,
        blank=True,
        help_text=_("Si renseignée, les inscriptions se ferment automatiquement une fois la capacité atteinte."),
    )
    hero_image = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("image d’en-tête"),
    )

    class Meta:
        verbose_name = _("édition du Forum")
        verbose_name_plural = _("éditions du Forum")
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_primary"], condition=models.Q(is_primary=True), name="uniq_forum_primary_event"
            ),
            models.CheckConstraint(condition=models.Q(start_time__lt=models.F("end_time")), name="forum_event_times"),
        ]

    def __str__(self) -> str:
        return f"{self.slug} ({self.date:%d.%m.%Y})"

    # -- prescribed texts -------------------------------------------------------------------
    def locked_key(self, suffix: str) -> str:
        return f"{self.locked_key_prefix}.{suffix}"

    def locked_text(self, suffix: str, language: str | None = None) -> str:
        try:
            value, effective = locked_content.get(self.locked_key(suffix), language)
        except locked_content.LockedContentMissing:
            return ""
        if not isinstance(value, str):
            return ""
        # LockedText is a str that remembers its language: breadcrumbs mark the French fallback.
        requested = (language or locked_content.FALLBACK_LANGUAGE).split("-")[0]
        return locked_content.LockedText(value, effective, requested)

    # -- time -------------------------------------------------------------------------------
    @property
    def starts_at(self) -> dt.datetime:
        return dt.datetime.combine(self.date, self.start_time, tzinfo=settings.ROME)

    @property
    def ends_at(self) -> dt.datetime:
        return dt.datetime.combine(self.date, self.end_time, tzinfo=settings.ROME)

    def has_ended(self, now: dt.datetime | None = None) -> bool:
        return (now or clock.now()) >= self.ends_at

    # -- gates ------------------------------------------------------------------------------
    def effective_mode(self, now: dt.datetime | None = None) -> str:
        from core import flags

        if self.mode_override == ModeOverride.PERMANENT:
            return ForumMode.PERMANENT
        if self.mode_override == ModeOverride.EVENT:
            return ForumMode.EVENT
        return ForumMode.PERMANENT if flags.is_enabled(PERMANENT_MODE_FLAG, now) else ForumMode.EVENT

    def is_permanent(self, now: dt.datetime | None = None) -> bool:
        return self.effective_mode(now) == ForumMode.PERMANENT

    def registration_is_open(self, now: dt.datetime | None = None) -> bool:
        now = now or clock.now()
        if self.effective_mode(now) != ForumMode.EVENT or not self.registration_open:
            return False
        if self.has_ended(now):
            return False
        if self.registration_deadline and now >= self.registration_deadline:
            return False
        if self.capacity:
            taken = self.registrations.exclude(status=RegistrationStatus.CANCELLED).count()
            if taken >= self.capacity:
                return False
        return True


class ForumProgramItem(TimeStampedModel):
    """Programme line. Seeded from ``p2.forum.programme.items``; editable in the back-office (§2.1)."""

    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="programme_items")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    time_label = models.CharField(_("horaire"), max_length=20, blank=True, help_text=_("ex. 15h00"))
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    description_fr = models.TextField(_("description (FR)"), blank=True)
    is_visible = models.BooleanField(_("visible"), default=True)
    is_locked_seed = models.BooleanField(_("issu du programme prescrit"), default=False, editable=False)
    locked_index = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("point du programme")
        verbose_name_plural = _("programme")

    def __str__(self) -> str:
        return f"{self.time_label + ' — ' if self.time_label else ''}{self.title_fr}"


class SpeakerRole(TimeStampedModel):
    """
    Institutional function of a speaker. The person's name is NEVER shown publicly unless the
    record is authorised in writing AND the site-wide flag ``forum_speaker_names_authorized`` is on.
    """

    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="speaker_roles")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    role_label_fr = models.CharField(_("fonction (FR)"), max_length=200)
    person_name = models.CharField(
        _("nom de la personne"),
        max_length=160,
        blank=True,
        help_text=_(
            "ATTENTION — aucun nom de personnalité institutionnelle ne doit être publié sans transmission "
            "écrite de l’Avv. Badrane. Le nom reste invisible tant que « nom autorisé » n’est pas coché ET que "
            "le drapeau forum_speaker_names_authorized n’est pas actif."
        ),
    )
    organisation = models.CharField(_("organisation"), max_length=200, blank=True)
    names_authorized = models.BooleanField(
        _("nom autorisé à la publication"),
        default=False,
        help_text=_("Cocher uniquement après réception écrite du programme définitif (référence obligatoire)."),
    )
    authorization_reference = models.CharField(
        _("référence de l’autorisation"),
        max_length=200,
        blank=True,
        help_text=_("ex. « e-mail de l’Avv. Badrane du 2026-09-30 » — au moins 10 caractères."),
    )
    authorized_at = models.DateTimeField(_("autorisé le"), null=True, blank=True)
    is_visible = models.BooleanField(_("visible"), default=True)
    is_locked_seed = models.BooleanField(_("issu du texte prescrit"), default=False, editable=False)
    locked_index = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("intervenant (fonction)")
        verbose_name_plural = _("intervenants (fonctions)")

    def __str__(self) -> str:
        return self.role_label_fr

    def clean(self) -> None:
        super().clean()
        if self.names_authorized and len(self.authorization_reference.strip()) < 10:
            raise ValidationError(
                {"authorization_reference": _("Indiquer la référence écrite de l’autorisation (≥ 10 caractères).")}
            )

    def save(self, *args, **kwargs):
        if self.names_authorized and not self.authorized_at:
            self.authorized_at = clock.now()
        if not self.names_authorized:
            self.authorized_at = None
        super().save(*args, **kwargs)

    def public_name(self, site_flag_enabled: bool) -> str:
        """Name shown to the public — empty unless both authorisations are present (gate G5)."""
        if self.names_authorized and site_flag_enabled and len(self.authorization_reference.strip()) >= 10:
            return self.person_name.strip()
        return ""


class RegistrationCategory(models.TextChoices):
    INSTITUTION = "institution", _CATEGORY_LABELS[0]
    COMPANY = "company", _CATEGORY_LABELS[1]
    PROFESSIONAL_ASSOCIATION = "professional_association", _CATEGORY_LABELS[2]
    UNIVERSITY_TRAINING = "university_training", _CATEGORY_LABELS[3]
    PROFESSIONAL = "professional", _CATEGORY_LABELS[4]
    LABOUR_BODY = "labour_body", _CATEGORY_LABELS[5]
    DIPLOMATIC_CONSULAR = "diplomatic_consular", _CATEGORY_LABELS[6]
    OTHER = "other", _CATEGORY_LABELS[7]


class RegistrationStatus(models.TextChoices):
    PENDING = "pending", _("Reçue")
    CONFIRMED = "confirmed", _("Confirmée")
    CANCELLED = "cancelled", _("Annulée")
    ATTENDED = "attended", _("Présente")


class ForumRegistration(TimeStampedModel):
    """Public registration (data minimisation: only the prescribed fields)."""

    event = models.ForeignKey(ForumEvent, on_delete=models.PROTECT, related_name="registrations")
    first_name = models.CharField(_("prénom"), max_length=80)
    last_name = models.CharField(_("nom"), max_length=80)
    organisation = models.CharField(_("organisme / entreprise"), max_length=200, blank=True)
    role = models.CharField(_("fonction"), max_length=160, blank=True)
    email = models.EmailField(_("e-mail"), db_index=True)
    phone = models.CharField(_("téléphone"), max_length=40, blank=True)
    country = models.CharField(_("pays"), max_length=80, blank=True)
    category = models.CharField(_("catégorie"), max_length=32, choices=RegistrationCategory.choices, db_index=True)
    sector_of_interest = models.CharField(_("secteur d’intérêt"), max_length=300, blank=True)
    consent = models.ForeignKey("consents.ConsentRecord", on_delete=models.PROTECT, related_name="forum_registrations")
    status = models.CharField(
        _("statut"),
        max_length=10,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
        db_index=True,
    )
    admin_notes = models.TextField(_("notes internes"), blank=True)
    language = models.CharField(_("langue"), max_length=5, default="fr")
    ip_hash = models.CharField(max_length=32, blank=True, editable=False)
    user_agent = models.CharField(max_length=160, blank=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="forum_registrations",
        verbose_name=_("compte lié"),
    )
    invited_to_virtual_forum = models.BooleanField(_("invité au Forum Virtuel"), default=False)
    last_contact_at = models.DateTimeField(_("dernier contact"), null=True, blank=True)
    anonymised_at = models.DateTimeField(_("anonymisée le"), null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("inscription au Forum")
        verbose_name_plural = _("inscriptions au Forum")
        constraints = [
            models.UniqueConstraint(models.F("event"), Lower("email"), name="uniq_forum_registration_event_email_ci"),
        ]
        indexes = [models.Index(fields=["event", "status"])]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} — {self.get_category_display()}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_anonymised(self) -> bool:
        return self.anonymised_at is not None

    def save(self, *args, **kwargs):
        self.email = (self.email or "").strip().lower()
        if not self.last_contact_at:
            self.last_contact_at = clock.now()
        super().save(*args, **kwargs)


class PartnerKind(models.TextChoices):
    PATRON = "patron", _("Patronage")
    INSTITUTIONAL = "institutional", _("Partenaire institutionnel")
    PARTNER = "partner", _("Partenaire")
    SPONSOR = "sponsor", _("Soutien")


class ForumPartner(TimeStampedModel):
    """Logo slot. Rendered publicly ONLY when authorised in writing AND a logo file exists (gate G6)."""

    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="partners")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    name = models.CharField(_("dénomination"), max_length=200)
    kind = models.CharField(_("type"), max_length=16, choices=PartnerKind.choices, default=PartnerKind.PARTNER)
    logo = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("logo"),
        help_text=_("Charger uniquement les logos transmis avec autorisation écrite. Jamais de logo téléchargé."),
    )
    website = models.CharField(
        _("site web (référence interne)"),
        max_length=300,
        blank=True,
        validators=[URLValidator(schemes=["https", "http"])],
        help_text=_("Non affiché publiquement (politique de sécurité : aucune ressource externe)."),
    )
    authorized = models.BooleanField(_("logo autorisé"), default=False)
    authorization_reference = models.CharField(_("référence de l’autorisation"), max_length=200, blank=True)
    note = models.CharField(_("note interne"), max_length=200, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("partenaire / logo")
        verbose_name_plural = _("partenaires / logos")
        constraints = [models.UniqueConstraint(fields=["event", "name"], name="uniq_forum_partner_name")]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()
        if self.authorized and len(self.authorization_reference.strip()) < 10:
            raise ValidationError(
                {"authorization_reference": _("Indiquer la référence écrite de l’autorisation (≥ 10 caractères).")}
            )

    @property
    def is_public(self) -> bool:
        return bool(self.authorized and self.logo_id and len(self.authorization_reference.strip()) >= 10)


class MediaKind(models.TextChoices):
    PHOTO = "photo", _("Photo")
    VIDEO = "video", _("Vidéo")


class ForumMedia(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="media_items")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    kind = models.CharField(_("type"), max_length=6, choices=MediaKind.choices, default=MediaKind.PHOTO)
    asset = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("image de la médiathèque"),
    )
    file = models.FileField(
        _("fichier (vidéo ou photo)"),
        upload_to="forum/media/%Y/%m/",
        blank=True,
        validators=[validate_media_file],
        help_text=_("JPG, PNG, WebP, MP4 ou WebM — 60 Mo max. Aucune vidéo externe (YouTube, etc.)."),
    )
    caption = models.CharField(_("légende"), max_length=200, blank=True)
    credit = models.CharField(_("crédit"), max_length=160, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("photo / vidéo")
        verbose_name_plural = _("photos et vidéos")

    def __str__(self) -> str:
        return self.caption or f"{self.get_kind_display()} #{self.pk}"

    def clean(self) -> None:
        super().clean()
        if not self.asset_id and not self.file:
            raise ValidationError(_("Indiquer une image de la médiathèque ou charger un fichier."))
        if self.kind == MediaKind.VIDEO and not self.file:
            raise ValidationError({"file": _("Une vidéo doit être chargée comme fichier.")})

    @property
    def url(self) -> str:
        if self.file:
            return self.file.url
        if self.asset_id and self.asset.file:
            return self.asset.file.url
        return ""

    def alt(self, lang: str) -> str:
        if self.asset_id:
            return self.asset.alt(lang)
        return self.caption


class ForumDocument(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="documents")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    title = models.CharField(_("titre"), max_length=200)
    file = models.FileField(
        _("fichier PDF"),
        upload_to="forum/documents/%Y/%m/",
        validators=[validate_pdf],
        help_text=_("Documents PUBLICS uniquement (aucune donnée personnelle). PDF, 10 Mo max."),
    )
    description = models.TextField(_("description"), blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self) -> str:
        return self.title


class ForumIntervention(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="interventions")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    speaker = models.ForeignKey(
        SpeakerRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interventions",
        verbose_name=_("intervenant"),
        help_text=_(
            "Le nom n’apparaît que si la fonction est autorisée (gate G5) ; sinon seule la fonction s’affiche."
        ),
    )
    title = models.CharField(_("titre"), max_length=200)
    abstract = models.TextField(_("résumé"), blank=True)
    document = models.ForeignKey(
        ForumDocument, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("document")
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("intervention")
        verbose_name_plural = _("interventions")

    def __str__(self) -> str:
        return self.title


class AgreementKind(models.TextChoices):
    ACCORD = "accord", _("Accord")
    CONVENTION = "convention", _("Convention")


class ForumAgreement(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="agreements")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    kind = models.CharField(_("type"), max_length=10, choices=AgreementKind.choices, default=AgreementKind.ACCORD)
    title = models.CharField(_("titre"), max_length=200)
    parties = models.CharField(_("parties"), max_length=300)
    signed_on = models.DateField(_("date de signature"), null=True, blank=True)
    summary = models.TextField(_("résumé"), blank=True)
    document = models.ForeignKey(
        ForumDocument, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("document")
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("accord / convention")
        verbose_name_plural = _("accords et conventions")

    def __str__(self) -> str:
        return self.title


class ForumOutcome(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="outcomes")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    title = models.CharField(_("titre"), max_length=200)
    text = models.TextField(_("texte"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("résultat")
        verbose_name_plural = _("résultats")

    def __str__(self) -> str:
        return self.title


class ForumNextEvent(PublishableModel):
    event = models.ForeignKey(ForumEvent, on_delete=models.CASCADE, related_name="next_events")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    title = models.CharField(_("titre"), max_length=200)
    date = models.DateField(_("date"))
    place = models.CharField(_("lieu"), max_length=200, blank=True)
    description = models.TextField(_("description"), blank=True)
    url = models.CharField(
        _("lien"),
        max_length=300,
        blank=True,
        help_text=_("Chemin interne (ex. /fr/forum/) rendu comme lien ; une adresse externe est affichée en texte."),
    )

    class Meta:
        ordering = ["date", "order", "id"]
        verbose_name = _("prochain rendez-vous")
        verbose_name_plural = _("prochains rendez-vous")

    def __str__(self) -> str:
        return f"{self.title} ({self.date:%d.%m.%Y})"

    @property
    def internal_url(self) -> str:
        url = (self.url or "").strip()
        return url if url.startswith("/") and not url.startswith("//") else ""


# =================================================================================================
# The authenticated governance module
# =================================================================================================
# Everything above is the PUBLIC Forum: the event page, its programme, its partners and its
# registrations. ``forum.governance`` holds the other half of the same name — editions, commissions,
# tables, proposals, projects, milestones, monitoring and the annual report — and it is imported
# here rather than written here for one reason: it is a different product with a different reader.
# The public half is read by anyone; the governance half is read by whoever holds a live mandate,
# and only while the ``virtual_forum`` flag is open.
#
# The import is at the BOTTOM so that ``forum.governance`` can name ``forum.ForumEvent`` by string
# reference without a circular import, and it is re-exported so that ``from forum.models import
# ForumProposal`` keeps working the way every other app in this codebase is written.
from forum.governance import (  # noqa: E402,F401 — models must be imported for Django to register them
    ALLOWED_PROJECT_TRANSITIONS,
    ALLOWED_PROPOSAL_TRANSITIONS,
    DECISION_PROPOSAL_STATUSES,
    FORBIDDEN_PROFILE_FIELDS,
    OPEN_MILESTONE_STATUSES,
    PRE_DECISION_PROPOSAL_STATUSES,
    PUBLIC_PROFILE_KEYS,
    AnnualReport,
    Commission,
    CommissionMember,
    CommissionStatus,
    EditionStatus,
    ForumEdition,
    ForumProfile,
    ForumProject,
    ForumProposal,
    ForumRole,
    MandateRole,
    MilestoneStatus,
    MonitoringEntry,
    ParticipantCategory,
    ProjectMilestone,
    ProjectStatus,
    ProposalStatus,
    ReportStatus,
    Table,
    TableStatus,
    project_transitions_from,
    proposal_transitions_from,
)
