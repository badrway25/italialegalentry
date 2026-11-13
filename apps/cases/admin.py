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

And since finding F-8, the back office reads and changes no more than the platform does
(``core.admin_base.PolicyBoundAdminMixin``). role:operator holds the «cases» model permissions for the
files it handles, and until F-8 it listed and opened EVERY file here. Every screen now reads its rows
through the domain's own answer — ``CaseFileQuerySet.readable_by`` (the owner, a LIVE assignee, the
administration), ``policies.readable_assignments`` — and asks the object policy before it lets a row
change. What the domain writes is read-only: the purpose and the pathway (the orientation writes them,
``cases.intake``), a checklist line's responsible actor once the line exists (an authority field,
PERMISSION_MODEL §6 rule 5). A line's status changes through ``services.set_checklist_status``, which
records ``case.checklist.status``. A CLOSED file is read-only for everybody (CASE_LIFECYCLE.md §4 rule 5),
a superuser included, and nobody acts on their own file here.
"""

from __future__ import annotations

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.permissions import can, require
from cases.models import CaseAssignment, CaseFile, ChecklistItem, ChecklistStatus, PathwayAssessment
from cases.policies import readable_assignments
from core.admin_base import PolicyBoundAdminMixin, with_frozen_account_fields

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


def readable_files(user):
    """The files ``user`` may read: the platform's own answer (``CaseFileQuerySet.readable_by``)."""
    return CaseFile.objects.readable_by(user)


class ChecklistLineForm(forms.ModelForm):
    """
    A line's responsible actor is set when the line is made, and never rewritten here.

    It decides who may tick the line — the person ticks the lines that are theirs to perform and no other
    (``cases.policies.checklist_policy``) — so it is an authority field (PERMISSION_MODEL §6 rule 5): changing it hands a
    capacity out, and no domain service records that. A disabled field keeps its stored value whatever is posted.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and "responsible_actor" in self.fields:
            self.fields["responsible_actor"].disabled = True


class ChecklistInline(admin.TabularInline):
    """
    The file's lines, editable only where the checklist policy lets the account change them — a live professional or
    operator assignee, the administration — on a file that is not CLOSED (§4 rule 5: for everybody, a superuser
    included), and never by the file's own owner: the back office is not where a person acts on their own file. The
    status moves through the domain (``CaseFileAdmin.save_checklist``).
    """

    model = ChecklistItem
    form = ChecklistLineForm
    extra = 0
    fields = ("order", "requirement", "status", "responsible_actor", "responsible_note", "due_date")
    ordering = ("order", "id")

    @staticmethod
    def may_change_lines(request, case) -> bool:
        return (
            case is not None
            and not case.is_read_only
            and case.person_id != request.user.id
            and can(request.user, "change", case)
        )

    def has_add_permission(self, request, obj=None) -> bool:
        return super().has_add_permission(request, obj) and (obj is None or self.may_change_lines(request, obj))

    def has_change_permission(self, request, obj=None) -> bool:
        return super().has_change_permission(request, obj) and (obj is None or self.may_change_lines(request, obj))

    def has_delete_permission(self, request, obj=None) -> bool:
        return super().has_delete_permission(request, obj) and (obj is None or self.may_change_lines(request, obj))


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

    def get_queryset(self, request):
        # the assignments the assignment policy lets this account read — not every assignment of a file it may read
        return readable_assignments(request.user, super().get_queryset(request))

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
class CaseFileAdmin(PolicyBoundAdminMixin, admin.ModelAdmin):
    object_policy = True
    list_display = ("reference", "person", "purpose", "status", "status_since", "open_items")
    list_filter = ("status", "purpose")
    search_fields = ("reference", "person__email", "pathway_key")
    readonly_fields = (
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

    def readable(self, request, queryset):
        return queryset.filter(pk__in=readable_files(request.user).values("pk"))

    def has_add_permission(self, request) -> bool:
        # ``services.open_case`` opens a file: it audits the opening and tells the person. A row added here would do
        # neither — and its owner, read-only above, could not even be set.
        return False

    def save_formset(self, request, form, formset, change):
        if formset.model is not ChecklistItem:
            return super().save_formset(request, form, formset, change)
        return self.save_checklist(request, formset)

    @staticmethod
    def save_checklist(request, formset) -> None:
        """
        Save the checklist inline the way the platform changes a line: its status through ``set_checklist_status``,
        which records ``case.checklist.status`` (who, which line, from what, to what) — one event per line that moved,
        each line judged by its own policy first. A new line is made PENDING and then moved by the domain, so no line
        reaches a status without its event. Every other field saves as the form posted it; the admin's own LogEntry
        (mirrored as «admin.change») records those.
        """
        from cases import services

        lines = formset.save(commit=False)
        for line in formset.deleted_objects:
            line.delete()
        changed = {line.pk: fields for line, fields in formset.changed_objects}
        for line in lines:
            requested = line.status
            if line.pk is None:
                line.status = ChecklistStatus.PENDING
                line.save()
            else:
                line.status = ChecklistItem.objects.filter(pk=line.pk).values_list("status", flat=True).get()
                others = [name for name in changed.get(line.pk, ()) if name != "status"]
                if others:
                    line.save(update_fields=[*others, "updated_at"])
            if requested != line.status:
                require(request.user, "change", line)
                services.set_checklist_status(line, requested, actor=request.user, request=request)
        formset.save_m2m()

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
class PathwayAssessmentAdmin(PolicyBoundAdminMixin, admin.ModelAdmin):
    """Read-only: an assessment is frozen evidence of what the engine decided and with which rules. Read where the
    file is read (``cases.policies.assessment_policy``: the owner, a live assignee, the administration)."""

    object_policy = True
    list_display = ("case", "assessed_at", "outcome", "pathway_key", "ruleset_version")
    list_filter = ("outcome", "purpose")
    search_fields = ("case__reference",)
    readonly_fields = [field.name for field in PathwayAssessment._meta.fields]

    def readable(self, request, queryset):
        return queryset.filter(case__in=readable_files(request.user).values("pk"))

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@admin.register(CaseAssignment)
class CaseAssignmentAdmin(PolicyBoundAdminMixin, admin.ModelAdmin):
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
    object_policy = True

    def readable(self, request, queryset):
        return readable_assignments(request.user, queryset)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            fields = ("assigned_at", "revoked_at")
        else:
            fields = tuple(name for name in ASSIGNMENT_FIELDS if name != "revoked_at")
        # no choice among accounts for an account that may not read them (F-8, review F8R-3)
        return tuple(with_frozen_account_fields(self, request, obj, fields))

    def has_change_permission(self, request, obj=None) -> bool:
        # the model permission and the assignment's own policy (``PolicyBoundAdminMixin``); and never a revoked one
        if not super().has_change_permission(request, obj):
            return False
        return obj is None or obj.revoked_at is None

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
