from __future__ import annotations

from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from core.forms import ConsentBooleanField, HoneypotFormMixin, PublicFormMixin

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
