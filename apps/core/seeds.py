"""
Seed registry. Each app may provide ``<app>/seeds.py`` with functions decorated by
``@register_seed("<app>.<name>", order=N)``. ``manage.py seed_all`` runs them in order.
Seeds must be idempotent (safe to run on every deploy) and must never overwrite editorial
changes to non-locked fields.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable
from dataclasses import dataclass

from django.apps import apps
from django.conf import settings

_REGISTRY: list[Seed] = []


@dataclass(frozen=True)
class Seed:
    name: str
    order: int
    func: Callable[[], object]


def register_seed(name: str, order: int = 100):
    def decorator(func):
        _REGISTRY.append(Seed(name, order, func))
        return func

    return decorator


def discover() -> list[Seed]:
    for app_config in apps.get_app_configs():
        module_name = f"{app_config.name}.seeds"
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            if exc.name != module_name:
                raise
    return sorted(_REGISTRY, key=lambda s: (s.order, s.name))


def demonstration_data_allowed() -> bool:
    """
    Whether a seed may create SYNTHETIC records that resemble real ones.

    Two kinds of seed are not the same thing, and conflating them is how a database ends up holding
    invented people:

    * **Configuration and published editorial content** — taxonomies, flags, menus, locked texts.
      Always seeded. They are the product.
    * **Demonstration records** — an account, a case file, a help-desk request, a training plan.
      Never seeded unless this returns True. They are invented, they are indistinguishable from real
      records once written, and the corrective directive forbids inventing data to make a screen look
      populated.

    The switch is its own setting rather than ``DEBUG`` so that an environment can keep DEBUG on for
    developer tooling and still refuse to manufacture people; it falls back to ``DEBUG`` so an
    existing configuration behaves as before.

    ``getattr`` with a default, not ``settings.ILE_SEED_DEMONSTRATION_DATA``: a test that overrides
    settings with ``@override_settings`` may remove it, and a seed that raises because a switch is
    absent fails the whole deployment over a question whose safe answer is "no".
    """
    return bool(getattr(settings, "ILE_SEED_DEMONSTRATION_DATA", settings.DEBUG))
