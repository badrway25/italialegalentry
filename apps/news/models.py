"""
Actualités (news): categories, articles with editorial workflow, translations.

Articles follow ``cms.models.PublishableModel`` (DRAFT → REVIEW → SCHEDULED/PUBLISHED → ARCHIVED).
Only users holding the custom permission ``news.publish_article`` can publish (see services).
Body text is plain editorial markup (``news.editorial``): editors never write HTML.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms.models import PublishableModel, PublishableQuerySet, TranslationBase
from cms.translation import resolve
from core.models import TimeStampedModel
from news.editorial import plain_text, validate_link_list

SUMMARY_MAX_LENGTH = 300
SEO_TITLE_MAX_LENGTH = 70
SEO_DESCRIPTION_MAX_LENGTH = 160


class NewsCategory(TimeStampedModel):
    """Editorial category (Normativa, Échéances, Forum, Écosystème…). Labels are UI content, not locked."""

    slug = models.SlugField(_("slug"), max_length=60, unique=True)
    name_fr = models.CharField("Nom (FR)", max_length=80)
    name_it = models.CharField("Nome (IT)", max_length=80, blank=True)
    name_en = models.CharField("Name (EN)", max_length=80, blank=True)
    name_ar = models.CharField("الاسم (AR)", max_length=80, blank=True)
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)

    class Meta:
        ordering = ["order", "name_fr"]
        verbose_name = _("catégorie d’actualité")
        verbose_name_plural = _("catégories d’actualités")

    def __str__(self) -> str:
        return self.name_fr

    def name(self, lang: str | None = None) -> str:
        """Label in ``lang`` (defaults to the active language) with French fallback."""
        lang = (lang or translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
        return getattr(self, f"name_{lang}", "") or self.name_fr

    @property
    def name_is_fallback(self) -> bool:
        """True when the active language has no label and the French one is shown (needs lang="fr")."""
        lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
        return lang != "fr" and not getattr(self, f"name_{lang}", "")

    def get_absolute_url(self) -> str:
        return f"{reverse('news:index')}?categorie={self.slug}"


class ArticleQuerySet(PublishableQuerySet):
    def with_dates(self):
        return self.annotate(date_published_db=Coalesce("publish_at", "published_at"))

    def public(self, at=None):
        """Live articles ordered by publication date (newest first) with the usual joins."""
        return (
            self.live(at)
            .with_dates()
            .select_related("category", "hero_image", "og_image")
            .order_by("-date_published_db", "-id")
        )


@dataclass(frozen=True)
class ArticleText:
    """Language-resolved texts of an article (gate G10: only PUBLISHED translations are public)."""

    title: str
    summary: str
    body: str
    seo_title: str
    seo_description: str
    language: str
    is_fallback: bool


class Article(PublishableModel):
    slug = models.SlugField(_("slug"), max_length=120, unique=True)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.PROTECT, related_name="articles", verbose_name=_("catégorie")
    )
    title_fr = models.CharField("Titre (FR)", max_length=200)
    summary_fr = models.CharField(
        "Résumé (FR)",
        max_length=SUMMARY_MAX_LENGTH,
        help_text=_("Chapeau affiché dans la liste et comme description par défaut (300 caractères max.)."),
    )
    body_fr = models.TextField(
        "Corps (FR)",
        help_text=_(
            "Texte brut : paragraphes séparés par une ligne vide ; « ## » en début de ligne pour un intertitre ; "
            "« - » pour une liste. Aucun HTML n’est interprété."
        ),
    )
    hero_image = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("image principale"),
    )
    image_caption = models.CharField(_("légende de l’image"), max_length=200, blank=True)
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("dernier éditeur"),
    )
    source_links = models.JSONField(
        _("sources"),
        default=list,
        blank=True,
        validators=[validate_link_list],
        help_text=_('Liste JSON de {"label": "…", "url": "https://…"} — liens simples, jamais de contenu intégré.'),
    )
    related = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="related_to", verbose_name=_("articles liés")
    )
    last_updated = models.DateTimeField(
        _("dernière mise à jour éditoriale"),
        null=True,
        blank=True,
        help_text=_("Date affichée comme « mis à jour le » ; vide = date de publication."),
    )
    seo_title = models.CharField(_("titre SEO"), max_length=SEO_TITLE_MAX_LENGTH, blank=True)
    seo_description = models.CharField(_("description SEO"), max_length=SEO_DESCRIPTION_MAX_LENGTH, blank=True)
    og_image = models.ForeignKey(
        "cms.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("image de partage (Open Graph)"),
    )

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_at", "-published_at", "-created_at"]
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        permissions = [("publish_article", "Can publish news articles")]
        indexes = [models.Index(fields=["status", "publish_at"], name="news_article_status_pub_idx")]

    def __str__(self) -> str:
        return self.title_fr

    def get_absolute_url(self) -> str:
        return reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def date_published(self):
        return self.publish_at or self.published_at

    @property
    def date_modified(self):
        return self.last_updated or self.date_published

    @property
    def share_image(self):
        return self.og_image or self.hero_image

    def texts(self, lang: str | None = None) -> ArticleText:
        """Resolve public texts for ``lang`` (PUBLISHED translation) with French fallback."""
        lang = (lang or settings.LANGUAGE_CODE).split("-")[0]
        row, effective, _is_fb = resolve(self, lang)
        if row is not None and effective == lang and lang != settings.CONTENT_FALLBACK_LANGUAGE:
            return ArticleText(
                title=row.title,
                summary=row.summary or self.summary_fr,
                body=row.body or self.body_fr,
                seo_title=row.seo_title or row.title,
                seo_description=row.seo_description or row.summary or self.summary_fr,
                language=lang,
                is_fallback=False,
            )
        fallback = settings.CONTENT_FALLBACK_LANGUAGE
        return ArticleText(
            title=self.title_fr,
            summary=self.summary_fr,
            body=self.body_fr,
            seo_title=self.seo_title or self.title_fr,
            seo_description=self.seo_description or self.summary_fr or plain_text(self.body_fr, 160),
            language=fallback,
            is_fallback=lang != fallback,
        )


class ArticleTranslation(TranslationBase):
    master = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField(_("titre"), max_length=200)
    summary = models.CharField(_("résumé"), max_length=SUMMARY_MAX_LENGTH, blank=True)
    body = models.TextField(_("corps"), blank=True)
    seo_title = models.CharField(_("titre SEO"), max_length=SEO_TITLE_MAX_LENGTH, blank=True)
    seo_description = models.CharField(_("description SEO"), max_length=SEO_DESCRIPTION_MAX_LENGTH, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["master", "language"], name="uniq_article_translation")]
        verbose_name = _("traduction d’article")
        verbose_name_plural = _("traductions d’articles")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"
