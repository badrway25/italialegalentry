"""
Shared form infrastructure for public forms.

* HoneypotFormMixin — privacy-friendly anti-spam (no third-party CAPTCHA): a hidden field that
  humans never fill plus a minimum fill time. Spam is *silently accepted* by the views (never
  stored) so bots receive no signal.
* PublicFormMixin — normalises whitespace, enforces maximum lengths, strips control characters.
* ConsentBooleanField — mandatory, never pre-checked consent checkbox.
"""

from __future__ import annotations

import re
import time

from django import forms
from django.utils.translation import gettext_lazy as _

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WS = re.compile(r"[ \t\f\v]+")

HONEYPOT_FIELD = "website_url"
TIMESTAMP_FIELD = "form_started_at"
MIN_FILL_SECONDS = 3
MAX_FILL_SECONDS = 60 * 60 * 6


class HoneypotFormMixin(forms.Form):
    website_url = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "class": "hp-field",
            }
        ),
    )
    form_started_at = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields[TIMESTAMP_FIELD].initial = str(int(time.time()))

    @property
    def is_spam(self) -> bool:
        data = self.data if self.is_bound else {}
        if (data.get(HONEYPOT_FIELD) or "").strip():
            return True
        started = data.get(TIMESTAMP_FIELD) or ""
        if not started.isdigit():
            return True
        elapsed = int(time.time()) - int(started)
        return elapsed < MIN_FILL_SECONDS or elapsed > MAX_FILL_SECONDS


class PublicFormMixin(forms.Form):
    """Normalise every text input: strip, collapse spaces, remove control characters."""

    max_text_length = 4000

    def clean(self):
        cleaned = super().clean()
        for name, value in list(cleaned.items()):
            if isinstance(value, str):
                value = _CONTROL_CHARS.sub("", value)
                value = "\n".join(_WS.sub(" ", line).strip() for line in value.splitlines()).strip()
                if len(value) > self.max_text_length:
                    self.add_error(name, _("Testo troppo lungo."))
                cleaned[name] = value
        return cleaned


class ConsentBooleanField(forms.BooleanField):
    """Mandatory consent checkbox; never pre-checked; label is the exact prescribed sentence."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", True)
        kwargs.setdefault("initial", False)
        kwargs.setdefault("error_messages", {"required": _("Il consenso è obbligatorio per inviare la richiesta.")})
        super().__init__(*args, **kwargs)
        self.widget.attrs.setdefault("class", "consent-checkbox")
