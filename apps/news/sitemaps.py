from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from news.models import Article


class NewsIndexSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    i18n = True

    def items(self):
        return ["news:index"]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    """Published (live) articles only — drafts, reviews and future-scheduled items never appear."""

    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        return list(Article.objects.public())

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_modified
