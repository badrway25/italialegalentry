"""
Forms of the company workspace.

Two rules shape every form here:

* the fields collected are the ones that DO WORK — a verification needs a legal name, a registration
  number and a named contact with a function; a need needs a territory, a métier, duties and skills.
  Nothing is collected because it would be nice to have;
* there is NO age field, and there will not be one. ``validate_no_age_criterion`` also refuses an
  age criterion typed into the free-text requirements, with an explanation rather than a bare
  rejection (Directive 2000/78/EC, D.lgs. 216/2003 — previous-platform audit, part 2 §3, kept in
  the private register).
"""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from companies.models import (
    CompanyNeed,
    CompanyProfile,
    Sector,
    Territory,
    validate_no_age_criterion,
)

SENSITIVE_DATA_HELP = _(
    "N’indiquez aucune donnée personnelle de tiers ni donnée sensible (santé, origine, opinions) dans ce champ."
)


class StyledModelForm(forms.ModelForm):
    """Applies the shared control class; the visual system is the site's, not this app's."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                continue
            widget.attrs.setdefault("class", "form-control")


class CompanyProfileForm(StyledModelForm):
    """
    The identity of the company — exactly what makes a verification possible.

    The previous platform collected these same fields and was right to: a verification that cannot
    name the legal entity, its registration and a responsible person with a function is not a
    verification.
    """

    # Declared rather than generated: Django 6.0 changes the default scheme of a URL field, and a
    # form that does not say which scheme it assumes is a form whose behaviour changes under it.
    website = forms.URLField(
        label=_("Site web"),
        required=False,
        assume_scheme="https",
        widget=forms.URLInput(attrs={"class": "form-control", "inputmode": "url"}),
    )

    class Meta:
        model = CompanyProfile
        fields = (
            "legal_name",
            "trade_name",
            "registration_number",
            "vat_number",
            "sector",
            "size",
            "year_founded",
            "contact_name",
            "contact_function",
            "contact_email",
            "contact_phone",
            "address_line",
            "postal_code",
            "city",
            "province",
            "country",
            "website",
        )
        widgets = {
            "legal_name": forms.TextInput(attrs={"autocomplete": "organization", "maxlength": 200}),
            "contact_name": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 160}),
            "contact_email": forms.EmailInput(attrs={"autocomplete": "email", "inputmode": "email"}),
            # V5.12 W2 (DECISIONS §5.16): every identity field says its purpose — organization, email, tel, the city
            "contact_phone": forms.TextInput(
                attrs={"type": "tel", "inputmode": "tel", "maxlength": 40, "autocomplete": "tel"}
            ),
            "contact_function": forms.TextInput(attrs={"autocomplete": "organization-title"}),
            "address_line": forms.TextInput(attrs={"autocomplete": "address-line1"}),
            "postal_code": forms.TextInput(attrs={"autocomplete": "postal-code"}),
            "city": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "province": forms.TextInput(attrs={"autocomplete": "address-level1"}),
            "year_founded": forms.NumberInput(attrs={"inputmode": "numeric", "min": 1800, "max": 2200}),
            # V5.12 W2 (DECISIONS §5.7): the two-letter code chosen from the CLDR list, a combobox over the select
            "country": forms.Select(attrs={"autocomplete": "country"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sector"].queryset = Sector.objects.active().ordered()
        self.fields["sector"].empty_label = _("— Choisir un secteur —")
        if "country" in self.fields:
            from django.utils import translation

            from core import countries

            self.fields["country"].widget.choices = countries.choices(translation.get_language() or "fr")
        for name in ("legal_name", "contact_name", "contact_function", "contact_email", "city"):
            self.fields[name].required = True


class CompanyNeedForm(StyledModelForm):
    """
    One expressed need. It describes the WORK.

    The skills are edited here as two ordered lines of text and stored as ``NeedSkill`` rows, so the
    Academy's skill gap (« required → held → gap → module ») has something to work with, while the
    company still types a list rather than filling a grid.
    """

    mandatory_skills = forms.CharField(
        label=_("Compétences obligatoires"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Une compétence par ligne. Ce sans quoi le poste ne peut pas être tenu."),
        validators=[validate_no_age_criterion],
    )
    preferred_skills = forms.CharField(
        label=_("Compétences souhaitées"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Une compétence par ligne. Ce qui serait un atout, sans être une condition."),
        validators=[validate_no_age_criterion],
    )

    class Meta:
        model = CompanyNeed
        fields = (
            "title",
            "territory",
            "work_place",
            "sector",
            "professional_profile",
            "duties",
            "motivation",
            "engagement_type",
            "headcount",
            "experience_years_min",
            "experience_note",
            "language_code",
            "language_level",
            "language_note",
            "safety_training_required",
            "safety_training_note",
            "training_needs",
            "start_from",
            "timing_note",
        )
        widgets = {
            "duties": forms.Textarea(attrs={"rows": 4}),
            "motivation": forms.Textarea(attrs={"rows": 3}),
            "training_needs": forms.Textarea(attrs={"rows": 3}),
            "headcount": forms.NumberInput(attrs={"inputmode": "numeric", "min": 1, "max": 999}),
            "experience_years_min": forms.NumberInput(attrs={"inputmode": "numeric", "min": 0, "max": 45}),
            "start_from": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
        help_texts = {"duties": SENSITIVE_DATA_HELP}

    #: The four steps of the need and its review (V5.15 W3, lane B; DECISIONS §5.12): the groups the page already
    #: drew as fieldsets — under the legends they already had («Le poste et son territoire», «Compétences attendues»:
    #: translated words, kept), asked one at a time (static/js/src/steps.js; without script, the four in sequence). The
    #: skills fields are this form's own (declared above): named here so that they stay in their step.
    steps = (
        (
            "poste",
            _("Le poste et son territoire"),
            "ile-need",
            (
                "title",
                "territory",
                "work_place",
                "sector",
                "professional_profile",
                "duties",
                "motivation",
                "engagement_type",
                "headcount",
            ),
        ),
        (
            "competences",
            _("Compétences attendues"),
            "clipboard-list",
            ("mandatory_skills", "preferred_skills", "experience_years_min", "experience_note"),
        ),
        (
            "langue",
            _("Langue et sécurité"),
            "languages",
            ("language_code", "language_level", "language_note", "safety_training_required", "safety_training_note"),
        ),
        ("calendrier", _("Formation et calendrier"), "presentation", ("training_needs", "start_from", "timing_note")),
        ("verification", _("Vérification"), "ile-review", ()),
    )
    #: The last step opens on the review: what the company typed, step by step, each with its way back.
    steps_review = True
    #: Round 2: the language and its level share a row (two short selects, next to each other in the order).
    steps_pairs = (("language_code", "language_level"),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["territory"].queryset = Territory.objects.active().ordered()
        self.fields["sector"].queryset = Sector.objects.active().ordered()
        self.fields["territory"].empty_label = _("— Choisir un territoire —")
        self.fields["sector"].empty_label = _("— Choisir un secteur —")
        # Worded empty options: « --------- » tells a reader nothing about what leaving a field
        # empty means, and these three fields all mean something specific when left empty.
        self.fields["language_code"].choices = [
            ("", _("— Aucune langue formellement exigée —")),
            *list(self.fields["language_code"].choices)[1:],
        ]
        self.fields["engagement_type"].choices = [
            ("", _("— Forme non encore arrêtée —")),
            *list(self.fields["engagement_type"].choices)[1:],
        ]
        if self.instance.pk:
            self.fields["mandatory_skills"].initial = "\n".join(row.label for row in self.instance.mandatory_skills())
            self.fields["preferred_skills"].initial = "\n".join(row.label for row in self.instance.preferred_skills())

    @staticmethod
    def _lines(value: str) -> list[str]:
        return [line.strip() for line in (value or "").splitlines() if line.strip()]

    def cleaned_mandatory(self) -> list[str]:
        return self._lines(self.cleaned_data.get("mandatory_skills", ""))

    def cleaned_preferred(self) -> list[str]:
        return self._lines(self.cleaned_data.get("preferred_skills", ""))

    def model_data(self) -> dict:
        """The cleaned values that belong to the model (the skills are stored separately)."""
        return {name: self.cleaned_data[name] for name in self.Meta.fields}


class WithdrawForm(forms.Form):
    reason = forms.CharField(
        label=_("motif du retrait"),
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
