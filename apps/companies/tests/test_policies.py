"""
Object-level authorisation of the company workspace — deny by default.

The rebase directive §61 requires these explicitly: company A does not reach company B, a member is
not a responsible, an unassigned account reaches nothing, and an identifier discovered by hand never
bypasses the rules.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.utils import timezone

from accounts import roles
from accounts.models import Membership, MembershipRole
from accounts.permissions import can
from companies import services
from companies.models import ActorRole, CompanyProfile, NeedStatus

pytestmark = pytest.mark.django_db


def test_a_company_reads_and_writes_only_its_own_profile(company_factory) -> None:
    alpha, alpha_user = company_factory("alpha")
    beta, beta_user = company_factory("beta")
    assert can(alpha_user, "view", alpha) is True
    assert can(alpha_user, "change", alpha) is True
    assert can(alpha_user, "view", beta) is False
    assert can(alpha_user, "change", beta) is False


def test_a_plain_member_reads_but_does_not_write(company_factory, user_factory) -> None:
    alpha, _owner = company_factory("alpha")
    member = user_factory("member@example.test", role=roles.COMPANY)
    Membership.objects.create(user=member, organisation=alpha.organisation, role=MembershipRole.MEMBER)
    assert can(member, "view", alpha) is True
    assert can(member, "change", alpha) is False


def test_a_company_cannot_reach_another_company_s_need_by_its_reference(company_factory, need_factory) -> None:
    """An identifier discovered by hand must never bypass the rules."""
    from django.http import Http404

    alpha, alpha_user = company_factory("alpha")
    beta, _beta_user = company_factory("beta")
    beta_need = need_factory(beta, title="Besoin de beta")
    assert can(alpha_user, "view", beta_need) is False
    with pytest.raises(Http404):
        services.get_own_need(alpha_user, beta_need.reference)


def test_an_unknown_reference_and_a_forbidden_one_answer_the_same_way(company_factory, need_factory) -> None:
    """Same 404 in both cases: a differently worded refusal is a disclosure."""
    from django.http import Http404

    alpha, alpha_user = company_factory("alpha")
    beta, _beta_user = company_factory("beta")
    forbidden = need_factory(beta)
    with pytest.raises(Http404):
        services.get_own_need(alpha_user, forbidden.reference)
    with pytest.raises(Http404):
        services.get_own_need(alpha_user, "BDOESNOTEX")


def test_a_need_taken_in_charge_is_no_longer_editable_by_the_company(
    company_factory, need_factory, user_factory, superuser
) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.transition(need, NeedStatus.UNDER_REVIEW, actor=superuser)
    assert can(user, "change", need) is True

    actor = user_factory("actor@example.test", role=roles.AUTHORISED_ACTOR)
    services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 2/2026",
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=30),
        actor=superuser,
    )
    services.transition(need, NeedStatus.IN_PROGRESS, actor=superuser)
    need.refresh_from_db()
    assert can(user, "change", need) is False
    assert can(user, "withdraw", need) is False


def test_the_designated_actor_reads_the_need_but_writes_nothing(
    company_factory, need_factory, user_factory, superuser
) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile)
    actor = user_factory("actor@example.test", role=roles.AUTHORISED_ACTOR)
    services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 3/2026",
        actor=superuser,
    )
    need = need.__class__.objects.prefetch_related("assignments").get(pk=need.pk)
    assert can(actor, "view", need) is True
    assert can(actor, "change", need) is False
    assert can(actor, "view", need.company) is False


def test_a_revoked_actor_loses_the_need_immediately(company_factory, need_factory, user_factory, superuser) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile)
    actor = user_factory("actor@example.test", role=roles.AUTHORISED_ACTOR)
    assignment = services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 4/2026",
        actor=superuser,
    )
    services.revoke_actor(assignment, actor=superuser)
    assert need.__class__.objects.readable_by(actor).count() == 0


def test_an_expired_authorisation_stops_reading(company_factory, need_factory, user_factory, superuser) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile)
    actor = user_factory("actor@example.test", role=roles.AUTHORISED_ACTOR)
    services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 5/2026",
        authorisation_valid_until=timezone.localdate() - dt.timedelta(days=1),
        actor=superuser,
    )
    assert need.__class__.objects.readable_by(actor).count() == 0


def test_a_person_account_reaches_nothing(company_factory, need_factory, person_user) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile)
    assert can(person_user, "view", need) is False
    assert can(person_user, "view", profile) is False
    assert CompanyProfile.objects.readable_by(person_user).count() == 0


def test_project_staff_get_no_platform_side_company_list(company_factory, staff_user) -> None:
    company_factory("alpha")
    assert CompanyProfile.objects.readable_by(staff_user).count() == 0


def test_every_model_of_this_app_has_a_registered_policy() -> None:
    """Deny by default only holds if every model actually declares its rule."""
    from django.apps import apps as django_apps

    import companies.policies  # noqa: F401 — the import IS the registration
    from accounts.permissions import _POLICIES

    models = set(django_apps.get_app_config("companies").get_models())
    # The two taxonomies are configuration, not data of a party: they carry no policy and are not
    # exposed as objects anywhere — they are rendered as labels inside an object the caller may read.
    from companies.models import Sector, Territory

    unregistered = {model.__name__ for model in models - {Sector, Territory} if model not in _POLICIES}
    assert unregistered == set(), f"models without an object-level policy: {unregistered}"
