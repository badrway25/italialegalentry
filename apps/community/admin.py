"""
Back-office of the virtual forum — the moderators' (finding F-8).

``community.policies`` names the moderators: role:moderator, role:administrator, role:superadmin. Every screen here
moderates or reads what only a moderator reads — every membership (with the name and the organisation a member chose
not to show, REQ-FOR-06), every hidden or pending post, every report — so each opens to them alone, whatever else holds
the «community» model permissions: until F-8 role:staff, which the policy does not name, moderated here.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from community import services
from community.models import (
    Attachment,
    CalendarEntry,
    Collaboration,
    Discussion,
    Initiative,
    Membership,
    ModerationAction,
    ModerationActionKind,
    PendingPost,
    Post,
    PostStatus,
    Report,
    ReportStatus,
    Room,
)
from community.policies import MODERATOR_ROLES
from core import gates
from core.admin_base import BaseModelAdmin, BaseTabularInline, PolicyBoundAdminMixin


class ModeratorsOnly(PolicyBoundAdminMixin):
    """The screen opens to the moderators ``community.policies`` names, and to nobody else."""

    policy_roles = MODERATOR_ROLES


class FeatureBadgeMixin:
    """Shows a notice in every community changelist while the Virtual Forum flag is off."""

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = f"{self.model._meta.verbose_name_plural}" + (
            "" if gates.virtual_forum_enabled() else " — " + str(_("Funzionalità disattivata (flag virtual_forum)"))
        )
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Membership)
class MembershipAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("id", "user", "category", "organisation", "status", "trusted", "show_name", "created_at")
    list_filter = ("status", "category", "trusted", "show_name", "show_organisation")
    search_fields = ("user__email", "organisation")
    autocomplete_fields = ("user",)
    readonly_fields = ("consent", "accepted_terms_at", "approved_at", "approved_by")
    actions = ("approve", "suspend", "mark_trusted")
    fieldsets = (
        (None, {"fields": ("user", "category", "organisation", "status", "trusted", "suspended_reason")}),
        (
            _("Visibilità scelta dal membro (mai modificare senza richiesta scritta del membro)"),
            {"fields": ("show_name", "show_organisation")},
        ),
        (_("Consenso e approvazione"), {"fields": ("consent", "accepted_terms_at", "approved_at", "approved_by")}),
    )

    @admin.action(description=_("Approva l'iscrizione"))
    def approve(self, request, queryset):
        for membership in queryset.exclude(status="approved"):
            services.approve_membership(membership, request.user, request=request)

    @admin.action(description=_("Sospendi"))
    def suspend(self, request, queryset):
        for membership in queryset.exclude(status="suspended"):
            services.suspend_membership(membership, request.user, reason="sospeso dal back-office", request=request)

    @admin.action(description=_("Segna come affidabile (salta la coda di moderazione)"))
    def mark_trusted(self, request, queryset):
        # a moderation act — the member's posts skip the queue from now on — so it is in the audit trail, row by row
        for membership in queryset.filter(trusted=False):
            membership.trusted = True
            membership.save(update_fields=["trusted", "updated_at"])
            audit_record(request, action="community.membership.trusted", target=membership)


@admin.register(Room)
class RoomAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("name_fr", "slug", "kind", "is_moderated", "published", "order")
    list_filter = ("kind", "is_moderated", "published")
    list_editable = ("order", "published")
    search_fields = ("name_fr", "slug")
    prepopulated_fields = {"slug": ("name_fr",)}


class PostInline(BaseTabularInline):
    model = Post
    fields = ("author", "status", "body", "created_at")
    readonly_fields = ("author", "body", "created_at")
    show_change_link = True


@admin.register(Discussion)
class DiscussionAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("title", "room", "status", "pinned", "author", "last_activity_at", "created_at")
    list_filter = ("status", "pinned", "room")
    list_editable = ("pinned",)
    search_fields = ("title",)
    readonly_fields = ("author", "last_activity_at")
    inlines = (PostInline,)
    actions = ("close", "reopen", "hide")

    @admin.action(description=_("Chiudi"))
    def close(self, request, queryset):
        for d in queryset:
            services.moderate_discussion(d, request.user, ModerationActionKind.CLOSE, request=request)

    @admin.action(description=_("Riapri"))
    def reopen(self, request, queryset):
        for d in queryset:
            services.moderate_discussion(d, request.user, ModerationActionKind.REOPEN, request=request)

    @admin.action(description=_("Nascondi"))
    def hide(self, request, queryset):
        for d in queryset:
            services.moderate_discussion(d, request.user, ModerationActionKind.HIDE, request=request)


class AttachmentInline(BaseTabularInline):
    model = Attachment
    fields = ("label", "document_uuid")


class PostAdminBase(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("id", "excerpt", "discussion", "author", "status", "created_at", "edited_at", "moderated_by")
    list_filter = ("status", "discussion__room")
    search_fields = ("body", "discussion__title")
    readonly_fields = ("author", "discussion", "edited_at", "moderated_by")
    inlines = (AttachmentInline,)
    actions = ("approve", "hide", "unhide")

    def has_add_permission(self, request):
        return False

    @admin.display(description=_("testo"))
    def excerpt(self, obj) -> str:
        return (obj.body[:80] + "…") if len(obj.body) > 80 else obj.body

    @admin.action(description=_("Approva (rendi visibile)"))
    def approve(self, request, queryset):
        for post in queryset.exclude(status=PostStatus.VISIBLE):
            services.moderate_post(post, request.user, ModerationActionKind.APPROVE, request=request)

    @admin.action(description=_("Nascondi"))
    def hide(self, request, queryset):
        for post in queryset.exclude(status=PostStatus.HIDDEN):
            services.moderate_post(post, request.user, ModerationActionKind.HIDE, request=request)

    @admin.action(description=_("Rendi visibile"))
    def unhide(self, request, queryset):
        for post in queryset.filter(status=PostStatus.HIDDEN):
            services.moderate_post(post, request.user, ModerationActionKind.UNHIDE, request=request)


@admin.register(Post)
class PostAdmin(PostAdminBase):
    pass


@admin.register(PendingPost)
class PendingPostAdmin(PostAdminBase):
    """Moderation queue: only posts awaiting approval."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=PostStatus.PENDING_MODERATION)


@admin.register(Report)
class ReportAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("id", "post", "reporter", "status", "created_at", "handled_by", "handled_at")
    list_filter = ("status",)
    search_fields = ("reason",)
    readonly_fields = ("post", "reporter", "reason", "handled_by", "handled_at")
    actions = ("mark_handled", "dismiss", "hide_reported_posts")

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Segna come gestita"))
    def mark_handled(self, request, queryset):
        for report in queryset.filter(status=ReportStatus.OPEN):
            services.handle_report(report, request.user, status=ReportStatus.HANDLED, request=request)

    @admin.action(description=_("Archivia senza seguito"))
    def dismiss(self, request, queryset):
        for report in queryset.filter(status=ReportStatus.OPEN):
            services.handle_report(report, request.user, status=ReportStatus.DISMISSED, request=request)

    @admin.action(description=_("Nascondi i messaggi segnalati e segna come gestite"))
    def hide_reported_posts(self, request, queryset):
        for report in queryset.filter(status=ReportStatus.OPEN).select_related("post"):
            services.moderate_post(report.post, request.user, ModerationActionKind.HIDE, request=request)
            services.handle_report(report, request.user, status=ReportStatus.HANDLED, request=request)


@admin.register(ModerationAction)
class ModerationActionAdmin(ModeratorsOnly, BaseModelAdmin):
    list_display = ("created_at", "action", "moderator", "post", "discussion", "membership", "note")
    list_filter = ("action",)
    readonly_fields = [f.name for f in ModerationAction._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CalendarEntry)
class CalendarEntryAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("title", "room", "starts_at", "ends_at", "place", "published")
    list_filter = ("published", "room")
    list_editable = ("published",)
    search_fields = ("title", "place")
    date_hierarchy = "starts_at"


class CollaborationInline(BaseTabularInline):
    model = Collaboration
    fields = ("organisation_names", "status", "note")


@admin.register(Initiative)
class InitiativeAdmin(ModeratorsOnly, FeatureBadgeMixin, BaseModelAdmin):
    list_display = ("title", "room", "status", "owner", "published", "created_at")
    list_filter = ("status", "published", "room")
    list_editable = ("published",)
    search_fields = ("title",)
    inlines = (CollaborationInline,)
