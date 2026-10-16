"""
Back-office of the digital case file.

Deliberately restrained: the case file is an operational workspace for the person and for assigned
actors, not an admin table. What lives here is supervision — reading a case, correcting a mistake,
revoking an assignment — never the day-to-day work, which belongs to the platform itself.

Two things are read-only by construction and not merely hidden:
* a ``PathwayAssessment`` is frozen evidence. Editing one would destroy the reproducibility claim;
* ``status`` is not editable in the form. State changes go through ``services.transition`` so that
  the declared transition table and the audit trail cannot be bypassed from the admin.

And since finding F-7 a third: WHO may move a file is read from the capacity an account holds on it —
its owner, or the role of a live assignment (``services.permitted_transitions``) — so a capacity IS a
right to a move, and none is handed out here (sec-f7 REVIEW, finding 2). A file's ``person`` and its
``suspension_reason`` are read-only: a file's owner never changes (a new file is opened), and the
reason is written by the domain with the move (CASE_LIFECYCLE.md §4, rules 3 and 4). An assignment
is granted by ``services.assign`` and ended by ``services.revoke_assignment`` — both audit the act
and tell the account concerned — and nothing else of it is editable; only an account the
assignment's own policy lets change it (the administrator) ends one. A file is opened by
``services.open_case``, never added here.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from cases.models import CaseAssignment, CaseFile, ChecklistItem, PathwayAssessment

#: An assignment's fields, in the order its screens show them. Its case, its assignee, its role and its
#: validity ARE the capacity: none of them changes once granted — revoke it and grant a new one.
ASSIGNMENT_FIELDS = (
    "case",
    "assignee",
    "role",
    "organisation",
    "authorisation_reference",
    "authorisation_jurisdiction",
    "authorisation_valid_until",
    "mandate_note",
    "assigned_at",
    "revoked_at",
)


class ChecklistInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0
    fields = ("order", "requirement", "status", "responsible_actor", "responsible_note", "due_date")
    ordering = ("order", "id")


class AssignmentInline(admin.TabularInline):
    """Who holds a capacity on the file — shown, never edited here: granting and revoking are the assignment's own
    screen's, through the domain (``CaseAssignmentAdmin``)."""

    model = CaseAssignment
    extra = 0
    can_delete = False
    show_change_link = True
    fields = (
        "assignee",
        "role",
        "organisation",
        "authorisation_reference",
        "authorisation_valid_until",
        "assigned_at",
        "revoked_at",
    )
    readonly_fields = fields

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


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
    readonly_fields = (
        "reference",
        "uuid",
        "person",
        "status",
        "status_since",
        "previous_status",
        "suspension_reason",
        "closed_at",
        "created_at",
    )
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

    def has_add_permission(self, request) -> bool:
        # ``services.open_case`` opens a file: it audits the opening and tells the person. A row added here would do
        # neither — and its owner, read-only above, could not even be set.
        return False

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
    """
    Granting and ending an assignment, through the domain (sec-f7 REVIEW, finding 2).

    The add form grants with ``services.assign``. A live assignment's screen offers one thing, and only to an account
    the assignment's own policy lets change it (``cases.policies.assignment_policy``: the administrator): its end,
    «revocato il», which ``services.revoke_assignment`` records at the moment it is saved — whatever was typed, the
    trail holds when the revocation was made. Nothing else is editable (``ASSIGNMENT_FIELDS``), and a revoked
    assignment's screen is read-only: an assignment is never revived, a new one is granted.
    """

    list_display = ("case", "assignee", "role", "authorisation_reference", "authorisation_valid_until", "revoked_at")
    list_filter = ("role",)
    search_fields = ("case__reference", "assignee__email", "authorisation_reference")
    autocomplete_fields = ("assignee", "case")
    fields = ASSIGNMENT_FIELDS

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ("assigned_at", "revoked_at")
        return tuple(name for name in ASSIGNMENT_FIELDS if name != "revoked_at")

    def has_change_permission(self, request, obj=None) -> bool:
        if not super().has_change_permission(request, obj):
            return False
        if obj is None:
            return True
        from accounts.permissions import can

        return obj.revoked_at is None and can(request.user, "change", obj)

    def save_model(self, request, obj, form, change) -> None:
        from cases import services

        if not change:
            granted = services.assign(
                obj.case,
                obj.assignee,
                role=obj.role,
                organisation=obj.organisation,
                authorisation_reference=obj.authorisation_reference,
                authorisation_jurisdiction=obj.authorisation_jurisdiction,
                authorisation_valid_until=obj.authorisation_valid_until,
                mandate_note=obj.mandate_note,
                actor=request.user,
                request=request,
            )
            # the admin logs and redirects with the row the domain wrote
            obj.pk, obj.assigned_at = granted.pk, granted.assigned_at
            obj._state.adding = False
            return
        if "revoked_at" in form.changed_data and obj.revoked_at is not None:
            services.revoke_assignment(CaseAssignment.objects.get(pk=obj.pk), actor=request.user, request=request)
        obj.refresh_from_db()
