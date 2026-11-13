from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class EnquiriesSitemap(Sitemap):
    """Public form pages (Phase 1 company needs, collaboration proposals) — no gated URLs.

    V5.32 (integration review P2-14): the contact form's own route (enquiries:contact, /contact/formulaire/) is no
    page of its own any more — the contact page (pages:contact, in the pages sitemap) carries the form; the route
    stays the form's POST and re-render address, linked by no page, so it is not listed.
    """

    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        return [
            "enquiries:company_needs",
            "enquiries:institution_proposal",
            "enquiries:university_proposal",
        ]

    def location(self, item):
        return reverse(item)
