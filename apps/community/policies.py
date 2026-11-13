"""
Object-level policies (deny by default) registered with ``accounts.permissions``.

Actions: "view", "reply", "edit", "report", "moderate". Moderators = role:moderator,
role:administrator, role:superadmin (or superuser). Members act only within their approved
membership and the rooms allowed for their category.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from community.models import (
    CalendarEntry,
    Discussion,
    DiscussionStatus,
    Initiative,
    Membership,
    MembershipStatus,
    Post,
    PostStatus,
    Report,
    Room,
)

MODERATOR_ROLES = (roles.MODERATOR, roles.ADMINISTRATOR, roles.SUPERADMIN)


def is_moderator(user) -> bool:
    return roles.has_role(user, *MODERATOR_ROLES)


def membership_of(user) -> Membership | None:
    if not getattr(user, "is_authenticated", False):
        return None
    try:
        return user.community_membership
    except Membership.DoesNotExist:
        return None


def approved_membership_of(user) -> Membership | None:
    membership = membership_of(user)
    if membership and membership.status == MembershipStatus.APPROVED:
        return membership
    return None


def _room_visible(user, room: Room) -> bool:
    if is_moderator(user):
        return True
    membership = approved_membership_of(user)
    return bool(membership and room.published and room.allows(membership.category))


@policy(Room)
def _room_policy(user, action, room: Room) -> bool:
    if action == "view":
        return _room_visible(user, room)
    if action == "post":
        return _room_visible(user, room) and approved_membership_of(user) is not None
    if action == "moderate":
        return is_moderator(user)
    return False


@policy(Discussion)
def _discussion_policy(user, action, discussion: Discussion) -> bool:
    moderator = is_moderator(user)
    if action == "view":
        if not _room_visible(user, discussion.room):
            return False
        if discussion.status == DiscussionStatus.HIDDEN and not moderator:
            membership = approved_membership_of(user)
            return bool(membership and discussion.author_id == membership.id)
        return True
    if action == "reply":
        membership = approved_membership_of(user)
        return bool(membership and discussion.is_open and _room_visible(user, discussion.room))
    if action == "moderate":
        return moderator
    return False


@policy(Post)
def _post_policy(user, action, post: Post) -> bool:
    moderator = is_moderator(user)
    membership = approved_membership_of(user)
    own = bool(membership and post.author_id == membership.id)
    if action == "view":
        if not _discussion_policy(user, "view", post.discussion):
            return False
        return post.status == PostStatus.VISIBLE or own or moderator
    if action == "edit":
        return own and post.status != PostStatus.HIDDEN and post.discussion.is_open
    if action == "report":
        return bool(membership and not own and post.status == PostStatus.VISIBLE)
    if action == "moderate":
        return moderator
    return False


@policy(Membership)
def _membership_policy(user, action, membership: Membership) -> bool:
    if action == "view":
        return membership.user_id == user.id or is_moderator(user)
    if action == "moderate":
        return is_moderator(user)
    return False


@policy(Report)
def _report_policy(user, action, report: Report) -> bool:
    return action in ("view", "moderate") and is_moderator(user)


@policy(CalendarEntry)
def _calendar_policy(user, action, entry: CalendarEntry) -> bool:
    if action != "view":
        return is_moderator(user) and action == "moderate"
    if is_moderator(user):
        return True
    if not entry.published:
        return False
    if entry.room_id is None:
        return approved_membership_of(user) is not None
    return _room_visible(user, entry.room)


@policy(Initiative)
def _initiative_policy(user, action, initiative: Initiative) -> bool:
    if action != "view":
        return is_moderator(user) and action == "moderate"
    if is_moderator(user):
        return True
    if not initiative.published:
        return False
    if initiative.room_id is None:
        return approved_membership_of(user) is not None
    return _room_visible(user, initiative.room)
