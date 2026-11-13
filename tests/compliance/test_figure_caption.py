"""
A photograph on this site is an archive plate, never an illustration.

Art direction A §6.2: a ``<figure>`` without a ``<figcaption>`` is a defect, and the caption must
carry four fields — place, date, one factual sentence, a credit. That rule is what makes anonymous
stock photography structurally impossible rather than merely discouraged, and the Design Council
found exactly the failure it prevents: six interchangeable frames serving fifty-two pages, none
captioned, none credited, five aspect ratios centre-cropping the same 3:2 library at random.

The rule is enforced where a Photo is BUILT (``pages.services.photo_from_asset`` and
``ecosystem.services.photo_for``), not in each of the eleven templates that render one — a rule
repeated eleven times is a rule that will be forgotten on the twelfth.

V5.12 (DECISIONS §6, W2-C): the art-directed Pexels frames of the slot registry (pages.imagery) are not archive plates
and never pretend to be: each is credited in its figcaption (author / licence) and names no place, date or event; its
provenance, licence and one-context rule are held by tests/compliance/test_imagery_v512.py.

V5.24 §2 (2 Nov 2026; FINAL_DELIVERY_V2.md §3.2 D6; the strict rule V5.20): the stock frames render NO caption any
more — the Pexels License requires no attribution and the owner wants no stock label on the product; the author stays
in PROVENANCE.json. The count «a figure per figcaption» therefore becomes two invariants, the first unchanged, the
second new: every curated plate (`figure.figura`) ships with its caption, and no stock frame (`figure[data-slot]`)
carries one. ``is_publishable`` is untouched (the credit stays recorded; the byline is drawn only when the licence
demands it — ``MediaAsset.attribution_required``).

v524-px-improve (the reviewer's m1, QA.md §9; V5.20 — a stronger invariant): the first rule is held on EVERY figure that
is not a stock frame, the exact complement of the second, so that the two together cover every figure as the old
count did — a figure with neither marker is a defect, not a gap between the rules.
"""

from __future__ import annotations

import datetime as dt
import re

import pytest
from django.urls import reverse
from django.utils import translation

from cms.models import MediaAsset

pytestmark = pytest.mark.django_db

#: Public routes that carry, or used to carry, a photograph.
PHOTO_PAGES = (
    "pages:home",
    "pages:project",
    "pages:agami",
    "pages:network",
    "pages:contact",
    "ecosystem:companies",
    "forum:index",
)


def rendered(client, name: str, lang: str = "fr") -> str:
    with translation.override(lang):
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == 200, (name, response.status_code)
    return response.content.decode()


@pytest.mark.parametrize("name", PHOTO_PAGES)
def test_a_plate_is_captioned_and_a_stock_frame_is_not(client, seeded, name: str) -> None:
    html = rendered(client, name)
    for attrs, body in re.findall(r"<figure\b([^>]*)>(.*?)</figure>", html, flags=re.S):
        if "data-slot=" not in attrs:
            assert "<figcaption" in body, (name, "a curated plate ships with its caption")
        if "data-slot=" in attrs:
            assert "<figcaption" not in body and "Pexels" not in body, (name, "a stock frame carries no credit")


def test_a_curated_asset_s_byline_follows_its_licence() -> None:
    """V5.24 §2: the byline renders only when the licence demands it; the credit stays recorded whatever the licence."""
    from cms.models import MediaLicense

    plate = {"title": "t", "alt_fr": "a", "caption_fr": "Une phrase.", "credit": "Archive", "caption_place": "Rovigo"}
    day = dt.date(2026, 10, 2)
    free = (MediaLicense.PEXELS, MediaLicense.UNSPLASH, MediaLicense.CC0, MediaLicense.CLIENT, MediaLicense.ORIGINAL)
    for licence in free:
        asset = MediaAsset(**plate, caption_date=day, license=licence)
        assert asset.is_publishable is True and asset.attribution_required is False, licence
    assert MediaAsset(**plate, caption_date=day, license=MediaLicense.CC_BY).attribution_required is True
    other = MediaAsset(**plate, caption_date=day, license=MediaLicense.OTHER)
    assert other.attribution_required is False
    other.license_notes = "attribution=required; see the licence text"
    assert other.attribution_required is True


def test_an_asset_without_its_caption_apparatus_is_not_publishable() -> None:
    asset = MediaAsset(title="t", alt_fr="a")
    assert asset.is_publishable is False
    asset.caption_fr = "Une phrase de fait."
    assert asset.is_publishable is False, "a caption alone is not the apparatus"
    asset.credit = "Photographe"
    asset.caption_place = "Rovigo"
    assert asset.is_publishable is False, "a plate carries its date"
    asset.caption_date = dt.date(2026, 10, 2)
    assert asset.is_publishable is True


def test_a_decorative_asset_is_exempt() -> None:
    """A decorative image carries no meaning to caption, and says so to assistive technology too."""
    asset = MediaAsset(title="t", alt_fr="", is_decorative=True)
    assert asset.is_publishable is True


def test_the_inherited_library_renders_nowhere_until_it_is_curated(seeded) -> None:
    """
    Stated as a test so the day someone curates the library, this turns red and asks to be updated.

    None of the seeded assets fills the apparatus: they are the frames the Design Council rejected.
    """
    assets = list(MediaAsset.objects.all())
    assert assets, "the media seed produced nothing"
    publishable = [a for a in assets if a.is_publishable and not a.is_decorative]
    assert publishable == [], (
        "an inherited asset became publishable: if it was curated, add its caption to the seed and "
        "update this test; if it was not, its apparatus is incomplete and it must not ship"
    )


def test_photo_from_asset_refuses_an_uncaptioned_asset(seeded) -> None:
    from pages.services import photo_from_asset

    asset = MediaAsset.objects.exclude(is_decorative=True).first()
    assert asset is not None
    assert photo_from_asset(asset) is None


def test_photo_from_asset_carries_the_apparatus_when_it_exists(seeded) -> None:
    from pages.services import photo_from_asset

    asset = MediaAsset.objects.exclude(is_decorative=True).first()
    asset.caption_place = "Rovigo"
    asset.caption_date = dt.date(2026, 10, 2)
    asset.caption_fr = "Séance de travail du Forum Vénétie–Maroc."
    asset.credit = "AGAMI"
    asset.save()

    photo = photo_from_asset(asset)
    assert photo is not None
    assert photo.place == "Rovigo"
    assert photo.date == dt.date(2026, 10, 2)
    assert photo.caption.startswith("Séance")
    assert photo.credit == "AGAMI"
