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
