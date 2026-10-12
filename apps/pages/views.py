"""Homepage and institutional pages — thin views; every decision lives in ``pages.services``."""

from __future__ import annotations

from django.http import Http404
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from core import gates
from pages import services


def _crumbs(*items: tuple[str, str]) -> list[dict]:
    return [{"label": label, "url": url} for label, url in items]


@require_safe
def home(request):
    return render(request, "pages/home.html", services.home_context(request))


@require_safe
def project(request):
    context = services.project_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), ""))
    return render(request, "pages/project.html", context)


@require_safe
def agami(request):
    context = services.agami_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), services.safe_reverse("pages:project")), (_("AGAMI"), ""))
    return render(request, "pages/agami.html", context)


@require_safe
def network(request):
    context = services.network_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), services.safe_reverse("pages:project")), (_("Le réseau"), ""))
    return render(request, "pages/network.html", context)


@require_safe
def contact(request):
    context = services.contact_context(request)
    context["breadcrumbs"] = _crumbs((_("Contact"), ""))
    return render(request, "pages/contact.html", context)


@require_safe
def antifraud(request):
    """Phase 3 page: 404 (never « coming soon ») while gate G3 is closed; staff preview is noindex."""
    is_preview = False
    if not gates.phase3_public():
        if not services.can_preview(request):
            raise Http404
        is_preview = True
    context = services.antifraud_context(request, is_preview=is_preview)
    context["breadcrumbs"] = _crumbs((_("Attention aux fraudes"), ""))
    response = render(request, "pages/antifraud.html", context)
    if is_preview:
        # A back-office preview of gated Phase 3 content must never be stored by a shared cache.
        add_never_cache_headers(response)
    return response
