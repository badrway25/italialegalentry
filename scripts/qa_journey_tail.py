"""
The tail of the person journey that `qa_person_journey.py` never reached: Academy and Help desk.

The mandate's flow ends `… → DOCUMENTI → FORMAZIONE/SPORTELLO → MONITORAGGIO`, and the existing
script stops at the documents. Two whole surfaces were therefore verified by their own unit suites
and never by clicking, which is exactly the gap the browser scripts exist to close.

Signs in by creating the session server-side. No password is typed into any field.
Local development only.
"""

from __future__ import annotations

import json
import os
import sys
from importlib import import_module
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import (  # noqa: E402
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    SESSION_KEY,
    get_user_model,  # noqa: E402
)
from playwright.sync_api import sync_playwright  # noqa: E402

QA_EMAIL = "qa-person@example.test"

PAGES = [
    ("academy_catalogue", "/fr/espace-reserve/formation/"),
    ("helpdesk_queue", "/fr/espace-reserve/guichet/"),
    ("dashboard", "/fr/espace-reserve/"),
]


def _console_sink(bucket: list[str]):
    def sink(message) -> None:
        if message.type == "error":
            bucket.append(message.text)

    return sink


def session_cookie(email: str) -> tuple[str, str]:
    user = get_user_model().objects.get(email=email)
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return settings.SESSION_COOKIE_NAME, session.session_key


def main(base: str) -> int:
    if urlparse(base).hostname not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to run against a non-loopback host")
        return 2

    name, value = session_cookie(QA_EMAIL)
    report: dict[str, object] = {"base": base}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        context.add_cookies([{"name": name, "value": value, "domain": urlparse(base).hostname, "path": "/"}])
        page = context.new_page()
        errors: list[str] = []
        page.on("console", _console_sink(errors))
        page.on("pageerror", lambda exc: errors.append(str(exc)))

        for label, path in PAGES:
            response = page.goto(base + path, wait_until="domcontentloaded")
            heading = page.locator("h1").first
            report[label] = {
                "path": path,
                "status": response.status if response else 0,
                "h1": heading.inner_text().strip() if heading.count() else "",
                "h1_count": page.locator("h1").count(),
                "links_into_the_surface": page.locator(f'a[href*="{path.split("/fr")[1]}"]').count(),
            }

        # The one link that proves the two surfaces are reachable FROM the journey, rather than
        # only by typing the URL: the reserved-area navigation.
        page.goto(base + "/fr/espace-reserve/", wait_until="domcontentloaded")
        nav_html = page.content()
        report["dashboard_links_to_academy"] = "/espace-reserve/formation/" in nav_html
        report["dashboard_links_to_helpdesk"] = "/espace-reserve/guichet/" in nav_html
        report["console_errors"] = len(errors)
        browser.close()

    print(json.dumps(report, indent=1, ensure_ascii=False))
    bad = [k for k, v in report.items() if isinstance(v, dict) and v.get("status") != 200]
    if bad:
        print("PAGES NOT 200:", bad)
        return 1
    if not (report["dashboard_links_to_academy"] and report["dashboard_links_to_helpdesk"]):
        print("the reserved area does not link to both surfaces")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main((sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8770").rstrip("/")))
