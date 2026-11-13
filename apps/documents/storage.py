"""
Private file storage — a FileSystemStorage rooted at ``settings.PRIVATE_MEDIA_ROOT``.

It refuses to be configured inside ``MEDIA_ROOT`` (which may be served publicly) and has no public
URL at all. A new instance is built per call so tests can point PRIVATE_MEDIA_ROOT elsewhere.
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage


class PrivateFileSystemStorage(FileSystemStorage):
    def url(self, name):  # pragma: no cover - defensive: must never be used
        raise ImproperlyConfigured("Private documents have no public URL; use documents:download.")


def private_root() -> Path:
    root = Path(settings.PRIVATE_MEDIA_ROOT).resolve()
    media_root = Path(settings.MEDIA_ROOT).resolve()
    if root == media_root or media_root in root.parents:
        raise ImproperlyConfigured("PRIVATE_MEDIA_ROOT must be outside MEDIA_ROOT.")
    return root


def private_storage() -> PrivateFileSystemStorage:
    root = private_root()
    root.mkdir(parents=True, exist_ok=True)
    return PrivateFileSystemStorage(location=str(root), base_url=None, file_permissions_mode=0o600)
