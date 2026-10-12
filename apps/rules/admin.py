"""
The rule editor.

Three things distinguish it from a generic model admin, and each exists because a legal rule is not
an ordinary row:

* **A rule in force is read-only.** Editing one in place would silently rewrite the reasoning behind
  every assessment that used it. The editor offers "open a new version" instead, which is the honest
  operation.
* **The workflow is not a dropdown.** ``review_status`` is never an editable field; it moves through
  ``services.transition``, which refuses an author approving their own rule and refuses a rule
  entering into force without a source. A dropdown would let a reviewer skip both by choosing well.
* **A version can be compared, and a rule can be tried before it binds anyone.** The diff shows what
  changed against the previous version, and the preview runs the rule against facts the reviewer
  types, so approval is an informed act rather than a signature.
"""

from __future__ import annotations

import json

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from accounts.permissions import can
from core.admin_base import BaseModelAdmin
from rules import services
from rules.engine import InvalidCondition, describe_condition, validate_condition
from rules.models import LegalRule, LegalSource, ReviewStatus

#: Fields whose change between two versions a reviewer must see. ``note`` is deliberately absent:
#: an internal justification changing is not a change to the rule.
DIFFED_FIELDS = (
    "jurisdiction",
    "pathway",
    "condition",
    "effect",
    "message_key",
    "message_fr",
    "requirement_fr",
    "responsible_actor",
    "valid_from",
    "valid_to",
)

STATUS_COLOURS = {
    ReviewStatus.DRAFT: "#6b6b6b",
    ReviewStatus.LEGAL_REVIEW: "#a88232",
    ReviewStatus.APPROVED: "#1c5c3a",
    ReviewStatus.ACTIVE: "#0f2b46",
    ReviewStatus.RETIRED: "#8a1c1c",
}


@admin.register(LegalSource)
class LegalSourceAdmin(BaseModelAdmin):
    list_display = ("title_fr", "reference", "authority", "consulted_on", "rule_count")
    search_fields = ("key", "title_fr", "title_it", "reference", "authority")
    list_filter = ("authority",)
    prepopulated_fields = {"key": ("title_fr",)}
    fieldsets = (
        (None, {"fields": ("key", "title_fr", "title_it", "reference")}),
        (_("Provenienza"), {"fields": ("authority", "url", "consulted_on")}),
        (_("Interno"), {"fields": ("note",)}),
    )

    @admin.display(description=_("regole"))
    def rule_count(self, obj: LegalSource) -> int:
        return obj.rules.count()


@admin.register(LegalRule)
class LegalRuleAdmin(BaseModelAdmin):
    list_display = ("rule_id", "version", "pathway", "effect", "status_badge", "valid_from", "valid_to", "source_count")
    list_filter = ("review_status", "effect", "jurisdiction", "pathway")
    search_fields = ("rule_id", "message_fr", "requirement_fr", "pathway")
    filter_horizontal = ("sources",)
    ordering = ("pathway", "rule_id", "-version")
    actions = ("action_submit_for_review", "action_approve", "action_activate", "action_retire")
    fieldsets = (
        (None, {"fields": ("rule_id", "version", "jurisdiction", "pathway")}),
        (_("Condizione"), {"fields": ("condition", "condition_readable")}),
        (_("Effetto"), {"fields": ("effect", "message_key", "message_fr", "requirement_fr", "responsible_actor")}),
        (_("Fonti e validità"), {"fields": ("sources", "valid_from", "valid_to")}),
        (
            _("Revisione"),
            {"fields": ("review_status", "created_by", "approved_by", "approved_at", "retired_at", "note", "workflow")},
        ),
    )
    readonly_fields = (
        "review_status",
        "created_by",
        "approved_by",
        "approved_at",
        "retired_at",
        "condition_readable",
        "workflow",
    )

    # ------------------------------------------------------------------ display
    @admin.display(description=_("stato"), ordering="review_status")
    def status_badge(self, obj: LegalRule):
        return format_html(
            '<span style="color:{};font-weight:600">{}</span>',
            STATUS_COLOURS.get(obj.review_status, "#000"),
            obj.get_review_status_display(),
        )

    @admin.display(description=_("fonti"))
    def source_count(self, obj: LegalRule) -> str:
        count = obj.sources.count()
        return str(count) if count else "—"

    @admin.display(description=_("lettura della condizione"))
    def condition_readable(self, obj: LegalRule):
        if obj.pk is None:
            return "—"
        return format_html("<code>{}</code>", describe_condition(obj.condition or {}))

    @admin.display(description=_("azioni"))
    def workflow(self, obj: LegalRule):
        if obj.pk is None:
            return "—"
        links = (
            (reverse("admin:rules_legalrule_diff", args=[obj.pk]), _("Confronta con la versione precedente")),
            (reverse("admin:rules_legalrule_preview", args=[obj.pk]), _("Prova la regola")),
        )
        return format_html_join(" · ", '<a href="{}">{}</a>', links)

    # ------------------------------------------------------------------ guards
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None and obj.review_status in {ReviewStatus.ACTIVE, ReviewStatus.RETIRED}:
            # Frozen: every editable field becomes read-only. Not hidden — a reviewer must still be
            # able to read a rule in force — but not changeable through this screen or any other.
            for name in DIFFED_FIELDS + ("sources", "note"):
                if name not in fields:
                    fields.append(name)
        return fields

    def has_delete_permission(self, request, obj=None) -> bool:
        # A rule leaves service by being retired, never by being deleted: an assessment that cites a
        # rule nobody can read any more is not explainable.
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.full_clean(exclude=["created_by", "approved_by"])
        super().save_model(request, obj, form, change)

    # ------------------------------------------------------------------ workflow actions
    def _run(self, request, queryset, target: str, done: str):
        moved, refused = 0, []
        for rule in queryset:
            try:
                services.transition(rule, target, actor=request.user, request=request)
                moved += 1
            except (ValidationError, PermissionDenied) as exc:
                refused.append(f"{rule.rule_id} v{rule.version}: {_message_of(exc)}")
        if moved:
            self.message_user(request, f"{done} ({moved})", messages.SUCCESS)
        for line in refused:
            self.message_user(request, line, messages.ERROR)

    @admin.action(description=_("Invia in revisione giuridica"))
    def action_submit_for_review(self, request, queryset):
        self._run(request, queryset, ReviewStatus.LEGAL_REVIEW, str(_("Inviate in revisione")))

    @admin.action(description=_("Approva (richiede un revisore diverso dall'autore)"))
    def action_approve(self, request, queryset):
        self._run(request, queryset, ReviewStatus.APPROVED, str(_("Approvate")))

    @admin.action(description=_("Metti in vigore"))
    def action_activate(self, request, queryset):
        self._run(request, queryset, ReviewStatus.ACTIVE, str(_("Messe in vigore")))

    @admin.action(description=_("Ritira"))
    def action_retire(self, request, queryset):
        self._run(request, queryset, ReviewStatus.RETIRED, str(_("Ritirate")))

    # ------------------------------------------------------------------ extra views
    def get_urls(self):
        return [
            path(
                "<int:pk>/diff/",
                self.admin_site.admin_view(self.diff_view),
                name="rules_legalrule_diff",
            ),
            path(
                "<int:pk>/preview/",
                self.admin_site.admin_view(self.preview_view),
                name="rules_legalrule_preview",
            ),
            path(
                "<int:pk>/new-version/",
                self.admin_site.admin_view(self.new_version_view),
                name="rules_legalrule_new_version",
            ),
            *super().get_urls(),
        ]

    def _rule_or_404(self, request, pk) -> LegalRule:
        rule = get_object_or_404(LegalRule, pk=pk)
        if not can(request.user, "view", rule):
            raise PermissionDenied
        return rule

    def diff_view(self, request, pk):
        rule = self._rule_or_404(request, pk)
        previous = (
            LegalRule.objects.filter(rule_id=rule.rule_id, version__lt=rule.version).order_by("-version").first()
        )
        rows = []
        for name in DIFFED_FIELDS:
            new = getattr(rule, name)
            old = getattr(previous, name, None) if previous else None
            rows.append(
                {
                    "field": rule._meta.get_field(name).verbose_name,
                    "old": _readable(old),
                    "new": _readable(new),
                    "changed": previous is not None and _readable(old) != _readable(new),
                }
            )
        old_sources = set(previous.sources.values_list("key", flat=True)) if previous else set()
        new_sources = set(rule.sources.values_list("key", flat=True))
        rows.append(
            {
                "field": _("fonti"),
                "old": ", ".join(sorted(old_sources)) or "—",
                "new": ", ".join(sorted(new_sources)) or "—",
                "changed": previous is not None and old_sources != new_sources,
            }
        )
        context = {
            **self.admin_site.each_context(request),
            "title": _("Confronto di versioni — %(rule)s") % {"rule": rule.rule_id},
            "rule": rule,
            "previous": previous,
            "rows": rows,
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/rules/legalrule/diff.html", context)

    def preview_view(self, request, pk):
        """
        Run the rule against facts the reviewer types. Nothing is written.

        The value is not the answer but the disagreement: a reviewer who expects a rule to fire and
        watches it stay silent has found the defect before it reaches a person's screen.
        """
        rule = self._rule_or_404(request, pk)
        raw = request.POST.get("facts", "") if request.method == "POST" else ""
        facts, error, fired, condition_error = {}, "", None, ""
        try:
            validate_condition(rule.condition or {})
        except InvalidCondition as exc:
            condition_error = str(exc)
        if request.method == "POST" and not condition_error:
            try:
                parsed = json.loads(raw or "{}")
                if not isinstance(parsed, dict):
                    raise ValueError("un oggetto JSON è atteso")
                facts = parsed
            except (ValueError, TypeError) as exc:
                error = str(exc)
            else:
                from rules.engine import evaluate_condition

                fired = evaluate_condition(rule.condition or {}, facts)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Prova della regola — %(rule)s") % {"rule": rule.rule_id},
            "rule": rule,
            "readable": describe_condition(rule.condition or {}),
            "raw": raw or json.dumps(_example_facts(rule), indent=2, ensure_ascii=False),
            "fired": fired,
            "error": error,
            "condition_error": condition_error,
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/rules/legalrule/preview.html", context)

    def new_version_view(self, request, pk):
        rule = self._rule_or_404(request, pk)
        if not can(request.user, "new_version", rule):
            raise PermissionDenied
        if request.method != "POST":
            raise Http404
        draft = services.new_version(rule, actor=request.user, request=request)
        self.message_user(
            request,
            _("Creata la versione %(version)s in bozza.") % {"version": draft.version},
            messages.SUCCESS,
        )
        return redirect(reverse("admin:rules_legalrule_change", args=[draft.pk]))


def _message_of(exc) -> str:
    messages_list = getattr(exc, "messages", None)
    if messages_list:
        return " ".join(str(m) for m in messages_list)
    return str(exc)


def _readable(value) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, dict | list):
        return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)
    return str(value)


def _example_facts(rule: LegalRule) -> dict:
    """A starting point for the preview, built from the fields the rule actually reads."""
    fields = sorted(_fields_in(rule.condition or {}))
    example: dict = {"pathway": rule.pathway}
    for field in fields:
        root = field.split(".", 1)[0]
        if root == "answers":
            example.setdefault("answers", {})[field.split(".", 1)[1]] = ""
        else:
            example.setdefault(root, "")
    return example


def _fields_in(node) -> set[str]:
    if not isinstance(node, dict) or not node:
        return set()
    if "all" in node or "any" in node:
        found: set[str] = set()
        for child in node.get("all", node.get("any", [])):
            found |= _fields_in(child)
        return found
    if "not" in node:
        return _fields_in(node["not"])
    field = node.get("field")
    return {field} if isinstance(field, str) else set()
