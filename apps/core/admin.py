from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin
from core.models import FeatureFlag, SiteSettings


@admin.register(FeatureFlag)
class FeatureFlagAdmin(BaseModelAdmin):
    list_display = ("key", "enabled", "enabled_from", "enabled_until", "note", "updated_at", "updated_by")
    list_editable = ("enabled",)
    search_fields = ("key", "note")
    list_filter = ("enabled",)
    readonly_fields = ("updated_by",)
    fieldsets = (
        (None, {"fields": ("key", "enabled", "note")}),
        (_("Finestra di attivazione (Europe/Rome)"), {"fields": ("enabled_from", "enabled_until")}),
        (_("Audit"), {"fields": ("updated_by", "created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        from audit.services import record

        record(
            request,
            action="feature_flag.changed",
            target=obj,
            metadata={"enabled": obj.enabled, "from": str(obj.enabled_from), "until": str(obj.enabled_until)},
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseModelAdmin):
    fieldsets = (
        (_("Identità"), {"fields": ("site_name", "promoter_name", "logo", "use_logo_image")}),
        (_("Contatti e versione"), {"fields": ("public_contact_email", "version_label", "content_verified_on")}),
        (_("Hosting (conferma richiesta dal documento §1.4)"), {"fields": ("hosting_provider", "hosting_location")}),
        (_("Area riservata"), {"fields": ("reserved_area_enabled",)}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
