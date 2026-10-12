"""
Back-office for the FAQ.

* Locked items (the nine prescribed entries) show ``question_fr`` / ``answer_fr`` / ``key`` read-only
  and cannot be deleted (gate G0). Editors can still reorder them, move them between categories,
  schedule them and add translations (official texts only, gate G10).
* Editors may create *new* unlocked entries and categories.
"""

from __future__ import annotations

import csv

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from cms.models import TranslationStatus
from cms.translation import translation_matrix
from core.admin_base import BaseModelAdmin, BaseTabularInline, LockedContentAdminMixin
from faq.models import FAQCategory, FAQCategoryTranslation, FAQItem, FAQItemTranslation

LOCKED_ITEM_FIELDS = ("key", "question_fr", "answer_fr")


def _matrix_html(obj) -> str:
    labels = dict(TranslationStatus.choices)
    rows = (
        (code, name, labels.get(status, status), status)
        for (code, name), status in zip(settings.LANGUAGES, translation_matrix(obj).values(), strict=True)
    )
    return format_html(
        '<table class="translation-matrix"><tbody>{}</tbody></table>',
        format_html_join(
            "",
            '<tr><th scope="row">{} ({})</th><td data-status="{}">{}</td></tr>',
            ((name, code, status, label) for code, name, label, status in rows),
        ),
    )


def _matrix_summary(obj) -> str:
    fallback = settings.CONTENT_FALLBACK_LANGUAGE
    labels = dict(TranslationStatus.choices)
    parts = [
        f"{code}: {labels.get(status, status)}" for code, status in translation_matrix(obj).items() if code != fallback
    ]
    return " · ".join(parts)


class FAQCategoryTranslationInline(BaseTabularInline):
    model = FAQCategoryTranslation
    fields = ("language", "name", "status", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)


@admin.register(FAQCategory)
class FAQCategoryAdmin(BaseModelAdmin):
    list_display = ("name_fr", "slug", "order", "item_count", "translation_summary", "updated_at")
    list_editable = ("order",)
    search_fields = ("name_fr", "slug", "translations__name")
    prepopulated_fields = {"slug": ("name_fr",)}
    ordering = ("order", "name_fr")
    inlines = (FAQCategoryTranslationInline,)
    fieldsets = (
        (None, {"fields": ("name_fr", "slug", "order")}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description=_("FAQ"))
    def item_count(self, obj) -> int:
        return obj.items.count()

    @admin.display(description=_("Traduzioni"))
    def translation_summary(self, obj) -> str:
        return _matrix_summary(obj)


class FAQItemTranslationInline(BaseTabularInline):
    model = FAQItemTranslation
    fields = ("language", "status", "question", "answer", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)
    verbose_name = _("traduzione")
    verbose_name_plural = _("traduzioni (solo testi ufficiali trasmessi; stato «pubblicata» per renderle online)")


@admin.register(FAQItem)
class FAQItemAdmin(LockedContentAdminMixin, PublishableAdminMixin, BaseModelAdmin):
    # ``locked_fields`` is resolved per object: only rows with ``is_locked`` become read-only.
    locked_fields = ()
    list_display = (
        "question_fr",
        "category",
        "order",
        "status",
        "is_locked",
        "last_updated",
        "translation_summary",
        "updated_at",
    )
    list_display_links = ("question_fr",)
    list_editable = ("order",)
    list_filter = ("status", "category", "is_locked")
    search_fields = ("question_fr", "answer_fr", "key", "translations__question", "translations__answer")
    autocomplete_fields = ("category", "author", "reviewer")
    readonly_fields = PUBLICATION_READONLY + ("is_locked", "translation_status_matrix")
    date_hierarchy = "last_updated"
    ordering = ("category__order", "order", "id")
    inlines = (FAQItemTranslationInline,)
    actions = ("export_csv",)
    fieldsets = (
        (None, {"fields": ("category", "order", "key", "is_locked")}),
        (
            _("Contenuto (FR — testo sorgente). Le FAQ bloccate provengono dal registro dei testi prescritti."),
            {"fields": ("question_fr", "answer_fr", "last_updated")},
        ),
        (_("Stato delle traduzioni"), {"fields": ("translation_status_matrix",)}),
        PUBLICATION_FIELDSET,
    )

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None and obj.is_locked:
            for name in LOCKED_ITEM_FIELDS:
                if name not in fields:
                    fields.append(name)
        return fields

    def get_prepopulated_fields(self, request, obj=None):
        if obj is None:
            return {"key": ("question_fr",)}
        return {}

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_locked:
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_locked = False  # only the seed may lock rows
        super().save_model(request, obj, form, change)

    @admin.display(description=_("Traduzioni"))
    def translation_summary(self, obj) -> str:
        return _matrix_summary(obj)

    @admin.display(description=_("Stato per lingua"))
    def translation_status_matrix(self, obj):
        if obj is None or obj.pk is None:
            return "—"
        return _matrix_html(obj)

    @admin.action(description=_("Esporta le FAQ selezionate (CSV)"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="faq.csv"'
        writer = csv.writer(response)
        writer.writerow(["key", "category", "order", "status", "is_locked", "last_updated", "question_fr", "answer_fr"])
        for item in queryset.select_related("category"):
            writer.writerow(
                [
                    item.key,
                    item.category.slug,
                    item.order,
                    item.status,
                    item.is_locked,
                    item.last_updated.isoformat(),
                    item.question_fr,
                    item.answer_fr,
                ]
            )
        return response
