"""
Outbound event emission from domain models WITHOUT modifying their apps.

Receivers are connected lazily in ``IntegrationsConfig.ready()``; a model that does not exist yet
(sibling app still under construction) is skipped. Payloads carry ids, timestamps and closed
vocabulary codes only (contract §6) — never the form contents.
"""

from __future__ import annotations

import logging

from django.apps import apps
from django.db.models.signals import post_save

from integrations.services import PayloadRejected, emit

log = logging.getLogger("ile.integrations")

# (app_label.ModelName, event prefix). Event types: "<prefix>.created".
WATCHED_MODELS: tuple[tuple[str, str], ...] = (
    ("enquiries.CompanyNeedsRequest", "enquiries.company_needs"),
    ("enquiries.CollaborationProposal", "enquiries.collaboration_proposal"),
    ("forum.ForumRegistration", "forum.registration"),
)

# Attributes copied into the payload when present — short closed-vocabulary codes only.
CODE_ATTRIBUTES = ("category", "kind", "status", "language")
_PREFIX_BY_MODEL: dict[type, str] = {}


def minimal_payload(instance) -> dict:
    payload: dict = {}
    for attr in CODE_ATTRIBUTES:
        value = getattr(instance, attr, None)
        if isinstance(value, str) and value and len(value) <= 40 and "@" not in value:
            payload[attr] = value
    created_at = getattr(instance, "created_at", None)
    if created_at is not None:
        payload["created_at"] = created_at
    return payload


def on_watched_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    prefix = _PREFIX_BY_MODEL.get(sender)
    if not prefix:
        return
    try:
        emit(f"{prefix}.created", instance, minimal_payload(instance))
    except PayloadRejected as exc:  # pragma: no cover - defensive; minimal_payload already filters
        log.warning("outbound payload rejected for %s: %s", sender.__name__, exc)
    except Exception:  # noqa: BLE001 - integration failures must never break the domain save
        log.exception("outbound event emission failed for %s", sender.__name__)


def connect_receivers() -> list[str]:
    """Connect post_save receivers for the watched models that exist; return the connected labels."""
    connected: list[str] = []
    for label, prefix in WATCHED_MODELS:
        try:
            model = apps.get_model(label)
        except (LookupError, ValueError):
            log.info("integrations: model %s not available yet — receiver skipped", label)
            continue
        _PREFIX_BY_MODEL[model] = prefix
        post_save.connect(on_watched_post_save, sender=model, dispatch_uid=f"integrations.{label}", weak=False)
        connected.append(label)
    return connected
