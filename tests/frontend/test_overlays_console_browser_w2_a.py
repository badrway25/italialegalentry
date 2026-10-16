"""
The overlay system on the console's pages, in the browser — design V5, family W2-A, step 2 (the propagation;
docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14, §3.4 item 1; docs/design-v5/QA/v54/w2-a/CONTRACT.md). What the board's
tests (tests/frontend/test_overlays_browser_w2_a.py) cannot see, on real pages with real accounts:

* the console drawer: the trap (Tab wraps, a focus sent outside comes back, the page behind takes no press), and the
  way out keeping the panel's shape while it slides (B1) and taking no click (B2), the focus back on «Menu»;
* the account popover: hanging from its trigger in the band (its inline end on the trigger's, in both directions),
  the focus on its first row, the arrows, Esc and the focus back, a press outside; a sheet on a phone that stays a
  menu over the one scrim, headed by its name;
* a menu sheet takes the whole press that dismisses it (the review's M1): a tap on the search field or on a filter
  link above the row menu's sheet closes the menu and reaches nothing — no field focused, no link followed;
* the drawer brings the focus into its own view (A11Y_PERF M1: «Academy», the rail's last page, at 390 × 844 and on
  a phone on its side, and Shift+Tab across the wrap), and takes the page behind out of the accessibility tree
  (M2: aria-hidden, the landmarks left are the dialog's);
* the row menu of «Mes documents»: «⋮» named by the top-layer tooltip after the wait, the menu 4 px under its button
  on its inline end (fr and ar), no tip while it is open, the focus back on «⋮»;
* O11 in the product: the compact rail's word is the system's one top-layer tip — whole, beyond the rail, hoverable,
  put away by Esc wherever the focus is — and it follows the keyboard down a list that scrolls (A11Y_PERF M3).

W3-A's own behaviours of the drawer and the rail's word are tests/frontend/test_console_phone_browser_w3_a.py and
test_console_shell_browser_w3_a.py. Chromium on the seeded site; a session minted with ``Client.force_login`` —
nothing typed, no password used.
"""

from __future__ import annotations

import os

import pytest
from django.conf import settings
from django.test import Client

from accounts import roles

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

REQUESTS = "/{lang}/espace-reserve/mes-demandes/"
DOCUMENTS = "/{lang}/espace-reserve/mes-documents/"
DASHBOARD = "/{lang}/espace-reserve/"
ACADEMY = "/{lang}/espace-reserve/formation/"

BOX = """(sel) => { const el = typeof sel === 'string' ? document.querySelector(sel) : sel; const r = el.getBoundingClientRect();
  return {x: r.left, r: r.right, top: r.top, b: r.bottom, w: r.width, h: r.height}; }"""
FOCUS = """() => { const a = document.activeElement;
  return a ? {id: a.id, cls: String(a.className), key: a.dataset ? a.dataset.key || '' : '', text: (a.textContent || '').trim().slice(0, 40)} : null; }"""
TIP = """() => { const t = document.querySelector('.tooltip'); if (!t || !t.matches(':popover-open')) return null;
  const r = t.getBoundingClientRect();
  return {text: t.textContent, x: r.left, r: r.right, top: r.top, b: r.bottom, fits: t.scrollWidth <= t.clientWidth + 1,
          count: document.querySelectorAll('.tooltip').length, legacy: document.querySelectorAll('.rail__tip').length}; }"""


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
def person(user_factory):
    return user_factory("w2a-b-person@example.test", role=roles.PERSON, full_name="Personne de test")


@pytest.fixture
def requirement(person):
    from cases.models import CasePurpose, ResponsibleActor
    from cases.services import open_case
    from documents import services
    from documents.models import DocumentKind

    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return services.declare_requirement(
        case,
        code="identity_document",
        title="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        kind=DocumentKind.IDENTITY,
        source_title="D.lgs. 286/1998",
        source_ref="art. 4, comma 1",
    )


def _context(browser, live_server, user, width, height, touch=False, stored=None, **options):
    client = Client()
    client.force_login(user)
    if touch:
        options.setdefault("has_touch", True)
        options.setdefault("is_mobile", True)
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **options)
    context.add_cookies(
        [
            {
                "name": settings.SESSION_COOKIE_NAME,
                "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
                "url": live_server.url,
            }
        ]
    )
    if stored:
        context.add_init_script(f"try {{ localStorage.setItem('ile.rail', '{stored}'); }} catch (e) {{}}")
    return context


def _at_rest(page, live_server, path):
    """Loaded twice: the session's first console page plays the entrance release, the second is at rest."""
    page.goto(live_server.url + path, wait_until="networkidle")
    page.goto(live_server.url + path, wait_until="networkidle")
    page.wait_for_function("() => document.body.classList.contains('is-ready')")


def _settled(page, selector):
    page.wait_for_function(
        "(s) => { const el = document.querySelector(s); return el && el.getAnimations().every((a) => a.playState !== 'running'); }",
        arg=selector,
    )


# ---------------------------------------------------------------------------------------------- the console drawer


def test_the_drawer_traps_the_focus_and_keeps_its_shape_while_it_leaves(browser, live_server, seeded, person):
    context = _context(browser, live_server, person, 390, 844, touch=True)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.click("#console-menu")
    page.wait_for_selector("dialog.console-drawer[open]")
    _settled(page, "dialog.console-drawer")
    state = page.evaluate(
        """() => { const d = document.querySelector('dialog.console-drawer'); const s = document.querySelector('.overlay-scrim');
          return {modal: d.getAttribute('aria-modal'), native: d.matches(':modal'), z: +getComputedStyle(d).zIndex,
                  scrim: s && s.hasAttribute('data-open') ? +getComputedStyle(s).zIndex : null, kind: s && s.dataset.kind,
                  behind: document.elementFromPoint(370, 400) === s, lock: document.documentElement.hasAttribute('data-overlay-lock')}; }"""
    )
    assert state["modal"] == "true" and not state["native"], "a modal drawer by the system's trap (the INP rule)"
    assert state["scrim"] == state["z"] - 1 and state["kind"] == "drawer", (
        "the one scrim, right under it, on its clocks"
    )
    assert state["behind"] and state["lock"], "the page behind takes no press and does not scroll"
    inside = "() => document.querySelector('dialog.console-drawer').contains(document.activeElement)"
    for _ in range(25):
        page.keyboard.press("Tab")
        assert page.evaluate(inside), "Tab wraps inside the drawer"
    for _ in range(3):
        page.keyboard.press("Shift+Tab")
        assert page.evaluate(inside), "and so does Shift+Tab"
    page.evaluate("document.getElementById('main-content').focus()")
    assert page.evaluate(inside), "a focus sent outside comes back"
    # the way out, by the pointer (the keyboard's is at once): the panel keeps its shape and takes no click (B1, B2)
    page.click("[data-console-close]")
    leaving = page.evaluate(
        """() => { const d = document.querySelector('dialog.console-drawer'); const r = d.getBoundingClientRect(); const s = getComputedStyle(d);
          return {open: d.open, display: s.display, w: Math.round(r.width), h: Math.round(r.height), inert: d.inert,
                  radius: s.borderTopRightRadius, bg: s.backgroundColor}; }"""
    )
    assert not leaving["open"] and leaving["inert"], "closed at once, and the leaving panel takes nothing"
    if leaving["display"] != "none":  # caught on its way out: its shape and its night, not the page's flow
        assert leaving["w"] == 320 and leaving["h"] == 844 and leaving["radius"] == "12px", leaving
    page.wait_for_function("() => getComputedStyle(document.querySelector('dialog.console-drawer')).display === 'none'")
    assert page.evaluate(FOCUS)["id"] == "console-menu", "the focus back on «Menu»"
    assert not page.evaluate("document.documentElement.hasAttribute('data-overlay-lock')")
    context.close()


#: The drawer as the system holds it, read once the next frames have run — the frame that brings the platform's
#: `close` event of a dialog closed during the frame before.
REOPENED = """async () => {
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const d = document.getElementById('console-drawer'); const s = document.querySelector('.overlay-scrim');
  return {open: d.open, modal: d.getAttribute('aria-modal'), inert: d.inert, scrim: Boolean(s && s.hasAttribute('data-open')),
          behind: document.elementFromPoint(370, 400) === s, lock: document.documentElement.hasAttribute('data-overlay-lock'),
          focus: d.contains(document.activeElement), expanded: document.getElementById('console-menu').getAttribute('aria-expanded')};
}"""
#: The trap, whole: drawn and modal, its scrim under it and in the press's way, the page locked, the focus inside.
TRAP = {
    "open": True,
    "modal": "true",
    "inert": False,
    "scrim": True,
    "behind": True,
    "lock": True,
    "focus": True,
    "expanded": "true",
}


def test_a_drawer_closed_and_opened_again_within_a_frame_keeps_its_trap_and_a_press_on_the_scrim_closes_it(
    browser, live_server, seeded, person
):
    """The integration fix (c) (docs/design-v5/QA/v54/intfix/NOTES.md). A dialog's `close` event is the platform's, and
    it comes late — Chromium dispatches it with the next frame's events —, and the system settled every close it heard:
    a drawer closed and opened again within one frame heard its first close while it was open again, and lost its trap
    — the scrim, the lock and aria-modal gone, the panel made inert, the focus sent back to «Menu» — while it stayed
    drawn over the page; a press on the dimmed page reached the page and the drawer stayed (W3-A's «Menu» test failed 2
    runs in 3 on design-v5). Esc then Space pressed behind one frame, twelve times over; the same close and opening in
    one task through the module's API; and a close by another script, not yet heard, before the system opens it again:
    each time the drawer is the whole trap, a press on the scrim closes it, and the page is given back."""
    context = _context(browser, live_server, person, 390, 844, touch=True)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    closed = "dialog.console-drawer:not([open])"

    def scrim_closes(how):
        state = page.evaluate(REOPENED)
        assert state == TRAP, (how, state)
        page.mouse.click(370, 400)
        page.wait_for_selector(closed, state="attached", timeout=2000)
        assert page.evaluate(FOCUS)["id"] == "console-menu", (how, "the focus back on «Menu»")

    page.focus("#console-menu")
    for attempt in range(1, 13):
        page.keyboard.press("Enter")
        page.wait_for_selector("dialog.console-drawer[open]")
        page.evaluate("() => new Promise((resolve) => requestAnimationFrame(() => resolve()))")
        page.keyboard.press("Escape")  # the two keys land between two frames: the Esc's close is heard after Space
        page.keyboard.press("Space")
        scrim_closes(f"Esc then Space, attempt {attempt}")
    assert not page.evaluate("document.documentElement.hasAttribute('data-overlay-lock')"), "the page is given back"

    # the API in one task (a page that closes a panel and opens it again), then a close by another script that the
    # system has not heard yet when it opens the panel again: the opening settles it first — its lock is not left behind
    module = page.evaluate(
        "() => document.querySelector('script[src*=\"js/dist/console.js\"]').src.replace('/console.js', '/overlay.js')"
    )
    for how, closing in (("the API, close then open", "m.close(d)"), ("another script's close", "d.close()")):
        page.keyboard.press("Enter")
        page.wait_for_selector("dialog.console-drawer[open]")
        page.evaluate(
            f"""async (url) => {{ const m = await import(url); const d = document.getElementById('console-drawer');
              {closing}; m.open(d, {{opener: document.getElementById('console-menu')}}); }}""",
            module,
        )
        scrim_closes(how)
        page.wait_for_function("() => getComputedStyle(document.getElementById('console-drawer')).display === 'none'")
        assert not page.evaluate("document.documentElement.hasAttribute('data-overlay-lock')"), (
            how,
            "the page given back",
        )
    context.close()


# ---------------------------------------------------------------------------------------------- the drawer's focus, its tree

DRAWER_VIEW = """() => { const a = document.activeElement; const d = document.getElementById('console-drawer');
  if (!a || !d.contains(a) || a === d) return {inside: false};
  const r = a.getBoundingClientRect(); let top = Math.max(0, d.getBoundingClientRect().top), bottom = innerHeight;
  for (let n = a.parentElement; n && n !== d.parentElement; n = n.parentElement) {
    if (/(auto|scroll|hidden)/.test(getComputedStyle(n).overflowY)) { const b = n.getBoundingClientRect();
      top = Math.max(top, b.top); bottom = Math.min(bottom, b.bottom); } }
  const seen = Math.max(0, Math.min(r.bottom, bottom) - Math.max(r.top, top)) / Math.max(1, r.height);
  const list = d.querySelector('.rail__scroll');
  return {inside: true, seen, text: (a.textContent || '').trim(), scrollY: scrollY, scrollX: scrollX,
          overflows: [...d.querySelectorAll('.rail__scroll, .rail--drawer')].some((s) => s.scrollHeight > s.clientHeight + 1)}; }"""


@pytest.mark.parametrize(("width", "height"), [(390, 844), (844, 390)])
def test_the_drawer_brings_the_focused_entry_into_its_view(browser, live_server, seeded, superuser, width, height):
    """A11Y_PERF M1: «Academy» is every rail's last page; on it the staff account's drawer opened with the focus on a
    row out of the list's view (WCAG 2.4.7). The module moves the focus without scrolling the page and brings it into
    the drawer's own view — by the pointer and by the keyboard; and Shift+Tab across the wrap lands in view too."""
    for how in ("tap", "key"):
        context = _context(browser, live_server, superuser, width, height, touch=True)
        page = context.new_page()
        _at_rest(page, live_server, ACADEMY.format(lang="fr"))
        if how == "tap":
            page.tap("#console-menu")
        else:
            page.focus("#console-menu")
            page.keyboard.press("Enter")
        page.wait_for_selector("dialog.console-drawer[open]")
        _settled(page, "dialog.console-drawer")
        view = page.evaluate(DRAWER_VIEW)
        assert view["inside"] and view["overflows"], ("a drawer whose list scrolls, the focus in it", how, view)
        assert view["text"] == "Academy" and view["seen"] == 1, (
            "the current page, whole in the drawer's view",
            how,
            view,
        )
        assert view["scrollY"] == 0 and view["scrollX"] == 0, ("the page behind did not move", how, view)
        if how == "key" and height < 500:
            page.evaluate(
                "() => document.querySelector('dialog.console-drawer').querySelector('a[href], button, summary').focus()"
            )
            page.keyboard.press("Shift+Tab")
            wrap = page.evaluate(DRAWER_VIEW)
            assert wrap["inside"] and wrap["seen"] == 1 and wrap["scrollY"] == 0, ("Shift+Tab's wrap, in view", wrap)
        context.close()


def test_the_page_behind_the_drawer_leaves_the_accessibility_tree(browser, live_server, seeded, person):
    """A11Y_PERF M2: the trapped drawer is show() + aria-modal, and Chromium prunes nothing for aria-modal: the page
    behind stays readable by a screen reader's virtual cursor. While the drawer is open every other child of the body is
    aria-hidden — the landmarks left are the dialog's —; closed, the page is whole again and the focus is on «Menu»."""
    context = _context(browser, live_server, person, 390, 844, touch=True)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    cdp = context.new_cdp_session(page)

    def landmarks():
        nodes = cdp.send("Accessibility.getFullAXTree")["nodes"]
        roles = ("main", "banner", "contentinfo", "navigation", "dialog")
        return sorted(
            (n.get("role") or {}).get("value")
            for n in nodes
            if not n.get("ignored") and (n.get("role") or {}).get("value") in roles
        )

    before = landmarks()
    assert {"banner", "main", "contentinfo"} <= set(before), before
    page.tap("#console-menu")
    page.wait_for_selector("dialog.console-drawer[open]")
    _settled(page, "dialog.console-drawer")
    hidden = page.evaluate(
        """() => [...document.body.children].filter((e) => !['SCRIPT', 'STYLE', 'TEMPLATE'].includes(e.tagName))
          .map((e) => [e.id || e.className.split(' ')[0] || e.tagName, e.getAttribute('aria-hidden')])"""
    )
    for who, flag in hidden:
        if who == "console-drawer":
            assert flag is None, "the drawer itself is read"
        else:
            assert flag == "true", (who, "the page behind the drawer is hidden from assistive technology")
    assert landmarks() == ["dialog", "navigation"], "only the dialog and its «Menu» are read"
    assert page.evaluate("document.querySelector('dialog.console-drawer').contains(document.activeElement)")
    page.keyboard.press("Escape")
    page.wait_for_function("() => getComputedStyle(document.querySelector('dialog.console-drawer')).display === 'none'")
    assert landmarks() == before, "closed, the page is whole again"
    assert page.evaluate(
        "() => [...document.body.children].filter((e) => e.getAttribute('aria-hidden') === 'true').every((e) => e.matches('.overlay-scrim, .tooltip'))"
    ), "only what hides itself stays hidden"
    assert page.evaluate(FOCUS)["id"] == "console-menu"
    cdp.detach()
    context.close()


# ---------------------------------------------------------------------------------------------- the account popover


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_account_popover_hangs_from_its_trigger_in_the_band(browser, live_server, seeded, person, lang):
    context = _context(browser, live_server, person, 820, 1180)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    trigger = ".console-bar .account-menu__summary"
    assert page.get_attribute(trigger, "aria-expanded") == "false"
    page.click(trigger)
    page.wait_for_selector("#console-account:popover-open")
    _settled(page, "#console-account")
    panel, button = page.evaluate(BOX, "#console-account"), page.evaluate(BOX, trigger)
    assert page.get_attribute(trigger, "aria-expanded") == "true"
    assert abs(panel["top"] - (button["b"] + 4)) <= 1.5, (panel, button, "4 px under its trigger")
    if lang == "fr":
        assert abs(panel["r"] - button["r"]) <= 1.5, (panel, button, "its inline end on the trigger's")
    else:
        assert abs(panel["x"] - button["x"]) <= 1.5, (panel, button, "its inline end on the trigger's — the left one")
    assert panel["w"] >= 192 and panel["x"] >= 0 and panel["r"] <= 820
    focused = page.evaluate(FOCUS)
    assert "overlay__item" in focused["cls"], "the focus on its first row"
    first = focused["text"]
    page.keyboard.press("ArrowDown")
    assert page.evaluate(FOCUS)["text"] != first, "the arrows move between the rows"
    page.keyboard.press("Escape")
    page.wait_for_selector("#console-account", state="hidden")
    assert "account-menu__summary" in page.evaluate(FOCUS)["cls"], "Esc, and the focus back on the trigger"
    assert page.get_attribute(trigger, "aria-expanded") == "false"
    # a press outside puts it away, and leaves the focus where the person put it
    page.click(trigger)
    page.wait_for_selector("#console-account:popover-open")
    page.mouse.click(400, 700)
    page.wait_for_selector("#console-account", state="hidden")
    context.close()


def test_on_a_phone_the_account_popover_is_a_sheet_that_stays_a_menu(browser, live_server, seeded, person):
    context = _context(browser, live_server, person, 390, 844, touch=True)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    page.tap(".console-bar .account-menu__summary")
    page.wait_for_selector("#console-account:popover-open")
    _settled(page, "#console-account")
    sheet = page.evaluate(BOX, "#console-account")
    assert sheet["x"] == 0 and sheet["r"] == 390 and sheet["b"] >= 844, (
        f"from the bottom edge, the whole width: {sheet}"
    )
    rows = page.evaluate(
        "() => [...document.querySelectorAll('#console-account .overlay__item')].map((i) => i.getBoundingClientRect().height)"
    )
    assert len(rows) == 4 and min(rows) >= 44, rows
    state = page.evaluate(
        """() => { const s = document.querySelector('.overlay-scrim'); const p = document.getElementById('console-account');
          const c = p.querySelector('.overlay__caption'); const first = p.querySelector('.overlay__item');
          return {scrim: Boolean(s && s.hasAttribute('data-open')), kind: s && s.dataset.kind,
                  caption: c && c.getClientRects().length ? c.textContent.trim() : null, label: p.getAttribute('aria-label'),
                  above: c ? c.getBoundingClientRect().bottom <= first.getBoundingClientRect().top + 1 : false,
                  modal: p.getAttribute('aria-modal'), lock: document.documentElement.hasAttribute('data-overlay-lock')}; }"""
    )
    assert state["scrim"] and state["kind"] == "sheet", ("a menu sheet stands over the one scrim (CONTRACT §2)", state)
    assert state["caption"] == state["label"] and state["above"], ("its name heads its rows", state)
    assert state["modal"] is None and not state["lock"], ("it stays a menu: no trap, no scroll lock", state)
    page.keyboard.press("Escape")
    page.wait_for_selector("#console-account", state="hidden")
    assert "account-menu__summary" in page.evaluate(FOCUS)["cls"], "Esc, and the focus back on the trigger"
    assert page.evaluate("!document.querySelector('.overlay-scrim[data-open]')")
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_menu_sheet_takes_the_whole_press_that_dismisses_it(browser, live_server, seeded, person, requirement, lang):
    """The review's M1 — retargeted by W3-C, intent kept: the register's rows have no menu any more (DOCUMENT_WORKSPACE
    D2), so the menu sheet is the account's, on the same «Mes pièces». Above it the page stays in sight, and the tap that
    dismisses the sheet lands on the scrim, which holds the whole press: the strip's act does not open the piece, a run
    of the register does not move the page."""
    context = _context(browser, live_server, person, 390, 844, touch=True)
    page = context.new_page()
    _at_rest(page, live_server, DOCUMENTS.format(lang=lang))
    menu = "#console-account"
    url = page.url

    def open_menu():
        page.tap(".console-bar .account-menu__summary")
        page.wait_for_selector(f"{menu}:popover-open")
        _settled(page, menu)

    def centre(selector):
        return page.evaluate(
            """([selector, menu]) => { const top = document.querySelector(menu).getBoundingClientRect().top;
              const e = [...document.querySelectorAll(selector)].find((x) => { const r = x.getBoundingClientRect();
                return r.height > 0 && r.top > 0 && r.bottom < top - 8 && r.left >= 0 && r.right <= innerWidth; });
              if (!e) return null; const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }""",
            [selector, menu],
        )

    state = """(menu) => ({open: document.querySelector(menu).matches(':popover-open'),
        drawer: Boolean(document.querySelector('#piece-drawer') && document.querySelector('#piece-drawer').open),
        held: Boolean(document.querySelector('.overlay-scrim[data-held]'))})"""
    for selector in (".reg__next-act a", "a.reg-run"):
        open_menu()
        target = centre(selector)
        assert target, f"{selector} stands above the sheet"
        page.touchscreen.tap(*target)
        page.wait_for_timeout(600)
        after = page.evaluate(state, menu)
        assert not after["open"] and not after["drawer"], (
            f"the tap closed the menu and reached nothing: {selector}",
            after,
        )
        assert not after["held"], "the scrim lets go of the page once its press has clicked"
        assert page.url == url, f"{selector} under the scrim was not followed"
    context.close()


# ---------------------------------------------------------------------------------------------- the register's row


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_rows_piece_opens_in_the_systems_drawer_beside_the_list(
    browser, live_server, seeded, person, requirement, lang
):
    """Retargeted by W3-C (intent kept: the register row's overlay is the system's, hangs on the right edge and gives
    the focus back): «Mes pièces» V5.2 has no row menu (DOCUMENT_WORKSPACE D2); the row's title opens the piece in the
    system's drawer — non-modal beside the list on desktop, at the inline end — and Esc gives the focus back."""
    context = _context(browser, live_server, person, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, DOCUMENTS.format(lang=lang))
    page.click(f".doc-row__link[href='/documents/requirements/{requirement.pk}/']")
    page.wait_for_function("() => document.querySelector('#piece-drawer').open")
    _settled(page, "#piece-drawer")
    drawer = page.evaluate(BOX, "#piece-drawer")
    if lang == "fr":
        assert abs(drawer["r"] - 1440) <= 1.5 and abs(drawer["w"] - 420) <= 1.5, drawer
    else:
        assert abs(drawer["x"]) <= 1.5 and abs(drawer["w"] - 420) <= 1.5, drawer
    assert page.evaluate("!document.querySelector('.overlay-scrim[data-open]')"), "beside the list: no scrim"
    assert page.evaluate(FOCUS)["id"] == "piece-drawer-title", "a non-modal drawer takes its title"
    page.keyboard.press("Escape")
    page.wait_for_function("() => !document.querySelector('#piece-drawer').open")
    assert "doc-row__link" in page.evaluate(FOCUS)["cls"], "the focus back on the row's title"
    context.close()


# ---------------------------------------------------------------------------------------------- O11


def test_the_compact_rails_word_is_the_systems_one_tip(browser, live_server, seeded, person):
    """Plan §1.14's O11: a tooltip on an icon-only control in the collapsed rail shown whole, hoverable and dismissed by
    Esc — the system's one top-layer tip, beyond the rail's edge."""
    context = _context(browser, live_server, person, 1440, 900, stored="closed")
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    item = "nav.rail[data-rail] [data-rail-item][data-key='documents']"
    page.hover(item)
    page.wait_for_function("() => document.querySelector('.tooltip:popover-open')", timeout=3000)
    tip = page.evaluate(TIP)
    label = page.get_attribute(item, "data-label")
    assert tip["text"] == label and tip["fits"] and tip["x"] >= 64, f"whole, beyond the rail's edge: {tip}"
    assert tip["count"] == 1 and tip["legacy"] == 0, "one tip for the whole page: the system's"
    page.hover(".tooltip")
    page.wait_for_timeout(300)
    assert page.evaluate(TIP) is not None, "the pointer may rest on it (WCAG 1.4.13)"
    focus_before = page.evaluate(FOCUS)
    page.keyboard.press("Escape")
    assert page.evaluate(TIP) is None, "Esc puts it away"
    assert page.evaluate(FOCUS) == focus_before, "without moving the focus"
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_compact_rails_word_follows_the_keyboard_down_a_list_that_scrolls(
    browser, live_server, seeded, superuser, lang
):
    """A11Y_PERF M3: on a short laptop the compact rail's list scrolls, and focusing an item scrolls it; the tip put
    itself away on that scroll, so two words were missing. Real Tab presses down the staff account's rail: a word for
    every item, beside it, and the list did scroll on the way."""
    context = _context(browser, live_server, superuser, 1366, 657, stored="closed")
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    scroller = "nav.rail[data-rail] [data-rail-scroll]"
    sizes = page.evaluate(
        f"() => {{ const s = document.querySelector('{scroller}'); return [s.scrollHeight, s.clientHeight]; }}"
    )
    assert sizes[0] > sizes[1] + 40, ("the compact rail's list scrolls at this height", sizes)
    page.evaluate("() => document.querySelector('nav.rail[data-rail] .rail__brand').focus()")
    words, missing, top = 0, [], 0
    for _ in range(60):
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)
        state = page.evaluate(
            f"""() => {{ const a = document.activeElement; const t = document.querySelector('.tooltip');
              const item = a && a.closest('{scroller} [data-rail-item]'); const tip = t && t.matches(':popover-open') ? t : null;
              const r = item && item.getBoundingClientRect(); const b = tip && tip.getBoundingClientRect();
              return {{inRail: Boolean(a && a.closest('nav.rail[data-rail]')), item: item ? item.dataset.label : null,
                       tip: tip ? tip.textContent : null, beside: Boolean(r && b && b.top < r.bottom && b.bottom > r.top),
                       scrolled: document.querySelector('{scroller}').scrollTop}}; }}"""
        )
        if not state["inRail"]:
            break
        top = max(top, state["scrolled"])
        if state["item"] is not None:
            if state["tip"] == state["item"] and state["beside"]:
                words += 1
            else:
                missing.append(state["item"])
    assert top > 0, "the walk scrolled the list"
    assert words > 8 and not missing, (f"a word for every item: {words} shown", missing)
    context.close()
