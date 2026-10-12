"""
Entreprises et besoins en compétences — the B2B side of the platform, WITHOUT a people browser.

An impresa expresses a NEED. It never browses, searches, counts or ranks persons. Selection is a
reserved activity and belongs to a named, authorised actor (CONFLICT_REGISTER CR-03 / CR-04,
PLATFORM_REQUIREMENTS_V2 §8, ROLE_JOURNEYS §2). Nothing in this module can return a person: the only
relation to ``AUTH_USER_MODEL`` that exists here is ``NeedAssignment.assignee``, which is the actor
answerable for the need — the opposite of a candidate.

Four invariants are enforced by the domain rather than by the interface:

1. **No age criterion, in any form.** The previous platform carried a structured age band on every
   job opening (20–45, 21–48, 28–55 …). That is direct age discrimination under Directive
   2000/78/EC and D.lgs. 216/2003, and the audit is explicit that the field must not be migrated.
   There is therefore no age field here, and ``validate_no_age_criterion`` refuses one typed into
   the free-text criteria: a requirement linked to age must be justified in writing against a rule
   and pass legal review before it exists as data at all.
2. **A need is transmitted only by a VERIFIED company** (``accounts.AccountVerification`` decides;
   this app never decides a verification, it reads the decision).
3. **A need cannot be taken in charge without a live authorisation.** ``IN_PROGRESS`` requires a
   non-revoked ``NeedAssignment`` as authorised actor carrying an authorisation reference valid
   today — the same rule the case file applies to ``SELECTION``.
4. **A transition that is not declared is refused**, and every declared one is audited
   (``companies.services``).

Taxonomies (sector, territory) are configurable rows, never a hard-coded list: Technical Blueprint
§20 puts professional, skill and document taxonomies outside the code.
"""

from __future__ import annotations

import re
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

# ---------------------------------------------------------------------------------------------
# The age guard
# ---------------------------------------------------------------------------------------------
#: An age word in any of the four languages. Word boundaries matter: « stage », « apprentissage »
#: and « langage » all contain "age" and none of them is an age criterion.
_AGE_WORDS = re.compile(r"(?<![\w’'-])(âge|age|aged|ages|âges|età|eta|edad|عمر|العمر|سن|السن)(?![\w’'-])", re.I)
#: A bare band of two plausible ages, e.g. « 24–50 », even with no word attached. Ranges below 15
#: are years of experience and are legitimate, so the band only triggers on two adult-looking values.
_AGE_BAND = re.compile(r"\b(1[5-9]|[2-7]\d)\s*[-–—/]\s*(1[5-9]|[2-7]\d)\b")
_DIGIT = re.compile(r"\d")

AGE_CRITERION_MESSAGE = _(
    "Un critère d’âge ne peut pas figurer dans un besoin : la sélection fondée sur l’âge est une "
    "discrimination directe (directive 2000/78/CE, D.lgs. 216/2003). Décrivez la tâche, la "
    "qualification ou l’expérience requise. Une exigence réellement liée à l’âge doit être motivée "
    "par écrit, rattachée à une norme et examinée par la revue juridique avant d’exister."
)


def validate_no_age_criterion(value) -> None:
    """
    Refuse an age criterion typed into a free-text requirement field.

    Two signals, both deliberately narrow so a legitimate « 3 à 5 ans d’expérience » passes:
    an age WORD together with a figure, or a bare band of two adult ages such as « 24-50 ».
    """
    text = str(value or "")
    if not text.strip():
        return
    if _AGE_BAND.search(text):
        raise ValidationError(AGE_CRITERION_MESSAGE)
    if _AGE_WORDS.search(text) and _DIGIT.search(text):
        raise ValidationError(AGE_CRITERION_MESSAGE)


# ---------------------------------------------------------------------------------------------
# Configurable taxonomies (Technical Blueprint §20 — never hard-coded)
# ---------------------------------------------------------------------------------------------
class TaxonomyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def ordered(self):
        return self.order_by("order", "label_fr")


def taxonomy_label(row) -> str:
    """
    The label of a taxonomy row in the reading language, falling back to the French source.

    The Italian labels are seeded and editable in the back-office but were reaching no screen: every
    template printed ``label_fr``, so an Italian reader was shown a French sector. A taxonomy row is
    editorial content, not a msgid, so it is not translated through the catalogues; the fallback is
    the French source, which is this project's source language.
    """
    from django.utils.translation import get_language

    language = (get_language() or "").split("-")[0]
    if language == "it" and getattr(row, "label_it", ""):
        return row.label_it
    return row.label_fr


class Sector(TimeStampedModel):
    """An activity sector. Editable in the back-office; the code is the stable identifier."""

    code = models.SlugField(_("code"), max_length=48, unique=True)
    label_fr = models.CharField(_("libellé (FR)"), max_length=120)
    label_it = models.CharField(_("libellé (IT)"), max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(_("ordre"), default=0, db_index=True)
    is_active = models.BooleanField(_("actif"), default=True)

    objects = TaxonomyQuerySet.as_manager()

    class Meta:
        verbose_name = _("secteur d’activité")
        verbose_name_plural = _("secteurs d’activité")
        ordering = ["order", "label_fr"]

    def __str__(self) -> str:
        return self.label_fr

    @property
    def label(self) -> str:
        return taxonomy_label(self)


class Territory(TimeStampedModel):
    """A territory of destination — a region or a province, configurable, never hard-coded."""

    code = models.SlugField(_("code"), max_length=48, unique=True)
    label_fr = models.CharField(_("libellé (FR)"), max_length=120)
    label_it = models.CharField(_("libellé (IT)"), max_length=120, blank=True)
    country = models.CharField(_("pays"), max_length=2, default="IT")
    order = models.PositiveSmallIntegerField(_("ordre"), default=0, db_index=True)
    is_active = models.BooleanField(_("actif"), default=True)

    objects = TaxonomyQuerySet.as_manager()

    class Meta:
        verbose_name = _("territoire")
        verbose_name_plural = _("territoires")
        ordering = ["order", "label_fr"]

    def __str__(self) -> str:
        return self.label_fr

    @property
    def label(self) -> str:
        return taxonomy_label(self)


# ---------------------------------------------------------------------------------------------
# The company
# ---------------------------------------------------------------------------------------------
class CompanySize(models.TextChoices):
    """EU size bands (Recommendation 2003/361/EC). A band, not a headcount: less data, same use."""

    MICRO = "micro", _("Micro-entreprise (moins de 10 personnes)")
    SMALL = "small", _("Petite entreprise (10 à 49)")
    MEDIUM = "medium", _("Entreprise moyenne (50 à 249)")
    LARGE = "large", _("Grande entreprise (250 et plus)")


class CompanyProfileQuerySet(models.QuerySet):
    def readable_by(self, user) -> CompanyProfileQuerySet:
        """
        Authorisation applied AT QUERY TIME. A company never learns that another company exists.

        Project staff get nothing here either: supervision happens in the back-office, where every
        access is role-checked and auditable. Same reasoning as ``CaseFileQuerySet.readable_by``.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        return self.filter(organisation__memberships__user=user).distinct()


class CompanyProfile(TimeStampedModel):
    """
    The managed identity of an impresa, attached to ``accounts.Organisation``.

    The fields collected are exactly the ones that make a VERIFICATION possible — legal name, trade
    name, registration and VAT numbers, sector, size, year founded, a contact person WITH THEIR
    FUNCTION, an address. The previous platform collected these and was right to; what it did with
    them afterwards is what this platform does not repeat.

    The verification STATE is not stored here: ``accounts.AccountVerification`` decides it, and this
    model reads the decision (``verification`` / ``is_verified``). Two places holding the same truth
    is one place holding a stale one.
    """

    organisation = models.OneToOneField(
        "accounts.Organisation",
        on_delete=models.CASCADE,
        related_name="company_profile",
        verbose_name=_("organisation"),
    )
    legal_name = models.CharField(_("dénomination légale"), max_length=200)
    trade_name = models.CharField(
        _("nom commercial"), max_length=200, blank=True, help_text=_("S’il diffère de la dénomination légale.")
    )
    registration_number = models.CharField(
        _("numéro d’immatriculation"),
        max_length=60,
        blank=True,
        help_text=_("Registro delle Imprese / REA, ou l’équivalent du pays d’établissement."),
    )
    vat_number = models.CharField(
        _("numéro de TVA"), max_length=40, blank=True, help_text=_("Partita IVA, ICE, ou équivalent.")
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        related_name="companies",
        null=True,
        blank=True,
        verbose_name=_("secteur d’activité"),
    )
    size = models.CharField(_("taille"), max_length=8, choices=CompanySize.choices, blank=True)
    year_founded = models.PositiveSmallIntegerField(
        _("année de création"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2200)],
    )
    contact_name = models.CharField(_("référent"), max_length=160)
    contact_function = models.CharField(
        _("fonction du référent"),
        max_length=160,
        help_text=_("Obligatoire : une vérification s’adresse à une fonction, pas à un nom seul."),
    )
    contact_email = models.EmailField(_("e-mail du référent"), max_length=254)
    contact_phone = models.CharField(_("téléphone du référent"), max_length=40, blank=True)
    address_line = models.CharField(_("adresse"), max_length=200, blank=True)
    postal_code = models.CharField(_("code postal"), max_length=16, blank=True)
    city = models.CharField(_("ville"), max_length=120)
    province = models.CharField(_("province ou région"), max_length=120, blank=True)
    country = models.CharField(_("pays"), max_length=2, default="IT")
    website = models.URLField(_("site web"), blank=True)

    objects = CompanyProfileQuerySet.as_manager()

    class Meta:
        verbose_name = _("entreprise")
        verbose_name_plural = _("entreprises")
        ordering = ["legal_name"]

    def __str__(self) -> str:
        return self.legal_name

    def clean(self) -> None:
        from accounts.models import OrganisationKind

        if self.organisation_id and self.organisation.kind != OrganisationKind.COMPANY:
            raise ValidationError(
                {"organisation": _("Ce profil ne s’attache qu’à une organisation de type entreprise.")}
            )
        if not self.contact_function.strip():
            raise ValidationError({"contact_function": _("Indiquez la fonction du référent.")})
        if self.year_founded and self.year_founded > timezone.localdate().year:
            raise ValidationError({"year_founded": _("L’année de création ne peut pas être dans le futur.")})

    # -- verification, read from accounts ------------------------------------------------------
    @property
    def verification(self):
        """
        The ``accounts.AccountVerification`` that decides this company's state, or None.

        Only a verification whose DECLARED TYPE is « impresa » counts. ``AccountVerification`` holds
        one row per account and records what that account declared; an account approved as a
        professional carries an APPROVED row, and reading it here would verify a company nobody ever
        verified — and would open the transmission gate of REQ-B2B-01 on the strength of a decision
        taken about something else.

        The organisation may have several members; the decision that counts is the one taken on a
        responsible member's account. APPROVED wins over PENDING wins over REJECTED, because a
        company with one approved responsible IS verified, whatever a second, stale row says.
        """
        from accounts.models import AccountType, AccountVerification, VerificationStatus

        rows = list(
            AccountVerification.objects.filter(
                user__memberships__organisation_id=self.organisation_id,
                declared_type=AccountType.COMPANY,
            ).order_by("-created_at")
        )
        if not rows:
            return None
        ranking = {
            VerificationStatus.APPROVED: 0,
            VerificationStatus.PENDING: 1,
            VerificationStatus.NOT_REQUIRED: 2,
            VerificationStatus.REJECTED: 3,
        }
        return sorted(rows, key=lambda row: ranking.get(row.status, 9))[0]

    @property
    def verification_status(self) -> str:
        from accounts.models import VerificationStatus

        row = self.verification
        return row.status if row is not None else VerificationStatus.PENDING

    @property
    def verification_label(self) -> str:
        from accounts.models import VerificationStatus

        return dict(VerificationStatus.choices).get(self.verification_status, str(_("En attente de vérification")))

    @property
    def is_verified(self) -> bool:
        from accounts.models import VerificationStatus

        return self.verification_status == VerificationStatus.APPROVED

    @property
    def verification_state_modifier(self) -> str:
        """State chip modifier — the word always carries the meaning, the rule only repeats it."""
        from accounts.models import VerificationStatus

        return {
            VerificationStatus.APPROVED: "valid",
            VerificationStatus.PENDING: "review",
            VerificationStatus.REJECTED: "invalid",
            VerificationStatus.NOT_REQUIRED: "filed",
        }.get(self.verification_status, "review")

    @property
    def display_address(self) -> str:
        parts = [self.address_line, f"{self.postal_code} {self.city}".strip(), self.province, self.country]
        return ", ".join(part for part in parts if part and part.strip())


# ---------------------------------------------------------------------------------------------
# The need
# ---------------------------------------------------------------------------------------------
class NeedStatus(models.TextChoices):
    """
    States of a need. Each one is a FACT about the file, never a verdict about anyone.

    There is no « approved » and no « matched »: this platform approves nobody and matches nobody.
    """

    DRAFT = "draft", _("Brouillon")
    SUBMITTED = "submitted", _("Transmis au projet")
    UNDER_REVIEW = "under_review", _("En cours d’examen")
    IN_PROGRESS = "in_progress", _("Pris en charge")
    ON_HOLD = "on_hold", _("En attente")
    CLOSED = "closed", _("Clos")
    WITHDRAWN = "withdrawn", _("Retiré par l’entreprise")


#: Declared transitions. Anything absent here is refused by ``companies.services.transition``.
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    NeedStatus.DRAFT: frozenset({NeedStatus.SUBMITTED, NeedStatus.WITHDRAWN}),
    NeedStatus.SUBMITTED: frozenset({NeedStatus.UNDER_REVIEW, NeedStatus.ON_HOLD, NeedStatus.WITHDRAWN}),
    NeedStatus.UNDER_REVIEW: frozenset(
        {NeedStatus.IN_PROGRESS, NeedStatus.ON_HOLD, NeedStatus.SUBMITTED, NeedStatus.CLOSED}
    ),
    NeedStatus.IN_PROGRESS: frozenset({NeedStatus.ON_HOLD, NeedStatus.CLOSED}),
    NeedStatus.ON_HOLD: frozenset(
        {NeedStatus.SUBMITTED, NeedStatus.UNDER_REVIEW, NeedStatus.IN_PROGRESS, NeedStatus.CLOSED, NeedStatus.WITHDRAWN}
    ),
    NeedStatus.CLOSED: frozenset(),
    NeedStatus.WITHDRAWN: frozenset(),
}

#: States whose entry requires a live authorised actor on the need (CR-03).
REQUIRES_AUTHORISED_ACTOR: frozenset[str] = frozenset({NeedStatus.IN_PROGRESS})

#: States in which the company may still edit its own need. Once an authorised actor has taken the
#: need in charge, a change goes through the project rather than behind the actor's back.
COMPANY_EDITABLE_STATUSES: frozenset[str] = frozenset(
    {NeedStatus.DRAFT, NeedStatus.SUBMITTED, NeedStatus.UNDER_REVIEW, NeedStatus.ON_HOLD}
)

#: States a company may withdraw from on its own.
COMPANY_WITHDRAWABLE_STATUSES: frozenset[str] = frozenset({NeedStatus.DRAFT, NeedStatus.SUBMITTED, NeedStatus.ON_HOLD})

#: States counted in the territorial / sectoral aggregate. A draft is a private working document and
#: a withdrawn need is not a need: neither belongs in an analysis of expressed needs.
AGGREGATED_STATUSES: frozenset[str] = frozenset(
    {NeedStatus.SUBMITTED, NeedStatus.UNDER_REVIEW, NeedStatus.IN_PROGRESS, NeedStatus.ON_HOLD, NeedStatus.CLOSED}
)

#: status -> the ``.state--*`` modifier of the design system. No new colour is invented.
STATE_MODIFIERS: dict[str, str] = {
    NeedStatus.DRAFT: "missing",
    NeedStatus.SUBMITTED: "filed",
    NeedStatus.UNDER_REVIEW: "review",
    NeedStatus.IN_PROGRESS: "filed",
    NeedStatus.ON_HOLD: "replace",
    NeedStatus.CLOSED: "done",
    NeedStatus.WITHDRAWN: "expired",
}


def transitions_from(status: str) -> frozenset[str]:
    return ALLOWED_TRANSITIONS.get(status, frozenset())


class EngagementType(models.TextChoices):
    """The form of the engagement. A fact about the WORK, never about the person."""

    PERMANENT = "permanent", _("Contrat à durée indéterminée")
    FIXED_TERM = "fixed_term", _("Contrat à durée déterminée")
    SEASONAL = "seasonal", _("Travail saisonnier")
    APPRENTICESHIP = "apprenticeship", _("Apprentissage / contrat de formation")
    OTHER = "other", _("Autre forme prévue par la loi")


class LanguageLevel(models.TextChoices):
    """CEFR levels. A language requirement is a requirement of the post, and must be stated as one."""

    NONE = "none", _("Aucune exigence formalisée")
    A1 = "a1", _("A1 — découverte")
    A2 = "a2", _("A2 — intermédiaire")
    B1 = "b1", _("B1 — seuil")
    B2 = "b2", _("B2 — avancé")
    C1 = "c1", _("C1 — autonome")


class CompanyNeedQuerySet(models.QuerySet):
    def readable_by(self, user) -> CompanyNeedQuerySet:
        """Authorisation in the queryset: a company sees ITS needs, and no other company's."""
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        assigned = models.Q(assignments__assignee=user, assignments__revoked_at__isnull=True) & (
            models.Q(assignments__authorisation_valid_until__isnull=True)
            | models.Q(assignments__authorisation_valid_until__gte=timezone.localdate())
        )
        return self.filter(models.Q(company__organisation__memberships__user=user) | assigned).distinct()

    def open(self) -> CompanyNeedQuerySet:
        return self.exclude(status__in=[NeedStatus.CLOSED, NeedStatus.WITHDRAWN])

    def aggregated(self) -> CompanyNeedQuerySet:
        return self.filter(status__in=AGGREGATED_STATUSES)


class CompanyNeed(TimeStampedModel):
    """
    One expressed need for skills. NOT an offer, not an advertisement, not a posting.

    It describes a territory, a sector, a professional profile, duties, the skills required and
    preferred, a language requirement, safety training, experience, a quantity, a timing and the
    training the company expects. It describes the WORK. It describes nobody.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(
        _("référence"),
        max_length=16,
        unique=True,
        editable=False,
        help_text=_("Référence courte citée dans les échanges avec le projet."),
    )
    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name="needs", verbose_name=_("entreprise")
    )
    title = models.CharField(
        _("intitulé du besoin"),
        max_length=160,
        validators=[validate_no_age_criterion],
        help_text=_(
            "Ce que l’entreprise cherche à couvrir, en une ligne. Ex. « Maintenance des lignes d’embouteillage »."
        ),
    )
    territory = models.ForeignKey(
        Territory,
        on_delete=models.PROTECT,
        related_name="needs",
        null=True,
        blank=True,
        verbose_name=_("territoire"),
    )
    work_place = models.CharField(_("lieu de travail"), max_length=160, blank=True)
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, related_name="needs", null=True, blank=True, verbose_name=_("secteur")
    )
    professional_profile = models.CharField(
        _("profil professionnel"),
        max_length=160,
        blank=True,
        validators=[validate_no_age_criterion],
        help_text=_("La qualification visée, dans les termes du métier. Ex. « Soudeur TIG/MIG »."),
    )
    duties = models.TextField(
        _("tâches confiées"),
        blank=True,
        validators=[validate_no_age_criterion],
        help_text=_("Ce que la personne aura à faire. Décrivez le poste, jamais la personne."),
    )
    motivation = models.TextField(
        _("motif du besoin"),
        blank=True,
        validators=[validate_no_age_criterion],
        help_text=_(
            "Pourquoi ce besoin existe : croissance de l’activité, remplacement d’un départ, "
            "saisonnalité, ouverture d’un marché. Il explique le besoin de l’entreprise, jamais la "
            "personne attendue."
        ),
    )
    engagement_type = models.CharField(
        _("forme de l’engagement"), max_length=16, choices=EngagementType.choices, blank=True
    )
    headcount = models.PositiveSmallIntegerField(
        _("nombre de profils"), default=1, validators=[MinValueValidator(1), MaxValueValidator(999)]
    )
    experience_years_min = models.PositiveSmallIntegerField(
        _("expérience minimale (années)"),
        default=0,
        validators=[MaxValueValidator(45)],
        help_text=_("0 lorsque l’expérience n’est pas une condition."),
    )
    experience_note = models.CharField(
        _("précision sur l’expérience"), max_length=200, blank=True, validators=[validate_no_age_criterion]
    )
    language_code = models.CharField(_("langue requise"), max_length=8, choices=settings.LANGUAGES, blank=True)
    language_level = models.CharField(
        _("niveau requis"), max_length=8, choices=LanguageLevel.choices, default=LanguageLevel.NONE
    )
    language_note = models.CharField(
        _("précision sur la langue"), max_length=200, blank=True, validators=[validate_no_age_criterion]
    )
    safety_training_required = models.BooleanField(
        _("formation à la sécurité requise"),
        default=False,
        help_text=_("Formation générale et spécifique (D.lgs. 81/2008) exigée pour le poste."),
    )
    safety_training_note = models.CharField(
        _("précision sur la sécurité"), max_length=200, blank=True, validators=[validate_no_age_criterion]
    )
    training_needs = models.TextField(
        _("besoins de formation"),
        blank=True,
        validators=[validate_no_age_criterion],
        help_text=_("Ce que l’entreprise attend du parcours de formation en amont."),
    )
    start_from = models.DateField(_("à partir du"), null=True, blank=True)
    timing_note = models.CharField(
        _("précision sur le calendrier"), max_length=200, blank=True, validators=[validate_no_age_criterion]
    )
    status = models.CharField(
        _("état"), max_length=16, choices=NeedStatus.choices, default=NeedStatus.DRAFT, db_index=True
    )
    status_since = models.DateTimeField(_("dans cet état depuis le"), default=timezone.now, editable=False)
    submitted_at = models.DateTimeField(_("transmis le"), null=True, blank=True, editable=False)
    closed_at = models.DateTimeField(_("clos le"), null=True, blank=True, editable=False)
    hold_reason = models.CharField(_("motif de l’attente"), max_length=300, blank=True)

    objects = CompanyNeedQuerySet.as_manager()

    class Meta:
        verbose_name = _("besoin en compétences")
        verbose_name_plural = _("besoins en compétences")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company", "status"]),
            models.Index(fields=["status", "status_since"]),
            models.Index(fields=["territory", "status"]),
            models.Index(fields=["sector", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.reference} · {self.title}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._new_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _new_reference() -> str:
        """Non-sequential: a sequential reference leaks how many needs the platform holds."""
        for _attempt in range(12):
            candidate = "B" + uuid.uuid4().hex[:9].upper()
            if not CompanyNeed.objects.filter(reference=candidate).exists():
                return candidate
        raise RuntimeError("could not allocate a unique need reference")

    def clean(self) -> None:
        if self.status == NeedStatus.ON_HOLD and not self.hold_reason.strip():
            raise ValidationError({"hold_reason": _("Une mise en attente doit être motivée.")})

    # -- lifecycle -----------------------------------------------------------------------------
    @property
    def state_modifier(self) -> str:
        return STATE_MODIFIERS.get(self.status, "filed")

    @property
    def is_editable_by_company(self) -> bool:
        return self.status in COMPANY_EDITABLE_STATUSES

    @property
    def is_withdrawable(self) -> bool:
        return self.status in COMPANY_WITHDRAWABLE_STATUSES

    @property
    def is_open(self) -> bool:
        return self.status not in {NeedStatus.CLOSED, NeedStatus.WITHDRAWN}

    def allowed_transitions(self) -> frozenset[str]:
        return transitions_from(self.status)

    def has_live_authorised_actor(self) -> bool:
        """A non-revoked authorised actor whose authorisation is valid today (CR-03)."""
        today = timezone.localdate()
        return (
            self.assignments.filter(
                role=ActorRole.AUTHORISED_ACTOR,
                revoked_at__isnull=True,
                authorisation_reference__gt="",
            )
            .filter(models.Q(authorisation_valid_until__isnull=True) | models.Q(authorisation_valid_until__gte=today))
            .exists()
        )

    # -- completeness --------------------------------------------------------------------------
    #: What a need must carry before it can be transmitted. Kept as data so the interface can list
    #: exactly what is missing instead of saying « formulaire incomplet ».
    REQUIRED_FOR_SUBMISSION: tuple[tuple[str, object], ...] = (
        ("title", _("un intitulé")),
        ("territory", _("un territoire")),
        ("sector", _("un secteur")),
        ("professional_profile", _("un profil professionnel")),
        ("duties", _("les tâches confiées")),
    )

    def missing_for_submission(self) -> list[str]:
        """Everything still missing before the need can be transmitted, in words."""
        missing = [str(label) for name, label in self.REQUIRED_FOR_SUBMISSION if not getattr(self, name, None)]
        if not self.skills.filter(level=SkillLevel.MANDATORY).exists():
            missing.append(str(_("au moins une compétence obligatoire")))
        return missing

    @property
    def is_complete(self) -> bool:
        return not self.missing_for_submission()

    # -- read helpers --------------------------------------------------------------------------
    def mandatory_skills(self):
        return self.skills.filter(level=SkillLevel.MANDATORY).order_by("order", "id")

    def preferred_skills(self):
        return self.skills.filter(level=SkillLevel.PREFERRED).order_by("order", "id")

    def live_assignments(self):
        return [row for row in self.assignments.all() if row.is_live]

    @property
    def language_requirement(self) -> str:
        """The language requirement in one readable line, or an empty string when there is none."""
        if not self.language_code:
            return ""
        label = dict(settings.LANGUAGES).get(self.language_code, self.language_code)
        if self.language_level and self.language_level != LanguageLevel.NONE:
            level = dict(LanguageLevel.choices)[self.language_level]
            return f"{label} — {level}"
        return str(label)


class SkillLevel(models.TextChoices):
    MANDATORY = "mandatory", _("Obligatoire")
    PREFERRED = "preferred", _("Souhaitée")


class NeedSkill(TimeStampedModel):
    """
    One skill required or preferred by a need.

    A row rather than a paragraph, because the skill gap of the Academy is « required competence →
    held competence → gap → training module », and a paragraph cannot take part in that.
    """

    need = models.ForeignKey(CompanyNeed, on_delete=models.CASCADE, related_name="skills", verbose_name=_("besoin"))
    label = models.CharField(_("compétence"), max_length=160, validators=[validate_no_age_criterion])
    level = models.CharField(_("niveau d’exigence"), max_length=12, choices=SkillLevel.choices)
    note = models.CharField(_("précision"), max_length=200, blank=True, validators=[validate_no_age_criterion])
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)

    class Meta:
        verbose_name = _("compétence du besoin")
        verbose_name_plural = _("compétences du besoin")
        ordering = ["need", "level", "order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["need", "label", "level"], name="uniq_need_skill"),
        ]

    def __str__(self) -> str:
        return f"{self.label} ({self.get_level_display()})"


class ActorRole(models.TextChoices):
    """Who may be answerable for a need. Deliberately never « Italy Legal Entry » alone."""

    AUTHORISED_ACTOR = "authorised_actor", _("Soggetto autorizzato / acteur autorisé")
    TRAINING_BODY = "training_body", _("Organisme de formation")
    PROFESSIONAL = "professional", _("Professionnel mandaté")
    PROJECT_TEAM = "project_team", _("Équipe du projet")


class NeedAssignment(TimeStampedModel):
    """
    WHO is answerable for this need, in which capacity, under which authorisation, until when.

    This is the first link of the mandatory chain of CR-03:
    ``CompanyNeed → AuthorizedActor → SelectionProcess → CaseFile → AuditEvent``. The selection
    process itself belongs to the selection workspace; what lives here is the company's right to
    know who is answerable, which ROLE_JOURNEYS §2 states as « chi sta seguendo quale fase, con
    nome e ruolo ».

    ``assignee`` is the only relation to a user account in this app, and it points at an ACTOR, not
    at a candidate: no view here ever lists, searches or counts persons.
    """

    need = models.ForeignKey(
        CompanyNeed, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("besoin")
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_need_assignments",
        verbose_name=_("intervenant"),
    )
    role = models.CharField(_("qualité"), max_length=20, choices=ActorRole.choices)
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="need_assignments",
        verbose_name=_("organisation responsable"),
    )
    authorisation_reference = models.CharField(
        _("référence de l’autorisation"),
        max_length=200,
        blank=True,
        help_text=_("Obligatoire pour un acteur autorisé : les références de l’habilitation."),
    )
    authorisation_jurisdiction = models.CharField(_("juridiction"), max_length=8, blank=True)
    authorisation_valid_until = models.DateField(_("autorisation valable jusqu’au"), null=True, blank=True)
    mandate_note = models.CharField(_("note sur le mandat"), max_length=300, blank=True)
    assigned_at = models.DateTimeField(_("assigné le"), default=timezone.now)
    revoked_at = models.DateTimeField(_("révoqué le"), null=True, blank=True)

    class Meta:
        verbose_name = _("intervenant sur un besoin")
        verbose_name_plural = _("intervenants sur un besoin")
        ordering = ["-assigned_at"]
        indexes = [models.Index(fields=["need", "revoked_at"])]

    def __str__(self) -> str:
        return f"{self.get_role_display()} · {self.need.reference}"

    @property
    def is_live(self) -> bool:
        if self.revoked_at is not None:
            return False
        return not (self.authorisation_valid_until and self.authorisation_valid_until < timezone.localdate())

    @property
    def display_name(self) -> str:
        """
        The responsible party, named — never an e-mail address.

        An e-mail address is the account identifier, not a professional identity: printing it on a
        company's screen would publish a staff member's contact data to satisfy a label.
        """
        if self.organisation_id and self.organisation is not None:
            return self.organisation.name
        full_name = (getattr(self.assignee, "full_name", "") or "").strip()
        return full_name or str(self.get_role_display())

    def clean(self) -> None:
        if self.role == ActorRole.AUTHORISED_ACTOR and not self.authorisation_reference.strip():
            raise ValidationError(
                {"authorisation_reference": _("Un acteur autorisé ne l’est que par une autorisation référencée.")}
            )


class NeedEvent(TimeStampedModel):
    """
    The visible history of a need — what happened, when, and on whose responsibility.

    The audit trail records the same facts for the auditor; this is the company's own copy, because
    « où en est mon besoin » is a question a company must be able to answer without asking anyone.
    Deliberately no e-mail address and no personal data: only a state, a note and a responsible
    party named by organisation or role.
    """

    need = models.ForeignKey(CompanyNeed, on_delete=models.CASCADE, related_name="events", verbose_name=_("besoin"))
    from_status = models.CharField(_("état précédent"), max_length=16, choices=NeedStatus.choices, blank=True)
    to_status = models.CharField(_("nouvel état"), max_length=16, choices=NeedStatus.choices)
    note = models.CharField(_("précision"), max_length=300, blank=True)
    responsible_label = models.CharField(_("responsable"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("étape du besoin")
        verbose_name_plural = _("étapes du besoin")
        ordering = ["created_at", "id"]
        indexes = [models.Index(fields=["need", "created_at"])]

    def __str__(self) -> str:
        return f"{self.need_id} → {self.to_status}"

    @property
    def state_modifier(self) -> str:
        return STATE_MODIFIERS.get(self.to_status, "filed")
