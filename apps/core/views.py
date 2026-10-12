from __future__ import annotations

from django.conf import settings
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@require_GET
@never_cache
def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_ok = True
    except Exception:  # pragma: no cover
        db_ok = False
    status = 200 if db_ok else 503
    return JsonResponse({"status": "ok" if db_ok else "degraded", "database": db_ok}, status=status)


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /backoffice/",
        "Disallow: /api/",
        "Disallow: /documents/",
        "Disallow: /*/espace-reserve/",
        "Disallow: /*/compte/",
        "Disallow: /*/orientation/session/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain; charset=utf-8")


def root_redirect(request):
    lang = translation.get_language_from_request(request, check_path=False) or settings.LANGUAGE_CODE
    if lang not in dict(settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE
    return HttpResponseRedirect(f"/{lang}/")


def _error(request, status: int, exception=None):
    return render(request, f"errors/{status}.html", status=status)


def error_400(request, exception=None):
    return _error(request, 400, exception)


def error_403(request, exception=None):
    return _error(request, 403, exception)


def error_404(request, exception=None):
    return _error(request, 404, exception)


def error_500(request):
    return _error(request, 500)


def error_429(request):
    return _error(request, 429)
