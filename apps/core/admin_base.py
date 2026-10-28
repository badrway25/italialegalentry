"""
Back-office base classes. Every ModelAdmin in the project inherits from these so the editorial
UI is consistent (django-unfold) and audit metadata is always read-only.
"""

from __future__ import annotations

from contextlib import suppress

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline, TabularInline

AUDIT_READONLY_FIELDS = ("created_at", "updated_at")


# -- no form and no filter names another account to an account that may not read accounts (F-8, review F8R-3) ------
def may_read_accounts(admin_site, request) -> bool:
    """Whether ``request.user`` may open the accounts screen — the test Django's own autocomplete asks of a target."""
    from django.contrib.auth import get_user_model

    accounts_admin = admin_site._registry.get(get_user_model())
    return accounts_admin is not None and accounts_admin.has_view_permission(request)


def account_fields(model) -> list[str]:
    """The editable fields of ``model`` that point at an account (a foreign key or a many-to-many to the user model)."""
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    return [
        field.name
        for field in model._meta.get_fields()
        if field.is_relation
        and not field.auto_created
        and getattr(field, "editable", False)
        and field.related_model is user_model
    ]


def frozen_account_fields(model_admin, request, obj=None) -> list[str]:
    """
    The account fields of a form that ``request.user`` may not choose: every one it shows, for an account that may not
    open the accounts screen.

    ``User.__str__`` is the e-mail address and a foreign key renders its choices from the whole user table: the
    editorial forms listed every account's address — persons included — to role:staff and role:content_editor, and an
    autocomplete rendered the address of whichever account its initial value named (``?author=<pk>``). Read-only, the
    field shows the account the row already names (who wrote it, who reviewed it) and nothing else; the workflow sets
    it — ``cms.admin.PublishableAdminMixin`` the author, the review actions the reviewer.
    """
    if may_read_accounts(model_admin.admin_site, request):
        return []
    names = account_fields(model_admin.model)
    if not names:
        return []
    form_meta = getattr(model_admin.form, "_meta", None)
    excluded = set(model_admin.get_exclude(request, obj) or ()) | set(getattr(form_meta, "exclude", None) or ())
    names = [name for name in names if name not in excluded]
    declared = getattr(form_meta, "fields", None)
    if not (model_admin.fieldsets or model_admin.fields) and declared not in (None, "__all__"):
        names = [name for name in names if name in declared]  # a form that never shows the field keeps not showing it
    return names


def with_frozen_account_fields(model_admin, request, obj, fields) -> list:
    """``fields`` (a screen's read-only fields) with its frozen account fields — for an override that does not call
    ``super().get_readonly_fields``."""
    fields = list(fields)
    for name in frozen_account_fields(model_admin, request, obj):
        if name not in fields:
            fields.append(name)
    return fields


class BaseModelAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        for f in AUDIT_READONLY_FIELDS:
            if hasattr(self.model, f) and f not in fields:
                fields.append(f)
        return with_frozen_account_fields(self, request, obj, fields)

    def get_list_filter(self, request):
        """
        A filter over an account lists, to an account that may not read accounts, only the accounts the screen's own
        rows name (``RelatedOnlyFieldListFilter``, which reads this screen's queryset) — never the whole user table, as
        Django's default filter for a foreign key does (F-8, review F8R-3: «dernier éditeur» on the news list).
        """
        filters = super().get_list_filter(request)
        if may_read_accounts(self.admin_site, request):
            return filters
        from django.contrib.admin import RelatedOnlyFieldListFilter
        from django.contrib.admin.utils import NotRelationField, get_fields_from_path
        from django.contrib.auth import get_user_model

        narrowed = []
        for item in filters:
            if isinstance(item, str):
                with suppress(FieldDoesNotExist, NotRelationField):
                    if getattr(get_fields_from_path(self.model, item)[-1], "related_model", None) is get_user_model():
                        item = (item, RelatedOnlyFieldListFilter)
            narrowed.append(item)
        return narrowed

    # -- a field the page hides is no filter either (finding F-8, review F8R-2) ------------------------------------
    def hidden_fields(self, request) -> frozenset[str]:
        """
        The model's fields this screen never shows to ``request.user`` — none by default; ``request`` may be ``None``,
        and is then answered with every field the screen ever hides.

        A changelist prints its count, and Django lets the query string filter on any of the model's own fields
        (``ModelAdmin.lookup_allowed`` refuses only lookups across relations): a field hidden from the page still
        answered, one predicate at a time, what the page hides — ``?confirm_token__startswith=`` recovered a
        subscriber's bearer token, ``?body_text__contains=`` read a mail's body for a view grant. A lookup over one of
        these fields is refused as Django refuses any lookup it does not allow (its 400, logged as a security event),
        and the search box never reads one.
        """
        return frozenset()

    def _over_hidden_field(self, request, lookup: str) -> bool:
        hidden = self.hidden_fields(request)
        if not hidden:
            return False
        head = lookup.split(LOOKUP_SEP, 1)[0]
        with suppress(FieldDoesNotExist):
            head = self.model._meta.get_field(head).name  # an attname («owner_id») names its field
        return head in hidden

    def lookup_allowed(self, lookup, value, request=None):
        if self._over_hidden_field(request, lookup):
            return False
        return super().lookup_allowed(lookup, value, request)

    def get_search_fields(self, request):
        fields = super().get_search_fields(request)
        if not self.hidden_fields(request):
            return fields
        return tuple(name for name in fields if not self._over_hidden_field(request, name.lstrip("^=@")))


class PolicyBoundAdminMixin:
    """
    A back-office screen that grants no more than the platform's own authorisation (finding F-8).

    A model permission opens a screen, and ``accounts.roles.ROLE_PERMISSIONS`` grants by application, never by row.
    On the platform the same account is judged by the model's object policy (``accounts.permissions.can``, deny by
    default) and by its ``readable_by`` queryset — per row, per role, per state. Until F-8 the back office asked the
    model permission alone, so role:operator read every case file here and none on the platform. A screen built on
    this mixin asks both; each is a necessary condition, so nobody gains anything:

    * ``policy_roles`` — the roles the model's policy names for reading its rows from the back office (for instance
      ``enquiries.policies.BACKOFFICE_VIEW_ROLES``). An account holding the model permission and none of these roles
      finds the screen closed, as without the permission. ``None``: no role gate, the rows decide.
    * ``readable(request, queryset)`` — the rows the policy lets the account read, as a queryset: the domain's
      ``readable_by``. Lists, counts, searches, filters, autocompletes and object pages all read from it, so a row the
      account may not read does not exist here either — Django's admin answers it as it answers an id never issued.
    * ``object_policy`` — an object's page also asks ``can(user, "view" | "change" | "delete", obj)``: an object the
      account may read and not change opens read-only, and a deletion the policy refuses is refused (Django's admin
      asks ``has_delete_permission`` for every object a deletion collects).

    A superuser passes every gate, as it passes every policy (PERMISSION_MODEL §3.4). Listed before the ModelAdmin
    class it narrows.
    """

    policy_roles: tuple[str, ...] | None = None
    object_policy: bool = False

    def policy_admits(self, request) -> bool:
        if self.policy_roles is None:
            return True
        from accounts import roles

        user = request.user
        return bool(getattr(user, "is_superuser", False)) or roles.has_role(user, *self.policy_roles)

    def readable(self, request, queryset):
        """The rows the platform lets ``request.user`` read — the domain's ``readable_by``. Every row by default."""
        return queryset

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.policy_admits(request):
            return queryset.none()
        return self.readable(request, queryset)

    def object_admits(self, request, action: str, obj) -> bool:
        if obj is None or not self.object_policy:
            return True
        from accounts.permissions import can

        return can(request.user, action, obj)

    def has_module_permission(self, request):
        return self.policy_admits(request) and super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        return (
            self.policy_admits(request)
            and super().has_view_permission(request, obj)
            and self.object_admits(request, "view", obj)
        )

    def has_change_permission(self, request, obj=None):
        return (
            self.policy_admits(request)
            and super().has_change_permission(request, obj)
            and self.object_admits(request, "change", obj)
        )

    def has_add_permission(self, request):
        return self.policy_admits(request) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return (
            self.policy_admits(request)
            and super().has_delete_permission(request, obj)
            and self.object_admits(request, "delete", obj)
        )


class BaseTabularInline(TabularInline):
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return with_frozen_account_fields(self, request, obj, super().get_readonly_fields(request, obj))


class BaseStackedInline(StackedInline):
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return with_frozen_account_fields(self, request, obj, super().get_readonly_fields(request, obj))


class LockedContentAdminMixin:
    """Fields listed in ``locked_fields`` come from the locked registry: shown, never editable."""

    locked_fields: tuple[str, ...] = ()

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        for f in self.locked_fields:
            if f not in fields:
                fields.append(f)
        return fields


def environment_badge(request):
    if settings.DEBUG:
        return [str(_("Sviluppo locale")), "warning"]
    return [str(_("Produzione")), "danger"]


def dashboard_callback(request, context):
    from core import gates
    from core.phases import console_rows

    snap = gates.snapshot()
    context["ile_gates"] = snap
    # The console says what each gate CONTROLS. The boolean rows below stay for the compact view;
    # a reader who needs to decide whether to open something needs the console.
    context["ile_phase_console"] = console_rows()
    context["ile_gate_rows"] = [
        (str(_("Pagine legali ufficiali (IT)")), snap["legal_pages_available"]),
        (str(_("Form pubblici attivi")), snap["public_forms_enabled"]),
        (str(_("Contenuti Fase 3 pubblici")), snap["phase3_public"]),
        (str(_("Banner Forum in homepage")), snap["forum_banner_visible"]),
        (str(_("Forum in modalità permanente")), snap["forum_permanent_mode"]),
        (str(_("Forum Virtuale")), snap["virtual_forum_enabled"]),
        (str(_("Newsletter")), snap["newsletter_enabled"]),
    ]
    return context
