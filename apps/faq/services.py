"""
FAQ services — every piece of logic used by the public view, the sitemap and the admin.

Public rendering rules
* only ``FAQItem.objects.live()`` rows are shown (status + scheduling window, ``core.clock``);
* locked items print the registry text (``cms.locked_content``), never the DB mirror;
* the requested language is served only from a PUBLISHED translation, otherwise the French
  source is rendered with an explicit ``lang="fr"`` (gate G10);
* the JSON-LD ``FAQPage`` block is emitted only for the full, non-search listing.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from cms.models import TranslationStatus
from cms.translation import resolve
from core import gates
from faq import registry
from faq.models import FAQCategory, FAQItem, FAQItemTranslation

MAX_QUERY_LENGTH = 100
_WS = re.compile(r"\s+")
# C0/C1 control characters (NUL included): PostgreSQL refuses NUL bytes in text parameters, and none
# of them is meaningful in a search query. Whitespace controls are normalised to spaces first.
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")

# Contextual links appended *after* a prescribed answer (never inside it). Labels are UI strings.
CONTEXT_LINKS: dict[str, tuple[tuple[str, str, dict], ...]] = {
    "faq_visas": ((_("Glossaire : « Visto d’ingresso »"), "glossary:term", {"slug": "visto_ingresso"}),),
    "faq_preassessment_guarantee": ((_("Commencer l’orientation"), "orientation:start", {}),),
    "faq_decreto_flussi": ((_("Glossaire : « Decreto flussi »"), "glossary:term", {"slug": "decreto_flussi"}),),
    "faq_diplomas": (
        (_("Diplômes et titres étrangers"), "pathways:diplomas", {}),
        (_("Glossaire : « Legalizzazione / Apostille »"), "glossary:term", {"slug": "legalizzazione_apostille"}),
    ),
    "faq_who": ((_("Le projet"), "pages:project", {}), (_("AGAMI"), "pages:agami", {})),
    "faq_data_protection": ((_("Lire la Privacy Policy"), "legal:privacy", {}),),
    "faq_guaranteed_visa_offer": ((_("Consulter « Attention aux fraudes »"), "pages:antifraud", {}),),
}


@dataclass(frozen=True)
class RelatedLink:
    label: str
    url: str


@dataclass(frozen=True)
class FAQEntry:
    item: FAQItem
    key: str
    question: str
    answer: str
    lang: str
    is_fallback: bool
    last_updated: dt.date
    links: tuple[RelatedLink, ...]


@dataclass(frozen=True)
class FAQGroup:
    category: FAQCategory
    name: str
    lang: str
    is_fallback: bool
    entries: tuple[FAQEntry, ...]


# --------------------------------------------------------------------------------------------
# Visibility (gate G3)
# --------------------------------------------------------------------------------------------
def page_visible(request) -> tuple[bool, bool]:
    """(visible, is_staff_preview). Public visitors get 404 while Phase 3 is closed."""
    if gates.phase3_public():
        return True, False
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated and user.is_staff:
        # a staff preview of unpublished content: the second-factor policy first (accounts.middleware)
        from accounts.middleware import require_second_factor

        require_second_factor(request)
        return True, True
    return False, False


# --------------------------------------------------------------------------------------------
# Queries
# --------------------------------------------------------------------------------------------
def live_items():
    return (
        FAQItem.objects.live()
        .select_related("category")
        .prefetch_related("translations", "category__translations")
        .order_by("category__order", "category_id", "order", "id")
    )


def normalise_query(raw: str | None) -> str:
    """Collapse whitespace, drop control characters (NUL would make PostgreSQL raise), cap the length."""
    if not raw:
        return ""
    return _CONTROL.sub("", _WS.sub(" ", raw)).strip()[:MAX_QUERY_LENGTH]


def search_items(query: str):
    """Server-side search: PostgreSQL full-text (French) ∪ substring match on FR source ∪ published translations."""
    query = normalise_query(query)
    if not query:
        return live_items()
    vector = SearchVector("question_fr", "answer_fr", config="french")
    fts = SearchQuery(query, config="french", search_type="websearch")
    matched: set[int] = set(FAQItem.objects.annotate(search=vector).filter(search=fts).values_list("pk", flat=True))
    matched |= set(
        FAQItem.objects.filter(Q(question_fr__icontains=query) | Q(answer_fr__icontains=query)).values_list(
            "pk", flat=True
        )
    )
    matched |= set(
        FAQItemTranslation.objects.filter(status=TranslationStatus.PUBLISHED)
        .filter(Q(question__icontains=query) | Q(answer__icontains=query))
        .values_list("master_id", flat=True)
    )
    return live_items().filter(pk__in=matched)


# --------------------------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------------------------
def _safe_reverse(name: str, kwargs: dict) -> str:
    from core.links import public_url

    return public_url(name, **(kwargs or {}))


def _glossary_term_is_live(slug: str) -> bool:
    """A contextual link to the glossary is only offered when the target term is live (no dead links)."""
    from glossary.services import link_map

    return slug in link_map()


def context_links(key: str) -> tuple[RelatedLink, ...]:
    links = []
    for label, url_name, kwargs in CONTEXT_LINKS.get(key, ()):
        if url_name == "glossary:term" and not _glossary_term_is_live(kwargs.get("slug", "")):
            continue
        url = _safe_reverse(url_name, kwargs)
        if url:
            links.append(RelatedLink(str(label), url))
    return tuple(links)


def entry_for(item: FAQItem, lang: str) -> FAQEntry:
    lang = (lang or settings.LANGUAGE_CODE).split("-")[0]
    fallback_lang = settings.CONTENT_FALLBACK_LANGUAGE
    if item.is_locked:
        # Prescribed wording comes from the registry, never from the (mirrored) DB columns.
        prescribed = item.registry_entry() or {"question": item.question_fr, "answer": item.answer_fr}
        question_src, answer_src = prescribed["question"], prescribed["answer"]
    else:
        question_src, answer_src = item.question_fr, item.answer_fr
    row, effective, _is_fb = resolve(item, lang)
    if row is not None and effective == lang and lang != fallback_lang:
        return FAQEntry(
            item, item.key, row.question, row.answer, lang, False, item.last_updated, context_links(item.key)
        )
    return FAQEntry(
        item,
        item.key,
        question_src,
        answer_src,
        fallback_lang,
        lang != fallback_lang,
        item.last_updated,
        context_links(item.key),
    )


def entries_for(items, lang: str) -> list[FAQEntry]:
    return [entry_for(item, lang) for item in items]


def category_name(category: FAQCategory, lang: str) -> tuple[str, str, bool]:
    lang = (lang or settings.LANGUAGE_CODE).split("-")[0]
    fallback_lang = settings.CONTENT_FALLBACK_LANGUAGE
    row, effective, _is_fb = resolve(category, lang)
    if row is not None and effective == lang and lang != fallback_lang:
        return row.name, lang, False
    return category.name_fr, fallback_lang, lang != fallback_lang


def group_entries(entries: list[FAQEntry], lang: str) -> list[FAQGroup]:
    buckets: dict[int, list[FAQEntry]] = {}
    categories: dict[int, FAQCategory] = {}
    for entry in entries:
        categories.setdefault(entry.item.category_id, entry.item.category)
        buckets.setdefault(entry.item.category_id, []).append(entry)
    groups = []
    for cat_id, cat_entries in buckets.items():
        category = categories[cat_id]
        name, name_lang, is_fb = category_name(category, lang)
        groups.append(FAQGroup(category, name, name_lang, is_fb, tuple(cat_entries)))
    groups.sort(key=lambda g: (g.category.order, g.category.pk))
    return groups


# --------------------------------------------------------------------------------------------
# Structured data (schema.org FAQPage) — only live items, only for the full listing
# --------------------------------------------------------------------------------------------
def faq_jsonld(entries: list[FAQEntry], lang: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": (lang or settings.LANGUAGE_CODE).split("-")[0],
        "mainEntity": [
            {
                "@type": "Question",
                "name": entry.question,
                "inLanguage": entry.lang,
                "acceptedAnswer": {"@type": "Answer", "text": entry.answer, "inLanguage": entry.lang},
            }
            for entry in entries
            if entry.item.is_live()
        ],
    }


def render_jsonld(data: dict) -> SafeString:
    """JSON safe to embed in a <script type="application/ld+json"> block (no </script> escape)."""
    dumped = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dumped = dumped.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(dumped)  # noqa: S308 - escaped above


# --------------------------------------------------------------------------------------------
# Registry helpers reused by seeds/tests
# --------------------------------------------------------------------------------------------
def locked_keys() -> list[str]:
    return registry.keys()


def latest_update() -> dt.date | None:
    from django.db.models import Max

    return FAQItem.objects.live().aggregate(m=Max("last_updated"))["m"]
