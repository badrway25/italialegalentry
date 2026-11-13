"""Access control: login, approved membership, category rooms, IDOR, member privacy."""

import pytest

from accounts.permissions import can
from community.models import Discussion, DiscussionStatus, MembershipStatus, Post, PostStatus
from core import clock

pytestmark = [pytest.mark.django_db, pytest.mark.security]

INDEX = "/fr/forum-virtuel/"


def test_anonymous_is_redirected_to_login(client, flag_on, rooms):
    r = client.get(INDEX + "salles/espace-commun/")
    assert r.status_code == 302
    assert r["Location"].startswith("/fr/compte/login/?next=")
    assert client.get(INDEX + "calendrier/").status_code == 302
    assert client.get(INDEX + "initiatives/").status_code == 302


def test_user_without_membership_is_403(client, flag_on, rooms, person_user):
    client.force_login(person_user)
    assert client.get(INDEX + "salles/espace-commun/").status_code == 403
    assert client.get(INDEX + "calendrier/").status_code == 403


@pytest.mark.parametrize("status", [MembershipStatus.PENDING, MembershipStatus.SUSPENDED])
def test_non_approved_member_is_403(client, flag_on, rooms, member_factory, status):
    m = member_factory("x@example.test", status=status)
    client.force_login(m.user)
    assert client.get(INDEX + "salles/espace-commun/").status_code == 403
    assert client.get(INDEX).status_code == 200  # landing with notice, no rooms
    assert "Salles thématiques" not in client.get(INDEX).content.decode()


def test_rooms_filtered_by_category_and_direct_access_denied(
    client, flag_on, rooms, company_member, institution_member
):
    client.force_login(company_member.user)
    html = client.get(INDEX).content.decode()
    assert "/salles/entreprises/" in html and "/salles/espace-commun/" in html
    assert "/salles/institutions/" not in html and "/salles/brouillon/" not in html
    assert client.get(INDEX + "salles/entreprises/").status_code == 200
    assert client.get(INDEX + "salles/institutions/").status_code == 403  # IDOR by URL
    assert client.get(INDEX + "salles/brouillon/").status_code == 403  # unpublished
    assert client.get(INDEX + "salles/inexistante/").status_code == 404
    client.force_login(institution_member.user)
    assert client.get(INDEX + "salles/institutions/").status_code == 200
    assert client.get(INDEX + "salles/entreprises/").status_code == 403


def test_discussion_in_forbidden_room_is_403(client, flag_on, rooms, company_member, institution_member):
    d = Discussion.objects.create(
        room=rooms["institutions"], author=institution_member, title="Réservé", last_activity_at=clock.now()
    )
    Post.objects.create(discussion=d, author=institution_member, body="secret", status=PostStatus.VISIBLE)
    client.force_login(company_member.user)
    assert client.get(f"{INDEX}discussions/{d.pk}/").status_code == 403
    assert client.post(f"{INDEX}discussions/{d.pk}/", {"body": "intrusion"}).status_code == 403
    assert Post.objects.filter(body="intrusion").count() == 0


def test_hidden_discussion_visible_only_to_moderator(
    client, flag_on, discussion, company_member, member_factory, moderator
):
    discussion.status = DiscussionStatus.HIDDEN
    discussion.save()
    other = member_factory("other@example.test", trusted=True)
    client.force_login(other.user)
    assert client.get(f"{INDEX}discussions/{discussion.pk}/").status_code == 403
    assert "Première discussion" not in client.get(INDEX + "salles/espace-commun/").content.decode()
    client.force_login(moderator)
    assert client.get(f"{INDEX}discussions/{discussion.pk}/").status_code == 200
    assert "Première discussion" in client.get(INDEX + "salles/espace-commun/").content.decode()


def test_member_cannot_edit_or_report_own_and_others_wrongly(
    client, flag_on, discussion, company_member, member_factory
):
    post = discussion.posts.get()
    other = member_factory("other@example.test", trusted=True)
    client.force_login(other.user)
    assert client.get(f"{INDEX}messages/{post.pk}/modifier/").status_code == 403
    assert client.post(f"{INDEX}messages/{post.pk}/modifier/", {"body": "hijack"}).status_code == 403
    assert Post.objects.get(pk=post.pk).body == "Premier message"
    client.force_login(company_member.user)
    assert client.get(f"{INDEX}messages/{post.pk}/modifier/").status_code == 200
    assert client.get(f"{INDEX}messages/{post.pk}/signaler/").status_code == 403  # cannot report own post


def test_nothing_personal_leaks_by_default(client, flag_on, rooms, member_factory):
    author = member_factory(
        "hidden.author@example.test", full_name="Nom Caché", organisation="Société Cachée", trusted=True
    )
    d = Discussion.objects.create(room=rooms["common"], author=author, title="Sujet", last_activity_at=clock.now())
    Post.objects.create(discussion=d, author=author, body="Bonjour", status=PostStatus.VISIBLE)
    viewer = member_factory("viewer@example.test", trusted=True)
    client.force_login(viewer.user)
    for path in (INDEX + "salles/espace-commun/", f"{INDEX}discussions/{d.pk}/"):
        html = client.get(path).content.decode()
        assert "hidden.author@example.test" not in html
        assert "Nom Caché" not in html and "Société Cachée" not in html
        # the viewer's own e-mail may appear in the site header account menu (shown only to themself)
        assert "hidden.author" not in html
    assert author.public_label() == "Participant"
    author.show_name = True
    author.save()
    html = client.get(f"{INDEX}discussions/{d.pk}/").content.decode()
    assert "Nom Caché" in html and "Société Cachée" not in html
    author.show_organisation = True
    author.save()
    assert "Société Cachée" in client.get(f"{INDEX}discussions/{d.pk}/").content.decode()
    assert author.public_label() == "Nom Caché — Société Cachée"


def test_policies_deny_by_default(rooms, company_member, moderator, person_user):
    room = rooms["institutions"]
    assert can(company_member.user, "view", room) is False
    assert can(company_member.user, "view", rooms["companies"]) is True
    assert can(company_member.user, "delete", rooms["companies"]) is False
    assert can(moderator, "view", room) is True and can(moderator, "moderate", room) is True
    assert can(person_user, "view", rooms["common"]) is False
    assert can(company_member.user, "view", company_member) is True
    assert can(person_user, "view", company_member) is False


def test_moderator_without_membership_can_read_but_not_post(client, flag_on, discussion, moderator):
    client.force_login(moderator)
    html = client.get(f"{INDEX}discussions/{discussion.pk}/").content.decode()
    assert "Modération de la discussion" in html
    assert 'name="body"' not in html
    assert client.post(f"{INDEX}discussions/{discussion.pk}/", {"body": "x"}).status_code == 403
