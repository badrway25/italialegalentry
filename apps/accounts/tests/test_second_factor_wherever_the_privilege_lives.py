"""
F-8 — a staff privilege meets the second-factor policy wherever its URL lives, not only on the guarded paths.

sec-f5 (``accounts.middleware``) guards three PATHS: the back office, the reserved area, ``/documents/``. Its review
left one observation open (docs/design-v5/QA/v54/sec-f5/REVIEW.md, «Outside this fix»): «the perimeter is defined by
path. Privileged actions on public paths are outside both rules» — a moderator's powers on the virtual forum's public
pages, staff previews of unpublished news, «living» sheets, FAQ, glossary and Phase 3 pages. A session opened by
another door (``force_login`` here; a session from before the device was enrolled, a shortcut written later) that
never presented the factor read and moderated there freely.

Each branch that decides «this account acts as staff» now calls ``accounts.middleware.require_second_factor``: the same
two rules (enrol when the deployment requires it, present the device the account holds), the same redirects, and back
to the page asked for. A public visitor's request is untouched; a staff session that presented its factor, or an
account the policy does not cover, goes on as before. Accounts are this module's own, with a test-only password; the
TOTP devices are allauth's own, activated over a generated secret.
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from allauth.account.internal.flows.login import AUTHENTICATION_METHODS_SESSION_KEY
from allauth.mfa.models import Authenticator
from allauth.mfa.totp.internal import auth as totp_auth

from accounts import roles

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8-2026!"
MFA_REAUTH = "/fr/compte/2fa/reauthenticate/"
TOTP_ACTIVATE = "/fr/compte/2fa/totp/activate/"
FORUM = "/fr/forum-virtuel/"

#: Every staff preview on the public site, while Phase 3 is closed: the page a staff account opens that a visitor
#: does not (each app's own preview rule — ecosystem, pathways, pages, FAQ, glossary, «living»).
PREVIEWS = (
    "/fr/institutions/?preview=1",
    "/fr/parcours/?preview=1",
    "/fr/attention-aux-fraudes/?preview=1",
    "/fr/faq/",
    "/fr/glossaire/",
    "/fr/vivre-en-italie/?preview=1",
)


def _enrol_totp(user) -> Authenticator:
    totp_auth.TOTP.activate(user, totp_auth.generate_totp_secret())
    return Authenticator.objects.get(user=user, type=Authenticator.Type.TOTP)


def _present(client, authenticator) -> None:
    """Write the record allauth's MFA step writes (``record_authentication``): this session presented the factor."""
    session = client.session
    records = list(session.get(AUTHENTICATION_METHODS_SESSION_KEY, []))
    records.append({"method": "mfa", "at": time.time(), "id": authenticator.pk, "type": authenticator.type})
    session[AUTHENTICATION_METHODS_SESSION_KEY] = records
    session.save()


def _sent_to_present(response, asked: str) -> bool:
    if response.status_code != 302:
        return False
    target = urlsplit(response["Location"])
    return target.path == MFA_REAUTH and parse_qs(target.query).get("next") == [asked]


@pytest.fixture
def people(django_user_model):
    roles.ensure_roles()  # role:staff holds news.view_article and living.view_livingtopic, as in production

    def make(email, role, **extra):
        user = django_user_model.objects.create_user(email=email, password=PASSWORD, **extra)
        roles.assign_role(user, role)
        return user

    return {
        "staff": make("f8.staff@example.test", roles.STAFF, is_staff=True),
        "moderator": make("f8.moderator@example.test", roles.MODERATOR, is_staff=True),
        "person": make("f8.person@example.test", roles.PERSON),
    }


@pytest.fixture
def unpublished(db):
    from cms.models import PublicationStatus
    from news.models import Article, NewsCategory

    category, _ = NewsCategory.objects.get_or_create(slug="f8", defaults={"name_fr": "F8"})
    return Article.objects.create(
        slug="f8-draft", category=category, title_fr="F8 brouillon", body_fr="F8", status=PublicationStatus.DRAFT
    )


@pytest.fixture
def forum(set_flag, legal_published, people):
    from community.models import Discussion, Membership, MembershipStatus, ParticipantCategory, Post, PostStatus, Room
    from core import clock

    set_flag("virtual_forum", True)
    member_user = people["person"]
    member = Membership.objects.create(
        user=member_user,
        category=ParticipantCategory.COMPANY,
        status=MembershipStatus.APPROVED,
        approved_at=clock.now(),
    )
    room, _ = Room.objects.update_or_create(slug="f8-room", defaults={"name_fr": "F8", "published": True})
    discussion = Discussion.objects.create(room=room, author=member, title="F8", last_activity_at=clock.now())
    post = Post.objects.create(discussion=discussion, author=member, body="F8 visible", status=PostStatus.VISIBLE)
    return {"discussion": discussion, "post": post}


# ---------------------------------------------------------------------------------------------
# Reproduced, then held: a session that owes the factor exercises no staff privilege on a public path
# ---------------------------------------------------------------------------------------------
class TestAPrivilegeMeetsTheSecondFactor:
    @pytest.mark.parametrize("path", PREVIEWS)
    def test_a_staff_preview_asks_for_the_factor_first(self, client, people, path):
        _enrol_totp(people["staff"])
        client.force_login(people["staff"])
        response = client.get(path)
        assert _sent_to_present(response, path), f"F-8: {path} previewed on a password alone ({response.status_code})"

    def test_an_unpublished_article_asks_for_the_factor_first(self, client, people, unpublished):
        _enrol_totp(people["staff"])
        client.force_login(people["staff"])
        path = f"/fr/actualites/{unpublished.slug}/"
        response = client.get(path)
        assert _sent_to_present(response, path)
        assert "F8 brouillon" not in response.content.decode("utf-8")

    def test_a_moderator_reads_the_forum_only_after_the_factor(self, client, people, forum):
        _enrol_totp(people["moderator"])
        client.force_login(people["moderator"])
        for path in (FORUM, f"{FORUM}discussions/{forum['discussion'].pk}/"):
            assert _sent_to_present(client.get(path), path), path

    def test_a_moderator_moderates_nothing_before_the_factor(self, client, people, forum):
        from community.models import PostStatus

        _enrol_totp(people["moderator"])
        client.force_login(people["moderator"])
        path = f"{FORUM}messages/{forum['post'].pk}/moderation/"
        response = client.post(path, {"action": "hide", "note": "F8"})
        assert _sent_to_present(response, path)
        forum["post"].refresh_from_db()
        assert forum["post"].status == PostStatus.VISIBLE

    def test_an_account_the_deployment_requires_to_enrol_is_sent_to_enrol(self, client, people, settings):
        settings.BACKOFFICE_MFA_ENFORCED = True
        client.force_login(people["staff"])
        response = client.get("/fr/faq/")
        assert response.status_code == 302 and urlsplit(response["Location"]).path == TOTP_ACTIVATE


# ---------------------------------------------------------------------------------------------
# What stays as it was
# ---------------------------------------------------------------------------------------------
class TestWhatStays:
    def test_a_staff_session_that_presented_its_factor_previews(self, client, people, unpublished):
        device = _enrol_totp(people["staff"])
        client.force_login(people["staff"])
        _present(client, device)
        assert client.get(f"/fr/actualites/{unpublished.slug}/").status_code == 200
        assert client.get("/fr/faq/").status_code == 200

    def test_a_moderator_that_presented_its_factor_moderates(self, client, people, forum):
        from community.models import PostStatus

        device = _enrol_totp(people["moderator"])
        client.force_login(people["moderator"])
        _present(client, device)
        assert client.get(FORUM).status_code == 200
        client.post(f"{FORUM}messages/{forum['post'].pk}/moderation/", {"action": "hide", "note": "F8"})
        forum["post"].refresh_from_db()
        assert forum["post"].status == PostStatus.HIDDEN

    def test_nothing_is_owed_without_a_device_where_the_deployment_does_not_require_one(self, client, people):
        client.force_login(people["staff"])
        assert client.get("/fr/faq/").status_code == 200

    def test_a_visitor_and_a_member_are_untouched(self, client, people, unpublished, forum):
        assert client.get(f"/fr/actualites/{unpublished.slug}/").status_code == 404
        assert client.get("/fr/faq/").status_code == 404
        client.force_login(people["person"])
        assert client.get(f"/fr/actualites/{unpublished.slug}/").status_code == 404
        assert client.get(f"{FORUM}discussions/{forum['discussion'].pk}/").status_code == 200, "a member reads"

    def test_a_staff_account_on_a_published_page_owes_nothing(self, client, people, phase3_open):
        """No privilege, no factor: Phase 3 open, the FAQ is everybody's page."""
        _enrol_totp(people["staff"])
        client.force_login(people["staff"])
        assert client.get("/fr/faq/").status_code == 200


# ---------------------------------------------------------------------------------------------
# The rule's reach: every staff branch of a public view asks for it
# ---------------------------------------------------------------------------------------------
APPS = Path(__file__).resolve().parents[2]

#: The tests a public view uses to decide that an account acts as staff.
PRIVILEGE = re.compile(r"\.is_staff\b|\bhas_perm\(|\bis_moderator\(")

#: Modules holding such a test that are NOT a public view's privileged branch, each with its reason. Anything else
#: holding one must call ``require_second_factor``.
NOT_A_PUBLIC_PRIVILEGE = {
    # mounted under the guarded perimeters (the reserved area: config/urls.py), where the middleware already rules —
    # their ``is_staff`` is the reserved area's kill switch
    "academy/views.py": "the reserved area",
    "cases/views.py": "the reserved area",
    "companies/views.py": "the reserved area",
    "forum/governance_views.py": "the reserved area",
    "helpdesk/views.py": "the reserved area",
    "portal/views.py": "the reserved area",
    "portal/services.py": "the reserved area's own presenters",
    # the publication rights, read by the back office's actions (inside /backoffice/)
    "news/services.py": "can_publish — the back office's publish action",
    "living/services.py": "can_publish — the back office's publish action",
    "legal/services.py": "publish/unpublish — the back office's actions",
}


def test_every_staff_branch_of_a_public_view_asks_for_the_second_factor():
    """A future preview or moderator branch that forgets the rule fails here, named."""
    offenders = []
    for path in sorted(APPS.glob("*/*.py")):
        relative = path.relative_to(APPS).as_posix()
        if (
            relative.startswith(("accounts/", "designpreview/"))
            or "/admin" in relative
            or relative.endswith(
                ("admin.py", "policies.py", "permissions.py", "models.py", "seeds.py", "checks.py", "apps.py")
            )
        ):
            continue
        text = path.read_text(encoding="utf-8")
        if not PRIVILEGE.search(text) or relative in NOT_A_PUBLIC_PRIVILEGE:
            continue
        if "require_second_factor" not in text:
            offenders.append(relative)
    assert not offenders, f"a staff branch on a public path without the second factor: {offenders}"
