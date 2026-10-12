from allauth.account.forms import SignupForm as AllauthSignupForm
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


class SignupForm(HoneypotFormMixin, AllauthSignupForm):
    full_name = forms.CharField(label=_("Nome e cognome"), max_length=160)
    account_type = forms.ChoiceField(label=_("Vi registrate come"), choices=PUBLIC_ACCOUNT_TYPES)
    # CONTENT_PENDING_LEGAL_REVIEW: label wording (the document prescribes acceptance of the
    # Conditions d’utilisation and the Privacy Policy for reserved-area access, §3.8.7 / §3.10).
    accept_terms = ConsentBooleanField(
        label=_("J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation."),
    )

    field_order = ["full_name", "email", "account_type", "password1", "password2", "accept_terms"]

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
