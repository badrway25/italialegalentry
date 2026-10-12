"""
Domain services of the Academy.

Every state change goes through this module — the views, the admin, the seeds and any future API
call the same functions — so the two invariants that matter cannot be bypassed by choosing another
entry point:

1. **Enrolling is unconditional.** ``enrol()`` takes a person and a course. It has no company
   parameter, no selection parameter and no case-file parameter, and it consults none of those
   objects. The only checks are: the course is published, and the person is authenticated. That is
   the client's acceptance criterion (Technical Blueprint §17, CR-14) expressed as a signature.
2. **A completion is an attendance fact.** It is produced by attending every module of the course,
   it records what was attended and when, and it is labelled as a record of attendance. No function
   here approves, validates, certifies or qualifies anybody (REQ-EDU-05).

Progress is counted, never measured: ``progress()`` returns "3 modules of 7", which anyone can
verify, instead of a percentage, which nobody can.
"""

from __future__ import annotations

import uuid

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from academy.models import (
    Competence,
    CompetenceLevel,
    Course,
    CourseModule,
    CourseType,
    Enrolment,
    EnrolmentOrigin,
    EnrolmentStatus,
    ModuleAttendance,
    PlanOrigin,
    PlanStatus,
    SkillGapLine,
    TrainingPlan,
    TrainingPlanItem,
)
from accounts.permissions import can, require
from audit.services import record


class EnrolmentRefused(ValidationError):
    """The domain refuses this enrolment. Never downgraded to a silent no-op."""


# =================================================================================================
# Catalogue (reading)
# =================================================================================================
def catalogue(user, *, course_type: str = "", language: str = "", search: str = ""):
    """
    The courses ``user`` may see, filtered. Authorisation is applied in the queryset.

    Filters are validated against the declared choices rather than passed through: an unknown
    ``?domaine=`` value is ignored, so a crafted query string can neither widen the result set nor
    raise a 500 that tells the caller something about the schema.
    """
    rows = Course.objects.visible_to(user).select_related("provider")
    if course_type in CourseType.values:
        rows = rows.filter(course_type=course_type)
    if language:
        rows = rows.filter(language=language)
    search = (search or "").strip()
    if search:
        rows = rows.filter(Q(title__icontains=search) | Q(summary__icontains=search))
    return rows.annotate(modules_count=Count("modules", distinct=True)).order_by("course_type", "title")


def catalogue_domains(user) -> list[dict]:
    """The seven domains with the number of visible courses in each — catalogue data, not personal."""
    counts = dict(
        Course.objects.visible_to(user)
        .values_list("course_type")
        .annotate(n=Count("id"))
        .values_list("course_type", "n")
    )
    return [
        {"key": value, "label": label, "count": counts.get(value, 0)}
        for value, label in CourseType.choices
        if counts.get(value, 0)
    ]


def course_for(user, slug: str) -> Course:
    """One course the user may read, or PermissionDenied — indistinguishable from "absent"."""
    course = (
        Course.objects.visible_to(user)
        .select_related("provider")
        .prefetch_related(
            Prefetch("modules", queryset=CourseModule.objects.order_by("order", "id")),
            "materials",
            "competences__competence",
        )
        .filter(slug=slug)
        .first()
    )
    if course is None:
        raise PermissionDenied
    return course


def enrolment_for(user, uuid_value) -> Enrolment:
    enrolment = (
        Enrolment.objects.readable_by(user)
        .select_related("course", "course__provider", "plan")
        .filter(uuid=uuid_value)
        .first()
    )
    if enrolment is None:
        raise PermissionDenied
    return enrolment


def enrolments_for(user):
    return (
        Enrolment.objects.readable_by(user)
        .select_related("course", "course__provider")
        .annotate(
            modules_total=Count("course__modules", distinct=True),
            modules_attended=Count("attendances", distinct=True),
        )
        .order_by("-enrolled_at")
    )


def enrolment_of(person, course: Course) -> Enrolment | None:
    return Enrolment.objects.filter(person=person, course=course).first()


# =================================================================================================
# Enrolment
# =================================================================================================
@transaction.atomic
def enrol(person, course: Course, *, plan: TrainingPlan | None = None, request=None) -> Enrolment:
    """
    Enrol ``person`` in ``course``.

    Read the signature: a person and a course. Nothing about a company, a selection, an employer or
    a case file is asked for, so nothing of the sort can be required. A plan may be named, and it
    changes only where the enrolment came FROM — never whether it is allowed.
    """
    if not getattr(person, "is_authenticated", False):
        raise PermissionDenied
    if not course.is_published:
        raise EnrolmentRefused(_("Ce cours n’est pas ouvert aux inscriptions."))
    if plan is not None and plan.person_id != person.id:
        # A plan belonging to someone else must not be attached — it would leak that it exists.
        raise PermissionDenied

    existing = Enrolment.objects.filter(person=person, course=course).first()
    if existing is not None:
        if existing.status == EnrolmentStatus.WITHDRAWN:
            return resume(existing, request=request)
        return existing

    enrolment = Enrolment.objects.create(
        person=person,
        course=course,
        plan=plan,
        origin=EnrolmentOrigin.PLAN if plan is not None else EnrolmentOrigin.CATALOGUE,
        course_version=course.version,
        status=EnrolmentStatus.ENROLLED,
    )
    record(
        request,
        actor=person,
        action="academy.enrolled",
        target=enrolment,
        metadata={"course": course.slug, "version": course.version, "origin": enrolment.origin},
    )
    return enrolment


@transaction.atomic
def resume(enrolment: Enrolment, *, request=None) -> Enrolment:
    """Restart a training that was interrupted. Attendance already recorded is kept."""
    if enrolment.status != EnrolmentStatus.WITHDRAWN:
        return enrolment
    enrolment.status = EnrolmentStatus.IN_PROGRESS if enrolment.attendances.exists() else EnrolmentStatus.ENROLLED
    enrolment.withdrawn_at = None
    enrolment.save(update_fields=["status", "withdrawn_at", "updated_at"])
    record(
        request,
        actor=enrolment.person,
        action="academy.resumed",
        target=enrolment,
        metadata={"course": enrolment.course.slug},
    )
    return enrolment


@transaction.atomic
def withdraw(enrolment: Enrolment, *, actor=None, request=None) -> Enrolment:
    """Interrupt a training. Never a sanction, never blocking: it can be resumed."""
    if enrolment.status == EnrolmentStatus.COMPLETED:
        raise EnrolmentRefused(_("Un parcours déjà suivi jusqu’au terme ne peut pas être interrompu."))
    enrolment.status = EnrolmentStatus.WITHDRAWN
    enrolment.withdrawn_at = timezone.now()
    enrolment.save(update_fields=["status", "withdrawn_at", "updated_at"])
    record(
        request,
        actor=actor or enrolment.person,
        action="academy.withdrawn",
        target=enrolment,
        metadata={"course": enrolment.course.slug},
    )
    return enrolment


@transaction.atomic
def record_attendance(enrolment: Enrolment, module: CourseModule, *, actor=None, request=None) -> ModuleAttendance:
    """
    Record that ``module`` was attended. Idempotent: attending twice is still one fact.

    When every module of the course has been attended, the enrolment completes on its own. The
    completion is therefore derived from the facts and never asserted by an administrator.
    """
    if module.course_id != enrolment.course_id:
        raise ValidationError({"module": _("Ce module n’appartient pas au cours suivi.")})
    if enrolment.status == EnrolmentStatus.COMPLETED:
        return enrolment.attendances.get(module=module)
    if enrolment.status == EnrolmentStatus.WITHDRAWN:
        resume(enrolment, request=request)

    attendance, created = ModuleAttendance.objects.get_or_create(enrolment=enrolment, module=module)
    if created:
        record(
            request,
            actor=actor or enrolment.person,
            action="academy.module.attended",
            target=enrolment,
            metadata={"course": enrolment.course.slug, "module": module.pk, "order": module.order},
        )
    if enrolment.status == EnrolmentStatus.ENROLLED:
        enrolment.status = EnrolmentStatus.IN_PROGRESS
        enrolment.started_at = enrolment.started_at or timezone.now()
        enrolment.save(update_fields=["status", "started_at", "updated_at"])

    counts = progress(enrolment)
    if counts["total"] and counts["attended"] >= counts["total"]:
        _complete(enrolment, actor=actor, request=request)
    return attendance


def _complete(enrolment: Enrolment, *, actor=None, request=None) -> Enrolment:
    """
    Close the enrolment as attended to the end.

    What is recorded is presence: the date, the modules, the hours. The reference produced is the
    reference of an ATTENDANCE record — not a diploma, not a licence, not a decision by anybody.
    """
    enrolment.status = EnrolmentStatus.COMPLETED
    enrolment.completed_at = timezone.now()
    enrolment.attendance_reference = enrolment.attendance_reference or _new_attendance_reference()
    enrolment.save(update_fields=["status", "completed_at", "attendance_reference", "updated_at"])
    record(
        request,
        actor=actor or enrolment.person,
        action="academy.completed",
        target=enrolment,
        metadata={
            "course": enrolment.course.slug,
            "version": enrolment.course_version,
            "minutes": enrolment.attended_minutes,
        },
    )
    return enrolment


def _new_attendance_reference() -> str:
    """Non-sequential: a sequential reference would leak how many people attended."""
    for _attempt in range(12):
        proposed = uuid.uuid4().hex[:10].upper()
        if not Enrolment.objects.filter(attendance_reference=proposed).exists():
            return proposed
    raise RuntimeError("could not allocate a unique attendance reference")


def progress(enrolment: Enrolment) -> dict:
    """
    Honest progress: counts, never a percentage.

    "3 modules of 7 attended" is verifiable against the attendance rows. A meter is not, and the
    client forbade meaningless meters (RB §31).
    """
    total = enrolment.course.modules.count()
    attended = enrolment.attendances.count()
    return {
        "total": total,
        "attended": attended,
        "remaining": max(total - attended, 0),
        "minutes": enrolment.attended_minutes,
    }


def module_rows(enrolment: Enrolment) -> list[dict]:
    """The course's modules with, for each, whether it has been attended and when."""
    attended = {row.module_id: row.attended_at for row in enrolment.attendances.all()}
    rows = []
    for module in enrolment.course.modules.all():
        rows.append(
            {
                "module": module,
                "attended": module.pk in attended,
                "attended_at": attended.get(module.pk),
            }
        )
    return rows


def next_module(enrolment: Enrolment) -> CourseModule | None:
    """The first module not yet attended — the single next action inside a course."""
    attended = enrolment.attended_module_ids
    for module in enrolment.course.modules.all():
        if module.pk not in attended:
            return module
    return None


# =================================================================================================
# Training plans
# =================================================================================================
@transaction.atomic
def create_plan(
    person,
    *,
    title: str,
    origin: str = PlanOrigin.SELF,
    origin_reference: str = "",
    case=None,
    note: str = "",
    created_by=None,
    status: str = PlanStatus.ACTIVE,
    request=None,
) -> TrainingPlan:
    plan = TrainingPlan(
        person=person,
        title=title,
        origin=origin,
        origin_reference=origin_reference,
        case=case,
        note=note,
        created_by=created_by,
        status=status,
    )
    plan.full_clean(exclude=["uuid"])
    plan.save()
    record(
        request,
        actor=created_by or person,
        action="academy.plan.created",
        target=plan,
        metadata={"origin": origin, "case": getattr(case, "reference", "")},
    )
    return plan


@transaction.atomic
def add_plan_item(
    plan: TrainingPlan,
    course: Course,
    *,
    rationale: str = "",
    expected_outcome: str = "",
    order: int | None = None,
    actor=None,
    request=None,
) -> TrainingPlanItem:
    """
    Recommend a course inside a plan.

    Audited, like every other change to a person's record: a plan is usually composed by somebody
    else — a professional, an operator, the administration — and "who added this course to my
    training path, and when" is a question the person is entitled to have answered. Only the plan
    and the course SLUG go into the metadata; no name and no e-mail address.
    """
    item, created = TrainingPlanItem.objects.get_or_create(
        plan=plan,
        course=course,
        defaults={
            "rationale": rationale,
            "expected_outcome": expected_outcome,
            "order": order if order is not None else plan.items.count(),
        },
    )
    if created:
        record(
            request,
            actor=actor or plan.created_by or plan.person,
            action="academy.plan.course_added",
            target=plan,
            metadata={"course": course.slug, "origin": plan.origin},
        )
    return item


@transaction.atomic
def add_gap_line(
    plan: TrainingPlan,
    competence: Competence,
    *,
    required_level: int,
    current_level: int = CompetenceLevel.NONE,
    course: Course | None = None,
    module: CourseModule | None = None,
    expected_outcome: str = "",
    source_note: str = "",
    order: int | None = None,
    actor=None,
    request=None,
) -> SkillGapLine:
    """
    Add one line of the competence comparison.

    Audited for the same reason as ``add_plan_item``: a statement about what a named person can
    and cannot do today is written by somebody, and the person may contest it. The metadata carries
    the competence CODE and the two level keys — never a sentence about the person.
    """
    line = SkillGapLine(
        plan=plan,
        competence=competence,
        required_level=required_level,
        current_level=current_level,
        course=course,
        module=module,
        expected_outcome=expected_outcome,
        source_note=source_note,
        order=order if order is not None else plan.skill_gap.count(),
    )
    line.full_clean()
    line.save()
    record(
        request,
        actor=actor or plan.created_by or plan.person,
        action="academy.plan.gap_line_added",
        target=plan,
        metadata={
            "competence": competence.code,
            "required_level": int(required_level),
            "current_level": int(current_level),
            "gap": line.gap_key,
        },
    )
    return line


def plans_for(user):
    return (
        TrainingPlan.objects.readable_by(user)
        .select_related("case")
        .annotate(item_count=Count("items", distinct=True))
        .order_by("-created_at")
    )


def plan_for(user, uuid_value) -> TrainingPlan:
    plan = (
        TrainingPlan.objects.readable_by(user)
        .select_related("case", "person")
        .prefetch_related(
            "items__course__provider",
            "skill_gap__competence",
            "skill_gap__course",
            "skill_gap__module",
        )
        .filter(uuid=uuid_value)
        .first()
    )
    if plan is None:
        raise PermissionDenied
    return plan


def plan_rows(plan: TrainingPlan, *, viewer=None) -> list[dict]:
    """
    The skill-gap table: required · current · gap · module · expected outcome.

    One row per competence, each carrying a WORD for the gap. Deliberately not a score, not a
    ranking and not a meter (REQ-EDU-07).
    """
    rows = []
    for line in plan.skill_gap.all():
        rows.append(
            {
                "competence": line.competence,
                "required": line.get_required_level_display(),
                "current": line.get_current_level_display(),
                "gap_key": line.gap_key,
                "gap": line.gap_label,
                "course": line.course,
                "module": line.module,
                "expected_outcome": line.expected_outcome,
                "source_note": line.source_note,
            }
        )
    return rows


def plan_item_rows(plan: TrainingPlan, viewer) -> list[dict]:
    """
    Plan items with the viewer's OWN enrolment state, if the viewer is the person concerned.

    A professional reading the plan of someone they are assigned to sees the recommended courses,
    not a live report of that person's attendance: the plan is a path, the attendance record is
    personal and stays with the enrolment.
    """
    own = viewer is not None and viewer.id == plan.person_id
    enrolled = {}
    if own:
        course_ids = [item.course_id for item in plan.items.all()]
        enrolled = {row.course_id: row for row in Enrolment.objects.filter(person=viewer, course_id__in=course_ids)}
    rows = []
    for item in plan.items.all():
        rows.append(
            {
                "item": item,
                "course": item.course,
                "enrolment": enrolled.get(item.course_id) if own else None,
                "own": own,
            }
        )
    return rows


# =================================================================================================
# Summary for the platform shell
# =================================================================================================
def summary(user) -> dict:
    """Counts for the Academy region of the platform: open trainings, attended, plans."""
    rows = list(Enrolment.objects.readable_by(user).filter(person=user))
    return {
        "ongoing": len([row for row in rows if row.is_open]),
        "completed": len([row for row in rows if row.is_completed]),
        "plans": TrainingPlan.objects.readable_by(user).filter(person=user).exclude(status=PlanStatus.ARCHIVED).count(),
    }


def require_can(user, action: str, obj) -> None:
    """Thin passthrough so views never import the permission registry directly."""
    require(user, action, obj)


def may(user, action: str, obj) -> bool:
    return can(user, action, obj)
