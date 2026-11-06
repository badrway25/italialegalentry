"""
The console's atrium in the browser — V5.15 lane D, round 1 (docs/design-v5/QA/v515/d/NOTES.md «Round 1
improvements»). What a static test cannot see:

* at rest the drawing is COMPLETE: the route's rendered end is the door's centre, the door's right leg and the third
  arch's right leg carry ink, and no gold of the key's light is left on the route — round 1's major: with
  `vector-effect: non-scaling-stroke` Chromium read the dash in screen pixels, not on pathLength, and the arches lost
  their legs, the door stood open, the route stopped short (on every page, in every language, under reduced motion);
* no word of the head ever lies on the drawing — no text box of the head (the h1, the eyebrow, the lead, the meta row,
  a chip, the action) intersects the arcade, the door, the route or its stations — at the eight review widths, in
  French and in Arabic, on the dashboard, a register and the Guichet (whose head carries its action);
* the envelope ends: after it, nothing of the atrium is still animating.

Round 2 (NOTES.md «Round 2 improvements»):

* the drawing is a FIGURE per family and FILLS its column: from 768 its ink stands at least 60 % of the head's height
  (it was a ~450 × 130 px sketch on a taller head, and an empty wash above a small drawing beside an action); on a
  phone the BAND (the route, its stations, the door) replaces the 6 × 2 rem mark — the checks read whichever is drawn;
* the ring's undone segments are hairlines (a dial, never the activity glyph);
* the «Présentation» disclosure's chevron points down in Arabic as in French (physical borders).

Finishing round F1 (NOTES.md «Finishing round F1»):

* every figure's route ends on its door's threshold (x and y);
* the organisation's and the company's heads fill their column too (ink ≥ 60 % at 768–1440), and the identity
  sheet's facts never split a word or a date (1440, 1280, 1024, 768; fr and ar);
* an Academy count takes one focus ring, the cell's.

Finishing round F2 (NOTES.md «Finishing round F2»):

* the gold station's pop and its ring's answer stay ON the station: the keyframes animate ``scale``, never
  ``transform`` (which replaced the SVG translate and drew them 36 units off, then jumped) — the ring's centre and
  the station's, sampled three times in their beat, are within 1 px of the station's rest centre (1440 and 390,
  fr and ar);
* the Academy count's focus draws no second box (no outline, no box-shadow on the label link);
* the organisation heads' ink is guarded in fr, en and ar.

Finishing round F1 of the W3 finishing pass (NOTES.md «Finishing round F1»):

* the seal's audience glyph stands IN its seal in every language: its box centre within 2 px of the seal ring's centre
  and, in Arabic, read the right way round (the net screen transform is not mirrored) — the F2 review's major: a CSS
  counter-flip on the <use> (fill-box origin resolved without x/y) threw it ~150 units out, an empty seal on the
  university and institution dashboards and a stray gold mark in the company's head (1440, 1024, 768; fr and ar).

Chromium on the test database; a session minted with ``Client.force_login`` — nothing typed, no password used.
"""

from __future__ import annotations

import io
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
  // the drawing that is drawn: the figure from 768, the band on a phone
  const art = head.querySelector('.atrium__art'), band = head.querySelector('.atrium__band');
  const phone = !art.getBoundingClientRect().width;
  const box = (phone ? band : art).getBoundingClientRect();
  const q = (fig, bnd) => head.querySelector(phone ? bnd : fig);
  const shapes = phone
    ? [['band', band.querySelector('svg')]]
    : ['.atrium__arcade', '.atrium__door', '.atrium__route', '.atrium__stations'].map((s) => [s, art.querySelector(s)]);
  const hits = [];
  for (const t of head.querySelectorAll('h1, p, a, button, summary, .chip, .ws-head__action-note')) {
    const a = t.getBoundingClientRect(); if (!a.width || !a.height) continue;
    for (const [n, s] of shapes) { const r = s.getBoundingClientRect();
      // what is drawn is clipped at the drawing's column (the route's lead-in runs on beyond the figure's box)
      const b = {left: Math.max(r.left, box.left), right: Math.min(r.right, box.right), top: Math.max(r.top, box.top), bottom: Math.min(r.bottom, box.bottom)};
      const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left), iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ix > 2 && iy > 2) hits.push([t.tagName, String(t.className), n, Math.round(ix), Math.round(iy)]); }
  }
  const route = q('.atrium__route', '.atrium__band-route'), door = q('.atrium__door', '.atrium__band-door');
  const S = (el, x, y) => { const p = new DOMPoint(x, y).matrixTransform(el.getScreenCTM()); return [p.x, p.y]; };
  const along = (el, f) => { const p = el.getPointAtLength(el.getTotalLength() * f); return S(el, p.x, p.y); };
  const end = along(route, 1);
  const db = door.getBoundingClientRect();
  const dbb = door.getBBox();
  let ink = 0;
  if (!phone) {
    const parts = [...art.querySelectorAll('.atrium__arcade, .atrium__door, .atrium__route')].map((e) => e.getBoundingClientRect());
    ink = Math.max(...parts.map((b) => b.bottom)) - Math.max(box.top, Math.min(...parts.map((b) => b.top)));
  }
  return {
    phone, hits, routeEndVsDoor: end[0] - (db.left + db.width / 2), routeEndVsThreshold: end[1] - db.bottom,
    doorRight: along(door, 0.94), arches: phone ? [] : [...art.querySelectorAll('.atrium__arcade path')].map((e) => along(e, 0.94)),
    blank: S(door, dbb.x + dbb.width / 2, dbb.y - 8),
    inkRatio: ink / head.getBoundingClientRect().height,
    lightOpacity: getComputedStyle(q('.atrium__light', '.atrium__band-light')).opacity,
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
def test_no_word_of_the_head_lies_on_the_drawing(browser, live_server, person, width, height):
    context = _context(browser, live_server, person, width, height)
    try:
        page = context.new_page()
        page.goto(live_server.url + PAGES[0].format(lang="fr"), wait_until="load")  # the session's entrance release
        for lang in ("fr", "ar"):
            for path in PAGES:
                atrium = _at_rest(page, live_server.url + path.format(lang=lang))
                assert atrium, f"{path} opens on the atrium"
                assert atrium["hits"] == [], f"{lang} {path} at {width}: a word on the drawing {atrium['hits']}"
                assert abs(atrium["routeEndVsDoor"]) <= 1.5, f"the route reaches the door: {atrium['routeEndVsDoor']}"
                assert atrium["overflow"] == 0
                assert atrium["moving"] == 0, "the envelope has ended"
                assert atrium["phone"] == (width < 768), "the band on a phone, the figure from 768"
                if width >= 768:
                    assert atrium["inkRatio"] >= 0.6, f"{lang} {path} at {width}: the drawing fills its column"
    finally:
        context.close()


def _ink(png, point, r=3, pick=min):
    """The darkest (or, with ``pick=max``, the lightest) luminance in a small box around a screen point."""
    from PIL import Image

    im = Image.open(io.BytesIO(png)).convert("L")
    x, y = int(round(point[0])), int(round(point[1]))
    return pick(
        im.getpixel((a, b))
        for a in range(max(0, x - r), min(im.width, x + r + 1))
        for b in range(max(0, y - r), min(im.height, y + r + 1))
    )


FIGURE_PAGES = [
    "/fr/espace-reserve/",
    "/fr/espace-reserve/communications/",
    "/fr/espace-reserve/guichet/",
    "/fr/espace-reserve/mes-documents/",
    "/fr/espace-reserve/formation/",
]


@pytest.mark.parametrize("reduced", ["no-preference", "reduce"])
@pytest.mark.parametrize(("width", "height"), [(1440, 900), (1024, 768), (768, 1024)], ids=["1440", "1024", "768"])
def test_at_rest_the_drawing_is_complete_and_the_light_is_gone(browser, live_server, person, width, height, reduced):
    """Every figure (the route, the exchange, the counter, the sheets, the thresholds) complete at rest: the door's
    right leg and every stroke of the arcade carry ink near their end, no gold of the light is left."""
    pytest.importorskip("PIL")
    context = _context(browser, live_server, person, width, height, reduced)
    try:
        page = context.new_page()
        page.goto(live_server.url + PAGES[0].format(lang="fr"), wait_until="load")
        for path in FIGURE_PAGES:
            atrium = _at_rest(page, live_server.url + path)
            png = page.screenshot()
            paper = _ink(png, atrium["blank"], pick=max)
            assert _ink(png, atrium["doorRight"]) < paper - 60, f"{path}: the door is closed, its right leg is drawn"
            for n, point in enumerate(atrium["arches"]):
                assert _ink(png, point) < paper - 12, f"{path}: the arcade's stroke {n} is drawn to its end"
            assert atrium["lightOpacity"] == "0", "no gold of the light is left at rest"
            assert atrium["inkRatio"] >= 0.6, f"{path} at {width}: the drawing fills its column"
            # F1: the route arrives AT the door — on its threshold, not under it (the counter's ended 27–40 px below)
            assert abs(atrium["routeEndVsDoor"]) <= 1.5, f"{path}: {atrium['routeEndVsDoor']}"
            assert abs(atrium["routeEndVsThreshold"]) <= 2, f"{path}: the route ends on the door's threshold"
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
    """F1 (major): «Responsabl|e», «28.10.202|6» in the side card at 1024–1280 (fr, ar); the seal figure at 0.54–0.59
    of the head at 768 and 1024; the company's dashboard was not guarded at all."""
    for user in (institution, university, company):
        context = _context(browser, live_server, user, width, height)
        try:
            page = context.new_page()
            page.goto(live_server.url + "/fr/espace-reserve/", wait_until="load")
            for lang in ("fr", "en", "ar"):
                atrium = _at_rest(page, live_server.url + f"/{lang}/espace-reserve/")
                assert atrium["inkRatio"] >= 0.6, f"{user.email} {lang} at {width}: {atrium['inkRatio']:.2f}"
                assert atrium["hits"] == [] and atrium["overflow"] == 0
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


#: The «here» station and its ring, restarted and paused at three points of their beat: their screen centres.
BEAT_JS = """() => {
  const halo = [...document.querySelectorAll('[data-atrium] .atrium__halo')].find((h) => h.getBoundingClientRect().width > 0);
  if (!halo) return null;
  const here = halo.closest('svg').querySelector('.atrium__station--here');
  const centre = (el) => { const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
  for (const a of document.getAnimations()) a.finish();
  const rest = centre(here);
  const samples = {};
  for (const [name, el] of [['halo', halo], ['here', here]]) {
    el.style.animation = 'none'; el.getBoundingClientRect(); el.style.animation = '';
    const anim = document.getAnimations().find((a) => a.effect && a.effect.target === el);
    if (!anim) { samples[name] = 'no animation'; continue; }
    anim.pause();
    const delay = anim.effect.getTiming().delay, dur = anim.effect.getComputedTiming().duration;
    samples[name] = [0.2, 0.6, 0.9].map((f) => { anim.currentTime = delay + dur * f; return centre(el); });
    anim.finish();
  }
  return {rest, samples};
}"""


@pytest.mark.parametrize(("width", "height"), [(1440, 900), (390, 844)], ids=["1440", "390"])
def test_the_gold_stations_pop_and_its_ring_stay_on_the_station(browser, live_server, person, width, height):
    """F1 (major): plat-pop / plat-halo animated ``transform``, which REPLACES an SVG element's transform attribute:
    every station popped ~36 units from its place and jumped back, the ring answered around station 3 (station 1 on
    the phone's band). Under ``scale`` and a translate on the parent group, the beat stays on the gold station."""
    context = _context(browser, live_server, person, width, height)
    try:
        page = context.new_page()
        page.goto(live_server.url + "/fr/espace-reserve/", wait_until="load")
        for lang in ("fr", "ar"):
            page.goto(live_server.url + f"/{lang}/espace-reserve/", wait_until="load")
            beat = page.evaluate(BEAT_JS)
            assert beat, "the dashboard draws the file's step and its ring"
            for name, points in beat["samples"].items():
                assert isinstance(points, list), f"{lang} {width}: {name}: {points}"
                for x, y in points:
                    assert abs(x - beat["rest"][0]) <= 1 and abs(y - beat["rest"][1]) <= 1, (
                        f"{lang} at {width}: the {name} is drawn at {x:.1f},{y:.1f}, the station rests at {beat['rest']}"
                    )
    finally:
        context.close()


SEAL_JS = """() => {
  const art = document.querySelector('[data-atrium] .atrium__art');
  const use = art && art.querySelector('.atrium__glyph-icon');
  const ring = art && [...art.querySelectorAll('.atrium__arcade path')].find((p) => p.getAttribute('d').startsWith('M160 62'));
  if (!use || !ring) return null;
  const c = (r) => [r.left + r.width / 2, r.top + r.height / 2];
  const g = c(use.getBoundingClientRect()), s = c(ring.getBoundingClientRect()), a = art.getBoundingClientRect();
  return {glyph: g, seal: s, inArt: g[0] >= a.left && g[0] <= a.right, a: use.getScreenCTM().a};
}"""


@pytest.mark.parametrize(("width", "height"), [(1440, 900), (1024, 768), (768, 1024)], ids=["1440", "1024", "768"])
def test_the_seals_glyph_stands_in_its_seal_in_every_direction(
    browser, live_server, institution, university, company, width, height
):
    for user in (institution, university, company):
        context = _context(browser, live_server, user, width, height, reduced="reduce")
        try:
            page = context.new_page()
            for lang in ("fr", "ar"):
                page.goto(live_server.url + f"/{lang}/espace-reserve/", wait_until="load")
                seal = page.evaluate(SEAL_JS)
                assert seal, f"{user.email} {lang} at {width}: no seal glyph"
                dx, dy = seal["glyph"][0] - seal["seal"][0], seal["glyph"][1] - seal["seal"][1]
                assert abs(dx) <= 2 and abs(dy) <= 2, f"{user.email} {lang} at {width}: off its seal by {dx:.1f}, {dy:.1f}"
                assert seal["inArt"], f"{user.email} {lang} at {width}: outside the drawing"
                assert seal["a"] > 0, f"{user.email} {lang} at {width}: the glyph reads mirrored"
        finally:
            context.close()
