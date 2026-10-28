"""
The documents that count the seeded legal rules say what the seed writes (W4-D part 2, A5).

Two older documents said «13 bozze … e 3 candidate ereditate» while ``apps/rules/seeds.py`` writes 16 candidates:
``ACTIVE_RULES`` at ``DRAFT`` (drafted from the norm) and ``REVIEW_RULES`` at ``LEGACY_CANDIDATE`` (taken from the
previous platform). The counts are read here from the database after ``seed_all``, not from the source text, so the
documents follow what a deployment actually holds; the release notes' line is held to the same figures.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from rules.models import LegalRule, LegalSource, ReviewStatus

pytestmark = pytest.mark.django_db

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / "docs" / "platform" / "RULE_ENGINE_GOVERNANCE.md"
QA_REPORT = ROOT / "docs" / "QA_REPORT.md"
RELEASE_NOTES = ROOT / "docs" / "RELEASE_NOTES_v2.0.0.md"


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


@pytest.fixture
def counts(seeded):
    drafted = LegalRule.objects.filter(review_status=ReviewStatus.DRAFT)
    legacy = LegalRule.objects.filter(review_status=ReviewStatus.LEGACY_CANDIDATE)
    return {
        "drafted": drafted.count(),
        "legacy": legacy.count(),
        "total": LegalRule.objects.count(),
        "sources": LegalSource.objects.count(),
        "in_force": LegalRule.objects.filter(review_status=ReviewStatus.ACTIVE).count(),
        "drafted_pathways": set(drafted.values_list("pathway", flat=True)),
        "legacy_by_pathway": {
            pathway: legacy.filter(pathway=pathway).count() for pathway in set(legacy.values_list("pathway", flat=True))
        },
    }


def test_the_seed_writes_sixteen_candidates_and_puts_none_in_force(counts):
    assert (counts["drafted"], counts["legacy"], counts["total"], counts["in_force"]) == (11, 5, 16, 0)
    assert counts["sources"] == 15


def test_the_governance_document_counts_what_the_seed_writes(counts):
    text = _read(GOVERNANCE)
    assert f"{counts['drafted']} bozze redatte dalla norma e {counts['legacy']} candidate ereditate" in text
    assert "13 bozze" not in text and "3 candidate ereditate" not in text
    assert f"**{counts['legacy']} regole in coda di revisione**" in text
    # The coverage row read «in vigore» while no rule is: seven pathways have a drafted rule, the eighth only a
    # legacy candidate.
    assert len(counts["drafted_pathways"]) == 7
    assert "training_in_origin_country" not in counts["drafted_pathways"]
    assert counts["legacy_by_pathway"]["training_in_origin_country"] == 1
    assert "7 degli 8 percorsi hanno almeno una regola redatta dalla norma" in text
    assert "hanno almeno una regola in vigore" not in text


def test_the_qa_report_counts_what_the_seed_writes(counts):
    text = _read(QA_REPORT)
    assert f"{counts['drafted']} bozze + {counts['legacy']} candidate ereditate" in text
    assert "13 bozze" not in text


def test_the_release_notes_count_what_the_seed_writes(counts):
    text = _read(RELEASE_NOTES)
    assert (
        f"{counts['total']} candidates — {counts['drafted']} drafted from the norm, {counts['legacy']} taken from the"
        in " ".join(text.split())
    )
