from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class OutboxStatus(models.TextChoices):
    QUEUED = "queued", _("In coda")
    SENT = "sent", _("Inviata")
    FAILED = "failed", _("Fallita")
    CANCELLED = "cancelled", _("Annullata")


class EmailOutbox(TimeStampedModel):
    """
    Database outbox for outgoing e-mail. Sending is decoupled from the request (no Celery needed
    at this scale): ``manage.py send_queued_emails`` or the in-process sender flushes the queue.
    In development the EMAIL_BACKEND is the console: no real e-mail is ever sent.
    """

    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    body_text = models.TextField()
    body_html = models.TextField(blank=True)
    reply_to = models.EmailField(blank=True)
    reference = models.CharField(
        max_length=120, blank=True, db_index=True, help_text=_("es. enquiries.CompanyNeedsRequest:42")
    )
    status = models.CharField(max_length=10, choices=OutboxStatus.choices, default=OutboxStatus.QUEUED, db_index=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    last_error = models.TextField(blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("e-mail in uscita")
        verbose_name_plural = _("e-mail in uscita (outbox)")

    def __str__(self) -> str:
        return f"[{self.status}] {self.subject} → {self.to_email}"


# ---------------------------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------------------------
def _event_choices():
    """
    The registry's keys, read lazily.

    Django evaluates a callable ``choices`` when it needs one, which keeps this module free of an
    import-time dependency on ``notifications.events`` — and keeps the migrations free of a frozen
    copy of the list, so declaring an event stays a change to the registry and not a schema change.
    """
    from notifications import events

    return events.choices()


class NotificationChannel(models.TextChoices):
    """What was actually done for this notification — not what was configured."""

    IN_APP = "in_app", _("Spazio riservato")
    IN_APP_AND_EMAIL = "in_app_email", _("Spazio riservato ed e-mail")


class EmailSuppression(models.TextChoices):
    """
    Why no e-mail left the platform for a notification that might otherwise have carried one.

    Recorded rather than inferred, because « je n'ai rien reçu » is a support question that has to be
    answerable in one query, and because "the preference was off" and "the address was unusable" are
    two very different answers to give someone. Empty means an e-mail was queued.
    """

    NOT_BY_EMAIL = "not_by_email", _("L'evento non prevede e-mail")
    PREFERENCE = "preference", _("Disattivata dalla persona")
    NO_ADDRESS = "no_address", _("Nessun indirizzo utilizzabile")
    INACTIVE = "inactive", _("Account disattivato")
    ANONYMISED = "anonymised", _("Account anonimizzato")
    FORBIDDEN_DOMAIN = "forbidden", _("Dominio non gestito dal progetto")


class NotificationQuerySet(models.QuerySet):
    def for_recipient(self, user):
        if not getattr(user, "is_authenticated", False):
            return self.none()
        return self.filter(recipient=user)

    def of_event(self, *keys):
        return self.filter(event__in=keys)

    def emailed(self):
        return self.filter(channel=NotificationChannel.IN_APP_AND_EMAIL)


class Notification(TimeStampedModel):
    """
    One machine-generated notification — and the reason this app does not own an inbox.

    The person already HAS an inbox: ``portal.Message``. The reserved area lists it, counts its
    unread rows for the badge, paginates it, authorises it row by row (``portal.policies``) and lets
    the person mark a row read. A second table with a recipient, a subject, a body and a read flag
    would be a second inbox — two lists to look in, a badge that is wrong by construction, and two
    places to forget when somebody exercises their right to erasure. So this model does not
    duplicate ``Message``: it ATTACHES to one, and deleting the message deletes the notification.

    What lives here is what ``Message`` cannot answer, and nothing else:

    * ``event``            — which declared event this is, so the same thing is never announced twice
                             under two wordings, and so a category can be counted and switched off;
    * ``dedupe_key``       — what makes a nightly scan idempotent (see ``notifications.deadlines``);
    * ``channel``          — what was really done: in-app only, or in-app and e-mail;
    * ``outbox``           — the outbox row, so "was it sent, did it fail" has an answer;
    * ``email_suppressed`` — why it was not sent, on the occasions it was not.

    The subject, the body, the related object and the read state are read THROUGH the message. The
    properties below exist so a caller can treat a notification as the whole thing it is, without
    having to know which of the two tables holds which column.
    """

    message = models.OneToOneField(
        "portal.Message",
        on_delete=models.CASCADE,
        related_name="notification",
        verbose_name=_("comunicazione"),
        help_text=_("La riga che la persona legge nell'area riservata. Unica casella di posta."),
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("destinatario"),
    )
    event = models.CharField(_("evento"), max_length=64, db_index=True, choices=_event_choices)
    category = models.CharField(_("categoria"), max_length=16, db_index=True)
    channel = models.CharField(
        _("canale"), max_length=16, choices=NotificationChannel.choices, default=NotificationChannel.IN_APP
    )
    dedupe_key = models.CharField(
        _("chiave di unicità"),
        max_length=200,
        blank=True,
        help_text=_("Vuota quando l'evento può legittimamente ripetersi (es. un messaggio dell'équipe)."),
    )
    # Named ``outbox`` and not ``email`` on purpose: ``audit.services._label`` reads an ``email``
    # attribute as an address when it builds the label of an audited row, and a notification is
    # audited on every send. A field name is a small thing to get right and a confusing crash to
    # debug — the value here is a queued message, not somebody's address.
    outbox = models.ForeignKey(
        EmailOutbox,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
        verbose_name=_("e-mail in uscita"),
    )
    email_suppressed = models.CharField(
        _("e-mail non inviata perché"), max_length=16, choices=EmailSuppression.choices, blank=True
    )

    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("notifica")
        verbose_name_plural = _("notifiche")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "-created_at"], name="notif_rcpt_date_idx"),
            models.Index(fields=["event", "-created_at"], name="notif_event_date_idx"),
        ]
        constraints = [
            # Idempotence, in one line of schema rather than in the discipline of every caller. A
            # scan run twice, a retried job and two workers racing on the same night all collide
            # here instead of warning the same person twice — and a warning repeated every night is
            # how people learn to ignore warnings. Partial, because an event that may legitimately
            # repeat (a message from the équipe) carries no key and must stay free to repeat.
            models.UniqueConstraint(
                fields=["recipient", "dedupe_key"],
                condition=~models.Q(dedupe_key=""),
                name="notif_once_per_recipient_and_key",
            ),
        ]

    def __str__(self) -> str:
        # Neutral, for the reason ``portal.Message.__str__`` is neutral: this string is copied into
        # audit rows, the application log and the admin's LogEntry, all of which outlive the erasure
        # of the notification itself. Identifiers only — never the subject, never the address.
        return f"{self.event} → user:{self.recipient_id}"

    # -- read through the message ---------------------------------------------------------------
    @property
    def subject(self) -> str:
        return self.message.subject

    @property
    def body(self) -> str:
        return self.message.body

    @property
    def related_object(self):
        return self.message.related_object

    @property
    def is_read(self) -> bool:
        return self.message.is_read

    @property
    def read_at(self):
        return self.message.read_at

    @property
    def was_emailed(self) -> bool:
        return self.channel == NotificationChannel.IN_APP_AND_EMAIL


class NotificationPreference(TimeStampedModel):
    """
    Per-account e-mail preferences: one switch per category, and no switch at all for the record.

    Why they live HERE rather than on ``accounts.PersonProfile``, which would be the obvious home:
    notifications are not addressed only to persons. A professional holding a mandate, a company
    contact and a training body all receive them, and none of those accounts has a
    ``PersonProfile`` — that model is the person's own situation, read by the legal rule engine,
    and widening it into a settings table for every account type would cost it exactly what makes
    it defensible. A preference about a channel also belongs beside the service that has to honour
    it: the one place that must never forget to consult it is ``notifications.services.notify``.

    **In-app cannot be switched off.** The in-app notification is the RECORD that the platform told
    somebody something. It is what the team reads back when a person says they were never informed,
    and what the audit row points at; a record its own subject can suppress is not a record. The
    e-mail is a convenience laid on top of it, and the convenience is what a person may decline.

    An account with no row here has refused nothing: every default is ON, because somebody who has
    never opened the preference screen still expects to be told that their dossier moved.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preference",
        verbose_name=_("account"),
    )
    # One boolean per category rather than a stored list of disabled keys: a new category then
    # arrives as a migration with an explicit default, visible in review, instead of silently
    # reading as "enabled" for every account because nobody's stored list mentions it yet.
    email_case = models.BooleanField(_("e-mail: seguito del fascicolo"), default=True)
    email_deadline = models.BooleanField(_("e-mail: scadenze"), default=True)
    email_document = models.BooleanField(_("e-mail: documenti"), default=True)
    email_message = models.BooleanField(_("e-mail: messaggi dell'équipe"), default=True)
    email_assignment = models.BooleanField(_("e-mail: accessi e incarichi"), default=True)

    class Meta:
        verbose_name = _("preferenze di notifica")
        verbose_name_plural = _("preferenze di notifica")

    def __str__(self) -> str:
        return f"preferences user:{self.user_id}"

    @staticmethod
    def field_for(category: str) -> str:
        return f"email_{category}"

    def allows_email(self, category: str) -> bool:
        """
        True when this account still wants e-mail for ``category``.

        An unknown category answers True rather than False: a notification worth sending must not be
        lost because a registry entry arrived before its switch did. The opposite default would
        silence people with nobody noticing, and ``test_every_category_has_a_switch`` closes the gap
        at the source instead.
        """
        return bool(getattr(self, self.field_for(category), True))
