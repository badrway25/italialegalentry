"""
The service pages on design V5 — «le pagine di servizio» (W3-F2 step 2; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5
item 2) — in a browser: what the sources cannot show (tests/frontend/test_service_pages_w3_f2.py holds the rules).

* every error page (400, 403, 404, 410, 429, 500) and every account page, in French and in Arabic, at 1440 and at
  390 px: no page wider than its viewport, one h1, at most three corner values a screen with the letterhead (§1.3; a
  pill is `full`), no shadow of level 3 or more at rest (SH-8), no CSP report, no console error, no Latin text under
  12 px and no Arabic text under 14 px, typed text at 16 px — and none wider than its viewport at 320 and 430 px;
* a real failure reaches the self-sufficient 500 (and a suspicious request the 400) through every middleware, CSP
  included: a view of this module raises, Django answers with core.views.error_500 / error_400;
* the account's sections: the current one carries the tabs' indicator at the reading edge from 64rem, a band below;
* the door at rest on the error pages (the review's M1) — in the head's end seat from 64rem, its arch on the end edge
  (the right, the left of an Arabic page), compact above the label at the reading edge on a phone; the stage never
  mirrored, the key out of the lock (turned on its side), the photograph loaded, nothing moving — on the public shell's
  404 and on the self-sufficient 500.

Chromium on the live server; the account pages through a session minted with ``Client.force_login`` — nothing typed,
no password used. With W3F2_SHOTS set, every page is captured there (the family's evidence).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from django.core.exceptions import SuspiciousOperation
from django.urls import path

from config import urls as project_urls

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True), pytest.mark.urls(__name__)]

SHOTS = Path(os.environ["W3F2_SHOTS"]) if os.environ.get("W3F2_SHOTS") else None


def _fails(request):
    raise RuntimeError("a failure inside a view (TEST-ONLY)")


def _suspicious(request):
    raise SuspiciousOperation("a request this server will not read (TEST-ONLY)")


#: this module is the URLconf of its tests: the project's, plus two views that fail on purpose
urlpatterns = [
    path("__w3f2__/500/", _fails),
    path("__w3f2__/400/", _suspicious),
    *project_urls.urlpatterns,
]
handler400 = project_urls.handler400
handler403 = project_urls.handler403
handler404 = project_urls.handler404
handler500 = project_urls.handler500

INIT = r"""window.__csp = []; document.addEventListener('securitypolicyviolation', (e) => window.__csp.push(e.violatedDirective));"""

PROBE = r"""() => {
  const out = {overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
               h1: document.querySelectorAll('h1').length, radii: 0, worst: null, shadows: 0, small: [], fields: [],
               csp: window.__csp || []};
  const vh = window.innerHeight, boxes = [];
  for (const el of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (el.closest('[hidden], .visually-hidden, .skip-link') || (el.closest('details:not([open])') && !el.closest('summary'))) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const edge = (s, w) => s !== 'none' && parseFloat(w) > 0;
    const drawn = edge(cs.borderTopStyle, cs.borderTopWidth) || edge(cs.borderBottomStyle, cs.borderBottomWidth)
      || edge(cs.borderLeftStyle, cs.borderLeftWidth) || edge(cs.borderRightStyle, cs.borderRightWidth)
      || cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || el.tagName === 'IMG';
    const half = Math.min(r.width, r.height) / 2 - 0.5, radii = new Set();
    if (drawn) for (const v of [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomLeftRadius, cs.borderBottomRightRadius]) {
      if (v !== '0px') radii.add(parseFloat(v) >= half ? 'full' : v);
    }
    const high = /40px -12px|64px -16px/.test(cs.boxShadow);
    if (radii.size || high) boxes.push({top: r.top + scrollY, bottom: r.bottom + scrollY, radii: [...radii], high});
    if (el.closest('main') && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) {
      const size = parseFloat(cs.fontSize);
      const arabic = (el.closest('[lang]') || document.documentElement).getAttribute('lang') === 'ar';
      if (size < (arabic ? 14 : 12)) out.small.push(`${el.tagName}.${el.className}: ${size}`);
    }
    if (el.closest('main') && el.matches('input:not([type=checkbox]):not([type=radio]):not([type=hidden]):not([type=submit]), textarea, select')) out.fields.push(cs.fontSize);
  }
  const height = document.documentElement.scrollHeight;
  for (let y = 0; y < Math.max(height - vh + 1, 1); y += Math.max(200, Math.floor(vh / 2))) {
    const seen = new Set(); let high = 0;
    for (const b of boxes) {
      if (b.bottom <= y || b.top >= y + vh) continue;
      b.radii.forEach((v) => seen.add(v));
      if (b.high) high++;
    }
    if (seen.size > out.radii) { out.radii = seen.size; out.worst = [...seen]; }
    out.shadows = Math.max(out.shadows, high);
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


@pytest.fixture
def site(live_server, seeded):
    return live_server.url


@pytest.fixture
def people(user_factory, superuser):
    from allauth.account.models import EmailAddress

    from accounts import roles

    person = user_factory("w3f2-service@example.test", role=roles.PERSON, full_name="Personne de test W3-F2")
    EmailAddress.objects.create(user=person, email=person.email, verified=True, primary=True)
    return {"person": person, "admin": superuser}


def _session(user, site: str) -> dict:
    from django.conf import settings
    from django.test import Client

    client = Client()
    client.force_login(user)
    return {
        "name": settings.SESSION_COOKIE_NAME,
        "value": client.cookies[settings.SESSION_COOKIE_NAME].value,
        "url": site,
    }


#: (path — `{lang}` replaced, or none for a path without a language —, who is signed in, the expected status)
PAGES = [
    ("/__w3f2__/400/", None, 400),
    ("/__w3f2__/500/", None, 500),
    ("/{lang}/page-inexistante-w3f2/", None, 404),
    ("/hello-world/", None, 410),
    ("/{lang}/compte/profil/suppression/", "admin", 403),
    ("/{lang}/compte/profil/", "person", 200),
    ("/{lang}/compte/email/", "person", 200),
    ("/{lang}/compte/password/change/", "person", 200),
    ("/{lang}/compte/2fa/", "person", 200),
    ("/{lang}/compte/profil/suppression/", "person", 200),
    ("/{lang}/compte/logout/", "person", 200),
    ("/{lang}/compte/profil/suppression/confirmee/", None, 200),
]


def _check(page, where: str, failures: list[str]) -> None:
    probe = page.evaluate(PROBE)
    if probe["overflow"] > 0:
        failures.append(f"{where}: {probe['overflow']} px wider than the viewport")
    if probe["h1"] != 1:
        failures.append(f"{where}: {probe['h1']} h1")
    if probe["radii"] > 3:
        failures.append(f"{where}: {probe['radii']} corner values on one screen {probe['worst']}")
    if probe["shadows"] > 1:
        failures.append(f"{where}: {probe['shadows']} shadows of level 3 or more at rest")
    if probe["csp"]:
        failures.append(f"{where}: CSP {probe['csp']}")
    if probe["small"]:
        failures.append(f"{where}: text too small {probe['small'][:3]}")
    if any(size != "16px" for size in probe["fields"]):
        failures.append(f"{where}: typed text {probe['fields']}")


def test_every_service_page_holds_the_grammar_in_both_directions(browser, site, people):
    failures = []
    sessions = {who: _session(user, site) for who, user in people.items()}
    for lang in ("fr", "ar"):
        for width in (1440, 390, 320, 430):
            context = browser.new_context(viewport={"width": width, "height": 900 if width > 800 else 844}, locale=lang)
            context.add_init_script(INIT)
            context.add_cookies([{"name": "ile_language", "value": lang, "url": site}])
            page = context.new_page()
            errors: list[str] = []
            page.on(
                "console",
                lambda m: (
                    errors.append(m.text)
                    if m.type == "error" and "the server responded with a status of" not in m.text
                    else None
                ),
            )
            for template, who, status in PAGES:
                context.clear_cookies()
                context.add_cookies([{"name": "ile_language", "value": lang, "url": site}])
                if who:
                    context.add_cookies([sessions[who]])
                url = site + template.format(lang=lang)
                errors.clear()
                response = page.goto(url, wait_until="networkidle")
                where = f"{lang} {width} {template}{f' ({who})' if who else ''}"
                if response.status != status:
                    failures.append(f"{where}: HTTP {response.status}, expected {status}")
                if page.evaluate("document.documentElement.lang") != lang:
                    failures.append(f"{where}: the page is not in {lang}")
                _check(page, where, failures)
                if errors:
                    failures.append(f"{where}: console {errors[:2]}")
                if SHOTS and width in (1440, 390):
                    SHOTS.mkdir(parents=True, exist_ok=True)
                    slug = template.replace("{lang}", "").strip("/").replace("/", "_") or "root"
                    page.screenshot(
                        path=str(SHOTS / f"{slug}{f'_{who}' if who else ''}_{lang}_{width}.png"), full_page=True
                    )
            context.close()
    assert failures == [], "\n".join(failures)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_account_s_current_section_stands_on_the_reading_edge(browser, site, people, lang):
    """From 64rem the sections are a list at the reading edge (the right one in Arabic) with the indicator on its rule;
    below, a band whose current link carries the indicator under its words."""
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        context.add_cookies([_session(people["person"], site)])
        page = context.new_page()
        page.goto(f"{site}/{lang}/compte/email/", wait_until="networkidle")
        geometry = page.evaluate(
            """() => { const nav = document.querySelector('.conto-nav').getBoundingClientRect();
                       const main = document.querySelector('.conto__main').getBoundingClientRect();
                       const link = document.querySelector('.conto-nav__link[aria-current]');
                       const mark = getComputedStyle(link, '::after');
                       return {navLeft: nav.left, navRight: nav.right, mainLeft: main.left, mainRight: main.right,
                               markWidth: parseFloat(mark.width), markHeight: parseFloat(mark.height)}; }"""
        )
        if lang == "ar":
            assert geometry["navLeft"] > geometry["mainRight"], geometry
        else:
            assert geometry["navRight"] < geometry["mainLeft"], geometry
        assert geometry["markWidth"] == 2 and geometry["markHeight"] >= 44, "the indicator on the list's rule"
        page.set_viewport_size({"width": 390, "height": 844})
        band = page.evaluate(
            """() => { const nav = document.querySelector('.conto-nav').getBoundingClientRect();
                       const h1 = document.querySelector('h1').getBoundingClientRect();
                       const mark = getComputedStyle(document.querySelector('.conto-nav__link[aria-current]'), '::after');
                       return {navBottom: nav.bottom, h1Top: h1.top, markHeight: parseFloat(mark.height)}; }"""
        )
        assert band["navBottom"] <= band["h1Top"] and band["markHeight"] == 2, band
    finally:
        context.close()


DOOR = r"""() => {
  const door = document.querySelector('.error-page__door'), body = document.querySelector('.error-page__body');
  const label = document.querySelector('.error-page__code'), section = document.querySelector('.error-page');
  const cs = getComputedStyle(section), box = section.getBoundingClientRect();
  const r = door.getBoundingClientRect(), b = body.getBoundingClientRect(), l = label.getBoundingClientRect();
  const img = door.querySelector('img');
  return {door: {left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width},
          body: {left: b.left, right: b.right}, label: {left: l.left, right: l.right, top: l.top},
          content: {left: box.left + parseFloat(cs.paddingLeft), right: box.right - parseFloat(cs.paddingRight)},
          direction: getComputedStyle(door).direction, hidden: door.getAttribute('aria-hidden'),
          key: getComputedStyle(door.querySelector('.error-page__key')).transform,
          photo: img.complete && img.naturalWidth > 0,
          moving: document.getAnimations().filter((a) => a.effect && door.contains(a.effect.target)).length};
}"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_error_pages_seat_the_door_at_rest(browser, site, lang):
    for address, status in (("/{lang}/page-inexistante-w3f2/", 404), ("/__w3f2__/500/", 500)):
        for width in (1440, 390):
            context = browser.new_context(viewport={"width": width, "height": 900 if width > 800 else 844}, locale=lang)
            try:
                context.add_cookies([{"name": "ile_language", "value": lang, "url": site}])
                page = context.new_page()
                response = page.goto(site + address.format(lang=lang), wait_until="networkidle")
                assert response.status == status
                state = page.evaluate(DOOR)
                where = (lang, width, status, state)
                # the arch, not its box, stands on the edge: the stage's margin beside the arch is 24 of its 368 units
                pull = state["door"]["width"] * 24 / 368
                assert state["direction"] == "ltr" and state["hidden"] == "true", where
                assert state["key"] == "matrix(0, 1, -1, 0, 0, 0)", where
                assert state["photo"] and state["moving"] == 0, where
                if width == 1440:
                    if lang == "ar":
                        assert state["door"]["right"] < state["body"]["left"], where
                        assert abs(state["door"]["left"] + pull - state["content"]["left"]) <= 1, where
                    else:
                        assert state["door"]["left"] > state["body"]["right"], where
                        assert abs(state["door"]["right"] - pull - state["content"]["right"]) <= 1, where
                else:
                    assert state["door"]["bottom"] <= state["label"]["top"], where
                    if lang == "ar":
                        assert abs(state["door"]["right"] - pull - state["label"]["right"]) <= 1, where
                    else:
                        assert abs(state["door"]["left"] + pull - state["label"]["left"]) <= 1, where
            finally:
                context.close()
