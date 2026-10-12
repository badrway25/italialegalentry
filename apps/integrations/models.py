"""
CRM / external-system integration boundary (docs/CRM_INTEGRATION_CONTRACT.md).

* ``ExternalSystem``      — a registered counterpart (CRM, partner platform). Secrets are NEVER stored
                             in clear: the row holds the *name* of the environment variable plus a
                             SHA-256 fingerprint used to detect misconfiguration.
* ``ExternalReference``   — mapping local object ↔ external id with sync status.
* ``OutboundEvent``       — idempotent, minimal-payload events queued for delivery (push through a
                             transport, or pull + ack through the API).
* ``WebhookEndpoint``     — where a push transport would deliver; inactive by default.
* ``InboundWebhookLog``   — every inbound call with its verification result (replay protection).
* ``ApiKey``              — hashed bearer keys with scopes for the versioned API.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import clock
from core.models import TimeStampedModel


class HttpsURLField(models.URLField):
    """URLField whose admin form assumes https (silences the Django 6.0 scheme deprecation)."""

    def formfield(self, **kwargs):
        kwargs.setdefault("assume_scheme", "https")
        return super().formfield(**kwargs)


class ExternalSystem(TimeStampedModel):
    key = models.SlugField(_("chiave"), max_length=40, unique=True)
    name = models.CharField(_("nome"), max_length=120)
    is_active = models.BooleanField(_("attivo"), default=True)
    inbound_secret_env = models.CharField(
        _("variabile d'ambiente del segreto (webhook in ingresso)"),
        max_length=80,
        blank=True,
        help_text=_("Nome della variabile d'ambiente che contiene il segreto condiviso HMAC. Mai il valore."),
    )
    inbound_secret_hash = models.CharField(
        _("impronta SHA-256 del segreto"),
        max_length=64,
        blank=True,
        help_text=_("sha256(segreto) in esadecimale: serve solo a verificare che l'ambiente sia configurato."),
    )
    note = models.CharField(_("nota"), max_length=255, blank=True)

    class Meta:
        ordering = ["key"]
        verbose_name = _("sistema esterno")
        verbose_name_plural = _("sistemi esterni")

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"


class SyncStatus(models.TextChoices):
    PENDING = "pending", _("In attesa")
    SYNCED = "synced", _("Sincronizzato")
    ERROR = "error", _("Errore")


class ExternalReference(TimeStampedModel):
    system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, related_name="references")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    target = GenericForeignKey("content_type", "object_id")
    external_id = models.CharField(_("id esterno"), max_length=120)
    sync_status = models.CharField(
        _("stato di sincronizzazione"),
        max_length=10,
        choices=SyncStatus.choices,
        default=SyncStatus.PENDING,
        db_index=True,
    )
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["system", "content_type", "object_id"], name="uniq_external_reference"),
        ]
        indexes = [models.Index(fields=["system", "external_id"])]
        verbose_name = _("riferimento esterno")
        verbose_name_plural = _("riferimenti esterni")

    def __str__(self) -> str:
        return f"{self.system.key}:{self.external_id} ↔ {self.content_type.model}:{self.object_id}"


class OutboundEventStatus(models.TextChoices):
    QUEUED = "queued", _("In coda")
    DELIVERED = "delivered", _("Consegnato")
    FAILED = "failed", _("Fallito")
    CANCELLED = "cancelled", _("Annullato")


class OutboundEvent(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    event_type = models.CharField(_("tipo di evento"), max_length=80, db_index=True)
    system = models.ForeignKey(
        ExternalSystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name=_("sistema destinatario"),
        help_text=_("Vuoto = evento disponibile a tutti i sistemi attivi."),
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.CharField(max_length=64, blank=True)
    occurred_at = models.DateTimeField(_("avvenuto il"), default=clock.now, db_index=True)
    payload = models.JSONField(_("payload (minimo, senza dati personali)"), default=dict, blank=True)
    idempotency_key = models.CharField(_("chiave di idempotenza"), max_length=160, unique=True)
    status = models.CharField(
        _("stato"),
        max_length=10,
        choices=OutboundEventStatus.choices,
        default=OutboundEventStatus.QUEUED,
        db_index=True,
    )
    attempts = models.PositiveSmallIntegerField(_("tentativi"), default=0)
    next_attempt_at = models.DateTimeField(_("prossimo tentativo"), null=True, blank=True, db_index=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        "integrations.ApiKey", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    response_code = models.SmallIntegerField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "next_attempt_at"])]
        verbose_name = _("evento in uscita")
        verbose_name_plural = _("eventi in uscita (outbox)")

    def __str__(self) -> str:
        return f"{self.event_type} [{self.status}] {self.uuid}"

    @property
    def object_type(self) -> str:
        if not self.content_type_id:
            return ""
        return f"{self.content_type.app_label}.{self.content_type.model}"


class WebhookEndpoint(TimeStampedModel):
    system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, related_name="endpoints")
    url = HttpsURLField(_("URL di destinazione"), max_length=500)
    signing_secret_env = models.CharField(
        _("variabile d'ambiente del segreto di firma"),
        max_length=80,
        blank=True,
        help_text=_("Nome della variabile d'ambiente con il segreto HMAC per firmare le consegne. Mai il valore."),
    )
    secret_hash = models.CharField(_("impronta SHA-256 del segreto"), max_length=64, blank=True)
    event_types = models.JSONField(
        _("tipi di evento"), default=list, blank=True, help_text=_("Lista vuota = tutti gli eventi.")
    )
    is_active = models.BooleanField(
        _("attivo"),
        default=False,
        help_text=_("Nessuna chiamata HTTP viene effettuata finché INTEGRATIONS_TRANSPORT non è configurato."),
    )
    last_delivery_at = models.DateTimeField(null=True, blank=True)
    last_status_code = models.SmallIntegerField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        ordering = ["system", "url"]
        verbose_name = _("endpoint webhook (uscita)")
        verbose_name_plural = _("endpoint webhook (uscita)")

    def __str__(self) -> str:
        return f"{self.system.key} → {self.url}"

    def accepts(self, event_type: str) -> bool:
        return not self.event_types or event_type in self.event_types


class InboundWebhookLog(TimeStampedModel):
    system = models.ForeignKey(
        ExternalSystem, on_delete=models.SET_NULL, null=True, blank=True, related_name="inbound_logs"
    )
    system_key = models.CharField(max_length=40, blank=True)
    nonce = models.CharField(max_length=64, blank=True)
    timestamp = models.CharField(max_length=32, blank=True)
    signature_valid = models.BooleanField(default=False, db_index=True)
    status_code = models.PositiveSmallIntegerField(default=0)
    event_type = models.CharField(max_length=80, blank=True)
    payload = models.JSONField(default=dict, blank=True, help_text=_("Solo identificativi (dati minimizzati)."))
    error = models.CharField(max_length=160, blank=True)
    request_id = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["system", "nonce"],
                condition=models.Q(signature_valid=True),
                name="uniq_inbound_webhook_nonce",
            ),
        ]
        verbose_name = _("webhook in ingresso")
        verbose_name_plural = _("webhook in ingresso (log)")

    def __str__(self) -> str:
        return f"{self.system_key} {self.status_code} {self.created_at:%Y-%m-%d %H:%M}"


class ApiScope(models.TextChoices):
    EVENTS_READ = "events:read", _("Lettura eventi")
    EVENTS_ACK = "events:ack", _("Conferma (ack) eventi")


class ApiKey(TimeStampedModel):
    name = models.CharField(_("nome"), max_length=120)
    prefix = models.CharField(max_length=16, db_index=True, editable=False)
    key_hash = models.CharField(max_length=64, unique=True, editable=False)
    scopes = models.JSONField(_("scope"), default=list, blank=True)
    system = models.ForeignKey(
        ExternalSystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="api_keys",
        help_text=_("Se impostato, la chiave vede solo gli eventi destinati a questo sistema (o a tutti)."),
    )
    is_active = models.BooleanField(_("attiva"), default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("chiave API")
        verbose_name_plural = _("chiavi API")

    def __str__(self) -> str:
        return f"{self.name} (ile_{self.prefix}_…)"

    def has_scope(self, scope: str) -> bool:
        return scope in (self.scopes or [])

    @property
    def is_valid(self) -> bool:
        if not self.is_active:
            return False
        return not (self.expires_at and self.expires_at <= clock.now())
