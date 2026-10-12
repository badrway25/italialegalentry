"""
Curated, self-hosted photo library for Italy Legal Entry™ (art direction: docs/IMAGE_LICENSES.md).

Run from the project root::

    .venv/Scripts/python scripts/fetch_images.py [--cache-dir DIR] [--force] [--only SLUG ...] [--check]

What it does (idempotently):

1. downloads the ORIGINAL of every curated photo into a cache directory outside the repository
   (never committed; default: <system temp>/ile-image-originals). Two sources are supported and
   each candidate names its own: ``unsplash`` (a CDN URL built from the photo id, no key) and
   ``pexels`` (the id is resolved through api.pexels.com, which needs ``PEXELS_API_KEY`` in the
   environment and hands back the original URL AND the photographer's name — so a Pexels entry
   carries a real author instead of a placeholder, which is what the Pexels License asks for);
2. applies the optional editorial treatments recorded for the photo — feathered blur of incidental
   brand marks / third-party text (``redact``) and a crop (``crop``); both licences allow
   modification and every treatment is recorded in the manifest with its reason;
3. strips every metadata block (EXIF/XMP/ICC) and generates responsive derivatives with Pillow:
   ``static/img/photos/<slug>-{480,960,1440,1920}.webp`` (quality ~78) plus a ``<slug>-1440.jpg``
   fallback (quality 80). Derivatives are never upscaled; each file is kept under 350 KB;
4. writes ``static/img/photos/manifest.json`` (provenance, licence, usage slot, alt text, sizes) and
   removes derivatives of photos that are no longer curated.

``apps/cms/seeds_media.py`` turns the manifest into ``cms.MediaAsset`` rows.

Editorial rules (Implementation document §3.1 note, forbidden registry F15): subjects are
enterprises, training, universities, institutional rooms, cooperation, workshops, professionals.
Never borders, luggage, waiting lines, passports, airports, doorways, grids or tourist clichés.
No logo, no readable third-party text, no recognisable branded product (docs/IMAGE_LICENSES.md §1.5).
Every candidate was downloaded and reviewed visually before entering ``CURATED``; rejected
candidates are listed in ``REJECTED`` with the reason, so nobody re-evaluates them by mistake.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "static" / "img" / "photos"
MANIFEST_PATH = PHOTOS_DIR / "manifest.json"

# Download only — hotlinking is forbidden by the project's CSP and by F24. 2400px originals so
# that a genuine 1920px derivative exists for full-width heroes.
DOWNLOAD_WIDTH = 2400


@dataclass(frozen=True)
class Source:
    """Where a curated photograph comes from, and what its licence obliges us to record."""

    key: str
    license_name: str
    license_url: str
    page_url: str  # the human page for the photo, recorded in the manifest as source_url
    author_fallback: str
    api_key_env: str = ""  # set when the id has to be resolved through an API before downloading


SOURCES: dict[str, Source] = {
    "unsplash": Source(
        key="unsplash",
        license_name="Unsplash License",
        license_url="https://unsplash.com/license",
        page_url="https://unsplash.com/photos/{photo_id}",
        author_fallback="Unsplash contributor (author lookup unavailable offline)",
    ),
    "pexels": Source(
        key="pexels",
        license_name="Pexels License",
        license_url="https://www.pexels.com/license/",
        page_url="https://www.pexels.com/photo/{photo_id}/",
        author_fallback="Pexels contributor (author lookup unavailable offline)",
        api_key_env="PEXELS_API_KEY",
    ),
}

UNSPLASH_DOWNLOAD_URL = "https://images.unsplash.com/photo-{photo_id}?w={width}&q=82&fm=jpg"
PEXELS_PHOTO_API = "https://api.pexels.com/v1/photos/{photo_id}"

#: Kept so a manifest written before two sources existed still reads. New code asks the Source.
LICENSE_NAME = SOURCES["unsplash"].license_name
LICENSE_URL = SOURCES["unsplash"].license_url
SOURCE_URL = SOURCES["unsplash"].page_url
AUTHOR_FALLBACK = SOURCES["unsplash"].author_fallback
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
)
# Crop and redaction boxes are expressed on a 1800px-wide reference frame of the ORIGINAL (before
# any crop) and scaled to the downloaded file.
CROP_REFERENCE_WIDTH = 1800

WEBP_WIDTHS = (480, 960, 1440, 1920)
JPG_WIDTH = 1440
WEBP_QUALITY = 78
JPG_QUALITY = 80
MAX_BYTES = 350 * 1024
MIN_QUALITY = 45

DERIVATIVE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-\d+\.(?:webp|jpg)$")
OS_ARTEFACTS = frozenset({"Thumbs.db", ".DS_Store", "desktop.ini"})

# Words that must never describe a library image (slug, title, alt text). Kept in sync with
# ``cms.seeds_media.FORBIDDEN_SUBJECT_KEYWORDS`` (a test asserts both lists are identical).
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

Box = tuple[int, int, int, int]  # (left, upper, right, lower) on the 1800px-wide reference frame


@dataclass(frozen=True)
class Candidate:
    photo_id: str
    slug: str
    usage_slot: str
    subject: str
    title_fr: str
    alt_fr: str
    crop: Box | None = None
    crop_reason: str = ""
    redact: tuple[Box, ...] = ()  # feathered blur of incidental brand marks / third-party text (before crop)
    redact_reason: str = ""
    #: Which library the id belongs to — see SOURCES. Defaulted, so the fifteen photographs curated
    #: before a second source existed keep reading exactly as they were written.
    source: str = "unsplash"


# Accepted photos — every one downloaded and viewed at full size before inclusion (builder) and
# reviewed a second time independently (review 2026-09-17: four photos needed redactions).
CURATED: tuple[Candidate, ...] = (
    Candidate(
        "1517048676732-d65bc937f952",
        "reunion-cooperation",
        "hero",
        "Réunion de travail entre professionnels, prise de notes, lumière naturelle",
        "Réunion de coopération",
        "Professionnels réunis autour d’une table de réunion, prenant des notes pendant un échange de travail",
    ),
    Candidate(
        "1454165804606-c3d57bc86b40",
        "entretien-accompagnement",
        "entrance_person",
        "Deux personnes travaillent avec ordinateurs et carnet lors d’un entretien",
        "Entretien d’accompagnement",
        "Deux personnes travaillent côte à côte avec des ordinateurs et un carnet de notes pendant un entretien",
    ),
    Candidate(
        "1522202176988-66273c2fd55f",
        "equipe-entreprise",
        "entrance_company",
        "Trois collègues échangent autour d’une table de travail",
        "Équipe d’entreprise",
        "Trois collègues échangent avec le sourire autour d’une table de travail équipée d’ordinateurs",
        redact=((570, 520, 815, 758), (1075, 642, 1130, 672), (1095, 732, 1170, 768)),
        redact_reason="blurs the left screen (third-party website) and manufacturer marks on both computers",
    ),
    Candidate(
        "1517245386807-bb43f82c33c4",
        "dialogue-institutionnel",
        "entrance_institution",
        "Participant qui prend la parole en réunion",
        "Dialogue en réunion",
        "Participant qui prend la parole pendant une réunion de travail, ordinateur et carnet ouverts devant lui",
    ),
    Candidate(
        "1523240795612-9a054b0db644",
        "etudiants-bibliotheque",
        "entrance_university",
        "Étudiants qui travaillent ensemble dans une bibliothèque",
        "Étudiants en bibliothèque",
        "Étudiants qui rient en travaillant ensemble dans une bibliothèque universitaire",
        redact=((705, 640, 800, 712), (815, 805, 1050, 925)),
        redact_reason="blurs a sports-team script on a cap and a printed brand on a sweatshirt",
    ),
    Candidate(
        "1540575467063-178a50c2df87",
        "public-conference",
        "forum_event",
        "Public assis dans une salle de conférence",
        "Public d’une conférence",
        "Public attentif assis dans une salle de conférence pendant une intervention",
    ),
    Candidate(
        "1524178232363-1fb2b075b655",
        "salle-de-formation",
        "training_classroom",
        "Formateur devant des participants dans une salle de formation",
        "Salle de formation",
        "Salle de formation : un formateur s’adresse à des participants assis en rangées",
        crop=(560, 0, 1800, 1200),
        crop_reason="removes the projected screen (readable third-party text)",
        redact=((624, 602, 656, 634), (604, 615, 632, 647)),
        redact_reason="blurs a social-network sticker and a manufacturer logo on the podium computer",
    ),
    Candidate(
        "1562774053-701939374585",
        "campus-universitaire",
        "university",
        "Façade d’un bâtiment universitaire et pelouse",
        "Campus universitaire",
        "Façade d’un bâtiment universitaire donnant sur une pelouse entourée d’arbres",
    ),
    Candidate(
        "1552664730-d307ca884978",
        "atelier-de-travail",
        "workshop",
        "Atelier : notes adhésives au mur, équipe autour d’une table",
        "Atelier de travail",
        "Atelier de travail : une animatrice organise des notes adhésives sur un mur devant une équipe",
    ),
    Candidate(
        "1475721027785-f74eccf877e2",
        "micro-conference",
        "news_default",
        "Micro sur pied devant une salle de conférence",
        "Micro de conférence",
        "Micro sur pied au premier plan, devant une salle de conférence en arrière-plan flou",
    ),
    Candidate(
        "1516321318423-f06f85e504b3",
        "orientation-ecran",
        "orientation",
        "Main qui pointe un élément à l’écran d’un ordinateur",
        "Séance d’orientation",
        "Main qui pointe un élément à l’écran d’un ordinateur pendant une séance d’orientation",
    ),
    Candidate(
        "1434030216411-0b793f4b4173",
        "demarches-ecriture",
        "living",
        "Personne qui remplit des documents à la main",
        "Démarches quotidiennes",
        "Personne qui remplit des documents à la main sur une table, avec une tasse et un carnet",
    ),
    Candidate(
        "1519389950473-47ba0277781c",
        "espace-de-travail",
        "reserved_area",
        "Vue de dessus d’un espace de travail partagé",
        "Espace de travail",
        "Vue de dessus d’un espace de travail avec ordinateurs, carnets et casque audio",
        crop=(0, 0, 1150, 1200),
        crop_reason="removes visible brand marks on a laptop and a charger",
        redact=((422, 598, 454, 636),),
        redact_reason="blurs the maker's emblem on an external drive",
    ),
    Candidate(
        "1600880292203-757bb62b4baf",
        "collaboration-bureau",
        "cooperation",
        "Deux collègues se félicitent dans un bureau",
        "Collaboration",
        "Deux collègues se félicitent en se tapant dans la main, dans un bureau aux murs de briques",
    ),
    Candidate(
        "1568667256549-094345857637",
        "bibliotheque-savoir",
        "academic",
        "Grande bibliothèque circulaire (format portrait)",
        "Bibliothèque",
        "Grande bibliothèque circulaire aux rayonnages remplis de livres",
    ),
)

# Candidates reviewed and discarded (photo id → reason). Keep for traceability.
REJECTED: dict[str, str] = {
    "1521737604893-d14cc237f11d": "large glass doorways dominate the background (F15: no doorways)",
    "1541339907198-e08756dedf3f": "graduation cliché with an identifiable non-European skyline",
    "1531482615713-2afd69097998": "a door is a visible element of the background (conservative reading of F15)",
    "1556761175-b413da4baf72": "wall lettering and a branded can in frame",
    "1573164713714-d95e436ab8d6": "brand product shot (tablet-laptop with vendor desktop)",
    "1497366216548-37526070297c": "long corridor of glass partitions reads as grid/doorway",
    "1523580494863-6f3031224c94": "third-party logo visible on the stage screens",
    "1505373877841-8d25f7d46678": "third-party product interface is the subject of the slide",
    "1553877522-43269d4ea984": "manufacturer logo visible on a computer; low-contrast monochrome",
    "1529156069898-49953e39b3ac": "tourist/leisure scene unrelated to the platform",
    "1455390582262-044cdead277a": "brand name engraved on the pen nib",
    "1486406146926-c627a92ad1ab": "corporate towers with grid façades, no link with contemporary Italy",
    "1513584684374-8bab748fbf90": "private villa with seasonal decorations, off subject",
}


@dataclass
class ManifestEntry:
    photo_id: str
    source: str
    slug: str
    usage_slot: str
    subject: str
    title_fr: str
    alt_fr: str
    author: str
    source_url: str
    license: str
    license_url: str
    downloaded_on: str
    width: int
    height: int
    source_width: int
    source_height: int
    crop: list[int] | None
    crop_reason: str
    redact: list[list[int]] | None
    redact_reason: str
    original_sha256: str
    files: dict[str, object] = field(default_factory=dict)
    forbidden_subject_check: bool = True

    @classmethod
    def from_manifest(cls, data: dict) -> ManifestEntry:
        """Build an entry from a manifest written by an earlier version of this script."""
        known = set(cls.__dataclass_fields__)
        payload = {k: v for k, v in data.items() if k in known}
        payload.setdefault("redact", None)
        payload.setdefault("redact_reason", "")
        payload.setdefault("source", "unsplash")  # manifests written before a second source existed
        return cls(**payload)


class PipelineError(RuntimeError):
    pass


# ------------------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------------------
def forbidden_keyword_hits(*texts: str) -> list[str]:
    hits = []
    for text in texts:
        lowered = (text or "").lower()
        hits.extend(k for k in FORBIDDEN_SUBJECT_KEYWORDS if k in lowered)
    return sorted(set(hits))


def _box_is_well_formed(box: Box) -> bool:
    return (
        len(box) == 4
        and all(isinstance(v, int) for v in box)
        and 0 <= box[0] < box[2] <= CROP_REFERENCE_WIDTH
        and 0 <= box[1] < box[3]
    )


def validate_candidates(candidates: tuple[Candidate, ...]) -> None:
    slugs = [c.slug for c in candidates]
    if len(slugs) != len(set(slugs)):
        raise PipelineError("duplicate slugs in CURATED")
    for c in candidates:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", c.slug):
            raise PipelineError(f"{c.slug}: slug must be lowercase ascii with dashes")
        hits = forbidden_keyword_hits(c.slug, c.title_fr, c.alt_fr, c.subject)
        if hits:
            raise PipelineError(f"{c.slug}: forbidden subject keyword(s) {hits}")
        if len(c.alt_fr) > 200:
            raise PipelineError(f"{c.slug}: alt_fr longer than 200 characters")
        if c.source not in SOURCES:
            raise PipelineError(f"{c.slug}: unknown source {c.source!r} (known: {sorted(SOURCES)})")
        if c.photo_id in REJECTED:
            raise PipelineError(f"{c.slug}: photo {c.photo_id} is in REJECTED")
        if c.crop and (not _box_is_well_formed(c.crop) or not c.crop_reason):
            raise PipelineError(f"{c.slug}: crop must be a well-formed box with a reason")
        if c.redact and not c.redact_reason:
            raise PipelineError(f"{c.slug}: redaction boxes need a redact_reason")
        for box in c.redact:
            if not _box_is_well_formed(box):
                raise PipelineError(f"{c.slug}: malformed redaction box {box}")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fetch(url: str, headers: dict[str, str], what: str) -> bytes:
    if not url.startswith("https://"):
        raise PipelineError(f"{what}: refusing non-https download")
    request = urllib.request.Request(url, headers=headers)  # noqa: S310 - https enforced above
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - https enforced above
            return response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise PipelineError(f"{what}: download failed ({exc})") from exc


def resolve_pexels(photo_id: str, cache_dir: Path) -> tuple[str, str]:
    """
    Ask the Pexels API for one photo: (original URL, photographer).

    The id alone is not enough — Pexels serves originals from a per-photo path — and the licence
    asks for the photographer to be credited. Both arrive in the same call, so a Pexels entry
    carries a real author instead of the placeholder an offline Unsplash entry has to settle for.
    The answer is cached beside the image: once the originals are in the cache the pipeline runs
    offline, which is how `--check` works on a machine with no key.
    """
    meta_path = cache_dir / f"pexels-{photo_id}.json"
    if meta_path.exists():
        cached = json.loads(meta_path.read_text(encoding="utf-8"))
        return cached["original"], cached["photographer"]

    key = os.environ.get(SOURCES["pexels"].api_key_env, "").strip()
    if not key:
        raise PipelineError(
            f"pexels:{photo_id}: {SOURCES['pexels'].api_key_env} is not set and the original is "
            f"not cached in {cache_dir}"
        )
    payload = json.loads(
        _fetch(
            PEXELS_PHOTO_API.format(photo_id=photo_id),
            {"Authorization": key, "User-Agent": USER_AGENT},
            f"pexels:{photo_id}",
        ).decode("utf-8")
    )
    original = ((payload.get("src") or {}).get("original") or "").strip()
    photographer = (payload.get("photographer") or "").strip()
    if not original:
        raise PipelineError(f"pexels:{photo_id}: the API answer carries no original URL")
    cache_dir.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(
        json.dumps({"original": original, "photographer": photographer}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    return original, photographer


def download_original(candidate: Candidate, cache_dir: Path) -> tuple[Path, str]:
    """
    Fetch the original once; later runs reuse the cached file. Returns (path, author or "").

    The author is only ever known here for Pexels, where it arrives with the URL. Unsplash's is
    completed by hand in the manifest and never overwritten by the placeholder (seeds_media).
    """
    source = SOURCES[candidate.source]
    photo_id = candidate.photo_id
    target = cache_dir / f"{source.key}-{photo_id}-w{DOWNLOAD_WIDTH}.jpg"
    legacy = cache_dir / f"{photo_id}-w{DOWNLOAD_WIDTH}.jpg"  # cached before sources existed
    if source.key == "unsplash" and legacy.exists() and not target.exists():
        target = legacy

    author = ""
    if source.key == "pexels":
        url, author = resolve_pexels(photo_id, cache_dir)
    else:
        url = UNSPLASH_DOWNLOAD_URL.format(photo_id=photo_id, width=DOWNLOAD_WIDTH)

    if target.exists() and target.stat().st_size > 0:
        return target, author

    data = _fetch(url, {"User-Agent": USER_AGENT}, f"{source.key}:{photo_id}")
    if not data.startswith(b"\xff\xd8"):
        raise PipelineError(f"{source.key}:{photo_id}: downloaded payload is not a JPEG")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return target, author


def apply_redactions(image: Image.Image, boxes: tuple[Box, ...], scale: float) -> Image.Image:
    """
    Blur each box (reference frame → scaled to ``image``) with a feathered edge so that incidental
    brand marks or third-party text become unreadable without a hard-edged patch.
    """
    for box in boxes:
        left, upper, right, lower = (round(v * scale) for v in box)
        right, lower = min(right, image.width), min(lower, image.height)
        if not (0 <= left < right and 0 <= upper < lower):
            raise PipelineError(f"redaction {box} outside the {image.size} original")
        radius = max(6.0, min(right - left, lower - upper) / 4)
        pad = int(radius * 2)
        pl, pu = max(0, left - pad), max(0, upper - pad)
        pr, plo = min(image.width, right + pad), min(image.height, lower + pad)
        region = image.crop((pl, pu, pr, plo))
        blurred = region.filter(ImageFilter.GaussianBlur(radius))
        mask = Image.new("L", region.size, 0)
        ImageDraw.Draw(mask).rectangle((left - pl, upper - pu, right - pl - 1, lower - pu - 1), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(max(2.0, radius / 3)))
        image.paste(blurred, (pl, pu), mask)
    return image


def load_master(path: Path, crop: Box | None, redact: tuple[Box, ...] = ()) -> tuple[Image.Image, tuple[int, int]]:
    """Open the original, honour orientation, drop every metadata block, apply redactions then the crop."""
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im) or im
        source_size = im.size
        rgb = im.convert("RGB")
    scale = source_size[0] / CROP_REFERENCE_WIDTH
    if redact:
        rgb = apply_redactions(rgb, redact, scale)
    if crop:
        left, upper, right, lower = (round(v * scale) for v in crop)
        right, lower = min(right, source_size[0]), min(lower, source_size[1])
        if not (0 <= left < right and 0 <= upper < lower):
            raise PipelineError(f"crop {crop} outside the {source_size} original")
        rgb = rgb.crop((left, upper, right, lower))
    clean = Image.new("RGB", rgb.size)
    clean.paste(rgb)  # a fresh image carries no EXIF/XMP/ICC
    return clean, source_size


def encode_under_limit(image: Image.Image, fmt: str, quality: int) -> bytes:
    """Encode at the requested quality, lowering quality (then size) until under MAX_BYTES."""
    current = image
    q = quality
    while True:
        buf = io.BytesIO()
        if fmt == "WEBP":
            current.save(buf, "WEBP", quality=q, method=6)
        else:
            current.save(buf, "JPEG", quality=q, optimize=True, progressive=True, subsampling=2)
        data = buf.getvalue()
        if len(data) <= MAX_BYTES:
            return data
        if q > MIN_QUALITY:
            q -= 6
            continue
        new_w = int(current.width * 0.9)
        if new_w < 320:
            raise PipelineError("cannot fit derivative under the size limit")
        current = current.resize((new_w, round(current.height * new_w / current.width)), Image.Resampling.LANCZOS)
        q = quality


def resized(master: Image.Image, width: int) -> Image.Image:
    if width >= master.width:
        return master
    return master.resize((width, round(master.height * width / master.width)), Image.Resampling.LANCZOS)


def derivative_plan(master_width: int) -> tuple[list[int], int]:
    """Widths to emit (never upscaled) and the JPG fallback width."""
    widths = [w for w in WEBP_WIDTHS if w <= master_width]
    if master_width < WEBP_WIDTHS[-1] and master_width not in widths and master_width < JPG_WIDTH:
        widths.append(master_width)  # keep the master itself when it is narrower than 1440
    return sorted(widths), min(JPG_WIDTH, master_width)


def existing_entry(manifest: dict, slug: str) -> dict | None:
    for entry in manifest.get("images", []):
        if entry.get("slug") == slug:
            return entry
    return None


def entry_file_names(entry: dict) -> list[str]:
    files = entry.get("files") or {}
    return [str(n) for n in [*(files.get("webp") or {}).values(), files.get("jpg")] if n]


def derivatives_present(entry: dict | None) -> bool:
    if not entry:
        return False
    names = entry_file_names(entry)
    return bool(names) and all((PHOTOS_DIR / name).exists() for name in names)


def derivative_files(slug: str) -> list[Path]:
    """Existing derivatives of exactly this slug (``atelier`` never matches ``atelier-de-travail-480.webp``)."""
    pattern = re.compile(rf"^{re.escape(slug)}-\d+\.(?:webp|jpg)$")
    if not PHOTOS_DIR.exists():
        return []
    return sorted(p for p in PHOTOS_DIR.iterdir() if p.is_file() and pattern.match(p.name))


def orphan_files(referenced: set[str]) -> list[Path]:
    """Derivative-shaped files in the photo directory that no manifest entry references."""
    if not PHOTOS_DIR.exists():
        return []
    return sorted(
        p for p in PHOTOS_DIR.iterdir() if p.is_file() and p.name not in referenced and DERIVATIVE_NAME.match(p.name)
    )


def stray_files(referenced: set[str]) -> list[Path]:
    """Any file in the photo directory that is neither referenced nor an OS artefact."""
    if not PHOTOS_DIR.exists():
        return []
    return sorted(
        p for p in PHOTOS_DIR.iterdir() if p.is_file() and p.name not in referenced and p.name not in OS_ARTEFACTS
    )


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"images": []}


def write_manifest(entries: list[ManifestEntry]) -> None:
    used = sorted({e.source for e in entries} or {"unsplash"})
    payload = {
        "generated_by": "scripts/fetch_images.py",
        # The libraries actually present, each with its licence. There used to be one `license`
        # key here naming Unsplash; with two sources that key could only ever be half true, and
        # the licence that binds a given file is the one on that file's own entry.
        "sources": {
            name: {"license": SOURCES[name].license_name, "license_url": SOURCES[name].license_url} for name in used
        },
        "policy": "Self-hosted only. Never hotlink. Every image reviewed against forbidden subjects (F15).",
        "derivative_widths": list(WEBP_WIDTHS),
        "max_bytes_per_file": MAX_BYTES,
        "images": [asdict(e) for e in sorted(entries, key=lambda e: e.slug)],
    }
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _crop_as_list(crop: Box | None) -> list[int] | None:
    return list(crop) if crop else None


def _redact_as_list(redact: tuple[Box, ...]) -> list[list[int]] | None:
    return [list(box) for box in redact] or None


# ------------------------------------------------------------------------------------------
# Pipeline
# ------------------------------------------------------------------------------------------
def process(
    candidate: Candidate,
    original: Path,
    previous: dict | None,
    force: bool,
    resolved_author: str = "",
) -> tuple[ManifestEntry, bool]:
    """`resolved_author` is filled by the download step when the source names the photographer."""
    digest = sha256_of(original)
    unchanged = (
        previous is not None
        and previous.get("original_sha256") == digest
        and previous.get("crop") == _crop_as_list(candidate.crop)
        and (previous.get("redact") or None) == _redact_as_list(candidate.redact)
        and derivatives_present(previous)
    )
    master, source_size = load_master(original, candidate.crop, candidate.redact)
    widths, jpg_width = derivative_plan(master.width)
    files: dict[str, object] = {"webp": {}, "jpg": f"{candidate.slug}-{jpg_width}.jpg"}
    for width in widths:
        files["webp"][str(width)] = f"{candidate.slug}-{width}.webp"

    if not (unchanged and not force):
        PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        for stale in derivative_files(candidate.slug):
            stale.unlink()
        for width in widths:
            data = encode_under_limit(resized(master, width), "WEBP", WEBP_QUALITY)
            (PHOTOS_DIR / files["webp"][str(width)]).write_bytes(data)
        data = encode_under_limit(resized(master, jpg_width), "JPEG", JPG_QUALITY)
        (PHOTOS_DIR / files["jpg"]).write_bytes(data)

    source = SOURCES[candidate.source]
    entry = ManifestEntry(
        photo_id=candidate.photo_id,
        source=candidate.source,
        slug=candidate.slug,
        usage_slot=candidate.usage_slot,
        subject=candidate.subject,
        title_fr=candidate.title_fr,
        alt_fr=candidate.alt_fr,
        author=resolved_author or (previous or {}).get("author") or source.author_fallback,
        source_url=source.page_url.format(photo_id=candidate.photo_id),
        license=source.license_name,
        license_url=source.license_url,
        downloaded_on=(previous or {}).get("downloaded_on") or dt.date.today().isoformat(),
        width=master.width,
        height=master.height,
        source_width=source_size[0],
        source_height=source_size[1],
        crop=_crop_as_list(candidate.crop),
        crop_reason=candidate.crop_reason,
        redact=_redact_as_list(candidate.redact),
        redact_reason=candidate.redact_reason,
        original_sha256=digest,
        files=files,
        forbidden_subject_check=True,
    )
    return entry, not (unchanged and not force)


def check_only() -> int:
    """Offline verification of CURATED, the manifest and the files on disk (no network)."""
    manifest = load_manifest()
    images = manifest.get("images", [])
    problems = []
    try:
        validate_candidates(CURATED)
    except PipelineError as exc:
        problems.append(f"CURATED: {exc}")
    manifest_slugs = {e.get("slug") for e in images}
    curated_slugs = {c.slug for c in CURATED}
    if manifest_slugs != curated_slugs:
        problems.append(f"manifest and CURATED differ: {sorted(manifest_slugs ^ curated_slugs)}")
    referenced = {MANIFEST_PATH.name}
    for entry in images:
        for name in entry_file_names(entry):
            referenced.add(name)
            path = PHOTOS_DIR / name
            if not path.exists():
                problems.append(f"missing {name}")
            elif path.stat().st_size > MAX_BYTES:
                problems.append(f"{name} exceeds {MAX_BYTES} bytes")
        hits = forbidden_keyword_hits(
            entry.get("slug", ""), entry.get("title_fr", ""), entry.get("alt_fr", ""), entry.get("subject", "")
        )
        if hits:
            problems.append(f"{entry.get('slug')}: forbidden keywords {hits}")
        if entry.get("redact") and not entry.get("redact_reason"):
            problems.append(f"{entry.get('slug')}: redaction without reason")
    problems.extend(f"stray file {p.name}" for p in stray_files(referenced))
    for problem in problems:
        print("PROBLEM:", problem)
    print(f"{len(images)} image(s) in manifest, {len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--cache-dir", type=Path, default=Path(tempfile.gettempdir()) / "ile-image-originals")
    parser.add_argument("--force", action="store_true", help="regenerate derivatives even when unchanged")
    parser.add_argument("--only", nargs="*", default=None, help="process only these slugs")
    parser.add_argument("--check", action="store_true", help="verify the manifest offline and exit")
    args = parser.parse_args(argv)

    if args.check:
        return check_only()

    validate_candidates(CURATED)
    manifest = load_manifest()
    selected = [c for c in CURATED if not args.only or c.slug in args.only]
    entries: list[ManifestEntry] = []
    regenerated = 0
    for candidate in selected:
        original, resolved_author = download_original(candidate, args.cache_dir)
        entry, changed = process(
            candidate, original, existing_entry(manifest, candidate.slug), args.force, resolved_author
        )
        regenerated += int(changed)
        entries.append(entry)
        state = "built" if changed else "kept "
        print(f"{state} {candidate.slug:28} {entry.width}x{entry.height} slot={entry.usage_slot}")

    if args.only:  # keep the entries that were not selected this run
        selected_slugs = {c.slug for c in selected}
        entries.extend(
            ManifestEntry.from_manifest(e) for e in manifest.get("images", []) if e.get("slug") not in selected_slugs
        )
    write_manifest(entries)

    referenced = {MANIFEST_PATH.name}
    for entry in entries:
        referenced.update(entry_file_names(asdict(entry)))
    if not args.only:  # a partial run must not judge the derivatives it did not look at
        for orphan in orphan_files(referenced):
            orphan.unlink()
            print(f"removed orphan derivative {orphan.name}")
    for stray in stray_files(referenced):
        print(f"WARNING: unexpected file {stray.name} in {PHOTOS_DIR} (not removed)")
    print(f"manifest: {MANIFEST_PATH} — {len(entries)} image(s), {regenerated} regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
