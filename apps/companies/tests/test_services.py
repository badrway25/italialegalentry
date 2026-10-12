"""
The domain services: transmission, transitions, the authorisation rule of CR-03, the audit trail
and the aggregate.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from accounts import roles
from audit.models import AuditEvent
from companies import services
from companies.models import ActorRole, CompanyNeed, NeedStatus

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# Creation and edition
# ---------------------------------------------------------------------------------------------
def test_create_need_records_an_opening_event_and_an_audit_row(company_factory, territory, sector) -> None:
    profile, user = company_factory("alpha")
    need = services.create_need(
        profile,
        data={"title": "Maintenance des lignes", "territory": territory, "sector": sector, "headcount": 2},
        actor=user,
    )
    assert need.status == NeedStatus.DRAFT
    assert need.events.count() == 1
    assert AuditEvent.objects.filter(action="companies.need.created", target_id=str(need.pk)).exists()


def test_set_skills_replaces_the_matrix_and_deduplicates(company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.set_skills(
        need,
        mandatory=["Soudure TIG", "Soudure TIG", "  Lecture de plan  "],
        preferred=["Automatisme"],
        actor=user,
    )
    assert [row.label for row in need.mandatory_skills()] == ["Soudure TIG", "Lecture de plan"]
    assert [row.label for row in need.preferred_skills()] == ["Automatisme"]


# ---------------------------------------------------------------------------------------------
# Transmission requires a VERIFIED company (REQ-B2B-01)
# ---------------------------------------------------------------------------------------------
def test_an_unverified_company_cannot_transmit(company_factory, need_factory) -> None:
    profile, user = company_factory("pending", verified=False)
    need = need_factory(profile)
    with pytest.raises(PermissionDenied):
        services.submit(need, actor=user)
    need.refresh_from_db()
    assert need.status == NeedStatus.DRAFT


def test_an_incomplete_need_cannot_be_transmitted(company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile, complete=False)
    with pytest.raises(PermissionDenied):
        services.submit(need, actor=user)


def test_a_verified_company_transmits_a_complete_need(company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    need.refresh_from_db()
    assert need.status == NeedStatus.SUBMITTED
    assert need.submitted_at is not None
    assert need.events.filter(to_status=NeedStatus.SUBMITTED).exists()
    assert AuditEvent.objects.filter(action="companies.need.transition").exists()


def test_the_company_withdraws_its_own_need(company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.withdraw(need, actor=user, reason="Poste pourvu autrement.")
    need.refresh_from_db()
    assert need.status == NeedStatus.WITHDRAWN
    assert need.closed_at is not None


# ---------------------------------------------------------------------------------------------
# Declared transitions only
# ---------------------------------------------------------------------------------------------
def test_an_undeclared_transition_is_refused(company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    with pytest.raises(ValidationError):
        services.transition(need, NeedStatus.CLOSED, actor=user)
    need.refresh_from_db()
    assert need.status == NeedStatus.DRAFT


def test_a_hold_must_be_motivated(company_factory, need_factory, superuser) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    with pytest.raises(ValidationError):
        services.transition(need, NeedStatus.ON_HOLD, actor=superuser, note="   ")
    services.transition(need, NeedStatus.ON_HOLD, actor=superuser, note="Documents manquants.")
    need.refresh_from_db()
    assert need.status == NeedStatus.ON_HOLD
    assert need.hold_reason == "Documents manquants."


# ---------------------------------------------------------------------------------------------
# CR-03 — no taking in charge without a LIVE authorisation
# ---------------------------------------------------------------------------------------------
def _authorised_actor(user_factory, email: str):
    actor = user_factory(email, role=roles.AUTHORISED_ACTOR)
    return actor


def test_a_need_cannot_be_taken_in_charge_without_an_authorised_actor(company_factory, need_factory, superuser) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.transition(need, NeedStatus.UNDER_REVIEW, actor=superuser)
    with pytest.raises(ValidationError):
        services.transition(need, NeedStatus.IN_PROGRESS, actor=superuser)


def test_an_assignment_without_a_reference_is_not_an_authorisation(
    company_factory, need_factory, user_factory, superuser
) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    actor = _authorised_actor(user_factory, "actor@example.test")
    with pytest.raises(ValidationError):
        services.assign_actor(need, assignee=actor, role=ActorRole.AUTHORISED_ACTOR, actor=superuser)


def test_an_expired_authorisation_does_not_allow_taking_in_charge(
    company_factory, need_factory, user_factory, superuser
) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.transition(need, NeedStatus.UNDER_REVIEW, actor=superuser)
    actor = _authorised_actor(user_factory, "actor@example.test")
    services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 1/2026",
        authorisation_valid_until=timezone.localdate() - dt.timedelta(days=1),
        actor=superuser,
    )
    with pytest.raises(ValidationError):
        services.transition(need, NeedStatus.IN_PROGRESS, actor=superuser)


def test_a_live_authorisation_allows_taking_in_charge_and_names_the_actor(
    company_factory, need_factory, user_factory, superuser
) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    services.submit(need, actor=user)
    services.transition(need, NeedStatus.UNDER_REVIEW, actor=superuser)
    actor = _authorised_actor(user_factory, "actor@example.test")
    from accounts.models import Organisation, OrganisationKind

    agency = Organisation.objects.create(name="Agenzia autorizzata", kind=OrganisationKind.OTHER)
    services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        organisation=agency,
        authorisation_reference="Albo — prot. 1/2026",
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=30),
        actor=superuser,
    )
    services.transition(need, NeedStatus.IN_PROGRESS, actor=superuser)
    need.refresh_from_db()
    assert need.status == NeedStatus.IN_PROGRESS
    named = services.responsible_for(need)
    assert named and named[0]["name"] == "Agenzia autorizzata"
    assert named[0]["is_authorised_actor"] is True


def test_a_company_cannot_assign_an_actor_to_its_own_need(company_factory, need_factory, user_factory) -> None:
    """An assignment a company could write for itself would be a self-issued authorisation."""
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    actor = _authorised_actor(user_factory, "actor@example.test")
    with pytest.raises(PermissionDenied):
        services.assign_actor(
            need,
            assignee=actor,
            role=ActorRole.AUTHORISED_ACTOR,
            authorisation_reference="Auto-délivrée",
            actor=user,
        )


def test_a_named_actor_never_prints_an_e_mail_address(company_factory, need_factory, user_factory, superuser) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile)
    actor = user_factory("actor@example.test", role=roles.AUTHORISED_ACTOR)
    assignment = services.assign_actor(
        need,
        assignee=actor,
        role=ActorRole.AUTHORISED_ACTOR,
        authorisation_reference="Albo — prot. 1/2026",
        actor=superuser,
    )
    assert "@" not in assignment.display_name


# ---------------------------------------------------------------------------------------------
# The next action — one priority
# ---------------------------------------------------------------------------------------------
def test_next_action_points_at_the_verification_while_it_is_pending(company_factory) -> None:
    profile, _user = company_factory("pending", verified=False)
    action = services.next_action(profile, [])
    assert action is not None
    assert action.is_for_someone_else is True
    assert action.responsible_actor == "project_team"


def test_next_action_names_what_is_missing_on_an_incomplete_draft(company_factory, need_factory) -> None:
    profile, _user = company_factory("alpha")
    need = need_factory(profile, complete=False)
    action = services.next_action(profile, [need])
    assert action is not None
    assert "territoire" in action.detail


# ---------------------------------------------------------------------------------------------
# Aggregation — counts only (REQ-B2B-05)
# ---------------------------------------------------------------------------------------------
def test_the_aggregate_is_refused_to_a_company(company_factory) -> None:
    _profile, user = company_factory("alpha")
    with pytest.raises(PermissionDenied):
        services.needs_aggregate(user)


def test_the_aggregate_counts_by_territory_and_sector_and_excludes_drafts(
    company_factory, need_factory, staff_user
) -> None:
    profile, user = company_factory("alpha")
    transmitted = need_factory(profile, title="Besoin transmis", headcount=4)
    services.submit(transmitted, actor=user)
    need_factory(profile, title="Besoin en brouillon", headcount=7)

    data = services.needs_aggregate(staff_user)
    assert data["total_needs"] == 1
    assert data["total_headcount"] == 4
    assert data["by_territory"][0]["label"] == "Vénétie"
    assert data["by_territory"][0]["needs"] == 1
    assert data["by_sector"][0]["needs"] == 1


def test_the_aggregate_returns_no_identifier_and_no_name(company_factory, need_factory, staff_user) -> None:
    profile, user = company_factory("alpha")
    need = need_factory(profile, title="Un intitulé reconnaissable")
    services.submit(need, actor=user)
    payload = repr(services.needs_aggregate(staff_user))
    assert "Un intitulé reconnaissable" not in payload
    assert profile.legal_name not in payload
    assert need.reference not in payload


# ---------------------------------------------------------------------------------------------
# Querysets carry the authorisation
# ---------------------------------------------------------------------------------------------
def test_a_company_never_sees_another_company_s_needs(company_factory, need_factory) -> None:
    alpha, alpha_user = company_factory("alpha")
    beta, beta_user = company_factory("beta")
    need_factory(alpha, title="Besoin alpha")
    need_factory(beta, title="Besoin beta")

    visible = CompanyNeed.objects.readable_by(alpha_user)
    assert visible.count() == 1
    assert visible.first().company_id == alpha.pk


def test_an_anonymous_caller_sees_nothing(company_factory, need_factory) -> None:
    from django.contrib.auth.models import AnonymousUser

    alpha, _user = company_factory("alpha")
    need_factory(alpha)
    assert CompanyNeed.objects.readable_by(AnonymousUser()).count() == 0


def test_project_staff_do_not_get_a_platform_side_list_of_every_need(company_factory, need_factory, staff_user) -> None:
    """Supervision happens in the back-office, where it is role-checked and audited."""
    alpha, _user = company_factory("alpha")
    need_factory(alpha)
    assert CompanyNeed.objects.readable_by(staff_user).count() == 0


# ---------------------------------------------------------------------------------------------
# Declaring a company — the verification it opens must be the one this workspace reads
# ---------------------------------------------------------------------------------------------
def test_declaring_a_company_opens_a_verification_declared_as_a_company(user_factory, sector) -> None:
    from accounts.models import AccountType, AccountVerification

    user = user_factory("fondateur@example.test", role=roles.PERSON)
    profile = services.declare_company(
        user,
        data={
            "legal_name": "Officina di prova S.r.l.",
            "trade_name": "",
            "registration_number": "RM-DECL-01",
            "vat_number": "",
            "sector": sector,
            "size": "small",
            "year_founded": 2010,
            "contact_name": "Référent de test",
            "contact_function": "Direction",
            "contact_email": "referent@example.test",
            "contact_phone": "",
            "address_line": "",
            "postal_code": "",
            "city": "Rovigo",
            "province": "",
            "country": "IT",
            "website": "",
        },
    )
    row = AccountVerification.objects.get(user=user)
    assert row.declared_type == AccountType.COMPANY
    assert profile.is_verified is False


def test_an_account_declared_as_another_actor_cannot_open_a_company_it_could_never_verify(user_factory, sector) -> None:
    """
    ``AccountVerification`` is ONE row per account. An account that already declared another type
    keeps that row, so no company verification would ever be opened — and if that row were already
    approved, reading it would verify a company nobody verified. Refuse plainly instead.
    """
    from accounts.models import AccountType, AccountVerification, VerificationStatus
    from companies.models import CompanyProfile

    user = user_factory("avocat@example.test", role=roles.PERSON)
    AccountVerification.objects.create(
        user=user, declared_type=AccountType.PROFESSIONAL, status=VerificationStatus.APPROVED
    )
    with pytest.raises(ValidationError):
        services.declare_company(
            user,
            data={
                "legal_name": "Studio che non deve nascere S.r.l.",
                "trade_name": "",
                "registration_number": "",
                "vat_number": "",
                "sector": sector,
                "size": "",
                "year_founded": None,
                "contact_name": "Référent",
                "contact_function": "Direction",
                "contact_email": "referent@example.test",
                "contact_phone": "",
                "address_line": "",
                "postal_code": "",
                "city": "Rovigo",
                "province": "",
                "country": "IT",
                "website": "",
            },
        )
    assert CompanyProfile.objects.count() == 0
    assert services.company_for(user) is None
