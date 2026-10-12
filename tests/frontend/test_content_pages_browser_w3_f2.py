"""
The content pages on design V5 — «la lettura» (W3-F2; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 2) — in a
browser: what the sources cannot show (tests/frontend/test_content_pages_w3_f2.py holds the rules).

* every page of the area, in French and in Arabic, at 1440 and at 390 px: no page wider than its viewport, one h1, at
  most three corner values a screen with the letterhead's targa (§1.3), no shadow at
  rest (hairlines before boxes — SH-2), at most six glyphs in its editorial body (§1.7), no Latin text under 12 px and
  no Arabic text under 14 px, typed text at 16 px;
* an authority's link shows its host (D26);
* the glossary's letter index stays under the letterhead while the register scrolls, from 48rem, and a letter
  reached from it stands under it; the FAQ's disclosure opens and closes from the keyboard;
* the review's fixes: on the Arabic pages every Latin head ends on its cell's reading edge — the glossary's Italian
  terms, the FAQ's French questions, the Forum Virtuel's French rooms (M2) — and a French lead stands on the reading
  edge, reading from its own start (m8); the letter band holds one line on a phone (m1); an enquiry form's first
  legend leaves the screen to its chapter's title (m6).

Chromium on the live server, gate G3 open (phase 3), gate G2 opened by TEST-ONLY legal text, the Forum Virtuel's flag
on; TEST-ONLY content: two articles (one with official sources), two practical sheets (one with sources), two
authorised partners, a member's Forum (rooms, a thread, a calendar entry, an initiative). A member's pages through a
session minted with ``Client.force_login`` — nothing typed, no password used. With W3F2_SHOTS set, every page is
captured there (the family's evidence); otherwise nothing is written.
"""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

SHOTS = Path(os.environ["W3F2_SHOTS"]) if os.environ.get("W3F2_SHOTS") else None

PROBE = r"""() => {
  const main = document.querySelector('main');
  const out = {overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
               h1: document.querySelectorAll('h1').length, radii: [], shadows: [], icons: 0, small: [], fields: []};
  const radii = new Set();
  for (const el of main.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const drawn = cs.borderTopStyle !== 'none' || cs.borderInlineStartStyle !== 'none'
      || cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || el.tagName === 'IMG';
    for (const v of [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomLeftRadius, cs.borderBottomRightRadius]) {
      if (drawn && v !== '0px') radii.add(v);
    }
    if (cs.boxShadow !== 'none' && !el.matches('input, textarea, select, :focus')) out.shadows.push(el.className || el.tagName);
    if (el.matches('svg.icon')) out.icons++;
    if ([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) {
      const size = parseFloat(cs.fontSize);
      const arabic = (el.closest('[lang]') || document.documentElement).getAttribute('lang') === 'ar';
      if (size < (arabic ? 14 : 12)) out.small.push(`${el.tagName}.${el.className}: ${size}`);
    }
    if (el.matches('input:not([type=checkbox]):not([type=radio]):not([type=hidden]):not([type=submit]), textarea, select')
        && !el.closest('.hp-wrap, .hp-field')) out.fields.push(cs.fontSize);
  }
  out.radii = [...radii];
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
def phase3_live(set_flag, monkeypatch):
    """Gate G3 open for the live server WITHOUT freezegun (a frozen ``time.monotonic`` stalls Playwright)."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    set_flag("virtual_forum", True)
    flags.invalidate()
    yield fixed
    flags.invalidate()


@pytest.fixture
def content(phase3_live, user_factory):
    """TEST-ONLY content for the pages the seed leaves empty."""
    from accounts import roles
    from cms.models import PublicationStatus
    from community.models import (
        CalendarEntry,
        Discussion,
        Initiative,
        InitiativeStatus,
        Membership,
        MembershipStatus,
        ParticipantCategory,
        Post,
        PostStatus,
        Room,
    )
    from living.models import LegalReviewStatus, LivingSheet, LivingTopic
    from news.models import Article, NewsCategory
    from partners.models import Partner, PartnerKind

    now = phase3_live
    category = NewsCategory.objects.get(slug="normativa")
    sources = [{"url": "https://www.gazzettaufficiale.it/eli/id/2026/01/01/test", "label": "Gazzetta Ufficiale (TEST)"}]
    article = Article.objects.create(
        slug="article-test-w3f2",
        category=category,
        title_fr="Article de test W3-F2 avec des sources",
        summary_fr="Résumé de test : aucune information réelle.",
        body_fr="Premier paragraphe de test.\n\n## Intertitre\n\nSecond paragraphe.\n\n- point un\n- point deux",
        status=PublicationStatus.PUBLISHED,
        published_at=now - dt.timedelta(days=2),
        source_links=sources,
    )
    Article.objects.create(
        slug="article-test-w3f2-b",
        category=category,
        title_fr="Second article de test W3-F2",
        summary_fr="Résumé de test.",
        body_fr="Paragraphe de test.",
        status=PublicationStatus.PUBLISHED,
        published_at=now - dt.timedelta(days=5),
    )
    reviewer = user_factory("w3f2-reviewer@example.test", role=roles.STAFF, is_staff=True)
    topic = LivingTopic.objects.get(slug="logement")
    sheet = LivingSheet.objects.create(
        topic=topic,
        slug="fiche-test-w3f2",
        title_fr="Fiche de test W3-F2",
        summary_fr="Résumé de la fiche de test.",
        body_fr="Paragraphe de test.\n\n## Section de test\n\n- a\n- b",
        status=PublicationStatus.PUBLISHED,
        published_at=now - dt.timedelta(days=1),
        legal_review=LegalReviewStatus.REVIEWED,
        reviewer=reviewer,
        last_reviewed_at=now - dt.timedelta(days=1),
        sources=[
            {"url": "https://www.integrazionemigranti.gov.it/test", "label": "Portale Integrazione Migranti (TEST)"}
        ],
    )
    LivingSheet.objects.create(
        topic=topic,
        slug="fiche-test-w3f2-b",
        title_fr="Seconde fiche de test W3-F2",
        summary_fr="Résumé.",
        body_fr="Paragraphe.",
        status=PublicationStatus.PUBLISHED,
        published_at=now - dt.timedelta(days=1),
        legal_review=LegalReviewStatus.REVIEWED,
        reviewer=reviewer,
        last_reviewed_at=now - dt.timedelta(days=1),
    )
    for name, kind in (
        ("Institution de test W3-F2", PartnerKind.INSTITUTION),
        ("Entreprise de test W3-F2", PartnerKind.COMPANY),
    ):
        Partner.objects.create(
            name=name,
            kind=kind,
            city="Rovigo",
            country="Italie",
            description_fr="Description de test.",
            authorized=True,
            authorization_reference="TEST-ONLY",
            authorized_at=now,
            status=PublicationStatus.PUBLISHED,
            published_at=now - dt.timedelta(days=1),
        )
    room = Room.objects.filter(published=True).order_by("order").first() or Room.objects.create(
        slug="espace-commun", name_fr="Espace commun", allowed_categories=[], order=1, published=True
    )
    user = user_factory("w3f2-member@example.test", role=roles.COMPANY)
    member = Membership.objects.create(
        user=user, category=ParticipantCategory.COMPANY, status=MembershipStatus.APPROVED, approved_at=now, trusted=True
    )
    discussion = Discussion.objects.create(
        room=room, author=member, title="Discussion de test W3-F2", last_activity_at=now
    )
    Post.objects.create(
        discussion=discussion, author=member, body="Premier message de test.", status=PostStatus.VISIBLE
    )
    Post.objects.create(
        discussion=discussion, author=member, body="Message de test en attente.", status=PostStatus.PENDING_MODERATION
    )
    CalendarEntry.objects.create(
        room=room,
        title="Rendez-vous de test W3-F2",
        starts_at=now + dt.timedelta(days=3),
        place="En ligne",
        published=True,
    )
    Initiative.objects.create(
        room=room, title="Initiative de test W3-F2", status=InitiativeStatus.choices[0][0], owner=member, published=True
    )
    return {"article": article, "sheet": sheet, "room": room, "discussion": discussion, "member": user}


@pytest.fixture
def site(live_server, seeded, legal_published, content):
    return live_server.url


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


def _bare(url: str) -> str:
    """A page's path without its language prefix: /fr/actualites/x/ → /actualites/x/."""
    return "/" + url.split("/", 2)[2]


def _pages(content) -> list[tuple[str, bool]]:
    """(path without the language, needs the member's session)."""
    return [
        ("/faq/", False),
        ("/faq/?q=visa", False),
        ("/glossaire/", False),
        ("/glossaire/codice_fiscale/", False),
        ("/partenaires/", False),
        ("/actualites/", False),
        (_bare(content["article"].get_absolute_url()), False),
        ("/vivre-en-italie/", False),
        ("/vivre-en-italie/logement/", False),
        (_bare(content["sheet"].get_absolute_url()), False),
        ("/contact/formulaire/", False),
        ("/entreprises/recueil-des-besoins/", False),
        ("/collaboration/institutions/", False),
        ("/privacy-policy/", False),
        ("/forum-virtuel/", False),
        ("/forum-virtuel/", True),
        (f"/forum-virtuel/salles/{content['room'].slug}/", True),
        (f"/forum-virtuel/discussions/{content['discussion'].pk}/", True),
        ("/forum-virtuel/calendrier/", True),
        ("/forum-virtuel/initiatives/", True),
    ]


def test_every_content_page_holds_the_grammar_in_both_directions(browser, site, content):
    failures = []
    for lang in ("fr", "ar"):
        for width in (1440, 390):
            for member in (False, True):
                context = browser.new_context(
                    viewport={"width": width, "height": 900 if width > 800 else 844}, device_scale_factor=1
                )
                if member:
                    context.add_cookies([_session(content["member"], site)])
                page = context.new_page()
                for path, needs_member in _pages(content):
                    if needs_member != member:
                        continue
                    response = page.goto(f"{site}/{lang}{path}", wait_until="networkidle")
                    probe = page.evaluate(PROBE)
                    where = f"{lang} {width} {path}{' (member)' if member else ''}"
                    if response.status != 200:
                        failures.append(f"{where}: HTTP {response.status}")
                    if probe["overflow"] > 0:
                        failures.append(f"{where}: {probe['overflow']} px wider than the viewport")
                    if probe["h1"] != 1:
                        failures.append(f"{where}: {probe['h1']} h1")
                    # the letterhead's targa draws 6 px on every screen: with it, three corner values at most (§1.3)
                    if len(set(probe["radii"]) | {"6px"}) > 3:
                        failures.append(f"{where}: corners {probe['radii']}")
                    if probe["shadows"]:
                        failures.append(f"{where}: shadows at rest on {probe['shadows'][:3]}")
                    if probe["icons"] > 6:
                        failures.append(f"{where}: {probe['icons']} glyphs in the editorial body")
                    if probe["small"]:
                        failures.append(f"{where}: text too small {probe['small'][:3]}")
                    if any(size != "16px" for size in probe["fields"]):
                        failures.append(f"{where}: typed text {probe['fields']}")
                    if SHOTS:
                        SHOTS.mkdir(parents=True, exist_ok=True)
                        slug = path.strip("/").replace("/", "_").replace("?", "_").replace("=", "-") or "root"
                        page.screenshot(
                            path=str(SHOTS / f"{slug}{'_member' if member else ''}_{lang}_{width}.png"), full_page=True
                        )
                context.close()
    assert failures == [], "\n".join(failures)


def test_an_authoritys_link_shows_its_host(browser, site, content):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(site + content["article"].get_absolute_url(), wait_until="networkidle")
        assert page.locator(".fonti .autorita__host").all_inner_texts() == ["gazzettaufficiale.it"]
        page.goto(site + content["sheet"].get_absolute_url(), wait_until="networkidle")
        assert page.locator(".fonti .autorita__host").all_inner_texts() == ["integrazionemigranti.gov.it"]
        # the sheet's slots: the verification line, the one inset, «who can help me»
        assert page.locator(".verifica").count() == 1 and page.locator(".inset").count() == 1
        assert page.locator(".aiuto a[href^='mailto:']").count() == 1
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_letter_index_stays_under_the_letterhead_and_a_letter_lands_under_it(browser, site, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
        page.evaluate("window.scrollTo(0, 900)")
        page.wait_for_timeout(300)
        bar = page.evaluate("""() => { const r = document.querySelector('.az-index').getBoundingClientRect();
            return {top: Math.round(r.top), bottom: r.bottom, header: Math.round(document.querySelector('.site-header').getBoundingClientRect().bottom)}; }""")
        assert bar["top"] == bar["header"], bar
        page.locator(".az-index__link").nth(3).click()
        page.wait_for_timeout(600)
        landed = page.evaluate("""() => document.getElementById(location.hash.slice(1)).getBoundingClientRect().top""")
        assert landed >= bar["bottom"], (landed, bar)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_faq_disclosure_opens_and_closes_from_the_keyboard(browser, site, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/faq/", wait_until="networkidle")
        page.focus("details.accordion__item > summary")
        page.keyboard.press("Enter")
        page.wait_for_timeout(200)
        first = page.locator("details.accordion__item").first
        assert first.evaluate("d => d.open")
        assert first.locator(".accordion__panel").is_visible()
        page.keyboard.press("Space")
        page.wait_for_timeout(200)
        assert not first.evaluate("d => d.open")
    finally:
        context.close()


#: where a head's words end, against its cell's reading edge: the right of the text's last box vs the cell's right (a
#: FAQ question's cell is its row, the summary, inside its padding)
ALIGN = r"""(selector) => [...document.querySelectorAll(selector)].map((el) => {
  const range = document.createRange();
  range.selectNodeContents(el);
  const right = Math.max(...[...range.getClientRects()].filter((r) => r.width > 0).map((r) => r.right));
  const row = el.closest('summary');
  const cell = row ? row.getBoundingClientRect().right - parseFloat(getComputedStyle(row).paddingRight)
                   : el.getBoundingClientRect().right;
  return {text: el.textContent.trim().slice(0, 32), gap: Math.round((cell - right) * 10) / 10};
})"""


@pytest.mark.parametrize("width", [1440, 390])
def test_the_latin_heads_of_the_arabic_pages_end_on_the_reading_edge(browser, site, content, width):
    """The review's M2: an Italian term, a French question, a French room — the inline end of their words on their
    cell's, the right of an Arabic page; and its m8: a French lead stands on the reading edge as a box the width of
    its words and reads from its own start, as a body does."""
    context = browser.new_context(viewport={"width": width, "height": 900 if width > 800 else 844})
    try:
        context.add_cookies([_session(content["member"], site)])
        page = context.new_page()
        for path, selector, required in (
            ("/ar/glossaire/", ".glossary-entry__term", True),
            ("/ar/forum-virtuel/", ".community-rooms__title[lang]", True),
            ("/ar/faq/", ".faq-item__question[lang]", False),
        ):
            page.goto(site + path, wait_until="networkidle")
            heads = page.evaluate(ALIGN, selector)
            assert heads or not required, (path, "no head to measure")
            off = [head for head in heads if abs(head["gap"]) > 1]
            assert off == [], (path, width, off)
        page.goto(f"{site}/ar/vivre-en-italie/", wait_until="networkidle")
        lead = page.evaluate(
            """() => { const p = document.querySelector('.page-header__lead[lang]');
                       if (!p) return null;
                       const header = p.closest('.page-header'), cs = getComputedStyle(header);
                       const edge = header.getBoundingClientRect().right - parseFloat(cs.paddingRight);
                       const style = getComputedStyle(p);
                       return {gap: edge - p.getBoundingClientRect().right, align: style.textAlign,
                               direction: style.direction}; }"""
        )
        if lead is not None:
            assert abs(lead["gap"]) <= 1 and lead["direction"] == "ltr", lead
            assert lead["align"] in ("start", "left"), lead
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_letter_band_holds_one_line_on_a_phone(browser, site, lang):
    """The review's m1: eight letters — 44 px cells — on one line from 360 px; never a letter left alone."""
    for width in (390, 360):
        context = browser.new_context(viewport={"width": width, "height": 844})
        try:
            page = context.new_page()
            page.goto(f"{site}/{lang}/glossaire/", wait_until="networkidle")
            band = page.evaluate(
                """() => { const links = [...document.querySelectorAll('.az-index__link')];
                           return {n: links.length, lines: new Set(links.map((a) => Math.round(a.getBoundingClientRect().top))).size,
                                   narrowest: Math.min(...links.map((a) => a.getBoundingClientRect().width)),
                                   overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
            )
            if band["n"] <= 8:
                assert band["lines"] == 1, (lang, width, band)
            assert band["narrowest"] >= 44 and band["overflow"] <= 0, (lang, width, band)
        finally:
            context.close()


def test_an_enquiry_form_s_first_legend_leaves_the_screen_to_its_chapter_s_title(browser, site):
    """The review's m6: «Votre message» then «Vos coordonnées et votre message» — one title on the screen; the legend
    stays the fieldset's name; the consent's group keeps its legend."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    try:
        page = context.new_page()
        page.goto(f"{site}/fr/contact/formulaire/", wait_until="networkidle")
        legends = page.evaluate(
            """() => [...document.querySelectorAll('.enquiry-form .form__legend')].map((l) => {
                     const r = l.getBoundingClientRect();
                     return {text: l.textContent.trim(), width: r.width, height: r.height}; })"""
        )
        assert len(legends) == 2 and legends[0]["text"], legends
        assert legends[0]["width"] <= 1 and legends[0]["height"] <= 1, "the first legend, off the screen"
        assert legends[1]["height"] > 20, "the consent's legend stays"
    finally:
        context.close()
