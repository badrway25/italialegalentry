from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PartnersSitemap(Sitemap):
    """The partners index is an always-public page; individual partners have no detail page."""

    changefreq = "monthly"
    priority = 0.4
    i18n = True

    def items(self):
        return ["partners:index"]

    def location(self, item):
        return reverse(item)
