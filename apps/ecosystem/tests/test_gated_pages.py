"""
Institutions, Universités et Formation, Projet Pilote — PHASE 3 (Implementation §3.4–§3.6).
404 while gate G3 is closed; with the gate open they print their prescribed texts verbatim.
"""

from __future__ import annotations

import re

import pytest

from cms import locked_content

from .conftest import GATED_PATHS, LANGS

pytestmark = pytest.mark.django_db

SEQUENCE = [
    "BESOINS DES ENTREPRISES",
    "PROFILS ET COMPÉTENCES",
    "FORMATION DANS LE PAYS D’ORIGINE",
    "PRÉPARATION AVANT LE DÉPART",
    "PROCÉDURES RÉGULIÈRES",
    "ENTRÉE EN ITALIE",
    "ACCOMPAGNEMENT",
    "SUIVI",
]
NOTICE_SENTENCE = "Cette présentation ne signifie pas qu’un canal d’entrée soit déjà autorisé ou opérationnel."


def _t(key: str) -> str:
    return locked_content.text(key, "fr")


# ---------------------------------------------------------------------------------------------
# Gate G3
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_gated_pages_404_by_default(client, seeded, lang, path):
    assert client.get(f"/{lang}/{path}").status_code == 404


@pytest.mark.compliance
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_gated_pages_404_when_flag_is_on_but_date_not_reached(client, seeded, before_phase3, path):
    assert client.get(f"/fr/{path}").status_code == 404


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_gated_pages_200_once_phase3_is_public(get_html, seeded, phase3_open, lang, path):
    html = get_html(lang, path)
    assert html.count("<h1") == 1
    assert f'<html lang="{lang}"' in html
    assert 'name="robots" content="noindex' not in html


@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_404_page_does_not_leak_prescribed_phase3_text(client, seeded, path):
    html = client.get(f"/fr/{path}").content.decode("utf-8")
    for key in ("p3.institutions.intro", "p3.universities.intro", "p3.pilot.body"):
        assert _t(key) not in html


# ---------------------------------------------------------------------------------------------
# Staff preview
# ---------------------------------------------------------------------------------------------
@pytest.mark.security
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_preview_is_for_back_office_users_only(client, seeded, person_user, staff_user, path):
    assert client.get(f"/fr/{path}?preview=1").status_code == 404
    client.force_login(person_user)
    assert client.get(f"/fr/{path}?preview=1").status_code == 404
    client.force_login(staff_user)
    assert client.get(f"/fr/{path}").status_code == 404, "preview must be asked for explicitly"
    response = client.get(f"/fr/{path}?preview=1")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert 'name="robots" content="noindex, nofollow"' in html
    assert 'data-preview="phase3"' in html


@pytest.mark.security
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_preview_is_never_cacheable_and_head_follows_the_gate(client, seeded, staff_user, path):
    assert client.head(f"/fr/{path}").status_code == 404, "HEAD must not reveal more than GET"
    client.force_login(staff_user)
    response = client.get(f"/fr/{path}?preview=1")
    assert response.status_code == 200
    cache_control = response["Cache-Control"]
    for directive in ("no-store", "private", "no-cache"):
        assert directive in cache_control, (path, cache_control)


def test_public_pages_do_not_carry_the_preview_cache_headers(client, seeded, phase3_open):
    response = client.get("/fr/projet-pilote/")
    assert response.status_code == 200
    assert "no-store" not in response.get("Cache-Control", "")


def test_preview_keeps_links_inside_the_preview(client, seeded, staff_user, curated_photo):
    client.force_login(staff_user)
    html = client.get("/fr/institutions/?preview=1").content.decode("utf-8")
    assert 'href="/fr/projet-pilote/?preview=1"' in html
    assert 'class="ingresso__aside figura"' in html, "the scheduled editorial row is visible in a preview"


# ---------------------------------------------------------------------------------------------
# Espace Institutions
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_institutions_prescribed_texts_and_button(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["institutions"])
    assert re.search(r'<p class="ingresso__lead">' + re.escape(_t("p3.institutions.intro")) + "</p>", html)
    # V5.22 (SECTION_SYSTEM_V2 §3.7 IN-1; strict rule): the sentence stands whole in «l'emiciclo», its items spans —
    # its element's text is the prescribed sentence, verbatim
    from bs4 import BeautifulSoup

    sentence = BeautifulSoup(html, "html.parser").select_one("#destinataires p.emiciclo__frase")
    assert sentence.get_text("") == _t("p3.institutions.recipients"), "the recipients sentence is printed verbatim"
    # the page's own primary is read in its content: the chrome's phone sheet carries a primary of its own earlier in
    # the document (W2-C2's «Découvrir le questionnaire d'orientation», `nav-sheet__primary`)
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    button = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', main, flags=re.S)
    assert button, "prescribed CTA missing"
    assert button.group(1) == "/fr/collaboration/institutions/"
    assert button.group(2).strip() == _t("p3.institutions.button")


def test_institutions_recipients_are_the_prescribed_sentence_as_written(get_html, seeded, phase3_open):
    """
    Design V5.4 (W3-F1's review m4): the sentence is the chapter's visible body, as written — its fragments, cut into
    rows with their mixed initials («Régions» · «organismes publics» · «Chambres de Commerce» …), read as a list with
    typos; a register is kept for real lists. No hidden copy, no presentational list beside it.
    """
    from bs4 import BeautifulSoup

    html = get_html("fr", GATED_PATHS["institutions"])
    block = html.split('data-block="recipients"', 1)[1].split("</section>", 1)[0]
    # V5.22 (SECTION_SYSTEM_V2 §3.7 IN-1 «l'emiciclo», §0.1 «words under the seats would print the locked sentence
    # twice»; strict rule): the outline keeps a team heading, hidden (the visible duplicate «Destinataires» is gone);
    # the sentence is the section's one visible text, whole, once — its items spans that light their seats; the seats
    # are glyphs only (aria-hidden, no word): no copy, no presentational list of the words beside it
    soup = BeautifulSoup(block, "html.parser")
    heading = soup.select_one("h2#destinataires-title")
    assert "visually-hidden" in heading["class"] and heading.get_text(strip=True) == "Destinataires"
    sentences = soup.select("p.emiciclo__frase")
    assert len(sentences) == 1 and sentences[0].get_text("") == _t("p3.institutions.recipients")
    assert block.count(_t("p3.institutions.recipients")[:20]) <= 1
    seats = soup.select("ol.emiciclo__seggi[aria-hidden='true'] > li")
    assert len(seats) == 6 and not "".join(s.get_text(strip=True) for s in seats), "the seats carry no word"
    assert "ecosystem-enum" not in block


def test_institutions_secondary_links(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["institutions"])
    # V5.22 (SECTION_SYSTEM_V2 §3.7 IN-2; strict rule): «Pour aller plus loin» is «l'approdo», the same destinations
    related = html.split('class="sez sez--approdo ecosistema-approdo"', 1)[1].split("</section>", 1)[0]
    for href in ("/fr/forum/", "/fr/projet-pilote/"):
        assert f'href="{href}"' in related
    # V5.12 §8: no link to the partners' page while no partner is authorised in writing (it answers 404)
    assert 'href="/fr/partenaires/"' not in html


def test_institutions_fallback_language_marked(get_html, seeded, phase3_open):
    html = get_html("en", GATED_PATHS["institutions"])
    assert '<p class="ingresso__lead"><span lang="fr">' + _t("p3.institutions.intro") + "</span></p>" in html
    # V5.22 (SECTION_SYSTEM_V2 §3.7 IN-1; strict rule): the sentence's element in «l'emiciclo» says it is French
    from bs4 import BeautifulSoup

    sentence = BeautifulSoup(html, "html.parser").select_one("#destinataires p.emiciclo__frase")
    assert sentence["lang"] == "fr" and sentence.get_text("") == _t("p3.institutions.recipients")


# ---------------------------------------------------------------------------------------------
# Espace Universités et Formation
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_universities_prescribed_texts_and_button(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["universities"])
    assert re.search(r'<p class="ingresso__lead">' + re.escape(_t("p3.universities.intro")) + "</p>", html)
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]  # the page's own primary (as above)
    button = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', main, flags=re.S)
    assert button and button.group(1) == "/fr/collaboration/universites-formation/"
    assert button.group(2).strip() == _t("p3.universities.button")


def test_universities_sentence_is_said_once(get_html, seeded, phase3_open):
    """
    Design V5.4 (W3-F1; RH-5 «one thing once»): the prescribed sentence is the page's lead, whole; the presentational
    breakdown of its words into «Acteurs» and «Domaines» — the same words a second time, a screen below — left the page.
    """
    html = get_html("fr", GATED_PATHS["universities"])
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert main.count(_t("p3.universities.intro")) == 1
    assert 'data-block="universities-enumeration"' not in main and "ecosystem-enum" not in main


def test_universities_links_to_training_and_pathways(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["universities"])
    # V5.22 (SECTION_SYSTEM_V2 §3.8 U1 «la filiera»; strict rule): the route's stations lead to Formation's two times
    # and the pathway sheets; its foot to the pathways' index — the same onward ways, and more
    related = html.split('<section id="filiere"', 1)[1].split("</section>", 1)[0]
    assert 'href="/fr/formation/#avant-le-depart"' in related and 'href="/fr/formation/#apres-l-arrivee"' in related
    assert 'href="/fr/parcours/"' in related
    assert 'href="/fr/parcours/study_and_training_in_italy/"' in related


# ---------------------------------------------------------------------------------------------
# Projet Pilote
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_pilot_title_and_body(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    assert re.search(r'<h1 class="ingresso__title[^"]*">' + re.escape(_t("p3.pilot.title")) + "</h1>", html)
    assert re.search(r'<p class="ingresso__lead">' + re.escape(_t("p3.pilot.body")) + "</p>", html)


@pytest.mark.compliance
def test_pilot_sequence_has_the_eight_prescribed_steps_in_order(get_html, seeded, phase3_open):
    assert locked_content.get("p3.pilot.sequence", "fr")[0] == SEQUENCE
    html = get_html("fr", GATED_PATHS["pilot"])
    diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    assert re.search(r"<ol class=\"linea[^\"]*\"[^>]* aria-label=", diagram), "ordered-list semantics"
    # V5.22 (SECTION_SYSTEM_V2 §3.3 PP-1 «la linea V2»; strict rule): a capitals label carries its tracking class and
    # its ink verb — the words, the order and the count are the same
    labels = re.findall(r'<p class="linea__label[^"]*"[^>]*>(.*?)</p>', diagram)
    assert labels == SEQUENCE
    assert 'data-steps="8"' in html
    assert "linea__text" not in diagram, "each step is a short prescribed label only"


def test_pilot_notice_follows_the_diagram_immediately(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    after_diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[1]
    # Only wrapper tags may sit in between: the very next content block must be the notice.
    wrappers = r'(?:\s*</div>|\s*<div class="container">)*\s*'
    # V5.22 (SECTION_SYSTEM_V2 §3.3 PP-1; strict rule): the notice is the route's terminal status plate — still the
    # very next block after the stations
    notice_open = '<div class="pilota-rotta__stato" data-notice="pilot-not-authorised">'
    assert re.match(wrappers + re.escape(notice_open), after_diagram)
    notice = after_diagram.split('data-notice="pilot-not-authorised"', 1)[1].split("</section>", 1)[0]
    assert 'class="notice notice--warning"' in notice
    assert "proposition en cours de construction" in notice
    assert NOTICE_SENTENCE in notice


@pytest.mark.compliance
@pytest.mark.parametrize("lang", LANGS)
def test_pilot_never_claims_an_authorised_channel(get_html, seeded, phase3_open, lang):
    html = get_html(lang, GATED_PATHS["pilot"])
    assert 'data-notice="pilot-not-authorised"' in html
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    lowered = main.lower()
    # The statute is never quoted as if it were prescribed public text.
    for token in ("286/1998", "art. 23", "d.lgs", "décret législatif"):
        assert token not in lowered, (lang, token)
    for token in ("canal actif", "corridoio operativo", "ingressi garantiti", "visa garanti", "entrée assurée"):
        assert token not in lowered, (lang, token)
    # "autorisé" only ever appears inside the negative sentence of the notice.
    without_notice = main.replace(NOTICE_SENTENCE, "")
    assert "autorisé" not in without_notice.lower()


# The notice is UI wording (translated through the catalogues). Whatever the language, it must keep
# its NEGATIVE meaning: a translation that dropped the negation would present the project as an
# authorised channel. An untranslated catalogue entry falls back to the French source sentence.
NOTICE_NEGATION = {"fr": "ne signifie pas", "it": "non significa", "en": "does not mean", "ar": "لا يعني"}


@pytest.mark.compliance
@pytest.mark.parametrize("lang", LANGS)
def test_pilot_notice_keeps_its_negative_meaning_in_every_language(get_html, seeded, phase3_open, lang):
    html = get_html(lang, GATED_PATHS["pilot"])
    notice = html.split('data-notice="pilot-not-authorised"', 1)[1].split("</section>", 1)[0]
    body = notice.split('<div class="notice__body">', 1)[1].split("</div>", 1)[0]
    assert len(body.strip()) > 80, (lang, "the notice is a full sentence, never an empty block")
    assert NOTICE_NEGATION[lang] in body or NOTICE_SENTENCE in body, (lang, body)


def test_pilot_calls_to_action(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    cta = html.split('<section id="participer"', 1)[1].split("</section>", 1)[0]
    primary = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', cta, flags=re.S)
    assert primary.group(1) == "/fr/entreprises/recueil-des-besoins/"
    assert primary.group(2).strip() == _t("p2.forum.registration.button_secondary_pilot")
    secondary = re.search(r'<a class="btn btn--secondary[^"]*" href="([^"]+)"[^>]*>(.*?)</a>', cta, flags=re.S)
    assert secondary.group(1) == "/fr/collaboration/institutions/"
    assert secondary.group(2).strip() == _t("p3.institutions.button")


def test_pilot_draws_its_sequence_on_the_line_and_no_illustration(get_html, seeded, phase3_open):
    """CREATIVE_DIRECTION_V5 §19: the pilot-flow illustration is retired; the sequence stands on «la linea» alone."""
    html = get_html("fr", GATED_PATHS["pilot"])
    assert "pilot-flow.svg" not in html and "pilot-diagram__illustration" not in html
    # V5.22 (SECTION_SYSTEM_V2 §3.3 PP-1; strict rule): «la linea V2», the same line evolved (components/stepper.html)
    assert 'class="linea linea--large linea--across"' in html


def test_pilot_additions_follow_the_prescribed_sequence_only_when_visible(get_html, seeded, phase3_open):
    from ecosystem.models import PilotStep

    PilotStep.objects.create(order=9, label_fr="ÉVALUATION PARTAGÉE", is_visible=False)
    html = get_html("fr", GATED_PATHS["pilot"])
    assert "ÉVALUATION PARTAGÉE" not in html
    PilotStep.objects.filter(order=9).update(is_visible=True)
    html = get_html("fr", GATED_PATHS["pilot"])
    diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    labels = re.findall(r'<p class="linea__label[^"]*"[^>]*>(.*?)</p>', diagram)  # V5.22 §3.3 PP-1 (as above)
    assert labels == SEQUENCE + ["ÉVALUATION PARTAGÉE"]


def test_pilot_sequence_ignores_a_tampered_database(get_html, seeded, phase3_open):
    """Gate G0: even a raw UPDATE of the mirror rows cannot change what the public page prints."""
    from ecosystem.models import PilotStep

    PilotStep.objects.filter(locked_index=1).update(label_fr="CANAL DÉJÀ ACTIF")
    html = get_html("fr", GATED_PATHS["pilot"])
    assert "CANAL DÉJÀ ACTIF" not in html
    assert SEQUENCE[0] in html


# ---------------------------------------------------------------------------------------------
# RTL
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("path", GATED_PATHS.values())
def test_arabic_pages_are_rtl_with_tagged_french_fallback(get_html, seeded, phase3_open, path):
    html = get_html("ar", path)
    assert '<html lang="ar" dir="rtl"' in html
    assert 'lang="fr"' in html
    assert html.count("<h1") == 1
