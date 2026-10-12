"""
Orientation platform — versioned rule engine + questionnaire sessions.

Content rule: questions, outcomes and checklist items are *team* texts (neutral, situational,
informational). They never assert legal criteria; every legal aspect is CONTENT_PENDING_LEGAL_REVIEW
and the result is always a « pré-évaluation à caractère informatif » (Annexe 1 §1.4, §4 art. 2).
"""

from __future__ import annotations

import datetime as dt
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import TranslationBase
from core import clock
from core.models import TimeStampedModel
from orientation import constants
from orientation.constants import OUTCOME_PATHWAY_KEYS

PENDING_LEGAL_REVIEW_HELP = _(
    "CONTENT_PENDING_LEGAL_REVIEW — texte d'équipe à caractère informatif : aucune condition légale, "
    "aucune promesse de résultat. Toute mention juridique doit être validée par la revue légale avant publication."
)


class RulesetStatus(models.TextChoices):
    DRAFT = "draft", _("Bozza")
    ACTIVE = "active", _("Attivo")
    RETIRED = "retired", _("Ritirato")


class Ruleset(TimeStampedModel):
    """A complete, versioned set of questions, rules and outcomes. Exactly one is active."""

    version = models.PositiveIntegerField(_("versione"), unique=True)
    status = models.CharField(
        _("stato"), max_length=10, choices=RulesetStatus.choices, default=RulesetStatus.DRAFT, db_index=True
    )
    notes = models.TextField(_("note"), blank=True, help_text=_("Origine, revisione, motivo della versione."))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("creato da"),
    )
    activated_at = models.DateTimeField(_("attivato il"), null=True, blank=True)

    class Meta:
        ordering = ["-version"]
        verbose_name = _("ruleset di orientamento")
        verbose_name_plural = _("ruleset di orientamento")
        constraints = [
            models.UniqueConstraint(
                fields=["status"], condition=models.Q(status="active"), name="uniq_active_orientation_ruleset"
            ),
        ]

    def __str__(self) -> str:
        return f"Ruleset v{self.version} ({self.get_status_display()})"

    @property
    def is_active(self) -> bool:
        return self.status == RulesetStatus.ACTIVE

    def entry_question(self) -> Question | None:
        return self.questions.filter(is_entry=True).first()

    def clean(self) -> None:
        if self.status == RulesetStatus.ACTIVE:
            clash = Ruleset.objects.filter(status=RulesetStatus.ACTIVE).exclude(pk=self.pk)
            if clash.exists():
                raise ValidationError(
                    {"status": _("Un solo ruleset può essere attivo: usare l'azione « Attiva » per sostituirlo.")}
                )


class QuestionType(models.TextChoices):
    SINGLE = "single", _("Scelta singola")
    MULTIPLE = "multiple", _("Scelta multipla")
    BOOLEAN = "boolean", _("Sì / No")


class Question(TimeStampedModel):
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE, related_name="questions")
    key = models.SlugField(_("chiave"), max_length=64)
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    text_fr = models.CharField("Question (FR)", max_length=300)
    help_fr = models.TextField("Aide / explication (FR)", blank=True)
    type = models.CharField(_("tipo"), max_length=10, choices=QuestionType.choices, default=QuestionType.SINGLE)
    is_entry = models.BooleanField(_("domanda iniziale"), default=False)

    class Meta:
        ordering = ["ruleset", "order", "id"]
        verbose_name = _("domanda")
        verbose_name_plural = _("domande")
        constraints = [
            models.UniqueConstraint(fields=["ruleset", "key"], name="uniq_orientation_question_key"),
            models.UniqueConstraint(
                fields=["ruleset"], condition=models.Q(is_entry=True), name="uniq_orientation_entry_question"
            ),
        ]

    def __str__(self) -> str:
        return f"[v{self.ruleset.version}] {self.key}"

    def clean(self) -> None:
        if self.is_entry and self.ruleset_id:
            clash = Question.objects.filter(ruleset_id=self.ruleset_id, is_entry=True).exclude(pk=self.pk)
            if clash.exists():
                raise ValidationError({"is_entry": _("Esiste già una domanda iniziale in questo ruleset.")})


class QuestionTranslation(TranslationBase):
    master = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="translations")
    text = models.CharField(_("domanda"), max_length=300)
    help = models.TextField(_("aiuto / spiegazione"), blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_orientation_question_translation")
        ]
        verbose_name = _("traduzione domanda")
        verbose_name_plural = _("traduzioni domande")

    def __str__(self) -> str:
        return f"{self.master.key} [{self.language}]"


class Choice(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    key = models.SlugField(_("chiave"), max_length=64)
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    label_fr = models.CharField("Libellé (FR)", max_length=200)

    class Meta:
        ordering = ["question", "order", "id"]
        verbose_name = _("scelta")
        verbose_name_plural = _("scelte")
        constraints = [models.UniqueConstraint(fields=["question", "key"], name="uniq_orientation_choice_key")]

    def __str__(self) -> str:
        return f"{self.question.key}:{self.key}"


class ChoiceTranslation(TranslationBase):
    master = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="translations")
    label = models.CharField(_("etichetta"), max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_orientation_choice_translation")
        ]
        verbose_name = _("traduzione scelta")
        verbose_name_plural = _("traduzioni scelte")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"


class Outcome(TimeStampedModel):
    """Family of regular pathways the answers point to — informational orientation, never a decision."""

    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE, related_name="outcomes")
    key = models.SlugField(_("chiave"), max_length=64)
    pathway_key = models.CharField(
        _("percorso"),
        max_length=64,
        choices=[(k, k) for k in OUTCOME_PATHWAY_KEYS],
        help_text=_("Una delle 8 chiavi bloccate dell'Espace Personnes oppure « needs_individual_analysis »."),
    )
    title_fr = models.CharField("Titre (FR)", max_length=200)
    explanation_fr = models.TextField("Explication (FR)", help_text=PENDING_LEGAL_REVIEW_HELP)
    disclaimer_key = models.CharField(
        _("chiave disclaimer"),
        max_length=64,
        default=constants.DISCLAIMER_KEY,
        help_text=_("Identificatore logico; il testo è reso dal registro bloccato (p3.persons.how_it_works)."),
    )

    class Meta:
        ordering = ["ruleset", "id"]
        verbose_name = _("risultato di orientamento")
        verbose_name_plural = _("risultati di orientamento (catalogo)")
        constraints = [models.UniqueConstraint(fields=["ruleset", "key"], name="uniq_orientation_outcome_key")]

    def __str__(self) -> str:
        return f"[v{self.ruleset.version}] {self.key} → {self.pathway_key}"

    @property
    def disclaimer_locked_key(self) -> str:
        return constants.DISCLAIMER_LOCKED_KEYS.get(
            self.disclaimer_key, constants.DISCLAIMER_LOCKED_KEYS[constants.DISCLAIMER_KEY]
        )

    def clean(self) -> None:
        if self.disclaimer_key not in constants.DISCLAIMER_LOCKED_KEYS:
            raise ValidationError({"disclaimer_key": _("Chiave disclaimer sconosciuta.")})


class OutcomeTranslation(TranslationBase):
    master = models.ForeignKey(Outcome, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField(_("titolo"), max_length=200)
    explanation = models.TextField(_("spiegazione"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_orientation_outcome_translation")
        ]
        verbose_name = _("traduzione risultato")
        verbose_name_plural = _("traduzioni risultati")

    def __str__(self) -> str:
        return f"{self.master.key} [{self.language}]"


class ChecklistCategory(models.TextChoices):
    DOCUMENTS = "documents", _("Documentation")
    STEPS = "steps", _("Étapes")
    AUTHORITIES = "authorities", _("Acteurs et autorités compétents")
    WARNINGS = "warnings", _("Points d’attention")


class ChecklistItem(TimeStampedModel):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE, related_name="checklist_items")
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    category = models.CharField(
        _("categoria"), max_length=12, choices=ChecklistCategory.choices, default=ChecklistCategory.STEPS
    )
    text_fr = models.CharField("Texte (FR)", max_length=300, help_text=PENDING_LEGAL_REVIEW_HELP)

    class Meta:
        ordering = ["outcome", "category", "order", "id"]
        verbose_name = _("voce di checklist")
        verbose_name_plural = _("voci di checklist")

    def __str__(self) -> str:
        return f"{self.outcome.key} / {self.category} #{self.order}"


class ChecklistItemTranslation(TranslationBase):
    master = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE, related_name="translations")
    text = models.CharField(_("testo"), max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["master", "language"], name="uniq_orientation_checklist_translation")
        ]
        verbose_name = _("traduzione voce di checklist")
        verbose_name_plural = _("traduzioni voci di checklist")

    def __str__(self) -> str:
        return f"{self.master} [{self.language}]"


class Rule(TimeStampedModel):
    """
    Ordered transition: when ``conditions`` match the answers, ask ``next_question`` (if not yet
    answered) or terminate with ``outcome``. Conditions use the declarative DSL of ``engine.py``.
    """

    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE, related_name="rules")
    order = models.PositiveSmallIntegerField(_("ordine"), default=0)
    name = models.CharField(_("nome"), max_length=120)
    conditions = models.JSONField(
        _("condizioni"),
        default=dict,
        blank=True,
        help_text=_(
            'JSON : {} (sempre) · {"all": [...]} · {"any": [...]} · '
            '{"question_key": "objective", "op": "eq|in|not_in|is_true|is_false", "value": "work"}'
        ),
    )
    next_question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, blank=True, related_name="incoming_rules"
    )
    outcome = models.ForeignKey(Outcome, on_delete=models.SET_NULL, null=True, blank=True, related_name="rules")
    explanation_fr = models.TextField(
        "Explication complémentaire (FR)", blank=True, help_text=PENDING_LEGAL_REVIEW_HELP
    )

    class Meta:
        ordering = ["ruleset", "order", "id"]
        verbose_name = _("regola")
        verbose_name_plural = _("regole")
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(next_question__isnull=False, outcome__isnull=True)
                    | models.Q(next_question__isnull=True, outcome__isnull=False)
                ),
                name="orientation_rule_exactly_one_target",
            )
        ]

    def __str__(self) -> str:
        return f"[v{self.ruleset.version}] #{self.order} {self.name}"

    @property
    def target_label(self) -> str:
        if self.next_question_id:
            return f"→ {self.next_question.key}"
        if self.outcome_id:
            return f"⇒ {self.outcome.key}"
        return "—"

    def clean(self) -> None:
        from orientation import engine

        errors: dict[str, list[str]] = {}
        if (self.next_question_id is None) == (self.outcome_id is None):
            errors["next_question"] = [
                str(_("Indicare esattamente una destinazione: domanda successiva oppure risultato."))
            ]
        if self.next_question_id and self.ruleset_id and self.next_question.ruleset_id != self.ruleset_id:
            errors.setdefault("next_question", []).append(str(_("La domanda appartiene a un altro ruleset.")))
        if self.outcome_id and self.ruleset_id and self.outcome.ruleset_id != self.ruleset_id:
            errors.setdefault("outcome", []).append(str(_("Il risultato appartiene a un altro ruleset.")))
        spec = None
        if self.ruleset_id:
            from orientation.services import spec_for

            spec = spec_for(self.ruleset)
        problems = engine.validate_conditions(self.conditions, spec)
        if problems:
            errors["conditions"] = problems
        if errors:
            raise ValidationError(errors)


class SessionStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", _("In corso")
    COMPLETED = "completed", _("Completata")
    ABANDONED = "abandoned", _("Abbandonata")


def _empty_state() -> dict:
    return {"answers": {}, "history": []}


class OrientationSession(TimeStampedModel):
    """
    One questionnaire run. Anonymous sessions hold no personal data (answers are choice keys) and
    expire after 30 days; sessions of authenticated users are attached to the account.
    Access: creating browser (Django session), owning user, or hashed resume token.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ruleset = models.ForeignKey(Ruleset, on_delete=models.PROTECT, related_name="sessions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orientation_sessions",
    )
    resume_token_hash = models.CharField(max_length=64, blank=True, db_index=True, editable=False)
    state = models.JSONField(default=_empty_state, blank=True, editable=False)
    current_question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", editable=False
    )
    status = models.CharField(
        max_length=12, choices=SessionStatus.choices, default=SessionStatus.IN_PROGRESS, db_index=True
    )
    language = models.CharField(max_length=5, default="fr")
    ip_hash = models.CharField(max_length=32, blank=True, editable=False)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("sessione di orientamento")
        verbose_name_plural = _("sessioni di orientamento")

    def __str__(self) -> str:
        return f"Session {str(self.id)[:8]} (v{self.ruleset.version}, {self.status})"

    @property
    def answers(self) -> dict:
        return dict((self.state or {}).get("answers") or {})

    @property
    def history(self) -> list[str]:
        return list((self.state or {}).get("history") or [])

    @property
    def reference(self) -> str:
        return str(self.id)[:8].upper()

    @property
    def is_completed(self) -> bool:
        return self.status == SessionStatus.COMPLETED

    def is_expired(self, at: dt.datetime | None = None) -> bool:
        if self.user_id:
            return False
        if not self.expires_at:
            return False
        return (at or clock.now()) >= self.expires_at

    def touch_expiry(self) -> None:
        if self.user_id:
            self.expires_at = None
        else:
            self.expires_at = clock.now() + dt.timedelta(days=constants.ANONYMOUS_SESSION_TTL_DAYS)


class OrientationResult(models.Model):
    """
    Frozen result of a completed session: outcome, ruleset version, answer snapshot and the version
    of the disclaimer the person saw. Always an informational pre-assessment (never a decision).
    """

    KIND = "INFORMATIVE_PREASSESSMENT"

    session = models.OneToOneField(OrientationSession, on_delete=models.CASCADE, related_name="result")
    outcome = models.ForeignKey(Outcome, on_delete=models.PROTECT, related_name="results")
    ruleset_version = models.PositiveIntegerField()
    answers_snapshot = models.JSONField(default=dict, blank=True)
    disclaimer_version = models.CharField(max_length=20, default=constants.DISCLAIMER_VERSION)
    disclaimer_key = models.CharField(max_length=64, default="p3.persons.how_it_works")
    result_text_fr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("risultato di orientamento")
        verbose_name_plural = _("risultati di orientamento")

    def __str__(self) -> str:
        return f"Result {self.session.reference} → {self.outcome.pathway_key} (v{self.ruleset_version})"

    @property
    def kind(self) -> str:
        return self.KIND
