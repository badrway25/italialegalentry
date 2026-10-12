from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from legal.models import LEGAL_URL_NAMES, LegalDocument, LegalStatus


class LegalSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3
    i18n = True

    def items(self):
        return list(LegalDocument.objects.filter(status=LegalStatus.PUBLISHED).exclude(body_it=""))

    def location(self, obj):
        return reverse(LEGAL_URL_NAMES[obj.kind])

    def lastmod(self, obj):
        return obj.published_at
