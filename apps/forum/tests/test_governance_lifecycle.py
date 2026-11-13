"""
The invariants of the Forum Permanent cycle, tested at the DOMAIN level rather than through screens.

An interface can be bypassed; a rule that only lives in a template is not a rule. Everything here
asserts behaviour that must hold however the change arrives — view, back-office, management command
or a future API — which is why almost nothing in this file touches a URL.

Follows the shape of ``apps/cases/tests/test_lifecycle.py``: one declared transition table, every
declared edge exercised, every undeclared edge refused, and the audit row asserted rather than
assumed.
"""

from __future__ import annotations

import datetime as dt
import pathlib

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from audit.models import AuditEvent
from forum import governance_services as services
from forum.governance import (
    ALLOWED_PROPOSAL_TRANSITIONS,
    DECISION_PROPOSAL_STATUSES,
    PRE_DECISION_PROPOSAL_STATUSES,
    Commission,
    CommissionMember,
    MandateRole,
    MilestoneStatus,
    ProjectStatus,
    ProposalStatus,
    proposal_transitions_from,
)

pytestmark = pytest.mark.django_db

BODY = (
    "La commission propose d’ouvrir un cycle de rencontres techniques entre les chambres consulaires "
    "des deux rives, avec un calendrier annuel et un compte rendu public."
)


def _draft(member, commission, title="Rencontres techniques consulaires"):
    return services.open_proposal(member.user, commission, title_fr=title, body_fr=BODY)


def _to_review(member, referent, commission):
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    return proposal


# ---------------------------------------------------------------------------------------------
# The seed is configuration, and it is the only place the five commissions are named
# ---------------------------------------------------------------------------------------------
def test_the_seed_creates_the_edition_and_five_commissions(governance_edition):
    assert governance_edition.year == 2026
    assert Commission.objects.filter(edition=governance_edition).count() == 5


def test_the_seed_is_idempotent(governance_edition):
    from forum.governance_seeds import seed_forum_governance

    seed_forum_governance()
    seed_forum_governance()
    assert Commission.objects.filter(edition=governance_edition).count() == 5


def test_the_seed_creates_no_account_no_profile_no_proposal(governance_edition):
    """Configuration only. Demonstration records are guarded by core.seeds.demonstration_data_allowed."""
    from forum.governance import ForumProfile, ForumProposal

    assert ForumProfile.objects.count() == 0
    assert ForumProposal.objects.count() == 0


def test_a_sixth_commission_needs_no_code_change(governance_edition):
    """REQ-CFG-03: the commissions are data. Nothing in the module enumerates their keys."""
    Commission.objects.create(
        edition=governance_edition, key="sante-protection-sociale", name_fr="Santé et protection sociale", order=60
    )
    assert Commission.objects.filter(edition=governance_edition).count() == 6


# ---------------------------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------------------------
def test_a_new_proposal_starts_as_a_draft_with_a_reference(member, commission):
    proposal = _draft(member, commission)
    assert proposal.status == ProposalStatus.DRAFT
    assert proposal.reference.startswith("P")
    assert len(proposal.reference) == 10


def test_references_are_not_sequential(member, commission):
    proposals = [_draft(member, commission, f"Proposition numéro {index}") for index in range(12)]
    references = [proposal.reference for proposal in proposals]
    assert len(set(references)) == 12
    # A sequential reference sorts like the primary keys; a random one matches one chance in 12!.
    # (« no reference is all digits after the P » failed by chance about one run in 14: nine random
    # hex digits are all decimal once in 69, five were drawn — and that draw is not a sequence.)
    assert sorted(references) != [proposal.reference for proposal in sorted(proposals, key=lambda p: p.pk)]


def test_opening_a_proposal_is_audited(member, commission):
    proposal = _draft(member, commission)
    assert AuditEvent.objects.filter(action="forum.proposal.created", target_id=str(proposal.pk)).exists()


def test_an_observer_may_not_table_a_proposal(observer, commission):
    """FORUM_GOVERNANCE §5: an observer consults within the perimeter of the agreement."""
    with pytest.raises(PermissionDenied):
        _draft(observer, commission)


def test_an_account_without_a_mandate_may_not_table_a_proposal(outsider, commission):
    with pytest.raises(PermissionDenied):
        services.open_proposal(outsider, commission, title_fr="Sans mandat", body_fr=BODY)


def test_a_lapsed_mandate_may_not_table_a_proposal(lapsed_member, commission):
    with pytest.raises(PermissionDenied):
        _draft(lapsed_member, commission)


# ---------------------------------------------------------------------------------------------
# Every DECLARED transition
# ---------------------------------------------------------------------------------------------
def test_draft_to_submitted_is_allowed_for_the_proposer(member, commission):
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.SUBMITTED
    assert proposal.previous_status == ProposalStatus.DRAFT


def test_submitted_to_under_review_is_allowed_for_the_referent(member, referent, commission):
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.UNDER_REVIEW


def test_under_review_to_accepted_is_allowed_with_a_motivation(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(
        proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Cohérente avec la priorité de l’édition."
    )
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.ACCEPTED
    assert proposal.decision_note_fr
    assert proposal.decided_at is not None


def test_under_review_to_rejected_is_allowed_with_a_motivation(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(
        proposal, ProposalStatus.REJECTED, actor=referent.user, note="Hors du champ de la commission."
    )
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.REJECTED


@pytest.mark.parametrize("start", sorted(PRE_DECISION_PROPOSAL_STATUSES))
def test_withdrawn_is_reachable_from_every_pre_decision_state(start):
    assert ProposalStatus.WITHDRAWN in proposal_transitions_from(start)


def test_the_proposer_may_withdraw_a_submitted_proposal(member, commission):
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.WITHDRAWN, actor=member.user)
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.WITHDRAWN


def test_every_transition_is_audited(member, commission):
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    event = AuditEvent.objects.filter(action="forum.proposal.transition").latest("created_at")
    assert event.metadata["from"] == ProposalStatus.DRAFT
    assert event.metadata["to"] == ProposalStatus.SUBMITTED
    assert event.metadata["commission"] == commission.key


# ---------------------------------------------------------------------------------------------
# Every REFUSED transition
# ---------------------------------------------------------------------------------------------
def test_an_undeclared_transition_is_refused(member, referent, commission):
    proposal = _draft(member, commission)
    with pytest.raises(services.TransitionRefused):
        services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="trop tôt")
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.DRAFT


def test_an_unknown_state_is_refused(member, commission):
    proposal = _draft(member, commission)
    with pytest.raises(services.TransitionRefused):
        services.transition_proposal(proposal, "approved", actor=member.user)


def test_a_decision_without_a_motivation_is_refused(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    with pytest.raises(services.TransitionRefused):
        services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="   ")
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.UNDER_REVIEW


def test_a_decided_proposal_is_a_dead_end(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    for target in (ProposalStatus.REJECTED, ProposalStatus.WITHDRAWN, ProposalStatus.UNDER_REVIEW):
        with pytest.raises(services.TransitionRefused):
            services.transition_proposal(proposal, target, actor=referent.user, note="peu importe")


def test_a_decided_proposal_cannot_be_withdrawn_by_its_author(member, referent, commission):
    """Withdrawal after a decision would rewrite what a commission actually resolved."""
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.REJECTED, actor=referent.user, note="Écartée.")
    with pytest.raises(services.TransitionRefused):
        services.transition_proposal(proposal, ProposalStatus.WITHDRAWN, actor=member.user)


def test_a_plain_member_may_not_open_the_review(member, forum_actor, commission):
    other = forum_actor("autre.membre@example.test", commission=commission)
    proposal = _draft(member, commission)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    with pytest.raises(PermissionDenied):
        services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=other.user)


def test_a_plain_member_may_not_decide(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    with pytest.raises(PermissionDenied):
        services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=member.user, note="Je m’auto-retiens.")


def test_a_referent_whose_mandate_lapsed_may_not_decide(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    referent.mandate.valid_until = timezone.localdate() - dt.timedelta(days=1)
    referent.mandate.save(update_fields=["valid_until"])
    with pytest.raises(PermissionDenied):
        services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")


def test_transitioning_to_the_same_state_is_a_no_op(member, commission):
    proposal = _draft(member, commission)
    assert services.transition_proposal(proposal, ProposalStatus.DRAFT, actor=member.user).status == (
        ProposalStatus.DRAFT
    )


def test_the_declared_table_is_the_whole_lifecycle():
    """Every state of the enum appears in the table, and no edge points outside the enum."""
    assert set(ALLOWED_PROPOSAL_TRANSITIONS) == set(ProposalStatus.values)
    for targets in ALLOWED_PROPOSAL_TRANSITIONS.values():
        assert targets <= set(ProposalStatus.values)


def test_a_view_never_calls_save_to_change_a_state():
    """
    Structural, and deliberately so: the rule is « a view must never write a state ».

    Grepping the views module is the cheapest way to keep that true over time — a future refactor
    that reaches for ``obj.save()`` in a view fails here instead of quietly bypassing the audit trail.
    """
    source = pathlib.Path(__file__).resolve().parents[1] / "governance_views.py"
    text = source.read_text(encoding="utf-8")
    assert ".save(" not in text
    assert ".objects.create(" not in text


# ---------------------------------------------------------------------------------------------
# Dated mandates — checked AT READ TIME
# ---------------------------------------------------------------------------------------------
def test_a_live_mandate_opens_the_commission(member, commission):
    assert commission in Commission.objects.readable_by(member.user)
    assert member.mandate.is_live is True


def test_a_lapsed_mandate_grants_nothing(lapsed_member, commission):
    assert lapsed_member.mandate.is_live is False
    assert list(Commission.objects.readable_by(lapsed_member.user)) == []
    assert lapsed_member.mandate not in CommissionMember.objects.live()


def test_a_mandate_valid_today_still_grants_access(forum_actor, commission):
    actor = forum_actor("aujourdhui@example.test", commission=commission, valid_until=timezone.localdate())
    assert commission in Commission.objects.readable_by(actor.user)


def test_a_mandate_that_has_not_started_grants_nothing(forum_actor, commission):
    actor = forum_actor(
        "demain@example.test", commission=commission, valid_from=timezone.localdate() + dt.timedelta(days=1)
    )
    assert actor.mandate.is_live is False
    assert list(Commission.objects.readable_by(actor.user)) == []


def test_a_revoked_mandate_grants_nothing(member, commission):
    services.revoke_mandate(member.mandate)
    member.mandate.refresh_from_db()
    assert member.mandate.is_live is False
    assert list(Commission.objects.readable_by(member.user)) == []
    assert AuditEvent.objects.filter(action="forum.mandate.revoked").exists()


def test_is_live_and_the_queryset_answer_the_same_question(forum_actor, commission):
    """One check for a row in hand, one for a filter. A disagreement is a security bug."""
    today = timezone.localdate()
    actors = [
        forum_actor("a@example.test", commission=commission, valid_until=today + dt.timedelta(days=1)),
        forum_actor("b@example.test", commission=commission, valid_until=today),
        forum_actor("c@example.test", commission=commission, valid_until=today - dt.timedelta(days=1)),
        forum_actor("d@example.test", commission=commission, valid_from=today + dt.timedelta(days=2)),
    ]
    live_ids = set(CommissionMember.objects.live().values_list("pk", flat=True))
    for actor in actors:
        assert actor.mandate.is_live is (actor.mandate.pk in live_ids), actor.user.email


def test_a_mandate_ending_before_it_starts_is_refused(governance_edition, commission, django_user_model):
    from forum.governance import ForumProfile

    user = django_user_model.objects.create_user(email="bornes@example.test", password="x")
    profile = ForumProfile.objects.create(user=user, edition=governance_edition, organisation_label="Test")
    with pytest.raises(ValidationError):
        services.grant_mandate(
            commission,
            profile,
            valid_from=timezone.localdate(),
            valid_until=timezone.localdate() - dt.timedelta(days=1),
        )


def test_a_mandate_across_editions_is_refused(commission, forum_actor, django_user_model):
    from forum.governance import EditionStatus, ForumEdition, ForumProfile

    other_edition = ForumEdition.objects.create(
        key="casablanca-2027", year=2027, title_fr="Édition de Casablanca", status=EditionStatus.PLANNED
    )
    user = django_user_model.objects.create_user(email="autre.edition@example.test", password="x")
    profile = ForumProfile.objects.create(user=user, edition=other_edition, organisation_label="Test")
    with pytest.raises(ValidationError):
        services.grant_mandate(commission, profile)


def test_granting_a_mandate_is_audited(member):
    assert AuditEvent.objects.filter(action="forum.mandate.granted").exists()


# ---------------------------------------------------------------------------------------------
# A proposal becomes a project — the hinge of the cycle
# ---------------------------------------------------------------------------------------------
def test_only_an_accepted_proposal_becomes_a_project(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    with pytest.raises(services.GovernanceRefused):
        services.promote_to_project(proposal, lead=member.profile)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    project = services.promote_to_project(proposal, lead=member.profile, actor=referent.user)
    assert project.origin_id == proposal.pk
    assert project.status == ProjectStatus.PREPARATION
    assert AuditEvent.objects.filter(action="forum.project.created").exists()


def test_a_proposal_produces_at_most_one_project(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    services.promote_to_project(proposal, lead=member.profile, actor=referent.user)
    proposal.refresh_from_db()
    with pytest.raises(services.GovernanceRefused):
        services.promote_to_project(proposal, lead=member.profile, actor=referent.user)


def test_project_transitions_follow_the_declared_table(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    project = services.promote_to_project(proposal, lead=member.profile, actor=referent.user)

    with pytest.raises(services.TransitionRefused):
        services.transition_project(project, ProjectStatus.COMPLETED, actor=referent.user)

    services.transition_project(project, ProjectStatus.ACTIVE, actor=referent.user)
    services.transition_project(project, ProjectStatus.SUSPENDED, actor=referent.user)
    project.refresh_from_db()
    assert project.previous_status == ProjectStatus.ACTIVE
    services.transition_project(project, ProjectStatus.ACTIVE, actor=referent.user)
    services.transition_project(project, ProjectStatus.COMPLETED, actor=referent.user)
    project.refresh_from_db()
    assert project.status == ProjectStatus.COMPLETED
    with pytest.raises(services.TransitionRefused):
        services.transition_project(project, ProjectStatus.ACTIVE, actor=referent.user)


def test_a_plain_member_may_not_move_a_project(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    project = services.promote_to_project(proposal, lead=member.profile, actor=referent.user)
    with pytest.raises(PermissionDenied):
        services.transition_project(project, ProjectStatus.ACTIVE, actor=member.user)


# ---------------------------------------------------------------------------------------------
# Milestones and monitoring
# ---------------------------------------------------------------------------------------------
@pytest.fixture
def project(member, referent, commission):
    proposal = _to_review(member, referent, commission)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    return services.promote_to_project(
        proposal, lead=member.profile, partners_fr="Chambre de Rovigo\nUniversité test", actor=referent.user
    )


def test_a_milestone_always_names_a_responsible_organisation(project, member):
    milestone = services.add_milestone(project, title_fr="Convention signée", responsible=member.profile)
    assert milestone.responsible_id == member.profile.pk
    with pytest.raises(ValidationError):
        services.add_milestone(project, title_fr="Sans responsable", responsible=None)


def test_milestone_progress_is_a_count_not_a_percentage(project, member):
    services.add_milestone(project, title_fr="A", responsible=member.profile)
    done = services.add_milestone(project, title_fr="B", responsible=member.profile)
    skipped = services.add_milestone(project, title_fr="C", responsible=member.profile)
    services.set_milestone_status(done, MilestoneStatus.DONE)
    services.set_milestone_status(skipped, MilestoneStatus.NOT_APPLICABLE)
    counts = project.milestone_counts()
    assert counts == {"total": 2, "done": 1, "open": 1, "overdue": 0}
    assert "percent" not in counts


def test_an_overdue_milestone_is_computed_from_its_due_date(project, member):
    services.add_milestone(
        project,
        title_fr="En retard",
        responsible=member.profile,
        due_on=timezone.localdate() - dt.timedelta(days=3),
    )
    assert project.milestone_counts()["overdue"] == 1


def test_changing_a_milestone_status_is_audited(project, member):
    milestone = services.add_milestone(project, title_fr="A", responsible=member.profile)
    services.set_milestone_status(milestone, MilestoneStatus.DONE, actor=member.user)
    assert AuditEvent.objects.filter(action="forum.milestone.status").exists()


def test_an_unknown_milestone_status_is_refused(project, member):
    milestone = services.add_milestone(project, title_fr="A", responsible=member.profile)
    with pytest.raises(ValidationError):
        services.set_milestone_status(milestone, "finished")


def test_a_monitoring_period_cannot_end_before_it_starts(project, member):
    with pytest.raises(ValidationError):
        services.record_monitoring(
            project,
            period_start=timezone.localdate(),
            period_end=timezone.localdate() - dt.timedelta(days=1),
            recorded_by=member.profile,
        )


def test_recording_monitoring_is_audited(project, member):
    services.record_monitoring(
        project,
        period_start=timezone.localdate() - dt.timedelta(days=90),
        period_end=timezone.localdate(),
        indicators={"rencontres": 3},
        recorded_by=member.profile,
        actor=member.user,
    )
    assert AuditEvent.objects.filter(action="forum.monitoring.recorded").exists()


def test_the_decision_statuses_are_the_two_the_document_names():
    assert DECISION_PROPOSAL_STATUSES == {ProposalStatus.ACCEPTED, ProposalStatus.REJECTED}


def test_there_is_no_approved_status():
    """« Approuvée » would read as an administrative decision; a commission retains or sets aside."""
    assert "approved" not in ProposalStatus.values


def test_a_referent_mandate_is_what_makes_a_referent(member, referent, commission):
    assert referent.mandate.role == MandateRole.REFERENT
    assert "referent" in services.capacities(referent.user, commission)
    assert "referent" not in services.capacities(member.user, commission)


# ---------------------------------------------------------------------------------------------
# The back-office has no private lifecycle
# ---------------------------------------------------------------------------------------------
def test_the_commissions_are_administrable_without_a_code_change():
    """REQ-CFG-03 is only true if there is a screen where a sixth commission can be added."""
    from django.contrib import admin as django_admin

    from forum.governance import AnnualReport, Commission, ForumEdition

    for model in (ForumEdition, Commission, AnnualReport):
        assert model in django_admin.site._registry, model.__name__


def test_the_back_office_cannot_edit_a_state_directly():
    """
    A back-office that could set ``status`` would give itself a private lifecycle — one that skips
    the declared transition table and writes no audit row. The fields are read-only there too.
    """
    from django.contrib import admin as django_admin

    from forum.governance import ForumProject, ForumProposal

    for model, fields in ((ForumProposal, ("status", "status_since")), (ForumProject, ("status",))):
        readonly = set(django_admin.site._registry[model].readonly_fields)
        assert set(fields) <= readonly, model.__name__
