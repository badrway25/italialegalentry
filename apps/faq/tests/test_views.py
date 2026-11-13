"""Integration + compliance tests — public FAQ page (gate G3, search, JSON-LD, translations, RTL, sitemap)."""

import json
import re

import pytest
from bs4 import BeautifulSoup
from django.conf import settings

from cms.forbidden import scan
from cms.models import PublicationStatus, TranslationStatus
from faq import registry
from faq.models import FAQCategory, FAQItem, FAQItemTranslation
from faq.seeds import seed_locked_faq_items
from glossary.seeds import seed_locked_terms
from glossary.services import invalidate_link_map
from tests.conftest import whatsapp_link_set_aside

pytestmark = pytest.mark.django_db

LANGS = [code for code, _ in settings.LANGUAGES]


@pytest.fixture
def faq_seeded(db):
    seed_locked_faq_items()
    # Contextual links from a FAQ answer to a glossary term are rendered only for terms that are
    # actually live (faq.services._glossary_term_is_live), exactly as after `manage.py seed_all`.
    seed_locked_terms()
    invalidate_link_map()


def _jsonld_blocks(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    return [json.loads(tag.string) for tag in soup.find_all("script", type="application/ld+json")]


# --------------------------------------------------------------------------------------------
# Gate G3
# --------------------------------------------------------------------------------------------
def test_faq_is_404_by_default(client, faq_seeded):
    assert client.get("/fr/faq/").status_code == 404


def test_faq_is_404_before_phase3_even_with_flag(client, faq_seeded, before_phase3):
    assert client.get("/fr/faq/").status_code == 404


def test_faq_is_200_when_phase3_open(client, faq_seeded, phase3_open):
    response = client.get("/fr/faq/")
    assert response.status_code == 200
    html = response.content.decode()
    for entry in registry.items():
        assert entry["question"] in html
        assert entry["answer"] in html
        assert f'id="{entry["key"]}"' in html
    assert "application/ld+json" in html


def test_staff_preview_while_gate_closed_is_noindex(client, faq_seeded, staff_user):
    client.force_login(staff_user)
    response = client.get("/fr/faq/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="robots" content="noindex' in html
    assert "Aperçu réservé au personnel" in html


def test_public_route_is_registered_as_gated():
    from core.public_routes import gated_routes

    routes = {(r.app, r.path): r.requires_gate for r in gated_routes()}
    assert routes[("faq", "faq/")] == "phase3_public"


# --------------------------------------------------------------------------------------------
# Structure & accessibility
# --------------------------------------------------------------------------------------------
def test_page_structure_landmarks_headings_and_anchors(client, faq_seeded, phase3_open):
    soup = BeautifulSoup(client.get("/fr/faq/").content, "html.parser")
    assert len(soup.find_all("h1")) == 1
    assert soup.find("main", id="main-content") is not None
    assert soup.find("nav", attrs={"aria-label": "Fil d’Ariane"}) is not None
    form = soup.find("form", attrs={"role": "search"})
    assert form is not None and form["method"].lower() == "get"
    assert soup.find("label", attrs={"for": "faq-q"}) is not None
    # FINAL MICRO-PASS §6 B1 (V5.20 strict rule; this decision replaces V5.22's explorer, L «l'indice»): the questions
    # are ONE list — the system's disclosures in one section, in the register's order, every answer in the page; each
    # row's id its question's key (the permalinks) and its own permalink link, its question an h3 in its summary, its
    # date; no explorer, no index of links, no panel is left — and the themes are aria-pressed buttons in one named
    # group, «Toutes» first and pressed, their counts the register's nine
    section = soup.find("section", id="questions")
    assert section is not None and section.get("aria-labelledby") == "faq-domande-title"
    rows = section.select(".accordion.faq-lista > details.accordion__item.faq-item")
    assert [row["id"] for row in rows] == [e["key"] for e in registry.items()]
    for row in rows:
        assert row.select_one(":scope > summary > h3.faq-item__question") is not None and row.find("time") is not None
        assert row.select_one(f'a.faq-item__permalink[href="/fr/faq/#{row["id"]}"]') is not None
    assert "2026-09-14" in str(rows[0])
    assert not soup.select(".faq-esploratore, .indice, .indice__voce, .indice__pannello, .faq-item__glifo")
    group = section.select_one('.faq-temi[role="group"]')
    pills = group.select('button.faq-tema[type="button"][aria-pressed]')
    assert len(pills) == 4
    assert pills[0]["aria-pressed"] == "true" and all(p["aria-pressed"] == "false" for p in pills[1:])
    assert sum(int(p.select_one(".faq-tema__n").get_text()) for p in pills[1:]) == int(
        pills[0].select_one(".faq-tema__n").get_text()
    ) == 9


def test_related_links_to_glossary_and_contextual_links(client, faq_seeded, phase3_open):
    html = client.get("/fr/faq/").content.decode()
    assert 'href="/fr/glossaire/"' in html
    assert 'href="/fr/glossaire/decreto_flussi/"' in html
    assert 'href="/fr/privacy-policy/"' in html


def test_draft_and_archived_items_are_not_rendered(client, faq_seeded, phase3_open):
    category = FAQCategory.objects.get(slug="general")
    FAQItem.objects.create(key="draft_item", category=category, question_fr="Brouillon ?", answer_fr="non publié")
    FAQItem.objects.create(
        key="old_item",
        category=category,
        question_fr="Archivée ?",
        answer_fr="archivée",
        status=PublicationStatus.ARCHIVED,
    )
    html = client.get("/fr/faq/").content.decode()
    assert "Brouillon ?" not in html and "Archivée ?" not in html


# --------------------------------------------------------------------------------------------
# Search
# --------------------------------------------------------------------------------------------
def test_search_lists_only_matching_items_and_no_jsonld(client, faq_seeded, phase3_open):
    response = client.get("/fr/faq/", {"q": "visa"})
    assert response.status_code == 200
    html = response.content.decode()
    assert registry.item("faq_visas")["question"] in html
    assert registry.item("faq_guaranteed_visa_offer")["question"] in html
    assert registry.item("faq_who")["question"] not in html
    assert "application/ld+json" not in html
    assert "<mark" not in html  # highlighting-free result list
    soup = BeautifulSoup(html, "html.parser")
    assert all(d.has_attr("open") for d in soup.find_all("details", class_="faq-item"))
    assert soup.find("input", id="faq-q")["value"] == "visa"


def test_search_without_result_shows_empty_state(client, faq_seeded, phase3_open):
    html = client.get("/fr/faq/", {"q": "xyzzy-nothing"}).content.decode()
    # the empty state in its glyph tile since V5.15 W3 round 1 (DECISIONS §15 lane B; v515-b 9211d5fc,
    # templates/components/empty_state.html): the class pair is the component's own
    assert '<div class="empty-state empty-state--tile" role="status">' in html
    assert "0 résultat" in html


def test_search_query_is_escaped_and_truncated(client, faq_seeded, phase3_open):
    html = client.get("/fr/faq/", {"q": "<script>alert(1)</script>" + "a" * 300}).content.decode()
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


# --------------------------------------------------------------------------------------------
# JSON-LD
# --------------------------------------------------------------------------------------------
def test_jsonld_faqpage_lists_the_nine_published_items_only(client, faq_seeded, phase3_open):
    category = FAQCategory.objects.get(slug="general")
    FAQItem.objects.create(key="draft_item", category=category, question_fr="Brouillon ?", answer_fr="non publié")
    blocks = _jsonld_blocks(client.get("/fr/faq/").content.decode())
    assert len(blocks) == 1
    data = blocks[0]
    assert data["@type"] == "FAQPage"
    names = [q["name"] for q in data["mainEntity"]]
    assert names == [e["question"] for e in registry.items()]
    assert "Brouillon ?" not in names
    assert data["mainEntity"][0]["acceptedAnswer"]["text"] == registry.item("faq_visas")["answer"]


# --------------------------------------------------------------------------------------------
# Languages (G10) and RTL
# --------------------------------------------------------------------------------------------
def test_other_languages_fall_back_to_french_with_lang_attr(client, faq_seeded, phase3_open):
    # V5.22 (SECTION_SYSTEM_V2 §3.13 Q1; strict rule V5.20): the questions are the explorer's panels' headings —
    # FINAL MICRO-PASS §6 B1 (V5.20): the list's rows' headings, the same invariants on the one list
    for lang in ("it", "en"):
        soup = BeautifulSoup(client.get(f"/{lang}/faq/").content, "html.parser")
        questions = soup.select(".faq-lista h3.faq-item__question")
        assert len(questions) == 9
        assert all(q.get("lang") == "fr" for q in questions), lang
        answers = soup.select(".faq-lista p.faq-risposta")
        assert len(answers) == 9 and all(a.get("lang") == "fr" for a in answers), lang
    # V5.27 / FINAL_DELIVERY_V2 R7′ (V5.20, the steward's amendment at the v524-pub2 merge): on /ar/ the question is
    # compositional (C-UI) — the provisional Arabic, no lang of its own —, the answer substantive (C-SUBST-FR) on its
    # own page — French, lang="fr", and preceded by its identification caption (stronger than the lang alone it held)
    soup = BeautifulSoup(client.get("/ar/faq/").content, "html.parser")
    questions = soup.select(".faq-lista h3.faq-item__question")
    assert len(questions) == 9
    assert all(q.get("lang") is None and re.search(r"[\u0600-\u06ff]", q.get_text()) for q in questions)
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211: «the Arabic FAQ must
    # not normally show French answers»): each answer takes the form its class gives it — an informational answer (C-UI)
    # its provisional Arabic, no lang, no caption; a substantive one (C-SUBST-FR) the French source, lang="fr",
    # preceded by its own identification caption — and no French answer stands without that treatment (unintended
    # French = 0)
    from cms import locked_renderings

    answers = soup.select(".faq-lista p.faq-risposta")
    assert len(answers) == 9
    keys = registry.keys()
    for answer in answers:
        index = keys.index(answer.find_parent("details")["id"])
        subkey = f"p3.faq.items[{index}].answer"
        caption = answer.find_previous_sibling("p", class_="locked-caption")
        if locked_renderings.treatment(subkey) == "C-UI":
            assert answer.get("lang") is None and caption is None, subkey
            assert answer.get_text().strip() == locked_renderings.rendering(subkey), subkey
        else:
            assert answer.get("lang") == "fr", subkey
            assert answer.get_text().strip() == registry.items()[index]["answer"], subkey
            assert caption is not None and caption.get("data-locked-caption") == subkey, caption
    assert sum(1 for answer in answers if answer.get("lang") == "fr") == 4
    soup_fr = BeautifulSoup(client.get("/fr/faq/").content, "html.parser")
    assert len(soup_fr.select(".faq-lista h3.faq-item__question")) == 9
    assert all(q.get("lang") is None for q in soup_fr.select(".faq-lista h3.faq-item__question"))


def test_published_translation_is_rendered_but_draft_is_not(client, faq_seeded, phase3_open):
    item = FAQItem.objects.get(key="faq_visas")
    row = FAQItemTranslation.objects.create(
        master=item,
        language="it",
        question="Domanda ufficiale IT",
        answer="Risposta ufficiale IT",
        status=TranslationStatus.DRAFT,
        source="ufficiale",
    )
    html = client.get("/it/faq/").content.decode()
    assert "Domanda ufficiale IT" not in html
    row.status = TranslationStatus.PUBLISHED
    row.save()
    soup = BeautifulSoup(client.get("/it/faq/").content, "html.parser")
    # V5.20 citing V5.29 §10–§13 / FINAL_DELIVERY_V2 §3.6 (lane PUB2): the heading now draws its question's glyph tile
    # (aria-hidden) before its words, so its text is read whole — the same invariant: the published Italian is the
    # heading's words, with no lang of its own
    heading = next((h for h in soup.find_all("h3") if h.get_text(strip=True) == "Domanda ufficiale IT"), None)
    assert heading is not None and heading.get("lang") is None
    assert "Risposta ufficiale IT" in str(soup)


def test_arabic_is_rtl_and_renders(client_ar, faq_seeded, phase3_open):
    response = client_ar.get("/ar/faq/")
    assert response.status_code == 200
    html = response.content.decode()
    assert '<html lang="ar" dir="rtl"' in html
    # V5.27 / FINAL_DELIVERY_V2 R7′ (V5.20, the steward's amendment at the v524-pub2 merge): the question renders in its
    # provisional Arabic (C-UI), never its French; the prescribed answer renders whole in French on its own page
    from cms import locked_renderings

    assert locked_renderings.rendering("p3.faq.items[0].question") in html
    assert registry.item("faq_visas")["question"] not in html
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211): the first answer is
    # informational — its provisional Arabic renders, its French does not; a substantive answer still renders whole in
    # French on its own page
    assert locked_renderings.rendering("p3.faq.items[0].answer") in html
    assert registry.item("faq_visas")["answer"] not in html
    assert registry.item("faq_data_protection")["answer"] in html


# --------------------------------------------------------------------------------------------
# Compliance scan (forbidden formulations, trademark, e-mail, external resources)
# --------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_rendered_pages_pass_compliance_scan(client, faq_seeded, phase3_open):
    from glossary.seeds import seed_locked_terms

    seed_locked_terms()  # cross links to the glossary must resolve to live pages
    for lang in LANGS:
        for params in ({}, {"q": "visa"}):
            response = client.get(f"/{lang}/faq/", params)
            assert response.status_code == 200, (lang, params)
            html = response.content.decode()
            assert not scan(html), (lang, params, scan(html))
            assert "®" not in html
            assert "Italy Legal Entry™" in html
            emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
            assert emails <= {"contact@agamieuromed.org"}, emails
            checked = whatsapp_link_set_aside(html)  # V5.19 §7: the owner's WhatsApp link only, as a link
            externals = [s for s in re.findall(r'(?:src|href)="(https?://[^"]+)"', checked) if "testserver" not in s]
            assert not externals, externals
            assert "CONTENT_PENDING_LEGAL_REVIEW" not in html


# --------------------------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------------------------
def test_sitemap_lists_faq_only_when_gate_open(client, faq_seeded):
    from core.sitemaps import SITEMAPS

    assert "faq" in SITEMAPS
    assert SITEMAPS["faq"]().items() == []
    assert "/fr/faq/" not in client.get("/sitemap.xml").content.decode()


def test_sitemap_contains_faq_when_gate_open(client, faq_seeded, phase3_open):
    from core.sitemaps import SITEMAPS

    assert SITEMAPS["faq"]().items() == ["faq:index"]
    xml = client.get("/sitemap.xml").content.decode()
    assert "/fr/faq/" in xml and "/ar/faq/" in xml
