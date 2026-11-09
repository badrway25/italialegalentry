"""
The companies' taxonomy in the reader's language (V5.24 §4–§5, the Arabic completeness audit's W3.1; lane AR): a sector
or a territory keeps its French source as its key and is said through the catalogue in Italian, English and Arabic; the
row's own Italian label and the French source remain the fallbacks for a row an editor adds later.
"""

from __future__ import annotations

import re

import pytest
from django.urls import reverse
from django.utils import translation

from companies import seeds
from companies.forms import CompanyNeedForm, CompanyProfileForm
from companies.models import TAXONOMY_LABELS, Sector, Territory, taxonomy_label

pytestmark = pytest.mark.django_db


def test_the_catalogue_knows_every_seeded_label():
    known = {str(label) for label in TAXONOMY_LABELS}
    with translation.override("fr"):
        seeded = {label_fr for _code, label_fr, _label_it in (*seeds.SECTORS, *seeds.TERRITORIES)}
    assert seeded == {str(label) for label in _french(TAXONOMY_LABELS)}, (
        "the listed labels are the seeds', no more, no less"
    )
    assert len(known) == len(seeds.SECTORS) + len(seeds.TERRITORIES)


def _french(labels):
    with translation.override(None):
        return [str(label) for label in labels]


@pytest.mark.parametrize(
    ("lang", "sector", "territory"),
    [
        ("fr", "Bâtiment et travaux publics", "Vénétie"),
        ("it", "Edilizia e opere pubbliche", "Veneto"),
        ("en", "Construction and public works", "Veneto"),
        ("ar", "البناء والأشغال العمومية", "فينيتو"),
    ],
)
def test_a_seeded_row_is_said_in_the_readers_language(lang, sector, territory):
    seeds.seed_taxonomy()
    row = Sector.objects.get(code="batiment")
    region = Territory.objects.get(code="veneto")
    with translation.override(lang):
        assert taxonomy_label(row) == sector
        assert row.label == sector
        assert taxonomy_label(region) == territory


def test_a_row_the_editor_adds_falls_back_to_its_italian_then_to_the_french():
    row = Sector.objects.create(code="editorial", label_fr="Un secteur ajouté", label_it="Un settore aggiunto")
    bare = Sector.objects.create(code="bare", label_fr="Un autre secteur")
    with translation.override("it"):
        assert taxonomy_label(row) == "Un settore aggiunto"
        assert taxonomy_label(bare) == "Un autre secteur"
    with translation.override("ar"):
        assert taxonomy_label(row) == "Un secteur ajouté"
    with translation.override("fr"):
        assert taxonomy_label(row) == "Un secteur ajouté"


# the need form's and the profile form's options (v524-ar-fix B2): a ModelChoiceField prints the row's __str__, which
# printed label_fr — «Vénétie», «Agroalimentaire et transformation» on /it/, /en/ and /ar/
CATALOGUE = {
    "it": ("Edilizia e opere pubbliche", "Veneto"),
    "en": ("Construction and public works", "Veneto"),
    "ar": ("البناء والأشغال العمومية", "فينيتو"),
}


@pytest.mark.parametrize("lang", sorted(CATALOGUE))
def test_the_forms_options_read_the_catalogues_rendering(lang):
    seeds.seed_taxonomy()
    sector, territory = CATALOGUE[lang]
    with translation.override(lang):
        need = CompanyNeedForm()
        sectors = {str(label) for _value, label in need.fields["sector"].choices}
        territories = {str(label) for _value, label in need.fields["territory"].choices}
        profile_sectors = {str(label) for _value, label in CompanyProfileForm().fields["sector"].choices}
        assert str(Sector.objects.get(code="batiment")) == sector
    assert sector in sectors and sector in profile_sectors
    assert territory in territories
    french = {label_fr for _code, label_fr, _label_it in (*seeds.SECTORS, *seeds.TERRITORIES)}
    leaked = (sectors | territories | profile_sectors) & french
    if lang == "ar":
        assert not leaked, leaked  # no French source among the Arabic options
    assert "Vénétie" not in territories and "Bâtiment et travaux publics" not in sectors


@pytest.mark.parametrize("lang", sorted(CATALOGUE))
def test_the_new_need_page_offers_the_options_in_the_readers_language(lang, client, company_factory):
    seeds.seed_taxonomy()
    _profile, user = company_factory("alpha")
    client.force_login(user)
    path = reverse("companies:need_create")
    response = client.get(f"/{lang}{path[3:]}")
    assert response.status_code == 200
    options = [
        re.sub(r"\s+", " ", text).strip()
        for text in re.findall(r"<option[^>]*>(.*?)</option>", response.content.decode(), flags=re.S)
    ]
    sector, territory = CATALOGUE[lang]
    assert sector in options and territory in options
    assert "Vénétie" not in options and "Agroalimentaire et transformation" not in options
