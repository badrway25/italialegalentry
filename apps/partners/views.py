from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _

from partners.services import grouped_by_kind


def index(request):
    lang = translation.get_language() or "fr"
    groups = grouped_by_kind(lang)
    context = {
        "groups": groups,
        "breadcrumbs": [{"label": _("Partenaires"), "url": ""}],
    }
    return render(request, "partners/index.html", context)
