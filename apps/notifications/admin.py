from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from core.admin_base import BaseModelAdmin
from notifications.models import EmailOutbox, Notification, NotificationPreference, OutboxStatus


@admin.register(EmailOutbox)
class EmailOutboxAdmin(BaseModelAdmin):
    list_display = ("created_at", "status", "to_email", "subject", "reference", "attempts", "sent_at")
    list_filter = ("status",)
    search_fields = ("to_email", "subject", "reference")
    readonly_fields = (
        "to_email",
        "subject",
        "body_text",
        "body_html",
        "reply_to",
        "reference",
        "attempts",
        "last_error",
        "sent_at",
    )
    actions = ("resend", "cancel")

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Reinvia (rimette in coda)"))
    def resend(self, request, queryset):
        queryset.exclude(status=OutboxStatus.SENT).update(status=OutboxStatus.QUEUED, attempts=0, last_error="")

    @admin.action(description=_("Annulla invio"))
    def cancel(self, request, queryset):
        queryset.filter(status__in=[OutboxStatus.QUEUED, OutboxStatus.FAILED]).update(status=OutboxStatus.CANCELLED)


@admin.register(Notification)
class NotificationAdmin(BaseModelAdmin):
    """
    Read-only by design. A notification is the record that somebody was told something; editing one
    after the fact turns the record into a claim, and the team's own screens are exactly where that
    temptation would arrive. Resending is a new notification, not a corrected old one.
    """

    list_display = ("created_at", "event", "category", "channel", "recipient", "email_suppressed")
    list_filter = ("event", "category", "channel", "email_suppressed")
    search_fields = ("dedupe_key", "recipient__email")
    autocomplete_fields = ("recipient",)
    readonly_fields = (
        "message",
        "recipient",
        "event",
        "category",
        "channel",
        "dedupe_key",
        "outbox",
        "email_suppressed",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # Deletion is reachable, because removing a communication cascades here and Django refuses the
    # parent deletion otherwise. It is never silent: the row disappears, the audit entry does not.
    def _audit_deleted(self, request, obj) -> None:
        audit_record(
            request,
            action="notifications.notification.deleted",
            target=obj,
            metadata={"event": obj.event, "category": obj.category, "channel": obj.channel},
        )

    def delete_model(self, request, obj):
        self._audit_deleted(request, obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self._audit_deleted(request, obj)
        super().delete_queryset(request, queryset)


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(BaseModelAdmin):
    list_display = ("user", "email_case", "email_deadline", "email_document", "email_message", "email_assignment")
    list_filter = ("email_case", "email_deadline", "email_document", "email_message", "email_assignment")
    search_fields = ("user__email",)
    autocomplete_fields = ("user",)
