from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditEvent(models.Model):
    """Append-only administrative / security audit trail. Never edited, never deleted from the UI."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_events"
    )
    actor_label = models.CharField(max_length=160, blank=True)
    action = models.CharField(max_length=80, db_index=True)
    target_type = models.CharField(max_length=80, blank=True, db_index=True)
    target_id = models.CharField(max_length=64, blank=True)
    target_repr = models.CharField(max_length=200, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_hash = models.CharField(max_length=32, blank=True)
    request_id = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("evento di audit")
        verbose_name_plural = _("audit trail")
        indexes = [models.Index(fields=["target_type", "target_id"])]

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.action} {self.target_repr}"
