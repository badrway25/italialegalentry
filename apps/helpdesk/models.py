"""
Sportello digitale — the digital help desk.

This module is the deliberate opposite of what the previous platform shipped. There, a button on
every screen opened a third-party language model that offered to answer «tout sur les visas
proposés, les documents à fournir», with no sources, no versioning, no human review and the API key
stored as the platform's single administrable setting
(previous-platform audit, part 2 §7, private register).

Here there is no model, no generated answer and no key. There is a **ticket**: a question that
travels from automated orientation to a named, mandated professional, through seven declared states,
with an audit event at every step. What the person finally reads was typed by a human being who is
answerable for it.

Four invariants are enforced by the domain rather than drawn on a screen:

1. A transition that is not declared in ``ALLOWED_TRANSITIONS`` is refused (``services.transition``),
   exactly as ``cases.services.transition`` refuses one.
2. ``ASSIGNED``, ``IN_REVIEW`` and ``RESPONSE_AVAILABLE`` are unreachable without a **live** mandate:
   an assignment that has been revoked, or whose mandate has expired, grants nothing — neither the
   state nor the reading of the ticket.
3. ``RESPONSE_AVAILABLE`` is unreachable until a shared reply from the assignee actually exists. A
   state that announces an answer which is not there would be the interface lying about the domain.
4. ``CLOSED`` is terminal. A closed exchange is not reopened; a new request is opened, so the record
   of what was asked and what was answered, and when, stays honest.
5. No state outlives the thing it announces. When the mandate behind ``ASSIGNED`` or ``IN_REVIEW``
   ends — revoked, or simply run out on its date, which is nobody's action — the request returns to
   ``PROFESSIONAL_REVIEW_REQUIRED`` and reappears on the designation register. Otherwise the page
   goes on telling the person that a professional is examining their question while no account in
   the platform can open it.

Two things are deliberately absent from the data model, and their absence is the privacy design:
the **name of the professional** (the person reads a ROLE and a date) and any **free identity of the
person** on the professional's side (the professional reads a reference and the mandate context).
The exchange is between two roles, under a mandate, about a question.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class TicketStatus(models.TextChoices):
    """
    The seven states of Technical Blueprint v1.0 §13, and no others.

    Nothing here is an administrative determination and nothing here is an approval:
    ``RESPONSE_AVAILABLE`` means a human has written a reply, not that anything was granted.
    """

    INFORMATION_ONLY = "information_only", _("Information seulement")
    NEEDS_CLARIFICATION = "needs_clarification", _("Clarification nécessaire")
    PROFESSIONAL_REVIEW_REQUIRED = "professional_review_required", _("Vérification professionnelle requise")
    ASSIGNED = "assigned", _("Confiée à un professionnel")
    IN_REVIEW = "in_review", _("En cours d’examen")
    RESPONSE_AVAILABLE = "response_available", _("Réponse disponible")
    CLOSED = "closed", _("Close")


#: States in which the request is still live.
OPEN_STATUSES: frozenset[str] = frozenset(
    {
        TicketStatus.INFORMATION_ONLY,
        TicketStatus.NEEDS_CLARIFICATION,
        TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
        TicketStatus.ASSIGNED,
        TicketStatus.IN_REVIEW,
        TicketStatus.RESPONSE_AVAILABLE,
    }
)

#: Declared transitions. Anything absent here is refused by ``services.transition``.
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    TicketStatus.INFORMATION_ONLY: frozenset(
        {TicketStatus.NEEDS_CLARIFICATION, TicketStatus.PROFESSIONAL_REVIEW_REQUIRED, TicketStatus.CLOSED}
    ),
    TicketStatus.NEEDS_CLARIFICATION: frozenset(
        {
            TicketStatus.INFORMATION_ONLY,
            TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
            TicketStatus.IN_REVIEW,
            TicketStatus.CLOSED,
        }
    ),
    TicketStatus.PROFESSIONAL_REVIEW_REQUIRED: frozenset({TicketStatus.ASSIGNED, TicketStatus.CLOSED}),
    # ASSIGNED and IN_REVIEW can go BACK to «waiting for a professional». Without that return a
    # mandate that is revoked or simply runs out strands the request for good: the professional
    # stops seeing it, the designation register only ever looked at PROFESSIONAL_REVIEW_REQUIRED, and
    # the page went on telling the person «le professionnel désigné examine votre demande» about
    # somebody who could no longer open it. A state that outlives the thing it announces is the one
    # failure this module exists to prevent.
    TicketStatus.ASSIGNED: frozenset(
        {
            TicketStatus.IN_REVIEW,
            TicketStatus.NEEDS_CLARIFICATION,
            TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
            TicketStatus.CLOSED,
        }
    ),
    TicketStatus.IN_REVIEW: frozenset(
        {
            TicketStatus.NEEDS_CLARIFICATION,
            TicketStatus.RESPONSE_AVAILABLE,
            TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
            TicketStatus.CLOSED,
        }
    ),
    TicketStatus.RESPONSE_AVAILABLE: frozenset({TicketStatus.NEEDS_CLARIFICATION, TicketStatus.CLOSED}),
    TicketStatus.CLOSED: frozenset(),
}

#: States that require a mandate which is live TODAY. A lapsed mandate is not an authorisation.
REQUIRES_LIVE_MANDATE: frozenset[str] = frozenset(
    {TicketStatus.ASSIGNED, TicketStatus.IN_REVIEW, TicketStatus.RESPONSE_AVAILABLE}
)

#: States that require a reply the person can actually read.
REQUIRES_SHARED_RESPONSE: frozenset[str] = frozenset({TicketStatus.RESPONSE_AVAILABLE})

#: States that CLAIM somebody is working on the request. When the mandate behind one of these ends —
#: revoked, or simply run out on its date — the claim stops being true and the request is waiting for
#: a professional again. ``RESPONSE_AVAILABLE`` is deliberately NOT here: a reply that exists goes on
#: existing after the mandate lapses, so re-queueing it would tell an operator that a request needs a
#: professional when it already has its answer.
STRANDED_WITHOUT_MANDATE: frozenset[str] = frozenset({TicketStatus.ASSIGNED, TicketStatus.IN_REVIEW})

#: State → the modifier of the ``.state`` chip (static/css/register.css). Mapping, not invention:
#: the design system owns the five tones and there is deliberately no green, because no colour in
#: this platform ever means «approved». ``RESPONSE_AVAILABLE`` uses the *blue* done tone, which in
#: this system means «a fact is recorded», never «yes».
STATE_TONE: dict[str, str] = {
    TicketStatus.INFORMATION_ONLY: "filed",
    TicketStatus.NEEDS_CLARIFICATION: "missing",
    TicketStatus.PROFESSIONAL_REVIEW_REQUIRED: "review",
    TicketStatus.ASSIGNED: "review",
    TicketStatus.IN_REVIEW: "review",
    TicketStatus.RESPONSE_AVAILABLE: "done",
    TicketStatus.CLOSED: "",
}


def transitions_from(status: str) -> frozenset[str]:
    return ALLOWED_TRANSITIONS.get(status, frozenset())


class TicketOrigin(models.TextChoices):
    """Where the request came from. An escalation is not the same event as a question."""

    PERSON = "person", _("Demande de la personne")
    ASSESSMENT = "assessment", _("Résultat d’orientation appelant une vérification")
    PROJECT_TEAM = "project_team", _("Signalement de l’équipe du projet")


class ResponderRole(models.TextChoices):
    """
    WHO is speaking in the exchange. This is what the person reads instead of a name.

    A professional answers under a role and a mandate; publishing the individual's name on the
    person's side would add nothing to the answer and would expose a private individual to a
    correspondent they never chose.
    """

    PERSON = "person", _("La personne")
    PROFESSIONAL = "professional", _("Le professionnel désigné")
    PROJECT_TEAM = "project_team", _("L’équipe du projet")


class TicketQuerySet(models.QuerySet):
    def readable_by(self, user) -> TicketQuerySet:
        """
        Authorisation applied AT QUERY TIME.

        A ticket carries a person's legal question, which is among the most sensitive things this
        platform holds. Three consequences, all stricter than the case file:

        * ``role:staff`` gets nothing. Reading someone's question to a lawyer is not supervision.
        * ``role:operator`` gets nothing HERE. An operator dispatches requests and does not need to
          read them to do it, so dispatching has its own narrower queryset (``dispatchable_by``).
        * The assignee is scoped by a LIVE mandate. A revoked or expired mandate stops listing the
          ticket the same day, because a dated authorisation that keeps reading after its date is
          not an authorisation.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self
        today = timezone.localdate()
        mandated = models.Q(assignee=user, assignment_revoked_at__isnull=True) & (
            models.Q(mandate_valid_until__isnull=True) | models.Q(mandate_valid_until__gte=today)
        )
        return self.filter(models.Q(person=user) | mandated).distinct()

    def dispatchable_by(self, user) -> TicketQuerySet:
        """
        The dispatch register: requests waiting for a professional, for whoever may assign one.

        ``question`` is DEFERRED on purpose. Choosing which professional should look at a request
        needs its origin, its language and its date; it does not need the text of what the person
        asked, and a screen that shows it to every operator has widened the audience of a legal
        question for no operational gain.

        The deferral is data MINIMISATION, not a wall: Django fetches a deferred field on first
        access, so a template that printed ``ticket.question`` would still print it, at the cost of
        one extra query. What actually keeps the text off this screen is that the dispatch template
        never asks for it, and ``test_views`` asserts that against the RENDERED page rather than
        against the queryset. Said plainly here because a comment that overstates a defence is how a
        later reader ends up trusting one that is not there.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        if not (getattr(user, "is_superuser", False) or roles.has_role(user, roles.OPERATOR, roles.ADMINISTRATOR)):
            return self.none()
        today = timezone.localdate()
        # A request whose mandate has ENDED is, again, a request waiting for a professional — whether
        # the mandate was revoked or simply ran out on its date. Expiry is nobody's action, so no
        # code runs on the day it happens; if this register did not ask the question itself, such a
        # request would sit in ASSIGNED or IN_REVIEW with no one able to open it and no one able to
        # find it.
        lapsed = models.Q(status__in=STRANDED_WITHOUT_MANDATE) & (
            models.Q(assignee__isnull=True)
            | models.Q(assignment_revoked_at__isnull=False)
            | models.Q(mandate_valid_until__lt=today)
        )
        return self.filter(models.Q(status=TicketStatus.PROFESSIONAL_REVIEW_REQUIRED) | lapsed).defer("question")

    def open(self) -> TicketQuerySet:
        return self.filter(status__in=OPEN_STATUSES)

    def awaiting_assignment(self) -> TicketQuerySet:
        return self.filter(status=TicketStatus.PROFESSIONAL_REVIEW_REQUIRED)


class HelpdeskTicket(TimeStampedModel):
    """One request at the digital help desk, from automated orientation to a named professional."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(
        _("référence"),
        max_length=16,
        unique=True,
        editable=False,
        help_text=_("Référence courte citée dans les communications. Non séquentielle."),
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="helpdesk_tickets",
        verbose_name=_("personne"),
    )
    case = models.ForeignKey(
        "cases.CaseFile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="helpdesk_tickets",
        verbose_name=_("dossier"),
    )
    assessment = models.ForeignKey(
        "cases.PathwayAssessment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="helpdesk_tickets",
        verbose_name=_("évaluation à l’origine"),
        help_text=_("Le résultat REVIEW_REQUIRED qui a déclenché l’escalade, le cas échéant."),
    )
    origin = models.CharField(
        _("origine"), max_length=16, choices=TicketOrigin.choices, default=TicketOrigin.PERSON, db_index=True
    )
    subject = models.CharField(_("objet"), max_length=200)
    question = models.TextField(
        _("question"),
        help_text=_("Le texte écrit par la personne. Aucune réponse n’est jamais produite automatiquement."),
    )
    language = models.CharField(_("langue de la demande"), max_length=8, default="fr")

    status = models.CharField(
        _("état"),
        max_length=32,
        choices=TicketStatus.choices,
        default=TicketStatus.INFORMATION_ONLY,
        db_index=True,
    )
    status_since = models.DateTimeField(_("dans cet état depuis le"), default=timezone.now, editable=False)
    previous_status = models.CharField(
        _("état précédent"), max_length=32, choices=TicketStatus.choices, blank=True, editable=False
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="helpdesk_assignments",
        verbose_name=_("professionnel désigné"),
    )
    assignee_role_label = models.CharField(
        _("fonction affichée à la personne"),
        max_length=120,
        blank=True,
        help_text=_("Par exemple « Avocat — droit de l’immigration ». Jamais le nom d’une personne physique."),
    )
    mandate_note = models.CharField(
        _("contexte du mandat"),
        max_length=300,
        blank=True,
        help_text=_("Ce que le professionnel est chargé d’examiner. Obligatoire lors de la désignation."),
    )
    mandate_valid_until = models.DateField(_("mandat valable jusqu’au"), null=True, blank=True)
    assigned_at = models.DateTimeField(_("désigné le"), null=True, blank=True, editable=False)
    assignment_revoked_at = models.DateTimeField(_("mandat révoqué le"), null=True, blank=True, editable=False)

    closed_at = models.DateTimeField(_("close le"), null=True, blank=True, editable=False)
    closure_note = models.CharField(_("motif de clôture"), max_length=300, blank=True)

    class Meta:
        verbose_name = _("demande au guichet")
        verbose_name_plural = _("demandes au guichet")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["person", "status"]),
            models.Index(fields=["status", "status_since"]),
            models.Index(fields=["assignee", "status"]),
        ]
        constraints = [
            # One escalation per assessment: a second ticket for the same frozen outcome would be
            # two records of one event, and the person would be asked the same question twice.
            models.UniqueConstraint(
                fields=["assessment"],
                condition=models.Q(assessment__isnull=False),
                name="helpdesk_one_ticket_per_assessment",
            )
        ]

    objects = TicketQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.reference} · {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._new_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _new_reference() -> str:
        """Non-sequential, like the case reference: a counter would leak how many requests exist."""
        for _attempt in range(12):
            # ``proposal``, not the obvious noun: the compliance scan forbids recruitment
            # vocabulary anywhere in this module, and a scan that has to make an exception for a
            # harmless occurrence is a scan that will one day make one for a harmful occurrence.
            proposal = uuid.uuid4().hex[:10].upper()
            if not HelpdeskTicket.objects.filter(reference=proposal).exists():
                return proposal
        raise RuntimeError("could not allocate a unique helpdesk reference")

    # -- lifecycle ----------------------------------------------------------------------------
    @property
    def is_open(self) -> bool:
        return self.status in OPEN_STATUSES

    @property
    def is_read_only(self) -> bool:
        return self.status == TicketStatus.CLOSED

    @property
    def mandate_is_live(self) -> bool:
        """A mandate exists, has not been revoked and has not expired."""
        if self.assignee_id is None or self.assignment_revoked_at is not None:
            return False
        return not (self.mandate_valid_until and self.mandate_valid_until < timezone.localdate())

    @property
    def effective_status(self) -> str:
        """
        What is true TODAY, as opposed to what was last recorded.

        A mandate lapses on a date, and a date passing is nobody's action: no code runs that morning,
        so the stored ``status`` still reads ASSIGNED or IN_REVIEW while the professional named in it
        can no longer open the request. Reading the state through this property is the same discipline
        as ``mandate_is_live`` — compare with today rather than trust a flag somebody had to remember
        to set — and it means the page never announces work that nobody is doing. The stored value is
        left alone because it is the record of what was decided; ``services.assign`` and
        ``services.revoke_mandate`` write the transition as soon as anybody acts.
        """
        if self.status in STRANDED_WITHOUT_MANDATE and not self.mandate_is_live:
            return TicketStatus.PROFESSIONAL_REVIEW_REQUIRED
        return self.status

    @property
    def effective_status_display(self) -> str:
        """The word the interface shows. Never ``get_status_display`` — that one can be out of date."""
        return str(dict(TicketStatus.choices).get(self.effective_status, ""))

    @property
    def state_tone(self) -> str:
        return STATE_TONE.get(self.effective_status, "")

    def allowed_transitions(self) -> frozenset[str]:
        return transitions_from(self.status)

    def can_transition_to(self, target: str) -> bool:
        return target in self.allowed_transitions()

    def has_shared_response(self) -> bool:
        return self.messages.filter(kind=MessageKind.RESPONSE, visibility=MessageVisibility.SHARED).exists()

    def shared_messages(self):
        return self.messages.filter(visibility=MessageVisibility.SHARED).order_by("created_at", "id")

    def clean(self) -> None:
        if self.assignee_id and not self.mandate_note.strip():
            raise ValidationError({"mandate_note": _("Une désignation sans contexte de mandat n’est pas un mandat.")})
        if self.assignee_id and self.assignee_id == self.person_id:
            raise ValidationError({"assignee": _("Une personne ne peut pas être désignée pour sa propre demande.")})


class MessageKind(models.TextChoices):
    QUESTION = "question", _("Question")
    CLARIFICATION_REQUEST = "clarification_request", _("Demande de clarification")
    CLARIFICATION = "clarification", _("Clarification")
    RESPONSE = "response", _("Réponse")
    NOTE = "note", _("Note professionnelle")
    CLOSURE = "closure", _("Clôture")


class MessageVisibility(models.TextChoices):
    """
    SHARED is the exchange; INTERNAL is the professional's own note.

    ROLE_JOURNEYS §4: «Le note professionali non sono visibili alla persona salvo esplicita
    condivisione.» The distinction lives in the data and in the queryset, not in a template ``if``.
    """

    SHARED = "shared", _("Visible par la personne")
    INTERNAL = "internal", _("Note interne au professionnel")


class TicketMessageQuerySet(models.QuerySet):
    def readable_by(self, user) -> TicketMessageQuerySet:
        """
        Authorisation applied AT QUERY TIME, and narrower for an administrator than the ticket is.

        An administrator reads the TICKET (``TicketQuerySet.readable_by``) because the platform has
        to be administrable: states, mandates and dates are the shape of the work. The professional's
        INTERNAL NOTE is not part of that shape — it is privileged working material written under a
        mandate the administrator does not hold, and the audit trail already records that a note was
        written, by whom and how long it was, without its text. So an administrator reads the shared
        exchange and no internal note, which is exactly what ``policies.message_policy`` declares;
        the two defences have to say the same thing or the narrower one is decoration.

        An administrator who *is* the live assignee of a request reads its notes like any assignee:
        that comes from the mandate below, not from the role.
        """
        from accounts import roles

        if not getattr(user, "is_authenticated", False):
            return self.none()
        today = timezone.localdate()
        mandated = models.Q(ticket__assignee=user, ticket__assignment_revoked_at__isnull=True) & (
            models.Q(ticket__mandate_valid_until__isnull=True) | models.Q(ticket__mandate_valid_until__gte=today)
        )
        if getattr(user, "is_superuser", False) or roles.has_role(user, roles.ADMINISTRATOR):
            return self.filter(models.Q(visibility=MessageVisibility.SHARED) | mandated).distinct()
        return self.filter(models.Q(ticket__person=user, visibility=MessageVisibility.SHARED) | mandated).distinct()


class TicketMessage(TimeStampedModel):
    """
    One turn of the exchange, written by a human being.

    ``author_role`` is frozen at write time and is what the interface shows. There is no property
    on this model that returns the author's name, on purpose: a template cannot print what the
    model does not expose.
    """

    ticket = models.ForeignKey(
        HelpdeskTicket, on_delete=models.CASCADE, related_name="messages", verbose_name=_("demande")
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="helpdesk_messages",
        verbose_name=_("auteur"),
    )
    author_role = models.CharField(_("en qualité de"), max_length=16, choices=ResponderRole.choices)
    kind = models.CharField(_("type"), max_length=24, choices=MessageKind.choices)
    visibility = models.CharField(
        _("visibilité"), max_length=10, choices=MessageVisibility.choices, default=MessageVisibility.SHARED
    )
    body = models.TextField(_("texte"))
    language = models.CharField(_("langue"), max_length=8, default="fr")

    class Meta:
        verbose_name = _("message de la demande")
        verbose_name_plural = _("messages de la demande")
        ordering = ["created_at", "id"]
        indexes = [models.Index(fields=["ticket", "visibility"])]

    objects = TicketMessageQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.ticket.reference} · {self.get_kind_display()}"

    def clean(self) -> None:
        if not self.body.strip():
            raise ValidationError({"body": _("Un message vide n’est pas un message.")})
        if self.visibility == MessageVisibility.INTERNAL and self.author_role == ResponderRole.PERSON:
            raise ValidationError({"visibility": _("La personne n’écrit pas de notes internes.")})
        if self.kind == MessageKind.RESPONSE and self.visibility != MessageVisibility.SHARED:
            # A response the person cannot read is not a response.
            raise ValidationError({"kind": _("Une réponse est toujours visible par la personne.")})

    @property
    def is_internal(self) -> bool:
        return self.visibility == MessageVisibility.INTERNAL
