"""
Forum domain services — views stay thin, admin actions delegate here.

Nothing in this module invents content: section texts come from the locked registry through the
event's ``locked_key_prefix``; editable data comes from the back-office models.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import logging
from dataclasses import dataclass

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.urls import reverse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from audit.services import record as audit_record
from cms import locked_content
from consents.models import ConsentPurpose
from consents.services import record_consent
from core import clock, flags, gates
from core.privacy import hashed_client_ip, truncated_user_agent
from forum.models import (
    SPEAKER_NAMES_FLAG,
    ForumEvent,
    ForumMode,
    ForumPartner,
    ForumProgramItem,
    ForumRegistration,
    PartnerKind,
    RegistrationStatus,
    SpeakerRole,
)
from notifications.services import notify_forms_inbox, queue_email

log = logging.getLogger("ile.forum")

# Exact wording from the implementation document (§2.1 note) — UI string, translatable via .po.
PERMANENT_TITLE = "FORUM PERMANENT VÉNÉTIE–MAROC"

CSV_COLUMNS = (
    "id",
    "created_at",
    "status",
    "first_name",
    "last_name",
    "organisation",
    "role",
    "email",
    "phone",
    "country",
    "category",
    "category_label",
    "sector_of_interest",
    "language",
    "consent_purpose",
    "consent_text_version",
    "consent_given_at",
    "consent_withdrawn_at",
    "invited_to_virtual_forum",
    "admin_notes",
)


# ------------------------------------------------------------------------------------------
# Event selection and mode
# ------------------------------------------------------------------------------------------
def current_event(now: dt.datetime | None = None) -> ForumEvent | None:
    """The live edition shown on /forum/: the primary one, else the most recent live edition."""
    qs = ForumEvent.objects.live(now)
    return qs.filter(is_primary=True).first() or qs.order_by("-date").first()


def speaker_names_visible() -> bool:
    return flags.is_enabled(SPEAKER_NAMES_FLAG)


@dataclass(frozen=True)
class PublicSpeaker:
    role_label: str
    person_name: str
    organisation: str


def public_speakers(event: ForumEvent) -> list[PublicSpeaker]:
    """Functions always; names (and organisation) only with both authorisations (gate G5)."""
    site_flag = speaker_names_visible()
    out: list[PublicSpeaker] = []
    for role in event.speaker_roles.filter(is_visible=True):
        name = role.public_name(site_flag)
        out.append(PublicSpeaker(role.role_label_fr, name, role.organisation if name else ""))
    return out


def public_partners(event: ForumEvent, kind: str | None = None) -> list[ForumPartner]:
    qs = event.partners.select_related("logo").filter(authorized=True, logo__isnull=False)
    if kind:
        qs = qs.filter(kind=kind)
    return [p for p in qs if p.is_public]


def programme(event: ForumEvent) -> list[ForumProgramItem]:
    return list(event.programme_items.filter(is_visible=True))


def permanent_sections(event: ForumEvent, now: dt.datetime | None = None) -> dict:
    """Only published rows; templates hide sections without content."""
    now = now or clock.now()
    interventions = list(event.interventions.live(now).select_related("speaker", "document"))
    site_flag = speaker_names_visible()
    for item in interventions:
        item.public_speaker_name = item.speaker.public_name(site_flag) if item.speaker_id else ""
        item.public_speaker_role = item.speaker.role_label_fr if item.speaker_id else ""
    return {
        "outcomes": list(event.outcomes.live(now)),
        "media_items": list(event.media_items.live(now).select_related("asset")),
        "documents": list(event.documents.live(now)),
        "interventions": interventions,
        "agreements": list(event.agreements.live(now).select_related("document")),
        "partners": public_partners(event),
        "next_events": list(event.next_events.live(now)),
    }


# ------------------------------------------------------------------------------------------
# JSON-LD (event mode only; no invented images/offers)
# ------------------------------------------------------------------------------------------
def jsonld_event(event: ForumEvent, request=None) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event.locked_text("header.title") or event.slug,
        "description": event.locked_text("header.subtitle"),
        "startDate": event.starts_at.isoformat(),
        "endDate": event.ends_at.isoformat(),
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled",
        "location": {
            "@type": "Place",
            "name": event.venue,
            "address": {"@type": "PostalAddress", "addressLocality": event.city, "addressCountry": event.country_code},
        },
        "organizer": {"@type": "Organization", "name": settings.ILE["PROMOTER"]},
        "isAccessibleForFree": True,
        "inLanguage": ["fr", "it"],
    }
    if request is not None:
        data["url"] = request.build_absolute_uri(reverse("forum:index"))
    # Same escaping as faq/glossary render_jsonld: <, > and & can never reach the page raw, so the
    # block cannot break out of <script type="application/ld+json">.
    dumped = json.dumps(data, ensure_ascii=False)
    dumped = dumped.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(dumped)  # noqa: S308 - escaped above


# ------------------------------------------------------------------------------------------
# Page context
# ------------------------------------------------------------------------------------------
def page_context(request, event: ForumEvent | None) -> dict:
    now = clock.now()
    lang = translation.get_language() or settings.LANGUAGE_CODE
    forms_gate = gates.public_forms_enabled()
    ctx: dict = {
        "event": event,
        "forms_enabled": forms_gate.open,
        "forms_reason": forms_gate.reason,
        "virtual_forum_enabled": gates.virtual_forum_enabled(),
        "now": now,
    }
    if event is None:
        ctx.update(
            {
                "mode": ForumMode.EVENT,
                "is_permanent": False,
                "registration_open": False,
                "page_title": locked_content.text("p2.forum.header.title", lang),
                "meta_description": locked_content.text("p2.forum.header.subtitle", lang),
            }
        )
        return ctx
    mode = event.effective_mode(now)
    is_permanent = mode == ForumMode.PERMANENT
    event_title = event.locked_text("header.title", lang)
    permanent_title = _(PERMANENT_TITLE)
    # the name stays in French where the translators have not given it yet (B2): the page then says which language
    # it is in (WCAG 3.1.2) — on the h1 and on the trail's link of the registration pages
    permanent_title_lang = "fr" if lang.split("-")[0] != "fr" and permanent_title == PERMANENT_TITLE else ""
    ctx.update(
        {
            "mode": mode,
            "is_permanent": is_permanent,
            "permanent_title": permanent_title,
            "permanent_title_lang": permanent_title_lang,
            "page_title": permanent_title if is_permanent else event_title,
            "page_title_lang": permanent_title_lang if is_permanent else "",
            "event_title": event_title,
            "meta_description": event.locked_text("header.subtitle", lang),
            "registration_open": event.registration_is_open(now),
            "programme": programme(event),
            "speakers": public_speakers(event),
            "patron_partners": public_partners(event, PartnerKind.PATRON),
            "hero_image_alt": event.hero_image.alt(lang) if event.hero_image_id else "",
            "jsonld": "" if is_permanent else jsonld_event(event, request),
        }
    )
    if is_permanent:
        ctx.update(permanent_sections(event, now))
    return ctx


# ------------------------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------------------------
def find_duplicate(event: ForumEvent, email: str) -> ForumRegistration | None:
    return ForumRegistration.objects.filter(event=event, email__iexact=(email or "").strip()).first()


def create_registration(request, event: ForumEvent, data: dict) -> tuple[ForumRegistration | None, bool]:
    """
    Persist a registration with its consent proof, notify the single forms inbox, acknowledge
    the registrant and audit. Returns ``(registration, created)``; a duplicate e-mail for the
    same edition returns ``(existing, False)`` without a new row (the caller shows success).
    """
    email = (data.get("email") or "").strip().lower()
    existing = find_duplicate(event, email)
    if existing:
        audit_record(request, action="forum.registration.duplicate", target=existing, metadata={"event": event.slug})
        return existing, False
    lang = (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]
    user = getattr(request, "user", None)
    try:
        with transaction.atomic():
            consent = record_consent(request, ConsentPurpose.FORUM_REGISTRATION, email, user=user, language=lang)
            registration = ForumRegistration.objects.create(
                event=event,
                first_name=data["first_name"],
                last_name=data["last_name"],
                organisation=data.get("organisation", ""),
                role=data.get("role", ""),
                email=email,
                phone=data.get("phone", ""),
                country=data.get("country", ""),
                category=data["category"],
                sector_of_interest=data.get("sector_of_interest", ""),
                consent=consent,
                language=lang,
                ip_hash=hashed_client_ip(request),
                user_agent=truncated_user_agent(request),
                user=user if getattr(user, "is_authenticated", False) else None,
            )
    except IntegrityError:  # race on the case-insensitive unique constraint
        existing = find_duplicate(event, email)
        if existing:
            audit_record(request, action="forum.registration.duplicate", target=existing)
            return existing, False
        raise
    _notify(registration)
    audit_record(
        request,
        action="forum.registration.created",
        target=registration,
        metadata={"event": event.slug, "category": registration.category, "consent_id": consent.pk},
    )
    log.info("forum registration created", extra={"event": event.slug, "registration": registration.pk})
    return registration, True


def _notify(registration: ForumRegistration) -> None:
    event = registration.event
    ctx = {
        "registration": registration,
        "event": event,
        "event_title": event.locked_text("header.title"),
        "event_meta": event.locked_text("header.meta"),
        "category_label": registration.get_category_display(),
        "consent_version": consent_version(registration),
        "contact_email": settings.ILE["PUBLIC_CONTACT_EMAIL"],
    }
    reference = f"forum.ForumRegistration:{registration.pk}"
    notify_forms_inbox(
        subject=_("Nouvelle inscription — %(title)s") % {"title": ctx["event_title"]},
        template="forum_registration_inbox",
        context=ctx,
        reference=reference,
    )
    queue_email(
        to_email=registration.email,
        subject=_("Votre inscription — %(title)s") % {"title": ctx["event_title"]},
        template="forum_registration_ack",
        context=ctx,
        reference=reference,
        reply_to=settings.ILE["PUBLIC_CONTACT_EMAIL"],
    )


def consent_version(registration: ForumRegistration) -> str:
    text = registration.consent.consent_text
    key = text.locked_key or text.purpose
    return f"{key}@v{text.version}"


def set_status(queryset, status: str, request=None) -> int:
    count = 0
    for registration in queryset:
        if registration.status == status:
            continue
        before = registration.status
        registration.status = status
        registration.last_contact_at = clock.now()
        registration.save(update_fields=["status", "last_contact_at", "updated_at"])
        audit_record(
            request,
            action="forum.registration.status",
            target=registration,
            metadata={"from": before, "to": status},
        )
        count += 1
    return count


def anonymise_registration(registration: ForumRegistration, request=None) -> ForumRegistration:
    """Irreversibly remove personal data (GDPR erasure) while keeping the statistical row."""
    if registration.is_anonymised:
        return registration
    registration.first_name = "—"
    registration.last_name = "—"
    registration.organisation = ""
    registration.role = ""
    registration.email = f"anonymised-{registration.pk}@example.invalid"
    registration.phone = ""
    registration.country = ""
    registration.sector_of_interest = ""
    registration.ip_hash = ""
    registration.user_agent = ""
    registration.admin_notes = ""
    registration.user = None
    registration.anonymised_at = clock.now()
    registration.save()
    audit_record(request, action="forum.registration.anonymised", target=registration)
    return registration


def export_csv(queryset, request=None) -> bytes:
    """UTF-8 with BOM (Excel friendly); includes consent version and timestamp."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";", lineterminator="\r\n")
    writer.writerow(CSV_COLUMNS)
    rows = 0
    for r in queryset.select_related("consent", "consent__consent_text"):
        writer.writerow(
            [
                r.pk,
                r.created_at.isoformat(),
                r.status,
                r.first_name,
                r.last_name,
                r.organisation,
                r.role,
                r.email,
                r.phone,
                r.country,
                r.category,
                r.get_category_display(),
                r.sector_of_interest,
                r.language,
                r.consent.purpose,
                consent_version(r),
                r.consent.given_at.isoformat(),
                r.consent.withdrawn_at.isoformat() if r.consent.withdrawn_at else "",
                "1" if r.invited_to_virtual_forum else "0",
                r.admin_notes,
            ]
        )
        rows += 1
    audit_record(request, action="forum.registration.export", metadata={"rows": rows})
    return ("﻿" + buffer.getvalue()).encode("utf-8")


# ------------------------------------------------------------------------------------------
# Programme (prescribed seed, editable, resettable)
# ------------------------------------------------------------------------------------------
def prescribed_programme(event: ForumEvent) -> list[dict]:
    try:
        items, _lang = locked_content.get(event.locked_key("programme.items"), "fr")
    except locked_content.LockedContentMissing:
        return []
    out = []
    for index, raw in enumerate(items):
        time_label, title = "", raw
        if " — " in raw:
            head, tail = raw.split(" — ", 1)
            if head.strip() and head.strip()[0].isdigit():
                time_label, title = head.strip(), tail.strip()
        out.append({"order": (index + 1) * 10, "time_label": time_label, "title_fr": title, "locked_index": index})
    return out


def reset_programme(event: ForumEvent, request=None) -> int:
    """Replace the whole programme with the prescribed eight items (admin action)."""
    items = prescribed_programme(event)
    with transaction.atomic():
        event.programme_items.all().delete()
        for item in items:
            ForumProgramItem.objects.create(event=event, is_locked_seed=True, is_visible=True, **item)
    audit_record(request, action="forum.programme.reset", target=event, metadata={"items": len(items)})
    return len(items)


def ensure_programme(event: ForumEvent) -> int:
    """Seed the prescribed programme only when the edition has no items (never overwrite edits)."""
    if event.programme_items.exists():
        return 0
    created = 0
    for item in prescribed_programme(event):
        ForumProgramItem.objects.create(event=event, is_locked_seed=True, **item)
        created += 1
    return created


def ensure_speaker_roles(event: ForumEvent) -> int:
    if event.speaker_roles.exists():
        return 0
    try:
        roles, _lang = locked_content.get(event.locked_key("speakers.roles"), "fr")
    except locked_content.LockedContentMissing:
        return 0
    for index, label in enumerate(roles):
        SpeakerRole.objects.create(
            event=event, order=(index + 1) * 10, role_label_fr=label, is_locked_seed=True, locked_index=index
        )
    return len(roles)


# ------------------------------------------------------------------------------------------
# Homepage banner (partial provided to the pages app)
# ------------------------------------------------------------------------------------------
def banner_context() -> dict:
    lang = translation.get_language() or settings.LANGUAGE_CODE
    visible = gates.forum_banner_visible()
    if visible:
        event = current_event()
        visible = event is not None and not event.is_permanent()
    return {
        "visible": visible,
        "title": locked_content.text("p2.home.banner.title", lang),
        "meta": locked_content.text("p2.home.banner.meta", lang),
        "quote": locked_content.text("p2.home.banner.quote", lang),
        "button": locked_content.text("p2.home.banner.button", lang),
        "lang": locked_content.get("p2.home.banner.title", lang)[1],
        "url": reverse("forum:index"),
    }


def registration_counts(event: ForumEvent) -> dict[str, int]:
    counts = dict.fromkeys(RegistrationStatus.values, 0)
    for row in event.registrations.values("status").order_by().annotate(n=Count("id")):
        counts[row["status"]] = row["n"]
    counts["total"] = sum(counts.values())
    return counts
