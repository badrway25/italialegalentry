"""The FAQ (Phase 3, gate G3).

FINAL MICRO-PASS (9 Nov 2026, BRIEF §6 B1): the listing is one column of questions on the ground — the system's
disclosures, searchable as one types and filtered by theme (21st.dev «Searchable Question Index», id 37558, adapted:
templates/faq/index.html says how). The view hands the template each question with its theme and the themes' pills
with their counts; the live count's sentences are the template's (one per count the page can show, in the language's
plural forms); the search's result list stays the system's disclosures, open. The explorer (master–detail), V5.29's
glyph a question (GLYPHS) and the answer plate's seal left.
"""

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_safe

from core.links import public_url
from faq import services

#: the fraud question keeps the protection's one mark, bare at the question's size (§3.13 Q1; BRIEF §2.1: the fraud
#: warning, one per page)
FRAUD_KEY = "faq_guaranteed_visa_offer"

#: FINAL MICRO-PASS §6 B1: the nine prescribed questions grouped by subject for the page's thematic navigation while the
#: register has one category — a presentation map (key → theme), never a category of the model. The names are existing
#: catalogue strings; an editor's question outside the map shows under «Toutes» only. Two categories or more in the
#: register: the categories are the themes.
THEMES = (
    ("projet", gettext_lazy("Le projet"), ("faq_visas", "faq_recruitment_agency", "faq_who")),
    (
        "parcours",
        gettext_lazy("Parcours réguliers"),
        ("faq_preassessment_guarantee", "faq_decreto_flussi", "faq_diplomas", "faq_prior_refusal"),
    ),
    ("securite", gettext_lazy("Sécurité"), ("faq_data_protection", FRAUD_KEY)),
)


def _url(name: str) -> str:
    """A cross-app link, empty when the page is gated shut (core.links.public_url: never a link to a 404)."""
    return public_url(name)


def _themes(entries, groups) -> tuple[list[dict], dict[str, str]]:
    """The pills (key, name, lang, count) and each question's theme; no pill row under two themes."""
    if len(groups) > 1:
        themes = [
            {"key": g.category.anchor, "name": g.name, "lang": g.lang if g.is_fallback else "", "count": len(g.entries)}
            for g in groups
        ]
        of = {entry.key: g.category.anchor for g in groups for entry in g.entries}
        return themes, of
    keys = {entry.key for entry in entries}
    themes, of = [], {}
    for key, name, members in THEMES:
        present = [member for member in members if member in keys]
        if present:
            themes.append({"key": key, "name": name, "lang": "", "count": len(present)})
            of.update(dict.fromkeys(present, key))
    return (themes if len(themes) > 1 else []), of


def _rimando(request) -> list[dict]:
    """E «il rimando» (§3.13 Q2): the glossary and the fraud page, as compact tiles. V5.32 (lane D): the help question
    («Vous n'avez pas trouvé de réponse ?») is the guide column's foot (templates/faq/_aiuto.html) — said once."""
    tiles = []
    glossary, antifraud = _url("glossary:index"), _url("pages:antifraud")
    if glossary:
        tiles.append({"href": glossary, "title": _("Glossaire : les termes italiens expliqués"), "glyph": "book-a"})
    if antifraud:
        tiles.append({"href": antifraud, "title": _("Attention aux fraudes"), "glyph": "ile-scudo"})
    return tiles


@require_safe
def index(request):
    visible, preview = services.page_visible(request)
    if not visible:
        raise Http404
    if not preview and not services.live_items().exists():  # V5.12 §8: no «questions in preparation» page
        raise Http404
    lang = translation.get_language() or settings.LANGUAGE_CODE
    query = services.normalise_query(request.GET.get("q"))
    suggestions, themes, theme_of = [], [], {}
    if query:
        entries = services.entries_for(services.search_items(query), lang)
        jsonld = ""
        if not entries:
            # V5.29 §13 (a strong empty search): every question stays one step away — the register's questions as
            # links to their permalinks beside the empty state (FINAL MICRO-PASS §6 B1: words only, no glyph)
            suggestions = services.entries_for(services.live_items(), lang)
    else:
        entries = services.entries_for(services.live_items(), lang)
        themes, theme_of = _themes(entries, services.group_entries(entries, lang))
        jsonld = services.render_jsonld(services.faq_jsonld(entries, lang)) if entries else ""
    context = {
        "page_title": _("Questions fréquentes"),
        "query": query,
        "is_search": bool(query),
        "entries": entries,
        "items": [
            {"entry": entry, "theme": theme_of.get(entry.key, ""), "marked": entry.key == FRAUD_KEY}
            for entry in entries
        ],
        "themes": themes,
        "suggestions": suggestions,
        "contact_url": _url("pages:contact"),
        "rimando": _rimando(request),
        "faq_jsonld": jsonld,
        "is_preview": preview,
        # Staff previews and search-result pages (unbounded URL space) are never indexed.
        "noindex": preview or bool(query),
        "breadcrumbs": [{"label": _("Questions fréquentes"), "url": ""}],
    }
    return render(request, "faq/index.html", context)
