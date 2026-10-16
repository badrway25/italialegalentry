"""
Orientation, the advice pages and the wizard of design V5.4 in a browser — W3-F1, step 2 (plan §3.5 item 1; §1.3
three corners a screen; §1.4 SH-8 no raised shadow at rest; §1.5 the reduced-motion state and tier 0; §1.6 focus;
§2.5 RTL; DL54-70 the questionnaire's foot is part of its page).

Chromium, gate G3 open through the clock (as the navigation family does), at 1440 × 900 and 390 × 844, in French
and in Arabic: no page wider than its viewport; at most three distinct corners painted in the first screen, the
chrome included (a circle is one corner, whether it is written 50 % or 999 px); no shadow of level 3 or more at rest;
the questionnaire's keyboard model (the focus on the new question after each step, the arrows choose, Enter goes
on); a choice's transitions at 0 s under reduced motion; typed text at 16 px and plates that are 44 px targets; a
French question ending on the reading edge of the Arabic page; «Ma situation» at three corners, its foot inside the
page — through a session minted with Client.force_login (nothing typed, no password used).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest
from django.conf import settings
from django.test import Client

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PAGES = (
    "/{lang}/orientation/",
    "/{lang}/orientation/reprendre/",
    "/{lang}/diplomes-et-titres/",
    "/{lang}/formation/",
    "/{lang}/attention-aux-fraudes/",
)
SITUATION = "/{lang}/espace-reserve/ma-situation/"

#: what is painted and on screen in the first viewport: its distinct radii (a circle counted once) and the shadows
#: of level 3 or more (a blur of 40 px or more: --shadow-3 and --shadow-4)
FIRST_SCREEN_JS = """() => {
  const radii = new Set(); let raised = 0;
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1 || r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
    const painted = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.borderTopWidth !== '0px' || cs.boxShadow !== 'none' || el.tagName === 'IMG';
    const rad = cs.borderTopLeftRadius !== '0px' ? cs.borderTopLeftRadius : cs.borderTopRightRadius;
    if (painted && rad && rad !== '0px') {
      const px = parseFloat(rad);
      radii.add(rad.includes('%') || px >= Math.min(r.width, r.height) / 2 ? 'full' : String(Math.round(px)));
    }
    if (cs.boxShadow !== 'none') {
      for (const part of cs.boxShadow.split(/,(?![^(]*\\))/)) {
        const px = part.replace(/rgba?\\([^)]*\\)/, '').trim().split(/\\s+/).map(parseFloat);
        if (px.length >= 3 && px[2] >= 40) { raised += 1; break; }
      }
    }
  }
  return {radii: [...radii].sort(), raised,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth};
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
def phase3(set_flag, monkeypatch):
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.fixture
def ruleset(db):
    from orientation.seeds import seed_ruleset_v1

    seed_ruleset_v1()


def _start(page, base, lang):
    page.goto(f"{base}/{lang}/orientation/", wait_until="load")
    page.locator("form.wizard-intro__start [type='submit']").click()
    page.wait_for_url("**/session/**", wait_until="load")


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (390, 844)])
def test_no_overflow_three_corners_and_no_raised_shadow_at_rest(
    browser, live_server, seeded, phase3, ruleset, lang, width, height
):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    page = context.new_page()
    try:
        visited = []
        for path in PAGES:
            page.goto(live_server.url + path.format(lang=lang), wait_until="load")
            visited.append(path)
            measure = page.evaluate(FIRST_SCREEN_JS)
            assert measure["overflow"] <= 0 and len(measure["radii"]) <= 3 and measure["raised"] == 0, (
                path,
                lang,
                width,
                measure,
            )
        # a step, its refused answer, the pre-evaluation
        _start(page, live_server.url, lang)
        measure = page.evaluate(FIRST_SCREEN_JS)
        assert measure["overflow"] <= 0 and len(measure["radii"]) <= 3 and measure["raised"] == 0, (
            "step",
            lang,
            width,
            measure,
        )
        page.evaluate(
            "() => document.querySelectorAll('input[name=answer]').forEach((i) => i.removeAttribute('required'))"
        )
        page.locator("button[name=action][value=answer]").click()
        page.wait_for_load_state("load")
        assert page.locator("#answer-error").is_visible()
        measure = page.evaluate(FIRST_SCREEN_JS)
        assert measure["overflow"] <= 0 and len(measure["radii"]) <= 3, ("error", lang, width, measure)
        for value in ("research",):
            page.locator(f"label[for='answer-{value}']").click()
            page.locator("button[name=action][value=answer]").click()
        page.wait_for_url("**/resultat/", wait_until="load")
        measure = page.evaluate(FIRST_SCREEN_JS)
        assert measure["overflow"] <= 0 and len(measure["radii"]) <= 3 and measure["raised"] == 0, (
            "result",
            lang,
            width,
            measure,
        )
    finally:
        context.close()


def test_the_questionnaire_s_keyboard_model(browser, live_server, seeded, phase3, ruleset):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = context.new_page()
    try:
        page.goto(live_server.url + "/fr/orientation/", wait_until="load")
        page.locator("form.wizard-intro__start [type='submit']").focus()
        page.keyboard.press("Enter")
        page.wait_for_url("**/session/**", wait_until="load")
        page.wait_for_function("() => document.activeElement && document.activeElement.id === 'wizard-question'")
        for _ in range(3):  # «Pourquoi cette question ?» may stand between the question and its choices
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement.name") == "answer":
                break
        assert page.evaluate("document.activeElement.name") == "answer", "Tab reaches the first choice"
        ring = page.evaluate("getComputedStyle(document.activeElement.closest('.wizard__choice')).outlineStyle")
        assert ring == "solid", "the plate shows the ring of the control it holds"
        page.keyboard.press("ArrowDown")
        chosen = page.evaluate(
            "document.querySelector('input[name=answer]:checked') && document.querySelector('input[name=answer]:checked').value"
        )
        assert chosen, "the arrows choose"
        before = page.locator("#wizard-question").inner_text()
        page.keyboard.press("Enter")
        page.wait_for_function(
            f"() => document.activeElement && document.activeElement.id === 'wizard-question' && document.activeElement.innerText !== {before!r}"
        )
        # opened any other way (here, typed: no referrer), a step keeps the browser's own start
        page.goto(page.url, wait_until="load")
        assert page.evaluate("document.activeElement === document.body"), (
            "a step not reached from the questionnaire is not focused"
        )
    finally:
        context.close()


def test_the_choices_are_static_under_reduced_motion_and_from_the_keyboard(
    browser, live_server, seeded, phase3, ruleset
):
    context = browser.new_context(
        viewport={"width": 390, "height": 844}, device_scale_factor=1, reduced_motion="reduce"
    )
    page = context.new_page()
    try:
        _start(page, live_server.url, "fr")
        durations = page.evaluate("getComputedStyle(document.querySelector('.wizard__choice')).transitionDuration")
        assert set(durations.replace(" ", "").split(",")) == {"0s"}, durations
        plates = page.evaluate(
            "[...document.querySelectorAll('.wizard__choice')].map((c) => c.getBoundingClientRect().height)"
        )
        assert min(plates) >= 44, plates
    finally:
        context.close()
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = context.new_page()
    try:
        _start(page, live_server.url, "fr")
        page.evaluate("document.documentElement.dataset.input = 'key'")
        durations = page.evaluate("getComputedStyle(document.querySelector('.wizard__choice')).transitionDuration")
        assert set(durations.replace(" ", "").split(",")) == {"0s"}, ("tier 0", durations)
        page.goto(live_server.url + "/fr/orientation/reprendre/", wait_until="load")
        field = page.evaluate(
            "(() => { const i = document.querySelector('input[name=token]'); const s = getComputedStyle(i); return [s.fontSize, i.getBoundingClientRect().height]; })()"
        )
        assert field[0] == "16px" and field[1] >= 44, field
    finally:
        context.close()


def test_a_french_question_and_its_choices_end_on_the_reading_edge_in_arabic(
    browser, live_server, seeded, phase3, ruleset
):
    context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    page = context.new_page()
    try:
        _start(page, live_server.url, "ar")
        styles = page.evaluate("""() => [document.querySelector('#wizard-question'), document.querySelector('.wizard__label')]
            .map((el) => [el.getAttribute('lang'), getComputedStyle(el).direction, getComputedStyle(el).textAlign])""")
        for lang, direction, align in styles:
            assert lang == "fr" and direction == "ltr" and align in ("end", "right"), styles
        bar, fill = (
            page.locator(".wizard__progress-bar").bounding_box(),
            page.locator(".wizard__progress-fill").bounding_box(),
        )
        assert abs((bar["x"] + bar["width"]) - (fill["x"] + fill["width"])) <= 1, (
            "the progress fills from the reading edge"
        )
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (390, 844)])
def test_ma_situation_draws_three_corners_and_keeps_its_foot_inside_the_page(
    browser, live_server, seeded, person_user, lang, width, height
):
    client = Client()
    client.force_login(person_user)
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
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
    try:
        path = live_server.url + SITUATION.format(lang=lang)
        page.goto(path, wait_until="networkidle")
        page.goto(path, wait_until="networkidle")  # the first console page of a session plays the entrance release
        page.wait_for_function("() => document.body.classList.contains('is-ready')")
        measure = page.evaluate(FIRST_SCREEN_JS)
        assert measure["overflow"] <= 0 and len(measure["radii"]) <= 3, (lang, width, measure)
        drawn = page.evaluate("""() => {
          const q = document.querySelector('.wiz__q:not([hidden])'); const foot = document.querySelector('[data-wizard-foot]');
          const field = document.querySelector('.wiz__field input'); const fs = getComputedStyle(foot);
          return {panel: getComputedStyle(q).borderTopLeftRadius, field: field ? getComputedStyle(field).borderTopLeftRadius : '4px',
                  position: fs.position, glass: fs.backdropFilter, wrap: fs.flexWrap};
        }""")
        assert drawn["panel"] == "8px" and drawn["field"] == "4px", drawn
        assert drawn["position"] == "static" and drawn["glass"] in ("none", "") and drawn["wrap"] == "wrap", drawn
    finally:
        context.close()
