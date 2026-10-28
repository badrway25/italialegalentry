"""
Back-office of notifications and the e-mail outbox.

Who (finding F-8): a notification's content is a portal ``Message`` — read, in the back office, by the roles
``portal.policies`` names (staff, administration) — so every screen here opens to those roles alone, whatever else
holds the «notifications» model permissions (role:operator read every person's messages here). The outbox's bodies
copy a message, a public submission or a newsletter confirmation, whose link carries the subscriber's bearer token:
they are shown to an account that may change the outbox (the administration), and a view grant reads the delivery
record only. A view grant never writes: resending and cancelling need «change», and each is recorded.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from core.admin_base import BaseModelAdmin, PolicyBoundAdminMixin
from notifications.models import EmailOutbox, Notification, NotificationPreference, OutboxStatus
from portal.policies import BACKOFFICE_VIEW_ROLES

#: The fields that carry what was written to the person: shown to an account that may change the outbox only.
BODY_FIELDS = ("body_text", "body_html")


class MessageReaders(PolicyBoundAdminMixin):
    """The screen opens to the roles that read the team's messages in the back office (``portal.policies``)."""

    policy_roles = BACKOFFICE_VIEW_ROLES


@admin.register(EmailOutbox)
class EmailOutboxAdmin(MessageReaders, BaseModelAdmin):
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

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if self.has_change_permission(request, obj):
            return fields
        return [name for name in fields if name not in BODY_FIELDS]

    def hidden_fields(self, request):
        # A body hidden from the page is no filter of the list either (F8R-2: ``?body_text__contains=`` read it).
        if request is not None and self.has_change_permission(request):
            return frozenset()
        return frozenset(BODY_FIELDS)

    @admin.action(description=_("Reinvia (rimette in coda)"), permissions=["change"])
    def resend(self, request, queryset):
        for item in queryset.exclude(status=OutboxStatus.SENT):
            item.status, item.attempts, item.last_error = OutboxStatus.QUEUED, 0, ""
            item.save(update_fields=["status", "attempts", "last_error", "updated_at"])
            audit_record(request, action="notifications.outbox.resent", target=item)

    @admin.action(description=_("Annulla invio"), permissions=["change"])
    def cancel(self, request, queryset):
        for item in queryset.filter(status__in=[OutboxStatus.QUEUED, OutboxStatus.FAILED]):
            item.status = OutboxStatus.CANCELLED
            item.save(update_fields=["status", "updated_at"])
            audit_record(request, action="notifications.outbox.cancelled", target=item)


@admin.register(Notification)
class NotificationAdmin(MessageReaders, BaseModelAdmin):
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
class NotificationPreferenceAdmin(MessageReaders, BaseModelAdmin):
    list_display = ("user", "email_case", "email_deadline", "email_document", "email_message", "email_assignment")
    list_filter = ("email_case", "email_deadline", "email_document", "email_message", "email_assignment")
    search_fields = ("user__email",)
    autocomplete_fields = ("user",)
