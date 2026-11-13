"""
A result produced by the demonstration ruleset must say so, on the page, above the outcome.

The assessment page carries numbered sources, precise legal references, consultation dates and a
reproducible replay. Every one of those reads as authority, and none of them is true when the rules
behind the result were activated to show the engine working. The database knew — `approved_by_label`
says it in words — and the reports knew, and the screen did not.

Where the notice sits matters as much as whether it exists: above the outcome, because a reader who
has already read the outcome has already believed it.
"""

from __future__ import annotations

import datetime as dt

import pytest

from cases import services as case_services
from cases.models import CasePurpose
from rules import services as rule_services
from rules.models import (
    DEMONSTRATION_APPROVAL_PREFIX,
    LegalRule,
    LegalSource,
    ReviewStatus,
    RuleEffect,
    is_demonstration_approval,
)

pytestmark = [pytest.mark.django_db, pytest.mark.security]

DEMO_LABEL = f"{DEMONSTRATION_APPROVAL_PREFIX} — nessun giurista ha approvato questa regola"
REAL_LABEL = "Avv. Referente Giuridico"


@pytest.fixture
def person(django_user_model):
    return django_user_model.objects.create_user(
        email="notice-person@example.test", password="Local-Only-2026!"
    )


@pytest.fixture
def reviewer(django_user_model):
    return django_user_model.objects.create_user(
        email="notice-reviewer@example.test", password="Local-Only-2026!", full_name="Revisore"
    )


def _rule_in_force(author, reviewer, *, label: str) -> LegalRule:
    source = LegalSource.objects.create(
        key=f"src-{label[:8].lower().strip().replace(' ', '-')}",
        title_fr="Travail salarié",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )
    rule = LegalRule.objects.create(
        rule_id="R-NOTICE-001",
        version=1,
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.notice",
        message_fr="Un avertissement.",
        valid_from=dt.date(2026, 1, 1),
        created_by=author,
    )
    rule.sources.set([source])
    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        rule_services.transition(rule, target, actor=reviewer, approver_label=label)
    return rule


def _assessment_page(client, person, label: str):
    """
    A case with one frozen assessment whose snapshot names its approver.

    Recorded through `record_assessment` rather than by writing the row: that service is what the
    intake calls, and a test that builds the row by hand stops covering the shape the application
    actually stores the day the service changes.
    """
    case = case_services.open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    assessment = case_services.record_assessment(
        case,
        outcome="missing_requirement",
        ruleset_version=1,
        ruleset_snapshot={
            "legal": {"rules": [{"rule_id": "R-NOTICE-001", "version": 1, "approved_by": label}]}
        },
        answers={},
        applied_rules=[{"rule_id": "R-NOTICE-001", "version": 1, "effect": "warning", "message": "x"}],
        sources=[
            {
                "title": "Travail salarié",
                "reference": "D.Lgs. 286/1998, art. 22",
                "url": "",
                "consulted_on": "2026-09-21",
            }
        ],
        pathway_key="salaried_work",
    )
    client.force_login(person)
    url = f"/fr/espace-reserve/dossiers/{case.reference}/pre-evaluation/{assessment.pk}/"
    response = client.get(url)
    assert response.status_code == 200, response.status_code
    return response.content.decode()


def test_the_helper_recognises_a_demonstration_approval():
    assert is_demonstration_approval(DEMO_LABEL)
    assert is_demonstration_approval("  dimostrazione — qualunque cosa  ")
    assert not is_demonstration_approval(REAL_LABEL)
    assert not is_demonstration_approval("")


def test_a_demonstration_result_warns_the_reader(client, person):
    html = _assessment_page(client, person, DEMO_LABEL)
    assert "notice--error" in html, "no warning at all on a demonstration result"
    assert "aucun juriste" in html, "the warning does not say the rules were never approved"
    assert "ne doit servir à aucune démarche" in html


def test_the_warning_comes_before_the_outcome(client, person):
    """A reader who has already read the outcome has already believed it."""
    html = _assessment_page(client, person, DEMO_LABEL)
    assert html.index("notice--error") < html.index('class="outcome'), (
        "the warning is rendered after the outcome it is warning about"
    )


def test_a_demonstration_result_does_not_show_consultation_dates(client, person):
    """
    «consultée le 2026-09-21» next to a source is a claim that somebody opened it that day.

    Under the demonstration ruleset nobody did — the date was stamped so the chain could be walked.
    Showing it would be the single most specific false statement on the page.
    """
    html = _assessment_page(client, person, DEMO_LABEL)
    assert "sources__consulted" not in html
    assert "2026-09-21" not in html


def test_a_real_result_carries_no_warning_and_keeps_its_dates(client, person):
    """
    The control case. Without it, every assertion above passes on a page that warns about everything.
    """
    html = _assessment_page(client, person, REAL_LABEL)
    assert "aucun juriste" not in html
    assert "sources__consulted" in html
    assert "2026-09-21" in html


def test_the_page_reads_the_snapshot_not_the_live_rules(client, person, reviewer):
    """
    An assessment produced under the demonstration ruleset keeps saying so after a real ruleset
    replaces it. The reader's question is «was THIS result trustworthy», not «is the engine
    trustworthy now», and the snapshot is the only thing that can answer the first.
    """
    html = _assessment_page(client, person, DEMO_LABEL)
    assert "aucun juriste" in html

    # A genuinely approved rule now exists and is in force. The old assessment must not change.
    _rule_in_force(person, reviewer, label=REAL_LABEL)
    case_reference = html.split("dossiers/")[1].split("/")[0]
    from cases.models import CaseFile

    case = CaseFile.objects.get(reference=case_reference)
    assessment = case.assessments.order_by("-pk").first()
    response = client.get(
        f"/fr/espace-reserve/dossiers/{case.reference}/pre-evaluation/{assessment.pk}/"
    )
    assert "aucun juriste" in response.content.decode()
