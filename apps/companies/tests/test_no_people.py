"""
THE PROOF: a company account cannot reach any person object by any route this vertical added.

CR-04 is explicit — « Deny by default. Nessuna ricerca libera, nessun elenco. In P0 la visibilità è
**zero** ». The previous platform verified company accounts precisely so that they could « consulter
les candidats »; that is the model this one does not reproduce.

Four independent proofs, because one of them alone could be defeated by a future change:

1. STRUCTURE — no model of this app relates to a person object (a case file, a person profile, an
   orientation session). The one relation to an account is ``NeedAssignment.assignee``, which is the
   ACTOR answerable for the need, and the test pins it by name so that adding a second one fails.
2. ROUTES — every route declared by ``companies.urls`` is walked as a company account, with a real
   person, a real case file and a real profile present in the database. Not one response contains
   that person's e-mail, name, case reference or identifier.
3. VOCABULARY — no RENDERED page of this vertical carries recruitment language, in any of the four
   languages: no matching, no candidate, no application, no job board, no CV. The check is on what
   is sent to the browser, not on the source, which says « no candidate browser » in its own
   comments and must not be confused with the offence it describes.
4. GUESSING — a person's primary key, a case reference and a person e-mail, pushed into every route
   that takes a parameter, produce 404 or 403, never a page.
"""

from __future__ import annotations

import re

import pytest
from django.urls import reverse

from accounts import roles
from cases.models import CasePurpose
from cases.services import open_case

pytestmark = pytest.mark.django_db

#: The only relation to an account this app is allowed to hold, and why.
ALLOWED_USER_RELATIONS = {("NeedAssignment", "assignee")}


@pytest.fixture
def a_person(user_factory):
    """A real person, with a real case file, present in the database while the company browses."""
    person = user_factory("une-personne@example.test", role=roles.PERSON, full_name="Prénom Nom De Famille")
    case = open_case(person, purpose=CasePurpose.WORK)
    return person, case


# ---------------------------------------------------------------------------------------------
# 1. Structure
# ---------------------------------------------------------------------------------------------
def test_no_model_of_this_app_relates_to_a_person_object() -> None:
    from django.apps import apps as django_apps
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    person_models = set()
    for label in ("cases.CaseFile", "cases.ChecklistItem", "cases.PathwayAssessment", "accounts.PersonProfile"):
        app_label, model_name = label.split(".")
        try:
            person_models.add(django_apps.get_model(app_label, model_name))
        except LookupError:  # pragma: no cover - the sibling app is always installed
            pass

    offenders = []
    for model in django_apps.get_app_config("companies").get_models():
        for field in model._meta.get_fields():
            related = getattr(field, "related_model", None)
            if related is None:
                continue
            if related in person_models:
                offenders.append(f"{model.__name__}.{field.name} -> {related.__name__}")
            if related is user_model and (model.__name__, field.name) not in ALLOWED_USER_RELATIONS:
                offenders.append(f"{model.__name__}.{field.name} -> User")
    assert offenders == [], f"this vertical must not hold a relation to a person: {offenders}"


def test_the_one_account_relation_is_the_answerable_actor() -> None:
    """``assignee`` is the party ANSWERABLE for the need — the opposite of a candidate."""
    from companies.models import ActorRole, NeedAssignment

    assert {choice for choice, _label in ActorRole.choices} == {
        "authorised_actor",
        "training_body",
        "professional",
        "project_team",
    }
    assert NeedAssignment._meta.get_field("assignee").verbose_name


# ---------------------------------------------------------------------------------------------
# 2. Routes
# ---------------------------------------------------------------------------------------------
def _company_routes(need_reference: str) -> list[str]:
    """Every route this vertical declares, with a real reference where one is needed."""
    from companies import urls as companies_urls

    routes = []
    for pattern in companies_urls.urlpatterns:
        name = pattern.name
        args = [need_reference] if "reference" in pattern.pattern.regex.groupindex else []
        routes.append(reverse(f"companies:{name}", args=args))
    return routes


def test_no_route_of_this_vertical_discloses_a_person(client, company_factory, need_factory, a_person) -> None:
    person, case = a_person
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    client.force_login(user)

    leaks = []
    for url in _company_routes(need.reference):
        for method in ("get", "post"):
            response = getattr(client, method)(url)
            if response.status_code >= 400 or response.status_code in (301, 302):
                continue
            body = response.content.decode()
            for token in (person.email, person.full_name, case.reference, str(case.uuid)):
                if token and token in body:
                    leaks.append(f"{method.upper()} {url} → {token}")
    assert leaks == [], f"a person leaked through the company workspace: {leaks}"


def test_there_is_no_route_that_takes_a_person(company_factory, need_factory) -> None:
    """No parameter of this vertical is a person, an account or a case."""
    from companies import urls as companies_urls

    forbidden = {"person", "personne", "user", "candidate", "candidat", "case", "dossier", "profile_id"}
    offenders = []
    for pattern in companies_urls.urlpatterns:
        captured = set(pattern.pattern.regex.groupindex)
        if captured & forbidden:
            offenders.append(f"{pattern.name}: {captured & forbidden}")
        route = str(pattern.pattern)
        if any(word in route for word in ("personne", "candidat", "profils/", "people")):
            offenders.append(f"{pattern.name}: {route}")
    assert offenders == [], f"a route of this vertical addresses a person: {offenders}"


# ---------------------------------------------------------------------------------------------
# 3. Vocabulary
# ---------------------------------------------------------------------------------------------
#: Recruitment vocabulary, in the four languages. A company expresses a NEED; it does not recruit
#: here, does not match, does not browse and does not receive applications (D0a, CR-03, CR-04).
RECRUITMENT_WORDS = (
    "matching",
    "candidat",
    "candidato",
    "candidate",
    "مرشح",
    "postuler",
    "candidature",
    "job board",
    "offre d’emploi",
    "offre d'emploi",
    "annonce d’emploi",
    "recrutement",
    "recruter",
    "reclutamento",
    "recruit",
    "cv ",
    "curriculum vitae",
    "profil de candidat",
    "banque de profils",
    "rechercher une personne",
    "consulter les candidats",
)


def _rendered_pages(client, need_reference: str) -> dict[str, str]:
    """Every page of this vertical, as a visitor actually receives it."""
    pages = {}
    for url in _company_routes(need_reference):
        response = client.get(url)
        if response.status_code == 200:
            pages[url] = response.content.decode()
    # A vocabulary check over an empty set of pages passes and proves nothing.
    assert len(pages) >= 5, f"too few pages rendered to prove anything: {sorted(pages)}"
    return pages


def test_no_recruitment_language_in_the_rendered_workspace(client, company_factory, need_factory) -> None:
    """
    The check is on what is RENDERED, not on the source: the source of this vertical says « no
    matching, no candidate browser » in its own comments, which is the opposite of the offence, and
    a test that could not tell the two apart would be a test of the comments.
    """
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    client.force_login(user)

    offenders = []
    for url, body in _rendered_pages(client, need.reference).items():
        lowered = body.lower()
        for word in RECRUITMENT_WORDS:
            if word in lowered:
                offenders.append(f"{url}: « {word} »")
    assert offenders == [], f"recruitment vocabulary rendered in the company workspace: {offenders}"


def test_the_rendered_workspace_promises_nothing(client, company_factory, need_factory) -> None:
    """No visa, no permit, no promise — and no word that could read as an administrative decision."""
    promises = ("visa garanti", "permis garanti", "emploi garanti", "approuvé", "vous serez sélectionné")
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    client.force_login(user)

    offenders = []
    for url, body in _rendered_pages(client, need.reference).items():
        lowered = body.lower()
        offenders += [f"{url}: « {word} »" for word in promises if word in lowered]
    assert offenders == [], offenders


def test_no_form_of_this_vertical_offers_an_age_field(client, company_factory, need_factory) -> None:
    """
    Two proofs on the rendered forms: no control is named after an age, and no age band appears as a
    value. The WORD may appear — the need form says in so many words that an age criterion has no
    place here — but a field, a choice or a band may not.
    """
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    client.force_login(user)

    age_word = re.compile(r"(?<![\w’'-])(âge|age|ages|età|eta|عمر)(?![\w’'-])", re.I)
    age_band = re.compile(r"(1[5-9]|[2-7]\d)\s*[-–—/]\s*(1[5-9]|[2-7]\d)")
    control = re.compile(r'(?:name|id)="([^"]+)"')

    offenders = []
    for url, body in _rendered_pages(client, need.reference).items():
        offenders += [f"{url}: control « {found} »" for found in control.findall(body) if age_word.search(found)]
        if age_band.search(body):
            offenders.append(f"{url}: an age band appears as a value")
    assert offenders == [], offenders


# ---------------------------------------------------------------------------------------------
# 4. Guessing
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("route_name", ["need_detail", "need_edit", "need_submit", "need_withdraw"])
def test_a_person_identifier_pushed_into_a_route_reaches_nothing(
    client, company_factory, a_person, route_name: str
) -> None:
    person, case = a_person
    _profile, user = company_factory("alpha")
    client.force_login(user)
    for guess in (str(person.pk), case.reference, str(case.uuid).replace("-", "")[:10].upper()):
        url = reverse(f"companies:{route_name}", args=[guess])
        for method in ("get", "post"):
            response = getattr(client, method)(url)
            assert response.status_code in (403, 404, 405), (url, method, response.status_code)


def test_the_company_workspace_offers_no_search(client, company_factory, need_factory) -> None:
    """No free search: a query parameter changes nothing, because no view reads one."""
    profile, user = company_factory("alpha")
    need = need_factory(profile)
    client.force_login(user)
    plain = client.get(reverse("companies:needs")).content.decode()
    searched = client.get(reverse("companies:needs") + "?q=nom&search=personne&user=1").content.decode()
    # The CSRF token differs between two renders, so the comparison is on the register itself.
    assert need.title in plain and need.title in searched
    assert '<input type="search"' not in plain
    assert 'name="q"' not in plain
