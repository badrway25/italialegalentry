from __future__ import annotations

from django.conf import settings
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import translation
from django.utils.html import escape
from django.utils.translation import gettext
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


#: The words of the bare page (`_bare`), the error pages' own: msgids of the four catalogues, never new copy.
_BARE_WORDS = {
    400: (
        "Requête invalide",
        "La requête n’a pas pu être traitée. Vérifiez l’adresse saisie ou revenez à l’accueil.",
    ),
    500: (
        "Erreur technique",
        "Une erreur technique est survenue. Nos équipes en ont été informées ; vous pouvez réessayer dans quelques "
        "instants.",
    ),
}


def _bare(status: int) -> str:
    """The last resort of a self-sufficient page: the same title and sentence, unstyled, when even the template fails
    (a static manifest that lost an entry, a broken template). It names nothing: no exception, no path, no request."""
    title, text = (escape(gettext(words)) for words in _BARE_WORDS[status])
    lang = translation.get_language() or settings.LANGUAGE_CODE
    direction = "rtl" if translation.get_language_bidi() else "ltr"
    return (
        f'<!DOCTYPE html><html lang="{escape(lang)}" dir="{direction}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
        f"<title>{title}</title></head><body><main><h1>{title}</h1><p>{text}</p>"
        f'<p><a href="/{escape(lang)}/">{escape(gettext("Retour à l’accueil"))}</a></p></main></body></html>'
    )


def _self_sufficient(request, status: int) -> HttpResponse:
    """
    400 and 500 (design V5, W3-F2): the error page drawn WITHOUT the request — no context processor, no database, no
    session — as Django's own `bad_request` and `server_error` are, because the failure they answer may have taken any
    of these with it (a request that could not be read, a database that is gone, a broken processor). What the page
    needs comes from here: the project's name and the public address from settings (not from the database), the
    request's correlation id from the request id middleware. The language is the one LocaleMiddleware set.
    """
    context = {
        "project_name": settings.ILE["PROJECT_NAME"],
        "contact_email": settings.ILE["PUBLIC_CONTACT_EMAIL"],
        "request_id": getattr(request, "request_id", ""),
    }
    try:
        body = loader.render_to_string(f"errors/{status}.html", context)
    except Exception:  # the page itself must never be the second failure
        body = _bare(status)
    return HttpResponse(body, status=status)


def error_400(request, exception=None):
    return _self_sufficient(request, 400)


def error_403(request, exception=None):
    return _error(request, 403, exception)


def error_404(request, exception=None):
    return _error(request, 404, exception)


def error_500(request):
    return _self_sufficient(request, 500)


def error_429(request):
    return _error(request, 429)
