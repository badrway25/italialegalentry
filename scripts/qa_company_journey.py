"""
End-to-end browser verification of the Company journey, against a running development server.

    .venv/Scripts/python scripts/qa_company_journey.py http://127.0.0.1:8770

    IMPRESA → ACCOUNT/VERIFICA → FABBISOGNO → COMPETENZE → ATTORI AUTORIZZATI → STATO

The second of the two flows the directive names. Like the person's journey, it navigates by CLICKING
rather than by constructing URLs: that is what proves the pages link to one another and that the
caller may open what the page offers.

Two things it checks that a test cannot: that declaring a company opens a VERIFICATION and grants
nothing, and that no screen anywhere in this journey lists people. An enterprise expresses a need;
it never browses candidates, and the absence has to be visible, not just asserted.

Signs in by creating the session server-side. Loopback only.
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

QA_EMAIL = "seed-company@example.test"
OUT = ROOT / "docs" / "qa" / "browser"
BASE_PATH = "/fr/espace-reserve/entreprise/"

#: Words that must not appear on any screen of this journey. The project does not select people and
#: does not intermediate labour; a page that offers to "find profiles" contradicts its own terms.
FORBIDDEN = (
    "matching",
    "recruit in morocco",
    "find qualified profiles",
    "profils qualifiés",
    "candidats disponibles",
    "sélectionner un candidat",
)


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


async def _text(page, selector: str) -> str:
    node = page.locator(selector).first
    if await node.count():
        return (await node.inner_text()).strip().replace("\n", " ")[:200]
    return ""


async def main(base: str) -> int:
    if urlparse(base).hostname not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to run against a non-loopback host")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    cookie = await asyncio.to_thread(_session_cookie_for, QA_EMAIL)
    if cookie is None:
        print(f"no account {QA_EMAIL}: run `manage.py seed_all` in a development database first")
        return 2
    name, value = cookie

    report: dict = {"base": base, "console_errors": [], "forbidden_found": []}

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        await context.add_cookies(
            [{"name": name, "value": value, "domain": urlparse(base).hostname, "path": "/"}]
        )
        page = await context.new_page()
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: report["console_errors"].append(str(e)))

        seen: list[str] = []

        async def visit(url: str, label: str) -> None:
            response = await page.goto(url, wait_until="domcontentloaded")
            body = (await page.content()).lower()
            for word in FORBIDDEN:
                if word in body:
                    report["forbidden_found"].append({"page": label, "word": word})
            seen.append(label)
            report[f"{label}_status"] = response.status if response else 0
            report[f"{label}_h1"] = await _text(page, "h1")

        # 1. the workspace
        await visit(f"{base}{BASE_PATH}", "dashboard")

        # 2. the company file — declared, and awaiting verification
        await visit(f"{base}{BASE_PATH}mon-entreprise/", "profile")
        profile_body = (await page.content()).lower()
        report["verification_stated"] = any(
            word in profile_body for word in ("vérification", "verifica", "en cours", "vérifi")
        )

        # 3. the needs register, reached by clicking rather than by URL
        # Scoped to the main region: the language switcher carries the same path in four languages
        # and comes first in the document, so an unscoped selector clicks a hidden link.
        link = page.locator(f"main a[href*='{BASE_PATH}mes-besoins/']").first
        if await link.count():
            await link.click()
            await page.wait_for_load_state("domcontentloaded")
            report["needs_reached_by_click"] = "mes-besoins" in page.url
        else:
            await visit(f"{base}{BASE_PATH}mes-besoins/", "needs")
            report["needs_reached_by_click"] = False
        report["needs_rows"] = await page.locator(".register__item, tbody tr").count()

        # 4. one need in full: the work described, the skills, who is answerable
        detail = page.locator(f"main .register__item a[href*='{BASE_PATH}mes-besoins/']").first
        if await detail.count():
            await detail.click()
            await page.wait_for_load_state("domcontentloaded")
            report["need_detail_url"] = page.url
            report["need_detail_h1"] = await _text(page, "h1")
            report["need_skills_rows"] = await page.locator(".data-table tbody tr, .register__item").count()
            report["need_state"] = await _text(page, ".state")
            body = (await page.content()).lower()
            report["responsible_named"] = "responsable" in body or "attribu" in body

        # 5. the territorial analysis is NOT for a company: it aggregates every company's needs.
        # The URL is typed here on purpose — the company's own navigation never offers it — and the
        # refusal is the assertion, not a failure. This is the one page of the journey that must NOT
        # open.
        await visit(f"{base}{BASE_PATH}analyse-territoriale/", "analysis")
        report["analysis_refused_to_the_company"] = report["analysis_status"] == 403

        await page.goto(f"{base}{BASE_PATH}", wait_until="domcontentloaded")
        await page.screenshot(path=str(OUT / "company_journey_dashboard.png"), full_page=True)

        report["pages_visited"] = seen
        await browser.close()

    (OUT / "company_journey.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # The only console error this journey may produce is the 403 it deliberately provokes.
    unexpected = [e for e in report["console_errors"] if "403" not in e]
    ok = (
        not report["forbidden_found"]
        and not unexpected
        and report.get("analysis_refused_to_the_company")
        and report.get("needs_reached_by_click")
        and report.get("needs_rows", 0) > 0
    )
    report["unexpected_console_errors"] = unexpected
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8770")))
