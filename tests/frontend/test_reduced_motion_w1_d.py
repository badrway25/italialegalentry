"""
Reduced motion as a state, in a browser (V5.4 plan §1.5, W1-D) — run with ``-m browser``.

The static half is tests/frontend/test_v5_tokens.py (the tokens), test_rm_flag_parity.py (the preview's flag) and
test_script_motion_gate.py (script motion). Here, in Chromium, with the setting emulated — Playwright's
``reduced_motion="reduce"``, never the preview's flag alone (MOTION_SYSTEM MS7):

* at rest no animation runs and no element, nor its ::before / ::after, carries a transition or an animation longer
  than 0 s — on the home, an interior page, the login and the console. The tokens are zeroed; nothing overrides them
  with a universal ``!important`` any more. One thing is admitted, because it is the state MS-O4 designs: an overlay's
  fade — a transition of ``opacity`` alone, lasting exactly ``--motion-reduced`` (80 ms), with the discrete
  ``display`` / ``overlay`` companion that keeps the surface in place while it goes (the portico's panels and their
  photographs, v5/chrome.css §9, W2-C1). Anything else that lasts, on any property, is a failure;
* without the setting the same pages do carry transitions, so the first check reads something;
* the preview's flag html.rm, without the setting, gives the root the setting's duration tokens;
* motion.js's helpers keep their contract in a page, from the built bundle: the gate reads the setting and the flag;
  under reduced motion play() creates nothing, tween() lands on its end, afterPaint() does not wait; settled() returns
  on a 0 s transition instead of hanging;
* head.js writes html[data-input]: "key" after Tab, "pointer" after a press.
"""

from __future__ import annotations

import os

import pytest
from django.conf import settings
from django.test import Client

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PUBLIC = ("/fr/", "/ar/", "/fr/parcours/", "/fr/compte/login/")
CONSOLE = ("/fr/espace-reserve/", "/ar/espace-reserve/")

#: Every element and pseudo-element whose computed transition or animation lasts more than 0 s; the running
#: animations. `fades` holds apart the one thing reduced motion keeps (MS-O4): a transition whose every lasting
#: property is `opacity` — or its discrete companion `display` / `overlay` — for exactly --motion-reduced.
MOVING = r"""() => {
  const secs = (v) => v.split(',').map((x) => parseFloat(x) * (x.trim().endsWith('ms') ? 0.001 : 1));
  const reduced = secs(getComputedStyle(document.documentElement).getPropertyValue('--motion-reduced').trim() || '0s')[0];
  const FADE = new Set(['opacity', 'display', 'overlay']);
  const moving = [];
  const fades = [];
  for (const el of document.querySelectorAll('*')) {
    for (const pseudo of [null, '::before', '::after']) {
      const cs = getComputedStyle(el, pseudo);
      if (pseudo && cs.content === 'none') continue;
      const name = el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/)[0] : '') + (pseudo || '');
      if (cs.transitionProperty !== 'none') {
        const durations = secs(cs.transitionDuration);
        const lasting = cs.transitionProperty.split(',').map((p, i) => [p.trim(), durations[i % durations.length]]).filter(([, d]) => d > 0);
        if (lasting.length) {
          const fade = reduced > 0 && lasting.some(([p]) => p === 'opacity') && lasting.every(([p, d]) => FADE.has(p) && Math.abs(d - reduced) < 1e-6);
          (fade ? fades : moving).push(name + ' transition ' + cs.transitionProperty + ' ' + cs.transitionDuration);
        }
      }
      if (cs.animationName !== 'none' && secs(cs.animationDuration).some((v) => v > 0)) moving.push(name + ' animation ' + cs.animationName);
    }
  }
  const running = document.getAnimations().filter((a) => a.playState === 'running').length;
  return {moving, fades, running};
}"""

TOKENS = (
    "--motion-fast",
    "--motion-standard",
    "--motion-emphasized",
    "--motion-key",
    "--motion-stagger",
    "--spring-snappy-duration",
)
ROOT_TOKENS = "(names) => names.map((n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim())"

HELPERS = r"""async () => {
  const m = await import('/static/js/dist/motion.js');
  const box = document.createElement('div');
  document.body.append(box);
  const out = {gate: m.reducedMotion(), play: m.play(box, [{opacity: 0}, {opacity: 1}], {duration: 200}) === null};
  const steps = [];
  m.tween(300, (p) => steps.push(p));
  out.tweenAtCall = steps.slice();
  const t0 = performance.now();
  await m.afterPaint();
  out.afterPaintMs = performance.now() - t0;
  box.style.setProperty('transition', 'opacity 0s');
  box.style.setProperty('opacity', '0.5');
  const t1 = performance.now();
  await m.settled(box, {timeout: 5000});
  out.settledMs = performance.now() - t1;
  out.duration = m.durationToken('--motion-fast', -1);
  await new Promise((resolve) => setTimeout(resolve, 400));
  out.tweenLater = steps;
  document.documentElement.classList.add('rm');
  out.gateWithFlag = m.reducedMotion();
  document.documentElement.classList.remove('rm');
  box.remove();
  return out;
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


def _context(browser, live_server, motion, user=None, width=1440, height=900):
    context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion=motion)
    if user is not None:
        client = Client()
        client.force_login(user)
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


def _settled(page):
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(600)  # past the console's two-frame is-ready and any one-shot of the load


@pytest.mark.parametrize("width", [1440, 390])
def test_under_the_setting_nothing_moves_at_rest(browser, live_server, seeded, person_user, width):
    context = _context(browser, live_server, "reduce", person_user, width=width, height=844 if width < 600 else 900)
    page = context.new_page()
    for path in PUBLIC + CONSOLE:
        page.goto(live_server.url + path)
        _settled(page)
        found = page.evaluate(MOVING)
        assert found["running"] == 0, (path, found["moving"][:8], found["fades"][:8])
        assert found["moving"] == [], (path, found["moving"][:8])
        assert page.evaluate(ROOT_TOKENS, list(TOKENS)) == ["0ms"] * len(TOKENS), path
    context.close()


def test_without_the_setting_the_same_pages_carry_transitions(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, "no-preference", person_user)
    page = context.new_page()
    for path in ("/fr/", "/fr/espace-reserve/"):
        page.goto(live_server.url + path)
        _settled(page)
        assert page.evaluate(MOVING)["moving"], f"{path}: no transition at all — the probe reads nothing"
    context.close()


def test_the_preview_flag_gives_the_root_the_settings_tokens(browser, live_server, seeded):
    reduced = _context(browser, live_server, "reduce")
    page = reduced.new_page()
    page.goto(live_server.url + "/fr/")
    under_setting = page.evaluate(ROOT_TOKENS, list(TOKENS))
    reduced.close()
    plain = _context(browser, live_server, "no-preference")
    page = plain.new_page()
    page.goto(live_server.url + "/fr/")
    at_rest = page.evaluate(ROOT_TOKENS, list(TOKENS))
    page.evaluate("() => document.documentElement.classList.add('rm')")
    under_flag = page.evaluate(ROOT_TOKENS, list(TOKENS))
    plain.close()
    assert under_flag == under_setting == ["0ms"] * len(TOKENS)
    assert all(value not in ("", "0ms", "0s") for value in at_rest), at_rest


@pytest.mark.parametrize("motion", ["reduce", "no-preference"])
def test_the_helpers_keep_their_contract_in_a_page(browser, live_server, seeded, motion):
    context = _context(browser, live_server, motion)
    page = context.new_page()
    page.goto(live_server.url + "/fr/")
    out = page.evaluate(HELPERS)
    context.close()
    reduced = motion == "reduce"
    assert out["gate"] is reduced and out["gateWithFlag"] is True
    assert out["play"] is reduced, "play() creates an animation only when motion is welcome"
    if reduced:
        assert out["tweenAtCall"] == [1] and out["tweenLater"] == [1], "under reduced motion the clock lands at once"
        assert out["afterPaintMs"] < 8 and out["duration"] == 0
    else:
        later = out["tweenLater"]
        assert out["tweenAtCall"] == [] and out["duration"] == 120, "the clock runs on frames, after this task"
        assert len(later) > 2 and later == sorted(later) and later[-1] == 1, later
    assert out["settledMs"] < 1000, "settled() waited on a 0 s transition"


def test_head_js_writes_the_input_modality(browser, live_server, seeded):
    context = _context(browser, live_server, "no-preference")
    page = context.new_page()
    page.goto(live_server.url + "/fr/")
    read = "() => document.documentElement.getAttribute('data-input')"
    assert page.evaluate(read) is None
    page.keyboard.press("Tab")
    assert page.evaluate(read) == "key"
    page.mouse.click(5, 880)
    assert page.evaluate(read) == "pointer"
    page.keyboard.type("abc")
    assert page.evaluate(read) == "pointer", "typing text is not a navigation key"
    page.keyboard.press("ArrowDown")
    assert page.evaluate(read) == "key"
    context.close()
