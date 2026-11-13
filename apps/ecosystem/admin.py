"""
Back-office for the ecosystem spaces.

* ``EcosystemSpace`` — editors choose the photograph and may write an optional introductory note
  (with translations). The page key and its publication gate are structural: read-only once created,
  and the four rows are seeded, so nothing can be added or deleted by hand.
* ``PilotStep`` — the eight prescribed steps (``p3.pilot.sequence``) are shown read-only and cannot be
  deleted (gate G0). Editors may add *new* steps after the prescribed sequence; an addition stays
  hidden until « visibile nel diagramma » is ticked.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from cms.translation import translation_matrix
from core.admin_base import BaseModelAdmin, BaseTabularInline, LockedContentAdminMixin
from ecosystem.models import EcosystemSpace, EcosystemSpaceTranslation, PilotStep, SpaceKey

LOCKED_STEP_FIELDS = ("order", "label_fr", "is_visible")


class EcosystemSpaceTranslationInline(BaseTabularInline):
    model = EcosystemSpaceTranslation
    fields = ("language", "status", "intro_note", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)
    verbose_name = _("traduzione della nota editoriale")
    verbose_name_plural = _("traduzioni della nota editoriale (stato «pubblicata» per renderle online)")


@admin.register(EcosystemSpace)
class EcosystemSpaceAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_display = ("key", "order", "status", "requires_gate", "hero_image", "translation_summary", "updated_at")
    list_editable = ("order",)
    list_filter = ("status", "requires_gate")
    search_fields = ("key", "intro_note_fr", "translations__intro_note")
    autocomplete_fields = ("hero_image", "author", "reviewer")
    readonly_fields = PUBLICATION_READONLY + ("requires_gate", "prescribed_texts")
    ordering = ("order", "id")
    inlines = (EcosystemSpaceTranslationInline,)
    fieldsets = (
        (None, {"fields": ("key", "order", "requires_gate")}),
        (
            _("Testi prescritti (registro dei testi bloccati — non modificabili)"),
            {"fields": ("prescribed_texts",)},
        ),
        (_("Livello editoriale"), {"fields": ("hero_image", "intro_note_fr")}),
        PUBLICATION_FIELDSET,
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    PRESCRIBED_KEYS = {
        SpaceKey.COMPANIES: ("p1.companies.title", "p1.companies.intro", "p1.companies.quote"),
        SpaceKey.INSTITUTIONS: ("p3.institutions.intro", "p3.institutions.recipients", "p3.institutions.button"),
        SpaceKey.UNIVERSITIES: ("p3.universities.intro", "p3.universities.button"),
        SpaceKey.PILOT: ("p3.pilot.title", "p3.pilot.body", "p3.pilot.sequence"),
    }

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None and "key" not in fields:
            fields.append("key")  # the page a row belongs to never changes
        return fields

    def has_add_permission(self, request):
        # Exactly four spaces exist (seeded); a fifth page cannot be invented from the back-office.
        return super().has_add_permission(request) and EcosystemSpace.objects.count() < len(SpaceKey.values)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_("Chiavi del registro"))
    def prescribed_texts(self, obj) -> str:
        if obj is None or not obj.key:
            return "—"
        return ", ".join(self.PRESCRIBED_KEYS.get(obj.key, ()))

    @admin.display(description=_("Traduzioni"))
    def translation_summary(self, obj) -> str:
        from django.conf import settings

        fallback = settings.CONTENT_FALLBACK_LANGUAGE
        return " · ".join(f"{code}: {status}" for code, status in translation_matrix(obj).items() if code != fallback)


@admin.register(PilotStep)
class PilotStepAdmin(LockedContentAdminMixin, BaseModelAdmin):
    # ``locked_fields`` is resolved per object: only the prescribed rows become read-only.
    locked_fields = ()
    list_display = ("order", "label_fr", "is_locked", "is_visible", "updated_at")
    list_display_links = ("label_fr",)
    list_filter = ("is_locked", "is_visible")
    search_fields = ("label_fr",)
    readonly_fields = ("is_locked", "locked_index")
    ordering = ("order",)
    fieldsets = (
        (
            _("Tappa (le otto tappe prescritte provengono dal registro dei testi bloccati)"),
            {"fields": ("order", "label_fr", "is_visible", "is_locked", "locked_index")},
        ),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None and obj.is_locked:
            for name in LOCKED_STEP_FIELDS:
                if name not in fields:
                    fields.append(name)
        return fields

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_locked:
            return False
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)  # bulk delete would bypass the per-object lock
        return actions
