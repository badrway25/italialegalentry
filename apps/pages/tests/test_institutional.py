"""Institutional pages: project, promoter, network, contact and the Phase 3 anti-fraud page."""

from __future__ import annotations

import re

import pytest

from cms import locked_content
from cms.forbidden import scan
from pages.tests.conftest import LANGS, escaped, text_of

pytestmark = pytest.mark.django_db

PAGES = ("le-projet/", "agami/", "reseau/", "contact/")
#: RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
#: Réseau («l'esploratore») and Contact («lo sportello») open with a head of their own in place of the interior's
#: entrance — each page still opens with ONE entrance: page → the class its <header> starts with
ENTRANCES = {"le-projet/": "ingresso", "agami/": "ingresso", "reseau/": "rete-testa", "contact/": "sportello-testa"}


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _faq_who() -> dict:
    return next(item for item in locked_content.get("p3.faq.items", "fr")[0] if item["key"] == "faq_who")


def _locked_texts(html: str, key: str) -> list[str]:
    """V5.22 (SECTION_SYSTEM_V2 §1 rule 6, §2.0 «Data»): a prescribed text recomposed at render — cut into spans on its
    own separators, a few words set in place as emphasis — stands as ONE element carrying its key; that element's text,
    its tags removed, is the registry's text character for character (never retyped, never printed twice)."""
    from bs4 import BeautifulSoup

    return [el.get_text() for el in BeautifulSoup(html, "html.parser").select(f'[data-locked="{key}"]')]


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("path", PAGES)
def test_institutional_pages_render_in_every_language(page, seeded, lang, path):
    response, html = page(f"/{lang}/{path}")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert 'class="breadcrumbs container"' in html
    # design V5.4 (W3-F1): the interior's entrance; no side column — the five pages are the «Projet» door's entries
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane
    # D): the page's entrance (ENTRANCES: the interior's, or Réseau's and Contact's own head), once — and the page's one
    # h1 stands inside it (stronger: the entrance was only required to exist)
    entrance = re.findall(rf'<header class="{ENTRANCES[path]}["\s][^>]*>(.*?)</header>', html, flags=re.S)
    assert len(entrance) == 1 and "<h1" in entrance[0], (path, ENTRANCES[path])
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
    # V5.22 (SECTION_SYSTEM_V2 §3.2 LP-2, strict rule V5.20): «Pourquoi» is a step of the story, its text one <p> cut
    # on its own full stops — the paragraph keeps its French language on the Arabic page, its text the registry's
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): «Pourquoi» is
    # compositional (C-UI) — its provisional Arabic rendering in the page's language, the same one element
    from cms import locked_renderings

    assert re.search(r'<p class="projet__perche" data-locked="p2.forum.why.body">', html)
    assert _locked_texts(html, "p2.forum.why.body") == [locked_renderings.rendering("p2.forum.why.body")]


# ---- /le-projet/ --------------------------------------------------------------------------------
def test_project_page_is_assembled_from_prescribed_texts(page, seeded):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    assert escaped(text_of("p2.forum.why.title")) in main
    # V5.22 (SECTION_SYSTEM_V2 §3.2 LP-2; strict rule V5.20): the text is cut at render into its three sentences — the
    # one element that holds it carries the registry's text, whole, once
    assert _locked_texts(main, "p2.forum.why.body") == [text_of("p2.forum.why.body")]
    # Phase 3 material stays out while the gate is closed.
    assert escaped(text_of("p3.hero.body")) not in main
    assert escaped(_faq_who()["answer"]) not in main
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in main


def test_project_page_adds_phase3_texts_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    assert escaped(text_of("p3.hero.body")) in main
    assert escaped(_faq_who()["answer"]) in main
    assert _locked_texts(main, "p2.forum.why.body") == [text_of("p2.forum.why.body")]  # V5.22 §3.2 LP-2 (above)


def test_project_page_trademark_line(page, seeded):
    _response, fr = page("/fr/le-projet/")
    line = re.search(r"<p class=\"page-trademark\" data-trademark>(.*?)</p>", fr, re.S).group(1)
    assert text_of("p1.trademark.mark") in line
    # I18N-06: the mark is a left-to-right isolate, so in Arabic «™» stays on the right of the name (v518g-p: the
    # line's span had translate="no" alone and painted «™Italy Legal Entry» on /ar/le-projet/)
    assert f'<span translate="no" dir="ltr" lang="en">{text_of("p1.trademark.mark")}</span>' in line
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
def test_agami_page_shows_the_promoters_verified_identification_and_nothing_else(page, seeded, phase3_open):
    """V5.23 — the owner's Q9 decision A (30 October 2026; SECTION_SYSTEM_V2 §11.1, §3.17 AG-3). Until then the page
    published no registry data (they belonged to the unpublished «Mentions légales»): that expectation conflicts with
    the owner's decision and is replaced (strict rule V5.20) by a stronger one — the association's verified public
    identification stands on the page itself, every field the owner gave, each ONCE, from one source
    (pages.identity), and NO other identifier; the page never links the unpublished legal notice."""
    from django.conf import settings

    from pages import identity

    _response, html = page("/fr/agami/")
    main = _main(html)
    assert _locked_texts(main, "p2.forum.who.body") == [text_of("p2.forum.who.body")]  # V5.22 §3.17 AG-1: emphasis only
    assert escaped(_faq_who()["question"]) in main
    assert escaped(_faq_who()["answer"]) in main
    plate = re.search(r'<section class="sez sez--strato agami-targa".*?</section>', main, re.S).group(0)
    words = " ".join(re.sub(r"<[^>]+>", " ", plate).split())
    fields = [
        settings.ILE["PROMOTER"],
        identity.LEGAL_FORM,
        identity.TAX_CODE,
        identity.RUNTS,
        identity.REGISTRATION,
        identity.REGISTERED_OFFICE["street"],
        "36061 Bassano del Grappa (VI)",
        identity.OPERATIONAL_OFFICE["street"],
        "00195 Roma",
        "contact@agamieuromed.org",
        identity.WEBSITE,
    ]
    for field in fields:
        assert field in words, field
    for once in (identity.TAX_CODE, identity.RUNTS, identity.REGISTRATION, identity.REGISTERED_OFFICE["street"]):
        assert main.count(escaped(once)) == 1, once
    assert 'href="mailto:contact@agamieuromed.org"' in plate
    # the website is a fact of the identification, never an outbound link (V5.19 §7: the one outbound link is WhatsApp)
    assert not re.search(r'href="https?://', main)
    # nothing the owner did not give: no trademark filing, no other register's form of a number
    for other in ("019405072", "PR-261439", "Rep. n°", "Codice fiscale"):
        assert other not in main, other
    # V5.14 C/D (lane C's M-2; the steward, the v515-c merge): the unpublished official notices answer 404, so no link
    assert 'href="/fr/note-legali/"' not in main
    assert "Mentions légales" not in main
    assert "CONTENT_PENDING_LEGAL_REVIEW" not in html  # template comments never reach the visitor


def test_agami_page_before_phase3_has_no_faq_text(page, seeded):
    _response, html = page("/fr/agami/")
    assert _locked_texts(html, "p2.forum.who.body") == [text_of("p2.forum.who.body")]  # V5.22 §3.17 AG-1 (above)
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
    for href in ("/fr/parcours/", "/fr/entreprises/recueil-des-besoins/", "/fr/contact/"):
        assert f'href="{href}"' in main
    # V5.12 §8: without an authorised partner, no partners' link and no «partners to come» sentence
    assert 'href="/fr/partenaires/"' not in main and "au fur et à mesure" not in main
    assert 'href="/fr/forum/"' in main and 'href="/fr/agami/"' in main
    assert escaped(text_of("p3.hero.body")) not in main


def test_network_page_links_the_presentation_when_open(page, seeded, phase3_open):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (P2-4 of
    # the integration review; was test_network_page_quotes_the_presentation_when_open): the prescribed presentation is
    # Le projet's «En bref», one click away — once G3 is open the network page links it where it stands whole, and
    # never repeats it (stronger: the text is followed to the page that shows it, whole, once)
    _response, html = page("/fr/reseau/")
    main = _main(html)
    assert escaped(text_of("p3.hero.body")) not in main
    assert main.count('href="/fr/le-projet/#project-presentation"') == 1
    _response, project = page("/fr/le-projet/")
    assert _main(project).count(escaped(text_of("p3.hero.body"))) == 1
    assert 'id="project-presentation"' in _main(project)


def test_network_page_shows_only_authorized_partners(page, seeded, partner_factory):
    partner_factory("Chambre partenaire autorisée")
    partner_factory("Partenaire sans autorisation", authorized=False)
    _response, html = page("/fr/reseau/")
    assert "Chambre partenaire autorisée" in html
    assert "Partenaire sans autorisation" not in html


# ---- /contact/ ----------------------------------------------------------------------------------
def test_contact_page_single_address_and_link_to_the_enquiries_form(page, seeded, whatsapp_channel):
    _response, html = page("/fr/contact/")
    main = _main(html)
    assert 'href="mailto:contact@agamieuromed.org"' in main
    assert "Tous les formulaires du site sont acheminés vers cette adresse." in main
    # The form itself is owned by the enquiries app: nothing is re-implemented here.
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «lo sportello»):
    # the page carries the enquiries app's own form (its ContactForm, posted to enquiries:contact — the view keeps the
    # validation, the consent, the honeypot and the throttle) instead of a link to the form's page; so, while gate G2
    # is closed, the form's own seat holds the G2 notice and no field — the visitor is told in place, never sent to a
    # closed form (stronger than a link beside the notice)
    assert re.search(r'<div class="sportello__modulo" id="formulaire">.*?data-gate="forms-closed"', main, flags=re.S)
    assert 'href="/fr/contact/formulaire/"' not in main
    assert "<form" not in main
    assert "<input" not in main and "<textarea" not in main
    # V5.19: the owner's two telephone channels, and no other number (no invented one, no postal address). V5.20: the
    # WhatsApp number is configured outside the repository — here Ofcom's fictional one (tests/conftest.py).
    assert 'href="tel:800642015"' in main and f'href="{whatsapp_channel.url}"' in main
    numbers = set(re.findall(r"\+?\d[\d .]{8,}\d", re.sub(r"<[^>]+>", " ", main)))
    assert {n.strip() for n in numbers} == {"800 642 015", whatsapp_channel.label}, numbers
    assert set(re.findall(r'href="tel:([^"]*)"', main)) == {"800642015"}
    # Gate G2 is closed (official legal texts missing): the visitor is told before clicking.
    assert 'data-gate="forms-closed"' in main


def test_contact_page_when_forms_are_open(page, seeded, legal_published):
    _response, html = page("/fr/contact/")
    main = _main(html)
    assert 'data-gate="forms-closed"' not in main
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «lo sportello»):
    # the page's one action is the enquiries form's own submit, on this page; the form posts to the enquiries view
    # (/fr/contact/formulaire/), which answers a submission with errors on its own page and a sent one with its «done»
    # (the system's enquiry-form hook on the desk's sheet: the public forms' generic selectors hold it)
    assert re.search(
        r'<form class="form enquiry-form sportello-form" method="post" action="/fr/contact/formulaire/"', main
    )
    assert len(re.findall(r'class="btn btn--primary', main)) == 1
    assert re.search(r'<button type="submit" class="btn btn--primary[^"]*">', main), "the page's one action"


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
    if lang == "ar":
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the title is compositional
        # (C-UI) — its provisional Arabic rendering; the body is substantive (C-SUBST-FR) and this is its page: the
        # French, verbatim, said with lang="fr"
        from cms import locked_renderings

        title = escaped(locked_renderings.rendering("p3.antifraud.title"))
        assert 'lang="fr" data-locked="p3.antifraud.body"' in main
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «l'avvertenza»):
    # the h1 is the page's own head's; the prescribed text stands whole in ONE element carrying its key, cut at render
    # on its own sentences (cms.locked_split «sentence») — its text, tags removed, is the registry's character for
    # character (the rule _locked_texts states for every recomposed prescribed text), never retyped, never twice
    assert re.search(rf'<h1 class="avvertenza-testa__titolo"[^>]*>{re.escape(title)}</h1>', main)
    assert _locked_texts(main, "p3.antifraud.body") == [text_of("p3.antifraud.body")]
    assert re.search(r'<p class="avvertenza__testo"[^>]*data-locked="p3.antifraud.body"><span class="ls ls-1">', main)
    assert body not in main, "cut on its sentences: never also printed whole elsewhere"
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
