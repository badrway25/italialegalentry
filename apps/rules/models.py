"""
The versioned legal rule engine — rules are DATA, not code.

Technical Blueprint v1.0 §7 and §20 are explicit: «Il Rule Engine deve essere separato dal codice
applicativo. Le regole sono dati amministrabili e versionati. Ogni regola deve poter essere
ricondotta a una fonte, a un periodo di validità e a un responsabile della revisione.»

Three properties follow, and each one is enforced here rather than trusted:

1. **A rule has a source.** An outcome that cannot say where it comes from is an oracle, and the one
   element that turns a questionnaire result into an institutional finding is the numbered source
   list beneath it. The previous platform carried four visa types with excellent document
   requirements and not one citation; six months after a decree changes, nobody would know.

2. **A rule has a validity window.** Entry requirements change by decree. An assessment selects the
   rules that were ACTIVE ON ITS OWN DATE, so an outcome given in October stays explainable in March
   even though the rules have moved.

3. **A rule is approved by someone other than its author.** Four eyes, from §4 of the Blueprint. The
   author cannot approve their own rule, and the constraint lives in the model and the service, not
   in a form that a different entry point could bypass.

Outcomes are the five of the domain. There is deliberately no ``eligible``: a person reads it as
"I am entitled to enter" (CONFLICT_REGISTER CR-11).

Conditions are DATA in a restricted JSON DSL, evaluated by ``rules.engine``. No ``eval``, no
``exec``, no dynamic import, no template rendered over user input.
"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


def _responsible_actor_choices():
    """
    The case file's own list of responsible actors, read lazily.

    A rule says who must act, and the case file is where that answer is used, so the two must agree
    letter for letter — a rule naming an actor the checklist cannot display is a rule whose most
    important field is decorative. Django evaluates a callable ``choices`` at need, which lets the
    rule app depend on this without importing the case app at module level.
    """
    from cases.models import ResponsibleActor

    return ResponsibleActor.choices


class RuleEffect(models.TextChoices):
    """
    What a rule contributes to an assessment. The five of ``cases.AssessmentOutcome``, and no sixth.

    A STOP is the strongest thing this system can say, and it still says it about a PATHWAY, never
    about a person: "this route cannot be presented as practicable", not "you are refused".
    """

    POSSIBLE = "possible", _("Percorso pertinente")
    MISSING_REQUIREMENT = "missing_requirement", _("Requisito mancante")
    WARNING = "warning", _("Avvertenza")
    STOP = "stop", _("Elemento ostativo")
    REVIEW_REQUIRED = "review_required", _("Verifica professionale necessaria")


class RuleProvenance(models.TextChoices):
    """
    Where the rule's CONTENT came from, which is not the same question as who wrote the record.

    The previous platform holds genuinely good domain work: the document lists per visa type are
    precise and were written by somebody who knows the material. They are also undated, unsourced,
    unversioned and approved by whoever held a permission. Importing that content is right;
    importing its authority is not, and the two arrive together unless something separates them.

    This field is that separation. ``LEGACY_*`` content starts at ``LEGACY_CANDIDATE`` and cannot
    reach ``ACTIVE`` without passing through a source verification and a legal review, whatever
    anyone types into the admin.
    """

    DRAFTED_FROM_SOURCE = "drafted_from_source", _("Redatta dalla fonte normativa")
    LEGACY_PLATFORM = "legacy_platform", _("Ripresa dalla piattaforma precedente")
    LEGACY_DERIVED = "legacy_derived", _("Derivata da un contenuto della piattaforma precedente")


#: Content that came from the previous platform, in whole or in part.
LEGACY_PROVENANCES = frozenset({RuleProvenance.LEGACY_PLATFORM, RuleProvenance.LEGACY_DERIVED})

#: Marks an approval that is not an approval. `rules_activate_demonstration` writes it so the
#: engine can be seen working locally without the review having happened.
#:
#: It lives here and not in the command because the READER of a result needs it: a page that shows
#: numbered sources, consultation dates and a reproducible replay looks authoritative whether or
#: not a jurist ever saw it, and the difference has to reach the screen.
DEMONSTRATION_APPROVAL_PREFIX = "DIMOSTRAZIONE"


def is_demonstration_approval(label: str) -> bool:
    """Whether an approver label says, in words, that nobody really approved this."""
    return bool(label) and label.strip().upper().startswith(DEMONSTRATION_APPROVAL_PREFIX)


class ReviewStatus(models.TextChoices):
    """
    LEGACY_CANDIDATE → SOURCE_VERIFIED → LEGAL_REVIEW → APPROVED → ACTIVE → RETIRED.

    A rule drafted from the norm starts at ``DRAFT`` instead of ``LEGACY_CANDIDATE``; from there
    the chain is the same, because a freshly drafted rule needs its source checked just as much as
    an inherited one.

    ``SOURCE_VERIFIED`` was added because the step it names was being skipped. Fifteen sources
    carried a precise reference — «D.Lgs. 286/1998, art. 22» — and not one carried a consultation
    date or a URL. A reference nobody has opened is a claim about the present that quietly becomes
    a claim about the past, and it was reaching a jurist as if it had been checked.
    """

    LEGACY_CANDIDATE = "legacy_candidate", _("Candidata — contenuto ereditato")
    DRAFT = "draft", _("Bozza")
    SOURCE_VERIFIED = "source_verified", _("Fonte verificata")
    LEGAL_REVIEW = "legal_review", _("In revisione giuridica")
    APPROVED = "approved", _("Approvata")
    ACTIVE = "active", _("In vigore")
    RETIRED = "retired", _("Ritirata")


#: States a rule may hold before anybody has approved it. None of them binds anybody.
PRE_APPROVAL_STATUSES = frozenset(
    {
        ReviewStatus.LEGACY_CANDIDATE,
        ReviewStatus.DRAFT,
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
    }
)

#: States that assert somebody stood behind the rule. Both require a named approver.
APPROVED_STATUSES = frozenset({ReviewStatus.APPROVED, ReviewStatus.ACTIVE})


#: Declared transitions. Anything absent is refused by the domain.
ALLOWED_REVIEW_TRANSITIONS: dict[str, frozenset[str]] = {
    # Inherited content may be verified as it stands, or sent back to be rewritten from the norm.
    ReviewStatus.LEGACY_CANDIDATE: frozenset({ReviewStatus.SOURCE_VERIFIED, ReviewStatus.DRAFT}),
    ReviewStatus.DRAFT: frozenset({ReviewStatus.SOURCE_VERIFIED}),
    ReviewStatus.SOURCE_VERIFIED: frozenset({ReviewStatus.LEGAL_REVIEW, ReviewStatus.DRAFT}),
    ReviewStatus.LEGAL_REVIEW: frozenset({ReviewStatus.DRAFT, ReviewStatus.APPROVED}),
    ReviewStatus.APPROVED: frozenset({ReviewStatus.ACTIVE, ReviewStatus.DRAFT}),
    ReviewStatus.ACTIVE: frozenset({ReviewStatus.RETIRED}),
    ReviewStatus.RETIRED: frozenset(set()),
}


class LegalSource(TimeStampedModel):
    """
    A norm, a circular, an official page — what a rule stands on.

    Kept as its own record rather than as free text on the rule, because one source justifies many
    rules and a source that moves must move once. ``consulted_on`` is not decoration: a reference to
    an administrative page without the date it was read is a claim about the present that quietly
    becomes a claim about the past.
    """

    key = models.SlugField(_("chiave"), max_length=80, unique=True)
    title_fr = models.CharField(_("titolo (FR)"), max_length=250)
    title_it = models.CharField(_("titolo (IT)"), max_length=250, blank=True)
    reference = models.CharField(
        _("riferimento"),
        max_length=250,
        help_text=_("Es. «D.lgs. 286/1998, art. 22» — l'estremo preciso, non il solo nome della norma."),
    )
    url = models.URLField(_("URL"), blank=True, help_text=_("Solo se pubblico e stabile."))
    authority = models.CharField(_("autorità o emittente"), max_length=160, blank=True)
    jurisdiction = models.CharField(
        _("giurisdizione"),
        max_length=8,
        default="IT",
        db_index=True,
        help_text=_(
            "Ordinamento da cui la fonte proviene: IT, EU, MA, o BIL per un atto bilaterale. "
            "Sta sulla fonte e non solo sulla regola, perché una regola italiana può poggiare su "
            "una direttiva europea, e chi rilegge deve vedere quale dei due è cambiato."
        ),
    )
    consulted_on = models.DateField(
        _("consultata il"),
        null=True,
        blank=True,
        help_text=_("Data in cui la fonte è stata verificata. Mostrata accanto alla citazione."),
    )
    consulted_by = models.CharField(
        _("verificata da"),
        max_length=160,
        blank=True,
        help_text=_("Chi ha aperto la fonte ufficiale quel giorno. Una data senza un nome non è una verifica."),
    )
    note = models.TextField(_("nota interna"), blank=True)

    @property
    def is_verified(self) -> bool:
        """
        A reference is not a verification.

        All fifteen seeded sources carried a precise `reference` and none carried a date, a URL or
        a name. That is the state this property exists to make visible: it is what stops a rule
        from leaving `SOURCE_VERIFIED`.
        """
        return bool(self.consulted_on and self.consulted_by and (self.url or self.authority))

    class Meta:
        verbose_name = _("fonte giuridica")
        verbose_name_plural = _("fonti giuridiche")
        ordering = ["title_fr"]

    def __str__(self) -> str:
        return f"{self.title_fr} — {self.reference}"

    def title(self, lang: str = "fr") -> str:
        return getattr(self, f"title_{lang}", "") or self.title_fr

    def as_citation(self, lang: str = "fr") -> dict:
        return {
            "title": self.title(lang),
            "reference": self.reference,
            "url": self.url,
            "authority": self.authority,
            "jurisdiction": self.jurisdiction,
            "consulted_on": self.consulted_on.isoformat() if self.consulted_on else "",
            "consulted_by": self.consulted_by,
        }


class LegalRuleQuerySet(models.QuerySet):
    def in_force(self, on_date=None):
        """
        Rules ACTIVE on a given date.

        The date is the assessment's own date, never "today": an outcome given in October must stay
        explainable in March, when the rules have moved on without it.
        """
        on_date = on_date or timezone.localdate()
        return self.filter(
            review_status=ReviewStatus.ACTIVE,
            valid_from__lte=on_date,
        ).filter(models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=on_date))

    def for_pathway(self, jurisdiction: str, pathway: str):
        return self.filter(jurisdiction=jurisdiction, pathway=pathway)


class LegalRule(TimeStampedModel):
    """One versioned legal rule. Every field of Technical Blueprint §7 is here and does work."""

    rule_id = models.SlugField(
        _("identificativo"),
        max_length=64,
        help_text=_("Stabile attraverso le versioni: R-2026-014 resta R-2026-014."),
    )
    version = models.PositiveIntegerField(_("versione"), default=1)

    jurisdiction = models.CharField(
        _("giurisdizione"), max_length=8, default="IT", help_text=_("Ordinamento di riferimento, es. IT, MA.")
    )
    pathway = models.CharField(
        _("percorso"), max_length=64, help_text=_("Chiave della famiglia di percorsi cui la regola si applica.")
    )

    condition = models.JSONField(
        _("condizione"),
        default=dict,
        blank=True,
        help_text=_("DSL JSON ristretto. Un oggetto vuoto significa «sempre vera»."),
    )
    effect = models.CharField(_("effetto"), max_length=24, choices=RuleEffect.choices)
    message_key = models.CharField(
        _("chiave del messaggio"),
        max_length=120,
        help_text=_("Il testo mostrato vive nel sistema di traduzione, non nella regola."),
    )
    message_fr = models.CharField(
        _("messaggio (FR)"),
        max_length=300,
        help_text=_("Testo sorgente francese, tradotto attraverso i cataloghi."),
    )
    requirement_fr = models.CharField(
        _("requisito (FR)"),
        max_length=300,
        blank=True,
        help_text=_("Per un effetto «requisito mancante»: che cosa manca, in forma comprensibile."),
    )
    responsible_actor = models.CharField(
        _("responsabile"),
        max_length=20,
        blank=True,
        choices=_responsible_actor_choices,
        help_text=_("Chi deve agire perché il requisito sia soddisfatto. Vuoto se non pertinente."),
    )

    sources = models.ManyToManyField(
        LegalSource,
        related_name="rules",
        blank=True,
        verbose_name=_("fonti"),
        help_text=_("Almeno una è obbligatoria per attivare la regola."),
    )

    valid_from = models.DateField(_("in vigore dal"))
    valid_to = models.DateField(_("in vigore fino al"), null=True, blank=True)

    review_status = models.CharField(
        _("stato"), max_length=16, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT, db_index=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="rules_authored"
    )
    provenance = models.CharField(
        _("provenienza del contenuto"),
        max_length=24,
        choices=RuleProvenance.choices,
        default=RuleProvenance.DRAFTED_FROM_SOURCE,
        db_index=True,
        help_text=_("Da dove viene il testo della regola. Il contenuto ereditato parte da «candidata»."),
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="rules_approved"
    )
    approved_by_label = models.CharField(
        _("approvata da (registrato)"),
        max_length=200,
        blank=True,
        help_text=_(
            "Chi ha approvato, come testo che sopravvive all'anonimizzazione dell'account. "
            "È questo campo, non la chiave esterna, che il vincolo di database esige: "
            "una regola in vigore deve dire chi la sostiene anche dopo che quell'account è sparito."
        ),
    )
    approved_at = models.DateTimeField(_("approvata il"), null=True, blank=True)
    retired_at = models.DateTimeField(_("ritirata il"), null=True, blank=True)
    note = models.TextField(_("motivazione interna"), blank=True)

    objects = LegalRuleQuerySet.as_manager()

    class Meta:
        verbose_name = _("regola giuridica")
        verbose_name_plural = _("regole giuridiche")
        ordering = ["pathway", "rule_id", "-version"]
        constraints = [
            models.UniqueConstraint(fields=["rule_id", "version"], name="unique_rule_version"),
            # Eleven rules were ACTIVE with `approved_by` null, because the seed wrote the status
            # straight to the column and never went through `services.transition`. The service
            # enforced four eyes; nothing enforced that a rule in force had been approved at all.
            # A domain rule that only the service applies is a rule the next writer will bypass
            # without noticing, so it lives in the database.
            #
            # The check is on the LABEL, not the foreign key: `approved_by` is SET_NULL, and
            # anonymising an account under art. 17 must not make a rule in force unrepresentable.
            models.CheckConstraint(
                condition=(
                    ~models.Q(review_status__in=["approved", "active"])
                    | ~models.Q(approved_by_label="")
                ),
                name="approved_or_active_rule_names_its_approver",
            ),
        ]
        indexes = [
            models.Index(fields=["jurisdiction", "pathway", "review_status"]),
            models.Index(fields=["review_status", "valid_from"]),
        ]

    def __str__(self) -> str:
        return f"{self.rule_id} v{self.version} — {self.get_effect_display()}"

    def clean(self) -> None:
        if self.valid_to and self.valid_to < self.valid_from:
            raise ValidationError({"valid_to": _("La fine della validità precede l'inizio.")})
        if self.effect == RuleEffect.MISSING_REQUIREMENT and not self.requirement_fr.strip():
            raise ValidationError(
                {"requirement_fr": _("Un effetto «requisito mancante» deve dire che cosa manca.")}
            )
        from rules.engine import InvalidCondition, validate_condition

        try:
            validate_condition(self.condition or {})
        except InvalidCondition as exc:
            raise ValidationError({"condition": str(exc)}) from exc

        if self.review_status in APPROVED_STATUSES and not self.approved_by_label.strip():
            raise ValidationError(
                {
                    "review_status": _(
                        "Una regola approvata o in vigore deve dire chi la sostiene. "
                        "Passare da «%(status)s» attraverso il flusso di revisione, non cambiando "
                        "lo stato a mano."
                    )
                    % {"status": self.get_review_status_display()}
                }
            )

    @property
    def unverified_sources(self):
        """The sources that still owe a consultation date, a name, and somewhere to look."""
        return [s for s in self.sources.all() if not s.is_verified]

    def is_in_force(self, on_date=None) -> bool:
        on_date = on_date or timezone.localdate()
        if self.review_status != ReviewStatus.ACTIVE or self.valid_from > on_date:
            return False
        return self.valid_to is None or self.valid_to >= on_date

    def as_snapshot(self, lang: str = "fr") -> dict:
        """
        The rule as it is frozen into an assessment.

        The snapshot carries the CONDITION and the SOURCES, not a reference to them: an assessment
        must stay reproducible and explainable after the rule is retired and the source has moved.

        It also carries `provenance` and `approved_by_label`. Those two answer a question the rest
        of the snapshot cannot: not «what did the rule say», but «on whose authority». A result
        produced by the demonstration ruleset carries a label that says no jurist approved it, and
        it carries it into the stored assessment — so the disclaimer survives being read six months
        later by somebody who was not here today.
        """
        return {
            "rule_id": self.rule_id,
            "version": self.version,
            "jurisdiction": self.jurisdiction,
            "pathway": self.pathway,
            "provenance": self.provenance,
            "condition": self.condition or {},
            "effect": self.effect,
            "message_key": self.message_key,
            "message": self.message_fr,
            "requirement": self.requirement_fr,
            "responsible_actor": self.responsible_actor,
            "valid_from": self.valid_from.isoformat(),
            "valid_to": self.valid_to.isoformat() if self.valid_to else "",
            "approved_by": self.approved_by_label,
            "approved_at": self.approved_at.isoformat() if self.approved_at else "",
            "sources": [source.as_citation(lang) for source in self.sources.all()],
        }
