"""
Back-office for the glossary.

* Locked terms (the ten prescribed entries) show ``key`` / ``term`` / ``definition_fr`` read-only and
  cannot be deleted (gate G0). Editors can relate them, add a source / review date, schedule them
  and add translations (official texts only, gate G10).
* Editors may create *new* unlocked terms.
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
from glossary.models import Term, TermTranslation

LOCKED_TERM_FIELDS = ("key", "term", "definition_fr")


def _matrix_html(obj) -> str:
    labels = dict(TranslationStatus.choices)
    matrix = translation_matrix(obj)
    return format_html(
        '<table class="translation-matrix"><tbody>{}</tbody></table>',
        format_html_join(
            "",
            '<tr><th scope="row">{} ({})</th><td data-status="{}">{}</td></tr>',
            ((name, code, matrix[code], labels.get(matrix[code], matrix[code])) for code, name in settings.LANGUAGES),
        ),
    )


def _matrix_summary(obj) -> str:
    fallback = settings.CONTENT_FALLBACK_LANGUAGE
    labels = dict(TranslationStatus.choices)
    return " · ".join(
        f"{code}: {labels.get(status, status)}" for code, status in translation_matrix(obj).items() if code != fallback
    )


class TermTranslationInline(BaseTabularInline):
    model = TermTranslation
    fields = ("language", "status", "term", "definition", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)
    verbose_name = _("traduzione")
    verbose_name_plural = _("traduzioni (solo testi ufficiali trasmessi; stato «pubblicata» per renderle online)")


@admin.register(Term)
class TermAdmin(LockedContentAdminMixin, PublishableAdminMixin, BaseModelAdmin):
    # ``locked_fields`` is resolved per object: only rows with ``is_locked`` become read-only.
    locked_fields = ()
    list_display = (
        "term",
        "key",
        "status",
        "is_locked",
        "source",
        "last_reviewed_at",
        "translation_summary",
        "updated_at",
    )
    list_filter = ("status", "is_locked")
    search_fields = ("term", "key", "definition_fr", "translations__term", "translations__definition")
    autocomplete_fields = ("related", "author", "reviewer")
    readonly_fields = PUBLICATION_READONLY + ("is_locked", "translation_status_matrix")
    ordering = ("term",)
    inlines = (TermTranslationInline,)
    actions = ("export_csv",)
    fieldsets = (
        (None, {"fields": ("term", "key", "is_locked")}),
        (
            _("Definizione (FR — testo sorgente). I termini bloccati provengono dal registro dei testi prescritti."),
            {"fields": ("definition_fr", "source", "related")},
        ),
        (_("Stato delle traduzioni"), {"fields": ("translation_status_matrix",)}),
        PUBLICATION_FIELDSET,
    )

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None and obj.is_locked:
            for name in LOCKED_TERM_FIELDS:
                if name not in fields:
                    fields.append(name)
        return fields

    def get_prepopulated_fields(self, request, obj=None):
        if obj is None:
            return {"key": ("term",)}
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

    @admin.action(description=_("Esporta i termini selezionati (CSV)"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="glossaire.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ["key", "term", "status", "is_locked", "source", "last_reviewed_at", "definition_fr", "related"]
        )
        for term in queryset.prefetch_related("related"):
            writer.writerow(
                [
                    term.key,
                    term.term,
                    term.status,
                    term.is_locked,
                    term.source,
                    term.last_reviewed_at.isoformat() if term.last_reviewed_at else "",
                    term.definition_fr,
                    "|".join(sorted(r.key for r in term.related.all())),
                ]
            )
        return response
