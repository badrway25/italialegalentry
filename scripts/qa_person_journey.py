"""
End-to-end browser verification of the Person journey, against a running development server.

    .venv/Scripts/python scripts/qa_person_journey.py http://127.0.0.1:8770

    VISITEUR → COMPTE → SITUATION → ORIENTATION → RÈGLES → RÉSULTAT → DOSSIER → LISTE DE PIÈCES

Why a script and not only tests: a test proves the service returns what it should; it does not prove
the page renders it. The failures this catches are the ones a test cannot see — a template variable
renamed, a source list rendered into the wrong grid column, a page that 500s because a context key
moved. Both are needed and neither replaces the other.

**It signs in by creating the session server-side and handing the browser the cookie.** No password
is typed into a form, by anyone or anything. That is a deliberate constraint of this workflow and it
also happens to be the right way to do it: the point is to exercise the JOURNEY, not the login form,
which has its own tests.

Local development only. It refuses to run against anything but a loopback address.
"""

from __future__ import annotations

import asyncio
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

from importlib import import_module  # noqa: E402

from django.conf import settings  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

QA_EMAIL = "qa-person@example.test"
OUT = ROOT / "docs" / "qa" / "browser"


def _session_cookie_for(email: str) -> tuple[str, str]:
    """
    Create a real Django session for the account and return the cookie to hand the browser.

    This is exactly what ``client.force_login`` does in a test, written out, because Playwright
    drives a real browser and has no test client to borrow it from.
    """
    from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY

    user = get_user_model().objects.get(email=email)
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return settings.SESSION_COOKIE_NAME, session.session_key


async def _fill_situation(page, base: str, report: dict) -> None:
    await page.goto(f"{base}/fr/espace-reserve/ma-situation/", wait_until="domcontentloaded")
    report["situation_status"] = "loaded"
    report["situation_h1"] = (await page.locator("h1").first.inner_text()).strip()

    await page.fill("#id_nationality", "MA")
    await page.fill("#id_country_of_residence", "MA")
    await page.fill("#id_date_of_birth", "1994-03-15")
    await page.select_option("#id_education_level", "higher")
    await page.fill("#id_years_of_experience", "7")
    for code in ("ar", "fr"):
        box = page.locator(f"input[name='languages'][value='{code}']")
        if await box.count():
            await box.first.check()
    await page.select_option("#id_has_job_offer", "no")
    # Scoped to the situation form: the page chrome carries an account menu whose control is also a
    # submit button, and it is the FIRST one in the document.
    await page.click("form[action*='ma-situation'] button[type=submit]")
    await page.wait_for_load_state("domcontentloaded")
    report["situation_saved"] = "espace-reserve/ma-situation" in page.url


async def _run_questionnaire(page, base: str, report: dict) -> None:
    await page.goto(f"{base}/fr/orientation/", wait_until="domcontentloaded")
    # The intro page posts to the same URL to open a session. Scoped by CLASS rather than by action,
    # because the language switcher's links also match `[href*='orientation']` and come first.
    start = page.locator("form.wizard-intro__start button[type=submit]").first
    if await start.count():
        await start.click()
        await page.wait_for_load_state("domcontentloaded")

    for step in range(25):
        radios = page.locator("form[action*='/session/'] input[type=radio]")
        checks = page.locator("form[action*='/session/'] input[type=checkbox]:not([name='honeypot'])")
        if await radios.count():
            await radios.first.check()
        elif await checks.count():
            await checks.first.check()
        else:
            break
        # Scope the submit to the questionnaire's own form: the page chrome carries a logout form
        # whose button is also a submit, and clicking it ends the run instead of advancing it.
        submit = page.locator("form[action*='/session/'] button[type=submit]").first
        if not await submit.count():
            break
        await submit.click()
        await page.wait_for_load_state("domcontentloaded")
        if "resultat" in page.url or "result" in page.url:
            report["questionnaire_steps"] = step + 1
            break
    report["result_url"] = page.url


async def _read_dashboard(page, base: str, report: dict) -> None:
    await page.goto(f"{base}/fr/espace-reserve/", wait_until="domcontentloaded")
    report["dashboard_status"] = "loaded"
    report["case_reference"] = await _text(page, ".case-header__reference, [data-case-reference]")
    report["outcome"] = await _text(page, ".outcome__kind")
    report["sources"] = [
        (await item.inner_text()).strip().replace("\n", " ")
        for item in await page.locator(".sources__item").all()
    ]
    report["checklist_rows"] = await page.locator(".register__item, .checklist__row, tbody tr").count()
    report["no_source_notice"] = await _text(page, ".outcome ~ .note, .note")
    report["console_errors"] = report.get("console_errors", [])


async def _read_case_file(page, base: str, report: dict) -> None:
    """
    Open the case file the way a person does: from the list, by clicking the row.

    Navigating by clicking rather than by constructing the URL is the point — it proves the list
    links to a page that exists and that the caller may open, which is the pair of facts a test on
    the service cannot establish.
    """
    await page.goto(f"{base}/fr/espace-reserve/dossiers/", wait_until="domcontentloaded")
    report["case_list_rows"] = await page.locator(".register__item").count()

    first = page.locator(".register__item a.entry").first
    if not await first.count():
        report["case_detail"] = "no case in the list"
        return
    await first.click()
    await page.wait_for_load_state("domcontentloaded")
    report["case_detail_url"] = page.url
    report["case_detail_h1"] = await _text(page, "h1")
    report["checklist_rows"] = await page.locator(".data-table tbody tr").count()
    report["checklist_with_a_source"] = await page.locator(".data-table tbody tr .t-ref").count()

    link = page.locator("a[href*='pre-evaluation']").first
    if await link.count():
        await link.click()
        await page.wait_for_load_state("domcontentloaded")
        report["assessment_url"] = page.url
        report["assessment_sources"] = await page.locator(".sources__item").count()
        report["assessment_rules"] = await page.locator(".register__item").count()
        report["assessment_is_reproducible"] = "reproductible" in (await page.content()).lower()


async def _text(page, selector: str) -> str:
    node = page.locator(selector).first
    if await node.count():
        return (await node.inner_text()).strip().replace("\n", " ")[:300]
    return ""


async def main(base: str) -> int:
    if urlparse(base).hostname not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to run against a non-loopback host")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    # The ORM is synchronous and this coroutine is not; the session is created on a worker thread
    # rather than by loosening Django's async guard, which exists for good reasons.
    name, value = await asyncio.to_thread(_session_cookie_for, QA_EMAIL)
    report: dict = {"base": base, "console_errors": []}

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        await context.add_cookies(
            [{"name": name, "value": value, "domain": urlparse(base).hostname, "path": "/"}]
        )
        page = await context.new_page()
        page.on(
            "console",
            lambda message: report["console_errors"].append(message.text)
            if message.type == "error"
            else None,
        )
        page.on("pageerror", lambda exc: report["console_errors"].append(str(exc)))

        await _fill_situation(page, base, report)
        await _run_questionnaire(page, base, report)
        await _read_dashboard(page, base, report)
        await _read_case_file(page, base, report)
        await page.screenshot(path=str(OUT / "person_journey_dashboard.png"), full_page=True)

        await page.goto(f"{base}/fr/espace-reserve/mes-documents/", wait_until="domcontentloaded")
        await page.screenshot(path=str(OUT / "person_journey_documents.png"), full_page=True)

        await browser.close()

    (OUT / "person_journey.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8770")))
