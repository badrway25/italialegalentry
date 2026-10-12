"""
Ecosystem spaces — thin views. Gates, prescribed texts, photography and navigation are resolved in
``ecosystem.services``; the forms live in ``enquiries`` (one canonical implementation): the Espace
Entreprises embeds the ``{% company_needs_form %}`` inclusion tag, the other pages link the routes.
"""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from ecosystem import services
from ecosystem.models import SpaceKey


def _render(
    request, key: str, template: str, *, title: str, description: str, sections: list, extra: dict, title_lang: str = ""
):
    visible, is_preview = services.page_visible(request, key)
    if not visible:
        raise Http404
    lang = request.LANGUAGE_CODE
    space = services.get_space(key, preview=is_preview)
    photo = services.photo_for(space, lang)
    crumbs = [{"label": title, "url": "", "lang": title_lang}]  # lang: prescribed French title on a translated page
    context = {
        "space_key": key,
        "page_title": title,
        "meta_description": description,
        "breadcrumbs": crumbs,
        "photo": photo,
        "note": services.editorial_note(space, lang),
        "local_nav_items": services.local_nav(key, sections, preview=is_preview),
        "links": services.related_links(preview=is_preview),
        "is_preview": is_preview,
        "noindex": is_preview,
        "seo": services.seo(title, description, photo),
        "jsonld": services.page_jsonld(request, name=title, description=description, crumbs=crumbs, lang=lang),
        **extra,
    }
    response = render(request, template, context)
    if is_preview:
        # A back-office preview of unpublished Phase 3 content must never be stored by a shared cache.
        add_never_cache_headers(response)
    return response


@require_safe
def companies(request):
    """Espace Entreprises — PHASE 1: never gated, independent of Phase 3."""
    lang = request.LANGUAGE_CODE
    title = services.locked_text("p1.companies.title", lang)
    intro = services.locked_text("p1.companies.intro", lang)
    guarantee = services.recruitment_guarantee(lang)
    sections = [("demarche", _("La démarche")), ("formulaire", _("Recueil des besoins"))]
    if guarantee:
        sections.append(("transparence", _("Transparence")))
    return _render(
        request,
        SpaceKey.COMPANIES,
        "ecosystem/companies.html",
        title=_("Espace Entreprises"),
        description=intro.text,
        sections=sections,
        extra={
            "title": title,
            "intro": intro,
            "quote": services.locked_text("p1.companies.quote", lang),
            "moments": services.company_moments(),
            "guarantee": guarantee,
        },
    )


@require_safe
def institutions(request):
    lang = request.LANGUAGE_CODE
    intro = services.locked_text("p3.institutions.intro", lang)
    recipients = services.enumeration("p3.institutions.recipients", lang)
    return _render(
        request,
        SpaceKey.INSTITUTIONS,
        "ecosystem/institutions.html",
        title=_("Espace Institutions"),
        description=intro.text,
        sections=[
            ("destinataires", recipients.label, recipients.source.lang_attr),
            ("collaboration", _("Proposer une collaboration")),
        ],
        extra={"recipients": recipients},
    )


@require_safe
def universities(request):
    lang = request.LANGUAGE_CODE
    intro = services.enumeration("p3.universities.intro", lang)
    return _render(
        request,
        SpaceKey.UNIVERSITIES,
        "ecosystem/universities.html",
        title=_("Espace Universités et Formation"),
        description=intro.source.text,
        sections=[("partenariat", _("Proposer un partenariat"))],
        extra={"intro": intro},
    )


@require_safe
def pilot(request):
    lang = request.LANGUAGE_CODE
    title = services.locked_text("p3.pilot.title", lang)
    body = services.locked_text("p3.pilot.body", lang)
    return _render(
        request,
        SpaceKey.PILOT,
        "ecosystem/pilot.html",
        title=title.text,
        title_lang=title.lang_attr,
        description=body.text,
        sections=[("sequence", _("La séquence")), ("participer", _("Participer"))],
        extra={"title": title, "body": body, "flow": services.pilot_flow(lang)},
    )
