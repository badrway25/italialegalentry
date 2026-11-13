"""
V5.32 lane E — the PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov
2026: «Mes demandes», «Mes échéances» and the register's loose files (`/documents/`) on the platform's list toolkit,
and the console's ONE empty state (portal/partials/empty.html) on the pages that hold nothing yet.
"""

from __future__ import annotations

import pytest

from portal import lists, services
from portal.models import DeadlineKind, DeadlineStatus

pytestmark = pytest.mark.django_db

REQUESTS = "/fr/espace-reserve/mes-demandes/"
DEADLINES = "/fr/espace-reserve/mes-echeances/"
MESSAGES = "/fr/espace-reserve/communications/"
# RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the V5.32
# integration review's P2-11 — /documents/ now leads to «Mes documents», where the loose files are listed among the
# account's files (portal.lists.FILES — the same search, type, period and orders the loose files had), their «Supprimer»
# with them
REGISTER = "/fr/espace-reserve/mes-documents/"
CALM = '<div class="org-calm reg-calm" role="status" data-spot>'


def _html(client, user, path):
    client.force_login(user)
    response = client.get(path)
    assert response.status_code == 200, path
    return response.content.decode()


# ---- «Mes demandes» -------------------------------------------------------------------------------------------------
def test_the_requests_narrow_by_kind_state_and_words_never_beyond_the_account(
    client, seeded, alice, bob, make_company_request, make_contact_request
):
    make_company_request(alice, company_name="Atelier Alpha")
    make_contact_request(alice, subject="Question sur le Forum")
    make_contact_request(bob, subject="Question de Bob")
    html = _html(client, alice, REQUESTS)
    assert 'class="lst__bar"' in html and 'id="lst-demandes-filters"' in html
    html = _html(client, alice, REQUESTS + "?type=contact")
    assert "Question sur le Forum" in html and "Atelier Alpha" not in html and "Question de Bob" not in html
    html = _html(client, alice, REQUESTS + "?q=alpha")
    assert "Atelier Alpha" in html and "Question sur le Forum" not in html
    band = html.split('class="db-ledger reg-band"', 1)[1].split("</div>", 1)[0]
    assert ">2<" in band, "the band counts the account's requests, not the narrowed ones"
    html = _html(client, alice, REQUESTS + "?q=introuvable")
    assert 'class="lst-empty"' in html and CALM not in html, "nothing matching is the toolkit's answer"


def test_the_requests_state_choices_are_the_two_registers_words():
    values = [value for value, _label in lists._request_states()]
    assert len(values) == len(set(values)), "a form's state and a registration's never share a value"


# ---- «Mes échéances» ------------------------------------------------------------------------------------------------
def test_the_deadlines_narrow_and_the_band_keeps_counting_every_date(client, alice, make_deadline):
    make_deadline(alice, title="Rendez-vous au consulat", days=-3)
    make_deadline(alice, title="Dépôt du dossier", days=12)
    make_deadline(alice, title="Session de formation", days=20, kind=DeadlineKind.TRAINING)
    html = _html(client, alice, DEADLINES + "?type=" + DeadlineKind.TRAINING)
    assert "Session de formation" in html and "Dépôt du dossier" not in html
    context = services.deadlines_page(alice, narrow=lambda rows: rows.filter(kind=DeadlineKind.TRAINING))
    assert context["deadlines_total"] == 3 and context["overdue_count"] == 1 and context["ahead_count"] == 2
    html = _html(client, alice, DEADLINES + "?q=introuvable")
    assert 'class="lst-empty"' in html and "Aucun résultat" in html


def test_a_narrowing_that_empties_a_section_sets_it_aside(client, alice, make_deadline):
    make_deadline(alice, title="Dépôt du dossier", days=12)
    make_deadline(alice, title="Ancien rendez-vous", days=-30, status=DeadlineStatus.DONE)
    html = _html(client, alice, DEADLINES + "?etat=" + DeadlineStatus.DONE)
    assert "Ancien rendez-vous" in html and 'id="deadlines-open-title"' not in html
    html = _html(client, alice, DEADLINES)
    assert 'id="deadlines-open-title"' in html and 'id="deadlines-closed-title"' in html


def test_dates_none_ahead_say_so_in_the_section_s_sentence(client, alice, make_deadline):
    make_deadline(alice, title="Ancien rendez-vous", days=-30, status=DeadlineStatus.DONE)
    html = _html(client, alice, DEADLINES)
    section = html.split('id="deadlines-open-title"', 1)[1].split("</section>", 1)[0]
    assert '<p class="db-empty">' in section and CALM not in html


# ---- the console's one empty state ----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("path", "words"),
    [
        (REQUESTS, "Aucune demande"),
        (DEADLINES, "Aucune échéance"),
        (MESSAGES, "Aucune communication"),
        ("/fr/espace-reserve/mon-parcours/", "Aucune pré-évaluation enregistrée"),
    ],
)
def test_a_page_that_holds_nothing_yet_draws_the_platforms_one_empty_state(client, seeded, alice, path, words):
    html = _html(client, alice, path)
    assert html.count(CALM) == 1, path
    panel = html.split(CALM, 1)[1].split("\n  </div>", 1)[0]
    assert '<span class="org-calm__art" aria-hidden="true">' in panel and words in panel
    assert "empty-state" not in html, "the public pages' tile and its doorway arch left the console"
    assert 'class="lst__bar"' not in html, "nothing to narrow: no toolkit"
    assert "css/dist/portal/platform.css" in html, "the panel's sheet"


def test_the_ar_page_says_its_empty_state_in_arabic(client, alice):
    html = _html(client, alice, "/ar/espace-reserve/mes-demandes/")
    panel = html.split(CALM, 1)[1].split("\n  </div>", 1)[0]
    assert "Aucune demande" not in panel and '<p class="org-calm__text">' in panel


# ---- /documents/: the loose files ------------------------------------------------------------------------------------
def test_the_loose_files_narrow_and_page_and_keep_the_registers_filter(client, alice, make_document):
    for n in range(23):
        make_document(alice, name=f"copie-{n:02d}.pdf")
    make_document(alice, name="passeport-scan.pdf")
    html = _html(client, alice, REGISTER)
    assert 'id="lst-files-filters"' in html and "Page 1 sur 2" in html
    html = _html(client, alice, REGISTER + "?q=passeport")
    assert "passeport-scan.pdf" in html and "copie-00.pdf" not in html
    html = _html(client, alice, REGISTER + "?q=passeport&%C3%A9tat=missing")
    assert '<input type="hidden" name="état" value="missing">' in html, "the register's filter rides along"
    html = _html(client, alice, REGISTER + "?q=introuvable")
    assert 'class="lst-empty"' in html


def test_somebody_elses_loose_file_is_never_listed(client, alice, bob, make_document):
    make_document(alice, name="a-moi.pdf")
    make_document(alice, name="a-moi-aussi.pdf")
    make_document(bob, name="a-bob.pdf")
    html = _html(client, alice, REGISTER + "?q=a-")
    assert "a-moi.pdf" in html and "a-bob.pdf" not in html
