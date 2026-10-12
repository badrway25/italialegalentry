"""
The sign-in of «Il varco» — the form (V5.4 plan §1.13; acceptance L3, L4; W2-B, step 2).

``accounts.forms.LoginForm`` is allauth's form with its PRESENTATION ONLY, wired by ``ACCOUNT_FORMS["login"]``.
These tests hold both halves of that sentence, through the real allauth views (no ``force_login``):

* what must NOT have changed — the fields and their names, every method of the sign-in (none is overridden), the one
  message for an unknown address and for a wrong password, the limit on failed attempts and what it answers, the
  CSRF check, the absence of «remember me», the mandatory verification of the address, the second factor, and a
  password reset that answers the same thing for every address;
* what the form now says — no placeholder, the e-mail keyboard, no capitals and no spell-check, left to right in
  every language, the address's purpose ``username`` (a password manager's identifier) and the password's
  ``current-password``; after a refusal the address is kept, the password is not, both fields point to the summary
  and neither is marked invalid; a field's own error stays on the field;
* the fix pass (11 October 2026): the sign-up's name says its input purpose (WCAG 1.3.5, review M3); allauth's reset,
  new-password and second-factor forms are allauth's with their presentation only — no placeholder, and the code on
  the digits' keyboard (review m4).
"""

from __future__ import annotations

import re

import pytest
from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.models import EmailAddress
from django import forms
from django.conf import settings
from django.test import Client
from django.utils import translation

from accounts.forms import (
    FORM_ERRORS_ID,
    AuthenticateForm,
    LoginForm,
    RefusalBoundField,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SignupForm,
)

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Str0ng-Passw0rd-2026!"
LOGIN = "/fr/compte/login/"


@pytest.fixture
def verified_user(user_factory):
    user = user_factory("varco-form@example.test", password=PASSWORD, full_name="Amina Test")
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    return user


def _input(html: str, field_id: str) -> str:
    match = re.search(rf'<input\b[^>]*\bid="{field_id}"[^>]*>', html)
    assert match, f"no input #{field_id}"
    return match.group(0)


def _attribute(tag: str, name: str) -> str | None:
    match = re.search(rf'\s{name}="([^"]*)"', tag)
    return match.group(1) if match else None


def _summary(html: str) -> str:
    match = re.search(
        rf'<div class="notice notice--error form-errors"[^>]*id="{FORM_ERRORS_ID}">(.*?)</div>\s*</div>', html, re.S
    )
    assert match, "no error summary"
    return " ".join(re.sub(r"<[^>]+>", " ", match.group(1)).split())


def _main(response) -> str:
    """The page's <main>, without the one thing that differs from a request to the next: the CSRF token."""
    html = re.sub(r'name="csrfmiddlewaretoken" value="[^"]*"', "", response.content.decode())
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


# ------------------------------------------------------------------------------------- presentation only


def test_the_login_form_is_allauth_s_form_and_overrides_no_method_of_the_sign_in():
    assert settings.ACCOUNT_FORMS["login"] == "accounts.forms.LoginForm"
    assert issubclass(LoginForm, AllauthLoginForm)
    # the class adds its constructor (the widgets' attributes) and the bound field's class; `media`, `base_fields`
    # and `declared_fields` are written by Django's form metaclass on every form class
    own = {name for name in vars(LoginForm) if not name.startswith("__")}
    assert own == {"bound_field_class", "base_fields", "declared_fields", "media"}, own
    assert LoginForm.declared_fields.keys() == AllauthLoginForm.declared_fields.keys(), "no field is added"
    for name in LoginForm.declared_fields:
        assert LoginForm.declared_fields[name] is AllauthLoginForm.declared_fields[name], f"{name} is redeclared"
    for name, member in vars(AllauthLoginForm).items():
        if callable(member) and name != "__init__":
            assert getattr(LoginForm, name) is member, f"LoginForm overrides {name}"
    for name in (
        "clean",
        "clean_login",
        "user_credentials",
        "login",
        "full_clean",
        "is_valid",
        "add_error",
        "_clean_with_password",
    ):
        assert getattr(LoginForm, name) is getattr(AllauthLoginForm, name), name
    # the bound field changes one read-only property, the description's ids
    assert LoginForm.bound_field_class is RefusalBoundField and issubclass(RefusalBoundField, forms.BoundField)
    assert {name for name in vars(RefusalBoundField) if not name.startswith("__")} == {"aria_describedby"}


def test_the_fields_are_allauth_s_two_fields_and_there_is_no_remember_me():
    ours, theirs = LoginForm(), AllauthLoginForm()
    assert list(ours.fields) == list(theirs.fields) == ["login", "password"]
    assert settings.ACCOUNT_SESSION_REMEMBER is False and "remember" not in ours.fields
    for name in ours.fields:
        a, b = ours.fields[name], theirs.fields[name]
        assert type(a) is type(b) and type(a.widget) is type(b.widget), name
        assert (a.required, a.max_length, a.strip, str(a.label)) == (b.required, b.max_length, b.strip, str(b.label))
        assert [type(v) for v in a.validators] == [type(v) for v in b.validators], name
        assert str(a.help_text) == str(b.help_text), "the «forgotten password» link is allauth's own help text"
        assert a.widget.input_type == b.widget.input_type, name


def test_what_the_two_widgets_say():
    form, theirs = LoginForm(), AllauthLoginForm()
    login, password = form.fields["login"].widget, form.fields["password"].widget
    their_login, their_password = theirs.fields["login"].widget, theirs.fields["password"].widget
    assert "placeholder" in their_login.attrs and "placeholder" in their_password.attrs
    assert "placeholder" not in login.attrs and "placeholder" not in password.attrs, "the label is above the field"
    assert login.input_type == "email" and password.input_type == "password"
    # the address is the sign-in's identifier: password managers key a saved credential on «username» (allauth writes
    # «email», which can offer the person's contact card instead — review m5); the password stays allauth's
    assert their_login.attrs["autocomplete"] == "email" and login.attrs["autocomplete"] == "username"
    assert password.attrs["autocomplete"] == their_password.attrs["autocomplete"] == "current-password"
    assert login.attrs["maxlength"] == their_login.attrs["maxlength"]
    assert login.attrs["inputmode"] == "email"
    for widget in (login, password):
        assert widget.attrs["autocapitalize"] == "none"
        assert widget.attrs["spellcheck"] == "false"
        assert widget.attrs["dir"] == "ltr"
    added = {"inputmode", "autocapitalize", "spellcheck", "dir"}
    assert set(login.attrs) - set(their_login.attrs) == added
    assert set(password.attrs) - set(their_password.attrs) == added - {"inputmode"}
    assert set(their_login.attrs) - set(login.attrs) == {"placeholder"}
    assert set(their_password.attrs) - set(password.attrs) == {"placeholder"}
    assert form.fields["password"].help_beside_label is True, "form_field.html sets the help in the label's row"
    assert not hasattr(form.fields["login"], "help_beside_label")
    # a second form is not touched by the first one's attributes: the widgets are per instance
    assert "placeholder" in AllauthLoginForm().fields["password"].widget.attrs


@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_the_page_writes_them(client, seeded, lang):
    html = client.get(f"/{lang}/compte/login/").content.decode()
    login, password = _input(html, "id_login"), _input(html, "id_password")
    assert _attribute(login, "type") == "email" and _attribute(login, "name") == "login"
    assert _attribute(password, "type") == "password" and _attribute(password, "name") == "password"
    assert _attribute(login, "autocomplete") == "username"
    assert _attribute(password, "autocomplete") == "current-password"
    for tag in (login, password):
        assert _attribute(tag, "placeholder") is None, tag
        assert _attribute(tag, "dir") == "ltr"
        assert _attribute(tag, "autocapitalize") == "none" and _attribute(tag, "spellcheck") == "false"
        assert " required" in tag and _attribute(tag, "aria-invalid") is None
        assert _attribute(tag, "value") is None
    assert _attribute(login, "inputmode") == "email" and _attribute(login, "aria-describedby") is None
    form = html.split('<form class="form"', 1)[1].split("</form>", 1)[0]
    assert 'name="remember"' not in html and 'type="checkbox"' not in form
    assert form.count('name="csrfmiddlewaretoken"') == 1
    assert not re.search(r"<title>\s*(Erreur|Errore|Error|خطأ)", html), "a page at rest says no error in its title"


# ------------------------------------------------------------------------------------- a refused sign-in


def test_a_refusal_keeps_the_address_and_says_one_thing_for_both_causes(client, seeded, verified_user):
    with translation.override("fr"):
        mismatch = str(get_adapter().error_messages["email_password_mismatch"])
    wrong_password = client.post(LOGIN, {"login": verified_user.email, "password": "not-the-password"})
    unknown_address = Client().post(LOGIN, {"login": "nobody-here@example.test", "password": "not-the-password"})
    for response in (wrong_password, unknown_address):
        assert response.status_code == 200
    assert "_auth_user_id" not in client.session
    first, second = wrong_password.content.decode(), unknown_address.content.decode()
    assert mismatch in _summary(first), _summary(first)
    assert _summary(first) == _summary(second), "an unknown address and a wrong password are answered alike"
    for html, address in ((first, verified_user.email), (second, "nobody-here@example.test")):
        login, password = _input(html, "id_login"), _input(html, "id_password")
        assert _attribute(login, "value") == address, "the address is kept"
        assert _attribute(password, "value") is None and "not-the-password" not in html, "the password is not"
        # both fields point to the summary, before what Django writes; neither is marked invalid: the refusal does
        # not say which of the two is wrong, and no field carries a red edge
        assert _attribute(login, "aria-describedby") == FORM_ERRORS_ID
        assert _attribute(password, "aria-describedby") == f"{FORM_ERRORS_ID} id_password_helptext"
        assert _attribute(login, "aria-invalid") is None and _attribute(password, "aria-invalid") is None
        assert 'class="form-field form-field--error' not in html
        assert f'id="{FORM_ERRORS_ID}"' in html and 'role="alert" tabindex="-1"' in html
        assert 'id="id_password_helptext"' in html, "the description's second id exists on the page"
        assert re.search(r"<title>\s*Erreur — \s*Connexion\s*·", html), "the title says the error first (L4)"


def test_a_field_s_own_error_stays_on_the_field(client, seeded):
    html = client.post(LOGIN, {"login": "", "password": ""}).content.decode()
    login, password = _input(html, "id_login"), _input(html, "id_password")
    assert _attribute(login, "aria-invalid") == "true" and _attribute(login, "aria-describedby") == "id_login_error"
    assert _attribute(password, "aria-invalid") == "true"
    assert _attribute(password, "aria-describedby") == "id_password_helptext id_password_error"
    assert 'id="id_login_error" role="alert"' in html and 'id="id_password_error" role="alert"' in html
    assert html.count('class="form-field form-field--error') == 2
    summary = _summary(html)
    assert 'href="#id_login"' in html and 'href="#id_password"' in html, "the summary links to each field in error"
    assert "Courriel" in summary and "Mot de passe" in summary


def test_the_limit_on_failed_attempts_is_allauth_s_and_answers_in_the_form(client, seeded, verified_user):
    assert settings.ACCOUNT_RATE_LIMITS["login_failed"] == "5/5m/ip,5/5m/key"
    with translation.override("fr"):
        too_many = str(get_adapter().error_messages["too_many_login_attempts"])
        mismatch = str(get_adapter().error_messages["email_password_mismatch"])
    for attempt in range(5):
        html = client.post(LOGIN, {"login": verified_user.email, "password": f"wrong-{attempt}"}).content.decode()
        assert mismatch in _summary(html) and too_many not in html, attempt
    # the sixth is refused whatever the password — the right one too — and it is said in the form, not on a 429 page
    response = client.post(LOGIN, {"login": verified_user.email, "password": PASSWORD})
    html = response.content.decode()
    assert response.status_code == 200 and "_auth_user_id" not in client.session
    assert too_many in _summary(html) and mismatch not in _summary(html)
    assert _attribute(_input(html, "id_login"), "aria-describedby") == FORM_ERRORS_ID
    assert "data-varco-stage" in html and 'href="/fr/compte/password/reset/"' in html, "the way forward is on the page"


def test_the_sign_in_still_needs_its_csrf_token(seeded, verified_user):
    strict = Client(enforce_csrf_checks=True)
    assert strict.get(LOGIN).status_code == 200
    response = strict.post(LOGIN, {"login": verified_user.email, "password": PASSWORD})
    assert response.status_code == 403 and "_auth_user_id" not in strict.session
    token = strict.cookies["csrftoken"].value
    response = strict.post(LOGIN, {"login": verified_user.email, "password": PASSWORD, "csrfmiddlewaretoken": token})
    assert response.status_code == 302 and "_auth_user_id" in strict.session


# ------------------------------------------------------------------------------------- the other states


def test_an_unverified_address_is_sent_to_its_verification_on_the_stage(client, seeded, user_factory, mailoutbox):
    user = user_factory("unverified-varco@example.test", password=PASSWORD)
    response = client.post(LOGIN, {"login": user.email, "password": PASSWORD}, follow=True)
    html = response.content.decode()
    assert response.status_code == 200 and "_auth_user_id" not in client.session
    assert response.redirect_chain[-1][0].endswith("/fr/compte/confirm-email/")
    assert "data-varco-stage" in html and html.count("<h1") == 1
    assert len(mailoutbox) == 1 and user.email in mailoutbox[0].to, "allauth sends the verification again"
    message = html.split('class="container messages"', 1)[1].split("</div>", 1)[0]
    assert user.email in message, "the session message names the address the e-mail was sent to"
    way = html.split('class="varco__back"', 1)[1].split("</p>", 1)[0]
    assert 'href="/fr/compte/login/"' in way, "a page that is not a form leads back to the sign-in"


def test_the_second_factor_s_step_is_on_the_stage_and_refuses_a_wrong_code(client, seeded, verified_user):
    from allauth.mfa.totp.internal import auth as totp

    totp.TOTP.activate(verified_user, totp.generate_totp_secret())
    response = client.post(LOGIN, {"login": verified_user.email, "password": PASSWORD})
    assert response.status_code == 302 and response["Location"].endswith("/fr/compte/2fa/authenticate/")
    assert "_auth_user_id" not in client.session, "a password alone does not open the reserved area"
    html = client.get(response["Location"]).content.decode()
    code = _input(html, "id_code")
    assert _attribute(code, "autocomplete") == "one-time-code" and _attribute(code, "name") == "code"
    assert _attribute(code, "inputmode") == "numeric", "the digits' keyboard"
    assert _attribute(code, "placeholder") is None, "no «Code» under «Code»"
    assert "data-varco-stage" in html and 'data-loader-host="varco-door"' in html and html.count("<h1") == 1
    with translation.override("fr"):
        incorrect = str(get_adapter().error_messages["incorrect_code"])
    refused = client.post(response["Location"], {"code": "000000"}).content.decode()
    assert "_auth_user_id" not in client.session
    assert incorrect in refused and _attribute(_input(refused, "id_code"), "aria-invalid") == "true"
    assert re.search(r"<title>\s*Erreur — ", refused)


def test_a_password_reset_answers_alike_for_every_address(client, seeded, verified_user, mailoutbox):
    known = client.post("/fr/compte/password/reset/", {"email": verified_user.email}, follow=True)
    unknown = Client().post("/fr/compte/password/reset/", {"email": "nobody-here@example.test"}, follow=True)
    for response in (known, unknown):
        assert response.status_code == 200
        assert response.redirect_chain[-1][0].endswith("/fr/compte/password/reset/done/")
    assert _main(known) == _main(unknown), "the page never says whether the address has an account"
    assert verified_user.email not in _main(known)
    assert "data-varco-stage" in _main(known) and 'class="varco__back"' in _main(known)
    reset = _main(client.get("/fr/compte/password/reset/"))
    assert 'placeholder="' not in reset, "the reset's address: no placeholder (m4)"


# ------------------------------------------------------------------------------------- the fix pass


def test_the_sign_up_s_name_says_its_purpose(client, seeded, legal_published):
    """WCAG 2.2 AA 1.3.5 (review M3, the check's A1): the name is «name», the address «email», both passwords
    «new-password» — and still no placeholder."""
    form = SignupForm()
    assert form.fields["full_name"].widget.attrs["autocomplete"] == "name"
    assert form.fields["email"].widget.attrs["autocomplete"] == "email"
    for name in ("password1", "password2"):
        assert form.fields[name].widget.attrs["autocomplete"] == "new-password", name
    html = client.get("/fr/compte/signup/").content.decode()
    name = _input(html, "id_full_name")
    assert _attribute(name, "autocomplete") == "name" and _attribute(name, "placeholder") is None, name


@pytest.mark.parametrize(
    ("ours", "key", "path"),
    [
        (ResetPasswordForm, "reset_password", "allauth.account.forms.ResetPasswordForm"),
        (ResetPasswordKeyForm, "reset_password_from_key", "allauth.account.forms.ResetPasswordKeyForm"),
        (AuthenticateForm, "authenticate", "allauth.mfa.base.forms.AuthenticateForm"),
    ],
)
def test_allauth_s_other_entrance_forms_change_their_presentation_only(ours, key, path):
    """Review m4: the reset's address, the new password's two fields and the second factor's code write no
    placeholder (the label is above the field: «Code» was read twice), and the code takes the digits' keyboard — the
    authenticator's six digits and allauth's recovery codes, eight digits. Nothing else: the class adds its
    constructor only, under the setting allauth reads."""
    import importlib

    module, name = path.rsplit(".", 1)
    theirs = getattr(importlib.import_module(module), name)
    setting = settings.MFA_FORMS if key == "authenticate" else settings.ACCOUNT_FORMS
    assert setting[key] == f"accounts.forms.{ours.__name__}" and issubclass(ours, theirs)
    own = {member for member in vars(ours) if not member.startswith("__")}
    assert own <= {"base_fields", "declared_fields", "media"}, f"{ours.__name__} adds {own}"
    assert set(ours.declared_fields) == set(theirs.declared_fields), "no field is added or taken away"
    kwargs = {"user": None} if key == "authenticate" else {}
    form, their = ours(**kwargs), theirs(**kwargs)
    for field_name, field in form.fields.items():
        assert "placeholder" in their.fields[field_name].widget.attrs, f"allauth writes one on {field_name}"
        assert "placeholder" not in field.widget.attrs, field_name
        assert set(their.fields[field_name].widget.attrs) - set(field.widget.attrs) == {"placeholder"}
    if key == "authenticate":
        from allauth.mfa import app_settings as mfa_settings

        assert form.fields["code"].widget.attrs["inputmode"] == "numeric"
        assert form.fields["code"].widget.attrs["autocomplete"] == "one-time-code"
        assert mfa_settings.RECOVERY_CODE_DIGITS == 8 and mfa_settings.TOTP_DIGITS == 6, "both codes are digits"
