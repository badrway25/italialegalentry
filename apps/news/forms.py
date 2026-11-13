from __future__ import annotations

from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from consents.models import ConsentPurpose
from core.forms import ConsentBooleanField, HoneypotFormMixin, PublicFormMixin
from enquiries.forms import consent_caption

NEWSLETTER_CONSENT_KEY = "p3.news.newsletter_consent"


class NewsletterForm(HoneypotFormMixin, PublicFormMixin):
    """« Restez informés » — e-mail + separate, mandatory, never pre-ticked consent (p3.news.newsletter_consent)."""

    max_text_length = 254

    email = forms.EmailField(
        label=_("Adresse e-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "inputmode": "email", "spellcheck": "false"}),
    )
    consent = ConsentBooleanField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lang = translation.get_language() or settings.LANGUAGE_CODE
        text, effective = locked_content.get(NEWSLETTER_CONSENT_KEY, lang)
        self.fields["consent"].label = text
        self.consent_language = effective
        self.consent_is_fallback = effective != lang.split("-")[0]
        # the error summary (components/form_errors.html) names the field by its label: a prescribed text shown in
        # another language than the page's keeps its `lang` there too, as the enquiry forms' consent does
        self.fields["consent"].label_lang = effective if self.consent_is_fallback else ""
        # V5.27 / R7′ (3), the V5.29 matrix's B2: on an Arabic page this prescribed French wording is identified source
        # material, by the locked layer's one caption — as the enquiry forms' box, the caption is the box's help text
        caption = consent_caption(ConsentPurpose.NEWSLETTER, lang.split("-")[0], effective)
        if caption:
            self.fields["consent"].help_text = caption
