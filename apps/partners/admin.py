import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from cms.admin import PUBLICATION_FIELDSET, PublishableAdminMixin
from core.admin_base import BaseModelAdmin, BaseTabularInline
from partners.models import Partner, PartnerTranslation


class PartnerTranslationInline(BaseTabularInline):
    model = PartnerTranslation
    fields = ("language", "description", "status", "source", "reviewed_by")
    autocomplete_fields = ("reviewed_by",)


@admin.register(Partner)
class PartnerAdmin(PublishableAdminMixin, BaseModelAdmin):
    list_display = ("name", "kind", "authorized", "status", "has_logo", "country", "city", "order", "updated_at")
    list_filter = ("kind", "authorized", "status")
    list_editable = ("order",)
    search_fields = ("name", "city", "country", "authorization_reference")
    autocomplete_fields = ("logo",)
    inlines = (PartnerTranslationInline,)
    actions = ("export_csv",)
    fieldsets = (
        (None, {"fields": ("name", "kind", "country", "city", "website", "description_fr", "order")}),
        (
            _("Autorizzazione alla pubblicazione (gate G6)"),
            {
                "description": _(
                    "ATTENZIONE: nome e logo di un partner compaiono sul sito pubblico solo con autorizzazione "
                    "scritta. Non caricare loghi scaricati da internet né segnaposto. Compilare il riferimento "
                    "dell'autorizzazione (chi, quando) prima di attivare la casella."
                ),
                "fields": ("logo", "authorized", "authorization_reference", "authorized_at"),
            },
        ),
        PUBLICATION_FIELDSET,
    )
    readonly_fields = PublishableAdminMixin.readonly_fields + ("authorized_at",)

    @admin.display(boolean=True, description=_("logo"))
    def has_logo(self, obj) -> bool:
        return obj.logo_id is not None

    @admin.action(description=_("Esporta CSV (selezione)"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="partners.csv"'
        writer = csv.writer(response)
        writer.writerow(["name", "kind", "country", "city", "authorized", "authorization_reference", "status"])
        for p in queryset.order_by("kind", "order", "name"):
            writer.writerow([p.name, p.kind, p.country, p.city, p.authorized, p.authorization_reference, p.status])
        return response
