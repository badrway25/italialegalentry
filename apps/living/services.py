"""Living services: public querysets with live sheet counts, workflow for sheets (audited)."""

from __future__ import annotations

from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from django.utils.translation import gettext as _

from audit.services import record as audit_record
from cms.models import PublicationStatus
from core import clock
from living.models import LegalReviewStatus, LivingSheet, LivingTopic

PUBLISH_PERMISSION = "living.publish_livingsheet"


class WorkflowError(ValidationError):
    pass


def _live_sheet_q(at=None) -> Q:
    at = at or clock.now()
    published = Q(sheets__status=PublicationStatus.PUBLISHED)
    scheduled = Q(sheets__status=PublicationStatus.SCHEDULED, sheets__publish_at__lte=at)
    not_expired = Q(sheets__unpublish_at__isnull=True) | Q(sheets__unpublish_at__gt=at)
    return (published | scheduled) & not_expired & Q(sheets__legal_review=LegalReviewStatus.REVIEWED)


def public_topics():
    """Live topics annotated with the number of live, reviewed sheets (``sheet_count``)."""
    return LivingTopic.objects.public().annotate(sheet_count=Count("sheets", filter=_live_sheet_q(), distinct=True))


def public_topic(slug: str) -> LivingTopic | None:
    return public_topics().filter(slug=slug).first()


def public_sheets(topic: LivingTopic):
    return LivingSheet.objects.public().filter(topic=topic)


def public_sheet(topic: LivingTopic, slug: str) -> LivingSheet | None:
    return public_sheets(topic).prefetch_related("translations").filter(slug=slug).first()


# ---------------------------------------------------------------------------------------------
# Sheet workflow
# ---------------------------------------------------------------------------------------------


def can_publish(user) -> bool:
    return bool(user and getattr(user, "is_active", False) and (user.is_superuser or user.has_perm(PUBLISH_PERMISSION)))


def mark_reviewed(sheet: LivingSheet, user, request=None) -> LivingSheet:
    """Record the legal review (who / when). Does not publish."""
    sheet.legal_review = LegalReviewStatus.REVIEWED
    sheet.reviewer = user
    sheet.last_reviewed_at = clock.now()
    sheet.full_clean()
    sheet.save()
    audit_record(request, action="living.sheet.reviewed", target=sheet, actor=user)
    return sheet


def submit_for_review(sheet: LivingSheet, user, request=None) -> LivingSheet:
    if sheet.status != PublicationStatus.DRAFT:
        raise WorkflowError(_("Seule une fiche en brouillon peut être soumise à la revue."))
    sheet.status = PublicationStatus.REVIEW
    sheet.save()
    audit_record(request, action="living.sheet.submitted_for_review", target=sheet, actor=user)
    return sheet


def publish(sheet: LivingSheet, user, request=None) -> LivingSheet:
    if not can_publish(user):
        raise PermissionDenied(_("Seuls les utilisateurs autorisés peuvent publier des fiches."))
    if sheet.status not in (PublicationStatus.REVIEW, PublicationStatus.SCHEDULED, PublicationStatus.ARCHIVED):
        raise WorkflowError(_("La fiche doit être en revue (ou archivée) pour être publiée."))
    if not sheet.is_reviewed:
        raise WorkflowError(_("Publication refusée : revue juridique en attente (CONTENT_PENDING_LEGAL_REVIEW)."))
    now = clock.now()
    future = bool(sheet.publish_at and sheet.publish_at > now)
    sheet.status = PublicationStatus.SCHEDULED if future else PublicationStatus.PUBLISHED
    sheet.full_clean()
    sheet.save()
    audit_record(request, action="living.sheet.published", target=sheet, actor=user, metadata={"status": sheet.status})
    return sheet


def archive(sheet: LivingSheet, user, request=None) -> LivingSheet:
    if sheet.status not in (PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED, PublicationStatus.REVIEW):
        raise WorkflowError(_("Cette fiche ne peut pas être archivée depuis son état actuel."))
    sheet.status = PublicationStatus.ARCHIVED
    sheet.save()
    audit_record(request, action="living.sheet.archived", target=sheet, actor=user)
    return sheet
