# ruff: noqa: F401 — the imports below ARE the fixtures; pytest collects them by name
"""
Fixtures of the notification test-suite.

The shared project fixtures live in ``tests/conftest.py`` and are not visible from an app package,
so the ones this suite needs are re-exported here, as the other app suites do.
"""

from __future__ import annotations

import datetime as dt

import pytest

from cases import services as case_services
from cases.models import CasePurpose, ResponsibleActor
from tests.conftest import _clear_caches, superuser


@pytest.fixture
def person(django_user_model):
    return django_user_model.objects.create_user(email="persona@example.test", password="x")


@pytest.fixture
def other_person(django_user_model):
    return django_user_model.objects.create_user(email="altra@example.test", password="x")


@pytest.fixture
def professional(django_user_model):
    return django_user_model.objects.create_user(email="prof@example.test", password="x")


@pytest.fixture
def case(person):
    return case_services.open_case(person, purpose=CasePurpose.WORK, pathway_key="work.salaried")


@pytest.fixture
def today():
    """A fixed date. Tests about deadlines must be about dates, not about the day they are run."""
    return dt.date(2026, 10, 1)


@pytest.fixture
def item_factory(case):
    def _make(*, due_date=None, requirement="Passeport en cours de validité", status=None, actor=None, target=None):
        item = case_services.add_checklist_item(
            target or case,
            requirement=requirement,
            responsible_actor=actor or ResponsibleActor.PERSON,
            due_date=due_date,
        )
        if status:
            item.status = status
            item.save(update_fields=["status", "updated_at"])
        return item

    return _make
