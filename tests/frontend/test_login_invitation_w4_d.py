"""
The sign-in page invites to the sign-up only while the sign-up is open (W4-D part 2, A3 — part 1's F-4).

The sign-in «Il varco» inherits allauth's block (templates/account/login.html, W2-B), whose paragraph «Si vous n'avez
pas encore créé de compte, merci de vous enregistrer au préalable.» links to the sign-up. While G2 keeps the public
forms closed, that link answers «Inscriptions fermées»: an invitation to a door that is shut. The page now asks for
that one paragraph not to be drawn while the sign-up is closed — the gate the account adapter reads
(``gates.public_forms_enabled``, ``accounts.adapters.AccountAdapter.is_open_for_signup``); allauth's words, form and
fields stay ``block.super``; no word is added.
"""

from __future__ import annotations

import re

import pytest

from core import gates

pytestmark = pytest.mark.django_db

LOGIN = {"fr": "/fr/compte/login/", "ar": "/ar/compte/login/"}
SIGNUP_PATH = "/compte/signup/"
INVITATION = {"fr": "pas encore créé de compte", "ar": "إذا لم يكن لديك حساب"}


def _main(html: str) -> str:
    return html[html.index("<main") : html.index("</main>")]


def _assert_the_form_is_there(main: str) -> None:
    assert 'name="login"' in main and 'name="password"' in main, "the sign-in form is allauth's, in both states"
    assert 'type="submit"' in main


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_invitation_to_a_closed_sign_up(client, seeded, lang):
    assert gates.public_forms_enabled().open is False
    main = _main(client.get(LOGIN[lang]).content.decode())
    assert INVITATION[lang] not in main, "the page invites to a sign-up that answers «Inscriptions fermées»"
    assert not re.search(rf'href="/{lang}{SIGNUP_PATH}[^"]*"', main), "a link to the closed sign-up is left"
    _assert_the_form_is_there(main)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_invitation_is_back_once_the_sign_up_opens(client, seeded, legal_published, lang):
    assert gates.public_forms_enabled().open is True
    main = _main(client.get(LOGIN[lang]).content.decode())
    assert INVITATION[lang] in main
    paragraph = next(p for p in re.findall(r"<p\b[^>]*>.*?</p>", main, flags=re.S) if INVITATION[lang] in p)
    assert re.search(rf'href="/{lang}{SIGNUP_PATH}[^"]*"', paragraph), paragraph
    _assert_the_form_is_there(main)


def test_the_forms_override_reopens_the_invitation_as_it_reopens_the_sign_up(client, seeded, set_flag):
    """The invitation follows the gate the sign-up follows, the QA override included."""
    set_flag("forms_override_without_legal", True)
    assert INVITATION["fr"] in _main(client.get(LOGIN["fr"]).content.decode())
    assert "Inscriptions ferm" not in client.get("/fr/compte/signup/").content.decode()


def test_other_entrance_paragraphs_are_drawn_while_the_sign_up_is_closed(client, seeded):
    """Only the invitation leaves: the password reset's own paragraph, an allauth `p` element too, stays."""
    main = _main(client.get("/fr/compte/password/reset/").content.decode())
    assert re.search(r'<p class="account-page__text">[^<]+', main), "the reset page lost its paragraph"
