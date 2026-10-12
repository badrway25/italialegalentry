from django.shortcuts import render
from django.utils.translation import gettext_lazy as _  # lazy: evaluated per request, not at import

from cms import locked_content
from legal.models import LegalKind
from legal.services import get_document

PAGE_TITLES = {
    LegalKind.PRIVACY: "Privacy Policy",
    LegalKind.COOKIES: "Cookie Policy",
    LegalKind.NOTICES: _("Note legali"),
    LegalKind.TERMS: _("Condizioni di utilizzo"),
    LegalKind.DISCLAIMER: _("Avvertenze"),
}


def _legal_page(request, kind: str):
    doc = get_document(kind)
    courtesy = None
    if doc.is_available and doc.courtesy_fr_enabled:
        courtesy, _lang = locked_content.get(doc.courtesy_key, "fr")
    context = {
        "document": doc,
        "kind": kind,
        "page_title": doc.title_it or PAGE_TITLES[kind],
        "available": doc.is_available,
        "paragraphs": doc.paragraphs() if doc.is_available else [],
        "courtesy": courtesy,
        "courtesy_notice": locked_content.text("legal.courtesy_notice.fr", "fr"),
        "noindex": not doc.is_available,
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
