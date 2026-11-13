"""
Public registration form — fields EXACTLY in the prescribed order (document §2.1 INSCRIPTION):
Prénom — Nom — Organisme / Entreprise — Fonction — E-mail — Téléphone — Pays, then Catégorie
(select, eight prescribed options), Secteur d’intérêt (free text), mandatory consent.
"""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from core.forms import HONEYPOT_FIELD, TIMESTAMP_FIELD, ConsentBooleanField, HoneypotFormMixin, PublicFormMixin
from forum.models import RegistrationCategory

FIELD_NAMES = ("first_name", "last_name", "organisation", "role", "email", "phone", "country")
PUBLIC_FIELD_ORDER = (*FIELD_NAMES, "category", "sector_of_interest", "consent")


def _labels() -> list[str]:
    return list(locked_content.get("p2.forum.registration.fields", "fr")[0])


class ForumRegistrationForm(HoneypotFormMixin, PublicFormMixin, forms.Form):
    max_text_length = 300
    field_order = [*PUBLIC_FIELD_ORDER, HONEYPOT_FIELD, TIMESTAMP_FIELD]

    first_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"autocomplete": "given-name"}))
    last_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"autocomplete": "family-name"}))
    organisation = forms.CharField(
        max_length=200, required=False, widget=forms.TextInput(attrs={"autocomplete": "organization"})
    )
    role = forms.CharField(
        max_length=160, required=False, widget=forms.TextInput(attrs={"autocomplete": "organization-title"})
    )
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    phone = forms.CharField(max_length=40, required=False, widget=forms.TextInput(attrs={"autocomplete": "tel"}))
    country = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"autocomplete": "country-name"}))
    category = forms.ChoiceField(choices=[])
    sector_of_interest = forms.CharField(max_length=300, required=False)
    consent = ConsentBooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = _labels()
        for name, label in zip(FIELD_NAMES, labels, strict=True):
            self.fields[name].label = label
        self.fields["category"].label = locked_content.text("p2.forum.registration.category_label", "fr")
        self.fields["category"].choices = [("", _("Sélectionnez une catégorie")), *RegistrationCategory.choices]
        self.fields["sector_of_interest"].label = locked_content.text("p2.forum.registration.sector_label", "fr")
        self.fields["consent"].label = locked_content.text("p2.forum.registration.consent", "fr")
        self.fields[HONEYPOT_FIELD].label = _("Ne pas remplir ce champ")
        for name in PUBLIC_FIELD_ORDER:
            field = self.fields[name]
            field.widget.attrs.setdefault("id", f"id_forum_{name}")
            if field.required:
                field.widget.attrs["required"] = "required"
                field.widget.attrs["aria-required"] = "true"

    def public_fields(self):
        """Bound fields in the prescribed order, without the anti-spam controls."""
        return [self[name] for name in PUBLIC_FIELD_ORDER]

    def is_valid(self) -> bool:
        valid = super().is_valid()
        for name in PUBLIC_FIELD_ORDER:
            bound = self[name]
            if bound.errors:
                bound.field.widget.attrs["aria-invalid"] = "true"
                bound.field.widget.attrs["aria-describedby"] = f"{bound.id_for_label}_errors"
        return valid

    def clean_email(self) -> str:
        return (self.cleaned_data.get("email") or "").strip().lower()
