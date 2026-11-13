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
# RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: Le projet is
# «la carta» — the three chapters are three bands (each its own composition) instead of the steps of a sticky story, the
# five-actor figure that said the doors' list twice left, the doors are a titled index of real links on night. The same
# invariants, kept or made stronger: the chapters keep their ids and their headings' anchors, in order; every prescribed
# text stands as ONE element, whole, with its three sentence spans; no drawn layer (no figure); four spaces in the
# audiences' order, each a real link; the actors' sentences stay on /reseau/; the trademark line and the three ways on.
CHAPTERS = ["project-presentation", "project-why", "project-promoter"]


def _chapters(main: BeautifulSoup) -> list:
    return [s for s in main.select("section.sez[id]") if s["id"] in CHAPTERS]


def test_the_project_is_three_chapters_each_its_own_band(page, seeded, phase3_open):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    chapters = _chapters(main)
    assert [s["id"] for s in chapters] == CHAPTERS
    # each chapter keeps its anchor: #project-why-title still lands on «Pourquoi», and names its band
    assert [s.find("h2")["id"] for s in chapters] == [f"{c}-title" for c in CHAPTERS]
    assert all(s["aria-labelledby"] == f"{s['id']}-title" for s in chapters)
    # no figure, no drawing: the story's plate and its actors' list left (the doors carry the actors once)
    assert not main.select(".racconto, .racconto__figura, .sistema__nodi, [data-from], svg.mosaico__arco")
    # the three chapters' prescribed texts, each one element, whole
    assert _locked(main, "p3.hero.body") == [text_of("p3.hero.body")]
    assert _locked(main, "p2.forum.why.body") == [text_of("p2.forum.why.body")]
    why = main.select_one('[data-locked="p2.forum.why.body"]')
    assert [span["class"] for span in why.find_all("span", recursive=False)] == [
        ["ls", "ls-1"],
        ["ls", "ls-2"],
        ["ls", "ls-3"],
    ]
    # the bearer's band: the promoter's official seal, decorative and lazy, beside the prescribed answer
    seal = main.select_one("#project-promoter picture.projet-chi__sigillo[data-mark='agami.sigillo'] img")
    assert seal is not None and seal["alt"] == "" and seal["loading"] == "lazy"


def test_without_phase3_the_page_starts_at_pourquoi(page, seeded):
    _response, html = page("/fr/le-projet/")
    main = _main(html)
    assert [s["id"] for s in _chapters(main)] == ["project-why", "project-promoter"]
    assert _locked(main, "p3.hero.body") == []
    assert not main.select(".racconto__figura, [data-from]")


@pytest.mark.parametrize("lang", LANGS)
def test_the_project_volumes_spaces_and_foot(page, seeded, phase3_open, lang):
    _response, html = page(f"/{lang}/le-projet/")
    main = _main(html)
    assert main.select_one('#project-why figure[data-slot="project.volumes"]') is not None
    spaces = main.select(".projet-spazi ul.projet-spazi__lista > li.projet-spazio")
    assert len(spaces) == 4
    assert [d["data-audience"] for d in spaces] == ["person", "company", "institution", "university"]
    assert all(d.select_one("a.projet-spazio__link[href]") for d in spaces)
    # the actors' sentences stay on /reseau/: the spaces say the name and the way in
    assert "Elles s’informent" not in str(main.select_one(".projet-spazi"))
    foot = main.select_one(".projet-piede")
    assert foot.select_one("p.page-trademark[data-trademark]") is not None
    assert len(foot.select(".projet-piede__vie a.link-arrow")) == 3


# ---- /reseau/ (§3.11) ------------------------------------------------------------------------------------------------
def test_the_network_head_is_the_map(page, seeded, phase3_open):
    _response, html = page("/fr/reseau/")
    main = _main(html)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «l'esploratore»; the owner's «not arches, lines or nodes everywhere»): the map left the head's ring for
    # the explorer under it — the same tablist runtime (sezioni/mappa.js) on complete markup, its five actors' tabs
    # beside their panels; the old register is gone (words once); the entries keep their five audience glyphs in
    # order; nothing is drawn (no ring, no lines)
    head = main.select_one("header.rete-testa")
    assert head is not None and len(main.find_all("h1")) == 1 and head.find("h1") is not None
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (P2-4 of
    # the integration review): the prescribed presentation is Le projet's «En bref», one click away — the network's
    # head links it instead of repeating it: no p3.hero.body on /reseau/; the head's link lands on the project page's
    # «En bref», where the text stands whole, once (stronger: the text is followed to where it is shown)
    assert _locked(main, "p3.hero.body") == []
    link = head.select_one('p.rete-testa__rinvio > a[href="/fr/le-projet/#project-presentation"]')
    assert link is not None and link.get_text(strip=True) and link.find("svg") is None
    _response, project_html = page("/fr/le-projet/")
    project = _main(project_html)
    assert _locked(project, "p3.hero.body") == [text_of("p3.hero.body")]
    assert project.select_one('section#project-presentation [data-locked="p3.hero.body"]') is not None
    explorer = main.select_one('section.rete-esplora[data-sec-js~="mappa"]')
    tabs = explorer.select("ul.mappa__nodi.mappa__anello .mappa__tasto")
    assert [t["href"] for t in tabs] == [
        f"#rete-{k}" for k in ("persons", "companies", "institutions", "universities", "professionals")
    ]
    panels = explorer.select(".rete__pannelli > section")
    assert [p["id"] for p in panels] == [t["href"][1:] for t in tabs]
    assert main.select(".actor-list") == []
    assert [p["data-actor"] for p in panels] == [
        "persons",
        "companies",
        "institutions",
        "universities",
        "professionals",
    ]
    assert main.select(".fronte-rete__lines, .fronte-rete, .mappa__raggio, [data-compose='network']") == []
    assert [use["href"].rsplit("#icon-", 1)[1] for use in explorer.select(".rete__pannelli .rete__disc use")] == [
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «l'esploratore»): the closing band is the reading pages' foot — «il rimando», the divided link list
    # (components/sezioni/mosaico.html) — on stone: the Forum then the promoter, each row its title as its link over its
    # one line, the Forum's its own prescribed subtitle whole (round 1, QA_ROUND1 m5: never an empty box); no row draws
    # a glyph, a tile or a plate (FINAL MICRO-PASS §5 A3, kept), and no flag under the band (the V5.30 «intesa» left)
    band = main.select_one('section.sez.rete-approdo[data-sec="approdo"][data-ground="stone"]')
    hrefs = [a["href"] for a in band.select("ul.mosaico--rimando > li.mosaico__tessera > a.mosaico__link")]
    assert hrefs == ["/fr/forum/", "/fr/agami/"]
    rows = band.select("ul.mosaico--rimando > li.mosaico__tessera")
    forum = rows[0]
    assert forum.select_one("p.mosaico__riga").get_text() == locked_content.get("p2.forum.header.subtitle", "fr")[0]
    assert len(rows) == 2 and all(row.select_one("svg, .sez-tile, .sez-disc") is None for row in rows)
    assert all("sez-plate" not in row["class"] for row in rows)
    assert all(row.select_one("a.mosaico__link").get_text().strip() for row in rows)
    assert main.select(".intesa, [data-sec='intesa']") == []


# ---- /contact/ (§3.12) -----------------------------------------------------------------------------------------------
def test_the_contact_page_is_one_board_and_three_doors(page, seeded, whatsapp_channel):
    _response, html = page("/fr/contact/")
    main = _main(html)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «lo sportello»): the board is the channels desk beside the form's own seat. The address is said once in
    # the body, its sentence its caption (and its copy action beside it); the two voices follow it; while G2 is closed
    # the notice stands IN the form's seat (the form is the enquiries app's, on this page: no link to a closed form);
    # the privacy link is the desk's legal foot, as visible as the desk; the three doors close the page in their order
    desk = main.select_one(".sportello__canali")
    rows = desk.select("ul.sportello__lista > li")
    assert [li["class"] for li in rows] == [
        ["sportello-canale", "sportello-canale--email"],
        ["sportello-canale", "sportello-canale--voce"],
        ["sportello-canale", "sportello-canale--whatsapp"],
    ]
    assert "Tous les formulaires du site sont acheminés vers cette adresse." in rows[0].get_text()
    assert rows[0].select_one('a.email#contact-address[href="mailto:contact@agamieuromed.org"]') is not None
    assert len(main.select('a[href="mailto:contact@agamieuromed.org"]')) == 2  # the desk's address and the G2 notice's
    seat = main.select_one(".sportello__modulo#formulaire")
    assert seat.select_one('[data-gate="forms-closed"]') is not None
    assert main.select('a[href="/fr/contact/formulaire/"]') == []
    assert desk.select_one('.sportello__dati a[href="/fr/privacy-policy/"]') is not None
    doors = main.select(".sportello-mirate ul.sportello-mirate__lista > li")
    assert [d["data-audience"] for d in doors] == ["company", "institution", "university"]
    assert [d.select_one("a")["href"] for d in doors] == [
        "/fr/entreprises/recueil-des-besoins/",
        "/fr/collaboration/institutions/",
        "/fr/collaboration/universites-formation/",
    ]


def test_with_the_forms_open_the_board_holds_the_page_s_one_primary(page, seeded, legal_published):
    _response, html = page("/fr/contact/")
    main = _main(html)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «lo sportello»): the one primary is the form's own submit, in the form's seat — the enquiries form,
    # posted to the enquiries view
    assert len(main.select(".btn--primary")) == 1
    form = main.select_one('.sportello__modulo#formulaire form[method="post"][action="/fr/contact/formulaire/"]')
    assert form is not None and form.select_one('button.btn--primary[type="submit"]') is not None
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D, «l'avvertenza»), replacing round 1's (QA_ROUND1 M10) drawn sill, stroked shield and keyhole: one mark
    # for one message — the statement's shield in the head; the report plate draws no seal and keeps the address as
    # its one action, its disc the mail's mark (hidden from the accessibility tree), its words the address itself
    assert report.select(".frodi__soglia, .frodi__scudo, .sigillo, [data-sigillo-scope], [data-azione]") == []
    action = report.select_one('a.frodi__indirizzo[href="mailto:contact@agamieuromed.org"]')
    assert action.select_one('.frodi__disc[aria-hidden="true"]') is not None
    assert action.select_one(".email").get_text() == "contact@agamieuromed.org"
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D): the two other ways are rows on hairlines under the disclosure, in the same order
    tiles = split.select("ul.frodi__rotte > li > a.frodi__rotta")
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (lane D): the way to a person is the guide's help card beside the list (once on the page); the foot keeps the
    # two reading ways
    tiles = [a["href"] for a in main.select(".faq-rimando ul.mosaico--rimando a")]
    assert tiles == ["/fr/glossaire/", "/fr/attention-aux-fraudes/"]
    assert [a["href"] for a in main.select('a[href="/fr/contact/"]')] == ["/fr/contact/"]
    assert main.select_one('aside.faq-guida .faq-aiuto a[href="/fr/contact/"]') is not None


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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the head stands without the frontispiece's wrapper (no band, no ground, its sheet not linked) — the same head
    head = main.select_one("header.page-header.vivere-testa__header")
    assert main.select(".fronte-wrap, [data-fronte]") == []
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: Le projet
    # draws no material recipe now (the incastro left) — its route sheet is its own rules alone
    "apps/pages/static/pages/css/projet.css": (["_projet.css"], ["pages/project.html"]),
    "apps/cms/static/cms/lessico.css": (
        ["_lessico-v2.css"],
        ["glossary/index.html", "glossary/term.html", "living/index.html"],
    ),
    # V5.20, citing V5.30 §7: the Italy + Morocco primitive under Réseau's closing band joins its route sheet, once.
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D,
    # «l'esploratore»): the flags left the page (no flag as decoration) and the primitive with them — the sheet is its
    # own partial alone (the same invariant: exactly its imports, linked by its page only)
    "apps/pages/static/pages/css/rete.css": (["_rete.css"], ["pages/network.html"]),
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


#: the pages of the list above that still open with the frontispiece (lane D's left it: FAQ, glossary, living, network,
#: fraud — tests/frontend/test_trust_pages_v532_d.py)
FRONTISPIECE_PAGES = ("/fr/agami/", "/fr/le-projet/")


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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the pages that no longer draw a frontispiece no longer link its sheet — their route sheet is the head's last
    # (the glossary's term page keeps its band and its sheet after the route sheet)
    after = ["pages/css/fronte.css"] if path == "/fr/glossaire/nulla_osta/" or path in FRONTISPIECE_PAGES else []
    assert links[at - 1] == shared and links[at + 1 :] == after, links
    routes = {route.split("/static/", 1)[1] for route in ROUTE_SHEETS}
    assert [link for link in links if link in routes] == [sheet], links


def test_no_family_class_shadows_a_chrome_class():
    """A page partial's block names are its own: «.targa» is the letterhead's reserved-space plate (the preserved
    navbar, V5.22 §9.8) — the AGAMI identification plate once took the name and wrapped the menu onto two rows."""
    chrome = (ROOT / "static" / "css" / "v5" / "chrome.css").read_text(encoding="utf-8")
    chrome_classes = set(re.findall(r"\.([a-z][a-z0-9_-]*)", re.sub(r"/\*.*?\*/", "", chrome, flags=re.S)))
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # one more partial held to the rule — the contact desk's (_contatto-v532.css)
    sheets = ["_projet.css", "_rete.css", "_contatto.css", "_contatto-v532.css", "_agami.css", "_frodi.css"]
    # the html state class a sheet reads (.rm: the preview's reduced motion) and shared components are not blocks
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the shared telephone isolate (base.css `.phone`, which the footer's and the nav sheet's channels read too) is read
    # by the desk's channels as `.email` is read by the fraud page's address — a shared component, not a block.
    # Stronger: a shared component is only ever read INSIDE a sheet's own block — no selector of the sheets opens on one
    shared = {"rm", "icon", "email", "link-arrow", "btn", "sez-disc", "sez-plate", "phone"}
    opening = re.compile(r"(?:\[[^\]]*\]\s*|:root(?::not\([^)]*\))*\s*|html\S*\s+|body\S*\s+)*\.([a-z][a-z0-9_-]*)")
    for name in sheets:
        css = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / name).read_text(encoding="utf-8")
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        own = set(re.findall(r"\.([a-z][a-z0-9_-]*)", stripped))
        blocks = {c.split("__")[0] for c in own}
        assert not (blocks & chrome_classes) - shared, (name, blocks & chrome_classes)
        for head in re.findall(r"(?:^|[{};])\s*([^{};@][^{};]*?)\s*\{", stripped):
            for selector in head.split(","):
                first = opening.match(selector.strip())
                assert not (first and first.group(1).split("__")[0] in shared), (name, selector.strip())
