from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class EnquiriesSitemap(Sitemap):
    """Public form pages (Phase 1 company needs, collaboration proposals, contact) — no gated URLs."""

    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        return [
            "enquiries:company_needs",
            "enquiries:institution_proposal",
            "enquiries:university_proposal",
            "enquiries:contact",
        ]

    def location(self, item):
        return reverse(item)
