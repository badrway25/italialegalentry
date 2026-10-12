from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates
from pathways.models import Pathway


class PathwaysSitemap(Sitemap):
    """Espace Personnes URLs. Gated pages are listed only while Phase 3 is public (gate G3)."""

    changefreq = "monthly"
    priority = 0.7
    i18n = True

    def items(self):
        items: list = ["pathways:index"]
        if gates.phase3_public():
            items += ["pathways:diplomas", "pathways:training"]
            items += list(Pathway.objects.live().ordered())
        return items

    def location(self, item):
        if isinstance(item, str):
            return reverse(item)
        return item.get_absolute_url()

    def lastmod(self, item):
        if isinstance(item, str):
            return None
        return item.last_reviewed_at or item.updated_at
