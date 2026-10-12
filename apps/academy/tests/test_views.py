"""
The HTTP layer: authentication, methods, redirects, and what each page actually renders.

Three properties are held here that no service test can hold:

* every route refuses an anonymous visitor by sending them to the login page, GET or POST;
* every mutation is POST-only and CSRF-protected — a state change must not be reachable by
  following a link, or a crafted image tag could enrol somebody;
* a page a user may not read answers the same way whether or not the object exists.
"""

from __future__ import annotations

import pytest
from django.urls import reverse
from django.utils import timezone

from academy import services
from academy.models import Enrolment, EnrolmentStatus

pytestmark = [pytest.mark.django_db, pytest.mark.urls("academy.tests.urls")]


def test_every_route_sends_an_anonymous_visitor_to_the_login_page(client, course):
    enrolment_uuid = "00000000-0000-0000-0000-000000000000"
    routes = [
        ("get", reverse("academy:catalogue")),
        ("get", reverse("academy:course", args=[course.slug])),
        ("post", reverse("academy:enrol", args=[course.slug])),
        ("get", reverse("academy:mine")),
        ("get", reverse("academy:enrolment", args=[enrolment_uuid])),
        ("post", reverse("academy:withdraw", args=[enrolment_uuid])),
        ("get", reverse("academy:plan", args=[enrolment_uuid])),
    ]
    for method, path in routes:
        response = getattr(client, method)(path)
        assert response.status_code == 302, path
        assert "/compte/" in response["Location"] or "login" in response["Location"], path


def test_enrolling_is_not_reachable_by_a_link(client, person, course):
    client.force_login(person)
    response = client.get(reverse("academy:enrol", args=[course.slug]))
    assert response.status_code == 405
    assert Enrolment.objects.count() == 0


def test_the_catalogue_filters_by_domain(client, person, course, course_factory, provider):
    from academy.models import CourseType

    course_factory(provider, slug="securite", title="Sécurité", course_type=CourseType.WORKPLACE_SAFETY)
    client.force_login(person)

    response = client.get(reverse("academy:catalogue"), {"domaine": CourseType.WORKPLACE_SAFETY})
    body = response.content.decode()
    assert response.status_code == 200
    assert "Sécurité" in body
    assert course.title not in body


def test_a_person_cannot_open_a_draft_course(client, person, draft_course):
    client.force_login(person)
    response = client.get(reverse("academy:course", args=[draft_course.slug]))
    assert response.status_code == 403


def test_a_missing_course_answers_exactly_like_a_forbidden_one(client, person, draft_course):
    client.force_login(person)
    forbidden = client.get(reverse("academy:course", args=[draft_course.slug]))
    absent = client.get(reverse("academy:course", args=["ce-cours-nexiste-pas"]))
    assert forbidden.status_code == absent.status_code == 403


def test_my_trainings_lists_only_my_own(client, person, other_person, course):
    services.enrol(other_person, course)
    client.force_login(person)
    response = client.get(reverse("academy:mine"))
    body = response.content.decode()
    assert response.status_code == 200
    assert other_person.email not in body
    assert "Vous ne suivez aucune formation" in body


def test_the_enrolment_page_shows_the_next_module_only(client, person, course):
    enrolment = services.enrol(person, course)
    client.force_login(person)
    response = client.get(reverse("academy:enrolment", args=[enrolment.uuid]))
    body = response.content.decode()
    assert response.status_code == 200
    # One control, for the first module not yet attended — not one per row.
    assert body.count("J’ai suivi ce module") == 1


def test_attending_the_last_module_renders_the_record_of_attendance(client, person, course):
    enrolment = services.enrol(person, course)
    client.force_login(person)
    for module in course.modules.all():
        client.post(reverse("academy:attend", args=[enrolment.uuid, module.pk]))

    response = client.get(reverse("academy:enrolment", args=[enrolment.uuid]))
    body = response.content.decode()
    enrolment.refresh_from_db()
    assert "Attestation de participation" in body
    assert enrolment.attendance_reference in body
    # The caveat travels with the record and cannot be separated from it.
    assert "pas un titre" in body


def test_a_person_cannot_record_attendance_on_someone_elses_enrolment(client, person, other_person, course):
    enrolment = services.enrol(other_person, course)
    client.force_login(person)
    response = client.post(reverse("academy:attend", args=[enrolment.uuid, course.modules.first().pk]))
    assert response.status_code == 403
    assert enrolment.attendances.count() == 0


def test_interrupting_and_resuming_from_the_page(client, person, course):
    enrolment = services.enrol(person, course)
    client.force_login(person)

    client.post(reverse("academy:withdraw", args=[enrolment.uuid]))
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.WITHDRAWN

    client.post(reverse("academy:resume", args=[enrolment.uuid]))
    enrolment.refresh_from_db()
    assert enrolment.status == EnrolmentStatus.ENROLLED


def test_the_plan_page_shows_the_gap_table_without_a_percentage(client, person, course, competence):
    from academy.models import CompetenceLevel

    plan = services.create_plan(person, title="Parcours conseillé")
    services.add_plan_item(plan, course, rationale="Cœur du besoin")
    services.add_gap_line(
        plan,
        competence,
        required_level=CompetenceLevel.INTERMEDIATE,
        current_level=CompetenceLevel.NONE,
        course=course,
        expected_outcome="Comprendre une consigne simple.",
    )
    client.force_login(person)
    response = client.get(reverse("academy:plan", args=[plan.uuid]))
    body = response.content.decode()
    assert response.status_code == 200
    assert "Niveau requis" in body and "Niveau actuel" in body and "Écart" in body
    assert "Compétence à acquérir" in body
    assert "jamais une condition d’accès" in body


def test_a_plan_of_another_person_answers_forbidden(client, person, other_person):
    plan = services.create_plan(other_person, title="Parcours d’un tiers")
    client.force_login(person)
    response = client.get(reverse("academy:plan", args=[plan.uuid]))
    assert response.status_code == 403


def test_the_academy_renders_inside_the_platform_shell(client, person, course):
    client.force_login(person)
    body = client.get(reverse("academy:catalogue")).content.decode()
    assert "portal-bar" in body  # the platform chrome, not the public header
    assert "portal/portal.css" in body
    assert "academy/academy.css" in body
    assert 'name="robots"' in body  # noindex on every authenticated page


def test_the_pages_carry_no_forbidden_design_devices(client, person, course):
    """
    The design rules of this build, checked on the rendered page rather than on the stylesheet.

    A KPI grid, a card, a dashed empty state and a percentage meter are all forbidden by the brief;
    the register language replaces them. The empty region is `.empty` — one hairline and one
    sentence — and never `.empty-state`, the dashed box with a centred icon it replaces.
    """
    client.force_login(person)
    for path in (reverse("academy:catalogue"), reverse("academy:mine")):
        body = client.get(path).content.decode()
        assert "empty-state" not in body
        assert "portal-card" not in body
        assert "progress" not in body.lower().replace("progression", "")


def test_every_academy_response_says_do_not_index_in_the_header(client, person, course):
    """
    The meta tag covers a rendered body; the header covers what it cannot.

    An enrolment and an attendance answer 302, and a redirect has no body to carry a meta tag. The
    platform shell already sets this header on every reserved-area response and documents why; the
    Academy must not be the one authenticated area that does not.
    """
    client.force_login(person)
    page = client.get(reverse("academy:catalogue"))
    assert page.headers["X-Robots-Tag"] == "noindex, nofollow"

    redirect = client.post(reverse("academy:enrol", args=[course.slug]))
    assert redirect.status_code == 302
    assert redirect.headers["X-Robots-Tag"] == "noindex, nofollow"

    head = client.head(reverse("academy:mine"))
    assert head.headers["X-Robots-Tag"] == "noindex, nofollow"


def test_a_plan_read_under_a_mandate_is_not_listed_as_the_readers_own(client, person, professional, course):
    """
    A professional reads the plan of the person they follow — under a heading that says so.

    Listing it among « Mes plans de formation » would say something false about whose record it is,
    and the detail page must state the mandate rather than look like the reader's own file.
    """
    import datetime as dt

    from cases import services as case_services
    from cases.models import AssignmentRole, CasePurpose

    case = case_services.open_case(person, purpose=CasePurpose.TRAINING)
    plan = services.create_plan(person, title="Parcours accompagné", case=case)
    case_services.assign(
        case,
        professional,
        role=AssignmentRole.PROFESSIONAL,
        # A live mandate: a year from today in Rome, not a fixed date (2099 was a fuse: red from 2 Jan 2099).
        authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),
    )
    client.force_login(professional)

    body = client.get(reverse("academy:mine")).content.decode()
    assert "Plans que je consulte au titre d’un mandat" in body
    assert case.reference in body
    own_register, mandated_register = body.split("Plans que je consulte au titre d’un mandat")
    assert plan.title not in own_register
    assert plan.title in mandated_register

    detail = client.get(reverse("academy:plan", args=[plan.uuid])).content.decode()
    assert "Ce parcours n’est pas le vôtre" in detail
    # The person's own attendance stays with the person: no enrolment state on a mandated read.
    assert "Suivi en cours" not in detail
