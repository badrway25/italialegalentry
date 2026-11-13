"""
V5.32 lane E — the Academy catalogue on the platform's list toolkit (academy.lists.CATALOGUE; portal.listing).

The owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 asks, on the platform's lists, for search,
sorting and filters where the backend supports them — a compact bar, an advanced drawer, the active criteria as chips,
a reset and a result count. The catalogue's service already held three narrowings (the domain, the teaching language,
a search); the page drew only the domain, as eight tabs. Held here:

* every narrowing applies to the rows the account may see (`Course.objects.visible_to`), never more — a draft course is
  reachable by no search, no filter, no order;
* an unknown value of a filter or of the order is ignored (whitelists), the search is cut at 80 characters;
* the GET keys keep the catalogue's own names (`domaine`, `langue`): an address written before still means the same;
* once something narrows: the result count, one chip per criterion (each a link that removes it), «Tout effacer»;
  nothing found → the toolkit's «Aucun résultat» with its way back, never the catalogue's «nothing published yet»;
* the domain tabs are gone; the bar, the drawer and their two page-only files are linked only where the bar is drawn.
"""

from __future__ import annotations

import re

import pytest
from django.urls import reverse

from academy.models import Course, CourseFormat, CourseType

pytestmark = [pytest.mark.django_db, pytest.mark.urls("academy.tests.urls")]


@pytest.fixture
def three_courses(provider, course_factory):
    """Three published courses that differ in every narrowable column, and one draft that matches every search."""
    a = course_factory(provider, slug="italien-a1", title="Italien A1", duration_hours=60)
    b = course_factory(
        provider,
        slug="securite",
        title="Sécurité sur le chantier",
        course_type=CourseType.WORKPLACE_SAFETY,
        language="fr",
        duration_hours=8,
    )
    # every title starts with an unaccented capital: the order by title never depends on the database's collation
    c = course_factory(
        provider,
        slug="civisme",
        title="Civisme et institutions",
        course_type=CourseType.CIVIC_EDUCATION,
        duration_hours=20,
    )
    Course.objects.filter(pk=c.pk).update(course_format=CourseFormat.IN_PERSON)
    course_factory(provider, slug="brouillon", title="Sécurité — brouillon", status="draft")
    return a, b, c


def _get(client, person, **params):
    client.force_login(person)
    response = client.get(reverse("academy:catalogue"), params)
    assert response.status_code == 200
    return response.content.decode("utf-8")


def _rows(html):
    return re.findall(r'<li class="db-task reg-row academy-row[^"]*" data-course="([\w-]+)"', html)


def test_the_bar_replaces_the_domain_tabs(client, person, three_courses):
    html = _get(client, person)
    assert 'class="lst__bar"' in html and 'name="q"' in html and 'name="tri"' in html
    assert 'class="reg-filter academy-filter"' not in html and "Tous les domaines" not in html
    assert html.count("css/dist/portal/listing.css") == 1 and html.count("js/dist/listing.js") == 1
    assert 'id="lst-catalogue-filters"' in html, "the drawer, on the overlay system"
    assert _rows(html) == ["civisme", "italien-a1", "securite"], "by default, by domain (then by title)"


def test_a_search_never_reaches_a_draft_and_names_its_chip(client, person, three_courses):
    html = _get(client, person, q="Sécurité")
    assert _rows(html) == ["securite"], "the draft «Sécurité — brouillon» is not visible, so not found"
    assert '<p class="lst__found" role="status">1 résultat</p>' in html
    assert 'class="lst__chip"' in html and "Votre recherche" in html
    assert 'class="lst__clear"' in html


@pytest.mark.parametrize(
    ("params", "expected"),
    [
        ({"domaine": CourseType.WORKPLACE_SAFETY}, ["securite"]),
        ({"langue": "fr"}, ["securite"]),
        ({"modalite": CourseFormat.IN_PERSON}, ["civisme"]),
        ({"domaine": CourseType.ITALIAN_LANGUAGE, "langue": "it"}, ["italien-a1"]),
    ],
)
def test_each_filter_narrows_with_the_catalogues_own_keys(client, person, three_courses, params, expected):
    html = _get(client, person, **params)
    assert _rows(html) == expected
    assert html.count('class="lst__chip"') == len(params)


def test_an_unknown_value_is_ignored_never_an_error(client, person, three_courses):
    html = _get(client, person, domaine="drop table", modalite="x", langue="xx", tri="-title")
    assert len(_rows(html)) == 3 and 'class="lst__chip"' not in html


def test_the_orders_are_the_whitelisted_three(client, person, three_courses):
    assert _rows(_get(client, person, tri="duree")) == ["securite", "civisme", "italien-a1"]
    assert _rows(_get(client, person, tri="titre")) == ["civisme", "italien-a1", "securite"]
    select = re.search(r'<select class="lst__select" name="tri"[^>]*>(.*?)</select>', _get(client, person), re.S)
    assert re.findall(r'<option value="(\w+)"', select.group(1)) == ["domaine", "titre", "duree"]


def test_the_search_is_cut_at_eighty_characters(client, person, three_courses):
    """The bar's own field and the search's chip carry the cut query (the page's hreflang alternates echo the raw
    address — base.html's, not the list's)."""
    html = _get(client, person, q="x" * 100)
    field = re.search(r'<input class="input lst__q"[^>]*\bvalue="([^"]*)"', html)
    assert field and field.group(1) == "x" * 80
    chip = re.search(r'<span class="lst__value" dir="auto">([^<]*)</span>', html)
    assert chip and chip.group(1) == "x" * 80


def test_nothing_found_is_the_toolkits_empty_state_with_its_way_back(client, person, three_courses):
    html = _get(client, person, q="zzzz")
    assert _rows(html) == [] and 'class="lst-empty"' in html and "Aucun résultat" in html
    assert "les cours publiés apparaîtront ici" not in html, "the catalogue is not empty: the search found nothing"


def test_an_empty_catalogue_keeps_its_own_sentence_and_draws_no_bar(client, person, draft_course):
    html = _get(client, person)
    assert "les cours publiés apparaîtront ici" in html
    assert 'class="lst__bar"' not in html and "css/dist/portal/listing.css" not in html
