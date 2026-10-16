"""
The console shell «Tre livelli» in the browser — design V5, family W3-A (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.18
D06, §3.5 item 3; docs/design-v5/QA/v54/w3-a/NOTES.md). What a static test cannot see:

* at 1366 × 657 — a 1366 × 768 laptop less the browser's own bars (the platform audit's S-1) — the open rail of a
  person holds whole, in French and in Arabic, and its foot (the account, sign-out, the language, the rail's
  control, «Site public») is in view; for an account whose rail is longer the foot stays in view and the last page
  is reached by scrolling the list;
* the rail is open from 80rem and compact below, the choice is kept, and it is written before the first frame: no
  layout shift; the glyph column does not move when the rail folds; nothing of the shell animates at load;
* the skip links: the content, the rail — and on a phone «Menu», in three keys (the audit's S-2);
* «il lume» marks the current page once per rail copy, by a shape and a weight, never by a bar at the edge;
* a glyph that stands alone shows its word on focus and puts it away on Esc; the language opens above its control;
* the shell draws two corners and no shadow at rest; one start edge and one title size for every page header;
* in Arabic the rail stands at the right edge and nothing overflows, from 1024 to 1920 px.

Chromium on the seeded site; a session minted with ``Client.force_login`` — nothing typed, no password used. The
first console page of a session carries the loader's entrance release (W1-D): each test loads a page once before it
measures the shell at rest.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse

from accounts import roles
from core import icons

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DASHBOARD = "/{lang}/espace-reserve/"
REQUESTS = "/{lang}/espace-reserve/mes-demandes/"

#: The rail's geometry: its state, its rows, its scroller, its foot and every control of the foot.
RAIL_JS = """() => {
  const vh = innerHeight, vw = innerWidth;
  const rail = document.querySelector('nav.rail[data-rail]');
  const shown = (el) => { const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1 && el.checkVisibility({visibilityProperty: true}); };
  const items = [...rail.querySelectorAll('[data-rail-item]')];
  const scroller = rail.querySelector('[data-rail-scroll]');
  const foot = rail.querySelector('[data-rail-foot]');
  const view = scroller.getBoundingClientRect();
  const controls = [...foot.querySelectorAll('a[href], button, summary')].filter(shown).map((el) => {
    const r = el.getBoundingClientRect();
    return {name: (el.textContent || '').trim().replace(/\\s+/g, ' '), top: r.top, bottom: r.bottom, left: r.left,
            right: r.right, width: r.width, height: r.height};
  });
  const box = rail.getBoundingClientRect();
  return {state: document.body.dataset.rail, vw, vh, left: box.left, right: box.right, width: box.width,
    rows: [...new Set(items.map((i) => Math.round(i.getBoundingClientRect().height)))],
    count: items.length,
    words: items.filter((i) => i.querySelector('.rail__label').getBoundingClientRect().width > 4).length,
    scrollHeight: scroller.scrollHeight, clientHeight: scroller.clientHeight,
    clipped: items.filter((i) => { const r = i.getBoundingClientRect(); return r.bottom > view.bottom + 0.5 || r.top < view.top - 0.5; }).length,
    footTop: foot.getBoundingClientRect().top, footBottom: foot.getBoundingClientRect().bottom, controls,
    discX: items.map((i) => { const r = i.querySelector('.rail__disc').getBoundingClientRect(); return Math.round((r.left + r.right) / 2); }),
    expanded: rail.querySelector('[data-rail-toggle]').getAttribute('aria-expanded'),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    workspace: (() => { const r = document.querySelector('.console__workspace').getBoundingClientRect(); return {left: r.left, right: r.right}; })(),
    bar: (() => { const r = document.querySelector('.console-bar').getBoundingClientRect(); return {left: r.left, right: r.right}; })(),
  };
}"""

#: The layout shift of the load, once the page is at rest (buffered: the entries of the load are replayed).
CLS_JS = """() => new Promise((resolve) => {
  let total = 0;
  new PerformanceObserver((list) => { for (const entry of list.getEntries()) if (!entry.hadRecentInput) total += entry.value; })
    .observe({type: 'layout-shift', buffered: true});
  setTimeout(() => resolve(total), 400);
})"""

#: Whatever is animating inside the shell: CSS animations and transitions and Web Animations alike.
SHELL_MOTION_JS = """() => document.getAnimations().filter((a) => {
  const target = a.effect && a.effect.target;
  return target && target.closest && target.closest('.rail, .console-bar, .console-bottom, .console__footer, .skip-link') && a.playState === 'running';
}).map((a) => (a.animationName || a.transitionProperty || 'waapi') + '@' + a.effect.target.className)"""


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


def _context(browser, live_server, user, width=1440, height=900, stored=None, **options):
    """A signed-in context. ``stored`` is the rail's stored choice ("open" / "closed"), written before any script."""
    client = Client()
    client.force_login(user)
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
    """The page loaded twice: the first console page of a session plays the entrance release, the second is at rest."""
    page.goto(live_server.url + path, wait_until="networkidle")
    page.goto(live_server.url + path, wait_until="networkidle")
    page.wait_for_function("() => document.body.classList.contains('is-ready')")


# ---------------------------------------------------------------------------------------------- 1366 × 657


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_at_1366_by_657_the_open_rail_of_a_person_holds_whole_and_its_foot_is_in_view(
    browser, live_server, seeded, person_user, lang
):
    context = _context(browser, live_server, person_user, 1366, 657)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    rail = page.evaluate(RAIL_JS)
    assert rail["state"] == "open" and rail["width"] == 248 and rail["expanded"] == "true", "open by default from 80rem"
    assert rail["count"] == 10 and rail["words"] == 10, "ten pages, glyph + word"
    assert rail["rows"] == [40], "the density step of a short screen under a fine pointer (plan §1.8)"
    assert rail["scrollHeight"] <= rail["clientHeight"] and rail["clipped"] == 0, (
        f"nothing of a person's rail waits under a fold at 657 px: {rail['scrollHeight']} in {rail['clientHeight']}"
    )
    assert rail["footBottom"] <= rail["vh"] + 0.5 and rail["footTop"] > 0, "the foot is pinned, in view"
    names = [control["name"] for control in rail["controls"]]
    assert len(rail["controls"]) == 5, names  # the account, sign-out, the rail's control, the language, «Site public»
    for control in rail["controls"]:
        assert 0 <= control["top"] and control["bottom"] <= rail["vh"] + 0.5, control
        assert control["width"] >= 24 and control["height"] >= 24, f"a target under 24 px (WCAG 2.5.8): {control}"
    assert rail["overflow"] <= 0
    if lang == "ar":
        assert rail["right"] == rail["vw"] and rail["workspace"]["right"] <= rail["vw"] - 248 + 0.5, (
            "the rail at the right edge"
        )
    else:
        assert rail["left"] == 0 and rail["workspace"]["left"] >= 248 - 0.5
    context.close()


@pytest.mark.parametrize("size", [(1366, 657), (1280, 720), (1536, 730)], ids=lambda s: f"{s[0]}x{s[1]}")
def test_a_longer_rail_scrolls_under_its_pinned_foot_and_its_last_page_is_reached(
    browser, live_server, seeded, user_factory, size
):
    """The audit's three sizes, with an account whose rail holds a register more than a person's."""
    professional = user_factory("w3a-pro@example.test", role=roles.PROFESSIONAL, full_name="Professionnelle de test")
    for stored in ("open", "closed"):
        context = _context(browser, live_server, professional, size[0], size[1], stored=stored)
        page = context.new_page()
        _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
        rail = page.evaluate(RAIL_JS)
        assert rail["state"] == stored and rail["count"] == 11
        assert rail["footBottom"] <= rail["vh"] + 0.5, (stored, size, "the foot left the view")
        for control in rail["controls"]:
            assert control["bottom"] <= rail["vh"] + 0.5 and control["top"] >= 0, (stored, control)
        last_clear = page.evaluate(
            """() => { const s = document.querySelector('nav.rail[data-rail] [data-rail-scroll]'); s.scrollTop = s.scrollHeight;
                 const items = s.querySelectorAll('[data-rail-item]'); const last = items[items.length - 1].getBoundingClientRect();
                 return last.bottom <= s.getBoundingClientRect().bottom + 0.5; }"""
        )
        assert last_clear, (stored, size, "the last page is clear of the foot once the list is scrolled")
        context.close()


# ---------------------------------------------------------------------------------------------- the state


def test_the_rail_is_open_from_80rem_compact_below_and_the_stored_choice_shifts_nothing(
    browser, live_server, seeded, person_user
):
    # no stored choice: the width decides
    for width, state, measure in ((1440, "open", 248), (1280, "open", 248), (1100, "closed", 64)):
        context = _context(browser, live_server, person_user, width, 900)
        page = context.new_page()
        _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
        rail = page.evaluate(RAIL_JS)
        assert (rail["state"], rail["width"]) == (state, measure), (width, rail["state"], rail["width"])
        assert rail["words"] == (10 if state == "open" else 0)
        assert rail["expanded"] == ("true" if state == "open" else "false")
        context.close()
    # a stored choice against the width: applied before the first frame — the page does not move
    for width, stored, measure in ((1440, "closed", 64), (1100, "open", 248)):
        context = _context(browser, live_server, person_user, width, 900, stored=stored)
        page = context.new_page()
        _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
        rail = page.evaluate(RAIL_JS)
        assert (rail["state"], rail["width"]) == (stored, measure), (width, stored, rail)
        shift = page.evaluate(CLS_JS)
        assert shift < 0.01, f"the stored choice moved the page at load (CLS {shift:.3f}) at {width} px"
        context.close()


def test_the_control_folds_the_rail_keeps_the_choice_and_the_glyph_column_stands_still(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    before = page.evaluate(RAIL_JS)
    page.click("[data-rail-toggle]")
    page.wait_for_function("() => document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width === 64")
    after = page.evaluate(RAIL_JS)
    assert (after["state"], after["expanded"], after["words"]) == ("closed", "false", 0)
    assert page.evaluate("localStorage.getItem('ile.rail')") == "closed"
    assert after["discX"] == before["discX"] == [32] * 10, "the glyphs stand on one column, open or compact"
    assert after["bar"]["left"] == 64 and after["workspace"]["left"] >= 64, (
        "the page takes the width the rail gave back"
    )
    # the words are kept for a reader: clipped, never removed
    names = page.evaluate(
        "() => [...document.querySelectorAll('nav.rail[data-rail] [data-rail-item]')].map((a) => a.textContent.trim().replace(/\\s+/g, ' '))"
    )
    assert names[0] == "Tableau de bord" and len(names) == 10
    assert (
        page.evaluate("getComputedStyle(document.querySelector('nav.rail[data-rail] .rail__label')).display") != "none"
    )
    # the choice survives the next page
    page.goto(live_server.url + DASHBOARD.format(lang="fr"), wait_until="networkidle")
    assert page.evaluate(RAIL_JS)["state"] == "closed"
    page.click("[data-rail-toggle]")
    page.wait_for_function("() => document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width === 248")
    assert page.evaluate("localStorage.getItem('ile.rail')") == "open"
    context.close()


def test_nothing_of_the_shell_animates_at_load_and_reduced_motion_folds_at_once(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user, 1440, 900)
    page = context.new_page()
    page.goto(live_server.url + REQUESTS.format(lang="fr"), wait_until="networkidle")  # the session's entrance release
    for path in (REQUESTS, DASHBOARD):
        page.goto(live_server.url + path.format(lang="fr"), wait_until="commit")
        page.wait_for_selector("nav.rail[data-rail]", state="attached")
        assert page.evaluate(SHELL_MOTION_JS) == [], f"{path}: the shell moves while the page loads"
        page.wait_for_load_state("networkidle")
        assert page.evaluate(SHELL_MOTION_JS) == [], f"{path}: the shell moves once the page is loaded"
    context.close()
    reduced = _context(browser, live_server, person_user, 1440, 900, reduced_motion="reduce")
    page = reduced.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.click("[data-rail-toggle]")
    assert page.evaluate("document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width") == 64, (
        "under reduced motion the rail has its new width in the same frame"
    )
    assert page.evaluate(SHELL_MOTION_JS) == []
    reduced.close()


# ---------------------------------------------------------------------------------------------- the keyboard


def test_the_skip_links_reach_the_content_the_rail_and_on_a_phone_the_menu_in_three_keys(
    browser, live_server, seeded, person_user
):
    focused = "() => ({text: document.activeElement.textContent.trim(), id: document.activeElement.id, tag: document.activeElement.tagName, role: document.activeElement.getAttribute('role')})"
    desktop = _context(browser, live_server, person_user, 1440, 900)
    page = desktop.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Aller au contenu principal"
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Navigation de l’espace réservé"
    page.wait_for_function(
        "() => document.activeElement.getBoundingClientRect().top >= 0", timeout=3000
    )  # it slides in
    box = page.evaluate(
        "(() => { const r = document.activeElement.getBoundingClientRect(); return [r.top, r.bottom, r.left]; })()"
    )
    assert 0 <= box[0] and box[1] <= 120 and box[2] >= 0, "the focused skip link is drawn, at the page's first corner"
    page.keyboard.press("Enter")
    assert page.evaluate(focused)["id"] == "console-rail"
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.classList.contains('rail__brand')"), "the rail's first stop follows"
    desktop.close()

    phone = _context(browser, live_server, person_user, 390, 844, has_touch=True, is_mobile=True)
    page = phone.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Aller au contenu principal"
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Menu", "below 64rem the second skip link is «Menu»: the rail is not drawn"
    page.keyboard.press("Enter")
    landed = page.evaluate(focused)
    assert (landed["id"], landed["tag"], landed["role"]) == ("console-menu", "A", "button"), (
        f"three keys to «Menu» (the audit's S-2) — a link to the drawer that script turns into its button: {landed}"
    )
    page.keyboard.press("Enter")
    page.wait_for_selector("dialog.console-drawer[open]")
    phone.close()


def test_il_lume_marks_the_current_page_once_per_rail_copy_and_a_lone_glyph_shows_its_word(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    lume = page.evaluate(
        """() => { const rail = document.querySelector('nav.rail[data-rail]');
          const current = [...rail.querySelectorAll('[data-rail-item][aria-current="page"]')];
          const item = current[0]; const disc = item.querySelector('.rail__disc');
          const others = [...rail.querySelectorAll('[data-rail-item]:not([aria-current])')];
          return {count: current.length, drawer: document.querySelectorAll('nav.rail--drawer [data-rail-item][aria-current="page"]').length,
            key: item.dataset.key, disc: getComputedStyle(disc).backgroundColor, glyph: getComputedStyle(disc).color,
            radius: getComputedStyle(disc).borderTopLeftRadius, plate: getComputedStyle(item).backgroundColor,
            weight: getComputedStyle(item).fontWeight, bar: getComputedStyle(item, '::before').content,
            otherDiscs: [...new Set(others.map((o) => getComputedStyle(o.querySelector('.rail__disc')).backgroundColor))],
            otherWeights: [...new Set(others.map((o) => getComputedStyle(o).fontWeight))],
            tile: getComputedStyle(rail.querySelector('.rail__tile')).backgroundColor}; }"""
    )
    assert (lume["count"], lume["drawer"], lume["key"]) == (1, 1, "requests"), "once per rail copy"
    assert lume["disc"] == lume["tile"] == "rgb(255, 255, 255)", "the lit paper disc is the tile's own material"
    assert lume["glyph"] == "rgb(21, 34, 42)" and lume["weight"] == "600" and lume["plate"] != "rgba(0, 0, 0, 0)"
    assert lume["bar"] == "none", "no bar at the edge"
    assert lume["otherDiscs"] == ["rgba(0, 0, 0, 0)"] and lume["otherWeights"] == ["500"]

    # the word — the overlay system's one top-layer tip (W2-A): where it stands, whether it is whole, and which
    # controls of the rail it lies over
    tip = """() => { const t = document.querySelector('.tooltip'); if (!t || !t.matches(':popover-open')) return {on: false};
      const r = t.getBoundingClientRect();
      const rail = document.querySelector('nav.rail[data-rail]');
      const over = [...rail.querySelectorAll('a[href], button, summary')].filter((el) => {
        const b = el.getBoundingClientRect();
        return el.checkVisibility() && b.width > 1 && b.left < r.right && b.right > r.left && b.top < r.bottom && b.bottom > r.top; });
      return {on: true, text: t.textContent, left: r.left, right: r.right, top: r.top,
        bottom: r.bottom, vh: innerHeight, fits: t.scrollWidth <= t.clientWidth + 1, over: over.length}; }"""
    # open: a page shows its word, so no tip; sign-out never does, so it has one
    page.focus("nav.rail[data-rail] [data-rail-item][data-key='documents']")
    assert page.evaluate(tip)["on"] is False
    page.focus("nav.rail[data-rail] .rail__signout button")
    shown = page.evaluate(tip)
    assert shown["on"] and shown["text"] == "Se déconnecter" and shown["left"] >= 248, "beyond the rail's edge"
    assert shown["over"] == 0 and shown["fits"] and 0 <= shown["top"] and shown["bottom"] <= shown["vh"], shown
    # the rail's own control stands at the start of the foot's last row: its word must not lie over the language
    page.focus("nav.rail[data-rail] [data-rail-toggle]")
    shown = page.evaluate(tip)
    assert shown["on"] and shown["text"] == "Navigation" and shown["left"] >= 248 and shown["over"] == 0, (
        f"a word over the next control keeps it out of reach while the pointer rests on the word: {shown}"
    )
    assert 0 <= shown["top"] and shown["bottom"] <= shown["vh"], "whole inside the viewport"
    page.focus("nav.rail[data-rail] .rail__signout button")
    page.keyboard.press("Escape")
    assert page.evaluate(tip)["on"] is False, "Esc puts the word away (WCAG 1.4.13)"
    assert page.evaluate("document.activeElement.closest('.rail__signout') !== null"), "and the focus stays"
    # the pointer brings the word too, after the tooltip's wait; the pointer may rest on it; Esc puts it away
    # wherever the focus is
    page.evaluate("document.activeElement.blur()")
    page.hover("nav.rail[data-rail] .rail__signout button")
    page.wait_for_function("() => document.querySelector('.tooltip:popover-open')", timeout=3000)
    page.hover(".tooltip")
    page.wait_for_timeout(300)
    assert page.evaluate(tip)["on"] is True, "the pointer may rest on the word (WCAG 1.4.13: hoverable)"
    assert page.evaluate("document.activeElement === document.body")
    page.keyboard.press("Escape")
    assert page.evaluate(tip)["on"] is False, "dismissible without moving the pointer, the focus being elsewhere"
    page.mouse.move(700, 300)
    # compact: every glyph has its word beside it on the keyboard's focus — the pointer's press on the rail's
    # control did not bring one: the rail's arrows take the focus to the page
    page.click("[data-rail-toggle]")
    page.wait_for_function("() => document.querySelector('nav.rail[data-rail]').getBoundingClientRect().width === 64")
    page.focus("nav.rail[data-rail] [data-rail-item][data-key='requests']")
    page.keyboard.press("ArrowDown")
    shown = page.evaluate(tip)
    assert shown["on"] and shown["text"] == "Mes documents" and shown["left"] >= 64 and shown["over"] == 0
    # compact, the account is a glyph: its word says the name and who the account is
    page.focus("nav.rail[data-rail] .rail__who")
    shown = page.evaluate(tip)
    assert shown["on"] and shown["text"].endswith("— Personne") and shown["left"] >= 64 and shown["fits"], shown
    context.close()

    arabic = _context(browser, live_server, person_user, 1440, 900, stored="closed")
    page = arabic.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="ar"))
    page.focus("nav.rail[data-rail] [data-rail-item][data-key='documents']")
    shown = page.evaluate(tip)
    assert shown["on"] and shown["right"] <= 1440 - 64, "in Arabic the word stands on the page's side of the rail"
    assert shown["over"] == 0 and shown["fits"]
    arabic.close()


def test_the_language_opens_above_its_control_by_the_languages_own_names(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    summary = page.locator("nav.rail[data-rail] .rail__lang-summary")
    assert summary.inner_text().strip().endswith("Français")
    before = summary.bounding_box()
    summary.click()
    page.wait_for_selector("nav.rail[data-rail] .rail__lang[open]")
    menu = page.evaluate(
        """() => { const m = document.querySelector('nav.rail[data-rail] .rail__lang .lang-seg'); const r = m.getBoundingClientRect();
          const links = [...m.querySelectorAll('a')];
          return {top: r.top, bottom: r.bottom, left: r.left, right: r.right,
            names: links.map((a) => a.textContent.trim()), current: links.filter((a) => a.hasAttribute('aria-current')).map((a) => a.textContent.trim()),
            x: links.map((a) => Math.round(a.querySelector('.lang-seg__name').getBoundingClientRect().left))}; }"""
    )
    after = summary.bounding_box()
    assert after == before, "the control stays under the pointer: the menu opens over the row above"
    assert menu["bottom"] <= before["y"] and menu["top"] >= 0 and menu["left"] >= 0 and menu["right"] <= 248
    assert menu["names"] == ["Italiano", "Français", "English", "العربية"] and menu["current"] == ["Français"]
    assert set(menu["x"]) == {64}, "the names stand on the rail's text axis, whatever their own direction"
    page.keyboard.press("Escape")
    page.wait_for_selector("nav.rail[data-rail] .rail__lang:not([open])")
    assert page.evaluate("document.activeElement.classList.contains('rail__lang-summary')"), (
        "the focus returns to the control"
    )
    context.close()


# ---------------------------------------------------------------------------------------------- the frame


def test_the_shell_draws_two_corners_no_shadow_at_rest_and_one_edge_for_every_page_header(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    drawn = page.evaluate(
        """() => { const radii = new Set(), shadows = new Set();
          for (const el of document.querySelectorAll('.rail:not(.rail--drawer) *, .rail:not(.rail--drawer), .console-bar, .console-bar *, .console__footer, .console__footer *')) {
            const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
            if (r.width < 2 || r.height < 2 || s.display === 'none' || el.closest('details:not([open]) > :not(summary)')) continue;
            const v = parseFloat(s.borderTopLeftRadius);
            radii.add(v === 0 ? '0' : v >= Math.min(r.width, r.height) / 2 - 0.5 ? 'full' : s.borderTopLeftRadius);
            if (s.boxShadow !== 'none') shadows.add(el.className + ' ' + s.boxShadow);
          }
          return {radii: [...radii].sort(), shadows: [...shadows]}; }"""
    )
    assert drawn["radii"] == ["0", "4px", "full"], f"the shell's corners: 4 px and full (plan §1.3): {drawn['radii']}"
    assert drawn["shadows"] == [], f"navigation never carries a shadow (SH-2): {drawn['shadows']}"

    # one start edge and one title size, whatever header a page's family still carries
    edges = {}
    for name, path in (
        ("page-header", "/fr/espace-reserve/mes-demandes/"),
        ("ws-head", "/fr/espace-reserve/mes-documents/"),
        ("ws-head-empty", "/fr/espace-reserve/"),
        ("doc-page", "/documents/"),
        ("academy", "/fr/espace-reserve/formation/"),
    ):
        page.goto(live_server.url + path, wait_until="networkidle")
        edges[name] = page.evaluate(
            """() => { const h = document.querySelector('.console__workspace h1'); const r = h.getBoundingClientRect(); const s = getComputedStyle(h);
              const f = document.querySelector('.console__footer .portal-footer__legal').getBoundingClientRect();
              const w = getComputedStyle(document.querySelector('.console__workspace'));
              return {x: Math.round(r.left), size: s.fontSize, line: s.lineHeight, weight: s.fontWeight, foot: Math.round(f.left),
                      pad: [w.paddingInlineStart, w.paddingBlockStart], crumb: Math.round(document.querySelector('.console-bar .breadcrumbs__list').getBoundingClientRect().left),
                      h1: document.querySelectorAll('h1').length}; }"""
        )
    for name, edge in edges.items():
        assert edge["h1"] == 1, name
        assert (edge["x"], edge["foot"], edge["crumb"]) == (280, 280, 280), (
            f"{name}: one start edge, 32 px from the rail: {edge}"
        )
        assert (edge["size"], edge["line"], edge["weight"]) == ("28px", "36px", "600"), (
            f"{name}: the console's title: {edge}"
        )
        assert edge["pad"] == ["32px", "32px"], name
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_nothing_overflows_from_1024_to_1920_and_in_arabic_the_rail_stands_at_the_right_edge(
    browser, live_server, seeded, person_user, lang
):
    context = _context(browser, live_server, person_user, 1920, 1080)
    page = context.new_page()
    page.goto(live_server.url + DASHBOARD.format(lang=lang), wait_until="networkidle")
    for width, height in ((1920, 1080), (1440, 900), (1366, 657), (1280, 800), (1024, 768)):
        page.set_viewport_size({"width": width, "height": height})
        for path in (DASHBOARD, REQUESTS, "/{lang}/espace-reserve/mes-documents/"):
            page.goto(live_server.url + path.format(lang=lang), wait_until="networkidle")
            rail = page.evaluate(RAIL_JS)
            assert rail["overflow"] <= 0, (lang, width, path, rail["overflow"])
            assert rail["footBottom"] <= height + 0.5, (lang, width, path)
            if lang == "ar":
                assert rail["right"] == width and rail["workspace"]["right"] <= rail["left"] + 0.5, (width, path)
            else:
                assert rail["left"] == 0 and rail["workspace"]["left"] >= rail["right"] - 0.5, (width, path)
            assert page.evaluate("document.documentElement.dir") == ("rtl" if lang == "ar" else "ltr")
    context.close()


def test_an_account_with_two_spaces_is_told_which_one_it_is_in_and_offered_the_other(
    browser, live_server, seeded, user_factory
):
    company = user_factory("w3a-two@example.test", role=roles.COMPANY, full_name="Entreprise de test")
    context = _context(browser, live_server, company, 1440, 900)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    head = "() => ({space: document.querySelector('nav.rail[data-rail] [data-rail-space]').textContent.trim(), ways: [...document.querySelectorAll('nav.rail[data-rail] .rail__switch')].map((a) => [a.textContent.trim(), a.getAttribute('href')]), who: document.querySelector('nav.rail[data-rail] .rail__who-role').textContent.trim()})"
    reserved = page.evaluate(head)
    assert reserved == {
        "space": "Espace réservé",
        "ways": [["Espace entreprise", reverse("companies:dashboard")]],
        "who": "Entreprise",
    }
    assert page.evaluate(RAIL_JS)["count"] == 10, "the other space is not a page of this rail"
    page.click("nav.rail[data-rail] .rail__switch")
    page.wait_for_load_state("networkidle")
    there = page.evaluate(head)
    assert there["space"] == "Espace entreprise" and there["ways"] == [["Espace réservé", "/fr/espace-reserve/"]]
    assert there["who"] == "Entreprise", "who the account is does not change with the space"
    context.close()


#: Who the account is, as the rail's foot draws it: the glyph of its disc, its name, its word — and whether the word fits.
WHO_JS = """() => { const who = document.querySelector('nav.rail[data-rail] .rail__who');
  const role = who.querySelector('.rail__who-role'); const name = who.querySelector('.rail__who-name');
  const box = who.getBoundingClientRect();
  return {glyph: who.querySelector('.rail__who-disc use').getAttribute('href').split('#')[1],
    name: name.textContent.trim(), role: role.textContent.trim(),
    roleClipped: role.scrollWidth > role.clientWidth + 1, nameClipped: name.scrollWidth > name.clientWidth + 1,
    label: who.dataset.label, top: box.top, bottom: box.bottom,
    space: document.querySelector('nav.rail[data-rail] [data-rail-space]').textContent.trim()}; }"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_an_institution_a_university_and_the_project_team_are_told_apart_at_the_foot(
    browser, live_server, seeded, user_factory, lang
):
    """Persona ≠ Impresa ≠ Istituzione ≠ Università (plan §1.7): the same «Espace réservé», another account."""
    accounts = {
        "institution": (
            user_factory("w3a-b-institution@example.test", account_type="institution", full_name="Institution de test"),
            icons.AUDIENCE["institution"],
        ),
        "university": (
            user_factory("w3a-b-university@example.test", role=roles.UNIVERSITY, full_name="Université de test"),
            icons.AUDIENCE["university"],
        ),
        "staff": (
            user_factory("w3a-b-staff@example.test", role=roles.STAFF, is_staff=True, full_name="Équipe de test"),
            icons.ACTOR["project_team"],
        ),
    }
    shots = os.environ.get("W3A_SCREENSHOT_DIR")
    seen = {}
    for who, (user, glyph) in accounts.items():
        context = _context(browser, live_server, user, 1366, 657)
        page = context.new_page()
        _at_rest(page, live_server, DASHBOARD.format(lang=lang))
        rail = page.evaluate(RAIL_JS)
        foot = page.evaluate(WHO_JS)
        assert foot["glyph"] == f"icon-{glyph}", (who, foot)
        assert foot["role"] and foot["name"], (who, foot)
        assert rail["state"] == "open" and rail["footBottom"] <= rail["vh"] + 0.5 and rail["overflow"] <= 0, (who, rail)
        assert 0 <= foot["top"] and foot["bottom"] <= rail["vh"] + 0.5, "who the account is stays in view"
        if who != "staff":
            assert rail["count"] == 10 and rail["clipped"] == 0, f"{who}: the ten, whole at 657 px"
        if foot["roleClipped"] or foot["nameClipped"]:
            assert foot["role"] in foot["label"] and foot["name"] in foot["label"], (
                f"{who}: what the rail had to cut is said whole by the word beside the control: {foot}"
            )
            page.focus("nav.rail[data-rail] .rail__who")
            page.wait_for_function("() => document.querySelector('.tooltip:popover-open')")
            word = page.evaluate(
                """() => { const t = document.querySelector('.tooltip:popover-open'); const r = t.getBoundingClientRect();
                  const rail = document.querySelector('nav.rail[data-rail]').getBoundingClientRect();
                  return {text: t.textContent, fits: t.scrollWidth <= t.clientWidth + 1, top: r.top, bottom: r.bottom,
                    beyond: document.documentElement.dir === 'rtl' ? r.right <= rail.left : r.left >= rail.right,
                    inside: r.left >= 0 && r.right <= innerWidth, vh: innerHeight}; }"""
            )
            assert foot["role"] in word["text"] and word["fits"] and word["beyond"] and word["inside"], word
            assert 0 <= word["top"] and word["bottom"] <= word["vh"], word
        if shots:
            Path(shots).mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(Path(shots) / f"audience-{who}-{lang}-1366x657.png"))
        seen[who] = (foot["glyph"], foot["role"])
        context.close()
    assert len(set(seen.values())) == 3, f"three accounts, three glyphs and three words: {seen}"


#: The controls of the rail's foot: their boxes, whether a word is squeezed, which pairs lie over one another.
FOOT_JS = """() => { const rail = document.querySelector('nav.rail[data-rail]');
  const vis = (el) => el.checkVisibility({visibilityProperty: true}) && el.getBoundingClientRect().width > 1;
  const controls = [...rail.querySelectorAll('[data-rail-foot] a[href], [data-rail-foot] button, [data-rail-foot] summary')].filter(vis);
  const boxes = controls.map((el) => { const r = el.getBoundingClientRect();
    return {name: (el.textContent || '').trim().replace(/\\s+/g, ' '), left: r.left, right: r.right, top: r.top, bottom: r.bottom,
            squeezed: el.scrollWidth > el.clientWidth + 1 && !el.matches('.rail__who')}; });
  const over = [];
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) { const a = boxes[i], b = boxes[j];
    if (a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5) over.push(a.name + ' x ' + b.name); }
  const box = rail.getBoundingClientRect(); const list = rail.querySelector('[data-rail-scroll]');
  const tools = [...rail.querySelectorAll('.rail__tools > *')].filter(vis).map((el) => Math.round(el.getBoundingClientRect().top));
  return {boxes, over, rows: [...new Set(tools)].length, vh: innerHeight,
    outside: boxes.filter((b) => b.left < box.left - 0.5 || b.right > box.right + 0.5).map((b) => b.name),
    footBottom: rail.querySelector('[data-rail-foot]').getBoundingClientRect().bottom,
    fits: list.scrollHeight <= list.clientHeight, overflow: document.documentElement.scrollWidth - innerWidth}; }"""

#: WCAG 1.4.12: the four spacings a person may set for themselves.
TEXT_SPACING = (
    "* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } "
    "p { margin-block-end: 2em !important; }"
)


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_the_foot_s_last_row_holds_in_the_four_languages_and_wraps_rather_than_overlap(
    browser, live_server, seeded, person_user, lang
):
    """Measured on the lane: French and Arabic fitted with 0 px to spare and Italian was 8 px over — the chevron of
    «Italiano» lay on «Sito pubblico». One row in the four languages; under the user's own spacing the last word
    goes under the row, never over its neighbour, and the foot stays in view."""
    context = _context(browser, live_server, person_user, 1366, 657, bypass_csp=True)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    foot = page.evaluate(FOOT_JS)
    assert len(foot["boxes"]) == 5 and foot["rows"] == 1, (lang, foot["rows"], [b["name"] for b in foot["boxes"]])
    assert not foot["over"] and not foot["outside"], (lang, foot["over"], foot["outside"])
    assert not [b["name"] for b in foot["boxes"] if b["squeezed"]], (lang, "a word of the foot is squeezed")
    assert foot["fits"] and foot["footBottom"] <= foot["vh"] + 0.5, f"{lang}: the ten and the foot, whole at 657 px"
    page.add_style_tag(content=TEXT_SPACING)
    page.wait_for_timeout(200)
    spaced = page.evaluate(FOOT_JS)
    assert not spaced["over"] and not spaced["outside"], (lang, spaced["over"], spaced["outside"])
    assert spaced["footBottom"] <= spaced["vh"] + 0.5 and spaced["overflow"] <= 0, (lang, spaced["footBottom"])
    assert not [b["name"] for b in spaced["boxes"] if b["squeezed"]], (lang, "a word is cut instead of wrapping")
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_at_320_px_a_long_account_name_gives_way_to_the_title_never_to_the_viewport(
    browser, live_server, seeded, user_factory, lang
):
    """400 % of a 1280 px window (WCAG 1.4.10): an e-mail address used as a name ran 8 px past the edge."""
    user = user_factory("w3a-b-long-name-of-an-account@example.test", role=roles.PERSON)
    context = _context(browser, live_server, user, 320, 640)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    bar = page.evaluate(
        """() => { const bar = document.querySelector('.console-bar'); const out = [];
          for (const el of bar.querySelectorAll('a[href], button, summary')) { if (!el.checkVisibility()) continue;
            const r = el.getBoundingClientRect(); if (r.left < -0.5 || r.right > innerWidth + 0.5) out.push(el.className); }
          return {overflow: document.documentElement.scrollWidth - innerWidth, out,
                  name: getComputedStyle(bar.querySelector('.account-menu__name')).textOverflow}; }"""
    )
    assert bar["overflow"] <= 0 and not bar["out"], bar
    assert bar["name"] == "ellipsis"
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_identity_panel_is_drawn_in_its_section_for_the_account_somebody_has_asked(
    browser, live_server, seeded, person_user, monkeypatch, lang
):
    """«Communications d’identité»: the last page of «Échanges», with the registry's consent glyph, lit on its own
    page; an eleventh row scrolls under the pinned foot at 657 px and is reached."""
    from selection import services as selection_services

    monkeypatch.setattr(selection_services, "has_disclosures", lambda user: user.pk == person_user.pk)
    context = _context(browser, live_server, person_user, 1366, 657)
    page = context.new_page()
    _at_rest(page, live_server, reverse("selection:disclosures").replace("/fr/", f"/{lang}/", 1))
    rail = page.evaluate(RAIL_JS)
    assert rail["count"] == 11 and rail["footBottom"] <= rail["vh"] + 0.5 and rail["overflow"] <= 0, rail
    row = page.evaluate(
        """() => { const rail = document.querySelector('nav.rail[data-rail]');
          const item = rail.querySelector('[data-rail-item][data-key="disclosures"]');
          const group = item.closest('.rail__group'); const view = rail.querySelector('[data-rail-scroll]').getBoundingClientRect();
          const r = item.getBoundingClientRect();
          return {glyph: item.querySelector('use').getAttribute('href').split('#')[1], current: item.getAttribute('aria-current'),
            marked: rail.querySelectorAll('[data-rail-item][aria-current="page"]').length,
            drawer: document.querySelectorAll('nav.rail--drawer [data-rail-item][aria-current="page"]').length,
            siblings: [...group.querySelectorAll('[data-rail-item]')].map((a) => a.dataset.key),
            inView: r.top >= view.top - 0.5 && r.bottom <= view.bottom + 0.5,
            disc: getComputedStyle(item.querySelector('.rail__disc')).backgroundColor}; }"""
    )
    assert row["glyph"] == f"icon-{icons.NAV['disclosures']}" and row["siblings"] == [
        "messages",
        "helpdesk",
        "disclosures",
    ]
    assert (row["current"], row["marked"], row["drawer"]) == ("page", 1, 1), "lit on its own page, once per copy"
    assert row["disc"] == "rgb(255, 255, 255)" and row["inView"], (
        "the current page is kept in view in a rail that scrolls"
    )
    shots = os.environ.get("W3A_SCREENSHOT_DIR")
    if shots:
        Path(shots).mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(Path(shots) / f"identity-panel-{lang}-1366x657.png"))
    context.close()


def test_forced_colours_keep_the_edges_and_the_current_page(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user, 1440, 900, forced_colors="active")
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    assert page.evaluate("matchMedia('(forced-colors: active)').matches")
    probe = """() => { const rail = document.querySelector('nav.rail[data-rail]'); const item = rail.querySelector('[aria-current="page"]');
          const s = getComputedStyle(item); const d = getComputedStyle(item.querySelector('.rail__disc'));
          return {outline: s.outlineStyle + ' ' + s.outlineWidth, edge: getComputedStyle(rail).borderInlineEndWidth,
                  word: getComputedStyle(item.querySelector('.rail__label')).textDecorationLine,
                  foot: getComputedStyle(rail.querySelector('.rail__foot')).borderBlockStartWidth, disc: d.backgroundColor, canvas: getComputedStyle(rail).backgroundColor}; }"""
    forced = page.evaluate(probe)
    assert forced["edge"] == "1px" and forced["foot"] == "1px"
    assert forced["disc"] != forced["canvas"], "the current page keeps its disc, in the system's highlight"
    # its own marker — the lit disc and the word underlined —, never the focus ring's outline at rest: the focus on the
    # current page must still add something (WCAG 2.4.7; W3-D's O2, W4-B)
    assert forced["outline"].startswith("none") and forced["word"] == "underline", forced
    page.keyboard.press("Tab")  # the keyboard's modality
    page.evaluate("document.querySelector('nav.rail[data-rail] [aria-current=\"page\"]').focus()")
    assert page.evaluate(probe)["outline"] == "solid 2px", "the focus draws its ring on the current page"
    context.close()


# ---------------------------------------------------------------------------------------------- the review's fixes
#
# The family's one review (docs/design-v5/QA/v54/w3-a/REVIEW.md) and its accessibility and performance check
# (A11Y_PERF.md), measured; the static halves are in tests/frontend/test_console_shell_w3_a.py.

#: The rail's night (`--rail-bg`: notte-900), as a screenshot draws it.
NIGHT = (11, 26, 51)

#: The list's scroller: the spot at its end, in its padding beside the rows (no row and no word there).
LIST_END_JS = """() => { const s = document.querySelector('nav.rail[data-rail] [data-rail-scroll]');
  const r = s.getBoundingClientRect(); const rtl = document.documentElement.dir === 'rtl';
  return {x: Math.floor(rtl ? r.left + 3 : r.right - 4), y: Math.floor(r.bottom - 3), over: s.scrollHeight - s.clientHeight}; }"""


def _list_end_colour(page):
    """The colour at the end of the rail's list: the rail's night, or the band of its scroll edge."""
    from io import BytesIO

    from PIL import Image

    spot = page.evaluate(LIST_END_JS)
    png = page.screenshot(clip={"x": spot["x"], "y": spot["y"], "width": 1, "height": 1})
    return Image.open(BytesIO(png)).convert("RGB").getpixel((0, 0)), spot["over"]


@pytest.mark.parametrize("stored", ["open", "closed"])
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_list_that_goes_on_under_the_foot_says_so_at_its_end_and_nowhere_else(
    browser, live_server, seeded, superuser, person_user, stored, lang
):
    """Review m1: the last row of a rail that scrolls was cut by the foot through its glyph and its word, and nothing
    said that more followed. A band of the night's sheet stands at the list's end while something is under it."""
    context = _context(browser, live_server, superuser, 1366, 657, stored=stored)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    colour, over = _list_end_colour(page)
    assert over > 0 and sum(colour) > sum(NIGHT) + 30, (stored, lang, colour, over, "more follows: the band")
    page.evaluate(
        "() => { const s = document.querySelector('nav.rail[data-rail] [data-rail-scroll]'); s.scrollTop = s.scrollHeight; }"
    )
    page.wait_for_timeout(100)
    colour, _over = _list_end_colour(page)
    assert colour == NIGHT, (stored, lang, colour, "at the list's end the rail's own night covers the band")
    context.close()
    whole = _context(browser, live_server, person_user, 1440, 900, stored=stored)
    page = whole.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang=lang))
    colour, over = _list_end_colour(page)
    assert over <= 0 and colour == NIGHT, (stored, lang, colour, over, "a list that does not scroll draws no edge")
    whole.close()


def test_the_mark_takes_a_role_account_to_its_register_and_a_person_to_the_dashboard(
    browser, live_server, seeded, user_factory, person_user
):
    """Review M1: the mark took an operator to a person's dashboard, whose one act is an applicant's questionnaire."""
    operator = user_factory("w3a-mark@example.test", role=roles.OPERATOR, full_name="Opératrice de test")
    current_js = (
        "() => [...document.querySelectorAll('nav.rail[data-rail] [data-rail-item][aria-current=\"page\"]')]"
        ".map((a) => a.dataset.key)"
    )
    for user, landing, key in (
        (operator, reverse("helpdesk:dispatch"), "helpdesk-dispatch"),
        (person_user, reverse("portal:dashboard"), "dashboard"),
    ):
        context = _context(browser, live_server, user, 1366, 657)
        page = context.new_page()
        _at_rest(page, live_server, REQUESTS.format(lang="fr"))
        page.click("nav.rail[data-rail] .rail__brand")
        page.wait_for_url(live_server.url + landing)
        assert page.evaluate(current_js) == [key], key
        context.close()


def test_the_footer_s_legal_pages_are_targets_and_a_skip_link_s_ring_stays_inside_its_box(
    browser, live_server, seeded, person_user
):
    """The accessibility check's M1, m1 and m2: the console footer drew its three legal pages 20 px tall — the only
    targets under SP-8's 24 px floor on a console page; where the rail is compact the skip link's night ring stood
    on the paper; and under a finger the footer's pages and the account menu's rows are 44 px."""
    links_js = (
        "() => [...document.querySelectorAll('.console__footer a')].map((a) => { const r = a.getBoundingClientRect();"
        " return [a.textContent.trim(), r.width, r.height]; })"
    )
    desk = _context(browser, live_server, person_user, 1100, 800)
    page = desk.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    links = page.evaluate(links_js)
    assert len(links) == 3 and min(height for _name, _width, height in links) >= 24, links
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    ring = page.evaluate(
        """() => { const a = document.activeElement; const s = getComputedStyle(a);
          return {cls: String(a.className), offset: parseFloat(s.outlineOffset), width: parseFloat(s.outlineWidth),
                  rail: document.body.dataset.rail}; }"""
    )
    assert ring["rail"] == "closed" and "skip-link--rail" in ring["cls"], ring
    assert ring["offset"] <= -ring["width"], ("the ring is drawn inside the navy box", ring)
    desk.close()
    phone = _context(browser, live_server, person_user, 390, 844, has_touch=True, is_mobile=True)
    page = phone.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="ar"))
    links = page.evaluate(links_js)
    assert len(links) == 3 and all(width >= 44 and height >= 44 for _name, width, height in links), links
    page.tap(".console-bar .account-menu__summary")
    # the account's popover (the overlay system's, W2-A): its rows, 44 px under a finger
    rows = page.evaluate(
        "() => [...document.querySelectorAll('#console-account .overlay__item')]"
        ".map((a) => a.getBoundingClientRect().height)"
    )
    assert rows and min(rows) >= 44, rows
    phone.close()


@pytest.mark.parametrize("size", [(1366, 657), (360, 800)], ids=lambda s: f"{s[0]}x{s[1]}")
def test_in_arabic_the_name_above_the_dashboard_s_title_stands_on_the_reading_edge(
    browser, live_server, seeded, user_factory, size
):
    """Review m2: a French name above an Arabic title hugged the left of a box anchored on the right — 130 px off
    the title's edge at 1366, mid-line on a phone."""
    from cases import services as case_services
    from cases.models import CasePurpose

    person = user_factory("w3a-ctx@example.test", role=roles.PERSON, full_name="Personne de test")
    case_services.open_case(person, purpose=CasePurpose.WORK)
    phone = {"has_touch": True, "is_mobile": True} if size[0] < 1024 else {}
    context = _context(browser, live_server, person, size[0], size[1], **phone)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="ar"))
    edges = page.evaluate(
        """() => { const end = (el) => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect().right; };
          return {name: end(document.querySelector('.ctx__greeting')), title: end(document.querySelector('.ctx__title')),
                  overflow: document.documentElement.scrollWidth - innerWidth}; }"""
    )
    assert abs(edges["name"] - edges["title"]) <= 1 and edges["overflow"] <= 0, edges
    context.close()


def test_in_the_band_the_account_s_name_goes_on_a_second_line_rather_than_lose_its_end(
    browser, live_server, seeded, user_factory
):
    """The accessibility check's m4: under a person's own text spacing (WCAG 1.4.12) the name beside the account's
    glyph lost its end to an ellipsis. (Below 48rem the glyph stands alone: the name is the trigger's word for a
    reader, by design.)"""
    user = user_factory("w3a-band-long-name@example.test", role=roles.PERSON)
    context = _context(browser, live_server, user, 820, 1180, has_touch=True, is_mobile=True, bypass_csp=True)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    page.add_style_tag(content=TEXT_SPACING)
    page.wait_for_timeout(200)
    name = page.evaluate(
        """() => { const n = document.querySelector('.console-bar .account-menu__name');
          return {cut: n.scrollWidth > n.clientWidth + 1 || n.scrollHeight > n.clientHeight + 1,
                  width: n.getBoundingClientRect().width, overflow: document.documentElement.scrollWidth - innerWidth}; }"""
    )
    assert not name["cut"] and name["width"] > 0 and name["overflow"] <= 0, name
    context.close()
