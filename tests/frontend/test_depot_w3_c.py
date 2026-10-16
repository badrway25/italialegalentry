"""
The Dépôt — design V5, family W3-C, step 2 (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5; DOCUMENT_WORKSPACE.md
§11; docs/design-v5/QA/v54/w3-c/NOTES.md). What the server and the markup must hold:

* the JSON road (``X-ILE-Depot: 1``) answers each of the eleven answers of §11.1 with its code and the server's own
  sentence — and changes nothing else: the same validation chain, size limit, MIME and antivirus checks, storage,
  throttle and permissions (an intruder still meets a 404, a third party's piece a 403, before any answer is composed);
* the road without script is untouched: a redirect and its message, the 429 page, the Conditions page at 403;
* the Dépôt's markup reads the server's own limits (``deposit_rules``), holds every block it composes, and every word
  is the catalogue's; the piece's page carries the slot where a filing's answer lands;
* the deadline registers (F13) on the legacy sheets: lateness is never drawn with a refusal's colour;
* the deletion map's row «register.css's register and entry»: only what a page still draws stays.

What a browser must show — the answers composed in place, without a page change — is in
tests/frontend/test_depot_browser_w3_c.py.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import translation

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock  # noqa: E402

pytestmark = [pytest.mark.django_db]

ROOT = Path(__file__).resolve().parents[2]
JSON = {"HTTP_X_ILE_DEPOT": "1", "HTTP_ACCEPT": "application/json"}
MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)
PNG_HEAD = b"\x89PNG\r\n\x1a\n"


def _png() -> bytes:
    import io

    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), (200, 190, 170)).save(buffer, "PNG")
    return buffer.getvalue()


def _file(name: str, content: bytes, content_type: str = "application/pdf"):
    return SimpleUploadedFile(name, content, content_type)


# ---- fixtures ------------------------------------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _private_root(settings, tmp_path):
    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def person(user_factory):
    return user_factory(
        "depot.person@example.test",
        role=roles.PERSON,
        full_name="Dépôt PERSONNE",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def piece(person):
    from cases.models import CasePurpose
    from cases.services import open_case
    from documents import services
    from documents.models import AccessClass

    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return services.declare_requirement(
        case, code="passport", title="Passeport", responsible_actor="person", access_class=AccessClass.CASE
    )


def _url(requirement) -> str:
    return f"/documents/requirements/{requirement.pk}/file/"


def _answer(response) -> dict:
    assert response.status_code == 200, response.status_code
    assert response["Content-Type"].startswith("application/json")
    assert "no-store" in response["Cache-Control"]
    return json.loads(response.content)


# ---- the eleven answers, on the JSON road --------------------------------------------------------------------------
def test_a_filing_answers_filed_with_its_version_and_the_servers_sentence(client, person, piece):
    client.force_login(person)
    body = _answer(client.post(_url(piece), {"file": _file("passeport.pdf", MINIMAL_PDF)}, **JSON))
    assert body["answer"] == "filed" and body["version"] == 1
    assert body["message"] == "Pièce déposée (version 1). Elle sera examinée par un intervenant du dossier."
    piece.refresh_from_db()
    assert piece.current_version is not None and piece.current_version.number == 1
    # the JSON road leaves no message behind for the next page: its answer is composed in place
    page = client.get(f"/documents/requirements/{piece.pk}/").content.decode()
    assert "Pièce déposée (version 1)" not in page


@pytest.mark.parametrize(
    ("code", "name", "content", "content_type"),
    [
        pytest.param("empty", "vide.pdf", b"", "application/pdf", id="empty"),
        pytest.param(
            "too_large", "gros.pdf", b"%PDF-" + b"0" * (10 * 1024 * 1024 + 1), "application/pdf", id="too_large"
        ),
        pytest.param("extension", "lettre.docx", b"PK\x03\x04docx", "application/octet-stream", id="extension"),
        pytest.param("content_mismatch", "attestation.pdf", None, "application/pdf", id="content_mismatch"),
        pytest.param("image_invalid", "photo.png", PNG_HEAD + b"\x00broken" * 20, "image/png", id="image_invalid"),
        pytest.param(
            "pdf_active_content",
            "formulaire.pdf",
            MINIMAL_PDF.replace(b"/Type/Catalog", b"/Type/Catalog/OpenAction<</S/JavaScript/JS(1)>>"),
            "application/pdf",
            id="pdf_active_content",
        ),
    ],
)
def test_each_refusal_of_the_chain_answers_its_code_on_the_file_and_stores_nothing(
    client, person, piece, code, name, content, content_type
):
    from documents import services
    from documents.models import PrivateDocument

    client.force_login(person)
    upload = _file(name, _png() if content is None else content, content_type)
    body = _answer(client.post(_url(piece), {"file": upload}, **JSON))
    assert (body["answer"], body["field"]) == (code, "file")
    if code == "empty":
        # Django's FileField refuses an empty upload before the chain does, under the same code and in its own words
        # (the framework's catalogue); the Dépôt's client guard says the chain's sentence before anything is sent
        assert body["message"] in {"Le fichier soumis est vide.", str(services.REJECT_MESSAGES["empty"])}
    else:
        assert body["message"] == str(services.REJECT_MESSAGES[code]), "the chain's own sentence, verbatim"
    assert piece.versions.count() == 0 and PrivateDocument.objects.count() == 0


def test_a_validity_date_already_past_answers_on_its_own_field(client, person, piece):
    import datetime as dt

    client.force_login(person)
    past = (clock.today() - dt.timedelta(days=1)).isoformat()
    body = _answer(client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF), "expires_on": past}, **JSON))
    assert body["field"] == "expires_on"
    assert body["message"] == "Cette date est déjà passée : la pièce ne serait pas valable."
    assert piece.versions.count() == 0


def test_no_file_answers_on_the_file_field(client, person, piece):
    client.force_login(person)
    body = _answer(client.post(_url(piece), {}, **JSON))
    assert (body["answer"], body["field"]) == ("required", "file") and body["message"]


def test_the_antivirus_answer_says_nothing_was_kept_and_the_piece_is_not_valid(client, person, piece, settings):
    from documents.models import RequirementState

    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_infected_scanner"
    client.force_login(person)
    body = _answer(client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON))
    assert body["answer"] == "infected" and body["version"] == 1
    assert body["message"] == "Le fichier a été signalé par l’analyse antivirus : il n’a pas été conservé."
    piece.refresh_from_db()
    assert piece.derived_state() == RequirementState.INVALID, "the Dépôt reads the piece again: its state changed"


def test_the_throttle_answers_as_a_sentence_never_a_page(client, person, piece, monkeypatch):
    from documents import views

    monkeypatch.setattr(views.throttle, "allow", lambda *args, **kwargs: False)
    client.force_login(person)
    body = _answer(client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON))
    assert body["answer"] == "throttled" and body["title"] == "Trop de requêtes"
    assert body["message"].startswith("Vous avez atteint la limite d’envois autorisée.")
    assert piece.versions.count() == 0


def test_the_conditions_gate_answers_its_sentence(client, person, piece):
    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    client.force_login(person)
    body = _answer(client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON))
    assert body["answer"] == "terms"
    assert body["message"] == "Le dépôt d’une pièce nécessite l’acceptation des Conditions d’utilisation."
    assert piece.versions.count() == 0


def test_the_answer_speaks_the_readers_language(client, person, piece):
    from documents import services

    client.force_login(person)
    client.cookies["ile_language"] = "ar"
    body = _answer(
        client.post(
            _url(piece), {"file": _file("x.docx", b"PK")}, HTTP_ACCEPT_LANGUAGE="ar", **{"HTTP_X_ILE_DEPOT": "1"}
        )
    )
    with translation.override("ar"):
        expected = str(services.REJECT_MESSAGES["extension"])
    with translation.override("fr"):
        french = str(services.REJECT_MESSAGES["extension"])
    assert body["message"] == expected and expected != french


# ---- the header opens no door --------------------------------------------------------------------------------------
def test_the_header_never_opens_a_door(client, user_factory, person, piece):
    from cases.models import ResponsibleActor
    from documents import services

    intruder = user_factory("depot.intruder@example.test", role=roles.PERSON, terms_accepted_at=clock.now())
    client.force_login(intruder)
    assert client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON).status_code == 404
    authority = services.declare_requirement(
        piece.case, code="nulla_osta", title="Nulla osta", responsible_actor=ResponsibleActor.AUTHORITY
    )
    client.force_login(person)
    response = client.post(_url(authority), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON)
    assert response.status_code == 403 and not response["Content-Type"].startswith("application/json")
    client.logout()
    assert client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}, **JSON).status_code == 302
    assert piece.versions.count() == 0 and authority.versions.count() == 0


def test_the_road_without_script_is_untouched(client, person, piece, monkeypatch):
    client.force_login(person)
    response = client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)})
    assert response.status_code == 302 and response["Location"] == f"/documents/requirements/{piece.pk}/"
    from documents import views

    monkeypatch.setattr(views.throttle, "allow", lambda *args, **kwargs: False)
    assert client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}).status_code == 429
    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    assert client.post(_url(piece), {"file": _file("p.pdf", MINIMAL_PDF)}).status_code == 403


# ---- the loose road --------------------------------------------------------------------------------------------------
def test_the_loose_road_answers_in_json_with_its_own_words(client, person, settings):
    from documents.models import PrivateDocument

    client.force_login(person)
    body = _answer(
        client.post("/documents/upload/", {"file": _file("copie.pdf", MINIMAL_PDF), "kind": "other"}, **JSON)
    )
    assert (body["answer"], body["message"], body["next"]) == ("filed", "Document téléversé.", "/documents/")
    body = _answer(client.post("/documents/upload/", {"file": _file("x.docx", b"PK"), "kind": "other"}, **JSON))
    assert (body["answer"], body["field"]) == ("extension", "file")
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_infected_scanner"
    body = _answer(client.post("/documents/upload/", {"file": _file("c.pdf", MINIMAL_PDF), "kind": "other"}, **JSON))
    assert body["answer"] == "infected"
    assert body["message"] == "Le fichier a été bloqué par l’analyse antivirus et n’a pas été conservé."
    assert PrivateDocument.objects.count() == 2
    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    body = _answer(client.post("/documents/upload/", {"file": _file("c.pdf", MINIMAL_PDF), "kind": "other"}, **JSON))
    assert body["answer"] == "terms" and "Privacy Policy" in body["message"]


# ---- the markup ------------------------------------------------------------------------------------------------------
def _depot(html: str) -> str:
    start = html.index("data-depot>")
    return html[html.rindex("<section", 0, start) : html.index("</section>", start)]


def test_the_depot_reads_the_servers_own_limits(client, person, piece):
    from documents import services

    client.force_login(person)
    html = client.get(f"/documents/requirements/{piece.pk}/").content.decode()
    form = re.search(r"<form [^>]*data-depot-form[^>]*>", html).group(0)
    attrs = dict(re.findall(r'(data-depot-[\w-]+)="([^"]*)"', form))
    assert int(attrs["data-depot-max"]) == services.MAX_UPLOAD_BYTES
    assert attrs["data-depot-extensions"].split(",") == list(services.ALLOWED_EXTENSIONS)
    assert attrs["data-depot-today"] == clock.today().isoformat(), "the project's clock, as the server's check"
    assert attrs["data-depot-empty"] == str(services.REJECT_MESSAGES["empty"])
    assert attrs["data-depot-too-large"] == str(services.REJECT_MESSAGES["too_large"])
    assert attrs["data-depot-extension"] == str(services.REJECT_MESSAGES["extension"])


def test_the_depot_holds_every_block_it_composes_and_the_real_input_in_its_zone(client, person, piece):
    client.force_login(person)
    html = client.get(f"/documents/requirements/{piece.pk}/").content.decode()
    depot = _depot(html)
    for name in ("throttled", "error", "server", "gate", "filed"):
        assert f'data-depot-block="{name}"' in depot, name
    zone = depot[depot.index("data-depot-zone") :]
    assert zone.index('type="file"') < zone.index("doc-depot__zone-title"), "the real input stays inside the zone"
    assert "Vous avez atteint la limite d’envois autorisée." in depot
    assert "Une erreur technique est survenue." in depot and "Une erreur est survenue" in depot
    assert 'class="doc-filed__ring"' in depot and "icon-check" not in depot, "the filed state's own mark, no check"
    assert 'role="status"' not in depot.split("<template")[0], "the regions speak; the blocks are not live"


def test_the_piece_page_carries_the_slot_of_a_filings_answer_under_its_state(client, person, piece):
    client.force_login(person)
    html = client.get(f"/documents/requirements/{piece.pk}/").content.decode()
    state = html[
        html.index('class="doc-piece__state"') : html.index("</section>", html.index('class="doc-piece__state"'))
    ]
    assert "data-piece-answer" in state
    assert html.count("data-piece-head") == 2, "the chip and the due date: what a preview drawer's head carries"


def test_the_upload_page_is_the_depots_loose_road(client, person):
    client.force_login(person)
    html = client.get("/documents/upload/").content.decode()
    depot = _depot(html)
    assert "doc-depot--loose" in depot and 'action="/documents/upload/"' in depot
    assert 'name="kind"' in depot and 'name="description"' in depot and "data-depot-piece" not in depot
    assert "Retour au registre des pièces" in depot, "a filing's answer leads back to the register"


def test_the_conditions_page_is_the_depots_gate(client, user_factory):
    no_terms = user_factory("depot.noterms@example.test", role=roles.PERSON)
    client.force_login(no_terms)
    response = client.get("/documents/upload/")
    assert response.status_code == 403
    html = response.content.decode()
    gate = html[html.index('class="doc-depot__gate"') :]
    gate = gate[: gate.index("</p>")]
    assert "Le dépôt de pièces est réservé aux comptes ayant accepté" in gate and "#icon-lock" in gate
    assert "<form" not in html[html.index('class="console__workspace"') :].split("console__footer")[0]


# ---- the script --------------------------------------------------------------------------------------------------------
def test_the_depots_script_carries_no_word_and_writes_no_style():
    source = (ROOT / "static" / "js" / "src" / "depot.js").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    code = re.sub(r"(?m)//.*$", "", code)
    assert not re.search(r"[À-ÿ«»’]", code), "every word is the page's (depot.html), none is the script's"
    for forbidden in (
        "innerHTML",
        "outerHTML",
        "insertAdjacentHTML",
        "eval(",
        "new Function",
        ".style.",
        'setAttribute("style"',
    ):
        assert forbidden not in code, forbidden
    console = (ROOT / "static" / "js" / "src" / "console.js").read_text(encoding="utf-8")
    assert 'import("./depot.js")' in console, "imported where a Dépôt is drawn, never before"
    assert (ROOT / "static" / "js" / "dist" / "depot.js").exists()


def test_a_refused_file_marks_its_field_and_downloads_have_a_fingers_band(client, person, piece):
    """A11Y_PERF findings 3 and 4: the refusal on the file's row has an id the field is described by (with
    `aria-invalid`, as every field in error: depot.js `refuseFile`, taken back by `clear`); «Télécharger» of a deposit
    carries the foot links' invisible 44 px band under a coarse pointer (44 px wide too where its word is short)."""
    client.force_login(person)
    html = client.get(f"/documents/requirements/{piece.pk}/").content.decode()
    assert '<p class="doc-depot__refusal" id="id_file_refusal" data-depot-refusal hidden>' in html
    source = (ROOT / "static" / "js" / "src" / "depot.js").read_text(encoding="utf-8")
    refuse = source[source.index("function refuseFile(") :]
    refuse = refuse[: refuse.index("\n}\n")]
    assert 'input.setAttribute("aria-invalid", "true");' in refuse and "describe(input, refusal.id, true);" in refuse
    clear = source[source.index("  const clear = () => {") :]
    clear = clear[: clear.index("  };")]
    assert "describe(input, refusal.id, false);" in clear and 'input.removeAttribute("aria-invalid");' in clear
    depot = (ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_depot.css").read_text(encoding="utf-8")
    coarse = depot[depot.index("@media (pointer: coarse) {\n  .doc-depot__zone {") :]
    coarse = coarse[: coarse.index("\n}\n")]
    assert ".doc-version__get a::before {" in coarse
    assert "inset-block: calc(50% - var(--hit-primary) / 2);" in coarse
    assert "inset-inline: min(0px, calc(50% - var(--hit-primary) / 2));" in coarse


def test_the_size_shown_never_contradicts_a_refusal():
    """REVIEW m6: an empty file is «0 ko», never «1 ko»; from a megabyte one decimal rounded away from the limit — a
    file over it never reads as the limit itself («10,1 Mo», not «10 Mo»)."""
    source = (ROOT / "static" / "js" / "src" / "depot.js").read_text(encoding="utf-8")
    size = source[source.index("function sizeOf(bytes, max = 0) {") :]
    size = size[: size.index("\n}\n")]
    assert "max && bytes > max ? Math.ceil(tenths) : Math.floor(tenths)" in size
    assert "bytes ? Math.max(1, Math.round(bytes / 1024)) : 0" in size
    assert "sizeOf(file.size, max)" in source


def test_no_documents_sheet_reads_a_focus_or_a_state_through_has():
    """A :has() whose argument holds :focus-visible made Blink re-style the whole page from <body> for every focus that
    entered or left its subject — measured on «Mes pièces» at 390: ≈ 650 elements for a row's title, 276 for the Dépôt's
    field, the preview drawer's open and close over 200 ms at CPU × 4. The documents sheets read the keyboard from the
    input's modality (`html[data-input="key"]`, head.js) and a waiting control from an attribute the script writes."""
    for name in ("_workspace.css", "_depot.css", "_table.css"):
        css = re.sub(
            r"/\*.*?\*/",
            "",
            (ROOT / "apps" / "portal" / "static" / "portal" / "v5" / name).read_text(encoding="utf-8"),
            flags=re.S,
        )
        for match in re.finditer(r":has\(", css):
            argument = css[match.end() : css.index("{", match.end())]
            for pseudo in (":focus", ":disabled", ":checked", ":hover"):
                assert pseudo not in argument, f"{name}: :has({argument.strip()[:60]}…) — a state read through :has()"
    depot = (ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_depot.css").read_text(encoding="utf-8")
    assert 'html[data-input="key"] [data-enhanced] .doc-depot__zone:focus-within {' in depot
    assert "[data-enhanced] .doc-depot__zone[data-sending] {" in depot
    script = (ROOT / "static" / "js" / "src" / "depot.js").read_text(encoding="utf-8")
    assert 'zone.setAttribute("data-sending", "")' in script and 'zone.removeAttribute("data-sending")' in script


# ---- F13 on the legacy sheets; the deletion map --------------------------------------------------------------------------
def _rule(css: str, selector: str) -> str:
    start = css.index(selector)
    return css[start : css.index("}", start)]


def test_lateness_is_never_drawn_with_a_refusals_colour_on_the_legacy_sheets():
    workspace = (ROOT / "static" / "css" / "v4" / "workspace.css").read_text(encoding="utf-8")
    portal = (ROOT / "apps" / "portal" / "static" / "portal" / "portal.css").read_text(encoding="utf-8")
    for css, selector in (
        (workspace, ".ws-next--overdue::before {"),
        (workspace, ".dates__row--overdue .dates__when {"),
        (workspace, ".table__overdue {"),
        (workspace, ".table__row--overdue th {"),
        (portal, ".next-action--overdue .next-action__inner {"),
        (portal, ".data-table tr.is-overdue th {"),
    ):
        rule = _rule(css, selector)
        assert "--deadline-overdue-" in rule, selector
        assert not re.search(r"--err-|--state-error|--line-grad-err|rifiuto", rule), selector
    assert "--deadline-soon-" in _rule(workspace, ".dates__row--soon .dates__when {")
    assert "--deadline-soon-" in _rule(portal, ".next-action--soon .next-action__inner {")


def test_the_register_entry_keeps_only_what_a_page_still_draws():
    register = (ROOT / "static" / "css" / "register.css").read_text(encoding="utf-8")
    assert ".entry[aria-current" not in register, "no page marks an entry current any more"
    templates = "".join(path.read_text(encoding="utf-8") for path in (ROOT / "templates").rglob("*.html"))
    for kept in ("register__item", "entry__ordinal", "entry__title", "entry__gloss", "entry__actor", "entry__cta"):
        assert kept in register and kept in templates, kept


def test_the_deadlines_page_draws_each_date_with_the_glyph_of_its_register(client, person):
    import datetime as dt

    from portal.models import Deadline, DeadlineKind

    for title, days in (("Échéance passée", -3), ("Échéance proche", 2), ("Échéance lointaine", 40)):
        Deadline.objects.create(
            owner=person, title=title, due_on=clock.today() + dt.timedelta(days=days), kind=DeadlineKind.DOCUMENT
        )
    client.force_login(person)
    html = client.get("/fr/espace-reserve/mes-echeances/").content.decode()
    dues = re.findall(r'<span class="db-due( db-due--(\w+))?">.*?#icon-([\w-]+)', html, re.S)
    assert [(kind, glyph) for _modifier, kind, glyph in dues] == [
        ("overdue", "alarm-clock"),
        ("soon", "clock"),
        ("", "calendar"),
    ], dues
