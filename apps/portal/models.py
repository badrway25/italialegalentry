"""
Espace réservé — foundation models (docs/REQUIREMENTS_MATRIX.md R-P3-034, R-POR-001).

* ``Message``      — staff-authored communication addressed to ONE account. Read-only for the person,
                     who may only mark it as read. Optional generic link to the record it is about.
* ``Deadline``     — a dated reminder attached to ONE account (document, procedure, training…). Dates
                     are always entered by the team from a written source (``source_note``): the
                     platform never computes or invents a legal time-limit.
* ``PortalNotice`` — staff-editable notice shown INSIDE the reserved area only (never public), with the
                     editorial workflow of ``cms.PublishableModel`` and an audience filter.

Privacy by design: every personal row has exactly one owner, querysets are always scoped by that
owner (``for_recipient`` / ``for_owner``) and object-level policies live in ``portal.policies``
(deny by default, ``accounts.permissions``). Messages use a UUID primary key so identifiers cannot be
enumerated from the portal URLs.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, PublishableQuerySet
from core import clock
from core.models import TimeStampedModel

DATA_MINIMISATION_HELP = _(
    "Minimisation des données : n’écrivez que ce qui est nécessaire au suivi de la personne concernée. "
    "Ne mentionnez jamais les données d’une autre personne ou d’une autre organisation."
)


# ---------------------------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------------------------
class MessageQuerySet(models.QuerySet):
    def for_recipient(self, user):
        if not getattr(user, "is_authenticated", False):
            return self.none()
        return self.filter(recipient=user)

    def visible(self, at=None):
        """Messages whose optional scheduling date has been reached."""
        at = at or clock.now()
        return self.filter(Q(visible_from__isnull=True) | Q(visible_from__lte=at))

    def unread(self):
        return self.filter(is_read=False)

    def inbox(self, user, at=None):
        """The only queryset the portal views ever use: own + visible, newest first."""
        return self.for_recipient(user).visible(at).order_by("-created_at")


class Message(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portal_messages",
        verbose_name=_("destinataire"),
        help_text=_("Le message n’est visible que par ce compte."),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        limit_choices_to={"is_staff": True},
        verbose_name=_("expéditeur (équipe)"),
        help_text=_("Renseigné automatiquement. L’identité de l’expéditeur n’est jamais affichée à la personne."),
    )
    subject = models.CharField(_("objet"), max_length=200)
    body = models.TextField(_("message (texte brut)"), help_text=DATA_MINIMISATION_HELP)
    is_read = models.BooleanField(_("lu"), default=False, editable=False, db_index=True)
    read_at = models.DateTimeField(_("lu le"), null=True, blank=True, editable=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("type de l’élément lié"),
    )
    object_id = models.CharField(_("identifiant de l’élément lié"), max_length=64, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")
    visible_from = models.DateTimeField(
        _("visible à partir du"),
        null=True,
        blank=True,
        help_text=_("Optionnel : le message reste invisible pour la personne jusqu’à cette date."),
    )

    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("communication")
        verbose_name_plural = _("communications")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"], name="portal_msg_rcpt_read_idx"),
            models.Index(fields=["recipient", "-created_at"], name="portal_msg_rcpt_date_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(is_read=False, read_at__isnull=True) | Q(is_read=True, read_at__isnull=False),
                name="portal_msg_read_consistent",
            ),
            # The (content_type, object_id) pair is validated in clean() only: content_type is
            # SET_NULL, so a DB constraint would turn the removal of a stale ContentType into an error.
        ]

    def __str__(self) -> str:
        # Deliberately NEUTRAL — no subject, no recipient e-mail. ``__str__`` is copied verbatim into
        # audit rows (``target_repr``), the application log and django.contrib.admin's LogEntry, all
        # of which outlive the GDPR erasure of the message itself. The back-office list shows the
        # subject in its own column.
        return f"Communication {self.reference}"

    def clean(self) -> None:
        super().clean()
        if self.object_id and not self.content_type_id:
            raise ValidationError({"content_type": _("Indiquez le type de l’élément lié.")})
        if self.content_type_id and not self.object_id:
            raise ValidationError({"object_id": _("Indiquez l’identifiant de l’élément lié.")})

    def is_visible(self, at=None) -> bool:
        return self.visible_from is None or self.visible_from <= (at or clock.now())

    @property
    def reference(self) -> str:
        return str(self.pk)[:8].upper()


# ---------------------------------------------------------------------------------------------
# Deadlines
# ---------------------------------------------------------------------------------------------
class DeadlineKind(models.TextChoices):
    DOCUMENT = "document", _("Document")
    PROCEDURE = "procedure", _("Démarche")
    TRAINING = "training", _("Formation")
    OTHER = "other", _("Autre")


class DeadlineStatus(models.TextChoices):
    OPEN = "open", _("À venir")
    DONE = "done", _("Terminée")
    CANCELLED = "cancelled", _("Annulée")


class DeadlineQuerySet(models.QuerySet):
    def for_owner(self, user):
        if not getattr(user, "is_authenticated", False):
            return self.none()
        return self.filter(owner=user)

    def open(self):
        return self.filter(status=DeadlineStatus.OPEN)

    def overdue(self, today=None):
        return self.open().filter(due_on__lt=today or clock.today())

    def upcoming(self, today=None):
        return self.open().filter(due_on__gte=today or clock.today())


class Deadline(TimeStampedModel):
    SOON_DAYS = 7

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portal_deadlines",
        verbose_name=_("compte concerné"),
        help_text=_("L’échéance n’est visible que par ce compte."),
    )
    title = models.CharField(_("intitulé"), max_length=200)
    due_on = models.DateField(_("date d’échéance"), db_index=True)
    description = models.TextField(_("description"), blank=True, help_text=DATA_MINIMISATION_HELP)
    kind = models.CharField(_("type"), max_length=10, choices=DeadlineKind.choices, default=DeadlineKind.OTHER)
    status = models.CharField(
        _("statut"), max_length=10, choices=DeadlineStatus.choices, default=DeadlineStatus.OPEN, db_index=True
    )
    source_note = models.CharField(
        _("origine de la date"),
        max_length=255,
        blank=True,
        help_text=_(
            "D’où vient cette date (courrier, convocation, programme de formation…). Affichée à la personne. "
            "La plateforme ne calcule jamais un délai légal : saisir uniquement une date communiquée par écrit."
        ),
    )

    objects = DeadlineQuerySet.as_manager()

    class Meta:
        verbose_name = _("échéance")
        verbose_name_plural = _("échéances")
        ordering = ["due_on", "id"]
        indexes = [models.Index(fields=["owner", "status", "due_on"], name="portal_deadline_owner_idx")]

    def __str__(self) -> str:
        # Neutral for the same reason as ``Message.__str__``: the title is free text written about a
        # person and must not leak into audit rows, logs or the admin LogEntry.
        return f"Échéance n° {self.pk}" if self.pk else "Échéance"

    @property
    def is_open(self) -> bool:
        return self.status == DeadlineStatus.OPEN

    def days_left(self, today=None) -> int:
        return (self.due_on - (today or clock.today())).days

    def is_overdue(self, today=None) -> bool:
        return self.is_open and self.days_left(today) < 0

    def is_soon(self, today=None) -> bool:
        return self.is_open and 0 <= self.days_left(today) <= self.SOON_DAYS


# ---------------------------------------------------------------------------------------------
# Notices (inside the reserved area only)
# ---------------------------------------------------------------------------------------------
class NoticeAudience(models.TextChoices):
    ALL = "all", _("Tous les comptes")
    PERSON = "person", _("Personnes")
    COMPANY = "company", _("Entreprises")
    INSTITUTION = "institution", _("Institutions")
    UNIVERSITY = "university", _("Universités / organismes de formation")
    PROFESSIONAL = "professional", _("Professionnels")


class PortalNoticeQuerySet(PublishableQuerySet):
    def for_audiences(self, audiences):
        return self.filter(audience__in=set(audiences) | {NoticeAudience.ALL})


class PortalNotice(PublishableModel):
    audience = models.CharField(
        _("public visé"), max_length=12, choices=NoticeAudience.choices, default=NoticeAudience.ALL, db_index=True
    )
    heading_fr = models.CharField("Titre (FR)", max_length=160)
    body_fr = models.TextField(
        "Texte (FR)",
        help_text=_(
            "Texte brut, affiché uniquement à l’intérieur de l’espace réservé. Aucune donnée personnelle, "
            "aucun contenu juridique non validé, aucune promesse de résultat."
        ),
    )
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)

    objects = PortalNoticeQuerySet.as_manager()

    class Meta:
        verbose_name = _("avis de l’espace réservé")
        verbose_name_plural = _("avis de l’espace réservé")
        ordering = ["order", "-created_at"]

    def __str__(self) -> str:
        return f"{self.heading_fr[:80]} [{self.get_audience_display()}]"
