from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import Organisation
from core import clock
from core.forms import PublicFormMixin
from documents import services
from documents.models import DocumentKind


class DocumentUploadForm(PublicFormMixin, forms.Form):
    """Authenticated upload form (reserved area): validation delegates to documents.services."""

    file = forms.FileField(
        label=_("Fichier"),
        help_text=_("PDF, JPEG ou PNG — 10 Mo maximum."),
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"}),
    )
    kind = forms.ChoiceField(label=_("Type de document"), choices=DocumentKind.choices, initial=DocumentKind.OTHER)
    description = forms.CharField(
        label=_("Description"),
        max_length=200,
        required=False,
        help_text=_("Facultatif — 200 caractères maximum. N’indiquez aucune donnée sensible."),
    )
    organisation = forms.ModelChoiceField(
        label=_("Organisation concernée"),
        queryset=Organisation.objects.none(),
        required=False,
        empty_label=_("— aucune (document personnel) —"),
    )

    max_text_length = 200

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["organisation"].queryset = Organisation.objects.filter(memberships__user=user).distinct()
        self.validated_upload: services.ValidatedUpload | None = None

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        self.validated_upload = services.validate_upload(uploaded)
        return uploaded


class RequirementUploadForm(PublicFormMixin, forms.Form):
    """
    Deposit a file against ONE named requirement.

    The requirement is not a field: it is in the URL and re-checked by the policy, so no form post
    can move a file to somebody else's requirement by editing a hidden input.

    ``expires_on`` is asked for because a document with no known validity cannot expire on its own,
    and a register that cannot say "expired" is a register that quietly goes stale. It is optional:
    many pieces have no end date, and inventing one would be worse than leaving it blank.
    """

    file = forms.FileField(
        label=_("Fichier"),
        help_text=_("PDF, JPEG ou PNG — 10 Mo maximum."),
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"}),
    )
    expires_on = forms.DateField(
        label=_("La pièce est valable jusqu’au"),
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text=_("Facultatif. Renseignez-la si la pièce porte une date de fin de validité."),
    )

    max_text_length = 200

    def __init__(self, *args, requirement, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirement = requirement
        self.user = user
        self.validated_upload: services.ValidatedUpload | None = None

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        self.validated_upload = services.validate_upload(uploaded)
        return uploaded

    def clean_expires_on(self):
        value = self.cleaned_data.get("expires_on")
        if value and value < clock.today():
            # Accepting a date already past would file a piece that is EXPIRÉ the instant it lands.
            raise forms.ValidationError(_("Cette date est déjà passée : la pièce ne serait pas valable."))
        return value


class RequirementReviewForm(PublicFormMixin, forms.Form):
    """
    A human decision on the version in force. Deliberately small, and deliberately not the person's.

    ``note`` is mandatory for a refusal and for a replacement request: "non valide" with no motive
    is an instruction to guess, given to the one party with the least information.
    """

    ACCEPT = "accept"
    REFUSE = "refuse"
    REVIEW = "review"
    REPLACE = "replace"
    DECISIONS = (
        (REVIEW, _("Prendre la pièce en examen")),
        (ACCEPT, _("La pièce correspond à ce qui était demandé")),
        (REFUSE, _("La pièce n’est pas retenue")),
        (REPLACE, _("Demander une pièce de remplacement")),
    )

    decision = forms.ChoiceField(label=_("Examen"), choices=DECISIONS, widget=forms.RadioSelect)
    note = forms.CharField(
        label=_("Motif"),
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text=_("Obligatoire pour un refus ou une demande de remplacement. Aucune donnée sensible."),
    )

    max_text_length = 300

    def clean(self):
        cleaned = super().clean()
        decision = cleaned.get("decision")
        note = (cleaned.get("note") or "").strip()
        if decision in {self.REFUSE, self.REPLACE} and not note:
            self.add_error("note", _("Indiquez le motif : la personne doit savoir quoi faire ensuite."))
        return cleaned
