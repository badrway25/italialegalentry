from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from consents.models import ConsentRecord, ConsentText, NewsletterSubscription
from core.admin_base import BaseModelAdmin


@admin.register(ConsentText)
class ConsentTextAdmin(BaseModelAdmin):
    list_display = ("purpose", "language", "version", "is_current", "locked_key", "effective_from")
    list_filter = ("purpose", "language", "is_current")
    search_fields = ("text",)
    readonly_fields = ("locked_key", "source")

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.locked_key:
            fields.append("text")  # prescribed wording is not editable in the back-office
        return fields

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentRecord)
class ConsentRecordAdmin(BaseModelAdmin):
    list_display = ("given_at", "purpose", "email", "consent_text", "language", "withdrawn_at")
    list_filter = ("purpose", "language")
    search_fields = ("email",)
    date_hierarchy = "given_at"
    readonly_fields = ("purpose", "consent_text", "email", "user", "given_at", "ip_hash", "user_agent", "language")
    actions = ("withdraw_selected",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description=_("Registra la revoca del consenso"))
    def withdraw_selected(self, request, queryset):
        from consents.services import withdraw

        for record in queryset.filter(withdrawn_at__isnull=True):
            withdraw(record, note=f"revoca registrata dal back-office da {request.user}")


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(BaseModelAdmin):
    list_display = ("email", "language", "confirmed_at", "unsubscribed_at", "created_at")
    list_filter = ("language",)
    search_fields = ("email",)
    readonly_fields = ("consent", "confirm_token", "unsubscribe_token", "confirmed_at", "unsubscribed_at")

    def has_add_permission(self, request):
        return False
