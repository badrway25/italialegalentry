from __future__ import annotations

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from cms.models import PublicationStatus
from core.admin_base import BaseModelAdmin, BaseStackedInline, BaseTabularInline
from living import services
from living.models import LegalReviewStatus, LivingSheet, LivingSheetTranslation, LivingTopic, LivingTopicTranslation
from news.admin import translation_matrix_html
from news.editorial import clean_link_list

TRANSLATION_LANGUAGES = [
    (code, name) for code, name in settings.LANGUAGES if code != settings.CONTENT_FALLBACK_LANGUAGE
]


class _TranslationLanguageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "language" in self.fields:
            self.fields["language"].choices = TRANSLATION_LANGUAGES


class LivingTopicTranslationInline(BaseStackedInline):
    model = LivingTopicTranslation
    form = _TranslationLanguageForm
    max_num = len(TRANSLATION_LANGUAGES)
    fields = ("language", "status", "source", "reviewed_by", "name", "intro")
    autocomplete_fields = ("reviewed_by",)
    verbose_name = _("traduction")
    verbose_name_plural = _("traductions (IT / EN / AR)")


class LivingSheetInline(BaseTabularInline):
    model = LivingSheet
    fields = ("title_fr", "slug", "order", "legal_review", "status", "last_reviewed_at")
    readonly_fields = ("status", "legal_review", "last_reviewed_at")
    show_change_link = True
    verbose_name = _("fiche")
    verbose_name_plural = _("fiches du thème (édition complète via le lien)")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(LivingTopic)
class LivingTopicAdmin(PublishableAdminMixin, BaseModelAdmin):
    inlines = (LivingTopicTranslationInline, LivingSheetInline)
    list_display = ("name_fr", "slug", "order", "status", "icon", "sheet_counts", "translations", "version")
    list_editable = ("order",)
    list_filter = ("status",)
    search_fields = ("name_fr", "slug", "intro_fr", "translations__name")
    prepopulated_fields = {"slug": ("name_fr",)}
    fieldsets = (
        (None, {"fields": ("name_fr", "slug", "order", "icon")}),
        (_("Introduction (CONTENT_PENDING_LEGAL_REVIEW jusqu’à validation)"), {"fields": ("intro_fr",)}),
        PUBLICATION_FIELDSET,
    )

    @admin.display(description=_("fiches (publiées / total)"))
    def sheet_counts(self, obj):
        total = obj.sheets.count()
        live = obj.sheets.public().count()
        return f"{live} / {total}"

    @admin.display(description=_("traductions"))
    def translations(self, obj):
        return translation_matrix_html(obj)


class LivingSheetTranslationInline(BaseStackedInline):
    model = LivingSheetTranslation
    form = _TranslationLanguageForm
    max_num = len(TRANSLATION_LANGUAGES)
    fields = ("language", "status", "source", "reviewed_by", "title", "summary", "body")
    autocomplete_fields = ("reviewed_by",)
    verbose_name = _("traduction")
    verbose_name_plural = _("traductions (IT / EN / AR)")


class LivingSheetAdminForm(forms.ModelForm):
    class Meta:
        model = LivingSheet
        # The admin replaces this list with the fields declared in ``fieldsets``.
        fields = ("sources",)

    def clean_sources(self):
        try:
            return clean_link_list(self.cleaned_data.get("sources") or [])
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages) from exc


@admin.register(LivingSheet)
class LivingSheetAdmin(PublishableAdminMixin, BaseModelAdmin):
    form = LivingSheetAdminForm
    inlines = (LivingSheetTranslationInline,)
    list_display = (
        "title_fr",
        "topic",
        "legal_review_badge",
        "status",
        "last_reviewed_at",
        "reviewer",
        "translations",
        "version",
    )
    list_filter = ("topic", "legal_review", "status")
    list_select_related = ("topic", "reviewer")
    search_fields = ("title_fr", "summary_fr", "body_fr", "slug", "translations__title")
    prepopulated_fields = {"slug": ("title_fr",)}
    autocomplete_fields = ("topic",)
    readonly_fields = PUBLICATION_READONLY
    actions = ("action_mark_reviewed", "action_submit_for_review", "action_publish", "action_archive")
    fieldsets = (
        (None, {"fields": ("topic", "title_fr", "slug", "order", "summary_fr", "body_fr", "sources")}),
        (
            _("Revue juridique — CONTENT_PENDING_LEGAL_REVIEW"),
            {
                "description": _(
                    "Aucune fiche n’est publiable tant qu’elle n’a pas été revue et validée (réviseur + date). "
                    "Ne jamais rédiger de contenu juridique sans source officielle vérifiée."
                ),
                "fields": ("legal_review",),
            },
        ),
        PUBLICATION_FIELDSET,
    )

    def has_publish_permission(self, request) -> bool:
        return services.can_publish(request.user)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not self.has_publish_permission(request):
            for name in ("status", "publish_at", "unpublish_at"):
                if name not in fields:
                    fields.append(name)
        return fields

    def save_model(self, request, obj, form, change):
        if obj.status in (PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED) and not self.has_publish_permission(
            request
        ):
            raise PermissionDenied
        super().save_model(request, obj, form, change)

    @admin.display(description=_("revue juridique"), ordering="legal_review")
    def legal_review_badge(self, obj):
        css = "success" if obj.legal_review == LegalReviewStatus.REVIEWED else "warning"
        return format_html('<span class="status-badge status-badge--{}">{}</span>', css, obj.get_legal_review_display())

    @admin.display(description=_("traductions"))
    def translations(self, obj):
        return translation_matrix_html(obj)

    def _run(self, request, queryset, func, label):
        done = 0
        for sheet in queryset:
            try:
                func(sheet, request.user, request)
                done += 1
            except PermissionDenied:
                messages.error(request, _("Permission refusée : seuls les utilisateurs autorisés peuvent publier."))
                return
            except ValidationError as exc:
                messages.warning(request, f"{sheet}: {'; '.join(exc.messages)}")
        if done:
            messages.success(request, _("%(n)d fiche(s) : %(label)s.") % {"n": done, "label": label})

    @admin.action(description=_("Marquer comme revue juridiquement (réviseur = vous, date = maintenant)"))
    def action_mark_reviewed(self, request, queryset):
        self._run(request, queryset, services.mark_reviewed, _("revue(s) et validée(s)"))

    @admin.action(description=_("Soumettre à la revue éditoriale"))
    def action_submit_for_review(self, request, queryset):
        self._run(request, queryset, services.submit_for_review, _("soumise(s) à la revue"))

    @admin.action(description=_("Publier (permission « publier des fiches » requise)"), permissions=["publish"])
    def action_publish(self, request, queryset):
        self._run(request, queryset, services.publish, _("publiée(s)"))

    @admin.action(description=_("Archiver"))
    def action_archive(self, request, queryset):
        self._run(request, queryset, services.archive, _("archivée(s)"))
