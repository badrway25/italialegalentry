"""
Photo library: manifest integrity, file limits, forbidden-subject vocabulary and idempotent seeding.

Files come from ``scripts/fetch_images.py`` (committed derivatives under static/img/photos);
rows come from ``cms.seeds_media.seed()`` (called by ``cms.seeds``).
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management import call_command
from PIL import Image

from cms import seeds_media
from cms.models import MediaAsset, MediaLicense

pytestmark = pytest.mark.compliance

PHOTOS_DIR = Path(settings.BASE_DIR) / "static" / "img" / "photos"
MANIFEST = PHOTOS_DIR / "manifest.json"
SCRIPT = Path(settings.BASE_DIR) / "scripts" / "fetch_images.py"
MAX_BYTES = 350 * 1024
# Vocabulary from the task brief (F15): nothing in a slug, title or alt text may contain these.
FORBIDDEN = (
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
REQUIRED_SLOTS = {
    "hero",
    "entrance_person",
    "entrance_company",
    "entrance_institution",
    "entrance_university",
    "forum_event",
    "training_classroom",
    "university",
    "workshop",
    "news_default",
    "orientation",
    "living",
    "reserved_area",
}
# Institutional logos must never be shipped as static files (gate G6).
FORBIDDEN_FILENAME_PARTS = ("veneto", "rovigo", "regione", "comune", "logo")


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def images(manifest) -> list[dict]:
    return manifest["images"]


@pytest.fixture
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    return settings.MEDIA_ROOT


def _script_module():
    """Load scripts/fetch_images.py as a module (registered in sys.modules for dataclasses)."""
    name = "ile_fetch_images_under_test"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ------------------------------------------------------------------------------------------
# Manifest & files
# ------------------------------------------------------------------------------------------
def test_manifest_is_valid_json_with_curated_size(manifest, images):
    # The header names the libraries actually present, each with its licence. It used to name one
    # licence for the whole file; with a second source (Pexels, added for the V3 image system) that
    # key could only ever be half true, and the licence that binds a file is the one on its own entry.
    assert set(manifest["sources"]) <= {"unsplash", "pexels"}
    assert manifest["sources"], "the manifest must say which libraries it draws on"
    for name, info in manifest["sources"].items():
        assert info["license"] and info["license_url"].startswith("https://"), name
    assert 14 <= len(images) <= 20
    slugs = [i["slug"] for i in images]
    assert len(slugs) == len(set(slugs))
    for entry in images:
        for key in seeds_media.REQUIRED_ENTRY_KEYS:
            assert key in entry, (entry["slug"], key)
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["slug"])
        assert entry["forbidden_subject_check"] is True
        source = entry.get("source", "unsplash")
        assert source in manifest["sources"], (entry["slug"], source)
        assert entry["license"] == manifest["sources"][source]["license"]
        expected_host = {"unsplash": "https://unsplash.com/photos/", "pexels": "https://www.pexels.com/photo/"}
        assert entry["source_url"].startswith(expected_host[source]), entry["source_url"]
        # The page URL, never the CDN: hotlinking is forbidden by the CSP and by F24, and a manifest
        # that carries the CDN host is a manifest somebody will eventually hotlink from.
        for cdn in ("images.unsplash.com", "images.pexels.com"):
            assert cdn not in json.dumps(entry), f"manifest must not carry the hotlink host {cdn}"
        assert entry["author"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["downloaded_on"])
        assert 0 < len(entry["alt_fr"]) <= 200
        assert 0 < len(entry["title_fr"]) <= 160


def test_every_usage_slot_is_covered(images):
    slots = {i["usage_slot"] for i in images}
    assert REQUIRED_SLOTS <= slots, REQUIRED_SLOTS - slots


def test_every_referenced_file_exists_within_limits(images):
    for entry in images:
        files = entry["files"]
        assert files["webp"], entry["slug"]
        names = [*files["webp"].values(), files["jpg"]]
        for name in names:
            path = PHOTOS_DIR / name
            assert path.exists(), name
            assert path.stat().st_size <= MAX_BYTES, (name, path.stat().st_size)
            assert name.startswith(entry["slug"] + "-")
        for width, name in files["webp"].items():
            with Image.open(PHOTOS_DIR / name) as im:
                assert im.format == "WEBP"
                assert im.width == int(width), name
                assert im.width <= entry["width"], "derivatives are never upscaled"
        with Image.open(PHOTOS_DIR / files["jpg"]) as im:
            assert im.format == "JPEG"
            assert im.width <= 1440


def test_hero_has_full_width_derivative(images):
    hero = next(i for i in images if i["usage_slot"] == "hero")
    assert "1920" in hero["files"]["webp"]
    assert hero["width"] >= 1920


def test_derivatives_carry_no_metadata(images):
    for entry in images:
        names = [*entry["files"]["webp"].values(), entry["files"]["jpg"]]
        for name in names:
            with Image.open(PHOTOS_DIR / name) as im:
                assert not im.getexif(), name
                assert "exif" not in im.info and "xmp" not in im.info and "icc_profile" not in im.info, name


def test_no_stray_files_in_photo_directory(images):
    referenced = {MANIFEST.name}
    for entry in images:
        referenced.update(entry["files"]["webp"].values())
        referenced.add(entry["files"]["jpg"])
    on_disk = {p.name for p in PHOTOS_DIR.iterdir() if p.is_file()}
    assert on_disk == referenced, on_disk ^ referenced


def test_no_forbidden_subject_keywords(images):
    for entry in images:
        blob = " ".join([entry["slug"], entry["title_fr"], entry["alt_fr"], entry.get("subject", "")]).lower()
        hits = [k for k in FORBIDDEN if k in blob]
        assert not hits, (entry["slug"], hits)
        for name in [*entry["files"]["webp"].values(), entry["files"]["jpg"]]:
            assert not [k for k in FORBIDDEN if k in name.lower()], name


def test_no_institutional_logo_files_in_static_img():
    static_img = Path(settings.BASE_DIR) / "static" / "img"
    offenders = [
        p.name
        for p in static_img.rglob("*")
        if p.is_file() and any(part in p.name.lower() for part in FORBIDDEN_FILENAME_PARTS)
    ]
    assert not offenders, offenders


def test_keyword_lists_are_identical_in_script_and_seed():
    module = _script_module()
    assert tuple(module.FORBIDDEN_SUBJECT_KEYWORDS) == tuple(seeds_media.FORBIDDEN_SUBJECT_KEYWORDS) == FORBIDDEN
    module.validate_candidates(module.CURATED)  # slugs, alt lengths, keywords, rejected overlap
    assert {c.photo_id for c in module.CURATED}.isdisjoint(module.REJECTED)


def test_script_check_mode_passes_offline(capsys):
    module = _script_module()
    assert module.main(["--check"]) == 0
    assert "0 problem(s)" in capsys.readouterr().out


def test_manifest_matches_curated_list(images):
    module = _script_module()
    assert {c.slug for c in module.CURATED} == {i["slug"] for i in images}
    for c in module.CURATED:
        entry = next(i for i in images if i["slug"] == c.slug)
        assert entry["alt_fr"] == c.alt_fr
        assert entry["usage_slot"] == c.usage_slot
        assert entry["photo_id"] == c.photo_id


def test_licence_document_lists_every_image(images):
    doc = (Path(settings.BASE_DIR) / "docs" / "IMAGE_LICENSES.md").read_text(encoding="utf-8")
    for entry in images:
        assert entry["slug"] in doc, entry["slug"]
        assert entry["photo_id"] in doc, entry["photo_id"]
    assert "DESIGN_SYSTEM.md" in doc
    assert "hotlink" in doc.lower()


# ------------------------------------------------------------------------------------------
# Seed
# ------------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_seed_creates_assets_and_copies_files(media_root, images):
    summary = seeds_media.seed()
    assert f"{len(images)} image(s)" in summary
    assert f"{len(images)} created" in summary
    assert MediaAsset.objects.count() == len(images)
    for entry in images:
        asset = MediaAsset.objects.get(source_url=entry["source_url"])
        assert asset.license == MediaLicense.UNSPLASH
        assert asset.stereotype_checked is True
        assert asset.alt_fr == entry["alt_fr"]
        assert asset.title == entry["title_fr"]
        assert asset.author == entry["author"]
        assert asset.downloaded_on.isoformat() == entry["downloaded_on"]
        assert asset.alt_it == asset.alt_en == asset.alt_ar == "", "translator fields stay blank"
        assert asset.file.name.startswith(seeds_media.STORAGE_PREFIX + "/")
        assert asset.file.name.endswith(".webp")
        assert default_storage.exists(asset.file.name)
        assert asset.width and asset.height and asset.width <= 1440
        assert (media_root / asset.file.name).stat().st_size <= MAX_BYTES


@pytest.mark.django_db
def test_seed_is_idempotent(media_root, images):
    first = seeds_media.seed()
    assert f"{len(images)} file(s) copied" in first
    before = {a.pk: (a.file.name, a.updated_at) for a in MediaAsset.objects.all()}
    second = seeds_media.seed()
    assert MediaAsset.objects.count() == len(images), "second run must not duplicate rows"
    assert "0 created" in second and "0 file(s) copied" in second and f"{len(images)} unchanged" in second
    after = {a.pk: (a.file.name, a.updated_at) for a in MediaAsset.objects.all()}
    assert before == after
    stored = [p for p in (media_root / seeds_media.STORAGE_PREFIX).iterdir() if p.is_file()]
    assert len(stored) == len(images), "no duplicate copies (e.g. name_abc123.webp)"


@pytest.mark.django_db
def test_seed_never_overwrites_editorial_fields(media_root, images):
    seeds_media.seed()
    asset = MediaAsset.objects.get(source_url=images[0]["source_url"])
    asset.alt_fr = "Texte alternatif révisé par la rédaction"
    asset.alt_it = "Testo alternativo tradotto"
    asset.title = "Titre révisé"
    asset.save()
    seeds_media.seed()
    asset.refresh_from_db()
    assert asset.alt_fr == "Texte alternatif révisé par la rédaction"
    assert asset.alt_it == "Testo alternativo tradotto"
    assert asset.title == "Titre révisé"


@pytest.mark.django_db
def test_seed_resyncs_provenance_facts(media_root, images):
    seeds_media.seed()
    asset = MediaAsset.objects.get(source_url=images[0]["source_url"])
    asset.stereotype_checked = False
    asset.license = MediaLicense.OTHER
    asset.save()
    summary = seeds_media.seed()
    assert "1 updated" in summary
    asset.refresh_from_db()
    assert asset.stereotype_checked is True
    assert asset.license == MediaLicense.UNSPLASH


@pytest.mark.django_db
def test_seed_registered_in_seed_all(media_root, images, capsys):
    call_command("seed_all", only="cms.media")
    out = capsys.readouterr().out
    assert "seed cms.media: media library" in out
    assert MediaAsset.objects.count() == len(images)


def test_seed_without_manifest_is_harmless(tmp_path):
    assert seeds_media.load_manifest(tmp_path / "missing.json") == []


def test_seed_rejects_manifest_with_forbidden_words(tmp_path):
    bad = {
        "images": [
            {
                "photo_id": "x",
                "slug": "porta-ingresso",
                "usage_slot": "hero",
                "title_fr": "t",
                "alt_fr": "a",
                "author": "a",
                "source_url": "https://unsplash.com/photos/x",
                "license": "Unsplash License",
                "downloaded_on": "2026-09-17",
                "width": 1,
                "height": 1,
                "files": {"webp": {}, "jpg": "x.jpg"},
                "forbidden_subject_check": True,
            }
        ]
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(seeds_media.MediaSeedError):
        seeds_media.load_manifest(path)
    bad["images"][0]["slug"] = "ok"
    bad["images"][0]["forbidden_subject_check"] = False
    path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(seeds_media.MediaSeedError):
        seeds_media.load_manifest(path)
