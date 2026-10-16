"""
The motion audit's outcomes in a browser — design V5, family W4-B (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.6 item 2,
§1.5, §2.6; docs/design-v5/QA/v54/w4-b/AUDIT.md and NOTES.md). What a static test cannot see:

* the Motion library is gone from what a page loads: the home's scripts carry none of its code and weigh less than
  §2.6's 45 KB gzip (46 080 B), in no more requests than the before set (nav.js lives inside shell.js, hero.js inside
  home.js);
* «Ma situation»'s question change runs on the Web Animations API through motion.js's gate — the leaving question
  fades on --motion-fast, then the arriving one comes in on --motion-standard from 16 px in the reading direction
  (−16 px in Arabic), both on --ease-enter — and no `style` attribute survives the swap; under reduced motion nothing
  animates and the question swaps at once; asked from the keyboard (Enter, Space) it swaps at once too, with the focus
  on the new question (tier 0, R-07); a change asked while another is still in flight lands that one first and plays
  its own arrival only, so exactly one question is drawn, whole, with the focus on it;
* the rail folds in the frame of the press (plan §1.5 R10), with motion as without;
* from the keyboard the chrome is tier 0 (R-07): the skip link stands at its place in the key's own frame, and a door's
  panel opened by the pointer closes on Esc with no transition running.

Chromium on the test database; sessions minted with ``Client.force_login`` — nothing typed, no password used.
"""

from __future__ import annotations

import datetime as dt
import gzip
import os
import re

import pytest
from django.conf import settings
from django.test import Client

from accounts import roles
from accounts.models import AccountType
from core import clock

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

SITUATION = "/{lang}/espace-reserve/ma-situation/"
DASHBOARD = "/{lang}/espace-reserve/"
#: Identifiers only the Motion library writes (its keyframe resolver, its stagger, its spring limit).
MOTION_SIGNATURES = ("staggerChildren", "spring-duration-limit", "value-not-animatable", "resolveKeyframes")
#: Every element.animate() call, recorded before the page's own scripts run (a probe of the test, never shipped).
RECORD_ANIMATE = """
window.__animate = [];
const original = Element.prototype.animate;
Element.prototype.animate = function (keyframes, options) {
  window.__animate.push({id: this.id, keyframes: JSON.parse(JSON.stringify(keyframes)), options: JSON.parse(JSON.stringify(options || {})),
                         at: performance.now()});
  return original.call(this, keyframes, options);
};
"""
STEPS_JS = """() => [...document.querySelectorAll('[data-wizard-step]')].map((s) => ({id: s.id, hidden: s.hidden,
  style: s.getAttribute('style'), opacity: getComputedStyle(s).opacity, transform: getComputedStyle(s).transform}))"""
#: --ease-enter, (0.25, 1, 0.5, 1), however the bundle writes it (the minifier drops the leading zeros).
ENTER = [0.25, 1.0, 0.5, 1.0]
RUNNING_JS = """(sel) => document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.target
  && a.effect.target.closest && a.effect.target.closest(sel)).map((a) => a.animationName || a.transitionProperty || 'waapi')"""
#: The questions as the click's own task leaves them: a listener on the document runs after the control's own handler.
ON_CLICK_JS = """() => { window.__onClick = null; document.addEventListener('click', () => {
  const steps = [...document.querySelectorAll('[data-wizard-step]')]; const focused = document.activeElement;
  window.__onClick = {shown: steps.filter((s) => !s.hidden).map((s) => s.id),
    styles: steps.map((s) => s.getAttribute('style')).filter((v) => v !== null),
    opacity: steps.filter((s) => !s.hidden).map((s) => getComputedStyle(s).opacity),
    focus: focused ? focused.id : null, ring: Boolean(focused && focused.matches(':focus-visible')),
    input: document.documentElement.getAttribute('data-input')}; }, {once: true}); }"""
#: Where the wizard stands: the focused element, the counter and the Stepper's current node.
WHERE_JS = """() => ({focus: document.activeElement ? document.activeElement.id : null,
  position: document.querySelector('[data-wizard-position]').textContent,
  current: [...document.querySelectorAll('[data-wizard-mark]')].findIndex((m) => m.getAttribute('aria-current') === 'step')})"""


def _curve(easing: str) -> list[float]:
    return [float(x) for x in re.findall(r"\d*\.?\d+", easing)]


def _tab_to(page, selector: str, cap: int = 150) -> bool:
    """Tab, as a person does, until the focus is on `selector`."""
    for _ in range(cap):
        page.keyboard.press("Tab")
        if page.evaluate("(sel) => Boolean(document.activeElement && document.activeElement.matches(sel))", selector):
            return True
    return False


def _question_calls(page) -> list[dict]:
    return [c for c in page.evaluate("window.__animate") if (c["id"] or "").startswith("q-")]


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
def four_doors(set_flag, monkeypatch, legal_published):
    """Gate G3 open for the live server, without freezegun (as test_browser_w2_c1.py): the four doors are in the bar."""
    from core import flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _person(user_factory, email):
    from cases.models import CasePurpose
    from cases.services import open_case

    person = user_factory(
        email,
        role=roles.PERSON,
        full_name="Personne W4-B",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return person


def _console(browser, live_server, user, path, lang="fr", width=1440, height=900, reduced=False, script=None):
    client = Client()
    client.force_login(user)
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
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
    if script:
        context.add_init_script(script)
    page = context.new_page()
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    url = live_server.url + path.format(lang=lang)
    page.goto(url, wait_until="load")  # the first console page of the session plays the entrance release
    page.goto(url, wait_until="networkidle")
    return context, page, errors


def test_the_home_loads_no_motion_library_and_its_script_fits_the_budget(browser, live_server, seeded):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    scripts = []
    try:
        page = context.new_page()
        page.on("response", lambda r: scripts.append(r) if r.url.split("?")[0].endswith(".js") else None)
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        bodies = {r.url.rsplit("/", 1)[-1]: r.body() for r in scripts if r.ok}
        assert {"shell.js", "home.js", "main.js", "head.js"} <= set(bodies), sorted(bodies)
        assert "nav.js" not in bodies and "hero.js" not in bodies, "inlined into their importers, no stub of their own"
        for name, body in bodies.items():
            text = body.decode("utf-8", "replace")
            assert not [s for s in MOTION_SIGNATURES if s in text], f"{name} carries the Motion library"
        weight = sum(len(gzip.compress(body, 9)) for body in bodies.values())
        assert weight <= 46080, f"the home's script is {weight} B gzip, over plan §2.6's 45 KB"
        assert len(scripts) <= 8, f"{len(scripts)} script requests, over the before set's eight: {sorted(bodies)}"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_question_change_runs_on_the_platform_through_the_gate_and_leaves_no_style(
    browser, live_server, user_factory, lang
):
    person = _person(user_factory, f"w4b.situation.{lang}@example.test")
    context, page, errors = _console(browser, live_server, person, SITUATION, lang, script=RECORD_ANIMATE)
    try:
        before = page.evaluate(STEPS_JS)
        first, second = before[0]["id"], before[1]["id"]
        assert not before[0]["hidden"] and before[1]["hidden"], before[:2]
        page.evaluate("window.__animate = []")
        page.click("[data-wizard-next]")
        page.wait_for_timeout(700)
        calls = page.evaluate("window.__animate")
        leave = [c for c in calls if c["id"] == first]
        arrive = [c for c in calls if c["id"] == second]
        assert len(leave) == 1 and len(arrive) == 1, calls
        assert leave[0]["keyframes"] == {"opacity": [1, 0]}, leave[0]
        assert leave[0]["options"]["duration"] == 120 and _curve(leave[0]["options"]["easing"]) == ENTER
        shift = "translateX(-16px)" if lang == "ar" else "translateX(16px)"
        assert arrive[0]["keyframes"]["transform"] == [shift, "translateX(0)"], arrive[0]["keyframes"]
        assert arrive[0]["keyframes"]["opacity"] == [0, 1]
        assert arrive[0]["options"]["duration"] == 200 and _curve(arrive[0]["options"]["easing"]) == ENTER
        assert arrive[0]["at"] - leave[0]["at"] >= 100, "the arriving question waits for the leaving one's fade"
        after = page.evaluate(STEPS_JS)
        assert after[0]["hidden"] and not after[1]["hidden"], after[:2]
        assert [s["style"] for s in after] == [None] * len(after), "no style attribute survives the swap"
        assert after[1]["opacity"] == "1" and after[1]["transform"] == "none", after[1]
        held = page.evaluate(
            "() => [...document.querySelectorAll('[data-wizard-step]')].flatMap((s) => s.getAnimations()).length"
        )
        assert held == 0, "no animation holds a question once it is in (the leaving fade's last frame let go)"
        assert errors == [], errors
    finally:
        context.close()


def test_under_reduced_motion_the_question_swaps_at_once(browser, live_server, user_factory):
    person = _person(user_factory, "w4b.situation.reduced@example.test")
    context, page, errors = _console(browser, live_server, person, SITUATION, reduced=True, script=RECORD_ANIMATE)
    try:
        page.evaluate("window.__animate = []")
        swapped = page.evaluate(
            """() => { document.querySelector('[data-wizard-next]').click();
                 const steps = [...document.querySelectorAll('[data-wizard-step]')];
                 return {first: steps[0].hidden, second: steps[1].hidden, style: steps[1].getAttribute('style')}; }"""
        )
        assert swapped == {"first": True, "second": False, "style": None}, "the new question, in the press's own task"
        page.wait_for_timeout(300)
        assert page.evaluate("window.__animate") == [], "no animation is created under the setting"
        assert errors == [], errors
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_change_the_keyboard_asks_for_is_there_at_once_with_the_focus_on_it(browser, live_server, user_factory, lang):
    """Tier 0 (plan §1.5, R-07): Enter on «Continuer», then Space on «Précédent», reached by Tab — each swaps the question
    in the key's own task, nothing animates, and the arriving question has the focus with its ring drawn at once."""
    person = _person(user_factory, f"w4b.situation.keys.{lang}@example.test")
    context, page, errors = _console(browser, live_server, person, SITUATION, lang, script=RECORD_ANIMATE)
    try:
        ids = [s["id"] for s in page.evaluate(STEPS_JS)]
        assert _tab_to(page, "[data-wizard-next]"), "«Continuer» is reached by Tab"
        page.evaluate("window.__animate = []")
        page.evaluate(ON_CLICK_JS)
        page.keyboard.press("Enter")
        on_click = page.evaluate("window.__onClick")
        assert on_click == {
            "shown": [ids[1]],
            "styles": [],
            "opacity": ["1"],
            "focus": ids[1],
            "ring": True,
            "input": "key",
        }, f"Enter: the next question whole, in the key's own task, the focus on it — {on_click}"
        assert _tab_to(page, "[data-wizard-prev]", cap=40), "«Précédent» is reached by Tab"
        page.evaluate(ON_CLICK_JS)
        page.keyboard.press(" ")
        on_click = page.evaluate("window.__onClick")
        assert on_click == {
            "shown": [ids[0]],
            "styles": [],
            "opacity": ["1"],
            "focus": ids[0],
            "ring": True,
            "input": "key",
        }, f"Space: the previous question whole, in the key's own task, the focus on it — {on_click}"
        page.wait_for_timeout(400)
        assert _question_calls(page) == [], "no animation is created for a change the keyboard asked for"
        assert page.evaluate(STEPS_JS)[0]["style"] is None and page.evaluate(WHERE_JS)["position"].startswith("1 /")
        assert errors == [], errors
    finally:
        context.close()


#: Two changes asked 40 ms apart by the pointer — the second inside the first's 120 ms leaving fade.
IN_FLIGHT = {
    "return": "() => { document.querySelector('[data-wizard-next]').click();"
    " setTimeout(() => document.querySelector('[data-wizard-prev]').click(), 40); }",
    "stepper": "() => { const go = document.querySelectorAll('[data-wizard-go]'); go[2].click();"
    " setTimeout(() => go[0].click(), 40); }",
    "forward": "() => { const next = document.querySelector('[data-wizard-next]'); next.click();"
    " setTimeout(() => next.click(), 40); }",
}


@pytest.mark.parametrize(
    ("case", "lang"),
    [("return", "fr"), ("stepper", "fr"), ("forward", "fr"), ("return", "ar")],
    ids=["continue-then-back", "stepper-q3-then-q1", "continue-twice", "continue-then-back-ar"],
)
def test_a_change_asked_in_flight_lands_on_one_whole_question_with_the_focus(
    browser, live_server, user_factory, case, lang
):
    """The interruption: the first change's late steps do nothing once a second change is asked; the second lands the
    first (its animations cancelled, no inline opacity) and plays its own arrival only. Exactly one question is drawn,
    at opacity 1 and in place, with no `style` attribute, the focus on it, the counter and the Stepper on it."""
    person = _person(user_factory, f"w4b.situation.flight.{case}.{lang}@example.test")
    context, page, errors = _console(browser, live_server, person, SITUATION, lang, script=RECORD_ANIMATE)
    try:
        ids = [s["id"] for s in page.evaluate(STEPS_JS)]
        expected = 2 if case == "forward" else 0
        page.evaluate("window.__animate = []")
        page.evaluate(IN_FLIGHT[case])
        page.wait_for_timeout(900)
        steps = page.evaluate(STEPS_JS)
        shown = [s for s in steps if not s["hidden"]]
        assert [s["id"] for s in shown] == [ids[expected]], f"{case}: one question drawn — {steps}"
        assert shown[0]["opacity"] == "1" and shown[0]["transform"] == "none", shown[0]
        assert [s["style"] for s in steps] == [None] * len(steps), "no style attribute is left on any question"
        where = page.evaluate(WHERE_JS)
        assert where == {"focus": ids[expected], "position": f"{expected + 1} / {len(ids)}", "current": expected}, where
        held = page.evaluate(
            "() => [...document.querySelectorAll('[data-wizard-step]')].flatMap((s) => s.getAnimations()).length"
        )
        assert held == 0, "nothing holds a question once the change has landed"
        calls = [(c["id"], c["keyframes"]) for c in _question_calls(page)]
        travel = 1 if case == "forward" else -1
        shift = f"translateX({16 * travel * (-1 if lang == 'ar' else 1)}px)"
        # Whether the second press lands in the first change's fade or in its arrival (a loaded machine runs the 40 ms
        # timer late), the second change plays no fade of its own: its arrival only, last.
        fades = [call for call in calls if call[1] == {"opacity": [1, 0]}]
        assert fades == [(ids[0], {"opacity": [1, 0]})], f"{case}: one fade, the first question's — {calls}"
        assert calls[-1] == (ids[expected], {"opacity": [0, 1], "transform": [shift, "translateX(0)"]}), (
            f"{case}: the last change's arrival, last — {calls}"
        )
        assert errors == [], errors
    finally:
        context.close()


@pytest.mark.parametrize("reduced", [False, True], ids=["motion", "reduced"])
def test_the_rail_folds_in_the_frame_of_the_press(browser, live_server, seeded, person_user, reduced):
    context, page, errors = _console(browser, live_server, person_user, DASHBOARD, reduced=reduced)
    try:
        assert page.evaluate("document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width") == 248
        folded = page.evaluate(
            """() => { document.querySelector('[data-rail-toggle]').click();
                 const rail = document.querySelector('nav.rail[data-rail]');
                 const bar = document.querySelector('.console-bar');
                 return {width: rail.getBoundingClientRect().width, bar: bar ? bar.getBoundingClientRect().left : null}; }"""
        )
        assert folded["width"] == 64 and folded["bar"] == 64, f"R10: at once, not on a glide — {folded}"
        assert page.evaluate(RUNNING_JS, "nav.rail, body") == [], "nothing of the fold transitions"
        page.click("[data-rail-toggle]")
        assert page.evaluate("document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width") == 248
        assert errors == [], errors
    finally:
        context.close()


def test_from_the_keyboard_the_skip_link_and_the_portico_do_not_animate(browser, live_server, seeded, four_doors):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(live_server.url + "/fr/", wait_until="networkidle")
        page.keyboard.press("Tab")
        skip = page.evaluate(
            """() => { const a = document.activeElement; const m = new DOMMatrixReadOnly(getComputedStyle(a).transform);
                 return {skip: a.classList.contains('skip-link'), y: m.f, running: a.getAnimations().length}; }"""
        )
        assert skip == {"skip": True, "y": 0, "running": 0}, (
            f"the skip link stands at its place in the key's frame: {skip}"
        )
        page.mouse.move(5, 600)  # the pointer again: html[data-input="pointer"]
        page.click("[data-portico-door]")
        page.wait_for_timeout(500)
        assert page.evaluate("document.querySelectorAll('[data-portico-door][aria-expanded=\"true\"]').length") == 1
        page.keyboard.press("Escape")
        closed = page.evaluate(
            """(sel) => ({open: document.querySelectorAll('[data-portico-door][aria-expanded="true"]').length,
                 running: document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.target
                   && a.effect.target.closest && a.effect.target.closest(sel)).map((a) => a.transitionProperty || a.animationName)})""",
            ".main-nav",
        )
        assert closed == {"open": 0, "running": []}, f"Esc closes the panel at once (tier 0): {closed}"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_link_the_keyboard_focuses_takes_its_colour_at_once(browser, live_server, seeded, person_user, lang):
    """Tier 0 for plain links (static/css/v5/base.css): the console bar's trail, reached by Tab, takes its focused
    colour in the key's frame — no colour transition runs; the pointer gets the links' 120 ms fade back."""
    context, page, errors = _console(browser, live_server, person_user, DASHBOARD, lang)
    try:
        assert _tab_to(page, ".console-bar .breadcrumbs a"), "the trail's first link is reached by Tab"
        focused = page.evaluate(
            """() => { const a = document.activeElement;
                 return {running: a.getAnimations().map((x) => x.transitionProperty || x.animationName),
                         duration: getComputedStyle(a).transitionDuration}; }"""
        )
        assert focused == {"running": [], "duration": "0s"}, f"the trail's link from the keyboard: {focused}"
        page.mouse.move(5, 600)  # the pointer again: html[data-input="pointer"]
        pointer = page.evaluate(
            "getComputedStyle(document.querySelector('.console-bar .breadcrumbs a')).transitionDuration"
        )
        assert pointer != "0s", "the pointer keeps the links' fade"
        assert errors == [], errors
    finally:
        context.close()
