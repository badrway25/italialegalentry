"""
Back-office of the digital help desk — deliberately incomplete.

An administrator configures the platform; they do not read people's legal questions. So this admin
shows the **shape** of a request (reference, state, origin, mandate, dates) and never its content:
``question`` is not in the form, ``TicketMessage`` is not registered, and nothing here can write a
reply. Everything is read-only, because every act that matters has a service that audits it, and an
act performed by editing a row in a table is an act with no author and no reason.

This is the opposite of the previous platform, whose entire administration page was one field — the
API key of the language model that answered the questions.
"""

from django.contrib import admin

from helpdesk.models import HelpdeskTicket


@admin.register(HelpdeskTicket)
class HelpdeskTicketAdmin(admin.ModelAdmin):
    list_display = ("reference", "status", "origin", "created_at", "assignee", "mandate_valid_until")
    list_filter = ("status", "origin")
    search_fields = ("reference",)  # never the question: an admin search must not be a content search
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    fields = (
        "reference",
        "status",
        "status_since",
        "origin",
        "case",
        "assignee",
        "assignee_role_label",
        "mandate_note",
        "mandate_valid_until",
        "assigned_at",
        "assignment_revoked_at",
        "closed_at",
    )

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def has_add_permission(self, request) -> bool:
        # A request is opened by the person or by the rule engine, never by an administrator.
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        # The record of what was asked and what was answered is not an administrator's to erase.
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("case", "assignee")
