"""
Upload hardening and document life-cycle (docs/REQUIREMENTS_MATRIX.md R-SEC-004).

Validation chain of ``store_upload``:
  1. extension allow-list (.pdf .jpg .jpeg .png) — nothing executable, no HTML/SVG/JS;
  2. size 1 byte … 10 MB;
  3. magic-byte sniffing (%PDF-, FF D8 FF, 89 50 4E 47 0D 0A 1A 0A) that must MATCH the extension —
     the client's Content-Type is never trusted;
  4. images: Pillow ``verify()`` + format check + decompression-bomb guard;
  5. PDF: reject active content (/JavaScript, /JS, /Launch) in the first 2 MB;
  6. random stored name (uuid4 + safe extension), one directory per owner, outside MEDIA_ROOT;
  7. antivirus hook ``scan_file`` (pluggable via settings.DOCUMENT_SCANNER; without one the honest
     answer is 'not_configured', never 'pending');
  8. audit row.

The second half of this module turns a stored file into a REQUIREMENT OF A CASE: declaring what a
case needs, filing versions against it, human review, expiry, and signed temporary links.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import logging
import re
import unicodedata
import uuid
import warnings
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath

from django.conf import settings
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature
from django.db import models, transaction
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from PIL import Image

from audit.services import record
from core import clock
from core.privacy import hashed_client_ip
from documents.models import (
    AccessClass,
    DocumentKind,
    DocumentRequirement,
    DocumentVersion,
    PrivateDocument,
    RequirementState,
    ScanStatus,
    VersionDecision,
)
from documents.storage import private_storage

log = logging.getLogger("ile.documents")

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
PDF_SCAN_BYTES = 2 * 1024 * 1024
ALLOWED_EXTENSIONS: dict[str, str] = {
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}
_MAGIC: tuple[tuple[bytes, str], ...] = (
    (b"%PDF-", "application/pdf"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
)
_PIL_FORMAT = {"image/jpeg": "JPEG", "image/png": "PNG"}
_PDF_ACTIVE_CONTENT = re.compile(rb"/(?:JavaScript|JS|Launch)\b")
_FILENAME_BAD = re.compile(r"[^\w.\- ]+", flags=re.UNICODE)
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
MAX_BASENAME = 100

REJECT_MESSAGES = {
    "empty": _("Le fichier est vide."),
    "too_large": _("Le fichier dépasse la taille maximale de 10 Mo."),
    "extension": _("Format non accepté : seuls les fichiers PDF, JPEG et PNG sont autorisés."),
    "content_mismatch": _("Le contenu du fichier ne correspond pas à son extension."),
    "image_invalid": _("L’image est illisible ou endommagée."),
    "pdf_active_content": _("Le PDF contient des éléments actifs (script ou lancement) et a été refusé."),
}


class UploadRejected(ValidationError):
    """Raised by validate_upload with a machine-readable ``code``."""

    def __init__(self, code: str):
        super().__init__(REJECT_MESSAGES[code], code=code)
        self.reason = code


@dataclass(frozen=True)
class ValidatedUpload:
    original_name: str
    extension: str
    content_type: str
    size: int
    sha256: str


# ---------------------------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------------------------
def sanitise_filename(name: str) -> str:
    """Base name only, no control characters, conservative character set, bounded length."""
    base = PureWindowsPath(PurePosixPath(name or "").name).name
    base = unicodedata.normalize("NFKC", base)
    base = _CONTROL.sub("", base)
    base = _FILENAME_BAD.sub("_", base).strip(" ._")
    if not base:
        base = "document"
    stem, dot, ext = base.rpartition(".")
    if not dot:
        stem, ext = base, ""
    stem = stem[:MAX_BASENAME].rstrip(" ._") or "document"
    return f"{stem}.{ext.lower()}" if ext else stem


def extension_of(name: str) -> str:
    _stem, dot, ext = name.rpartition(".")
    return f".{ext.lower()}" if dot and ext else ""


def sniff_content_type(head: bytes) -> str | None:
    for magic, content_type in _MAGIC:
        if head.startswith(magic):
            return content_type
    return None


def _read_head(uploaded_file, n: int = 16) -> bytes:
    uploaded_file.seek(0)
    head = uploaded_file.read(n)
    uploaded_file.seek(0)
    return head


def _sha256(uploaded_file) -> str:
    digest = hashlib.sha256()
    uploaded_file.seek(0)
    for chunk in uploaded_file.chunks():
        digest.update(chunk)
    uploaded_file.seek(0)
    return digest.hexdigest()


def _verify_image(uploaded_file, expected_format: str) -> None:
    uploaded_file.seek(0)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(uploaded_file) as img:
                fmt = img.format
                img.verify()
    except Exception as exc:  # Pillow raises many different error types
        raise UploadRejected("image_invalid") from exc
    finally:
        uploaded_file.seek(0)
    if fmt != expected_format:
        raise UploadRejected("content_mismatch")


def _verify_pdf(uploaded_file) -> None:
    uploaded_file.seek(0)
    head = uploaded_file.read(PDF_SCAN_BYTES)
    uploaded_file.seek(0)
    if _PDF_ACTIVE_CONTENT.search(head):
        raise UploadRejected("pdf_active_content")


def validate_upload(uploaded_file) -> ValidatedUpload:
    """Run the whole validation chain; raise UploadRejected (a ValidationError) on any failure."""
    size = int(getattr(uploaded_file, "size", 0) or 0)
    if size <= 0:
        raise UploadRejected("empty")
    if size > MAX_UPLOAD_BYTES:
        raise UploadRejected("too_large")
    original_name = sanitise_filename(getattr(uploaded_file, "name", "") or "")
    extension = extension_of(original_name)
    if extension not in ALLOWED_EXTENSIONS:
        raise UploadRejected("extension")
    expected_type = ALLOWED_EXTENSIONS[extension]
    sniffed = sniff_content_type(_read_head(uploaded_file))
    if sniffed != expected_type:
        raise UploadRejected("content_mismatch")
    if expected_type == "application/pdf":
        _verify_pdf(uploaded_file)
    else:
        _verify_image(uploaded_file, _PIL_FORMAT[expected_type])
    return ValidatedUpload(
        original_name=original_name,
        extension=extension,
        content_type=expected_type,
        size=size,
        sha256=_sha256(uploaded_file),
    )


# ---------------------------------------------------------------------------------------------
# Antivirus hook
# ---------------------------------------------------------------------------------------------
def scan_file(path: str) -> str:
    """
    Return one of the ScanStatus values.

    Without ``settings.DOCUMENT_SCANNER`` (dotted path of a callable ``(path) -> str``) nothing is
    scanned and the answer is ``not_configured`` — NOT ``pending``. The difference matters: a queue
    that nobody is draining is not a queue, and a security control that reports a backlog it does
    not have buys trust it has not earned. The interface says so in as many words
    (``documents.requirements.SCAN_RULES``). A scanner error yields 'error', never 'clean'.
    """
    dotted = getattr(settings, "DOCUMENT_SCANNER", "") or ""
    if not dotted:
        return ScanStatus.NOT_CONFIGURED
    try:
        scanner = import_string(dotted)
        result = str(scanner(path) or "").lower()
    except Exception:  # noqa: BLE001 - any scanner failure must be recorded, never hidden
        log.exception("document scanner failed")
        return ScanStatus.ERROR
    if result not in ScanStatus.values:
        log.error("document scanner returned an unknown status %r", result)
        return ScanStatus.ERROR
    return result


def apply_scan_result(doc: PrivateDocument, status: str, *, request=None, actor=None, note: str = "") -> None:
    doc.scan_status = status
    doc.scanned_at = clock.now()
    update_fields = ["scan_status", "scanned_at", "updated_at"]
    if status == ScanStatus.INFECTED and doc.has_file:
        _remove_file(doc)
        update_fields.append("file_removed_at")
    doc.save(update_fields=update_fields)
    record(
        request,
        action="documents.scan_result",
        target=doc,
        actor=actor,
        metadata={"status": status, "note": note[:200]},
    )


def run_pending_scans(limit: int = 100) -> dict[str, int]:
    storage = private_storage()
    counts = dict.fromkeys(ScanStatus.values, 0)
    for doc in PrivateDocument.objects.pending_scan().filter(file_removed_at__isnull=True)[:limit]:
        status = scan_file(storage.path(doc.relative_path))
        if status != doc.scan_status:
            apply_scan_result(doc, status, note="documents_scan_pending")
        counts[status] += 1
    return counts


# ---------------------------------------------------------------------------------------------
# Life-cycle
# ---------------------------------------------------------------------------------------------
def user_may_upload(user) -> bool:
    """Uploads are inside the reserved area: active account that accepted the Conditions."""
    return bool(getattr(user, "is_authenticated", False) and user.is_active and user.terms_accepted_at)


def store_upload(user, uploaded_file, kind: str, description: str = "", *, organisation=None, request=None):
    validated = validate_upload(uploaded_file)
    storage = private_storage()
    stored_name = f"{uuid.uuid4().hex}{validated.extension}"
    relative_path = f"{user.pk}/{stored_name}"
    uploaded_file.seek(0)
    saved_name = storage.save(relative_path, uploaded_file)
    status = scan_file(storage.path(saved_name))
    with transaction.atomic():
        doc = PrivateDocument.objects.create(
            owner=user,
            organisation=organisation,
            kind=kind,
            original_name=validated.original_name,
            stored_name=PurePosixPath(saved_name).name,
            content_type=validated.content_type,
            size=validated.size,
            sha256=validated.sha256,
            description=(description or "")[:200],
            scan_status=status,
            scanned_at=clock.now() if status not in (ScanStatus.PENDING, ScanStatus.NOT_CONFIGURED) else None,
            uploaded_ip_hash=hashed_client_ip(request) if request is not None else "",
        )
        if status == ScanStatus.INFECTED:
            _remove_file(doc)
            doc.save(update_fields=["file_removed_at", "updated_at"])
        record(
            request,
            action="documents.uploaded",
            target=doc,
            actor=user,
            metadata={"kind": kind, "size": validated.size, "scan_status": status},
        )
    return doc


def open_for_download(doc: PrivateDocument):
    return private_storage().open(doc.relative_path, "rb")


def _remove_file(doc: PrivateDocument) -> bool:
    storage = private_storage()
    removed = False
    if storage.exists(doc.relative_path):
        storage.delete(doc.relative_path)
        removed = True
    doc.file_removed_at = clock.now()
    return removed


def soft_delete(doc: PrivateDocument, *, request=None, actor=None) -> PrivateDocument:
    if doc.deleted_at is None:
        doc.deleted_at = clock.now()
        doc.save(update_fields=["deleted_at", "updated_at"])
        record(request, action="documents.deleted", target=doc, actor=actor)
    return doc


def purge_document(doc: PrivateDocument, *, request=None, actor=None, reason: str = "") -> None:
    """Remove the file and scrub the human-readable metadata; keep the row as a tombstone."""
    with transaction.atomic():
        removed = _remove_file(doc)
        if doc.deleted_at is None:
            doc.deleted_at = clock.now()
        doc.original_name = "purged"
        doc.description = ""
        doc.save(update_fields=["file_removed_at", "deleted_at", "original_name", "description", "updated_at"])
        record(
            request,
            action="documents.purged",
            target=doc,
            actor=actor,
            metadata={"file_removed": removed, "reason": reason},
        )


def purge_expired(*, today=None, apply: bool = False) -> dict[str, int]:
    """Purge files past ``retention_until`` and files of soft-deleted rows. Dry-run unless ``apply``."""
    today = today or clock.today()
    expired = PrivateDocument.objects.alive().filter(retention_until__lt=today, file_removed_at__isnull=True)
    deleted_with_file = PrivateDocument.objects.deleted().filter(file_removed_at__isnull=True)
    counts = {"expired": expired.count(), "soft_deleted": deleted_with_file.count()}
    if apply:
        for doc in list(expired):
            purge_document(doc, reason="retention_until")
        for doc in list(deleted_with_file):
            purge_document(doc, reason="soft_deleted")
    return counts


def purge_user_documents(user_id: int) -> int:
    """Erase every file of a user (account anonymisation). Rows remain as scrubbed tombstones."""
    count = 0
    for doc in PrivateDocument.objects.filter(owner_id=user_id):
        purge_document(doc, reason="account_anonymised")
        count += 1
    return count


def documents_export_section(user) -> list[dict]:
    return [
        {
            "id": str(doc.pk),
            "kind": doc.kind,
            "original_name": doc.original_name,
            "description": doc.description,
            "size": doc.size,
            "sha256": doc.sha256,
            "scan_status": doc.scan_status,
            "uploaded_at": doc.created_at,
            "organisation": doc.organisation.name if doc.organisation_id else None,
        }
        for doc in PrivateDocument.objects.for_owner(user).select_related("organisation")
    ]


# =================================================================================================
# REQUIREMENTS, VERSIONS, EXPIRY AND SIGNED TEMPORARY LINKS
#
# Everything below goes through this module for the same reason the rest of it does: there must be
# exactly ONE way for a file to enter and exactly one way for it to leave. A second upload path
# would be a second validation chain, and the second one is always the one that is wrong.
# =================================================================================================

#: Validity of a signed download link, in seconds (REQ-DOC-02). Stated to the user next to the
#: link — a temporary link whose expiry is a secret is a trap, not a control.
DOWNLOAD_LINK_TTL = 600
DOWNLOAD_LINK_MINUTES = DOWNLOAD_LINK_TTL // 60
DOWNLOAD_SALT = "documents.signed_download.v1"


class RequirementRefused(ValidationError):
    """An action the document domain does not allow. Never downgraded to a silent no-op."""


def antivirus_state(doc) -> dict:
    """The honest antivirus line for one file: its word, its rule, and whether a scan ever ran."""
    from documents.requirements import scan_rule

    status = doc.scan_status if doc is not None else ScanStatus.NOT_CONFIGURED
    return {
        "status": status,
        "label": dict(ScanStatus.choices).get(status, status),
        "rule": scan_rule(status),
        "scanned": status in (ScanStatus.CLEAN, ScanStatus.INFECTED),
        "scanned_at": getattr(doc, "scanned_at", None),
    }


# ---------------------------------------------------------------------------------------------
# May this file be HANDED OVER to this account?
#
# Distinct from "may this account READ this object" (documents.policies) on purpose. The policy
# answers a question about a person and a case; this answers a question about a file and a scanner.
# Both must be true before a byte leaves the server, and ``documents.views._serve`` asks both.
#
# It lives here, next to the scanner hook, so the PAGE and the DELIVERY cannot drift apart: before
# this function existed, ``presenters.present_version`` minted a signed link whenever the policy
# allowed a read, and ``_serve`` then refused it — every reviewer on an installation with no
# scanner (which is every installation today) was shown a "Télécharger" link that answered 403.
# ---------------------------------------------------------------------------------------------
def delivery_block(doc, user) -> str:
    """Return the code of what stops this file being delivered to ``user``, or '' if nothing does."""
    if doc is None or doc.deleted_at is not None or not doc.has_file:
        return "file_gone"
    if doc.is_infected:
        return "infected"
    if not doc.is_clean and doc.owner_id != getattr(user, "id", None):
        # Not scanned — no scanner deployed, or one still to run. Only the account that deposited
        # the file may retrieve it; anybody else waits for a verdict, human or automated.
        return "unscanned"
    return ""


def may_deliver(doc, user) -> bool:
    return not delivery_block(doc, user)


# ---------------------------------------------------------------------------------------------
# Declaring a requirement
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def declare_requirement(
    case,
    *,
    code: str,
    title: str,
    responsible_actor: str,
    kind: str = DocumentKind.OTHER,
    detail: str = "",
    responsible_note: str = "",
    mandatory: bool = True,
    due_date=None,
    access_class: str = AccessClass.CASE,
    source_title: str = "",
    source_ref: str = "",
    source_url: str = "",
    checklist_item=None,
    order: int | None = None,
    request=None,
) -> DocumentRequirement:
    """
    Add (or update, by its stable ``code``) one required piece to a case file.

    Idempotent on ``(case, code)`` so a rule-engine outcome can be replayed without duplicating the
    person's register. Never touches a state: a state is derived, never declared.
    """
    defaults = {
        "title": title,
        "detail": detail,
        "kind": kind,
        "responsible_actor": responsible_actor,
        "responsible_note": responsible_note,
        "mandatory": mandatory,
        "due_date": due_date,
        "access_class": access_class,
        "source_title": source_title,
        "source_ref": source_ref,
        "source_url": source_url,
        "checklist_item": checklist_item,
        "order": order if order is not None else case.document_requirements.count(),
    }
    requirement, created = DocumentRequirement.objects.update_or_create(case=case, code=code, defaults=defaults)
    requirement.full_clean(exclude=["state"])
    refresh_state(requirement)
    if created:
        record(
            request,
            action="documents.requirement.declared",
            target=requirement,
            metadata={"case": str(case.uuid), "code": code, "responsible": responsible_actor},
        )
    return requirement


# ---------------------------------------------------------------------------------------------
# Filing a version
# ---------------------------------------------------------------------------------------------
def may_file(user, requirement) -> bool:
    """
    Who may deposit a file against this requirement.

    The person whose case it is, when the piece is theirs to provide; and a live assignee whose
    mandate lets them act on the case. Never anybody else — deny by default, checked again by the
    object-level policy before the view does anything.
    """
    from accounts.permissions import can

    return can(user, "file", requirement)


@transaction.atomic
def file_version(
    requirement,
    user,
    uploaded_file,
    *,
    expires_on=None,
    request=None,
    description: str = "",
) -> DocumentVersion:
    """
    Store a file against a named requirement and make it the version in force.

    The previous version is superseded, not deleted: the history of what was deposited, when and by
    whom is part of the case file, and a person who replaces a blurred scan must still be able to
    show what they had sent first.

    The file goes through ``store_upload`` — the same allow-list, the same magic-byte check, the
    same random storage key, the same audit row. There is no second way in.
    """
    if requirement.case.is_read_only:
        raise RequirementRefused(_("Ce dossier est clos : aucune pièce ne peut plus y être déposée."))
    if not user_may_upload(user):
        raise RequirementRefused(_("Le dépôt de pièces nécessite l’acceptation des Conditions d’utilisation."))

    document = store_upload(
        user,
        uploaded_file,
        requirement.kind,
        description or requirement.title[:200],
        request=request,
    )

    previous = requirement.versions.filter(is_current=True).first()
    if previous is not None:
        previous.is_current = False
        previous.superseded_at = clock.now()
        previous.save(update_fields=["is_current", "superseded_at", "updated_at"])

    number = (requirement.versions.aggregate(models.Max("number"))["number__max"] or 0) + 1
    version = DocumentVersion.objects.create(
        requirement=requirement,
        number=number,
        document=document,
        filed_by=user,
        is_current=True,
        expires_on=expires_on,
        decision=VersionDecision.PENDING,
    )

    # A new deposit answers an outstanding request for a replacement.
    if requirement.replacement_requested_at is not None:
        requirement.replacement_requested_at = None
        requirement.replacement_reason = ""
        requirement.save(update_fields=["replacement_requested_at", "replacement_reason", "updated_at"])

    refresh_state(requirement, request=request, actor=user)
    record(
        request,
        actor=user,
        action="documents.requirement.filed",
        target=requirement,
        metadata={
            "case": str(requirement.case.uuid),
            "code": requirement.code,
            "version": number,
            "supersedes": previous.number if previous else None,
            "document": str(document.pk),
            "scan_status": document.scan_status,
            "expires_on": expires_on.isoformat() if expires_on else None,
        },
    )
    return version


# ---------------------------------------------------------------------------------------------
# Human review — never automatic, never the scanner's job
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def set_decision(version, decision: str, *, actor, note: str = "", request=None) -> DocumentVersion:
    """
    Record what a PERSON concluded about a deposited version.

    A refusal must carry its motive: "non valide" with no reason is an instruction to guess, and
    the person guessing is the one who has the least information.
    """
    if decision not in VersionDecision.values:
        raise RequirementRefused(_("Décision d’examen non reconnue."))
    if decision == VersionDecision.REFUSED and not (note or "").strip():
        raise RequirementRefused(_("Un refus doit indiquer son motif."))
    if not version.is_current:
        raise RequirementRefused(_("Seule la version en vigueur peut être examinée."))

    previous = version.decision
    version.decision = decision
    version.decision_note = (note or "").strip()[:300]
    version.decided_at = clock.now() if decision in (VersionDecision.ACCEPTED, VersionDecision.REFUSED) else None
    version.decided_by = actor if decision != VersionDecision.PENDING else None
    version.save(update_fields=["decision", "decision_note", "decided_at", "decided_by", "updated_at"])

    requirement = version.requirement
    refresh_state(requirement, request=request, actor=actor)
    record(
        request,
        actor=actor,
        action="documents.requirement.reviewed",
        target=requirement,
        metadata={
            "case": str(requirement.case.uuid),
            "code": requirement.code,
            "version": version.number,
            "from": previous,
            "to": decision,
            "state": requirement.state,
        },
    )
    if decision == VersionDecision.REFUSED:
        # A refusal is the one decision a person must not discover by logging in. It is also the one
        # whose REASON they need, so it travels in the body — never in the subject, which crosses
        # mail servers in the clear.
        _announce(
            requirement.case.person,
            "DOCUMENT_REJECTED",
            context={
                "case_reference": requirement.case.reference,
                "requirement": requirement.title,
                "reason": version.decision_note or str(_("motif précisé dans votre espace réservé")),
            },
            related=requirement,
            dedupe_key=f"document.rejected:{version.pk}:{version.number}",
            request=request,
        )
    return version


@transaction.atomic
def request_replacement(requirement, *, actor, reason: str, request=None) -> DocumentRequirement:
    """Ask for a new copy of a piece that is readable but no longer usable. The motive is required."""
    reason = (reason or "").strip()
    if not reason:
        raise RequirementRefused(_("Une demande de remplacement doit indiquer son motif."))
    requirement.replacement_requested_at = clock.now()
    requirement.replacement_reason = reason[:300]
    requirement.save(update_fields=["replacement_requested_at", "replacement_reason", "updated_at"])
    refresh_state(requirement, request=request, actor=actor)
    record(
        request,
        actor=actor,
        action="documents.requirement.replacement_requested",
        target=requirement,
        metadata={"case": str(requirement.case.uuid), "code": requirement.code, "reason": reason[:200]},
    )
    return requirement


# ---------------------------------------------------------------------------------------------
# Expiry — a document expires on its own, and the case must say so
# ---------------------------------------------------------------------------------------------
def refresh_state(requirement, *, today=None, request=None, actor=None) -> str:
    """
    Reconcile the cached ``state`` column with the derivation, and audit the change.

    The interface never waits for this: it reads ``display_state``, which derives on every render,
    so a piece that expires overnight is EXPIRÉ the next morning whether or not a job has run. This
    function exists so a queryset can count and filter, and so the transition leaves a trace.
    """
    from documents.requirements import derive_state, state_reason

    version = requirement.versions.filter(is_current=True).first()
    state = derive_state(requirement, version, today=today)
    reason = state_reason(requirement, version, state)
    if state == requirement.state and reason == requirement.state_note:
        return state
    previous, requirement.state = requirement.state, state
    requirement.state_note = reason[:300]
    requirement.save(update_fields=["state", "state_note", "updated_at"])
    record(
        request,
        actor=actor,
        action="documents.requirement.state",
        target=requirement,
        metadata={"case": str(requirement.case.uuid), "code": requirement.code, "from": previous, "to": state},
    )
    if state == RequirementState.EXPIRED and previous != RequirementState.EXPIRED:
        _announce(
            requirement.case.person,
            "DOCUMENT_EXPIRED",
            context={
                "case_reference": requirement.case.reference,
                "requirement": requirement.title,
                "valid_until": f"{version.expires_on:%d/%m/%Y}" if version and version.expires_on else "—",
            },
            related=requirement,
            dedupe_key=f"document.expired:{requirement.pk}:{version.pk if version else 0}",
        )
    return state


def refresh_all_states(*, today=None, limit: int | None = None) -> dict[str, int]:
    """Reconcile every requirement (management command). Returns the transitions it performed."""
    changed: dict[str, int] = {}
    queryset = DocumentRequirement.objects.select_related("case").prefetch_related("versions")
    if limit:
        queryset = queryset[:limit]
    for requirement in queryset:
        before = requirement.state
        after = refresh_state(requirement, today=today)
        if after != before:
            changed[f"{before}->{after}"] = changed.get(f"{before}->{after}", 0) + 1
    return changed


def expiring_soon(user, *, days: int | None = None):
    """Rows whose piece stops being usable within ``days`` — for the case's échéances."""
    from documents.requirements import REPLACE_WINDOW_DAYS

    horizon = clock.today() + dt.timedelta(days=days if days is not None else REPLACE_WINDOW_DAYS)
    return (
        DocumentRequirement.objects.readable_by(user)
        .filter(versions__is_current=True, versions__expires_on__lte=horizon)
        .select_related("case")
        .distinct()
    )


def valid_document_codes(case) -> list[str]:
    """
    The stable codes of the pieces this case has actually obtained, for the rule engine.

    ``rules.facts._documents_present`` wants exactly this and currently asks for it by importing
    ``documents.models.CaseDocument`` and ``DocumentState`` — names this app has never had. Both
    imports fail, both are swallowed by a bare ``except``, and the ``documents_present`` fact is
    therefore permanently empty: a rule that requires a document can never be satisfied, silently.
    This function is the supported way to ask, so the fix on that side is one line.

    The DERIVED state is used, not the cached column, so a piece that lapsed overnight stops
    counting immediately rather than when the reconciliation command next runs.
    """
    from documents.requirements import derive_state

    rows = (
        DocumentRequirement.objects.filter(case=case)
        .only("id", "code", "replacement_requested_at", "state")
        .prefetch_related("versions__document")
    )
    return sorted({row.code for row in rows if derive_state(row, row.current_version) == RequirementState.VALID})


# ---------------------------------------------------------------------------------------------
# Signed temporary download links (REQ-DOC-02)
# ---------------------------------------------------------------------------------------------
def signed_download_token(doc, user) -> str:
    """
    A signed, time-limited, USER-BOUND token for one document.

    Three properties, and the third is the one that is usually missing: the token expires, it
    cannot be forged, and it is worthless in anybody else's browser. It is an ADDITIONAL constraint
    on top of the object-level check, never a replacement for it — ``documents.views`` runs the
    policy again on every delivery, so a link that leaks into a chat, an e-mail thread or a proxy
    log grants nothing at all.
    """
    return signing.dumps({"d": str(doc.pk), "u": user.pk}, salt=DOWNLOAD_SALT)


def resolve_download_token(token: str, user) -> PrivateDocument:
    """
    Verify a token and return its document, or raise.

    ``SignatureExpired`` is deliberately allowed to propagate so the view can say *the link
    expired* and mint a fresh one, rather than showing "not found" for a document that is there.
    """
    payload = signing.loads(token, salt=DOWNLOAD_SALT, max_age=DOWNLOAD_LINK_TTL)
    if payload.get("u") != getattr(user, "pk", None):
        # Bound to the account it was issued for: a copied link is inert elsewhere.
        raise BadSignature("token does not belong to this account")
    doc = PrivateDocument.objects.alive().filter(pk=payload.get("d")).first()
    if doc is None:
        raise BadSignature("unknown document")
    return doc


def peek_expired_token(token: str) -> str:
    """Document id inside an EXPIRED but correctly signed token, so the page can offer a new link."""
    try:
        payload = signing.loads(token, salt=DOWNLOAD_SALT)
    except BadSignature:
        return ""
    return str(payload.get("d") or "")


def _announce(recipient, event_name: str, **kwargs) -> None:
    """
    Send one declared notification, and never let it break the decision that has already been made.

    Imported locally so ``documents`` does not depend on ``notifications`` at module level, and sent
    through ``notify_quietly`` so the notification lives in its own savepoint: a document decision
    that was recorded and audited must not be rolled back because a template had a typo.
    """
    try:
        from notifications import events
        from notifications.services import notify_quietly

        notify_quietly(recipient, getattr(events, event_name), **kwargs)
    except Exception:  # noqa: BLE001 - the decision is done and audited; this is an extra
        log.exception("notification %s could not be sent", event_name)
