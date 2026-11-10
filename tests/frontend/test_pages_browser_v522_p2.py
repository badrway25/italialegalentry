"""
V5.22 — Page Composition V2, lane P2 «system, trust and reading», in Chromium (SECTION_SYSTEM_V2 §3.2, §3.11–§3.18;
label v522-p2-build): what the server cannot show (apps/pages/tests/test_interior_v522.py holds the markup's rules,
apps/forum/tests/test_forum_page.py the Forum's).

* the network's map (§3.11 R1): from a desktop's width, once the module runs, a tablist — the hub first and selected,
  the Arrows around the ring (in the reading direction: mirrored in Arabic), Home, End, Escape back to the hub,
  activation following the focus; the entries stacked in one cell, so a selection never moves the page and the stage
  keeps one height; on a phone (a ring narrower than 300 px) the map is its list, every entry shown;
* the FAQ's explorer (§3.13 Q1): from 64 rem the tabs — the permalink's question selected at load, the address kept in
  step with the selection; below 64 rem each panel's heading becomes its disclosure button, one open at a time;
* the glossary's rail (§3.14 G1): from 64 rem a thumb index beside the cards that stays under the letterhead while the
  register scrolls; a letter reached from it lands under the letterhead and the rail marks it as the one in view;
* the family's ten pages at eight widths, in French and in Arabic: never wider than the viewport, one h1, and the
  letterhead's height the one it has on a page this lane did not touch (the AGAMI plate once took the letterhead's
  «targa» class and wrapped its menu onto two rows);
* under reduced motion every composition stands still and complete: no section state written, no animation running,
  the story not driven; without script every entry is in the page, in reading order (the map's six entries, the FAQ's
  nine answers, the story's steps);
* the final round (QA_ROUND3 m1, m2, m6): Vivre's band begins at its moment's foot, on the moment's own ground; a
  glossary row holds its cards' parts on shared lines; the Forum's desktop drawing hangs from the title's line whatever
  the head receives after the first paint;
* the final improve round (v522-p2-final-qa1 M1, m1–m3; with lane S's v522/s2): the scroll-spy lights each letter
  followed and every entry of the Forum's sommaire; a dictionary card under the hand keeps its row, so a mouse reader's
  read-through lights every letter of the rail; AGAMI's identity band plays its signature in view at load; the rows of
  two V2 disclosures never wait for the legacy rise.

Chromium on the live server, the seeded site, gate G3 open, gate G2 opened by TEST-ONLY legal text, the clock at
3 October 2026 through `core.clock.now` (a frozen monotonic clock stalls Playwright), the WhatsApp channel configured
with the fictional number of tests/conftest.py.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

#: the lane's pages (the Forum's included), and a page this lane did not touch for the letterhead's reference height
PAGES = (
    "le-projet/",
    "reseau/",
    "contact/",
    "faq/",
    "glossaire/",
    "glossaire/nulla_osta/",
    "vivre-en-italie/",
    "forum/",
    "agami/",
    "attention-aux-fraudes/",
)
REFERENCE = "privacy-policy/"
WIDTHS = (320, 360, 390, 414, 768, 1024, 1280, 1440)
ACTORS = ("#rete-persons", "#rete-companies", "#rete-institutions", "#rete-universities", "#rete-professionals")

MAP = r"""() => {
  const root = document.querySelector('header.ingresso[data-sec-js~="mappa"]');
  const tabs = [...root.querySelectorAll('.mappa__tasto')];
  const panels = [...root.querySelectorAll('.rete__pannello')];
  const shown = (el) => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  return {sel: root.dataset.sel || null, role: root.querySelector('.mappa__nodi').getAttribute('role'),
          tabs: tabs.filter((t) => t.getAttribute('role') === 'tab').length,
          selected: tabs.filter((t) => t.getAttribute('aria-selected') === 'true').map((t) => t.hash),
          tabbable: tabs.filter((t) => t.tabIndex === 0).map((t) => t.hash),
          focus: document.activeElement && document.activeElement.hash ? document.activeElement.hash : null,
          on: panels.filter((p) => p.hasAttribute('data-on')).map((p) => '#' + p.id),
          shown: panels.filter(shown).map((p) => '#' + p.id),
          height: Math.round(root.querySelector('.rete__pannelli').getBoundingClientRect().height), y: Math.round(scrollY)};
}"""

#: FINAL MICRO-PASS §6 B1 (V5.20): the FAQ is one list of the system's disclosures (the explorer's probe left with it)
LIST = r"""() => {
  const root = document.querySelector('section#questions[data-cerca]');
  const rows = [...root.querySelectorAll('.faq-lista > details.faq-item')];
  return {open: rows.filter((r) => r.open).map((r) => '#' + r.id),
          shown: rows.filter((r) => !r.hidden && r.getBoundingClientRect().height > 0).map((r) => '#' + r.id),
          pressed: [...root.querySelectorAll('.faq-tema')].filter((b) => b.getAttribute('aria-pressed') === 'true')
            .map((b) => b.dataset.cercaTema),
          count: root.querySelector('[data-cerca-conto]').textContent.trim(),
          empty: !root.querySelector('[data-cerca-vuoto]').hidden,
          hash: location.hash, y: Math.round(scrollY),
          header: Math.round(document.querySelector('.site-header').getBoundingClientRect().bottom)};
}"""


def _settled(page) -> int:
    """The page's scroll once it rests: a permalink's jump lands, then the module's tabs collapse the panels into one
    cell and the browser settles the fragment again (smoothly, under no preference) — measure after, never during."""
    last, still = -1, 0
    for _ in range(40):
        y = page.evaluate("() => Math.round(scrollY)")
        still = still + 1 if y == last else 0
        if still >= 3:
            return y
        last = y
        page.wait_for_timeout(100)
    return last


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
def site(live_server, seeded, set_flag, monkeypatch, legal_published, whatsapp_channel):
    """Gate G3 open for the live server without freezegun, the Forum's seeded edition."""
    from core import clock, flags
    from forum.seeds import seed_forum_event

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    seed_forum_event()
    flags.invalidate()
    yield live_server.url
    flags.invalidate()


# ---- the network's map (§3.11 R1) -------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_network_map_is_a_tablist_around_its_ring(browser, site, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/reseau/", wait_until="networkidle")
        page.wait_for_selector(".mappa__nodi[role='tablist']")
        state = page.evaluate(MAP)
        assert state["tabs"] == 6 and state["role"] == "tablist", state
        assert state["selected"] == ["#rete-hub"] and state["tabbable"] == ["#rete-hub"], state
        assert state["on"] == ["#rete-hub"] and state["shown"] == ["#rete-hub"] and state["sel"] == "hub", state
        height, y = state["height"], state["y"]
        page.focus("#rete-hub-tab")
        # the Arrows follow the reading direction: ArrowRight is the next actor in French, the previous in Arabic
        forward, back = ("ArrowRight", "ArrowLeft") if lang == "fr" else ("ArrowLeft", "ArrowRight")
        steps = [
            (forward, ACTORS[0]),
            (forward, ACTORS[1]),
            (back, ACTORS[0]),
            ("End", ACTORS[-1]),
            ("Home", "#rete-hub"),
            (back, ACTORS[-1]),
            ("Escape", "#rete-hub"),
            ("ArrowDown", ACTORS[0]),
        ]
        for key, expected in steps:
            page.keyboard.press(key)
            state = page.evaluate(MAP)
            where = (lang, key, expected, state)
            assert state["selected"] == [expected] and state["tabbable"] == [expected], where
            assert state["focus"] == expected and state["on"] == [expected], where
            assert state["shown"] == [expected], where
            assert state["sel"] != "hub" if expected != "#rete-hub" else state["sel"] == "hub", where
            # one cell for every entry: the stage keeps its height, the page never moves
            assert abs(state["height"] - height) <= 1 and state["y"] == y, where
        # a click commits a node as the keyboard does
        page.click(f"{ACTORS[2]}-tab")
        assert page.evaluate(MAP)["selected"] == [ACTORS[2]]
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_phone_s_map_is_a_tablist_and_a_narrow_ring_its_list(browser, site, lang):
    """Round 1 (QA_ROUND1 m3): at the phones' widths the ring is 300 px and more (335 at 390), so the map is the tablist
    there too, its entries in one cell from the first paint; only a narrower ring (a 320 px viewport: 288 px) leaves the
    list as the map, every entry shown — sezioni/mappa.js's contract, and the page's first paint agrees with it."""
    for width, tablist in ((390, True), (360, True), (320, False)):
        context = browser.new_context(viewport={"width": width, "height": 800})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/reseau/", wait_until="networkidle")
            ring = page.evaluate("() => document.querySelector('.mappa__anello').getBoundingClientRect().width")
            state = page.evaluate(MAP)
            where = (lang, width, ring, state)
            if tablist:
                page.wait_for_selector(".mappa__nodi[role='tablist']")
                state = page.evaluate(MAP)
                assert ring >= 300 and state["tabs"] == 6 and state["shown"] == ["#rete-hub"], where
            else:
                assert ring < 300 and state["role"] == "list" and state["sel"] is None, where
                assert state["shown"] == ["#rete-hub", *ACTORS], where
        finally:
            context.close()


# ---- round 1 (QA_ROUND1 M2): the relational draw reaches the chosen actor, in both directions --------------------------
SPOKE = r"""(k) => {
  const mid = (r) => [r.left + r.width / 2, r.top + r.height / 2];
  const ring = mid(document.querySelector('.fronte-rete__lines').getBoundingClientRect());
  const s = document.querySelector('.rete__raggio--' + k).getBoundingClientRect();
  const corners = [[s.left, s.top], [s.right, s.top], [s.left, s.bottom], [s.right, s.bottom]];
  const far = corners.reduce((a, b) => Math.hypot(b[0] - ring[0], b[1] - ring[1]) > Math.hypot(a[0] - ring[0], a[1] - ring[1]) ? b : a);
  const disc = mid(document.querySelector('.fronte-rete__node--' + k + ' .fronte-rete__disc').getBoundingClientRect());
  return {lit: getComputedStyle(document.querySelector('.rete__raggio--' + k)).opacity, gap: Math.round(Math.hypot(far[0] - disc[0], far[1] - disc[1]))};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_chosen_actor_s_spoke_ends_on_its_own_disc(browser, site, lang):
    """The line layer is drawn left to right while the nodes stand on logical insets: on the Arabic page it mirrors with
    them, so each actor chosen lights the spoke that ends on its own disc (it lit the mirrored actor's — 4 of 5)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/reseau/", wait_until="networkidle")
        page.wait_for_selector(".mappa__nodi[role='tablist']")
        for k, actor in enumerate(ACTORS):
            page.click(f"{actor}-tab")
            # the pointer then leaves the ring — while the head's entrance still moves the nodes, another one passing
            # under a resting pointer previews itself (the fine pointer's hover) — and the spoke is measured once its
            # draw has played (sez-stroke over --motion-emphasized), never in the middle of it
            page.mouse.move(5, 5)
            page.wait_for_function(
                "(k) => document.querySelector('.rete__raggio--' + k).getAnimations().length === 0", arg=k
            )
            spoke = page.evaluate(SPOKE, k)
            assert spoke["lit"] == "1" and spoke["gap"] <= 6, (lang, actor, spoke)
    finally:
        context.close()


# ---- the FAQ's explorer (§3.13 Q1) ------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_faq_permalink_opens_its_row_and_the_list_answers_as_one_types(browser, site, lang):
    """FINAL MICRO-PASS §6 B1 (V5.20 strict rule; replaces «the FAQ explorer selects its permalink and keeps the address in
    step»): the explorer left for ONE list of the system's disclosures, after 21st.dev 37558. A permalink opens its row —
    the only one open — under the letterhead; a theme narrows the list (its pill pressed, the live count saying how
    many); a query narrows it as one types; a query without answer draws the inline empty state, whose button gives
    every question back; Escape empties the field."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/faq/#faq_diplomas", wait_until="networkidle")
        page.wait_for_selector("section#questions.cerca-viva")
        _settled(page)
        state = page.evaluate(LIST)
        assert state["open"] == ["#faq_diplomas"] and len(state["shown"]) == 9 and state["count"] == "", state
        top = page.evaluate("() => document.getElementById('faq_diplomas').getBoundingClientRect().top")
        assert state["header"] - 1 <= top < 900 * 0.6, (top, state)
        page.locator("button.faq-tema[data-cerca-tema='securite']").click()
        state = page.evaluate(LIST)
        assert state["pressed"] == ["securite"], state
        assert state["shown"] == ["#faq_data_protection", "#faq_guaranteed_visa_offer"] and "2" in state["count"], state
        page.locator("button.faq-tema[data-cerca-tema='']").click()
        page.fill("#faq-q", "zzzz")
        state = page.evaluate(LIST)
        assert state["shown"] == [] and state["empty"] and "0" in state["count"], state
        page.locator("[data-cerca-azzera]").click()
        state = page.evaluate(LIST)
        assert len(state["shown"]) == 9 and not state["empty"] and state["count"] == "" and state["pressed"] == [""], state
        assert page.input_value("#faq-q") == ""
        word = page.evaluate(
            "() => document.querySelector('#faq_diplomas .faq-item__question').textContent.trim().split(/\\s+/)"
            ".sort((a, b) => b.length - a.length)[0]"
        )
        page.fill("#faq-q", word)
        state = page.evaluate(LIST)
        assert "#faq_diplomas" in state["shown"] and 0 < len(state["shown"]) < 9 and state["count"], (word, state)
        page.locator("#faq-q").press("Escape")
        assert len(page.evaluate(LIST)["shown"]) == 9 and page.input_value("#faq-q") == ""
    finally:
        context.close()



@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_below_64rem_the_faq_questions_are_exclusive_disclosures(browser, site, lang):
    """FINAL MICRO-PASS §6 B1 (V5.20; the explorer's phone disclosures became the list's rows — the same invariant, now at
    every width): the questions are native disclosures of one exclusive group — closed at load, Enter and Space open and
    close them from the keyboard, one answer open at a time — and the summary holds the question's words."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/faq/", wait_until="networkidle")
        page.wait_for_selector("section#questions.cerca-viva")
        state = page.evaluate(LIST)
        assert state["open"] == [] and len(state["shown"]) == 9, state
        summaries = page.locator("section#questions details.faq-item > summary")
        summaries.nth(0).focus()
        page.keyboard.press("Enter")
        assert page.evaluate(LIST)["open"] == ["#faq_visas"]
        summaries.nth(1).focus()
        page.keyboard.press("Space")
        assert page.evaluate(LIST)["open"] == ["#faq_recruitment_agency"], "one answer open at a time"
        page.keyboard.press("Space")
        assert page.evaluate(LIST)["open"] == []
        assert summaries.nth(0).inner_text().strip() == page.locator("#faq_visas-title").inner_text().strip()
    finally:
        context.close()



# ---- the Forum's ring (§3.16 FO2b) ------------------------------------------------------------------------------------
RING = r"""() => {
  const mid = (el) => { const r = el.getBoundingClientRect(); return r.left + r.width / 2; };
  const hub = mid(document.querySelector('.forum-anello__centro'));
  return [...document.querySelectorAll('.forum-attore')].map((a) => Math.round(mid(a) - hub));
}"""


def test_the_forum_ring_turns_round_its_hub_and_mirrors_in_arabic(browser, site):
    """The nine actors stand round the hub: the first above it, the others clockwise in the sentence's order — and
    counter-clockwise on the Arabic page (the sentence stays a French run: its places mirror, never its words)."""
    offsets = {}
    for lang in ("fr", "ar"):
        context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
            offsets[lang] = page.evaluate(RING)
        finally:
            context.close()
    assert len(offsets["fr"]) == 9 and abs(offsets["fr"][0]) <= 2 and abs(offsets["ar"][0]) <= 2, offsets
    assert all(x > 0 for x in offsets["fr"][1:4]) and all(x < 0 for x in offsets["fr"][6:9]), offsets
    assert all(abs(a + b) <= 2 for a, b in zip(offsets["fr"], offsets["ar"], strict=True)), offsets


# ---- the glossary's rail (§3.14 G1) -----------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_letter_rail_stands_beside_the_cards_and_a_letter_lands_under_the_letterhead(browser, site, lang):
    """FINAL MICRO-PASS §6 B2 (V5.20; was «the rail stands beside the cards, at the reading edge»): the alphabet is a quiet
    row ABOVE the register, its width — sticky under the letterhead, in the screen, at the same place while the register
    scrolls; a letter followed lands under the letterhead and the row, and is the one current."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
        geometry = """() => { const rail = document.querySelector('nav.az-index').getBoundingClientRect();
            const cards = document.querySelector('.lessico__registro').getBoundingClientRect();
            return {top: rail.top, bottom: rail.bottom, left: rail.left, right: rail.right,
                    cardsTop: cards.top, cardsLeft: cards.left, cardsRight: cards.right,
                    header: document.querySelector('.site-header').getBoundingClientRect().bottom}; }"""
        rest = page.evaluate(geometry)
        assert rest["bottom"] <= rest["cardsTop"] + 0.5, ("above the register", rest)
        assert abs(rest["left"] - rest["cardsLeft"]) <= 1 and abs(rest["right"] - rest["cardsRight"]) <= 1, rest
        start = page.evaluate(
            "() => Math.round(document.querySelector('.lessico__registro').getBoundingClientRect().top + scrollY)"
        )
        page.evaluate("(y) => window.scrollTo(0, y)", start + 300)
        page.wait_for_timeout(300)
        first = page.evaluate(geometry)
        page.evaluate("(y) => window.scrollTo(0, y)", start + 700)
        page.wait_for_timeout(300)
        second = page.evaluate(geometry)
        assert first["top"] >= first["header"] - 1 and first["bottom"] <= 900, first
        assert abs(second["top"] - first["top"]) <= 1, (first, second)
        link = page.locator(".az-index__link").nth(3)
        target = link.get_attribute("href")
        link.click()
        page.wait_for_timeout(700)
        landed = page.evaluate("(id) => document.getElementById(id).getBoundingClientRect().top", target[1:])
        assert landed >= first["bottom"] - 1 and landed < 450, (landed, first)
        page.wait_for_function(
            "(href) => document.querySelector(`.az-index__link[href='${href}']`).getAttribute('aria-current') === 'location'",
            arg=target,
            timeout=3000,
        )
        assert page.locator(".az-index__link[aria-current='location']").count() == 1
    finally:
        context.close()



# ---- every page of the family, eight widths, two directions -----------------------------------------------------------
def test_the_family_never_overflows_and_keeps_the_letterhead_s_height(browser, site):
    failures = []
    for lang in ("fr", "ar"):
        for width in WIDTHS:
            context = browser.new_context(
                viewport={"width": width, "height": 900 if width > 800 else 800}, reduced_motion="reduce"
            )
            page = context.new_page()
            page.goto(f"{site}/{lang}/{REFERENCE}", wait_until="load")
            reference = page.evaluate("() => document.querySelector('.site-header').getBoundingClientRect().height")
            for path in PAGES:
                response = page.goto(f"{site}/{lang}/{path}", wait_until="load")
                probe = page.evaluate(
                    """() => ({overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                               h1: document.querySelectorAll('h1').length,
                               header: document.querySelector('.site-header').getBoundingClientRect().height})"""
                )
                where = f"{lang} {width} /{path}"
                if response.status != 200:
                    failures.append(f"{where}: HTTP {response.status}")
                if probe["overflow"] > 0:
                    failures.append(f"{where}: {probe['overflow']} px wider than the viewport")
                if probe["h1"] != 1:
                    failures.append(f"{where}: {probe['h1']} h1")
                if abs(probe["header"] - reference) > 0.5:
                    failures.append(f"{where}: the letterhead {probe['header']} px, {reference} px elsewhere")
            context.close()
    assert failures == [], "\n".join(failures)


# ---- reduced motion and no script --------------------------------------------------------------------------------------
STILL = r"""async () => {
  for (let y = 0; y < document.documentElement.scrollHeight; y += Math.round(innerHeight * 0.8)) {
    scrollTo(0, y);
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  }
  await new Promise((r) => setTimeout(r, 400));
  return {states: document.querySelectorAll('[data-sec-state]').length,
          running: document.getAnimations().filter((a) => a.playState === 'running').map((a) => a.animationName || a.transitionProperty || 'animation'),
          live: document.querySelectorAll('.racconto[data-live]').length};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_under_reduced_motion_every_composition_stands_still_and_complete(browser, site, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    try:
        page = context.new_page()
        for path in PAGES:
            page.goto(f"{site}/{lang}/{path}", wait_until="networkidle")
            still = page.evaluate(STILL)
            assert still == {"states": 0, "running": [], "live": 0}, (path, still)
    finally:
        context.close()


def test_without_script_every_entry_is_in_the_page_in_reading_order(browser, site):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    try:
        page = context.new_page()
        page.goto(f"{site}/fr/reseau/", wait_until="load")
        shown = page.evaluate(
            """() => [...document.querySelectorAll('.rete__pannello')].filter((p) => {
                 const cs = getComputedStyle(p); return cs.display !== 'none' && cs.visibility !== 'hidden'; })
               .map((p) => '#' + p.id)"""
        )
        assert shown == ["#rete-hub", *ACTORS]
        # FINAL MICRO-PASS §6 B1 (V5.20; the explorer's nine panels stood open without script): the nine rows stand in the
        # register's order, every answer in the page and opened by the browser alone, the search's submit drawn
        page.goto(f"{site}/fr/faq/", wait_until="load")
        rows = page.evaluate("() => [...document.querySelectorAll('.faq-lista > details.faq-item')].map((d) => d.id)")
        assert len(rows) == 9 and rows[0] == "faq_visas" and rows[-1] == "faq_guaranteed_visa_offer", rows
        assert page.locator(".faq-lista .faq-risposta").count() == 9
        page.locator("#faq_diplomas > summary").click()
        # the disclosure's content turns visible on its transition's first frame (v5/motion.css): read it then, not before
        answer = page.locator("#faq_diplomas .faq-risposta")
        answer.wait_for(state="visible")
        assert page.evaluate("() => document.getElementById('faq_diplomas').open") and answer.bounding_box()["height"] > 0
        assert page.locator(".faq__search .cerca__invio").is_visible()
        page.goto(f"{site}/fr/le-projet/", wait_until="load")
        steps = page.evaluate(
            """() => [...document.querySelectorAll('.racconto__passo')].map((s) => {
                 const cs = getComputedStyle(s); return [s.id, cs.opacity, cs.visibility]; })"""
        )
        assert [s[0] for s in steps] == ["project-presentation", "project-why", "project-promoter"]
        assert all(s[1] == "1" and s[2] == "visible" for s in steps), steps
    finally:
        context.close()


# ---- round 1 (QA_ROUND1 M1, M3–M6): what the round's review measured broken, held ------------------------------------
#: the eight widths of SECTION_SYSTEM_V2 §9.9 and their heights
EIGHT = ((1440, 900), (1280, 800), (1024, 768), (768, 1024), (430, 932), (390, 844), (375, 812), (360, 800))
#: the FAQ's permalinks the site's own links name: the trust band's four and the fraud page's
PERMALINKS = (
    "faq_visas",
    "faq_recruitment_agency",
    "faq_preassessment_guarantee",
    "faq_diplomas",
    "faq_guaranteed_visa_offer",
)

CLS_INIT = """window.__cls = 0; new PerformanceObserver((list) => { for (const e of list.getEntries()) {
  if (!e.hadRecentInput) window.__cls += e.value; } }).observe({type: 'layout-shift', buffered: true});"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_faq_permalink_followed_from_another_page_lands_on_its_question(browser, site, lang):
    """M1: a permalink opened as a fresh document (the trust band's, the fraud page's) leaves its question in the screen,
    under the letterhead, at every form of the explorer — from 64 rem its answer the one on the stage; below, the phone's
    form drawn from the first paint as the module draws it (the index said by the panels, the other answers folded), so
    the browser's jump lands where the module keeps the question (it landed 265–544 px past it). (Opening the named
    answer on a phone is sezioni/indice.js's — requested of lane S.)"""
    for width, height in ((1440, 900), (768, 1024), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            for key in PERMALINKS:
                # each permalink from another page: a fresh document (from /faq/#a, /faq/#b is the same document)
                page.goto(f"{site}/{lang}/attention-aux-fraudes/", wait_until="networkidle")
                page.goto(f"{site}/{lang}/faq/#{key}", wait_until="networkidle")
                page.wait_for_selector("section#questions.cerca-viva")
                _settled(page)
                box = page.evaluate(
                    """(key) => { const h = document.getElementById(key + '-title').getBoundingClientRect();
                        return {top: h.top, bottom: h.bottom,
                                header: document.querySelector('.site-header').getBoundingClientRect().bottom}; }""",
                    key,
                )
                where = (lang, width, key, box)
                assert box["top"] >= box["header"] - 1 and box["bottom"] <= height, where
                # FINAL MICRO-PASS §6 B1 (V5.20): at every width the named row is the one open (it was the explorer's
                # selected panel from 64 rem, its one expanded button below)
                assert page.evaluate(LIST)["open"] == [f"#{key}"], where
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_map_and_the_explorer_never_move_the_page_as_they_load(browser, site, lang):
    """M3 (§5.3: CLS ≤ 0.1): with script the map's entries and the phone explorer's answers are drawn from the first
    paint as their modules draw them, so nothing restacks once they run (CLS was 0.16–0.34)."""
    for path, width, height in (
        ("reseau/", 1440, 900),
        ("reseau/", 1024, 768),
        ("faq/", 1440, 900),
        ("faq/", 768, 1024),
        ("faq/", 390, 844),
    ):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.add_init_script(CLS_INIT)
            page.goto(f"{site}/{lang}/{path}", wait_until="networkidle")
            page.wait_for_timeout(1500)
            cls = page.evaluate("() => window.__cls")
            assert cls <= 0.1, (lang, path, width, cls)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_story_s_figure_stays_inside_its_plate(browser, site, lang):
    """M4: the figure is the largest square inside its plate's content box (a size container) — every actor's disc inside
    the plate at the laptops' widths (it spilled off it from 1366 to 1024, and covered the steps at 1024)."""
    for width, height in ((1440, 900), (1366, 768), (1280, 800), (1152, 864), (1024, 768), (768, 1024), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/le-projet/", wait_until="networkidle")
            out = page.evaluate(
                """() => { const plate = document.querySelector('.projet-racconto .racconto__figura').getBoundingClientRect();
                    return [...document.querySelectorAll('.projet-racconto .sistema__nodo')].filter((n) => {
                      const r = n.getBoundingClientRect();
                      return r.left < plate.left - 0.5 || r.right > plate.right + 0.5 || r.top < plate.top - 0.5 || r.bottom > plate.bottom + 0.5;
                    }).map((n) => n.className); }"""
            )
            assert out == [], (lang, width, out)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_every_channel_holds_its_words_and_an_address_never_breaks(browser, site, lang):
    """M5: each channel's plate holds its number, kind and act at the eight widths (WhatsApp's number ran past its plate
    at 1280 and 1024); M6: the report's and the identification's address stands on one line at the eight widths (it
    broke inside its domain at 1024, 430–360 and 1280, 1024, 360)."""
    plates = """() => [...document.querySelectorAll('.centralino .canale')].map((c) => { const r = c.getBoundingClientRect();
        const kids = [...c.querySelectorAll('.canale__number, .canale__kind, .canale__act, .btn')].map((k) => k.getBoundingClientRect());
        return Math.max(0, ...kids.map((k) => k.right - r.right), ...kids.map((k) => r.left - k.left)); })"""
    lines = """(sel) => { const e = document.querySelector(sel); const range = document.createRange(); range.selectNodeContents(e);
        return new Set([...range.getClientRects()].map((r) => Math.round(r.top))).size; }"""
    failures = []
    for width, height in EIGHT:
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/contact/", wait_until="networkidle")
            over = page.evaluate(plates)
            if len(over) != 3 or max(over) > 0.5:
                failures.append(f"{lang} {width} contact: {over}")
            for path, sel in (
                ("attention-aux-fraudes/", ".frodi__indirizzo .email"),
                ("agami/", ".agami-id__indirizzo .email"),
            ):
                page.goto(f"{site}/{lang}/{path}", wait_until="networkidle")
                if page.evaluate(lines, sel) != 1:
                    failures.append(f"{lang} {width} {path}: the address breaks")
        finally:
            context.close()
    assert failures == [], "\n".join(failures)


# ---- round 2 (label v522-p2-improve2; QA_ROUND2) ----------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_spy_lights_each_letter_followed_and_each_section_read(browser, site, lang):
    """QA_ROUND2 M3 (with lane S's spia.js: parts crossing the band together are one stop, marked from its first; a
    followed link current at once): each of the glossary's letters, followed from the rail, lights itself — three columns
    at 1440 and 1280, two at 1024 —; scrolling the Forum at 1440 lights every entry of its sommaire (the pairs read side
    by side as one stop) — counted from the sommaire itself, which lists the five sections and, while the event is
    ahead, its programme and registration (seven in the test database; S2 review m1, v522-p2-final-qa1 M1)."""
    lit = """(sel) => [...document.querySelectorAll(sel)].filter((a) => a.hasAttribute('aria-current')
        || a.hasAttribute('data-spia-con')).map((a) => a.hash)"""
    for width, height in ((1440, 900), (1280, 800), (1024, 768)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
            links = page.locator(".az-index__link")
            for i in range(links.count()):
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(300)
                href = links.nth(i).get_attribute("href")
                links.nth(i).click()
                page.wait_for_timeout(1200)
                current = page.evaluate("() => document.querySelector('.az-index__link[aria-current]')?.hash")
                assert current == href, (lang, width, href, current)
            if width == 1440:
                page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
                every = set(
                    page.evaluate("() => [...document.querySelectorAll('.forum-localnav a')].map((a) => a.hash)")
                )
                assert len(every) >= 5, (lang, sorted(every))
                seen = set()
                for _ in range(60):
                    page.mouse.wheel(0, 90)
                    page.wait_for_timeout(90)
                    seen |= set(page.evaluate(lit, ".forum-localnav a"))
                assert seen == every, (lang, sorted(every - seen))
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_faq_permalink_arrives_without_moving_the_page(browser, site, lang):
    """QA_ROUND2 M1 (§5.3: CLS ≤ 0.1): a permalink followed from another page — the trust band's, the fraud page's, the
    Entreprises link — never shifts the page as it lands: from 64 rem the explorer is drawn from the first paint as the
    tabs draw it (every answer in the stage's one cell, :target switching visibility, never display), below 64 rem as
    the phone's disclosures fold it. It measured 0.10–0.14 on the trust links' path (the stage collapsed from 2 596 px
    to the named answer as Chromium matched :target)."""
    for width, height in ((1440, 900), (1024, 768), (768, 1024), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.add_init_script(CLS_INIT)
            for key in PERMALINKS:
                page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
                page.evaluate("(href) => { location.href = href; }", f"/{lang}/faq/#{key}")
                page.wait_for_url(f"**/faq/#{key}")
                page.wait_for_selector("section#questions.cerca-viva")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(600)
                cls = page.evaluate("() => window.__cls")
                assert cls <= 0.1, (lang, width, key, cls)  # the gate (§5.3); 0.0001 measured at this round
                # FINAL MICRO-PASS §6 B1 (V5.20): the named row is the one open, at every width
                assert page.evaluate(LIST)["open"] == [f"#{key}"], (lang, width, key)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_glossary_letters_are_drawn_and_light_as_they_cross_the_reading_line(browser, site, lang):
    """FINAL MICRO-PASS §6 B2 (V5.20; this decision replaces QA_ROUND2 M6's outlined letters scrubbed by the scroll and the
    register's rules drawn at load — «no giant outlined letters», «existing reveal only»): a letter of the register is a
    modest heading, solid in the accent ink, the same at rest and on the reading line; no rule of the register is drawn
    — every row stands on its hairline, its term and its definition whole (the section's own reveal is the one motion)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
        page.wait_for_timeout(600)
        assert page.locator(".lessico__regola").count() == 0
        letters = """() => [...document.querySelectorAll('.lessico__lettera')].map((h) => { const cs = getComputedStyle(h);
            return {l: h.textContent, color: cs.color, fill: cs.webkitTextFillColor, stroke: parseFloat(cs.webkitTextStrokeWidth),
                    size: parseFloat(cs.fontSize)}; })"""
        rest = page.evaluate(letters)
        assert len(rest) >= 5 and all(x["fill"] == x["color"] and x["stroke"] == 0 and x["size"] <= 22 for x in rest), rest
        y = page.evaluate("() => document.getElementById('lettre-N').getBoundingClientRect().top + scrollY")
        page.evaluate("(y) => window.scrollTo(0, y - 900 * 0.325)", y)
        page.wait_for_timeout(400)
        assert page.evaluate(letters) == rest, "the scroll changes no letter"
        rows = page.evaluate(
            """() => [...document.querySelectorAll('.lessico__registro .lessico__carta')].map((c) =>
                [c.querySelector('.lessico__termine').textContent.trim().length > 0,
                 c.querySelector('.lessico__definizione').getBoundingClientRect().height > 0])"""
        )
        assert len(rows) == 10 and all(r[0] and r[1] for r in rows), rows
    finally:
        context.close()



@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_fraud_page_answers_its_question_and_its_address_answers_the_hand(browser, site, lang):
    """QA_ROUND2 M7: the prescribed question opens the prescribed answer in place (the system's accordion, from the
    keyboard too); the address's hover and focus are seen — the light runs along the plate's sill from the reading
    edge and the shield's keyhole fills; in view at load on a desktop, the sill draws in the head's sequence."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/attention-aux-fraudes/", wait_until="commit")
        page.wait_for_selector(".frodi__soglia", state="attached")
        page.wait_for_timeout(200)
        assert page.evaluate("() => document.querySelector('.frodi__soglia').getAnimations().length") == 1
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        page.mouse.move(2, 2)
        response = """() => ({sill: getComputedStyle(document.querySelector('.frodi__soglia'), '::after').scale,
            key: parseFloat(getComputedStyle(document.querySelector('.frodi__scudo .sg-t')).fillOpacity)})"""
        rest = page.evaluate(response)
        assert rest["sill"].startswith("0") and rest["key"] < 0.2, rest
        page.hover(".frodi__indirizzo")
        page.wait_for_timeout(700)
        lit = page.evaluate(response)
        assert lit["sill"] in ("1", "1 1") and lit["key"] > 0.7, lit
        page.mouse.move(2, 2)
        # from the keyboard: the same response, at once; the question opens its answer
        page.keyboard.press("Tab")
        page.focus(".frodi__indirizzo")
        assert page.evaluate(response)["key"] > 0.7
        page.focus(".frodi__domanda summary")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        opened = page.evaluate(
            """() => { const d = document.getElementById('frodi-domanda'); const p = d.querySelector('.accordion__panel p');
                return {open: d.open, h: p.getBoundingClientRect().height,
                        link: !!d.querySelector('.accordion__panel a[href$="/faq/#faq_guaranteed_visa_offer"]')}; }"""
        )
        assert opened["open"] and opened["h"] > 20 and opened["link"], opened
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_vivre_s_seal_draws_in_the_head_and_its_door_answers_the_band_s_action(browser, site, lang):
    """QA_ROUND2 M8 (§4.9 n° 13, §4.7) RESTATED under V5.20 for FINAL MICRO-PASS §5 A3 (the heads' T1 seals left, the
    living head's «ile-vivere» with them): the head draws no seal — nothing to stroke, no door to light — under either
    motion, and the band's action stands, the way down to «Pour s'installer», under the hand and from the keyboard."""
    for motion in ("no-preference", "reduce"):
        context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion=motion)
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/vivre-en-italie/", wait_until="networkidle")
            head = page.evaluate(
                "() => { const h = document.querySelector('.vivere-testa__header');"
                " return [h.querySelectorAll('.sigillo, .vivere-testa__sigillo, [data-mark]').length,"
                " document.getAnimations().filter((a) => a.animationName === 'sez-stroke').length,"
                " h.querySelector('h1').textContent.trim().length]; }"
            )
            assert head[0] == 0 and head[1] == 0 and head[2] > 0, (motion, head)
            page.hover(".vivere-testa__azione")
            assert page.evaluate("document.querySelector('.vivere-testa__azione').hash") == "#living-settle-title"
            page.focus(".vivere-testa__azione")
            assert page.evaluate("document.activeElement.matches('.vivere-testa__azione')"), (
                "the action takes the focus"
            )
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_forum_s_drawing_never_lies_under_its_index(browser, site, lang):
    """QA_ROUND2 m2: below 64 rem the head's drawing stands under the page's index, on the band's foot — its drawn arcs
    cross no link (at 768 they lay under the sommaire: 103 000 px² of overlap, the drawing's centre under a link)."""
    for width, height in ((1024, 768), (768, 1024), (390, 844), (360, 800)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
            out = page.evaluate(
                """() => { const d = document.querySelector('.forum-hero__marchio .sg-a0').getBoundingClientRect();
                    const hero = document.querySelector('.forum-hero').getBoundingClientRect();
                    const hits = [...document.querySelectorAll('.forum-localnav a')].filter((a) => {
                      const r = a.getBoundingClientRect();
                      return Math.min(d.right, r.right) > Math.max(d.left, r.left)
                        && Math.min(d.bottom, r.bottom) > Math.max(d.top, r.top);
                    }).map((a) => a.hash);
                    return {hits, inside: d.bottom <= hero.bottom + 1 && d.top >= hero.top}; }"""
            )
            assert out["hits"] == [] and out["inside"], (lang, width, out)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_identity_plate_keeps_its_box_when_the_question_opens(browser, site, lang):
    """QA_ROUND2 m3: opening the promoter's question (the row grows) never re-scales the identity's plate.
    V5.30 §8 (the owner's final art direction, an approved decision; strict rule V5.20): the plate holds «En bref», the role
    panel, instead of the drawn colonnade — the same invariant on what it now holds: the plate's box and its first fact stay
    exactly where they were (the plate stands at the row's start, never stretched by the text column), and nothing in the
    band is drawn."""
    for width, height in ((1440, 900), (1280, 800), (1024, 768)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/agami/", wait_until="networkidle")
            box = """() => { const p = document.querySelector('.agami-identita__lastra').getBoundingClientRect();
                const f = document.querySelector('.agami-breve__voce').getBoundingClientRect();
                return {w: Math.round(p.width), h: Math.round(p.height), top: Math.round(f.top - p.top),
                        drawn: document.querySelectorAll('.agami-identita svg').length}; }"""
            closed = page.evaluate(box)
            page.click("#agami-faq > summary")
            page.wait_for_timeout(300)
            opened = page.evaluate(box)
            assert opened == closed, (lang, width, closed, opened)
            assert closed["drawn"] == 0, (lang, width, "the band draws nothing (V5.30 §8)")
        finally:
            context.close()


# ---- final round (label v522-p2-fix; QA_ROUND3 m1, m2, m6) ------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_vivre_s_frame_meets_its_band(browser, site, lang):
    """QA_ROUND3 m1: a paper strip stood between the street frame and the stone band (96 px at 1440, 64 at 768 and 390) —
    the moment and its band read as two blocks with a seam of a third ground. The band now begins at the moment's foot:
    on a desktop at the frame's foot (the lead's plate inside the frame), below 64 rem at the foot of the plate that
    overlaps the frame — on the band's own stone, the moment's ground."""
    for width, height in ((1440, 900), (1024, 768), (768, 1024), (390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/vivre-en-italie/", wait_until="networkidle")
            out = page.evaluate(
                """() => { const moment = document.querySelector('.vivere-panorama'), band = document.querySelector('.vivere-installer');
                    const frame = document.querySelector('.vivere-panorama__quadro').getBoundingClientRect();
                    const plate = document.querySelector('.vivere-panorama__lastra').getBoundingClientRect();
                    return {gap: band.getBoundingClientRect().top - Math.max(frame.bottom, plate.bottom),
                            onFrame: plate.bottom <= frame.bottom + 0.5,
                            ground: getComputedStyle(moment).backgroundColor, band: getComputedStyle(band).backgroundColor}; }"""
            )
            assert abs(out["gap"]) <= 1, (lang, width, out)
            assert out["onFrame"] == (width >= 1024), (lang, width, out)
            assert out["ground"] == out["band"], (lang, width, "the plate stands on the band's stone", out)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_glossary_row_holds_its_cards_parts_on_shared_lines(browser, site, lang):
    """FINAL MICRO-PASS §6 B2 (V5.20; was QA_ROUND3 m2's subgrid of cards side by side): the register is ONE column of
    definition rows on hairlines, so no row holds another's blank — every term starts on one line and every definition
    on another (from 64 rem the term holds its own column, the definition the second, as a dictionary's page — the
    column's first line the term's, a French fallback's identification caption heading its definition); the rows follow
    one another without overlap; below 64 rem the definition stands under its term."""
    for width, height in ((1440, 900), (1280, 800), (1024, 768), (768, 1024)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
            rows = page.evaluate(
                """() => [...document.querySelectorAll('.lessico__registro .lessico__carta')].map((card) => {
                    const box = card.getBoundingClientRect(), t = card.querySelector('.lessico__termine').getBoundingClientRect();
                    const d = card.querySelector(':scope > .lessico__fonte, :scope > .lessico__definizione').getBoundingClientRect();
                    return {id: card.id, top: box.top, bottom: box.bottom, termStart: document.dir === 'rtl' ? t.right : t.left,
                            defStart: document.dir === 'rtl' ? d.right : d.left, termTop: t.top, defTop: d.top, termBottom: t.bottom,
                            rule: getComputedStyle(card).borderBlockEndWidth}; })"""
            )
            assert len(rows) == 10, (lang, width, rows)
            for a, b in zip(rows, rows[1:]):
                assert b["top"] >= a["bottom"] - 0.5, (lang, width, "one row under another", a, b)
            assert max(r["termStart"] for r in rows) - min(r["termStart"] for r in rows) <= 1, (lang, width, rows)
            assert max(r["defStart"] for r in rows) - min(r["defStart"] for r in rows) <= 1, (lang, width, rows)
            if width >= 1024:
                assert all(abs(r["defTop"] - r["termTop"]) <= 8 and r["defStart"] != r["termStart"] for r in rows), (lang, width, rows)
            else:
                assert all(r["defTop"] >= r["termBottom"] - 0.5 for r in rows), (lang, width, rows)
            assert sum(r["rule"] == "1px" for r in rows) >= 9, (lang, width, "the rows on hairlines", rows)
        finally:
            context.close()



@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_forum_s_drawing_hangs_from_the_title_s_line(browser, site, lang):
    """QA_ROUND3 m6: one throttled desktop load moved the head's drawing 44 px (CLS 0.019): from 64 rem it was centred on
    the head's height, which grows when the rest of the document or a late face arrives after the first paint. It now
    hangs from the title's line, a fixed distance from the head's top, on a block seat (an inline seat stood on a line
    whose descent is the face's): what the head receives after the first paint — here its index's last rows, taken out
    then put back — moves nothing of it, and however little the head holds it stays as tall as its drawing asks."""
    measure = """() => { const head = document.querySelector('.forum-hero').getBoundingClientRect();
        const d = document.querySelector('.forum-hero__disegno').getBoundingClientRect();
        const seat = document.querySelector('.forum-hero__marchio').getBoundingClientRect();
        const title = document.querySelector('.forum-hero__title').getBoundingClientRect();
        return {top: d.top - head.top, title: title.top - head.top, h: d.height, seat: seat.height, w: d.width,
                head: head.height, bottom: head.bottom - d.bottom}; }"""
    late = """(back) => { const list = document.querySelector('.forum-localnav .sommaire__list');
        if (back) { for (const li of window.__rows) list.append(li); return; }
        window.__rows = [...list.children].slice(2); for (const li of window.__rows) li.remove(); }"""
    for width, height in ((1920, 1080), (1440, 900), (1280, 800), (1024, 768)):
        context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
            whole = page.evaluate(measure)
            assert abs(whole["top"] - whole["title"]) <= 1, (lang, width, whole)
            assert abs(whole["h"] - whole["w"]) <= 1 and abs(whole["seat"] - whole["w"]) <= 1, (lang, width, whole)
            assert whole["bottom"] >= 47, (lang, width, "the drawing inside its head", whole)
            page.evaluate(late, False)
            partial = page.evaluate(measure)
            page.evaluate(late, True)
            again = page.evaluate(measure)
            assert abs(partial["top"] - whole["top"]) <= 0.5 and abs(again["top"] - whole["top"]) <= 0.5, (
                lang,
                width,
                whole,
                partial,
                again,
            )
            assert partial["bottom"] >= 47, (lang, width, "the drawing never cut by its head's edge", partial)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_register_s_cards_stay_inside_a_narrow_phone(browser, site, lang):
    """Found by the final round's own sweep: below 400 px the register's one column took its widest card's min-content
    («Ricongiungimento» at the band size beside a letter's room), wider than the band — at 320 px the cards ran 45 px
    past the viewport's edge, the drawn letter cut. The column is the band's width, a 360 px phone keeps the word whole,
    and a word longer than a 320 px line breaks inside its card; no card leaves the screen, no term runs under its
    letter."""
    for width, height in ((320, 640), (360, 780), (375, 812)):
        context = browser.new_context(viewport={"width": width, "height": height}, is_mobile=True, has_touch=True)
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
            out = page.evaluate(
                """() => { const cw = document.documentElement.clientWidth, rtl = document.dir === 'rtl', cards = [];
                    for (const card of document.querySelectorAll('.lessico__registro .lessico__carta')) {
                      const box = card.getBoundingClientRect(), letter = card.querySelector('.lessico__lettera');
                      const words = document.createRange(); words.selectNodeContents(card.querySelector('.lessico__termine'));
                      const runs = [...words.getClientRects()];
                      let above = true;
                      if (letter) { const lb = letter.getBoundingClientRect(); above = lb.bottom <= Math.min(...runs.map((r) => r.top)) + 0.5; }
                      const text = card.querySelector('.lessico__termine a').firstChild, word = document.createRange();
                      word.setStart(text, 0); word.setEnd(text, text.data.split(' ')[0].length);
                      cards.push({id: card.id, inside: box.left >= -0.5 && box.right <= cw + 0.5, above,
                                  whole: new Set([...word.getClientRects()].map((r) => Math.round(r.top))).size === 1}); }
                    return cards; }"""
            )
            assert all(card["inside"] for card in out), (lang, width, out)
            # FINAL MICRO-PASS §6 B2 (V5.20; the outlined letter stood beside the term, «room» its distance): the letter is
            # a heading above its first term — no term runs under it (stronger: never beside it either)
            assert all(card["above"] for card in out), (lang, width, out)
            if width >= 360:
                word = next(card for card in out if card["id"] == "ricongiungimento_familiare")
                assert word["whole"], (lang, width, "«Ricongiungimento» whole on its line", word)
        finally:
            context.close()


# ---- final improve round (label v522-p2-final-improve; v522-p2-final-qa1 m1, m2, m3) ----------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_card_under_the_hand_keeps_its_row_and_the_rail_lights_every_letter(browser, site, lang):
    """v522-p2-final-qa1 m1: lane S's sezioni/spia.js makes one stop of the parts whose rendered tops are under 2 px apart,
    and the library's plate lifted 2 px under the hand — the card under a resting pointer left its row, and a mouse
    reader's read-through never lit that row's first letters (C, L, P and Q at 1440; P and R at 768). A dictionary card
    answers the hand in place (its letter fills, its rule runs, its shadow deepens): under the hand it stays on its row,
    and a read-through with the pointer resting on the register lights every letter of the rail."""
    lit = """() => [...document.querySelectorAll('.lessico .az-index__link')].filter((a) => a.hasAttribute('aria-current')
        || a.hasAttribute('data-spia-con')).map((a) => a.hash)"""
    for width, height in ((1440, 900), (768, 1024)):
        context = browser.new_context(viewport={"width": width, "height": height})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
            letters = set(
                page.evaluate("() => [...document.querySelectorAll('.lessico .az-index__link')].map((a) => a.hash)")
            )
            assert len(letters) >= 5, (lang, width, letters)
            # FINAL MICRO-PASS §6 B2 (V5.20; the cards stood side by side, «its row» the cards' row): a definition row
            # under the hand stays where it stands — it lifts, grows and shifts nothing.
            # RESTATED under V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 3: the search seated 32 px
            # under the lead moved the register down; at 1440 in Arabic the first card's foot now enters the page's 8 px
            # end scroll-padding, and Playwright's hover scrolls the page 2 px to bring it in — the card itself never
            # moves, measured with the pointer moved by hand; DL54-210): a row's place is read in the document, its top
            # plus the page's scroll — a card that lifts, grows or shifts still moves it, a scroll into view does not
            where = "() => [...document.querySelectorAll('.lessico__registro .lessico__carta')].slice(0, 2).map((c) => c.getBoundingClientRect().top + scrollY)"
            before = page.evaluate(where)
            page.locator(".lessico__registro .lessico__carta").first.hover()
            page.wait_for_timeout(400)
            tops = page.evaluate(where)
            assert all(abs(a - b) < 0.5 for a, b in zip(before, tops)), (lang, width, "the row under the hand stays", before, tops)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            page.mouse.move(int(width * (0.22 if lang == "ar" else 0.78)), height // 2)
            seen = set()
            for _ in range(80):
                page.mouse.wheel(0, 70)
                page.wait_for_timeout(120)
                seen |= set(page.evaluate(lit))
            assert seen == letters, (lang, width, sorted(letters - seen))
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_agami_s_identity_band_plays_its_signature_in_view_at_load(browser, site, lang):
    """v522-p2-final-qa1 m2 (SECTION_SYSTEM_V2 §3.17 AG-1: «the plate is revealed from the reading edge (MASK, 900 ms)»): at
    1440 and 390 the band stands in view at load, so the section runtime writes it no state and it was drawn at rest — its
    signature never played. In view at load it plays in the head's own sequence and every animation ends; under reduced
    motion the band stands at rest, nothing running.
    V5.30 §8 (the owner's final art direction, an approved decision; strict rule V5.20): the plate holds the role panel, no
    longer a colonnade — its signature is the plate's mask alone (no line left to draw: no sez-stroke), and the assertion
    that the drawing was mirrored on the Arabic page becomes a stronger one: NOTHING of AGAMI's is mirrored — the official
    logo in the head and the seal on the identification plate stand unflipped in both languages (the ribbon's national
    colours are never mirrored: V5.29, the owner's correction of 6 Nov 13:12)."""
    band = """() => { const anims = document.getAnimations().filter((a) => a.effect && a.effect.target
                  && a.effect.target.closest && a.effect.target.closest('.agami-identita'));
        const flips = [...document.querySelectorAll('.agami-insegna, .agami-insegna img, .agami-id__sigillo, .agami-id__sigillo img')]
            .map((e) => getComputedStyle(e)).filter((cs) => cs.scale !== 'none' || cs.transform !== 'none').length;
        return {state: document.querySelector('.agami-identita').dataset.secState || null,
                names: [...new Set(anims.map((a) => a.animationName))].sort(), running: anims.length, flips,
                marks: document.querySelectorAll('.agami-insegna img, .agami-id__sigillo img').length}; }"""
    for width, height in ((1440, 900), (390, 844)):
        for motion in ("no-preference", "reduce"):
            context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion=motion)
            try:
                page = context.new_page()
                page.goto(f"{site}/{lang}/agami/", wait_until="domcontentloaded")
                first = page.evaluate(band)
                assert first["state"] is None, (lang, width, "the band is in view at load", first)
                assert first["marks"] == 2 and first["flips"] == 0, (lang, width, "the marks drawn unflipped", first)
                if motion == "reduce":
                    assert first["names"] == [], (lang, width, "at rest under reduced motion", first)
                    continue
                assert "sez-mask" in first["names"] and "sez-stroke" not in first["names"], (lang, width, first)
                page.wait_for_function(f"() => ({band})().running === 0", timeout=6000)
            finally:
                context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_v2_disclosure_s_rows_never_wait_for_the_legacy_rise(browser, site, lang):
    """v522-p2-final-qa1 m3 (§1 rule 3: the words never wait; the owner's §17: no translateY + opacity as a section's
    motion): AGAMI's question and the term page's related terms are rows of the system's accordion, which
    static/js/src/rise.js still holds below the fold (`data-rise`, until S-close removes the legacy rise) — they stood at
    opacity 0, 18 px low, until they entered. In these V2 sections a row the rise holds stands at rest: opacity 1, in its
    place, before it enters and after. FINAL MICRO-PASS §6 B1: the FAQ's questions became the same system's rows, and
    stand at rest too (a permalink's row held 18 px low landed behind the letterhead)."""
    rows = """(sel) => [...document.querySelectorAll(sel)].map((row) => { const cs = getComputedStyle(row);
        return {rise: row.dataset.rise === undefined ? null : row.dataset.rise, opacity: cs.opacity, translate: cs.translate}; })"""
    for path, sel in (
        ("agami/", ".agami-identita .accordion > details"),
        ("glossaire/nulla_osta/", ".scheda .accordion > details"),
        ("faq/", ".faq-lista > details"),
    ):
        for width, height in ((1440, 900), (390, 844)):
            context = browser.new_context(viewport={"width": width, "height": height})
            try:
                page = context.new_page()
                page.goto(f"{site}/{lang}/{path}", wait_until="networkidle")
                page.wait_for_timeout(600)
                out = page.evaluate(rows, sel)
                assert out, (lang, path, width, sel)
                if width == 390:
                    assert any(row["rise"] == "" for row in out), (
                        lang,
                        path,
                        "below the fold the rise holds a row",
                        out,
                    )
                assert all(row["opacity"] == "1" and row["translate"] == "none" for row in out), (
                    lang,
                    path,
                    width,
                    out,
                )
            finally:
                context.close()
