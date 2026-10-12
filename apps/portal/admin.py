"""
Back-office of the reserved area.

Access is ROLE-based (``accounts.roles``) rather than driven by Django's per-model permissions: a
bare ``is_staff`` flag opens nothing here. Staff/administrator roles may read and write; only the
administrator role (and superadmins — ``is_superuser`` or the role:superadmin group) may delete or
rewrite a communication.

Data minimisation: the recipient of a message / the owner of a deadline is designated by typing the
EXACT e-mail address of the account — the form never offers a browsable list of accounts, and the
account can no longer be changed once the row exists. Creation, changes and deletions (object page
AND bulk action) are audited (``audit.services.record``) without ever copying the subject, the
title, the body or an e-mail address — the models' ``__str__`` is neutral for that reason.
"""

from __future__ import annotations

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts import roles
from audit.services import record as audit_record
from cms.admin import PUBLICATION_FIELDSET, PUBLICATION_READONLY, PublishableAdminMixin
from core.admin_base import BaseModelAdmin
from portal import services
from portal.models import Deadline, Message, PortalNotice

# role:superadmin is listed explicitly: ``accounts.permissions.can`` treats that group like a
# superuser, so the back-office must not lock it out (``roles.has_role`` only short-circuits on
# ``is_superuser``). ``is_staff`` stays mandatory in every case.
WRITE_ROLES = (roles.STAFF, roles.ADMINISTRATOR, roles.SUPERADMIN)
MANAGE_ROLES = (roles.ADMINISTRATOR, roles.SUPERADMIN)

ACCOUNT_EMAIL_HELP = _(
    "Saisissez l’adresse e-mail exacte du compte concerné. Minimisation des données : aucune liste de comptes "
    "n’est proposée, et l’élément ne sera visible que par ce compte — jamais par un autre utilisateur."
)

#: Records a communication may point to (the portal only ever links to a record owned by the reader).
RELATED_MODELS = (
    ("enquiries", "companyneedsrequest"),
    ("enquiries", "collaborationproposal"),
    ("enquiries", "contactrequest"),
    ("forum", "forumregistration"),
    ("documents", "privatedocument"),
    ("portal", "deadline"),
)


class RoleScopedAdmin(BaseModelAdmin):
    """View/add/change for the staff + administrator roles; delete for administrators only."""

    write_roles = WRITE_ROLES
    manage_roles = MANAGE_ROLES

    def _has_role(self, request, allowed) -> bool:
        user = request.user
        return bool(user.is_active and user.is_staff and roles.has_role(user, *allowed))

    def has_module_permission(self, request):
        return self._has_role(request, self.write_roles)

    def has_view_permission(self, request, obj=None):
        return self._has_role(request, self.write_roles)

    def has_add_permission(self, request):
        return self._has_role(request, self.write_roles)

    def has_change_permission(self, request, obj=None):
        return self._has_role(request, self.write_roles)

    def has_delete_permission(self, request, obj=None):
        return self._has_role(request, self.manage_roles)

    # -- deletions are always audited, row by row, on BOTH paths (object page and bulk action) ----
    audit_name = ""  # "message" → action ``portal.message.deleted``
    audit_account_field = ""  # FK whose *id* goes to the audit metadata (never an e-mail address)

    def _audit_deleted(self, request, obj) -> None:
        metadata = {}
        if self.audit_account_field:
            key = f"{self.audit_account_field}_id"
            metadata[key] = getattr(obj, key, None)
        audit_record(request, action=f"portal.{self.audit_name}.deleted", target=obj, metadata=metadata)

    def delete_model(self, request, obj):
        self._audit_deleted(request, obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # The « delete selected » action never calls delete_model(): audit each row here too.
        for obj in queryset:
            self._audit_deleted(request, obj)
        super().delete_queryset(request, queryset)


class AccountEmailForm(forms.ModelForm):
    """Designates the account by exact e-mail on creation (no browsable user list)."""

    account_field = "owner"
    account_email = forms.EmailField(label=_("E-mail du compte concerné"), help_text=ACCOUNT_EMAIL_HELP)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance._state.adding:
            self.fields.pop("account_email", None)

    def clean_account_email(self):
        email = (self.cleaned_data.get("account_email") or "").strip().lower()
        user = get_user_model().objects.filter(email__iexact=email, is_active=True).first()
        if user is None:
            raise forms.ValidationError(_("Aucun compte actif ne correspond à cette adresse e-mail."))
        setattr(self.instance, self.account_field, user)
        return email


class MessageAdminForm(AccountEmailForm):
    account_field = "recipient"

    class Meta:
        model = Message
        fields = ("subject", "body", "visible_from", "content_type", "object_id")


class DeadlineAdminForm(AccountEmailForm):
    account_field = "owner"

    class Meta:
        model = Deadline
        fields = ("title", "due_on", "kind", "status", "description", "source_note")


@admin.register(Message)
class MessageAdmin(RoleScopedAdmin):
    form = MessageAdminForm
    audit_name = "message"
    audit_account_field = "recipient"
    list_display = ("created_at", "subject", "recipient", "is_read", "read_at", "visible_from", "sender")
    list_filter = ("is_read", "created_at", "visible_from")
    search_fields = ("recipient__email", "subject")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("recipient", "sender")
    list_per_page = 50

    def has_change_permission(self, request, obj=None):
        # A sent communication is evidence: only administrators may correct it afterwards.
        return self._has_role(request, self.manage_roles)

    def get_fieldsets(self, request, obj=None):
        account = ("recipient",) if obj else ("account_email",)
        return (
            (_("Destinataire"), {"fields": account}),
            (_("Communication"), {"fields": ("subject", "body", "visible_from")}),
            (
                _("Élément lié (optionnel)"),
                {
                    "classes": ("collapse",),
                    "fields": ("content_type", "object_id"),
                    "description": _(
                        "Le lien n’est affiché à la personne que si l’élément lui appartient ; sinon il est ignoré."
                    ),
                },
            ),
            (_("Suivi"), {"fields": ("sender", "is_read", "read_at", "created_at", "updated_at")}),
        )

    def get_readonly_fields(self, request, obj=None):
        fields = [*super().get_readonly_fields(request, obj), "sender", "is_read", "read_at"]
        if obj is not None:
            fields.append("recipient")
            if obj.is_read:
                fields += ["subject", "body", "visible_from", "content_type", "object_id"]
        return tuple(dict.fromkeys(fields))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            query = Q()
            for app_label, model in RELATED_MODELS:
                query |= Q(app_label=app_label, model=model)
            kwargs["queryset"] = ContentType.objects.filter(query)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user
        super().save_model(request, obj, form, change)
        if change:
            audit_record(
                request,
                action="portal.message.changed",
                target=obj,
                metadata={"recipient_id": obj.recipient_id, "fields": sorted(form.changed_data)},
            )
        else:
            services.audit_message_created(obj, request=request, actor=request.user)


@admin.register(Deadline)
class DeadlineAdmin(RoleScopedAdmin):
    form = DeadlineAdminForm
    audit_name = "deadline"
    audit_account_field = "owner"
    list_display = ("due_on", "title", "owner", "kind", "status", "updated_at")
    list_filter = ("status", "kind", "due_on")
    search_fields = ("owner__email", "title")
    date_hierarchy = "due_on"
    ordering = ("due_on",)
    list_select_related = ("owner",)
    list_per_page = 50

    def get_fieldsets(self, request, obj=None):
        account = ("owner",) if obj else ("account_email",)
        return (
            (_("Compte concerné"), {"fields": account}),
            (_("Échéance"), {"fields": ("title", "due_on", "kind", "status", "description", "source_note")}),
            (_("Suivi"), {"fields": ("created_at", "updated_at")}),
        )

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            fields.append("owner")
        return tuple(dict.fromkeys(fields))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        audit_record(
            request,
            action="portal.deadline.changed" if change else "portal.deadline.created",
            target=obj,
            metadata={"owner_id": obj.owner_id, "fields": sorted(form.changed_data) if change else []},
        )


@admin.register(PortalNotice)
class PortalNoticeAdmin(PublishableAdminMixin, RoleScopedAdmin):
    audit_name = "notice"
    list_display = ("heading_fr", "audience", "status", "order", "publish_at", "unpublish_at", "version")
    list_filter = ("status", "audience")
    list_editable = ("order",)
    search_fields = ("heading_fr", "body_fr")
    readonly_fields = PUBLICATION_READONLY + ("author",)
    fieldsets = (
        (
            None,
            {
                "fields": ("audience", "heading_fr", "body_fr", "order"),
                "description": _(
                    "Avis affiché uniquement à l’intérieur de l’espace réservé (jamais sur le site public). "
                    "Aucune donnée personnelle, aucun contenu juridique non validé."
                ),
            },
        ),
        PUBLICATION_FIELDSET,
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reviewer":
            kwargs["queryset"] = get_user_model().objects.filter(is_staff=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
