"""
Progressive disclosure of identity — the good idea of the previous platform, with its three
defects removed (previous-platform audit §3.1 and part 2 §5, private register).

The previous platform: the platform's own staff decided, from an admin screen, whether a company
could see a candidate's identity. No consent from the person, no purpose, no duration, no legal
basis; and once communicated, communicated for ever.

What must hold here, and is tested below:
  * a company sees NO identity without a recorded consent of the person;
  * the actor asks, the person decides — nobody decides for them, including an administrator;
  * the authorisation expires by itself;
  * withdrawal is immediate;
  * every access is recorded, one row per access, and the person can read that list.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from accounts.permissions import can
from audit.models import AuditEvent
from selection import services
from selection.models import (
    MAX_DISCLOSURE_DAYS,
    DisclosureStatus,
    IdentityAccess,
    IdentityDisclosure,
    IdentityField,
    SelectionOutcome,
)

pytestmark = pytest.mark.django_db

FIELDS = [IdentityField.FULL_NAME, IdentityField.CONTACT_EMAIL]


@pytest.fixture
def disclosure(process, operator):
    return services.request_identity_disclosure(
        process,
        operator=operator,
        purpose="Prise de contact en vue d’un entretien conduit par l’acteur autorisé",
        fields=FIELDS,
        duration_days=30,
    )


# ---------------------------------------------------------------------------------------------
# A company sees no person without a recorded consent
# ---------------------------------------------------------------------------------------------
def test_a_company_sees_no_identity_without_a_recorded_consent(disclosure, company_user):
    assert disclosure.status == DisclosureStatus.REQUESTED
    assert disclosure.is_active() is False
    assert services.read_identity(disclosure, user=company_user) is None
    assert can(company_user, "read_identity", disclosure) is False
    assert IdentityAccess.objects.count() == 0


def test_a_company_sees_no_identity_before_anyone_has_even_asked(process, company_user):
    page = services.process_page(company_user, process)
    assert page.live_disclosure is None
    assert page.view.can_read_identity is False


def test_the_identity_reaches_the_company_only_after_the_person_consents(disclosure, company_user, person):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    assert disclosure.is_active() is True
    assert disclosure.consent is not None
    assert disclosure.consent.user_id == person.pk
    assert disclosure.consent.consent_text.text, "the record points at the wording the person read"

    disclosed = services.read_identity(disclosure, user=company_user)
    assert disclosed is not None
    assert person.email in disclosed.values()


def test_the_consent_carries_a_purpose_a_duration_and_a_legal_basis(disclosure, person):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    assert disclosure.purpose
    assert disclosure.expires_at is not None
    assert disclosure.legal_basis == "gdpr_6_1_a_consent"
    expected = disclosure.decided_at + dt.timedelta(days=disclosure.duration_days)
    assert abs((disclosure.expires_at - expected).total_seconds()) < 2


def test_only_the_named_fields_are_disclosed(disclosure, person, company_user):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    disclosed = services.read_identity(disclosure, user=company_user)
    assert len(disclosed) == len(FIELDS)
    assert str(IdentityField.PREFERRED_LANGUAGE.label) not in disclosed


def test_a_field_outside_the_register_cannot_be_requested(process, operator):
    with pytest.raises(ValidationError):
        services.request_identity_disclosure(
            process,
            operator=operator,
            purpose="Finalité",
            fields=["date_of_birth", "nationality"],
            duration_days=10,
        )


def test_a_disclosure_without_a_duration_is_refused(process, operator):
    with pytest.raises(ValidationError):
        services.request_identity_disclosure(
            process, operator=operator, purpose="Finalité", fields=FIELDS, duration_days=0
        )
    with pytest.raises(ValidationError):
        services.request_identity_disclosure(
            process,
            operator=operator,
            purpose="Finalité",
            fields=FIELDS,
            duration_days=MAX_DISCLOSURE_DAYS + 1,
        )


def test_a_disclosure_without_a_purpose_is_refused(process, operator):
    with pytest.raises(ValidationError):
        services.request_identity_disclosure(process, operator=operator, purpose="   ", fields=FIELDS, duration_days=10)


# ---------------------------------------------------------------------------------------------
# The person decides — nobody decides for them
# ---------------------------------------------------------------------------------------------
def test_nobody_but_the_person_can_grant(disclosure, operator, company_user, stranger, superuser):
    for user in (operator, company_user, stranger, superuser):
        with pytest.raises(PermissionDenied):
            services.grant_identity_disclosure(disclosure, person=user)
    disclosure.refresh_from_db()
    assert disclosure.status == DisclosureStatus.REQUESTED


def test_the_actor_asks_but_never_reads_on_the_company_s_behalf(disclosure, person, operator):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    assert can(operator, "read_identity", disclosure) is False
    with pytest.raises(PermissionDenied):
        services.read_identity(disclosure, user=operator)


def test_a_refusal_is_recorded_and_closes_the_request(disclosure, person):
    services.refuse_identity_disclosure(disclosure, person=person, note="Je préfère pas")
    disclosure.refresh_from_db()
    assert disclosure.status == DisclosureStatus.REFUSED
    assert disclosure.is_active() is False
    assert AuditEvent.objects.filter(action="selection.identity.refused").exists()


def test_a_decision_is_taken_once(disclosure, person):
    services.refuse_identity_disclosure(disclosure, person=person)
    with pytest.raises(ValidationError):
        services.grant_identity_disclosure(disclosure, person=person)


def test_two_requests_cannot_be_pending_at_once(process, operator, disclosure):
    with pytest.raises(ValidationError):
        services.request_identity_disclosure(
            process, operator=operator, purpose="Autre finalité", fields=FIELDS, duration_days=5
        )


# ---------------------------------------------------------------------------------------------
# It ends: by expiry, by withdrawal, or with the process
# ---------------------------------------------------------------------------------------------
def test_the_authorisation_expires_by_itself(disclosure, person, company_user):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    disclosure.expires_at = timezone.now() - dt.timedelta(seconds=1)
    disclosure.save(update_fields=["expires_at"])
    assert disclosure.is_active() is False
    assert disclosure.is_expired is True
    assert services.read_identity(disclosure, user=company_user) is None
    assert can(company_user, "read_identity", disclosure) is False


def test_withdrawal_is_immediate_and_withdraws_the_consent_record(disclosure, person, company_user):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    services.withdraw_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    assert disclosure.status == DisclosureStatus.WITHDRAWN
    assert disclosure.consent.is_active is False
    assert services.read_identity(disclosure, user=company_user) is None
    assert AuditEvent.objects.filter(action="selection.identity.withdrawn").exists()


def test_a_withdrawn_consent_alone_ends_the_disclosure(disclosure, person, company_user):
    """Belt and braces: even if only the consent record is withdrawn, nothing is readable."""
    from consents.services import withdraw as withdraw_consent

    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    withdraw_consent(disclosure.consent, note="retrait direct")
    disclosure.refresh_from_db()
    assert disclosure.is_active() is False
    assert services.read_identity(disclosure, user=company_user) is None


def test_concluding_the_process_ends_a_standing_disclosure(disclosure, person, operator, company_user):
    services.grant_identity_disclosure(disclosure, person=person)
    services.conclude(disclosure.process, SelectionOutcome.CLOSED_NO_FOLLOW_UP, operator=operator)
    disclosure.refresh_from_db()
    assert disclosure.is_active() is False, "a purpose that no longer exists cannot justify an access"
    assert services.read_identity(disclosure, user=company_user) is None


# ---------------------------------------------------------------------------------------------
# Every access is recorded
# ---------------------------------------------------------------------------------------------
def test_every_access_writes_one_row_and_one_audit_event(disclosure, person, company_user, company):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()

    services.read_identity(disclosure, user=company_user)
    services.read_identity(disclosure, user=company_user)

    rows = list(IdentityAccess.objects.filter(disclosure=disclosure))
    assert len(rows) == 2, "one row per access, not one row per disclosure"
    assert rows[0].accessed_by_organisation_id == company.pk
    assert rows[0].purpose_at_access == disclosure.purpose
    assert set(rows[0].fields_read) == set(FIELDS)
    assert AuditEvent.objects.filter(action="selection.identity.accessed").count() == 2


def test_the_person_can_read_who_consulted_their_identity(disclosure, person, company_user):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    services.read_identity(disclosure, user=company_user)
    accesses = services.accesses_for(disclosure)
    assert len(accesses) == 1
    assert can(person, "view", accesses[0]) is True


def test_a_stranger_reading_an_active_disclosure_is_refused_and_leaves_no_row(disclosure, person, stranger):
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    with pytest.raises(PermissionDenied):
        services.read_identity(disclosure, user=stranger)
    assert IdentityAccess.objects.count() == 0


def test_disclosures_are_scoped_by_the_queryset(disclosure, person, company_user, stranger, operator):
    assert IdentityDisclosure.objects.readable_by(person).count() == 1
    assert IdentityDisclosure.objects.readable_by(company_user).count() == 1
    assert IdentityDisclosure.objects.readable_by(operator).count() == 1
    assert IdentityDisclosure.objects.readable_by(stranger).count() == 0


def test_no_special_category_or_protected_field_can_ever_be_disclosed():
    """
    The register of communicable fields is an enumeration on purpose. Age is not there, and never
    will be: the previous platform carried an age band on every opening, which is direct age
    discrimination under Directive 2000/78/EC and D.lgs. 216/2003.
    """
    assert set(IdentityField.values) == {"full_name", "contact_email", "preferred_language"}, (
        "the register of communicable fields is closed: adding one is a deliberate legal decision, "
        "not a field added in passing"
    )
    forbidden = {
        "age",
        "birth",
        "naissance",
        "nationalite",
        "nationality",
        "health",
        "sante",
        "religion",
        "gender",
        "sexe",
        "genre",
    }
    for value in IdentityField.values:
        tokens = set(re.findall(r"[a-z]+", value))
        assert not (tokens & forbidden), f"{value} carries a protected characteristic"
