"""
Capture the BEFORE/AFTER screenshot baseline for the design rebase (docs/rebase, docs/design).

Usage (servers must already be running; see docs/rebase/CURRENT_IMPLEMENTATION_STATE.md):

    .venv/Scripts/python scripts/capture_baseline.py --label before --out docs/qa/visual/before

Public pages are taken from server A (interim state, today's date) unless the page only exists
behind the Phase 3 gate, in which case server B (simulated 5 October 2026) is used. Authenticated
pages are always taken from server B with the QA accounts.

Screenshots are written as <page>__<viewport>__<lang>.png. They are ignored by git (docs/qa/**/*.png)
except for the curated set copied into docs/qa/golden/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from playwright.sync_api import sync_playwright  # noqa: E402

SERVER_A = "http://127.0.0.1:8770"  # interim: today, Phase 3 closed
SERVER_B = "http://127.0.0.1:8771"  # phase3: simulated 5 October 2026, flags open

#: No password is needed any more: ``sign_in`` creates the session server-side and hands the browser
#: the cookie. Nothing in this repository types a credential into a form.
#:
#: One consequence to know: the session must be written into the database the TARGET SERVER reads.
#: Server B runs on ``ile_qa``, so capturing its authenticated pages means running this script with
#: the same ``DATABASE_URL``:
#:
#:     DATABASE_URL=…/ile_qa .venv/Scripts/python scripts/capture_baseline.py \
#:         --label after --out docs/qa/visual/after
#:
#: Run without it, the public pages are captured normally and the authenticated ones are skipped
#: with a line saying so — which is the right failure: a screenshot of a login page filed under
#: "portal dashboard" is worse than a missing file.

#: (width, height) — the ten viewports required by the design rebase directive §8.
VIEWPORTS = [
    (320, 800),
    (360, 800),
    (390, 844),
    (430, 932),
    (768, 1024),
    (1024, 1366),
    (1280, 800),
    (1440, 900),
    (1600, 1000),
    (1920, 1080),
]

#: A smaller set for the long tail of pages: phone, tablet, laptop, large desktop.
VIEWPORTS_SHORT = [(390, 844), (768, 1024), (1280, 800), (1920, 1080)]

#: name, path, server, needs_login, viewport set
PAGES = [
    ("home", "/{lang}/", "A", None, "full"),
    ("home-phase3", "/{lang}/", "B", None, "full"),
    ("persons", "/{lang}/parcours/", "B", None, "full"),
    ("companies", "/{lang}/entreprises/", "A", None, "full"),
    ("institutions", "/{lang}/institutions/", "B", None, "short"),
    ("universities", "/{lang}/universites-et-formation/", "B", None, "short"),
    ("forum", "/{lang}/forum/", "A", None, "full"),
    ("faq", "/{lang}/faq/", "B", None, "short"),
    ("glossary", "/{lang}/glossaire/", "B", None, "short"),
    ("news-index", "/{lang}/actualites/", "B", None, "short"),
    ("project", "/{lang}/le-projet/", "A", None, "short"),
    ("agami", "/{lang}/agami/", "A", None, "short"),
    ("contact", "/{lang}/contact/", "A", None, "short"),
    ("pilot", "/{lang}/projet-pilote/", "B", None, "short"),
    ("login", "/{lang}/compte/login/", "A", None, "short"),
    ("signup", "/{lang}/compte/signup/", "B", None, "short"),
    ("orientation-start", "/{lang}/orientation/", "B", None, "short"),
    ("company-needs-form", "/{lang}/entreprises/recueil-des-besoins/", "B", None, "short"),
    ("error-404", "/{lang}/cette-page-nexiste-pas/", "A", None, "short"),
    # Authenticated (server B)
    ("portal-dashboard", "/{lang}/espace-reserve/", "B", "person", "full"),
    ("portal-pathways", "/{lang}/espace-reserve/mon-parcours/", "B", "person", "short"),
    ("portal-documents", "/{lang}/espace-reserve/mes-documents/", "B", "person", "short"),
    ("portal-messages", "/{lang}/espace-reserve/communications/", "B", "person", "short"),
    ("portal-deadlines", "/{lang}/espace-reserve/mes-echeances/", "B", "person", "short"),
    ("portal-company", "/{lang}/espace-reserve/", "B", "company", "short"),
]


def session_cookie_for(email: str) -> tuple[str, str] | None:
    """
    Create a real Django session for the account and return the cookie to hand the browser.

    Called BEFORE ``sync_playwright()`` is entered. Playwright's synchronous API is a greenlet
    wrapper over an asyncio loop, and Django refuses an ORM call from inside a running loop
    (``SynchronousOnlyOperation``) — a guard worth respecting rather than disabling, so the database
    work happens first and the browser only ever receives a value.

    This is what ``client.force_login`` does in a test, written out, because Playwright drives a real
    browser and has no test client to borrow it from.
    """
    from importlib import import_module

    from django.conf import settings
    from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY, get_user_model

    user = get_user_model().objects.filter(email=email).first()
    if user is None:
        return None

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return settings.SESSION_COOKIE_NAME, session.session_key


def cookies_for_plan(pages) -> dict[str, tuple[str, str]]:
    """One session per account the plan needs, all created before the browser starts."""
    cookies: dict[str, tuple[str, str]] = {}
    for _name, _path, _server, login, _size in pages:
        if not login or login in cookies:
            continue
        email = f"qa-{login}@example.test"
        cookie = session_cookie_for(email)
        if cookie is None:
            print(f"  no account {email}: its pages will be skipped")
            continue
        cookies[login] = cookie
    return cookies


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="before")
    parser.add_argument("--out", default="docs/qa/visual/before")
    parser.add_argument("--langs", default="fr,ar")
    parser.add_argument("--only", default="", help="comma-separated page names")
    args = parser.parse_args()

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    langs = [item for item in args.langs.split(",") if item]
    only = {item for item in args.only.split(",") if item}

    manifest: list[dict] = []
    # Every session is created before the browser starts: see session_cookie_for.
    cookies = cookies_for_plan([row for row in PAGES if not only or row[0] in only])

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        contexts: dict[tuple[str, str | None], object] = {}

        def context_for(server: str, login: str | None, width: int, height: int):
            key = (server, login, width, height)
            if key not in contexts:
                base = SERVER_A if server == "A" else SERVER_B
                ctx = browser.new_context(
                    viewport={"width": width, "height": height},
                    device_scale_factor=2 if width <= 430 else 1,
                )
                if login:
                    cookie = cookies.get(login)
                    if cookie is None:
                        return None
                    name_, value = cookie
                    ctx.add_cookies(
                        [{"name": name_, "value": value, "domain": urlparse(base).hostname, "path": "/"}]
                    )
                contexts[key] = ctx
            return contexts[key]

        for name, path, server, login, size_set in PAGES:
            if only and name not in only:
                continue
            base = SERVER_A if server == "A" else SERVER_B
            viewports = VIEWPORTS if size_set == "full" else VIEWPORTS_SHORT
            for lang in langs:
                for width, height in viewports:
                    ctx = context_for(server, login, width, height)
                    if ctx is None:
                        # No session for this account: skip rather than photograph a login page and
                        # file it under the name of the page it is not.
                        continue
                    page = ctx.new_page()
                    url = base + path.format(lang=lang)
                    try:
                        response = page.goto(url, wait_until="networkidle", timeout=30000)
                        status = response.status if response else 0
                        page.wait_for_timeout(200)
                        filename = f"{name}__{width}x{height}__{lang}.png"
                        page.screenshot(path=str(out_root / filename), full_page=True)
                        overflow = page.evaluate(
                            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
                        )
                        manifest.append(
                            {
                                "page": name,
                                "url": url,
                                "status": status,
                                "viewport": f"{width}x{height}",
                                "lang": lang,
                                "file": filename,
                                "scroll_width": overflow[0],
                                "client_width": overflow[1],
                            }
                        )
                        print(f"{status} {url} {width}x{height} -> {filename}", flush=True)
                    except Exception as exc:  # pragma: no cover - diagnostics only
                        print(f"ERROR {url} {width}x{height}: {exc}", flush=True)
                        manifest.append(
                            {"page": name, "url": url, "viewport": f"{width}x{height}", "lang": lang, "error": str(exc)}
                        )
                    finally:
                        page.close()

        browser.close()

    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    errors = [row for row in manifest if row.get("error") or row.get("status", 200) >= 400]
    print(f"\n{len(manifest)} screenshots, {len(errors)} problem(s), label={args.label}")
    for row in errors[:20]:
        print(" ", row.get("page"), row.get("viewport"), row.get("lang"), row.get("status"), row.get("error", "")[:80])
    return 0


if __name__ == "__main__":
    sys.exit(main())
