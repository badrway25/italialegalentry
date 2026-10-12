"""
The mandatory chain, and the four refusals that make it a chain rather than a diagram:

    CompanyNeed → AuthorizedActor → SelectionMandate → SelectionProcess → CaseFile/Person → AuditEvent

Each test below corresponds to a sentence somebody would otherwise have to take on trust.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from audit.models import AuditEvent
from cases import services as case_services
from cases.models import AssignmentRole, CaseStatus
from selection import services
from selection.models import (
    SelectionOutcome,
    SelectionProcess,
    SelectionStage,
)

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# No process without a valid actor
# ---------------------------------------------------------------------------------------------
def test_no_process_without_a_valid_actor(lapsed_actor, company, case, lapsed_operator):
    """A lapsed authorisation cannot even receive the mandate a process would need."""
    with pytest.raises(ValidationError):
        services.issue_mandate(
            actor=lapsed_actor,
            company=company,
            need_profile="Soudeur qualifié",
        )
    assert SelectionProcess.objects.count() == 0


def test_no_process_once_the_authorisation_lapses_after_the_mandate(mandate, case, operator, actor):
    """
    The mandate was issued while the authorisation was in force, and the authorisation then expired.

    The mandate is a piece of paper; what makes the act lawful is the authorisation behind it, so
    the process is refused at the moment it is asked for, not at the moment the paper was signed.
    """
    actor.valid_until = timezone.localdate() - dt.timedelta(days=1)
    actor.save(update_fields=["valid_until"])
    mandate.refresh_from_db()
    assert mandate.is_live is False
    with pytest.raises(ValidationError):
        services.open_process(mandate=mandate, case=case, operator=operator)
    assert SelectionProcess.objects.count() == 0


def test_no_process_when_the_authorisation_is_withdrawn(mandate, case, operator, actor):
    actor.withdrawn_at = timezone.now()
    actor.save(update_fields=["withdrawn_at"])
    mandate.refresh_from_db()
    with pytest.raises(ValidationError):
        services.open_process(mandate=mandate, case=case, operator=operator)


def test_no_process_for_an_account_that_is_not_an_operator_of_the_actor(mandate, case, stranger):
    with pytest.raises(PermissionDenied):
        services.open_process(mandate=mandate, case=case, operator=stranger)
    assert SelectionProcess.objects.count() == 0


def test_no_process_from_a_case_state_that_cases_does_not_allow(mandate, case, operator):
    """
    ``cases.ALLOWED_TRANSITIONS`` declares TRAINING → SELECTION and nothing else reaches SELECTION.
    This module does not invent a second answer to the same question.
    """
    case_services.transition(case, CaseStatus.ORIENTED)
    with pytest.raises(ValidationError):
        services.open_process(mandate=mandate, case=case, operator=operator)


def test_a_mandate_cannot_be_issued_to_a_lapsed_authorisation(lapsed_actor, company):
    with pytest.raises(ValidationError):
        services.issue_mandate(actor=lapsed_actor, company=company, need_profile="Soudeur")


# ---------------------------------------------------------------------------------------------
# The chain, when it works
# ---------------------------------------------------------------------------------------------
def test_opening_a_process_assigns_the_actor_and_moves_the_case_to_selection(process, case, actor, operator):
    case.refresh_from_db()
    assert case.status == CaseStatus.SELECTION
    assignment = case.assignments.get(role=AssignmentRole.AUTHORISED_ACTOR)
    # The assignment carries the actor's OWN authorisation, which is why cases accepts the state.
    assert assignment.authorisation_reference == actor.authorisation_reference
    assert assignment.authorisation_valid_until == actor.valid_until
    assert assignment.organisation_id == actor.organisation_id
    assert case.has_valid_authorised_actor() is True


def test_cases_refuses_selection_without_an_authorised_actor_the_same_way(case, person):
    """The rule stated by ``cases`` and the rule stated here must not be two different rules."""
    with pytest.raises(ValidationError):
        case_services.transition(case, CaseStatus.SELECTION)
    case.refresh_from_db()
    assert case.status == CaseStatus.TRAINING


def test_opening_a_process_is_audited_and_names_the_responsible_actor(process, actor):
    event = AuditEvent.objects.filter(action="selection.process.opened").first()
    assert event is not None
    assert actor.organisation.name in event.metadata["responsible_actor"]
    assert event.metadata["authorisation"] == actor.authorisation_reference


def test_the_process_starts_with_evidence_that_always_names_a_responsible(process):
    rows = list(process.evidence.all())
    assert rows, "a process opens with the evidence the actor requires"
    assert all(row.responsible_actor for row in rows)


def test_a_second_process_for_the_same_mandate_and_case_is_refused(process, mandate, case, operator):
    with pytest.raises(ValidationError):
        services.open_process(mandate=mandate, case=case, operator=operator)


# ---------------------------------------------------------------------------------------------
# Stages
# ---------------------------------------------------------------------------------------------
def test_an_undeclared_stage_transition_is_refused(process, operator):
    with pytest.raises(ValidationError):
        services.advance(process, SelectionStage.COMPANY_REVIEW, operator=operator)
    process.refresh_from_db()
    assert process.stage == SelectionStage.MANDATE_CONFIRMED


def test_every_stage_change_writes_an_event_naming_the_actor_and_an_audit_row(process, operator, actor):
    services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator, note="Examen ouvert")
    event = process.events.order_by("-created_at").first()
    assert event.to_stage == SelectionStage.COMPETENCE_REVIEW
    assert event.actor_id == actor.pk
    assert actor.organisation.name in event.responsible_label

    audit = AuditEvent.objects.filter(action="selection.stage").first()
    assert audit.metadata["to"] == SelectionStage.COMPETENCE_REVIEW
    assert actor.organisation.name in audit.metadata["responsible_actor"]


def test_an_account_that_is_not_the_operator_cannot_advance_a_stage(process, stranger, company_user, person):
    for user in (stranger, company_user, person):
        with pytest.raises(PermissionDenied):
            services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=user)


def test_a_lapsed_authorisation_can_no_longer_advance_the_process(process, operator, actor):
    actor.valid_until = timezone.localdate() - dt.timedelta(days=1)
    actor.save(update_fields=["valid_until"])
    process.refresh_from_db()
    with pytest.raises((ValidationError, PermissionDenied)):
        services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator)


def test_a_suspension_requires_a_reason(process, operator):
    with pytest.raises(ValidationError):
        services.advance(process, SelectionStage.SUSPENDED, operator=operator, note="")
    services.advance(process, SelectionStage.SUSPENDED, operator=operator, note="Pièce manquante")
    process.refresh_from_db()
    assert process.suspension_reason == "Pièce manquante"


# ---------------------------------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------------------------------
def test_concluding_moves_the_case_on_and_revokes_the_assignment(process, case, operator):
    services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator)
    services.conclude(process, SelectionOutcome.REFERRED_TO_PROCEDURE, operator=operator, note="Transmis")
    process.refresh_from_db()
    case.refresh_from_db()
    assert process.stage == SelectionStage.CONCLUDED
    assert process.outcome == SelectionOutcome.REFERRED_TO_PROCEDURE
    assert case.status == CaseStatus.ADMIN_PROCESS
    assert case.has_valid_authorised_actor() is False, "the mandate ends with the process"


def test_concluding_without_referral_returns_the_case_to_its_pathway(process, case, operator):
    services.conclude(process, SelectionOutcome.CLOSED_NO_FOLLOW_UP, operator=operator)
    case.refresh_from_db()
    assert case.status == CaseStatus.TRAINING, "a person whose selection ended is still on their pathway"


def test_a_closed_process_does_not_reopen(process, operator):
    services.conclude(process, SelectionOutcome.CLOSED_NO_FOLLOW_UP, operator=operator)
    with pytest.raises(ValidationError):
        services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator)


def test_no_outcome_reads_as_a_decision_about_the_person():
    """
    CR-11 removed ``eligible`` from the rule engine for a reason; the same reason applies here.
    An issue describes what happened to the PROCESS.
    """
    forbidden = (
        "approuv",
        "approved",
        "eligible",
        "éligible",
        "idoneo",
        "retenu",
        "selected",
        "sélectionné",
        "rejet",
        "rejected",
        "recrut",
        "embauch",
    )
    for value, label in SelectionOutcome.choices:
        text = f"{value} {label}".lower()
        for word in forbidden:
            assert word not in text, f"{value}: « {word} » lu par un utilisateur est une décision"
