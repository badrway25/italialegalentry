"""
Back-office of authorised selection.

The admin is an ADMINISTRATION tool, never the user interface of an actor: the actor works in
``selection/workspace.html``. What administrators do here is register an authorisation, entitle the
accounts that may work under it, and issue a mandate — the three acts that create the chain. They
do NOT advance a process from here: a stage change must name the authorised actor that performed
it, and an administrator is not that actor.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin, BaseTabularInline
from selection.models import (
    ActorOperator,
    AuthorizedActor,
    IdentityAccess,
    IdentityDisclosure,
    SelectionEvidence,
    SelectionMandate,
    SelectionProcess,
    SelectionStageEvent,
)


class ActorOperatorInline(BaseTabularInline):
    model = ActorOperator
    extra = 0
    fields = ("user", "function_note", "added_at", "revoked_at")
    autocomplete_fields = ("user",)


@admin.register(AuthorizedActor)
class AuthorizedActorAdmin(BaseModelAdmin):
    list_display = ("organisation", "actor_type", "jurisdiction", "authorisation_reference", "validity")
    list_filter = ("actor_type", "jurisdiction")
    search_fields = ("organisation__name", "authorisation_reference", "authorisation_register")
    inlines = [ActorOperatorInline]
    readonly_fields = ("uuid", "created_at", "updated_at")

    @admin.display(description=_("validité"))
    def validity(self, obj: AuthorizedActor) -> str:
        words = {
            "valid": _("en vigueur"),
            "expired": _("échue"),
            "suspended": _("suspendue"),
            "withdrawn": _("retirée"),
        }
        until = obj.valid_until.strftime("%d.%m.%Y") if obj.valid_until else "—"
        return f"{words[obj.status_word]} · {until}"


class SelectionEvidenceInline(BaseTabularInline):
    model = SelectionEvidence
    extra = 0
    fields = ("order", "requirement", "responsible_actor", "status", "due_date")


class SelectionStageEventInline(BaseTabularInline):
    model = SelectionStageEvent
    extra = 0
    can_delete = False
    fields = ("created_at", "from_stage", "to_stage", "actor", "note")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None) -> bool:
        # A movement is written by the service that performed it, with the actor answerable for it.
        return False


@admin.register(SelectionMandate)
class SelectionMandateAdmin(BaseModelAdmin):
    list_display = ("reference", "need_profile", "company", "actor", "issued_at", "valid_until", "revoked_at")
    list_filter = ("need_sector", "need_territory")
    search_fields = ("reference", "need_profile", "need_reference", "company__name")
    readonly_fields = ("uuid", "reference", "created_at", "updated_at")
    autocomplete_fields = ("actor", "company")


@admin.register(SelectionProcess)
class SelectionProcessAdmin(BaseModelAdmin):
    list_display = ("reference", "stage", "outcome", "actor", "opened_at", "closed_at")
    list_filter = ("stage", "outcome")
    search_fields = ("reference", "case__reference", "mandate__reference")
    # ``stage`` and ``outcome`` are READ-ONLY here, as this module's docstring says they must be.
    # Left editable they were a second, undeclared way to move a process: the admin form calls
    # neither ``services.advance`` nor ``services.conclude``, so a stage changed here would skip
    # ``ALLOWED_STAGE_TRANSITIONS``, write no ``SelectionStageEvent`` and write no audit event —
    # and the resulting stage would name no authorised actor answerable for it. An administrator is
    # not that actor; the act belongs to the operator, in the workspace.
    readonly_fields = (
        "uuid",
        "reference",
        "stage",
        "outcome",
        "stage_since",
        "previous_stage",
        "opened_at",
        "closed_at",
    )
    inlines = [SelectionEvidenceInline, SelectionStageEventInline]

    def has_add_permission(self, request) -> bool:
        # ``services.open_process`` is the only way a process comes into existence, because it is
        # what checks the mandate is live, that the account is a live operator, and that the case
        # is in a state ``cases`` lets SELECTION be reached from — and what then creates the
        # ``CaseAssignment`` carrying the authorisation. A row added through this form would have
        # none of that: an unassigned case in SELECTION, with no authorisation behind it.
        return False


class IdentityAccessInline(BaseTabularInline):
    model = IdentityAccess
    extra = 0
    can_delete = False
    fields = ("accessed_at", "accessed_by", "accessed_by_organisation", "fields_read", "purpose_at_access")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(IdentityDisclosure)
class IdentityDisclosureAdmin(BaseModelAdmin):
    list_display = ("process", "recipient_organisation", "status", "decided_at", "expires_at", "withdrawn_at")
    list_filter = ("status",)
    search_fields = ("process__reference", "recipient_organisation__name")
    # ``status`` joins the list: granting is the PERSON's act and nobody else's. An administrator
    # flipping it to "Autorisée" could not in fact disclose anything — ``consent`` and
    # ``expires_at`` are read-only, so ``is_active()`` stays False and ``read_identity`` still
    # returns None — but the back-office listing would have said a person had consented when they
    # had not, which is the previous platform's defect written in a different place.
    readonly_fields = (
        "uuid",
        "status",
        "requested_at",
        "decided_at",
        "expires_at",
        "withdrawn_at",
        "consent",
    )
    inlines = [IdentityAccessInline]

    def has_add_permission(self, request) -> bool:
        # Only an authorised actor requests a disclosure, and only the person grants it. An
        # administrator creating one here would be exactly the defect the previous platform had.
        return False
