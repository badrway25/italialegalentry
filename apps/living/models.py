"""
« Vivre en Italie » — thematic topics and practical sheets ("fiches") managed from the back-office.

Topics are published categories (10 seeded). Sheets carry practical/legal-adjacent information
and are CONTENT_PENDING_LEGAL_REVIEW until a reviewer marks them ``legal_review=REVIEWED``:
a database CheckConstraint makes it impossible to publish a sheet that has not been reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms.models import PublicationStatus, PublishableModel, PublishableQuerySet, TranslationBase
from cms.translation import resolve
from living.catalogue import TOPIC_BY_SLUG, TOPIC_LABELS
from news.editorial import plain_text, validate_link_list

SUMMARY_MAX_LENGTH = 300


@dataclass(frozen=True)
class LocalizedText:
    title: str
    summary: str
    body: str
    language: str
    is_fallback: bool


class LivingTopicQuerySet(PublishableQuerySet):
    def public(self, at=None):
        return self.live(at).order_by("order", "name_fr")


class LivingTopic(PublishableModel):
    slug = models.SlugField(_("slug"), max_length=60, unique=True)
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    name_fr = models.CharField("Nom (FR)", max_length=120)
    icon = models.CharField(
        _("icône"),
        max_length=40,
        blank=True,
        help_text=_("Nom de l’icône dans le sprite (static/img/icons.svg), ex. « home »."),
    )
    intro_fr = models.TextField(
        "Introduction (FR)",
        blank=True,
        help_text=_("Texte de présentation du thème. CONTENT_PENDING_LEGAL_REVIEW : à valider avant publication."),
    )

    objects = LivingTopicQuerySet.as_manager()

    class Meta:
        ordering = ["order", "name_fr"]
        verbose_name = _("thème « Vivre en Italie »")
        verbose_name_plural = _("thèmes « Vivre en Italie »")

    def __str__(self) -> str:
        return self.name_fr

    def get_absolute_url(self) -> str:
        return reverse("living:topic", kwargs={"slug": self.slug})

    def texts(self, lang: str | None = None) -> LocalizedText:
        lang = (lang or translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
        row, effective, _fb = resolve(self, lang)
        if row is not None and effective == lang and lang != settings.CONTENT_FALLBACK_LANGUAGE:
            return LocalizedText(row.name, "", row.intro or self.intro_fr, lang, False)
        # Seeded topics keep their catalogue label: a gettext source string → translated UI label.
        spec = TOPIC_BY_SLUG.get(self.slug)
        if spec is not None and spec.name_fr == self.name_fr:
            name, is_fallback = str(TOPIC_LABELS[self.slug]), False
        else:  # editorial rename or new topic: the stored French name (fallback marked for non-FR)
            name, is_fallback = self.name_fr, lang != settings.CONTENT_FALLBACK_LANGUAGE
        language = settings.CONTENT_FALLBACK_LANGUAGE if is_fallback else lang
        return LocalizedText(name, "", self.intro_fr, language, is_fallback)


class LivingTopicTranslation(TranslationBase):
    master = models.ForeignKey(LivingTopic, on_delete=models.CASCADE, related_name="translations")
    name = models.CharField(_("nom"), max_length=120)
    intro = models.TextField(_("introduction"), blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["master", "language"], name="uniq_livingtopic_translation")]
        verbose_name = _("traduction de thème")
        verbose_name_plural = _("traductions de thèmes")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"


class LegalReviewStatus(models.TextChoices):
    PENDING = "pending", "CONTENT_PENDING_LEGAL_REVIEW"
    REVIEWED = "reviewed", _("Revu et validé")


class LivingSheetQuerySet(PublishableQuerySet):
    def public(self, at=None):
        return (
            self.live(at)
            .filter(legal_review=LegalReviewStatus.REVIEWED)
            .select_related("topic")
            .order_by("order", "title_fr")
        )


class LivingSheet(PublishableModel):
    """A practical sheet ("fiche") attached to a topic."""

    topic = models.ForeignKey(LivingTopic, on_delete=models.CASCADE, related_name="sheets", verbose_name=_("thème"))
    slug = models.SlugField(_("slug"), max_length=120)
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    title_fr = models.CharField("Titre (FR)", max_length=200)
    summary_fr = models.CharField("Résumé (FR)", max_length=SUMMARY_MAX_LENGTH, blank=True)
    body_fr = models.TextField(
        "Contenu (FR)",
        blank=True,
        help_text=_(
            "Texte brut : paragraphes séparés par une ligne vide ; « ## » pour un intertitre ; « - » pour une liste. "
            "Aucun contenu juridique ne doit être rédigé sans source officielle vérifiée."
        ),
    )
    sources = models.JSONField(
        _("sources"),
        default=list,
        blank=True,
        validators=[validate_link_list],
        help_text=_('Liste JSON de {"label": "…", "url": "https://…"} vers les sources officielles consultées.'),
    )
    legal_review = models.CharField(
        _("revue juridique"),
        max_length=10,
        choices=LegalReviewStatus.choices,
        default=LegalReviewStatus.PENDING,
        db_index=True,
        help_text=_("La publication est impossible tant que la fiche n’est pas « revue et validée »."),
    )

    objects = LivingSheetQuerySet.as_manager()

    class Meta:
        ordering = ["topic__order", "order", "title_fr"]
        verbose_name = _("fiche « Vivre en Italie »")
        verbose_name_plural = _("fiches « Vivre en Italie »")
        permissions = [("publish_livingsheet", "Can publish « Vivre en Italie » sheets")]
        constraints = [
            models.UniqueConstraint(fields=["topic", "slug"], name="uniq_livingsheet_topic_slug"),
            models.CheckConstraint(
                condition=~Q(status__in=[PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED])
                | Q(legal_review=LegalReviewStatus.REVIEWED),
                name="livingsheet_publish_requires_legal_review",
            ),
        ]

    def __str__(self) -> str:
        return self.title_fr

    def get_absolute_url(self) -> str:
        return reverse("living:sheet", kwargs={"topic": self.topic.slug, "slug": self.slug})

    @property
    def is_reviewed(self) -> bool:
        return self.legal_review == LegalReviewStatus.REVIEWED

    def clean(self):
        super().clean()
        if self.status in (PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED) and not self.is_reviewed:
            raise ValidationError(
                {
                    "status": _(
                        "Impossible de publier : la fiche est en attente de revue juridique "
                        "(CONTENT_PENDING_LEGAL_REVIEW)."
                    )
                }
            )
        if self.is_reviewed and not self.last_reviewed_at:
            raise ValidationError({"last_reviewed_at": _("Indiquer la date de la revue.")})
        if self.is_reviewed and not self.reviewer_id:
            raise ValidationError({"reviewer": _("Indiquer le réviseur.")})

    def texts(self, lang: str | None = None) -> LocalizedText:
        lang = (lang or translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
        row, effective, _fb = resolve(self, lang)
        if row is not None and effective == lang and lang != settings.CONTENT_FALLBACK_LANGUAGE:
            return LocalizedText(row.title, row.summary or self.summary_fr, row.body or self.body_fr, lang, False)
        fallback = settings.CONTENT_FALLBACK_LANGUAGE
        return LocalizedText(
            self.title_fr,
            self.summary_fr or plain_text(self.body_fr, 160),
            self.body_fr,
            fallback,
            lang != fallback,
        )


class LivingSheetTranslation(TranslationBase):
    master = models.ForeignKey(LivingSheet, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField(_("titre"), max_length=200)
    summary = models.CharField(_("résumé"), max_length=SUMMARY_MAX_LENGTH, blank=True)
    body = models.TextField(_("contenu"), blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["master", "language"], name="uniq_livingsheet_translation")]
        verbose_name = _("traduction de fiche")
        verbose_name_plural = _("traductions de fiches")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"
