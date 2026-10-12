"""Forum Virtuel services — every state change goes through here (views stay thin)."""

from __future__ import annotations

import logging

from django.db import transaction
from django.db.models import Exists, OuterRef, Q, QuerySet
from django.utils.translation import gettext as _

from community import conf
from community.models import (
    CalendarEntry,
    Collaboration,
    Discussion,
    DiscussionStatus,
    Initiative,
    Membership,
    MembershipStatus,
    ModerationAction,
    ModerationActionKind,
    Post,
    PostStatus,
    Report,
    ReportStatus,
    Room,
)
from community.policies import approved_membership_of, is_moderator, membership_of
from core import clock

log = logging.getLogger("ile.community")

__all__ = [
    "approved_membership_of",
    "is_moderator",
    "membership_of",
]


def _audit(request, action: str, target=None, metadata: dict | None = None, actor=None):
    from audit.services import record

    return record(request, action=action, target=target, metadata=metadata or {}, actor=actor)


def _emit(event_type: str, obj, payload: dict) -> None:
    try:
        from integrations.services import emit

        emit(event_type, obj, payload)
    except Exception:  # noqa: BLE001 - integration must never break the forum
        log.exception("integration emit failed for %s", event_type)


# --------------------------------------------------------------------------------------------
# Access & visibility
# --------------------------------------------------------------------------------------------
def rooms_for(membership: Membership | None, moderator: bool = False) -> QuerySet[Room]:
    if moderator:
        return Room.objects.published()
    if membership is None or not membership.is_approved:
        return Room.objects.none()
    return Room.objects.for_category(membership.category)


def visible_discussions(room: Room, membership: Membership | None, moderator: bool) -> QuerySet[Discussion]:
    qs = room.discussions.select_related("author__user")
    if moderator:
        return qs
    has_visible = Post.objects.filter(discussion=OuterRef("pk"), status=PostStatus.VISIBLE)
    qs = qs.exclude(status=DiscussionStatus.HIDDEN).annotate(has_visible=Exists(has_visible))
    return qs.filter(Q(has_visible=True) | Q(author=membership))


def visible_posts(discussion: Discussion, membership: Membership | None, moderator: bool) -> QuerySet[Post]:
    qs = discussion.posts.select_related("author__user").prefetch_related("attachments").order_by("created_at")
    if moderator:
        return qs
    return qs.filter(Q(status=PostStatus.VISIBLE) | Q(author=membership, status=PostStatus.PENDING_MODERATION))


def visible_post_count(membership: Membership) -> int:
    return Post.objects.filter(author=membership, status=PostStatus.VISIBLE).count()


def needs_moderation(room: Room, membership: Membership) -> bool:
    """New members (few visible posts, not marked trusted) queue their posts in moderated rooms."""
    if not room.is_moderated or membership.trusted:
        return False
    return visible_post_count(membership) < conf.trusted_post_threshold()


def upcoming_calendar(membership: Membership | None, moderator: bool) -> QuerySet[CalendarEntry]:
    now = clock.now()
    qs = CalendarEntry.objects.filter(Q(ends_at__gte=now) | Q(ends_at__isnull=True, starts_at__gte=now))
    qs = qs.select_related("room").order_by("starts_at")
    if moderator:
        return qs
    room_ids = list(rooms_for(membership).values_list("id", flat=True))
    return qs.filter(published=True).filter(Q(room__isnull=True) | Q(room_id__in=room_ids))


def initiatives_for(membership: Membership | None, moderator: bool) -> QuerySet[Initiative]:
    qs = Initiative.objects.select_related("room").prefetch_related("collaborations")
    if moderator:
        return qs
    room_ids = list(rooms_for(membership).values_list("id", flat=True))
    return qs.filter(published=True).filter(Q(room__isnull=True) | Q(room_id__in=room_ids))


# --------------------------------------------------------------------------------------------
# Membership lifecycle
# --------------------------------------------------------------------------------------------
@transaction.atomic
def request_membership(
    request, user, *, category: str, organisation: str, show_name: bool, show_organisation: bool
) -> Membership:
    from consents.models import ConsentPurpose
    from consents.services import record_consent
    from notifications.services import notify_forms_inbox

    consent = record_consent(request, ConsentPurpose.COMMUNITY, email=user.email, user=user)
    membership = Membership.objects.create(
        user=user,
        category=category,
        organisation=organisation,
        status=MembershipStatus.PENDING,
        accepted_terms_at=clock.now(),
        consent=consent,
        show_name=show_name,
        show_organisation=show_organisation,
    )
    _audit(request, "community.membership.requested", membership, {"category": category})
    notify_forms_inbox(
        subject=_("Nouvelle demande d’accès au Forum Virtuel"),
        template="community_membership_requested",
        context={"membership": membership, "user_email": user.email},
        reference=f"community.Membership:{membership.pk}",
    )
    _emit("community.membership.requested", membership, {"category": category, "created_at": membership.created_at})
    return membership


def approve_membership(membership: Membership, by_user, request=None) -> Membership:
    membership.status = MembershipStatus.APPROVED
    membership.approved_at = clock.now()
    membership.approved_by = by_user
    membership.suspended_reason = ""
    membership.save(update_fields=["status", "approved_at", "approved_by", "suspended_reason", "updated_at"])
    _audit(request, "community.membership.approved", membership, actor=by_user)
    _emit("community.membership.approved", membership, {"category": membership.category})
    return membership


def suspend_membership(membership: Membership, by_user, reason: str = "", request=None) -> Membership:
    membership.status = MembershipStatus.SUSPENDED
    membership.suspended_reason = reason[:200]
    membership.save(update_fields=["status", "suspended_reason", "updated_at"])
    ModerationAction.objects.create(
        moderator=by_user, membership=membership, action=ModerationActionKind.SUSPEND, note=reason[:300]
    )
    _audit(request, "community.membership.suspended", membership, actor=by_user)
    return membership


def update_visibility(membership: Membership, *, show_name: bool, show_organisation: bool) -> Membership:
    membership.show_name = show_name
    membership.show_organisation = show_organisation
    membership.save(update_fields=["show_name", "show_organisation", "updated_at"])
    return membership


# --------------------------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------------------------
def _post_status_for(room: Room, membership: Membership) -> str:
    return PostStatus.PENDING_MODERATION if needs_moderation(room, membership) else PostStatus.VISIBLE


@transaction.atomic
def create_discussion(request, room: Room, membership: Membership, *, title: str, body: str) -> tuple[Discussion, Post]:
    now = clock.now()
    discussion = Discussion.objects.create(room=room, author=membership, title=title, last_activity_at=now)
    post = Post.objects.create(
        discussion=discussion, author=membership, body=body, status=_post_status_for(room, membership)
    )
    _audit(request, "community.discussion.created", discussion, {"room": room.slug, "post_status": post.status})
    return discussion, post


@transaction.atomic
def create_post(request, discussion: Discussion, membership: Membership, *, body: str) -> Post:
    post = Post.objects.create(
        discussion=discussion,
        author=membership,
        body=body,
        status=_post_status_for(discussion.room, membership),
    )
    if post.status == PostStatus.VISIBLE:
        discussion.last_activity_at = clock.now()
        discussion.save(update_fields=["last_activity_at", "updated_at"])
    _audit(request, "community.post.created", post, {"status": post.status})
    return post


def edit_post(request, post: Post, *, body: str) -> Post:
    post.body = body
    post.edited_at = clock.now()
    post.save(update_fields=["body", "edited_at", "updated_at"])
    _audit(request, "community.post.edited", post)
    return post


def report_post(request, post: Post, reporter: Membership, *, reason: str) -> Report:
    report, created = Report.objects.get_or_create(post=post, reporter=reporter, defaults={"reason": reason})
    if created:
        _audit(request, "community.report.created", report)
    return report


# --------------------------------------------------------------------------------------------
# Moderation
# --------------------------------------------------------------------------------------------
POST_ACTIONS = {
    ModerationActionKind.HIDE: PostStatus.HIDDEN,
    ModerationActionKind.UNHIDE: PostStatus.VISIBLE,
    ModerationActionKind.APPROVE: PostStatus.VISIBLE,
}
DISCUSSION_ACTIONS = {
    ModerationActionKind.CLOSE: DiscussionStatus.CLOSED,
    ModerationActionKind.REOPEN: DiscussionStatus.OPEN,
    ModerationActionKind.HIDE: DiscussionStatus.HIDDEN,
    ModerationActionKind.UNHIDE: DiscussionStatus.OPEN,
}


@transaction.atomic
def moderate_post(post: Post, moderator, action: str, note: str = "", request=None) -> Post:
    if action not in POST_ACTIONS:
        raise ValueError(f"unsupported post action {action!r}")
    post.status = POST_ACTIONS[action]
    post.moderated_by = moderator
    post.save(update_fields=["status", "moderated_by", "updated_at"])
    if post.status == PostStatus.VISIBLE:
        Discussion.objects.filter(pk=post.discussion_id).update(last_activity_at=clock.now())
    ModerationAction.objects.create(moderator=moderator, post=post, action=action, note=note[:300])
    _audit(request, f"community.post.{action}", post, actor=moderator)
    return post


@transaction.atomic
def moderate_discussion(discussion: Discussion, moderator, action: str, note: str = "", request=None) -> Discussion:
    if action not in DISCUSSION_ACTIONS:
        raise ValueError(f"unsupported discussion action {action!r}")
    discussion.status = DISCUSSION_ACTIONS[action]
    discussion.save(update_fields=["status", "updated_at"])
    ModerationAction.objects.create(moderator=moderator, discussion=discussion, action=action, note=note[:300])
    _audit(request, f"community.discussion.{action}", discussion, actor=moderator)
    return discussion


def warn_member(membership: Membership, moderator, note: str, request=None) -> ModerationAction:
    action = ModerationAction.objects.create(
        moderator=moderator, membership=membership, action=ModerationActionKind.WARN, note=note[:300]
    )
    _audit(request, "community.membership.warned", membership, actor=moderator)
    return action


def handle_report(report: Report, moderator, *, status: str, note: str = "", request=None) -> Report:
    report.status = status
    report.handled_by = moderator
    report.handled_at = clock.now()
    report.handling_note = note[:300]
    report.save(update_fields=["status", "handled_by", "handled_at", "handling_note", "updated_at"])
    _audit(request, f"community.report.{status}", report, actor=moderator)
    return report


def moderation_queue() -> QuerySet[Post]:
    return Post.objects.filter(status=PostStatus.PENDING_MODERATION).select_related("discussion__room", "author")


def open_reports() -> QuerySet[Report]:
    return Report.objects.filter(status=ReportStatus.OPEN).select_related("post__discussion", "reporter")


def add_collaboration(initiative: Initiative, *, organisation_names: str, status: str, note: str = "") -> Collaboration:
    return Collaboration.objects.create(
        initiative=initiative, organisation_names=organisation_names, status=status, note=note[:300]
    )
