from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from accounts import roles
from accounts.models import Membership, Organisation, PersonProfile, User
from core.admin_base import BaseModelAdmin, BaseTabularInline

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin, BaseModelAdmin):
    pass


class MembershipInline(BaseTabularInline):
    model = Membership
    autocomplete_fields = ("organisation",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin, BaseModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    ordering = ("email",)
    list_display = ("email", "full_name", "account_type", "is_active", "is_staff", "date_joined")
    list_filter = ("account_type", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("email", "full_name")
    readonly_fields = ("date_joined", "last_login", "terms_accepted_at", "terms_consent", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Profilo"), {"fields": ("full_name", "preferred_language", "account_type")}),
        (_("Autorizzazioni (RBAC)"), {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
        (_("Consenso e audit"), {"fields": ("terms_accepted_at", "terms_consent", "date_joined", "last_login")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "full_name", "account_type", "password1", "password2")}),
    )
    inlines = (MembershipInline,)
    filter_horizontal = ("groups",)

    # -- privilege-escalation guard -------------------------------------------------------------
    # ``role:administrator`` holds ``accounts: change``, and Django's UserAdmin happily exposes
    # ``is_superuser`` and ``groups`` to anyone with that permission. Without the three overrides
    # below, an administrator can tick "superuser" on their own account — or grant themselves
    # ``role:superadmin``, which ``accounts.permissions.can`` short-circuits past every policy — and
    # walk out with full control. That is a one-click escalation, and it defeats REQ-IAM-05
    # (least privilege), REQ-IAM-07 (authorisation is not ``is_staff``) and REQ-IAM-10 (a role
    # editor must not reach unrelated superadmin access).
    #
    # Rule: only a superuser grants superuser-level power. Everyone else manages ordinary accounts.

    #: Groups a non-superuser may never grant, because holding one is equivalent to escalation.
    PROTECTED_GROUPS = ("role:superadmin", "role:administrator")

    def _is_privileged(self, request) -> bool:
        return bool(request.user and request.user.is_superuser)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self._is_privileged(request):
            return fieldsets
        trimmed = []
        for title, options in fieldsets:
            fields = tuple(name for name in options.get("fields", ()) if name != "is_superuser")
            trimmed.append((title, {**options, "fields": fields}))
        return tuple(trimmed)

    def get_readonly_fields(self, request, obj=None):
        readonly = tuple(super().get_readonly_fields(request, obj))
        if self._is_privileged(request):
            return readonly
        # Belt and braces: hidden from the form AND rejected if posted anyway.
        return readonly + ("is_superuser",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self._forbid_incompatible_roles(form)
        if self._is_privileged(request) or "groups" not in form.base_fields:
            return form
        field = form.base_fields["groups"]
        field.queryset = field.queryset.exclude(name__in=self.PROTECTED_GROUPS)
        field.help_text = _("I gruppi di amministrazione generale sono assegnabili solo da un'utenza superadmin.")
        return form

    @staticmethod
    def _forbid_incompatible_roles(form) -> None:
        """
        Refuse a separation-of-duties breach posted through the admin.

        ``roles.assign_role`` already refuses the pair, but the admin does not go through it: it
        writes the many-to-many directly. A constraint that only one of two entry points enforces is
        not a constraint, so the same check is applied to whatever this form is about to save —
        including a superuser's form, because four eyes is precisely the rule a privileged account
        must not be able to waive for itself.
        """
        field = form.base_fields.get("groups")
        if field is None:
            return
        original_clean = field.clean

        def clean(value):
            groups = original_clean(value)
            roles.check_role_set(group.name for group in groups)
            return groups

        field.clean = clean

    def has_change_permission(self, request, obj=None) -> bool:
        # A non-superuser never edits a superuser: otherwise they could reset that account's
        # password and sign in as it, reaching the same place by a longer road.
        if obj is not None and obj.is_superuser and not self._is_privileged(request):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        if obj is not None and obj.is_superuser and not self._is_privileged(request):
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        # Last line of defence: a crafted POST cannot raise privilege even if the form is bypassed.
        if not self._is_privileged(request):
            if change:
                stored = type(obj).objects.filter(pk=obj.pk).values("is_superuser").first()
                obj.is_superuser = bool(stored and stored["is_superuser"])
            else:
                obj.is_superuser = False
        super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        # Read the protected groups the account holds BEFORE the many-to-many is overwritten, and
        # carry them on the request (never on self: a ModelAdmin instance is shared across threads).
        request._ile_protected_groups = (
            set(form.instance.groups.filter(name__in=self.PROTECTED_GROUPS).values_list("pk", flat=True))
            if change and form.instance.pk
            else set()
        )
        return super().save_form(request, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if self._is_privileged(request):
            return
        # Groups are a many-to-many written after the model: restore exactly the protected groups
        # the account already held, so a non-superuser can neither grant nor strip them.
        obj = form.instance
        protected_pks = set(Group.objects.filter(name__in=self.PROTECTED_GROUPS).values_list("pk", flat=True))
        if not protected_pks:
            return
        kept = set(obj.groups.values_list("pk", flat=True)) - protected_pks
        obj.groups.set(kept | getattr(request, "_ile_protected_groups", set()))


@admin.register(Organisation)
class OrganisationAdmin(BaseModelAdmin):
    list_display = ("name", "kind", "country", "city", "created_at")
    list_filter = ("kind", "country")
    search_fields = ("name", "city")
    inlines = (MembershipInline,)


@admin.register(PersonProfile)
class PersonProfileAdmin(BaseModelAdmin):
    list_display = ("user", "country_of_residence")
    search_fields = ("user__email",)
    autocomplete_fields = ("user",)
