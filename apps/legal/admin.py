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
    list_display = (
        "kind",
        "category",
        "status",
        "version",
        "open_fields_count",
        "translation_status",
        "effective_date",
        "published_at",
        "updated_at",
    )
    list_filter = ("status", "translation_status")
    readonly_fields = ("status", "version", "checksum", "published_at", "published_by", "slug", "open_fields_list")
    fieldsets = (
        (None, {"fields": ("kind", "slug", "status", "version", "checksum")}),
        (
            _("Testo ufficiale italiano — Allegato 1 (copiare integralmente, nessuna riformulazione)"),
            {"fields": ("title_it", "body_it", "source_reference", "effective_date", "last_reviewed_at")},
        ),
        (_("Traduzione di cortesia (FR) — solo su conferma scritta"), {"fields": ("courtesy_fr_enabled",)}),
        (
            "Informativa privacy e cookie (V5.14) — traduzioni di cortesia FR/EN/AR, il testo italiano prevale",
            {"fields": ("open_fields_list", "translation_status", "translations")},
        ),
        (_("Pubblicazione"), {"fields": ("published_at", "published_by")}),
    )
    inlines = (LegalDocumentVersionInline,)
    actions = ("publish_official", "unpublish_official")

    def has_add_permission(self, request):
        return False

    @admin.display(description="categoria (V5.14)")
    def category(self, obj):
        return obj.category

    @admin.display(description="campi da completare")
    def open_fields_count(self, obj):
        return len(obj.open_field_ids())

    @admin.display(description="campi da completare (la produzione rifiuta di pubblicare finché ne resta uno)")
    def open_fields_list(self, obj):
        return " · ".join(f"{label}: {', '.join(ids)}" for label, ids in obj.open_field_classes()) or "—"

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if obj.status == LegalStatus.BLOCKED and obj.body_it.strip():
            obj.status = LegalStatus.DRAFT
        was_published = bool(obj.pk) and LegalDocument.objects.filter(pk=obj.pk, status=LegalStatus.PUBLISHED).exists()
        super().save_model(request, obj, form, change)
        invalidate()
        if was_published and obj.status != LegalStatus.PUBLISHED:
            # LegalDocument.save: a change to a published text takes it offline until publish() (V5.14 review).
            # Plain Italian, like the rest of the back office's legal screens: no new catalogue message.
            messages.warning(
                request,
                "Il testo pubblicato è stato modificato: è tornato in bozza e non è più visibile online. "
                "Usare l’azione «Pubblica testo ufficiale» per pubblicare la nuova versione.",
            )
        elif obj.status != LegalStatus.PUBLISHED:
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
