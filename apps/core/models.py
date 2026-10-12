from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract base with creation/update timestamps used by every domain model."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class FeatureFlag(TimeStampedModel):
    """
    Feature / publication gate stored in the database (defaults in settings.FEATURE_FLAG_DEFAULTS).

    A flag is *active* only when ``enabled`` is true AND the current time lies inside the
    optional [enabled_from, enabled_until) window. This lets the back-office schedule
    transitions (Phase 3 on 2 Oct 2026, Forum permanent mode, banner expiry) without code.
    """

    key = models.SlugField(_("chiave"), max_length=64, unique=True)
    enabled = models.BooleanField(_("abilitato"), default=False)
    enabled_from = models.DateTimeField(_("attivo dal"), null=True, blank=True)
    enabled_until = models.DateTimeField(_("attivo fino al"), null=True, blank=True)
    note = models.CharField(_("nota"), max_length=255, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("aggiornato da"),
    )

    class Meta:
        verbose_name = _("feature flag / gate")
        verbose_name_plural = _("feature flag / gate")
        ordering = ["key"]

    def __str__(self) -> str:
        return f"{self.key} ({'on' if self.enabled else 'off'})"

    def clean(self) -> None:
        if self.enabled_from and self.enabled_until and self.enabled_from >= self.enabled_until:
            raise ValidationError(_("La finestra di attivazione non è valida (dal ≥ fino al)."))


def validate_public_email(value: str) -> None:
    """Public e-mail addresses must never use the not-yet-activated legalitalentry.it domain."""
    forbidden = settings.ILE["FORBIDDEN_EMAIL_DOMAIN"]
    if value and value.lower().rstrip().endswith("@" + forbidden):
        raise ValidationError(
            _("Gli indirizzi @%(domain)s non possono essere pubblicati finché non vengono attivati."),
            params={"domain": forbidden},
        )


class SiteSettings(TimeStampedModel):
    """Singleton with the editable identity and footer metadata of the site."""

    SINGLETON_ID = 1

    site_name = models.CharField(_("nome del sito"), max_length=120, default="Italy Legal Entry™")
    promoter_name = models.CharField(
        _("promotore"), max_length=200, default="AGAMI — Dialogo Giuridico Interculturale APS"
    )
    logo = models.ImageField(
        _("logo (opzionale)"),
        upload_to="identity/",
        blank=True,
        help_text=_(
            "Se assente viene usato il marchio tipografico. Il logo fornito contiene la tagline "
            "«Digital Pathways to Italy» e una porta, entrambe da rimuovere in Fase 3: caricarlo solo "
            "dopo conferma scritta (LOGO_PENDING_CLIENT_CONFIRMATION)."
        ),
    )
    use_logo_image = models.BooleanField(_("usa il logo grafico nell'header"), default=False)
    public_contact_email = models.EmailField(
        _("e-mail pubblica"),
        default="contact@agamieuromed.org",
        validators=[validate_public_email],
    )
    version_label = models.CharField(_("indicazione di versione (footer)"), max_length=60, default="v2.0.0 — Fase 1")
    content_verified_on = models.DateField(_("contenuti verificati il"), null=True, blank=True)
    hosting_provider = models.CharField(
        _("prestatore di hosting"),
        max_length=200,
        blank=True,
        help_text=_("Da confermare per iscritto (documento §1.4): prestatore e localizzazione UE."),
    )
    hosting_location = models.CharField(_("localizzazione server (UE)"), max_length=200, blank=True)
    reserved_area_enabled = models.BooleanField(_("area riservata attiva"), default=True)

    class Meta:
        verbose_name = _("impostazioni del sito")
        verbose_name_plural = _("impostazioni del sito")

    def __str__(self) -> str:
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_ID
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> SiteSettings:
        obj, _created = cls.objects.get_or_create(pk=cls.SINGLETON_ID)
        return obj
