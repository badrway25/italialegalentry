from __future__ import annotations

from django.core.cache import cache
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from core import clock
from legal.models import (
    VERIFIED_PROCESSING_KINDS,
    LegalDocument,
    LegalDocumentVersion,
    LegalKind,
    LegalStatus,
    open_fields_allowed,
)

CACHE_KEY = "legal.all_published"
DOCUMENT_CACHE_KEY = "legal.published.%s"


def ensure_documents() -> int:
    created = 0
    for kind in LegalKind.values:
        _obj, was_created = LegalDocument.objects.get_or_create(kind=kind)
        created += int(was_created)
    return created


def all_official_pages_published() -> bool:
    """Gate G1: ALL FIVE documents published — never only the privacy and cookie information (V5.14 §6).

    The forms, sign-up, newsletter and Virtual Forum depend on the Allegato 1 pages (C, D) as well as on A and B,
    so A and B public on their own keep every one of them closed.
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached
    try:
        docs = {d.kind: d for d in LegalDocument.objects.all()}
        ok = all(kind in docs and docs[kind].is_available for kind in LegalKind.values)
    except Exception:  # pragma: no cover - before migrations
        ok = False
    cache.set(CACHE_KEY, ok, 30)
    return ok


def document_available(kind: str) -> bool:
    """One document published and showable (per-document gate: a link to it, a route that 404s without it)."""
    key = DOCUMENT_CACHE_KEY % kind
    cached = cache.get(key)
    if cached is not None:
        return cached
    try:
        doc = LegalDocument.objects.filter(kind=kind).first()
        ok = bool(doc and doc.is_available)
    except Exception:  # pragma: no cover - before migrations
        ok = False
    cache.set(key, ok, 30)
    return ok


def invalidate() -> None:
    cache.delete(CACHE_KEY)
    cache.delete_many([DOCUMENT_CACHE_KEY % kind for kind in LegalKind.values])


def get_document(kind: str) -> LegalDocument:
    obj, _ = LegalDocument.objects.get_or_create(kind=kind)
    return obj


def publish(document: LegalDocument, user, request=None) -> LegalDocument:
    """Publish the official Italian text. Requires the dedicated permission and a non-empty text."""
    if not (user.is_superuser or user.has_perm("legal.publish_legaldocument")):
        raise PermissionDenied
    if not document.body_it.strip():
        raise ValidationError(_("Impossibile pubblicare: il testo ufficiale italiano è assente."))
    if not document.source_reference.strip():
        raise ValidationError(_("Indicare il riferimento della fonte ufficiale (Allegato 1)."))
    if document.open_fields() and not open_fields_allowed():
        # Plain Italian, like the rest of the back office's legal screens: no new catalogue message.
        # V5.16: by class — whatever the class (production configuration, owner confirmation, legal review), it refuses
        listed = "; ".join(f"{label}: {', '.join(ids)}" for label, ids in document.open_field_classes())
        raise ValidationError(
            f"Impossibile pubblicare: il testo contiene ancora campi da completare ({listed}). "
            "Sostituire ogni «[DA COMPLETARE …]», nel testo italiano e nelle traduzioni, con il dato verificato."
        )
    now = clock.now()
    document.status = LegalStatus.PUBLISHED
    document.published_at = now
    document.published_by = user
    document.last_reviewed_at = document.last_reviewed_at or now
    if document.kind in VERIFIED_PROCESSING_KINDS and not document.effective_date:
        document.effective_date = timezone.localdate(now)  # the date of the revision, shown in the page's head
    document._publishing = True  # LegalDocument.save: this change of text is the publication itself
    try:
        document.save()
    finally:
        document._publishing = False
    LegalDocumentVersion.objects.get_or_create(
        document=document,
        version=document.version,
        defaults={
            "title_it": document.title_it,
            "body_it": document.body_it,
            "translations": document.translations or {},
            "checksum": document.checksum,
            "published_at": now,
            "published_by": user,
        },
    )
    invalidate()
    from audit.services import record

    record(request, action="legal.published", target=document, actor=user, metadata={"version": document.version})
    return document


def unpublish(document: LegalDocument, user, request=None) -> LegalDocument:
    if not (user.is_superuser or user.has_perm("legal.publish_legaldocument")):
        raise PermissionDenied
    document.status = LegalStatus.DRAFT if document.body_it.strip() else LegalStatus.BLOCKED
    document.save()
    invalidate()
    from audit.services import record

    record(request, action="legal.unpublished", target=document, actor=user)
    return document
