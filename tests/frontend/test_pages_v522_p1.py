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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane C,
    # P2-2 of the integration review): round 2's ecosystem/proposta.css left with the university head's frame — the
    # invariant is back in its V5.29 form, stronger than round 2's: a university's proposal adds no sheet at all
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
    if path == "/fr/parcours/salaried_work/":
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
        # sheet's six bands became ONE paper body of chapters under its head (lane B; the decision
        # test_a_pathway_sheet_draws_no_band_one_paper_body_under_its_head holds) — no V2 band and no moment in it
        # (none ≤ one), its ground declared and of the library's kinds, every part a labelled chapter of the body, the
        # five the rail names among them
        assert not sections, path
        body = soup.select_one(".pathway-entrance ~ .scheda-corpo[data-ground='paper']")
        chapters = body.select(".scheda-capitoli > section.scheda-cap[id][aria-labelledby]")
        assert len(chapters) == len(body.select("section")), path
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the senior
        # integration review's correction round (P2-3) — the questionnaire's action closes the body inside the last
        # chapter, «Avertissements» («la chiusura», with the anti-fraud notice): four named chapters, no «Orientation»
        ids = [c["id"] for c in chapters]
        assert {"etapes", "autorites", "avertissements", "ressources"} <= set(ids) and "orientation" not in ids, ids
        assert ids[-1] == "avertissements" and chapters[-1].get("data-action") == "orientation", ids
        return
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
    # FINAL MICRO-PASS §5 A2/A3 (V5.20 strict rule: the T1 `ile-pilota` seal beside the title and the stations'
    # concept tiles left — numbers only for sequence): the head is its title alone, no seal; each of the eight stations
    # is its quiet sequence marker (21st.dev 26891) and its prescribed words — no tile, no glyph
    head = soup.select_one(".pilota-rotta__capo")
    assert head.select_one(".sigillo, [data-mark]") is None and head.select_one("h2#sequence-header")
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
    assert not route.select_one("ol.linea").select(".sigillo, .sez-tile, .linea__segno, svg"), "no seal, tile or glyph"
    assert all(len(li.select('span.linea__num[aria-hidden="true"]')) == 1 for li in stations[:8]), "one marker each"
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


def test_the_explorer_holds_the_eight_pathways_on_their_families(get):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the route
    # board (lanes, numbered stations, the families' radios and count line) gave way to «l'esploratore» (lane B,
    # pathways/_esplora.html — no numbering, no filter: eight rows need none). Each invariant on the new composition, the
    # same or stronger: the four families in their order, each its name and its rows; each prescribed pathway once; in a
    # family the rows keep the prescribed rank and the families stand in the rank of their first pathway (the order is
    # read in the document, no figure beside it); each row's title and line the registry's, character for character;
    # each row's family the services' tuple; every frame drawn at the width its `sizes` states; the families are the
    # navigation (each list named by its family's heading); no numeral, no tile; the questionnaire's primary stays in
    # the head
    from pathways import services

    soup = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    # the region is named by its heading, as the board's fieldset was by its legend
    assert soup.select_one('section.esplora-sez[aria-labelledby="pathways-title"] h2#pathways-title')
    explorer = soup.select_one("section.esplora-sez [data-esplora]")
    families = explorer.select(".esplora__famiglia")
    assert [f["data-family"] for f in families] == ["work", "study", "family", "other"]
    entries = locked_content.get("p3.persons.pathways", "fr")[0]
    rank = {entry["key"]: index for index, entry in enumerate(entries)}
    by_key = {entry["key"]: entry for entry in entries}
    assert sorted(row["data-pathway"] for row in explorer.select(".esplora__voce")) == sorted(rank)
    firsts = []
    for family in families:
        heading = family.select_one("h3.esplora__famiglia-nome")
        assert _text(heading) == str(services.FAMILY_LABELS[family["data-family"]])
        listing = family.select_one("ul.esplora__voci")
        assert listing["aria-labelledby"] == heading["id"]
        rows = listing.select(":scope > li.esplora__voce")
        ranks = [rank[row["data-pathway"]] for row in rows]
        assert ranks == sorted(ranks), family["data-family"]
        firsts.append(ranks[0])
        for row in rows:
            key = row["data-pathway"]
            assert _text(row.select_one(".esplora__titolo")) == by_key[key]["title"]
            assert _text(row.select_one(".esplora__riga")) == by_key[key]["description"]
            assert services.FAMILY_OF[key] == row["data-family"] == family["data-family"]
            assert not row.select(".tracciato__num, .t-numeral, .sez-tile"), key
    assert firsts == sorted(firsts)
    thumbs = explorer.select(".esplora__miniatura img")
    frames = explorer.select(".esplora__foto img")
    assert thumbs and frames
    assert all(img["sizes"] == services.FRAME_SIZES_THUMB for img in thumbs)
    assert all(img["sizes"] == services.FRAME_SIZES_PREVIEW for img in frames)
    assert not explorer.select(".btn--primary"), "the questionnaire's primary stays in the head"


def test_a_row_whose_sheet_is_not_live_is_never_a_link(client, seeded, phase3_open, legal_published):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the board's
    # station became the explorer's row (lane B) — the same invariant on the row AND on its preview: a pathway whose sheet
    # is not live is listed without any link (and without a word about it, V5.12 §8); a live one is its sheet's link
    from pathways.models import Pathway

    Pathway.objects.filter(key="scientific_research").update(status="draft")
    soup = BeautifulSoup(_main(client.get("/fr/parcours/").content.decode("utf-8")), "html.parser")
    row = soup.select_one('.esplora__voce[data-pathway="scientific_research"]')
    assert row.select_one(".esplora__link--attesa") and not row.select("a")
    assert not soup.select_one('[data-esplora-anteprima="scientific_research"]').select("a")
    assert soup.select_one(
        '.esplora__voce[data-pathway="salaried_work"] a.esplora__link[href="/fr/parcours/salaried_work/"]'
    )


def test_how_it_works_reads_back_whole_on_its_four_moments_and_its_caveat_is_never_small_print(get):
    text = locked_content.text("p3.persons.how_it_works", "fr")
    soup = BeautifulSoup(_main(get("/fr/parcours/")), "html.parser")
    block = soup.select_one('[data-locked="p3.persons.how_it_works"]')
    assert " ".join(block.get_text(" ").split()) == text
    plates = block.select("ol.come__tappe > li.come__tappa")
    assert len(plates) == 4
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
    # numbering»): the quiet sequence marker «1»–«4» gave way to one dot on the rail (lane B, _esplora.css) — each moment
    # its point and its words, the point decorative and EMPTY (stronger: no figure at all); still no tile, no node
    assert all(p.select_one('span.come__punto[aria-hidden="true"]') for p in plates)
    assert not any(_text(p.select_one(".come__punto")) for p in plates)
    assert not block.select(".come__nodo, .come__num, .sez-tile")
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: a pathway sheet is ONE paper body of chapters (lane B) —
    # there the plate stands whole as the first element of its own chapter, «Avertissements», which the sticky
    # navigation names; the space's three other pages keep it on pietra
    if path.startswith("/fr/parcours/") and path != "/fr/parcours/":
        plate = soup.select_one(
            'section#avertissements > .protezione__campo:first-child > aside.protezione[data-callout="antifraud"]'
        )
    else:
        plate = soup.select_one('.sez[data-ground="pietra"] aside.protezione[data-callout="antifraud"]')
    assert plate, path
    body = plate.select_one('p[data-locked="p3.antifraud.body"]')
    assert body.get_text("") == locked_content.text("p3.antifraud.body", "fr")
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the shield is drawn bare — no seal's seat —, once
    assert ICON.findall(str(plate.select_one(".protezione__sigillo"))) == ["ile-scudo"] and not plate.select(".sigillo")
    assert "notice--warning" not in plate.get("class", []), "ink, never the alarm's amber (§0.1)"


# ---- the pathway sheets (§3.5) --------------------------------------------------------------------------------------


def test_a_sheet_s_milestones_run_on_one_rail_beside_the_page_s_one_sticky_index(get):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (every pathway
    # page: «sticky local navigation … NOT one big timeline diagram»): «il filo» (numbered milestones on a stone band)
    # and the rail gave way to lane B's editorial sheet — the milestones on one rail without figures, and ONE local
    # navigation for every width (sticky beside the chapters from 64 rem, a sticky bar of anchors below it: its reach is
    # measured in test_pathways_browser_v532_b.py). The same invariants: five milestones in order, no tile and — stronger
    # — no figure; one labelled index for the page, whose span holds every part it names; the first part holds no index
    # of its own, and the head none either (its seat holds the photograph)
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    section = soup.select_one("section#etapes")
    milestones = section.select("ol.scheda-tappe > li.scheda-tappa")
    assert len(milestones) == 5
    assert _text(milestones[0].select_one("h3")) == "S’orienter"
    assert _text(milestones[-1].select_one("h3")) == "Accompagnement après l’arrivée"
    assert all(m.select_one('span.scheda-tappa__punto[aria-hidden="true"]') for m in milestones)
    assert not any(_text(m.select_one(".scheda-tappa__punto")) for m in milestones)
    assert not section.select(".filo__nodo, .filo__num, .t-numeral, .sez-tile")
    body = soup.select_one(".scheda-corpo")
    assert len(body.select("nav")) == 1
    rail = body.select_one("nav.scheda-nav[data-sec-js~='spia']")
    assert rail.get("aria-labelledby") and rail.select_one("#" + rail["aria-labelledby"])
    anchors = [a["href"] for a in rail.select("a.scheda-nav__voce")]
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
    # correction round (P2-3) — the index's last entry is the closing chapter, «Avertissements» (the anti-fraud notice
    # and the questionnaire's action, «la chiusura»); no «Orientation» entry, since no such chapter is drawn
    assert anchors[0] == "#etapes" and anchors[-1] == "#avertissements" and "#orientation" not in anchors
    chapters = body.select_one(".scheda-capitoli")
    for anchor in anchors:
        assert chapters.select_one(f":scope > section{anchor}"), anchor
    assert not section.select("nav"), "the first part holds no index of its own"
    assert not soup.select("header.ingresso nav"), "one index: the head's seat holds the photograph"


def test_italy_legal_entry_stands_outside_the_competent_actors_register(get):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the arc of
    # four seats on the night became lane B's register of the competent actors (each its name; its official link and
    # host once verified) — the same invariants: four actors, each named, no disc, no glyph; Italy Legal Entry™'s
    # position stated outside the list, in its words
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    section = soup.select_one("section#autorites")
    seats = section.select("ul.scheda-attori__lista > li.scheda-attori__voce")
    assert len(seats) == 4
    assert not any(ICON.findall(str(s)) or s.select(".sez-disc, .sez-tile") for s in seats)
    assert all(_text(s.select_one(".scheda-attori__nome")) for s in seats)
    ile = section.select_one(".scheda-attori__nota")
    assert ile and not ile.find_parent("ul"), "Italy Legal Entry™ stands outside the register"
    assert "n’intervient pas auprès des autorités et ne délivre aucune autorisation" in _text(ile)


def test_a_sheet_s_terms_open_their_locked_definitions_in_place(get):
    terms = {t["key"]: t for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: lane B's
    # disclosures (`scheda-termine`, one open at a time) — the same invariants under their new names; the Italian term is
    # its own run (`span[lang=it]`), so on an Arabic page the control keeps the page's direction — the term on the
    # reading edge, the chevron at the row's end (base.css turns a whole `summary[lang]` left to right)
    disclosures = soup.select("#ressources details.scheda-termine[name='termini']")
    assert len(disclosures) >= 3
    for details in disclosures:
        term = _text(details.select_one("summary"))
        entry = next(t for t in terms.values() if t["term"] == term)
        assert _text(details.select_one(".scheda-termine__corpo p")) == entry["definition"]
        assert details.select_one("summary > span")["lang"] == "it" and not details.select_one("summary").get("lang")
        assert details.select_one(f'a[href$="/glossaire/{entry["key"]}/"]')


@pytest.mark.parametrize("path", ["/fr/parcours/salaried_work/", "/fr/formation/", "/fr/diplomes-et-titres/"])
def test_the_compass_closes_on_the_questionnaire_with_its_caution(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: on a pathway
    # sheet the plate closes the one paper body as its last chapter (lane B) — Formation and Diplômes keep the brand band
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the senior
    # integration review's correction round (P2-3) — the questionnaire's action, its caution and the help line close the
    # page inside ONE compact band with the anti-fraud notice, «la chiusura» (pathways/_chiusura.html): the sheet's last
    # chapter, «Avertissements»; on Formation and Diplômes the page's last band, on pietra. Still the caution whole, the
    # one primary and the help line beside it — and no boussole plate at all (stronger: no `.boussole` of any kind)
    if path.startswith("/fr/parcours/"):
        band = soup.select_one(".scheda-capitoli > section#avertissements.chiusura:last-child")
    else:
        band = soup.select("section.sez")[-1]
        assert band.select_one(".container.chiusura") and band["data-ground"] == "pietra"
    assert band["data-action"] == "orientation"
    # V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule): the plate is the sentence and its action, no compass drawn
    assert not band.select(".boussole, .boussole__ago, svg.boussole")
    assert "Les décisions relèvent des autorités compétentes." in _text(band.select_one(".chiusura__testo"))
    assert len(band.select("a.btn--primary")) == 1 and band.select_one('a.btn--primary[href="/fr/orientation/"]')
    assert band.select_one(".sez-annotation a.email"), "who can help me, beside the action"


# ---- Entreprises (§3.6) ---------------------------------------------------------------------------------------------


def test_the_companies_quote_opens_the_flow_and_the_answer_is_split_on_its_own_colon(get):
    soup = BeautifulSoup(_main(get("/fr/entreprises/")), "html.parser")
    quote = soup.select_one("section#demarche blockquote.imprese-citazione p")
    assert _text(quote) == locked_content.text("p1.companies.quote", "fr")
    # V5.30 Fast Visual Variety Correction §7 ENTREPRISES, «process panels» (V5.20 strict rule; no measured curve, no module)
    # FINAL MICRO-PASS §6 B3 (V5.20; was «the flow in the démarche's stone band, each moment opening on the registry's
    # company-moment glyph» and «the territory's panorama band on paper»): the démarche's band opens on the quotation
    # beside the territory's photograph (the same slot; no panorama band is left), and the three moments follow in the
    # band the panorama held, on paper — the quiet sequence (BRIEF §2.2): no tile, no glyph, no disc in the markup (the
    # sheet's counter draws «1», «2», «3»), each its title
    flow = soup.select_one('section#trois-temps[data-ground="paper"] .flusso')
    assert soup.select_one("section#demarche + section#trois-temps") is not None
    assert not flow.has_attr("data-sec-js") and not soup.select("main [data-flow], main [data-flow-node]")
    assert not soup.select("section#demarche .flusso")
    moments = flow.select("ol.flusso__tappe > li.flusso__tappa")
    assert len(moments) == len(icons.COMPANY_MOMENT) == 3
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: «no decorative
    # numeric markers anywhere» — the sheet's «1 2 3» counter left (was: «no tile, no glyph, no disc in the markup; the
    # sheet's counter draws 1, 2, 3»). Each moment now opens on ITS concept glyph — the registry's COMPANY_MOMENT, in the
    # list's order, exactly one, aria-hidden — a stop on its own hairline; still no tile, no disc, no node, no current
    # stop, and no figure anywhere in a stop (ecosystem/partials/tempi.html; the list stays an <ol>: the order is read)
    for moment, glyph in zip(moments, icons.COMPANY_MOMENT, strict=True):
        stops = moment.select(':scope > span.flusso__segno[aria-hidden="true"]')
        assert len(stops) == 1 and len(stops[0].select("svg")) == 1, moment
        assert stops[0].select_one("svg use")["href"].endswith(f"#icon-{glyph}"), (glyph, stops[0])
        assert not re.search(r"\d", stops[0].get_text()), "no numeral in a stop"
        assert moment.select_one(':scope > span.flusso__filo[aria-hidden="true"]'), "each stop on its hairline"
    assert not flow.select(".flusso__tappe :is(.flusso__nodo, .sez-tile, .sez-disc, [aria-current], .is-current)")
    assert not soup.select_one("section#trois-temps").select("svg:not(.flusso__segno svg)"), "a glyph only as a stop"
    assert all(m.select_one("h3.flusso__titolo").get_text(strip=True) for m in moments)
    opening = soup.select_one("section#demarche .imprese-apertura")
    assert opening.select_one(
        ':scope > blockquote.imprese-citazione + figure.imprese-apertura__foto[data-slot="companies.territory"]'
    )
    assert not soup.select(".sez--panorama")
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
    assert not section.select("[data-seat]")
    # FINAL MICRO-PASS §6 B4 (V5.20; was «the six seats, a row of the registry's recipient glyph tiles, aria-hidden»): the
    # seats left — no tile, no disc, no glyph in the band; the sentence is the one typographic annotation, its six
    # phrases keeping the pattern's pairing attribute, in order, and its head the label
    assert [phrase["data-seggio"] for phrase in sentence.select(".emiciclo__voce")] == [str(n) for n in range(1, 7)]
    assert sentence.select_one(":scope > .emiciclo__capo") is not None
    assert not section.select("ol.emiciclo__seggi, .emiciclo__seggio, .sez-disc, .sez-tile")
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
    # FINAL MICRO-PASS §5 A2 (V5.20 strict rule: the stations' tiles gave way to the quiet sequence marker): each
    # station says its rank, in order, and none draws a node — RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # («no numbering»): the marker is an empty ring (lane B), the rank the ordered list's own, read in the document
    assert all(s.select_one('.dossier__num[aria-hidden="true"]') for s in stations)
    assert not any(_text(s.select_one(".dossier__num")) for s in stations)
    assert soup.select_one("ol.dossier > li.dossier__tappa")
    assert not soup.select("ol.dossier .dossier__nodo, ol.dossier .sez-tile")
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
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the compact head's folio is typographic — no seal —, its title stands
    assert not head.select(".sigillo, [data-mark]") and head.select_one("h1")
    assert _text(head.select_one(".ingresso__lead")) == locked_content.text("p1.companies.intro", "fr")
    assert needs.select_one("section#formulaire form")
    collab = BeautifulSoup(_main(get("/fr/collaboration/institutions/")), "html.parser")
    head = collab.select_one('header.ingresso[data-fronte="civic"][data-compact]')
    assert not head.select(".sigillo, [data-mark]") and head.select_one("h1")
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
    uni_head = uni.select_one('header.ingresso[data-fronte="learning"][data-compact]')
    assert uni_head and not uni_head.select(".sigillo, [data-mark]") and uni_head.select_one("h1")


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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane B):
    # Parcours — the head, «l'esploratore» a paper strip under it, «Comment ça marche» on stone, the space's register
    # on «carta viva», the protection on pietra; a pathway sheet draws no band at all — its head, then ONE paper body
    # of chapters under a rule (test_a_pathway_sheet_draws_no_band_one_paper_body_under_its_head)
    "/fr/parcours/": ["paper", "paper", "stone", "paper", "pietra"],
    "/fr/parcours/salaried_work/": ["paper"],
    "/fr/projet-pilote/": ["night", "brand", "paper", "stone"],
    "/fr/entreprises/": ["paper", "stone", "paper", "stone", "paper", "stone"],
    "/fr/institutions/": ["paper", "night", "stone"],  # V5.30 VARIETY §7: the split's plate, its photograph beside it
    "/fr/universites-et-formation/": ["paper", "brand"],
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
    # senior integration review's correction round (P2-3) — Formation and Diplômes close on ONE band, «la chiusura» on
    # pietra (the anti-fraud notice, the questionnaire's action, the way to the space's register): the register's paper
    # and the boussole's brand leave them; the head, the page's moment, the stone — still no two kinds touching
    "/fr/formation/": ["paper", "paper", "pietra"],
    "/fr/diplomes-et-titres/": ["paper", "paper", "pietra"],
}
#: the route sheets that draw a recipe import the material partial; the two that draw none do not (a page carries only what
#: it draws — Entreprises' and Universités' changes are grounds and a page rule, §3.5; PUB1 NOTES §4)
MATERIA_IMPORTS = {
    "pathways/index.css": True,
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the sheet
    # draws no recipe now (lane B: no pietra band, no «carta viva» — one paper body), so it carries none
    "pathways/sheet.css": False,
    "pathways/training.css": True,
    "pathways/diplomas.css": True,
    "ecosystem/pilot.css": True,
    "ecosystem/institutions.css": True,
    "ecosystem/companies.css": False,
    "ecosystem/universities.css": False,
}
PUB1_SHEETS = (
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: lane B's
    # partials in place of the three it retired (_index.css, _sheet.css, _persone-v2.css) — held to the same discipline
    "apps/pathways/static/pathways/_esplora.css",
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
    # correction round's closing band (P2-3) joins them under the same discipline
    "apps/pathways/static/pathways/_chiusura.css",
    "apps/pathways/static/pathways/_scheda.css",
    "apps/pathways/static/pathways/_spazio.css",
    "apps/pathways/static/pathways/_training.css",
    "apps/pathways/static/pathways/_diplomas.css",
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


def test_a_pathway_sheet_draws_no_band_one_paper_body_under_its_head(get):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the sheet's
    # six bands (paper, stone, night, pietra, paper, brand) became ONE paper body of chapters (lane B) — no two grounds
    # can meet inside it, and the head's ground and the body's are divided by the body's own rule
    soup = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    assert not soup.select(".sez[data-ground]")
    body = soup.select_one(".pathway-entrance ~ .scheda-corpo[data-ground='paper']")
    assert body and body.select_one(".scheda-capitoli > section#etapes")
    css = re.sub(
        r"/\*.*?\*/", "", (ROOT / "apps/pathways/static/pathways/_scheda.css").read_text(encoding="utf-8"), flags=re.S
    )
    assert re.search(r"(?m)^\.scheda-corpo \{[^}]*border-block-start: 1px solid", css)


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
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the trunk's raccordo left with the head's route it rose into — the
    # space's pages draw no raccordo at all
    assert not parcours.select(".sez-raccordo")
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the space's
    # register of links (lane B, pathways/_spazio.html) keeps «carta viva» where the mosaic stood, on all three pages
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the senior
    # integration review's correction round (P2-3) — on /parcours/ alone; Formation and Diplômes lead to it from their
    # closing band (below)
    assert parcours.select_one('section.spazio#espace-personnes[data-ground="paper"][data-luce="origine"]')
    assert parcours.select_one('section.persone-protezione[data-ground="pietra"] aside.protezione')
    # FINAL MICRO-PASS §5 A2 (V5.20 strict rule): the «Comment ça marche» plates carry their quiet markers, no tile —
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no numbering»):
    # each moment's marker is an empty dot, four of them
    assert (
        not parcours.select(".come__tappa .sez-tile, .come__num")
        and len(parcours.select(".come__tappa .come__punto")) == 4
    )
    sheet = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the sheet is
    # ONE paper body (lane B) — the steps a chapter of it, no band, no seam, no night, and the protection the first
    # element of its own chapter (test_a_pathway_sheet_draws_no_band_one_paper_body_under_its_head)
    assert sheet.select_one('.scheda-corpo[data-ground="paper"] section#etapes:not([data-ground])')
    assert not sheet.select(".sez-raccordo, .sez[data-ground]"), "V5.30 VARIETY §5: no line into the night"
    assert sheet.select_one("section#avertissements > .protezione__campo:first-child > aside.protezione")
    diplomas = BeautifulSoup(_main(get("/fr/diplomes-et-titres/")), "html.parser")
    protezione = diplomas.select_one("section.persone-protezione")
    assert protezione["data-ground"] == "pietra" and not protezione.select(".sez-raccordo"), "V5.30 VARIETY §5"
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
    # correction round (P2-3) — the protection on pietra is the page's closing band, the register's «carta viva» left with
    # the register (no grid drawn, no light), its way kept in the band; Formation's order (R5) — the traversata, then the
    # protection on pietra — now ends there
    assert not diplomas.select("section.spazio, [data-luce]")
    assert protezione.select_one('.chiusura a[href="/fr/parcours/#espace-personnes"]')
    training = BeautifulSoup(_main(get("/fr/formation/")), "html.parser")
    assert [s.get("data-sec") for s in training.select(".sez[data-sec]")] == ["filo", "strato"]
    assert training.select_one(
        '.formazione-traversata + section.persone-protezione[data-ground="pietra"][data-action="orientation"]'
    )
    assert not training.select("section.spazio, [data-luce]")
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
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the board's
    # lane names became the explorer's family names (lane B) — the label role by name, four of them; the stations'
    # numerals left with the numbering (no rank figure at all now: the rows' order is the rank, see
    # test_the_explorer_holds_the_eight_pathways_on_their_families)
    names = parcours.select(".esplora__famiglia-nome")
    assert len(names) == 4 and all("t-label" in n["class"] for n in names)
    assert not parcours.select(".tracciato__num, [data-esplora] .t-numeral")
    sheet = BeautifulSoup(_main(get("/fr/parcours/salaried_work/")), "html.parser")
    assert "t-label" in sheet.select_one(".scheda-nav__titolo")["class"]
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
