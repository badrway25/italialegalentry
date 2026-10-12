"""
Back-office of the Academy.

Two halves, with two different rules.

THE CATALOGUE is editorial and is edited here: providers, courses, modules, materials, competences.
That is administration of an offer, not of a person.

A TRAINING RECORD is not editorial. ``Enrolment`` and ``ModuleAttendance`` are read-only in the
admin: an attendance fact that an administrator can write by hand is not a fact, and a completion
that can be granted from a form is exactly the "administrative approval" REQ-EDU-05 forbids. A
completion is produced by attending the modules, through ``academy.services``, which audits it.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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


class ModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0
    fields = ("order", "title", "kind", "duration_minutes", "summary")
    ordering = ("order", "id")


class MaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 0
    fields = ("order", "title", "kind", "module", "source_title", "source_ref")
    ordering = ("order", "id")


class CourseCompetenceInline(admin.TabularInline):
    model = CourseCompetence
    extra = 0
    fields = ("competence", "level_reached", "expected_outcome")


@admin.register(TrainingProvider)
class TrainingProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "city", "country", "is_active")
    list_filter = ("kind", "is_active")
    search_fields = ("name", "slug", "city")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "course_type", "provider", "language", "duration_hours", "version", "status")
    list_filter = ("status", "course_type", "language", "course_format", "provider")
    search_fields = ("title", "slug", "summary")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ModuleInline, MaterialInline, CourseCompetenceInline)
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description")}),
        (_("Offre"), {"fields": ("course_type", "provider", "language", "course_format", "duration_hours")}),
        (
            _("Publication"),
            {
                "fields": ("status", "version", "published_at", "access_note"),
                "description": _(
                    "« Condition d’accès » désigne un prérequis pédagogique. L’accès à l’Academy ne peut "
                    "jamais être subordonné à une sélection par une entreprise."
                ),
            },
        ),
    )


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("label", "code", "area")
    list_filter = ("area",)
    search_fields = ("label", "code")
    prepopulated_fields = {"code": ("label",)}


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    """Read-only supervision. Nothing here can create a completion (REQ-EDU-05)."""

    list_display = ("course", "status", "enrolled_at", "completed_at")
    list_filter = ("status", "course__course_type", "course")
    search_fields = ("attendance_reference", "course__title")
    date_hierarchy = "enrolled_at"
    readonly_fields = (
        "person",
        "course",
        "status",
        "origin",
        "plan",
        "enrolled_at",
        "started_at",
        "completed_at",
        "withdrawn_at",
        "attendance_reference",
        "course_version",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ModuleAttendance)
class ModuleAttendanceAdmin(admin.ModelAdmin):
    list_display = ("enrolment", "module", "attended_at")
    readonly_fields = ("enrolment", "module", "attended_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PlanItemInline(admin.TabularInline):
    model = TrainingPlanItem
    extra = 0
    fields = ("order", "course", "rationale", "expected_outcome")


class SkillGapInline(admin.TabularInline):
    model = SkillGapLine
    extra = 0
    fields = ("order", "competence", "required_level", "current_level", "course", "module", "expected_outcome")


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "origin", "status", "created_at")
    list_filter = ("status", "origin")
    search_fields = ("title", "origin_reference")
    inlines = (PlanItemInline, SkillGapInline)
    autocomplete_fields = ("person",)
    readonly_fields = ("uuid",)
