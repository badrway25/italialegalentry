from __future__ import annotations

import secrets

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class ConsentPurpose(models.TextChoices):
    COMPANY_NEEDS = "company_needs", _("Recueil des besoins — imprese")
    FORUM_REGISTRATION = "forum_registration", _("Iscrizione al Forum")
    INSTITUTION_PROPOSAL = "institution_proposal", _("Proposta di collaborazione istituzionale")
    UNIVERSITY_PROPOSAL = "university_proposal", _("Proposta di partenariato università/formazione")
    CONTACT = "contact", _("Richiesta di contatto")
    NEWSLETTER = "newsletter", _("Newsletter (consenso separato e revocabile)")
    ACCOUNT_TERMS = "account_terms", _("Registrazione account — Condizioni d’utilizzo e Privacy")
    ORIENTATION = "orientation", _("Questionario di orientamento")
    COMMUNITY = "community", _("Forum Virtuale — partecipazione")


class ConsentText(TimeStampedModel):
    """
    Versioned wording shown next to a consent checkbox. New wording = new version row; existing
    records keep pointing to the version the person actually saw.
    """

    purpose = models.CharField(max_length=32, choices=ConsentPurpose.choices, db_index=True)
    version = models.PositiveSmallIntegerField(default=1)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default="fr")
    text = models.TextField(_("testo del consenso"))
    locked_key = models.CharField(
        max_length=64, blank=True, help_text=_("chiave nel registro testi bloccati, se prescritto")
    )
    effective_from = models.DateTimeField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    source = models.CharField(max_length=120, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["purpose", "language", "version"], name="uniq_consent_text_version"),
        ]
        ordering = ["purpose", "language", "-version"]
        verbose_name = _("testo di consenso")
        verbose_name_plural = _("testi di consenso")

    def __str__(self) -> str:
        return f"{self.get_purpose_display()} v{self.version} ({self.language})"


class ConsentRecord(TimeStampedModel):
    """Proof of consent: what text (version), when, for which purpose, from which (hashed) IP."""

    purpose = models.CharField(max_length=32, choices=ConsentPurpose.choices, db_index=True)
    consent_text = models.ForeignKey(ConsentText, on_delete=models.PROTECT, related_name="records")
    email = models.EmailField(db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="consents"
    )
    given_at = models.DateTimeField(db_index=True)
    ip_hash = models.CharField(max_length=32, blank=True)
    user_agent = models.CharField(max_length=160, blank=True)
    language = models.CharField(max_length=5, default="fr")
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    withdrawal_note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-given_at"]
        verbose_name = _("registrazione di consenso")
        verbose_name_plural = _("registrazioni di consenso")

    def __str__(self) -> str:
        return f"{self.purpose} — {self.email} — {self.given_at:%Y-%m-%d %H:%M}"

    @property
    def is_active(self) -> bool:
        return self.withdrawn_at is None


def _token() -> str:
    return secrets.token_urlsafe(32)


class NewsletterSubscription(TimeStampedModel):
    """Separate, explicit, non-pre-ticked, revocable newsletter consent with double opt-in."""

    email = models.EmailField(unique=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default="fr")
    consent = models.ForeignKey(ConsentRecord, on_delete=models.PROTECT, related_name="+")
    confirm_token = models.CharField(max_length=64, default=_token, unique=True, editable=False)
    unsubscribe_token = models.CharField(max_length=64, default=_token, unique=True, editable=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("iscrizione newsletter")
        verbose_name_plural = _("iscrizioni newsletter")

    def __str__(self) -> str:
        return self.email

    @property
    def is_active(self) -> bool:
        return self.confirmed_at is not None and self.unsubscribed_at is None
