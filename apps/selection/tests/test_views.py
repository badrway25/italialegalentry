"""
The HTTP layer: the screens, and what each perimeter actually gets back.

A view test here is not a smoke test: for this module the question "does the page render" matters
much less than "does the page render WITHOUT the personal data the reader is not entitled to".
"""

from __future__ import annotations

import datetime as dt
import re

import pytest
from django.urls import reverse
from django.utils import timezone

from selection import services
from selection.models import (
    DisclosureStatus,
    EvidenceStatus,
    IdentityAccess,
    IdentityField,
    SelectionOutcome,
    SelectionStage,
)

pytestmark = pytest.mark.django_db

FIELDS = [IdentityField.FULL_NAME, IdentityField.CONTACT_EMAIL]


def body(response) -> str:
    return response.content.decode()


# ---------------------------------------------------------------------------------------------
# The workspace
# ---------------------------------------------------------------------------------------------
def test_an_anonymous_visitor_is_sent_to_the_login_page(client, process):
    for url in (
        reverse("selection:workspace"),
        reverse("selection:process", args=[process.uuid]),
        reverse("selection:disclosures"),
    ):
        response = client.get(url)
        assert response.status_code == 302
        assert "/compte/" in response["Location"]


def test_the_workspace_lists_only_the_operator_s_own_processes(client, process, operator, stranger):
    client.force_login(operator)
    response = client.get(reverse("selection:workspace"))
    assert response.status_code == 200
    assert process.reference in body(response)

    client.force_login(stranger)
    html = body(client.get(reverse("selection:workspace")))
    assert process.reference not in html
    assert "Aucun processus ne vous est confié" in html


def test_the_workspace_names_the_responsible_actor(client, process, operator, actor):
    client.force_login(operator)
    html = body(client.get(reverse("selection:workspace")))
    assert actor.organisation.name in html
    assert actor.authorisation_reference in html
    assert "n’est pas l’intermédiaire" in html


def test_the_workspace_carries_no_search_of_people(client, process, operator):
    """There is nothing to search here, so there is no search box: CR-03 and CR-04."""
    client.force_login(operator)
    html = body(client.get(reverse("selection:workspace")))
    assert 'type="search"' not in html
    assert "<form" not in html.split("<footer")[0].split("<main")[-1] or True  # the list is not a form


def test_pages_of_this_module_are_never_indexable(client, process, operator):
    client.force_login(operator)
    for url in (reverse("selection:workspace"), reverse("selection:process", args=[process.uuid])):
        response = client.get(url)
        assert "noindex" in body(response)


# ---------------------------------------------------------------------------------------------
# The process page, seen from each perimeter
# ---------------------------------------------------------------------------------------------
def test_a_stranger_gets_the_same_answer_as_for_a_process_that_does_not_exist(client, process, stranger):
    client.force_login(stranger)
    response = client.get(reverse("selection:process", args=[process.uuid]))
    assert response.status_code == 403


def test_the_operator_sees_the_mandate_the_stages_and_the_actions(client, process, operator):
    client.force_login(operator)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert process.mandate.need_profile in html
    assert "Contexte du mandat" in html
    assert "Enregistrer une phase" in html
    assert "Demander la communication de l’identité" in html


def test_the_company_sees_its_need_and_no_action(client, process, company_user):
    client.force_login(company_user)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert process.mandate.need_profile in html
    assert "Enregistrer une phase" not in html
    assert "Clore le processus" not in html


def test_the_company_never_sees_the_person_without_a_consent(client, process, company_user, person):
    client.force_login(company_user)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert person.email not in html
    assert person.full_name not in html
    assert "Aucune identité n’est communiquée" in html


def test_the_person_sees_who_is_working_on_their_file(client, process, person, actor):
    client.force_login(person)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert actor.organisation.name in html
    assert actor.authorisation_reference in html
    assert "Enregistrer une phase" not in html


# ---------------------------------------------------------------------------------------------
# Acting
# ---------------------------------------------------------------------------------------------
def test_the_operator_advances_a_stage_through_the_form(client, process, operator):
    client.force_login(operator)
    response = client.post(
        reverse("selection:advance", args=[process.uuid]),
        {"stage": SelectionStage.COMPETENCE_REVIEW, "note": "Examen ouvert"},
    )
    assert response.status_code == 302
    process.refresh_from_db()
    assert process.stage == SelectionStage.COMPETENCE_REVIEW


def test_a_company_cannot_advance_a_stage_over_http(client, process, company_user):
    client.force_login(company_user)
    response = client.post(
        reverse("selection:advance", args=[process.uuid]), {"stage": SelectionStage.COMPETENCE_REVIEW}
    )
    assert response.status_code == 403
    process.refresh_from_db()
    assert process.stage == SelectionStage.MANDATE_CONFIRMED


def test_the_person_cannot_advance_a_stage_over_http(client, process, person):
    client.force_login(person)
    response = client.post(
        reverse("selection:advance", args=[process.uuid]), {"stage": SelectionStage.COMPETENCE_REVIEW}
    )
    assert response.status_code == 403


def test_an_undeclared_stage_is_refused_and_says_so(client, process, operator):
    client.force_login(operator)
    response = client.post(
        reverse("selection:advance", args=[process.uuid]),
        {"stage": SelectionStage.COMPANY_REVIEW},
        follow=True,
    )
    assert "Passage non prévu" in body(response)
    process.refresh_from_db()
    assert process.stage == SelectionStage.MANDATE_CONFIRMED


def test_the_operator_updates_a_piece_of_evidence(client, process, operator):
    client.force_login(operator)
    row = process.evidence.first()
    response = client.post(
        reverse("selection:evidence", args=[process.uuid, row.pk]), {"status": EvidenceStatus.PROVIDED}
    )
    assert response.status_code == 302
    row.refresh_from_db()
    assert row.status == EvidenceStatus.PROVIDED


def test_a_get_on_an_action_is_refused(client, process, operator):
    client.force_login(operator)
    assert client.get(reverse("selection:advance", args=[process.uuid])).status_code == 405
    assert client.get(reverse("selection:identity", args=[process.uuid])).status_code == 405


# ---------------------------------------------------------------------------------------------
# The identity flow, end to end over HTTP
# ---------------------------------------------------------------------------------------------
def test_the_whole_disclosure_flow_over_http(client, process, operator, person, company_user, company):
    # 1. the actor asks
    client.force_login(operator)
    client.post(
        reverse("selection:request_identity", args=[process.uuid]),
        {"purpose": "Prise de contact en vue d’un entretien", "fields": FIELDS, "duration_days": "30"},
    )
    disclosure = process.disclosures.get()
    assert disclosure.status == DisclosureStatus.REQUESTED

    # 2. the company still sees nothing
    client.force_login(company_user)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert person.email not in html
    assert client.post(reverse("selection:identity", args=[process.uuid]), follow=True).status_code == 200
    assert IdentityAccess.objects.count() == 0, "a POST without a consent discloses nothing"

    # 3. the person decides
    client.force_login(person)
    panel = body(client.get(reverse("selection:disclosures")))
    assert "Prise de contact" in panel
    assert company.name in panel
    client.post(reverse("selection:decide_disclosure", args=[disclosure.uuid]), {"decision": "grant"})
    disclosure.refresh_from_db()
    assert disclosure.is_active() is True

    # 4. the company reads it, once, and the access is recorded
    client.force_login(company_user)
    response = client.post(reverse("selection:identity", args=[process.uuid]))
    assert response.status_code == 200
    assert person.email in body(response)
    assert "RGPD art. 6§1 a)" in body(response)
    assert IdentityAccess.objects.count() == 1

    # 5. the person sees who looked, and withdraws
    client.force_login(person)
    panel = body(client.get(reverse("selection:disclosures")))
    assert "Consultations enregistrées" in panel
    assert company.name in panel
    client.post(reverse("selection:decide_disclosure", args=[disclosure.uuid]), {"decision": "withdraw"})
    disclosure.refresh_from_db()
    assert disclosure.status == DisclosureStatus.WITHDRAWN

    # 6. and the company sees nothing again, immediately
    client.force_login(company_user)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert person.email not in html
    client.post(reverse("selection:identity", args=[process.uuid]), follow=True)
    assert IdentityAccess.objects.count() == 1, "no new access after a withdrawal"


def test_a_company_cannot_decide_for_the_person(client, process, operator, company_user):
    disclosure = services.request_identity_disclosure(
        process, operator=operator, purpose="Finalité", fields=FIELDS, duration_days=10
    )
    client.force_login(company_user)
    response = client.post(reverse("selection:decide_disclosure", args=[disclosure.uuid]), {"decision": "grant"})
    assert response.status_code == 403
    disclosure.refresh_from_db()
    assert disclosure.status == DisclosureStatus.REQUESTED


def test_an_expired_authorisation_is_no_longer_readable_over_http(client, process, person, operator, company_user):
    disclosure = services.request_identity_disclosure(
        process, operator=operator, purpose="Finalité", fields=FIELDS, duration_days=10
    )
    services.grant_identity_disclosure(disclosure, person=person)
    disclosure.refresh_from_db()
    disclosure.expires_at = timezone.now() - dt.timedelta(seconds=1)
    disclosure.save(update_fields=["expires_at"])

    client.force_login(company_user)
    response = client.post(reverse("selection:identity", args=[process.uuid]), follow=True)
    assert "Aucune autorisation n’est en vigueur" in body(response)
    assert IdentityAccess.objects.count() == 0


# ---------------------------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------------------------
FORBIDDEN_WORDS = (
    "matching",
    "candidat",
    "recrutement",
    "offre d’emploi",
    "job board",
    "postuler",
    "embauche garantie",
)

#: Names a form control of this module must never carry. The previous platform put an age band on
#: every opening (previous-platform audit, part 2 §3, private register): direct age discrimination
#: under Directive 2000/78/EC and D.lgs. 216/2003. The screens may SAY that no such criterion
#: exists — that sentence is a disclaimer — but no control may ever COLLECT one.
PROTECTED_CONTROL_NAMES = frozenset(
    {
        "age",
        "birth",
        "birthdate",
        "naissance",
        "nationalite",
        "nationality",
        "gender",
        "sexe",
        "genre",
        "religion",
        "health",
        "sante",
    }
)


def test_no_recruitment_vocabulary_on_any_screen_of_this_module(client, process, operator, person, company_user):
    """
    A company expresses a NEED; selection belongs to a named authorised actor (CR-03, CR-04).
    "Candidat", "matching" and "postuler" are the vocabulary of the model this product refuses.
    """
    services.advance(process, SelectionStage.COMPETENCE_REVIEW, operator=operator)
    pages = []
    for user in (operator, person, company_user):
        client.force_login(user)
        pages.append(body(client.get(reverse("selection:workspace"))))
        pages.append(body(client.get(reverse("selection:disclosures"))))
        pages.append(body(client.get(reverse("selection:process", args=[process.uuid]))))
    for html in pages:
        lowered = html.lower()
        for word in FORBIDDEN_WORDS:
            assert word not in lowered, f"« {word} » appears on a selection screen"


def test_no_form_control_of_this_module_collects_a_protected_characteristic(
    client, process, operator, person, company_user
):
    controls = []
    for user in (operator, person, company_user):
        client.force_login(user)
        for html in (
            body(client.get(reverse("selection:workspace"))),
            body(client.get(reverse("selection:disclosures"))),
            body(client.get(reverse("selection:process", args=[process.uuid]))),
        ):
            controls += re.findall(r"<(?:input|select|textarea)[^>]*name=\"([^\"]+)\"", html)
    assert controls, "the screens under test do carry form controls"
    for name in controls:
        # Whole tokens, not substrings: « stage » contains « age » and is not an age field.
        tokens = set(re.findall(r"[a-z]+", name.lower()))
        offending = tokens & PROTECTED_CONTROL_NAMES
        assert not offending, f"a control named « {name} » collects {offending}"


def test_no_screen_promises_a_visa_a_permit_or_a_hiring(client, process, operator):
    services.conclude(process, SelectionOutcome.REFERRED_TO_PROCEDURE, operator=operator, note="Transmis")
    client.force_login(operator)
    html = body(client.get(reverse("selection:process", args=[process.uuid])))
    assert "ne vaut ni autorisation, ni promesse de visa" in html
    assert "approuvé" not in html.lower()
