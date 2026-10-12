from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from faq import services


@require_safe
def index(request):
    visible, preview = services.page_visible(request)
    if not visible:
        raise Http404
    lang = translation.get_language() or settings.LANGUAGE_CODE
    query = services.normalise_query(request.GET.get("q"))
    if query:
        entries = services.entries_for(services.search_items(query), lang)
        groups = []
        jsonld = ""
    else:
        entries = services.entries_for(services.live_items(), lang)
        groups = services.group_entries(entries, lang)
        jsonld = services.render_jsonld(services.faq_jsonld(entries, lang)) if entries else ""
    context = {
        "page_title": _("Questions fréquentes"),
        "query": query,
        "is_search": bool(query),
        "entries": entries,
        "groups": groups,
        "faq_jsonld": jsonld,
        "is_preview": preview,
        # Staff previews and search-result pages (unbounded URL space) are never indexed.
        "noindex": preview or bool(query),
        "breadcrumbs": [{"label": _("Questions fréquentes"), "url": ""}],
    }
    return render(request, "faq/index.html", context)
