"""
The bridge between the orientation questionnaire and the digital case file.

This is the step that turns a questionnaire into a product: without it the platform asks a person
ten questions about their life, shows them an answer, and forgets. Technical Blueprint §5 puts it in
sequence — «Restituzione di uno o più percorsi … **Creazione del fascicolo e checklist**» — and
REQ-PER-07 is the requirement.

What happens when a session completes:

1. A ``CaseFile`` is opened for the person, with the purpose and the pathway the outcome names.
   One case per purpose: a person who retakes the questionnaire for the same purpose updates their
   case rather than accumulating a second one, because two open files for one objective is not a
   richer record, it is an ambiguous one.
2. A ``PathwayAssessment`` freezes the WHOLE ruleset used, not a version number, so the outcome
   stays reproducible after the rules change — which is the day it matters.
3. The outcome's checklist becomes the case's checklist, with a **responsible actor on every item**.
   The orientation checklist has four categories (documents, steps, authorities, warnings); each one
   maps to who actually acts, because "who is responsible" is an acceptance criterion and an item
   that cannot answer it is invalid.

An anonymous session has no person, so nothing is created: the case appears when the visitor has an
account, and the session is attached then.
"""

from __future__ import annotations

import logging

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from cases import services
from cases.models import AssessmentOutcome, CaseFile, CasePurpose, ResponsibleActor

logger = logging.getLogger("ile.cases")

#: Orientation outcome key or pathway prefix -> the lawful purpose of the case file.
#: The questionnaire speaks of pathway families; the case file speaks of purposes, and the mapping
#: is here rather than in either model so neither has to know about the other.
PURPOSE_BY_PATHWAY_PREFIX: tuple[tuple[str, str], ...] = (
    ("work", CasePurpose.WORK),
    ("study", CasePurpose.STUDY),
    ("training", CasePurpose.TRAINING),
    ("family", CasePurpose.FAMILY),
)

#: Orientation checklist category -> who acts on it.
#: `documents` and `steps` are the person's to carry out; `authorities` names an act the competent
#: authority performs, which the applicant cannot do and must not be shown as their task; `warnings`
#: is information the project team stands behind.
RESPONSIBLE_BY_CATEGORY: dict[str, str] = {
    "documents": ResponsibleActor.PERSON,
    "steps": ResponsibleActor.PERSON,
    "authorities": ResponsibleActor.AUTHORITY,
    "warnings": ResponsibleActor.PROJECT_TEAM,
}

#: Orientation has one informative outcome family; the case file has five. A questionnaire that
#: cannot reach a STOP or a WARNING must not manufacture one, so everything it can reach maps to
#: POSSIBLE, and the two stronger outcomes stay reserved for the legal rule engine, which has the
#: sources and the validity dates to justify them.
DEFAULT_OUTCOME = AssessmentOutcome.POSSIBLE

#: Outcome keys the ruleset uses for "this needs a human", kept as data rather than guessed.
REVIEW_OUTCOME_KEYS = frozenset({"needs_individual_analysis", "review_required"})


def purpose_for(pathway_key: str, outcome_key: str) -> str:
    """The lawful purpose a pathway belongs to. Unknown pathways are OTHER, never a guess."""
    haystack = f"{pathway_key} {outcome_key}".lower()
    for prefix, purpose in PURPOSE_BY_PATHWAY_PREFIX:
        if prefix in haystack:
            return purpose
    return CasePurpose.OTHER


def outcome_for(outcome_key: str) -> str:
    return AssessmentOutcome.REVIEW_REQUIRED if outcome_key in REVIEW_OUTCOME_KEYS else DEFAULT_OUTCOME


def case_for_purpose(person, purpose: str) -> CaseFile | None:
    """The person's open case for this purpose, if any."""
    return CaseFile.objects.filter(person=person, purpose=purpose).active().order_by("-created_at").first()


@transaction.atomic
def open_case_from_session(session, *, request=None) -> CaseFile | None:
    """
    Open or update the case file a completed orientation session produces.

    Returns None for an anonymous session: there is nobody to open a file for. The session keeps its
    result, and the case appears when the visitor creates an account.
    """
    person = getattr(session, "user", None)
    if person is None or not getattr(person, "is_authenticated", True):
        return None

    result = getattr(session, "result", None)
    if result is None:
        return None

    outcome = result.outcome
    pathway_key = outcome.pathway_key or ""
    purpose = purpose_for(pathway_key, outcome.key)

    case = case_for_purpose(person, purpose)
    if case is None:
        case = services.open_case(person, purpose=purpose, pathway_key=pathway_key, request=request)
    elif case.pathway_key != pathway_key:
        case.pathway_key = pathway_key
        case.save(update_fields=["pathway_key", "updated_at"])

    legal = _legal_evaluation(person, session, case, pathway_key)

    services.record_assessment(
        case,
        outcome=_combined_outcome(outcome.key, legal),
        ruleset_version=result.ruleset_version,
        ruleset_snapshot=_combined_snapshot(session.ruleset, legal),
        answers=result.answers_snapshot or {},
        applied_rules=_applied_rules(legal),
        missing_requirements=_missing_requirements(legal),
        rationale=result.result_text_fr or "",
        sources=_sources_of(outcome, legal),
        pathway_key=pathway_key,
        request=request,
    )

    _sync_checklist(case, outcome)
    _sync_legal_checklist(case, legal)
    return case


def _snapshot_of(ruleset) -> dict:
    """The whole ruleset, serialised. A pointer stops being reproducible the day the rules change."""
    from orientation import services as orientation_services
    from orientation.engine import spec_to_dict

    return spec_to_dict(orientation_services.spec_for(ruleset))


def _legal_evaluation(person, session, case, pathway_key, answers=None):
    """
    Run the versioned legal rule engine over this case.

    Wrapped, and deliberately so: the questionnaire result is already saved by the time we get here,
    and a failure in the legal layer must degrade the explanation, never destroy the answer a person
    has just spent ten questions earning. A None return means the assessment records what the
    questionnaire alone could establish, which is exactly what it recorded before this layer existed.
    """
    if not pathway_key:
        return None
    try:
        from rules import services as rule_services
        from rules.facts import facts_for

        facts = facts_for(person=person, session=session, case=case, pathway=pathway_key, answers=answers)
        # The case's date in Rome, the platform's calendar (``timezone.localdate``, as the rule engine
        # reads «today»). ``created_at`` is held in UTC, whose date is the day before between 00:00 and
        # 02:00 in Rome: its bare ``.date()`` applied the previous day's rules to a case opened then.
        return rule_services.evaluate(facts, pathway=pathway_key, on_date=timezone.localdate(case.created_at))
    except Exception:  # noqa: BLE001 - see the docstring; the questionnaire result is already safe
        logger.exception("legal rule evaluation failed for case %s", getattr(case, "reference", "?"))
        return None


#: Rule-engine effect -> case assessment outcome. The two vocabularies are deliberately the same
#: five values, so the mapping is an identity check rather than a translation, and a sixth effect
#: appearing on one side would fail here rather than quietly become something else.
EFFECT_TO_OUTCOME: dict[str, str] = {
    "possible": AssessmentOutcome.POSSIBLE,
    "missing_requirement": AssessmentOutcome.MISSING_REQUIREMENT,
    "warning": AssessmentOutcome.WARNING,
    "stop": AssessmentOutcome.STOP,
    "review_required": AssessmentOutcome.REVIEW_REQUIRED,
}

#: How strongly each outcome speaks. The stronger of the questionnaire's answer and the legal
#: engine's answer is the one recorded: a blocking element found by a rule is not cancelled by a
#: questionnaire that knew nothing about it.
OUTCOME_RANK: dict[str, int] = {
    AssessmentOutcome.POSSIBLE: 0,
    AssessmentOutcome.WARNING: 1,
    AssessmentOutcome.MISSING_REQUIREMENT: 2,
    AssessmentOutcome.REVIEW_REQUIRED: 3,
    AssessmentOutcome.STOP: 4,
}


def _combined_outcome(outcome_key: str, legal) -> str:
    """The stronger of what the questionnaire concluded and what the rules in force conclude."""
    from_questionnaire = outcome_for(outcome_key)
    if legal is None:
        return from_questionnaire
    from_rules = EFFECT_TO_OUTCOME.get(legal.outcome, AssessmentOutcome.POSSIBLE)
    return max((from_questionnaire, from_rules), key=lambda value: OUTCOME_RANK[value])


def _combined_snapshot(ruleset, legal) -> dict:
    """
    Both rulesets, frozen together.

    An outcome now depends on two things — the questionnaire's ruleset and the legal rules in force
    on the day — so reproducing it needs both. Keeping only one would leave an assessment that can be
    replayed but not explained, which is the worse half.
    """
    snapshot = {"orientation": _snapshot_of(ruleset)}
    if legal is not None:
        snapshot["legal"] = legal.snapshot
    return snapshot


def _applied_rules(legal) -> list[dict]:
    if legal is None:
        return []
    return [
        {
            "rule_id": finding.rule_id,
            "version": finding.version,
            "effect": finding.effect,
            "message": finding.message,
        }
        for finding in legal.findings
    ]


def _missing_requirements(legal) -> list[dict]:
    if legal is None:
        return []
    return [
        {
            "rule_id": finding.rule_id,
            "requirement": finding.requirement,
            "responsible_actor": finding.responsible_actor,
        }
        for finding in legal.missing
    ]


def _sources_of(outcome, legal=None) -> list[dict]:
    """
    The sources behind an outcome, in the order they were met.

    The legal rule engine supplies them: every rule in force carries at least one, and the service
    refuses to put a rule in force without one. The pathway's own editorial references follow, and
    duplicates are dropped on the reference, so the same norm cited twice appears once.

    An outcome with no rule in force still shows no source. That remains the honest answer, and it is
    now a statement about the review queue rather than about the architecture.
    """
    collected: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(entry: dict) -> None:
        key = (entry.get("reference", ""), entry.get("title", ""))
        if key not in seen and any(key):
            seen.add(key)
            collected.append(entry)

    if legal is not None:
        for source in legal.sources:
            add(source)

    pathway_key = outcome.pathway_key or ""
    if pathway_key:
        try:
            from pathways.models import PathwaySource

            for source in PathwaySource.objects.filter(pathway__key=pathway_key).order_by("order", "id")[:6]:
                add({"title": source.title_fr, "reference": source.reference or "", "url": source.url or ""})
        except Exception:  # noqa: BLE001 - a sibling app that is absent or changed must not break intake
            logger.exception("pathway sources unavailable for %s", pathway_key)
    return collected


def _sync_checklist(case: CaseFile, outcome) -> None:
    """
    Bring the case's checklist in line with the outcome's items.

    Items already on the case keep their status: a person who has completed a requirement and then
    retakes the questionnaire must not find their work undone. Items no longer required are left in
    place rather than deleted, because a requirement that disappears from a case without a trace is
    indistinguishable from one that was never there.
    """
    existing = {item.requirement: item for item in case.checklist.all()}
    order = case.checklist.count()

    for source_item in outcome.checklist_items.all().order_by("category", "order", "id"):
        requirement = (source_item.text_fr or "").strip()
        if not requirement or requirement in existing:
            continue
        services.add_checklist_item(
            case,
            requirement=requirement,
            responsible_actor=RESPONSIBLE_BY_CATEGORY.get(source_item.category, ResponsibleActor.PERSON),
            responsible_note=_note_for(source_item.category),
            order=order,
        )
        order += 1


def _note_for(category: str) -> str:
    if category == "authorities":
        return str(_("Selon l’autorité compétente pour votre situation"))
    if category == "warnings":
        return str(_("Point d’attention signalé par l’équipe du projet"))
    return ""


def _sync_legal_checklist(case: CaseFile, legal) -> None:
    """
    Add a checklist line for every requirement the rules in force found missing.

    These lines differ from the questionnaire's in one way that matters: each carries the rule that
    produced it and the actor that rule names. A person looking at "nulla osta al lavoro" can see
    that it is the employer's step and which provision says so, instead of finding an instruction
    with no author.
    """
    if legal is None:
        return
    existing = {item.requirement for item in case.checklist.all()}
    order = case.checklist.count()
    for finding in legal.missing:
        requirement = (finding.requirement or finding.message or "").strip()
        if not requirement or requirement in existing:
            continue
        title, reference = _first_source(finding)
        services.add_checklist_item(
            case,
            requirement=requirement,
            responsible_actor=finding.responsible_actor or ResponsibleActor.PERSON,
            source_title=title,
            source_ref=reference,
            order=order,
        )
        existing.add(requirement)
        order += 1


def _first_source(finding) -> tuple[str, str]:
    """
    The source a checklist line shows: title and precise reference.

    The checklist item has its own fields for these, so the citation is structured data rather than a
    sentence appended to a note — which means the line can be rendered as a citation, searched, and
    checked against the rule that produced it.
    """
    if not finding.sources:
        return "", ""
    first = finding.sources[0]
    return str(first.get("title", ""))[:255], str(first.get("reference", ""))[:255]


@transaction.atomic
def reassess(case: CaseFile, *, request=None, reason: str = "situation_updated"):
    """
    Re-run the legal rules against the case's current facts and record a NEW assessment.

    This is what makes the orientation dynamic rather than a snapshot taken once: a person who tells
    us they now have a job offer, or who uploads the document a rule asked for, gets an outcome that
    reflects it. The previous assessment is kept — it is evidence of what was said at the time, and
    deleting it would leave the person's file unable to explain the advice they acted on.

    A new assessment is recorded only when the outcome or the findings actually moved. Re-running the
    same rules against the same facts and storing an identical row makes the history longer and
    harder to read, not richer.
    """
    last = case.assessments.order_by("-assessed_at").first()
    if last is None:
        return None

    # The answers come from the FROZEN assessment, not from the session: the session is purged on a
    # retention schedule and a reassessment must not stop working the day that happens.
    legal = _legal_evaluation(case.person, None, case, case.pathway_key, answers=last.answers)
    if legal is None:
        return None

    outcome = max(
        (last.outcome, EFFECT_TO_OUTCOME.get(legal.outcome, AssessmentOutcome.POSSIBLE)),
        key=lambda value: OUTCOME_RANK[value],
    )
    applied = _applied_rules(legal)
    if outcome == last.outcome and applied == last.applied_rules:
        return None

    snapshot = dict(last.ruleset_snapshot or {})
    snapshot["legal"] = legal.snapshot
    assessment = services.record_assessment(
        case,
        outcome=outcome,
        ruleset_version=last.ruleset_version,
        ruleset_snapshot=snapshot,
        answers=last.answers,
        applied_rules=applied,
        missing_requirements=_missing_requirements(legal),
        rationale=last.rationale,
        sources=list(legal.sources),
        pathway_key=case.pathway_key,
        request=request,
    )
    _sync_legal_checklist(case, legal)
    return assessment
