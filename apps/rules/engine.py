"""
The condition evaluator — pure Python, deterministic, ORM-free, and with no way to execute code.

**No ``eval``. No ``exec``. No dynamic import. No format string over user input.** The client's own
brief names unsafe rule expressions as a threat, and a rule engine is exactly where a project
reaches for ``eval`` because it is convenient. It is not available here, and the grammar below is
small enough that it never needs to be.

The grammar, deliberately small:

    {}                                              always true
    {"all": [node, ...]}                            every child true (empty list → true)
    {"any": [node, ...]}                            at least one child true (empty list → false)
    {"not": node}                                   negation
    {"field": "<name>", "op": "<op>", "value": ...} a comparison against ONE declared field

Operators: eq · ne · in · not_in · lt · lte · gt · gte · is_true · is_false · is_set · is_not_set

Two semantics that matter more than they look:

* **An unknown field is refused at save time, not at evaluation time.** ``ALLOWED_FIELDS`` is a
  closed list, so a rule cannot quietly read something nobody meant to expose.

* **A field with no value makes its comparison FALSE**, never true. No information means no
  inference. The inverse would let a rule about a document someone has not uploaded fire as though
  they had, and in this domain the cost of that is a person being told a route is closed.
"""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Mapping
from typing import Any

MAX_DEPTH = 8
MAX_NODES = 120


class InvalidCondition(ValueError):
    """The condition is not expressible in this grammar. Raised at SAVE time, never at runtime."""


#: Every field a condition may read, and what it means. A closed list: adding one is a deliberate
#: act, reviewed like any other change, and nothing outside it is reachable from a rule.
ALLOWED_FIELDS: dict[str, str] = {
    # From the orientation answers
    "objective": "The declared objective of the project (work, study, family, training, other).",
    "answers": "Raw questionnaire answers, addressed as answers.<question_key>.",
    # From the person's profile
    "age": "Age in years, derived from the date of birth.",
    "nationality": "ISO country code of nationality.",
    "residence_country": "ISO country code of residence.",
    "education_level": "Highest declared education level.",
    "years_of_experience": "Declared years of professional experience.",
    "languages": "Declared languages, as a list of codes.",
    "has_job_offer": "Whether a signed job offer exists.",
    "has_qualification_recognition": "Whether a recognition procedure has been completed.",
    # From the case
    "purpose": "The lawful purpose of the case file.",
    "pathway": "The pathway family under evaluation.",
    "documents_present": "Keys of the documents currently VALID on the case.",
}

#: A field may be addressed as ``answers.<key>`` or ``documents_present`` and so on; the prefix is
#: what is checked, so a rule cannot invent a namespace.
_PREFIXED = ("answers",)

#: The shape a sub-key may take. Plain, and deliberately so: a questionnaire key is a slug, and
#: anything that LOOKS like attribute traversal is refused even though the evaluator reads mapping
#: keys and would not honour it. A closed grammar that relies on the reader staying careful is not
#: closed — the day ``_read`` is rewritten with ``getattr`` for convenience, this is what stands.
_SUBKEY = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{0,63}$")

OPERATORS = (
    "eq",
    "ne",
    "in",
    "not_in",
    "lt",
    "lte",
    "gt",
    "gte",
    "is_true",
    "is_false",
    "is_set",
    "is_not_set",
)

_VALUELESS = frozenset({"is_true", "is_false", "is_set", "is_not_set"})
_ORDERED = frozenset({"lt", "lte", "gt", "gte"})
_COLLECTION = frozenset({"in", "not_in"})


# ------------------------------------------------------------------------------------------------
# Validation — runs when a rule is saved, so a malformed rule never reaches an evaluation
# ------------------------------------------------------------------------------------------------
def validate_condition(node: Any, *, depth: int = 0, counter: list[int] | None = None) -> None:
    counter = counter if counter is not None else [0]
    counter[0] += 1
    if counter[0] > MAX_NODES:
        raise InvalidCondition(f"condition has more than {MAX_NODES} nodes")
    if depth > MAX_DEPTH:
        raise InvalidCondition(f"condition nested deeper than {MAX_DEPTH}")
    if not isinstance(node, Mapping):
        raise InvalidCondition("every node must be an object")
    if not node:
        return  # {} is "always true"

    keys = set(node)
    if keys & {"all", "any"}:
        name = "all" if "all" in keys else "any"
        if keys - {name}:
            raise InvalidCondition(f"'{name}' must be the only key of its node")
        children = node[name]
        if not isinstance(children, list):
            raise InvalidCondition(f"'{name}' takes a list")
        for child in children:
            validate_condition(child, depth=depth + 1, counter=counter)
        return

    if "not" in keys:
        if keys - {"not"}:
            raise InvalidCondition("'not' must be the only key of its node")
        validate_condition(node["not"], depth=depth + 1, counter=counter)
        return

    if not keys <= {"field", "op", "value"}:
        raise InvalidCondition(f"unexpected keys: {sorted(keys - {'field', 'op', 'value'})}")
    field = node.get("field")
    op = node.get("op")
    if not isinstance(field, str) or not field:
        raise InvalidCondition("'field' is required and must be a string")
    root = field.split(".", 1)[0]
    if root not in ALLOWED_FIELDS:
        raise InvalidCondition(f"unknown field '{field}'; allowed: {sorted(ALLOWED_FIELDS)}")
    if "." in field:
        if root not in _PREFIXED:
            raise InvalidCondition(f"field '{root}' takes no sub-key")
        subkey = field.split(".", 1)[1]
        if subkey.startswith("_") or not _SUBKEY.match(subkey):
            raise InvalidCondition(f"invalid sub-key '{subkey}'")
    if op not in OPERATORS:
        raise InvalidCondition(f"unknown operator '{op}'; allowed: {list(OPERATORS)}")
    if op in _VALUELESS:
        if "value" in node:
            raise InvalidCondition(f"operator '{op}' takes no value")
        return
    if "value" not in node:
        raise InvalidCondition(f"operator '{op}' requires a value")
    value = node["value"]
    if op in _COLLECTION and not isinstance(value, list):
        raise InvalidCondition(f"operator '{op}' takes a list")
    if op in _ORDERED and not isinstance(value, int | float | str):
        raise InvalidCondition(f"operator '{op}' takes a number or a date string")


# ------------------------------------------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------------------------------------------
def _read(facts: Mapping[str, Any], field: str) -> Any:
    if "." in field:
        root, key = field.split(".", 1)
        container = facts.get(root)
        if isinstance(container, Mapping):
            return container.get(key)
        return None
    return facts.get(field)


def _as_comparable(value: Any) -> Any:
    """Dates arrive as ISO strings from JSON; compare them as dates, not as text."""
    if isinstance(value, str) and len(value) == 10 and value[4] == "-" and value[7] == "-":
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return value
    return value


def evaluate_condition(node: Any, facts: Mapping[str, Any]) -> bool:
    """True when the condition holds for these facts. Never raises on data; only on a bad rule."""
    if not isinstance(node, Mapping):
        raise InvalidCondition("every node must be an object")
    if not node:
        return True

    if "all" in node:
        return all(evaluate_condition(child, facts) for child in node["all"])
    if "any" in node:
        return any(evaluate_condition(child, facts) for child in node["any"])
    if "not" in node:
        return not evaluate_condition(node["not"], facts)

    field = node["field"]
    op = node["op"]
    actual = _read(facts, field)

    if op == "is_set":
        return actual not in (None, "", [], {})
    if op == "is_not_set":
        return actual in (None, "", [], {})

    # No information means no inference: an absent fact makes its comparison false, never true.
    if actual is None:
        return False

    if op == "is_true":
        return actual is True
    if op == "is_false":
        return actual is False

    expected = node.get("value")
    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "in":
        # A list fact satisfies `in` when any of its members is listed: "one of the languages
        # declared is among those required" is the question a rule actually asks.
        if isinstance(actual, list):
            return any(item in expected for item in actual)
        return actual in expected
    if op == "not_in":
        if isinstance(actual, list):
            return all(item not in expected for item in actual)
        return actual not in expected

    left, right = _as_comparable(actual), _as_comparable(expected)
    try:
        if op == "lt":
            return left < right
        if op == "lte":
            return left <= right
        if op == "gt":
            return left > right
        if op == "gte":
            return left >= right
    except TypeError:
        # Comparing a number with a word is a rule-authoring mistake, not a fact about the person:
        # it must not silently decide their outcome in either direction.
        return False
    raise InvalidCondition(f"unknown operator '{op}'")


def describe_condition(node: Any, lang: str = "fr") -> str:
    """
    A human rendering of a condition, for the rule editor and for a reviewer.

    Deliberately literal rather than fluent: a legal reviewer needs to see the structure they are
    approving, not a paraphrase of it.
    """
    if not isinstance(node, Mapping) or not node:
        return "toujours"
    if "all" in node:
        return "(" + " ET ".join(describe_condition(c, lang) for c in node["all"]) + ")"
    if "any" in node:
        return "(" + " OU ".join(describe_condition(c, lang) for c in node["any"]) + ")"
    if "not" in node:
        return "NON " + describe_condition(node["not"], lang)
    field, op = node.get("field"), node.get("op")
    if op in _VALUELESS:
        return f"{field} {op}"
    return f"{field} {op} {node.get('value')!r}"
