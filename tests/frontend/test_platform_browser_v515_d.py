"""
The console's page head in the browser — V5.15 lane D's rounds (docs/design-v5/QA/v515/d/NOTES.md), RESTATED under
V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (V5.32 lane E: «no geometry
as filler — arches, arcs, curves, nodes, outlined frames»; «decorative imagery dramatically reduced» on the platform).
The atrium's drawing — its porticoes, route, stations, keyhole, band and their light — left the console; each check of
the drawing is restated as a stronger check of its absence. What a static test cannot see:

* the head draws NOTHING and rests: at the eight review widths, in French and in Arabic, on the dashboard, a register
  and the Guichet (whose head carries its action), the head holds its one h1 and no figure, no band, no ground image,
  no ::before/::after layer and no sheet border; nothing in it moves at rest; the page never scrolls sideways (was:
  no word of the head lies on the drawing; the envelope ends);
* on every family's page, with and without reduced motion, no figure and no light is left in the head (was: at rest
  the drawing is complete and the key's light gone — round 1's major);
* no gold station and no ring is drawn in the dashboard's head; the file's step is the head's chip, in words (was:
  the station's pop and its ring stay on the station — F2);
* the organisation's and the company's heads draw no figure, and the identity sheet's facts never split a word or a
  date (1440, 1280, 1024, 768; fr, en and ar) (was: the seal figure's ink ≥ 60 % of the head — F1/F2);
* the identity plate's seal glyph stands IN its seal, never mirrored, in both directions, and no arcade is drawn
  (was: the glyph in the arcade's central arch — W3 F1);
* kept as they were: the ring's undone segments are hairlines and its count stands in it; the «Présentation»
  disclosure's chevron points down in Arabic as in French; an Academy count takes one focus ring, the cell's.

Chromium on the test database; a session minted with ``Client.force_login`` — nothing typed, no password used.
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

WIDTHS = [(1440, 900), (1280, 800), (1024, 768), (768, 1024), (430, 932), (390, 844), (375, 812), (360, 780)]
PAGES = ["/{lang}/espace-reserve/", "/{lang}/espace-reserve/communications/", "/{lang}/espace-reserve/guichet/"]

SETTLE_JS = """() => Promise.all(document.getAnimations()
  .filter((a) => { const el = a.effect && a.effect.target; const t = a.effect && a.effect.getComputedTiming();
    return el && t && Number.isFinite(t.endTime) && t.endTime <= 2500 && (el.closest('[data-atrium]') || el.closest('[data-platform]')); })
  .map((a) => a.finished.catch(() => null)))"""

ATRIUM_JS = """() => {
  const head = document.querySelector('[data-atrium]');
  if (!head) return null;
  const hs = getComputedStyle(head), before = getComputedStyle(head, '::before'), after = getComputedStyle(head, '::after');
  const drawn = head.querySelectorAll('.atrium__art, .atrium__band, .atrium__svg, .atrium__band-svg, [data-figure]').length;
  return {
    drawn, h1: head.querySelectorAll('h1').length,
    ground: [hs.backgroundImage, before.content, after.content],
    sheet: [parseFloat(hs.borderInlineStartWidth), parseFloat(hs.borderBlockStartWidth), parseFloat(hs.borderBlockEndWidth)],
    moving: document.getAnimations().filter((a) => a.effect && a.effect.target && head.contains(a.effect.target)).length,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
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
def person(db, user_factory):
    from cases.models import CasePurpose
    from cases.services import open_case

    user = user_factory(
        "atrium.browser@example.test",
        role=roles.PERSON,
        full_name="Personne ATRIUM",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    open_case(user, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return user


def _context(browser, live_server, user, width, height, reduced="no-preference"):
    client = Client()
    client.force_login(user)
    phone = width < 768
    context = browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=1,
        reduced_motion=reduced,
        is_mobile=phone,
        has_touch=width < 1024,
    )
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


def _at_rest(page, url):
    page.goto(url, wait_until="load")
    page.evaluate(SETTLE_JS)
    page.wait_for_timeout(50)
    return page.evaluate(ATRIUM_JS)


@pytest.mark.parametrize(("width", "height"), WIDTHS, ids=[f"{w}x{h}" for w, h in WIDTHS])
def test_the_head_draws_nothing_and_rests(browser, live_server, person, width, height):
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
    geometry as filler — arches, arcs, curves, nodes, outlined frames»; «decorative imagery dramatically reduced» on the
    platform): no word could lie on the drawing because there is no drawing any more. Stronger, at every width, in
    French and in Arabic: the head holds its one h1 and no figure, no band, no ground image, no ::before/::after layer,
    no sheet border; nothing in it moves at rest; the page never scrolls sideways."""
    context = _context(browser, live_server, person, width, height)
    try:
        page = context.new_page()
        page.goto(live_server.url + PAGES[0].format(lang="fr"), wait_until="load")  # the session's entrance release
        for lang in ("fr", "ar"):
            for path in PAGES:
                head = _at_rest(page, live_server.url + path.format(lang=lang))
                assert head, f"{path} opens on the product head"
                assert head["drawn"] == 0 and head["h1"] == 1, f"{lang} {path} at {width}: {head}"
                assert head["ground"] == ["none", "none", "none"], f"{lang} {path} at {width}: {head['ground']}"
                assert head["sheet"] == [0, 0, 0], f"{lang} {path} at {width}: on the frame, no sheet, no rule"
                assert head["overflow"] == 0
                assert head["moving"] == 0, "nothing in the head moves at rest"
    finally:
        context.close()


FIGURE_PAGES = [
    "/fr/espace-reserve/",
    "/fr/espace-reserve/communications/",
    "/fr/espace-reserve/guichet/",
    "/fr/espace-reserve/mes-documents/",
    "/fr/espace-reserve/formation/",
]


@pytest.mark.parametrize("reduced", ["no-preference", "reduce"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (1024, 768), (768, 1024)], ids=["1440", "1024", "768"])
def test_at_rest_no_family_head_carries_a_drawing_or_its_light(browser, live_server, person, width, height, reduced):
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
    geometry as filler — arches, arcs, curves, nodes, outlined frames»; «decorative imagery dramatically reduced» on the
    platform): every figure was checked complete at rest, its light gone. Stronger: on every family's page (the route,
    the exchange, the counter, the sheets, the thresholds) the head carries no figure and no light at all, with and
    without reduced motion."""
    context = _context(browser, live_server, person, width, height, reduced)
    try:
        page = context.new_page()
        page.goto(live_server.url + PAGES[0].format(lang="fr"), wait_until="load")
        for path in FIGURE_PAGES:
            head = _at_rest(page, live_server.url + path)
            assert head and head["drawn"] == 0 and head["moving"] == 0, f"{path} at {width}: {head}"
            assert page.evaluate("() => document.querySelectorAll('.atrium__light, .atrium__band-light').length") == 0
    finally:
        context.close()


def test_the_rings_undone_segments_are_hairlines_and_its_count_stands_in_it(browser, live_server, person):
    from cases import services as case_services
    from cases.models import ResponsibleActor

    case = person.case_files.first()
    for n in range(5):
        case_services.add_checklist_item(case, requirement=f"Pièce {n}", responsible_actor=ResponsibleActor.AUTHORITY)
    context = _context(browser, live_server, person, 1440, 900)
    try:
        page = context.new_page()
        url = live_server.url + PAGES[0].format(lang="fr")
        page.goto(url, wait_until="load")
        _at_rest(page, url)
        ring = page.evaluate("""() => ({
          undone: [...document.querySelectorAll('.ring__seg:not(.ring__seg--done)')].map((e) => parseFloat(getComputedStyle(e).strokeWidth)),
          count: (document.querySelector('.ring-dial__count') || {}).textContent,
          centred: (() => { const r = document.querySelector('.ring').getBoundingClientRect(), c = document.querySelector('.ring-dial__count').getBoundingClientRect();
            return Math.abs((r.left + r.width / 2) - (c.left + c.width / 2)) < 2 && Math.abs((r.top + r.height / 2) - (c.top + c.height / 2)) < 2; })(),
        })""")
        assert len(ring["undone"]) == 5 and max(ring["undone"]) <= 2, ring
        assert ring["count"] == "0/5" and ring["centred"], ring
    finally:
        context.close()


@pytest.fixture
def institution(db, user_factory):
    from accounts.models import Membership, Organisation, OrganisationKind

    user = user_factory("atrium.institution@example.test", role=roles.INSTITUTION, account_type=AccountType.INSTITUTION)
    organisation = Organisation.objects.create(name="Comune di prova", kind=OrganisationKind.INSTITUTION, country="IT")
    Membership.objects.create(user=user, organisation=organisation)
    return user


def test_the_presentations_chevron_points_down_in_arabic_as_in_french(browser, live_server, institution):
    """Round 2: the logical inline border flipped in Arabic while the rotation did not — the chevron pointed sideways.
    The L of the two borders has its corner at the inline end; after the pseudo-element's transform that corner must
    point DOWN closed and UP open, in both scripts."""
    corner_js = """() => { const s = getComputedStyle(document.querySelector('.atrium__intro > summary'), '::after');
      const rtl = document.documentElement.dir === 'rtl';
      const w = parseFloat(s.width) / 2, h = parseFloat(s.height) / 2;
      const m = new DOMMatrix(s.transform);
      const o = m.transformPoint(new DOMPoint(0, 0)), c = m.transformPoint(new DOMPoint(rtl ? -w : w, h));
      return [c.x - o.x, c.y - o.y]; }"""
    context = _context(browser, live_server, institution, 768, 1024)
    try:
        page = context.new_page()
        page.goto(live_server.url + "/fr/espace-reserve/", wait_until="load")
        for lang in ("fr", "ar"):
            page.goto(live_server.url + f"/{lang}/espace-reserve/", wait_until="load")
            closed = page.evaluate(corner_js)
            page.click(".atrium__intro > summary")
            opened = page.evaluate(corner_js)
            assert abs(closed[0]) < 0.5 and closed[1] > 0, (lang, "closed: the corner points down", closed)
            assert abs(opened[0]) < 0.5 and opened[1] < 0, (lang, "open: the corner points up", opened)
    finally:
        context.close()


@pytest.fixture
def university(db, user_factory):
    from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind

    user = user_factory("atrium.university@example.test", role=roles.UNIVERSITY, account_type=AccountType.UNIVERSITY)
    organisation = Organisation.objects.create(
        name="Istituto di formazione Collina Verde", kind=OrganisationKind.UNIVERSITY, country="IT", city="Collina Verde"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    return user


@pytest.fixture
def company(db, user_factory):
    from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind

    user = user_factory("atrium.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    organisation = Organisation.objects.create(
        name="Cantiere Adriatico S.r.l.", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    return user


#: Each word of a fact's value is ONE box: a word split across two lines has two client rects.
SPLIT_JS = """() => {
  const split = [];
  for (const dd of document.querySelectorAll('.org-id__fact > dd')) {
    const walker = document.createTreeWalker(dd, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      for (const m of node.data.matchAll(/\\S+/g)) {
        const r = document.createRange(); r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length);
        const lines = new Set([...r.getClientRects()].filter((b) => b.width > 0).map((b) => Math.round(b.top)));
        if (lines.size > 1) split.push(m[0]);
      }
    }
  }
  return {split, facts: document.querySelectorAll('.org-id__fact > dd').length};
}"""


@pytest.mark.parametrize(("width", "height"), [(1440, 900), (1280, 800), (1024, 768), (768, 1024)], ids=["1440", "1280", "1024", "768"])
def test_the_organisation_and_company_heads_fill_their_column_and_no_fact_splits_a_word(
    browser, live_server, institution, university, company, width, height
):
    """F1 (major): «Responsabl|e», «28.10.202|6» in the side card at 1024–1280 (fr, ar); the company's dashboard was not
    guarded at all. RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov
    2026 («no geometry as filler — arches, arcs, curves, nodes, outlined frames»; «decorative imagery dramatically
    reduced» on the platform): the seal figure's share of the head (≥ 0.6) is replaced by: the head draws no figure at
    all."""
    for user in (institution, university, company):
        context = _context(browser, live_server, user, width, height)
        try:
            page = context.new_page()
            page.goto(live_server.url + "/fr/espace-reserve/", wait_until="load")
            for lang in ("fr", "en", "ar"):
                atrium = _at_rest(page, live_server.url + f"/{lang}/espace-reserve/")
                assert atrium["drawn"] == 0, f"{user.email} {lang} at {width}: {atrium}"
                assert atrium["overflow"] == 0
                facts = page.evaluate(SPLIT_JS)
                assert facts["facts"] >= 4, "the identity sheet's facts are drawn"
                assert facts["split"] == [], f"{user.email} {lang} at {width}: a word split {facts['split']}"
        finally:
            context.close()


def test_an_academy_count_takes_one_focus_ring_the_cells(browser, live_server, person, monkeypatch):
    """F1: keyboard focus drew two rings — the cell's and the shell's outline around the label link."""
    monkeypatch.setattr("academy.services.summary", lambda user: {"ongoing": 2, "completed": 1, "plans": 0})
    context = _context(browser, live_server, person, 1440, 900)
    try:
        page = context.new_page()
        page.goto(live_server.url + "/fr/espace-reserve/formation/", wait_until="load")
        page.evaluate(SETTLE_JS)
        for _ in range(80):
            page.keyboard.press("Tab")
            if page.evaluate("() => document.activeElement.classList.contains('lattice__go')"):
                break
        else:  # pragma: no cover - the counts are drawn (monkeypatched summary)
            pytest.fail("no Academy count reached by the keyboard")
        rings = page.evaluate("""() => { const a = document.activeElement, cell = a.closest('.lattice__cell');
          return {link: getComputedStyle(a).outlineStyle, shadow: getComputedStyle(a).boxShadow,
                  cell: getComputedStyle(cell).outlineStyle}; }""")
        assert rings == {"link": "none", "shadow": "none", "cell": "solid"}, rings
    finally:
        context.close()


SEAL_JS = """() => {
  const seal = document.querySelector('[data-atrium] .atrium__seal');
  const icon = seal && seal.querySelector('svg');
  if (!seal || !icon) return null;
  const c = (r) => [r.left + r.width / 2, r.top + r.height / 2];
  const t = getComputedStyle(icon).transform;
  return {glyph: c(icon.getBoundingClientRect()), seal: c(seal.getBoundingClientRect()),
          a: t === 'none' ? 1 : new DOMMatrix(t).a,
          arch: document.querySelectorAll('[data-atrium] .atrium__arcade, [data-atrium] .atrium__glyph-icon').length};
}"""


@pytest.mark.parametrize(("width", "height"), [(1440, 900), (1024, 768), (768, 1024)], ids=["1440", "1024", "768"])
def test_the_seals_glyph_stands_in_its_seal_in_every_direction(
    browser, live_server, institution, university, company, width, height
):
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
    geometry as filler — arches, arcs, curves, nodes, outlined frames»; «decorative imagery dramatically reduced» on the
    platform): the glyph stood in the central arch of a drawn arcade; the arcade is gone and the seal is the identity
    plate's (where an organisation has one): its glyph centred in it, never mirrored, in both directions — and no arcade
    is drawn."""
    for user in (institution, university, company):
        context = _context(browser, live_server, user, width, height, reduced="reduce")
        try:
            page = context.new_page()
            for lang in ("fr", "ar"):
                page.goto(live_server.url + f"/{lang}/espace-reserve/", wait_until="load")
                seal = page.evaluate(SEAL_JS)
                if seal is None:  # a company's head carries no identity plate (its glyph is its panel's disc)
                    assert user is company, f"{user.email} {lang} at {width}: no seal glyph"
                    continue
                assert seal["arch"] == 0, f"{user.email} {lang} at {width}: an arcade is still drawn"
                dx, dy = seal["glyph"][0] - seal["seal"][0], seal["glyph"][1] - seal["seal"][1]
                assert abs(dx) <= 2 and abs(dy) <= 2, f"{user.email} {lang} at {width}: off its seal by {dx:.1f}, {dy:.1f}"
                assert seal["a"] > 0, f"{user.email} {lang} at {width}: the glyph reads mirrored"
        finally:
            context.close()
