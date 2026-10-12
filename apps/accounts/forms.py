from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllauthResetPasswordKeyForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.mfa.base.forms import AuthenticateForm as AllauthAuthenticateForm
from django import forms
from django.utils.translation import gettext_lazy as _

from accounts import roles
from accounts.models import AccountType
from core.forms import ConsentBooleanField, HoneypotFormMixin

PUBLIC_ACCOUNT_TYPES = [
    (AccountType.PERSON, AccountType.PERSON.label),
    (AccountType.COMPANY, AccountType.COMPANY.label),
    (AccountType.INSTITUTION, AccountType.INSTITUTION.label),
    (AccountType.UNIVERSITY, AccountType.UNIVERSITY.label),
    (AccountType.PROFESSIONAL, AccountType.PROFESSIONAL.label),
]

ROLE_BY_ACCOUNT_TYPE = {
    AccountType.PERSON: roles.PERSON,
    AccountType.COMPANY: roles.COMPANY,
    AccountType.INSTITUTION: roles.INSTITUTION,
    AccountType.UNIVERSITY: roles.UNIVERSITY,
    AccountType.PROFESSIONAL: roles.PROFESSIONAL,
}


#: The id of the form's error summary (templates/components/form_errors.html).
FORM_ERRORS_ID = "form-errors"

#: What the sign-in's two fields say to the browser and to the keyboard of a phone — nothing else. ``None`` takes
#: an attribute away: allauth writes the label a second time as a placeholder («Adresse e-mail» under «Courriel»).
#: The address's purpose is ``username`` (allauth writes ``email``): it is the sign-in's identifier, and password
#: managers and a phone's suggestion bar key a saved credential on ``username``, where ``email`` may offer the
#: person's contact card instead (the review's m5; both are input purposes of WCAG 1.3.5).
LOGIN_PRESENTATION = {
    "login": {
        "placeholder": None,
        "autocomplete": "username",
        "inputmode": "email",
        "autocapitalize": "none",
        "spellcheck": "false",
        "dir": "ltr",
    },
    "password": {
        "placeholder": None,
        "autocapitalize": "none",
        "spellcheck": "false",
        "dir": "ltr",
    },
}


def without_placeholders(form: forms.BaseForm) -> None:
    """allauth writes each label a second time as a placeholder. On the entrance the label is above the field, so the
    attribute is taken away — the sheet does not draw it, and assistive technology would read the label twice
    («Code», «Code»)."""
    for field in form.fields.values():
        field.widget.attrs.pop("placeholder", None)


class RefusalBoundField(forms.BoundField):
    """
    A refused sign-in is said once, by the form's summary — «the address or the password», never which of the
    two — so no field carries an error of its own. Each visible field then points to that summary: its
    ``aria-describedby`` begins with the summary's id, before the ids Django writes (the help text, a field error).
    A widget that names its own description keeps it, as in Django.
    """

    @property
    def aria_describedby(self):
        described = super().aria_describedby
        if described is None or self.is_hidden or not self.form.non_field_errors():
            return described
        return " ".join(part for part in (FORM_ERRORS_ID, described) if part)


class LoginForm(AllauthLoginForm):
    """
    The sign-in form of «Il varco» (design V5, V5.4 plan §1.13; W2-B) — PRESENTATION ONLY.

    It is allauth's form: the same fields under the same names, the same validation, the same authentication
    through the adapter, the same rate limits and the same single message for a wrong address or a wrong
    password. No method of the sign-in is overridden (apps/accounts/tests/test_login_form_w2_b.py holds that),
    and there is still no «remember me» (``ACCOUNT_SESSION_REMEMBER = False``). What changes is what the two
    widgets say, and where the page draws the password's help:

    * no placeholder (the label is above the field, and a placeholder that renames it is read twice);
    * the address is typed on the e-mail keyboard, never capitalised nor spell-checked, left to right on an Arabic
      page too; its ``autocomplete`` says ``username`` — the identifier a password manager fills — and the
      password's stays allauth's ``current-password``;
    * ``help_beside_label``: templates/components/form_field.html sets the password's help text — allauth's own
      «forgotten password» link — at the end of the label's row instead of under the field;
    * after a refusal both fields are described by the form's summary (``RefusalBoundField``).
    """

    bound_field_class = RefusalBoundField

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, attributes in LOGIN_PRESENTATION.items():
            field = self.fields.get(name)
            if field is None:
                continue
            for attribute, value in attributes.items():
                if value is None:
                    field.widget.attrs.pop(attribute, None)
                elif attribute != "inputmode" or field.widget.input_type == value:
                    # the e-mail keyboard only for an e-mail field: a sign-in by user name would keep the text one
                    field.widget.attrs[attribute] = value
        if "password" in self.fields:
            self.fields["password"].help_beside_label = True


class ResetPasswordForm(AllauthResetPasswordForm):
    """
    The reset's request on «Il varco» (``ACCOUNT_FORMS["reset_password"]``) — allauth's form, PRESENTATION ONLY: its
    address writes no placeholder. The same field, the same answer for every address, the same rate limit
    (apps/accounts/tests/test_login_form_w2_b.py holds that it overrides nothing else).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        without_placeholders(self)


class ResetPasswordKeyForm(AllauthResetPasswordKeyForm):
    """
    The new password after a reset link (``ACCOUNT_FORMS["reset_password_from_key"]``) — allauth's form,
    PRESENTATION ONLY: its two passwords write no placeholder («Nouveau mot de passe» read a second time). The same
    fields, validators and key check.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        without_placeholders(self)


class AuthenticateForm(AllauthAuthenticateForm):
    """
    The second factor's code on «Il varco» (``MFA_FORMS["authenticate"]``) — allauth's form, PRESENTATION ONLY: no
    placeholder («Code» under «Code»), and the digits' keyboard. Both codes the field takes are digits — the
    authenticator's six and allauth's recovery codes (``MFA_RECOVERY_CODE_DIGITS``: eight digits, 65.19.4) — so
    ``inputmode="numeric"`` refuses nothing a person may type. The same field, validation and rate limit.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        without_placeholders(self)
        self.fields["code"].widget.attrs["inputmode"] = "numeric"


class SignupForm(HoneypotFormMixin, AllauthSignupForm):
    full_name = forms.CharField(label=_("Nome e cognome"), max_length=160)
    account_type = forms.ChoiceField(label=_("Vi registrate come"), choices=PUBLIC_ACCOUNT_TYPES)
    # CONTENT_PENDING_LEGAL_REVIEW: label wording (the document prescribes acceptance of the
    # Conditions d’utilisation and the Privacy Policy for reserved-area access, §3.8.7 / §3.10).
    accept_terms = ConsentBooleanField(
        label=_("J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation."),
    )

    field_order = ["full_name", "email", "account_type", "password1", "password2", "accept_terms"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Presentation only (design V5 «Il varco», W2-B; the core components' review, 9 October 2026): allauth writes
        # each label a second time as a placeholder («Adresse e-mail» under «Courriel», «Mot de passe (confirmation)»
        # cut short by the field's own control). The label is above the field: no placeholder.
        without_placeholders(self)
        # the name's input purpose (WCAG 2.2 AA, 1.3.5 — W2-B, review M3): a browser fills it, assistive technology
        # can say what it is for; the address says «email» and both passwords «new-password» (allauth's)
        self.fields["full_name"].widget.attrs["autocomplete"] = "name"

    def clean(self):
        cleaned = super().clean()
        if self.is_spam:
            raise forms.ValidationError(_("Impossibile completare la registrazione."))
        return cleaned

    def save(self, request):
        from accounts.services import register_declared_account_type
        from consents.models import ConsentPurpose
        from consents.services import record_consent
        from core import clock

        user = super().save(request)
        # The declared account type does NOT grant its role. A visitor can tick "Institution" on a
        # public form, and from phase P1 each role opens a real workspace: granting on declaration
        # would be an escalation that needs no exploit, only a dropdown. Only "person" is granted
        # immediately, because claiming to be a person claims nothing; the rest is queued for
        # verification and granted by a human in the back-office.
        register_declared_account_type(user, self.cleaned_data["account_type"], request=request)
        user.terms_accepted_at = clock.now()
        user.terms_consent = record_consent(request, ConsentPurpose.ACCOUNT_TERMS, email=user.email, user=user)
        user.save(update_fields=["terms_accepted_at", "terms_consent"])
        return user
