"""Every community page renders the locked texts verbatim and contains no forbidden formulation."""

import pytest

from cms import locked_content
from cms.forbidden import scan
from community.models import Post, PostStatus

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

INDEX = "/fr/forum-virtuel/"


def test_member_pages_are_compliant(client, seeded, flag_on, legal_published, discussion, company_member, person_user):
    post = discussion.posts.get()
    other_post = Post.objects.create(discussion=discussion, author=None, body="autre", status=PostStatus.VISIBLE)
    client.force_login(company_member.user)
    paths = [
        INDEX,
        INDEX + "salles/espace-commun/",
        f"{INDEX}discussions/{discussion.pk}/",
        f"{INDEX}messages/{post.pk}/modifier/",
        f"{INDEX}messages/{other_post.pk}/signaler/",
        INDEX + "calendrier/",
        INDEX + "initiatives/",
    ]
    for path in paths:
        r = client.get(path)
        assert r.status_code == 200, path
        html = r.content.decode()
        assert not scan(html), (path, scan(html))
        assert "Italy Legal Entry™" in html and "®" not in html, path
        assert html.count("<h1") == 1, path
        assert 'id="main-content"' in html and "<nav" in html, path
        assert "legalitalentry.it" not in html.replace("legalitalentry.it/", "").replace("://localhost", "")
    html = client.get(INDEX).content.decode()
    assert locked_content.text("p3.virtual_forum.title", "fr") in html
    assert locked_content.text("p3.virtual_forum.body", "fr") in html
    client.force_login(person_user)
    html = client.get(INDEX + "rejoindre/").content.decode()
    assert not scan(html) and html.count("<h1") == 1


def test_email_notification_has_no_forbidden_strings(seeded, flag_on, legal_published, client, person_user):
    from notifications.models import EmailOutbox

    client.force_login(person_user)
    client.post(INDEX + "rejoindre/", {"category": "company", "consent": "on"})
    mail = EmailOutbox.objects.get()
    assert not scan(mail.subject + "\n" + mail.body_text)
    assert "@legalitalentry.it" not in mail.body_text
