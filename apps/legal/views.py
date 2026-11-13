from django.http import Http404
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _  # lazy: evaluated per request, not at import

from cms import locked_content
from legal.models import LegalKind, TranslationStatus, open_fields_allowed
from legal.rendering import blocks
from legal.services import get_document

PAGE_TITLES = {
    LegalKind.PRIVACY: "Privacy Policy",
    LegalKind.COOKIES: "Cookie Policy",
    LegalKind.NOTICES: _("Note legali"),
    LegalKind.TERMS: _("Condizioni di utilizzo"),
    LegalKind.DISCLAIMER: _("Avvertenze"),
}

#: V5.14 categories C/D: substantive ILE legal content and governance documents — absent until published (Q2)
SUBSTANTIVE = frozenset({LegalKind.NOTICES, LegalKind.TERMS, LegalKind.DISCLAIMER})


def _legal_page(request, kind: str):
    doc = get_document(kind)
    available = doc.is_available
    preview = open_fields_allowed()
    # Q2 (owner, 28 Oct 2026) and the W2 review's M-2: an unpublished SUBSTANTIVE page (category C/D of V5.14: the
    # official notices, the terms, the disclaimer) is never shown to the public — not even as «Page en cours de
    # préparation». It answers 404 (the sitemap and the links already leave it out); only the preview (development
    # settings: open fields allowed, which production forces off) still reaches it, through the preview hub's legal
    # rows and the phase console. The privacy notice and the cookie information (A/B) are lane P's: they keep their
    # route and their blocked state, because privacy is never hidden behind Allegato 1 (V5.14).
    if kind in SUBSTANTIVE and not available and not preview:
        raise Http404
    # A/B (V5.14): on /fr/, /en/, /ar/ the courtesy translation, with its «the Italian prevails» notice and a link
    # to the Italian master; on /it/ the master. C/D: the Italian text, and the archived FR courtesy if enabled.
    translation = doc.translation_for(get_language()) if available else None
    courtesy = None
    if available and doc.courtesy_fr_enabled and not doc.translations:
        courtesy, _lang = locked_content.get(doc.courtesy_key, "fr")
    if translation:
        title = translation.get("title") or doc.title_it or PAGE_TITLES[kind]
        body = translation["body"]
    elif available:
        title = doc.title_it or PAGE_TITLES[kind]
        body = doc.body_it
    else:  # an unpublished draft's title never reaches the page
        title, body = PAGE_TITLES[kind], ""
    page_blocks = blocks(body) if available else []
    # V5.32 (lane A): the reader's «Sommaire de la page» — each h2 of the text gets an anchor, the index its words
    # verbatim (the official text's own headings, its own numbering); nothing in the text changes
    toc = []
    for number, block in enumerate((b for b in page_blocks if b["kind"] == "h2"), start=1):
        block["id"] = f"sezione-{number}"
        toc.append({"id": block["id"], "html": block["html"]})
    context = {
        "document": doc,
        "kind": kind,
        "page_title": title,
        "available": available,
        "translation": translation,
        "translation_pending": bool(
            translation
            and preview
            and doc.translation_status == TranslationStatus.PENDING
            and translation.get("pending")
        ),
        "blocks": page_blocks,
        "toc": toc,
        "open_fields": doc.open_field_ids() if available and preview else [],
        "open_field_classes": doc.open_field_classes() if available and preview else [],
        "courtesy": courtesy,
        "courtesy_notice": locked_content.text("legal.courtesy_notice.fr", "fr"),
        "noindex": not available,
    }
    return render(request, "legal/document.html", context)


def privacy(request):
    return _legal_page(request, LegalKind.PRIVACY)


def cookies(request):
    return _legal_page(request, LegalKind.COOKIES)


def notices(request):
    return _legal_page(request, LegalKind.NOTICES)


def terms(request):
    return _legal_page(request, LegalKind.TERMS)


def disclaimer(request):
    return _legal_page(request, LegalKind.DISCLAIMER)
