"""
Read-only back-office listing of private documents. No file link for non-superusers; scan status
can be set manually (audited) by users holding the change permission — the default scanner is a
no-op, so a documented human review is the way a document becomes 'clean' in this deployment.

The rows are those ``documents.policies`` lets the account read (finding F-8): for the administration
every document that is not deleted — a deleted document is nobody's to read, and a superuser stays the
last resort. The register's export is recorded in the audit trail. The model has no file field: a file
leaves only through ``documents.views._serve`` (the policy, the delivery rule, the throttle, the audit
event), the one link drawn here.
"""

from __future__ import annotations

import csv

from django.contrib import admin
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts import roles
from audit.services import record as audit_record
from core.admin_base import BaseModelAdmin, BaseTabularInline, PolicyBoundAdminMixin
from documents import services
from documents.models import (
    DocumentRequirement,
    DocumentVersion,
    PrivateDocument,
    RequirementState,
    ScanStatus,
)

ALL_FIELDS = (
    "id",
    "owner",
    "organisation",
    "kind",
    "original_name",
    "stored_name",
    "content_type",
    "size",
    "sha256",
    "description",
    "scan_status",
    "scanned_at",
    "retention_until",
    "uploaded_ip_hash",
    "deleted_at",
    "file_removed_at",
    "created_at",
    "updated_at",
)


class DeletedFilter(admin.SimpleListFilter):
    title = _("supprimé")
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (("no", _("actifs")), ("yes", _("supprimés")))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.deleted()
        if self.value() == "no":
            return queryset.alive()
        return queryset


@admin.register(PrivateDocument)
class PrivateDocumentAdmin(PolicyBoundAdminMixin, BaseModelAdmin):
    object_policy = True
    list_display = (
        "original_name",
        "owner",
        "organisation",
        "kind",
        "scan_status",
        "size_display",
        "created_at",
        "deleted_at",
    )
    list_filter = ("scan_status", "kind", DeletedFilter)
    search_fields = ("original_name", "owner__email", "sha256", "id")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ALL_FIELDS
    autocomplete_fields = ()
    actions = ("mark_clean", "mark_infected", "export_csv")
    fieldsets = (
        (None, {"fields": ("id", "owner", "organisation", "kind", "original_name", "description")}),
        (_("Fichier"), {"fields": ("stored_name", "content_type", "size", "sha256", "file_removed_at")}),
        (_("Analyse et conservation"), {"fields": ("scan_status", "scanned_at", "retention_until", "deleted_at")}),
        (_("Audit"), {"fields": ("uploaded_ip_hash", "created_at", "updated_at")}),
    )

    def readable(self, request, queryset):
        return queryset if roles.is_superadmin(request.user) else queryset.alive()

    @admin.display(description=_("taille"), ordering="size")
    def size_display(self, obj):
        return filesizeformat(obj.size)

    @admin.display(description=_("téléchargement"))
    def download_link(self, obj):
        """
        A link only where the delivery would actually succeed.

        ``documents.views._serve`` refuses an unscanned file to anybody but its depositor, so on an
        installation with no scanner a link here answered 403 for every file but the administrator's
        own. The same rule is consulted (``services.delivery_block``) and the reason is printed
        instead — with the action that resolves it, which is the manual review below.
        """
        from documents.requirements import delivery_rule

        # ``None`` deliberately: a ModelAdmin is a singleton shared by every worker thread, so the
        # viewing account cannot be stashed on it. Asking the rule as "somebody who is not the
        # depositor" is the conservative reading and the right one here — the back-office is never
        # the place where a person fetches their own file.
        blocked = services.delivery_block(obj, None)
        if blocked:
            return delivery_rule(blocked) or "—"
        return format_html('<a href="{}">{}</a>', reverse("documents:download", args=[obj.pk]), _("Télécharger"))

    def get_list_display(self, request):
        display = list(super().get_list_display(request))
        if request.user.is_superuser:
            display.append("download_link")
        return display

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if request.user.is_superuser and "download_link" not in fields:
            fields.append("download_link")
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if request.user.is_superuser:
            fieldsets.append((_("Accès superutilisateur"), {"fields": ("download_link",)}))
        return fieldsets

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description=_("Marquer comme sain (revue manuelle)"), permissions=["change"])
    def mark_clean(self, request, queryset):
        count = 0
        for doc in queryset.alive().exclude(scan_status=ScanStatus.INFECTED):
            services.apply_scan_result(doc, ScanStatus.CLEAN, request=request, note="manual review (admin)")
            count += 1
        self.message_user(request, _("%(count)d document(s) marqué(s) comme sains.") % {"count": count})

    @admin.action(description=_("Marquer comme infecté (fichier supprimé)"), permissions=["change"])
    def mark_infected(self, request, queryset):
        count = 0
        for doc in queryset.exclude(scan_status=ScanStatus.INFECTED):
            services.apply_scan_result(doc, ScanStatus.INFECTED, request=request, note="manual review (admin)")
            count += 1
        self.message_user(request, _("%(count)d document(s) marqué(s) comme infectés.") % {"count": count})

    @admin.action(description=_("Exporter la liste (CSV, métadonnées uniquement)"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="private_documents.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ["id", "owner", "organisation", "kind", "original_name", "size", "scan_status", "created_at", "deleted_at"]
        )
        # a register of people's documents leaves the platform: recorded, like the enquiries' exports
        audit_record(request, action="documents.exported", metadata={"count": queryset.count()})
        for doc in queryset.select_related("owner", "organisation"):
            writer.writerow(
                [
                    doc.pk,
                    doc.owner.email,
                    doc.organisation.name if doc.organisation_id else "",
                    doc.kind,
                    doc.original_name,
                    doc.size,
                    doc.scan_status,
                    doc.created_at.isoformat(),
                    doc.deleted_at.isoformat() if doc.deleted_at else "",
                ]
            )
        return response


class RequirementStateFilter(admin.SimpleListFilter):
    title = _("état visible")
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return RequirementState.choices

    def queryset(self, request, queryset):
        value = self.value()
        return queryset.filter(state=value) if value else queryset


class DocumentVersionInline(BaseTabularInline):
    """The history, inside the row it belongs to. Read-only: a version is evidence, not a draft."""

    model = DocumentVersion
    fields = ("number", "document", "filed_by", "is_current", "expires_on", "decision", "decision_note", "created_at")
    readonly_fields = fields
    ordering = ("-number",)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DocumentRequirement)
class DocumentRequirementAdmin(PolicyBoundAdminMixin, BaseModelAdmin):
    """
    Back-office view of what each case file still needs.

    The ``state`` column is the CACHED derivation (``documents_refresh_requirements`` reconciles it
    and audits every move); it is read-only here because a state is derived from the evidence, and
    an administrator who could type one would be recording a conclusion nobody reached.
    """

    list_display = ("title", "case", "state", "responsible_actor", "due_date", "access_class", "updated_at")
    list_filter = (RequirementStateFilter, "responsible_actor", "access_class", "mandatory", "kind")
    search_fields = ("title", "code", "case__reference")
    date_hierarchy = "created_at"
    ordering = ("case", "order")
    inlines = (DocumentVersionInline,)
    readonly_fields = ("id", "state", "state_note", "replacement_requested_at", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("id", "case", "checklist_item", "code", "order", "title", "detail", "kind")}),
        (_("Responsabilité"), {"fields": ("responsible_actor", "responsible_note", "mandatory", "due_date")}),
        (_("Source"), {"fields": ("source_title", "source_ref", "source_url")}),
        (
            _("État (dérivé — non modifiable)"),
            {"fields": ("state", "state_note", "replacement_requested_at", "replacement_reason")},
        ),
        (_("Accès et audit"), {"fields": ("access_class", "created_at", "updated_at")}),
    )
    actions = ("refresh_states",)
    object_policy = True

    def readable(self, request, queryset):
        # what the requirement's own queryset gives the account (the person, a live assignee, the administration)
        return queryset.filter(pk__in=DocumentRequirement.objects.readable_by(request.user).values("pk"))

    @admin.action(description=_("Recalculer l’état (expiration, examen)"), permissions=["change"])
    def refresh_states(self, request, queryset):
        moved = 0
        for requirement in queryset.select_related("case").prefetch_related("versions"):
            before = requirement.state
            if services.refresh_state(requirement, request=request, actor=request.user) != before:
                moved += 1
        self.message_user(request, _("%(n)d pièce(s) ont changé d’état.") % {"n": moved})

    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
