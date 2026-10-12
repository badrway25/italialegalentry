from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core import gates


class _IndexEntry:
    """Sentinel for the glossary index page inside the term list."""

    url_name = "glossary:index"

    def __str__(self) -> str:
        return self.url_name


INDEX_ENTRY = _IndexEntry()


class GlossarySitemap(Sitemap):
    """Glossary index + live term permalinks, in every language — only while gate G3 is open."""

    changefreq = "monthly"
    priority = 0.5
    i18n = True

    def items(self):
        if not gates.phase3_public():
            return []
        from glossary.services import live_terms

        return [INDEX_ENTRY, *live_terms()]

    def location(self, item):
        if item is INDEX_ENTRY:
            return reverse(item.url_name)
        return item.get_absolute_url()

    def lastmod(self, item):
        if item is INDEX_ENTRY:
            from django.db.models import Max

            from glossary.models import Term

            return Term.objects.live().aggregate(m=Max("updated_at"))["m"]
        return item.updated_at
