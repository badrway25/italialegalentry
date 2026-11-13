"""
Sign the VISIBLE Chrome window in as a QA account, without typing a password anywhere.

    ILE_QA_BASE=http://127.0.0.1:8771 ILE_QA_DB=ile_qa \\
      python scripts/qa_chrome_signin.py qa-person@example.test /fr/espace-reserve/

The session is created server-side and the cookie is handed to the browser. Nothing in this
repository types a credential into a form: a password in a script is a password in a shell history,
in a process list and in a screen recording.

`ILE_QA_DB` picks which development database the session is minted against; it must be the same one
the server at `ILE_QA_BASE` is serving, or the cookie names a session that server has never heard
of and you get a silent redirect to the login page.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
os.environ.setdefault(
    "DATABASE_URL",
    f"postgres://ile:ile-dev-password@127.0.0.1:5439/{os.environ.get('ILE_QA_DB', 'ile')}",
)

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import (  # noqa: E402
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    SESSION_KEY,
    get_user_model,  # noqa: E402
)

sys.path.insert(0, str(ROOT / "scripts"))
from cdp import Page  # noqa: E402

# A Windows console is cp1252 and this project's output is French, Italian and Arabic. Printing a
# navigation label killed this script after it had already signed the browser in — the work was
# done, the report was not. `errors="replace"` costs a mangled glyph and never a traceback.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CDP = "http://127.0.0.1:9222"
BASE = os.environ.get("ILE_QA_BASE", "http://127.0.0.1:8770")


def session_cookie(email: str) -> tuple[str, str]:
    user = get_user_model().objects.get(email=email)
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return settings.SESSION_COOKIE_NAME, session.session_key


def main(email: str, landing: str) -> int:
    host = urlparse(BASE).hostname
    if host not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to mint a session against a non-loopback host")
        return 2

    name, value = session_cookie(email)
    # Over scripts/cdp.py, one socket to one page, rather than Playwright's browser-wide attach:
    # that attach enumerates every target in the window and stops returning when the user's own
    # tabs hold something it chokes on (a sign-in page with hCaptcha iframes did it on 24 Sept).
    # `Network.setCookie` is the same hand-over — the session was minted server-side above and the
    # browser is only told its name; no credential is typed anywhere.
    with Page.attach(url_contains="127.0.0.1:") as page:
        page.send("Network.enable")
        # Replace any session already there: signing in as a second role while the first is still
        # present is how you end up reviewing the wrong navigation and believing it.
        page.send("Network.deleteCookies", {"name": name, "domain": host})
        page.send("Network.setCookie", {"name": name, "value": value, "domain": host, "path": "/"})
        page.navigate(BASE + landing, settle=0.7)
        who = page.evaluate(
            "({url: location.href, h1: document.querySelector('h1')?.textContent?.trim() || '',"
            " nav: [...document.querySelectorAll('.local-nav a, nav a')].map(a => a.textContent.trim()).slice(0, 14)})"
        )
        status = 200 if who["url"].startswith(BASE + landing.split("?")[0]) else 302
    print(f"signed in as {email}")
    print(f"  landed {status}  ->  {who['url']}")
    print(f"  h1: {who['h1']}")
    print(f"  nav: {who['nav']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "/fr/espace-reserve/"))
