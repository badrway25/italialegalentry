"""Integration + compliance tests — glossary index/permalinks (gate G3, A–Z, search, JSON-LD, i18n, RTL, sitemap)."""

import json
import re

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse

from cms.forbidden import scan
from cms.models import PublicationStatus, TranslationStatus
from glossary import registry
from glossary.models import Term, TermTranslation
from glossary.seeds import seed_locked_terms

pytestmark = pytest.mark.django_db

LANGS = [code for code, _ in settings.LANGUAGES]


@pytest.fixture
def glossary_seeded(db):
    seed_locked_terms()


def _jsonld_blocks(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    return [json.loads(tag.string) for tag in soup.find_all("script", type="application/ld+json")]


# --------------------------------------------------------------------------------------------
# Gate G3
# --------------------------------------------------------------------------------------------
def test_index_and_permalink_are_404_by_default(client, glossary_seeded):
    assert client.get("/fr/glossaire/").status_code == 404
    assert client.get("/fr/glossaire/codice_fiscale/").status_code == 404


def test_404_before_phase3_even_with_flag(client, glossary_seeded, before_phase3):
    assert client.get("/fr/glossaire/").status_code == 404
    assert client.get("/fr/glossaire/codice_fiscale/").status_code == 404


def test_index_200_when_phase3_open_with_all_terms(client, glossary_seeded, phase3_open):
    response = client.get("/fr/glossaire/")
    assert response.status_code == 200
    html = response.content.decode()
    for entry in registry.terms():
        assert entry["term"] in html
        assert entry["definition"] in html
        assert f'id="{entry["key"]}"' in html
        assert f'href="/fr/glossaire/{entry["key"]}/"' in html


def test_staff_preview_while_gate_closed_is_noindex(client, glossary_seeded, staff_user):
    client.force_login(staff_user)
    response = client.get("/fr/glossaire/codice_fiscale/")
    assert response.status_code == 200
    assert 'name="robots" content="noindex' in response.content.decode()


def test_public_routes_are_registered_as_gated():
    from core.public_routes import gated_routes

    routes = {(r.app, r.path): r.requires_gate for r in gated_routes()}
    assert routes[("glossary", "glossaire/")] == "phase3_public"
    assert routes[("glossary", "glossaire/codice_fiscale/")] == "phase3_public"


# --------------------------------------------------------------------------------------------
# Index structure: A–Z with only letters that have terms, search form, landmarks
# --------------------------------------------------------------------------------------------
def test_alphabetical_index_lists_only_letters_with_terms(client, glossary_seeded, phase3_open):
    soup = BeautifulSoup(client.get("/fr/glossaire/").content, "html.parser")
    nav = soup.find("nav", class_="az-index")
    letters = [a.get_text(strip=True) for a in nav.find_all("a")]
    assert letters == ["C", "D", "L", "N", "P", "Q", "R", "V"]
    for letter in letters:
        assert soup.find("section", id=f"lettre-{letter}") is not None
    assert len(soup.find_all("h1")) == 1
    assert soup.find("form", attrs={"role": "search"})["method"].lower() == "get"
    assert soup.find("label", attrs={"for": "glossary-q"}) is not None
    dts = soup.select("dl.glossary__list dt")
    assert len(dts) == 10 and all(dt.get("lang") == "it" for dt in dts)
    assert 'href="/fr/faq/"' in str(soup)


def test_terms_are_sorted_alphabetically_inside_letters(client, glossary_seeded, phase3_open):
    soup = BeautifulSoup(client.get("/fr/glossaire/").content, "html.parser")
    section = soup.find("section", id="lettre-C")
    assert [dt.get_text(strip=True) for dt in section.find_all("dt")] == ["Carta blu UE", "Codice fiscale"]


# --------------------------------------------------------------------------------------------
# Permalinks
# --------------------------------------------------------------------------------------------
def test_permalink_is_stable_and_shows_definition_related_and_metadata(client, glossary_seeded, phase3_open):
    assert reverse("glossary:term", kwargs={"slug": "visto_ingresso"}) == "/fr/glossaire/visto_ingresso/"
    response = client.get("/fr/glossaire/visto_ingresso/")
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    h1 = soup.find("h1")
    assert h1.get_text(strip=True) == "Visto d’ingresso" and h1.get("lang") == "it"
    assert registry.term("visto_ingresso")["definition"] in str(soup)
    related = [a["href"] for a in soup.select(".glossary-term__related-list a")]
    assert "/fr/glossaire/permesso_di_soggiorno/" in related
    assert "/fr/glossaire/nulla_osta/" in related
    assert "14.09.2026" in str(soup)  # last reviewed
    assert "Document d’implémentation" in str(soup)  # source
    crumbs = soup.find("nav", attrs={"aria-label": "Fil d’Ariane"})
    assert 'href="/fr/glossaire/"' in str(crumbs)


def test_unknown_or_unpublished_permalink_is_404(client, glossary_seeded, phase3_open):
    assert client.get("/fr/glossaire/does-not-exist/").status_code == 404
    Term.objects.filter(key="codice_fiscale").update(status=PublicationStatus.DRAFT)
    assert client.get("/fr/glossaire/codice_fiscale/").status_code == 404
    assert "Codice fiscale" not in client.get("/fr/glossaire/").content.decode()


def test_related_list_hides_unpublished_terms(client, glossary_seeded, phase3_open):
    Term.objects.filter(key="nulla_osta").update(status=PublicationStatus.DRAFT)
    html = client.get("/fr/glossaire/visto_ingresso/").content.decode()
    assert "/fr/glossaire/nulla_osta/" not in html
    assert "/fr/glossaire/permesso_di_soggiorno/" in html


# --------------------------------------------------------------------------------------------
# Search
# --------------------------------------------------------------------------------------------
def test_search_lists_only_matching_terms_and_no_jsonld(client, glossary_seeded, phase3_open):
    response = client.get("/fr/glossaire/", {"q": "questura"})
    assert response.status_code == 200
    html = response.content.decode()
    assert "Questura / Prefettura" in html
    assert "Permesso di soggiorno" in html  # definition mentions the Questura
    assert "Codice fiscale" not in html.split("Pour aller plus loin")[0]
    assert "application/ld+json" not in html
    assert "<mark" not in html


def test_search_without_result_shows_empty_state(client, glossary_seeded, phase3_open):
    html = client.get("/fr/glossaire/", {"q": "xyzzy-nothing"}).content.decode()
    assert 'class="empty-state"' in html
    assert "0 terme" in html


# --------------------------------------------------------------------------------------------
# JSON-LD
# --------------------------------------------------------------------------------------------
def test_jsonld_defined_term_set_on_index_and_defined_term_on_permalink(client, glossary_seeded, phase3_open):
    Term.objects.create(key="draft", term="Zeta", definition_fr="z")
    blocks = _jsonld_blocks(client.get("/fr/glossaire/").content.decode())
    assert len(blocks) == 1 and blocks[0]["@type"] == "DefinedTermSet"
    names = [t["name"] for t in blocks[0]["hasDefinedTerm"]]
    assert len(names) == 10 and "Zeta" not in names
    blocks = _jsonld_blocks(client.get("/fr/glossaire/codice_fiscale/").content.decode())
    assert len(blocks) == 1
    assert blocks[0]["@type"] == "DefinedTerm"
    assert blocks[0]["name"] == "Codice fiscale"
    assert blocks[0]["url"] == "http://testserver/fr/glossaire/codice_fiscale/"


# --------------------------------------------------------------------------------------------
# Languages (G10) and RTL
# --------------------------------------------------------------------------------------------
def test_other_languages_fall_back_to_french_with_lang_attr(client, glossary_seeded, phase3_open):
    for lang in ("it", "en", "ar"):
        soup = BeautifulSoup(client.get(f"/{lang}/glossaire/").content, "html.parser")
        dds = soup.select("dl.glossary__list dd")
        assert len(dds) == 10 and all(dd.get("lang") == "fr" for dd in dds), lang
        detail = BeautifulSoup(client.get(f"/{lang}/glossaire/codice_fiscale/").content, "html.parser")
        assert detail.find("p", class_="glossary-term__definition").get("lang") == "fr"
    soup_fr = BeautifulSoup(client.get("/fr/glossaire/").content, "html.parser")
    assert all(dd.get("lang") is None for dd in soup_fr.select("dl.glossary__list dd"))


def test_published_translation_is_rendered_but_draft_is_not(client, glossary_seeded, phase3_open):
    term = Term.objects.get(key="codice_fiscale")
    row = TermTranslation.objects.create(
        master=term,
        language="en",
        definition="Official EN definition.",
        status=TranslationStatus.DRAFT,
        source="official",
    )
    assert "Official EN definition." not in client.get("/en/glossaire/codice_fiscale/").content.decode()
    row.status = TranslationStatus.PUBLISHED
    row.save()
    soup = BeautifulSoup(client.get("/en/glossaire/codice_fiscale/").content, "html.parser")
    definition = soup.find("p", class_="glossary-term__definition")
    assert definition.get_text(strip=True) == "Official EN definition." and definition.get("lang") is None
    assert soup.find("h1").get("lang") == "it"


def test_arabic_is_rtl_and_renders(client_ar, glossary_seeded, phase3_open):
    for path in ("/ar/glossaire/", "/ar/glossaire/nulla_osta/"):
        response = client_ar.get(path)
        assert response.status_code == 200
        assert '<html lang="ar" dir="rtl"' in response.content.decode()


# --------------------------------------------------------------------------------------------
# Compliance scan
# --------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_rendered_pages_pass_compliance_scan(client, glossary_seeded, phase3_open):
    paths = ["glossaire/", "glossaire/?q=visto"] + [f"glossaire/{key}/" for key in registry.keys()]
    for lang in LANGS:
        for path in paths:
            response = client.get(f"/{lang}/{path}")
            assert response.status_code == 200, (lang, path)
            html = response.content.decode()
            assert not scan(html), (lang, path, scan(html))
            assert "®" not in html
            assert "Italy Legal Entry™" in html
            emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
            assert emails <= {"contact@agamieuromed.org"}, emails
            externals = [s for s in re.findall(r'(?:src|href)="(https?://[^"]+)"', html) if "testserver" not in s]
            assert not externals, externals
            assert "CONTENT_PENDING_LEGAL_REVIEW" not in html


# --------------------------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------------------------
def test_sitemap_empty_when_gate_closed(client, glossary_seeded):
    from core.sitemaps import SITEMAPS

    assert "glossary" in SITEMAPS
    assert SITEMAPS["glossary"]().items() == []
    assert "/fr/glossaire/" not in client.get("/sitemap.xml").content.decode()


def test_sitemap_lists_index_and_live_terms_when_gate_open(client, glossary_seeded, phase3_open):
    from core.sitemaps import SITEMAPS

    Term.objects.filter(key="codice_fiscale").update(status=PublicationStatus.DRAFT)
    items = SITEMAPS["glossary"]().items()
    assert len(items) == 1 + 9
    xml = client.get("/sitemap.xml").content.decode()
    assert "/fr/glossaire/" in xml and "/ar/glossaire/nulla_osta/" in xml
    assert "/fr/glossaire/codice_fiscale/" not in xml
