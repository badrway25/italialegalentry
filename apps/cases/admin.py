"""
Back-office of the digital case file.

Deliberately restrained: the case file is an operational workspace for the person and for assigned
actors, not an admin table. What lives here is supervision — reading a case, correcting a mistake,
revoking an assignment — never the day-to-day work, which belongs to the platform itself.

Two things are read-only by construction and not merely hidden:
* a ``PathwayAssessment`` is frozen evidence. Editing one would destroy the reproducibility claim;
* ``status`` is not editable in the form. State changes go through ``services.transition`` so that
  the declared transition table and the audit trail cannot be bypassed from the admin.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from cases.models import CaseAssignment, CaseFile, ChecklistItem, PathwayAssessment


class ChecklistInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0
    fields = ("order", "requirement", "status", "responsible_actor", "responsible_note", "due_date")
    ordering = ("order", "id")


class AssignmentInline(admin.TabularInline):
    model = CaseAssignment
    extra = 0
    fields = (
        "assignee",
        "role",
        "organisation",
        "authorisation_reference",
        "authorisation_valid_until",
        "assigned_at",
        "revoked_at",
    )
    readonly_fields = ("assigned_at",)
    autocomplete_fields = ("assignee",)


class AssessmentInline(admin.TabularInline):
    model = PathwayAssessment
    extra = 0
    can_delete = False
    fields = ("assessed_at", "outcome", "pathway_key", "ruleset_version")
    readonly_fields = fields
    show_change_link = True

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(CaseFile)
class CaseFileAdmin(admin.ModelAdmin):
    list_display = ("reference", "person", "purpose", "status", "status_since", "open_items")
    list_filter = ("status", "purpose")
    search_fields = ("reference", "person__email", "pathway_key")
    readonly_fields = ("reference", "uuid", "status", "status_since", "previous_status", "closed_at", "created_at")
    fields = (
        "reference",
        "uuid",
        "person",
        "purpose",
        "pathway_key",
        "status",
        "status_since",
        "previous_status",
        "suspension_reason",
        "closed_at",
        "created_at",
    )
    inlines = (ChecklistInline, AssignmentInline, AssessmentInline)
    autocomplete_fields = ("person",)

    @admin.display(description=_("voci aperte"))
    def open_items(self, obj: CaseFile) -> str:
        from cases.services import progress

        counts = progress(obj)
        if counts["overdue"]:
            return format_html(
                "<strong>{} / {}</strong> ({} in ritardo)", counts["open"], counts["total"], counts["overdue"]
            )
        return f"{counts['open']} / {counts['total']}"


@admin.register(PathwayAssessment)
class PathwayAssessmentAdmin(admin.ModelAdmin):
    """Read-only: an assessment is frozen evidence of what the engine decided and with which rules."""

    list_display = ("case", "assessed_at", "outcome", "pathway_key", "ruleset_version")
    list_filter = ("outcome", "purpose")
    search_fields = ("case__reference",)
    readonly_fields = [field.name for field in PathwayAssessment._meta.fields]

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(CaseAssignment)
class CaseAssignmentAdmin(admin.ModelAdmin):
    list_display = ("case", "assignee", "role", "authorisation_reference", "authorisation_valid_until", "revoked_at")
    list_filter = ("role",)
    search_fields = ("case__reference", "assignee__email", "authorisation_reference")
    autocomplete_fields = ("assignee", "case")
