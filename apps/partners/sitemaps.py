from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates


class PartnersSitemap(Sitemap):
    """The partners index, once a partner is authorised (core.gates.partners_public); partners have no detail page."""

    changefreq = "monthly"
    priority = 0.4
    i18n = True

    def items(self):
        return ["partners:index"] if gates.partners_public() else []

    def location(self, item):
        return reverse(item)
