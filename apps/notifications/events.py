"""
The closed registry of notification events — what the platform tells people about, and how.

A notification is a promise. When the reserved area says « vous serez prévenu », the list of things
the person will be prevented about has to be finite, reviewable and identical whichever entry point
fires it: a view, the admin, a management command or a future API. So the events live here, one
constant per event, and ``notify()`` refuses a key that is not in this table. A registry that can be
extended at the call site is not a registry, it is a naming convention.

Three properties are enforced by the shape of the data rather than by the discipline of whoever
writes the next call site:

1. **A subject is a CONSTANT of its event, never a rendering of its context.** Mail subjects travel
   between servers in the clear, are copied into bounce reports, spam-filter logs and phone
   notification banners, and survive on devices nobody in this project controls. « Pièce refusée :
   passeport_amina_2024.pdf » on a lock screen discloses both the person and what they are doing,
   to whoever is looking at the phone. The detail therefore belongs to the BODY, which reaches the
   account's own inbox and the reserved area, and the subject says only what kind of thing happened.
   ``test_no_personal_data_in_subjects`` holds the line: a subject carrying a placeholder fails.

2. **Whether an event warrants an e-mail is a FIELD, not an ``if``.** The decision is a judgement
   about attention, not about code paths, and it has to be readable by someone who does not read
   Python — which is who will be asked whether the platform sends too much mail. ``email_note``
   carries the reasoning next to the decision, because "why does this one not send mail" is the
   question that gets asked six months later, and an undocumented False invites someone to flip it.

3. **The French source text lives here.** The body of a notification is institutional writing about
   somebody's file; it is reviewed as text, in one place, and translated through the catalogues like
   the rest of the platform. Scattering it across templates would mean nobody could answer "what
   exactly do we say to people?" without reading ten files.

In-app delivery has no switch: see ``NotificationPreference``. The person can silence the e-mail,
never the record.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------------------------
# Categories — the granularity at which a person may switch e-mail off
# ---------------------------------------------------------------------------------------------
#: Deliberately coarse. A preference screen with twenty switches is a screen nobody configures, and
#: an unconfigured preference is the platform deciding for the person. Each category is a kind of
#: thing that happens, not a technical event: "mon dossier avance", "j'ai une échéance", "une pièce
#: pose problème", "l'équipe m'écrit", "mes accès changent".
CATEGORY_CASE = "case"
CATEGORY_DEADLINE = "deadline"
CATEGORY_DOCUMENT = "document"
CATEGORY_MESSAGE = "message"
CATEGORY_ASSIGNMENT = "assignment"

CATEGORY_LABELS: dict[str, str] = {
    CATEGORY_CASE: _("Suivi du dossier"),
    CATEGORY_DEADLINE: _("Échéances"),
    CATEGORY_DOCUMENT: _("Pièces justificatives"),
    CATEGORY_MESSAGE: _("Messages de l’équipe"),
    CATEGORY_ASSIGNMENT: _("Accès et mandats"),
}

CATEGORIES: tuple[str, ...] = tuple(CATEGORY_LABELS)


class UnknownEvent(KeyError):
    """A key that is not in the registry. Raised loudly: a silent no-op is a notification never sent."""


class MissingContext(ValueError):
    """A body that cannot be filled. A notification with a hole in it is worse than none at all."""


@dataclass(frozen=True)
class NotificationEvent:
    """One declared event: what it is about, what it says, and whether it is worth an e-mail."""

    key: str
    category: str
    #: Constant, personal-data-free, used for BOTH the in-app subject and the mail subject.
    subject_fr: str
    #: French source text with ``{placeholder}`` slots, filled from the declared ``fields``.
    body_fr: str
    #: Does this event warrant leaving the platform and landing in somebody's mailbox?
    email: bool
    #: Why — in one sentence, for the person who will ask whether we send too much or too little.
    email_note: str
    #: The context keys the body needs. Missing one is an error, never an empty line in the text.
    fields: tuple[str, ...] = ()

    def render_body(self, context: dict | None = None) -> str:
        """
        Fill the French source text, or refuse.

        Refusing is the point: a body rendered with a blank where the case reference should be looks
        like a broken system to the person reading it, and like a success to the code that sent it.
        """
        context = context or {}
        missing = [name for name in self.fields if not str(context.get(name, "") or "").strip()]
        if missing:
            raise MissingContext(f"{self.key}: missing context {', '.join(sorted(missing))}")
        return self.body_fr.format(**{name: context[name] for name in self.fields}).strip()


def _event(**kwargs) -> NotificationEvent:
    event = NotificationEvent(**kwargs)
    # A placeholder in a subject is how personal data reaches a mail server's logs. Checked when the
    # registry is built rather than left to review, because review is where this kind of thing slips
    # through. ``str()`` resolves the lazy translation; the stored attribute stays lazy.
    if "{" in str(event.subject_fr):
        raise ValueError(f"{event.key}: a subject is a constant, not a template")
    if event.category not in CATEGORIES:
        raise ValueError(f"{event.key}: unknown category {event.category}")
    return event


# ---------------------------------------------------------------------------------------------
# The events
# ---------------------------------------------------------------------------------------------
CASE_OPENED = "case.opened"
CASE_TRANSITIONED = "case.transitioned"
CASE_ASSESSED = "case.assessed"
CHECKLIST_DUE_SOON = "checklist.due_soon"
CHECKLIST_OVERDUE = "checklist.overdue"
DOCUMENT_REJECTED = "document.rejected"
DOCUMENT_EXPIRED = "document.expired"
TEAM_MESSAGE = "team.message"
ASSIGNMENT_GRANTED = "assignment.granted"
ASSIGNMENT_REVOKED = "assignment.revoked"

EVENTS: dict[str, NotificationEvent] = {
    event.key: event
    for event in (
        _event(
            key=CASE_OPENED,
            category=CATEGORY_CASE,
            subject_fr=_("Ouverture d’un dossier"),
            body_fr=_(
                "Un dossier a été ouvert à votre nom.\n\n"
                "Référence : {case_reference}\n"
                "Objet : {purpose}\n\n"
                "Vous en suivez l’avancement dans votre espace réservé. "
                "L’ouverture d’un dossier n’est pas une demande déposée auprès d’une administration "
                "et ne préjuge d’aucune décision."
            ),
            fields=("case_reference", "purpose"),
            email=False,
            email_note=_(
                "Pas d’e-mail : le dossier s’ouvre pendant que la personne est devant l’écran qui "
                "l’ouvre. Un message qui annonce ce que l’on vient de faire soi-même apprend à ne "
                "plus lire les messages."
            ),
        ),
        _event(
            key=CASE_TRANSITIONED,
            category=CATEGORY_CASE,
            subject_fr=_("Mise à jour de votre dossier"),
            body_fr=_(
                "L’état de votre dossier a changé.\n\n"
                "Référence : {case_reference}\n"
                "Nouvel état : {status}\n"
                "État précédent : {previous_status}\n\n"
                "Le détail et la prochaine étape figurent dans votre espace réservé."
            ),
            fields=("case_reference", "status", "previous_status"),
            email=True,
            email_note=_(
                "E-mail : un dossier change d’état pendant que la personne est ailleurs, parfois des "
                "semaines après sa dernière connexion."
            ),
        ),
        _event(
            key=CASE_ASSESSED,
            category=CATEGORY_CASE,
            subject_fr=_("Nouvelle pré-évaluation enregistrée"),
            body_fr=_(
                "Une pré-évaluation a été enregistrée sur votre dossier.\n\n"
                "Référence : {case_reference}\n"
                "Résultat : {outcome}\n"
                "Règles appliquées : version {ruleset_version} du référentiel\n\n"
                "Une pré-évaluation est une orientation motivée et sourcée, jamais une décision "
                "administrative. Les sources citées sont consultables dans votre espace réservé."
            ),
            fields=("case_reference", "outcome", "ruleset_version"),
            email=False,
            email_note=_(
                "Pas d’e-mail : une pré-évaluation est enregistrée dans la même requête que le "
                "questionnaire ou la mise à jour de situation qui la déclenche — elle est déjà à "
                "l’écran. Quand l’équipe en enregistre une depuis le back-office, elle accompagne le "
                "dossier d’un message, qui, lui, part par e-mail."
            ),
        ),
        _event(
            key=CHECKLIST_DUE_SOON,
            category=CATEGORY_DEADLINE,
            subject_fr=_("Une échéance approche"),
            body_fr=_(
                "Une exigence de votre dossier arrive à échéance.\n\n"
                "Dossier : {case_reference}\n"
                "Exigence : {requirement}\n"
                "Échéance : {due_date} (dans {days} jour(s))\n"
                "Responsable : {responsible}\n\n"
                "La date indiquée est celle inscrite au dossier par l’équipe à partir d’une source "
                "écrite ; la plateforme ne calcule aucun délai légal."
            ),
            fields=("case_reference", "requirement", "due_date", "days", "responsible"),
            email=True,
            email_note=_("E-mail : prévenir après la date n’est plus prévenir, c’est constater."),
        ),
        _event(
            key=CHECKLIST_OVERDUE,
            category=CATEGORY_DEADLINE,
            subject_fr=_("Une échéance est dépassée"),
            body_fr=_(
                "Une exigence de votre dossier a dépassé sa date.\n\n"
                "Dossier : {case_reference}\n"
                "Exigence : {requirement}\n"
                "Échéance : {due_date} (dépassée de {days} jour(s))\n"
                "Responsable : {responsible}\n\n"
                "Un retard ne ferme pas le dossier. Si la date n’est plus la bonne, signalez-le à "
                "l’équipe depuis votre espace réservé."
            ),
            fields=("case_reference", "requirement", "due_date", "days", "responsible"),
            email=True,
            email_note=_("E-mail : c’est l’information qui coûte le plus cher à découvrir trop tard."),
        ),
        _event(
            key=DOCUMENT_REJECTED,
            category=CATEGORY_DOCUMENT,
            subject_fr=_("Une pièce n’a pas été acceptée"),
            body_fr=_(
                "Une pièce déposée n’a pas été retenue en l’état.\n\n"
                "Dossier : {case_reference}\n"
                "Pièce demandée : {requirement}\n"
                "Motif : {reason}\n\n"
                "Un refus porte sur la pièce reçue, jamais sur la personne. Vous pouvez en déposer "
                "une nouvelle version depuis votre espace réservé."
            ),
            fields=("case_reference", "requirement", "reason"),
            email=True,
            email_note=_("E-mail : le dossier est arrêté tant que rien n’est redéposé."),
        ),
        _event(
            key=DOCUMENT_EXPIRED,
            category=CATEGORY_DOCUMENT,
            subject_fr=_("Une pièce est arrivée à expiration"),
            body_fr=_(
                "Une pièce de votre dossier a atteint sa date de validité.\n\n"
                "Dossier : {case_reference}\n"
                "Pièce demandée : {requirement}\n"
                "Valable jusqu’au : {valid_until}\n\n"
                "Une pièce expire d’elle-même : personne ne l’a retirée de votre dossier."
            ),
            fields=("case_reference", "requirement", "valid_until"),
            email=True,
            email_note=_("E-mail : rien à l’écran ne bouge le jour de l’expiration, il faut aller le dire."),
        ),
        _event(
            key=TEAM_MESSAGE,
            category=CATEGORY_MESSAGE,
            subject_fr=_("Message de l’équipe du projet"),
            # Not translated: the body IS the text the team wrote, in the language it wrote it in.
            body_fr="{body}",
            fields=("body",),
            email=True,
            email_note=_(
                "E-mail : c’est un être humain qui écrit et qui attend une réponse. Le texte complet "
                "reste dans l’espace réservé ; l’e-mail en porte l’avis."
            ),
        ),
        _event(
            key=ASSIGNMENT_GRANTED,
            category=CATEGORY_ASSIGNMENT,
            subject_fr=_("Accès à un dossier accordé"),
            body_fr=_(
                "Un dossier vous a été confié.\n\n"
                "Dossier : {case_reference}\n"
                "Rôle : {role}\n"
                "Mandat valable jusqu’au : {valid_until}\n\n"
                "Votre accès prend fin à cette date sans intervention de personne."
            ),
            fields=("case_reference", "role", "valid_until"),
            email=True,
            email_note=_(
                "E-mail : un professionnel ne se connecte pas à l’espace réservé pour découvrir qu’on l’attend."
            ),
        ),
        _event(
            key=ASSIGNMENT_REVOKED,
            category=CATEGORY_ASSIGNMENT,
            subject_fr=_("Accès à un dossier retiré"),
            body_fr=_(
                "Votre accès à un dossier a pris fin.\n\n"
                "Dossier : {case_reference}\n"
                "Rôle : {role}\n\n"
                "Les travaux déjà versés au dossier y restent ; seul l’accès est retiré."
            ),
            fields=("case_reference", "role"),
            email=True,
            email_note=_("E-mail : perdre un accès doit s’apprendre autrement qu’en le découvrant fermé un matin."),
        ),
    )
}

#: The keys, in declaration order — for the admin, the preference screen and the tests.
EVENT_KEYS: tuple[str, ...] = tuple(EVENTS)


def get(key: str) -> NotificationEvent:
    """The declared event, or ``UnknownEvent``. The registry is closed on purpose."""
    try:
        return EVENTS[key]
    except KeyError as exc:
        raise UnknownEvent(f"unknown notification event {key!r}") from exc


def events_of(category: str) -> tuple[NotificationEvent, ...]:
    return tuple(event for event in EVENTS.values() if event.category == category)


def choices() -> list[tuple[str, str]]:
    """Model choices for the stored event key (callable, so models need not import at load time)."""
    return [(event.key, event.subject_fr) for event in EVENTS.values()]
