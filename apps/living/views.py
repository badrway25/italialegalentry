"""Thin gated views (G3 — phase3_public). Logic in ``living.services``.

V5.22 (SECTION_SYSTEM_V2 §3.15; lane P2): «Vivre en Italie» closes on E «pour s'installer», built only from what
exists — the training after the arrival (its prescribed title), the two prescribed glossary terms everyone meets after
the arrival (their prescribed definitions) and the FAQ. Q8: no theme card and no «coming soon»; reviewed themes take
their place through the existing publication model.
"""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from accounts.middleware import require_second_factor
from cms import locked_content
from core import gates
from core.links import public_url
from glossary import services as glossary
from glossary.views import where_to_meet
from living import services
from news.editorial import blocks


def _current_language() -> str:
    return (translation.get_language() or "fr").split("-")[0]


def _check_gate(request) -> bool:
    """404 while Phase 3 is closed. Staff may preview with ?preview=1 (page is noindex)."""
    if gates.phase3_public():
        return False
    user = request.user
    wants_preview = request.GET.get("preview") == "1"
    if wants_preview and user.is_authenticated and user.is_staff and user.has_perm("living.view_livingtopic"):
        # a staff preview of unpublished content: the second-factor policy first (accounts.middleware)
        require_second_factor(request)
        return True
    raise Http404


#: the two prescribed terms of the glossary a newcomer meets after the arrival (§3.15 V2)
SETTLE_TERMS = ("permesso_di_soggiorno", "codice_fiscale")


def _settle(lang: str) -> dict:
    """«Pour s'installer», two rows of one kind each (round 1, QA_ROUND1 M8 — an emptied lead tile above tiles of two
    kinds): the two terms as the glossary's own dictionary cards (glossary/_entry.html: the Italian term, the prescribed
    definition whole, «Où le rencontrer», the card's answer to the hand and the focus), then the two ways on as compact
    route tiles — the training after the arrival (its prescribed title) and the FAQ."""
    terms = []
    if public_url("glossary:index"):
        where = where_to_meet(lang)
        live = {term.key: term for term in glossary.live_terms().filter(key__in=SETTLE_TERMS)}
        for key in SETTLE_TERMS:
            if key in live:
                entry = glossary.entry_for(live[key], lang)
                terms.append({"entry": entry, "chips": where.get(entry.key, [])})
    routes = []
    training = public_url("pathways:training")
    if training:
        title, effective = locked_content.get("p3.training_after.title", lang)
        routes.append(
            {
                "href": f"{training}#apres-l-arrivee",
                "title": title,
                "title_lang": "" if effective == lang else effective,
                "glyph": "presentation",
            }
        )
    faq = public_url("faq:index")
    if faq:
        routes.append({"href": faq, "title": _("Questions fréquentes"), "glyph": "circle-help"})
    return {"terms": terms, "routes": routes}


@require_GET
def index(request):
    preview = _check_gate(request)
    lang = _current_language()
    topics = list(services.public_topics())
    context = {
        "topics": [(topic, topic.texts(lang)) for topic in topics],
        "settle": _settle(lang),
        "preview": preview,
        "noindex": preview,
        "breadcrumbs": [{"label": _("Vivre en Italie"), "url": ""}],
    }
    return render(request, "living/index.html", context)


@require_GET
def topic(request, slug: str):
    preview = _check_gate(request)
    lang = _current_language()
    topic_obj = services.public_topic(slug)
    if topic_obj is None:
        raise Http404
    sheets = list(services.public_sheets(topic_obj).prefetch_related("translations"))
    texts = topic_obj.texts(lang)
    context = {
        "topic": topic_obj,
        "texts": texts,
        "intro_blocks": blocks(texts.body),
        "sheets": [(sheet, sheet.texts(lang)) for sheet in sheets],
        "preview": preview,
        "noindex": preview,
        "breadcrumbs": [
            {"label": _("Vivre en Italie"), "url": reverse("living:index")},
            {"label": texts.title, "url": ""},
        ],
    }
    return render(request, "living/topic.html", context)


@require_GET
def sheet(request, topic: str, slug: str):
    preview = _check_gate(request)
    lang = _current_language()
    topic_obj = services.public_topic(topic)
    if topic_obj is None:
        raise Http404
    sheet_obj = services.public_sheet(topic_obj, slug)
    if sheet_obj is None:
        raise Http404
    topic_texts = topic_obj.texts(lang)
    texts = sheet_obj.texts(lang)
    context = {
        "topic": topic_obj,
        "topic_texts": topic_texts,
        "sheet": sheet_obj,
        "texts": texts,
        "blocks": blocks(texts.body),
        "sources": sheet_obj.sources or [],
        "preview": preview,
        "noindex": preview,
        "breadcrumbs": [
            {"label": _("Vivre en Italie"), "url": reverse("living:index")},
            {"label": topic_texts.title, "url": topic_obj.get_absolute_url()},
            {"label": texts.title, "url": ""},
        ],
    }
    return render(request, "living/sheet.html", context)
