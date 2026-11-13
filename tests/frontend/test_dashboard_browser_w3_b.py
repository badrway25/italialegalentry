"""
The person's dashboard in the browser — design V5, family W3-B (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 4;
docs/design-v5/QA/v54/w3-b/NOTES.md). What a static test cannot see:

* the one primary is in the first viewport with its piece and its date — at 1920 × 1080, 1440 × 900, 1366 × 657 (a
  1366 × 768 laptop less the browser's bars), 1024 × 768 and on a 390 × 844 phone, in French and in Arabic;
* nothing animates at load in the workspace — V4's journey line drew itself at every visit;
* one raised plane — the NowPanel — and at most two shadow values in the workspace; the corners 8 · 4 · full;
* nothing overflows the page, and in Arabic the NowPanel stands on the reading edge (the right one);
* the company's dashboard (step 2): the same — its one primary in the first viewport at 1440, 1024, 834 (the
  768–1023 band) and 390, fr and ar, one raised plane, nothing moving — and under reduced motion and forced colours;
* the bridge (step 2): no raised plane, no primary — the system knows no next action for an institution or a
  university —, its registers flat, nothing overflowing, fr and ar, 1440 and 390;
* the review fixes: under a finger a list row's link is 44 px with its subject's date tight under it, an empty line's
  link 44 px too; the console's empty state spans the main column again on the pages that draw it.

Chromium on the test database; a session minted with ``Client.force_login`` — nothing typed, no password used. The
first console page of a session carries the loader's entrance release (W1-D): each test loads the page once before
it measures the dashboard at rest.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest
from django.conf import settings
from django.test import Client
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType
from core import clock

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DASHBOARD = "/{lang}/espace-reserve/"

#: V5.15 (the owner's creative override, §20: the platform «must not collapse into static rectangles») gives every console
#: page a FINITE load envelope (lane D's atrium draws, its planes rise; portal/v5/_platform.css): the page is read «at rest»
#: once that envelope has ended. What the guards below still refuse is a motion that never ends — a loop, a scroll-linked
#: timeline — and any motion of the journey on a return (M5), which «moving» keeps catching after the settle.
#: V5.18 (T3): lane A's own load envelope, `c-rise` (the dashboard's and the organisation's blocks rising once, 420 ms,
#: portal/v5/_motion.css), is admitted on the same terms — finite, waited for here, gone once it has ended (it fills
#: backwards only, so an ended rise is no longer listed) and absent under reduced motion (the tests below).
SETTLE_JS = """() => Promise.all(document.getAnimations()
  .filter((a) => {
    const el = a.effect && a.effect.target, t = a.effect && a.effect.getComputedTiming();
    if (!el || !t || !Number.isFinite(t.endTime) || t.endTime > 2500) return false;
    // V5.18 T3: the console's own finite rise (lane A's c-rise) is awaited too — once ended it leaves the list
    if (a.animationName === 'c-rise') return true;
    // lane D's envelope only — the atrium and the platform's planes; never the journey (M5 must stay still on a return)
    return Boolean(el.closest('[data-atrium]') || (el.closest('[data-platform]') && !el.closest('.db-journey, .journey, .journey-now')));
  })
  .map((a) => a.finished.catch(() => null)))"""


def _settle(page):
    # the arrival's veil first (html.lume-in): while it stands, the rise waits on it (--rise-wait), and its end moves
    # the rise's delay — an animation awaited before that would play again after it
    page.wait_for_function("() => !document.documentElement.classList.contains('lume-in')", timeout=5000)
    page.evaluate(SETTLE_JS)


#: What «moving» counts at rest: EVERY animation in the workspace, c-rise included. V5.20 (the strict test-update rule;
#: «animation remaining applied after completion» is a release blocker): V5.18 T3 had let a FINISHED c-rise through,
#: for its `both` fill kept it in getAnimations() — the fill is `backwards` since lane A (portal/v5/_motion.css,
#: v5/_conto-console.css), so an ended rise is gone from the list and one that stays applied after it ends fails here.
MOVING_JS = """(ws) => document.getAnimations().filter((a) => a.effect && a.effect.target && ws.contains(a.effect.target))
  .map((a) => a.animationName || a.transitionProperty || 'waapi')"""


#: What the gate asks, read on the page at rest.
GATE_JS = """() => {
  const vh = innerHeight;
  const ws = document.querySelector('.console__workspace');
  const shown = (el) => { const r = el.getBoundingClientRect(); return r.width > 1 && r.height > 1 && el.checkVisibility({visibilityProperty: true, opacityProperty: true}); };
  const now = document.querySelector('.db-now');
  const primary = [...ws.querySelectorAll('.btn--primary')].filter(shown);
  const title = now.querySelector('.db-now__title');
  const date = now.querySelector('.db-due time');
  const shadows = new Set(); let raised = 0;
  for (const el of ws.querySelectorAll('*')) {
    if (!shown(el)) continue;
    const s = getComputedStyle(el).boxShadow;
    if (s && s !== 'none') { shadows.add(s); if (/\\)[^,]*,\\s*rgba?\\(/.test(s)) raised += 1; }
  }
  const radii = new Set();
  for (const el of ws.querySelectorAll('*')) {
    if (!shown(el)) continue;
    const r = el.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) continue;
    const v = getComputedStyle(el).borderTopLeftRadius;
    // V5.20: a chip counts as the pill by its drawing, as every element does (V5.18 T3 had counted any `.chip` as the
    // pill for the step chip that wrapped on a phone; lane D keeps that chip on one line since — test_terminology_v512_d)
    if (v && v !== '0px') radii.add(parseFloat(v) >= r.height / 2 - 0.5 || parseFloat(v) >= 100 ? 'full' : v);
  }
  const nr = now.getBoundingClientRect(), wr = document.querySelector('.db').getBoundingClientRect();
  return {
    primaries: primary.length, primaryBottom: primary.length ? primary[0].getBoundingClientRect().bottom : null,
    titleBottom: title.getBoundingClientRect().bottom, dateBottom: date ? date.getBoundingClientRect().bottom : null,
    vh, shadows: [...shadows], raised, radii: [...radii],
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    moving: (""" + MOVING_JS + """)(ws),
    nowStart: getComputedStyle(document.documentElement).direction === 'rtl' ? wr.right - nr.right : nr.left - wr.left,
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
def person_with_a_due_piece(db, settings, tmp_path, user_factory):
    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services as documents

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    person = user_factory(
        "dash.browser@example.test",
        role=roles.PERSON,
        full_name="Personne DASHBOARD",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    documents.declare_requirement(
        case,
        code="civil_record",
        title="Acte d’état civil légalisé",
        detail="Traduction assermentée si l’acte n’est pas rédigé dans une langue acceptée.",
        responsible_actor="person",
        due_date=timezone.localdate() + dt.timedelta(days=9),
    )
    documents.declare_requirement(case, code="nulla_osta", title="Nulla osta au travail", responsible_actor="authority")
    return person


def _page(browser, live_server, user, lang, width, height, phone=False, path=DASHBOARD):
    client = Client()
    client.force_login(user)
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
    if phone:
        options.update(is_mobile=True, has_touch=True)
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
    _settle(page)
    return context, page, errors


SIZES = [(1920, 1080, False), (1440, 900, False), (1366, 657, False), (1024, 768, False), (390, 844, True)]


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height", "phone"), SIZES, ids=[f"{w}x{h}" for w, h, _ in SIZES])
def test_the_one_primary_with_its_piece_and_its_date_in_the_first_viewport(
    browser, live_server, person_with_a_due_piece, lang, width, height, phone
):
    context, page, errors = _page(browser, live_server, person_with_a_due_piece, lang, width, height, phone)
    try:
        gate = page.evaluate(GATE_JS)
        assert gate["primaries"] == 1, gate
        assert gate["primaryBottom"] <= gate["vh"], f"the primary below the first viewport: {gate}"
        assert gate["titleBottom"] <= gate["vh"] and gate["dateBottom"] and gate["dateBottom"] <= gate["vh"], gate
        assert gate["overflow"] == 0, gate
        assert gate["moving"] == [], f"nothing animates at load on the dashboard: {gate['moving']}"
        assert gate["raised"] == 1 and len(gate["shadows"]) <= 2, gate
        assert set(gate["radii"]) <= {"4px", "8px", "full"}, gate
        assert abs(gate["nowStart"]) <= 1, "the NowPanel stands on the reading edge"
        assert errors == [], errors
    finally:
        context.close()


def test_without_a_file_the_questionnaire_is_the_primary_on_a_phone(browser, live_server, user_factory):
    person = user_factory("dash.fresh@example.test", role=roles.PERSON, account_type=AccountType.PERSON)
    context, page, errors = _page(browser, live_server, person, "fr", 390, 844, phone=True)
    try:
        assert page.locator('.db-now[data-now="no-case"]').count() == 1
        primary = page.locator(".console__workspace .btn--primary")
        if primary.count():
            box = primary.first.bounding_box()
            assert box["y"] + box["height"] <= 844 - 66, "above the bottom bar"
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") == 0
        assert errors == []
    finally:
        context.close()


def test_under_reduced_motion_and_forced_colours_the_panel_keeps_its_edge(
    browser, live_server, person_with_a_due_piece
):
    context, page, _errors = _page(browser, live_server, person_with_a_due_piece, "fr", 1440, 900)
    try:
        page.emulate_media(reduced_motion="reduce", forced_colors="active")
        page.reload(wait_until="load")
        edge = page.evaluate(
            "(() => { const s = getComputedStyle(document.querySelector('.db-now')); return [s.borderTopStyle, s.borderTopColor]; })()"
        )
        assert edge[0] == "solid" and edge[1] not in ("transparent", "rgba(0, 0, 0, 0)"), (
            f"the raised plane keeps an edge when the forced palette drops its shadow: {edge}"
        )
        assert page.evaluate("document.getAnimations().length") == 0
    finally:
        context.close()


# ---- step 2: the company's dashboard and the bridge ----------------------------------------------------------------
COMPANY_DASHBOARD = "/{lang}/espace-reserve/entreprise/"

#: The bridge at rest: no NowPanel, no primary, no raised plane; its registers, in the DOM's order.
BRIDGE_JS = """() => {
  const ws = document.querySelector('.console__workspace');
  const shown = (el) => { const r = el.getBoundingClientRect(); return r.width > 1 && r.height > 1 && el.checkVisibility({visibilityProperty: true, opacityProperty: true}); };
  const shadows = new Set();
  for (const el of ws.querySelectorAll('*')) { if (!shown(el)) continue; const s = getComputedStyle(el).boxShadow; if (s && s !== 'none') shadows.add(s); }
  return {
    now: !!ws.querySelector('.db-now'), primaries: [...ws.querySelectorAll('.btn--primary')].filter(shown).length,
    shadows: [...shadows], sections: [...ws.querySelectorAll('[data-card]')].filter(shown).map((e) => e.dataset.card),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    moving: (""" + MOVING_JS + """)(ws).length,
    offEdge: [...ws.querySelectorAll('.db-list__row > .db-list__title')].filter(shown).filter((t) => {
      const r = t.getBoundingClientRect(), row = t.parentElement.getBoundingClientRect();
      return getComputedStyle(document.documentElement).direction === 'rtl' ? row.right - r.right > 1 : r.left - row.left > 1;
    }).map((t) => t.textContent.trim()),
  };
}"""


@pytest.fixture
def company_with_a_draft(db, user_factory):
    from accounts.models import (
        AccountVerification,
        Membership,
        MembershipRole,
        Organisation,
        OrganisationKind,
        VerificationStatus,
    )
    from companies.models import CompanyNeed, CompanyProfile, NeedSkill, Sector, SkillLevel, Territory

    user = user_factory("dash.company.browser@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    organisation = Organisation.objects.create(
        name="Organisation navigateur", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    AccountVerification.objects.create(
        user=user, declared_type=AccountType.COMPANY, status=VerificationStatus.APPROVED, decided_at=timezone.now()
    )
    sector, _created = Sector.objects.get_or_create(
        code="batiment", defaults={"label_fr": "Bâtiment et travaux publics", "order": 10}
    )
    territory, _created = Territory.objects.get_or_create(
        code="veneto", defaults={"label_fr": "Vénétie", "country": "IT", "order": 10}
    )
    company = CompanyProfile.objects.create(
        organisation=organisation,
        legal_name="Cantiere di prova S.r.l.",
        registration_number="RM-PROVA-01",
        sector=sector,
        contact_name="Référent de test",
        contact_function="Responsable des ressources humaines",
        contact_email="referent-prova@example.test",
        city="Rovigo",
        country="IT",
    )
    for title, status in (
        ("Soudure d’assemblage sur charpente métallique", "draft"),
        ("Préparation de commandes en entrepôt frigorifique", "submitted"),
        ("Maintenance des lignes d’embouteillage", "in_progress"),
    ):
        need = CompanyNeed.objects.create(
            company=company,
            title=title,
            territory=territory,
            sector=sector,
            professional_profile="Technicien",
            duties="Entretien des lignes.",
            headcount=2,
            status=status,
        )
        NeedSkill.objects.create(need=need, label="Mécanique industrielle", level=SkillLevel.MANDATORY)
    return user


COMPANY_SIZES = [(1440, 900, False), (1024, 768, False), (834, 1112, False), (390, 844, True)]


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height", "phone"), COMPANY_SIZES, ids=[f"{w}x{h}" for w, h, _ in COMPANY_SIZES])
def test_the_company_dashboards_one_primary_in_the_first_viewport(
    browser, live_server, company_with_a_draft, lang, width, height, phone
):
    context, page, errors = _page(
        browser, live_server, company_with_a_draft, lang, width, height, phone, path=COMPANY_DASHBOARD
    )
    try:
        gate = page.evaluate(GATE_JS)
        assert gate["primaries"] == 1, gate
        assert gate["primaryBottom"] <= gate["vh"] and gate["titleBottom"] <= gate["vh"], gate
        assert gate["overflow"] == 0, gate
        assert gate["moving"] == [], f"nothing animates at load on the dashboard: {gate['moving']}"
        assert gate["raised"] == 1 and len(gate["shadows"]) <= 2, gate
        assert set(gate["radii"]) <= {"4px", "8px", "full"}, gate
        assert abs(gate["nowStart"]) <= 1, "the NowPanel stands on the reading edge"
        needs = page.evaluate("[...document.querySelectorAll('[data-need]')].map((e) => e.dataset.need)")
        assert len(needs) == 3 and len(set(needs)) == 3, "the NowPanel's need is drawn there and only there"
        assert errors == [], errors
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(
    ("width", "height", "phone"), [(1440, 900, False), (390, 844, True)], ids=["1440x900", "390x844"]
)
def test_the_reserved_area_draws_the_companys_act_and_its_way_in_the_first_viewport(
    browser, live_server, company_with_a_draft, lang, width, height, phone
):
    """V5.32 correction round, the integration review's P1-4: «Espace réservé» said «Aucune action ne vous est
    demandée» while «Espace entreprise» opened on «Transmettez le besoin … au projet». The reserved area draws the
    company's act — the need's title — in the company's NowPanel, on the reading edge, whose ONE primary leads to
    «Espace entreprise», in the first viewport; no calm panel; one raised plane; nothing moves, nothing overflows."""
    context, page, errors = _page(browser, live_server, company_with_a_draft, lang, width, height, phone)
    try:
        gate = page.evaluate(GATE_JS)
        assert gate["primaries"] == 1, gate
        assert gate["primaryBottom"] <= gate["vh"] and gate["titleBottom"] <= gate["vh"], gate
        assert gate["overflow"] == 0, gate
        assert gate["moving"] == [], f"nothing animates at load on the dashboard: {gate['moving']}"
        assert gate["raised"] == 1 and len(gate["shadows"]) <= 2, gate
        assert set(gate["radii"]) <= {"4px", "8px", "full"}, gate
        assert abs(gate["nowStart"]) <= 1, "the NowPanel stands on the reading edge"
        reading = page.evaluate(
            """() => ({title: document.querySelector('.db-now__title').textContent,
                      way: document.querySelector('.db-now [data-now-primary]').getAttribute('href'),
                      calm: document.querySelectorAll('.org-calm').length})"""
        )
        assert "Soudure d’assemblage sur charpente métallique" in reading["title"], reading
        assert reading["way"] == f"/{lang}/espace-reserve/entreprise/" and reading["calm"] == 0, reading
        assert errors == [], errors
    finally:
        context.close()


def test_the_company_dashboard_under_reduced_motion_and_forced_colours(browser, live_server, company_with_a_draft):
    context, page, _errors = _page(browser, live_server, company_with_a_draft, "fr", 1440, 900, path=COMPANY_DASHBOARD)
    try:
        page.emulate_media(reduced_motion="reduce", forced_colors="active")
        page.reload(wait_until="load")
        edge = page.evaluate(
            "(() => { const s = getComputedStyle(document.querySelector('.db-now')); return [s.borderTopStyle, s.borderTopColor]; })()"
        )
        assert edge[0] == "solid" and edge[1] not in ("transparent", "rgba(0, 0, 0, 0)"), edge
        assert page.evaluate("document.getAnimations().length") == 0
    finally:
        context.close()


@pytest.fixture
def institution_account(db, user_factory):
    from accounts.models import Membership, Organisation, OrganisationKind
    from portal.models import Deadline, Message

    user = user_factory(
        "dash.institution.browser@example.test", role=roles.INSTITUTION, account_type=AccountType.INSTITUTION
    )
    organisation = Organisation.objects.create(
        name="Institution de test", kind=OrganisationKind.INSTITUTION, country="MA", city="Rabat"
    )
    Membership.objects.create(user=user, organisation=organisation)
    Deadline.objects.create(
        owner=user, title="Convention à transmettre", due_on=timezone.localdate() - dt.timedelta(days=3)
    )
    Message.objects.create(recipient=user, subject="Calendrier des sessions", body="Corps du message.")
    return user


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(
    ("width", "height", "phone"), [(1440, 900, False), (390, 844, True)], ids=["1440x900", "390x844"]
)
def test_the_bridge_has_no_raised_plane_no_primary_and_flat_registers(
    browser, live_server, institution_account, lang, width, height, phone
):
    context, page, errors = _page(browser, live_server, institution_account, lang, width, height, phone)
    try:
        bridge = page.evaluate(BRIDGE_JS)
        assert not bridge["now"] and bridge["primaries"] == 0, bridge
        assert bridge["shadows"] == [], f"no raised plane, no box on the bridge: {bridge['shadows']}"
        # V5.12 Q7 / V5.15 lane D: an institution has its own dashboard (dashboard_organisation.html) — its registers
        # drawn only with rows (D-20: no «… apparaîtront ici» heading over an empty «requests» or «documents»), the date
        # and the communication this account holds, then its organisation's identity sheet
        assert bridge["sections"] == ["deadlines", "messages", "organisation"], bridge
        assert bridge["overflow"] == 0 and bridge["moving"] == 0, bridge
        assert bridge["offEdge"] == [], f"a row's own words on the reading edge, whatever their script: {bridge}"
        assert errors == [], errors
    finally:
        context.close()


#: A finger on the bridge: the list link's height and the air between its subject and its date; an empty line's link.
TOUCH_JS = """() => {
  const row = [...document.querySelectorAll('.db-list__row')].find((r) => r.querySelector('.db-list__link'));
  const link = row.querySelector('.db-list__link'), title = row.querySelector('.db-list__title'), meta = row.querySelector('.db-list__meta');
  return {
    coarse: matchMedia('(pointer: coarse)').matches,
    link: Math.round(link.getBoundingClientRect().height),
    gap: Math.round(meta.getBoundingClientRect().top - title.getBoundingClientRect().bottom),
    empty: [...document.querySelectorAll('.db-empty a')].map((a) => Math.round(a.getBoundingClientRect().height)),
  };
}"""


def test_under_a_finger_a_list_link_is_44_px_with_its_date_tight_under_its_subject(
    browser, live_server, institution_account
):
    """The review's m6 and the check's finding 3: a linked row's words are centred in its 44 px box, so its date stands
    tight under the subject (the box left 24 px under it); a link inside an empty line's sentence is 44 px too."""
    context, page, errors = _page(browser, live_server, institution_account, "fr", 390, 844, phone=True)
    try:
        touch = page.evaluate(TOUCH_JS)
        assert touch["coarse"], touch
        assert touch["link"] >= 44 and touch["gap"] <= 14, touch
        assert all(height >= 44 for height in touch["empty"]), touch
        assert errors == [], errors
    finally:
        context.close()


#: The console's empty registers and the state each one draws (V5.18, lane B — the w3-b ownership crossing of the
#: v515-d merge, settled by name instead of by whichever class the page happens to carry): «Communications» is lane
#: D's calm panel (.reg-calm, the platform's quiet surface: it spans the main column); «Mes demandes» and, since
#: V5.18 P-5, «Mes documents» are lane B's empty-state tile (.empty-state, F1: the page's opening statement, no
#: surface, on the main column's start edge at the reading measure). Each page is held to its own rule.
#: RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (the
#: PLATFORM=READY round, lane E): the console draws ONE empty state — the platform's calm panel
#: (portal/partials/empty.html), the public pages' tile and its doorway arch left the console — so the three registers
#: are held to that one rule, each by name as before: one empty state on the page, on the main column's start edge, and
#: the calm panel spanning the column (the assertions of the calm panel's branch, unchanged).
EMPTY_REGISTERS = [
    ("/{lang}/espace-reserve/communications/", "reg-calm"),
    ("/{lang}/espace-reserve/mes-demandes/", "reg-calm"),
    ("/{lang}/espace-reserve/mes-documents/", "reg-calm"),
]


@pytest.mark.parametrize(("path", "kind"), EMPTY_REGISTERS, ids=["communications", "requests", "documents"])
def test_the_consoles_empty_state_spans_the_main_column(browser, live_server, user_factory, path, kind):
    """The review's M3: an empty console register draws its empty state on the main column's start edge — not the
    centred 42rem box the bridge's clean-up had left it in. Since V5.15 lane D F1 «Communications» draws the platform's
    calm panel (.reg-calm), which spans the column; the registers that draw lane B's empty-state tile keep its rules."""
    person = user_factory("dash.empty@example.test", role=roles.PERSON, account_type=AccountType.PERSON)
    for lang in ("fr", "ar"):
        context, page, errors = _page(browser, live_server, person, lang, 1440, 900, path=path)
        try:
            # V5.15 W3 (lane B, F1; the v515-b merge): the empty state is the page's opening statement, no surface —
            # it stands on the main column's start edge at the reading measure (max-inline-size 40rem), never a
            # centred box; the start edge is the right one in Arabic
            boxes = page.evaluate(
                "(() => { const m = document.querySelector('.portal__main').getBoundingClientRect(),"
                " found = document.querySelectorAll('.portal__main :is(.empty-state, .reg-calm)'), el = found[0],"
                " e = el.getBoundingClientRect(), s = getComputedStyle(el), rtl = document.dir === 'rtl';"
                " return [Math.round(rtl ? m.right : m.left), Math.round(m.width), Math.round(rtl ? e.right : e.left),"
                " Math.round(e.width), s.backgroundColor, s.borderTopWidth, el.classList.contains('reg-calm'),"
                " found.length]; })()"
            )
            assert boxes[7] == 1, (lang, path, "one empty state on the page", boxes)
            assert boxes[6] is (kind == "reg-calm"), (lang, path, f"the register draws its {kind}", boxes)
            assert abs(boxes[0] - boxes[2]) <= 1, (lang, path, "on the main column's start edge", boxes)
            if kind == "reg-calm":
                # the v515-d merge: on «Communications» the empty state is lane D's calm panel (the platform's quiet
                # surface, its drawing and its lead at 38rem inside it) — it spans the main column
                assert abs(boxes[1] - boxes[3]) <= 1, (lang, path, "the calm panel spans the main column", boxes)
            else:
                assert boxes[3] <= boxes[1] and (boxes[3] >= boxes[1] - 1 or boxes[3] <= 640), (lang, path, "the reading measure", boxes)
                assert boxes[4] in ("rgba(0, 0, 0, 0)", "transparent") and boxes[5] == "0px", (lang, path, "no surface", boxes)
            assert errors == [], errors
        finally:
            context.close()
