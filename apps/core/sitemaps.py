"""
Sitemap registry. Apps register their Sitemap classes from ``AppConfig.ready()``::

    from core.sitemaps import register
    register("news", NewsSitemap)

Only *published* and *gated-open* content must be listed by each sitemap.
"""

from __future__ import annotations

from django.contrib.sitemaps import Sitemap

SITEMAPS: dict[str, type[Sitemap] | Sitemap] = {}


def register(name: str, sitemap: type[Sitemap] | Sitemap) -> None:
    SITEMAPS[name] = sitemap
