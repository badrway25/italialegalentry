"""
V5.32 lane E — «Mes formations» on the platform's list toolkit (academy.lists.MINE; the PLATFORM=READY round of the
owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026): the person's own enrolments, narrowed by
the course's words and its domain, the registers drawn from the narrowed rows, the training plans never narrowed.
"""

from __future__ import annotations

import pytest
from django.urls import reverse

from academy import lists, services
from academy.models import CourseType

pytestmark = pytest.mark.django_db


@pytest.fixture
def two_enrolments(person, provider, course_factory):
    italian = course_factory(provider, slug="italien-a2", title="Italien pour le travail")
    civic = course_factory(
        provider, slug="civique", title="Institutions et vie quotidienne", course_type=CourseType.CIVIC_EDUCATION
    )
    return services.enrol(person, italian), services.enrol(person, civic)


def _html(client, user, query=""):
    client.force_login(user)
    response = client.get(reverse("academy:mine") + query)
    assert response.status_code == 200
    return response.content.decode()


def test_one_enrolment_draws_no_toolkit_and_two_draw_it(client, person, provider, course_factory):
    services.enrol(person, course_factory(provider, slug="un", title="Un seul cours"))
    html = _html(client, person)
    assert 'class="lst__bar"' not in html and "js/dist/listing.js" not in html
    services.enrol(person, course_factory(provider, slug="deux", title="Un second cours"))
    html = _html(client, person)
    assert 'class="lst__bar"' in html and "js/dist/listing.js" in html and "css/dist/portal/listing.css" in html


def test_the_search_and_the_domain_narrow_the_persons_own_enrolments(
    client, person, other_person, provider, course_factory, two_enrolments
):
    services.enrol(other_person, course_factory(provider, slug="autre", title="Italien pour un autre"))
    html = _html(client, person, "?q=italien")
    assert "Italien pour le travail" in html and "Institutions et vie quotidienne" not in html
    assert "Italien pour un autre" not in html, "never somebody else's enrolment"
    html = _html(client, person, "?domaine=" + CourseType.CIVIC_EDUCATION)
    assert "Institutions et vie quotidienne" in html and "Italien pour le travail" not in html


def test_nothing_matching_is_the_toolkits_answer_and_the_empty_registers_step_aside(client, person, two_enrolments):
    html = _html(client, person, "?q=introuvable")
    assert 'class="lst-empty"' in html and "Aucun résultat" in html
    assert 'id="mine-ongoing-title"' not in html and 'id="mine-done-title"' not in html
    assert 'id="mine-plans-title"' in html, "the training plans are their own register, never narrowed"


def test_the_domain_offered_are_the_persons_own(person, two_enrolments):
    scoped = services.enrolments_for(person).filter(person=person)
    state = lists.MINE.read({})
    fields = lists.MINE.context(state, scoped=scoped, count=2, total=2, path="/")["fields"]
    offered = {option["value"] for field in fields for option in field["options"]}
    assert offered == {CourseType.ITALIAN_LANGUAGE, CourseType.CIVIC_EDUCATION}
