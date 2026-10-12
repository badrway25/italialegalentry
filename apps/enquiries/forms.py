"""
Public forms of the enquiries app.

Every form combines ``HoneypotFormMixin`` (privacy-friendly anti-spam), ``PublicFormMixin``
(normalisation, maximum lengths) and a mandatory, never pre-checked ``ConsentBooleanField`` whose
label is the locked consent sentence. Prescribed labels are read from the locked registry at
instantiation time — never hand-copied.
"""

from __future__ import annotations

from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from consents.models import ConsentPurpose
from consents.services import LOCKED_CONSENT_KEYS, REUSED_CONSENT_KEYS
from core.forms import ConsentBooleanField, HoneypotFormMixin, PublicFormMixin
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest

SENSITIVE_DATA_HELP = _("Merci de ne pas indiquer de données sensibles (santé, origine, opinions, etc.) dans ce champ.")
HONEYPOT_FIELDS = ("website_url", "form_started_at")


def current_language() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def consent_label(purpose: str) -> tuple[str, str]:
    """(locked consent sentence, effective language) for a consent purpose."""
    key = LOCKED_CONSENT_KEYS.get(purpose) or REUSED_CONSENT_KEYS.get(purpose)
    return locked_content.get(key, current_language())


class PublicSubmissionForm(HoneypotFormMixin, PublicFormMixin, forms.ModelForm):
    """
    Common behaviour: consent field, locked consent label with ``label_lang`` marker when the
    sentence is rendered in fallback French, honeypot fields excluded from the visible sequence.
    """

    consent_purpose: str = ""
    consent = ConsentBooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lang = current_language()
        sentence, effective = consent_label(self.consent_purpose)
        self.fields["consent"].label = sentence
        self.fields["consent"].label_lang = effective if effective != lang else ""
        for name, field in self.fields.items():
            if name in HONEYPOT_FIELDS or name == "consent":
                continue
            field.widget.attrs.setdefault("class", "form-control")
            if isinstance(field, forms.EmailField):
                field.widget.attrs.setdefault("autocomplete", "email")
                field.widget.attrs.setdefault("inputmode", "email")

    def prescribed_fields(self):
        """Visible data fields, in the model/prescribed order (without honeypot and consent)."""
        for name in self.Meta.fields:
            yield self[name]

    def spam_fields(self):
        return [self[name] for name in HONEYPOT_FIELDS]

    def normalised_email(self) -> str:
        return (self.cleaned_data.get("email") or "").strip().lower()


class CompanyNeedsForm(PublicSubmissionForm):
    """« Recueil des besoins » — 14 fields in the prescribed order, labels from the locked registry."""

    consent_purpose = ConsentPurpose.COMPANY_NEEDS
    max_text_length = 4000

    class Meta:
        model = CompanyNeedsRequest
        fields = CompanyNeedsRequest.DATA_FIELDS
        widgets = {
            "company_name": forms.TextInput(attrs={"autocomplete": "organization", "maxlength": 200}),
            "sector": forms.TextInput(attrs={"maxlength": 160}),
            "headquarters": forms.TextInput(attrs={"autocomplete": "address-level2", "maxlength": 200}),
            "contact_name_and_role": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 200}),
            "phone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel", "inputmode": "tel", "maxlength": 40}),
            "profiles_needed": forms.Textarea(attrs={"rows": 4}),
            "indicative_headcount": forms.TextInput(attrs={"maxlength": 60}),
            "qualifications_required": forms.Textarea(attrs={"rows": 3}),
            "experience_required": forms.Textarea(attrs={"rows": 3}),
            "language_requirements": forms.Textarea(attrs={"rows": 3}),
            "training_needs": forms.Textarea(attrs={"rows": 3}),
            "indicative_timeline": forms.TextInput(attrs={"maxlength": 200}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {"notes": SENSITIVE_DATA_HELP}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lang = current_language()
        labels, effective = locked_content.get("p1.companies.form.fields", lang)
        for name, label in zip(self.Meta.fields, labels, strict=True):
            self.fields[name].label = label
            self.fields[name].label_lang = effective if effective != lang else ""


class CollaborationProposalForm(PublicSubmissionForm):
    """
    Institutions / universities collaboration proposal. ``kind`` is set by the view.
    CONTENT_PENDING_LEGAL_REVIEW: labels are team UI strings (not prescribed by the document).
    """

    consent_purpose = ConsentPurpose.INSTITUTION_PROPOSAL

    class Meta:
        model = CollaborationProposal
        fields = (
            "organisation_name",
            "organisation_type",
            "contact_name_and_role",
            "email",
            "phone",
            "country",
            "proposal",
        )
        widgets = {
            "organisation_name": forms.TextInput(attrs={"autocomplete": "organization", "maxlength": 200}),
            "organisation_type": forms.TextInput(attrs={"maxlength": 120}),
            "contact_name_and_role": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 200}),
            "phone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel", "inputmode": "tel", "maxlength": 40}),
            "country": forms.TextInput(attrs={"autocomplete": "country-name", "maxlength": 80}),
            "proposal": forms.Textarea(attrs={"rows": 6}),
        }
        help_texts = {"proposal": SENSITIVE_DATA_HELP}

    def __init__(self, *args, purpose: str | None = None, **kwargs):
        if purpose:
            self.consent_purpose = purpose
        super().__init__(*args, **kwargs)


class ContactForm(PublicSubmissionForm):
    """Generic contact form (name, e-mail, subject, message)."""

    consent_purpose = ConsentPurpose.CONTACT

    class Meta:
        model = ContactRequest
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 160}),
            "subject": forms.TextInput(attrs={"maxlength": 200}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }
        help_texts = {"message": SENSITIVE_DATA_HELP}
