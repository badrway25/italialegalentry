"""Institutional pages: project, promoter, network, contact and the Phase 3 anti-fraud page."""

from __future__ import annotations

import re

import pytest

from cms import locked_content
from cms.forbidden import scan
from pages.tests.conftest import LANGS, escaped, text_of

pytestmark = pytest.mark.django_db

PAGES = ("le-projet/", "agami/", "reseau/", "contact/")


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _faq_who() -> dict:
    return next(item for item in locked_content.get("p3.faq.items", "fr")[0] if item["key"] == "faq_who")


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("path", PAGES)
def test_institutional_pages_render_in_every_language(page, seeded, lang, path):
    response, html = page(f"/{lang}/{path}")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert 'class="breadcrumbs container"' in html
    # design V5.4 (W3-F1): the interior's entrance; no side column — the five pages are the «Projet» door's entries
    assert '<header class="ingresso"' in html
    assert 'class="local-nav"' not in html
    assert re.search(r'<meta name="description" content="[^"]{20,}">', html)
    assert scan(html) == []
    assert "®" not in html
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
    assert emails <= {"contact@agamieuromed.org"}
    assert not re.search(r"<[a-z][^>]*\sstyle=", html)


@pytest.mark.parametrize("path", PAGES)
def test_institutional_pages_render_with_phase3_open(page, seeded, phase3_open, path):
    response, html = page(f"/fr/{path}")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert scan(html) == []
    assert 'href="/fr/attention-aux-fraudes/"' in html  # the footer's link, once public


def test_promoter_page_links_its_siblings_and_hides_the_gated_entry(page, seeded):
    """Design V5.4 (W3-F1): no side column; «Pour aller plus loin» links the project's pages that are public."""
    _response, html = page("/fr/agami/")
    main = _main(html)
    assert '<nav class="local-nav"' not in main
    for href in ("/fr/le-projet/", "/fr/reseau/"):
        assert f'href="{href}"' in main
    assert "attention-aux-fraudes" not in main


def test_arabic_institutional_page_is_rtl(page, seeded):
    _response, html = page("/ar/le-projet/")
    assert '<html lang="ar" dir="rtl"' in html
    assert 'data-locked="p2.forum.why.body"' in html
    assert re.search(r'<p class="page-section__text chapter__prose" lang="fr" data-locked="p2.forum.why.body">', html)


# ---- /le-projet/ --------------------------------------------------------------------------------
def test_project_page_is_assembled_from_prescribed_texts(page, seeded):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    assert escaped(text_of("p2.forum.why.title")) in main
    assert escaped(text_of("p2.forum.why.body")) in main
    # Phase 3 material stays out while the gate is closed.
    assert escaped(text_of("p3.hero.body")) not in main
    assert escaped(_faq_who()["answer"]) not in main
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in main


def test_project_page_adds_phase3_texts_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    assert escaped(text_of("p3.hero.body")) in main
    assert escaped(_faq_who()["answer"]) in main
    assert escaped(text_of("p2.forum.why.body")) in main


def test_project_page_trademark_line(page, seeded):
    _response, fr = page("/fr/le-projet/")
    line = re.search(r"<p class=\"page-trademark\" data-trademark>(.*?)</p>", fr, re.S).group(1)
    assert text_of("p1.trademark.mark") in line
    assert text_of("p1.trademark.words_fr") in line
    _response, it = page("/it/le-projet/")
    line_it = re.search(r"<p class=\"page-trademark\" data-trademark>(.*?)</p>", it, re.S).group(1)
    assert text_of("p1.trademark.words_it") in line_it
    assert "registrato" not in it.lower()
    _response, en = page("/en/le-projet/")
    line_en = re.search(r"<p class=\"page-trademark\" data-trademark>(.*?)</p>", en, re.S).group(1)
    assert '<span lang="fr">marque déposée</span>' in line_en
    for html in (fr, it, en):
        assert "®" not in html and "registered trademark" not in html.lower()


# ---- /agami/ ------------------------------------------------------------------------------------
def test_agami_page_uses_prescribed_texts_and_publishes_no_registry_data(page, seeded, phase3_open):
    _response, html = page("/fr/agami/")
    main = _main(html)
    assert escaped(text_of("p2.forum.who.body")) in main
    assert escaped(_faq_who()["question"]) in main
    assert escaped(_faq_who()["answer"]) in main
    # CONTENT_PENDING_LEGAL_REVIEW — identification data belong to the official Mentions légales.
    for forbidden_data in ("RUNTS", "149809", "91036640240", "Bassano", "Codice fiscale", "Code fiscal"):
        assert forbidden_data not in html, forbidden_data
    assert 'href="/fr/note-legali/"' in main
    assert "CONTENT_PENDING_LEGAL_REVIEW" not in html  # template comments never reach the visitor


def test_agami_page_before_phase3_has_no_faq_text(page, seeded):
    _response, html = page("/fr/agami/")
    assert escaped(text_of("p2.forum.who.body")) in html
    assert escaped(_faq_who()["answer"]) not in html


# ---- /reseau/ -----------------------------------------------------------------------------------
def test_network_page_lists_the_five_actors_and_links_the_spaces(page, seeded):
    _response, html = page("/fr/reseau/")
    main = _main(html)
    assert re.findall(r'data-actor="([a-z]+)"', main) == [
        "persons",
        "companies",
        "institutions",
        "universities",
        "professionals",
    ]
    for href in ("/fr/parcours/", "/fr/entreprises/recueil-des-besoins/", "/fr/partenaires/", "/fr/contact/"):
        assert f'href="{href}"' in main
    assert escaped(text_of("p3.hero.body")) not in main


def test_network_page_quotes_the_presentation_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/reseau/")
    assert escaped(text_of("p3.hero.body")) in _main(html)


def test_network_page_shows_only_authorized_partners(page, seeded, partner_factory):
    partner_factory("Chambre partenaire autorisée")
    partner_factory("Partenaire sans autorisation", authorized=False)
    _response, html = page("/fr/reseau/")
    assert "Chambre partenaire autorisée" in html
    assert "Partenaire sans autorisation" not in html


# ---- /contact/ ----------------------------------------------------------------------------------
def test_contact_page_single_address_and_link_to_the_enquiries_form(page, seeded):
    _response, html = page("/fr/contact/")
    main = _main(html)
    assert 'href="mailto:contact@agamieuromed.org"' in main
    assert 'href="/fr/contact/formulaire/"' in main
    assert "Tous les formulaires du site sont acheminés vers cette adresse." in main
    # The form itself is owned by the enquiries app: nothing is re-implemented here.
    assert "<form" not in main
    assert "<input" not in main and "<textarea" not in main
    # No invented phone number or postal address.
    assert "tel:" not in main
    assert not re.search(r"\+?\d[\d .]{8,}\d", re.sub(r"<[^>]+>", " ", main))
    # Gate G2 is closed (official legal texts missing): the visitor is told before clicking.
    assert 'data-gate="forms-closed"' in main


def test_contact_page_when_forms_are_open(page, seeded, legal_published):
    _response, html = page("/fr/contact/")
    main = _main(html)
    assert 'data-gate="forms-closed"' not in main
    assert re.search(r'class="btn btn--primary[^"]*" href="/fr/contact/formulaire/"', main), "the page's one action"


# ---- /attention-aux-fraudes/ --------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_antifraud_is_404_while_gate_closed(page, seeded, lang):
    response, html = page(f"/{lang}/attention-aux-fraudes/")
    assert response.status_code == 404
    assert escaped(text_of("p3.antifraud.body")) not in html


def test_antifraud_is_404_before_the_date_even_with_flag(page, seeded, before_phase3):
    response, _html = page("/fr/attention-aux-fraudes/")
    assert response.status_code == 404


@pytest.mark.parametrize("lang", LANGS)
def test_antifraud_is_200_with_exact_locked_text_when_open(page, seeded, phase3_open, lang):
    response, html = page(f"/{lang}/attention-aux-fraudes/")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    main = _main(html)
    title, body = escaped(text_of("p3.antifraud.title")), escaped(text_of("p3.antifraud.body"))
    assert re.search(rf'<h1 class="ingresso__title[^"]*"[^>]*>{re.escape(title)}</h1>', main)
    assert re.search(
        rf'<p class="antifraud-panel__body"[^>]*data-locked="p3.antifraud.body">{re.escape(body)}</p>', main
    )
    assert "#icon-shield" in main
    assert scan(html) == []
    assert 'name="robots"' not in html


def test_antifraud_links_and_report_line(page, seeded, phase3_open):
    _response, html = page("/fr/attention-aux-fraudes/")
    main = _main(html)
    assert 'href="/fr/faq/#faq_guaranteed_visa_offer"' in main
    # The link is labelled with the prescribed question (registry), never with a paraphrase of it.
    question = next(i for i in locked_content.get("p3.faq.items", "fr")[0] if i["key"] == "faq_guaranteed_visa_offer")
    assert escaped(question["question"]) in main
    assert "que faire face" not in main
    assert 'href="/fr/parcours/"' in main
    assert 'href="/fr/glossaire/"' in main
    assert 'href="mailto:contact@agamieuromed.org"' in main
    # No external authority link is authorised yet.
    hrefs = re.findall(r'href="([^"]+)"', main)
    assert all(h.startswith(("/", "mailto:contact@agamieuromed.org", "#")) for h in hrefs), hrefs


def test_antifraud_faq_anchor_exists_on_the_faq_page(page, seeded, phase3_open):
    _response, html = page("/fr/faq/")
    assert 'id="faq_guaranteed_visa_offer"' in html


def test_antifraud_staff_preview_is_noindex(client, seeded, staff_user, person_user):
    assert client.get("/fr/attention-aux-fraudes/?preview=1").status_code == 404  # anonymous visitor
    client.force_login(person_user)
    assert client.get("/fr/attention-aux-fraudes/?preview=1").status_code == 404
    client.force_login(staff_user)
    assert client.get("/fr/attention-aux-fraudes/").status_code == 404
    response = client.get("/fr/attention-aux-fraudes/?preview=1")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="robots" content="noindex' in html
    assert escaped(text_of("p3.antifraud.body")) in html


def test_pages_only_accept_safe_methods(client, seeded):
    assert client.post("/fr/").status_code == 405
    assert client.post("/fr/contact/").status_code == 405
    assert client.head("/fr/").status_code == 200
