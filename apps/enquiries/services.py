"""
Business logic of the enquiries app (views stay thin).

* ``submit(request, form, spec)`` — the single pipeline used by every public form: spam drop,
  duplicate suppression (24 h), consent record, persistence, notification to the single forms
  inbox, optional neutral acknowledgement, audit trail.
* ``anonymise`` / ``purge_expired`` — GDPR erasure and retention.
* ``submissions_for_user`` — portal hook (owner match).
* ``export_csv_rows`` / ``export_json`` — back-office exports (portability).
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from dataclasses import dataclass, field

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from audit.services import record as audit_record
from consents.services import record_consent
from core import clock
from core.privacy import hashed_client_ip, truncated_user_agent
from enquiries.models import (
    SUBMISSION_MODELS,
    CollaborationProposal,
    CompanyNeedsRequest,
    ContactRequest,
    ProposalKind,
    PublicSubmission,
    SubmissionStatus,
    compute_duplicate_hash,
)
from notifications.services import notify_forms_inbox, queue_email

log = logging.getLogger("ile.enquiries")

DUPLICATE_WINDOW = dt.timedelta(hours=24)
ACK_SETTING = "ENQUIRIES_ACKNOWLEDGE_SUBMITTER"  # default False: nothing is ever e-mailed to submitters unless enabled


@dataclass(frozen=True)
class FormSpec:
    """Static description of a public form (one per view)."""

    key: str
    model: type[PublicSubmission]
    purpose: str
    throttle_scope: str
    email_template: str
    subject: object  # str or lazy translation
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SubmissionResult:
    obj: PublicSubmission | None = None
    created: bool = False
    spam: bool = False
    duplicate: bool = False


COMPANY_NEEDS = FormSpec(
    key="company_needs",
    model=CompanyNeedsRequest,
    purpose="company_needs",
    throttle_scope="enquiries.company_needs",
    email_template="enquiries_company_needs",
    subject=_("Recueil des besoins — nouvelle demande d’entreprise"),
)
INSTITUTION_PROPOSAL = FormSpec(
    key="institution_proposal",
    model=CollaborationProposal,
    purpose="institution_proposal",
    throttle_scope="enquiries.collaboration",
    email_template="enquiries_collaboration_proposal",
    subject=_("Proposition de collaboration — institution"),
    extra={"kind": ProposalKind.INSTITUTION},
)
UNIVERSITY_PROPOSAL = FormSpec(
    key="university_proposal",
    model=CollaborationProposal,
    purpose="university_proposal",
    throttle_scope="enquiries.collaboration",
    email_template="enquiries_collaboration_proposal",
    subject=_("Proposition de partenariat — université / organisme de formation"),
    extra={"kind": ProposalKind.UNIVERSITY},
)
CONTACT = FormSpec(
    key="contact",
    model=ContactRequest,
    purpose="contact",
    throttle_scope="enquiries.contact",
    email_template="enquiries_contact",
    subject=_("Nouvelle demande de contact"),
)
SPECS: dict[str, FormSpec] = {s.key: s for s in (COMPANY_NEEDS, INSTITUTION_PROPOSAL, UNIVERSITY_PROPOSAL, CONTACT)}


def _language() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def find_duplicate(spec: FormSpec, duplicate_hash: str, now=None) -> PublicSubmission | None:
    since = (now or clock.now()) - DUPLICATE_WINDOW
    return (
        spec.model.objects.filter(duplicate_hash=duplicate_hash, created_at__gte=since).order_by("-created_at").first()
    )


def submit(request, form, spec: FormSpec) -> SubmissionResult:
    """
    Process a *valid* public form. Returns a ``SubmissionResult``; the caller always shows the
    same success page so that bots and duplicate senders receive no signal.
    """
    if form.is_spam:
        audit_record(request, action="enquiries.spam_dropped", metadata={"form": spec.key})
        log.info("spam dropped", extra={"event": "enquiries.spam_dropped", "form": spec.key})
        return SubmissionResult(spam=True)

    obj: PublicSubmission = form.save(commit=False)
    for name, value in spec.extra.items():
        setattr(obj, name, value)
    obj.email = form.normalised_email()
    obj.duplicate_hash = compute_duplicate_hash(spec.model._meta.label_lower, obj.duplicate_key_values())

    existing = find_duplicate(spec, obj.duplicate_hash)
    if existing is not None:
        audit_record(request, action="enquiries.duplicate", target=existing, metadata={"form": spec.key})
        return SubmissionResult(obj=None, duplicate=True)

    user = getattr(request, "user", None)
    user = user if getattr(user, "is_authenticated", False) else None
    with transaction.atomic():
        consent = record_consent(request, spec.purpose, email=obj.email, user=user, language=_language())
        obj.consent = consent
        obj.language = _language()
        obj.source_path = (request.path or "")[:300]
        obj.ip_hash = hashed_client_ip(request)
        obj.user_agent = truncated_user_agent(request)
        obj.owner = user
        obj.last_contact_at = clock.now()
        obj.save()
        _notify_inbox(obj, spec)
        if getattr(settings, ACK_SETTING, False):
            _acknowledge(obj, spec)
        audit_record(
            request,
            action="enquiries.submitted",
            target=obj,
            metadata={"form": spec.key, "consent_text": consent.consent_text.locked_key, "language": obj.language},
        )
    return SubmissionResult(obj=obj, created=True)


def _notify_inbox(obj: PublicSubmission, spec: FormSpec):
    """Plain-text notification listing the submitted fields, to the single configured inbox only."""
    return notify_forms_inbox(
        subject=str(spec.subject),
        template=spec.email_template,
        context={
            "submission": obj,
            "rows": obj.data_rows(),
            "kind_label": obj.kind_label(),
            "consent": obj.consent,
            "submitted_at": obj.created_at,
            "language": obj.language,
            "reference": f"{obj._meta.label}:{obj.pk}",
        },
        reference=f"{obj._meta.label}:{obj.pk}",
    )


def _acknowledge(obj: PublicSubmission, spec: FormSpec):
    """Neutral acknowledgement to the submitter — no submitted data, no promise of any outcome."""
    return queue_email(
        to_email=obj.email,
        subject=str(_("Votre demande a bien été transmise")),
        template="enquiries_acknowledgement",
        context={"kind_label": obj.kind_label(), "submitted_at": obj.created_at},
        reference=f"{obj._meta.label}:{obj.pk}:ack",
    )


# ---------------------------------------------------------------------------------------------
# Back-office / GDPR helpers
# ---------------------------------------------------------------------------------------------


def mark_handled(obj: PublicSubmission, user, request=None) -> PublicSubmission:
    now = clock.now()
    obj.status = SubmissionStatus.HANDLED
    obj.handled_at = now
    obj.handled_by = user if getattr(user, "is_authenticated", False) else None
    obj.last_contact_at = now
    obj.save(update_fields=["status", "handled_at", "handled_by", "last_contact_at", "updated_at"])
    audit_record(request, action="enquiries.handled", target=obj, actor=user)
    return obj


def anonymise(obj: PublicSubmission, user=None, request=None, reason: str = "") -> PublicSubmission:
    """GDPR erasure: personal fields become "[anonymised]"; the row and its audit trail stay."""
    if obj.is_anonymised:
        return obj
    obj.anonymise_fields()
    obj.anonymised_at = clock.now()
    obj.save()
    audit_record(
        request,
        action="enquiries.anonymised",
        target=obj,
        actor=user,
        metadata={"reason": reason[:200], "fields": list(obj.PERSONAL_FIELDS)},
    )
    return obj


def expired_queryset(model: type[PublicSubmission], months: int | None = None, now=None):
    months = months or settings.ILE["RETENTION_MONTHS_FORMS"]
    now = now or clock.now()
    cutoff = now - dt.timedelta(days=int(months * 30.4375))
    return model.objects.filter(
        Q(last_contact_at__lt=cutoff)
        | Q(last_contact_at__isnull=True, handled_at__lt=cutoff)
        | Q(last_contact_at__isnull=True, handled_at__isnull=True, created_at__lt=cutoff)
    )


def purge_expired(months: int | None = None, dry_run: bool = True, user=None, now=None) -> dict[str, int]:
    """
    Delete submissions older than the retention period (24 months from the last contact, from the
    legal texts). ``dry_run`` (default) only counts. Returns ``{model_label: count}``.
    """
    months = months or settings.ILE["RETENTION_MONTHS_FORMS"]
    counts: dict[str, int] = {}
    for model in SUBMISSION_MODELS:
        qs = expired_queryset(model, months, now)
        counts[model._meta.label] = qs.count()
        if not dry_run and counts[model._meta.label]:
            qs.delete()
    if not dry_run:
        audit_record(None, action="enquiries.purged", actor=user, metadata={"months": months, "counts": counts})
    return counts


def submissions_for_user(user) -> list[PublicSubmission]:
    """Portal hook: every submission owned by the user, newest first, across the three models."""
    if not getattr(user, "is_authenticated", False):
        return []
    items: list[PublicSubmission] = []
    for model in SUBMISSION_MODELS:
        items.extend(model.objects.filter(owner=user, anonymised_at__isnull=True))
    items.sort(key=lambda o: o.created_at, reverse=True)
    return items


EXPORT_META_FIELDS = (
    "id",
    "created_at",
    "status",
    "language",
    "source_path",
    "external_reference",
    "handled_at",
    "handled_by",
    "last_contact_at",
    "anonymised_at",
    "admin_notes",
)
EXPORT_CONSENT_FIELDS = ("consent_purpose", "consent_text_key", "consent_text_version", "consent_given_at")


def export_header(model: type[PublicSubmission]) -> list[str]:
    return [*EXPORT_META_FIELDS, *model.DATA_FIELDS, *EXPORT_CONSENT_FIELDS]


def export_row(obj: PublicSubmission) -> list[str]:
    def _s(value) -> str:
        if value is None:
            return ""
        if isinstance(value, dt.datetime):
            return value.isoformat()
        return str(value)

    meta = [_s(getattr(obj, name)) for name in EXPORT_META_FIELDS]
    data = [_s(getattr(obj, name)) for name in obj.DATA_FIELDS]
    consent = obj.consent
    consent_cols = [
        consent.purpose,
        consent.consent_text.locked_key or f"{consent.consent_text.purpose}@v{consent.consent_text.version}",
        str(consent.consent_text.version),
        consent.given_at.isoformat(),
    ]
    return [*meta, *data, *consent_cols]


def export_json(obj: PublicSubmission) -> str:
    """Single submission as JSON (GDPR portability, art. 20)."""
    payload = dict(zip(export_header(type(obj)), export_row(obj), strict=True))
    payload["model"] = obj._meta.label
    return json.dumps(payload, ensure_ascii=False, indent=2)
