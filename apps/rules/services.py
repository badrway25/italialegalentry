"""
Services of the legal rule engine: the four-eyes workflow, and the evaluation.

Every state change goes through here, so the constraint that an author cannot approve their own rule
holds whichever entry point is used — a view, the admin, a management command or a future API.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from audit.services import record
from rules.engine import evaluate_condition
from rules.models import (
    ALLOWED_REVIEW_TRANSITIONS,
    LEGACY_PROVENANCES,
    LegalRule,
    ReviewStatus,
    RuleEffect,
)

#: Effect → how strongly it speaks. The strongest effect present decides the assessment's outcome:
#: a STOP anywhere means the pathway is not presented as practicable, whatever else matched.
EFFECT_RANK: dict[str, int] = {
    RuleEffect.POSSIBLE: 0,
    RuleEffect.WARNING: 1,
    RuleEffect.MISSING_REQUIREMENT: 2,
    RuleEffect.REVIEW_REQUIRED: 3,
    RuleEffect.STOP: 4,
}


def displayed(key: str, source_text: str) -> str:
    """
    The rule's text in the reader's language, or its French source.

    ``LegalRule.message_key`` exists so that what a person reads lives in the translation system
    rather than in the rule row — and nothing was reading it, so every rule message rendered in
    French whatever language the page was in.

    gettext returns the KEY when there is no entry for it, which would put ``rules.work.offer`` on
    somebody's screen: worse than French. So a translation is used only when it actually differs
    from the key, and the French source is used otherwise. The field becomes useful the day a
    translator adds the keys, and changes nothing until then.

    Supplying four languages per rule is editorial work for the legal referent, not a code change.
    """
    if not key:
        return source_text
    translated = gettext(key)
    return translated if translated != key else source_text


class TransitionRefused(ValidationError):
    """A review-workflow change the domain does not allow."""


@dataclass(frozen=True)
class Finding:
    """One rule that fired, with everything needed to explain it afterwards."""

    rule_id: str
    version: int
    effect: str
    message: str
    requirement: str
    responsible_actor: str
    sources: list = field(default_factory=list)


@dataclass(frozen=True)
class Evaluation:
    """
    The result of an evaluation, and the evidence for it.

    ``snapshot`` carries the whole ruleset that was applied, so the outcome can be recomputed later
    even after every rule in it has been retired.
    """

    outcome: str
    findings: list[Finding]
    snapshot: dict
    evaluated_on: str
    jurisdiction: str
    pathway: str

    @property
    def is_blocking(self) -> bool:
        return self.outcome == RuleEffect.STOP

    @property
    def missing(self) -> list[Finding]:
        return [f for f in self.findings if f.effect == RuleEffect.MISSING_REQUIREMENT]

    @property
    def sources(self) -> list:
        """Every distinct source behind the findings, in the order they were met."""
        seen, out = set(), []
        for finding in self.findings:
            for source in finding.sources:
                key = (source.get("reference"), source.get("title"))
                if key not in seen:
                    seen.add(key)
                    out.append(source)
        return out


# ---------------------------------------------------------------------------------------------
# The four-eyes workflow
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def _label_for(actor) -> str:
    """
    A readable record of who approved, kept as text.

    The foreign key is SET_NULL and accounts get anonymised under art. 17. A rule in force
    must still name who stands behind it after that, so the label is what the database
    constraint checks.
    """
    if actor is None:
        return ""
    return getattr(actor, "full_name", "") or getattr(actor, "email", "") or str(actor.pk)


def transition(
    rule: LegalRule,
    target: str,
    *,
    actor,
    note: str = "",
    request=None,
    approver_label: str = "",
) -> LegalRule:
    """
    Move a rule through its review workflow, or refuse.

    Two refusals matter more than the others, and both are here rather than in a form:
    an author cannot approve their own rule, and a rule cannot be activated without a source.
    """
    if target not in ReviewStatus.values:
        raise TransitionRefused(_("Stato non riconosciuto."))
    if target == rule.review_status:
        return rule
    if target not in ALLOWED_REVIEW_TRANSITIONS.get(rule.review_status, frozenset()):
        raise TransitionRefused(
            _("Transizione non consentita da «%(from)s» a «%(to)s».")
            % {"from": rule.get_review_status_display(), "to": dict(ReviewStatus.choices)[target]}
        )

    if target == ReviewStatus.APPROVED:
        if actor is None:
            raise TransitionRefused(_("L'approvazione richiede un revisore identificato."))
        if rule.created_by_id is not None and actor.pk == rule.created_by_id:
            # Four eyes, Technical Blueprint §4. An author approving their own legal rule is not a
            # review: it is the same judgement recorded twice.
            raise PermissionDenied(_("L'autore di una regola non può approvarla."))

    if target == ReviewStatus.SOURCE_VERIFIED:
        # The step this state names was being skipped. Every seeded source carried a precise
        # reference and not one carried a consultation date, a URL or a name — and a jurist was
        # being handed those references as if somebody had opened them.
        if not rule.sources.exists():
            raise TransitionRefused(_("Non si verifica la fonte di una regola che non ne ha nessuna."))
        unverified = rule.unverified_sources
        if unverified:
            raise TransitionRefused(
                _(
                    "Fonti ancora da verificare alla fonte ufficiale: %(list)s. "
                    "Servono data, nome di chi ha verificato, e URL o autorità."
                )
                % {"list": ", ".join(source.reference for source in unverified)}
            )

    if target == ReviewStatus.ACTIVE:
        # A rule in force with no source produces an outcome nobody can check, which is the defect
        # the previous platform had across its entire document catalogue.
        if not rule.sources.exists():
            raise TransitionRefused(_("Una regola non entra in vigore senza almeno una fonte."))
        if not rule.approved_by_label.strip():
            raise TransitionRefused(_("Una regola non entra in vigore senza un approvatore registrato."))

    previous = rule.review_status
    rule.review_status = target
    if target == ReviewStatus.APPROVED:
        rule.approved_by = actor
        rule.approved_by_label = approver_label or _label_for(actor)
        rule.approved_at = timezone.now()
    elif target in {ReviewStatus.DRAFT, ReviewStatus.LEGACY_CANDIDATE}:
        # Sending a rule back withdraws the approval with it. Leaving the label behind would let a
        # later activation inherit an approval of a text that has since changed.
        rule.approved_by = None
        rule.approved_by_label = ""
        rule.approved_at = None
    elif target == ReviewStatus.RETIRED:
        rule.retired_at = timezone.now()
    if note:
        rule.note = note
    rule.save(
        update_fields=[
            "review_status",
            "approved_by",
            "approved_by_label",
            "approved_at",
            "retired_at",
            "note",
            "updated_at",
        ]
    )

    record(
        request,
        actor=actor,
        action="rule.transition",
        target=rule,
        metadata={
            "rule_id": rule.rule_id,
            "version": rule.version,
            "from": previous,
            "to": target,
            "provenance": rule.provenance,
        },
    )
    return rule


@transaction.atomic
def new_version(rule: LegalRule, *, actor, request=None, **changes) -> LegalRule:
    """
    Open a new pre-approval version of a rule, leaving the one in force untouched.

    A rule in force is never edited in place: assessments already given depend on it reading the way
    it read when they were given.

    The new version starts where its PROVENANCE says it should: inherited content returns to
    ``LEGACY_CANDIDATE``, content drafted from a norm to ``DRAFT``. Either way it must walk the
    chain again, because a new version is new text and the old approval was of the old text.
    """
    latest = LegalRule.objects.filter(rule_id=rule.rule_id).order_by("-version").first()
    draft = LegalRule(
        rule_id=rule.rule_id,
        version=(latest.version if latest else rule.version) + 1,
        jurisdiction=rule.jurisdiction,
        pathway=rule.pathway,
        condition=rule.condition,
        effect=rule.effect,
        message_key=rule.message_key,
        message_fr=rule.message_fr,
        requirement_fr=rule.requirement_fr,
        responsible_actor=rule.responsible_actor,
        valid_from=rule.valid_from,
        valid_to=rule.valid_to,
        # Provenance travels with the CONTENT, so it travels with a new version. Without this line
        # a second version of an inherited rule silently became `drafted_from_source`, which is
        # provenance laundering: the field exists precisely to stop the previous platform's
        # authority from being acquired by editing.
        provenance=rule.provenance,
        review_status=(
            ReviewStatus.LEGACY_CANDIDATE
            if rule.provenance in LEGACY_PROVENANCES
            else ReviewStatus.DRAFT
        ),
        created_by=actor,
    )
    for name, value in changes.items():
        setattr(draft, name, value)
    draft.full_clean(exclude=["created_by", "approved_by"])
    draft.save()
    draft.sources.set(rule.sources.all())
    record(
        request,
        actor=actor,
        action="rule.new_version",
        target=draft,
        metadata={"rule_id": draft.rule_id, "version": draft.version, "from_version": rule.version},
    )
    return draft


# ---------------------------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------------------------
def rules_in_force(jurisdiction: str, pathway: str, on_date=None):
    return (
        LegalRule.objects.in_force(on_date).for_pathway(jurisdiction, pathway).prefetch_related("sources")
    ).order_by("rule_id", "-version")


def evaluate(facts: dict, *, jurisdiction: str = "IT", pathway: str = "", on_date=None, lang: str = "fr") -> Evaluation:
    """
    Apply every rule in force on ``on_date`` and return the outcome with its evidence.

    ``on_date`` is the ASSESSMENT's date, not today. Re-running an old assessment must select the
    rules that were in force when it was given, or the replay proves nothing.
    """
    on_date = on_date or timezone.localdate()
    applicable = list(rules_in_force(jurisdiction, pathway, on_date))

    # One version per rule_id: the highest in force. Two versions of the same rule firing together
    # would double-count a single legal requirement.
    by_id: dict[str, LegalRule] = {}
    for rule in applicable:
        by_id.setdefault(rule.rule_id, rule)

    findings: list[Finding] = []
    for rule in by_id.values():
        if not evaluate_condition(rule.condition or {}, facts):
            continue
        findings.append(
            Finding(
                rule_id=rule.rule_id,
                version=rule.version,
                effect=rule.effect,
                message=displayed(rule.message_key, rule.message_fr),
                requirement=displayed(f"{rule.message_key}.requirement", rule.requirement_fr),
                responsible_actor=rule.responsible_actor,
                sources=[source.as_citation(lang) for source in rule.sources.all()],
            )
        )

    outcome = RuleEffect.POSSIBLE
    for finding in findings:
        if EFFECT_RANK[finding.effect] > EFFECT_RANK[outcome]:
            outcome = finding.effect

    return Evaluation(
        outcome=outcome,
        findings=findings,
        snapshot={
            "format": "ile.legal.ruleset/1",
            "evaluated_on": on_date.isoformat(),
            "jurisdiction": jurisdiction,
            "pathway": pathway,
            "rules": [rule.as_snapshot(lang) for rule in by_id.values()],
        },
        evaluated_on=on_date.isoformat(),
        jurisdiction=jurisdiction,
        pathway=pathway,
    )


def replay(snapshot: dict, facts: dict) -> str:
    """
    Recompute an outcome from a frozen snapshot.

    This is what makes "every outcome is reproducible using the ruleset snapshot" a testable claim
    rather than a sentence in a document: the rules are read from the snapshot, not from the
    database, so the replay is unaffected by everything that has changed since.
    """
    outcome = RuleEffect.POSSIBLE
    for rule in snapshot.get("rules", []):
        if not evaluate_condition(rule.get("condition") or {}, facts):
            continue
        effect = rule.get("effect", RuleEffect.POSSIBLE)
        if EFFECT_RANK.get(effect, 0) > EFFECT_RANK[outcome]:
            outcome = effect
    return outcome
