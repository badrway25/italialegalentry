"""
The REAL allauth login/logout round-trip (no ``force_login``).

Regression (browser QA 2026-09-20): every real login answered 500 because allauth looked for
``user.username`` while rendering its "signed in as …" message; the custom user only has an e-mail.
The rest of the suite logs users in with ``force_login`` and therefore never exercised that path.
"""

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings

from accounts.utils import user_display

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Str0ng-Passw0rd-2026!"


@pytest.fixture
def verified_user(user_factory):
    user = user_factory("real-login@example.test", password=PASSWORD, full_name="Amina Test")
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    return user


def test_settings_tell_allauth_there_is_no_username_field():
    assert settings.ACCOUNT_USER_MODEL_USERNAME_FIELD is None
    assert settings.ACCOUNT_USER_DISPLAY == "accounts.utils.user_display"


def test_user_display_prefers_full_name_then_email(user_factory):
    assert user_display(user_factory("a@example.test", full_name="Nadia B.")) == "Nadia B."
    assert user_display(user_factory("b@example.test")) == "b@example.test"


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_real_login_reaches_the_reserved_area(client, seeded, verified_user, lang):
    response = client.post(f"/{lang}/compte/login/", {"login": verified_user.email, "password": PASSWORD})
    assert response.status_code == 302, response.content[:300]
    assert "/espace-reserve/" in response["Location"]
    page = client.get(response["Location"])
    assert page.status_code == 200
    assert "Italy Legal Entry™" in page.content.decode()


def test_wrong_password_is_rejected_without_error(client, seeded, verified_user):
    response = client.post("/fr/compte/login/", {"login": verified_user.email, "password": "wrong-password"})
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


def test_unverified_email_cannot_enter_the_reserved_area(client, seeded, user_factory):
    user = user_factory("unverified@example.test", password=PASSWORD)
    response = client.post("/fr/compte/login/", {"login": user.email, "password": PASSWORD}, follow=True)
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session, "mandatory e-mail verification must block the session"


def test_logout_round_trip(client, seeded, verified_user):
    client.post("/fr/compte/login/", {"login": verified_user.email, "password": PASSWORD})
    assert "_auth_user_id" in client.session
    response = client.post("/fr/compte/logout/")
    assert response.status_code == 302
    assert "_auth_user_id" not in client.session
    assert client.get("/fr/espace-reserve/").status_code == 302
