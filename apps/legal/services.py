from __future__ import annotations

from django.core.cache import cache
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext as _

from core import clock
from legal.models import LegalDocument, LegalDocumentVersion, LegalKind, LegalStatus

CACHE_KEY = "legal.all_published"


def ensure_documents() -> int:
    created = 0
    for kind in LegalKind.values:
        _obj, was_created = LegalDocument.objects.get_or_create(kind=kind)
        created += int(was_created)
    return created


def all_official_pages_published() -> bool:
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


def invalidate() -> None:
    cache.delete(CACHE_KEY)


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
    now = clock.now()
    document.status = LegalStatus.PUBLISHED
    document.published_at = now
    document.published_by = user
    document.last_reviewed_at = document.last_reviewed_at or now
    document.save()
    LegalDocumentVersion.objects.get_or_create(
        document=document,
        version=document.version,
        defaults={
            "title_it": document.title_it,
            "body_it": document.body_it,
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
