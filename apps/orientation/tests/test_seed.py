"""Seed validity: neutral questions, every outcome maps to a locked pathway key, no promises."""

import re

import pytest

from cms import locked_content
from cms.forbidden import scan
from orientation import engine
from orientation.constants import DISCLAIMER_VERSION, NEEDS_INDIVIDUAL_ANALYSIS, PATHWAY_KEYS
from orientation.models import Ruleset, RulesetStatus
from orientation.seeds import build_v1_spec, seed_ruleset_v1

PROMISE_PATTERNS = [
    r"visa garanti",
    r"résultat garanti",
    r"garanti[es]?\b",
    r"entrée assurée",
    r"guaranteed",
    r"visto garantito",
    r"certitude",
    r"approbation",
    r"prévision de visa",
    r"\bmatching\b",
    r"CONTENT_PENDING_LEGAL_REVIEW",
]


def _all_public_texts(spec: engine.RulesetSpec) -> list[str]:
    texts = []
    for q in spec.questions:
        texts += [q.text_fr, q.help_fr, *(c.label_fr for c in q.choices)]
    for o in spec.outcomes:
        texts += [o.title_fr, o.explanation_fr, *(i.text_fr for i in o.checklist)]
    for r in spec.rules:
        texts.append(r.explanation_fr)
    return [t for t in texts if t]


def test_v1_spec_is_valid():
    report = engine.validate(build_v1_spec())
    assert report.ok, report.errors
    assert report.truncated is False


def test_v1_pathway_keys_are_locked_keys():
    spec = build_v1_spec()
    locked_keys = {e["key"] for e in locked_content.get("p3.persons.pathways", "fr")[0]}
    assert set(PATHWAY_KEYS) == locked_keys and len(PATHWAY_KEYS) == 8
    mapped = {o.pathway_key for o in spec.outcomes}
    assert mapped == locked_keys | {NEEDS_INDIVIDUAL_ANALYSIS}, "every locked pathway must be reachable by an outcome"


def test_v1_every_outcome_reachable():
    spec = build_v1_spec()
    report = engine.validate(spec)
    assert report.reachable_outcomes == {o.key for o in spec.outcomes}
    assert report.reachable_questions == {q.key for q in spec.questions}
    assert not [w for w in report.warnings if "jamais" in w], report.warnings


def test_v1_texts_have_no_forbidden_or_promise_wording():
    for text in _all_public_texts(build_v1_spec()):
        assert not scan(text), text
        for pattern in PROMISE_PATTERNS:
            assert not re.search(pattern, text, flags=re.IGNORECASE), (pattern, text)
        assert "®" not in text


def test_v1_disclaimer_is_not_stored():
    """The locked sentence is rendered by the template, never copied into ruleset texts."""
    disclaimer = locked_content.text("p3.persons.how_it_works", "fr")
    for text in _all_public_texts(build_v1_spec()):
        assert disclaimer not in text
        assert "Aucun résultat administratif" not in text


def test_v1_questions_are_situational_not_legal():
    spec = build_v1_spec()
    for q in spec.questions:
        assert not re.search(r"art\.\s*\d+|D\.Lgs|décret|quota|nulla osta|permesso", q.text_fr, flags=re.IGNORECASE), (
            q.key
        )


def test_disclaimer_version_constant():
    assert DISCLAIMER_VERSION == "2026-09-17.1"


@pytest.mark.django_db
def test_seed_is_idempotent_and_activates_once():
    assert seed_ruleset_v1().startswith("ruleset v1 created")
    assert seed_ruleset_v1() == "ruleset v1 present"
    assert Ruleset.objects.count() == 1
    ruleset = Ruleset.objects.get(version=1)
    assert ruleset.status == RulesetStatus.ACTIVE
    assert ruleset.questions.count() == 5
    assert ruleset.outcomes.count() == 9
    assert ruleset.rules.count() == 15
    assert ruleset.questions.filter(is_entry=True).count() == 1
    assert "CONTENT_PENDING_LEGAL_REVIEW" in ruleset.notes


@pytest.mark.django_db
def test_seed_does_not_override_editorial_changes():
    seed_ruleset_v1()
    q = Ruleset.objects.get(version=1).questions.get(key="objective")
    q.help_fr = "Aide modifiée par la rédaction"
    q.save()
    seed_ruleset_v1()
    q.refresh_from_db()
    assert q.help_fr == "Aide modifiée par la rédaction"


@pytest.mark.django_db
def test_seed_does_not_activate_when_another_ruleset_is_active():
    Ruleset.objects.create(version=5, status=RulesetStatus.ACTIVE)
    seed_ruleset_v1()
    assert Ruleset.objects.get(version=1).status == RulesetStatus.DRAFT
    assert Ruleset.objects.filter(status=RulesetStatus.ACTIVE).count() == 1


@pytest.mark.django_db
def test_seed_all_registers_orientation(seeded):
    assert Ruleset.objects.filter(version=1, status=RulesetStatus.ACTIVE).exists()
