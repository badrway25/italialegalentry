from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class OrientationSitemap(Sitemap):
    """Only the public entry page; sessions are private and disallowed in robots.txt."""

    changefreq = "monthly"
    priority = 0.7
    i18n = True

    def items(self):
        return ["orientation:start"]

    def location(self, item):
        return reverse(item)
