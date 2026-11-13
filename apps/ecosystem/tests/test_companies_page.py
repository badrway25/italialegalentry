"""
Espace Entreprises — PHASE 1 (Implementation §1.1). The page is online now: it must not depend on
gate G3 (Phase 3) nor on gate G2 (public forms), and it replaces the former recruitment page.
"""

from __future__ import annotations

import re

import pytest

from cms import locked_content
from core import gates

from .conftest import COMPANIES_PATH, LANGS

pytestmark = pytest.mark.django_db

TITLE = locked_content.text("p1.companies.title", "fr")
INTRO = locked_content.text("p1.companies.intro", "fr")
QUOTE = locked_content.text("p1.companies.quote", "fr")
BUTTON = locked_content.text("p1.companies.form.button", "fr")
FAQ_ENTRY = next(e for e in locked_content.get("p3.faq.items", "fr")[0] if e["key"] == "faq_recruitment_agency")


@pytest.mark.parametrize("lang", LANGS)
def test_page_is_online_in_every_language_with_both_gates_closed(get_html, seeded, lang):
    assert gates.phase3_public() is False, "precondition: gate G3 closed"
    assert gates.public_forms_enabled().open is False, "precondition: gate G2 closed"
    html = get_html(lang, COMPANIES_PATH)
    if lang == "ar":
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the title, the intro and
        # the quotation are compositional texts (C-UI) — on /ar/ their provisional Arabic renderings, whole, and never
        # the French; every other language keeps the prescribed French, whole
        from cms import locked_renderings

        for key, prescribed in (
            ("p1.companies.title", TITLE),
            ("p1.companies.intro", INTRO),
            ("p1.companies.quote", QUOTE),
        ):
            assert locked_renderings.treatment(key) == "C-UI", key
            assert locked_renderings.rendering(key) in html, (lang, key)
            assert prescribed not in html, (lang, key)
        return
    for prescribed in (TITLE, INTRO, QUOTE):
        assert prescribed in html, (lang, prescribed[:40])


def test_page_needs_no_database_row(get_html, db):
    """Phase 1 must be online even before any seed ran: prescribed texts come from the registry."""
    from ecosystem.models import EcosystemSpace

    assert not EcosystemSpace.objects.exists()
    html = get_html("fr", COMPANIES_PATH)
    assert TITLE in html and INTRO in html and QUOTE in html
    assert 'class="ingresso__aside figura"' not in html, "no photograph without a curated, captioned asset"
    # V5.12 (DECISIONS §6/§7): the space's art-directed photograph instead (slot «companies.hero», credited), the way
    # in under the lead; a curated, captioned asset of the back office still takes precedence (below)
    assert 'data-slot="companies.hero"' in html and 'class="ingresso__way via"' in html


@pytest.mark.compliance
def test_prescribed_texts_in_their_prescribed_places(get_html, seeded):
    html = get_html("fr", COMPANIES_PATH)
    assert html.count("<h1") == 1
    assert re.search(r'<h1 class="ingresso__title[^"]*"[^>]*>' + re.escape(TITLE) + "</h1>", html)
    assert re.search(r'<p class="ingresso__lead"[^>]*>' + re.escape(INTRO) + "</p>", html)
    # V5.22 (SECTION_SYSTEM_V2 §3.6 EN-1, an approved owner/product decision; V5.20 strict rule): the quotation opens
    # «Trois temps» as the band's statement (its own blockquote, its rule a drawn span) — the same text, whole, in its
    # own paragraph
    quote = re.search(r'<blockquote class="imprese-citazione"[^>]*>.*?<p>(.*?)</p>', html, flags=re.S)
    assert quote and quote.group(1) == QUOTE


def test_fallback_language_is_marked_on_prescribed_texts(get_html, seeded):
    html = get_html("it", COMPANIES_PATH)
    assert re.search(r'<h1 class="ingresso__title[^"]*" lang="fr">' + re.escape(TITLE), html)
    # V5.22 §3.6 EN-1 (strict rule): the quotation's blockquote is the flow's statement; its language still marked
    assert re.search(r'<blockquote class="imprese-citazione" lang="fr">', html)
    french = get_html("fr", COMPANIES_PATH)
    assert re.search(r'<h1 class="ingresso__title[^"]*">', french), "no lang attribute on a page already in French"


@pytest.mark.compliance
@pytest.mark.parametrize("lang", LANGS)
def test_no_recruitment_wording_of_the_former_page(get_html, seeded, lang):
    html = get_html(lang, COMPANIES_PATH)
    lowered = html.lower()
    assert not re.search(r"\bmatching\b", html, flags=re.I)
    for forbidden in ("Recruit in Morocco", "Find Qualified Profiles", "profils à recruter", "Submit a Recruitment"):
        assert forbidden.lower() not in lowered, (lang, forbidden)
    # No selection / ranking / candidate vocabulary in the UI wording of the page body.
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0].lower()
    for token in ("candidat", "classement", "ranking", "shortlist"):
        assert token not in main, (lang, token)


def test_three_neutral_moments_are_an_ordered_list(get_html, seeded):
    html = get_html("fr", COMPANIES_PATH)
    # FINAL MICRO-PASS §6 B3 (V5.20; was «in the démarche's band, under its quotation»): the démarche opens on the
    # quotation beside the territory's photograph (its band, on stone) and the three moments follow in their own band,
    # on paper (the one the panorama held) — the same ordered list, one heading each, in their order
    assert html.index('id="demarche"') < html.index('id="trois-temps"')
    section = html.split('id="trois-temps"', 1)[1].split("</section>", 1)[0]
    # V5.22 (SECTION_SYSTEM_V2 §3.6 EN-1; strict rule): the three moments are «il flusso»'s stations — an ordered list,
    # one heading each, in their order
    assert re.search(r'<ol class="flusso__tappe" role="list"[^>]*data-steps="3"', section)
    assert section.count('<li class="flusso__tappa">') == 3
    labels = re.findall(r'<h3 class="flusso__titolo">(.*?)</h3>', section)
    assert labels == [
        "Recueil des besoins",
        "Construction des parcours avec les acteurs compétents",
        "Formation et mobilité régulière",
    ]


def test_form_closed_renders_the_unavailable_component_once(get_html, seeded):
    html = get_html("fr", COMPANIES_PATH)
    assert html.count('data-gate="forms-closed"') == 1
    assert "<form" not in html.split('id="formulaire"', 1)[1].split("</section>", 1)[0]
    assert 'id="formulaire-recueil-des-besoins"' not in html


def test_form_open_is_the_single_canonical_enquiries_form(get_html, seeded, legal_published):
    html = get_html("fr", COMPANIES_PATH)
    assert html.count('id="formulaire-recueil-des-besoins"') == 1, "the company form must appear exactly once"
    assert html.count("enquiry-form--company-needs") == 1
    assert 'data-gate="forms-closed"' not in html
    form = html.split('id="formulaire-recueil-des-besoins"', 1)[0].rsplit("<form", 1)[1]
    assert 'action="/fr/entreprises/recueil-des-besoins/"' in form, "the form posts to the canonical enquiries view"
    assert "csrfmiddlewaretoken" in html
    # Prescribed labels, order and button come from the enquiries implementation, untouched.
    labels = locked_content.get("p1.companies.form.fields", "fr")[0]
    positions = [html.index(label) for label in labels]
    assert positions == sorted(positions)
    assert BUTTON in html


def test_ecosystem_app_does_not_reimplement_the_form():
    """One canonical implementation: no form class, no POST handling, no <form> in this app."""
    from pathlib import Path

    from django.conf import settings

    app_dir = Path(settings.BASE_DIR) / "apps" / "ecosystem"
    assert not (app_dir / "forms.py").exists()
    templates = Path(settings.BASE_DIR) / "templates" / "ecosystem"
    for path in templates.rglob("*.html"):
        assert "<form" not in path.read_text(encoding="utf-8"), path
    views = (app_dir / "views.py").read_text(encoding="utf-8")
    assert "request.POST" not in views and "require_safe" in views
    assert views.count("@require_safe") == 4, "every view of the app is read-only (GET and HEAD)"


@pytest.mark.security
@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_unsafe_methods_are_not_accepted_by_the_page(client, seeded, method):
    response = getattr(client, method)("/fr/entreprises/", {"company_name": "x"})
    assert response.status_code == 405
    assert sorted(m.strip() for m in response["Allow"].split(",")) == ["GET", "HEAD"]


def test_head_requests_are_answered(client, seeded):
    """Link checkers, uptime monitors and some crawlers probe public pages with HEAD."""
    response = client.head("/fr/entreprises/")
    assert response.status_code == 200
    assert response.content == b""


def test_single_destination_note_uses_the_public_address(get_html, seeded):
    html = get_html("fr", COMPANIES_PATH)
    note = html.split("ecosystem-form__destination", 1)[1].split("</p>", 1)[0]
    assert 'href="mailto:contact@agamieuromed.org"' in note
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
    assert emails == {"contact@agamieuromed.org"}


def test_secondary_links_before_phase3(get_html, seeded):
    html = get_html("fr", COMPANIES_PATH)
    assert 'href="/fr/forum/"' in html
    assert "Le Forum Vénétie–Maroc" in html
    assert "/fr/projet-pilote/" not in html, "the pilot page is Phase 3: never linked while gate G3 is closed"
    assert "/fr/institutions/" not in html and "/fr/universites-et-formation/" not in html


def test_phase3_content_is_absent_before_the_gate(get_html, seeded, before_phase3):
    html = get_html("fr", COMPANIES_PATH)
    assert FAQ_ENTRY["answer"] not in html, "p3.faq.items is Phase 3 content"
    assert 'data-block="recruitment-guarantee"' not in html
    assert locked_content.text("p3.pilot.title", "fr") not in html


def test_phase3_adds_the_transparency_block_and_the_pilot_link(get_html, seeded, phase3_open):
    html = get_html("fr", COMPANIES_PATH)
    block = html.split('data-block="recruitment-guarantee"', 1)[1].split("</section>", 1)[0]
    assert FAQ_ENTRY["question"] in block
    # V5.22 (SECTION_SYSTEM_V2 §3.6 EN-4; strict rule): the answer is cut at its own «Non.» and colon into the split's
    # spans — read in its one paragraph's text, it is the prescribed answer, character for character
    from bs4 import BeautifulSoup

    answer = BeautifulSoup(block, "html.parser").select_one("p[data-faq]")
    assert answer.get_text("") == FAQ_ENTRY["answer"]
    assert 'href="/fr/faq/#faq_recruitment_agency"' in block
    assert 'href="/fr/projet-pilote/"' in html
    assert locked_content.text("p3.pilot.title", "fr") in html
    # Still exactly one h1 and the Phase 1 texts unchanged.
    assert html.count("<h1") == 1 and TITLE in html and INTRO in html and QUOTE in html


def test_sections_keep_their_anchors_and_no_gated_space_is_linked(get_html, seeded):
    """Design V5.4 (W3-F1): no side column — the sibling spaces are the navigation's doors; the anchors stay."""
    html = get_html("fr", COMPANIES_PATH)
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert '<nav class="local-nav"' not in main
    assert 'id="demarche"' in main and 'id="formulaire"' in main
    assert "/fr/institutions/" not in main and "/fr/projet-pilote/" not in main


def test_after_phase3_the_transparency_anchor_and_the_pilot_link(get_html, seeded, phase3_open):
    html = get_html("fr", COMPANIES_PATH)
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert 'id="transparence"' in main
    # V5.22 (SECTION_SYSTEM_V2 §3.6 EN-5; strict rule): «Pour aller plus loin» is «l'approdo», the same destinations
    related = main.split('class="sez sez--approdo ecosistema-approdo"', 1)[1].split("</section>", 1)[0]
    assert 'href="/fr/projet-pilote/"' in related and 'href="/fr/forum/"' in related


def test_photograph_is_self_hosted_and_described(get_html, seeded, curated_photo):
    html = get_html("fr", COMPANIES_PATH)
    figure = html.split('<figure class="ingresso__aside figura">', 1)[1].split("</figure>", 1)[0]
    assert 'type="image/webp"' in figure and "/static/img/photos/equipe-entreprise-960.webp 960w" in figure
    assert 'src="/static/img/photos/equipe-entreprise-1440.jpg"' in figure
    alt = re.search(r'alt="([^"]+)"', figure)
    assert alt and len(alt.group(1)) > 20
    assert "http" not in figure
    assert "<figcaption>" in figure, "a caption and a credit under every photograph (D26)"
    assert 'fetchpriority="high"' in figure and 'loading="lazy"' not in figure, "the entrance's photograph is the LCP"
    italian = get_html("it", COMPANIES_PATH).split('<figure class="ingresso__aside figura">', 1)[1]
    italian = italian.split("</figure>", 1)[0]
    assert 'lang="fr"' in italian, "French alternative text is tagged while no Italian one exists"


def test_seo_head(get_html, seeded, curated_photo):
    html = get_html("fr", COMPANIES_PATH)
    assert "<title>Espace Entreprises · Italy Legal Entry™</title>" in html
    description = re.search(r'<meta name="description" content="([^"]*)">', html).group(1)
    assert description == INTRO
    assert '<link rel="canonical" href="http://testserver/fr/entreprises/">' in html
    for lang in LANGS:
        assert f'hreflang="{lang}" href="http://testserver/{lang}/entreprises/"' in html
    assert 'property="og:image" content="http://testserver/static/img/photos/equipe-entreprise-1440.jpg"' in html
    assert 'name="robots" content="noindex' not in html
    assert '<script type="application/ld+json">' in html and '"@type":"BreadcrumbList"' in html
    assert "GovernmentOrganization" not in html


def test_arabic_page_is_rtl(get_html, seeded):
    from cms import locked_renderings

    html = get_html("ar", COMPANIES_PATH)
    assert '<html lang="ar" dir="rtl"' in html
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the title is a compositional
    # text (C-UI) — its provisional Arabic rendering in the page's language, no French run
    title = locked_renderings.rendering("p1.companies.title")
    assert re.search(r'<h1 class="ingresso__title[^"]*">' + re.escape(title) + "</h1>", html)
    assert not re.search(r'<h1 class="ingresso__title[^"]*" lang="fr">', html)
    assert html.count("<h1") == 1
