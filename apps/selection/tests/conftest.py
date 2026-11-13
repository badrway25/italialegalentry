# ruff: noqa: F401 — the imports below ARE the fixtures; pytest collects them by name
"""
Fixtures of the authorised-selection suite.

The shared project fixtures live in ``tests/conftest.py`` and are not visible from an app package,
so they are re-exported here, as ``apps/cases/tests/conftest.py`` does.

The local fixtures build the chain the module is about — an authorisation, an operator entitled to
work under it, a company with a member, a person with a case file in TRAINING — plus a LAPSED
authorisation, because half of this module's rules are about what an expired mandate cannot do.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType, Membership, MembershipRole, Organisation, OrganisationKind
from cases import services as case_services
from cases.models import CasePurpose, CaseStatus
from selection import services
from selection.models import AuthorizedActor
from tests.conftest import (
    _clear_caches,
    before_phase3,
    legal_published,
    phase3_open,
    seeded,
    set_flag,
    superuser,
)

PASSWORD = "Str0ng-Passw0rd-2026!"


@pytest.fixture
def make_user(db):
    User = get_user_model()

    def _make(email: str, *, role: str, account_type: str = AccountType.PERSON, full_name: str = ""):
        user = User.objects.create_user(email=email, password=PASSWORD, account_type=account_type, full_name=full_name)
        roles.assign_role(user, role)
        return user

    return _make


@pytest.fixture
def agency(db):
    return Organisation.objects.create(name="Agence de test", kind=OrganisationKind.COMPANY, city="Rovigo")


@pytest.fixture
def other_agency(db):
    return Organisation.objects.create(
        name="Autre agence de test", kind=OrganisationKind.PROFESSIONAL_FIRM, city="Padoue"
    )


@pytest.fixture
def company(db):
    return Organisation.objects.create(name="Entreprise de test", kind=OrganisationKind.COMPANY, city="Rovigo")


@pytest.fixture
def actor(agency):
    today = timezone.localdate()
    return services.register_actor(
        organisation=agency,
        actor_type="employment_agency",
        jurisdiction="IT-VEN",
        authorisation_reference="TEST-AUT-0001",
        valid_from=today - dt.timedelta(days=30),
        valid_until=today + dt.timedelta(days=365),
    )


@pytest.fixture
def lapsed_actor(other_agency):
    """An authorisation whose window closed yesterday. It must open nothing at all."""
    today = timezone.localdate()
    row = AuthorizedActor(
        organisation=other_agency,
        actor_type="authorised_professional",
        jurisdiction="IT",
        authorisation_reference="TEST-AUT-EXPIRED",
        valid_from=today - dt.timedelta(days=400),
        valid_until=today - dt.timedelta(days=1),
    )
    row.full_clean(exclude=["uuid"])
    row.save()
    return row


@pytest.fixture
def operator(make_user, actor):
    user = make_user("operator@example.test", role=roles.AUTHORISED_ACTOR, account_type=AccountType.PROFESSIONAL)
    services.add_operator(actor, user, function_note="Responsable du processus")
    return user


@pytest.fixture
def lapsed_operator(make_user, lapsed_actor):
    user = make_user("lapsed@example.test", role=roles.AUTHORISED_ACTOR, account_type=AccountType.PROFESSIONAL)
    services.add_operator(lapsed_actor, user, function_note="Responsable du processus")
    return user


@pytest.fixture
def company_user(make_user, company):
    user = make_user("company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    Membership.objects.create(user=user, organisation=company, role=MembershipRole.OWNER)
    return user


@pytest.fixture
def stranger(make_user):
    """An ordinary account with no link whatsoever to the chain. It must see nothing."""
    return make_user("stranger@example.test", role=roles.PERSON)


@pytest.fixture
def person(make_user):
    return make_user("subject@example.test", role=roles.PERSON, full_name="Personne de test")


@pytest.fixture
def case(person):
    row = case_services.open_case(person, purpose=CasePurpose.WORK, pathway_key="work.subordinate")
    case_services.transition(row, CaseStatus.ORIENTED)
    case_services.transition(row, CaseStatus.TRAINING)
    return row


def _mandate(actor, company, **extra):
    return services.issue_mandate(
        actor=actor,
        company=company,
        need_profile="Soudeur qualifié",
        need_sector="Métallurgie",
        need_territory="Rovigo",
        need_headcount=2,
        need_competences=[{"label": "Soudure MIG/MAG", "level": "Autonome"}],
        **extra,
    )


@pytest.fixture
def mandate(actor, company):
    return _mandate(actor, company)


@pytest.fixture
def mandate_factory():
    return _mandate


@pytest.fixture
def process(mandate, case, operator):
    return services.open_process(mandate=mandate, case=case, operator=operator)
