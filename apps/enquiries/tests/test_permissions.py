"""Object-level policy: owner sees own, staff sees all, everybody else denied (IDOR)."""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from accounts import roles
from accounts.permissions import can, require
from enquiries import services

pytestmark = [pytest.mark.django_db, pytest.mark.security]


def test_person_a_cannot_view_person_b_submission(user_factory, make_company, make_contact, make_proposal):
    a = user_factory("a@example.test", role=roles.PERSON)
    b = user_factory("b@example.test", role=roles.COMPANY)
    own = make_company(email="a@example.test", owner=a)
    other = make_company(email="b@example.test", owner=b)
    assert can(a, "view", own) is True
    assert can(a, "view", other) is False
    assert can(b, "view", own) is False
    assert can(a, "view", make_contact(owner=b)) is False
    assert can(a, "view", make_proposal(owner=a)) is True
    with pytest.raises(PermissionDenied):
        require(a, "view", other)


def test_owner_cannot_change_or_export(user_factory, make_company):
    a = user_factory("a@example.test", role=roles.PERSON)
    own = make_company(owner=a)
    for action in ("change", "export", "anonymise", "delete"):
        assert can(a, action, own) is False


def test_anonymous_and_unowned_denied(make_company, user_factory):
    obj = make_company()  # no owner (anonymous submission)
    assert can(AnonymousUser(), "view", obj) is False
    assert can(None, "view", obj) is False
    assert can(user_factory("x@example.test"), "view", obj) is False


def test_staff_roles_see_everything(user_factory, make_company, staff_user, superuser):
    other = make_company(owner=user_factory("owner@example.test"))
    assert can(staff_user, "view", other) is True
    assert can(staff_user, "change", other) is True
    assert can(superuser, "view", other) is True
    admin = user_factory("admin2@example.test", role=roles.ADMINISTRATOR)
    assert can(admin, "view", other) is True
    moderator = user_factory("mod@example.test", role=roles.MODERATOR)
    assert can(moderator, "view", other) is False, "community moderators must not read enquiries"


def test_anonymised_submission_no_longer_visible_to_owner(user_factory, make_company):
    a = user_factory("a@example.test", role=roles.PERSON)
    own = make_company(owner=a)
    assert can(a, "view", own) is True
    services.anonymise(own)
    assert can(a, "view", own) is False


def test_inactive_user_denied(user_factory, make_company):
    a = user_factory("a@example.test", role=roles.PERSON)
    own = make_company(owner=a)
    a.is_active = False
    a.save()
    assert can(a, "view", own) is False
