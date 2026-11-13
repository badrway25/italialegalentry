from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates


class FAQSitemap(Sitemap):
    """Lists the FAQ page in every language — only while gate G3 (Phase 3) is open."""

    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        if not gates.phase3_public():
            return []
        return ["faq:index"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        from faq.services import latest_update

        return latest_update()
