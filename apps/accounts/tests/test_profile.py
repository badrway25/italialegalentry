"""Profile page: self only, edit own fields, memberships list, anonymous redirected."""

from __future__ import annotations

import pytest

from accounts.models import PersonProfile
from audit.models import AuditEvent
from cms.forbidden import scan

pytestmark = [pytest.mark.django_db]

PROFILE_URL = "/fr/compte/profil/"


def test_anonymous_is_redirected_to_login(client):
    r = client.get(PROFILE_URL)
    assert r.status_code == 302
    assert "/fr/compte/login/" in r["Location"]


def test_profile_shows_only_own_data(client, terms_user, other_user, organisation):
    client.force_login(terms_user)
    r = client.get(PROFILE_URL)
    assert r.status_code == 200
    html = r.content.decode()
    assert "alice@example.test" in html
    assert "Acme Formazione" in html
    assert "bob@example.test" not in html
    assert "Bob Durand" not in html
    assert html.count("<h1") == 1
    assert 'name="robots" content="noindex' in html
    assert not scan(html)
    assert "/fr/compte/2fa/" in html
    assert "/fr/compte/email/" in html
    assert "/fr/compte/password/change/" in html
    assert "/documents/" in html


def test_profile_edit_updates_user_and_person_profile(client, terms_user):
    client.force_login(terms_user)
    r = client.post(
        PROFILE_URL,
        {
            "full_name": "  Alice   Martin-Bey ",
            "preferred_language": "it",
            "phone": "+39 041 123456",
            "country_of_residence": "Maroc",
        },
    )
    assert r.status_code == 302
    terms_user.refresh_from_db()
    assert terms_user.full_name == "Alice Martin-Bey"
    assert terms_user.preferred_language == "it"
    profile = PersonProfile.objects.get(user=terms_user)
    assert profile.phone == "+39 041 123456"
    assert profile.country_of_residence == "Maroc"
    event = AuditEvent.objects.get(action="account.profile_updated")
    assert event.actor_id == terms_user.pk
    assert set(event.metadata["fields"]) == {"full_name", "preferred_language", "phone", "country_of_residence"}


def test_profile_edit_rejects_bad_phone_and_language(client, terms_user):
    client.force_login(terms_user)
    r = client.post(PROFILE_URL, {"full_name": "A", "preferred_language": "xx", "phone": "call me maybe"})
    assert r.status_code == 200
    html = r.content.decode()
    assert "aria-describedby" in html or "form-field__errors" in html
    terms_user.refresh_from_db()
    assert terms_user.full_name == "Alice Martin"


def test_profile_edit_cannot_target_another_user(client, terms_user, other_user):
    """There is no user id in the URL/form: posting foreign identifiers changes nothing for others."""
    client.force_login(terms_user)
    client.post(
        PROFILE_URL, {"full_name": "Hacked", "preferred_language": "fr", "user": other_user.pk, "id": other_user.pk}
    )
    other_user.refresh_from_db()
    assert other_user.full_name == "Bob Durand"
    terms_user.refresh_from_db()
    assert terms_user.full_name == "Hacked"


def test_delete_done_page_is_public_and_compliant(client):
    r = client.get("/fr/compte/profil/suppression/confirmee/")
    assert r.status_code == 200
    html = r.content.decode()
    assert not scan(html)
    assert "Italy Legal Entry™" in html
    assert "contact@agamieuromed.org" in html
