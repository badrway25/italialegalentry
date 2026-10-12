from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates

ALWAYS_PUBLIC = ("pages:home", "pages:project", "pages:agami", "pages:network", "pages:contact")
PHASE3_ONLY = ("pages:antifraud",)


class PagesSitemap(Sitemap):
    """Homepage + institutional pages; the anti-fraud page is listed only while gate G3 is open."""

    changefreq = "weekly"
    i18n = True

    def items(self):
        names = list(ALWAYS_PUBLIC)
        if gates.phase3_public():
            names += list(PHASE3_ONLY)
        return names

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "pages:home" else 0.6
