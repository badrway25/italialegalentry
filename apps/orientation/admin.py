"""
Back-office for the rule engine. Rulesets are versioned; activation goes through a validated
action (never by editing the status field). Results are read-only; the only export is an
anonymised statistics CSV (no answers, no identifiers).
"""

from __future__ import annotations

import json

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.admin_base import BaseModelAdmin, BaseStackedInline, BaseTabularInline
from orientation import engine, services
from orientation.models import (
    ChecklistItem,
    ChecklistItemTranslation,
    Choice,
    ChoiceTranslation,
    OrientationResult,
    OrientationSession,
    Outcome,
    OutcomeTranslation,
    Question,
    QuestionTranslation,
    Rule,
    Ruleset,
    RulesetStatus,
)

PENDING_NOTE = _(
    "CONTENT_PENDING_LEGAL_REVIEW — les textes de ce module sont des textes d'équipe à caractère informatif. "
    "Ils ne doivent contenir ni critère légal, ni promesse de résultat ; toute mention juridique doit être "
    "validée par la revue légale avant activation du ruleset."
)


# --------------------------------------------------------------------------------------------
# Forms
# --------------------------------------------------------------------------------------------
class PrettyJSONWidget(forms.Textarea):
    def format_value(self, value):
        if value in (None, ""):
            return "{}"
        try:
            parsed = json.loads(value) if isinstance(value, str) else value
            return json.dumps(parsed, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            return value


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ("ruleset", "order", "name", "conditions", "next_question", "outcome", "explanation_fr")
        widgets = {"conditions": PrettyJSONWidget(attrs={"rows": 8, "class": "font-mono"})}

    def clean(self):
        cleaned = super().clean()
        ruleset = cleaned.get("ruleset") or getattr(self.instance, "ruleset", None)
        nxt, out = cleaned.get("next_question"), cleaned.get("outcome")
        if (nxt is None) == (out is None):
            raise forms.ValidationError(_("Indiquer exactement une destination : question suivante ou résultat."))
        if ruleset is not None:
            spec = services.spec_for(ruleset)
            problems = engine.validate_conditions(cleaned.get("conditions") or {}, spec)
            if problems:
                self.add_error("conditions", problems)
            if nxt is not None and nxt.ruleset_id != ruleset.pk:
                self.add_error("next_question", _("La question appartient à un autre ruleset."))
            if out is not None and out.ruleset_id != ruleset.pk:
                self.add_error("outcome", _("Le résultat appartient à un autre ruleset."))
        return cleaned


# --------------------------------------------------------------------------------------------
# Inlines
# --------------------------------------------------------------------------------------------
class QuestionInline(BaseTabularInline):
    model = Question
    fields = ("order", "key", "text_fr", "type", "is_entry")
    show_change_link = True


class OutcomeInline(BaseTabularInline):
    model = Outcome
    fields = ("key", "pathway_key", "title_fr")
    show_change_link = True


class RuleInline(BaseStackedInline):
    model = Rule
    form = RuleForm
    fields = ("order", "name", "conditions", "next_question", "outcome", "explanation_fr")
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        ruleset_id = request.resolver_match.kwargs.get("object_id") if request.resolver_match else None
        if db_field.name == "next_question" and ruleset_id:
            kwargs["queryset"] = Question.objects.filter(ruleset_id=ruleset_id)
        if db_field.name == "outcome" and ruleset_id:
            kwargs["queryset"] = Outcome.objects.filter(ruleset_id=ruleset_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ChoiceInline(BaseTabularInline):
    model = Choice
    fields = ("order", "key", "label_fr")


class QuestionTranslationInline(BaseTabularInline):
    model = QuestionTranslation
    fields = ("language", "status", "text", "help", "source")


class ChoiceTranslationInline(BaseTabularInline):
    model = ChoiceTranslation
    fields = ("language", "status", "label", "source")


class ChecklistItemInline(BaseTabularInline):
    model = ChecklistItem
    fields = ("category", "order", "text_fr")


class OutcomeTranslationInline(BaseStackedInline):
    model = OutcomeTranslation
    fields = ("language", "status", "title", "explanation", "source")


class ChecklistItemTranslationInline(BaseTabularInline):
    model = ChecklistItemTranslation
    fields = ("language", "status", "text", "source")


# --------------------------------------------------------------------------------------------
# Admins
# --------------------------------------------------------------------------------------------
@admin.register(Ruleset)
class RulesetAdmin(BaseModelAdmin):
    list_display = ("version", "status", "question_count", "outcome_count", "rule_count", "activated_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("notes",)
    readonly_fields = ("status", "activated_at", "created_by", "integrity_report", "pending_note")
    fieldsets = (
        (None, {"fields": ("version", "status", "notes", "pending_note")}),
        (_("Intégrité"), {"fields": ("integrity_report",)}),
        (_("Audit"), {"fields": ("created_by", "activated_at", "created_at", "updated_at")}),
    )
    inlines = (QuestionInline, OutcomeInline, RuleInline)
    actions = ("validate_action", "activate_action", "export_action")

    @admin.display(description=_("domande"))
    def question_count(self, obj):
        return obj.questions.count()

    @admin.display(description=_("risultati"))
    def outcome_count(self, obj):
        return obj.outcomes.count()

    @admin.display(description=_("regole"))
    def rule_count(self, obj):
        return obj.rules.count()

    @admin.display(description=_("nota"))
    def pending_note(self, obj):
        return PENDING_NOTE

    @admin.display(description=_("rapporto di integrità"))
    def integrity_report(self, obj):
        if not obj.pk:
            return "—"
        report = services.validate_ruleset(obj)
        lines = [f"{'OK' if report.ok else 'ERRORI'} — {report.paths} percorsi, profondità max {report.max_depth}"]
        lines += [f"✗ {e}" for e in report.errors]
        lines += [f"⚠ {w}" for w in report.warnings]
        return format_html("<pre style='white-space:pre-wrap'>{}</pre>", "\n".join(lines))

    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description=_("Valider l’intégrité du ruleset"))
    def validate_action(self, request, queryset):
        for ruleset in queryset:
            report = services.validate_ruleset(ruleset)
            if report.ok:
                self.message_user(
                    request, f"v{ruleset.version}: OK ({report.paths} chemins, {len(report.warnings)} avertissements)"
                )
            else:
                self.message_user(request, f"v{ruleset.version}: {'; '.join(report.errors)}", level=messages.ERROR)

    @admin.action(description=_("Activer ce ruleset (remplace le ruleset actif)"))
    def activate_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, _("Sélectionner exactement un ruleset."), level=messages.ERROR)
            return
        ruleset = queryset.first()
        try:
            services.activate_ruleset(ruleset, user=request.user, request=request)
        except services.RulesetInvalid as exc:
            self.message_user(request, "; ".join(exc.report.errors), level=messages.ERROR)
            return
        self.message_user(request, f"Ruleset v{ruleset.version} activé.")

    @admin.action(description=_("Exporter en JSON"))
    def export_action(self, request, queryset):
        payload = [services.export_ruleset(r) for r in queryset]
        data = json.dumps(payload[0] if len(payload) == 1 else payload, ensure_ascii=False, indent=2)
        response = HttpResponse(data, content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="orientation-ruleset.json"'
        return response


@admin.register(Question)
class QuestionAdmin(BaseModelAdmin):
    list_display = ("key", "ruleset", "order", "type", "is_entry", "text_fr")
    list_filter = ("ruleset", "type", "is_entry")
    search_fields = ("key", "text_fr")
    ordering = ("ruleset", "order")
    inlines = (ChoiceInline, QuestionTranslationInline)
    fieldsets = (
        (None, {"fields": ("ruleset", "key", "order", "type", "is_entry")}),
        (_("Texte (FR — source)"), {"fields": ("text_fr", "help_fr")}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    list_display = ("key", "question", "order", "label_fr")
    list_filter = ("question__ruleset",)
    search_fields = ("key", "label_fr")
    inlines = (ChoiceTranslationInline,)


@admin.register(Outcome)
class OutcomeAdmin(BaseModelAdmin):
    list_display = ("key", "ruleset", "pathway_key", "title_fr")
    list_filter = ("ruleset", "pathway_key")
    search_fields = ("key", "title_fr", "explanation_fr")
    readonly_fields = ("pending_note",)
    inlines = (ChecklistItemInline, OutcomeTranslationInline)
    fieldsets = (
        (None, {"fields": ("ruleset", "key", "pathway_key", "disclaimer_key", "pending_note")}),
        (_("Texte (FR — source)"), {"fields": ("title_fr", "explanation_fr")}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description=_("nota"))
    def pending_note(self, obj):
        return PENDING_NOTE


@admin.register(ChecklistItem)
class ChecklistItemAdmin(BaseModelAdmin):
    list_display = ("outcome", "category", "order", "text_fr")
    list_filter = ("outcome__ruleset", "category")
    search_fields = ("text_fr",)
    inlines = (ChecklistItemTranslationInline,)


@admin.register(Rule)
class RuleAdmin(BaseModelAdmin):
    form = RuleForm
    list_display = ("ruleset", "order", "name", "readable_conditions", "target_label")
    list_filter = ("ruleset",)
    search_fields = ("name",)
    ordering = ("ruleset", "order")
    readonly_fields = ("readable_conditions",)
    fieldsets = (
        (None, {"fields": ("ruleset", "order", "name")}),
        (_("Conditions"), {"fields": ("conditions", "readable_conditions")}),
        (_("Destination"), {"fields": ("next_question", "outcome", "explanation_fr")}),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description=_("condizioni (lettura)"))
    def readable_conditions(self, obj):
        if obj is None or obj.pk is None:
            return "—"
        try:
            return engine.describe_conditions(obj.conditions)
        except engine.InvalidConditions as exc:
            return f"⚠ {exc}"


@admin.register(OrientationSession)
class OrientationSessionAdmin(BaseModelAdmin):
    list_display = ("reference", "status", "ruleset", "language", "has_user", "created_at", "expires_at")
    list_filter = ("status", "ruleset", "language")
    date_hierarchy = "created_at"
    readonly_fields = ("id", "ruleset", "user", "status", "language", "state", "current_question", "expires_at")
    fields = (
        "id",
        "ruleset",
        "user",
        "status",
        "language",
        "current_question",
        "expires_at",
        "state",
        "created_at",
        "updated_at",
    )
    actions = ("anonymise_action",)
    search_fields = ("id",)

    @admin.display(description=_("riferimento"))
    def reference(self, obj):
        return obj.reference

    @admin.display(description=_("account"), boolean=True)
    def has_user(self, obj):
        return bool(obj.user_id)

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Anonymiser (RGPD) — supprime identifiants et réponses"))
    def anonymise_action(self, request, queryset):
        count = 0
        for session in queryset:
            services.anonymise_session(session, request)
            count += 1
        self.message_user(request, f"{count} session(s) anonymisée(s).")


@admin.register(OrientationResult)
class OrientationResultAdmin(BaseModelAdmin):
    list_display = ("session_reference", "outcome", "ruleset_version", "disclaimer_version", "created_at")
    list_filter = ("outcome", "ruleset_version", "disclaimer_version")
    date_hierarchy = "created_at"
    readonly_fields = (
        "session",
        "outcome",
        "ruleset_version",
        "disclaimer_version",
        "disclaimer_key",
        "answers_snapshot",
        "result_text_fr",
        "created_at",
    )
    actions = ("export_statistics_csv",)

    @admin.display(description=_("sessione"))
    def session_reference(self, obj):
        return obj.session.reference

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description=_("Exporter les statistiques anonymisées (CSV)"))
    def export_statistics_csv(self, request, queryset):
        response = HttpResponse(services.statistics_csv(queryset), content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="orientation-statistiques.csv"'
        return response


# Keep RulesetStatus importable for admin tests/filters.
__all__ = ["RulesetStatus"]
