"""
Forms of the governance module. They validate INPUT; they never decide a state.

A form here may say « ce champ est obligatoire ». It may not say « cette proposition passe en
examen »: that sentence belongs to ``governance_services.transition_proposal``, which checks the
declared transition table, the caller's capacity and the motivation, and writes the audit row.
The transition form therefore collects a target and a note and hands both to the service — the
choices it offers are the ones the service would accept, computed by the service itself.
"""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from forum.governance import Commission, ForumProposal, Table, TableStatus


class ProposalForm(forms.ModelForm):
    """Draft a proposal inside ONE commission. The commission comes from the URL, never from POST."""

    class Meta:
        model = ForumProposal
        fields = ("table", "title_fr", "body_fr")
        labels = {
            "table": _("Table thématique"),
            "title_fr": _("Intitulé de la proposition"),
            "body_fr": _("Texte de la proposition"),
        }
        help_texts = {
            "table": _("Facultatif : la table où la proposition est élaborée."),
            "body_fr": _(
                "Décrivez l’objet, les parties concernées et le résultat attendu. "
                "N’indiquez aucune donnée personnelle : la proposition est lue par toute la commission."
            ),
        }
        widgets = {"body_fr": forms.Textarea(attrs={"rows": 10})}

    def __init__(self, *args, commission: Commission, **kwargs):
        super().__init__(*args, **kwargs)
        self.commission = commission
        self.fields["table"].queryset = Table.objects.filter(
            commission=commission, status__in=[TableStatus.OPEN, TableStatus.CONSOLIDATING]
        )
        self.fields["table"].required = False
        self.fields["table"].empty_label = _("Aucune table")

    def clean_title_fr(self) -> str:
        title = (self.cleaned_data.get("title_fr") or "").strip()
        if len(title) < 8:
            raise forms.ValidationError(_("Donnez un intitulé explicite (au moins huit caractères)."))
        return title

    def clean_body_fr(self) -> str:
        body = (self.cleaned_data.get("body_fr") or "").strip()
        if len(body) < 40:
            raise forms.ValidationError(
                _("Une proposition doit être suffisamment développée pour être examinée par la commission.")
            )
        return body


class ProposalTransitionForm(forms.Form):
    """
    The state change asked for by a human.

    ``choices`` are the transitions the caller may ACTUALLY ask for, computed by
    ``governance_services.available_transitions``: a screen that offers a button the domain will
    refuse teaches people to distrust the screen.
    """

    target = forms.ChoiceField(label=_("Nouvel état"), choices=())
    note = forms.CharField(
        label=_("Motif de la décision"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text=_("Obligatoire pour retenir ou écarter une proposition."),
    )

    def __init__(self, *args, transitions: list[dict], **kwargs):
        super().__init__(*args, **kwargs)
        self.transitions = transitions
        self.fields["target"].choices = [(row["value"], row["label"]) for row in transitions]
        self._needs_note = {row["value"] for row in transitions if row["needs_note"]}

    def clean(self):
        data = super().clean()
        target = data.get("target")
        note = (data.get("note") or "").strip()
        if target in self._needs_note and not note:
            # The service refuses this too. Catching it here means the person is told in the form,
            # next to the field, instead of being shown a 400 after the fact.
            self.add_error("note", _("Une décision doit être motivée."))
        data["note"] = note
        return data
