"""
«Mes pièces» V5.2 — design V5, family W3-C (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5, §1.2;
docs/design-v5/QA/v54/w3-c/NOTES.md). What the presenters and the rendered pages must hold:

* F8 — the urgency ladder stops once a piece is filed: a filed piece due tomorrow reads calm; an open one does not;
* F13 — the deadline registers: a date past due speaks ``overdue`` (azione, terracotta), a date close by ``soon``
  (attesa, amber); «En retard» is never drawn as a refusal again;
* one partition: the strip's three runs count exactly the collection's three groups (ledger counts = group counts),
  by whose move it is — never by the state alone;
* the state filter follows the register's own order (``STATE_ORDER``), and it is the key to the marks;
* the row is the link: no row menu, no «Consulter»; an act only on an OPEN piece the reader acts on, described by the
  piece's title (W-3: no two controls of the collection share a name and a description);
* the page's ONE primary is the strip's — T1's piece when the reader can act on it — with its piece and its date;
* the search field is drawn in the card layout from thirteen pieces on; no ``badge--*`` on the pages; every word is
  the catalogue's;
* the sheets: three `_` partials imported by the documents page sheet in the collected tree, tokens and logical
  properties only; the legacy register rules gone from main.css's cascade.

What a browser must show — the first card's title at ≤ 700 px at 390 × 844, the first piece in the first viewport at
390 and 360, no dead point on a row, six / five columns then cards by the register's own width, the filter's sheet —
is in tests/frontend/test_documents_browser_w3_c.py.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PORTAL = "/fr/espace-reserve/mes-documents/"
REGISTER = "/documents/"
DEADLINES = "/fr/espace-reserve/mes-echeances/"
PARTIALS = ROOT / "apps" / "portal" / "static" / "portal" / "v5"
PAGE_SHEET = ROOT / "apps" / "documents" / "static" / "documents" / "documents.css"
CATALOGUE = ROOT / "locale" / "ar" / "LC_MESSAGES" / "django.po"
TEMPLATES = [
    ROOT / "templates" / "documents" / "partials" / "register.html",
    ROOT / "templates" / "documents" / "partials" / "depot.html",
    ROOT / "templates" / "components" / "document_row.html",
    ROOT / "templates" / "portal" / "documents.html",
    ROOT / "templates" / "documents" / "index.html",
    ROOT / "templates" / "documents" / "requirement_detail.html",
    ROOT / "templates" / "documents" / "upload.html",
    ROOT / "templates" / "documents" / "terms_required.html",
    ROOT / "templates" / "documents" / "partials" / "piece_drawer.html",
    ROOT / "templates" / "documents" / "partials" / "state_filter.html",
    ROOT / "templates" / "documents" / "partials" / "delete_confirm.html",
    ROOT / "templates" / "portal" / "partials" / "deadline_item.html",
]

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)


# ---- fixtures ------------------------------------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _private_root(settings, tmp_path):
    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def person(user_factory):
    return user_factory(
        "pieces.person@example.test",
        role=roles.PERSON,
        full_name="Pièces PERSONNE",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def reviewer(user_factory):
    return user_factory("pieces.reviewer@example.test", role=roles.STAFF, is_staff=True)


@pytest.fixture
def case(person):
    from cases.models import CasePurpose
    from cases.services import open_case

    return open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _days(n: int) -> dt.date:
    return timezone.localdate() + dt.timedelta(days=n)


def _piece(case, code, *, actor="person", due=None, title=None):
    from documents import services
    from documents.models import AccessClass

    return services.declare_requirement(
        case,
        code=code,
        title=title or f"Pièce {code}",
        responsible_actor=actor,
        due_date=due,
        access_class=AccessClass.CASE,
    )


def _file(requirement, user, *, expires_on=None):
    from documents import services

    return services.file_version(
        requirement, user, SimpleUploadedFile("piece.pdf", MINIMAL_PDF, "application/pdf"), expires_on=expires_on
    )


@pytest.fixture
def dossier(case, person, reviewer):
    """A file with a piece in each of the seven states, the person's and other actors'."""
    from documents import services
    from documents.models import VersionDecision

    pieces = {
        "missing": _piece(case, "missing", due=_days(20)),
        "missing_theirs": _piece(case, "missing_theirs", actor="authority", due=_days(30)),
        "filed": _piece(case, "filed", due=_days(1)),
        "in_review": _piece(case, "in_review", actor="training_body"),
        "valid": _piece(case, "valid", due=_days(5)),
        "invalid": _piece(case, "invalid", due=_days(-3)),
        "expired": _piece(case, "expired"),
        "to_replace": _piece(case, "to_replace", due=_days(40)),
    }
    _file(pieces["filed"], person)
    version = _file(pieces["in_review"], person)
    services.set_decision(version, VersionDecision.IN_REVIEW, actor=reviewer)
    version = _file(pieces["valid"], person)
    services.set_decision(version, VersionDecision.ACCEPTED, actor=reviewer)
    version = _file(pieces["invalid"], person)
    services.set_decision(version, VersionDecision.REFUSED, actor=reviewer, note="Copie partielle : page 2 absente.")
    _file(pieces["expired"], person, expires_on=_days(-2))
    _file(pieces["to_replace"], person, expires_on=_days(10))
    return pieces


def _register(user, **kwargs):
    from documents.presenters import register_context

    return register_context(user, **kwargs)


def _html(client, url) -> str:
    response = client.get(url)
    assert response.status_code == 200, url
    return response.content.decode()


# ---- F8 — the urgency ladder stops once a piece is filed ------------------------------------------------------------
def test_a_filed_piece_due_tomorrow_reads_calm(dossier, person):
    from documents.presenters import present_requirement

    filed = present_requirement(dossier["filed"], user=person)
    assert filed["state"] == "filed" and filed["due_date"] == _days(1)
    assert filed["urgency"] == "" and filed["due_word"] == "", "the clock is no longer the person's"
    # the same date on an OPEN piece is still the person's to beat
    open_piece = present_requirement(_piece(dossier["filed"].case, "open_tomorrow", due=_days(1)), user=person)
    assert open_piece["urgency"] == "soon" and str(open_piece["due_word"]) == "Bientôt"


def test_the_ladder_runs_on_open_pieces_only(dossier, person):
    rows = {row["code"]: row for row in _register(person)["blocks"][0]["all_rows"]}
    assert rows["valid"]["urgency"] == "", "a valid piece due in five days is calm"
    assert rows["invalid"]["urgency"] == "overdue" and str(rows["invalid"]["due_word"]) == "En retard"
    assert rows["missing"]["urgency"] == "upcoming"


def test_the_rendered_row_of_a_filed_piece_due_tomorrow_draws_the_calm_date(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    row = _row_html(html, dossier["filed"].pk)
    assert 'class="doc-due"' in row and "doc-due--soon" not in row and "Bientôt" not in row
    assert "#icon-calendar" in row, "a dated row keeps its glyph: the calendar, calm"


# ---- F13 — the deadline registers ---------------------------------------------------------------------------------
def test_a_date_past_due_speaks_azione_and_one_close_by_attesa(person):
    from core.chips import register_for_kind
    from portal.models import Deadline, DeadlineKind
    from portal.services import present_deadline

    late = Deadline.objects.create(
        owner=person, title="Dépôt", due_on=clock.today() - dt.timedelta(days=3), kind=DeadlineKind.DOCUMENT
    )
    soon = Deadline.objects.create(
        owner=person, title="Rendez-vous", due_on=clock.today() + dt.timedelta(days=2), kind=DeadlineKind.DOCUMENT
    )
    late_row, soon_row = present_deadline(late), present_deadline(soon)
    assert (late_row["badge_kind"], str(late_row["badge_label"])) == ("overdue", "En retard")
    assert (soon_row["badge_kind"], str(soon_row["badge_label"])) == ("soon", "Bientôt")
    assert register_for_kind(late_row["badge_kind"]) == "azione", "terracotta — red never means lateness"
    assert register_for_kind(soon_row["badge_kind"]) == "attesa"


def test_the_deadlines_page_draws_lateness_in_azione_never_as_a_refusal(client, person):
    from portal.models import Deadline, DeadlineKind

    Deadline.objects.create(
        owner=person, title="Échéance passée", due_on=clock.today() - dt.timedelta(days=3), kind=DeadlineKind.DOCUMENT
    )
    Deadline.objects.create(
        owner=person, title="Échéance proche", due_on=clock.today() + dt.timedelta(days=2), kind=DeadlineKind.DOCUMENT
    )
    client.force_login(person)
    html = _html(client, DEADLINES)
    chips = re.findall(
        r'<span class="[^"]*\bchip\b[^"]*" data-register="(\w+)"[^>]*>.*?<span class="chip__w">([^<]+)</span>',
        html,
        re.S,
    )
    words = {word.strip(): register for register, word in chips}
    assert words.get("En retard") == "azione" and words.get("Bientôt") == "attesa", words
    assert "rifiuto" not in words.values()


# ---- one partition: ledger counts = group counts -------------------------------------------------------------------
def test_the_strips_runs_count_exactly_the_collections_groups(dossier, person):
    block = _register(person)["blocks"][0]
    runs = {run["key"]: [row["code"] for row in run["rows"]] for run in block["runs"]}
    groups = {group["key"]: [row["code"] for row in group["rows"]] for group in block["groups"]}
    assert runs == groups, "one partition, one vocabulary"
    assert sum(len(codes) for codes in runs.values()) == block["counts"]["total"] == 8
    # whose move it is — never the state alone: a missing piece the authority must provide is «en cours»
    assert set(runs["to-act"]) == {"missing", "invalid", "expired", "to_replace"}
    assert set(runs["in-hand"]) == {"missing_theirs", "filed", "in_review"}
    assert runs["settled"] == ["valid"]


def test_the_rendered_counts_equal_the_rendered_groups(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    runs = dict(
        re.findall(
            r'class="reg-run reg-run--([\w-]+)[^"]*"[^>]*>\s*<span class="reg-run__label">[^<]*</span>\s*<span class="reg-run__n">(\d+)</span>',
            html,
        )
    )
    groups = {
        key: body.count('<li class="doc-row"')
        for key, body in re.findall(r'<section class="doc-group doc-group--([\w-]+)"(.*?)</section>', html, re.S)
    }
    assert runs == {key: str(n) for key, n in groups.items()} == {"to-act": "4", "in-hand": "3", "settled": "1"}
    total = re.search(r'class="reg__total">(\d+) pièces demandées', html)
    assert total and int(total.group(1)) == sum(groups.values())


def test_the_group_words_are_the_catalogues_until_b1_signs(dossier, person):
    block = _register(person)["blocks"][0]
    assert [str(run["label"]) for run in block["runs"]] == ["À faire", "En cours", "Valide"]


def test_a_filter_keeps_the_strip_whole_and_draws_the_groups_it_keeps(client, dossier, person):
    block = _register(person, state_filter="filed")["blocks"][0]
    assert [len(run["rows"]) for run in block["runs"]] == [4, 3, 1], "the strip counts the whole file"
    assert [(group["key"], [row["code"] for row in group["rows"]]) for group in block["groups"]] == [
        ("in-hand", ["filed"])
    ]
    client.force_login(person)
    html = _html(client, PORTAL + "?état=filed")
    assert html.count('<li class="doc-row"') == 1
    assert f'href="{PORTAL}#g-' in html, "a run leads to its group on the unfiltered page"


# ---- the state filter ------------------------------------------------------------------------------------------------
def test_the_filters_entries_follow_the_registers_order():
    from documents.presenters import state_filters
    from documents.requirements import STATE_ORDER

    values = [entry["value"] for entry in state_filters({})]
    assert values == sorted(STATE_ORDER, key=STATE_ORDER.get)
    assert values == ["expired", "invalid", "missing", "to_replace", "in_review", "filed", "valid"]


def test_the_rendered_filter_is_the_key_to_the_marks_in_the_registers_order(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    track = html[html.index('class="seg ws-filters__seg"') :]
    track = track[: track.index("</nav>")]
    marks = re.findall(r"#icon-(st-[\w-]+|lock)", track)
    assert marks == [
        "st-azione",
        "st-rifiuto",
        "st-attesa",
        "st-attesa-replace",
        "st-esame",
        "st-neutro",
        "st-conforme",
    ]
    assert "icon-check" not in track, "O14: no check, the chosen entry included"


def test_a_state_with_no_piece_is_a_word_not_a_link(client, case, person):
    _piece(case, "only")
    client.force_login(person)
    html = _html(client, PORTAL)
    track = html[html.index('class="seg ws-filters__seg"') :]
    track = track[: track.index("</nav>")]
    assert track.count('class="seg__link seg__link--empty"') == 6 and track.count('<a class="seg__link"') == 2


# ---- the row is the link ---------------------------------------------------------------------------------------------
def test_the_row_has_no_menu_and_says_no_consulter(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    collection = html[html.index('class="doc-collection"') :]
    assert "doc-row__more" not in collection and 'popovertarget="doc-menu' not in collection
    assert "Consulter" not in collection and "Ouvrir le menu de la pièce" not in collection
    assert collection.count('class="doc-row__link"') == 8


def test_an_act_only_on_an_open_piece_described_by_its_title(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    for code in ("missing", "invalid", "expired", "to_replace"):
        row = _row_html(html, dossier[code].pk)
        assert f'aria-describedby="piece-{dossier[code].pk}"' in row and 'class="doc-row__act"' in row, code
    for code in ("filed", "in_review", "valid", "missing_theirs"):
        assert 'class="doc-row__act"' not in _row_html(html, dossier[code].pk), f"{code}: the quiet row"
    labels = [
        str(label) for label in re.findall(r'<div class="doc-row__act"><a [^>]*>(?:<svg.*?</svg>)?([^<]+)</a>', html)
    ]
    assert sorted(labels) == ["Déposer la pièce", "Remplacer la pièce", "Remplacer la pièce", "Remplacer la pièce"]


def test_no_two_controls_of_the_collection_share_a_name_and_a_description(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    collection = html[html.index('class="doc-collection"') : html.index('class="doc-search-status"')]
    found = _controls(collection, html)
    assert len(found) == 8 + 4
    assert len(set(found)) == len(found), "W-3: every control named by its piece"


def test_the_conditions_gate_promises_no_act_its_target_cannot_do(client, dossier, person):
    """W3-B's review, M1, carried over: «Accepter les Conditions» led to a page with nothing to accept (the acceptance
    flow waits on the legal texts). The rows the gate blocks say «Bloqué» and offer no act; the strip leads to the
    piece's page and says why, in the register row's own words — as the dashboard's NowPanel does."""
    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    client.force_login(person)
    html = _html(client, PORTAL)
    for code in ("missing", "invalid", "expired", "to_replace"):
        row = _row_html(html, dossier[code].pk)
        assert "Bloqué" in row and 'class="doc-row__act"' not in row, code
    assert "Bloqué" not in _row_html(html, dossier["valid"].pk), "nothing is blocked on a valid piece"
    assert "Accepter les Conditions" not in html
    strip = html[html.index('class="reg__next"') : html.index('class="reg__caption"')]
    assert "Acceptation des Conditions d’utilisation requise." in strip and "#icon-lock" in strip
    assert f'href="/documents/requirements/{dossier["invalid"].pk}/"' in strip and ">Consulter" in strip


# ---- the page's one primary ------------------------------------------------------------------------------------------
def test_the_strip_carries_the_pages_one_primary_with_its_piece_and_its_date(client, dossier, person):
    from cases.services import next_action

    block = _register(person)["blocks"][0]
    action = next_action(dossier["missing"].case, reader=person)
    if action is not None and action.kind == "piece":
        assert block["next"]["id"] == action.piece_id, "T1 names it: the dashboard and «Mes pièces» name the same piece"
    assert block["next"]["code"] == "invalid", "overdue first"
    client.force_login(person)
    html = _html(client, PORTAL)
    main = html[html.index('class="console__workspace"') :]
    assert main.count("btn--primary") == 1
    strip = main[main.index('class="reg__next"') : main.index('class="reg__caption"')]
    assert "Votre prochaine action" in strip and dossier["invalid"].title in strip
    assert "data-page-primary" in strip and 'aria-describedby="next-' in strip
    assert f'<time datetime="{_days(-3):%Y-%m-%d}">' in strip and "En retard" in strip


def test_nothing_to_do_says_so_and_offers_no_primary(client, case, person, reviewer):
    from documents import services
    from documents.models import VersionDecision

    version = _file(_piece(case, "done"), person)
    services.set_decision(version, VersionDecision.ACCEPTED, actor=reviewer)
    client.force_login(person)
    html = _html(client, PORTAL)
    assert "Aucune action ne vous est demandée pour l’instant." in html
    assert "btn--primary" not in html[html.index('class="console__workspace"') :]


# ---- the search field, the badges, the words ---------------------------------------------------------------------------
def test_the_card_layout_draws_the_search_from_thirteen_pieces(client, case, person):
    for index in range(12):
        _piece(case, f"p{index}")
    client.force_login(person)
    assert "ws-case--long" not in _html(client, PORTAL)
    _piece(case, "p12")
    assert "ws-case ws-case--long" in _html(client, PORTAL)


def test_no_badge_modifier_on_the_documents_pages(client, dossier, person):
    client.force_login(person)
    for url in (PORTAL, REGISTER, f"/documents/requirements/{dossier['invalid'].pk}/", "/documents/upload/", DEADLINES):
        assert "badge--" not in _html(client, url), url


def test_every_word_on_the_documents_pages_is_the_catalogues():
    """No new copy: every word of the documents pages is a msgid the catalogues already hold (the group words and
    glosses «À vous · En cours · Réglées» are the owner's B1 item 3 — listed in the notes, never written here)."""
    known = _catalogue_msgids()
    for template in TEMPLATES:
        for msgid in _msgids(template.read_text(encoding="utf-8")):
            assert msgid in known, f"{template.name}: «{msgid}» is not a catalogue string"


# ---- the sheets ---------------------------------------------------------------------------------------------------------
def test_the_three_partials_are_imported_by_the_page_sheet_in_the_collected_tree():
    sheet = PAGE_SHEET.read_text(encoding="utf-8")
    imports = re.findall(r'^@import url\("([^"]+)"\);', sheet, re.M)
    assert imports == ["../portal/v5/_workspace.css", "../portal/v5/_table.css", "../portal/v5/_depot.css"]
    for name in ("_workspace.css", "_table.css", "_depot.css"):
        assert (PARTIALS / name).exists(), name
        assert not (ROOT / "static" / "css" / "dist" / "portal" / "v5" / name).exists(), "a partial is never an output"
    for entry in (ROOT / "static" / "css" / "main.css", ROOT / "apps" / "portal" / "static" / "portal" / "console.css"):
        assert "_workspace" not in entry.read_text(encoding="utf-8"), f"{entry.name}: only the documents pages load it"
    bundle = (ROOT / "static" / "css" / "dist" / "documents" / "documents.css").read_text(encoding="utf-8")
    assert ".reg-run" in bundle and ".doc-files__table" in bundle and ".doc-version__line" in bundle


@pytest.mark.parametrize("name", ["_workspace.css", "_table.css", "_depot.css"])
def test_the_partials_hold_tokens_and_logical_properties_only(name):
    css = re.sub(r"/\*.*?\*/", "", (PARTIALS / name).read_text(encoding="utf-8"), flags=re.S)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css), "colours are tokens"
    physical = re.findall(
        r"(?<![\w-])(?:margin|padding|border)-(?:left|right)\b|(?<![\w-])(?:left|right)\s*:|text-align:\s*(?:left|right)",
        css,
    )
    assert not physical, physical
    assert "!important" not in css
    assert not re.search(r"animation\s*:|@keyframes", css), "nothing moves at load"


def test_the_legacy_register_rules_left_main_css_cascade():
    # W3-E (step 3) deleted v4/workspace.css with the case file; what console pages still drew of it moved to the
    # console partial v5/_frame.css (retargeted, intent kept: the register's legacy rules came back nowhere)
    assert not (ROOT / "static" / "css" / "v4" / "workspace.css").exists()
    workspace = (ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_frame.css").read_text(encoding="utf-8")
    for gone in (
        ".doc-row",
        ".doc-collection",
        ".doc-menu",
        ".seg__",
        ".doc-search",
        ".doc-controls",
        ".files__",
        ".table__link",
    ):
        assert gone not in workspace, gone
    assert "/* ---- 1 · The ContextHeader" in workspace, "the dashboards and the case file keep their head"
    assert ".health__" not in workspace, "the HealthStrip left with its last consumer, the V4 case file"


# ---- the preview drawer and the filter's sheet, on the overlay system (step 2) ------------------------------------------
DRAWER_OPEN_TAG = (
    '<dialog class="overlay overlay--drawer doc-drawer" id="piece-drawer" data-overlay="drawer" '
    'data-overlay-modal="none" aria-labelledby="piece-drawer-title" data-piece-drawer>'
)


def test_the_register_pages_draw_the_preview_drawer_on_the_overlay_system(client, dossier, person):
    client.force_login(person)
    for url in (PORTAL, REGISTER):
        html = _html(client, url)
        assert html.count(DRAWER_OPEN_TAG) == 1, f"{url}: the system's drawer, non-modal beside the list"
        assert html.index('class="doc-page"') < html.index('id="piece-drawer"'), "outside the page it reads again"
        panel = html[html.index('id="piece-drawer"') :]
        panel = panel[: panel.index("</dialog>")]
        assert 'class="overlay__close" href="#main-content" data-overlay-close aria-label="Fermer"' in panel
        assert 'id="piece-drawer-title"' in panel and "data-drawer-state" in panel and "busy-key" in panel
        assert "data-drawer-body" in panel


def test_the_register_pages_link_the_overlay_systems_page_only_sheet_before_their_own(client, dossier, person):
    """W2-A's CONTRACT §1 (the owner's V5.8 budget): the drawer's and the sheet's head and body are page-only — the two
    register pages link css/dist/core/overlay-panels.css in their head, after main.css and before the documents sheet,
    which places the drawer's head over the system's anatomy; the piece's page draws neither and links nothing more."""
    client.force_login(person)
    for url in (PORTAL, REGISTER):
        head = _html(client, url).split("</head>", 1)[0]
        panels = head.index("/static/css/dist/core/overlay-panels.css")
        assert (
            head.index("/static/css/dist/main.css") < panels < head.index("/static/css/dist/documents/documents.css")
        ), url
    assert "overlay-panels.css" not in _html(client, f"/documents/requirements/{dossier['missing'].pk}/")


def test_a_records_own_words_keep_their_direction_on_the_pieces_page(client, dossier, person):
    """The piece's detail, its source and the responsible's note are the record's words (French data on an Arabic
    page): each is isolated (`dir="auto"`) inside an element that keeps the page's reading edge — an unisolated sentence
    drew its final period at the wrong end (seen in the drawer's body, the same article)."""
    piece = dossier["missing_theirs"]
    piece.detail = "Copie complète, toutes pages."
    piece.responsible_note = "Questure de Milan"
    piece.source_title = "D.Lgs. 286/1998"
    piece.source_ref = "art. 22"
    piece.save(update_fields=["detail", "responsible_note", "source_title", "source_ref"])
    client.force_login(person)
    html = _html(client, f"/documents/requirements/{piece.pk}/")
    assert '<p class="doc-piece__detail"><span dir="auto">Copie complète, toutes pages.</span></p>' in html
    assert ' — <span dir="auto">Questure de Milan</span>' in html
    assert '<span dir="auto">D.Lgs. 286/1998 — art. 22</span>' in html


def test_a_register_with_nothing_to_open_draws_no_drawer(client, user_factory):
    company = user_factory("drawer.none@example.test", role=roles.PERSON, terms_accepted_at=clock.now())
    client.force_login(company)
    assert "piece-drawer" not in _html(client, PORTAL)


def test_the_filters_sheet_is_the_overlay_systems_sheet_and_its_entries_one_markup(client, dossier, person):
    client.force_login(person)
    html = _html(client, PORTAL)
    case_pk = dossier["missing"].case.pk
    sheet_id = f"states-{case_pk}"
    assert f'<a class="btn btn--secondary ws-filter" href="#{sheet_id}" data-overlay-open="{sheet_id}">' in html, (
        "a link to the sheet: without script it shows in place"
    )
    assert f'<dialog class="overlay overlay--sheet" id="{sheet_id}" data-overlay="sheet"' in html
    sheet = html[html.index(f'id="{sheet_id}"') :]
    sheet = sheet[: sheet.index("</dialog>")]
    assert "overlay__grip" in sheet and 'data-overlay-close aria-label="Fermer"' in sheet
    assert f'<nav class="seg seg--sheet" aria-labelledby="{sheet_id}-title">' in sheet
    track = html[html.index('class="seg ws-filters__seg"') :]
    track = track[: track.index("</nav>")]
    entries = lambda part: re.findall(r'class="seg__link[^"]*"[^>]*>(?:<span[^>]*>.*?</span>)?([^<]+)', part, re.S)  # noqa: E731
    assert entries(track) == entries(sheet[sheet.index("seg__list") :]), "one partial, drawn twice"
    assert " popover" not in html[html.index('class="ws-filters"') : html.index("</dialog>", html.index(sheet_id))]
    workspace = (PARTIALS / "_workspace.css").read_text(encoding="utf-8")
    assert ".ws-sheet" not in workspace, "the native popover sheet left with its own motion: the system draws it"


def test_the_drawers_script_carries_no_word_and_is_imported_where_the_register_draws_it():
    source = (ROOT / "static" / "js" / "src" / "piece-drawer.js").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    code = re.sub(r"(?m)//.*$", "", code)
    assert not re.search(r"[À-ÿ«»’]", code), "every word is the page's"
    for forbidden in ("innerHTML", "outerHTML", "insertAdjacentHTML", "eval(", ".style.", 'setAttribute("style"'):
        assert forbidden not in code, forbidden
    assert 'from "./overlay.js"' in code and "seat(" in code, "the overlay system's drawer, L3 on the fragment"
    assert "replace: true" in code, "a swap replaces the history entry"
    console = (ROOT / "static" / "js" / "src" / "console.js").read_text(encoding="utf-8")
    assert 'if (document.querySelector("[data-piece-drawer]"))' in console and 'import("./piece-drawer.js")' in console


def test_inside_the_drawer_a_download_keeps_it_open_and_the_heads_facts_are_not_drawn_twice(client, dossier, person):
    client.force_login(person)
    html = _html(client, f"/documents/requirements/{dossier['filed'].pk}/")
    assert re.search(r'<a href="/documents/link/[^"]+/" aria-describedby="version-1" data-overlay-keep>', html)
    workspace = (PARTIALS / "_workspace.css").read_text(encoding="utf-8")
    hidden = workspace[workspace.index(".doc-drawer [data-piece-head]") :]
    assert hidden[: hidden.index("}")].rstrip().endswith("display: none;")


# ---- the review's fixes (docs/design-v5/QA/v54/w3-c/REVIEW.md, A11Y_PERF.md; NOTES «Review fixes») ---------------------
@pytest.mark.parametrize("shift", [-30, 30])
def test_one_clock_decides_a_deadline_under_a_reference_date(settings, case, person, shift):
    """REVIEW M3: on a lane or the preview a reference date stands in for today (``ILE_REFERENCE_DATE``, honoured with
    DEBUG). A piece's and a checklist item's lateness are read on that clock — as the register's urgency, the deadlines
    page and T1 are —, never on the real date: a piece due the day after the reference date reads «soon» whatever the
    real date says, and one due the day before reads «overdue» even when the real date is a month earlier."""
    from cases import services as case_services
    from cases.models import ChecklistItem
    from documents.presenters import present_requirement

    reference = timezone.localdate() + dt.timedelta(days=shift)
    settings.DEBUG = True
    settings.ILE = {**settings.ILE, "REFERENCE_DATE_OVERRIDE": reference.isoformat()}
    assert clock.today() == reference
    tomorrow, yesterday = reference + dt.timedelta(days=1), reference - dt.timedelta(days=1)
    soon, late = _piece(case, "soon", due=tomorrow), _piece(case, "late", due=yesterday)
    item_soon = ChecklistItem.objects.create(
        case=case, requirement="Voce domani", responsible_actor="person", due_date=tomorrow
    )
    item_late = ChecklistItem.objects.create(
        case=case, requirement="Voce ieri", responsible_actor="person", due_date=yesterday
    )

    assert not soon.is_overdue and late.is_overdue
    assert not item_soon.is_overdue and item_late.is_overdue
    assert present_requirement(soon, user=person)["urgency"] == "soon"
    assert present_requirement(late, user=person)["urgency"] == "overdue"
    overdue = {o.label: o.overdue for o in case_services._open_obligations(case, reader=person)}
    assert overdue["Pièce soon"] is False and overdue["Pièce late"] is True, "T1 reads the same clock"
    assert overdue["Voce domani"] is False and overdue["Voce ieri"] is True


def test_the_models_read_the_projects_clock_for_lateness():
    for path in (ROOT / "apps" / "documents" / "models.py", ROOT / "apps" / "cases" / "models.py"):
        source = path.read_text(encoding="utf-8")
        body = source[source.index("def is_overdue(self) -> bool:") :]
        body = body[: body.index("\n\n")]
        assert "clock.today()" in body and "timezone.localdate()" not in body, path


def test_the_caption_ends_at_the_validated_count(client, dossier, person):
    """REVIEW m1: the strip's caption counts what the strip shows — the pieces asked and how many are validated — and
    stops there: its third clause («n en attente») counted the open pieces, a set no run shows."""
    client.force_login(person)
    html = _html(client, PORTAL)
    caption = html[html.index('class="reg__caption"') :]
    caption = caption[: caption.index("</p>")]
    assert "8 pièces demandées" in caption and "1 sur 8 validées" in caption
    assert "en attente" not in caption and caption.count('class="reg__sep"') == 1


def test_the_strips_marks_are_the_dashboards_ledger_drawn_once(client, dossier, person):
    """REVIEW m7 (V5.8 rule 3: the family that merges second consolidates): the strip's marks are «il registro» as the
    dashboard draws it — `.db-ledger__marks` and its group's colour — and the documents sheet keeps only their place."""
    client.force_login(person)
    html = _html(client, PORTAL)
    for key in ("to-act", "in-hand", "settled"):
        assert f'<a class="reg-run reg-run--{key} db-ledger__group--{key}"' in html, key
    assert html.count('<span class="reg-run__marks db-ledger__marks" aria-hidden="true">') == 3
    workspace = re.sub(r"/\*.*?\*/", "", (PARTIALS / "_workspace.css").read_text(encoding="utf-8"), flags=re.S)
    assert ".reg-run__marks .icon" not in workspace and "--ledger-mark-size" not in workspace
    assert not re.search(r"\.reg-run--[\w-]+ \.reg-run__marks", workspace), "the group colours are the dashboard's"
    dashboard = (PARTIALS / "_dashboard.css").read_text(encoding="utf-8")
    assert ".db-ledger__marks .icon" in dashboard and ".db-ledger__group--to-act .db-ledger__marks" in dashboard
    assert "_dashboard.css" in (ROOT / "apps" / "portal" / "static" / "portal" / "console.css").read_text(
        encoding="utf-8"
    )


def test_the_runs_ring_is_drawn_inside_the_strip_above_the_workspaces_ring_rule():
    """A11Y_PERF finding 2: the strip clips its children — the run's ring is drawn inside it, at a specificity above
    v4/workspace.css's `.console__workspace :is(a, …):focus-visible` (0-3-0), which set the 2 px offset back."""
    workspace = (PARTIALS / "_workspace.css").read_text(encoding="utf-8")
    assert re.search(r"\.reg a\.reg-run:focus-visible \{\s*outline-offset: -4px;", workspace)
    # the workspace's ring moved with W3-E (step 3) from v4/workspace.css to the console partial v5/_frame.css
    legacy = (ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_frame.css").read_text(encoding="utf-8")
    assert ".console__workspace :is(a, button, input, select, textarea, summary, [tabindex]):focus-visible" in legacy


def test_the_files_fold_into_a_list_and_no_labelled_pop_in_reaches_them(client, dossier, person):
    """REVIEW m3: below 40rem of their region the files are one item each — the name, then «type · taille · date» on
    one muted line, the act at its inline end; no cell carries `data-label`, so portal.css's labelled pop-in (its
    uppercase labels and 2 px navy rules) never reaches them."""
    client.force_login(person)
    html = _html(client, PORTAL)
    files = html[html.index('<section class="doc-files"') :]
    assert "<table" in files and "data-label" not in files
    for template in (ROOT / "templates" / "portal" / "documents.html", ROOT / "templates" / "documents" / "index.html"):
        assert "data-label" not in template.read_text(encoding="utf-8"), template
    table = re.sub(r"/\*.*?\*/", "", (PARTIALS / "_table.css").read_text(encoding="utf-8"), flags=re.S)
    folded = table[table.index("@container docfiles (max-width: 39.999rem)") :]
    assert "attr(data-label)" not in table and "text-transform" not in table
    assert (
        'td + td::before {\n    content: "·";' in folded
        and "td.doc-files__act {\n    margin-inline-start: auto;" in folded
    )


def test_the_deletion_of_a_loose_file_asks_first_in_the_systems_alert(client, person):
    """REVIEW m4: «Supprimer» opens the overlay system's alert dialog (the declarative opener: without script the button
    posts its form, as it always has) — the file's name in the question, «Annuler» the safe answer, «Supprimer» the
    garnet outline that sends that row's form; console.js writes the name and points the button at the form."""
    from django.urls import reverse

    from documents import services
    from documents.models import PrivateDocument

    doc = services.store_upload(person, SimpleUploadedFile("copie.pdf", MINIMAL_PDF, "application/pdf"), "other", "")
    client.force_login(person)
    html = _html(client, REGISTER)
    action = reverse("documents:delete", args=[doc.pk])
    assert (
        f'<form method="post" action="{action}" class="doc-files__form" id="loose-delete-{doc.pk}" '
        'data-doc-delete="copie.pdf">'
    ) in html
    assert re.search(
        rf'<button type="submit" class="btn btn--text" aria-describedby="loose-{doc.pk}" data-overlay-open="loose-delete">Supprimer</button>',
        html,
    )
    assert (
        '<dialog class="overlay overlay--dialog overlay--alert" id="loose-delete" data-overlay="alert" role="alertdialog" '
        'aria-labelledby="loose-delete-title" aria-describedby="loose-delete-text">'
    ) in html
    dialog = html[html.index('id="loose-delete"') :]
    dialog = dialog[: dialog.index("</dialog>")]
    assert 'class="overlay__glyph"' in dialog and 'id="loose-delete-title">Supprimer</h2>' in dialog
    assert (
        '<p class="doc-files__ask" id="loose-delete-text"><span class="doc-files__name" dir="auto" data-doc-delete-name></span> Cette action est définitive.</p>'
        in dialog
    )
    assert 'type="button" data-overlay-close data-overlay-safe>Annuler</button>' in dialog
    assert '<button class="btn btn--danger" type="submit" data-doc-delete-go>Supprimer</button>' in dialog
    console = (ROOT / "static" / "js" / "src" / "console.js").read_text(encoding="utf-8")
    assert 'addEventListener("overlay:open"' in console and 'deletion.setAttribute("form", form.id);' in console
    # the road without script: the form posts at once, the file goes
    assert client.post(action).status_code == 302
    assert PrivateDocument.objects.get(pk=doc.pk).deleted_at is not None


# ---- helpers ---------------------------------------------------------------------------------------------------------
def _msgids(source: str) -> set[str]:
    source = re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", source, flags=re.S)
    found = set(re.findall(r'\{%\s*translate\s+"([^"]+)"', source))
    found |= set(re.findall(r"\{%\s*translate\s+'([^']+)'", source))
    for block in re.findall(r"\{%\s*blocktranslate[^%]*%\}(.*?)\{%\s*endblocktranslate\s*%\}", source, flags=re.S):
        singular = block.split("{% plural %}")[0]
        found.add(re.sub(r"\{\{\s*(\w+)\s*\}\}", r"%(\1)s", singular))
    return found


def _catalogue_msgids() -> set[str]:
    """Every msgid of the Arabic catalogue — a long one is written over several lines, joined here."""
    known, current, inside = set(), [], False
    for line in CATALOGUE.read_text(encoding="utf-8").splitlines():
        if line.startswith("msgid "):
            current, inside = [line[6:]], True
        elif inside and line.startswith('"'):
            current.append(line)
        else:
            if inside:
                known.add("".join(part.strip()[1:-1] for part in current).replace('\\"', '"'))
            inside = False
    return known


def _row_html(html: str, pk) -> str:
    start = html.index(f'data-piece="{pk}"')
    return html[start : html.index("</li>", start)]


class _Controls(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[dict] = []
        self.done: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "button"):
            self.stack.append({"attrs": dict(attrs), "text": ""})

    def handle_data(self, data):
        for item in self.stack:
            item["text"] += data

    def handle_endtag(self, tag):
        if tag in ("a", "button") and self.stack:
            item = self.stack.pop()
            name = item["attrs"].get("aria-label") or " ".join(item["text"].split())
            self.done.append((name, item["attrs"].get("aria-describedby", "")))


def _controls(fragment: str, page: str) -> list[tuple[str, str]]:
    parser = _Controls()
    parser.feed(fragment)
    found = []
    for name, described in parser.done:
        description = ""
        if described:
            match = re.search(rf'id="{re.escape(described)}"[^>]*>(.*?)</p>', page, re.S)
            description = " ".join(re.sub(r"<[^>]+>", " ", match.group(1)).split()) if match else ""
        found.append((name, description))
    return found
