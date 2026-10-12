"""
The views of the V5 live preview (V5.4 plan §4).

**The live product** — what ``/__design-v5/`` is since V5.4:

* ``landing`` — the live V5 home: the real ``/fr/`` page of this server, full window, in one
  same-origin frame, under the strip (designpreview.live);
* ``index`` — one click away: every live surface, public and authenticated, in fr and ar, frames
  opened on demand (at most one pair at a time — the index's script holds it), the persona cards,
  the families' status, the foundation's specimen boards, the V4 control on 8771, the archive;
* ``persona_enter`` / ``persona_exit`` — the persona switch, POST only (designpreview.personas);
* ``state`` — the states a person reaches without credentials whose page this server cannot show
  at an address of its own: the 429 page, and the product's 404 (under DEBUG an address that
  matches nothing gets Django's technical page);
* ``decision`` — a family's CD decision, as text, from ``docs/design-v5/QA/v54/``;
* ``specimen`` — a foundation family's specimen board (W1-0's route, unchanged).

**The research archive** — the catalogue the preview was until V5.4, moved as it was under
``/__design-v5/research/``: ``hub``, the hero and type pickers, the compare view and the proof
files. The old addresses (``/hero/``, ``/type/``, ``/compare/``, ``/proof/…``) answer 302 to their
``/research/`` equivalents (``legacy``), and an old link to an anchor of the hub (``/#g-…``) is
sent on by the landing's script.

**Who is answered** (designpreview.access): ``DEBUG`` and ``ILE_DESIGN_PREVIEW`` both true, a
loopback caller with no proxy header, and this process's own ``Host``. A refused caller is never
served the preview: it meets a plain 404 that names nothing, before the method is looked at and
before the CSRF check — every route is exempt from the middleware's check, so that a refused POST
is not told «CSRF verification failed» about a route that then plainly exists (review W1-P,
security m1). Django's own pages are another matter: under DEBUG its 404 page for a path that
matches nothing lists the URL patterns, the mount among them. Then the method: GET and HEAD for
every page (``_preview_only``: a POST is a 405 and changes nothing), POST with its CSRF token —
checked inside, after the gate — for the persona switch (``_persona_only``); 405 otherwise. Every
response to an allowed caller says ``X-Robots-Tag: noindex, nofollow`` and ``Cache-Control:
no-store``.

**The Content-Security-Policy** is widened per view, never globally: the landing, the index, the
two pickers and the compare view frame pages of this origin (``frame-src 'self'``); a proof file
may be framed by this origin (``frame-ancestors 'self'``, ``X-Frame-Options: SAMEORIGIN``). A real
page is framed only through ``designpreview.frames``, under its narrow condition. The landing and
the index drop ``upgrade-insecure-requests``: on this plain-http loopback server it made Chromium
upgrade the frame's redirect hops to https and refuse them, leaving a blank frame (review W1-P B1),
and a frame inherits its parent's insecure-requests policy. ``script-src 'self'`` and ``style-src
'self'`` hold on every page.

**The database.** No view asks for a transaction (``non_atomic_requests``, outermost — the
project's ``ATOMIC_REQUESTS`` would otherwise open a connection for every call, the preview outage
of 2 October 2026, docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md). The pickers, the compare view,
the proof files, the specimen boards and the decisions read nothing. The landing and the index are
rendered without the request's context processors too; they read the session — one query, and only
when a session cookie came — to say which persona is in. The archive's hub extends base.html and
keeps its reads; the persona switch reads the account and writes the session; the 429 page is the
site's own template. Every connection is closed when its response leaves, under the ceiling of
``designpreview.middleware``.
"""

from __future__ import annotations

import re
from functools import wraps
from pathlib import Path

from csp.decorators import csp_replace, csp_update
from django.conf import settings
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from django.utils import translation
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST

from designpreview import access, live, personas, services

#: Kept for the code that imported it from here: the loopback interface (designpreview.access).
LOOPBACK = access.LOOPBACK


def _enabled() -> bool:
    return access.enabled()


def _proof_root() -> Path:
    return Path(getattr(settings, "ILE_DESIGN_PREVIEW_PROOF_DIR", "C:/tmp/ile_v5_council/proof"))


def _decisions_root() -> Path:
    return Path(settings.BASE_DIR) / "docs" / "design-v5" / "QA" / "v54"


def _seal(response):
    response["X-Robots-Tag"] = "noindex, nofollow"
    response["Cache-Control"] = "no-store"
    return response


def _not_found() -> HttpResponse:
    """
    What a refused caller meets: a 404 of two words. Never ``Http404`` — under DEBUG Django would
    answer it with its technical page, which names the view that raised it.
    """
    return HttpResponseNotFound("Not Found\n", content_type="text/plain; charset=utf-8")


def _guarded(view, methods):
    """
    The gate first (a plain 404), then the method (405), then the view; every answer to an allowed
    caller sealed. Exempt from the CSRF middleware, so that the gate answers before it: the switch
    checks its token itself, inside, once the caller is allowed (``_persona_only``), and a page
    takes GET and HEAD only, so a POST that reaches it is a 405 that changes nothing.
    """

    inner = methods(view)

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not access.allowed(request):
            return _not_found()
        return _seal(inner(request, *args, **kwargs))

    wrapped.csrf_exempt = True
    # Outermost, so that the attribute Django reads (BaseHandler.make_view_atomic) is on the very
    # callable the URLconf holds, whatever the decorators inside do with ``__dict__``.
    return transaction.non_atomic_requests(wrapped)


def _preview_only(view):
    """A page of the preview: GET and HEAD."""
    return _guarded(view, require_http_methods(["GET", "HEAD"]))


def _persona_only(view):
    """The persona switch: POST, with its CSRF token — enforced here, whatever the middleware chain says."""
    return _guarded(view, lambda inner: require_POST(csrf_protect(inner)))


def _render(request, template: str, context: dict, status: int = 200) -> HttpResponse:
    """Render in Italian — the owner's language and the proof package's — whatever the request says."""
    context.setdefault("noindex", True)
    context.setdefault("proof_dir", str(_proof_root()))
    with translation.override("it"):
        response = render(request, template, context, status=status)
    # LocaleMiddleware would otherwise stamp the request's language on a page written in Italian.
    response.headers["Content-Language"] = "it"
    return response


FRAME = "dev/designpreview/frame.html"
COMPARE = "dev/designpreview/compare.html"
LANDING = "dev/designpreview/landing.html"
INDEX = "dev/designpreview/index.html"


def _render_frame(context: dict, status: int = 200, template: str = FRAME) -> HttpResponse:
    """
    A standalone document — a picker, the compare view, the landing, the index — in Italian,
    WITHOUT the request's context processors, and so without the query they would run.

    None of these pages names a site setting: ``core.context_processors.site`` would read
    ``SiteSettings`` for values the template never prints. The templates need ``static``, ``url``,
    the lock-up and — on the landing and the index — the CSRF token of the persona forms, which the
    view hands over itself.
    """
    context.setdefault("stylesheets", services.token_stylesheets())
    with translation.override("it"):
        content = loader.render_to_string(template, context)
    response = HttpResponse(content, status=status)
    response.headers["Content-Language"] = "it"
    return response


# ---------------------------------------------------------------------------------------------
# The live product
# ---------------------------------------------------------------------------------------------


def _csrf(request) -> str:
    from django.middleware.csrf import get_token

    return get_token(request)


#: The landing and the index frame pages of this plain-http server: under the global directive,
#: Chromium upgrades the frame's redirect hops to https and refuses them (review W1-P B1).
#: django-csp omits a directive replaced by ``None``; the global policy keeps it.
NO_UPGRADE = {"upgrade-insecure-requests": None}


@_preview_only
@csp_update({"frame-src": ["'self'"]})
@csp_replace(NO_UPGRADE)
def landing(request):
    """
    The live V5 home under the strip: exactly one frame, holding the real page — the home unless
    ``?page=`` names another page of this site (designpreview.live.page_param), in the window or in a
    phone of 390 px (``?frame=phone``). A ``?page=`` that is not a page of this site is answered 400,
    with the way back — never framed, never guessed.

    A page of the documents app has no language prefix: it answers in the language cookie's
    language. ``?lang=`` then says which, and the landing sets that cookie — as
    ``core.middleware.LanguageCookieMiddleware`` does whenever a prefixed page is served — so that
    the frame shows the page in the language the strip names.
    """
    raw = request.GET.get("page", "")
    page = live.page_param(raw) if raw else live.url_of(live.PUBLIC_PAGES[0], "fr")
    frame = request.GET.get("frame", "desktop")
    if frame not in live.FRAMES:
        frame = "desktop"
    if not page:
        context = {
            "strip": live.strip(request, "/fr/", frame),
            "error": "La pagina chiesta non è una pagina di questo sito: la cornice tiene soltanto un indirizzo "
            "di questo stesso server, una pagina in /fr/, /ar/, /it/, /en/ o /documents/.",
            "csrf_token": _csrf(request),
        }
        return _render_frame(context, status=400, template=LANDING)
    cookie = settings.LANGUAGE_COOKIE_NAME
    asked = request.GET.get("lang", "")
    lang = ""
    if live.is_neutral(page):
        lang = asked if asked in live.LANGS_ALL else request.COOKIES.get(cookie, "")
    context = {"strip": live.strip(request, page, frame, lang=lang), "csrf_token": _csrf(request)}
    response = _render_frame(context, template=LANDING)
    if live.is_neutral(page) and asked in live.LANGS_ALL and request.COOKIES.get(cookie) != asked:
        from core.middleware import LanguageCookieMiddleware

        response.set_cookie(
            cookie,
            asked,
            max_age=LanguageCookieMiddleware.MAX_AGE,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=True,
        )
    return response


@_preview_only
@csp_update({"frame-src": ["'self'"]})
@csp_replace(NO_UPGRADE)
def index(request):
    """Every live surface, one click from the landing (plan §4.1)."""
    status = live.live_status()
    rows = live.public_rows(status)
    context = {
        "strip": live.strip(request, "/fr/", "desktop", status),
        "status": status,
        "passed": [row for row in rows if row["state"] == live.STATE_V5],
        "fondation": [row for row in rows if row["state"] != live.STATE_V5],
        "cards": live.persona_cards(request, status),
        "families_passed": [family for family in status["families"] if family["state"] == live.STATE_V5],
        "families_fondation": [family for family in status["families"] if family["state"] != live.STATE_V5],
        "boards": live.specimen_boards(),
        "v4_origin": live.v4_origin(),
        "surface_keys": live.surface_keys(),
        "outside": [{"key": key, "title": title, "role": role} for key, title, role in live.OUTSIDE],
        "error_pages": live.DEBUG_ERROR_PAGES,
        "coming": live.coming(status),
        "login": live.public_url("login", "fr"),
        "orientation": live.public_url("orientation", "fr"),
        "csrf_token": _csrf(request),
    }
    return _render_frame(context, template=INDEX)


def _next(request, persona: personas.Persona | None) -> str:
    """
    Where the switch sends the browser. After «Entrer»: the landing framing the page the index asked
    for — only if it is one of that persona's own pages, in any of its languages (review W1-P M3:
    one click enters the persona and opens the page) — and the persona's first page otherwise.
    After «Sortir»: the public page it came from, or its language's home if that page needs a
    session.
    """
    lang = request.POST.get("lang", "fr")
    if lang not in live.LANGS_ALL:
        lang = "fr"
    frame = request.POST.get("frame", "desktop")
    if frame not in live.FRAMES:
        frame = "desktop"
    asked = live.page_param(request.POST.get("page", ""))
    if persona is not None:
        if asked and asked in live.persona_urls(persona.key):
            return live.landing_url(asked, frame, lang)
        with translation.override(lang):
            return live.landing_url(reverse(persona.home), frame)
    page = asked or f"/{lang}/"
    if live.reserved(page):
        page = f"/{lang if live.is_neutral(page) else live.lang_of(page)}/"
    return live.landing_url(page, frame)


def _refused(sentence: str) -> HttpResponse:
    return HttpResponse(sentence + "\n", status=403, content_type="text/plain; charset=utf-8")


@_persona_only
def persona_enter(request, persona: str):
    """Sign in as one of the four QA personas — read-only — and open its first page in the landing's frame."""
    try:
        entered = personas.enter(request, persona)
    except personas.Refused as refusal:
        return _refused(refusal.sentence)
    return HttpResponseRedirect(_next(request, entered))


@_persona_only
def persona_exit(request):
    """Sign this browser out and frame the public page it came from (the home, if that page was a reserved one)."""
    personas.leave(request)
    return HttpResponseRedirect(_next(request, None))


#: The states a person reaches without credentials whose page this server cannot show at an address
#: of its own (plan §4.5): the throttled form's 429, and the product's 404 — the preview runs with
#: DEBUG on, and under DEBUG Django answers an address that matches nothing with its technical page,
#: in English, listing the URL patterns; ``handler404`` is used only when DEBUG is off (review W1-P,
#: UX r2 n1; CD condition C1).
STATES = ("404", "429")


@_preview_only
def state(request, code: str):
    """
    The site's own page for the state ``code``, with its status: 404, a page that does not exist
    (``errors/404.html``), and 429, the throttled form. ``?lang=`` renders it in that language — the
    index links the 404 in fr and in ar — and without it, in the request's.
    """
    if code not in STATES:
        raise Http404
    from core import views as core_views

    view = core_views.error_404 if code == "404" else core_views.error_429
    lang = request.GET.get("lang", "")
    if lang not in live.LANGS_ALL:
        return view(request)
    with translation.override(lang):
        response = view(request)
    # LocaleMiddleware only sets the header when the view has not.
    response.headers["Content-Language"] = lang
    return response


@_preview_only
def decision(request, path: str):
    """A family's CD decision (``decision`` in live_status.json): a Markdown file of docs/design-v5/QA/v54/, as text."""
    if not path.lower().endswith(".md"):
        raise Http404
    full, content_type = services.resolve_proof_file(_decisions_root(), path)
    return FileResponse(full.open("rb"), content_type=content_type)


# ---------------------------------------------------------------------------------------------
# The research archive
# ---------------------------------------------------------------------------------------------


@_preview_only
def hub(request):
    root = _proof_root()
    return _render(
        request,
        "dev/designpreview/hub.html",
        {
            "groups": services.catalogue(root),
            "viewports": services.WIDTHS,
            "proof_present": root.is_dir(),
            "proof_index_url": services.proof_url("index.html") if services.proof_exists(root, "index.html") else "",
        },
    )


def _picker(build, known: dict[str, dict], back: tuple[str, str], template: str = FRAME) -> HttpResponse:
    """
    One picker page: ``build`` resolves the query into the bar and the stage (services.hero_picker,
    services.type_picker, services.compare_view — drawn by ``template``). A value it does not know
    is answered 400 — never a guess, never another comp — with the values it does know (``known``:
    a name → the table whose keys they are) and the way back to a combination that exists; that
    answer is frame.html's, whatever the page.
    """
    try:
        context = build(_proof_root())
    except services.UnknownChoice as exc:
        values = " · ".join(f"{name}: {', '.join(table)}" for name, table in known.items())
        context = {"error": f"Scelta sconosciuta ({exc}). {values}.", "back_url": back[0], "back_label": back[1]}
        return _render_frame(context, status=400)
    return _render_frame(context, template=template)


@_preview_only
@csp_update({"frame-src": ["'self'"]})
def hero(request):
    query = request.GET
    return _picker(
        lambda root: services.hero_picker(
            root, query.get("variant", "h0"), query.get("lang", "fr"), query.get("phase", "3"), query.get("w", "")
        ),
        {"Varianti": services.HERO_VARIANTS, "lingue": services.LANGS, "fasi": services.PHASES},
        (services.hero_url("h0"), "Torna a H-0"),
    )


@_preview_only
@csp_update({"frame-src": ["'self'"]})
def type_systems(request):
    query = request.GET
    return _picker(
        lambda root: services.type_picker(
            root, query.get("system", "a"), query.get("surface", "home"), query.get("lang", "fr"), query.get("w", "")
        ),
        {"Sistemi": services.TYPE_SYSTEMS, "superfici": services.TYPE_SURFACES, "lingue": services.LANGS},
        (services.type_url("a"), "Torna a TYPE A"),
    )


@_preview_only
@csp_update({"frame-src": ["'self'"]})
def compare(request):
    """Two proof pages of one surface, side by side at the same phone width (services.compare_view)."""
    query = request.GET
    return _picker(
        lambda root: services.compare_view(root, query.get("pair", "mes-pieces"), query.get("lang", "fr")),
        {"Confronti": services.COMPARISONS, "lingue": services.LANGS},
        (services.compare_url("mes-pieces"), "Torna al confronto di «Mes pièces»"),
        template=COMPARE,
    )


@_preview_only
@xframe_options_sameorigin
@csp_replace({"frame-ancestors": ["'self'"]})
def proof(request, path: str):
    full, content_type = services.resolve_proof_file(_proof_root(), path)
    return FileResponse(full.open("rb"), content_type=content_type)


#: The archive's old addresses → the URL name of their ``/research/`` equivalent.
LEGACY = {"hero": "hero", "type": "type", "compare": "compare", "proof": "proof"}


@_preview_only
def legacy(request, target: str, path: str = ""):
    """
    302 from an address of the hub before V5.4 to the same thing under ``/research/``, query string
    kept. A proof path is judged as the proof view judges it first, by its string — what the target
    would refuse is a 404 here already — so the redirect is never broader than the page it names.
    """
    if target not in LEGACY:
        raise Http404
    if target == "proof":
        services.refuse_proof_string(path)
        url = reverse("designpreview:proof", kwargs={"path": path})
    else:
        url = reverse(f"designpreview:{LEGACY[target]}")
    query = request.META.get("QUERY_STRING", "")
    return HttpResponseRedirect(f"{url}?{query}" if query else url)


# ---------------------------------------------------------------------------------------------
# The foundation's specimen boards (V5.4 W1-0)
# ---------------------------------------------------------------------------------------------

#: A specimen board's name: lower-case words of letters and digits joined by single hyphens
#: («type», «colour», «corners», «chip-board»), at most 64 characters. The name becomes a template
#: path, so anything else is a 404 — whatever the URL converter let through.
SPECIMEN_BOARD = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SPECIMEN_TEMPLATE = "dev/designpreview/specimens/{board}.html"


@_preview_only
def specimen(request, board: str):
    """
    A foundation family's specimen board — the type specimen, the colour register board, the corner
    and shadow board, the icon sheet, the chip board, the button and field set, the loader filmstrips
    (V5.4 plan §3.1 item 6): ``templates/dev/designpreview/specimens/<board>.html`` when it exists,
    404 otherwise.

    Rendered like a picker: in Italian, without the request's context processors and so without a
    query (the folder's README states what a board's template may rely on). Its policy is the site's
    own, unwidened: a board draws components on its page, frames nothing and is framed by nothing.
    """
    if len(board) > 64 or not SPECIMEN_BOARD.fullmatch(board):
        raise Http404
    try:
        template = loader.get_template(SPECIMEN_TEMPLATE.format(board=board))
    except TemplateDoesNotExist:
        raise Http404 from None
    with translation.override("it"):
        content = template.render({"board": board})
    response = HttpResponse(content)
    response.headers["Content-Language"] = "it"
    return response
