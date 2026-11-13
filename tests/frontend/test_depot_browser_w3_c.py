"""
The Dépôt in the browser — design V5, family W3-C, step 2 (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5;
DOCUMENT_WORKSPACE.md §11; docs/design-v5/QA/v54/w3-c/NOTES.md). What a static test cannot see:

* the zone keeps the real input: with the script it covers the zone, so a press anywhere is the input's;
* a client guard refuses a file before anything is sent, on the file's row, in the server's words;
* a server refusal is composed IN PLACE — the page does not change, the row says why;
* a filing reads the piece again: its new state, its version, the answer under the state, the focus on the state;
* the throttle is a notice in place with «Déposer» kept; the Conditions gate replaces the form by its sentence;
* the loose road's filing says «Document téléversé.» in place, with the way back to the register;
* in Arabic the refused row mirrors (its double rule on the right) and a long file name wraps — nothing overflows
  from 320 to 430 px; nothing writes an inline style (CSP: 0 reports); no console error.

Chromium on the test database; sessions minted with ``Client.force_login`` — nothing typed, no password used.
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

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)
CSP_HOOK = (
    "document.addEventListener('securitypolicyviolation', (e) => "
    "{ (window.__csp = window.__csp || []).push(e.violatedDirective + ' ' + e.blockedURI); });"
)


def _png() -> bytes:
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), (200, 190, 170)).save(buffer, "PNG")
    return buffer.getvalue()


def _pdf(name="diplome-scan-2026.pdf"):
    return {"name": name, "mimeType": "application/pdf", "buffer": MINIMAL_PDF}


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
def depositor(db, settings, tmp_path, user_factory):
    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services
    from documents.models import AccessClass

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    person = user_factory(
        "depot.browser@example.test",
        role=roles.PERSON,
        full_name="Dépôt NAVIGATEUR",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    pieces = {
        code: services.declare_requirement(
            case, code=code, title=title, responsible_actor="person", access_class=AccessClass.CASE
        )
        for code, title in (
            ("passport", "Passeport en cours de validité"),
            ("diploma", "Diplôme ou titre de formation"),
        )
    }
    return person, pieces


def _open(browser, live_server, user, path, lang="fr", width=1440, height=900, phone=False, block=None):
    """The page, signed in, with depot.js wired — or, with `block` (a URL pattern), that request aborted: the page as it
    stands when the module is lost on the way (W4-C's review, M2), returned once the module's request has failed."""
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
            },
            {"name": settings.LANGUAGE_COOKIE_NAME, "value": lang, "url": live_server.url},
        ]
    )
    page = context.new_page()
    page.add_init_script(CSP_HOOK)
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    failed = []
    if block:
        context.route(block, lambda route: route.abort())
        page.on("requestfailed", lambda request: failed.append(request.url))
    page.goto(live_server.url + path, wait_until="load")  # the session's first console page plays the release
    failed.clear()
    page.goto(live_server.url + path, wait_until="load")
    if block:
        for _ in range(50):
            if failed:
                break
            page.wait_for_timeout(100)
        assert failed, f"{block} was never asked for"
        return context, page, errors
    page.wait_for_function("document.querySelector('[data-depot]')?.hasAttribute('data-enhanced')")
    return context, page, errors


def _submit_and_wait(page):
    page.click("[data-depot-submit]")
    page.wait_for_function("() => !document.querySelector('[data-depot-submit][aria-busy=\"true\"]')", timeout=15000)


def _csp(page):
    return page.evaluate("window.__csp || []")


def test_the_zone_keeps_the_real_input_and_a_guard_refuses_before_anything_is_sent(browser, live_server, depositor):
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    try:
        hit = page.evaluate(
            """() => { const zone = document.querySelector('[data-depot-zone]').getBoundingClientRect();
              const el = document.elementFromPoint(zone.left + zone.width * 0.8, zone.top + zone.height / 2);
              return el && el.matches('input[type=file]'); }"""
        )
        assert hit, "a press anywhere on the zone is the input's own"
        posts = []
        page.on("request", lambda request: posts.append(request.url) if request.method == "POST" else None)
        page.set_input_files(
            "[data-depot] input[type=file]",
            {"name": "lettre.docx", "mimeType": "application/octet-stream", "buffer": b"PK"},
        )
        page.click("[data-depot-submit]")
        page.wait_for_timeout(300)
        row = page.evaluate(
            """() => ({ state: document.querySelector('[data-depot-file]').dataset.state,
              refusal: document.querySelector('[data-depot-refusal-text]').textContent,
              name: document.querySelector('[data-depot-name]').textContent,
              live: document.querySelector('[data-depot-live=assertive]').textContent })"""
        )
        assert row["state"] == "refused" and row["name"] == "lettre.docx"
        assert row["refusal"] == "Format non accepté : seuls les fichiers PDF, JPEG et PNG sont autorisés."
        assert row["live"] == row["refusal"], "assertive: a refusal"
        assert posts == [], "the client guard sends nothing"
        # A11Y_PERF finding 4: the field is marked in error and described by the refusal; a new choice takes both back
        field = "() => { const i = document.querySelector('[data-depot] input[type=file]'); return [i.getAttribute('aria-invalid'), i.getAttribute('aria-describedby')]; }"
        invalid, described = page.evaluate(field)
        assert invalid == "true" and "id_file_refusal" in described.split(), (invalid, described)
        page.set_input_files("[data-depot] input[type=file]", _pdf())
        invalid, described = page.evaluate(field)
        assert invalid is None and "id_file_refusal" not in (described or "").split(), (invalid, described)
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_the_zone_takes_the_keyboards_ring_and_a_pointer_leaves_it_plain(browser, live_server, depositor):
    """The zone's ring is the keyboard's (the input's modality, head.js) — read without a :has(:focus-visible)."""
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    try:
        ring = "() => { const s = getComputedStyle(document.querySelector('[data-depot-zone]')); return [s.outlineStyle, s.borderTopStyle]; }"
        assert page.evaluate(ring) == ["none", "dashed"], "at rest: the dashed frame, no ring"
        for _ in range(60):
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement.matches('[data-depot] input[type=file]')"):
                break
        assert page.evaluate("document.activeElement.matches('[data-depot] input[type=file]')"), (
            "the field takes the Tab"
        )
        assert page.evaluate("document.documentElement.dataset.input") == "key"
        assert page.evaluate(ring) == ["solid", "solid"], "the keyboard's focus: the ring and a solid frame"
        page.mouse.click(5, 5)
        page.focus("[data-depot] input[type=file]")
        assert page.evaluate("document.documentElement.dataset.input") == "pointer"
        assert page.evaluate(ring)[0] == "none", "a pointer's focus draws no ring"
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_a_server_refusal_is_composed_in_place_without_a_page_change(browser, live_server, depositor):
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    try:
        page.evaluate("window.__stay = 1")
        page.set_input_files(
            "[data-depot] input[type=file]",
            {"name": "attestation.pdf", "mimeType": "application/pdf", "buffer": _png()},
        )
        _submit_and_wait(page)
        page.wait_for_function("() => !document.querySelector('[data-depot-refusal]').hidden")
        state = page.evaluate(
            """() => ({ stay: window.__stay, refusal: document.querySelector('[data-depot-refusal-text]').textContent,
              focus: document.activeElement.type })"""
        )
        assert state["stay"] == 1, "no page change: the refusal arrives late and stays in place"
        assert state["refusal"] == "Le contenu du fichier ne correspond pas à son extension."
        assert state["focus"] == "file", "the one way on is another file"
        assert pieces["passport"].versions.count() == 0
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_a_filing_reads_the_piece_again_and_answers_under_its_state(browser, live_server, depositor):
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    try:
        page.set_input_files("[data-depot] input[type=file]", _pdf())
        page.click("[data-depot-submit]")
        page.wait_for_function("() => (document.querySelector('[data-piece-answer]') || {}).textContent", timeout=15000)
        # the announcement follows the answer by a moment (depot.js `say`: the region emptied, then its words)
        page.wait_for_function("() => document.querySelector('[data-depot-live=polite]').textContent")
        state = page.evaluate(
            """() => ({ answer: document.querySelector('[data-piece-answer]').textContent.trim(),
              chip: document.querySelector('.doc-piece__chip').textContent.trim(),
              versions: document.querySelectorAll('.doc-version').length,
              focus: document.activeElement.textContent.trim(),
              heading: document.activeElement.classList.contains('doc-piece__h2'),
              ring: getComputedStyle(document.querySelector('[data-piece-answer] .doc-filed__ring')).transitionProperty,
              check: !!document.querySelector('[data-piece-answer] [href*="icon-check"]'),
              live: document.querySelector('[data-depot-live=polite]').textContent })"""
        )
        sentence = "Pièce déposée (version 1). Elle sera examinée par un intervenant du dossier."
        assert state["answer"] == sentence and state["live"] == sentence
        assert state["chip"] == "Déposé" and state["versions"] == 1, state
        assert state["heading"] and state["focus"] == "État de la pièce", "the focus lands on the state it changed"
        assert "stroke-dashoffset" in state["ring"] and not state["check"], "the filed mark draws itself, no check"
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_the_throttle_is_a_notice_in_place_and_deposer_stays(browser, live_server, depositor):
    from django.core.cache import cache
    from django.test import RequestFactory

    from core.privacy import hashed_client_ip

    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['diploma'].pk}/")
    ident = hashed_client_ip(RequestFactory().get("/", REMOTE_ADDR="127.0.0.1"))
    key = f"throttle:documents_upload:{ident}"
    cache.set(key, 30, 3600)
    try:
        page.set_input_files("[data-depot] input[type=file]", _pdf())
        _submit_and_wait(page)
        state = page.evaluate(
            """() => ({ notice: document.querySelector('[data-depot-answer] .notice')?.textContent.replace(/\\s+/g, ' ').trim(),
              submit: !!document.querySelector('[data-depot-submit]'), file: document.querySelector('[data-depot-name]').textContent,
              live: document.querySelector('[data-depot-live=polite]').textContent })"""
        )
        assert state["notice"] and state["notice"].startswith("Trop de requêtes"), state
        assert "rien n’a été perdu de votre côté" in state["notice"] and state["live"].startswith("Trop de requêtes.")
        assert state["submit"] and state["file"] == "diplome-scan-2026.pdf", (
            "the file stays chosen; «Déposer» is the retry"
        )
        assert pieces["diploma"].versions.count() == 0
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        cache.delete(key)
        context.close()


def test_the_conditions_gate_replaces_the_form_by_its_sentence(browser, live_server, depositor):
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['diploma'].pk}/")
    try:
        person.terms_accepted_at = None
        person.save(update_fields=["terms_accepted_at"])
        page.set_input_files("[data-depot] input[type=file]", _pdf())
        page.click("[data-depot-submit]")
        page.wait_for_selector("[data-depot] .doc-depot__gate", timeout=15000)
        state = page.evaluate(
            """() => ({ gate: document.querySelector('[data-depot] .doc-depot__gate').textContent.replace(/\\s+/g, ' ').trim(),
              form: !!document.querySelector('[data-depot-form]'),
              note: document.querySelector('[data-depot] .doc-depot__note').hidden })"""
        )
        assert state["gate"].startswith("Le dépôt d’une pièce nécessite l’acceptation des Conditions d’utilisation.")
        assert not state["form"] and state["note"], state
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_the_loose_roads_filing_is_said_in_place_and_the_zone_comes_back(browser, live_server, depositor):
    """The loose road's filing: «Document téléversé.» in place, with the way back to the register — and (REVIEW m5) the
    file's name before the server's sentence, the form set back and the zone there for another file."""
    person, _pieces = depositor
    context, page, errors = _open(browser, live_server, person, "/documents/upload/")
    try:
        page.set_input_files("[data-depot] input[type=file]", _pdf("copie-personnelle.pdf"))
        page.click("[data-depot-submit]")
        page.wait_for_selector("[data-depot] .doc-filed", timeout=15000)
        page.wait_for_function("() => document.querySelector('[data-depot-live=polite]').textContent")
        state = page.evaluate(
            """() => ({ filed: document.querySelector('[data-depot] .doc-filed').textContent.replace(/\\s+/g, ' ').trim(),
              link: document.querySelector('[data-depot] .doc-filed a')?.getAttribute('href'),
              focus: document.activeElement.classList.contains('doc-filed'),
              zone: !!document.querySelector('[data-depot-form] [data-depot-zone]')?.getClientRects().length,
              files: document.querySelector('[data-depot] input[type=file]').files.length,
              row: document.querySelector('[data-depot-file]').hidden,
              live: document.querySelector('[data-depot-live=polite]').textContent })"""
        )
        assert state["filed"].startswith("copie-personnelle.pdf Document téléversé."), state
        assert state["link"] == "/documents/" and state["focus"], state
        assert state["zone"] and state["files"] == 0 and state["row"], "the zone is back for another file"
        assert state["live"] == "copie-personnelle.pdf — Document téléversé.", state
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_the_chosen_files_size_never_contradicts_its_refusal(browser, live_server, depositor):
    """REVIEW m6: an empty file read «PDF · 1 ko» beside «Le fichier est vide.», and one just over the limit «PDF · 10 Mo»
    beside «… la taille maximale de 10 Mo.» — now «0 ko» and «10,1 Mo»; a file at the limit reads «10 Mo» and passes."""
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    try:
        read = "() => [document.querySelector('[data-depot-meta]').textContent, document.querySelector('[data-depot-refusal]').hidden]"
        cases = (
            (b"", "PDF · 0\u00a0ko", False),
            (b"%" * (10 * 1024 * 1024 + 1), "PDF · 10,1\u00a0Mo", False),
            (b"%" * (10 * 1024 * 1024), "PDF · 10\u00a0Mo", True),
        )
        for buffer, meta, passes in cases:
            page.set_input_files(
                "[data-depot] input[type=file]", {"name": "piece.pdf", "mimeType": "application/pdf", "buffer": buffer}
            )
            shown, hidden = page.evaluate(read)
            assert shown.replace("\u202f", "\u00a0") == meta and hidden == passes, (shown, hidden, meta)
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_refused_row_mirrors_and_nothing_overflows_from_320_to_430(browser, live_server, depositor, lang):
    person, pieces = depositor
    context, page, errors = _open(
        browser,
        live_server,
        person,
        f"/documents/requirements/{pieces['passport'].pk}/",
        lang=lang,
        width=390,
        height=844,
        phone=True,
    )
    try:
        long_name = "attestation-de-niveau-de-langue-italienne-B1-certificat-officiel-2026-version-definitive.docx"
        page.set_input_files(
            "[data-depot] input[type=file]",
            {"name": long_name, "mimeType": "application/octet-stream", "buffer": b"PK"},
        )
        page.wait_for_timeout(200)
        for width in (320, 360, 390, 430):
            page.set_viewport_size({"width": width, "height": 844})
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            assert overflow <= 0, (lang, width, overflow)
        edge = page.evaluate(
            """() => { const row = document.querySelector('[data-depot-file]'); const cs = getComputedStyle(row);
              return { left: cs.borderLeftStyle, right: cs.borderRightStyle, rtl: getComputedStyle(document.documentElement).direction === 'rtl' }; }"""
        )
        assert edge["rtl"] == (lang == "ar")
        assert (edge["right"] if edge["rtl"] else edge["left"]) == "double", edge
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


MODULE = "**/js/dist/depot.js"
ZONE = """() => { const zone = document.querySelector('[data-depot-zone]'); const input = zone.querySelector('input[type=file]');
  const box = input.getBoundingClientRect(); const frame = zone.getBoundingClientRect(); const seen = getComputedStyle(input);
  const hit = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
  const row = document.querySelector('[data-depot-file]');
  return { enhanced: zone.closest('[data-depot]').hasAttribute('data-enhanced'),
    js: document.documentElement.classList.contains('js'), required: input.required, valid: input.matches(':valid'),
    file: input.files.length ? input.files[0].name : null, opacity: seen.opacity, visibility: seen.visibility,
    onTop: hit === input, covers: box.width >= frame.width - 2 && box.height >= frame.height - 2,
    title: getComputedStyle(zone.querySelector('.doc-depot__zone-title')).visibility,
    mark: getComputedStyle(zone.querySelector('.doc-depot__zone-mark')).visibility, height: frame.height,
    row: row.hidden, rowShown: getComputedStyle(row).display !== 'none',
    name: document.querySelector('[data-depot-name]').textContent,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth }; }"""


@pytest.mark.parametrize(("lang", "width", "phone"), [("fr", 1440, False), ("ar", 390, True)])
def test_without_its_module_a_chosen_file_shows_the_browsers_own_control_with_its_name(
    browser, live_server, depositor, lang, width, phone
):
    """W4-C's review, M2: P1 draws the zone from the first paint (html.js, no layout shift), and html.js does not mean
    that depot.js arrived — its module lost on the way left a silent picker: the input transparent over the frame, no
    row, no name. With the module's request aborted, a chosen file now shows the browser's own control — its name
    with it — on top of the frame, in the frame's box: nothing moves, nothing overflows, no inline style."""
    person, _pieces = depositor
    height = 844 if phone else 900
    context, page, errors = _open(
        browser,
        live_server,
        person,
        "/documents/upload/",
        lang=lang,
        width=width,
        height=height,
        phone=phone,
        block=MODULE,
    )
    try:
        rest = page.evaluate(ZONE)
        assert rest["js"] and not rest["enhanced"], rest
        assert rest["opacity"] == "0" and rest["title"] == "visible", "P1's first frame: the frame's own words"
        assert rest["required"] and not rest["valid"], "the field is required: :valid is a file chosen"
        page.set_input_files("[data-depot] input[type=file]", _pdf("attestation-sans-module.pdf"))
        page.wait_for_timeout(100)
        chosen = page.evaluate(ZONE)
        assert chosen["file"] == "attestation-sans-module.pdf" and chosen["valid"], chosen
        assert chosen["opacity"] == "1" and chosen["visibility"] == "visible", "the browser's own control is painted"
        assert chosen["onTop"] and chosen["covers"], "on top of the frame, the frame's whole box: it names the file"
        assert chosen["title"] == "hidden" and chosen["mark"] == "hidden", "the frame's words give it their place"
        assert chosen["height"] == rest["height"], ("the zone keeps its size", rest["height"], chosen["height"])
        assert chosen["row"] and not chosen["rowShown"], "no module, no row: the control itself says the name"
        assert chosen["overflow"] <= 0 and _csp(page) == [], (chosen["overflow"], _csp(page))
        lost = ("depot.js", "dynamically imported module", "ERR_FAILED")
        assert all(any(word in error for word in lost) for error in errors), errors
    finally:
        context.close()


def test_a_file_chosen_before_the_module_arrives_is_taken_up_on_its_row(browser, live_server, depositor):
    """The late module (W4-C's review, M2): a file chosen while depot.js is on its way shows the browser's own control
    meanwhile; once the module arrives the file is shown, guarded and said on its row, as if chosen that moment — the
    control is transparent again, the name never lost."""
    person, _pieces = depositor
    context, page, errors = _open(browser, live_server, person, "/documents/upload/")
    held = []
    try:
        context.route(MODULE, lambda route: held.append(route))
        page.goto(live_server.url + "/documents/upload/", wait_until="domcontentloaded")
        page.wait_for_function(
            "() => document.documentElement.classList.contains('js') && !!document.querySelector('[data-depot-zone]')"
        )
        for _ in range(50):
            if held:
                break
            page.wait_for_timeout(100)
        assert held, "the module is on its way"
        page.set_input_files("[data-depot] input[type=file]", _pdf("attestation-en-chemin.pdf"))
        page.wait_for_timeout(100)
        waiting = page.evaluate(ZONE)
        assert not waiting["enhanced"] and waiting["opacity"] == "1" and waiting["onTop"], waiting
        held[0].continue_()
        # an arrow function: a string expression that has to poll is evaluated in the page, which the CSP refuses
        page.wait_for_function("() => document.querySelector('[data-depot]').hasAttribute('data-enhanced')")
        page.wait_for_function("() => !document.querySelector('[data-depot-file]').hidden")
        page.wait_for_function("() => document.querySelector('[data-depot-live=polite]')?.textContent")
        taken = page.evaluate(ZONE)
        live = page.evaluate("document.querySelector('[data-depot-live=polite]').textContent")
        assert taken["name"] == "attestation-en-chemin.pdf" and taken["rowShown"], taken
        assert taken["opacity"] == "0" and taken["title"] == "visible", "the enhanced zone again: its row says the file"
        assert live.startswith("attestation-en-chemin.pdf — PDF"), live
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()


def test_a_refused_choice_leaves_no_sentence_of_the_file_before_it(browser, live_server, depositor):
    """A11Y_PERF a1 (W4-C): the polite region kept the previous file's sentence («….pdf — PDF · 1 ko») while the alert
    said the refusal of the new one; a new choice now empties both regions first, and a valid one empties the alert."""
    person, pieces = depositor
    context, page, errors = _open(browser, live_server, person, f"/documents/requirements/{pieces['passport'].pk}/")
    regions = (
        "() => ['polite', 'assertive'].map((kind) => document.querySelector(`[data-depot-live=${kind}]`).textContent)"
    )
    try:
        page.set_input_files("[data-depot] input[type=file]", _pdf("attestation-w4c.pdf"))
        page.wait_for_function("() => document.querySelector('[data-depot-live=polite]').textContent")
        page.set_input_files(
            "[data-depot] input[type=file]",
            {"name": "lettre.docx", "mimeType": "application/octet-stream", "buffer": b"PK"},
        )
        page.wait_for_function("() => document.querySelector('[data-depot-live=assertive]').textContent")
        polite, assertive = page.evaluate(regions)
        assert polite == "" and assertive.startswith("Format non accepté"), (polite, assertive)
        page.set_input_files("[data-depot] input[type=file]", _pdf("attestation-w4c.pdf"))
        page.wait_for_function("() => document.querySelector('[data-depot-live=polite]').textContent")
        polite, assertive = page.evaluate(regions)
        assert polite.startswith("attestation-w4c.pdf — PDF") and assertive == "", (polite, assertive)
        assert not errors and _csp(page) == [], (errors, _csp(page))
    finally:
        context.close()
