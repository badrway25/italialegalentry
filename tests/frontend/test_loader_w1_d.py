"""
The loader «Lume» in the product (V5.4 plan §1.9; DL54-07; W1-D): the entrance release and the busy key.

With Django's client (fast):
* a successful sign-in — allauth's real round trip, `force_login` (the browser tests, the lane's minted sessions) and
  the preview's persona switch all pass through `user_logged_in` — leaves the release flag in the session; the first
  console page carries the release on the rail's mark and the top bar's mark, consumes the flag, and the next page
  carries the <img> again; a refused sign-in leaves no flag; a public page neither shows nor consumes it.

In Chromium (``-m browser``):
* on the first console page the release's animations run at load, from the first paint, and the mark is at rest once
  the phase has passed — the light transparent, no animation running; the second console page has no release;
* under the emulated setting (``reduced_motion="reduce"``) the same page shows the still: the release's markup is
  there, every animation lasts 0 s and nothing runs;
* on the login's submit the control's busy face — `.is-busy`, `aria-busy` — is set in the submit's own task, the
  focus stays on the control, the busy key turns once on the button's pseudo-element with no change to the button's
  box or the label's position, dim at 80 %; under the setting the turn lasts 0 s;
* the key sits in the middle of the inline-end padding on every size, in French and in Arabic, clear of the label;
  on the pixels of a real activation it reads at least 3 : 1 against its ground (WCAG 1.4.11), fr and ar;
* Enter in a field — the keyboard's implicit submit — makes the form's own button wait, the focus still in the field;
* NO WAIT IS FOR EVER (the review's major): a submit answered in the page is at rest in the next task and can be
  sent again; an answer that is not a page — 204, a file nobody declared — leaves the control waiting, the second
  submit of a guarded form refused, and the lease ends the wait after 10 s, the guard lifted; a page that comes
  back from the back/forward cache is at rest; without the state machine nothing waits and nothing refuses;
* a form whose answer is a file (the account's export, `data-loader="none"`) never waits and loads no loader;
  a submit control that is not a `.btn` (the console's sign-out controls) declares no state;
* a link-styled submit (the real «Marquer comme lue» of an unread communication) waits without a key: `aria-busy`,
  its own face, nothing over its label;
* under forced colours the release's room and ink layers are not displayed.
An answer that is not a page is given at the network (`page.route`): no view is reached. The real back/forward cache
was exercised on the lane with a full Chromium (QA/v54/w1-d/NOTES.md); Playwright's headless shell has none, so the
test here dispatches the event the cache sends. The no-JS submit is held by apps/portal/tests/test_browser.py.
"""

from __future__ import annotations

import os
import time

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import translation

from accounts.signals import ENTRANCE_RELEASE_KEY

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

PASSWORD = "Str0ng-Passw0rd-2026!"
RELEASE = 'data-lume="release"'
MARK_IMG = "brand/original/logo-mark.svg"


@pytest.fixture
def verified_user(user_factory):
    user = user_factory("lume@example.test", password=PASSWORD, full_name="Lume Test")
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    return user


# ---------------------------------------------------------------------------------------------- the flag


@pytest.mark.django_db
def test_a_real_sign_in_sets_the_release_and_the_first_console_page_consumes_it(client, seeded, verified_user):
    response = client.post("/fr/compte/login/", {"login": verified_user.email, "password": PASSWORD})
    assert response.status_code == 302 and "/espace-reserve/" in response["Location"]
    assert client.session.get(ENTRANCE_RELEASE_KEY) is True

    first = client.get(response["Location"])
    html = first.content.decode()
    assert first.status_code == 200
    assert html.count(RELEASE) == 2, "the rail's mark and the top bar's mark"
    assert html.count(MARK_IMG) == 1, "the drawer keeps its <img>"
    assert ENTRANCE_RELEASE_KEY not in client.session, "consumed by the page that played it"

    second = client.get(response["Location"])
    html = second.content.decode()
    assert RELEASE not in html and html.count(MARK_IMG) == 3, "every later page carries the <img>"


@pytest.mark.django_db
def test_force_login_sets_the_flag_as_a_sign_in_does(client, seeded, person_user):
    client.force_login(person_user)
    assert client.session.get(ENTRANCE_RELEASE_KEY) is True


@pytest.mark.django_db
def test_a_refused_sign_in_leaves_no_flag(client, seeded, verified_user):
    response = client.post("/fr/compte/login/", {"login": verified_user.email, "password": "wrong-password"})
    assert response.status_code == 200
    assert ENTRANCE_RELEASE_KEY not in client.session


@pytest.mark.django_db
def test_a_public_page_neither_shows_nor_consumes_the_release(client, seeded, person_user):
    client.force_login(person_user)
    home = client.get("/fr/")
    assert home.status_code == 200 and RELEASE not in home.content.decode()
    assert client.session.get(ENTRANCE_RELEASE_KEY) is True, "the flag waits for the first console page"
    console = client.get("/fr/espace-reserve/")
    assert RELEASE in console.content.decode()
    assert ENTRANCE_RELEASE_KEY not in client.session


@pytest.mark.django_db
def test_the_arabic_console_carries_the_release_unmirrored(client, seeded, person_user):
    client.force_login(person_user)
    html = client.get("/ar/espace-reserve/").content.decode()
    assert html.count(RELEASE) == 2
    assert 'dir="rtl"' in html


# ---------------------------------------------------------------------------------------------- in Chromium

pytest_browser = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

LOGIN = 'form[data-single-submit] button[type="submit"]'
#: The account's profile form — guarded (`data-single-submit`) since W3-F2's account pages, like every form of their
#: frame.
PROFILE = 'form:not([data-loader]) button[type="submit"].btn--primary'
#: An unguarded form a person reaches: the help desk's request (one `.btn--primary`, no guard, no opt-out).
DESK_PAGE = "/fr/espace-reserve/guichet/nouvelle-demande/"
DESK = 'form[action$="/guichet/nouvelle-demande/"] button[type="submit"]'
MARK_READ = 'form.portal-list__form button[type="submit"]'

RELEASE_STATE = r"""() => {
  const host = [...document.querySelectorAll('[data-lume="release"]')].find((el) => el.getClientRects().length);
  if (!host) return {host: false};
  const light = host.querySelector('.sig__lume');
  const ink = host.querySelector('.sig__face--ink');
  const names = (el) => el.getAnimations().map((a) => a.animationName).sort();
  const running = host.getAnimations({subtree: true}).filter((a) => a.playState === 'running').length;
  const box = host.getBoundingClientRect();
  return {
    host: true,
    size: Math.round(box.width),
    names: [...names(light), ...names(ink)],
    durations: [getComputedStyle(light).animationDuration, getComputedStyle(ink).animationDuration],
    lightOpacity: Number(getComputedStyle(light).opacity),
    inkOpacity: Number(getComputedStyle(ink).opacity),
    running,
    seat: host.parentElement.className,
  };
}"""

#: The control's state, as the three scripts leave it.
STATE = r"""(sel) => {
  const b = document.querySelector(sel);
  return {
    busy: b.classList.contains('is-busy'),
    ariaBusy: b.getAttribute('aria-busy'),
    ariaDisabled: b.getAttribute('aria-disabled'),
    submitted: b.form.hasAttribute('data-submitted'),
    focused: document.activeElement === b,
  };
}"""
AT_REST = {"busy": False, "ariaBusy": None, "ariaDisabled": None, "submitted": False}

#: A submit that a listener AFTER shell.js's hook cancels (window, bubbling): what is set in the submit's own task,
#: and what is left once the control has come back to rest (polled every 25 ms, 5 s at most: the first time the state
#: machine has to arrive over the network) — twice, so that the second submit is seen to be accepted.
BUSY_PROBE = r"""(sel) => new Promise((resolve) => {
  const button = document.querySelector(sel);
  const form = button.form;
  const before = button.getBoundingClientRect();
  const range = document.createRange();
  range.selectNodeContents(button);
  const label = range.getBoundingClientRect();
  const state = () => ({
    busy: button.classList.contains('is-busy'),
    ariaBusy: button.getAttribute('aria-busy'),
    ariaDisabled: button.getAttribute('aria-disabled'),
    submitted: form.hasAttribute('data-submitted'),
  });
  const seen = [];
  button.focus();
  window.addEventListener('submit', (event) => {
    event.preventDefault();
    const after = button.getBoundingClientRect();
    const labelAfter = range.getBoundingClientRect();
    const pseudo = getComputedStyle(button, '::after');
    const inTask = {
      ...state(),
      focused: document.activeElement === button,
      widthDelta: Math.abs(after.width - before.width),
      labelDelta: Math.abs(labelAfter.left - label.left) + Math.abs(labelAfter.width - label.width),
      animation: pseudo.animationName,
      duration: pseudo.animationDuration,
      iterations: pseudo.animationIterationCount,
      opacity: pseudo.opacity,
      mask: pseudo.maskImage || pseudo.webkitMaskImage,
      labelColor: getComputedStyle(button).color,
    };
    const since = performance.now();
    const poll = setInterval(() => {
      const waited = performance.now() - since;
      if (button.hasAttribute('aria-busy') && waited < 5000) return;
      clearInterval(poll);
      seen.push({inTask, waited: Math.round(waited), later: {...state(), focused: document.activeElement === button}});
      if (seen.length === 1) button.click();
      else resolve(seen);
    }, 25);
  });
  button.click();
})"""

#: True once the control neither waits nor shows the key.
RESTED = "(sel) => { const b = document.querySelector(sel); return !b.hasAttribute('aria-busy') && !b.classList.contains('is-busy'); }"

#: The key's box against the button's padding and its label, with the class set in place (geometry is the sheet's).
PLACE_PROBE = r"""([sel, size]) => {
  const b = document.querySelector(sel);
  if (size) b.classList.add(size);
  b.classList.add('is-busy');
  const cs = getComputedStyle(b), ps = getComputedStyle(b, '::after');
  const r = b.getBoundingClientRect();
  const range = document.createRange();
  range.selectNodeContents(b);
  const t = range.getBoundingClientRect();
  const rtl = cs.direction === 'rtl';
  const border = parseFloat(rtl ? cs.borderLeftWidth : cs.borderRightWidth);
  const keyW = parseFloat(ps.width);
  const inset = parseFloat(rtl ? ps.left : ps.right);
  const facing = rtl ? r.left + border + inset + keyW : r.right - border - inset - keyW;
  return {
    dir: cs.direction,
    pad: parseFloat(cs.paddingInlineEnd),
    keyW,
    keyH: parseFloat(ps.height),
    inset,
    gapLabel: rtl ? t.left - facing : facing - t.right,
    classes: b.className,
  };
}"""

#: A sheet that hides the key, so that two captures differ by the key alone (CSSOM: the page's CSP is untouched).
NO_KEY = r"""(on) => {
  if (!window.__nokey) {
    window.__nokey = new CSSStyleSheet();
    window.__nokey.replaceSync('.is-busy::after{visibility:hidden !important}');
  }
  const sheets = document.adoptedStyleSheets.filter((sheet) => sheet !== window.__nokey);
  document.adoptedStyleSheets = on ? [...sheets, window.__nokey] : sheets;
}"""

LINK_PROBE = r"""(sel) => new Promise((resolve) => {
  const button = document.querySelector(sel);
  const range = document.createRange();
  range.selectNodeContents(button);
  const read = () => {
    const cs = getComputedStyle(button), ps = getComputedStyle(button, '::after');
    const box = button.getBoundingClientRect(), label = range.getBoundingClientRect();
    return {
      classes: button.className, ariaBusy: button.getAttribute('aria-busy'), cursor: cs.cursor,
      color: cs.color, fill: cs.backgroundColor, image: cs.backgroundImage,
      rule: [ps.content, ps.height, ps.animationName, ps.opacity].join(' | '),
      box: [box.left, box.top, box.width, box.height].map((v) => Math.round(v * 100) / 100).join(','),
      label: [label.left, label.width].map((v) => Math.round(v * 100) / 100).join(','),
    };
  };
  const before = read();
  window.addEventListener('submit', (event) => {
    const inTask = read();
    event.preventDefault();
    resolve({before, inTask});
  });
  button.click();
})"""

#: Every sign-out control of the page — the forms that post to the sign-out — sent in turn (requestSubmit dispatches the
#: submit at once; a window listener, after shell.js's hook, reads what the hook set and keeps the page).
LOGOUT_PROBE = r"""(logout) => {
  const seen = [];
  const read = (event) => {
    event.preventDefault();
    const b = event.submitter;
    seen.push({cls: b.className, btn: b.classList.contains('btn'), busy: b.classList.contains('is-busy'),
               ariaBusy: b.getAttribute('aria-busy')});
  };
  window.addEventListener('submit', read);
  document.querySelectorAll(`form[action="${logout}"] button[type="submit"]`).forEach((b) => b.form.requestSubmit(b));
  window.removeEventListener('submit', read);
  return seen;
}"""

FORCED_STATE = r"""() => {
  const host = [...document.querySelectorAll('[data-lume="release"]')].find((el) => el.getClientRects().length);
  if (!host) return {host: false};
  return {
    host: true,
    room: getComputedStyle(host.querySelector('.sig__room')).display,
    ink: getComputedStyle(host.querySelector('.sig__face--ink')).display,
    running: host.getAnimations({subtree: true}).filter((a) => a.playState === 'running').length,
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


def _context(browser, live_server, motion="no-preference", user=None, width=1440, height=900, forced="none", scale=1):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion=motion,
        forced_colors=forced,
        accept_downloads=True,
        device_scale_factor=scale,
    )
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


def _answer_without_a_page(page, kind="nocontent", lose=()):
    """Every POST of the page is answered at the network, never by a view, with an answer that is not a page: 204,
    or an attachment (`kind="file"`). A script whose name starts with one of `lose` is never delivered. Returns the
    list of the POSTs that left the page."""
    posts = []

    def handler(route):
        request = route.request
        if lose and request.resource_type == "script" and request.url.rsplit("/", 1)[-1].startswith(tuple(lose)):
            return route.abort()
        if request.method != "POST":
            return route.continue_()
        posts.append(request.url)
        if kind == "file":
            headers = {"Content-Type": "application/json", "Content-Disposition": 'attachment; filename="answer.json"'}
            return route.fulfill(status=200, headers=headers, body="{}")
        return route.fulfill(status=204, body="")

    page.route("**/*", handler)
    return posts


def _press(page, selector):
    """A real pointer press on the control (the pointer stays over it, as a person's does)."""
    control = page.locator(selector).first
    control.scroll_into_view_if_needed()
    box = control.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.up()


def _eventually(page, check, timeout=5.0):
    """`check()` polled while the page's own clock runs: a loaded machine is slow, not wrong."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return True
        page.wait_for_timeout(50)
    return bool(check())


def _luminance(rgb):
    def channel(value):
        value = value / 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])


def _contrast(a, b):
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


# ---- the release ------------------------------------------------------------------------------------------------


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", [1440, 390])
def test_the_release_plays_once_at_load_and_lands_on_the_rest(browser, live_server, seeded, person_user, width):
    context = _context(browser, live_server, user=person_user, width=width, height=844 if width < 600 else 900)
    page = context.new_page()
    page.goto(live_server.url + "/fr/espace-reserve/", wait_until="commit")
    # attached, not visible: below 64rem the rail's host (the first match) is not displayed, the bar's is
    page.wait_for_selector('[data-lume="release"]', state="attached")
    early = page.evaluate(RELEASE_STATE)
    assert early["host"], "the first console page carries the release"
    assert early["names"] == ["lume-light-o", "lume-light-t", "lume-ink-o"], early
    assert early["durations"] == ["1.6s, 1.6s", "1.6s"], early
    assert early["running"] == 3, "the three animations of the one phase run from the first paint"
    assert early["seat"] == ("rail__tile" if width >= 1024 else "console-bar__tile") and early["size"] == (24 if width >= 1024 else 20)
    page.wait_for_timeout(1900)
    late = page.evaluate(RELEASE_STATE)
    assert late["running"] == 0 and late["lightOpacity"] == 0 and late["inkOpacity"] == 0, late
    page.goto(live_server.url + "/fr/espace-reserve/", wait_until="networkidle")
    assert page.evaluate('() => document.querySelectorAll(\'[data-lume="release"]\').length') == 0
    # the rail's tile, the top bar's tile and the drawer's tile (a .rail__tile too, which always keeps the <img>)
    assert page.evaluate("() => document.querySelectorAll('.rail__tile img, .console-bar__tile img').length") == 3
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_under_the_setting_the_release_is_a_still(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, motion="reduce", user=person_user)
    page = context.new_page()
    page.goto(live_server.url + "/fr/espace-reserve/", wait_until="networkidle")
    state = page.evaluate(RELEASE_STATE)
    assert state["host"], "the markup is there: the still is the end state"
    assert state["durations"] == ["0s, 0s", "0s"] and state["running"] == 0, state
    assert state["lightOpacity"] == 0 and state["inkOpacity"] == 0, "the verbatim mark, without travel"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_under_forced_colours_the_release_shows_neither_room_nor_ink(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, forced="active", user=person_user)
    page = context.new_page()
    page.goto(live_server.url + "/fr/espace-reserve/", wait_until="networkidle")
    state = page.evaluate(FORCED_STATE)
    assert state == {"host": True, "room": "none", "ink": "none", "running": 0}, state
    context.close()


# ---- L2: the busy key -----------------------------------------------------------------------------------------------


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("motion", ["no-preference", "reduce"])
def test_the_busy_key_is_in_the_click_s_task_and_moves_nothing(browser, live_server, seeded, motion):
    context = _context(browser, live_server, motion=motion)
    page = context.new_page()
    page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
    in_task = page.evaluate(BUSY_PROBE, LOGIN)[0]["inTask"]
    assert in_task["busy"] and in_task["ariaBusy"] == "true", in_task
    assert in_task["ariaDisabled"] == "true" and in_task["submitted"], "the login's form is guarded (main.js, the same task)"
    assert in_task["focused"], "aria-disabled, never disabled: the focus stays"
    assert in_task["widthDelta"] < 0.5 and in_task["labelDelta"] < 0.5, "the key sits in the padding: nothing is laid out again"
    assert in_task["animation"] == "sig-turn" and in_task["iterations"] == "1", in_task
    assert in_task["duration"] == ("0.32s" if motion == "no-preference" else "0s"), in_task
    assert in_task["opacity"] == "0.8", "the dim face: 80 % of the ink keeps 3 : 1 on every variant (WCAG 1.4.11)"
    assert "svg" in in_task["mask"], "the key is key.svg, masked in the button's own ink"
    assert in_task["labelColor"] != "rgba(0, 0, 0, 0)", "the label stays"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang, size", [("fr", ""), ("fr", "btn--sm"), ("fr", "btn--large"), ("ar", ""), ("ar", "btn--sm")])
def test_the_key_sits_in_the_middle_of_the_inline_end_padding(browser, live_server, seeded, lang, size):
    """Whatever the button's size, in both directions: the same air on both sides of the key, and never against the
    label's last glyph (at a fixed 8 px from the edge the key touched the label of a small button)."""
    context = _context(browser, live_server)
    page = context.new_page()
    page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
    out = page.evaluate(PLACE_PROBE, [LOGIN, size])
    assert out["dir"] == ("rtl" if lang == "ar" else "ltr") and (not size or size in out["classes"]), out
    assert 7 < out["keyW"] < 8.5 and out["keyH"] == 18, out
    assert abs(out["inset"] - (out["pad"] - out["keyW"]) / 2) < 0.6, f"the key is not centred in the padding: {out}"
    assert out["inset"] >= 3.5 and out["gapLabel"] >= out["inset"] - 0.6, f"the key is against the label or the edge: {out}"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_busy_key_reads_three_to_one_on_its_ground(browser, live_server, seeded, lang, tmp_path):
    """The key is the one visual indicator of the state: WCAG 1.4.11 asks 3 : 1 of it against the ground it is drawn
    on. Read on the pixels of a real activation (the pointer still over the control): two captures at device scale 3
    that differ by the key alone; its fully covered pixels against the ground under each of them."""
    from PIL import Image

    context = _context(browser, live_server, scale=3)
    page = context.new_page()
    _answer_without_a_page(page)
    page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
    _press(page, LOGIN)
    page.wait_for_timeout(700)  # past the turn: the key holds
    assert page.evaluate(STATE, LOGIN)["busy"], "the control is waiting"
    box = page.locator(LOGIN).first.bounding_box()
    clip = {"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]}
    page.screenshot(path=str(tmp_path / "key.png"), clip=clip)
    page.evaluate(NO_KEY, True)
    page.screenshot(path=str(tmp_path / "ground.png"), clip=clip)
    key, ground = Image.open(tmp_path / "key.png").convert("RGB"), Image.open(tmp_path / "ground.png").convert("RGB")
    assert key.size == ground.size
    differing = [
        (max(abs(a - b) for a, b in zip(key.getpixel((x, y)), ground.getpixel((x, y)))), x, y)
        for x in range(key.width)
        for y in range(key.height)
    ]
    top = max(d for d, _, _ in differing)
    assert top > 60, "no key was drawn"
    core = [(x, y) for d, x, y in differing if d >= 0.9 * top]
    drawn = [x for d, x, _ in differing if d >= 0.25 * top]
    ratios = sorted(_contrast(key.getpixel(xy), ground.getpixel(xy)) for xy in core)
    assert len(core) > 60, len(core)
    assert ratios[0] >= 3.0, f"the dim key reads {ratios[0]:.2f} : 1 at its weakest pixel (median {ratios[len(ratios) // 2]:.2f})"
    # the key is at the inline end: the right half of the button in French, the left half in Arabic
    centre = (min(drawn) + max(drawn)) / 2 / key.width
    assert (centre < 0.2) if lang == "ar" else (centre > 0.8), centre
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_enter_in_a_field_makes_the_form_s_own_button_wait(browser, live_server, seeded):
    """The keyboard's implicit submit — Enter in a text field: the control that waits is the form's own submit
    button (the event's submitter), and the focus stays in the field the person is typing in."""
    context = _context(browser, live_server)
    page = context.new_page()
    posts = _answer_without_a_page(page)
    page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
    field = page.locator('form[data-single-submit] input[type="email"], form[data-single-submit] input[name="login"]').first
    field.focus()
    page.keyboard.press("Enter")
    assert _eventually(page, lambda: len(posts) == 1), "the form was sent"
    state = page.evaluate(STATE, LOGIN)
    assert state["busy"] and state["ariaBusy"] == "true" and state["ariaDisabled"] == "true", state
    assert not state["focused"] and page.evaluate("() => document.activeElement.tagName") == "INPUT", "the focus stays in the field"
    context.close()


# ---- no wait is for ever ----------------------------------------------------------------------------------------------


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_submit_answered_in_the_page_is_at_rest_in_the_next_task(browser, live_server, seeded):
    """A listener that runs after shell.js's hook cancels the submit — a validation, a confirmation answered in
    place: the page stays, so the wait is over at once, the guard is lifted and the form can be sent again."""
    context = _context(browser, live_server)
    page = context.new_page()
    page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
    first, second = page.evaluate(BUSY_PROBE, LOGIN)
    assert first["inTask"]["busy"] and first["inTask"]["ariaBusy"] == "true" and first["inTask"]["submitted"]
    later = first["later"]
    assert {key: later[key] for key in AT_REST} == AT_REST, f"the control still waits for an answer that was given: {first}"
    assert later["focused"], "the focus is where the person left it"
    assert second["inTask"]["busy"] and second["inTask"]["ariaBusy"] == "true", "the second submit is accepted, not refused"
    assert {key: second["later"][key] for key in AT_REST} == AT_REST, second
    assert second["waited"] <= 250, f"with the state machine already there the wait ends in the next task: {second['waited']} ms"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_wait_that_no_page_ends_is_a_lease(browser, live_server, seeded, person_user):
    """The answer is not a page — 204 on the guarded login, a file nobody declared on an unguarded form (the help
    desk's request): no event tells a script, so the control waits, the guarded form refuses the second submit, and
    after SLOW_AFTER (10 s) the form is at rest by itself and can be sent again. Before the fix it waited, announced and
    refused for ever. (The unguarded form was the account's profile form until W3-F2's account pages guarded it, as
    every form of their frame: read as unguarded, it failed here; its guard is the next test's guarded case.)"""
    anonymous, signed_in = _context(browser, live_server), _context(browser, live_server, user=person_user)
    login, desk = anonymous.new_page(), signed_in.new_page()
    login_posts = _answer_without_a_page(login)
    _answer_without_a_page(desk, kind="file")
    login.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
    desk.goto(live_server.url + DESK_PAGE, wait_until="networkidle")
    assert desk.evaluate("(sel) => document.querySelectorAll(sel).length", DESK) == 1
    assert not desk.evaluate("(sel) => document.querySelector(sel).form.hasAttribute('data-single-submit')", DESK)

    _press(login, LOGIN)
    sent = {login: time.monotonic()}
    with desk.expect_download() as download:
        _press(desk, DESK)
    sent[desk] = time.monotonic()
    assert download.value.suggested_filename == "answer.json"
    assert _eventually(login, lambda: len(login_posts) == 1), "the login was sent"
    waiting = login.evaluate(STATE, LOGIN)
    assert waiting == {"busy": True, "ariaBusy": "true", "ariaDisabled": "true", "submitted": True, "focused": True}, waiting
    _press(login, LOGIN)
    login.wait_for_timeout(200)
    assert len(login_posts) == 1, "the guarded form refuses the second submit while it waits"
    waiting = desk.evaluate(STATE, DESK)
    assert waiting == {"busy": True, "ariaBusy": "true", "ariaDisabled": None, "submitted": False, "focused": True}, (
        f"an unguarded form announces no refusal: {waiting}"
    )
    assert desk.url.endswith(DESK_PAGE), "the page was not replaced"

    # the lease is SLOW_AFTER: 7 s after its submit each control still waits; then the rest comes by itself — waited
    # for, not dated (the lease runs from the moment loader.js took the submit), and never before 9 s
    for page, selector in ((login, LOGIN), (desk, DESK)):
        page.wait_for_timeout(max(0, int((sent[page] + 7.0 - time.monotonic()) * 1000)))
        if time.monotonic() - sent[page] < 8.5:  # a machine that stalled past the lease proves nothing either way
            assert page.evaluate(STATE, selector)["ariaBusy"] == "true", "the wait ended long before its lease"
    for page, selector in ((login, LOGIN), (desk, DESK)):
        page.wait_for_function(RESTED, arg=selector, timeout=max(1000, int((sent[page] + 25 - time.monotonic()) * 1000)))
        assert time.monotonic() - sent[page] >= 9.0, "the wait ended before its lease"
        rested = page.evaluate(STATE, selector)
        assert {key: rested[key] for key in AT_REST} == AT_REST, f"the wait outlived its lease: {rested}"
        assert rested["focused"], "the focus is where the person left it"
    _press(login, LOGIN)
    assert _eventually(login, lambda: len(login_posts) == 2), "the form can be sent again"
    assert login.evaluate(STATE, LOGIN)["ariaBusy"] == "true"
    anonymous.close()
    signed_in.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_page_back_from_the_cache_is_at_rest(browser, live_server, seeded):
    """A page restored from the back/forward cache comes back as it was left — waiting: `pageshow` with `persisted`
    puts every control and the guard at rest, in loader.js, shell.js and main.js (the event is dispatched here; the
    real cache was exercised on the lane)."""
    context = _context(browser, live_server)
    page = context.new_page()
    posts = _answer_without_a_page(page)
    page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
    _press(page, LOGIN)
    page.wait_for_timeout(500)
    assert page.evaluate(STATE, LOGIN)["ariaDisabled"] == "true"
    page.evaluate("() => window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted: false}))")
    assert page.evaluate(STATE, LOGIN)["ariaBusy"] == "true", "the first show of a page is not a return"
    page.evaluate("() => window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted: true}))")
    back = page.evaluate(STATE, LOGIN)
    assert {key: back[key] for key in AT_REST} == AT_REST, back
    _press(page, LOGIN)
    assert _eventually(page, lambda: len(posts) == 2), "the form can be sent again"
    assert page.evaluate(STATE, LOGIN)["ariaBusy"] == "true"
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    ("path", "selector", "guarded"),
    [("/fr/compte/profil/", PROFILE, True), (DESK_PAGE, DESK, False)],
    ids=["the account's guarded form", "the help desk's unguarded form"],
)
def test_without_the_state_machine_nothing_waits(browser, live_server, seeded, person_user, path, selector, guarded):
    """If loader.js cannot be loaded nothing would ever end a wait: shell.js takes back what it set — and nothing
    refuses for ever either: main.js's guard on a guarded form (the account's, since W3-F2) is lifted with the face.
    Without that, the guarded form kept `data-submitted` and an `aria-disabled` that nothing would end (the integration
    fix (d)). The guard's own state is read in the submit's task, so a guard never set cannot pass for one lifted."""
    context = _context(browser, live_server, user=person_user)
    page = context.new_page()
    posts = _answer_without_a_page(page, lose=("loader",))
    page.goto(live_server.url + path, wait_until="networkidle")
    guard = page.evaluate("(sel) => document.querySelector(sel).form.hasAttribute('data-single-submit')", selector)
    assert guard is guarded, (path, guard)
    page.evaluate(
        """(sel) => { const b = document.querySelector(sel); window.__inTask = null;
          window.addEventListener('submit', () => { window.__inTask = {submitted: b.form.hasAttribute('data-submitted'),
            ariaDisabled: b.getAttribute('aria-disabled')}; }); }""",
        selector,
    )
    _press(page, selector)
    assert _eventually(page, lambda: len(posts) == 1), "the form was sent"
    assert page.evaluate("() => window.__inTask") == {"submitted": guarded, "ariaDisabled": "true" if guarded else None}
    page.wait_for_function(RESTED, arg=selector, timeout=5000)
    state = page.evaluate(STATE, selector)
    assert {key: state[key] for key in AT_REST} == AT_REST, state
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_form_whose_answer_is_a_file_never_waits_and_loads_no_loader(browser, live_server, seeded, person_user):
    """«Exporter mes données (JSON)» answers with an attachment: the page stays, and the form says so
    (`data-loader="none"`) — the hook sets nothing, loads nothing, refuses nothing (a second export downloads)."""
    context = _context(browser, live_server, user=person_user)
    page = context.new_page()
    scripts = []
    page.on("request", lambda request: scripts.append(request.url) if request.resource_type == "script" else None)
    page.goto(live_server.url + "/fr/compte/profil/", wait_until="networkidle")
    button = page.locator('form[data-loader="none"] button[type="submit"]')
    assert button.count() == 1
    with page.expect_download() as first:
        button.click()
    assert first.value.suggested_filename.endswith(".json")
    page.wait_for_timeout(600)
    state = button.evaluate(
        "(b) => ({busy: b.classList.contains('is-busy'), ariaBusy: b.getAttribute('aria-busy'), "
        "ariaDisabled: b.getAttribute('aria-disabled'), cursor: getComputedStyle(b).cursor})"
    )
    assert state == {"busy": False, "ariaBusy": None, "ariaDisabled": None, "cursor": "pointer"}, state
    assert page.url.endswith("/fr/compte/profil/"), "the page was not replaced"
    assert not [url for url in scripts if url.rsplit("/", 1)[-1].startswith("loader")], scripts
    with page.expect_download() as second:
        button.click()
    assert second.value.suggested_filename == first.value.suggested_filename
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_submit_control_that_is_not_a_button_of_the_system_declares_no_state(browser, live_server, seeded, person_user):
    """The console's sign-out controls are not buttons of the system — the account popover's row (`overlay__item`, the
    overlay system's popover) and the rail's own control (`rail__tool`), the drawer's copy of the rail with it: v5/
    loader.css has no key to draw on them, so the hook sets no class and no `aria-busy` — nothing the eye cannot see is
    announced. (The probe looked for `button.account-menu__link`, the account menu's design-V4 face, which W2-C2
    retired for the popover: it found no control at all. The controls are now found by what they do — they post to the
    sign-out — and each is checked to be no `.btn`, the premise.)"""
    with translation.override("fr"):
        logout = reverse("account_logout")
    context = _context(browser, live_server, user=person_user)
    page = context.new_page()
    page.goto(live_server.url + "/fr/espace-reserve/", wait_until="networkidle")
    out = page.evaluate(LOGOUT_PROBE, logout)
    kinds = {control["cls"].split()[0] for control in out}
    assert {"overlay__item", "rail__tool"} <= kinds, out
    for control in out:
        assert control == {"cls": control["cls"], "btn": False, "busy": False, "ariaBusy": None}, control
    context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_link_styled_submit_waits_without_a_key(browser, live_server, seeded, person_user, lang):
    """A link-styled button is its text: no padding holds the key, and it was drawn over the label's last glyphs.
    The real «Marquer comme lue» of an unread communication now waits with `aria-busy` and keeps its own face — no
    class, so neither the key nor V4's busy slab: its rule, its colours, its box and its label are what they were."""
    from portal.services import send_message

    send_message(recipient=person_user, subject="Convocation", body="Votre rendez-vous est confirmé.")
    context = _context(browser, live_server, user=person_user)
    page = context.new_page()
    page.goto(f"{live_server.url}/{lang}/espace-reserve/communications/", wait_until="networkidle")
    out = page.evaluate(LINK_PROBE, MARK_READ)
    before, in_task = out["before"], out["inTask"]
    assert before["classes"] == "btn btn--link btn--sm" and before["ariaBusy"] is None and before["cursor"] == "pointer", before
    assert in_task["ariaBusy"] == "true" and in_task["cursor"] == "progress", "it waits, and says so"
    assert in_task["classes"] == before["classes"], "no .is-busy: the key has no place in a button without padding"
    for kept in ("rule", "color", "fill", "image", "box", "label"):
        assert in_task[kept] == before[kept], f"the link's {kept} changed while it waits: {before[kept]} → {in_task[kept]}"
    # the V5 link underlines with text-decoration (v5/buttons.css, W1-C): it has no ::after at all — V3's was the
    # 1 px rule under the label — so there is nothing a key could be drawn in
    assert before["rule"].split(" | ")[0] == "none" and before["rule"].split(" | ")[2] == "none", before["rule"]
    context.close()
