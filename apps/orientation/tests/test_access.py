"""Access control: IDOR, resume tokens, ownership, save gate (G2)."""

import pytest
from django.test import Client
from django.urls import reverse

from accounts.permissions import can
from orientation.models import OrientationSession
from orientation.tests.conftest import walk

pytestmark = [pytest.mark.django_db, pytest.mark.security]


def _start(client, lang="fr"):
    response = client.post(f"/{lang}/orientation/")
    assert response.status_code == 302
    return response["Location"]


def _complete(client):
    url = _start(client)
    walk(client, url, [("objective", "research")])
    session = OrientationSession.objects.latest("created_at")
    return session, reverse("orientation:result", kwargs={"session_id": session.id})


def _token_from(client, result_url):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(client.get(result_url).content, "html.parser")
    return soup.find(id="resume-token").get_text().strip()


def test_other_browser_cannot_open_session(client, other_client, active_ruleset):
    url = _start(client)
    assert client.get(url).status_code == 200
    assert other_client.get(url).status_code == 404
    assert (
        other_client.post(url, {"question_key": "objective", "answer": "work", "action": "answer"}).status_code == 404
    )
    session = OrientationSession.objects.get()
    assert other_client.get(reverse("orientation:result", kwargs={"session_id": session.id})).status_code == 404
    assert other_client.post(reverse("orientation:restart", kwargs={"session_id": session.id})).status_code == 404
    assert session.answers == {}


def test_unknown_session_is_404(client, active_ruleset):
    assert client.get("/fr/orientation/session/00000000-0000-0000-0000-000000000000/").status_code == 404


def test_resume_token_grants_access_to_another_browser(client, other_client, active_ruleset):
    session, result_url = _complete(client)
    token = _token_from(client, result_url)
    assert other_client.get(result_url).status_code == 404
    response = other_client.post("/fr/orientation/reprendre/", {"token": token})
    assert response.status_code == 302 and response["Location"] == result_url
    assert other_client.get(result_url).status_code == 200


def test_wrong_or_malformed_token_is_refused(client, other_client, active_ruleset):
    _complete(client)
    response = other_client.post("/fr/orientation/reprendre/", {"token": "f" * 64})
    assert response.status_code == 200
    html = response.content.decode()
    assert "Aucune pré-évaluation ne correspond" in html
    assert 'role="alert"' in html
    response = other_client.post("/fr/orientation/reprendre/", {"token": "short"})
    assert response.status_code == 200 and "n’est pas valide" in response.content.decode()
    assert other_client.get("/fr/orientation/reprendre/").status_code == 200


def test_resume_is_throttled(client, active_ruleset):
    from orientation import constants

    for _ in range(constants.THROTTLE_RESUME_LIMIT):
        assert client.post("/fr/orientation/reprendre/", {"token": "a" * 64}).status_code == 200
    assert client.post("/fr/orientation/reprendre/", {"token": "a" * 64}).status_code == 429


def test_token_is_stored_hashed(client, active_ruleset):
    session, result_url = _complete(client)
    token = _token_from(client, result_url)
    session.refresh_from_db()
    assert session.resume_token_hash != token and token not in session.resume_token_hash


def test_authenticated_user_owns_sessions(client, person_user, user_factory, active_ruleset):
    client.force_login(person_user)
    url = _start(client)
    session = OrientationSession.objects.get()
    assert session.user == person_user and session.expires_at is None
    # a fresh browser logged in as the owner can open it
    owner_client = Client()
    owner_client.force_login(person_user)
    assert owner_client.get(url).status_code == 200
    # another user cannot
    other = user_factory("other@example.test")
    other_client = Client()
    other_client.force_login(other)
    assert other_client.get(url).status_code == 404
    assert can(person_user, "view", session) is True
    assert can(other, "view", session) is False
    assert can(other, "delete", session) is False


def test_policy_denies_anonymous_and_staff_by_default(client, staff_user, active_ruleset):
    _start(client)
    session = OrientationSession.objects.get()
    assert can(staff_user, "view", session) is False
    from django.contrib.auth.models import AnonymousUser

    assert can(AnonymousUser(), "view", session) is False


def test_save_requires_login(client, active_ruleset):
    session, _ = _complete(client)
    response = client.post(reverse("orientation:save", kwargs={"session_id": session.id}))
    assert response.status_code == 302 and "/compte/login/" in response["Location"]


def test_save_is_gated_by_public_forms_gate(client, person_user, active_ruleset, seeded):
    session, result_url = _complete(client)
    client.force_login(person_user)
    html = client.get(result_url).content.decode()
    assert 'data-gate="forms-closed"' in html  # save button replaced by the unavailable notice
    response = client.post(reverse("orientation:save", kwargs={"session_id": session.id}))
    assert response.status_code == 200 and 'data-gate="forms-closed"' in response.content.decode()
    session.refresh_from_db()
    assert session.user is None


def test_save_attaches_session_when_gate_open(client, person_user, active_ruleset, seeded, legal_published):
    session, result_url = _complete(client)
    client.force_login(person_user)
    html = client.get(result_url).content.decode()
    assert "Enregistrer dans mon espace" in html
    response = client.post(reverse("orientation:save", kwargs={"session_id": session.id}))
    assert response.status_code == 302
    session.refresh_from_db()
    assert session.user == person_user and session.expires_at is None
    html = client.get(result_url).content.decode()
    assert "enregistrée dans votre espace" in html
    from orientation.services import sessions_for_user

    assert list(sessions_for_user(person_user)) == [session]


def test_other_user_cannot_save_someone_elses_session(client, person_user, active_ruleset, legal_published):
    session, _ = _complete(client)
    stranger = Client()
    stranger.force_login(person_user)
    assert stranger.post(reverse("orientation:save", kwargs={"session_id": session.id})).status_code == 404


def test_expired_anonymous_session_is_not_accessible(client, active_ruleset):
    import datetime as dt

    from django.utils import timezone

    url = _start(client)
    OrientationSession.objects.update(expires_at=timezone.now() - dt.timedelta(minutes=1))
    assert client.get(url).status_code == 404
