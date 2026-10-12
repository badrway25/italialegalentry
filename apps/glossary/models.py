"""
Glossary — « Glossaire : termes italiens expliqués » (Implementation document §3.8.3, Phase 3, G3).

* ``Term`` is publishable; the ten prescribed terms are seeded with ``is_locked=True`` and their
  Italian label + French definition are re-asserted from the locked registry on every save (G0).
  Editors may add new unlocked terms, relate terms to each other, record a source and a review date.
* ``TermTranslation`` — one row per language; only PUBLISHED rows are rendered publicly (G10).
"""

from __future__ import annotations

import unicodedata

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, TranslationBase, TranslationStatus
from glossary import registry

NON_ALPHA_GROUP = "0-9"


def initial_letter(text: str) -> str:
    """
    Upper-case, accent-stripped first letter used by the A–Z index ('É' → 'E').
    Terms without any letter (e.g. « 730 ») fall into the ``0-9`` group — the value is also used as
    an HTML id / URL fragment, so it must stay a plain ASCII token.
    """
    for char in text.strip():
        if char.isalpha():
            base = unicodedata.normalize("NFKD", char)
            base = "".join(c for c in base if not unicodedata.combining(c)) or char
            return base[0].upper()
    return NON_ALPHA_GROUP


class Term(PublishableModel):
    key = models.SlugField(
        _("chiave (slug permalink)"),
        max_length=64,
        unique=True,
        help_text=_(
            "Slug stabile del permalink (/glossaire/<chiave>/). "
            "Per i termini bloccati coincide con la chiave del registro."
        ),
    )
    term = models.CharField(_("termine (italiano)"), max_length=120)
    definition_fr = models.TextField(_("definizione (FR — sorgente)"))
    is_locked = models.BooleanField(
        _("testo bloccato"),
        default=False,
        help_text=_(
            "Vero per i 10 termini prescritti: termine e definizione provengono dal registro e non sono modificabili."
        ),
    )
    source = models.CharField(
        _("fonte"),
        max_length=200,
        blank=True,
        help_text=_(
            "Riferimento della fonte (documento, norma, sito ufficiale). Nessun contenuto giuridico inventato."
        ),
    )
    related = models.ManyToManyField("self", symmetrical=True, blank=True, verbose_name=_("termini correlati"))

    class Meta:
        ordering = ["term", "id"]
        verbose_name = _("termine di glossario")
        verbose_name_plural = _("glossario")
        indexes = [models.Index(fields=["status"], name="glossary_term_status_idx")]

    def __str__(self) -> str:
        return self.term

    @property
    def initial(self) -> str:
        return initial_letter(self.term)

    def get_absolute_url(self) -> str:
        return reverse("glossary:term", kwargs={"slug": self.key})

    def registry_entry(self) -> dict[str, str] | None:
        return registry.term(self.key)

    def clean(self):
        super().clean()
        if self.is_locked and self.registry_entry() is None:
            raise ValidationError(
                {"is_locked": _("Solo i termini presenti nel registro dei testi bloccati possono essere bloccati.")}
            )

    def save(self, *args, **kwargs):
        if self.is_locked:
            entry = self.registry_entry()
            if entry is not None:
                # Gate G0: the prescribed wording always wins, whatever was submitted.
                self.term = entry["term"]
                self.definition_fr = entry["definition"]
        super().save(*args, **kwargs)
        from glossary.services import invalidate_link_map

        invalidate_link_map()

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        from glossary.services import invalidate_link_map

        invalidate_link_map()
        return result


class TermTranslation(TranslationBase):
    master = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="translations")
    term = models.CharField(
        _("termine (etichetta localizzata, opzionale)"),
        max_length=120,
        blank=True,
        help_text=_("Vuoto = resta il termine italiano."),
    )
    definition = models.TextField(_("definizione tradotta"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_term_translation"),
        ]
        verbose_name = _("traduzione termine")
        verbose_name_plural = _("traduzioni termini")

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
