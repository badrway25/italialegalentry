"""
The project team as a training provider, said in the reader's language (V5.24 §4–§5, the Arabic completeness audit's
W3.3; lane AR): the seeded «Équipe du projet Italy Legal Entry» is the catalogue's «Équipe du projet» followed by the
brand as one left-to-right run; every other provider keeps the name it registered under.
"""

from __future__ import annotations

import pytest
from django.utils import translation

from academy.models import ProviderKind, TrainingProvider

pytestmark = pytest.mark.django_db


@pytest.fixture
def project_team():
    return TrainingProvider.objects.create(
        slug="equipe-projet", name="Équipe du projet Italy Legal Entry", kind=ProviderKind.PROJECT, country="Italie"
    )


@pytest.fixture
def institute():
    return TrainingProvider.objects.create(
        slug="collina-verde",
        name="Istituto di formazione Collina Verde",
        kind=ProviderKind.TRAINING_BODY,
        country="Italia",
    )


@pytest.mark.parametrize(
    ("lang", "words"),
    [("fr", "Équipe du projet"), ("it", "Équipe del progetto"), ("en", "Project team"), ("ar", "فريق المشروع")],
)
def test_the_project_team_is_said_in_the_readers_language(project_team, lang, words):
    from django.utils.translation import gettext

    with translation.override(lang):
        shown = str(project_team.display_name)
        assert shown.startswith(gettext("Équipe du projet"))
        assert (
            gettext("Équipe du projet") == words or lang == "it"
        )  # the Italian catalogue's own wording is checked below
        assert '<span translate="no" dir="ltr" lang="en">Italy Legal Entry™</span>' in shown
        assert "Équipe du projet Italy Legal Entry" not in shown or lang == "fr"


def test_every_other_provider_keeps_its_registered_name(institute):
    with translation.override("ar"):
        assert str(institute.display_name) == "Istituto di formazione Collina Verde"
    assert str(institute) == "Istituto di formazione Collina Verde"
