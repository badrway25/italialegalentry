from django.http import Http404
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

from core import gates
from partners.services import grouped_by_kind


def index(request):
    if not gates.partners_public():  # V5.12 §8: no page that only says «nobody yet»
        raise Http404
    lang = translation.get_language() or "fr"
    groups = grouped_by_kind(lang)
    context = {
        "groups": groups,
        "breadcrumbs": [{"label": _("Partenaires"), "url": ""}],
    }
    return render(request, "partners/index.html", context)
