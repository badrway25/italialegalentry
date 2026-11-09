"""The FAQ (Phase 3, gate G3).

V5.22 (SECTION_SYSTEM_V2 §3.13; lane P2): the listing is an explorer (L «l'indice», master–detail from 64 rem): the
locked questions as the index, one answer plate beside it — the view hands the library's partial its items (the
question, the answer with its links as chips, its date and its permalink) and the foot «il rimando» its tiles. The
search's result list stays the system's disclosures, open.
"""

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from core.links import public_url
from faq import services

#: the fraud question carries the protection's mark and an ink rule at its reading edge (§3.13 Q1)
FRAUD_KEY = "faq_guaranteed_visa_offer"

#: V5.29 §10–§13 (lane PUB2): each prescribed question says its subject by one glyph of the registry
#: (apps/core/icons.py), drawn in the library's T2 tile (.sez-tile--sm, stream SYS) — never one icon twice
#: (tests/frontend/test_faq_v529_pub2.py). An editor's question outside the register draws no glyph.
GLYPHS = {
    "faq_visas": "stamp",  # the visa: an act of the competent authority
    "faq_recruitment_agency": "briefcase",  # work and its intermediaries
    "faq_preassessment_guarantee": "compass",  # eligibility / orientation
    "faq_decreto_flussi": "book-text",  # a legal source
    "faq_diplomas": "university",  # diplomas and their recognition
    "faq_prior_refusal": "signpost",  # the pathway after a refusal
    "faq_who": "institution",  # who stands behind the platform
    "faq_data_protection": "lock",  # security: the data under lock (no second shield beside fraud)
    FRAUD_KEY: "ile-scudo",  # fraud: the protection's own mark
}


def glyph(key: str) -> str:
    return GLYPHS.get(key, "")


def _url(name: str) -> str:
    """A cross-app link, empty when the page is gated shut (core.links.public_url: never a link to a 404)."""
    return public_url(name)


def _explorer_items(group, request) -> list[dict]:
    """The items of one category's explorer: the panel's id is the question's own key (the permalinks and the home's
    trust links keep landing on their question)."""
    items = []
    for entry in group.entries:
        items.append(
            {
                "id": entry.key,
                "title": entry.question,
                "title_lang": entry.question_lang if entry.question_is_fallback else "",
                "glyph": glyph(entry.key),
                "marked": entry.key == FRAUD_KEY,
                "body": render_to_string("faq/_risposta.html", {"entry": entry}, request),
                "links": render_to_string("faq/_collegamenti.html", {"entry": entry}, request) if entry.links else "",
            }
        )
    return items


def _rimando(request) -> list[dict]:
    """E «il rimando» (§3.13 Q2): the glossary, the fraud page and the help question, as compact tiles."""
    tiles = []
    glossary, antifraud, contact = _url("glossary:index"), _url("pages:antifraud"), _url("pages:contact")
    if glossary:
        tiles.append({"href": glossary, "title": _("Glossaire : les termes italiens expliqués"), "glyph": "book-a"})
    if antifraud:
        tiles.append({"href": antifraud, "title": _("Attention aux fraudes"), "glyph": "ile-scudo"})
    if contact:
        tiles.append(
            {
                "href": contact,
                "title": _("Vous n’avez pas trouvé de réponse ? Contactez-nous"),
                "glyph": "message-square-text",
            }
        )
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
    suggestions = []
    if query:
        entries = services.entries_for(services.search_items(query), lang)
        groups = []
        jsonld = ""
        if not entries:
            # V5.29 §13 (a strong empty search): every question stays one step away — the register's questions as
            # links to their permalinks, each with its glyph, beside the empty state
            suggestions = [
                {"entry": entry, "glyph": glyph(entry.key)}
                for entry in services.entries_for(services.live_items(), lang)
            ]
    else:
        entries = services.entries_for(services.live_items(), lang)
        groups = services.group_entries(entries, lang)
        jsonld = services.render_jsonld(services.faq_jsonld(entries, lang)) if entries else ""
    context = {
        "page_title": _("Questions fréquentes"),
        "query": query,
        "is_search": bool(query),
        "entries": entries,
        "results": [{"entry": entry, "glyph": glyph(entry.key)} for entry in entries] if query else [],
        "suggestions": suggestions,
        "groups": [{"group": g, "items": _explorer_items(g, request)} for g in groups],
        "single_group": len(groups) == 1,
        "rimando": _rimando(request),
        "faq_jsonld": jsonld,
        "is_preview": preview,
        # Staff previews and search-result pages (unbounded URL space) are never indexed.
        "noindex": preview or bool(query),
        "breadcrumbs": [{"label": _("Questions fréquentes"), "url": ""}],
    }
    return render(request, "faq/index.html", context)
