"""
Pages seeds — idempotent (safe on every deploy).

* ``pages.home_hero``: the two ``cms.HomeHero`` variants. The interim hero is editorial and carries
  no Phase 3 sentence; its body is a *reference* to a Phase 1 prescribed fragment
  (``locked:p1.persons.replacement_1``), resolved through the locked registry at render time.
  The Phase 3 variant stores no text at all: ``p3.hero.*`` come from the registry, behind gate G3.
* ``pages.home_sections``: the eleven homepage sections in the prescribed order (master brief §21).

Existing rows are never overwritten: editors own order, activation, headings and introductions.
"""

from __future__ import annotations

from django.conf import settings

from cms.models import HeroVariant, HomeHero, PublicationStatus
from core.seeds import register_seed
from pages import content, services
from pages.models import HomeSection


def _hero_image():
    return services.asset_for_slot("hero")


@register_seed("pages.home_hero", order=50)
def seed_home_hero() -> str:
    image = _hero_image()
    plans = (
        (HeroVariant.INTERIM, content.HERO_INTERIM, {"status": PublicationStatus.PUBLISHED}),
        (
            HeroVariant.PHASE3,
            content.HERO_PHASE3,
            {"status": PublicationStatus.SCHEDULED, "publish_at": settings.ILE["PHASE3_DATE"]},
        ),
    )
    created = 0
    for variant, texts, publication in plans:
        defaults = {name: services.str_source(value) for name, value in texts.items()}
        defaults.update(publication)
        defaults["image"] = image
        defaults["editorial_note"] = "Seed initial — pages.seeds"
        row, was_created = HomeHero.objects.get_or_create(variant=variant, defaults=defaults)
        created += int(was_created)
        if not was_created and row.image_id is None and image is not None:
            # Only fills a missing photo (e.g. media library seeded after the hero); never replaces a choice.
            HomeHero.objects.filter(pk=row.pk, image__isnull=True).update(image=image)
    return f"{created} hero variant(s) created, 2 ensured"


@register_seed("pages.home_sections", order=51)
def seed_home_sections() -> str:
    created = 0
    for default in content.SECTION_DEFAULTS:
        _row, was_created = HomeSection.objects.get_or_create(
            key=default.key,
            defaults={
                "order": default.order,
                "is_enabled": True,
                "requires_gate": default.requires_gate,
                "heading_fr": services.str_source(default.heading),
                "intro_fr": services.str_source(default.intro),
                "note_fr": services.str_source(default.note),
                "status": PublicationStatus.PUBLISHED,
                "editorial_note": "Seed initial — pages.seeds",
            },
        )
        created += int(was_created)
    return f"{created} homepage section(s) created, {len(content.SECTION_DEFAULTS)} ensured"
