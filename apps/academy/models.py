"""
Academy — the training catalogue, enrolment and progression.

The one rule that shapes every model here is the client's own acceptance criterion (Technical
Blueprint §17, CONFLICT_REGISTER CR-14): «Una persona può accedere all'Academy senza essere
selezionata da un'impresa.» There is therefore **no field, no foreign key and no status anywhere in
this module that could make access conditional on a company, a selection or a case file**. The
catalogue is designed from territorial needs — that is how a catalogue is *built* — but who may
enter it is settled here: any authenticated person, full stop.

Four consequences that are enforced rather than documented:

1. ``Enrolment`` carries person and course and nothing else that could gate it. The service that
   creates one takes no company argument, so the rule cannot be bent by calling it differently.
2. A ``TrainingPlan`` is a RECOMMENDED path. Its items are suggestions; enrolling in a course listed
   in a plan and enrolling in a course found in the catalogue are the same operation, and a plan is
   never consulted to decide whether someone may enrol.
3. A completion is a FACT ABOUT ATTENDANCE — modules attended, hours, dates. It is never an
   administrative approval, never a qualification the State recognises, and the wording used for it
   (``attendance_reference``, "attestation de suivi") says so (REQ-EDU-05).
4. The skill gap is a STRUCTURED COMPARISON — required competence, current competence, gap, module,
   expected outcome — with ordinal levels that carry words. No percentage exists on these models,
   because a percentage of a competence is a number nobody can defend (REQ-EDU-07, RB §31).

Requirements: REQ-EDU-01..07, PLATFORM_REQUIREMENTS_V2 §10.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

# =================================================================================================
# Providers
# =================================================================================================


class ProviderKind(models.TextChoices):
    UNIVERSITY = "university", _("Université")
    TRAINING_BODY = "training_body", _("Organisme de formation")
    INSTITUTION = "institution", _("Institution")
    ASSOCIATION = "association", _("Association")
    PROJECT = "project", _("Équipe du projet")


class TrainingProvider(TimeStampedModel):
    """
    Who delivers the course, and is answerable for it.

    The provider is mandatory on every course for the same reason a checklist item must name a
    responsible actor: a training offer with no named body behind it is an anonymous promise, and
    this platform does not make those.
    """

    slug = models.SlugField(_("identifiant"), max_length=80, unique=True)
    name = models.CharField(_("dénomination"), max_length=200)
    kind = models.CharField(_("type"), max_length=20, choices=ProviderKind.choices)
    country = models.CharField(_("pays"), max_length=80, blank=True)
    city = models.CharField(_("ville"), max_length=120, blank=True)
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_offers",
        verbose_name=_("organisation"),
    )
    note = models.CharField(_("précision"), max_length=300, blank=True)
    is_active = models.BooleanField(_("actif"), default=True)

    class Meta:
        verbose_name = _("organisme de formation")
        verbose_name_plural = _("organismes de formation")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# =================================================================================================
# Courses
# =================================================================================================


class CourseType(models.TextChoices):
    """The seven families of the Master Dossier (D1 §4, D2 §3, RB §32). Nothing else is offered."""

    ITALIAN_LANGUAGE = "italian_language", _("Langue italienne")
    RIGHTS_AND_DUTIES = "rights_and_duties", _("Droits et devoirs")
    CIVIC_EDUCATION = "civic_education", _("Éducation civique")
    WORKPLACE_SAFETY = "workplace_safety", _("Sécurité au travail")
    WORK_CULTURE = "work_culture", _("Culture du travail")
    PROFESSIONAL_TRAINING = "professional_training", _("Formation professionnelle")
    PRE_DEPARTURE = "pre_departure", _("Préparation au départ")


class CourseFormat(models.TextChoices):
    ONLINE = "online", _("À distance")
    IN_PERSON = "in_person", _("En présentiel")
    BLENDED = "blended", _("Mixte")


class CourseStatus(models.TextChoices):
    DRAFT = "draft", _("Brouillon")
    PUBLISHED = "published", _("Publié")
    ARCHIVED = "archived", _("Archivé")


class CourseQuerySet(models.QuerySet):
    def visible_to(self, user) -> CourseQuerySet:
        """
        Authorisation applied AT QUERY TIME (deny by default).

        A published course is visible to EVERY authenticated account — that is the whole point of
        CR-14 and the reason there is no role test here beyond authentication. Drafts and archived
        courses are editorial states and stay with the back-office roles: a person must not discover
        an unpublished course through a count or a filter.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.STAFF, roles.ADMINISTRATOR):
            return self
        return self.filter(status=CourseStatus.PUBLISHED)

    def published(self) -> CourseQuerySet:
        return self.filter(status=CourseStatus.PUBLISHED)


class Course(TimeStampedModel):
    """One training course of the catalogue, in one language, at one version."""

    slug = models.SlugField(_("identifiant"), max_length=80, unique=True)
    title = models.CharField(_("intitulé"), max_length=200)
    summary = models.CharField(_("résumé"), max_length=300)
    description = models.TextField(_("description"), blank=True)
    course_type = models.CharField(_("domaine"), max_length=32, choices=CourseType.choices, db_index=True)
    provider = models.ForeignKey(
        TrainingProvider,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("organisme"),
    )
    language = models.CharField(
        _("langue d’enseignement"), max_length=8, choices=settings.LANGUAGES, default="it", db_index=True
    )
    text_language = models.CharField(
        _("langue du texte"),
        max_length=8,
        default="fr",
        editable=False,
        help_text=_("Langue dans laquelle l’intitulé et le résumé sont rédigés (attribut lang)."),
    )
    course_format = models.CharField(_("modalité"), max_length=16, choices=CourseFormat.choices)
    duration_hours = models.PositiveIntegerField(_("durée (heures)"))
    version = models.PositiveIntegerField(_("version"), default=1)
    status = models.CharField(_("état"), max_length=16, choices=CourseStatus.choices, default=CourseStatus.DRAFT)
    published_at = models.DateTimeField(_("publié le"), null=True, blank=True)
    access_note = models.CharField(
        _("condition d’accès"),
        max_length=300,
        blank=True,
        help_text=_("Prérequis pédagogique éventuel. Ne peut jamais porter sur une sélection par une entreprise."),
    )

    objects = CourseQuerySet.as_manager()

    class Meta:
        verbose_name = _("cours")
        verbose_name_plural = _("cours")
        ordering = ["course_type", "title"]
        indexes = [models.Index(fields=["status", "course_type"])]

    def __str__(self) -> str:
        return f"{self.title} (v{self.version})"

    @property
    def is_published(self) -> bool:
        return self.status == CourseStatus.PUBLISHED

    @property
    def module_count(self) -> int:
        return self.modules.count()


class ModuleKind(models.TextChoices):
    LESSON = "lesson", _("Séance")
    PRACTICE = "practice", _("Atelier pratique")
    READING = "reading", _("Lecture")
    REVIEW = "review", _("Révision")


class CourseModule(TimeStampedModel):
    """One step inside a course. Progression is counted in modules attended, never in per cent."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules", verbose_name=_("cours"))
    order = models.PositiveIntegerField(_("ordre"), default=0)
    title = models.CharField(_("intitulé"), max_length=200)
    summary = models.CharField(_("résumé"), max_length=300, blank=True)
    kind = models.CharField(_("type"), max_length=16, choices=ModuleKind.choices, default=ModuleKind.LESSON)
    duration_minutes = models.PositiveIntegerField(_("durée (minutes)"), default=60)

    class Meta:
        verbose_name = _("module")
        verbose_name_plural = _("modules")
        ordering = ["course", "order", "id"]
        constraints = [models.UniqueConstraint(fields=["course", "order"], name="academy_module_order_unique")]

    def __str__(self) -> str:
        return self.title


class MaterialKind(models.TextChoices):
    DOCUMENT = "document", _("Document")
    READING = "reading", _("Lecture")
    EXERCISE = "exercise", _("Exercice")
    RECORDING = "recording", _("Enregistrement")


class CourseMaterial(TimeStampedModel):
    """
    A teaching material, described and SOURCED — never an uploaded personal file.

    Materials name their origin (``source_title`` / ``source_ref``) so a learner can tell an
    institutional text from a document written by the training body. Files belonging to a person
    live in ``documents`` and never here.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials", verbose_name=_("cours"))
    module = models.ForeignKey(
        CourseModule,
        on_delete=models.CASCADE,
        related_name="materials",
        null=True,
        blank=True,
        verbose_name=_("module"),
    )
    order = models.PositiveIntegerField(_("ordre"), default=0)
    title = models.CharField(_("intitulé"), max_length=200)
    kind = models.CharField(_("type"), max_length=16, choices=MaterialKind.choices, default=MaterialKind.DOCUMENT)
    note = models.CharField(_("précision"), max_length=300, blank=True)
    source_title = models.CharField(_("source"), max_length=200, blank=True)
    source_ref = models.CharField(_("référence de la source"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("support de formation")
        verbose_name_plural = _("supports de formation")
        ordering = ["course", "order", "id"]

    def __str__(self) -> str:
        return self.title


# =================================================================================================
# Competences
# =================================================================================================


class CompetenceArea(models.TextChoices):
    LANGUAGE = "language", _("Langue")
    SAFETY = "safety", _("Sécurité")
    CIVIC = "civic", _("Vie civique")
    TECHNICAL = "technical", _("Technique")
    WORKPLACE = "workplace", _("Organisation du travail")


class CompetenceLevel(models.IntegerChoices):
    """
    Four ordered levels, each carrying a WORD.

    Ordinal integers exist so a gap can be computed; they are never shown as a number, a score or a
    meter. The interface prints the label, and the gap prints a word.
    """

    NONE = 0, _("Non acquise")
    BASIC = 1, _("Notions")
    INTERMEDIATE = 2, _("Autonomie partielle")
    ADVANCED = 3, _("Autonomie")


class Competence(TimeStampedModel):
    code = models.SlugField(_("code"), max_length=60, unique=True)
    label = models.CharField(_("compétence"), max_length=200)
    description = models.CharField(_("description"), max_length=300, blank=True)
    area = models.CharField(_("domaine"), max_length=20, choices=CompetenceArea.choices)

    class Meta:
        verbose_name = _("compétence")
        verbose_name_plural = _("compétences")
        ordering = ["area", "label"]

    def __str__(self) -> str:
        return self.label


class CourseCompetence(TimeStampedModel):
    """What a course lets a learner do afterwards — the “expected outcome” of the gap table."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="competences", verbose_name=_("cours"))
    competence = models.ForeignKey(
        Competence, on_delete=models.CASCADE, related_name="courses", verbose_name=_("compétence")
    )
    level_reached = models.IntegerField(
        _("niveau visé"), choices=CompetenceLevel.choices, default=CompetenceLevel.BASIC
    )
    expected_outcome = models.CharField(_("résultat attendu"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("compétence du cours")
        verbose_name_plural = _("compétences du cours")
        ordering = ["course", "competence__label"]
        constraints = [
            models.UniqueConstraint(fields=["course", "competence"], name="academy_course_competence_unique")
        ]

    def __str__(self) -> str:
        return f"{self.course.slug} · {self.competence.code}"


# =================================================================================================
# Training plans (a RECOMMENDED path — never a condition of access)
# =================================================================================================


class PlanOrigin(models.TextChoices):
    SELF = "self", _("Démarche personnelle")
    ORIENTATION = "orientation", _("Issu de l’orientation")
    COMPANY_NEED = "company_need", _("Issu d’un besoin exprimé par une entreprise")
    PROFESSIONAL = "professional", _("Proposé par un professionnel")


class PlanStatus(models.TextChoices):
    DRAFT = "draft", _("Brouillon")
    ACTIVE = "active", _("En cours")
    COMPLETED = "completed", _("Terminé")
    ARCHIVED = "archived", _("Archivé")


class TrainingPlanQuerySet(models.QuerySet):
    def readable_by(self, user) -> TrainingPlanQuerySet:
        """
        The person, plus anyone holding a LIVE assignment IN A TRAINING CAPACITY on the linked case.

        The validity of the mandate is checked in the query, exactly as ``CaseFileQuerySet`` does: a
        revoked or expired authorisation must stop listing a person's training plan the day it
        lapses, not the day someone notices.

        The CAPACITY is checked in the query too, for the same reason. ``academy.policies`` already
        refuses an assignment as *soggetto autorizzato* — their mandate concerns the phase reserved
        to them, not the person's training record (CR-03) — but a policy only guards an object
        already in hand. Without the role in the filter, an authorised actor's own "my trainings"
        page listed the title, the origin and the origin reference of a plan they may not open:
        deny by default means the row never enters the queryset, not that the detail view refuses
        it afterwards. The two lists are kept identical by a test.
        """
        from accounts import roles
        from cases.models import AssignmentRole

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        today = timezone.localdate()
        assigned = models.Q(
            case__assignments__assignee=user,
            case__assignments__revoked_at__isnull=True,
            case__assignments__role__in=[
                AssignmentRole.PROFESSIONAL,
                AssignmentRole.OPERATOR,
                AssignmentRole.TRAINING_BODY,
            ],
        ) & (
            models.Q(case__assignments__authorisation_valid_until__isnull=True)
            | models.Q(case__assignments__authorisation_valid_until__gte=today)
        )
        return self.filter(models.Q(person=user) | assigned).distinct()


class TrainingPlan(TimeStampedModel):
    """
    A person's recommended training path.

    It may come from a company's expressed need, from the orientation, from a professional, or from
    the person themselves — and the origin changes NOTHING about access: every course in the plan is
    a course of the open catalogue, enrolled in exactly the same way.

    ``origin_reference`` is deliberately a text reference rather than a foreign key to a company
    need: the plan must stay readable when the need it came from is corrected, withdrawn or
    archived, and a person's training record must never be destroyed by a cascade from a company
    object.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="training_plans",
        verbose_name=_("personne"),
    )
    title = models.CharField(_("intitulé"), max_length=200)
    origin = models.CharField(_("origine"), max_length=20, choices=PlanOrigin.choices, default=PlanOrigin.SELF)
    origin_reference = models.CharField(
        _("référence de l’origine"),
        max_length=200,
        blank=True,
        help_text=_("Obligatoire pour un besoin d’entreprise : la référence du besoin, jamais un nom de personne."),
    )
    case = models.ForeignKey(
        "cases.CaseFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_plans",
        verbose_name=_("dossier"),
    )
    status = models.CharField(_("état"), max_length=16, choices=PlanStatus.choices, default=PlanStatus.DRAFT)
    note = models.TextField(_("note"), blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("établi par"),
    )

    objects = TrainingPlanQuerySet.as_manager()

    class Meta:
        verbose_name = _("plan de formation")
        verbose_name_plural = _("plans de formation")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["person", "status"])]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        # Same reasoning as an authorisation reference on a case assignment: a plan that claims to
        # come from a company need without naming it is a claim, not a traceable origin (REQ-EDU-06).
        if self.origin == PlanOrigin.COMPANY_NEED and not self.origin_reference.strip():
            raise ValidationError(
                {"origin_reference": _("Un plan issu d’un besoin d’entreprise doit citer la référence du besoin.")}
            )


class TrainingPlanItem(TimeStampedModel):
    """One recommended course of a plan. A recommendation, never a condition."""

    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="items", verbose_name=_("plan"))
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="plan_items", verbose_name=_("cours"))
    order = models.PositiveIntegerField(_("ordre"), default=0)
    rationale = models.CharField(_("motif"), max_length=300, blank=True)
    expected_outcome = models.CharField(_("résultat attendu"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("cours recommandé")
        verbose_name_plural = _("cours recommandés")
        ordering = ["plan", "order", "id"]
        constraints = [models.UniqueConstraint(fields=["plan", "course"], name="academy_plan_course_unique")]

    def __str__(self) -> str:
        return f"{self.plan.title} · {self.course.title}"


class SkillGapLine(TimeStampedModel):
    """
    One line of the competence comparison: required · current · gap · module · expected outcome.

    The gap is DERIVED from the two levels and printed as a word. There is no percentage field here
    and there must never be one: a meter showing “62 % of the competence” is not a measurement, and
    the client forbade it (RB §31, REQ-EDU-07).
    """

    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="skill_gap", verbose_name=_("plan"))
    order = models.PositiveIntegerField(_("ordre"), default=0)
    competence = models.ForeignKey(
        Competence, on_delete=models.PROTECT, related_name="gap_lines", verbose_name=_("compétence")
    )
    required_level = models.IntegerField(_("niveau requis"), choices=CompetenceLevel.choices)
    current_level = models.IntegerField(
        _("niveau actuel"), choices=CompetenceLevel.choices, default=CompetenceLevel.NONE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gap_lines",
        verbose_name=_("cours"),
    )
    module = models.ForeignKey(
        CourseModule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gap_lines",
        verbose_name=_("module"),
    )
    expected_outcome = models.CharField(_("résultat attendu"), max_length=300, blank=True)
    source_note = models.CharField(
        _("origine de l’exigence"),
        max_length=200,
        blank=True,
        help_text=_("D’où vient le niveau requis : référentiel, besoin exprimé, texte réglementaire."),
    )

    class Meta:
        verbose_name = _("écart de compétence")
        verbose_name_plural = _("écarts de compétence")
        ordering = ["plan", "order", "id"]

    def __str__(self) -> str:
        return f"{self.competence.label} · {self.gap_key}"

    @property
    def gap_key(self) -> str:
        if self.current_level >= self.required_level:
            return "covered"
        if self.current_level <= CompetenceLevel.NONE:
            return "missing"
        return "partial"

    @property
    def gap_label(self) -> str:
        return {
            "covered": _("Aucun écart"),
            "partial": _("Écart partiel"),
            "missing": _("Compétence à acquérir"),
        }[self.gap_key]

    def clean(self) -> None:
        if self.module_id and self.course_id and self.module.course_id != self.course_id:
            raise ValidationError({"module": _("Le module choisi n’appartient pas au cours indiqué.")})


# =================================================================================================
# Enrolment and attendance
# =================================================================================================


class EnrolmentStatus(models.TextChoices):
    """
    Four states, none of which is an approval.

    ``COMPLETED`` means “followed to the end” — an attendance fact. It is never “approved”,
    “validated”, “qualified” or “recognised by the State”, because the Academy attests presence and
    nothing else (REQ-EDU-05).
    """

    ENROLLED = "enrolled", _("Inscription enregistrée")
    IN_PROGRESS = "in_progress", _("Suivi en cours")
    COMPLETED = "completed", _("Suivi jusqu’au terme")
    WITHDRAWN = "withdrawn", _("Interrompu")


class EnrolmentOrigin(models.TextChoices):
    CATALOGUE = "catalogue", _("Catalogue")
    PLAN = "plan", _("Plan de formation")


class EnrolmentQuerySet(models.QuerySet):
    def readable_by(self, user) -> EnrolmentQuerySet:
        """
        A person's own enrolments, and nothing else.

        Deliberately stricter than the course catalogue: what someone is learning is personal data,
        and a training record is exactly the kind of list that gets quietly reused to sort people.
        Supervision happens in the back-office, where every access is role-checked and audited —
        the same reasoning ``CaseFileQuerySet`` applies to ``role:staff``.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        return self.filter(person=user)

    def ongoing(self) -> EnrolmentQuerySet:
        return self.filter(status__in=[EnrolmentStatus.ENROLLED, EnrolmentStatus.IN_PROGRESS])


class Enrolment(TimeStampedModel):
    """
    One person following one course.

    Note what is NOT here: no company, no selection, no eligibility, no approval, no grade, no
    score. The model cannot express “allowed to enrol because an employer chose this person”,
    which is the point.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrolments",
        verbose_name=_("personne"),
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="enrolments", verbose_name=_("cours"))
    status = models.CharField(
        _("état"), max_length=16, choices=EnrolmentStatus.choices, default=EnrolmentStatus.ENROLLED, db_index=True
    )
    origin = models.CharField(
        _("origine de l’inscription"),
        max_length=16,
        choices=EnrolmentOrigin.choices,
        default=EnrolmentOrigin.CATALOGUE,
    )
    plan = models.ForeignKey(
        TrainingPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrolments",
        verbose_name=_("plan de formation"),
    )
    enrolled_at = models.DateTimeField(_("inscrit le"), default=timezone.now, editable=False)
    started_at = models.DateTimeField(_("commencé le"), null=True, blank=True, editable=False)
    completed_at = models.DateTimeField(_("terminé le"), null=True, blank=True, editable=False)
    withdrawn_at = models.DateTimeField(_("interrompu le"), null=True, blank=True, editable=False)
    attendance_reference = models.CharField(
        _("référence de l’attestation de suivi"),
        max_length=16,
        blank=True,
        editable=False,
        help_text=_("Référence d’une attestation de SUIVI. Ce n’est ni un titre reconnu ni une décision."),
    )
    course_version = models.PositiveIntegerField(
        _("version du cours suivie"),
        default=1,
        editable=False,
        help_text=_("Version du cours au moment de l’inscription : l’attestation doit rester lisible plus tard."),
    )

    objects = EnrolmentQuerySet.as_manager()

    class Meta:
        verbose_name = _("inscription")
        verbose_name_plural = _("inscriptions")
        ordering = ["-enrolled_at"]
        constraints = [models.UniqueConstraint(fields=["person", "course"], name="academy_enrolment_unique")]
        indexes = [models.Index(fields=["person", "status"])]

    def __str__(self) -> str:
        return f"{self.course.title} · {self.get_status_display()}"

    @property
    def is_open(self) -> bool:
        return self.status in {EnrolmentStatus.ENROLLED, EnrolmentStatus.IN_PROGRESS}

    @property
    def is_completed(self) -> bool:
        return self.status == EnrolmentStatus.COMPLETED

    @property
    def attended_module_ids(self) -> set[int]:
        return set(self.attendances.values_list("module_id", flat=True))

    @property
    def attended_minutes(self) -> int:
        total = self.attendances.aggregate(total=models.Sum("module__duration_minutes"))["total"]
        return int(total or 0)


class ModuleAttendance(TimeStampedModel):
    """
    A module was attended, on a date. One fact, recorded once.

    No mark, no score, no pass/fail: the Academy records presence. Anything stronger would be a
    judgement about a person that this platform has no standing to make.
    """

    enrolment = models.ForeignKey(
        Enrolment, on_delete=models.CASCADE, related_name="attendances", verbose_name=_("inscription")
    )
    module = models.ForeignKey(
        CourseModule, on_delete=models.CASCADE, related_name="attendances", verbose_name=_("module")
    )
    attended_at = models.DateTimeField(_("suivi le"), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("module suivi")
        verbose_name_plural = _("modules suivis")
        ordering = ["enrolment", "module__order"]
        constraints = [models.UniqueConstraint(fields=["enrolment", "module"], name="academy_attendance_unique")]

    def __str__(self) -> str:
        return f"{self.enrolment_id} · {self.module.title}"

    def clean(self) -> None:
        if self.module.course_id != self.enrolment.course_id:
            raise ValidationError({"module": _("Ce module n’appartient pas au cours suivi.")})
