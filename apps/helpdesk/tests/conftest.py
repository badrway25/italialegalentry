# ruff: noqa: F401, F811 — the imports below ARE the fixtures; pytest collects them by name,
#                            and a fixture that takes another one by name is not a redefinition
"""
Fixtures of the help-desk test-suite.

The shared project fixtures live in ``tests/conftest.py`` and are not visible from an app package,
so they are re-exported here, as ``apps/cases/tests/conftest.py`` does.
"""

from __future__ import annotations

import pytest

from tests.conftest import (
    _clear_caches,
    before_phase3,
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
def other_person(user_factory):
    """A second person. The one whose requests nobody else may ever see."""
    from accounts import roles

    return user_factory("other-person@example.test", role=roles.PERSON)


@pytest.fixture
def professional(user_factory):
    from accounts import roles

    return user_factory("pro@example.test", role=roles.PROFESSIONAL)


@pytest.fixture
def other_professional(user_factory):
    from accounts import roles

    return user_factory("pro-2@example.test", role=roles.PROFESSIONAL)


@pytest.fixture
def operator(user_factory):
    from accounts import roles

    return user_factory("operator@example.test", role=roles.OPERATOR)


@pytest.fixture
def administrator(user_factory):
    """An administrator by ROLE, not a superuser: the account the object policies actually judge."""
    from accounts import roles

    return user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)


@pytest.fixture
def reserved_area_on(db):
    """The reserved-area kill switch must be on for any authenticated page to render."""
    from core.models import SiteSettings

    settings_row = SiteSettings.load()
    settings_row.reserved_area_enabled = True
    settings_row.save()
    return settings_row


@pytest.fixture
def ticket(db, person_user):
    from helpdesk import services

    return services.open_ticket(
        person_user,
        subject="Validité de mon attestation de langue",
        question="Mon attestation date de dix-huit mois : est-elle encore recevable ?",
    )


@pytest.fixture
def assigned_ticket(db, ticket, professional, operator):
    """A request escalated, confided under a mandate, and taken in review."""
    from helpdesk import services

    services.request_professional_review(ticket, actor=ticket.person)
    services.assign(
        ticket,
        professional,
        mandate_note="Examiner la recevabilité de l’attestation de langue.",
        role_label="Avocat — droit de l’immigration",
        actor=operator,
    )
    services.take_in_review(ticket, actor=professional)
    return ticket
