"""
Orientation services — the only place where views, admin and commands touch the domain.

Sessions are private: a session is reachable by the browser that created it (Django session),
by the owning user, or by the resume token (stored hashed). Everything else is 404.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import logging
import secrets
from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, QuerySet
from django.http import Http404
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from cms.translation import resolve
from core import clock
from core.privacy import hashed_client_ip
from orientation import constants, engine
from orientation.models import (
    ChecklistCategory,
    ChecklistItem,
    Choice,
    OrientationResult,
    OrientationSession,
    Outcome,
    Question,
    Rule,
    Ruleset,
    RulesetStatus,
    SessionStatus,
)

log = logging.getLogger("ile.orientation")


class RulesetInvalid(Exception):
    def __init__(self, report: engine.ValidationReport):
        super().__init__("; ".join(report.errors))
        self.report = report


class NoActiveRuleset(Exception):
    pass


# ------------------------------------------------------------------------------------------------
# Ruleset ↔ spec
# ------------------------------------------------------------------------------------------------
def spec_for(ruleset: Ruleset) -> engine.RulesetSpec:
    """Build the pure engine spec from the database (few small queries; rulesets are tiny)."""
    questions = tuple(
        engine.QuestionSpec(
            key=q.key,
            text_fr=q.text_fr,
            type=q.type,
            help_fr=q.help_fr,
            is_entry=q.is_entry,
            order=q.order,
            choices=tuple(engine.ChoiceSpec(c.key, c.label_fr, c.order) for c in q.choices.all()),
        )
        for q in ruleset.questions.prefetch_related("choices").order_by("order", "id")
    )
    outcomes = tuple(
        engine.OutcomeSpec(
            key=o.key,
            pathway_key=o.pathway_key,
            title_fr=o.title_fr,
            explanation_fr=o.explanation_fr,
            disclaimer_key=o.disclaimer_key,
            checklist=tuple(
                engine.ChecklistItemSpec(i.text_fr, i.category, i.order)
                for i in sorted(o.checklist_items.all(), key=lambda i: (i.order, i.pk))
            ),
        )
        for o in ruleset.outcomes.prefetch_related("checklist_items").order_by("id")
    )
    rules = tuple(
        engine.RuleSpec(
            name=r.name,
            conditions=dict(r.conditions or {}),
            next_question=r.next_question.key if r.next_question_id else None,
            outcome=r.outcome.key if r.outcome_id else None,
            explanation_fr=r.explanation_fr,
            order=r.order,
        )
        for r in ruleset.rules.select_related("next_question", "outcome").order_by("order", "id")
    )
    return engine.RulesetSpec(ruleset.version, questions, outcomes, rules, ruleset.notes)


def validate_ruleset(ruleset: Ruleset) -> engine.ValidationReport:
    return engine.validate(spec_for(ruleset))


def active_ruleset() -> Ruleset | None:
    return Ruleset.objects.filter(status=RulesetStatus.ACTIVE).first()


@transaction.atomic
def activate_ruleset(ruleset: Ruleset, user=None, request=None) -> Ruleset:
    """Validate then activate ``ruleset``; the previously active one is retired. Atomic."""
    report = validate_ruleset(ruleset)
    if not report.ok:
        raise RulesetInvalid(report)
    now = clock.now()
    Ruleset.objects.filter(status=RulesetStatus.ACTIVE).exclude(pk=ruleset.pk).update(status=RulesetStatus.RETIRED)
    ruleset.status = RulesetStatus.ACTIVE
    ruleset.activated_at = now
    ruleset.save(update_fields=["status", "activated_at", "updated_at"])
    audit_record(
        request,
        action="orientation.ruleset.activated",
        target=ruleset,
        actor=user,
        metadata={"version": ruleset.version, "warnings": report.warnings[:20]},
    )
    return ruleset


def export_ruleset(ruleset: Ruleset) -> dict[str, Any]:
    return engine.spec_to_dict(spec_for(ruleset))


@transaction.atomic
def import_ruleset(data: dict[str, Any], version: int | None = None, user=None, notes: str = "") -> Ruleset:
    """Create a DRAFT ruleset from an exported JSON document. Refuses an existing version."""
    if version is None:
        latest = Ruleset.objects.order_by("-version").values_list("version", flat=True).first()
        version = (latest or 0) + 1
    if Ruleset.objects.filter(version=version).exists():
        raise ValidationError(_("La versione %(v)s esiste già.") % {"v": version})
    spec = engine.spec_from_dict(data, version=version)
    ruleset = Ruleset.objects.create(
        version=version, status=RulesetStatus.DRAFT, notes=notes or spec.notes, created_by=user
    )
    materialise_spec(ruleset, spec)
    return ruleset


def materialise_spec(ruleset: Ruleset, spec: engine.RulesetSpec) -> None:
    """Write the spec rows into an (empty) ruleset."""
    qmap: dict[str, Question] = {}
    for q in spec.questions:
        question = Question.objects.create(
            ruleset=ruleset,
            key=q.key,
            order=q.order,
            text_fr=q.text_fr,
            help_fr=q.help_fr,
            type=q.type,
            is_entry=q.is_entry,
        )
        qmap[q.key] = question
        for c in q.choices:
            Choice.objects.create(question=question, key=c.key, order=c.order, label_fr=c.label_fr)
    omap: dict[str, Outcome] = {}
    for o in spec.outcomes:
        outcome = Outcome.objects.create(
            ruleset=ruleset,
            key=o.key,
            pathway_key=o.pathway_key,
            title_fr=o.title_fr,
            explanation_fr=o.explanation_fr,
            disclaimer_key=o.disclaimer_key,
        )
        omap[o.key] = outcome
        for item in o.checklist:
            ChecklistItem.objects.create(
                outcome=outcome, order=item.order, category=item.category, text_fr=item.text_fr
            )
    for r in spec.ordered_rules:
        Rule.objects.create(
            ruleset=ruleset,
            order=r.order,
            name=r.name,
            conditions=dict(r.conditions),
            next_question=qmap.get(r.next_question) if r.next_question else None,
            outcome=omap.get(r.outcome) if r.outcome else None,
            explanation_fr=r.explanation_fr,
        )


# ------------------------------------------------------------------------------------------------
# Resume tokens
# ------------------------------------------------------------------------------------------------
def _hash_token(token: str) -> str:
    return hashlib.sha256(f"{settings.SECRET_KEY}:{token}".encode()).hexdigest()


def new_resume_token() -> str:
    return secrets.token_hex(constants.RESUME_TOKEN_LENGTH // 2)


def normalise_token(raw: str) -> str:
    return "".join(ch for ch in (raw or "").strip().lower() if ch in "0123456789abcdef")


# ------------------------------------------------------------------------------------------------
# Browser (Django session) bookkeeping
# ------------------------------------------------------------------------------------------------
def _browser_ids(request) -> list[str]:
    try:
        ids = request.session.get(constants.BROWSER_SESSION_KEY) or []
    except AttributeError:  # no session middleware (unit tests with RequestFactory)
        return []
    return [str(i) for i in ids]


def remember_in_browser(request, session: OrientationSession) -> None:
    if not hasattr(request, "session"):
        return
    ids = [i for i in _browser_ids(request) if i != str(session.id)]
    ids.append(str(session.id))
    request.session[constants.BROWSER_SESSION_KEY] = ids[-constants.MAX_SESSIONS_PER_BROWSER :]
    request.session.modified = True


def forget_in_browser(request, session: OrientationSession) -> None:
    if not hasattr(request, "session"):
        return
    ids = [i for i in _browser_ids(request) if i != str(session.id)]
    request.session[constants.BROWSER_SESSION_KEY] = ids
    request.session.modified = True


# ------------------------------------------------------------------------------------------------
# Session lifecycle
# ------------------------------------------------------------------------------------------------
def start_session(request, ruleset: Ruleset | None = None) -> OrientationSession:
    ruleset = ruleset or active_ruleset()
    if ruleset is None:
        raise NoActiveRuleset
    user = getattr(request, "user", None)
    user = user if getattr(user, "is_authenticated", False) else None
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    session = OrientationSession(
        ruleset=ruleset,
        user=user,
        language=lang,
        ip_hash=hashed_client_ip(request),
        state={"answers": {}, "history": []},
    )
    session.touch_expiry()
    session.current_question = ruleset.entry_question()
    session.save()
    remember_in_browser(request, session)
    audit_record(
        request, action="orientation.session.started", target=session, metadata={"ruleset_version": ruleset.version}
    )
    return session


def can_access(request, session: OrientationSession, token: str | None = None) -> bool:
    if session.is_expired():
        return False
    if str(session.id) in _browser_ids(request):
        return True
    user = getattr(request, "user", None)
    if session.user_id and getattr(user, "is_authenticated", False) and session.user_id == user.id:
        return True
    if token and session.resume_token_hash:
        return secrets.compare_digest(session.resume_token_hash, _hash_token(normalise_token(token)))
    return False


def get_session_or_404(request, session_id, token: str | None = None) -> OrientationSession:
    """404 (not 403) for anything the caller may not open, so session ids cannot be probed."""
    try:
        session = OrientationSession.objects.select_related("ruleset", "user").get(pk=session_id)
    except (OrientationSession.DoesNotExist, ValueError, ValidationError) as exc:
        raise Http404 from exc
    if not can_access(request, session, token):
        raise Http404
    return session


def resume_by_token(request, raw_token: str) -> OrientationSession | None:
    token = normalise_token(raw_token)
    if len(token) != constants.RESUME_TOKEN_LENGTH:
        return None
    session = OrientationSession.objects.select_related("ruleset").filter(resume_token_hash=_hash_token(token)).first()
    if session is None or session.is_expired():
        return None
    remember_in_browser(request, session)
    audit_record(request, action="orientation.session.resumed", target=session)
    return session


@dataclass(frozen=True)
class Step:
    """What the wizard must show now."""

    question: engine.QuestionSpec | None
    result: engine.Result | None
    step_number: int
    progress: int
    can_go_back: bool
    max_steps: int = 1


def current_step(session: OrientationSession, spec: engine.RulesetSpec | None = None) -> Step:
    spec = spec or spec_for(session.ruleset)
    answers = session.answers
    outcome = engine.evaluate(spec, answers)
    answered = len(session.history)
    if isinstance(outcome, engine.Result):
        return Step(None, outcome, answered + 1, 100, answered > 0, spec.max_depth)
    return Step(
        outcome.question, None, answered + 1, engine.progress_percent(spec, answered), answered > 0, spec.max_depth
    )


def submit_answer(request, session: OrientationSession, question_key: str, raw_value: Any) -> Step:
    """Record an answer for the question currently asked; returns the next step (question/result)."""
    if session.is_completed:
        return current_step(session)
    spec = spec_for(session.ruleset)
    step = engine.evaluate(spec, session.answers)
    if isinstance(step, engine.Result):
        return complete_session(request, session, step)
    question = step.question
    if question.key != question_key:
        raise engine.InvalidAnswer("stale")
    value = engine.normalise_answer(question, raw_value)
    state = session.state or {"answers": {}, "history": []}
    state.setdefault("answers", {})[question.key] = value
    state.setdefault("history", []).append(question.key)
    session.state = state
    nxt = engine.evaluate(spec, state["answers"])
    if isinstance(nxt, engine.Result):
        return complete_session(request, session, nxt)
    session.current_question = Question.objects.filter(ruleset=session.ruleset, key=nxt.question.key).first()
    session.touch_expiry()
    session.save(update_fields=["state", "current_question", "expires_at", "updated_at"])
    return current_step(session, spec)


def go_back(session: OrientationSession) -> Step:
    if session.is_completed:
        return current_step(session)
    state = session.state or {"answers": {}, "history": []}
    history = state.get("history") or []
    if history:
        last = history.pop()
        state.get("answers", {}).pop(last, None)
        session.state = state
        session.current_question = Question.objects.filter(ruleset=session.ruleset, key=last).first()
        session.touch_expiry()
        session.save(update_fields=["state", "current_question", "expires_at", "updated_at"])
    return current_step(session)


@transaction.atomic
def complete_session(request, session: OrientationSession, result: engine.Result) -> Step:
    outcome = Outcome.objects.get(ruleset=session.ruleset, key=result.outcome.key)
    text = outcome.explanation_fr
    if result.rule is not None and result.rule.explanation_fr:
        text = f"{text}\n\n{result.rule.explanation_fr}"
    OrientationResult.objects.update_or_create(
        session=session,
        defaults={
            "outcome": outcome,
            "ruleset_version": session.ruleset.version,
            "answers_snapshot": session.answers,
            "disclaimer_version": constants.DISCLAIMER_VERSION,
            "disclaimer_key": outcome.disclaimer_locked_key,
            "result_text_fr": text,
        },
    )
    token = new_resume_token()
    session.resume_token_hash = _hash_token(token)
    session.status = SessionStatus.COMPLETED
    session.current_question = None
    session.touch_expiry()
    session.save(update_fields=["state", "status", "current_question", "resume_token_hash", "expires_at", "updated_at"])
    if request is not None and hasattr(request, "session"):
        request.session[constants.REVEAL_TOKEN_KEY] = {"session": str(session.id), "token": token}
        request.session.modified = True
    audit_record(
        request,
        action="orientation.session.completed",
        target=session,
        metadata={
            "ruleset_version": session.ruleset.version,
            "outcome": outcome.key,
            "pathway_key": outcome.pathway_key,
            "disclaimer_version": constants.DISCLAIMER_VERSION,
            "fallback": result.fallback,
        },
    )
    # The questionnaire becomes a file. Without this step the platform asks a person ten questions
    # about their life, shows them an answer, and forgets (Technical Blueprint §5, REQ-PER-07).
    # An anonymous session opens nothing: the case appears when the visitor has an account.
    _open_case_file(session, request)
    return current_step(session)


def _open_case_file(session: OrientationSession, request) -> None:
    """
    Open or update the case file this session produces.

    Deliberately defensive: a failure here must not lose the result the person just earned. The
    session and its result are already saved when this runs, so a case that could not be opened is
    an incident to investigate, not an answer to throw away — the dashboard reads the session as a
    fallback in the meantime.
    """
    if session.user_id is None:
        return
    try:
        from cases.intake import open_case_from_session

        open_case_from_session(session, request=request)
    except Exception:  # noqa: BLE001 - never lose a completed assessment over a downstream failure
        log.exception("case file not opened for a completed orientation session", extra={"session": str(session.id)})


def pop_reveal_token(request, session: OrientationSession) -> str | None:
    """Return the resume token exactly once (right after completion), then forget it."""
    try:
        data = request.session.get(constants.REVEAL_TOKEN_KEY)
    except AttributeError:
        return None
    if not data or data.get("session") != str(session.id):
        return None
    del request.session[constants.REVEAL_TOKEN_KEY]
    request.session.modified = True
    return data.get("token")


def abandon_session(request, session: OrientationSession) -> None:
    if session.status == SessionStatus.IN_PROGRESS:
        session.status = SessionStatus.ABANDONED
        session.save(update_fields=["status", "updated_at"])
    forget_in_browser(request, session)


def restart(request, session: OrientationSession) -> OrientationSession:
    abandon_session(request, session)
    return start_session(request)


@transaction.atomic
def attach_to_user(request, session: OrientationSession, user) -> OrientationSession:
    """Save an anonymous session into the person's account (gated G2 in the view)."""
    session.user = user
    session.touch_expiry()
    session.save(update_fields=["user", "expires_at", "updated_at"])
    audit_record(request, action="orientation.session.saved", target=session)
    return session


def sessions_for_user(user) -> QuerySet[OrientationSession]:
    """Portal hook: the person's sessions, most recent first (results prefetched)."""
    if not getattr(user, "is_authenticated", False):
        return OrientationSession.objects.none()
    return (
        OrientationSession.objects.filter(user=user)
        .select_related("ruleset", "result", "result__outcome")
        .order_by("-updated_at")
    )


# ------------------------------------------------------------------------------------------------
# GDPR: anonymisation, deletion, retention purge
# ------------------------------------------------------------------------------------------------
@transaction.atomic
def anonymise_session(session: OrientationSession, request=None) -> OrientationSession:
    """Strip every identifier and the answers; keep only statistics (outcome, version, dates)."""
    session.user = None
    session.ip_hash = ""
    session.resume_token_hash = ""
    session.state = {"answers": {}, "history": []}
    session.current_question = None
    session.expires_at = None
    if session.status == SessionStatus.IN_PROGRESS:
        session.status = SessionStatus.ABANDONED
    session.save()
    OrientationResult.objects.filter(session=session).update(answers_snapshot={}, result_text_fr="")
    audit_record(request, action="orientation.session.anonymised", target=session)
    return session


def delete_session(session: OrientationSession, request=None) -> None:
    ref = session.reference
    audit_record(request, action="orientation.session.deleted", metadata={"reference": ref})
    session.delete()


def anonymise_user_sessions(user, request=None) -> int:
    count = 0
    for session in OrientationSession.objects.filter(user=user):
        anonymise_session(session, request)
        count += 1
    return count


@dataclass
class PurgeReport:
    deleted: int = 0
    anonymised: int = 0
    dry_run: bool = False


def purge_expired_sessions(
    days: int | None = None, dry_run: bool = False, at: dt.datetime | None = None
) -> PurgeReport:
    """
    Retention: anonymous sessions older than ``days`` (default 30) are removed. Completed ones are
    anonymised (statistics kept, no answers, no token); in-progress/abandoned ones are deleted.
    """
    at = at or clock.now()
    days = constants.ANONYMOUS_SESSION_TTL_DAYS if days is None else days
    cutoff = at - dt.timedelta(days=days)
    report = PurgeReport(dry_run=dry_run)
    expired = OrientationSession.objects.filter(user__isnull=True, updated_at__lt=cutoff)
    to_delete = expired.exclude(status=SessionStatus.COMPLETED)
    to_anonymise = expired.filter(status=SessionStatus.COMPLETED).exclude(state={"answers": {}, "history": []})
    report.deleted = to_delete.count()
    report.anonymised = to_anonymise.count()
    if dry_run:
        return report
    for session in to_anonymise:
        anonymise_session(session)
    to_delete.delete()
    log.info("orientation purge: deleted=%s anonymised=%s", report.deleted, report.anonymised)
    return report


# ------------------------------------------------------------------------------------------------
# Presentation helpers (translations resolved here so templates stay logic-free)
# ------------------------------------------------------------------------------------------------
def _lang() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def present_question(ruleset: Ruleset, question: engine.QuestionSpec, lang: str | None = None) -> dict[str, Any]:
    """Localised presentation of a question and its choices (published translations, FR fallback)."""
    lang = lang or _lang()
    obj = (
        Question.objects.filter(ruleset=ruleset, key=question.key)
        .prefetch_related("translations", "choices", "choices__translations")
        .first()
    )
    text, help_text, text_lang = question.text_fr, question.help_fr, "fr"
    choices: list[dict[str, Any]] = []
    if obj is not None:
        row, effective, _fb = resolve(obj, lang)
        if row is not None:
            text, help_text, text_lang = row.text, row.help, effective
        for choice in obj.choices.all():
            crow, ceff, _cfb = resolve(choice, lang)
            choices.append(
                {
                    "key": choice.key,
                    "label": crow.label if crow is not None else choice.label_fr,
                    "lang": ceff if crow is not None else "fr",
                }
            )
    else:
        choices = [{"key": c.key, "label": c.label_fr, "lang": "fr"} for c in question.choices]
    if question.type == "boolean":
        choices = [
            {"key": engine.BOOLEAN_TRUE, "label": _("Oui"), "lang": lang},
            {"key": engine.BOOLEAN_FALSE, "label": _("Non"), "lang": lang},
        ]
    return {
        "key": question.key,
        "type": question.type,
        "text": text,
        "help": help_text,
        "lang": text_lang,
        "fallback": text_lang != lang,
        "choices": choices,
        "input_type": "checkbox" if question.type == "multiple" else "radio",
    }


def present_result(result: OrientationResult, lang: str | None = None) -> dict[str, Any]:
    lang = lang or _lang()
    outcome = result.outcome
    row, effective, _fb = resolve(outcome, lang)
    title = row.title if row is not None else outcome.title_fr
    explanation = row.explanation if row is not None else result.result_text_fr or outcome.explanation_fr
    groups: list[dict[str, Any]] = []
    items = (
        ChecklistItem.objects.filter(outcome=outcome)
        .prefetch_related("translations")
        .order_by("category", "order", "id")
    )
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        irow, ieff, _ifb = resolve(item, lang)
        by_cat.setdefault(item.category, []).append(
            {"text": irow.text if irow is not None else item.text_fr, "lang": ieff if irow is not None else "fr"}
        )
    for value, label in ChecklistCategory.choices:
        if value in by_cat:
            groups.append({"key": value, "label": label, "items": by_cat[value]})
    answers = result.answers_snapshot or {}
    return {
        "title": title,
        "explanation_paragraphs": [p for p in explanation.split("\n\n") if p.strip()],
        "lang": effective if row is not None else "fr",
        "pathway_key": outcome.pathway_key,
        "is_individual_analysis": outcome.pathway_key == constants.NEEDS_INDIVIDUAL_ANALYSIS,
        "disclaimer_locked_key": outcome.disclaimer_locked_key,
        "checklist_groups": groups,
        "training_interest": answers.get("training_interest") is True,
        "kind": result.kind,
    }


# ------------------------------------------------------------------------------------------------
# Back-office statistics (anonymised — never the answers)
# ------------------------------------------------------------------------------------------------
def statistics_rows(queryset: QuerySet[OrientationResult]) -> list[dict[str, Any]]:
    rows = (
        queryset.values(
            "ruleset_version", "outcome__key", "outcome__pathway_key", "session__language", "disclaimer_version"
        )
        .annotate(total=Count("id"))
        .order_by("ruleset_version", "outcome__key", "session__language")
    )
    return [
        {
            "ruleset_version": r["ruleset_version"],
            "outcome": r["outcome__key"],
            "pathway_key": r["outcome__pathway_key"],
            "language": r["session__language"],
            "disclaimer_version": r["disclaimer_version"],
            "total": r["total"],
        }
        for r in rows
    ]


def statistics_csv(queryset: QuerySet[OrientationResult]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=";")
    writer.writerow(["ruleset_version", "outcome", "pathway_key", "language", "disclaimer_version", "total"])
    for r in statistics_rows(queryset):
        writer.writerow(
            [r["ruleset_version"], r["outcome"], r["pathway_key"], r["language"], r["disclaimer_version"], r["total"]]
        )
    return buf.getvalue()
