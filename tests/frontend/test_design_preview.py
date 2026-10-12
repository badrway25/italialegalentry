"""
The V5 live preview (apps/designpreview): absent unless asked for, honest and sealed when it is —
and, since V5.4, the live V5 product (docs/design-v5/V5_4_EXECUTION_PLAN.md §4).

**What it is now.** ``/__design-v5/`` opens the current best V5: the real ``/fr/`` page of this
server, in exactly one same-origin frame, under a strip of 40 px that sits outside the page and
says the build, the state of the page («V5 — council-passed» only where the steward's
``live_status.json`` says so, «V4 + fondation» everywhere else), its languages, the frame (the
window or a phone of 390), the personas, the steward's changelog, the index and the page alone.
``/__design-v5/index/`` lists every live surface, public and authenticated, in fr and ar, with
frames on demand — at most one pair at a time, which its script holds — the families' state, the
foundation's specimen boards and the V4 control on 8771, never on this server.
``POST /__design-v5/accedi/<persona>/`` and ``POST /__design-v5/esci/`` sign a browser in and out
as one of the four QA personas of the preview's own database — no password, never a staff account
nor any privileged role, never on the V4 control's database — and a persona session is read-only: an
unsafe method outside the preview is answered 403, signing out and the language switch excepted. A
real page may be framed by this origin only when the browser says it is being loaded into a
same-origin frame, for the preview's own caller, by GET, HEAD or POST (a form submitted inside the
frame, DL54-17); everything else keeps the site's policy. The index mirrors W1-0's census of 79 page
types, one row each, and the review fixes of round 1 (docs/design-v5/QA/v54/w1-p/) are held here
too: no blank frame, no strip that outgrows its row, no focus under the sticky strip.

**The research archive.** The hub of before V5.4 — the gate-0 comps of the design council, the
research prototypes of waves 1, 2 and 3, H-E with its measurement pages, the hero council's record,
the hero and type pickers, the compare view and the proof files — moved as it was to
``/__design-v5/research/``; its old addresses answer 302, and an old link to one of its anchors is
sent on by the landing's script. One group left it (plan §4.3): «Baseline V4 (controllo)», which
linked this server's own pages as V4.

**The guarantees held here** are the same as for the design showcase, and stronger: under the test
settings there is no app, no route and no view — a visitor meets a 404; with ``DEBUG`` on and
``ILE_DESIGN_PREVIEW`` set, every route answers only a loopback caller with no proxy header, on
this process's own ``Host`` — anything else is a 404 before the method is looked at; every page
says «do not index, do not store»; the proof server never leaves its root or serves a working file
— judged on the real path the file system opens, because on NTFS ``WORK~1`` is ``.work`` and a link
is its target; and the production Content-Security-Policy of every other page does not move by a
character. The tests of the preview run with the preview block of ``config/settings/dev.py``
installed as the owner's server reads it — its middleware chain (the database ceiling first, the
frame exception after CSP and X-Frame-Options, the read-only rule last), its cookie names, its
personas — read from the module itself (``dev_preview``).

Nothing the archive shows is approved, and it has to say so: on the hub wherever a candidate
stands — where a first screen is described and never ranked against the other four, and no
builder's recommendation stands — in the bar of the two pickers, at every window width, and in
the caption of each frame of the compare view: written in the markup is not enough, so three
tests open a browser and look where the owner would. What is not on disk is never linked —
«manca» on the hub, a plain sentence in a picker — and a combination that was never built is said
not to exist. What is on disk is looked up on every request: a file that arrives is linked at the
next reload, with no restart.

And the preview must not be able to take the database down again (2 October 2026,
docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md): no view asks for a transaction, a proof file, a
picker, the landing and the index open no connection at all, and a burst — fired here at the very
server class ``runserver`` builds, one thread per socket — leaves no PostgreSQL backend behind and
never holds more than the ceiling.

The proof directory is faked under ``tmp_path``: these tests must pass on a machine that has no
``C:/tmp/ile_v5_council``. The fake package carries a part of the research on purpose, so both
answers — framed, and missing — are exercised. Four tests look at the real directory when it is
there, and skip when it is not, so the hub's catalogue cannot silently drift away from the
package it describes: every catalogued file is on disk and servable, the CTA rig still reads the
primary the hub's links name, and the working folders beside the new entries stay closed by
their names and by their 8.3 aliases. The steward's ``live_status.json`` and changelog are faked
under ``tmp_path`` too, absent unless a test writes them.
"""

from __future__ import annotations

import collections
import concurrent.futures
import contextlib
import copy
import gc
import importlib
import json
import logging
import os
import re
import socket
import socketserver
import struct
import subprocess
import sys
import threading
import time
import types
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, StreamingHttpResponse
from django.test import Client, override_settings
from django.urls import Resolver404, clear_url_caches, resolve

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from cms.forbidden import scan  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
#: The live product.
LANDING = "/__design-v5/"
INDEX = "/__design-v5/index/"
ENTER = "/__design-v5/accedi/"
EXIT = "/__design-v5/esci/"
STATE_429 = "/__design-v5/stati/429/"
STATE_404 = "/__design-v5/stati/404/"
DECISIONS = "/__design-v5/decisioni/"
SPECIMENS = "/__design-v5/specimens/"
#: The research archive — the hub of before V5.4, moved as it was; ``HUB`` keeps its name in the
#: archive's own tests.
ARCHIVE = HUB = "/__design-v5/research/"
PICKER = "/__design-v5/research/hero/"
TYPE = "/__design-v5/research/type/"
PROOF = "/__design-v5/research/proof/"
COMPARE = "/__design-v5/research/compare/"
#: The archive's addresses before V5.4, which redirect.
OLD_PICKER = "/__design-v5/hero/"
OLD_TYPE = "/__design-v5/type/"
OLD_COMPARE = "/__design-v5/compare/"
OLD_PROOF = "/__design-v5/proof/"
DEFAULT_PROOF_DIR = Path("C:/tmp/ile_v5_council/proof")
NOT_APPROVED = "prototipo di ricerca — non approvato"
#: The owner's server: the port the preview answers on unless the environment says otherwise.
PORT = 8780
HOST = f"127.0.0.1:{PORT}"
CEILING = "designpreview.middleware.ConnectionCeilingMiddleware"
FRAMES = "designpreview.frames.PreviewFrameMiddleware"
READ_ONLY = "designpreview.personas.PersonaReadOnlyMiddleware"
#: The headers of a request a browser loads into a frame of a page of the same origin.
FRAMED = {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "same-origin"}


def _tall(lang: str, words: str) -> bytes:
    """A page taller than any window: each frame of the compare view must scroll on its own."""
    direction = " dir='rtl'" if lang == "ar" else ""
    return (
        f"<!doctype html><html lang='{lang}'{direction}><body>" + f"<p>{words}</p>" * 160 + "</body></html>"
    ).encode()


#: proof-relative files the fake package carries, with their bytes
FAKE_PACKAGE = {
    "index.html": b"<!doctype html><title>La prova</title>",
    "SIGNING_SHEET.md": b"# Scheda di firma\n",
    "home/phase3.html": b"<!doctype html><html lang='fr'><body class='home home--phase3'>H-0</body></html>",
    "home/phase3-ar.html": b"<!doctype html><html lang='ar'><body>H-0 ar</body></html>",
    "home/interim.html": b"<!doctype html><body>interim</body>",
    "home/home.js": b"export const home = 1;\n",
    "home/home.css": b".home{color:var(--ink)}\n",
    "home/build.py": b"print('never served')\n",
    "home/perf_run.log": b"never served\n",
    "home/options/ha-phase3.html": b"<!doctype html><body>H-A</body>",
    "home/options/hb-phase3.html": b"<!doctype html><body>H-B</body>",
    "home/options/hb-phase3-ar.html": b"<!doctype html><body>H-B ar</body>",
    "home/options/.git-status-after.txt": b"never served\n",
    "assets/css/tokens.css": b":root{--x:1}\n",
    "assets/fonts/v5.woff2": b"wOF2fake",
    "assets/img/mark.svg": b"<svg xmlns='http://www.w3.org/2000/svg'/>",
    "assets/img/door.webp": b"RIFFfake",
    "assets/img/shot.png": b"\x89PNGfake",
    "home/measure.json": b"{}",
    "tools/run.ps1": b"Write-Host never\n",
    ".work/notes.txt": b"never served\n",
    ".profiles/stream/Default/Cookies": b"never served\n",
    # Wave 1 of the research — a part of it. What is NOT here is as deliberate as what is:
    # H-D has no Arabic page, TYPE A has no documents page, TYPE C and A+ have nothing, «Lume» and
    # «Passo» are absent, and so is every Arabic navigation state.
    "research/hero/hc/index.html": b"<!doctype html><html lang='fr'><body>H-C</body></html>",
    "research/hero/hc/ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>H-C ar</body></html>",
    "research/hero/hc/explore.html": b"<!doctype html><body>H-C explore</body>",
    "research/hero/hc/.work/live-8771-fr.html": b"never served\n",
    "research/hero/hd/index.html": b"<!doctype html><html lang='fr'><body>H-D</body></html>",
    "research/hero/hd/build_hd.py": b"print('never served')\n",
    "research/type/index.html": b"<!doctype html><body>type research</body>",
    "research/type/V4/home.html": b"<!doctype html><body>V4 home</body>",
    "research/type/A/home.html": b"<!doctype html><body>TYPE A home</body>",
    "research/type/A/home-ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>TYPE A home ar</body></html>",
    "research/type/A/menu.html": b"<!doctype html><body>TYPE A menu</body>",
    "research/type/A/dashboard.html": b"<!doctype html><body>TYPE A dashboard</body>",
    "research/type/A/type.css": b":root{--type:1}\n",
    "research/type/B/home.html": b"<!doctype html><body>TYPE B home</body>",
    "research/type/B/case.html": b"<!doctype html><body>TYPE B case</body>",
    "research/loader/index.html": b"<!doctype html><body>loader picker</body>",
    "research/loader/mandata/index.html": b"<!doctype html><body>Mandata</body>",
    "research/navigation/index.html": b"<!doctype html><body>navigation</body>",
    "research/navigation/public-fr-sheet.html": b"<!doctype html><body>the phone sheet</body>",
    "research/navigation/app-fr.html": b"<!doctype html><body>the console</body>",
    "research/navigation/.evidence/raw.json": b"never served\n",
    "research/emil/prototype/drawer/index.html": b"<!doctype html><body>drawer</body>",
    "research/21st-group1/signature-cta/index.html": b"<!doctype html><body>CTA</body>",
    # Wave 2 — a part of it again: the code field has no Arabic page here, the stage, the motion
    # bench's Arabic page, the whole public audit and the Arabic page of the «Mes pièces» proposal
    # are absent. And nothing of H-E's own folder is here: what is not on disk says «manca», and
    # is linked by itself when it arrives.
    "research/21st-group2/code-field/index.html": b"<!doctype html><body>code field</body>",
    "research/21st-group2/code-field/measure.py": b"print('never served')\n",
    "research/21st-group4/proto/overlays.html": b"<!doctype html><body>tooltip</body>",
    "research/21st-group4/proto/overlays-ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>tooltip ar</body></html>",
    "research/motion/bench/index.html": b"<!doctype html><body>motion bench</body>",
    "research/uiux-platform/proto/shell-fr.html": b"<!doctype html><body>shell proposal</body>",
    "research/uiux-platform/proto/shell-ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>shell proposal ar</body></html>",
    "research/uiux-platform/proto/docs-fr.html": _tall("fr", "Mes pièces — la proposition de l’audit"),
    # Wave 3 and H-E's measurement pages — a part again. Absent on purpose: the Arabic journey, the
    # icon candidates, the Arabic door row, the Arabic twins of the CTA rig. Beside the pages, the
    # lanes' working folders and scripts, which the proof server must refuse.
    "research/documents/index.html": _tall("fr", "Mes pièces — la proposition des documents"),
    "research/documents/ar.html": _tall("ar", "مستنداتي"),
    "research/documents/anatomy.html": b"<!doctype html><body>the row and the register</body>",
    "research/documents/_tools/build.py": b"print('never served')\n",
    "research/journey/index.html": b"<!doctype html><html lang='fr'><body>La soglia V5.2</body></html>",
    "research/colour/specimen.html": b"<!doctype html><body>colour specimen</body>",
    "research/colour/build_specimen.py": b"print('never served')\n",
    "research/icons/sheet.html": b"<!doctype html><body>icon sheet</body>",
    "research/icons/sheet-ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>icon sheet ar</body></html>",
    "research/icons/families.html": b"<!doctype html><html lang='en'><body>icon families</body></html>",
    "research/images/proto/doors.html": b"<!doctype html><body>the door row</body>",
    "research/hero/he-motion/index.html": b"<!doctype html><body>the motion bench of H-E</body>",
    "research/hero/he-motion/probe_he_motion.py": b"print('never served')\n",
    "research/hero/he-motion/.work/frames.html": b"never served\n",
    "research/hero/he-21st/states.html": b"<!doctype html><body>CTA rig, states</body>",
    "research/hero/he-21st/stage.html": b"<!doctype html><body>CTA rig, stand-in first screen</body>",
    "research/hero/he-21st/measure.py": b"print('never served')\n",
    "research/hero/door-master/snippet.html": b"<!-- a fragment --><picture><img src='doorway-arch-400.webp' alt=''></picture>",
    "research/hero/door-master/check/door-snippet.html": b"<!doctype html><body>today's door, the snippet's door</body>",
    "research/hero/door-master/doorway-arch-400.webp": b"RIFFfake",
    "research/hero/door-master/.work/notes.html": b"never served\n",
}


@pytest.fixture
def proof_root(tmp_path: Path) -> Path:
    root = tmp_path / "proof"
    for relative, content in FAKE_PACKAGE.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    (tmp_path / "outside.html").write_bytes(b"<!doctype html><body>outside the root</body>")
    return root


#: The environment of a preview server, as dev.py reads it — removed before dev.py is imported, so
#: that the shell a test runs from (a lane exports its own port, its own PGAPPNAME) changes nothing.
PREVIEW_ENVIRONMENT = (
    "ILE_DESIGN_PREVIEW",
    "ILE_DESIGN_PREVIEW_PROOF_DIR",
    "ILE_DESIGN_PREVIEW_DB_CEILING",
    "ILE_DESIGN_PREVIEW_PORT",
    "ILE_DESIGN_PREVIEW_V4_ORIGIN",
    "ILE_DESIGN_PREVIEW_LIVE_STATUS",
    "ILE_DESIGN_PREVIEW_CHANGELOG",
    "PGAPPNAME",
    "DB_CONN_MAX_AGE",
)


@contextlib.contextmanager
def _dev_settings(mp: pytest.MonkeyPatch, **environment: str):
    """
    ``config/settings/dev.py`` imported under ``environment`` (DEBUG on unless it says otherwise),
    and every object of ``config.settings.base`` it writes in place put back afterwards — whatever
    happens.

    Two lines of dev.py write the base settings in place, on purpose: the development log level,
    and the development default ``DB_CONN_MAX_AGE`` 0 (main ``31048b6``, cherry-picked into
    design-v5 for V5.4 W1-0; its own test, tests/test_dev_database_connection_lifetime.py, runs in a
    fresh interpreter). Re-imported here, that second line would hand the test process's live
    connection whatever lifetime the shell exports, so the variable is removed for the duration —
    the line then writes the 0 the test settings already hold — and the entry is put back as it was.
    """
    from config.settings import base

    level_before = base.LOGGING["root"]["level"]
    database_before = dict(base.DATABASES["default"])
    for name in PREVIEW_ENVIRONMENT:
        mp.delenv(name, raising=False)
    mp.setenv("DJANGO_DEBUG", "1")
    for name, value in environment.items():
        mp.setenv(name, value)
    sys.modules.pop("config.settings.dev", None)
    try:
        yield importlib.import_module("config.settings.dev")
    finally:
        sys.modules.pop("config.settings.dev", None)
        base.LOGGING["root"]["level"] = level_before
        base.DATABASES["default"].clear()
        base.DATABASES["default"].update(database_before)


#: What the preview block of dev.py sets that the tests install as the owner's server has it.
DEV_PREVIEW_SETTINGS = (
    "MIDDLEWARE",
    "SESSION_COOKIE_NAME",
    "CSRF_COOKIE_NAME",
    "LANGUAGE_COOKIE_NAME",
    "ILE_DESIGN_PREVIEW_PORT",
    "ILE_DESIGN_PREVIEW_PERSONAS",
    "ILE_DESIGN_PREVIEW_ALLOWED_DATABASES",
    "ILE_DESIGN_PREVIEW_V4_ORIGIN",
    "ILE_DESIGN_PREVIEW_DB_CEILING",
)


@pytest.fixture(scope="session")
def dev_preview() -> types.SimpleNamespace:
    """
    The preview block of config/settings/dev.py as the owner's server reads it — ``DEBUG`` on and
    ``ILE_DESIGN_PREVIEW=1``, nothing else in the environment — read from the module itself, once:
    its middleware chain, its cookie names, its port, its personas, its databases, its V4 control.
    """
    with pytest.MonkeyPatch.context() as mp, _dev_settings(mp, ILE_DESIGN_PREVIEW="1") as dev:
        values = {name: copy.deepcopy(getattr(dev, name)) for name in DEV_PREVIEW_SETTINGS}
    return types.SimpleNamespace(**values)


@pytest.fixture
def preview(proof_root: Path, client, tmp_path: Path, dev_preview, monkeypatch):
    """
    The preview as the dev settings switch it on: DEBUG on, the flag on, the preview block of
    dev.py installed — its middleware chain, its cookie names, its port and its personas
    (``dev_preview``) — the proof directory pointed at the fake package, the steward's two files at
    paths under ``tmp_path`` (absent until a test writes them), the build the strip names fixed,
    and the test client calling as the owner's browser does: from 127.0.0.1, on ``127.0.0.1:8780``.
    The root URLconf is rebuilt, because config/urls.py decides at import time whether
    ``/__design-v5/`` exists. Put back afterwards.

    Two settings differ from the owner's server, on purpose. The databases a persona may be opened
    on are ``ile_v5`` alone — the test database is not among them, so a persona is refused unless a
    test says otherwise (``this_database``): the guard is read from its setting, and the happy path
    is testable. And INSTALLED_APPS is NOT overridden: the app has no models and no app-directory
    templates (they live under templates/dev/), so the routes work without it; and in this project
    ``override_settings(INSTALLED_APPS=…)`` re-populates the app registry in a way that empties
    ``admin.site._registry`` for the rest of the process — the admin tests after this file would
    fail. The registration itself is covered by test_dev_settings_read_the_flag_from_the_environment
    and test_manage_check_passes_with_the_preview_on, which exercise the real dev settings.
    """
    from designpreview import live

    import config.urls

    monkeypatch.setattr(
        live, "identity", lambda: {"tag": "v54/base", "branch": "", "commit": "f11d131", "date": "2026-10-05"}
    )
    installed = {name: getattr(dev_preview, name) for name in DEV_PREVIEW_SETTINGS}
    installed["ILE_DESIGN_PREVIEW_ALLOWED_DATABASES"] = ("ile_v5",)
    with override_settings(
        DEBUG=True,
        ILE_DESIGN_PREVIEW=True,
        ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root,
        ILE_DESIGN_PREVIEW_LIVE_STATUS=tmp_path / "steward" / "live_status.json",
        ILE_DESIGN_PREVIEW_CHANGELOG=tmp_path / "steward" / "CHANGELOG_V54.md",
        **installed,
    ):
        client.defaults["HTTP_HOST"] = HOST
        clear_url_caches()
        importlib.reload(config.urls)
        yield proof_root
    clear_url_caches()
    importlib.reload(config.urls)


def _steward(tmp_path: Path, name: str, content: str) -> Path:
    """Write one of the steward's files where the ``preview`` fixture points the preview at it."""
    target = tmp_path / "steward" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content.encode("utf-8"))
    return target


def _test_database_name() -> str:
    from django.db import connection

    return connection.settings_dict["NAME"]


@pytest.fixture
def this_database():
    """The test database among those a persona may be opened on — the happy path of the switch."""
    name = _test_database_name()
    with override_settings(ILE_DESIGN_PREVIEW_ALLOWED_DATABASES=(name,)):
        yield name


@pytest.fixture
def accounts(django_user_model):
    """The QA accounts as the preview's database holds them — none with a usable password."""
    made = {
        key: django_user_model.objects.create_user(email=f"{key}@example.test", password=None, full_name=key)
        for key in ("qa-doc-person", "qa-person", "qa-fresh-person", "qa-company")
    }
    made["qa-admin"] = django_user_model.objects.create_superuser(email="qa-admin@example.test", password=None)
    assert not any(user.has_usable_password() for user in made.values())
    return made


@pytest.fixture
def served(live_server, preview):
    """
    The archive's browser tests on pytest-django's ``live_server``: the preview answers that
    server's own port. (Its middleware chain is the test settings' — it was built before this test
    began — which the archive's pages do not need: a proof file says ``frame-ancestors 'self'``
    itself.)
    """
    with override_settings(ILE_DESIGN_PREVIEW_PORT=int(live_server.url.rsplit(":", 1)[1])):
        yield live_server.url


@pytest.fixture
def dev_server(preview):
    """
    The live product in a browser: the server ``runserver`` builds, with the middleware chain of the
    preview block and the static files ``runserver`` serves — a real page is framed through
    ``designpreview.frames``, which ``live_server``'s chain, built at the start of the session, has
    not got. The preview answers that server's own port.
    """
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    from django.core.handlers.wsgi import WSGIHandler

    handler = StaticFilesHandler(WSGIHandler())
    with _runserver(handler) as base:
        yield base


def _csp(response) -> str:
    return response.get("Content-Security-Policy", "")


def _assert_sealed(response) -> None:
    assert response["X-Robots-Tag"] == "noindex, nofollow"
    assert "no-store" in response["Cache-Control"]


def _refused(response) -> None:
    """
    What a refused caller meets: a plain 404 that names nothing of the preview — not its seals, not a
    view, not the CSRF check (review W1-P, security m1).
    """
    assert response.status_code == 404, response.status_code
    assert "X-Robots-Tag" not in response
    assert b"designpreview" not in response.content and b"CSRF" not in response.content


# --------------------------------------------------------------------------- absence


def test_absent_without_the_flag():
    """Under the test settings there is no route (resolver level, no database needed) and no app."""
    for path in (
        LANDING,
        INDEX,
        ENTER + "qa-doc-person/",
        EXIT,
        STATE_429,
        DECISIONS + "w1-a/CD_DECISION.md",
        OLD_PICKER,
        OLD_PROOF + "home/phase3.html",
    ):
        with pytest.raises(Resolver404):
            resolve(path)
    with pytest.raises(Resolver404):
        resolve(HUB)
    with pytest.raises(Resolver404):
        resolve(PICKER)
    with pytest.raises(Resolver404):
        resolve(TYPE)
    with pytest.raises(Resolver404):
        resolve(COMPARE)
    with pytest.raises(Resolver404):
        resolve(SPECIMENS + "type/")
    assert "designpreview" not in settings.INSTALLED_APPS
    assert not hasattr(settings, "ILE_DESIGN_PREVIEW"), "only config/settings/dev.py may define the flag"
    for name in ("ILE_DESIGN_PREVIEW_PORT", "ILE_DESIGN_PREVIEW_PERSONAS", "ILE_DESIGN_PREVIEW_ALLOWED_DATABASES"):
        assert not hasattr(settings, name), name
    assert settings.SESSION_COOKIE_NAME == "sessionid" and settings.CSRF_COOKIE_NAME == "csrftoken"
    assert settings.LANGUAGE_COOKIE_NAME == "ile_language"
    assert FRAMES not in settings.MIDDLEWARE and READ_ONLY not in settings.MIDDLEWARE


@pytest.mark.django_db
def test_answers_404_without_the_flag(client):
    for path in (LANDING, INDEX, STATE_429, OLD_PICKER, DECISIONS + "w1-a/CD_DECISION.md"):
        assert client.get(path).status_code == 404, path
        assert client.get(path, HTTP_HOST=HOST).status_code == 404, path
    for path in (ENTER + "qa-doc-person/", EXIT):
        assert client.post(path, HTTP_HOST=HOST).status_code == 404, path
    assert client.get(HUB).status_code == 404
    assert client.get(PICKER).status_code == 404
    assert client.get(TYPE).status_code == 404
    assert client.get(COMPARE).status_code == 404
    assert client.get(SPECIMENS + "type/").status_code == 404
    assert client.get(PROOF + "home/phase3.html").status_code == 404
    assert client.get(PROOF + "research/hero/hc/index.html").status_code == 404


def test_the_views_refuse_even_if_someone_wires_them_up(rf, proof_root):
    """
    A URLconf is a file: the views check DEBUG, the flag, the loopback address, the proxy headers and
    the host themselves — the new ones as the old — and answer a plain 404 that names nothing: under
    DEBUG an ``Http404`` would be Django's technical page, which names the view (security m1).
    """
    from designpreview import views

    def every_view(request_for):
        yield views.landing, request_for(LANDING), {}
        yield views.index, request_for(INDEX), {}
        yield views.hub, request_for(HUB), {}
        yield views.state, request_for(STATE_429), {"code": "429"}
        yield views.decision, request_for(DECISIONS + "w1-a/CD_DECISION.md"), {"path": "w1-a/CD_DECISION.md"}
        yield views.legacy, request_for(OLD_PICKER), {"target": "hero"}
        yield views.persona_enter, request_for(ENTER + "qa-doc-person/", "post"), {"persona": "qa-doc-person"}
        yield views.persona_exit, request_for(EXIT, "post"), {}

    rf.defaults["HTTP_HOST"] = HOST
    for switches in ({"DEBUG": True, "ILE_DESIGN_PREVIEW": False}, {"DEBUG": False, "ILE_DESIGN_PREVIEW": True}):
        with override_settings(**switches, ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root):
            for view, request, kwargs in every_view(lambda path, verb="get": getattr(rf, verb)(path)):
                _refused(view(request, **kwargs))
    with override_settings(DEBUG=True, ILE_DESIGN_PREVIEW=True, ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root):
        for caller in (
            {"REMOTE_ADDR": "10.0.0.9"},
            {"HTTP_X_FORWARDED_FOR": "127.0.0.1"},
            {"HTTP_HOST": "localhost:8781"},
        ):
            for view, request, kwargs in every_view(
                lambda path, verb="get", caller=caller: getattr(rf, verb)(path, **caller)
            ):
                _refused(view(request, **kwargs))
    rf.defaults.pop("HTTP_HOST")
    with override_settings(DEBUG=True, ILE_DESIGN_PREVIEW=False, ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root):
        _refused(views.hub(rf.get(HUB)))
        _refused(views.hero(rf.get(PICKER)))
        _refused(views.type_systems(rf.get(TYPE)))
        _refused(views.compare(rf.get(COMPARE)))
        _refused(views.proof(rf.get(PROOF + "home/phase3.html"), path="home/phase3.html"))
        _refused(views.specimen(rf.get(SPECIMENS + "type/"), board="type"))
    with override_settings(DEBUG=False, ILE_DESIGN_PREVIEW=True, ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root):
        _refused(views.hub(rf.get(HUB)))
        _refused(views.type_systems(rf.get(TYPE)))
        _refused(views.specimen(rf.get(SPECIMENS + "type/"), board="type"))
    with override_settings(DEBUG=True, ILE_DESIGN_PREVIEW=True, ILE_DESIGN_PREVIEW_PROOF_DIR=proof_root):
        _refused(views.proof(rf.get(PROOF + "home/phase3.html", REMOTE_ADDR="10.0.0.9"), path="home/phase3.html"))
        _refused(views.type_systems(rf.get(TYPE, REMOTE_ADDR="10.0.0.9")))
        _refused(views.compare(rf.get(COMPARE, REMOTE_ADDR="10.0.0.9")))
        _refused(views.specimen(rf.get(SPECIMENS + "type/", REMOTE_ADDR="10.0.0.9"), board="type"))


def test_dev_settings_read_the_flag_from_the_environment(monkeypatch):
    """
    ``config/settings/dev.py`` is the one place that knows ``ILE_DESIGN_PREVIEW``: off by default,
    on with the environment variable, never on with DEBUG off — and the app is installed only then.

    The same block is the one place that changes how the preview server holds the database — a
    connection lives for one request, the ceiling's middleware stands first, the connections carry
    a name — and, since V5.4, everything the live product needs (plan §4.4): the port it answers,
    the four personas and the databases they may be opened on, the steward's two files, the V4
    control, cookie names of its own, and the two middleware of the frames and of the read-only
    personas. It does so on objects of its own: ``base.DATABASES`` and ``base.MIDDLEWARE`` are every
    environment's, and in this very process they are the test's. (``_dev_settings`` says how the
    one line that writes the base entry in place is kept from the shell, and put back.)
    """
    from config.settings import base

    database_before = dict(base.DATABASES["default"])
    middleware_before = list(base.MIDDLEWARE)
    with _dev_settings(monkeypatch) as dev:
        assert dev.DEBUG is True
        assert dev.ILE_DESIGN_PREVIEW is False
        assert "designpreview" not in dev.INSTALLED_APPS
        assert dev.ILE_DESIGN_PREVIEW_PROOF_DIR == DEFAULT_PROOF_DIR
        # Without the flag the database settings and the middleware are the base's own objects,
        # and nothing of the live product exists.
        assert dev.DATABASES is base.DATABASES and dev.MIDDLEWARE is base.MIDDLEWARE
        assert CEILING not in dev.MIDDLEWARE and FRAMES not in dev.MIDDLEWARE and READ_ONLY not in dev.MIDDLEWARE
        for name in (
            "ILE_DESIGN_PREVIEW_DB_CEILING",
            "ILE_DESIGN_PREVIEW_PORT",
            "ILE_DESIGN_PREVIEW_PERSONAS",
            "ILE_DESIGN_PREVIEW_ALLOWED_DATABASES",
            "ILE_DESIGN_PREVIEW_LIVE_STATUS",
            "ILE_DESIGN_PREVIEW_CHANGELOG",
            "ILE_DESIGN_PREVIEW_V4_ORIGIN",
        ):
            assert not hasattr(dev, name), name
        # Django's own cookie names, and the base's language cookie.
        assert not hasattr(dev, "SESSION_COOKIE_NAME") and not hasattr(dev, "CSRF_COOKIE_NAME")
        assert dev.LANGUAGE_COOKIE_NAME == "ile_language"

    with _dev_settings(monkeypatch, ILE_DESIGN_PREVIEW="1", ILE_DESIGN_PREVIEW_PROOF_DIR="C:/elsewhere/proof") as dev:
        assert dev.ILE_DESIGN_PREVIEW is True
        assert dev.INSTALLED_APPS[-1] == "designpreview"
        assert "designpreview" not in base.INSTALLED_APPS, "the base list must stay untouched"
        assert dev.ILE_DESIGN_PREVIEW_PROOF_DIR == Path("C:/elsewhere/proof")
        # The preview server and the database: one request per connection, a ceiling, a name.
        database = dev.DATABASES["default"]
        assert database["CONN_MAX_AGE"] == 0, "a connection must not outlive its request"
        assert database["CONN_HEALTH_CHECKS"] is True
        assert database["OPTIONS"]["application_name"] == "ile-design-preview"
        assert database["ATOMIC_REQUESTS"] is True, "the rest of the site keeps its transactions"
        changed = {key for key in database if database[key] != database_before.get(key)}
        assert changed <= {"CONN_MAX_AGE", "CONN_HEALTH_CHECKS", "OPTIONS"}, changed
        assert set(database_before) <= set(database), "nothing of the base entry is dropped"
        assert dev.ILE_DESIGN_PREVIEW_DB_CEILING == 8
        # The chain: the ceiling first; the frame exception after CSP and X-Frame-Options; the
        # read-only rule last; the base chain between them, as it is.
        assert dev.MIDDLEWARE == [CEILING, *middleware_before, FRAMES, READ_ONLY]
        # The live product: the owner's port, the four personas — never the staff account — the
        # databases they may be opened on — never the V4 control's — the steward's files, the V4
        # control on 8771, and the cookie names of its own.
        assert dev.ILE_DESIGN_PREVIEW_PORT == 8780
        assert dev.ILE_DESIGN_PREVIEW_PERSONAS == {
            "qa-doc-person": "qa-doc-person@example.test",
            "qa-person": "qa-person@example.test",
            "qa-fresh-person": "qa-fresh-person@example.test",
            "qa-company": "qa-company@example.test",
        }
        assert dev.ILE_DESIGN_PREVIEW_ALLOWED_DATABASES == (
            "ile_v5",
            "ile_v5_l3",
            "ile_v5_l4",
            "ile_v5_l5",
            "ile_v5_l6",
            "ile_v5_l7",
            "ile_v5_l8",
            "ile_v5_l9",
        )
        assert dev.ILE_DESIGN_PREVIEW_LIVE_STATUS == base.BASE_DIR / "docs" / "design-v5" / "live_status.json"
        assert dev.ILE_DESIGN_PREVIEW_CHANGELOG == base.BASE_DIR / "docs" / "design-v5" / "CHANGELOG_V54.md"
        assert dev.ILE_DESIGN_PREVIEW_V4_ORIGIN == "http://127.0.0.1:8771"
        assert (dev.SESSION_COOKIE_NAME, dev.CSRF_COOKIE_NAME, dev.LANGUAGE_COOKIE_NAME) == (
            "ile_v5_sessionid",
            "ile_v5_csrftoken",
            "ile_v5_language",
        )
        # … on objects of its own.
        assert base.DATABASES["default"] == database_before, "the base settings must stay untouched"
        assert base.MIDDLEWARE == middleware_before and CEILING not in base.MIDDLEWARE
        assert base.LANGUAGE_COOKIE_NAME == "ile_language" and not hasattr(base, "SESSION_COOKIE_NAME")

    # The knobs the environment has: the ceiling, the name libpq would have used, the lane's port,
    # the V4 control.
    with _dev_settings(
        monkeypatch,
        ILE_DESIGN_PREVIEW="1",
        ILE_DESIGN_PREVIEW_DB_CEILING="3",
        PGAPPNAME="a-lane-of-its-own",
        ILE_DESIGN_PREVIEW_PORT="8784",
        ILE_DESIGN_PREVIEW_V4_ORIGIN="http://127.0.0.1:8770",
    ) as dev:
        assert dev.ILE_DESIGN_PREVIEW_DB_CEILING == 3
        assert dev.DATABASES["default"]["OPTIONS"]["application_name"] == "a-lane-of-its-own"
        assert dev.ILE_DESIGN_PREVIEW_PORT == 8784
        assert dev.ILE_DESIGN_PREVIEW_V4_ORIGIN == "http://127.0.0.1:8770"
        assert "ile_qa" not in dev.ILE_DESIGN_PREVIEW_ALLOWED_DATABASES

    with _dev_settings(monkeypatch, ILE_DESIGN_PREVIEW="1", DJANGO_DEBUG="0") as dev:
        assert dev.DEBUG is False
        assert dev.ILE_DESIGN_PREVIEW is False, "the flag alone must never switch the preview on"
        assert "designpreview" not in dev.INSTALLED_APPS
        assert dev.DATABASES is base.DATABASES and dev.MIDDLEWARE is base.MIDDLEWARE
        assert not hasattr(dev, "SESSION_COOKIE_NAME") and not hasattr(dev, "ILE_DESIGN_PREVIEW_PERSONAS")
    assert base.DATABASES["default"] == database_before
    assert base.MIDDLEWARE == middleware_before


def test_manage_check_passes_with_the_preview_on(tmp_path):
    """
    ``manage.py check designpreview`` under the dev settings with the flag on: the app is installed
    (an unknown label is an error) and registers cleanly, with the URLconf that mounts it.

    The check is asked about this app, not about the project. Asked about the project it failed on
    2 October 2026 for a reason that is nobody's defect: ``forum.ForumEvent.date`` defaults to the
    day of the Forum, ``dt.date(2026, 10, 2)``, and Django's ``fields.W161`` («Fixed default value
    provided») fires on the one day a fixed default equals today. Another app's warning is not
    this test's subject; the URL, template and security checks still run with a label.
    """
    env = dict(os.environ)
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "config.settings.dev",
            "DJANGO_DEBUG": "1",
            "ILE_DESIGN_PREVIEW": "1",
            "ILE_DESIGN_PREVIEW_PROOF_DIR": str(tmp_path),
            "PYTHONIOENCODING": "utf-8",
        }
    )
    result = subprocess.run(
        [sys.executable, "manage.py", "check", "designpreview"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no issues" in result.stdout, result.stdout


# --------------------------------------------------------------------------- the hub


@pytest.mark.django_db
def test_the_hub_lists_every_surface_and_is_sealed(client, preview):
    response = client.get(HUB)
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert '<html lang="it" dir="ltr"' in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
    # The five first screens the council examined, as files and through the picker: three of
    # gate 0, two of the research. (H-E, the sixth, has its own test, below.)
    for href in (
        PROOF + "home/phase3.html",
        PROOF + "home/phase3-ar.html",
        PROOF + "home/options/ha-phase3.html",
        PROOF + "home/options/hb-phase3.html",
        PROOF + "home/options/hb-phase3-ar.html",
        PROOF + "research/hero/hc/index.html",
        PROOF + "research/hero/hc/ar.html",
        PROOF + "research/hero/hc/explore.html",
        PROOF + "research/hero/hd/index.html",
    ):
        assert f'href="{href}"' in html, href
    for variant in ("h0", "ha", "hb", "hc", "hd"):
        assert f'href="{PICKER}?variant={variant}&amp;lang=fr&amp;phase=3"' in html, variant
    for code, name in (("H-C", "Quattro soglie, una chiave"), ("H-D", "La porta, di giorno")):
        assert f'<span class="dp-surface__code">{code}</span> {name}</h3>' in html, code
    assert html.count("non ancora disponibile") == 4  # the four upcoming surfaces, and nothing else
    # Every group is present: the gate-0 viewing order, then the research, the control, what is to come.
    order = [
        "La home — il primo schermo (O67)",
        "H-E — nuova direzione",
        "Consiglio sull’hero",
        "Navbar e mega-menu",
        "Accesso «Il varco»",
        "Guscio della piattaforma e cruscotto della persona",
        "Spazio documenti",
        "Il passaggio «La soglia» e il prototipo delle luci",
        "Tavola telefono (misura)",
        "Il caricatore di firma",
        "Vetrina dei componenti (fondazione)",
        "Il pacchetto di firma",
        "Ricerca — sistemi tipografici TYPE A / B / C / D",
        "Ricerca — il caricatore di firma, tre candidati",
        "Ricerca — navigazione pubblica e di console",
        "Ricerca — il cassetto della console, il movimento",
        "Ricerca — la CTA di firma",
        "Ricerca, seconda ondata — tre componenti dalla rassegna 21st",
        "Ricerca, seconda ondata — il banco di prova del movimento",
        "Ricerca, seconda ondata — le proposte dei due audit UI-UX-Pro-Max",
        "Ricerca, terza ondata — «Mes pièces» V5.2",
        "Ricerca, terza ondata — «La soglia» V5.2",
        "Ricerca, terza ondata — i colori della piattaforma",
        "Ricerca, terza ondata — le icone",
        "Ricerca, terza ondata — la fila delle porte",
        "In arrivo (V5.2 §7.2)",
    ]
    assert len(order) == 26, "«Baseline V4 (controllo)» left the archive (plan §4.3)"
    positions = [html.index(f"</span>{title}</a>") for title in order]
    assert positions == sorted(positions), "the table of contents is not in the viewing order"
    assert html.count('<li class="dp-group"') == len(order)
    # No group links this server's own live pages as the V4 control any more: that is V5 now.
    for live in ("/fr/", "/fr/compte/login/", "/fr/espace-reserve/", "/ar/"):
        assert f'href="{live}"' not in html, live
    # The recommended widths and the warning that nothing is approved.
    for width in (1440, 1280, 1024, 768, 430, 390, 375, 360):
        assert f'<li class="dp-chip">{width}</li>' in html, width
    assert "Niente di ciò che è mostrato è approvato" in html
    # A comp missing from the package is said to be missing, never linked to a 404.
    assert PROOF + "home/interim-ar.html" not in html
    assert "ar · intérim · manca" in html


@pytest.mark.django_db
def test_the_hub_is_product_clean(client, preview):
    """No inline style (CSP), no forbidden wording, no id used twice, no leaked template comment."""
    html = client.get(HUB).content.decode()
    assert not re.search(r"<[^>]+\sstyle=", html), "an inline style attribute cannot survive the CSP"
    assert scan(html) == []
    ids = re.findall(r'\sid="([^"]+)"', html)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    assert not duplicates, duplicates
    assert "{#" not in html and "{%" not in html
    # The hub loads its own dev stylesheet and the site's bundled cascade, nothing external.
    assert "css/dev/designpreview.css" in html
    assert not re.findall(r'(?:src|href)="https?://', html)


@pytest.mark.django_db
def test_the_hub_answers_head(client, preview):
    response = client.head(HUB)
    assert response.status_code == 200
    _assert_sealed(response)


@pytest.mark.django_db
def test_the_hub_refuses_a_caller_that_is_not_loopback(client, preview):
    assert client.get(HUB, REMOTE_ADDR="192.168.1.20").status_code == 404
    assert client.get(PICKER, REMOTE_ADDR="192.168.1.20").status_code == 404
    assert client.get(TYPE, REMOTE_ADDR="192.168.1.20").status_code == 404
    assert client.get(COMPARE, REMOTE_ADDR="192.168.1.20").status_code == 404
    assert client.get(PROOF + "home/phase3.html", REMOTE_ADDR="192.168.1.20").status_code == 404


def _group_of(html: str, key: str) -> str:
    """The markup of one group of the hub, from its opening tag to the next group's."""
    start = html.index(f'<li class="dp-group" id="g-{key}">')
    end = html.find('<li class="dp-group"', start + 1)
    return html[start : end if end != -1 else len(html)]


@pytest.mark.django_db
def test_the_hub_says_that_a_research_prototype_is_not_approved_wherever_one_stands(client, preview):
    """
    The warning at the top of the page is not enough: every research group carries the status
    under its title — H-E's too — and so do H-C and H-D, which sit among the gate-0 comps, with the
    one honest line that says who has looked at them and whose decision it is. Since 2 October
    that line names the hero council: «revisione indipendente in attesa» stopped being true the
    day five chairs reported.

    Review W1-1: that line does not say what the judgement is. The hub is the page the owner
    decides O67 on: a first screen is described, with what it asks of the rules, and is not
    measured against the others in the hub's own voice. Review W2-2: nor in the council's — the
    order its majority gave (three 3–2 comparisons, a fourth place with no majority, and the
    owner's «non voglio scegliere sulla base del report del council») is not on the page at all;
    it stands in the minutes, with its reservations, and the hub prints the path to the minutes.
    """
    html = client.get(HUB).content.decode()
    tag = f'<p class="dp-tag">{NOT_APPROVED}</p>'
    for key in (
        "he",
        "type",
        "research-loader",
        "research-navigation",
        "research-drawer",
        "research-cta",
        "research-21st",
        "research-motion",
        "research-uiux",
        "research-documents",
        "research-journey",
        "research-colour",
        "research-icons",
        "research-images",
    ):
        group = _group_of(html, key)
        head = group[: group.index('<ul class="dp-surfaces"')]
        assert tag in head, key
    home = _group_of(html, "home")
    assert home.count(tag) == 2, "H-C and H-D, and only they, are research among the gate-0 first screens"
    for code in ("H-C", "H-D"):
        row = home[home.index(f'<span class="dp-surface__code">{code}</span>') :]
        row = row[: row.index("</li>")]
        assert tag in row, code
        for words in (
            "Il consiglio sull’hero l’ha esaminata il 2 ottobre",
            "il verbale è nel gruppo «Consiglio sull’hero»",
            "Decide il proprietario (O67).",
        ):
            assert words in row, (code, words)
        assert "revisione indipendente in attesa" not in row and "solo autore" not in row, code
    for code in ("H-0", "H-A", "H-B"):
        row = home[home.index(f'<span class="dp-surface__code">{code}</span>') :]
        assert tag not in row[: row.index("</li>")], f"{code} is a gate-0 comp"
    # No first screen is ranked: not in the lead of the group, not in a note.
    notes = re.findall(r'<p class="dp-surface__note">(.*?)</p>', home, flags=re.S)
    assert len(notes) == 5
    for words in ("più forte", "superiore", "migliore"):
        assert words not in home.lower(), words
    # … and a research direction is not set against another variant at all: its note names none.
    for code, note in (("H-C", notes[3]), ("H-D", notes[4])):
        assert not re.search(r"\bH-[0A-D]\b", note), (code, note)
    # What a research direction asks of the rules is said, as a fact the owner needs.
    assert "Chiede due emendamenti alla Direzione creativa e poggia su fotografie provvisorie." in notes[3]
    assert "Il primo schermo non è più notturno, e il §9 della Direzione creativa andrebbe emendato." in notes[4]
    # The recommendation H-B carries is the gate's, and the gate had three first screens, not five.
    assert "che avevano davanti le sole H-0, H-A e H-B" in notes[2]
    # The control of the type research is not a proposal, and says so.
    assert '<p class="dp-tag">controllo — non una proposta</p>' in _group_of(html, "type")
    # No gate-0 group is labelled as research, and neither is the council's record.
    for key in (
        "council",
        "navbar",
        "login",
        "shell",
        "documents",
        "journey",
        "phone",
        "loader",
        "components",
        "package",
    ):
        assert NOT_APPROVED not in _group_of(html, key), key
    assert (
        "I prototipi di ricerca portano soltanto il giudizio di chi li ha costruiti — tranne i cinque primi "
        "schermi, che il consiglio sull’hero ha esaminato il 2 ottobre, e H-E, la cui revisione indipendente al 4 "
        "ottobre non è conclusa: per gli altri la revisione indipendente è in attesa."
    ) in html
    # The order of the council's majority is nowhere on the page — not even as the council's.
    council = _group_of(html, "council")
    assert "L’ordine di preferenza dei seggi sta nel verbale, con le sue riserve, e non in questa pagina." in council
    assert "H-D, H-C, H-A, H-B, H-0" not in html
    for words in ("maggioranza", "ordine dato", "classifica", "primo posto", "ultimo posto"):
        assert words not in html.lower(), words
    for words in ("più forte", "superiore", "migliore", "raccomand"):
        assert words not in council.lower(), words


@pytest.mark.django_db
def test_the_hub_keeps_a_warning_with_its_own_link(client, preview):
    """
    Review W1-4. «da non firmare come /ar/» is said of one link. The two were separate items of a
    wrapping row, and at 360–390 px the warning went to the next line and stood beside the
    following link. They are one item now, a box that does not wrap; a link with nothing to warn
    about has no such box.
    """
    html = client.get(HUB).content.decode()
    assert (
        f'<span class="dp-link-pair"><a class="dp-link dp-link--proof" href="{PROOF}home/phase3-ar.html" '
        'hreflang="ar">ar · fase 3</a><span class="dp-link__note">da non firmare come /ar/</span></span>'
    ) in html
    # H-0, H-B and H-C have their Arabic page in this package; H-A and H-D do not, and say «manca».
    assert html.count('<span class="dp-link-pair">') == html.count('<span class="dp-link__note">') == 3
    assert html.count('<span class="dp-link-pair"><a class="dp-link ') == 3, "a pair opens on its link"
    assert html.count('</a><span class="dp-link__note">da non firmare come /ar/</span></span>') == 3, "and closes on it"
    css = (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8")
    pair = _declarations(re.sub(r"/\*.*?\*/", "", css, flags=re.S), ".dp-link-pair")
    assert "display: inline-flex" in pair and "flex-wrap" not in pair


@pytest.mark.django_db
def test_the_hub_lists_the_research_prototypes_with_their_states(client, preview):
    """The loader, the navigation with its phone states, the drawer, the CTA, the type picker's entries."""
    html = client.get(HUB).content.decode()
    # Plain files, and the query string that opens a prototype in one of its states — printed in the label.
    for href, label in (
        (PROOF + "research/loader/index.html", "confronto"),
        (PROOF + "research/loader/mandata/index.html", "tavole fr e ar"),
        (PROOF + "research/loader/mandata/index.html?rm=1", "movimento ridotto · ?rm=1"),
        (PROOF + "research/navigation/index.html", "indice"),
        (PROOF + "research/navigation/public-fr-sheet.html?drawer=1", "fr · ?drawer=1"),
        (PROOF + "research/navigation/app-fr.html", "fr"),
        (PROOF + "research/navigation/app-fr.html?drawer=1", "fr · ?drawer=1"),
        (PROOF + "research/emil/prototype/drawer/index.html", "fr"),
        (PROOF + "research/emil/prototype/drawer/index.html?exit=out", "fr · altra curva d’uscita · ?exit=out"),
        (PROOF + "research/emil/prototype/drawer/index.html?rm=1", "fr · movimento ridotto · ?rm=1"),
        (PROOF + "research/21st-group1/signature-cta/index.html", "fr"),
        (PROOF + "research/type/index.html", "indice della ricerca"),
    ):
        assert re.search(
            rf'<a class="dp-link dp-link--proof" href="{re.escape(href)}"[^>]*>{re.escape(label)}</a>', html
        ), href
    # The three loader candidates are named, each for what answers.
    for name in ("«Mandata» — risponde la porta", "«Lume» — risponde la luce", "«Passo» — risponde il percorso"):
        assert name in html, name
    # The two navigation proposals, public and console.
    navigation = _group_of(html, "research-navigation")
    assert "N-A «Il sommario»" in navigation and "P-A «Tre livelli»" in navigation
    assert navigation.count('<span class="dp-surface__code">N-A</span>') == 7
    assert navigation.count('<span class="dp-surface__code">P-A</span>') == 4
    # The type picker is entered from the hub: two entries per sheet, the public face and the console's.
    for system in ("v4", "a", "b"):
        assert f'href="{TYPE}?system={system}&amp;surface=home&amp;lang=fr"' in html, system
    assert f'href="{TYPE}?system=a&amp;surface=dashboard&amp;lang=fr"' in html
    for code in ("V4", "TYPE A", "A-bis", "A+", "TYPE B", "TYPE C", "TYPE D"):
        assert f'<span class="dp-surface__code">{code}</span>' in html, code
    # Wave 2: what is in the package is linked, with the query string that replays the bench.
    for href, label in (
        (PROOF + "research/21st-group2/code-field/index.html", "fr"),
        (PROOF + "research/21st-group4/proto/overlays.html", "fr"),
        (PROOF + "research/21st-group4/proto/overlays-ar.html", "ar"),
        (PROOF + "research/motion/bench/index.html", "fr"),
        (PROOF + "research/motion/bench/index.html?rm=1", "fr · movimento ridotto · ?rm=1"),
        (PROOF + "research/motion/bench/index.html?slow=5", "fr · al rallentatore · ?slow=5"),
        (PROOF + "research/uiux-platform/proto/shell-fr.html", "fr"),
        (PROOF + "research/uiux-platform/proto/shell-ar.html", "ar"),
    ):
        assert re.search(
            rf'<a class="dp-link dp-link--proof" href="{re.escape(href)}"[^>]*>{re.escape(label)}</a>', html
        ), href
    for name in (
        "Il codice di verifica — un campo, sei caselle",
        "Il suggerimento e la definizione",
        "La scelta guida l’immagine",
        "Il banco",
        "Pubblico — la home",
        "Pubblico — il menu aperto",
        "Pubblico — l’accesso",
        "Piattaforma — il guscio e il cruscotto",
        "Piattaforma — «Mes pièces»",
    ):
        assert f'<h3 class="dp-surface__title">{name}</h3>' in html, name
    # Both pickers' keys are written on the hub; the three concepts of H-E have none.
    assert "<kbd>d</kbd> <kbd>e</kbd> la variante, da H-0 a H-E (i concetti E1–E3 non hanno tasto)" in html
    assert (
        "<kbd>v</kbd> <kbd>a</kbd> <kbd>s</kbd> <kbd>p</kbd> <kbd>b</kbd> <kbd>c</kbd> <kbd>d</kbd> il sistema" in html
    )


def _hub_links(html: str) -> tuple[list[str], list[str], list[str]]:
    """The hub's links by kind — proof files (without query), hero picker entries, type picker entries."""
    hrefs = [value.replace("&amp;", "&") for value in re.findall(r'<a class="dp-link[^"]*" href="([^"]+)"', html)]
    proof = [href[len(PROOF) :].split("?")[0] for href in hrefs if href.startswith(PROOF)]
    hero = [href for href in hrefs if href.startswith(PICKER)]
    type_ = [href for href in hrefs if href.startswith(TYPE)]
    return proof, hero, type_


@pytest.mark.django_db
def test_the_hub_never_links_what_is_not_on_disk(client, preview):
    """
    The catalogue stays honest: a file, a prototype state or a picker entry whose file is not in the
    proof directory is printed as «manca» — a word, not a link that would answer 404 or an empty frame.
    """
    from designpreview import services

    html = client.get(HUB).content.decode()
    proof, hero, type_ = _hub_links(html)
    assert proof and hero and type_
    for relative in proof:
        assert relative in FAKE_PACKAGE, f"{relative} is linked and is not in the package"
    for href in hero:
        query = dict(pair.split("=") for pair in href.split("?")[1].split("&"))
        file = services.HERO_VARIANTS[query["variant"]].files[(query["lang"], query["phase"])]
        assert file in FAKE_PACKAGE, href
    for href in type_:
        query = dict(pair.split("=") for pair in href.split("?")[1].split("&"))
        assert services.type_file(query["system"], query["surface"], query["lang"]) in FAKE_PACKAGE, href
    # What is missing is said, by name, where it would have been.
    for label in (
        "ar · fase 3 · manca",  # H-D has no Arabic page in this package
        "esplorazione · La loggia · manca",
        "ar · ?drawer=1 · manca",
        "selettore · cruscotto · 390 · manca",  # A+ on the dashboard, at phone width
        "selettore · home · manca",  # TYPE C, TYPE D, A-bis
        "movimento ridotto · ?rm=1 · manca",  # «Lume», «Passo»
        "H-B · ar · manca",  # the public audit's pages
        "fr · errore · manca",
        "campione · manca",  # H-E's own folder, absent from this package: the CTA specimen …
        "selettore · concetto 2 · manca",  # … a concept frame …
        "selettore · fr · fase 3 · manca",  # … and the page itself
        "candidati · manca",  # the icon candidates (wave 3)
        "stati · ar · manca",  # the Arabic twins of H-E's CTA rig
        "palco · ar · CTA-A · ?cta=a · manca",  # … once per primary of its stand-in first screen
        "confronto · ar · manca",  # the compare view: one of its two Arabic pages is absent
    ):
        assert f">{label}</span>" in html, label
    assert PROOF + "research/hero/hd/ar.html" not in html
    assert "system=ap" not in html and "system=c&amp;" not in html
    # An entry of the compare view is a link only when both of its pages are on disk.
    compared = [
        value.replace("&amp;", "&") for value in re.findall(r'<a class="dp-link dp-link--compare" href="([^"]+)"', html)
    ]
    assert compared == [f"{COMPARE}?pair=mes-pieces&lang=fr"]
    for href in compared:
        query = dict(pair.split("=") for pair in href.split("?")[1].split("&"))
        for file in services.compare_files(query["pair"], query["lang"]):
            assert file in FAKE_PACKAGE, (href, file)
    # Every link of the catalogue is either drawn as a link or as «manca»: none is dropped.
    drawn = len(re.findall(r'<a class="dp-link', html)) + len(
        re.findall(r'<span class="dp-link dp-link--missing"', html)
    )
    assert drawn == sum(len(surface.links) for group in services.GROUPS for surface in group.surfaces)


@pytest.mark.django_db
def test_the_hub_of_an_empty_proof_directory_links_nothing(client, preview, tmp_path):
    """No package at all: the archive still answers, says the directory is not there, and links no file."""
    empty = tmp_path / "nowhere"
    with override_settings(ILE_DESIGN_PREVIEW_PROOF_DIR=empty):
        response = client.get(HUB)
    assert response.status_code == 200
    html = response.content.decode()
    assert "La cartella delle prove non è raggiungibile" in html
    proof, hero, type_ = _hub_links(html)
    assert proof == [] and hero == [] and type_ == []
    assert COMPARE not in html, "a comparison with no page on disk is not linked"
    assert "dp-link--live" not in html


# --------------------------------------------------------------------------- H-E, from «manca» to a link


def _own_missing(drawn: str) -> list[str]:
    """The «manca» of H-E's own entries — those that stand on a file of research/hero/he/ — in the order of the page."""
    return [
        label
        for title, label in re.findall(r'<span class="dp-link dp-link--missing" title="([^"]+)">([^<]+)</span>', drawn)
        if title.startswith("research/hero/he/")
    ]


@pytest.mark.django_db
def test_what_is_not_on_disk_says_manca_and_is_linked_by_itself_when_its_file_arrives(client, preview):
    """
    H-E was authorised on 2 October 2026 and built while the owner looked at the hub: its group was
    on the page from the first day, every entry of its own folder saying «manca» — a word, never a
    dead link — and on 4 October its files reached the disk and its entries became links, with no
    restart and no commit between the builder and the owner. The fake package carries nothing of
    H-E's own folder, so this replays those two days: what is not there says «manca»; the day a
    file is written into the proof directory its entry is a link at the next request; a file that
    goes away is «manca» again. Nothing about the disk is remembered from one request to the next.
    (H-E's measurement pages, in other folders, are the next test's.)
    """
    from designpreview import services

    he_folder = preview / "research" / "hero" / "he"
    assert not he_folder.exists(), "the fake package carries nothing of H-E's own folder"

    def group() -> str:
        return _group_of(client.get(HUB).content.decode(), "he")

    drawn = group()
    head = drawn[: drawn.index('<ul class="dp-surfaces"')]
    assert "H-E — nuova direzione</h2>" in head
    assert f'<p class="dp-tag">{NOT_APPROVED}</p>' in head
    for code, title in (("H-E", "La pagina costruita"), ("E1–E3", "I tre concetti")):
        assert f'<span class="dp-surface__code">{code}</span> {title}</h3>' in drawn, code
    assert '<h3 class="dp-surface__title">CTA-A / CTA-B</h3>' in drawn
    labels = [
        "fr · fase 3",
        "ar · fase 3",
        "selettore · fr · fase 3",
        "selettore · concetto 1",
        "selettore · concetto 2",
        "selettore · concetto 3",
        "campione",
    ]
    assert _own_missing(drawn) == [f"{label} · manca" for label in labels]
    assert f'href="{PROOF}research/hero/he/' not in drawn, "nothing of H-E's own folder is linked before it exists"
    assert not re.search(r'href="[^"]*variant=(?:he|e[123])&', drawn)
    # The picker knows the four choices and says what is missing, in the bar and on the stage.
    html = client.get(PICKER + "?variant=he").content.decode()
    assert "<iframe" not in html
    assert '<span class="dp-bar__code">H-E</span> Nuova direzione</span>' in html
    assert f'<span class="dp-bar__status">{NOT_APPROVED}</span>' in html
    assert "H-E · fr · fase 3: il file manca nella cartella delle prove." in html
    assert "research/hero/he/index.html" in html and "non è nella cartella delle prove" in html
    html = client.get(PICKER + "?variant=e2&lang=ar").content.decode()
    assert "<iframe" not in html
    assert "E2 è un prototipo di ricerca, costruito soltanto in fr · fase 3." in html
    assert "E2 · ar · fase 3: questa combinazione non esiste." in html

    # The files arrive — one by one, as a build writes them. No reload, no restart.
    arrivals = {
        "index.html": b"<!doctype html><html lang='fr'><body>H-E</body></html>",
        "ar.html": b"<!doctype html><html lang='ar' dir='rtl'><body>H-E ar</body></html>",
        "concepts/e2/index.html": b"<!doctype html><body>concept 2</body>",
        "cta/index.html": b"<!doctype html><body>CTA-A / CTA-B</body>",
    }
    (he_folder / "concepts" / "e2").mkdir(parents=True)  # a folder alone is not a file: still «manca»
    assert "selettore · concetto 2 · manca" in _own_missing(group())
    for relative, content in arrivals.items():
        target = he_folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    drawn = group()
    for link in (
        f'<a class="dp-link dp-link--proof" href="{PROOF}research/hero/he/index.html" hreflang="fr">fr · fase 3</a>',
        f'<span class="dp-link-pair"><a class="dp-link dp-link--proof" href="{PROOF}research/hero/he/ar.html" '
        'hreflang="ar">ar · fase 3</a><span class="dp-link__note">da non firmare come /ar/</span></span>',
        f'<a class="dp-link dp-link--picker" href="{PICKER}?variant=he&amp;lang=fr&amp;phase=3" hreflang="fr">'
        "selettore · fr · fase 3</a>",
        f'<a class="dp-link dp-link--picker" href="{PICKER}?variant=e2&amp;lang=fr&amp;phase=3" hreflang="fr">'
        "selettore · concetto 2</a>",
        f'<a class="dp-link dp-link--proof" href="{PROOF}research/hero/he/cta/index.html" hreflang="fr">campione</a>',
    ):
        assert link in drawn, link
    assert _own_missing(drawn) == ["selettore · concetto 1 · manca", "selettore · concetto 3 · manca"]
    for relative, content in arrivals.items():
        response = client.get(f"{PROOF}research/hero/he/{relative}")
        assert response.status_code == 200 and b"".join(response.streaming_content) == content, relative
    # The picker frames them, H-E with its key and the concept without one, and says what they are.
    response = client.get(PICKER + "?variant=he")
    html = response.content.decode()
    assert f'<iframe class="dp-stage__frame" src="{PROOF}research/hero/he/index.html"' in html
    assert 'data-dp-key="e" aria-current="true" title="Nuova direzione — tasto e">H-E</a>' in html
    assert f'title="H-E — Français, fase 3 — {NOT_APPROVED}"></iframe>' in html
    assert "frame-src 'self'" in _csp(response)
    html = client.get(PICKER + "?variant=he&lang=ar").content.decode()
    assert f'src="{PROOF}research/hero/he/ar.html"' in html
    assert '<strong class="dp-bar__flag-warning">da non firmare come /ar/</strong>' in html
    html = client.get(PICKER + "?variant=e2").content.decode()
    assert f'<iframe class="dp-stage__frame" src="{PROOF}research/hero/he/concepts/e2/index.html"' in html
    assert '<span class="dp-bar__code">E2</span> Concetto H-E 2</span>' in html
    assert (
        f'href="{PICKER}?variant=e2&amp;lang=fr&amp;phase=3" aria-current="true" title="Concetto H-E 2">E2</a>' in html
    )
    assert _keys(html) == ["0", "a", "b", "c", "d", "e", "f", "r", "3", "i"], "the concepts take no key"

    # And a file that goes is «manca» again, at the next request.
    (he_folder / "index.html").unlink()
    assert {"fr · fase 3 · manca", "selettore · fr · fase 3 · manca"} <= set(_own_missing(group()))
    assert "<iframe" not in client.get(PICKER + "?variant=he").content.decode()
    assert services.proof_exists(preview, "research/hero/he/ar.html")


# --------------------------------------------------------------------------- the hero council's record


@pytest.mark.django_db
def test_the_hub_names_the_council_record_as_text_and_serves_none_of_it(client, preview, monkeypatch, tmp_path):
    """
    The council's minutes and its two sheets live in another stream's folders. The hub says what
    the council found, in one sentence and as the council's, and prints where the record is: a
    path to select and copy, not a link — this server does not serve those folders, and nothing is
    copied into the proof directory to make it. Whether a file is there is looked up when the hub
    is drawn, like everything else on the page.
    """
    from designpreview import services

    html = client.get(HUB).content.decode()
    council = _group_of(html, "council")
    assert (
        "Cinque seggi su cinque: nessuno tra H-0, H-A, H-B, H-C e H-D raggiunge, così com’è costruito, il livello "
        "richiesto. Il consiglio non approva nulla e non impone un vincitore: decide il proprietario (O67). "
        "L’ordine di preferenza dei seggi sta nel verbale, con le sue riserve, e non in questa pagina."
    ) in council
    references = (
        ("verbale", "C:/tmp/ile_wt/qa-v5/docs/design-v5/QA/HERO_COUNCIL_REVIEW.md"),
        ("1440 × 900", "C:/tmp/ile_v5_council/.work/hero-council/design/BEFORE_AFTER_1440x900.png"),
        ("390 × 844", "C:/tmp/ile_v5_council/.work/hero-council/design/BEFORE_AFTER_390x844.png"),
    )
    for label, location in references:
        line = (
            f'<p class="dp-ref"><span class="dp-ref__label">{label}</span> <code class="dp-ref__path">{location}</code>'
        )
        assert line in council, label
    assert council.count('<p class="dp-ref">') == 3
    # Text, never a link — nowhere on the page.
    assert "<a " not in council
    hrefs = " ".join(re.findall(r'href="([^"]*)"', html))
    assert "HERO_COUNCIL_REVIEW" not in hrefs and "BEFORE_AFTER" not in hrefs and "hero-council" not in hrefs
    # … and not served: the proof view answers for the proof directory alone.
    for attempt in (
        "C:/tmp/ile_wt/qa-v5/docs/design-v5/QA/HERO_COUNCIL_REVIEW.md",
        "../.work/hero-council/design/BEFORE_AFTER_1440x900.png",
        ".work/hero-council/design/BEFORE_AFTER_390x844.png",
    ):
        assert client.get(PROOF + attempt).status_code == 404, attempt
    assert [p for p in services.catalogued_proof_paths() if "council" in p.lower() or "BEFORE_AFTER" in p] == []
    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    assert "overflow-wrap: anywhere" in _declarations(css, ".dp-ref__path"), "a path has no spaces to break at"

    # On disk, or «manca» — looked up when the hub is drawn, and found at the next request.
    here, gone = tmp_path / "minutes.md", tmp_path / "sheet.png"
    here.write_bytes(b"# minutes\n")
    record = services.Surface(
        "Il verbale",
        "Una nota.",
        references=(services.Reference("verbale", here.as_posix()), services.Reference("tavola", gone.as_posix())),
    )
    monkeypatch.setattr(services, "GROUPS", (services.Group("council", "Consiglio sull’hero", "Un esito.", (record,)),))
    html = client.get(HUB).content.decode()
    assert f'<code class="dp-ref__path">{here.as_posix()}</code></p>' in html
    assert f'<code class="dp-ref__path">{gone.as_posix()}</code> <span class="dp-ref__missing">manca</span></p>' in html
    gone.write_bytes(b"png")
    assert "dp-ref__missing" not in client.get(HUB).content.decode()


# --------------------------------------------------------------------------- step 0: the hub catches up


def _link_to(path: str, label: str, kind: str = "proof", query: str = "") -> str:
    """The pattern of the hub's link to the proof file ``path`` — in one of its states with ``query`` — and its label."""
    href = PROOF + path + (f"?{query}" if query else "")
    return rf'<a class="dp-link dp-link--{kind}" href="{re.escape(href)}"[^>]*>{re.escape(label)}</a>'


@pytest.mark.django_db
def test_the_hub_shows_the_third_wave_each_group_tagged_and_every_link_on_a_file(client, preview):
    """
    Step 0 of the research consolidation (RESEARCH_SYNTHESIS_V52.md §6, X-1). The prototypes of
    wave 3 were on disk and not on the hub; they are now, after wave 2 and before the control, a
    group per lane as for the waves before them, each under «prototipo di ricerca — non approvato»
    and each saying who has looked at it: «Mes pièces» V5.2, «La soglia» V5.2, the colour specimen,
    the icon sheets, the door rows. What the fake package carries is linked; what it lacks says
    «manca». The door rows say, in one plain line, what their photographs are — stock, provisional
    until the owner answers O54 and O55 and rules O81, one of the alternates held for O55 — and that
    the page is local only (review HC-4). The words are Italian ones, not calques (review HC-3), and
    the comparison's row says its widths as they are at every window width (review HC-2).
    """
    html = client.get(HUB).content.decode()
    tag = f'<p class="dp-tag">{NOT_APPROVED}</p>'
    expected = {
        "research-documents": (
            "Ricerca, terza ondata — «Mes pièces» V5.2",
            [
                ("fr", "research/documents/index.html"),
                ("ar", "research/documents/ar.html"),
                ("tavola", "research/documents/anatomy.html"),
            ],
        ),
        "research-journey": ("Ricerca, terza ondata — «La soglia» V5.2", [("fr", "research/journey/index.html")]),
        "research-colour": (
            "Ricerca, terza ondata — i colori della piattaforma",
            [("campione", "research/colour/specimen.html")],
        ),
        "research-icons": (
            "Ricerca, terza ondata — le icone",
            [
                ("fr", "research/icons/sheet.html"),
                ("ar", "research/icons/sheet-ar.html"),
                ("famiglie", "research/icons/families.html"),
            ],
        ),
        "research-images": (
            "Ricerca, terza ondata — la fila delle porte",
            [("fr", "research/images/proto/doors.html")],
        ),
    }
    for key, (title, links) in expected.items():
        group = _group_of(html, key)
        head = group[: group.index('<ul class="dp-surfaces"')]
        assert f"</span>{title}</h2>" in head, key
        assert tag in head, key
        assert "la revisione indipendente è in attesa." in head, key
        for label, path in links:
            assert path in FAKE_PACKAGE, path
            assert re.search(_link_to(path, label), group), (key, path)
    # What this package lacks is said where it would have been.
    assert ">ar · manca</span>" in _group_of(html, "research-journey")
    assert ">candidati · manca</span>" in _group_of(html, "research-icons")
    assert ">ar · manca</span>" in _group_of(html, "research-images")
    # The door rows: stock photographs, provisional until the owner's rulings, one of them held; a
    # page that stays local.
    assert (
        "Mostra fotografie stock (Pexels), provvisorie finché il proprietario non risponde a O54 e O55 e non "
        "decide O81; fra le alternative, una è trattenuta per O55. È una pagina soltanto locale, da non pubblicare."
    ) in _group_of(html, "research-images")
    # «Audiences» are «pubblici»: an «udienza» is a court's hearing, the wrong word on a legal platform.
    icons = _group_of(html, "research-icons")
    assert "i quattro pubblici" in icons and "I quattro pubblici" in icons and "i momenti su misura" in icons
    assert "udienz" not in html.lower()
    assert "una linea in piano" in _group_of(html, "research-journey") and "linea di livello" not in html
    # The second phone version of «Mes pièces» stands beside the first through the compare view.
    documents = _group_of(html, "research-documents")
    assert '<span class="dp-surface__code">K5</span> Due telefoni a confronto</h3>' in documents
    assert (
        "Alla stessa larghezza: 390 px, affiancate, da 864 px di finestra; sotto, una sotto l’altra, larghe quanto "
        "la finestra permette, fino a 390 px."
    ) in documents
    assert (
        f'<a class="dp-link dp-link--compare" href="{COMPARE}?pair=mes-pieces&amp;lang=fr" hreflang="fr">'
        "confronto · fr</a>"
    ) in documents
    assert "Il confronto non ne indica una: decide il proprietario." in documents
    # The wave-3 groups come after wave 2 and before what is to come, in the order of step 0.
    keys = re.findall(r'<li class="dp-group" id="g-([^"]+)">', html)
    wave_3 = ["research-documents", "research-journey", "research-colour", "research-icons", "research-images"]
    assert keys[keys.index("research-uiux") + 1 : keys.index("upcoming")] == wave_3


@pytest.mark.django_db
def test_h_e_says_where_it_stands_and_each_measurement_page_what_it_is_not(client, preview):
    """
    X-2. H-E's build reached the disk on 4 October: its group no longer says «in costruzione» — it
    says, with the date, that the page is built as a provisional proof and that its independent
    review is not concluded — and its page is «La pagina costruita», not a «finale» that it is not.
    Beside H-E's own entries stand three measurement pages, each with the one line that says what
    it is and what it is not: the motion bench (a diagram of timing, not a drawing to judge), the
    two CTA recipes on their rig (not a hero, not a proposal; its numbers are to be taken again
    on H-E), the door from its master (a fragment, not a page). The rig's stand-in first screen draws
    one primary, the one ``?cta=`` names, and T0 without it: the hub links it once per primary and
    says so, never bare (review HC-1); the door master's row links the lane's check page too, where
    today's door stands beside the snippet's (review HC-7).
    """
    html = client.get(HUB).content.decode()
    group = _group_of(html, "he")
    head = group[: group.index('<ul class="dp-surfaces"')]
    assert (
        "Direzione nuova autorizzata dal proprietario il 2 ottobre. Al 4 ottobre la pagina è costruita, come prova "
        "provvisoria, e la sua revisione indipendente non è conclusa; decide il proprietario — O67."
    ) in head
    for stale in ("in costruzione", "a seguire", "La pagina finale", "Finché un file"):
        assert stale not in group, stale
    stage = "research/hero/he-21st/stage.html"
    rows = {
        "Il banco del primo movimento": (
            "Il primo movimento di H-E misurato su una geometria di sostituzione: un diagramma dei tempi — si "
            "giudicano i tempi, non il disegno.",
            [("banco", "research/hero/he-motion/index.html", "")],
        ),
        "Le due CTA sul loro banco": (
            "il palco. Sul palco una CTA alla volta: il parametro cta sceglie T0, CTA-A o CTA-B. È un banco di prova, "
            "non un eroe e non una proposta: i suoi numeri vanno ripresi su H-E.",
            [
                ("stati · fr", "research/hero/he-21st/states.html", ""),
                ("palco · fr · T0 · ?cta=t0", stage, "cta=t0"),
                ("palco · fr · CTA-A · ?cta=a", stage, "cta=a"),
                ("palco · fr · CTA-B · ?cta=b", stage, "cta=b"),
            ],
        ),
        "La porta dal suo master": (
            "un frammento da copiare in una pagina, non una pagina — aperto da solo mostra la fotografia, senza la "
            "porta disegnata. La pagina di verifica mette la porta di oggi accanto a quella del frammento, così com’è "
            "scritto: una verifica, non una maquette.",
            [
                ("frammento", "research/hero/door-master/snippet.html", ""),
                ("verifica · oggi e il frammento", "research/hero/door-master/check/door-snippet.html", ""),
            ],
        ),
    }
    for title, (line, links) in rows.items():
        row = group[group.index(f'<h3 class="dp-surface__title">{title}</h3>') :]
        row = row[: row.index("</li>")]
        assert line in row, title
        for label, path, query in links:
            assert path in FAKE_PACKAGE, path
            assert re.search(_link_to(path, label, query=query), row), (path, query)
    # Every link to the stand-in first screen names its primary: T0, CTA-A, CTA-B, once each, none bare.
    hrefs = [href for href in re.findall(r'href="([^"]+)"', group) if "/he-21st/stage" in href]
    assert hrefs == [f"{PROOF}{stage}?cta={value}" for value in ("t0", "a", "b")], hrefs
    # The rig's Arabic twins are not in this package: «manca», never a dead link — once per primary.
    for label in (
        "stati · ar · manca",
        "palco · ar · T0 · ?cta=t0 · manca",
        "palco · ar · CTA-A · ?cta=a · manca",
        "palco · ar · CTA-B · ?cta=b · manca",
    ):
        assert f">{label}</span>" in group, label
    # The measurement pages come after H-E's own entries, under the same tag.
    titles = re.findall(
        r'<h3 class="dp-surface__title">(?:<span class="dp-surface__code">[^<]+</span> )?([^<]+)</h3>', group
    )
    assert titles == [
        "La pagina costruita",
        "I tre concetti",
        "CTA-A / CTA-B",
        "Il banco del primo movimento",
        "Le due CTA sul loro banco",
        "La porta dal suo master",
    ]


@pytest.mark.django_db
def test_where_the_hub_offers_rm_1_it_says_the_flag_is_not_yet_the_reduced_motion_state(client, preview):
    """
    X-4 (MOTION_SYSTEM.md MS7). Gate 0's ``?rm=1`` sets ``html.rm``, which stops what each sheet
    stops — a loader's key, the drawer — and leaves the duration tokens of the token sheet as they
    are: a review of the motion made with the flag still sees motion. Making the flag the state is
    the foundation's to do. Until then the hub says so wherever it offers the flag on a prototype
    that leaves those tokens alone — the three loaders, the drawer — and once in its keys, with
    the one offer that is the state: the motion bench zeroes the tokens itself under the flag
    (research/motion/bench/bench.css). The pickers and the compare view offer no such flag.
    """
    html = client.get(HUB).content.decode()
    start = html.index('<dl class="dp-keys">')
    keys = html[start : html.index("</dl>", start)]
    assert "<dt>Movimento ridotto</dt>" in keys
    for words in (
        "Il parametro <code>?rm=1</code> che l’hub offre per i tre caricatori e per il cassetto non è ancora lo "
        "stato di movimento ridotto",
        "il foglio dei token del gate 0 non azzera le durate sotto il parametro (MS7, aperto nella fondazione del "
        "gate 0), e una revisione del movimento fatta così vede ancora movimento.",
        "Lo stato vero è l’impostazione «riduci movimento» del sistema",
        "Il banco del movimento azzera da sé le durate sotto lo stesso parametro.",
    ):
        assert words in keys, words
    loader = _group_of(html, "research-loader")
    assert (
        "Il link «movimento ridotto · ?rm=1» non è ancora lo stato di movimento ridotto: ferma il caricatore, ma i "
        "token di durata del gate 0 restano (MS7)."
    ) in loader[: loader.index('<ul class="dp-surfaces"')]
    drawer = _group_of(html, "research-drawer")
    assert (
        "Il parametro rm=1 non è ancora lo stato di movimento ridotto: cambia il cassetto, ma i token di durata del "
        "gate 0 restano (MS7)."
    ) in drawer
    # Every offer of the flag stands in one of those groups, or on the bench.
    offers = re.findall(r'href="([^"]*rm=1[^"]*)"', html)
    assert offers, "the fake package carries a loader, the drawer and the bench"
    said = tuple(PROOF + folder for folder in ("research/loader/", "research/emil/prototype/drawer/"))
    for href in offers:
        assert href.startswith(said) or href.startswith(PROOF + "research/motion/bench/"), href
    assert any(href.startswith(said) for href in offers) and any("motion/bench" in href for href in offers)
    for url in (PICKER + "?variant=hb", TYPE + "?system=a", COMPARE + "?pair=mes-pieces&lang=fr"):
        assert "rm=" not in client.get(url).content.decode(), url


@pytest.mark.django_db
def test_no_research_group_carries_a_recommendation_or_an_adjective_of_merit(client, preview):
    """
    The hub describes a prototype — what it is, what it asks of the rules, who has looked at it,
    who decides — and never says which one is better: not in its own voice, not in the council's
    (review W2-2), and not in a builder's either. The type research's and the loader's
    recommendations and one loader's «strongest image» were their builders' words on the page the
    owner chooses on; they are gone, and none of their kind stands in the new groups.
    """
    html = client.get(HUB).content.decode()
    keys = re.findall(r'<li class="dp-group" id="g-([^"]+)">', html)
    research = [key for key in keys if key in {"he", "type"} or key.startswith("research-")]
    assert len(research) == 14
    for key in research:
        text = re.sub(r"<[^>]+>", " ", _group_of(html, key)).lower()
        # «superiore» alone is the console's «barra superiore»: the top bar, not a verdict.
        for words in ("raccomand", "più forte", "superiore a", "migliore", "preferit", "il più ", "il meno ", "vincit"):
            assert words not in text, (key, words)


# --------------------------------------------------------------------------- proof files


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("relative", "content_type"),
    [
        ("home/phase3.html", "text/html; charset=utf-8"),
        ("assets/css/tokens.css", "text/css; charset=utf-8"),
        ("home/home.js", "text/javascript; charset=utf-8"),
        ("assets/img/mark.svg", "image/svg+xml"),
        ("assets/fonts/v5.woff2", "font/woff2"),
        ("assets/img/door.webp", "image/webp"),
        ("assets/img/shot.png", "image/png"),
        ("home/measure.json", "application/json; charset=utf-8"),
        ("SIGNING_SHEET.md", "text/plain; charset=utf-8"),
        ("research/hero/hc/index.html", "text/html; charset=utf-8"),
        ("research/type/A/type.css", "text/css; charset=utf-8"),
        ("research/emil/prototype/drawer/index.html", "text/html; charset=utf-8"),
    ],
)
def test_proof_files_are_served_with_their_content_type(client, preview, relative, content_type):
    response = client.get(PROOF + relative)
    assert response.status_code == 200
    assert response["Content-Type"] == content_type
    assert b"".join(response.streaming_content) == FAKE_PACKAGE[relative]
    _assert_sealed(response)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("relative", "query"),
    [
        ("research/navigation/public-fr-sheet.html", "drawer=1"),
        ("research/navigation/app-fr.html", "drawer=1"),
        ("research/loader/mandata/index.html", "rm=1"),
        ("research/emil/prototype/drawer/index.html", "exit=out"),
    ],
)
def test_a_prototype_state_is_the_same_file_with_a_query_string(client, preview, relative, query):
    """The hub links a prototype's states by query string; the file is read by its path alone."""
    response = client.get(f"{PROOF}{relative}?{query}")
    assert response.status_code == 200
    assert response["Content-Type"] == "text/html; charset=utf-8"
    assert b"".join(response.streaming_content) == FAKE_PACKAGE[relative]
    _assert_sealed(response)
    assert "frame-ancestors 'self'" in _csp(response)


@pytest.mark.django_db
def test_proof_html_may_be_framed_by_this_origin_only(client, preview):
    response = client.get(PROOF + "home/phase3.html")
    csp = _csp(response)
    assert "frame-ancestors 'self'" in csp
    assert "frame-ancestors 'none'" not in csp
    assert "script-src 'self'" in csp and "style-src 'self'" in csp, "the strict part of the policy must hold"
    assert "unsafe" not in csp
    assert response["X-Frame-Options"] == "SAMEORIGIN"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "relative",
    [
        ".work/notes.txt",  # a dotted working folder
        ".profiles/stream/Default/Cookies",  # a browser profile
        "home/options/.git-status-after.txt",  # a dotted file inside a served folder
        "WORK~1/notes.txt",  # the shape of an 8.3 alias of a dotted folder (review F1)
        "home/options/GIT-ST~1.TXT",  # the shape of an 8.3 alias of a dotted file
        "home/build.py",  # a generator
        "tools/run.ps1",  # a script
        "home/perf_run.log",  # a log
        "research/hero/hc/.work/live-8771-fr.html",  # a research lane's working folder
        "research/navigation/.evidence/raw.json",  # and its evidence folder
        "research/hero/hd/build_hd.py",  # a research generator
        "research/hero/hd/",  # a research folder is not listed either
        "research/hero/hc/../../../../outside.html",  # traversal from inside the research tree
        "research/type/A/TYPE~1.CSS",  # the shape of an 8.3 alias, in the research tree
        "home/",  # a directory is never listed
        "home",  # nor a bare one
        "missing/nothing.html",  # absent
        "home/../../outside.html",  # traversal, plain
        "home/%2e%2e/%2e%2e/outside.html",  # traversal, percent-encoded
        "home//phase3.html",  # an empty segment
        "C:/Windows/win.ini",  # a drive letter
        "home/phase3.html/",  # a trailing slash on a file
        "research/hero/he-motion/.work/frames.html",  # wave 3 and H-E's measurement pages: a working folder
        "research/hero/door-master/.work/notes.html",
        "research/hero/he-motion/WORK~1/frames.html",  # … and the shape of its 8.3 alias
        "research/hero/he-motion/probe_he_motion.py",  # their scripts
        "research/hero/he-21st/measure.py",
        "research/colour/build_specimen.py",
        "research/documents/_tools/build.py",
        "research/documents/",  # a new folder is not listed either
    ],
)
def test_proof_refuses_what_it_must_with_a_404(client, preview, relative):
    response = client.get(PROOF + relative)
    assert response.status_code == 404, relative
    assert b"outside the root" not in response.content
    assert b"never served" not in response.content


def test_resolution_never_leaves_the_root(proof_root):
    """The resolver itself, below the URLconf: a backslash, a NUL, a drive letter, a dotted segment, a tilde."""
    from designpreview.services import resolve_proof_file

    for raw in (
        "..\\outside.html",
        "home\\phase3.html",
        "home/phase3.html\x00",
        "home/../outside.html",
        "",
        "C:/x.html",
        "HOME~1/phase3.html",
    ):
        with pytest.raises(Http404):
            resolve_proof_file(proof_root, raw)
    full, content_type = resolve_proof_file(proof_root, "home/phase3.html")
    assert full == (proof_root / "home" / "phase3.html").resolve(), "the real path is what gets opened"
    assert content_type.startswith("text/html")


def _short_name(path: Path) -> str:
    """The last component of ``path`` as its 8.3 alias — or its long name, where the volume has none."""
    if sys.platform != "win32":
        pytest.skip("8.3 aliases are a Windows file-system feature")
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    if not ctypes.windll.kernel32.GetShortPathNameW(str(path), buffer, 1024):
        pytest.skip("GetShortPathNameW gave no answer for the temporary directory")
    return Path(buffer.value).name


@pytest.mark.django_db
def test_proof_refuses_a_dotted_folder_through_its_short_name_alias(client, preview):
    """
    Regression (review F1). On NTFS every long name also answers to an 8.3 alias: ``WORK~1/x.json``
    opens ``.work/x.json`` although no segment of the request starts with a dot, and
    ``GIT-ST~1.TXT`` opens ``.git-status-after.txt``. Both layers of the resolver must refuse the
    alias: the shape check on the string, and — should that one ever be relaxed — the check on the
    real path the file system reports.
    """
    from designpreview.services import real_proof_path

    root = preview
    (root / ".work" / "x.json").write_bytes(b"never served\n")
    folder_alias = _short_name(root / ".work")
    if folder_alias.lower() == ".work":
        pytest.skip("this volume does not generate 8.3 names")
    file_alias = _short_name(root / "home" / "options" / ".git-status-after.txt")
    assert "~" in folder_alias and "~" in file_alias
    # The aliases really do open the dotted things on this volume: a 404 below is the resolver's.
    assert (root / folder_alias / "x.json").is_file()
    assert (root / "home" / "options" / file_alias).is_file()

    for relative in (f"{folder_alias}/x.json", f"home/options/{file_alias}"):
        response = client.get(PROOF + relative)
        assert response.status_code == 404, relative
        assert b"never served" not in response.content
    # The second layer alone, given the alias path as safe_join would have accepted it.
    with pytest.raises(Http404):
        real_proof_path(root, root / folder_alias / "x.json", ".json")
    with pytest.raises(Http404):
        real_proof_path(root, root / "home" / "options" / file_alias, ".txt")
    # And it still accepts a real file, by its real name, whatever the case of the request.
    assert real_proof_path(root, root / "home" / "PHASE3.HTML", ".html") == (root / "home" / "phase3.html").resolve()


def _link_directory(target: Path, link: Path) -> None:
    """A symbolic link to a directory — or, on a Windows account without that privilege, a junction."""
    try:
        os.symlink(target, link, target_is_directory=True)
        return
    except (OSError, NotImplementedError):
        pass
    if sys.platform == "win32":
        import _winapi

        try:
            _winapi.CreateJunction(str(target), str(link))
            return
        except OSError:
            pass
    pytest.skip("this account can create neither a symbolic link nor a junction")


@pytest.mark.django_db
def test_proof_refuses_what_a_link_points_at(client, preview, tmp_path):
    """
    A link inside the root is a string safe_join accepts and a file is_file() finds; what it opens
    is its target. Outside the root → 404; inside the root but in a working folder → 404.
    """
    root = preview
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "leak.html").write_bytes(b"outside the root")
    away, work = root / "home" / "away", root / "home" / "work"
    try:
        _link_directory(elsewhere, away)
        _link_directory(root / ".work", work)
        assert (away / "leak.html").is_file() and (work / "notes.txt").is_file(), "the links must open their targets"
        response = client.get(PROOF + "home/away/leak.html")
        assert response.status_code == 404
        assert b"outside the root" not in response.content
        response = client.get(PROOF + "home/work/notes.txt")
        assert response.status_code == 404
        assert b"never served" not in response.content
    finally:
        # Remove the links themselves, never through them: os.unlink removes a directory symlink
        # and a junction on Windows, and a symlink on POSIX, without touching the target.
        for link in (away, work):
            if os.path.lexists(link):
                os.unlink(link)


def _alias(path: Path) -> str:
    """The 8.3 alias of the last component of ``path`` — or "" where the volume gives none."""
    if sys.platform != "win32":
        return ""
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    if not ctypes.windll.kernel32.GetShortPathNameW(str(path), buffer, 1024):
        return ""
    name = Path(buffer.value).name
    return name if name.lower() != path.name.lower() else ""


#: The proof-relative folders step 0 of the research consolidation brought to the hub.
STEP_0_FOLDERS = (
    "research/documents",
    "research/journey",
    "research/colour",
    "research/icons",
    "research/images/proto",
    "research/hero/he",
    "research/hero/he/concepts/e1",
    "research/hero/he/concepts/e2",
    "research/hero/he/concepts/e3",
    "research/hero/he-motion",
    "research/hero/he-21st",
    "research/hero/door-master",
)


#: The working folders of the fake package beside the new entries, with a file inside each.
STEP_0_WORK = (("research/hero/he-motion", "frames.html"), ("research/hero/door-master", "notes.html"))


@pytest.mark.django_db
def test_no_new_entry_reaches_a_dotted_folder(client, preview):
    """
    The folders wave 3 and H-E's measurement pages bring hold their lanes' working folders
    (``.work``) and scripts beside the pages the hub links. None of it is served by its name, nor
    through the compare view, whose pages come from its table and never from the query. And every
    path the new entries name is a plain file under the root, with no dotted or tilde'd component
    in the request or in the real path the file system opens. (By their NTFS 8.3 aliases: the next
    test, which says so when the volume gives none — review HS-1.)
    """
    from designpreview import services

    new = {"research-documents", "research-journey", "research-colour", "research-icons", "research-images"}
    paths = [
        link.path
        for group in services.GROUPS
        if group.key in new or group.key == "he"
        for surface in group.surfaces
        for link in surface.links
        if link.path and any(link.path.startswith(folder + "/") for folder in STEP_0_FOLDERS)
    ]
    paths += [
        file
        for comparison in services.COMPARISONS.values()
        for side in comparison.sides
        for file in side.files.values()
    ]
    assert len(set(paths)) == 24, sorted(set(paths))
    root = preview.resolve()
    for relative in sorted(set(paths)):
        assert not any(part.startswith(".") or "~" in part or part == "" for part in relative.split("/")), relative
        if relative in FAKE_PACKAGE:
            full, _content_type = services.resolve_proof_file(preview, relative)
            assert not any(part.startswith(".") or "~" in part for part in full.relative_to(root).parts), relative
    for folder, name in STEP_0_WORK:
        assert (preview / folder / ".work" / name).is_file(), "the dotted folder is there: a 404 is the resolver's"
        response = client.get(f"{PROOF}{folder}/.work/{name}")
        assert response.status_code == 404 and b"never served" not in response.content, folder
    for query in ("pair=../.work", "pair=research/hero/he-motion/.work/frames.html", "pair=mes-pieces&lang=.work"):
        assert client.get(f"{COMPARE}?{query}").status_code == 400, query


@pytest.mark.django_db
def test_no_new_entry_reaches_a_dotted_folder_through_its_short_name_alias(client, preview):
    """
    Review HS-1. The same working folders through the NTFS 8.3 alias the volume gives each — which
    really opens it — are refused by the proof view, and by the second layer of the resolver on its
    own. Where the volume gives no alias the test says so, with a skip and its reason, instead of
    passing without having looked.
    """
    from designpreview import services

    aliases = {folder: _short_name(preview / folder / ".work") for folder, _name in STEP_0_WORK}
    if any(alias.lower() == ".work" for alias in aliases.values()):
        pytest.skip("this volume does not generate 8.3 names: the alias half was not checked")
    for folder, name in STEP_0_WORK:
        alias = aliases[folder]
        assert "~" in alias, (folder, alias)
        assert (preview / folder / alias / name).is_file(), "the alias really opens the dotted folder"
        response = client.get(f"{PROOF}{folder}/{alias}/{name}")
        assert response.status_code == 404 and b"never served" not in response.content, (folder, alias)
        with pytest.raises(Http404):
            services.real_proof_path(preview, preview / folder / alias / name, ".html")


# --------------------------------------------------------------------------- the picker


@pytest.mark.django_db
def test_the_picker_frames_the_chosen_comp(client, preview):
    response = client.get(PICKER + "?variant=hb")
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert '<html lang="it"' in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
    assert f'<iframe class="dp-stage__frame" src="{PROOF}home/options/hb-phase3.html"' in html
    csp = _csp(response)
    assert "frame-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp, "the picker page itself is not framed by anyone"
    assert "script-src 'self'" in csp and "style-src 'self'" in csp
    # The bar: every variant with its key, both languages, both phases, the widths.
    for variant, key in (("h0", "0"), ("ha", "a"), ("hb", "b"), ("hc", "c"), ("hd", "d"), ("he", "e")):
        link = f'href="{PICKER}?variant={variant}&amp;lang=fr&amp;phase=3" data-dp-key="{key}"'
        assert link in html, variant
    assert _keys(html) == ["0", "a", "b", "c", "d", "e", "f", "r", "3", "i"]
    # The three concept frames of H-E are choices of the same group, after it, and have no key.
    for number in (1, 2, 3):
        link = (
            f'href="{PICKER}?variant=e{number}&amp;lang=fr&amp;phase=3" '
            f'title="Concetto H-E {number} · E{number} · fr · fase 3 non c’è">E{number}</a>'
        )
        assert link in html, number
    assert '<header class="dp-bar dp-bar--long" data-dp-bar>' in html, "nine first screens: the long bar"
    assert f'href="{PICKER}?variant=hb&amp;lang=ar&amp;phase=3"' in html
    assert f'href="{PICKER}?variant=hb&amp;lang=fr&amp;phase=interim"' in html
    assert f'href="{PICKER}?variant=hb&amp;lang=fr&amp;phase=3&amp;w=390"' in html
    assert 'aria-current="true" title="Il pilastro e la soglia — tasto b">H-B</a>' in html
    # What is framed, and that it is not approved, in the bar and on the frame itself.
    assert '<span class="dp-bar__code">H-B</span> Il pilastro e la soglia</span>' in html
    assert '<span class="dp-bar__status">maquette del gate 0 — non approvata</span>' in html
    assert 'title="H-B — Français, fase 3 — maquette del gate 0 — non approvata"></iframe>' in html
    # The flag — the bar's second line in a few words, for a window below 48rem — says the status too.
    assert '<p class="dp-bar__flag"><span class="dp-bar__flag-status">non approvata</span></p>' in html
    assert "dp-bar__warning" not in html and "dp-bar__flag-warning" not in html, "nothing to warn about in French"
    assert f'<a class="dp-bar__open" href="{PROOF}home/options/hb-phase3.html" target="_blank" rel="noopener"' in html
    assert "js/dev/designpreview.js" in html
    assert not re.search(r"<[^>]+\sstyle=", html)
    assert scan(html) == []


def _keys(html: str) -> list[str]:
    """The keyboard shortcuts of a picker's bar, in the order of the bar."""
    return re.findall(r'data-dp-key="([^"]+)"', html)


@pytest.mark.django_db
def test_the_picker_defaults_to_h0_french_phase_3(client, preview):
    html = client.get(PICKER).content.decode()
    assert f'src="{PROOF}home/phase3.html"' in html


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("query", "file", "code", "name"),
    [
        ("variant=hc", "research/hero/hc/index.html", "H-C", "Quattro soglie, una chiave"),
        ("variant=hc&lang=fr&phase=3", "research/hero/hc/index.html", "H-C", "Quattro soglie, una chiave"),
        ("variant=hc&lang=ar&phase=3", "research/hero/hc/ar.html", "H-C", "Quattro soglie, una chiave"),
        ("variant=hd", "research/hero/hd/index.html", "H-D", "La porta, di giorno"),
    ],
)
def test_the_picker_frames_the_two_research_directions(client, preview, query, file, code, name):
    """H-C and H-D are framed like the gate-0 options, and the bar says what they are: research, not approved."""
    response = client.get(PICKER + "?" + query)
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert f'<iframe class="dp-stage__frame" src="{PROOF}{file}"' in html
    assert f'<span class="dp-bar__code">{code}</span> {name}</span>' in html
    assert f'<span class="dp-bar__status">{NOT_APPROVED}</span>' in html
    assert '<span class="dp-bar__flag-status">non approvato</span>' in html
    assert f'— {NOT_APPROVED}"></iframe>' in html
    assert "frame-src 'self'" in _csp(response)
    assert not re.search(r"<[^>]+\sstyle=", html)
    assert scan(html) == []


@pytest.mark.django_db
@pytest.mark.parametrize("variant", ["h0", "hb", "hc"])
def test_the_picker_says_that_the_arabic_of_phase_3_is_not_translated(client, preview, variant):
    """
    Review F4. Every /ar/ page of phase 3 carries the locked copy as 8771 serves it, in French; the
    comp says so at the foot of its document, outside the first screen. The picker says it in its
    bar — the sentence on the second line, the hub's own words kept for the flag of a narrow window,
    after the status.
    """
    html = client.get(f"{PICKER}?variant={variant}&lang=ar&phase=3").content.decode()
    assert "<iframe" in html
    warning = "ar · fase 3: la pagina porta la copia bloccata NON tradotta — da non firmare come /ar/."
    assert f'<strong class="dp-bar__warning">{warning}</strong>' in html
    status = "non approvato" if variant == "hc" else "non approvata"
    assert (
        f'<p class="dp-bar__flag"><span class="dp-bar__flag-status">{status}</span> '
        '<strong class="dp-bar__flag-warning">da non firmare come /ar/</strong></p>'
    ) in html
    # Not in French, where there is nothing to warn about.
    french = client.get(f"{PICKER}?variant={variant}&lang=fr&phase=3").content.decode()
    assert "NON tradotta" not in french and "da non firmare" not in french


@pytest.mark.django_db
def test_the_picker_draws_a_recommended_width_as_a_class(client, preview):
    html = client.get(PICKER + "?variant=hb&w=390").content.decode()
    assert 'class="dp-stage dp-stage--w390"' in html
    html = client.get(PICKER + "?variant=hb&w=999").content.decode()
    assert "dp-stage--w" not in html, "an unlisted width falls back to the full window"


@pytest.mark.django_db
@pytest.mark.parametrize("width", ["²", "٣٩٠", "9" * 5000, "-390", "390px", " 390", "0x186"])
@pytest.mark.parametrize(("picker", "choice"), [(PICKER, {"variant": "hb"}), (TYPE, {"system": "a"})])
def test_a_width_that_is_not_one_of_the_eight_never_raises(client, preview, picker, choice, width):
    """
    Regression. ``str.isdigit()`` is true of «²» and of Arabic-Indic digits, and ``int()`` refuses
    the first and a five-thousand-digit string: the width was once parsed that way, and such a
    query answered 500. A width is now looked up, never converted.
    """
    response = client.get(picker, {**choice, "w": width})
    assert response.status_code == 200
    html = response.content.decode()
    assert "dp-stage--w" not in html
    assert "<iframe" in html


@pytest.mark.django_db
@pytest.mark.parametrize("query", ["variant=hz", "variant=hb&lang=de", "variant=hb&phase=9", "variant=H0", "variant="])
def test_the_picker_answers_400_to_an_unknown_choice(client, preview, query):
    response = client.get(PICKER + "?" + query)
    assert response.status_code == 400
    _assert_sealed(response)
    html = response.content.decode()
    assert "Scelta sconosciuta" in html
    assert "Varianti: h0, ha, hb, hc, hd, he, e1, e2, e3 · lingue: fr, ar · fasi: 3, interim." in html
    assert f'<a href="{PICKER}?variant=h0&amp;lang=fr&amp;phase=3">Torna a H-0</a>' in html
    assert "<iframe" not in html and "dp-bar__group" not in html


@pytest.mark.django_db
def test_the_picker_says_in_the_bar_when_a_combination_does_not_exist(client, preview):
    """
    H-C and H-D were built for phase 3 alone, H-A and H-B have no Arabic intérim. The picker never
    falls back to another comp: the stage says what exists instead of the frame, the bar says in
    plain words that the combination does not, and the choices that lead there are struck through.
    """
    # A research direction has no intérim page.
    response = client.get(PICKER + "?variant=hc&lang=fr&phase=interim")
    assert response.status_code == 200
    html = response.content.decode()
    assert "<iframe" not in html and "dp-bar__open" not in html
    assert '<strong class="dp-bar__warning">H-C · fr · intérim: questa combinazione non esiste.</strong>' in html
    assert '<strong class="dp-bar__flag-warning">combinazione inesistente</strong>' in html
    assert "H-C è un prototipo di ricerca, costruito soltanto in fr · fase 3, ar · fase 3." in html
    assert f'<span class="dp-bar__status">{NOT_APPROVED}</span>' in html
    # From the page that does exist, the way to the one that does not is marked — and still a link.
    html = client.get(PICKER + "?variant=hc&lang=fr&phase=3").content.decode()
    off = f'<a class="dp-bar__link dp-bar__link--off" href="{PICKER}?variant=hc&amp;lang=fr&amp;phase=interim" data-dp-key="i"'
    assert off in html
    assert "intérim — tasto i · H-C · fr · intérim non c’è" in html
    off = re.findall(
        r'class="dp-bar__link dp-bar__link--off" href="[^"]*variant=(\w+)&amp;lang=fr&amp;phase=(\w+)"', html
    )
    assert off == [("he", "3"), ("e1", "3"), ("e2", "3"), ("e3", "3"), ("hc", "interim")], (
        "H-E and its concepts are absent from the fake package; everything else H-C offers in French, phase 3, exists"
    )
    # In the intérim, the two research directions are the ones struck through.
    html = client.get(PICKER + "?variant=h0&lang=fr&phase=interim").content.decode()
    for variant, off in (("h0", False), ("hc", True), ("hd", True)):
        link = f'href="{PICKER}?variant={variant}&amp;lang=fr&amp;phase=interim"'
        assert (f'class="dp-bar__link dp-bar__link--off" {link}' in html) is off, variant
    # A gate-0 option without its Arabic intérim.
    html = client.get(PICKER + "?variant=ha&lang=ar&phase=interim").content.decode()
    assert "<iframe" not in html
    assert "non è nel pacchetto del gate 0: H-A esiste in fr · fase 3, ar · fase 3, fr · intérim." in html
    assert "H-A · ar · intérim: questa combinazione non esiste." in html


@pytest.mark.django_db
def test_the_picker_reports_a_catalogued_file_that_is_not_on_disk(client, preview):
    """In the table, not in the directory: reported by name, never framed — and marked in the bar."""
    html = client.get(PICKER + "?variant=h0&lang=ar&phase=interim").content.decode()
    assert "<iframe" not in html
    assert "home/interim-ar.html" in html and "non è nella cartella delle prove" in html
    assert "H-0 · ar · intérim: il file manca nella cartella delle prove." in html
    assert (
        '<p class="dp-bar__flag"><span class="dp-bar__flag-status">non approvata</span> '
        '<strong class="dp-bar__flag-warning">il file manca</strong></p>'
    ) in html
    # H-D's Arabic page is in the table and not in this package.
    html = client.get(PICKER + "?variant=hd&lang=ar&phase=3").content.decode()
    assert "<iframe" not in html
    assert "research/hero/hd/ar.html" in html and "non è nella cartella delle prove" in html
    assert "NON tradotta" not in html, "nothing is framed, so there is nothing not to sign"
    html = client.get(PICKER + "?variant=hd&lang=fr&phase=3").content.decode()
    off = f'<a class="dp-bar__link dp-bar__link--off" href="{PICKER}?variant=hd&amp;lang=ar&amp;phase=3" hreflang="ar"'
    assert off in html
    # With no package at all, every choice is struck through and nothing is framed.
    with override_settings(ILE_DESIGN_PREVIEW_PROOF_DIR=preview / "nowhere"):
        html = client.get(PICKER + "?variant=hb").content.decode()
    assert "<iframe" not in html
    assert html.count("dp-bar__link--off") == 13, "nine first screens, two languages, two phases"


# --------------------------------------------------------------------------- the type picker


@pytest.mark.django_db
def test_the_type_picker_frames_the_chosen_system_and_surface(client, preview):
    response = client.get(TYPE + "?system=b&surface=case&lang=fr")
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert '<html lang="it"' in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
    assert "<title>TYPE B — fascicolo, Français · Selettore tipografico · Italy Legal Entry™</title>" in html
    assert f'<iframe class="dp-stage__frame" src="{PROOF}research/type/B/case.html"' in html
    csp = _csp(response)
    assert "frame-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp, "the picker page itself is not framed by anyone"
    assert "script-src 'self'" in csp and "style-src 'self'" in csp and "unsafe" not in csp
    # The bar is the hero picker's: the seven sheets, the five surfaces, the two languages, the widths.
    systems = (("v4", "v"), ("a", "a"), ("a2", "s"), ("ap", "p"), ("b", "b"), ("c", "c"), ("d", "d"))
    for system, key in systems:
        assert f'href="{TYPE}?system={system}&amp;surface=case&amp;lang=fr" data-dp-key="{key}"' in html, system
    surfaces = (("home", "1"), ("menu", "2"), ("dashboard", "3"), ("documents", "4"), ("case", "5"))
    for surface, key in surfaces:
        assert f'href="{TYPE}?system=b&amp;surface={surface}&amp;lang=fr" data-dp-key="{key}"' in html, surface
    assert _keys(html) == ["v", "a", "s", "p", "b", "c", "d", "1", "2", "3", "4", "5", "f", "r"]
    for label in (">V4</a>", ">A</a>", ">A-bis</a>", ">A+</a>", ">home</a>", ">cruscotto</a>", ">fascicolo</a>"):
        assert label in html, label
    assert f'href="{TYPE}?system=b&amp;surface=case&amp;lang=fr&amp;w=390"' in html
    assert 'class="dp-bar dp-bar--dense"' in html
    assert 'aria-label="Sistema tipografico"' in html and 'aria-label="Superficie"' in html
    # What is framed, and that it is not approved.
    assert '<span class="dp-bar__code">TYPE B</span> Una voce — solo Host Grotesk</span>' in html
    assert f'<span class="dp-bar__status">{NOT_APPROVED}</span>' in html
    assert '<p class="dp-bar__flag"><span class="dp-bar__flag-status">non approvato</span></p>' in html
    assert f'title="TYPE B — fascicolo, Français — {NOT_APPROVED}"></iframe>' in html
    assert "js/dev/designpreview.js" in html
    assert not re.search(r"<[^>]+\sstyle=", html)
    assert scan(html) == []
    assert "{#" not in html and "{%" not in html


@pytest.mark.django_db
def test_the_type_picker_defaults_to_type_a_on_the_french_home(client, preview):
    html = client.get(TYPE).content.decode()
    assert f'src="{PROOF}research/type/A/home.html"' in html
    assert (
        '<span class="dp-bar__code">TYPE A</span> Fournier e la console — Source Serif 4 + Host Grotesk</span>' in html
    )


@pytest.mark.django_db
def test_the_type_picker_answers_head_and_draws_a_width_as_a_class(client, preview):
    response = client.head(TYPE + "?system=a&surface=dashboard")
    assert response.status_code == 200
    _assert_sealed(response)
    html = client.get(TYPE + "?system=a&surface=dashboard&w=390").content.decode()
    assert 'class="dp-stage dp-stage--w390"' in html
    assert f'href="{TYPE}?system=b&amp;surface=dashboard&amp;lang=fr&amp;w=390"' in html, "a choice keeps the width"


@pytest.mark.django_db
def test_the_type_picker_says_what_the_control_is(client, preview):
    """V4 is in the picker to be compared against: it is not one of the proposals."""
    html = client.get(TYPE + "?system=v4").content.decode()
    assert f'src="{PROOF}research/type/V4/home.html"' in html
    assert '<span class="dp-bar__code">V4</span> Il controllo — Newsreader 300 + IBM Plex Sans</span>' in html
    assert '<span class="dp-bar__status">controllo — non una proposta</span>' in html
    assert '<p class="dp-bar__flag"><span class="dp-bar__flag-status">non una proposta</span></p>' in html
    assert NOT_APPROVED not in html and "non approvat" not in html


@pytest.mark.django_db
def test_the_type_picker_frames_arabic_only_where_the_research_built_it(client, preview):
    """Arabic exists for the home and the dashboard; anywhere else the picker says so and frames nothing."""
    # The Arabic home of TYPE A: framed, with what the owner must know about the Arabic faces.
    html = client.get(TYPE + "?system=a&surface=home&lang=ar").content.decode()
    assert f'<iframe class="dp-stage__frame" src="{PROOF}research/type/A/home-ar.html"' in html
    assert "Caratteri arabi provvisori: manca la lettura di un lettore marocchino (O10)." in html
    assert "La home araba è quella dell’intérim." in html
    assert (
        '<p class="dp-bar__flag"><span class="dp-bar__flag-status">non approvato</span> '
        '<strong class="dp-bar__flag-warning">caratteri arabi provvisori (O10)</strong></p>'
    ) in html
    # The menu was not built in Arabic, in any system.
    response = client.get(TYPE + "?system=a&surface=menu&lang=ar")
    assert response.status_code == 200
    html = response.content.decode()
    assert "<iframe" not in html and "dp-bar__open" not in html
    assert "la ricerca tipografica ha costruito in arabo soltanto la home e il cruscotto" in html
    assert '<strong class="dp-bar__warning">A · menu · ar: questa combinazione non esiste.</strong>' in html
    assert '<strong class="dp-bar__flag-warning">combinazione inesistente</strong>' in html
    # From the French menu, the way to the Arabic one is struck through; the surfaces are not.
    html = client.get(TYPE + "?system=a&surface=menu&lang=fr").content.decode()
    off = f'<a class="dp-bar__link dp-bar__link--off" href="{TYPE}?system=a&amp;surface=menu&amp;lang=ar" hreflang="ar"'
    assert off in html
    assert "العربية — tasto r · A · menu · ar non c’è" in html
    assert f'class="dp-bar__link" href="{TYPE}?system=a&amp;surface=home&amp;lang=fr"' in html
    # In Arabic, the surfaces without an Arabic page are the ones struck through.
    html = client.get(TYPE + "?system=a&surface=home&lang=ar").content.decode()
    for surface, off in (("home", False), ("menu", True), ("documents", True), ("case", True)):
        link = f'href="{TYPE}?system=a&amp;surface={surface}&amp;lang=ar"'
        assert (f'class="dp-bar__link dp-bar__link--off" {link}' in html) is off, surface


@pytest.mark.django_db
def test_the_type_picker_reports_a_page_that_is_not_on_disk(client, preview):
    """TYPE C is in the table and not in this package: reported by name, never framed, struck in the bar."""
    response = client.get(TYPE + "?system=c&surface=home")
    assert response.status_code == 200
    html = response.content.decode()
    assert "<iframe" not in html
    assert "research/type/C/home.html" in html and "non è nella cartella delle prove" in html
    assert "C · home · fr: il file manca nella cartella delle prove." in html
    # From TYPE A's home, the sheets that are not on disk are struck through; the ones that are, not.
    html = client.get(TYPE + "?system=a&surface=home").content.decode()
    for system, off in (
        ("v4", False),
        ("a", False),
        ("b", False),
        ("a2", True),
        ("ap", True),
        ("c", True),
        ("d", True),
    ):
        link = f'href="{TYPE}?system={system}&amp;surface=home&amp;lang=fr"'
        assert (f'class="dp-bar__link dp-bar__link--off" {link}' in html) is off, system


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query",
    [
        "system=zz",
        "system=A",  # the keys are lower case, like the hero picker's
        "system=a3",
        "system=",
        "system=a&surface=zz",
        "system=a&surface=Home",
        "system=a&surface=home-ar",
        "system=a&surface=../home",
        "system=a&surface=home&lang=de",
        "system=a&surface=home&lang=it",
        "surface=type.css",
    ],
)
def test_the_type_picker_answers_400_to_an_unknown_choice(client, preview, query):
    response = client.get(TYPE + "?" + query)
    assert response.status_code == 400
    _assert_sealed(response)
    html = response.content.decode()
    assert "Scelta sconosciuta" in html
    assert (
        "Sistemi: v4, a, a2, ap, b, c, d · superfici: home, menu, dashboard, documents, case · lingue: fr, ar." in html
    )
    assert f'<a href="{TYPE}?system=a&amp;surface=home&amp;lang=fr">Torna a TYPE A</a>' in html
    assert "<iframe" not in html and "dp-bar__group" not in html
    assert "frame-src 'self'" in _csp(response)


@pytest.mark.django_db
def test_an_unknown_choice_is_echoed_escaped(client, preview):
    """The 400 page prints the value it refused; a tag in it stays text."""
    for url in (PICKER + "?variant=<script>alert(1)</script>", TYPE + "?system=<script>alert(1)</script>"):
        response = client.get(url)
        assert response.status_code == 400
        html = response.content.decode()
        assert "<script>alert(1)</script>" not in html
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


@pytest.mark.django_db
def test_every_state_of_the_two_pickers_writes_its_status_in_the_flag(client, preview):
    """
    Review W1-2. Below 48 rem the flag is all the bar says about what it frames, and it used to
    exist only when there was something to warn about: on a phone no state said «non approvato».
    Now each of the hundred and six states — framed or not, warning or not — carries the status
    in the flag, in the closing words of the status itself.
    """
    from designpreview import services

    assert services.short_status(services.STATUS_GATE0) == "non approvata"
    assert services.short_status(services.STATUS_RESEARCH) == "non approvato"
    assert services.short_status(services.STATUS_CONTROL) == "non una proposta"
    hero = [
        (PICKER, {"variant": variant, "lang": lang, "phase": phase}, services.HERO_VARIANTS[variant].status)
        for variant in services.HERO_VARIANTS
        for lang in services.LANGS
        for phase in services.PHASES
    ]
    type_ = [
        (TYPE, {"system": system, "surface": surface, "lang": lang}, services.TYPE_SYSTEMS[system].status)
        for system in services.TYPE_SYSTEMS
        for surface in services.TYPE_SURFACES
        for lang in services.LANGS
    ]
    assert (len(hero), len(type_)) == (36, 70)
    said = set()
    for url, query, status in hero + type_:
        html = client.get(url, query).content.decode()
        short = services.short_status(status)
        assert status.endswith(f" — {short}") and short.startswith("non "), status
        assert html.count('class="dp-bar__flag"') == 1, query
        assert f'<p class="dp-bar__flag"><span class="dp-bar__flag-status">{short}</span>' in html, query
        assert f'<span class="dp-bar__status">{status}</span>' in html, query
        said.add(short)
    assert said == {"non approvata", "non approvato", "non una proposta"}


# --------------------------------------------------------------------------- the compare view


@pytest.mark.django_db
def test_the_compare_view_frames_the_two_phones_of_mes_pieces_side_by_side(client, preview):
    """
    X-3 (research consolidation K5). Two lanes built «Mes pièces» for a phone: the platform
    audit's proposal (wave 2) and the documents lane's (wave 3). The compare view frames the two
    at the same width, each in a frame of its own — so each scrolls on its own — named by their
    authors' roles, in the order they arrived and said to be that order: nothing on the page
    says which one is the candidate, and nothing measures one against the other. Sealed like
    every preview page; its policy adds frame-src 'self' and nothing else, and no one frames it.
    """
    response = client.get(COMPARE + "?pair=mes-pieces&lang=fr")
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert '<html lang="it" dir="ltr"' in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
    assert "<title>«Mes pièces» su telefono — Français · Confronto · Italy Legal Entry™</title>" in html
    csp = _csp(response)
    assert "frame-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp, "the compare view itself is framed by no one"
    assert "script-src 'self'" in csp and "style-src 'self'" in csp and "unsafe" not in csp
    assert response["X-Frame-Options"] == "DENY"
    # The two frames, left to right in the order they arrived, each with its author's role.
    sides = [
        (
            "La proposta dell’audit UI-UX-Pro-Max della piattaforma",
            "seconda ondata",
            "research/uiux-platform/proto/docs-fr.html",
        ),
        ("La proposta dello specialista dello spazio documenti", "terza ondata", "research/documents/index.html"),
    ]
    frames = re.findall(r'<iframe class="dp-compare__frame" src="([^"]+)" title="([^"]+)"></iframe>', html)
    assert frames == [(PROOF + file, f"{who} — {NOT_APPROVED}") for who, _wave, file in sides]
    heads = re.findall(r'<figcaption class="dp-compare__head">(.*?)</figcaption>', html, flags=re.S)
    assert len(heads) == 2
    for head, (who, wave, file) in zip(heads, sides, strict=True):
        assert f'<span class="dp-compare__who">{who}</span>' in head
        assert f'<span class="dp-compare__wave">{wave}</span>' in head
        assert f'<span class="dp-compare__status">{NOT_APPROVED}</span>' in head
        assert f'<a class="dp-compare__open" href="{PROOF}{file}" target="_blank" rel="noopener"' in head
    # The bar: the way back, the language with its keys, what is compared and in what order.
    assert '<header class="dp-bar dp-bar--compare" data-dp-bar>' in html
    assert f'<a class="dp-bar__home" href="{HUB}"' in html
    assert (
        f'<a class="dp-bar__link" href="{COMPARE}?pair=mes-pieces&amp;lang=fr" hreflang="fr" data-dp-key="f" '
        'aria-current="true" title="Français — tasto f">fr</a>'
    ) in html
    assert _keys(html) == ["f", "r"]
    assert '<span class="dp-bar__code">K5</span> «Mes pièces» su telefono</span>' in html
    # Drawn from 48 rem, where the two stand side by side or — up to 54 rem — one under the other:
    # «prima» and «poi» are true in both, «a sinistra» and «a destra» were true in one (review HC-2).
    assert (
        "Le due pagine a 390 px, ciascuna con il suo scorrimento; in ordine d’arrivo — prima la seconda ondata, poi "
        "la terza ondata — e non di preferenza: decide il proprietario."
    ) in html
    assert "sinistra" not in html and "destra" not in html
    text = re.sub(r"<[^>]+>", " ", html).lower()
    for words in ("candidat", "raccomand", "migliore", "più forte", "superiore", "preferit", "648", "669"):
        assert words not in text, words
    assert "dp-compare__caution" not in html, "nothing to warn about in French"
    assert html.count("<script") == 1 and "js/dev/designpreview.js" in html
    assert not re.search(r"<[^>]+\sstyle=", html)
    assert scan(html) == []
    assert "{#" not in html and "{%" not in html
    assert client.head(COMPARE + "?pair=mes-pieces&lang=fr").status_code == 200
    assert client.get(COMPARE).content.decode() == html, "the comparison of «Mes pièces» in French by default"


@pytest.mark.django_db
def test_the_compare_view_says_what_is_missing_and_never_frames_another_page(client, preview):
    """
    The auditor's Arabic «Mes pièces» is not in this package. The Arabic comparison frames the page
    that is there, says by name which one is missing where its frame would be — the caption, with
    its status, stays — carries the caution of every Arabic page of the package (O10), and strikes
    its language through in the bar; the hub's entry for it says «manca». Remove a page and its
    frame goes at the next request; the view never falls back on another page.
    """
    response = client.get(COMPARE + "?pair=mes-pieces&lang=ar")
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert "<title>«Mes pièces» su telefono — العربية · Confronto · Italy Legal Entry™</title>" in html
    assert re.findall(r'<iframe class="dp-compare__frame" src="([^"]+)"', html) == [
        f"{PROOF}research/documents/ar.html"
    ]
    assert "Il file research/uiux-platform/proto/docs-ar.html non è nella cartella delle prove" in html
    assert html.count(f'<span class="dp-compare__status">{NOT_APPROVED}</span>') == 2, "framed or not, the status"
    assert (
        '<p class="dp-compare__caution">Caratteri arabi provvisori: manca la lettura di un lettore marocchino (O10).</p>'
    ) in html
    assert f'class="dp-bar__link dp-bar__link--off" href="{COMPARE}?pair=mes-pieces&amp;lang=ar"' in html
    assert "«Mes pièces» su telefono · ar: una delle due pagine non c’è" in html
    hub = client.get(HUB).content.decode()
    assert f'href="{COMPARE}?pair=mes-pieces&amp;lang=fr"' in hub
    assert ">confronto · ar · manca</span>" in hub
    (preview / "research" / "documents" / "index.html").unlink()
    html = client.get(COMPARE + "?pair=mes-pieces&lang=fr").content.decode()
    framed = re.findall(r'<iframe class="dp-compare__frame" src="([^"]+)"', html)
    assert framed == [f"{PROOF}research/uiux-platform/proto/docs-fr.html"]
    assert "Il file research/documents/index.html non è nella cartella delle prove" in html
    assert ">confronto · fr · manca</span>" in client.get(HUB).content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query",
    [
        "pair=zz",
        "pair=",
        "pair=Mes-Pieces",
        "pair=../.work",
        "pair=research/documents/index.html",
        "pair=mes-pieces&lang=de",
        "pair=mes-pieces&lang=../../.work",
        "pair=mes-pieces&lang=",
        "lang=it",
    ],
)
def test_the_compare_view_answers_400_to_an_unknown_choice(client, preview, query):
    """A value the table does not know — a path among them — is answered 400, never with a frame."""
    response = client.get(COMPARE + "?" + query)
    assert response.status_code == 400
    _assert_sealed(response)
    html = response.content.decode()
    assert "Scelta sconosciuta" in html
    assert "Confronti: mes-pieces · lingue: fr, ar." in html
    assert f'<a href="{COMPARE}?pair=mes-pieces&amp;lang=fr">Torna al confronto di «Mes pièces»</a>' in html
    assert "<iframe" not in html and "dp-bar__group" not in html
    assert "frame-src 'self'" in _csp(response)


def test_the_compare_view_draws_its_two_frames_at_the_width_of_its_table():
    """
    The width is the table's (``Comparison.width``) and the stylesheet's: each frame is that wide
    inside its two hairlines. From 54 rem — two frames, their gap and the stage's padding need
    848 px of the 864 — they stand side by side, in two columns of that width, as tall as the
    window allows, the two captions on one row and the two frames on the next, so that the frames
    start and end on one line whatever a caption wraps to; below, one under the other, each up to
    that width, and the stage scrolls.
    Below 48 rem the compare bar is one row: the way back and the language. No rule of the sheet
    hides a caption or a frame.
    """
    from designpreview import services

    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    width = services.COMPARISONS["mes-pieces"].width
    assert width == 390 and [side.wave for side in services.COMPARISONS["mes-pieces"].sides] == [
        "seconda ondata",
        "terza ondata",
    ]
    (wide,) = _media_blocks(css, "min-width: 54rem")
    narrow = css.replace(wide, "")
    item = _declarations(narrow, ".dp-compare__item")
    assert f"max-inline-size: calc({width}px + 2px)" in item and "block-size: 80dvh" in item
    assert "grid-template-columns: minmax(0, 1fr)" in _declarations(narrow, ".dp-compare__pair")
    assert "overflow-y: auto" in _declarations(narrow, ".dp-compare")
    frame = _declarations(narrow, ".dp-compare__frame")
    assert "inline-size: 100%" in frame and "border: 1px solid" in frame and "flex: 1 1 auto" in frame
    pair = _declarations(wide, ".dp-compare__pair")
    assert f"grid-template-columns: repeat(2, calc({width}px + 2px))" in pair
    assert "grid-template-rows: auto minmax(0, 1fr)" in pair, "the captions share a row, the frames the next"
    wide_item = _declarations(wide, ".dp-compare__item")
    assert f"inline-size: calc({width}px + 2px)" in wide_item and "grid-template-rows: subgrid" in wide_item
    assert "overflow: hidden" in _declarations(wide, ".dp-compare")
    assert 2 * (width + 2) + 32 + 2 * 16 <= 54 * 16, "two frames, the gap (--s-8) and the padding (--s-4) fit in 54rem"
    (phone,) = [block for block in _media_blocks(css, "max-width: 47.99rem") if ".dp-bar" in block]
    assert re.findall(r'"([^"]+)"', _declarations(phone, ".dp-bar--compare")) == ["home lang"]
    for selectors, body in _rules(css):
        if any("dp-compare" in selector for selector in selectors):
            for road in ("display: none", "visibility", "opacity", "clip", "text-indent", "font-size: 0"):
                assert road not in body, (selectors, road)


def test_every_side_of_a_comparison_names_a_page_in_every_language():
    """
    Review HS-2. The compare view reads ``side.files[lang]`` for each language of ``LANGS`` on every
    request — its language choices ask for both — and so does the hub for each of its entries: a
    side without a page in one language would answer 500, even in the language it has. The table
    names a page in every language for every side; whether that page is on disk is the view's to
    say, in a sentence, and the hub's, in «manca».
    """
    from designpreview import services

    assert services.COMPARISONS, "the table is empty"
    for comparison in services.COMPARISONS.values():
        for side in comparison.sides:
            assert set(side.files) == set(services.LANGS), (comparison.key, side.author, sorted(side.files))


# --------------------------------------------------------------------------- the database
#
# 2 October 2026: the preview answered 500 «too many clients already» for twenty minutes, and so
# did every other dev server on the same PostgreSQL. The cause is in
# docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md; what must never come back is held here.


def _backends() -> int:
    """
    PostgreSQL backends on this test database other than the one that asks — as they are now.

    Inside a transaction PostgreSQL answers ``pg_stat_activity`` from the snapshot it took at the
    first question, and most tests here run inside one: asked twice, it would say twice what it
    saw the first time, and «nothing was left behind» would be true of any burst. The snapshot
    is discarded before every count.
    """
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("select pg_stat_clear_snapshot()")
        cursor.execute(
            "select count(*) from pg_stat_activity where datname = current_database() and pid <> pg_backend_pid()"
        )
        return cursor.fetchone()[0]


def _baseline() -> int:
    """
    ``_backends()`` once nothing is waiting to be collected. A connection whose thread has ended
    lives until Python's garbage collector finds its wrapper — that is the outage — and one left
    by an earlier test of the session could be found in the middle of this one, and make a count
    go down for a reason that is not this test's.
    """
    gc.collect()
    return _backends()


@contextlib.contextmanager
def _runserver(handler=None):
    """
    The server ``manage.py runserver`` builds (django.core.servers.basehttp.run): Django's
    ``WSGIServer`` under ``socketserver.ThreadingMixIn``, daemon threads, Django's request handler.
    One thread per socket, HTTP/1.1 keep-alive, and nothing that closes a thread's database
    connection when the thread ends.

    Deliberately NOT pytest-django's ``live_server``: that one is ``ThreadedWSGIServer``, which
    closes every connection after every request — the very thing ``runserver`` does not do — and
    would have hidden what happened on 2 October.
    """
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer

    server = type("WSGIServer", (socketserver.ThreadingMixIn, WSGIServer), {})(("127.0.0.1", 0), WSGIRequestHandler)
    server.daemon_threads = True
    server.set_app(handler or WSGIHandler())
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    try:
        # The preview answers this server's own port (designpreview.access), as a lane's answers its own.
        with override_settings(ILE_DESIGN_PREVIEW_PORT=server.server_port):
            yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=10)


def _burst(base: str, paths: list[str], total: int, concurrency: int) -> dict[int, int]:
    """
    ``total`` GETs over ``paths`` in turn, ``concurrency`` at a time, each on a socket of its own —
    what urllib does, and what a browser launched for one capture does: for the server, a new
    thread per request. The dev server queues ten connections; ``concurrency`` stays below that.
    """

    def get(index: int) -> int:
        url = base + paths[index % len(paths)]
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    response.read()
                    return response.status
            except urllib.error.HTTPError as error:
                error.read()
                return error.code
            except urllib.error.URLError:
                if attempt == 2:
                    raise
                time.sleep(0.05)
        raise AssertionError("unreachable")

    with concurrent.futures.ThreadPoolExecutor(concurrency) as pool:
        return dict(collections.Counter(pool.map(get, range(total))))


def _elsewhere(function):
    """Run ``function`` on a thread of its own, as a request is — never on the test's, whose connection is the test's."""
    with concurrent.futures.ThreadPoolExecutor(1) as pool:
        return pool.submit(function).result(timeout=30)


def test_no_preview_view_asks_for_a_transaction(preview):
    """
    ``ATOMIC_REQUESTS`` opens a PostgreSQL connection for every view call, before the view runs:
    Django wraps the view in ``transaction.atomic()``, and entering it connects. That is right for
    the site and was fatal for a view that sends a stylesheet. The views of the preview write
    nothing — the persona switch writes the session and the audit row of a sign-in, outside any
    transaction of its own — and each is marked on the very callable the URLconf holds, which is
    where Django looks (``BaseHandler.make_view_atomic``). The site's own pages keep their
    transaction.
    """
    for url in (
        LANDING,
        INDEX,
        ENTER + "qa-doc-person/",
        EXIT,
        STATE_429,
        DECISIONS + "w1-a/CD_DECISION.md",
        OLD_PICKER,
        OLD_PROOF + "home/phase3.html",
        HUB,
        PICKER,
        TYPE,
        COMPARE,
        PROOF + "home/phase3.html",
        PROOF + "assets/css/tokens.css",
        SPECIMENS + "type/",
    ):
        assert resolve(url).func._non_atomic_requests == {"default"}, url
    assert not getattr(resolve("/fr/compte/login/").func, "_non_atomic_requests", None)
    assert settings.DATABASES["default"]["ATOMIC_REQUESTS"] is True, "the rule this test is about"


@pytest.mark.django_db
def test_a_picker_and_a_proof_file_read_nothing(client, preview, django_assert_num_queries):
    """
    Not a query, not a savepoint: a proof file is a file, and a picker is a bar of links over a
    frame — the compare view the same bar over two — rendered without the request's context
    processors, which read ``SiteSettings`` for every template they are run for and whose values
    frame.html and compare.html never print. The hub extends base.html and keeps its reads; it is
    the one preview page that needs the database.
    """
    with django_assert_num_queries(0):
        assert client.get(LANDING).status_code == 200
        assert client.get(LANDING + "?page=/ar/espace-reserve/").status_code == 200
        assert client.get(INDEX).status_code == 200
        assert client.get(OLD_PICKER + "?variant=hb").status_code == 302
        assert client.get(COMPARE + "?pair=mes-pieces&lang=fr").status_code == 200
        assert client.get(COMPARE + "?pair=mes-pieces&lang=ar").status_code == 200
        assert client.get(COMPARE + "?pair=zz").status_code == 400
        assert client.head(COMPARE).status_code == 200
        assert client.get(PICKER + "?variant=hb").status_code == 200
        assert client.get(PICKER + "?variant=hc&lang=ar").status_code == 200
        assert client.get(PICKER + "?variant=he").status_code == 200
        assert client.get(PICKER + "?variant=hz").status_code == 400
        assert client.get(TYPE + "?system=a&surface=dashboard").status_code == 200
        assert client.get(TYPE + "?system=zz").status_code == 400
        for relative in ("home/phase3.html", "assets/css/tokens.css", "assets/fonts/v5.woff2", "home/measure.json"):
            response = client.get(PROOF + relative)
            assert response.status_code == 200 and b"".join(response.streaming_content), relative
        assert client.head(PROOF + "home/home.js").status_code == 200


@pytest.mark.django_db
def test_a_burst_of_proof_requests_opens_no_connection_and_leaves_none_behind(preview, monkeypatch):
    """
    The regression of 2 October 2026, at the server that suffered it.

    Before: every proof request — a font, an image — opened a PostgreSQL connection on its own
    thread, the thread ended with its socket, and the connection stayed, owned by nobody, until
    Python's garbage collector happened to find it; 200 requests at a concurrency of 32 left 85
    behind, and the bursts of five review agents took all 300. Now a burst of proof files and
    picker pages — on a socket each, the worst case — opens no connection at all: none is
    created in this process while it runs, and PostgreSQL counts the same backends on this
    database before, during and after.

    The server is given the lifetime every dev server has (``CONN_MAX_AGE = 60``, base.py). The
    test settings replace the database entry and fall back to Django's zero, under which a
    connection that should never have been opened would at least be closed — and the second
    half of this test would have nothing to find.
    """
    from django.db import connections
    from django.db.backends.signals import connection_created

    monkeypatch.setitem(connections.settings["default"], "CONN_MAX_AGE", 60)
    opened: list[str] = []

    def remember(sender, connection, **kwargs):
        opened.append(threading.current_thread().name)

    paths = [
        PROOF + "home/phase3.html",
        PROOF + "assets/css/tokens.css",
        PROOF + "home/home.css",
        PROOF + "home/home.js",
        PROOF + "assets/fonts/v5.woff2",
        PROOF + "assets/img/door.webp",
        PROOF + "assets/img/mark.svg",
        PROOF + "research/hero/hc/index.html",
        PICKER + "?variant=hb&lang=fr&phase=3",
        TYPE + "?system=a&surface=home&lang=fr",
        COMPARE + "?pair=mes-pieces&lang=fr",
        PROOF + "research/documents/index.html",
    ]
    before = _baseline()
    connection_created.connect(remember)
    try:
        with _runserver() as base:
            statuses = _burst(base, paths, total=120, concurrency=8)
            during = _backends()
        after = _backends()
    finally:
        connection_created.disconnect(remember)
    assert statuses == {200: 120}
    assert opened == [], f"{len(opened)} connections were opened by {len(set(opened))} request threads"
    assert (during, after) == (before, before), "a burst of proof requests left PostgreSQL backends behind"


@pytest.mark.django_db(transaction=True)
def test_a_burst_on_pages_that_read_the_database_stays_under_the_ceiling(preview, monkeypatch):
    """
    The hub, a page of the site and a missing proof file (a 404 is looked up in ``cms.Redirect``)
    do read the database. Fired at the ``runserver`` class through the preview's middleware — with
    a ceiling of two, and with the lifetime that used to keep a connection for a minute after its
    request, to show that the guarantee does not rest on ``CONN_MAX_AGE`` staying at zero — every
    request is served, PostgreSQL never counts more than two backends from this burst, and none
    is left when it ends.
    """
    from django.core.handlers.wsgi import WSGIHandler
    from django.db import connections
    from django.db.backends.signals import connection_created

    ceiling = 2
    monkeypatch.setitem(connections.settings["default"], "CONN_MAX_AGE", 60)
    opened: list[int] = []

    def remember(sender, connection, **kwargs):
        opened.append(1)

    # The preview's chain already stands the ceiling first: one ceiling, never two.
    chain = [CEILING, *(name for name in settings.MIDDLEWARE if name != CEILING)]
    with override_settings(MIDDLEWARE=chain, ILE_DESIGN_PREVIEW_DB_CEILING=ceiling):
        handler = WSGIHandler()
    paths = [HUB, "/fr/compte/login/", PROOF + "nope/missing.css"]
    before, peak = _baseline(), 0
    connection_created.connect(remember)
    try:
        with _runserver(handler) as base, concurrent.futures.ThreadPoolExecutor(1) as side:
            burst = side.submit(_burst, base, paths, 36, 8)
            while not burst.done():
                peak = max(peak, _backends() - before)
            statuses = burst.result()
        after = _backends()
    finally:
        connection_created.disconnect(remember)
    assert statuses == {200: 24, 404: 12}
    assert len(opened) >= 36, "each of these requests reads the database: the test would prove nothing otherwise"
    assert 1 <= peak <= ceiling, f"PostgreSQL counted {peak} backends from a burst under a ceiling of {ceiling}"
    assert after == before, "connections were left behind"


@pytest.mark.django_db
def test_no_more_connections_than_the_ceiling_whatever_arrives(rf, monkeypatch):
    """
    The ceiling itself, without a server in the way and without chance: twenty-four requests on
    twenty-four threads meet a ceiling of three. Every request opens its thread's connection,
    waits for two others to be in with it, asks PostgreSQL how many backends this database has,
    and leaves only when the other two have asked as well — so nobody counts while a slot is
    changing hands. The answer is three more than before the burst, every time: never four, with
    a lifetime that would have kept each connection for a minute. And when the burst ends, none.
    """
    from designpreview import middleware
    from django.db import connection, connections

    ceiling, total = 3, 24
    monkeypatch.setitem(connections.settings["default"], "CONN_MAX_AGE", 60)
    all_in, all_counted = threading.Barrier(ceiling), threading.Barrier(ceiling)
    counted: list[int] = []

    def view(request):
        connection.ensure_connection()
        all_in.wait(timeout=20)
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from pg_stat_activity where datname = current_database()")
            counted.append(cursor.fetchone()[0])
        all_counted.wait(timeout=20)
        return HttpResponse("ok")

    with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=ceiling):
        gate = middleware.ConnectionCeilingMiddleware(view)
    assert gate.ceiling == ceiling
    before = _baseline() + 1  # … and the test's own

    def one(_index: int) -> int:
        response = gate(rf.get(HUB))
        response.close()  # what the WSGI server does when the response has been sent: request_finished
        return response.status_code

    with concurrent.futures.ThreadPoolExecutor(total) as pool:
        statuses = list(pool.map(one, range(total)))
        assert statuses == [200] * total
        assert counted == [before + ceiling] * total, sorted(set(counted))
        assert _backends() + 1 == before, "the threads are still alive, and hold nothing"


def test_the_ceiling_makes_a_request_wait_and_then_says_so_in_plain_words(rf, monkeypatch):
    """
    A request that finds every slot taken waits; it is not refused at once, and it does not wait
    for ever. After ``WAIT_SECONDS`` it is answered 503 with a sentence, ``Retry-After`` and the
    two headers of every preview response — a stuck request can cost the preview a page, never
    the server its voice. When the slot is back the next request is served. The sentence speaks
    of slots, not of «connections in use» (review W2-1): a slot can be held while no connection
    is open, and the SQL count of the outage note would then say 0 of a server answering 503.
    """
    from designpreview import middleware

    monkeypatch.setattr(middleware, "WAIT_SECONDS", 0.3)
    inside, leave = threading.Event(), threading.Event()

    def view(request):
        inside.set()
        assert leave.wait(20)
        return HttpResponse("ok")

    with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=1):
        gate = middleware.ConnectionCeilingMiddleware(view)

    def served() -> int:
        response = gate(rf.get(HUB))
        response.close()
        return response.status_code

    with concurrent.futures.ThreadPoolExecutor(1) as holder:
        first = holder.submit(served)
        assert inside.wait(20)
        started = time.monotonic()
        refused = _elsewhere(lambda: gate(rf.get(PICKER)))
        waited = time.monotonic() - started
        leave.set()
        assert first.result(timeout=20) == 200
    assert refused.status_code == 503 and waited >= 0.3
    assert refused["Retry-After"] == "2"
    assert refused["Cache-Control"] == "no-store" and refused["X-Robots-Tag"] == "noindex, nofollow"
    assert refused["Content-Type"] == "text/plain; charset=utf-8"
    assert refused["X-Content-Type-Options"] == "nosniff"
    assert refused.content.decode() == (
        "Anteprima occupata: questo server ha 1 posto per le richieste che usano il database, ed è preso da più "
        "di 0.3 secondi. Riprovare tra poco.\n"
    )
    assert "connessioni" not in refused.content.decode()
    with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=8):
        eight = middleware.ConnectionCeilingMiddleware(view).busy(rf.get(HUB)).content.decode()
    assert eight.startswith(
        "Anteprima occupata: questo server ha 8 posti per le richieste che usano il database, e sono tutti presi "
        "da più di 0.3 secondi."
    )
    assert _elsewhere(served) == 200, "the slot went back with the first response"
    # The ceiling is read from the settings, is 8 without one, and is never less than one.
    assert middleware.ConnectionCeilingMiddleware(view).ceiling == middleware.DEFAULT_CEILING == 8
    with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=0):
        assert middleware.ConnectionCeilingMiddleware(view).ceiling == 1


def test_a_file_response_gives_its_slot_back_before_it_is_sent(rf, tmp_path, monkeypatch):
    """
    A file on disk asks the database nothing while it travels, and a slow reader of a large one —
    a video of a prototype — must not hold a slot for as long as it reads. With a ceiling of one,
    a file response that is neither read nor closed does not keep the next request waiting; nor,
    since review W2-1, does a page that is never closed: a page is complete when it leaves the
    middleware, and a slot that waited for its ``close()`` could be lost with it
    (test_a_slot_is_not_lost_when_request_finished_never_comes).
    """
    from designpreview import middleware

    monkeypatch.setattr(middleware, "WAIT_SECONDS", 0.3)
    video = tmp_path / "prototype.webm"
    video.write_bytes(b"\x1aE\xdf\xa3 fake")
    answers = {
        "file": lambda: FileResponse(video.open("rb"), content_type="video/webm"),
        "page": lambda: HttpResponse("ok"),
    }

    def gate_for(kind: str):
        with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=1):
            return middleware.ConnectionCeilingMiddleware(lambda request: answers[kind]())

    gate = gate_for("file")
    unread = _elsewhere(lambda: gate(rf.get(PROOF + "x.webm")))
    second = _elsewhere(lambda: gate(rf.get(PROOF + "x.webm")))
    assert (unread.status_code, second.status_code) == (200, 200), "the first file still holds the only slot"
    _elsewhere(lambda: (unread.close(), second.close()))
    gate = gate_for("page")
    unfinished = _elsewhere(lambda: gate(rf.get(HUB)))
    assert unfinished.status_code == 200
    assert _elsewhere(lambda: gate(rf.get(HUB))).status_code == 200, "a page that was never closed kept its slot"


def test_a_slot_is_not_lost_when_request_finished_never_comes(rf, monkeypatch):
    """
    Review W2-1. Under ``runserver`` the ``request_finished`` signal is sent by
    ``ServerHandler.close()``, which reads what is left of the request body before it closes the
    response: a client that announced a body and never sent it keeps the thread waiting, and one
    that resets after the answer makes that read fail — wsgiref swallows the error, the signal
    never comes, the thread ends. A slot given back at that signal was lost for the life of the
    process: eight of them, and the preview answered 503 until a restart, with no connection open.

    So, with a ceiling of one: a page answered on a thread that ends without ``close()`` leaves
    its slot free, at once; the signal, when it does come late, finds nothing to return (the
    semaphore is bounded — a second release would raise); a view that raises leaves the slot free
    too; and a stream that is not a file is the one response that keeps its slot while it is
    sent, until its own thread closes it — the preview has no such response, and ``apps/`` none.
    """
    from designpreview import middleware

    monkeypatch.setattr(middleware, "WAIT_SECONDS", 0.3)

    def gate_for(view):
        with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=1):
            return middleware.ConnectionCeilingMiddleware(view)

    def one_free_slot(gate) -> bool:
        if not gate.slots.acquire(timeout=0):
            return False
        try:
            return not gate.slots.acquire(timeout=0)
        finally:
            gate.slots.release()

    # A page, on a thread that ends without close(): the slot is free before the next request asks.
    gate = gate_for(lambda request: HttpResponse("ok"))
    never_closed = _elsewhere(lambda: gate(rf.get(HUB)))
    assert never_closed.status_code == 200
    assert _elsewhere(lambda: gate(rf.get(PICKER))).status_code == 200, "the slot of a page never closed was lost"
    assert one_free_slot(gate)

    # The signal that does come — late, on the serving thread, as the server sends it — finds
    # nothing to return: meanwhile another thread was served, and the bound was never exceeded.
    def page_then_late_close() -> tuple[int, int]:
        response = gate(rf.get(HUB))
        meanwhile = _elsewhere(lambda: gate(rf.get(PICKER)))
        response.close()
        return response.status_code, meanwhile.status_code

    assert _elsewhere(page_then_late_close) == (200, 200)
    assert one_free_slot(gate)

    # A view that raises: the exception is the caller's, the slot is nobody's.
    answers = iter([None, HttpResponse("ok")])

    def flaky(request):
        response = next(answers)
        if response is None:
            raise RuntimeError("the view failed")
        return response

    gate = gate_for(flaky)
    with pytest.raises(RuntimeError, match="the view failed"):
        _elsewhere(lambda: gate(rf.get(HUB)))
    assert _elsewhere(lambda: gate(rf.get(HUB))).status_code == 200
    assert one_free_slot(gate)

    # A stream that is not a file keeps its slot while it is sent — its generator may read the
    # database — and gives it back when the thread that serves it closes it.
    gate = gate_for(lambda request: StreamingHttpResponse(iter([b"a", b"b"])))

    def stream_then_close() -> tuple[int, int]:
        streaming = gate(rf.get(HUB))
        meanwhile = _elsewhere(lambda: gate(rf.get(HUB)))
        streaming.close()
        return streaming.status_code, meanwhile.status_code

    assert _elsewhere(stream_then_close) == (200, 503)

    def stream_and_close() -> int:
        streaming = gate(rf.get(HUB))
        streaming.close()
        return streaming.status_code

    assert _elsewhere(stream_and_close) == 200
    assert one_free_slot(gate)


@pytest.mark.django_db(transaction=True)
def test_a_client_that_resets_after_its_page_costs_the_server_no_slot(preview, monkeypatch):
    """
    The same through the server ``runserver`` builds, as the review measured it on the commit
    before this one (PREVIEW_REVIEW_W2.md §2.3). Three GETs of the hub announce a body of 100 000
    bytes and send ten: the page is answered — the hub does not read the body — and the server's
    ``close()`` then waits for the rest, which is where ``request_finished`` would be sent. With
    a ceiling of one, while the three wait: the next requests are served at once. Then the three
    clients reset; the threads end, the signal never comes; hub, picker and proof file are served
    all the same, nothing was logged as taken, and PostgreSQL counts nothing left behind — the
    hub's connection was closed when its page left the middleware, not at a signal.
    """
    from designpreview import middleware
    from django.core.handlers.wsgi import WSGIHandler

    monkeypatch.setattr(middleware, "WAIT_SECONDS", 1.0)
    chain = [CEILING, *(name for name in settings.MIDDLEWARE if name != CEILING)]
    with override_settings(MIDDLEWARE=chain, ILE_DESIGN_PREVIEW_DB_CEILING=1):
        handler = WSGIHandler()

    def page_with_a_body_to_come(host: str, port: int) -> tuple[socket.socket, int]:
        sock = socket.create_connection((host, port), timeout=30)
        head = f"GET {HUB} HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Length: 100000\r\n\r\n".encode()
        sock.sendall(head + b"x" * 10)
        raw = b""
        while b"\r\n\r\n" not in raw:
            raw += sock.recv(65536)
        header, _, body = raw.partition(b"\r\n\r\n")
        status = int(header.split(b" ", 2)[1])
        length = re.search(rb"(?im)^content-length:\s*(\d+)", header)
        # The ceiling's 503 leaves before CommonMiddleware and carries no Content-Length: the
        # status is the finding, the body is not read.
        while length is not None and len(body) < int(length.group(1)):
            body += sock.recv(65536)
        return sock, status

    def reset(sock: socket.socket) -> None:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("hh", 1, 0))
        sock.close()

    before, held = _baseline(), []
    with _runserver(handler) as base:
        host, port = base.removeprefix("http://").split(":")
        for _ in range(3):
            sock, status = page_with_a_body_to_come(host, int(port))
            assert status == 200
            held.append(sock)
        assert _burst(base, [HUB, PICKER + "?variant=he&lang=fr&phase=3"], 4, 2) == {200: 4}
        for sock in held:
            reset(sock)
        time.sleep(0.5)
        paths = [HUB, PICKER + "?variant=hb&lang=fr&phase=3", PROOF + "home/phase3.html"]
        assert _burst(base, paths, 9, 3) == {200: 9}
        during = _backends()
    assert during == before and _backends() == before, "the pages whose clients reset left connections behind"


@pytest.mark.django_db(transaction=True)
def test_a_client_that_withholds_its_body_costs_a_thread_never_a_slot(preview, monkeypatch):
    """
    Review W1-P, performance P-1. The CSRF check reads the body of a POST, and it ran inside the
    slot: eight clients that announced a body and never sent it held all eight slots, and every page
    — the landing, which reads nothing, included — answered 503 after twenty seconds. The ceiling
    now reads a small announced body before it takes a slot. With a ceiling of two: three sockets
    announce a body to the persona switch, with its CSRF cookie, and withhold it; the landing is
    served at once all the same; once they close, nothing is left behind.
    """
    from designpreview import middleware
    from django.core.handlers.wsgi import WSGIHandler

    monkeypatch.setattr(middleware, "WAIT_SECONDS", 2.0)
    with override_settings(ILE_DESIGN_PREVIEW_DB_CEILING=2):
        handler = WSGIHandler()
    before, held = _baseline(), []
    with _runserver(handler) as base:
        host, port = base.removeprefix("http://").split(":")
        for _ in range(3):
            sock = socket.create_connection((host, int(port)), timeout=30)
            head = (
                f"POST {ENTER}qa-doc-person/ HTTP/1.1\r\nHost: {host}:{port}\r\n"
                "Cookie: ile_v5_csrftoken=abcdefghijklmnopqrstuvwxyzABCDEF\r\n"
                "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: 200\r\n\r\n"
            )
            sock.sendall(head.encode())
            held.append(sock)
        time.sleep(0.3)
        started = time.monotonic()
        with urllib.request.urlopen(base + LANDING, timeout=30) as response:
            assert response.status == 200
        assert time.monotonic() - started < 1.5, "the landing waited for a slot the withheld bodies held"
        for sock in held:
            sock.close()
        time.sleep(0.5)
        assert _burst(base, [LANDING, INDEX], 6, 3) == {200: 6}
    assert _backends() == before, "the withheld requests left connections behind"
    source = (ROOT / "apps" / "designpreview" / "middleware.py").read_text(encoding="utf-8")
    assert source.index("_read_a_small_body(request)") < source.index("self.slots.acquire(timeout=WAIT_SECONDS)")


def test_the_ceiling_is_installed_by_the_preview_block_alone():
    """Under the test settings — and in production — the middleware is not in the chain and was never asked for."""
    assert CEILING not in settings.MIDDLEWARE
    assert not hasattr(settings, "ILE_DESIGN_PREVIEW_DB_CEILING")
    for name in ("base.py", "test.py", "prod.py"):
        source = (ROOT / "config" / "settings" / name).read_text(encoding="utf-8")
        assert "designpreview" not in source, name
    dev = (ROOT / "config" / "settings" / "dev.py").read_text(encoding="utf-8")
    block = dev[dev.index("if ILE_DESIGN_PREVIEW:") :]
    for line in (
        f'        "{CEILING}",\n        *MIDDLEWARE,\n        "{FRAMES}",\n        "{READ_ONLY}",\n    ]',
        '            "CONN_MAX_AGE": 0,',
        '            "CONN_HEALTH_CHECKS": True,',
        '                "application_name": env("PGAPPNAME", default="ile-design-preview"),',
        '    ILE_DESIGN_PREVIEW_DB_CEILING = env.int("ILE_DESIGN_PREVIEW_DB_CEILING", default=8)',
    ):
        assert line in block, line
    assert "max_connections" not in dev, "the answer to the outage is not a higher limit"


# --------------------------------------------------------------------------- the specimen boards

#: A board as a family writes one (templates/dev/designpreview/specimens/README.md): a standalone
#: document that loads the product's own sheet, shows a sample in its own language, and prints the one
#: variable its context holds — and two the request's context would have given it, which must be empty.
BOARD = (
    '{% load static %}<!doctype html><html lang="it"><head><meta charset="utf-8">'
    "<title>Specimen — {{ board }}</title>"
    '<link rel="stylesheet" href="{% static \'css/dist/main.css\' %}"></head>'
    '<body><h1>{{ board }}</h1><p lang="fr">Mes pièces</p>'
    '<p class="context">[{{ user }}][{{ request.path }}]</p></body></html>'
)


@pytest.fixture
def specimen_boards(preview, tmp_path):
    """
    Two boards in a template directory of their own, searched before the project's: the route is
    exercised on boards that exist without committing one — no board exists yet, each foundation
    family writes its own. Django rebuilds the template engines when TEMPLATES changes, and again
    when it is put back.
    """
    folder = tmp_path / "board-templates" / "dev" / "designpreview" / "specimens"
    folder.mkdir(parents=True)
    for board in ("type", "chip-board"):
        (folder / f"{board}.html").write_bytes(BOARD.encode("utf-8"))
    templates = copy.deepcopy(settings.TEMPLATES)
    templates[0]["DIRS"] = [tmp_path / "board-templates", *templates[0]["DIRS"]]
    with override_settings(TEMPLATES=templates):
        yield folder


@pytest.mark.django_db
def test_a_specimen_board_is_served_sealed_in_italian_under_the_site_s_own_policy(client, specimen_boards):
    """
    ``/__design-v5/specimens/<board>/`` renders the board's template: in Italian, without the
    request's context (no user, no request in it), with the two headers of every preview page and the
    policy of the hub — the site's own, unwidened: a board frames nothing and is framed by nothing.
    """
    response = client.get(SPECIMENS + "type/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "<h1>type</h1>" in html and "/static/css/dist/main.css" in html
    assert "[][]" in html, "a board is rendered without the request's context processors"
    _assert_sealed(response)
    assert response["Content-Language"] == "it"
    csp = _csp(response)
    assert csp == _csp(client.get(HUB)), "the same policy as the other preview pages"
    assert "frame-ancestors 'none'" in csp and "frame-src" not in csp
    assert "script-src 'self'" in csp and "style-src 'self'" in csp
    assert response["X-Frame-Options"] == "DENY"
    assert client.get(SPECIMENS + "chip-board/").status_code == 200
    head = client.head(SPECIMENS + "type/")
    assert head.status_code == 200
    _assert_sealed(head)


@pytest.mark.django_db
@pytest.mark.parametrize("board", ["colour", "absent-board", "readme", "a" * 64])
def test_a_board_without_its_template_is_a_404(client, specimen_boards, board):
    assert client.get(f"{SPECIMENS}{board}/").status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("board", ["Type", "TYPE", "type_board", "-type", "type-", "ty--pe", "a" * 65])
def test_a_board_name_that_is_not_a_slug_is_a_404_even_when_its_file_exists(client, specimen_boards, board):
    """
    The name becomes a template path, so it is checked by the view as well as by the URL converter
    (which lets capitals and underscores through): the file exists, the answer is still 404. On a
    file system that ignores case, «Type» would otherwise be served from type.html.
    """
    (specimen_boards / f"{board}.html").write_bytes(BOARD.encode("utf-8"))
    assert client.get(f"{SPECIMENS}{board}/").status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["../", "%2e%2e/", "type.html/", "a.b/", "type/extra/"])
def test_what_is_not_a_board_name_never_reaches_the_view(client, specimen_boards, path):
    assert client.get(SPECIMENS + path).status_code == 404


@pytest.mark.django_db
def test_a_board_answers_get_and_head_only(client, specimen_boards):
    assert client.post(SPECIMENS + "type/").status_code == 405
    assert client.put(SPECIMENS + "type/").status_code == 405
    assert client.delete(SPECIMENS + "type/").status_code == 405


@pytest.mark.django_db
def test_a_board_reads_nothing_and_asks_for_no_transaction(client, rf, specimen_boards, django_assert_num_queries):
    """
    Not a query for a board that is served, nor in the view for one that is not. (A 404 page is the
    site's: on the way out, cms.middleware.LegacyURLMiddleware looks the path up among the legacy
    redirects, as for any unknown URL — so the view is asked directly for that half.)
    """
    from designpreview import views

    assert resolve(SPECIMENS + "type/").func._non_atomic_requests == {"default"}
    with django_assert_num_queries(0):
        assert client.get(SPECIMENS + "type/").status_code == 200
        assert client.get(SPECIMENS + "chip-board/").status_code == 200
        assert client.head(SPECIMENS + "type/").status_code == 200
        for board in ("colour", "Type", "type_board"):
            with pytest.raises(Http404):
                views.specimen(rf.get(f"{SPECIMENS}{board}/", HTTP_HOST=HOST), board=board)


def test_the_specimens_folder_holds_its_readme_and_boards_only():
    """
    templates/dev/designpreview/specimens/ — made by W1-0 with its README and no board — holds the
    README and boards whose names the route can serve: a file the route would refuse is a board nobody
    can see. The README states the contract the view keeps, in LF bytes.
    """
    from designpreview import views

    folder = TEMPLATES / "dev" / "designpreview" / "specimens"
    names = sorted(path.name for path in folder.iterdir())
    assert "README.md" in names, names
    for name in names:
        if name == "README.md":
            continue
        stem, _, suffix = name.rpartition(".")
        assert suffix == "html" and len(stem) <= 64 and views.SPECIMEN_BOARD.fullmatch(stem), name
    readme = (folder / "README.md").read_bytes()
    assert b"\r" not in readme
    text = readme.decode("utf-8")
    for promise in ("/__design-v5/specimens/<board>/", "404", "base.html", "Content-Language: it", "no-store"):
        assert promise in text, promise


# --------------------------------------------------------------------------- production untouched


@pytest.mark.django_db
def test_the_production_policy_of_a_normal_page_is_unchanged(client, preview):
    """With the preview on, a page outside it keeps the strict policy and the DENY frame option."""
    response = client.get("/fr/compte/login/")
    assert response.status_code == 200
    csp = _csp(response)
    assert "frame-ancestors 'none'" in csp
    assert "frame-src" not in csp
    assert "script-src 'self'" in csp and "style-src 'self'" in csp
    assert response["X-Frame-Options"] == "DENY"
    assert "X-Robots-Tag" not in response
    directives = settings.CONTENT_SECURITY_POLICY["DIRECTIVES"]
    assert directives["frame-ancestors"] == ("'none'",)
    assert "frame-src" not in directives


def test_the_global_policy_is_not_edited_by_the_app():
    """
    The directives the preview needs appear in the views as decorators and in the frame middleware,
    nowhere in settings: the global policy keeps ``frame-ancestors 'none'`` and
    ``upgrade-insecure-requests``; the landing and the index drop the second (review W1-P B1), and
    so does a page framed under the narrow condition.
    """
    base = (ROOT / "config" / "settings" / "base.py").read_text(encoding="utf-8")
    assert "frame-src" not in base
    assert '"frame-ancestors": ("\'none\'",)' in base
    assert '"upgrade-insecure-requests": True' in base, "production needs the directive"
    views = (ROOT / "apps" / "designpreview" / "views.py").read_text(encoding="utf-8")
    assert views.count('csp_update({"frame-src": ["\'self\'"]})') == 5, (
        "the landing, the index, the two pickers, the compare"
    )
    assert 'NO_UPGRADE = {"upgrade-insecure-requests": None}' in views
    assert views.count("@csp_replace(NO_UPGRADE)") == 2, "the landing and the index, and nothing else"
    assert views.count('csp_replace({"frame-ancestors": ["\'self\'"]})') == 1, "the proof files, and nothing else"
    # A real page is framed through the frame middleware alone, by the codebase's own pattern.
    frames = (ROOT / "apps" / "designpreview" / "frames.py").read_text(encoding="utf-8")
    assert 'RELAXED = {"frame-ancestors": ("\'self\'",), "upgrade-insecure-requests": None}' in frames
    assert "replace.update(RELAXED)" in frames and "response._csp_replace = replace" in frames
    assert 'response["X-Frame-Options"] = "SAMEORIGIN"' in frames
    for name in ("test.py", "prod.py"):
        assert "ILE_DESIGN_PREVIEW" not in (ROOT / "config" / "settings" / name).read_text(encoding="utf-8"), name


def test_the_mount_lives_inside_the_debug_guard():
    source = (ROOT / "config" / "urls.py").read_text(encoding="utf-8")
    guard = source.index("if settings.DEBUG:")
    mount = source.index('path("__design-v5/", include("designpreview.urls"))')
    assert mount > guard
    assert 'if getattr(settings, "ILE_DESIGN_PREVIEW", False):' in source
    assert "designpreview" not in source[:guard], "nothing about the preview may precede the DEBUG guard"


# --------------------------------------------------------------------------- the gate (plan §4.4)

#: Every route of the preview with the method an allowed caller uses.
ROUTES = (
    ("get", LANDING),
    ("get", INDEX),
    ("get", ARCHIVE),
    ("get", PICKER),
    ("get", TYPE),
    ("get", COMPARE),
    ("get", PROOF + "home/phase3.html"),
    ("get", SPECIMENS + "type/"),
    ("get", STATE_429),
    ("get", DECISIONS + "w1-a/CD_DECISION.md"),
    ("get", OLD_PICKER),
    ("get", OLD_PROOF + "home/phase3.html"),
    ("post", ENTER + "qa-doc-person/"),
    ("post", EXIT),
)


def _refused_callers() -> list[dict]:
    """A caller off loopback, a caller behind each proxy header, a caller naming another host."""
    from designpreview import access

    callers = [{"REMOTE_ADDR": "10.0.0.9"}, {"REMOTE_ADDR": "192.168.1.20"}]
    callers += [{header: "203.0.113.7"} for header in access.PROXY_HEADERS]
    callers += [{header: ""} for header in access.PROXY_HEADERS[:5]]  # present, even empty
    callers += [
        {"HTTP_HOST": "localhost:8781"},
        {"HTTP_HOST": "127.0.0.1:8784"},
        {"HTTP_HOST": "127.0.0.1"},
        {"HTTP_HOST": "localhost"},
        {"HTTP_HOST": "testserver"},
    ]
    return callers


@pytest.mark.django_db
@pytest.mark.parametrize(("method", "path"), ROUTES)
def test_every_route_is_a_404_off_loopback_behind_a_proxy_or_for_another_host(preview, method, path):
    """
    Plan §4.4 and §4.6. A local tunnel or a port-forward connects from loopback too: what gives it
    away is the header it adds, or the host it names. Each refusal is a plain 404 — never the
    preview's seals, never its 405, never the CSRF check's 403, never a page that names a view:
    a refused caller is never served the preview, whatever its method. Asked as the real server is
    asked, with the CSRF check enforced (review W1-P, security m1: the default test client skips it,
    and the old assertion passed only because of that).
    """
    client = Client(enforce_csrf_checks=True, HTTP_HOST=HOST)
    for caller in _refused_callers():
        for verb in {method, "post", "get", "put", "delete"}:
            response = getattr(client, verb)(path, **caller)
            assert response.status_code == 404, (path, verb, caller, response.status_code)
            _refused(response)
    # A name outside ALLOWED_HOSTS never reaches the preview at all: Django answers 400 first.
    response = client.get(path, HTTP_HOST="attacker.test:8780")
    assert response.status_code == 400 and "X-Robots-Tag" not in response


@pytest.mark.django_db
def test_the_gate_answers_the_port_of_its_own_process(client, preview):
    """``ILE_DESIGN_PREVIEW_PORT``: 8780 for the owner's server, the lane's for a lane — and only that."""
    assert client.get(LANDING).status_code == 200
    assert client.get(LANDING, HTTP_HOST="localhost:8780").status_code == 200
    with override_settings(ILE_DESIGN_PREVIEW_PORT=8784):
        assert client.get(LANDING).status_code == 404
        assert client.get(LANDING, HTTP_HOST="127.0.0.1:8784").status_code == 200
        assert client.get(LANDING, HTTP_HOST="localhost:8784").status_code == 200
        assert client.get(LANDING, HTTP_HOST="[::1]:8784").status_code in (400, 404)


@pytest.mark.django_db
def test_an_allowed_caller_meets_405_for_a_method_a_route_does_not_take(preview):
    """
    GET and HEAD for the pages; POST for the switch (plan §4.6: «405 on GET for accedi / esci») —
    with the CSRF check enforced: the routes are exempt from the middleware's check, so the method is
    answered first, and the switch checks its token itself, inside (security m1).
    """
    client = Client(enforce_csrf_checks=True, HTTP_HOST=HOST)
    for path in (LANDING, INDEX, ARCHIVE, STATE_429):
        for verb in ("post", "put", "patch", "delete"):
            response = getattr(client, verb)(path)
            assert response.status_code == 405, (path, verb)
            _assert_sealed(response)
    for path in (ENTER + "qa-doc-person/", EXIT):
        for verb in ("get", "head", "put", "patch", "delete", "options"):
            response = getattr(client, verb)(path)
            assert response.status_code == 405, (path, verb)
        assert client.get(path)["Allow"] == "POST"


# --------------------------------------------------------------------------- the landing (plan §4.1)


def _frames(html: str) -> list[str]:
    return re.findall(r"<iframe\b[^>]*>", html)


@pytest.mark.django_db
def test_the_landing_frames_the_live_home_once_under_the_strip(client, preview):
    """
    ``/__design-v5/`` opens the current best V5: the real ``/fr/`` of this server, in exactly one
    same-origin frame, under the strip. The page itself is the preview's — sealed, in Italian, never
    framed — and widens its policy by ``frame-src 'self'`` alone.
    """
    response = client.get(LANDING)
    assert response.status_code == 200
    _assert_sealed(response)
    assert response["Content-Language"] == "it"
    html = response.content.decode()
    assert '<html lang="it" dir="ltr" class="dp-live-root">' in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
    frames = _frames(html)
    assert len(frames) == 1, frames
    assert 'src="/fr/"' in frames[0] and "data-dp-frame" in frames[0]
    assert 'title="La home — V4 + fondation"' in frames[0]
    assert "<title>La home · V5 dal vivo · Italy Legal Entry™</title>" in html, "the window names the page"
    assert html.index('<header class="dp-strip"') < html.index("<iframe"), "the strip sits outside the page, above it"
    csp = _csp(response)
    assert "frame-src 'self'" in csp and "frame-ancestors 'none'" in csp
    assert "script-src 'self'" in csp and "style-src 'self'" in csp and "unsafe" not in csp
    assert "upgrade-insecure-requests" not in csp, "a frame inherits it, and its redirects then fail (B1)"
    # Never a blank frame: the stage holds the message the script shows when the frame cannot.
    assert '<div class="dp-live__message dp-live__message--blocked" role="alert" data-dp-blocked hidden>' in html
    assert "Questa pagina non si apre nella cornice." in html and "Torna alla pagina di prima" in html
    assert response["X-Frame-Options"] == "DENY", "the landing is never framed, by itself or anything else"
    # The strip: the name, the build, the state, the languages, the frame, the personas, the
    # changelog, the index, the page alone — and the way to the archive for the old anchors.
    for part in (
        'title="Italy Legal Entry™ — V5, la migliore di oggi"',
        '<span class="dp-strip__tag">v54/base</span> · <span class="dp-strip__commit">f11d131</span>',
        '<span class="dp-strip__state dp-strip__state--v4-fondation" title="V4 + fondation" data-dp-state>',
        '<span class="dp-hidden">Stato della pagina nella cornice: </span><span class="dp-strip__state-what" '
        'aria-hidden="true">pagina:</span> <span class="dp-strip__state-label" data-dp-state-label lang="fr">V4 + fondation'
        "</span>",
        '<summary class="dp-strip__summary">Personas</summary>',
        '<summary class="dp-strip__summary">Novità</summary>',
        '<p class="dp-strip__panel-title">Versione in uso</p>',
        "Cambiato dall’ultimo rapporto",
        f'href="{INDEX}">Indice</a>',
        'href="/fr/" target="_blank" rel="noopener" title="Apri la pagina da sola, in una nuova scheda" data-dp-open>'
        'Apri a parte<span class="dp-hidden"> (nuova scheda)</span></a>',
        f'data-dp-archive="{ARCHIVE}"',
        '<script id="dp-live-map" type="application/json">',
    ):
        assert part in html, part
    for code, name in (("fr", "Francese"), ("ar", "Arabo"), ("it", "Italiano"), ("en", "Inglese")):
        assert f'hreflang="{code}" title="{name}" data-dp-lang="{code}"' in html, code
        assert f'>{code}<span class="dp-hidden"> — {name.lower()}</span></a>' in html, code
    assert "Superfici V5" not in html, "no council-passed surface: no menu for them"
    assert '<p class="dp-strip__state' not in html and '<p class="dp-strip__build' not in html, "words, not paragraphs"
    assert f'href="{LANDING}?page=/ar/" hreflang="ar"' in html
    assert f'href="{LANDING}?page=/fr/&amp;frame=phone" data-dp-frame-mode="phone"' in html
    assert 'class="dp-live__stage dp-live__stage--desktop"' in html


@pytest.mark.django_db
def test_the_landing_is_clean_and_reads_nothing_without_a_session(client, preview, django_assert_num_queries):
    """
    No inline style or handler (CSP), no executable inline script — the one inline block is the
    strip's data, ``application/json`` — no forbidden wording, no id twice; and not a query: the
    landing is rendered without the request's context processors and reads the session only when a
    session cookie came.
    """
    with django_assert_num_queries(0):
        html = client.get(LANDING).content.decode()
        assert client.get(LANDING + "?page=/ar/espace-reserve/&frame=phone").status_code == 200
        assert client.get(INDEX).status_code == 200
    assert not re.search(r"<[^>]+\sstyle=", html)
    assert not re.search(r"\son[a-z]+=", html)
    scripts = re.findall(r"<script\b[^>]*>", html)
    assert scripts == [
        '<script src="/static/js/dev/designpreview.js" defer>',
        '<script id="dp-live-map" type="application/json">',
    ], scripts
    assert scan(html) == []
    ids = re.findall(r'\sid="([^"]+)"', html)
    assert len(ids) == len(set(ids)), ids
    assert "{#" not in html and "{%" not in html
    assert not re.findall(r'(?:src|href)="https?://', html)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "page",
    [
        "/ar/",
        "/it/",
        "/en/compte/login/",
        "/fr/espace-reserve/dossiers/EE167596D4/",
        "/fr/espace-reserve/mes-documents/?état=valid",
        "/documents/",
        "/documents/requirements/70d79bd5-9917-468f-abaf-6ec44669abb4/",
    ],
)
def test_the_landing_frames_a_page_of_this_site(client, preview, page):
    html = client.get(LANDING, {"page": page}).content.decode()
    frames = _frames(html)
    assert len(frames) == 1
    src = re.search(r'src="([^"]+)"', frames[0]).group(1).replace("&amp;", "&")
    assert src == page


@pytest.mark.django_db
@pytest.mark.parametrize(
    "page",
    [
        "https://attacker.test/",
        "//attacker.test/fr/",
        "javascript:alert(1)",
        "/__design-v5/",
        "/__design-v5/index/",
        "/backoffice/",
        "/static/css/dist/main.css",
        "fr/",
        "/de/",
        "/fr/\\..\\",
        "/fr/\x00",
        "/fr/ x",
        "/fr/" + "a" * 600,
        "http:/fr/",
        "/documents",
        "/api/v1/",
        "/fr/../__design-v5/",
        "/fr/%2e%2e/backoffice/",
        "/fr/./",
        "/ar/..%2f..%2fx",
        "/fr//x/",
        "/fr/.%2E/__design-v5/research/proof/index.html",
        "/documents/../backoffice/",
        "/fr/%252e%252e/",
    ],
)
def test_the_landing_never_frames_what_is_not_a_page_of_this_site(client, preview, page):
    """
    A page a frame holds is a path under /fr/, /ar/, /it/, /en/ or /documents/ of this server, with no
    dot segment and no empty one, written or percent-encoded (the URL standard reads ``%2e%2e`` as
    ``..``: review W1-P, security m3): anything else is a 400, never framed.
    """
    response = client.get(LANDING, {"page": page})
    assert response.status_code == 400
    _assert_sealed(response)
    html = response.content.decode()
    assert _frames(html) == []
    assert "La pagina chiesta non è una pagina di questo sito" in html
    assert f'<a href="{LANDING}">Torna alla home</a>' in html


@pytest.mark.django_db
@pytest.mark.parametrize(
    "page",
    ["/fr/../__design-v5/", "/fr/%2e%2e/backoffice/", "/fr/./", "/ar/..%2f..%2fx", "/ar/../__design-v5/"],
)
def test_sortir_never_frames_a_dot_segment(client, preview, accounts, this_database, page):
    """«Sortir» frames the page it came from only through ``page_param``: a dot segment is the home (security m3)."""
    client.post(ENTER + "qa-person/")
    response = client.post(EXIT, {"page": page})
    assert response["Location"] == LANDING + "?page=/fr/", page


@pytest.mark.django_db
def test_a_page_of_the_documents_app_is_framed_in_the_language_it_was_asked_for(client, preview):
    """
    The documents app has no language prefix: it answers in the language cookie's language. The
    landing frames it as it is, and ``?lang=`` sets that cookie — as LanguageCookieMiddleware does
    for a prefixed page — so that the strip's language and the page's agree (review W1-P M2).
    """
    response = client.get(LANDING, {"page": "/documents/", "lang": "ar"})
    assert response.status_code == 200
    html = response.content.decode()
    assert re.search(r'<iframe[^>]+src="/documents/"', html)
    cookie = response.cookies["ile_v5_language"]
    assert cookie.value == "ar" and cookie["httponly"] and cookie["samesite"] == "Lax"
    assert 'data-dp-lang="ar" aria-current="true"' in html
    assert f'href="{LANDING}?page=/documents/&amp;lang=fr" hreflang="fr"' in html
    assert "<title>Mes pièces — /documents/ · V5 dal vivo · Italy Legal Entry™</title>" in html
    # Without ?lang=, the cookie the browser holds decides, and the landing sets nothing.
    client.cookies["ile_v5_language"] = "ar"
    response = client.get(LANDING, {"page": "/documents/"})
    assert "ile_v5_language" not in response.cookies
    assert 'data-dp-lang="ar" aria-current="true"' in response.content.decode()
    # A prefixed page never carries ?lang=: its prefix is its language, and the landing sets nothing.
    response = client.get(LANDING, {"page": "/fr/le-projet/", "lang": "ar"})
    strip = response.content.decode().split('<script id="dp-live-map"')[0]
    assert "ile_v5_language" not in response.cookies
    assert "&amp;lang=" not in strip and "?lang=" not in strip


@pytest.mark.django_db
def test_the_phone_frame_is_a_class_and_an_unknown_frame_is_the_window(client, preview):
    html = client.get(LANDING, {"frame": "phone"}).content.decode()
    assert 'class="dp-live__stage dp-live__stage--phone"' in html
    assert 'data-dp-frame-mode="phone" aria-current="true"' in html
    html = client.get(LANDING, {"frame": "tablet"}).content.decode()
    assert 'class="dp-live__stage dp-live__stage--desktop"' in html
    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    phone = _declarations(css, ".dp-live__stage--phone .dp-live__frame")
    assert "inline-size: calc(390px + 2px)" in phone and "block-size: min(844px, 100%)" in phone


@pytest.mark.django_db
def test_the_strip_offers_it_and_en_for_the_home_and_the_login_and_fr_and_ar_everywhere(client, preview):
    def offered(page: str) -> list[str]:
        html = client.get(LANDING, {"page": page}).content.decode()
        strip = html[html.index('<nav class="dp-strip__group dp-strip__group--lang') :]
        strip = strip[: strip.index("</nav>")]
        return re.findall(r'data-dp-lang="([a-z]{2})"', strip)

    assert offered("/fr/") == ["fr", "ar", "it", "en"]
    assert offered("/it/compte/login/") == ["fr", "ar", "it", "en"]
    assert offered("/fr/le-projet/") == ["fr", "ar"]
    assert offered("/ar/espace-reserve/") == ["fr", "ar"]
    assert offered("/fr/une-page-inconnue/") == ["fr", "ar"]
    html = client.get(LANDING, {"page": "/ar/le-projet/"}).content.decode()
    assert f'href="{LANDING}?page=/fr/le-projet/" hreflang="fr"' in html
    assert 'data-dp-lang="ar" aria-current="true"' in html


@pytest.mark.django_db
def test_the_strip_says_v5_only_where_the_steward_s_live_status_says_so(client, preview, tmp_path):
    """
    «V4 + fondation» wherever the steward has not written «v5» for a surface — when the file is
    absent, unreadable, or silent about the page — and «V5 — council-passed» where it has; the
    council-passed surfaces are the strip's quick links, and nothing else is.
    """

    def state(page: str) -> str:
        html = client.get(LANDING, {"page": page}).content.decode()
        return re.search(r'data-dp-state-label(?: lang="fr")?>([^<]+)</span>', html).group(1)

    assert state("/fr/") == "V4 + fondation"
    _steward(tmp_path, "live_status.json", "{not json")
    assert state("/fr/") == "V4 + fondation"
    _steward(tmp_path, "live_status.json", json.dumps(["v5"]))
    assert state("/fr/") == "V4 + fondation"
    _steward(
        tmp_path,
        "live_status.json",
        json.dumps({"surfaces": {"home": "v5", "login": {"state": "v5"}, "faq": "V5", "news": "passed"}}),
    )
    assert state("/fr/") == "V5 — council-passed"
    assert state("/ar/") == "V5 — council-passed"
    assert state("/en/compte/login/") == "V5 — council-passed"
    assert state("/fr/faq/") == "V4 + fondation", "a state is the word «v5», nothing like it"
    assert state("/fr/actualites/") == "V4 + fondation"
    assert state("/fr/le-projet/") == "V4 + fondation"
    html = client.get(LANDING).content.decode()
    # One menu, «Superfici V5 · n», never a row of links (review W1-P M5) — and the same list again
    # in «Altro», which holds what the row does not below 80 rem.
    menu = html[html.index('<details class="dp-strip__menu dp-strip__menu--quick dp-strip__wide">') :]
    menu = menu[: menu.index("</details>")]
    assert (
        '<summary class="dp-strip__summary">Superfici V5<span class="dp-hidden">:</span> '
        '<span class="dp-strip__count">2</span><span class="dp-hidden"> pagine</span></summary>'
    ) in menu, "«Superfici V5: 2 pagine» for assistive technology, the pill for the eye (a11y r2 n4)"
    assert re.findall(r'<li><a href="[^"]+">([^<]+)</a></li>', menu) == ["La home", "L’accesso «Il varco»"]
    assert f'<li><a href="{LANDING}?page=/fr/compte/login/">' in menu
    altro = html[html.index('<details class="dp-strip__menu dp-strip__narrow">') :]
    assert "Superfici V5 — hanno passato il consiglio" in altro[: altro.index("</details>")]
    assert "dp-strip__state--v5" in html
    # The page's data block carries the same states, for the script that follows the frame.
    data = json.loads(re.search(r'<script id="dp-live-map" type="application/json">(.*?)</script>', html).group(1))
    assert data["pages"]["/fr/"] == ["v5", "fr ar it en", "La home"]
    assert data["pages"]["/fr/faq/"][0] == "v4-fondation" and data["pages"]["/fr/le-projet/"][1] == "fr ar"
    assert data["labels"] == {"v5": "V5 — council-passed", "v4-fondation": "V4 + fondation"}
    assert data["fallback"] == "v4-fondation" and data["archive"] == ARCHIVE and data["landing"] == LANDING
    assert data["follow"] == "^/(?:it|fr|en|ar|documents)/" and data["persona"] == ""


@pytest.mark.django_db
def test_the_strip_carries_three_lines_of_the_steward_s_changelog_on_demand(client, preview, tmp_path):
    html = client.get(LANDING).content.decode()
    assert "Ancora nessuna novità registrata." in html, "plain words; the path is the line's title (m1)"
    assert "CHANGELOG_V54.md" not in re.sub(r'title="[^"]*"', "", html)
    _steward(
        tmp_path,
        "CHANGELOG_V54.md",
        "# Changelog V5.4\n\n## v54/w1-a — 6 October 2026\n\n- The foundation: **Host Grotesk**, `Vazirmatn`.\n"
        "- Lo spigolo: 2 · 4 · 6 · 8 · 12.\n* «En examen» in lapis.\n- A fourth line.\n- A fifth.\n",
    )
    html = client.get(LANDING).content.decode()
    news = html[html.index('<ul class="dp-strip__news" role="list">') :]
    news = news[: news.index("</ul>")]
    assert re.findall(r"<li>([^<]+)</li>", news) == [
        "The foundation: Host Grotesk, Vazirmatn.",
        "Lo spigolo: 2 · 4 · 6 · 8 · 12.",
        "«En examen» in lapis.",
    ]
    assert "A fourth line." not in html
    # Opened on demand: inside a <details>, never open by default.
    assert "<details open" not in html and " open>" not in html
    _steward(tmp_path, "CHANGELOG_V54.md", "# Changelog V5.4\n\nNothing yet.\n")
    assert "Ancora nessuna novità registrata." in client.get(LANDING).content.decode()


@pytest.mark.django_db
def test_the_strip_names_the_build_this_server_is_checked_out_at(client, preview, monkeypatch):
    from designpreview import live

    html = client.get(LANDING).content.decode()
    assert '<time datetime="2026-10-05">5 ottobre 2026</time>' in html, "the date, in the menus, in words (UX r2 n8)"
    monkeypatch.setattr(live, "identity", lambda: {"tag": "", "branch": "v54-w1-p", "commit": "1a2b3c4", "date": ""})
    html = client.get(LANDING).content.decode()
    assert '<span class="dp-strip__tag">ramo v54-w1-p</span> · <span class="dp-strip__commit">1a2b3c4</span>' in html
    monkeypatch.setattr(live, "identity", lambda: {"tag": "", "branch": "", "commit": "", "date": ""})
    assert '<span class="dp-strip__tag">versione sconosciuta</span>' in client.get(LANDING).content.decode()


def test_the_build_is_read_from_git_once_per_process(monkeypatch):
    """The tag (v5-live's, on 8780), the commit and the date — from git, at most five seconds a question, cached."""
    from designpreview import live

    asked: list[tuple[str, ...]] = []

    def git(*args):
        asked.append(args)
        return {
            ("describe", "--tags", "--exact-match", "HEAD"): "v54/w1-a",
            ("log", "-1", "--format=%h%x09%cs"): "abc1234\t2026-10-06",
        }.get(args, "")

    monkeypatch.setattr(live, "_git", git)
    live.identity.cache_clear()
    try:
        assert live.identity() == {"tag": "v54/w1-a", "branch": "", "commit": "abc1234", "date": "2026-10-06"}
        live.identity()
        assert len(asked) == 2, "asked once per process: 8780 is restarted after every checkout"
    finally:
        live.identity.cache_clear()
    source = (ROOT / "apps" / "designpreview" / "live.py").read_text(encoding="utf-8")
    assert "timeout=5" in source and "shell=" not in source


def test_the_landing_sends_an_old_anchor_of_the_hub_to_the_archive():
    """
    Before V5.4 the hub was ``/__design-v5/`` and its groups were anchors (``#g-he``). A fragment
    never reaches the server, so the landing's script sends a link to one of them on to the
    archive, which holds the anchor now — and leaves every other fragment alone.
    """
    js = (STATIC / "js" / "dev" / "designpreview.js").read_text(encoding="utf-8")
    assert "/^#g-[a-z0-9-]+$/.test(window.location.hash)" in js
    assert 'window.location.replace(strip.getAttribute("data-dp-archive") + window.location.hash);' in js
    hub = (TEMPLATES / "dev" / "designpreview" / "hub.html").read_text(encoding="utf-8")
    assert '<li class="dp-group" id="g-{{ group.key }}">' in hub, "the anchors the old links name are still there"


# --------------------------------------------------------------------------- the index (plan §4.1)


@pytest.mark.django_db
def test_the_index_lists_every_public_page_in_fr_and_ar_with_its_frames_and_its_v4_twin(client, preview):
    """
    One row per public page: the real URLs in fr and ar — it and en as well for the home and the
    login — each opened in the landing's frame, each with «Desktop 1440» and «Telefono 390» (frames
    the script makes on demand; without it, the landing) and the same URL on the V4 control, 8771 —
    never on this server. No frame is in the markup.
    """
    from designpreview import live

    response = client.get(INDEX)
    assert response.status_code == 200
    _assert_sealed(response)
    html = response.content.decode()
    assert _frames(html) == []
    assert "frame-src 'self'" in _csp(response) and response["X-Frame-Options"] == "DENY"
    rows = re.findall(r'<li class="dp-row" id="p-([a-z0-9-]+)">', html)
    assert rows == [page.slug for page in live.PUBLIC_PAGES], rows
    assert len(rows) >= 40
    for page in live.PUBLIC_PAGES:
        row = html[html.index(f'<li class="dp-row" id="p-{page.slug}">') :]
        row = row[: row.index("</ul>")]
        langs = ("fr", "ar", "it", "en") if page.slug in {"home", "login"} else ("fr", "ar")
        assert re.findall(r'class="dp-row__page" href="[^"]+" hreflang="([a-z]{2})"', row) == list(langs), page.slug
        for lang in langs:
            url = live.url_of(page, lang)
            assert url.startswith(f"/{lang}/"), (page.slug, url)
            landing = live.landing_url(url).replace("&", "&amp;")
            phone = live.landing_url(url, "phone").replace("&", "&amp;")
            assert f'href="{landing}" hreflang="{lang}"' in row, (page.slug, lang)
            assert f'href="{landing}" data-dp-pair="{url}" data-dp-kind="desktop"' in row
            assert f'href="{phone}" data-dp-pair="{url}" data-dp-kind="phone"' in row
            assert f'href="http://127.0.0.1:8771{url}" target="_blank" rel="noopener"' in row
            assert "(nuova scheda)</span></a>" in row, "a new tab says so (a11y m7)"
    assert ":8780" not in html, "V4 is compared on 8771, never on the server that serves V5"


@pytest.mark.django_db
def test_the_index_groups_the_v4_fondation_pages_apart_open_until_one_passes(client, preview, tmp_path):
    """
    «V4 + fondation» pages stand apart (plan §4.1) — open while nothing has passed, so that every
    public page is one click from the index; collapsed once a page has passed (review W1-P M4). The
    fold says it opens: the strip's chevron, turning when it is open.
    """
    from designpreview import live

    html = client.get(INDEX).content.decode()
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    assert "Nessuna pagina pubblica ha ancora passato il consiglio: tutte sono qui sotto." in public
    assert '<details class="dp-index__fold" open>' in public, "open while nothing has passed"
    fold = public[public.index('<details class="dp-index__fold" open>') :]
    assert f"{len(live.PUBLIC_PAGES)} pagine pubbliche" in fold
    assert '<li class="dp-row" id="p-home">' in fold
    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    chevron = _declarations(css, ".dp-index__summary::after")
    assert "border-inline-end: 1.5px solid currentColor" in chevron and "rotate(45deg)" in chevron
    assert "rotate(225deg)" in _declarations(css, ".dp-index__fold[open] > .dp-index__summary::after")
    assert "list-style: none" in _declarations(css, ".dp-index__summary")
    _steward(tmp_path, "live_status.json", json.dumps({"surfaces": {"home": "v5"}}))
    html = client.get(INDEX).content.decode()
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    passed, fold = public.split('<details class="dp-index__fold">', 1)
    assert '<li class="dp-row" id="p-home">' in passed and '<li class="dp-row" id="p-home">' not in fold
    assert '<span class="dp-state dp-state--v5">V5 — council-passed</span>' in passed
    assert "Nessuna pagina pubblica ha ancora passato il consiglio." not in public


@pytest.mark.django_db
def test_the_index_offers_the_four_personas_and_never_a_staff_one(client, preview):
    """
    Four cards (plan §4.1): «Personne avec dossier» (qa-doc-person, EE167596D4), «Personne,
    conditions non acceptées» (qa-person), «Personne sans dossier» (qa-fresh-person), «Entreprise —
    Cantiere Adriatico» (qa-company); each with «Entrer» — a POST with its CSRF token — and its pages
    in fr and ar. A staff persona is never offered.
    """
    html = client.get(INDEX).content.decode()
    cards = html[html.index('id="personas"') : html.index('id="stati"')]
    assert re.findall(r'<h3 class="dp-card__name" lang="fr">([^<]+)</h3>', cards) == [
        "Personne avec dossier",
        "Personne, conditions non acceptées",
        "Personne sans dossier",
        "Entreprise — Cantiere Adriatico",
    ]
    for key in ("qa-doc-person", "qa-person", "qa-fresh-person", "qa-company"):
        form = cards[cards.index(f'action="{ENTER}{key}/"') - 60 :]
        form = form[: form.index("</form>")]
        assert 'method="post"' in form and 'name="csrfmiddlewaretoken"' in form, key
        assert '><span lang="fr">Entrer</span><span class="dp-hidden">' in form
    assert "qa-admin" not in html and "is_staff" not in html
    assert "fascicolo <code>EE167596D4</code>" in cards and "fascicolo <code>E46E03B461</code>" in cards
    assert '<span class="dp-card__opens">apre il suo <span lang="fr">Tableau de bord</span></span>' in cards
    assert '<span class="dp-card__opens">apre il suo <span lang="fr">Espace entreprise</span></span>' in cards
    # Nobody is inside: each page of a persona is a POST that enters it and opens that page (M3).
    for page in ("/fr/espace-reserve/", "/ar/espace-reserve/", "/fr/espace-reserve/dossiers/EE167596D4/"):
        assert f'<input type="hidden" name="page" value="{page}">' in cards, page
        assert f'href="{LANDING}?page={page}"' not in cards, "a link would meet the login"
    assert '<input type="hidden" name="page" value="/fr/espace-reserve/entreprise/mes-besoins/">' in cards
    assert 'Analyse territoriale</span> <span class="dp-card__aside">— 403 per questa impresa' in cards
    # The page types only a role account reaches stand apart, said once.
    assert "<strong>Fuori dall’anteprima</strong> — nessuna persona per questi ruoli:" in cards
    # The strip's menu holds the same four, and the database this server uses is said when a persona
    # would be refused on it.
    strip = html[html.index('<header class="dp-strip"') : html.index("</header>")]
    for key in ("qa-doc-person", "qa-person", "qa-fresh-person", "qa-company"):
        assert f'action="{ENTER}{key}/"' in strip
    assert "qui le personas sono rifiutate" in html


@pytest.mark.django_db
def test_the_index_draws_the_families_from_the_steward_s_live_status(client, preview, tmp_path):
    html = client.get(INDEX).content.decode()
    assert (
        'Nessuna superficie ha ancora passato il consiglio: per ora ogni pagina è «<span lang="fr">V4 + fondation</span>».'
        in html
    )
    assert "Nessuna famiglia ha ancora passato il consiglio." in html
    _steward(
        tmp_path,
        "live_status.json",
        json.dumps(
            {
                "schema": "ile-live-status-v54/1",
                "updated": "2026-10-06",
                "families": [
                    {
                        "key": "w1-a",
                        "title": "Fondazione",
                        "state": "v5",
                        "scores": {
                            "visual": 4,
                            "premium": 4.5,
                            "originality": 4,
                            "ux": 4,
                            "mobile": 4,
                            "coherence": 4,
                            "secret": 9,
                            "taste": True,
                        },
                        "decision": "w1-a/CD_DECISION.md",
                        "tag": "v54/w1-a",
                        "date": "2026-10-06",
                    },
                    {"key": "w1-b", "title": "Icone", "state": "v4-fondation"},
                    {"title": "no key"},
                    "not an object",
                ],
            }
        ),
    )
    html = client.get(INDEX).content.decode()
    board = html[html.index('id="famiglie"') : html.index('id="fondazione"')]
    passed, fold = board.split('<details class="dp-index__fold">', 1)
    assert "<code>w1-a</code> Fondazione" in passed and "<code>w1-b</code>" in fold
    assert re.findall(r'<span class="dp-family__score">([^<]+)</span>', passed) == [
        "visivo 4",
        "premium 4,5",  # in Italian, as the index is
        "originalità 4",
        "UX 4",
        "telefono 4",
        "coerenza 4",
    ]
    assert f'<a href="{DECISIONS}w1-a/CD_DECISION.md">la decisione del CD</a>' in passed
    assert "<code>v54/w1-a</code>" in passed and '<time datetime="2026-10-06">' in passed
    assert "no key" not in board
    assert 'Aggiornato il <time datetime="2026-10-06">' in board
    _steward(tmp_path, "live_status.json", "\x00garbage")
    assert (
        'Il registro dello stato è illeggibile: per ora ogni pagina è «<span lang="fr">V4 + fondation</span>».'
        in client.get(INDEX).content.decode()
    )


@pytest.mark.django_db
def test_a_cd_decision_is_served_as_text_from_the_family_s_qa_folder_and_nothing_else(client, preview, tmp_path):
    """The link of the status board: a Markdown file under docs/design-v5/QA/v54/, by the proof server's resolver."""
    root = tmp_path / "qa-v54"
    (root / "w1-a").mkdir(parents=True)
    (root / "w1-a" / "CD_DECISION.md").write_bytes(b"# Decisione\n\nPassa.\n")
    (root / "w1-a" / "scores.json").write_bytes(b"{}")
    (root / "w1-a" / ".work").mkdir()
    (root / "w1-a" / ".work" / "notes.md").write_bytes(b"never served\n")
    (tmp_path / "outside.md").write_bytes(b"never served\n")
    from designpreview import views

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(views, "_decisions_root", lambda: root)
        response = client.get(DECISIONS + "w1-a/CD_DECISION.md")
        assert response.status_code == 200 and response["Content-Type"] == "text/plain; charset=utf-8"
        assert b"".join(response.streaming_content) == b"# Decisione\n\nPassa.\n"
        _assert_sealed(response)
        for refused in (
            "w1-a/scores.json",
            "w1-a/.work/notes.md",
            "w1-a/../../outside.md",
            "w1-a/%2e%2e/%2e%2e/outside.md",
            "w1-a/",
            "W1-A~1/CD_DECISION.md",
            "C:/x.md",
            "w1-a/missing.md",
        ):
            response = client.get(DECISIONS + refused)
            assert response.status_code == 404, refused
            assert b"never served" not in response.content


#: W1-0's census — the before set of V5.4, 79 page types (C:/tmp/ile_v5_council/evidence/v54/w1-0/
#: before/PAGE_TYPES.json): id → (the persona it was captured with, its French URL). Copied here so
#: that the index is held to it where the evidence folder does not exist; the next test compares the
#: copy with the file wherever the file is.
CENSUS_TYPES = {
    "home": (None, "/fr/"),
    "navbar-open": (None, "/fr/"),
    "door-persons": (None, "/fr/parcours/"),
    "door-companies": (None, "/fr/entreprises/"),
    "door-institutions": (None, "/fr/institutions/"),
    "door-universities": (None, "/fr/universites-et-formation/"),
    "door-forum": (None, "/fr/forum/"),
    "project": (None, "/fr/le-projet/"),
    "project-pilot": (None, "/fr/projet-pilote/"),
    "project-agami": (None, "/fr/agami/"),
    "project-network": (None, "/fr/reseau/"),
    "antifraud": (None, "/fr/attention-aux-fraudes/"),
    "orientation-start": (None, "/fr/orientation/"),
    "orientation-step": (None, "/fr/orientation/"),
    "orientation-resume": (None, "/fr/orientation/reprendre/"),
    "pathway-detail": (None, "/fr/parcours/salaried_work/"),
    "diplomas": (None, "/fr/diplomes-et-titres/"),
    "training": (None, "/fr/formation/"),
    "living-index": (None, "/fr/vivre-en-italie/"),
    "living-topic": (None, "/fr/vivre-en-italie/logement/"),
    "news-index": (None, "/fr/actualites/"),
    "faq": (None, "/fr/faq/"),
    "glossary-index": (None, "/fr/glossaire/"),
    "glossary-term": (None, "/fr/glossaire/permesso_di_soggiorno/"),
    "partners": (None, "/fr/partenaires/"),
    "contact": (None, "/fr/contact/"),
    "contact-form": (None, "/fr/contact/formulaire/"),
    "enquiry-company-needs": (None, "/fr/entreprises/recueil-des-besoins/"),
    "enquiry-collaboration": (None, "/fr/collaboration/institutions/"),
    "enquiry-done": (None, "/fr/demande-transmise/?k=contact"),
    "forum-register": (None, "/fr/forum/inscription/"),
    "legal-document": (None, "/fr/privacy-policy/"),
    "login": (None, "/fr/compte/login/"),
    "signup": (None, "/fr/compte/signup/"),
    "password-reset": (None, "/fr/compte/password/reset/"),
    "password-reset-done": (None, "/fr/compte/password/reset/done/"),
    "email-verification-sent": (None, "/fr/compte/confirm-email/"),
    "error-404": (None, "/fr/page-inexistante/"),
    "error-410": (None, "/wp-login.php"),
    "error-403": ("qa-company", "/fr/espace-reserve/entreprise/analyse-territoriale/"),
    "console-unavailable": ("demo-professionnel", "/fr/espace-reserve/forum-permanent/"),
    "account-profile": ("qa-doc-person", "/fr/compte/profil/"),
    "account-email": ("qa-doc-person", "/fr/compte/email/"),
    "account-password-change": ("qa-doc-person", "/fr/compte/password/change/"),
    "account-mfa": ("qa-doc-person", "/fr/compte/2fa/"),
    "account-delete": ("qa-doc-person", "/fr/compte/profil/suppression/"),
    "logout-confirm": ("qa-doc-person", "/fr/compte/logout/"),
    "dashboard-person": ("qa-doc-person", "/fr/espace-reserve/"),
    "dashboard-person-terms-pending": ("qa-person", "/fr/espace-reserve/"),
    "dashboard-person-empty": ("qa-fresh-person", "/fr/espace-reserve/"),
    "situation": ("qa-doc-person", "/fr/espace-reserve/ma-situation/"),
    "journey": ("qa-doc-person", "/fr/espace-reserve/mon-parcours/"),
    "journey-results": ("qa-person", "/fr/espace-reserve/mon-parcours/"),
    "documents": ("qa-doc-person", "/documents/"),
    "documents-portal": ("qa-doc-person", "/fr/espace-reserve/mes-documents/"),
    "document-upload": ("qa-doc-person", "/documents/upload/"),
    "document-upload-terms-required": ("qa-person", "/documents/upload/"),
    "document-requirement": ("qa-doc-person", "/documents/requirements/70d79bd5-9917-468f-abaf-6ec44669abb4/"),
    "requests": ("qa-person", "/fr/espace-reserve/mes-demandes/"),
    "request-detail": ("qa-person", "/fr/espace-reserve/mes-demandes/contact/1/"),
    "messages": ("qa-doc-person", "/fr/espace-reserve/communications/"),
    "deadlines": ("qa-doc-person", "/fr/espace-reserve/mes-echeances/"),
    "cases-index": ("qa-doc-person", "/fr/espace-reserve/dossiers/"),
    "case-file": ("qa-doc-person", "/fr/espace-reserve/dossiers/EE167596D4/"),
    "helpdesk": ("qa-person", "/fr/espace-reserve/guichet/"),
    "helpdesk-detail": ("qa-person", "/fr/espace-reserve/guichet/4262f0d4-1396-4f63-a690-a2b8e9c27ad4/"),
    "helpdesk-new": ("qa-person", "/fr/espace-reserve/guichet/nouvelle-demande/"),
    "academy-catalogue": ("qa-doc-person", "/fr/espace-reserve/formation/"),
    "academy-course": ("qa-doc-person", "/fr/espace-reserve/formation/cours/italien-a1/"),
    "academy-mine": ("qa-person", "/fr/espace-reserve/formation/mes-formations/"),
    "academy-enrolment": (
        "qa-person",
        "/fr/espace-reserve/formation/mes-formations/32589170-cc35-4fda-984f-edabf4d3f30f/",
    ),
    "company-dashboard": ("qa-company", "/fr/espace-reserve/entreprise/"),
    "company-profile": ("qa-company", "/fr/espace-reserve/entreprise/mon-entreprise/"),
    "company-needs": ("qa-company", "/fr/espace-reserve/entreprise/mes-besoins/"),
    "company-need-form": ("qa-company", "/fr/espace-reserve/entreprise/mes-besoins/nouveau/"),
    "org-bridge": ("qa-company", "/fr/espace-reserve/"),
    "helpdesk-queue": ("demo-professionnel", "/fr/espace-reserve/guichet/confiees/"),
    "helpdesk-dispatch": ("demo-operateur", "/fr/espace-reserve/guichet/designation/"),
    "selection-workspace": ("demo-acteur-autorise", "/fr/espace-reserve/selection/"),
}
CENSUS_FILE = Path("C:/tmp/ile_v5_council/evidence/v54/w1-0/before/PAGE_TYPES.json")


def _cards(html: str) -> dict[str, str]:
    """The index's persona cards, by persona key."""
    section = html[html.index('id="personas"') : html.index('id="stati"')]
    cards = {}
    for chunk in re.split(r'<li class="dp-card(?: dp-card--active)?">', section)[1:]:
        key = re.search(r"<code>(qa-[a-z-]+)</code>", chunk).group(1)
        cards[key] = chunk
    return cards


@pytest.mark.django_db
def test_the_index_covers_every_page_type_of_w1_0_s_census(client, preview):
    """
    Review W1-P M2: the index exposed 47 of the census's 79 page types. Every one has its place now —
    a public row, a page on the card of the persona the census captured it with, a state without
    credentials, or «fuori dall'anteprima» for the four that only a role account reaches — and every
    surface key the steward may mark is a census id.
    """
    from designpreview import live

    html = client.get(INDEX).content.decode()
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    states = html[html.index('id="stati"') : html.index('id="famiglie"')]
    cards = _cards(html)
    outside = {key: title for key, title, _role in live.OUTSIDE}
    state_only = {
        "navbar-open": f'<a href="{LANDING}">Nella cornice</a>',
        "orientation-step": f'<a href="{LANDING}?page=/fr/orientation/">Nella cornice</a>',
        "error-404": f'<a href="{STATE_404}?lang=fr" hreflang="fr" target="_blank" rel="noopener">fr',
        "error-410": '<a href="/wp-login.php" target="_blank" rel="noopener">',
    }
    for key, (persona, url) in CENSUS_TYPES.items():
        if key in outside:
            assert outside[key] in html, key
        elif key in state_only:
            assert state_only[key] in states, key
        elif persona is None:
            assert f'href="{live.landing_url(url).replace("&", "&amp;")}" hreflang="fr"' in public, (key, url)
        else:
            assert f'<input type="hidden" name="page" value="{url}">' in cards[persona], (key, persona, url)
    keys = set(live.surface_keys())
    assert set(CENSUS_TYPES) - set(outside) <= keys, sorted(set(CENSUS_TYPES) - set(outside) - keys)
    assert keys - set(CENSUS_TYPES) == {"community"}, "every key is a census id, but the closed virtual forum"


def test_the_census_the_index_mirrors_is_w1_0_s():
    """The copy above is W1-0's census, page type for page type — where the evidence folder is on disk."""
    if not CENSUS_FILE.exists():
        pytest.skip(f"no census at {CENSUS_FILE}")
    data = json.loads(CENSUS_FILE.read_bytes().decode("utf-8"))
    assert {item["id"]: (item["persona"], item["url"]["fr"]) for item in data["page_types"]} == CENSUS_TYPES
    assert data["count"] == len(CENSUS_TYPES) == 79


@pytest.mark.django_db
def test_a_persona_s_pages_are_links_once_it_is_inside_and_forms_for_the_others(
    client, preview, accounts, this_database
):
    """
    Review W1-P M3: before «Entrer» a persona's page link met the login; under another persona it met
    that persona's view. Now a page of the persona inside is a link, framed at once, and a page of
    any other persona is a POST that enters that persona and opens that page, in that language.
    """
    client.post(ENTER + "qa-doc-person/")
    cards = _cards(client.get(INDEX).content.decode())
    inside, other = cards["qa-doc-person"], cards["qa-company"]
    assert f'<a class="dp-card__link" href="{LANDING}?page=/ar/espace-reserve/mes-echeances/" hreflang="ar">' in inside
    assert '<input type="hidden" name="page" value="/fr/espace-reserve/mes-echeances/">' not in inside
    assert f'<a class="dp-card__link" href="{LANDING}?page=/documents/&amp;lang=ar" hreflang="ar">' in inside
    assert '<span class="dp-card__state">dentro</span>' in inside
    assert '<input type="hidden" name="page" value="/ar/espace-reserve/entreprise/">' in other
    assert '<input type="hidden" name="lang" value="ar">' in other
    assert f'href="{LANDING}?page=/fr/espace-reserve/entreprise/"' not in other


@pytest.mark.django_db
def test_the_index_lists_the_foundation_s_specimen_boards(client, specimen_boards):
    html = client.get(INDEX).content.decode()
    boards = html[html.index('id="fondazione"') : html.index('id="v4"')]
    assert f'<a href="{SPECIMENS}type/">Il campione tipografico</a>' in boards
    # The icon board landed with W1-B (templates/dev/designpreview/specimens/icons.html): the index links a board
    # the moment its template exists, so «Il foglio delle icone» is a link, no longer «non ancora».
    assert f'<a href="{SPECIMENS}icons/">Il foglio delle icone</a>' in boards
    # W1-D's board landed on 8 October 2026: linked the moment its template exists (live.specimen_boards).
    assert f'<a href="{SPECIMENS}loader/">Le sequenze del caricatore</a>' in boards
    for title in ("La tavola dei registri di colore",):
        assert f'<span class="dp-boards__missing">{title} · non ancora</span>' in boards, title


@pytest.mark.django_db
@pytest.mark.parametrize(
    "origin",
    ["http://127.0.0.1:8780", "http://localhost:8780", "https://127.0.0.1:8771", "http://example.test:8771", ""],
)
def test_v4_is_never_compared_on_this_server_nor_off_this_machine(client, preview, origin):
    with override_settings(ILE_DESIGN_PREVIEW_V4_ORIGIN=origin):
        html = client.get(INDEX).content.decode()
    assert "dp-row__v4" not in html
    assert "Nessun server di controllo V4 configurato" in html


@pytest.mark.django_db
def test_the_states_without_credentials_are_reachable(client, preview):
    """
    Plan §4.5: the engage on the login (the page alone — its error is the answer to a POST, which no
    frame may show), the release (Entrer), the stage's states (the login, framed) and the 429 page —
    through the preview's own state route, the site's own template with its status — beside the
    DEBUG error pages.
    """
    html = client.get(INDEX).content.decode()
    states = html[html.index('id="stati"') : html.index('id="famiglie"')]
    assert (
        f'<a href="{LANDING}?page=/fr/compte/login/">Nella cornice</a> · <a href="/fr/compte/login/" '
        'target="_blank" rel="noopener">l’accesso da solo<span class="dp-hidden"> (nuova scheda)</span></a>'
    ) in states, "a form's answer is framed now (DL54-17): the engage plays in the frame too"
    assert "(senza inviare)" in states
    assert f'<a href="{LANDING}?page=/fr/orientation/">Nella cornice</a>' in states, "a step of the questionnaire"
    assert f'<a href="{STATE_404}?lang=fr" hreflang="fr" target="_blank" rel="noopener">fr' in states, "the 404 (C1)"
    assert '<a href="/wp-login.php" target="_blank" rel="noopener">' in states, "the 410"
    assert f'<a href="{STATE_429}" target="_blank" rel="noopener">' in states
    for code in ("400", "403", "404", "500"):
        assert (
            f'<a href="/_errors/{code}/" target="_blank" rel="noopener">{code}<span class="dp-hidden"> (nuova scheda)'
            "</span></a>"
        ) in states
    for jargon in ("L’ingaggio", "Il rilascio", "Gli stati del palco", "marchio della colonna"):
        assert jargon not in states, jargon
    response = client.get(STATE_429)
    assert response.status_code == 429
    _assert_sealed(response)
    assert b"429" in response.content or b"Trop" in response.content
    assert client.get("/__design-v5/stati/418/").status_code == 404
    assert client.head(STATE_429).status_code == 429


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("lang", "title", "direction"), [("fr", "Page introuvable", "ltr"), ("ar", "الصفحة غير موجودة", "rtl")]
)
def test_the_index_s_404_is_the_product_s_own_in_fr_and_in_ar(client, preview, lang, title, direction):
    """
    Review W1-P, UX r2 n1 (CD condition C1): «La 404» framed Django's technical page — the preview
    runs with DEBUG on, and under DEBUG an address that matches nothing gets it, in English, listing
    the URL patterns. The index links the product's own 404, through the preview's state route, in
    fr and in ar; the closed virtual forum's row says what a frame shows there.
    """
    html = client.get(INDEX).content.decode()
    states = html[html.index('id="stati"') : html.index('id="famiglie"')]
    link = f"{STATE_404}?lang={lang}"
    assert f'<a href="{link}" hreflang="{lang}" target="_blank" rel="noopener">{lang}<span class="dp-hidden">' in states
    assert "page-inexistante" not in states, "never Django's technical page"
    response = client.get(link)
    assert response.status_code == 404
    _assert_sealed(response)
    assert "errors/404.html" in [template.name for template in response.templates]
    assert response["Content-Language"] == lang
    page = response.content.decode()
    assert f'<html lang="{lang}" dir="{direction}"' in page and title in page
    assert "Page not found" not in page and "URLconf" not in page
    assert client.head(link).status_code == 404
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    assert "404 finché il forum virtuale è chiuso (in sviluppo: la pagina tecnica di Django)" in public


@pytest.mark.django_db
def test_the_states_a_later_family_builds_say_in_arrivo_until_it_has_passed(client, preview, tmp_path):
    """
    Review W1-P, UX r2 n4 (CD condition C2): the index described the engage, the release and the
    stage's answers as facts, and none is built yet — W1-D builds the loader and the release, W2-B
    wires the engage and the stage. Each says «in arrivo» with the families it waits for, until
    every one of them is "v5" in live_status.json: never a promise worded as a fact.
    """

    def notes() -> list[str]:
        html = client.get(INDEX).content.decode()
        states = html[html.index('id="stati"') : html.index('id="famiglie"')]
        return re.findall(r'<span class="dp-states__coming">([^<]+)</span>', states)

    lume, varco = "W1-D (il caricatore «Lume»)", "W2-B (l’accesso «Il varco»)"
    tail = ": oggi la pagina non lo mostra ancora."
    assert notes() == [
        f"— in arrivo con {lume} e {varco}{tail}",
        f"— in arrivo con {lume}{tail}",
        f"— in arrivo con {varco}{tail}",
    ], "without the file"
    _steward(tmp_path, "live_status.json", json.dumps({"families": [{"key": "w1-d", "state": "v5"}]}))
    assert notes() == [f"— in arrivo con {varco}{tail}", f"— in arrivo con {varco}{tail}"], "W1-D at «v5»"
    _steward(
        tmp_path,
        "live_status.json",
        json.dumps({"families": [{"key": "w1-d", "state": "v5"}, {"key": "w2-b", "state": {"state": "v5"}}]}),
    )
    assert notes() == [], "both at «v5»: the notes go"
    _steward(tmp_path, "live_status.json", json.dumps({"families": [{"key": "w1-d", "state": "V5"}]}))
    assert len(notes()) == 3, "a state is the word «v5», nothing like it"


@pytest.mark.django_db
def test_while_a_persona_is_inside_the_sign_in_states_leave_it_first(client, preview, accounts, this_database):
    """
    Review W1-P, UX r2 n3 (CD condition C3): as a persona, the two sign-in states framed the
    dashboard — allauth sends a signed-in visitor on. While a persona is inside, each is a small POST
    to «esci» that opens the sign-in; signed out, they stay links.
    """

    def states() -> str:
        html = client.get(INDEX).content.decode()
        return html[html.index('id="stati"') : html.index('id="famiglie"')]

    signed_out = states()
    assert signed_out.count(f'<a href="{LANDING}?page=/fr/compte/login/">Nella cornice</a>') == 2
    assert "dp-states__go" not in signed_out
    client.post(ENTER + "qa-doc-person/")
    inside = states()
    assert f'<a href="{LANDING}?page=/fr/compte/login/">' not in inside
    forms = re.findall(r'<form class="dp-states__go" method="post" action="([^"]+)">(.*?)</form>', inside, flags=re.S)
    assert [action for action, _body in forms] == [EXIT, EXIT]
    for _action, body in forms:
        assert 'name="csrfmiddlewaretoken"' in body
        assert '<input type="hidden" name="page" value="/fr/compte/login/">' in body
        assert '<button class="dp-states__button" type="submit">Esci dalla persona e apri l’accesso</button>' in body
    # The form does what it says: the persona leaves, and the landing frames the sign-in.
    response = client.post(EXIT, {"page": "/fr/compte/login/"})
    assert response.status_code == 302 and response["Location"] == f"{LANDING}?page=/fr/compte/login/"
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_signed_out_the_way_in_says_personas_and_entrer_opens_the_page_asked_for(
    client, preview, accounts, this_database
):
    """
    Review W1-P, UX r2 n2 (CD condition C4): signed out, the product's own way in ends on the
    sign-in's password form, and nothing pointed to «Personas»; «Entrer» dropped the sign-in's
    ``next``. One muted line beside the state says the way in, and each «Entrer» carries the page the
    sign-in was asked for — which the switch opens only when it is that persona's own.
    """
    hint = '<span class="dp-strip__hint" data-dp-hint>Per entrare senza password: «Personas»</span>'
    asked = "/fr/espace-reserve/mes-echeances/"
    html = client.get(LANDING, {"page": asked}).content.decode()
    assert hint in html
    strip = html[html.index('<header class="dp-strip"') : html.index("</header>")]
    for key in ("qa-doc-person", "qa-person", "qa-fresh-person", "qa-company"):
        form = strip[strip.index(f'action="{ENTER}{key}/"') :]
        form = form[: form.index("</form>")]
        assert f'<input type="hidden" name="page" value="{asked}" data-dp-next-field>' in form, key
    # The sign-in itself, with the next it was given: the same line, the same page.
    html = client.get(LANDING, {"page": f"/fr/compte/login/?next={asked}"}).content.decode()
    assert hint in html and f'value="{asked}" data-dp-next-field>' in html
    # A next that is not a page of this site is never carried; the line stays, it is the sign-in.
    html = client.get(LANDING, {"page": "/fr/compte/login/?next=https://evil.example/"}).content.decode()
    assert hint in html and '<input type="hidden" name="page" value="" data-dp-next-field>' in html
    # Nowhere else.
    for page in ("/fr/", "/fr/faq/"):
        html = client.get(LANDING, {"page": page}).content.decode()
        assert "data-dp-hint hidden>" in html, page
        assert '<input type="hidden" name="page" value="" data-dp-next-field>' in html, page
    data = json.loads(re.search(r'<script id="dp-live-map" type="application/json">(.*?)</script>', html).group(1))
    assert data["signin"] == ["/fr/compte/login/", "/ar/compte/login/", "/it/compte/login/", "/en/compte/login/"]
    # «Entrer» as qa-doc-person lands on «Mes échéances»; another persona's page would not be opened.
    response = client.post(ENTER + "qa-doc-person/", {"page": asked, "lang": "fr"})
    assert response.status_code == 302 and response["Location"] == f"{LANDING}?page={asked}"
    # With a persona inside, the line is gone.
    html = client.get(LANDING, {"page": "/fr/compte/login/"}).content.decode()
    assert "data-dp-hint hidden>" in html
    script = (STATIC / "js" / "dev" / "designpreview.js").read_text(encoding="utf-8")
    assert "hint.hidden = !(signin && !map.persona);" in script, "the strip follows the frame to the sign-in"


@pytest.mark.django_db
def test_the_names_and_languages_the_owner_and_assistive_technology_read(client, preview, tmp_path):
    """
    Review W1-P, accessibility r2 n1–n4 and m6′ (CD condition C8): the home link keeps «Italy Legal
    Entry™ — V5» below 90 rem (the words leave the eye, never the name); «1:1» says what it does and
    is disabled until there is a desktop frame; forced colours keep a pressed toggle pressed;
    «Superfici V5» says its count in words; «V4 + fondation» is French wherever it is the state.
    """
    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    ile = "".join(_declarations(block, ".dp-strip__ile") for block in _media_blocks(css, "max-width: 89.99rem"))
    assert "clip-path: inset(50%)" in ile and "position: absolute" in ile and "display: none" not in ile
    forced = "".join(
        _declarations(block, '.dp-viewer__button[aria-pressed="true"]')
        for block in _media_blocks(css, "forced-colors: active")
    )
    assert (
        "background: Highlight" in forced and "color: HighlightText" in forced and "forced-color-adjust: none" in forced
    )
    html = client.get(INDEX).content.decode()
    assert (
        'data-dp-true-size aria-pressed="false" title="La cornice desktop alla sua misura vera, senza ridurla" disabled>'
        '1:1<span class="dp-hidden"> — misura vera della cornice desktop</span></button>'
    ) in html
    html = client.get(LANDING).content.decode()
    assert 'data-dp-state-label lang="fr">V4 + fondation</span>' in html
    _steward(
        tmp_path,
        "live_status.json",
        json.dumps(
            {
                "surfaces": {"home": "v5"},
                "families": [
                    {"key": "w1-a", "title": "Fondazione", "state": "v5"},
                    {"key": "w1-b", "title": "Icone", "state": "v4-fondation"},
                ],
            }
        ),
    )
    html = client.get(LANDING).content.decode()
    assert "data-dp-state-label>V5 — council-passed</span>" in html
    assert (
        '<summary class="dp-strip__summary">Superfici V5<span class="dp-hidden">:</span> '
        '<span class="dp-strip__count">1</span><span class="dp-hidden"> pagina</span></summary>'
    ) in html
    board = client.get(INDEX).content.decode()
    board = board[board.index('id="famiglie"') : board.index('id="fondazione"')]
    assert '<span class="dp-state dp-state--v5">V5 — council-passed</span>' in board
    assert '<span class="dp-state dp-state--v4-fondation" lang="fr">V4 + fondation</span>' in board
    script = (STATIC / "js" / "dev" / "designpreview.js").read_text(encoding="utf-8")
    assert 'words.removeAttribute("lang");' in script and 'words.lang = "fr";' in script
    assert "trueSize.disabled = !held.frames.some(" in script


@pytest.mark.django_db
def test_the_index_says_one_in_the_singular_and_dates_in_words(client, preview, tmp_path):
    """
    Review W1-P, UX r2 n8 and n9, accessibility r2 O8 (CD condition C9): «1 famiglie» and ISO dates
    in Italian sentences; 41 identical «V4 + fondation» chips under a fold that already says it. The
    singular where it is one; «5 ottobre 2026», the ISO value kept in ``datetime``; inside the fold a
    row carries no chip; a path in a sentence breaks wherever it must.
    """
    from designpreview import live

    html = client.get(INDEX).content.decode()
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    summary, rows = public[public.index('<details class="dp-index__fold" open>') :].split("</summary>", 1)
    assert "dp-state--v4-fondation" in summary, "the fold says it, once"
    assert "dp-state" not in rows, "no chip on a V4 row inside the fold"
    keys = {page.surface: "v5" for page in live.PUBLIC_PAGES if page.slug != "faq"}
    _steward(
        tmp_path,
        "live_status.json",
        json.dumps(
            {
                "updated": "2026-10-05",
                "surfaces": keys,
                "families": [{"key": "w1-b", "title": "Icone", "state": "v4-fondation", "date": "2026-10-06"}],
            }
        ),
    )
    html = client.get(INDEX).content.decode()
    assert "</span></span> 1 pagina pubblica</summary>" in html
    assert "</span></span> 1 famiglia</summary>" in html
    assert 'Aggiornato il <time datetime="2026-10-05">5 ottobre 2026</time>.' in html
    assert '<time datetime="2026-10-06">6 ottobre 2026</time>' in html
    public = html[html.index('id="pubbliche"') : html.index('id="personas"')]
    passed, fold = public.split('<details class="dp-index__fold">', 1)
    assert passed.count('<span class="dp-state dp-state--v5">V5 — council-passed</span>') == passed.count(
        '<li class="dp-row"'
    )
    assert "dp-state" not in fold.split("</summary>", 1)[1]
    _steward(tmp_path, "live_status.json", json.dumps({"updated": "domani"}))
    assert 'Aggiornato il <time datetime="domani">domani</time>.' in client.get(INDEX).content.decode()
    _steward(tmp_path, "live_status.json", json.dumps({"families": [{"key": "w1-b"}, {"key": "w1-c"}]}))
    html = client.get(INDEX).content.decode()
    assert "</span></span> 2 famiglie</summary>" in html
    assert f"</span></span> {len(live.PUBLIC_PAGES)} pagine pubbliche</summary>" in html
    css = re.sub(
        r"/\*.*?\*/", "", (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8"), flags=re.S
    )
    assert "overflow-wrap: anywhere" in _declarations(css, ".dp-index__text code")


# --------------------------------------------------------------------------- the archive (plan §4.2, §4.3)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("old", "new"),
    [
        (OLD_PICKER, PICKER),
        (OLD_PICKER + "?variant=he&lang=ar&phase=3", PICKER + "?variant=he&lang=ar&phase=3"),
        (OLD_TYPE + "?system=b&surface=case", TYPE + "?system=b&surface=case"),
        (OLD_COMPARE + "?pair=mes-pieces&lang=ar", COMPARE + "?pair=mes-pieces&lang=ar"),
        (OLD_PROOF + "home/phase3.html", PROOF + "home/phase3.html"),
        (OLD_PROOF + "research/loader/mandata/index.html?rm=1", PROOF + "research/loader/mandata/index.html?rm=1"),
        (OLD_PROOF + "research/hero/hc/ar.html", PROOF + "research/hero/hc/ar.html"),
    ],
)
def test_the_archive_s_old_addresses_redirect_to_their_research_equivalents(client, preview, old, new):
    response = client.get(old)
    assert response.status_code == 302, old
    assert response["Location"] == new
    _assert_sealed(response)
    assert client.get(response["Location"]).status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "relative",
    [".work/notes.txt", "WORK~1/notes.txt", "home/build.py", "home/../../outside.html", "home//phase3.html", "home/"],
)
def test_an_old_proof_address_is_judged_before_it_is_redirected(client, preview, relative):
    """What the proof view would refuse by its string is a 404 at the old address already: no redirect is broader."""
    response = client.get(OLD_PROOF + relative)
    assert response.status_code == 404, relative
    assert "Location" not in response


@pytest.mark.django_db
def test_the_archive_says_what_it_is_and_has_left_the_baseline_group(client, preview):
    """
    §4.3: «Baseline V4 (controllo)» linked this server's own pages as V4 — false the moment V5
    enters the templates. The archive links no live page of this server; it says it is the archive
    and where the live product and its index are.
    """
    html = client.get(ARCHIVE).content.decode()
    assert "Baseline V4 (controllo)" not in html and 'id="g-baseline"' not in html
    assert "dp-link--live" not in html
    for live_page in ('href="/fr/"', 'href="/ar/"', 'href="/fr/compte/login/"', 'href="/fr/espace-reserve/"'):
        assert live_page not in html, live_page
    assert "Anteprima V5 · archivio della ricerca · sviluppo · non pubblica" in html
    assert f'<a class="dp-masthead__live" href="{LANDING}">Il prodotto V5 dal vivo</a>' in html
    assert f'<a href="{INDEX}">indice</a>' in html
    # Review W1-P M6: the archive keeps every note as it was (plan §4.2) and no longer reads as the
    # place to look, nor hands the owner a choice V5.4 closed — one historical notice says so.
    assert '<h1 class="dp-title">Archivio della ricerca</h1>' in html
    assert "conservati come erano, per tracciabilità" in html
    assert "Le note sono quelle di allora" in html and "Scritte fino al 4 ottobre 2026." in html
    assert "con la V5.4 decide il consiglio, e una famiglia che lo passa si propaga senza attendere" in html
    for gone in (
        "Le superfici da guardare",
        "nell’ordine in cui vanno guardati",
        "decisioni aperte del proprietario",
        "nessuna famiglia V5 viene propagata prima della sua approvazione",
    ):
        assert gone not in html, gone
    assert "decide il proprietario" in html, "the notes themselves are kept, as written"


# --------------------------------------------------------------------------- the persona switch (plan §4.4)


@pytest.mark.django_db
def test_the_switch_signs_a_persona_in_read_only_and_logs_its_key_never_its_e_mail(
    client, preview, accounts, this_database, caplog
):
    """
    ``auth.login`` with the ModelBackend: the session belongs to the QA account, carries the
    persona's flag, sends ``user_logged_in`` (the audit trail records the sign-in, so the entrance
    plays as after a real one) and is minted without a password. One log line: the persona key.
    The browser lands on the landing, framing the persona's first page.
    """
    from designpreview import personas

    from audit.models import AuditEvent

    caplog.set_level(logging.INFO, logger="ile.designpreview")
    response = client.post(ENTER + "qa-doc-person/", {"lang": "fr"})
    assert response.status_code == 302
    assert response["Location"] == LANDING + "?page=/fr/espace-reserve/"
    _assert_sealed(response)
    assert "ile_v5_sessionid" in response.cookies and "sessionid" not in response.cookies
    session = client.session
    assert session["_auth_user_id"] == str(accounts["qa-doc-person"].pk)
    assert session["_auth_user_backend"] == "django.contrib.auth.backends.ModelBackend"
    assert session[personas.SESSION_KEY] == "qa-doc-person"
    lines = [record.getMessage() for record in caplog.records if record.name == "ile.designpreview"]
    assert lines == ["Design preview: persona qa-doc-person signed in (read-only session)."]
    assert "@" not in " ".join(lines)
    assert AuditEvent.objects.filter(action="auth.login", actor=accounts["qa-doc-person"]).exists()
    html = client.get(LANDING + "?page=/fr/espace-reserve/").content.decode()
    assert '<span class="dp-strip__dot" aria-hidden="true"></span>' in html
    assert 'Dentro come «<span lang="fr">Personne avec dossier</span>»' in html
    assert '<button class="dp-persona__button" type="submit" lang="fr">Sortir</button>' in html
    # The summary says who is in, without a stray space; the list says «dentro» on that row (m6, m9).
    assert '<span class="dp-hidden"> — dentro come </span><span lang="fr">Personne avec dossier</span>' in html
    strip = html[html.index('<header class="dp-strip"') : html.index("</header>")]
    row = strip[strip.index(f'action="{ENTER}qa-doc-person/"') :]
    row = row[: row.index("</form>")]
    assert '<span class="dp-persona__state">dentro</span>' in row and "Entrer" not in row
    assert 'apre il suo <span lang="fr">Tableau de bord</span>' in row
    # The company persona opens the company's space; the language and the frame follow the strip.
    response = client.post(ENTER + "qa-company/", {"lang": "ar", "frame": "phone"})
    assert response["Location"] == LANDING + "?page=/ar/espace-reserve/entreprise/&frame=phone"
    assert client.session["_auth_user_id"] == str(accounts["qa-company"].pk)
    assert client.session[personas.SESSION_KEY] == "qa-company"


@pytest.mark.django_db
def test_the_switch_enforces_its_csrf_token(preview, accounts, this_database):
    csrf_client = Client(enforce_csrf_checks=True, HTTP_HOST=HOST)
    response = csrf_client.post(ENTER + "qa-doc-person/", {"lang": "fr"})
    assert response.status_code == 403
    assert "_auth_user_id" not in csrf_client.session
    html = csrf_client.get(LANDING).content.decode()
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)
    response = csrf_client.post(ENTER + "qa-doc-person/", {"lang": "fr", "csrfmiddlewaretoken": token})
    assert response.status_code == 302
    assert "_auth_user_id" in csrf_client.session
    response = Client(enforce_csrf_checks=True, HTTP_HOST=HOST).post(EXIT)
    assert response.status_code == 403


@pytest.mark.django_db
def test_the_switch_never_opens_a_staff_session_whatever_the_allow_list_says(
    client, preview, accounts, this_database, django_user_model, caplog
):
    caplog.set_level(logging.INFO, logger="ile.designpreview")
    staff = django_user_model.objects.create_user(email="qa-staff@example.test", password=None, is_staff=True)
    for email in ("qa-admin@example.test", staff.email):
        with override_settings(ILE_DESIGN_PREVIEW_PERSONAS={"qa-doc-person": email}):
            response = client.post(ENTER + "qa-doc-person/")
        assert response.status_code == 403, email
        assert "non apre mai una sessione dello staff" in response.content.decode()
        assert "_auth_user_id" not in client.session
    lines = " ".join(record.getMessage() for record in caplog.records if record.name == "ile.designpreview")
    assert "persona qa-doc-person refused (staff)" in lines and "@" not in lines


@pytest.mark.django_db
def test_the_switch_refuses_an_unknown_persona_and_an_absent_or_inactive_account(
    client, preview, accounts, this_database
):
    assert client.post(ENTER + "qa-admin/").status_code == 404, "not a persona: not a route"
    assert client.post(ENTER + "qa-somebody/").status_code == 404
    with override_settings(ILE_DESIGN_PREVIEW_PERSONAS={"qa-person": "nobody@example.test"}):
        response = client.post(ENTER + "qa-person/")
        assert response.status_code == 403 and "nessun account attivo per «qa-person»" in response.content.decode()
        assert client.post(ENTER + "qa-doc-person/").status_code == 404, "a persona the list does not name"
    accounts["qa-fresh-person"].is_active = False
    accounts["qa-fresh-person"].save(update_fields=["is_active"])
    response = client.post(ENTER + "qa-fresh-person/")
    assert response.status_code == 403
    assert "@" not in response.content.decode(), "the refusal names the persona, never its e-mail"
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_one_click_enters_a_persona_and_opens_its_page_only_if_the_page_is_its_own(
    client, preview, accounts, this_database
):
    """
    Review W1-P M3: «fr» or «ar» of a page on a persona's card enters that persona and opens that
    page. The switch honours ``page`` only when it is one of that persona's own pages, in any of its
    languages; anything else — another persona's page, a public page, another origin, a dot
    segment — opens the persona's first page, as «Entrer» always did.
    """
    from designpreview import personas

    response = client.post(ENTER + "qa-doc-person/", {"page": "/ar/espace-reserve/mes-echeances/", "lang": "ar"})
    assert response["Location"] == LANDING + "?page=/ar/espace-reserve/mes-echeances/"
    assert client.session[personas.SESSION_KEY] == "qa-doc-person"
    for page in (
        "/fr/espace-reserve/entreprise/mes-besoins/",
        "/fr/le-projet/",
        "https://attacker.test/fr/espace-reserve/",
        "/fr/../fr/espace-reserve/mes-echeances/",
        "/fr/espace-reserve/mes-echeances/?x=1",
    ):
        response = client.post(ENTER + "qa-doc-person/", {"page": page, "lang": "fr"})
        assert response["Location"] == LANDING + "?page=/fr/espace-reserve/", page
    # The documents app has no prefix: the language goes with it, and the landing sets the cookie.
    response = client.post(ENTER + "qa-doc-person/", {"page": "/documents/", "lang": "ar"})
    assert response["Location"] == LANDING + "?page=/documents/&lang=ar"
    assert client.get(response["Location"]).cookies["ile_v5_language"].value == "ar"
    # A page of qa-company is qa-company's: entered by its own form, it opens there.
    response = client.post(ENTER + "qa-company/", {"page": "/fr/espace-reserve/entreprise/mes-besoins/"})
    assert response["Location"] == LANDING + "?page=/fr/espace-reserve/entreprise/mes-besoins/"


@pytest.mark.django_db
def test_the_switch_never_opens_a_privileged_session_whatever_the_role(
    client, preview, accounts, this_database, caplog
):
    """
    Review W1-P, security m4 (DL54-18): a privilege here is a group, independent of ``is_staff`` —
    an operator handles case files, a moderator moderates. An allow-listed account that holds any
    role but a person's or a company's, or a permission of its own, is refused: no session.
    """
    from django.contrib.auth.models import Group, Permission

    caplog.set_level(logging.INFO, logger="ile.designpreview")
    accounts["qa-person"].groups.add(Group.objects.get_or_create(name="role:operator")[0])
    response = client.post(ENTER + "qa-person/")
    assert response.status_code == 403
    assert "l’anteprima non apre mai una sessione con privilegi" in response.content.decode()
    assert "_auth_user_id" not in client.session
    accounts["qa-fresh-person"].user_permissions.add(Permission.objects.order_by("pk").first())
    assert client.post(ENTER + "qa-fresh-person/").status_code == 403
    assert "_auth_user_id" not in client.session
    # A person's and a company's roles are what a persona is.
    accounts["qa-company"].groups.add(Group.objects.get_or_create(name="role:company")[0])
    accounts["qa-doc-person"].groups.add(Group.objects.get_or_create(name="role:person")[0])
    assert client.post(ENTER + "qa-company/").status_code == 302
    assert client.post(ENTER + "qa-doc-person/").status_code == 302
    lines = " ".join(record.getMessage() for record in caplog.records if record.name == "ile.designpreview")
    assert "persona qa-person refused (privileged)" in lines and "persona qa-fresh-person refused (privileged)" in lines
    assert "@" not in lines


@pytest.mark.django_db
def test_the_switch_refuses_any_database_outside_its_list_and_the_v4_control_s_always(
    client, preview, accounts, monkeypatch
):
    """``ILE_DESIGN_PREVIEW_ALLOWED_DATABASES`` decides — and ``ile_qa`` and ``ile`` are refused even when it names them."""
    from designpreview import personas

    response = client.post(ENTER + "qa-doc-person/")  # the test database is not ile_v5
    assert response.status_code == 403
    assert "questo server usa il database «test_" in response.content.decode()
    assert "_auth_user_id" not in client.session
    for name in ("ile_qa", "ile"):
        monkeypatch.setattr(personas, "database_name", lambda alias="default", name=name: name)
        with override_settings(ILE_DESIGN_PREVIEW_ALLOWED_DATABASES=(name, "ile_v5")):
            response = client.post(ENTER + "qa-doc-person/")
        assert response.status_code == 403, name
        assert f"il database «{name}»" in response.content.decode()
        assert "_auth_user_id" not in client.session
    assert personas.V4_CONTROL_DATABASES == {"ile", "ile_qa"}


@pytest.mark.django_db
def test_sortir_signs_the_browser_out_and_frames_a_public_page(client, preview, accounts, this_database, caplog):
    caplog.set_level(logging.INFO, logger="ile.designpreview")
    client.post(ENTER + "qa-person/")
    response = client.post(EXIT, {"page": "/ar/espace-reserve/mes-documents/", "frame": "phone"})
    assert response.status_code == 302
    assert response["Location"] == LANDING + "?page=/ar/&frame=phone", "a reserved page needs a session"
    assert "_auth_user_id" not in client.session
    client.post(ENTER + "qa-person/")
    assert client.post(EXIT, {"page": "/fr/le-projet/"})["Location"] == LANDING + "?page=/fr/le-projet/"
    assert client.post(EXIT, {"page": "https://attacker.test/"})["Location"] == LANDING + "?page=/fr/"
    lines = [record.getMessage() for record in caplog.records if record.name == "ile.designpreview"]
    assert "Design preview: persona qa-person signed out." in lines
    assert "Design preview: persona - signed out." in lines, "signing out a browser that was signed out"


# --------------------------------------------------------------------------- read-only personas (plan §4.4)


@pytest.mark.django_db
def test_a_persona_session_cannot_write_outside_the_preview(client, preview, accounts, this_database, caplog):
    """
    Accepting the terms as ``qa-person`` would destroy that persona for everyone who looks after it.
    While the flag is set, every unsafe method outside ``/__design-v5/`` meets 403 — a sentence in
    plain words, sealed — except signing out and the language switch; reading is untouched.
    """
    caplog.set_level(logging.INFO, logger="ile.designpreview")
    client.post(ENTER + "qa-person/")
    for verb, path in (
        ("post", "/fr/espace-reserve/ma-situation/"),
        ("post", "/fr/consentements/newsletter/confirmer/x/"),
        ("post", "/fr/compte/profil/"),
        ("put", "/fr/espace-reserve/"),
        ("patch", "/fr/espace-reserve/mes-documents/"),
        ("delete", "/fr/espace-reserve/mes-documents/"),
        ("post", "/documents/upload/"),
        ("post", "/api/v1/anything/"),
    ):
        response = getattr(client, verb)(path)
        assert response.status_code == 403, (verb, path)
        text = response.content.decode()
        assert response["Content-Type"] == "text/plain; charset=utf-8"
        assert text.startswith("Anteprima V5 — sola lettura.")
        assert (
            "Questa azione non è stata eseguita, e nulla è cambiato: «Personne, conditions non acceptées» resta "
            "uguale per chi guarda dopo."
        ) in text
        assert "«Indietro» del browser" in text and "«Sortir», nella barra in alto" in text
        for jargon in (path, "?état=", "cantieri", "non scrive"):
            assert jargon not in text, jargon
        _assert_sealed(response)
    lines = " ".join(record.getMessage() for record in caplog.records if record.name == "ile.designpreview")
    assert "persona qa-person, POST /fr/espace-reserve/ma-situation/ refused (read-only)" in lines
    assert "@" not in lines
    # Reading is untouched; the switch itself, inside the preview, still works.
    assert "sola lettura" not in client.get("/fr/espace-reserve/").content.decode()
    assert client.options("/fr/").status_code != 403
    assert client.post(ENTER + "qa-doc-person/").status_code == 302
    # The language switch and signing out are the two writes a persona keeps.
    response = client.post("/i18n/setlang/", {"language": "ar", "next": "/ar/"})
    assert response.status_code == 302 and response["Location"] == "/ar/"
    response = client.post("/fr/compte/logout/")
    assert response.status_code == 302
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_a_persona_cannot_forge_a_line_of_the_preview_s_log(client, preview, accounts, this_database, caplog):
    """
    Review W1-P, security m2: the refusal's log line wrote ``request.path`` raw, so a path holding
    ``%0a`` wrote a second line that looked like the switch's own. The method and the path reach the
    line escaped: one record, one line.
    """
    client.post(ENTER + "qa-doc-person/")
    caplog.set_level(logging.INFO, logger="ile.designpreview")
    caplog.clear()
    forged = "/fr/x%0aINFO%20ile.designpreview%20Design%20preview:%20persona%20qa-admin%20signed%20in.%0d"
    assert client.post(forged).status_code == 403
    records = [record for record in caplog.records if record.name == "ile.designpreview"]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message and "\r" not in message
    assert message.startswith("Design preview: persona qa-doc-person, POST /fr/x\\nINFO")
    assert message.endswith("refused (read-only).")


def test_the_ceiling_s_busy_line_escapes_what_a_request_chose(rf, caplog):
    """
    Review W1-P, security m7 (CD condition C6): the ceiling's 503 line wrote ``request.path`` raw, in
    the same logger as the persona lines, and a loopback client with no persona forged «persona
    qa-admin signed in» with it. Every line the preview logs escapes what a request chose
    (``designpreview.access.loggable``): one record, one line.
    """
    from designpreview.middleware import ConnectionCeilingMiddleware

    caplog.set_level(logging.INFO, logger="ile.designpreview")
    request = rf.get("/fr/x%0aINFO%20forged%0d")
    assert "\n" in request.path and "\r" in request.path, "the factory hands the view the decoded path"
    response = ConnectionCeilingMiddleware(lambda r: HttpResponse()).busy(request)
    assert response.status_code == 503
    records = [record for record in caplog.records if record.name == "ile.designpreview"]
    assert len(records) == 1
    message = records[0].getMessage()
    assert "\n" not in message and "\r" not in message
    assert "/fr/x\\nINFO forged\\r answered 503." in message


@pytest.mark.django_db
def test_a_session_that_is_not_a_persona_s_is_not_touched_by_the_rule(client, preview, accounts):
    client.force_login(accounts["qa-person"])
    response = client.post("/fr/nowhere/")
    assert response.status_code == 404 and "sola lettura" not in response.content.decode()
    client.logout()
    response = client.post("/fr/compte/login/", {"login": "x@example.test", "password": "wrong"})
    assert response.status_code in (200, 429) and "sola lettura" not in response.content.decode()
    # The same POST from a persona session is refused before any view.
    with override_settings(ILE_DESIGN_PREVIEW_ALLOWED_DATABASES=(_test_database_name(),)):
        client.post(ENTER + "qa-person/")
    assert client.post("/fr/nowhere/").status_code == 403


@pytest.mark.django_db
def test_a_frame_of_this_origin_may_show_the_refusal_and_nothing_else_may(client, preview, accounts, this_database):
    """
    The refusal answers a POST, and a POST is never framed — but it is the preview's own sentence,
    with nothing to click: inside the landing's frame the owner reads it instead of the browser's
    «refused to connect». Anywhere else it keeps the site's policy.
    """
    client.post(ENTER + "qa-person/")
    response = client.post("/fr/espace-reserve/ma-situation/", **FRAMED)
    assert response.status_code == 403
    assert response["X-Frame-Options"] == "SAMEORIGIN" and "frame-ancestors 'self'" in _csp(response)
    response = client.post("/fr/espace-reserve/ma-situation/")
    assert response["X-Frame-Options"] == "DENY" and "frame-ancestors 'none'" in _csp(response)
    response = client.post(
        "/fr/espace-reserve/ma-situation/", HTTP_SEC_FETCH_DEST="iframe", HTTP_SEC_FETCH_SITE="cross-site"
    )
    assert response["X-Frame-Options"] == "DENY"
    # The method belongs to the one predicate (review W1-P, security m6; CD condition C5): no frame is
    # navigated with PUT, PATCH or DELETE, so the refusal of one keeps the normal policy, framed or not.
    for method in ("put", "patch", "delete"):
        response = getattr(client, method)("/fr/espace-reserve/ma-situation/", **FRAMED)
        assert response.status_code == 403 and "sola lettura" in response.content.decode(), method
        assert response["X-Frame-Options"] == "DENY" and "frame-ancestors 'none'" in _csp(response), method
    response = client.post("/fr/espace-reserve/ma-situation/", **FRAMED)
    assert response["X-Frame-Options"] == "SAMEORIGIN" and "frame-ancestors 'self'" in _csp(response)


# --------------------------------------------------------------------------- frames (plan §4.4)


def _relaxed(response) -> bool:
    return "frame-ancestors 'self'" in _csp(response) and response.get("X-Frame-Options") == "SAMEORIGIN"


def _strict(response) -> bool:
    return "frame-ancestors 'none'" in _csp(response) and response.get("X-Frame-Options") == "DENY"


@pytest.mark.django_db
def test_a_real_page_is_framed_by_this_origin_only_when_every_condition_holds(client, preview):
    """
    Relaxed — ``frame-ancestors 'self'``, ``X-Frame-Options: SAMEORIGIN`` — only for GET or HEAD,
    ``Sec-Fetch-Dest: iframe``, ``Sec-Fetch-Site: same-origin``, from loopback with no proxy header,
    on this process's own host, with DEBUG and the flag. The rest of the policy does not move, and
    the response varies on the two headers that decided. Strict whenever one condition fails.
    """
    response = client.get("/fr/", **FRAMED)
    assert response.status_code == 200 and _relaxed(response)
    csp = _csp(response)
    assert "script-src 'self'" in csp and "style-src 'self'" in csp and "unsafe" not in csp
    assert "Sec-Fetch-Dest" in response["Vary"] and "Sec-Fetch-Site" in response["Vary"]
    assert _relaxed(client.head("/fr/", **FRAMED))
    assert _relaxed(client.get("/ar/espace-reserve/", **FRAMED)), "a redirect to the login is framed too"
    for extra in (
        {},
        {"HTTP_SEC_FETCH_DEST": "document", "HTTP_SEC_FETCH_SITE": "same-origin"},
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "cross-site"},
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "same-site"},
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "none"},
        {"HTTP_SEC_FETCH_DEST": "iframe"},
        {"HTTP_SEC_FETCH_SITE": "same-origin"},
        {"HTTP_SEC_FETCH_DEST": "frame", "HTTP_SEC_FETCH_SITE": "same-origin"},
        {**FRAMED, "REMOTE_ADDR": "10.0.0.9"},
        {**FRAMED, "HTTP_X_FORWARDED_FOR": "203.0.113.7"},
        {**FRAMED, "HTTP_FORWARDED": "for=203.0.113.7"},
        {**FRAMED, "HTTP_CF_CONNECTING_IP": "203.0.113.7"},
        {**FRAMED, "HTTP_HOST": "localhost:8781"},
    ):
        response = client.get("/fr/", **extra)
        assert response.status_code == 200 and _strict(response), extra
        assert "Sec-Fetch-Dest" in response["Vary"], extra
    # A form's answer inside the frame is relaxed under exactly the same condition (DL54-17, security
    # M1): the sign-in's error is the engage the index points at. Strict for any other caller.
    response = client.post("/fr/compte/login/", {"login": "x@example.test", "password": "wrong"}, **FRAMED)
    assert response.status_code in (200, 429) and _relaxed(response), "200, or 429 once allauth's limit is met"
    for extra in (
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "cross-site"},
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "same-site"},
        {"HTTP_SEC_FETCH_DEST": "iframe", "HTTP_SEC_FETCH_SITE": "none"},
        {"HTTP_SEC_FETCH_DEST": "document", "HTTP_SEC_FETCH_SITE": "same-origin"},
        {**FRAMED, "HTTP_X_FORWARDED_FOR": "203.0.113.7"},
        {**FRAMED, "HTTP_HOST": "localhost:8781"},
        {**FRAMED, "REMOTE_ADDR": "10.0.0.9"},
    ):
        response = client.post("/fr/compte/login/", {"login": "x@example.test", "password": "wrong"}, **extra)
        assert _strict(response), extra
    assert _strict(client.put("/fr/", **FRAMED)), "a PUT is never a frame's navigation"

    # The back-office, and the preview's own pages, are never relaxed by the middleware.
    assert _strict(client.get("/backoffice/login/", **FRAMED))
    for path in (LANDING, INDEX, ARCHIVE, STATE_429):
        assert _strict(client.get(path, **FRAMED)), path
    # Without the flag, or without DEBUG, nothing is relaxed — the middleware is in the chain all the same.
    for switch in ({"ILE_DESIGN_PREVIEW": False}, {"DEBUG": False}):
        with override_settings(**switch):
            assert _strict(client.get("/fr/", **FRAMED)), switch


def _directives(response) -> dict[str, str]:
    return {
        part.split(" ", 1)[0]: (part.split(" ", 1) + [""])[1]
        for part in (piece.strip() for piece in _csp(response).split(";"))
        if part
    }


@pytest.mark.django_db
def test_a_relaxed_policy_differs_from_the_strict_one_in_two_directives_and_nothing_else(client, preview):
    """
    Security M1's constraint: the frame exception changes ``frame-ancestors`` (to ``'self'``) and
    drops ``upgrade-insecure-requests`` — compared directive by directive with the strict policy of
    the same page, for a GET and for a form's answer — and the global policy keeps both.
    """
    for relaxed, strict in (
        (client.get("/fr/le-projet/", **FRAMED), client.get("/fr/le-projet/")),
        (
            client.post("/fr/compte/login/", {"login": "x@example.test", "password": "wrong"}, **FRAMED),
            client.post("/fr/compte/login/", {"login": "x@example.test", "password": "wrong"}),
        ),
    ):
        loose, tight = _directives(relaxed), _directives(strict)
        assert tight["frame-ancestors"] == "'none'" and "upgrade-insecure-requests" in tight
        assert loose["frame-ancestors"] == "'self'" and "upgrade-insecure-requests" not in loose
        rest = {
            key: value for key, value in tight.items() if key not in ("frame-ancestors", "upgrade-insecure-requests")
        }
        assert {key: value for key, value in loose.items() if key != "frame-ancestors"} == rest


def test_the_frame_exception_merges_into_what_a_view_has_replaced():
    """The codebase's own pattern (core.middleware.BackofficeCSPMiddleware): ``_csp_replace``, which django-csp applies."""
    from designpreview import frames

    response = HttpResponse()
    response._csp_replace = {"img-src": ("'self'", "data:")}
    frames.relax(response)
    assert response._csp_replace == {
        "img-src": ("'self'", "data:"),
        "frame-ancestors": ("'self'",),
        "upgrade-insecure-requests": None,
    }
    assert response["X-Frame-Options"] == "SAMEORIGIN"
    bare = HttpResponse()
    frames.relax(bare)
    assert bare._csp_replace == {"frame-ancestors": ("'self'",), "upgrade-insecure-requests": None}


def test_the_dev_chain_puts_the_ceiling_first_the_frame_exception_after_csp_and_the_read_only_rule_last(
    dev_preview, preview
):
    """
    The ceiling first, so that nothing reads the database before it; the frame exception listed
    after ``CSPMiddleware`` and ``XFrameOptionsMiddleware``, so that its response hook runs before
    theirs (django-csp writes the header from ``_csp_replace``; XFrameOptions keeps a header that
    is there); the read-only rule last, once the session and the language are known. The base chain
    in between, untouched.
    """
    from config.settings import base

    chain = dev_preview.MIDDLEWARE
    assert chain[0] == CEILING
    assert chain[1:-2] == list(base.MIDDLEWARE)
    assert chain[-2:] == [FRAMES, READ_ONLY]
    for earlier in (
        "csp.middleware.CSPMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "core.middleware.BackofficeCSPMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
    ):
        assert chain.index(earlier) < chain.index(FRAMES), earlier
    assert settings.MIDDLEWARE == chain, "the preview's tests run with this chain installed"


@pytest.mark.django_db
def test_the_read_only_rule_and_the_frame_exception_do_nothing_outside_the_preview_s_condition(preview):
    """Installed and idle: no persona flag, no relaxation, no header changed but ``Vary``."""
    from designpreview import frames, personas

    seen = []

    def view(request):
        seen.append(request.method)
        return HttpResponse("ok")

    rule = personas.PersonaReadOnlyMiddleware(view)
    exception = frames.PreviewFrameMiddleware(view)
    from django.test import RequestFactory

    factory = RequestFactory(HTTP_HOST=HOST)
    request = factory.post("/fr/espace-reserve/ma-situation/")
    request.session = {}
    assert rule(request).status_code == 200 and seen == ["POST"]
    request = factory.post("/fr/espace-reserve/ma-situation/")
    request.session = {personas.SESSION_KEY: "qa-person"}
    response = rule(request)
    assert response.status_code == 403 and seen == ["POST"], "refused before the view"
    response = exception(factory.get("/fr/"))
    assert "_csp_replace" not in response.__dict__ and "X-Frame-Options" not in response
    response = exception(factory.get("/fr/", **FRAMED))
    assert response._csp_replace == {"frame-ancestors": ("'self'",), "upgrade-insecure-requests": None}
    assert response["X-Frame-Options"] == "SAMEORIGIN"


# --------------------------------------------------------------------------- the dev assets


def _all_templates() -> dict[str, str]:
    found = {}
    for path in list(TEMPLATES.rglob("*.html")) + list((ROOT / "apps").rglob("templates/**/*.html")):
        found[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    return found


def test_the_dev_assets_are_loaded_only_by_the_dev_templates():
    """
    The stylesheet and the script of the preview are referenced by templates/dev/designpreview/*
    and by nothing else: not the production cascade, not a bundle, not a template a visitor reaches.
    """
    assert (STATIC / "css" / "dev" / "designpreview.css").exists()
    assert (STATIC / "js" / "dev" / "designpreview.js").exists()
    assert "dev/designpreview" not in (STATIC / "css" / "main.css").read_text(encoding="utf-8")
    assert "dev/designpreview" not in (ROOT / "scripts" / "build_frontend.mjs").read_text(encoding="utf-8")
    assert "dev/designpreview" not in (ROOT / "scripts" / "build_css.mjs").read_text(encoding="utf-8")
    loaders = {name for name, text in _all_templates().items() if "dev/designpreview." in text}
    assert loaders == {
        "templates/dev/designpreview/_stylesheets.html",
        "templates/dev/designpreview/hub.html",
        "templates/dev/designpreview/frame.html",
        "templates/dev/designpreview/compare.html",
        "templates/dev/designpreview/landing.html",
        "templates/dev/designpreview/index.html",
    }, loaders
    # The preview's own templates: the live product's two pages and their partials, the archive's
    # three pages and its partial, beside the folder of the foundation families' specimen boards
    # (held by test_the_specimens_folder_holds_its_readme_and_boards_only).
    own = sorted(path.name for path in (TEMPLATES / "dev" / "designpreview").iterdir())
    assert own == [
        "_build.html",
        "_changelog.html",
        "_family.html",
        "_personas.html",
        "_quick.html",
        "_row.html",
        "_strip.html",
        "_stylesheets.html",
        "bar_group.html",
        "compare.html",
        "frame.html",
        "hub.html",
        "index.html",
        "landing.html",
        "specimens",
    ], own
    includers = {name for name, text in _all_templates().items() if "designpreview/bar_group.html" in text}
    assert includers == {"templates/dev/designpreview/frame.html", "templates/dev/designpreview/compare.html"}
    standalone = {name for name, text in _all_templates().items() if "designpreview/_stylesheets.html" in text}
    assert standalone == {
        "templates/dev/designpreview/frame.html",
        "templates/dev/designpreview/compare.html",
        "templates/dev/designpreview/landing.html",
        "templates/dev/designpreview/index.html",
    }, "every document that holds a frame loads the token layers, never the bundled cascade"
    for name in standalone:
        assert "css/dist/main.css" not in (ROOT / name).read_text(encoding="utf-8"), name


def test_the_dev_stylesheet_speaks_tokens_only():
    css = (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8")
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    assert re.findall(r"#[0-9a-fA-F]{3,8}\b", stripped) == [], "no literal colour: use var(--…)"
    assert not re.search(r"\brgba?\(|\bhsla?\(", stripped)
    assert not re.search(r"https?://", stripped)
    assert "!important" not in stripped and "@import" not in stripped
    declared: set[str] = set()
    for sheet in (STATIC / "css").rglob("*.css"):
        if "dist" in sheet.parts or sheet.parent.name == "dev":
            continue
        declared |= set(re.findall(r"(?<![\w-])(--[a-z0-9-]+)\s*:", sheet.read_text(encoding="utf-8")))
    # The sheet's own properties — the viewer's scale, set by its script — are declared in it.
    declared |= set(re.findall(r"(?<![\w-])(--dp-[a-z0-9-]+)\s*:", stripped))
    used = set(re.findall(r"var\((--[a-z0-9-]+)", stripped))
    assert used <= declared, sorted(used - declared)
    shim = set(
        re.findall(
            r"^\s*(--[a-z0-9-]+):", (STATIC / "css" / "_legacy-tokens.css").read_text(encoding="utf-8"), flags=re.M
        )
    )
    assert not (used & shim), f"new code written against the retired system: {sorted(used & shim)}"
    physical = re.findall(
        r"(?<![-\w])(?:margin|padding|border)-(?:left|right)\b|text-align:\s*(?:left|right)|float:", stripped
    )
    assert physical == [], physical


def _media_blocks(css: str, condition: str) -> list[str]:
    """The body of every ``@media (<condition>) { … }`` block of the sheet, braces matched."""
    opening = f"@media ({condition}) {{"
    bodies, cursor = [], css.find(opening)
    while cursor != -1:
        start = position = cursor + len(opening)
        depth = 1
        while depth:
            position = min(index for index in (css.find("{", position), css.find("}", position)) if index != -1)
            depth += 1 if css[position] == "{" else -1
            position += 1
        bodies.append(css[start : position - 1])
        cursor = css.find(opening, position)
    assert bodies, f"no {opening} in the sheet"
    return bodies


def _declarations(block: str, selector: str) -> str:
    """The declarations of the rule(s) whose selector list names ``selector``, in ``block``."""
    found = ""
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block):
        if selector in [part.strip() for part in selectors.split(",")]:
            found += body
    return found


def _rules(css: str) -> list[tuple[list[str], str]]:
    """Every rule of ``css`` — whatever ``@media`` block it stands in — as (its selectors, its declarations)."""
    return [
        ([part.strip() for part in selectors.split(",")], body)
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
    ]


def test_below_48rem_the_bar_is_three_rows_for_both_pickers(preview):
    """
    Reviews F5, W1-2 and W1-3. At 390 px the bar was four rows — a quarter of the window. Below
    48 rem the width links are not drawn (the frame is the window there, so the width classes apply
    from 48 rem only), the second line of the bar is not drawn either, and what is left is laid out
    by name: the way back, the main choice, the language and «Apri»; then the remaining group and
    the flag — the status, then the warning — which says in a few words what that second line
    said. The type picker's five surfaces fill the second row, so the flag of the dense bar is a
    row of its own, in every state: three rows. The hero picker's bar was two rows while it had
    five first screens; with H-E and its three concepts it has nine, which fit beside the language
    at no phone width, so the long bar gives them the second row and the phases, with the flag
    beside them, the third: three rows too, in every state.

    This holds the rules that produce that geometry. The geometry itself — the rows, and the
    status actually drawn — is a browser's to say:
    test_below_48rem_a_browser_draws_the_status_in_the_bar.
    """
    css = (STATIC / "css" / "dev" / "designpreview.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    (phone,) = [block for block in _media_blocks(css, "max-width: 47.99rem") if ".dp-bar" in block]
    # What gives way is the hub's word, the widths and the second line — and nothing else.
    hidden = {selector for selectors, body in _rules(phone) if "display: none" in body for selector in selectors}
    assert hidden == {".dp-bar__group--widths", ".dp-bar__note", ".dp-bar__hub"}
    bar = _declarations(phone, ".dp-bar")
    assert "display: grid" in bar
    rows = re.findall(r'"([^"]+)"', bar)
    assert rows == ["home main lang open", "rest rest rest rest"], "the choices are two rows below 48rem"
    # The long bar — nine choices in the main group — gives that group a row of its own.
    long_bar = _declarations(phone, ".dp-bar--long")
    assert re.findall(r'"([^"]+)"', long_bar) == ["home lang open", "main main main", "rest rest rest"]
    assert "grid-template-columns: auto minmax(0, 1fr) auto" in long_bar
    long_rules = [selectors for selectors, _body in _rules(phone) if any("dp-bar--long" in s for s in selectors)]
    assert long_rules == [[".dp-bar--long"], [".dp-bar--long .dp-bar__group--lang"]], "and changes nothing else"
    for selector, area in (
        (".dp-bar__home", "home"),
        (".dp-bar__group--main", "main"),
        (".dp-bar__group--lang", "lang"),
        (".dp-bar__open", "open"),
        (".dp-bar__rest", "rest"),
    ):
        assert f"grid-area: {area}" in _declarations(phone, selector), selector
    # The flag is drawn there: beside the group of the second row where there is room for it (the
    # hero picker), on a row of its own under the dense bar's five surfaces (the type picker).
    assert "flex-wrap: wrap" in _declarations(phone, ".dp-bar__rest")
    flag = _declarations(phone, ".dp-bar__flag")
    assert "display: flex" in flag and "flex: 1 1 9rem" in flag, "the status stays, beside the second row"
    assert "flex-basis: 100%" in _declarations(phone, ".dp-bar--dense .dp-bar__flag"), "a third row for the type picker"
    # Nothing hides the flag, or a part of it, by another road — at any width.
    outside = css.replace(phone, "")
    for selectors, body in _rules(css):
        if not any("dp-bar__flag" in selector or "dp-bar__rest" in selector for selector in selectors):
            continue
        for road in ("visibility", "opacity", "clip", "overflow", "text-indent", "transparent", "font-size: 0"):
            assert road not in body, (selectors, road)
        if "display: none" in body:
            assert selectors == [".dp-bar__flag"] and body in outside, selectors
    # From 48rem the flag is not drawn: the second line of the bar says the status and the warning in full.
    assert "display: none" in _declarations(outside, ".dp-bar__flag")
    assert "display: contents" in _declarations(outside, ".dp-bar__rest")
    assert "display: flex" in _declarations(outside, ".dp-bar__note")
    # A width is a class on the stage, and means something from 48rem only.
    wide = _media_blocks(css, "min-width: 48rem")
    for width in (1440, 1280, 1024, 768, 430, 390, 375, 360):
        rule = f".dp-stage--w{width} .dp-stage__frame {{ inline-size: {width}px; }}"
        assert any(rule in block for block in wide), width
    elsewhere = css
    for block in wide:
        elsewhere = elsewhere.replace(block, "")
    assert ".dp-stage--w" not in elsewhere, "no width rule outside a 48rem block"
    # The slots the stylesheet places are the ones the two pickers hand over, each exactly once;
    # only the type picker's bar is the dense one.
    from designpreview import services

    hero = services.hero_picker(preview, "h0", "fr", "3", "")
    type_ = services.type_picker(preview, "a", "home", "fr", "")
    for picker in (hero, type_):
        assert sorted(group["slot"] for group in picker["bar"]["groups"]) == ["lang", "main", "rest"]
    assert (hero["bar"]["dense"], type_["bar"]["dense"]) == (False, True)
    assert (hero["bar"]["long"], type_["bar"]["long"]) == (True, False)
    assert len(hero["bar"]["groups"][0]["options"]) == 9 and len(type_["bar"]["groups"][0]["options"]) == 7
    frame = (TEMPLATES / "dev" / "designpreview" / "frame.html").read_text(encoding="utf-8")
    assert 'class="dp-bar__group dp-bar__group--widths"' in frame
    assert (
        '<header class="dp-bar{% if bar.dense %} dp-bar--dense{% endif %}'
        '{% if bar.long %} dp-bar--long{% endif %}" data-dp-bar>'
    ) in frame
    group = (TEMPLATES / "dev" / "designpreview" / "bar_group.html").read_text(encoding="utf-8")
    assert 'class="dp-bar__group dp-bar__group--{{ group.slot }}"' in group
    # The flag follows the group of the second row, and its status hangs on no condition: the only
    # ``if`` of that line is the warning's.
    (line,) = [line.strip() for line in frame.splitlines() if 'class="dp-bar__flag"' in line]
    assert line == (
        '<p class="dp-bar__flag"><span class="dp-bar__flag-status">{{ bar.status_short }}</span>'
        '{% if bar.flag %} <strong class="dp-bar__flag-warning">{{ bar.flag }}</strong>{% endif %}</p>'
    )
    rest = frame[frame.index('<div class="dp-bar__rest">') :]
    assert rest.index('class="dp-bar__flag"') < rest.index("</div>"), "the flag stands in the second row's box"


def test_the_dev_script_is_a_classic_script_without_network_or_storage():
    js = (STATIC / "js" / "dev" / "designpreview.js").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    for forbidden in (
        "fetch(",
        "XMLHttpRequest",
        "sendBeacon",
        "WebSocket",
        "import(",
        "import ",
        "export ",
        "document.cookie",
        "localStorage",
        "sessionStorage",
    ):
        assert forbidden not in code, forbidden
    assert not re.search(r"https?://", js)
    assert scan(js) == []
    for name in ("frame.html", "compare.html", "landing.html", "index.html"):
        page = (TEMPLATES / "dev" / "designpreview" / name).read_text(encoding="utf-8")
        assert 'type="module"' not in page.split("designpreview.js")[0].rsplit("<script", 1)[-1], name


def test_the_templates_are_clean():
    for path in sorted((TEMPLATES / "dev" / "designpreview").glob("*.html")):
        name = path.name
        text = (TEMPLATES / "dev" / "designpreview" / name).read_text(encoding="utf-8")
        assert not re.search(r'\sstyle="', text), name
        assert "<style" not in text, name
        assert not re.search(r'\son[a-z]+="', text), name
        assert not re.search(r"https?://", text), name
        assert scan(text) == [], name
        assert "®" not in text
    for name in ("frame.html", "compare.html", "index.html"):
        page = (TEMPLATES / "dev" / "designpreview" / name).read_text(encoding="utf-8")
        assert page.count("<script") == 1, f"{name}: one script, the dev one, by src"
    landing = (TEMPLATES / "dev" / "designpreview" / "landing.html").read_text(encoding="utf-8")
    assert landing.count("<script") == 1 and landing.count("|json_script:") == 1, "the dev script, and the strip's data"
    assert landing.count("<iframe") == 1, "the landing loads exactly one frame"
    for name in ("index.html", "_row.html", "_strip.html", "_personas.html", "_quick.html"):
        assert "<iframe" not in (TEMPLATES / "dev" / "designpreview" / name).read_text(encoding="utf-8"), name


# --------------------------------------------------------------------------- the bar, in a browser

#: What a browser draws of a picker's bar, once its fonts are in: the status and the warning that
#: can be read — a box with a size, inside the bar and inside the window, visible, on top at its
#: own place, in type of a legible size and at 4.5:1 or more against the ground it stands on —
#: the rows the bar takes (links and words that overlap vertically are one row) and its height.
_BAR_PROBE = """
async () => {
  document.body.getBoundingClientRect();
  await document.fonts.ready;
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const bar = document.querySelector('[data-dp-bar]').getBoundingClientRect();
  const light = (colour) => {
    const [red, green, blue, alpha] = colour.match(/[\\d.]+/g).map(Number);
    if (alpha !== undefined && alpha < 1) { return null; }
    const linear = (value) => (value / 255 <= 0.03928 ? value / 255 / 12.92 : ((value / 255 + 0.055) / 1.055) ** 2.4);
    return 0.2126 * linear(red) + 0.7152 * linear(green) + 0.0722 * linear(blue);
  };
  const ground = (element) => {
    for (let node = element; node; node = node.parentElement) {
      const colour = getComputedStyle(node).backgroundColor;
      if (light(colour) !== null) { return colour; }
    }
    return 'rgb(255, 255, 255)';
  };
  const contrast = (element) => {
    const ink = light(getComputedStyle(element).color);
    if (ink === null) { return 0; }
    const [high, low] = [ink, light(ground(element))].sort((a, b) => b - a);
    return (high + 0.05) / (low + 0.05);
  };
  const read = (selector) => Array.from(document.querySelectorAll(selector)).filter((element) => {
    const box = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    if (!(box.width > 0 && box.height > 0)) { return false; }
    const first = element.getClientRects()[0];
    const top = document.elementFromPoint(first.left + first.width / 2, first.top + first.height / 2);
    return style.visibility === 'visible' && Number(style.opacity) > 0
      && parseFloat(style.fontSize) >= 11 && contrast(element) >= 4.5
      && box.left >= bar.left - 0.5 && box.right <= bar.right + 0.5
      && box.top >= bar.top - 0.5 && box.bottom <= bar.bottom + 0.5
      && box.right <= window.innerWidth + 0.5
      && element.contains(top);
  }).map((element) => element.textContent.trim());
  const boxes = Array.from(document.querySelectorAll(
    '[data-dp-bar] a, .dp-bar__what, .dp-bar__status, .dp-bar__warning, .dp-bar__flag-status, .dp-bar__flag-warning'
  )).map((element) => element.getBoundingClientRect()).filter((box) => box.height > 0)
    .sort((a, b) => a.top - b.top);
  let rows = 0;
  let floor = -1;
  for (const box of boxes) {
    if (box.top >= floor - 1) { rows += 1; floor = box.bottom; } else { floor = Math.max(floor, box.bottom); }
  }
  const main = Array.from(document.querySelectorAll('.dp-bar__group--main a')).map((link) => link.getBoundingClientRect());
  return {
    status: read('.dp-bar__status, .dp-bar__flag-status'),
    warning: read('.dp-bar__warning, .dp-bar__flag-warning'),
    widths: read('.dp-bar__group--widths a').length,
    main: [
      new Set(main.map((box) => Math.round(box.top))).size,
      main.filter((box) => box.left < -0.5 || box.right > window.innerWidth + 0.5 || box.width < 24 || box.height < 24).length,
    ],
    rows: rows,
    height: Math.round(bar.height),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}
"""


@pytest.fixture
def chromium(monkeypatch):
    """A headless Chromium of this test's own — skipped where none is installed, like the other browser tests."""
    playwright = pytest.importorskip("playwright.sync_api")
    # Playwright's synchronous API keeps an event loop on this thread; Django would otherwise
    # refuse the database to whatever runs beside it.
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    with playwright.sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield browser
        browser.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_below_48rem_a_browser_draws_the_status_in_the_bar(chromium, served):
    """
    Review W1-2, the check the markup tests could not be. Below 48 rem the second line of the bar
    is not drawn, and with it went the status: «non approvato» was in the HTML of every state
    and on the screen of none — in the very window Chrome's device toolbar gives. This
    opens the two pickers in a browser at the four phone widths of the review and at the last
    pixel before 48 rem, and fails unless the status can be read in the bar, with the warning
    after it when there is one.

    Review W1-3, measured rather than declared: both bars are three rows there, in every state
    — warning or none, framed or not, on disk or not — so the frame keeps one height
    from a choice to the next; and the hero picker's nine first screens stand on one line of the
    bar, none of them outside the window. At 48 rem the second line is back and says both in full.
    """
    gate0, research, control = "non approvata", "non approvato", "non una proposta"
    pickers = {
        # the picker → (its rows below 48rem, [(query, the status in short, the warning in short)])
        PICKER: (
            3,
            [
                ("variant=hb", gate0, ""),
                ("variant=hb&lang=ar", gate0, "da non firmare come /ar/"),
                ("variant=hc", research, ""),
                ("variant=hc&lang=ar", research, "da non firmare come /ar/"),
                ("variant=hc&phase=interim", research, "combinazione inesistente"),
                ("variant=h0&lang=ar&phase=interim", gate0, "il file manca"),
                ("variant=he", research, "il file manca"),
                ("variant=e2&lang=ar", research, "combinazione inesistente"),
            ],
        ),
        TYPE: (
            3,
            [
                ("system=a", research, ""),
                ("system=a&lang=ar", research, "caratteri arabi provvisori (O10)"),
                ("system=v4", control, ""),
                ("system=a&surface=menu&lang=ar", research, "combinazione inesistente"),
                ("system=c", research, "il file manca"),
            ],
        ),
    }
    narrow, wide = (360, 375, 390, 430, 767), 768
    page = chromium.new_page(viewport={"width": wide, "height": 800}, device_scale_factor=1)
    try:
        for picker, (rows, states) in pickers.items():
            heights: dict[int, set[int]] = {width: set() for width in narrow}
            for query, status, warning in states:
                where = f"{picker}?{query}"
                page.set_viewport_size({"width": wide, "height": 800})
                page.goto(f"{served}{where}", wait_until="load")
                seen = page.evaluate(_BAR_PROBE)
                # From 48rem: the second line, in full, and the widths.
                assert len(seen["status"]) == 1 and seen["status"][0].endswith(f" — {status}"), (where, wide, seen)
                assert len(seen["warning"]) == (1 if warning else 0), (where, wide, seen)
                assert seen["widths"] == 9 and seen["overflow"] <= 0, (where, wide, seen)
                for width in narrow:
                    page.set_viewport_size({"width": width, "height": 800})
                    seen = page.evaluate(_BAR_PROBE)
                    assert seen["status"] == [status], (where, width, seen)
                    assert seen["warning"] == ([warning] if warning else []), (where, width, seen)
                    assert seen["rows"] == rows, (where, width, seen)
                    assert seen["widths"] == 0 and seen["overflow"] <= 0, (where, width, seen)
                    assert seen["main"] == [1, 0], (where, width, seen)
                    heights[width].add(seen["height"])
            for width, found in heights.items():
                assert len(found) == 1, f"{picker} at {width} px: the bar is not one height: {sorted(found)}"
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_on_a_phone_a_browser_draws_each_warning_of_the_hub_beside_its_own_link(chromium, served):
    """
    Review W1-4, measured. At 360, 375 and 390 px five warnings out of six stood on the line of
    the link that follows theirs. Each one is now on the line of its own link, right after it.
    """
    probe = """
    async () => {
      document.body.getBoundingClientRect();
      await document.fonts.ready;
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      return Array.from(document.querySelectorAll('.dp-link__note')).map((note) => {
        const own = note.previousElementSibling.getBoundingClientRect();
        const box = note.getBoundingClientRect();
        return {
          link: note.previousElementSibling.textContent.trim(),
          line: box.top < own.bottom && box.bottom > own.top,
          after: Math.round(box.left - own.right),
          height: Math.round(box.height),
        };
      });
    }
    """
    page = chromium.new_page(viewport={"width": 390, "height": 800}, device_scale_factor=1)
    try:
        page.goto(f"{served}{HUB}", wait_until="load")
        for width in (360, 375, 390, 430):
            page.set_viewport_size({"width": width, "height": 800})
            notes = page.evaluate(probe)
            assert [note["link"] for note in notes] == ["ar · fase 3"] * 3, (width, notes)
            for note in notes:
                assert note["line"] and 0 <= note["after"] <= 12 and note["height"] > 0, (width, note)
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_browser_draws_the_two_phones_side_by_side_each_with_its_own_scroll(chromium, served):
    """
    X-3, measured. At 1440 × 900 the two pages are drawn at the same time, side by side on one
    line, each 390 CSS pixels wide inside its frame and as tall as the window allows; scrolling
    one moves nothing in the other; nothing leaves the window and the page does not scroll
    sideways; the policy refuses nothing. At 800 × 900 — from 48 rem the bar's line is drawn, below
    54 rem the two stand one under the other — each is still 390 px wide and the line says «prima»
    and «poi», not left and right (review HC-2). At 390 × 844 they stand one under the other, each
    caption still saying the status, and nothing overflows.
    """
    probe = """
    async () => {
      document.body.getBoundingClientRect();
      await document.fonts.ready;
      const frames = Array.from(document.querySelectorAll('iframe.dp-compare__frame'));
      const boxes = frames.map((frame) => frame.getBoundingClientRect());
      const inner = frames.map((frame) => frame.contentWindow.innerWidth);
      frames[0].contentWindow.scrollTo(0, 600);
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      const statuses = Array.from(document.querySelectorAll('.dp-compare__status')).filter((element) => {
        const box = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        return box.width > 0 && box.height > 0 && style.visibility === 'visible' && Number(style.opacity) > 0;
      }).map((element) => element.textContent.trim());
      return {
        boxes: boxes.map((box) => [Math.round(box.left), Math.round(box.top), Math.round(box.width), Math.round(box.height)]),
        inner: inner,
        scrolled: frames.map((frame) => Math.round(frame.contentWindow.scrollY)),
        statuses: statuses,
        right: Math.round(Math.max(...boxes.map((box) => box.right)) - window.innerWidth),
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      };
    }
    """
    refused: list[str] = []
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page.on(
        "console", lambda message: refused.append(message.text) if "Content Security Policy" in message.text else None
    )
    try:
        page.goto(f"{served}{COMPARE}?pair=mes-pieces&lang=fr", wait_until="load")
        seen = page.evaluate(probe)
        (left, top, width, height), (left_2, top_2, width_2, height_2) = seen["boxes"]
        assert seen["inner"] == [390, 390], seen
        assert (width, width_2) == (392, 392) and top == top_2 and height == height_2 > 600, seen
        assert left_2 - (left + width) == 32, seen
        assert seen["scrolled"] == [600, 0], "scrolling one frame moved the other"
        assert seen["statuses"] == [NOT_APPROVED, NOT_APPROVED], seen
        assert seen["right"] <= 0 and seen["overflow"] <= 0, seen
        page.set_viewport_size({"width": 800, "height": 900})
        page.goto(f"{served}{COMPARE}?pair=mes-pieces&lang=fr", wait_until="load")
        seen = page.evaluate(probe)
        (left, top, width, height), (left_2, top_2, width_2, height_2) = seen["boxes"]
        assert seen["inner"] == [390, 390] and top_2 > top + height, seen
        assert seen["statuses"] == [NOT_APPROVED, NOT_APPROVED], seen
        assert seen["right"] <= 0 and seen["overflow"] <= 0, seen
        order = page.locator(".dp-bar__order")
        assert order.is_visible(), "from 48 rem the bar says what is compared and in what order"
        assert "prima la seconda ondata, poi la terza ondata" in order.inner_text()
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(f"{served}{COMPARE}?pair=mes-pieces&lang=fr", wait_until="load")
        seen = page.evaluate(probe)
        (left, top, width, height), (left_2, top_2, width_2, height_2) = seen["boxes"]
        assert top_2 > top + height, "below 54rem the two stand one under the other"
        assert width <= 392 and width_2 <= 392 and left >= 0 and left_2 >= 0, seen
        assert seen["statuses"] == [NOT_APPROVED, NOT_APPROVED], seen
        assert seen["right"] <= 0 and seen["overflow"] <= 0, seen
        assert refused == [], refused
    finally:
        page.close()


# --------------------------------------------------------------------------- the live product, in a browser

#: Installed in every frame before its scripts: the policy violations the document meets, kept on it.
_VIOLATIONS = """
window.__violations = [];
document.addEventListener('securitypolicyviolation', (event) => {
  window.__violations.push(event.violatedDirective + ' ' + event.blockedURI);
});
"""

_LANDING_PROBE = """
async () => {
  await document.fonts.ready;
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const strip = document.querySelector('[data-dp-strip]').getBoundingClientRect();
  const frames = Array.from(document.querySelectorAll('iframe'));
  const inner = frames[0];
  const doc = inner.contentDocument;
  const paint = performance.getEntriesByType('paint').find((entry) => entry.name === 'first-contentful-paint');
  return {
    strip: [Math.round(strip.top), Math.round(strip.height), Math.round(strip.width)],
    frames: frames.length,
    box: [Math.round(inner.getBoundingClientRect().width), Math.round(inner.getBoundingClientRect().height)],
    inner: inner.contentWindow.innerWidth,
    path: inner.contentWindow.location.pathname,
    lang: doc ? doc.documentElement.lang : null,
    homeBody: doc ? doc.body.className : null,
    fcp: paint ? Math.round(paint.startTime) : null,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    violations: window.__violations.concat(inner.contentWindow.__violations || []),
  };
}
"""


def _console(page, kept: list[str]) -> None:
    page.on(
        "console",
        lambda message: (
            kept.append(message.text)
            if any(words in message.text for words in ("Content Security Policy", "Refused to", "X-Frame-Options"))
            else None
        ),
    )


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_landing_draws_one_frame_of_the_real_home_under_a_strip_of_40_px(chromium, dev_server):
    """
    Plan §4.6: the strip paints in at most a second and the landing loads exactly one frame; the
    frame holds the real home — this origin, so the policy lets it be framed — and nothing is
    refused, in the landing or in the page it frames. At 1440 × 900 and at 390 × 844, in French and
    in Arabic; the strip is 40 px and the window never scrolls sideways.

    Measured on a running server, as the owner meets it: the first request after a server starts
    pays Django's one-time costs — the URLconf, every template compiled — which belong to no page
    (on a loaded machine they alone passed the second, fix round 1). One request warms it first.
    """
    refused: list[str] = []
    for warm in (f"{LANDING}?page=/fr/", "/fr/", f"{LANDING}?page=/ar/", "/ar/"):
        with urllib.request.urlopen(f"{dev_server}{warm}", timeout=60) as response:
            response.read()
    context = chromium.new_context(device_scale_factor=1)
    context.add_init_script(_VIOLATIONS)
    page = context.new_page()
    _console(page, refused)
    try:
        for width, height in ((1440, 900), (390, 844)):
            for lang in ("fr", "ar"):
                page.set_viewport_size({"width": width, "height": height})
                page.goto(f"{dev_server}{LANDING}?page=/{lang}/", wait_until="load")
                seen = page.evaluate(_LANDING_PROBE)
                assert seen["frames"] == 1, seen
                assert seen["strip"] == [0, 40, width], seen
                assert seen["path"] == f"/{lang}/" and seen["lang"] == lang, seen
                assert "home" in seen["homeBody"], seen
                assert seen["inner"] == width and seen["box"] == [width, height - 40], seen
                assert seen["fcp"] is not None and seen["fcp"] <= 1000, seen
                assert seen["overflow"] <= 0, seen
                assert seen["violations"] == [], seen
        # The phone frame: 390 CSS pixels of page in a wide window.
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(f"{dev_server}{LANDING}?frame=phone", wait_until="load")
        seen = page.evaluate(_LANDING_PROBE)
        assert seen["inner"] == 390 and seen["frames"] == 1, seen
        assert refused == [], refused
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_strip_follows_the_page_the_frame_navigates_to(chromium, dev_server):
    """
    When the page in the frame moves, the strip says that page's state, offers its languages, and
    «Apri a parte» and the frame links point at it; the address bar keeps it, so a reload frames it
    again. The frame changes from the window to a phone without reloading the page it holds.
    """
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page.goto(f"{dev_server}{LANDING}", wait_until="load")
        page.wait_for_function(
            "() => document.querySelector('iframe[data-dp-frame]').title === 'La home — V4 + fondation'"
        )
        assert page.title() == "La home · V5 dal vivo · Italy Legal Entry™", "named after the page, not its path"
        frame = page.frame_locator("iframe[data-dp-frame]")
        with page.expect_event("framenavigated", predicate=lambda f: f.url.endswith("/fr/le-projet/")):
            page.evaluate(
                "() => document.querySelector('iframe[data-dp-frame]').contentWindow.location.assign('/fr/le-projet/')"
            )
        page.wait_for_function("() => new URLSearchParams(location.search).get('page') === '/fr/le-projet/'")
        seen = page.evaluate(
            """() => ({
              open: document.querySelector('.dp-strip__open[data-dp-open]').getAttribute('href'),
              langs: Array.from(document.querySelectorAll('.dp-strip__group--lang a[data-dp-lang]')).filter((a) => !a.hidden).map((a) => a.getAttribute('data-dp-lang')),
              ar: document.querySelector('.dp-strip__group--lang a[data-dp-lang="ar"]').getAttribute('href'),
              phone: document.querySelector('.dp-strip__group a[data-dp-frame-mode="phone"]').getAttribute('href'),
              state: document.querySelector('[data-dp-state-label]').textContent,
              field: document.querySelector('input[data-dp-lang-field]').value,
              frameTitle: document.querySelector('iframe[data-dp-frame]').title,
              windowTitle: document.title,
            })"""
        )
        assert seen == {
            "open": "/fr/le-projet/",
            "langs": ["fr", "ar"],
            "ar": f"{LANDING}?page=/ar/le-projet/",
            "phone": f"{LANDING}?page=/fr/le-projet/&frame=phone",
            "state": "V4 + fondation",
            "field": "fr",
            "frameTitle": "Il progetto — V4 + fondation",
            "windowTitle": "Il progetto · V5 dal vivo · Italy Legal Entry™",
        }, seen
        # To the login: it and en come back.
        with page.expect_event("framenavigated", predicate=lambda f: f.url.endswith("/fr/compte/login/")):
            page.evaluate(
                "() => document.querySelector('iframe[data-dp-frame]').contentWindow.location.assign('/fr/compte/login/')"
            )
        page.wait_for_function("() => new URLSearchParams(location.search).get('page') === '/fr/compte/login/'")
        langs = page.evaluate(
            "() => Array.from(document.querySelectorAll('.dp-strip__group--lang a[data-dp-lang]')).filter((a) => !a.hidden).map((a) => a.getAttribute('data-dp-lang'))"
        )
        assert langs == ["fr", "ar", "it", "en"], langs
        # The phone, without reloading what the frame holds.
        page.evaluate(
            "() => { document.querySelector('iframe[data-dp-frame]').contentWindow.__kept = 'same document'; }"
        )
        page.locator('.dp-strip__group a[data-dp-frame-mode="phone"]').click()
        seen = page.evaluate(
            """() => ({
              phone: document.querySelector('[data-dp-stage]').classList.contains('dp-live__stage--phone'),
              kept: document.querySelector('iframe[data-dp-frame]').contentWindow.__kept,
              inner: document.querySelector('iframe[data-dp-frame]').contentWindow.innerWidth,
              search: location.search,
            })"""
        )
        assert seen == {
            "phone": True,
            "kept": "same document",
            "inner": 390,
            "search": "?page=/fr/compte/login/&frame=phone",
        }, seen
        assert frame.locator("form").count() >= 1
        # A reload frames the same page, in the same frame.
        page.reload(wait_until="load")
        assert (
            page.evaluate("() => document.querySelector('iframe[data-dp-frame]').getAttribute('src')")
            == "/fr/compte/login/"
        )
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_an_old_anchor_of_the_hub_opens_the_archive_at_that_anchor(chromium, dev_server):
    page = chromium.new_page(viewport={"width": 1440, "height": 900})
    try:
        page.goto(f"{dev_server}{LANDING}#g-he", wait_until="load")
        page.wait_for_url(f"{dev_server}{ARCHIVE}#g-he")
        assert page.locator("#g-he").count() == 1
        page.goto(f"{dev_server}{LANDING}#elsewhere", wait_until="load")
        assert page.url == f"{dev_server}{LANDING}#elsewhere", "another fragment is left alone"
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_index_never_holds_more_than_one_pair_of_frames(chromium, dev_server):
    """
    Plan §4.1, RTE-m9: 8780 has eight database slots and a frame is a page and its requests. The
    index's script holds at most one pair — the desktop and the phone of one address — unloading
    the pair it holds before it loads the next; closing the viewer unloads it, and a pressed frame
    button releases its own frame (review W1-P, accessibility m5). Counted by an observer from the
    first frame to the last, so that a third frame for a moment would be seen. And the server is
    asked for the pair that remains, not for every pair on the way (performance P-2): ten addresses
    × pair, opened back to back by script, cost at most two frame documents.
    """
    refused: list[str] = []
    context = chromium.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    context.add_init_script(_VIOLATIONS)
    page = context.new_page()
    _console(page, refused)
    documents: list[str] = []
    page.on(
        "request",
        lambda request: (
            documents.append(request.url)
            if request.resource_type == "document" and request.frame != page.main_frame
            else None
        ),
    )
    try:
        page.goto(f"{dev_server}{INDEX}", wait_until="load")
        assert page.locator("iframe").count() == 0, "no frame before one is asked for"
        page.evaluate(
            """() => {
              window.__most = 0;
              new MutationObserver(() => {
                window.__most = Math.max(window.__most, document.querySelectorAll('iframe').length);
              }).observe(document.body, {childList: true, subtree: true});
            }"""
        )
        assert page.locator("#pubbliche details.dp-index__fold").get_attribute("open") is not None, "open by default"
        # A first open is asked for at the next task, not after the 150 ms an unload costs (review W1-P,
        # performance r2 P-4; CD condition C7): timed from the click's own timeStamp to the src.
        page.evaluate(
            """() => {
              window.__clickAt = null;
              window.__srcAt = null;
              document.addEventListener('click', (event) => {
                if (window.__clickAt === null && event.target.closest && event.target.closest('a[data-dp-pair]')) {
                  window.__clickAt = event.timeStamp;
                }
              }, true);
              new MutationObserver((records) => {
                for (const record of records) {
                  if (window.__srcAt === null && record.target.getAttribute('data-dp-kind') === 'desktop'
                      && record.target.getAttribute('src')) {
                    window.__srcAt = performance.now();
                  }
                }
              }).observe(document.body, {attributes: true, attributeFilter: ['src'], subtree: true});
            }"""
        )
        true_size = page.locator("dialog[data-dp-viewer] button[data-dp-true-size]")
        assert true_size.is_disabled(), "«1:1» acts on a desktop frame, and there is none (a11y r2 n2)"

        def frames():
            return page.evaluate(
                "() => Array.from(document.querySelectorAll('iframe')).map((f) => [f.getAttribute('data-dp-kind'), f.getAttribute('data-dp-src')])"
            )

        def requested(count):
            page.wait_for_function(
                f"() => Array.from(document.querySelectorAll('iframe')).filter((f) => f.getAttribute('src')).length === {count}"
            )

        page.locator('#p-home a[data-dp-pair="/fr/"][data-dp-kind="desktop"]').click()
        page.wait_for_function("() => document.querySelector('dialog[data-dp-viewer]').open")
        assert frames() == [["desktop", "/fr/"]]
        requested(1)
        waited = page.evaluate("() => window.__srcAt - window.__clickAt")
        assert 0 <= waited < 100, f"a first open waited {waited} ms for its frame (P-4)"
        assert true_size.is_enabled()
        page.locator('dialog[data-dp-viewer] button[data-dp-add="phone"]').click()
        assert frames() == [["desktop", "/fr/"], ["phone", "/fr/"]], "the pair: one address, two frames"
        requested(2)
        page.evaluate('() => document.querySelector(\'#p-home a[data-dp-pair="/fr/"][data-dp-kind="phone"]\').click()')
        assert len(frames()) == 2, "a frame of the pair is never doubled"
        # A pressed frame button releases its own frame, and says so.
        page.locator('dialog[data-dp-viewer] button[data-dp-add="phone"]').click()
        assert frames() == [["desktop", "/fr/"]]
        assert (
            page.locator('dialog[data-dp-viewer] button[data-dp-add="phone"]').get_attribute("aria-pressed") == "false"
        )
        page.locator('dialog[data-dp-viewer] button[data-dp-add="phone"]').click()
        assert frames() == [["desktop", "/fr/"], ["phone", "/fr/"]]
        # Another address while the pair is open (the dialog is modal: the click is the script's own).
        page.evaluate(
            '() => document.querySelector(\'#p-faq a[data-dp-pair="/fr/faq/"][data-dp-kind="desktop"]\').click()'
        )
        assert frames() == [["desktop", "/fr/faq/"]], "the pair that was open went before the next came"
        requested(1)
        page.wait_for_load_state("load")
        title = page.locator("[data-dp-viewer-title]").inner_text()
        assert title == "Le domande frequenti · fr"
        assert page.locator("[data-dp-viewer-alone]").get_attribute("href") == "/fr/faq/"
        page.keyboard.press("Escape")
        page.wait_for_function(
            "() => !document.querySelector('dialog[data-dp-viewer]').open && !document.querySelector('iframe')"
        )
        assert frames() == [], "closing the viewer unloads its frames"
        # Ten addresses × pair, back to back: the server is asked for the last pair only.
        documents.clear()
        page.evaluate(
            """() => {
              const rows = Array.from(document.querySelectorAll('#pubbliche li.dp-row')).slice(1, 11);
              for (const row of rows) {
                row.querySelector('a[data-dp-kind="desktop"]').click();
                row.querySelector('a[data-dp-kind="phone"]').click();
              }
            }"""
        )
        requested(2)
        page.wait_for_timeout(600)
        assert len(documents) <= 2, documents
        assert len(frames()) == 2
        page.locator("dialog[data-dp-viewer] button[data-dp-close]").click()
        assert frames() == []
        page.locator('#p-login a[data-dp-pair="/ar/compte/login/"][data-dp-kind="phone"]').click()
        assert frames() == [["phone", "/ar/compte/login/"]]
        assert true_size.is_disabled(), "a phone alone: «1:1» has nothing to act on"
        page.locator("dialog[data-dp-viewer] button[data-dp-close]").click()
        assert frames() == []
        assert page.evaluate("() => window.__most") == 2
        assert page.evaluate("() => window.__violations") == [] and refused == [], refused
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_persona_enters_and_leaves_from_the_strip(chromium, dev_server, accounts, this_database):
    """«Personas» → «Entrer»: the landing frames the persona's first page and the strip says who is in; «Sortir» ends it."""
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page.goto(f"{dev_server}{LANDING}", wait_until="load")
        page.locator(".dp-strip__menu--personas > summary").click()
        page.locator(f'.dp-strip form[action="{ENTER}qa-doc-person/"] button').click()
        page.wait_for_url(f"{dev_server}{LANDING}?page=/fr/espace-reserve/")
        page.wait_for_load_state("load")
        assert page.locator(".dp-strip__menu--personas .dp-strip__dot").count() == 1
        assert "Personne avec dossier" in page.locator(".dp-strip__menu--personas > summary").inner_text()
        assert page.evaluate(
            "() => document.querySelector('iframe[data-dp-frame]').contentWindow.location.pathname"
        ).startswith("/fr/espace-reserve/")
        cookies = {cookie["name"] for cookie in page.context.cookies()}
        assert "ile_v5_sessionid" in cookies and "sessionid" not in cookies
        page.locator(".dp-strip__menu--personas > summary").click()
        page.locator(f'.dp-strip form[action="{EXIT}"] button').click()
        page.wait_for_url(f"{dev_server}{LANDING}?page=/fr/")
        assert page.locator(".dp-strip__dot").count() == 0
    finally:
        page.close()


#: What the landing's frame holds, read from inside it (same origin), and what the stage shows.
_FRAMED = """
() => {
  const frame = document.querySelector('iframe[data-dp-frame]');
  let path = 'unreadable', forms = 0, violations = [];
  try {
    path = frame.contentWindow.location.pathname;
    forms = frame.contentDocument.querySelectorAll('form').length;
    violations = frame.contentWindow.__violations || [];
  } catch (error) {}
  const message = document.querySelector('[data-dp-blocked]');
  return {path, forms, blocked: !message.hidden, frameShown: getComputedStyle(frame).display !== 'none',
          dot: !!document.querySelector('.dp-strip__dot'), violations: window.__violations.concat(violations)};
}
"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_redirect_and_a_form_s_answer_render_in_the_frame_without_a_policy_violation(chromium, dev_server):
    """
    Review W1-P B1 (security M1). Signed out, a reserved page answers with a redirect to the sign-in:
    under ``upgrade-insecure-requests`` Chromium upgraded that hop to https and refused it, and the
    frame stayed blank. And a form's answer was never framed. Now the sign-in renders in the frame,
    and so does its answer to an empty submission — with 0 policy violations, in the landing or in
    the frame.
    """
    refused: list[str] = []
    context = chromium.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    context.add_init_script(_VIOLATIONS)
    page = context.new_page()
    _console(page, refused)
    try:
        page.goto(f"{dev_server}{LANDING}?page=/fr/espace-reserve/", wait_until="load")
        page.wait_for_function(
            "() => { try { return document.querySelector('iframe[data-dp-frame]').contentWindow.location.pathname === '/fr/compte/login/'; } catch (e) { return false; } }"
        )
        page.wait_for_load_state("load")
        seen = page.evaluate(_FRAMED)
        assert seen["path"] == "/fr/compte/login/" and seen["forms"] >= 1 and not seen["blocked"], seen
        assert page.evaluate("() => new URLSearchParams(location.search).get('page')").startswith("/fr/compte/login/")
        # Signed out, on the sign-in: the way in without a password, and the page «Entrer» opens (C4).
        assert page.locator("[data-dp-hint]").is_visible()
        assert set(
            page.locator("input[data-dp-next-field]").evaluate_all("(fields) => fields.map((f) => f.value)")
        ) == {"/fr/espace-reserve/"}
        # The sign-in submitted empty, inside the frame: its answer is a page of the frame too.
        with page.expect_event("framenavigated", predicate=lambda frame: frame != page.main_frame):
            page.evaluate(
                "() => document.querySelector('iframe[data-dp-frame]').contentDocument.querySelector('form[method=post]').submit()"
            )
        page.wait_for_load_state("load")
        page.wait_for_timeout(300)
        seen = page.evaluate(_FRAMED)
        assert seen["path"] == "/fr/compte/login/" and seen["forms"] >= 1, seen
        assert not seen["blocked"] and seen["frameShown"], seen
        assert seen["violations"] == [] and refused == [], (seen, refused)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_product_s_own_sign_out_in_the_frame_ends_on_the_home_and_the_strip_follows(
    chromium, dev_server, accounts, this_database
):
    """
    Review W1-P B1 (c) and UX m9. As a persona, the product's own «Se déconnecter» inside the frame
    posts to the sign-out and is answered with a redirect to the home: it left a blank frame, two
    policy violations, and a strip that still named the persona. Now the home renders, and the
    landing is served again — the strip names nobody.
    """
    refused: list[str] = []
    context = chromium.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    context.add_init_script(_VIOLATIONS)
    page = context.new_page()
    _console(page, refused)
    try:
        page.goto(f"{dev_server}{LANDING}", wait_until="load")
        page.locator(".dp-strip__menu--personas > summary").click()
        page.locator(f'.dp-strip form[action="{ENTER}qa-doc-person/"] button').click()
        page.wait_for_url(f"{dev_server}{LANDING}?page=/fr/espace-reserve/")
        assert page.locator(".dp-strip__dot").count() == 1
        page.goto(f"{dev_server}{LANDING}?page=/fr/compte/logout/", wait_until="load")
        page.wait_for_load_state("load")
        page.evaluate(
            "() => document.querySelector('iframe[data-dp-frame]').contentDocument.querySelector('main form[method=post] [type=submit]').click()"
        )
        page.wait_for_url(f"{dev_server}{LANDING}?page=/fr/")
        page.wait_for_load_state("load")
        page.wait_for_function(
            "() => { try { return document.querySelector('iframe[data-dp-frame]').contentWindow.location.pathname === '/fr/'; } catch (e) { return false; } }"
        )
        seen = page.evaluate(_FRAMED)
        assert seen["path"] == "/fr/" and not seen["blocked"] and not seen["dot"], seen
        assert seen["violations"] == [] and refused == [], (seen, refused)
        assert page.locator(".dp-strip__menu--personas > summary").inner_text().strip() == "Personas"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_page_the_frame_cannot_hold_is_said_never_a_blank_frame(chromium, dev_server):
    """
    Review W1-P B1, item 2. Some addresses can never be framed — the back-office, the preview's own
    pages, another site. When the frame is refused one, the stage says so instead of a blank frame:
    the page alone, at the address the link asked for, and the way back to the page before.
    """
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        page.goto(f"{dev_server}{LANDING}?page=/fr/le-projet/", wait_until="load")
        page.wait_for_load_state("load")
        page.evaluate(
            """() => {
              const doc = document.querySelector('iframe[data-dp-frame]').contentDocument;
              const link = doc.createElement('a');
              link.href = '/backoffice/login/';
              link.textContent = 'back-office';
              doc.body.appendChild(link);
              link.click();
            }"""
        )
        page.wait_for_function("() => !document.querySelector('[data-dp-blocked]').hidden", timeout=15000)
        seen = page.evaluate(
            """() => ({
              frameShown: getComputedStyle(document.querySelector('iframe[data-dp-frame]')).display !== 'none',
              alone: document.querySelector('[data-dp-blocked-open]').getAttribute('href'),
              aloneShown: !document.querySelector('[data-dp-blocked-open]').hidden,
              back: document.querySelector('[data-dp-blocked-back]').getAttribute('href'),
              role: document.querySelector('[data-dp-blocked]').getAttribute('role'),
              text: document.querySelector('[data-dp-blocked]').innerText,
            })"""
        )
        assert not seen["frameShown"] and seen["role"] == "alert", seen
        assert seen["aloneShown"] and seen["alone"].endswith("/backoffice/login/"), seen
        assert seen["back"] == f"{LANDING}?page=/fr/le-projet/", seen
        assert "Questa pagina non si apre nella cornice." in seen["text"]
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_viewer_shows_both_frames_of_the_pair_at_the_owner_s_widths(chromium, dev_server):
    """
    Review W1-P M1: at 1440 the desktop frame was drawn at its true size and the phone sat past the
    window's edge. The desktop frame still lays its page out at 1440 CSS pixels, drawn scaled to fit
    beside the phone; «1:1» draws it at its true size.
    """
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    try:
        for width, height in ((1440, 900), (1280, 800)):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"{dev_server}{INDEX}", wait_until="load")
            page.locator('#p-home a[data-dp-pair="/fr/"][data-dp-kind="desktop"]').click()
            page.locator('dialog[data-dp-viewer] button[data-dp-add="phone"]').click()
            page.wait_for_function(
                "() => Array.from(document.querySelectorAll('dialog iframe')).every((f) => f.getAttribute('src'))"
            )
            page.wait_for_load_state("load")
            boxes = page.evaluate(
                """() => Object.fromEntries(Array.from(document.querySelectorAll('dialog iframe')).map((f) => {
                  const r = f.getBoundingClientRect();
                  return [f.getAttribute('data-dp-kind'), {left: r.left, right: r.right, width: r.width, inner: f.contentWindow.innerWidth}];
                }))"""
            )
            for kind in ("desktop", "phone"):
                assert boxes[kind]["width"] > 0 and boxes[kind]["left"] >= 0, (width, boxes)
                assert boxes[kind]["right"] <= width, (width, kind, boxes)
            assert boxes["desktop"]["inner"] == 1440 and boxes["phone"]["inner"] == 390, boxes
            assert boxes["desktop"]["right"] <= boxes["phone"]["left"], "side by side"
            page.locator("dialog[data-dp-viewer] button[data-dp-true-size]").click()
            true_width = page.evaluate(
                "() => document.querySelector('dialog iframe[data-dp-kind=desktop]').getBoundingClientRect().width"
            )
            assert round(true_width) == 1442, true_width
            page.keyboard.press("Escape")
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_no_focused_control_of_the_index_hides_under_its_sticky_strip(chromium, dev_server):
    """
    Review W1-P, accessibility B1 (WCAG 2.4.11; plan §1.6): Shift+Tab from the index's last control
    back to the strip left controls entirely under the sticky strip at 390. The scroller keeps the
    strip's height free; walked at 390 × 844 and 1440 × 900, no focused control's box meets the
    strip's.
    """
    page = chromium.new_page(device_scale_factor=1)
    try:
        for width, height in ((390, 844), (1440, 900)):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"{dev_server}{INDEX}", wait_until="load")
            page.evaluate(
                "() => { const all = Array.from(document.querySelectorAll('main a, main button, main summary')); all[all.length - 1].focus(); }"
            )
            hidden: list[str] = []
            for _ in range(900):
                page.keyboard.press("Shift+Tab")
                seen = page.evaluate(
                    """() => {
                      const strip = document.querySelector('[data-dp-strip]');
                      const active = document.activeElement;
                      if (!active || active === document.body) return {skip: true};
                      if (strip.contains(active)) return {inStrip: true};
                      const a = active.getBoundingClientRect(), s = strip.getBoundingClientRect();
                      return {under: a.top < s.bottom - 0.5 && a.bottom > s.top, name: (active.textContent || active.tagName).trim().slice(0, 40)};
                    }"""
                )
                if seen.get("inStrip"):
                    break
                if seen.get("under"):
                    hidden.append(seen["name"])
            else:
                raise AssertionError("the walk never reached the strip")
            assert hidden == [], (width, hidden)
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_choosing_the_frame_from_altro_keeps_the_focus_on_altro(chromium, dev_server):
    """
    Review W1-P, accessibility M1 (WCAG 2.4.3, 2.4.7): from 48 to 80 rem the frame is chosen in
    «Altro», and closing the menu dropped the focus to <body>. It goes back to «Altro»'s summary.
    """
    page = chromium.new_page(viewport={"width": 1024, "height": 768}, device_scale_factor=1)
    try:
        page.goto(f"{dev_server}{LANDING}", wait_until="load")
        page.locator(".dp-strip__narrow > summary").focus()
        page.keyboard.press("Enter")
        page.locator('.dp-strip__narrow a[data-dp-frame-mode="phone"]').focus()
        page.keyboard.press("Enter")
        seen = page.evaluate(
            """() => ({
              focused: document.activeElement.matches('.dp-strip__narrow > summary'),
              open: document.querySelector('.dp-strip__narrow').open,
              phone: document.querySelector('[data-dp-stage]').classList.contains('dp-live__stage--phone'),
            })"""
        )
        assert seen == {"focused": True, "open": False, "phone": True}, seen
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_strip_never_outgrows_its_row_with_council_passed_surfaces(
    chromium, dev_server, tmp_path, accounts, this_database
):
    """
    Review W1-P M5 (accessibility M2): the council-passed surfaces were a row of links that pushed
    the strip's own controls off the window once two surfaces passed. They are one menu, «Superfici
    V5 · n», and «Altro» lists them below 80 rem. With 2, 6 and 12 surfaces, at 1280 and 1440, signed
    out and with the longest persona name inside: one row of 40 px, nothing outside the window.
    """
    keys = [
        "home",
        "login",
        "signup",
        "password-reset",
        "door-persons",
        "door-companies",
        "door-institutions",
        "door-universities",
        "door-forum",
        "project",
        "project-pilot",
        "project-agami",
    ]
    page = chromium.new_page(device_scale_factor=1)
    probe = """() => {
      const strip = document.querySelector('[data-dp-strip]');
      const outside = Array.from(strip.children).filter((el) => {
        const r = el.getBoundingClientRect();
        return getComputedStyle(el).display !== 'none' && r.width > 0 && (r.right > innerWidth + 0.5 || r.left < -0.5);
      }).map((el) => el.className);
      const count = document.querySelector('.dp-strip__menu--quick .dp-strip__count');
      return {height: Math.round(strip.getBoundingClientRect().height), scroll: document.documentElement.scrollWidth - innerWidth,
              outside, count: count ? count.textContent : null};
    }"""
    try:
        for who in ("anon", "qa-person"):
            if who != "anon":
                page.set_viewport_size({"width": 1440, "height": 900})
                page.goto(f"{dev_server}{LANDING}", wait_until="load")
                page.locator(".dp-strip__menu--personas > summary").click()
                page.locator(f'.dp-strip form[action="{ENTER}{who}/"] button').click()
                page.wait_for_load_state("load")
            for count in (2, 6, 12):
                _steward(tmp_path, "live_status.json", json.dumps({"surfaces": dict.fromkeys(keys[:count], "v5")}))
                for width in (1280, 1440):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(f"{dev_server}{LANDING}?page=/fr/", wait_until="load")
                    page.evaluate("() => document.fonts.ready")
                    seen = page.evaluate(probe)
                    assert seen == {"height": 40, "scroll": 0, "outside": [], "count": str(count)}, (
                        who,
                        count,
                        width,
                        seen,
                    )
            page.set_viewport_size({"width": 1024, "height": 768})
            page.goto(f"{dev_server}{LANDING}?page=/fr/", wait_until="load")
            page.locator(".dp-strip__narrow > summary").click()
            assert (
                page.locator(".dp-strip__narrow .dp-strip__panel")
                .get_by_text("Superfici V5 — hanno passato il consiglio")
                .is_visible()
            )
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_home_link_keeps_its_name_between_48_and_90_rem(chromium, dev_server):
    """
    Review W1-P, accessibility r2 n1 (CD condition C8): from 48 to 90 rem the home link was named
    «V5» alone — «Italy Legal Entry™ — » was ``display: none``. The words leave the eye, never the
    link's name, and take no room in the row.
    """
    page = chromium.new_page(device_scale_factor=1)
    try:
        for width, height in ((800, 600), (1024, 768), (1280, 800), (1439, 900)):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(f"{dev_server}{LANDING}", wait_until="load")
            link = page.locator("[data-dp-strip]").get_by_role("link", name="Italy Legal Entry™ — V5", exact=True)
            assert link.count() == 1 and link.is_visible(), width
            box = page.evaluate(
                "() => { const r = document.querySelector('.dp-strip__ile').getBoundingClientRect(); return [r.width, r.height]; }"
            )
            assert box[0] <= 1 and box[1] <= 1, (width, box)
    finally:
        page.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_strip_says_the_way_in_when_the_frame_reaches_the_sign_in(chromium, dev_server):
    """
    Review W1-P, UX r2 n2 (CD condition C4), in the browser: the frame navigates from the home to the
    sign-in — as the product's «Espace réservé» does — and the strip follows it: «Per entrare senza
    password: «Personas»» appears, and every «Entrer» carries the sign-in's ``next``; back on a
    public page, both go.
    """
    page = chromium.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)

    def frame_at(path: str) -> None:
        page.wait_for_function(
            "(path) => { try { const f = document.querySelector('iframe[data-dp-frame]'); return f.contentWindow.location.pathname === path && f.contentDocument.readyState === 'complete'; } catch (e) { return false; } }",
            arg=path,
        )
        page.wait_for_timeout(100)

    def strip() -> dict:
        return page.evaluate(
            "() => ({hidden: document.querySelector('[data-dp-hint]').hidden, next: Array.from(document.querySelectorAll('input[data-dp-next-field]')).map((f) => f.value)})"
        )

    try:
        page.goto(f"{dev_server}{LANDING}", wait_until="load")
        frame_at("/fr/")
        assert strip() == {"hidden": True, "next": ["", "", "", ""]}
        page.evaluate(
            "() => { document.querySelector('iframe[data-dp-frame]').contentWindow.location.assign('/fr/compte/login/?next=/fr/espace-reserve/mes-echeances/'); }"
        )
        frame_at("/fr/compte/login/")
        assert strip() == {"hidden": False, "next": ["/fr/espace-reserve/mes-echeances/"] * 4}
        assert page.locator("[data-dp-hint]").is_visible()
        page.evaluate(
            "() => { document.querySelector('iframe[data-dp-frame]').contentWindow.location.assign('/fr/faq/'); }"
        )
        frame_at("/fr/faq/")
        assert strip() == {"hidden": True, "next": ["", "", "", ""]}
    finally:
        page.close()


# --------------------------------------------------------------------------- the real package


def test_the_preview_files_are_written_with_lf_line_endings():
    footprint = [
        *sorted((ROOT / "apps" / "designpreview").glob("*.py")),
        *sorted((TEMPLATES / "dev" / "designpreview").glob("*.html")),
        ROOT / "config" / "settings" / "dev.py",
        STATIC / "css" / "dev" / "designpreview.css",
        STATIC / "js" / "dev" / "designpreview.js",
        Path(__file__),
    ]
    assert len(footprint) == 28, "ten modules of the app, fourteen templates, dev.py, a sheet, a script, this file"
    for path in footprint:
        assert b"\r" not in path.read_bytes(), path.name


# --------------------------------------------------------------------------- the catalogue


def test_the_catalogue_names_every_file_the_hub_and_the_pickers_point_at():
    """
    ``catalogued_proof_paths()`` is what the currency test below holds against the real directory:
    it must cover the hub's links, the hero picker's table and the type picker's whole grid —
    seven sheets, five surfaces, Arabic for the home and the dashboard.
    """
    from designpreview import services

    paths = services.catalogued_proof_paths()
    assert paths == sorted(set(paths))
    for relative in (
        "home/phase3.html",
        "home/options/hb-interim.html",
        "research/hero/hc/index.html",
        "research/hero/hc/ar.html",
        "research/hero/hc/explore.html",
        "research/hero/hd/index.html",
        "research/hero/hd/ar.html",
        "research/hero/hd/explore/loggia.html",
        "research/loader/index.html",
        "research/loader/mandata/index.html",
        "research/loader/lume/index.html",
        "research/loader/passo/index.html",
        "research/navigation/index.html",
        "research/navigation/public-fr-sheet.html",
        "research/navigation/public-ar-sheet.html",
        "research/navigation/app-fr-stuck.html",
        "research/navigation/app-ar-compact.html",
        "research/emil/prototype/drawer/index.html",
        "research/emil/prototype/drawer/ar.html",
        "research/21st-group1/signature-cta/index.html",
        "research/21st-group1/signature-cta/ar.html",
        "research/type/index.html",
        "research/hero/he/index.html",
        "research/hero/he/ar.html",
        "research/hero/he/concepts/e1/index.html",
        "research/hero/he/concepts/e2/index.html",
        "research/hero/he/concepts/e3/index.html",
        "research/hero/he/cta/index.html",
        "research/21st-group2/code-field/index.html",
        "research/21st-group2/code-field/ar.html",
        "research/21st-group4/proto/overlays.html",
        "research/21st-group4/proto/overlays-ar.html",
        "research/21st-group4/proto/stage.html",
        "research/21st-group4/proto/stage-ar.html",
        "research/motion/bench/index.html",
        "research/motion/bench/ar.html",
        "research/uiux-public/proto/home-h0.html",
        "research/uiux-public/proto/home-hb.html",
        "research/uiux-public/proto/home-hb-ar.html",
        "research/uiux-public/proto/menu.html",
        "research/uiux-public/proto/login.html",
        "research/uiux-public/proto/login-ar.html",
        "research/uiux-public/proto/login-error.html",
        "research/uiux-platform/proto/shell-fr.html",
        "research/uiux-platform/proto/shell-ar.html",
        "research/uiux-platform/proto/docs-fr.html",
        "research/uiux-platform/proto/docs-ar.html",
        # Step 0 of the research consolidation: wave 3, H-E's measurement pages.
        "research/documents/index.html",
        "research/documents/ar.html",
        "research/documents/anatomy.html",
        "research/journey/index.html",
        "research/journey/ar.html",
        "research/colour/specimen.html",
        "research/icons/sheet.html",
        "research/icons/sheet-ar.html",
        "research/icons/candidates.html",
        "research/icons/families.html",
        "research/images/proto/doors.html",
        "research/images/proto/doors-ar.html",
        "research/hero/he-motion/index.html",
        "research/hero/he-21st/states.html",
        "research/hero/he-21st/states-ar.html",
        "research/hero/he-21st/stage.html",
        "research/hero/he-21st/stage-ar.html",
        "research/hero/door-master/snippet.html",
        "research/hero/door-master/check/door-snippet.html",
    ):
        assert relative in paths, relative
    type_pages = [relative for relative in paths if relative.startswith("research/type/") and relative.count("/") == 3]
    assert len(type_pages) == 7 * (5 + 2)
    for folder in ("V4", "A", "A2", "Ap", "B", "C", "D"):
        for page in ("home", "home-ar", "menu", "dashboard", "dashboard-ar", "documents", "case"):
            assert f"research/type/{folder}/{page}.html" in type_pages, (folder, page)
    # A path is a file under the root: no query string, no leading slash, nothing dotted, a served type.
    for relative in paths:
        assert "?" not in relative and not relative.startswith("/"), relative
        assert not any(part.startswith(".") for part in relative.split("/")), relative
        assert Path(relative).suffix in services.PROOF_CONTENT_TYPES, relative
    # The Arabic pages the type research did not build are not in the grid at all.
    assert services.type_file("a", "menu", "ar") == ""
    assert services.type_file("a", "documents", "ar") == "" and services.type_file("a", "case", "ar") == ""
    assert services.type_file("a2", "dashboard", "ar") == "research/type/A2/dashboard-ar.html"
    assert services.type_file("ap", "home", "fr") == "research/type/Ap/home.html"


def test_every_candidate_of_the_catalogue_carries_its_status():
    """A research group is tagged; so is a research surface among gate-0 comps; a picker's table agrees."""
    from designpreview import services

    by_key = {group.key: group for group in services.GROUPS}
    research = {key for key in by_key if key in {"type", "he"} or key.startswith("research-")}
    assert research == {
        "he",
        "type",
        "research-loader",
        "research-navigation",
        "research-drawer",
        "research-cta",
        "research-21st",
        "research-motion",
        "research-uiux",
        "research-documents",
        "research-journey",
        "research-colour",
        "research-icons",
        "research-images",
    }
    research_variants = {("hc",), ("hd",), ("he",), ("e1",), ("e2",), ("e3",)}
    for key, group in by_key.items():
        assert (group.tag == services.STATUS_RESEARCH) is (key in research), key
        for surface in group.surfaces:
            touches_research = any(
                link.path.startswith("research/")
                or link.type_entry
                or link.compare_entry
                or link.hero_entry[:1] in research_variants
                for link in surface.links
            )
            if touches_research:
                assert group.tag or surface.tag == services.STATUS_RESEARCH, (key, surface.title)
    assert [v.key for v in services.HERO_VARIANTS.values() if v.research] == ["hc", "hd", "he", "e1", "e2", "e3"]
    assert services.HERO_VARIANTS["hc"].status == services.STATUS_RESEARCH == NOT_APPROVED
    assert services.HERO_VARIANTS["he"].status == services.HERO_VARIANTS["e2"].status == NOT_APPROVED
    assert services.HERO_VARIANTS["hb"].status == services.STATUS_GATE0
    for variant in ("hc", "hd", "he"):
        assert set(services.HERO_VARIANTS[variant].files) == {("fr", "3"), ("ar", "3")}, "phase 3 only"
    for number in (1, 2, 3):
        concept = services.HERO_VARIANTS[f"e{number}"]
        assert (concept.label, concept.name) == (f"E{number}", f"Concetto H-E {number}")
        assert concept.files == {("fr", "3"): f"research/hero/he/concepts/e{number}/index.html"}, "French only"
    assert services.TYPE_SYSTEMS["v4"].status == services.STATUS_CONTROL
    assert {system.status for key, system in services.TYPE_SYSTEMS.items() if key != "v4"} == {NOT_APPROVED}
    # No two choices of a bar answer to the same key. The three concepts have none: «3» is the
    # phase's in this bar, and a key for two concepts out of three would be worse than none.
    hero_keys = [v.shortcut for v in services.HERO_VARIANTS.values() if v.shortcut] + ["f", "r", "3", "i"]
    assert hero_keys == ["0", "a", "b", "c", "d", "e", "f", "r", "3", "i"]
    assert [v.key for v in services.HERO_VARIANTS.values() if not v.shortcut] == ["e1", "e2", "e3"]
    for keys in (
        hero_keys,
        [s.shortcut for s in services.TYPE_SYSTEMS.values()]
        + [s.shortcut for s in services.TYPE_SURFACES.values()]
        + ["f", "r"],
    ):
        assert len(keys) == len(set(keys)), keys
    # Nothing is announced before it is built any more: H-E's six files reached the disk on
    # 4 October 2026, and the currency test below holds them like every other file.
    assert services.IN_CONSTRUCTION == ()
    he = [p for p in services.catalogued_proof_paths() if p.startswith("research/hero/he/")]
    assert he == [
        "research/hero/he/ar.html",
        "research/hero/he/concepts/e1/index.html",
        "research/hero/he/concepts/e2/index.html",
        "research/hero/he/concepts/e3/index.html",
        "research/hero/he/cta/index.html",
        "research/hero/he/index.html",
    ]


# --------------------------------------------------------------------------- the real package


def test_the_catalogue_is_current_against_the_real_package():
    """
    Every file the hub, the pickers and the compare view point at exists in the council's proof
    directory — when that directory is here — and the proof server would serve each of them. The
    one exception would be what the catalogue announces before it is built (``IN_CONSTRUCTION``,
    empty since H-E's build reached the disk on 4 October): such a file may be missing, and the
    hub says «manca» until it arrives; one that is there must be servable like any other.
    """
    from designpreview.services import IN_CONSTRUCTION, catalogued_proof_paths, proof_exists

    if not DEFAULT_PROOF_DIR.is_dir():
        pytest.skip("the design council's proof directory is not on this machine")
    paths = catalogued_proof_paths()
    built = [relative for relative in paths if not relative.startswith(IN_CONSTRUCTION)]
    missing = [relative for relative in built if not (DEFAULT_PROOF_DIR / relative).is_file()]
    assert missing == [], missing
    on_disk = [relative for relative in paths if (DEFAULT_PROOF_DIR / relative).is_file()]
    refused = [relative for relative in on_disk if not proof_exists(DEFAULT_PROOF_DIR, relative)]
    assert refused == [], refused
    assert len(built) >= 160, "the catalogue has been emptied"


def test_the_cta_rig_still_reads_the_primary_the_hub_s_links_name():
    """
    Review HC-1, against the real package when it is here. The hub links the stand-in first screen
    of the CTA rig once per primary — ``?cta=t0``, ``a``, ``b`` — because the page draws one
    primary, the one its script reads from that parameter, and T0 when there is none. Were the rig
    rebuilt with another parameter or other values, every link would show T0 again while its label
    said otherwise: this holds the script to what the links name, and the links to every primary
    the script knows.
    """
    from designpreview import services

    if not DEFAULT_PROOF_DIR.is_dir():
        pytest.skip("the design council's proof directory is not on this machine")
    script = (DEFAULT_PROOF_DIR / "research" / "hero" / "he-21st" / "bench.js").read_text(encoding="utf-8")
    assert 'get("cta")' in script, "the rig no longer reads ?cta="
    classes = re.search(r"const CLASS = \{([^}]*)\}", script)
    assert classes, "the rig no longer maps a primary to a class"
    known = set(re.findall(r"(\w+):", classes.group(1)))
    stage = [
        link
        for group in services.GROUPS
        for surface in group.surfaces
        for link in surface.links
        if link.path.startswith("research/hero/he-21st/stage")
    ]
    assert stage and all(link.query.startswith("cta=") for link in stage), [link.label for link in stage]
    for page in ("stage.html", "stage-ar.html"):
        values = {link.query.removeprefix("cta=") for link in stage if link.path.endswith(f"/{page}")}
        assert values == known == {"t0", "a", "b"}, (page, values, known)
        markup = (DEFAULT_PROOF_DIR / "research" / "hero" / "he-21st" / page).read_text(encoding="utf-8")
        assert 'src="bench.js"' in markup and 'id="primary"' in markup, page


def _real_dotted_folders() -> list[tuple[Path, str]]:
    """
    Each dotted folder beside a page the new entries link, in the council's real directory, that
    holds a file of a served type: (the folder, that file's proof-relative path).
    """
    from designpreview.services import PROOF_CONTENT_TYPES

    found = []
    for folder in STEP_0_FOLDERS:
        base = DEFAULT_PROOF_DIR / folder
        assert base.is_dir(), folder
        for entry in sorted(os.scandir(base), key=lambda entry: entry.name):
            if not (entry.is_dir() and entry.name.startswith(".")):
                continue
            served = (path for path in Path(entry.path).rglob("*") if path.suffix.lower() in PROOF_CONTENT_TYPES)
            inside = next((path for path in served if path.is_file()), None)
            if inside is not None:
                found.append((Path(entry.path), inside.relative_to(DEFAULT_PROOF_DIR).as_posix()))
    return found


def test_beside_the_new_entries_the_real_package_s_working_folders_stay_closed():
    """
    The same, on the council's real directory when it is here: every dotted folder beside a page
    the new entries link — H-E's ``.work`` and ``.source``, the concepts', the motion bench's, the
    door master's — is refused by its name by the very resolver the proof view uses. (By the 8.3
    alias the volume gives it: the next test — review HS-1.)
    """
    from designpreview.services import proof_exists

    if not DEFAULT_PROOF_DIR.is_dir():
        pytest.skip("the design council's proof directory is not on this machine")
    found = _real_dotted_folders()
    for _folder, relative in found:
        assert not proof_exists(DEFAULT_PROOF_DIR, relative), relative
    assert len(found) >= 4, found


def test_beside_the_new_entries_the_real_package_s_working_folders_stay_closed_through_their_short_names():
    """
    Review HS-1: the alias half, on its own. Whether the volume generates 8.3 names is asked of a
    long-named folder of the package itself, not of the dotted folders: where it does, dotted
    folders that give no alias cannot pass for a volume without them — each one that has an alias,
    which really opens it, is refused through it, and at least one must be checked. Where it does
    not, the test says so with a skip.
    """
    from designpreview.services import proof_exists

    if not DEFAULT_PROOF_DIR.is_dir():
        pytest.skip("the design council's proof directory is not on this machine")
    if sys.platform != "win32":
        pytest.skip("8.3 aliases are a Windows file-system feature")
    if not _alias(DEFAULT_PROOF_DIR / "research" / "hero" / "door-master"):
        pytest.skip("this volume does not generate 8.3 names: the alias half was not checked")
    checked = []
    for folder, relative in _real_dotted_folders():
        alias = _alias(folder)
        if not alias:
            continue  # made while the volume generated no 8.3 name: no alias can open it
        aliased = relative.replace(f"/{folder.name}/", f"/{alias}/", 1)
        assert (DEFAULT_PROOF_DIR / aliased).is_file(), aliased
        assert not proof_exists(DEFAULT_PROOF_DIR, aliased), aliased
        checked.append(aliased)
    assert checked, "the volume gives 8.3 names, and no dotted folder was checked through its alias"
