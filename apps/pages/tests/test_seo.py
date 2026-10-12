"""SEO: JSON-LD (never a public-authority claim), meta tags, sitemap gating, route registration."""

from __future__ import annotations

import json
import re

import pytest

from core.public_routes import all_routes
from pages.tests.conftest import LANGS

pytestmark = pytest.mark.django_db

GOVERNMENT_MARKERS = (
    "GovernmentOrganization",
    "GovernmentOffice",
    "GovernmentService",
    "GovernmentBuilding",
    "GovernmentPermit",
    "Embassy",
    "ministry",
    "ministère",
    "ministero",
    "gouvernement",
    "governo",
    "government",
    "consulat",
    "autorité",
)


def _jsonld(html: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return [json.loads(block) for block in blocks]


@pytest.mark.parametrize("state", ["closed", "open"])
def test_home_jsonld_parses_and_makes_no_governmental_claim(request, page, seeded, state):
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    blocks = _jsonld(html)
    assert len(blocks) == 1
    data = blocks[0]
    assert data["@context"] == "https://schema.org"
    graph = {node["@type"]: node for node in data["@graph"]}
    assert set(graph) == {"Organization", "WebSite"}

    organization = graph["Organization"]
    assert organization["name"] == "AGAMI — Dialogo Giuridico Interculturale APS"
    assert organization["email"] == "contact@agamieuromed.org"
    assert organization["url"] == "http://testserver/fr/"
    for absent in ("sameAs", "logo", "parentOrganization", "memberOf", "address", "telephone", "taxID", "vatID"):
        assert absent not in organization, absent

    website = graph["WebSite"]
    assert website["name"] == "Italy Legal Entry™"
    assert website["inLanguage"] == "fr"
    assert website["publisher"] == {"@id": organization["@id"]}

    dump = json.dumps(data, ensure_ascii=False).lower()
    for marker in GOVERNMENT_MARKERS:
        assert marker.lower() not in dump, marker
    assert "®" not in dump


@pytest.mark.parametrize("lang", LANGS)
def test_home_jsonld_language_and_url_follow_the_page(page, seeded, lang):
    _response, html = page(f"/{lang}/")
    graph = {node["@type"]: node for node in _jsonld(html)[0]["@graph"]}
    assert graph["WebSite"]["inLanguage"] == lang
    assert graph["WebSite"]["url"] == f"http://testserver/{lang}/"


def test_jsonld_is_escaped_against_script_breakout():
    from pages.services import render_jsonld

    rendered = render_jsonld({"name": "</script><script>alert(1)</script> & co"})
    assert "<" not in rendered and ">" not in rendered and "&" not in rendered
    assert json.loads(rendered)["name"] == "</script><script>alert(1)</script> & co"


def test_institutional_pages_carry_no_structured_data(page, seeded):
    for path in ("le-projet/", "agami/", "reseau/", "contact/"):
        _response, html = page(f"/fr/{path}")
        assert _jsonld(html) == [], path


def test_home_meta_title_description_and_social_image(page, seeded):
    _response, html = page("/fr/")
    assert "<title>Italy Legal Entry™ · Parcours réguliers vers l’Italie</title>" in html
    assert re.search(r'<meta name="description" content="[^"]{30,}">', html)
    assert '<link rel="canonical" href="http://testserver/fr/">' in html
    assert '<meta property="og:image" content="http://testserver/static/img/og-default.png">' in html
    assert '<meta property="og:title" content="Italy Legal Entry™">' in html
    for lang in LANGS:
        assert f'hreflang="{lang}"' in html


def test_institutional_page_shares_its_own_self_hosted_photo(page, seeded, curated_photo):
    _response, html = page("/fr/le-projet/")
    assert (
        '<meta property="og:image" content="http://testserver/static/img/photos/atelier-de-travail-1440.jpg">' in html
    )


def test_phase3_meta_description_is_the_prescribed_subtitle(page, seeded, phase3_open):
    from pages.tests.conftest import escaped, text_of

    _response, html = page("/fr/")
    assert f'<meta name="description" content="{escaped(text_of("p3.hero.subtitle"))}">' in html


def _sitemap_locations(client) -> list[str]:
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    return re.findall(r"<loc>([^<]+)</loc>", response.content.decode())


def test_sitemap_lists_institutional_pages_but_not_the_gated_one(client, seeded):
    locations = _sitemap_locations(client)
    for lang in LANGS:
        for path in ("", "le-projet/", "agami/", "reseau/", "contact/"):
            assert any(loc.endswith(f"/{lang}/{path}") for loc in locations), (lang, path)
    assert not any("attention-aux-fraudes" in loc for loc in locations)


def test_sitemap_lists_antifraud_once_phase3_is_open(client, seeded, phase3_open):
    locations = _sitemap_locations(client)
    for lang in LANGS:
        assert any(loc.endswith(f"/{lang}/attention-aux-fraudes/") for loc in locations), lang


def test_public_routes_are_registered_for_the_compliance_crawl():
    routes = {(r.path, r.requires_gate) for r in all_routes() if r.app == "pages"}
    assert routes == {
        ("", ""),
        ("le-projet/", ""),
        ("agami/", ""),
        ("reseau/", ""),
        ("contact/", ""),
        ("attention-aux-fraudes/", "phase3_public"),
    }


def test_url_name_contract():
    from django.urls import reverse
    from django.utils import translation

    with translation.override("fr"):
        assert reverse("pages:home") == "/fr/"
        assert reverse("pages:project") == "/fr/le-projet/"
        assert reverse("pages:agami") == "/fr/agami/"
        assert reverse("pages:network") == "/fr/reseau/"
        assert reverse("pages:contact") == "/fr/contact/"
        assert reverse("pages:antifraud") == "/fr/attention-aux-fraudes/"
