# Re-export the project-wide fixtures (tests/conftest.py applies only below tests/).
import pytest

from accounts import roles
from community.models import Discussion, Membership, MembershipStatus, ParticipantCategory, Post, PostStatus, Room
from core import clock
from tests.conftest import *  # noqa: F401,F403
from tests.conftest import _clear_caches  # noqa: F401


@pytest.fixture
def flag_on(set_flag):
    return set_flag("virtual_forum", True)


@pytest.fixture
def rooms(db):
    # update_or_create so the fixture coexists with the ``seeded`` rooms (same slugs)
    common, _ = Room.objects.update_or_create(
        slug="espace-commun",
        defaults={"name_fr": "Espace commun", "allowed_categories": [], "order": 1, "published": True},
    )
    companies, _ = Room.objects.update_or_create(
        slug="entreprises",
        defaults={
            "name_fr": "Entreprises",
            "allowed_categories": [ParticipantCategory.COMPANY],
            "order": 2,
            "published": True,
        },
    )
    institutions, _ = Room.objects.update_or_create(
        slug="institutions",
        defaults={
            "name_fr": "Institutions",
            "allowed_categories": [ParticipantCategory.INSTITUTION],
            "order": 3,
            "published": True,
            "is_moderated": False,
        },
    )
    Room.objects.update_or_create(
        slug="brouillon", defaults={"name_fr": "Brouillon", "allowed_categories": [], "order": 9, "published": False}
    )
    return {"common": common, "companies": companies, "institutions": institutions}


@pytest.fixture
def member_factory(user_factory):
    def _make(email, category=ParticipantCategory.COMPANY, status=MembershipStatus.APPROVED, **extra):
        user = user_factory(email, role=roles.COMPANY, full_name=extra.pop("full_name", ""))
        membership = Membership.objects.create(
            user=user,
            category=category,
            status=status,
            organisation=extra.pop("organisation", ""),
            approved_at=clock.now() if status == MembershipStatus.APPROVED else None,
            **extra,
        )
        return membership

    return _make


@pytest.fixture
def company_member(member_factory):
    return member_factory("company@example.test", ParticipantCategory.COMPANY, trusted=True)


@pytest.fixture
def new_member(member_factory):
    return member_factory("newbie@example.test", ParticipantCategory.COMPANY)


@pytest.fixture
def institution_member(member_factory):
    return member_factory("institution@example.test", ParticipantCategory.INSTITUTION, trusted=True)


@pytest.fixture
def moderator(user_factory):
    return user_factory("moderator@example.test", role=roles.MODERATOR)


@pytest.fixture
def discussion(rooms, company_member):
    d = Discussion.objects.create(
        room=rooms["common"], author=company_member, title="Première discussion", last_activity_at=clock.now()
    )
    Post.objects.create(discussion=d, author=company_member, body="Premier message", status=PostStatus.VISIBLE)
    return d
