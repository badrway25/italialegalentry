"""Espace Personnes views — thin; every decision lives in ``pathways.services``."""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from pathways import services


def _crumbs(*items: tuple) -> list[dict]:
    """(label, url) or (label, url, lang): `lang` marks a label written in another language than the page."""
    return [{"label": i[0], "url": i[1], "lang": i[2] if len(i) > 2 else ""} for i in items]


def _page_lang() -> str:
    from django.conf import settings
    from django.utils import translation

    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def _help(request) -> SafeString:
    """«Who can help me» (D26), live: the help line with the public address — the side annotation of «la boussole»."""
    from core.context_processors import site

    email = site(request)["site"]["contact_email"]
    return format_html('{} <a class="email" href="mailto:{}">{}</a>', _("Besoin d’aide ? Écrivez-nous :"), email, email)


def _boussole(request, links: dict) -> dict:
    """PS-5 / F3 / D4 «la boussole» (SECTION_SYSTEM_V2 §2 A, §3.5, §3.9, §3.10): the questionnaire's action — what,
    why (its caution «Les décisions relèvent des autorités compétentes» kept), the one primary — or, while it is not
    open, the sentence that says so; the live help line as its side annotation. V5.32, the correction round of the
    senior integration review (P2-3): the closing band «la chiusura» draws it (pathways/_chiusura.html) — the plate's
    title left with the plate."""
    action = (
        {"url": links["orientation"], "label": _("Commencer le questionnaire d’orientation")}
        if links.get("orientation")
        else None
    )
    return {
        "text": _(
            "Le questionnaire d’orientation vous propose, en quelques questions progressives, une pré-évaluation à "
            "caractère informatif. Les décisions relèvent des autorités compétentes."
        ),
        "action": action,
        "pending": "" if action else _("Le questionnaire d’orientation sera disponible prochainement."),
        "help": _help(request),
    }


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
    entries = services.index_entries(lang=_page_lang())  # V5.27 / R7′: each part by its sub-key (the explorer's rows)
    how = services.how_it_works()
    context = {
        "entries": entries,
        "family_counts": services.family_counts(entries),
        "how": how,
        "links": links,
        # V5.32 (lane B): «l'esploratore» — the families, each pathway its line, frame and actors (its own `lang`s)
        "families": services.explorer(entries, _page_lang()),
        "how_steps": services.how_steps(how, links),
        "tiles": services.space_tiles(links),
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
    links = services.related_links()
    lang = _page_lang()
    context = {
        "d": ctx,
        "pathway": pathway,
        "links": links,
        # V5.22 (SECTION_SYSTEM_V2 §3.5; lane P1): the milestones, the terms with their definitions, the help line
        "milestones": services.sheet_steps(services.sheet_milestones(ctx.steps, lang), links),
        # V5.32 (lane B): the sheet's photograph, its family and its neighbours
        "frame": services.pathway_frame(pathway.key, services.FRAME_SIZES_SHEET),
        "neighbours": services.sheet_neighbours(pathway.key, lang),
        "terms": services.glossary_terms([term["slug"] for term in ctx.glossary], lang),
        "authority_glyph": services.icons.AUTHORITY_SEAT,
        # V5.32, the correction round (P2-3): the closing band «la chiusura» — the questionnaire's action, the help line
        "boussole": _boussole(request, links),
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs((_("Espace Personnes"), reverse("pathways:index")), (ctx.title, "", ctx.title_lang)),
    }
    return render(request, "pathways/detail.html", context)


@require_GET
def diplomas(request):
    is_preview = _gate(request)
    links = services.related_links()
    dossier = services.diploma_dossier(_page_lang())
    context = {
        "steps": services.diploma_steps(),
        "links": links,
        # V5.22 (SECTION_SYSTEM_V2 §3.10; lane P1): the dossier's stations and their status in words; V5.32, the
        # correction round (P2-3): the closing band «la chiusura» — the questionnaire's action, the help line
        "dossier": dossier,
        "dossier_pending": any(step["pending"] for step in dossier),
        "boussole": _boussole(request, links),
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
    links = services.related_links()
    context = {
        "links": links,
        "origin_pathway_url": services.index_entries()[2].url,  # training_in_origin_country when live
        # V5.32, the correction round (P2-3): the closing band «la chiusura» — the questionnaire's action, the help line
        "boussole": _boussole(request, links),
        "before_sizes": services.TRAVERSATA_BEFORE_SIZES,
        "after_sizes": services.TRAVERSATA_AFTER_SIZES,
        "is_preview": is_preview,
        "noindex": is_preview,
        "breadcrumbs": _crumbs((_("Espace Personnes"), reverse("pathways:index")), (_("Formation"), "")),
    }
    return render(request, "pathways/training.html", context)
