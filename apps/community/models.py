"""
Forum Virtuel (gate G11 — FeatureFlag ``virtual_forum``).

Privacy by design: a member is identified to other members ONLY through what they explicitly
chose to show (``show_name``, ``show_organisation`` — both default False). E-mail addresses never
reach a template seen by another member. Rooms restrict access by participant category; posts
are plain text (auto-escaped) and can be queued for moderation.
"""

from __future__ import annotations

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from core.models import TimeStampedModel

# The eight participant categories are prescribed (p2.forum.registration.categories). Labels come
# from the locked registry — never typed by hand — and technical keys mirror forum registration.
_CATEGORY_LABELS: list[str] = list(locked_content.get("p2.forum.registration.categories", "fr")[0])


class HttpsURLField(models.URLField):
    """URLField whose admin form assumes https (silences the Django 6.0 scheme deprecation)."""

    def formfield(self, **kwargs):
        kwargs.setdefault("assume_scheme", "https")
        return super().formfield(**kwargs)


class ParticipantCategory(models.TextChoices):
    INSTITUTION = "institution", _CATEGORY_LABELS[0]
    COMPANY = "company", _CATEGORY_LABELS[1]
    PROFESSIONAL_ASSOCIATION_CHAMBER = "professional_association_chamber", _CATEGORY_LABELS[2]
    UNIVERSITY_TRAINING = "university_training", _CATEGORY_LABELS[3]
    PROFESSIONAL = "professional", _CATEGORY_LABELS[4]
    LABOUR_BODY = "labour_body", _CATEGORY_LABELS[5]
    DIPLOMATIC_CONSULAR = "diplomatic_consular", _CATEGORY_LABELS[6]
    OTHER = "other", _CATEGORY_LABELS[7]


def validate_categories(value) -> None:
    if not isinstance(value, list):
        raise ValidationError(_("Indicare una lista di categorie."))
    unknown = [v for v in value if v not in ParticipantCategory.values]
    if unknown:
        raise ValidationError(_("Categorie sconosciute: %(values)s") % {"values": ", ".join(map(str, unknown))})


class MembershipStatus(models.TextChoices):
    PENDING = "pending", _("In attesa di approvazione")
    APPROVED = "approved", _("Approvato")
    SUSPENDED = "suspended", _("Sospeso")


class Membership(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="community_membership")
    category = models.CharField(_("categoria"), max_length=40, choices=ParticipantCategory.choices, db_index=True)
    organisation = models.CharField(_("organismo / impresa"), max_length=200, blank=True)
    status = models.CharField(
        _("stato"), max_length=10, choices=MembershipStatus.choices, default=MembershipStatus.PENDING, db_index=True
    )
    accepted_terms_at = models.DateTimeField(_("condizioni accettate il"), null=True, blank=True)
    consent = models.ForeignKey(
        "consents.ConsentRecord", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    show_name = models.BooleanField(
        _("mostra il nome agli altri membri"), default=False, help_text=_("Scelta del membro; mai attiva per default.")
    )
    show_organisation = models.BooleanField(_("mostra l'organismo agli altri membri"), default=False)
    trusted = models.BooleanField(
        _("membro affidabile"),
        default=False,
        help_text=_("Se attivo, i messaggi non passano dalla coda di moderazione nelle stanze moderate."),
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    suspended_reason = models.CharField(_("motivo della sospensione"), max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("membro del Forum Virtuale")
        verbose_name_plural = _("membri del Forum Virtuale")

    def __str__(self) -> str:
        return f"Membro #{self.pk} ({self.get_category_display()}, {self.status})"

    @property
    def is_approved(self) -> bool:
        return self.status == MembershipStatus.APPROVED

    def public_label(self) -> str:
        """What OTHER members may see. Defaults reveal nothing personal."""
        name = self.user.full_name.strip() if self.show_name and self.user.full_name else ""
        organisation = self.organisation.strip() if self.show_organisation and self.organisation else ""
        if name and organisation:
            return f"{name} — {organisation}"
        if name:
            return name
        if organisation:
            return organisation
        return str(_("Participant"))


class RoomKind(models.TextChoices):
    ENTERPRISES = "enterprises", _("Entreprises")
    UNIVERSITIES = "universities", _("Universités et formation")
    INSTITUTIONS = "institutions", _("Institutions")
    GENERAL = "general", _("Espace commun")


class RoomQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def for_category(self, category: str):
        return self.published().filter(
            models.Q(allowed_categories=[]) | models.Q(allowed_categories__contains=[category])
        )


class Room(TimeStampedModel):
    slug = models.SlugField(max_length=60, unique=True)
    name_fr = models.CharField(_("nome (FR)"), max_length=120)
    description_fr = models.TextField(_("descrizione (FR)"), blank=True)
    kind = models.CharField(_("tipo"), max_length=12, choices=RoomKind.choices, default=RoomKind.GENERAL)
    is_moderated = models.BooleanField(_("moderata"), default=True)
    allowed_categories = models.JSONField(
        _("categorie ammesse"),
        default=list,
        blank=True,
        validators=[validate_categories],
        help_text=_("Lista vuota = tutte le categorie."),
    )
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    published = models.BooleanField(_("pubblicata"), default=False)

    objects = RoomQuerySet.as_manager()

    class Meta:
        ordering = ["order", "name_fr"]
        verbose_name = _("stanza tematica")
        verbose_name_plural = _("stanze tematiche")

    def __str__(self) -> str:
        return self.name_fr

    def allows(self, category: str) -> bool:
        return not self.allowed_categories or category in self.allowed_categories


class DiscussionStatus(models.TextChoices):
    OPEN = "open", _("Aperta")
    CLOSED = "closed", _("Chiusa")
    HIDDEN = "hidden", _("Nascosta")


class Discussion(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="discussions")
    author = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, related_name="discussions")
    title = models.CharField(_("titolo"), max_length=200)
    status = models.CharField(
        _("stato"), max_length=10, choices=DiscussionStatus.choices, default=DiscussionStatus.OPEN, db_index=True
    )
    pinned = models.BooleanField(_("in evidenza"), default=False)
    last_activity_at = models.DateTimeField(_("ultima attività"), db_index=True)

    class Meta:
        ordering = ["-pinned", "-last_activity_at"]
        verbose_name = _("discussione")
        verbose_name_plural = _("discussioni")

    def __str__(self) -> str:
        return self.title

    @property
    def is_open(self) -> bool:
        return self.status == DiscussionStatus.OPEN


class PostStatus(models.TextChoices):
    VISIBLE = "visible", _("Visibile")
    HIDDEN = "hidden", _("Nascosto")
    PENDING_MODERATION = "pending_moderation", _("In attesa di moderazione")


class Post(TimeStampedModel):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, related_name="posts")
    body = models.TextField(_("testo"), validators=[MaxLengthValidator(8000)])
    status = models.CharField(
        _("stato"), max_length=20, choices=PostStatus.choices, default=PostStatus.VISIBLE, db_index=True
    )
    edited_at = models.DateTimeField(null=True, blank=True)
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("messaggio")
        verbose_name_plural = _("messaggi")
        indexes = [models.Index(fields=["discussion", "status", "created_at"])]

    def __str__(self) -> str:
        return f"Post #{self.pk} in {self.discussion_id}"

    @property
    def is_visible(self) -> bool:
        return self.status == PostStatus.VISIBLE


class PendingPost(Post):
    """Proxy used by the back-office moderation queue."""

    class Meta:
        proxy = True
        verbose_name = _("messaggio in coda di moderazione")
        verbose_name_plural = _("coda di moderazione")


class Attachment(TimeStampedModel):
    """
    File shared in a post. The file itself is a private document managed by the ``documents`` app
    (allow-listed MIME types, random names, storage outside MEDIA_ROOT, authorised download).

    TODO(documents): replace ``document_uuid`` by ``ForeignKey("documents.PrivateDocument")`` once the
    documents app ships its model, and extend its download policy to room members (see report).
    Uploads are disabled in the UI until then; the model keeps the structure ready.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")
    document_uuid = models.UUIDField(_("documento privato (uuid)"), null=True, blank=True, db_index=True)
    label = models.CharField(_("etichetta"), max_length=160)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("allegato")
        verbose_name_plural = _("allegati")

    def __str__(self) -> str:
        return self.label

    def document(self):
        """Resolve the private document lazily; None while the documents app is not available."""
        if not self.document_uuid:
            return None
        try:
            model = apps.get_model("documents", "PrivateDocument")
        except LookupError:
            return None
        return model.objects.filter(uuid=self.document_uuid).first()


class ReportStatus(models.TextChoices):
    OPEN = "open", _("Aperta")
    HANDLED = "handled", _("Gestita")
    DISMISSED = "dismissed", _("Archiviata senza seguito")


class Report(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, related_name="reports")
    reason = models.TextField(_("motivo"), validators=[MaxLengthValidator(2000)])
    status = models.CharField(
        _("stato"), max_length=10, choices=ReportStatus.choices, default=ReportStatus.OPEN, db_index=True
    )
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    handled_at = models.DateTimeField(null=True, blank=True)
    handling_note = models.CharField(_("nota di gestione"), max_length=300, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["post", "reporter"], name="uniq_report_per_member")]
        verbose_name = _("segnalazione")
        verbose_name_plural = _("segnalazioni")

    def __str__(self) -> str:
        return f"Segnalazione #{self.pk} su post {self.post_id} [{self.status}]"


class ModerationActionKind(models.TextChoices):
    HIDE = "hide", _("Nascondi")
    UNHIDE = "unhide", _("Rendi visibile")
    APPROVE = "approve", _("Approva (coda di moderazione)")
    CLOSE = "close", _("Chiudi discussione")
    REOPEN = "reopen", _("Riapri discussione")
    WARN = "warn", _("Avverti il membro")
    SUSPEND = "suspend", _("Sospendi il membro")
    REINSTATE = "reinstate", _("Riattiva il membro")


class ModerationAction(TimeStampedModel):
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="community_moderation_actions"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="moderation_actions")
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, null=True, blank=True, related_name="moderation_actions"
    )
    membership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, null=True, blank=True, related_name="moderation_actions"
    )
    action = models.CharField(_("azione"), max_length=12, choices=ModerationActionKind.choices)
    note = models.CharField(_("nota"), max_length=300, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("azione di moderazione")
        verbose_name_plural = _("azioni di moderazione")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(post__isnull=False)
                | models.Q(discussion__isnull=False)
                | models.Q(membership__isnull=False),
                name="moderation_action_has_target",
            )
        ]

    def __str__(self) -> str:
        return f"{self.get_action_display()} ({self.created_at:%Y-%m-%d %H:%M})"


class CalendarEntry(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, related_name="calendar_entries")
    title = models.CharField(_("titolo"), max_length=200)
    description = models.TextField(_("descrizione"), blank=True)
    starts_at = models.DateTimeField(_("inizio"), db_index=True)
    ends_at = models.DateTimeField(_("fine"), null=True, blank=True)
    place = models.CharField(_("luogo"), max_length=200, blank=True)
    online_url = HttpsURLField(_("collegamento online"), blank=True)
    published = models.BooleanField(_("pubblicato"), default=False)

    class Meta:
        ordering = ["starts_at"]
        verbose_name = _("appuntamento")
        verbose_name_plural = _("calendario")

    def __str__(self) -> str:
        return f"{self.title} ({self.starts_at:%Y-%m-%d})"

    def clean(self):
        super().clean()
        if self.ends_at and self.starts_at and self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": _("La fine deve seguire l'inizio.")})


class InitiativeStatus(models.TextChoices):
    PROPOSED = "proposed", _("Proposta")
    ACTIVE = "active", _("Attiva")
    CLOSED = "closed", _("Chiusa")


class Initiative(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="initiatives")
    title = models.CharField(_("titolo"), max_length=200)
    description = models.TextField(_("descrizione"), blank=True)
    status = models.CharField(
        _("stato"), max_length=10, choices=InitiativeStatus.choices, default=InitiativeStatus.PROPOSED, db_index=True
    )
    owner = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True, related_name="initiatives")
    published = models.BooleanField(_("visibile ai membri"), default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("iniziativa")
        verbose_name_plural = _("iniziative")

    def __str__(self) -> str:
        return self.title


class CollaborationStatus(models.TextChoices):
    PROPOSED = "proposed", _("Proposta")
    ACTIVE = "active", _("In corso")
    CONCLUDED = "concluded", _("Conclusa")
    CLOSED = "closed", _("Chiusa")


class Collaboration(TimeStampedModel):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name="collaborations")
    organisation_names = models.CharField(
        _("organismi coinvolti"), max_length=400, help_text=_("Denominazioni degli organismi (mai persone).")
    )
    status = models.CharField(
        _("stato"), max_length=10, choices=CollaborationStatus.choices, default=CollaborationStatus.PROPOSED
    )
    note = models.CharField(_("nota"), max_length=300, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("collaborazione")
        verbose_name_plural = _("collaborazioni")

    def __str__(self) -> str:
        return f"{self.organisation_names} [{self.status}]"
