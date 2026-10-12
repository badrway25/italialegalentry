"""
Design V5 core components, part 1, in a browser (W1-C; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.3 item 7) —
what the sources cannot show (tests/frontend/test_components_w1_c.py holds the rules):

* a field is «la lastra»: 52 px on a public page, typed text 16 px, a 1 px edge and no shadow; on focus the one
  ring, the 5 px halo and the 2 px rule drawn along its foot; an empty submit shows errors that are not colour
  alone, wired to their fields;
* a primary is flat, and the press is the one gesture — 1 px down, nothing under reduced motion;
* under a coarse pointer every form control is hit in 44 px;
* in Arabic the password keeps its room for the show / hide control and the entrance does not overflow at 390 px;
* tabs: the keyboard model, the roving tabindex, the one indicator under the selected label in French and in
  Arabic (it is placed by script: the static RTL guard cannot see it — plan §2.5), travelling for a pointer only;
* a link to an FAQ row opens it.

Chromium on the live server: the contact form with gate G2 opened by TEST-ONLY legal text, the FAQ with phase 3
open, the entrance, and the development showcase (/_design/, DEBUG only) for the tabs, which no product page uses yet.
"""

from __future__ import annotations

import datetime as dt
import importlib
import os

import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import clear_url_caches

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

FORM = "/{lang}/contact/formulaire/"
TEXT = "form.enquiry-form .form-field input[type='text']"
FIELD_JS = """(sel) => {
  const el = document.querySelector(sel);
  const cs = getComputedStyle(el);
  const foot = getComputedStyle(el.closest('.form-field'), '::after');
  const r = el.getBoundingClientRect();
  return {
    height: r.height, fontSize: cs.fontSize, borderWidth: cs.borderTopWidth, radius: cs.borderTopLeftRadius,
    shadow: cs.boxShadow, outline: `${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineOffset}`,
    focusVisible: el.matches(':focus-visible'), foot: foot.transform, footHeight: foot.height,
  };
}"""
TABS_JS = """() => {
  const widget = document.querySelector('[data-tabs]');
  const list = widget.querySelector('[role=tablist]');
  const tabs = [...widget.querySelectorAll('[role=tab]')];
  const selected = tabs.findIndex((t) => t.getAttribute('aria-selected') === 'true');
  const tab = tabs[selected].getBoundingClientRect();
  const box = list.getBoundingClientRect();
  const pad = parseFloat(getComputedStyle(tabs[selected]).paddingInlineStart);
  const m = new DOMMatrixReadOnly(getComputedStyle(list, '::after').transform);
  return {
    selected, focused: tabs.indexOf(document.activeElement), tabindex: tabs.map((t) => t.tabIndex),
    hidden: [...widget.querySelectorAll('[role=tabpanel]')].map((p) => p.hidden),
    travelling: widget.classList.contains('is-travelling'), ready: widget.classList.contains('is-ready'),
    direction: getComputedStyle(list).direction,
    // the indicator's box, from the list's left edge: where it is and how wide
    indicator: { x: m.e, width: m.a, y: m.f },
    label: { x: tab.left - box.left + pad, width: tab.width - 2 * pad, bottom: tab.bottom - box.top },
    lefts: tabs.map((t) => Math.round(t.getBoundingClientRect().left)),
  };
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
def phase3_live(set_flag, monkeypatch):
    """Gate G3 open for the live server WITHOUT freezegun (a frozen ``time.monotonic`` stalls Playwright): every
    publication decision goes through ``core.clock.now()``, so patching it is enough."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.fixture
def site(live_server, seeded, legal_published, phase3_live):
    return live_server.url


@pytest.fixture
def showcase(live_server, seeded):
    """The development showcase on the live server: ``config/urls.py`` registers /_design/ at import time, with DEBUG
    on only, so the URLconf is rebuilt for the test and put back after it (tests/frontend/test_design_showcase.py)."""
    import config.urls

    with override_settings(DEBUG=True):
        clear_url_caches()
        importlib.reload(config.urls)
        yield live_server.url + "/_design/"
    clear_url_caches()
    importlib.reload(config.urls)


def _open(browser, width=1440, height=900, **kwargs):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **kwargs)
    return context, context.new_page()


def _px(value: str) -> float:
    return float(value.replace("px", ""))


# ---- fields ----------------------------------------------------------------------------------------------------


def test_a_public_field_is_la_lastra_and_its_focus_is_the_one_system(browser, site):
    context, page = _open(browser)
    try:
        page.goto(site + FORM.format(lang="fr"), wait_until="networkidle")
        rest = page.evaluate(FIELD_JS, TEXT)
        assert rest["height"] == 52, "public form fields are 52 px (plan §1.8)"
        assert rest["fontSize"] == "16px", "typed text is 16 px at every width"
        assert rest["borderWidth"] == "1px" and rest["radius"] == "4px" and rest["shadow"] == "none"
        assert rest["foot"] == "matrix(0, 0, 0, 1, 0, 0)" and rest["footHeight"] == "2px", (
            "the rule is drawn only on focus"
        )

        page.click(TEXT)
        page.wait_for_timeout(350)  # the 200 ms draw
        focused = page.evaluate(FIELD_JS, TEXT)
        assert focused["focusVisible"] and focused["outline"] == "solid 2px 2px", "the ring: 2 px at 2 px"
        assert focused["shadow"].endswith("0px 0px 0px 5px") and "inset" not in focused["shadow"], (
            "the 5 px halo of a text field"
        )
        assert focused["foot"] == "matrix(1, 0, 0, 1, 0, 0)", "the 2 px rule along the foot"
        assert focused["height"] == 52, "focus moves nothing"
    finally:
        context.close()


def test_an_empty_submit_names_each_error_with_a_mark_an_edge_and_the_words(browser, site):
    context, page = _open(browser)
    try:
        page.goto(site + FORM.format(lang="fr"), wait_until="networkidle")
        page.click("form.enquiry-form button[type='submit']")
        page.wait_for_load_state("networkidle")
        assert page.evaluate("document.activeElement && document.activeElement.id") == "form-errors", (
            "the summary takes the focus"
        )
        state = page.evaluate(
            """() => {
              const input = document.querySelector("form.enquiry-form .form-field--error input[type='text']");
              const cs = getComputedStyle(input);
              const error = document.getElementById(input.getAttribute('aria-describedby').split(' ').pop());
              const item = error.querySelector('li');
              const mark = getComputedStyle(item, '::before');
              const rest = getComputedStyle(document.querySelector("form.enquiry-form button[type='submit']"));
              return { invalid: input.getAttribute('aria-invalid'), shadow: cs.boxShadow, edge: cs.borderTopColor,
                       words: item.textContent.trim().length, mark: [mark.width, mark.height, mark.borderTopWidth, mark.borderTopStyle],
                       errorColour: getComputedStyle(item).color, markColour: mark.borderTopColor, button: rest.backgroundColor };
            }"""
        )
        assert state["invalid"] == "true"
        assert "inset" in state["shadow"] and state["shadow"].endswith("0px 0px 0px 1px inset"), (
            "the edge doubles: 2 px against 1"
        )
        assert state["words"] > 0, "the words"
        # a 1.5 px edge is snapped to a whole device pixel at 1x (1 px here, 1.5 px on a 2x screen)
        assert state["mark"][:2] == ["16px", "16px"] and state["mark"][3] == "solid", "a drawn mark beside them"
        assert state["mark"][2] in ("1px", "1.5px"), state["mark"]
        assert state["markColour"] == state["errorColour"], "in the message's own ink"
        scroll_w, client_w = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        assert scroll_w <= client_w
    finally:
        context.close()


def test_under_a_coarse_pointer_every_form_control_is_hit_in_44px(browser, site):
    context, page = _open(browser, 390, 844, is_mobile=True, has_touch=True)
    try:
        page.goto(site + FORM.format(lang="fr"), wait_until="networkidle")
        assert page.evaluate("matchMedia('(pointer: coarse)').matches")
        boxes = page.evaluate(
            """() => [...document.querySelectorAll('form.enquiry-form :is(input, select, textarea, button)')]
              .filter((e) => e.type !== 'hidden' && e.getClientRects().length && !e.closest('.hp-field, .hp-wrap'))
              .map((e) => { const r = e.getBoundingClientRect(); const hit = getComputedStyle(e, '::after');
                            return { id: e.id || e.type, type: e.type, h: r.height, w: r.width,
                                     hit: hit.content === 'none' ? null : [parseFloat(hit.width), parseFloat(hit.height)] }; })"""
        )
        assert boxes, "the form has controls"
        for box in boxes:
            if box["type"] in ("checkbox", "radio"):
                assert box["h"] == 24 and box["hit"] == [44, 44], box
            else:
                assert box["h"] >= 44, box
        scroll_w, client_w = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        assert scroll_w <= client_w
    finally:
        context.close()


@pytest.mark.parametrize("width", [390, 1440])
def test_in_arabic_the_password_keeps_its_room_for_the_show_hide_control(browser, site, width):
    """V4 padded the input's inline END, and a password is typed left to right on an Arabic page: the room was on the
    wrong side, and the control's label was drawn over what is typed (W1-A's review, the Arabic login at 390)."""
    context, page = _open(browser, width, 844 if width == 390 else 900)
    try:
        page.goto(site + "/ar/compte/login/", wait_until="networkidle")
        scroll_w, client_w = page.evaluate(
            "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
        )
        assert scroll_w <= client_w, "the entrance does not overflow"
        page.fill("input[type='password']", "Parola-dordine-2026")
        geometry = page.evaluate(
            """() => {
              const input = document.querySelector("input[type='password']");
              const toggle = document.querySelector('.form-field__toggle');
              const cs = getComputedStyle(input);
              const i = input.getBoundingClientRect(), t = toggle.getBoundingClientRect();
              return { direction: cs.direction, textStart: i.left + parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth),
                       textEnd: i.right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth),
                       toggleLeft: t.left, toggleRight: t.right, inputLeft: i.left, inputRight: i.right };
            }"""
        )
        assert geometry["direction"] == "ltr"
        assert geometry["toggleLeft"] >= geometry["inputLeft"] and geometry["toggleRight"] <= geometry["inputRight"]
        assert geometry["textStart"] >= geometry["toggleRight"], "what is typed starts after the control"
        assert geometry["textEnd"] - geometry["textStart"] >= 96, "and keeps room to be read"
        page.click(".form-field__toggle")
        assert page.get_attribute("#id_password", "type") == "text"
        shown = page.evaluate("getComputedStyle(document.getElementById('id_password')).direction")
        assert shown == "ltr", "shown, the password is still read left to right"
    finally:
        context.close()


# ---- buttons ---------------------------------------------------------------------------------------------------


def test_a_primary_is_flat_and_the_press_is_one_pixel_down(browser, site):
    context, page = _open(browser)
    try:
        page.goto(site + FORM.format(lang="fr"), wait_until="networkidle")
        submit = "form.enquiry-form button.btn--primary"
        read = """(sel) => { const cs = getComputedStyle(document.querySelector(sel));
                    return { shadow: cs.boxShadow, image: cs.backgroundImage, fill: cs.backgroundColor, translate: cs.translate,
                             height: document.querySelector(sel).getBoundingClientRect().height }; }"""
        rest = page.evaluate(read, submit)
        assert rest["shadow"] == "none" and rest["image"] == "none", "flat: no shadow, no gradient (SH-9)"
        assert rest["translate"] == "none" and rest["height"] == 52, "a public form's action stands at its fields' 52 px (review M3)"
        page.locator(submit).scroll_into_view_if_needed()
        box = page.locator(submit).bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(200)
        hovered = page.evaluate(read, submit)
        assert hovered["fill"] != rest["fill"] and hovered["translate"] == "none", (
            "hover: the fill moves one step, nothing travels"
        )
        page.mouse.down()
        pressed = page.evaluate(read, submit)  # at once: the press goes down at 0 ms
        assert pressed["translate"] == "0px 1px", "the one gesture: 1 px down"
        assert pressed["fill"] not in (rest["fill"], hovered["fill"]), "and the press fill"
        assert pressed["shadow"] == "none" and pressed["image"] == "none"
        page.mouse.move(0, 0)  # leave before releasing: nothing is submitted
        page.mouse.up()
    finally:
        context.close()


def test_under_reduced_motion_a_press_changes_colour_only(browser, site):
    context, page = _open(browser, reduced_motion="reduce")
    try:
        page.goto(site + FORM.format(lang="fr"), wait_until="networkidle")
        submit = "form.enquiry-form button.btn--primary"
        page.locator(submit).scroll_into_view_if_needed()
        box = page.locator(submit).bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.mouse.down()
        translate = page.evaluate("(sel) => getComputedStyle(document.querySelector(sel)).translate", submit)
        assert translate == "none"
        page.mouse.move(0, 0)
        page.mouse.up()
        page.click(TEXT)
        duration = page.evaluate(
            "(sel) => getComputedStyle(document.querySelector(sel).closest('.form-field'), '::after').transitionDuration",
            TEXT,
        )
        seconds = max(float(part.strip().rstrip("s")) for part in duration.split(","))
        assert seconds <= 0.001, f"the rule is not drawn over time: {duration}"
        page.wait_for_timeout(60)  # a frame: a style read in the very frame of the focus is the starting one
        foot = page.evaluate(FIELD_JS, TEXT)["foot"]
        assert foot == "matrix(1, 0, 0, 1, 0, 0)", "the rule is there at once"
    finally:
        context.close()


# ---- tabs and the disclosure -----------------------------------------------------------------------------------


def _assert_indicator_under_the_selected_label(state):
    assert state["ready"], "the script has taken the indicator over"
    assert abs(state["indicator"]["x"] - state["label"]["x"]) <= 1, state
    assert abs(state["indicator"]["width"] - state["label"]["width"]) <= 1, state
    assert abs(state["indicator"]["y"] + 1 - state["label"]["bottom"]) <= 1, "on the list's hairline"


def test_tabs_keyboard_model_roving_tabindex_and_the_one_indicator(browser, showcase):
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        page.locator("[data-tabs]").scroll_into_view_if_needed()
        first = page.evaluate(TABS_JS)
        assert first["selected"] == 0 and first["tabindex"] == [0, -1, -1] and first["hidden"] == [False, True, True]
        assert not first["travelling"], "at load the indicator is where it is"
        _assert_indicator_under_the_selected_label(first)

        page.focus("[data-tabs] [role=tab] >> nth=0")
        page.keyboard.press("ArrowRight")
        second = page.evaluate(TABS_JS)
        assert second["selected"] == 1 and second["focused"] == 1, (
            "automatic activation: the selection follows the focus"
        )
        assert second["tabindex"] == [-1, 0, -1] and second["hidden"] == [True, False, True]
        assert not second["travelling"], "tier 0: a change made from the keyboard does not travel"
        _assert_indicator_under_the_selected_label(second)

        page.keyboard.press("End")
        assert page.evaluate(TABS_JS)["selected"] == 2
        page.keyboard.press("ArrowRight")
        assert page.evaluate(TABS_JS)["selected"] == 0, "the arrows wrap"
        page.keyboard.press("ArrowLeft")
        assert page.evaluate(TABS_JS)["selected"] == 2
        page.keyboard.press("Home")
        assert page.evaluate(TABS_JS)["selected"] == 0
        page.keyboard.press("Alt+ArrowRight")
        assert page.evaluate(TABS_JS)["selected"] == 0, "Alt + arrow is the browser's"

        page.click("[data-tabs] [role=tab] >> nth=2")
        clicked = page.evaluate(TABS_JS)
        assert clicked["selected"] == 2 and clicked["travelling"], "a pointer's choice travels"
        page.wait_for_timeout(700)  # the snappy spring is 470 ms
        _assert_indicator_under_the_selected_label(page.evaluate(TABS_JS))
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.getAttribute('role')") == "tabpanel", "Tab enters the panel"
    finally:
        context.close()


def test_in_arabic_the_arrows_follow_the_reading_direction_and_the_indicator_its_label(browser, showcase):
    context, page = _open(browser, locale="ar")
    try:
        context.add_cookies([{"name": settings.LANGUAGE_COOKIE_NAME, "value": "ar", "url": showcase}])
        page.goto(showcase, wait_until="networkidle")
        assert page.evaluate("document.documentElement.dir") == "rtl"
        page.locator("[data-tabs]").scroll_into_view_if_needed()
        first = page.evaluate(TABS_JS)
        assert first["direction"] == "rtl" and first["selected"] == 0
        assert first["lefts"][0] > first["lefts"][1] > first["lefts"][2], "the first tab is at the right"
        _assert_indicator_under_the_selected_label(first)
        page.focus("[data-tabs] [role=tab] >> nth=0")
        page.keyboard.press("ArrowLeft")
        second = page.evaluate(TABS_JS)
        assert second["selected"] == 1, "← is «next» when the text reads right to left"
        _assert_indicator_under_the_selected_label(second)
        page.keyboard.press("ArrowRight")
        assert page.evaluate(TABS_JS)["selected"] == 0
        page.click("[data-tabs] [role=tab] >> nth=2")
        page.wait_for_timeout(700)
        _assert_indicator_under_the_selected_label(page.evaluate(TABS_JS))
    finally:
        context.close()


def test_from_the_keyboard_nothing_in_the_family_animates(browser, showcase):
    """Tier 0: with the input-modality flag on «key» (static/js/head.js writes it, W1-D; the test sets it, so it
    holds before and after that merge) every transition of the family lasts 0 s; without the flag they are there."""
    context, page = _open(browser)
    try:
        page.goto(showcase, wait_until="networkidle")
        read = """() => {
          const longest = (el, pseudo) => el ? Math.max(...getComputedStyle(el, pseudo).transitionDuration.split(',').map(parseFloat)) : null;
          const q = (sel) => document.querySelector(sel);
          return {
            button: longest(q('.btn--primary')),
            field: longest(q(".form-field input[type='text']")),
            select: longest(q('.form-field select')),
            toggle: longest(q('.form-field__toggle')),
            checkbox: longest(q("input[type='checkbox']")),
            tick: longest(q("input[type='checkbox']"), '::before'),
            tab: longest(q('[data-tabs] [role=tab]')),
            mark: longest(q('.accordion__summary'), '::after'),
            rule: longest(q(".form-field input[type='text']").closest('.form-field'), '::after'),
          };
        }"""
        pointer = page.evaluate(read)
        assert all(value is not None for value in pointer.values()), pointer
        for name in ("button", "field", "select", "toggle", "checkbox", "tick", "tab", "mark"):
            assert pointer[name] > 0, f"{name}: a pointer gets its feedback"
        page.evaluate("document.documentElement.setAttribute('data-input', 'key')")
        keyboard = page.evaluate(read)
        assert set(keyboard.values()) == {0}, keyboard
        page.focus(".form-field input[type='text']")
        focused = page.evaluate(
            """() => { const f = document.querySelector(".form-field input[type='text']").closest('.form-field');
                       const s = getComputedStyle(f, '::after'); return [s.transform, s.transitionDuration]; }"""
        )
        assert focused == ["matrix(1, 0, 0, 1, 0, 0)", "0s"], "the 2 px rule is there at once"
    finally:
        context.close()


def test_a_link_to_an_faq_row_opens_it(browser, site):
    context, page = _open(browser)
    try:
        page.goto(site + "/fr/faq/", wait_until="networkidle")
        ids = page.evaluate("[...document.querySelectorAll('details.accordion__item')].map((d) => d.id)")
        assert len(ids) >= 2 and not page.evaluate("document.querySelector('details.accordion__item').open")
        page.goto(site + f"/fr/faq/#{ids[1]}", wait_until="networkidle")
        assert page.evaluate("(id) => document.getElementById(id).open", ids[1]), "the permalink lands on the answer"
        assert not page.evaluate("(id) => document.getElementById(id).open", ids[0])
        mark = page.evaluate(
            "(id) => getComputedStyle(document.getElementById(id).querySelector('summary'), '::after').transform",
            ids[1],
        )
        assert mark != "none", "the drawn chevron"
    finally:
        context.close()
