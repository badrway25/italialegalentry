"""
The mobile + RTL sweep's fixes, held — design V5.4, W4-A (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.6 item 1; SP-8,
N13 / N14, §2.5; docs/design-v5/QA/v54/w4-a/SWEEP.md, the defects D1 … D23, and NOTES.md).

What the sweep found and fixed, each in its owning family's file:

* under a finger every target answers on 44 px, and none is under the 24 px floor under a pointer (SP-8): the public
  footer's links (D1), the «aiuto» help line on the door and interior pages (D2), the pending legal notice's address
  (D3), orientation's resume link (D4), the passage's forward links and the consent's privacy link (D5), the closed
  registration's link (D6), the documents' foot links and «Télécharger» (D7), «Ma situation»'s Stepper from 360 px
  (D9), the dashboards' «Profil» (D10), a short arrow link (D11), the lock-up at 320 (D20);
* the company's contact phone reads left to right on the Arabic page (D8); a record's own title in another language
  is cut at its own end in the phone bar, with or without a `lang` (D16); a long word in an organisation's name wraps
  inside the head (D18); a video's controls never mirror (D19);
* the error pages' title opens a phone on its side (D12); the passage's station words are one step up on a phone
  (D21, W3-D's hand-off); the FAQ's hint keeps its guillemets with their words (D15);
* found by the after-sweep's look: a register row's reference or date, left to right on an Arabic page, opens with its
  point on the row's side, never closing the line (D22); a saved result's French title ends on the Arabic page's
  reading edge, wrapped or not (D23);
* W4-B's O1, handed to this area: a stop that Tab brings in from below keeps its whole ring on a phone;
* the fix pass (REVIEW.md, A11Y_PERF.md): a name in the other direction than the page — a file's on «Mes pièces» and
  the loose upload's answer, an answerable party's, a step's words and who answers for it, a table's cell, a
  company's own name in its dashboard's head, a reference in a record's facts — stands on the page's reading edge
  (M1); «Profil» keeps its block's start edge (m1); every notice's address answers on 44 px under a finger and 24
  under a pointer — the go-live notice on every public form included (finding 1); the console phone bar's account
  button keeps its whole ring on screen (finding 2).

A target is measured as the sweep measured it (C:/tmp/ile_v5_council/.work/w4-a/w4-a-impl-1/probe.js): through its
middle, `elementFromPoint` one pixel at a time until another element answers — a target's own `::before` / `::after`
area counts, a neighbour's does not. Chromium on the seeded site, the clock at 3 October 2026 through `core.clock.now`
(a frozen `time.monotonic` stalls Playwright); a session minted with `Client.force_login` — nothing typed, no password.
Emulated, and said so: no real iOS or Android device was used.
"""

from __future__ import annotations

import datetime as dt
import os
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.test import Client
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]

#: the hit extent of each element a selector names: its box, and how far beyond it a point still lands on it
HIT_JS = """async ([sel, step]) => {
  const out = [];
  const els = [...document.querySelectorAll(sel)].filter((el) => el.getClientRects().length && el.checkVisibility());
  for (const el of els) {
    el.scrollIntoView({block: 'center', behavior: 'instant'});
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const own = (x, y) => { if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) return false;
      const h = document.elementFromPoint(x, y); return !!h && (h === el || el.contains(h)); };
    let up = 0, dn = 0, lf = 0, rt = 0;
    while (up < 40 && own(cx, r.top - up - step)) up += step;
    while (dn < 40 && own(cx, r.bottom + dn)) dn += step;
    while (lf < 40 && own(r.left - lf - step, cy)) lf += step;
    while (rt < 40 && own(r.right + rt, cy)) rt += step;
    out.push({text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40), box: [Math.round(r.width), Math.round(r.height)],
              hit: [Math.round(r.width + lf + rt), Math.round(r.height + up + dn)], middle: own(cx, cy)});
  }
  return out;
}"""

OVERFLOW_JS = "document.documentElement.scrollWidth - document.documentElement.clientWidth"


def _css(path: str) -> str:
    return re.sub(r"/\*.*?\*/", "", (ROOT / path).read_text(encoding="utf-8"), flags=re.S)


# ---------------------------------------------------------------------------------------------- the sheets


def test_the_colophon_and_the_lock_up_answer_on_44px_under_a_finger():
    """D1, D20 (v5/chrome.css, W2-C1): the footer's rows are its links' own 44 px under a finger, its gap folded in;
    the lock-up's link is 44 px wide even where it is the mark alone."""
    chrome = _css("static/css/v5/chrome.css")
    coarse = "".join(re.findall(r"@media \(pointer: coarse\) \{(.*?)\n\}", chrome, flags=re.S))
    assert re.search(r"\.site-footer__list \{ gap: 0; \}", coarse), "the list's gap folds into the 44 px rows"
    assert re.search(
        r"\.site-footer a \{ min-block-size: var\(--hit-primary\); min-inline-size: var\(--hit-primary\); \}", coarse
    ), "a short word of the colophon is 44 px wide too («Projet», «تنبيه»)"
    brand = re.search(r"\n\.brand \{([^}]*)\}", chrome).group(1)
    assert "min-inline-size: var(--hit-primary)" in brand and "min-block-size: var(--hit-primary)" in brand


def test_a_short_arrow_link_is_widened_about_its_middle():
    """D11 (v5/buttons.css, W1-C): the arrow link's 44 px band is 44 px wide too where its word is shorter."""
    buttons = _css("static/css/v5/buttons.css")
    rule = re.search(r"\.link-arrow::after \{([^}]*)\}", buttons).group(1)
    # half the word's width less half the 44 px, as the block axis: the same expression, a width on this axis
    assert "inset-inline: min(0px, calc(50% - var(--hit-primary) / 2))" in rule, rule


def test_what_scrolls_into_view_keeps_its_rings_room_at_the_foot():
    """W4-B's O1 (v5/chrome.css §3, W2-C1): the public pages' scroll padding keeps the letterhead's clearance at the top
    and 8 px at the foot — the focus ring's 2 + 2 px, which the screen's edge cut off on a phone."""
    chrome = _css("static/css/v5/chrome.css")
    assert re.search(
        r"html:has\(\.site-header\) \{ scroll-padding-block: calc\(var\(--header-h\) \+ var\(--s-4\)\) var\(--s-2\); \}",
        chrome,
    )


def test_the_help_line_and_the_consent_link_are_drawn_once_for_every_page_that_carries_them():
    """D2, D5: the shared page partial draws their 44 px area for every page (the doors' and interior pages' too);
    the reading pages' list no longer names them — one drawing (the owner's V5.8 rule 3)."""
    pagina = _css("static/css/v5/_pagina.css")
    assert re.search(r"\.form__privacy-link a \{\s*display: inline-block;", pagina)
    assert ":is(.aiuto, .form__privacy-link) a::after" in pagina
    lettura = _css("static/css/v5/_lettura.css")
    for selector in (".aiuto a", ".form__privacy-link a", ".legal-page__pending .notice__body a"):
        assert selector not in lettura, f"{selector} is drawn by v5/_pagina.css or v5/notice.css now"


def test_a_notices_address_is_drawn_once_for_every_notice():
    """The accessibility check's finding 1: the go-live notice's address (every public form while G2 is closed) and the
    pending legal page's (D3) are one rule of the notice's own sheet — one box of its line and 2 px, a 44 px band under
    a finger; the reading pages' sheet that drew D3 no longer does (the Forum's closed registration keeps D6)."""
    notice = _css("static/css/v5/notice.css")
    assert re.search(r"\.notice__body \.email \{ display: inline-block; padding-block: 2px; \}", notice)
    coarse = re.search(r"@media \(pointer: coarse\) \{(.*?)\n\}", notice, flags=re.S).group(1)
    assert ".notice__body .email { position: relative; }" in coarse
    assert re.search(r"\.notice__body \.email::after \{[^}]*inset-block: -10px; inset-inline: 0;", coarse)
    for template in ("components/form_unavailable.html", "legal/document.html"):
        assert '<a class="email" href="mailto:{{ site.contact_email }}">' in (ROOT / "templates" / template).read_text(
            encoding="utf-8"
        ), template


def test_the_documents_links_stand_on_24px_and_their_bands_never_overlap():
    """D7 (W3-C's partials, «Mes pièces»' page-only sheet): the foot's links and «Télécharger» are 24 px boxes; two
    foot links that wrap stand 20 px apart under a finger, so that their 44 px bands meet without overlapping."""
    workspace = _css("apps/portal/static/portal/v5/_workspace.css")
    assert re.search(r"\n\.doc-aside a \{\s*padding-block: 2px;\s*\}", workspace)
    coarse = workspace.split(".doc-aside {\n    row-gap: var(--s-5);", 1)
    assert len(coarse) == 2, "under a finger the foot's rows stand 20 px apart"
    depot = _css("apps/portal/static/portal/v5/_depot.css")
    assert re.search(r"\n\.doc-version__get a \{\s*padding-block: 2px;\s*\}", depot)


def test_the_page_only_sheets_hold_the_rest():
    """D4, D5, D6, D9, D10, D12, D16, D18, D19, D21 — each in the sheet of the family that draws it."""
    wizard = _css("apps/orientation/static/orientation/wizard.css")
    assert re.search(r"\.wizard-intro__resume-link a \{\s*display: inline-block;", wizard)
    pathways = _css("apps/pathways/static/pathways/_pathways.css")
    assert re.search(r"\.linea__more a \{\s*display: inline-block;", pathways)
    forum = _css("apps/forum/static/forum/_forum.css")
    assert re.search(r"\.forum-gallery__video \{\s*direction: ltr;", forum), "a video's controls never mirror"
    assert '[data-registration="closed"] .notice__body a::after' in forum
    stepper = _css("apps/portal/static/portal/v5/_journey-stepper.css")
    # through its rail: the base sheet's list reset (`ol[role="list"]`, 0-1-1) outranks the class alone
    rule = re.search(r"\.wiz__rail \.wstep \{([^}]*)\}", stepper).group(1)
    assert "margin-inline: max(calc(-1 * var(--page-pad)), min(0px, calc((100% - 8 * var(--hit-primary)) / 2)))" in rule
    dashboard = _css("apps/portal/static/portal/v5/_dashboard.css")
    rule = re.search(r"\.db-account__links a \{([^}]*min-inline-size[^}]*)\}", dashboard).group(1)
    assert "min-inline-size: var(--hit-primary)" in rule and "min-block-size: var(--hit-primary)" in rule
    assert "justify-content" not in rule, "the review's m1: the box grows at its end, «Profil» keeps the start edge"
    shell = _css("apps/portal/static/portal/v5/_shell.css")
    title = re.search(r"\.console-bar__title \{([^}]*)\}", shell).group(1)
    assert "unicode-bidi: plaintext" in title and "text-overflow: ellipsis" in title
    frame = _css("apps/portal/static/portal/v5/_frame.css")
    assert re.search(r"\.ctx__words,\s*\.ws-head__words \{\s*min-inline-size: 0;", frame)
    errori = _css("apps/cms/static/cms/errori.css")
    assert "@media (min-width: 64rem), (min-width: 48rem) and (max-height: 30rem)" in errori
    passage = _css("static/css/v5/_journey-passage.css")
    assert re.search(r"@media \(max-width: 63\.999rem\) \{\s*\.linea__text \{\s*font-size: var\(--t-body\);", passage)


def test_a_part_in_the_other_direction_opens_with_its_point_on_the_rows_side():
    """D22, D23 (W3-E's v5/_registers.css): a reference, a date or a name in its own script — the other direction than
    its meta row — lays its point and its pull on the row's side; a saved result's French title takes the head rule
    (its lines on the Arabic page's reading edge), which `:dir()` alone missed: its `lang` turns it, not a `dir`."""
    registers = _css("apps/portal/static/portal/v5/_registers.css")
    rule = re.search(
        r":is\(\.reg-row__meta, \.reg-step__meta\):dir\(rtl\) > :is\(\.reg-ref, time, :dir\(ltr\)\),\s*"
        r":is\(\.reg-row__meta, \.reg-step__meta\):dir\(ltr\) > :dir\(rtl\) \{([^}]*)\}",
        registers,
    )
    assert rule, "the other-direction part's rule"
    body = rule.group(1)
    assert "flex-direction: row-reverse" in body and "margin-inline: 0 calc(-1 * var(--meta-sep))" in body, body
    head = re.search(r"(:dir\(rtl\) :is\(\.reg-head__title[^{]*)\{\s*text-align: end;", registers)
    assert head and ':dir(rtl) .reg-result__title:is([lang="fr"], [lang="it"], [lang="en"])' in head.group(1)


def test_a_name_in_the_other_direction_stands_on_the_pages_reading_edge():
    """The review's M1 and what the survey of its class found: a block that `dir="auto"` turns (a file's name, the loose
    upload's answer, an answerable party's name, a step's words, who answers for a step, a table's cell) ends on the
    page's reading edge — the registers' head rule, in the owning sheets; a reference in a record's facts packs to its
    cell's reading edge; the company's own name is an isolate in the page's own head, its box rule gone."""
    for sheet, cls in (
        ("apps/portal/static/portal/v5/_table.css", ".doc-files__name"),
        ("apps/portal/static/portal/v5/_depot.css", ".doc-filed__name"),
    ):
        css = _css(sheet)
        assert re.search(
            rf":dir\(rtl\) {re.escape(cls)}:dir\(ltr\),\s*:dir\(ltr\) {re.escape(cls)}:dir\(rtl\) \{{\s*text-align: end;",
            css,
        ), sheet
    registers = _css("apps/portal/static/portal/v5/_registers.css")
    names = ".reg-head__title, .reg-row .db-task__title, .reg-party__name, .reg-step__text, .db-task__who, .data-table [dir]"
    assert f":dir(rtl) :is({names}):dir(ltr)," in registers and f":dir(ltr) :is({names}):dir(rtl)," in registers
    assert re.search(r"\.reg-summary \.summary__item:dir\(rtl\) > \.reg-ref \{\s*justify-content: flex-end;", registers)
    assert ".ctx__title[dir]" not in _css("apps/portal/static/portal/v5/_dashboard.css")
    template = (ROOT / "templates" / "companies" / "dashboard.html").read_text(encoding="utf-8")
    assert '<h1 class="ctx__title"><span dir="auto">{{ company.legal_name }}</span></h1>' in template
    profile = (ROOT / "templates" / "companies" / "profile.html").read_text(encoding="utf-8")
    assert '<dd><span dir="auto">{{ company.legal_name }}</span></dd>' in profile and '<dd dir="auto">' not in profile


def test_a_team_written_sentence_keeps_its_period_at_its_end_on_the_arabic_page():
    """The look at the whole pages (the review's M1, item 3): a French sentence an actor or the team wrote — an
    authorisation's scope, a piece of evidence and its detail, a step's note in the process's journal — is an isolate,
    so that on the Arabic page its period stays at its end («.Documents déposés…» before); the detail and the note
    then stand on the reading edge by the registers' head rule."""
    responsible = (ROOT / "templates" / "selection" / "partials" / "responsible.html").read_text(encoding="utf-8")
    assert '<span class="responsible__scope"><span dir="auto">{{ actor.scope_note }}</span></span>' in responsible
    process = (ROOT / "templates" / "selection" / "process.html").read_text(encoding="utf-8")
    assert '<span dir="auto">{{ row.requirement }}</span>' in process
    assert '<span class="t-caption" dir="auto">{{ row.detail }}</span>' in process
    assert """<td data-label="{% translate 'Note' %}" dir="auto">{{ event.note|default:"—" }}</td>""" in process


def test_a_loose_files_act_answers_on_44px_under_a_finger():
    """Found by the fix pass's accessibility pass: the loose files' «Supprimer» — «حذف», a 31 px word in Arabic — is
    44 px wide about its middle under a finger (the icon buttons' own band), and nothing moves."""
    table = _css("apps/portal/static/portal/v5/_table.css")
    coarse = re.search(r"@media \(pointer: coarse\) \{(.*?)\n\}", table, flags=re.S).group(1)
    assert re.search(
        r"\.doc-files__act \.btn::before \{[^}]*inset-inline: min\(0px, calc\(50% - var\(--hit-primary\) / 2\)\);",
        coarse,
    )


def test_the_phone_bars_account_button_draws_its_ring_inside_its_box():
    """The accessibility check's finding 2: the button stands 2 px under the screen's top — its ring is inset."""
    shell = _css("apps/portal/static/portal/v5/_shell.css")
    assert re.search(
        r"\.console-bar \.account-menu__summary:focus-visible \{\s*outline-offset: calc\(-2 \* var\(--focus-ring-width\)\);",
        shell,
    )


def test_the_companys_contact_reads_left_to_right_in_its_own_isolates():
    """D8 (companies/profile.html, W3-E): the e-mail and the phone are each a left-to-right isolate — a phone number in
    an Arabic paragraph otherwise lays its digit groups out right to left («000000 0000 39+»)."""
    template = (ROOT / "templates" / "companies" / "profile.html").read_text(encoding="utf-8")
    assert '<span dir="ltr">{{ company.contact_email }}</span>' in template
    assert '<span dir="ltr">{{ company.contact_phone }}</span>' in template


@pytest.mark.django_db
def test_the_faq_hint_keeps_its_guillemets_with_their_words(client, seeded, phase3_open):
    """D15: the hint is a team-authored string, French spacing applies (pages_typo.py): a phone no longer breaks a line
    before «»» or after «««."""
    html = client.get("/fr/faq/").content.decode()
    hint = re.search(r'<p class="search-form__help" id="faq-q-help">(.*?)</p>', html).group(1)
    assert "«\u00a0visa\u00a0»" in hint and "«\u00a0diplôme\u00a0»" in hint, hint


def test_the_500_keeps_its_semicolon_with_its_words():
    """D15: the 500's sentence (a catalogue string, drawn with no database) never starts a line with «; vous pouvez
    réessayer» — the typo filter reads no table, only the registry in memory."""
    from django.test import RequestFactory
    from django.utils import translation

    from core import views as core_views

    request = RequestFactory().get("/fr/une-adresse/")
    with translation.override("fr"):
        html = core_views.error_500(request).content.decode()
    text = re.search(r'<p class="error-page__text">(.*?)</p>', html, flags=re.S).group(1)
    assert "informées\u00a0; vous pouvez" in text, text


def test_the_strings_the_review_named_keep_their_guillemets_with_their_words():
    """The review's m2, the strings it names: «Lire la page « Attention aux fraudes »» (the phone sheet's foot and the
    portico's, the anti-fraud callout, orientation's warnings) and the training page's two links pass W2-D's `typo`
    filter — a phone never starts a line with «»» nor ends one on «««; the other team-authored lines are W4-D's, beside
    D14 (NOTES)."""
    fraud = '{% translate "Lire la page « Attention aux fraudes »" as fraud_label %}{{ fraud_label|typo }}'
    for template, count in (
        ("partials/main_nav.html", 2),
        ("pathways/_antifraud_callout.html", 1),
        ("orientation/result.html", 1),
    ):
        source = (ROOT / "templates" / template).read_text(encoding="utf-8")
        assert source.count(fraud) == count and "pages_typo" in source.splitlines()[0], template
    training = (ROOT / "templates" / "pathways" / "training.html").read_text(encoding="utf-8")
    assert "{{ origin_label|typo }}" in training and "{{ living_label|typo }}" in training
    assert "pages_typo" in training.splitlines()[0]


# ---------------------------------------------------------------------------------------------- in the browser


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
def third_october(set_flag, monkeypatch):
    """Gate G3 open, the Forum's registration closed (the event was on 2 October): the clock through core.clock."""
    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _context(browser, live_server, width, height, touch, user=None):
    options = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
    if touch:
        options.update(is_mobile=True, has_touch=True)
    context = browser.new_context(**options)
    if user is not None:
        client = Client()
        client.force_login(user)
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


#: the legal texts published (the forms open: the companies' consent is drawn) …
PUBLIC_TARGETS = (
    ("/fr/", ".site-footer a"),
    ("/ar/", ".site-footer a"),
    ("/fr/parcours/", ".aiuto a"),
    ("/fr/entreprises/", ".aiuto a, .form__privacy-link a"),
    ("/ar/entreprises/", ".form__privacy-link a"),
    ("/fr/orientation/", ".wizard-intro__resume-link a"),
    ("/fr/formation/", ".linea__more a"),
    ("/fr/forum/inscription/", '[data-registration="closed"] .notice__body a'),
    ("/ar/le-projet/", ".chapter__more > a.link-arrow"),
)
#: … or not yet (a legal page says it is being prepared, with the address to write to; every public form is the
#: go-live notice, with the same address — the accessibility check's finding 1)
PENDING_TARGETS = (
    ("/fr/privacy-policy/", ".legal-page__pending .notice__body a"),
    ("/ar/condizioni-di-utilizzo/", ".legal-page__pending .notice__body a"),
    ("/fr/contact/formulaire/", ".form-unavailable .notice__body a"),
    ("/ar/entreprises/recueil-des-besoins/", ".form-unavailable .notice__body a"),
    ("/fr/entreprises/", ".form-unavailable .notice__body a"),
)


def _check_targets(page, live_server, targets, touch):
    for path, selector in targets:
        page.goto(live_server.url + path, wait_until="load")
        page.evaluate("document.fonts.ready")
        found = page.evaluate(HIT_JS, [selector, 1])
        assert found, (path, selector, "nothing to measure: the page no longer draws it")
        for target in found:
            where = (path, target)
            assert target["middle"], where
            if touch:
                assert target["hit"][0] >= 43.5 and target["hit"][1] >= 43.5, where
            else:
                assert target["box"][1] >= 23.5, where
        assert page.evaluate(OVERFLOW_JS) <= 0, (path, "the page never wider than the phone")


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("touch", [True, False], ids=["finger", "pointer"])
def test_every_stand_alone_link_answers_on_44px_under_a_finger_and_24_under_a_pointer(
    browser, live_server, seeded, legal_published, third_october, touch
):
    """SP-8 on the public pages the sweep found short: 44 × 44 under a finger at 390, a 24 px box at least under a
    pointer (a narrowed desktop window)."""
    context = _context(browser, live_server, 390, 844, touch)
    page = context.new_page()
    try:
        _check_targets(page, live_server, PUBLIC_TARGETS, touch)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("touch", [True, False], ids=["finger", "pointer"])
def test_a_notices_address_answers_on_its_targets_while_the_legal_texts_are_awaited(
    browser, live_server, seeded, third_october, touch
):
    """D3 and the accessibility check's finding 1 — the release state (G2 closed): a legal page's one link and every
    public form's go-live notice's, the address, is a 24 px box at least, 44 px under a finger (it was its 20 px run,
    23 in Arabic, with no band)."""
    context = _context(browser, live_server, 390, 844, touch)
    page = context.new_page()
    try:
        _check_targets(page, live_server, PENDING_TARGETS, touch)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_lock_up_answers_on_44px_at_320(browser, live_server, seeded, third_october):
    """D20: at 320 the lock-up is the mark alone, 38 px wide — its link is 44, and the row still fits."""
    context = _context(browser, live_server, 320, 640, True)
    page = context.new_page()
    try:
        for lang in ("fr", "ar"):
            page.goto(f"{live_server.url}/{lang}/", wait_until="load")
            box = page.evaluate(
                "(() => { const r = document.querySelector('.site-header .brand').getBoundingClientRect(); return [r.width, r.height]; })()"
            )
            assert box[0] >= 43.5 and box[1] >= 43.5, (lang, box)
            assert page.evaluate(OVERFLOW_JS) <= 0, lang
    finally:
        context.close()


@pytest.fixture
def company_with_a_phone(db, user_factory):
    from accounts.models import (
        AccountVerification,
        Membership,
        MembershipRole,
        Organisation,
        OrganisationKind,
        VerificationStatus,
    )
    from companies.models import CompanyProfile

    user = user_factory("w4a.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    organisation = Organisation.objects.create(
        name="Organisation W4-A", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    AccountVerification.objects.create(
        user=user, declared_type=AccountType.COMPANY, status=VerificationStatus.APPROVED, decided_at=timezone.now()
    )
    CompanyProfile.objects.create(
        organisation=organisation,
        legal_name="Cantiere W4-A S.r.l.",
        contact_name="Référent W4-A",
        contact_function="Responsable",
        contact_email="referent-w4a@example.test",
        contact_phone="+39 041 234 5678",
        city="Rovigo",
        country="IT",
    )
    return user


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_companys_phone_number_keeps_its_order_on_the_arabic_page(browser, live_server, company_with_a_phone):
    """D8: its digit groups stand left to right — «+39», then «041», «234», «5678» — inside a right-to-left row."""
    context = _context(browser, live_server, 390, 844, True, company_with_a_phone)
    page = context.new_page()
    try:
        url = f"{live_server.url}/ar/espace-reserve/entreprise/mon-entreprise/"
        page.goto(url, wait_until="load")
        page.goto(url, wait_until="load")
        groups = page.evaluate(
            """() => { const span = [...document.querySelectorAll('.portal-facts__row dd span[dir="ltr"]')]
                .find((s) => s.textContent.includes('041'));
              const node = span.firstChild, text = node.textContent, out = [];
              for (const m of text.matchAll(/\\S+/g)) { const r = document.createRange(); r.setStart(node, m.index);
                r.setEnd(node, m.index + m[0].length); out.push([m[0], r.getBoundingClientRect().left]); }
              return {dir: getComputedStyle(span).direction, groups: out}; }"""
        )
        assert groups["dir"] == "ltr", groups
        lefts = [left for _, left in groups["groups"]]
        assert [word for word, _ in groups["groups"]] == ["+39", "041", "234", "5678"], groups
        assert lefts == sorted(lefts), f"the groups run left to right: {groups['groups']}"
    finally:
        context.close()


@pytest.fixture
def person(db, user_factory):
    from core import clock

    return user_factory(
        "w4a.person@example.test",
        role=roles.PERSON,
        full_name="Personne W4-A",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_records_own_title_in_another_language_is_cut_at_its_own_end(browser, live_server, seeded, person):
    """D16: a French title with no `lang` in the Arabic phone bar keeps its first words — the ellipsis at its end."""
    context = _context(browser, live_server, 320, 568, True, person)
    page = context.new_page()
    try:
        url = f"{live_server.url}/ar/espace-reserve/mes-demandes/"
        page.goto(url, wait_until="load")
        page.goto(url, wait_until="load")
        cut = page.evaluate(
            """() => { const title = document.querySelector('.console-bar__title');
              title.textContent = 'Culture du travail et organisation de l’entreprise en Italie';
              const node = title.firstChild, r = document.createRange(); r.setStart(node, 0); r.setEnd(node, 7);
              const first = r.getBoundingClientRect(), box = title.getBoundingClientRect(), s = getComputedStyle(title);
              return {bidi: s.unicodeBidi, clipped: title.scrollWidth > title.clientWidth + 1,
                      firstInside: first.left >= box.left - 0.5 && first.right <= box.right + 0.5,
                      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
        )
        assert cut["bidi"] == "plaintext" and cut["clipped"], cut
        assert cut["firstInside"], "the title's first words are on screen: the cut is at its own end"
        assert cut["overflow"] <= 0, cut
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_steppers_columns_hold_44px_from_360(browser, live_server, seeded, person, lang):
    """D9: eight columns of 44 px from 360 (the row takes from the gutters what it lacks); never wider than the phone."""
    context = _context(browser, live_server, 360, 800, True, person)
    page = context.new_page()
    try:
        url = f"{live_server.url}/{lang}/espace-reserve/ma-situation/"
        page.goto(url, wait_until="load")
        page.goto(url, wait_until="load")
        for width in (360, 375, 320):
            page.set_viewport_size({"width": width, "height": 800})
            page.wait_for_timeout(100)
            widths = page.evaluate(
                "[...document.querySelectorAll('.wstep__link')].map((a) => a.getBoundingClientRect().width)"
            )
            assert len(widths) == 8, widths
            if width >= 360:
                assert min(widths) >= 43.5, (lang, width, widths)
            assert page.evaluate(OVERFLOW_JS) <= 0, (lang, width)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_error_pages_title_opens_a_phone_on_its_side(browser, live_server, seeded, lang):
    """D12: at 844 × 390 the door takes the end seat and the title stands whole in the first screen."""
    context = _context(browser, live_server, 844, 390, True)
    page = context.new_page()
    try:
        response = page.goto(f"{live_server.url}/{lang}/page-inexistante/", wait_until="load")
        assert response.status == 404
        place = page.evaluate(
            """() => { const t = document.querySelector('.error-page h1').getBoundingClientRect();
              const d = document.querySelector('.error-page__door').getBoundingClientRect();
              const b = document.querySelector('.error-page__body').getBoundingClientRect();
              return {titleBottom: t.bottom, vh: innerHeight, beside: d.top < b.bottom && (d.left >= b.right || d.right <= b.left)}; }"""
        )
        assert place["titleBottom"] <= place["vh"], place
        assert place["beside"], "the door stands beside the words, not above them"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_station_words_read_one_step_up_on_a_phone(browser, live_server, seeded, third_october):
    """D21: the passage's station words at 17 px below 64rem (RE-4), at 15 px on a desktop."""
    for width, size in ((390, "17px"), (1440, "15px")):
        context = _context(browser, live_server, width, 900, width < 1000)
        page = context.new_page()
        try:
            page.goto(f"{live_server.url}/fr/orientation/", wait_until="load")
            sizes = page.evaluate(
                "[...document.querySelectorAll('.linea__text')].map((e) => getComputedStyle(e).fontSize)"
            )
            assert sizes and set(sizes) == {size}, (width, sizes)
        finally:
            context.close()


@pytest.fixture
def person_with_a_request(person):
    """One contact request linked to the account: «Mes demandes» draws its row, «Demande de contact · contact-N»."""
    from consents.services import record_consent
    from enquiries.models import ContactRequest

    consent = record_consent(None, "contact", email=person.email, user=person, language="fr")
    obj = ContactRequest(
        email=person.email,
        consent=consent,
        owner=person,
        language="fr",
        name="Personne W4-A",
        subject="Objet W4-A",
        message="Message W4-A",
    )
    obj.duplicate_hash = obj.compute_duplicate_hash()
    obj.save()
    return person


#: each meta row's parts: which side of its box the point lies on (the part's box against its words' own range)
POINT_SIDES_JS = """() => [...document.querySelectorAll('.reg-row__meta, .reg-step__meta')].map((row) => {
  const box = row.getBoundingClientRect();
  return {rtl: getComputedStyle(row).direction === 'rtl', parts: [...row.children].map((part) => {
    const p = part.getBoundingClientRect(), r = document.createRange(); r.selectNodeContents(part);
    const t = r.getBoundingClientRect(), left = t.left - p.left, right = p.right - t.right;
    return {text: part.textContent.trim(), side: right > left + 2 ? 'right' : (left > right + 2 ? 'left' : 'none'),
            shown: right > left ? p.right <= box.right + 0.5 : p.left >= box.left - 0.5};
  })};
})"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_reference_opens_with_its_point_on_the_rows_side(browser, live_server, seeded, person_with_a_request, lang):
    """D22: «Demande de contact · contact-N» — the reference reads left to right on the Arabic page and still opens with
    its point between the two parts, none closing the line; D23: a saved result's French title, two lines on a phone,
    ends on the reading edge (the title drawn by the registers' sheet this page links, its markup as «Mon parcours»
    writes it)."""
    context = _context(browser, live_server, 390, 844, True, person_with_a_request)
    page = context.new_page()
    try:
        url = f"{live_server.url}/{lang}/espace-reserve/mes-demandes/"
        page.goto(url, wait_until="load")
        page.goto(url, wait_until="load")
        rows = page.evaluate(POINT_SIDES_JS)
        assert rows, "the request's row draws its meta line"
        for row in rows:
            want = "right" if row["rtl"] else "left"
            assert row["rtl"] == (lang == "ar"), row
            assert all(part["side"] == want for part in row["parts"]), row
            assert [part["shown"] for part in row["parts"]] == [False] + [True] * (len(row["parts"]) - 1), (
                "the first part's point is clipped, every other one stands between two parts",
                row,
            )
        lines = page.evaluate(
            """() => { const article = document.createElement('article'); article.className = 'reg-result';
              article.innerHTML = '<h2 class="reg-result__title" lang="fr">Orientation vers un parcours de travail salarié</h2>';
              const host = document.querySelector('.reg-results, .reg-page, main'); host.prepend(article);
              const title = article.firstElementChild, box = article.getBoundingClientRect();
              const r = document.createRange(); r.selectNodeContents(title);
              return [...r.getClientRects()].map((x) => [Math.round(x.left - box.left), Math.round(box.right - x.right)]); }"""
        )
        assert len(lines) >= 2, ("the title wraps on a phone", lines)
        edge = 1 if lang == "ar" else 0  # the reading edge: the right on the Arabic page, the left on the French
        assert all(line[edge] <= 1 for line in lines), (lang, lines)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_stop_brought_in_from_below_keeps_its_whole_ring(browser, live_server, seeded, third_october, lang):
    """W4-B's O1: on the home at 390 × 844, with a keyboard, no focus ring is cut by the screen's bottom edge — the
    stops Tab brings in from below («Autres voies régulières», «Découvrir le projet pilote» were cut by 2 to 4 px)."""
    context = _context(browser, live_server, 390, 844, False)
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/{lang}/", wait_until="load")
        page.evaluate("document.fonts.ready")
        cuts, seen = [], 0
        for _ in range(45):
            page.keyboard.press("Tab")
            ring = page.evaluate(
                """() => { const el = document.activeElement;
                  if (!el || el === document.body) return null;
                  const r = el.getBoundingClientRect(); if (!r.width && !r.height) return null;
                  const s = getComputedStyle(el);
                  const extent = s.outlineStyle === 'none' ? 0 : parseFloat(s.outlineWidth) + parseFloat(s.outlineOffset);
                  return {text: (el.textContent || '').trim().slice(0, 40), cut: r.bottom + extent - innerHeight}; }"""
            )
            if ring is None:
                continue
            seen += 1
            if ring["cut"] > 0.5:
                cuts.append(ring)
        assert seen >= 20, ("the page offers its stops to the keyboard", seen)
        assert not cuts, cuts
    finally:
        context.close()


# ---------------------------------------------------------------------------------------------- the fix pass

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)

#: each element's lines (its range's client rects, grouped by line): their gap to its content box's left and right
#: edges, with its own direction and its parent's
EDGE_JS = """(sel) => [...document.querySelectorAll(sel)].filter((el) => el.getClientRects().length).map((el) => {
  const s = getComputedStyle(el), r = el.getBoundingClientRect();
  const left = r.left + parseFloat(s.borderLeftWidth) + parseFloat(s.paddingLeft);
  const right = r.right - parseFloat(s.borderRightWidth) - parseFloat(s.paddingRight);
  const range = document.createRange(); range.selectNodeContents(el);
  const lines = [];
  for (const x of range.getClientRects()) {
    if (x.width < 1) continue;
    const line = lines.find((l) => Math.abs(l.top - x.top) < 4);
    if (line) { line.l = Math.min(line.l, x.left); line.r = Math.max(line.r, x.right); }
    else lines.push({top: x.top, l: x.left, r: x.right});
  }
  return {text: el.textContent.trim().slice(0, 40), own: s.direction, parent: getComputedStyle(el.parentElement).direction,
          lines: lines.map((l) => [Math.round(l.l - left), Math.round(right - l.r)])};
})"""


def _turned_on_the_reading_edge(rows, rtl):
    """The rows whose direction is not their parent's — each of their lines ends on the page's reading edge."""
    edge = 1 if rtl else 0  # the right on the Arabic page, the left on the French
    turned = [row for row in rows if row["own"] != row["parent"]]
    for row in turned:
        assert row["lines"] and all(line[edge] <= 1 for line in row["lines"]), row
    return turned


def _at_rest(page, url):
    page.goto(url, wait_until="load")
    page.goto(url, wait_until="load")  # the first console page of a session carries the loader's entrance release
    page.evaluate("document.fonts.ready")


@pytest.fixture
def person_with_pieces(person, settings, tmp_path):
    """Files in both directions: a piece filed as «diploma.pdf», one as «شهادة الميلاد.pdf», and two loose files."""
    from django.core.files.uploadedfile import SimpleUploadedFile

    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services
    from documents.models import AccessClass, DocumentKind

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    for code, title, name in (
        ("diploma", "Diplôme ou titre de formation", "diploma.pdf"),
        ("civil", "Acte d’état civil légalisé", "شهادة الميلاد.pdf"),
    ):
        requirement = services.declare_requirement(
            case, code=code, title=title, responsible_actor="person", access_class=AccessClass.CASE
        )
        services.file_version(requirement, person, SimpleUploadedFile(name, MINIMAL_PDF, "application/pdf"))
    for name in ("passeport-scan.pdf", "عقد العمل.pdf"):
        services.store_upload(person, SimpleUploadedFile(name, MINIMAL_PDF, "application/pdf"), DocumentKind.OTHER)
    return person


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", [390, 1440])
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_files_name_in_the_other_direction_stands_on_the_reading_edge(
    browser, live_server, person_with_pieces, lang, width
):
    """The review's M1: on «Mes pièces» and on the loose files' register, «diploma.pdf» on the Arabic page and
    «شهادة الميلاد.pdf» on the French one end on the page's reading edge, with their gloss and the column's head — a card
    at 390, a cell at 1440 (they stood 198 and 428 px from it); the loose upload's answer names its file the same way."""
    context = _context(browser, live_server, width, 900, width < 1000, person_with_pieces)
    context.add_cookies([{"name": settings.LANGUAGE_COOKIE_NAME, "value": lang, "url": live_server.url}])
    page = context.new_page()
    try:
        for path in (f"/{lang}/espace-reserve/mes-documents/", "/documents/"):
            _at_rest(page, live_server.url + path)
            rows = page.evaluate(EDGE_JS, ".doc-files__name")
            assert rows, (path, "the files' register draws its names")
            assert _turned_on_the_reading_edge(rows, lang == "ar"), (path, "a name in the other direction", rows)
            assert page.evaluate(OVERFLOW_JS) <= 0, path
        _at_rest(page, live_server.url + "/documents/upload/")
        name = "diploma.pdf" if lang == "ar" else "شهادة الميلاد.pdf"
        page.evaluate(
            """(name) => { const block = document.querySelector('template[data-depot-block="filed"]').content.cloneNode(true);
              const el = block.querySelector('[data-depot-filed-name]'); el.hidden = false; el.textContent = name;
              block.querySelector('[data-depot-filed-text]').textContent = document.documentElement.lang === 'ar'
                ? 'تم إيداع الملف في سجل وثائقكم.' : 'Le fichier est déposé dans votre registre.';
              document.querySelector('[data-depot]').append(block); }""",
            name,
        )
        rows = page.evaluate(EDGE_JS, ".doc-filed__name")
        assert len(_turned_on_the_reading_edge(rows, lang == "ar")) == 1, rows
    finally:
        context.close()


@pytest.fixture
def person_with_parties(person, user_factory):
    """A file and who intervenes on it: an organisation named in Latin, one named in Arabic."""
    from accounts.models import Organisation, OrganisationKind
    from cases.models import AssignmentRole, CasePurpose
    from cases.services import assign, open_case

    actor = user_factory("w4a.actor@example.test", role=roles.AUTHORISED_ACTOR)
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    for name, role, reference in (
        ("Agenzia Formazione Veneto S.r.l.", AssignmentRole.AUTHORISED_ACTOR, "SYNTH-AUT-2026-0311"),
        ("مركز التكوين المهني بالرباط", AssignmentRole.TRAINING_BODY, ""),
    ):
        organisation = Organisation.objects.create(
            name=name, kind=OrganisationKind.COMPANY, country="IT", city="Padova"
        )
        assign(
            case,
            actor,
            role=role,
            organisation=organisation,
            authorisation_reference=reference,
            authorisation_jurisdiction="IT-VEN" if reference else "",
            authorisation_valid_until=timezone.localdate() + dt.timedelta(days=300) if reference else None,
        )
    return person, case


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", [390, 1440])
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_an_answerable_partys_name_stands_on_the_reading_edge(
    browser, live_server, seeded, person_with_parties, lang, width
):
    """The review's M1, its second site: in the file's «Qui intervient», a Latin organisation's name on the Arabic page
    and an Arabic one on the French page end on the page's reading edge, under their label (60 and 428 px short of it)."""
    person, case = person_with_parties
    context = _context(browser, live_server, width, 900, width < 1000, person)
    page = context.new_page()
    try:
        _at_rest(page, f"{live_server.url}/{lang}/espace-reserve/dossiers/{case.reference}/")
        rows = page.evaluate(EDGE_JS, ".reg-party__name")
        assert _turned_on_the_reading_edge(rows, lang == "ar"), rows
        assert page.evaluate(OVERFLOW_JS) <= 0
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_steps_words_who_answers_a_tables_cell_and_a_reference_stand_on_the_reading_edge(
    browser, live_server, seeded, person_with_a_request, lang
):
    """The survey of M1's class: on a page that links the registers' sheet (a request's own page), a step's words, who
    answers for it and a table's cell in the other direction than the page — drawn with the markup a need's history and
    its skills write — end on its reading edge, wrapped on a phone; the request's reference stands on its cell's reading
    edge on the Arabic page, as the date beside it does (it stood 57 px short of it)."""
    from enquiries.models import ContactRequest

    pk = ContactRequest.objects.get(owner=person_with_a_request).pk
    context = _context(browser, live_server, 390, 844, True, person_with_a_request)
    page = context.new_page()
    try:
        _at_rest(page, f"{live_server.url}/{lang}/espace-reserve/mes-demandes/contact/{pk}/")
        words = (
            "Agenzia Formazione Veneto S.r.l. — SYNTH-AUT-2026-0148 (donnée de test)"
            if lang == "ar"
            else "مركز التكوين المهني بالرباط — جمعية التكوين والتأهيل المهني"
        )
        page.evaluate(
            """(words) => { const box = document.createElement('div'); box.setAttribute('data-w4a', '');
              box.innerHTML = '<ol class="reg-steps reg-steps--log"><li class="reg-step"><div class="reg-step__words">'
                + '<p class="reg-step__text" dir="auto"></p></div><div class="reg-step__end"><span class="db-task__who" dir="auto">'
                + '</span></div></li></ol><table class="data-table"><tbody><tr><th scope="row" dir="auto" data-label="—"></th>'
                + '<td data-label="—">—</td></tr></tbody></table>';
              for (const el of box.querySelectorAll('[dir="auto"]')) el.textContent = words;
              document.querySelector('.reg-page, main').prepend(box); }""",
            words,
        )
        rows = page.evaluate(EDGE_JS, "[data-w4a] [dir='auto']")
        assert len(rows) == 3 and len(_turned_on_the_reading_edge(rows, lang == "ar")) == 3, rows
        assert any(len(row["lines"]) >= 2 for row in rows), ("wrapped on a phone", rows)
        reference = page.evaluate(EDGE_JS, ".reg-summary .reg-ref")
        assert reference and _turned_on_the_reading_edge(reference, lang == "ar") == (
            reference if lang == "ar" else []
        ), reference
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_companys_own_name_heads_its_dashboard_on_the_reading_edge(
    browser, live_server, company_with_a_phone, lang
):
    """The survey of M1's class: the company's legal name, a Latin one on the Arabic page and an Arabic one on the
    French page, two lines on a phone, stands on the page's reading edge (it hugged the far side: 84 and 117 px)."""
    from companies.models import CompanyProfile

    name = (
        "Metalmeccanica Polesine Costruzioni Saldate S.r.l." if lang == "ar" else "شركة البناء والتجهيز المعدني بالرباط"
    )
    CompanyProfile.objects.update(legal_name=name)
    context = _context(browser, live_server, 390, 844, True, company_with_a_phone)
    page = context.new_page()
    try:
        _at_rest(page, f"{live_server.url}/{lang}/espace-reserve/entreprise/")
        rows = page.evaluate(EDGE_JS, ".db-head .ctx__title")
        assert len(rows) == 1 and len(rows[0]["lines"]) >= 2, rows
        edge = 1 if lang == "ar" else 0
        assert all(line[edge] <= 1 for line in rows[0]["lines"]), rows
        assert page.evaluate(OVERFLOW_JS) <= 0
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_phone_bars_account_ring_stays_on_screen(browser, live_server, seeded, person, lang):
    """The accessibility check's finding 2: Tab to the account button of the console's phone bar — its ring lies inside
    the bar, its top on screen (it ran from -2 to 0 px), its foot never on the paper under the bar."""
    context = _context(browser, live_server, 390, 844, True, person)
    page = context.new_page()
    try:
        _at_rest(page, f"{live_server.url}/{lang}/espace-reserve/")
        ring = None
        for _ in range(15):
            page.keyboard.press("Tab")
            ring = page.evaluate(
                """() => { const el = document.activeElement;
                  if (!el || !el.matches('.console-bar .account-menu__summary')) return null;
                  const r = el.getBoundingClientRect(), s = getComputedStyle(el);
                  const out = parseFloat(s.outlineOffset) + parseFloat(s.outlineWidth);
                  return {style: s.outlineStyle, top: r.top - out, bottom: r.bottom + out,
                          bar: document.querySelector('.console-bar').getBoundingClientRect().bottom}; }"""
            )
            if ring:
                break
        assert ring, "the keyboard reaches the account button"
        assert ring["style"] != "none" and ring["top"] >= 0 and ring["bottom"] <= ring["bar"], ring
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("width", [390, 360])
def test_profil_keeps_its_blocks_start_edge(browser, live_server, seeded, person, width):
    """The review's m1: under a finger «Profil» is 44 × 44 and its word starts where the line above it starts (centred
    in its box, it stood 6 px in)."""
    context = _context(browser, live_server, width, 800, True, person)
    page = context.new_page()
    try:
        _at_rest(page, f"{live_server.url}/fr/espace-reserve/")
        account = page.evaluate(
            """() => { const box = document.querySelector('.db-account'), b = box.getBoundingClientRect();
              const start = (el) => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect().left - b.left; };
              const link = box.querySelector('.db-account__links a'), l = link.getBoundingClientRect();
              return {text: link.textContent.trim(), start: start(link), above: start(box.querySelector('.db-account__who')),
                      box: [l.width, l.height]}; }"""
        )
        assert account["box"][0] >= 43.5 and account["box"][1] >= 43.5, account
        assert abs(account["start"] - account["above"]) <= 1, account
    finally:
        context.close()
