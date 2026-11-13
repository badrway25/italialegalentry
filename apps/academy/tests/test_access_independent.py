"""
THE acceptance criterion of this vertical, from the client's Technical Blueprint §17:

    «Una persona può accedere all'Academy senza essere selezionata da un'impresa.»

CONFLICT_REGISTER CR-14 resolves the apparent contradiction with the sources that tie training to
company needs: those describe how the CATALOGUE IS BUILT, this describes WHO MAY ENTER IT. The
tests below hold the second half of that decision.

The account under test is deliberately bare: one user, one role, and nothing else. No company, no
membership, no case file, no assignment, no selection, no training plan, no verification. If any
of those ever becomes necessary to reach a course, one of these tests fails.
"""

from __future__ import annotations

import pytest
from django.test import override_settings
from django.urls import reverse

from academy import services
from academy.models import Enrolment, EnrolmentStatus
from accounts.models import Membership
from cases.models import CaseAssignment, CaseFile

pytestmark = pytest.mark.django_db

URLCONF = "academy.tests.urls"


def test_person_has_nothing_but_an_account(person):
    """The premise of every test in this file: the fixture grants nothing beyond authentication."""
    assert CaseFile.objects.filter(person=person).count() == 0
    assert CaseAssignment.objects.filter(assignee=person).count() == 0
    assert Membership.objects.filter(user=person).count() == 0
    assert person.training_plans.count() == 0


def test_a_person_enrols_without_being_selected_by_a_company(person, course):
    """The criterion itself, at the level of the domain: person + course, nothing else."""
    enrolment = services.enrol(person, course)

    assert enrolment.pk is not None
    assert enrolment.person_id == person.id
    assert enrolment.status == EnrolmentStatus.ENROLLED
    assert enrolment.plan is None


def test_the_enrolment_service_cannot_be_given_a_company_or_a_selection(person, course):
    """
    A signature is a guarantee: what cannot be passed cannot be required.

    This is the test that keeps the criterion true as the code grows — the day someone adds a
    ``company=`` or ``selection=`` parameter to make enrolment conditional, it fails here rather
    than in a review six months later.
    """
    import inspect

    parameters = set(inspect.signature(services.enrol).parameters)
    assert parameters == {"person", "course", "plan", "request"}
    forbidden = {"company", "selection", "employer", "need", "case", "sponsor", "invitation"}
    assert parameters & forbidden == set()


@override_settings(ROOT_URLCONF=URLCONF)
def test_a_person_walks_the_whole_academy_in_the_browser(client, person, course):
    """End to end through the HTTP layer: catalogue → course → enrolment → every module → record."""
    client.force_login(person)

    catalogue = client.get(reverse("academy:catalogue"))
    assert catalogue.status_code == 200
    assert course.title in catalogue.content.decode()

    detail = client.get(reverse("academy:course", args=[course.slug]))
    assert detail.status_code == 200

    enrol = client.post(reverse("academy:enrol", args=[course.slug]))
    assert enrol.status_code == 302
    enrolment = Enrolment.objects.get(person=person, course=course)

    for module in course.modules.all():
        response = client.post(reverse("academy:attend", args=[enrolment.uuid, module.pk]))
        assert response.status_code == 302

    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.COMPLETED
    assert enrolment.attendance_reference != ""

    page = client.get(reverse("academy:enrolment", args=[enrolment.uuid]))
    body = page.content.decode()
    assert page.status_code == 200
    assert enrolment.attendance_reference in body


@override_settings(ROOT_URLCONF=URLCONF)
def test_the_catalogue_never_asks_who_selected_you(client, person, course):
    """
    No recruitment vocabulary, and no vocabulary of administrative approval, on the way in.

    CR-03 and CR-04 forbid the first; CR-11 and REQ-EDU-05 forbid the second. A person reading the
    catalogue must not be able to believe that a company chose them or that the State approved
    anything.
    """
    client.force_login(person)
    pages = [
        client.get(reverse("academy:catalogue")),
        client.get(reverse("academy:course", args=[course.slug])),
    ]
    forbidden = (
        "candidat",
        "recrut",
        "matching",
        "postuler",
        "offre d’emploi",
        "offre d'emploi",
        "sélectionné",
        "éligible",
        "approuvé",
        "agréé par l’état",
        "diplôme reconnu",
    )
    for response in pages:
        text = response.content.decode().lower()
        for word in forbidden:
            assert word not in text, f"forbidden wording {word!r} rendered by {response.request['PATH_INFO']}"
