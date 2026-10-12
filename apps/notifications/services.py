"""
The notification service: one door in, two channels out.

``notify()`` is the single entry point. Every app that has something to tell somebody calls it, and
what happens next — the in-app record, the e-mail (or not), the preference, the audit row, the
idempotence — happens once, here, instead of being re-decided at each call site. The alternative was
tried everywhere before it was abandoned everywhere: a ``send_mail`` in a view, a second one in the
admin, and a year later nobody can answer what the platform actually sends to people.

Two invariants this module exists to hold:

* **The in-app record always wins.** It is written first and it is written whatever the preferences
  say. If the e-mail fails, is refused or is switched off, the person was still told, and the team
  can prove it. The e-mail is a courtesy layered on a record, never the record itself.
* **The only address is the account's own.** ``notify()`` takes a RECIPIENT, never an address, and
  resolves ``recipient.email`` itself. No caller can redirect a person's mail to a third party by
  passing a string, because there is no string to pass. The project's other outbound address — the
  single forms inbox, ``ILE["FORMS_DESTINATION_EMAIL"]`` — is reached through ``notify_forms_inbox``
  and is not part of person-directed mail.

The e-mail leaves through the existing ``EmailOutbox``, so notifications inherit its retries, its
back-office visibility and, in development and under test, its console / locmem backend: nothing in
this module can send a real e-mail on its own.
"""

from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from django.utils import translation

from core import clock
from notifications import events
from notifications.models import (
    EmailOutbox,
    EmailSuppression,
    Notification,
    NotificationChannel,
    NotificationPreference,
    OutboxStatus,
)

log = logging.getLogger("ile.notifications")

#: The one e-mail template every notification is rendered through. The TEXT of a notification is in
#: the registry, not in a template per event: a template per event is how twelve slightly different
#: signatures and three different tones appear in the same product.
NOTIFICATION_TEMPLATE = "notification"


def queue_email(
    *,
    to_email: str,
    subject: str,
    template: str,
    context: dict | None = None,
    reference: str = "",
    reply_to: str = "",
    send_now: bool | None = None,
) -> EmailOutbox:
    """Render ``notifications/email/<template>.txt`` (+ optional ``.html``) and queue it."""
    ctx = {"project": settings.ILE, **(context or {})}
    body_text = render_to_string(f"notifications/email/{template}.txt", ctx)
    try:
        body_html = render_to_string(f"notifications/email/{template}.html", ctx)
    except Exception:
        body_html = ""
    item = EmailOutbox.objects.create(
        to_email=to_email,
        subject=f"{settings.ACCOUNT_EMAIL_SUBJECT_PREFIX}{subject}"[:200],
        body_text=body_text,
        body_html=body_html,
        reference=reference,
        reply_to=reply_to,
    )
    if send_now if send_now is not None else getattr(settings, "NOTIFICATIONS_SEND_IMMEDIATELY", False):
        deliver(item)
    return item


def notify_forms_inbox(*, subject: str, template: str, context: dict, reference: str) -> EmailOutbox:
    """Every public form notification goes to the single configured destination (§1.1 note)."""
    return queue_email(
        to_email=settings.ILE["FORMS_DESTINATION_EMAIL"],
        subject=subject,
        template=template,
        context=context,
        reference=reference,
    )


def deliver(item: EmailOutbox) -> bool:
    if item.status in (OutboxStatus.SENT, OutboxStatus.CANCELLED):
        return False
    item.attempts += 1
    try:
        msg = EmailMultiAlternatives(
            subject=item.subject,
            body=item.body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[item.to_email],
            reply_to=[item.reply_to] if item.reply_to else None,
        )
        if item.body_html:
            msg.attach_alternative(item.body_html, "text/html")
        msg.send(fail_silently=False)
    except Exception as exc:  # noqa: BLE001 - we want to persist any delivery failure
        item.status = OutboxStatus.FAILED
        item.last_error = str(exc)[:2000]
        item.save(update_fields=["status", "attempts", "last_error", "updated_at"])
        log.warning("email delivery failed for outbox %s: %s", item.pk, exc)
        return False
    item.status = OutboxStatus.SENT
    item.sent_at = clock.now()
    item.last_error = ""
    item.save(update_fields=["status", "attempts", "sent_at", "last_error", "updated_at"])
    return True


def send_pending(limit: int = 100) -> tuple[int, int]:
    now = clock.now()
    qs = (
        EmailOutbox.objects.filter(status__in=[OutboxStatus.QUEUED, OutboxStatus.FAILED], attempts__lt=5)
        .filter(models_q_scheduled(now))
        .order_by("created_at")[:limit]
    )
    sent = failed = 0
    for item in qs:
        if deliver(item):
            sent += 1
        else:
            failed += 1
    return sent, failed


def models_q_scheduled(now):
    from django.db.models import Q

    return Q(scheduled_for__isnull=True) | Q(scheduled_for__lte=now)


# ---------------------------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------------------------
def preferences_for(user) -> NotificationPreference:
    """The account's preferences, created with the ON defaults the first time they are consulted."""
    preference, _created = NotificationPreference.objects.get_or_create(user=user)
    return preference


def email_allowed(user, category: str) -> bool:
    """
    Does this account still want e-mail for ``category``?

    Read without creating a row: consulting a preference is not the moment to write to the database,
    and an absent row means "nothing refused", which is the default the model documents.
    """
    preference = NotificationPreference.objects.filter(user=user).first()
    return preference.allows_email(category) if preference else True


@transaction.atomic
def set_email_preference(user, category: str, *, enabled: bool, request=None, actor=None) -> NotificationPreference:
    """
    Switch one category's e-mail on or off for one account, and audit the change.

    Audited because a person who stops receiving e-mail will one day ask why, and "somebody turned
    it off, on this date, from here" is the only answer worth giving. The in-app record is never
    affected — there is deliberately no argument for it.
    """
    if category not in events.CATEGORIES:
        raise events.UnknownEvent(f"unknown notification category {category!r}")
    preference = preferences_for(user)
    field = NotificationPreference.field_for(category)
    if getattr(preference, field) != enabled:
        setattr(preference, field, enabled)
        preference.save(update_fields=[field, "updated_at"])
        from audit.services import record

        record(
            request,
            actor=actor or user,
            action="notifications.preference",
            target=preference,
            metadata={"user_id": user.pk, "category": category, "email": enabled},
        )
    return preference


# ---------------------------------------------------------------------------------------------
# The entry point
# ---------------------------------------------------------------------------------------------
def _deliverable_address(recipient) -> tuple[str, str]:
    """
    The account's own address, or the reason there is none — in that order of preference.

    Four refusals, each of which has a way of becoming an incident:

    * **no address** — nothing to send to;
    * **inactive account** — a deactivated or suspended account is not somebody to keep writing to;
    * **anonymised account** — ``accounts.services.anonymise_user`` rewrites the address to
      ``anonymised-<id>@anonymised.invalid``. That domain does not exist, so mail to it bounces out
      of the platform and into whatever logs the bounce, carrying the subject of a notification
      about a person who asked to be erased;
    * **the look-alike domain** — ``ILE["FORBIDDEN_EMAIL_DOMAIN"]`` is not operated by the project.
      Writing to it would hand a person's notification to whoever does operate it.
    """
    from accounts.services import ANONYMISED_DOMAIN

    address = (getattr(recipient, "email", "") or "").strip()
    if not address:
        return "", EmailSuppression.NO_ADDRESS
    if not getattr(recipient, "is_active", True):
        return "", EmailSuppression.INACTIVE
    if address.lower().endswith("@" + ANONYMISED_DOMAIN):
        return "", EmailSuppression.ANONYMISED
    if address.lower().endswith("@" + settings.ILE["FORBIDDEN_EMAIL_DOMAIN"]):
        return "", EmailSuppression.FORBIDDEN_DOMAIN
    return address, ""


def _language_of(recipient) -> str:
    return getattr(recipient, "preferred_language", "") or settings.LANGUAGE_CODE


@transaction.atomic
def notify(
    recipient,
    event: str,
    *,
    context: dict | None = None,
    related=None,
    dedupe_key: str = "",
    sender=None,
    request=None,
) -> Notification:
    """
    Tell one account one declared thing, exactly once.

    ``event`` is a key of ``notifications.events``; anything else raises ``UnknownEvent`` rather
    than being written under a name nobody declared. ``context`` fills the registry's French source
    text and must carry every field the event declares — a body with a blank where the case
    reference belongs reads as a broken platform to the person and as a success to the code.

    ``dedupe_key`` is what makes a repeated scan harmless: pass a key that identifies the STATE
    being announced (``"checklist.overdue:412:2026-10-02"``), and the second call returns the
    notification the first one wrote instead of sending it again. Leave it empty for events that may
    legitimately repeat, such as a message from the équipe.

    The text is rendered in the RECIPIENT's language, not in the language of whoever triggered the
    event: a night-time management command has no language, and a member of staff working in Italian
    must not send an Italian notification to a person who reads French.

    Returns the ``Notification``. It never returns ``None``, and it never "succeeds" silently
    without a record: if this function returns, the person has been told in the reserved area.
    """
    declared = events.get(event)
    recipient_pk = getattr(recipient, "pk", None)
    if recipient_pk is None:
        raise ValueError("notify() needs a saved account as recipient")

    if dedupe_key:
        existing = Notification.objects.filter(recipient=recipient, dedupe_key=dedupe_key).first()
        if existing is not None:
            return existing

    with translation.override(_language_of(recipient)):
        subject = str(declared.subject_fr)
        body = declared.render_body(context)

    try:
        with transaction.atomic():
            notification = _write(
                recipient=recipient,
                declared=declared,
                subject=subject,
                body=body,
                related=related,
                dedupe_key=dedupe_key,
                sender=sender,
            )
    except IntegrityError:
        # Two workers on the same night, or a job retried after a timeout. The unique constraint did
        # its work; the right answer is the row that won, not an exception at the call site.
        existing = Notification.objects.filter(recipient=recipient, dedupe_key=dedupe_key).first()
        if existing is None:
            raise
        return existing

    _maybe_email(notification, declared, subject=subject, body=body)
    _audit(notification, request=request, actor=sender)
    return notification


def _write(*, recipient, declared, subject: str, body: str, related, dedupe_key: str, sender) -> Notification:
    """
    Write the in-app record: one ``portal.Message`` row and its notification companion.

    The sender is kept only when it is a member of staff, which is what ``Message.sender`` means —
    its own ``limit_choices_to`` says so, and the reserved area presents a message as coming from
    « l'équipe ». A professional holding a mandate is not the équipe, and an automatic scan is
    nobody at all; both are recorded as system-generated, with no sender, rather than being dressed
    up as a person who wrote.
    """
    from portal.models import Message

    sender = sender if getattr(sender, "is_staff", False) else None
    message = Message(recipient=recipient, sender=sender, subject=subject[:200], body=body)
    if related is not None:
        message.content_type = ContentType.objects.get_for_model(related)
        message.object_id = str(related.pk)
    message.full_clean()
    message.save()
    return Notification.objects.create(
        message=message,
        recipient=recipient,
        event=declared.key,
        category=declared.category,
        dedupe_key=dedupe_key,
        channel=NotificationChannel.IN_APP,
    )


def _maybe_email(notification: Notification, declared, *, subject: str, body: str) -> None:
    """
    Queue the e-mail, or record why not. The decision is read from the registry and the preference.

    Deliberately no ``if event == ...`` anywhere in this function: which events warrant mail is data
    (``NotificationEvent.email``), and a preference is data too. The day someone wants to stop
    mailing a category, they change a row or a constant — not a branch.
    """
    recipient = notification.recipient
    if not declared.email:
        reason = EmailSuppression.NOT_BY_EMAIL
    elif not email_allowed(recipient, declared.category):
        reason = EmailSuppression.PREFERENCE
    else:
        address, reason = _deliverable_address(recipient)
        if address:
            item = queue_email(
                to_email=address,
                subject=subject,
                template=NOTIFICATION_TEMPLATE,
                context={
                    "heading": subject,
                    "body": body,
                    "event": declared.key,
                    "category": declared.category,
                    "language": _language_of(recipient),
                },
                reference=f"notifications.Notification:{notification.pk}",
            )
            notification.outbox = item
            notification.channel = NotificationChannel.IN_APP_AND_EMAIL
            notification.email_suppressed = ""
            notification.save(update_fields=["outbox", "channel", "email_suppressed", "updated_at"])
            return
    notification.email_suppressed = reason
    notification.save(update_fields=["email_suppressed", "updated_at"])


def _audit(notification: Notification, *, request=None, actor=None) -> None:
    """
    Audit metadata carries identifiers only — never the subject, the body or the address.

    The audit trail outlives the notification and is read by people who need to know THAT somebody
    was told, not WHAT they were told; the text itself stays in the reserved area, where reading it
    is an authorised act.
    """
    from audit.services import record

    record(
        request,
        actor=actor,
        action="notifications.sent",
        target=notification,
        metadata={
            "event": notification.event,
            "category": notification.category,
            "channel": notification.channel,
            "recipient_id": notification.recipient_id,
            "message_id": str(notification.message_id),
            "email_suppressed": notification.email_suppressed,
        },
    )


@transaction.atomic
def notify_for_message(message, *, event: str = events.TEAM_MESSAGE, request=None, actor=None) -> Notification | None:
    """
    Turn a staff-authored ``portal.Message`` that ALREADY EXISTS into a notification.

    ``notify()`` writes the message itself, which is right for a machine-generated event whose text
    comes from the registry. A message written BY somebody is created by
    ``portal.services.send_message`` — with the subject that person chose, its own scheduling and
    its own audit row — and writing a second one here would show the person the same thing twice.
    So this attaches to the row that exists, and everything else (the e-mail, the preference, the
    audit, the idempotence) behaves exactly as it does for every other event.

    Two deliberate refusals:

    * The MAIL subject stays the registry's constant, never the subject a member of staff typed. A
      subject somebody typed in a hurry is a subject nobody vetted for a name or a file name, and
      the whole point of the constant is that no such thing can reach a mail header.
    * A message scheduled for later (``visible_from``) is not announced at all. E-mailing it would
      deliver, today, a communication the team chose to hold until a date — and the person cannot
      open it in the reserved area either, so the e-mail would be an announcement of nothing.

    Idempotent: called twice on the same message, the second call returns the first notification.
    """
    declared = events.get(event)
    existing = Notification.objects.filter(message=message).first()
    if existing is not None:
        return existing
    if not message.is_visible():
        return None

    recipient = message.recipient
    with translation.override(_language_of(recipient)):
        subject = str(declared.subject_fr)
        body = declared.render_body({"body": message.body}) if declared.fields == ("body",) else message.body

    notification = Notification.objects.create(
        message=message,
        recipient=recipient,
        event=declared.key,
        category=declared.category,
        dedupe_key="",
        channel=NotificationChannel.IN_APP,
    )
    _maybe_email(notification, declared, subject=subject, body=body)
    _audit(notification, request=request, actor=actor)
    return notification


def notify_quietly(recipient, event: str, **kwargs) -> Notification | None:
    """
    ``notify()`` for callers whose own work must survive a notification failing.

    A transition of the case file must not be lost because a mail template did not render. The call
    runs in its own savepoint (``notify`` is atomic), so a database error rolls back the
    notification alone and leaves the caller's transaction usable — catching an ``IntegrityError``
    without one would leave the surrounding transaction in an aborted state on PostgreSQL, which is
    a far worse failure than the missing notification.

    Failures are logged with the event key and the recipient's id, and nothing else: this logger's
    stream is shipped elsewhere and must never carry a subject line or an address.
    """
    try:
        return notify(recipient, event, **kwargs)
    except Exception:  # noqa: BLE001 - a notification is never worth losing the caller's work over
        log.exception(
            "notification %s could not be written",
            event,
            extra={"event": event, "recipient": f"user:{getattr(recipient, 'pk', None)}"},
        )
        return None
