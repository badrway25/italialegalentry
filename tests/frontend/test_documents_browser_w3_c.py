"""
«Mes pièces» V5.2 in the browser — design V5, family W3-C (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5;
docs/design-v5/QA/v54/w3-c/NOTES.md). What a static test cannot see:

* the first card's title at ≤ 700 px on a 390 × 844 phone, and the first piece in the first viewport — above the
  console's bottom bar — at 390 and at 360, in French and in Arabic;
* the whole row is the target: every point of a row that shows its hover state opens its piece (0 dead probe points),
  at 1440 and on a phone, fr and ar;
* the register takes six columns, then five, then cards — by the width it is given, not the viewport's;
* the page's one primary and the rows' acts end on one axis (in Arabic, on the left);
* the filter's sheet: one 44 px control opens it, «Fermer» and Esc close it;
* typed text is 16 px under a coarse pointer; nothing overflows from 320 to 1440 px; nothing moves at load;
* the review's fixes: the strip's runs draw their whole ring inside the strip; on a phone the files are one item each;
  a loose file's deletion asks first in the system's alert dialog; a deposit's «Télécharger» is 44 px under a finger.

Chromium on the test database; a session minted with ``Client.force_login`` — nothing typed, no password used. The
first console page of a session carries the loader's entrance release (W1-D): each page is loaded once before it is
measured at rest.
"""

from __future__ import annotations

import datetime as dt
import io
import os

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType
from core import clock

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

PORTAL = "/{lang}/espace-reserve/mes-documents/"

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)

#: Every point of a row that shows its hover state must open its piece — or be its act.
PROBE_JS = """() => {
  const out = {probes: 0, dead: []};
  for (const row of document.querySelectorAll('.doc-row')) {
    const link = row.querySelector('.doc-row__link'), act = row.querySelector('.doc-row__act');
    for (const sel of ['.chip', '.doc-row__state', '.doc-row__due', '.doc-row__resp', '.doc-row__meta', '.doc-row__note', '.doc-row__open']) {
      const part = row.querySelector(sel);
      if (!part || !part.getClientRects().length) continue;
      part.scrollIntoView({block: 'center', behavior: 'instant'});
      const r = part.getBoundingClientRect();
      const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      out.probes += 1;
      if (!(hit && (hit === link || link.contains(hit) || (act && act.contains(hit))))) out.dead.push(sel + ' @ ' + link.textContent.trim());
    }
  }
  window.scrollTo({top: 0, behavior: 'instant'});
  return out;
}"""

#: The register's layout and the page's measures, read at rest.
LAYOUT_JS = """() => {
  const coll = document.querySelector('.doc-collection');
  const cs = getComputedStyle(coll);
  const tracks = cs.display.includes('grid') ? cs.gridTemplateColumns.split(' ').filter((t) => /px$/.test(t)).length : 0;
  const first = document.querySelector('.doc-row__link').getBoundingClientRect();
  const bar = document.querySelector('.console-bottom');
  const barTop = bar && bar.getClientRects().length ? bar.getBoundingClientRect().top : innerHeight;
  const primary = document.querySelector('[data-page-primary]');
  const act = document.querySelector('.doc-row__act .btn');
  const ws = document.querySelector('.console__workspace');
  return {
    tracks, display: cs.display, firstTop: first.top, firstBottom: first.bottom, barTop, vh: innerHeight,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    primary: primary ? [primary.getBoundingClientRect().left, primary.getBoundingClientRect().right] : null,
    act: act ? [act.getBoundingClientRect().left, act.getBoundingClientRect().right] : null,
    moving: document.getAnimations().filter((a) => a.effect && a.effect.target && ws.contains(a.effect.target)).map((a) => a.animationName || a.transitionProperty || 'waapi'),
    rtl: getComputedStyle(document.documentElement).direction === 'rtl',
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


def _days(n: int) -> dt.date:
    return timezone.localdate() + dt.timedelta(days=n)


@pytest.fixture
def person_with_a_dossier(db, settings, tmp_path, user_factory):
    """A file with a piece in each state, the person's and other actors': the QA persona's register, built here."""
    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services
    from documents.models import AccessClass, VersionDecision

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    person = user_factory(
        "pieces.browser@example.test",
        role=roles.PERSON,
        full_name="Pièces NAVIGATEUR",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    reviewer = user_factory("pieces.browser.reviewer@example.test", role=roles.STAFF, is_staff=True)
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")

    def piece(code, title, actor="person", due=None):
        return services.declare_requirement(
            case, code=code, title=title, responsible_actor=actor, due_date=due, access_class=AccessClass.CASE
        )

    def deposit(requirement, expires_on=None):
        upload = SimpleUploadedFile("piece.pdf", MINIMAL_PDF, "application/pdf")
        return services.file_version(requirement, person, upload, expires_on=expires_on)

    deposit(piece("criminal", "Extrait de casier judiciaire", due=_days(48)), expires_on=_days(-2))
    refused = deposit(piece("diploma", "Diplôme ou titre de formation", due=_days(63)))
    services.set_decision(
        refused,
        VersionDecision.REFUSED,
        actor=reviewer,
        note="Copie partielle : il manque la page portant la mention et la signature.",
    )
    piece("nulla_osta", "Nulla osta au travail", actor="authority", due=_days(108))
    deposit(piece("civil", "Acte d’état civil légalisé", due=_days(33)), expires_on=_days(3))
    review = deposit(piece("language", "Attestation de niveau de langue", actor="training_body", due=_days(78)))
    services.set_decision(review, VersionDecision.IN_REVIEW, actor=reviewer)
    deposit(piece("contract", "Proposition de contrat de travail", actor="company", due=_days(93)))
    valid = deposit(piece("passport", "Passeport en cours de validité", due=_days(18)))
    services.set_decision(valid, VersionDecision.ACCEPTED, actor=reviewer)
    return person


def _page(browser, live_server, user, lang, width, height, phone=False, path=PORTAL):
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
    return context, page, errors


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height"), [(390, 844), (360, 800)])
def test_the_first_piece_is_in_the_first_viewport_on_a_phone(
    browser, live_server, person_with_a_dossier, lang, width, height
):
    context, page, errors = _page(browser, live_server, person_with_a_dossier, lang, width, height, phone=True)
    try:
        layout = page.evaluate(LAYOUT_JS)
        assert layout["display"] == "block", "cards on a phone"
        if width == 390:
            assert layout["firstTop"] <= 700, f"the first card's title at {layout['firstTop']} px (gate: ≤ 700)"
        assert layout["firstBottom"] <= layout["barTop"], f"the first piece is above the bottom bar: {layout}"
        assert layout["overflow"] <= 0 and not errors, (layout["overflow"], errors)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize(("width", "height", "phone"), [(1440, 900, False), (390, 844, True)])
def test_every_point_of_a_row_opens_its_piece(browser, live_server, person_with_a_dossier, lang, width, height, phone):
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, lang, width, height, phone=phone)
    try:
        probe = page.evaluate(PROBE_JS)
        assert probe["probes"] >= 35, probe
        assert probe["dead"] == [], f"dead points on the rows: {probe['dead']}"
    finally:
        context.close()


@pytest.mark.parametrize(
    ("width", "height", "tracks"), [(1440, 900, 6), (1280, 800, 5), (1100, 800, 5), (768, 1024, 0)]
)
def test_the_register_takes_six_then_five_columns_then_cards_by_its_own_width(
    browser, live_server, person_with_a_dossier, width, height, tracks
):
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, "fr", width, height)
    try:
        layout = page.evaluate(LAYOUT_JS)
        assert layout["tracks"] == tracks, layout
        width_given = page.evaluate("document.querySelector('.ws-case').getBoundingClientRect().width / 16")
        expected = 6 if width_given >= 66 else 5 if width_given >= 52 else 0
        assert expected == tracks, f"the layout follows the register's {width_given:.1f}rem, not the viewport"
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_primary_and_the_rows_acts_end_on_one_axis(browser, live_server, person_with_a_dossier, lang):
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, lang, 1440, 900)
    try:
        layout = page.evaluate(LAYOUT_JS)
        assert layout["primary"] and layout["act"], layout
        edge = 0 if layout["rtl"] else 1
        assert abs(layout["primary"][edge] - layout["act"][edge]) <= 1, layout
        assert layout["moving"] == [], f"nothing moves at load: {layout['moving']}"
    finally:
        context.close()


def test_a_row_lights_under_the_keyboards_focus_only(browser, live_server, person_with_a_dossier):
    """A row's background answers the keyboard's focus in it (`html[data-input="key"] .doc-row:focus-within`) — read
    from the input's modality, never from a :has(:focus-visible), which re-styled the whole page at every focus."""
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, "fr", 1440, 900)
    try:
        lit = "() => getComputedStyle(document.querySelector('.doc-row')).backgroundColor"
        rest = page.evaluate(lit)
        page.focus(".doc-row__link")
        assert page.evaluate(lit) == rest, "a focus the script or a pointer gives lights nothing"
        page.keyboard.press("Shift+Tab")
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.classList.contains('doc-row__link')")
        assert page.evaluate("document.documentElement.dataset.input") == "key"
        assert page.evaluate(lit) != rest, "the keyboard's focus lights the row as the pointer does"
    finally:
        context.close()


def test_the_filters_sheet_opens_from_one_control_and_closes(browser, live_server, person_with_a_dossier):
    """The card layout's filter: one 44 px control, the overlay system's bottom sheet (W2-A; step 2 of W3-C) — the
    scrim, the focus on the current entry, «Fermer» and Esc, the focus back on the control."""
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, "fr", 390, 844, phone=True)
    try:
        control = page.locator(".ws-filter")
        assert control.is_visible() and not page.locator(".ws-filters__seg").is_visible()
        box = control.bounding_box()
        assert box["height"] >= 44, box
        assert control.get_attribute("aria-haspopup") == "dialog" and control.get_attribute("aria-expanded") == "false"
        control.click()
        sheet = page.locator(".ws-filters dialog.overlay--sheet")
        page.wait_for_function("document.querySelector('.ws-filters dialog.overlay--sheet').open")
        assert sheet.locator(".seg__item").count() == 8
        assert sheet.locator('.seg__link[aria-current="true"]').count() == 1
        assert page.evaluate("document.activeElement.getAttribute('aria-current')") == "true", "the focus on the choice"
        assert page.evaluate("document.querySelector('.overlay-scrim').hasAttribute('data-open')")
        sheet.locator(".overlay__close").click()
        page.wait_for_function("!document.querySelector('.ws-filters dialog.overlay--sheet').open")
        assert page.evaluate("document.activeElement.classList.contains('ws-filter')"), "the focus back on the control"
        control.click()
        page.wait_for_function("document.querySelector('.ws-filters dialog.overlay--sheet').open")
        page.keyboard.press("Escape")
        page.wait_for_function("!document.querySelector('.ws-filters dialog.overlay--sheet').open")
        assert control.get_attribute("aria-expanded") == "false"
    finally:
        context.close()


def test_typed_text_is_16px_under_a_coarse_pointer(browser, live_server, person_with_a_dossier):
    from documents.models import DocumentRequirement

    piece = DocumentRequirement.objects.get(code="diploma")
    for path in (PORTAL.format(lang="fr"), f"/documents/requirements/{piece.pk}/"):
        context, page, _errors = _page(
            browser, live_server, person_with_a_dossier, "fr", 390, 844, phone=True, path=path
        )
        try:
            sizes = page.evaluate(
                """() => [...document.querySelectorAll('input:not([type=hidden]):not([type=file]):not([type=checkbox]):not([type=radio]), select, textarea')]
                  .filter((el) => el.getClientRects().length).map((el) => parseFloat(getComputedStyle(el).fontSize))"""
            )
            assert all(size >= 16 for size in sizes), (path, sizes)
        finally:
            context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_nothing_overflows_from_320_to_1440(browser, live_server, person_with_a_dossier, lang):
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, lang, 1440, 900)
    try:
        for width in (1440, 1280, 1100, 1024, 768, 390, 360, 320):
            page.set_viewport_size({"width": width, "height": 900})
            # the settled page: the shell's own transitions (the rail's width, the frame's padding, after the 80rem
            # crossing) are waited out — read in their middle they push the inline end out for a moment
            page.wait_for_function("() => document.getAnimations().every((a) => a.playState !== 'running')")
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            assert overflow <= 0, (lang, width, overflow)
    finally:
        context.close()


#: The focused element's ring against every clipping ancestor: the outline's outer edge must stand inside each one.
RING_JS = """() => {
  const el = document.activeElement, cs = getComputedStyle(el), r = el.getBoundingClientRect();
  const grow = Math.max(0, parseFloat(cs.outlineOffset) + parseFloat(cs.outlineWidth));
  const ring = { l: r.left - grow, t: r.top - grow, r: r.right + grow, b: r.bottom + grow };
  for (let node = el.parentElement; node && node !== document.body; node = node.parentElement) {
    const s = getComputedStyle(node);
    if (s.overflowX === 'visible' && s.overflowY === 'visible') continue;
    const b = node.getBoundingClientRect();
    const box = { l: b.left + parseFloat(s.borderLeftWidth), t: b.top + parseFloat(s.borderTopWidth),
      r: b.right - parseFloat(s.borderRightWidth), b: b.bottom - parseFloat(s.borderBottomWidth) };
    if (ring.l < box.l - 0.5 || ring.t < box.t - 0.5 || ring.r > box.r + 0.5 || ring.b > box.b + 0.5) {
      return { cut: node.className, cls: el.className };
    }
  }
  return { cut: null, cls: el.className, style: cs.outlineStyle, offset: parseFloat(cs.outlineOffset),
    width: parseFloat(cs.outlineWidth), box: [r.x, r.y, r.width, r.height] };
}"""


def _ring_fill(page, ring) -> float:
    """The ring read on pixels: the focused clip against the same clip unfocused — changed pixels over a 2 px band
    along the ring's centre line (A11Y_PERF's probe)."""
    from PIL import Image, ImageChops

    x, y, w, h = ring["box"]
    clip = {"x": max(0, x - 6), "y": max(0, y - 6), "width": w + 12, "height": h + 12}
    focused = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("L")
    page.evaluate("() => { window.__ring = document.activeElement; window.__ring.blur(); }")
    rest = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("L")
    page.evaluate("() => window.__ring.focus()")
    changed = sum(
        1 for value in ImageChops.difference(focused, rest).point(lambda v: 255 if v > 24 else 0).tobytes() if value
    )
    centre = ring["offset"] + ring["width"] / 2
    return changed / (ring["width"] * 2 * ((w + 2 * centre) + (h + 2 * centre)))


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_strips_runs_and_the_rows_draw_their_whole_ring(browser, live_server, person_with_a_dossier, lang):
    """A11Y_PERF finding 2: the strip clips what stands outside it, and the runs' ring (2 px at a 2 px offset, set back by
    v4/workspace.css's workspace rule) kept 0.27–0.68 of itself. Now drawn inside the run: no clipping ancestor cuts
    the ring of a run or of a row's title, and a run's ring is whole on the pixels."""
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, lang, 1440, 900)
    try:
        page.focus(".ws-search__input")
        for _ in range(3):
            page.keyboard.press("Tab")
            ring = page.evaluate(RING_JS)
            assert "reg-run" in ring["cls"] and ring["cut"] is None, ring
            assert ring["style"] == "solid" and ring["offset"] <= -ring["width"], ring
            assert _ring_fill(page, ring) >= 0.9, ring
        page.focus(".doc-row__link")
        page.keyboard.press("Shift+Tab")
        page.keyboard.press("Tab")
        ring = page.evaluate(RING_JS)
        assert "doc-row__link" in ring["cls"] and ring["cut"] is None, ring
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_on_a_phone_the_files_are_one_item_each(browser, live_server, person_with_a_dossier, lang):
    """REVIEW m3: below 40rem of their region each file is one item — the name on its line, then «type · taille · date»
    on one muted line; no label above a value (portal.css's labelled pop-in reached these tables: six blocks of four
    uppercase labels, ≈ 1 300 px at 390)."""
    context, page, errors = _page(browser, live_server, person_with_a_dossier, lang, 390, 844, phone=True)
    try:
        items = page.evaluate(
            """() => [...document.querySelectorAll('.doc-files__table tbody tr')].map((tr) => {
              const th = tr.querySelector('th'), tds = [...tr.querySelectorAll('td')];
              const tops = tds.map((td) => Math.round(td.getBoundingClientRect().top));
              return { display: getComputedStyle(tr).display, height: Math.round(tr.getBoundingClientRect().height),
                labels: tds.map((td) => getComputedStyle(td, '::before').content),
                nameAbove: th.getBoundingClientRect().bottom <= Math.min(...tops) + 1,
                oneLine: Math.max(...tops) - Math.min(...tops) <= 2 };
            })"""
        )
        assert len(items) >= 6, items
        for item in items:
            assert item["display"] == "flex" and item["nameAbove"] and item["oneLine"], item
            assert item["labels"][0] == "none" and all(label == '"·"' for label in item["labels"][1:]), item
            assert item["height"] <= 110, f"one short item a file: {item}"
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
        assert not errors, errors
    finally:
        context.close()


def test_a_loose_files_deletion_asks_first(browser, live_server, person_with_a_dossier):
    """REVIEW m4: «Supprimer» opens the system's alert dialog — the file's name in the question, the focus on «Annuler»
    (Esc answers it, the focus goes back to the row's «Supprimer», nothing is sent); its «Supprimer» sends the row's
    form: the file goes, the register says so."""
    from documents import services
    from documents.models import PrivateDocument

    doc = services.store_upload(
        person_with_a_dossier, SimpleUploadedFile("copie-perso.pdf", MINIMAL_PDF, "application/pdf"), "other", ""
    )
    context, page, errors = _page(browser, live_server, person_with_a_dossier, "fr", 1440, 900, path="/documents/")
    try:
        posts = []
        page.on("request", lambda request: posts.append(request.url) if request.method == "POST" else None)
        button = page.locator(f"#loose-delete-{doc.pk} button")
        button.click()
        page.wait_for_function("() => document.getElementById('loose-delete').open")
        state = page.evaluate(
            """() => { const d = document.getElementById('loose-delete');
              return { role: d.getAttribute('role'), modal: d.getAttribute('aria-modal'),
                question: document.getElementById(d.getAttribute('aria-describedby')).textContent.trim(),
                focus: document.activeElement.textContent.trim(), safe: document.activeElement.hasAttribute('data-overlay-safe') }; }"""
        )
        assert state["role"] == "alertdialog" and state["modal"] == "true", state
        assert state["question"] == "copie-perso.pdf Cette action est définitive.", state
        assert state["focus"] == "Annuler" and state["safe"], state
        assert button.get_attribute("aria-expanded") == "true"
        page.keyboard.press("Escape")
        page.wait_for_function("() => !document.getElementById('loose-delete').open")
        assert page.evaluate("document.activeElement.closest('form')?.id") == f"loose-delete-{doc.pk}"
        assert posts == [] and PrivateDocument.objects.get(pk=doc.pk).deleted_at is None, "Annuler sends nothing"
        button.click()
        page.wait_for_function("() => document.getElementById('loose-delete').open")
        with page.expect_navigation():
            page.locator("#loose-delete [data-doc-delete-go]").click()
        assert PrivateDocument.objects.get(pk=doc.pk).deleted_at is not None
        assert "Document supprimé." in page.content()
        assert not errors, errors
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_deposits_download_is_44px_under_a_finger(browser, live_server, person_with_a_dossier, lang):
    """A11Y_PERF finding 3: «Télécharger» was 77 × 20 px in French and 30 × 22 in Arabic under a coarse pointer — it
    carries the foot links' invisible 44 px band, 44 px wide too where its word is shorter."""
    from documents.models import DocumentRequirement

    piece = DocumentRequirement.objects.get(code="passport")
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, lang, 390, 844, phone=True)
    context.add_cookies([{"name": settings.LANGUAGE_COOKIE_NAME, "value": lang, "url": live_server.url}])
    page.goto(f"{live_server.url}/documents/requirements/{piece.pk}/", wait_until="load")
    try:
        hit = page.evaluate(
            """() => { const a = document.querySelector('.doc-version__get a');
              a.scrollIntoView({block: 'center', behavior: 'instant'});
              const r = a.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
              const on = (x, y) => { const el = document.elementFromPoint(x, y); return !!el && (el === a || a.contains(el)); };
              let up = 0, down = 0, left = 0, right = 0;
              while (on(cx, cy - up - 1) && up < 60) up += 1;
              while (on(cx, cy + down + 1) && down < 60) down += 1;
              while (on(cx - left - 1, cy) && left < 80) left += 1;
              while (on(cx + right + 1, cy) && right < 80) right += 1;
              return [left + right + 1, up + down + 1]; }"""
        )
        assert hit[0] >= 44 and hit[1] >= 44, hit
    finally:
        context.close()


def test_in_arabic_the_row_mirrors_and_its_chevron_points_to_the_inline_end(
    browser, live_server, person_with_a_dossier
):
    context, page, _errors = _page(browser, live_server, person_with_a_dossier, "ar", 1440, 900)
    try:
        geometry = page.evaluate(
            """() => { const row = document.querySelector('.doc-row');
              const title = row.querySelector('.doc-row__link').getBoundingClientRect();
              const open = row.querySelector('.doc-row__open').getBoundingClientRect();
              const svg = row.querySelector('.doc-row__open svg');
              return {titleRight: title.right, openLeft: open.left, rowRight: row.getBoundingClientRect().right,
                      flipped: getComputedStyle(svg).transform !== 'none' || svg.classList.contains('icon--flip-rtl')}; }"""
        )
        assert geometry["openLeft"] < geometry["titleRight"] and geometry["rowRight"] - geometry["titleRight"] < 60, (
            geometry
        )
        assert geometry["flipped"], "the chevron mirrors in Arabic"
    finally:
        context.close()
