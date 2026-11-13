"""Moderator actions in-site and in the back-office; membership approval; audit trail."""

import datetime as dt

import pytest

from audit.models import AuditEvent
from community import services
from community.models import (
    Discussion,
    DiscussionStatus,
    MembershipStatus,
    ModerationAction,
    Post,
    PostStatus,
    Report,
    ReportStatus,
)
from core import clock

pytestmark = pytest.mark.django_db

INDEX = "/fr/forum-virtuel/"


@pytest.fixture
def pending_post(discussion, new_member):
    return Post.objects.create(
        discussion=discussion, author=new_member, body="en attente", status=PostStatus.PENDING_MODERATION
    )


def test_member_cannot_moderate(client, flag_on, pending_post, company_member):
    client.force_login(company_member.user)
    r = client.post(f"{INDEX}messages/{pending_post.pk}/moderation/", {"action": "approve"})
    assert r.status_code == 403
    assert Post.objects.get(pk=pending_post.pk).status == PostStatus.PENDING_MODERATION
    r = client.post(f"{INDEX}discussions/{pending_post.discussion_id}/moderation/", {"action": "close"})
    assert r.status_code == 403


def test_moderator_approves_and_hides_posts(client, flag_on, pending_post, moderator, company_member):
    client.force_login(moderator)
    html = client.get(f"{INDEX}discussions/{pending_post.discussion_id}/").content.decode()
    assert "en attente" in html  # moderators see the queue inline
    r = client.post(f"{INDEX}messages/{pending_post.pk}/moderation/", {"action": "approve", "note": "ok"})
    assert r.status_code == 302
    pending_post.refresh_from_db()
    assert pending_post.status == PostStatus.VISIBLE and pending_post.moderated_by == moderator
    assert ModerationAction.objects.filter(post=pending_post, action="approve", note="ok").exists()
    assert AuditEvent.objects.filter(action="community.post.approve", actor=moderator).exists()
    client.post(f"{INDEX}messages/{pending_post.pk}/moderation/", {"action": "hide"})
    assert Post.objects.get(pk=pending_post.pk).status == PostStatus.HIDDEN
    client.force_login(company_member.user)
    assert "en attente" not in client.get(f"{INDEX}discussions/{pending_post.discussion_id}/").content.decode()
    assert client.get(f"{INDEX}messages/{pending_post.pk}/moderation/").status_code == 405  # POST-only endpoint


def test_invalid_moderation_action_is_rejected(client, flag_on, pending_post, moderator):
    client.force_login(moderator)
    client.post(f"{INDEX}messages/{pending_post.pk}/moderation/", {"action": "delete"})
    assert Post.objects.get(pk=pending_post.pk).status == PostStatus.PENDING_MODERATION
    assert ModerationAction.objects.count() == 0
    assert client.get(f"{INDEX}messages/{pending_post.pk}/moderation/").status_code == 405


def test_moderator_closes_and_reopens_discussion(client, flag_on, discussion, moderator):
    client.force_login(moderator)
    client.post(f"{INDEX}discussions/{discussion.pk}/moderation/", {"action": "close"})
    assert Discussion.objects.get(pk=discussion.pk).status == DiscussionStatus.CLOSED
    client.post(f"{INDEX}discussions/{discussion.pk}/moderation/", {"action": "reopen"})
    assert Discussion.objects.get(pk=discussion.pk).status == DiscussionStatus.OPEN
    assert ModerationAction.objects.filter(discussion=discussion).count() == 2


def test_services_reject_unknown_actions(discussion, moderator):
    with pytest.raises(ValueError):
        services.moderate_post(discussion.posts.get(), moderator, "delete")
    with pytest.raises(ValueError):
        services.moderate_discussion(discussion, moderator, "purge")


def test_admin_moderation_queue_and_actions(admin_client, pending_post, admin_user):
    r = admin_client.get("/backoffice/community/pendingpost/")
    assert r.status_code == 200
    assert "en attente" in r.content.decode()
    r = admin_client.post(
        "/backoffice/community/pendingpost/",
        {"action": "approve", "_selected_action": [pending_post.pk]},
    )
    assert r.status_code == 302
    assert Post.objects.get(pk=pending_post.pk).status == PostStatus.VISIBLE
    assert "en attente" not in admin_client.get("/backoffice/community/pendingpost/").content.decode()


def test_admin_membership_approval_and_suspension(admin_client, member_factory, admin_user):
    m = member_factory("wait@example.test", status=MembershipStatus.PENDING)
    r = admin_client.post("/backoffice/community/membership/", {"action": "approve", "_selected_action": [m.pk]})
    assert r.status_code == 302
    m.refresh_from_db()
    assert m.status == MembershipStatus.APPROVED and m.approved_by == admin_user and m.approved_at
    assert AuditEvent.objects.filter(action="community.membership.approved").exists()
    admin_client.post("/backoffice/community/membership/", {"action": "suspend", "_selected_action": [m.pk]})
    m.refresh_from_db()
    assert m.status == MembershipStatus.SUSPENDED
    assert ModerationAction.objects.filter(membership=m, action="suspend").exists()


def test_admin_reports_handling(admin_client, discussion, member_factory, admin_user):
    post = discussion.posts.get()
    reporter = member_factory("rep@example.test")
    report = Report.objects.create(post=post, reporter=reporter, reason="spam")
    r = admin_client.post(
        "/backoffice/community/report/", {"action": "hide_reported_posts", "_selected_action": [report.pk]}
    )
    assert r.status_code == 302
    report.refresh_from_db()
    assert report.status == ReportStatus.HANDLED and report.handled_by == admin_user
    assert Post.objects.get(pk=post.pk).status == PostStatus.HIDDEN


def test_admin_changelists_load(admin_client, discussion, rooms):
    for model in (
        "membership",
        "room",
        "discussion",
        "post",
        "report",
        "moderationaction",
        "calendarentry",
        "initiative",
    ):
        assert admin_client.get(f"/backoffice/community/{model}/").status_code == 200, model


def test_calendar_and_initiatives_scoping(client, flag_on, rooms, company_member, institution_member, moderator):
    from community.models import CalendarEntry, Collaboration, Initiative

    # A year after and a year before the clock, never a fixed year: « 2030 » stopped being upcoming on
    # 1 January 2030, and ``replace(year=...)`` cannot carry 29 February into a common year.
    now = clock.now()
    later = now + dt.timedelta(days=365)
    CalendarEntry.objects.create(title="Réunion commune", starts_at=later, published=True)
    CalendarEntry.objects.create(
        title="Réunion institutions", starts_at=later, published=True, room=rooms["institutions"]
    )
    CalendarEntry.objects.create(title="Brouillon calendrier", starts_at=later, published=False)
    CalendarEntry.objects.create(title="Passé", starts_at=now - dt.timedelta(days=365), published=True)
    init = Initiative.objects.create(title="Initiative commune", published=True, status="active")
    Collaboration.objects.create(initiative=init, organisation_names="Org A, Org B", status="active")
    Initiative.objects.create(title="Initiative institutions", published=True, room=rooms["institutions"])
    Initiative.objects.create(title="Initiative cachée", published=False)
    client.force_login(company_member.user)
    html = client.get(INDEX + "calendrier/").content.decode()
    assert "Réunion commune" in html
    assert "Réunion institutions" not in html and "Brouillon calendrier" not in html and "Passé" not in html
    html = client.get(INDEX + "initiatives/").content.decode()
    assert "Initiative commune" in html and "Org A, Org B" in html
    assert "Initiative institutions" not in html and "Initiative cachée" not in html
    client.force_login(institution_member.user)
    assert "Réunion institutions" in client.get(INDEX + "calendrier/").content.decode()
    client.force_login(moderator)
    html = client.get(INDEX + "calendrier/").content.decode()
    assert "Brouillon calendrier" in html
    assert "Réunion commune" in client.get(INDEX).content.decode()
