"""
Assembling the facts a rule reads.

The engine's ``ALLOWED_FIELDS`` is a contract in two directions: a rule may read nothing outside it,
and this module is what has to supply it. Keeping the assembly in one place means there is a single
answer to "where did this fact come from", which is the question anyone disputing an outcome asks
first.

Two rules govern what goes in:

* **Only what the person actually told us.** Nothing is inferred from a name, a country or a
  language. An absent fact stays absent, and the engine treats absence as "no inference" rather than
  as a false value, so a rule never fires on something nobody said.
* **The answers keep their own namespace.** ``answers.<question_key>`` holds the questionnaire
  verbatim, so a rule can address a specific choice without this module having to anticipate it.
"""

from __future__ import annotations

import datetime as dt
import logging
from typing import Any

from django.utils import timezone

logger = logging.getLogger("ile.rules")

#: Questionnaire answer key -> the top-level fact it also supplies.
#: A small, declared list. Everything else stays under ``answers.`` and is addressed there, because
#: promoting an answer to a first-class fact is a decision about meaning, not a convenience.
PROMOTED_ANSWERS: dict[str, str] = {
    "objective": "objective",
}


def facts_for(*, person=None, session=None, case=None, pathway: str = "", answers=None) -> dict[str, Any]:
    """
    Build the fact set for one evaluation. Every source is optional; none of them is invented.

    ``answers`` may be supplied directly by a caller that already holds them — a reassessment reads
    them from the frozen assessment rather than from the session, which the retention policy will
    eventually purge. The facts must not depend on a record that is designed to disappear.
    """
    facts: dict[str, Any] = {}

    answers = dict(answers) if answers else _answers_of(session)
    if answers:
        facts["answers"] = answers
        for answer_key, fact_name in PROMOTED_ANSWERS.items():
            if answer_key in answers:
                facts[fact_name] = answers[answer_key]

    if pathway:
        facts["pathway"] = pathway
    if case is not None:
        facts["purpose"] = case.purpose
        facts["pathway"] = facts.get("pathway") or case.pathway_key
        facts["documents_present"] = _documents_present(case)

    if person is not None:
        facts.update(_profile_facts(person))

    return {key: value for key, value in facts.items() if value not in (None, "")}


def _answers_of(session) -> dict:
    if session is None:
        return {}
    result = getattr(session, "result", None)
    snapshot = getattr(result, "answers_snapshot", None) if result is not None else None
    return dict(snapshot or getattr(session, "answers", {}) or {})


def _profile_facts(person) -> dict[str, Any]:
    profile = getattr(person, "person_profile", None)
    if profile is None:
        return {}
    facts: dict[str, Any] = {}
    residence = getattr(profile, "country_of_residence", "")
    if residence:
        facts["residence_country"] = residence
    for name in (
        "nationality",
        "education_level",
        "years_of_experience",
        "has_job_offer",
        "has_qualification_recognition",
    ):
        value = getattr(profile, name, None)
        if value not in (None, ""):
            facts[name] = value
    languages = getattr(profile, "languages", None)
    if languages:
        facts["languages"] = list(languages)
    age = _age_of(getattr(profile, "date_of_birth", None))
    if age is not None:
        facts["age"] = age
    return facts


def _age_of(date_of_birth) -> int | None:
    """
    Age in completed years.

    The rule engine reads an age, never a date of birth: a rule that could compare dates of birth
    directly would be one refactor away from holding one, and the fact set is copied into every
    assessment snapshot. An integer is the whole of what a rule needs.
    """
    if not isinstance(date_of_birth, dt.date):
        return None
    today = timezone.localdate()
    years = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        years -= 1
    return max(years, 0)


def _documents_present(case) -> list[str]:
    """
    Codes of the pieces the case has actually obtained.

    This used to import ``documents.models.CaseDocument`` and ``DocumentState`` — names that app has
    never had. Both imports failed, both were swallowed, and the fact was therefore permanently and
    SILENTLY empty: a rule requiring a document could never be satisfied, and nothing said so. That
    is the failure mode a defensive ``except`` around an import creates, and it is why the fallback
    is now narrow and the call goes through a function the other app declares for this purpose.

    ``valid_document_codes`` derives the state rather than reading the cached column, so a piece that
    lapsed overnight stops counting immediately instead of when the reconciliation next runs.
    """
    try:
        from documents.services import valid_document_codes
    except ImportError:  # the document module is not installed in this deployment
        logger.warning("documents module absent: documents_present will be empty")
        return []
    try:
        return valid_document_codes(case)
    except Exception:  # noqa: BLE001 - a failure here must not lose the assessment
        logger.exception("valid_document_codes failed for case %s", getattr(case, "reference", "?"))
        return []
