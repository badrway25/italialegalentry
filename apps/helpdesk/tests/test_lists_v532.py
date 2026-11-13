"""
V5.32 lane E — the help desk's three registers on the platform's list toolkit (helpdesk.lists; the coordinator's
PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026): search, the
state the chip says, the period, the orders, the drawer, the chips, the count and the toolkit's no-result answer —
each register narrowing only what its service already scoped, and the dispatch register's search never reaching a
request's words.
"""

from __future__ import annotations

import pytest

from helpdesk import lists, services
from helpdesk.models import TicketOrigin, TicketStatus

pytestmark = pytest.mark.django_db

GUICHET = "/fr/espace-reserve/guichet/"
DISPATCH = "/fr/espace-reserve/guichet/designation/"


def _open(person, subject, **extra):
    return services.open_ticket(person, subject=subject, question="Une question écrite par la personne.", **extra)


@pytest.fixture
def two_requests(person_user):
    first = _open(person_user, "Validité de mon attestation de langue")
    second = _open(person_user, "Traduction de mon acte de naissance")
    services.request_professional_review(second, actor=person_user)
    return first, second


def _page(client, user, path):
    client.force_login(user)
    response = client.get(path)
    assert response.status_code == 200
    return response.content.decode()


def test_one_request_draws_no_toolkit_and_two_draw_it(client, reserved_area_on, person_user):
    _open(person_user, "Validité de mon attestation de langue")
    html = _page(client, person_user, GUICHET)
    assert 'class="lst__bar"' not in html and "js/dist/listing.js" not in html
    _open(person_user, "Traduction de mon acte de naissance")
    html = _page(client, person_user, GUICHET)
    assert 'class="lst__bar"' in html and 'id="lst-guichet-filters"' in html
    assert "css/dist/portal/listing.css" in html and "js/dist/listing.js" in html


def test_the_search_narrows_the_persons_own_requests_and_the_band_still_counts_them_all(
    client, reserved_area_on, person_user, other_person, two_requests
):
    _open(other_person, "Validité d’une autre attestation")
    html = _page(client, person_user, GUICHET + "?q=attestation")
    assert "Validité de mon attestation de langue" in html
    assert "Traduction de mon acte de naissance" not in html
    assert "Validité d’une autre attestation" not in html, "never somebody else's request"
    band = html.split('class="db-ledger reg-band"', 1)[1].split("</div>", 1)[0]
    assert "2 demandes en cours." in band, "the band counts every open request of the person, not the narrowed ones"
    assert "Votre recherche" in html and "attestation" in html


def test_the_state_is_the_one_the_chip_says(client, reserved_area_on, person_user, two_requests):
    html = _page(client, person_user, GUICHET + "?etat=" + TicketStatus.PROFESSIONAL_REVIEW_REQUIRED)
    assert "Traduction de mon acte de naissance" in html
    assert "Validité de mon attestation de langue" not in html
    state = lists.REQUESTS.read({"etat": TicketStatus.PROFESSIONAL_REVIEW_REQUIRED})
    rows = lists.REQUESTS.apply(list(services.tickets_for(person_user)), state)
    assert {ticket.effective_status for ticket in rows} == {TicketStatus.PROFESSIONAL_REVIEW_REQUIRED}


def test_nothing_matching_is_the_toolkits_answer_never_the_empty_register(
    client, reserved_area_on, person_user, two_requests
):
    html = _page(client, person_user, GUICHET + "?q=introuvable")
    assert 'class="lst-empty"' in html and "Aucun résultat" in html
    assert "Vous n’avez encore adressé aucune demande au guichet." not in html


def test_a_crafted_value_is_ignored_and_never_printed(client, reserved_area_on, person_user, two_requests):
    html = _page(client, person_user, GUICHET + "?etat=granted&tri=%3Cscript%3E")
    # the page's own words (the head's hreflang alternates carry the address as it was asked, encoded and escaped —
    # base.html's, not the list's)
    main = html.split("<main", 1)[1].split("</main>", 1)[0]
    assert "Validité de mon attestation de langue" in main and "Traduction de mon acte de naissance" in main
    assert "granted" not in main and "<script>" not in main and "%3Cscript%3E" not in main
    assert 'class="lst__chips"' not in main, "an ignored value narrows nothing and draws no chip"


def test_the_dispatch_search_reaches_the_references_never_the_request_s_words(
    client, reserved_area_on, person_user, operator
):
    first = _open(person_user, "Validité de mon attestation de langue", origin=TicketOrigin.PERSON)
    second = _open(person_user, "Traduction de mon acte de naissance", language="ar")
    for ticket in (first, second):
        services.request_professional_review(ticket, actor=person_user)
    html = _page(client, operator, DISPATCH + "?q=" + first.reference)
    assert first.reference in html and second.reference not in html
    html = _page(client, operator, DISPATCH + "?q=attestation")
    assert 'class="lst-empty"' in html, "a word of the question finds nothing: the search reads references only"
    html = _page(client, operator, DISPATCH + "?langue=ar")
    assert second.reference in html and first.reference not in html


def test_the_dispatch_spec_narrows_the_operators_queue_and_nothing_else(reserved_area_on, person_user, operator):
    first = _open(person_user, "Validité de mon attestation de langue")
    second = _open(person_user, "Traduction de mon acte de naissance")
    for ticket in (first, second):
        services.request_professional_review(ticket, actor=person_user)
    state = lists.DISPATCH.read({"q": first.reference})
    narrowed = list(lists.DISPATCH.apply(services.dispatch_queue(operator), state))
    assert [ticket.uuid for ticket in narrowed] == [first.uuid]


def test_a_mandate_form_that_came_back_with_an_error_stays_in_view_whatever_the_narrowing(
    client, reserved_area_on, person_user, operator
):
    first = _open(person_user, "Validité de mon attestation de langue")
    second = _open(person_user, "Traduction de mon acte de naissance")
    for ticket in (first, second):
        services.request_professional_review(ticket, actor=person_user)
    client.force_login(operator)
    response = client.post(DISPATCH + "?q=" + second.reference, {"ticket": str(first.uuid)})
    assert response.status_code == 200, "an incomplete mandate is answered on the page, never redirected away"
    html = response.content.decode()
    assert "Le mandat est incomplet" in html
    assert first.reference in html, "the request whose form came back stays in view, though the search would hide it"
    assert second.reference in html
    assert '<p class="lst__found" role="status">1 résultat</p>' in html, "the count says what the search found"


def test_every_lookup_is_whitelisted():
    for spec in (lists.REQUESTS, lists.QUEUE, lists.DISPATCH):
        keys = {f.key for f in spec.filters}
        assert keys <= {"etat", "origine", "langue"}, spec.name
        assert {"q", "tri", "page"}.isdisjoint(keys)
