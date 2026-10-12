"""The configurable taxonomy, the personal-data export and the back-office surface."""

from __future__ import annotations

import pytest

from companies.models import Sector, Territory

pytestmark = pytest.mark.django_db


def test_the_taxonomies_are_configuration_rows_not_a_python_list(seeded) -> None:
    """Technical Blueprint §20: a taxonomy an administrator cannot reach is not configurable."""
    assert Sector.objects.active().count() >= 10
    assert Territory.objects.active().count() >= 10
    assert Sector.objects.filter(code="batiment").exists()
    assert Territory.objects.filter(code="veneto", country="IT").exists()


def test_the_seed_is_idempotent(seeded) -> None:
    from django.core.management import call_command

    before = (Sector.objects.count(), Territory.objects.count())
    call_command("seed_all", verbosity=0)
    assert (Sector.objects.count(), Territory.objects.count()) == before


def test_an_editorial_change_survives_a_reseed(seeded) -> None:
    from django.core.management import call_command

    row = Sector.objects.get(code="batiment")
    row.label_fr = "Bâtiment, travaux publics et second œuvre"
    row.save(update_fields=["label_fr"])
    call_command("seed_all", verbosity=0)
    row.refresh_from_db()
    assert row.label_fr == "Bâtiment, travaux publics et second œuvre"


def test_the_personal_data_export_carries_the_company_and_its_needs(company_factory, need_factory) -> None:
    """GDPR art. 15: the contact's data are personal data, and the account may have a copy."""
    from accounts.services import export_user_data

    profile, user = company_factory("alpha")
    need = need_factory(profile, title="Un besoin exporté")
    data = export_user_data(user)
    assert "companies" in data
    exported = data["companies"]
    assert exported["companies"][0]["legal_name"] == profile.legal_name
    assert exported["companies"][0]["contact_function"] == profile.contact_function
    assert exported["needs"][0]["reference"] == need.reference


def test_the_export_of_one_account_never_contains_another_company(company_factory, need_factory) -> None:
    from accounts.services import export_user_data

    alpha, alpha_user = company_factory("alpha")
    beta, _beta_user = company_factory("beta")
    need_factory(beta, title="Besoin de beta")
    payload = repr(export_user_data(alpha_user)["companies"])
    assert beta.legal_name not in payload
    assert "Besoin de beta" not in payload


def test_the_back_office_never_edits_a_state_by_hand() -> None:
    """A state written straight into the admin form would bypass the transition table and the audit."""
    from django.contrib import admin

    from companies.models import CompanyNeed, NeedEvent

    need_admin = admin.site._registry[CompanyNeed]
    assert "status" in need_admin.readonly_fields
    assert "reference" in need_admin.readonly_fields

    event_admin = admin.site._registry[NeedEvent]
    assert event_admin.has_add_permission(None) is False
    assert event_admin.has_change_permission(None) is False


def test_the_back_office_cannot_take_a_need_in_charge_without_an_authorisation(
    company_factory, need_factory, superuser
) -> None:
    """CR-03, from the back-office too: the rule is in the domain, not in one screen."""
    from django.contrib import admin
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.test import RequestFactory

    from companies import services
    from companies.models import CompanyNeed, NeedStatus

    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.transition(need, NeedStatus.UNDER_REVIEW, actor=superuser)

    request = RequestFactory().post("/backoffice/")
    request.user = superuser
    request.session = {}
    request._messages = FallbackStorage(request)

    need_admin = admin.site._registry[CompanyNeed]
    need_admin.action_take_in_charge(request, CompanyNeed.objects.filter(pk=need.pk))
    need.refresh_from_db()
    assert need.status == NeedStatus.UNDER_REVIEW, "a need was taken in charge with no authorised actor"
