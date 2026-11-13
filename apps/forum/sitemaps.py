from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from forum import services


class ForumSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True

    def items(self):
        event = services.current_event()
        return [event] if event else []

    def location(self, obj):
        return reverse("forum:index")

    def lastmod(self, obj):
        return obj.updated_at
