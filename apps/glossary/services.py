"""
Glossary services — logic for the public index/permalink pages, the sitemap, the admin and the
``{% glossary_link %}`` template tag.

Public rendering rules mirror the FAQ: only ``Term.objects.live()`` rows; locked terms print the
registry text; PUBLISHED translations only, otherwise French source with ``lang="fr"`` (G10);
JSON-LD ``DefinedTermSet`` only for the full listing, ``DefinedTerm`` on permalinks.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.cache import cache
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe
from django.utils.text import Truncator

from cms.models import TranslationStatus
from cms.translation import resolve
from core import gates
from glossary import registry
from glossary.models import Term, TermTranslation, initial_letter

MAX_QUERY_LENGTH = 100
LINK_MAP_CACHE_KEY = "glossary.link_map"
LINK_MAP_TTL = 60
SHORT_DEFINITION_CHARS = 160
_WS = re.compile(r"\s+")
# C0/C1 control characters (NUL included): PostgreSQL refuses NUL bytes in text parameters, and none
# of them is meaningful in a search query. Whitespace controls are normalised to spaces first.
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")


@dataclass(frozen=True)
class GlossaryEntry:
    term_obj: Term
    key: str
    term: str
    term_lang: str
    definition: str
    lang: str
    is_fallback: bool
    url: str
    initial: str
    source: str
    last_reviewed_at: dt.datetime | None


@dataclass(frozen=True)
class LetterGroup:
    letter: str
    entries: tuple[GlossaryEntry, ...]


@dataclass(frozen=True)
class LinkTarget:
    key: str
    term: str
    short_definition: str


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
def live_terms():
    return Term.objects.live().prefetch_related("translations").order_by("term", "id")


def get_live_term(key: str) -> Term | None:
    return live_terms().filter(key=key).first()


def normalise_query(raw: str | None) -> str:
    """Collapse whitespace, drop control characters (NUL would make PostgreSQL raise), cap the length."""
    if not raw:
        return ""
    return _CONTROL.sub("", _WS.sub(" ", raw)).strip()[:MAX_QUERY_LENGTH]


def search_terms(query: str):
    query = normalise_query(query)
    if not query:
        return live_terms()
    vector = SearchVector("term", "definition_fr", config="french")
    fts = SearchQuery(query, config="french", search_type="websearch")
    matched: set[int] = set(Term.objects.annotate(search=vector).filter(search=fts).values_list("pk", flat=True))
    matched |= set(
        Term.objects.filter(
            Q(term__icontains=query) | Q(definition_fr__icontains=query) | Q(key__icontains=query.replace(" ", "_"))
        ).values_list("pk", flat=True)
    )
    matched |= set(
        TermTranslation.objects.filter(status=TranslationStatus.PUBLISHED)
        .filter(Q(term__icontains=query) | Q(definition__icontains=query))
        .values_list("master_id", flat=True)
    )
    return live_terms().filter(pk__in=matched)


# --------------------------------------------------------------------------------------------
# Presentation
# --------------------------------------------------------------------------------------------
def prescribed_texts(term: Term) -> tuple[str, str]:
    """(term label, French definition) — from the registry for locked rows, else from the DB."""
    if term.is_locked:
        entry = term.registry_entry()
        if entry is not None:
            return entry["term"], entry["definition"]
    return term.term, term.definition_fr


def entry_for(term: Term, lang: str) -> GlossaryEntry:
    lang = (lang or settings.LANGUAGE_CODE).split("-")[0]
    fallback_lang = settings.CONTENT_FALLBACK_LANGUAGE
    label, definition_fr = prescribed_texts(term)
    row, effective, _is_fb = resolve(term, lang)
    url = term.get_absolute_url()
    if row is not None and effective == lang and lang != fallback_lang:
        term_label = row.term.strip() or label
        term_lang = lang if row.term.strip() else "it"
        return GlossaryEntry(
            term,
            term.key,
            term_label,
            term_lang,
            row.definition,
            lang,
            False,
            url,
            initial_letter(label),
            term.source,
            term.last_reviewed_at,
        )
    return GlossaryEntry(
        term,
        term.key,
        label,
        "it",
        definition_fr,
        fallback_lang,
        lang != fallback_lang,
        url,
        initial_letter(label),
        term.source,
        term.last_reviewed_at,
    )


def entries_for(terms, lang: str) -> list[GlossaryEntry]:
    return [entry_for(term, lang) for term in terms]


def letter_groups(entries: list[GlossaryEntry]) -> list[LetterGroup]:
    buckets: dict[str, list[GlossaryEntry]] = {}
    for entry in entries:
        buckets.setdefault(entry.initial, []).append(entry)
    groups = []
    for letter in sorted(buckets):
        ordered = sorted(buckets[letter], key=lambda e: (e.term.casefold(), e.key))
        groups.append(LetterGroup(letter, tuple(ordered)))
    return groups


def related_entries(term: Term, lang: str) -> list[GlossaryEntry]:
    related = term.related.live().prefetch_related("translations").order_by("term", "id")
    return entries_for(related, lang)


# --------------------------------------------------------------------------------------------
# Structured data (schema.org) — sober: name, description, url only
# --------------------------------------------------------------------------------------------
def _absolute(request, path: str) -> str:
    return request.build_absolute_uri(path) if request is not None else path


def term_jsonld(entry: GlossaryEntry, request=None, set_url: str = "") -> dict:
    data = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": entry.term,
        "description": entry.definition,
        "inLanguage": entry.lang,
        "url": _absolute(request, entry.url),
    }
    if set_url:
        data["inDefinedTermSet"] = set_url
    return data


def term_set_jsonld(entries: list[GlossaryEntry], lang: str, request=None) -> dict:
    set_url = _absolute(request, reverse("glossary:index"))
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": f"{settings.ILE['PROJECT_NAME']} — Glossaire",
        "inLanguage": (lang or settings.LANGUAGE_CODE).split("-")[0],
        "url": set_url,
        "hasDefinedTerm": [
            {k: v for k, v in term_jsonld(entry, request).items() if k != "@context"}
            for entry in entries
            if entry.term_obj.is_live()
        ],
    }


def render_jsonld(data: dict) -> SafeString:
    dumped = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dumped = dumped.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(dumped)  # noqa: S308 - escaped above


# --------------------------------------------------------------------------------------------
# Contextual links ({% glossary_link %}) — cached map of live terms, invalidated on save/delete
# --------------------------------------------------------------------------------------------
def link_map() -> dict[str, LinkTarget]:
    cached = cache.get(LINK_MAP_CACHE_KEY)
    if cached is not None:
        return cached
    mapping: dict[str, LinkTarget] = {}
    for term in Term.objects.live().only(
        "key", "term", "definition_fr", "is_locked", "status", "publish_at", "unpublish_at"
    ):
        label, definition = prescribed_texts(term)
        short = Truncator(definition).chars(SHORT_DEFINITION_CHARS)
        mapping[term.key] = LinkTarget(term.key, label, short)
    cache.set(LINK_MAP_CACHE_KEY, mapping, LINK_MAP_TTL)
    return mapping


def invalidate_link_map() -> None:
    cache.delete(LINK_MAP_CACHE_KEY)


def link_target(key: str) -> LinkTarget | None:
    """Target for an inline glossary link, or None when the glossary is not publicly reachable."""
    if not gates.phase3_public():
        return None
    return link_map().get(key)


# --------------------------------------------------------------------------------------------
# Registry helpers
# --------------------------------------------------------------------------------------------
def locked_keys() -> list[str]:
    return registry.keys()
