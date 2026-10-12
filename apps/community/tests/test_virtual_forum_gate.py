"""Gate G11: the Virtual Forum is invisible until FeatureFlag ``virtual_forum`` is on."""

import pytest

from cms import locked_content
from cms.forbidden import scan

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

INDEX = "/fr/forum-virtuel/"


def test_hidden_when_flag_off(client, seeded, person_user):
    assert client.get(INDEX).status_code == 404
    client.force_login(person_user)
    assert client.get(INDEX).status_code == 404
    assert client.get(INDEX + "rejoindre/").status_code == 404
    assert client.get(INDEX + "salles/espace-commun/").status_code == 404


def test_text_when_flag_on_for_anonymous(client, seeded, flag_on):
    r = client.get(INDEX)
    assert r.status_code == 200
    html = r.content.decode()
    for key in ("p3.virtual_forum.title", "p3.virtual_forum.body", "p3.virtual_forum.button"):
        assert locked_content.text(key, "fr") in html, key
    assert 'href="/fr/compte/login/?next=' in html
    assert 'href="/fr/compte/signup/"' in html
    assert html.count("<h1") == 1
    assert not scan(html)
    assert "Italy Legal Entry™" in html and "®" not in html


def test_locked_text_falls_back_to_french_with_lang_attr(client, seeded, flag_on):
    html = client.get("/ar/forum-virtuel/").content.decode()
    assert 'lang="fr"' in html
    assert locked_content.text("p3.virtual_forum.body", "fr") in html


def test_logged_in_without_membership_sees_join_cta(client, seeded, flag_on, person_user):
    client.force_login(person_user)
    html = client.get(INDEX).content.decode()
    assert 'href="/fr/forum-virtuel/rejoindre/"' in html
    assert locked_content.text("p3.virtual_forum.button", "fr") in html
    assert "Salles thématiques" not in html


def test_pending_member_sees_pending_notice(client, seeded, flag_on, member_factory):
    m = member_factory("pending@example.test", status="pending")
    client.force_login(m.user)
    html = client.get(INDEX).content.decode()
    assert "Demande d’accès en cours d’examen" in html
    assert "Salles thématiques" not in html


def test_route_registered_as_gated_public_route():
    from core.public_routes import gated_routes

    routes = {(r.app, r.path, r.requires_gate) for r in gated_routes()}
    assert ("community", "forum-virtuel/", "virtual_forum") in routes
