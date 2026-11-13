"""CMS seeds: menus, hero variants, banners and the media library (see seeds_media.py)."""

import contextlib
import importlib

from core.seeds import register_seed


@register_seed("cms.media", order=30)
def seed_media():
    with contextlib.suppress(ModuleNotFoundError):
        module = importlib.import_module("cms.seeds_media")
        return module.seed()
    return "no media seed module"


@register_seed("cms.team_translations", order=99)
def seed_team_translations():
    """The team's it/en/ar rows for the seeded reference data (V5.24 W2) — after the masters' seeds (pathways 40, faq
    40,
    orientation 60), so the rows find them on every environment the seeds run on."""
    from cms.management.commands.seed_team_translations import seed

    return seed()
