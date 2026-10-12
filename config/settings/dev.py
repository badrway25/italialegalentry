from pathlib import Path

from .base import *  # noqa: F401,F403
from .base import DATABASES, INSTALLED_APPS, LOGGING, STORAGES, env

DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]  # noqa: S104
STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
LANGUAGE_COOKIE_SECURE = False
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LOGGING["root"]["level"] = "INFO"

# The development server is runserver: one thread per client socket, no worker limit, and a request
# opens its connection before the view runs (ATOMIC_REQUESTS). base.py's 60 s lifetime kept every one
# of those connections open after its thread had ended, until the shared PostgreSQL ran out of slots
# (preview outage of 2 October 2026). `.env.example` has prescribed 0 since 21 September; this makes
# it the default so a fresh checkout behaves the same. Production keeps 60 s under gunicorn's fixed
# number of workers, where one reused connection per worker is the point.
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=0)

NOTIFICATIONS_SEND_IMMEDIATELY = True

# ---------------------------------------------------------------------------
# V5 live preview (apps/designpreview) — development only, opt-in per process.
# /__design-v5/ — the live V5 product, its index, the persona switch and the
# research archive — exists when DEBUG is on AND the environment says
# ILE_DESIGN_PREVIEW=1; config/urls.py mounts it inside its DEBUG block. Only
# this module knows the flag: test.py and prod.py never define it, so the app
# is never installed and the routes never exist there. Remove this block, the
# mount and the app to be rid of the preview.
# ---------------------------------------------------------------------------
ILE_DESIGN_PREVIEW = DEBUG and env.bool("ILE_DESIGN_PREVIEW", default=False)
ILE_DESIGN_PREVIEW_PROOF_DIR = Path(env("ILE_DESIGN_PREVIEW_PROOF_DIR", default="C:/tmp/ile_v5_council/proof"))
if ILE_DESIGN_PREVIEW:
    from .base import BASE_DIR, DATABASES, MIDDLEWARE

    INSTALLED_APPS = [*INSTALLED_APPS, "designpreview"]
    # The preview server and the database (docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md). On
    # 2 October 2026 this server took all 300 connections of the shared PostgreSQL: `runserver`
    # gives every socket a thread, a thread keeps its connection past its request (CONN_MAX_AGE),
    # and nothing ever closes the connection of a thread that has ended. Three things, all of
    # them only here:
    #   · a connection lives for one request — Django closes it when the response ends — and is
    #     checked before reuse should that ever change;
    #   · no more than ILE_DESIGN_PREVIEW_DB_CEILING at a time, whatever arrives
    #     (designpreview.middleware, first in the chain so that nothing reads before it);
    #   · they carry a name, so the count is one query away:
    #     select count(*) from pg_stat_activity where application_name = 'ile-design-preview'.
    # New objects, not edits: base.DATABASES and base.MIDDLEWARE belong to every environment.
    ILE_DESIGN_PREVIEW_DB_CEILING = env.int("ILE_DESIGN_PREVIEW_DB_CEILING", default=8)
    DATABASES = {
        **DATABASES,
        "default": {
            **DATABASES["default"],
            "CONN_MAX_AGE": 0,
            "CONN_HEALTH_CHECKS": True,
            "OPTIONS": {
                **DATABASES["default"].get("OPTIONS", {}),
                "application_name": env("PGAPPNAME", default="ile-design-preview"),
            },
        },
    }
    # The live product (V5.4 plan §4.4). The preview answers its own port only: the Host of every
    # request must be 127.0.0.1:<port> or localhost:<port> — 8780 for the owner's server, the
    # lane's port for a lane (each lane exports its own).
    ILE_DESIGN_PREVIEW_PORT = env.int("ILE_DESIGN_PREVIEW_PORT", default=8780)
    # The persona switch: the four QA accounts of the preview's own database, by e-mail — never a
    # staff account, never a password. A persona is opened only on a database named here: ile_v5
    # (8780's) and the lane clones, never ile_qa or ile (the V4 control's), whatever this says.
    ILE_DESIGN_PREVIEW_PERSONAS = {
        "qa-doc-person": "qa-doc-person@example.test",
        "qa-person": "qa-person@example.test",
        "qa-fresh-person": "qa-fresh-person@example.test",
        "qa-company": "qa-company@example.test",
    }
    ILE_DESIGN_PREVIEW_ALLOWED_DATABASES = ("ile_v5", *(f"ile_v5_l{lane}" for lane in range(3, 10)))
    # What the strip and the index read, and never write: the steward's two files, and the V4
    # control the index compares with — on 8771, never on the server that serves V5. A lane or a
    # reviewer may point the first two at a scratch copy (a state to measure) without touching the
    # steward's own files.
    ILE_DESIGN_PREVIEW_LIVE_STATUS = Path(
        env("ILE_DESIGN_PREVIEW_LIVE_STATUS", default=str(BASE_DIR / "docs" / "design-v5" / "live_status.json"))
    )
    ILE_DESIGN_PREVIEW_CHANGELOG = Path(
        env("ILE_DESIGN_PREVIEW_CHANGELOG", default=str(BASE_DIR / "docs" / "design-v5" / "CHANGELOG_V54.md"))
    )
    ILE_DESIGN_PREVIEW_V4_ORIGIN = env("ILE_DESIGN_PREVIEW_V4_ORIGIN", default="http://127.0.0.1:8771")
    # Cookies are per host, not per port: with names of its own, a V5 session, CSRF token or
    # language never clobbers V4's on 8770–8772 (and messages, session-stored, follow).
    SESSION_COOKIE_NAME = "ile_v5_sessionid"
    CSRF_COOKIE_NAME = "ile_v5_csrftoken"
    LANGUAGE_COOKIE_NAME = "ile_v5_language"
    # The chain: the ceiling first, so that nothing reads the database before it; the frame
    # exception after CSPMiddleware and XFrameOptionsMiddleware, so that its response hook runs
    # before theirs (designpreview.frames); the read-only rule of persona sessions last, once the
    # session and the language are known (designpreview.personas).
    MIDDLEWARE = [
        "designpreview.middleware.ConnectionCeilingMiddleware",
        *MIDDLEWARE,
        "designpreview.frames.PreviewFrameMiddleware",
        "designpreview.personas.PersonaReadOnlyMiddleware",
    ]
