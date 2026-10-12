# ruff: noqa: F811 — pytest fixtures legitimately shadow the imported shared fixture names
from __future__ import annotations

import pytest

from accounts import roles
from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind
from core import clock

# Shared project fixtures (tests/conftest.py is not a root conftest, so import them explicitly).
from tests.conftest import (  # noqa: F401
    _clear_caches,
    before_phase3,
    client_ar,
    client_fr,
    legal_published,
    person_user,
    phase3_open,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)


@pytest.fixture
def terms_user(user_factory):
    """A person account that accepted the Conditions (required for the reserved area uploads)."""
    return user_factory(
        "alice@example.test", role=roles.PERSON, full_name="Alice Martin", terms_accepted_at=clock.now()
    )


@pytest.fixture
def other_user(user_factory):
    return user_factory("bob@example.test", role=roles.PERSON, full_name="Bob Durand", terms_accepted_at=clock.now())


@pytest.fixture
def organisation(db, terms_user):
    org = Organisation.objects.create(name="Acme Formazione", kind=OrganisationKind.COMPANY, created_by=terms_user)
    Membership.objects.create(user=terms_user, organisation=org, role=MembershipRole.OWNER)
    return org
