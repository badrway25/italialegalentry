"""The glossary (Phase 3, gate G3).

V5.22 (SECTION_SYSTEM_V2 §3.14; lane P2): the register is «il lessico» — one run of term cards, a letter's first card
carrying its letter (round 1, QA_ROUND1 M7), each with the pathways that name the term («Où le rencontrer»:
pathways.services.GLOSSARY_TERMS_BY_PATHWAY, read-only, inverted here; each pathway labelled with its prescribed
title); the term page's plate shows the same pathways, and its related terms disclose their definitions in place.
"""

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from core.links import public_url
from core.templatetags.ile_core import svg_icon
from glossary import services
from pathways.services import GENERAL_GLOSSARY_TERMS, GLOSSARY_TERMS_BY_PATHWAY, index_entries


def _lang() -> str:
    return translation.get_language() or settings.LANGUAGE_CODE


def where_to_meet(lang: str) -> dict[str, list[dict]]:
    """Term key → the pathways whose sheets name it (live sheets only: a chip is a link), each with its prescribed title
    (French on the other pages: it says so); a general term (the visa, the residence permit, the tax code — every
    pathway's) leads to the pathways' index instead. V5.27 / R7′ (the v524-pub2 steward): the title read by its sub-key
    in the page's language (``index_entries(lang=…)``: the provisional Arabic on /ar/), its ``lang`` when not the
    page's."""
    found: dict[str, list[dict]] = {}
    for entry in index_entries(lang=lang.split("-")[0]):
        if not entry.url:
            continue
        for key in GLOSSARY_TERMS_BY_PATHWAY.get(entry.key, ()):
            found.setdefault(key, []).append({"label": entry.title, "url": entry.url, "lang": entry.title_lang})
    index_url = public_url("pathways:index")
    if index_url:
        for key in GENERAL_GLOSSARY_TERMS:
            found.setdefault(key, []).append(
                {"label": _("Les parcours réguliers vers l’Italie"), "url": index_url, "lang": ""}
            )
    return found


def _lessico(groups, where: dict) -> list[dict]:
    """The register as ONE run of term cards, in the letters' order (round 1, QA_ROUND1 M7: eight letter groups held
    one or two cards each, a sparse column for ten terms); a letter's first card carries the letter, set large as its
    marker and as the anchor the thumb index reaches (#lettre-X)."""
    return [
        {"entry": entry, "chips": where.get(entry.key, []), "letter": group.letter if i == 0 else ""}
        for group in groups
        for i, entry in enumerate(group.entries)
    ]


def _related(entries) -> list[dict]:
    """The term page's related terms, their definitions disclosed in place (§1 rule 7: definitions behind glossary
    chips; §2 L «l'indice», the native exclusive disclosure): the Italian term the row, its prescribed definition whole
    and the way to its own page inside."""
    return [
        {
            "title": rel.term,
            "title_lang": rel.term_lang,
            "body": rel.definition,
            "body_lang": rel.lang if rel.is_fallback else "",
            "body_key": rel.definition_key,  # the caption's sub-key (V5.27 / R7′; "" for an editor's term)
            "links": format_html(
                '<a class="link-arrow" href="{}" lang="{}">{}{}</a>',
                rel.url,
                rel.term_lang,
                rel.term,
                svg_icon("arrow", "icon icon--sm"),
            ),
        }
        for rel in entries
    ]


def _rimando() -> list[dict]:
    """E «il rimando» (§3.14 G3): the FAQ, the pathways, the fraud page."""
    tiles = []
    for name, title, glyph in (
        ("faq:index", _("Questions fréquentes"), "circle-help"),
        ("pathways:index", _("Les parcours réguliers vers l’Italie"), "signpost"),
        ("pages:antifraud", _("Attention aux fraudes"), "ile-scudo"),
    ):
        url = public_url(name)
        if url:
            tiles.append({"href": url, "title": title, "glyph": glyph})
    return tiles


@require_safe
def index(request):
    visible, preview = services.page_visible(request)
    if not visible:
        raise Http404
    if not preview and not services.live_terms().exists():  # V5.12 §8: no «glossary in preparation» page
        raise Http404
    lang = _lang()
    query = services.normalise_query(request.GET.get("q"))
    if query:
        entries = services.entries_for(services.search_terms(query), lang)
        groups = services.letter_groups(entries)
        jsonld = ""
    else:
        entries = services.entries_for(services.live_terms(), lang)
        groups = services.letter_groups(entries)
        jsonld = services.render_jsonld(services.term_set_jsonld(entries, lang, request)) if entries else ""
    where = where_to_meet(lang)
    context = {
        "page_title": _("Glossaire"),
        "query": query,
        "is_search": bool(query),
        "entries": entries,
        "groups": groups,
        "letters": [g.letter for g in groups],
        "lessico": _lessico(groups, where),
        "results": [{"entry": e, "chips": where.get(e.key, [])} for e in entries] if query else [],
        "rimando": _rimando(),
        "glossary_jsonld": jsonld,
        "is_preview": preview,
        # Staff previews and search-result pages (unbounded URL space) are never indexed.
        "noindex": preview or bool(query),
        "breadcrumbs": [{"label": _("Glossaire"), "url": ""}],
    }
    return render(request, "glossary/index.html", context)


@require_safe
def term(request, slug: str):
    visible, preview = services.page_visible(request)
    if not visible:
        raise Http404
    term_obj = services.get_live_term(slug)
    if term_obj is None:
        raise Http404
    lang = _lang()
    entry = services.entry_for(term_obj, lang)
    set_url = request.build_absolute_uri(reverse("glossary:index"))
    related = services.related_entries(term_obj, lang)
    context = {
        "entry": entry,
        # the head's h1 takes the page's direction and holds the term as a run of its own language, so an Italian term
        # ends on the Arabic page's reading edge beside its seal (QA_ROUND2 M5: a lang="it" h1 was a left-to-right block
        # standing 592 px short of it)
        "title": format_html('<span lang="{}">{}</span>', entry.term_lang, entry.term)
        if entry.term_lang != lang
        else entry.term,
        "related": related,
        "related_items": _related(related),
        "where": where_to_meet(lang).get(entry.key, []),
        "term_jsonld": services.render_jsonld(services.term_jsonld(entry, request, set_url)),
        "is_preview": preview,
        "noindex": preview,
        "breadcrumbs": [
            {"label": _("Glossaire"), "url": reverse("glossary:index")},
            # the term is Italian by definition (or a published translation): tell the component
            {"label": entry.term, "url": "", "lang": entry.term_lang if entry.term_lang != lang else ""},
        ],
    }
    return render(request, "glossary/term.html", context)
