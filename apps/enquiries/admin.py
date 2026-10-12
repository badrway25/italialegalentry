"""
Back-office for public submissions.

Submission data is evidence: read-only. Staff edit only the workflow fields (status, notes,
external reference, handled/last-contact). Actions: CSV export (UTF-8 BOM, consent version and
timestamp), mark handled, anonymise (GDPR erasure), single-submission JSON export (portability).
"""

from __future__ import annotations

import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from core import gates
from core.admin_base import BaseModelAdmin
from enquiries import services
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest

WORKFLOW_FIELDS = ("status", "admin_notes", "external_reference", "handled_at", "handled_by", "last_contact_at")
META_FIELDS = (
    "consent",
    "language",
    "source_path",
    "owner",
    "ip_hash",
    "user_agent",
    "duplicate_hash",
    "anonymised_at",
    "created_at",
    "updated_at",
)


class PublicSubmissionAdmin(BaseModelAdmin):
    list_filter = ("status", "language")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    autocomplete_fields = ("handled_by",)
    list_per_page = 50
    actions = ("export_csv", "mark_handled", "anonymise_selected", "export_json_single")

    def has_add_permission(self, request):
        return False  # submissions only come from the public forms

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj))
        data = [f.name for f in self.model._meta.fields if f.name not in WORKFLOW_FIELDS and f.name != "id"]
        return tuple(dict.fromkeys([*data, *base]))

    def get_fieldsets(self, request, obj=None):
        return (
            (_("Traitement"), {"fields": WORKFLOW_FIELDS}),
            (_("Données transmises (lecture seule)"), {"fields": self.model.DATA_FIELDS}),
            (_("Consentement et métadonnées"), {"fields": META_FIELDS}),
        )

    def changelist_view(self, request, extra_context=None):
        if not gates.public_forms_enabled().open:
            messages.warning(request, _("Formulaires publics désactivés (gate G2 : pages légales non publiées)."))
        return super().changelist_view(request, extra_context)

    # ---- actions ----------------------------------------------------------------------------

    @admin.action(description=_("Exporter en CSV (UTF-8, avec version et date du consentement)"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{self.model._meta.model_name}.csv"'
        response.write("﻿")  # BOM so that spreadsheet software opens UTF-8 correctly
        writer = csv.writer(response, delimiter=";", lineterminator="\r\n")
        writer.writerow(services.export_header(self.model))
        count = 0
        for obj in queryset.select_related("consent__consent_text", "handled_by"):
            writer.writerow(services.export_row(obj))
            count += 1
        audit_record(request, action="enquiries.export_csv", metadata={"model": self.model._meta.label, "count": count})
        return response

    @admin.action(description=_("Marquer comme traitée"))
    def mark_handled(self, request, queryset):
        handled = 0
        for obj in queryset:
            services.mark_handled(obj, request.user, request)
            handled += 1
        messages.success(request, _("%(n)d demande(s) marquée(s) comme traitée(s).") % {"n": handled})

    @admin.action(description=_("Anonymiser (effacement RGPD — irréversible)"))
    def anonymise_selected(self, request, queryset):
        done = 0
        for obj in queryset.filter(anonymised_at__isnull=True):
            services.anonymise(obj, request.user, request, reason="back-office action")
            done += 1
        messages.success(request, _("%(n)d demande(s) anonymisée(s).") % {"n": done})

    @admin.action(description=_("Exporter une demande en JSON (portabilité)"))
    def export_json_single(self, request, queryset):
        if queryset.count() != 1:
            messages.error(request, _("Sélectionnez exactement une demande pour l’export JSON."))
            return None
        obj = queryset.select_related("consent__consent_text").get()
        payload = services.export_json(obj)
        response = HttpResponse(payload, content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{self.model._meta.model_name}-{obj.pk}.json"'
        audit_record(request, action="enquiries.export_json", target=obj)
        return response


@admin.register(CompanyNeedsRequest)
class CompanyNeedsRequestAdmin(PublicSubmissionAdmin):
    list_display = ("created_at", "status", "company_name", "email", "language", "handled_at")
    search_fields = ("company_name", "email", "contact_name_and_role", "sector", "headquarters", "external_reference")


@admin.register(CollaborationProposal)
class CollaborationProposalAdmin(PublicSubmissionAdmin):
    list_display = ("created_at", "status", "kind", "organisation_name", "email", "language", "handled_at")
    list_filter = ("status", "language", "kind")
    search_fields = ("organisation_name", "email", "contact_name_and_role", "country", "external_reference")


@admin.register(ContactRequest)
class ContactRequestAdmin(PublicSubmissionAdmin):
    list_display = ("created_at", "status", "subject", "email", "language", "handled_at")
    search_fields = ("subject", "email", "name", "external_reference")
