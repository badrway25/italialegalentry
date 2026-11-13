"""
Back-office of the company workspace.

Deliberately restrained. The company's own work happens in the platform; what lives here is the
project side — reading a need, moving it through the states only the project may move, naming the
authorised actor answerable for it, and maintaining the two taxonomies.

Two things are not editable here and not merely hidden:

* ``status`` is read-only on the form. Every state change goes through ``companies.services``, so
  the declared transition table, the authorisation rule of CR-03 and the audit trail cannot be
  bypassed from the admin.
* ``NeedEvent`` is read-only everywhere. A history that can be edited is not a history.
"""

from __future__ import annotations

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from companies import services
from companies.models import (
    CompanyNeed,
    CompanyProfile,
    NeedAssignment,
    NeedEvent,
    NeedSkill,
    NeedStatus,
    Sector,
    Territory,
)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("label_fr", "label_it", "code", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("label_fr", "label_it", "code")
    prepopulated_fields = {"code": ("label_fr",)}


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ("label_fr", "label_it", "country", "code", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("country", "is_active")
    search_fields = ("label_fr", "label_it", "code")
    prepopulated_fields = {"code": ("label_fr",)}


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("legal_name", "sector", "city", "country", "verification_column", "need_count")
    list_filter = ("sector", "size", "country")
    search_fields = ("legal_name", "trade_name", "registration_number", "vat_number", "organisation__name")
    autocomplete_fields = ("organisation",)
    readonly_fields = ("verification_column",)

    @admin.display(description=_("vérification"))
    def verification_column(self, obj: CompanyProfile) -> str:
        # Read from accounts.AccountVerification — this app never decides a verification.
        return obj.verification_label

    @admin.display(description=_("besoins"))
    def need_count(self, obj: CompanyProfile) -> int:
        return obj.needs.count()


class NeedSkillInline(admin.TabularInline):
    model = NeedSkill
    extra = 0
    fields = ("label", "level", "note", "order")
    ordering = ("level", "order", "id")


class NeedAssignmentInline(admin.TabularInline):
    model = NeedAssignment
    extra = 0
    fields = (
        "assignee",
        "role",
        "organisation",
        "authorisation_reference",
        "authorisation_jurisdiction",
        "authorisation_valid_until",
        "revoked_at",
    )
    autocomplete_fields = ("assignee", "organisation")


class NeedEventInline(admin.TabularInline):
    model = NeedEvent
    extra = 0
    can_delete = False
    fields = ("created_at", "from_status", "to_status", "note", "responsible_label")
    readonly_fields = fields
    ordering = ("created_at",)

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(CompanyNeed)
class CompanyNeedAdmin(admin.ModelAdmin):
    list_display = ("reference", "title", "company", "territory", "sector", "headcount", "status", "status_since")
    list_filter = ("status", "territory", "sector", "engagement_type")
    search_fields = ("reference", "title", "professional_profile", "company__legal_name")
    autocomplete_fields = ("company", "territory", "sector")
    readonly_fields = ("reference", "status", "status_since", "submitted_at", "closed_at")
    inlines = (NeedSkillInline, NeedAssignmentInline, NeedEventInline)
    actions = ("action_take_under_review", "action_take_in_charge", "action_close")

    def _bulk_transition(self, request, queryset, target: str, note: str) -> None:
        moved, refused = 0, 0
        for need in queryset:
            try:
                services.transition(need, target, actor=request.user, note=note, request=request)
            except ValidationError:
                refused += 1
            else:
                moved += 1
        if moved:
            self.message_user(
                request,
                ngettext("%(n)d besoin déplacé.", "%(n)d besoins déplacés.", moved) % {"n": moved},
                messages.SUCCESS,
            )
        if refused:
            self.message_user(
                request,
                ngettext(
                    "%(n)d besoin refusé par le domaine (transition non déclarée ou condition manquante).",
                    "%(n)d besoins refusés par le domaine (transition non déclarée ou condition manquante).",
                    refused,
                )
                % {"n": refused},
                messages.WARNING,
            )

    @admin.action(description=_("Mettre à l’examen"))
    def action_take_under_review(self, request, queryset) -> None:
        self._bulk_transition(request, queryset, NeedStatus.UNDER_REVIEW, str(_("Examen ouvert par l’équipe.")))

    @admin.action(description=_("Prendre en charge (exige un acteur autorisé valide)"))
    def action_take_in_charge(self, request, queryset) -> None:
        """
        Refused by the domain for every need without a live, referenced authorisation (CR-03).

        The action exists so the rule is visible where the work happens: a need that cannot be
        taken in charge says so here, instead of being moved by hand in a form.
        """
        self._bulk_transition(request, queryset, NeedStatus.IN_PROGRESS, str(_("Prise en charge ouverte.")))

    @admin.action(description=_("Clore"))
    def action_close(self, request, queryset) -> None:
        self._bulk_transition(request, queryset, NeedStatus.CLOSED, str(_("Clos par l’équipe.")))


@admin.register(NeedEvent)
class NeedEventAdmin(admin.ModelAdmin):
    list_display = ("need", "from_status", "to_status", "responsible_label", "created_at")
    list_filter = ("to_status",)
    search_fields = ("need__reference",)
    readonly_fields = ("need", "from_status", "to_status", "note", "responsible_label")

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
