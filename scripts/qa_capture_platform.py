"""
Screenshots of the authenticated platform, one per role, against a running development server.

    .venv/Scripts/python scripts/qa_capture_platform.py http://127.0.0.1:8770

Why per role and not per page: the question the images have to answer is «what does each kind of
account actually see», and the same URL answers it differently for a person, a professional and an
authorised actor. A gallery of pages captured as one superuser shows a product nobody uses.

Signs in by creating each session server-side — no password is typed into a form. Loopback only.
"""

from __future__ import annotations

import asyncio
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
from django.contrib.auth import get_user_model  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

OUT = ROOT / "docs" / "qa" / "platform"

#: account -> (slug, paths). The slug names the file, so a reader browsing the directory can tell
#: which account produced which image without opening it.
SHOTS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "qa-person@example.test",
        "person",
        (
            "/espace-reserve/",
            "/espace-reserve/ma-situation/",
            "/espace-reserve/dossiers/",
            "/espace-reserve/mes-documents/",
        ),
    ),
    ("seed-person@example.test", "person-seeded", ("/espace-reserve/", "/espace-reserve/formation/")),
    ("seed-actor@example.test", "authorised-actor", ("/espace-reserve/selection/",)),
    ("seed-company@example.test", "company", ("/espace-reserve/entreprise/",)),
    ("demo-professionnel@example.test", "professional", ("/espace-reserve/guichet/confiees/",)),
)

VIEWPORTS = (("desktop", 1440, 900), ("phone", 390, 844))
LANGUAGES = ("fr", "ar")


def _session_cookie_for(email: str) -> tuple[str, str] | None:
    from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY

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


async def main(base: str) -> int:
    if urlparse(base).hostname not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to run against a non-loopback host")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    host = urlparse(base).hostname
    taken: list[dict] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for email, slug, paths in SHOTS:
            cookie = await asyncio.to_thread(_session_cookie_for, email)
            if cookie is None:
                print(f"  skipped {slug}: no account {email}")
                continue
            name, value = cookie
            for label, width, height in VIEWPORTS:
                context = await browser.new_context(viewport={"width": width, "height": height})
                await context.add_cookies([{"name": name, "value": value, "domain": host, "path": "/"}])
                page = await context.new_page()
                for language in LANGUAGES:
                    # Arabic only at phone width: the point of the second language here is the
                    # layout under pressure, and a second desktop set doubles the files for nothing.
                    if language != "fr" and label != "phone":
                        continue
                    for path in paths:
                        url = f"{base}/{language}{path}"
                        response = await page.goto(url, wait_until="networkidle")
                        stem = path.strip("/").replace("/", "_") or "root"
                        filename = f"{slug}_{language}_{label}_{stem}.png"
                        await page.screenshot(path=str(OUT / filename), full_page=True)
                        taken.append(
                            {
                                "file": filename,
                                "account": slug,
                                "url": url,
                                "status": response.status if response else 0,
                            }
                        )
                await context.close()
        await browser.close()

    (OUT / "index.json").write_text(json.dumps(taken, indent=2, ensure_ascii=False), encoding="utf-8")
    bad = [row for row in taken if row["status"] != 200]
    print(f"{len(taken)} screenshots written to {OUT}")
    for row in bad:
        print(f"  NOT 200: {row['status']}  {row['url']}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8770")))
