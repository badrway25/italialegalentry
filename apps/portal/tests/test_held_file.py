"""
The dashboard of a person whose latest file is SUSPENDED or CLOSED (sec-f7; the W3-D review's «seen on the way»).

Before: ``portal.services.active_case`` keeps the active statuses only, so such a person read «Vous n'avez pas encore
de dossier…» and was offered the questionnaire — a falsehood about a file that exists, and, for a suspended file, an
invitation to open a second one beside it (``cases.intake.case_for_purpose`` reads the active files only). Now the
dashboard draws THAT file: its reference and its state's chip in the head; the NowPanel saying the state as the case
file says it — «Dossier suspendu» and why, or «Parcours clôturé» and that a new file opens with the questionnaire —;
the way to the file; its journey read from its trail, nothing «here». Every word the catalogue's.
"""

from __future__ import annotations

import pytest
from django.urls import reverse
from django.utils import translation

from cases import services as case_services
from cases.models import CasePurpose, CaseStatus
from portal import services

pytestmark = pytest.mark.django_db

REASON = "En attente de la copie du passeport"
#: NOW_NO_CASE's text (portal.services.now_panel), the sentence a held file's owner must never read again.
NO_FILE_YET = (
    "Vous n’avez pas encore de dossier. Il s’en ouvre un lorsque vous terminez le questionnaire d’orientation, et il "
    "conserve alors votre résultat, votre liste de pièces et les personnes responsables de chaque étape."
)
DOOR = '<svg class="doorway db-now__door"'


@pytest.fixture
def case(alice):
    return case_services.open_case(alice, purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _suspended(case, by):
    case_services.transition(case, CaseStatus.ORIENTED)  # the platform's own move (the orientation service)
    case_services.transition(case, CaseStatus.SUSPENDED, actor=by, reason=REASON)
    case.refresh_from_db()
    return case


def _closed(case):
    case_services.transition(case, CaseStatus.ORIENTED)
    case_services.transition(case, CaseStatus.CLOSED, actor=case.person)  # «qualunque → CLOSED: persona»
    case.refresh_from_db()
    return case


def _held(case, state):
    return _suspended(case, case.person) if state == "suspended" else _closed(case)


def test_the_owner_of_a_suspended_file_is_told_it_is_suspended_and_why(alice, case):
    _suspended(case, alice)
    context = services.dashboard_context(alice)
    now = context["now"]
    assert context["case"] == case and context["case_url"].endswith(f"/{case.reference}/")
    assert now["variant"] == services.NOW_SUSPENDED
    assert (str(now["eyebrow"]), str(now["title"]), now["text"]) == ("Votre dossier", "Dossier suspendu", REASON)
    assert now["words"] == {"lang": "", "dir": "auto"}, "the reason is in the words of whoever suspended the file"
    assert str(now["primary"]["label"]) == "Votre dossier" and now["primary"]["url"] == context["case_url"]
    assert now["secondary"] is None, "no questionnaire: it would open a second file beside the suspended one"
    assert context["next_action"] is None
    assert context["journey"] and not any(step["is_current"] for step in context["journey"])


def test_the_owner_of_a_closed_file_is_told_a_new_one_opens_with_the_questionnaire(alice, case):
    _closed(case)
    context = services.dashboard_context(alice)
    now = context["now"]
    assert context["case"] == case
    assert now["variant"] == services.NOW_CLOSED
    assert (str(now["eyebrow"]), str(now["title"])) == ("Votre dossier", "Parcours clôturé")
    assert str(now["text"]) == "Un dossier clôturé ne se rouvre pas : on en ouvre un nouveau."
    assert str(now["primary"]["label"]) == "Commencer le questionnaire" and now["primary"]["url"]
    assert str(now["secondary"]["label"]) == "Votre dossier" and now["secondary"]["url"] == context["case_url"]
    assert context["next_action"] is None


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("state", ["suspended", "closed"])
def test_the_page_draws_the_held_file_and_never_the_empty_state(client, alice, case, state, lang):
    _held(case, state)
    client.force_login(alice)
    response = client.get(f"/{lang}/espace-reserve/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    with translation.override(lang):
        state_label = str(CaseStatus(state).label)
        no_file_yet = translation.gettext(NO_FILE_YET)
        to_the_file = translation.gettext("Votre dossier")
        file_url = reverse("cases:detail", args=[case.reference])
        questionnaire_url = reverse("orientation:start")
    assert f'data-now="{state}"' in html and 'data-now="no-case"' not in html and DOOR not in html
    assert no_file_yet not in html
    head = html.split('<header class="ctx db-head">', 1)[1].split("</header>", 1)[0]
    assert case.reference in head and state_label in head, "the head's chip says the state"
    panel = html.split('class="card card--action db-now', 1)[1].split("</section>", 1)[0]
    assert panel.count("data-now-primary") == 1 and to_the_file in panel
    assert 'aria-current="step"' not in html, "a held file is never «here» on the journey"
    if state == "suspended":
        assert f'href="{file_url}" data-now-primary' in panel and questionnaire_url not in panel
        assert html.count(REASON) == 1, "the reason, drawn once: in the NowPanel"
    else:
        assert f'href="{questionnaire_url}" data-now-primary' in panel and f'href="{file_url}"' in panel


def test_the_closed_files_own_page_asks_nothing_either_and_a_suspended_one_keeps_its_obligations(client, alice, case):
    """One click from the dashboard, the case file must not contradict it: a closed file names no next action
    (``cases.services.next_action``); a suspended file still names what it waits for."""
    case_services.add_checklist_item(case, requirement="Passeport en cours de validité", responsible_actor="person")
    _suspended(case, alice)
    assert case_services.next_action(case).label == "Passeport en cours de validité"
    case_services.transition(case, CaseStatus.CLOSED, actor=alice)
    case.refresh_from_db()
    assert case_services.next_action(case) is None
    client.force_login(alice)
    page = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/")
    assert page.status_code == 200 and page.context["next_action"] is None and page.context["transitions"] == []


def test_an_active_file_still_comes_first(alice, case):
    _closed(case)
    newer = case_services.open_case(alice, purpose=CasePurpose.STUDY)
    context = services.dashboard_context(alice)
    assert context["case"] == newer and context["now"]["variant"] not in (services.NOW_SUSPENDED, services.NOW_CLOSED)


def test_a_suspended_file_comes_before_a_closed_one(alice, case):
    _suspended(case, alice)
    _closed(case_services.open_case(alice, purpose=CasePurpose.STUDY))
    context = services.dashboard_context(alice)
    assert context["case"] == case and context["now"]["variant"] == services.NOW_SUSPENDED


def test_a_person_who_never_had_a_file_still_reads_the_empty_state(alice):
    context = services.dashboard_context(alice)
    assert context["case"] is None and context["now"]["variant"] == services.NOW_NO_CASE


def test_an_overdue_date_does_not_take_a_held_files_panel_over_and_stays_listed(alice, case, make_deadline):
    _suspended(case, alice)
    late = make_deadline(alice, title="Rendez-vous au consulat", days=-3)
    context = services.dashboard_context(alice)
    assert context["now"]["variant"] == services.NOW_SUSPENDED and not context["now"]["takeover"]
    assert [row["pk"] for row in context["deadlines"]] == [late.pk]


def test_somebody_elses_held_file_is_never_drawn(alice, bob):
    """``held_case`` reads through the authorisation queryset, as ``active_case`` does: bob's file is not hers."""
    _closed(case_services.open_case(bob, purpose=CasePurpose.WORK))
    assert services.held_case(alice) is None
    assert services.dashboard_context(alice)["now"]["variant"] == services.NOW_NO_CASE


def test_the_reassessment_still_touches_active_files_only(alice, case):
    _closed(case)
    assert services.active_case(alice) is None
    assert services.reassess_person(alice) is None
