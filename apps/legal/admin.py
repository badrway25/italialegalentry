from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin, BaseTabularInline
from legal.models import LegalDocument, LegalDocumentVersion, LegalStatus
from legal.services import invalidate, publish, unpublish


class LegalDocumentVersionInline(BaseTabularInline):
    model = LegalDocumentVersion
    fields = ("version", "published_at", "published_by", "checksum")
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(LegalDocument)
class LegalDocumentAdmin(BaseModelAdmin):
    list_display = ("kind", "status", "version", "effective_date", "published_at", "courtesy_fr_enabled", "updated_at")
    list_filter = ("status",)
    readonly_fields = ("status", "version", "checksum", "published_at", "published_by", "slug")
    fieldsets = (
        (None, {"fields": ("kind", "slug", "status", "version", "checksum")}),
        (
            _("Testo ufficiale italiano — Allegato 1 (copiare integralmente, nessuna riformulazione)"),
            {"fields": ("title_it", "body_it", "source_reference", "effective_date", "last_reviewed_at")},
        ),
        (_("Traduzione di cortesia (FR) — solo su conferma scritta"), {"fields": ("courtesy_fr_enabled",)}),
        (_("Pubblicazione"), {"fields": ("published_at", "published_by")}),
    )
    inlines = (LegalDocumentVersionInline,)
    actions = ("publish_official", "unpublish_official")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if obj.status == LegalStatus.BLOCKED and obj.body_it.strip():
            obj.status = LegalStatus.DRAFT
        super().save_model(request, obj, form, change)
        invalidate()
        if obj.status != LegalStatus.PUBLISHED:
            messages.warning(
                request,
                _("Il testo è salvato come bozza: usare l’azione «Pubblica testo ufficiale» per renderlo pubblico."),
            )

    @admin.action(description=_("Pubblica testo ufficiale (richiede permesso dedicato)"))
    def publish_official(self, request, queryset):
        for doc in queryset:
            try:
                publish(doc, request.user, request)
                messages.success(
                    request, _("%(doc)s pubblicato (v%(v)s).") % {"doc": doc.get_kind_display(), "v": doc.version}
                )
            except PermissionDenied:
                messages.error(request, _("Permesso negato: solo utenti autorizzati possono pubblicare testi legali."))
            except ValidationError as exc:
                messages.error(request, "; ".join(exc.messages))

    @admin.action(description=_("Ritira dalla pubblicazione"))
    def unpublish_official(self, request, queryset):
        for doc in queryset:
            try:
                unpublish(doc, request.user, request)
            except PermissionDenied:
                messages.error(request, _("Permesso negato."))
