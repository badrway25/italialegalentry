"""
Ecosystem seeds — idempotent, safe on every deploy.

* ``ecosystem.spaces`` — the four editorial rows. The Espace Entreprises (Phase 1) is PUBLISHED; the
  three Phase 3 spaces are SCHEDULED for 2 October 2026 (their routes stay behind gate G3 anyway).
  An existing row is never overwritten: the photograph is only filled in while the row has never
  been edited (``version == 1``) and still has none — e.g. when the media library was seeded later.
* ``ecosystem.pilot_steps`` — mirror of the prescribed sequence ``p3.pilot.sequence``. Only the locked
  columns are re-synchronised from the registry; editorial additions are never touched.
"""

from __future__ import annotations

import datetime as dt

from django.conf import settings

from cms.models import MediaAsset, PublicationStatus
from core.seeds import register_seed
from ecosystem import services
from ecosystem.models import EcosystemSpace, PilotStep, pilot_sequence, required_gate

# Implementation document p.7: « PHASE 3 — Après le 2 octobre 2026 ».
PHASE3_PUBLISH_AT = dt.datetime(2026, 10, 2, 0, 0, tzinfo=settings.ROME)
SPACE_EDITORIAL_NOTE = "Riga editoriale iniziale (seed) — i testi della pagina provengono dal registro bloccato"


def asset_for_slot(slot: str) -> MediaAsset | None:
    """The curated photo of a usage slot (natural key of a media asset = its source URL)."""
    entry = services.manifest_entry_for_slot(slot)
    if entry is None:
        return None
    return MediaAsset.objects.filter(source_url=entry["source_url"]).order_by("pk").first()


@register_seed("ecosystem.spaces", order=60)
def seed_spaces() -> str:
    created = images = 0
    for spec in services.SPACES.values():
        space = EcosystemSpace.objects.filter(key=spec.key).first()
        if space is None:
            gated = bool(required_gate(spec.key))
            EcosystemSpace.objects.create(
                key=spec.key,
                order=spec.order,
                hero_image=asset_for_slot(spec.photo_slot),
                status=PublicationStatus.SCHEDULED if gated else PublicationStatus.PUBLISHED,
                publish_at=PHASE3_PUBLISH_AT if gated else None,
                editorial_note=SPACE_EDITORIAL_NOTE,
            )
            created += 1
            continue
        if space.hero_image_id is None and space.version <= 1:
            asset = asset_for_slot(spec.photo_slot)
            if asset is not None:
                space.hero_image = asset
                space.save()
                images += 1
    return f"{created} ecosystem space(s) created, {images} photograph(s) attached, {len(services.SPACES)} total"


@register_seed("ecosystem.pilot_steps", order=61)
def seed_pilot_steps() -> str:
    created = resynced = 0
    sequence = pilot_sequence()
    for index, label in enumerate(sequence, start=1):
        step = PilotStep.objects.filter(locked_index=index).first()
        if step is None:
            PilotStep.objects.create(order=index, locked_index=index, label_fr=label, is_locked=True)
            created += 1
            continue
        if not step.is_locked or step.label_fr != label or step.order != index or not step.is_visible:
            step.is_locked = True
            step.save()  # save() re-asserts the registry wording and position
            resynced += 1
    return f"{created} prescribed pilot step(s) created, {resynced} re-synchronised, {len(sequence)} total locked"
