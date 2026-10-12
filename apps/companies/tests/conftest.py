# ruff: noqa: F401 — the imports below ARE the fixtures; pytest collects them by name
"""
Fixtures of the company-workspace test-suite.

The shared project fixtures live in ``tests/conftest.py`` and are not visible from an app package,
so they are re-exported here, as ``apps/cases/tests/conftest.py`` does.
"""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts import roles
from accounts.models import (
    AccountType,
    AccountVerification,
    Membership,
    MembershipRole,
    Organisation,
    OrganisationKind,
    VerificationStatus,
)
from companies.models import CompanyNeed, CompanyProfile, NeedSkill, Sector, SkillLevel, Territory
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

PASSWORD = "Str0ng-Passw0rd-2026!"


@pytest.fixture
def sector(db) -> Sector:
    # get_or_create: the taxonomy seed may already have created this row (the ``seeded`` fixture),
    # and a fixture that fights the seed tests the fixture, not the product.
    row, _created = Sector.objects.get_or_create(
        code="batiment", defaults={"label_fr": "Bâtiment et travaux publics", "order": 10}
    )
    return row


@pytest.fixture
def territory(db) -> Territory:
    row, _created = Territory.objects.get_or_create(
        code="veneto", defaults={"label_fr": "Vénétie", "country": "IT", "order": 10}
    )
    return row


@pytest.fixture
def company_factory(db, sector):
    """A company, its organisation, a responsible account and (optionally) its verification."""

    User = get_user_model()

    def _make(slug: str = "alpha", *, verified: bool = True, email: str | None = None):
        email = email or f"{slug}@example.test"
        user = User.objects.create_user(email=email, password=PASSWORD, account_type=AccountType.COMPANY)
        roles.assign_role(user, roles.COMPANY)
        organisation = Organisation.objects.create(
            name=f"Organisation {slug}", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
        )
        Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
        AccountVerification.objects.create(
            user=user,
            declared_type=AccountType.COMPANY,
            status=VerificationStatus.APPROVED if verified else VerificationStatus.PENDING,
            decided_at=timezone.now() if verified else None,
        )
        profile = CompanyProfile.objects.create(
            organisation=organisation,
            legal_name=f"Société {slug} S.r.l.",
            registration_number=f"RM-{slug.upper()}-01",
            sector=sector,
            contact_name="Référent de test",
            contact_function="Responsable des ressources humaines",
            contact_email=f"referent-{slug}@example.test",
            city="Rovigo",
            country="IT",
        )
        return profile, user

    return _make


@pytest.fixture
def company(company_factory):
    profile, _user = company_factory("alpha")
    return profile


@pytest.fixture
def company_user(company_factory):
    _profile, user = company_factory("beta")
    return user


@pytest.fixture
def need_factory(db, territory, sector):
    def _make(company: CompanyProfile, *, title: str = "Maintenance des lignes", complete: bool = True, **extra):
        need = CompanyNeed.objects.create(
            company=company,
            title=title,
            territory=territory if complete else None,
            sector=sector if complete else None,
            professional_profile="Technicien de maintenance" if complete else "",
            duties="Entretien préventif et correctif des lignes." if complete else "",
            headcount=extra.pop("headcount", 2),
            **extra,
        )
        if complete:
            NeedSkill.objects.create(need=need, label="Mécanique industrielle", level=SkillLevel.MANDATORY)
        return need

    return _make
