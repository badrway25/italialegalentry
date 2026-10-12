from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from glossary import services


def _lang() -> str:
    return translation.get_language() or settings.LANGUAGE_CODE


@require_safe
def index(request):
    visible, preview = services.page_visible(request)
    if not visible:
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
    context = {
        "page_title": _("Glossaire"),
        "query": query,
        "is_search": bool(query),
        "entries": entries,
        "groups": groups,
        "letters": [g.letter for g in groups],
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
    context = {
        "entry": entry,
        "related": services.related_entries(term_obj, lang),
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
