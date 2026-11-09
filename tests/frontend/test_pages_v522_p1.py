"""
V5.22 lane P1 — Page Composition V2: journeys and spaces (SECTION_SYSTEM_V2 §3.3–§3.10, §9.4; label v522-p1-build).

What the recomposed pages promise, read in the rendered HTML and in the sheets (presentation is judged in headed
Chromium — QA/v522/p1/NOTES.md — and the behaviour in the browser module test_pages_browser_v522_p1.py):

* each page links ONE page sheet of its own (the family's sheet bundled with the V2 patterns it composes): requests
  unchanged; each sheet inside its recorded ceiling, each page's total inside its type's (§7.1); main.css untouched;
* the chapter device has left the bodies (§0 item 3): every body section is a V2 section (`.sez`, its pattern named),
  except the preserved form (V5.22 §24);
* locked copy is re-composed, never retyped (§1 rule 6): the pilot's eight labels in their order, the «Comment ça
  marche» sentence, the recipients sentence, the recruitment answer, the training's body — each element's text is the
  registry's, character for character;
* the legally required notices stay whole and visible (§1 rule 7): the pilot's status, the how-it-works caveat, the
  anti-fraud text, «Qui décide ?», the Formation notice, the orientation caution, the training-in-origin notice;
* the registry's glyphs (§4.10): the pilot's stations, the companies' moments, the recipients' seats, a sheet's
  milestones, the diplomas' stations — never a check but the diplomas' seal;
* the page's one primary action, the live «who can help me» line where the page offers an action;
* a station whose sheet is not live is never a link; Italy Legal Entry™ stands outside the authorities' arc.

V5.24, lane PUB1 — the material pass (FINAL_DELIVERY_V2 §3.5, R3, R4 b, R5; BACKGROUND_MATERIAL_V2 §3.2–§3.4, §4.2; V5.20's
strict rule, each change cited where it stands): the eight route sheets' ceilings are RECORDED at the family's §7.1 letter
(11 264 — a recording, not a raise of any page total: the page totals stay the letter, 56 320); a band's ground may be
«pietra» (dressed stone — one kind with stone for the adjacency rule, and the two never touch); the pilot's route and a
sheet's steps are bands (content-bound, R5); every protection stands on pietra; and the new assertions below read the
material, the seams (the three raccordi as the first child of the band each enters), the verbs, the roles and the
grounds' sequence on every page type.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings

from cms import locked_content
from core import icons

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
DIST = ROOT / "static" / "css" / "dist"

#: page → its page sheet (one per page: the family's sheet and the V2 partials it composes, bundled)
SHEETS = {
    "/fr/projet-pilote/": "ecosystem/pilot.css",
    "/fr/entreprises/": "ecosystem/companies.css",
    "/fr/institutions/": "ecosystem/institutions.css",
    "/fr/universites-et-formation/": "ecosystem/universities.css",
    "/fr/parcours/": "pathways/index.css",
    "/fr/parcours/salaried_work/": "pathways/sheet.css",
    "/fr/formation/": "pathways/training.css",
    "/fr/diplomes-et-titres/": "pathways/diplomas.css",
}
#: the page sheets' ceilings (gzip -9): the family sheets keep §7.1's 11 264, and — V5.24, FINAL_DELIVERY_V2 R4 b (V5.24
#: §7–§10; V5.20 strict rule) — the eight route sheets' ceilings, set by lane P1 on its own measures, are RECORDED at the
#: family's §7.1 letter 11 264 so the material partial (v5/_materia.css, ≈ 790 B) can enter them: a recording cited to
#: FINAL_DELIVERY_V2.md, never a raise of a page total (PAGE_TOTAL below stays the letter). Measured at the lane's build
#: (gzip -9 of the dist): index 10 655 · sheet 10 147 · training 9 257 · diplomas 9 388 · pilot 9 851 · companies 8 625 ·
#: institutions 8 724 · universities 7 519 — CLOSING ratchets each to its measure (§3.9 c).
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
CEILINGS = {
    "ecosystem/ecosystem.css": 4_719,
    "pathways/pathways.css": 4_423,
    "ecosystem/pilot.css": 9_701,
    "ecosystem/companies.css": 8_480,
    # V5.30 §7 (stream A; V5.20, re-recorded at the measure — NOTES docs/design-v5/QA/v530/art/NOTES.md §6): the generalised
    # «intesa» (a stronger presence, the panel variant and the night modifier in the primitive), the bookend's rules paid
    "ecosystem/institutions.css": 9_041,
    "ecosystem/universities.css": 7_366,
    "pathways/index.css": 10_452,
    "pathways/sheet.css": 10_007,
    "pathways/training.css": 9_079,
    "pathways/diplomas.css": 9_225,
}
#: §7.1: landings, interior and pathways pages ≤ 56 320 B, all the sheets a page links on a desktop (the portico's
#: included, the preserved form sheets excepted — test_frontispiece_v515_c.py's rule)
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
PAGE_TOTAL = 55_067
FORM_SHEETS = {"css/dist/core/forms.css", "css/dist/core/steps.css", "css/dist/core/glyph.css"}
STYLESHEET = re.compile(r'<link rel="stylesheet" href="/static/(css/dist/[^"?]+\.css)[^"]*"')
ICON = re.compile(r'<use href="[^"#]*#icon-([a-z0-9-]+)"')


def _gz(relative: str) -> int:
    return len(gzip.compress((ROOT / "static" / relative).read_bytes(), 9))


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _text(node) -> str:
    return " ".join(node.get_text("").split())


@pytest.fixture
def get(client, seeded, phase3_open, legal_published):
    def fetch(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return fetch


# ---- the sheets: one a page, inside their ceilings ------------------------------------------------------------------


def test_every_page_sheet_is_a_plain_import_list_that_starts_from_its_family_sheet():
    for sheet in SHEETS.values():
        family, name = sheet.split("/")
        source = (ROOT / "apps" / family / "static" / family / name).read_text(encoding="utf-8")
        body = re.sub(r"/\*.*?\*/", "", source, flags=re.S).strip()
        imports = re.findall(r'@import url\("([^"]+)"\);', body)
        assert re.sub(r'@import url\("[^"]+"\);', "", body).strip() == "", (sheet, "nothing but imports")
        assert imports[0] == f"{family}.css", (sheet, "the family's sheet first")
        assert imports[1] == "../css/v5/_sezioni.css", (sheet, "then the shell of the V2 sections")
        assert all(i.startswith("../css/v5/_") or i.startswith("_") for i in imports[1:]), sheet


def test_the_sheets_stay_inside_their_ceilings_and_main_css_never_rises():
    assert _gz("css/dist/main.css") <= 32_105
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    for partial in ("_sezioni.css", "_sec-", "_spazi-v2", "_persone-v2"):
        assert partial not in main
    for sheet, ceiling in CEILINGS.items():
        assert _gz(f"css/dist/{sheet}") <= ceiling, (sheet, _gz(f"css/dist/{sheet}"), ceiling)


@pytest.mark.parametrize("path", list(SHEETS))
def test_each_page_links_its_own_sheet_once_and_stays_inside_its_total(get, path):
    html = get(path)
    sheets = STYLESHEET.findall(html)
    assert sheets.count(f"css/dist/{SHEETS[path]}") == 1, (path, sheets)
    family = {"ecosystem/ecosystem.css", "pathways/pathways.css"} & {s.removeprefix("css/dist/") for s in sheets}
    assert not family, (path, "the family's sheet arrives inside the page's sheet, never as a second request")
    total = sum(_gz(sheet) for sheet in set(sheets) if sheet not in FORM_SHEETS)
    assert total <= PAGE_TOTAL, (path, total)


@pytest.mark.parametrize(
    "path",
    [
        "/fr/entreprises/recueil-des-besoins/",
        "/fr/collaboration/institutions/",
        "/fr/collaboration/universites-formation/",
    ],
)
def test_the_form_pages_add_the_band_s_sheet_and_nothing_else(get, path):
    sheets = STYLESHEET.findall(get(path))
    assert "css/dist/pages/css/fronte.css" in sheets and "css/dist/cms/lettura.css" in sheets, sheets
    # V5.29 §15–§17 (the owner's order of 6 Nov 2026: the institutions' collaboration page on the Italy + Morocco
    # ground; FINAL_DELIVERY_V2 §3.5; V5.20 — the same invariant, named exactly): an institution's proposal adds that
    # ground's own sheet, ecosystem/intesa.css (871 B gzip -9 since V5.30's generalised primitive), once — never a space's page sheet; the others nothing
    intesa = ["css/dist/ecosystem/intesa.css"] if path == "/fr/collaboration/institutions/" else []
    assert [s for s in sheets if "/ecosystem/" in s or "/pathways/" in s] == intesa, sheets


# ---- the bodies: V2 sections, the chapter device gone ---------------------------------------------------------------


@pytest.mark.parametrize("path", list(SHEETS))
def test_the_chapter_device_has_left_the_body(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    # the preserved form keeps its chapter and its sticky side (V5.22 §24, §3.6 EN-3): nothing else is a chapter
    for form in soup.select(".chapter.ecosystem-form"):
        form.decompose()
    assert not soup.select(".chapter, .chapter__head, .chapter__mark"), path
    sections = soup.select(".sez[data-sec]")
    assert sections, path
    for section in sections:
        # V5.24 (BACKGROUND_MATERIAL_V2 §3.1; FINAL_DELIVERY_V2 R3): «pietra», the dressed stone, is the sixth ground kind
        assert section.get("data-ground") in {"paper", "stone", "pietra", "brand", "night", "photo"}, (
            path,
            section.get("class"),
        )
        assert section.get("data-rhythm") in {"strip", "band", "moment"}, (path, section.get("class"))
    assert len([s for s in sections if s.get("data-rhythm") == "moment"]) <= 1, (path, "one moment at most (§1 rule 5)")


@pytest.mark.parametrize("path", list(SHEETS))
def test_one_primary_action_and_the_registry_s_glyphs_only(get, path):
    main = _main(get(path))
    assert len(re.findall(r'class="btn btn--primary\b', main)) <= 1, path
    names = ICON.findall(main)
    assert set(names) <= set(icons.SYMBOLS), (path, set(names) - set(icons.SYMBOLS))
    assert "ile-steps" not in names and "list-checks" not in names, path
    checks = {n for n in names if "check" in n}
    allowed = {"badge-check"} if "diplomes" in path else set()
    assert checks <= allowed, (path, checks)


# ---- Projet pilote (§3.3) -------------------------------------------------------------------------------------------


def test_the_pilot_s_seal_heads_its_eight_stations_and_the_status_plate_ends_them(get):
    soup = BeautifulSoup(_main(get("/fr/projet-pilote/")), "html.parser")
    # §3.3 PP-1: the T1 `ile-pilota` seal beside the section's title; the eight stations each draw their concept tile
    # (icons.PILOT_STATION — a register's glyphs all or none, §4.10), never the seal in a station's seat
    head = soup.select_one(".pilota-rotta__capo")
    assert head.select_one('.sigillo.sigillo--body[data-mark="ile-pilota"]') and head.select_one("h2#sequence-header")
    # §3.3's map (QA_ROUND1 M2): the route is its own trigger, so a desktop's first screen — which holds the section's top
    # — still sees the line drawn when the route is in view. V5.24 (FINAL_DELIVERY_V2 R5, §3.5; BACKGROUND_MATERIAL_V2
    # §3.3; V5.20 strict rule): the route stands on the page's one wash as a BAND (a two-row route is content-bound, no
    # moment — recorded), the doors on paper — night → brand → paper → stone, no two grounds of one kind touching
    assert soup.select_one('section#sequence.sez[data-ground="brand"][data-rhythm="band"]')
    assert soup.select_one('section#participer.sez[data-ground="paper"][data-rhythm="band"]')
    route = soup.select_one('[data-diagram="pilot-sequence"]')
    assert route.get("data-sec") == "linea", route.attrs
    stations = route.select("ol.linea.linea--large > li")
    labels = [_text(li.select_one(".linea__label")) for li in stations]
    assert labels[:8] == locked_content.get("p3.pilot.sequence", "fr")[0], labels
    assert not route.select(".sigillo"), "the seal stands in the head, never in a station's seat"
    tiles = [ICON.findall(str(li.select_one(".linea__segno"))) for li in stations[:8]]
    assert [t[0] for t in tiles] == list(icons.PILOT_STATION), tiles
    # the mandatory notice: the route's terminal plate, directly after the stations, whole, never collapsible
    after = str(route).split("</ol>", 1)[1]
    assert 'data-notice="pilot-not-authorised"' in after and "<details" not in after
    notice = route.select_one('[data-notice="pilot-not-authorised"] .notice')
    assert "notice--warning" in notice["class"]
    assert "ne signifie pas qu’un canal d’entrée soit déjà autorisé ou opérationnel" in _text(notice)


def test_the_pilot_s_two_doors_carry_their_halves_and_the_locked_calls(get):
    soup = BeautifulSoup(_main(get("/fr/projet-pilote/")), "html.parser")
    doors = soup.select(".pilota-porte__coppia > .porta-pilota")
    assert len(doors) == 2
    company, institution = doors
    assert company["data-audience"] == "company" and "on-inverse" in company["class"]
    assert _text(company.select_one(".porta-pilota__testo")) == "Entreprises : signalez vos besoins professionnels."
    assert _text(institution.select_one(".porta-pilota__testo")) == "Institutions : proposez une collaboration."
    primary = company.select_one("a.btn--primary")
    assert _text(primary) == locked_content.text("p2.forum.registration.button_secondary_pilot", "fr")
    secondary = institution.select_one("a.btn--secondary")
    assert _text(secondary) == locked_content.text("p3.institutions.button", "fr")
    assert soup.select_one("#participer .aiuto a.email"), "who can help me, under both doors"
    # the two doors stand on one sill, the help line after them (§3.3 PP-2, QA_ROUND1 M2 a–b)
    assert soup.select_one("#participer ul.pilota-porte__coppia + p.aiuto")


# ---- Parcours (§3.4) ------------------------------------------------------------------------------------------------


def test_the_route_board_holds_the_eight_pathways_on_their_family_lanes(get):
    from pathways import services

    soup = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    board = soup.select_one(".percorsi-tracciato")
    lanes = board.select(".tracciato__corsia")
    assert [lane["data-lane"] for lane in lanes] == ["work", "study", "family", "other"]
    stations = board.select(".tracciato__stazione")
    assert sorted(s.select_one(".tracciato__num").get_text() for s in stations) == [f"0{i}" for i in range(1, 9)]
    entries = {e["key"]: e for e in locked_content.get("p3.persons.pathways", "fr")[0]}
    for station in stations:
        key = station["data-pathway"]
        assert _text(station.select_one(".tracciato__titolo")) == entries[key]["title"]
        assert _text(station.select_one(".tracciato__riga")) == entries[key]["description"]
        assert services.FAMILY_OF[key] == station["data-family"]
    # every lane its family frame, black and white at rest («select»), drawn at the width its sizes states — round 2
    # (QA_ROUND2 m9; V5.20 strict rule, SECTION_SYSTEM_V2 §3.4: the two one-station lanes share the board's last row,
    # «the fork», so the pair's frames are drawn at the pair's widths): each frame states its own lane's width, the
    # three-station lanes the head's, the pair the fork's (the browser test measures every one)
    frames = board.select('.tracciato__testa figure[data-grade="select"]')
    assert len(frames) == 4
    stated = {lane["data-lane"]: lane.select_one(".tracciato__testa img")["sizes"] for lane in lanes}
    assert stated == {
        "work": services.FAMILY_SIZES_V2,
        "study": services.FAMILY_SIZES_V2,
        "family": services.FAMILY_SIZES_FORK_START,
        "other": services.FAMILY_SIZES_FORK_END,
    }
    assert [lane.get("class") for lane in lanes][2:] == [
        ["tracciato__corsia", "tracciato__corsia--start"],
        ["tracciato__corsia", "tracciato__corsia--end"],
    ]
    # the choice: a native radio group named by its legend, the polite count line, the origin's secondary link. Round 2
    # (QA_ROUND2 M1; V5.20 strict rule — SECTION_SYSTEM_V2 §0.1 and §2 B «nothing leaves the layout», the old fold
    # gone): the board is the group (a fieldset, its legend first), «Tous» in its chip and each family's radio at its
    # own lane's head, its chip its label — a choice brings its lane, by the browser's own focus; the chips and the
    # count are one bar (QA_ROUND1 M3)
    assert board.name == "fieldset" and board.contents and board.find(True).name == "legend"
    assert board.find(True).get_text(strip=True) == "Familles de parcours"
    radios = board.select('input[type="radio"][name="pathway-family"]')
    assert [radio["value"] for radio in radios] == ["all", "work", "study", "family", "other"]
    assert radios[0].find_parent("label", class_="tracciato__chip") and radios[0].has_attr("checked")
    for lane, radio in zip(lanes, radios[1:], strict=True):
        assert lane.find(True) is radio and radio["id"] == f"family-{lane['data-lane']}"
        assert "percorsi-via" in radio["class"]
    bar = board.select_one(".percorsi-scelta")
    chips = bar.select(".tracciato__scelta > label.tracciato__chip")
    assert [chip.get("for") for chip in chips] == [None, "family-work", "family-study", "family-family", "family-other"]
    assert [chip.get_text(strip=True) for chip in chips[1:]] == [
        str(services.FAMILY_LABELS[k]) for k in services.FAMILY_LABELS
    ]
    assert bar.select_one('.tracciato__conto[aria-live="polite"][role="status"]')
    # the prescribed order is said, not only drawn (QA_ROUND1 m9): each numeral is read with its station's title
    assert not board.select(".tracciato__num[aria-hidden]")
    assert not board.select(".btn--primary"), "the questionnaire's primary stays in the head"


def test_a_station_whose_sheet_is_not_live_is_never_a_link(client, seeded, phase3_open, legal_published):
    from pathways.models import Pathway

    Pathway.objects.filter(key="scientific_research").update(status="draft")
    soup = BeautifulSoup(_main(client.get("/fr/parcours/").content.decode("utf-8")), "html.parser")
    station = soup.select_one('.tracciato__stazione[data-pathway="scientific_research"]')
    assert station.select_one(".tracciato__carta--attesa") and not station.select("a")
    assert soup.select_one('.tracciato__stazione[data-pathway="salaried_work"] a.tracciato__carta')


def test_how_it_works_reads_back_whole_on_its_four_plates_and_its_caveat_is_never_small_print(get):
    text = locked_content.text("p3.persons.how_it_works", "fr")
    soup = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    block = soup.select_one('[data-locked="p3.persons.how_it_works"]')
    assert " ".join(block.get_text(" ").split()) == text
    plates = block.select("ol.come__tappe > li.come__tappa")
    assert len(plates) == 4
    assert [ICON.findall(str(p.select_one(".come__nodo")))[0] for p in plates] == list(icons.HOW_STEP)
    assert plates[0].select_one('a[href="/fr/orientation/"]') and plates[2].select_one('a[href="/fr/formation/"]')
    assert not plates[1].select("a") and not plates[3].select("a")
    assert all(p.select_one(".come__testo .visually-hidden") for p in plates[:3]), "the arrows kept as text"
    caveat = block.select_one(".come__avvertenza")
    assert _text(caveat) == text.rsplit(". ", 1)[1]


@pytest.mark.parametrize(
    "path", ["/fr/parcours/", "/fr/parcours/salaried_work/", "/fr/formation/", "/fr/diplomes-et-titres/"]
)
def test_the_anti_fraud_text_stands_whole_in_its_own_band(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    # V5.24 (BACKGROUND_MATERIAL_V2 §3.1 «pietra»; FINAL_DELIVERY_V2 §3.5; V5.20 strict rule): every protection stands on
    # the dressed stone — the grid on the far side, the shield bookend, the sill (the library's recipe)
    plate = soup.select_one('.sez[data-ground="pietra"] aside.protezione[data-callout="antifraud"]')
    assert plate, path
    body = plate.select_one('p[data-locked="p3.antifraud.body"]')
    assert body.get_text("") == locked_content.text("p3.antifraud.body", "fr")
    assert plate.select_one('.sigillo[data-mark="ile-scudo"]')
    assert "notice--warning" not in plate.get("class", []), "ink, never the alarm's amber (§0.1)"


# ---- the pathway sheets (§3.5) --------------------------------------------------------------------------------------


def test_a_sheet_s_steps_run_on_the_thread_beside_the_page_s_rail(get):
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    section = soup.select_one("section#etapes.sez[data-sec='filo']")
    milestones = section.select("ol.filo__linea > li.filo__tappa")
    assert len(milestones) == 5
    assert [ICON.findall(str(m.select_one(".filo__nodo")))[0] for m in milestones] == list(icons.SHEET_STEP)
    # V5.22 (SECTION_SYSTEM_V2 §3.5 PS-1: the rail «tracks Étapes → Autorités → Avertissements → Ressources →
    # Orientation»; QA_ROUND1 M4; V5.20 strict rule): the rail is the page's, not the first part's — one sticky index
    # whose span holds EVERY part it names, so it is in reach wherever the reader is (it was sticky inside «Étapes» only)
    body = soup.select_one(".scheda-corpo")
    rail = body.select_one(":scope > nav.filo__rail.scheda-rail[data-sec-js~='spia']")
    assert rail.get("aria-labelledby") and rail.select_one("#" + rail["aria-labelledby"])
    anchors = [a["href"] for a in rail.select("a.filo__voce")]
    assert anchors[0] == "#etapes" and "#orientation" in anchors
    for anchor in anchors:
        assert body.select_one(f":scope > section{anchor}"), anchor
    assert not section.select("nav"), "the first part no longer holds the page's index"
    head = soup.select_one("header.ingresso nav.sommaire")
    assert head, "below 64 rem the «Sommaire» stays in the head (the rail is a wide screen's)"


def test_italy_legal_entry_stands_outside_the_authorities_arc(get):
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    section = soup.select_one('section#autorites.sez[data-ground="night"]')
    seats = section.select("ol.decide__arco > li.decide__seggio")
    assert len(seats) == 4
    assert all(ICON.findall(str(s))[0] == icons.AUTHORITY_SEAT for s in seats)
    ile = section.select_one(".decide__ile")
    assert ile and not ile.find_parent("ol"), "the node of ILE is outside the arc"
    assert "n’intervient pas auprès des autorités et ne délivre aucune autorisation" in _text(ile)


def test_a_sheet_s_terms_open_their_locked_definitions_in_place(get):
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    disclosures = soup.select("#ressources details.indice__dettaglio[name='termini']")
    assert len(disclosures) >= 3
    for details in disclosures:
        term = _text(details.select_one("summary"))
        entry = next(t for t in terms.values() if t["term"] == term)
        assert _text(details.select_one(".indice__corpo p")) == entry["definition"]
        assert details.select_one("summary")["lang"] == "it"
        assert details.select_one(f'a[href$="/glossaire/{entry["key"]}/"]')


@pytest.mark.parametrize("path", ["/fr/parcours/salaried_work/", "/fr/formation/", "/fr/diplomes-et-titres/"])
def test_the_compass_closes_on_the_questionnaire_with_its_caution(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    band = soup.select_one('section#orientation.sez[data-ground="brand"]')
    # V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule): the plate is the sentence and its action, no compass drawn
    assert not band.select(".boussole__ago, svg.boussole")
    assert "Les décisions relèvent des autorités compétentes." in _text(band.select_one(".boussole__testo"))
    assert band.select_one('a.btn--primary[href="/fr/orientation/"]')
    assert band.select_one(".sez-annotation a.email"), "who can help me, beside the action"


# ---- Entreprises (§3.6) ---------------------------------------------------------------------------------------------


def test_the_companies_quote_opens_the_flow_and_the_answer_is_split_on_its_own_colon(get):
    soup = BeautifulSoup(_main(get("/fr/entreprises/")), "html.parser")
    quote = soup.select_one("section#demarche blockquote.imprese-citazione p")
    assert _text(quote) == locked_content.text("p1.companies.quote", "fr")
    # V5.30 Fast Visual Variety Correction §7 ENTREPRISES, «process panels» (V5.20 strict rule; no measured curve, no module)
    flow = soup.select_one("section#demarche .flusso")
    assert not flow.has_attr("data-sec-js") and not soup.select("#demarche [data-flow], #demarche [data-flow-node]")
    nodes = flow.select("li.flusso__tappa .flusso__nodo")
    assert [ICON.findall(str(n))[0] for n in nodes] == list(icons.COMPANY_MOMENT)
    band = soup.select_one(".sez--panorama")
    assert band.select_one('figure[data-slot="companies.territory"]')
    answer = soup.select_one("section#transparence p.imprese-confine__risposta[data-faq]")
    faq = next(e for e in locked_content.get("p3.faq.items", "fr")[0] if e["key"] == "faq_recruitment_agency")
    assert answer.get_text("") == faq["answer"]
    assert [s["class"][-1] for s in answer.select("span")] == ["giu-1", "giu-2", "giu-3"]
    assert _text(answer.select_one(".giu-1")) == "Non."
    assert _text(soup.select_one("#transparence-header")) == faq["question"]
    assert not soup.select("#transparence svg.notice__icon"), "no mark reads as a verdict"
    assert soup.select_one("section#formulaire form"), "the form is preserved"


# ---- Institutions (§3.7) --------------------------------------------------------------------------------------------


def test_the_hemicycle_holds_the_locked_sentence_whole_and_its_six_seats(get):
    soup = BeautifulSoup(_main(get("/fr/institutions/")), "html.parser")
    # V5.30 Fast Visual Variety Correction §7 INSTITUTIONS, «premium split», «Do not make every institutional relationship an
    # arc» (V5.20 strict rule): the chamber's photograph beside the night plate, the same six seats in a row of tiles
    section = soup.select_one('section#destinataires.sez[data-ground="night"]')
    assert section.select_one("h2.visually-hidden#destinataires-title")
    sentence = section.select_one("p.emiciclo__frase")
    assert sentence.get_text("") == locked_content.text("p3.institutions.recipients", "fr")
    # V5.20 strict rule, cited (v522-s2): the six phrases pair with the six seats through the pattern's own attribute —
    # DL54-182 item 10 b; Lume's L3 attribute is reserved for the fragment containers loader.js seats (DS 2026 §12,
    # W1-D: «no server-rendered region seats», tests/frontend/test_loader_rules.py) — the same pairing, and now none of
    # the section's elements carries the seat's attribute (stronger)
    assert len(sentence.select("[data-seggio]")) == 6
    assert [seat["data-seggio"] for seat in section.select("ol.emiciclo__seggi > li")] == [str(n) for n in range(1, 7)]
    assert not section.select("[data-seat]")
    seats = section.select("ol.emiciclo__seggi[aria-hidden='true'] > li")
    assert [ICON.findall(str(s))[0] for s in seats] == list(icons.RECIPIENT_SEAT)
    assert section.select_one('figure[data-slot="institutions.chamber"][data-grade="bw-scroll"]')
    assert section.select_one(".aiuto a.email") and not section.select(".btn--primary")


# ---- Universités (§3.8) ---------------------------------------------------------------------------------------------


def test_the_learning_route_keeps_its_stations_and_its_frame_and_ends_on_no_arch(get):
    from ecosystem import services

    entries = {e["key"]: e for e in locked_content.get("p3.persons.pathways", "fr")[0]}
    soup = BeautifulSoup(_main(get("/fr/universites-et-formation/")), "html.parser")
    route = soup.select_one(".filiera")
    stations = route.select("ol.filiera__stazioni > li")
    titles = [_text(s.select_one(".filiera__titolo")) for s in stations]
    assert titles == [
        entries["training_in_origin_country"]["title"],
        entries["study_and_training_in_italy"]["title"],
        locked_content.text("p3.training_after.title", "fr"),
    ]
    assert _text(stations[1].select_one(".filiera__ramo-titolo")) == entries["scientific_research"]["title"]
    # V5.30 Fast Visual Variety Correction §4 (V5.20 strict rule): arches are signature only, this is not one of the moments
    assert not route.select(".filiera__arrivo, .filiera__arrivo svg")
    frame = route.select_one('figure[data-slot="universities.exchange"] img')
    assert frame["sizes"] == services.DESTINATION_SIZES
    # the moment names its own subject (QA_ROUND1 m11: it kept the closing bands' «Pour aller plus loin»)
    assert _text(soup.select_one("#filiere #related-header")) == "Formation et mobilité régulière"
    assert route.select_one(".aiuto a.email")


# ---- Formation (§3.9) -----------------------------------------------------------------------------------------------


def test_the_two_times_cross_one_line_and_the_notice_stays_beside_its_frame(get):
    from pathways import services

    soup = BeautifulSoup(_main(get("/fr/formation/")), "html.parser")
    times = soup.select("ol.traversata > li.traversata__tempo")
    assert [t["id"] for t in times] == ["avant-le-depart", "apres-l-arrivee"]
    assert [_text(t.select_one(".traversata__kicker")) for t in times] == ["Premier temps", "Second temps"]
    assert [ICON.findall(str(t.select_one(".traversata__nodo")))[0] for t in times] == ["earth", "ile-arch"]
    note = times[0].select_one('.traversata__media [data-notice="training-before"]')
    assert "aucune attestation n’a valeur d’approbation administrative" in _text(note)
    body = times[1].select_one('p[data-locked="p3.training_after.body"]')
    assert body.get_text("") == locked_content.text("p3.training_after.body", "fr")
    assert body.select_one(".ls-1").get_text("") == "L’accompagnement ne s’arrête pas à l’entrée en Italie. "
    assert times[0].select_one('figure[data-slot="training.before"] img')["sizes"] == services.TRAVERSATA_BEFORE_SIZES
    assert times[1].select_one('figure[data-slot="training.after"] img')["sizes"] == services.TRAVERSATA_AFTER_SIZES


# ---- Diplômes (§3.10) -----------------------------------------------------------------------------------------------


def test_the_dossier_opens_its_locked_definitions_one_at_a_time_beside_who_decides(get):
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    soup = BeautifulSoup(_main(get("/fr/diplomes-et-titres/")), "html.parser")
    stations = soup.select("ol.dossier > li.dossier__tappa")
    assert len(stations) == 5 and all("dossier__tappa--attesa" in s["class"] for s in stations)
    # the status in words, never by its dashed ring alone (§3.10 D1): the caption under the stations, a catalogue msgid
    assert _text(soup.select_one(".diplomi-dossier .dossier__didascalia")) == "En attente de vérification"
    assert [ICON.findall(str(s.select_one(".dossier__nodo")))[0] for s in stations] == list(icons.DIPLOMA_STEP)
    assert not stations[0].select("details") and not stations[1].select("details"), "nothing invented"
    opened = soup.select("ol.dossier details[open]")
    assert len(opened) == 1 and opened[0].find_parent("li")["id"] == "etape-legalisation"
    for slug, station in (("legalizzazione_apostille", 2), ("dichiarazione_di_valore", 3), ("questura_prefettura", 4)):
        details = stations[station].select_one("details[name='dossier']")
        assert _text(details.select_one(".dossier__definizione")) == terms[slug]["definition"]
    aside = soup.select_one("aside#qui-decide")
    assert _text(aside.select_one("h2")) == "Qui décide ?"
    assert "relèvent exclusivement des autorités et organismes compétents" in _text(aside)


# ---- the form pages' heads (§3.6 EN-H, §3.7 IN-H) -------------------------------------------------------------------


def test_the_form_pages_open_on_their_space_s_compact_band_and_keep_their_form(get):
    needs = BeautifulSoup(_main(get("/fr/entreprises/recueil-des-besoins/")), "html.parser")
    head = needs.select_one('header.ingresso[data-fronte="economic"][data-compact]')
    assert head.select_one('.sigillo[data-mark="ile-impresa"]') and head.select_one("h1")
    assert _text(head.select_one(".ingresso__lead")) == locked_content.text("p1.companies.intro", "fr")
    assert needs.select_one("section#formulaire form")
    collab = BeautifulSoup(_main(get("/fr/collaboration/institutions/")), "html.parser")
    head = collab.select_one('header.ingresso[data-fronte="civic"][data-compact]')
    assert head.select_one('.sigillo[data-mark="ile-istituzione"]')
    note = head.select_one('.ingresso__aside [data-annotation="recipients"]')
    # V5.30 Fast Visual Variety Correction §7 INSTITUTIONS (V5.20 strict rule): the small hemicycle is gone
    assert not note.select("svg")
    assert _text(note.select_one("p")) == locked_content.text("p3.institutions.recipients", "fr")
    # QA_ROUND2 M2 (§3.7 IN-H, §4.1): one annotation — its words an annotation's secondary text, never a second lead
    row = note.select_one(".meta-row__item")
    assert [child.name for child in row.find_all(True, recursive=False)] == ["p"]
    assert "ingresso__lead" not in row.p["class"]
    assert collab.select_one("section#formulaire")
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the introduction and the
    # recipients are compositional (C-UI) — in Arabic their provisional renderings, never a French box
    from cms import locked_renderings

    arabic = BeautifulSoup(_main(get("/ar/collaboration/institutions/")), "html.parser")
    lead = arabic.select_one("header.ingresso p.ingresso__lead")
    assert lead.get("lang") in (None, "ar") and _text(lead) == locked_renderings.rendering("p3.institutions.intro")
    note = arabic.select_one('[data-annotation="recipients"] p')
    assert note.get("lang") in (None, "ar") and _text(note) == locked_renderings.rendering("p3.institutions.recipients")
    uni = BeautifulSoup(_main(get("/fr/collaboration/universites-formation/")), "html.parser")
    assert uni.select_one('header.ingresso[data-fronte="learning"][data-compact] .sigillo[data-mark="ile-sapere"]')


# ---- the data the compositions draw: cuts that never retype -----------------------------------------------------------


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_the_doors_cut_the_team_sentence_on_its_own_full_stop(lang):
    from django.utils import translation

    from ecosystem import services

    with translation.override(lang):
        doors = services.pilot_doors()
        whole = str(
            services._("Entreprises : signalez vos besoins professionnels. Institutions : proposez une collaboration.")
        )
    assert "whole" not in doors, (lang, doors)
    assert f"{doors['company']} {doors['institution']}" == whole


def test_the_recipients_spans_rebuild_the_sentence():
    from ecosystem import services

    for lang in ("fr", "it", "en", "ar"):
        recipients = services.enumeration("p3.institutions.recipients", lang)
        html = str(services.recipients_sentence(recipients))
        assert re.sub(r"<[^>]+>", "", html).replace("&#x27;", "'").replace("&amp;", "&") == recipients.source.text
        # V5.20 strict rule, cited (v522-s2; DL54-182 item 10 b; DS 2026 §12): the pattern's own attribute, never L3's
        assert html.count("data-seggio=") == len(recipients.items) == 6 and "data-seat" not in html


# ---- V5.24 · the material pass (FINAL_DELIVERY_V2 §3.5, R3, R5; BACKGROUND_MATERIAL_V2 §3.1–§3.4, §4.2; lane PUB1) ------------

#: stone and pietra are ONE kind for the adjacency rule (R3): two neighbours never share a kind, so pietra never touches stone
GROUND_KIND = {"pietra": "stone"}
#: the grounds the Director's table decides, head to foot (§3.5 «Budgets»; the probe of BACKGROUND_MATERIAL_V2 §5.3 re-run)
SEQUENCES = {
    "/fr/parcours/": ["paper", "paper", "brand", "paper", "pietra"],
    "/fr/parcours/salaried_work/": ["paper", "stone", "night", "pietra", "paper", "brand"],
    "/fr/projet-pilote/": ["night", "brand", "paper", "stone"],
    "/fr/entreprises/": ["paper", "stone", "paper", "stone", "paper", "stone"],
    "/fr/institutions/": ["paper", "night", "stone"],  # V5.30 VARIETY §7: the split's plate, its photograph beside it
    "/fr/universites-et-formation/": ["paper", "brand"],
    "/fr/formation/": ["paper", "paper", "pietra", "paper", "brand"],
    "/fr/diplomes-et-titres/": ["paper", "paper", "pietra", "paper", "brand"],
}
#: the route sheets that draw a recipe import the material partial; the two that draw none do not (a page carries only what
#: it draws — Entreprises' and Universités' changes are grounds and a page rule, §3.5; PUB1 NOTES §4)
MATERIA_IMPORTS = {
    "pathways/index.css": True,
    "pathways/sheet.css": True,
    "pathways/training.css": True,
    "pathways/diplomas.css": True,
    "ecosystem/pilot.css": True,
    "ecosystem/institutions.css": True,
    "ecosystem/companies.css": False,
    "ecosystem/universities.css": False,
}
PUB1_SHEETS = (
    "apps/pathways/static/pathways/_index.css",
    "apps/pathways/static/pathways/_sheet.css",
    "apps/pathways/static/pathways/_training.css",
    "apps/pathways/static/pathways/_diplomas.css",
    "apps/pathways/static/pathways/_persone-v2.css",
    "apps/ecosystem/static/ecosystem/_pilot.css",
    "apps/ecosystem/static/ecosystem/_companies.css",
    "apps/ecosystem/static/ecosystem/_institutions.css",
    "apps/ecosystem/static/ecosystem/_universities.css",
    "apps/ecosystem/static/ecosystem/_spazi-v2.css",
)


def _bands(soup) -> list[tuple[str, str, str]]:
    """The page's bands head to foot: the head (paper; night under data-tone="night"), every top-level V2 section by its
    ground, the preserved form chapter (stone) — (name, ground, rhythm)."""
    out = []
    for el in soup.find_all(["header", "section", "div"]):
        classes = el.get("class", [])
        if el.name == "header" and "ingresso" in classes:
            out.append(("head", "night" if el.get("data-tone") == "night" else "paper", "head"))
        elif "sez" in classes and el.get("data-ground") and not el.find_parent(class_="sez"):
            out.append((el.get("id") or " ".join(classes), el["data-ground"], el.get("data-rhythm", "")))
        elif "chapter--area" in classes:
            out.append((el.get("id") or "chapter", "stone", "chapter"))
    return out


@pytest.mark.parametrize("path", list(SEQUENCES))
def test_two_neighbouring_grounds_never_share_a_kind_and_pietra_never_touches_stone(get, path):
    """BACKGROUND_MATERIAL_V2 §3.3 and §4.2 as FINAL_DELIVERY_V2 §3.5 decides them: the grounds' sequence on every page type
    (head → first body section included), two neighbours never one kind — stone ≡ pietra —; the one touch accepted is the
    head's paper against a paper moment or strip standing on its own frames (§3.5 «*»; §5.3 KEEP)."""
    bands = _bands(BeautifulSoup(_main(get(path)), "html.parser"))
    assert [ground for _, ground, _ in bands] == SEQUENCES[path], (path, bands)
    for (a_name, a, a_rhythm), (b_name, b, b_rhythm) in zip(bands, bands[1:], strict=False):
        if a_rhythm == "head" and b_rhythm in {"moment", "strip"} and a == b == "paper":
            continue
        assert GROUND_KIND.get(a, a) != GROUND_KIND.get(b, b), (
            path,
            a_name,
            a,
            b_name,
            b,
            "two grounds of one kind touch",
        )


def test_the_material_and_the_seams_stand_where_the_director_placed_them(get):
    """BACKGROUND_MATERIAL_V2 §3.1–§3.4 as FINAL_DELIVERY_V2 §3.5 places them (R3's names): «carta viva» on the three grids
    (data-luce="origine"), «pietra» under every protection, the trunk's raccordo the FIRST CHILD of the band it enters (LIB
    NOTES §4 c: every .sez isolates — hung under the leaving band a line is painted over) rising into the head («risale»);
    V5.30 Fast Visual Variety Correction §5, §7 (V5.20 strict rule): only «Parcours» keeps a raccordo, the filo into the
    night, the dossier's and «la velatura» on the chamber's foot are gone —, the «Comment ça marche» plates' tiles that ink
    instead of settling (§3.4 PA-2), Formation's order
    (R5), the pilot's route on the wash, Entreprises' démarche on stone, the filiera on the wash; and the imports."""
    parcours = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    first = parcours.select_one("section.percorsi-famiglie").find(True)
    assert first.name == "span" and first["class"] == ["sez-raccordo", "sez-raccordo--risale"], first
    assert first["data-verb"] == "draw-y" and first["aria-hidden"] == "true"
    assert parcours.select_one('section.percorsi-spazio[data-ground="paper"][data-luce="origine"]')
    assert parcours.select_one('section.persone-protezione[data-ground="pietra"] aside.protezione')
    tiles = parcours.select(".come__tappa .come__nodo.sez-tile")
    assert len(tiles) == 4 and all(tile["data-verb"] == "ink" for tile in tiles), (
        "the plates' tiles ink, they never settle"
    )
    sheet = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    assert sheet.select_one('section#etapes[data-ground="stone"][data-rhythm="band"]'), (
        "R5: the steps are a band on stone"
    )
    assert not sheet.select("section#autorites .sez-raccordo"), "V5.30 VARIETY §5: no line into the night"
    assert sheet.select_one('section#avertissements[data-ground="pietra"]')
    assert not sheet.select('.sez[data-ground="stone"] + .sez[data-ground="stone"]')
    diplomas = BeautifulSoup(_main(get("/fr/diplomes-et-titres/")), "html.parser")
    protezione = diplomas.select_one("section.persone-protezione")
    assert protezione["data-ground"] == "pietra" and not protezione.select(".sez-raccordo"), "V5.30 VARIETY §5"
    assert diplomas.select_one('section.persone-spazio[data-ground="paper"][data-luce="origine"]')
    training = BeautifulSoup(_main(get("/fr/formation/")), "html.parser")
    assert [s.get("data-sec") for s in training.select(".sez[data-sec]")] == ["filo", "strato", "mosaico", "boussole"]
    assert training.select_one(
        'section.persone-protezione[data-ground="pietra"] + section.persone-spazio[data-luce="origine"]'
    )
    pilot = BeautifulSoup(_main(get("/fr/projet-pilote/")), "html.parser")
    assert pilot.select_one(
        'section#sequence[data-ground="brand"][data-rhythm="band"] [data-notice="pilot-not-authorised"]'
    )
    assert pilot.select_one('section#participer[data-ground="paper"]')
    companies = BeautifulSoup(_main(get("/fr/entreprises/")), "html.parser")
    assert companies.select_one('section#demarche[data-ground="stone"] blockquote.imprese-citazione')
    institutions = BeautifulSoup(_main(get("/fr/institutions/")), "html.parser")
    assert institutions.select_one('section#destinataires[data-ground="night"]:not([data-sfuma])'), "V5.30 VARIETY §7"
    assert not institutions.select("#destinataires .foto__credit"), "the credit chip left with lane PX (V5.24 §2)"
    universities = BeautifulSoup(_main(get("/fr/universites-et-formation/")), "html.parser")
    assert universities.select_one('section#filiere[data-ground="brand"][data-rhythm="moment"]')
    for sheet_name, imports in MATERIA_IMPORTS.items():
        family, name = sheet_name.split("/")
        source = (ROOT / "apps" / family / "static" / family / name).read_text(encoding="utf-8")
        assert ('@import url("../css/v5/_materia.css");' in source) is imports, sheet_name


def test_the_space_s_labels_kickers_and_numerals_carry_the_library_s_roles(get):
    """TYPOGRAPHY_V2 §4.2, §6 (F-3 the numeral role, F-4 the label role) through LIB NOTES §4: the label role by name
    (`t-label`) on the board's lane names, the two times' kickers, the filiera's kickers and the sheet's rail title; the
    numeral role (`t-numeral`) on the board's eight station numerals; no page sheet of the space seats the mono."""
    parcours = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    names = parcours.select(".tracciato__nome")
    assert len(names) == 4 and all("t-label" in n["class"] for n in names)
    nums = parcours.select(".tracciato__num")
    assert len(nums) == 8 and all("t-numeral" in n["class"] for n in nums)
    sheet = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    assert "t-label" in sheet.select_one(".scheda-rail__titolo")["class"]
    training = BeautifulSoup(_main(get("/fr/formation/")), "html.parser")
    assert [("t-label" in k["class"]) for k in training.select(".traversata__kicker")] == [True, True]
    universities = BeautifulSoup(_main(get("/fr/universites-et-formation/")), "html.parser")
    kickers = universities.select(".filiera__kicker")
    assert len(kickers) == 3 and all("t-label" in k["class"] for k in kickers)
    for relative in PUB1_SHEETS:
        source = re.sub(r"/\*.*?\*/", "", (ROOT / relative).read_text(encoding="utf-8"), flags=re.S)
        assert "var(--f-mono)" not in source and "font-size: clamp(" not in source, relative


def test_the_sheet_s_curated_figure_draws_its_byline_only_when_the_licence_asks_for_it():
    """IMAGERY_ATTRIBUTION D5 on lane PX's contract (FINAL_DELIVERY_V2 §3.2, §3.5; V5.24 §2): the figcaption's byline in
    templates/pathways/detail.html stands behind `attribution_required` — no stock credit reaches the product, and an
    attribution-required asset is never silently stripped of its byline."""
    source = (ROOT / "templates" / "pathways" / "detail.html").read_text(encoding="utf-8")
    assert "{% if pathway.hero_image.credit and pathway.hero_image.attribution_required %}" in source
    assert "{% if pathway.hero_image.credit %}" not in source
