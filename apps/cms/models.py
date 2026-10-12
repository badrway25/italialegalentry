"""
CMS foundation: publication workflow, translation status, menus, banners, hero, media library,
redirects. Domain apps build on ``PublishableModel`` and ``TranslationBase``.
"""

from __future__ import annotations

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import clock
from core.models import TimeStampedModel

logger = logging.getLogger("ile.cms")


class PublicationStatus(models.TextChoices):
    DRAFT = "draft", _("Bozza")
    REVIEW = "review", _("In revisione")
    SCHEDULED = "scheduled", _("Programmato")
    PUBLISHED = "published", _("Pubblicato")
    ARCHIVED = "archived", _("Archiviato")


class PublishableQuerySet(models.QuerySet):
    def live(self, at=None):
        """Rows visible to the public right now (status + scheduling window)."""
        at = at or clock.now()
        return self.filter(
            models.Q(status=PublicationStatus.PUBLISHED)
            | models.Q(status=PublicationStatus.SCHEDULED, publish_at__lte=at)
        ).filter(models.Q(unpublish_at__isnull=True) | models.Q(unpublish_at__gt=at))


class PublishableModel(TimeStampedModel):
    """
    Editorial workflow: DRAFT → REVIEW → (SCHEDULED) → PUBLISHED → ARCHIVED.
    Version increments on every save; timestamps let staff know what was online when.
    """

    status = models.CharField(
        _("stato"), max_length=12, choices=PublicationStatus.choices, default=PublicationStatus.DRAFT, db_index=True
    )
    publish_at = models.DateTimeField(_("pubblica dal"), null=True, blank=True)
    unpublish_at = models.DateTimeField(_("ritira dal"), null=True, blank=True)
    published_at = models.DateTimeField(_("pubblicato il"), null=True, blank=True, editable=False)
    last_reviewed_at = models.DateTimeField(_("ultima revisione"), null=True, blank=True)
    version = models.PositiveIntegerField(_("versione"), default=0, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("autore"),
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("revisore"),
    )
    editorial_note = models.CharField(_("nota editoriale"), max_length=255, blank=True)

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.status == PublicationStatus.SCHEDULED and not self.publish_at:
            raise ValidationError({"publish_at": _("Indicare la data di pubblicazione programmata.")})
        if self.publish_at and self.unpublish_at and self.publish_at >= self.unpublish_at:
            raise ValidationError({"unpublish_at": _("La data di ritiro deve seguire quella di pubblicazione.")})

    def save(self, *args, **kwargs):
        self.version = (self.version or 0) + 1
        if self.status == PublicationStatus.PUBLISHED and not self.published_at:
            self.published_at = clock.now()
        super().save(*args, **kwargs)

    def is_live(self, at=None) -> bool:
        at = at or clock.now()
        if self.unpublish_at and at >= self.unpublish_at:
            return False
        if self.status == PublicationStatus.PUBLISHED:
            return True
        return self.status == PublicationStatus.SCHEDULED and bool(self.publish_at) and self.publish_at <= at


class TranslationStatus(models.TextChoices):
    MISSING = "missing", _("Mancante")
    DRAFT = "draft", _("Bozza")
    REVIEWED = "reviewed", _("Revisionata")
    APPROVED = "approved", _("Approvata")
    PUBLISHED = "published", _("Pubblicata")


class TranslationBase(TimeStampedModel):
    """
    One row per (master object, language). Concrete subclasses add the translated fields and
    declare ``master = ForeignKey(..., related_name="translations")`` plus a unique constraint.
    Only PUBLISHED translations are rendered publicly (docs/I18N_RTL.md, gate G10).
    """

    language = models.CharField(_("lingua"), max_length=5, choices=settings.LANGUAGES, db_index=True)
    status = models.CharField(
        _("stato traduzione"), max_length=10, choices=TranslationStatus.choices, default=TranslationStatus.DRAFT
    )
    source = models.CharField(
        _("origine"),
        max_length=40,
        blank=True,
        help_text=_("es. «testo ufficiale trasmesso il 2026-09-14» — mai traduzione automatica per testi bloccati"),
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        abstract = True

    @property
    def is_public(self) -> bool:
        return self.status == TranslationStatus.PUBLISHED


class MenuLocation(models.TextChoices):
    MAIN = "main", _("Navigazione principale")
    UTILITY = "utility", _("Barra istituzionale")
    FOOTER_1 = "footer_1", _("Footer — colonna 1")
    FOOTER_2 = "footer_2", _("Footer — colonna 2")
    FOOTER_3 = "footer_3", _("Footer — colonna 3")
    FOOTER_LEGAL = "footer_legal", _("Footer — informazioni legali")


class MenuItem(TimeStampedModel):
    location = models.CharField(_("posizione"), max_length=20, choices=MenuLocation.choices, db_index=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    label_it = models.CharField("Etichetta (IT)", max_length=80)
    label_fr = models.CharField("Étiquette (FR)", max_length=80)
    label_en = models.CharField("Label (EN)", max_length=80)
    label_ar = models.CharField("التسمية (AR)", max_length=80, blank=True)
    url_name = models.CharField(
        _("nome URL Django"), max_length=120, blank=True, help_text=_("es. pages:home — prevale su URL manuale")
    )
    url = models.CharField(_("URL manuale"), max_length=300, blank=True)
    requires_flag = models.CharField(_("visibile solo se flag attivo"), max_length=64, blank=True)
    requires_gate = models.CharField(
        _("visibile solo se gate aperto"), max_length=40, blank=True, help_text=_("es. phase3_public, virtual_forum")
    )
    is_visible = models.BooleanField(_("visibile"), default=True)
    open_in_new_tab = models.BooleanField(default=False)
    description_fr = models.CharField(_("descrizione breve (mega-menu, FR)"), max_length=160, blank=True)

    class Meta:
        ordering = ["location", "parent__id", "order", "id"]
        verbose_name = _("voce di menu")
        verbose_name_plural = _("voci di menu")

    def __str__(self) -> str:
        return f"[{self.location}] {self.label_fr}"

    def label(self, lang: str) -> str:
        return getattr(self, f"label_{lang.split('-')[0]}", "") or self.label_fr


class SiteBanner(PublishableModel):
    """
    Institutional notice on the homepage (e.g. Forum Vénétie–Maroc banner until 2 Oct 2026).
    When ``locked_key`` is set, texts come from the locked registry and are not editable.
    """

    key = models.SlugField(max_length=40, unique=True)
    locked_key = models.CharField(max_length=64, blank=True, help_text=_("prefisso nel registro dei testi bloccati"))
    title_fr = models.CharField(max_length=160, blank=True)
    meta_fr = models.CharField(max_length=160, blank=True)
    quote_fr = models.TextField(blank=True)
    button_label_fr = models.CharField(max_length=80, blank=True)
    url_name = models.CharField(max_length=120, blank=True)
    url = models.CharField(max_length=300, blank=True)
    requires_flag = models.CharField(max_length=64, blank=True, default="forum_banner")

    class Meta:
        verbose_name = _("banner istituzionale")
        verbose_name_plural = _("banner istituzionali")

    def __str__(self) -> str:
        return self.key


class HeroVariant(models.TextChoices):
    INTERIM = "interim", _("Interim (pre Fase 3)")
    PHASE3 = "phase3", _("Fase 3 (testo prescritto)")


class HomeHero(PublishableModel):
    """
    Homepage hero. The Phase 3 variant renders the locked ``p3.hero.*`` texts and is shown only
    when gate G3 is open; the interim variant is CMS-editable and uses approved excerpts.
    """

    variant = models.CharField(max_length=10, choices=HeroVariant.choices, unique=True)
    eyebrow_fr = models.CharField(max_length=120, blank=True)
    title_fr = models.CharField(max_length=160, blank=True)
    subtitle_fr = models.CharField(max_length=240, blank=True)
    body_fr = models.TextField(blank=True)
    primary_cta_label_fr = models.CharField(max_length=80, blank=True)
    primary_cta_url_name = models.CharField(max_length=120, blank=True)
    secondary_cta_label_fr = models.CharField(max_length=80, blank=True)
    secondary_cta_url_name = models.CharField(max_length=120, blank=True)
    image = models.ForeignKey("cms.MediaAsset", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("hero homepage")
        verbose_name_plural = _("hero homepage")

    def __str__(self) -> str:
        return f"Hero {self.get_variant_display()}"


class MediaLicense(models.TextChoices):
    UNSPLASH = "unsplash", "Unsplash License"
    PEXELS = "pexels", "Pexels License"
    CC0 = "cc0", "CC0 / Public domain"
    CC_BY = "cc_by", "CC BY 4.0"
    CLIENT = "client", _("Fornito dal committente")
    ORIGINAL = "original", _("Originale (SVG / illustrazione)")
    OTHER = "other", _("Altra licenza (vedi note)")


class MediaAsset(TimeStampedModel):
    """Self-hosted image with provenance and licence metadata (docs/IMAGE_LICENSES.md)."""

    title = models.CharField(max_length=160)
    file = models.ImageField(upload_to="media/%Y/%m/")
    alt_it = models.CharField("Testo alternativo (IT)", max_length=200, blank=True)
    alt_fr = models.CharField("Texte alternatif (FR)", max_length=200)
    alt_en = models.CharField("Alt text (EN)", max_length=200, blank=True)
    alt_ar = models.CharField("النص البديل (AR)", max_length=200, blank=True)
    author = models.CharField(_("autore"), max_length=160, blank=True)
    source_url = models.URLField(_("URL sorgente"), blank=True)
    license = models.CharField(_("licenza"), max_length=12, choices=MediaLicense.choices, default=MediaLicense.OTHER)
    license_notes = models.CharField(max_length=255, blank=True)
    downloaded_on = models.DateField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    is_decorative = models.BooleanField(default=False)
    #: The caption apparatus. A photograph on this site is an ARCHIVE PLATE, not an illustration:
    #: it says where it was taken, when, what it shows and who made it. Art direction A §6.2 makes
    #: a <figure> without a <figcaption> a defect, and `services.photo_from_asset` returns None for
    #: an asset that cannot fill these — which is what makes anonymous stock photography
    #: structurally impossible rather than merely discouraged.
    #:
    #: The library inherited from the previous build fills none of them: six interchangeable frames
    #: served fifty-two pages. Those assets therefore render nowhere until they are curated.
    caption_place = models.CharField(_("luogo"), max_length=120, blank=True)
    caption_date = models.DateField(_("data della ripresa"), null=True, blank=True)
    caption_fr = models.CharField(
        _("didascalia (FR)"),
        max_length=300,
        blank=True,
        help_text=_("Una frase di fatto su ciò che si vede. Non un commento, non uno slogan."),
    )
    caption_it = models.CharField(_("didascalia (IT)"), max_length=300, blank=True)
    caption_en = models.CharField(_("didascalia (EN)"), max_length=300, blank=True)
    caption_ar = models.CharField(_("didascalia (AR)"), max_length=300, blank=True)
    credit = models.CharField(
        _("credito"),
        max_length=160,
        blank=True,
        help_text=_("Chi ha realizzato l'immagine, nella forma richiesta dalla licenza."),
    )
    stereotype_checked = models.BooleanField(
        _("verificato: nessuna immagine stereotipata"),
        default=False,
        help_text=_("Nessuna frontiera, valigia, fila, passaporto, aeroporto, porta o griglia (Fase 3 §3.1)."),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("immagine")
        verbose_name_plural = _("libreria immagini")

    def __str__(self) -> str:
        return self.title

    def caption(self, lang: str = "fr") -> str:
        return getattr(self, f"caption_{lang}", "") or self.caption_fr

    @property
    def is_publishable(self) -> bool:
        """
        True when the asset can ship: it carries its whole caption apparatus.

        A decorative image is exempt — it carries no meaning to caption, and it is marked as such
        for assistive technology too.
        """
        if self.is_decorative:
            return True
        return bool(self.caption_fr and self.credit and self.caption_place and self.caption_date)

    def alt(self, lang: str) -> str:
        return getattr(self, f"alt_{lang.split('-')[0]}", "") or self.alt_fr

    def save(self, *args, **kwargs):
        if self.file and not (self.width and self.height):
            try:
                self.width, self.height = self.file.width, self.file.height
            except (OSError, ValueError) as exc:  # unreadable or not-yet-stored image
                logger.info("Could not read dimensions of media asset %r: %s", self.title, exc)
        super().save(*args, **kwargs)


class Redirect(TimeStampedModel):
    """Old → new URL mapping used at migration time (docs/URL_MIGRATION_MAP.md)."""

    old_path = models.CharField(max_length=300, unique=True)
    new_path = models.CharField(max_length=300)
    permanent = models.BooleanField(default=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirect")

    def __str__(self) -> str:
        return f"{self.old_path} → {self.new_path}"
