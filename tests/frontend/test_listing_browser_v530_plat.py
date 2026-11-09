"""
The platform's list toolkit in the browser — V5.30, stream C (docs/design-v5/QA/v530/plat/NOTES.md §1, §7; the overlay
system's contract docs/design-v5/QA/v54/w2-a/CONTRACT.md). What a static test cannot see:

* «Filtres» opens the overlay system's drawer as a MODAL: `aria-modal`, the scrim, the page behind hidden from assistive
  technology; the focus inside it, Tab and Shift+Tab wrap inside it (contained), Esc closes it and the focus comes back
  to «Filtres»;
* the drawer stands at the inline END — the right edge in French, the left edge in Arabic — and on a phone it takes the
  whole width; under reduced motion it never slides (no translation at any frame);
* choosing in the drawer writes the URL (only what narrows: listing.js leaves the empty fields out), the chips and the
  count follow; a chip's × removes its criterion alone, «Tout effacer» the whole narrowing; the sort applies when chosen;
  Back returns to the list as it was — the state lives in the URL;
* the need's withdrawal asks first in the alert dialog: «Annuler» takes the focus, Tab stays inside, Esc answers safe
  and the focus returns to the opener;
* no console error, no CSP violation.
Chromium on the test database; sessions minted with ``Client.force_login`` — nothing typed, no password used. The first
console page of a session carries the loader's entrance release (W1-D): each page is loaded once first.
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

MESSAGES = "/{lang}/espace-reserve/communications/"
CSP_HOOK = (
    "document.addEventListener('securitypolicyviolation', (e) => "
    "{ (window.__csp = window.__csp || []).push(e.violatedDirective + ' ' + e.blockedURI); });"
)
DRAWER = "#lst-messages-filters"


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
def reader(db, user_factory):
    from portal.models import Message

    person = user_factory(
        "v530.reader@example.test",
        role=roles.PERSON,
        full_name="Lecture ESSAI",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    staff = user_factory("v530.reader-staff@example.test", role=roles.STAFF, is_staff=True)
    for subject, read, days in (
        ("Mise à jour de votre dossier", False, 1),
        ("Ouverture d’un dossier", True, 20),
        ("Rappel de pièce", False, 5),
    ):
        message = Message.objects.create(recipient=person, sender=staff, subject=subject, body=f"Corps — {subject}")
        when = timezone.now() - dt.timedelta(days=days)
        Message.objects.filter(pk=message.pk).update(
            created_at=when, **({"is_read": True, "read_at": when} if read else {})
        )
    return person


def _open(browser, live_server, user, path, *, lang="fr", width=1440, height=900, phone=False, reduced=False):
    client = Client()
    client.force_login(user)
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
    if phone:
        options.update(is_mobile=True, has_touch=True)
    if reduced:
        options["reduced_motion"] = "reduce"
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
    page.add_init_script(CSP_HOOK)
    errors: list[str] = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    url = live_server.url + path.format(lang=lang)
    page.goto(url, wait_until="load")
    page.goto(url, wait_until="load")
    page.wait_for_function("() => document.body.classList.contains('is-ready')")
    return context, page, errors


#: Chromium's own DOMException when a Back lands on a page whose cross-document view transition (the shell's «Lume»,
#: static/js/src/head/head.js — a preserved family, not the toolkit's) was already revealed: the transition's `ready`
#: promise rejects. Only the history test meets it; every other message still fails the test.
BACK_TRANSITION = "Transition was aborted because of invalid state. Page already revealed"


def _clean(page, errors, *, back=False):
    assert not [e for e in errors if not (back and e == BACK_TRANSITION)], errors
    assert page.evaluate("window.__csp || []") == []


def _open_drawer(page, *, keyboard=False):
    if keyboard:
        page.focus(".lst__open")
        page.keyboard.press("Enter")
    else:
        page.click(".lst__open")
    page.wait_for_function(f"() => document.querySelector('{DRAWER}').open")
    page.wait_for_timeout(400)  # the slide's 320 ms


def test_filtres_opens_a_modal_drawer_that_contains_the_focus_and_gives_it_back(browser, live_server, reader):
    context, page, errors = _open(browser, live_server, reader, MESSAGES)
    _open_drawer(page, keyboard=True)
    state = page.evaluate(
        f"""() => {{ const d = document.querySelector('{DRAWER}');
        return {{ modal: d.getAttribute('aria-modal'), inside: d.contains(document.activeElement),
                 scrim: !!document.querySelector('.overlay-scrim') && getComputedStyle(document.querySelector('.overlay-scrim')).display !== 'none',
                 hidden: document.querySelector('.reg-page').closest('[aria-hidden="true"]') !== null }}; }}"""
    )
    assert state["modal"] == "true" and state["inside"] and state["scrim"], state
    assert state["hidden"], "the page behind is hidden from assistive technology while the trap holds"
    # Tab and Shift+Tab never leave the panel
    for key in ["Tab"] * 12 + ["Shift+Tab"] * 12:
        page.keyboard.press(key)
        assert page.evaluate(f"() => document.querySelector('{DRAWER}').contains(document.activeElement)"), key
    page.keyboard.press("Escape")
    page.wait_for_function(f"() => !document.querySelector('{DRAWER}').open")
    assert page.evaluate("() => document.activeElement && document.activeElement.classList.contains('lst__open')")
    _clean(page, errors)
    context.close()


@pytest.mark.parametrize(("lang", "edge"), [("fr", "right"), ("ar", "left")])
def test_the_drawer_stands_at_the_inline_end_and_mirrors_in_arabic(browser, live_server, reader, lang, edge):
    context, page, errors = _open(browser, live_server, reader, MESSAGES, lang=lang)
    _open_drawer(page)
    box = page.evaluate(
        f"() => {{ const r = document.querySelector('{DRAWER}').getBoundingClientRect(); return [r.left, r.right, innerWidth, r.width]; }}"
    )
    left, right, width, panel = box
    assert panel < width * 0.6, box
    if edge == "right":
        assert abs(right - width) <= 1 and left > width / 2, box
    else:
        assert abs(left) <= 1 and right < width / 2, box
    # the whole height of the viewport, its foot in view: never pushed down by the column's flow margin (48 px once)
    top, bottom, inner, foot = page.evaluate(
        f"""() => {{ const r = document.querySelector('{DRAWER}').getBoundingClientRect();
        const f = document.querySelector('{DRAWER} .overlay__foot button[type=submit]').getBoundingClientRect();
        return [r.top, r.bottom, innerHeight, f.bottom]; }}"""
    )
    assert abs(top) <= 1 and abs(bottom - inner) <= 1 and foot <= inner, (top, bottom, inner, foot)
    _clean(page, errors)
    context.close()


def test_on_a_desk_the_bar_stays_in_reach_directly_under_the_console_bar(browser, live_server, reader):
    # V5.30 §12 «sticky header»: scrolled, the search is neither behind the console's own sticky bar nor out of view.
    context, page, errors = _open(browser, live_server, reader, MESSAGES, height=360)
    state = page.evaluate(
        """() => {
            const lst = document.querySelector('.lst');
            const top = lst.getBoundingClientRect().top + window.scrollY;
            window.scrollTo({ top: top + 120, behavior: 'instant' });
            const bar = document.querySelector('.console-bar').getBoundingClientRect();
            const box = lst.getBoundingClientRect();
            const q = document.querySelector('.lst__q').getBoundingClientRect();
            const at = document.elementFromPoint(q.left + q.width / 2, q.top + q.height / 2);
            return {
                scrolled: window.scrollY,
                barBottom: bar.bottom,
                lstTop: box.top,
                searchOnTop: Boolean(at && at.closest('.lst')),
            };
        }"""
    )
    assert state["scrolled"] > 0, state
    assert abs(state["lstTop"] - state["barBottom"]) <= 1, state
    assert state["searchOnTop"], state
    _clean(page, errors)
    context.close()


def test_on_a_phone_the_drawer_takes_the_whole_width(browser, live_server, reader):
    context, page, errors = _open(browser, live_server, reader, MESSAGES, width=390, height=844, phone=True)
    _open_drawer(page)
    left, width, inner = page.evaluate(
        f"() => {{ const r = document.querySelector('{DRAWER}').getBoundingClientRect(); return [r.left, r.width, innerWidth]; }}"
    )
    assert abs(left) <= 1 and abs(width - inner) <= 1, (left, width, inner)
    assert page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
    _clean(page, errors)
    context.close()


def test_under_reduced_motion_the_drawer_never_slides(browser, live_server, reader):
    context, page, errors = _open(browser, live_server, reader, MESSAGES, reduced=True)
    page.evaluate(
        f"""() => {{ window.__moves = []; const d = document.querySelector('{DRAWER}');
        const sample = () => {{ const cs = getComputedStyle(d); window.__moves.push(cs.translate + '|' + cs.transform);
                               if (window.__moves.length < 30) requestAnimationFrame(sample); }};
        document.querySelector('.lst__open').addEventListener('click', () => requestAnimationFrame(sample)); }}"""
    )
    _open_drawer(page)
    moves = set(page.evaluate("() => window.__moves"))
    assert moves and all(m.split("|")[0] in ("none", "0px") and m.split("|")[1] == "none" for m in moves), moves
    _clean(page, errors)
    context.close()


def test_the_drawer_writes_the_url_the_chips_remove_and_clear_all_restores(browser, live_server, reader):
    context, page, errors = _open(browser, live_server, reader, MESSAGES)
    base = live_server.url + MESSAGES.format(lang="fr")
    _open_drawer(page)
    page.check(f"{DRAWER} input[name='lecture'][value='non-lues']")
    with page.expect_navigation():
        page.click(f"{DRAWER} .overlay__foot button[type='submit']")
    assert page.url == base + "?lecture=non-lues", "only what narrows: the empty period stays out of the URL"
    assert page.inner_text(".lst__found") == "2 résultats"
    assert page.locator(".lst__chip").count() == 1 and page.locator(".lst__n").inner_text().strip().endswith("1")
    # the search keeps the drawer's choice; then the chip of the state removes the state alone
    page.fill(".lst__q", "rappel")
    with page.expect_navigation():
        page.press(".lst__q", "Enter")
    assert "lecture=non-lues" in page.url and "q=rappel" in page.url
    assert page.inner_text(".lst__found") == "1 résultat" and page.locator(".lst__chip").count() == 2
    with page.expect_navigation():
        page.click(".lst__chip:has-text('Non lues') .lst__x")
    assert "lecture" not in page.url and "q=rappel" in page.url
    # the sort applies as soon as it is chosen (listing.js), and Back returns to the list as it was
    with page.expect_navigation():
        page.select_option(".lst__select", "anciennes")
    assert "tri=anciennes" in page.url
    page.go_back()
    page.wait_for_load_state("load")
    assert "tri=anciennes" not in page.url and "q=rappel" in page.url
    with page.expect_navigation():
        page.click(".lst__clear")
    assert page.url == base and page.locator(".lst__chip").count() == 0
    assert page.locator(".reg-rows--mail .reg-row").count() == 3
    _clean(page, errors, back=True)
    context.close()


@pytest.fixture
def need_owner(db, user_factory):
    from accounts.models import (
        AccountVerification,
        Membership,
        MembershipRole,
        Organisation,
        OrganisationKind,
        VerificationStatus,
    )
    from companies.models import CompanyNeed, CompanyProfile, Sector

    user = user_factory("v530.need@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    organisation = Organisation.objects.create(
        name="Organisation besoin", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    AccountVerification.objects.create(
        user=user, declared_type=AccountType.COMPANY, status=VerificationStatus.APPROVED, decided_at=timezone.now()
    )
    sector, _created = Sector.objects.get_or_create(
        code="batiment", defaults={"label_fr": "Bâtiment et travaux publics", "order": 10}
    )
    profile = CompanyProfile.objects.create(
        organisation=organisation,
        legal_name="Société besoin S.r.l.",
        registration_number="RM-BESOIN-01",
        sector=sector,
        contact_name="Référent",
        contact_function="RH",
        contact_email="referent-besoin@example.test",
        city="Rovigo",
        country="IT",
    )
    need = CompanyNeed.objects.create(company=profile, title="Soudure sur charpente", headcount=1, status="draft")
    return user, need


def test_the_withdrawal_asks_first_and_answers_safe_on_esc(browser, live_server, need_owner):
    user, need = need_owner
    context, page, errors = _open(
        browser, live_server, user, f"/fr/espace-reserve/entreprise/mes-besoins/{need.reference}/"
    )
    page.focus("a[href='#need-withdraw-dialog']")
    page.keyboard.press("Enter")
    page.wait_for_function("() => document.getElementById('need-withdraw-dialog').open")
    assert page.evaluate("() => document.activeElement.matches('[data-overlay-safe]')"), "«Annuler» takes the focus"
    for key in ["Tab"] * 6 + ["Shift+Tab"] * 6:
        page.keyboard.press(key)
        assert page.evaluate(
            "() => document.getElementById('need-withdraw-dialog').contains(document.activeElement)"
        ), key
    page.keyboard.press("Escape")
    page.wait_for_function("() => !document.getElementById('need-withdraw-dialog').open")
    assert page.evaluate("() => document.activeElement.matches(\"a[href='#need-withdraw-dialog']\")")
    need.refresh_from_db()
    assert need.status == "draft", "Esc is the safe answer: nothing withdrawn"
    _clean(page, errors)
    context.close()
