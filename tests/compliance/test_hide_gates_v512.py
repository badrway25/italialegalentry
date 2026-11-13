"""
V5.12 §8 / §13 (W1-C): an incomplete public surface is hidden, never shown «in preparation».

The hide gates live where the rest of the publication gates do (``core.gates.news_public`` / ``partners_public``) and
reach every link through the route registry (``core.links.path_is_open``): a menu row typed in the back-office is held to
the same rule as the static menu. The content-driven pages (FAQ, glossary, a living theme) answer 404 while empty.
"""

from __future__ import annotations

import pytest
from django.conf import settings

from cms.models import MenuItem, MenuLocation
from cms.templatetags.cms_nav import build_menu
from core import gates
from core.links import public_url

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

LANGS = [code for code, _ in settings.LANGUAGES]


def _urls(items):
    for item in items:
        yield item.url
        yield from (child.url for child in item.children)


def test_the_two_gates_are_closed_on_an_empty_site(seeded):
    assert gates.news_public() is False
    assert gates.partners_public() is False
    assert public_url("news:index") == "" and public_url("partners:index") == ""


@pytest.mark.parametrize("lang", LANGS)
def test_no_menu_and_no_footer_link_to_a_hidden_page(seeded, phase3_open, lang):
    for location in (MenuLocation.MAIN, MenuLocation.FOOTER_1):
        urls = set(_urls(build_menu(location, lang)))
        assert f"/{lang}/actualites/" not in urls, location
        assert f"/{lang}/partenaires/" not in urls, location


def test_a_back_office_menu_row_to_a_hidden_page_is_left_out(seeded, phase3_open):
    for order, (name, label) in enumerate((("news:index", "Actualités"), ("partners:index", "Partenaires"))):
        MenuItem.objects.create(
            location=MenuLocation.MAIN, order=order, url_name=name, label_it=label, label_fr=label, label_en=label
        )
    MenuItem.objects.create(
        location=MenuLocation.MAIN, order=9, url_name="pages:contact", label_it="C", label_fr="Contact", label_en="C"
    )
    urls = set(_urls(build_menu(MenuLocation.MAIN, "fr")))
    assert urls == {"/fr/contact/"}, urls


@pytest.mark.parametrize("app, path", [("faq", "/fr/faq/"), ("glossary", "/fr/glossaire/")])
def test_an_empty_faq_or_glossary_is_no_page(client, phase3_open, app, path):
    """Without a live entry the index answers 404 — never «en cours de préparation»."""
    response = client.get(path)
    assert response.status_code == 404
    assert "en cours de préparation" not in response.content.decode()


def test_health_has_no_reachable_route(client, seeded, phase3_open):
    for lang in LANGS:
        for slug in ("sante", "service-sanitaire-national"):
            assert client.get(f"/{lang}/vivre-en-italie/{slug}/").status_code == 404, (lang, slug)
        index = client.get(f"/{lang}/vivre-en-italie/").content.decode()
        assert "/vivre-en-italie/sante/" not in index and "/vivre-en-italie/service-sanitaire-national/" not in index
