"""
Authentication and authorisation events in the audit trail.

The Technical Blueprint (§13) lists "registrazione di accessi, download, modifiche e decisioni" and
REQ-SEC-06 puts security events of authentication first. Before this module the coverage of that
requirement was zero: the audit trail recorded what people did with objects, and nothing at all
about who signed in, who failed to, and who was granted a role.

Failed logins carry NO identifier. The submitted address is often a real person's e-mail typed by
someone else, sometimes a password typed into the wrong field: storing it would build a list of
credentials-adjacent personal data in the name of security. What matters for detecting an attack is
the rate and the origin, so the event records the hashed client IP that ``audit.services.record``
already computes, and nothing more.
"""

from __future__ import annotations

from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from audit.services import record


def on_user_logged_in(sender, request, user, **kwargs) -> None:
    record(request, action="auth.login", actor=user, target=user)


def on_user_logged_out(sender, request, user, **kwargs) -> None:
    if user is not None:
        record(request, action="auth.logout", actor=user, target=user)


def on_user_login_failed(sender, credentials, request=None, **kwargs) -> None:
    # Deliberately no credentials, not even the submitted address: see the module docstring.
    record(request, action="auth.login_failed")


@receiver(m2m_changed, dispatch_uid="audit.role_changed")
def on_role_changed(sender, instance, action, reverse, model, pk_set, **kwargs) -> None:
    """Any grant or revocation of a group, whatever the entry point (admin, shell, services)."""
    if action not in {"post_add", "post_remove", "post_clear"}:
        return
    if model is not Group and not isinstance(instance, Group):
        return

    if isinstance(instance, Group):
        # Reverse side: group.user_set.add(user, ...)
        group_names = [instance.name]
        targets = list(model.objects.filter(pk__in=pk_set or [])) if pk_set else []
        for target in targets:
            record(
                action="auth.role_granted" if action == "post_add" else "auth.role_revoked",
                target=target,
                metadata={"roles": group_names},
            )
        return

    names = list(Group.objects.filter(pk__in=pk_set or []).values_list("name", flat=True)) if pk_set else []
    if action == "post_clear":
        record(action="auth.role_revoked", target=instance, metadata={"roles": ["<all>"]})
        return
    if not names:
        return
    record(
        action="auth.role_granted" if action == "post_add" else "auth.role_revoked",
        target=instance,
        metadata={"roles": names},
    )
