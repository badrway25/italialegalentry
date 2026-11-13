"""
Upload validators for the public Forum media library.

Only public, non-personal material is uploaded here (photos, videos, PDF documents of the
Forum). Private documents belong to the ``documents`` app (private storage, authorised download).
"""

from __future__ import annotations

from pathlib import PurePosixPath

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PDF_MAX_BYTES = 10 * 1024 * 1024
MEDIA_MAX_BYTES = 60 * 1024 * 1024

PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".webm"}

_IMAGE_MAGIC = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF")
_VIDEO_MAGIC = (b"\x1a\x45\xdf\xa3",)  # webm/matroska; mp4 checked through the ``ftyp`` box


def _extension(name: str) -> str:
    return PurePosixPath(name or "").suffix.lower()


def _head(file, size: int = 16) -> bytes:
    try:
        pos = file.tell()
    except Exception:  # pragma: no cover - non seekable
        pos = None
    try:
        file.seek(0)
        head = file.read(size)
    finally:
        if pos is not None:
            file.seek(pos)
    return head or b""


def validate_pdf(file) -> None:
    ext = _extension(getattr(file, "name", ""))
    if ext not in PDF_EXTENSIONS:
        raise ValidationError(_("Seuls les documents PDF sont acceptés."))
    if file.size > PDF_MAX_BYTES:
        raise ValidationError(_("Le document dépasse la taille maximale autorisée (10 Mo)."))
    if not _head(file, 5).startswith(b"%PDF-"):
        raise ValidationError(_("Le fichier n’est pas un PDF valide."))


def validate_media_file(file) -> None:
    ext = _extension(getattr(file, "name", ""))
    if ext not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
        raise ValidationError(_("Formats acceptés : JPG, PNG, WebP, MP4, WebM."))
    if file.size > MEDIA_MAX_BYTES:
        raise ValidationError(_("Le fichier dépasse la taille maximale autorisée (60 Mo)."))
    head = _head(file, 16)
    if ext in IMAGE_EXTENSIONS and not head.startswith(_IMAGE_MAGIC):
        raise ValidationError(_("Le fichier image n’est pas valide."))
    if ext == ".webm" and not head.startswith(_VIDEO_MAGIC):
        raise ValidationError(_("Le fichier vidéo n’est pas valide."))
    if ext == ".mp4" and b"ftyp" not in head:
        raise ValidationError(_("Le fichier vidéo n’est pas valide."))
