"""
FAQ — « Questions fréquentes » (Implementation document §3.8.2, Phase 3, gate G3).

* ``FAQCategory`` groups items (anchors on the public page); optional translations.
* ``FAQItem`` is publishable (draft → review → scheduled → published → archived). The nine
  prescribed entries are seeded from the locked registry with ``is_locked=True``: their French
  question/answer are re-asserted from the registry on every save, so neither the admin nor the
  shell can drift from the prescribed wording (gate G0). Editors may add *new* unlocked entries.
* ``FAQItemTranslation`` — one row per language; only PUBLISHED rows are rendered (gate G10).
"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, TranslationBase, TranslationStatus
from core import clock
from core.models import TimeStampedModel
from faq import registry

GENERAL_CATEGORY_SLUG = "general"


class FAQCategory(TimeStampedModel):
    slug = models.SlugField(_("slug (ancora)"), max_length=60, unique=True)
    order = models.PositiveSmallIntegerField(_("ordine"), default=0, db_index=True)
    name_fr = models.CharField(_("nome (FR — sorgente)"), max_length=120)

    class Meta:
        ordering = ["order", "name_fr", "id"]
        verbose_name = _("categoria FAQ")
        verbose_name_plural = _("categorie FAQ")

    def __str__(self) -> str:
        return self.name_fr

    @property
    def anchor(self) -> str:
        return f"cat-{self.slug}"


class FAQCategoryTranslation(TranslationBase):
    master = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name="translations")
    name = models.CharField(_("nome tradotto"), max_length=120)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_faqcategory_translation"),
        ]
        verbose_name = _("traduzione categoria FAQ")
        verbose_name_plural = _("traduzioni categorie FAQ")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"

    def clean(self):
        super().clean()
        if self.language == settings.CONTENT_FALLBACK_LANGUAGE:
            raise ValidationError({"language": _("La versione francese è il testo sorgente, non una traduzione.")})


class FAQItem(PublishableModel):
    category = models.ForeignKey(
        FAQCategory, on_delete=models.PROTECT, related_name="items", verbose_name=_("categoria")
    )
    order = models.PositiveSmallIntegerField(_("ordine"), default=0, db_index=True)
    key = models.SlugField(
        _("chiave (ancora URL)"),
        max_length=64,
        unique=True,
        help_text=_(
            "Identificativo stabile usato come ancora (#chiave). "
            "Per le FAQ bloccate coincide con la chiave del registro."
        ),
    )
    is_locked = models.BooleanField(
        _("testo bloccato"),
        default=False,
        help_text=_(
            "Vero per le 9 FAQ prescritte: domanda e risposta provengono dal registro e non sono modificabili."
        ),
    )
    question_fr = models.CharField(_("domanda (FR — sorgente)"), max_length=300)
    answer_fr = models.TextField(_("risposta (FR — sorgente)"))
    last_updated = models.DateField(_("ultimo aggiornamento"), default=clock.today)

    class Meta:
        ordering = ["category__order", "category_id", "order", "id"]
        verbose_name = _("domanda frequente (FAQ)")
        verbose_name_plural = _("domande frequenti (FAQ)")
        indexes = [models.Index(fields=["status", "category"], name="faq_item_status_cat_idx")]

    def __str__(self) -> str:
        return self.question_fr

    @property
    def anchor(self) -> str:
        return self.key

    def registry_entry(self) -> dict[str, str] | None:
        return registry.item(self.key)

    def clean(self):
        super().clean()
        if self.is_locked and self.registry_entry() is None:
            raise ValidationError(
                {"is_locked": _("Solo le FAQ presenti nel registro dei testi bloccati possono essere bloccate.")}
            )

    def save(self, *args, **kwargs):
        if self.is_locked:
            entry = self.registry_entry()
            if entry is not None:
                # Gate G0: the prescribed wording always wins, whatever was submitted.
                self.question_fr = entry["question"]
                self.answer_fr = entry["answer"]
        super().save(*args, **kwargs)


class FAQItemTranslation(TranslationBase):
    master = models.ForeignKey(FAQItem, on_delete=models.CASCADE, related_name="translations")
    question = models.CharField(_("domanda tradotta"), max_length=300)
    answer = models.TextField(_("risposta tradotta"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_faqitem_translation"),
        ]
        verbose_name = _("traduzione FAQ")
        verbose_name_plural = _("traduzioni FAQ")

    def __str__(self) -> str:
        return f"{self.master_id} [{self.language}] {self.get_status_display()}"

    def clean(self):
        super().clean()
        if self.language == settings.CONTENT_FALLBACK_LANGUAGE:
            raise ValidationError({"language": _("La versione francese è il testo sorgente, non una traduzione.")})
        if (
            self.master_id
            and self.master.is_locked
            and self.status == TranslationStatus.PUBLISHED
            and not self.source.strip()
        ):
            raise ValidationError(
                {
                    "source": _(
                        "Per un testo bloccato indicare la fonte ufficiale della traduzione trasmessa "
                        "(mai una traduzione automatica)."
                    )
                }
            )
