"""
The platform's typography in Chromium — V5.24, lane PLAT (FINAL_DELIVERY_V2 §3.7 gate (2)–(3); TYPOGRAPHY_V2 F-3, F-4,
F-7, F-8, §4.2, §4.5; R8: a preserved family — typography only). Headless, on the test database, a session minted with
``Client.force_login`` (nothing typed, no password); no Chromium lock slot (R12). What a static test cannot see:

* the eyebrow AS RENDERED is the label role: Host Grotesk at the role's weight `--w-label` at 12 px (13 on a phone) in French — in
  sentence case since V5.32 lane E (RESTATED under V5.20: «no arbitrary uppercase»), uppercase before; Readex Pro,
  no capitals, 0 tracking, ≥ 14 px in Arabic — the same element, the same class, two scripts;
* the workspace lead stands at or under 29 rem (464 px) wherever the column allows it (F-8);
* the atrium's title: 28 → 36 px at `--w-title`, tracked −0.016 em in French and 0 in Arabic, its Arabic leading opened by 0.1;
* the figures and markers (the ring's count, the next date, the organisation's tile indices) in the sans at `--w-title`; the
  references in ILE Mono (R8 «refs stay in the mono»);
* no Arabic letters under 14 px, no multi-line Arabic element under 1.3 em of leading, no Arabic drawn by ILE Mono, every
  lang="fr" run of 20 px or more at its Latin leading (T's Arabic guards, now on the platform's pages);
* V5.29 §5–§6 (owner, 6 Nov 2026: «font weight too heavy … not bold hierarchy»; stream SYS's weight map): every
  title, label and figure reads its ROLE's weight from the tokens, never above 500 — the platform inherits the map;
* Readex Pro loaded on /ar/ and never on /fr/; 0 animations running at rest; no horizontal overflow; 0 console errors.
"""

from __future__ import annotations

import datetime as dt
import os

import pytest
from django.conf import settings
from django.test import Client

from accounts import roles
from accounts.models import AccountType
from core import clock
from tests.frontend.test_typography_v2 import _ARABIC_GUARDS_JS

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

DASHBOARD = "/{lang}/espace-reserve/"
ORGANISATION = "/{lang}/espace-reserve/mon-organisation/"
DEADLINES = "/{lang}/espace-reserve/mes-echeances/"
SIZES = [(1440, 900), (390, 844)]

TYPE_JS = """() => {
  const type = (s) => { const el = document.querySelector(s); if (!el) return null;
    const st = getComputedStyle(el), r = el.getBoundingClientRect();
    return {ff: st.fontFamily.split(',')[0].replace(/"/g, ''), fs: parseFloat(st.fontSize), fw: st.fontWeight,
            lh: parseFloat(st.lineHeight), ls: st.letterSpacing, tt: st.textTransform, w: Math.round(r.width)}; };
  const root = getComputedStyle(document.documentElement);
  return {
    roles: {label: root.getPropertyValue('--w-label').trim(), title: root.getPropertyValue('--w-title').trim()},
    eyebrow: type('.atrium__eyebrow'),
    lead: type('[data-atrium] .ws-head__lead, [data-atrium] .org-head__lead'),
    title: type('[data-atrium] .ws-head__title, [data-atrium] .ctx__title'),
    ring: type('.ring-dial__count'),
    nextDay: type('.db-next__day'),
    orgIndex: type('.org-refs__index'),
    factLabel: type('.org-id__fact > dt'),
    factTime: type('.org-id__fact time'),
    ref: type('.ctx__ref, .db-ref, .reg-ref'),
    faces: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    running: document.getAnimations().filter(a => a.playState === 'running'
      && !(a.timeline instanceof ScrollTimeline || a.timeline instanceof ViewTimeline)).length,
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
    """A person with a file, a checklist line, a due date and a message: the dashboard draws its ring, its figure and its
    references (the NowPanel, the lattice, the dates' panel)."""
    from cases.models import CasePurpose, ResponsibleActor
    from cases.services import add_checklist_item, open_case
    from portal.models import Deadline, Message

    user = user_factory(
        "plat.browser.person@example.test",
        role=roles.PERSON,
        full_name="Personne PLAT",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    case = open_case(user, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    add_checklist_item(
        case,
        requirement="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        detail="Validité résiduelle d’au moins six mois.",
        due_date=clock.today() + dt.timedelta(days=12),
    )
    Deadline.objects.create(owner=user, title="Dépôt du dossier", due_on=clock.today() + dt.timedelta(days=9))
    Message.objects.create(recipient=user, subject="Information", body="Bonjour.")
    return user


@pytest.fixture
def institution(db, user_factory):
    from accounts.models import Membership, Organisation, OrganisationKind

    user = user_factory(
        "plat.browser.institution@example.test", role=roles.INSTITUTION, account_type=AccountType.INSTITUTION
    )
    organisation = Organisation.objects.create(
        name="Istituzione PLAT", kind=OrganisationKind.INSTITUTION, country="IT", city="Padova"
    )
    Membership.objects.create(user=user, organisation=organisation)
    return user


def _page(browser, live_server, user, lang, width, height):
    client = Client()
    client.force_login(user)
    context = browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=1,
        is_mobile=width < 768,
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
    page = context.new_page()
    errors: list[str] = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    return context, page, errors


def _open(page, url):
    page.goto(url, wait_until="load")  # the first console page of a session plays the entrance release
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(2600)  # the atrium's drawing envelope, then rest


def _role(found: dict, name: str) -> str:
    """The role's weight as the tokens declare it — V5.29 §6 (stream SYS's map, tokens.css «one step down»): a title,
    label or figure of the platform takes its role's weight and never more than 500 (no «bold hierarchy»); amended under
    V5.20 citing V5.29 and FINAL_DELIVERY_V2 §3.7 from the literal 600 of TYPOGRAPHY_V2 §4.3 this module first read — the
    same invariant (the element on its role, through the tokens) and a stronger one (the ceiling)."""
    weight = found["roles"][name]
    assert weight.isdigit() and int(weight) <= 500, (name, weight)
    return weight


def _em(value: str, size: float) -> float:
    return 0.0 if value == "normal" else round(float(value.replace("px", "")) / size, 3)


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), SIZES, ids=[f"{w}x{h}" for w, h in SIZES])
def test_the_person_dashboards_type_is_the_contract(browser, live_server, person, lang, width, height):
    """Gate (2): the eyebrow as the label role, the lead ≤ 29 rem, the title's step and tracking, the figures at the role's weight in the
    sans, the reference in the mono, Arabic parity on Readex Pro, nothing moving at rest."""
    context, page, errors = _page(browser, live_server, person, lang, width, height)
    try:
        _open(page, live_server.url + DASHBOARD.format(lang=lang))
        t = page.evaluate(TYPE_JS)
        eyebrow = t["eyebrow"]
        assert eyebrow["fw"] == _role(t, "label")
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
        # arbitrary uppercase»; the platform must not read as the public site): the space's name keeps the label role's
        # face, weight and size, and drops its capitals and its tracking in French as in Arabic (French read
        # «uppercase» at +0.08 em before) — the Arabic invariant, now held in every language
        assert eyebrow["tt"] == "none" and _em(eyebrow["ls"], eyebrow["fs"]) == 0, eyebrow
        if lang == "fr":
            assert eyebrow["ff"] == "Host Grotesk"
            assert eyebrow["fs"] == (13 if width < 768 else 12)
        else:
            assert eyebrow["ff"] == "Readex Pro", eyebrow
            assert eyebrow["fs"] >= 14, eyebrow
        assert t["lead"] is None, "the dashboard's atrium carries no lead — the registers' heads do (below)"
        title = t["title"]
        assert title["fw"] == _role(t, "title") and 24 <= title["fs"] <= 36, title
        if lang == "fr":
            assert abs(_em(title["ls"], title["fs"]) + 0.016) < 0.002 or width < 768, title
        else:
            assert _em(title["ls"], title["fs"]) == 0 and title["lh"] >= title["fs"] * 1.2, title
        for key in ("ring", "nextDay"):
            figure = t[key]
            assert figure and not figure["ff"].startswith("ILE Mono") and figure["fw"] == _role(t, "title"), (
                key,
                figure,
            )
        assert t["nextDay"]["fs"] == 28 and t["nextDay"]["lh"] == 32, t["nextDay"]
        assert t["ref"] and t["ref"]["ff"] == "ILE Mono", t["ref"]
        assert ("Readex Pro" in t["faces"]) == (lang == "ar"), t["faces"]
        assert "Vazirmatn" not in t["faces"]
        assert t["overflow"] == 0 and t["running"] == 0, t
        if lang == "ar":
            found = page.evaluate(_ARABIC_GUARDS_JS)
            assert found["small"] == [] and found["tight"] == [] and found["mono"] == [], found
            assert found["frenchLeading"] == [], found["frenchLeading"]
        # F-8 on a register's head: «Mes échéances» — the lead at or under 29 rem (464 px); the band's figure at the title role's weight
        _open(page, live_server.url + DEADLINES.format(lang=lang))
        r = page.evaluate(TYPE_JS)
        assert r["lead"] and r["lead"]["w"] <= 29 * 16 + 1, r["lead"]
        assert r["title"]["fw"] == _role(r, "title") and r["overflow"] == 0 and r["running"] == 0, r
        assert errors == [], errors
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_organisations_identity_sheet_labels_and_indices(browser, live_server, institution, lang):
    """The identity sheet's facts: the label role on the dt (capitals in French, none in Arabic, the role's weight), the date in the sans
    with tabular figures, the «Le projet» tile indices in the sans at the title role's weight — on «Mon organisation» at 1440."""
    context, page, errors = _page(browser, live_server, institution, lang, 1440, 900)
    try:
        _open(page, live_server.url + ORGANISATION.format(lang=lang))
        t = page.evaluate(TYPE_JS)
        label = t["factLabel"]
        assert label and label["fw"] == _role(t, "label") and label["fs"] >= 12, label
        assert label["tt"] == ("uppercase" if lang == "fr" else "none"), label
        assert label["ff"] == ("Host Grotesk" if lang == "fr" else "Readex Pro"), label
        time_ = t["factTime"]
        assert time_ and not time_["ff"].startswith("ILE Mono"), time_
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
        # tiles' numeric index is retired («no decorative numeric markers»), and the console's eyebrow is the space's
        # name in sentence case in every language («no arbitrary uppercase») — still at the label role's weight
        assert t["orgIndex"] is None, t["orgIndex"]
        assert t["eyebrow"]["fw"] == _role(t, "label") and t["eyebrow"]["tt"] == "none", t["eyebrow"]
        assert t["overflow"] == 0 and t["running"] == 0 and errors == [], (t, errors)
    finally:
        context.close()
