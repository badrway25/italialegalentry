"""
The condition evaluator.

Two properties are worth more than the rest and are tested hardest:

* the grammar is CLOSED — no code execution, no field outside the declared list, no unbounded
  nesting — and a rule that breaks it is refused when it is SAVED, not when someone is waiting for
  an answer;
* an absent fact makes its comparison FALSE. The inverse is the failure mode that matters in this
  domain: a rule about a document nobody has uploaded firing as though they had.
"""

from __future__ import annotations

import pytest

from rules.engine import (
    MAX_DEPTH,
    MAX_NODES,
    InvalidCondition,
    describe_condition,
    evaluate_condition,
    validate_condition,
)


class TestGrammarIsClosed:
    def test_an_empty_object_is_always_true(self):
        validate_condition({})
        assert evaluate_condition({}, {}) is True

    def test_an_unknown_field_is_refused(self):
        with pytest.raises(InvalidCondition, match="unknown field"):
            validate_condition({"field": "password", "op": "is_set"})

    def test_an_unknown_operator_is_refused(self):
        with pytest.raises(InvalidCondition, match="unknown operator"):
            validate_condition({"field": "age", "op": "matches_regex", "value": ".*"})

    def test_a_sub_key_on_a_field_that_takes_none_is_refused(self):
        with pytest.raises(InvalidCondition, match="takes no sub-key"):
            validate_condition({"field": "age.year", "op": "eq", "value": 30})

    def test_the_answers_namespace_takes_a_sub_key(self):
        validate_condition({"field": "answers.objective", "op": "eq", "value": "work"})

    def test_a_node_that_is_not_an_object_is_refused(self):
        with pytest.raises(InvalidCondition, match="must be an object"):
            validate_condition(["age", "eq", 30])

    def test_all_must_be_the_only_key_of_its_node(self):
        with pytest.raises(InvalidCondition, match="only key"):
            validate_condition({"all": [], "field": "age", "op": "is_set"})

    def test_an_unexpected_key_is_refused(self):
        with pytest.raises(InvalidCondition, match="unexpected keys"):
            validate_condition({"field": "age", "op": "is_set", "sql": "DROP TABLE"})

    def test_a_valueless_operator_refuses_a_value(self):
        with pytest.raises(InvalidCondition, match="takes no value"):
            validate_condition({"field": "age", "op": "is_set", "value": 1})

    def test_a_comparison_operator_requires_a_value(self):
        with pytest.raises(InvalidCondition, match="requires a value"):
            validate_condition({"field": "age", "op": "gte"})

    def test_in_requires_a_list(self):
        with pytest.raises(InvalidCondition, match="takes a list"):
            validate_condition({"field": "nationality", "op": "in", "value": "MA"})

    def test_nesting_deeper_than_the_limit_is_refused(self):
        node = {"field": "age", "op": "is_set"}
        for _ in range(MAX_DEPTH + 2):
            node = {"not": node}
        with pytest.raises(InvalidCondition, match="nested deeper"):
            validate_condition(node)

    def test_more_nodes_than_the_limit_are_refused(self):
        node = {"all": [{"field": "age", "op": "is_set"} for _ in range(MAX_NODES + 5)]}
        with pytest.raises(InvalidCondition, match="more than"):
            validate_condition(node)


class TestAbsenceMeansNoInference:
    """A fact nobody supplied must not decide anybody's outcome."""

    @pytest.mark.parametrize(
        "op,value",
        [
            ("eq", "MA"),
            ("ne", "MA"),
            ("in", ["MA"]),
            ("not_in", ["MA"]),
            ("lt", 5),
            ("gte", 5),
            ("is_true", None),
            ("is_false", None),
        ],
    )
    def test_an_absent_fact_never_makes_a_comparison_true(self, op, value):
        node = {"field": "nationality", "op": op}
        if value is not None:
            node["value"] = value
        assert evaluate_condition(node, {}) is False

    def test_is_not_set_is_the_only_way_to_test_for_absence(self):
        assert evaluate_condition({"field": "nationality", "op": "is_not_set"}, {}) is True
        assert evaluate_condition({"field": "nationality", "op": "is_set"}, {}) is False

    def test_an_empty_string_counts_as_absent(self):
        assert evaluate_condition({"field": "nationality", "op": "is_set"}, {"nationality": ""}) is False

    def test_not_of_an_absent_fact_does_not_become_an_assertion(self):
        # `not (age >= 18)` on an unknown age must not conclude "under 18" — it concludes nothing,
        # and the rule author has to say `is_not_set` if that is what they mean.
        assert evaluate_condition({"not": {"field": "age", "op": "gte", "value": 18}}, {}) is True
        assert evaluate_condition({"field": "age", "op": "lt", "value": 18}, {}) is False


class TestOperators:
    def test_equality_and_inequality(self):
        assert evaluate_condition({"field": "nationality", "op": "eq", "value": "MA"}, {"nationality": "MA"})
        assert evaluate_condition({"field": "nationality", "op": "ne", "value": "IT"}, {"nationality": "MA"})

    def test_a_list_fact_satisfies_in_when_any_member_is_listed(self):
        node = {"field": "languages", "op": "in", "value": ["fr", "en"]}
        assert evaluate_condition(node, {"languages": ["ar", "fr"]}) is True
        assert evaluate_condition(node, {"languages": ["ar"]}) is False

    def test_a_list_fact_satisfies_not_in_only_when_no_member_is_listed(self):
        node = {"field": "languages", "op": "not_in", "value": ["fr"]}
        assert evaluate_condition(node, {"languages": ["ar", "en"]}) is True
        assert evaluate_condition(node, {"languages": ["ar", "fr"]}) is False

    def test_iso_date_strings_compare_as_dates_not_as_text(self):
        node = {"field": "answers.passport_expiry", "op": "gte", "value": "2026-10-02"}
        assert evaluate_condition(node, {"answers": {"passport_expiry": "2027-01-09"}}) is True
        assert evaluate_condition(node, {"answers": {"passport_expiry": "2026-09-30"}}) is False

    def test_comparing_a_number_with_a_word_decides_nothing(self):
        # A rule-authoring mistake must not silently decide an outcome in either direction.
        node = {"field": "years_of_experience", "op": "gte", "value": 5}
        assert evaluate_condition(node, {"years_of_experience": "beaucoup"}) is False

    def test_boolean_operators_require_a_real_boolean(self):
        assert evaluate_condition({"field": "has_job_offer", "op": "is_true"}, {"has_job_offer": True}) is True
        assert evaluate_condition({"field": "has_job_offer", "op": "is_true"}, {"has_job_offer": 1}) is False


class TestComposition:
    def test_all_of_an_empty_list_is_true_and_any_of_an_empty_list_is_false(self):
        assert evaluate_condition({"all": []}, {}) is True
        assert evaluate_condition({"any": []}, {}) is False

    def test_a_realistic_composed_condition(self):
        node = {
            "all": [
                {"field": "objective", "op": "eq", "value": "work"},
                {"any": [{"field": "has_job_offer", "op": "is_false"}, {"field": "has_job_offer", "op": "is_not_set"}]},
            ]
        }
        assert evaluate_condition(node, {"objective": "work"}) is True
        assert evaluate_condition(node, {"objective": "work", "has_job_offer": True}) is False
        assert evaluate_condition(node, {"objective": "study", "has_job_offer": False}) is False


class TestNoCodeExecution:
    """The engine must not be persuadable to run anything. These are the shapes an attacker tries."""

    @pytest.mark.parametrize(
        "condition",
        [
            {"field": "__class__", "op": "is_set"},
            {"field": "answers.__class__", "op": "eq", "value": "dict"},
            {"eval": "1+1"},
            {"field": "age", "op": "__import__"},
            {"exec": {"field": "age", "op": "is_set"}},
        ],
    )
    def test_nothing_that_looks_like_code_is_accepted(self, condition):
        with pytest.raises(InvalidCondition):
            validate_condition(condition)

    def test_a_dunder_key_in_the_answers_namespace_reads_nothing(self):
        # `answers.__class__` is refused at save time; if one ever reached evaluation it would read
        # a mapping KEY, never an attribute.
        assert evaluate_condition({"field": "answers.__class__", "op": "is_set"}, {"answers": {}}) is False


class TestDescription:
    def test_a_composed_condition_reads_structurally(self):
        text = describe_condition(
            {"all": [{"field": "objective", "op": "eq", "value": "work"}, {"not": {"field": "age", "op": "is_set"}}]}
        )
        assert "ET" in text
        assert "NON" in text
        assert "objective" in text

    def test_an_empty_condition_says_always(self):
        assert describe_condition({}) == "toujours"
