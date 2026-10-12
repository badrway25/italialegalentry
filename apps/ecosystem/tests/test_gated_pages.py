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
    assert 'class="ecosystem-photo"' in html, "the scheduled editorial row is visible in a preview"


# ---------------------------------------------------------------------------------------------
# Espace Institutions
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_institutions_prescribed_texts_and_button(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["institutions"])
    assert re.search(r'<p class="page-header__lead">' + re.escape(_t("p3.institutions.intro")) + "</p>", html)
    assert _t("p3.institutions.recipients") in html, "the recipients sentence is printed verbatim"
    button = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', html, flags=re.S)
    assert button, "prescribed CTA missing"
    assert button.group(1) == "/fr/collaboration/institutions/"
    assert button.group(2).strip() == _t("p3.institutions.button")


def test_institutions_recipients_are_a_styled_list_of_the_same_words(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["institutions"])
    block = html.split('data-block="recipients"', 1)[1].split("</section>", 1)[0]
    assert re.search(r'<h2 id="destinataires-title" class="section__title">Destinataires</h2>', block)
    items = re.findall(r'<span class="ecosystem-enum__text">(.*?)</span>', block)
    assert items == [
        "Régions",
        "Communes",
        "organismes publics",
        "Chambres de Commerce",
        "organismes du travail",
        "représentations diplomatiques et consulaires et institutions des pays partenaires",
    ]
    assert '<p class="visually-hidden">' + _t("p3.institutions.recipients") + "</p>" in block
    assert '<ul class="ecosystem-enum ecosystem-enum--two" aria-hidden="true">' in block


def test_institutions_secondary_links(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["institutions"])
    related = html.split('class="ecosystem-section ecosystem-related"', 1)[1].split("</section>", 1)[0]
    for href in ("/fr/forum/", "/fr/projet-pilote/", "/fr/partenaires/"):
        assert f'href="{href}"' in related


def test_institutions_fallback_language_marked(get_html, seeded, phase3_open):
    html = get_html("en", GATED_PATHS["institutions"])
    assert '<p class="page-header__lead"><span lang="fr">' + _t("p3.institutions.intro") + "</span></p>" in html
    assert '<p class="visually-hidden" lang="fr">' + _t("p3.institutions.recipients") + "</p>" in html
    assert re.search(r'<ul class="ecosystem-enum[^"]*" aria-hidden="true" lang="fr">', html)


# ---------------------------------------------------------------------------------------------
# Espace Universités et Formation
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_universities_prescribed_texts_and_button(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["universities"])
    assert re.search(r'<p class="page-header__lead">' + re.escape(_t("p3.universities.intro")) + "</p>", html)
    button = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', html, flags=re.S)
    assert button and button.group(1) == "/fr/collaboration/universites-formation/"
    assert button.group(2).strip() == _t("p3.universities.button")


def test_universities_enumeration_lists_keep_every_word(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["universities"])
    block = html.split('data-block="universities-enumeration"', 1)[1].split('<div id="partenariat"', 1)[0]
    items = re.findall(r'<span class="ecosystem-enum__text">(.*?)</span>', block)
    assert items == [
        "Universités",
        "organismes de formation",
        "instituts et centres de recherche",
        "formation",
        "stages",
        "mobilité internationale",
        "échanges d’étudiants",
        "programmes conjoints",
        "coopération académique",
        "formation avant le départ et valorisation des compétences",
    ]
    # The breakdown is presentational: the verbatim lead above it is the accessible text.
    assert '<div id="domaines" class="ecosystem-section" aria-hidden="true"' in html


def test_universities_links_to_training_and_pathways(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["universities"])
    related = html.split('class="ecosystem-section ecosystem-related"', 1)[1].split("</section>", 1)[0]
    assert 'href="/fr/formation/"' in related
    assert 'href="/fr/parcours/"' in related


# ---------------------------------------------------------------------------------------------
# Projet Pilote
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
def test_pilot_title_and_body(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    assert re.search(r'<h1 class="page-header__title">' + re.escape(_t("p3.pilot.title")) + "</h1>", html)
    assert re.search(r'<p class="page-header__lead">' + re.escape(_t("p3.pilot.body")) + "</p>", html)


@pytest.mark.compliance
def test_pilot_sequence_has_the_eight_prescribed_steps_in_order(get_html, seeded, phase3_open):
    assert locked_content.get("p3.pilot.sequence", "fr")[0] == SEQUENCE
    html = get_html("fr", GATED_PATHS["pilot"])
    diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    assert re.search(r"<ol class=\"timeline[^\"]*\" aria-label=", diagram), "ordered-list semantics"
    labels = re.findall(r'<p class="timeline__label">(.*?)</p>', diagram)
    assert labels == SEQUENCE
    assert 'data-steps="8"' in html
    assert "timeline__text" not in diagram, "each step is a short prescribed label only"


def test_pilot_notice_follows_the_diagram_immediately(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    after_diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[1]
    # Only wrapper tags may sit in between: the very next content block must be the notice.
    wrappers = r'(?:\s*</div>|\s*<div class="container">)*\s*'
    notice_open = '<div class="pilot-diagram__notice" data-notice="pilot-not-authorised">'
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
    cta = html.split('<div id="participer"', 1)[1].split("</section>", 1)[0]
    primary = re.search(r'<a class="btn btn--primary[^"]*" href="([^"]+)"[^>]*>\s*(.*?)\s*<svg', cta, flags=re.S)
    assert primary.group(1) == "/fr/entreprises/recueil-des-besoins/"
    assert primary.group(2).strip() == _t("p2.forum.registration.button_secondary_pilot")
    secondary = re.search(r'<a class="btn btn--secondary[^"]*" href="([^"]+)"[^>]*>(.*?)</a>', cta, flags=re.S)
    assert secondary.group(1) == "/fr/collaboration/institutions/"
    assert secondary.group(2).strip() == _t("p3.institutions.button")


def test_pilot_illustration_is_decorative_and_local(get_html, seeded, phase3_open):
    html = get_html("fr", GATED_PATHS["pilot"])
    img = re.search(r'<img class="pilot-diagram__illustration"[^>]*>', html).group(0)
    assert 'src="/static/img/illustrations/pilot-flow.svg"' in img
    assert 'alt=""' in img and 'aria-hidden="true"' in img


def test_pilot_additions_follow_the_prescribed_sequence_only_when_visible(get_html, seeded, phase3_open):
    from ecosystem.models import PilotStep

    PilotStep.objects.create(order=9, label_fr="ÉVALUATION PARTAGÉE", is_visible=False)
    html = get_html("fr", GATED_PATHS["pilot"])
    assert "ÉVALUATION PARTAGÉE" not in html
    PilotStep.objects.filter(order=9).update(is_visible=True)
    html = get_html("fr", GATED_PATHS["pilot"])
    diagram = html.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    labels = re.findall(r'<p class="timeline__label">(.*?)</p>', diagram)
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
