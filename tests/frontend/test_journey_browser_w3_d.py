"""
The journey «La soglia» in the browser — design V5, family W3-D (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 6;
docs/design-v5/QA/v54/w3-d/NOTES.md). What a static test cannot see:

* the dashboard's rail on ONE level at 1440: the nodes' centres on one line, the file in SELECTION standing on
  threshold A (the list's current item), the line travelled to it and no further, mirrored in Arabic — Morocco at
  the reading start;
* the phone's journey: the card (what is true now, «Vous êtes ici») and the disclosure, closed, its summary 44 px and
  more; opened, the list is the spine;
* still at load, and a true still under reduced motion: nothing animates in the workspace — on the dashboard, the case
  file and «Ma situation»;
* the case file's journey is the spine at every width, its latest timeline event lit;
* «Ma situation»'s Stepper: the spine at the start of the row, a level row of nodes on a phone with the line between
  them;
* forced colours: the nodes and the line in system colours, the wash dropped.

Chromium on the test database; a session minted with ``Client.force_login`` — nothing typed, no password used. The
first console page of a session carries the loader's entrance release (W1-D): each test loads its page twice.
"""

from __future__ import annotations

import os

import pytest
from django.conf import settings
from django.test import Client

from accounts import roles
from accounts.models import AccountType
from core import clock

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DASHBOARD = "/{lang}/espace-reserve/"
SITUATION = "/{lang}/espace-reserve/ma-situation/"

#: The journey as the page draws it: the list, its exposed items, its nodes, the card, the disclosure, what moves.
RAIL_JS = """() => {
  const ws = document.querySelector('.console__workspace');
  const ol = document.querySelector('ol.journey');
  const seen = (el) => !!el && el.checkVisibility({visibilityProperty: true, contentVisibilityAuto: true}) && el.getBoundingClientRect().width > 0;
  const centre = (el) => { const r = el.getBoundingClientRect(); return [(r.left + r.right) / 2, (r.top + r.bottom) / 2]; };
  const steps = [...ol.querySelectorAll(':scope > .journey__step')];
  const nodes = [...ol.querySelectorAll('.journey__node')].filter(seen).map(centre);
  const current = ol.querySelector('[aria-current="step"]');
  const fold = document.querySelector('.journey-fold');
  const summary = fold ? fold.querySelector('summary') : null;
  const line = (li) => getComputedStyle(li, '::before').backgroundColor;
  return {
    laidOut: seen(ol),
    exposed: [...ol.children].filter((li) => li.getAttribute('aria-hidden') !== 'true').length,
    currentClass: current ? current.className : null,
    ys: nodes.map((n) => n[1]), xs: nodes.map((n) => n[0]),
    stepXs: steps.map((li) => centre(li.querySelector('.journey__node'))[0]),
    lines: steps.map(line), travelled: getComputedStyle(document.documentElement).getPropertyValue('--journey-line-travelled').trim(),
    cardShown: seen(document.querySelector('.journey-now')), cardText: (document.querySelector('.journey-now') || {}).innerText || '',
    open: fold ? fold.open : null, summaryShown: seen(summary), summaryH: summary ? summary.getBoundingClientRect().height : null,
    shadows: [...ol.querySelectorAll('*')].map((el) => getComputedStyle(el).boxShadow).filter((v) => v && v !== 'none'),
    moving: document.getAnimations().filter((a) => a.effect && a.effect.target && ws.contains(a.effect.target)).map((a) => a.animationName || a.transitionProperty || 'waapi'),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}"""


#: How far the stretch each item draws stops from the next item's node centre, along the line (0: the line is whole).
#: `sel` names the items, `node` their node; `axis` "y" (a spine) or "x" (a level row); the last item draws none.
GAPS_JS = """([sel, node, axis]) => {
  const items = [...document.querySelectorAll(sel)];
  const rtl = getComputedStyle(document.documentElement).direction === 'rtl';
  const centre = (el) => { const r = el.getBoundingClientRect(); return axis === 'y' ? (r.top + r.bottom) / 2 : (r.left + r.right) / 2; };
  const out = [];
  for (let i = 0; i < items.length - 1; i++) {
    const li = items[i], b = getComputedStyle(li, '::before'), r = li.getBoundingClientRect();
    if (b.display === 'none' || b.content === 'none') { out.push(null); continue; }
    const next = items[i + 1].querySelector(node) || items[i + 1];
    let end;
    if (axis === 'y') end = r.top + parseFloat(b.top) + parseFloat(b.height);
    else end = rtl ? r.right - parseFloat(b.right) - parseFloat(b.width) : r.left + parseFloat(b.left) + parseFloat(b.width);
    out.push(Math.round(Math.abs(end - centre(next)) * 10) / 10);
  }
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


def _person(user_factory, email, status=None):
    from cases.models import CaseFile, CasePurpose
    from cases.services import open_case

    person = user_factory(
        email,
        role=roles.PERSON,
        full_name="Personne SOGLIA",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    if status:
        CaseFile.objects.filter(pk=case.pk).update(status=status, status_since=clock.now())
        case.refresh_from_db()
    return person, case


def _page(browser, live_server, user, path, lang, width, height, phone=False, reduced=False, forced=False):
    client = Client()
    client.force_login(user)
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
    if phone:
        options.update(is_mobile=True, has_touch=True)
    if reduced:
        options["reduced_motion"] = "reduce"
    if forced:
        options["forced_colors"] = "active"
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
    page = context.new_page()
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    url = live_server.url + path.format(lang=lang)
    page.goto(url, wait_until="load")  # the first console page of the session plays the entrance release
    page.goto(url, wait_until="load")
    return context, page, errors


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_dashboard_rail_stands_on_one_level_on_threshold_a_and_mirrors_in_arabic(
    browser, live_server, user_factory, lang
):
    person, _case = _person(user_factory, f"soglia.level.{lang}@example.test", "selection")
    context, page, errors = _page(browser, live_server, person, DASHBOARD, lang, 1440, 900)
    try:
        rail = page.evaluate(RAIL_JS)
        assert rail["laidOut"] and not rail["cardShown"] and not rail["summaryShown"], rail
        assert rail["exposed"] == 8 and "journey__threshold--current" in rail["currentClass"], rail
        assert max(rail["ys"]) - min(rail["ys"]) <= 1, f"the nodes on one level: {rail['ys']}"
        first, last = rail["stepXs"][0], rail["stepXs"][-1]
        assert (first > last) if lang == "ar" else (first < last), "Morocco at the reading start"
        # the line travelled from the first step to the threshold the file stands on, and no further
        travelled = rail["lines"][0]
        assert rail["lines"][:3] == [travelled] * 3 and travelled not in rail["lines"][3:], rail["lines"]
        assert rail["shadows"] == [], "the current node's wash is a disc, not a shadow"
        assert rail["moving"] == [] and rail["overflow"] == 0 and errors == [], rail
        # the shores are the line's two ends: the last stretch runs on from step 7 to the rail's far end, under «Italie»
        ends = page.evaluate(
            """() => { const ol = document.querySelector('ol.journey'), li = ol.querySelector('.journey__step--7');
              const rtl = getComputedStyle(ol).direction === 'rtl', b = getComputedStyle(li, '::before');
              const r = li.getBoundingClientRect(), o = ol.getBoundingClientRect();
              const end = rtl ? r.right - parseFloat(b.right) - parseFloat(b.width) : r.left + parseFloat(b.left) + parseFloat(b.width);
              const shore = ol.querySelector('.journey__shore--end').getBoundingClientRect();
              return {shown: b.display !== 'none', gap: Math.abs(end - (rtl ? o.left : o.right)),
                      shoreGap: Math.abs((rtl ? shore.left : shore.right) - (rtl ? o.left : o.right))}; }"""
        )
        assert ends["shown"] and ends["gap"] <= 1 and ends["shoreGap"] <= 1, ends
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_on_a_phone_the_journey_is_a_card_and_a_disclosure_that_opens_onto_the_spine(
    browser, live_server, user_factory, lang
):
    person, _case = _person(user_factory, f"soglia.phone.{lang}@example.test", "oriented")
    context, page, errors = _page(browser, live_server, person, DASHBOARD, lang, 390, 844, phone=True)
    try:
        rail = page.evaluate(RAIL_JS)
        assert rail["cardShown"] and rail["open"] is False and rail["summaryShown"], rail
        assert rail["summaryH"] >= 44, rail["summaryH"]
        assert not rail["laidOut"], "behind the closed disclosure the list is not laid out"
        page.locator(".journey-fold__summary").click()
        opened = page.evaluate(RAIL_JS)
        assert opened["open"] and opened["laidOut"] and opened["exposed"] == 7, opened
        assert max(opened["xs"]) - min(opened["xs"]) <= 1, f"the spine: one column of nodes {opened['xs']}"
        assert opened["ys"] == sorted(opened["ys"]), "in the list's order, down"
        assert opened["moving"] == [] and opened["overflow"] == 0 and errors == [], opened
    finally:
        context.close()


@pytest.mark.parametrize("reduced", [False, True], ids=["motion", "reduced"])
def test_nothing_moves_at_load_on_the_journeys_three_pages(browser, live_server, user_factory, reduced):
    person, case = _person(user_factory, f"soglia.still.{int(reduced)}@example.test", "selection")
    for path in (DASHBOARD, f"/{{lang}}/espace-reserve/dossiers/{case.reference}/", SITUATION):
        context, page, errors = _page(browser, live_server, person, path, "fr", 1440, 900, reduced=reduced)
        try:
            moving = page.evaluate(
                """() => { const ws = document.querySelector('.console__workspace');
                  return document.getAnimations().filter((a) => a.effect && a.effect.target && ws.contains(a.effect.target)
                    && (a.effect.target.closest('.journey-rail, .tl, .wstep, .wiz'))).map((a) => a.animationName || a.transitionProperty); }"""
            )
            assert moving == [], (path, moving)
            assert errors == [], (path, errors)
        finally:
            context.close()


def test_the_case_file_journey_is_the_spine_and_its_latest_event_is_lit(browser, live_server, user_factory):
    person, case = _person(user_factory, "soglia.case@example.test", "training")
    context, page, errors = _page(
        browser, live_server, person, f"/{{lang}}/espace-reserve/dossiers/{case.reference}/", "fr", 1440, 900
    )
    try:
        drawn = page.evaluate(
            """() => { const ol = document.querySelector('ol.journey--descriptive');
              const xs = [...ol.querySelectorAll('.journey__node')].map((n) => Math.round(n.getBoundingClientRect().left));
              const last = document.querySelector('.tl__row--latest .tl__node');
              return {xs, current: ol.querySelector('[aria-current="step"]').className,
                      ring: last ? getComputedStyle(last, '::after').borderTopWidth : null,
                      halo: last ? getComputedStyle(last, '::before').display : null}; }"""
        )
        assert max(drawn["xs"]) - min(drawn["xs"]) <= 1, drawn
        assert "journey__step--3" in drawn["current"], drawn
        assert drawn["ring"] == "2px" and drawn["halo"] == "block", "the latest event: the ring on its wash"
        first = page.evaluate("() => document.querySelector('.tl > li').classList.contains('tl__row--latest')")
        assert first, "newest first: the lit event heads the timeline"
        gaps = page.evaluate(GAPS_JS, [".journey--descriptive > .journey__step", ".journey__node", "y"])
        assert all(gap is not None and gap <= 1.5 for gap in gaps[:2]), f"the line from node to node: {gaps}"
        assert errors == []
    finally:
        context.close()


@pytest.mark.parametrize(
    ("width", "height", "phone", "orientation"), [(1440, 900, False, "spine"), (390, 844, True, "level")]
)
def test_ma_situations_stepper_is_the_rail_a_spine_or_a_level_row(
    browser, live_server, user_factory, width, height, phone, orientation
):
    person, _case = _person(user_factory, f"soglia.situation.{width}@example.test")
    context, page, errors = _page(browser, live_server, person, SITUATION, "fr", width, height, phone=phone)
    try:
        drawn = page.evaluate(
            """() => { const items = [...document.querySelectorAll('.wstep__item')];
              const nodes = items.map((li) => { const r = li.querySelector('.wstep__node').getBoundingClientRect(); return [(r.left + r.right) / 2, (r.top + r.bottom) / 2]; });
              return {xs: nodes.map((n) => n[0]), ys: nodes.map((n) => n[1]),
                      lines: items.map((li) => getComputedStyle(li, '::before').display),
                      current: document.querySelectorAll('.wstep__item--current').length,
                      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
        )
        spread = (
            (max(drawn["xs"]) - min(drawn["xs"])) if orientation == "spine" else (max(drawn["ys"]) - min(drawn["ys"]))
        )
        assert spread <= 1, (orientation, drawn)
        assert drawn["lines"][:-1] == ["block"] * (len(drawn["lines"]) - 1) and drawn["lines"][-1] == "none", drawn
        assert drawn["current"] == 1 and drawn["overflow"] == 0 and errors == [], drawn
        gaps = page.evaluate(GAPS_JS, [".wstep__item", ".wstep__node", "y" if orientation == "spine" else "x"])
        assert all(gap is not None and gap <= 1.5 for gap in gaps), f"the line from node to node: {gaps}"
        # the line is a drawing: a tap on it, just past a node, lands on the question's link (pointer-events: none)
        hits = page.evaluate(
            """(axis) => [...document.querySelectorAll('.wstep__item')].slice(0, -1).map((li) => {
                const n = li.querySelector('.wstep__node').getBoundingClientRect();
                const rtl = getComputedStyle(li).direction === 'rtl';
                const x = axis === 'y' ? (n.left + n.right) / 2 : (rtl ? n.left - 4 : n.right + 4);
                const y = axis === 'y' ? n.bottom + 4 : (n.top + n.bottom) / 2;
                const el = document.elementFromPoint(x, y);
                return !!(el && el.closest('a.wstep__link')); })""",
            "y" if orientation == "spine" else "x",
        )
        assert hits and all(hits), f"a tap on the line selects its question: {hits}"
    finally:
        context.close()


@pytest.mark.parametrize(("width", "height", "phone"), [(1440, 900, False), (390, 844, True)], ids=["level", "card"])
def test_mon_parcours_draws_the_dashboards_journey_at_its_head(
    browser, live_server, user_factory, width, height, phone
):
    person, _case = _person(user_factory, f"soglia.parcours.{width}@example.test", "selection")
    context, page, errors = _page(
        browser, live_server, person, "/{lang}/espace-reserve/mon-parcours/", "fr", width, height, phone=phone
    )
    try:
        rail = page.evaluate(RAIL_JS)
        if phone:
            assert rail["cardShown"] and rail["summaryShown"] and not rail["laidOut"], rail
            assert "Autorités compétentes" in rail["cardText"], "on a threshold the card says where that phase sits"
        else:
            assert rail["laidOut"] and not rail["cardShown"] and rail["exposed"] == 8, rail
            assert max(rail["ys"]) - min(rail["ys"]) <= 1, rail["ys"]
        assert rail["moving"] == [] and rail["overflow"] == 0 and errors == [], rail
    finally:
        context.close()


def test_forced_colours_draw_the_nodes_and_the_line_in_system_colours(browser, live_server, user_factory):
    person, _case = _person(user_factory, "soglia.forced@example.test", "training")
    context, page, errors = _page(browser, live_server, person, DASHBOARD, "fr", 1440, 900, forced=True)
    try:
        drawn = page.evaluate(
            """() => { const done = document.querySelector('.journey__step--done > .journey__node');
              const now = document.querySelector('.journey__step--current > .journey__node');
              return {dot: getComputedStyle(done, '::after').backgroundColor, ring: getComputedStyle(now, '::after').borderTopColor,
                      halo: getComputedStyle(now, '::before').display,
                      line: getComputedStyle(document.querySelector('.journey__step--done'), '::before').backgroundColor}; }"""
        )
        assert drawn["halo"] == "none", "the wash is dropped"
        assert drawn["dot"] not in ("rgba(0, 0, 0, 0)", "transparent") and drawn["line"] not in ("rgba(0, 0, 0, 0)",), (
            drawn
        )
        assert drawn["ring"] != drawn["dot"], "the current ring in Highlight, the dots in CanvasText"
        assert errors == []
    finally:
        context.close()
