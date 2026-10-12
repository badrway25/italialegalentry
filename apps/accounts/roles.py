"""
Role catalogue (RBAC). Roles are Django groups with a fixed name; ``ensure_roles()`` seeds them
with their model permissions. Object-level rules live in ``accounts.permissions``.
"""

from __future__ import annotations

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PERSON = "role:person"
COMPANY = "role:company"
INSTITUTION = "role:institution"
UNIVERSITY = "role:university"
PROFESSIONAL = "role:professional"
# An actor authorised under a named provision to act on a case for someone else. This is NOT a
# courtesy label: the case file refuses an assignment whose authorisation reference or validity
# window is missing, and the role exists so that refusal has something to check.
AUTHORISED_ACTOR = "role:authorised_actor"
# A body that delivers training and certifies its completion. Distinct from UNIVERSITY, which awards
# qualifications: the project's training partners mostly do not.
TRAINING_PROVIDER = "role:training_provider"
# Drafts legal rules. Deliberately CANNOT approve them — four eyes (Technical Blueprint §4) needs two
# distinct people, so the catalogue has to be able to name two distinct people.
LEGAL_EDITOR = "role:legal_editor"
# Approves legal rules and puts them in force. Held by the legal referent, not by the author.
LEGAL_APPROVER = "role:legal_approver"
# Edits published editorial content. Separated from ADMINISTRATOR so that changing a page does not
# require an account that can also change accounts.
CONTENT_EDITOR = "role:content_editor"
# Handles case files and the help desk day to day. The operational role the previous platform lacked,
# which is why its staff accounts all carried full administration.
OPERATOR = "role:operator"
MODERATOR = "role:moderator"
STAFF = "role:staff"
ADMINISTRATOR = "role:administrator"
SUPERADMIN = "role:superadmin"

# Human labels (French source, translated through the catalogues). The technical group name
# (« role:person ») is an identifier and must never be shown to a visitor.
ROLE_LABELS = {
    "role:person": _("Personne"),
    "role:company": _("Entreprise"),
    "role:institution": _("Institution"),
    "role:university": _("Université ou organisme de formation"),
    "role:professional": _("Professionnel"),
    "role:authorised_actor": _("Acteur autorisé"),
    "role:training_provider": _("Organisme de formation"),
    "role:legal_editor": _("Rédaction juridique"),
    "role:legal_approver": _("Validation juridique"),
    "role:content_editor": _("Rédaction éditoriale"),
    "role:operator": _("Opérateur"),
    "role:moderator": _("Modération"),
    "role:staff": _("Équipe du projet"),
    "role:administrator": _("Administration"),
    "role:superadmin": _("Administration générale"),
}

ALL_ROLES = (
    PERSON,
    COMPANY,
    INSTITUTION,
    UNIVERSITY,
    PROFESSIONAL,
    AUTHORISED_ACTOR,
    TRAINING_PROVIDER,
    LEGAL_EDITOR,
    LEGAL_APPROVER,
    CONTENT_EDITOR,
    OPERATOR,
    MODERATOR,
    STAFF,
    ADMINISTRATOR,
    SUPERADMIN,
)
BACKOFFICE_ROLES = (
    LEGAL_EDITOR,
    LEGAL_APPROVER,
    CONTENT_EDITOR,
    OPERATOR,
    MODERATOR,
    STAFF,
    ADMINISTRATOR,
    SUPERADMIN,
)

#: Roles a person may NOT hold at the same time, and why.
#: Four eyes is not a UI convention: if one account can both draft and approve, the review is the
#: same judgement recorded twice. ``assign_role`` refuses the pair, and the admin refuses it again
#: when groups are edited directly, so the constraint does not depend on which screen was used.
INCOMPATIBLE_ROLES: tuple[tuple[str, str], ...] = ((LEGAL_EDITOR, LEGAL_APPROVER),)


class IncompatibleRoles(ValidationError):
    """The requested combination of roles would defeat a separation of duties."""


def conflicting_role(held: set[str] | frozenset[str], candidate: str) -> str | None:
    """The role already held that ``candidate`` may not accompany, or None."""
    for first, second in INCOMPATIBLE_ROLES:
        if candidate == first and second in held:
            return second
        if candidate == second and first in held:
            return first
    return None


def check_role_set(names) -> None:
    """Raise if a set of role names contains an incompatible pair. Used wherever groups are set."""
    wanted = {name for name in names if name in ALL_ROLES}
    for first, second in INCOMPATIBLE_ROLES:
        if first in wanted and second in wanted:
            raise IncompatibleRoles(
                _("Les rôles « %(a)s » et « %(b)s » ne peuvent pas être attribués au même compte.")
                % {"a": ROLE_LABELS[first], "b": ROLE_LABELS[second]}
            )

# (app_label, model) → permission codenames granted per role. Deny by default: unlisted = nothing.
ROLE_PERMISSIONS: dict[str, dict[str, tuple[str, ...]]] = {
    MODERATOR: {
        "community": ("view", "change"),
    },
    STAFF: {
        "enquiries": ("view", "change"),
        "forum": ("view", "change", "add"),
        "news": ("view", "change", "add"),
        "faq": ("view", "change", "add"),
        "glossary": ("view", "change", "add"),
        "living": ("view", "change", "add"),
        "pathways": ("view", "change"),
        "cms": ("view", "change", "add"),
        "partners": ("view", "change", "add"),
        "consents": ("view",),
        "notifications": ("view",),
        "community": ("view", "change"),
    },
    LEGAL_EDITOR: {
        # Drafts rules and sources. No delete: a rule leaves service by being retired, which keeps
        # the assessments that used it explainable, not by disappearing.
        "rules": ("view", "change", "add"),
        "pathways": ("view",),
    },
    LEGAL_APPROVER: {
        # Reads everything a reviewer needs and changes only the review state, which the service
        # guards. Notably NO "add": an approver who could create a rule could approve their own.
        "rules": ("view", "change"),
        "pathways": ("view",),
        "audit": ("view",),
    },
    CONTENT_EDITOR: {
        "cms": ("view", "change", "add"),
        "news": ("view", "change", "add"),
        "faq": ("view", "change", "add"),
        "glossary": ("view", "change", "add"),
        "living": ("view", "change", "add"),
        "pathways": ("view", "change"),
        "partners": ("view", "change", "add"),
    },
    OPERATOR: {
        "cases": ("view", "change"),
        "helpdesk": ("view", "change", "add"),
        "enquiries": ("view", "change"),
        "notifications": ("view",),
    },
    ADMINISTRATOR: {
        "enquiries": ("view", "change", "delete", "add"),
        "rules": ("view",),
        "forum": ("view", "change", "add", "delete"),
        "news": ("view", "change", "add", "delete"),
        "faq": ("view", "change", "add", "delete"),
        "glossary": ("view", "change", "add", "delete"),
        "living": ("view", "change", "add", "delete"),
        "pathways": ("view", "change", "add", "delete"),
        "orientation": ("view", "change", "add"),
        "cms": ("view", "change", "add", "delete"),
        "partners": ("view", "change", "add", "delete"),
        "consents": ("view", "change", "add"),
        "notifications": ("view", "change"),
        # Model-scoped on purpose. Deleting a communication in the back office cascades to its
        # notification companion, and Django refuses the whole deletion unless the account may
        # delete the cascaded row too — so without this an administrator could not remove ANY
        # message that had been notified. The grant stops at the notification: the outbox keeps the
        # record of what was actually sent, and no role may erase that.
        "notifications.notification": ("delete",),
        "community": ("view", "change", "add", "delete"),
        "accounts": ("view", "change"),
        "audit": ("view",),
        "core": ("view", "change"),
        "legal": ("view", "change"),
        "documents": ("view",),
        "integrations": ("view",),
    },
}


def ensure_roles() -> int:
    created = 0
    for name in ALL_ROLES:
        group, was_created = Group.objects.get_or_create(name=name)
        created += int(was_created)
        perms = []
        for target, actions in ROLE_PERMISSIONS.get(name, {}).items():
            # "app" grants over the whole application; "app.model" over one model of it.
            app_label, _, model = target.partition(".")
            scope = {"content_type__app_label": app_label}
            if model:
                scope["content_type__model"] = model
            for action in actions:
                perms.extend(Permission.objects.filter(**scope, codename__startswith=f"{action}_"))
        group.permissions.set(perms)
    return created


def assign_role(user, role: str) -> None:
    clash = conflicting_role(roles_of(user), role)
    if clash is not None:
        raise IncompatibleRoles(
            _("Les rôles « %(a)s » et « %(b)s » ne peuvent pas être attribués au même compte.")
            % {"a": ROLE_LABELS[role], "b": ROLE_LABELS[clash]}
        )
    group, _created = Group.objects.get_or_create(name=role)
    user.groups.add(group)


def revoke_role(user, role: str, *, request=None, end_sessions: bool = True) -> None:
    """
    Withdraw a role, and end the account's open sessions.

    A revocation that takes effect at the next login is not a revocation: the session cookie already
    issued carries the access the role granted until it expires. Ending the sessions costs the person
    a re-login, which is the correct price for an authorisation that has been withdrawn.
    """
    group = Group.objects.filter(name=role).first()
    if not group:
        return
    user.groups.remove(group)
    if end_sessions:
        from accounts.services import revoke_sessions

        revoke_sessions(user, request=request, reason=f"role revoked: {role}")


def has_role(user, *roles: str) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=roles).exists()


def roles_of(user) -> set[str]:
    if not getattr(user, "is_authenticated", False):
        return set()
    return set(user.groups.filter(name__in=ALL_ROLES).values_list("name", flat=True))


def is_backoffice(user) -> bool:
    return has_role(user, *BACKOFFICE_ROLES)


def is_superadmin(user) -> bool:
    return bool(getattr(user, "is_superuser", False)) or has_role(user, SUPERADMIN)


def role_labels(user) -> list[str]:
    """Translated labels of the user's roles, in catalogue order (never the technical group names)."""
    owned = roles_of(user)
    return [str(ROLE_LABELS[name]) for name in ALL_ROLES if name in owned]
