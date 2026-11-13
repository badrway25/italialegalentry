"""Posting: moderation queue for new members, throttle, escaping, edit, reports."""

import pytest
from django.test import override_settings

from audit.models import AuditEvent
from community.models import Discussion, Post, PostStatus, Report

pytestmark = pytest.mark.django_db

INDEX = "/fr/forum-virtuel/"


def test_new_member_in_moderated_room_is_queued(client, flag_on, rooms, new_member, company_member):
    client.force_login(new_member.user)
    r = client.post(INDEX + "salles/espace-commun/", {"title": "Bonjour", "body": "Mon premier message"})
    assert r.status_code == 302
    d = Discussion.objects.get(title="Bonjour")
    post = d.posts.get()
    assert post.status == PostStatus.PENDING_MODERATION
    html = client.get(r["Location"]).content.decode()
    assert "Mon premier message" in html and "En attente de modération" in html
    # invisible to other members (and the discussion itself is not listed for them)
    client.force_login(company_member.user)
    assert client.get(f"{INDEX}discussions/{d.pk}/").status_code == 200
    assert "Mon premier message" not in client.get(f"{INDEX}discussions/{d.pk}/").content.decode()
    assert "Bonjour" not in client.get(INDEX + "salles/espace-commun/").content.decode()
    assert AuditEvent.objects.filter(action="community.discussion.created").exists()


def test_new_member_in_unmoderated_room_posts_directly(client, flag_on, rooms, member_factory):
    m = member_factory("inst.new@example.test", category="institution")
    client.force_login(m.user)
    client.post(INDEX + "salles/institutions/", {"title": "Direct", "body": "texte"})
    assert Discussion.objects.get(title="Direct").posts.get().status == PostStatus.VISIBLE


def test_trusted_member_posts_are_visible(client, flag_on, discussion, company_member, member_factory):
    client.force_login(company_member.user)
    r = client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "Réponse directe"})
    assert r.status_code == 302
    post = Post.objects.get(body="Réponse directe")
    assert post.status == PostStatus.VISIBLE
    discussion.refresh_from_db()
    assert discussion.last_activity_at >= post.created_at
    other = member_factory("reader@example.test", trusted=True)
    client.force_login(other.user)
    assert "Réponse directe" in client.get(f"{INDEX}discussions/{discussion.pk}/").content.decode()


@override_settings(COMMUNITY_TRUSTED_POST_THRESHOLD=1)
def test_member_becomes_trusted_after_threshold(client, flag_on, discussion, new_member):
    client.force_login(new_member.user)
    client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "premier"})
    assert Post.objects.get(body="premier").status == PostStatus.PENDING_MODERATION
    Post.objects.filter(body="premier").update(status=PostStatus.VISIBLE)
    client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "second"})
    assert Post.objects.get(body="second").status == PostStatus.VISIBLE


def test_body_is_escaped(client, flag_on, discussion, company_member):
    client.force_login(company_member.user)
    client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "<script>alert(1)</script> & <b>x</b>"})
    html = client.get(f"{INDEX}discussions/{discussion.pk}/").content.decode()
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp; &lt;b&gt;x&lt;/b&gt;" in html


@override_settings(COMMUNITY_POST_THROTTLE={"limit": 2, "window_seconds": 600})
def test_post_throttle_returns_429(client, flag_on, discussion, company_member):
    client.force_login(company_member.user)
    assert client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "un"}).status_code == 302
    assert client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "deux"}).status_code == 302
    r = client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "trois"})
    assert r.status_code == 429
    assert Post.objects.filter(body="trois").count() == 0


def test_validation_errors_are_shown_and_nothing_saved(client, flag_on, discussion, company_member):
    client.force_login(company_member.user)
    r = client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": ""})
    assert r.status_code == 200
    assert 'role="alert"' in r.content.decode()
    assert discussion.posts.count() == 1
    r = client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "x" * 9000})
    assert r.status_code == 200 and discussion.posts.count() == 1


def test_edit_own_post(client, flag_on, discussion, company_member):
    post = discussion.posts.get()
    client.force_login(company_member.user)
    r = client.post(f"{INDEX}messages/{post.pk}/modifier/", {"body": "Message corrigé"})
    assert r.status_code == 302
    post.refresh_from_db()
    assert post.body == "Message corrigé" and post.edited_at is not None
    assert "modifié" in client.get(f"{INDEX}discussions/{discussion.pk}/").content.decode()


def test_closed_discussion_rejects_replies(client, flag_on, discussion, company_member):
    discussion.status = "closed"
    discussion.save()
    client.force_login(company_member.user)
    html = client.get(f"{INDEX}discussions/{discussion.pk}/").content.decode()
    assert "Discussion fermée" in html and 'name="body"' not in html
    assert client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "trop tard"}).status_code == 403


def test_report_post(client, flag_on, discussion, member_factory):
    post = discussion.posts.get()
    reporter = member_factory("reporter@example.test", trusted=True)
    client.force_login(reporter.user)
    assert client.get(f"{INDEX}messages/{post.pk}/signaler/").status_code == 200
    r = client.post(f"{INDEX}messages/{post.pk}/signaler/", {"reason": "Contenu inapproprié"})
    assert r.status_code == 302
    report = Report.objects.get()
    assert report.reporter == reporter and report.status == "open"
    # duplicate report is idempotent
    client.post(f"{INDEX}messages/{post.pk}/signaler/", {"reason": "encore"})
    assert Report.objects.count() == 1
    assert AuditEvent.objects.filter(action="community.report.created").count() == 1


@override_settings(COMMUNITY_REPORT_THROTTLE={"limit": 1, "window_seconds": 600})
def test_report_throttle(client, flag_on, discussion, member_factory, company_member):
    post = discussion.posts.get()
    post2 = Post.objects.create(discussion=discussion, author=company_member, body="deux", status=PostStatus.VISIBLE)
    reporter = member_factory("reporter@example.test", trusted=True)
    client.force_login(reporter.user)
    assert client.post(f"{INDEX}messages/{post.pk}/signaler/", {"reason": "a"}).status_code == 302
    assert client.post(f"{INDEX}messages/{post2.pk}/signaler/", {"reason": "b"}).status_code == 429
