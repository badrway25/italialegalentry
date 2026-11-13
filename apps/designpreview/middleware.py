"""
The preview server's database ceiling. DEVELOPMENT ONLY.

Installed — first in ``MIDDLEWARE`` — by the preview block of config/settings/dev.py and by nothing
else: without ``DEBUG`` and ``ILE_DESIGN_PREVIEW=1`` this module is never imported.

Why it exists (docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md). ``runserver`` answers every TCP
connection on a thread of its own, without limit, and a thread that touches the database owns a
PostgreSQL connection. On 2 October 2026 five review agents drove headless browsers at the
preview, each page load opening six sockets or more; the server took one connection per socket
and kept it, and the 300 the shared PostgreSQL allows were gone — for every dev server and every
test lane on it, not only for this one. Raising the 300 would have moved the wall, not removed it.

What it guarantees: **this server never holds more than ``ILE_DESIGN_PREVIEW_DB_CEILING``
connections (8 unless the environment says otherwise), whatever arrives.**

How. A request takes one of that many slots before anything can read the database, and gives it
back *when its response leaves this middleware* — the first of the chain, so the last to see the
response — once its thread holds no connection any more:

* a thread opens a connection only while it holds a slot, so open connections ≤ slots taken ≤
  the ceiling. The main thread holds none: ``runserver`` closes what its migration check opened;
* a page is complete when it leaves: every other middleware has run, a template response is
  rendered, and nothing that follows — the server writing the bytes, ``request_finished`` —
  reads the database. So the thread's connection is closed here and the slot released before
  the page is sent. ``CONN_MAX_AGE = 0`` on the preview server means Django would close the
  connection at ``request_finished`` anyway; the guarantee rests neither on that setting staying
  as it is nor on that signal arriving. A connection inside an atomic block is left alone, and
  then the slot stays with the thread exactly as the connection does — under a WSGI server that
  cannot happen: it is a test's transaction;
* a file response likewise gives its slot back before it is sent: a file on disk asks the
  database nothing while it travels, and a slow reader of a large one must not keep others
  waiting;
* a stream that is not a file (``StreamingHttpResponse``; the preview has none, and ``apps/`` has
  none today) is the one response that keeps its slot while it is sent — its generator may read
  the database — and gives it back at ``request_finished``, when the server closes it. It is the
  one case that still depends on the signal, and the signal can fail to come (below): whoever
  adds a stream to the site must know that a client that resets after it can cost a slot;
* a request that finds every slot taken waits, up to ``WAIT_SECONDS``, then is answered 503 in
  plain words. Requests are short (a proof file a few milliseconds, the hub some sixty), so the
  wait is not seen; the 503 exists so that a stuck request can never become a server that hangs
  in silence;
* a request that announces a body reads it **before** it takes a slot, when the body is small
  enough to be read into memory anyway (``DATA_UPLOAD_MAX_MEMORY_SIZE``). The CSRF check reads the
  body of every POST, and it runs inside the slot: eight clients that announced a body and never
  sent it held all eight slots, and every page of the server — the landing, which reads nothing,
  included — answered 503 after twenty seconds (review W1-P, performance P-1). Such a client now
  ties up a thread of its own, never a slot. A body too large to be read into memory, or one sent
  without a length, is read where it always was.

Why not at ``request_finished`` (review W2-1, docs/design-v5/QA/PREVIEW_REVIEW_W2.md §2.3; the
commit before this one did that). Under ``runserver`` the signal is sent by
``ServerHandler.close()`` (django/core/servers/basehttp.py), which first reads whatever is left
of the request body and only then closes the response. A client that announced a body and never
sent it keeps that read — and the thread — waiting for as long as its socket stays open; one
that resets the connection after the answer makes the read fail, wsgiref swallows the error, the
signal is never sent and the thread ends. A slot returned at that signal is then lost for the
life of the process: nothing can give it back, nothing is logged when it goes, and the SQL
count below says 0. Measured by the review: eight POSTs answered 403 by the CSRF check before
their body was read, then reset — and hub, pickers and proof files answered 503 until a restart.
Aborted or reset GETs do not do this (160 lost nothing), so the preview's own routes cannot
trigger it; but the ceiling stands before every route of the site. Giving the slot back when the
response leaves removes the dependence: the signal, when it does come, finds nothing to return.

How to measure it: the preview's connections carry ``application_name = ile-design-preview``
(dev.py), so ``select count(*) from pg_stat_activity where application_name =
'ile-design-preview'`` is this server's count at any instant — 0 at rest, at most the ceiling
under any burst. It counts connections, not slots: a slot held without a connection (a stream
being sent) is invisible to it, which is why the 503 and its log line speak of slots.
"""

from __future__ import annotations

import contextlib
import logging
import threading

from django.conf import settings
from django.core.exceptions import RequestDataTooBig
from django.core.signals import request_finished
from django.db import connections
from django.http import FileResponse, HttpResponse

from designpreview.access import loggable

logger = logging.getLogger("ile.designpreview")

DEFAULT_CEILING = 8
#: Shorter than Playwright's default navigation timeout (30 s): a capture script that meets a
#: saturated preview reads a status and a sentence, not a timeout.
WAIT_SECONDS = 20

#: The slots this thread holds — the semaphore it took one from, or nothing.
_mine = threading.local()

#: The methods whose body nobody reads: a body they announce is left alone.
_BODILESS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE"})


def _read_a_small_body(request) -> None:
    """
    Read the body a request announced, before it takes a slot — once, and kept by ``HttpRequest``,
    which parses ``POST`` and ``FILES`` from it later. Only a body of a known length that would be
    read into memory anyway: a larger one is read where it always was, and an unreadable or
    oversized one meets the chain with the same error it meets today.
    """
    if request.method in _BODILESS:
        return
    try:
        length = int(request.META.get("CONTENT_LENGTH") or 0)
    except ValueError:
        return
    limit = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    if length <= 0 or (limit is not None and length > limit):
        return
    # UnreadablePostError is an OSError: a client that resets meets the chain as it does today.
    with contextlib.suppress(RequestDataTooBig, OSError):
        request.body  # noqa: B018 - read for its side effect: the body, in memory


def _close_what_is_left() -> None:
    """Close this thread's connections, except one that is inside an atomic block."""
    for connection in connections.all(initialized_only=True):
        if connection.connection is not None and not connection.in_atomic_block:
            connection.close()


def _holds_a_connection() -> bool:
    return any(connection.connection is not None for connection in connections.all(initialized_only=True))


def give_back(**kwargs) -> None:
    """Return this thread's slot, once the thread holds no connection. Also the ``request_finished`` receiver."""
    slots = getattr(_mine, "slots", None)
    if slots is None:
        return
    _close_what_is_left()
    if _holds_a_connection():
        return
    _mine.slots = None
    slots.release()


# Django connects its own ``close_old_connections`` when ``django.db`` is imported, long before
# this module: receivers run in the order they were connected, so the connection is closed first.
# No ``dispatch_uid``: the receiver and the slots it returns belong to this module object, and a
# second copy of the module, should one ever be imported under another name, needs its own.
request_finished.connect(give_back)


class ConnectionCeilingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ceiling = max(1, int(getattr(settings, "ILE_DESIGN_PREVIEW_DB_CEILING", DEFAULT_CEILING)))
        self.slots = threading.BoundedSemaphore(self.ceiling)

    def __call__(self, request):
        if getattr(_mine, "slots", None) is not self.slots:
            _read_a_small_body(request)
            if not self.slots.acquire(timeout=WAIT_SECONDS):
                return self.busy(request)
            _mine.slots = self.slots
        try:
            response = self.get_response(request)
        except BaseException:
            give_back()
            raise
        # A page is complete here and a file reads nothing while it travels: neither needs the
        # slot a moment longer, and neither may keep it until a signal that can fail to come
        # (module docstring). Only a stream that is not a file keeps its slot while it is sent.
        if isinstance(response, FileResponse) or not getattr(response, "streaming", False):
            give_back()
        return response

    def busy(self, request) -> HttpResponse:
        # The path is the request's choice: escaped, it cannot write a second line that looks like
        # the preview's own (review W1-P, security m7 — «persona qa-admin signed in» was forged so).
        logger.warning(
            "Design preview: the %s database slots stayed taken for %s s — %s answered 503.",
            self.ceiling,
            WAIT_SECONDS,
            loggable(request.path),
        )
        # Slots, not «connections in use»: a slot can be held with no connection open, and the
        # SQL count would then say 0 of a server that is saying 503.
        slots = "1 posto" if self.ceiling == 1 else f"{self.ceiling} posti"
        taken = "ed è preso" if self.ceiling == 1 else "e sono tutti presi"
        response = HttpResponse(
            f"Anteprima occupata: questo server ha {slots} per le richieste che usano il database, {taken} "
            f"da più di {WAIT_SECONDS} secondi. Riprovare tra poco.\n",
            status=503,
            content_type="text/plain; charset=utf-8",
        )
        # This response leaves before any other middleware has seen the request: it carries the
        # seals of a preview page itself, and says what it is to a browser that would guess.
        response["Retry-After"] = "2"
        response["Cache-Control"] = "no-store"
        response["X-Robots-Tag"] = "noindex, nofollow"
        response["X-Content-Type-Options"] = "nosniff"
        return response
