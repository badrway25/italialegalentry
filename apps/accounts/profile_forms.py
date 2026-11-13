"""
Forms of the self-service account area (authenticated users only — no honeypot/consent needed).
``accounts.forms`` keeps the allauth signup form; this module holds profile and deletion forms.
"""

from __future__ import annotations

import re

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.forms import PublicFormMixin


class LanguageSelect(forms.Select):
    """
    A language chooser whose options carry their OWN language.

    ``settings.LANGUAGES`` holds endonyms — « Français », « Italiano », « English », « العربية » —
    and an endonym is not a translatable string: it is that language's own name for itself, and it
    stays the same whatever language the page is in. Rendered without a ``lang`` attribute it is a
    French word sitting inside an English page, which a screen reader pronounces with the wrong
    voice and an automated check reads as an untranslated leak. The language switcher already tags
    each of its links; the form field did not.

    Arabic additionally needs ``dir``, or its name renders inside a left-to-right run.
    """

    LANGUAGE_DIRECTIONS = {"ar": "rtl"}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        code = str(value)
        if code:
            option["attrs"]["lang"] = code
            direction = self.LANGUAGE_DIRECTIONS.get(code)
            if direction:
                option["attrs"]["dir"] = direction
        return option


_PHONE_RE = re.compile(r"^\+?[0-9 ().-]{6,40}$")


class CountryField(forms.ChoiceField):
    """
    A country, chosen from the CLDR list in the visitor's language (V5.12 W2, DECISIONS §5.7): the stored value is the
    ISO 3166-1 alpha-2 code — what the rules engine reads (rules.engine: ``nationality`` and ``residence_country`` are
    ISO codes) — and the long list is a combobox over the native select (static/js/src/combobox.js). A value saved by
    the earlier free-text field is read back by its name in any of the four languages (core.countries.match).
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("choices", _country_choices)
        super().__init__(*args, **kwargs)


def _country_choices():
    from django.utils import translation

    from core import countries

    return [("", "—"), *countries.choices(translation.get_language() or "fr")]


def _country_initial(value: str) -> str:
    from core import countries

    return countries.match(value)


class ProfileForm(PublicFormMixin, forms.Form):
    # Each personal field says what it is for (WCAG 2.2 AA, 1.3.5 «identify input purpose» — W3-F2's accessibility
    # check, A2), as SignupForm's name does: a browser can fill it, assistive technology can name it. The telephone is
    # typed `tel` (the dialling keypad on a phone; base.css keeps it left to right on an Arabic page); the validation
    # stays the form's own (`clean_phone`).
    full_name = forms.CharField(
        label=_("Nom et prénom"),
        max_length=160,
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    preferred_language = forms.ChoiceField(
        label=_("Langue de communication"),
        choices=settings.LANGUAGES,
        widget=LanguageSelect(attrs={"autocomplete": "language"}),
    )
    phone = forms.CharField(
        label=_("Téléphone"),
        max_length=40,
        required=False,
        # V5.12 W2: «facultatif» is the label's tag now; the help's own «Facultatif —» stays until lane D's catalogue
        # pass gives the shorter sentence its translations (requested in docs/design-v5/QA/v512/b-w2/NOTES.md)
        help_text=_("Facultatif — utilisé uniquement pour le suivi de vos demandes."),
        widget=forms.TextInput(attrs={"type": "tel", "autocomplete": "tel", "inputmode": "tel"}),
    )
    country_of_residence = CountryField(
        label=_("Pays de résidence"),
        required=False,
        widget=forms.Select(attrs={"autocomplete": "country"}),
    )

    def __init__(self, *args, user=None, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not self.is_bound:
            self.fields["full_name"].initial = user.full_name
            self.fields["preferred_language"].initial = user.preferred_language
        if profile is not None and not self.is_bound:
            self.fields["phone"].initial = profile.phone
            self.fields["country_of_residence"].initial = _country_initial(profile.country_of_residence)

    def clean_phone(self) -> str:
        value = (self.cleaned_data.get("phone") or "").strip()
        if value and not _PHONE_RE.match(value):
            raise forms.ValidationError(_("Indiquez un numéro de téléphone valide (chiffres, espaces, +)."))
        return value


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label=_("Votre mot de passe actuel"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        strip=False,
    )
    confirm = forms.BooleanField(
        label=_("Je comprends que mon compte sera désactivé et mes données personnelles anonymisées."),
        required=True,
        initial=False,
        error_messages={"required": _("Veuillez confirmer votre demande.")},
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self) -> str:
        password = self.cleaned_data.get("password") or ""
        if not self.user.check_password(password):
            raise forms.ValidationError(_("Mot de passe incorrect."))
        return password


#: Languages a person may declare. Deliberately a short, closed list with an "other" escape: a free
#: text field here would collect dialect names, proficiency claims and occasionally a life story,
#: none of which any rule reads. The four project languages plus the two most common others.
DECLARABLE_LANGUAGES = (
    ("ar", _("Arabe")),
    ("fr", _("Français")),
    ("it", _("Italien")),
    ("en", _("Anglais")),
    ("es", _("Espagnol")),
    ("other", _("Autre")),
)

#: Answered as "not yet" rather than as False, because the two are different facts and only one of
#: them is an answer. A rule that reads ``has_job_offer`` must be able to tell "no" from "unknown".
TRISTATE = (("", _("Je ne sais pas encore")), ("yes", _("Oui")), ("no", _("Non")))


class SituationForm(PublicFormMixin, forms.Form):
    """
    What a person tells us about their situation, and why each answer is asked.

    Every field is optional and every field says what reads it. That is not politeness: the legal
    rule engine declares the facts a rule may consult, and a question whose answer no rule reads is
    personal data collected for no reason. If a field here cannot name what uses it, it should not
    be here.

    Nothing is inferred. A person who answers nothing still gets an orientation; it will be the one
    that can be given without knowing anything, which is the honest result rather than a guess
    dressed up as a finding.
    """

    # The two facts about the person whose purpose HTML names say what they are for (WCAG 2.2 AA, 1.3.5 «identify
    # input purpose» — W4-C's review, M1), as ProfileForm's personal fields do (W3-F2's A2): the date of birth is
    # `bday` (still typed `date`), the country of residence `country` (an ISO code since V5.12 W2).
    # The nationality has no purpose token.
    date_of_birth = forms.DateField(
        label=_("Date de naissance"),
        required=False,
        # an <input type="date"> holds only an ISO date: without the format, French and Italian drew 15/03/1994, the
        # field showed empty and the next save erased the date (V5.32 certification, 13 Nov 2026; companies/forms.py)
        widget=forms.DateInput(attrs={"type": "date", "autocomplete": "bday"}, format="%Y-%m-%d"),
        help_text=_("Certaines conditions d’entrée dépendent de l’âge. Les règles lisent l’âge, jamais la date."),
    )
    nationality = CountryField(
        label=_("Nationalité"),
        required=False,
        help_text=_("Les conditions d’entrée dépendent de la nationalité déclarée."),
    )
    country_of_residence = CountryField(
        label=_("Pays de résidence actuel"),
        required=False,
        widget=forms.Select(attrs={"autocomplete": "country"}),
        help_text=_("La démarche à suivre dépend du pays depuis lequel vous la commencez."),
    )
    education_level = forms.ChoiceField(
        label=_("Niveau d’études"),
        required=False,
        widget=forms.RadioSelect,
        help_text=_(
            "Sert à distinguer les voies qui supposent un titre de l’enseignement supérieur. "
            "Ce n’est pas une évaluation de votre dossier, et la plateforme ne reconnaît aucun diplôme."
        ),
    )
    years_of_experience = forms.IntegerField(
        label=_("Années d’expérience professionnelle"),
        required=False,
        min_value=0,
        max_value=60,
        help_text=_("Déclarées par vous. La plateforme ne les vérifie pas et ne les certifie pas."),
    )
    languages = forms.MultipleChoiceField(
        label=_("Langues que vous parlez"),
        required=False,
        choices=DECLARABLE_LANGUAGES,
        widget=forms.CheckboxSelectMultiple,
        help_text=_("Déclarées, jamais certifiées. Aucun niveau n’est demandé ici."),
    )
    has_job_offer = forms.ChoiceField(
        label=_("Avez-vous une proposition d’emploi en Italie ?"),
        required=False,
        choices=TRISTATE,
        widget=forms.RadioSelect,
        help_text=_("Oui ou non. Le nom de l’entreprise n’est pas demandé ici."),
    )
    has_qualification_recognition = forms.ChoiceField(
        label=_("Votre titre d’études a-t-il déjà été reconnu en Italie ?"),
        required=False,
        choices=TRISTATE,
        widget=forms.RadioSelect,
        # Worded so it does not repeat p3.diplomas.body: a prescribed text retyped here would drift
        # from the official version and would enter the translation catalogues, which is forbidden.
        help_text=_("Répondez oui seulement si la procédure a abouti auprès de l’autorité compétente."),
    )

    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import EducationLevel

        self.fields["education_level"].choices = [("", _("Non précisé")), *EducationLevel.choices]
        if profile is not None and not self.is_bound:
            self.fields["date_of_birth"].initial = profile.date_of_birth
            self.fields["nationality"].initial = _country_initial(profile.nationality)
            self.fields["country_of_residence"].initial = _country_initial(profile.country_of_residence)
            self.fields["education_level"].initial = profile.education_level
            self.fields["years_of_experience"].initial = profile.years_of_experience
            self.fields["languages"].initial = list(profile.languages or [])
            self.fields["has_job_offer"].initial = _tristate_value(profile.has_job_offer)
            self.fields["has_qualification_recognition"].initial = _tristate_value(
                profile.has_qualification_recognition
            )

    def clean_date_of_birth(self):
        from django.utils import timezone

        value = self.cleaned_data.get("date_of_birth")
        if value and value > timezone.localdate():
            raise forms.ValidationError(_("La date de naissance ne peut pas être dans le futur."))
        return value

    def to_profile_values(self) -> dict:
        """The cleaned answers as the profile stores them, with the tri-states turned back into None."""
        data = dict(self.cleaned_data)
        data["languages"] = list(data.get("languages") or [])
        data["has_job_offer"] = _tristate_to_bool(data.get("has_job_offer"))
        data["has_qualification_recognition"] = _tristate_to_bool(data.get("has_qualification_recognition"))
        return data


def _tristate_value(value) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return ""


def _tristate_to_bool(value):
    """ "" means the person has not answered — which is different from answering "no"."""
    if value == "yes":
        return True
    if value == "no":
        return False
    return None
