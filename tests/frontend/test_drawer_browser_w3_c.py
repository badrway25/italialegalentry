"""
The preview drawer in the browser — design V5, family W3-C, step 2 (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14
«Preview drawer», §3.5 item 5; DOCUMENT_WORKSPACE.md §12; the overlay system's contract
docs/design-v5/QA/v54/w2-a/CONTRACT.md; docs/design-v5/QA/v54/w3-c/NOTES.md). What a static test cannot see:

* a row opens its piece BESIDE the register on desktop — non-modal: no scrim, no aria-modal, the page usable; the head
  at once from the row, the focus on the title, the piece's page in the body; the register lays itself out by the width
  it is left;
* the history: the opening pushes the piece's URL; a swap from the list replaces it and leaves the focus in the list;
  Esc, «Fermer» and Back close it and the register's URL comes back with its `?état=`;
* on a phone the drawer is a modal sheet: the scrim, `aria-modal`, Tab wraps inside, Esc closes, the focus comes back;
* in Arabic it stands on the left and arrives from there; under reduced motion it only fades;
* a row's act opens it on the Dépôt's field, and a filing reads the piece and the register again;
* after a swap the close keeps the person's place: the page where it was, the focus on the shown piece's row (REVIEW
  M1); the row pressed stays under the pointer, and the register marks the piece open (M2); the strip's act steps down
  while the drawer shows its piece (m2);
* a modified press keeps the link's own way; no inline style is written (CSP: 0), no console error.

Chromium on the test database; sessions minted with ``Client.force_login`` — nothing typed, no password used. The
first console page of a session carries the loader's entrance release (W1-D): each page is loaded once first.
"""

from __future__ import annotations

import datetime as dt
import os
from urllib.parse import urlsplit

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType
from core import clock

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PORTAL = "/{lang}/espace-reserve/mes-documents/"
MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)
CSP_HOOK = (
    "document.addEventListener('securitypolicyviolation', (e) => "
    "{ (window.__csp = window.__csp || []).push(e.violatedDirective + ' ' + e.blockedURI); });"
)
STATE = """() => {
  const d = document.querySelector('[data-piece-drawer]');
  const r = d.getBoundingClientRect();
  const coll = document.querySelector('.doc-collection');
  const cs = coll ? getComputedStyle(coll) : null;
  const scrim = document.querySelector('.overlay-scrim');
  return {
    url: location.pathname + location.search, hlen: history.length, open: d.open,
    mode: d.getAttribute('data-overlay-mode'), modal: d.getAttribute('aria-modal'),
    beside: document.querySelector('.console__workspace').hasAttribute('data-drawer-beside'),
    left: Math.round(r.left), right: Math.round(r.right), top: Math.round(r.top), width: Math.round(r.width),
    title: d.querySelector('[data-drawer-title]').textContent.trim(),
    line: d.querySelector('.doc-drawer__line').textContent.replace(/\\s+/g, ' ').trim(),
    body: !!d.querySelector('[data-drawer-body] article.doc-piece'),
    scrim: !!(scrim && scrim.hasAttribute('data-open')),
    tracks: cs && cs.display.includes('grid') ? cs.gridTemplateColumns.split(' ').filter((t) => /px$/.test(t)).length : 0,
    focusInDrawer: d.contains(document.activeElement),
    focusTitle: document.activeElement === document.getElementById('piece-drawer-title'),
    focusClass: document.activeElement.className,
    focusText: document.activeElement.textContent.trim().slice(0, 60),
  };
}"""


def _days(n: int) -> dt.date:
    return timezone.localdate() + dt.timedelta(days=n)


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


@pytest.fixture
def register(db, settings, tmp_path, user_factory):
    """A file with an open piece of the person's (missing), a refused one, a filed one and the authority's."""
    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services
    from documents.models import AccessClass, VersionDecision

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    person = user_factory(
        "drawer.person@example.test",
        role=roles.PERSON,
        full_name="Tiroir PERSONNE",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    reviewer = user_factory("drawer.reviewer@example.test", role=roles.STAFF, is_staff=True)
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")

    def piece(code, title, actor="person", due=None):
        return services.declare_requirement(
            case, code=code, title=title, responsible_actor=actor, due_date=due, access_class=AccessClass.CASE
        )

    def deposit(requirement):
        return services.file_version(requirement, person, SimpleUploadedFile("p.pdf", MINIMAL_PDF, "application/pdf"))

    piece("passport", "Passeport en cours de validité", due=_days(20))
    refused = deposit(piece("diploma", "Diplôme ou titre de formation", due=_days(-3)))
    services.set_decision(refused, VersionDecision.REFUSED, actor=reviewer, note="Copie partielle : page 2 absente.")
    deposit(piece("contract", "Proposition de contrat de travail", due=_days(40)))
    piece("nulla_osta", "Nulla osta au travail", actor="authority", due=_days(90))
    return person


def _open(browser, live_server, user, lang="fr", width=1440, height=900, phone=False, reduced=False, query=""):
    client = Client()
    client.force_login(user)
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
    if phone:
        options.update(is_mobile=True, has_touch=True)
    if reduced:
        options["reduced_motion"] = "reduce"
    context = browser.new_context(**options)
    context.add_cookies(
        [
            {
                "name": settings.SESSION_COOKIE_NAME,
                "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
                "url": live_server.url,
            }
        ]
    )
    page = context.new_page()
    page.add_init_script(CSP_HOOK)
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    url = live_server.url + PORTAL.format(lang=lang) + query
    page.goto(url, wait_until="load")
    page.goto(url, wait_until="load")
    page.wait_for_function(
        "() => document.querySelector('[data-piece-drawer]')?.hasAttribute('data-piece-drawer-ready')"
    )
    return context, page, errors


def _loaded(page):
    page.wait_for_function(
        "() => { const d = document.querySelector('[data-piece-drawer]'); return d.open && d.querySelector('[data-drawer-body] article.doc-piece'); }",
        timeout=15000,
    )
    page.wait_for_timeout(450)  # the slide's 320 ms


def _clean(page, errors):
    assert not errors, errors
    assert page.evaluate("window.__csp || []") == []


def test_a_row_opens_its_piece_beside_the_register_with_its_head_at_once(browser, live_server, register):
    context, page, errors = _open(browser, live_server, register)
    try:
        before = page.evaluate(STATE)
        assert before["tracks"] == 6 and not before["open"]
        row = page.locator(".doc-row__link", has_text="Diplôme ou titre de formation")
        row.click()
        at_once = page.evaluate(STATE)
        assert at_once["title"] == "Diplôme ou titre de formation", "the head is filled from the row, at 0 ms"
        assert "Non valide" in at_once["line"]
        _loaded(page)
        state = page.evaluate(STATE)
        assert state["url"].startswith("/documents/requirements/") and state["hlen"] == before["hlen"] + 1
        assert state["open"] and state["modal"] is None and not state["scrim"], "non-modal beside the list: no trap"
        assert state["beside"] and state["right"] == 1440 and state["width"] == 420 and state["top"] == 0
        assert state["tracks"] in (0, 5), "the register lays itself out by the width it is left"
        assert state["focusTitle"], "a non-modal drawer takes its title"
        assert state["body"]
        assert page.locator("[data-drawer-body] [data-piece-head]").first.is_hidden(), "the head's facts, not twice"
        _clean(page, errors)
    finally:
        context.close()


def test_a_swap_replaces_the_history_entry_and_leaves_the_focus_in_the_list(browser, live_server, register):
    context, page, errors = _open(browser, live_server, register)
    try:
        page.locator(".doc-row__link", has_text="Passeport").click()
        _loaded(page)
        first = page.evaluate(STATE)
        other = page.locator(".doc-row__link", has_text="Proposition de contrat")
        other.focus()
        page.keyboard.press("Enter")
        page.wait_for_function(
            "() => document.querySelector('[data-drawer-title]').textContent.includes('Proposition de contrat')"
        )
        _loaded(page)
        second = page.evaluate(STATE)
        assert second["hlen"] == first["hlen"] and second["url"] != first["url"], "replaceState on a swap"
        assert "doc-row__link" in second["focusClass"], "the focus stays where the person is"
        _clean(page, errors)
    finally:
        context.close()


@pytest.mark.parametrize("how", ["esc", "close", "back"])
def test_esc_fermer_and_back_close_it_and_the_registers_url_comes_back_with_its_filter(
    browser, live_server, register, how
):
    context, page, errors = _open(browser, live_server, register, query="?état=invalid")
    try:
        start = page.evaluate(STATE)["url"]
        page.locator(".doc-row__link").first.click()
        _loaded(page)
        if how == "esc":
            page.keyboard.press("Escape")
        elif how == "close":
            page.locator("[data-piece-drawer] .overlay__close").click()
        else:
            page.go_back()
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        page.wait_for_timeout(300)
        state = page.evaluate(STATE)
        assert state["url"] == start and "%C3%A9tat=invalid" in state["url"], "the register's URL, its ?état= kept"
        assert not state["beside"] and state["tracks"] == 6
        if how != "back":
            assert "doc-row__link" in state["focusClass"], "the focus back on the row's title"
        _clean(page, errors)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_on_a_phone_the_drawer_is_a_modal_sheet_that_holds_the_focus(browser, live_server, register, lang):
    context, page, errors = _open(browser, live_server, register, lang=lang, width=390, height=844, phone=True)
    try:
        page.locator(".doc-row__link").first.click()
        _loaded(page)
        state = page.evaluate(STATE)
        assert state["mode"] == "sheet" and state["modal"] == "true" and state["scrim"] and not state["beside"]
        for _ in range(6):
            page.keyboard.press("Tab")
            assert page.evaluate(STATE)["focusInDrawer"], "Tab wraps inside the sheet"
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        assert "doc-row__link" in page.evaluate(STATE)["focusClass"]
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 0
        _clean(page, errors)
    finally:
        context.close()


def test_in_arabic_it_stands_on_the_left_and_under_reduced_motion_it_only_fades(browser, live_server, register):
    context, page, errors = _open(browser, live_server, register, lang="ar")
    try:
        page.locator(".doc-row__link").first.click()
        _loaded(page)
        state = page.evaluate(STATE)
        assert state["left"] == 0 and state["width"] == 420, "the inline end of an Arabic page is its left"
        _clean(page, errors)
    finally:
        context.close()
    context, page, errors = _open(browser, live_server, register, reduced=True)
    try:
        page.locator(".doc-row__link").first.click()
        motion = page.evaluate(
            """() => { const cs = getComputedStyle(document.querySelector('[data-piece-drawer]'));
              return {translate: cs.translate, properties: cs.transitionProperty}; }"""
        )
        assert motion["translate"] == "none" and "opacity" in motion["properties"], motion
        _loaded(page)
        _clean(page, errors)
    finally:
        context.close()


def test_a_rows_act_opens_it_on_the_depot_and_a_filing_reads_the_piece_and_the_register_again(
    browser, live_server, register
):
    context, page, errors = _open(browser, live_server, register)
    try:
        act = page.locator(".doc-row__act a").first
        act.click()
        _loaded(page)
        assert page.evaluate("document.activeElement.type") == "file", "the act's way: the Dépôt's field"
        title = page.evaluate("document.querySelector('[data-drawer-title]').textContent.trim()")
        page.set_input_files(
            "[data-piece-drawer] [data-depot] input[type=file]",
            {"name": "piece.pdf", "mimeType": "application/pdf", "buffer": MINIMAL_PDF},
        )
        page.click("[data-piece-drawer] [data-depot-submit]")
        page.wait_for_function(
            "() => (document.querySelector('[data-piece-drawer] [data-piece-answer]') || {}).textContent", timeout=20000
        )
        page.wait_for_function("() => document.querySelector('.doc-drawer__line').textContent.includes('Déposé')")
        # the announcement follows the answer by a moment (depot.js `say`)
        page.wait_for_function(
            "() => document.querySelector('[data-piece-drawer] [data-depot-live=polite]').textContent"
        )
        state = page.evaluate(
            """(title) => ({
              answer: document.querySelector('[data-piece-drawer] [data-piece-answer]').textContent.trim(),
              live: document.querySelector('[data-piece-drawer] [data-depot-live=polite]').textContent,
              row: [...document.querySelectorAll('.doc-row')].find((row) => row.querySelector('.doc-row__link').textContent.trim() === title)
                .querySelector('.doc-row__state .chip__w').textContent.trim(),
              focus: document.activeElement.textContent.trim() })""",
            title,
        )
        assert state["answer"].startswith("Pièce déposée (version") and state["live"] == state["answer"]
        assert state["row"] == "Déposé", "the register behind the drawer is read again"
        assert state["focus"] == "État de la pièce"
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        assert page.evaluate("document.activeElement.textContent.trim()") == title, "the focus on the fresh row"
        _clean(page, errors)
    finally:
        context.close()


#: Where a row stands, and whether it holds the focus — read by its title.
PLACE = """(title) => {
  const link = [...document.querySelectorAll('.doc-row__link')].find((l) => l.textContent.trim() === title);
  const r = link.getBoundingClientRect();
  return { y: Math.round(scrollY), top: Math.round(r.top), bottom: Math.round(r.bottom), vh: innerHeight,
    focused: document.activeElement === link, focusText: document.activeElement.textContent.trim().slice(0, 60) };
}"""
#: What the register says of the piece the drawer shows.
MARKS = """([x, y]) => {
  const el = document.elementFromPoint(x, y);
  const row = el && el.closest('.doc-row');
  return { under: row ? row.querySelector('.doc-row__link').textContent.trim() : null,
    current: [...document.querySelectorAll('.doc-row__link[aria-current="true"]')].map((l) => l.textContent.trim()),
    open: [...document.querySelectorAll('.doc-row[data-drawer-open]')].map((r) => r.querySelector('.doc-row__link').textContent.trim()) };
}"""


@pytest.mark.parametrize(
    ("how", "lang"), [("fermer", "fr"), ("esc-inside", "fr"), ("esc-list", "fr"), ("back", "fr"), ("esc-list", "ar")]
)
def test_after_a_swap_the_close_keeps_the_place_and_gives_the_focus_to_the_shown_pieces_row(
    browser, live_server, register, how, lang
):
    """REVIEW M1, A11Y_PERF finding 1 — the keyboard path: Enter on a row opens the drawer, the focus goes back into the
    list to a lower row, Enter swaps the piece; then «Fermer», Esc from the drawer, Esc from the list or Back. The page
    stays where the person is (it was thrown to the scroll of the first opening) and the focus is on the row of the
    piece shown, inside the viewport (it was on the first row opened, or 1 060 px below the fold)."""
    context, page, errors = _open(browser, live_server, register, lang=lang, height=560)
    try:
        links = page.locator(".doc-row__link")
        target = links.nth(2)
        title = target.text_content().strip()
        links.first.focus()
        page.keyboard.press("Enter")
        _loaded(page)
        target.focus()  # back in the list, lower down: the page scrolls to it
        page.keyboard.press("Enter")
        page.wait_for_function(
            "(t) => document.querySelector('[data-drawer-title]').textContent.trim() === t", arg=title
        )
        _loaded(page)
        before = page.evaluate(PLACE, title)
        assert before["y"] > 0 and before["focused"], before
        if how == "fermer":
            page.locator("[data-piece-drawer] .overlay__close").click()
        elif how == "esc-inside":
            page.focus("#piece-drawer-title")
            page.keyboard.press("Escape")
        elif how == "esc-list":
            page.keyboard.press("Escape")
        else:
            page.go_back()
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        page.wait_for_function("() => history.scrollRestoration === 'auto'")
        page.wait_for_timeout(300)
        after = page.evaluate(PLACE, title)
        assert after["focused"], f"the focus on the shown piece's row, not «{after['focusText']}»"
        assert 0 <= after["top"] and after["bottom"] <= after["vh"], f"the row in the viewport: {after}"
        assert after["y"] > 0, "the page is not thrown back to the scroll of the first opening"
        assert abs(after["top"] - before["top"]) <= 2, f"the row stays where it stood: {before} → {after}"
        _clean(page, errors)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_open_row_is_marked_and_stays_under_the_pointer(browser, live_server, register, lang):
    """REVIEW M2: the workspace makes room and the register lays itself out again (cards beside the drawer) — the row
    pressed stays under the pointer (the card that slid there read as the piece open), and the register says which
    piece is open: its title `aria-current`, the row in the selected state; a swap moves both, closing clears them."""
    context, page, errors = _open(browser, live_server, register, lang=lang)
    try:
        link = page.locator(".doc-row__link").nth(1)
        title = link.text_content().strip()
        box = link.bounding_box()
        point = [box["x"] + 12, box["y"] + box["height"] / 2]
        page.mouse.click(*point)
        _loaded(page)
        state = page.evaluate(MARKS, point)
        assert page.evaluate(STATE)["beside"], "the register laid itself out beside the drawer"
        assert state["under"] == title, f"the row pressed stays under the pointer: {state}"
        assert state["current"] == [title] and state["open"] == [title], state
        selected = page.evaluate(
            """() => { const row = document.querySelector('.doc-row[data-drawer-open]'); const cs = getComputedStyle(row);
              return { surface: cs.backgroundColor, rule: cs.boxShadow }; }"""
        )
        assert selected["surface"] != "rgba(0, 0, 0, 0)" and "inset" in selected["rule"], selected
        other = page.locator(".doc-row__link").first
        other_title = other.text_content().strip()
        other.click()
        page.wait_for_function(
            "(t) => document.querySelector('[data-drawer-title]').textContent.trim() === t", arg=other_title
        )
        page.wait_for_timeout(200)
        assert page.evaluate(MARKS, point)["current"] == [other_title], "a swap moves the mark"
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        page.wait_for_timeout(300)
        cleared = page.evaluate(MARKS, point)
        assert cleared["current"] == [] and cleared["open"] == [], "closing clears it"
        _clean(page, errors)
    finally:
        context.close()


def test_while_the_drawer_shows_the_strips_piece_its_act_steps_down(browser, live_server, register):
    """REVIEW m2: the strip's act and the drawer's «Déposer» were two primaries for one act — while the drawer shows the
    strip's piece, the strip's next piece takes the open row's state and its act steps down to a secondary."""
    context, page, errors = _open(browser, live_server, register)
    try:
        act = page.locator(".reg__next-act a")
        assert "btn--primary" in act.get_attribute("class")
        act.click()
        _loaded(page)
        state = page.evaluate(
            """() => ({ act: document.querySelector('.reg__next-act a').className,
              next: document.querySelector('.reg__next').hasAttribute('data-drawer-open'),
              primaries: [...document.querySelectorAll('.btn--primary')].filter((b) => b.getClientRects().length)
                .map((b) => b.closest('[data-piece-drawer]') ? 'drawer' : 'page') })"""
        )
        assert "btn--secondary" in state["act"] and "btn--primary" not in state["act"] and state["next"], state
        assert state["primaries"] == ["drawer"], "the drawer's «Déposer» is the one primary in view"
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.querySelector('[data-piece-drawer]').open")
        page.wait_for_timeout(300)
        assert "btn--primary" in act.get_attribute("class") and not page.evaluate(
            "() => document.querySelector('.reg__next').hasAttribute('data-drawer-open')"
        )
        _clean(page, errors)
    finally:
        context.close()


def test_a_modified_press_keeps_the_links_own_way(browser, live_server, register):
    context, page, errors = _open(browser, live_server, register)
    try:
        link = page.locator(".doc-row__link").first
        href = link.get_attribute("href")
        with context.expect_page() as other:
            link.click(modifiers=["Control"])
        # The link's own way: the new tab reaches the piece's page and loads it before it is closed. Closed at once (the
        # tab still on about:blank), its request was still being served when the test returned, and the transactional
        # flush's TRUNCATE deadlocked with it (integration checkpoint 3, docs/design-v5/QA/v54/intfix/NOTES.md).
        other.value.wait_for_url(lambda url: urlsplit(url).path == urlsplit(href).path, wait_until="load")
        other.value.close()
        assert not page.evaluate(STATE)["open"], "a new tab is the person's choice: the drawer stays closed"
        _clean(page, errors)
    finally:
        context.close()
