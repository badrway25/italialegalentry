"""
Espace Personnes — the eight regular pathways (Implementation document §3.3).

Titles and short descriptions of the pathways are LOCKED texts (``p3.persons.pathways``) and are
never stored in the database: ``Pathway`` stores only the key, the order and editorial metadata,
and reads title/description from the registry at render time.

Editorial detail (eligibility context, steps, documentation, warnings) is CONTENT_PENDING_LEGAL_REVIEW:
the seed creates a neutral structural skeleton only; no eligibility criterion, deadline or legal
condition is invented by the technical team. Items flagged ``pending_legal_review`` are rendered
publicly as headings only (never their body text) until a reviewer clears the flag.
"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.models import PublishableModel, PublishableQuerySet, TranslationBase
from core.models import TimeStampedModel

LOCKED_PATHWAYS_KEY = "p3.persons.pathways"


def locked_pathway_entries() -> list[dict]:
    """The eight prescribed pathways, in the prescribed order (registry, never DB)."""
    entries, _lang = locked_content.get(LOCKED_PATHWAYS_KEY, "fr")
    return list(entries)


def locked_pathway_keys() -> tuple[str, ...]:
    return tuple(entry["key"] for entry in locked_pathway_entries())


PATHWAY_KEYS: tuple[str, ...] = locked_pathway_keys()
PATHWAY_KEY_CHOICES: tuple[tuple[str, str], ...] = tuple(
    (entry["key"], entry["title"]) for entry in locked_pathway_entries()
)

# Authority names that may be seeded: only generic designations literally present in the locked
# texts (glossary / FAQ). No URL is invented — editors add official links after verification.
GENERIC_AUTHORITY_NAMES: tuple[str, ...] = (
    "représentations diplomatiques et consulaires italiennes",
    "Questura",
    "Sportello Unico per l’Immigrazione",
    "Prefettura",
)


def validate_pathway_key(value: str) -> None:
    if value not in PATHWAY_KEYS:
        raise ValidationError(
            _("La clé « %(key)s » ne fait pas partie des huit parcours prescrits."), params={"key": value}
        )


def validate_authorities(value) -> None:
    if value in (None, ""):
        return
    if not isinstance(value, list):
        raise ValidationError(_("Les autorités doivent être une liste d’objets {name, url}."))
    for item in value:
        if not isinstance(item, dict) or not str(item.get("name", "")).strip():
            raise ValidationError(_("Chaque autorité doit avoir au moins un nom."))
        url = item.get("url", "") or ""
        if url and not str(url).startswith("https://"):
            raise ValidationError(_("Les liens vers les autorités doivent commencer par https://."))


class PathwayQuerySet(PublishableQuerySet):
    def ordered(self):
        return self.order_by("order", "key")


class Pathway(PublishableModel):
    """
    One of the eight prescribed regular pathways. ``key`` is the locked identifier; title and
    description are resolved from the locked registry (see ``title`` / ``description``).
    """

    key = models.CharField(
        _("clé du parcours (verrouillée)"),
        max_length=48,
        unique=True,
        choices=PATHWAY_KEY_CHOICES,
        validators=[validate_pathway_key],
    )
    order = models.PositiveSmallIntegerField(_("ordre"), default=0, db_index=True)
    locked = models.BooleanField(
        _("titre et description verrouillés"),
        default=True,
        editable=False,
        help_text=_("Le titre et la description proviennent du registre des textes prescrits (p3.persons.pathways)."),
    )
    icon = models.CharField(
        _("icône"),
        max_length=40,
        blank=True,
        help_text=_("Nom d’icône du sprite (static/img/icons.svg), ex. « briefcase »."),
    )
    hero_image = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("image d’en-tête"),
    )
    eligibility_context_fr = models.TextField(
        _("contexte d’éligibilité (FR)"),
        blank=True,
        help_text=_(
            "CONTENT_PENDING_LEGAL_REVIEW — texte éditorial à vérifier sur des sources primaires "
            "(Normattiva, ministères, portail UE) avant publication. Aucun critère légal ne doit être inventé."
        ),
    )
    authorities = models.JSONField(
        _("autorités et acteurs compétents"),
        default=list,
        blank=True,
        validators=[validate_authorities],
        help_text=_(
            "Liste de {name, url}. CONTENT_PENDING_LEGAL_REVIEW — seuls des noms génériques présents dans les "
            "textes prescrits sont pré-remplis ; ajouter les liens officiels après vérification."
        ),
    )
    source_notes = models.TextField(
        _("notes sur les sources"),
        blank=True,
        help_text=_("Références vérifiées (Normattiva, GU, ministères, EUR-Lex, EU Immigration Portal) et date."),
    )

    objects = PathwayQuerySet.as_manager()

    class Meta:
        ordering = ["order", "key"]
        verbose_name = _("parcours régulier")
        verbose_name_plural = _("parcours réguliers")
        constraints = [
            models.UniqueConstraint(fields=["order"], name="pathways_pathway_order_unique"),
        ]

    def __str__(self) -> str:
        return self.title

    # ---- locked registry accessors -------------------------------------------------------------
    @property
    def locked_entry(self) -> dict:
        for entry in locked_pathway_entries():
            if entry["key"] == self.key:
                return entry
        return {"key": self.key, "title": self.key, "description": ""}

    @property
    def title(self) -> str:
        return self.locked_entry["title"]

    @property
    def description(self) -> str:
        return self.locked_entry["description"]

    @property
    def reviewed_by(self):
        """Alias of the inherited ``reviewer`` field (PublishableModel)."""
        return self.reviewer

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse("pathways:detail", kwargs={"key": self.key})

    def clean(self):
        super().clean()
        validate_pathway_key(self.key)


class PathwayTranslation(TranslationBase):
    master = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="translations")
    eligibility_context = models.TextField(_("contexte d’éligibilité"), blank=True)

    class Meta:
        verbose_name = _("traduction du parcours")
        verbose_name_plural = _("traductions du parcours")
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="pathways_pathwaytranslation_unique"),
        ]

    def __str__(self) -> str:
        return f"{self.master_id}:{self.language}"


class PathwayItemBase(TimeStampedModel):
    """Common shape of steps / documents / warnings: ordered, reviewable, attached to a pathway."""

    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    pending_legal_review = models.BooleanField(
        _("CONTENT_PENDING_LEGAL_REVIEW"),
        default=True,
        help_text=_("Tant que la case est cochée, seul l’intitulé est publié (jamais le texte détaillé)."),
    )

    class Meta:
        abstract = True
        ordering = ["order", "id"]

    @property
    def is_reviewed(self) -> bool:
        return not self.pending_legal_review


class PathwayStep(PathwayItemBase):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="steps")
    title_fr = models.CharField(_("intitulé (FR)"), max_length=160)
    text_fr = models.TextField(_("texte (FR)"), blank=True)

    class Meta(PathwayItemBase.Meta):
        verbose_name = _("étape")
        verbose_name_plural = _("étapes")
        constraints = [models.UniqueConstraint(fields=["pathway", "order"], name="pathways_step_order_unique")]

    def __str__(self) -> str:
        return f"{self.order}. {self.title_fr}"


class PathwayStepTranslation(TranslationBase):
    master = models.ForeignKey(PathwayStep, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField(_("intitulé"), max_length=160)
    text = models.TextField(_("texte"), blank=True)

    class Meta:
        verbose_name = _("traduction de l’étape")
        verbose_name_plural = _("traductions de l’étape")
        constraints = [models.UniqueConstraint(fields=["master", "language"], name="pathways_steptranslation_unique")]

    def __str__(self) -> str:
        return f"{self.master_id}:{self.language}"


class PathwayDocument(PathwayItemBase):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="documents")
    label_fr = models.CharField(_("document (FR)"), max_length=200)
    note_fr = models.TextField(_("précision (FR)"), blank=True)

    class Meta(PathwayItemBase.Meta):
        verbose_name = _("document généralement requis")
        verbose_name_plural = _("documents généralement requis")
        constraints = [models.UniqueConstraint(fields=["pathway", "order"], name="pathways_document_order_unique")]

    def __str__(self) -> str:
        return self.label_fr


class PathwayDocumentTranslation(TranslationBase):
    master = models.ForeignKey(PathwayDocument, on_delete=models.CASCADE, related_name="translations")
    label = models.CharField(_("document"), max_length=200)
    note = models.TextField(_("précision"), blank=True)

    class Meta:
        verbose_name = _("traduction du document")
        verbose_name_plural = _("traductions du document")
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="pathways_documenttranslation_unique")
        ]

    def __str__(self) -> str:
        return f"{self.master_id}:{self.language}"


class PathwayWarning(PathwayItemBase):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="warnings")
    text_fr = models.TextField(_("avertissement (FR)"))

    class Meta(PathwayItemBase.Meta):
        verbose_name = _("avertissement")
        verbose_name_plural = _("avertissements")
        constraints = [models.UniqueConstraint(fields=["pathway", "order"], name="pathways_warning_order_unique")]

    def __str__(self) -> str:
        return self.text_fr[:60]


class PathwayWarningTranslation(TranslationBase):
    master = models.ForeignKey(PathwayWarning, on_delete=models.CASCADE, related_name="translations")
    text = models.TextField(_("avertissement"))

    class Meta:
        verbose_name = _("traduction de l’avertissement")
        verbose_name_plural = _("traductions de l’avertissement")
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="pathways_warningtranslation_unique")
        ]

    def __str__(self) -> str:
        return f"{self.master_id}:{self.language}"


class PathwaySource(TimeStampedModel):
    """Primary source consulted for a pathway (requirement R-CNT-005): never published, traceability only."""

    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="sources")
    title = models.CharField(_("titre"), max_length=200)
    url = models.URLField(_("URL"), blank=True)
    publisher = models.CharField(_("éditeur / autorité"), max_length=160, blank=True)
    retrieved_at = models.DateField(_("consulté le"), null=True, blank=True)
    note = models.CharField(_("note"), max_length=255, blank=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["pathway", "id"]
        verbose_name = _("source primaire")
        verbose_name_plural = _("sources primaires")

    def __str__(self) -> str:
        return self.title
