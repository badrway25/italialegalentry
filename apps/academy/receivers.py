"""
What the Academy owes the accounts domain: an export section, and an answer to anonymisation.

An enrolment is personal data — it says what a named person is learning and when they attended.
Two consequences the app has to honour itself, because ``accounts`` cannot know about it:

* **Right of access (GDPR art. 15).** The personal-data export must contain the training record, or
  the export is incomplete and the answer given to the person is false. ``academy`` registers its
  own section through ``accounts.services.register_export_section``.
* **Erasure / anonymisation (art. 17).** When an account is anonymised, the enrolments and the
  attendance rows go with it. Deleting rather than scrubbing is the right answer here: unlike an
  audit event, a training record has no legal retention duty of its own, and what would be left
  after scrubbing — "somebody attended three modules" — serves nobody.

Both are wired from ``AcademyConfig.ready`` by CALLING the accounts API. No file outside this app
is edited to make it work.
"""

from __future__ import annotations

from academy.models import Enrolment, TrainingPlan


def academy_export_section(user) -> dict:
    """The person's training record, as it is actually stored (art. 15 — no summarising)."""
    return {
        "enrolments": [
            {
                "course": row.course.title,
                "course_reference": row.course.slug,
                "course_version_followed": row.course_version,
                "provider": row.course.provider.name,
                "status": row.get_status_display(),
                "origin": row.get_origin_display(),
                "enrolled_at": row.enrolled_at,
                "started_at": row.started_at,
                "completed_at": row.completed_at,
                "withdrawn_at": row.withdrawn_at,
                "attendance_reference": row.attendance_reference,
                "modules_attended": [
                    {"module": attendance.module.title, "attended_at": attendance.attended_at}
                    for attendance in row.attendances.select_related("module").order_by("module__order")
                ],
            }
            for row in Enrolment.objects.filter(person=user)
            .select_related("course", "course__provider")
            .order_by("-enrolled_at")
        ],
        "training_plans": [
            {
                "title": plan.title,
                "origin": plan.get_origin_display(),
                "origin_reference": plan.origin_reference,
                "status": plan.get_status_display(),
                "created_at": plan.created_at,
                "recommended_courses": [item.course.title for item in plan.items.select_related("course")],
                "competence_comparison": [
                    {
                        "competence": line.competence.label,
                        "required_level": line.get_required_level_display(),
                        "current_level": line.get_current_level_display(),
                        "gap": str(line.gap_label),
                        "expected_outcome": line.expected_outcome,
                    }
                    for line in plan.skill_gap.select_related("competence")
                ],
            }
            for plan in TrainingPlan.objects.filter(person=user).order_by("-created_at")
        ],
    }


def on_user_anonymised(sender, *, user_id, **kwargs):
    """Erase the training record of an anonymised account. Idempotent, and never re-creates data."""
    # Attendance rows cascade from the enrolment; plan items and gap lines cascade from the plan.
    Enrolment.objects.filter(person_id=user_id).delete()
    TrainingPlan.objects.filter(person_id=user_id).delete()
