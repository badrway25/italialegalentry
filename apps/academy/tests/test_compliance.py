"""
Compliance of the Academy: what the domain is not allowed to say, hold or imply.

These are not style tests. Each one corresponds to a decision in the source of truth that a future
change could silently undo:

* CR-03 / CR-04 — no recruitment vocabulary anywhere, in any language. A company expresses a NEED;
  selection belongs to a named, answerable authorised actor. The Academy sits outside that entirely.
* CR-11 / REQ-EDU-05 — nothing approves anybody. No "eligible", no "approved", no wording that
  could be read as an administrative decision or a State-recognised qualification.
* Age is never a selection criterion (Directive 2000/78/EC, D.lgs. 216/2003). The previous platform
  carried an age band on every job opening; this one carries no age at all.
* GDPR art. 5 §1 c) and art. 9 — minimise, and never collect special-category data. A training
  record is already sensitive enough without a health field or an origin field beside it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.apps import apps

pytestmark = pytest.mark.django_db

APP_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = APP_DIR.parent.parent / "templates" / "academy"

#: Vocabulary that must never appear in the Academy, in any of the four languages of the platform.
FORBIDDEN_WORDS = (
    # recruitment (CR-03, CR-04)
    "candidature",
    "candidat",
    "recrutement",
    "recruter",
    "matching",
    "postuler",
    "offre d’emploi",
    "offre d'emploi",
    "job board",
    "reclutamento",
    "candidato",
    "selezionato",
    "توظيف",
    # administrative approval (CR-11, REQ-EDU-05)
    "éligible",
    "eleggibile",
    "approuvé",
    "approvato",
    "certifié par l’état",
    "titre reconnu par l’état",
    "diplôme d’état",
    # promises the platform cannot make
    "garantit un emploi",
    "garantit un visa",
    "obtenez votre permis",
)

#: Model field names that would reintroduce a discrimination risk or special-category data.
FORBIDDEN_FIELD_FRAGMENTS = (
    "age",
    "birth",
    "naissance",
    "gender",
    "sexe",
    "nationality",
    "nationalite",
    "religion",
    "health",
    "sante",
    "origin_country",
    "ethnic",
    "disab",
    "handicap",
    "union",
    "score",
    "rating",
    "percent",
)


def _source_files() -> list[Path]:
    files = [path for path in APP_DIR.rglob("*.py") if "migrations" not in path.parts]
    files += list(TEMPLATE_DIR.rglob("*.html"))
    files += list((APP_DIR / "static").rglob("*.css"))
    return files


def test_no_recruitment_or_approval_vocabulary_in_the_source():
    offences = []
    for path in _source_files():
        if path.name.startswith("test_"):
            continue  # this very file lists the forbidden words on purpose
        text = path.read_text(encoding="utf-8").lower()
        offences += [f"{path.name}: {word}" for word in FORBIDDEN_WORDS if word in text]
    assert offences == [], offences


def test_no_academy_model_collects_age_or_special_category_data():
    """
    Read the field names of every model of this app.

    The previous platform attached an age band to each opening, which is direct age discrimination.
    Nothing here may carry an age, a date of birth, a nationality, a health status or a score —
    and a field whose name merely contains one of those fragments fails, because a field that has
    to be named carefully is a field that will be used carelessly.
    """
    offences = []
    for model in apps.get_app_config("academy").get_models():
        for field in model._meta.get_fields():
            name = getattr(field, "name", "").lower()
            for fragment in FORBIDDEN_FIELD_FRAGMENTS:
                if fragment in name and name not in {"language", "text_language", "message"}:
                    offences.append(f"{model.__name__}.{name} contains {fragment!r}")
    assert offences == [], offences


def test_no_percentage_is_ever_rendered_for_progress(client, person, course):
    """
    Progress is counted in modules, never measured in per cent (RB §31).

    The check runs on the RENDERED page, because a percentage that never exists as a model field
    can still be computed in a template.
    """
    from django.urls import reverse

    from academy import services

    enrolment = services.enrol(person, course)
    services.record_attendance(enrolment, course.modules.first())
    client.force_login(person)

    for path in (reverse("academy:mine"), reverse("academy:enrolment", args=[enrolment.uuid])):
        body = client.get(path).content.decode()
        assert re.search(r"\d+\s*%", body) is None, f"a percentage is rendered on {path}"
        assert "<progress" not in body
        assert 'role="progressbar"' not in body


test_no_percentage_is_ever_rendered_for_progress = pytest.mark.urls("academy.tests.urls")(
    test_no_percentage_is_ever_rendered_for_progress
)


def test_the_catalogue_never_states_that_a_course_leads_to_a_right(academy_seeded):
    """
    Read the seeded catalogue itself: descriptions are content, and content drifts.

    Every seeded course must avoid promising an outcome. The seed is the only content this app
    ships, so it is the only content this test can hold — editorial text added later is covered by
    the same list through the back-office review.
    """
    from academy.models import Course

    for course in Course.objects.all():
        blob = " ".join([course.title, course.summary, course.description, course.access_note]).lower()
        for word in FORBIDDEN_WORDS:
            assert word not in blob, f"{course.slug} says {word!r}"


def test_the_seeded_catalogue_contains_no_real_personal_data(academy_seeded):
    """No name, no e-mail address, no telephone number anywhere in the seeded catalogue."""
    from academy.models import Course, TrainingProvider

    blob = " ".join(
        [f"{c.title} {c.summary} {c.description} {c.access_note}" for c in Course.objects.all()]
        + [f"{p.name} {p.note} {p.city}" for p in TrainingProvider.objects.all()]
    )
    assert "@" not in blob
    assert re.search(r"\+?\d[\d ().-]{7,}", blob) is None
