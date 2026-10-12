from __future__ import annotations

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from cms.models import PublicationStatus
from cms.translation import translation_matrix
from core.admin_base import BaseModelAdmin, BaseStackedInline
from news import services
from news.editorial import clean_link_list
from news.models import Article, ArticleTranslation, NewsCategory

TRANSLATION_LANGUAGES = [
    (code, name) for code, name in settings.LANGUAGES if code != settings.CONTENT_FALLBACK_LANGUAGE
]
STATUS_LABELS = {
    PublicationStatus.DRAFT: "secondary",
    PublicationStatus.REVIEW: "warning",
    PublicationStatus.SCHEDULED: "info",
    PublicationStatus.PUBLISHED: "success",
    PublicationStatus.ARCHIVED: "danger",
}


def translation_matrix_html(obj) -> str:
    matrix = translation_matrix(obj)
    return format_html_join(
        " · ",
        '<span class="translation-status translation-status--{}" title="{}">{}: {}</span>',
        (
            (status, status, lang.upper(), status)
            for lang, status in matrix.items()
            if lang != settings.CONTENT_FALLBACK_LANGUAGE
        ),
    )


@admin.register(NewsCategory)
class NewsCategoryAdmin(BaseModelAdmin):
    list_display = ("name_fr", "slug", "order", "article_count")
    list_editable = ("order",)
    search_fields = ("name_fr", "name_it", "name_en", "name_ar", "slug")
    prepopulated_fields = {"slug": ("name_fr",)}
    fieldsets = (
        (None, {"fields": ("slug", "order")}),
        (_("Libellés"), {"fields": ("name_fr", "name_it", "name_en", "name_ar")}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description=_("articles"))
    def article_count(self, obj) -> int:
        return obj.articles.count()


class ArticleTranslationForm(forms.ModelForm):
    class Meta:
        model = ArticleTranslation
        fields = (
            "language",
            "status",
            "source",
            "reviewed_by",
            "title",
            "summary",
            "body",
            "seo_title",
            "seo_description",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"].choices = TRANSLATION_LANGUAGES


class ArticleTranslationInline(BaseStackedInline):
    model = ArticleTranslation
    form = ArticleTranslationForm
    max_num = len(TRANSLATION_LANGUAGES)
    verbose_name = _("traduction")
    verbose_name_plural = _("traductions (IT / EN / AR) — seules les traductions « publiées » sont visibles en ligne")
    fields = ("language", "status", "source", "reviewed_by", "title", "summary", "body", "seo_title", "seo_description")
    autocomplete_fields = ("reviewed_by",)


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        # The admin replaces this list with the fields declared in ``fieldsets``.
        fields = ("source_links", "related")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and "related" in self.fields:
            self.fields["related"].queryset = Article.objects.exclude(pk=self.instance.pk)

    def clean_source_links(self):
        try:
            return clean_link_list(self.cleaned_data.get("source_links") or [])
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages) from exc


@admin.register(Article)
class ArticleAdmin(PublishableAdminMixin, BaseModelAdmin):
    form = ArticleAdminForm
    inlines = (ArticleTranslationInline,)
    list_display = (
        "title_fr",
        "category",
        "status_badge",
        "date_published",
        "last_updated",
        "editor",
        "translations",
        "version",
    )
    list_filter = ("status", "category", "editor")
    list_select_related = ("category", "editor")
    search_fields = ("title_fr", "summary_fr", "body_fr", "slug", "translations__title")
    date_hierarchy = "publish_at"
    ordering = ("-publish_at", "-published_at", "-created_at")
    prepopulated_fields = {"slug": ("title_fr",)}
    autocomplete_fields = ("category", "hero_image", "og_image", "related")
    readonly_fields = PUBLICATION_READONLY + ("editor",)
    actions = ("action_submit_for_review", "action_publish", "action_archive", "action_back_to_draft")
    fieldsets = (
        (None, {"fields": ("title_fr", "slug", "category", "summary_fr", "body_fr")}),
        (_("Image"), {"fields": ("hero_image", "image_caption")}),
        (_("Sources et articles liés"), {"fields": ("source_links", "related")}),
        (_("SEO et partage"), {"fields": ("seo_title", "seo_description", "og_image")}),
        (_("Éditorial"), {"fields": ("editor", "last_updated")}),
        PUBLICATION_FIELDSET,
    )

    # -- permissions -----------------------------------------------------------------------
    def has_publish_permission(self, request) -> bool:
        return services.can_publish(request.user)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not self.has_publish_permission(request):
            # Status changes to PUBLISHED/SCHEDULED go through the audited actions only.
            for name in ("status", "publish_at", "unpublish_at", "reviewer"):
                if name not in fields:
                    fields.append(name)
        return fields

    def save_model(self, request, obj, form, change):
        publishing = obj.status in (PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED)
        if publishing and not self.has_publish_permission(request):
            raise PermissionDenied
        obj.editor = request.user
        super().save_model(request, obj, form, change)

    # -- list columns ----------------------------------------------------------------------
    @admin.display(description=_("état"), ordering="status")
    def status_badge(self, obj):
        return format_html(
            '<span class="status-badge status-badge--{}">{}</span>',
            STATUS_LABELS.get(obj.status, "secondary"),
            obj.get_status_display(),
        )

    @admin.display(description=_("publié le"), ordering="publish_at")
    def date_published(self, obj):
        return obj.date_published

    @admin.display(description=_("traductions"))
    def translations(self, obj):
        return translation_matrix_html(obj)

    # -- workflow actions (audited, permission-checked in services) ------------------------
    def _run(self, request, queryset, func, label):
        done = 0
        for article in queryset:
            try:
                func(article, request.user, request)
                done += 1
            except PermissionDenied:
                messages.error(request, _("Permission refusée : seuls les utilisateurs autorisés peuvent publier."))
                return
            except ValidationError as exc:
                messages.warning(request, f"{article}: {'; '.join(exc.messages)}")
        if done:
            messages.success(request, _("%(n)d article(s) : %(label)s.") % {"n": done, "label": label})

    @admin.action(description=_("Soumettre à la revue"))
    def action_submit_for_review(self, request, queryset):
        self._run(request, queryset, services.submit_for_review, _("soumis à la revue"))

    @admin.action(description=_("Publier (permission « publier des articles » requise)"), permissions=["publish"])
    def action_publish(self, request, queryset):
        self._run(request, queryset, services.publish, _("publié(s)"))

    @admin.action(description=_("Archiver"))
    def action_archive(self, request, queryset):
        self._run(request, queryset, services.archive, _("archivé(s)"))

    @admin.action(description=_("Renvoyer en brouillon"))
    def action_back_to_draft(self, request, queryset):
        self._run(request, queryset, services.back_to_draft, _("renvoyé(s) en brouillon"))
