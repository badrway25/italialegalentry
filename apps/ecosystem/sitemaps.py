from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from ecosystem import services


class EcosystemSitemap(Sitemap):
    """The four spaces. Gated pages are listed only while their gate is open (G3)."""

    changefreq = "monthly"
    priority = 0.8
    i18n = True

    def items(self):
        return [spec.key for spec in services.SPACES.values() if services.gate_open(spec.key)]

    def location(self, item):
        return reverse(services.SPACES[item].url_name)

    def lastmod(self, item):
        space = services.get_space(item)
        return space.updated_at if space else None
