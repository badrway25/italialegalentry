"""
Browser checks of the reserved area (Playwright, Chromium) — run with ``-m browser``.

No horizontal overflow at 360 / 1440 px in LTR and RTL on the dashboard and the inbox, the local
navigation is reachable, and the mark-as-read form works without JavaScript. Screenshots are
written to ``$PORTAL_SCREENSHOT_DIR`` when set (QA), otherwise to the test's temporary directory.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from django.conf import settings
from django.test import Client

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

VIEWPORTS = {"mobile": (360, 780), "desktop": (1440, 900)}


@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


def _signed_in_context(browser, live_server, user, width, height, javascript=True):
    client = Client()
    client.force_login(user)
    context = browser.new_context(
        viewport={"width": width, "height": height}, device_scale_factor=1, java_script_enabled=javascript
    )
    context.add_cookies(
        [
            {
                "name": settings.SESSION_COOKIE_NAME,
                "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
                "url": live_server.url,
            }
        ]
    )
    return context


def _populate(user, make_contact_request, make_message, make_deadline, make_document):
    for i in range(4):
        make_contact_request(user, subject=f"Demande d’information numéro {i}", message=f"Texte {i}")
    make_message(user, subject="Convocation à un entretien d’orientation — merci de confirmer votre présence")
    make_message(user, subject="Votre dossier")
    make_deadline(user, title="Dépôt des pièces complémentaires", days=3)
    make_deadline(user, title="Inscription à la formation linguistique", days=-1)
    make_document(user, name="un-nom-de-fichier-particulierement-long-pour-tester-le-retour-a-la-ligne.pdf")


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("viewport", list(VIEWPORTS))
def test_dashboard_and_inbox_have_no_horizontal_overflow(
    browser,
    live_server,
    seeded,
    alice,
    make_contact_request,
    make_message,
    make_deadline,
    make_document,
    lang,
    viewport,
    tmp_path,
):
    _populate(alice, make_contact_request, make_message, make_deadline, make_document)
    out_dir = Path(os.environ.get("PORTAL_SCREENSHOT_DIR") or tmp_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    width, height = VIEWPORTS[viewport]
    context = _signed_in_context(browser, live_server, alice, width, height)
    page = context.new_page()
    for name, path in (("dashboard", ""), ("messages", "communications/"), ("requests", "mes-demandes/")):
        page.goto(f"{live_server.url}/{lang}/espace-reserve/{path}", wait_until="networkidle")
        assert page.locator("h1").count() == 1
        scroll_width, client_width = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        assert scroll_width <= client_width + 1, (name, lang, viewport, scroll_width, client_width)
        page.screenshot(path=str(out_dir / f"portal-{name}-{lang}-{viewport}.png"), full_page=True)
    # The console (design V4) marks the current page on its rail, not on the V2 local nav. The
    # chrome renders the rail twice on purpose — the desktop rail and the phone drawer's copy
    # (templates/partials/portal_chrome.html) — so the DOM always holds two marked items: one per
    # copy, never two within a copy, never none. (The 26/09 version counted the whole page and
    # expected one; it was committed without being re-run and failed on every parametrisation.)
    for rail_copy in ("nav.rail[data-rail]", "nav.rail--drawer"):
        assert page.locator(f"{rail_copy} .rail__item[aria-current='page']").count() == 1, rail_copy
    context.close()


#: Names the elements that stick out of the viewport — turns an overflow failure into a diagnosis.
_OVERFLOW_CULPRITS = """
(() => {
  const width = document.documentElement.clientWidth;
  return [...document.querySelectorAll('body *')]
    .filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && (r.right > width + 1 || r.left < -1) && !el.closest('.scroll-x, .visually-hidden');
    })
    .slice(0, 8)
    .map((el) => el.tagName.toLowerCase() + '.' + String(el.className).split(' ').join('.'));
})()
"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_secondary_pages_have_no_horizontal_overflow_at_390(
    browser,
    live_server,
    seeded,
    alice,
    make_contact_request,
    make_message,
    make_deadline,
    make_document,
    completed_orientation,
    lang,
    tmp_path,
):
    """Review addition: the pages the first browser test skips, at 390 px, LTR and RTL, long content."""
    from portal.models import Message

    _populate(alice, make_contact_request, make_message, make_deadline, make_document)
    long_word = "Identifiant" + "X" * 90
    request_row = make_contact_request(alice, subject=f"Sujet {long_word}", message=f"Texte {long_word}")
    make_message(alice, subject=f"Objet {long_word}", body=f"Corps {long_word}")
    make_deadline(alice, title=f"Titre {long_word}", description=long_word, source_note=long_word)
    completed_orientation(alice)
    message = Message.objects.filter(recipient=alice).order_by("-created_at").first()
    out_dir = Path(os.environ.get("PORTAL_SCREENSHOT_DIR") or tmp_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    context = _signed_in_context(browser, live_server, alice, 390, 844)
    page = context.new_page()
    pages = (
        ("documents", "mes-documents/"),
        ("pathways", "mon-parcours/"),
        ("deadlines", "mes-echeances/"),
        ("request-detail", f"mes-demandes/contact/{request_row.pk}/"),
        ("message-detail", f"communications/{message.pk}/"),
        ("messages", "communications/"),
        ("dashboard", ""),
    )
    for name, path in pages:
        page.goto(f"{live_server.url}/{lang}/espace-reserve/{path}", wait_until="networkidle")
        assert page.locator("h1").count() == 1, name
        assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
        scroll_width, client_width = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        culprits = page.evaluate(_OVERFLOW_CULPRITS) if scroll_width > client_width + 1 else []
        assert scroll_width <= client_width + 1, (name, lang, scroll_width, client_width, culprits)
        page.screenshot(path=str(out_dir / f"portal-{name}-{lang}-390.png"), full_page=True)
    context.close()


@pytest.mark.parametrize("size", [(1024, 800), (390, 844)], ids=["tablet-1024", "phone-390"])
def test_mark_as_read_works_without_javascript(browser, live_server, seeded, alice, make_message, size):
    """
    Below the navigation breakpoint (80rem) the no-JS header renders the whole menu expanded; it must
    not stay sticky over the page (it used to cover the full viewport and swallow every click).
    """
    message = make_message(alice, subject="Message à lire")
    context = _signed_in_context(browser, live_server, alice, size[0], size[1], javascript=False)
    page = context.new_page()
    page.goto(f"{live_server.url}/fr/espace-reserve/communications/{message.pk}/", wait_until="load")
    # A real pointer click: Playwright refuses it while another element (the header) covers the button.
    page.get_by_role("button", name="Marquer comme lue").click(timeout=10_000)
    page.wait_for_load_state("load")
    message.refresh_from_db()
    assert message.is_read is True
    assert page.get_by_role("button", name="Marquer comme lue").count() == 0
    context.close()
