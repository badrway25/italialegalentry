"""Espace Personnes views — thin; every decision lives in ``pathways.services``."""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from pathways import services


def _crumbs(*items: tuple) -> list[dict]:
    """(label, url) or (label, url, lang): `lang` marks a label written in another language than the page."""
    return [{"label": i[0], "url": i[1], "lang": i[2] if len(i) > 2 else ""} for i in items]


def _fallback_lang() -> str:
    """Language attribute of a prescribed French text on a page displayed in another language."""
    from django.conf import settings
    from django.utils import translation

    current = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    return settings.CONTENT_FALLBACK_LANGUAGE if current != settings.CONTENT_FALLBACK_LANGUAGE else ""


def _gate(request) -> bool:
    """True when gated pages may render (Phase 3 open, or staff preview). Raises 404 otherwise."""
    visible, is_preview = services.gated_pages_visible(request)
    if not visible:
        raise Http404
    return is_preview


@require_GET
def index(request):
    visible, is_preview = services.gated_pages_visible(request)
    links = services.related_links()
    if not visible:
        context = {
            "links": links,
            "breadcrumbs": _crumbs((_("Espace Personnes"), "")),
        }
        return render(request, "pathways/index_interim.html", context)
    context = {
        "entries": services.index_entries(),
        "how": services.how_it_works(),
        "links": links,
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs((_("Espace Personnes"), "")),
    }
    return render(request, "pathways/index.html", context)


@require_GET
def detail(request, key: str):
    is_preview = _gate(request)
    pathway = services.get_pathway_for_preview(key) if is_preview else services.get_live_pathway(key)
    if pathway is None:
        raise Http404
    ctx = services.detail_context(pathway)
    context = {
        "d": ctx,
        "pathway": pathway,
        "links": services.related_links(),
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs((_("Espace Personnes"), reverse("pathways:index")), (ctx.title, "", _fallback_lang())),
    }
    return render(request, "pathways/detail.html", context)


@require_GET
def diplomas(request):
    is_preview = _gate(request)
    context = {
        "steps": services.diploma_steps(),
        "links": services.related_links(),
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs(
            (_("Espace Personnes"), reverse("pathways:index")), (_("Diplômes et titres étrangers"), "")
        ),
    }
    return render(request, "pathways/diplomas.html", context)


@require_GET
def training(request):
    is_preview = _gate(request)
    context = {
        "links": services.related_links(),
        "origin_pathway_url": services.index_entries()[2].url,  # training_in_origin_country when live
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs((_("Espace Personnes"), reverse("pathways:index")), (_("Formation"), "")),
    }
    return render(request, "pathways/training.html", context)
