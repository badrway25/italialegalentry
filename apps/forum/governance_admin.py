"""
Back-office of the Forum Permanent governance module.

This file exists because of one line in the specification. REQ-CFG-03 (FORUM_GOVERNANCE §3): «queste
cinque righe sono dati di seed, non costanti nel codice. Aggiungere una sesta commissione è
un'operazione di back-office.» A claim like that is only true if there is a screen where the
operation can be performed, so here it is.

Three rules this back-office keeps:

* **A state is never edited as a field.** ``ForumProposal.status`` and ``ForumProject.status`` are
  read-only here, exactly as they are in the views: the state moves through
  ``governance_services.transition_*``, which checks the declared table and writes the audit row.
  Making them editable would give the back-office a private lifecycle, and a private lifecycle is
  how an audit trail stops being complete.

* **A mandate is dated.** ``CommissionMember`` shows the window and whether the mandate is in force
  TODAY, because « is this person still on the commission » is the question the row exists to answer.

* **A participation profile shows no personal data**, in the back-office as everywhere else. There
  is nothing to hide: the model holds an organisation, a category and declared interests.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin, BaseTabularInline
from forum.governance import (
    AnnualReport,
    Commission,
    CommissionMember,
    ForumEdition,
    ForumProfile,
    ForumProject,
    ForumProposal,
    MonitoringEntry,
    ProjectMilestone,
    Table,
)

STATE_NOTE = _(
    "L’état se modifie par le cycle du Forum (dépôt, examen, décision), jamais directement : "
    "chaque changement est contrôlé et inscrit au journal d’audit."
)


class CommissionInline(BaseTabularInline):
    model = Commission
    fields = ("key", "name_fr", "status", "order")
    show_change_link = True


class CommissionMemberInline(BaseTabularInline):
    model = CommissionMember
    fields = ("profile", "role", "valid_from", "valid_until", "revoked_at", "mandate_reference")
    autocomplete_fields = ("profile",)


class TableInline(BaseTabularInline):
    model = Table
    fields = ("key", "title_fr", "status", "referent", "opened_on", "closed_on")
    show_change_link = True


class ProjectMilestoneInline(BaseTabularInline):
    model = ProjectMilestone
    fields = ("order", "title_fr", "responsible", "responsible_note", "due_on", "status")


class MonitoringEntryInline(BaseTabularInline):
    model = MonitoringEntry
    fields = ("period_start", "period_end", "indicators", "note_fr", "recorded_by")


@admin.register(ForumEdition)
class ForumEditionAdmin(BaseModelAdmin):
    list_display = ("title_fr", "year", "city", "status", "commission_count")
    list_filter = ("status", "year")
    search_fields = ("key", "title_fr", "city")
    inlines = (CommissionInline,)

    @admin.display(description=_("commissions"))
    def commission_count(self, obj: ForumEdition) -> int:
        return obj.commissions.count()


@admin.register(Commission)
class CommissionAdmin(BaseModelAdmin):
    list_display = ("name_fr", "edition", "key", "status", "order", "live_member_count")
    list_filter = ("edition", "status")
    search_fields = ("key", "name_fr", "scope_fr")
    inlines = (TableInline, CommissionMemberInline)
    fieldsets = (
        (None, {"fields": ("edition", "key", "name_fr", "order", "status")}),
        (
            _("Champ et gouvernance"),
            {
                "fields": ("scope_fr", "governance_fr"),
                "description": str(
                    _(
                        "Une sixième commission s’ajoute ici, sans modification du code (REQ-CFG-03). "
                        "Ne jamais nommer de personne physique dans la gouvernance."
                    )
                ),
            },
        ),
    )

    @admin.display(description=_("membres en fonction"))
    def live_member_count(self, obj: Commission) -> int:
        return obj.members.live().count()


@admin.register(ForumProfile)
class ForumProfileAdmin(BaseModelAdmin):
    """No personal data is displayed because none is stored (FORUM_GOVERNANCE §5)."""

    list_display = ("display_label", "edition", "category", "role", "is_active", "joined_on")
    list_filter = ("edition", "category", "role", "is_active")
    search_fields = ("organisation_label", "declared_interests")
    autocomplete_fields = ("user", "organisation")

    @admin.display(description=_("organisation"))
    def display_label(self, obj: ForumProfile) -> str:
        return obj.display_label


@admin.register(CommissionMember)
class CommissionMemberAdmin(BaseModelAdmin):
    list_display = ("profile", "commission", "role", "valid_from", "valid_until", "in_force")
    list_filter = ("commission", "role")
    search_fields = ("profile__organisation_label", "mandate_reference")
    autocomplete_fields = ("commission", "profile")

    @admin.display(boolean=True, description=_("en vigueur aujourd’hui"))
    def in_force(self, obj: CommissionMember) -> bool:
        return obj.is_live


@admin.register(Table)
class TableAdmin(BaseModelAdmin):
    list_display = ("title_fr", "commission", "status", "opened_on", "closed_on")
    list_filter = ("commission", "status")
    search_fields = ("key", "title_fr", "topic_fr")
    autocomplete_fields = ("commission", "referent")


@admin.register(ForumProposal)
class ForumProposalAdmin(BaseModelAdmin):
    list_display = ("reference", "title_fr", "commission", "status", "status_since")
    list_filter = ("commission", "status")
    search_fields = ("reference", "title_fr", "body_fr")
    autocomplete_fields = ("commission", "table", "proposer")
    readonly_fields = ("reference", "uuid", "status", "status_since", "previous_status", "decided_at")
    fieldsets = (
        (None, {"fields": ("reference", "uuid", "proposer", "commission", "table")}),
        (_("Texte"), {"fields": ("title_fr", "body_fr")}),
        (
            _("Cycle"),
            {
                "fields": ("status", "status_since", "previous_status", "decision_note_fr", "decided_at"),
                "description": str(STATE_NOTE),
            },
        ),
    )


@admin.register(ForumProject)
class ForumProjectAdmin(BaseModelAdmin):
    list_display = ("title_fr", "commission", "lead", "status", "status_since")
    list_filter = ("commission", "status")
    search_fields = ("title_fr", "summary_fr", "partners_fr")
    autocomplete_fields = ("commission", "lead", "origin")
    readonly_fields = ("uuid", "status", "status_since", "previous_status")
    inlines = (ProjectMilestoneInline, MonitoringEntryInline)
    fieldsets = (
        (None, {"fields": ("uuid", "origin", "commission", "title_fr", "summary_fr")}),
        (_("Responsabilité"), {"fields": ("lead", "partners_fr")}),
        (
            _("Cycle"),
            {"fields": ("status", "status_since", "previous_status", "started_on", "ends_on"),
             "description": str(STATE_NOTE)},
        ),
    )


@admin.register(AnnualReport)
class AnnualReportAdmin(BaseModelAdmin):
    """
    The relation is assembled, not written: ``sections`` is ``editable=False`` and never appears in
    a form. What the back-office does here is publish it — and publishing freezes it.
    """

    list_display = ("edition", "status", "generated_at", "published_at", "section_count")
    list_filter = ("status",)
    readonly_fields = ("generated_at", "generated_by", "published_at")

    @admin.display(description=_("sections assemblées"))
    def section_count(self, obj: AnnualReport) -> int:
        return len(obj.sections or [])
