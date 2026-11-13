"""Living sitemap — empty while gate G3 is closed (URLs must not be discoverable before 2 Oct 2026); afterwards the
index and only the themes that carry a live, reviewed sheet (V5.12 §8)."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates
from living import services
from living.models import LivingSheet


class LivingSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        if not gates.phase3_public():
            return []
        items: list[tuple[str, dict, object]] = [("living:index", {}, None)]
        # V5.12 §8: a theme is listed only with a live, reviewed sheet (services.public_topics); so is its sheet
        topics = list(services.public_topics())
        items += [("living:topic", {"slug": t.slug}, t.updated_at) for t in topics]
        items += [
            ("living:sheet", {"topic": s.topic.slug, "slug": s.slug}, s.last_reviewed_at or s.updated_at)
            for s in LivingSheet.objects.public().filter(topic__in=topics)
        ]
        return items

    def location(self, item):
        name, kwargs, _lastmod = item
        return reverse(name, kwargs=kwargs)

    def lastmod(self, item):
        return item[2]
