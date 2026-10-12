"""
The overlay system in a browser (design V5, family W2-A; docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14 O1–O11; the
contract docs/design-v5/QA/v54/w2-a/CONTRACT.md). What the sources cannot show:

* Esc closes every modal kind and the focus goes back to its opener; the focus goes in where the contract says
  (an alert's safe answer, the current entry, the first control, a non-modal drawer's title);
* the trap (the INP rule of plan §1.14: a modal kind opens with show(), `aria-modal`, one shared scrim and the trap in
  script — showModal() stays an opt-in): Tab and Shift+Tab stay inside the panel, a focus sent outside comes back, the
  page behind takes no press, does not scroll and does not shift; the native opt-in keeps the same behaviour;
* the scrim closes a dialog — never an alertdialog, never a dialog holding unsaved input;
* Back closes the drawer beside the list and leaves the address as it was; closing it another way takes its history
  entry back;
* a menu opens from its trigger, on the trigger's inline end, focuses its first row, follows the arrows, and every
  way out works (Esc, a choice, the focus leaving);
* O1–O3: the exit is a transition, the leaving panel takes no click and no Tab, a re-opening continues from the
  current pose; an opening from the keyboard shows no animation;
* O4: under reduced motion one opacity and no transform at any frame;
* the tooltip waits, warms its group, can be hovered, and leaves on Esc and on a press; the top-layer tip stands
  beyond the edge that would clip the ::after;
* «Fermer» is on every panel, 44 × 44; the grip drags a sheet away or back; on a phone the dialog and the menu are
  sheets — the menu over the one scrim, headed by its name —; at 400 % a dialog's body that scrolls with nothing to
  focus is a stop of its own; the JS API (open, close, toggle, isOpen, the events) does what it says;
* no CSP violation, no console error.

The page is the overlay board — real components, live strings — rendered by Django through a URL of this module
(the preview's own route answers only a DEBUG process). Chromium; Firefox and WebKit run the smoke when their
binaries are installed, never downloaded. The Arabic geometry is tests/i18n/test_rtl_browser_overlays.py.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path
from django.utils import translation

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

BOARD = "dev/designpreview/specimens/overlays.html"


def _board(request):
    with translation.override("it"):
        return HttpResponse(render_to_string(BOARD, {"board": "overlays"}))


urlpatterns = [path("overlay-board/", _board)]

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True), pytest.mark.urls(__name__)]

CSP_HOOK = """
window.__csp = [];
document.addEventListener('securitypolicyviolation', (e) => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI));
"""

#: What a panel looks like now: open (either kind), modal, inert, displayed, its box, the focus, the lock.
STATE_JS = """(id) => {
  const d = document.getElementById(id); const r = d.getBoundingClientRect(); const a = document.activeElement;
  let popover = false; try { popover = d.matches(':popover-open'); } catch (e) {}
  const scrim = document.querySelector('.overlay-scrim');
  return {open: Boolean(d.open) || popover, modal: d.matches(':modal'), trapped: d.getAttribute('aria-modal') === 'true',
          scrim: Boolean(scrim && scrim.hasAttribute('data-open')), inert: d.inert,
          display: getComputedStyle(d).display, box: {x: r.x, y: r.y, w: r.width, h: r.height, right: r.right, bottom: r.bottom},
          focusIn: d.contains(a), focus: a ? ((a.getAttribute('aria-label') || a.textContent || a.value || '').trim()) : '',
          focusTag: a ? a.tagName : '', lock: document.documentElement.getAttribute('data-overlay-lock')};
}"""


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
def board(browser, live_server):
    """The board at 1440 × 900, with the console and the CSP watched. Yields (page, problems)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    context.add_init_script(CSP_HOOK)
    page = context.new_page()
    problems: list[str] = []
    page.on("console", lambda m: problems.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: problems.append(f"pageerror: {e}"))
    page.goto(f"{live_server.url}/overlay-board/", wait_until="networkidle")
    page.evaluate("async () => { await document.fonts.ready }")
    try:
        yield page, problems
    finally:
        context.close()


def _state(page, panel_id: str) -> dict:
    return page.evaluate(STATE_JS, panel_id)


def _press_open(page, opener: str) -> None:
    """Open from the keyboard: the opener focused, then Enter."""
    page.focus(opener)
    page.keyboard.press("Enter")


def _settle(page, ms: int = 450) -> None:
    page.wait_for_timeout(ms)


# ---- Esc, the focus in and back ----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("panel", "expected_focus"),
    [
        ("ob-alert-fr", "Annuler"),  # an alert's safe answer
        ("ob-need-fr", "INPUT"),  # the first control of the body
        ("ob-nav-fr", "Tableau de bord"),  # the current entry
        ("ob-sheet-fr", "Français"),  # the current language
        ("ob-detail-fr", "Mes documents"),  # a drawer beside the list: its title
    ],
)
def test_esc_closes_every_modal_kind_and_the_focus_goes_back_to_its_opener(board, panel, expected_focus):
    page, problems = board
    opener = f'a[href="#{panel}"]'
    _press_open(page, opener)
    state = _state(page, panel)
    assert state["open"] and state["focusIn"], state
    if expected_focus == "INPUT":
        assert state["focusTag"] == "INPUT", state
    else:
        assert state["focus"] == expected_focus, state
    assert page.get_attribute(opener, "aria-expanded") == "true"
    page.keyboard.press("Escape")
    _settle(page)
    state = _state(page, panel)
    assert not state["open"] and state["lock"] is None, state
    assert page.evaluate("(sel) => document.activeElement === document.querySelector(sel)", opener), (
        "the focus went back"
    )
    assert page.get_attribute(opener, "aria-expanded") == "false"
    assert not problems and page.evaluate("window.__csp") == []


# ---- the trap, the inert and still page ----------------------------------------------------------------------------


def test_the_trap_keeps_tab_inside_a_modal_panel(board):
    page, _ = board
    _press_open(page, 'a[href="#ob-need-fr"]')
    for _ in range(7):
        page.keyboard.press("Tab")
        assert _state(page, "ob-need-fr")["focusIn"], "Tab left the modal panel"
    page.focus("#ob-need-fr .overlay__close")
    page.keyboard.press("Shift+Tab")
    state = _state(page, "ob-need-fr")
    assert state["focusIn"] and state["focus"] == "Retirer le besoin", ("Shift+Tab wraps to the last control", state)


def test_the_native_opt_in_is_a_real_modal_with_the_same_behaviour(board):
    """`data-overlay-modal="native"`: showModal() — the platform's inertness — with the same focus, trap, Esc and return."""
    page, _ = board
    page.evaluate("document.getElementById('ob-need-fr').setAttribute('data-overlay-modal', 'native')")
    _press_open(page, 'a[href="#ob-need-fr"]')
    state = _state(page, "ob-need-fr")
    assert state["modal"] and not state["trapped"] and not state["scrim"] and state["focusTag"] == "INPUT", state
    for _ in range(5):
        page.keyboard.press("Tab")
        assert _state(page, "ob-need-fr")["focusIn"]
    page.keyboard.press("Escape")
    _settle(page)
    assert not _state(page, "ob-need-fr")["open"]
    assert page.evaluate("document.activeElement === document.querySelector('a[href=\"#ob-need-fr\"]')")


def test_the_page_behind_a_modal_is_inert_still_and_does_not_shift(board):
    page, _ = board
    page.evaluate("window.scrollTo(0, 240)")
    before = page.evaluate(
        "() => ({y: scrollY, x: document.querySelector('.ob__section').getBoundingClientRect().x, w: document.documentElement.clientWidth})"
    )
    page.click('a[href="#ob-need-fr"]')
    _settle(page)
    state = _state(page, "ob-need-fr")
    assert state["trapped"] and state["scrim"] and not state["modal"] and state["lock"] is not None, state
    assert page.evaluate("getComputedStyle(document.documentElement).overflow") == "hidden"
    page.mouse.wheel(0, 600)
    _settle(page, 200)
    after = page.evaluate(
        "() => ({y: scrollY, x: document.querySelector('.ob__section').getBoundingClientRect().x, w: document.documentElement.clientWidth})"
    )
    assert after == before, ("the page behind neither scrolls nor moves sideways", before, after)
    # a press on the page behind lands on the scrim, under the panel
    hit = page.evaluate("() => { const e = document.elementFromPoint(20, 20); return e && e.className; }")
    assert hit == "overlay-scrim", hit
    panel_z, scrim_z = page.evaluate(
        "() => [getComputedStyle(document.getElementById('ob-need-fr')).zIndex, getComputedStyle(document.querySelector('.overlay-scrim')).zIndex]"
    )
    assert int(panel_z) == int(scrim_z) + 1, (panel_z, scrim_z)
    # a focus sent outside the panel comes back into it
    page.evaluate("document.querySelector('a[href=\"#ob-alert-fr\"]').focus()")
    assert _state(page, "ob-need-fr")["focusIn"], "the trap brings the focus back"
    page.keyboard.press("Escape")
    _settle(page)
    assert page.evaluate("document.documentElement.hasAttribute('data-overlay-lock')") is False


# ---- the scrim -----------------------------------------------------------------------------------------------------


def test_the_scrim_closes_a_dialog_never_an_alert_nor_unsaved_input(board):
    page, _ = board
    page.click('a[href="#ob-need-fr"]')
    _settle(page)
    page.mouse.click(12, 12)
    _settle(page)
    assert not _state(page, "ob-need-fr")["open"], "a press on the scrim closes the dialog"

    page.click('a[href="#ob-alert-fr"]')
    _settle(page)
    page.mouse.click(12, 12)
    _settle(page)
    assert _state(page, "ob-alert-fr")["open"], "an alertdialog never closes on its scrim"
    page.keyboard.press("Escape")
    _settle(page)
    assert not _state(page, "ob-alert-fr")["open"], "and its Esc is the safe answer"

    page.click('a[href="#ob-need-fr"]')
    _settle(page)
    page.keyboard.type("motif")
    page.mouse.click(12, 12)
    _settle(page)
    assert _state(page, "ob-need-fr")["open"], "unsaved input keeps the scrim from closing the dialog"
    page.keyboard.press("Escape")
    _settle(page)
    assert not _state(page, "ob-need-fr")["open"], "Esc still does"


# ---- Back ------------------------------------------------------------------------------------------------------------


def test_back_closes_the_drawer_beside_the_list_and_keeps_the_address(board):
    page, _ = board
    url = page.url
    page.click('a[href="#ob-detail-fr"]')
    _settle(page)
    state = _state(page, "ob-detail-fr")
    assert state["open"] and not state["modal"] and state["lock"] is None, "beside the list: no scrim, no lock"
    assert page.evaluate("history.state && history.state.ileOverlay") == "ob-detail-fr"
    page.go_back()
    _settle(page)
    assert not _state(page, "ob-detail-fr")["open"], "Back closes it"
    assert page.url == url, "and the address is the one the page had"
    assert page.evaluate("document.activeElement === document.querySelector('a[href=\"#ob-detail-fr\"]')")
    # closed another way, the panel takes its history entry back
    page.click('a[href="#ob-detail-fr"]')
    _settle(page)
    page.click("#ob-detail-fr .overlay__close")
    page.wait_for_function("!(history.state && history.state.ileOverlay)", timeout=3000)
    assert page.url == url


# ---- the menu ------------------------------------------------------------------------------------------------------


def test_a_menu_opens_from_its_trigger_on_its_inline_end_and_every_way_out_works(board):
    page, _ = board
    trigger = '[popovertarget="ob-account-fr"]'
    page.click(trigger)
    _settle(page)
    state = _state(page, "ob-account-fr")
    box = page.locator(trigger).bounding_box()
    assert state["open"] and state["focus"] == "Espace réservé", state
    assert abs(state["box"]["right"] - (box["x"] + box["width"])) <= 1, ("on the trigger's inline end", state, box)
    side = page.get_attribute("#ob-account-fr", "data-overlay-side")
    if side == "above":
        assert state["box"]["bottom"] <= box["y"] - 2, (state, box)
    else:
        assert state["box"]["y"] >= box["y"] + box["height"] + 2, (state, box)
    assert page.get_attribute(trigger, "aria-expanded") == "true"
    page.keyboard.press("ArrowDown")
    assert _state(page, "ob-account-fr")["focus"] == "Profil"
    page.keyboard.press("End")
    assert _state(page, "ob-account-fr")["focus"] == "Se déconnecter"
    page.keyboard.press("Escape")
    _settle(page, 300)
    assert not _state(page, "ob-account-fr")["open"]
    assert page.evaluate("(s) => document.activeElement === document.querySelector(s)", trigger), (
        "Esc gives the focus back"
    )
    assert page.get_attribute(trigger, "aria-expanded") == "false"
    # the focus leaving it (S-7)
    page.keyboard.press("Enter")
    _settle(page, 300)
    assert _state(page, "ob-account-fr")["open"]
    page.keyboard.press("End")
    page.keyboard.press("Tab")
    _settle(page, 300)
    assert not _state(page, "ob-account-fr")["open"], "the focus left the menu: it closed"
    # a choice
    page.click(trigger)
    _settle(page, 300)
    page.click("#ob-account-fr .overlay__item >> nth=1")
    _settle(page, 300)
    assert not _state(page, "ob-account-fr")["open"], "a choice closes the menu"


# ---- O1–O3: the exit, the leaving panel, the re-opening, the keyboard -------------------------------------------------

#: The panel's clocks stretched to 900 ms, so the frames can be read on a busy machine (the bench's «?slow»).
SLOW_JS = """(id) => { const d = document.getElementById(id);
  for (const name of ['--overlay-in', '--overlay-out', '--overlay-scrim-in']) d.style.setProperty(name, '900ms'); }"""
POSE_JS = """(id) => { const s = getComputedStyle(document.getElementById(id));
  return {opacity: parseFloat(s.opacity), scale: s.scale, translate: s.translate}; }"""


def test_the_exit_is_a_transition_the_leaving_panel_takes_nothing_and_a_reopening_retargets(board):
    page, _ = board
    panel = "ob-need-fr"
    page.evaluate(SLOW_JS, panel)
    page.click('a[href="#ob-need-fr"]')
    page.wait_for_timeout(950)
    assert page.evaluate(POSE_JS, panel)["opacity"] == 1
    page.click("#ob-need-fr .overlay__close")
    page.wait_for_timeout(250)
    leaving = page.evaluate(
        """(id) => { const d = document.getElementById(id); const r = d.getBoundingClientRect();
          const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
          return {open: d.open, inert: d.inert, display: getComputedStyle(d).display,
                  running: d.getAnimations().filter((a) => a.playState === 'running').map((a) => a.transitionProperty),
                  hitInside: d.contains(hit), opacity: parseFloat(getComputedStyle(d).opacity)}; }""",
        panel,
    )
    assert not leaving["open"] and leaving["inert"], ("closed at t = 0, and inert while it leaves (B2)", leaving)
    assert leaving["display"] != "none" and "opacity" in leaving["running"], ("still leaving, by a transition", leaving)
    assert not leaving["hitInside"], "the leaving panel takes no click"
    assert 0 < leaving["opacity"] < 1, leaving
    before = page.evaluate(POSE_JS, panel)["opacity"]
    page.evaluate("document.querySelector('a[href=\"#ob-need-fr\"]').click()")
    page.wait_for_timeout(60)
    after = page.evaluate(POSE_JS, panel)
    assert after["opacity"] >= before - 0.05, (
        "a re-opening continues from the current pose, never from 0 (O1)",
        before,
        after,
    )
    page.wait_for_timeout(1000)
    assert page.evaluate(POSE_JS, panel)["opacity"] == 1


def test_an_opening_from_the_keyboard_shows_no_animation(board):
    page, _ = board
    _press_open(page, 'a[href="#ob-alert-fr"]')
    first = page.evaluate(
        """(id) => { const d = document.getElementById(id);
          return {open: d.open, opacity: parseFloat(getComputedStyle(d).opacity), scale: getComputedStyle(d).scale,
                  running: d.getAnimations().filter((a) => a.playState === 'running').length}; }""",
        "ob-alert-fr",
    )
    assert first == {"open": True, "opacity": 1.0, "scale": "none", "running": 0}, first


def test_reduced_motion_is_one_opacity_and_no_transform(browser, live_server):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/overlay-board/", wait_until="networkidle")
        for panel in ("ob-nav-fr", "ob-need-fr", "ob-sheet-fr"):
            page.click(f'a[href="#{panel}"]')
            poses = []
            for _ in range(6):
                poses.append(
                    page.evaluate(
                        """(id) => { const d = document.getElementById(id); const s = getComputedStyle(d);
                      return {t: s.translate, s: s.scale, props: d.getAnimations().map((a) => a.transitionProperty)}; }""",
                        panel,
                    )
                )
                page.wait_for_timeout(16)
            for pose in poses:
                assert pose["t"] == "none" and pose["s"] == "none", (panel, poses)
                assert set(pose["props"]) <= {"opacity", "display", "overlay"}, (panel, poses)
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
    finally:
        context.close()


# ---- the tooltip -------------------------------------------------------------------------------------------------------

AFTER_JS = """(sel) => { const s = getComputedStyle(document.querySelector(sel), '::after');
  return {visibility: s.visibility, opacity: parseFloat(s.opacity)}; }"""


def test_the_tooltip_waits_warms_its_group_can_be_hovered_and_leaves_on_esc_and_on_a_press(board):
    page, _ = board
    first = '[data-tip-group] [aria-label="Rechercher"]'
    neighbour = '[data-tip-group] [aria-label="Télécharger"]'
    page.hover(first)
    page.wait_for_timeout(150)
    assert page.evaluate(AFTER_JS, first)["visibility"] == "hidden", "it waits (400 ms)"
    page.wait_for_timeout(600)
    assert page.evaluate(AFTER_JS, first) == {"visibility": "visible", "opacity": 1.0}
    page.hover(neighbour)
    page.wait_for_timeout(40)
    assert page.evaluate(AFTER_JS, neighbour)["visibility"] == "visible", "a warm neighbour shows at once"
    # hoverable: the pointer moves onto the tip, 14 px above its control, and the tip stays
    box = page.locator(neighbour).bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] - 14)
    page.wait_for_timeout(80)
    assert page.evaluate(AFTER_JS, neighbour)["visibility"] == "visible", "WCAG 1.4.13: hoverable"
    page.keyboard.press("Escape")
    assert page.evaluate(AFTER_JS, neighbour)["visibility"] == "hidden", "Esc dismisses it"
    page.mouse.move(5, 5)
    page.wait_for_timeout(500)
    page.hover(first)
    page.wait_for_timeout(700)
    page.mouse.down()
    assert page.evaluate(AFTER_JS, first)["visibility"] == "hidden", "a press puts it away"
    page.mouse.up()
    page.wait_for_timeout(100)
    assert page.evaluate(AFTER_JS, first)["visibility"] == "hidden", "and it stays away while the pointer stays"
    # from the keyboard: at once
    page.mouse.move(5, 5)
    page.focus('[data-tip-group] [aria-label="Consulter"]')
    page.keyboard.press("Shift+Tab")
    page.keyboard.press("Tab")
    assert page.evaluate(AFTER_JS, '[data-tip-group] [aria-label="Consulter"]') == {
        "visibility": "visible",
        "opacity": 1.0,
    }


def test_the_top_layer_tip_stands_beyond_the_edge_that_would_clip_the_after(board):
    page, _ = board
    control = '.ob__cell[lang="fr"] .ob__scroller [data-tip="layer"] >> nth=0'
    page.hover(control)
    page.wait_for_timeout(700)
    tip = page.evaluate(
        """() => { const t = document.querySelector('.tooltip'); if (!t) return null; let open = false;
          try { open = t.matches(':popover-open'); } catch (e) {}
          const r = t.getBoundingClientRect(); return {open, text: t.textContent, left: r.left, top: r.top, bottom: r.bottom}; }"""
    )
    scroller = page.locator('.ob__cell[lang="fr"] .ob__scroller').bounding_box()
    box = page.locator(control).bounding_box()
    assert tip and tip["open"] and tip["text"] == "Consulter", tip
    assert tip["left"] >= scroller["x"] + scroller["width"] - 1, ("beyond the list's inline end", tip, scroller)
    assert tip["top"] < box["y"] + box["height"] and tip["bottom"] > box["y"], ("on the control's own line", tip, box)
    page.keyboard.press("Escape")
    assert page.evaluate("() => !document.querySelector('.tooltip').matches(':popover-open')"), "Esc dismisses it"


# ---- «Fermer», the grip, the phone, the API ------------------------------------------------------------------------------


@pytest.mark.parametrize("panel", ["ob-alert-fr", "ob-need-fr", "ob-nav-fr", "ob-detail-fr", "ob-sheet-fr"])
def test_fermer_is_on_every_panel_44px(board, panel):
    page, _ = board
    page.click(f'a[href="#{panel}"]')
    _settle(page)
    close = page.locator(f"#{panel} .overlay__close").bounding_box()
    assert close and round(close["width"]) == 44 and round(close["height"]) == 44, close
    assert page.get_attribute(f"#{panel} .overlay__close", "aria-label") == "Fermer"


def test_the_grip_drags_the_sheet_back_or_away(board):
    page, _ = board
    page.click('a[href="#ob-sheet-fr"]')
    page.wait_for_timeout(700)
    grip = page.locator("#ob-sheet-fr .overlay__grip").bounding_box()
    height = _state(page, "ob-sheet-fr")["box"]["h"]
    x, y = grip["x"] + grip["width"] / 2, grip["y"] + grip["height"] / 2
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x, y + 30, steps=4)
    dragging = page.evaluate("document.getElementById('ob-sheet-fr').style.translate")
    page.mouse.up()
    page.wait_for_timeout(700)
    assert dragging.startswith("0px") and _state(page, "ob-sheet-fr")["open"], ("a short drag springs back", dragging)
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x, y + height * 0.6, steps=8)
    page.mouse.up()
    page.wait_for_timeout(500)
    assert not _state(page, "ob-sheet-fr")["open"], "dragged past a third, the sheet goes"


def test_on_a_phone_the_dialog_and_the_menu_are_sheets(browser, live_server):
    context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/overlay-board/", wait_until="networkidle")
        page.click('a[href="#ob-alert-fr"]')
        page.wait_for_timeout(800)
        alert = _state(page, "ob-alert-fr")
        assert alert["box"]["x"] == 0 and alert["box"]["w"] == 390 and alert["box"]["bottom"] >= 844, alert
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click('[popovertarget="ob-row-fr"]')
        page.wait_for_timeout(800)
        menu = _state(page, "ob-row-fr")
        assert menu["open"] and menu["box"]["x"] == 0 and menu["box"]["w"] == 390 and menu["box"]["bottom"] >= 844, menu
        assert page.evaluate(
            "getComputedStyle(document.getElementById('ob-row-fr'), '::backdrop').backgroundColor"
        ) in (
            "rgba(0, 0, 0, 0)",
            "transparent",
        ), "a menu as a sheet stays a menu: its own ::backdrop lets every press through"
        assert menu["scrim"] and not menu["trapped"] and menu["lock"] is None, (
            "the one scrim stands under it, without a trap or a scroll lock (CONTRACT §2)",
            menu,
        )
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click('[popovertarget="ob-account-fr"]')
        page.wait_for_timeout(800)
        caption = page.evaluate(
            "() => { const c = document.querySelector('#ob-account-fr .overlay__caption'); return c && c.getClientRects().length ? c.textContent.trim() : null; }"
        )
        assert caption == page.get_attribute("#ob-account-fr", "aria-label") == "Mon compte", caption
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click('a[href="#ob-detail-fr"]')
        page.wait_for_timeout(700)
        detail = _state(page, "ob-detail-fr")
        assert detail["trapped"] and detail["scrim"] and detail["box"]["bottom"] >= 844, (
            "beside the list on a desktop, a modal sheet here",
            detail,
        )
    finally:
        context.close()


def test_at_400_percent_a_scrolling_body_with_nothing_to_focus_is_a_stop(browser, live_server):
    """A11Y_PERF m1: at 400 % (320 × 256 CSS px) the alert's body scrolls and holds nothing to focus — axe's
    scrollable-region-focusable (WCAG 2.1.1); Chromium and Firefox make such a scroller focusable, Safari does not. The
    module makes it a stop of its own while it scrolls, and the trap's Tab reaches it."""
    context = browser.new_context(viewport={"width": 320, "height": 256}, device_scale_factor=4)
    try:
        page = context.new_page()
        page.goto(f"{live_server.url}/overlay-board/", wait_until="networkidle")
        _press_open(page, 'a[href="#ob-alert-fr"]')
        page.wait_for_function(
            "() => document.querySelector('#ob-alert-fr .overlay__body').getAttribute('tabindex') === '0'"
        )
        body = page.evaluate(
            "() => { const b = document.querySelector('#ob-alert-fr .overlay__body'); return [b.scrollHeight, b.clientHeight]; }"
        )
        assert body[0] > body[1] + 1, ("the body scrolls at 400 %", body)
        stops = []
        for _ in range(4):
            page.keyboard.press("Tab")
            stops.append(page.evaluate("() => document.activeElement.classList.contains('overlay__body')"))
        assert any(stops), "the trap's Tab reaches the body"
        assert _state(page, "ob-alert-fr")["focusIn"], "and stays in the dialog"
    finally:
        context.close()


def test_the_api_opens_closes_toggles_and_says_why(board):
    page, _ = board
    result = page.evaluate(
        """async () => {
          const m = await import('/static/js/dist/overlay.js');
          const events = [];
          const d = document.getElementById('ob-sheet-fr');
          d.addEventListener('overlay:open', (e) => events.push('open:' + e.detail.reason));
          d.addEventListener('overlay:close', (e) => events.push('close:' + e.detail.reason));
          const opened = m.open('ob-sheet-fr', {instant: true});
          const running = d.getAnimations().filter((a) => a.playState === 'running').length;
          const isOpen = m.isOpen(d);
          const again = m.open(d);
          const closed = m.close(d, {reason: 'done', focus: false});
          const toggled = m.toggle('ob-sheet-fr');
          const toggledBack = m.toggle('ob-sheet-fr');
          return {opened, running, isOpen, again, closed, toggled, toggledBack, open: d.open, events,
                  instant: d.hasAttribute('data-instant')};
        }"""
    )
    assert result["opened"] and result["isOpen"] and result["again"] and result["closed"], result
    assert result["running"] == 0, "instant: tier 0"
    assert result["toggled"] is True and result["toggledBack"] is False and result["open"] is False, result
    assert result["events"] == ["open:api", "close:done", "open:api", "close:api"], result["events"]


# ---- Firefox and WebKit: the smoke, where their binaries are installed (never downloaded) ---------------------------


def _installed(engine: str) -> bool:
    """Is the engine's binary in Playwright's browser folder? Read from the disk: nothing is launched at collection."""
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or str(
        Path(os.environ.get("LOCALAPPDATA", "~")) / "ms-playwright"
    )
    folder = Path(base).expanduser()
    return folder.is_dir() and any(path.is_dir() for path in folder.glob(f"{engine}-*"))


#: ILE_OVERLAY_SMOKE_ENGINES (comma-separated) overrides the list, e.g. to run the smoke on Chromium itself.
ENGINES = [e for e in os.environ.get("ILE_OVERLAY_SMOKE_ENGINES", "firefox,webkit").split(",") if e and _installed(e)]

if ENGINES:

    @pytest.mark.parametrize("engine", ENGINES)
    def test_the_smoke_in_other_engines_open_close_esc_focus_return_and_the_trap(live_server, engine):
        """O10: on every engine the system opens, closes, takes Esc, gives the focus back and holds the trap."""
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            instance = getattr(p, engine).launch()
            try:
                page = instance.new_page(viewport={"width": 1280, "height": 800})
                page.goto(f"{live_server.url}/overlay-board/", wait_until="networkidle")
                for panel in ("ob-need-fr", "ob-nav-fr", "ob-sheet-fr"):
                    opener = f'a[href="#{panel}"]'
                    _press_open(page, opener)
                    page.wait_for_timeout(500)
                    assert _state(page, panel)["open"] and _state(page, panel)["focusIn"], (engine, panel)
                    for _ in range(5):
                        page.keyboard.press("Tab")
                        assert _state(page, panel)["focusIn"], (engine, panel, "Tab left the panel")
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                    assert not _state(page, panel)["open"], (engine, panel)
                    assert page.evaluate("(s) => document.activeElement === document.querySelector(s)", opener), (
                        engine,
                        panel,
                    )
                page.click('[popovertarget="ob-account-fr"]')
                page.wait_for_timeout(400)
                assert _state(page, "ob-account-fr")["open"], engine
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
                assert not _state(page, "ob-account-fr")["open"], engine
            finally:
                instance.close()
