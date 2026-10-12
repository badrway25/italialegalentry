from django.contrib import admin

from audit.models import AuditEvent
from core.admin_base import BaseModelAdmin


@admin.register(AuditEvent)
class AuditEventAdmin(BaseModelAdmin):
    list_display = ("created_at", "action", "actor_label", "target_type", "target_repr", "request_id")
    list_filter = ("action", "target_type")
    search_fields = ("actor_label", "target_repr", "action", "request_id")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in AuditEvent._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
