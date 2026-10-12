"""End-to-end wizard flow through the HTML views (fr and ar), previous/next, HTMX, throttle."""

import pytest
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.urls import reverse

from cms import locked_content
from orientation import constants
from orientation.models import OrientationResult, OrientationSession, Ruleset, SessionStatus
from orientation.tests.conftest import walk

pytestmark = pytest.mark.django_db

DISCLAIMER = locked_content.text("p3.persons.how_it_works", "fr")


def _start(client, lang="fr"):
    response = client.post(f"/{lang}/orientation/")
    assert response.status_code == 302, response.content[:200]
    return response["Location"]


def _soup(response):
    return BeautifulSoup(response.content, "html.parser")


def test_start_page_renders_intro_and_disclaimer(
    client, active_ruleset, phase3_open
):  # prescribed Phase 3 wording is rendered only once gate G3 is open
    response = client.get("/fr/orientation/")
    assert response.status_code == 200
    html = response.content.decode()
    soup = _soup(response)
    assert len(soup.find_all("h1")) == 1
    assert DISCLAIMER in html
    assert "pré-évaluation" in html
    form = soup.find("form", action="/fr/orientation/")
    assert form is not None and form.get("method") == "post"
    assert soup.find("input", {"name": "csrfmiddlewaretoken"}) is not None
    assert "/fr/orientation/reprendre/" in html


def test_start_page_without_active_ruleset(client, db):
    response = client.get("/fr/orientation/")
    assert response.status_code == 200
    html = response.content.decode()
    assert "Questionnaire indisponible" in html
    assert 'action="/fr/orientation/"' not in html
    response = client.post("/fr/orientation/")
    assert response.status_code == 302  # back to the intro with a message, never a 500
    assert OrientationSession.objects.count() == 0


def test_full_flow_fr_work_salaried(
    client, active_ruleset, phase3_open
):  # prescribed Phase 3 wording is rendered only once gate G3 is open
    url = _start(client)
    session = OrientationSession.objects.get()
    assert url == reverse("orientation:step", kwargs={"session_id": session.id})
    assert session.status == SessionStatus.IN_PROGRESS
    assert session.user is None and session.expires_at is not None

    response = client.get(url)
    assert response.status_code == 200
    soup = _soup(response)
    fieldset = soup.find("fieldset")
    assert fieldset is not None and fieldset.find("legend") is not None
    assert "Quel est l’objectif principal" in fieldset.find("legend").get_text()
    bar = soup.find(attrs={"role": "progressbar"})
    assert bar["aria-valuenow"] == "0" and bar["aria-valuemin"] == "0" and bar["aria-valuemax"] == "100"
    assert soup.find("button", {"name": "action", "value": "back"}) is None  # first question: no previous
    assert response.get("Cache-Control", "") and "no-cache" in response["Cache-Control"]

    response = walk(client, url, [("objective", "work")])
    assert response.status_code == 302 and response["Location"] == url
    soup = _soup(client.get(url))
    assert "projet professionnel" in soup.find("legend").get_text()
    assert int(soup.find(attrs={"role": "progressbar"})["aria-valuenow"]) > 0
    assert soup.find("button", {"name": "action", "value": "back"}) is not None
    # Implicit submission (Enter key) triggers the FIRST submit button: it must be "Continuer".
    submit_values = [b.get("value") for b in soup.find("form", class_="wizard__form").find_all("button", type="submit")]
    assert submit_values[0] == "answer", submit_values

    response = walk(client, url, [("work_profile", "salaried"), ("training_interest", "true")])
    result_url = reverse("orientation:result", kwargs={"session_id": session.id})
    assert response.status_code == 302 and response["Location"] == result_url

    session.refresh_from_db()
    assert session.status == SessionStatus.COMPLETED
    assert session.resume_token_hash and len(session.resume_token_hash) == 64
    result = OrientationResult.objects.get(session=session)
    assert result.outcome.pathway_key == "salaried_work"
    assert result.ruleset_version == 1
    assert result.disclaimer_version == constants.DISCLAIMER_VERSION
    assert result.disclaimer_key == "p3.persons.how_it_works"
    assert result.answers_snapshot == {"objective": "work", "work_profile": "salaried", "training_interest": True}
    assert result.kind == "INFORMATIVE_PREASSESSMENT"

    response = client.get(result_url)
    assert response.status_code == 200
    html = response.content.decode()
    soup = _soup(response)
    assert len(soup.find_all("h1")) == 1
    assert "Pré-évaluation à caractère informatif" in html
    assert DISCLAIMER in html
    assert "Travail salarié" in html  # locked pathway title via the registry tag
    assert "v1" in html and constants.DISCLAIMER_VERSION in html
    assert "Formation avant le départ" in html  # training interest block
    token_el = soup.find(id="resume-token")
    assert token_el is not None and len(token_el.get_text().strip()) == 64
    # shown once only
    assert _soup(client.get(result_url)).find(id="resume-token") is None
    # step URL now redirects to the result
    assert client.get(url)["Location"] == result_url


def test_previous_button_reverts_last_answer(client, active_ruleset):
    url = _start(client)
    walk(client, url, [("objective", "work"), ("work_profile", "salaried")])
    session = OrientationSession.objects.get()
    assert session.history == ["objective", "work_profile"]
    response = client.post(url, {"action": "back"})
    assert response.status_code == 302
    session.refresh_from_db()
    assert session.history == ["objective"]
    assert "work_profile" not in session.answers
    assert "projet professionnel" in _soup(client.get(url)).find("legend").get_text()
    client.post(url, {"action": "back"})
    session.refresh_from_db()
    assert session.history == [] and session.answers == {}
    client.post(url, {"action": "back"})  # no-op at the first question
    session.refresh_from_db()
    assert session.history == []


def test_invalid_and_stale_answers_are_rejected(client, active_ruleset):
    url = _start(client)
    response = client.post(url, {"question_key": "objective", "answer": "teleport", "action": "answer"})
    assert response.status_code == 200
    soup = _soup(response)
    error = soup.find(id="answer-error")
    assert error is not None and error.get("role") == "alert"
    assert soup.find("fieldset")["aria-describedby"] == "answer-error"
    response = client.post(url, {"question_key": "work_profile", "answer": "salaried", "action": "answer"})
    assert response.status_code == 200 and "répondre à nouveau" in response.content.decode()
    response = client.post(url, {"question_key": "objective", "action": "answer"})
    assert response.status_code == 200 and "Sélectionnez une réponse" in response.content.decode()
    assert OrientationSession.objects.get().answers == {}


def test_flow_family_unsure_goes_to_individual_analysis(
    client, active_ruleset, phase3_open
):  # prescribed Phase 3 wording is rendered only once gate G3 is open
    url = _start(client)
    walk(client, url, [("objective", "family"), ("family_member_status", "unsure")])
    result = OrientationResult.objects.get()
    assert result.outcome.pathway_key == constants.NEEDS_INDIVIDUAL_ANALYSIS
    html = client.get(reverse("orientation:result", kwargs={"session_id": result.session_id})).content.decode()
    assert "Situation à examiner individuellement" in html
    assert DISCLAIMER in html


def test_flow_in_arabic_falls_back_to_french_with_lang_attr(
    client_ar, active_ruleset, phase3_open
):  # prescribed Phase 3 wording is rendered only once gate G3 is open
    response = client_ar.get("/ar/orientation/")
    assert response.status_code == 200
    assert '<html lang="ar" dir="rtl"' in response.content.decode()
    url = _start(client_ar, "ar")
    assert url.startswith("/ar/orientation/session/")
    soup = _soup(client_ar.get(url))
    question = soup.find(id="wizard-question")
    assert question["lang"] == "fr"
    labels = soup.select("label.wizard__label")
    assert labels and all(label.get("lang") == "fr" for label in labels)
    walk(client_ar, url, [("objective", "research")])
    session = OrientationSession.objects.get()
    assert session.language == "ar"
    response = client_ar.get(reverse("orientation:result", kwargs={"session_id": session.id}))
    html = response.content.decode()
    assert response.status_code == 200 and '<html lang="ar" dir="rtl"' in html
    assert DISCLAIMER in html and 'lang="fr"' in html


def test_boolean_question_renders_radio_group(client, active_ruleset):
    url = _start(client)
    walk(client, url, [("objective", "work"), ("work_profile", "seasonal")])
    soup = _soup(client.get(url))
    inputs = soup.select("input[name=answer]")
    assert [i["value"] for i in inputs] == ["true", "false"]
    assert all(i["type"] == "radio" for i in inputs)
    for i in inputs:
        assert soup.find("label", {"for": i["id"]}) is not None
    walk(client, url, [("training_interest", "false")])
    assert OrientationResult.objects.get().outcome.pathway_key == "other_regular_routes"


def test_htmx_requests_get_fragment_and_headers(client, active_ruleset):
    url = _start(client)
    response = client.get(url, HTTP_HX_REQUEST="true")
    assert response.status_code == 200
    html = response.content.decode()
    assert "<html" not in html and 'id="orientation-step"' in html
    response = client.post(
        url, {"question_key": "objective", "answer": "work", "action": "answer"}, HTTP_HX_REQUEST="true"
    )
    assert response.status_code == 200
    assert response["HX-Push-Url"] == url
    assert "projet professionnel" in response.content.decode() and "<html" not in response.content.decode()
    response = client.post(url, {"action": "back"}, HTTP_HX_REQUEST="true")
    assert "objectif principal" in response.content.decode()
    walk(client, url, [("objective", "self_employment")])  # plain POST → 302
    response = client.get(url, HTTP_HX_REQUEST="true")
    assert response["HX-Redirect"].endswith("/resultat/")


def test_htmx_completion_sends_hx_redirect(client, active_ruleset):
    url = _start(client)
    response = client.post(
        url, {"question_key": "objective", "answer": "research", "action": "answer"}, HTTP_HX_REQUEST="true"
    )
    assert response.status_code == 200
    assert response["HX-Redirect"] == reverse(
        "orientation:result", kwargs={"session_id": OrientationSession.objects.get().id}
    )


def test_start_is_throttled(client, active_ruleset):
    cache.clear()
    for _ in range(constants.THROTTLE_START_LIMIT):
        assert client.post("/fr/orientation/").status_code == 302
    response = client.post("/fr/orientation/")
    assert response.status_code == 429
    assert "Trop de requêtes" in response.content.decode()
    assert OrientationSession.objects.count() == constants.THROTTLE_START_LIMIT


def test_restart_abandons_and_creates_new_session(client, active_ruleset):
    url = _start(client)
    walk(client, url, [("objective", "research")])
    first = OrientationSession.objects.get()
    response = client.post(reverse("orientation:restart", kwargs={"session_id": first.id}))
    assert response.status_code == 302
    assert OrientationSession.objects.count() == 2
    first.refresh_from_db()
    assert first.status == SessionStatus.COMPLETED  # completed sessions stay completed
    second = OrientationSession.objects.exclude(pk=first.pk).get()
    assert response["Location"].endswith(f"/session/{second.id}/")
    # an in-progress session is abandoned on restart
    client.post(reverse("orientation:restart", kwargs={"session_id": second.id}))
    second.refresh_from_db()
    assert second.status == SessionStatus.ABANDONED


def test_result_redirects_to_step_when_not_completed(client, active_ruleset):
    url = _start(client)
    session = OrientationSession.objects.get()
    response = client.get(reverse("orientation:result", kwargs={"session_id": session.id}))
    assert response.status_code == 302 and response["Location"] == url


def test_session_pages_are_noindex(client, active_ruleset):
    url = _start(client)
    assert 'content="noindex, nofollow"' in client.get(url).content.decode()


def test_new_sessions_use_the_active_ruleset(client, active_ruleset, superuser):
    from orientation import services

    v2 = services.import_ruleset(services.export_ruleset(active_ruleset), version=2, user=superuser)
    services.activate_ruleset(v2)
    _start(client)
    assert OrientationSession.objects.get().ruleset == v2
    assert Ruleset.objects.get(version=1).status == "retired"
