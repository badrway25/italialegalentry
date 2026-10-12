"""
Back-office base classes. Every ModelAdmin in the project inherits from these so the editorial
UI is consistent (django-unfold) and audit metadata is always read-only.
"""

from __future__ import annotations

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline, TabularInline

AUDIT_READONLY_FIELDS = ("created_at", "updated_at")


class BaseModelAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        for f in AUDIT_READONLY_FIELDS:
            if hasattr(self.model, f) and f not in fields:
                fields.append(f)
        return fields


class BaseTabularInline(TabularInline):
    extra = 0


class BaseStackedInline(StackedInline):
    extra = 0


class LockedContentAdminMixin:
    """Fields listed in ``locked_fields`` come from the locked registry: shown, never editable."""

    locked_fields: tuple[str, ...] = ()

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        for f in self.locked_fields:
            if f not in fields:
                fields.append(f)
        return fields


def environment_badge(request):
    if settings.DEBUG:
        return [str(_("Sviluppo locale")), "warning"]
    return [str(_("Produzione")), "danger"]


def dashboard_callback(request, context):
    from core import gates
    from core.phases import console_rows

    snap = gates.snapshot()
    context["ile_gates"] = snap
    # The console says what each gate CONTROLS. The boolean rows below stay for the compact view;
    # a reader who needs to decide whether to open something needs the console.
    context["ile_phase_console"] = console_rows()
    context["ile_gate_rows"] = [
        (str(_("Pagine legali ufficiali (IT)")), snap["legal_pages_available"]),
        (str(_("Form pubblici attivi")), snap["public_forms_enabled"]),
        (str(_("Contenuti Fase 3 pubblici")), snap["phase3_public"]),
        (str(_("Banner Forum in homepage")), snap["forum_banner_visible"]),
        (str(_("Forum in modalità permanente")), snap["forum_permanent_mode"]),
        (str(_("Forum Virtuale")), snap["virtual_forum_enabled"]),
        (str(_("Newsletter")), snap["newsletter_enabled"]),
    ]
    return context
