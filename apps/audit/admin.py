"""
Back-office of the audit trail — read-only for everybody (AUDIT_MODEL §6.1).

The administration reads it whole. role:legal_approver holds «audit: view» to read the trail of what it reviews — the
legal rules and their sources — and until F-8 it read every event: every sign-in, every file's events, the e-mail
addresses in ``actor_label``, the file names in ``target_repr`` (AUDIT_MODEL §6.1: «tutti gli altri ruoli: nessun
accesso»). Any account other than the administration reads the rules' trail only.
"""

from django.contrib import admin

from audit.models import AuditEvent
from core.admin_base import BaseModelAdmin, PolicyBoundAdminMixin

#: The rules' trail: ``audit.services.record`` names a target by its class, the admin's own log by its model's name.
RULE_TRAIL = ("LegalRule", "LegalSource", "legalrule", "legalsource")


@admin.register(AuditEvent)
class AuditEventAdmin(PolicyBoundAdminMixin, BaseModelAdmin):
    list_display = ("created_at", "action", "actor_label", "target_type", "target_repr", "request_id")
    list_filter = ("action", "target_type")
    search_fields = ("actor_label", "target_repr", "action", "request_id")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in AuditEvent._meta.fields]

    def readable(self, request, queryset):
        from accounts import roles

        if roles.is_superadmin(request.user) or roles.has_role(request.user, roles.ADMINISTRATOR):
            return queryset
        return queryset.filter(target_type__in=RULE_TRAIL)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
