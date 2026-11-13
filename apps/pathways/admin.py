"""Back-office for the Espace Personnes. Locked attributes are displayed, never editable."""

from __future__ import annotations

import csv

from django import forms
from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PublishableAdminMixin
from cms.translation import translation_matrix
from core.admin_base import BaseModelAdmin, BaseStackedInline, BaseTabularInline, LockedContentAdminMixin
from pathways.models import (
    Pathway,
    PathwayDocument,
    PathwayDocumentTranslation,
    PathwaySource,
    PathwayStep,
    PathwayStepTranslation,
    PathwayTranslation,
    PathwayWarning,
    PathwayWarningTranslation,
)

PENDING_HELP = _("CONTENT_PENDING_LEGAL_REVIEW : tant que la case est cochée, seul l’intitulé est publié.")


class PathwayTranslationInline(BaseStackedInline):
    model = PathwayTranslation
    fields = ("language", "status", "eligibility_context", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)


class PathwayStepInline(BaseTabularInline):
    model = PathwayStep
    fields = ("order", "title_fr", "text_fr", "pending_legal_review")
    ordering = ("order",)
    show_change_link = True


class PathwayDocumentInline(BaseTabularInline):
    model = PathwayDocument
    fields = ("order", "label_fr", "note_fr", "pending_legal_review")
    ordering = ("order",)
    show_change_link = True


class PathwayWarningInline(BaseTabularInline):
    model = PathwayWarning
    fields = ("order", "text_fr", "pending_legal_review")
    ordering = ("order",)
    show_change_link = True


class PathwaySourceInline(BaseTabularInline):
    model = PathwaySource
    fields = ("title", "url", "publisher", "retrieved_at", "note", "added_by")
    readonly_fields = ("added_by",)
    # Official sources are https-only; also silences Django's 6.0 URLField scheme deprecation.
    formfield_overrides = {models.URLField: {"form_class": forms.URLField, "assume_scheme": "https"}}


@admin.register(Pathway)
class PathwayAdmin(LockedContentAdminMixin, PublishableAdminMixin, BaseModelAdmin):
    locked_fields = ("key", "order", "locked", "locked_title", "locked_description")
    list_display = (
        "order",
        "locked_title",
        "key",
        "status",
        "publish_at",
        "last_reviewed_at",
        "reviewer",
        "pending_items",
        "translation_overview",
        "version",
    )
    list_display_links = ("locked_title",)
    list_filter = ("status",)
    search_fields = ("key", "eligibility_context_fr", "source_notes")
    ordering = ("order",)
    date_hierarchy = "last_reviewed_at"
    autocomplete_fields = ("hero_image", "author", "reviewer")
    inlines = (
        PathwayTranslationInline,
        PathwayStepInline,
        PathwayDocumentInline,
        PathwayWarningInline,
        PathwaySourceInline,
    )
    actions = ("export_review_status_csv",)
    fieldsets = (
        (
            _("Textes prescrits (registre p3.persons.pathways — non modifiables)"),
            {"fields": ("key", "order", "locked", "locked_title", "locked_description")},
        ),
        (_("Présentation"), {"fields": ("icon", "hero_image")}),
        (
            _("Contenu éditorial — CONTENT_PENDING_LEGAL_REVIEW"),
            {
                "fields": ("eligibility_context_fr", "authorities", "source_notes"),
                "description": _(
                    "Aucun critère d’éligibilité, délai ou condition légale ne doit être rédigé sans vérification "
                    "sur des sources primaires et validation par le référent juridique."
                ),
            },
        ),
        PUBLICATION_FIELDSET,
    )

    def has_add_permission(self, request):
        # The eight pathways are prescribed and seeded; nothing else can be added.
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_("Titre (verrouillé)"), ordering="order")
    def locked_title(self, obj):
        return obj.title if obj else ""

    @admin.display(description=_("Description (verrouillée)"))
    def locked_description(self, obj):
        return obj.description if obj else ""

    @admin.display(description=_("Éléments à vérifier"))
    def pending_items(self, obj):
        return (
            obj.steps.filter(pending_legal_review=True).count()
            + obj.documents.filter(pending_legal_review=True).count()
            + obj.warnings.filter(pending_legal_review=True).count()
        )

    @admin.display(description=_("Traductions"))
    def translation_overview(self, obj):
        matrix = translation_matrix(obj)
        return " · ".join(f"{lang}:{status}" for lang, status in matrix.items())

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, PathwaySource) and not instance.added_by_id:
                instance.added_by = request.user
            instance.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    @admin.action(description=_("Exporter l’état de révision (CSV)"))
    def export_review_status_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="pathways-review-status.csv"'
        writer = csv.writer(response)
        writer.writerow(["order", "key", "title", "status", "publish_at", "last_reviewed_at", "reviewer", "pending"])
        for obj in queryset.order_by("order"):
            writer.writerow(
                [
                    obj.order,
                    obj.key,
                    obj.title,
                    obj.status,
                    obj.publish_at.isoformat() if obj.publish_at else "",
                    obj.last_reviewed_at.isoformat() if obj.last_reviewed_at else "",
                    obj.reviewer.email if obj.reviewer else "",
                    self.pending_items(obj),
                ]
            )
        return response


class PathwayStepTranslationInline(BaseStackedInline):
    model = PathwayStepTranslation
    fields = ("language", "status", "title", "text", "source", "reviewed_by")


@admin.register(PathwayStep)
class PathwayStepAdmin(BaseModelAdmin):
    list_display = ("pathway", "order", "title_fr", "pending_legal_review", "updated_at")
    list_filter = ("pending_legal_review", "pathway")
    search_fields = ("title_fr", "text_fr")
    ordering = ("pathway__order", "order")
    inlines = (PathwayStepTranslationInline,)
    fieldsets = ((None, {"fields": ("pathway", "order", "title_fr", "text_fr", "pending_legal_review")}),)


class PathwayDocumentTranslationInline(BaseStackedInline):
    model = PathwayDocumentTranslation
    fields = ("language", "status", "label", "note", "source", "reviewed_by")


@admin.register(PathwayDocument)
class PathwayDocumentAdmin(BaseModelAdmin):
    list_display = ("pathway", "order", "label_fr", "pending_legal_review", "updated_at")
    list_filter = ("pending_legal_review", "pathway")
    search_fields = ("label_fr", "note_fr")
    ordering = ("pathway__order", "order")
    inlines = (PathwayDocumentTranslationInline,)
    fieldsets = ((None, {"fields": ("pathway", "order", "label_fr", "note_fr", "pending_legal_review")}),)


class PathwayWarningTranslationInline(BaseStackedInline):
    model = PathwayWarningTranslation
    fields = ("language", "status", "text", "source", "reviewed_by")


@admin.register(PathwayWarning)
class PathwayWarningAdmin(BaseModelAdmin):
    list_display = ("pathway", "order", "__str__", "pending_legal_review", "updated_at")
    list_filter = ("pending_legal_review", "pathway")
    search_fields = ("text_fr",)
    ordering = ("pathway__order", "order")
    inlines = (PathwayWarningTranslationInline,)
    fieldsets = ((None, {"fields": ("pathway", "order", "text_fr", "pending_legal_review")}),)
