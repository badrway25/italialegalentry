"""
Forms of the digital help desk.

All four are small on purpose. The previous platform replaced this whole surface with one free-text
box wired to a language model; the answer is not a bigger box, it is a short, honest form whose
fields do work and whose help text says what will happen to what you write.

``OpenRequestForm`` builds its case choices from the signed-in person's OWN case files — the
queryset is the authorisation, so a posted identifier belonging to somebody else simply is not a
valid choice.
"""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

BODY_MAX = 4000


class OpenRequestForm(forms.Form):
    """What the person asks, and which file it concerns."""

    subject = forms.CharField(
        label=_("Objet de votre demande"),
        max_length=200,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        help_text=_("Une ligne. Par exemple : « Durée de validité de mon attestation de langue »."),
    )
    case = forms.ModelChoiceField(
        label=_("Dossier concerné"),
        queryset=None,
        required=False,
        empty_label=_("Aucun dossier en particulier"),
        help_text=_("Rattacher la demande à un dossier aide la personne qui l’examinera."),
    )
    question = forms.CharField(
        label=_("Votre question"),
        max_length=BODY_MAX,
        widget=forms.Textarea(attrs={"rows": 8}),
        help_text=_(
            "Écrivez votre question dans la langue de votre choix. Aucune réponse n’est produite "
            "automatiquement : ce texte est lu par une personne. N’indiquez pas de données de santé, "
            "de religion ou d’opinion — elles ne sont pas nécessaires et ne doivent pas être conservées."
        ),
    )
    professional_review = forms.BooleanField(
        label=_("Je demande une vérification par un professionnel"),
        required=False,
        help_text=_(
            "À cocher si votre situation dépasse ce que l’orientation peut établir. "
            "Un délai s’ensuit : un professionnel doit être désigné."
        ),
    )

    def __init__(self, *args, person=None, **kwargs):
        super().__init__(*args, **kwargs)
        from cases.models import CaseFile

        queryset = CaseFile.objects.none() if person is None else CaseFile.objects.filter(person=person)
        self.fields["case"].queryset = queryset.order_by("-created_at")
        if not queryset.exists():
            # No file, no field: an empty select that explains nothing is noise.
            del self.fields["case"]

    def clean_question(self) -> str:
        value = self.cleaned_data["question"].strip()
        if len(value) < 10:
            raise forms.ValidationError(_("Décrivez votre question en une phrase au moins."))
        return value


class MessageForm(forms.Form):
    """One turn of the exchange, written by whoever is signed in."""

    body = forms.CharField(
        label=_("Votre message"),
        max_length=BODY_MAX,
        widget=forms.Textarea(attrs={"rows": 6}),
    )

    def clean_body(self) -> str:
        value = self.cleaned_data["body"].strip()
        if not value:
            raise forms.ValidationError(_("Un message vide n’est pas un message."))
        return value


class ResponseForm(MessageForm):
    """The professional's reply. The person reads it with its date and the responder's function."""

    body = forms.CharField(
        label=_("Réponse transmise à la personne"),
        max_length=BODY_MAX,
        widget=forms.Textarea(attrs={"rows": 10}),
        help_text=_(
            "Ce texte est lu par la personne, daté et attribué à votre fonction, jamais à votre nom. "
            "Il ne constitue ni une décision ni une garantie de résultat."
        ),
    )


class AssignForm(forms.Form):
    """Designating a professional and stating the mandate, in one act."""

    professional = forms.ModelChoiceField(
        label=_("Professionnel désigné"),
        queryset=None,
        help_text=_("Seuls les comptes portant le rôle « Professionnel » figurent ici."),
    )
    role_label = forms.CharField(
        label=_("Fonction affichée à la personne"),
        max_length=120,
        help_text=_("Par exemple : « Avocat — droit de l’immigration ». Jamais un nom de personne."),
    )
    mandate_note = forms.CharField(
        label=_("Contexte du mandat"),
        max_length=300,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Ce que le professionnel est chargé d’examiner. Obligatoire."),
    )
    valid_until = forms.DateField(
        label=_("Mandat valable jusqu’au"),
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text=_("Au-delà de cette date, l’accès du professionnel à la demande cesse."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model

        from accounts import roles

        self.fields["professional"].queryset = (
            get_user_model().objects.filter(is_active=True, groups__name=roles.PROFESSIONAL).order_by("email")
        )

    def clean_mandate_note(self) -> str:
        value = self.cleaned_data["mandate_note"].strip()
        if len(value) < 10:
            raise forms.ValidationError(_("Un mandat se formule : indiquez ce qui doit être examiné."))
        return value


class CloseForm(forms.Form):
    """Closing is final, so it is a deliberate act with a stated reason."""

    reason = forms.CharField(
        label=_("Motif de clôture"),
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Visible par la personne. Une demande close n’est pas rouverte."),
    )
