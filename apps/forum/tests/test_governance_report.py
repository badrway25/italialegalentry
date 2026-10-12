"""
The annual relation is GENERATED from the data, never typed (FORUM_GOVERNANCE §4).

The distinction is the whole test. A relation that can be written by hand says whatever its author
wanted it to say; a relation assembled from the edition, its commissions, the proposals that were
actually decided, the projects and the monitoring entries says what happened, and can be checked
against the rows it came from. Every assertion below therefore changes DATA and then reads the
report, rather than reading a field somebody set.

Two further properties are asserted because they are easy to lose:

* **A published relation is frozen.** Regenerating it is refused. It is the record of what the Forum
  reported on the day it reported it — the same reasoning that freezes a ruleset snapshot onto a
  case assessment.
* **The figures are counts and sums, never an index.** Nothing in the report is weighted, scored or
  turned into a percentage. A number here is a count of rows or the sum of indicators a commission
  declared, and ``test_the_report_computes_no_index`` keeps it that way.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.utils import timezone

from audit.models import AuditEvent
from forum import governance_services as services
from forum.governance import AnnualReport, MilestoneStatus, ProjectStatus, ProposalStatus, ReportStatus, Table

pytestmark = pytest.mark.django_db

BODY = "Proposition de coopération entre chambres consulaires, avec un calendrier annuel partagé."


def _sections(edition) -> dict[str, dict]:
    return {section["key"]: section for section in services.build_report_sections(edition)}


@pytest.fixture
def cycle(member, referent, commission, governance_edition):
    """
    One full turn of the cycle, built through the services: a table, three proposals (one retained,
    one set aside, one still in examination), a project with milestones and a monitoring entry.
    """
    Table.objects.create(commission=commission, key="table-report", title_fr="Table de travail")

    retained = services.open_proposal(member.user, commission, title_fr="Rencontres consulaires", body_fr=BODY)
    services.transition_proposal(retained, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(retained, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(retained, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")

    set_aside = services.open_proposal(member.user, commission, title_fr="Hors champ", body_fr=BODY)
    services.transition_proposal(set_aside, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(set_aside, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(set_aside, ProposalStatus.REJECTED, actor=referent.user, note="Hors du champ.")

    pending = services.open_proposal(member.user, commission, title_fr="En cours d’examen", body_fr=BODY)
    services.transition_proposal(pending, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(pending, ProposalStatus.UNDER_REVIEW, actor=referent.user)

    draft = services.open_proposal(member.user, commission, title_fr="Brouillon jamais déposé", body_fr=BODY)

    project = services.promote_to_project(
        retained,
        lead=member.profile,
        partners_fr="Chambre de Rovigo\nUniversité test",
        actor=referent.user,
    )
    services.transition_project(project, ProjectStatus.ACTIVE, actor=referent.user)
    done = services.add_milestone(project, title_fr="Convention signée", responsible=member.profile)
    services.set_milestone_status(done, MilestoneStatus.DONE)
    services.add_milestone(
        project,
        title_fr="Première rencontre",
        responsible=member.profile,
        due_on=timezone.localdate() - dt.timedelta(days=2),
    )
    services.record_monitoring(
        project,
        period_start=timezone.localdate() - dt.timedelta(days=90),
        period_end=timezone.localdate() - dt.timedelta(days=1),
        indicators={"rencontres": 2, "participants": 40},
        recorded_by=member.profile,
    )
    services.record_monitoring(
        project,
        period_start=timezone.localdate() - dt.timedelta(days=1),
        period_end=timezone.localdate(),
        indicators={"rencontres": 1, "participants": 25},
        recorded_by=member.profile,
    )
    return {
        "retained": retained,
        "set_aside": set_aside,
        "pending": pending,
        "draft": draft,
        "project": project,
    }


# ---------------------------------------------------------------------------------------------
# The sections follow the cycle
# ---------------------------------------------------------------------------------------------
def test_the_report_has_the_five_sections_of_the_cycle(governance_edition):
    keys = [section["key"] for section in services.build_report_sections(governance_edition)]
    assert keys == ["edition", "commissions", "proposals", "projects", "monitoring"]


def test_an_empty_edition_produces_honest_empty_sections(governance_edition):
    sections = _sections(governance_edition)
    assert sections["edition"]["summary"]["commissions"] == 5
    assert sections["edition"]["summary"]["participants"] == 0
    assert sections["proposals"]["rows"] == []
    assert sections["projects"]["rows"] == []
    assert sections["monitoring"]["rows"] == []


def test_the_edition_section_counts_participants_and_live_mandates(governance_edition, member, referent, lapsed_member):
    summary = _sections(governance_edition)["edition"]["summary"]
    assert summary["participants"] == 3
    # Three profiles, but only two mandates are in force: the lapsed one does not count.
    assert summary["mandates_live"] == 2


def test_the_commissions_section_counts_what_the_commissions_did(governance_edition, commission, cycle):
    row = next(row for row in _sections(governance_edition)["commissions"]["rows"] if row["key"] == commission.key)
    assert row["name"] == commission.name_fr
    assert row["tables"] == 1
    assert row["proposals"] == 4
    assert row["accepted"] == 1
    assert row["rejected"] == 1
    assert row["under_review"] == 1
    assert row["members_live"] == 2


def test_the_proposals_section_lists_only_the_retained_ones(governance_edition, cycle):
    section = _sections(governance_edition)["proposals"]
    references = {row["reference"] for row in section["rows"]}
    assert references == {cycle["retained"].reference}
    assert section["summary"] == {"submitted": 3, "accepted": 1, "rejected": 1, "withdrawn": 0}


def test_a_decision_taken_after_midnight_in_rome_is_dated_that_day(
    after_midnight_in_rome, governance_edition, member, referent, commission
):
    """
    The relation dates a decision in Rome's calendar. ``decided_at`` is held in UTC: a proposal
    accepted at 00:30 on 5 October in Rome was printed as decided on 4 October.
    """
    proposal = services.open_proposal(member.user, commission, title_fr="Retenue après minuit", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    proposal.refresh_from_db()
    assert proposal.decided_at.date() == dt.date(2026, 10, 4), "held in UTC: the trap"
    rows = _sections(governance_edition)["proposals"]["rows"]
    assert [row["decided_on"] for row in rows] == ["2026-10-05"]


def test_a_draft_never_reaches_the_report(governance_edition, cycle):
    section = _sections(governance_edition)["proposals"]
    assert cycle["draft"].reference not in {row["reference"] for row in section["rows"]}
    assert section["summary"]["submitted"] == 3, "a draft is not a deposited proposal"


def test_the_projects_section_names_the_responsible_organisation(governance_edition, cycle, member):
    row = _sections(governance_edition)["projects"]["rows"][0]
    assert row["lead"] == member.profile.display_label
    assert row["origin"] == cycle["retained"].reference
    assert row["partners"] == ["Chambre de Rovigo", "Université test"]
    assert row["milestones_total"] == 2
    assert row["milestones_done"] == 1
    assert row["milestones_overdue"] == 1


def test_the_monitoring_section_sums_the_declared_indicators(governance_edition, cycle):
    section = _sections(governance_edition)["monitoring"]
    assert section["rows"][0]["entries"] == 2
    assert section["rows"][0]["indicators"] == {"rencontres": 3, "participants": 65}
    assert section["summary"]["entries"] == 2
    assert section["summary"]["projects_monitored"] == 1
    assert section["summary"]["projects_without_monitoring"] == 0


def test_a_project_without_monitoring_is_named_as_such(governance_edition, member, referent, other_commission):
    """« Un progetto senza monitoraggio è un tavolo di discussione » — so the report says so."""
    services.grant_mandate(other_commission, referent.profile, role=referent.mandate.role)
    proposal = services.open_proposal(referent.user, other_commission, title_fr="Sans suivi", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=referent.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    services.promote_to_project(proposal, lead=referent.profile, actor=referent.user)
    summary = _sections(governance_edition)["monitoring"]["summary"]
    assert summary["projects_without_monitoring"] == 1


def test_the_report_computes_no_index(governance_edition, cycle):
    """Counts and sums only: no score, no weighting, no percentage anywhere in the document."""
    import json

    blob = json.dumps(services.build_report_sections(governance_edition))
    for forbidden in ("percent", "score", "index", "rating", "note_globale"):
        assert forbidden not in blob


def test_non_numeric_indicators_are_ignored_rather_than_coerced(governance_edition, cycle, member):
    services.record_monitoring(
        cycle["project"],
        period_start=timezone.localdate(),
        period_end=timezone.localdate(),
        indicators={"rencontres": "trois", "commentaire": True, "participants": 5},
        recorded_by=member.profile,
    )
    indicators = _sections(governance_edition)["monitoring"]["rows"][0]["indicators"]
    assert indicators == {"rencontres": 3, "participants": 70}


# ---------------------------------------------------------------------------------------------
# Generating, freezing and publishing
# ---------------------------------------------------------------------------------------------
def test_generating_stores_the_sections_and_is_audited(governance_edition, secretariat, cycle):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    assert report.status == ReportStatus.DRAFT
    assert [section["key"] for section in report.sections] == [
        "edition",
        "commissions",
        "proposals",
        "projects",
        "monitoring",
    ]
    assert report.generated_at is not None
    assert report.generated_by_id == secretariat.profile.pk
    assert AuditEvent.objects.filter(action="forum.report.generated").exists()


def test_regenerating_a_draft_picks_up_new_data(governance_edition, secretariat, member, referent, commission):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    before = _summary(report, "proposals")["accepted"]
    proposal = services.open_proposal(member.user, commission, title_fr="Nouvelle proposition", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    assert _summary(report, "proposals")["accepted"] == before + 1


def _summary(report: AnnualReport, key: str) -> dict:
    return next(section for section in report.sections if section["key"] == key)["summary"]


def test_a_published_report_is_never_regenerated(governance_edition, secretariat, cycle):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    services.publish_annual_report(report, actor=secretariat.user)
    with pytest.raises(services.GovernanceRefused):
        services.generate_annual_report(governance_edition, actor=secretariat.user)


def test_a_published_report_keeps_saying_what_it_said(governance_edition, secretariat, member, referent, commission):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    services.publish_annual_report(report, actor=secretariat.user)
    frozen = _summary(report, "proposals")["accepted"]
    proposal = services.open_proposal(member.user, commission, title_fr="Après publication", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    report.refresh_from_db()
    assert _summary(report, "proposals")["accepted"] == frozen


def test_an_empty_report_is_not_published(governance_edition, secretariat):
    report = AnnualReport.objects.create(edition=governance_edition)
    with pytest.raises(services.GovernanceRefused):
        services.publish_annual_report(report, actor=secretariat.user)


def test_publishing_is_audited_and_idempotent(governance_edition, secretariat, cycle):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    services.publish_annual_report(report, actor=secretariat.user)
    published_at = report.published_at
    services.publish_annual_report(report, actor=secretariat.user)
    assert report.published_at == published_at
    assert AuditEvent.objects.filter(action="forum.report.published").count() == 1


def test_the_sections_field_is_not_editable_by_hand():
    """`editable=False` keeps the report out of every ModelForm and out of the back-office."""
    assert AnnualReport._meta.get_field("sections").editable is False
