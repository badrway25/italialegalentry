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
"""

from __future__ import annotations

import datetime as dt

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
def test_no_figure_ships_without_its_caption(client, seeded, name: str) -> None:
    html = rendered(client, name)
    figures = html.count("<figure")
    captions = html.count("<figcaption")
    assert figures == captions, f"{name}: {figures} <figure> for {captions} <figcaption>"


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
