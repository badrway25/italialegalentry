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
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from consents.models import ConsentPurpose
from consents.services import (
    ACKNOWLEDGEMENT_PURPOSES,
    ACKNOWLEDGEMENT_SOURCE_KEY,
    LOCKED_CONSENT_KEYS,
    REUSED_CONSENT_KEYS,
    UI_CONSENT_TEXTS,
)
from core.forms import AcknowledgementBooleanField, ConsentBooleanField, HoneypotFormMixin, PublicFormMixin
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest

SENSITIVE_DATA_HELP = _("Merci de ne pas indiquer de données sensibles (santé, origine, opinions, etc.) dans ce champ.")
HONEYPOT_FIELDS = ("website_url", "form_started_at")


def current_language() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def consent_label(purpose: str) -> tuple[str, str]:
    """(label, effective language) for a form's box: the locked consent sentence where one is prescribed, else the
    team's acknowledgement (V5.16 §3), in French like the prescribed sentences (``ACKNOWLEDGEMENT_TEXT``)."""
    if purpose in ACKNOWLEDGEMENT_PURPOSES:
        return UI_CONSENT_TEXTS[purpose], "fr"
    key = LOCKED_CONSENT_KEYS.get(purpose) or REUSED_CONSENT_KEYS.get(purpose)
    return locked_content.get(key, current_language())


def consent_caption(purpose: str, lang: str, effective: str) -> str:
    """V5.27 / R7′ (3), FINAL_DELIVERY_V2 §3.9: on a page of another language the box's French wording is identified
    source material — the prescribed consent on its own form, or the team's acknowledgement whose words open it
    (``ACKNOWLEDGEMENT_SOURCE_KEY``) on the form it belongs to — by the one identification caption of the locked layer
    (the label role, «the source text in French; the Arabic translation pending validation»); "" on a page in the
    wording's own language and wherever the policy draws no caption (Italian, English keep today's rendering). The words
    of the box are never translated: the record keeps the French it shows."""
    if effective == lang:
        return ""
    from cms import locked_renderings

    key = LOCKED_CONSENT_KEYS.get(purpose) or REUSED_CONSENT_KEYS.get(purpose) or ACKNOWLEDGEMENT_SOURCE_KEY
    text = locked_renderings.caption_text(key, lang)
    return format_html('<p class="t-label locked-caption" data-locked-caption="{}">{}</p>', key, text) if text else ""


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
        if self.consent_purpose in ACKNOWLEDGEMENT_PURPOSES:  # category A, team wording: not a consent (V5.16 §3)
            self.fields["consent"] = AcknowledgementBooleanField()
        sentence, effective = consent_label(self.consent_purpose)
        self.fields["consent"].label = sentence
        self.fields["consent"].label_lang = effective if effective != lang else ""
        caption = consent_caption(self.consent_purpose, lang, effective)
        if caption:  # the preserved form's body is otherwise unchanged: the caption is the box's help text
            self.fields["consent"].help_text = caption
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

    #: Three steps (V5.15 W3, lane B; DECISIONS §5.12): the 14 prescribed fields keep their prescribed order — the
    #: company and its referent, then the need — and the last step reviews them before the locked consent and the
    #: locked button (static/js/src/steps.js; without script, the two groups and the consent in sequence).
    steps = (
        (
            "entreprise",
            _("L’entreprise et son référent"),
            "ile-referent",
            ("company_name", "sector", "headquarters", "contact_name_and_role", "email", "phone"),
        ),
        (
            "besoin",
            _("Le besoin"),
            "ile-need",
            (
                "profiles_needed",
                "indicative_headcount",
                "qualifications_required",
                "experience_required",
                "language_requirements",
                "training_needs",
                "indicative_timeline",
                "notes",
            ),
        ),
        ("envoi", _("Vérification et envoi"), "ile-review", ("consent",)),
    )
    steps_review = True
    #: Round 2 (V5.15 W3, lane B): the short fields paired by meaning where the prescribed order already sets them
    #: side by side (the sector and the seat, the e-mail and the telephone) — the headcount and the timeline are not
    #: next to each other in that order, so they are not paired; and «Le besoin» gathers its seven optional fields
    #: under a quiet sub-head after the one it requires (components/form_steps.html).
    #: F1: inside «Le besoin»'s details only like pairs with like — the two text areas the prescribed order already sets
    #: side by side (the qualifications and the experience; the languages and the training); the headcount and the
    #: timeline, single lines, stand alone at a short measure (no ragged row of a line beside a text area).
    steps_pairs = (
        ("sector", "headquarters"),
        ("email", "phone"),
        ("qualifications_required", "experience_required"),
        ("language_requirements", "training_needs"),
    )
    steps_more = {"besoin": _("Précisions facultatives")}

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
