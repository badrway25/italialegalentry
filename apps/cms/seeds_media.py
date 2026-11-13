"""
Media library seed: turns ``static/img/photos/manifest.json`` (written by ``scripts/fetch_images.py``)
into ``cms.MediaAsset`` rows, idempotently.

* The natural key of an asset is its ``source_url`` (one row per curated photo).
* Provenance facts (licence, download date, stereotype check, dimensions) are always synchronised
  from the manifest. The author is synchronised too, except that a name completed in the back-office
  is never replaced by the manifest's placeholder ("Unsplash contributor …").
* Editorial fields are protected: ``title``, ``alt_fr`` and ``license_notes`` are written only when
  empty, ``is_decorative`` only on creation, and the translator fields ``alt_it`` / ``alt_en`` /
  ``alt_ar`` are never touched (they stay blank until the translations are supplied — see
  docs/IMAGE_LICENSES.md).
* The largest WebP derivative ≤ 1440px is copied into the default storage when it is missing there
  or when its content differs from the committed derivative (e.g. after a new crop or redaction), so
  re-running the seed never rewrites an up-to-date file but never serves a stale one either.

Called by ``cms.seeds.seed_media`` (``manage.py seed_all``); ``seed()`` returns a summary string.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction

log = logging.getLogger("ile.cms")

PHOTOS_DIR = Path(settings.BASE_DIR) / "static" / "img" / "photos"
MANIFEST_PATH = PHOTOS_DIR / "manifest.json"
STORAGE_PREFIX = "library/photos"
PREFERRED_WIDTH = 1440
# Author placeholder written by scripts/fetch_images.py when the contributor name could not be
# looked up; a real name entered in the back-office always wins over it.
AUTHOR_PLACEHOLDER_PREFIX = "Unsplash contributor"

# Must stay identical to ``scripts/fetch_images.py::FORBIDDEN_SUBJECT_KEYWORDS`` (tested).
FORBIDDEN_SUBJECT_KEYWORDS: tuple[str, ...] = (
    "door",
    "porta",
    "passport",
    "valise",
    "suitcase",
    "frontière",
    "border",
    "aéroport",
    "airport",
    "queue",
    "file",
    "grille",
    "gate",
)

REQUIRED_ENTRY_KEYS = (
    "photo_id",
    "slug",
    "usage_slot",
    "title_fr",
    "alt_fr",
    "author",
    "source_url",
    "license",
    "downloaded_on",
    "width",
    "height",
    "files",
    "forbidden_subject_check",
)

LICENSE_CODES = {"Unsplash License": "unsplash", "Pexels License": "pexels", "CC0": "cc0", "CC BY 4.0": "cc_by"}


class MediaSeedError(ValueError):
    pass


def forbidden_keyword_hits(*texts: str) -> list[str]:
    hits: set[str] = set()
    for text in texts:
        lowered = (text or "").lower()
        hits.update(k for k in FORBIDDEN_SUBJECT_KEYWORDS if k in lowered)
    return sorted(hits)


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    images = data.get("images", [])
    for entry in images:
        missing = [k for k in REQUIRED_ENTRY_KEYS if k not in entry]
        if missing:
            raise MediaSeedError(f"manifest entry {entry.get('slug', '?')} misses {missing}")
        if entry["forbidden_subject_check"] is not True:
            raise MediaSeedError(f"{entry['slug']}: forbidden-subject check not recorded")
        hits = forbidden_keyword_hits(entry["slug"], entry["title_fr"], entry["alt_fr"], entry.get("subject", ""))
        if hits:
            raise MediaSeedError(f"{entry['slug']}: forbidden subject keyword(s) {hits}")
        if entry.get("redact") and not entry.get("redact_reason"):
            raise MediaSeedError(f"{entry['slug']}: redaction recorded without a reason")
    return images


def preferred_derivative(entry: dict) -> Path:
    """Largest WebP derivative not wider than PREFERRED_WIDTH (falls back to the JPG)."""
    webp = entry["files"].get("webp") or {}
    widths = sorted((int(w) for w in webp), reverse=True)
    for width in widths:
        if width <= PREFERRED_WIDTH:
            return PHOTOS_DIR / webp[str(width)]
    if widths:
        return PHOTOS_DIR / webp[str(widths[-1])]
    return PHOTOS_DIR / entry["files"]["jpg"]


def ensure_stored(entry: dict) -> tuple[str, bool]:
    """
    Make sure the preferred derivative is in the default storage with the committed content.
    Returns ``(name, copied)``; ``copied`` is True when the file was created or refreshed.
    """
    source = preferred_derivative(entry)
    if not source.exists():
        raise MediaSeedError(f"{entry['slug']}: derivative {source.name} missing — run scripts/fetch_images.py")
    name = f"{STORAGE_PREFIX}/{source.name}"
    data = source.read_bytes()
    if default_storage.exists(name):
        with default_storage.open(name, "rb") as fh:
            if fh.read() == data:
                return name, False
        default_storage.delete(name)  # stale copy (older crop/redaction): replace in place
    saved = default_storage.save(name, ContentFile(data, name=source.name))
    if saved != name:  # pragma: no cover - would mean the storage renamed a freshly freed name
        raise MediaSeedError(f"{entry['slug']}: storage saved {saved!r} instead of {name!r}")
    return saved, True


def _license_code(label: str) -> str:
    from cms.models import MediaLicense

    code = LICENSE_CODES.get(label, "")
    return code if code in MediaLicense.values else MediaLicense.OTHER


def _provenance_note(entry: dict) -> str:
    return f"slug={entry['slug']}; slot={entry['usage_slot']}; photo_id={entry['photo_id']}"[:255]


def author_should_sync(current: str, from_manifest: str) -> bool:
    """The manifest wins unless it only carries the placeholder and the row already has a real name."""
    if from_manifest == current:
        return False
    manifest_is_placeholder = from_manifest.startswith(AUTHOR_PLACEHOLDER_PREFIX)
    current_is_real = bool(current) and not current.startswith(AUTHOR_PLACEHOLDER_PREFIX)
    return not (manifest_is_placeholder and current_is_real)


def sync_entry(entry: dict) -> tuple[str, bool]:
    """Create or update the MediaAsset for one manifest entry. Returns (status, file_copied)."""
    from cms.models import MediaAsset

    stored_name, copied = ensure_stored(entry)
    downloaded_on = dt.date.fromisoformat(entry["downloaded_on"]) if entry.get("downloaded_on") else None
    facts = {  # always re-synchronised from the manifest (pipeline facts, not editorial choices)
        "license": _license_code(entry["license"]),
        "downloaded_on": downloaded_on,
        "stereotype_checked": bool(entry["forbidden_subject_check"]),
    }
    manifest_author = entry["author"][:160]
    asset = MediaAsset.objects.filter(source_url=entry["source_url"]).order_by("pk").first()
    if asset is None:
        asset = MediaAsset(
            source_url=entry["source_url"],
            title=entry["title_fr"][:160],
            alt_fr=entry["alt_fr"][:200],
            author=manifest_author,
            license_notes=_provenance_note(entry),
            is_decorative=False,
            **facts,
        )
        asset.file.name = stored_name
        asset.width, asset.height = None, None
        asset.save()
        return "created", copied

    changed = False
    for field_name, value in facts.items():
        if getattr(asset, field_name) != value:
            setattr(asset, field_name, value)
            changed = True
    if author_should_sync(asset.author, manifest_author):
        asset.author, changed = manifest_author, True
    if not asset.title:
        asset.title, changed = entry["title_fr"][:160], True
    if not asset.alt_fr:
        asset.alt_fr, changed = entry["alt_fr"][:200], True
    if not asset.license_notes:
        asset.license_notes, changed = _provenance_note(entry), True
    if asset.file.name != stored_name or copied:
        asset.file.name, changed = stored_name, True
        asset.width, asset.height = None, None  # recomputed from the (new) file on save
    if changed:
        asset.save()
    return ("updated" if changed else "unchanged"), copied


def seed() -> str:
    """Idempotent entry point used by ``cms.seeds`` — returns a one-line summary."""
    entries = load_manifest()
    if not entries:
        return "media library: no manifest (run scripts/fetch_images.py)"
    counts = {"created": 0, "updated": 0, "unchanged": 0}
    copied = 0
    with transaction.atomic():
        for entry in entries:
            status, was_copied = sync_entry(entry)
            counts[status] += 1
            copied += int(was_copied)
    summary = (
        f"media library: {len(entries)} image(s) — {counts['created']} created, {counts['updated']} updated, "
        f"{counts['unchanged']} unchanged, {copied} file(s) copied to storage"
    )
    log.info(summary)
    return summary
