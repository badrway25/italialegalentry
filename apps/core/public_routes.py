"""
Registry of public, language-prefixed routes used by the compliance test-suite and by QA scripts.

Each app registers its public paths from ``AppConfig.ready()``::

    from core.public_routes import register_public_paths
    register_public_paths("forum", ["forum/", "forum/inscription/"])

Paths are relative to the language prefix (no leading slash). Only routes that must render 200
for anonymous visitors belong here. Gated routes may be registered with ``requires_gate`` so the
suite knows they legitimately 404/redirect while the gate is closed.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PublicRoute:
    app: str
    path: str
    requires_gate: str = ""
    expected_status: int = 200
    tags: tuple[str, ...] = field(default_factory=tuple)


_ROUTES: list[PublicRoute] = []


def register_public_paths(app: str, paths: list[str], requires_gate: str = "", tags: tuple[str, ...] = ()) -> None:
    for path in paths:
        route = PublicRoute(app, path.lstrip("/"), requires_gate, 200, tags)
        if route not in _ROUTES:
            _ROUTES.append(route)


def all_routes() -> list[PublicRoute]:
    return list(_ROUTES)


def ungated_paths() -> list[str]:
    return [r.path for r in _ROUTES if not r.requires_gate]


def gated_routes() -> list[PublicRoute]:
    return [r for r in _ROUTES if r.requires_gate]
