from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from community import conf
from community.models import ModerationActionKind, ParticipantCategory
from core.forms import ConsentBooleanField, PublicFormMixin


class JoinForm(PublicFormMixin, forms.Form):
    """Membership request: category (prescribed labels), optional organisation, visibility, consent."""

    category = forms.ChoiceField(choices=ParticipantCategory.choices)
    organisation = forms.CharField(max_length=200, required=False)
    show_name = forms.BooleanField(required=False, label=_("Afficher mon nom aux autres membres"))
    show_organisation = forms.BooleanField(required=False, label=_("Afficher mon organisme aux autres membres"))
    consent = ConsentBooleanField()

    def __init__(self, *args, consent_text: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].label = locked_content.text("p2.forum.registration.category_label", "fr")
        self.fields["organisation"].label = locked_content.get("p2.forum.registration.fields", "fr")[0][2]
        self.fields["consent"].label = consent_text
        self.fields["show_name"].help_text = _(
            "Désactivé par défaut : rien vous concernant n’est visible sans votre choix."
        )


class DiscussionForm(PublicFormMixin, forms.Form):
    max_text_length = 8000

    title = forms.CharField(max_length=200, label=_("Titre de la discussion"))
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6}),
        label=_("Votre message"),
        help_text=_("Texte simple ; aucune donnée personnelle de tiers."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_text_length = conf.max_post_length()
        self.fields["body"].max_length = self.max_text_length


class PostForm(PublicFormMixin, forms.Form):
    max_text_length = 8000

    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label=_("Votre réponse"),
        help_text=_("Texte simple ; aucune donnée personnelle de tiers."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_text_length = conf.max_post_length()
        self.fields["body"].max_length = self.max_text_length


class ReportForm(PublicFormMixin, forms.Form):
    max_text_length = 2000

    reason = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        max_length=2000,
        label=_("Motif du signalement"),
    )


class PostModerationForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            (ModerationActionKind.APPROVE, ModerationActionKind.APPROVE.label),
            (ModerationActionKind.HIDE, ModerationActionKind.HIDE.label),
            (ModerationActionKind.UNHIDE, ModerationActionKind.UNHIDE.label),
        ]
    )
    note = forms.CharField(max_length=300, required=False, label=_("Note (interne)"))


class DiscussionModerationForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            (ModerationActionKind.CLOSE, ModerationActionKind.CLOSE.label),
            (ModerationActionKind.REOPEN, ModerationActionKind.REOPEN.label),
            (ModerationActionKind.HIDE, ModerationActionKind.HIDE.label),
            (ModerationActionKind.UNHIDE, ModerationActionKind.UNHIDE.label),
        ]
    )
    note = forms.CharField(max_length=300, required=False, label=_("Note (interne)"))
