"""Pure engine tests — no database."""

import pytest

from orientation import engine


def test_entry_question_first(mini_spec):
    step = engine.evaluate(mini_spec, {})
    assert isinstance(step, engine.NextQuestion)
    assert step.question.key == "q1"


def test_branching_and_termination(mini_spec):
    step = engine.evaluate(mini_spec, {"q1": "a"})
    assert isinstance(step, engine.NextQuestion) and step.question.key == "q2"
    step = engine.evaluate(mini_spec, {"q1": "a", "q2": ["x"]})
    assert isinstance(step, engine.NextQuestion) and step.question.key == "q3"
    result = engine.evaluate(mini_spec, {"q1": "a", "q2": ["x"], "q3": True})
    assert isinstance(result, engine.Result) and result.outcome.key == "o_a"
    result = engine.evaluate(mini_spec, {"q1": "a", "q2": ["x"], "q3": False})
    assert result.outcome.key == "o_b"
    result = engine.evaluate(mini_spec, {"q1": "a", "q2": ["y"]})
    assert result.outcome.key == "o_b"
    result = engine.evaluate(mini_spec, {"q1": "b"})
    assert result.outcome.key == "o_nia" and result.fallback is False


def test_deterministic_and_previous_is_reversible(mini_spec):
    first = engine.evaluate(mini_spec, {"q1": "a", "q2": ["x"]})
    second = engine.evaluate(mini_spec, {"q1": "a", "q2": ["x"]})
    assert first == second
    # dropping the last answer asks the same question again
    again = engine.evaluate(mini_spec, {"q1": "a"})
    assert again.question.key == "q2"


def test_unanswered_condition_is_false():
    assert engine.conditions_match({"question_key": "missing", "op": "not_in", "value": ["x"]}, {}) is False
    assert engine.conditions_match({"question_key": "missing", "op": "is_false"}, {}) is False
    assert engine.conditions_match({}, {}) is True
    assert engine.conditions_match(None, {"a": 1}) is True


def test_any_all_nesting():
    cond = {"any": [{"question_key": "a", "op": "eq", "value": "1"}, {"all": [{"question_key": "b", "op": "is_true"}]}]}
    assert engine.conditions_match(cond, {"b": True}) is True
    assert engine.conditions_match(cond, {"a": "2", "b": False}) is False
    assert engine.conditions_match({"any": []}, {"a": "1"}) is False


def test_eq_on_multiple_compares_sets():
    cond = {"question_key": "m", "op": "eq", "value": ["y", "x"]}
    assert engine.conditions_match(cond, {"m": ["x", "y"]}) is True
    assert engine.conditions_match(cond, {"m": ["x"]}) is False


def test_invalid_operator_raises():
    with pytest.raises(engine.InvalidConditions):
        engine.conditions_match({"question_key": "a", "op": "like", "value": "x"}, {"a": "x"})
    with pytest.raises(engine.InvalidConditions):
        engine.conditions_match({"foo": "bar"}, {"a": "x"})


def test_fallback_outcome_when_no_rule_matches(mini_spec):
    spec = engine.RulesetSpec(
        version=1,
        questions=mini_spec.questions,
        outcomes=mini_spec.outcomes,
        rules=(mini_spec.rules[0],),  # only q1=a → q2 ; everything else is a dead end
    )
    result = engine.evaluate(spec, {"q1": "b"})
    assert result.outcome.key == "o_nia" and result.fallback is True
    with pytest.raises(engine.NoTransition):
        engine.evaluate(spec, {"q1": "b"}, fallback=False)


def test_no_entry_question_raises():
    spec = engine.RulesetSpec(version=1, questions=(engine.QuestionSpec("q", "Q", choices=()),))
    with pytest.raises(engine.NoTransition):
        engine.evaluate(spec, {})


def test_normalise_answers(mini_spec):
    q1, q2, q3 = mini_spec.questions
    assert engine.normalise_answer(q1, "a") == "a"
    assert engine.normalise_answer(q1, ["b"]) == "b"
    assert engine.normalise_answer(q2, ["y", "x", "x"]) == ["x", "y"]
    assert engine.normalise_answer(q2, "x") == ["x"]
    assert engine.normalise_answer(q3, "true") is True
    assert engine.normalise_answer(q3, ["false"]) is False
    for question, bad in ((q1, "zzz"), (q1, ["a", "b"]), (q2, []), (q2, ["nope"]), (q3, "yes"), (q3, None)):
        with pytest.raises(engine.InvalidAnswer):
            engine.normalise_answer(question, bad)


def test_validate_ok_mini(mini_spec):
    report = engine.validate(mini_spec)
    assert report.ok, report.errors
    assert report.reachable_outcomes == {"o_a", "o_b", "o_nia"}
    assert report.reachable_questions == {"q1", "q2", "q3"}
    assert report.max_depth == 3
    assert report.paths > 0
    assert mini_spec.max_depth == 3


def test_validate_reports_dangling_targets_and_bad_conditions(mini_spec):
    bad_rules = (
        engine.RuleSpec("dangling q", {}, next_question="nope", order=1),
        engine.RuleSpec("dangling o", {}, outcome="nope", order=2),
        engine.RuleSpec("both", {}, next_question="q2", outcome="o_a", order=3),
        engine.RuleSpec("none", {}, order=4),
        engine.RuleSpec("bad op", {"question_key": "q1", "op": "gt", "value": "a"}, outcome="o_a", order=5),
        engine.RuleSpec("bad value", {"question_key": "q1", "op": "eq", "value": "zzz"}, outcome="o_a", order=6),
        engine.RuleSpec("unknown q", {"question_key": "qX", "op": "eq", "value": "a"}, outcome="o_a", order=7),
        engine.RuleSpec("bool in", {"question_key": "q3", "op": "in", "value": [True]}, outcome="o_a", order=8),
        engine.RuleSpec("is_true on single", {"question_key": "q1", "op": "is_true"}, outcome="o_a", order=9),
        engine.RuleSpec("empty all", {"all": []}, outcome="o_a", order=10),
    )
    spec = engine.RulesetSpec(1, mini_spec.questions, mini_spec.outcomes, bad_rules)
    report = engine.validate(spec)
    assert not report.ok
    joined = "\n".join(report.errors)
    for fragment in (
        "question cible inconnue 'nope'",
        "résultat cible inconnu 'nope'",
        "exactement une cible",
        "opérateur invalide 'gt'",
        "valeur inconnue 'zzz'",
        "question inconnue 'qX'",
        "n'est pas admis sur une question booléenne",
        "n'est admis que sur une question booléenne",
        "liste vide",
    ):
        assert fragment in joined, fragment


def test_validate_entry_question_errors(mini_spec):
    no_entry = tuple(
        engine.QuestionSpec(q.key, q.text_fr, q.type, q.help_fr, False, q.order, q.choices) for q in mini_spec.questions
    )
    report = engine.validate(engine.RulesetSpec(1, no_entry, mini_spec.outcomes, mini_spec.rules))
    assert any("Aucune question d'entrée" in e for e in report.errors)
    two_entries = tuple(
        engine.QuestionSpec(q.key, q.text_fr, q.type, q.help_fr, True, q.order, q.choices) for q in mini_spec.questions
    )
    report = engine.validate(engine.RulesetSpec(1, two_entries, mini_spec.outcomes, mini_spec.rules))
    assert any("Plusieurs questions d'entrée" in e for e in report.errors)


def test_validate_detects_non_terminating_path(mini_spec):
    rules = (mini_spec.rules[0], mini_spec.rules[5])  # q1=a → q2, but nothing after q2
    report = engine.validate(engine.RulesetSpec(1, mini_spec.questions, mini_spec.outcomes, rules))
    assert not report.ok
    assert any("Chemin sans issue" in e for e in report.errors)


def test_validate_warns_unreachable(mini_spec):
    extra_outcome = (*mini_spec.outcomes, engine.OutcomeSpec("o_never", "scientific_research", "never"))
    report = engine.validate(engine.RulesetSpec(1, mini_spec.questions, extra_outcome, mini_spec.rules))
    assert report.ok
    assert any("o_never" in w for w in report.warnings)


def test_validate_rejects_unknown_pathway_key(mini_spec):
    outcomes = (*mini_spec.outcomes, engine.OutcomeSpec("bad", "visa_express", "x"))
    report = engine.validate(engine.RulesetSpec(1, mini_spec.questions, outcomes, mini_spec.rules))
    assert any("pathway_key inconnu 'visa_express'" in e for e in report.errors)


def test_progress_percent(mini_spec):
    assert engine.progress_percent(mini_spec, 0) == 0
    assert engine.progress_percent(mini_spec, 1) in (30, 35)
    assert engine.progress_percent(mini_spec, 3) == 100
    assert engine.progress_percent(mini_spec, 10) == 100


def test_json_round_trip(mini_spec):
    data = engine.spec_to_dict(mini_spec)
    assert data["format"] == "ile.orientation.ruleset/1"
    back = engine.spec_from_dict(data)
    assert back == mini_spec
    assert engine.validate(back).ok
    assert engine.spec_from_dict(data, version=7).version == 7


def test_spec_from_dict_rejects_garbage():
    with pytest.raises(engine.InvalidConditions):
        engine.spec_from_dict([])  # type: ignore[arg-type]
    with pytest.raises(engine.InvalidConditions):
        engine.spec_from_dict({"questions": "nope"})


def test_describe_conditions():
    text = engine.describe_conditions(
        {
            "all": [
                {"question_key": "a", "op": "eq", "value": "1"},
                {
                    "any": [
                        {"question_key": "b", "op": "is_true"},
                        {"question_key": "c", "op": "not_in", "value": ["z"]},
                    ]
                },
            ]
        }
    )
    assert "a = '1'" in text and "b = oui" in text and "c ∉ ['z']" in text and " ET " in text and " OU " in text
    assert engine.describe_conditions({}) == "toujours"


def test_possible_answers_caps_multiple():
    big = engine.QuestionSpec("m", "M", "multiple", choices=tuple(engine.ChoiceSpec(str(i), str(i)) for i in range(8)))
    values = engine.possible_answers(big)
    assert len(values) == 9  # 8 singletons + full set
    small = engine.QuestionSpec(
        "m", "M", "multiple", choices=(engine.ChoiceSpec("a", "A"), engine.ChoiceSpec("b", "B"))
    )
    assert engine.possible_answers(small) == [["a"], ["b"], ["a", "b"]]
