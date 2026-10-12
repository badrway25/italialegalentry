"""Thin gated views (G3 — phase3_public). Logic in ``living.services``."""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from core import gates
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
        return True
    raise Http404


@require_GET
def index(request):
    preview = _check_gate(request)
    lang = _current_language()
    topics = list(services.public_topics())
    context = {
        "topics": [(topic, topic.texts(lang)) for topic in topics],
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
