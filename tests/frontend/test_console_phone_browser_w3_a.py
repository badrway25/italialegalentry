"""
The console shell below 64rem, in the browser — «the rail laid flat» — design V5, family W3-A, step 2
(docs/design-v5/V5_4_EXECUTION_PLAN.md §1.18 D06, §3.5 item 3; DL54-66 … DL54-71;
docs/design-v5/QA/v54/w3-a/NOTES.md). What a static test cannot see:

* the bottom bar holds four entries at most and «Menu» for every role, in the four languages, from 320 to 412 px:
  the words are the live labels, whole, on one line or two, with air between two entries, each seat 44 px to the
  finger; the chrome that stays on screen is 120 px at most;
* «il lume» on the bar is the rail's lit disc; «Menu» is reached in three keys and opens a modal drawer that holds
  the whole rail and its foot — the overlay system's (W2-A: the trap with aria-modal, the one scrim, «Slide»); Esc puts
  the language's list away before it puts the drawer away;
* the band from 48rem draws the rail's own row; a phone on its side lets the top bar leave with the page;
* Arabic mirrors the chrome and never the mark; a title in another language is cut at its own end;
* reduced motion, forced colours, the device's safe areas, a page's action bar, and «Menu» without script.

Chromium on the seeded site; a session minted with ``Client.force_login`` — nothing typed, no password used.
Emulated, and said so: no real iOS or Android device was used.
"""

from __future__ import annotations

import os

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import translation

from accounts import roles
from portal import services

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DASHBOARD = "/{lang}/espace-reserve/"
REQUESTS = "/{lang}/espace-reserve/mes-demandes/"
SITUATION = "/{lang}/espace-reserve/ma-situation/"

#: The phone's chrome as it is drawn: the top bar, the bottom bar and each of its entries.
CHROME_JS = """() => {
  const r1 = (n) => Math.round(n * 10) / 10;
  const shown = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const box = (el) => { const r = el.getBoundingClientRect(); return {x: r1(r.left), y: r1(r.top), w: r1(r.width), h: r1(r.height), r: r1(r.right), b: r1(r.bottom)}; };
  const bar = document.querySelector('.console-bar');
  const tile = bar.querySelector('.console-bar__tile'); const title = bar.querySelector('.console-bar__title');
  const account = bar.querySelector('.account-menu__summary'); const name = bar.querySelector('.account-menu__name');
  const after = getComputedStyle(tile, '::after');
  const bottom = document.querySelector('nav.console-bottom');
  const items = [...bottom.querySelectorAll('.console-bottom__item')].filter(shown);
  const rail = document.querySelector('nav.rail[data-rail]');
  return {vw: document.documentElement.clientWidth, vh: innerHeight, dir: document.documentElement.dir,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    rail: shown(rail),
    bar: {box: box(bar), position: getComputedStyle(bar).position, bg: getComputedStyle(bar).backgroundColor,
      edge: getComputedStyle(bar).borderBottomWidth, glass: getComputedStyle(bar).backdropFilter,
      tile: shown(tile) ? {box: box(tile), bg: getComputedStyle(tile).backgroundColor,
        hit: [tile.getBoundingClientRect().width - 2 * parseFloat(after.left), tile.getBoundingClientRect().height - 2 * parseFloat(after.top)],
        mark: getComputedStyle(tile.firstElementChild).transform, markDir: getComputedStyle(tile.firstElementChild).direction} : null,
      title: shown(title) ? {text: title.textContent.trim(), box: box(title), color: getComputedStyle(title).color,
        clipped: title.scrollWidth > title.clientWidth + 1} : null,
      account: shown(account) ? {box: box(account), name: name.getBoundingClientRect().width} : null,
      crumbs: shown(bar.querySelector('.console-bar__crumbs'))},
    bottom: shown(bottom) ? {box: box(bottom), bg: getComputedStyle(bottom).backgroundColor, position: getComputedStyle(bottom).position,
      edge: getComputedStyle(bottom).borderTopWidth,
      items: items.map((i) => { const label = i.querySelector('.console-bottom__label'); const disc = i.querySelector('.console-bottom__disc');
        const runs = [...label.querySelectorAll('.console-bottom__line')];
        const range = document.createRange(); range.selectNodeContents(label);
        const rects = [...range.getClientRects()].filter((q) => q.width > 0.5);
        const s = getComputedStyle(i); const d = getComputedStyle(disc);
        return {key: i.dataset.key || '', menu: i.hasAttribute('data-console-menu'), text: label.textContent.trim().replace(/\\s+/g, ' '),
          current: i.getAttribute('aria-current') === 'page', box: box(i), disc: box(disc), label: box(label),
          lines: runs.length ? new Set(runs.map((q) => Math.round(q.getBoundingClientRect().top))).size : 1,
          ink: [r1(Math.min(...rects.map((q) => q.left))), r1(Math.max(...rects.map((q) => q.right)))],
          size: parseFloat(s.fontSize), color: s.color, weight: s.fontWeight, outline: s.outlineStyle + ' ' + s.outlineWidth,
          discBg: d.backgroundColor, glyph: d.color, radius: d.borderTopLeftRadius,
          glyphSize: disc.querySelector('svg').getBoundingClientRect().width}; })} : null};
}"""

#: The drawer once it is open: its box, its rows, every control a finger can press, where the focus is.
DRAWER_JS = """() => {
  const d = document.querySelector('dialog.console-drawer'); const r = d.getBoundingClientRect();
  const shown = (el) => { const b = el.getBoundingClientRect(); return b.width > 1 && b.height > 1 && el.checkVisibility({visibilityProperty: true}); };
  const controls = [...d.querySelectorAll('a[href], button, summary')].filter(shown).map((el) => { const b = el.getBoundingClientRect();
    return {name: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40), cls: String(el.className).split(' ')[0], w: Math.round(b.width), h: Math.round(b.height),
      out: b.left < r.left - 0.5 || b.right > r.right + 0.5}; });
  const list = d.querySelector('.rail--drawer .rail__scroll'); const foot = d.querySelector('.rail__foot').getBoundingClientRect();
  const word = d.querySelector('.rail__tool-word').getBoundingClientRect();
  const active = document.activeElement;
  return {open: d.open, modal: d.matches(':modal') || d.getAttribute('aria-modal') === 'true', box: {x: r.left, r: r.right, w: r.width, h: r.height}, vw: document.documentElement.clientWidth, vh: innerHeight,
    bg: getComputedStyle(d).backgroundColor, edge: getComputedStyle(d).borderInlineEndWidth,
    keys: [...d.querySelectorAll('[data-rail-item]')].map((a) => a.dataset.key),
    current: [...d.querySelectorAll('[data-rail-item][aria-current="page"]')].map((a) => a.dataset.key),
    controls, small: controls.filter((c) => c.w < 44 || c.h < 44).map((c) => `${c.name} ${c.w}x${c.h}`),
    outside: controls.filter((c) => c.out).map((c) => c.name),
    focus: active ? {key: active.dataset.key || '', id: active.id, cls: String(active.className).split(' ')[0], inside: d.contains(active)} : null,
    scrolls: list.scrollHeight > list.clientHeight + 1, footBottom: foot.bottom, footTop: foot.top, signOutWord: word.width,
    lang: d.querySelector('.rail__lang').open, toggle: d.querySelectorAll('[data-rail-toggle]').length,
    expanded: document.querySelector('#console-menu').getAttribute('aria-expanded'), hash: location.hash,
    motion: d.getAnimations().filter((a) => a.playState === 'running').map((a) => a.animationName || a.transitionProperty)};
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


def _context(browser, live_server, user, width=390, height=844, touch=True, **options):
    """A signed-in context at a phone's size; ``touch`` makes it a phone (a coarse pointer, no hover)."""
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
    return context


def _at_rest(page, live_server, path):
    """The page loaded twice: the first console page of a session plays the entrance release, the second is at rest."""
    page.goto(live_server.url + path, wait_until="networkidle")
    page.goto(live_server.url + path, wait_until="networkidle")
    page.wait_for_function("() => document.body.classList.contains('is-ready')")


def _drawer_at_rest(page):
    """The drawer open and arrived: it slides in from its edge for 320 ms, and a box measured on the way is not its place."""
    page.wait_for_selector("dialog.console-drawer[open]")
    page.wait_for_function(
        "() => document.querySelector('dialog.console-drawer').getAnimations().every((a) => a.playState !== 'running')"
    )


def _drawer_put_away(page):
    """The drawer closed and the page told: the overlay system folds «Menu»'s ``aria-expanded`` and returns the focus
    as the ``open`` attribute leaves; the drawer itself leaves on its 200 ms way out."""
    page.wait_for_selector("dialog.console-drawer:not([open])", state="attached")
    page.wait_for_function("() => document.querySelector('#console-menu').getAttribute('aria-expanded') === 'false'")


def _luminance(colour: str) -> float:
    channels = [float(part) / 255 for part in colour[colour.index("(") + 1 : colour.index(")")].split(",")[:3]]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a: str, b: str) -> float:
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


@pytest.fixture
def accounts(user_factory, superuser):
    """One account per kind of bottom bar: a person's four, a second space, a role's register, everything."""
    return {
        "person": user_factory("w3a-p-person@example.test", role=roles.PERSON, full_name="Personne de test"),
        "company": user_factory("w3a-p-company@example.test", role=roles.COMPANY, full_name="Entreprise de test"),
        "professional": user_factory("w3a-p-pro@example.test", role=roles.PROFESSIONAL, full_name="Professionnelle"),
        "operator": user_factory("w3a-p-operator@example.test", role=roles.OPERATOR, full_name="Opératrice de test"),
        "actor": user_factory("w3a-p-actor@example.test", role=roles.AUTHORISED_ACTOR, full_name="Acteur de test"),
        "superuser": superuser,
    }


# ---------------------------------------------------------------------------------------------- the bottom bar


def _check_bar(chrome, expected, lang, who, width, height):
    """The gate's facts on one drawing of the chrome."""
    where = (who, lang, width)
    assert chrome["overflow"] <= 0, (where, chrome["overflow"])
    bar, bottom = chrome["bar"], chrome["bottom"]
    assert bottom and not chrome["rail"], (where, "below 64rem the rail is not drawn and the bottom bar is")
    items = bottom["items"]
    entries, menu = [item for item in items if not item["menu"]], [item for item in items if item["menu"]]
    assert len(menu) == 1 and len(entries) <= 4, (where, [item["text"] for item in items])
    # the words are the rail's own, whole, in the rail's order — less the entry that leaves a row too short
    register = any(entry["yields"] == services.YIELDS_PHONE for entry in expected)
    kept = [
        entry
        for entry in expected
        if not (entry["yields"] == services.YIELDS_NARROW and width < 360)
        and not (entry["yields"] == services.YIELDS_PHONE and width < 480)
    ]
    assert [item["key"] for item in entries] == [entry["key"] for entry in kept], where
    assert [item["text"] for item in entries] == [str(entry["label"]) for entry in kept], where
    assert len(entries) <= (3 if width < 360 or (register and width < 480) else 4), where
    # «Menu» closes the row at the reading end
    ordered = sorted(items, key=lambda item: item["box"]["x"], reverse=lang == "ar")
    assert ordered[-1]["menu"], (where, "«Menu» stands at the inline end")
    assert [item["key"] for item in ordered[:-1]] == [entry["key"] for entry in kept], (where, "the rail's order")
    for item in items:
        assert item["lines"] <= 2, (where, item["text"], item["lines"])
        assert item["box"]["w"] >= 44 and item["box"]["h"] >= 44, (where, item["text"], item["box"])
        assert item["ink"][0] >= item["box"]["x"] - 0.5 and item["ink"][1] <= item["box"]["r"] + 0.5, (
            where,
            f"a word stands outside its seat: {item['text']}",
        )
        assert item["ink"][0] >= 0 and item["ink"][1] <= chrome["vw"], (where, item["text"])
        assert item["size"] >= (14 if lang == "ar" else 12), (where, item["size"])
        assert item["glyphSize"] == 20 and item["disc"]["w"] == 32, (where, item["text"])
        assert _contrast(item["color"], bottom["bg"]) >= 4.5, (where, item["text"], item["color"])
    for one, two in zip(ordered, ordered[1:]):
        gap = (one["ink"][0] - two["ink"][1]) if lang == "ar" else (two["ink"][0] - one["ink"][1])
        assert gap >= 6, (where, f"«{one['text']}» and «{two['text']}» stand {gap:.1f} px apart")
    assert sum(1 for item in items if item["current"]) <= 1, where
    # the chrome that stays on screen
    sticky = bar["position"] == "sticky"
    assert sticky is (width >= 360 and height >= 480), (where, bar["position"])
    stays = (bar["box"]["h"] if sticky else 0) + bottom["box"]["h"]
    assert stays <= 120, (where, f"{stays} px of chrome stay on screen")
    assert bar["box"]["h"] == 48 and bottom["box"]["b"] == chrome["vh"] and bottom["position"] == "fixed", where
    return stays


@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_the_bar_holds_whole_words_on_two_lines_at_most_for_every_role_and_the_chrome_120_px(
    browser, live_server, seeded, accounts, lang
):
    sizes = [(360, 800), (390, 844), (412, 915)]
    if lang in ("fr", "ar"):
        sizes = [(320, 568), *sizes, (375, 667)]
    tallest = 0
    for who, user in accounts.items():
        with translation.override(lang):
            expected = [
                {**entry, "label": str(entry["label"])} for entry in services.shell_navigation(user) if entry["bottom"]
            ]
        assert len(expected) <= 4
        context = _context(browser, live_server, user)
        page = context.new_page()
        page.goto(live_server.url + REQUESTS.format(lang=lang), wait_until="networkidle")  # the entrance release
        for width, height in sizes:
            page.set_viewport_size({"width": width, "height": height})
            page.goto(live_server.url + REQUESTS.format(lang=lang), wait_until="networkidle")
            chrome = page.evaluate(CHROME_JS)
            tallest = max(tallest, _check_bar(chrome, expected, lang, who, width, height))
        context.close()
    assert tallest >= 96, "the measure is of a drawn chrome"


def test_the_company_space_draws_its_own_bar_and_a_reader_s_page_is_on_it(browser, live_server, seeded, accounts):
    for who, path, current in (
        ("company", reverse("companies:dashboard"), "dashboard"),
        ("superuser", reverse("companies:analysis"), "analysis"),
    ):
        user = accounts[who]
        expected = [
            {**entry, "label": str(entry["label"])}
            for entry in services.shell_navigation(user, services.SPACE_COMPANY)
            if entry["bottom"]
        ]
        context = _context(browser, live_server, user)
        page = context.new_page()
        _at_rest(page, live_server, path)
        chrome = page.evaluate(CHROME_JS)
        _check_bar(chrome, expected, "fr", who, 390, 844)
        lit = [item["key"] for item in chrome["bottom"]["items"] if item["current"]]
        assert lit == [current], (who, "the page one is on is on the bar, and lit")
        context.close()


def test_il_lume_on_the_bar_is_the_rail_s_lit_disc(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    chrome = page.evaluate(CHROME_JS)
    items = chrome["bottom"]["items"]
    current = [item for item in items if item["current"]]
    assert [item["key"] for item in current] == ["dashboard"]
    lit, others = current[0], [item for item in items if not item["current"]]
    assert lit["discBg"] == "rgb(255, 255, 255)" and lit["glyph"] == "rgb(21, 34, 42)", (
        "the lit paper disc, the glyph in ink"
    )
    assert float(lit["radius"].rstrip("px")) >= 16, "a disc"
    assert {item["discBg"] for item in others} == {"rgba(0, 0, 0, 0)"}, "one lit disc on the bar"
    assert lit["weight"] == others[0]["weight"] == "500", "the weight stays: a word never changes lines"
    assert _luminance(lit["color"]) > _luminance(others[0]["color"]), "the current word in the night's first ink"
    assert chrome["bottom"]["bg"] == chrome["bar"]["bg"], "the two bars are one night"
    assert _luminance(chrome["bar"]["bg"]) < 0.02 and chrome["bar"]["glass"] == "none", "night, without glass"
    edge = page.evaluate(
        """() => { const i = document.querySelector('.console-bottom__item[aria-current="page"]');
          const b = getComputedStyle(i, '::before'); return {bg: b.backgroundColor, w: b.width}; }"""
    )
    assert edge["bg"] == "rgba(0, 0, 0, 0)", "no bar at the edge: the entry's ::before is air, not an indicator"
    # the same disc in the rail's copy the drawer holds
    page.click("#console-menu")
    _drawer_at_rest(page)
    disc = page.evaluate(
        """() => getComputedStyle(document.querySelector('dialog.console-drawer [data-rail-item][aria-current="page"] .rail__disc')).backgroundColor"""
    )
    assert disc == lit["discBg"]
    context.close()


# ---------------------------------------------------------------------------------------------- «Menu» and the drawer


def test_menu_is_reached_in_three_keys_and_opens_a_drawer_that_holds_the_whole_rail(
    browser, live_server, seeded, person_user
):
    focused = "() => ({text: document.activeElement.textContent.trim(), id: document.activeElement.id, tag: document.activeElement.tagName, role: document.activeElement.getAttribute('role')})"
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    assert page.locator("[data-console-menu]").count() == 1, "one «Menu»: no «≡» in the top bar"
    assert page.evaluate("document.querySelector('#console-menu').getAttribute('aria-expanded')") == "false"
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Aller au contenu principal"
    page.keyboard.press("Tab")
    assert page.evaluate(focused)["text"] == "Menu"
    page.keyboard.press("Enter")
    landed = page.evaluate(focused)
    assert (landed["id"], landed["tag"], landed["role"]) == ("console-menu", "A", "button"), (
        f"three keys to «Menu» (the audit's S-2): {landed}"
    )
    address = page.evaluate("location.hash")  # the skip link's own target: «Menu» adds nothing to it
    page.keyboard.press("Enter")
    _drawer_at_rest(page)
    drawer = page.evaluate(DRAWER_JS)
    assert drawer["open"] and drawer["modal"] and drawer["expanded"] == "true" and drawer["hash"] == address, drawer
    assert drawer["box"]["x"] == 0 and drawer["box"]["w"] == 320 and drawer["box"]["h"] == drawer["vh"], drawer["box"]
    assert drawer["keys"] == [entry["key"] for entry in services.shell_navigation(person_user)], "the whole rail"
    assert drawer["current"] == ["requests"] and drawer["focus"] == {
        "key": "requests",
        "id": "",
        "cls": "rail__item",
        "inside": True,
    }, "the focus goes to the page one is on"
    assert not drawer["small"] and not drawer["outside"], f"a control under 44 px, or outside the drawer: {drawer}"
    names = [control["name"] for control in drawer["controls"]]
    for word in ("Se déconnecter", "Site public", "Français", "Fermer le menu"):
        assert any(word in name for name in names), (word, names)
    assert drawer["signOutWord"] > 40, "sign-out is a row with its word: a finger finds no hover"
    assert drawer["toggle"] == 0, "the rail's own control is not drawn: nothing folds in a drawer"
    locked = "getComputedStyle(document.documentElement).overflowY"
    assert page.evaluate(locked) == "hidden", "the page behind the scrim does not scroll while the drawer is open"
    assert drawer["footBottom"] <= drawer["vh"] + 0.5, "the foot is the drawer's last thing, in view"
    # the language's list goes away first, then the drawer; the focus comes back to «Menu»
    page.click("dialog.console-drawer .rail__lang-summary")
    opened = page.evaluate(DRAWER_JS)
    assert opened["lang"] and opened["open"]
    languages = page.evaluate(
        "() => [...document.querySelectorAll('dialog.console-drawer .rail__lang .lang-seg__link')].map((a) => a.textContent.trim())"
    )
    assert languages == ["Italiano", "Français", "English", "العربية"], "by their own names (D21)"
    page.keyboard.press("Escape")
    after = page.evaluate(DRAWER_JS)
    assert after["open"] and not after["lang"], "Esc puts the list away, not the drawer it stands in"
    page.keyboard.press("Escape")
    _drawer_put_away(page)
    closed = page.evaluate(DRAWER_JS)
    assert closed["focus"]["id"] == "console-menu" and closed["expanded"] == "false" and closed["hash"] == address
    assert page.evaluate(locked) != "hidden", "and scrolls again once it is closed"
    # Space presses it as Enter does; a press on the scrim closes
    page.keyboard.press("Space")
    _drawer_at_rest(page)
    page.mouse.click(370, 400)
    _drawer_put_away(page)
    # and the close control
    page.click("#console-menu")
    _drawer_at_rest(page)
    page.click("[data-console-close]")
    _drawer_put_away(page)
    assert page.evaluate("location.hash") == address, "nothing is added to the address"
    context.close()


@pytest.mark.parametrize("who", ["operator", "superuser"])
def test_a_longer_rail_scrolls_inside_the_drawer_under_its_pinned_foot(browser, live_server, seeded, accounts, who):
    context = _context(browser, live_server, accounts[who], 360, 640)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    page.click("#console-menu")
    _drawer_at_rest(page)
    drawer = page.evaluate(DRAWER_JS)
    assert drawer["scrolls"] and drawer["footBottom"] <= drawer["vh"] + 0.5 and not drawer["small"], drawer
    assert drawer["box"]["w"] == pytest.approx(360 * 0.88, abs=1), "88 % of a narrow screen: the page stays in sight"
    reached = page.evaluate(
        """() => { const s = document.querySelector('dialog.console-drawer .rail__scroll'); s.scrollTop = s.scrollHeight;
          const rows = s.querySelectorAll('[data-rail-item]'); const last = rows[rows.length - 1].getBoundingClientRect();
          return last.bottom <= s.getBoundingClientRect().bottom + 0.5; }"""
    )
    assert reached, "the last page is clear of the foot once the list is scrolled"
    context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_in_the_drawer_a_long_name_goes_on_a_second_line_never_under_an_ellipsis(
    browser, live_server, seeded, user_factory, lang
):
    """The rail shows a name it had to cut whole in the word beside it; a drawer has no such word."""
    user = user_factory("w3a-p-a-very-long-name-of-an-account@example.test", role=roles.PERSON)
    context = _context(browser, live_server, user, 320, 640)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang=lang))
    page.click("#console-menu")
    _drawer_at_rest(page)
    who = page.evaluate(
        """() => { const d = document.querySelector('dialog.console-drawer'); const name = d.querySelector('.rail__who-name');
          const r = name.getBoundingClientRect(); const box = d.getBoundingClientRect();
          return {text: name.textContent.trim(), cut: name.scrollWidth > name.clientWidth + 1, lines: Math.round(r.height / parseFloat(getComputedStyle(name).lineHeight)),
                  inside: r.left >= box.left - 0.5 && r.right <= box.right + 0.5, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
    )
    assert who["text"] == user.email and not who["cut"] and who["lines"] >= 2 and who["inside"], who
    drawer = page.evaluate(DRAWER_JS)
    assert not drawer["small"] and not drawer["outside"] and drawer["footBottom"] <= drawer["vh"] + 0.5, drawer
    context.close()


def test_without_script_menu_is_a_link_that_shows_the_drawer(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user, java_script_enabled=False)
    page = context.new_page()
    page.goto(live_server.url + REQUESTS.format(lang="fr"), wait_until="load")
    drawer = page.locator("dialog.console-drawer")
    assert not drawer.is_visible()
    assert page.locator("#console-menu").get_attribute("role") is None, "without script a link is a link"
    page.locator("#console-menu").click()
    assert page.url.endswith("#console-drawer")
    assert drawer.is_visible(), "the link's target is the drawer, and the stylesheet shows it"
    box = drawer.bounding_box()
    assert box["x"] == 0 and box["width"] == 320 and box["height"] == 844
    assert page.locator("dialog.console-drawer .rail__item[aria-current='page']").count() == 1
    assert page.locator("dialog.console-drawer .rail__signout button").is_visible()
    page.locator("[data-console-close]").click()
    assert page.url.endswith("#main-content") and not drawer.is_visible(), "the close control leads back to the page"
    context.close()


# ---------------------------------------------------------------------------------------------- the top bar


def test_the_top_bar_is_the_rail_s_head_the_mark_the_level_of_the_page_the_account(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    chrome = page.evaluate(CHROME_JS)
    bar = chrome["bar"]
    assert bar["box"]["h"] == 48 and bar["box"]["y"] == 0 and bar["edge"] == "0px" and not bar["crumbs"], bar
    tile, title, account = bar["tile"], bar["title"], bar["account"]
    assert tile["box"]["w"] == tile["box"]["h"] == 32 and tile["box"]["x"] == 16, (
        "the tile on the page's own start edge"
    )
    assert tile["bg"] == "rgb(255, 255, 255)" and tile["hit"] == [44, 44], (
        "the mark on its paper tile, 44 px to the finger"
    )
    assert title["text"] == "Mes demandes" and not title["clipped"] and _contrast(title["color"], bar["bg"]) >= 7
    assert account["box"]["w"] == 44 and account["box"]["h"] == 44 and account["name"] <= 1, (
        "the account is its glyph alone on a phone: its name stays its name for a reader"
    )
    assert account["box"]["r"] == chrome["vw"] - 10, "the account's disc ends on the page's own edge"
    assert page.evaluate("document.querySelector('.console-bar__tile').getAttribute('href')") == "/fr/espace-reserve/"
    # the account's popover opens — on a phone the overlay system's sheet (W2-A) — whole in the screen, below the bar
    page.click(".console-bar .account-menu__summary")
    menu = page.evaluate(
        """() => { const p = document.getElementById('console-account'); const r = p.getBoundingClientRect();
          return {left: r.left, right: r.right, top: r.top, vw: document.documentElement.clientWidth,
                  open: p.matches(':popover-open')}; }"""
    )
    assert menu["open"] and menu["left"] >= 0 and menu["right"] <= menu["vw"] and menu["top"] >= 48, menu
    context.close()


@pytest.mark.parametrize("size", [(844, 390), (320, 568)], ids=["a phone on its side", "320 px"])
def test_where_the_viewport_is_short_or_very_narrow_the_top_bar_leaves_with_the_page(
    browser, live_server, seeded, person_user, size
):
    context = _context(browser, live_server, person_user, *size)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    chrome = page.evaluate(CHROME_JS)
    assert chrome["bar"]["position"] == "static" and chrome["overflow"] <= 0, chrome["bar"]
    page.evaluate("window.scrollTo(0, 300)")
    page.wait_for_timeout(100)
    scrolled = page.evaluate(CHROME_JS)
    assert scrolled["bar"]["box"]["b"] <= 0, "the top bar has left with the page"
    assert scrolled["bottom"]["box"]["b"] == scrolled["vh"], "the bottom bar alone stays"
    if size[1] < 480:
        page.click("#console-menu")
        _drawer_at_rest(page)
        short = page.evaluate(
            """() => { const n = document.querySelector('dialog.console-drawer .rail--drawer'); n.scrollTop = n.scrollHeight;
              const foot = n.querySelector('.rail__foot').getBoundingClientRect(); const out = n.querySelector('.rail__exit').getBoundingClientRect();
              return {scrolls: n.scrollHeight > n.clientHeight + 1, exitBottom: out.bottom, vh: innerHeight, footHeight: foot.height}; }"""
        )
        assert short["scrolls"] and short["exitBottom"] <= short["vh"] + 0.5, (
            "in a short viewport the whole rail scrolls under the drawer's head, the foot at its end"
        )
    context.close()


# ---------------------------------------------------------------------------------------------- the band


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_band_from_48rem_draws_the_rail_s_own_row_and_the_rail_returns_at_64rem(
    browser, live_server, seeded, accounts, lang
):
    for who in ("person", "professional"):
        user = accounts[who]
        context = _context(browser, live_server, user, 768, 1024)
        page = context.new_page()
        page.goto(live_server.url + DASHBOARD.format(lang=lang), wait_until="networkidle")
        for width, height in ((768, 1024), (820, 1180), (1023, 768)):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(live_server.url + DASHBOARD.format(lang=lang), wait_until="networkidle")
            chrome = page.evaluate(CHROME_JS)
            where = (who, lang, width)
            assert chrome["overflow"] <= 0 and not chrome["rail"], where
            bar, bottom = chrome["bar"], chrome["bottom"]
            assert bar["box"]["h"] == 56 and bottom["box"]["h"] == 56 and bar["position"] == "sticky", (
                where,
                bar["box"],
                bottom["box"],
            )
            assert bar["account"]["name"] > 20, (where, "from 48rem the account's name stands beside its glyph")
            items = bottom["items"]
            assert len(items) == 5 and sum(1 for item in items if item["menu"]) == 1, (where, "four entries and «Menu»")
            for item in items:
                beside = (
                    item["disc"]["r"] <= item["label"]["x"] + 0.5
                    if lang == "fr"
                    else item["label"]["r"] <= item["disc"]["x"] + 0.5
                )
                assert beside, (where, item["text"], "the glyph on its disc BESIDE its word")
                assert item["lines"] <= 2 and item["box"]["h"] >= 44 and item["box"]["w"] >= 44, (where, item)
                assert item["ink"][0] >= item["box"]["x"] - 0.5 and item["ink"][1] <= item["box"]["r"] + 0.5, (
                    where,
                    item["text"],
                )
            lit = [item for item in items if item["current"]]
            assert len(lit) == 1 and lit[0]["discBg"] == "rgb(255, 255, 255)", where
        page.set_viewport_size({"width": 1024, "height": 768})
        page.goto(live_server.url + DASHBOARD.format(lang=lang), wait_until="networkidle")
        wide = page.evaluate(CHROME_JS)
        assert wide["rail"] and wide["bottom"] is None and wide["bar"]["crumbs"] and wide["bar"]["tile"] is None, (
            "from 64rem the rail stands at the reading edge and the bar is the level of the page"
        )
        assert _luminance(wide["bar"]["bg"]) > 0.8, "and the bar is glass again"
        context.close()


def test_a_window_widened_past_64rem_puts_the_drawer_away(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user, 900, 800, touch=False)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.click("#console-menu")
    _drawer_at_rest(page)
    page.set_viewport_size({"width": 1280, "height": 800})
    _drawer_put_away(page)
    assert page.evaluate("document.querySelector('#console-menu').getAttribute('aria-expanded')") == "false"
    context.close()


# ---------------------------------------------------------------------------------------------- Arabic


def test_arabic_mirrors_the_chrome_and_never_the_mark(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="ar"))
    chrome = page.evaluate(CHROME_JS)
    assert chrome["dir"] == "rtl" and chrome["overflow"] <= 0
    bar = chrome["bar"]
    assert bar["tile"]["box"]["r"] == chrome["vw"] - 16, "the mark's tile at the reading edge: the right one"
    assert bar["account"]["box"]["x"] == 10 and bar["title"]["box"]["r"] < bar["tile"]["box"]["x"], bar
    assert bar["tile"]["mark"] == "none", "the mark is never mirrored: no transform on it, in any locale"
    mark = page.evaluate(
        "() => { const i = document.querySelector('.console-bar__tile img'); return [i.getAttribute('src').split('/').pop().split('.')[0], getComputedStyle(i).transform]; }"
    )
    assert mark[0].startswith("logo-mark") and mark[1] == "none"
    # the entrance release's seat is left-to-right in every locale (W1-D); the still mark is one file for all
    page.click("#console-menu")
    _drawer_at_rest(page)
    drawer = page.evaluate(DRAWER_JS)
    assert drawer["box"]["r"] == drawer["vw"] and drawer["box"]["x"] == drawer["vw"] - 320, (
        "the drawer at the reading edge"
    )
    assert not drawer["small"] and not drawer["outside"], drawer
    flips = page.evaluate(
        """() => { const d = document.querySelector('dialog.console-drawer');
          const out = d.querySelector('.rail__signout svg'); const steps = d.querySelector('[data-key="pathways"] svg');
          const tile = d.querySelector('.rail__tile img');
          const s = getComputedStyle(d);
          return {signOut: getComputedStyle(out).transform, steps: getComputedStyle(steps).transform, tile: getComputedStyle(tile).transform,
                  travel: parseFloat(s.getPropertyValue('--overlay-edge')) * parseFloat(s.getPropertyValue('--dir'))}; }"""
    )
    assert flips["signOut"] != "none", "a direction mirrors: the way out points the other way"
    assert flips["steps"] == "none" and flips["tile"] == "none", "a meaning does not: the mark and its steps stay"
    # the overlay system's «Slide»: translate(100% × edge × --dir) — +100 %, from the right, the reading edge here
    assert flips["travel"] == 1, "and the drawer comes from its own edge"
    context.close()


def test_a_title_in_another_language_is_cut_at_its_own_end(browser, live_server, seeded, person_user):
    """A French course on an Arabic page: cut by the page's box, the title lost its FIRST words."""
    context = _context(browser, live_server, person_user, 320, 568)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="ar"))
    cut = page.evaluate(
        """() => { const title = document.querySelector('.console-bar__title');
          const run = document.createElement('span'); run.lang = 'fr';
          run.textContent = 'Italien A1 — premiers échanges, niveau débutant complet';
          title.replaceChildren(run);
          const s = getComputedStyle(run); const r = run.getBoundingClientRect(); const bar = document.querySelector('.console-bar__inner').getBoundingClientRect();
          const tile = document.querySelector('.console-bar__tile').getBoundingClientRect(); const account = document.querySelector('.account-menu__summary').getBoundingClientRect();
          return {direction: s.direction, overflow: s.textOverflow, clipped: run.scrollWidth > run.clientWidth + 1, scrollLeft: run.scrollLeft,
                  inside: r.left >= account.right - 0.5 && r.right <= tile.left + 0.5, pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                  barHeight: bar.height}; }"""
    )
    assert cut["clipped"] and cut["direction"] == "ltr" and cut["overflow"] == "ellipsis", cut
    assert cut["scrollLeft"] == 0, "the run shows its first words: the ellipsis stands at its own end"
    assert cut["inside"] and cut["pageOverflow"] <= 0 and cut["barHeight"] == 48, cut
    context.close()


# ---------------------------------------------------------------------------------------------- states


def test_reduced_motion_opens_the_drawer_at_once_and_nothing_of_the_chrome_moves_at_load(
    browser, live_server, seeded, person_user
):
    moving = """() => document.getAnimations().filter((a) => { const t = a.effect && a.effect.target;
      return t && t.closest && t.closest('.console-bar, .console-bottom, .console-drawer') && a.playState === 'running'; })
      .map((a) => a.animationName || a.transitionProperty)"""
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    page.goto(live_server.url + REQUESTS.format(lang="fr"), wait_until="networkidle")  # the session's entrance release
    page.goto(live_server.url + REQUESTS.format(lang="fr"), wait_until="commit")
    page.wait_for_selector("nav.console-bottom", state="attached")
    assert page.evaluate(moving) == [], "the chrome moves while the page loads"
    page.wait_for_load_state("networkidle")
    assert page.evaluate(moving) == []
    page.click("#console-menu")
    _drawer_at_rest(page)
    slide = page.evaluate(
        """() => { const d = document.querySelector('dialog.console-drawer'); const s = getComputedStyle(d);
          return [s.transitionProperty.split(', ').includes('translate'), s.transitionDuration,
                  parseFloat(s.getPropertyValue('--overlay-edge')) * parseFloat(s.getPropertyValue('--dir'))]; }"""
    )
    # the overlay system's «Slide» (W2-A): a translate from the reading edge (-100 % here), 320 ms in
    assert slide == [True, "0.32s", -1], "the drawer comes from its edge, on the person's own press"
    context.close()
    reduced = _context(browser, live_server, person_user, reduced_motion="reduce")
    page = reduced.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.click("#console-menu")
    _drawer_at_rest(page)
    drawer = page.evaluate(DRAWER_JS)
    assert drawer["motion"] == [] and drawer["box"]["x"] == 0, "under reduced motion the drawer is there at once"
    reduced.close()


def test_forced_colours_keep_the_bars_edges_and_the_current_page(browser, live_server, seeded, person_user):
    context = _context(browser, live_server, person_user, forced_colors="active")
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    assert page.evaluate("matchMedia('(forced-colors: active)').matches")
    chrome = page.evaluate(CHROME_JS)
    assert chrome["bar"]["edge"] == "1px" and chrome["bottom"]["edge"] == "1px", (
        "the system's colours give the bars an edge"
    )
    lit = [item for item in chrome["bottom"]["items"] if item["current"]][0]
    assert lit["outline"] == "solid 2px" and lit["discBg"] != chrome["bottom"]["bg"], lit
    stays = chrome["bar"]["box"]["h"] + chrome["bottom"]["box"]["h"]
    assert stays <= 120, stays
    page.click("#console-menu")
    _drawer_at_rest(page)
    assert page.evaluate(DRAWER_JS)["edge"] == "1px", "and the drawer one"
    context.close()


def test_the_device_s_safe_areas_pad_the_bars_and_the_drawer(browser, live_server, seeded, person_user):
    """Emulated (CDP): a notch at the top and the home indicator's band; then the phone on its side."""

    def insets(context, page, top, right, bottom, left):
        session = context.new_cdp_session(page)
        try:
            session.send(
                "Emulation.setSafeAreaInsetsOverride",
                {"insets": {"top": top, "right": right, "bottom": bottom, "left": left}},
            )
        except Exception:  # pragma: no cover - a Chromium without the override: the insets stay 0
            return False
        return True

    context = _context(browser, live_server, person_user)
    page = context.new_page()
    emulated = insets(context, page, 47, 0, 34, 0)
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    chrome = page.evaluate(CHROME_JS)
    plain = 66  # two-line words: 2 + 32 + 2 + 28 + 2
    if emulated:
        assert chrome["bar"]["box"]["h"] == 48 + 47 and chrome["bar"]["tile"]["box"]["y"] == 47 + 8, chrome["bar"]
        assert chrome["bottom"]["box"]["h"] == plain + 34, chrome["bottom"]["box"]
        assert max(item["label"]["b"] for item in chrome["bottom"]["items"]) <= chrome["vh"] - 34, (
            "the words clear the band"
        )
    else:
        assert chrome["bar"]["box"]["h"] == 48 and chrome["bottom"]["box"]["h"] == plain
    context.close()

    for lang in ("fr", "ar"):
        side = _context(browser, live_server, person_user, 844, 390)
        page = side.new_page()
        emulated = insets(side, page, 0, 47, 21, 47)
        _at_rest(page, live_server, REQUESTS.format(lang=lang))
        chrome = page.evaluate(CHROME_JS)
        inset = 47 if emulated else 0
        tile = chrome["bar"]["tile"]["box"]
        if lang == "fr":
            assert tile["x"] == max(32, inset), tile
        else:
            assert tile["r"] == chrome["vw"] - max(32, inset), tile
        for item in chrome["bottom"]["items"]:
            assert item["box"]["x"] >= inset - 0.5 and item["box"]["r"] <= chrome["vw"] - inset + 0.5, (
                lang,
                item["text"],
            )
        workspace = page.evaluate(
            "() => { const s = getComputedStyle(document.querySelector('.console__workspace')); return [parseFloat(s.paddingLeft), parseFloat(s.paddingRight)]; }"
        )
        assert min(workspace) >= max(32, inset), (lang, workspace)
        page.click("#console-menu")
        _drawer_at_rest(page)
        brand = page.evaluate(
            "() => { const d = document.querySelector('dialog.console-drawer'); const b = d.querySelector('.rail__tile').getBoundingClientRect(); const r = d.getBoundingClientRect(); return {x: b.left, r: b.right, left: r.left, right: r.right, vw: document.documentElement.clientWidth}; }"
        )
        if lang == "fr":
            assert brand["x"] >= inset + 12 - 0.5, brand
        else:
            assert brand["r"] <= brand["vw"] - inset - 12 + 0.5, brand
        side.close()


def test_the_focus_is_never_under_a_bar(browser, live_server, seeded, person_user):
    """WCAG 2.4.11: what the keyboard reaches scrolls clear of the sticky top bar and of the fixed bottom bar."""
    context = _context(browser, live_server, person_user, 390, 700, touch=False)
    page = context.new_page()
    _at_rest(page, live_server, DASHBOARD.format(lang="fr"))
    seen = 0
    for _ in range(60):
        page.keyboard.press("Tab")
        where = page.evaluate(
            """() => { const a = document.activeElement; if (!a || a === document.body) return null;
              const r = a.getBoundingClientRect(); const top = document.querySelector('.console-bar').getBoundingClientRect().bottom;
              const bottom = document.querySelector('.console-bottom').getBoundingClientRect().top;
              return {inMain: !!a.closest('main, footer'), top: r.top, bottom: r.bottom, barBottom: top, bottomTop: bottom, height: r.height,
                      name: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 40)}; }"""
        )
        if not where or not where["inMain"]:
            continue
        seen += 1
        assert where["bottom"] > where["barBottom"] and where["top"] < where["bottomTop"], (
            f"focus hidden by a bar: {where}"
        )
        if where["height"] <= 200:
            assert where["top"] >= where["barBottom"] - 0.5 and where["bottom"] <= where["bottomTop"] + 0.5, (
                f"focus partly under a bar: {where}"
            )
    assert seen >= 3, "the walk reached the page"
    context.close()


@pytest.mark.parametrize("size", [(390, 844), (1440, 900)], ids=["a phone", "a desk"])
def test_on_paper_the_page_is_the_page(browser, live_server, seeded, person_user, size):
    """A fixed bar is printed again on every sheet: on paper there is no rail, no bar, no drawer, no reserved room."""
    context = _context(browser, live_server, person_user, *size, touch=size[0] < 1024)
    page = context.new_page()
    _at_rest(page, live_server, REQUESTS.format(lang="fr"))
    page.emulate_media(media="print")
    paper = page.evaluate(
        """() => { const shown = (s) => [...document.querySelectorAll(s)].filter((el) => getComputedStyle(el).display !== 'none').length;
          const b = getComputedStyle(document.body);
          return {chrome: shown('.rail, .console-bar, .console-bottom, .console-drawer'), start: b.paddingInlineStart, end: b.paddingBlockEnd,
                  title: document.querySelector('h1').getBoundingClientRect().width > 0}; }"""
    )
    assert paper == {"chrome": 0, "start": "0px", "end": "0px", "title": True}, paper
    context.close()


# ---------------------------------------------------------------------------------------------- a page's own bar


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_page_s_action_bar_takes_the_entries_place_and_menu_keeps_its_end(
    browser, live_server, seeded, person_user, lang
):
    from cases import services as case_services
    from cases.models import CasePurpose

    case = case_services.open_case(person_user, purpose=CasePurpose.WORK)
    path = reverse("cases:detail", kwargs={"reference": case.reference}).replace("/fr/", f"/{lang}/", 1)
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, path)
    assert page.locator("[data-file-action-bar]").count() == 1, "the case file declares its phone action bar"
    chrome = page.evaluate(CHROME_JS)
    assert chrome["overflow"] <= 0
    items = chrome["bottom"]["items"]
    assert [item["menu"] for item in items] == [True], "the four entries give their place: «Menu» alone stays"
    menu = items[0]
    bar = page.evaluate(
        """() => { const b = document.querySelector('[data-file-action-bar]'); const r = b.getBoundingClientRect(); const act = b.querySelector('a, button').getBoundingClientRect();
          const s = getComputedStyle(b); return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, height: r.height, position: s.position,
            act: {left: act.left, right: act.right, width: act.width, height: act.height, top: act.top, bottom: act.bottom}, vh: innerHeight}; }"""
    )
    assert bar["position"] == "fixed" and bar["bottom"] == bar["vh"] and bar["height"] == 61, bar
    assert bar["left"] == 0 and bar["right"] == chrome["vw"], "one bar, edge to edge"
    stays = chrome["bar"]["box"]["h"] + bar["height"]
    assert stays == 109, f"48 + 61 px of chrome, where two bars made 174: {stays}"
    assert bar["act"]["height"] >= 44 and bar["act"]["width"] >= 240, "the page's one act fills the rest"
    assert menu["box"]["w"] >= 44 and menu["box"]["h"] >= 44
    if lang == "fr":
        assert menu["box"]["x"] >= bar["act"]["right"] and menu["box"]["r"] <= chrome["vw"], "«Menu» at the same end"
    else:
        assert menu["box"]["r"] <= bar["act"]["left"] and menu["box"]["x"] >= 0, "«Menu» at the same end, mirrored"
    assert bar["top"] <= menu["box"]["y"] and menu["box"]["b"] <= bar["bottom"], "on the bar's own row"
    assert _contrast(menu["color"], "rgb(251, 250, 248)") >= 4.5, "in the page's ink, on the page's glass"
    page.click("#console-menu")
    _drawer_at_rest(page)
    assert page.evaluate(DRAWER_JS)["current"] == ["cases"], "and it opens the same drawer"
    page.keyboard.press("Escape")
    # wider: «Menu» keeps a whole seat of 44 px inside the screen (the row's own margin would have pushed it out)
    for width, height in ((430, 932), (768, 1024)):
        page.set_viewport_size({"width": width, "height": height})
        page.goto(live_server.url + path, wait_until="networkidle")
        wide = page.evaluate(CHROME_JS)
        seat = wide["bottom"]["items"][0]["box"]
        assert wide["overflow"] <= 0 and len(wide["bottom"]["items"]) == 1, (lang, width)
        assert seat["w"] >= 44 and seat["x"] >= 0 and seat["r"] <= wide["vw"], (lang, width, seat)
        assert wide["bottom"]["items"][0]["size"] >= (14 if lang == "ar" else 12), (lang, width, "the scale's floor")
    context.close()


def test_the_questionnaire_s_foot_is_part_of_its_page_and_the_bar_keeps_its_entries(
    browser, live_server, seeded, person_user
):
    context = _context(browser, live_server, person_user)
    page = context.new_page()
    _at_rest(page, live_server, SITUATION.format(lang="fr"))
    chrome = page.evaluate(CHROME_JS)
    assert len(chrome["bottom"]["items"]) == 5 and chrome["overflow"] <= 0, "the bar keeps its four entries and «Menu»"
    foot = page.evaluate(
        """() => { const f = document.querySelector('[data-wizard-foot]'); const s = getComputedStyle(f); const r = f.getBoundingClientRect();
          const kids = [...f.children].filter((c) => !c.hidden && c.getBoundingClientRect().width > 0).map((c) => c.getBoundingClientRect());
          return {position: s.position, wrap: s.flexWrap, left: r.left, right: r.right, vw: document.documentElement.clientWidth,
                  inside: kids.every((k) => k.left >= r.left - 0.5 && k.right <= r.right + 0.5)}; }"""
    )
    assert foot["position"] == "static" and foot["wrap"] == "wrap" and foot["inside"], foot
    stays = chrome["bar"]["box"]["h"] + chrome["bottom"]["box"]["h"]
    assert stays <= 120, f"«Ma situation» kept 177 px of chrome while its form was on screen: {stays}"
    context.close()
