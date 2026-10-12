"""
Object-level policies of the Academy (deny by default — ``accounts.permissions``).

The querysets (``CourseQuerySet.visible_to``, ``EnrolmentQuerySet.readable_by``,
``TrainingPlanQuerySet.readable_by``) are the primary defence: they keep rows a user may not see
out of lists, counts and filters, so nobody learns that an object exists. These policies are the
second defence, for one object already in hand.

The asymmetry between the two halves of this module is deliberate and is the whole design:

* THE CATALOGUE IS OPEN. Any authenticated account may view any published course, its modules, its
  materials and the competences it develops. No role, no case file, no company, no selection is
  consulted — CR-14 and REQ-EDU-04 are satisfied by the ABSENCE of a condition, and a test proves
  a plain person with no case, no plan and no company can enrol.
* A TRAINING RECORD IS PRIVATE. What a person is learning is personal data. Only the person
  themselves reads their enrolments; supervision goes through the back-office, which is
  role-checked and audited. Not even ``role:staff`` gets a platform-side list, for the same reason
  ``CaseFileQuerySet`` refuses it: a standing list of everyone's training is a disclosure, not
  supervision.

A training plan is the one object with a second legitimate reader: a professional or operator
holding a LIVE assignment on the linked case file. Liveness is checked (``is_live``), never the
mere existence of the assignment row, so a lapsed mandate stops reading the day it lapses.
"""

from __future__ import annotations

from academy.models import (
    Competence,
    Course,
    CourseCompetence,
    CourseMaterial,
    CourseModule,
    Enrolment,
    ModuleAttendance,
    SkillGapLine,
    TrainingPlan,
    TrainingPlanItem,
    TrainingProvider,
)
from accounts import roles
from accounts.permissions import can, member_of, policy
from cases.models import AssignmentRole

#: Roles that may read an unpublished course in the back-office.
CATALOGUE_VIEW_ROLES = (roles.STAFF, roles.ADMINISTRATOR)
#: Roles that may change the catalogue anywhere.
CATALOGUE_MANAGE_ROLES = (roles.ADMINISTRATOR,)
#: Assignment roles on a case file that may work on the person's training plan. An authorised actor
#: is NOT here: their mandate concerns the phase reserved to them, not the person's training record.
PLAN_ASSIGNEE_ROLES = frozenset({AssignmentRole.PROFESSIONAL, AssignmentRole.OPERATOR, AssignmentRole.TRAINING_BODY})


def _training_body_of(user, provider: TrainingProvider | None) -> bool:
    """True when ``user`` belongs to the organisation that delivers this course."""
    if provider is None or not roles.has_role(user, roles.TRAINING_PROVIDER):
        return False
    return member_of(user, provider.organisation_id)


@policy(TrainingProvider)
def provider_policy(user, action: str, obj: TrainingProvider) -> bool:
    if action == "view":
        # A learner must always be able to name the body answerable for a course.
        return True
    if action in {"change", "add", "delete"}:
        return roles.has_role(user, *CATALOGUE_MANAGE_ROLES)
    return False


@policy(Course)
def course_policy(user, action: str, obj: Course) -> bool:
    if action == "view":
        if obj.is_published:
            return True  # CR-14: open to every authenticated account, with no further condition.
        return roles.has_role(user, *CATALOGUE_VIEW_ROLES)
    if action == "enrol":
        # Enrolment is a view-level right, not an administrative one: if you can see the course and
        # it is published, you may enrol in it. The service repeats the published check.
        return obj.is_published
    if action in {"change", "delete"}:
        return roles.has_role(user, *CATALOGUE_MANAGE_ROLES) or _training_body_of(user, obj.provider)
    return False


def _follows_course(user, action: str, course: Course) -> bool:
    return can(user, "view", course) if action == "view" else can(user, "change", course)


@policy(CourseModule)
def module_policy(user, action: str, obj: CourseModule) -> bool:
    return _follows_course(user, action, obj.course)


@policy(CourseMaterial)
def material_policy(user, action: str, obj: CourseMaterial) -> bool:
    return _follows_course(user, action, obj.course)


@policy(CourseCompetence)
def course_competence_policy(user, action: str, obj: CourseCompetence) -> bool:
    return _follows_course(user, action, obj.course)


@policy(Competence)
def competence_policy(user, action: str, obj: Competence) -> bool:
    if action == "view":
        return True
    return roles.has_role(user, *CATALOGUE_MANAGE_ROLES)


@policy(Enrolment)
def enrolment_policy(user, action: str, obj: Enrolment) -> bool:
    if obj.person_id == user.id:
        # The person records their own attendance and may interrupt at any time. They may NOT
        # delete the record: an attendance fact is evidence, and evidence that the subject can
        # erase is not evidence. Account deletion is handled by the accounts app, globally.
        return action in {"view", "change"}
    if action == "view":
        return roles.has_role(user, roles.ADMINISTRATOR)
    return False


@policy(ModuleAttendance)
def attendance_policy(user, action: str, obj: ModuleAttendance) -> bool:
    if action == "view":
        return can(user, "view", obj.enrolment)
    return False  # An attendance fact is written once, by the service, and never edited.


def _live_plan_assignment(user, plan: TrainingPlan) -> bool:
    case = plan.case
    if case is None:
        return False
    return any(
        row.assignee_id == user.id and row.is_live and row.role in PLAN_ASSIGNEE_ROLES for row in case.assignments.all()
    )


@policy(TrainingPlan)
def plan_policy(user, action: str, obj: TrainingPlan) -> bool:
    if obj.person_id == user.id:
        return action in {"view", "change"}
    if _live_plan_assignment(user, obj):
        return action in {"view", "change"}
    if action == "view":
        return roles.has_role(user, roles.ADMINISTRATOR)
    if action in {"change", "add", "delete"}:
        return roles.has_role(user, roles.ADMINISTRATOR)
    return False


@policy(TrainingPlanItem)
def plan_item_policy(user, action: str, obj: TrainingPlanItem) -> bool:
    return can(user, "view", obj.plan) if action == "view" else can(user, "change", obj.plan)


@policy(SkillGapLine)
def skill_gap_policy(user, action: str, obj: SkillGapLine) -> bool:
    return can(user, "view", obj.plan) if action == "view" else can(user, "change", obj.plan)
