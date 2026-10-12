# ruff: noqa: F401, F811 — the imports ARE the fixtures (collected by name), and a local fixture
# legitimately takes an imported fixture as an argument
"""
Fixtures of the Academy test-suite.

The shared project fixtures live in ``tests/conftest.py``, which is not a root conftest and is not
visible from an app package, so they are re-exported here as the other app suites do.

The local fixtures build the smallest world each test needs. Note what ``person`` deliberately has
NOT got: no case file, no company, no membership, no selection, no training plan. That is the
point — the acceptance criterion of this vertical is that such an account reaches the Academy and
enrols, and a fixture that quietly granted it something would hide a regression.
"""

from __future__ import annotations

import pytest

from academy.models import (
    Competence,
    CompetenceArea,
    CompetenceLevel,
    Course,
    CourseCompetence,
    CourseFormat,
    CourseModule,
    CourseStatus,
    CourseType,
    ProviderKind,
    TrainingProvider,
)
from accounts import roles
from tests.conftest import (
    _clear_caches,
    before_phase3,
    legal_published,
    person_user,
    phase3_open,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)


@pytest.fixture
def provider(db):
    return TrainingProvider.objects.create(
        slug="organisme-test",
        name="Organisme de formation (test)",
        kind=ProviderKind.TRAINING_BODY,
        country="Italie",
        city="Rovigo",
        note="Organisme fictif — données de test.",
    )


def _make_course(provider, *, slug="cours-test", status=CourseStatus.PUBLISHED, modules=3, **extra):
    course = Course.objects.create(
        slug=slug,
        title=extra.pop("title", "Cours de test"),
        summary="Un cours utilisé par les tests.",
        description="Description de test.",
        course_type=extra.pop("course_type", CourseType.ITALIAN_LANGUAGE),
        provider=provider,
        language=extra.pop("language", "it"),
        course_format=CourseFormat.ONLINE,
        duration_hours=extra.pop("duration_hours", 10),
        status=status,
        **extra,
    )
    for order in range(1, modules + 1):
        CourseModule.objects.create(course=course, order=order, title=f"Module {order}", duration_minutes=60)
    return course


@pytest.fixture
def course_factory(db):
    return _make_course


@pytest.fixture
def course(provider):
    return _make_course(provider)


@pytest.fixture
def draft_course(provider):
    return _make_course(provider, slug="cours-brouillon", status=CourseStatus.DRAFT, title="Cours en préparation")


@pytest.fixture
def person(user_factory):
    """A plain person: an account, a role, and nothing else whatsoever."""
    return user_factory("apprenant@example.test", role=roles.PERSON)


@pytest.fixture
def other_person(user_factory):
    return user_factory("autre@example.test", role=roles.PERSON)


@pytest.fixture
def professional(user_factory):
    return user_factory("pro@example.test", role=roles.PROFESSIONAL)


@pytest.fixture
def admin_user(user_factory):
    return user_factory("administration@example.test", role=roles.ADMINISTRATOR)


@pytest.fixture
def competence(db):
    return Competence.objects.create(
        code="comprendre-test",
        label="Comprendre une consigne simple",
        area=CompetenceArea.LANGUAGE,
    )


@pytest.fixture
def course_with_competence(course, competence):
    CourseCompetence.objects.create(
        course=course,
        competence=competence,
        level_reached=CompetenceLevel.BASIC,
        expected_outcome="Comprendre une consigne simple et y répondre.",
    )
    return course


@pytest.fixture
def academy_seeded(db):
    """
    Run the Academy's OWN seeds, and only those.

    The shared ``seeded`` fixture runs ``seed_all`` — every app's seed, in order — which makes a
    test of the Academy catalogue fail whenever any other lane's seed is momentarily broken (it
    was, on 21 September 2026: an unmigrated model in another app raised UndefinedTable and errored
    these two tests). A test that reads the seeded Academy catalogue should depend on the seeded
    Academy catalogue and on nothing else, so it says what it means and fails for its own reasons.
    """
    from django.core.management import call_command

    call_command("seed_all", "--only", "academy", verbosity=0)
