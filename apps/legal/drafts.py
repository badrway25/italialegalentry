"""
The drafted texts of the privacy notice (A) and the cookie / technical-storage information (B) — V5.14.

They are written from the processing this software actually performs: every factual sentence is traced to its
evidence in ``docs/legal/PRIVACY_NOTICE_SOURCES.md`` and ``docs/compliance/PRIVACY_PROCESSING_AUDIT.md``. A fact
that could not be verified is an OPEN FIELD, «[DA COMPLETARE — OF-nn — <class>: …]» (V5.16: the class says who
fills it, ``legal.models.OPEN_FIELD_CLASSES``), and production refuses to publish a
document that still carries one (``legal.services.publish``).

The texts live in ``apps/legal/content/<kind>/<lang>.txt``: a header of ``key: value`` lines, a line ``---``, then
the body (``## `` a section heading, ``### `` a sub-heading, ``- `` a list item, a blank line between blocks). The
Italian file is the master; ``fr``, ``en`` and ``ar`` are courtesy translations and say that the Italian prevails.

``load_drafts`` (the seed) writes them into a document only while nobody has touched it: an empty, unpublished
row, or a draft whose text is still exactly what the seed wrote last time (``seed_checksum``). A published
document, or one an editor changed in the back office, is never overwritten.
"""

from __future__ import annotations

from pathlib import Path

from legal.models import (
    TRANSLATION_LANGUAGES,
    VERIFIED_PROCESSING_KINDS,
    LegalDocument,
    LegalStatus,
    TranslationStatus,
)

CONTENT_DIR = Path(__file__).resolve().parent / "content"
SOURCE_REFERENCE = (
    "Redatto dai trattamenti verificati del software (direttiva V5.14) — docs/legal/PRIVACY_NOTICE_SOURCES.md"
)
HEADER_KEYS = ("title", "notice", "italian_link", "pending")


def parse(raw: str) -> dict:
    """``key: value`` header lines, ``---``, then the body."""
    text = raw.replace("\r\n", "\n")
    head, sep, body = text.partition("\n---\n")
    if not sep:
        raise ValueError("a drafted legal text needs a header, a line '---' and a body")
    entry: dict[str, str] = {}
    for line in head.splitlines():
        if not line.strip():
            continue
        key, colon, value = line.partition(":")
        key = key.strip()
        if not colon or key not in HEADER_KEYS:
            raise ValueError(f"unknown header line in a drafted legal text: {line!r}")
        entry[key] = value.strip()
    entry["body"] = body.strip() + "\n"
    return entry


def read(kind: str, lang: str) -> dict:
    return parse((CONTENT_DIR / kind / f"{lang}.txt").read_bytes().decode("utf-8"))


def drafted(kind: str) -> tuple[str, str, dict]:
    """(title_it, body_it, translations) for one A/B document."""
    master = read(kind, "it")
    translations = {lang: read(kind, lang) for lang in TRANSLATION_LANGUAGES}
    return master["title"], master["body"], translations


def apply_draft(document: LegalDocument) -> bool:
    """Write the drafted text into ``document`` when that overwrites nobody's work; True when it did."""
    if document.kind not in VERIFIED_PROCESSING_KINDS or document.status == LegalStatus.PUBLISHED:
        return False
    untouched = not document.body_it.strip() or (
        document.seed_checksum and document.compute_checksum() == document.seed_checksum
    )
    if not untouched:
        return False
    title, body, translations = drafted(document.kind)
    if document.title_it == title and document.body_it == body and document.translations == translations:
        return False
    document.title_it = title
    document.body_it = body
    document.translations = translations
    document.translation_status = TranslationStatus.PENDING
    document.source_reference = SOURCE_REFERENCE
    document.status = LegalStatus.DRAFT
    document.seed_checksum = document.compute_checksum()
    document.save()
    return True


def load_drafts() -> int:
    updated = 0
    for kind in VERIFIED_PROCESSING_KINDS:
        document, _created = LegalDocument.objects.get_or_create(kind=kind)
        updated += int(apply_draft(document))
    return updated
