"""Mirror django.contrib.admin LogEntry rows into the project audit trail."""

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.db.models.signals import post_save
from django.dispatch import receiver

from audit.models import AuditEvent

_ACTIONS = {ADDITION: "admin.add", CHANGE: "admin.change", DELETION: "admin.delete"}


@receiver(post_save, sender=LogEntry)
def mirror_admin_log(sender, instance: LogEntry, created: bool, **kwargs):
    if not created:
        return
    AuditEvent.objects.create(
        actor=instance.user,
        actor_label=str(instance.user),
        action=_ACTIONS.get(instance.action_flag, "admin.other"),
        target_type=instance.content_type.model if instance.content_type else "",
        target_id=str(instance.object_id or ""),
        target_repr=(instance.object_repr or "")[:200],
        metadata={"change_message": instance.get_change_message()[:500]},
    )
