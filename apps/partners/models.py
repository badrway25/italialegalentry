"""
Partners / institutions shown publicly ONLY when authorised in writing (gate G6).

A partner's name and logo reach a public page only when *both* conditions hold:
``authorized=True`` (with a written authorisation reference) AND the editorial status is live
(``PublishableModel.objects.live()``). Nothing is ever rendered from an unauthorised row, and no
placeholder logo exists anywhere in the public templates.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, PublishableQuerySet, TranslationBase
from core import clock

MIN_AUTHORIZATION_REFERENCE_LENGTH = 10


class HttpsURLField(models.URLField):
    """URLField whose admin form assumes https (silences the Django 6.0 scheme deprecation)."""

    def formfield(self, **kwargs):
        kwargs.setdefault("assume_scheme", "https")
        return super().formfield(**kwargs)


class PartnerKind(models.TextChoices):
    INSTITUTION = "institution", _("Institutions")
    COMPANY = "company", _("Entreprises")
    UNIVERSITY = "university", _("Universités")
    TRAINING_BODY = "training_body", _("Organismes de formation")
    ASSOCIATION = "association", _("Associations")
    CHAMBER_OF_COMMERCE = "chamber_of_commerce", _("Chambres de Commerce")
    PROFESSIONAL = "professional", _("Professionnels")
    DIPLOMATIC = "diplomatic", _("Représentations diplomatiques et consulaires")
    OTHER = "other", _("Autres partenaires")


class PartnerQuerySet(PublishableQuerySet):
    def authorized(self, at=None):
        """Rows that may be shown to the public: live AND authorised with a written reference."""
        return self.live(at).filter(authorized=True).exclude(authorization_reference="")


class Partner(PublishableModel):
    name = models.CharField(_("denominazione"), max_length=200)
    kind = models.CharField(_("tipo"), max_length=24, choices=PartnerKind.choices, db_index=True)
    country = models.CharField(_("paese"), max_length=80, blank=True)
    city = models.CharField(_("città"), max_length=120, blank=True)
    website = HttpsURLField(_("sito web"), blank=True)
    logo = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("logo"),
        help_text=_("Caricare SOLO loghi trasmessi dal partner con autorizzazione scritta (gate G6)."),
    )
    authorized = models.BooleanField(
        _("pubblicazione autorizzata"),
        default=False,
        help_text=_(
            "Nome e logo vengono mostrati al pubblico SOLO se questa casella è attiva E lo stato editoriale è "
            "«Pubblicato». Attivare unicamente dopo ricezione dell'autorizzazione scritta del partner."
        ),
    )
    authorization_reference = models.CharField(
        _("riferimento dell'autorizzazione"),
        max_length=200,
        blank=True,
        help_text=_(
            "Chi ha autorizzato e quando (es. «e-mail del referente X del 2026-10-05»). Obbligatorio se autorizzato."
        ),
    )
    authorized_at = models.DateTimeField(_("autorizzato il"), null=True, blank=True)
    description_fr = models.CharField(_("descrizione breve (FR)"), max_length=300, blank=True)
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)

    objects = PartnerQuerySet.as_manager()

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("partner")
        verbose_name_plural = _("partner")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(authorized=False) | ~models.Q(authorization_reference=""),
                name="partner_authorized_requires_reference",
            ),
        ]
        indexes = [models.Index(fields=["authorized", "status"])]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        if self.authorized and len(self.authorization_reference.strip()) < MIN_AUTHORIZATION_REFERENCE_LENGTH:
            raise ValidationError(
                {
                    "authorization_reference": _(
                        "Indicare il riferimento dell'autorizzazione scritta (almeno %(n)d caratteri)."
                    )
                    % {"n": MIN_AUTHORIZATION_REFERENCE_LENGTH}
                }
            )

    def save(self, *args, **kwargs):
        if self.authorized and not self.authorized_at:
            self.authorized_at = clock.now()
        if not self.authorized:
            self.authorized_at = None
        super().save(*args, **kwargs)

    @property
    def is_public(self) -> bool:
        return bool(self.authorized and self.authorization_reference.strip() and self.is_live())

    @property
    def logo_public(self) -> bool:
        return self.is_public and self.logo_id is not None


class PartnerTranslation(TranslationBase):
    master = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="translations")
    description = models.CharField(_("descrizione breve"), max_length=300, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["master", "language"], name="uniq_partner_translation")]
        verbose_name = _("traduzione partner")
        verbose_name_plural = _("traduzioni partner")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"
