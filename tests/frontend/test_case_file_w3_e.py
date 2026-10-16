"""
The case file and the console's secondary pages — design V5, family W3-E, the fix pass (docs/design-v5/QA/v54/w3-e/
REVIEW.md, A11Y_PERF.md; the notes' «Review fixes»).

* the case file's first screen holds the next act: the journey in W3-D's compact forms — the card and the disclosure,
  never the dated spine (the dated history is the feed's) —, then the NowPanel (M1, LA-9);
* the NowPanel's checklist line is drawn once: «Exigences» skips it and keeps the file's count; the page keeps the
  line's id on the panel; its act opens the line's alert dialog where the reader may move it — the person's primary, a
  mandated reader's quiet secondary — and there is none where the reader may not (M2);
* the history says «Vous» for the person's acts to the person only, «La personne» to anybody else (M3), and names the
  line a change was about (minor 5);
* the irreversible closures — the guichet's, for the person and the appointed professional, and the selection's — open
  the overlay system's alert dialog, the consequence said, «Annuler» the safe answer; the page links the panels'
  page-only sheet where it draws one (M4);
* a held file's NowPanel (sec-f7's variants) on the file's own page: never a way to the page one is on, the person's
  act for the person only, the reason drawn once;
* a training plan's state is a chip through its producer (minor 9); the plan's scroll region is named by its caption;
* the registers' sheet: a head's acts take the line on a phone (WCAG 1.4.10), a line of facts never ends or opens on its
  point, the filter is one row that scrolls on a phone, a row link's ring keeps its room under forced colours, a
  section's sentence holds the reading measure; the row menu is the system's icon control.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import pytest
from django.utils import translation

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PORTAL_V5 = ROOT / "apps" / "portal" / "static" / "portal" / "v5"
TEMPLATES = ROOT / "templates"
PANELS_LINK = "css/dist/core/overlay-panels.css"


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)


def _block(css: str, at_rule: str) -> str:
    """The body of the first at-rule block that starts with ``at_rule`` (balanced braces)."""
    start = css.index(at_rule)
    depth, i = 0, css.index("{", start)
    for j in range(i, len(css)):
        depth += {"{": 1, "}": -1}.get(css[j], 0)
        if depth == 0:
            return css[i + 1 : j]
    raise AssertionError(at_rule)


def _section(html: str, marker: str) -> str:
    return html.split(marker, 1)[1].split("</section>", 1)[0]


@pytest.fixture
def owner(user_factory):
    return user_factory(
        "w3e.owner@example.test",
        role=roles.PERSON,
        full_name="Owner W3E",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def professional(user_factory):
    return user_factory("w3e.pro@example.test", role=roles.PROFESSIONAL)


@pytest.fixture
def case(owner):
    from cases import services
    from cases.models import CasePurpose, ResponsibleActor

    row = services.open_case(owner, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    services.add_checklist_item(
        row,
        requirement="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        responsible_note="Consulat d’Italie à Casablanca",
        source_title="Code des visas",
        source_ref="Reg. (CE) n. 810/2009, art. 12",
    )
    services.add_checklist_item(row, requirement="Nulla osta al lavoro", responsible_actor=ResponsibleActor.AUTHORITY)
    return row


@pytest.fixture
def assigned(case, professional):
    from cases import services
    from cases.models import AssignmentRole

    services.assign(
        case,
        professional,
        role=AssignmentRole.PROFESSIONAL,
        authorisation_reference="SYNTH-AUTH-0001",
        authorisation_valid_until=clock.today() + dt.timedelta(days=30),
    )
    return case


def _detail(client, user, case, lang="fr") -> str:
    client.force_login(user)
    response = client.get(f"/{lang}/espace-reserve/dossiers/{case.reference}/")
    assert response.status_code == 200
    return response.content.decode("utf-8")


# ---- M1 · the first screen: the compact journey, then the NowPanel ---------------------------------------------------
def test_the_case_file_draws_the_journey_compact_and_the_now_panel_after_it(client, owner, case):
    html = _detail(client, owner, case)
    journey = _section(html, '<section class="db-journey file-journey"')
    assert '<div class="journey-now">' in journey and '<details class="journey-fold">' in journey
    assert "journey--descriptive" not in html and "journey__when" not in journey, "the dated spine is the feed's"
    assert '<summary class="journey-fold__summary">Où j’en suis</summary>' in journey, "the person's own words"
    assert (
        html.index('class="db-journey file-journey"') < html.index('id="db-now-title"') < html.index('id="asked-title"')
    )


def test_a_mandated_reader_s_journey_disclosure_speaks_in_nobody_s_voice(client, assigned, professional):
    journey = _section(_detail(client, professional, assigned), '<section class="db-journey file-journey"')
    assert '<summary class="journey-fold__summary">Parcours</summary>' in journey and "Où j’en suis" not in journey


# ---- M2 · the NowPanel's line, drawn once; its act opens its dialog --------------------------------------------------
def test_the_now_panel_s_line_is_drawn_once_with_its_source_and_its_act_opens_the_line_s_dialog(client, owner, case):
    line = case.checklist.get(requirement="Passeport en cours de validité")
    other = case.checklist.get(requirement="Nulla osta al lavoro")
    html = _detail(client, owner, case)
    assert html.count(f'id="line-{line.pk}"') == 1
    assert f'<div class="file-now" id="line-{line.pk}" tabindex="-1">' in html, "the panel keeps the line's id"
    asked = _section(html, 'aria-labelledby="asked-title"')
    assert f'data-line="{line.pk}"' not in asked and f'data-line="{other.pk}"' in asked, "«Exigences» skips it"
    assert "0 sur 2 éléments complétés" in asked, "the count stays the file's"
    now = html.split('id="db-now-title"', 1)[1].split("</section>", 1)[0]
    assert "Reg. (CE) n. 810/2009, art. 12" in now and "Consulat d’Italie à Casablanca" in now
    assert (
        f'<a class="btn btn--primary" href="#line-{line.pk}-state" data-overlay-open data-now-primary>'
        "Nouvel état de cette ligne</a>" in now
    ), "the act opens the line's alert dialog — never a link that only scrolls"
    assert f'href="#line-{line.pk}"' not in now and "Continuer" not in now, "no «Continuer» that only scrolls"
    assert f'<dialog class="overlay overlay--dialog overlay--alert" id="line-{line.pk}-state"' in html
    bar = html.split("data-file-action-bar", 1)[1].split("</div>", 1)[0]
    assert f'href="#line-{line.pk}-state" data-overlay-open' in bar and "btn--arrow" not in bar
    assert PANELS_LINK in html.split("</head>", 1)[0]


def test_a_mandated_reader_keeps_the_line_s_act_quietly_and_no_primary(client, assigned, professional):
    line = assigned.checklist.get(requirement="Passeport en cours de validité")
    html = _detail(client, professional, assigned)
    now = html.split('id="db-now-title"', 1)[1].split("</section>", 1)[0]
    assert "data-now-primary" not in now and "data-file-action-bar" not in html
    assert (
        f'<a class="btn btn--secondary" href="#line-{line.pk}-state" aria-describedby="db-now-title" data-overlay-open>'
        in now
    )
    assert "Prochaine étape" in html and "Votre prochaine action" not in html


def test_a_line_the_reader_may_not_move_is_drawn_in_the_panel_with_no_act(client, owner, case):
    from cases import services
    from cases.models import ChecklistStatus

    passport = case.checklist.get(requirement="Passeport en cours de validité")
    services.set_checklist_status(passport, ChecklistStatus.DONE, actor=owner)
    authority = case.checklist.get(requirement="Nulla osta al lavoro")
    html = _detail(client, owner, case)
    assert f'<div class="file-now" id="line-{authority.pk}"' in html
    now = html.split('id="db-now-title"', 1)[1].split("</section>", 1)[0]
    assert "Nulla osta al lavoro" in now and "btn" not in now.split("db-now__facts", 1)[1]
    assert "data-file-action-bar" not in html and f'id="line-{authority.pk}-state"' not in html
    assert f'data-line="{passport.pk}"' in html, "a line done stays in «Exigences»"


def test_the_case_now_panel_matches_the_line_by_its_words_date_holder_and_state(owner, case):
    from cases import services
    from portal.services import _now_line, case_lines

    checklist = list(case.checklist.all().order_by("order", "id"))
    for item in checklist:
        item.can_change = True
    lines = case_lines(owner, case, checklist)
    action = services.next_action(case, reader=owner)
    assert _now_line(lines, action)["title"] == "Passeport en cours de validité"
    assert _now_line(lines, None) is None


# ---- a held file (sec-f7's variants), on its own page ----------------------------------------------------------------
@pytest.mark.parametrize("is_own", [True, False])
def test_a_held_file_s_panel_never_leads_to_the_page_one_is_on(monkeypatch, owner, case, is_own):
    from core.links import public_url
    from portal import services

    here = public_url("cases:detail", case.reference)
    held = {
        **services._now_base(),
        "variant": "suspended",
        "eyebrow": "Votre dossier",
        "glyph": "folder",
        "title": "Dossier suspendu",
        "text": "En attente du titre de séjour.",
        "primary": {"label": "Votre dossier", "url": here},
    }
    monkeypatch.setattr(services, "now_panel", lambda *args, **kwargs: dict(held))
    now = services.case_now_panel(owner, case, None, is_own=is_own)
    assert now["variant"] == "suspended" and now["text"] == "En attente du titre de séjour."
    assert now["primary"] is None, "never a way to the page one is on"
    assert (now["eyebrow"] == "Votre dossier") is is_own, "a mandated reader is not addressed as the owner"


def test_a_suspension_s_reason_is_drawn_once():
    source = (TEMPLATES / "cases" / "detail.html").read_text(encoding="utf-8")
    assert '{% if case.suspension_reason and now.variant != "suspended" %}' in source


def test_a_suspended_file_says_its_reason_once_in_its_now_panel(client, owner, assigned, professional):
    """At the merge (w3-e-merge, 16 Oct 2026) sec-f7's held NowPanel met this page: the person's suspended file says its
    state and its reason in the NowPanel, once — no notice of the page's own —, and never a way to the page itself; a
    mandated reader is addressed «Dossier», not «Votre dossier». The two tests above hold the presenter and the template
    each alone; this one renders the page."""
    from cases.models import CaseFile, CaseStatus

    reason = "En attente du titre de séjour."
    CaseFile.objects.filter(pk=assigned.pk).update(status=CaseStatus.SUSPENDED, suspension_reason=reason)
    here = f'href="/fr/espace-reserve/dossiers/{assigned.reference}/"'
    with translation.override("fr"):
        own = _detail(client, owner, assigned)
        client.logout()
        theirs = _detail(client, professional, assigned)
    for html, eyebrow in ((own, "Votre dossier"), (theirs, "Dossier")):
        panel = _section(html, 'data-now="suspended"')
        assert html.count(reason) == 1 and reason in panel, "the reason drawn once, in the NowPanel"
        assert 'class="file__notice"' not in html
        assert here not in panel, "never a way to the page one is on"
        assert f'<span id="db-now-eyebrow">{eyebrow}</span>' in panel


# ---- M3 · the history's voice; the line a change names ---------------------------------------------------------------
def test_the_history_says_vous_to_the_person_only_and_names_the_line(client, owner, assigned, professional):
    from cases import services
    from cases.models import ChecklistStatus

    passport = assigned.checklist.get(requirement="Passeport en cours de validité")
    services.set_checklist_status(passport, ChecklistStatus.IN_PROGRESS, actor=owner)
    with translation.override("fr"):
        theirs = _section(_detail(client, professional, assigned), 'aria-labelledby="history-title"')
        client.logout()
        own = _section(_detail(client, owner, assigned), 'aria-labelledby="history-title"')
    assert "Vous" not in theirs and '<span class="tl__actor">La personne</span>' in theirs
    assert '<span class="tl__actor">Vous</span>' in own
    assert '<span class="tl__detail" dir="auto">Passeport en cours de validité</span>' in own, "the line it changed"


def test_the_timeline_presenter_says_nobody_is_you_without_a_reader(owner, case):
    from audit.services import record
    from cases.presenters import timeline

    record(action="case.transition", target=case, actor=owner, metadata={"from": "draft", "to": "oriented"})
    with translation.override("fr"):
        assert {row["actor"] for row in timeline(case) if row["actor"]} == {"La personne"}
        assert {row["actor"] for row in timeline(case, reader=owner) if row["actor"]} == {"Vous"}


# ---- M4 · the irreversible closures on the alert dialog --------------------------------------------------------------
@pytest.fixture
def reserved_area_on(db):
    from core.models import SiteSettings

    row = SiteSettings.load()
    row.reserved_area_enabled = True
    row.save()
    return row


@pytest.fixture
def ticket(owner, reserved_area_on):
    from helpdesk import services

    return services.open_ticket(
        owner,
        subject="Validité de mon attestation de langue",
        question="Mon attestation date de dix-huit mois : est-elle encore recevable ?",
    )


def test_closing_a_request_is_one_act_that_opens_the_alert_dialog(client, owner, ticket):
    client.force_login(owner)
    html = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode("utf-8")
    assert PANELS_LINK in html.split("</head>", 1)[0], "the page links the panels where it draws one"
    page = html.split('<dialog class="overlay overlay--dialog overlay--alert" id="desk-close-dialog"', 1)[0]
    assert '<a class="btn btn--secondary" href="#desk-close-dialog" data-overlay-open>Clore la demande</a>' in page
    assert "/cloture/" not in page, "no one-press submit on the page"
    dialog = html.split('id="desk-close-dialog"', 1)[1].split("</dialog>", 1)[0]
    assert 'data-overlay="alert" role="alertdialog"' in dialog and 'aria-describedby="desk-close-text"' in dialog
    assert "Une demande close n’est pas rouverte : une nouvelle demande est ouverte." in dialog
    assert f'action="/fr/espace-reserve/guichet/{ticket.uuid}/cloture/"' in dialog and 'name="close-reason"' in dialog
    assert "data-overlay-close data-overlay-safe>Annuler</button>" in dialog
    assert (
        '<button class="btn btn--danger" type="submit" form="desk-close-form">Clore définitivement</button>' in dialog
    )


def test_a_closed_request_draws_no_closure_and_no_panels(client, owner, ticket):
    from helpdesk import services

    services.close(ticket, actor=owner, reason="")
    client.force_login(owner)
    html = client.get(f"/fr/espace-reserve/guichet/{ticket.uuid}/").content.decode("utf-8")
    assert "desk-close-dialog" not in html and PANELS_LINK not in html


@pytest.fixture
def selection_chain(user_factory, reserved_area_on):
    """An authorisation, its operator, a company and its member, a person whose file is in training, a mandate and the
    process it opens (apps/selection/tests/conftest.py's chain; the demonstration seed is off in tests)."""
    from django.utils import timezone

    from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind
    from cases import services as case_services
    from cases.models import CaseFile, CasePurpose, CaseStatus
    from selection import services

    today = timezone.localdate()
    agency = Organisation.objects.create(name="Agence W3E", kind=OrganisationKind.COMPANY, city="Rovigo")
    company = Organisation.objects.create(name="Entreprise W3E", kind=OrganisationKind.COMPANY, city="Rovigo")
    actor = services.register_actor(
        organisation=agency,
        actor_type="employment_agency",
        jurisdiction="IT-VEN",
        authorisation_reference="TEST-AUT-W3E",
        valid_from=today - dt.timedelta(days=30),
        valid_until=today + dt.timedelta(days=365),
    )
    operator = user_factory(
        "w3e.operator@example.test", role=roles.AUTHORISED_ACTOR, account_type=AccountType.PROFESSIONAL
    )
    services.add_operator(actor, operator, function_note="Responsable du processus")
    member = user_factory("w3e.company@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    Membership.objects.create(user=member, organisation=company, role=MembershipRole.OWNER)
    person = user_factory("w3e.subject@example.test", role=roles.PERSON)
    case = case_services.open_case(person, purpose=CasePurpose.WORK, pathway_key="work.subordinate")
    CaseFile.objects.filter(pk=case.pk).update(status=CaseStatus.TRAINING)
    case.refresh_from_db()
    mandate = services.issue_mandate(
        actor=actor,
        company=company,
        need_profile="Soudeur qualifié",
        need_sector="Métallurgie",
        need_territory="Rovigo",
        need_headcount=2,
        need_competences=[{"label": "Soudure MIG/MAG", "level": "Autonome"}],
    )
    process = services.open_process(mandate=mandate, case=case, operator=operator)
    return process, operator, member


def test_closing_a_selection_process_opens_the_alert_dialog_and_never_preselects_an_outcome(client, selection_chain):
    process, operator, member = selection_chain
    client.force_login(operator)
    html = client.get(f"/fr/espace-reserve/selection/{process.uuid}/").content.decode("utf-8")
    assert PANELS_LINK in html.split("</head>", 1)[0]
    page = html.split('<dialog class="overlay overlay--dialog overlay--alert" id="conclude-dialog"', 1)[0]
    assert 'href="#conclude-dialog" data-overlay-open>Clore le processus</a>' in page
    assert "outcome-select" not in html, "no select of outcomes with the first one chosen"
    dialog = html.split('id="conclude-dialog"', 1)[1].split("</dialog>", 1)[0]
    assert 'role="alertdialog"' in dialog and "Un processus clos ne se rouvre pas." in dialog
    radios = re.findall(r'<input type="radio" id="outcome-[^"]+" name="outcome" value="[^"]+" required>', dialog)
    assert len(radios) >= 2 and "checked" not in dialog
    assert '<button class="btn btn--danger" type="submit" form="conclude-form">Clore le processus</button>' in dialog
    client.force_login(member)
    body = client.get(f"/fr/espace-reserve/selection/{process.uuid}/").content.decode("utf-8")
    assert "conclude-dialog" not in body and PANELS_LINK not in body, "the company acts on nothing here"


# ---- the Academy ----------------------------------------------------------------------------------------------------
def test_a_training_plan_s_state_is_a_chip_through_its_producer_and_its_table_region_is_named_once():
    mine = (TEMPLATES / "academy" / "mine.html").read_text(encoding="utf-8")
    plan = (TEMPLATES / "academy" / "plan_detail.html").read_text(encoding="utf-8")
    assert mine.count('{% chip plan.status "academy.PlanStatus" %}') == 2
    assert '{% chip plan.status "academy.PlanStatus" %}' in plan
    assert 'aria-labelledby="t-plan-gap"' in plan and '<caption class="visually-hidden" id="t-plan-gap">' in plan
    assert 'role="region" aria-labelledby="plan-gap-title"' not in plan, "two landmarks, one name"


# ---- the registers' sheet and the case file's -----------------------------------------------------------------------
def test_a_head_s_acts_take_the_line_on_a_phone():
    phone = _block(_css(PORTAL_V5 / "_registers.css"), "@media (max-width: 47.999rem)")
    rule = re.search(r"\.reg-head \.ws-head__action\s*\{([^}]*)\}", phone)
    assert rule and "flex: 1 1 100%" in rule.group(1) and "min-inline-size: 0" in rule.group(1)


def test_a_line_of_facts_never_ends_or_opens_on_its_point():
    css = _css(PORTAL_V5 / "_registers.css")
    assert ":not(:last-child)::after" not in css, "the point that ended a part's line is gone"
    assert re.search(r"\.reg-row__meta,\s*\.reg-step__meta\s*\{[^}]*overflow-x: clip", css)
    assert re.search(r'\.reg-row__meta > \*::before,\s*\.reg-step__meta > \*::before\s*\{[^}]*content: "·"', css)


def test_the_filter_is_one_row_that_scrolls_on_a_phone():
    phone = _block(_css(PORTAL_V5 / "_registers.css"), "@media (max-width: 51.999rem)")
    assert "flex-wrap: nowrap" in phone and "overflow-x: auto" in phone


def test_a_row_link_s_ring_keeps_its_room_under_forced_colours_and_a_sentence_its_measure():
    css = _css(PORTAL_V5 / "_registers.css")
    forced = _block(css, "@media (forced-colors: active)")
    assert re.search(r"\.reg-row \.db-task__title\s*\{\s*margin-block-end: 6px", forced)
    assert re.search(r"\.reg-sec > :is\(\.db-empty, \.sources\)\s*\{\s*max-inline-size: var\(--measure-body\)", css)


def test_the_row_menu_is_the_system_s_icon_control_at_the_row_s_end():
    css = _css(PORTAL_V5 / "_case.css")
    rule = re.search(r"\.db-task__end \.file-row__menu\s*\{([^}]*)\}", css)
    assert rule and "inline-size: var(--btn-h-icon)" in rule.group(1) and "auto" not in rule.group(1)
    phone = _block(css, "@media (max-width: 47.999rem)")
    assert re.search(r"\.file-rows > \.db-task > \.file-row__end\s*\{[^}]*grid-column: 3", phone)


def test_one_dialog_body_for_the_family_s_acts():
    registers = _css(PORTAL_V5 / "_registers.css")
    assert re.search(r"\.reg-dialog\s*\{[^}]*display: grid", registers)
    assert not re.search(r"\.file-dialog\s*\{", _css(PORTAL_V5 / "_case.css")), "drawn once, in the registers' sheet"
    for partial in (
        "cases/partials/line_dialog.html",
        "cases/partials/state_dialog.html",
        "helpdesk/partials/close_dialog.html",
        "selection/partials/conclude_dialog.html",
    ):
        assert "reg-dialog" in (TEMPLATES / partial).read_text(encoding="utf-8"), partial
