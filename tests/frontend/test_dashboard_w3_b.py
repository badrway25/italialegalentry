"""
The person's dashboard — design V5, family W3-B (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 4, §1.15, §1.18
Track T; docs/design-v5/QA/v54/w3-b/NOTES.md).

* T1 — ONE next action over every open obligation of the file (its checklist items and the pieces it still waits
  for), on the precedence the domain already had: a blocking outcome, then an overdue obligation, then the nearest
  date, then the person's own open obligation (else anybody's), then the questionnaire, then nothing. A piece is
  named only to an account that may read it (the documents app's own query-time authorisation).
* the NowPanel: four variants chosen by the system — «à vous», «en attente d'un tiers», «rien à faire», «pas encore
  de dossier» — and an overdue date that takes it over; ONE primary, the act itself, in the register's words;
* F9 — a person's dashboard builds no card grid; the bridge keeps its cards;
* the page: DOM order h1 → NowPanel → journey; one primary; no piece drawn twice; one raised panel; no stat card; a
  French record isolated on an Arabic page; every word on it the catalogue's (no new copy);
* the partial: imported by console.css after the shell, tokens and logical properties only, no shadow, no
  animation, no corner of its own beyond the discs' full.

Step 2 — the company's dashboard and the bridge of the accounts that are not a person:

* the company's NowPanel — the same plane, the company's one next action (declare, verify, create, complete,
  transmit, nothing); the need it is about drawn there only; «il registro» of the needs by who holds them;
* the bridge — no NowPanel (the system knows no next action for an institution, a university or a professional), its
  registers in the person's grammar, flat, each empty region one line, no grid of equal cards, no figure;
* one NowPanel partial for the dashboards; every word the catalogue's; the legacy rules gone with their consumers.

What a browser must show — the primary with its piece and its date in the first viewport at 1920 / 1440 / 1366 ×
657 / 1024 / 390, fr and ar, nothing animating at load, one raised plane; the company's and the bridge's — is in
tests/frontend/test_dashboard_browser_w3_b.py.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "portal" / "dashboard.html"
PARTIAL = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_dashboard.css"
ENTRY = ROOT / "apps" / "portal" / "static" / "portal" / "console.css"
CATALOGUE = ROOT / "locale" / "ar" / "LC_MESSAGES" / "django.po"
DASHBOARD = "/{lang}/espace-reserve/"

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
        "dash.person@example.test",
        role=roles.PERSON,
        full_name="Dash PERSON",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def case(person):
    from cases.models import CasePurpose
    from cases.services import open_case

    return open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _days(n: int) -> dt.date:
    return timezone.localdate() + dt.timedelta(days=n)


def _piece(case, code, *, actor="person", due=None, access=None, item=None, title=None):
    from documents import services
    from documents.models import AccessClass

    return services.declare_requirement(
        case,
        code=code,
        title=title or f"Pièce {code}",
        responsible_actor=actor,
        due_date=due,
        access_class=access or AccessClass.CASE,
        checklist_item=item,
    )


def _item(case, text, *, actor="person", due=None):
    from cases.services import add_checklist_item

    return add_checklist_item(case, requirement=text, responsible_actor=actor, due_date=due)


def _file(requirement, user):
    from documents import services

    return services.file_version(requirement, user, SimpleUploadedFile("piece.pdf", MINIMAL_PDF, "application/pdf"))


def _next(case, **kwargs):
    from cases.services import next_action

    return next_action(case, **kwargs)


# ---- T1: one next action over every open obligation ------------------------------------------------------------------
pytestmark = pytest.mark.django_db


def test_t1_the_nearest_date_wins_whatever_the_obligation(case):
    _item(case, "Étape lointaine", due=_days(40))
    piece = _piece(case, "acte", due=_days(20), title="Acte d’état civil légalisé")
    action = _next(case)
    assert (action.kind, action.label, action.urgency) == ("piece", "Acte d’état civil légalisé", "soon")
    assert action.piece_id == str(piece.pk) and action.due_date == _days(20) and action.state == "missing"
    assert action.url.endswith(f"/requirements/{piece.pk}/"), "a piece has a page: the action leads to it"


def test_t1_an_overdue_obligation_comes_first_item_or_piece(case):
    _piece(case, "bientot", due=_days(5))
    _item(case, "En retard", due=_days(-20))
    assert (_next(case).label, _next(case).urgency, _next(case).kind) == ("En retard", "overdue", "item")


def test_t1_an_overdue_piece_comes_before_an_item_due_soon(case):
    _item(case, "Bientôt", due=_days(5))
    _piece(case, "retard", due=_days(-20), title="Pièce en retard")
    action = _next(case)
    assert (action.label, action.urgency, action.kind) == ("Pièce en retard", "overdue", "piece")


def test_t1_on_the_same_date_the_item_keeps_its_place_before_the_piece(case):
    _piece(case, "meme-jour", due=_days(10))
    _item(case, "Le même jour", due=_days(10))
    assert _next(case).kind == "item", "on a tie the order before T1 holds: the checklist first"


def test_t1_without_a_date_the_persons_own_obligation_comes_first(case):
    _item(case, "Délivrance par l’autorité", actor="authority")
    _piece(case, "a-vous", title="Pièce à fournir")
    action = _next(case)
    assert action.label == "Pièce à fournir" and not action.is_for_someone_else


def test_t1_without_a_date_and_nothing_of_the_persons_the_first_of_anybodys(case):
    _item(case, "Délivrance par l’autorité", actor="authority")
    _piece(case, "entreprise", actor="company")
    action = _next(case)
    assert action.label == "Délivrance par l’autorité" and action.is_for_someone_else


def test_t1_a_piece_that_satisfies_an_item_stands_for_it_once(case):
    from cases.services import _open_obligations

    item = _item(case, "Obtenir la déclaration de valeur")
    _piece(case, "declaration", item=item, title="Déclaration de valeur")
    assert [row.kind for row in _open_obligations(case)] == ["piece"], "one obligation, drawn once: the piece"
    assert _next(case).label == "Déclaration de valeur"


def test_t1_an_open_piece_comes_before_the_questionnaire_and_nothing_left_means_the_questionnaire(case, person):
    from cases.models import CaseStatus

    assert case.status == CaseStatus.DRAFT
    assert _next(case).kind == "orientation", "a draft file with nothing open: the questionnaire"
    piece = _piece(case, "a-remplacer")
    assert _next(case).piece_id == str(piece.pk), "the person's open piece before the questionnaire"
    _file(piece, person)
    assert _next(case).kind == "orientation", "a filed piece is in a reviewer's hands: no longer an obligation"


def test_t1_a_restricted_piece_is_named_only_to_an_account_that_may_read_it(case, person, user_factory):
    from cases.models import AssignmentRole
    from cases.services import assign
    from documents.models import AccessClass

    piece = _piece(case, "famille", access=AccessClass.RESTRICTED, title="Livret de famille")
    professional = user_factory("dash.pro@example.test", role=roles.PROFESSIONAL, terms_accepted_at=clock.now())
    assign(case, professional, role=AssignmentRole.PROFESSIONAL, mandate_note="mandat de test")
    assert _next(case).label != "Livret de famille", "nobody said who is looking: only what every reader may read"
    assert _next(case, reader=professional).label != "Livret de famille", "kept to the person and the administration"
    assert _next(case, reader=person).piece_id == str(piece.pk)


def test_t1_a_blocking_outcome_still_comes_first_and_leads_to_its_page(case):
    from cases.models import AssessmentOutcome
    from cases.services import record_assessment
    from cases.tests.test_lifecycle import SNAPSHOT

    _item(case, "En retard", due=_days(-5))
    assessment = record_assessment(
        case,
        outcome=AssessmentOutcome.STOP,
        ruleset_version=1,
        ruleset_snapshot=SNAPSHOT,
        answers={"objective": "work"},
    )
    action = _next(case)
    assert (action.urgency, action.kind) == ("blocked", "outcome")
    assert action.url.endswith(f"/{case.reference}/pre-evaluation/{assessment.pk}/")


def test_t1_the_case_views_name_the_same_action_as_the_dashboard(client, case, person):
    piece = _piece(case, "acte", due=_days(12), title="Acte d’état civil légalisé")
    client.force_login(person)
    from portal import services

    assert services.dashboard_context(person)["now"]["piece_id"] == str(piece.pk)
    detail = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/")
    assert detail.status_code == 200 and detail.context["next_action"].piece_id == str(piece.pk)


# ---- the NowPanel --------------------------------------------------------------------------------------------------
def _now(user):
    from portal import services

    return services.dashboard_context(user)["now"]


def test_now_panel_without_a_file_opens_one(person):
    now = _now(person)
    assert now["variant"] == "no-case" and str(now["title"]) == "Le questionnaire d’orientation"
    assert now["primary"] is None or str(now["primary"]["label"]) == "Commencer le questionnaire"


def test_now_panel_yours_does_the_act_in_the_registers_words(case, person):
    piece = _piece(case, "acte", due=_days(9))
    now = _now(person)
    assert (now["variant"], now["piece_id"]) == ("yours", str(piece.pk))
    assert str(now["primary"]["label"]) == "Déposer la pièce" and now["primary"]["url"].endswith(f"/{piece.pk}/")
    assert now["due"]["date"] == _days(9) and now["due"]["urgency"] == "soon" and str(now["due"]["word"]) == "Bientôt"
    assert now["state"]["producer"] == "documents.RequirementState" and str(now["responsible"]["label"])
    from documents.services import request_replacement

    _file(piece, person)
    request_replacement(piece, actor=person, reason="Illisible")
    assert str(_now(person)["primary"]["label"]) == "Remplacer la pièce", "a piece with a version is replaced"


def test_now_panel_never_promises_an_act_its_target_cannot_do_when_the_conditions_block_the_filing(
    client, case, person
):
    """The W3-B review's M1 (and the check's 2.5.3 finding): the terms page has nothing to accept until the acceptance
    flow exists (G1), so the panel reads the piece on its own page — «Consulter», as the dashboard's rows say — and
    its note says why, in the register's own words; no button names an act the page cannot do, and no accessible name
    differs from the words shown."""
    from django.urls import reverse
    from django.utils import translation

    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    piece = _piece(case, "acte", due=_days(9))
    now = _now(person)
    assert now["variant"] == "yours" and now["piece_id"] == str(piece.pk)
    assert str(now["primary"]["label"]) == "Consulter" and now["primary"]["url"].endswith(f"/{piece.pk}/")
    assert "aria_label" not in now["primary"]
    assert str(now["note"]) == "Acceptation des Conditions d’utilisation requise."
    for lang in ("fr", "ar"):
        work = _workspace(_page(client, person, lang))
        panel = work.split('class="card card--action db-now', 1)[1].split("</section>", 1)[0]
        assert reverse("legal:terms") not in panel and 'aria-label="' not in panel, lang
        assert panel.count("data-now-primary") == 1, lang
    client.logout()
    person.terms_accepted_at = clock.now()
    person.save(update_fields=["terms_accepted_at"])
    with translation.override("fr"):  # the Arabic page above left its language active in this thread
        accepted = _now(person)
    assert str(accepted["primary"]["label"]) == "Déposer la pièce" and accepted["note"] == "", "the gate lifted"


def test_now_panel_in_somebody_elses_hands_says_so_and_offers_no_primary(case, person):
    _piece(case, "nulla-osta", actor="authority", title="Nulla osta au travail")
    now = _now(person)
    assert now["variant"] == "third" and now["primary"] is None
    assert str(now["note"]) == "Cette étape ne dépend pas de vous." and str(now["secondary"]["label"]) == "Consulter"


def test_now_panel_with_nothing_to_do_says_so(case, person):
    from cases.models import CaseStatus
    from cases.services import transition

    transition(case, CaseStatus.ORIENTED)
    now = _now(person)
    assert now["variant"] == "nothing" and now["primary"] is None
    assert str(now["title"]) == "Aucune action ne vous est demandée pour l’instant."
    assert now["responsible"] is None, "nobody is assigned: the panel names nobody"


def test_now_panel_with_nothing_to_do_says_whose_hands_the_file_is_in(client, case, person, user_factory):
    """The review's m2: «rien à faire» names the file's live assignment — its role and its organisation, as the file's
    strip says them —, the organisation's words isolated in their own direction."""
    from accounts.models import Organisation, OrganisationKind
    from cases.models import CaseStatus
    from cases.services import assign, transition

    agency = Organisation.objects.create(
        name="Agenzia di prova (Roma).", kind=OrganisationKind.COMPANY, country="IT", city="Roma"
    )
    professional = user_factory("dash.professional@example.test", role=roles.PROFESSIONAL)
    assign(case, professional, role="professional", organisation=agency)
    transition(case, CaseStatus.ORIENTED)
    now = _now(person)
    assert now["variant"] == "nothing" and now["primary"] is None
    assert now["responsible"]["actor"] == "professional" and now["responsible"]["organisation"] == agency.name
    work = _workspace(_page(client, person, "ar"))
    panel = work.split('class="card card--action db-now', 1)[1].split("</section>", 1)[0]
    assert '<span dir="auto">Agenzia di prova (Roma).</span>' in panel


def test_an_overdue_date_takes_the_now_panel_over_and_is_drawn_there_only(case, person):
    from portal import services
    from portal.models import Deadline

    _piece(case, "plus-tard", due=_days(30))
    deadline = Deadline.objects.create(
        owner=person, title="Convocation au consulat", due_on=clock.today() - dt.timedelta(days=3)
    )
    context = services.dashboard_context(person)
    assert context["now"]["takeover"] == "overdue" and context["now"]["title"] == "Convocation au consulat"
    assert context["now"]["deadline_pk"] == deadline.pk and str(context["now"]["due"]["word"]) == "En retard"
    assert all(row["pk"] != deadline.pk for row in context["deadlines"]), "one date, drawn once"


def test_the_takeover_draws_the_teams_words_in_their_own_direction_under_origine(client, case, person):
    """The review's M2 and m8, the check's finding 1: a date's title and its source note are the team's own words, in
    no language the data records — on an Arabic page they keep their direction (dir="auto"; the box on the panel's
    reading edge) and their brackets and final point where they were written; the note stands under the deadlines
    page's «Origine :», in the page's language."""
    from portal.models import Deadline

    _piece(case, "plus-tard", due=_days(30))
    Deadline.objects.create(
        owner=person,
        title="[revue] Rendez-vous au consulat — confirmer la date",
        due_on=clock.today() - dt.timedelta(days=3),
        source_note="Note de test (lane 6, revue).",
    )
    ar = _workspace(_page(client, person, "ar"))
    title = '<h2 class="db-now__title" id="db-now-title" dir="auto">[revue] Rendez-vous au consulat — confirmer la date</h2>'
    assert title in ar
    note = '<span dir="auto">Note de test (lane 6, revue).</span></p>'
    assert f'<p class="db-now__text"><span class="db-now__label">المصدر:</span> {note}' in ar
    fr = _workspace(_page(client, person, "fr"))
    assert f'<p class="db-now__text"><span class="db-now__label">Origine\u00a0:</span> {note}' in fr


def test_the_takeovers_only_date_leaves_no_empty_section_behind(client, case, person):
    """The review's m1: when the one date is the NowPanel's, «Mes échéances» is not drawn — the panel holds the date
    and the way to every date; a second date brings the section back, with its link."""
    from django.urls import reverse

    from portal.models import Deadline

    _piece(case, "plus-tard", due=_days(30))
    Deadline.objects.create(owner=person, title="Convocation", due_on=clock.today() - dt.timedelta(days=3))
    work = _workspace(_page(client, person))
    assert 'data-now="yours"' in work and "db-now--overdue" in work
    assert 'class="db-dates"' not in work, "no head with nothing under it"
    assert work.count(f'href="{reverse("portal:deadlines")}"') == 1, "the way to every date: the panel's primary"
    Deadline.objects.create(owner=person, title="Visite médicale", due_on=_days(20))
    work = _workspace(_page(client, person))
    dates = work.split('class="db-dates"', 1)[1].split("</section>", 1)[0]
    assert '<span class="db-list__title" dir="auto">Visite médicale</span>' in dates
    assert "Toutes mes échéances" in dates


def test_an_overdue_obligation_is_not_taken_over_by_a_date(case, person):
    from portal.models import Deadline

    _item(case, "Étape en retard", due=_days(-10))
    Deadline.objects.create(owner=person, title="Convocation", due_on=clock.today() - dt.timedelta(days=3))
    now = _now(person)
    assert now["title"] == "Étape en retard" and now["takeover"] == "overdue" and now["deadline_pk"] is None


# ---- F9 and the pieces -----------------------------------------------------------------------------------------------
def test_a_persons_dashboard_builds_no_card_grid(person, monkeypatch):
    from portal import services

    def refuse(user):  # pragma: no cover - the point is that it is never called
        raise AssertionError("a person's dashboard built a card of the bridge")

    for name in ("_requests_card", "_documents_card", "_deadlines_card", "_messages_card", "_organisation_card"):
        monkeypatch.setattr(services, name, refuse)
    assert services.dashboard_context(person)["cards"] == []


def test_the_bridge_keeps_its_cards(user_factory):
    from portal import services

    company = user_factory("dash.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    context = services.dashboard_context(company)
    assert not context["is_person"] and context["now"] is None
    assert [card.key for card in context["cards"]][:1] == ["requests"]


def test_the_pieces_by_who_holds_them_the_persons_first_the_now_panels_piece_once(case, person):
    from portal import services

    now_piece = _piece(case, "acte", due=_days(9))
    later = _piece(case, "casier", due=_days(30))
    theirs = _piece(case, "nulla-osta", actor="authority")
    filed = _piece(case, "passeport")
    _file(filed, person)
    context = services.dashboard_context(person)
    pieces = context["pieces"]
    groups = {group["key"]: len(group["states"]) for group in pieces["groups"]}
    assert groups == {"to-act": 2, "in-hand": 2}, groups
    ids = [row["id"] for row in pieces["rows"]]
    assert str(now_piece.pk) not in ids and pieces["now"]["id"] == str(now_piece.pk)
    assert ids[0] == str(later.pk) and set(ids[1:]) == {str(theirs.pk), str(filed.pk)}
    assert [row["is_yours"] for row in pieces["rows"]] == [True, False, False]


def test_a_piece_the_person_filed_names_no_party_its_chip_says_it(client, case, person):
    """The review's m3: a piece the person answers for, filed or in review, is not «in somebody else's hands» under
    the person's own name — its row names no party (the chip «Déposé» says it); a piece another actor holds names
    that actor."""
    filed = _piece(case, "passeport", title="Passeport en cours de validité")
    _file(filed, person)
    theirs = _piece(case, "nulla-osta", actor="authority", title="Nulla osta au travail")
    _piece(case, "acte", due=_days(9))
    work = _workspace(_page(client, person))
    row = work.split(f'data-piece="{filed.pk}"', 1)[1].split("</li>", 1)[0]
    assert "db-task__who" not in row and "Déposé" in row
    other = work.split(f'data-piece="{theirs.pk}"', 1)[1].split("</li>", 1)[0]
    assert "db-task__who" in other


def test_the_files_progress_keeps_its_figures_together(client, case, person):
    """The review's m11: the strip's progress ties its two figures and the word between them with no-break spaces —
    the Arabic line left its total alone on the next line. The words are the catalogue's."""
    from cases.models import ChecklistStatus
    from cases.services import progress

    item = _item(case, "Étape faite")
    item.status = ChecklistStatus.DONE
    item.save()
    _item(case, "Étape ouverte")
    done, total = progress(case)["done"], progress(case)["total"]
    assert done >= 1 and total >= 2
    fr = _workspace(_page(client, person))
    assert f"{done}\u00a0sur\u00a0{total} éléments complétés" in fr
    ar = _workspace(_page(client, person, "ar"))
    assert f"العناصر المكتملة: {done}\u00a0من\u00a0{total}" in ar


def test_the_now_panel_is_named_by_whose_move_it_is_and_by_the_obligation(client, case, person):
    """The check's finding 6: heading and region navigation hear the eyebrow — «Votre prochaine action» — before the
    obligation; the h2 stays the obligation."""
    _piece(case, "acte", due=_days(9), title="Acte d’état civil légalisé")
    work = _workspace(_page(client, person))
    assert 'aria-labelledby="db-now-eyebrow db-now-title"' in work
    assert '<span id="db-now-eyebrow">Votre prochaine action</span>' in work


# ---- the page --------------------------------------------------------------------------------------------------------
def _page(client, user, lang="fr"):
    client.force_login(user)
    response = client.get(DASHBOARD.format(lang=lang))
    assert response.status_code == 200
    return response.content.decode("utf-8")


def _workspace(html: str) -> str:
    return html.split('class="console__workspace"', 1)[1].split('class="portal-footer', 1)[0]


def test_the_page_h1_then_the_now_panel_then_the_journey_one_primary_each_piece_once(client, case, person):
    _piece(case, "acte", due=_days(9))
    _piece(case, "casier", due=_days(30))
    _piece(case, "nulla-osta", actor="authority")
    html = _page(client, person)
    work = _workspace(html)
    assert work.index("<h1") < work.index('class="card card--action db-now') < work.index('class="db-journey"')
    assert work.count("btn--primary") == 1, "one primary on the screen: the NowPanel's"
    pieces = re.findall(r'data-piece="([^"]+)"', work)
    assert len(pieces) == 3 and len(set(pieces)) == 3, "no piece drawn twice"
    assert work.count("card--action") == 1, "one raised panel"
    assert not re.search(r"stat-card|portal-cards|portal-card__count|summary__figure", work), "no stat card"


@pytest.mark.parametrize("variant", ["no-case", "yours", "third", "nothing"])
def test_the_four_now_panel_variants_are_composed(client, person, variant):
    from cases.models import CasePurpose, CaseStatus
    from cases.services import open_case, transition

    if variant != "no-case":
        case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
        if variant == "yours":
            _piece(case, "acte")
        elif variant == "third":
            _piece(case, "nulla-osta", actor="authority")
        else:
            transition(case, CaseStatus.ORIENTED)
    html = _page(client, person)
    assert f'data-now="{variant}"' in html
    # the console's one empty state shows the owner's door, as the doorway component draws it — and only there
    door = '<svg class="doorway db-now__door" viewBox="264 64 368 456" aria-hidden="true" focusable="false">'
    assert (door in html) is (variant == "no-case")


def test_a_french_record_keeps_its_language_and_direction_on_an_arabic_page(client, case, person):
    _piece(case, "acte", due=_days(9), title="Acte d’état civil légalisé")
    html = _page(client, person, "ar")
    assert re.search(
        r'<h2 class="db-now__title" id="db-now-title" lang="fr" dir="ltr">Acte d’état civil légalisé</h2>', html
    )
    assert '<html lang="ar" dir="rtl" class="no-js">' in html


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


def test_every_word_on_the_dashboard_is_the_catalogues_no_new_copy():
    known = _catalogue_msgids()
    missing = sorted(msgid for msgid in _msgids(TEMPLATE.read_text(encoding="utf-8")) if msgid not in known)
    assert not missing, f"new copy on the dashboard (it goes to the owner's copy packet first): {missing}"


# ---- the partial -----------------------------------------------------------------------------------------------------
def _css() -> str:
    return re.sub(r"/\*.*?\*/", "", PARTIAL.read_text(encoding="utf-8"), flags=re.S)


def test_the_partial_is_the_consoles_after_the_shell_and_never_an_output_of_its_own():
    entry = ENTRY.read_text(encoding="utf-8")
    imports = re.findall(r'@import url\("([^"]+)"\);', entry)
    assert imports.index("v5/_dashboard.css") == imports.index("v5/_shell.css") + 1
    assert not (ROOT / "static" / "css" / "dist" / "portal" / "v5" / "_dashboard.css").exists()
    bundle = (ROOT / "static" / "css" / "dist" / "portal" / "console.css").read_text(encoding="utf-8")
    assert ".db-now__title" in bundle and ".db-ledger__marks" in bundle


def test_the_partial_draws_with_tokens_and_logical_properties_only():
    css = _css()
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|gradient\(", css), "tokens only"
    physical = re.findall(
        r"(?<![\w-])(?:margin|padding|border)-(?:left|right|top|bottom)\b|(?<![\w-])(?:left|right|top|bottom)\s*:", css
    )
    assert not physical, f"logical properties only: {physical}"
    assert "text-align: left" not in css and "text-align: right" not in css


def test_the_partial_adds_no_plane_no_motion_and_no_corner_of_its_own():
    css = _css()
    shadows = set(re.findall(r"box-shadow:\s*([^;]+);", css))
    assert shadows <= {"none"}, f"the one plane is the action card's (v5/card.css): {shadows}"
    assert "@keyframes" not in css
    assert set(re.findall(r"(?<![\w-])animation:\s*([^;]+);", css)) <= {"none"}, "nothing animates at load"
    for value in re.findall(r"transition:\s*([^;]+);", css):
        assert re.fullmatch(r"color var\(--motion-[a-z]+\) var\(--ease-[a-z]+\)", value.strip()), value
    assert set(re.findall(r"border-radius:\s*([^;]+);", css)) <= {"var(--radius-full)"}, "the panels' 8 is the card's"


# ======================================================================================================================
# Step 2 — the company's dashboard and the bridge of the accounts that are not a person (plan §3.5 item 4: «the company
# dashboard, the institution / university bridge»; NOTES.md «Step 2/2»)
# ======================================================================================================================
COMPANY_DASHBOARD = "/{lang}/espace-reserve/entreprise/"
COMPANY_TEMPLATE = ROOT / "templates" / "companies" / "dashboard.html"
NOW_PARTIAL = ROOT / "templates" / "portal" / "partials" / "now_panel.html"
BRIDGE_PARTIAL = ROOT / "templates" / "portal" / "partials" / "card.html"


@pytest.fixture
def make_company(user_factory):
    """A company, its organisation, its responsible account and its verification — the shape of the company app's own
    fixture (apps/companies/tests/conftest.py), which an app package keeps to itself."""
    from accounts.models import (
        AccountVerification,
        Membership,
        MembershipRole,
        Organisation,
        OrganisationKind,
        VerificationStatus,
    )
    from companies.models import CompanyProfile, Sector

    def _make(slug="dash", *, verified=True):
        user = user_factory(f"{slug}.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
        organisation = Organisation.objects.create(
            name=f"Organisation {slug}", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
        )
        Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
        AccountVerification.objects.create(
            user=user,
            declared_type=AccountType.COMPANY,
            status=VerificationStatus.APPROVED if verified else VerificationStatus.PENDING,
            decided_at=timezone.now() if verified else None,
        )
        sector, _created = Sector.objects.get_or_create(
            code="batiment", defaults={"label_fr": "Bâtiment et travaux publics", "order": 10}
        )
        profile = CompanyProfile.objects.create(
            organisation=organisation,
            legal_name=f"Société {slug} S.r.l.",
            registration_number=f"RM-{slug.upper()}-01",
            sector=sector,
            contact_name="Référent de test",
            contact_function="Responsable des ressources humaines",
            contact_email=f"referent-{slug}@example.test",
            city="Rovigo",
            country="IT",
        )
        return profile, user

    return _make


def _need(company, title, status="draft", *, complete=True):
    from companies.models import CompanyNeed, NeedSkill, Sector, SkillLevel, Territory

    territory, _created = Territory.objects.get_or_create(
        code="veneto", defaults={"label_fr": "Vénétie", "country": "IT", "order": 10}
    )
    need = CompanyNeed.objects.create(
        company=company,
        title=title,
        territory=territory if complete else None,
        sector=Sector.objects.get(code="batiment") if complete else None,
        professional_profile="Technicien de maintenance" if complete else "",
        duties="Entretien préventif et correctif des lignes." if complete else "",
        headcount=2,
        status=status,
    )
    if complete:
        NeedSkill.objects.create(need=need, label="Mécanique industrielle", level=SkillLevel.MANDATORY)
    return need


def _composition(company):
    from companies import services as companies
    from portal import services

    needs = list(companies.needs_of(company)) if company is not None else []
    return services.company_dashboard(company, needs, companies.next_action(company, needs))


# ---- the company's NowPanel: the company's one next action, on the person's plane ---------------------------------
def test_the_company_now_panel_declares_verifies_creates_completes_transmits_and_rests(make_company):
    from django.urls import reverse

    declare = _composition(None)["now"]
    assert declare["variant"] == "yours" and declare["primary"]["label"] == "Déclarer mon entreprise"
    assert declare["primary"]["url"] == reverse("companies:profile_create") and declare["need_ref"] == ""
    assert declare["responsible"]["actor"] == "company" and declare["responsible"]["label"] == "Votre entreprise"

    unverified, _user = make_company("unverified", verified=False)
    waiting = _composition(unverified)["now"]
    assert waiting["variant"] == "third" and waiting["primary"] is None
    assert waiting["note"] == "Cette étape ne dépend pas de vous." and waiting["responsible"]["actor"] == "project_team"

    company, _user = make_company("verified")
    first = _composition(company)["now"]
    assert first["variant"] == "yours" and first["primary"]["url"] == reverse("companies:need_create")

    draft = _need(company, "Soudure d’assemblage", complete=False)
    complete = _composition(company)["now"]
    assert complete["need_ref"] == draft.reference and complete["state"]["value"] == "draft"
    assert complete["primary"]["url"] == reverse("companies:need_edit", args=[draft.reference])

    draft.status = "submitted"
    draft.save()
    under_review = _composition(company)["now"]
    assert under_review["variant"] == "third" and under_review["primary"] is None and under_review["need_ref"] == ""

    draft.status = "in_progress"
    draft.save()
    rest = _composition(company)["now"]
    assert rest["variant"] == "nothing" and rest["primary"] is None
    assert rest["title"] == "Aucune action ne vous est demandée pour l’instant."


def test_the_needs_by_who_holds_them_the_companys_drafts_first_the_now_panels_need_once(make_company):
    company, _user = make_company("ledger")
    now_need = _need(company, "Incomplet", complete=False)  # the oldest incomplete draft: the NowPanel's
    other_draft = _need(company, "Brouillon complet")
    submitted = _need(company, "Transmis", "submitted")
    taken = _need(company, "Pris en charge", "in_progress")
    closed = _need(company, "Clos", "closed")
    withdrawn = _need(company, "Retiré", "withdrawn")
    composition = _composition(company)
    ledger = composition["needs_ledger"]
    assert composition["now"]["need_ref"] == now_need.reference
    assert {group["key"]: len(group["states"]) for group in ledger["groups"]} == {
        "to-act": 2,
        "in-hand": 2,
        "settled": 2,
    }
    assert [str(group["label"]) for group in ledger["groups"]] == ["À faire", "En cours", "Clos"]
    rows = [need.reference for need in ledger["rows"]]
    assert now_need.reference not in rows, "the NowPanel's need is drawn there and only there"
    assert rows[0] == other_draft.reference, "the company's own drafts come first"
    assert set(rows[1:3]) == {submitted.reference, taken.reference}
    assert len(rows) == 5 and set(rows[3:]) <= {closed.reference, withdrawn.reference}
    assert ledger["more"] == 0


def _company_page(client, user, lang="fr"):
    client.force_login(user)
    response = client.get(COMPANY_DASHBOARD.format(lang=lang))
    assert response.status_code == 200
    return response.content.decode("utf-8")


def test_the_company_page_h1_then_the_now_panel_one_primary_one_plane_each_need_once(client, make_company):
    company, user = make_company("page")
    _need(company, "Soudure d’assemblage")
    _need(company, "Conduite d’engins", "under_review")
    _need(company, "Maintenance", "in_progress")
    work = _workspace(_company_page(client, user))
    assert work.index("<h1") < work.index('class="card card--action db-now') < work.index('class="db-file db-company"')
    assert work.count("btn--primary") == 1, "one primary on the screen: the NowPanel's"
    assert work.count("card--action") == 1, "one raised panel"
    needs = re.findall(r'data-need="([^"]+)"', work)
    assert len(needs) == 3 and len(set(needs)) == 3, "no need drawn twice"
    assert not re.search(r"stat-card|portal-card|card--stat|data-count|__figure|class=\"panel", work), "no stat card"
    assert "Société page S.r.l." in work and work.count("Société page S.r.l.") == 1, "the legal name is said once"


@pytest.mark.parametrize("state", ["no-company", "unverified", "draft", "nothing"])
def test_the_company_now_panel_variants_are_composed(client, make_company, user_factory, state):
    if state == "no-company":
        user = user_factory("prospect.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
        expected, primaries = "yours", 1
    elif state == "unverified":
        _company, user = make_company("pending", verified=False)
        expected, primaries = "third", 0
    else:
        company, user = make_company(state)
        _need(company, "Besoin", "draft" if state == "draft" else "in_progress")
        expected, primaries = ("yours", 1) if state == "draft" else ("nothing", 0)
    work = _workspace(_company_page(client, user))
    assert f'data-now="{expected}"' in work
    assert work.count("btn--primary") == primaries
    assert "doorway" not in work, "the door is the person's one empty state, not the company's"


def test_a_need_can_be_prepared_before_the_verification_and_creation_is_offered_once(client, make_company):
    from django.urls import reverse

    create = f'href="{reverse("companies:need_create")}"'
    _pending, waiting = make_company("waiting", verified=False)
    work = _workspace(_company_page(client, waiting))
    assert work.count(create) == 1 and "btn--primary" not in work, "the act stays offered while the project verifies"
    client.logout()
    _verified, first = make_company("first")
    work = _workspace(_company_page(client, first))
    assert work.count(create) == 1 and f'class="btn btn--primary btn--arrow" {create}' in work, "once: the primary"


def test_the_company_dashboard_renders_in_arabic_with_the_name_on_the_reading_edge(client, make_company):
    company, user = make_company("rtl")
    _need(company, "Soudure d’assemblage", "submitted")
    html = _company_page(client, user, "ar")
    assert '<html lang="ar" dir="rtl" class="no-js">' in html
    assert '<h1 class="ctx__title" dir="auto">Société rtl S.r.l.</h1>' in html
    assert re.search(r'<a href="[^"]+" dir="auto">Soudure d’assemblage</a>', html), "a need's title keeps its direction"


def test_the_company_now_panel_carries_the_need_pages_own_act_to_transmit(client, make_company):
    """The review's m4, the team's decision: when the next action is to transmit a complete draft and the account may
    submit it, the NowPanel carries the need page's own act — its POST form and its words, «Transmettre au projet» —
    with the need in view (its title, its state, its reference); «Ouvrir le besoin» stays beside it, quiet. One verb,
    one click; the link is never relabelled as the act. Without an account that may submit, the link as before."""
    from django.urls import reverse

    from companies import services as companies
    from portal import services

    company, user = make_company("transmit")
    need = _need(company, "Soudure d’assemblage")
    needs = list(companies.needs_of(company))
    action = companies.next_action(company, needs)
    submit_url = reverse("companies:need_submit", args=[need.reference])
    now = services.company_dashboard(company, needs, action, user=user)["now"]
    assert now["primary"] == {"label": "Transmettre au projet", "url": submit_url, "method": "post"}
    assert now["secondary"] == {
        "label": "Ouvrir le besoin",
        "url": reverse("companies:need_detail", args=[need.reference]),
    }
    assert now["need_ref"] == need.reference and now["state"]["value"] == "draft"
    bare = services.company_dashboard(company, needs, action)["now"]
    assert (
        bare["primary"]["label"] == "Ouvrir le besoin" and "method" not in bare["primary"] and bare["secondary"] is None
    )

    work = _workspace(_company_page(client, user))
    panel = work.split('class="card card--action db-now', 1)[1].split("</section>", 1)[0]
    assert f'<form class="db-now__form" method="post" action="{submit_url}">' in panel
    assert 'name="csrfmiddlewaretoken"' in panel and panel.count("btn--primary") == 1
    assert f'<span class="db-ref">{need.reference}</span>' in panel, "the need in view: its reference"
    assert work.count("btn--primary") == 1, "one primary on the screen"
    assert client.post(submit_url).status_code == 302
    need.refresh_from_db()
    assert need.status == "submitted", "the panel's act is the act"


def test_the_company_now_panel_title_keeps_its_guillemets_with_their_words(client, make_company):
    """The review's m5: the catalogue's title passes the French-spacing filter (W2-D's ``typo``) — a no-break space
    inside « » — so no line ends on an opening guillemet at 390 or 360."""
    company, user = make_company("typo")
    _need(company, "Soudure d’assemblage sur charpente métallique")
    work = _workspace(_company_page(client, user))
    assert "Transmettez le besoin «\u00a0Soudure d’assemblage sur charpente métallique\u00a0» au projet" in work


def test_the_company_account_without_a_company_has_its_communications_beside_the_now_panel(client, user_factory):
    """The review's m9: without a company the NowPanel no longer stands alone on eight columns — the account's
    communications stand beside it, as a person's page draws them without a file; a subject in its own direction."""
    from portal.models import Message

    user = user_factory("lonely.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    Message.objects.create(recipient=user, subject="Bienvenue (espace entreprise).", body="Corps du message.")
    work = _workspace(_company_page(client, user, "ar"))
    assert '<div class="db db--company">' in work, "no file, no company: the side takes the first row (the grid's rule)"
    assert work.index('class="card card--action db-now') < work.index('<div class="db-side">')
    side = work.split('<div class="db-side">', 1)[1]
    assert '<span class="db-list__title" dir="auto">Bienvenue (espace entreprise).</span>' in side


# ---- the bridge: the accounts that are not a person ----------------------------------------------------------------
@pytest.fixture
def institution(user_factory):
    from accounts.models import Membership, Organisation, OrganisationKind
    from portal.models import Deadline, Message

    user = user_factory("dash.institution@example.test", role=roles.INSTITUTION, account_type=AccountType.INSTITUTION)
    organisation = Organisation.objects.create(
        name="Institution de test", kind=OrganisationKind.INSTITUTION, country="MA", city="Rabat"
    )
    Membership.objects.create(user=user, organisation=organisation)
    Deadline.objects.create(owner=user, title="Convention à transmettre", due_on=_days(-3))
    Message.objects.create(recipient=user, subject="Calendrier des sessions", body="Corps du message.")
    return user


def test_the_bridge_draws_its_registers_in_the_persons_grammar_and_claims_no_next_action(client, institution):
    html = _page(client, institution)
    work = _workspace(html)
    assert "db-now" not in work and "btn--primary" not in work, "no NowPanel: the system knows no next action here"
    assert "card--action" not in work, "no raised plane"
    main = work.split('<div class="db-main">', 1)[1].split('<div class="db-side">', 1)[0]
    side = work.split('<div class="db-side">', 1)[1]
    assert re.findall(r'data-card="(\w+)"', main) == ["deadlines", "messages", "requests", "documents"], (
        "what is due and what came in first: the system orders priority"
    )
    assert re.findall(r'data-card="(\w+)"', side)[:1] == ["organisation"]
    assert "Convention à transmettre" in main and "Calendrier des sessions" in main
    assert "Institution de test" in side and "Rabat" in side
    for banned in ("portal-cards", "portal-card", "data-count", 'class="empty-state"', "card--stat"):
        assert banned not in work, banned
    assert 'class="db-account"' in work, "the account's quiet line closes the bridge as it closes the person's page"


def test_on_the_bridge_a_date_past_due_speaks_azione_never_the_red_of_a_refusal(client, institution):
    side = _workspace(_page(client, institution)).split('data-card="deadlines"', 1)[1].split("</section>", 1)[0]
    registers = re.findall(r'data-register="([a-z]+)"', side)
    assert registers and set(registers) == {"azione"}, registers  # «1 en retard» on the head, «En retard» on the row


def test_the_bridge_for_a_university_says_each_empty_region_in_one_line(client, user_factory):
    university = user_factory(
        "dash.university@example.test", role=roles.UNIVERSITY, account_type=AccountType.UNIVERSITY
    )
    work = _workspace(_page(client, university))
    assert work.count('class="db-empty"') >= 5, "deadlines, messages, requests, documents, organisation: one line each"
    assert "db-list__row" not in work and "data-count" not in work, "an empty region prints no figure"


def test_the_bridge_says_where_the_accounts_work_lives_in_the_rails_words(client, user_factory):
    """The review's m10: a company account on «Espace réservé» and an authorised actor read, at the head of the main
    column, one quiet link to where their work lives — named as the rail names it; an account with no such place
    (a university) gets none: no claim."""
    from django.urls import reverse

    company = user_factory("bridge.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    main = _workspace(_page(client, company)).split('<div class="db-main">', 1)[1]
    assert main.lstrip().startswith(
        f'<p class="db-space"><a class="db-link" href="{reverse("companies:dashboard")}">Espace entreprise'
    )
    client.logout()
    actor = user_factory(
        "bridge.actor@example.test", role=roles.AUTHORISED_ACTOR, account_type=AccountType.PROFESSIONAL
    )
    main = _workspace(_page(client, actor)).split('<div class="db-main">', 1)[1]
    assert main.lstrip().startswith(
        f'<p class="db-space"><a class="db-link" href="{reverse("selection:workspace")}">Processus assignés'
    )
    client.logout()
    university = user_factory(
        "bridge.university@example.test", role=roles.UNIVERSITY, account_type=AccountType.UNIVERSITY
    )
    assert "db-space" not in _workspace(_page(client, university))


def test_the_bridge_never_draws_the_pre_assessment_twice():
    source = TEMPLATE.read_text(encoding="utf-8")
    assert '{% elif card.key == "orientation" and not assessment %}' in source, (
        "the orientation register gives way to the pre-assessment section that reads it"
    )


# ---- the words, and the partials ----------------------------------------------------------------------------------
def test_every_word_on_the_company_dashboard_and_the_shared_partials_is_the_catalogues():
    known = _catalogue_msgids()
    for path in (COMPANY_TEMPLATE, NOW_PARTIAL, BRIDGE_PARTIAL):
        missing = sorted(msgid for msgid in _msgids(path.read_text(encoding="utf-8")) if msgid not in known)
        assert not missing, f"{path.name}: new copy (it goes to the owner's copy packet first): {missing}"


def test_the_three_dashboards_draw_one_now_panel():
    for path in (TEMPLATE, COMPANY_TEMPLATE):
        source = path.read_text(encoding="utf-8")
        assert source.count('{% include "portal/partials/now_panel.html" with now=now %}') == 1, path.name
        assert "card--action" not in re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", source, flags=re.S), path.name
    partial = NOW_PARTIAL.read_text(encoding="utf-8")
    assert partial.count('class="card card--action db-now') == 1
    # ONE primary: the act's own form (a POST) or the link to the act's page, in one {% if %} … {% elif %} — never both
    acts = re.search(
        r'\{% if now\.primary\.method == "post" %\}(.*?)\{% elif now\.primary %\}(.*?)\{% endif %\}', partial
    )
    assert acts and acts.group(1).count("btn--primary") == 1 and acts.group(2).count("btn--primary") == 1
    assert partial.count("btn--primary") == 2 and 'aria-label="' not in partial, "the visible words are the name"


def test_a_records_own_words_keep_their_direction_in_every_list_of_the_dashboards():
    """The review's M2, the check's finding 1: a date's title, a message's subject and a file's name are a record's own
    words — isolated in their own direction on every dashboard, as the bridge's register already did; so are the
    pre-assessment's rationale (French on an Arabic page: its final point was drawn at the line's start) and an
    organisation's name in the file's strip."""
    person = TEMPLATE.read_text(encoding="utf-8")
    for variable in ("deadline.title", "message.subject", "document.label"):
        assert f'<span class="db-list__title" dir="auto">{{{{ {variable} }}}}</span>' in person, variable
    assert '<p class="db-assessment__text"><span dir="auto">{{ assessment.rationale }}</span></p>' in person
    assert '— <span dir="auto">{{ assignment.organisation.name }}</span>' in person
    company = COMPANY_TEMPLATE.read_text(encoding="utf-8")
    assert '<span class="db-list__title" dir="auto">{{ message.subject }}</span>' in company
    for source in (person, company, BRIDGE_PARTIAL.read_text(encoding="utf-8")):
        assert '<span class="db-list__title">' not in source


def test_the_partials_rules_after_the_review_touch_the_reading_edge_and_the_font_swap():
    """The fixes' rules: the takeover's words hug their box on the reading edge (M2); under a finger a list link's
    words are centred in its 44 px (m6) and an empty line's link is 44 px too (the check's finding 3); the
    «Responsable» disc and its word hold together (m7); the needs' end track is a fixed measure, so a late font
    cannot resize the shared columns (the check's finding 4)."""
    css = _css()
    assert ".db-now__title[dir]" in css and ".db-now__text[dir]" in css
    coarse = css.split("@media (pointer: coarse)", 1)[1].split("@media", 1)[0]
    assert re.search(r"\.db-list__link\s*\{\s*align-items:\s*center;", coarse)
    assert re.search(r"\.db-empty a\s*\{[^}]*min-block-size:\s*var\(--hit-primary\);", coarse)
    assert re.search(r"\.db-now__who\s*\{\s*display:\s*inline-flex;", css)
    assert re.search(
        r"\.db-tasks--needs\s*\{\s*grid-template-columns:\s*minmax\(0, 1fr\) auto minmax\(0, 15rem\);", css
    )


def test_the_consoles_empty_state_spans_the_main_column_again():
    """The review's M3: the bridge's clean-up had taken with it the rule that holds every components/empty_state.html
    of the console's main column across the column, on its start edge — «Communications», «Mes échéances», «Mes
    demandes», «Mon parcours» drew it 42rem wide and centred. Restored, in the source and in the bundle."""
    source = re.sub(
        r"/\*.*?\*/",
        "",
        (ROOT / "apps" / "portal" / "static" / "portal" / "portal.css").read_text(encoding="utf-8"),
        flags=re.S,
    )
    assert re.search(r"\.portal__main \.empty-state\s*\{\s*max-inline-size:\s*none;\s*margin-inline:\s*0;\s*\}", source)
    bundle = (ROOT / "static" / "css" / "dist" / "portal" / "portal.css").read_text(encoding="utf-8")
    assert ".portal__main .empty-state" in bundle


def test_the_company_dashboards_legacy_rules_left_the_v4_sheet_and_the_bridge_left_portal_css():
    workspace = re.sub(
        r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v4" / "workspace.css").read_text(encoding="utf-8"), flags=re.S
    )
    for selector in (
        ".ws-grid",
        ".ws-company",
        ".company-id",
        ".facts",
        ".ctx__count",
        ".ws-next--alone",
        ".ws-assessment",
        ".table--needs",
    ):
        assert not re.search(re.escape(selector) + r"(?![\w-])", workspace), selector
    portal = re.sub(
        r"/\*.*?\*/",
        "",
        (ROOT / "apps" / "portal" / "static" / "portal" / "portal.css").read_text(encoding="utf-8"),
        flags=re.S,
    )
    assert ".portal-card" not in portal, "the bridge's six equal cards left with their grid"
