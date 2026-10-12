"""Orientation test fixtures. Shared project fixtures are re-exported from ``tests/conftest.py``."""

from __future__ import annotations

import pytest
from django.test import Client

from orientation import engine
from tests.conftest import *  # noqa: F401,F403 - seeded, legal_published, phase3_open, set_flag, users…
from tests.conftest import _clear_caches  # noqa: F401 - autouse cache/flag reset (not exported by *)


@pytest.fixture
def active_ruleset(db):
    """Ruleset v1 seeded and active (the seed activates it when nothing is active)."""
    from orientation.models import Ruleset
    from orientation.seeds import seed_ruleset_v1

    seed_ruleset_v1()
    return Ruleset.objects.get(version=1)


@pytest.fixture
def mini_spec() -> engine.RulesetSpec:
    """A tiny hand-written ruleset used by the pure engine tests."""
    return engine.RulesetSpec(
        version=99,
        questions=(
            engine.QuestionSpec(
                key="q1",
                text_fr="Q1 ?",
                is_entry=True,
                order=1,
                choices=(
                    engine.ChoiceSpec("a", "A", 1),
                    engine.ChoiceSpec("b", "B", 2),
                    engine.ChoiceSpec("c", "C", 3),
                ),
            ),
            engine.QuestionSpec(
                key="q2",
                text_fr="Q2 ?",
                type="multiple",
                order=2,
                choices=(engine.ChoiceSpec("x", "X", 1), engine.ChoiceSpec("y", "Y", 2)),
            ),
            engine.QuestionSpec(key="q3", text_fr="Q3 ?", type="boolean", order=3),
        ),
        outcomes=(
            engine.OutcomeSpec("o_a", "salaried_work", "A"),
            engine.OutcomeSpec("o_b", "study_and_training_in_italy", "B"),
            engine.OutcomeSpec("o_nia", "needs_individual_analysis", "NIA"),
        ),
        rules=(
            engine.RuleSpec("q1=a → q2", {"question_key": "q1", "op": "eq", "value": "a"}, next_question="q2", order=1),
            engine.RuleSpec(
                "q1=a & q2 has x → q3",
                {
                    "all": [
                        {"question_key": "q1", "op": "eq", "value": "a"},
                        {"question_key": "q2", "op": "in", "value": ["x"]},
                    ]
                },
                next_question="q3",
                order=2,
            ),
            engine.RuleSpec(
                "q1=a & q3 yes → o_a",
                {"all": [{"question_key": "q1", "op": "eq", "value": "a"}, {"question_key": "q3", "op": "is_true"}]},
                outcome="o_a",
                order=3,
            ),
            engine.RuleSpec(
                "q1=a & q3 no → o_b",
                {"all": [{"question_key": "q1", "op": "eq", "value": "a"}, {"question_key": "q3", "op": "is_false"}]},
                outcome="o_b",
                order=4,
            ),
            engine.RuleSpec(
                "q1=a & q2 without x → o_b",
                {
                    "all": [
                        {"question_key": "q1", "op": "eq", "value": "a"},
                        {"question_key": "q2", "op": "not_in", "value": ["x"]},
                    ]
                },
                outcome="o_b",
                order=5,
            ),
            engine.RuleSpec(
                "q1 in b,c → nia", {"question_key": "q1", "op": "in", "value": ["b", "c"]}, outcome="o_nia", order=6
            ),
        ),
    )


@pytest.fixture
def other_client():
    return Client()


def walk(client, session_url: str, answers: list[tuple[str, object]]):
    """Answer a list of (question_key, value) through the HTML wizard; return the last response."""
    response = None
    for key, value in answers:
        data = {"question_key": key, "answer": value, "action": "answer"}
        response = client.post(session_url, data)
    return response
