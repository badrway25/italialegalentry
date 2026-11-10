"""
V5.22 — Page Composition V2, lane P2 «system, trust and reading» (SECTION_SYSTEM_V2 §3.2, §3.11–§3.15, §3.17, §3.18;
label v522-p2-build): what the compositions promise, rendered by the server (the browser half is
tests/frontend/test_pages_browser_v522_p2.py; the Forum's is apps/forum/tests/test_forum_v522.py).

  * every prescribed text a composition re-composes stands as ONE element carrying its key, its text the registry's;
  * the legally required lines stay visible (the trademark, «Définition à caractère informatif.», the G2 notice, the
    privacy link where the board collects nothing but leads to the form);
  * the network's map, the FAQ's explorer and the glossary's rail are the library's modules on complete markup (every
    entry in the page without script);
  * the promoter's identification comes from its one source (pages.identity) and nowhere else;
  * the contact architecture is unchanged (the channels' tests are test_contact_channels_v519.py).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from cms import locked_content
from pages.tests.conftest import LANGS, text_of

pytestmark = pytest.mark.django_db

ROOT = Path(__file__).resolve().parents[3]


def _main(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")


def _locked(soup: BeautifulSoup, key: str) -> list[str]:
    return [el.get_text() for el in soup.select(f'[data-locked="{key}"]')]


# ---- /le-projet/ (§3.2) ----------------------------------------------------------------------------------------------
def test_the_project_is_one_story_beside_one_figure(page, seeded, phase3_open):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    story = main.select_one('[data-sec="racconto"] .racconto[data-sec-js~="racconto"]')
    assert story is not None
    steps = story.select("section.racconto__passo")
    assert [s["id"] for s in steps] == ["project-presentation", "project-why", "project-promoter"]
    # each step keeps its chapter's anchor: #project-why-title still lands on «Pourquoi»
    assert [s.find("h2")["id"] for s in steps] == [
        "project-presentation-title",
        "project-why-title",
        "project-promoter-title",
    ]
    figure = story.select_one(".racconto__figura")
    # V5.30 Fast Visual Variety Correction §5, §11 (V5.20 strict rule; a material panel, no drawing): the arch with
    # its rays
    # and its foundations is gone, the figure is the five actors named on a night panel
    assert figure["aria-hidden"] == "true" and not figure.select(".sistema, .sistema__rotta, .sistema__fondamenta")
    # the five actors' nodes: one register (§4.10), every node its registry glyph and now its name
    nodes = figure.select("ul.sistema__nodi[data-registro] > li.sistema__nodo")
    assert len(nodes) == 5 and all(node.select_one("svg use") for node in nodes)
    assert all(node.select_one(".sistema__nome").get_text(strip=True) for node in nodes)
    # the three chapters' prescribed texts, each one element, whole
    assert _locked(main, "p3.hero.body") == [text_of("p3.hero.body")]
    assert _locked(main, "p2.forum.why.body") == [text_of("p2.forum.why.body")]
    why = main.select_one('[data-locked="p2.forum.why.body"]')
    assert [span["class"] for span in why.find_all("span", recursive=False)] == [
        ["ls", "ls-1"],
        ["ls", "ls-2"],
        ["ls", "ls-3"],
    ]
    # no layer of the figure waits for a step (V5.30, as above): the words change, the panel stands
    assert not figure.select("[data-from]")


def test_without_phase3_the_story_starts_at_pourquoi(page, seeded):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    steps = main.select("section.racconto__passo")
    assert [s["id"] for s in steps] == ["project-why", "project-promoter"]
    assert _locked(main, "p3.hero.body") == []
    # V5.30 Fast Visual Variety Correction §5, §11 (V5.20 strict rule): the panel is the same whichever step opens
    # the story
    figure = main.select_one(".racconto__figura")
    assert not figure.select("[data-from]") and len(figure.select("li.sistema__nodo")) == 5


@pytest.mark.parametrize("lang", LANGS)
def test_the_project_panorama_doors_and_foot(page, seeded, phase3_open, lang):
    _response, html = page(f"/{lang}/le-projet/")
    main = _main(html)
    assert main.select_one('[data-sec="panorama"] figure[data-slot="project.volumes"]') is not None
    doors = main.select(".projet-porte ul.mosaico--porte > li")
    assert len(doors) == 4
    assert [d["data-audience"] for d in doors] == ["person", "company", "institution", "university"]
    assert all(d.select_one("a.sez-stretch[href]") for d in doors)
    # the actors' sentences stay on /reseau/: the doors say the name and the way in
    assert "Elles s’informent" not in str(main.select_one(".projet-porte"))
    foot = main.select_one(".projet-piede")
    assert foot.select_one("p.page-trademark[data-trademark]") is not None
    assert len(foot.select(".projet-piede__vie a.link-arrow")) == 3


# ---- /reseau/ (§3.11) ------------------------------------------------------------------------------------------------
def test_the_network_head_is_the_map(page, seeded, phase3_open):
    _response, html = page("/fr/reseau/")
    main = _main(html)
    head = main.select_one('header.ingresso[data-sec-js~="mappa"]')
    assert head is not None and head["data-compose"] == "network"
    assert len(main.find_all("h1")) == 1
    tabs = head.select(".mappa__nodi .mappa__tasto")
    assert [t["href"] for t in tabs] == ["#rete-hub"] + [
        f"#rete-{k}" for k in ("persons", "companies", "institutions", "universities", "professionals")
    ]
    panels = head.select(".rete__pannelli > section")
    assert [p["id"] for p in panels] == [t["href"][1:] for t in tabs]
    # the hub's entry is «En bref», whole (exactly what the old chapter said); the old register is gone (words once)
    assert _locked(main, "p3.hero.body") == [text_of("p3.hero.body")]
    assert main.select(".actor-list") == []
    assert [p["data-actor"] for p in panels[1:]] == [
        "persons",
        "companies",
        "institutions",
        "universities",
        "professionals",
    ]
    # the ring's drawing stays decorative; the controls are the links; the entries are one register of five glyphs
    assert head.select_one(".fronte-rete__lines")["aria-hidden"] == "true"
    assert head.select_one('.ingresso__aside.fronte-rete ul.mappa__nodi.mappa__anello[role="list"]') is not None
    register = head.select_one(".rete__pannelli[data-registro]")
    assert [use["href"].rsplit("#icon-", 1)[1] for use in register.select(".sez-disc use")] == [
        "person",
        "building",
        "institution",
        "university",
        "briefcase",
    ]


def test_without_phase3_the_map_opens_on_its_first_actor(page, seeded):
    _response, html = page("/fr/reseau/")
    main = _main(html)
    assert main.select_one("#rete-hub") is None and main.select_one(".fronte-rete__hub") is None
    assert main.select(".mappa__tasto")[0]["href"] == "#rete-persons"
    assert _locked(main, "p3.hero.body") == []


def test_the_network_closes_on_the_approdo(page, seeded):
    _response, html = page("/fr/reseau/")
    main = _main(html)
    band = main.select_one('section.sez--approdo[data-ground="stone"][data-verb~="light"]')
    hrefs = [a["href"] for a in band.select("a.approdo__link")]
    assert hrefs == ["/fr/forum/", "/fr/agami/"]
    forum = band.select_one(".approdo__tessera--forum")
    assert forum is not None and forum.select_one("svg") is None  # Q4: the Forum's tile is typographic
    # round 1 (QA_ROUND1 m5): the night tile carries the Forum's own prescribed subtitle, whole — never an empty box
    assert forum.select_one("p.approdo__riga").get_text() == locked_content.get("p2.forum.header.subtitle", "fr")[0]
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule: the tiles' glyphs left — «l'approdo» is a divided link list, 21st.dev
    # 28595): no row draws a glyph, a tile or a plate, and every row still says its title as its link
    rows = band.select(".approdo__tessera")
    assert len(rows) == 2 and all(row.select_one("svg, .sez-tile, .sez-disc") is None for row in rows)
    assert all("sez-plate" not in row["class"] and row.select_one("a.approdo__link").get_text().strip() for row in rows)


# ---- /contact/ (§3.12) -----------------------------------------------------------------------------------------------
def test_the_contact_page_is_one_board_and_three_doors(page, seeded, whatsapp_channel):
    _response, html = page("/fr/contact/")
    main = _main(html)
    # the head's address is said once in the body: its sentence is its caption
    head = main.select_one("header.ingresso")
    assert "Tous les formulaires du site sont acheminés vers cette adresse." in head.get_text()
    # the old chapter «Par e-mail»'s anchor goes with its address (the head's action)
    assert head.select_one('p.fronte-azione#contact-email-title a[href="mailto:contact@agamieuromed.org"]') is not None
    assert len(main.select('a[href="mailto:contact@agamieuromed.org"]')) == 2  # the head's action and the G2 notice's
    board = main.select_one('section.sez--centralino[aria-labelledby="contact-voice-title"]')
    assert board is not None
    assert [li["class"] for li in board.select("ul.canali > li")] == [
        ["canale", "canale--voce"],
        ["canale", "canale--whatsapp"],
    ]
    plate = board.select_one(".canale--modulo")
    assert plate.select_one('[data-gate="forms-closed"]') is not None  # G2 closed: the notice in the same plate
    assert plate.select_one('a.btn--secondary[href="/fr/contact/formulaire/"]') is not None
    # the privacy link is the board's legal foot, as visible as the board
    assert board.select_one('.centralino__dati a[href="/fr/privacy-policy/"]') is not None
    doors = main.select(".contatto-porte ul.mosaico--porte > li")
    assert [d["data-audience"] for d in doors] == ["company", "institution", "university"]
    assert [d.select_one("a")["href"] for d in doors] == [
        "/fr/entreprises/recueil-des-besoins/",
        "/fr/collaboration/institutions/",
        "/fr/collaboration/universites-formation/",
    ]


def test_with_the_forms_open_the_board_holds_the_page_s_one_primary(page, seeded, legal_published):
    _response, html = page("/fr/contact/")
    main = _main(html)
    assert len(main.select(".btn--primary")) == 1
    assert main.select_one('.canale--modulo a.btn--primary[href="/fr/contact/formulaire/"]') is not None
    assert main.select_one('[data-gate="forms-closed"]') is None


# ---- /agami/ (§3.17, V5.23) ------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_the_promoter_page_identity_and_plate(page, seeded, phase3_open, lang):
    _response, html = page(f"/{lang}/agami/")
    main = _main(html)
    identita = main.select_one('section.agami-identita[data-sec="campata"]')
    # V5.30 §8 (the owner's final art direction, an approved decision; strict rule V5.20): the plate masked from the
    # reading edge holds «En bref», the role panel of verified facts, instead of the drawn colonnade — the same plate,
    # revealed the same way, now with content; and the band draws nothing (stronger: no temple returns unnoticed). The
    # official logo stands in the head's composed seat (tests/compliance/test_agami_assets_v530.py holds both)
    plate = identita.select_one('.agami-identita__lastra[data-verb~="mask"]')
    assert plate is not None and len(plate.select("dl.agami-breve > .agami-breve__voce")) == 3
    assert not identita.select("svg"), "the identity band draws no colonnade (V5.30 §8)"
    assert _locked(main, "p2.forum.who.body") == [locked_content.get("p2.forum.who.body", lang)[0]]
    # the FAQ's near-identical answer: a disclosure under the text, closed, its words unchanged
    disclosure = identita.select_one("details.agami-identita__domanda")
    assert disclosure is not None and not disclosure.has_attr("open")
    plate = main.select_one('section.agami-targa[data-ground="night"]')
    labels = [dt.get_text(strip=True) for dt in plate.select(".agami-id__voci dt")]
    assert len(labels) == 5 and "RUNTS" in labels
    assert plate.select_one(".agami-id__nome").get_text() == "AGAMI — Dialogo Giuridico Interculturale APS"
    # round 1 (QA_ROUND1 m11, m8): an office reads as the owner wrote it — its lines joined by his commas in the text
    # and the accessibility tree (never «n. 2936061») — its Italian lines one left-to-right box, the country after it
    from pages import identity

    offices = [dd for dd in plate.select(".agami-id__voci dd") if dd.select_one(".agami-id__luogo")]
    assert len(offices) == 2
    for dd, office in zip(offices, (identity.REGISTERED_OFFICE, identity.OPERATIONAL_OFFICE), strict=True):
        town = f"{office['postcode']} {office['town']}" + (f" ({office['province']})" if office["province"] else "")
        assert dd.get_text().startswith(f"{office['street']}, {town}, "), dd.get_text()
        assert dd.select_one(".agami-id__luogo")["lang"] == "it"


def test_the_promoter_s_identification_has_one_source():
    """V5.23: the owner's fields live in pages/identity.py — no template and no other module retypes them; the one
    other home is the locked registry, whose prescribed privacy notice names its data controller (a legal text, never
    retyped: apps/cms/locked_content.py)."""
    from pages import identity

    values = (identity.TAX_CODE, identity.RUNTS, identity.REGISTRATION, identity.LEGAL_FORM)
    allowed = {ROOT / "apps" / "pages" / "identity.py", ROOT / "apps" / "cms" / "locked_content.py"}
    for path in [*ROOT.joinpath("apps").rglob("*.py"), *ROOT.joinpath("templates").rglob("*.html")]:
        if "tests" in path.parts or path in allowed or "migrations" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for value in values:
            assert value not in text, (path, value)


# ---- /attention-aux-fraudes/ (§3.18) ---------------------------------------------------------------------------------
def test_the_fraud_page_reports_and_informs_in_one_split(page, seeded, phase3_open):
    _response, html = page("/fr/attention-aux-fraudes/")
    main = _main(html)
    split = main.select_one('[data-sec="frodi"]')
    report = split.select_one("section.frodi__segnala")
    assert report.select_one('a.frodi__indirizzo[href="mailto:contact@agamieuromed.org"]')
    # round 1 (QA_ROUND1 M10; SECTION_SYSTEM_V2 §3.18, §4.9 n° 9): the plate's ink rule is the protection's — its top
    # rule, drawn from the reading edge — and the sill of the shield mark at body scale; the address is the plate's
    # action for the seal system (its hover and focus deepen the keyhole), the plate its scope
    assert report.has_attr("data-sigillo-scope")
    assert report.select_one('.frodi__soglia[data-verb~="draw"]')
    assert report.select_one('.frodi__scudo svg[data-mark="ile-scudo"]')
    assert report.select_one('a.frodi__indirizzo[data-azione][href="mailto:contact@agamieuromed.org"]')
    # round 2 (QA_ROUND2 M7; §1 rule 7 «FAQ answers behind a disclosure»; strict rule V5.20 — the FAQ's way was a tile
    # linking the permalink): the page answers its own question — the prescribed question opens the prescribed answer in
    # place (the system's accordion, closed), each whole and once on the page, the permalink under the answer; the two
    # other ways stay route tiles
    question = next(i for i in locked_content.get("p3.faq.items", "fr")[0] if i["key"] == "faq_guaranteed_visa_offer")
    disclosure = split.select_one(".accordion.frodi__domanda > details.accordion__item#frodi-domanda")
    assert disclosure is not None and not disclosure.has_attr("open")
    assert disclosure.select_one("summary .frodi__domanda-testo").get_text() == question["question"]
    panel = disclosure.select_one(".accordion__panel")
    assert panel.select_one("p").get_text() == question["answer"]
    assert panel.select_one('a[href="/fr/faq/#faq_guaranteed_visa_offer"]') is not None
    assert split.get_text().count(question["question"]) == 1 and main.get_text().count(question["answer"]) == 1
    tiles = split.select("ul.mosaico--rimando > li a")
    assert [a["href"] for a in tiles] == ["/fr/parcours/", "/fr/glossaire/"]
    # no authority, police, embassy or portal link
    assert all(a["href"].startswith(("/", "mailto:")) for a in split.select("a[href]"))


# ---- /faq/ (§3.13) ---------------------------------------------------------------------------------------------------
def test_the_faq_is_one_list_whose_rows_are_the_permalinks(page, seeded, phase3_open):
    """FINAL MICRO-PASS §6 B1 (V5.20 strict rule; replaces «the FAQ is an explorer whose panels are the permalinks»):
    the questions are one list of the system's disclosures — no explorer, no index, no seal beside the answers — and its
    rows keep the permalinks the trust band and the fraud page link to; the fraud row keeps its ink rule and its one
    mark."""
    _response, html = page("/fr/faq/")
    main = _main(html)
    rows = main.select('section#questions[data-cerca="faq-q"] .accordion.faq-lista > details.accordion__item.faq-item')
    assert rows and not main.select('.faq-esploratore, .indice, [data-sec-js~="indice"], .indice__tessera')
    # the trust band's four links and the fraud page's land on their question
    ids = [row["id"] for row in rows]
    for key in (
        "faq_visas",
        "faq_recruitment_agency",
        "faq_preassessment_guarantee",
        "faq_diplomas",
        "faq_guaranteed_visa_offer",
    ):
        assert key in ids, key
    fraud = main.select_one("details.faq-item#faq_guaranteed_visa_offer")
    assert "faq-item--marcata" in fraud["class"] and fraud.select_one("summary use[href*='ile-scudo']")
    # no seal and no item tile beside the answers: the answer is the row's own words
    assert main.select(".sigillo[data-mark='ile-domande'], .faq-item__glifo, .faq-lista .sez-tile") == []
    # the foot «il rimando»
    tiles = [a["href"] for a in main.select(".faq-rimando ul.mosaico--rimando a")]
    assert tiles == ["/fr/glossaire/", "/fr/attention-aux-fraudes/", "/fr/contact/"]


# ---- /glossaire/ (§3.14) ---------------------------------------------------------------------------------------------
def test_the_glossary_is_a_rail_beside_term_cards(page, seeded, phase3_open):
    _response, html = page("/fr/glossaire/")
    main = _main(html)
    rail = main.select_one('nav.az-index[data-sec-js~="spia"]')
    assert rail is not None
    letters = [a["href"] for a in rail.select("a")]
    assert all(main.select_one(h) is not None for h in letters)
    cards = main.select(".lessico__carta")
    assert len(cards) == 10
    # round 1 (QA_ROUND1 M7): ONE register — the ten cards in one grid, in the letters' order; each letter is the
    # heading (h2) set in its first card, the anchor the rail reaches, and the cards up to the next letter are its own
    grid = main.select(".lessico__registro > .lessico__carte")
    assert len(grid) == 1 and len(grid[0].select(":scope > .lessico__carta")) == 10
    letters_seen, run = [], {}
    for card in cards:
        mark = card.select_one(":scope > h2.lessico__lettera")
        if mark is not None:
            assert mark["id"] == f"lettre-{mark.get_text()}"
            letters_seen.append(mark.get_text())
        run.setdefault(letters_seen[-1], []).append(card.select_one("h3.lessico__termine").get_text().strip())
    assert [f"#lettre-{letter}" for letter in letters_seen] == letters
    assert all(term[0].upper() == letter for letter, terms in run.items() for term in terms), run
    assert run["C"] == ["Carta blu UE", "Codice fiscale"]
    # «Où le rencontrer»: the pathways that name the term (live sheets), labelled by their prescribed titles
    nulla = main.select_one("#nulla_osta")
    chips = {a["href"] for a in nulla.select("a.lessico__chip")}
    assert {
        "/fr/parcours/salaried_work/",
        "/fr/parcours/skilled_work_eu_blue_card/",
        "/fr/parcours/family_reunification/",
    } <= chips
    titles = {p["key"]: p["title"] for p in locked_content.get("p3.persons.pathways", "fr")[0]}
    assert titles["salaried_work"] in nulla.get_text()
    # a general term leads to the pathways' index
    assert main.select_one('#codice_fiscale a.lessico__chip[href="/fr/parcours/"]') is not None
    # the definitions stand whole and visible
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    assert nulla.select_one("p.lessico__definizione").get_text() == terms["nulla_osta"]["definition"]


@pytest.mark.parametrize("lang", LANGS)
def test_the_term_page_takes_its_frontispiece_and_its_plate(page, seeded, phase3_open, lang):
    _response, html = page(f"/{lang}/glossaire/nulla_osta/")
    assert '<link rel="stylesheet" href="/static/css/dist/pages/css/fronte.css">' in html.split("</head>", 1)[0]
    main = _main(html)
    head = main.select_one('header.ingresso[data-compact][data-fronte="learning"]')
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule: the head folios' seals left — `ile-lessico` with them): the folio is
    # typographic and still says its label
    assert head is not None and head.select_one(".sigillo, [data-mark]") is None
    assert head.select_one("p.ingresso__label").get_text(strip=True)
    # round 2 (QA_ROUND2 M5; strict rule V5.20 — the h1 carried lang="it" and stood as a left-to-right block 592 px
    # short of the Arabic reading edge): the h1 takes the page's direction and holds the term as a run of its language
    h1 = head.find("h1")
    assert h1.get_text() == "Nulla osta"
    if lang == "it":
        assert h1.find("span") is None
    else:
        assert not h1.has_attr("lang") and h1.select_one("span[lang='it']").get_text() == "Nulla osta"
    plate = main.select_one(".scheda__lastra.sez-plate")
    assert plate.select_one("p.glossary-term__definition") is not None
    assert plate.select_one("p.glossary-term__note") is not None  # «Définition à caractère informatif.»: always shown
    # FINAL MICRO-PASS §6 B2 (V5.20; was «the outlined initial behind the plate is aria-hidden»): the 288 px initial
    # left — the term is named once, by the h1; the plate and its rows below are unchanged
    assert main.select_one(".scheda__iniziale") is None and main.get_text().count(h1.get_text()) >= 1
    assert main.select_one('.scheda__legami a.lessico__chip[href="/' + lang + '/parcours/salaried_work/"]') is not None
    # round 1 (QA_ROUND1 M7; §1 rule 7 «definitions behind glossary chips», §2 L): the related terms' definitions are
    # disclosed in place — native exclusive disclosures, closed, each definition whole in the page and its term's link;
    # round 2 (QA_ROUND2 m5; strict rule V5.20 — the rows were the library's «indice» disclosure): the system's
    # accordion, whose CSS every page has (main.css), so the term page's route sheet needs no pattern sheet of its own
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    rows = main.select(".glossary-term__related .accordion > details.accordion__item[name='termini-legati']")
    assert rows and not any(row.has_attr("open") for row in rows)
    for row in rows:
        term = row.select_one("summary").get_text(strip=True)
        key = next(k for k, t in terms.items() if t["term"] == term)
        assert terms[key]["definition"] in row.select_one(".accordion__panel").get_text()
        assert row.select_one(f'.scheda__link a[href="/{lang}/glossaire/{key}/"]') is not None


# ---- /vivre-en-italie/ (§3.15) ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_living_opens_on_its_panorama_and_closes_on_what_exists(page, seeded, phase3_open, lang):
    _response, html = page(f"/{lang}/vivre-en-italie/")
    main = _main(html)
    head = main.select_one('.fronte-wrap[data-fronte="territory"]')
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule: the head's `ile-vivere` seal in its niche left, and its scope with
    # it): the head is the prescribed title and its way down — no seal, no drawing —, the action still there
    assert head.select_one(".sigillo, [data-mark]") is None and len(main.find_all("h1")) == 1
    assert head.select_one("[data-sigillo-scope]") is None
    assert head.select_one('a.vivere-testa__azione[data-azione][href="#living-settle-title"]') is not None
    assert main.select_one("#living-settle-title") is not None
    frame = main.select_one(".vivere-panorama__quadro[data-parallax] figure[data-slot='living.street']")
    assert frame is not None and not frame.has_attr("data-reveal"), "the LCP is never masked"
    assert frame.select_one("img")["fetchpriority"] == "high"
    lead = main.select_one(".vivere-panorama__lastra p.page-header__lead")
    assert lead.get_text() == locked_content.get("p3.living.body", lang)[0]
    # round 1 (QA_ROUND1 M8): «pour s'installer», two rows of one kind each — the two prescribed terms as the
    # glossary's dictionary cards (the definition whole), then the two ways on as route tiles; the lead's plate is no
    # longer a head (its words never wait: m10)
    band = main.select_one('section.vivere-installer[data-ground="stone"]')
    # final round (QA_ROUND3 m1): the moment meets its band — no third ground between them: the moment's ground is the
    # band's (the frame fills it on a desktop; below 64 rem the lead's plate stands on it) and nothing stands between
    moment = main.select_one('.vivere-panorama[data-ground="stone"]')
    assert moment is not None and moment.find_next_sibling() is band
    cards = band.select(".vivere-installer__termini > article.lessico__carta")
    assert [c["id"] for c in cards] == ["permesso_di_soggiorno", "codice_fiscale"]
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    for card in cards:
        assert card.select_one("a.sez-stretch")["href"] == f"/{lang}/glossaire/{card['id']}/"
        definition = card.select_one("p.lessico__definizione")
        if lang != "ar":
            assert definition.get_text() == terms[card["id"]]["definition"]
            continue
        # V5.27 / FINAL_DELIVERY_V2 R7′ (V5.20, the steward's amendment at the v524-pub2 merge): a definition is
        # substantive (C-SUBST-FR) and this is not its page — on /ar/ the card says, in Arabic, where its words stand
        # (the pointer line, exactly), and no French run is drawn (stronger than the French it read)
        from django.utils import translation

        from cms import locked_renderings

        index = [t["key"] for t in locked_content.get("p3.glossary.terms", "fr")[0]].index(card["id"])
        with translation.override("ar"):
            pointer = str(locked_renderings.pointer_line(f"p3.glossary.terms[{index}].definition"))
        assert definition.get_text() == pointer and definition.get("lang") is None
        assert terms[card["id"]]["definition"] not in card.get_text()
    hrefs = [a["href"] for a in band.select("ul.mosaico--rimando > li a")]
    assert hrefs[0].endswith("/formation/#apres-l-arrivee") and hrefs[-1] == f"/{lang}/faq/" and len(hrefs) == 2
    assert main.select_one(".vivere-panorama__lastra.page-header") is None
    # Q8: no theme card while no theme carries a reviewed sheet
    assert main.select(".living-topics") == []


# ---- the CSS of the family -------------------------------------------------------------------------------------------
#: round 2 (QA_ROUND2 m5; the owner's V5.22 standing constraint «page-only sheets / route-specific bundles with their
#: own recorded budgets»; strict rule V5.20 — the family's partials were all in the two shared sheets): a page's own
#: compositions are its route sheet's, linked by that page only, between its shared sheet and the frontispiece's
#: V5.24 lane PUB2 (FINAL_DELIVERY_V2 §3.6, R4 a; V5.20 — the same invariant on one more sheet): Le projet's
#: partial left the shared interior sheet for a route sheet of its own, with the material partial
#: (v5/_materia.css) for the incastro — the Réseau and AGAMI pages stood 407 and 464 B under their 56 320 B
#: letter, which the material on the shared sheet would have passed; every other institutional page is
#: lighter by Le projet's compositions
ROUTE_SHEETS = {
    # FINAL MICRO-PASS §6 B1 (V5.20; the same invariant on what the sheet now holds): the explorer's pattern partial
    # (v5/_sec-indice.css) left the FAQ's route sheet with the explorer — the list is the system's accordion (main.css)
    "apps/cms/static/cms/faq.css": (["_faq-v2.css"], ["faq/index.html"]),
    "apps/pages/static/pages/css/projet.css": (["../../css/v5/_materia.css", "_projet.css"], ["pages/project.html"]),
    "apps/cms/static/cms/lessico.css": (
        ["_lessico-v2.css"],
        ["glossary/index.html", "glossary/term.html", "living/index.html"],
    ),
    # V5.20, citing V5.30 §7: the Italy + Morocco primitive under Réseau's closing band joins its route sheet, once
    "apps/pages/static/pages/css/rete.css": (["../../css/v5/_intesa.css", "_rete.css"], ["pages/network.html"]),
    "apps/pages/static/pages/css/agami.css": (["_agami.css"], ["pages/agami.html"]),
    "apps/pages/static/pages/css/frodi.css": (["_frodi.css"], ["pages/antifraud.html"]),
}


def test_the_family_sheets_import_the_library_and_their_partials_never_main_css():
    main_css = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    for partial in (
        "_projet.css",
        "_rete.css",
        "_contatto.css",
        "_agami.css",
        "_frodi.css",
        "_lettura-v2.css",
        "_faq-v2.css",
        "_lessico-v2.css",
    ):
        assert partial not in main_css
    interior = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "interior.css").read_text(encoding="utf-8")
    for partial in ("_sezioni.css", "_sec-racconto.css", "_sec-mosaico.css", "_sec-strato.css"):
        assert partial in interior, partial
    # V5.24 (FINAL_DELIVERY_V2 §3.6, R3, R4 a): the material partial is page-only and reaches the institutional pages
    # through Le projet's route sheet alone; _projet.css left the shared sheet with it (ROUTE_SHEETS checks its imports)
    assert "_materia.css" not in interior and "_projet.css" not in interior
    assert "_materia.css" not in main_css
    lettura = (ROOT / "apps" / "cms" / "static" / "cms" / "lettura.css").read_text(encoding="utf-8")
    for partial in ("_sezioni.css", "_sec-mosaico.css", "_lettura-v2.css"):
        assert partial in lettura, partial
    templates = ROOT / "templates"
    for sheet, (imports, linkers) in ROUTE_SHEETS.items():
        assert re.findall(r'@import url\("([^"]+)"\);', (ROOT / sheet).read_text(encoding="utf-8")) == imports, sheet
        shared = interior if "/pages/" in sheet else lettura
        for partial in imports:
            assert partial.rsplit("/", 1)[-1] not in shared, (sheet, partial, "drawn once, in its route sheet")
        link = "{% static 'css/dist/" + sheet.split("/static/", 1)[1] + "' %}"
        for template in templates.rglob("*.html"):
            name = template.relative_to(templates).as_posix()
            assert (link in template.read_text(encoding="utf-8")) is (name in linkers), (sheet, name)
    forum = (ROOT / "apps" / "forum" / "static" / "forum" / "forum.css").read_text(encoding="utf-8")
    assert "_sezioni.css" in forum and "_sigillo.css" in forum


@pytest.mark.parametrize(
    "path, sheet",
    [
        ("/fr/faq/", "cms/faq.css"),
        ("/fr/glossaire/", "cms/lessico.css"),
        ("/fr/glossaire/nulla_osta/", "cms/lessico.css"),
        ("/fr/vivre-en-italie/", "cms/lessico.css"),
        ("/fr/reseau/", "pages/css/rete.css"),
        ("/fr/agami/", "pages/css/agami.css"),
        ("/fr/attention-aux-fraudes/", "pages/css/frodi.css"),
        ("/fr/le-projet/", "pages/css/projet.css"),  # V5.24 lane PUB2
    ],
)
def test_a_route_sheet_sits_between_its_shared_sheet_and_the_frontispiece_s(page, seeded, phase3_open, path, sheet):
    _response, html = page(path)
    links = re.findall(r'<link rel="stylesheet" href="/static/css/dist/([^"?]+\.css)', html.split("</head>", 1)[0])
    shared = "cms/lettura.css" if sheet.startswith("cms/") else "pages/css/interior.css"
    at = links.index(sheet)
    assert links[at - 1] == shared and links[at + 1] == "pages/css/fronte.css", links
    routes = {route.split("/static/", 1)[1] for route in ROUTE_SHEETS}
    assert [link for link in links if link in routes] == [sheet], links


def test_no_family_class_shadows_a_chrome_class():
    """A page partial's block names are its own: «.targa» is the letterhead's reserved-space plate (the preserved
    navbar, V5.22 §9.8) — the AGAMI identification plate once took the name and wrapped the menu onto two rows."""
    chrome = (ROOT / "static" / "css" / "v5" / "chrome.css").read_text(encoding="utf-8")
    chrome_classes = set(re.findall(r"\.([a-z][a-z0-9_-]*)", re.sub(r"/\*.*?\*/", "", chrome, flags=re.S)))
    sheets = ["_projet.css", "_rete.css", "_contatto.css", "_agami.css", "_frodi.css"]
    for name in sheets:
        css = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / name).read_text(encoding="utf-8")
        own = set(re.findall(r"\.([a-z][a-z0-9_-]*)", re.sub(r"/\*.*?\*/", "", css, flags=re.S)))
        blocks = {c.split("__")[0] for c in own}
        # the html state class a sheet reads (.rm: the preview's reduced motion) and shared components are not blocks
        assert not (blocks & chrome_classes) - {"rm", "icon", "email", "link-arrow", "btn", "sez-disc", "sez-plate"}, (
            name,
            blocks & chrome_classes,
        )
