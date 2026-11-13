"""
«Mon compte» inside the console (V5.12 W2, lane B; DECISIONS «Lane B» acceptance 6: «/fr/compte/* renders inside the
console with the rail»), and the «Sécurité du compte» overview (DECISIONS §4: shield / shield-check).
"""

from __future__ import annotations

import pytest
from django.test import RequestFactory
from django.urls import reverse

from accounts import shell

pytestmark = pytest.mark.django_db


@pytest.fixture
def person(user_factory):
    return user_factory("shell.person@example.test", password="Une-phrase-longue-2026!")  # noqa: S106


def _get(client, user, name):
    client.force_login(user)
    response = client.get(reverse(name))
    assert response.status_code == 200, (name, response.status_code)
    return response.content.decode()


@pytest.mark.parametrize("name", ["accounts:profile", "account_email", "account_change_password", "mfa_index"])
def test_every_account_page_draws_the_console_rail_and_the_account_sections(client, person, name):
    html = _get(client, person, name)
    assert 'id="console-rail"' in html and 'class="console-bar' in html, f"{name}: the console's frame"
    assert "conto conto--console" in html and 'class="conto-nav"' in html, f"{name}: the account's own sections"
    assert 'class="site-header' not in html and "portal-footer" in html, f"{name}: not the public header and footer"
    assert html.count("<h1") == 1, name
    assert 'content="noindex, nofollow"' in html


def test_the_trail_says_the_space_then_my_account(client, person):
    html = _get(client, person, "account_email")
    bar = html.split('class="console-bar__crumbs"', 1)[1].split("</div>", 1)[0]
    assert "Espace réservé" in bar and "Mon compte" in bar
    assert f'href="{reverse("accounts:profile")}"' in bar, "away from the profile, «Mon compte» leads back to it"


def test_the_public_frame_stays_for_an_anonymous_visitor_and_a_closed_reserved_area(client, person, settings):
    response = client.get(reverse("account_reset_password"))
    assert response.status_code == 200
    assert 'id="console-rail"' not in response.content.decode()
    request = RequestFactory().get("/")
    request.user = person
    from core.models import SiteSettings

    site = SiteSettings.load()
    site.reserved_area_enabled = False
    site.save()
    assert shell.frame(request) == shell.PUBLIC_FRAME
    site.reserved_area_enabled = True
    site.save()
    assert shell.frame(request) == shell.CONSOLE_FRAME
    assert shell.frame("") == shell.PUBLIC_FRAME, "a template rendered without a request keeps the public frame"


def test_the_security_overview_says_the_second_factor_with_its_shield(client, person):
    html = _get(client, person, "accounts:profile")
    section = html.split('id="securite"', 1)[1].split("</section>", 1)[0]
    assert "Sécurité du compte" in section
    assert "#icon-shield" in section and "#icon-shield-check" not in section, "off: the plain shield"
    assert "non activée" in section and reverse("mfa_index") in section and reverse("account_change_password") in section
    assert reverse("account_email") in section
