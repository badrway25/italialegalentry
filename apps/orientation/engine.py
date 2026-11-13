"""
Orientation rule engine — pure Python, deterministic, ORM-free.

A ruleset is a frozen ``RulesetSpec`` (built from the database by ``services.spec_for`` or from
JSON by ``spec_from_dict``). ``evaluate(spec, answers)`` returns either the next question to ask
or the outcome reached. ``validate(spec)`` checks the integrity of a ruleset (entry question,
dangling targets, malformed conditions, every answer path terminates).

Semantics
---------
* ``answers`` is a mapping ``question_key → value`` (``str`` for single, ``list[str]`` for multiple,
  ``bool`` for boolean questions).
* Rules are evaluated in order. The first matching rule whose ``next_question`` is not yet answered
  wins; a matching rule with an ``outcome`` terminates the evaluation. Rules pointing to an already
  answered question are skipped, so "previous" (dropping the last answer) is deterministic.
* A condition referring to an unanswered question is False (no information → no inference).
* With no answers the entry question is returned before any rule is consulted.

Conditions DSL (JSON)
---------------------
``{}`` (always true) · ``{"all": [node, ...]}`` · ``{"any": [node, ...]}`` ·
``{"question_key": "k", "op": "eq|in|not_in|is_true|is_false", "value": ...}``.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from functools import cached_property
from itertools import combinations
from typing import Any

from orientation.constants import MAX_VALIDATION_PATHS, NEEDS_INDIVIDUAL_ANALYSIS, OUTCOME_PATHWAY_KEYS

OPS: tuple[str, ...] = ("eq", "in", "not_in", "is_true", "is_false")
QUESTION_TYPES: tuple[str, ...] = ("single", "multiple", "boolean")
CHECKLIST_CATEGORIES: tuple[str, ...] = ("documents", "steps", "authorities", "warnings")
BOOLEAN_TRUE = "true"
BOOLEAN_FALSE = "false"
MULTIPLE_SUBSET_LIMIT = 5  # exhaustive subsets up to 2**5 - 1 = 31 combinations per question


class EngineError(Exception):
    """Base class for engine errors."""


class InvalidAnswer(EngineError):
    """The submitted answer is not acceptable for the question."""


class NoTransition(EngineError):
    """No rule matches the current answers (ruleset integrity problem)."""


class InvalidConditions(EngineError):
    """The conditions DSL is malformed."""


# ------------------------------------------------------------------------------------------------
# Specs
# ------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ChoiceSpec:
    key: str
    label_fr: str
    order: int = 0


@dataclass(frozen=True)
class QuestionSpec:
    key: str
    text_fr: str
    type: str = "single"
    help_fr: str = ""
    is_entry: bool = False
    order: int = 0
    choices: tuple[ChoiceSpec, ...] = ()

    @cached_property
    def choice_keys(self) -> tuple[str, ...]:
        return tuple(c.key for c in self.choices)


@dataclass(frozen=True)
class ChecklistItemSpec:
    text_fr: str
    category: str = "steps"
    order: int = 0


@dataclass(frozen=True)
class OutcomeSpec:
    key: str
    pathway_key: str
    title_fr: str
    explanation_fr: str = ""
    disclaimer_key: str = "orientation.disclaimer"
    checklist: tuple[ChecklistItemSpec, ...] = ()


@dataclass(frozen=True)
class RuleSpec:
    name: str
    conditions: Mapping[str, Any] = field(default_factory=dict)
    next_question: str | None = None
    outcome: str | None = None
    explanation_fr: str = ""
    order: int = 0


@dataclass(frozen=True)
class RulesetSpec:
    version: int
    questions: tuple[QuestionSpec, ...] = ()
    outcomes: tuple[OutcomeSpec, ...] = ()
    rules: tuple[RuleSpec, ...] = ()
    notes: str = ""

    @cached_property
    def question_map(self) -> dict[str, QuestionSpec]:
        return {q.key: q for q in self.questions}

    @cached_property
    def outcome_map(self) -> dict[str, OutcomeSpec]:
        return {o.key: o for o in self.outcomes}

    @cached_property
    def ordered_rules(self) -> tuple[RuleSpec, ...]:
        return tuple(sorted(self.rules, key=lambda r: r.order))

    @cached_property
    def entry_question(self) -> QuestionSpec | None:
        entries = [q for q in self.questions if q.is_entry]
        if len(entries) != 1:
            return None
        return entries[0]

    @cached_property
    def fallback_outcome(self) -> OutcomeSpec | None:
        for outcome in self.outcomes:
            if outcome.pathway_key == NEEDS_INDIVIDUAL_ANALYSIS:
                return outcome
        return None

    @cached_property
    def max_depth(self) -> int:
        """Longest number of questions on any path (used for the progress indicator)."""
        report = validate(self)
        return max(report.max_depth, 1)


@dataclass(frozen=True)
class NextQuestion:
    question: QuestionSpec


@dataclass(frozen=True)
class Result:
    outcome: OutcomeSpec
    rule: RuleSpec | None = None
    fallback: bool = False


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    paths: int = 0
    max_depth: int = 0
    reachable_questions: set[str] = field(default_factory=set)
    reachable_outcomes: set[str] = field(default_factory=set)
    used_rules: set[int] = field(default_factory=set)
    truncated: bool = False

    @property
    def ok(self) -> bool:
        return not self.errors


# ------------------------------------------------------------------------------------------------
# Conditions
# ------------------------------------------------------------------------------------------------
def _leaf_matches(cond: Mapping[str, Any], answers: Mapping[str, Any]) -> bool:
    key = cond.get("question_key")
    op = cond.get("op")
    if key not in answers:
        return False
    answer = answers[key]
    value = cond.get("value")
    if op == "is_true":
        return answer is True
    if op == "is_false":
        return answer is False
    if op == "eq":
        if isinstance(answer, list):
            return isinstance(value, list) and sorted(answer) == sorted(value)
        return answer == value
    if op in ("in", "not_in"):
        values = value if isinstance(value, list) else [value]
        hit = any(a in values for a in answer) if isinstance(answer, list) else answer in values
        return hit if op == "in" else not hit
    raise InvalidConditions(f"Opérateur inconnu : {op!r}")


def conditions_match(conditions: Mapping[str, Any] | None, answers: Mapping[str, Any]) -> bool:
    if not conditions:
        return True
    if "all" in conditions:
        return all(conditions_match(node, answers) for node in conditions["all"])
    if "any" in conditions:
        nodes = conditions["any"]
        return any(conditions_match(node, answers) for node in nodes) if nodes else False
    if "question_key" in conditions:
        return _leaf_matches(conditions, answers)
    raise InvalidConditions(f"Nœud de condition invalide : {conditions!r}")


def validate_conditions(conditions: Any, spec: RulesetSpec | None = None, path: str = "conditions") -> list[str]:
    """Structural (and, when ``spec`` is given, referential) validation of a conditions node."""
    errors: list[str] = []
    if conditions is None or conditions == {}:
        return errors
    if not isinstance(conditions, Mapping):
        return [f"{path} : un objet JSON est attendu"]
    if "all" in conditions or "any" in conditions:
        op = "all" if "all" in conditions else "any"
        extra = set(conditions) - {op}
        if extra:
            errors.append(f"{path} : clés inattendues {sorted(extra)}")
        nodes = conditions[op]
        if not isinstance(nodes, list):
            return errors + [f"{path}.{op} : une liste est attendue"]
        if not nodes:
            errors.append(f"{path}.{op} : liste vide")
        for i, node in enumerate(nodes):
            errors.extend(validate_conditions(node, spec, f"{path}.{op}[{i}]"))
        return errors
    if "question_key" not in conditions:
        return [f"{path} : « question_key », « all » ou « any » attendu"]
    extra = set(conditions) - {"question_key", "op", "value"}
    if extra:
        errors.append(f"{path} : clés inattendues {sorted(extra)}")
    key = conditions.get("question_key")
    op = conditions.get("op")
    if op not in OPS:
        errors.append(f"{path} : opérateur invalide {op!r} (attendu : {', '.join(OPS)})")
        return errors
    if op in ("is_true", "is_false") and "value" in conditions:
        errors.append(f"{path} : « value » n'est pas admis avec {op}")
    if op in ("eq", "in", "not_in") and "value" not in conditions:
        errors.append(f"{path} : « value » est obligatoire avec {op}")
    if spec is None:
        return errors
    question = spec.question_map.get(key)
    if question is None:
        errors.append(f"{path} : question inconnue {key!r}")
        return errors
    if question.type == "boolean":
        if op in ("in", "not_in"):
            errors.append(f"{path} : {op} n'est pas admis sur une question booléenne")
        elif op == "eq" and not isinstance(conditions.get("value"), bool):
            errors.append(f"{path} : eq sur une question booléenne exige true/false")
        return errors
    if op in ("is_true", "is_false"):
        errors.append(f"{path} : {op} n'est admis que sur une question booléenne")
        return errors
    value = conditions.get("value")
    values = value if isinstance(value, list) else [value]
    if op == "eq" and question.type == "multiple" and not isinstance(value, list):
        errors.append(f"{path} : eq sur une question à choix multiples exige une liste")
    if op == "eq" and question.type == "single" and isinstance(value, list):
        errors.append(f"{path} : eq sur une question à choix unique exige une seule valeur")
    for v in values:
        if v not in question.choice_keys:
            errors.append(f"{path} : valeur inconnue {v!r} pour la question {key!r}")
    return errors


def describe_conditions(conditions: Mapping[str, Any] | None, spec: RulesetSpec | None = None) -> str:
    """Human readable rendering for the back-office."""
    if not conditions:
        return "toujours"
    if "all" in conditions:
        return "(" + " ET ".join(describe_conditions(n, spec) for n in conditions["all"]) + ")"
    if "any" in conditions:
        return "(" + " OU ".join(describe_conditions(n, spec) for n in conditions["any"]) + ")"
    key = conditions.get("question_key", "?")
    op = conditions.get("op", "?")
    value = conditions.get("value")
    label = key
    if spec and key in spec.question_map:
        label = f"{key}"
    if op == "is_true":
        return f"{label} = oui"
    if op == "is_false":
        return f"{label} = non"
    if op == "eq":
        return f"{label} = {value!r}"
    if op == "in":
        return f"{label} ∈ {value!r}"
    if op == "not_in":
        return f"{label} ∉ {value!r}"
    return f"{label} {op} {value!r}"


# ------------------------------------------------------------------------------------------------
# Answers
# ------------------------------------------------------------------------------------------------
def normalise_answer(question: QuestionSpec, raw: Any) -> str | list[str] | bool:
    """Validate and normalise a submitted answer for ``question``."""
    if question.type == "boolean":
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, list):
            raw = raw[-1] if raw else None
        if raw == BOOLEAN_TRUE:
            return True
        if raw == BOOLEAN_FALSE:
            return False
        raise InvalidAnswer("boolean")
    if question.type == "single":
        if isinstance(raw, list):
            if len(raw) != 1:
                raise InvalidAnswer("single")
            raw = raw[0]
        if not isinstance(raw, str) or raw not in question.choice_keys:
            raise InvalidAnswer("single")
        return raw
    if question.type == "multiple":
        if isinstance(raw, str):
            raw = [raw]
        if not isinstance(raw, list) or not raw:
            raise InvalidAnswer("multiple")
        selected = {v for v in raw if isinstance(v, str)}
        if not selected or not selected <= set(question.choice_keys):
            raise InvalidAnswer("multiple")
        return [k for k in question.choice_keys if k in selected]
    raise InvalidAnswer("type")


def possible_answers(question: QuestionSpec) -> list[Any]:
    """Every value the traversal explores for a question (capped for multiple-choice questions)."""
    if question.type == "boolean":
        return [True, False]
    if question.type == "single":
        return list(question.choice_keys)
    keys = list(question.choice_keys)
    if len(keys) <= MULTIPLE_SUBSET_LIMIT:
        out: list[Any] = []
        for size in range(1, len(keys) + 1):
            out.extend(list(c) for c in combinations(keys, size))
        return out
    return [[k] for k in keys] + [keys]


# ------------------------------------------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------------------------------------------
def evaluate(spec: RulesetSpec, answers: Mapping[str, Any], *, fallback: bool = True) -> NextQuestion | Result:
    """Return the next question or the outcome for ``answers``. Deterministic."""
    if not answers:
        entry = spec.entry_question
        if entry is None:
            raise NoTransition("Aucune question d'entrée")
        return NextQuestion(entry)
    for rule in spec.ordered_rules:
        if not conditions_match(rule.conditions, answers):
            continue
        if rule.next_question is not None:
            if rule.next_question in answers:
                continue
            question = spec.question_map.get(rule.next_question)
            if question is None:
                raise NoTransition(f"Question cible inconnue : {rule.next_question!r}")
            return NextQuestion(question)
        if rule.outcome is not None:
            outcome = spec.outcome_map.get(rule.outcome)
            if outcome is None:
                raise NoTransition(f"Résultat cible inconnu : {rule.outcome!r}")
            return Result(outcome, rule)
    if fallback and spec.fallback_outcome is not None:
        return Result(spec.fallback_outcome, None, fallback=True)
    raise NoTransition(f"Aucune règle applicable pour {dict(answers)!r}")


def progress_percent(spec: RulesetSpec, answered: int) -> int:
    """0–100, rounded to a multiple of 5 so the bar can be styled without inline CSS (CSP)."""
    depth = max(spec.max_depth, 1)
    pct = int(round(100 * min(answered, depth) / depth / 5.0) * 5)
    return max(0, min(100, pct))


# ------------------------------------------------------------------------------------------------
# Integrity validation
# ------------------------------------------------------------------------------------------------
def validate(spec: RulesetSpec) -> ValidationReport:
    report = ValidationReport()
    _validate_structure(spec, report)
    if report.errors:
        return report
    _walk(spec, {}, 0, report)
    _report_unreachable(spec, report)
    return report


def _validate_structure(spec: RulesetSpec, report: ValidationReport) -> None:
    keys = [q.key for q in spec.questions]
    if len(keys) != len(set(keys)):
        report.errors.append("Clés de questions en double")
    entries = [q for q in spec.questions if q.is_entry]
    if not entries:
        report.errors.append("Aucune question d'entrée (is_entry)")
    elif len(entries) > 1:
        report.errors.append("Plusieurs questions d'entrée : " + ", ".join(q.key for q in entries))
    for q in spec.questions:
        if q.type not in QUESTION_TYPES:
            report.errors.append(f"Question {q.key!r} : type invalide {q.type!r}")
        if q.type in ("single", "multiple"):
            if len(q.choices) < 2:
                report.errors.append(f"Question {q.key!r} : au moins deux choix sont requis")
            ckeys = [c.key for c in q.choices]
            if len(ckeys) != len(set(ckeys)):
                report.errors.append(f"Question {q.key!r} : clés de choix en double")
        elif q.choices:
            report.warnings.append(f"Question {q.key!r} : les choix sont ignorés pour une question booléenne")
        if not q.text_fr.strip():
            report.errors.append(f"Question {q.key!r} : texte vide")
    okeys = [o.key for o in spec.outcomes]
    if len(okeys) != len(set(okeys)):
        report.errors.append("Clés de résultats en double")
    if not spec.outcomes:
        report.errors.append("Aucun résultat défini")
    for o in spec.outcomes:
        if o.pathway_key not in OUTCOME_PATHWAY_KEYS:
            report.errors.append(f"Résultat {o.key!r} : pathway_key inconnu {o.pathway_key!r}")
        for item in o.checklist:
            if item.category not in CHECKLIST_CATEGORIES:
                report.errors.append(f"Résultat {o.key!r} : catégorie de checklist invalide {item.category!r}")
    if spec.fallback_outcome is None:
        report.warnings.append("Aucun résultat « needs_individual_analysis » : pas de repli en cas d'impasse")
    if not spec.rules:
        report.errors.append("Aucune règle définie")
    for i, rule in enumerate(spec.ordered_rules):
        label = f"Règle #{i + 1} « {rule.name} »"
        if (rule.next_question is None) == (rule.outcome is None):
            report.errors.append(f"{label} : exactement une cible (next_question ou outcome) est requise")
        if rule.next_question is not None and rule.next_question not in spec.question_map:
            report.errors.append(f"{label} : question cible inconnue {rule.next_question!r}")
        if rule.outcome is not None and rule.outcome not in spec.outcome_map:
            report.errors.append(f"{label} : résultat cible inconnu {rule.outcome!r}")
        for err in validate_conditions(rule.conditions, spec):
            report.errors.append(f"{label} : {err}")


def _walk(spec: RulesetSpec, answers: dict[str, Any], depth: int, report: ValidationReport) -> None:
    if report.truncated:
        return
    if report.paths >= MAX_VALIDATION_PATHS:
        report.truncated = True
        report.warnings.append(f"Validation partielle : plus de {MAX_VALIDATION_PATHS} chemins de réponses")
        return
    try:
        step = evaluate(spec, answers, fallback=False)
    except NoTransition as exc:
        report.paths += 1
        report.errors.append(f"Chemin sans issue pour {answers!r} : {exc}")
        return
    if isinstance(step, Result):
        report.paths += 1
        report.max_depth = max(report.max_depth, depth)
        report.reachable_outcomes.add(step.outcome.key)
        if step.rule is not None:
            report.used_rules.add(spec.ordered_rules.index(step.rule))
        return
    question = step.question
    if question.key in answers:  # defensive: cannot happen with the skip semantics
        report.errors.append(f"Boucle détectée sur la question {question.key!r}")
        return
    if depth >= len(spec.questions):
        report.errors.append(f"Profondeur excessive après {answers!r}")
        return
    report.reachable_questions.add(question.key)
    for rule in spec.ordered_rules:
        if rule.next_question == question.key and conditions_match(rule.conditions, answers):
            report.used_rules.add(spec.ordered_rules.index(rule))
            break
    for value in possible_answers(question):
        _walk(spec, {**answers, question.key: value}, depth + 1, report)


def _report_unreachable(spec: RulesetSpec, report: ValidationReport) -> None:
    for q in spec.questions:
        if q.key not in report.reachable_questions:
            report.warnings.append(f"Question {q.key!r} jamais atteinte")
    for o in spec.outcomes:
        if o.key not in report.reachable_outcomes and o is not spec.fallback_outcome:
            report.warnings.append(f"Résultat {o.key!r} jamais atteint")
    for i, rule in enumerate(spec.ordered_rules):
        if i not in report.used_rules:
            report.warnings.append(f"Règle #{i + 1} « {rule.name} » jamais utilisée")


# ------------------------------------------------------------------------------------------------
# JSON (export / import)
# ------------------------------------------------------------------------------------------------
def spec_to_dict(spec: RulesetSpec) -> dict[str, Any]:
    return {
        "format": "ile.orientation.ruleset/1",
        "version": spec.version,
        "notes": spec.notes,
        "questions": [
            {
                "key": q.key,
                "order": q.order,
                "type": q.type,
                "is_entry": q.is_entry,
                "text_fr": q.text_fr,
                "help_fr": q.help_fr,
                "choices": [{"key": c.key, "order": c.order, "label_fr": c.label_fr} for c in q.choices],
            }
            for q in spec.questions
        ],
        "outcomes": [
            {
                "key": o.key,
                "pathway_key": o.pathway_key,
                "title_fr": o.title_fr,
                "explanation_fr": o.explanation_fr,
                "disclaimer_key": o.disclaimer_key,
                "checklist": [{"order": i.order, "category": i.category, "text_fr": i.text_fr} for i in o.checklist],
            }
            for o in spec.outcomes
        ],
        "rules": [
            {
                "order": r.order,
                "name": r.name,
                "conditions": dict(r.conditions),
                "next_question": r.next_question,
                "outcome": r.outcome,
                "explanation_fr": r.explanation_fr,
            }
            for r in spec.ordered_rules
        ],
    }


def _as_list(value: Any, what: str) -> list:
    if value is None:
        return []
    if not isinstance(value, list):
        raise InvalidConditions(f"{what} : une liste est attendue")
    return value


def spec_from_dict(data: Mapping[str, Any], version: int | None = None) -> RulesetSpec:
    if not isinstance(data, Mapping):
        raise InvalidConditions("Le document JSON doit être un objet")
    questions = tuple(
        QuestionSpec(
            key=str(q["key"]),
            text_fr=str(q.get("text_fr", "")),
            type=str(q.get("type", "single")),
            help_fr=str(q.get("help_fr", "")),
            is_entry=bool(q.get("is_entry", False)),
            order=int(q.get("order", i)),
            choices=tuple(
                ChoiceSpec(key=str(c["key"]), label_fr=str(c.get("label_fr", "")), order=int(c.get("order", j)))
                for j, c in enumerate(_as_list(q.get("choices"), f"questions[{i}].choices"))
            ),
        )
        for i, q in enumerate(_as_list(data.get("questions"), "questions"))
    )
    outcomes = tuple(
        OutcomeSpec(
            key=str(o["key"]),
            pathway_key=str(o.get("pathway_key", "")),
            title_fr=str(o.get("title_fr", "")),
            explanation_fr=str(o.get("explanation_fr", "")),
            disclaimer_key=str(o.get("disclaimer_key", "orientation.disclaimer")),
            checklist=tuple(
                ChecklistItemSpec(
                    text_fr=str(c.get("text_fr", "")),
                    category=str(c.get("category", "steps")),
                    order=int(c.get("order", j)),
                )
                for j, c in enumerate(_as_list(o.get("checklist"), f"outcomes[{i}].checklist"))
            ),
        )
        for i, o in enumerate(_as_list(data.get("outcomes"), "outcomes"))
    )
    rules = tuple(
        RuleSpec(
            name=str(r.get("name", f"rule-{i + 1}")),
            conditions=dict(r.get("conditions") or {}),
            next_question=r.get("next_question") or None,
            outcome=r.get("outcome") or None,
            explanation_fr=str(r.get("explanation_fr", "")),
            order=int(r.get("order", i)),
        )
        for i, r in enumerate(_as_list(data.get("rules"), "rules"))
    )
    return RulesetSpec(
        version=int(version if version is not None else data.get("version", 0)),
        questions=questions,
        outcomes=outcomes,
        rules=rules,
        notes=str(data.get("notes", "")),
    )


def iter_leaf_conditions(conditions: Mapping[str, Any] | None) -> Iterable[Mapping[str, Any]]:
    if not conditions:
        return
    if "all" in conditions or "any" in conditions:
        for node in conditions.get("all") or conditions.get("any") or []:
            yield from iter_leaf_conditions(node)
    else:
        yield conditions
