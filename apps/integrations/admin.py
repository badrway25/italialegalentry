from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin, BaseTabularInline
from integrations.models import (
    ApiKey,
    ExternalReference,
    ExternalSystem,
    InboundWebhookLog,
    OutboundEvent,
    WebhookEndpoint,
)
from integrations.services import cancel_event, requeue_event


class WebhookEndpointInline(BaseTabularInline):
    model = WebhookEndpoint
    fields = ("url", "is_active", "event_types", "signing_secret_env", "last_delivery_at", "last_status_code")
    readonly_fields = ("last_delivery_at", "last_status_code")


@admin.register(ExternalSystem)
class ExternalSystemAdmin(BaseModelAdmin):
    list_display = ("key", "name", "is_active", "inbound_secret_env", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("key", "name")
    inlines = (WebhookEndpointInline,)
    fieldsets = (
        (None, {"fields": ("key", "name", "is_active", "note")}),
        (
            _("Webhook in ingresso — segreto condiviso"),
            {
                "description": _(
                    "Il segreto NON viene mai salvato nel database: indicare solo il nome della variabile "
                    "d'ambiente e, facoltativamente, l'impronta SHA-256 per verificare la configurazione."
                ),
                "fields": ("inbound_secret_env", "inbound_secret_hash"),
            },
        ),
    )


@admin.register(ExternalReference)
class ExternalReferenceAdmin(BaseModelAdmin):
    list_display = ("system", "content_type", "object_id", "external_id", "sync_status", "last_synced_at")
    list_filter = ("system", "sync_status", "content_type")
    search_fields = ("external_id", "object_id")
    readonly_fields = ("last_synced_at",)


@admin.register(OutboundEvent)
class OutboundEventAdmin(BaseModelAdmin):
    list_display = ("created_at", "event_type", "status", "system", "attempts", "next_attempt_at", "delivered_at")
    list_filter = ("status", "event_type", "system")
    search_fields = ("uuid", "idempotency_key", "object_id")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in OutboundEvent._meta.fields]
    actions = ("requeue", "cancel")

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Rimetti in coda (falliti/annullati)"))
    def requeue(self, request, queryset):
        for event in queryset:
            requeue_event(event)

    @admin.action(description=_("Annulla consegna"))
    def cancel(self, request, queryset):
        for event in queryset:
            cancel_event(event, reason=f"annullato dal back-office da {request.user}")


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(BaseModelAdmin):
    list_display = ("system", "url", "is_active", "last_delivery_at", "last_status_code")
    list_filter = ("is_active", "system")
    search_fields = ("url",)
    readonly_fields = ("last_delivery_at", "last_status_code", "last_error")


@admin.register(InboundWebhookLog)
class InboundWebhookLogAdmin(BaseModelAdmin):
    list_display = ("created_at", "system_key", "status_code", "signature_valid", "event_type", "error", "request_id")
    list_filter = ("signature_valid", "status_code", "system")
    search_fields = ("system_key", "nonce", "request_id", "event_type")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in InboundWebhookLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ApiKey)
class ApiKeyAdmin(BaseModelAdmin):
    list_display = ("name", "prefix", "system", "is_active", "scopes", "expires_at", "last_used_at", "created_by")
    list_filter = ("is_active", "system")
    search_fields = ("name", "prefix")
    readonly_fields = ("prefix", "key_hash", "last_used_at", "created_by")
    fieldsets = (
        (None, {"fields": ("name", "system", "scopes", "is_active", "expires_at")}),
        (
            _("Chiave (creata solo dal comando create_api_key; il valore non è recuperabile)"),
            {"fields": ("prefix", "key_hash", "last_used_at", "created_by")},
        ),
    )

    def has_add_permission(self, request):
        return False  # keys are created by `manage.py create_api_key`, which prints the value once
