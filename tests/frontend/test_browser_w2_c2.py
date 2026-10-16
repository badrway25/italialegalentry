"""
The navbar, part 2 in the browser (design V5, V5.4 plan §1.12 item 8, §1.11, §1.14; W2-C2) — the gate's N8, N13, N14
and O2–O8 for the sheet and the account popover:

- the sheet is the overlay system's modal drawer: «Menu» opens it with `aria-modal`, the focus on «Fermer», the page
  out of the tree and held without a shift; Tab stays inside; Esc closes it and gives the focus back to «Menu»;
- its head line stands on the letterhead's row; every target holds 44 px under a finger, «Italiano»'s ring whole;
  the doors unfold in place, one at a time, and an open door adds no glyph;
- from 48rem the side sheet slides in from the inline end and leaves by it, taking no click on the way out; the scrim
  closes it; reduced motion is one 80 ms opacity, no transform; from 64rem it carries Forum · Projet · the languages ·
  the search; a window widened past 80rem puts it away;
- signed in, the targa's seat opens the account popover: hung on the trigger's inline end, the focus on its first
  row, the arrows, Esc and the focus back, closed when the focus leaves; 44 px under a finger;
- no photograph is fetched on a phone, sheet open, nor with Save-Data (N8).
Chromium on the French home with the static fallback menu, gate G3 open (four doors). The Arabic geometry is
tests/i18n/test_rtl_browser_w2_c2.py's; the cold open's INP is measured, not tested (docs/design-v5/QA/v54/w2-c2/
NOTES.md: a shared machine makes a latency assertion a coin).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

MENU = "[data-nav-toggle]"
SHEET = "#nav-sheet"

STATE_JS = """() => {
  const s = document.getElementById('nav-sheet');
  const t = document.querySelector('[data-nav-toggle]');
  const a = document.activeElement;
  return {
    open: s.open, modal: s.getAttribute('aria-modal'), expanded: t.getAttribute('aria-expanded'),
    lock: document.documentElement.getAttribute('data-overlay-lock'),
    onFermer: a === s.querySelector('.nav-sheet__head .nav-toggle'), onMenu: a === t, inSheet: s.contains(a),
    mainHidden: document.getElementById('main-content').closest('[aria-hidden="true"]') !== null,
    scrollY: Math.round(scrollY), scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
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
def four_doors(set_flag, monkeypatch, legal_published):
    """Gate G3 open for the live server WITHOUT freezegun (a frozen ``time.monotonic`` stalls Playwright): every
    publication decision goes through ``core.clock.now()``, so patching it is enough (as W2-C1's tests do)."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _open(browser, width, height, **kwargs):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, **kwargs)
    return context, context.new_page()


def _session(live_server, user):
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(user)  # nothing typed, no password used
    return {
        "name": settings.SESSION_COOKIE_NAME,
        "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
        "url": live_server.url,
    }


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_sheet_opens_and_closes_on_the_overlay_system(browser, live_server, seeded, four_doors, lang):
    context, page = _open(browser, 390, 844, has_touch=True)
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(200)
        before = page.evaluate(STATE_JS)
        assert not before["open"] and before["expanded"] == "false"
        page.tap(MENU)
        page.wait_for_timeout(450)
        state = page.evaluate(STATE_JS)
        assert state["open"] and state["modal"] == "true" and state["expanded"] == "true", state
        assert state["onFermer"], "«Fermer» takes the first focus (plan §1.12 item 8)"
        assert state["mainHidden"], "the page behind leaves the accessibility tree"
        assert state["lock"] is not None and state["scrollY"] == before["scrollY"], "held, not moved (O8)"
        assert state["scrollWidth"] == state["clientWidth"]
        # the head line stands on the letterhead's row: the lock-up does not move, «Fermer» ends where «Menu» ends
        rows = page.evaluate(
            """() => {
              const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom].map(Math.round); };
              const s = document.getElementById('nav-sheet');
              return {head: r(s.querySelector('.nav-sheet__head .brand')), bar: r(document.querySelector('.site-header__inner > .brand')),
                      fermer: r(s.querySelector('.nav-sheet__head .nav-toggle')), menu: r(document.querySelector('[data-nav-toggle]')),
                      rtl: document.documentElement.dir === 'rtl'};
            }"""
        )
        assert rows["head"] == rows["bar"], rows
        end = 0 if rows["rtl"] else 2
        assert abs(rows["fermer"][end] - rows["menu"][end]) <= 1 and rows["fermer"][1] == rows["menu"][1], rows
        # one width for «Menu» and «Fermer» (the longer word's): only the word and the glyph change (REVIEW m5)
        assert abs(rows["fermer"][2 - end] - rows["menu"][2 - end]) <= 1, rows
        # Tab stays inside the sheet, both ways round
        for key in ["Tab"] * 45 + ["Shift+Tab"] * 5:
            page.keyboard.press(key)
            assert page.evaluate("document.getElementById('nav-sheet').contains(document.activeElement)"), key
        # Esc closes it, gives the focus back to «Menu», lifts the lock, leaves the page where it was
        page.keyboard.press("Escape")
        page.wait_for_timeout(350)
        after = page.evaluate(STATE_JS)
        assert not after["open"] and after["expanded"] == "false" and after["onMenu"], after
        assert after["lock"] is None and not after["mainHidden"] and after["scrollY"] == before["scrollY"], after
        # «Fermer» does the same
        page.tap(MENU)
        page.wait_for_timeout(450)
        page.tap(f"{SHEET} .nav-sheet__head .nav-toggle")
        page.wait_for_timeout(350)
        assert not page.evaluate(STATE_JS)["open"]
    finally:
        context.close()


def test_every_target_of_the_sheet_holds_44_px_under_a_finger(browser, live_server, seeded, four_doors):
    """N14: no target under 44 px in the sheet on a coarse pointer, «Italiano»'s ring fully visible; the doors
    unfold in place one at a time; an open door adds no glyph (DE-2)."""
    context, page = _open(browser, 360, 780, has_touch=True)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.tap(MENU)
        page.wait_for_timeout(450)
        small = page.evaluate(
            """() => [...document.querySelectorAll('#nav-sheet :is(a[href], button, summary, input)')]
                .filter((e) => e.getClientRects().length)
                .map((e) => [(e.textContent || e.name || '').trim().slice(0, 30), e.getBoundingClientRect()])
                .filter(([, b]) => b.width < 43.5 || b.height < 43.5).map(([t, b]) => [t, Math.round(b.width), Math.round(b.height)])"""
        )
        assert small == [], small
        page.keyboard.press("Tab")  # from «Fermer», the first language — from the keyboard: its ring is drawn
        ring = page.evaluate(
            """() => {
              const link = document.activeElement, cs = getComputedStyle(link), b = link.getBoundingClientRect();
              const pad = (parseFloat(cs.outlineWidth) || 0) + (parseFloat(cs.outlineOffset) || 0);
              const body = document.querySelector('#nav-sheet .nav-sheet__body').getBoundingClientRect();
              return {text: link.textContent.trim(), ring: cs.outlineStyle !== 'none',
                      inside: b.left - pad >= body.left && b.right + pad <= body.right && b.top - pad >= body.top && b.left - pad >= 0};
            }"""
        )
        assert ring == {"text": "Italiano", "ring": True, "inside": True}, ring
        doors = page.locator(f"{SHEET} .nav-sheet__item--door > details > summary")
        assert doors.count() == 4
        doors.nth(0).tap()
        doors.nth(1).tap()
        opened = page.evaluate(
            "[...document.querySelectorAll('#nav-sheet details.nav-sheet__door')].map((d) => d.open)"
        )
        assert opened == [False, True, False, False, False], opened
        panel = page.evaluate(
            """() => { const p = document.querySelectorAll('#nav-sheet details.nav-sheet__door')[1].querySelector('.nav-sheet__panel');
              return {gloss: !!p.querySelector('.nav-sheet__gloss'), entries: p.querySelectorAll('.portico__link').length,
                      space: !!p.querySelector('.portico__space'), glyphs: p.querySelectorAll('svg').length}; }"""
        )
        assert panel["gloss"] and panel["entries"] >= 2 and panel["space"] and panel["glyphs"] == 0, panel
    finally:
        context.close()


def test_the_side_sheet_slides_in_and_out_by_the_inline_end(browser, live_server, seeded, four_doors):
    """O2 from 48rem: in from the inline end, out by it, taking no click and no Tab on the way; the scrim closes it."""
    context, page = _open(browser, 768, 1024, has_touch=True)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.tap(MENU)
        lefts = page.evaluate(
            """async () => { const s = document.getElementById('nav-sheet'), out = [];
              for (let i = 0; i < 6; i++) { await new Promise((r) => setTimeout(r, 40)); out.push(Math.round(s.getBoundingClientRect().left)); }
              return out; }"""
        )
        page.wait_for_timeout(300)
        box = page.evaluate(
            "(() => { const b = document.getElementById('nav-sheet').getBoundingClientRect(); return [b.left, b.right, b.top, b.bottom].map(Math.round); })()"
        )
        assert box[1] == 768 and box[2] == 0 and box[3] == 1024 and 340 <= box[0] <= 352, box
        assert lefts[0] > lefts[-1] >= box[0] - 2 and lefts == sorted(lefts, reverse=True), lefts
        page.mouse.click(100, 600)  # the scrim, beside the sheet
        out = page.evaluate(
            """async () => { const s = document.getElementById('nav-sheet'), out = [];
              for (let i = 0; i < 4; i++) { await new Promise((r) => setTimeout(r, 35)); out.push([Math.round(s.getBoundingClientRect().left), s.inert]); }
              return out; }"""
        )
        moving = [left for left, _ in out if left > 0]
        assert moving and moving == sorted(moving) and moving[-1] > box[0], out
        assert all(inert for _, inert in out), "the leaving sheet takes no click and no Tab (B2)"
        page.wait_for_timeout(300)
        state = page.evaluate(STATE_JS)
        assert not state["open"] and state["onMenu"] and state["lock"] is None, state
    finally:
        context.close()


def test_reduced_motion_is_one_short_opacity_and_no_transform(browser, live_server, seeded, four_doors):
    """O4: under reduced motion the sheet appears in one 80 ms opacity, with no transform at any sampled frame — the
    phone's rise included."""
    for width in (390, 768):
        context, page = _open(browser, width, 844, reduced_motion="reduce")
        try:
            page.goto(f"{live_server.url}/fr/", wait_until="load")
            page.click(MENU)
            frames = page.evaluate(
                """async () => { const s = document.getElementById('nav-sheet'), b = s.querySelector('.nav-sheet__body'), out = [];
                  for (let i = 0; i < 6; i++) { const cs = getComputedStyle(s);
                    out.push([cs.translate, cs.scale, getComputedStyle(b).translate, cs.transitionDuration, s.getBoundingClientRect().left]);
                    await new Promise((r) => setTimeout(r, 16)); }
                  return out; }"""
            )
            for translate, scale, body, duration, _left in frames:
                assert translate == "none" and scale == "none" and body == "none", (width, frames)
                assert set(duration.replace(" ", "").split(",")) == {"0.08s"}, (width, duration)
            assert len({round(left) for *_, left in frames}) == 1, (width, frames)
        finally:
            context.close()


def test_from_64rem_the_sheet_carries_forum_projet_the_languages_and_the_search(
    browser, live_server, seeded, four_doors
):
    """Plan §1.12 item 7, as W2-C1 built the band: the four doors in the bar, «Menu» for the rest — and, as every
    sheet, the night foot with «la targa» (REVIEW M2: the letterhead's targa lies under the side sheet); a window
    widened past 80rem puts the sheet away, and the focus lands on the letterhead."""
    context, page = _open(browser, 1024, 768)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.click(MENU)
        page.wait_for_timeout(450)
        shown = page.evaluate(
            """() => { const s = document.getElementById('nav-sheet'), v = (q) => [...s.querySelectorAll(q)].filter((e) => e.getClientRects().length).length;
              return {doors: v('.nav-sheet__item--door'), rows: v('.nav-sheet__item'), langs: v('.lang-seg__link'), search: v('.nav-sheet__search'),
                      primary: v('.nav-sheet__primary'), fraud: v('.nav-sheet__fraud'), foot: v('.nav-sheet__foot'), brand: v('.nav-sheet__head .brand'),
                      targa: v('.nav-sheet__foot .targa--night')}; }"""
        )
        assert shown == {
            "doors": 0,
            "rows": 2,
            "langs": 4,
            "search": 1,
            "primary": 0,
            "fraud": 0,
            "foot": 1,
            "brand": 0,
            "targa": 1,
        }, shown
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(450)
        state = page.evaluate(STATE_JS)
        assert not state["open"] and state["lock"] is None and not state["mainHidden"], state
        assert page.evaluate("document.activeElement === document.querySelector('.site-header__inner > .brand')")
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_signed_in_the_targa_opens_the_account_popover(browser, live_server, seeded, four_doors, person_user, lang):
    """N13 and plan §1.11: the same seat, signed in, opens the overlay system's account popover — hung on the
    trigger's inline end, the focus on its first row, the arrows, Esc and the focus back, closed when the focus
    leaves; the seat holds 44 px under a finger."""
    context, page = _open(browser, 1440, 900)
    try:
        context.add_cookies([_session(live_server, person_user)])
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        trigger = page.locator(".site-header__end .account-menu__summary")
        trigger.click()
        page.wait_for_timeout(350)
        geo = page.evaluate(
            """() => { const t = document.querySelector('.site-header__end .account-menu__summary').getBoundingClientRect();
              const p = document.getElementById('account-menu'), b = p.getBoundingClientRect();
              return {open: p.matches(':popover-open'), expanded: document.querySelector('.site-header__end .account-menu__summary').getAttribute('aria-expanded'),
                      gap: Math.round(b.top - t.bottom), left: Math.round(b.left - t.left), right: Math.round(b.right - t.right),
                      first: document.activeElement === p.querySelector('.overlay__item')}; }"""
        )
        assert geo["open"] and geo["expanded"] == "true" and geo["first"], geo
        assert 0 <= geo["gap"] <= 8, geo
        assert abs(geo["left" if lang == "ar" else "right"]) <= 1, f"hung on the trigger's inline end: {geo}"
        page.keyboard.press("ArrowDown")
        assert page.evaluate("document.activeElement === document.querySelectorAll('#account-menu .overlay__item')[1]")
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        assert not page.evaluate("document.getElementById('account-menu').matches(':popover-open')")
        assert page.evaluate(
            "document.activeElement === document.querySelector('.site-header__end .account-menu__summary')"
        )
        # the focus leaving the menu closes it (S-7)
        trigger.click()
        page.wait_for_timeout(300)
        page.evaluate("document.querySelector('.site-header__inner > .brand').focus()")
        page.wait_for_timeout(250)
        assert not page.evaluate("document.getElementById('account-menu').matches(':popover-open')")
    finally:
        context.close()
    context, page = _open(browser, 1024, 768, has_touch=True)
    try:
        context.add_cookies([_session(live_server, person_user)])
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        box = page.locator(".site-header__end .account-menu__summary").bounding_box()
        assert box["width"] >= 44 and box["height"] >= 44, box
    finally:
        context.close()


def test_the_key_alone_is_named_by_the_systems_top_layer_tooltip(browser, live_server, seeded, four_doors):
    """N13 and plan §1.11: below 100rem «la targa» is the key alone, named by the overlay system's top-layer tooltip —
    after the wait under the pointer, at once on the keyboard's focus, put away by Esc (1.4.13); from 100rem the plate
    says its word and the tip is refused (nav.js, the system's `overlay:tip`)."""
    tip = "(() => { const t = document.querySelector('.tooltip'); return t && t.matches(':popover-open') ? t.textContent : null; })()"
    context, page = _open(browser, 1280, 800)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        targa = page.locator(".site-header__end > .targa")
        box = targa.bounding_box()
        assert box["width"] == 32 and box["height"] == 32, box
        page.mouse.move(box["x"] + 16, box["y"] + 16)
        page.wait_for_timeout(150)
        assert page.evaluate(tip) is None, "nothing before the wait"
        page.wait_for_timeout(600)
        assert page.evaluate(tip) == "Espace réservé"
        under = page.evaluate("document.querySelector('.tooltip').getBoundingClientRect().top")
        assert under >= box["y"] + box["height"], "below the plate"
        page.keyboard.press("Escape")
        assert page.evaluate(tip) is None, "Esc puts it away while the pointer stays"
        page.mouse.move(640, 600)
        page.keyboard.press("Tab")  # the keyboard's modality, then the focus on the key
        targa.focus()
        page.wait_for_timeout(100)
        assert page.evaluate(tip) == "Espace réservé", "at once on the keyboard's focus"
    finally:
        context.close()
    context, page = _open(browser, 1600, 900)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        targa = page.locator(".site-header__end > .targa")
        assert targa.locator(".targa__label").is_visible()
        box = targa.bounding_box()
        page.mouse.move(box["x"] + 10, box["y"] + 10)
        page.wait_for_timeout(800)
        assert page.evaluate(tip) is None, "the plate says its word: no tip"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_flag_off_leaves_no_hole_in_the_letterhead(browser, live_server, seeded, four_doors, set_flag, lang):
    """N13 and plan §1.11: with `reserved_area_public_link` off, «la targa» is not drawn and leaves no hole — from 80rem,
    where «Menu» is not drawn either, the bar's inline end sits on the column's edge (no empty end zone, no gap)."""
    set_flag("reserved_area_public_link", False)
    edges = """() => {
      const inner = document.querySelector('.site-header__inner'), nav = document.querySelector('.main-nav[data-portico]');
      const s = getComputedStyle(inner), b = inner.getBoundingClientRect(), n = nav.getBoundingClientRect();
      const rtl = document.documentElement.dir === 'rtl';
      const edge = rtl ? b.left + parseFloat(s.paddingLeft) : b.right - parseFloat(s.paddingRight);
      return {targa: document.querySelectorAll('.targa').length, edge: Math.round(edge), navEnd: Math.round(rtl ? n.left : n.right),
              endZone: getComputedStyle(document.querySelector('.site-header__end')).display};
    }"""
    for width in (1280, 1440, 1920):
        context, page = _open(browser, width, 900)
        try:
            page.goto(f"{live_server.url}/{lang}/", wait_until="load")
            state = page.evaluate(edges)
            assert state["targa"] == 0, state
            assert abs(state["navEnd"] - state["edge"]) <= 1, (width, state)
        finally:
            context.close()


def test_no_photograph_on_a_phone_nor_with_save_data(browser, live_server, seeded, four_doors):
    """N8: on a phone the sheet draws discs, never the doors' photographs — opened, every door unfolded — and from
    80rem a Save-Data visitor gets none at idle either."""
    context, page = _open(browser, 390, 844, has_touch=True)
    try:
        requests: list[str] = []
        page.on("request", lambda r: requests.append(r.url))
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.tap(MENU)
        page.wait_for_timeout(450)
        doors = page.locator(f"{SHEET} details > summary")
        for i in range(doors.count()):
            doors.nth(i).tap()
            page.wait_for_timeout(100)
        page.wait_for_timeout(2500)
        assert [u for u in requests if "/img/portico/" in u] == []
    finally:
        context.close()
    context, page = _open(browser, 1440, 900)
    try:
        page.add_init_script(
            "Object.defineProperty(navigator, 'connection', {value: {saveData: true}, configurable: true})"
        )
        requests = []
        page.on("request", lambda r: requests.append(r.url))
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.wait_for_timeout(3500)
        assert [u for u in requests if "/img/portico/" in u] == []
    finally:
        context.close()


#: The 64–80rem band's row at the rendered boxes (REVIEW M1, N11): the content column, what the row's items need
#: beside each other (the bar's items at their natural width), the spare and the bar's rows.
BAND_JS = """async () => {
  await document.fonts.ready;
  const inner = document.querySelector('.site-header__inner'), cs = getComputedStyle(inner);
  const column = inner.clientWidth - parseFloat(cs.paddingInlineStart) - parseFloat(cs.paddingInlineEnd);
  const kids = [...inner.children].filter((k) => getComputedStyle(k).display !== 'none');
  const items = [...document.querySelectorAll('.main-nav__list > li')].filter((li) => getComputedStyle(li).display !== 'none');
  const bar = items.reduce((sum, li) => sum + li.getBoundingClientRect().width + (parseFloat(getComputedStyle(li).marginInlineStart) || 0), 0);
  const need = kids.reduce((sum, k) => sum + (k.classList.contains('main-nav') ? bar : k.getBoundingClientRect().width), 0)
    + (parseFloat(cs.columnGap) || 0) * (kids.length - 1);
  return {column: Math.round(column * 10) / 10, spare: Math.round((column - need) * 10) / 10, items: items.length,
          rows: new Set(items.map((li) => Math.round(li.getBoundingClientRect().top))).size,
          header: Math.round(document.querySelector('.site-header').getBoundingClientRect().height)};
}"""


@pytest.mark.parametrize("lang", ["fr", "en", "it", "ar"])
def test_the_band_holds_one_row_with_24_px_to_spare_at_1024(
    browser, live_server, seeded, four_doors, person_user, lang
):
    """REVIEW M1 and N11 («one row, ≥ 24 px spare at 1024 px in the longest language»): from 64 to 80rem the lock-up is
    drawn at the compact 32/17, so the French row — 945 px with the full lock-up under a finger, where the plate and
    «Menu» are 44 px, in a 944 px column: an iPad in landscape drew two rows — holds one row with 24 px to spare under a
    fine pointer, under a coarse one (has_touch + is_mobile) and beside a 17 px classic scrollbar (Windows; the gutter
    emulated by the root's padding: the media query still sees 1024), signed out and signed in."""
    for signed_in in (False, True):
        for touch in (False, True):
            extra = {"has_touch": True, "is_mobile": True} if touch else {}
            context, page = _open(browser, 1024, 768, **extra)
            try:
                if signed_in:
                    context.add_cookies([_session(live_server, person_user)])
                page.goto(f"{live_server.url}/{lang}/", wait_until="load")
                assert page.evaluate("matchMedia('(pointer: coarse)').matches") is touch
                for gutter in (0, 17):
                    page.evaluate(f"document.documentElement.style.paddingInlineEnd = '{gutter}px'")
                    fit = page.evaluate(BAND_JS)
                    where = f"{lang} 1024 {'coarse' if touch else 'fine'} gutter {gutter} {'signed in' if signed_in else 'signed out'}"
                    assert fit["column"] == 944 - gutter, (where, fit)
                    assert fit["items"] == 4 and fit["rows"] == 1 and fit["header"] <= 65, (where, fit)
                    assert fit["spare"] >= 24, f"{fit['spare']} px to spare ({where}): {fit}"
            finally:
                context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_side_sheet_ends_on_its_night_foot(browser, live_server, seeded, four_doors, lang):
    """REVIEW M2 and m3: from 48rem the side sheet keeps the pinned night foot — «la targa» at 44 px, the promoter — as
    every sheet does (the letterhead's targa lies under it), and its head drops only the duplicate lock-up; on its own
    24 px margin the primary holds one line at 768; the trap's cycle reaches the foot's targa and wraps."""
    context, page = _open(browser, 768, 1024, has_touch=True)
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        page.tap(MENU)
        page.wait_for_timeout(500)
        geo = page.evaluate(
            """() => { const s = document.getElementById('nav-sheet'), r = (q) => { const e = s.querySelector(q); return e && e.getClientRects().length ? e.getBoundingClientRect() : null; };
              const body = s.querySelector('.nav-sheet__body'), cs = getComputedStyle(body), foot = r('.nav-sheet__foot'), targa = r('.nav-sheet__foot .targa--night');
              return {foot: foot && [foot.top, foot.bottom].map(Math.round), sheet: Math.round(s.getBoundingClientRect().bottom), brand: r('.nav-sheet__head .brand'),
                      targa: targa && [Math.round(targa.width), Math.round(targa.height)], promoter: Boolean(r('.nav-sheet__promoter')),
                      margin: cs.paddingInlineStart, column: Math.round(body.clientWidth - parseFloat(cs.paddingInlineStart) - parseFloat(cs.paddingInlineEnd)),
                      lines: (() => { const tops = new Set(), range = document.createRange();
                        const walk = document.createTreeWalker(s.querySelector('.nav-sheet__primary'), NodeFilter.SHOW_TEXT);
                        for (let n = walk.nextNode(); n; n = walk.nextNode()) { if (!n.textContent.trim()) continue;
                          range.selectNodeContents(n); for (const b of range.getClientRects()) if (b.width > 1) tops.add(Math.round(b.top)); }
                        return tops.size; })()}; }"""
        )
        assert geo["foot"] and geo["foot"][1] == geo["sheet"] and geo["promoter"] and geo["brand"] is None, geo
        assert geo["targa"][1] >= 44 and geo["targa"][0] == geo["column"], geo
        assert geo["margin"] == "24px" and geo["column"] >= 350, geo
        assert geo["lines"] == 1, f"the primary on one line: {geo}"
        stops = []
        for _ in range(20):
            page.keyboard.press("Tab")
            stops.append(
                page.evaluate(
                    "document.activeElement.matches('.nav-sheet__foot .targa') ? 'targa' : document.activeElement.matches('.nav-sheet__head .nav-toggle') ? 'fermer' : document.getElementById('nav-sheet').contains(document.activeElement)"
                )
            )
        assert all(stops) and "targa" in stops and stops.index("fermer") == stops.index("targa") + 1, stops
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_tap_on_the_menu_sheets_scrim_reaches_nothing_beneath(
    browser, live_server, seeded, four_doors, person_user, lang
):
    """A11Y_PERF M1: signed in on a phone, the account menu opened from the sheet's foot is a bottom sheet over the one
    scrim. A tap on that scrim closes the menu and nothing else: the platform light-dismisses the menu as the press goes
    down, and a touch's compatibility mouse events and its click are hit-tested later — the scrim keeps its place over
    the trapped sheet until the press ends (overlay.js), so the door under the finger stays folded, Forum is not
    followed, the language does not change; the focus is back on the foot's trigger, the sheet still open and modal."""
    for target in ("door", "forum", "language"):
        context, page = _open(browser, 390, 844, has_touch=True, is_mobile=True)
        try:
            context.add_cookies([_session(live_server, person_user)])
            page.goto(f"{live_server.url}/{lang}/", wait_until="load")
            page.tap(MENU)
            page.wait_for_timeout(500)
            page.tap(f"{SHEET} .nav-sheet__foot .account-menu__summary")
            page.wait_for_timeout(600)
            assert page.evaluate("document.getElementById('account-menu-sheet').matches(':popover-open')")
            row = {
                "door": "document.querySelectorAll('#nav-sheet summary.nav-sheet__row')[2]",
                "forum": "document.querySelector('#nav-sheet a.nav-sheet__row')",
                "language": "document.querySelectorAll('#nav-sheet .lang-seg__link')[2]",
            }[target]
            x, y = page.evaluate(
                f"(() => {{ const b = {row}.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; }})()"
            )
            assert page.evaluate(f"document.elementFromPoint({x}, {y}).classList.contains('overlay-scrim')"), target
            url = page.url
            page.touchscreen.tap(x, y)
            page.wait_for_timeout(700)
            state = page.evaluate(
                """() => ({menu: document.getElementById('account-menu-sheet').matches(':popover-open'),
                          doors: [...document.querySelectorAll('#nav-sheet details.nav-sheet__door')].some((d) => d.open),
                          onTrigger: document.activeElement === document.querySelector('#nav-sheet .nav-sheet__foot .account-menu__summary'),
                          sheet: document.getElementById('nav-sheet').open, modal: document.getElementById('nav-sheet').getAttribute('aria-modal')})"""
            )
            assert state == {"menu": False, "doors": False, "onTrigger": True, "sheet": True, "modal": "true"}, (
                target,
                state,
            )
            assert page.url == url, (target, page.url)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_account_menu_from_the_night_foot_draws_the_paper_ring(
    browser, live_server, seeded, four_doors, person_user, lang
):
    """A11Y_PERF M2 (WCAG 1.4.11, plan §1.6): the account menu opened from the sheet's night foot is a paper panel —
    each focused row draws the paper's ring (#1d8a93, 4.11 : 1 on white) and its glyph the paper's ink, never the
    night's (#7fd1d8, 1.75 : 1 on white), on a phone (a bottom sheet) and at 768 (anchored); the foot's trigger keeps
    the night's ring."""
    for width, height in ((390, 844), (768, 1024)):
        context, page = _open(browser, width, height, has_touch=True, is_mobile=True)
        try:
            context.add_cookies([_session(live_server, person_user)])
            page.goto(f"{live_server.url}/{lang}/", wait_until="load")
            page.tap(MENU)
            page.wait_for_timeout(500)
            page.focus(f"{SHEET} .nav-sheet__foot .account-menu__summary")
            page.keyboard.press("Shift+Tab")
            page.keyboard.press("Tab")  # the keyboard's modality, then the trigger
            trigger = page.evaluate("getComputedStyle(document.activeElement).outlineColor")
            page.keyboard.press("Enter")
            page.wait_for_timeout(400)
            rings = []
            for _ in range(page.evaluate("document.querySelectorAll('#account-menu-sheet .overlay__item').length")):
                rings.append(
                    page.evaluate(
                        "(() => { const a = document.activeElement; return [a.closest('#account-menu-sheet') !== null, getComputedStyle(a).outlineColor, getComputedStyle(a.querySelector('.icon')).color]; })()"
                    )
                )
                page.keyboard.press("ArrowDown")
            assert trigger == "rgb(127, 209, 216)", (width, trigger)
            assert rings and all(r == [True, "rgb(29, 138, 147)", "rgb(74, 90, 98)"] for r in rings), (width, rings)
        finally:
            context.close()


def test_an_overlay_opening_puts_the_door_panel_away(browser, live_server, seeded, four_doors):
    """REVIEW m2: in Safari and on an iPad a press does not focus the button pressed, so a door's panel pinned by a press
    has no focus to lose — the nav's focusout never comes. The overlay system's «overlay:open» puts the panel away:
    here a door opened and «Menu» pressed by clicks that move no focus (dispatched, as WebKit's press)."""
    context, page = _open(browser, 1024, 768)
    try:
        page.goto(f"{live_server.url}/fr/", wait_until="load")
        page.wait_for_timeout(300)
        page.dispatch_event("[data-portico-door] >> nth=0", "click")
        page.wait_for_timeout(250)
        assert page.evaluate("document.querySelector('[data-portico-door]').getAttribute('aria-expanded')") == "true"
        assert page.evaluate("document.activeElement === document.body"), "no focus moved by the press"
        page.dispatch_event(MENU, "click")
        page.wait_for_timeout(450)
        state = page.evaluate(
            "[document.getElementById('nav-sheet').open, document.querySelector('[data-portico-door]').getAttribute('aria-expanded'), document.querySelector('[data-portico-scrim]').hidden]"
        )
        assert state == [True, "false", True], state
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_short_viewport_does_not_pin_the_foot(browser, live_server, seeded, four_doors, lang):
    """A11Y_PERF m1 (WCAG 1.4.10): at 320 × 256 (400 % of 1280 × 1024) the head and a pinned foot left the list 80 px;
    under 30rem of height the sheet scrolls as one under its head, the foot at the end of the list — the list takes at
    least half the viewport, and the keyboard reaches «la targa» at the end, every stop whole and never under the head."""
    context, page = _open(browser, 320, 256)
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        page.click(MENU)
        page.wait_for_timeout(500)
        share = page.evaluate(
            """() => { const s = document.getElementById('nav-sheet'), head = s.querySelector('.nav-sheet__head').getBoundingClientRect();
              const body = s.querySelector('.nav-sheet__body').getBoundingClientRect(), foot = s.querySelector('.nav-sheet__foot').getBoundingClientRect();
              return (Math.min(body.bottom, foot.top, innerHeight) - Math.max(body.top, head.bottom)) / innerHeight; }"""
        )
        assert share >= 0.5, share
        reached = False
        for _ in range(30):
            page.keyboard.press("Tab")
            stop = page.evaluate(
                """() => { const a = document.activeElement, s = document.getElementById('nav-sheet'), head = s.querySelector('.nav-sheet__head');
                  const b = a.getBoundingClientRect(), h = head.getBoundingClientRect();
                  return {inside: s.contains(a), hidden: !head.contains(a) && b.top < h.bottom - 0.5, off: b.top < -0.5 || b.bottom > innerHeight + 0.5,
                          targa: a.matches('.nav-sheet__foot .targa')}; }"""
            )
            assert stop["inside"] and not stop["hidden"] and not stop["off"], stop
            if stop["targa"]:
                reached = True
                break
        assert reached, "the foot's targa is reached at the end of the list"
    finally:
        context.close()
